"""Closed semantic and projection profile controls."""

from __future__ import annotations

from functools import lru_cache
import os
import re

from .control import parse_json
from .errors import StructuredSourceError
from .grammar import parse_content_grammar

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE_DIRECTORY = os.path.join(ROOT, "structured_source", "profiles")
_ID = re.compile(r"[a-z][a-z0-9-]{0,159}\Z")
_XML_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_.-]*\Z")

_PDF_PROFILE_FIELDS = {
    "contentGrammar", "dependencyKinds", "documentItem", "documentMetadataFields",
    "itemIdentityAttribute", "itemMetadataFields", "itemOrder",
    "noticeVersion", "originElement", "projectionProfile",
    "provenanceFields", "readableStorage", "sourceNumberPolicy",
    "typedContentChildElements", "typedContentNodeFields",
    "typedContentTextElements", "typedItemDigest",
}
_PDF_READABLE_STORAGE = {
    "attributeOrder": "expanded-name",
    "byteOrderMark": "prohibited",
    "containerLayout": "one-child-per-structural-line",
    "declaration": '<?xml version="1.0" encoding="UTF-8"?>',
    "emptyElement": "space-before-solidus",
    "encoding": "UTF-8",
    "finalNewline": True,
    "indent": "two-spaces",
    "lineEndings": "LF",
    "namespaceDeclarations": "root-default-then-lexicographic-prefix",
    "structuralBlankLines": False,
    "tabs": "prohibited",
    "textLeafControls": "numeric-character-references",
    "textLeafLayout": "one-unwrapped-line",
    "unicodeNormalization": "NFC",
}
_SCALAR_TYPES = frozenset({"boolean", "positive-integer", "string"})
_CONTENT_AUTHORITY_SCHEMES = frozenset({
    "authored-markdown-v1", "pdf-evidence-transcription-v1",
})


def _field_map(value, label, *, nonempty=True):
    if not isinstance(value, dict) or (nonempty and not value) or any(
            _XML_NAME.fullmatch(name) is None or not isinstance(fields, dict) or any(
                _XML_NAME.fullmatch(field) is None or scalar not in _SCALAR_TYPES
                for field, scalar in fields.items())
            for name, fields in value.items()):
        raise StructuredSourceError("%s is malformed" % label)
    return value


def _scalar_map(value, label):
    if not isinstance(value, dict) or not value or any(
            _XML_NAME.fullmatch(name) is None or scalar not in _SCALAR_TYPES
            for name, scalar in value.items()):
        raise StructuredSourceError("%s is malformed" % label)
    return value


def _validate_pdf_profile(profile, profile_id, projection):
    if _ID.fullmatch(profile_id) is None or not isinstance(profile, dict) or \
            set(profile) != _PDF_PROFILE_FIELDS or \
            profile.get("projectionProfile") != projection["profileId"] or \
            profile.get("noticeVersion") != projection["generatedNoticeVersion"] or \
            profile.get("itemIdentityAttribute") != "xml:id" or \
            profile.get("itemOrder") != "xml-document-order" or \
            profile.get("sourceNumberPolicy") != \
            "content-or-typed-metadata-not-identity" or \
            profile.get("readableStorage") != _PDF_READABLE_STORAGE:
        raise StructuredSourceError(
            "content-document profile is malformed: %s" % profile_id)
    parse_content_grammar(profile.get("contentGrammar"))
    item_fields = _field_map(
        profile.get("itemMetadataFields"), "PDF item metadata")
    node_fields = _field_map(
        profile.get("typedContentNodeFields"), "PDF typed-content metadata")
    _scalar_map(profile.get("documentMetadataFields"), "PDF document metadata")
    _scalar_map(profile.get("provenanceFields"), "PDF provenance metadata")
    if not set(item_fields).issubset(node_fields) or any(
            item_fields[name] != node_fields[name] for name in item_fields):
        raise StructuredSourceError(
            "PDF addressable-item metadata is outside typed content")
    text = _string_set(
        profile.get("typedContentTextElements"), "PDF text elements")
    children = _string_set(
        profile.get("typedContentChildElements"), "PDF child elements")
    if set(text) & set(children) or not (set(text) | set(children)).issubset(
            node_fields):
        raise StructuredSourceError("PDF typed-content value models overlap")
    if profile.get("documentItem") != {
            "identityAttribute": "xml:id", "itemType": "document",
            "sourceBinding": "manifest-stored-source",
            "substantiveMetadata": [],
            "typedContent": "ordered-content-children"}:
        raise StructuredSourceError("PDF document item is unsupported")
    if profile.get("dependencyKinds") != {
            "asset": {"digest": "required-raw", "itemId": "prohibited",
                      "target": "manifest-asset"},
            "document": {"digest": "optional-with-item-id-typed",
                         "itemId": "optional-with-digest",
                         "target": "content-package"},
            "relation-set": {"digest": "prohibited", "itemId": "prohibited",
                             "target": "relation-package"}}:
        raise StructuredSourceError("PDF dependency kinds are unsupported")
    if not isinstance(profile.get("originElement"), str) or \
            _XML_NAME.fullmatch(profile["originElement"]) is None:
        raise StructuredSourceError("PDF origin element is malformed")
    if profile.get("typedItemDigest") != {
            "canonicalization": "c1",
            "digestDomain": "aa11393:ssp:typed-item:v1",
            "fields": [
                "digestDomain", "authorityScheme", "schemaProfile",
                "documentId", "itemId", "itemType", "typedContent",
                "substantiveMetadata"],
            "prefix": "sha256/typed-item-v1:",
            "wholeXmlDigest": "prohibited"}:
        raise StructuredSourceError("PDF typed-item digest law is unsupported")


def _read(name):
    path = os.path.join(PROFILE_DIRECTORY, name)
    try:
        with open(path, "rb") as handle:
            return parse_json(handle.read())
    except (OSError, StructuredSourceError) as exc:
        raise StructuredSourceError("structured-source profile is unreadable: %s" % name) from exc


def _string_set(value, label):
    if not isinstance(value, list) or not value or value != sorted(set(value)) or \
            not all(isinstance(item, str) and item for item in value):
        raise StructuredSourceError("%s is not an exact sorted string set" % label)
    return value


def _validate_projection_profile(value):
    fields = {"profileVersion", "profileId", "lineEndings", "finalNewline",
              "stableAnchorPrefix", "tableStyle", "unorderedListMarker",
              "generatedNoticeVersion", "externalSchemes", "anchorSyntax",
              "xmlFragmentIdPolicy",
              "pandocVersion", "pandocApiVersion", "pandocReader",
              "pandocWriter", "supportedBlockConstructors",
              "topLevelBlockConstructors", "supportedInlineConstructors",
              "supportedAuxiliaryConstructors",
              "presentationalNormalizations"}
    if not isinstance(value, dict) or set(value) != fields or \
            value.get("profileVersion") != "1" or value.get("profileId") != "gfm-v1" or \
            value.get("lineEndings") != "LF" or value.get("finalNewline") is not True or \
            value.get("tableStyle") != "pipe" or value.get("unorderedListMarker") not in {"-", "+", "*"} or \
            value.get("stableAnchorPrefix") != "ssp-" or \
            not isinstance(value.get("generatedNoticeVersion"), str) or \
            _ID.fullmatch(value["generatedNoticeVersion"]) is None or \
            value.get("anchorSyntax") != "html-a-id-v1" or \
            value.get("xmlFragmentIdPolicy") != "strip-stable-anchor-prefix" or \
            value.get("pandocVersion") != "3.5" or \
            value.get("pandocApiVersion") != [1, 23, 1] or \
            value.get("pandocReader") != "gfm" or \
            value.get("pandocWriter") != "gfm":
        raise StructuredSourceError("GFM projection profile shape/version is not current")
    for field in ("externalSchemes", "supportedBlockConstructors",
                  "topLevelBlockConstructors", "supportedInlineConstructors",
                  "supportedAuxiliaryConstructors",
                  "presentationalNormalizations"):
        _string_set(value.get(field), "GFM %s" % field)
    if not set(value["topLevelBlockConstructors"]).issubset(
            value["supportedBlockConstructors"]) or \
            set(value["supportedBlockConstructors"]) & \
            set(value["supportedInlineConstructors"]) or \
            set(value["supportedBlockConstructors"]) & \
            set(value["supportedAuxiliaryConstructors"]) or \
            set(value["supportedInlineConstructors"]) & \
            set(value["supportedAuxiliaryConstructors"]) or \
            value["presentationalNormalizations"] != [
                "anchor-carrier-placement", "equivalent-markdown-escaping",
                "final-newline"]:
        raise StructuredSourceError("GFM constructor or normalization registry is not exact")
    return value


def parse_projection_profile(data: bytes):
    """Validate projection-profile bytes supplied by a retained snapshot."""
    try:
        value = parse_json(data)
    except StructuredSourceError as exc:
        raise StructuredSourceError(
            "structured-source projection profile is unreadable") from exc
    return _validate_projection_profile(value)


@lru_cache(maxsize=1)
def load_projection_profile():
    return _validate_projection_profile(_read("gfm-v1.json"))


def _validate_xml_profiles(value, projection):
    if not isinstance(value, dict) or set(value) != {
            "profileVersion", "contentDocuments", "relationSets"} or \
            value.get("profileVersion") != "3":
        raise StructuredSourceError("XML profile registry shape/version is not current")
    content = value.get("contentDocuments")
    if not isinstance(content, dict) or set(content) != {
            "pdf-evidence-transcription-v1"}:
        raise StructuredSourceError(
            "content-document profile registry is not exact")
    for profile_id, profile in content.items():
        _validate_pdf_profile(profile, profile_id, projection)
    relations = value.get("relationSets")
    if not isinstance(relations, dict) or not relations:
        raise StructuredSourceError("relation-set profile registry is empty")
    for profile_id, profile in relations.items():
        if _ID.fullmatch(profile_id) is None or not isinstance(profile, dict) or \
                set(profile) != {"relationType", "directions", "endpointRoles",
                                 "requiredEndpointRoles", "assertionFields",
                                 "endpointRoleTargets"} or \
                _ID.fullmatch(profile.get("relationType", "")) is None:
            raise StructuredSourceError("relation-set profile is malformed: %s" % profile_id)
        for field in ("directions", "endpointRoles", "requiredEndpointRoles",
                      "assertionFields"):
            _string_set(profile.get(field), "%s %s" % (profile_id, field))
            if any(_ID.fullmatch(item) is None for item in profile[field]):
                raise StructuredSourceError(
                    "relation-set profile vocabulary is malformed: %s" %
                    profile_id)
        if not set(profile["requiredEndpointRoles"]).issubset(profile["endpointRoles"]):
            raise StructuredSourceError("relation required roles are outside its profile")
        targets = profile.get("endpointRoleTargets")
        if not isinstance(targets, dict) or \
                set(targets) != set(profile["endpointRoles"]):
            raise StructuredSourceError(
                "relation endpoint-role targets are outside its profile")
        for role, schemes in targets.items():
            _string_set(schemes, "%s %s targets" % (profile_id, role))
            if not set(schemes).issubset(_CONTENT_AUTHORITY_SCHEMES):
                raise StructuredSourceError(
                    "relation endpoint-role target scheme is not current")
    return value


def parse_xml_profiles(data: bytes, projection):
    """Validate XML-profile bytes against the supplied projection profile."""
    try:
        value = parse_json(data)
    except StructuredSourceError as exc:
        raise StructuredSourceError(
            "structured-source XML profile is unreadable") from exc
    return _validate_xml_profiles(value, projection)


@lru_cache(maxsize=1)
def load_xml_profiles():
    return _validate_xml_profiles(
        _read("xml-v3.json"), load_projection_profile())
