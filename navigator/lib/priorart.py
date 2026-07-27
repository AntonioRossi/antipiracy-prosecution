"""Immutable claims-to-prior-art model from declared XML handoffs."""

from __future__ import annotations

from dataclasses import dataclass
import re
from types import MappingProxyType

from structured_source.pdf_transcription import PDFTranscriptionSurface

from . import bundlezip, canon, claims as claims_mod, depgraph, projections
from . import registry as registry_mod, schema_validate
from .gateway import ContentLock
from .model import (
    EDITION_SCHEMA, WORDING_NAMESPACE, WORDING_SCHEMA, Endpoint, Mapping,
    ModelError, PhraseMapping, RelationSet, Target, WordingEntry,
    _parse_wording, _render_wording_entry, _source_items, _unique_span,
)

SR = "{urn:aa11393:ssp:relations:1}"
PRIOR_ART_WORDING = "navigator/wording/prior-art.wording.xml"


@dataclass(frozen=True, slots=True)
class PriorArtScopeDocument:
    document_id: str
    label: str


@dataclass(frozen=True, slots=True)
class PriorArtPassage:
    document_id: str
    fragment_id: str
    content_digest: str
    text: str
    page: int
    region: str | None
    uncertainty: str | None


@dataclass(frozen=True, slots=True)
class PriorArtCandidate:
    relation_id: str
    subject: Endpoint
    exact_text: str | None
    targets: tuple[Target, ...]


def _fields(relation):
    pairs = tuple((item.get("name"), item.text or "")
                  for item in relation.findall(SR + "assertionField"))
    if len(pairs) != len({name for name, unused in pairs}) or any(
            not name or not value.strip() or value != value.strip()
            for name, value in pairs):
        raise ModelError("prior-art relation fields are not exact")
    return dict(pairs)


def _endpoint(element):
    return Endpoint(
        document_id=element.get("documentId"),
        fragment_id=element.get("fragmentId"),
        content_digest=element.get("fragmentContentDigest"),
    )


def _typed_text(value):
    parts = []

    def visit(node):
        if node.text:
            parts.append(node.text)
        for child in node.children:
            visit(child)

    if value.text:
        parts.append(value.text)
    for child in value.children:
        visit(child)
    return canon.canon_prose(" ".join(parts))


class PriorArtModel:
    """One current strategy product using claim, scope, map, and passage XML."""

    def __setattr__(self, name, value):
        if getattr(self, "_sealed", False):
            raise AttributeError("PriorArtModel is immutable after construction")
        object.__setattr__(self, name, value)

    def __init__(self, gw, edition_path, consumer_input, *, capture_token,
                 plan_token, derivation_token):
        if capture_token is None or plan_token is None or derivation_token is None or \
                not isinstance(consumer_input, registry_mod.ConsumerInput) or \
                consumer_input.capture_token is not capture_token:
            raise ModelError("prior-art model inputs do not belong to one derivation")
        try:
            registry = registry_mod.Registry(gw, consumer_input)
            config = canon.parse_json(gw.read_text(edition_path))
            edition_schema = canon.parse_json(gw.read_text(EDITION_SCHEMA))
            schema_validate.check_schema(edition_schema)
            problems = schema_validate.validate(config, edition_schema)
        except Exception as exc:
            raise ModelError("prior-art product control is unreadable or invalid") from exc
        if problems:
            raise ModelError("prior-art product control is invalid: %s" %
                             "; ".join(problems))
        required_fields = {
            "comparisonPackageId", "passageMapPackageId",
            "priorArtWordingPath", "documentCensus"}
        if config["productKind"] != "prior-art" or \
                config["productId"] != config["editionId"] + "-prior-art" or \
                not required_fields.issubset(config) or \
                config["priorArtWordingPath"] != PRIOR_ART_WORDING or \
                edition_path != "navigator/editions/%s.json" % config["productId"] or \
                config["consumerId"] != "navigator-" + config["productId"] or \
                config["strategyPrefix"].casefold() != config["editionId"]:
            raise ModelError("prior-art product identity/path bindings are not exact")
        if any(field in config for field in ("relationPath", "editionWordingPath")):
            raise ModelError("prior-art product contains specification-only controls")
        try:
            bundlezip.parse_utc_second(config["declaredReleaseTimestamp"])
        except bundlezip.BundleError as exc:
            raise ModelError("declared release timestamp is not a UTC second") from exc

        self.product_id = config["productId"]
        self.product_kind = config["productKind"]
        self.edition_id = config["editionId"]
        self._consumer_id = config["consumerId"]
        self._claim_package_id = config["claimPackageId"]
        self._comparison_package_id = config["comparisonPackageId"]
        self._passage_map_package_id = config["passageMapPackageId"]
        self._capture_token = capture_token
        self._plan_token = plan_token
        self._derivation_token = derivation_token
        self.display_name = config["displayName"]
        self.strategy_name = config["strategyName"]
        self.strategy_prefix = config["strategyPrefix"]
        self.artifact_name = config["artifactName"]
        self.declared_release_timestamp = config["declaredReleaseTimestamp"]
        self.claim_set_version = config["claimSetVersion"]
        self.target_pane_label = "Prior-art passages"
        self.authority_header = "Prior-art XML evidence"
        self.forward_mode_label = "Claims → Prior art"
        self.reverse_mode_label = "Prior art → Claims"
        self.independent_claims = tuple(config["independentClaims"])
        self._expected_census = MappingProxyType(dict(config["census"]))
        self._expected_groups = tuple(config["groups"])
        self._expected_document_census = config["documentCensus"]
        self._edition_path = edition_path
        self._relation_path = registry.handoff(
            config["passageMapPackageId"])["path"]
        self._edition_wording_path = PRIOR_ART_WORDING
        self._handoff_validation_paths = registry.validation_paths

        package_ids = registry.prior_art_packages(
            config["consumerId"], config["claimPackageId"],
            config["comparisonPackageId"], config["passageMapPackageId"])
        claim_document, claim_artifact = registry.load_document(package_ids[0])
        comparison_document, comparison_artifact = registry.load_relation(package_ids[1])
        map_document, map_artifact = registry.load_relation(package_ids[2])
        target_documents = []
        target_surfaces = {}
        for package_id in package_ids[3:]:
            document, surface = registry.load_document(package_id)
            if not isinstance(surface, PDFTranscriptionSurface):
                raise ModelError("prior-art passage target is not a PDF transcription")
            target_documents.append(document)
            target_surfaces[document.document_id] = surface
        self.source_documents = (
            claim_document, comparison_document, map_document,
            *tuple(target_documents))
        self._documents = MappingProxyType({
            item.document_id: item for item in self.source_documents})

        claim_set = claims_mod.parse_claims(
            claim_artifact._validated_root(), claim_artifact.fragment_digests)
        self.claims = claim_set.claims
        self.claims_by_number = claim_set.by_number
        self.units_by_fragment = claim_set.units_by_fragment
        self.claim_groups = claim_set.groups
        self._source_items = _source_items(
            claim_artifact._validated_root(), claim_artifact.fragment_digests)
        graph = depgraph.build(self.claims, self.independent_claims)
        self.parents = graph.parents
        self.children = graph.children
        self.aggregate_hashes = graph.aggregate_hashes
        self.chain_hashes = graph.chain_hashes

        comparison_root = comparison_artifact._validated_root()
        scope_ids = []
        for relation in comparison_root.findall(SR + "relation"):
            for item in relation.findall(SR + "endpoint"):
                document_id = item.get("documentId", "")
                if item.get("role") == "evidence" and \
                        document_id.startswith("us-prior-art-") and \
                        document_id not in scope_ids:
                    scope_ids.append(document_id)
        scope_ids = sorted(scope_ids)
        if len(scope_ids) != self._expected_document_census:
            raise ModelError("prior-art comparison document census is stale")
        self.prior_art_scope = tuple(PriorArtScopeDocument(
            document_id=item, label=item.removeprefix("us-prior-art-").upper())
            for item in scope_ids)

        states = {}
        candidates = {}
        raw_candidates = []
        map_root = map_artifact._validated_root()
        for relation in map_root.findall(SR + "relation"):
            relation_id = relation.get("relationId")
            fields = _fields(relation)
            endpoint_elements = tuple(relation.findall(SR + "endpoint"))
            subjects = tuple(_endpoint(item) for item in endpoint_elements
                             if item.get("role") == "subject")
            evidence = tuple(_endpoint(item) for item in endpoint_elements
                             if item.get("role") == "evidence")
            if len(subjects) != 1:
                raise ModelError("prior-art map relation has no exact subject")
            subject = subjects[0]
            unit = self.units_by_fragment.get(subject.fragment_id)
            if subject.document_id != claim_document.document_id or unit is None or \
                    unit.content_digest != subject.content_digest:
                raise ModelError("prior-art map subject does not resolve exactly")
            kind = fields.get("record-kind")
            if kind == "state":
                if set(fields) != {"mapping-status", "record-kind"} or evidence or \
                        fields["mapping-status"] not in {
                            "mapped", "counsel-review-required"} or \
                        subject.fragment_id in states:
                    raise ModelError("prior-art state relation is malformed")
                states[subject.fragment_id] = (relation_id, fields["mapping-status"], subject)
            elif kind == "candidate":
                allowed = {"candidate-role", "proposition", "record-kind",
                           "subject-exact-text"}
                if not set(fields).issubset(allowed) or \
                        not {"candidate-role", "proposition", "record-kind"}.issubset(fields) or \
                        fields["candidate-role"] not in {"specific", "context", "combination"} or \
                        not evidence:
                    raise ModelError("prior-art candidate relation is malformed")
                raw_candidates.append((relation_id, subject, unit, fields, evidence))
                candidates.setdefault(subject.fragment_id, []).append(relation_id)
            else:
                raise ModelError("prior-art relation record kind is unsupported")
        if set(states) != set(self.units_by_fragment):
            raise ModelError("prior-art map state coverage is not exactly one per claim unit")

        target_values = {}
        passage_values = {}
        phrase_values = []
        candidate_values = []
        for relation_id, subject, unit, fields, evidence in raw_candidates:
            for endpoint in evidence:
                if endpoint.document_id not in scope_ids:
                    raise ModelError("mapped passage is outside comparison scope")
                surface = target_surfaces.get(endpoint.document_id)
                if surface is None:
                    raise ModelError("mapped passage has no declared XML handoff")
                item = surface.item(endpoint.fragment_id)
                if item.content_digest != endpoint.content_digest or \
                        endpoint.fragment_id == surface.document_item.item_id:
                    raise ModelError("mapped passage endpoint does not resolve exactly")
                passage_values[(endpoint.document_id, endpoint.fragment_id)] = PriorArtPassage(
                    document_id=endpoint.document_id,
                    fragment_id=endpoint.fragment_id,
                    content_digest=endpoint.content_digest,
                    text=_typed_text(item.typed_content),
                    page=item.provenance.page,
                    region=item.provenance.region,
                    uncertainty=item.provenance.uncertainty,
                )
            target = Target(
                role=fields["candidate-role"], endpoints=evidence,
                note=fields["proposition"], caution=None)
            exact = fields.get("subject-exact-text")
            if exact is None:
                target_values.setdefault(subject.fragment_id, []).append(target)
                candidate_values.append(PriorArtCandidate(
                    relation_id=relation_id, subject=subject,
                    exact_text=None, targets=(target,)))
            else:
                start, end = _unique_span(unit.text, exact)
                candidate = PhraseMapping(
                    relation_id=relation_id, parent=subject,
                    unit_kind=unit.unit_kind, unit_index=unit.unit_index,
                    exact_text=exact, start=start, end=end,
                    targets=(target,))
                phrase_values.append(candidate)
                candidate_values.append(candidate)

        mappings = []
        for unit_id, unit in self.units_by_fragment.items():
            relation_id, status, subject = states[unit_id]
            has_candidates = bool(candidates.get(unit_id))
            if (status == "mapped") != has_candidates:
                raise ModelError("prior-art state and candidate inventory disagree")
            mappings.append(Mapping(
                relation_id=relation_id, status=status, subject=subject,
                unit_kind=unit.unit_kind, unit_index=unit.unit_index,
                caution=None, targets=tuple(target_values.get(unit_id, ()))))
        self.relations = RelationSet(
            relation_set_id=config["passageMapPackageId"],
            edition=self.edition_id, documents=(), gate_definitions=(),
            mappings=tuple(mappings), phrase_mappings=tuple(phrase_values),
            dispositions=())
        self.relation_set_id = self.relations.relation_set_id
        self.mappings_by_unit = self._index_by_unit(self.relations.mappings)
        self.phrases_by_unit = self._index_by_unit(
            self.relations.phrase_mappings, parent=True)
        self.gates_by_id = MappingProxyType({})
        self.dispositions_by_subject = MappingProxyType({})
        self.candidate_relations = tuple(candidate_values)
        self._relations_by_id = MappingProxyType({
            item.relation_id: item for item in
            (*self.relations.mappings, *self.candidate_relations)})
        self.reverse_index = projections.reverse_index(
            self.relations, self.units_by_fragment)
        self.prior_art_passages = tuple(
            passage_values[key] for key in sorted(passage_values))
        self.disclosure_blocks = ()
        self.disclosure_index = MappingProxyType({
            item.fragment_id: item for item in self.prior_art_passages})
        self._editorial_ids = frozenset()
        self.assets = MappingProxyType({})
        self._relations_by_endpoint = self._endpoint_relation_index()

        wording_bytes = gw.read_bytes(PRIOR_ART_WORDING)
        wording_root = gw.read_validated_xml(
            PRIOR_ART_WORDING, WORDING_SCHEMA,
            expected_namespace=WORDING_NAMESPACE, expected_root="wording",
            parser_controls=registry.parser_controls)
        wording = _parse_wording(wording_root, "prior-art")
        self._wording = MappingProxyType(wording)
        self._wording_owner_paths = MappingProxyType({
            identifier: PRIOR_ART_WORDING for identifier in wording})
        self.shared_wording_digest = canon.bytes_digest(wording_bytes)
        self.profile_label = self.controlled_text(
            "artifact-label-technical-preview")

        expected_reads = {
            self._edition_path, EDITION_SCHEMA, registry_mod.REGISTRY_PATH,
            PRIOR_ART_WORDING, WORDING_SCHEMA}
        expected_reads.update(self._handoff_validation_paths)
        gw.seal(expected_reads)
        self._read_inventory = tuple(sorted(gw.read_log.items()))
        lock = gw.lock()
        if not isinstance(lock, ContentLock):
            raise ModelError("gateway did not construct an immutable content lock")
        self._content_lock = lock
        self.origin_inventory = projections.origin_inventory(self)
        object.__setattr__(self, "_sealed", True)

    @staticmethod
    def _index_by_unit(items, parent=False):
        values = {}
        for item in items:
            endpoint = item.parent if parent else item.subject
            values.setdefault(endpoint.fragment_id, []).append(item)
        return MappingProxyType({key: tuple(value)
                                 for key, value in sorted(values.items())})

    def _endpoint_relation_index(self):
        values = {}
        for relation in self.relations.mappings:
            subject = relation.subject
            values.setdefault((subject.document_id, subject.fragment_id), []).append(relation)
        for relation in self.candidate_relations:
            subject = (relation.parent if isinstance(relation, PhraseMapping)
                       else relation.subject)
            values.setdefault((subject.document_id, subject.fragment_id), []).append(relation)
            for target in relation.targets:
                for endpoint in target.endpoints:
                    values.setdefault((endpoint.document_id, endpoint.fragment_id), []).append(relation)
        return MappingProxyType({key: tuple(value)
                                 for key, value in sorted(values.items())})

    @property
    def read_inventory(self):
        return self._read_inventory

    @property
    def content_lock(self):
        return self._content_lock

    def _origin_value(self, origin_ref):
        values = {
            "edition.claimSetVersion": self.claim_set_version,
            "edition.declaredReleaseTimestamp": self.declared_release_timestamp,
            "edition.claimCount": len(self.claims),
            "edition.unitCount": len(self.units_by_fragment),
            "target.blockCount": len(self.prior_art_scope),
        }
        try:
            return values[origin_ref]
        except KeyError as exc:
            raise ModelError("controlled wording origin is not product-resolvable") from exc

    def controlled_text(self, wording_id):
        entry = self._wording.get(wording_id)
        if not isinstance(entry, WordingEntry):
            raise ModelError("controlled wording identity does not resolve")
        return _render_wording_entry(entry, {
            slot.name: self._origin_value(slot.origin_ref)
            for slot in entry.slots})

    def get_document(self, document_id):
        try:
            return self._documents[document_id]
        except KeyError as exc:
            raise ModelError("source document does not resolve") from exc

    def get_metadata(self, document_id):
        document = self.get_document(document_id)
        return MappingProxyType({
            "documentId": document.document_id,
            "authorityScheme": document.authority_scheme,
            "xmlRole": document.xml_role,
            "xmlRawDigest": document.xml_raw_digest,
            "registeredPath": document.registered_path,
        })

    def get_item(self, document_id, fragment_id):
        if document_id == self._claim_package_id:
            value = self.units_by_fragment.get(fragment_id) or \
                self._source_items.get(fragment_id)
            match = re.fullmatch(r"claim-([1-9][0-9]*)", fragment_id)
            if value is None and match:
                value = self.claims_by_number.get(int(match.group(1)))
        else:
            value = next((item for item in self.prior_art_passages
                          if item.document_id == document_id and
                          item.fragment_id == fragment_id), None)
        if value is None:
            raise ModelError("source item does not resolve")
        return value

    def resolve_relation(self, relation_id):
        try:
            return self._relations_by_id[relation_id]
        except KeyError as exc:
            raise ModelError("relation identity does not resolve") from exc

    def relations_for(self, document_id, fragment_id):
        self.get_item(document_id, fragment_id)
        return self._relations_by_endpoint.get((document_id, fragment_id), ())

    @staticmethod
    def dom_id(document_id, fragment_id):
        framed = (document_id + "\x00" + fragment_id).encode("utf-8")
        return "n-" + canon.bytes_digest(framed).rsplit(":", 1)[1]
