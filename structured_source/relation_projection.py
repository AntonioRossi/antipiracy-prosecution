"""Independent validation of generated authored-relation review Markdown."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import posixpath
import re
from urllib.parse import quote

from . import RELATIONS_NAMESPACE
from .canonical import raw_digest
from .errors import StructuredSourceError
from .parser import ParsedArtifact


R = "{%s}" % RELATIONS_NAMESPACE
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
_STABLE_ID = re.compile(r"[A-Za-z][A-Za-z0-9_.:-]*\Z")


@dataclass(frozen=True, slots=True)
class RelationEndpointCoverage:
    """One exact endpoint row in the generated review projection."""

    role: str
    document_id: str
    fragment_id: str
    fragment_content_digest: str
    excerpt: str
    link: str
    line: int


@dataclass(frozen=True, slots=True)
class RelationFieldCoverage:
    """One exact ordered assertion-field row in the review projection."""

    name: str
    value: str
    line: int


@dataclass(frozen=True, slots=True)
class RelationAssertionCoverage:
    """One assertion and its complete generated anchor region."""

    relation_id: str
    xml_id: str
    relation_type: str
    direction: str
    semantic_owner: str
    anchor: str
    start_line: int
    end_line: int
    endpoints: tuple[RelationEndpointCoverage, ...]
    fields: tuple[RelationFieldCoverage, ...]


@dataclass(frozen=True, slots=True)
class RelationCoverage:
    """Fresh immutable ordered census derived from XML, views, and Markdown."""

    relation_set_id: str
    source_profile: str
    projection_profile: str
    source_raw_digest: str
    markdown_raw_digest: str
    metadata_anchor: str
    schedule_anchor: str
    anchor_inventory: tuple[str, ...]
    assertions: tuple[RelationAssertionCoverage, ...]

    @property
    def assertion_count(self) -> int:
        return len(self.assertions)

    @property
    def assertion_field_count(self) -> int:
        return sum(len(assertion.fields) for assertion in self.assertions)

    @property
    def endpoint_count(self) -> int:
        return sum(len(assertion.endpoints) for assertion in self.assertions)


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


def _anchor_line(anchor: str) -> str:
    return '<a id="%s"></a>' % anchor


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


def _view_values(view: object) -> tuple[str, str]:
    if not isinstance(view, Mapping) or set(view) != {
            "excerpt", "markdownPath"} or not isinstance(
                view.get("excerpt"), str) or not isinstance(
                    view.get("markdownPath"), str):
        raise StructuredSourceError(
            "relation projection endpoint view does not resolve exactly")
    return view["excerpt"], view["markdownPath"]


def _expected_projection(
        artifact: ParsedArtifact, output_path: str,
        endpoint_views: Mapping, projection_profile: Mapping,
        ) -> tuple[bytes, RelationCoverage]:
    """Reconstruct exact bytes and census without renderer-owned evidence."""
    prefix = projection_profile.get("stableAnchorPrefix")
    profile_id = projection_profile.get("profileId")
    notice_version = projection_profile.get("generatedNoticeVersion")
    if not all(isinstance(value, str) and value for value in (
            prefix, profile_id, notice_version)):
        raise StructuredSourceError(
            "relation projection profile is malformed")

    root = artifact._validated_root()
    identity = root.find(R + "identity")
    if identity is None:
        raise StructuredSourceError("relation projection identity is absent")
    subject = identity.get("relationSetId")
    if not isinstance(subject, str) or not subject:
        raise StructuredSourceError(
            "relation projection relation-set identity is absent")

    metadata_anchor = _anchor(prefix, "relation-metadata")
    schedule_anchor = _anchor(prefix, "relation-schedule")
    lines = [
        "<!-- GENERATED RELATION REVIEW PROJECTION — relation set %s; "
        "byte digest %s; source profile %s; projection profile %s/%s; "
        "regenerate with `uv --no-cache --offline run --locked --no-sync "
        "python -m structured_source regenerate %s`; edit the relation XML, "
        "never this Markdown. -->" % (
            subject, artifact.raw_digest, artifact.profile, profile_id,
            notice_version, subject),
        "",
        _anchor_line(metadata_anchor),
        "# Relation-set review metadata",
        "",
        "| Field | Current value |",
        "|---|---|",
        "| Relation-set ID | %s |" % subject,
        "| Profile | %s |" % identity.get("profile"),
        "| Semantic owner | %s |" % _escape_text(identity.get("owner", "")),
        "| Scope | %s |" % identity.get("scope"),
        "| Status | %s |" % identity.get("status"),
        "",
        _anchor_line(schedule_anchor),
        "# Exact relations",
        "",
    ]
    anchor_inventory = [metadata_anchor, schedule_anchor]
    assertion_census = []

    for relation in root.findall(R + "relation"):
        xml_id = relation.get(XML_ID, "")
        relation_id = relation.get("relationId", "")
        relation_anchor = _anchor(prefix, xml_id)
        anchor_inventory.append(relation_anchor)
        start_line = len(lines) + 1
        lines.extend((
            _anchor_line(relation_anchor),
            "## %s" % _escape_text(relation_id),
            "",
            "| Field | Current value |",
            "|---|---|",
            "| Type | %s |" % relation.get("type"),
            "| Direction | %s |" % relation.get("direction"),
            "| Semantic owner | %s |" % _escape_text(
                relation.get("semanticOwner", "")),
            "",
            "### Exact endpoints",
            "",
            "| Role | Document | Fragment | Fragment digest | Current excerpt |",
            "|---|---|---|---|---|",
        ))
        endpoint_census = []
        for endpoint in relation.findall(R + "endpoint"):
            document_id = endpoint.get("documentId", "")
            fragment_id = endpoint.get("fragmentId", "")
            fragment_digest = endpoint.get("fragmentContentDigest", "")
            key = (document_id, fragment_id, fragment_digest)
            excerpt, markdown_path = _view_values(endpoint_views.get(key))
            link = (_relative_target(markdown_path, output_path) + "#" +
                    _anchor(prefix, fragment_id))
            rendered_excerpt = excerpt.replace("\n", " ")
            row = "| %s | %s | [%s](%s) | `%s` | %s |" % (
                endpoint.get("role"), document_id, fragment_id, link,
                fragment_digest, _escape_text(rendered_excerpt))
            lines.append(row)
            endpoint_census.append(RelationEndpointCoverage(
                role=endpoint.get("role", ""),
                document_id=document_id,
                fragment_id=fragment_id,
                fragment_content_digest=fragment_digest,
                excerpt=rendered_excerpt,
                link=link,
                line=len(lines),
            ))

        lines.extend((
            "",
            "### Assertion fields",
            "",
            "| Field | Current value |",
            "|---|---|",
        ))
        field_census = []
        for field in relation.findall(R + "assertionField"):
            value = field.text or ""
            lines.append("| %s | %s |" % (
                field.get("name"), _escape_text(value)))
            field_census.append(RelationFieldCoverage(
                name=field.get("name", ""), value=value, line=len(lines)))
        end_line = len(lines)
        lines.append("")
        assertion_census.append(RelationAssertionCoverage(
            relation_id=relation_id,
            xml_id=xml_id,
            relation_type=relation.get("type", ""),
            direction=relation.get("direction", ""),
            semantic_owner=relation.get("semanticOwner", ""),
            anchor=relation_anchor,
            start_line=start_line,
            end_line=end_line,
            endpoints=tuple(endpoint_census),
            fields=tuple(field_census),
        ))

    markdown = ("\n".join(lines).rstrip() + "\n").encode("utf-8")
    coverage = RelationCoverage(
        relation_set_id=subject,
        source_profile=artifact.profile,
        projection_profile=profile_id,
        source_raw_digest=artifact.raw_digest,
        markdown_raw_digest=raw_digest(markdown),
        metadata_anchor=metadata_anchor,
        schedule_anchor=schedule_anchor,
        anchor_inventory=tuple(anchor_inventory),
        assertions=tuple(assertion_census),
    )
    return markdown, coverage


def validate_relation_projection(
        artifact: ParsedArtifact, markdown: bytes, output_path: str,
        endpoint_views: Mapping, *, projection_profile: Mapping,
        ) -> RelationCoverage:
    """Prove exact bytes and return an ordered immutable coverage census."""
    if not isinstance(artifact, ParsedArtifact) or artifact.kind != "relation-set" or \
            not isinstance(markdown, bytes) or not isinstance(output_path, str) or \
            not output_path or not isinstance(endpoint_views, Mapping) or \
            not isinstance(projection_profile, Mapping):
        raise StructuredSourceError(
            "relation projection coverage input is malformed")
    try:
        text = markdown.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise StructuredSourceError(
            "relation projection is not UTF-8") from exc
    if "\r" in text or not text.endswith("\n"):
        raise StructuredSourceError(
            "relation projection line storage is not exact")

    expected, coverage = _expected_projection(
        artifact, output_path, endpoint_views, projection_profile)
    if markdown != expected:
        raise StructuredSourceError(
            "relation projection bytes and ordered coverage are not exact")
    return coverage
