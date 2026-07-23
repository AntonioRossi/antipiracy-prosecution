"""Focused regressions for renderer and UI hardening.

These tests intentionally live outside the acceptance registry: they pin bugs
found while auditing the implementation against the TDD without changing the
meaning or traceability of AC-01 … AC-20.
"""

from html.parser import HTMLParser
import copy
import json
import os
import re
import subprocess
import sys
import unittest
from types import SimpleNamespace


sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib import gateway, model, projections, render  # noqa: E402
if __package__:
    from .test_acceptance import run_api_probe_harness  # noqa: E402
else:
    # ``unittest discover -s navigator/tests`` imports test modules at the
    # top level, while module-qualified runs import this package relatively.
    from test_acceptance import run_api_probe_harness  # noqa: E402


HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
EDITIONS = ("na", "af")
_CACHE = {}


def get_model(edition_id):
    key = (edition_id, "model")
    if key not in _CACHE:
        boot = gateway.ContentGateway(ROOT)
        path = "navigator/editions/%s.json" % edition_id
        config = json.loads(boot.read_text(path))
        content = gateway.ContentGateway(
            ROOT, allowlist=config["declaredTransitiveInputs"])
        _CACHE[key] = model.EditionModel(content, path)
    return _CACHE[key]


def get_html(edition_id):
    key = (edition_id, "html")
    if key not in _CACHE:
        _CACHE[key] = render.render(get_model(edition_id)).decode("utf-8")
    return _CACHE[key]


def nav_data(html):
    payload = re.search(
        r'<script type="application/json" id="nav-data">(.*?)</script>',
        html, re.S)
    if payload is None:
        raise AssertionError("rendered artifact has no navigation data")
    return json.loads(payload.group(1))


class _ButtonParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.buttons = []

    def handle_starttag(self, tag, attrs):
        if tag == "button":
            self.buttons.append(dict(attrs))


class UIRegressions(unittest.TestCase):
    maxDiff = None

    def test_reverse_index_lists_all_units_before_phrases_per_claim(self):
        target = lambda: {"block": "S001"}
        ship = {"fragments": {
            "c1u1": {"targets": [target()], "phrases": [
                {"id": "c1u1p10", "targets": [target()]},
                {"id": "c1u1p2", "targets": [target()]},
            ]},
            "c1u2": {"targets": [target()], "phrases": [
                {"id": "c1u2p1", "targets": [target()]},
            ]},
            "c2u1": {"targets": [target()]},
        }}
        self.assertEqual(
            [entry["fragment"] for entry in
             projections.reverse_index(ship)["S001"]],
            ["c1u1", "c1u2", "c1u1p2", "c1u1p10", "c1u2p1", "c2u1"])

    def test_claim_gate_quotations_are_embedded(self):
        for edition_id in EDITIONS:
            m = get_model(edition_id)
            ship = projections.ship_relation(m)
            quotes = projections.quotable_texts(m, ship)
            gates = [gate for claim_gates in
                     ship.get("claimGates", {}).values()
                     for gate in claim_gates]
            self.assertTrue(gates, edition_id)
            for gate in gates:
                block = gate["source"]["block"]
                self.assertIn(block, quotes, (edition_id, gate["gateId"]))
                self.assertEqual(
                    quotes[block], m.quotable_anchor(block).block.canonical)

            embedded = nav_data(get_html(edition_id))["quotes"]
            for gate in gates:
                self.assertEqual(embedded[gate["source"]["block"]],
                                 quotes[gate["source"]["block"]])

    def test_reverse_and_claim_gate_triggers_have_stable_focus_ids(self):
        for edition_id in EDITIONS:
            parser = _ButtonParser()
            parser.feed(get_html(edition_id))
            reverse = [b for b in parser.buttons
                       if "rev-badge" in b.get("class", "").split()]
            claim_gates = [b for b in parser.buttons
                           if "gate-chip" in b.get("class", "").split()]
            self.assertTrue(reverse, edition_id)
            self.assertTrue(claim_gates, edition_id)

            ids = []
            for button in reverse:
                expected = "btn-rev-%s" % button["data-block"]
                self.assertEqual(button.get("id"), expected)
                ids.append(button["id"])
            for button in claim_gates:
                expected = "btn-gate-%s-%s" % (
                    button["data-claim"], button["data-gate"])
                self.assertEqual(button.get("id"), expected)
                ids.append(button["id"])
            self.assertEqual(len(ids), len(set(ids)), edition_id)

        self.assertIn("activateReverse(b.dataset.block, b.id)", render.JS)
        self.assertIn(
            "activateGate(b.dataset.claim, b.dataset.gate, b.id)", render.JS)
        self.assertIn("document.getElementById(rf)", render.JS)

    def test_counsel_review_forward_bar_can_clear_and_shows_disposition(self):
        controls_start = render.JS.index("function selectionControls")
        controls_end = render.JS.index("\nfunction cautionChip", controls_start)
        controls = render.JS[controls_start:controls_end]
        forward_start = render.JS.index("function renderForwardBar")
        forward_end = render.JS.index(
            "\nfunction applyForwardHighlights", forward_start)
        forward = render.JS[forward_start:forward_end]

        script = r"""
var DATA = {strings: {
  ui: {forwardMode:'forward', noCandidateNotice:'review required',
       previous:'previous', next:'next', clearSelection:'clear'},
  dispositions: {'carried-at-required-scope':'neutral disposition'}
}, unitLabels: {'c1u0':'NA claim 1 · limitation 1'}};
function el(tag, cls, text){
  return {tag:tag, className:cls || '', textContent:text || '', hidden:false,
    children:[], appendChild:function(child){ this.children.push(child); }};
}
function btn(cls, label, text, fn){
  var node = el('button', cls, text); node.label = label; node.click = fn;
  return node;
}
function move(){}
function clearSelection(){}
function cautionChip(){ throw new Error('unexpected caution'); }
var NavModel = {claimGates:function(){ return []; }};
var fbar = el('div');
var state = {key:'c1u0', info:{status:'counsel-review-required', targets:[],
  dispositions:[{gateId:'g1', disposition:'carried-at-required-scope'}]}};
%s
%s
renderForwardBar();
function view(node){ return {text:node.textContent, cls:node.className,
  children:node.children.map(view)}; }
process.stdout.write(JSON.stringify(view(fbar)));
""" % (controls, forward)
        completed = subprocess.run(
            ["node", "-e", script], capture_output=True, text=True,
            timeout=30)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        bar = json.loads(completed.stdout)
        self.assertIn("review required", [c["text"] for c in bar["children"]])
        self.assertIn("neutral disposition",
                      [c["text"] for c in bar["children"]])
        controls_node = next(
            c for c in bar["children"] if c["cls"] == "selection-controls")
        self.assertEqual([c["text"] for c in controls_node["children"]], ["×"])

    def test_claim_gate_focus_does_not_enter_empty_candidate_cycle(self):
        start = render.JS.index("function activateGate")
        functions = render.JS[start:]
        script = r"""
var listeners = {};
var document = {
  activeElement: null,
  addEventListener: function(kind, fn){ listeners[kind] = fn; }
};
function node(){ return {
  children: [], hidden: true, textContent: '',
  appendChild: function(child){ this.children.push(child); },
  setAttribute: function(){},
  focus: function(){ document.activeElement = this; },
  contains: function(other){ return other === this; }
}; }
var fbar = node(), rbar = node();
var state = {mode:null};
var DATA = {
  edition:{prefix:'NA'},
  claimGates:{c1:[{gateId:'g1'}]},
  claimDispositions:{c1:[]},
  strings:{ui:{forwardMode:'forward',claimGateContext:'{prefix} claim {n}',
    clearSelection:'clear',claimGateAnnouncement:'{prefix} claim {n}',
    gatePresent:'gate'},dispositions:{}}
};
function clearSelection(){}
function el(tag, cls, value){ var n=node(); n.textContent=value || ''; return n; }
function btn(){ return node(); }
function fmt(value, fields){ Object.keys(fields).forEach(function(key){
  value=value.split('{'+key+'}').join(String(fields[key])); }); return value; }
function cautionChip(){ return node(); }
function say(){}
function move(){ throw new Error('claim gate entered candidate cycling'); }
%s
activateGate('c1', 'g1', 'btn-gate-c1-g1');
var prevented = false;
listeners.keydown({key:'ArrowRight', preventDefault:function(){prevented=true;}});
process.stdout.write(JSON.stringify({mode:state.mode, prevented:prevented}));
""" % functions
        completed = subprocess.run(
            ["node", "-e", script], capture_output=True, text=True,
            timeout=30)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout), {
            "mode": "claim-gate", "prevented": False})

    def test_template_substitution_is_single_pass(self):
        template = "<title>@@TITLE@@</title><main>@@BODY@@</main>"
        result = render.substitute_template(template, {
            "@@TITLE@@": "safe title",
            "@@BODY@@": "authored @@TITLE@@ token",
        })
        self.assertEqual(
            result,
            "<title>safe title</title><main>authored @@TITLE@@ token</main>")
        with self.assertRaisesRegex(ValueError, "@@BODY@@"):
            render.substitute_template(template, {"@@TITLE@@": "safe"})

    def test_flat_schedule_escapes_target_label_and_block_id(self):
        label = '<img src=x onerror="label">'
        block = 'S1"><script>alert("block")</script>'
        role = '<img src=x onerror="role">'
        unit = SimpleNamespace(id="c1u0", label="limitation 1")
        claim = SimpleNamespace(number=1, units=[unit])
        m = SimpleNamespace(
            edition={"strategyPrefix": "NA", "stringsNamespace": "test"},
            strings={
                "editionNamespaces": {"test": {"sourceGateCodes": {}}},
                "generalizationCodes": {},
            },
            claims=[claim],
            target_anchor=lambda unused: SimpleNamespace(label=label),
        )
        ship = {"fragments": {"c1u0": {
            "status": "mapped", "targets": [{"block": block, "note": "note"}]
        }}}
        strings = copy.deepcopy(get_model("na").strings)
        strings["role"]["specific"] = role
        ship["fragments"]["c1u0"]["targets"][0]["role"] = "specific"
        schedule = render._schedule(m, ship, strings)
        self.assertNotIn(label, schedule)
        self.assertNotIn(block, schedule)
        self.assertNotIn(role, schedule)
        self.assertIn(render.esc(label), schedule)
        self.assertIn(render.esc(block), schedule)
        self.assertIn(render.esc(role), schedule)

    def test_csp_is_escaped_in_its_html_attribute(self):
        m = copy.copy(get_model("na"))
        m.api_policy = copy.deepcopy(m.api_policy)
        payload = 'default-src none" onload="alert(1)'
        m.api_policy["csp"] = payload
        html = render.render(m).decode("utf-8")
        self.assertNotIn('content="%s"' % payload, html)
        self.assertIn('content="%s"' % render.esc(payload), html)

    def test_api_probe_labels_and_classes_are_policy_derived(self):
        m = copy.copy(get_model("na"))
        m.api_policy = copy.deepcopy(m.api_policy)
        m.api_policy["apis"]["indexedDB.open"]["instrument"] = "db-marker"
        html = render.render(m).decode("utf-8")
        payload = re.search(
            r'<script type="application/json" id="api-probes">(.*?)</script>',
            html, re.S)
        self.assertIsNotNone(payload)
        probes = json.loads(payload.group(1))
        self.assertEqual(probes["indexedDB.open"], "db-marker")
        self.assertEqual(
            probes["history.pushState"], "navigation-mutation")
        for api in ("fetch", "XMLHttpRequest", "WebSocket", "EventSource"):
            self.assertNotIn(api, probes)
        self.assertIn(
            "window.IDBFactory && window.IDBFactory.prototype", render.JS)
        self.assertIn("var api = 'document.cookie'", render.JS)
        self.assertIn("var cookieName = policyInstrument(api)", render.JS)
        self.assertIn("window.__apiProbeStatus", render.JS)
        self.assertIn("failed(api, 'installer-not-invoked')", render.JS)
        self.assertIn("throw new Error('API probe installation failed:",
                      render.JS)
        for api in probes:
            self.assertIn("'%s'" % api, render.JS,
                          "no runtime hook for %s" % api)

        policy = copy.deepcopy(m.api_policy)
        policy["apis"]["new.probe"] = {
            "class": "probed", "instrument": "new-marker"}
        with self.assertRaisesRegex(ValueError, "new.probe"):
            render.api_probe_instruments(policy)

    def test_api_probe_installation_ledger_fails_closed_behaviorally(self):
        m = get_model("na")
        html = get_html("na")
        js = html.split("<script>")[-1].split("</script>")[0]
        probe = js.split("})();", 1)[0] + "})();"
        registered = render.api_probe_instruments(m.api_policy)
        behavior_policy = {
            api: "probe:" + api for api in sorted(registered)}

        success = run_api_probe_harness(probe, behavior_policy, "success")
        self.assertIsNone(success["thrown"], success)
        self.assertEqual(success["status"]["expected"], sorted(registered))
        self.assertEqual(sorted(success["status"]["hooks"]),
                         sorted(registered))
        self.assertTrue(success["status"]["ready"], success)
        self.assertEqual(success["before"], [])
        self.assertGreater(len(success["after"]), 0)
        self.assertEqual(success["deltas"], {
            api: [behavior_policy[api]] for api in (
                "navigator.sendBeacon", "history.pushState",
                "history.replaceState", "window.localStorage",
                "window.sessionStorage", "indexedDB.open",
                "document.cookie",
            )
        })

        failures = (
            ("nonwritable-function", "history.pushState", "push",
             "installation-threw"),
            ("getter-failure", "window.localStorage", "localGet",
             "installation-threw"),
            ("cookie-failure", "document.cookie", "cookieWrite",
             "descriptor-not-configurable"),
        )
        for scenario, api, counter, expected_error in failures:
            with self.subTest(scenario=scenario):
                result = run_api_probe_harness(
                    probe, behavior_policy, scenario)
                self.assertFalse(result["status"]["ready"], result)
                hook = result["status"]["hooks"][api]
                self.assertEqual(hook["status"], "failed")
                self.assertEqual(hook["error"], expected_error)
                if expected_error == "installation-threw":
                    self.assertTrue(hook["detail"])
                self.assertIn("API probe installation failed",
                              result["thrown"])
                self.assertEqual(result["before"], [])
                self.assertEqual(result["after"], [])
                self.assertEqual(result["deltas"], {api: []})
                self.assertEqual(result["calls"][counter], 1)

    def test_responsive_breakpoint_and_note_come_from_support_matrix(self):
        m = copy.copy(get_model("na"))
        m.support_matrix = copy.deepcopy(m.support_matrix)
        m.support_matrix["viewport"]["minimum"] = [1024, 600]
        html = render.render(m).decode("utf-8")
        self.assertIn("(max-width:1023px),(max-height:599px)", html)
        self.assertIn("viewports of 1024×600 and above", html)

        m.support_matrix["viewport"]["stackedBelowMinimum"] = False
        with self.assertRaisesRegex(ValueError, "require stacking"):
            render.render(m)

    def test_print_has_one_nonoverlapping_repeating_legend_block(self):
        self.assertIn("@page { margin:12mm 10mm; }", render.CSS)
        reserve = re.search(
            r"#content-root \{ display:block; overflow:visible; "
            r"padding-bottom:(\d+)mm;[^}]*"
            r"-webkit-box-decoration-break:clone; "
            r"box-decoration-break:clone;",
            render.CSS)
        self.assertIsNotNone(reserve)
        self.assertIn(
            "#masthead > .legend,#masthead > .disclaimer { display:none; }",
            render.CSS)
        self.assertRegex(
            render.CSS,
            r"footer \{ position:fixed; top:auto; bottom:0;[^}]*"
            r"height:(\d+)mm;"
            r" min-height:0; overflow:hidden;[^}]*transform:none;")
        footer_height = int(re.search(
            r"footer \{[^}]*height:(\d+)mm;", render.CSS).group(1))
        self.assertGreater(int(reserve.group(1)), footer_height)
        self.assertNotIn("transform:translateY", render.CSS)
        self.assertNotIn("bottom:-", render.CSS)
        self.assertIn(
            "footer .legend,footer .disclaimer { position:static", render.CSS)
        self.assertNotIn(".legend { position:fixed", render.CSS)
        self.assertIn("button:not(.phrase-btn)", render.CSS)
        self.assertIn(".phrase-btn { border:none", render.CSS)
        self.assertRegex(
            render.HTML_TEMPLATE,
            r"<footer><p class=\"legend\">@@LEGEND@@</p>"
            r"<p class=\"disclaimer\">@@DISCLAIMER@@</p></footer>")
        self.assertGreater(render.HTML_TEMPLATE.index("<footer>"),
                           render.HTML_TEMPLATE.index('</div>\n</div>'))
        self.assertLess(render.HTML_TEMPLATE.index("<footer>"),
                        render.HTML_TEMPLATE.index("<noscript>"))

    def test_nojs_uses_a_reachable_combined_scroll_owner(self):
        nojs = re.search(r"<noscript><style>(.*?)</style></noscript>",
                         render.HTML_TEMPLATE, re.S)
        self.assertIsNotNone(nojs)
        css = re.sub(r"\s+", "", nojs.group(1))
        self.assertIn(
            "#content-root{display:block;overflow-y:auto;min-height:0;",
            css)
        self.assertIn("#aux{display:block}", css)
        self.assertIn("#aux-toggle{display:none}", css)
        self.assertIn("#content-root{flex:11auto;display:flex;",
                      re.sub(r"\s+", "", render.CSS))

    def test_noncolor_state_and_hit_target_regressions(self):
        compact = re.sub(r"\s+", " ", render.CSS)
        self.assertRegex(
            compact, r"\.hl-frag-soft \{[^}]*outline:2px dotted")
        self.assertRegex(compact, r"\.unit-btn \{[^}]*width:24px;")

    def test_preview_watermark_wording_has_one_registry_display_path(self):
        self.assertNotIn("content:\"PREVIEW", render.CSS)
        m = copy.copy(get_model("na"))
        m.strings = copy.deepcopy(m.strings)
        marker = "CENTRAL PREVIEW MARKER"
        m.strings["ui"]["previewWatermark"] = marker
        html = render.render(m, mode="preview").decode("utf-8")
        self.assertIn(
            '<div class="watermark" aria-hidden="true"><span>%s</span></div>'
            % marker, html)

    def test_reverse_and_gate_accessible_names_include_context(self):
        for edition_id in EDITIONS:
            parser = _ButtonParser()
            parser.feed(get_html(edition_id))
            scoped = [b for b in parser.buttons if
                      "rev-badge" in b.get("class", "").split() or
                      "gate-chip" in b.get("class", "").split()]
            labels = [b.get("aria-label") for b in scoped]
            self.assertTrue(all(labels), edition_id)
            self.assertEqual(len(labels), len(set(labels)), edition_id)

    def test_caution_presence_tracks_current_target_and_expansion_state(self):
        self.assertIn("currentTarget !== undefined", render.JS)
        self.assertIn("presenceText(state.info, state.key, t)", render.JS)
        self.assertIn("chip.setAttribute('aria-expanded', 'false')", render.JS)
        self.assertIn("chip.setAttribute('aria-expanded', 'true')", render.JS)

        start = render.JS.index("function presenceText")
        end = render.JS.index("\nfunction clearHighlights", start)
        fn = render.JS[start:end]
        script = r"""
var DATA = {strings:{ui:{cautionPresent:'CAUTION',gatePresent:'GATE'}},
  claimGates:{}};
var NavModel = {claimOf:function(){ return 'c1'; }};
%s
var info = {caution:null, targets:[{block:'S1'},{block:'S2',caution:{}}]};
process.stdout.write(JSON.stringify({
  first:presenceText(info,'c1u0',info.targets[0]),
  second:presenceText(info,'c1u0',info.targets[1]),
  reverse:presenceText(info,'c1u0')
}));
""" % fn
        completed = subprocess.run(
            ["node", "-e", script], capture_output=True, text=True,
            timeout=30)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["first"], "")
        self.assertIn("CAUTION", result["second"])
        self.assertIn("CAUTION", result["reverse"])

    def test_registered_claim_and_unit_labels_drive_rendering(self):
        m = copy.copy(get_model("na"))
        m.strings = copy.deepcopy(m.strings)
        m.strings["ui"]["claimReference"] = "{prefix} CLAIM-{n}"
        m.strings["ui"]["preambleLabel"] = "INTRO"
        m.strings["ui"]["limitationLabel"] = "STEP {n}"
        m.strings["ui"]["authorityHeader"] = "AUTHORITY MARKER"
        html = render.render(m).decode("utf-8")
        self.assertIn('<span class="claim-no">NA CLAIM-1</span>', html)
        self.assertIn('<span class="unit-label">INTRO</span>', html)
        self.assertIn('<span class="unit-label">STEP 1</span>', html)
        self.assertIn("AUTHORITY MARKER", html)

    def test_counsel_review_controls_name_their_status(self):
        for edition_id in EDITIONS:
            parser = _ButtonParser()
            parser.feed(get_html(edition_id))
            buttons = {b.get("id"): b for b in parser.buttons}
            ship = projections.ship_relation(get_model(edition_id))
            checked = 0
            for fragment_id, fragment in ship["fragments"].items():
                if fragment["status"] == "counsel-review-required":
                    self.assertIn(
                        "counsel review required",
                        buttons["btn-" + fragment_id]["aria-label"].lower())
                    checked += 1
                for phrase in fragment.get("phrases", []):
                    if phrase["status"] == "counsel-review-required":
                        self.assertIn(
                            "counsel review required",
                            buttons["btn-" + phrase["id"]]["aria-label"].lower())
                        checked += 1
            self.assertGreater(checked, 0, edition_id)

    def test_more_than_five_indicator_branch_is_static_and_counted(self):
        controls_start = render.JS.index("function selectionControls")
        controls_end = render.JS.index("\nfunction cautionChip", controls_start)
        controls = render.JS[controls_start:controls_end]
        forward_start = render.JS.index("function renderForwardBar")
        forward_end = render.JS.index(
            "\nfunction applyForwardHighlights", forward_start)
        forward = render.JS[forward_start:forward_end]
        script = r"""
var DATA = {strings:{ui:{forwardMode:'forward',previous:'previous',
  next:'next',clearSelection:'clear',moreCandidates:'+{n} more'},
  role:{},dispositions:{}}, unitLabels:{c1u0:'context'}, anchors:{S1:'one'}};
function el(tag, cls, text){ return {tag:tag,className:cls || '',
  textContent:text || '',hidden:false,children:[],
  appendChild:function(child){this.children.push(child);}}; }
function btn(cls,label,text,fn){var n=el('button',cls,text);n.click=fn;return n;}
function fmt(t,v){Object.keys(v).forEach(function(k){
  t=t.split('{'+k+'}').join(String(v[k]));});return t;}
function positionText(p,total,label){return p+' of '+total+': '+label;}
function move(){} function clearSelection(){}
function cautionChip(){throw new Error('unexpected caution');}
var NavModel={claimGates:function(){return [];}};
var fbar=el('div');
var state={key:'c1u0',pos:0,info:{status:'mapped',dispositions:[],targets:[
  {block:'S1'},{block:'S2'},{block:'S3'},{block:'S4'},
  {block:'S5'},{block:'S6'},{block:'S7'}]}};
%s
%s
renderForwardBar();
var more=fbar.children.filter(function(n){return n.className==='more';})[0];
process.stdout.write(JSON.stringify(more));
""" % (controls, forward)
        completed = subprocess.run(
            ["node", "-e", script], capture_output=True, text=True,
            timeout=30)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        more = json.loads(completed.stdout)
        self.assertEqual(more["tag"], "span")
        self.assertEqual(more["textContent"], "+2 more")

    def test_guidance_and_editorial_labels_follow_source_semantics(self):
        af = get_html("af")
        group = af.index("<h2>Priority-gated production fallbacks</h2>")
        guidance = af.index('<aside class="guidance-note"', group)
        claim_2 = af.index('id="claim-2"', group)
        self.assertLess(group, guidance)
        self.assertLess(guidance, claim_2)

        for edition_id in EDITIONS:
            m = get_model(edition_id)
            html = get_html(edition_id)
            headings = [b for b in m.target_blocks
                        if b.kind == "heading" and b.cls == "editorial"]
            self.assertTrue(headings, edition_id)
            for heading in headings:
                match = re.search(
                    r'<h\d class="dblock" id="%s">(.*?)</h\d>' %
                    re.escape(heading.id), html, re.S)
                self.assertIsNotNone(match, (edition_id, heading.id))
                self.assertIn('class="editorial-tag"', match.group(1))

            captions = re.findall(
                r'<caption class="tcaption">(.*?)</caption>', html, re.S)
            self.assertTrue(captions, edition_id)
            for caption in captions:
                self.assertNotIn("editorial-tag", caption)
            self.assertNotIn('<p class="tcaption">', html)
            self.assertEqual(html.count("<figcaption"), 4)
            self.assertEqual(html.count("aria-describedby=\"S"), 4)


if __name__ == "__main__":
    unittest.main()
