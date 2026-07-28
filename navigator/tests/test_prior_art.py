"""Focused executable contract for the current claims-to-prior-art products."""

import json
from pathlib import Path
import re
from types import MappingProxyType
import unittest

from navigator.lib import bundlezip, render
from navigator.lib.priorart import PriorArtModel
from navigator.lib.validate import validate_prior_art
from navigator.tests import validation_session
from structured_source.control import parse_json


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
        expected_mapped = {"na-prior-art": 58, "af-prior-art": 47}
        expected_obligations = {
            "na-prior-art": {
                "passage-mapped": 33,
                "counsel-review-required": 152,
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
                self.assertTrue(all(item.targets for item in mapped))
                self.assertTrue(all(not item.targets for item in review))
                self.assertEqual(model.relations.phrase_mappings, ())
                self.assertEqual(len(model.candidate_relations),
                                 expected_mapped[product_id])
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
                for candidate in model.candidate_relations:
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
                self.assertIn("scrollToNode(selected.primary);", text)
                self.assertIn("details.open = true;", text)
                self.assertIn("readerTarget.focus();", text)
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
                        self.assertIn(target["primary"], target["blocks"])
                        for block_id in target["blocks"]:
                            self.assertIn('id="%s"' % block_id, text)
                            self.assertIn(
                                mapping.relation_id,
                                navigation["reverse"][block_id])
                self.assertIn("<noscript>", text)
                self.assertIn("@media print", text)
                self.assertIn("prefers-reduced-motion: reduce", text)
                for token in (
                        "fetch(", "XMLHttpRequest", "WebSocket",
                        "localStorage", "sessionStorage", "document.cookie"):
                    self.assertNotIn(token, text)

    def test_closed_profile_and_bundle_controls_are_current(self):
        profiles = parse_json((ROOT / "structured_source/profiles/xml-v3.json").read_bytes())
        passage = profiles["relationSets"][
            "claim-prior-art-passage-map-v1"]
        self.assertEqual(passage["minimumEndpoints"], 1)
        self.assertEqual(passage["requiredEndpointRoles"], ["subject"])
        self.assertEqual(passage["relationType"],
                         "claim-prior-art-passage-map")
        self.assertEqual(passage["assertionFields"], [
            "candidate-role", "matrix-field", "matrix-relation-id",
            "obligation-ids", "obligation-status", "proposition",
            "record-kind", "subject-exact-text",
        ])
        config = json.loads((ROOT / bundlezip.BUNDLE_CONFIG_PATH).read_text())
        self.assertEqual(bundlezip.validate_bundle_config(config), config)
        self.assertEqual(len(config["products"]), 4)
        self.assertEqual(len(config["members"]), 9)
        self.assertEqual(config["members"][-1], {
            "kind": "manifest", "name": "MANIFEST.txt"})


if __name__ == "__main__":
    unittest.main()
