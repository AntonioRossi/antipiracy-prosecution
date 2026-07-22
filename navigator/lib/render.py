"""Artifact renderer — one self-contained HTML5 file per edition (TDD
§§4–6, 11–13). Everything inlined; all source-derived text escaped for its
context; embedded JSON script-safe-escaped; no untrusted innerHTML in the
page script (it builds DOM via textContent only).
"""

import base64
import json

from . import projections

CSP = ("default-src 'none'; img-src data:; style-src 'unsafe-inline'; "
       "script-src 'unsafe-inline'; base-uri 'none'; form-action 'none'; "
       "object-src 'none'; connect-src 'none'")


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def md_inline(s):
    """Escape, then minimal markdown: **bold** and `code` only."""
    out = esc(s)
    parts = out.split("**")
    if len(parts) % 2 == 1:
        out = ""
        for i, p in enumerate(parts):
            out += p if i % 2 == 0 else "<strong>%s</strong>" % p
    parts = out.split("`")
    if len(parts) % 2 == 1:
        out = ""
        for i, p in enumerate(parts):
            out += p if i % 2 == 0 else "<code>%s</code>" % p
    return out


def script_json(obj):
    """JSON for embedding inside <script> — escapes </script sequences."""
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")) \
        .replace("<", "\\u003c").replace(" ", "\\u2028") \
        .replace(" ", "\\u2029")


def _unit_html(prefix, claim, unit, frag, strings):
    fid = unit.id
    label = "%s claim %d · %s" % (prefix, claim.number, unit.label)
    phrases = frag.get("phrases", [])
    spans = []
    for ph in phrases:
        import re as _re
        pos = [mm.start() for mm in
               _re.finditer(_re.escape(ph["text"]), unit.text)]
        if len(pos) >= ph["occurrence"] >= 1:
            start = pos[ph["occurrence"] - 1]
            spans.append((start, start + len(ph["text"]), ph))
    spans.sort()
    text_html, cur = [], 0
    for start, end, ph in spans:
        text_html.append(esc(unit.text[cur:start]))
        marker = "" if ph["status"] == "mapped" else \
            ' <span class="crr-dot" title="%s">◇</span>' % \
            esc(strings["status"]["counsel-review-required"])
        text_html.append(
            '<button type="button" class="phrase-btn" id="btn-%s" '
            'data-frag="%s" aria-label="%s · &quot;%s&quot;">%s</button>%s'
            % (ph["id"], ph["id"], esc(label), esc(ph["text"]),
               esc(ph["text"]), marker))
        cur = end
    text_html.append(esc(unit.text[cur:]))
    status = frag["status"]
    marker = ""
    if status == "counsel-review-required":
        marker = ('<p class="crr-note" role="note">◇ %s</p>'
                  % esc(strings["status"]["counsel-review-required"]))
    return (
        '<div class="unit status-%s" id="u-%s" data-frag="%s">'
        '<button type="button" class="unit-btn" id="btn-%s" data-frag="%s" '
        'aria-label="%s — show recorded candidate passages"></button>'
        '<div class="unit-body"><span class="unit-label">%s</span>'
        '<span class="pointer-surface" data-frag="%s">%s</span>%s</div></div>'
        % (status, fid, fid, fid, fid, esc(label),
           esc(unit.label), fid, "".join(text_html), marker))


def _claims_pane(m, ship, strings):
    prefix = m.edition["strategyPrefix"]
    gate_codes = m.strings["editionNamespaces"][
        m.edition["stringsNamespace"]]["sourceGateCodes"]
    independents = set(m.edition["independentClaims"])
    groups, order = {}, []
    for c in m.claims:
        if c.group not in groups:
            groups[c.group] = []
            order.append(c.group)
        groups[c.group].append(c)
    chips, sections = [], []
    for g in order:
        chips.append('<span class="chip-group"><span class="chip-group-name">%s</span>'
                     % esc(g))
        for c in groups[g]:
            cls = "chip chip-ind" if c.number in independents else "chip"
            chips.append(
                '<button type="button" class="%s" data-goto="claim-%d" '
                'aria-label="Go to %s claim %d">%d</button>'
                % (cls, c.number, esc(prefix), c.number, c.number))
        chips.append("</span>")
        body = ['<section class="claim-group"><h2>%s</h2>' % esc(g)]
        for c in groups[g]:
            ckey = "c%d" % c.number
            gates = ship.get("claimGates", {}).get(ckey, [])
            gate_html = "".join(
                '<button type="button" class="gate-chip" data-gate="%s" '
                'data-claim="%s" aria-label="Claim-level gate: %s">⚑ %s</button>'
                % (esc(gt["gateId"]), ckey, esc(gate_codes[gt["code"]]),
                   esc(gate_codes[gt["code"]]))
                for gt in gates)
            ind = " claim-independent" if c.number in independents else ""
            body.append(
                '<article class="claim%s" id="claim-%d">'
                '<header class="claim-header"><span class="claim-no">%s claim %d'
                '</span>%s</header>' % (ind, c.number, esc(prefix), c.number,
                                        gate_html))
            for u in c.units:
                body.append(_unit_html(prefix, c, u,
                                       ship["fragments"][u.id], strings))
            body.append("</article>")
        # AF priority-gate blockquote renders as a labeled guidance note in
        # its §3 position (profile-designated quotable, never claim text)
        for b in m.guidance_blocks:
            if b.kind == "note" and b.cls == "quotable" and \
                    len(b.path) >= 3 and b.path[-1] == g:
                body.append(
                    '<aside class="guidance-note" role="note">'
                    '<span class="editorial-tag">%s</span>%s</aside>'
                    % (esc(strings["ui"]["guidanceNoteLabel"]),
                       md_inline(b.canonical)))
        body.append("</section>")
        sections.append("".join(body))
    return ('<div class="claim-strip" role="navigation" '
            'aria-label="Claim index">%s</div>%s'
            % ("".join(chips), "".join(sections)))


def _disclosure_pane(m, reverse, figures_b64, strings):
    out = []
    blocks = [b for b in m.target_blocks if b.id.startswith("S")]
    in_list = False
    claim_open = None

    def badge(bid):
        n = len(reverse.get(bid, []))
        if not n:
            return ""
        return ('<button type="button" class="rev-badge" data-block="%s" '
                'aria-label="%s">◂ %d</button>'
                % (bid, esc(strings["ui"]["indexedBy"].replace("{n}", str(n))),
                   n))

    def margin(b):
        return ('<span class="anchor-label" aria-hidden="true">%s</span>'
                % b.id)

    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    def close_claim():
        nonlocal claim_open
        if claim_open is not None:
            out.append("</div>")
            claim_open = None

    for b in blocks:
        if b.kind != "list-item" and b.kind != "claim-element":
            close_list()
        if b.kind in ("heading",) or (b.meta.get("pctClaim") and
                                      claim_open != b.meta.get("pctClaim") and
                                      b.kind == "claim-head"):
            close_claim()
        ed = ('<span class="editorial-tag">%s</span>'
              % esc(strings["ui"]["editorialLabel"])) if b.cls == "editorial" else ""
        if b.kind == "heading":
            depth = min(len(b.path), 4)
            out.append('<h%d class="dblock" id="%s">%s%s%s</h%d>'
                       % (depth, b.id, margin(b), esc(b.text), badge(b.id), depth))
        elif b.kind == "claim-head":
            num = b.meta["pctClaim"]
            out.append('<div class="pct-claim" id="PC%d">' % num)
            claim_open = num
            out.append('<p class="dblock claim-head" id="%s">%s%s%s%s</p>'
                       % (b.id, margin(b), md_inline(b.text), badge(b.id),
                          badge("PC%d" % num)))
        elif b.kind == "claim-element":
            if not in_list:
                out.append('<ul class="claim-elements">')
                in_list = True
            out.append('<li class="dblock" id="%s">%s%s%s</li>'
                       % (b.id, margin(b), md_inline(b.text), badge(b.id)))
        elif b.kind == "list-item":
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append('<li class="dblock" id="%s">%s%s%s</li>'
                       % (b.id, margin(b), md_inline(b.text), badge(b.id)))
        elif b.kind == "code":
            out.append('<pre class="dblock" id="%s">%s%s<code>%s</code></pre>'
                       % (b.id, margin(b), badge(b.id), esc(b.canonical)))
        elif b.kind == "table":
            rows = [b.meta["header"]] if b.meta.get("header") else []
            out.append('<div class="tablewrap dblock" id="%s">%s%s<table>'
                       % (b.id, margin(b), badge(b.id)))
            if rows:
                out.append("<thead><tr><th></th>%s</tr></thead>" % "".join(
                    "<th>%s</th>" % md_inline(c) for c in b.meta["header"]))
            out.append("<tbody>")
            for r in b.rows:
                rid = "%s.%s" % (b.id, r["id"])
                out.append(
                    '<tr id="%s"><td class="rowmeta">'
                    '<span class="anchor-label" aria-hidden="true">%s</span>%s</td>%s</tr>'
                    % (rid, rid, badge(rid),
                       "".join("<td>%s</td>" % md_inline(c) for c in r["cells"])))
            out.append("</tbody></table>")
            if b.meta.get("caption"):
                out.append('<p class="tcaption"><span class="editorial-tag">%s'
                           '</span>%s</p>'
                           % (esc(strings["ui"]["editorialLabel"]),
                              esc(b.meta["caption"])))
            out.append("</div>")
        elif b.kind == "figure":
            data = figures_b64[b.meta["file"]]
            out.append(
                '<figure class="dblock" id="%s">%s%s'
                '<img src="data:image/png;base64,%s" alt="%s"></figure>'
                % (b.id, margin(b), badge(b.id), data, esc(b.label)))
        elif b.kind == "figure-caption":
            out.append('<p class="dblock editorial" id="%s">%s%s%s</p>'
                       % (b.id, margin(b), ed, md_inline(b.text)))
        elif b.kind in ("note",):
            out.append('<blockquote class="dblock editorial" id="%s">%s%s%s'
                       '</blockquote>'
                       % (b.id, margin(b), ed, md_inline(b.text)))
        elif b.kind == "footer":
            out.append('<p class="dblock editorial filing-footer" id="%s">%s%s%s</p>'
                       % (b.id, margin(b), ed, md_inline(b.text)))
        else:  # paragraph
            cls = "dblock editorial" if b.cls == "editorial" else "dblock"
            out.append('<p class="%s" id="%s">%s%s%s%s</p>'
                       % (cls, b.id, margin(b), ed, md_inline(b.text), badge(b.id)))
    close_list()
    close_claim()
    return "".join(out)


def _schedule(m, ship_schedule, strings):
    """Flat mapping schedule — static markup, printable, lists ALL
    candidates including rationale (schedule-only axis)."""
    prefix = m.edition["strategyPrefix"]
    gate_codes = m.strings["editionNamespaces"][
        m.edition["stringsNamespace"]]["sourceGateCodes"]
    rows = []

    def target_cell(t):
        parts = ["%s (%s)" % (m.target_anchor(t["block"]).label, t["block"])]
        if t.get("role"):
            parts.append("[%s]" % strings["role"][t["role"]])
        parts.append(esc(t["note"]))
        if t.get("rationale"):
            parts.append("<em>%s</em>" % esc(t["rationale"]))
        if t.get("caution"):
            c = t["caution"]
            name = gate_codes.get(c["code"]) if c["type"] == "source-gate" \
                else m.strings["generalizationCodes"].get(c["code"], c["code"])
            parts.append('<span class="sched-caution">⚑ %s</span>' % esc(name))
        return " · ".join(parts)

    for c in m.claims:
        for u in c.units:
            frag = ship_schedule["fragments"][u.id]
            label = "%s claim %d · %s" % (prefix, c.number, u.label)
            tcells = "<br>".join(target_cell(t) for t in frag.get("targets", []))
            extra = []
            if frag.get("caution"):
                cc = frag["caution"]
                extra.append("⚑ %s" % esc(gate_codes.get(
                    cc["code"], cc["code"]) if cc["type"] == "source-gate"
                    else cc["code"]))
            for d in frag.get("dispositions", []):
                extra.append(esc(strings["dispositions"][d["disposition"]]))
            rows.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
                        % (esc(label), esc(strings["status"][frag["status"]]),
                           tcells, "<br>".join(extra)))
            for ph in frag.get("phrases", []):
                tcells = "<br>".join(target_cell(t) for t in ph.get("targets", []))
                rows.append(
                    "<tr><td>%s · «%s»</td><td>%s</td><td>%s</td><td></td></tr>"
                    % (esc(label), esc(ph["text"]),
                       esc(strings["status"][ph["status"]]), tcells))
    gate_rows = []
    for ckey in sorted(ship_schedule.get("claimGates", {}),
                       key=lambda k: int(k[1:])):
        for g in ship_schedule["claimGates"][ckey]:
            disp = "; ".join(
                esc(strings["dispositions"][d["disposition"]])
                for d in ship_schedule.get("claimDispositions", {}).get(ckey, [])
                if d["gateId"] == g["gateId"])
            gate_rows.append(
                "<tr><td>%s claim %s</td><td>⚑ %s</td><td>%s</td></tr>"
                % (esc(prefix), ckey[1:], esc(gate_codes[g["code"]]), disp))
    return (
        '<section id="schedule"><h2>%s</h2>'
        '<table class="sched"><thead><tr><th>Fragment</th><th>Status</th>'
        '<th>Recorded candidate passages</th><th>Cautions / dispositions</th>'
        '</tr></thead><tbody>%s</tbody></table>'
        '<h3>Claim-level gates</h3><table class="sched"><thead><tr>'
        '<th>Claim</th><th>Gate</th><th>Disposition</th></tr></thead>'
        '<tbody>%s</tbody></table></section>'
        % (esc(strings["ui"]["scheduleTitle"]), "".join(rows),
           "".join(gate_rows)))


def _provenance_html(prov, strings):
    rows = []
    for c in prov["corpora"]:
        files = "<br>".join("%s — <code>%s</code>" % (esc(p), esc(d[:23]) + "…")
                            for p, d in sorted(c["files"].items()))
        rows.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
                    % (esc(c["id"]), esc(c["role"]), esc(c["version"]), files))
    auth = prov.get("authority")
    auth_html = ""
    if auth:
        auth_html = ("<p>Authority of record: <strong>%s</strong> (%s) — "
                     "<code>%s…</code></p>"
                     % (esc(auth["id"]), esc(auth["version"]),
                        esc(auth["digest"][:23])))
    digests = "".join(
        "<li>%s: <code>%s…</code></li>" % (esc(k), esc((prov[k] or "?")[:23]))
        for k in ("relationSetDigest", "gateInventoryDigest",
                  "dependencyMapDigest", "editionConfigDigest",
                  "stringsDigest", "builderTreeHash") if prov.get(k))
    return (
        '<section id="about"><h2>%s</h2>%s'
        '<table class="sched"><thead><tr><th>Corpus</th><th>Role</th>'
        '<th>Version</th><th>Pinned files (SHA-256, abbreviated display; '
        'full digests in the machine-readable block)</th></tr></thead>'
        '<tbody>%s</tbody></table><ul>%s</ul>'
        '<p>canonVersion %s · schema %s · declared release timestamp %s · '
        '%d claims / %d units / %d disclosure blocks</p><p>%s</p></section>'
        % (esc(strings["ui"]["aboutTitle"]), auth_html, "".join(rows), digests,
           esc(prov["canonVersion"]), esc(prov["schemaVersion"]),
           esc(prov["declaredReleaseTimestamp"]), prov["counts"]["claims"],
           prov["counts"]["units"], prov["counts"]["disclosureBlocks"],
           esc(strings["ui"]["viewportNote"])))


def render(m, mode="candidate"):
    """Render the edition artifact. mode: 'preview' adds the watermark
    (additive only — identical shipping projection)."""
    strings = m.strings
    ship = projections.ship_relation(m, "artifact")
    ship_schedule = projections.ship_relation(m, "schedule")
    reverse = projections.reverse_index(ship)
    quotes = projections.quotable_texts(m, ship)
    prov = projections.provenance(m)
    prov["builderTreeHash"] = projections.builder_tree_hash(
        m.gw, m.edition["declaredTransitiveInputs"])

    figures_b64 = {}
    for b in m.target_blocks:
        if b.kind == "figure":
            reader = m.registry.sibling_reader(m.edition["targetCorpus"])
            figures_b64[b.meta["file"]] = base64.b64encode(
                reader(b.meta["file"])).decode("ascii")

    anchors = {a.id: a.label for a in m.target_order}
    unit_labels = {}
    prefix = m.edition["strategyPrefix"]
    for c in m.claims:
        for u in c.units:
            unit_labels[u.id] = "%s claim %d · %s" % (prefix, c.number, u.label)
            frag = m.relation["fragments"][u.id]
            for ph in frag.get("phrases", []):
                unit_labels[ph["id"]] = "%s claim %d · “%s”" % (
                    prefix, c.number, ph["text"])

    disclaimer = strings["standingDisclaimer"].replace(
        "{editionVersion}", m.edition["claimSetVersion"])
    gate_codes = strings["editionNamespaces"][
        m.edition["stringsNamespace"]]["sourceGateCodes"]

    navdata = {
        "edition": {
            "id": m.edition["editionId"], "prefix": prefix,
            "version": m.edition["claimSetVersion"],
            "name": m.edition["displayName"],
        },
        "strings": {
            "ui": strings["ui"], "status": strings["status"],
            "role": strings["role"], "dispositions": strings["dispositions"],
            "cautionType": strings["cautionType"],
            "cautionScope": strings["cautionScope"],
            "gateCodes": gate_codes,
            "generalizationCodes": strings["generalizationCodes"],
        },
        "fragments": ship["fragments"],
        "claimGates": ship.get("claimGates", {}),
        "claimDispositions": ship.get("claimDispositions", {}),
        "reverse": reverse,
        "quotes": quotes,
        "anchors": anchors,
        "unitLabels": unit_labels,
    }

    watermark = ""
    if mode == "preview":
        watermark = ('<div class="watermark" aria-hidden="true">%s</div>'
                     % esc(strings["ui"]["previewWatermark"]))

    html = HTML_TEMPLATE
    for key, val in {
        "@@TITLE@@": esc("%s — %s" % (m.edition["displayName"],
                                      m.edition["claimSetVersion"])),
        "@@CSP@@": CSP,
        "@@CSS@@": CSS,
        "@@WATERMARK@@": watermark,
        "@@HEADERTITLE@@": esc(m.edition["displayName"]),
        "@@STRATEGY@@": esc("%s — %s" % (prefix, m.edition["strategyName"])),
        "@@VERSION@@": esc(m.edition["claimSetVersion"]),
        "@@WO@@": "PCT/IB2025/051755 · WO 2025/181623 A1",
        "@@LEGEND@@": esc(strings["counselLegend"]),
        "@@DISCLAIMER@@": esc(disclaimer),
        "@@CLAIMSPANE@@": _claims_pane(m, ship, strings),
        "@@DISCLOSUREPANE@@": _disclosure_pane(m, reverse, figures_b64, strings),
        "@@SCHEDULE@@": _schedule(m, ship_schedule, strings),
        "@@ABOUT@@": _provenance_html(prov, strings),
        "@@NAVDATA@@": script_json(navdata),
        "@@PROVDATA@@": script_json(prov),
        "@@JS@@": JS,
    }.items():
        html = html.replace(key, val)
    return html.encode("utf-8")


HTML_TEMPLATE = """<!DOCTYPE html>
<!-- GENERATED artifact: built by navigator/build.py from pinned sources;
     do not edit by hand. Verify against the detached .sha256 checksum;
     rebuild with: python3 navigator/build.py candidate <edition> (TDD §13). -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="@@CSP@@">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>@@TITLE@@</title>
<style>@@CSS@@</style>
</head>
<body>
@@WATERMARK@@
<header id="masthead">
<p class="legend">@@LEGEND@@</p>
<h1>@@HEADERTITLE@@ <span class="strategy">@@STRATEGY@@</span></h1>
<p class="meta">Claim set <strong>@@VERSION@@</strong> · @@WO@@
<button type="button" id="aux-toggle" data-aux="1" aria-pressed="false">About &amp; mapping schedule</button></p>
<p class="disclaimer">@@DISCLAIMER@@</p>
</header>
<main id="panes">
<section id="claims-pane" aria-label="Candidate claims">
<div id="reverse-bar" class="navbar" hidden></div>
@@CLAIMSPANE@@
</section>
<section id="disclosure-pane" aria-label="As-filed disclosure">
<div id="forward-bar" class="navbar" hidden></div>
<div id="disclosure-scroll">
@@DISCLOSUREPANE@@
</div>
</section>
</main>
<div id="live" aria-live="polite" class="visually-hidden"></div>
<div id="aux">
@@SCHEDULE@@
@@ABOUT@@
<footer><p class="legend">@@LEGEND@@</p><p class="disclaimer">@@DISCLAIMER@@</p></footer>
</div>
<noscript><style>#aux{display:block;flex:1;min-height:0}</style></noscript>
<script type="application/json" id="nav-data">@@NAVDATA@@</script>
<script type="application/json" id="prov-data">@@PROVDATA@@</script>
<script>@@JS@@</script>
</body>
</html>
"""

CSS = """
:root { --accent:#1a4f8b; --strong:#ffe08a; --soft:#fff3c9; --gate:#8b2c1a;
        --crr:#6a4a00; --chrome:#f4f2ec; --line:#c9c4b8; }
* { box-sizing:border-box; }
html,body { margin:0; padding:0; height:100%; }
body { font-family:Georgia,'Times New Roman',serif; color:#1c1c1c;
       display:flex; flex-direction:column; overflow:hidden; }
.visually-hidden { position:absolute; width:1px; height:1px; overflow:hidden;
       clip:rect(0 0 0 0); }
#masthead,footer { font-family:'Helvetica Neue',Arial,sans-serif;
       background:var(--chrome); border-bottom:1px solid var(--line);
       padding:6px 14px; flex:none; }
#masthead h1 { font-size:15px; margin:2px 0; }
.strategy { color:var(--accent); font-weight:normal; }
#masthead .meta { margin:2px 0; font-size:12px; }
.legend { font-size:10px; letter-spacing:.4px; color:#7a1f1f; margin:2px 0;
       font-weight:bold; }
.disclaimer { font-size:10.5px; color:#444; margin:2px 0; }
#panes { flex:1 1 auto; display:flex; min-height:0; }
#claims-pane { width:45%; overflow-y:auto; padding:10px 14px;
       border-right:2px solid var(--line); position:relative; }
#disclosure-pane { width:55%; display:flex; flex-direction:column;
       min-height:0; position:relative; }
#disclosure-scroll { overflow-y:auto; padding:10px 40px 10px 58px; flex:1; }
.claim-strip { position:sticky; top:-10px; z-index:5; background:#fff;
       border-bottom:1px solid var(--line); padding:6px 0; font-family:Arial,
       sans-serif; }
.chip-group { margin-right:8px; white-space:nowrap; display:inline-block; }
.chip-group-name { font-size:9px; color:#666; margin-right:2px;
       text-transform:uppercase; }
.chip { min-width:24px; min-height:24px; border:1px solid var(--line);
       background:#fff; border-radius:4px; cursor:pointer; font-size:12px; }
.chip-ind { border:2px solid var(--accent); font-weight:bold; }
.claim-group h2 { font-family:Arial,sans-serif; font-size:13px;
       color:var(--accent); border-bottom:1px solid var(--line); }
.claim { margin:0 0 14px 0; }
.claim-header { font-family:Arial,sans-serif; font-weight:bold;
       margin:8px 0 4px 0; }
.claim-independent > .claim-header .claim-no { color:var(--accent); }
.gate-chip { margin-left:8px; font-size:11px; border:1.5px dashed var(--gate);
       color:var(--gate); background:#fdf3f0; border-radius:4px;
       cursor:pointer; min-height:24px; }
.unit { display:flex; margin:2px 0; }
.unit-btn { flex:none; width:18px; min-height:24px; border:none;
       border-left:4px solid var(--line); background:transparent;
       cursor:pointer; }
.unit:hover .unit-btn,.unit-btn:focus { border-left-color:var(--accent);
       background:#eef3fa; }
.unit-body { padding:2px 4px; }
.unit-label { display:block; font-family:Arial,sans-serif; font-size:9px;
       color:#888; text-transform:uppercase; }
.status-counsel-review-required > .unit-body { background:#fbf6e8; }
.crr-note { font-family:Arial,sans-serif; font-size:11px; color:var(--crr);
       margin:2px 0; }
.crr-dot { color:var(--crr); }
.phrase-btn { font:inherit; border:none; border-bottom:2px dotted var(--accent);
       background:transparent; color:var(--accent); cursor:pointer;
       padding:0 1px; min-height:24px; }
.phrase-btn:focus,.unit-btn:focus,.rev-badge:focus,.chip:focus,
.gate-chip:focus,.navbar button:focus { outline:3px solid #d98c00;
       outline-offset:1px; }
.pointer-surface { cursor:pointer; }
.guidance-note { border:1px solid var(--gate); background:#fdf6f0;
       padding:6px 10px; font-size:13px; margin:8px 0; }
.editorial-tag { display:inline-block; font-family:Arial,sans-serif;
       font-size:9px; background:#e8e4da; color:#555; border-radius:3px;
       padding:0 4px; margin-right:6px; text-transform:uppercase;
       vertical-align:middle; }
.dblock { position:relative; }
.anchor-label { position:absolute; left:-46px; top:2px; width:40px;
       font-family:Menlo,monospace; font-size:9px; color:#999;
       text-align:right; }
.tablewrap .anchor-label,.rowmeta .anchor-label { position:static;
       display:block; width:auto; text-align:left; }
.rev-badge { font-family:Arial,sans-serif; font-size:10px; margin-left:6px;
       border:1px solid var(--accent); color:var(--accent); background:#fff;
       border-radius:8px; cursor:pointer; min-height:24px; min-width:24px; }
.hl-strong { background:var(--strong); box-shadow:0 0 0 2px var(--strong);
       border-left:4px solid var(--accent); }
.hl-soft { background:var(--soft); border-left:4px double var(--accent); }
.hl-frag { outline:2px solid var(--accent); }
.hl-frag-soft { background:var(--soft); }
.navbar { position:sticky; top:0; z-index:10; background:#fff;
       border:2px solid var(--accent); border-radius:0 0 6px 6px;
       padding:6px 10px; font-family:Arial,sans-serif; font-size:12px;
       box-shadow:0 2px 6px rgba(0,0,0,.15); }
.navbar .mode { font-size:10px; text-transform:uppercase; color:var(--accent);
       letter-spacing:.5px; }
.navbar .ctx { font-weight:bold; }
.navbar button { min-width:28px; min-height:24px; border:1px solid var(--line);
       background:#fff; border-radius:4px; cursor:pointer; }
.caution-chip { display:inline-block; border:1px solid var(--gate);
       color:var(--gate); background:#fdf3f0; border-radius:4px;
       padding:1px 5px; margin:2px 4px 2px 0; font-size:11px; }
.caution-chip.claim-gate-chip { border-style:dashed; border-width:2px;
       font-weight:bold; }
.caution-quote { display:block; font-size:11px; background:#faf7f2;
       border-left:3px solid var(--gate); margin:4px 0; padding:4px 6px; }
.pct-claim { border-left:3px solid #ddd; padding-left:8px; margin:6px 0; }
.tablewrap { overflow-x:auto; }
table { border-collapse:collapse; font-size:12.5px; }
td,th { border:1px solid var(--line); padding:3px 7px; }
.rowmeta { background:var(--chrome); font-size:9px; }
.tcaption { font-size:11px; color:#555; }
figure { margin:10px 0; }
figure img { max-width:100%; border:1px solid var(--line); }
pre { background:#f7f6f2; border:1px solid var(--line); padding:8px;
       overflow-x:auto; font-size:11.5px; }
#aux { display:none; overflow-y:auto; flex:1; min-height:0; }
body.aux-open #aux { display:block; }
body.aux-open #panes { display:none; }
#aux-toggle { font-size:11px; margin-left:12px; min-height:24px;
       border:1px solid var(--line); background:#fff; border-radius:4px;
       cursor:pointer; }
#schedule,#about { display:block; font-family:Arial,sans-serif;
       padding:10px 16px; }
.sched { font-size:11px; }
.sched-caution { color:var(--gate); }
.watermark { position:fixed; inset:0; pointer-events:none; z-index:99;
       display:flex; align-items:center; justify-content:center; }
.watermark::after { content:"PREVIEW — NOT FOR QA OR DELIVERY";
       font:bold 42px Arial,sans-serif; color:rgba(180,30,30,.18);
       transform:rotate(-28deg); white-space:nowrap; }
@media (max-width:1279px),(max-height:719px) {
  /* stacked: one dedicated combined scroll container; the page body
     never scrolls in any mode (TDD §12) */
  #panes { display:block; overflow-y:auto; }
  #claims-pane,#disclosure-pane { width:100%; height:auto; display:block;
       border-right:none; overflow:visible; }
  #disclosure-scroll { overflow:visible; }
}
@media (prefers-reduced-motion:reduce) {
  html { scroll-behavior:auto; }
}
@media print {
  body { overflow:visible; display:block; }
  #aux { display:block; overflow:visible; }
  #panes { display:block; }
  #claims-pane,#disclosure-pane,#disclosure-scroll { width:100%;
       overflow:visible; border:none; display:block; }
  .navbar,.rev-badge,.unit-btn,.chip,.claim-strip,.watermark { display:none !important; }
  .legend { position:fixed; bottom:0; left:0; right:0; background:#fff; }
  footer .disclaimer { margin-bottom:18px; }
}
noscript .navbar { display:none; }
"""

JS = r"""
'use strict';
/* Attempted-use instrumentation per schema/api-policy.json (probed class).
   Records attempts; the page's own code never uses these APIs (AC-15). */
window.__apiAttempts = [];
(function(){
  function rec(name){ window.__apiAttempts.push(name); }
  function wrapFn(obj, key, name){
    try { var orig = obj[key];
      if (typeof orig !== 'function') return;
      obj[key] = function(){ rec(name); return orig.apply(this, arguments); };
    } catch (e) {}
  }
  wrapFn(window, 'fetch', 'fetch');
  if (window.XMLHttpRequest) wrapFn(XMLHttpRequest.prototype, 'open', 'XMLHttpRequest');
  try { var WS = window.WebSocket;
    if (WS) window.WebSocket = function(){ rec('WebSocket');
      return new (Function.prototype.bind.apply(WS,[null].concat([].slice.call(arguments))))(); };
  } catch (e) {}
  try { var ES = window.EventSource;
    if (ES) window.EventSource = function(){ rec('EventSource');
      return new (Function.prototype.bind.apply(ES,[null].concat([].slice.call(arguments))))(); };
  } catch (e) {}
  if (window.navigator) wrapFn(navigator, 'sendBeacon', 'navigator.sendBeacon');
  if (window.history){ wrapFn(history, 'pushState', 'history.pushState');
    wrapFn(history, 'replaceState', 'history.replaceState'); }
  /* localStorage + sessionStorage are covered via Storage.prototype */
  if (window.Storage){ wrapFn(Storage.prototype, 'setItem', 'web-storage');
    wrapFn(Storage.prototype, 'getItem', 'web-storage'); }
  if (window.indexedDB) wrapFn(window.indexedDB.constructor ?
    IDBFactory.prototype : {}, 'open', 'indexedDB.open');
  try {
    var desc = Object.getOwnPropertyDescriptor(Document.prototype, 'cookie');
    if (desc && desc.configurable) Object.defineProperty(document, 'cookie', {
      get: function(){ rec('cookie-read'); return desc.get.call(document); },
      set: function(v){ rec('cookie-write'); return desc.set.call(document, v); }
    });
  } catch (e) {}
})();

var DATA = JSON.parse(document.getElementById('nav-data').textContent);

/*NAVMODEL-START*/
/* ---- pure selection model (also exercised by AC-10 scripted checks) ---- */
var NavModel = {
  forwardTargets: function(data, fragId){
    var frag = null;
    if (fragId.indexOf('p') > 0){
      var uid = fragId.slice(0, fragId.indexOf('p', fragId.indexOf('u')));
      var unit = data.fragments[uid];
      if (!unit || !unit.phrases) return null;
      for (var i = 0; i < unit.phrases.length; i++)
        if (unit.phrases[i].id === fragId) frag = unit.phrases[i];
    } else frag = data.fragments[fragId];
    if (!frag) return null;
    return { status: frag.status, targets: frag.targets || [],
             caution: frag.caution || null,
             dispositions: frag.dispositions || [] };
  },
  claimOf: function(fragId){ return 'c' + parseInt(fragId.slice(1), 10); },
  claimGates: function(data, fragId){
    return data.claimGates[NavModel.claimOf(fragId)] || [];
  },
  reverseFragments: function(data, blockId){
    return data.reverse[blockId] || [];
  },
  cycle: function(pos, len, delta){ return len ? (pos + delta + len) % len : 0; }
};
/*NAVMODEL-END*/

var state = { mode: null, key: null, pos: 0, list: [], returnFocus: null };
var fbar = document.getElementById('forward-bar');
var rbar = document.getElementById('reverse-bar');
var live = document.getElementById('live');
var reduced = window.matchMedia &&
  window.matchMedia('(prefers-reduced-motion: reduce)').matches;

function say(t){ live.textContent = t; }
function el(tag, cls, text){ var e = document.createElement(tag);
  if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
function btn(cls, label, text, fn){ var b = el('button', cls, text);
  b.type = 'button'; b.setAttribute('aria-label', label);
  b.addEventListener('click', fn); return b; }

function clearHighlights(){
  ['hl-strong','hl-soft','hl-frag','hl-frag-soft'].forEach(function(c){
    Array.prototype.slice.call(document.querySelectorAll('.' + c))
      .forEach(function(n){ n.classList.remove(c); });
  });
}
function clearSelection(refocus){
  var rf = state.returnFocus;
  state = { mode: null, key: null, pos: 0, list: [], returnFocus: null };
  fbar.hidden = true; rbar.hidden = true; clearHighlights();
  fbar.textContent = ''; rbar.textContent = '';
  if (refocus && rf){ var n = document.getElementById(rf); if (n) n.focus(); }
  say('Selection cleared');
}
function scrollToBlock(id, strong){
  var n = document.getElementById(id);
  if (!n) return;
  n.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'center' });
  if (strong) n.classList.add('hl-strong');
}

function cautionChip(caution, isClaimGate){
  var wrap = el('span');
  var name;
  if (caution.type === 'source-gate') name = DATA.strings.gateCodes[caution.code] || caution.code;
  else name = 'Author observation';
  var chip = btn('caution-chip' + (isClaimGate ? ' claim-gate-chip' : ''),
    (isClaimGate ? 'Claim-level gate: ' : 'Caution: ') + name, '⚑ ' + name,
    function(){
      var q = wrap.querySelector('.caution-quote');
      if (q){ q.remove(); return; }
      var quote = el('span', 'caution-quote');
      if (caution.type === 'source-gate' && caution.source &&
          DATA.quotes[caution.source.block])
        quote.textContent = DATA.quotes[caution.source.block];
      else quote.textContent = DATA.strings.generalizationCodes[caution.code] || '';
      wrap.appendChild(quote);
    });
  wrap.appendChild(chip);
  return wrap;
}

function renderForwardBar(){
  fbar.textContent = '';
  var info = state.info;
  fbar.appendChild(el('div', 'mode', DATA.strings.ui.forwardMode));
  fbar.appendChild(el('div', 'ctx', DATA.unitLabels[state.key] || state.key));
  if (info.status === 'counsel-review-required'){
    fbar.appendChild(el('div', null, DATA.strings.ui.noCandidateNotice));
  } else {
    var t = info.targets[state.pos];
    var line = el('div');
    line.appendChild(el('span', null, (state.pos + 1) + ' of ' +
      info.targets.length + ' : ' + (DATA.anchors[t.block] || t.block)));
    if (t.role) line.appendChild(el('span', null, '  [' +
      DATA.strings.role[t.role] + ']'));
    fbar.appendChild(line);
    if (t.note) fbar.appendChild(el('div', null, t.note));
    if (info.targets.length > 5)
      fbar.appendChild(el('span', 'more', DATA.strings.ui.moreCandidates
        .replace('{n}', String(info.targets.length - 5))));
    var controls = el('div');
    controls.appendChild(btn(null, DATA.strings.ui.previous, '◀',
      function(){ move(-1); }));
    controls.appendChild(btn(null, DATA.strings.ui.next, '▶',
      function(){ move(1); }));
    controls.appendChild(btn(null, DATA.strings.ui.clearSelection, '×',
      function(){ clearSelection(true); }));
    fbar.appendChild(controls);
    if (t.caution) fbar.appendChild(cautionChip(t.caution, false));
  }
  if (info.caution) fbar.appendChild(cautionChip(info.caution, false));
  NavModel.claimGates(DATA, state.key).forEach(function(g){
    fbar.appendChild(cautionChip(g, true));
  });
  fbar.hidden = false;
}

function applyForwardHighlights(){
  clearHighlights();
  var info = state.info;
  var fragNode = document.getElementById('u-' + state.key) ||
    document.getElementById('btn-' + state.key);
  if (fragNode) fragNode.classList.add('hl-frag');
  if (info.status !== 'counsel-review-required'){
    info.targets.slice(0, 5).forEach(function(t, i){
      var n = document.getElementById(t.block);
      if (n && i !== state.pos) n.classList.add('hl-soft');
    });
    scrollToBlock(info.targets[state.pos].block, true);
  }
}

function activate(fragId, fromId){
  var info = NavModel.forwardTargets(DATA, fragId);
  if (!info) return;
  clearSelection(false);
  state = { mode: 'forward', key: fragId, pos: 0, info: info,
            returnFocus: fromId };
  renderForwardBar();
  applyForwardHighlights();
  var label = DATA.unitLabels[fragId] || fragId;
  if (info.status === 'counsel-review-required')
    say(label + ' — ' + DATA.strings.ui.noCandidateNotice);
  else say(DATA.strings.ui.forwardMode + ' — ' + label + ' — 1 of ' +
    info.targets.length + ' : ' + (DATA.anchors[info.targets[0].block] || ''));
  fbar.setAttribute('tabindex', '-1');
  fbar.focus();
}

function move(delta){
  if (state.mode === 'forward' && state.info.status === 'mapped'){
    state.pos = NavModel.cycle(state.pos, state.info.targets.length, delta);
    renderForwardBar(); applyForwardHighlights();
    var t = state.info.targets[state.pos];
    say((state.pos + 1) + ' of ' + state.info.targets.length + ' : ' +
        (DATA.anchors[t.block] || t.block));
    fbar.focus();
  } else if (state.mode === 'reverse'){
    state.pos = NavModel.cycle(state.pos, state.list.length, delta);
    renderReverseBar(); applyReverseHighlights();
    say((state.pos + 1) + ' of ' + state.list.length + ' : ' +
        (DATA.unitLabels[state.list[state.pos].fragment] || ''));
    rbar.focus();
  }
}

function renderReverseBar(){
  rbar.textContent = '';
  rbar.appendChild(el('div', 'mode', DATA.strings.ui.reverseMode));
  var claims = {};
  state.list.forEach(function(e){ claims[NavModel.claimOf(e.fragment)] = 1; });
  rbar.appendChild(el('div', 'ctx', (DATA.anchors[state.key] || state.key)));
  rbar.appendChild(el('div', null, state.list.length + ' fragments · ' +
    Object.keys(claims).length + ' claims'));
  var cur = state.list[state.pos];
  rbar.appendChild(el('div', null, (state.pos + 1) + ' of ' +
    state.list.length + ' : ' + (DATA.unitLabels[cur.fragment] || cur.fragment)));
  var controls = el('div');
  controls.appendChild(btn(null, DATA.strings.ui.previous, '◀',
    function(){ move(-1); }));
  controls.appendChild(btn(null, DATA.strings.ui.next, '▶',
    function(){ move(1); }));
  controls.appendChild(btn(null, DATA.strings.ui.clearSelection, '×',
    function(){ clearSelection(true); }));
  rbar.appendChild(controls);
  rbar.hidden = false;
}

function applyReverseHighlights(){
  clearHighlights();
  var blockNode = document.getElementById(state.key);
  if (blockNode) blockNode.classList.add('hl-frag');
  state.list.forEach(function(e, i){
    var n = document.getElementById('u-' + e.fragment) ||
            document.getElementById('btn-' + e.fragment);
    if (!n) return;
    if (i === state.pos){ n.classList.add('hl-strong');
      n.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth',
                         block: 'center' });
    } else n.classList.add('hl-frag-soft');
  });
}

function activateReverse(blockId, fromId){
  var list = NavModel.reverseFragments(DATA, blockId);
  if (!list.length) return;
  clearSelection(false);
  state = { mode: 'reverse', key: blockId, pos: 0, list: list,
            returnFocus: fromId };
  renderReverseBar(); applyReverseHighlights();
  say(DATA.strings.ui.reverseMode + ' — ' + (DATA.anchors[blockId] || '') +
      ' — ' + list.length + ' fragments');
  rbar.setAttribute('tabindex', '-1');
  rbar.focus();
}

document.addEventListener('click', function(ev){
  var b = ev.target.closest ? ev.target.closest('button') : null;
  if (b){
    if (b.dataset.frag){ activate(b.dataset.frag, b.id); return; }
    if (b.dataset.block){ activateReverse(b.dataset.block, b.id); return; }
    if (b.dataset.goto){
      var n = document.getElementById(b.dataset.goto);
      if (n) n.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth',
                                block: 'start' });
      return;
    }
    if (b.dataset.gate){
      activateGate(b.dataset.claim, b.dataset.gate, b.id); return;
    }
    if (b.dataset.aux){
      var on = document.body.classList.toggle('aux-open');
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      return;
    }
    return;
  }
  var surf = ev.target.closest ? ev.target.closest('.pointer-surface') : null;
  if (surf){
    var sel = window.getSelection && window.getSelection();
    if (sel && sel.toString().length) return; /* selection suppresses it */
    activate(surf.dataset.frag, 'btn-' + surf.dataset.frag);
  }
});

function activateGate(claimKey, gateId, fromId){
  var gates = DATA.claimGates[claimKey] || [];
  for (var i = 0; i < gates.length; i++){
    if (gates[i].gateId === gateId){
      clearSelection(false);
      state = { mode: 'forward', key: claimKey, pos: 0,
        info: { status: 'claim-gate', targets: [] }, returnFocus: fromId };
      fbar.textContent = '';
      fbar.appendChild(el('div', 'mode', DATA.strings.ui.forwardMode));
      fbar.appendChild(el('div', 'ctx', DATA.edition.prefix + ' claim ' +
        claimKey.slice(1) + ' — claim-level gate'));
      fbar.appendChild(cautionChip(gates[i], true));
      (DATA.claimDispositions[claimKey] || []).forEach(function(d){
        if (d.gateId === gateId)
          fbar.appendChild(el('div', null,
            DATA.strings.dispositions[d.disposition]));
      });
      fbar.appendChild(btn(null, DATA.strings.ui.clearSelection, '×',
        function(){ clearSelection(true); }));
      fbar.hidden = false;
      fbar.setAttribute('tabindex', '-1');
      fbar.focus();
      say('Claim-level gate on ' + DATA.edition.prefix + ' claim ' +
          claimKey.slice(1));
      return;
    }
  }
}

document.addEventListener('keydown', function(ev){
  if (ev.key === 'Escape' && state.mode){ clearSelection(true); return; }
  if ((ev.key === 'ArrowLeft' || ev.key === 'ArrowRight') && state.mode){
    var bar = state.mode === 'forward' ? fbar : rbar;
    if (bar.contains(document.activeElement)){
      ev.preventDefault();
      move(ev.key === 'ArrowLeft' ? -1 : 1);
    }
  }
});
"""
