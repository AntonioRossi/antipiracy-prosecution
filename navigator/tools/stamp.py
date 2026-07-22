#!/usr/bin/env python3
"""Authoring endpoint-pinning tool (action class d: human edit via git).

Fills endpoint digests (fragment/claim/target/caution-source hashes,
inventory profileDigest, disposition pins) from the pinned corpora and
computes ``review.contentHash`` over each owner's review projection. Run by
the author before committing authored data; never part of the build
pipeline (build commands are content-plane read-only). All digests come
from lib.canon through the model — the single digest path.

Usage: python3 navigator/tools/stamp.py <edition-config> [--mark-reviewed]
"""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lib import gateway, model  # noqa: E402


def dump(path, obj):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1, ensure_ascii=False)
        fh.write("\n")


def stamp(root, edition_path, mark_reviewed=False):
    os.chdir(root)
    gw = gateway.ContentGateway(".")
    m = model.EditionModel(gw, edition_path)

    # --- 1. gate inventory ------------------------------------------------
    gates = m.gates
    gates["profileDigest"] = m.claim_profile_digest
    for gate in gates["gates"]:
        src = m.quotable_anchor(gate["source"]["block"])
        if src is None:
            raise SystemExit("gate %s: source block %r not quotable"
                             % (gate["gateId"], gate["source"]["block"]))
        gate["source"]["textHash"] = src.digest
        for c in gate["appliesTo"].get("claims", []):
            c["claimHash"] = m.agg_hashes[c["claim"]]
        for f in gate["appliesTo"].get("fragments", []):
            f["hash"] = m.units[f["id"]].digest
    dump(m.edition["gateInventory"], gates)

    # --- 2. relation set: endpoint digests --------------------------------
    gw2 = gateway.ContentGateway(".")
    m = model.EditionModel(gw2, edition_path)  # reload with stamped gates
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

    for fid, frag in rel["fragments"].items():
        frag["fragmentTextHash"] = m.units[fid].digest
        stamp_targets(frag.get("targets", []))
        stamp_caution(frag.get("caution"))
        for ph in frag.get("phrases", []):
            stamp_targets(ph.get("targets", []))
            stamp_caution(ph.get("caution"))
    for ckey, gates_list in rel["claimGates"].items():
        for g in gates_list:
            g["claimHash"] = m.agg_hashes[int(ckey[1:])]
            entry = m.gates_by_id[g["gateId"]]
            g["source"]["block"] = entry["source"]["block"]
            g["source"]["textHash"] = entry["source"]["textHash"]
    for disp in rel["dispositions"]:
        disp["gateEntryHash"] = m.gate_entry_hash(disp["gateId"])
        if disp["subject"]["kind"] == "fragment":
            disp["subjectHash"] = m.units[disp["subject"]["id"]].digest
        else:
            disp["subjectHash"] = m.agg_hashes[int(disp["subject"]["id"][1:])]

    # --- 3. review contentHash over the (now-pinned) projections ----------
    for otype, key, fields, projection in m.iter_owners():
        if mark_reviewed:
            fields["reviewState"] = "internally-reviewed"
        fields["review"]["contentHash"] = m.content_hash(projection)
    dump(m.edition["relationSet"], rel)
    print("stamped %s (%d fragments, %d dispositions%s)"
          % (m.edition["editionId"], len(rel["fragments"]),
             len(rel["dispositions"]),
             ", marked reviewed" if mark_reviewed else ""))


if __name__ == "__main__":
    edition = sys.argv[1]
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    stamp(root, edition, mark_reviewed="--mark-reviewed" in sys.argv)
