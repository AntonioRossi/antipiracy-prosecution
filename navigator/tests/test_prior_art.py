"""Focused executable contract for the current claims-to-prior-art products."""

from collections import Counter
from dataclasses import replace
import html
import json
from pathlib import Path
import re
from types import MappingProxyType
import unittest

from navigator.lib import browserqa, bundlezip, canon, currentstate, render, snapshot
from navigator.lib.model import Endpoint, ModelError
from navigator.lib.priorart import (
    PriorArtModel, PriorArtReviewAllocation,
    _allocation_semantic_signature, _candidate_semantic_signature,
    _record_unique_signature, _validate_candidate_obligation_coverage,
    _validate_preamble_candidate,
    _validate_review_allocation,
)
from navigator.lib.validate import validate_prior_art
from navigator.lib.registry import ConsumerInput
from navigator.tests import validation_session
from structured_source import parser
from structured_source.canonical import raw_digest
from structured_source.control import parse_json
from structured_source.errors import ParseError


ROOT = Path(__file__).resolve().parents[2]
TARGET_PACKAGES = {
    *("us-prior-art-a%d" % number for number in range(1, 22)),
    *("us-prior-art-b%d" % number for number in range(1, 11)),
    "us-prior-art-c3", "us-prior-art-c8",
}


def _navigation(text):
    match = re.search(
        r'<script type="application/json" id="nav-data"[^>]*>(.*?)</script>',
        text, re.DOTALL)
    if match is None:
        raise AssertionError("rendered prior-art product has no navigation data")
    return json.loads(match.group(1))


def _relation_chunk(payload, relation_id):
    pattern = (
        rb"  <relation [^\n]*relationId=\"" +
        re.escape(relation_id.encode("utf-8")) +
        rb"\".*?  </relation>\n")
    match = re.search(pattern, payload, re.DOTALL)
    if match is None:
        raise AssertionError("current-profile relation vector owner is absent")
    return match.group(0)


def _snapshot_with_bytes(base, path, payload):
    retained = dict(base.retained_bytes)
    retained[path] = payload
    entries = []
    for entry in base.entries:
        if entry.path == path:
            entry = snapshot.SnapshotEntry(
                path, canon.bytes_digest(payload), entry.mode, len(payload),
                entry.fingerprint)
        entries.append(entry)
    digest = canon.composite_digest(
        "aa11393:lock:c1",
        {"repositorySnapshot": [entry.as_record() for entry in entries]})
    return snapshot.RepositorySnapshot(
        base.root, tuple(entries), digest, MappingProxyType(retained))


def _model_from_map_payload(session, payload):
    edition = session["plan"].by_id["na-prior-art"]
    consumer = session["sources"].consumer_inputs[edition.consumer_id]
    package_id = edition.passage_map_package_id
    handoff = consumer.handoffs[package_id]
    path = handoff["path"]
    parser.parse_artifact(
        payload, "relation-set", controls=consumer.parser_controls)
    vector_snapshot = _snapshot_with_bytes(session["snapshot"], path, payload)
    handoffs = dict(consumer.handoffs)
    vector_handoff = dict(handoff)
    vector_handoff["bytes"] = payload
    vector_handoff["validationReads"] = tuple(
        (read_path, raw_digest(payload) if read_path == path else digest)
        for read_path, digest in handoff["validationReads"])
    handoffs[package_id] = MappingProxyType(vector_handoff)
    vector_consumer = ConsumerInput(
        consumer_id=consumer.consumer_id,
        snapshot_digest=vector_snapshot.digest,
        capture_token=vector_snapshot.capture_token,
        handoffs=MappingProxyType(handoffs),
        parser_controls=consumer.parser_controls)
    vector_edition = replace(
        edition, capture_token=vector_snapshot.capture_token,
        plan_token=object())
    return currentstate.build_model(
        vector_edition, vector_snapshot, vector_consumer, object())


def _current_profile_vector(session):
    """Build the multiplicity vector through XML, parser, handoff, and model."""
    base_model = session["models"]["na-prior-art"]
    edition = session["plan"].by_id["na-prior-art"]
    consumer = session["sources"].consumer_inputs[edition.consumer_id]
    package_id = edition.passage_map_package_id
    handoff = consumer.handoffs[package_id]
    path = handoff["path"]
    payload = handoff["bytes"]

    base_candidate = next(
        item for item in base_model.candidate_relations
        if item.exact_text is None and len(item.targets[0].endpoints) > 1)
    alternate_role = (
        "context" if base_candidate.targets[0].role != "context" else "specific")
    candidate_id = package_id + "-candidate-browser-vector"
    candidate = _relation_chunk(payload, base_candidate.relation_id)
    candidate = candidate.replace(
        base_candidate.relation_id.encode("utf-8"),
        candidate_id.encode("utf-8"))
    old_role = (
        '<assertionField name="candidate-role">%s</assertionField>' %
        base_candidate.targets[0].role).encode("utf-8")
    new_role = (
        '<assertionField name="candidate-role">%s</assertionField>' %
        alternate_role).encode("utf-8")
    if candidate.count(old_role) != 1:
        raise AssertionError("candidate-role vector owner is not exact")
    candidate = candidate.replace(old_role, new_role)

    review = next(
        item for item in base_model.prior_art_obligations
        if item.status == "counsel-review-required")
    allocation_unit = next(
        unit for unit in base_model.units_by_fragment.values()
        if unit.claim_number == review.claim_number and
        unit.fragment_id not in base_model.candidates_by_unit)
    allocation_id = package_id + "-allocation-browser-vector"
    allocation_note = "Exact current-profile browser-vector allocation."
    allocation = (
        '  <relation direction="forward" relationId="{identifier}" '
        'semanticOwner="Applicant — Antonio Rossi" '
        'type="claim-prior-art-passage-map" xml:id="{identifier}">\n'
        '    <endpoint documentId="{document}" '
        'fragmentContentDigest="{digest}" fragmentId="{fragment}" '
        'role="subject" />\n'
        '    <assertionField name="obligation-ids">{obligation}</assertionField>\n'
        '    <assertionField name="record-kind">fragment-review-allocation</assertionField>\n'
        '    <assertionField name="relevance-note">{note}</assertionField>\n'
        '  </relation>\n'
    ).format(
        identifier=allocation_id,
        document=base_model._claim_package_id,
        digest=allocation_unit.content_digest,
        fragment=allocation_unit.fragment_id,
        obligation=review.relation_id,
        note=allocation_note,
    ).encode("utf-8")
    closing = b"</relations>\n"
    if payload.count(closing) != 1:
        raise AssertionError("current-profile relation closure is not exact")
    vector_payload = payload.replace(
        closing, candidate + allocation + closing)

    vector_model = _model_from_map_payload(session, vector_payload)
    if validate_prior_art(vector_model):
        raise AssertionError("current-profile browser vector is not model-valid")
    unresolved = next(
        unit.fragment_id for unit in vector_model.units_by_fragment.values()
        if unit.fragment_id not in vector_model.candidates_by_unit and
        unit.fragment_id not in vector_model.review_allocations_by_unit)
    return MappingProxyType({
        "allocationId": allocation_id,
        "allocationUnit": allocation_unit.fragment_id,
        "baseCandidateId": base_candidate.relation_id,
        "baseCandidateRole": base_candidate.targets[0].role,
        "candidateId": candidate_id,
        "candidateUnit": base_candidate.subject.fragment_id,
        "model": vector_model,
        "unresolvedUnit": unresolved,
        "xml": vector_payload,
    })


class _ModelVector:
    """Expose exact test-only derived indexes over one sealed current model."""

    def __init__(self, model, **overrides):
        self._model = model
        self._overrides = overrides

    def __getattr__(self, name):
        try:
            return self._overrides[name]
        except KeyError:
            return getattr(self._model, name)


class PriorArtNavigatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = validation_session()
        cls.plan = cls.session["plan"]
        cls.models = MappingProxyType({
            key: value for key, value in cls.session["models"].items()
            if value.product_kind == "prior-art"})
        cls.artifacts = MappingProxyType({
            key: render.render(value) for key, value in cls.models.items()})
        cls.authority_vector = _current_profile_vector(cls.session)
        cls.authority_vector_artifact = render.render(
            cls.authority_vector["model"])

    def _exercise_runtime_navigation(self, page, navigation, expected_mode):
        relation_id, current = next(
            (identifier, item)
            for identifier, item in navigation["relations"].items()
            if item["targets"] and any(
                len(target["blocks"]) > 1 for target in item["targets"]))
        expected_owner = (
            "disclosure-scroll" if expected_mode == "side-by-side" else "panes")
        expected_claims_owner = (
            "claims-pane" if expected_mode == "side-by-side" else "panes")
        owners = page.evaluate("""() => ({
          disclosure:paneScrollOwner(disclosureScroll).id,
          claims:paneScrollOwner(claimsPane).id
        })""")
        self.assertEqual(owners, {
            "claims": expected_claims_owner,
            "disclosure": expected_owner,
        })
        page.locator('button[data-relation="%s"]' % relation_id).first.click()
        selected = current["targets"][0]["blocks"][0]
        activation = page.evaluate("""() => ({
          mode:state.mode, candidateIndex:state.candidateIndex,
          passageIndex:state.passageIndex, focus:document.activeElement.id,
          selected:selectedPassageId(relation(state.key)),
          strong:Array.from(document.querySelectorAll('.highlight-strong'))
            .map(node => node.id),
          related:Array.from(document.querySelectorAll('.highlight-soft'))
            .map(node => node.id),
          alternate:Array.from(document.querySelectorAll(
            '.highlight-alternate-candidate')).map(node => node.id),
          owner:paneScrollOwner(disclosureScroll).id,
          visible:unobscured(paneScrollOwner(disclosureScroll),
            document.getElementById(selectedPassageId(relation(state.key))))
        })""")
        self.assertEqual(activation["mode"], "forward")
        self.assertEqual(activation["candidateIndex"], 0)
        self.assertEqual(activation["passageIndex"], 0)
        self.assertEqual(activation["focus"], "forward-bar")
        self.assertEqual(activation["selected"], selected)
        self.assertEqual(activation["strong"], [selected])
        self.assertTrue(activation["related"])
        self.assertEqual(activation["alternate"], [])
        self.assertEqual(activation["owner"], expected_owner)
        self.assertTrue(activation["visible"])

        page.evaluate("movePassage(1)")
        moved = page.evaluate("""() => ({
          mode:state.mode, candidateIndex:state.candidateIndex,
          passageIndex:state.passageIndex, focus:document.activeElement.id,
          selected:selectedPassageId(relation(state.key)),
          owner:paneScrollOwner(disclosureScroll).id,
          visible:unobscured(paneScrollOwner(disclosureScroll),
            document.getElementById(selectedPassageId(relation(state.key))))
        })""")
        self.assertEqual(moved["mode"], "forward")
        self.assertEqual(moved["candidateIndex"], 0)
        self.assertEqual(moved["passageIndex"], 1)
        self.assertEqual(moved["focus"], "forward-bar")
        self.assertEqual(moved["owner"], expected_owner)
        self.assertTrue(moved["visible"])

        reader = page.locator(
            '#%s button.reader-jump' % moved["selected"]).first
        reader_target = reader.get_attribute("data-reader")
        reader.click()
        reader_state = page.evaluate("""target => ({
          focus:document.activeElement.id,
          owner:paneScrollOwner(disclosureScroll).id,
          visible:unobscured(paneScrollOwner(disclosureScroll),
            document.getElementById(target)),
          details:document.getElementById(target)
            .closest('details.full-reader').open
        })""", reader_target)
        self.assertEqual(reader_state["focus"], reader_target)
        self.assertEqual(reader_state["owner"], expected_owner)
        self.assertTrue(reader_state["visible"])
        self.assertTrue(reader_state["details"])

        reverse = page.locator(
            '#%s button[data-block]' % moved["selected"]).first
        reverse_id = reverse.get_attribute("id")
        reverse.click()
        reverse_state = page.evaluate("""() => {
          const entry = reverseEntry();
          const subject = relation(entry.relationId).subjectDomId;
          return {
            mode:state.mode, reverseIndex:state.reverseIndex,
            passage:state.key, focus:document.activeElement.id,
            subject:subject, owner:paneScrollOwner(claimsPane).id,
            visible:unobscured(paneScrollOwner(claimsPane),
              document.getElementById(subject)),
            occurrenceCount:state.reverseList.length
          };
        }""")
        self.assertEqual(reverse_state["mode"], "reverse")
        self.assertEqual(reverse_state["reverseIndex"], 0)
        self.assertEqual(reverse_state["passage"], moved["selected"])
        self.assertEqual(reverse_state["focus"], "reverse-bar")
        self.assertEqual(reverse_state["owner"], expected_claims_owner)
        self.assertTrue(reverse_state["visible"])
        self.assertGreater(reverse_state["occurrenceCount"], 1)
        page.evaluate("moveCandidate(1)")
        self.assertEqual(page.evaluate("state.reverseIndex"), 1)
        page.keyboard.press("Escape")
        cleared = page.evaluate("""returnFocus => ({
          mode:state.mode, focus:document.activeElement.id,
          forwardHidden:forwardBar.hidden, reverseHidden:reverseBar.hidden,
          highlights:document.querySelectorAll(
            '.highlight-strong,.highlight-soft,.highlight-subject,' +
            '.highlight-related,.highlight-alternate-candidate,' +
            '.highlight-obligation').length
        })""", reverse_id)
        self.assertEqual(cleared, {
            "focus": reverse_id,
            "forwardHidden": True,
            "highlights": 0,
            "mode": None,
            "reverseHidden": True,
        })
        return activation, moved, reader_state, reverse_state, cleared

    def test_exact_product_and_handoff_inventory(self):
        self.assertEqual(self.plan.product_ids, (
            "na-specification", "af-specification",
            "na-prior-art", "af-prior-art"))
        self.assertEqual(tuple(self.models), (
            "na-prior-art", "af-prior-art"))
        for product_id, model in self.models.items():
            with self.subTest(product=product_id):
                self.assertIsInstance(model, PriorArtModel)
                self.assertEqual(validate_prior_art(model), ())
                self.assertEqual(model.product_id, product_id)
                self.assertEqual(len(model.source_documents), 36)
                self.assertEqual(
                    [item.authority_scheme for item in model.source_documents],
                    ["authored-markdown-v1", "authored-relations-v1",
                     "authored-relations-v1"] +
                    ["pdf-evidence-transcription-v1"] * 33)
                self.assertEqual(
                    {item.document_id for item in model.source_documents[3:]},
                    TARGET_PACKAGES)
                handoffs = self.session["sources"].consumer_inputs[
                    model._consumer_id].handoffs
                self.assertEqual(set(handoffs), TARGET_PACKAGES | {
                    model._claim_package_id, model._comparison_package_id,
                    model._passage_map_package_id})
                self.assertTrue(all(
                    value["inputRepresentation"] == "xml" and
                    not value["dependencies"] for value in handoffs.values()))

    def test_matrix_scope_obligations_and_candidates_are_exact(self):
        expected_units = {"na-prior-art": 45, "af-prior-art": 55}
        expected_mapped = {"na-prior-art": 28, "af-prior-art": 42}
        expected_candidates = {"na-prior-art": 28, "af-prior-art": 46}
        expected_obligations = {
            "na-prior-art": {
                "passage-mapped": 16,
                "counsel-review-required": 131,
                "reviewed-no-material-passage": 21,
            },
            "af-prior-art": {
                "passage-mapped": 32,
                "counsel-review-required": 211,
                "reviewed-no-material-passage": 36,
            },
        }
        for product_id, model in self.models.items():
            with self.subTest(product=product_id):
                self.assertEqual(len(model.prior_art_scope), 33)
                self.assertEqual(len({item.document_id
                                      for item in model.prior_art_scope}), 33)
                self.assertEqual(len(model.relations.mappings),
                                 expected_units[product_id])
                self.assertEqual(set(model.mappings_by_unit),
                                 set(model.units_by_fragment))
                mapped = tuple(
                    item for item in model.relations.mappings
                    if item.status == "mapped")
                review = tuple(
                    item for item in model.relations.mappings
                    if item.status == "counsel-review-required")
                self.assertEqual(len(mapped), expected_mapped[product_id])
                self.assertEqual(len(review),
                                 expected_units[product_id] -
                                 expected_mapped[product_id])
                self.assertTrue(all(not item.targets
                                    for item in model.relations.mappings))
                self.assertTrue(all(
                    model.candidates_by_unit.get(item.subject.fragment_id)
                    for item in mapped))
                self.assertTrue(all(
                    not model.candidates_by_unit.get(item.subject.fragment_id)
                    for item in review))
                self.assertEqual(model.relations.phrase_mappings, ())
                self.assertEqual(len(model.candidate_relations),
                                 expected_candidates[product_id])
                counts = {
                    status: sum(item.status == status
                                for item in model.prior_art_obligations)
                    for status in expected_obligations[product_id]}
                self.assertEqual(counts, expected_obligations[product_id])
                self.assertEqual(
                    len(model.prior_art_obligations),
                    sum(expected_obligations[product_id].values()))
                self.assertEqual(len(model.prior_art_readers), 33)
                self.assertEqual(len(model.prior_art_passages), 15)
                self.assertEqual(len(model.reverse_index), 15)
                self.assertEqual(
                    {(item.document_id, item.fragment_id)
                     for item in model.prior_art_passages},
                    set(model.reverse_index))
                self.assertEqual(
                    set(model.candidates_by_unit),
                    {item.subject.fragment_id
                     for item in model.candidate_relations
                     if item.exact_text is None})
                self.assertEqual(
                    set(model.phrase_candidates_by_unit),
                    {item.subject.fragment_id
                     for item in model.candidate_relations
                     if item.exact_text is not None})
                self.assertEqual(
                    {item.relation_id for values in model.reverse_index.values()
                     for item in values},
                    {item.relation_id for item in model.candidate_relations})
                for candidate in model.candidate_relations:
                    unit = model.units_by_fragment[
                        candidate.subject.fragment_id]
                    if unit.unit_kind == "preamble":
                        self.assertNotEqual(
                            candidate.targets[0].role, "combination")
                        self.assertEqual(len(candidate.obligation_ids), 1)
                        self.assertEqual(len({
                            endpoint.document_id
                            for endpoint in candidate.targets[0].endpoints}), 1)
                    for target in candidate.targets:
                        self.assertIn(
                            target.role, {"specific", "combination", "context"})
                        self.assertTrue(target.note)
                        for endpoint in target.endpoints:
                            self.assertIn(endpoint.document_id, TARGET_PACKAGES)
                            self.assertNotEqual(
                                endpoint.fragment_id, endpoint.document_id)
                            item = model.get_item(
                                endpoint.document_id, endpoint.fragment_id)
                            self.assertEqual(item.item_id, endpoint.fragment_id)
                            self.assertEqual(item.content_digest,
                                             endpoint.content_digest)
                    self.assertTrue(candidate.obligation_ids)
                    self.assertTrue(all(
                        model.resolve_relation(identifier).status ==
                        "passage-mapped"
                        for identifier in candidate.obligation_ids))
                with self.assertRaises(AttributeError):
                    model.prior_art_scope = ()

    def test_static_html_has_exact_forward_and_reverse_passage_navigation(self):
        for product_id, artifact in self.artifacts.items():
            with self.subTest(product=product_id):
                model = self.models[product_id]
                text = artifact.decode("utf-8")
                navigation = _navigation(text)
                self.assertEqual(navigation["productKind"], "prior-art")
                self.assertNotIn("allCandidatesExposed", navigation["ui"])
                self.assertNotIn(
                    "specificationHighlightKey", navigation["ui"])
                self.assertNotIn('<p class="highlight-key">', text)
                self.assertTrue(text.startswith("<!DOCTYPE html>"))
                self.assertIn("Prior-art passages", text)
                self.assertIn("Claims → Prior art", text)
                self.assertIn("Prior art → Claims", text)
                self.assertIn("canonical source PDFs remain fidelity authority", text)
                self.assertNotIn('class="release-profile"', text)
                self.assertNotIn('class="disclaimer"', text)
                self.assertNotIn("TECHNICAL PREVIEW", text)
                self.assertEqual(text.count(
                    '<p class="state-note">No exact candidate passage '
                    'from this document'), 26)
                self.assertEqual(text.count(
                    'class="dblock reading-measure prior-art-passage"'), 15)
                self.assertEqual(text.count(
                    'class="full-reader"'), 33)
                self.assertEqual(text.count(
                    'class="reader-jump"'), 15)
                self.assertEqual(text.count(
                    'class="obligation obligation-'),
                    len(model.prior_art_obligations))
                self.assertEqual(text.count('class="unit state-'),
                                 len(model.units_by_fragment))
                self.assertEqual(text.count('class="mapping-row"'),
                                 len(model.units_by_fragment))
                self.assertIn("candidateIndex:0, passageIndex:0", text)
                self.assertIn("function moveCandidate(delta)", text)
                self.assertIn("function movePassage(delta)", text)
                self.assertNotIn("state.position", text)
                self.assertNotIn("obligationsByClaim", text)
                self.assertIn(
                    "state.passageIndex = 0;", text)
                self.assertIn(
                    "scrollDisclosureToNode(selectedPassageId(current));", text)
                self.assertIn(
                    "owner.scrollTop = owner.scrollTop + nodeBox.top - "
                    "desiredTop;", text)
                self.assertIn("function capableScrollOwner(node)", text)
                self.assertIn("function paneScrollOwner(primary)", text)
                self.assertIn("function unobscured(owner, node)", text)
                self.assertIn(
                    "navigation owner is absent", text)
                self.assertIn(
                    "var owner = sideBySide ? primary : panes;", text)
                self.assertIn(
                    "navigation target is outside its scroll owner", text)
                self.assertIn(
                    "navigation target is outside unobscured owner geometry",
                    text)
                self.assertIn(
                    "scrollWithin(paneScrollOwner(disclosureScroll),", text)
                self.assertIn(
                    "scrollWithin(paneScrollOwner(claimsPane),", text)
                self.assertNotIn("behavior:reducedMotion", text)
                self.assertIn(
                    "focusWithoutScroll(forwardBar);\n  applyForwardHighlights();",
                    text)
                self.assertIn("details.open = true;", text)
                self.assertIn(
                    "readerTarget.focus({preventScroll:true});", text)
                self.assertIn(
                    "scrollDisclosureToNode(control.dataset.reader);", text)
                self.assertIn(
                    "activateReverse(control.dataset.block, control.id);", text)
                for reader in model.prior_art_readers:
                    document_dom_id = model.dom_id(
                        model.relation_set_id, reader.document_id)
                    self.assertIn(
                        'class="full-reader" id="full-reader-%s"' %
                        document_dom_id, text)
                for passage in model.prior_art_passages:
                    reader_target = "reader-" + model.dom_id(
                        passage.document_id, passage.fragment_id)
                    self.assertIn('id="%s" tabindex="-1"' % reader_target,
                                  text)
                    self.assertIn('data-reader="%s"' % reader_target, text)
                for mapping in model.relations.mappings:
                    relation = navigation["relations"][mapping.relation_id]
                    self.assertIn(
                        'data-relation="%s"' % mapping.relation_id, text)
                    if mapping.status == "counsel-review-required":
                        self.assertEqual(relation["targets"], [])
                        continue
                    self.assertTrue(relation["targets"])
                    for target in relation["targets"]:
                        self.assertFalse({
                            "primary", "currentPassage", "currentTarget",
                            "selectedPassage", "selectedTarget",
                        } & set(target))
                        for block_id in target["blocks"]:
                            self.assertIn('id="%s"' % block_id, text)
                            self.assertTrue(any(
                                item["relationId"] == mapping.relation_id and
                                item["candidateId"] == target["candidateId"]
                                for item in navigation["reverse"][block_id]))
                self.assertEqual(
                    set(navigation["obligations"]), {"byClaim", "domById"})
                for claim in navigation["obligations"]["byClaim"].values():
                    self.assertEqual(set(claim), {"ids", "counts"})
                    self.assertEqual(sum(claim["counts"].values()),
                                     len(claim["ids"]))
                self.assertIn("<noscript>", text)
                self.assertIn("@media print", text)
                self.assertIn("prefers-reduced-motion: reduce", text)
                static_surface = text.split(
                    '<script type="application/json" id="nav-data"', 1)[0]
                for candidate in model.candidate_relations:
                    self.assertIn(candidate.relation_id, static_surface)
                    self.assertIn(
                        html.escape(candidate.targets[0].note, quote=True),
                        static_surface)
                for token in (
                        "fetch(", "XMLHttpRequest", "WebSocket",
                        "localStorage", "sessionStorage", "document.cookie"):
                    self.assertNotIn(token, text)

    def test_positive_and_adverse_multiplicity_vectors_use_model_enforcers(self):
        for product_id, model in self.models.items():
            with self.subTest(product=product_id):
                self.assertTrue(any(
                    len(candidate.targets[0].endpoints) > 1
                    for candidate in model.candidate_relations))
                obligation_use = Counter(
                    identifier for candidate in model.candidate_relations
                    for identifier in candidate.obligation_ids)
                self.assertTrue(any(count > 1
                                    for count in obligation_use.values()))

                base = next(
                    item for item in model.candidate_relations
                    if item.exact_text is None and
                    len(item.targets[0].endpoints) > 1)
                alternate_role = (
                    "context" if base.targets[0].role != "context"
                    else "specific")
                alternate = replace(
                    base, relation_id=base.relation_id + "-vector",
                    targets=(replace(
                        base.targets[0], role=alternate_role),))
                grouped = PriorArtModel._index_candidates(
                    (base, alternate), exact_text=False)
                self.assertEqual(
                    grouped[base.subject.fragment_id], (base, alternate))
                signatures = {
                    _candidate_semantic_signature(
                        item.subject, item.exact_text,
                        item.targets[0].role, item.obligation_ids,
                        item.targets[0].endpoints)
                    for item in (base, alternate)}
                self.assertEqual(len(signatures), 2)

                reversed_signature = _candidate_semantic_signature(
                    base.subject, base.exact_text,
                    base.targets[0].role, base.obligation_ids,
                    tuple(reversed(base.targets[0].endpoints)))
                self.assertEqual(
                    _candidate_semantic_signature(
                        base.subject, base.exact_text,
                        base.targets[0].role, base.obligation_ids,
                        base.targets[0].endpoints),
                    reversed_signature)

                inventory = set()
                signature = _candidate_semantic_signature(
                    base.subject, base.exact_text, base.targets[0].role,
                    base.obligation_ids, base.targets[0].endpoints)
                _record_unique_signature(inventory, signature, "candidate")
                with self.assertRaisesRegex(
                        ModelError, "candidate semantic signature is duplicated"):
                    _record_unique_signature(
                        inventory, signature, "candidate")

                mapped_ids = {
                    item.relation_id for item in model.prior_art_obligations
                    if item.status == "passage-mapped"}
                _validate_candidate_obligation_coverage(
                    model.prior_art_obligations, mapped_ids)
                with self.assertRaisesRegex(
                        ModelError,
                        "mapped obligation and candidate coverage disagree"):
                    _validate_candidate_obligation_coverage(
                        model.prior_art_obligations,
                        mapped_ids - {next(iter(mapped_ids))})

                preamble = next(
                    unit for unit in model.units_by_fragment.values()
                    if unit.unit_kind == "preamble")
                _validate_preamble_candidate(
                    preamble, "specific", ("one-obligation",), {"one-document"})
                for role, obligations, documents in (
                        ("combination", ("one-obligation",), {"one-document"}),
                        ("specific", ("one", "two"), {"one-document"}),
                        ("specific", ("one",), {"one", "two"})):
                    with self.assertRaisesRegex(
                            ModelError, "synthetic claim roll-up"):
                        _validate_preamble_candidate(
                            preamble, role, obligations, documents)

                review_obligation = next(
                    item for item in model.prior_art_obligations
                    if item.status == "counsel-review-required")
                review_unit = next(
                    unit for unit in model.units_by_fragment.values()
                    if unit.claim_number == review_obligation.claim_number)
                _validate_review_allocation(
                    review_unit, (review_obligation,))
                mapped_obligation = next(
                    item for item in model.prior_art_obligations
                    if item.status == "passage-mapped")
                with self.assertRaisesRegex(
                        ModelError, "does not close exact review obligations"):
                    _validate_review_allocation(
                        review_unit, (mapped_obligation,))
                allocation_subject = Endpoint(
                    model.source_documents[0].document_id,
                    review_unit.fragment_id, review_unit.content_digest)
                allocation = PriorArtReviewAllocation(
                    relation_id="allocation-vector",
                    subject=allocation_subject,
                    obligation_ids=(review_obligation.relation_id,),
                    relevance_note="Neutral fragment review allocation.")
                self.assertEqual(
                    PriorArtModel._index_by_unit((allocation,)),
                    {review_unit.fragment_id: (allocation,)})
                allocation_inventory = set()
                allocation_signature = _allocation_semantic_signature(
                    allocation.subject, allocation.obligation_ids)
                _record_unique_signature(
                    allocation_inventory, allocation_signature,
                    "fragment-review allocation")
                with self.assertRaisesRegex(
                        ModelError,
                        "fragment-review allocation semantic signature is duplicated"):
                    _record_unique_signature(
                        allocation_inventory, allocation_signature,
                        "fragment-review allocation")

                multi_passage = next(
                    item for item in model.candidate_relations
                    if item.exact_text is None and
                    len(item.targets[0].endpoints) > 1)
                vector_role = (
                    "context" if multi_passage.targets[0].role != "context"
                    else "specific")
                vector_candidate = replace(
                    multi_passage,
                    relation_id=multi_passage.relation_id + "-render-vector",
                    targets=(replace(
                        multi_passage.targets[0], role=vector_role),))
                candidate_index = dict(model.candidates_by_unit)
                candidate_index[multi_passage.subject.fragment_id] = (
                    multi_passage, vector_candidate)
                allocation_index = dict(model.review_allocations_by_unit)
                allocation_index[review_unit.fragment_id] = (allocation,)
                vector_model = _ModelVector(
                    model,
                    candidates_by_unit=MappingProxyType(candidate_index),
                    review_allocations_by_unit=MappingProxyType(
                        allocation_index))
                rendered = render.render(vector_model).decode("utf-8")
                navigation = _navigation(rendered)
                relation_id = next(
                    item.relation_id for item in model.relations.mappings
                    if item.subject.fragment_id ==
                    multi_passage.subject.fragment_id)
                targets = navigation["relations"][relation_id]["targets"]
                self.assertEqual(
                    {item["candidateId"] for item in targets},
                    {multi_passage.relation_id,
                     vector_candidate.relation_id})
                self.assertEqual(len(targets), 2)
                self.assertTrue(any(len(item["blocks"]) > 1
                                    for item in targets))
                allocation_relation_id = next(
                    item.relation_id for item in model.relations.mappings
                    if item.subject.fragment_id == review_unit.fragment_id)
                self.assertEqual(
                    navigation["relations"][allocation_relation_id]
                    ["reviewAllocations"], [{
                        "allocationId": allocation.relation_id,
                        "obligationIds": list(allocation.obligation_ids),
                        "note": allocation.relevance_note,
                    }])
                for block_id in targets[0]["blocks"]:
                    occurrences = navigation["reverse"][block_id]
                    self.assertEqual(
                        {item["candidateId"] for item in occurrences
                         if item["relationId"] == relation_id},
                        {multi_passage.relation_id,
                         vector_candidate.relation_id})
                    self.assertEqual(
                        {item["candidateIndex"] for item in occurrences
                         if item["relationId"] == relation_id}, {0, 1})
                self.assertIn(vector_candidate.relation_id, rendered)
                self.assertIn(allocation.relevance_note, rendered)

    def test_current_profile_xml_vector_reaches_the_immutable_renderer(self):
        vector = self.authority_vector
        model = vector["model"]
        self.assertIsInstance(model, PriorArtModel)
        self.assertEqual(validate_prior_art(model), ())
        self.assertIn(b"claim-prior-art-passage-map-v2", vector["xml"])
        candidates = model.candidates_by_unit[vector["candidateUnit"]]
        self.assertEqual(len(candidates), 2)
        self.assertIn(vector["candidateId"], {
            item.relation_id for item in candidates})
        self.assertTrue(any(
            len(item.targets[0].endpoints) > 1 for item in candidates))
        self.assertTrue(any(
            len(model.reverse_index[(endpoint.document_id,
                                     endpoint.fragment_id)]) > 1
            for item in candidates for endpoint in item.targets[0].endpoints))
        self.assertEqual(
            model.review_allocations_by_unit[vector["allocationUnit"]][0]
            .relation_id,
            vector["allocationId"])
        self.assertNotIn(vector["unresolvedUnit"], model.candidates_by_unit)
        self.assertNotIn(
            vector["unresolvedUnit"], model.review_allocations_by_unit)
        rendered = self.authority_vector_artifact.decode("utf-8")
        navigation = _navigation(rendered)
        relation_id = next(
            item.relation_id for item in model.relations.mappings
            if item.subject.fragment_id == vector["candidateUnit"])
        self.assertEqual(
            len(navigation["relations"][relation_id]["targets"]), 2)
        allocation_relation_id = next(
            item.relation_id for item in model.relations.mappings
            if item.subject.fragment_id == vector["allocationUnit"])
        self.assertEqual(
            navigation["relations"][allocation_relation_id]
            ["reviewAllocations"][0]["allocationId"],
            vector["allocationId"])

    def test_current_profile_adverse_vectors_fail_before_render(self):
        vector = self.authority_vector
        payload = vector["xml"]
        model = vector["model"]
        candidate = _relation_chunk(payload, vector["candidateId"])
        role = next(
            item.targets[0].role for item in model.candidate_relations
            if item.relation_id == vector["candidateId"])
        current_role = (
            '<assertionField name="candidate-role">%s</assertionField>' %
            role).encode("utf-8")
        base_role = (
            '<assertionField name="candidate-role">%s</assertionField>' %
            vector["baseCandidateRole"]).encode("utf-8")
        endpoint_pattern = rb"    <endpoint [^\n]+ role=\"evidence\" />\n"
        endpoints = re.findall(endpoint_pattern, candidate)
        self.assertGreater(len(endpoints), 1)

        permuted = candidate.replace(current_role, base_role)
        permuted = permuted.replace(
            b"".join(endpoints), b"".join(reversed(endpoints)), 1)
        with self.subTest(vector="endpoint-permuted duplicate"), \
                self.assertRaises(currentstate.CurrentStateError):
            _model_from_map_payload(
                self.session, payload.replace(candidate, permuted))

        first = endpoints[0]
        stale_endpoint = re.sub(
            rb'fragmentContentDigest="[^"]+"',
            b'fragmentContentDigest="sha256/typed-item-v1:' +
            b'0' * 64 + b'"', first, count=1)
        stale = candidate.replace(first, stale_endpoint, 1)
        with self.subTest(vector="stale digest"), \
                self.assertRaises(currentstate.CurrentStateError):
            _model_from_map_payload(
                self.session, payload.replace(candidate, stale))

        selected = next(
            item for item in model.candidate_relations
            if item.relation_id == vector["candidateId"])
        endpoint = selected.targets[0].endpoints[0]
        root_item = model.get_item(
            endpoint.document_id, endpoint.document_id + "-root")
        root_endpoint = (
            '    <endpoint documentId="{document}" '
            'fragmentContentDigest="{digest}" fragmentId="{fragment}" '
            'role="evidence" />\n').format(
                document=endpoint.document_id,
                digest=root_item.content_digest,
                fragment=root_item.item_id).encode("utf-8")
        root_target = candidate.replace(first, root_endpoint, 1)
        with self.subTest(vector="root passage"), \
                self.assertRaises(currentstate.CurrentStateError):
            _model_from_map_payload(
                self.session, payload.replace(candidate, root_target))

        obligation_documents = {
            item.evidence.document_id for item in model.prior_art_obligations
            if item.relation_id in selected.obligation_ids}
        outside = next(
            endpoint for item in model.candidate_relations
            for endpoint in item.targets[0].endpoints
            if endpoint.document_id not in obligation_documents)
        wrong_endpoint = (
            '    <endpoint documentId="{document}" '
            'fragmentContentDigest="{digest}" fragmentId="{fragment}" '
            'role="evidence" />\n').format(
                document=outside.document_id,
                digest=outside.content_digest,
                fragment=outside.fragment_id).encode("utf-8")
        wrong_document = candidate.replace(first, wrong_endpoint, 1)
        with self.subTest(vector="wrong-document closure"), \
                self.assertRaises(currentstate.CurrentStateError):
            _model_from_map_payload(
                self.session, payload.replace(candidate, wrong_document))

        allocation = _relation_chunk(payload, vector["allocationId"])
        duplicate_id = vector["allocationId"] + "-duplicate"
        duplicate = allocation.replace(
            vector["allocationId"].encode("utf-8"),
            duplicate_id.encode("utf-8"))
        duplicate_allocation = payload.replace(
            b"</relations>\n", duplicate + b"</relations>\n")
        with self.subTest(vector="duplicate allocation"), \
                self.assertRaises(currentstate.CurrentStateError):
            _model_from_map_payload(self.session, duplicate_allocation)

        subject_line = re.search(
            rb"    <endpoint [^\n]+ role=\"subject\" />\n", candidate)
        self.assertIsNotNone(subject_line)
        selected_claim = model.units_by_fragment[
            selected.subject.fragment_id].claim_number
        inferred_unit = next(
            unit for unit in model.units_by_fragment.values()
            if unit.claim_number != selected_claim and
            unit.fragment_id not in model.candidates_by_unit)
        inferred_subject = (
            '    <endpoint documentId="{document}" '
            'fragmentContentDigest="{digest}" fragmentId="{fragment}" '
            'role="subject" />\n').format(
                document=model._claim_package_id,
                digest=inferred_unit.content_digest,
                fragment=inferred_unit.fragment_id).encode("utf-8")
        inferred = candidate.replace(
            subject_line.group(0), inferred_subject, 1)
        with self.subTest(vector="inferred child"), \
                self.assertRaises(currentstate.CurrentStateError):
            _model_from_map_payload(
                self.session, payload.replace(candidate, inferred))

        rendered = self.authority_vector_artifact.decode("utf-8")
        for parallel in (
                "selectedCandidate:null", "selectedPassage:null",
                "currentCandidate:null", "currentPassage:null"):
            self.assertNotIn(parallel, rendered)

    def test_pinned_browser_matrix_proves_runtime_layout_and_navigation(self):
        with browserqa.browser_runtime(str(ROOT)) as (control, browser):
            self.assertEqual(len(browserqa.runtime_matrix(control)), 8)
            for product_id, artifact in self.artifacts.items():
                navigation = _navigation(artifact.decode("utf-8"))
                ordinary = {}
                for width, height, mode, reduced in \
                        browserqa.runtime_matrix(control):
                    label = (product_id, width, height, mode, reduced)
                    with self.subTest(vector=label):
                        context = browser.new_context(
                            viewport={"width": width, "height": height},
                            reduced_motion=("reduce" if reduced else
                                            "no-preference"))
                        page = context.new_page()
                        errors = []
                        requests = []
                        page.on("pageerror", lambda error: errors.append(str(error)))
                        page.on("request", lambda request:
                                requests.append(request.url))
                        page.set_content(artifact.decode("utf-8"),
                                         wait_until="load")
                        self.assertEqual(
                            page.evaluate("""() =>
                              matchMedia('(prefers-reduced-motion: reduce)').matches
                            """), reduced)
                        # The guide overlay auto-opens on every load; dismiss
                        # it before exercising the surfaces beneath it.
                        page.evaluate(
                            "document.getElementById('guide-overlay').close()")
                        result = self._exercise_runtime_navigation(
                            page, navigation, mode)
                        self.assertEqual(errors, [])
                        self.assertEqual(requests, [])
                        semantic = tuple(
                            tuple(sorted(item.items())) for item in result)
                        key = (width, height, mode)
                        if reduced:
                            self.assertEqual(semantic, ordinary[key])
                        else:
                            ordinary[key] = semantic
                        context.close()

    def test_pinned_browser_vector_proves_independent_candidate_movement(self):
        artifact = self.authority_vector_artifact
        navigation = _navigation(artifact.decode("utf-8"))
        relation_id, current = next(
            (identifier, item)
            for identifier, item in navigation["relations"].items()
            if len(item["targets"]) == 2 and any(
                len(target["blocks"]) > 1 for target in item["targets"]))
        with browserqa.browser_runtime(str(ROOT)) as (control, browser):
            minimum = control["layout"]["minimumViewport"]
            outcomes = []
            for reduced in (False, True):
                context = browser.new_context(
                    viewport={"width": minimum["width"],
                              "height": minimum["height"]},
                    reduced_motion=("reduce" if reduced else "no-preference"))
                page = context.new_page()
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.set_content(artifact.decode("utf-8"), wait_until="load")
                page.evaluate(
                    "document.getElementById('guide-overlay').close()")
                page.locator(
                    'button[data-relation="%s"]' % relation_id).first.click()
                page.evaluate("movePassage(1)")
                page.evaluate("moveCandidate(1)")
                state_value = page.evaluate("""() => ({
                  mode:state.mode, candidateIndex:state.candidateIndex,
                  passageIndex:state.passageIndex,
                  candidate:selectedCandidate(relation(state.key)).candidateId,
                  passage:selectedPassageId(relation(state.key)),
                  alternate:document.querySelectorAll(
                    '.highlight-alternate-candidate').length,
                  focus:document.activeElement.id,
                  owner:paneScrollOwner(disclosureScroll).id,
                  visible:unobscured(paneScrollOwner(disclosureScroll),
                    document.getElementById(
                      selectedPassageId(relation(state.key))))
                })""")
                self.assertEqual(state_value, {
                    "alternate": 0,
                    "candidate": current["targets"][1]["candidateId"],
                    "candidateIndex": 1,
                    "focus": "forward-bar",
                    "mode": "forward",
                    "owner": "panes",
                    "passage": current["targets"][1]["blocks"][0],
                    "passageIndex": 0,
                    "visible": True,
                })
                self.assertEqual(errors, [])
                outcomes.append(state_value)
                context.close()
            self.assertEqual(outcomes[0], outcomes[1])

    def test_noncurrent_passage_map_profile_fails_closed(self):
        path = ROOT / (
            "US/allowance-first/parent/prior-art-analysis/"
            "AA11393US-AF-claim-prior-art-passage-map_DRAFT.relations.xml")
        payload = path.read_bytes()
        active = b"claim-prior-art-passage-map-v2"
        noncurrent = b"claim-prior-art-passage-map-v" + str(1).encode("ascii")
        self.assertEqual(payload.count(active), 2)
        with self.assertRaises(ParseError):
            parser.parse_artifact(
                payload.replace(active, noncurrent), "relation-set")

    def test_closed_profile_and_bundle_controls_are_current(self):
        profiles = parse_json((ROOT / "structured_source/profiles/xml-v3.json").read_bytes())
        passage = profiles["relationSets"][
            "claim-prior-art-passage-map-v2"]
        self.assertEqual(passage["minimumEndpoints"], 1)
        self.assertEqual(passage["requiredEndpointRoles"], ["subject"])
        self.assertEqual(passage["relationType"],
                         "claim-prior-art-passage-map")
        self.assertEqual(passage["assertionFields"], [
            "candidate-role", "matrix-field", "matrix-relation-id",
            "obligation-ids", "obligation-status", "proposition",
            "record-kind", "relevance-note", "subject-exact-text",
        ])
        self.assertEqual(
            [key for key in profiles["relationSets"]
             if key.startswith("claim-prior-art-passage-map-")],
            ["claim-prior-art-passage-map-v2"])
        config = json.loads((ROOT / bundlezip.BUNDLE_CONFIG_PATH).read_text())
        self.assertEqual(bundlezip.validate_bundle_config(config), config)
        self.assertEqual(len(config["products"]), 4)
        self.assertEqual(len(config["members"]), 9)
        self.assertEqual(config["members"][-1], {
            "kind": "manifest", "name": "MANIFEST.txt"})


if __name__ == "__main__":
    unittest.main()
