"""Migration — the closed case table (TDD §10.6), action classes b + c only.

``migrate`` never guesses: mechanical re-anchoring happens only on a unique
canonical-hash match in the eligible set (relation target and caution-source
locators and gate-inventory source locators alike); every other situation
degrades to ``stale`` with a closed-enum reason (staleness rolls up to the
owning reviewed object) or a new ``pending`` proposal entry. Semantic
content and review state are never touched by re-anchoring — locators are
outside the review projection.

A canonVersion mismatch on the relation binding is ordinary staleness
(TDD §8.2) surfacing as ``stale / unclassified`` on every owner: no digest
comparison is meaningful across canon versions.
"""

from . import canon


def _unique_position(m, digest, current_block):
    positions = m.digest_positions.get(digest, [])
    if len(positions) == 1:
        return positions[0], False
    if current_block in positions:
        return current_block, len(positions) > 1
    return None, len(positions) > 1


def _stale(owner, reason, log, key):
    if owner.get("migrationState") != "stale":
        owner["migrationState"] = "stale"
        owner["migrationReason"] = reason
        log.append(("stale", key, reason))


def migrate_relation(m, log):
    """Apply the case table to the relation set in place. Returns log of
    (action, owner, detail) tuples."""
    rel = m.relation

    if rel.get("binding", {}).get("canonVersion") != canon.CANON_VERSION:
        # no digest comparison is meaningful across canon versions
        for _, key, fields, _ in m.iter_owners():
            _stale(fields, "unclassified", log, key)
        return log

    def retarget(owner, key, targets):
        for t in targets:
            anchor = m.target_anchor(t["block"])
            if anchor is not None and anchor.digest == t["textHash"]:
                continue  # current
            pos, ambiguous = _unique_position(m, t["textHash"], t["block"])
            if pos is not None and not ambiguous:
                if pos != t["block"]:
                    log.append(("re-anchor", key,
                                "%s -> %s" % (t["block"], pos)))
                    t["block"] = pos  # class b: locator only
                continue
            if ambiguous:
                _stale(owner, "ambiguous", log, key)
            elif anchor is None:
                _stale(owner, "target-removed", log, key)
            else:
                _stale(owner, "target-changed", log, key)
                owner.setdefault("previousTargets", []).append(dict(t))

    def recheck_caution(owner, key, caution):
        if not caution or caution.get("type") != "source-gate":
            return
        src = caution.get("source", {})
        anchor = m.quotable_anchor(src.get("block"))
        if anchor is not None and anchor.digest == src.get("textHash"):
            return
        # class b: caution-source locators re-anchor on a unique match
        positions = [a.id for a in m.guidance_order
                     if a.cls == "quotable" and a.digest == src.get("textHash")]
        if len(positions) == 1:
            log.append(("re-anchor", key,
                        "caution source %s -> %s" % (src.get("block"),
                                                     positions[0])))
            src["block"] = positions[0]
            return
        _stale(owner, "source-changed", log, key)

    for fid in sorted(rel.get("fragments", {})):
        frag = rel["fragments"][fid]
        unit = m.units.get(fid)
        if unit is None:
            _stale(frag, "fragment-removed", log, fid)
            continue
        if frag.get("fragmentTextHash") != unit.digest:
            _stale(frag, "changed", log, fid)
            frag.setdefault("previousTargets", []).extend(
                dict(t) for t in frag.get("targets", []))
        retarget(frag, fid, frag.get("targets", []))
        recheck_caution(frag, fid, frag.get("caution"))
        chain = m.chain_hashes.get(m.claim_of(fid))
        # ancestor-claim changes surface via the review projection; detect
        # endpoint change by recomputing the projection hash domain inputs
        for ph in frag.get("phrases", []):
            pid = ph.get("id", fid + "p?")
            if ph.get("text", "") not in unit.text:
                _stale(ph, "changed", log, pid)
            retarget(ph, pid, ph.get("targets", []))
            recheck_caution(ph, pid, ph.get("caution"))
        del chain

    for ckey in sorted(rel.get("claimGates", {})):
        num = int(ckey[1:])
        for gate in rel["claimGates"][ckey]:
            key = "%s/%s" % (ckey, gate.get("gateId"))
            if num not in m.agg_hashes:
                _stale(gate, "fragment-removed", log, key)
                continue
            if gate.get("claimHash") != m.agg_hashes[num]:
                _stale(gate, "endpoint-changed", log, key)
            recheck_caution(gate, key, {"type": "source-gate",
                                        "source": gate.get("source")})

    for disp in rel.get("dispositions", []):
        key = "disp:%s@%s" % (disp.get("gateId"),
                              disp.get("subject", {}).get("id"))
        entry = m.gates_by_id.get(disp.get("gateId"))
        if entry is None or disp.get("gateEntryHash") != \
                m.gate_entry_hash(disp["gateId"]):
            _stale(disp, "endpoint-changed", log, key)
            continue
        subject = disp["subject"]
        if subject["kind"] == "fragment":
            unit = m.units.get(subject["id"])
            current = unit.digest if unit else None
        else:
            current = m.agg_hashes.get(int(subject["id"][1:]))
        if disp.get("subjectHash") != current:
            _stale(disp, "endpoint-changed", log, key)

    # new fragments appear as counsel-review-required + pending (class c)
    for fid, unit in sorted(m.units.items()):
        if fid not in rel.get("fragments", {}):
            rel["fragments"][fid] = {
                "status": "counsel-review-required",
                "reviewState": "pending",
                "migrationState": "current",
                "review": {"by": "migrate", "date": "", "contentHash": ""},
                "fragmentTextHash": unit.digest,
            }
            log.append(("proposal", fid, "new fragment entry (pending)"))

    # owners whose review projection no longer matches (parent-claim
    # amendments, endpoint drift not caught above) -> endpoint-changed
    for otype, key, fields, projection in m.iter_owners():
        if fields.get("migrationState") == "stale":
            continue
        expected = m.content_hash(projection)
        review = fields.get("review") or {}
        if review.get("contentHash") and review["contentHash"] != expected:
            _stale(fields, "endpoint-changed", log, "%s %s" % (otype, key))
    return log


def migrate_inventory(m, log):
    """Gate-inventory source locators are eligible for mechanical
    re-anchoring under a unique canonical-hash match (class b)."""
    for gate in m.gates["gates"]:
        src = gate["source"]
        anchor = m.quotable_anchor(src["block"])
        if anchor is not None and anchor.digest == src["textHash"]:
            continue
        positions = [a.id for a in m.guidance_order
                     if a.cls == "quotable" and a.digest == src["textHash"]]
        if len(positions) == 1:
            if positions[0] != src["block"]:
                log.append(("re-anchor", "inventory:%s" % gate["gateId"],
                            "%s -> %s" % (src["block"], positions[0])))
                src["block"] = positions[0]
        else:
            log.append(("manual", "inventory:%s" % gate["gateId"],
                        "source block unresolved (%d matches)" % len(positions)))
    return log
