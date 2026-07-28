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

from navigator.lib import browserqa
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
        self.product_id = "na-specification"
        self.product_kind = "specification"
        self.display_name = 'Hostile </title><img src=x onerror="boom">'
        self.strategy_name = "test & strategy"
        self.strategy_prefix = "NA"
        self.artifact_name = "fake.html"
        self.declared_release_timestamp = "2026-07-23T00:00:00Z"
        self.claim_set_version = "NA-test-v1"
        self.target_pane_label = "PCT as-filed disclosure"
        self.authority_header = "PCT as filed"
        self.forward_mode_label = "Claims → Specification"
        self.reverse_mode_label = "Specification → Claims"
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
            ("pct-doc", "target-a"): reference,
            ("pct-doc", "target-b"): reference})
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
            "authority-target-sources": "PCT as filed",
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
        cls.session = validation_session()
        cls.models = MappingProxyType({
            key: value for key, value in
            cls.session["models"].items()
            if value.product_kind == "specification"})
        cls.artifacts = {
            edition: render(model)
            for edition, model in cls.models.items()
        }

    def _parsed(self, edition):
        parser = ArtifactParser()
        parser.feed(self.artifacts[edition].decode("utf-8"))
        return parser

    def _exercise_runtime_navigation(self, page, navigation, expected_mode):
        relation_id, current = next(
            (identifier, item)
            for identifier, item in navigation["relations"].items()
            if len(item["targets"]) > 1 and any(
                len(target["blocks"]) > 1 for target in item["targets"]))
        composite_index = next(
            index for index, target in enumerate(current["targets"])
            if len(target["blocks"]) > 1)
        disclosure_owner = (
            "disclosure-scroll" if expected_mode == "side-by-side" else "panes")
        claims_owner = (
            "claims-pane" if expected_mode == "side-by-side" else "panes")
        owners = page.evaluate("""() => ({
          disclosure:paneScrollOwner(disclosureScroll).id,
          claims:paneScrollOwner(claimsPane).id
        })""")
        self.assertEqual(owners, {
            "claims": claims_owner, "disclosure": disclosure_owner})

        forward = page.locator(
            'button[data-relation="%s"]' % relation_id).first
        forward_id = forward.get_attribute("id")
        forward.focus()
        page.keyboard.press("Enter")
        first = current["targets"][0]
        activation = page.evaluate("""() => ({
          mode:state.mode, candidateIndex:state.candidateIndex,
          passageIndex:state.passageIndex, focus:document.activeElement.id,
          selected:selectedPassageId(relation(state.key)),
          strong:Array.from(document.querySelectorAll('.highlight-strong'))
            .map(node => node.id),
          soft:Array.from(document.querySelectorAll('.highlight-soft'))
            .map(node => node.id),
          owner:paneScrollOwner(disclosureScroll).id,
          visible:unobscured(paneScrollOwner(disclosureScroll),
            document.getElementById(selectedPassageId(relation(state.key))))
        })""")
        self.assertEqual(activation, {
            "candidateIndex": 0,
            "focus": "forward-bar",
            "mode": "forward",
            "owner": disclosure_owner,
            "passageIndex": 0,
            "selected": first["blocks"][0],
            "soft": first["blocks"][1:],
            "strong": [first["blocks"][0]],
            "visible": True,
        })

        page.keyboard.press("ArrowLeft")
        wrapped = page.evaluate("""() => ({
          candidateIndex:state.candidateIndex,
          passageIndex:state.passageIndex,
          focus:document.activeElement.id,
          selected:selectedPassageId(relation(state.key))
        })""")
        self.assertEqual(wrapped, {
            "candidateIndex": len(current["targets"]) - 1,
            "focus": "forward-bar",
            "passageIndex": 0,
            "selected": current["targets"][-1]["blocks"][0],
        })

        page.evaluate(
            "index => moveCandidate(index - state.candidateIndex)",
            composite_index)
        page.keyboard.press("ArrowDown")
        composite = current["targets"][composite_index]
        passage = page.evaluate("""() => ({
          candidateIndex:state.candidateIndex,
          passageIndex:state.passageIndex,
          focus:document.activeElement.id,
          selected:selectedPassageId(relation(state.key)),
          strong:Array.from(document.querySelectorAll('.highlight-strong'))
            .map(node => node.id),
          soft:Array.from(document.querySelectorAll('.highlight-soft'))
            .map(node => node.id),
          owner:paneScrollOwner(disclosureScroll).id,
          visible:unobscured(paneScrollOwner(disclosureScroll),
            document.getElementById(selectedPassageId(relation(state.key))))
        })""")
        self.assertEqual(passage, {
            "candidateIndex": composite_index,
            "focus": "forward-bar",
            "owner": disclosure_owner,
            "passageIndex": 1,
            "selected": composite["blocks"][1],
            "soft": [composite["blocks"][0], *composite["blocks"][2:]],
            "strong": [composite["blocks"][1]],
            "visible": True,
        })

        page.keyboard.press("Escape")
        forward_clear = page.evaluate("""() => ({
          mode:state.mode, focus:document.activeElement.id,
          bars:[forwardBar.hidden, reverseBar.hidden],
          highlights:document.querySelectorAll(
            '.highlight-strong,.highlight-soft,.highlight-subject,' +
            '.highlight-related,.highlight-obligation').length,
          owner:paneScrollOwner(claimsPane).id,
          visible:unobscured(paneScrollOwner(claimsPane),
            document.getElementById(document.activeElement.id))
        })""")
        self.assertEqual(forward_clear, {
            "bars": [True, True], "focus": forward_id, "highlights": 0,
            "mode": None, "owner": claims_owner, "visible": True})

        phrase_control = page.locator(
            "button.phrase-btn[data-relation]").first
        phrase_relation = phrase_control.get_attribute("data-relation")
        phrase_control.focus()
        page.keyboard.press("Enter")
        phrase = page.evaluate("""() => ({
          mode:state.mode, key:state.key, focus:document.activeElement.id,
          owner:paneScrollOwner(disclosureScroll).id,
          selected:selectedPassageId(relation(state.key)),
          visible:unobscured(paneScrollOwner(disclosureScroll),
            document.getElementById(selectedPassageId(relation(state.key))))
        })""")
        self.assertEqual(phrase, {
            "focus": "forward-bar", "key": phrase_relation,
            "mode": "forward", "owner": disclosure_owner,
            "selected": navigation["relations"][
                phrase_relation]["targets"][0]["blocks"][0],
            "visible": True})
        page.keyboard.press("Escape")

        caution_id, caution_relation, caution_index = next(
            (identifier, item, index)
            for identifier, item in navigation["relations"].items()
            for index, target in enumerate(item["targets"])
            if item["caution"] or target["caution"])
        caution_control = page.locator(
            'button[data-relation="%s"]' % caution_id).first
        caution_control.focus()
        page.keyboard.press("Enter")
        if caution_index:
            page.evaluate(
                "index => moveCandidate(index - state.candidateIndex)",
                caution_index)
        caution_chip = page.locator(
            "#forward-bar button.caution-chip").first
        caution_chip.click()
        caution = page.evaluate("""() => ({
          mode:state.mode, candidateIndex:state.candidateIndex,
          focus:document.activeElement.className,
          expanded:document.querySelector(
            '#forward-bar button.caution-chip').getAttribute('aria-expanded'),
          details:document.querySelectorAll(
            '#forward-bar .caution-detail').length,
          visible:unobscured(paneScrollOwner(disclosureScroll),
            document.getElementById(selectedPassageId(relation(state.key))))
        })""")
        self.assertEqual(caution, {
            "candidateIndex": caution_index, "details": 1,
            "expanded": "true", "focus": "caution-chip",
            "mode": "forward", "visible": True})
        expected_caution = (
            caution_relation["targets"][caution_index]["caution"] or
            caution_relation["caution"])
        self.assertIn(expected_caution["name"],
                      caution_chip.get_attribute("aria-label"))
        page.keyboard.press("Escape")

        disposition_id, disposition_relation = next(
            (identifier, item)
            for identifier, item in navigation["relations"].items()
            if item["dispositions"])
        disposition_control = page.locator(
            'button[data-relation="%s"]' % disposition_id).first
        disposition_control.focus()
        page.keyboard.press("Enter")
        disposition = page.evaluate("""() => ({
          mode:state.mode, count:document.querySelectorAll(
            '#forward-bar .disposition').length,
          text:forwardBar.textContent
        })""")
        self.assertEqual(disposition["mode"], "forward")
        self.assertEqual(
            disposition["count"], len(disposition_relation["dispositions"]))
        for item in disposition_relation["dispositions"]:
            self.assertIn(item["text"], disposition["text"])
        page.keyboard.press("Escape")

        no_id, no_candidate = next(
            (identifier, item)
            for identifier, item in navigation["relations"].items()
            if not item["targets"])
        no_control = page.locator(
            'button[data-relation="%s"]' % no_id).first
        no_control.focus()
        page.keyboard.press("Space")
        no_state = page.evaluate("""() => ({
          mode:state.mode, candidateIndex:state.candidateIndex,
          passageIndex:state.passageIndex, focus:document.activeElement.id,
          status:forwardBar.textContent.includes(
            relation(state.key).statusLabel),
          disclosureHighlights:disclosureScroll.querySelectorAll(
            '.highlight-strong,.highlight-soft').length
        })""")
        self.assertEqual(no_state, {
            "candidateIndex": 0, "disclosureHighlights": 0,
            "focus": "forward-bar", "mode": "forward", "passageIndex": 0,
            "status": bool(no_candidate["statusLabel"])})
        page.keyboard.press("Escape")

        block_id, reverse_list = next(
            (identifier, items)
            for identifier, items in navigation["reverse"].items()
            if len(items) > 1)
        reverse_control = page.locator(
            'button[data-block="%s"]' % block_id).first
        reverse_id = reverse_control.get_attribute("id")
        reverse_control.focus()
        page.keyboard.press("Enter")
        reverse = page.evaluate("""() => {
          const entry = reverseEntry();
          const subject = relation(entry.relationId).subjectDomId;
          return {
            mode:state.mode, reverseIndex:state.reverseIndex,
            focus:document.activeElement.id, passage:state.key,
            occurrenceCount:state.reverseList.length,
            selected:subject,
            strong:Array.from(document.querySelectorAll('.highlight-strong'))
              .map(node => node.id),
            owner:paneScrollOwner(claimsPane).id,
            visible:unobscured(paneScrollOwner(claimsPane),
              document.getElementById(subject))
          };
        }""")
        expected_subject = navigation["relations"][
            reverse_list[0]["relationId"]]["subjectDomId"]
        self.assertEqual(reverse, {
            "focus": "reverse-bar", "mode": "reverse",
            "occurrenceCount": len(reverse_list), "owner": claims_owner,
            "passage": block_id, "reverseIndex": 0,
            "selected": expected_subject, "strong": [expected_subject],
            "visible": True})
        page.keyboard.press("ArrowRight")
        self.assertEqual(page.evaluate("state.reverseIndex"), 1)
        page.keyboard.press("Escape")
        reverse_clear = page.evaluate("""() => ({
          mode:state.mode, focus:document.activeElement.id,
          bars:[forwardBar.hidden, reverseBar.hidden],
          highlights:document.querySelectorAll(
            '.highlight-strong,.highlight-soft,.highlight-subject,' +
            '.highlight-related,.highlight-obligation').length,
          owner:paneScrollOwner(disclosureScroll).id,
          visible:unobscured(paneScrollOwner(disclosureScroll),
            document.getElementById(document.activeElement.id))
        })""")
        self.assertEqual(reverse_clear, {
            "bars": [True, True], "focus": reverse_id, "highlights": 0,
            "mode": None, "owner": disclosure_owner, "visible": True})

        claim_key = next(iter(navigation["claimGates"]))
        gate_id = navigation["claimGates"][claim_key][0]["gate"]["gateId"]
        gate_control = page.locator(
            'button[data-gate="%s"][data-claim="%s"]' %
            (gate_id, claim_key)).first
        gate_id_control = gate_control.get_attribute("id")
        gate_control.focus()
        page.keyboard.press("Space")
        gate = page.evaluate("""() => ({
          mode:state.mode, key:state.key, focus:document.activeElement.id,
          forwardHidden:forwardBar.hidden, reverseHidden:reverseBar.hidden,
          highlights:document.querySelectorAll(
            '.highlight-strong,.highlight-soft,.highlight-subject,' +
            '.highlight-related,.highlight-obligation').length
        })""")
        self.assertEqual(gate, {
            "focus": "forward-bar", "forwardHidden": False,
            "highlights": 0, "key": claim_key, "mode": "claim-gate",
            "reverseHidden": True})
        page.keyboard.press("Escape")
        self.assertEqual(page.evaluate("document.activeElement.id"),
                         gate_id_control)
        return {
            "activation": activation, "caution": caution,
            "disposition": disposition, "forwardClear": forward_clear,
            "gate": gate, "noCandidate": no_state, "passage": passage,
            "phrase": phrase, "reverse": reverse,
            "reverseClear": reverse_clear, "wrapped": wrapped,
        }

    def test_live_products_are_complete_self_contained_and_accessible(self):
        expected = {"na-specification": (30, 77),
                    "af-specification": (23, 61)}
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
                    for block_id in target["blocks"]:
                        self.assertIn(block_id, parser.ids)
                        self.assertTrue(any(
                            item["relationId"] == relation_id
                            for item in data["reverse"][block_id]))
                schedule_rows = self.artifacts[edition].count(
                    b'class="mapping-row"')
                self.assertEqual(schedule_rows,
                    len(model.relations.mappings) +
                    len(model.relations.phrase_mappings))

                # Reverse entries bind the exact candidate index, so a shared
                # endpoint never requires a first-match target search.
                text = self.artifacts[edition].decode("utf-8")
                self.assertIn("function reverseCandidate()", text)
                self.assertIn(
                    "current.targets[entry.candidateIndex]", text)
                self.assertIn("cautionPresence(current, candidate)", text)

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

    def test_current_profile_specification_vectors_reach_renderer(self):
        self.assertEqual(tuple(self.models), (
            "na-specification", "af-specification"))
        expected_ui = {
            "candidatePosition": "Candidate {position} of {total} — {label}",
            "nextCandidate": "Next candidate",
            "nextPassage": "Next passage in candidate",
            "passagePosition": "Passage {position} of {total} — {label}",
            "previousCandidate": "Previous candidate",
            "previousPassage": "Previous passage in candidate",
        }
        for product_id, model in self.models.items():
            with self.subTest(product=product_id):
                parser = self._parsed(product_id)
                navigation = json.loads(parser.scripts["nav-data"])
                relations = navigation["relations"]
                self.assertEqual(
                    {key: navigation["ui"][key] for key in expected_ui},
                    expected_ui)
                self.assertTrue(any(
                    len(item["targets"]) > 1 for item in relations.values()))
                self.assertTrue(any(
                    len(target["blocks"]) > 1
                    for item in relations.values()
                    for target in item["targets"]))
                self.assertTrue(any(
                    len(items) > 1
                    for items in navigation["reverse"].values()))
                self.assertTrue(model.relations.phrase_mappings)
                self.assertTrue(any(
                    not item["targets"] for item in relations.values()))
                self.assertTrue(any(
                    item["caution"] or any(
                        target["caution"] for target in item["targets"])
                    for item in relations.values()))
                self.assertTrue(navigation["claimGates"])
                self.assertTrue(any(
                    item["dispositions"] for item in relations.values()))
                text = self.artifacts[product_id].decode("utf-8")
                for parallel in (
                        "selectedCandidate:null", "selectedPassage:null",
                        "currentCandidate:null", "currentPassage:null",
                        "currentTarget:null"):
                    self.assertNotIn(parallel, text)

    def test_pinned_browser_matrix_proves_specification_runtime(self):
        with browserqa.browser_runtime(ROOT) as (control, browser):
            self.assertEqual(len(browserqa.runtime_matrix(control)), 8)
            for product_id, artifact in self.artifacts.items():
                parser = self._parsed(product_id)
                navigation = json.loads(parser.scripts["nav-data"])
                ordinary = {}
                for width, height, mode, reduced in \
                        browserqa.runtime_matrix(control):
                    label = (product_id, width, height, mode, reduced)
                    with self.subTest(vector=label):
                        context = browser.new_context(
                            viewport={"width": width, "height": height},
                            reduced_motion=(
                                "reduce" if reduced else "no-preference"))
                        page = context.new_page()
                        errors = []
                        requests = []
                        page.on("pageerror", lambda error:
                                errors.append(str(error)))
                        page.on("request", lambda request:
                                requests.append(request.url))
                        page.set_content(
                            artifact.decode("utf-8"), wait_until="load")
                        self.assertEqual(page.evaluate("""() =>
                          matchMedia(
                            '(prefers-reduced-motion: reduce)').matches
                        """), reduced)
                        result = self._exercise_runtime_navigation(
                            page, navigation, mode)
                        self.assertEqual(errors, [])
                        self.assertEqual(requests, [])
                        key = (width, height, mode)
                        if reduced:
                            self.assertEqual(result, ordinary[key])
                        else:
                            ordinary[key] = result
                        context.close()

    def test_preview_is_candidate_plus_only_the_controlled_watermark(self):
        model = self.models["na-specification"]
        candidate = self.artifacts["na-specification"].decode("utf-8")
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
        self.assertTrue(all(any(
            item["relationId"] == "relation-one"
            for item in data["reverse"][block])
            for block in target["blocks"]))
        called = set(model.calls)
        self.assertTrue({
            "mapping-status-mapped", "mapping-role-combination",
            "counsel-legend", "standing-disclaimer",
            "artifact-label-technical-preview",
            "source-input-provenance", "authority-target-sources",
            "provenance-summary",
        }.issubset(called))


if __name__ == "__main__":
    unittest.main()
