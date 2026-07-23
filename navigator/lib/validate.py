"""Edition validation — the complete check list behind AC-01 … AC-05.

Every check returns (code, message) defects; ``candidate`` fails listing
all of them; ``release`` requires zero plus the release predicate. The
release predicate itself lives in schema/invariants.py (defined once).
"""

import importlib.util
import posixpath
import re

from . import authority, projections, render, schema_validate, timepolicy
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
    relation_schema_valid = True
    for name, instance in (
        ("relation", m.relation), ("gates", m.gates), ("deps", m.deps),
        ("edition", m.edition), ("support-matrix", m.support_matrix),
    ):
        try:
            schema_validate.check_schema(m.schemas[name])
        except schema_validate.SchemaError as exc:
            err("schema:%s" % name, str(exc))
            if name == "relation":
                relation_schema_valid = False
            continue
        for e in schema_validate.validate(instance, m.schemas[name]):
            err("schema:%s" % name, e)
    if relation_schema_valid:
        try:
            schema_validate.check_axes(m.schemas["relation"])
            schema_validate.check_locator_coverage(m.schemas["relation"])
        except schema_validate.SchemaError as e:
            err("schema:axes", str(e))

    for problem in render.api_policy_problems(m.api_policy):
        err("api-policy", problem)

    # The schema repeats closed enums at each owner shape for fail-closed JSON
    # validation.  Cross-check those declarations against the one normative
    # invariant module so a schema edit cannot silently create a second enum
    # or lifecycle-applicability definition.
    relation_schema = m.schemas["relation"]
    owner_schemas = {
        "unit": next(iter(relation_schema["properties"]["fragments"]
                          ["patternProperties"].values())),
        "phrase": relation_schema["definitions"]["phrase"],
        "claim-gate": next(iter(
            relation_schema["properties"]["claimGates"]
            ["patternProperties"].values()))["items"],
        "disposition": relation_schema["properties"]["dispositions"]
        ["items"],
    }
    lifecycle_names = {"status", "reviewState", "migrationState", "review"}
    enum_sources = {
        "status": inv.STATUSES,
        "reviewState": inv.REVIEW_STATES,
        "migrationState": inv.MIGRATION_STATES,
        "migrationReason": inv.MIGRATION_REASONS,
    }
    for owner_type, owner_schema in owner_schemas.items():
        properties = owner_schema["properties"]
        actual_applicability = lifecycle_names & set(properties)
        expected_applicability = set(inv.APPLICABILITY[owner_type])
        if actual_applicability != expected_applicability:
            err("schema:axes", "%s lifecycle applicability %r != %r" %
                (owner_type, sorted(actual_applicability),
                 sorted(expected_applicability)))
        if not expected_applicability.issubset(set(owner_schema["required"])):
            err("schema:axes", "%s lifecycle fields are not all required"
                % owner_type)
        for field, expected_values in enum_sources.items():
            if field in properties and \
                    tuple(properties[field].get("enum", ())) != \
                    tuple(expected_values):
                err("schema:axes", "%s.%s enum drifts from invariants" %
                    (owner_type, field))
    operator_enum = relation_schema["definitions"]["review"]["properties"] \
        ["operatorKind"].get("enum", ())
    if tuple(operator_enum) != tuple(inv.REVIEW_OPERATOR_KINDS):
        err("schema:axes", "review.operatorKind enum drifts from invariants")

    # Edition input declarations are security boundaries, not just build
    # metadata.  Reject aliases and platform-dependent spellings before a
    # gateway normalizes them, and reject both exact and normalized
    # duplicates so one logical input has exactly one declared identity.
    declared = m.edition.get("declaredTransitiveInputs", [])
    seen_inputs = set()
    seen_normalized = set()
    for index, path in enumerate(declared):
        owner = "declaredTransitiveInputs[%d]" % index
        if not isinstance(path, str) or not path:
            continue  # schema validation reports the shape/empty value
        normalized = posixpath.normpath(path)
        unsafe = (
            "\x00" in path or "\\" in path or path.startswith("/") or
            re.match(r"^[A-Za-z]:", path) is not None or
            normalized in (".", "..") or normalized.startswith("../") or
            normalized != path or any(
                part in ("", ".", "..") for part in path.split("/")))
        if unsafe:
            err("inputs", "%s: unsafe or non-canonical relative path %r"
                % (owner, path))
        if path in seen_inputs or normalized in seen_normalized:
            err("inputs", "%s: duplicate declared input %r" % (owner, path))
        seen_inputs.add(path)
        seen_normalized.add(normalized)

    try:
        timepolicy.parse_utc_second(
            m.edition.get("declaredReleaseTimestamp"),
            "edition declaredReleaseTimestamp")
    except timepolicy.TimestampError as exc:
        err("edition", str(exc))

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
    pct_numbers = [b.meta.get("pctClaim") for b in pct]
    if pct_numbers != list(range(1, 19)):
        err("census", "whole PCT claim identities must be exactly 1..18; "
            "found %r" % pct_numbers)
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
    claim_corpus = m.edition["claimCorpus"]
    target_corpus = m.edition["targetCorpus"]
    for field, corpus_id, expected_role in (
            ("claimCorpus", claim_corpus, "fragment-source"),
            ("targetCorpus", target_corpus, "derivative")):
        entry = m.registry.entry(corpus_id)
        if entry.get("role") != expected_role or \
                entry.get("visibility") != "rendered":
            err("binding", "%s %r must be role %r with rendered visibility"
                % (field, corpus_id, expected_role))
    for profile_name, profile, expected in (
        ("claim segmentation profile", m.claim_profile, claim_corpus),
        ("target segmentation profile", m.target_profile, target_corpus),
        ("gate inventory", m.gates, claim_corpus),
        ("dependency map", m.deps, claim_corpus),
    ):
        if profile.get("corpusId") != expected:
            err("binding", "%s corpusId %r != edition corpus %r" %
                (profile_name, profile.get("corpusId"), expected))

    # ---- gate inventory endpoint currency -------------------------------
    if m.gates.get("profileDigest") != m.claim_profile_digest:
        err("inventory", "profileDigest stale (profile is %s)"
            % m.claim_profile_digest)
    seen_gate_ids = set()
    for gate in m.gates.get("gates", []):
        gid = gate.get("gateId", "<missing-gateId>")
        if gid in seen_gate_ids:
            err("duplicate", "inventory gateId %r is duplicated" % gid)
        seen_gate_ids.add(gid)
        source = gate.get("source") or {}
        src = m.quotable_anchor(source.get("block"))
        if src is None:
            err("inventory", "%s: source block %r is not a quotable block"
                % (gid, source.get("block")))
        elif source.get("textHash") != src.digest:
            err("inventory", "%s: source textHash stale for block %s"
                % (gid, source.get("block")))
        scope = gate.get("requiredScope")
        applies = gate.get("appliesTo") or {}

        # Applicability arrays have semantic identity keys; JSON object
        # equality alone cannot detect a repeated id carrying a different
        # hash.  Check both possible arrays even when the scope shape is
        # malformed so all duplicate subjects are reported in one pass.
        for collection, key in (("claims", "claim"), ("fragments", "id")):
            seen_subjects = set()
            for subject in applies.get(collection, []):
                subject_id = subject.get(key)
                if subject_id in seen_subjects:
                    err("duplicate", "%s: duplicate applicability subject %r"
                        % (gid, subject_id))
                seen_subjects.add(subject_id)

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
            if scope == "target" and "cardinality" in applies:
                minimum = applies.get("cardinality", {}).get(
                    "minTargetsPerFragment")
                if not isinstance(minimum, int) or isinstance(minimum, bool) \
                        or minimum < 1:
                    err("inventory", "%s: target cardinality must be an "
                        "integer >= 1" % gid)
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

    def check_forbidden_text(owner, field, text):
        if not isinstance(text, str):
            return
        for term in forbidden:
            if term.casefold() in text.casefold():
                err("forbidden-terms", "%s: %s contains forbidden term %r"
                    % (owner, field, term))

    def authored_strings(value, path):
        if isinstance(value, str):
            yield path, value
        elif isinstance(value, dict):
            for key in sorted(value):
                yield from authored_strings(value[key], "%s.%s" % (path, key))
        elif isinstance(value, (list, tuple)):
            for index, item in enumerate(value):
                yield from authored_strings(item, "%s[%d]" % (path, index))

    # Full authored visible surface. Pinned claim/disclosure quotations and
    # phrase text are deliberately absent: those are verbatim source text.
    strings_surface = projections.artifact_strings(m)
    strings_surface["migrationReasons"] = m.strings["migrationReasons"]
    for path, text in authored_strings(strings_surface, "strings"):
        check_forbidden_text("microcopy", path, text)
    for field in ("editionId", "displayName", "strategyName",
                  "strategyPrefix", "claimSetVersion", "artifactName"):
        check_forbidden_text("edition", field, m.edition.get(field))
    for corpus_id in (m.edition["claimCorpus"], m.edition["targetCorpus"],
                      m.edition["authorityCorpus"]):
        entry = m.registry.entry(corpus_id)
        check_forbidden_text("corpus", "%s.id" % corpus_id, corpus_id)
        for field in ("role", "version"):
            check_forbidden_text(
                "corpus", "%s.%s" % (corpus_id, field), entry.get(field))
        if corpus_id in (m.edition["claimCorpus"],
                         m.edition["targetCorpus"]):
            for path in entry.get("files", {}):
                check_forbidden_text(
                    "corpus", "%s.files" % corpus_id, path)

    def check_text_bounds(owner, field, text, limit):
        if len(text) > limit:
            err("bounds", "%s: %s exceeds %d chars" % (owner, field, limit))
        check_forbidden_text(owner, field, text)

    def check_caution(owner, caution, scope, frag_id=None, target_block=None,
                      claim_key=None):
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

            # An inventory match is not sufficient: the carried instance's
            # owner must also be one of the gate's hashed applicability
            # subjects.  Target and fragment gates are keyed by fragment;
            # claim gates are keyed by claim.  The only scope exception is
            # the documented target -> fragment fallback for an honest
            # no-candidate fragment with its matching reviewed disposition.
            if req_scope == "claim":
                listed = {"c%d" % c["claim"] for c in
                          entry["appliesTo"].get("claims", [])}
                applicable = claim_key is not None and claim_key in listed
                subject_label = claim_key or frag_id or "<unknown>"
            else:
                listed = {f["id"] for f in
                          entry["appliesTo"].get("fragments", [])}
                applicable = frag_id is not None and frag_id in listed
                subject_label = frag_id or claim_key or "<unknown>"
            if not applicable:
                err("caution", "%s: gate %s is not applicable to %s" %
                    (owner, gid, subject_label))

            if scope != req_scope:
                fragment = m.relation.get("fragments", {}).get(frag_id, {})
                fallback_ok = (
                    req_scope == "target" and scope == "fragment" and
                    applicable and
                    fragment.get("status") == "counsel-review-required" and
                    _has_disposition(
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

    def check_target(owner, frag_id, target, seen_blocks, seen_target_gates):
        block = target["block"]
        block_key = inv.target_block_key(owner, target)
        if block_key in seen_blocks:
            err("duplicate", "%s: duplicate target block %s" % (owner, block))
        seen_blocks.add(block_key)
        gate_key = inv.target_gate_key(owner, target)
        if gate_key is not None:
            if gate_key in seen_target_gates:
                err("duplicate", "%s: duplicate target gate assignment %r"
                    % (owner, gate_key))
            seen_target_gates.add(gate_key)
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
        seen_target_gates = set()
        for t in targets:
            check_target(fid, fid, t, seen_blocks, seen_target_gates)
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
            phrase_identity = inv.phrase_key(fid, pid)
            if phrase_identity in seen_pids:
                err("duplicate", "%s: duplicate phrase id %s" % (fid, pid))
            seen_pids.add(phrase_identity)
            text, occ = ph.get("text", ""), ph.get("occurrence", 0)
            if not isinstance(text, str) or not text.strip():
                err("phrase", "%s: phrase text must be non-empty" % pid)
                continue
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
            pseen_target_gates = set()
            for t in p_targets:
                check_target(pid, fid, t, pseen, pseen_target_gates)
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
            gate_identity = inv.owner_gate_key(ckey, gid)
            if gate_identity in seen_gids:
                err("duplicate", "%s: duplicate claim-gate" % owner)
            seen_gids.add(gate_identity)
            if gate.get("claimHash") != m.agg_hashes[num]:
                err("drift", "%s: claimHash stale" % owner)
            check_caution(owner, {
                "gateId": gid, "type": gate.get("type"),
                "code": gate.get("code"), "source": gate.get("source"),
            }, "claim", claim_key=ckey)

    # ---- dispositions: totality, honesty, uniqueness, pins --------------
    disp_index = {}
    for disp in m.relation.get("dispositions", []):
        key = inv.disposition_key(disp)
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

        # Optional means that the inventory does not require every listed
        # subject to carry the gate.  It does not license a reviewed
        # disposition to claim that evidence was carried when no matching
        # instance exists.  Mandatory gates receive the same reverse check in
        # direction 2 below; close the optional branch here so affirmative
        # dispositions are honest in both requirement modes.
        disposition = disp.get("disposition")
        if entry.get("requirement") == "optional" and disposition in (
                "carried-at-required-scope",
                "carried-at-fragment-fallback"):
            gid = entry["gateId"]
            scope = entry["requiredScope"]
            subject_id = subject["id"]
            carried = False
            required_count = 1
            carried_count = 0
            if disposition == "carried-at-fragment-fallback":
                caution = frags.get(subject_id, {}).get("caution") or {}
                carried = caution.get("gateId") == gid
            elif scope == "claim":
                carried = any(
                    gate.get("gateId") == gid for gate in
                    m.relation.get("claimGates", {}).get(subject_id, []))
            elif scope == "fragment":
                caution = frags.get(subject_id, {}).get("caution") or {}
                carried = caution.get("gateId") == gid
            else:  # target scope
                frag = frags.get(subject_id, {})
                all_targets = list(frag.get("targets", []))
                for phrase in frag.get("phrases", []):
                    all_targets.extend(phrase.get("targets", []))
                carrying = {
                    target.get("block") for target in all_targets
                    if target.get("caution", {}).get("gateId") == gid
                }
                minimum = entry.get("appliesTo", {}).get(
                    "cardinality", {}).get("minTargetsPerFragment")
                if isinstance(minimum, int) and not isinstance(minimum, bool) \
                        and minimum >= 1:
                    required_count = minimum
                carried_count = len(carrying)
                carried = carried_count >= required_count
            if not carried:
                if scope == "target" and \
                        disposition == "carried-at-required-scope":
                    detail = "%d matching target(s), requires at least %d" % (
                        carried_count, required_count)
                else:
                    detail = "no matching gate/caution instance"
                err("integrity", "%s: optional gate has affirmative %r "
                    "disposition but %s" % (owner, disposition, detail))

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
        elif scope in ("fragment", "target"):
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
                    minimum = gate.get("appliesTo", {}).get(
                        "cardinality", {}).get("minTargetsPerFragment")
                    if not isinstance(minimum, int) or \
                            isinstance(minimum, bool) or minimum < 1:
                        continue  # inventory/schema defect already reported
                    all_targets = list(frag.get("targets", []))
                    for phrase in frag.get("phrases", []):
                        all_targets.extend(phrase.get("targets", []))
                    carrying = {
                        t.get("block") for t in all_targets
                        if t.get("caution", {}).get("gateId") == gid
                    }
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
        proposal = fields.get("proposedFrom")
        if isinstance(proposal, dict):
            source_owner = proposal.get("owner")
            if isinstance(source_owner, dict):
                source_kind = source_owner.get("kind")
                source_id = source_owner.get("id")
                identity_pattern = {
                    "unit": FRAG_ID_RE,
                    "phrase": PHRASE_ID_RE,
                }.get(source_kind)
                if identity_pattern is not None and \
                        (not isinstance(source_id, str) or
                         identity_pattern.fullmatch(source_id) is None):
                    err("provenance", "%s %s: proposedFrom owner id %r "
                        "does not match kind %r" %
                        (otype, key, source_id, source_kind))
            if proposal.get("sourceEdition") == m.edition.get("editionId"):
                err("provenance", "%s %s: proposedFrom sourceEdition must "
                    "differ from the destination edition" % (otype, key))
        expected = m.content_hash(projection)
        defects = inv.release_ready(fields, expected)
        review = fields.get("review") or {}
        metadata_defects = inv.review_metadata_defects(review)
        for defect in metadata_defects:
            if "operatorKind" in defect:
                continue
            err("lifecycle", "%s %s: %s" % (otype, key, defect))
        if not authority.is_authoritative_operator_kind(
                review.get("operatorKind")) and not for_release:
            err("pending", "%s %s: authorized operator review required "
                "(review.operatorKind is %r)" %
                (otype, key, review.get("operatorKind")))
        migration_state = fields.get("migrationState")
        has_reason = "migrationReason" in fields
        if migration_state == "stale" and not has_reason:
            err("lifecycle", "%s %s: stale owner requires migrationReason"
                % (otype, key))
        if migration_state == "current" and has_reason:
            err("lifecycle", "%s %s: current owner forbids migrationReason"
                % (otype, key))
        if review.get("contentHash") != expected:
            err("content-hash", "%s %s: %s" % (
                otype, key,
                "stale review.contentHash" if review.get("contentHash")
                else "missing review.contentHash"))
        if for_release:
            for d in defects:
                if "contentHash" not in d and d not in metadata_defects:
                    err("release", "%s %s: %s" % (otype, key, d))
            for d in metadata_defects:
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
