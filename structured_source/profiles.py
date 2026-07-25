"""Closed semantic and projection profile controls."""

from __future__ import annotations

from functools import lru_cache
import json
import os
import re

from .errors import StructuredSourceError

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE_DIRECTORY = os.path.join(ROOT, "structured_source", "profiles")
_ID = re.compile(r"[a-z][a-z0-9-]{0,159}\Z")


def _read(name):
    path = os.path.join(PROFILE_DIRECTORY, name)
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise StructuredSourceError("structured-source profile is unreadable: %s" % name) from exc


def _string_set(value, label):
    if not isinstance(value, list) or not value or value != sorted(set(value)) or \
            not all(isinstance(item, str) and item for item in value):
        raise StructuredSourceError("%s is not an exact sorted string set" % label)
    return value


@lru_cache(maxsize=1)
def load_projection_profile():
    value = _read("gfm-v1.json")
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


@lru_cache(maxsize=1)
def load_xml_profiles():
    value = _read("xml-v1.json")
    if not isinstance(value, dict) or set(value) != {
            "profileVersion", "contentDocuments", "relationSets"} or \
            value.get("profileVersion") != "1":
        raise StructuredSourceError("XML profile registry shape/version is not current")
    projection = load_projection_profile()
    content = value.get("contentDocuments")
    if not isinstance(content, dict) or not content:
        raise StructuredSourceError("content-document profile registry is empty")
    for profile_id, profile in content.items():
        if _ID.fullmatch(profile_id) is None or not isinstance(profile, dict) or \
                set(profile) != {"originElement", "projectionProfile", "noticeVersion"} or \
                profile.get("originElement") not in {"authoredSource", "pdfDerivative"} or \
                profile.get("projectionProfile") != projection["profileId"] or \
                profile.get("noticeVersion") != projection["generatedNoticeVersion"]:
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
        if not set(profile["requiredEndpointRoles"]).issubset(profile["endpointRoles"]):
            raise StructuredSourceError("relation required roles are outside its profile")
    return value
