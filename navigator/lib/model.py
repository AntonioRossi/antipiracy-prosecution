"""Immutable XML-only semantic model for one navigator edition."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import os
import re
from types import MappingProxyType

from structured_source.canonical import raw_digest

from . import canon, claims as claims_mod, depgraph, projections
from . import registry as registry_mod, schema_validate

C = "{urn:aa11393:ssp:content:1}"
R = "{urn:aa11393:navigator:relations:1}"
W = "{urn:aa11393:navigator:wording:1}"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
RELATION_NAMESPACE = "urn:aa11393:navigator:relations:1"
WORDING_NAMESPACE = "urn:aa11393:navigator:wording:1"
RELATION_SCHEMA = "navigator/schema/navigator-relations.xsd"
WORDING_SCHEMA = "navigator/schema/wording.xsd"
SHARED_WORDING = "navigator/wording/shared.wording.xml"
EDITION_SCHEMA = "navigator/schema/edition.schema.json"
_STABLE_ID = re.compile(r"[A-Za-z][A-Za-z0-9._:-]*\Z")
_TIMESTAMP = re.compile(
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z\Z")
_WORDING_CONTRACT = {
    "counsel-legend": ("legend", "counsel-legend"),
    "standing-disclaimer": ("disclaimer", "standing-disclaimer"),
    "authority-pct-as-filed": ("provenance", "authority-provenance"),
    "source-input-provenance": ("provenance", "source-input-provenance"),
    "provenance-summary": ("provenance", "provenance-summary"),
    "editorial-not-filed": ("editorial", "editorial-label"),
    "claim-set-guidance": ("editorial", "guidance-label"),
    "artifact-label-technical-preview": ("release-profile", "artifact-label"),
    "artifact-watermark-technical-preview": ("security", "artifact-watermark"),
    "bundle-manifest-neutral": ("bundle-manifest", "bundle-manifest"),
}
_WORDING_PREFIX_CONTRACT = (
    ("mapping-status-", "mapping-status", "mapping-status"),
    ("mapping-role-", "mapping-role", "mapping-role"),
    ("caution-type-", "caution", "caution-type"),
    ("caution-scope-", "caution", "caution-scope"),
    ("gate-disposition-", "disposition", "gate-disposition"),
    ("generalization-", "caution", "generalization-caution"),
    ("gate-label-", "gate-label", "gate-label"),
)
_SLOT_CONTRACT = {
    "standing-disclaimer": (
        ("editionVersion", "stable-id", "registered-control",
         "edition.claimSetVersion"),
    ),
    "provenance-summary": (
        ("timestamp", "timestamp", "registered-control",
         "edition.declaredReleaseTimestamp"),
        ("claims", "integer", "closed-derivation", "edition.claimCount"),
        ("units", "integer", "closed-derivation", "edition.unitCount"),
        ("blocks", "integer", "closed-derivation", "pct.blockCount"),
    ),
    "bundle-manifest-neutral": (
        ("naEditionVersion", "stable-id", "registered-control",
         "edition.na.claimSetVersion"),
        ("afEditionVersion", "stable-id", "registered-control",
         "edition.af.claimSetVersion"),
    ),
}


class ModelError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class SourceItem:
    fragment_id: str
    text: str
    content_digest: str
    binding_kind: str


@dataclass(frozen=True, slots=True)
class Asset:
    asset_id: str
    path: str
    media_type: str
    data: bytes
    raw_digest: str


@dataclass(frozen=True, slots=True)
class ContentNode:
    fragment_id: str | None
    kind: str
    text: str
    level: int | None
    attributes: tuple[tuple[str, str], ...]
    children: tuple["ContentNode", ...]
    content_digest: str | None
    editorial: bool


@dataclass(frozen=True, slots=True)
class Endpoint:
    document_id: str
    fragment_id: str
    content_digest: str


@dataclass(frozen=True, slots=True)
class Caution:
    kind: str
    gate_id: str | None
    code: str | None


@dataclass(frozen=True, slots=True)
class Target:
    role: str
    endpoints: tuple[Endpoint, ...]
    note: str
    caution: Caution | None


@dataclass(frozen=True, slots=True)
class Mapping:
    relation_id: str
    status: str
    subject: Endpoint
    unit_kind: str
    unit_index: int
    caution: Caution | None
    targets: tuple[Target, ...]


@dataclass(frozen=True, slots=True)
class PhraseMapping:
    relation_id: str
    parent: Endpoint
    unit_kind: str
    unit_index: int
    exact_text: str
    start: int
    end: int
    targets: tuple[Target, ...]


@dataclass(frozen=True, slots=True)
class GateDefinition:
    gate_id: str
    code: str
    required_scope: str
    source: Endpoint


@dataclass(frozen=True, slots=True)
class Disposition:
    disposition_id: str
    gate_id: str
    value: str
    subject_kind: str
    subject: Endpoint
    unit_kind: str | None
    unit_index: int | None


@dataclass(frozen=True, slots=True)
class RelationDocument:
    role: str
    document_id: str
    semantic_digest: str


@dataclass(frozen=True, slots=True)
class RelationSet:
    relation_set_id: str
    edition: str
    documents: tuple[RelationDocument, ...]
    gate_definitions: tuple[GateDefinition, ...]
    mappings: tuple[Mapping, ...]
    phrase_mappings: tuple[PhraseMapping, ...]
    dispositions: tuple[Disposition, ...]


@dataclass(frozen=True, slots=True)
class WordingSlot:
    name: str
    scalar_type: str
    origin_kind: str
    origin_ref: str


@dataclass(frozen=True, slots=True)
class WordingEntry:
    wording_id: str
    category: str
    usage: tuple[str, ...]
    text: str
    slots: tuple[WordingSlot, ...]


def _wording_contract(wording_id):
    direct = _WORDING_CONTRACT.get(wording_id)
    if direct is not None:
        return direct
    for prefix, category, usage in _WORDING_PREFIX_CONTRACT:
        if wording_id.startswith(prefix):
            return category, usage
    return None


def _slot_shape(entry):
    return tuple((slot.name, slot.scalar_type, slot.origin_kind, slot.origin_ref)
                 for slot in entry.slots)


def _render_wording_entry(entry, values):
    slots = {slot.name: slot for slot in entry.slots}
    if set(values) != set(slots):
        raise ModelError("controlled wording slot inventory is not exact")
    text = entry.text
    for name, slot in slots.items():
        value = values[name]
        if slot.scalar_type == "integer":
            if not isinstance(value, int) or isinstance(value, bool):
                raise ModelError("controlled wording integer slot is invalid")
            rendered = str(value)
        else:
            if not isinstance(value, str) or not value or \
                    canon.normalize_nfc(value) != value:
                raise ModelError("controlled wording text slot is invalid")
            rendered = value
            if slot.scalar_type == "stable-id" and \
                    _STABLE_ID.fullmatch(value) is None:
                raise ModelError("controlled wording stable-id slot is invalid")
            if slot.scalar_type == "timestamp" and \
                    _TIMESTAMP.fullmatch(value) is None:
                raise ModelError("controlled wording timestamp slot is invalid")
        token = "{%s}" % name
        if text.count(token) != 1:
            raise ModelError("controlled wording slot occurrence is stale")
        text = text.replace(token, rendered)
    if re.search(r"\{[A-Za-z][A-Za-z0-9._:-]*\}", text):
        raise ModelError("controlled wording retains an unresolved slot")
    return text


def _local(element):
    return element.tag.rsplit("}", 1)[-1]


def _plain_text(element) -> str:
    if _local(element) == "codeBlock":
        return canon.canon_code(element.text or "")
    parts = []

    def visit(node):
        local = _local(node)
        if local == "text":
            parts.append(node.text or "")
            return
        if local == "space":
            parts.append(" ")
            return
        if local in {"softBreak", "lineBreak"}:
            parts.append("\n")
            return
        if local == "image":
            parts.append(node.get("alt", ""))
            return
        for child in node:
            visit(child)

    visit(element)
    return canon.canon_prose("".join(parts))


def _content_node(element, fragment_digests, editorial_ids, inherited=False):
    identifier = element.get(XML_ID)
    editorial = inherited or identifier in editorial_ids
    attributes = tuple(sorted(
        (name.rsplit("}", 1)[-1], value)
        for name, value in element.attrib.items() if name != XML_ID))
    level = None
    if _local(element) == "heading":
        try:
            level = int(element.get("level"))
        except (TypeError, ValueError) as exc:
            raise ModelError("disclosure heading level is invalid") from exc
    digest = fragment_digests.get(identifier) if identifier else None
    if identifier and digest is None:
        raise ModelError("addressable disclosure node has no semantic digest")
    return ContentNode(
        fragment_id=identifier,
        kind=_local(element),
        text=_plain_text(element),
        level=level,
        attributes=attributes,
        children=tuple(_content_node(
            child, fragment_digests, editorial_ids, editorial)
            for child in element),
        content_digest=digest,
        editorial=editorial,
    )


def _disclosure(content_root, fragment_digests):
    blocks = list(content_root)
    wrappers = [index for index, block in enumerate(blocks)
                if _local(block) == "heading" and
                _plain_text(block) == "5. International Application Text"]
    if len(wrappers) != 1 or wrappers[0] + 1 >= len(blocks):
        raise ModelError("PCT filed-text render boundary is not exact")
    filed = blocks[wrappers[0] + 1:]
    texts = [_plain_text(block) for block in filed]
    if _local(filed[0]) != "paragraph" or not texts[0].startswith(
            "AI – DRIVEN SYSTEM AND METHOD"):
        raise ModelError("PCT filed title is absent at the render boundary")

    def one_heading(text):
        found = [index for index, block in enumerate(filed)
                 if _local(block) == "heading" and texts[index] == text]
        if len(found) != 1:
            raise ModelError("PCT section heading is not exact: %s" % text)
        return found[0]

    description = one_heading("Description")
    claims_heading = one_heading("Claims")
    abstract = one_heading("Abstract")
    drawings = one_heading("6. Drawings")
    if not 0 < description < claims_heading < abstract < drawings:
        raise ModelError("PCT title/description/claims/abstract/drawings order is stale")
    examples = [text for index, text in enumerate(texts)
                if _local(filed[index]) == "heading" and
                re.fullmatch(r"Example [1-5]", text)]
    if examples != ["Example %d" % number for number in range(1, 6)]:
        raise ModelError("PCT Example 1..5 heading inventory is not exact")
    pct_claims = []
    for text in texts[claims_heading + 1:abstract]:
        match = re.match(r"^([1-9][0-9]*)\.\s", text)
        if match:
            pct_claims.append(int(match.group(1)))
    if pct_claims != list(range(1, 19)):
        raise ModelError("PCT claim inventory is not exactly 1..18")

    drawing_blocks = filed[drawings + 1:]
    image_positions = [index for index, block in enumerate(drawing_blocks)
                       if any(_local(node) == "image" for node in block.iter())]
    image_ids = [node.get("assetId") for block in drawing_blocks
                 for node in block.iter() if _local(node) == "image"]
    if image_ids != ["asset-fig-%d-png" % number for number in range(1, 5)] or \
            len(image_positions) != 4:
        raise ModelError("PCT figure inventory is not exactly figures 1..4")
    if not drawing_blocks or _local(drawing_blocks[0]) != "blockQuotation":
        raise ModelError("PCT drawing transcription note is absent")
    editorial_ids = {drawing_blocks[0].get(XML_ID)}
    for position in image_positions:
        if position + 1 >= len(drawing_blocks) or \
                _local(drawing_blocks[position + 1]) != "paragraph":
            raise ModelError("PCT drawing reference caption is absent")
        editorial_ids.add(drawing_blocks[position + 1].get(XML_ID))
    if _local(drawing_blocks[-1]) != "paragraph" or \
            not _plain_text(drawing_blocks[-1]).startswith("Application: PCT/"):
        raise ModelError("PCT editorial filing footer is absent")
    editorial_ids.add(drawing_blocks[-1].get(XML_ID))
    if None in editorial_ids or len(editorial_ids) != 6:
        raise ModelError("PCT editorial marker inventory is not exact")

    nodes = tuple(_content_node(
        block, fragment_digests, editorial_ids) for block in filed)
    index = {}

    def add(node):
        if node.fragment_id:
            if node.fragment_id in index:
                raise ModelError("duplicate disclosure fragment identity")
            index[node.fragment_id] = node
        for child in node.children:
            add(child)

    for node in nodes:
        add(node)
    return nodes, MappingProxyType(index), frozenset(editorial_ids)


def _source_items(authored_root, fragment_digests):
    parent = authored_root.find(C + "fragments")
    if parent is None:
        raise ModelError("authored source has no fragment index")
    items = {}
    for fragment in parent.findall(C + "fragment"):
        identifier = fragment.get(XML_ID)
        excerpt = fragment.find(C + "excerpt")
        if not identifier or excerpt is None or not excerpt.text or \
                identifier not in fragment_digests:
            raise ModelError("authored source item is incomplete")
        items[identifier] = SourceItem(
            fragment_id=identifier,
            text=excerpt.text,
            content_digest=fragment_digests[identifier],
            binding_kind=fragment.get("bindingKind"),
        )
    return MappingProxyType(items)


def _endpoint(element):
    return Endpoint(
        document_id=element.get("documentId"),
        fragment_id=element.get("fragmentId"),
        content_digest=element.get("fragmentContentDigest"),
    )


def _caution(element):
    if element is None:
        return None
    return Caution(
        kind=element.get("kind"), gate_id=element.get("gateId"),
        code=element.get("code"))


def _target(element):
    note = element.find(R + "note")
    return Target(
        role=element.get("role"),
        endpoints=tuple(_endpoint(item)
                        for item in element.findall(R + "endpoint")),
        note=note.text if note is not None else "",
        caution=_caution(element.find(R + "caution")),
    )


def _targets(parent):
    if parent is None:
        return ()
    return tuple(_target(item) for item in parent.findall(R + "target"))


def _unique_span(text, exact):
    starts = []
    offset = 0
    while True:
        found = text.find(exact, offset)
        if found < 0:
            break
        starts.append(found)
        offset = found + 1
    if len(starts) != 1:
        raise ModelError("phrase selector exactText does not resolve uniquely")
    start = starts[0]
    return start, start + len(exact)


def _parse_relations(root, units_by_fragment):
    documents = tuple(RelationDocument(
        role=item.get("role"), document_id=item.get("documentId"),
        semantic_digest=item.get("semanticDigest"))
        for item in root.findall(R + "documents/" + R + "document"))
    gates = []
    for item in root.findall(R + "gateDefinitions/" + R + "gate"):
        gates.append(GateDefinition(
            gate_id=item.get("gateId"), code=item.get("code"),
            required_scope=item.get("requiredScope"),
            source=_endpoint(item.find(R + "source/" + R + "endpoint")),
        ))
    mappings = []
    for item in root.findall(R + "mappings/" + R + "mapping"):
        subject = item.find(R + "subject")
        mappings.append(Mapping(
            relation_id=item.get("relationId"), status=item.get("status"),
            subject=_endpoint(subject.find(R + "endpoint")),
            unit_kind=subject.get("unitKind"),
            unit_index=int(subject.get("unitIndex")),
            caution=_caution(item.find(R + "caution")),
            targets=_targets(item.find(R + "targets")),
        ))
    phrases = []
    for item in root.findall(R + "phraseMappings/" + R + "phrase"):
        parent = item.find(R + "parent")
        endpoint = _endpoint(parent.find(R + "endpoint"))
        selector = item.find(R + "selector")
        exact = selector.find(R + "exactText").text
        unit = units_by_fragment.get(endpoint.fragment_id)
        if unit is None:
            raise ModelError("phrase parent is not a claim unit")
        start, end = _unique_span(unit.text, exact)
        phrases.append(PhraseMapping(
            relation_id=item.get("relationId"), parent=endpoint,
            unit_kind=parent.get("unitKind"),
            unit_index=int(parent.get("unitIndex")),
            exact_text=exact, start=start, end=end,
            targets=_targets(item.find(R + "targets")),
        ))
    dispositions = []
    for item in root.findall(R + "dispositions/" + R + "disposition"):
        subject = item.find(R + "subject")
        dispositions.append(Disposition(
            disposition_id=item.get("dispositionId"),
            gate_id=item.get("gateId"), value=item.get("value"),
            subject_kind=subject.get("kind"),
            subject=_endpoint(subject.find(R + "endpoint")),
            unit_kind=subject.get("unitKind"),
            unit_index=(int(subject.get("unitIndex"))
                        if subject.get("unitIndex") is not None else None),
        ))
    return RelationSet(
        relation_set_id=root.get("relationSetId"), edition=root.get("edition"),
        documents=documents, gate_definitions=tuple(gates),
        mappings=tuple(mappings), phrase_mappings=tuple(phrases),
        dispositions=tuple(dispositions),
    )


def _parse_wording(root, expected_scope):
    if root.get("scope") != expected_scope or root.get("wordingSetId") != expected_scope:
        raise ModelError("controlled wording scope is stale")
    entries = {}
    for element in root.findall(W + "entry"):
        identifier = element.get("wordingId")
        text = element.find(W + "text")
        slots_parent = element.find(W + "slots")
        slots = tuple(WordingSlot(
            name=item.get("name"), scalar_type=item.get("scalarType"),
            origin_kind=item.get("originKind"), origin_ref=item.get("originRef"))
            for item in (() if slots_parent is None
                         else slots_parent.findall(W + "slot")))
        if not identifier or identifier in entries or text is None or not text.text:
            raise ModelError("controlled wording entry is incomplete or duplicated")
        entry = WordingEntry(
            wording_id=identifier, category=element.get("category"),
            usage=tuple(item.get("context")
                        for item in element.findall(W + "usage")),
            text=text.text, slots=slots,
        )
        contract = _wording_contract(identifier)
        expected_slots = _SLOT_CONTRACT.get(identifier, ())
        scope_is_current = (
            (expected_scope == "shared" and
             not identifier.startswith("gate-label-")) or
            (expected_scope in {"na", "af"} and
             identifier.startswith("gate-label-%s-" % expected_scope))
        )
        if not scope_is_current or contract is None or \
                (entry.category, entry.usage) != (contract[0], (contract[1],)) or \
                _slot_shape(entry) != expected_slots:
            raise ModelError(
                "controlled wording context or slot origin is not current")
        entries[identifier] = entry
    return entries


class EditionModel:
    """One current edition, decoded from registered XML and closed controls."""

    def __setattr__(self, name, value):
        if getattr(self, "_sealed", False):
            raise AttributeError("EditionModel is immutable after construction")
        object.__setattr__(self, name, value)

    def __init__(self, gw, edition_path):
        try:
            config = canon.parse_json(gw.read_text(edition_path))
            edition_schema = canon.parse_json(gw.read_text(EDITION_SCHEMA))
            schema_validate.check_schema(edition_schema)
            problems = schema_validate.validate(config, edition_schema)
        except Exception as exc:
            raise ModelError("edition control is unreadable or invalid") from exc
        if problems:
            raise ModelError("edition control is invalid: %s" % "; ".join(problems))
        expected_path = "navigator/editions/%s.json" % config["editionId"]
        if edition_path != expected_path or \
                config["consumerId"] != "navigator-" + config["editionId"] or \
                config["strategyPrefix"].casefold() != config["editionId"] or \
                config["relationPath"] != (
                    "navigator/relations/%s__pct.relations.xml" % config["editionId"]) or \
                config["editionWordingPath"] != (
                    "navigator/wording/%s.wording.xml" % config["editionId"]):
            raise ModelError("edition identity/path bindings are not exact")
        try:
            parsed_timestamp = datetime.fromisoformat(
                config["declaredReleaseTimestamp"].replace("Z", "+00:00"))
        except ValueError as exc:
            raise ModelError("declared release timestamp is invalid") from exc
        if not _TIMESTAMP.fullmatch(config["declaredReleaseTimestamp"]) or \
                parsed_timestamp.utcoffset().total_seconds() != 0:
            raise ModelError("declared release timestamp is not a UTC second")

        self.edition_id = config["editionId"]
        self.display_name = config["displayName"]
        self.strategy_name = config["strategyName"]
        self.strategy_prefix = config["strategyPrefix"]
        self.artifact_name = config["artifactName"]
        self.declared_release_timestamp = config["declaredReleaseTimestamp"]
        self.claim_set_version = config["claimSetVersion"]
        self.independent_claims = tuple(config["independentClaims"])
        self._expected_census = MappingProxyType(dict(config["census"]))
        self._expected_groups = tuple(config["groups"])
        self._edition_path = edition_path
        self._relation_path = config["relationPath"]
        self._edition_wording_path = config["editionWordingPath"]

        registry = registry_mod.Registry(gw)
        claim_package, pct_package = registry.consumer_packages(
            config["consumerId"], config["claimPackageId"])
        claim_document, claim_artifact = registry.load_document(claim_package)
        pct_document, pct_artifact = registry.load_document(pct_package)
        self.source_documents = (claim_document, pct_document)
        self._document_artifacts = MappingProxyType({
            claim_package: claim_artifact, pct_package: pct_artifact})
        self._documents = MappingProxyType({
            item.document_id: item for item in self.source_documents})

        claim_set = claims_mod.parse_claims(
            claim_artifact.root, claim_artifact.fragment_digests)
        self.claims = claim_set.claims
        self.claims_by_number = claim_set.by_number
        self.units_by_fragment = claim_set.units_by_fragment
        self.claim_groups = claim_set.groups
        self._source_items = _source_items(
            claim_artifact.root, claim_artifact.fragment_digests)
        graph = depgraph.build(self.claims, self.independent_claims)
        self.parents = graph.parents
        self.children = graph.children
        self.aggregate_hashes = graph.aggregate_hashes
        self.chain_hashes = graph.chain_hashes

        content = pct_artifact.root.find(C + "content")
        if content is None:
            raise ModelError("PCT XML omits typed content")
        self.disclosure_blocks, self.disclosure_index, self._editorial_ids = \
            _disclosure(content, pct_artifact.fragment_digests)
        self.assets = self._load_assets(
            pct_artifact.root, pct_package, registry, gw)

        relation_root = gw.read_validated_xml(
            self._relation_path, RELATION_SCHEMA,
            expected_namespace=RELATION_NAMESPACE, expected_root="relations")
        self.relations = _parse_relations(relation_root, self.units_by_fragment)
        self.relation_set_id = self.relations.relation_set_id
        self._validate_relations(claim_package, pct_package)

        shared_bytes = gw.read_bytes(SHARED_WORDING)
        shared_root = gw.read_validated_xml(
            SHARED_WORDING, WORDING_SCHEMA,
            expected_namespace=WORDING_NAMESPACE, expected_root="wording")
        edition_root = gw.read_validated_xml(
            self._edition_wording_path, WORDING_SCHEMA,
            expected_namespace=WORDING_NAMESPACE, expected_root="wording")
        wording = _parse_wording(shared_root, "shared")
        edition_wording = _parse_wording(edition_root, self.edition_id)
        collision = set(wording) & set(edition_wording)
        if collision:
            raise ModelError("shared and edition wording identities collide")
        wording_owners = {identifier: SHARED_WORDING for identifier in wording}
        wording_owners.update({
            identifier: self._edition_wording_path
            for identifier in edition_wording
        })
        wording.update(edition_wording)
        self._wording = MappingProxyType(wording)
        self._wording_owner_paths = MappingProxyType(wording_owners)
        self.shared_wording_digest = canon.bytes_digest(shared_bytes)
        self.profile_label = self.controlled_text(
            "artifact-label-technical-preview")

        self.mappings_by_unit = self._index_by_unit(self.relations.mappings)
        self.phrases_by_unit = self._index_by_unit(
            self.relations.phrase_mappings, parent=True)
        self.gates_by_id = MappingProxyType({
            gate.gate_id: gate for gate in self.relations.gate_definitions})
        disposition_index = {}
        for disposition in self.relations.dispositions:
            key = (disposition.subject_kind,
                   disposition.subject.fragment_id)
            disposition_index.setdefault(key, []).append(disposition)
        self.dispositions_by_subject = MappingProxyType({
            key: tuple(value) for key, value in sorted(disposition_index.items())})
        relation_index = {
            item.relation_id: item for item in
            (*self.relations.mappings, *self.relations.phrase_mappings)}
        if len(relation_index) != len(self.relations.mappings) + \
                len(self.relations.phrase_mappings):
            raise ModelError("relation identities are not globally unique")
        self._relations_by_id = MappingProxyType(relation_index)
        self.reverse_index = projections.reverse_index(
            self.relations, self.units_by_fragment)
        self._relations_by_endpoint = self._endpoint_relation_index()
        expected_reads = {
            self._edition_path,
            EDITION_SCHEMA,
            registry_mod.REGISTRY_PATH,
            self._relation_path,
            RELATION_SCHEMA,
            SHARED_WORDING,
            self._edition_wording_path,
            WORDING_SCHEMA,
        }
        expected_reads.update(document.registered_path
                              for document in self.source_documents)
        expected_reads.update(asset.path for asset in self.assets.values())
        gw.seal(expected_reads)
        self._read_inventory = tuple(sorted(gw.read_log.items()))
        lock = gw.lock()
        self._content_lock_digest = lock["lockDigest"]
        self.origin_inventory = projections.origin_inventory(self)
        # Parsed XML roots and their resolver are construction details.  No
        # mutable tree or generic repository reader survives into rendering.
        self._document_artifacts = None
        object.__setattr__(self, "_sealed", True)

    @staticmethod
    def _load_assets(pct_root, package_id, registry, gw):
        dependencies = {}
        parent = pct_root.find(C + "dependencies")
        if parent is None:
            raise ModelError("PCT XML omits registered asset dependencies")
        for item in parent.findall(C + "dependency"):
            if item.get("kind") == "asset":
                dependencies[item.get("subjectId")] = item.get("digest")
        assets = {}
        for path in registry.asset_paths(package_id):
            match = re.fullmatch(r".*/Fig-([1-4])[.]png", path)
            if match is None:
                raise ModelError("registered PCT asset path is outside the figure set")
            asset_id = "asset-fig-%s-png" % match.group(1)
            data = gw.read_bytes(path)
            digest = raw_digest(data)
            if dependencies.get(asset_id) != digest:
                raise ModelError("PCT asset digest does not match its XML dependency")
            assets[asset_id] = Asset(
                asset_id=asset_id, path=path, media_type="image/png",
                data=data, raw_digest=digest)
        if set(assets) != set(dependencies) or len(assets) != 4:
            raise ModelError("PCT registered asset/dependency inventory is not exact")
        return MappingProxyType(dict(sorted(assets.items())))

    @staticmethod
    def _index_by_unit(items, parent=False):
        index = {}
        for item in items:
            endpoint = item.parent if parent else item.subject
            index.setdefault(endpoint.fragment_id, []).append(item)
        return MappingProxyType({
            key: tuple(value) for key, value in sorted(index.items())})

    def _validate_endpoint(self, endpoint, expected_document, *, target=False):
        if endpoint.document_id != expected_document:
            raise ModelError("relation endpoint document identity is stale")
        artifact = self._document_artifacts[expected_document]
        if artifact.fragment_digests.get(endpoint.fragment_id) != \
                endpoint.content_digest:
            raise ModelError("relation endpoint ID/digest does not resolve exactly")
        if target:
            node = self.disclosure_index.get(endpoint.fragment_id)
            if node is None:
                raise ModelError(
                    "relation target is outside the PCT filed render boundary")
            if node.editorial:
                raise ModelError("relation target resolves to editorial material")

    def _validate_relations(self, claim_document, pct_document):
        if self.relations.edition != self.edition_id or \
                self.relations.relation_set_id != self.edition_id + "-pct":
            raise ModelError("relation set identity is stale")
        declared = {item.role: item for item in self.relations.documents}
        if set(declared) != {"subject", "target"}:
            raise ModelError("relation document role inventory is not exact")
        for role, document_id in (("subject", claim_document),
                                  ("target", pct_document)):
            metadata = self._documents[document_id]
            if declared[role].document_id != document_id or \
                    declared[role].semantic_digest != metadata.semantic_digest:
                raise ModelError("relation document semantic binding is stale")

        mapped = []
        for mapping in self.relations.mappings:
            self._validate_endpoint(mapping.subject, claim_document)
            unit = self.units_by_fragment.get(mapping.subject.fragment_id)
            if unit is None or unit.unit_kind != mapping.unit_kind or \
                    unit.unit_index != mapping.unit_index:
                raise ModelError("mapping subject does not resolve to its typed claim unit")
            mapped.append(unit.fragment_id)
            target_fragments = []
            for target in mapping.targets:
                for endpoint in target.endpoints:
                    self._validate_endpoint(endpoint, pct_document, target=True)
                    target_fragments.append(endpoint.fragment_id)
            if len(target_fragments) != len(set(target_fragments)):
                raise ModelError(
                    "one relation repeats an endpoint across candidate targets")
        if len(mapped) != len(set(mapped)) or set(mapped) != set(self.units_by_fragment):
            raise ModelError("relation mapping coverage is not exactly one per claim unit")

        selected = {}
        for phrase in self.relations.phrase_mappings:
            self._validate_endpoint(phrase.parent, claim_document)
            unit = self.units_by_fragment.get(phrase.parent.fragment_id)
            if unit is None or unit.unit_kind != phrase.unit_kind or \
                    unit.unit_index != phrase.unit_index or \
                    unit.text[phrase.start:phrase.end] != phrase.exact_text:
                raise ModelError("phrase selector is not a contiguous exact unit substring")
            span = (phrase.start, phrase.end)
            prior = selected.setdefault(unit.fragment_id, [])
            if any(span[0] < other[1] and other[0] < span[1]
                   for other in prior):
                raise ModelError("phrase selectors overlap within one claim unit")
            prior.append(span)
            target_fragments = []
            for target in phrase.targets:
                for endpoint in target.endpoints:
                    self._validate_endpoint(endpoint, pct_document, target=True)
                    target_fragments.append(endpoint.fragment_id)
            if len(target_fragments) != len(set(target_fragments)):
                raise ModelError(
                    "one phrase relation repeats an endpoint across candidate targets")

        for gate in self.relations.gate_definitions:
            self._validate_endpoint(gate.source, claim_document)
        for disposition in self.relations.dispositions:
            self._validate_endpoint(disposition.subject, claim_document)
            if disposition.subject_kind == "claim":
                match = re.fullmatch(r"claim-([1-9][0-9]*)",
                                     disposition.subject.fragment_id)
                if match is None or int(match.group(1)) not in self.claims_by_number:
                    raise ModelError("claim disposition subject is not a claim")
            else:
                unit = self.units_by_fragment.get(disposition.subject.fragment_id)
                if unit is None or unit.unit_kind != disposition.unit_kind or \
                        unit.unit_index != disposition.unit_index:
                    raise ModelError("unit disposition subject is stale")

    def _endpoint_relation_index(self):
        index = {}

        def add(endpoint, owner):
            index.setdefault((endpoint.document_id, endpoint.fragment_id), []).append(
                owner)

        for mapping in self.relations.mappings:
            add(mapping.subject, mapping)
            for target in mapping.targets:
                for endpoint in target.endpoints:
                    add(endpoint, mapping)
        for phrase in self.relations.phrase_mappings:
            add(phrase.parent, phrase)
            for target in phrase.targets:
                for endpoint in target.endpoints:
                    add(endpoint, phrase)
        for gate in self.relations.gate_definitions:
            add(gate.source, gate)
        for disposition in self.relations.dispositions:
            add(disposition.subject, disposition)
        return MappingProxyType({
            key: tuple(value) for key, value in sorted(index.items())})

    @property
    def read_inventory(self):
        return self._read_inventory

    @property
    def content_lock(self):
        reads = [{"path": path, "digest": digest}
                 for path, digest in self._read_inventory]
        return {
            "canonVersion": canon.CANON_VERSION,
            "reads": reads,
            "lockDigest": self._content_lock_digest,
        }

    def _origin_value(self, origin_ref):
        values = {
            "edition.claimSetVersion": self.claim_set_version,
            "edition.declaredReleaseTimestamp": self.declared_release_timestamp,
            "edition.claimCount": len(self.claims),
            "edition.unitCount": len(self.units_by_fragment),
            "pct.blockCount": len(self.disclosure_blocks),
        }
        try:
            return values[origin_ref]
        except KeyError as exc:
            raise ModelError(
                "controlled wording origin is not edition-resolvable") from exc

    def controlled_text(self, wording_id):
        entry = self._wording.get(wording_id)
        if entry is None:
            raise ModelError("controlled wording identity does not resolve")
        values = {slot.name: self._origin_value(slot.origin_ref)
                  for slot in entry.slots}
        return _render_wording_entry(entry, values)

    def get_document(self, document_id):
        document = self._documents.get(document_id)
        if document is None:
            raise ModelError("source document does not resolve")
        return document

    def get_metadata(self, document_id):
        document = self.get_document(document_id)
        return MappingProxyType({
            "documentId": document.document_id,
            "authorityScheme": document.authority_scheme,
            "xmlRole": document.xml_role,
            "semanticDigest": document.semantic_digest,
            "registeredPath": document.registered_path,
        })

    def get_item(self, document_id, fragment_id):
        if document_id == self.source_documents[0].document_id:
            unit = self.units_by_fragment.get(fragment_id)
            if unit is not None:
                return unit
            match = re.fullmatch(r"claim-([1-9][0-9]*)", fragment_id)
            if match and int(match.group(1)) in self.claims_by_number:
                return self.claims_by_number[int(match.group(1))]
            item = self._source_items.get(fragment_id)
        elif document_id == self.source_documents[1].document_id:
            item = self.disclosure_index.get(fragment_id)
        else:
            raise ModelError("source document does not resolve")
        if item is None:
            raise ModelError("source item does not resolve")
        return item

    def resolve_relation(self, relation_id):
        relation = self._relations_by_id.get(relation_id)
        if relation is None:
            raise ModelError("relation identity does not resolve")
        return relation

    def relations_for(self, document_id, fragment_id):
        self.get_item(document_id, fragment_id)
        return self._relations_by_endpoint.get((document_id, fragment_id), ())

    @staticmethod
    def dom_id(document_id, fragment_id):
        if not isinstance(document_id, str) or not isinstance(fragment_id, str):
            raise ModelError("DOM identity inputs must be strings")
        framed = (document_id + "\x00" + fragment_id).encode("utf-8")
        return "n-" + canon.bytes_digest(framed).rsplit(":", 1)[1]


def bundle_manifest_text(na_model, af_model):
    """Resolve shared bundle wording from the two typed edition origins."""
    if not isinstance(na_model, EditionModel) or \
            not isinstance(af_model, EditionModel) or \
            na_model.edition_id != "na" or af_model.edition_id != "af" or \
            na_model.shared_wording_digest != af_model.shared_wording_digest:
        raise ModelError("bundle wording models are not the exact edition pair")
    na_entry = na_model._wording.get("bundle-manifest-neutral")
    af_entry = af_model._wording.get("bundle-manifest-neutral")
    if na_entry is None or na_entry != af_entry:
        raise ModelError("bundle wording differs between edition models")
    return _render_wording_entry(na_entry, {
        "naEditionVersion": na_model.claim_set_version,
        "afEditionVersion": af_model.claim_set_version,
    })
