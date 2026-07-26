"""Closed semantic and projection profile controls."""

from __future__ import annotations

from functools import lru_cache
import os
import re

from .control import parse_json
from .errors import StructuredSourceError

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE_DIRECTORY = os.path.join(ROOT, "structured_source", "profiles")
_ID = re.compile(r"[a-z][a-z0-9-]{0,159}\Z")

_PDF_ITEM_METADATA_FIELDS = {
    "action": {"owner": "string", "status": "string"},
    "blockQuotation": {},
    "caution": {"owner": "string", "status": "string"},
    "claim": {"claimId": "string", "number": "positive-integer", "type": "string"},
    "codeBlock": {"language": "string"},
    "division": {"role": "string"},
    "figure": {"alt": "string", "assetId": "string"},
    "heading": {"level": "positive-integer"},
    "item": {},
    "limitation": {"limitationId": "string"},
    "list": {"delimiter": "string", "ordered": "boolean", "start": "positive-integer"},
    "noteBlock": {"owner": "string", "status": "string"},
    "paragraph": {},
    "plain": {},
    "row": {},
    "separator": {},
    "table": {},
}
_PDF_TYPED_CONTENT_NODE_FIELDS = {
    "action": {"owner": "string", "status": "string"},
    "blockQuotation": {},
    "body": {},
    "caption": {},
    "caution": {"owner": "string", "status": "string"},
    "cell": {"alignment": "string"},
    "citation": {"citationId": "string"},
    "claim": {"claimId": "string", "number": "positive-integer",
              "type": "string"},
    "code": {},
    "codeBlock": {"language": "string"},
    "definedTerm": {},
    "dependency": {},
    "division": {"role": "string"},
    "emphasis": {},
    "figure": {"alt": "string", "assetId": "string"},
    "head": {},
    "heading": {"level": "positive-integer"},
    "image": {"alt": "string", "assetId": "string", "title": "string"},
    "item": {},
    "limitation": {"limitationId": "string"},
    "lineBreak": {},
    "link": {"target": "string", "title": "string"},
    "list": {"delimiter": "string", "ordered": "boolean",
             "start": "positive-integer"},
    "math": {},
    "note": {},
    "noteBlock": {"owner": "string", "status": "string"},
    "paragraph": {},
    "plain": {},
    "preamble": {},
    "quotation": {},
    "reviewMark": {"style": "string"},
    "row": {},
    "separator": {},
    "softBreak": {},
    "space": {},
    "strikeout": {},
    "strong": {},
    "subscript": {},
    "superscript": {},
    "table": {},
    "text": {},
}
_PDF_TYPED_CONTENT_TEXT_ELEMENTS = [
    "code", "codeBlock", "dependency", "math", "text",
]
_PDF_TYPED_CONTENT_CHILD_ELEMENTS = [
    "action", "blockQuotation", "body", "caption", "caution", "cell",
    "citation", "claim", "definedTerm", "division", "emphasis", "figure",
    "head", "heading", "item", "limitation", "link", "list", "note",
    "noteBlock", "paragraph", "plain", "preamble", "quotation",
    "reviewMark", "row", "strikeout", "strong", "subscript",
    "superscript", "table",
]
_PDF_DOCUMENT_METADATA_FIELDS = {
    "artifactFamily": "string",
    "documentId": "string",
    "jurisdiction": "string",
    "language": "string",
    "scope": "string",
    "status": "string",
    "title": "string",
}
_PDF_PROVENANCE_FIELDS = {
    "fragmentId": "string",
    "page": "positive-integer",
    "region": "string",
    "sourcePath": "string",
    "uncertainty": "string",
}
_PDF_PROFILE_FIELDS = {
    "dependencyKinds", "documentItem", "documentMetadataFields",
    "itemIdentityAttribute", "itemMetadataFields", "itemOrder",
    "noticeVersion", "originElement", "projectionProfile",
    "provenanceFields", "readableStorage", "sourceNumberPolicy",
    "typedContentChildElements", "typedContentNodeFields",
    "typedContentTextElements", "typedItemDigest",
}
_PDF_DOCUMENT_ITEM = {
    "identityAttribute": "xml:id",
    "itemType": "document",
    "sourceBinding": "manifest-stored-source",
    "substantiveMetadata": [],
    "typedContent": "ordered-content-children",
}
_PDF_DEPENDENCY_KINDS = {
    "asset": {"digest": "required-raw", "itemId": "prohibited",
              "target": "manifest-asset"},
    "document": {"digest": "optional-with-item-id-typed",
                 "itemId": "optional-with-digest", "target": "content-package"},
    "relation-set": {"digest": "prohibited", "itemId": "prohibited",
                     "target": "relation-package"},
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
_PDF_TYPED_ITEM_DIGEST = {
    "canonicalization": "c1",
    "digestDomain": "aa11393:ssp:typed-item:v1",
    "fields": [
        "digestDomain", "authorityScheme", "schemaProfile", "documentId",
        "itemId", "itemType", "typedContent", "substantiveMetadata",
    ],
    "prefix": "sha256/typed-item-v1:",
    "wholeXmlDigest": "prohibited",
}


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
            value.get("profileVersion") != "1":
        raise StructuredSourceError("XML profile registry shape/version is not current")
    content = value.get("contentDocuments")
    if not isinstance(content, dict) or set(content) != {
            "pdf-evidence-transcription-v1"}:
        raise StructuredSourceError(
            "content-document profile registry is not exact")
    for profile_id, profile in content.items():
        if _ID.fullmatch(profile_id) is None or not isinstance(profile, dict) or \
                set(profile) != _PDF_PROFILE_FIELDS or \
                profile.get("originElement") != "pdfDerivative" or \
                profile.get("projectionProfile") != projection["profileId"] or \
                profile.get("noticeVersion") != projection["generatedNoticeVersion"] or \
                profile.get("dependencyKinds") != _PDF_DEPENDENCY_KINDS or \
                profile.get("documentItem") != _PDF_DOCUMENT_ITEM or \
                profile.get("documentMetadataFields") != \
                _PDF_DOCUMENT_METADATA_FIELDS or \
                profile.get("itemIdentityAttribute") != "xml:id" or \
                profile.get("itemMetadataFields") != _PDF_ITEM_METADATA_FIELDS or \
                profile.get("itemOrder") != "xml-document-order" or \
                profile.get("provenanceFields") != _PDF_PROVENANCE_FIELDS or \
                profile.get("readableStorage") != _PDF_READABLE_STORAGE or \
                profile.get("sourceNumberPolicy") != \
                "content-or-typed-metadata-not-identity" or \
                profile.get("typedContentNodeFields") != \
                _PDF_TYPED_CONTENT_NODE_FIELDS or \
                profile.get("typedContentTextElements") != \
                _PDF_TYPED_CONTENT_TEXT_ELEMENTS or \
                profile.get("typedContentChildElements") != \
                _PDF_TYPED_CONTENT_CHILD_ELEMENTS or \
                profile.get("typedItemDigest") != _PDF_TYPED_ITEM_DIGEST:
            raise StructuredSourceError("content-document profile is malformed: %s" % profile_id)
    relations = value.get("relationSets")
    if not isinstance(relations, dict) or not relations:
        raise StructuredSourceError("relation-set profile registry is empty")
    for profile_id, profile in relations.items():
        if _ID.fullmatch(profile_id) is None or not isinstance(profile, dict) or \
                set(profile) != {"relationType", "directions", "endpointRoles",
                                 "requiredEndpointRoles", "assertionFields"} or \
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
        _read("xml-v1.json"), load_projection_profile())
