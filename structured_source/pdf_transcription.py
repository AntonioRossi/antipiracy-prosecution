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
from .canonical import raw_digest, readable_xml_bytes, typed_item_digest
from .control import canonical_json
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
    item_id: str | None
    digest: str | None


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


TypedScalar = str | int | bool


@dataclass(frozen=True, slots=True)
class TypedContentNode:
    element: str
    item_id: str | None
    text: str | None
    attributes: tuple[tuple[str, TypedScalar], ...]
    children: tuple["TypedContentNode", ...]


@dataclass(frozen=True, slots=True)
class TypedItemContent:
    text: str | None
    children: tuple[TypedContentNode, ...]


@dataclass(frozen=True, slots=True)
class TypedDocumentItem:
    item_id: str
    item_type: str
    child_ids: tuple[str, ...]
    typed_content: tuple[TypedContentNode, ...]
    content_digest: str
    source: SourceBinding


@dataclass(frozen=True, slots=True)
class TranscriptionItem:
    item_id: str
    item_type: str
    parent_id: str | None
    child_ids: tuple[str, ...]
    ordinal: int
    metadata: tuple[tuple[str, TypedScalar], ...]
    typed_content: TypedItemContent
    content_digest: str
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
    manifest_path: str
    manifest_raw_digest: str
    markdown_path: str
    markdown_raw_digest: str
    document: DocumentMetadata
    document_item: TypedDocumentItem
    source: SourceBinding
    items: tuple[TranscriptionItem, ...]
    dependencies: tuple[DependencyBinding, ...]
    assets: tuple[AssetBinding, ...]
    convenience_derivatives: tuple[ConvenienceBinding, ...]
    coverage_field_count: int

    def item(self, item_id: str) -> TranscriptionItem | TypedDocumentItem:
        """Return one exact stable item or fail without inference."""
        if self.document_item.item_id == item_id:
            return self.document_item
        matches = [item for item in self.items if item.item_id == item_id]
        if len(matches) != 1:
            raise StructuredSourceError(
                "PDF transcription item does not resolve exactly")
        return matches[0]

    def children(self, item_id: str | None = None) -> tuple[TranscriptionItem, ...]:
        """Traverse the asserted hierarchy in XML document order."""
        if item_id == self.document_item.item_id:
            child_ids = set(self.document_item.child_ids)
            return tuple(item for item in self.items if item.item_id in child_ids)
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


def _freeze_typed_node(value: dict) -> TypedContentNode:
    if not isinstance(value, dict) or set(value) not in (
            {"attributes", "children", "element", "text"},
            {"attributes", "children", "element", "itemId", "text"}):
        raise StructuredSourceError("PDF typed content node is malformed")
    attributes = value["attributes"]
    children = value["children"]
    if not isinstance(attributes, dict) or not isinstance(children, list):
        raise StructuredSourceError("PDF typed content node is malformed")
    return TypedContentNode(
        element=value["element"], item_id=value.get("itemId"),
        text=value["text"], attributes=tuple(sorted(attributes.items())),
        children=tuple(_freeze_typed_node(child) for child in children))


def _freeze_typed_content(value: dict) -> TypedItemContent:
    if not isinstance(value, dict) or set(value) != {"children", "text"} or \
            not isinstance(value["children"], list):
        raise StructuredSourceError("PDF typed item content is malformed")
    return TypedItemContent(
        text=value["text"], children=tuple(
            _freeze_typed_node(child) for child in value["children"]))


def _independent_markdown_regions(
        root: ET.Element, markdown: bytes) -> dict[str, tuple[int, int]]:
    try:
        lines = markdown.decode("utf-8").splitlines()
    except UnicodeDecodeError as exc:
        raise StructuredSourceError("PDF Markdown is not UTF-8") from exc
    anchor_lines: dict[str, list[int]] = {}
    for line_number, line in enumerate(lines, start=1):
        for match in re.finditer(
                r'<a id="ssp-([A-Za-z][A-Za-z0-9_.:-]*)"></a>', line):
            anchor_lines.setdefault(match.group(1), []).append(line_number)

    content = root.find(C + "content")
    if content is None:
        raise StructuredSourceError("PDF coverage content is absent")
    item_nodes = [node for node in content.iter() if node.get(XML_ID)]
    item_ids = [node.get(XML_ID) for node in item_nodes]
    root_id = root.get(XML_ID)
    review_ids = ["review-metadata", "review-dependencies", "review-provenance"]
    expected_anchor_ids = {root_id, *item_ids, *review_ids}
    if set(anchor_lines) != expected_anchor_ids:
        raise StructuredSourceError(
            "PDF independently computed Markdown anchor inventory is not exact")
    for identifier in [root_id, *item_ids, *review_ids]:
        if len(anchor_lines.get(identifier, [])) != 1:
            raise StructuredSourceError(
                "PDF independently computed Markdown anchor census is not exact")

    metadata_start = anchor_lines["review-metadata"][0]
    top_level = list(content)
    top_ids = [node.get(XML_ID) for node in top_level]
    starts = [anchor_lines[identifier][0] for identifier in top_ids]
    if starts != sorted(set(starts)) or \
            (starts and starts[-1] >= metadata_start):
        raise StructuredSourceError(
            "PDF independently computed Markdown block order is not exact")
    ends = [*([start - 1 for start in starts[1:]]), metadata_start - 1]
    regions = {}
    for node, start, end in zip(top_level, starts, ends):
        region = (start, end)
        for descendant in node.iter():
            identifier = descendant.get(XML_ID)
            if identifier:
                regions[identifier] = region
    regions[root_id] = (anchor_lines[root_id][0], metadata_start - 1)
    dependencies_start = anchor_lines["review-dependencies"][0]
    provenance_start = anchor_lines["review-provenance"][0]
    regions.update({
        "review-metadata": (metadata_start, dependencies_start - 1),
        "review-dependencies": (dependencies_start, provenance_start - 1),
        "review-provenance": (provenance_start, len(lines)),
    })
    return regions


def _coverage_expectations(
        root: ET.Element, subject_id: str,
        markdown_regions: dict[str, tuple[int, int]]):
    expected = []
    sequence = 0

    def visit(node: ET.Element, nearest_item: str | None, plane: str):
        nonlocal sequence
        sequence += 1
        item_id = node.get(XML_ID) or nearest_item
        local = _local(node)
        node_ref = "%s:n%d:%s" % (subject_id, sequence, local)
        if plane in {"content", "document"} and item_id:
            classification = "review-visible"
            anchors = [_ANCHOR_PREFIX + item_id]
            regions = [markdown_regions[item_id]]
        elif plane == "content":
            classification = "mechanically-derived"
            anchors = []
            regions = []
        elif plane in {"dependencies", "provenance", "metadata"}:
            classification = "review-scheduled"
            review_id = {
                "dependencies": "review-dependencies",
                "provenance": "review-provenance",
                "metadata": "review-metadata",
            }[plane]
            anchors = [_ANCHOR_PREFIX + review_id]
            regions = [markdown_regions[review_id]]
        elif plane == "projection":
            classification = "mechanically-derived"
            anchors = []
            regions = [(1, 1)]
        else:
            classification = "internal-justified"
            anchors = []
            regions = []

        def add(suffix):
            expected.append((node_ref + suffix, node_ref, suffix[1:],
                             classification, anchors, regions))

        add(":element")
        for name in sorted(node.attrib):
            add(":attribute:" + name.rsplit("}", 1)[-1])
        if node.text is not None:
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

    visit(root, root.get(XML_ID), "document")
    return expected


def _validate_projection_coverage(
        artifact: ParsedArtifact, projection: Projection,
        document_id: str, manifest: dict, manifest_raw_digest: str) -> int:
    if artifact.raw_bytes != readable_xml_bytes(artifact.root):
        raise StructuredSourceError(
            "PDF independent readable serialization census is stale")
    if manifest_raw_digest != raw_digest(canonical_json(manifest)):
        raise StructuredSourceError("PDF independent manifest binding is stale")
    if set(artifact.fragment_digests) != set(artifact.typed_item_records):
        raise StructuredSourceError("PDF independent typed-item census is stale")
    for item_id, record in artifact.typed_item_records.items():
        if not isinstance(record, dict) or set(record) != {
                "authorityScheme", "digestDomain", "documentId", "itemId",
                "itemType", "schemaProfile", "substantiveMetadata",
                "typedContent"} or record.get("itemId") != item_id or \
                typed_item_digest(
                    authority_scheme=record["authorityScheme"],
                    schema_profile=record["schemaProfile"],
                    document_id=record["documentId"], item_id=record["itemId"],
                    item_type=record["itemType"],
                    typed_content=record["typedContent"],
                    substantive_metadata=record["substantiveMetadata"]) != \
                artifact.fragment_digests[item_id]:
            raise StructuredSourceError(
                "PDF independent typed-item digest census is stale")
    value = projection.coverage
    if not isinstance(value, dict) or set(value) != {
            "coverageVersion", "fields", "markdownDigest", "projectionProfile",
            "sourceProfile", "sourceRawDigest", "subjectId"} or \
            value.get("coverageVersion") != "1" or \
            value.get("subjectId") != document_id or \
            value.get("sourceRawDigest") != artifact.raw_digest or \
            value.get("sourceProfile") != artifact.profile or \
            value.get("projectionProfile") != "gfm-v1" or \
            value.get("markdownDigest") != projection.markdown_digest or \
            projection.markdown_digest != raw_digest(projection.markdown):
        raise StructuredSourceError(
            "PDF computed field/projection coverage envelope is stale")
    fields = value.get("fields")
    markdown_regions = _independent_markdown_regions(
        artifact.root, projection.markdown)
    expected = _coverage_expectations(
        artifact.root, document_id, markdown_regions)
    if not isinstance(fields, list) or len(fields) != len(expected):
        raise StructuredSourceError("PDF computed field coverage census is incomplete")
    seen = set()
    for actual, required in zip(fields, expected):
        (field_id, node_ref, field_name, classification, anchors,
         expected_regions) = required
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
        normalized_regions = [
            (region["startLine"], region["endLine"]) for region in regions]
        if normalized_regions != expected_regions:
            raise StructuredSourceError(
                "PDF computed field coverage region is stale")
        if classification in {"review-visible", "review-scheduled"} and \
                not regions:
            raise StructuredSourceError(
                "PDF review field has no generated Markdown region")
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
        item_id=entry.get("itemId"),
        digest=entry.get("digest"))
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
    expected_anchors = {
        root.get(XML_ID), *item_ids,
        "review-metadata", "review-dependencies", "review-provenance"}
    if len(anchors) != len(expected_anchors) or set(anchors) != expected_anchors:
        raise StructuredSourceError(
            "PDF generated Markdown anchor census is not exact")
    field_count = _validate_projection_coverage(
        artifact, projection, document.document_id, manifest,
        manifest_raw_digest)

    items = []
    for ordinal, node in enumerate(item_nodes, start=1):
        item_id = node.get(XML_ID)
        record = artifact.typed_item_records.get(item_id)
        if not isinstance(record, dict) or record.get("itemId") != item_id:
            raise StructuredSourceError("PDF typed item record is absent")
        metadata = tuple(sorted(record["substantiveMetadata"].items()))
        direct_assets = tuple(sorted({
            entry.get("assetId") for entry in node.iter()
            if _local(entry) in {"image", "figure"} and
            entry.get("assetId") is not None}))
        digest = artifact.fragment_digests.get(item_id)
        if not isinstance(digest, str):
            raise StructuredSourceError("PDF item typed-item digest is absent")
        items.append(TranscriptionItem(
            item_id=item_id, item_type=_local(node),
            parent_id=parent_by_id[item_id],
            child_ids=tuple(children_by_id[item_id]), ordinal=ordinal,
            metadata=metadata,
            typed_content=_freeze_typed_content(record["typedContent"]),
            content_digest=digest, provenance=evidence_by_id[item_id],
            asset_ids=direct_assets,
        ))

    document_record = artifact.typed_item_records.get(root.get(XML_ID))
    document_digest = artifact.fragment_digests.get(root.get(XML_ID))
    if not isinstance(document_record, dict) or \
            document_record.get("itemType") != "document" or \
            document_record.get("substantiveMetadata") != {} or \
            not isinstance(document_record.get("typedContent"), list) or \
            not isinstance(document_digest, str):
        raise StructuredSourceError("PDF typed document item is incomplete")
    top_level_ids = tuple(node.get(XML_ID) for node in content)
    if any(item_id is None for item_id in top_level_ids):
        raise StructuredSourceError("PDF typed document hierarchy is incomplete")
    document_item = TypedDocumentItem(
        item_id=root.get(XML_ID), item_type="document",
        child_ids=top_level_ids,
        typed_content=tuple(_freeze_typed_node(node)
                            for node in document_record["typedContent"]),
        content_digest=document_digest, source=source)

    convenience = tuple(ConvenienceBinding(
        path=entry["path"], raw_digest=entry["rawDigest"], size=entry["size"],
        role=entry["role"], non_authoritative=entry["nonAuthoritative"])
        for entry in manifest["convenienceDerivatives"])
    return PDFTranscriptionSurface(
        package_id=package_id, authority_scheme=AUTHORITY_SCHEME,
        representation_role=TRANSCRIPTION_ROLE, schema_profile=artifact.profile,
        xml_path=xml_path, xml_raw_digest=artifact.raw_digest,
        manifest_path=manifest_path, manifest_raw_digest=manifest_raw_digest,
        markdown_path=markdown_path,
        markdown_raw_digest=projection.markdown_digest, document=document,
        document_item=document_item, source=source, items=tuple(items),
        dependencies=declared_dependencies,
        assets=assets, convenience_derivatives=convenience,
        coverage_field_count=field_count,
    )
