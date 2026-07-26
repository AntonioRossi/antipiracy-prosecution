"""Secure, resource-bounded XSD 1.1 parsing for readable XML packages."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import os
import re
from types import MappingProxyType
from typing import Mapping
import unicodedata
from xml.etree import ElementTree as ET

import xmlschema
from xmlschema.resources import XMLResource

from . import CONTENT_NAMESPACE, RELATIONS_NAMESPACE, SCHEMA_VERSION
from .canonical import (raw_digest, readable_xml_bytes,
                        strip_structural_whitespace, typed_item_digest,
                        typed_item_record)
from .control import parse_json
from .errors import ParseError, SchemaError, StructuredSourceError
from .profiles import (load_projection_profile, load_xml_profiles,
                       parse_projection_profile, parse_xml_profiles)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_DIRECTORY = os.path.join(ROOT, "structured_source", "schemas")
PARSER_POLICY_PATH = "structured_source/policy/parser.json"
PROJECTION_PROFILE_PATH = "structured_source/profiles/gfm-v1.json"
XML_PROFILE_PATH = "structured_source/profiles/xml-v1.json"
XML_SCHEMA_PATH = "structured_source/schemas/xml.xsd"
SCHEMA_PATHS = MappingProxyType({
    "content-document": "structured_source/schemas/content.xsd",
    "authored-document": "structured_source/schemas/authored.xsd",
    "relation-set": "structured_source/schemas/relations.xsd",
})
PARSER_CONTROL_PATHS = (
    PARSER_POLICY_PATH,
    PROJECTION_PROFILE_PATH,
    XML_PROFILE_PATH,
    XML_SCHEMA_PATH,
    *SCHEMA_PATHS.values(),
)
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
XML_BASE = "{http://www.w3.org/XML/1998/namespace}base"

_POLICY_FIELDS = {
    "parserPolicyVersion", "xmlVersion", "encoding", "unicodeNormalization",
    "xsdVersion", "forbiddenConstructs", "limits",
}
_FORBIDDEN_NAMES = {
    "CDATA", "DOCTYPE", "XInclude", "XLink", "comments",
    "entity-declarations", "external-resources",
    "non-predefined-entity-references", "processing-instructions",
    "raw-html", "raw-markdown", "recovery", "xml-base",
}
MAX_XML_BYTES = 16777216
MAX_DEPTH = 96
MAX_NODES = 200000
MAX_ATTRIBUTES = 64
MAX_TEXT_LENGTH = 2097152
_CURRENT_LIMITS = {
    "attributesPerElement": MAX_ATTRIBUTES,
    "bytes": MAX_XML_BYTES,
    "depth": MAX_DEPTH,
    "nodes": MAX_NODES,
    "textNodeCharacters": MAX_TEXT_LENGTH,
}


def _parse_policy(data: bytes):
    try:
        value = parse_json(data)
    except StructuredSourceError as exc:
        raise ParseError("secure-parser policy is unreadable") from exc
    limits = value.get("limits") if isinstance(value, dict) else None
    if not isinstance(value, dict) or set(value) != _POLICY_FIELDS or \
            value.get("parserPolicyVersion") != "1" or \
            value.get("xmlVersion") != "1.0" or value.get("encoding") != "UTF-8" or \
            value.get("unicodeNormalization") != "NFC" or \
            value.get("xsdVersion") != "1.1" or \
            value.get("forbiddenConstructs") != sorted(_FORBIDDEN_NAMES) or \
            not isinstance(limits, dict) or limits != _CURRENT_LIMITS:
        raise ParseError("secure-parser policy shape/version is not current")
    return value

_FORBIDDEN_LEXICAL = (
    (re.compile(br"<!DOCTYPE", re.IGNORECASE), "DOCTYPE"),
    (re.compile(br"<!ENTITY", re.IGNORECASE), "entity declaration"),
    (re.compile(br"<!\[CDATA\[", re.IGNORECASE), "CDATA"),
    (re.compile(br"<\?[^xX]"), "processing instruction"),
    (re.compile(br"<!--"), "comment"),
)
_NAMED_ENTITY = re.compile(br"&([A-Za-z_:][A-Za-z0-9_.:-]*);")
_ALLOWED_ENTITIES = {b"amp", b"lt", b"gt", b"apos", b"quot"}
_STABLE_ITEM_ID = re.compile(r"[a-z][a-z0-9-]{0,159}\Z")
@dataclass(frozen=True)
class ParsedArtifact:
    kind: str
    profile: str
    root: ET.Element
    raw_bytes: bytes
    raw_digest: str
    fragment_digests: dict[str, str]
    typed_item_records: dict[str, dict]


@dataclass(frozen=True)
class ParserControls:
    """Validated policy, profiles, and schemas from one byte source."""

    limits: Mapping[str, int]
    projection_profile: Mapping
    xml_profiles: Mapping
    schemas: Mapping


def _deep_freeze(value):
    """Make retained parser controls transitively immutable."""
    if isinstance(value, dict):
        return MappingProxyType({
            key: _deep_freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_deep_freeze(item) for item in value)
    return value


def _schema_from_bytes(
        kind: str, schema_data: bytes,
        xml_schema_data: bytes) -> xmlschema.XMLSchema11:
    if kind not in SCHEMA_PATHS:
        raise ParseError("unsupported XML artifact kind %s" % kind)
    try:
        return xmlschema.XMLSchema11(
            [schema_data, xml_schema_data], validation="strict",
            allow="none", defuse="always")
    except (OSError, ValueError, xmlschema.XMLSchemaException) as exc:
        raise SchemaError("current XSD 1.1 schema is invalid: %s" % exc) from exc


def _xsd_named(root: ET.Element, local: str, name: str) -> ET.Element:
    namespace = "{http://www.w3.org/2001/XMLSchema}"
    matches = [node for node in root.findall(namespace + local)
               if node.get("name") == name]
    if len(matches) != 1:
        raise SchemaError("XSD named declaration is not exact: %s" % name)
    return matches[0]


def _xsd_local(value: str | None) -> str:
    return "" if not value else value.rsplit(":", 1)[-1]


def _xsd_attribute_type(attribute: ET.Element) -> str:
    namespace = "{http://www.w3.org/2001/XMLSchema}"
    scalar = _xsd_local(attribute.get("type"))
    if not scalar:
        restriction = attribute.find(".//" + namespace + "restriction")
        scalar = _xsd_local(
            restriction.get("base") if restriction is not None else None)
    if scalar == "positiveInteger":
        return "positive-integer"
    if scalar == "boolean":
        return "boolean"
    return "string"


def _validate_pdf_xsd_profile(schema_data: bytes, profile: dict) -> None:
    """Prove that the PDF XSD and exclusive executable profile agree."""
    namespace = "{http://www.w3.org/2001/XMLSchema}"
    _preflight(schema_data)
    root = _parse_tree(schema_data)
    if root.tag != namespace + "schema":
        raise SchemaError("PDF content XSD root is not exact")
    complex_types = {
        node.get("name"): node for node in root.findall(namespace + "complexType")
        if node.get("name")}
    simple_types = {
        node.get("name") for node in root.findall(namespace + "simpleType")
        if node.get("name")}
    block = _xsd_named(root, "group", "block")
    block_elements = block.findall(
        namespace + "choice/" + namespace + "element")
    bindings = {
        node.get("name"): _xsd_local(node.get("type"))
        for node in block_elements}
    nested_contract = {
        "item": ("listBlock", "listItem"),
        "limitation": ("claimBlock", "limitation"),
        "row": ("tableSection", "tableRow"),
    }
    for item_name, (parent_type, item_type) in nested_contract.items():
        parent = complex_types.get(parent_type)
        matches = ([] if parent is None else [
            node for node in parent.findall(".//" + namespace + "element")
            if node.get("name") == item_name and
            _xsd_local(node.get("type")) == item_type])
        if len(matches) != 1:
            raise SchemaError(
                "PDF XSD nested item binding is not exact: %s" % item_name)
        bindings[item_name] = item_type
    if set(bindings) != set(profile["itemMetadataFields"]):
        raise SchemaError("PDF XSD/profile item-type inventories differ")
    actual_metadata = {}
    for item_type, type_name in bindings.items():
        node = complex_types.get(type_name)
        if node is None:
            raise SchemaError("PDF item XSD type is absent: %s" % type_name)
        attributes = node.findall(".//" + namespace + "attribute")
        xml_ids = [attribute for attribute in attributes
                   if attribute.get("ref") == "xml:id"]
        if len(xml_ids) != 1 or xml_ids[0].get("use") != "required":
            raise SchemaError("PDF XSD item identity is not exact: %s" % item_type)
        actual_metadata[item_type] = {
            attribute.get("name"): _xsd_attribute_type(attribute)
            for attribute in attributes if attribute.get("name")}
    if actual_metadata != profile["itemMetadataFields"]:
        raise SchemaError("PDF XSD/profile item metadata differ")

    groups = {
        node.get("name"): node for node in root.findall(namespace + "group")
        if node.get("name")}
    typed_bindings = {}
    visited_groups = set()
    visited_types = set()

    def add_typed_binding(element):
        name = element.get("name")
        if not name:
            raise SchemaError("PDF typed-content element name is absent")
        type_name = _xsd_local(element.get("type"))
        previous = typed_bindings.setdefault(name, type_name)
        if previous != type_name:
            raise SchemaError(
                "PDF typed-content element binding is ambiguous: %s" % name)
        visit_type(type_name)

    def visit_group(name):
        if name in visited_groups:
            return
        group = groups.get(name)
        if group is None:
            raise SchemaError("PDF typed-content XSD group is absent: %s" % name)
        visited_groups.add(name)
        for element in group.findall(".//" + namespace + "element"):
            add_typed_binding(element)
        for reference in group.findall(".//" + namespace + "group"):
            visit_group(_xsd_local(reference.get("ref")))

    def visit_type(name):
        if not name or name in visited_types or name not in complex_types:
            return
        visited_types.add(name)
        node = complex_types[name]
        extensions = node.findall(".//" + namespace + "extension")
        for extension in extensions:
            visit_type(_xsd_local(extension.get("base")))
        for reference in node.findall(".//" + namespace + "group"):
            visit_group(_xsd_local(reference.get("ref")))
        for element in node.findall(".//" + namespace + "element"):
            add_typed_binding(element)

    visit_group("block")

    def typed_attributes(type_name, active=frozenset()):
        if not type_name or type_name not in complex_types:
            return {}
        if type_name in active:
            raise SchemaError("PDF typed-content XSD inheritance contains a cycle")
        node = complex_types[type_name]
        values = {}
        for extension in node.findall(".//" + namespace + "extension"):
            base = _xsd_local(extension.get("base"))
            inherited = typed_attributes(type_name=base,
                                         active=active | {type_name})
            collision = set(values) & set(inherited)
            if collision:
                raise SchemaError(
                    "PDF typed-content inherited metadata collides")
            values.update(inherited)
        for attribute in node.findall(".//" + namespace + "attribute"):
            if attribute.get("ref") == "xml:id":
                continue
            name = attribute.get("name")
            if not name or name in values:
                raise SchemaError(
                    "PDF typed-content metadata binding is ambiguous")
            values[name] = _xsd_attribute_type(attribute)
        return values

    actual_typed_fields = {
        name: typed_attributes(type_name)
        for name, type_name in sorted(typed_bindings.items())}
    if actual_typed_fields != profile["typedContentNodeFields"]:
        raise SchemaError("PDF XSD/profile typed-content fields differ")

    def typed_value_kind(type_name, active=frozenset()):
        if not type_name:
            return "empty"
        if type_name in simple_types or type_name not in complex_types:
            return "text"
        if type_name in active:
            raise SchemaError("PDF typed-content value model contains a cycle")
        node = complex_types[type_name]
        if node.find(".//" + namespace + "simpleContent") is not None:
            return "text"
        if node.findall(".//" + namespace + "element") or \
                node.findall(".//" + namespace + "group"):
            return "children"
        inherited = {
            typed_value_kind(_xsd_local(extension.get("base")),
                             active | {type_name})
            for extension in node.findall(".//" + namespace + "extension")
            if _xsd_local(extension.get("base")) in complex_types}
        if len(inherited) > 1:
            raise SchemaError("PDF typed-content value model is ambiguous")
        return next(iter(inherited), "empty")

    actual_text_elements = sorted(
        name for name, type_name in typed_bindings.items()
        if typed_value_kind(type_name) == "text")
    actual_child_elements = sorted(
        name for name, type_name in typed_bindings.items()
        if typed_value_kind(type_name) == "children")
    if actual_text_elements != profile["typedContentTextElements"] or \
            actual_child_elements != profile["typedContentChildElements"]:
        raise SchemaError("PDF XSD/profile typed-content value models differ")

    source_document = _xsd_named(root, "complexType", "sourceDocument")
    document_ids = [attribute for attribute in source_document.findall(
        ".//" + namespace + "attribute")
        if attribute.get("ref") == "xml:id"]
    if len(document_ids) != 1 or document_ids[0].get("use") != "required" or \
            profile["documentItem"] != {
                "identityAttribute": "xml:id", "itemType": "document",
                "sourceBinding": "manifest-stored-source",
                "substantiveMetadata": [],
                "typedContent": "ordered-content-children"}:
        raise SchemaError("PDF XSD/profile document item differs")

    identity = _xsd_named(root, "complexType", "documentIdentity")
    identity_fields = {
        node.get("name"): _xsd_attribute_type(node)
        for node in (*identity.findall(".//" + namespace + "attribute"),
                     *identity.findall(".//" + namespace + "element"))
        if node.get("name")}
    if identity_fields != profile["documentMetadataFields"]:
        raise SchemaError("PDF XSD/profile document metadata differ")

    evidence = _xsd_named(root, "complexType", "fragmentEvidence")
    provenance_fields = {
        node.get("name"): _xsd_attribute_type(node)
        for node in evidence.findall(".//" + namespace + "attribute")
        if node.get("name")}
    if provenance_fields != profile["provenanceFields"]:
        raise SchemaError("PDF XSD/profile provenance fields differ")

    dependency = _xsd_named(root, "complexType", "dependency")
    kind = next((node for node in dependency.findall(
        ".//" + namespace + "attribute") if node.get("name") == "kind"), None)
    kinds = sorted(node.get("value") for node in kind.findall(
        ".//" + namespace + "enumeration")) if kind is not None else []
    if kinds != sorted(profile["dependencyKinds"]):
        raise SchemaError("PDF XSD/profile dependency kinds differ")
    patterns = {}
    for name in ("rawDigest", "typedItemDigest"):
        pattern = _xsd_named(root, "simpleType", name).find(
            ".//" + namespace + "pattern")
        if pattern is None:
            raise SchemaError("PDF XSD digest pattern is absent: %s" % name)
        patterns[name] = pattern.get("value")
    union = _xsd_named(root, "simpleType", "dependencyDigest").find(
        namespace + "union")
    assertion = dependency.find(namespace + "assert")
    expected_assertion = (
        "if (@kind = 'asset') then (exists(@digest) and "
        "starts-with(string(@digest), 'sha256/raw:') and not(exists(@itemId))) "
        "else if (@kind = 'document') then (exists(@itemId) = exists(@digest) "
        "and (not(exists(@digest)) or starts-with(string(@digest), "
        "'sha256/typed-item-v1:'))) else (not(exists(@itemId)) and "
        "not(exists(@digest)))")
    if patterns != {
            "rawDigest": "sha256/raw:[0-9a-f]{64}",
            "typedItemDigest": "sha256/typed-item-v1:[0-9a-f]{64}"} or \
            union is None or union.get("memberTypes") != \
            "c:rawDigest c:typedItemDigest" or assertion is None or \
            assertion.get("test") != expected_assertion:
        raise SchemaError("PDF XSD/profile dependency digest law differs")

    origin = _xsd_named(root, "complexType", "origin")
    origins = [node.get("name") for node in origin.findall(
        ".//" + namespace + "element")]
    if origins != [profile["originElement"]]:
        raise SchemaError("PDF XSD/profile origin element differs")


def _validate_authored_xsd_profile(schema_data: bytes, profile: dict) -> None:
    """Prove the complete authored XML grammar agrees with its GFM profile."""
    namespace = "{http://www.w3.org/2001/XMLSchema}"
    versioning = "{http://www.w3.org/2007/XMLSchema-versioning}"
    _preflight(schema_data)
    root = _parse_tree(schema_data)
    if root.tag != namespace + "schema" or root.attrib != {
            "targetNamespace": CONTENT_NAMESPACE,
            "elementFormDefault": "qualified",
            "attributeFormDefault": "unqualified",
            "version": "1", versioning + "minVersion": "1.1"}:
        raise SchemaError("authored XSD root is not exact")

    simple_names = {
        node.get("name") for node in root.findall(namespace + "simpleType")}
    complex_names = {
        node.get("name") for node in root.findall(namespace + "complexType")}
    group_names = {
        node.get("name") for node in root.findall(namespace + "group")}
    element_names = {
        node.get("name") for node in root.findall(namespace + "element")}
    if simple_names != {
            "authoredPresentationId", "authoredRawDigest", "authoredRepoPath",
            "authoredStableId", "bindingKind", "pandocConstructor",
            "topLevelBlockConstructor"} or complex_names != {
                "authoredDocument", "authoredFragment", "authoredFragments",
                "authoredIdentity", "authoredPandoc", "emptyValue",
                "markdownBinding", "pandocArray", "pandocBlock",
                "pandocNode"} or group_names != {"pandocValue"} or \
            element_names != {"authored"}:
        raise SchemaError("authored XSD declaration inventory differs")
    imports = root.findall(namespace + "import")
    if len(imports) != 1 or imports[0].attrib != {
            "namespace": "http://www.w3.org/XML/1998/namespace",
            "schemaLocation": "xml.xsd"}:
        raise SchemaError("authored XSD import closure differs")

    def simple_contract(name):
        simple = _xsd_named(root, "simpleType", name)
        restriction = simple.find(namespace + "restriction")
        if restriction is None or tuple(
                child.tag for child in simple) != (namespace + "restriction",) or \
                set(restriction.attrib) != {"base"} or any(
                    set(child.attrib) != {"value"} or list(child)
                    for child in restriction):
            raise SchemaError("authored XSD simple type is not exact: %s" % name)
        return {
            "base": restriction.get("base"),
            "facets": tuple(
                (child.tag.rsplit("}", 1)[-1], child.get("value"))
                for child in restriction),
        }

    expected_simple = {
        "authoredStableId": {
            "base": "xs:NCName", "facets": (
                ("minLength", "1"), ("maxLength", "160"),
                ("pattern", "[a-z][a-z0-9-]*"))},
        "authoredPresentationId": {
            "base": "xs:NCName", "facets": (
                ("minLength", "5"), ("maxLength", "164"),
                ("pattern", "ssp-[a-z][a-z0-9-]*"))},
        "authoredRepoPath": {
            "base": "xs:string", "facets": (
                ("minLength", "1"), ("maxLength", "512"),
                ("pattern", r"[^\\]*"))},
        "authoredRawDigest": {
            "base": "xs:string", "facets": (
                ("pattern", "sha256/raw:[0-9a-f]{64}"),)},
        "bindingKind": {
            "base": "xs:string", "facets": tuple(
                ("enumeration", value)
                for value in ("block", "claim", "document"))},
    }
    if any(simple_contract(name) != value
           for name, value in expected_simple.items()):
        raise SchemaError("authored XSD identity or fragment grammar differs")

    constructors = sorted({
        *profile["supportedBlockConstructors"],
        *profile["supportedInlineConstructors"],
        *profile["supportedAuxiliaryConstructors"],
    })
    if simple_contract("pandocConstructor") != {
            "base": "xs:string", "facets": tuple(
                ("enumeration", value) for value in constructors)} or \
            simple_contract("topLevelBlockConstructor") != {
                "base": "xs:string", "facets": tuple(
                    ("enumeration", value)
                    for value in profile["topLevelBlockConstructors"])}:
        raise SchemaError("authored XSD/profile constructor inventories differ")

    value_group = _xsd_named(root, "group", "pandocValue")
    choice = value_group.find(namespace + "choice")
    value_nodes = ([] if choice is None else list(choice))
    if tuple(child.tag for child in value_group) != (namespace + "choice",) or \
            any(node.tag != namespace + "element" or
                set(node.attrib) != {"name", "type"} or list(node)
                for node in value_nodes) or \
            tuple((node.get("name"), node.get("type")) for node in value_nodes) != (
            ("string", "xs:string"), ("integer", "xs:integer"),
            ("number", "xs:decimal"), ("boolean", "xs:boolean"),
            ("null", "c:emptyValue"), ("array", "c:pandocArray"),
            ("node", "c:pandocNode")):
        raise SchemaError("authored XSD Pandoc value grammar differs")

    def complex_contract(name):
        node = _xsd_named(root, "complexType", name)
        sequence = node.find(namespace + "sequence")
        sequence_nodes = [] if sequence is None else list(sequence)
        direct_tags = tuple(child.tag.rsplit("}", 1)[-1] for child in node)
        sequence_tags = tuple(
            child.tag.rsplit("}", 1)[-1] for child in sequence_nodes)
        if any(
                child.tag == namespace + "element" and
                (set(child.attrib) - {
                    "name", "type", "minOccurs", "maxOccurs"})
                for child in sequence_nodes) or any(
                    child.tag == namespace + "group" and
                    (set(child.attrib) - {"ref", "minOccurs", "maxOccurs"})
                    for child in sequence_nodes) or any(
                        set(child.attrib) - {
                            "name", "ref", "type", "use", "fixed"}
                        for child in node.findall(namespace + "attribute")) or any(
                            set(child.attrib) != {"test"}
                            for child in node.findall(namespace + "assert")):
            raise SchemaError("authored XSD declaration fields differ")
        elements = tuple(
            tuple(child.get(field) for field in (
                "name", "type", "minOccurs", "maxOccurs"))
            for child in node.findall(
                namespace + "sequence/" + namespace + "element"))
        groups = tuple(
            tuple(child.get(field) for field in (
                "ref", "minOccurs", "maxOccurs"))
            for child in node.findall(
                namespace + "sequence/" + namespace + "group"))
        attributes = tuple(sorted((
            tuple(child.get(field) for field in (
                "name", "ref", "type", "use", "fixed"))
            for child in node.findall(namespace + "attribute")), key=lambda entry: tuple(
                "" if item is None else item for item in entry)))
        assertions = tuple(
            child.get("test") for child in node.findall(namespace + "assert"))
        return node, {
            "elements": elements, "groups": groups,
            "attributes": attributes, "assertions": assertions,
            "directTags": direct_tags, "sequenceTags": sequence_tags,
        }

    def complete_complex(expected):
        has_sequence = bool(expected["elements"] or expected["groups"])
        return {
            **expected,
            "directTags": (
                *(("sequence",) if has_sequence else ()),
                *("attribute",) * len(expected["attributes"]),
                *("assert",) * len(expected["assertions"])),
            "sequenceTags": (
                *("element",) * len(expected["elements"]),
                *("group",) * len(expected["groups"])),
        }

    expected_complex = {
        "emptyValue": {
            "elements": (), "groups": (), "attributes": (), "assertions": ()},
        "pandocArray": {
            "elements": (), "groups": (("c:pandocValue", "0", "unbounded"),),
            "attributes": (), "assertions": ()},
        "pandocNode": {
            "elements": (), "groups": (("c:pandocValue", "0", "1"),),
            "attributes": (("constructor", None, "c:pandocConstructor",
                            "required", None),), "assertions": ()},
        "pandocBlock": {
            "elements": (), "groups": (("c:pandocValue", "0", "1"),),
            "attributes": (("constructor", None,
                            "c:topLevelBlockConstructor", "required", None),),
            "assertions": ()},
        "authoredPandoc": {
            "elements": (("block", "c:pandocBlock", "1", "100000"),),
            "groups": (),
            "attributes": tuple(sorted((
                ("apiVersion", None, None, "required", ".".join(
                    str(value) for value in profile["pandocApiVersion"])),
                ("profile", None, None, "required", profile["profileId"])))),
            "assertions": ()},
        "authoredFragments": {
            "elements": (("fragment", "c:authoredFragment", "1", "100000"),),
            "groups": (), "attributes": (), "assertions": ()},
        "authoredIdentity": {
            "elements": (), "groups": (),
            "attributes": (("documentId", None, "c:authoredStableId",
                            "required", None),), "assertions": ()},
        "markdownBinding": {
            "elements": (), "groups": (),
            "attributes": tuple(sorted((
                ("path", None, "c:authoredRepoPath", "required", None),
                ("rawDigest", None, "c:authoredRawDigest", "required", None),
                ("size", None, "xs:nonNegativeInteger", "required", None)))),
            "assertions": ()},
        "authoredDocument": {
            "elements": (
                ("documentIdentity", "c:authoredIdentity", None, None),
                ("markdownBinding", "c:markdownBinding", None, None),
                ("fragments", "c:authoredFragments", None, None),
                ("pandoc", "c:authoredPandoc", None, None)),
            "groups": (),
            "attributes": tuple(sorted((
                ("schemaProfile", None, None, "required",
                 "authored-markdown-v1"),
                ("schemaVersion", None, None, "required", "1")))),
            "assertions": ()},
    }
    for name, expected in expected_complex.items():
        unused_node, actual = complex_contract(name)
        if actual != complete_complex(expected):
            raise SchemaError("authored XSD Pandoc or envelope grammar differs")

    fragment, fragment_contract = complex_contract("authoredFragment")
    expected_fragment = {
        "elements": (("excerpt", None, None, None),), "groups": (),
        "attributes": (
            (None, "xml:id", None, "required", None),
            ("bindingDigest", None, "c:authoredRawDigest", "required", None),
            ("bindingKind", None, "c:bindingKind", "required", None),
            ("presentationId", None, "c:authoredPresentationId", "required", None),
            ("semanticPath", None, "xs:string", "required", None)),
        "assertions": (
            "matches(string(@xml:id), '^[a-z][a-z0-9-]*$')",),
    }
    excerpt = fragment.find(namespace + "sequence/" + namespace + "element")
    excerpt_restriction = (None if excerpt is None else excerpt.find(
        namespace + "simpleType/" + namespace + "restriction"))
    excerpt_contract = None if excerpt_restriction is None else {
        "base": excerpt_restriction.get("base"),
        "facets": tuple(
            (child.tag.rsplit("}", 1)[-1], child.get("value"))
            for child in excerpt_restriction),
    }
    if fragment_contract != complete_complex(expected_fragment) or \
            excerpt is None or set(excerpt.attrib) != {"name"} or \
            tuple(child.tag for child in excerpt) != (namespace + "simpleType",) or \
            excerpt_contract != {
            "base": "xs:string", "facets": (
                ("minLength", "1"), ("maxLength", "1000000"))}:
        raise SchemaError("authored XSD fragment grammar differs")

    authored = _xsd_named(root, "element", "authored")
    if authored.attrib != {"name": "authored", "type": "c:authoredDocument"}:
        raise SchemaError("authored XSD document root differs")


def _validate_relation_xsd_profile(schema_data: bytes, profiles: dict) -> None:
    """Prove the complete relation XML grammar fits its exclusive profiles."""
    namespace = "{http://www.w3.org/2001/XMLSchema}"
    versioning = "{http://www.w3.org/2007/XMLSchema-versioning}"
    _preflight(schema_data)
    root = _parse_tree(schema_data)
    if root.tag != namespace + "schema" or root.attrib != {
            "targetNamespace": RELATIONS_NAMESPACE,
            "elementFormDefault": "qualified",
            "attributeFormDefault": "unqualified",
            "version": "1", versioning + "minVersion": "1.1"}:
        raise SchemaError("relation XSD root is not exact")

    simple_names = {
        node.get("name") for node in root.findall(namespace + "simpleType")}
    complex_names = {
        node.get("name") for node in root.findall(namespace + "complexType")}
    element_names = {
        node.get("name") for node in root.findall(namespace + "element")}
    if simple_names != {"stableId", "typedItemDigest"} or \
            complex_names != {
                "assertionField", "endpoint", "identity", "relation",
                "relationSet"} or element_names != {"relations"} or \
            root.findall(namespace + "group"):
        raise SchemaError("relation XSD declaration inventory differs")
    imports = root.findall(namespace + "import")
    if len(imports) != 1 or imports[0].attrib != {
            "namespace": "http://www.w3.org/XML/1998/namespace",
            "schemaLocation": "xml.xsd"}:
        raise SchemaError("relation XSD import closure differs")

    def simple_contract(name):
        simple = _xsd_named(root, "simpleType", name)
        restriction = simple.find(namespace + "restriction")
        if simple.attrib != {"name": name} or restriction is None or tuple(
                child.tag for child in simple) != (namespace + "restriction",) or \
                set(restriction.attrib) != {"base"} or any(
                    set(child.attrib) != {"value"} or list(child)
                    for child in restriction):
            raise SchemaError(
                "relation XSD simple type is not exact: %s" % name)
        return {
            "base": restriction.get("base"),
            "facets": tuple(
                (child.tag.rsplit("}", 1)[-1], child.get("value"))
                for child in restriction),
        }

    if simple_contract("stableId") != {
            "base": "xs:NCName", "facets": (
                ("minLength", "1"), ("maxLength", "160"))} or \
            simple_contract("typedItemDigest") != {
                "base": "xs:string", "facets": (
                    ("pattern", "sha256/typed-item-v1:[0-9a-f]{64}"),)}:
        raise SchemaError("relation XSD scalar grammar differs")

    def attributes(node):
        return tuple(
            tuple(child.get(field) for field in (
                "name", "ref", "type", "use", "fixed"))
            for child in node.findall(namespace + "attribute"))

    def sequence_contract(name):
        node = _xsd_named(root, "complexType", name)
        sequence = node.find(namespace + "sequence")
        if node.attrib != {"name": name} or sequence is None or tuple(
                child.tag for child in node) != (
                    namespace + "sequence",
                    *(namespace + "attribute",) * len(
                        node.findall(namespace + "attribute"))) or any(
                    child.tag != namespace + "element" or
                    set(child.attrib) - {
                        "name", "type", "minOccurs", "maxOccurs"} or
                    list(child)
                    for child in sequence):
            raise SchemaError(
                "relation XSD complex declaration is not exact: %s" % name)
        return {
            "elements": tuple(
                tuple(child.get(field) for field in (
                    "name", "type", "minOccurs", "maxOccurs"))
                for child in sequence),
            "attributes": attributes(node),
        }

    identity = _xsd_named(root, "complexType", "identity")
    endpoint = _xsd_named(root, "complexType", "endpoint")
    for name, node, expected in (
            ("identity", identity, (
                ("relationSetId", None, "r:stableId", "required", None),
                ("profile", None, "r:stableId", "required", None),
                ("owner", None, "xs:string", "required", None),
                ("scope", None, "r:stableId", "required", None),
                ("status", None, "r:stableId", "required", None))),
            ("endpoint", endpoint, (
                ("role", None, "r:stableId", "required", None),
                ("documentId", None, "r:stableId", "required", None),
                ("fragmentId", None, "r:stableId", "required", None),
                ("fragmentContentDigest", None, "r:typedItemDigest",
                 "required", None)))):
        if node.attrib != {"name": name} or tuple(
                child.tag for child in node) != (
                    namespace + "attribute",) * len(expected) or \
                attributes(node) != expected:
            raise SchemaError(
                "relation XSD envelope grammar differs: %s" % name)

    assertion = _xsd_named(root, "complexType", "assertionField")
    simple_content = assertion.find(namespace + "simpleContent")
    extension = (None if simple_content is None else
                 simple_content.find(namespace + "extension"))
    if assertion.attrib != {"name": "assertionField"} or \
            tuple(child.tag for child in assertion) != (
                namespace + "simpleContent",) or simple_content is None or \
            tuple(child.tag for child in simple_content) != (
                namespace + "extension",) or extension is None or \
            extension.attrib != {"base": "xs:string"} or tuple(
                child.tag for child in extension) != (
                    namespace + "attribute",) or attributes(extension) != (
                        ("name", None, "r:stableId", "required", None),):
        raise SchemaError("relation XSD assertion-field grammar differs")

    if sequence_contract("relation") != {
            "elements": (
                ("endpoint", "r:endpoint", "2", "32"),
                ("assertionField", "r:assertionField", "1", "64")),
            "attributes": (
                (None, "xml:id", None, "required", None),
                ("relationId", None, "r:stableId", "required", None),
                ("type", None, "r:stableId", "required", None),
                ("direction", None, "r:stableId", "required", None),
                ("semanticOwner", None, "xs:string", "required", None))} or \
            sequence_contract("relationSet") != {
                "elements": (
                    ("identity", "r:identity", None, None),
                    ("relation", "r:relation", "1", "100000")),
                "attributes": (
                    ("schemaProfile", None, "r:stableId", "required", None),
                    ("schemaVersion", None, "xs:string", "required", "1"))}:
        raise SchemaError("relation XSD relation grammar differs")

    relations = _xsd_named(root, "element", "relations")
    if relations.attrib != {"name": "relations", "type": "r:relationSet"} or \
            list(relations):
        raise SchemaError("relation XSD document root differs")

    for profile_id, definition in profiles.items():
        vocabularies = (
            (profile_id,), (definition["relationType"],),
            definition["directions"], definition["endpointRoles"],
            definition["requiredEndpointRoles"],
            definition["assertionFields"])
        if any(
                _STABLE_ITEM_ID.fullmatch(value) is None
                for vocabulary in vocabularies for value in vocabulary):
            raise SchemaError("relation XSD/profile vocabulary differs")


def load_parser_controls(read_bytes) -> ParserControls:
    """Load every package-parser control through one retained-byte reader."""
    if not callable(read_bytes):
        raise TypeError("parser control reader must be callable")
    policy = _parse_policy(read_bytes(PARSER_POLICY_PATH))
    projection = parse_projection_profile(read_bytes(PROJECTION_PROFILE_PATH))
    xml_profiles = parse_xml_profiles(read_bytes(XML_PROFILE_PATH), projection)
    xml_schema_data = read_bytes(XML_SCHEMA_PATH)
    schema_data = {
        kind: read_bytes(path) for kind, path in SCHEMA_PATHS.items()}
    xsd_namespace = "http://www.w3.org/2001/XMLSchema"
    for data in (xml_schema_data, *schema_data.values()):
        _preflight(data, policy["limits"])
        _closed_tree_checks(
            _parse_tree(data), xsd_namespace, "schema",
            limits=policy["limits"])
    _validate_pdf_xsd_profile(
        schema_data["content-document"],
        xml_profiles["contentDocuments"]["pdf-evidence-transcription-v1"])
    _validate_authored_xsd_profile(
        schema_data["authored-document"], projection)
    _validate_relation_xsd_profile(
        schema_data["relation-set"], xml_profiles["relationSets"])
    schemas = {
        kind: _schema_from_bytes(kind, data, xml_schema_data)
        for kind, data in schema_data.items()}
    return ParserControls(
        limits=MappingProxyType(dict(policy["limits"])),
        projection_profile=_deep_freeze(projection),
        xml_profiles=_deep_freeze(xml_profiles),
        schemas=MappingProxyType(schemas),
    )


@lru_cache(maxsize=1)
def _default_parser_controls() -> ParserControls:
    def read(path):
        try:
            with open(os.path.join(ROOT, *path.split("/")), "rb") as handle:
                return handle.read()
        except OSError as exc:
            raise ParseError("parser control is unreadable: %s" % path) from exc
    return load_parser_controls(read)


def _schema(kind: str) -> xmlschema.XMLSchema11:
    try:
        return _default_parser_controls().schemas[kind]
    except KeyError as exc:
        raise ParseError("unsupported XML artifact kind %s" % kind) from exc


def _active_limits(limits=None):
    return (limits if limits is not None else {
        "bytes": MAX_XML_BYTES,
        "depth": MAX_DEPTH,
        "nodes": MAX_NODES,
        "attributesPerElement": MAX_ATTRIBUTES,
        "textNodeCharacters": MAX_TEXT_LENGTH,
    })


def _preflight(data: bytes, limits=None) -> None:
    if not isinstance(data, bytes):
        raise TypeError("XML parser input must be bytes")
    active = _active_limits(limits)
    if not data or len(data) > active["bytes"]:
        raise ParseError("XML byte size is outside the closed resource limit")
    if data.startswith((b"\xef\xbb\xbf", b"\xff\xfe", b"\xfe\xff", b"\x00")):
        raise ParseError("readable XML must use UTF-8")
    if b"\r" in data:
        raise ParseError("readable XML must use LF line endings")
    if b"\t" in data:
        raise ParseError("readable XML must not contain literal tabs")
    if data.startswith(b"<?xml") and not data.startswith(
            b'<?xml version="1.0" encoding="UTF-8"?>'):
        raise ParseError(
            "readable XML declaration must select XML 1.0 and UTF-8")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ParseError("readable XML is not UTF-8") from exc
    if unicodedata.normalize("NFC", text) != text:
        raise ParseError("readable XML text is not NFC")
    for pattern, label in _FORBIDDEN_LEXICAL:
        if pattern.search(data):
            raise ParseError("readable XML contains forbidden %s" % label)
    for match in _NAMED_ENTITY.finditer(data):
        if match.group(1) not in _ALLOWED_ENTITIES:
            raise ParseError(
                "readable XML contains a non-predefined entity reference")


def _parse_tree(data: bytes) -> ET.Element:
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True,
                                                insert_pis=True))
    try:
        root = ET.fromstring(data, parser=parser)
    except ET.ParseError as exc:
        raise ParseError("XML is not well formed: %s" % exc) from exc
    if any(not isinstance(node.tag, str) for node in root.iter()):
        raise ParseError("comments and processing instructions are prohibited")
    return root


def _closed_tree_checks(
        root: ET.Element, expected_namespace: str, expected_root: str, *,
        additional_namespaces: frozenset[str] = frozenset(),
        limits=None,
) -> list[tuple[ET.Element, str]]:
    if not isinstance(expected_namespace, str) or not expected_namespace or \
            any(character in expected_namespace for character in "{}\x00") or \
            not isinstance(expected_root, str) or not expected_root or \
            any(character in expected_root for character in "{}:/\x00"):
        raise ParseError("expected XML namespace/root is malformed")
    if root.tag != "{%s}%s" % (expected_namespace, expected_root):
        raise ParseError("XML root does not match the selected artifact kind")
    active = _active_limits(limits)
    stack = [(root, 1)]
    nodes = 0
    identifiers: set[str] = set()
    addressable: list[tuple[ET.Element, str]] = []
    allowed_namespaces = {expected_namespace, *additional_namespaces}
    while stack:
        node, depth = stack.pop()
        nodes += 1
        if nodes > active["nodes"] or depth > active["depth"]:
            raise ParseError("XML tree exceeds a closed resource limit")
        if len(node.attrib) > active["attributesPerElement"]:
            raise ParseError("XML element exceeds the attribute limit")
        for value in (node.text, node.tail):
            if value is not None and len(value) > active["textNodeCharacters"]:
                raise ParseError("XML text node exceeds the text limit")
        if XML_BASE in node.attrib:
            raise ParseError("xml:base is prohibited")
        namespace = node.tag[1:].split("}", 1)[0] \
            if node.tag.startswith("{") else ""
        if namespace not in allowed_namespaces:
            raise ParseError("foreign element namespace is prohibited")
        identifier = node.get(XML_ID)
        if identifier is not None:
            if identifier in identifiers:
                raise ParseError("duplicate xml:id %s" % identifier)
            identifiers.add(identifier)
            addressable.append((node, namespace))
        stack.extend((child, depth + 1) for child in reversed(list(node)))
    return addressable


def parse_validated_xml(data: bytes, schema: bytes, *,
                        expected_namespace: str,
                        expected_root: str,
                        controls: ParserControls | None = None) -> ET.Element:
    """Secure-parse one registered XML document against a closed XSD 1.1.

    This is the public extension point for consumer-owned XML namespaces. A
    caller supplies the exact tracked, self-contained schema bytes; imports,
    includes, overrides, and other resolver-dependent schema composition are
    prohibited. The same lexical and resource limits used for package XML
    apply before strict schema validation.
    """
    limits = controls.limits if controls is not None else None
    _preflight(data, limits)
    _preflight(schema, limits)
    root = _parse_tree(data)
    _closed_tree_checks(
        root, expected_namespace, expected_root, limits=limits)

    xsd_namespace = "http://www.w3.org/2001/XMLSchema"
    schema_root = _parse_tree(schema)
    _closed_tree_checks(
        schema_root, xsd_namespace, "schema", limits=limits)
    if schema_root.tag != "{%s}schema" % xsd_namespace or \
            schema_root.get("targetNamespace") != expected_namespace:
        raise SchemaError("XSD target namespace does not match the XML contract")
    prohibited = {"include", "import", "redefine", "override"}
    if any(node.tag == "{%s}%s" % (xsd_namespace, local)
           for node in schema_root.iter() for local in prohibited):
        raise SchemaError("consumer XSD must be self-contained")
    try:
        schema_resource = XMLResource(
            schema, base_url=ROOT, allow="sandbox", defuse="always")
        validator = xmlschema.XMLSchema11(
            schema_resource, validation="strict", allow="sandbox",
            defuse="always")
        document_resource = XMLResource(
            data, base_url=ROOT, allow="sandbox", defuse="always")
        errors = list(validator.iter_errors(
            document_resource, validation="lax"))
    except xmlschema.XMLSchemaException as exc:
        raise SchemaError("current XSD 1.1 schema is invalid: %s" % exc) from exc
    if errors:
        detail = "; ".join(error.reason for error in errors[:8])
        raise SchemaError("XSD 1.1 validation failed: %s" % detail)
    return root


def _resource_and_profile_checks(
        root: ET.Element, kind: str, *, xml_profiles=None,
        projection_profile=None, limits=None) -> None:
    expected_namespace = (RELATIONS_NAMESPACE if kind == "relation-set"
                          else CONTENT_NAMESPACE)
    expected_root = {
        "content-document": "source",
        "authored-document": "authored",
        "relation-set": "relations",
    }.get(kind)
    if expected_root is None:
        raise ParseError("unsupported XML artifact kind %s" % kind)
    additional = (frozenset({CONTENT_NAMESPACE})
                  if kind == "relation-set" else frozenset())
    _closed_tree_checks(
        root, expected_namespace, expected_root,
        additional_namespaces=additional,
        limits=limits,
    )

    profile = root.get("schemaProfile")
    if not profile or root.get("schemaVersion") != SCHEMA_VERSION:
        raise ParseError("XML schema profile/version is absent or unsupported")
    profiles = xml_profiles if xml_profiles is not None else load_xml_profiles()
    if kind == "content-document":
        definition = profiles["contentDocuments"].get(profile)
        if definition is None:
            raise ParseError("content-document schema profile is unsupported")
        namespace = "{%s}" % CONTENT_NAMESPACE
        origin = root.find(namespace + "origin")
        projection = root.find(namespace + "projectionPolicy")
        actual_origin = ([child.tag.rsplit("}", 1)[-1] for child in origin]
                         if origin is not None else [])
        if actual_origin != [definition["originElement"]] or projection is None or \
                projection.get("profile") != definition["projectionProfile"] or \
                projection.get("noticeVersion") != definition["noticeVersion"]:
            raise ParseError("content-document profile controls do not match the XML")
        content = root.find(namespace + "content")
        if content is None:
            raise ParseError("content-document item surface is absent")
        declared_metadata = definition["itemMetadataFields"]
        item_ids = []
        for node in content.iter():
            identifier = node.get(XML_ID)
            if identifier is None:
                continue
            if _STABLE_ITEM_ID.fullmatch(identifier) is None:
                raise ParseError(
                    "content item identity is outside the stable-ID profile")
            local = node.tag.rsplit("}", 1)[-1]
            permitted = declared_metadata.get(local)
            if permitted is None:
                raise ParseError(
                    "content item type is outside the closed profile: %s" % local)
            metadata = sorted(
                name.rsplit("}", 1)[-1] for name in node.attrib
                if name != XML_ID)
            if not set(metadata).issubset(permitted):
                raise ParseError(
                    "content item metadata is outside its closed type: %s" % local)
            item_ids.append(identifier)
        if not item_ids or len(item_ids) != len(set(item_ids)):
            raise ParseError("content-document item identity census is not exact")
    elif kind == "authored-document":
        projection_profile = (projection_profile if projection_profile is not None
                              else load_projection_profile())
        if profile != "authored-markdown-v1":
            raise ParseError("authored-document schema profile is unsupported")
        namespace = "{%s}" % CONTENT_NAMESPACE
        pandoc = root.find(namespace + "pandoc")
        fragments_node = root.find(namespace + "fragments")
        binding = root.find(namespace + "markdownBinding")
        identity = root.find(namespace + "documentIdentity")
        if pandoc is None or fragments_node is None or binding is None or \
                identity is None or \
                pandoc.get("profile") != projection_profile["profileId"] or \
                pandoc.get("apiVersion") != ".".join(
                    str(item) for item in projection_profile["pandocApiVersion"]):
            raise ParseError("authored-document profile controls do not match the XML")
        path = binding.get("path", "")
        if os.path.isabs(path) or "\\" in path or any(
                part in {"", ".", ".."} for part in path.split("/")):
            raise ParseError("authored Markdown binding path is not canonical")
        allowed = set(projection_profile["supportedBlockConstructors"]) | \
            set(projection_profile["supportedInlineConstructors"]) | \
            set(projection_profile["supportedAuxiliaryConstructors"])
        top_level = set(projection_profile["topLevelBlockConstructors"])
        for block in pandoc.findall(namespace + "block"):
            if block.get("constructor") not in top_level:
                raise ParseError("authored document has an unsupported top-level constructor")
            for node in block.iter(namespace + "node"):
                if node.get("constructor") not in allowed:
                    raise ParseError("authored XML has an unsupported Pandoc constructor")
        fragment_ids = []
        presentation_ids = []
        prefix = projection_profile["stableAnchorPrefix"]
        for fragment in fragments_node.findall(namespace + "fragment"):
            fragment_id = fragment.get(XML_ID, "")
            presentation_id = fragment.get("presentationId", "")
            if presentation_id != prefix + fragment_id:
                raise ParseError("authored fragment and presentation identities disagree")
            fragment_ids.append(fragment_id)
            presentation_ids.append(presentation_id)
        if not fragment_ids or len(fragment_ids) != len(set(fragment_ids)) or \
                len(presentation_ids) != len(set(presentation_ids)):
            raise ParseError("authored fragment identity inventory is not exact")
    else:
        definition = profiles["relationSets"].get(profile)
        if definition is None:
            raise ParseError("relation-set schema profile is unsupported")
        namespace = "{%s}" % RELATIONS_NAMESPACE
        identity = root.find(namespace + "identity")
        if identity is None or identity.get("profile") != profile:
            raise ParseError("relation-set identity profile is stale")
        for relation in root.findall(namespace + "relation"):
            if relation.get("type") != definition["relationType"] or \
                    relation.get("direction") not in definition["directions"]:
                raise ParseError("relation type/direction is outside its closed profile")
            roles = [item.get("role") for item in relation.findall(namespace + "endpoint")]
            if not set(roles).issubset(definition["endpointRoles"]) or \
                    not set(definition["requiredEndpointRoles"]).issubset(roles):
                raise ParseError("relation endpoint role is outside its closed profile")
            fields = [item.get("name") for item in relation.findall(
                namespace + "assertionField")]
            if len(fields) != len(set(fields)) or \
                    not set(fields).issubset(definition["assertionFields"]):
                raise ParseError("relation assertion field is outside its closed profile")


def _typed_scalar(field_type: str, value: str):
    if field_type == "positive-integer":
        try:
            converted = int(value)
        except ValueError as exc:
            raise ParseError("typed item integer metadata is malformed") from exc
        if converted <= 0:
            raise ParseError("typed item integer metadata is not positive")
        return converted
    if field_type == "boolean":
        if value in {"true", "1"}:
            return True
        if value in {"false", "0"}:
            return False
        raise ParseError("typed item boolean metadata is malformed")
    if field_type == "string":
        return value
    raise ParseError("typed item metadata type is outside the profile")


def _typed_content_node(
        node: ET.Element, node_fields, text_elements, child_elements) -> dict:
    attributes = {}
    identifier = node.get(XML_ID)
    item_type = node.tag.rsplit("}", 1)[-1]
    field_types = node_fields.get(item_type)
    if field_types is None:
        raise ParseError("PDF typed-content node is outside the profile")
    children = list(node)
    if item_type in text_elements:
        if children:
            raise ParseError("PDF typed-content text node has child content")
    elif item_type in child_elements:
        if node.text is not None:
            raise ParseError("PDF typed-content container has untyped text")
    elif node.text is not None or children:
        raise ParseError("PDF typed-content empty node has content")
    for qname, value in node.attrib.items():
        if qname == XML_ID:
            continue
        local = qname.rsplit("}", 1)[-1]
        if local not in field_types:
            raise ParseError("PDF typed-content field is outside the profile")
        attributes[local] = _typed_scalar(field_types[local], value)
    return {
        "attributes": attributes,
        "children": [
            _typed_content_node(
                child, node_fields, text_elements, child_elements)
            for child in children],
        "element": item_type,
        **({"itemId": identifier} if identifier is not None else {}),
        "text": node.text if not children else None,
    }


def _pdf_typed_items(
        root: ET.Element, profile: str, *,
        xml_profiles=None) -> tuple[dict[str, str], dict[str, dict]]:
    namespace = "{%s}" % CONTENT_NAMESPACE
    identity = root.find(namespace + "documentIdentity")
    content = root.find(namespace + "content")
    if identity is None or content is None:
        raise ParseError("PDF typed item surface is incomplete")
    document_id = identity.get("documentId", "")
    profiles = xml_profiles if xml_profiles is not None else load_xml_profiles()
    definition = profiles["contentDocuments"][profile]
    metadata_fields = definition["itemMetadataFields"]
    node_fields = definition["typedContentNodeFields"]
    text_elements = frozenset(definition["typedContentTextElements"])
    child_elements = frozenset(definition["typedContentChildElements"])
    records = {}
    root_id = root.get(XML_ID)
    document_item = definition["documentItem"]
    if not root_id:
        raise ParseError("PDF typed document item identity is absent")
    records[root_id] = typed_item_record(
        authority_scheme=profile, schema_profile=profile,
        document_id=document_id, item_id=root_id,
        item_type=document_item["itemType"],
        typed_content=[
            _typed_content_node(
                child, node_fields, text_elements, child_elements)
            for child in content],
        substantive_metadata={},
    )
    for node in content.iter():
        item_id = node.get(XML_ID)
        if item_id is None:
            continue
        item_type = node.tag.rsplit("}", 1)[-1]
        permitted = metadata_fields.get(item_type)
        if permitted is None:
            raise ParseError("PDF typed item type is outside the profile")
        metadata = {}
        for qname, value in node.attrib.items():
            if qname == XML_ID:
                continue
            name = qname.rsplit("}", 1)[-1]
            if name not in permitted:
                raise ParseError("PDF typed item metadata is outside the profile")
            metadata[name] = _typed_scalar(permitted[name], value)
        typed_content = {
            "children": [
                _typed_content_node(
                    child, node_fields, text_elements, child_elements)
                for child in node],
            "text": node.text if not list(node) else None,
        }
        records[item_id] = typed_item_record(
            authority_scheme=profile, schema_profile=profile,
            document_id=document_id, item_id=item_id, item_type=item_type,
            typed_content=typed_content, substantive_metadata=metadata,
        )
    digests = {
        item_id: typed_item_digest(
            authority_scheme=record["authorityScheme"],
            schema_profile=record["schemaProfile"],
            document_id=record["documentId"], item_id=record["itemId"],
            item_type=record["itemType"],
            typed_content=record["typedContent"],
            substantive_metadata=record["substantiveMetadata"])
        for item_id, record in records.items()
    }
    return digests, records


def parse_artifact(
        data: bytes, kind: str, *,
        controls: ParserControls | None = None) -> ParsedArtifact:
    """Securely parse, XSD-validate, and digest one package."""
    active_controls = controls or _default_parser_controls()
    limits = active_controls.limits
    _preflight(data, limits)
    root = _parse_tree(data)
    _resource_and_profile_checks(
        root, kind, xml_profiles=active_controls.xml_profiles,
        projection_profile=active_controls.projection_profile,
        limits=limits)
    try:
        schema = active_controls.schemas[kind]
    except KeyError as exc:
        raise ParseError("unsupported XML artifact kind %s" % kind) from exc
    resource = XMLResource(
        root, base_url=SCHEMA_DIRECTORY, allow="sandbox", defuse="always")
    # ``lax`` here is xmlschema's error-collection mode, not permissive
    # schema handling: every reported validation defect is rejected below.
    errors = list(schema.iter_errors(resource, validation="lax"))
    if errors:
        detail = "; ".join(error.reason for error in errors[:8])
        raise SchemaError("XSD 1.1 validation failed: %s" % detail)
    strip_structural_whitespace(root)
    if data != readable_xml_bytes(root):
        raise ParseError(
            "registered XML does not equal the readable storage serialization")
    if kind == "authored-document":
        try:
            from .markdown import _validate_authored_root, authored_typed_items
            _validate_authored_root(root)
            fragments, typed_records = authored_typed_items(root)
        except StructuredSourceError as exc:
            raise ParseError("authored XML semantic model is invalid: %s" % exc) from exc
    profile = root.get("schemaProfile")
    if kind == "content-document" and profile == \
            "pdf-evidence-transcription-v1":
        fragments, typed_records = _pdf_typed_items(
            root, profile, xml_profiles=active_controls.xml_profiles)
    elif kind == "authored-document":
        pass
    else:
        fragments = {}
        typed_records = {}
    return ParsedArtifact(
        kind=kind,
        profile=profile,
        root=root,
        raw_bytes=data,
        raw_digest=raw_digest(data),
        fragment_digests=fragments,
        typed_item_records=typed_records,
    )
