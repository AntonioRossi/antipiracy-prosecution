"""Immutable claims-to-prior-art model from declared XML handoffs."""

from __future__ import annotations

from dataclasses import dataclass
import re
from types import MappingProxyType

from structured_source.pdf_transcription import (
    PDFTranscriptionSurface, TypedContentNode,
)

from . import bundlezip, canon, claims as claims_mod, depgraph, projections
from . import registry as registry_mod, schema_validate
from .gateway import ContentLock
from .model import (
    EDITION_SCHEMA, WORDING_NAMESPACE, WORDING_SCHEMA, Endpoint, Mapping,
    ModelError, PhraseMapping, RelationSet, Target, WordingEntry,
    _parse_wording, _render_wording_entry, _source_items, _unique_span,
    _wording_origin_value,
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
class PriorArtReaderDocument:
    document_id: str
    label: str
    title: str
    content: tuple[TypedContentNode, ...]


@dataclass(frozen=True, slots=True)
class PriorArtObligation:
    relation_id: str
    matrix_relation_id: str
    matrix_field: str
    matrix_value: str
    status: str
    subject: Endpoint
    evidence: Endpoint
    claim_number: int


@dataclass(frozen=True, slots=True)
class PriorArtCandidate:
    relation_id: str
    subject: Endpoint
    exact_text: str | None
    obligation_ids: tuple[str, ...]
    targets: tuple[Target, ...]


@dataclass(frozen=True, slots=True)
class PriorArtReviewAllocation:
    relation_id: str
    subject: Endpoint
    obligation_ids: tuple[str, ...]
    relevance_note: str


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


def _claim_number(fragment_id):
    match = re.fullmatch(r"claim-([1-9][0-9]*)", fragment_id or "")
    if match is None:
        raise ModelError("prior-art obligation subject is not an exact claim")
    return int(match.group(1))


def _claim_numbers(value):
    normalized = value.replace("–", "-")
    numbers = []
    for start, end in re.findall(
            r"(?<![A-Za-z0-9])([1-9][0-9]*)(?:\s*-\s*([1-9][0-9]*))?",
            normalized):
        first = int(start)
        last = int(end or start)
        if last < first:
            raise ModelError("matrix claim range is reversed")
        numbers.extend(range(first, last + 1))
    return tuple(sorted(set(numbers)))


def _candidate_semantic_signature(
        subject, exact_text, role, obligation_ids, evidence):
    evidence_identity = tuple(sorted(
        (endpoint.document_id, endpoint.fragment_id,
         endpoint.content_digest) for endpoint in evidence))
    return (
        subject.document_id, subject.fragment_id, subject.content_digest,
        exact_text, role, obligation_ids,
        evidence_identity,
    )


def _allocation_semantic_signature(subject, obligation_ids):
    return (
        subject.document_id, subject.fragment_id, subject.content_digest,
        obligation_ids,
    )


def _record_unique_signature(inventory, signature, label):
    if signature in inventory:
        raise ModelError("%s semantic signature is duplicated" % label)
    inventory.add(signature)


def _validate_preamble_candidate(unit, role, obligation_ids,
                                 evidence_documents):
    if unit.unit_kind == "preamble" and (
            role == "combination" or len(obligation_ids) != 1 or
            len(evidence_documents) != 1):
        raise ModelError("preamble candidate is a synthetic claim roll-up")


def _validate_review_allocation(unit, selected_obligations):
    if any(item is None for item in selected_obligations) or any(
            item.claim_number != unit.claim_number or
            item.status != "counsel-review-required"
            for item in selected_obligations):
        raise ModelError(
            "fragment-review allocation does not close exact review obligations")


def _validate_candidate_obligation_coverage(obligations, referenced):
    mapped = {
        item.relation_id for item in obligations
        if item.status == "passage-mapped"}
    if set(referenced) != mapped:
        raise ModelError("mapped obligation and candidate coverage disagree")


def _primary_document(fields, name):
    value = fields.get(name)
    match = re.match(r"([ABC][1-9][0-9]*)\b", value or "")
    if match is None:
        raise ModelError("matrix inventory document identity is not exact")
    return "us-prior-art-" + match.group(1).casefold()


def _matrix_obligations(matrix_relations):
    """Compute the exact claim/document obligation census from matrix XML."""
    expected = {}
    for relation_id, relation in matrix_relations.items():
        fields = relation["fields"]
        subject_claims = tuple(
            _claim_number(endpoint.fragment_id)
            for endpoint in relation["subjects"])
        evidence_by_document = {
            endpoint.document_id: endpoint
            for endpoint in relation["evidence"]
            if endpoint.document_id.startswith("us-prior-art-")
        }

        axes = []
        na_axes = tuple(
            (name, int(match.group(1)))
            for name in fields
            if (match := re.fullmatch(r"na-([1-9][0-9]*)-[a-z0-9-]+", name)))
        if na_axes:
            document_id = _primary_document(fields, "document")
            axes.extend((field, claim_number, (document_id,))
                        for field, claim_number in na_axes)
        integrated_fields = tuple(
            name for name in (
                "production-individualized-variation",
                "delivery-association", "suspect-recovery")
            if name in fields)
        if integrated_fields:
            if subject_claims != (1,):
                raise ModelError("integrated matrix inventory subject is not exact")
            document_id = _primary_document(fields, "id-document")
            axes.extend((field, 1, (document_id,))
                        for field in integrated_fields)
        if "score" in fields:
            if len(subject_claims) != 1:
                raise ModelError("scored matrix inventory subject is not exact")
            document_id = _primary_document(fields, "document")
            axes.append(("score", subject_claims[0], (document_id,)))
        for field in ("claimed-relationship", "claimed-operation"):
            if field in fields:
                if len(subject_claims) != 1 or not evidence_by_document:
                    raise ModelError("matrix relationship obligation is not exact")
                axes.append((field, subject_claims[0],
                             tuple(sorted(evidence_by_document))))
        for field in ("na-claims", "af-claims"):
            if field in fields and evidence_by_document:
                claim_numbers = _claim_numbers(fields[field])
                if not claim_numbers:
                    raise ModelError("dependent matrix claim census is not exact")
                axes.extend((field, claim_number,
                             tuple(sorted(evidence_by_document)))
                            for claim_number in claim_numbers)

        for field, claim_number, document_ids in axes:
            value = fields[field]
            for document_id in document_ids:
                endpoint = evidence_by_document.get(document_id)
                if endpoint is None:
                    raise ModelError("matrix obligation document endpoint is absent")
                key = (relation_id, field, claim_number, document_id)
                if key in expected:
                    raise ModelError("matrix obligation is duplicated")
                expected[key] = (value, endpoint)
    return expected


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
        matrix_relations = {}
        scope_ids = set()
        for relation in comparison_root.findall(SR + "relation"):
            relation_id = relation.get("relationId")
            if not relation_id or relation_id in matrix_relations:
                raise ModelError("comparison-matrix relation identity is not exact")
            endpoint_elements = tuple(relation.findall(SR + "endpoint"))
            subjects = tuple(_endpoint(item) for item in endpoint_elements
                             if item.get("role") == "subject")
            evidence = tuple(_endpoint(item) for item in endpoint_elements
                             if item.get("role") == "evidence")
            fields = _fields(relation)
            if not subjects or not fields:
                raise ModelError("comparison-matrix relation is incomplete")
            matrix_relations[relation_id] = {
                "subjects": subjects, "evidence": evidence, "fields": fields}
            scope_ids.update(
                endpoint.document_id for endpoint in evidence
                if endpoint.document_id.startswith("us-prior-art-"))
        scope_ids = sorted(scope_ids)
        if len(scope_ids) != self._expected_document_census:
            raise ModelError("prior-art comparison document census is stale")
        if set(target_surfaces) != set(scope_ids):
            raise ModelError(
                "prior-art XML handoffs do not close the complete matrix scope")
        self.prior_art_scope = tuple(PriorArtScopeDocument(
            document_id=item, label=item.removeprefix("us-prior-art-").upper())
            for item in scope_ids)
        self.prior_art_readers = tuple(PriorArtReaderDocument(
            document_id=document_id,
            label=document_id.removeprefix("us-prior-art-").upper(),
            title=target_surfaces[document_id].document.title,
            content=target_surfaces[document_id].document_item.typed_content,
        ) for document_id in scope_ids)
        self._target_surfaces = MappingProxyType(dict(target_surfaces))

        obligations = {}
        raw_candidates = []
        raw_allocations = []
        expected_obligations = _matrix_obligations(matrix_relations)
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
            if subject.document_id != claim_document.document_id:
                raise ModelError("prior-art map subject document is not exact")
            kind = fields.get("record-kind")
            if kind == "obligation":
                if set(fields) != {
                        "matrix-field", "matrix-relation-id",
                        "obligation-status", "record-kind"} or len(evidence) != 1:
                    raise ModelError("prior-art obligation relation is malformed")
                claim_number = _claim_number(subject.fragment_id)
                claim = self.claims_by_number.get(claim_number)
                if claim is None or claim.content_digest != subject.content_digest:
                    raise ModelError("prior-art obligation claim does not resolve exactly")
                matrix_relation_id = fields["matrix-relation-id"]
                matrix_field = fields["matrix-field"]
                matrix_relation = matrix_relations.get(matrix_relation_id)
                if matrix_relation is None or matrix_field not in matrix_relation["fields"]:
                    raise ModelError("prior-art obligation matrix owner does not resolve")
                evidence_endpoint = evidence[0]
                key = (matrix_relation_id, matrix_field, claim_number,
                       evidence_endpoint.document_id)
                expected = expected_obligations.get(key)
                if expected is None or expected[1] != evidence_endpoint:
                    raise ModelError("prior-art obligation is not matrix-exact")
                status = fields["obligation-status"]
                expected_status = ("reviewed-no-material-passage"
                                   if expected[0].strip() == "—" else None)
                if status not in {
                        "passage-mapped", "counsel-review-required",
                        "reviewed-no-material-passage"} or \
                        (expected_status is not None) != \
                        (status == "reviewed-no-material-passage") or \
                        relation_id in obligations:
                    raise ModelError("prior-art obligation status is not exact")
                obligations[relation_id] = PriorArtObligation(
                    relation_id=relation_id,
                    matrix_relation_id=matrix_relation_id,
                    matrix_field=matrix_field,
                    matrix_value=expected[0], status=status,
                    subject=subject, evidence=evidence_endpoint,
                    claim_number=claim_number)
            elif kind == "candidate":
                allowed = {"candidate-role", "proposition", "record-kind",
                           "subject-exact-text", "obligation-ids"}
                if not set(fields).issubset(allowed) or \
                        not {"candidate-role", "obligation-ids", "proposition",
                             "record-kind"}.issubset(fields) or \
                        fields["candidate-role"] not in {"specific", "context", "combination"} or \
                        not evidence:
                    raise ModelError("prior-art candidate relation is malformed")
                unit = self.units_by_fragment.get(subject.fragment_id)
                if unit is None or unit.content_digest != subject.content_digest:
                    raise ModelError("prior-art candidate subject does not resolve exactly")
                obligation_ids = tuple(fields["obligation-ids"].split(" "))
                if not obligation_ids or obligation_ids != tuple(
                        sorted(set(obligation_ids))):
                    raise ModelError("candidate obligation identities are not exact")
                raw_candidates.append((
                    relation_id, subject, unit, fields, evidence, obligation_ids))
            elif kind == "fragment-review-allocation":
                if set(fields) != {
                        "obligation-ids", "record-kind", "relevance-note"} or \
                        evidence:
                    raise ModelError(
                        "prior-art fragment-review allocation is malformed")
                unit = self.units_by_fragment.get(subject.fragment_id)
                if unit is None or unit.content_digest != subject.content_digest:
                    raise ModelError(
                        "fragment-review allocation subject does not resolve exactly")
                obligation_ids = tuple(fields["obligation-ids"].split(" "))
                if not obligation_ids or obligation_ids != tuple(
                        sorted(set(obligation_ids))):
                    raise ModelError(
                        "fragment-review allocation identities are not exact")
                raw_allocations.append((
                    relation_id, subject, unit, fields, obligation_ids))
            else:
                raise ModelError("prior-art relation record kind is unsupported")

        actual_obligations = {
            (item.matrix_relation_id, item.matrix_field, item.claim_number,
             item.evidence.document_id): item
            for item in obligations.values()}
        if set(actual_obligations) != set(expected_obligations) or \
                len(actual_obligations) != len(obligations):
            raise ModelError("matrix claim/document obligation coverage is incomplete")

        passage_values = {}
        phrase_values = []
        candidate_values = []
        allocation_values = []
        referenced_obligations = set()
        candidate_signatures = set()
        for (relation_id, subject, unit, fields, evidence,
             obligation_ids) in raw_candidates:
            selected_obligations = tuple(
                obligations.get(identifier) for identifier in obligation_ids)
            if any(item is None for item in selected_obligations):
                raise ModelError("candidate obligation identity does not resolve")
            claim_number = unit.claim_number
            obligation_documents = {
                item.evidence.document_id for item in selected_obligations}
            evidence_documents = {endpoint.document_id for endpoint in evidence}
            if obligation_documents != evidence_documents or any(
                    item.claim_number != claim_number or
                    item.status != "passage-mapped"
                    for item in selected_obligations):
                raise ModelError("candidate does not close its exact obligations")
            evidence_signature = tuple(
                (endpoint.document_id, endpoint.fragment_id,
                 endpoint.content_digest) for endpoint in evidence)
            if len(evidence_signature) != len(set(evidence_signature)):
                raise ModelError("candidate repeats an exact passage endpoint")
            exact = fields.get("subject-exact-text")
            signature = _candidate_semantic_signature(
                subject, exact, fields["candidate-role"], obligation_ids,
                evidence)
            _record_unique_signature(
                candidate_signatures, signature, "candidate")
            _validate_preamble_candidate(
                unit, fields["candidate-role"], obligation_ids,
                evidence_documents)
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
            referenced_obligations.update(obligation_ids)
            target = Target(
                role=fields["candidate-role"], endpoints=evidence,
                note=fields["proposition"], caution=None)
            if exact is None:
                candidate_values.append(PriorArtCandidate(
                    relation_id=relation_id, subject=subject,
                    exact_text=None, obligation_ids=obligation_ids,
                    targets=(target,)))
            else:
                start, end = _unique_span(unit.text, exact)
                candidate = PhraseMapping(
                    relation_id=relation_id, parent=subject,
                    unit_kind=unit.unit_kind, unit_index=unit.unit_index,
                    exact_text=exact, start=start, end=end,
                    targets=(target,))
                phrase_values.append(candidate)
                candidate_values.append(PriorArtCandidate(
                    relation_id=relation_id, subject=subject,
                    exact_text=exact, obligation_ids=obligation_ids,
                    targets=(target,)))

        allocation_signatures = set()
        for (relation_id, subject, unit, fields,
             obligation_ids) in raw_allocations:
            selected_obligations = tuple(
                obligations.get(identifier) for identifier in obligation_ids)
            _validate_review_allocation(unit, selected_obligations)
            signature = _allocation_semantic_signature(
                subject, obligation_ids)
            _record_unique_signature(
                allocation_signatures, signature,
                "fragment-review allocation")
            allocation_values.append(PriorArtReviewAllocation(
                relation_id=relation_id, subject=subject,
                obligation_ids=obligation_ids,
                relevance_note=fields["relevance-note"]))

        _validate_candidate_obligation_coverage(
            obligations.values(), referenced_obligations)

        exact_candidate_units = {
            item.subject.fragment_id for item in candidate_values
            if item.exact_text is None}
        mappings = []
        for unit_id, unit in self.units_by_fragment.items():
            has_candidates = unit_id in exact_candidate_units
            mappings.append(Mapping(
                relation_id=(config["passageMapPackageId"] +
                             "-computed-unit-" + unit_id),
                status=("mapped" if has_candidates else
                        "counsel-review-required"),
                subject=Endpoint(
                    document_id=claim_document.document_id,
                    fragment_id=unit.fragment_id,
                    content_digest=unit.content_digest),
                unit_kind=unit.unit_kind, unit_index=unit.unit_index,
                caution=None, targets=()))
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
        self.prior_art_obligations = tuple(
            obligations[key] for key in sorted(obligations))
        obligation_values = {}
        for item in self.prior_art_obligations:
            obligation_values.setdefault(item.claim_number, []).append(item)
        self.obligations_by_claim = MappingProxyType({
            key: tuple(value) for key, value in sorted(obligation_values.items())})
        self.candidate_relations = tuple(candidate_values)
        self.review_allocations = tuple(allocation_values)
        self.candidates_by_unit = self._index_candidates(
            self.candidate_relations, exact_text=False)
        self.phrase_candidates_by_unit = self._index_candidates(
            self.candidate_relations, exact_text=True)
        self.candidates_by_id = MappingProxyType({
            item.relation_id: item for item in self.candidate_relations})
        self.review_allocations_by_unit = self._index_by_unit(
            self.review_allocations)
        self._relations_by_id = MappingProxyType({
            item.relation_id: item for item in
            (*self.relations.mappings, *self.prior_art_obligations,
             *self.review_allocations, *self.candidate_relations)})
        self.reverse_index = self._candidate_reverse_index(
            self.candidate_relations)
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

    @staticmethod
    def _index_candidates(items, *, exact_text):
        values = {}
        for item in items:
            if (item.exact_text is not None) != exact_text:
                continue
            values.setdefault(item.subject.fragment_id, []).append(item)
        return MappingProxyType({
            key: tuple(value) for key, value in sorted(values.items())})

    @staticmethod
    def _candidate_reverse_index(items):
        values = {}
        for candidate in items:
            for target in candidate.targets:
                for endpoint in target.endpoints:
                    values.setdefault(
                        (endpoint.document_id, endpoint.fragment_id), []).append(
                            candidate)
        return MappingProxyType({
            key: tuple(value) for key, value in sorted(values.items())})

    def _endpoint_relation_index(self):
        values = {}
        for relation in self.relations.mappings:
            subject = relation.subject
            values.setdefault((subject.document_id, subject.fragment_id), []).append(relation)
        for relation in self.prior_art_obligations:
            values.setdefault(
                (relation.subject.document_id, relation.subject.fragment_id),
                []).append(relation)
            values.setdefault(
                (relation.evidence.document_id, relation.evidence.fragment_id),
                []).append(relation)
        for relation in self.candidate_relations:
            subject = relation.subject
            values.setdefault((subject.document_id, subject.fragment_id), []).append(relation)
            for target in relation.targets:
                for endpoint in target.endpoints:
                    values.setdefault((endpoint.document_id, endpoint.fragment_id), []).append(relation)
        for relation in self.review_allocations:
            subject = relation.subject
            values.setdefault(
                (subject.document_id, subject.fragment_id), []).append(relation)
        return MappingProxyType({key: tuple(value)
                                 for key, value in sorted(values.items())})

    @property
    def read_inventory(self):
        return self._read_inventory

    @property
    def content_lock(self):
        return self._content_lock

    def _origin_value(self, origin_ref):
        if origin_ref.startswith("wording."):
            return _wording_origin_value(self._wording, origin_ref)
        values = {
            "edition.claimSetVersion": self.claim_set_version,
            "edition.declaredReleaseTimestamp": self.declared_release_timestamp,
            "edition.claimCount": len(self.claims),
            "edition.unitCount": len(self.units_by_fragment),
            "edition.strategyName": self.strategy_name,
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
            surface = self._target_surfaces.get(document_id)
            try:
                value = surface.item(fragment_id) if surface is not None else None
            except Exception as exc:
                raise ModelError("source item does not resolve") from exc
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
