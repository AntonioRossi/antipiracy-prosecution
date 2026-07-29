"""Focused contracts for the typed-model-only HTML renderer."""

from __future__ import annotations

from collections import Counter
import hashlib
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
    _VOID = frozenset({
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr",
    })

    def __init__(self):
        super().__init__()
        self.ids = []
        self.event_attributes = []
        self.image_sources = []
        self.nested_buttons = 0
        self._button_depth = 0
        self._script_id = None
        self.scripts = {}
        self._elements = []
        self.text_by_id = {}
        self.outside_script_text = []

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
        if tag not in self._VOID:
            self._elements.append((tag, values.get("id")))

    def handle_endtag(self, tag):
        if tag == "button":
            self._button_depth -= 1
        if tag == "script":
            self._script_id = None
        if self._elements:
            open_tag, unused_identifier = self._elements.pop()
            if open_tag != tag:
                raise AssertionError(
                    "generated HTML element nesting is malformed: %s/%s" %
                    (open_tag, tag))

    def handle_data(self, data):
        if self._script_id:
            self.scripts[self._script_id] = self.scripts.get(
                self._script_id, "") + data
        if not any(tag in {"script", "style"}
                   for tag, unused_identifier in self._elements):
            self.outside_script_text.append(data)
        for unused_tag, identifier in self._elements:
            if identifier:
                self.text_by_id.setdefault(identifier, []).append(data)


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

    def _assert_unobscured_geometry(
            self, page, owner_id, node_id, clearance):
        geometry = page.evaluate("""values => {
          const owner = document.getElementById(values.ownerId);
          const node = document.getElementById(values.nodeId);
          const bar = activeNavigationBar();
          if (!owner || !node) return {present:false};
          const ownerBox = owner.getBoundingClientRect();
          const nodeBox = node.getBoundingClientRect();
          let top = Math.max(0, ownerBox.top);
          const bottom = Math.min(window.innerHeight, ownerBox.bottom);
          if (bar && !bar.hidden && owner.contains(bar)) {
            top = Math.max(top,
              ownerBox.top + bar.getBoundingClientRect().height);
          }
          return {
            present:true,
            contains:owner.contains(node),
            height:nodeBox.height,
            available:bottom - top - (2 * values.clearance),
            topClearance:nodeBox.top - top,
            bottomClearance:bottom - nodeBox.bottom
          };
        }""", {
            "ownerId": owner_id, "nodeId": node_id,
            "clearance": clearance,
        })
        self.assertTrue(geometry["present"])
        self.assertTrue(geometry["contains"])
        self.assertGreaterEqual(
            geometry["topClearance"], clearance - 1)
        if geometry["height"] <= geometry["available"] + 1:
            self.assertGreaterEqual(
                geometry["bottomClearance"], clearance - 1)
        else:
            self.assertLess(
                geometry["topClearance"],
                geometry["available"] + clearance + 1)

    def _assert_exact_owner_fails_closed(
            self, page, primary_id, expected_owner_id, target_id):
        result = page.evaluate("""values => {
          const primary = document.getElementById(values.primaryId);
          const expected = document.getElementById(values.expectedOwnerId);
          const target = document.getElementById(values.targetId);
          const oldX = expected.style.getPropertyValue('overflow-x');
          const oldXPriority = expected.style.getPropertyPriority('overflow-x');
          const oldY = expected.style.getPropertyValue('overflow-y');
          const oldYPriority = expected.style.getPropertyPriority('overflow-y');
          expected.style.setProperty('overflow-x', 'visible', 'important');
          expected.style.setProperty('overflow-y', 'visible', 'important');
          let selected = null;
          let error = null;
          try {
            selected = paneScrollOwner(primary);
            try {
              scrollWithin(selected, target, 'center');
            } catch (caught) {
              error = caught.message;
            }
          } finally {
            if (oldX) {
              expected.style.setProperty('overflow-x', oldX, oldXPriority);
            } else {
              expected.style.removeProperty('overflow-x');
            }
            if (oldY) {
              expected.style.setProperty('overflow-y', oldY, oldYPriority);
            } else {
              expected.style.removeProperty('overflow-y');
            }
          }
          return {owner:selected ? selected.id : null, error:error};
        }""", {
            "expectedOwnerId": expected_owner_id,
            "primaryId": primary_id,
            "targetId": target_id,
        })
        self.assertEqual(result, {
            "error": "navigation owner is absent", "owner": None,
        })

    def _exercise_runtime_navigation(
            self, page, navigation, expected_mode, clearance):
        self.assertEqual(navigation["productKind"], "specification")
        wide_relation_id, wide = max(
            navigation["relations"].items(),
            key=lambda item: len(item[1]["targets"]))
        self.assertGreater(len(wide["targets"]), 5)
        relation_id, current = next(
            (identifier, item)
            for identifier, item in navigation["relations"].items()
            if len(item["targets"]) > 1 and any(
                len(target["blocks"]) > 1 for target in item["targets"]))
        composite_index = next(
            index for index, target in enumerate(current["targets"])
            if len(target["blocks"]) > 1)

        def alternate_blocks(relation, selected_index):
            return sorted({
                block_id
                for index, target in enumerate(relation["targets"])
                if index != selected_index
                for block_id in target["blocks"]
            })

        def all_blocks(relation):
            return sorted({
                block_id
                for target in relation["targets"]
                for block_id in target["blocks"]
            })
        disclosure_owner = (
            "disclosure-scroll" if expected_mode == "side-by-side" else "panes")
        claims_owner = (
            "claims-pane" if expected_mode == "side-by-side" else "panes")
        owners = page.evaluate("""() => {
          const sideBySide = matchMedia(
            '(min-width:1280px) and (min-height:720px)').matches;
          return {
            mode:sideBySide ? 'side-by-side' : 'stacked',
            disclosure:paneScrollOwner(disclosureScroll).id,
            claims:paneScrollOwner(claimsPane).id,
            disclosureCapable:capableScrollOwner(
              sideBySide ? disclosureScroll : panes),
            claimsCapable:capableScrollOwner(
              sideBySide ? claimsPane : panes)
          };
        }""")
        self.assertEqual(owners, {
            "claims": claims_owner, "claimsCapable": True,
            "disclosure": disclosure_owner, "disclosureCapable": True,
            "mode": expected_mode,
        })

        # A live six- or seven-candidate relation defeats every retained
        # first-N cap and proves the specification-only concurrent overview.
        wide_forward = page.locator(
            'button[data-relation="%s"]' % wide_relation_id).first
        wide_forward.focus()
        page.keyboard.press("Enter")
        wide_first = wide["targets"][0]
        wide_activation = page.evaluate("""() => ({
          candidateIndex:state.candidateIndex,
          passageIndex:state.passageIndex,
          selected:selectedPassageId(relation(state.key)),
          strong:Array.from(document.querySelectorAll('.highlight-strong'))
            .map(node => node.id).sort(),
          context:Array.from(document.querySelectorAll('.highlight-soft'))
            .map(node => node.id).sort(),
          alternate:Array.from(document.querySelectorAll(
            '.highlight-alternate-candidate')).map(node => node.id).sort(),
          all:Array.from(document.querySelectorAll(
            '.highlight-strong,.highlight-soft,' +
            '.highlight-alternate-candidate')).map(node => node.id).sort(),
          exposure:forwardBar.textContent.includes(format(
            ui('allCandidatesExposed'), {
              count:relation(state.key).targets.length
            })),
          live:live.textContent
        })""")
        self.assertEqual(wide_activation, {
            "all": all_blocks(wide),
            "alternate": alternate_blocks(wide, 0),
            "candidateIndex": 0,
            "context": sorted(wide_first["blocks"][1:]),
            "exposure": True,
            "live": page.evaluate(
                "forwardAnnouncement(relation(state.key))"),
            "passageIndex": 0,
            "selected": wide_first["blocks"][0],
            "strong": [wide_first["blocks"][0]],
        })
        page.evaluate("moveCandidate(1)")
        wide_second = wide["targets"][1]
        wide_moved = page.evaluate("""() => ({
          candidateIndex:state.candidateIndex,
          passageIndex:state.passageIndex,
          selected:selectedPassageId(relation(state.key)),
          strong:Array.from(document.querySelectorAll('.highlight-strong'))
            .map(node => node.id).sort(),
          context:Array.from(document.querySelectorAll('.highlight-soft'))
            .map(node => node.id).sort(),
          alternate:Array.from(document.querySelectorAll(
            '.highlight-alternate-candidate')).map(node => node.id).sort(),
          all:Array.from(document.querySelectorAll(
            '.highlight-strong,.highlight-soft,' +
            '.highlight-alternate-candidate')).map(node => node.id).sort()
        })""")
        self.assertEqual(wide_moved, {
            "all": all_blocks(wide),
            "alternate": alternate_blocks(wide, 1),
            "candidateIndex": 1,
            "context": sorted(wide_second["blocks"][1:]),
            "passageIndex": 0,
            "selected": wide_second["blocks"][0],
            "strong": [wide_second["blocks"][0]],
        })
        page.keyboard.press("Escape")
        self.assertEqual(page.locator(
            ".highlight-alternate-candidate").count(), 0)

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
          alternate:Array.from(document.querySelectorAll(
            '.highlight-alternate-candidate')).map(node => node.id).sort(),
          subject:Array.from(document.querySelectorAll('.highlight-subject'))
            .map(node => node.id),
          owner:paneScrollOwner(disclosureScroll).id,
          live:live.textContent
        })""")
        self.assertEqual(activation, {
            "alternate": alternate_blocks(current, 0),
            "candidateIndex": 0,
            "focus": "forward-bar",
            "live": page.evaluate(
                "forwardAnnouncement(relation(state.key))"),
            "mode": "forward",
            "owner": disclosure_owner,
            "passageIndex": 0,
            "selected": first["blocks"][0],
            "soft": first["blocks"][1:],
            "strong": [first["blocks"][0]],
            "subject": [current["subjectDomId"]],
        })
        self._assert_unobscured_geometry(
            page, disclosure_owner, first["blocks"][0], clearance)

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
        composite = current["targets"][composite_index]
        page.keyboard.press("ArrowUp")
        passage_wrapped = page.evaluate("""() => ({
          candidateIndex:state.candidateIndex,
          passageIndex:state.passageIndex,
          selected:selectedPassageId(relation(state.key))
        })""")
        self.assertEqual(passage_wrapped, {
            "candidateIndex": composite_index,
            "passageIndex": len(composite["blocks"]) - 1,
            "selected": composite["blocks"][-1],
        })

        next_candidate = page.locator(
            '#forward-bar button[aria-label="%s"]' %
            navigation["ui"]["nextCandidate"])
        next_candidate.focus()
        page.keyboard.press("Enter")
        next_index = (composite_index + 1) % len(current["targets"])
        candidate_reset = page.evaluate("""() => ({
          candidateIndex:state.candidateIndex,
          passageIndex:state.passageIndex,
          focus:document.activeElement.id,
          selected:selectedPassageId(relation(state.key)),
          strong:Array.from(document.querySelectorAll('.highlight-strong'))
            .map(node => node.id).sort(),
          context:Array.from(document.querySelectorAll('.highlight-soft'))
            .map(node => node.id).sort(),
          alternate:Array.from(document.querySelectorAll(
            '.highlight-alternate-candidate')).map(node => node.id).sort()
        })""")
        self.assertEqual(candidate_reset, {
            "alternate": alternate_blocks(current, next_index),
            "candidateIndex": next_index,
            "context": sorted(
                current["targets"][next_index]["blocks"][1:]),
            "focus": "forward-bar",
            "passageIndex": 0,
            "selected": current["targets"][next_index]["blocks"][0],
            "strong": [current["targets"][next_index]["blocks"][0]],
        })

        page.evaluate(
            "index => moveCandidate(index - state.candidateIndex)",
            composite_index)
        next_passage = page.locator(
            '#forward-bar button[aria-label="%s"]' %
            navigation["ui"]["nextPassage"])
        next_passage.click()
        passage = page.evaluate("""() => ({
          candidateIndex:state.candidateIndex,
          passageIndex:state.passageIndex,
          focus:document.activeElement.id,
          selected:selectedPassageId(relation(state.key)),
          strong:Array.from(document.querySelectorAll('.highlight-strong'))
            .map(node => node.id),
          soft:Array.from(document.querySelectorAll('.highlight-soft'))
            .map(node => node.id),
          alternate:Array.from(document.querySelectorAll(
            '.highlight-alternate-candidate')).map(node => node.id).sort(),
          subject:Array.from(document.querySelectorAll('.highlight-subject'))
            .map(node => node.id),
          owner:paneScrollOwner(disclosureScroll).id,
          live:live.textContent
        })""")
        self.assertEqual(passage, {
            "alternate": alternate_blocks(current, composite_index),
            "candidateIndex": composite_index,
            "focus": "forward-bar",
            "live": page.evaluate(
                "forwardAnnouncement(relation(state.key))"),
            "owner": disclosure_owner,
            "passageIndex": 1,
            "selected": composite["blocks"][1],
            "soft": [composite["blocks"][0], *composite["blocks"][2:]],
            "strong": [composite["blocks"][1]],
            "subject": [current["subjectDomId"]],
        })
        self._assert_unobscured_geometry(
            page, disclosure_owner, composite["blocks"][1], clearance)

        forward.focus()
        before_scoped_arrow = page.evaluate("state.candidateIndex")
        page.keyboard.press("ArrowRight")
        self.assertEqual(
            page.evaluate("state.candidateIndex"), before_scoped_arrow)
        page.locator("#forward-bar").focus()

        page.locator(
            '#forward-bar button[aria-label="%s"]' %
            navigation["ui"]["clearSelection"]).click()
        forward_button_clear = page.evaluate("""() => ({
          mode:state.mode, focus:document.activeElement.id,
          bars:[forwardBar.hidden, reverseBar.hidden],
          highlights:document.querySelectorAll(
            '.highlight-strong,.highlight-soft,.highlight-subject,' +
            '.highlight-related,.highlight-alternate-candidate,' +
            '.highlight-obligation').length,
          owner:paneScrollOwner(claimsPane).id,
          live:live.textContent
        })""")
        self.assertEqual(forward_button_clear, {
            "bars": [True, True], "focus": forward_id, "highlights": 0,
            "live": navigation["ui"]["selectionCleared"],
            "mode": None, "owner": claims_owner,
        })
        self._assert_unobscured_geometry(
            page, claims_owner, forward_id, clearance)

        forward.focus()
        page.keyboard.press("Enter")
        page.keyboard.press("Escape")
        forward_clear = page.evaluate("""() => ({
          mode:state.mode, focus:document.activeElement.id,
          bars:[forwardBar.hidden, reverseBar.hidden],
          highlights:document.querySelectorAll(
            '.highlight-strong,.highlight-soft,.highlight-subject,' +
            '.highlight-related,.highlight-alternate-candidate,' +
            '.highlight-obligation').length,
          owner:paneScrollOwner(claimsPane).id,
          live:live.textContent
        })""")
        self.assertEqual(forward_clear, {
            "bars": [True, True], "focus": forward_id, "highlights": 0,
            "live": navigation["ui"]["selectionCleared"],
            "mode": None, "owner": claims_owner})
        self._assert_unobscured_geometry(
            page, claims_owner, forward_id, clearance)

        phrase_control = page.locator(
            "button.phrase-btn[data-relation]").first
        phrase_relation = phrase_control.get_attribute("data-relation")
        phrase_control.focus()
        page.keyboard.press("Enter")
        phrase = page.evaluate("""() => ({
          mode:state.mode, key:state.key, focus:document.activeElement.id,
          owner:paneScrollOwner(disclosureScroll).id,
          selected:selectedPassageId(relation(state.key)),
          live:live.textContent
        })""")
        self.assertEqual(phrase, {
            "focus": "forward-bar", "key": phrase_relation,
            "live": page.evaluate(
                "forwardAnnouncement(relation(state.key))"),
            "mode": "forward", "owner": disclosure_owner,
            "selected": navigation["relations"][
                phrase_relation]["targets"][0]["blocks"][0],
        })
        self._assert_unobscured_geometry(
            page, disclosure_owner, phrase["selected"], clearance)
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
          selected:selectedPassageId(relation(state.key)),
          live:live.textContent
        })""")
        self.assertEqual(caution, {
            "candidateIndex": caution_index, "details": 1,
            "expanded": "true", "focus": "caution-chip",
            "live": page.evaluate(
                "forwardAnnouncement(relation(state.key))"),
            "mode": "forward",
            "selected": caution_relation[
                "targets"][caution_index]["blocks"][0],
        })
        self._assert_unobscured_geometry(
            page, disclosure_owner, caution["selected"], clearance)
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
          text:forwardBar.textContent,
          live:live.textContent
        })""")
        self.assertEqual(disposition["mode"], "forward")
        self.assertEqual(
            disposition["live"],
            page.evaluate("forwardAnnouncement(relation(state.key))"))
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
            '.highlight-strong,.highlight-soft,' +
            '.highlight-alternate-candidate').length,
          subject:Array.from(document.querySelectorAll('.highlight-subject'))
            .map(node => node.id),
          live:live.textContent
        })""")
        self.assertEqual(no_state, {
            "candidateIndex": 0, "disclosureHighlights": 0,
            "focus": "forward-bar", "mode": "forward", "passageIndex": 0,
            "status": bool(no_candidate["statusLabel"]),
            "subject": [no_candidate["subjectDomId"]],
            "live": page.evaluate(
                "forwardAnnouncement(relation(state.key))"),
        })
        page.keyboard.press("Escape")
        no_clear = page.evaluate("""() => ({
          mode:state.mode, focus:document.activeElement.id,
          highlights:document.querySelectorAll(
            '.highlight-strong,.highlight-soft,.highlight-subject,' +
            '.highlight-related,.highlight-alternate-candidate,' +
            '.highlight-obligation').length,
          owner:paneScrollOwner(claimsPane).id,
          live:live.textContent
        })""")
        self.assertEqual(no_clear, {
            "focus": no_control.get_attribute("id"), "highlights": 0,
            "live": navigation["ui"]["selectionCleared"],
            "mode": None, "owner": claims_owner,
        })
        self._assert_unobscured_geometry(
            page, claims_owner, no_clear["focus"], clearance)

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
              .map(node => node.id).sort(),
            related:Array.from(document.querySelectorAll('.highlight-related'))
              .map(node => node.id).sort(),
            disclosureSubject:Array.from(document.querySelectorAll(
              '.highlight-subject')).map(node => node.id).sort(),
            owner:paneScrollOwner(claimsPane).id,
            live:live.textContent
          };
        }""")
        expected_subject = navigation["relations"][
            reverse_list[0]["relationId"]]["subjectDomId"]
        related_subjects = sorted({
            navigation["relations"][item["relationId"]]["subjectDomId"]
            for item in reverse_list
        } - {expected_subject})
        self.assertEqual(reverse, {
            "disclosureSubject": [block_id],
            "focus": "reverse-bar", "mode": "reverse",
            "live": page.evaluate("reverseAnnouncement()"),
            "occurrenceCount": len(reverse_list), "owner": claims_owner,
            "passage": block_id, "reverseIndex": 0,
            "related": related_subjects,
            "selected": expected_subject, "strong": [expected_subject],
        })
        self._assert_unobscured_geometry(
            page, claims_owner, expected_subject, clearance)

        page.keyboard.press("ArrowLeft")
        reverse_wrapped = page.evaluate("""() => ({
          reverseIndex:state.reverseIndex,
          selected:relation(reverseEntry().relationId).subjectDomId,
          live:live.textContent
        })""")
        self.assertEqual(reverse_wrapped, {
            "live": page.evaluate("reverseAnnouncement()"),
            "reverseIndex": len(reverse_list) - 1,
            "selected": navigation["relations"][
                reverse_list[-1]["relationId"]]["subjectDomId"],
        })
        page.keyboard.press("ArrowRight")
        self.assertEqual(page.evaluate("state.reverseIndex"), 0)
        next_reverse = page.locator(
            '#reverse-bar button[aria-label="%s"]' %
            navigation["ui"]["next"])
        next_reverse.focus()
        page.keyboard.press("Space")
        self.assertEqual(page.evaluate("state.reverseIndex"), 1)
        page.keyboard.press("Escape")
        reverse_clear = page.evaluate("""() => ({
          mode:state.mode, focus:document.activeElement.id,
          bars:[forwardBar.hidden, reverseBar.hidden],
          highlights:document.querySelectorAll(
            '.highlight-strong,.highlight-soft,.highlight-subject,' +
            '.highlight-related,.highlight-alternate-candidate,' +
            '.highlight-obligation').length,
          owner:paneScrollOwner(disclosureScroll).id,
          live:live.textContent
        })""")
        self.assertEqual(reverse_clear, {
            "bars": [True, True], "focus": reverse_id, "highlights": 0,
            "live": navigation["ui"]["selectionCleared"],
            "mode": None, "owner": disclosure_owner})
        self._assert_unobscured_geometry(
            page, disclosure_owner, reverse_id, clearance)

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
            '.highlight-related,.highlight-alternate-candidate,' +
            '.highlight-obligation').length,
          dispositionCount:document.querySelectorAll(
            '#forward-bar .disposition').length,
          cautionCount:document.querySelectorAll(
            '#forward-bar .caution-chip').length,
          live:live.textContent
        })""")
        self.assertEqual(gate, {
            "cautionCount": 1, "dispositionCount": 1,
            "focus": "forward-bar", "forwardHidden": False,
            "highlights": 0, "key": claim_key, "mode": "claim-gate",
            "live": page.evaluate("live.textContent"),
            "reverseHidden": True})
        self.assertIn(
            navigation["ui"]["gatePresent"], gate["live"])
        page.locator(
            '#forward-bar button[aria-label="%s"]' %
            navigation["ui"]["clearSelection"]).click()
        gate_button_clear = page.evaluate("""() => ({
          mode:state.mode, focus:document.activeElement.id,
          highlights:document.querySelectorAll(
            '.highlight-strong,.highlight-soft,.highlight-subject,' +
            '.highlight-related,.highlight-alternate-candidate,' +
            '.highlight-obligation').length,
          owner:paneScrollOwner(claimsPane).id,
          live:live.textContent
        })""")
        self.assertEqual(gate_button_clear, {
            "focus": gate_id_control, "highlights": 0,
            "live": navigation["ui"]["selectionCleared"],
            "mode": None, "owner": claims_owner,
        })
        self._assert_unobscured_geometry(
            page, claims_owner, gate_id_control, clearance)

        gate_control.focus()
        page.keyboard.press("Enter")
        page.keyboard.press("Escape")
        self.assertEqual(page.evaluate("document.activeElement.id"),
                         gate_id_control)
        self._assert_unobscured_geometry(
            page, claims_owner, gate_id_control, clearance)

        self._assert_exact_owner_fails_closed(
            page, "disclosure-scroll", disclosure_owner,
            first["blocks"][0])
        self._assert_exact_owner_fails_closed(
            page, "claims-pane", claims_owner, forward_id)
        return {
            "activation": activation, "caution": caution,
            "candidateReset": candidate_reset,
            "disposition": disposition,
            "forwardButtonClear": forward_button_clear,
            "forwardClear": forward_clear,
            "gate": gate, "gateButtonClear": gate_button_clear,
            "noCandidate": no_state, "noClear": no_clear,
            "passage": passage, "passageWrapped": passage_wrapped,
            "phrase": phrase, "reverse": reverse,
            "reverseClear": reverse_clear,
            "reverseWrapped": reverse_wrapped, "wrapped": wrapped,
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
                outside_text = "".join(parser.outside_script_text)
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
                self.assertGreaterEqual(outside_text.count(model.profile_label), 2)
                self.assertGreaterEqual(outside_text.count(
                    model.controlled_text("counsel-legend")), 2)
                self.assertGreaterEqual(outside_text.count(
                    model.controlled_text("standing-disclaimer")), 2)
                self.assertIn(
                    '#aux,#panes,#masthead {\n'
                    '    display:block !important; max-block-size:none; '
                    'overflow:visible; height:auto;',
                    text)
                self.assertIn(
                    '#claims-pane,#disclosure-pane,#disclosure-scroll {\n'
                    '    display:block; width:100%; overflow:visible; border:0;',
                    text)
                self.assertIn(
                    '.highlight-strong {\n'
                    '  background:var(--strong); border-left:4px solid', text)
                self.assertIn(
                    '.highlight-soft { background:var(--soft); '
                    'border-left:4px double', text)
                self.assertIn(
                    '.highlight-alternate-candidate {\n'
                    '  outline:2px dashed', text)
                self.assertIn(
                    '.highlight-subject { outline:2px solid', text)
                self.assertIn('◇ ', outside_text)

                navigation = json.loads(parser.scripts["nav-data"])
                self.assertEqual(navigation["productKind"], "specification")
                self.assertIn(
                    navigation["ui"]["specificationHighlightKey"],
                    outside_text)

                claim_document = model.source_documents[0].document_id
                for fragment_id, unit in model.units_by_fragment.items():
                    dom_id = model.dom_id(claim_document, fragment_id)
                    self.assertIn(
                        unit.text, "".join(parser.text_by_id[dom_id]))
                target_document = model.source_documents[1].document_id
                def has_addressable_descendant(node):
                    return any(
                        child.fragment_id is not None or
                        has_addressable_descendant(child)
                        for child in node.children)

                for fragment_id, node in model.disclosure_index.items():
                    if node.text and not has_addressable_descendant(node):
                        dom_id = model.dom_id(target_document, fragment_id)
                        self.assertIn(
                            node.text, "".join(parser.text_by_id[dom_id]))
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

                relation_data = navigation["relations"]
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
                for relation in relation_data.values():
                    self.assertIn(relation["subjectLabel"], outside_text)
                    self.assertIn(relation["statusLabel"], outside_text)
                    for disposition in relation["dispositions"]:
                        self.assertIn(disposition["text"], outside_text)
                    cautions = [relation["caution"]]
                    for target in relation["targets"]:
                        self.assertIn(target["note"], outside_text)
                        cautions.append(target["caution"])
                    for caution in (item for item in cautions if item):
                        for field in ("name", "scope", "typeLabel"):
                            self.assertIn(caution[field], outside_text)
                        self.assertIn(caution["quote"], outside_text)

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
            "allCandidatesExposed": (
                "All {count} recorded candidates are concurrently indicated."),
            "candidatePosition": "Candidate {position} of {total} — {label}",
            "nextCandidate": "Next candidate",
            "nextPassage": "Next passage in candidate",
            "passagePosition": "Passage {position} of {total} — {label}",
            "previousCandidate": "Previous candidate",
            "previousPassage": "Previous passage in candidate",
            "specificationHighlightKey": (
                "Highlight key: solid marks the selected passage; double "
                "marks another passage in the selected candidate; dashed "
                "marks a passage in another recorded candidate."),
        }
        expected_max_candidates = {
            "na-specification": 7,
            "af-specification": 6,
        }
        for product_id, model in self.models.items():
            with self.subTest(product=product_id):
                parser = self._parsed(product_id)
                navigation = json.loads(parser.scripts["nav-data"])
                relations = navigation["relations"]
                self.assertEqual(navigation["productKind"], "specification")
                self.assertEqual(
                    {key: navigation["ui"][key] for key in expected_ui},
                    expected_ui)
                self.assertTrue(any(
                    len(item["targets"]) > 1 for item in relations.values()))
                self.assertEqual(
                    max(len(item["targets"]) for item in relations.values()),
                    expected_max_candidates[product_id])
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
                        control_defects = page.locator("button").evaluate_all(
                            """nodes => nodes.map(node => {
                              const box = node.getBoundingClientRect();
                              const name = node.getAttribute('aria-label') ||
                                node.textContent.trim();
                              return {id:node.id, width:box.width,
                                height:box.height, name:name};
                            }).filter(item => !item.name ||
                              item.width < 24 || item.height < 24)""")
                        self.assertEqual(control_defects, [])
                        self.assertEqual(page.evaluate("""() =>
                          matchMedia(
                            '(prefers-reduced-motion: reduce)').matches
                        """), reduced)
                        result = self._exercise_runtime_navigation(
                            page, navigation, mode,
                            control["layout"]["clearancePixels"])
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
