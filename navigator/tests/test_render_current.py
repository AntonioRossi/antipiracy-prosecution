"""Focused contracts for the typed-model-only HTML renderer."""

from __future__ import annotations

from collections import Counter
import hashlib
import html
from html.parser import HTMLParser
import json
import os
from types import MappingProxyType, SimpleNamespace
import unittest

from navigator.lib.claims import Claim, ClaimUnit
from navigator.lib.model import (
    ContentNode, Endpoint, Mapping, RelationSet, Target,
)
from navigator.lib.projections import RelationRef
from navigator.lib.render import (
    EXACT_CSP, FORBIDDEN_SCRIPT_TOKENS, JS, UI, RenderError, render,
)
from navigator.tests import validation_session


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))


class ArtifactParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.event_attributes = []
        self.image_sources = []
        self.nested_buttons = 0
        self._button_depth = 0
        self._script_id = None
        self.scripts = {}

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"])
        self.event_attributes.extend(
            name for name in values if name.casefold().startswith("on"))
        if tag == "img":
            self.image_sources.append(values.get("src", ""))
        if tag == "button":
            if self._button_depth:
                self.nested_buttons += 1
            self._button_depth += 1
        if tag == "script":
            self._script_id = values.get("id")

    def handle_endtag(self, tag):
        if tag == "button":
            self._button_depth -= 1
        if tag == "script":
            self._script_id = None

    def handle_data(self, data):
        if self._script_id:
            self.scripts[self._script_id] = self.scripts.get(
                self._script_id, "") + data


class FakeModel:
    """Small hostile typed model; it exposes no source-reading surface."""

    def __init__(self):
        self.edition_id = "na"
        self.display_name = 'Hostile </title><img src=x onerror="boom">'
        self.strategy_name = "test & strategy"
        self.strategy_prefix = "NA"
        self.artifact_name = "fake.html"
        self.declared_release_timestamp = "2026-07-23T00:00:00Z"
        self.claim_set_version = "NA-test-v1"
        self.independent_claims = (1,)
        self.relation_set_id = "na-pct"
        self.profile_label = "TECHNICAL PREVIEW <profile>"
        self.calls = []
        self.source_documents = (
            SimpleNamespace(
                document_id="claim-doc", authority_scheme="authored-markdown-v1",
                xml_role="generated-xml",
                xml_raw_digest="sha256/raw:" + "1" * 64,
                registered_path='claims/"source".xml'),
            SimpleNamespace(
                document_id="pct-doc", authority_scheme="pdf-evidence-transcription-v1",
                xml_role="transcription-xml",
                xml_raw_digest="sha256/raw:" + "2" * 64,
                registered_path="pct/source.xml"),
        )
        unit = ClaimUnit(
            fragment_id="claim-1", claim_number=1, unit_kind="preamble",
            unit_index=0, text="A </script><svg onload=boom> system",
            text_digest="sha256/c1:" + "3" * 64,
            content_digest="sha256/typed-item-v1:" + "4" * 64)
        claim = Claim(
            number=1, group="Only <group>", units=(unit,), dependencies=(),
            fragment_id="claim-1",
            content_digest="sha256/typed-item-v1:" + "5" * 64)
        self.claims = (claim,)
        self.claims_by_number = MappingProxyType({1: claim})
        self.units_by_fragment = MappingProxyType({unit.fragment_id: unit})
        self.claim_groups = ((claim.group, (1,)),)
        nodes = (
            ContentNode(
                fragment_id="target-a", kind="paragraph", text="Target <A>",
                level=None, attributes=(), children=(ContentNode(
                    fragment_id=None, kind="text", text="Target <A>",
                    level=None, attributes=(), children=(),
                    content_digest=None, editorial=False),),
                content_digest="sha256/typed-item-v1:" + "6" * 64,
                editorial=False),
            ContentNode(
                fragment_id="target-b", kind="paragraph", text="Target & B",
                level=None, attributes=(), children=(ContentNode(
                    fragment_id=None, kind="text", text="Target & B",
                    level=None, attributes=(), children=(),
                    content_digest=None, editorial=False),),
                content_digest="sha256/typed-item-v1:" + "7" * 64,
                editorial=False),
        )
        self.disclosure_blocks = nodes
        self.disclosure_index = MappingProxyType({
            node.fragment_id: node for node in nodes})
        subject = Endpoint("claim-doc", "claim-1", unit.content_digest)
        endpoints = (
            Endpoint("pct-doc", "target-a", nodes[0].content_digest),
            Endpoint("pct-doc", "target-b", nodes[1].content_digest),
        )
        mapping = Mapping(
            relation_id="relation-one", status="mapped", subject=subject,
            unit_kind="preamble", unit_index=0, caution=None,
            targets=(Target(
                role="combination", endpoints=endpoints,
                note='Note </script><img src="remote">', caution=None),))
        self.relations = RelationSet(
            relation_set_id="na-pct", edition="na", documents=(),
            gate_definitions=(), mappings=(mapping,), phrase_mappings=(),
            dispositions=())
        self.mappings_by_unit = MappingProxyType({"claim-1": (mapping,)})
        self.phrases_by_unit = MappingProxyType({})
        self.gates_by_id = MappingProxyType({})
        self.dispositions_by_subject = MappingProxyType({})
        reference = (RelationRef("mapping", "relation-one", "claim-1"),)
        self.reverse_index = MappingProxyType({
            "target-a": reference, "target-b": reference})
        self.assets = MappingProxyType({})
        self.origin_inventory = ()

    def controlled_text(self, wording_id):
        self.calls.append(wording_id)
        values = {
            "mapping-status-mapped": "Candidate passages recorded",
            "mapping-status-counsel-review-required":
                "No candidate passage recorded — counsel review required",
            "mapping-role-combination": "combination",
            "counsel-legend": "CONFIDENTIAL <legend>",
            "artifact-label-technical-preview": self.profile_label,
            "source-input-provenance": "Source inputs",
            "authority-pct-as-filed": "PCT as filed",
        }
        if wording_id == "standing-disclaimer":
            return "Disclaimer " + self.claim_set_version
        if wording_id == "provenance-summary":
            return "Summary %d/%d/%d" % (
                len(self.claims), len(self.units_by_fragment),
                len(self.disclosure_blocks))
        if wording_id == "artifact-watermark-technical-preview":
            return "PREVIEW <watermark>"
        if wording_id in values:
            return values[wording_id]
        raise KeyError(wording_id)

    @staticmethod
    def dom_id(document_id, fragment_id):
        digest = hashlib.sha256(
            (document_id + "\0" + fragment_id).encode("utf-8")).hexdigest()
        return "n-" + digest


class CurrentRenderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.models = validation_session()["models"]
        cls.artifacts = {
            edition: render(model)
            for edition, model in cls.models.items()
        }

    def _parsed(self, edition):
        parser = ArtifactParser()
        parser.feed(self.artifacts[edition].decode("utf-8"))
        return parser

    def test_live_products_are_complete_self_contained_and_accessible(self):
        expected = {"na": (30, 77), "af": (23, 61)}
        for edition, artifact in self.artifacts.items():
            with self.subTest(edition=edition):
                model = self.models[edition]
                claims, units = expected[edition]
                text = artifact.decode("utf-8")
                parser = self._parsed(edition)
                self.assertEqual(text.count('<article class="claim'), claims)
                self.assertEqual(text.count('class="unit state-'), units)
                self.assertEqual(text.count("<figure"), 4)
                self.assertEqual(len(parser.image_sources), 4)
                self.assertTrue(all(source.startswith(
                    "data:image/png;base64,") for source in parser.image_sources))
                self.assertIn('content="%s"' % EXACT_CSP, text)
                self.assertIn("<noscript>", text)
                self.assertIn('@media print', text)
                self.assertIn('@media (max-width:1279px),(max-height:719px)', text)
                self.assertIn("prefers-reduced-motion: reduce", text)
                self.assertEqual(parser.nested_buttons, 0)
                self.assertEqual(parser.event_attributes, [])
                for forbidden in (
                        "fetch(", "XMLHttpRequest", "WebSocket",
                        "localStorage", "sessionStorage", "document.cookie",
                        "history.", "location.",
                        ".innerHTML"):
                    self.assertNotIn(forbidden, text)
                self.assertFalse(any(
                    token in JS for token in FORBIDDEN_SCRIPT_TOKENS))
                self.assertIn(model.profile_label, text)
                self.assertIn(model.controlled_text("counsel-legend"), text)
                self.assertIn(html.escape(model.controlled_text(
                    "standing-disclaimer"), quote=True), text)
                provenance_data = json.loads(
                    parser.scripts["provenance-data"])
                self.assertEqual(
                    [item["xmlRole"]
                     for item in provenance_data["documents"]],
                    ["generated-xml", "transcription-xml"])
                self.assertIn(UI["xmlRoleHeader"], text)

                # All filed-text table alignment metadata is preserved by one
                # closed CSS-class mapping.
                self.assertEqual(text.count('class="cell-align-center"'), 60)
                self.assertEqual(text.count('class="cell-align-left"'), 12)

                relation_data = json.loads(
                    parser.scripts["nav-data"])["relations"]
                for mapping in model.relations.mappings:
                    expected_dispositions = {
                        item.disposition_id
                        for item in model.relations.dispositions
                        if item.subject_kind == "claim-unit" and
                        item.subject.fragment_id == mapping.subject.fragment_id
                    }
                    rendered_dispositions = relation_data[
                        mapping.relation_id]["dispositions"]
                    self.assertEqual(
                        len(rendered_dispositions), len(expected_dispositions))

    def test_every_typed_semantic_item_has_one_collision_safe_dom_locator(self):
        for edition, model in self.models.items():
            with self.subTest(edition=edition):
                parser = self._parsed(edition)
                counts = Counter(parser.ids)
                self.assertFalse([identifier for identifier, count in counts.items()
                                  if count != 1])
                claim_document = model.source_documents[0].document_id
                target_document = model.source_documents[1].document_id
                for fragment_id in model.units_by_fragment:
                    self.assertEqual(counts[
                        model.dom_id(claim_document, fragment_id)], 1)
                for fragment_id in model.disclosure_index:
                    self.assertEqual(counts[
                        model.dom_id(target_document, fragment_id)], 1)

    def test_composites_are_one_candidate_and_reverse_index_every_endpoint(self):
        for edition, model in self.models.items():
            with self.subTest(edition=edition):
                parser = self._parsed(edition)
                data = json.loads(parser.scripts["nav-data"])
                composites = [
                    (relation_id, target)
                    for relation_id, relation in data["relations"].items()
                    for target in relation["targets"]
                    if len(target["blocks"]) > 1]
                self.assertTrue(composites)
                for relation_id, target in composites:
                    self.assertEqual(target["primary"], target["blocks"][0])
                    for block_id in target["blocks"]:
                        self.assertIn(block_id, parser.ids)
                        self.assertIn(relation_id, data["reverse"][block_id])
                schedule_rows = self.artifacts[edition].count(
                    b'class="mapping-row"')
                self.assertEqual(schedule_rows,
                    len(model.relations.mappings) +
                    len(model.relations.phrase_mappings))

                # Reverse announcements must resolve the target containing the
                # activated block so target-level cautions are not discarded.
                text = self.artifacts[edition].decode("utf-8")
                self.assertIn(
                    "candidate.blocks.indexOf(blockId) !== -1", text)
                self.assertIn("cautionPresence(current, target)", text)

    def test_rendered_relations_preserve_typed_substantive_values(self):
        role_rank = {"specific": 0, "combination": 1, "context": 2}
        for edition, model in self.models.items():
            with self.subTest(edition=edition):
                parser = self._parsed(edition)
                navigation = json.loads(parser.scripts["nav-data"])
                rendered = navigation["relations"]
                typed = {
                    item.relation_id: item
                    for item in (*model.relations.mappings,
                                 *model.relations.phrase_mappings)
                }
                self.assertEqual(set(rendered), set(typed))
                target_document = model.source_documents[1].document_id

                def gate_view(gate, scope=None):
                    source = model.get_item(
                        gate.source.document_id, gate.source.fragment_id)
                    return {
                        "gateId": gate.gate_id,
                        "code": gate.code,
                        "name": model.controlled_text(
                            "gate-label-%s-%s" %
                            (model.edition_id, gate.code)),
                        "scope": model.controlled_text(
                            "caution-scope-" +
                            (gate.required_scope if scope is None else scope)),
                        "typeLabel": model.controlled_text(
                            "caution-type-source-gate"),
                        "quote": source.text,
                    }

                def caution_view(caution, scope):
                    if caution is None:
                        return None
                    if caution.kind == "source-gate":
                        return gate_view(
                            model.gates_by_id[caution.gate_id], scope)
                    wording_id = "generalization-" + caution.code
                    wording = model.controlled_text(wording_id)
                    return {
                        "gateId": None,
                        "code": caution.code,
                        "name": wording,
                        "scope": model.controlled_text(
                            "caution-scope-" + scope),
                        "typeLabel": model.controlled_text(
                            "caution-type-generalization-note"),
                        "quote": wording,
                    }

                def disposition_view(item):
                    return {
                        "gateId": item.gate_id,
                        "value": item.value,
                        "text": model.controlled_text(
                            "gate-disposition-" + item.value),
                    }

                for relation_id, relation in typed.items():
                    actual = rendered[relation_id]
                    if isinstance(relation, Mapping):
                        self.assertEqual(actual["status"], relation.status)
                        self.assertEqual(
                            actual["caution"],
                            caution_view(relation.caution, "fragment"))
                        expected_dispositions = [
                            disposition_view(item)
                            for item in model.relations.dispositions
                            if item.subject_kind == "claim-unit" and
                            item.subject.fragment_id ==
                            relation.subject.fragment_id
                        ]
                        self.assertEqual(
                            actual["dispositions"], expected_dispositions)
                    ordered = [item for _index, item in sorted(
                        enumerate(relation.targets),
                        key=lambda pair: (
                            role_rank[pair[1].role], pair[0]))]
                    self.assertEqual(
                        [item["role"] for item in actual["targets"]],
                        [item.role for item in ordered])
                    self.assertEqual(
                        [item["note"] for item in actual["targets"]],
                        [item.note for item in ordered])
                    self.assertEqual(
                        [item["blocks"] for item in actual["targets"]],
                        [[model.dom_id(target_document, endpoint.fragment_id)
                          for endpoint in item.endpoints]
                         for item in ordered])
                    self.assertEqual(
                        [item["caution"] for item in actual["targets"]],
                        [caution_view(item.caution, "target")
                         for item in ordered])

                expected_claim_gates = {}
                for disposition in model.relations.dispositions:
                    if disposition.subject_kind != "claim":
                        continue
                    number = int(
                        disposition.subject.fragment_id.rsplit("-", 1)[1])
                    expected_claim_gates.setdefault(
                        "claim-%d" % number, []).append({
                            "gate": gate_view(
                                model.gates_by_id[disposition.gate_id]),
                            "disposition": disposition_view(disposition),
                        })
                self.assertEqual(
                    navigation["claimGates"], expected_claim_gates)

    def test_preview_is_candidate_plus_only_the_controlled_watermark(self):
        model = self.models["na"]
        candidate = self.artifacts["na"].decode("utf-8")
        preview = render(model, mode="preview").decode("utf-8")
        watermark = model.controlled_text(
            "artifact-watermark-technical-preview")
        self.assertNotIn(watermark, candidate)
        self.assertIn(watermark, preview)
        start = preview.index('<div class="watermark"')
        end = preview.index("</div>", start) + len("</div>")
        self.assertEqual(preview[:start] + preview[end:], candidate)
        with self.assertRaises(RenderError):
            render(model, mode="legacy")

    def test_hostile_typed_values_are_inert_and_composite_data_is_exact(self):
        model = FakeModel()
        artifact = render(model)
        text = artifact.decode("utf-8")
        parser = ArtifactParser()
        parser.feed(text)
        data = json.loads(parser.scripts["nav-data"])
        self.assertNotIn("</script><svg", text)
        self.assertNotIn("</script><img", text)
        self.assertNotIn('onerror="boom"', text)
        self.assertNotIn('src="remote"', text)
        self.assertIn("&lt;/script&gt;&lt;svg onload=boom&gt;", text)
        target = data["relations"]["relation-one"]["targets"][0]
        self.assertEqual(len(target["blocks"]), 2)
        self.assertEqual(target["primary"], target["blocks"][0])
        self.assertTrue(all("relation-one" in data["reverse"][block]
                            for block in target["blocks"]))
        called = set(model.calls)
        self.assertTrue({
            "mapping-status-mapped", "mapping-role-combination",
            "counsel-legend", "standing-disclaimer",
            "artifact-label-technical-preview",
            "source-input-provenance", "authority-pct-as-filed",
            "provenance-summary",
        }.issubset(called))


if __name__ == "__main__":
    unittest.main()
