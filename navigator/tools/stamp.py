#!/usr/bin/env python3
"""Owner-scoped endpoint pinning and explicit operator review (class d).

The review path fills endpoint digests only for explicitly selected owners
and records an identified authorized human or model operator's approval of
the resulting projections.  There is no pin-only relation mode: silently
refreshing pins before migration would destroy the evidence used to classify
endpoint changes.  Gate-inventory pinning is a separate, explicit,
single-file operation.

Run by the author before committing authored data; never part of the build
pipeline (build commands are content-plane read-only). All digests come from
lib.canon through the model — the single digest path.

Usage: python3 navigator/tools/stamp.py <edition-config> --mark-reviewed \
           --owner=unit:c1u0 [--owner=phrase:c1u0p1 ...] \
           --reviewer=<identity> --review-date=YYYY-MM-DD \
           --operator-kind=<human|model>
       python3 navigator/tools/stamp.py <edition-config> --stamp-inventory
"""

import argparse
import datetime
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lib import authority, gateway, model  # noqa: E402


def dump(path, obj):
    """Atomically replace one authored JSON document."""
    directory = os.path.dirname(os.path.abspath(path))
    prefix = ".%s." % os.path.basename(path)
    fd, temporary = tempfile.mkstemp(prefix=prefix, suffix=".tmp",
                                     dir=directory, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, indent=1, ensure_ascii=False)
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())
        try:
            os.chmod(temporary, os.stat(path).st_mode & 0o777)
        except FileNotFoundError:
            pass
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def _review_metadata(reviewer, review_date, operator_kind):
    """Validate explicit reviewer metadata for an authoring review commit."""
    if not authority.is_identified_operator_identity(reviewer):
        raise SystemExit("--mark-reviewed requires a non-empty --reviewer")
    if not authority.is_authoritative_operator_kind(operator_kind):
        raise SystemExit("--operator-kind must be explicitly 'human' or "
                         "'model'; tool reviews cannot authorize a candidate")
    if not isinstance(review_date, str):
        raise SystemExit("--mark-reviewed requires --review-date=YYYY-MM-DD")
    try:
        parsed = datetime.date.fromisoformat(review_date)
    except ValueError:
        raise SystemExit("--review-date must be a real YYYY-MM-DD date")
    if parsed.isoformat() != review_date:
        raise SystemExit("--review-date must use canonical YYYY-MM-DD form")
    return reviewer, review_date, operator_kind


def _owner_selector(owner_type, key):
    return "%s:%s" % (owner_type, key)


def stamp(root, edition_path, mark_reviewed=False, owners=None,
          all_owners=False, reviewer=None, review_date=None,
          operator_kind=None, stamp_inventory=False):
    gw = gateway.ContentGateway(root)
    m = model.EditionModel(gw, edition_path)

    requested = list(owners or [])
    if mark_reviewed and stamp_inventory:
        raise SystemExit("--mark-reviewed and --stamp-inventory are separate "
                         "single-file operations")
    if not mark_reviewed and not stamp_inventory:
        raise SystemExit("choose --mark-reviewed or --stamp-inventory; "
                         "implicit pin-only stamping is forbidden")
    if not mark_reviewed and (requested or all_owners):
        raise SystemExit("--owner/--all-owners require --mark-reviewed")
    if not mark_reviewed and any(value is not None
                                 for value in (reviewer, review_date,
                                               operator_kind)):
        raise SystemExit("review metadata is valid only with --mark-reviewed")

    if stamp_inventory:
        gates = m.gates
        gates["profileDigest"] = m.claim_profile_digest
        for gate in gates["gates"]:
            src = m.quotable_anchor(gate["source"]["block"])
            if src is None:
                raise SystemExit("gate %s: source block %r not quotable"
                                 % (gate["gateId"], gate["source"]["block"]))
            gate["source"]["textHash"] = src.digest
            for claim in gate["appliesTo"].get("claims", []):
                claim["claimHash"] = m.agg_hashes[claim["claim"]]
            for fragment in gate["appliesTo"].get("fragments", []):
                fragment["hash"] = m.units[fragment["id"]].digest
        dump(os.path.join(root, m.edition["gateInventory"]), gates)
        print("stamped inventory %s (%d gates)" %
              (m.edition["editionId"], len(gates["gates"])))
        return

    metadata = _review_metadata(reviewer, review_date, operator_kind)
    if bool(requested) == bool(all_owners):
        raise SystemExit("--mark-reviewed requires exactly one of one-or-more "
                         "--owner selectors or --all-owners")

    owner_rows = list(m.iter_owners(with_projection=False))
    owner_map = {}
    duplicate_keys = []
    for owner_type, key, fields, unused in owner_rows:
        selector = _owner_selector(owner_type, key)
        if selector in owner_map:
            duplicate_keys.append(selector)
        owner_map[selector] = (owner_type, key, fields)
    if duplicate_keys:
        raise SystemExit("relation has duplicate owner identity/identities: %s"
                         % ", ".join(sorted(set(duplicate_keys))))
    if all_owners:
        selected = list(owner_map)
    else:
        selected = requested
        duplicates = sorted({selector for selector in selected
                             if selected.count(selector) > 1})
        if duplicates:
            raise SystemExit("duplicate --owner selector(s): %s" %
                             ", ".join(duplicates))
        unknown = sorted(set(selected) - set(owner_map))
        if unknown:
            raise SystemExit("unknown --owner selector(s): %s" %
                             ", ".join(unknown))

    unresolved = [selector for selector in selected
                  if owner_map[selector][2].get("migrationState") != "current"
                  or "migrationReason" in owner_map[selector][2]]
    if unresolved:
        sample = ", ".join(unresolved[:8])
        suffix = " ..." if len(unresolved) > 8 else ""
        raise SystemExit("cannot mark reviewed: resolve %d selected "
                         "stale/non-current owner(s) first (%s%s)" %
                         (len(unresolved), sample, suffix))

    rel = m.relation

    def stamp_caution(c):
        if c and c.get("type") == "source-gate":
            entry = m.gates_by_id[c["gateId"]]
            c["source"]["block"] = entry["source"]["block"]
            c["source"]["textHash"] = entry["source"]["textHash"]

    def stamp_targets(targets):
        for t in targets:
            anchor = m.target_anchor(t["block"])
            if anchor is None:
                raise SystemExit("unknown target block %r" % t["block"])
            t["textHash"] = anchor.digest
            stamp_caution(t.get("caution"))

    # Endpoint pins are changed only inside the same explicit operator action
    # that approves that selected owner.  Every unselected owner, including
    # pending proposals, retains its data and provenance byte-for-byte.
    for selector in selected:
        owner_type, key, fields = owner_map[selector]
        if owner_type == "unit":
            fields["fragmentTextHash"] = m.units[key].digest
            stamp_targets(fields.get("targets", []))
            stamp_caution(fields.get("caution"))
            projection = m.unit_projection(key, fields)
        elif owner_type == "phrase":
            fragment_id = key.split("p", 1)[0]
            fragment = rel["fragments"][fragment_id]
            stamp_targets(fields.get("targets", []))
            stamp_caution(fields.get("caution"))
            projection = m.phrase_projection(fragment_id, fragment, fields)
        elif owner_type == "claim-gate":
            claim_key = key.split("/", 1)[0]
            fields["claimHash"] = m.agg_hashes[int(claim_key[1:])]
            entry = m.gates_by_id[fields["gateId"]]
            fields["source"]["block"] = entry["source"]["block"]
            fields["source"]["textHash"] = entry["source"]["textHash"]
            projection = m.claim_gate_projection(claim_key, fields)
        else:
            fields["gateEntryHash"] = m.gate_entry_hash(fields["gateId"])
            subject = fields["subject"]
            if subject["kind"] == "fragment":
                fields["subjectHash"] = m.units[subject["id"]].digest
            else:
                fields["subjectHash"] = \
                    m.agg_hashes[int(subject["id"][1:])]
            projection = m.disposition_projection(fields)

        fields["reviewState"] = "internally-reviewed"
        fields["review"].update({
            "by": metadata[0],
            "date": metadata[1],
            "operatorKind": metadata[2],
            "contentHash": m.content_hash(projection),
        })
    dump(os.path.join(root, m.edition["relationSet"]), rel)
    print("marked %d owner(s) %s-reviewed in %s" %
          (len(selected), metadata[2], m.edition["editionId"]))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("edition_config")
    parser.add_argument("--mark-reviewed", action="store_true")
    parser.add_argument("--stamp-inventory", action="store_true")
    selectors = parser.add_mutually_exclusive_group()
    selectors.add_argument("--owner", action="append", default=[])
    selectors.add_argument("--all-owners", action="store_true")
    parser.add_argument("--reviewer")
    parser.add_argument("--review-date")
    parser.add_argument("--operator-kind", choices=("human", "model", "tool"))
    args = parser.parse_args(argv)
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    stamp(root, args.edition_config, mark_reviewed=args.mark_reviewed,
          owners=args.owner, all_owners=args.all_owners,
          reviewer=args.reviewer, review_date=args.review_date,
          operator_kind=args.operator_kind,
          stamp_inventory=args.stamp_inventory)


if __name__ == "__main__":
    main()
