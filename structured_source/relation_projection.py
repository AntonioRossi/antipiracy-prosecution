"""Independent validation of generated authored-relation review Markdown."""

from __future__ import annotations

from collections.abc import Mapping
import posixpath
import re
from types import MappingProxyType
from urllib.parse import quote

from . import RELATIONS_NAMESPACE
from .errors import StructuredSourceError
from .parser import ParsedArtifact


R = "{%s}" % RELATIONS_NAMESPACE
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
_STABLE_ID = re.compile(r"[A-Za-z][A-Za-z0-9_.:-]*\Z")
_TABLE_CONTROLS = frozenset({
    "| Field | Current value |",
    "| Role | Document | Fragment | Fragment digest | Current excerpt |",
    "|---|---|",
    "|---|---|---|---|---|",
})


def _escape_text(value: str) -> str:
    if not isinstance(value, str):
        raise StructuredSourceError(
            "relation projection text value is not a string")
    output = []
    for character in value:
        if character in "\\`*_{}[]<>#|~":
            output.append("\\")
        output.append(character)
    return "".join(output)


def _anchor(prefix: str, identifier: str) -> str:
    if _STABLE_ID.fullmatch(identifier or "") is None:
        raise StructuredSourceError(
            "relation projection identity cannot form an exact anchor")
    return prefix + identifier


def _relative_target(target: str, output_path: str) -> str:
    if not isinstance(target, str) or not target or target.startswith("/") or \
            "\\" in target or any(
                part in {"", ".", ".."} for part in target.split("/")):
        raise StructuredSourceError(
            "relation projection endpoint path is not canonical")
    normalized = posixpath.normpath(target)
    relative = posixpath.relpath(
        normalized, posixpath.dirname(output_path) or ".")
    return quote(relative, safe="/-._~%")


def _table_rows(lines: list[str]) -> tuple[str, ...]:
    return tuple(
        line for line in lines
        if line.startswith("|") and line.endswith("|") and
        line not in _TABLE_CONTROLS)


def _headings(lines: list[str]) -> tuple[str, ...]:
    return tuple(line for line in lines if line.startswith("#"))


def validate_relation_projection(
        artifact: ParsedArtifact, markdown: bytes, output_path: str,
        endpoint_views: Mapping, *, projection_profile: Mapping) -> MappingProxyType:
    """Prove exact relation-review placement and semantic row coverage."""
    if not isinstance(artifact, ParsedArtifact) or artifact.kind != "relation-set" or \
            not isinstance(markdown, bytes) or not isinstance(output_path, str) or \
            not output_path or not isinstance(endpoint_views, Mapping) or \
            not isinstance(projection_profile, Mapping):
        raise StructuredSourceError(
            "relation projection coverage input is malformed")
    prefix = projection_profile.get("stableAnchorPrefix")
    if not isinstance(prefix, str) or not prefix:
        raise StructuredSourceError(
            "relation projection anchor profile is malformed")
    try:
        text = markdown.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise StructuredSourceError(
            "relation projection is not UTF-8") from exc
    if "\r" in text or not text.endswith("\n"):
        raise StructuredSourceError(
            "relation projection line storage is not exact")
    lines = text.splitlines()

    root = artifact._validated_root()
    relation_nodes = root.findall(R + "relation")
    relation_anchor_ids = [node.get(XML_ID, "") for node in relation_nodes]
    expected_anchor_ids = [
        "relation-metadata", "relation-schedule", *relation_anchor_ids]
    carrier = re.compile(
        r'<a id="%s([A-Za-z][A-Za-z0-9_.:-]*)"></a>' %
        re.escape(prefix))
    occurrences = carrier.findall(text)
    anchor_lines = [
        (index, match.group(1))
        for index, line in enumerate(lines)
        if (match := carrier.fullmatch(line)) is not None]
    actual_anchor_ids = [identifier for unused_index, identifier in anchor_lines]
    if occurrences != actual_anchor_ids or actual_anchor_ids != expected_anchor_ids:
        raise StructuredSourceError(
            "relation projection anchor inventory/order/placement is not exact")

    positions = {identifier: index for index, identifier in anchor_lines}
    identity = root.find(R + "identity")
    if identity is None:
        raise StructuredSourceError("relation projection identity is absent")
    metadata_region = lines[
        positions["relation-metadata"]:positions["relation-schedule"]]
    expected_metadata_rows = (
        "| Relation-set ID | %s |" % identity.get("relationSetId"),
        "| Profile | %s |" % identity.get("profile"),
        "| Semantic owner | %s |" % _escape_text(identity.get("owner", "")),
        "| Scope | %s |" % identity.get("scope"),
        "| Status | %s |" % identity.get("status"),
    )
    if _headings(metadata_region) != ("# Relation-set review metadata",) or \
            _table_rows(metadata_region) != expected_metadata_rows:
        raise StructuredSourceError(
            "relation projection metadata coverage is not exact")

    schedule_end = (positions[relation_anchor_ids[0]]
                    if relation_anchor_ids else len(lines))
    schedule_region = lines[positions["relation-schedule"]:schedule_end]
    if _headings(schedule_region) != ("# Exact relations",) or \
            _table_rows(schedule_region):
        raise StructuredSourceError(
            "relation projection schedule coverage is not exact")

    field_count = 0
    endpoint_count = 0
    for relation_index, relation in enumerate(relation_nodes):
        xml_id = relation_anchor_ids[relation_index]
        end = (positions[relation_anchor_ids[relation_index + 1]]
               if relation_index + 1 < len(relation_anchor_ids) else len(lines))
        region = lines[positions[xml_id]:end]
        relation_id = relation.get("relationId", "")
        expected_headings = (
            "## %s" % _escape_text(relation_id),
            "### Exact endpoints",
            "### Assertion fields",
        )
        expected_rows = [
            "| Type | %s |" % relation.get("type"),
            "| Direction | %s |" % relation.get("direction"),
            "| Semantic owner | %s |" % _escape_text(
                relation.get("semanticOwner", "")),
        ]
        for endpoint in relation.findall(R + "endpoint"):
            endpoint_count += 1
            key = (
                endpoint.get("documentId"), endpoint.get("fragmentId"),
                endpoint.get("fragmentContentDigest"))
            view = endpoint_views.get(key)
            if not isinstance(view, Mapping) or set(view) != {
                    "excerpt", "markdownPath"} or not isinstance(
                        view["excerpt"], str):
                raise StructuredSourceError(
                    "relation projection endpoint view does not resolve exactly")
            target = (_relative_target(view["markdownPath"], output_path) +
                      "#" + _anchor(prefix, endpoint.get("fragmentId", "")))
            excerpt = view["excerpt"].replace("\n", " ")
            expected_rows.append("| %s | %s | [%s](%s) | `%s` | %s |" % (
                endpoint.get("role"), endpoint.get("documentId"),
                endpoint.get("fragmentId"), target,
                endpoint.get("fragmentContentDigest"), _escape_text(excerpt)))
        for field in relation.findall(R + "assertionField"):
            field_count += 1
            expected_rows.append("| %s | %s |" % (
                field.get("name"), _escape_text(field.text or "")))
        if _headings(region) != expected_headings or \
                _table_rows(region) != tuple(expected_rows):
            raise StructuredSourceError(
                "relation projection assertion/field/endpoint coverage is not exact")

    return MappingProxyType({
        "assertions": len(relation_nodes),
        "assertionFields": field_count,
        "endpoints": endpoint_count,
    })
