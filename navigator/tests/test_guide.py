"""Executable acceptance for the shared navigator guide mechanism."""

from __future__ import annotations

from contextlib import contextmanager
import html
import json
import os
import re
from types import MappingProxyType
import unittest

from navigator.lib import browserqa, presentationqa, release, render, validate
from navigator.lib.model import ModelError
from navigator.tests import validation_session


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))


def _navigation(artifact):
    match = re.search(
        r'<script type="application/json" id="nav-data"[^>]*>(.*?)</script>',
        artifact, flags=re.DOTALL)
    if match is None:
        raise AssertionError("rendered product has no navigation data")
    return json.loads(match.group(1))


class GuideTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = validation_session()
        cls.models = cls.session["models"]
        cls.artifacts = MappingProxyType({
            product_id: render.render(model).decode("utf-8")
            for product_id, model in cls.models.items()
        })
        cls.runtime = browserqa.browser_runtime(ROOT)
        cls.control, cls.browser = cls.runtime.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.runtime.__exit__(None, None, None)

    @contextmanager
    def _page(self, artifact, width, height, reduced=False,
              java_script_enabled=True):
        context = self.browser.new_context(
            viewport={"width": width, "height": height},
            java_script_enabled=java_script_enabled,
            reduced_motion=("reduce" if reduced else "no-preference"))
        page = context.new_page()
        errors = []
        requests = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("request", lambda request: requests.append(request.url))
        page.set_content(artifact, wait_until="load")
        try:
            yield page, errors, requests
        finally:
            context.close()

    def _guide_items(self, model):
        return [model.controlled_text(wording_id)
                for wording_id in render.GUIDE_PROFILE_ITEMS[model.product_kind]]

    def _guide_state(self, page):
        return page.evaluate("""() => {
          const dialog = document.getElementById('guide-overlay');
          const carrier = document.getElementById('guide-details');
          const active = document.activeElement;
          return {
            open:dialog.open,
            carrierHidden:carrier.hidden,
            focusInside:active === dialog || dialog.contains(active),
            focusContained:active === dialog || dialog.contains(active) ||
              active === document.body ||
              active === document.documentElement,
            focusOutsidePageControl:!!(active && active !== dialog &&
              !dialog.contains(active) && active !== document.body &&
              active !== document.documentElement),
            focusId:active && active.id ? active.id : '',
            items:Array.from(dialog.querySelectorAll('.guide-items > li'))
              .map(node => node.textContent)
          };
        }""")

    def _semantic_state(self, page):
        return page.evaluate("""() => ({
          mode:state.mode, key:state.key,
          candidateIndex:state.candidateIndex,
          passageIndex:state.passageIndex,
          reverseIndex:state.reverseIndex,
          highlights:document.querySelectorAll(
            '.highlight-strong,.highlight-soft,.highlight-subject,' +
            '.highlight-related,.highlight-alternate-candidate,' +
            '.highlight-obligation').length,
          forwardHidden:forwardBar.hidden, reverseHidden:reverseBar.hidden,
          scroll:[claimsPane.scrollTop, disclosureScroll.scrollTop,
            panes.scrollTop]
        })""")

    def _assert_overlay_surface(self, page):
        result = page.evaluate("""() => {
          const dialog = document.getElementById('guide-overlay');
          const box = dialog.getBoundingClientRect();
          return {
            open:dialog.open,
            withinViewport:box.top >= -1 && box.left >= -1 &&
              box.bottom <= innerHeight + 1 && box.right <= innerWidth + 1,
            inlineClipped:dialog.scrollWidth > dialog.clientWidth + 1,
            pageOverflow:document.documentElement.scrollWidth >
              document.documentElement.clientWidth + 1,
            transition:getComputedStyle(dialog).transitionDuration,
            animation:getComputedStyle(dialog).animationDuration,
            positiveArea:box.width > 0 && box.height > 0
          };
        }""")
        self.assertTrue(result["open"])
        self.assertTrue(result["withinViewport"], result)
        self.assertFalse(result["inlineClipped"], result)
        self.assertFalse(result["pageOverflow"], result)
        self.assertTrue(result["positiveArea"], result)
        self.assertEqual(result["transition"], "0s")
        self.assertEqual(result["animation"], "0s")

    def test_shared_mechanism_is_product_isolated(self):
        self.assertEqual(tuple(self.models), (
            "na-specification", "af-specification",
            "na-prior-art", "af-prior-art"))
        for product_id, artifact in self.artifacts.items():
            with self.subTest(product=product_id):
                model = self.models[product_id]
                self.assertEqual(
                    artifact.count('<dialog id="guide-overlay"'), 1)
                self.assertEqual(artifact.count('<details class="guide"'), 1)
                self.assertEqual(artifact.count('id="guide-open"'), 1)
                self.assertEqual(artifact.count('class="guide-close"'), 1)
                self.assertEqual(artifact.count('<ol class="guide-items">'), 2)
                self.assertEqual(artifact.count('<span class="guide-glyph">'), 14)
                self.assertEqual(
                    artifact.count(html.escape(
                        model.controlled_text("guide-dialog-title"),
                        quote=True)), 2)
                navigation = _navigation(artifact)
                self.assertNotIn("guide", navigation)
                self.assertNotIn("guide", navigation["ui"])
                typed_relations = {
                    item.relation_id for item in
                    (*model.relations.mappings, *model.relations.phrase_mappings)
                }
                self.assertEqual(set(navigation["relations"]), typed_relations)
        for kind, editions in (
                ("specification", ("na-specification", "af-specification")),
                ("prior-art", ("na-prior-art", "af-prior-art"))):
            with self.subTest(profile=kind):
                first, second = (
                    self._guide_items(self.models[product_id])
                    for product_id in editions)
                self.assertEqual(len(first), 7)
                self.assertEqual(first[1:], second[1:])
                self.assertNotEqual(first[0], second[0])

    def test_auto_open_presents_product_kind_profile(self):
        for product_id, artifact in self.artifacts.items():
            model = self.models[product_id]
            expected = self._guide_items(model)
            for reduced in (False, True):
                label = (product_id, reduced)
                with self.subTest(vector=label), self._page(
                        artifact, 1280, 720, reduced) as (page, errors,
                                                        requests):
                    state = self._guide_state(page)
                    self.assertTrue(state["open"])
                    self.assertTrue(state["focusInside"])
                    self.assertTrue(state["carrierHidden"])
                    self.assertEqual(state["items"], expected)
                    joined = " ".join(state["items"])
                    if model.product_kind == "specification":
                        self.assertNotIn("issue-spotting", joined)
                    else:
                        self.assertNotIn("concurrently indicated", joined)
                    self.assertEqual(errors, [])
                    self.assertEqual(requests, [])

    def test_reopen_control_and_focus_cycle(self):
        for product_id, artifact in self.artifacts.items():
            for reduced in (False, True):
                label = (product_id, reduced)
                with self.subTest(vector=label), self._page(
                        artifact, 1280, 720, reduced) as (page, errors,
                                                        requests):
                    self.assertTrue(self._guide_state(page)["open"])
                    page.locator("#guide-overlay .guide-close").click()
                    self.assertFalse(self._guide_state(page)["open"])
                    page.locator("#guide-open").click()
                    self.assertTrue(self._guide_state(page)["open"])
                    reached_close = False
                    for unused_step in range(6):
                        page.keyboard.press("Tab")
                        state = self._guide_state(page)
                        self.assertTrue(state["focusContained"], state)
                        self.assertFalse(
                            state["focusOutsidePageControl"], state)
                        reached_close = reached_close or state["focusInside"]
                    self.assertTrue(reached_close)
                    page.keyboard.press("Shift+Tab")
                    state = self._guide_state(page)
                    self.assertTrue(state["focusContained"], state)
                    self.assertFalse(state["focusOutsidePageControl"], state)
                    page.keyboard.press("Escape")
                    state = self._guide_state(page)
                    self.assertFalse(state["open"])
                    self.assertEqual(state["focusId"], "guide-open")
                    self.assertEqual(errors, [])
                    self.assertEqual(requests, [])

    def test_dismissal_routes_preserve_state(self):
        for product_id, artifact in self.artifacts.items():
            model = self.models[product_id]
            navigation = _navigation(artifact)
            relation_id = next(
                identifier for identifier, item in
                navigation["relations"].items() if item["targets"])
            glyphs = {
                ui_key: model.controlled_text(wording_id)
                for ui_key, wording_id in render.GUIDE_GLYPHS.items()}
            relation = navigation["relations"][relation_id]
            expected_forward = []
            if len(relation["targets"]) > 1:
                expected_forward.extend((
                    glyphs["glyphCandidatePrevious"],
                    glyphs["glyphCandidateNext"]))
            if len(relation["targets"][0]["blocks"]) > 1:
                expected_forward.extend((
                    glyphs["glyphPassagePrevious"],
                    glyphs["glyphPassageNext"]))
            expected_forward.append(glyphs["glyphClear"])
            block_id, reverse_list = next(
                (identifier, items)
                for identifier, items in navigation["reverse"].items()
                if len(items) > 1)
            expected_reverse = [
                glyphs["glyphMovePrevious"], glyphs["glyphMoveNext"],
                glyphs["glyphClear"]]
            for reduced in (False, True):
                label = (product_id, reduced)
                with self.subTest(vector=label), self._page(
                        artifact, 1280, 720, reduced) as (page, errors,
                                                        requests):
                    before = self._semantic_state(page)
                    page.keyboard.press("Escape")
                    self.assertFalse(self._guide_state(page)["open"])
                    self.assertEqual(self._semantic_state(page), before)
                    page.locator(
                        'button[data-relation="%s"]' % relation_id).first.click()
                    engaged = self._semantic_state(page)
                    self.assertEqual(engaged["mode"], "forward")
                    self.assertGreater(engaged["highlights"], 0)
                    # The movement and clear controls render the exact
                    # wording glyphs shown in the guide, per product kind.
                    self.assertEqual(page.evaluate("""() => Array.from(
                      document.querySelectorAll(
                        '#forward-bar .selection-controls button'))
                      .map(node => node.textContent)"""), expected_forward)
                    page.locator("#guide-open").click()
                    self.assertTrue(self._guide_state(page)["open"])
                    self.assertEqual(self._semantic_state(page), engaged)
                    page.mouse.click(4, 4)
                    self.assertFalse(self._guide_state(page)["open"])
                    self.assertEqual(self._semantic_state(page), engaged)
                    page.locator("#guide-open").click()
                    self.assertTrue(self._guide_state(page)["open"])
                    page.locator("#guide-overlay .guide-close").click()
                    self.assertFalse(self._guide_state(page)["open"])
                    self.assertEqual(self._semantic_state(page), engaged)
                    page.locator("#guide-open").click()
                    self.assertTrue(self._guide_state(page)["open"])
                    page.keyboard.press("Escape")
                    self.assertFalse(self._guide_state(page)["open"])
                    self.assertEqual(self._semantic_state(page), engaged)
                    page.keyboard.press("Escape")
                    cleared = self._semantic_state(page)
                    # Clearing returns to the empty selection state; scroll
                    # positions legitimately follow the returned focus.
                    self.assertEqual(
                        {key: value for key, value in cleared.items()
                         if key != "scroll"},
                        {key: value for key, value in before.items()
                         if key != "scroll"})
                    page.locator(
                        'button[data-block="%s"]' % block_id).first.click()
                    self.assertEqual(
                        self._semantic_state(page)["mode"], "reverse")
                    self.assertEqual(page.evaluate("""() => Array.from(
                      document.querySelectorAll(
                        '#reverse-bar .selection-controls button'))
                      .map(node => node.textContent)"""), expected_reverse)
                    self.assertEqual(errors, [])
                    self.assertEqual(requests, [])

    def test_no_script_guide_is_readable_in_document_order(self):
        for product_id, artifact in self.artifacts.items():
            model = self.models[product_id]
            expected = self._guide_items(model)
            for reduced in (False, True):
                label = (product_id, reduced)
                with self.subTest(vector=label), self._page(
                        artifact, 320, 256, reduced,
                        java_script_enabled=False) as (page, errors, requests):
                    result = page.evaluate("""() => {
                      const dialog = document.getElementById('guide-overlay');
                      const carrier = document.getElementById('guide-details');
                      const legend = document.querySelector(
                        '#masthead > .legend');
                      return {
                        dialogOpen:dialog.open,
                        dialogDisplay:getComputedStyle(dialog).display,
                        carrierHidden:carrier.hidden,
                        carrierOpen:carrier.open,
                        afterLegend:legend.nextElementSibling === carrier,
                        guideOpenDisplay:getComputedStyle(
                          document.getElementById('guide-open')).display,
                        summary:carrier.querySelector('summary').textContent,
                        items:Array.from(
                          carrier.querySelectorAll('.guide-items > li'))
                          .map(node => node.textContent)
                      };
                    }""")
                    self.assertFalse(result["dialogOpen"])
                    self.assertEqual(result["dialogDisplay"], "none")
                    self.assertFalse(result["carrierHidden"])
                    self.assertFalse(result["carrierOpen"])
                    self.assertTrue(result["afterLegend"], result)
                    self.assertEqual(result["guideOpenDisplay"], "none")
                    self.assertEqual(
                        result["summary"],
                        model.controlled_text("guide-dialog-title"))
                    self.assertEqual(result["items"], expected)
                    page.locator("#guide-details > summary").focus()
                    page.keyboard.press("Enter")
                    self.assertTrue(page.evaluate(
                        "document.getElementById('guide-details').open"))
                    presentationqa.validate_noninteractive_surfaces(
                        page, self.control)
                    self.assertEqual(errors, [])
                    self.assertEqual(requests, [])

    def test_print_excludes_guide_furniture(self):
        for product_id, artifact in self.artifacts.items():
            model = self.models[product_id]
            for reduced in (False, True):
                label = (product_id, reduced)
                with self.subTest(vector=label), self._page(
                        artifact, 1280, 720, reduced) as (page, errors,
                                                        requests):
                    self.assertTrue(self._guide_state(page)["open"])
                    page.emulate_media(media="print")
                    state = page.evaluate("""() => {
                      const footer = document.querySelector('footer');
                      return {
                        dialogDisplay:getComputedStyle(
                          document.getElementById('guide-overlay')).display,
                        carrierDisplay:getComputedStyle(
                          document.getElementById('guide-details')).display,
                        guideOpenDisplay:getComputedStyle(
                          document.getElementById('guide-open')).display,
                        footerDisplay:getComputedStyle(footer).display,
                        footerLegend:footer.querySelector('.legend')
                          .textContent,
                        footerProfile:footer.querySelector('.release-profile')
                          .textContent,
                        footerDisclaimer:footer.querySelector('.disclaimer')
                          .textContent
                      };
                    }""")
                    self.assertEqual(state["dialogDisplay"], "none")
                    self.assertEqual(state["carrierDisplay"], "none")
                    self.assertEqual(state["guideOpenDisplay"], "none")
                    self.assertEqual(state["footerDisplay"], "block")
                    self.assertEqual(
                        state["footerLegend"],
                        model.controlled_text("counsel-legend"))
                    self.assertEqual(state["footerProfile"], model.profile_label)
                    self.assertEqual(
                        state["footerDisclaimer"],
                        model.controlled_text("standing-disclaimer"))
                    presentationqa.validate_noninteractive_surfaces(
                        page, self.control)
                    pdf = page.pdf(format="A4", print_background=True)
                    self.assertTrue(pdf.startswith(b"%PDF-"))
                    self.assertEqual(errors, [])
                    self.assertEqual(requests, [])
            with self.subTest(vector=(product_id, "no-script-print")), \
                    self._page(
                        artifact, 1280, 720,
                        java_script_enabled=False) as (page, errors, requests):
                page.emulate_media(media="print")
                state = page.evaluate("""() => ({
                  carrierDisplay:getComputedStyle(
                    document.getElementById('guide-details')).display,
                  footerDisplay:getComputedStyle(
                    document.querySelector('footer')).display
                })""")
                self.assertEqual(state["carrierDisplay"], "none")
                self.assertEqual(state["footerDisplay"], "block")
                self.assertEqual(errors, [])
                self.assertEqual(requests, [])

    def test_guide_surfaces_survive_enlargement_and_reflow(self):
        factor = self.control["presentation"]["textResizeFactor"]
        for product_id, artifact in self.artifacts.items():
            vectors = [
                ("text-resize", 1280, 720, reduced) for reduced in (False, True)
            ]
            vectors.extend(
                ("page-zoom", width, height, reduced)
                for width, height, unused_original_width,
                unused_original_height, reduced in
                browserqa.zoom_matrix(self.control))
            vectors.extend(
                ("reflow", width, height, reduced)
                for width, height, reduced in
                browserqa.reflow_matrix(self.control))
            vectors.extend(
                ("text-spacing", width, height, reduced)
                for width, height in ((1000, 700), (320, 256))
                for reduced in (False, True))
            for label, width, height, reduced in vectors:
                vector = (product_id, label, width, height, reduced)
                with self.subTest(vector=vector), self._page(
                        artifact, width, height, reduced) as (page, errors,
                                                            requests):
                    if label == "text-resize":
                        root = page.evaluate(
                            "parseFloat(getComputedStyle("
                            "document.documentElement).fontSize)")
                        page.evaluate(
                            "value => document.documentElement.style.fontSize ="
                            " String(value) + 'px'", root * factor)
                    if label == "text-spacing":
                        presentationqa.validate_text_spacing_adaptation(
                            page, self.control)
                    self._assert_overlay_surface(page)
                    presentationqa.validate_reading_surfaces(page, self.control)
                    self.assertEqual(errors, [])
                    self.assertEqual(requests, [])
            carrier_vectors = [
                ("carrier-text-resize", 1280, 720, reduced)
                for reduced in (False, True)
            ]
            carrier_vectors.extend(
                ("carrier-page-zoom", 640, 360, reduced)
                for reduced in (False, True))
            carrier_vectors.extend(
                ("carrier-reflow", 320, 256, reduced)
                for reduced in (False, True))
            carrier_vectors.extend(
                ("carrier-text-spacing", 320, 256, reduced)
                for reduced in (False, True))
            for label, width, height, reduced in carrier_vectors:
                vector = (product_id, label, reduced)
                with self.subTest(vector=vector), self._page(
                        artifact, width, height, reduced,
                        java_script_enabled=False) as (page, errors, requests):
                    if label == "carrier-text-resize":
                        root = page.evaluate(
                            "parseFloat(getComputedStyle("
                            "document.documentElement).fontSize)")
                        page.evaluate(
                            "value => document.documentElement.style.fontSize ="
                            " String(value) + 'px'", root * factor)
                    if label == "carrier-text-spacing":
                        presentationqa.validate_text_spacing_adaptation(
                            page, self.control)
                    page.locator("#guide-details > summary").focus()
                    page.keyboard.press("Enter")
                    self.assertTrue(page.evaluate(
                        "document.getElementById('guide-details').open"))
                    presentationqa.validate_noninteractive_surfaces(
                        page, self.control)
                    self.assertFalse(page.evaluate(
                        "document.documentElement.scrollWidth >"
                        " document.documentElement.clientWidth + 1"))
                    self.assertEqual(errors, [])
                    self.assertEqual(requests, [])

    def test_guide_wording_slots_close(self):
        chrome = {"guide-control-open", "guide-control-close",
                  "guide-dialog-title"} | set(render.GUIDE_GLYPHS.values())
        for product_id, model in self.models.items():
            with self.subTest(product=product_id):
                self.assertEqual(validate.validate_product(model), ())
                artifact = self.artifacts[product_id]
                expected = chrome | set(
                    render.GUIDE_PROFILE_ITEMS[model.product_kind])
                self.assertTrue(expected.issubset(set(model._wording)))
                other_kind = ("prior-art" if model.product_kind ==
                              "specification" else "specification")
                for wording_id in sorted(
                        set(render.GUIDE_PROFILE_ITEMS[other_kind]) - chrome):
                    with self.assertRaises(ModelError):
                        model.controlled_text(wording_id)
                title = model.controlled_text("guide-dialog-title")
                self.assertIn(model.strategy_name, title)
                self.assertIn(model.claim_set_version, title)
                profile_items = set(
                    render.GUIDE_PROFILE_ITEMS[model.product_kind])
                glyphs = render.guide_glyphs(model)
                for wording_id in sorted(expected):
                    resolved = model.controlled_text(wording_id)
                    self.assertTrue(resolved)
                    self.assertEqual(resolved, resolved.strip())
                    self.assertNotRegex(
                        resolved, r"\{[A-Za-z][A-Za-z0-9._:-]*\}")
                    if wording_id in profile_items:
                        self.assertIn(
                            render._guide_item_html(resolved, glyphs),
                            artifact)
                    else:
                        self.assertIn(
                            html.escape(resolved, quote=True), artifact)
                dialog = artifact.split(
                    '<dialog id="guide-overlay"', 1)[1].split(
                    "</dialog>", 1)[0]
                self.assertNotRegex(dialog, r"\{[A-Za-z][A-Za-z0-9._:-]*\}")
                navigation = _navigation(artifact)
                for ui_key, wording_id in render.GUIDE_GLYPHS.items():
                    glyph = model.controlled_text(wording_id)
                    # One wording origin feeds the navigation controls ...
                    self.assertEqual(navigation["ui"][ui_key], glyph)
                    # ... and the inert guide chips, with no second copy.
                    self.assertIn(
                        '<span class="guide-glyph">%s</span>' %
                        html.escape(glyph, quote=True), dialog)

    def test_guide_is_stateless_and_byte_stable(self):
        self.assertFalse([token for token in render.FORBIDDEN_SCRIPT_TOKENS
                          if token in render.JS])
        self.assertNotIn("indexedDB", render.JS)
        for product_id, model in self.models.items():
            with self.subTest(product=product_id):
                first = render.render(model)
                self.assertEqual(first, render.render(model))
                text = first.decode("utf-8")
                for token in ("localStorage", "sessionStorage",
                              "document.cookie", "indexedDB"):
                    self.assertNotIn(token, text)
                stored = self.session["snapshot"].read_bytes(
                    "navigator/dist/" +
                    release.candidate_name(model.artifact_name))
                self.assertEqual(stored, first)
                for reduced in (False, True):
                    context = self.browser.new_context(
                        viewport={"width": 1280, "height": 720},
                        reduced_motion=(
                            "reduce" if reduced else "no-preference"))
                    page = context.new_page()
                    errors = []
                    page.on("pageerror",
                            lambda error: errors.append(str(error)))
                    try:
                        page.set_content(text, wait_until="load")
                        self.assertTrue(self._guide_state(page)["open"])
                        page.evaluate(
                            "document.getElementById('guide-overlay').close()")
                        page.set_content(text, wait_until="load")
                        self.assertTrue(self._guide_state(page)["open"])
                        self.assertEqual(errors, [])
                    finally:
                        context.close()


if __name__ == "__main__":
    unittest.main()
