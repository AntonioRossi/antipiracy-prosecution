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

import copy

from . import canon


_MISSING = object()


def _json_differences(before, after, path=()):
    """Yield atomic structural changes, keeping added/removed subtrees whole."""
    if isinstance(before, dict) and isinstance(after, dict):
        for key in sorted(set(before) | set(after)):
            if key not in before:
                yield path + (key,), _MISSING, after[key]
            elif key not in after:
                yield path + (key,), before[key], _MISSING
            else:
                yield from _json_differences(
                    before[key], after[key], path + (key,))
        return
    if isinstance(before, list) and isinstance(after, list) and \
            len(before) == len(after):
        for index, (old, new) in enumerate(zip(before, after)):
            yield from _json_differences(old, new, path + (index,))
        return
    if before != after:
        yield path, before, after


def _owner_lifecycle_path(path, field):
    if not path or path[-1] != field:
        return False
    return (
        (len(path) == 3 and path[0] == "fragments") or
        (len(path) == 5 and path[0] == "fragments" and
         path[2] == "phrases" and isinstance(path[3], int)) or
        (len(path) == 4 and path[0] == "claimGates" and
         isinstance(path[2], int)) or
        (len(path) == 3 and path[0] == "dispositions" and
         isinstance(path[1], int))
    )


def _relation_locator_path(path):
    if not path or path[-1] != "block":
        return False
    if len(path) >= 4 and path[-3:-1] == ("caution", "source"):
        return True
    if len(path) >= 3 and path[-2] == "source" and \
            path[0] == "claimGates":
        return True
    return len(path) >= 3 and isinstance(path[-2], int) and \
        path[-3] == "targets"


def _lookup(value, path):
    for part in path:
        value = value[part]
    return value


def migration_diff_problems(before_relation, after_relation,
                            before_inventory, after_inventory,
                            fragment_hashes=None):
    """Classify every migrate write under the closed b/c action taxonomy.

    Class b may replace existing block locators only. Class c may add the
    exact pending-new-fragment shape, mark an existing owner stale with a
    reason, and add an immutable snapshot equal to that owner's old targets.
    Any semantic/review mutation is rejected before source files are written.
    """
    problems = []
    for path, old, new in _json_differences(
            before_inventory, after_inventory):
        allowed = (
            len(path) == 4 and path[0] == "gates" and
            isinstance(path[1], int) and path[2:] == ("source", "block") and
            isinstance(old, str) and isinstance(new, str))
        if not allowed:
            problems.append("inventory change outside class b at %r" %
                            (path,))

    for path, old, new in _json_differences(before_relation, after_relation):
        if _relation_locator_path(path) and isinstance(old, str) and \
                isinstance(new, str):
            continue
        if _owner_lifecycle_path(path, "migrationState") and \
                old is not _MISSING and new == "stale":
            continue
        if _owner_lifecycle_path(path, "migrationReason") and \
                new is not _MISSING and isinstance(new, str) and new:
            after_owner = _lookup(after_relation, path[:-1])
            if after_owner.get("migrationState") == "stale":
                continue
        if path and path[-1] == "previousTargets" and new is not _MISSING \
                and old is _MISSING and (
                    (len(path) == 3 and path[0] == "fragments") or
                    (len(path) == 5 and path[0] == "fragments" and
                     path[2] == "phrases" and isinstance(path[3], int))):
            parent_path = path[:-1]
            old_owner = _lookup(before_relation, parent_path)
            after_owner = _lookup(after_relation, parent_path)
            if new == old_owner.get("targets", []) and \
                    after_owner.get("migrationState") == "stale":
                continue
            problems.append("previousTargets is not the pre-migration "
                            "target snapshot at %r" % (path,))
            continue
        if len(path) == 2 and path[0] == "fragments" and \
                old is _MISSING and isinstance(new, dict):
            expected_fields = {
                "status", "reviewState", "migrationState", "review",
                "fragmentTextHash",
            }
            review = new.get("review")
            proposal_ok = (
                set(new) == expected_fields and
                new.get("status") == "counsel-review-required" and
                new.get("reviewState") == "pending" and
                new.get("migrationState") == "current" and
                review == {"by": "migrate", "operatorKind": "tool",
                           "date": "", "contentHash": ""})
            try:
                canon.parse_digest(new.get("fragmentTextHash"))
            except (canon.CanonError, TypeError, ValueError):
                proposal_ok = False
            if fragment_hashes is not None and \
                    new.get("fragmentTextHash") != fragment_hashes.get(path[1]):
                proposal_ok = False
            if proposal_ok:
                continue
        problems.append("relation change outside action classes b/c at %r" %
                        (path,))
    return problems


def _unique_position(m, digest, current_block):
    positions = m.digest_positions.get(digest, [])
    if len(positions) == 1:
        return positions[0], False
    if current_block in positions:
        return current_block, len(positions) > 1
    return None, len(positions) > 1


def _stale(owner, reason, log, key, force=False):
    previous_state = owner.get("migrationState")
    previous_reason = owner.get("migrationReason")
    # Projection-wide endpoint drift is deliberately the least-specific
    # fallback.  If a later migration observes the concrete missing/changed
    # endpoint, retain that stronger diagnosis and make the mutation visible
    # to the caller even though the owner was already stale.
    improves_diagnosis = (previous_reason in (None, "endpoint-changed") and
                           reason != previous_reason)
    if previous_state != "stale" or improves_diagnosis or \
            (force and previous_reason != reason):
        owner["migrationState"] = "stale"
        owner["migrationReason"] = reason
        log.append(("stale", key, reason))


def _preserve_targets(owner, targets):
    """Snapshot prior target state once.

    Migration is idempotent: rerunning it on an already-stale owner must not
    append another copy of the same prior targets.
    """
    if "previousTargets" not in owner:
        owner["previousTargets"] = copy.deepcopy(list(targets))


def migrate_relation(m, log):
    """Apply the case table to the relation set in place. Returns log of
    (action, owner, detail) tuples."""
    rel = m.relation

    if rel.get("binding", {}).get("canonVersion") != canon.CANON_VERSION:
        # no digest comparison is meaningful across canon versions
        for _, key, fields, _ in m.iter_owners(with_projection=False):
            _stale(fields, "unclassified", log, key, force=True)
        return log

    def retarget(owner, key, targets):
        snapshot = copy.deepcopy(list(targets))
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
                _preserve_targets(owner, snapshot)
            elif anchor is None:
                _stale(owner, "target-removed", log, key)
                _preserve_targets(owner, snapshot)
            else:
                _stale(owner, "target-changed", log, key)
                _preserve_targets(owner, snapshot)
        for t in targets:
            recheck_caution(owner, key, t.get("caution"))

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
            _preserve_targets(frag, frag.get("targets", []))
            for ph in frag.get("phrases", []):
                _stale(ph, "fragment-removed", log,
                       ph.get("id", fid + "p?"))
                _preserve_targets(ph, ph.get("targets", []))
            continue
        if frag.get("fragmentTextHash") != unit.digest:
            _stale(frag, "changed", log, fid)
            _preserve_targets(frag, frag.get("targets", []))
        retarget(frag, fid, frag.get("targets", []))
        recheck_caution(frag, fid, frag.get("caution"))
        # ancestor-claim changes surface via the review projection; detect
        # endpoint change by recomputing the projection hash domain inputs
        for ph in frag.get("phrases", []):
            pid = ph.get("id", fid + "p?")
            text = ph.get("text", "")
            occurrence = ph.get("occurrence", 0)
            count = unit.text.count(text) if text else 0
            if occurrence < 1 or count < occurrence:
                _stale(ph, "changed", log, pid)
                _preserve_targets(ph, ph.get("targets", []))
            retarget(ph, pid, ph.get("targets", []))
            recheck_caution(ph, pid, ph.get("caution"))

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
                "review": {"by": "migrate", "operatorKind": "tool",
                           "date": "", "contentHash": ""},
                "fragmentTextHash": unit.digest,
            }
            log.append(("proposal", fid, "new fragment entry (pending)"))

    # owners whose review projection no longer matches (parent-claim
    # amendments, endpoint drift not caught above) -> endpoint-changed
    for otype, key, fields, projection in m.iter_owners(skip_stale=True):
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
