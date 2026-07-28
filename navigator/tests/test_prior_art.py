"""Focused executable contract for the current claims-to-prior-art products."""

from collections import Counter
from dataclasses import replace
import html
import json
from pathlib import Path
import re
from types import MappingProxyType
import unittest

from navigator.lib import bundlezip, render
from navigator.lib.model import Endpoint, ModelError
from navigator.lib.priorart import (
    PriorArtModel, PriorArtReviewAllocation,
    _allocation_semantic_signature, _candidate_semantic_signature,
    _record_unique_signature, _validate_candidate_obligation_coverage,
    _validate_preamble_candidate,
    _validate_review_allocation,
)
from navigator.lib.validate import validate_prior_art
from navigator.tests import validation_session
from structured_source import parser
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
        expected_units = {"na-prior-art": 77, "af-prior-art": 61}
        expected_mapped = {"na-prior-art": 51, "af-prior-art": 44}
        expected_candidates = {"na-prior-art": 51, "af-prior-art": 44}
        expected_obligations = {
            "na-prior-art": {
                "passage-mapped": 26,
                "counsel-review-required": 159,
                "reviewed-no-material-passage": 33,
            },
            "af-prior-art": {
                "passage-mapped": 29,
                "counsel-review-required": 199,
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
                self.assertTrue(text.startswith("<!DOCTYPE html>"))
                self.assertIn("Prior-art passages", text)
                self.assertIn("Claims → Prior art", text)
                self.assertIn("Prior art → Claims", text)
                self.assertIn("canonical source PDFs remain fidelity authority", text)
                self.assertIn("not a novelty, obviousness, disclosure", text)
                self.assertEqual(text.count(
                    '<p class="state-note">No exact candidate passage '
                    'from this document'), 26)
                self.assertEqual(text.count(
                    'class="dblock prior-art-passage"'), 15)
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
                    "ownerBox.top - offset;", text)
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
