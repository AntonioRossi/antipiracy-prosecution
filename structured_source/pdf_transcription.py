"""Closed, immutable PDF-transcription item surface and computed coverage.

The stored PDF remains the fidelity authority.  This module validates the
asserted XML surface and builds the only consumer-facing semantic handoff; it
does not inspect, OCR, or infer content from the PDF.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from xml.etree import ElementTree as ET

from . import CONTENT_NAMESPACE
from .canonical import canonical_bytes, raw_digest
from .errors import StructuredSourceError
from .parser import ParsedArtifact
from .render import Projection

C = "{%s}" % CONTENT_NAMESPACE
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
AUTHORITY_SCHEME = "pdf-evidence-transcription-v1"
TRANSCRIPTION_ROLE = "transcription-xml"
_ANCHOR_PREFIX = "ssp-"
_ANCHOR = re.compile(br'<a id="ssp-([A-Za-z][A-Za-z0-9_.:-]*)"></a>')


@dataclass(frozen=True, slots=True)
class DocumentMetadata:
    document_id: str
    title: str
    artifact_family: str
    jurisdiction: str
    scope: str
    status: str
    language: str


@dataclass(frozen=True, slots=True)
class ProvenanceEvidence:
    item_id: str
    source_path: str
    page: int
    region: str | None
    uncertainty: str | None


@dataclass(frozen=True, slots=True)
class DependencyBinding:
    kind: str
    subject_id: str
    digest: str


@dataclass(frozen=True, slots=True)
class AssetBinding:
    asset_id: str
    path: str
    raw_digest: str
    size: int


@dataclass(frozen=True, slots=True)
class ConvenienceBinding:
    path: str
    raw_digest: str
    size: int
    role: str
    non_authoritative: bool


@dataclass(frozen=True, slots=True)
class SourceBinding:
    path: str
    raw_digest: str
    size: int
    role: str
    official_copy_status: str
    extraction_method: str


@dataclass(frozen=True, slots=True)
class TranscriptionItem:
    item_id: str
    item_type: str
    parent_id: str | None
    child_ids: tuple[str, ...]
    ordinal: int
    metadata: tuple[tuple[str, str], ...]
    semantic_content: bytes
    semantic_digest: str
    provenance: ProvenanceEvidence
    asset_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PDFTranscriptionSurface:
    package_id: str
    authority_scheme: str
    representation_role: str
    schema_profile: str
    xml_path: str
    xml_raw_digest: str
    semantic_digest: str
    manifest_path: str
    manifest_raw_digest: str
    markdown_path: str
    markdown_raw_digest: str
    document: DocumentMetadata
    source: SourceBinding
    items: tuple[TranscriptionItem, ...]
    dependencies: tuple[DependencyBinding, ...]
    assets: tuple[AssetBinding, ...]
    convenience_derivatives: tuple[ConvenienceBinding, ...]
    coverage_field_count: int

    def item(self, item_id: str) -> TranscriptionItem:
        """Return one exact stable item or fail without inference."""
        matches = [item for item in self.items if item.item_id == item_id]
        if len(matches) != 1:
            raise StructuredSourceError(
                "PDF transcription item does not resolve exactly")
        return matches[0]

    def children(self, item_id: str | None = None) -> tuple[TranscriptionItem, ...]:
        """Traverse the asserted hierarchy in XML document order."""
        return tuple(item for item in self.items if item.parent_id == item_id)


def _local(node: ET.Element) -> str:
    return node.tag.rsplit("}", 1)[-1]


def _metadata(identity: ET.Element) -> DocumentMetadata:
    title = identity.find(C + "title")
    if title is None or not title.text:
        raise StructuredSourceError("PDF transcription title is absent")
    return DocumentMetadata(
        document_id=identity.get("documentId", ""),
        title=title.text,
        artifact_family=identity.get("artifactFamily", ""),
        jurisdiction=identity.get("jurisdiction", ""),
        scope=identity.get("scope", ""),
        status=identity.get("status", ""),
        language=identity.get("language", ""),
    )


def _coverage_expectations(root: ET.Element, subject_id: str):
    expected = []
    sequence = 0

    def visit(node: ET.Element, nearest_item: str | None, plane: str):
        nonlocal sequence
        sequence += 1
        item_id = node.get(XML_ID) or nearest_item
        local = _local(node)
        node_ref = "%s:n%d:%s" % (subject_id, sequence, local)
        if plane == "content" and item_id:
            classification = "review-visible"
            anchors = [_ANCHOR_PREFIX + item_id]
        elif plane == "content":
            classification = "mechanically-derived"
            anchors = []
        elif plane in {"dependencies", "provenance", "metadata"}:
            classification = "review-scheduled"
            anchors = [_ANCHOR_PREFIX + {
                "dependencies": "review-dependencies",
                "provenance": "review-provenance",
                "metadata": "review-metadata",
            }[plane]]
        elif plane == "projection":
            classification = "mechanically-derived"
            anchors = []
        else:
            classification = "internal-justified"
            anchors = []

        def add(suffix):
            expected.append((node_ref + suffix, node_ref, suffix[1:],
                             classification, anchors))

        add(":element")
        for name in sorted(node.attrib):
            add(":attribute:" + name.rsplit("}", 1)[-1])
        if node.text is not None and node.text.strip():
            add(":text")
        for child in node:
            child_plane = plane
            if node is root:
                child_plane = {
                    "documentIdentity": "metadata",
                    "origin": "metadata",
                    "dependencies": "dependencies",
                    "provenance": "provenance",
                    "content": "content",
                    "projectionPolicy": "projection",
                }.get(_local(child), "internal")
            visit(child, None if node is root else item_id, child_plane)

    visit(root, None, "internal")
    return expected


def _validate_projection_coverage(
        artifact: ParsedArtifact, projection: Projection,
        document_id: str) -> int:
    value = projection.coverage
    if not isinstance(value, dict) or set(value) != {
            "coverageVersion", "fields", "markdownDigest", "projectionProfile",
            "sourceDigest", "sourceProfile", "subjectId"} or \
            value.get("coverageVersion") != "1" or \
            value.get("subjectId") != document_id or \
            value.get("sourceDigest") != artifact.semantic_digest or \
            value.get("sourceProfile") != artifact.profile or \
            value.get("projectionProfile") != "gfm-v1" or \
            value.get("markdownDigest") != projection.markdown_digest or \
            projection.markdown_digest != raw_digest(projection.markdown):
        raise StructuredSourceError(
            "PDF computed field/projection coverage envelope is stale")
    fields = value.get("fields")
    expected = _coverage_expectations(artifact.root, document_id)
    if not isinstance(fields, list) or len(fields) != len(expected):
        raise StructuredSourceError("PDF computed field coverage census is incomplete")
    seen = set()
    for actual, required in zip(fields, expected):
        field_id, node_ref, field_name, classification, anchors = required
        extra = ({"derivationId"} if classification == "mechanically-derived"
                 else {"justification"} if classification == "internal-justified"
                 else set())
        if not isinstance(actual, dict) or set(actual) != {
                "anchors", "classification", "fieldId", "origin", "regions",
                *extra} or actual.get("fieldId") != field_id or \
                actual.get("classification") != classification or \
                actual.get("anchors") != anchors or \
                actual.get("origin") != {
                    "subjectId": document_id, "nodeRef": node_ref,
                    "field": field_name} or field_id in seen:
            raise StructuredSourceError(
                "PDF computed field coverage entry is stale")
        seen.add(field_id)
        regions = actual.get("regions")
        if not isinstance(regions, list) or any(
                not isinstance(region, dict) or set(region) != {
                    "endLine", "startLine"} or
                not isinstance(region["startLine"], int) or
                not isinstance(region["endLine"], int) or
                region["startLine"] < 1 or
                region["endLine"] < region["startLine"]
                for region in regions):
            raise StructuredSourceError(
                "PDF computed field coverage region is malformed")
        if classification == "review-visible" and not regions:
            raise StructuredSourceError(
                "PDF review-visible field has no generated Markdown region")
        if classification == "mechanically-derived" and \
                actual.get("derivationId") != "gfm-v1-structure":
            raise StructuredSourceError(
                "PDF mechanical field derivation is undeclared")
        if classification == "internal-justified" and \
                actual.get("justification") != "schema-envelope-control":
            raise StructuredSourceError(
                "PDF internal field coverage has no current justification")
    return len(fields)


def build_surface(
        artifact: ParsedArtifact, manifest: dict, projection: Projection, *,
        package_id: str, xml_path: str, manifest_path: str,
        manifest_raw_digest: str, markdown_path: str,
        resolved_dependencies: tuple[DependencyBinding, ...],
) -> PDFTranscriptionSurface:
    """Validate and freeze one complete PDF-transcription semantic surface."""
    if artifact.kind != "content-document" or artifact.profile != AUTHORITY_SCHEME:
        raise StructuredSourceError(
            "PDF surface received a different authority/profile")
    root = artifact.root
    identity = root.find(C + "documentIdentity")
    content = root.find(C + "content")
    provenance = root.find(C + "provenance")
    dependencies_node = root.find(C + "dependencies")
    if identity is None or content is None or provenance is None or \
            dependencies_node is None:
        raise StructuredSourceError("PDF transcription item surface is incomplete")
    document = _metadata(identity)
    if document.document_id != package_id or manifest.get("documentId") != package_id:
        raise StructuredSourceError("PDF package/document/manifest identity is stale")

    evidence_entries = provenance.findall(C + "fragmentEvidence")
    evidence_ids = [entry.get("fragmentId") for entry in evidence_entries]
    if len(evidence_ids) != len(set(evidence_ids)):
        raise StructuredSourceError("PDF item provenance identity is duplicated")
    evidence_by_id = {}
    for entry in evidence_entries:
        try:
            page = int(entry.get("page", ""))
        except ValueError as exc:
            raise StructuredSourceError("PDF item provenance page is malformed") from exc
        evidence_by_id[entry.get("fragmentId")] = ProvenanceEvidence(
            item_id=entry.get("fragmentId", ""),
            source_path=entry.get("sourcePath", ""),
            page=page,
            region=entry.get("region"),
            uncertainty=entry.get("uncertainty"),
        )

    item_nodes = [node for node in content.iter() if node.get(XML_ID)]
    item_ids = [node.get(XML_ID) for node in item_nodes]
    if not item_ids or len(item_ids) != len(set(item_ids)) or \
            set(item_ids) != set(evidence_by_id):
        raise StructuredSourceError(
            "PDF item/provenance census is not exact")
    parent_by_id = {}
    children_by_id = {item_id: [] for item_id in item_ids}

    def hierarchy(node: ET.Element, parent_id: str | None):
        current = node.get(XML_ID) or parent_id
        if node.get(XML_ID):
            item_id = node.get(XML_ID)
            parent_by_id[item_id] = parent_id
            if parent_id is not None:
                children_by_id[parent_id].append(item_id)
        for child in node:
            hierarchy(child, current)

    for top_level in content:
        hierarchy(top_level, None)

    stored = manifest.get("storedSource")
    if not isinstance(stored, dict) or not stored.get("path", "").casefold().endswith(
            ".pdf"):
        raise StructuredSourceError("PDF source binding does not name one stored PDF")
    source = SourceBinding(
        path=stored["path"], raw_digest=stored["rawDigest"], size=stored["size"],
        role=stored["role"], official_copy_status=stored["officialCopyStatus"],
        extraction_method=manifest["extractionMethod"],
    )
    if any(item.source_path != source.path for item in evidence_by_id.values()):
        raise StructuredSourceError(
            "PDF item provenance does not bind the manifest PDF")

    assets = tuple(AssetBinding(
        asset_id=entry["assetId"], path=entry["path"],
        raw_digest=entry["rawDigest"], size=entry["size"])
        for entry in manifest["assets"])
    if len(assets) != len({asset.asset_id for asset in assets}):
        raise StructuredSourceError("PDF manifest asset identities are not exact")
    asset_by_id = {asset.asset_id: asset for asset in assets}
    used_assets = {
        node.get("assetId") for node in content.iter()
        if _local(node) in {"image", "figure"}}
    if used_assets != set(asset_by_id):
        raise StructuredSourceError(
            "PDF XML/manifest asset census is not exact")

    declared_dependencies = tuple(DependencyBinding(
        kind=entry.get("kind", ""), subject_id=entry.get("subjectId", ""),
        digest=entry.get("digest", ""))
        for entry in dependencies_node.findall(C + "dependency"))
    if declared_dependencies != resolved_dependencies or \
            len(declared_dependencies) != len({
                (item.kind, item.subject_id) for item in declared_dependencies}):
        raise StructuredSourceError(
            "PDF dependency binding census is not exact")
    asset_dependencies = {
        item.subject_id: item.digest for item in declared_dependencies
        if item.kind == "asset"}
    if asset_dependencies != {
            asset.asset_id: asset.raw_digest for asset in assets}:
        raise StructuredSourceError(
            "PDF asset dependency digests are stale")

    anchors = [match.group(1).decode("ascii")
               for match in _ANCHOR.finditer(projection.markdown)]
    if any(anchors.count(item_id) != 1 for item_id in item_ids):
        raise StructuredSourceError(
            "PDF generated Markdown item anchors are not exact")
    field_count = _validate_projection_coverage(
        artifact, projection, document.document_id)

    items = []
    for ordinal, node in enumerate(item_nodes, start=1):
        item_id = node.get(XML_ID)
        metadata = tuple(sorted(
            (name.rsplit("}", 1)[-1], value)
            for name, value in node.attrib.items() if name != XML_ID))
        direct_assets = tuple(sorted({
            entry.get("assetId") for entry in node.iter()
            if _local(entry) in {"image", "figure"} and
            entry.get("assetId") is not None}))
        digest = artifact.fragment_digests.get(item_id)
        if not isinstance(digest, str):
            raise StructuredSourceError("PDF item semantic digest is absent")
        items.append(TranscriptionItem(
            item_id=item_id, item_type=_local(node),
            parent_id=parent_by_id[item_id],
            child_ids=tuple(children_by_id[item_id]), ordinal=ordinal,
            metadata=metadata, semantic_content=canonical_bytes(node),
            semantic_digest=digest, provenance=evidence_by_id[item_id],
            asset_ids=direct_assets,
        ))

    convenience = tuple(ConvenienceBinding(
        path=entry["path"], raw_digest=entry["rawDigest"], size=entry["size"],
        role=entry["role"], non_authoritative=entry["nonAuthoritative"])
        for entry in manifest["convenienceDerivatives"])
    return PDFTranscriptionSurface(
        package_id=package_id, authority_scheme=AUTHORITY_SCHEME,
        representation_role=TRANSCRIPTION_ROLE, schema_profile=artifact.profile,
        xml_path=xml_path, xml_raw_digest=artifact.raw_digest,
        semantic_digest=artifact.semantic_digest, manifest_path=manifest_path,
        manifest_raw_digest=manifest_raw_digest, markdown_path=markdown_path,
        markdown_raw_digest=projection.markdown_digest, document=document,
        source=source, items=tuple(items), dependencies=declared_dependencies,
        assets=assets, convenience_derivatives=convenience,
        coverage_field_count=field_count,
    )
