"""Secure, resource-bounded XSD 1.1 parsing for canonical packages."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import json
import os
import re
import unicodedata
from xml.etree import ElementTree as ET

import xmlschema
from xmlschema.resources import XMLResource

from . import CONTENT_NAMESPACE, RELATIONS_NAMESPACE, SCHEMA_VERSION
from .canonical import raw_digest, semantic_digest
from .errors import ParseError, SchemaError, StructuredSourceError
from .profiles import load_projection_profile, load_xml_profiles

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_DIRECTORY = os.path.join(ROOT, "structured_source", "schemas")
POLICY_PATH = os.path.join(ROOT, "structured_source", "policy", "parser.json")
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
XML_BASE = "{http://www.w3.org/XML/1998/namespace}base"

_POLICY_FIELDS = {
    "parserPolicyVersion", "xmlVersion", "encoding", "unicodeNormalization",
    "xsdVersion", "canonicalizationVersion", "digestDomainVersion",
    "forbiddenConstructs", "limits",
}
_LIMIT_FIELDS = {"attributesPerElement", "bytes", "depth", "nodes",
                 "textNodeCharacters"}
_FORBIDDEN_NAMES = {
    "CDATA", "DOCTYPE", "XInclude", "XLink", "comments",
    "entity-declarations", "external-resources",
    "non-predefined-entity-references", "processing-instructions",
    "raw-html", "raw-markdown", "recovery", "xml-base",
}


def _load_policy():
    try:
        with open(POLICY_PATH, "r", encoding="utf-8") as handle:
            value = json.load(handle)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ParseError("secure-parser policy is unreadable") from exc
    limits = value.get("limits") if isinstance(value, dict) else None
    if not isinstance(value, dict) or set(value) != _POLICY_FIELDS or \
            value.get("parserPolicyVersion") != "1" or \
            value.get("xmlVersion") != "1.0" or value.get("encoding") != "UTF-8" or \
            value.get("unicodeNormalization") != "NFC" or \
            value.get("xsdVersion") != "1.1" or \
            value.get("canonicalizationVersion") != "xc1" or \
            value.get("digestDomainVersion") != "ssp-xd1" or \
            value.get("forbiddenConstructs") != sorted(_FORBIDDEN_NAMES) or \
            not isinstance(limits, dict) or set(limits) != _LIMIT_FIELDS or \
            not all(isinstance(item, int) and item > 0 for item in limits.values()):
        raise ParseError("secure-parser policy shape/version is not current")
    return value


_POLICY = _load_policy()
MAX_XML_BYTES = _POLICY["limits"]["bytes"]
MAX_DEPTH = _POLICY["limits"]["depth"]
MAX_NODES = _POLICY["limits"]["nodes"]
MAX_ATTRIBUTES = _POLICY["limits"]["attributesPerElement"]
MAX_TEXT_LENGTH = _POLICY["limits"]["textNodeCharacters"]

_FORBIDDEN_LEXICAL = (
    (re.compile(br"<!DOCTYPE", re.IGNORECASE), "DOCTYPE"),
    (re.compile(br"<!ENTITY", re.IGNORECASE), "entity declaration"),
    (re.compile(br"<!\[CDATA\[", re.IGNORECASE), "CDATA"),
    (re.compile(br"<\?[^xX]"), "processing instruction"),
    (re.compile(br"<!--"), "comment"),
)
_NAMED_ENTITY = re.compile(br"&([A-Za-z_:][A-Za-z0-9_.:-]*);")
_ALLOWED_ENTITIES = {b"amp", b"lt", b"gt", b"apos", b"quot"}


@dataclass(frozen=True)
class ParsedArtifact:
    kind: str
    profile: str
    root: ET.Element
    raw_bytes: bytes
    raw_digest: str
    semantic_digest: str
    fragment_digests: dict[str, str]


@lru_cache(maxsize=3)
def _schema(kind: str) -> xmlschema.XMLSchema11:
    filename = {
        "content-document": "content.xsd",
        "authored-document": "authored.xsd",
        "relation-set": "relations.xsd",
    }.get(kind)
    if filename is None:
        raise ParseError("unsupported XML artifact kind %s" % kind)
    path = os.path.join(SCHEMA_DIRECTORY, filename)
    try:
        return xmlschema.XMLSchema11(
            path, validation="strict", allow="sandbox", defuse="always")
    except (OSError, xmlschema.XMLSchemaException) as exc:
        raise SchemaError("current XSD 1.1 schema is invalid: %s" % exc) from exc


def _preflight(data: bytes) -> None:
    if not isinstance(data, bytes):
        raise TypeError("XML parser input must be bytes")
    if not data or len(data) > MAX_XML_BYTES:
        raise ParseError("XML byte size is outside the closed resource limit")
    if data.startswith((b"\xff\xfe", b"\xfe\xff", b"\x00")):
        raise ParseError("canonical XML must use UTF-8")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ParseError("canonical XML is not UTF-8") from exc
    if unicodedata.normalize("NFC", text) != text:
        raise ParseError("canonical XML text is not NFC")
    for pattern, label in _FORBIDDEN_LEXICAL:
        if pattern.search(data):
            raise ParseError("canonical XML contains forbidden %s" % label)
    for match in _NAMED_ENTITY.finditer(data):
        if match.group(1) not in _ALLOWED_ENTITIES:
            raise ParseError("canonical XML contains a non-predefined entity reference")


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
) -> list[tuple[ET.Element, str]]:
    if not isinstance(expected_namespace, str) or not expected_namespace or \
            any(character in expected_namespace for character in "{}\x00") or \
            not isinstance(expected_root, str) or not expected_root or \
            any(character in expected_root for character in "{}:/\x00"):
        raise ParseError("expected XML namespace/root is malformed")
    if root.tag != "{%s}%s" % (expected_namespace, expected_root):
        raise ParseError("XML root does not match the selected artifact kind")
    stack = [(root, 1)]
    nodes = 0
    identifiers: set[str] = set()
    addressable: list[tuple[ET.Element, str]] = []
    allowed_namespaces = {expected_namespace, *additional_namespaces}
    while stack:
        node, depth = stack.pop()
        nodes += 1
        if nodes > MAX_NODES or depth > MAX_DEPTH:
            raise ParseError("XML tree exceeds a closed resource limit")
        if len(node.attrib) > MAX_ATTRIBUTES:
            raise ParseError("XML element exceeds the attribute limit")
        for value in (node.text, node.tail):
            if value is not None and len(value) > MAX_TEXT_LENGTH:
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
                        expected_root: str) -> ET.Element:
    """Secure-parse one registered XML document against a closed XSD 1.1.

    This is the public extension point for consumer-owned XML namespaces. A
    caller supplies the exact tracked, self-contained schema bytes; imports,
    includes, overrides, and other resolver-dependent schema composition are
    prohibited. The same lexical and resource limits used for package XML
    apply before strict schema validation.
    """
    _preflight(data)
    _preflight(schema)
    root = _parse_tree(data)
    _closed_tree_checks(root, expected_namespace, expected_root)

    xsd_namespace = "http://www.w3.org/2001/XMLSchema"
    schema_root = _parse_tree(schema)
    _closed_tree_checks(schema_root, xsd_namespace, "schema")
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


def _resource_and_semantic_checks(root: ET.Element, kind: str) -> dict[str, str]:
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
    addressable = _closed_tree_checks(
        root, expected_namespace, expected_root,
        additional_namespaces=additional,
    )

    profile = root.get("schemaProfile")
    if not profile or root.get("schemaVersion") != SCHEMA_VERSION:
        raise ParseError("XML schema profile/version is absent or unsupported")
    profiles = load_xml_profiles()
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
    elif kind == "authored-document":
        projection_profile = load_projection_profile()
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
    result = {}
    for node, namespace in addressable:
        fragment_kind = (
            "content-fragment" if kind == "content-document"
            else "authored-fragment" if kind == "authored-document"
            else "relation" if namespace == RELATIONS_NAMESPACE
            else "relation-context-fragment")
        result[node.get(XML_ID)] = semantic_digest(node, fragment_kind, profile)
    return result


def parse_artifact(data: bytes, kind: str) -> ParsedArtifact:
    """Securely parse, XSD-validate, and digest one package."""
    _preflight(data)
    root = _parse_tree(data)
    fragments = _resource_and_semantic_checks(root, kind)
    schema = _schema(kind)
    resource = XMLResource(
        root, base_url=SCHEMA_DIRECTORY, allow="sandbox", defuse="always")
    # ``lax`` here is xmlschema's error-collection mode, not permissive
    # schema handling: every reported validation defect is rejected below.
    errors = list(schema.iter_errors(resource, validation="lax"))
    if errors:
        detail = "; ".join(error.reason for error in errors[:8])
        raise SchemaError("XSD 1.1 validation failed: %s" % detail)
    if kind == "authored-document":
        try:
            from .markdown import _validate_authored_root
            _validate_authored_root(root)
        except StructuredSourceError as exc:
            raise ParseError("authored XML semantic model is invalid: %s" % exc) from exc
    profile = root.get("schemaProfile")
    return ParsedArtifact(
        kind=kind,
        profile=profile,
        root=root,
        raw_bytes=data,
        raw_digest=raw_digest(data),
        semantic_digest=semantic_digest(root, kind, profile),
        fragment_digests=fragments,
    )
