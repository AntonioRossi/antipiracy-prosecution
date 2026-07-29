"""Executable acceptance for shared navigator presentation and readability."""

from __future__ import annotations

from contextlib import contextmanager
import json
import math
import os
import re
from types import MappingProxyType
import unittest

from navigator.lib import browserqa, presentationqa
from navigator.lib.render import CSS, render
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


class PresentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = validation_session()
        cls.models = cls.session["models"]
        cls.artifacts = MappingProxyType({
            product_id: render(model).decode("utf-8")
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
        # The guide overlay auto-opens on every load; existing vectors exercise
        # the surfaces beneath it, so each harness page dismisses it first.
        page.evaluate("document.getElementById('guide-overlay').close()")
        try:
            yield page, errors, requests
        finally:
            context.close()

    def _assert_layout_surface(self, page):
        result = page.evaluate("""() => {
          const masthead = document.getElementById('masthead');
          const claims = document.getElementById('claims-pane');
          const disclosure = document.getElementById('disclosure-pane');
          const panesBox = panes.getBoundingClientRect();
          const mastheadBox = masthead.getBoundingClientRect();
          const claimsBox = claims.getBoundingClientRect();
          const disclosureBox = disclosure.getBoundingClientRect();
          const clipped = [...document.querySelectorAll('body *')].filter(node => {
            if (!node.getClientRects().length || node.matches(
                '.visually-hidden,.watermark,.navigation-bar[hidden]')) return false;
            const style = getComputedStyle(node);
            const clipsX = ['hidden','clip'].includes(style.overflowX) &&
              node.scrollWidth > node.clientWidth + 1;
            const clipsY = ['hidden','clip'].includes(style.overflowY) &&
              node.scrollHeight > node.clientHeight + 1;
            return clipsX || clipsY;
          }).map(node => ({tag:node.tagName, id:node.id,
            className:String(node.className), clientWidth:node.clientWidth,
            scrollWidth:node.scrollWidth, clientHeight:node.clientHeight,
            scrollHeight:node.scrollHeight}));
          const overflowing = [...panes.querySelectorAll('*')].filter(node => {
            const box = node.getBoundingClientRect();
            return box.right > panesBox.right + 1 || box.left < panesBox.left - 1;
          }).slice(0, 12).map(node => {
            const box = node.getBoundingClientRect();
            return {
              tag:node.tagName, id:node.id, className:String(node.className),
              left:box.left, right:box.right, width:box.width,
              clientWidth:node.clientWidth, scrollWidth:node.scrollWidth
            };
          });
          const side = matchMedia(
            '(min-width:1280px) and (min-height:720px)').matches;
          return {
            contentHeight:document.getElementById('content-root').clientHeight,
            panesHeight:panes.clientHeight,
            panesWidth:panes.clientWidth,
            pageOverflow:document.documentElement.scrollWidth >
              document.documentElement.clientWidth + 1,
            panesOverflowX:panes.scrollWidth > panes.clientWidth + 1,
            mastheadOverflow:masthead.scrollWidth > masthead.clientWidth + 1,
            mastheadBeforeClaims:mastheadBox.bottom <= claimsBox.top + 1,
            mastheadBeforeDisclosure:mastheadBox.bottom <= disclosureBox.top + 1,
            panesInViewport:panesBox.top >= -1 &&
              panesBox.bottom <= innerHeight + 1,
            clipped:clipped,
            overflowing:overflowing,
            sideBySide:side
          };
        }""")
        self.assertGreater(result["contentHeight"], 0)
        self.assertGreater(result["panesHeight"], 0)
        self.assertGreater(result["panesWidth"], 0)
        self.assertFalse(result["pageOverflow"])
        self.assertFalse(result["panesOverflowX"], result["overflowing"])
        self.assertFalse(result["mastheadOverflow"])
        self.assertEqual(result["clipped"], [])
        self.assertTrue(result["mastheadBeforeClaims"])
        self.assertTrue(result["mastheadBeforeDisclosure"])
        self.assertTrue(result["panesInViewport"])

    def _assert_aux_surface_reachable(self, page):
        toggle = page.locator("#aux-toggle")
        toggle.click()
        self.assertEqual(toggle.get_attribute("aria-pressed"), "true")
        about = page.locator("#about")
        about.scroll_into_view_if_needed()
        result = page.evaluate("""() => {
          const aux = document.getElementById('aux');
          const schedule = document.getElementById('schedule');
          const about = document.getElementById('about');
          const auxBox = aux.getBoundingClientRect();
          const aboutBox = about.getBoundingClientRect();
          const side = matchMedia(
            '(min-width:1280px) and (min-height:720px)').matches;
          const owner = side ? aux : panes;
          const ownerBox = owner.getBoundingClientRect();
          return {
            display:getComputedStyle(aux).display,
            auxWidth:aux.clientWidth, auxHeight:aux.clientHeight,
            scheduleHeight:schedule.getBoundingClientRect().height,
            aboutHeight:aboutBox.height,
            owner:owner.id, ownerHeight:owner.clientHeight,
            aboutReachable:aboutBox.bottom > ownerBox.top &&
              aboutBox.top < ownerBox.bottom
          };
        }""")
        self.assertEqual(result["display"], "block")
        self.assertGreater(result["auxWidth"], 0)
        self.assertGreater(result["auxHeight"], 0)
        self.assertGreater(result["scheduleHeight"], 0)
        self.assertGreater(result["aboutHeight"], 0)
        self.assertGreater(result["ownerHeight"], 0)
        self.assertTrue(result["aboutReachable"])
        presentationqa.validate_reading_surfaces(page, self.control)
        toggle.click()
        self.assertEqual(toggle.get_attribute("aria-pressed"), "false")

    def _mapped_vector(self, navigation):
        relation_id, relation = next(
            (identifier, item)
            for identifier, item in navigation["relations"].items()
            if item["targets"])
        composite = next((
            (identifier, item, index)
            for identifier, item in navigation["relations"].items()
            for index, target in enumerate(item["targets"])
            if len(target["blocks"]) > 1
        ), None)
        return relation_id, relation, composite

    def _assert_basic_navigation(self, page, navigation, product_kind):
        relation_id, relation, composite = self._mapped_vector(navigation)
        origin = page.locator(
            'button[data-relation="%s"]' % relation_id).first
        origin_id = origin.get_attribute("id")
        origin.focus()
        page.keyboard.press("Enter")
        forward = page.evaluate("""() => {
          const current = relation(state.key);
          const selected = selectedPassageId(current);
          const owner = paneScrollOwner(disclosureScroll);
          return {
            mode:state.mode, selected:selected,
            candidateIndex:state.candidateIndex,
            passageIndex:state.passageIndex,
            focus:document.activeElement.id,
            owner:owner ? owner.id : null,
            unobscured:unobscured(owner, document.getElementById(selected))
          };
        }""")
        self.assertEqual(forward["mode"], "forward")
        self.assertEqual(forward["focus"], "forward-bar")
        self.assertEqual(
            forward["selected"], relation["targets"][0]["blocks"][0])
        self.assertTrue(forward["unobscured"], forward)

        if len(relation["targets"]) > 1:
            page.keyboard.press("ArrowRight")
            self.assertEqual(page.evaluate("state.candidateIndex"), 1)
            self.assertEqual(page.evaluate("state.passageIndex"), 0)
            page.keyboard.press("ArrowLeft")

        if composite is not None:
            composite_id, composite_relation, candidate_index = composite
            if composite_id != relation_id:
                page.keyboard.press("Escape")
                composite_origin = page.locator(
                    'button[data-relation="%s"]' % composite_id).first
                composite_origin.focus()
                page.keyboard.press("Enter")
            for unused_index in range(candidate_index):
                page.keyboard.press("ArrowRight")
            before = page.evaluate("selectedPassageId(relation(state.key))")
            page.keyboard.press("ArrowDown")
            after = page.evaluate("selectedPassageId(relation(state.key))")
            self.assertNotEqual(before, after)
            relation_id = composite_id
            relation = composite_relation
            origin_id = page.locator(
                'button[data-relation="%s"]' % relation_id).first.get_attribute(
                    "id")

        selected = page.evaluate("selectedPassageId(relation(state.key))")
        page.keyboard.press("Escape")
        self.assertEqual(page.evaluate("state.mode"), None)
        self.assertEqual(page.evaluate("document.activeElement.id"), origin_id)

        reverse = page.locator(
            'button[data-block="%s"]' % selected).first
        reverse_id = reverse.get_attribute("id")
        reverse.focus()
        page.keyboard.press("Enter")
        reverse_state = page.evaluate("""() => {
          const entry = reverseEntry();
          const current = relation(entry.relationId);
          const owner = paneScrollOwner(claimsPane);
          const target = document.getElementById(current.subjectDomId);
          return {mode:state.mode, focus:document.activeElement.id,
            owner:owner ? owner.id : null, unobscured:unobscured(owner,target)};
        }""")
        self.assertEqual(reverse_state["mode"], "reverse")
        self.assertEqual(reverse_state["focus"], "reverse-bar")
        self.assertTrue(reverse_state["unobscured"])
        if page.evaluate("state.reverseList.length") > 1:
            page.keyboard.press("ArrowRight")
            self.assertEqual(page.evaluate("state.reverseIndex"), 1)
        page.keyboard.press("Escape")
        self.assertEqual(page.evaluate("document.activeElement.id"), reverse_id)

        no_candidate = next((
            identifier for identifier, item in navigation["relations"].items()
            if not item["targets"]), None)
        if no_candidate is not None:
            control = page.locator(
                'button[data-relation="%s"]' % no_candidate).first
            control.focus()
            page.keyboard.press("Enter")
            self.assertEqual(page.evaluate("state.mode"), "forward")
            self.assertEqual(
                page.locator(".highlight-strong").count(), 0)
            page.keyboard.press("Escape")

        if product_kind == "prior-art":
            reader = page.locator("button.reader-jump").first
            target_id = reader.get_attribute("data-reader")
            details_id = reader.get_attribute("data-reader-details")
            reader.focus()
            page.keyboard.press("Enter")
            self.assertTrue(page.locator("#" + details_id).evaluate(
                "node => node.open"))
            self.assertEqual(
                page.evaluate("document.activeElement.id"), target_id)
        else:
            gate = page.locator("button.gate-chip").first
            if gate.count():
                gate_id = gate.get_attribute("id")
                gate.focus()
                page.keyboard.press("Enter")
                self.assertEqual(page.evaluate("state.mode"), "claim-gate")
                self.assertEqual(
                    page.evaluate("document.activeElement.id"), "forward-bar")
                page.keyboard.press("Escape")
                self.assertEqual(
                    page.evaluate("document.activeElement.id"), gate_id)

    def test_shared_contract_is_product_isolated(self):
        self.assertEqual(tuple(self.models), (
            "na-specification", "af-specification",
            "na-prior-art", "af-prior-art"))
        self.assertIn("--type-reading:1.125rem", CSS)
        self.assertIn("--type-interface:.875rem", CSS)
        self.assertIn("--type-auxiliary:.75rem", CSS)
        self.assertIn(
            "max-block-size:%dvh" %
            self.control["presentation"]["maximumChromeViewportPercent"],
            CSS)
        for product_id, artifact in self.artifacts.items():
            with self.subTest(product=product_id):
                model = self.models[product_id]
                navigation = _navigation(artifact)
                self.assertEqual(navigation["productKind"], model.product_kind)
                self.assertNotIn("presentation", navigation)
                self.assertNotIn("typography", navigation)
                rendered_relations = set(navigation["relations"])
                typed_relations = {
                    item.relation_id for item in
                    (*model.relations.mappings, *model.relations.phrase_mappings)
                }
                self.assertEqual(rendered_relations, typed_relations)
                self.assertEqual(artifact.count(CSS), 1)

    def test_all_products_meet_exact_typography_tiers(self):
        for product_id, artifact in self.artifacts.items():
            with self.subTest(product=product_id), \
                    self._page(artifact, 1280, 720) as (page, errors, requests):
                baseline = presentationqa.validate_computed_typography(
                    page, self.control)
                initial = page.locator(".unit-body").first.evaluate(
                    "node => parseFloat(getComputedStyle(node).fontSize)")
                page.evaluate("document.documentElement.style.fontSize='20px'")
                enlarged = presentationqa.validate_computed_typography(
                    page, self.control)
                changed = page.locator(".unit-body").first.evaluate(
                    "node => parseFloat(getComputedStyle(node).fontSize)")
                self.assertTrue(math.isclose(changed / initial, 1.25,
                                             rel_tol=0.01))
                self.assertGreater(enlarged["reading"]["minimumPixels"],
                                   baseline["reading"]["minimumPixels"])
                self.assertEqual(errors, [])
                self.assertEqual(requests, [])

    def test_readable_measure_wrapping_and_scoped_overflow(self):
        for product_id, artifact in self.artifacts.items():
            with self.subTest(product=product_id), \
                    self._page(artifact, 1920, 1080) as (page, errors, requests):
                first = presentationqa.validate_reading_surfaces(
                    page, self.control)
                page.locator("#aux-toggle").click()
                second = presentationqa.validate_reading_surfaces(
                    page, self.control)
                self.assertGreater(first["count"], 0)
                self.assertGreater(second["count"], 0)
                self.assertGreater(second["scopedOverflowCount"], 0)
                self.assertEqual(errors, [])
                self.assertEqual(requests, [])

    def test_baseline_viewport_matrix_is_readable(self):
        for product_id, artifact in self.artifacts.items():
            for width, height, mode, reduced in browserqa.runtime_matrix(
                    self.control):
                label = (product_id, width, height, mode, reduced)
                with self.subTest(vector=label), self._page(
                        artifact, width, height, reduced) as (
                            page, errors, requests):
                    presentationqa.validate_computed_typography(
                        page, self.control)
                    presentationqa.validate_reading_surfaces(
                        page, self.control)
                    self._assert_layout_surface(page)
                    self._assert_aux_surface_reachable(page)
                    self.assertEqual(errors, [])
                    self.assertEqual(requests, [])

    def test_text_resize_and_page_zoom_preserve_functionality(self):
        for product_id, artifact in self.artifacts.items():
            navigation = _navigation(artifact)
            kind = self.models[product_id].product_kind
            with self.subTest(product=product_id, vector="text-resize"), \
                    self._page(artifact, 1280, 720) as (page, errors, requests):
                factor = self.control["presentation"]["textResizeFactor"]
                root = page.evaluate(
                    "parseFloat(getComputedStyle(document.documentElement).fontSize)")
                page.evaluate("value => document.documentElement.style.fontSize = "
                              "String(value) + 'px'", root * factor)
                presentationqa.validate_computed_typography(page, self.control)
                presentationqa.validate_reading_surfaces(page, self.control)
                self._assert_layout_surface(page)
                self._assert_aux_surface_reachable(page)
                self._assert_basic_navigation(page, navigation, kind)
                self.assertEqual(errors, [])
                self.assertEqual(requests, [])
            for width, height, original_width, original_height, reduced in \
                    browserqa.zoom_matrix(self.control):
                label = (product_id, "page-zoom", original_width,
                         original_height, reduced)
                with self.subTest(vector=label), self._page(
                        artifact, width, height, reduced) as (
                            page, errors, requests):
                    presentationqa.validate_computed_typography(
                        page, self.control)
                    presentationqa.validate_reading_surfaces(
                        page, self.control)
                    self._assert_layout_surface(page)
                    self._assert_aux_surface_reachable(page)
                    self._assert_basic_navigation(page, navigation, kind)
                    self.assertEqual(errors, [])
                    self.assertEqual(requests, [])

    def test_reflow_preserves_content_and_positive_geometry(self):
        for product_id, artifact in self.artifacts.items():
            navigation = _navigation(artifact)
            kind = self.models[product_id].product_kind
            for width, height, reduced in browserqa.reflow_matrix(self.control):
                label = (product_id, width, height, reduced)
                with self.subTest(vector=label), self._page(
                        artifact, width, height, reduced) as (
                            page, errors, requests):
                    presentationqa.validate_computed_typography(
                        page, self.control)
                    presentationqa.validate_reading_surfaces(
                        page, self.control)
                    self._assert_layout_surface(page)
                    self._assert_aux_surface_reachable(page)
                    self._assert_basic_navigation(page, navigation, kind)
                    self.assertEqual(errors, [])
                    self.assertEqual(requests, [])

    def test_text_spacing_override_preserves_content_and_controls(self):
        reflow = self.control["presentation"]["reflowViewport"]
        for product_id, artifact in self.artifacts.items():
            navigation = _navigation(artifact)
            kind = self.models[product_id].product_kind
            for width, height in ((1000, 700),
                                  (reflow["width"], reflow["height"])):
                label = (product_id, width, height)
                with self.subTest(vector=label), self._page(
                        artifact, width, height) as (page, errors, requests):
                    presentationqa.validate_text_spacing_adaptation(
                        page, self.control)
                    presentationqa.validate_reading_surfaces(
                        page, self.control)
                    self._assert_layout_surface(page)
                    self._assert_aux_surface_reachable(page)
                    self._assert_basic_navigation(page, navigation, kind)
                    self.assertEqual(errors, [])
                    self.assertEqual(requests, [])

    def test_scaled_navigation_preserves_state_focus_owner_and_geometry(self):
        vectors = ((1000, 700, False), (500, 350, False),
                   (320, 256, False), (320, 256, True))
        for product_id, artifact in self.artifacts.items():
            navigation = _navigation(artifact)
            kind = self.models[product_id].product_kind
            for width, height, reduced in vectors:
                label = (product_id, width, height, reduced)
                with self.subTest(vector=label), self._page(
                        artifact, width, height, reduced) as (
                            page, errors, requests):
                    self._assert_basic_navigation(page, navigation, kind)
                    self.assertEqual(errors, [])
                    self.assertEqual(requests, [])

    def test_no_script_and_print_surfaces_are_readable(self):
        for product_id, artifact in self.artifacts.items():
            with self.subTest(product=product_id, surface="no-script"), \
                    self._page(
                        artifact, 320, 256, java_script_enabled=False) as (
                            page, errors, requests):
                presentationqa.validate_noninteractive_surfaces(
                    page, self.control)
                result = page.evaluate("""() => ({
                  bodyOverflow:getComputedStyle(document.body).overflowY,
                  panesOverflow:getComputedStyle(panes).overflowY,
                  pageOverflow:document.documentElement.scrollWidth >
                    document.documentElement.clientWidth + 1,
                  auxDisplay:getComputedStyle(document.getElementById('aux')).display
                })""")
                self.assertIn(result["bodyOverflow"], {"auto", "visible"})
                self.assertEqual(result["panesOverflow"], "visible")
                self.assertFalse(result["pageOverflow"])
                self.assertEqual(result["auxDisplay"], "block")
                self.assertEqual(errors, [])
                self.assertEqual(requests, [])

            with self.subTest(product=product_id, surface="print"), \
                    self._page(artifact, 1280, 720) as (page, errors, requests):
                page.emulate_media(media="print")
                presentationqa.validate_noninteractive_surfaces(
                    page, self.control)
                print_state = page.evaluate("""() => {
                  const footer = document.querySelector('footer');
                  return {
                    footerDisplay:getComputedStyle(footer).display,
                    footerClipped:footer.scrollHeight > footer.clientHeight + 1 ||
                      footer.scrollWidth > footer.clientWidth + 1,
                    footerClient:[footer.clientWidth,footer.clientHeight],
                    footerScroll:[footer.scrollWidth,footer.scrollHeight],
                    auxDisplay:getComputedStyle(document.getElementById('aux')).display,
                    bodyOverflow:getComputedStyle(document.body).overflowY
                  };
                }""")
                self.assertEqual(print_state["footerDisplay"], "block")
                self.assertFalse(print_state["footerClipped"], print_state)
                self.assertEqual(print_state["auxDisplay"], "block")
                self.assertEqual(print_state["bodyOverflow"], "visible")
                pdf = page.pdf(format="A4", print_background=True)
                self.assertTrue(pdf.startswith(b"%PDF-"))
                self.assertEqual(errors, [])
                self.assertEqual(requests, [])


if __name__ == "__main__":
    unittest.main()
