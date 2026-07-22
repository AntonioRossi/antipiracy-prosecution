"""Edition validation — the complete check list behind AC-01 … AC-05.

Every check returns (code, message) defects; ``candidate`` fails listing
all of them; ``release`` requires zero plus the release predicate. The
release predicate itself lives in schema/invariants.py (defined once).
"""

import importlib.util
import re

from . import schema_validate
from .model import FRAG_ID_RE, PHRASE_ID_RE


def _load_invariants(gw):
    source = gw.read_text("navigator/schema/invariants.py")
    spec = importlib.util.spec_from_loader("aa11393_invariants", loader=None)
    mod = importlib.util.module_from_spec(spec)
    exec(compile(source, "navigator/schema/invariants.py", "exec"), mod.__dict__)
    return mod


def validate_edition(m, for_release=False):
    """Validate an EditionModel. Returns a list of (code, message)."""
    inv = _load_invariants(m.gw)
    errors = []

    def err(code, msg):
        errors.append((code, msg))

    # ---- schema conformance + axis discipline ---------------------------
    for name, instance in (
        ("relation", m.relation), ("gates", m.gates), ("deps", m.deps),
        ("edition", m.edition),
    ):
        for e in schema_validate.validate(instance, m.schemas[name]):
            err("schema:%s" % name, e)
    try:
        schema_validate.check_axes(m.schemas["relation"])
        schema_validate.check_locator_coverage(m.schemas["relation"])
    except schema_validate.SchemaError as e:
        err("schema:axes", str(e))

    # ---- census (AC-01) -------------------------------------------------
    census = m.edition["census"]
    per = {str(c.number): len(c.units) for c in m.claims}
    if len(m.claims) != census["claims"]:
        err("census", "parsed %d claims, config declares %d"
            % (len(m.claims), census["claims"]))
    if sum(per.values()) != census["units"]:
        err("census", "parsed %d units, config declares %d"
            % (sum(per.values()), census["units"]))
    if per != census["perClaim"]:
        diff = {k for k in set(per) | set(census["perClaim"])
                if per.get(k) != census["perClaim"].get(k)}
        err("census", "per-claim census mismatch on claims %s" % sorted(diff))
    groups = []
    for c in m.claims:
        if c.group not in groups:
            groups.append(c.group)
    if groups != m.edition["groups"]:
        err("census", "group headings %r do not match config %r"
            % (groups, m.edition["groups"]))
    pct = [b for b in m.target_blocks if b.kind == "claim-whole"]
    if len(pct) != 18:
        err("census", "expected 18 whole PCT claim anchors, found %d" % len(pct))
    figures = [b for b in m.target_blocks if b.kind == "figure"]
    if len(figures) != 4:
        err("census", "expected 4 figures, found %d" % len(figures))
    tables = [b for b in m.target_blocks if b.kind == "table" and b.rows]
    if len([t for t in tables if "Example 2" in t.label]) != 3:
        err("census", "expected the 3 Example 2 EDL tables with row anchors")

    # ---- binding --------------------------------------------------------
    b = m.binding
    if b.get("fragmentCorpus") != m.edition["claimCorpus"]:
        err("binding", "relation fragmentCorpus %r != edition claim corpus %r"
            % (b.get("fragmentCorpus"), m.edition["claimCorpus"]))
    if b.get("targetCorpus") != m.edition["targetCorpus"]:
        err("binding", "relation targetCorpus %r != edition target corpus %r"
            % (b.get("targetCorpus"), m.edition["targetCorpus"]))

    # ---- gate inventory endpoint currency -------------------------------
    if m.gates.get("profileDigest") != m.claim_profile_digest:
        err("inventory", "profileDigest stale (profile is %s)"
            % m.claim_profile_digest)
    for gate in m.gates["gates"]:
        gid = gate["gateId"]
        src = m.quotable_anchor(gate["source"]["block"])
        if src is None:
            err("inventory", "%s: source block %r is not a quotable block"
                % (gid, gate["source"]["block"]))
        elif gate["source"]["textHash"] != src.digest:
            err("inventory", "%s: source textHash stale for block %s"
                % (gid, gate["source"]["block"]))
        scope = gate["requiredScope"]
        applies = gate["appliesTo"]
        if scope == "claim":
            if "claims" not in applies or "fragments" in applies:
                err("inventory", "%s: claim-scope gate must list claims only" % gid)
            for c in applies.get("claims", []):
                agg = m.agg_hashes.get(c["claim"])
                if agg is None:
                    err("inventory", "%s: unknown claim %r" % (gid, c["claim"]))
                elif c["claimHash"] != agg:
                    err("inventory", "%s: claimHash stale for claim %d"
                        % (gid, c["claim"]))
        else:
            if "fragments" not in applies or "claims" in applies:
                err("inventory", "%s: %s-scope gate must list fragments" % (gid, scope))
            if scope == "target" and "cardinality" not in applies:
                err("inventory", "%s: target-scope gate needs a cardinality" % gid)
            if scope != "target" and "cardinality" in applies:
                err("inventory", "%s: cardinality is target-scope only" % gid)
            for f in applies.get("fragments", []):
                unit = m.units.get(f["id"])
                if unit is None:
                    err("inventory", "%s: unknown fragment %r" % (gid, f["id"]))
                elif f["hash"] != unit.digest:
                    err("inventory", "%s: fragment hash stale for %s"
                        % (gid, f["id"]))

    # ---- fragment completeness + per-fragment checks --------------------
    frags = m.relation.get("fragments", {})
    expected_units = set(m.units)
    got_units = set(frags)
    for missing in sorted(expected_units - got_units):
        err("completeness", "unit %s has no relation entry" % missing)
    for extra in sorted(got_units - expected_units):
        err("completeness", "relation entry %s matches no census unit" % extra)

    strings_ns = m.strings["editionNamespaces"][m.edition["stringsNamespace"]]
    inventory_codes = {g["code"] for g in m.gates["gates"]}
    used_gen_codes = set()
    used_source_codes = set()
    forbidden = m.edition["forbiddenTerms"]

    def check_text_bounds(owner, field, text, limit):
        if len(text) > limit:
            err("bounds", "%s: %s exceeds %d chars" % (owner, field, limit))
        for term in forbidden:
            if term.lower() in text.lower():
                err("forbidden-terms", "%s: %s contains forbidden term %r"
                    % (owner, field, term))

    def check_caution(owner, caution, scope, frag_id=None, target_block=None):
        ctype, code = caution.get("type"), caution.get("code")
        if not inv.CAUTION_MATRIX.get((ctype, scope), False):
            err("caution", "%s: %s at %s scope is unrepresentable"
                % (owner, ctype, scope))
        if ctype == "source-gate":
            used_source_codes.add(code)
            gid = caution.get("gateId")
            if not gid:
                err("caution", "%s: source-gate without gateId" % owner)
                return
            entry = m.gates_by_id.get(gid)
            if entry is None:
                err("caution", "%s: gateId %r not in inventory" % (owner, gid))
                return
            if entry["code"] != code:
                err("caution", "%s: code %r does not match inventory %r"
                    % (owner, code, entry["code"]))
            src = caution.get("source")
            if not src:
                err("caution", "%s: source-gate without source" % owner)
            else:
                if src["corpus"] != m.edition["claimCorpus"]:
                    err("caution", "%s: caution source corpus %r is not the "
                        "edition's claim corpus" % (owner, src["corpus"]))
                if (src["block"], src["textHash"]) != (
                        entry["source"]["block"], entry["source"]["textHash"]):
                    err("caution", "%s: source does not match inventory entry"
                        % owner)
                qa = m.quotable_anchor(src["block"])
                if qa is None:
                    err("caution", "%s: source block %r not quotable"
                        % (owner, src["block"]))
                elif src["textHash"] != qa.digest:
                    err("drift", "%s: caution source textHash stale" % owner)
            req_scope = entry["requiredScope"]
            if scope != req_scope:
                fallback_ok = (
                    req_scope == "target" and scope == "fragment" and
                    frag_id is not None and _has_disposition(
                        m, gid, frag_id, "carried-at-fragment-fallback"))
                if not fallback_ok:
                    err("caution", "%s: gate %s carried at %s scope but "
                        "required at %s" % (owner, gid, scope, req_scope))
        else:
            if caution.get("gateId") or caution.get("source"):
                err("caution", "%s: generalization-note carries gate fields"
                    % owner)
            used_gen_codes.add(code)
            if code not in m.strings["generalizationCodes"]:
                err("enum", "%s: generalization code %r unregistered"
                    % (owner, code))

    def check_target(owner, frag_id, target, seen_blocks):
        block = target["block"]
        if block in seen_blocks:
            err("duplicate", "%s: duplicate target block %s" % (owner, block))
        seen_blocks.add(block)
        anchor = m.target_anchor(block)
        if anchor is None:
            err("target", "%s: unknown target block %r" % (owner, block))
            return
        if anchor.cls != "targetable":
            err("target", "%s: block %s is %s — non-targetable"
                % (owner, block, anchor.cls))
            return
        if target["textHash"] != anchor.digest:
            err("drift", "%s: target %s textHash stale" % (owner, block))
        check_text_bounds(owner, "note", target.get("note", ""), inv.NOTE_MAX)
        if "rationale" in target:
            check_text_bounds(owner, "rationale", target["rationale"],
                              inv.RATIONALE_MAX)
        if "caution" in target:
            check_caution(owner + ":" + block, target["caution"], "target",
                          frag_id=frag_id, target_block=block)

    for fid in sorted(frags):
        frag = frags[fid]
        unit = m.units.get(fid)
        if unit is None:
            continue
        if frag.get("fragmentTextHash") != unit.digest:
            err("drift", "%s: fragmentTextHash stale" % fid)
        status = frag.get("status")
        targets = frag.get("targets", [])
        if status == "mapped" and not targets:
            err("evidence", "%s: mapped but has no targets" % fid)
        if status == "counsel-review-required" and targets:
            err("evidence", "%s: no-candidate fragment carries targets" % fid)
        seen_blocks = set()
        for t in targets:
            check_target(fid, fid, t, seen_blocks)
        if "caution" in frag:
            check_caution(fid, frag["caution"], "fragment", frag_id=fid)
        seen_pids = set()
        spans = []
        for ph in frag.get("phrases", []):
            pid = ph.get("id", "")
            pm = PHRASE_ID_RE.match(pid)
            if not pm or not pid.startswith(fid + "p"):
                err("phrase", "%s: bad phrase id %r" % (fid, pid))
                continue
            if pid in seen_pids:
                err("duplicate", "%s: duplicate phrase id %s" % (fid, pid))
            seen_pids.add(pid)
            text, occ = ph.get("text", ""), ph.get("occurrence", 0)
            positions = [mm.start() for mm in
                         re.finditer(re.escape(text), unit.text)]
            if occ < 1 or len(positions) < occ:
                err("phrase", "%s: %r occurrence %d not found verbatim in unit"
                    % (pid, text, occ))
            else:
                start = positions[occ - 1]
                spans.append((pid, start, start + len(text)))
            p_status = ph.get("status")
            p_targets = ph.get("targets", [])
            if p_status == "mapped" and not p_targets:
                err("evidence", "%s: mapped but has no targets" % pid)
            if p_status == "counsel-review-required" and p_targets:
                err("evidence", "%s: no-candidate phrase carries targets" % pid)
            pseen = set()
            for t in p_targets:
                check_target(pid, fid, t, pseen)
            if "caution" in ph:
                check_caution(pid, ph["caution"], "fragment", frag_id=fid)
        spans.sort(key=lambda s: s[1])
        for (p1, s1, e1), (p2, s2, e2) in zip(spans, spans[1:]):
            if s2 < e1:
                err("phrase", "phrases %s and %s overlap" % (p1, p2))

    # ---- claim gates ----------------------------------------------------
    for ckey in sorted(m.relation.get("claimGates", {})):
        num = int(ckey[1:])
        if num not in m.claims_by_number:
            err("claim-gate", "%s: unknown claim" % ckey)
            continue
        seen_gids = set()
        for gate in m.relation["claimGates"][ckey]:
            gid = gate.get("gateId")
            owner = "%s/%s" % (ckey, gid)
            if gid in seen_gids:
                err("duplicate", "%s: duplicate claim-gate" % owner)
            seen_gids.add(gid)
            if gate.get("claimHash") != m.agg_hashes[num]:
                err("drift", "%s: claimHash stale" % owner)
            check_caution(owner, {
                "gateId": gid, "type": gate.get("type"),
                "code": gate.get("code"), "source": gate.get("source"),
            }, "claim")

    # ---- dispositions: totality, honesty, uniqueness, pins --------------
    disp_index = {}
    for disp in m.relation.get("dispositions", []):
        key = (disp.get("gateId"), disp.get("subject", {}).get("kind"),
               disp.get("subject", {}).get("id"))
        owner = "disposition %s@%s" % (key[0], key[2])
        if key in disp_index:
            err("duplicate", "%s: duplicate disposition" % owner)
        disp_index[key] = disp
        entry = m.gates_by_id.get(disp.get("gateId"))
        if entry is None:
            err("disposition", "%s: unknown gateId" % owner)
            continue
        if disp.get("gateEntryHash") != m.gate_entry_hash(disp["gateId"]):
            err("drift", "%s: gateEntryHash stale" % owner)
        subject = disp["subject"]
        if subject["kind"] == "fragment":
            listed = {f["id"] for f in entry["appliesTo"].get("fragments", [])}
            if subject["id"] not in listed:
                err("disposition", "%s: subject not listed by the gate" % owner)
            unit = m.units.get(subject["id"])
            if unit is not None and disp.get("subjectHash") != unit.digest:
                err("drift", "%s: subjectHash stale" % owner)
            frag = frags.get(subject["id"], {})
            evidence = frag.get("status", "counsel-review-required")
        else:
            listed = {"c%d" % c["claim"]
                      for c in entry["appliesTo"].get("claims", [])}
            if subject["id"] not in listed:
                err("disposition", "%s: subject not listed by the gate" % owner)
            num = int(subject["id"][1:])
            if disp.get("subjectHash") != m.agg_hashes.get(num):
                err("drift", "%s: subjectHash stale" % owner)
            evidence = "mapped"
        permitted = inv.permitted_dispositions(entry["requiredScope"], evidence)
        if disp.get("disposition") not in permitted:
            err("disposition", "%s: %r not permitted for %s-scope gate over a "
                "%s subject" % (owner, disp.get("disposition"),
                                entry["requiredScope"], evidence))

    # ---- referential integrity, direction 2 (inventory -> evidence) -----
    for gate in m.gates["gates"]:
        gid = gate["gateId"]
        if gate["requirement"] != "mandatory":
            continue
        scope = gate["requiredScope"]
        if scope == "claim":
            for c in gate["appliesTo"].get("claims", []):
                ckey = "c%d" % c["claim"]
                carried = any(g.get("gateId") == gid for g in
                              m.relation.get("claimGates", {}).get(ckey, []))
                if not carried:
                    err("integrity", "%s: mandatory claim gate not carried on %s"
                        % (gid, ckey))
                if (gid, "claim", ckey) not in disp_index:
                    err("integrity", "%s: no disposition for %s" % (gid, ckey))
        else:
            for f in gate["appliesTo"].get("fragments", []):
                fid = f["id"]
                frag = frags.get(fid)
                if frag is None:
                    continue  # completeness already reported
                key = (gid, "fragment", fid)
                disp = disp_index.get(key)
                if disp is None:
                    err("integrity", "%s: no disposition for %s" % (gid, fid))
                if scope == "fragment":
                    caution = frag.get("caution")
                    if not (caution and caution.get("gateId") == gid):
                        err("integrity",
                            "%s: mandatory fragment gate not carried on %s"
                            % (gid, fid))
                else:  # target scope
                    minimum = gate["appliesTo"]["cardinality"][
                        "minTargetsPerFragment"]
                    carrying = [t for t in frag.get("targets", [])
                                if t.get("caution", {}).get("gateId") == gid]
                    if frag.get("status") == "mapped":
                        if len(carrying) < minimum:
                            err("integrity",
                                "%s: %d target(s) of %s carry the gate; "
                                "cardinality requires ≥ %d"
                                % (gid, len(carrying), fid, minimum))
                    else:
                        # honest no-candidate: fallback or no-target-recorded
                        caution = frag.get("caution")
                        if disp is not None and disp.get("disposition") == \
                                "carried-at-fragment-fallback":
                            if not (caution and caution.get("gateId") == gid):
                                err("integrity",
                                    "%s: fallback disposition on %s without a "
                                    "fragment-scope instance" % (gid, fid))

    # ---- enum exhaustiveness (guardrail 13) -----------------------------
    reg_codes = set(strings_ns["sourceGateCodes"])
    if reg_codes != inventory_codes:
        err("enum", "source-gate code registry %r != inventory codes %r"
            % (sorted(reg_codes), sorted(inventory_codes)))
    unreg = used_source_codes - reg_codes
    if unreg:
        err("enum", "source-gate codes without display entries: %r" % sorted(unreg))
    gen_reg = set(m.strings["generalizationCodes"])
    if used_gen_codes - gen_reg:
        err("enum", "generalization codes unregistered: %r"
            % sorted(used_gen_codes - gen_reg))
    if gen_reg - used_gen_codes:
        err("enum", "generalization codes registered but unused: %r"
            % sorted(gen_reg - used_gen_codes))
    for reg_key, enum in (
        ("status", inv.STATUSES), ("role", inv.ROLES),
        ("cautionType", inv.CAUTION_TYPES), ("cautionScope", inv.CAUTION_SCOPES),
        ("dispositions", inv.DISPOSITIONS),
        ("migrationReasons", inv.MIGRATION_REASONS),
    ):
        if set(m.strings[reg_key]) != set(enum):
            err("enum", "strings registry %r does not exactly cover its enum"
                % reg_key)

    # ---- lifecycle: contentHash, pending, stale (AC-02) -----------------
    for otype, key, fields, projection in m.iter_owners():
        expected = m.content_hash(projection)
        defects = inv.release_ready(fields, expected)
        review = fields.get("review") or {}
        if review.get("contentHash") != expected:
            err("content-hash", "%s %s: %s" % (
                otype, key,
                "stale review.contentHash" if review.get("contentHash")
                else "missing review.contentHash"))
        if for_release:
            for d in defects:
                if "contentHash" not in d:
                    err("release", "%s %s: %s" % (otype, key, d))
        else:
            if fields.get("reviewState") == "pending":
                err("pending", "%s %s: reviewState pending" % (otype, key))
            if fields.get("migrationState") == "stale":
                err("stale", "%s %s: migrationState stale (%s)"
                    % (otype, key, fields.get("migrationReason", "?")))

    return errors


def _has_disposition(m, gate_id, fragment_id, value):
    for disp in m.relation.get("dispositions", []):
        if disp.get("gateId") == gate_id and \
                disp.get("subject", {}).get("id") == fragment_id and \
                disp.get("disposition") == value:
            return True
    return False
