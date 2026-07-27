"""Computed validation for the current handoff-backed navigator model.

Construction proves syntax, XSD conformance, registered-source identity, and
endpoint currency.  This module checks the remaining cross-document semantic
invariants without introducing a second evidence, approval, or lineage plane.
"""

from __future__ import annotations

import re

from . import canon, depgraph, projections
from .gateway import GatewayError
from .model import ModelError


_C1_DIGEST = re.compile(r"sha256/c1:[0-9a-f]{64}\Z")
_XML_RAW_DIGEST = re.compile(r"sha256/raw:[0-9a-f]{64}\Z")
_BASE_WORDING = frozenset({
    "artifact-label-technical-preview",
    "artifact-watermark-technical-preview",
    "authority-pct-as-filed",
    "bundle-manifest-neutral",
    "claim-set-guidance",
    "counsel-legend",
    "editorial-not-filed",
    "gate-disposition-carried-at-required-scope",
    "source-input-provenance",
    "provenance-summary",
    "standing-disclaimer",
    "caution-scope-claim",
    "caution-scope-fragment",
    "caution-scope-target",
})


def _metadata(model, error):
    if re.fullmatch(r"[a-z][a-z0-9-]{0,31}", model.edition_id or "") is None:
        error("metadata", "edition identity is not current")
    if model.strategy_prefix.casefold() != model.edition_id:
        error("metadata", "strategy prefix and edition identity differ")
    version_prefix = model.strategy_prefix + "-"
    if not model.claim_set_version.startswith(version_prefix):
        error("metadata", "claim-set version is not bound to the edition")
    if not model.artifact_name.endswith(
            "_%s.html" % model.claim_set_version):
        error("metadata", "artifact name is not bound to the claim-set version")
    if model.relation_set_id != model.edition_id + "-pct":
        error("metadata", "relation-set identity is not bound to the edition")
    if model.profile_label != model.controlled_text(
            "artifact-label-technical-preview"):
        error("metadata", "product profile does not resolve from controlled wording")
    if _C1_DIGEST.fullmatch(model.shared_wording_digest) is None:
        error("metadata", "shared wording digest is malformed")


def _sources(model, error):
    documents = model.source_documents
    if len(documents) != 2 or len({item.document_id for item in documents}) != 2:
        error("sources", "source-document inventory is not exactly claim plus PCT")
        return
    claim, pct = documents
    expected = (
        (claim, "authored-markdown-v1", "generated-xml"),
        (pct, "pdf-evidence-transcription-v1", "transcription-xml"),
    )
    for document, scheme, role in expected:
        if document.authority_scheme != scheme or document.xml_role != role:
            error("sources", "%s has the wrong authority direction or XML role" %
                  document.document_id)
        if not document.registered_path.endswith(".source.xml"):
            error("sources", "%s is not resolved through registered XML" %
                  document.document_id)
        if _XML_RAW_DIGEST.fullmatch(document.xml_raw_digest) is None:
            error("sources", "%s has a malformed XML raw digest" %
                  document.document_id)
        if model.get_document(document.document_id) != document:
            error("sources", "%s does not round-trip through the typed lookup" %
                  document.document_id)
        metadata = model.get_metadata(document.document_id)
        if set(metadata) != {
                "documentId", "authorityScheme", "xmlRole",
                "xmlRawDigest", "registeredPath"}:
            error("sources", "%s metadata projection is not closed" %
                  document.document_id)


def _claims(model, error):
    expected_claims = model._expected_census["claims"]
    expected_units = model._expected_census["units"]
    numbers = tuple(claim.number for claim in model.claims)
    if numbers != tuple(range(1, expected_claims + 1)):
        error("census", "claim numbers are not exactly contiguous 1..%d" %
              expected_claims)
    if len(model.claims) != expected_claims:
        error("census", "parsed claim count differs from the edition control")
    if len(model.units_by_fragment) != expected_units or \
            sum(len(claim.units) for claim in model.claims) != expected_units:
        error("census", "parsed claim-unit count differs from the edition control")
    group_names = tuple(name for name, _numbers in model.claim_groups)
    if group_names != model._expected_groups:
        error("census", "claim group order differs from the edition control")
    grouped = tuple(number for _name, group in model.claim_groups for number in group)
    if grouped != numbers:
        error("census", "claim groups do not partition the claim inventory")

    fragment_ids = []
    for claim in model.claims:
        if not claim.units:
            error("claims", "claim %d has no typed claim unit" % claim.number)
        preambles = [unit for unit in claim.units if unit.unit_kind == "preamble"]
        limitations = [unit for unit in claim.units
                       if unit.unit_kind == "limitation"]
        if len(preambles) > 1 or any(unit.unit_index != 0 for unit in preambles) or \
                [unit.unit_index for unit in limitations] != \
                list(range(1, len(limitations) + 1)):
            error("claims", "claim %d unit indices are not contiguous" %
                  claim.number)
        for unit in claim.units:
            fragment_ids.append(unit.fragment_id)
            if unit.claim_number != claim.number or \
                    unit.content_digest != model._source_items[
                        unit.fragment_id].content_digest:
                error("claims", "%s is not bound to its authored XML fragment" %
                      unit.fragment_id)
    if len(fragment_ids) != len(set(fragment_ids)) or \
            set(fragment_ids) != set(model.units_by_fragment):
        error("claims", "claim-unit identities are not one exact inventory")

    rebuilt = depgraph.build(model.claims, model.independent_claims)
    for name in ("parents", "children", "aggregate_hashes", "chain_hashes"):
        if dict(getattr(model, name)) != dict(getattr(rebuilt, name)):
            error("dependencies", "%s is not the computed dependency projection" %
                  name)


def _disclosure(model, error):
    if not model.disclosure_blocks or not model.disclosure_index:
        error("disclosure", "PCT filed-text render boundary is empty")
    expected_assets = {"asset-fig-%d-png" % number for number in range(1, 5)}
    if set(model.assets) != expected_assets:
        error("disclosure", "PCT asset inventory is not exactly figures 1..4")
    for asset_id, asset in model.assets.items():
        if asset.asset_id != asset_id:
            error("disclosure", "%s has a mismatched typed identity" % asset_id)
        if asset.media_type != "image/png" or \
                not asset.path.endswith("/Fig-%s.png" % asset_id.split("-")[2]):
            error("disclosure", "%s has a stale media type or path" % asset_id)
        # Structured-source raw digests use the same bytes but a distinct
        # authority prefix. Compare the hexadecimal payload exactly.
        if asset.raw_digest.rsplit(":", 1)[-1] != \
                canon.bytes_digest(asset.data).rsplit(":", 1)[-1]:
            error("disclosure", "%s bytes do not match its registered digest" %
                  asset_id)
    if len(model._editorial_ids) != 6 or \
            not model._editorial_ids.issubset(model.disclosure_index):
        error("disclosure", "PCT editorial inventory is not exactly note, captions, footer")
    for fragment_id, node in model.disclosure_index.items():
        if node.fragment_id != fragment_id or not node.content_digest:
            error("disclosure", "%s is not a typed addressable PCT node" %
                  fragment_id)
        if fragment_id in model._editorial_ids and not node.editorial:
            error("disclosure", "%s lost its explicit editorial status" % fragment_id)


def _source_gate(caution):
    return caution is not None and caution.kind == "source-gate"


def _relations(model, error):
    relation_set = model.relations
    gate_by_id = {gate.gate_id: gate for gate in relation_set.gate_definitions}
    if len(gate_by_id) != len(relation_set.gate_definitions) or \
            len({gate.code for gate in relation_set.gate_definitions}) != len(gate_by_id):
        error("relations", "gate identities and codes are not unique")
    if any(gate.required_scope not in {"claim", "fragment", "target"}
           for gate in gate_by_id.values()):
        error("relations", "gate required scope is outside the closed vocabulary")

    mapping_units = []
    relation_ids = set()
    carries = set()
    for mapping in relation_set.mappings:
        if mapping.relation_id in relation_ids:
            error("relations", "relation identity is duplicated: %s" %
                  mapping.relation_id)
        relation_ids.add(mapping.relation_id)
        mapping_units.append(mapping.subject.fragment_id)
        unit = model.units_by_fragment.get(mapping.subject.fragment_id)
        if unit is None or mapping.unit_kind != unit.unit_kind or \
                mapping.unit_index != unit.unit_index:
            error("relations", "%s has a stale typed subject" % mapping.relation_id)
        if (mapping.status == "mapped") != bool(mapping.targets):
            error("relations", "%s status and target presence disagree" %
                  mapping.relation_id)
        if mapping.status not in {"mapped", "counsel-review-required"}:
            error("relations", "%s has an unknown mapping status" %
                  mapping.relation_id)
        if mapping.caution is not None:
            if not _source_gate(mapping.caution) or \
                    mapping.caution.gate_id not in gate_by_id or \
                    gate_by_id[mapping.caution.gate_id].required_scope != "fragment":
                error("relations", "%s has an invalid fragment gate caution" %
                      mapping.relation_id)
            else:
                carries.add((mapping.caution.gate_id,
                             mapping.subject.fragment_id, "fragment"))
        relation_target_fragments = []
        for target in mapping.targets:
            if len(target.endpoints) != len({endpoint.fragment_id
                                             for endpoint in target.endpoints}):
                error("relations", "%s repeats a target endpoint" %
                      mapping.relation_id)
            relation_target_fragments.extend(
                endpoint.fragment_id for endpoint in target.endpoints)
            if target.caution is not None:
                if _source_gate(target.caution):
                    gate = gate_by_id.get(target.caution.gate_id)
                    if gate is None or gate.required_scope != "target":
                        error("relations", "%s has an invalid target gate caution" %
                              mapping.relation_id)
                    else:
                        carries.add((target.caution.gate_id,
                                     mapping.subject.fragment_id, "target"))
                elif target.caution.kind != "generalization-note" or \
                        target.caution.code != "beyond-literal-example":
                    error("relations", "%s has an invalid generalization caution" %
                          mapping.relation_id)
        if len(relation_target_fragments) != len(set(relation_target_fragments)):
            error("relations", "%s repeats an endpoint across candidate targets" %
                  mapping.relation_id)

    if len(mapping_units) != len(set(mapping_units)) or \
            set(mapping_units) != set(model.units_by_fragment):
        error("coverage", "claim units do not have exactly one mapping each")

    spans = {}
    for phrase in relation_set.phrase_mappings:
        if phrase.relation_id in relation_ids:
            error("relations", "relation identity is duplicated: %s" %
                  phrase.relation_id)
        relation_ids.add(phrase.relation_id)
        unit = model.units_by_fragment.get(phrase.parent.fragment_id)
        span = (phrase.start, phrase.end)
        if unit is None or unit.text[phrase.start:phrase.end] != phrase.exact_text or \
                phrase.start < 0 or phrase.end <= phrase.start:
            error("relations", "%s selector is not an exact contiguous unit span" %
                  phrase.relation_id)
        prior = spans.setdefault(phrase.parent.fragment_id, [])
        if any(span[0] < other[1] and other[0] < span[1]
               for other in prior):
            error("relations", "%s overlaps a resolved phrase span" %
                  phrase.relation_id)
        prior.append(span)
        if not phrase.targets:
            error("relations", "%s has no target" % phrase.relation_id)
        relation_target_fragments = []
        for target in phrase.targets:
            if len(target.endpoints) != len({endpoint.fragment_id
                                             for endpoint in target.endpoints}):
                error("relations", "%s repeats a target endpoint" %
                      phrase.relation_id)
            relation_target_fragments.extend(
                endpoint.fragment_id for endpoint in target.endpoints)
            if target.caution is not None:
                if _source_gate(target.caution):
                    gate = gate_by_id.get(target.caution.gate_id)
                    if gate is None or gate.required_scope != "target":
                        error("relations", "%s has an invalid target gate caution" %
                              phrase.relation_id)
                    else:
                        carries.add((target.caution.gate_id,
                                     phrase.parent.fragment_id, "target"))
                elif target.caution.kind != "generalization-note" or \
                        target.caution.code != "beyond-literal-example":
                    error("relations", "%s has an invalid generalization caution" %
                          phrase.relation_id)
        if len(relation_target_fragments) != len(set(relation_target_fragments)):
            error("relations", "%s repeats an endpoint across candidate targets" %
                  phrase.relation_id)

    disposition_keys = set()
    disposition_gates = set()
    for disposition in relation_set.dispositions:
        gate = gate_by_id.get(disposition.gate_id)
        key = (disposition.gate_id, disposition.subject.fragment_id)
        if key in disposition_keys:
            error("dispositions", "gate/subject disposition is duplicated")
        disposition_keys.add(key)
        disposition_gates.add(disposition.gate_id)
        if gate is None:
            error("dispositions", "%s references an unknown gate" %
                  disposition.disposition_id)
            continue
        expected_kind = "claim" if gate.required_scope == "claim" else "claim-unit"
        if disposition.subject_kind != expected_kind:
            error("dispositions", "%s is recorded at the wrong subject kind" %
                  disposition.disposition_id)
        carry_key = (gate.gate_id, disposition.subject.fragment_id,
                     gate.required_scope)
        if disposition.value != "carried-at-required-scope":
            error("dispositions", "%s has a non-current disposition" %
                  disposition.disposition_id)
        elif gate.required_scope != "claim" and carry_key not in carries:
            error("dispositions", "%s has no gate caution at its required scope" %
                  disposition.disposition_id)
    if disposition_gates != set(gate_by_id):
        error("dispositions", "every gate must have a current disposition")
    for gate_id, fragment_id, _scope in carries:
        if (gate_id, fragment_id) not in disposition_keys:
            error("dispositions", "%s on %s has no matching disposition" %
                  (gate_id, fragment_id))

    rebuilt = projections.reverse_index(relation_set, model.units_by_fragment)
    if dict(rebuilt) != dict(model.reverse_index):
        error("coverage", "reverse index is not the computed relation projection")


def _wording(model, error):
    expected = set(_BASE_WORDING)
    expected.update("mapping-status-%s" % item.status
                    for item in model.relations.mappings)
    all_targets = [target for item in model.relations.mappings
                   for target in item.targets]
    all_targets.extend(target for item in model.relations.phrase_mappings
                       for target in item.targets)
    expected.update("mapping-role-%s" % target.role for target in all_targets)
    expected.update("gate-disposition-%s" % item.value
                    for item in model.relations.dispositions)
    expected.update("gate-label-%s-%s" % (model.edition_id, gate.code)
                    for gate in model.relations.gate_definitions)
    cautions = [item.caution for item in model.relations.mappings
                if item.caution is not None]
    cautions.extend(target.caution for target in all_targets
                    if target.caution is not None)
    expected.update("caution-type-%s" % item.kind for item in cautions)
    expected.update("generalization-%s" % item.code for item in cautions
                    if item.kind == "generalization-note")
    expected.update("caution-scope-%s" % gate.required_scope
                    for gate in model.relations.gate_definitions)
    if set(model._wording) != expected:
        missing = sorted(expected - set(model._wording))
        unused = sorted(set(model._wording) - expected)
        error("wording", "controlled wording has missing %r or unused %r entries" %
              (missing, unused))

    for wording_id, entry in model._wording.items():
        if not entry.slots:
            value = model.controlled_text(wording_id)
            if not value or value != value.strip():
                error("wording", "%s does not resolve to exact nonblank text" %
                      wording_id)
    model.controlled_text("standing-disclaimer")
    model.controlled_text("provenance-summary")


def _origins(model, error):
    expected_paths = {
        model._edition_path,
        "navigator/schema/edition.schema.json",
        model._relation_path,
        "navigator/schema/navigator-relations.xsd",
        "navigator/wording/shared.wording.xml",
        model._edition_wording_path,
        "navigator/schema/wording.xsd",
    }
    expected_paths.update(model._handoff_validation_paths)
    reads = dict(model.read_inventory)
    if set(reads) != expected_paths:
        error("origins", "gateway reads are not the exact computed input closure")
    forbidden = [path for path in reads
                 if path.startswith(("navigator/dist/", "navigator/records/"))]
    if forbidden:
        error("origins", "semantic model read forbidden source or derived paths: %r" %
              sorted(forbidden))
    if any(_C1_DIGEST.fullmatch(digest) is None for digest in reads.values()):
        error("origins", "gateway read inventory contains a malformed byte digest")
    rebuilt = projections.origin_inventory(model)
    if rebuilt != model.origin_inventory:
        error("origins", "substantive origin inventory is not the computed projection")
    lock = model.content_lock
    lock_reads = {item.path: item.digest for item in lock.reads}
    if lock_reads != reads or \
            _C1_DIGEST.fullmatch(lock.lock_digest) is None or \
            lock.canon_version != canon.CANON_VERSION:
        error("origins", "gateway lock does not bind the exact read inventory")


def validate_edition(model):
    """Return an immutable, deterministic tuple of ``(code, message)`` defects."""
    errors = []

    def error(code, message):
        errors.append((str(code), str(message)))

    for code, check in (
            ("metadata", _metadata),
            ("sources", _sources),
            ("claims", _claims),
            ("disclosure", _disclosure),
            ("relations", _relations),
            ("wording", _wording),
            ("origins", _origins)):
        try:
            check(model, error)
        except (AttributeError, KeyError, TypeError, ValueError,
                GatewayError, ModelError, RuntimeError) as exc:
            error(code, "validation could not prove the current invariant: %s" % exc)
    return tuple(sorted(set(errors)))
