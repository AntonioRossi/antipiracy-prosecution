#!/usr/bin/env python3
"""Regenerate the required test fixtures (TDD §8.3) as verbatim excerpts of
the live relation sets, plus the five disposition fixtures and the golden
bundle fixture. Authoring tool (class d), run when live data changes; the
fixtures then validate against schemas and pinned corpora (AC-06) and the
TDD §8.3 code blocks are compared against the excerpt projections."""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lib import bundlezip, canon, gateway, model  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FIX = os.path.join(ROOT, "navigator", "tests", "fixtures")


def dump(name, obj):
    with open(os.path.join(FIX, name), "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print("fixture", name)


def excerpt(rel, fragments, claims=()):
    out = {"binding": rel["binding"], "claimGates": {}, "fragments": {},
           "dispositions": []}
    for c in claims:
        out["claimGates"][c] = rel["claimGates"][c]
    for f in fragments:
        out["fragments"][f] = rel["fragments"][f]
    subjects = set(fragments) | set(claims)
    for d in rel["dispositions"]:
        if d["subject"]["id"] in subjects:
            out["dispositions"].append(d)
    return out


def main():
    os.chdir(ROOT)
    os.makedirs(FIX, exist_ok=True)
    gw = gateway.ContentGateway(ROOT)
    na_m = model.EditionModel(gw, "navigator/editions/na.json")
    gw2 = gateway.ContentGateway(ROOT)
    af_m = model.EditionModel(gw2, "navigator/editions/af.json")

    dump("na_excerpt.json", excerpt(na_m.relation, ["c9u6", "c16u6"], ["c9"]))
    dump("af_excerpt.json",
         excerpt(af_m.relation, ["c1u8", "c1u11", "c1u12"], ["c1", "c2"]))

    # Five disposition fixtures (§8.1): synthetic gate compositions pinned
    # to real corpora hashes; the wrong-scope case is expected-invalid.
    unit_mapped = "c2u0"          # NA: mapped, carries example2-priority
    unit_crr = "c16u6"            # NA: honest no-candidate fragment
    gate_target = {
        "gateId": "fx-gate-target", "code": "example2-priority",
        "requiredScope": "target", "requirement": "mandatory",
        "source": dict(na_m.gates["gates"][0]["source"]),
        "appliesTo": {
            "fragments": [
                {"id": unit_mapped, "hash": na_m.units[unit_mapped].digest},
                {"id": unit_crr, "hash": na_m.units[unit_crr].digest},
            ],
            "cardinality": {"minTargetsPerFragment": 1},
        },
    }
    gate_claim = {
        "gateId": "fx-gate-claim", "code": "combined-example",
        "requiredScope": "claim", "requirement": "mandatory",
        "source": dict(na_m.gates_by_id["na-gate-combined-example"]["source"]),
        "appliesTo": {"claims": [
            {"claim": 9, "claimHash": na_m.agg_hashes[9]},
        ]},
    }
    fixture_gates = {
        "inventoryVersion": "1", "corpusId": "na-claims",
        "profileDigest": na_m.gates["profileDigest"],
        "gates": [gate_target, gate_claim],
    }

    def disp(gate, subject_kind, subject_id, value, subject_hash):
        return {
            "gateId": gate["gateId"],
            "subject": {"kind": subject_kind, "id": subject_id},
            "disposition": value,
            "gateEntryHash": canon.composite_digest(
                "aa11393:inventory:c1", model.gate_entry_projection(gate)),
            "subjectHash": subject_hash,
            "reviewState": "internally-reviewed",
            "migrationState": "current",
            "review": {"by": "fixture", "date": "2026-07-21",
                       "contentHash": "sha256/c1:" + "0" * 64},
        }

    dump("dispositions_fixture.json", {
        "comment": "Five disposition fixtures over the requiredScope x "
                   "evidence-state matrix (TDD §8.1): one per enum value, "
                   "the honest no-candidate release case, and a rejected "
                   "wrong-scope case. Pinned to real corpora digests.",
        "gates": fixture_gates,
        "cases": [
            {"name": "carried-at-required-scope (claim scope)",
             "expect": "valid",
             "disposition": disp(gate_claim, "claim", "c9",
                                 "carried-at-required-scope",
                                 na_m.agg_hashes[9])},
            {"name": "carried-at-required-scope (target scope, mapped)",
             "expect": "valid",
             "disposition": disp(gate_target, "fragment", unit_mapped,
                                 "carried-at-required-scope",
                                 na_m.units[unit_mapped].digest)},
            {"name": "carried-at-fragment-fallback (no-candidate fragment)",
             "expect": "valid",
             "disposition": disp(gate_target, "fragment", unit_crr,
                                 "carried-at-fragment-fallback",
                                 na_m.units[unit_crr].digest)},
            {"name": "no-target-recorded releases without a fabricated "
                     "mapping",
             "expect": "valid",
             "disposition": disp(gate_target, "fragment", unit_crr,
                                 "no-target-recorded",
                                 na_m.units[unit_crr].digest)},
            {"name": "wrong scope: no-target-recorded over a mapped "
                     "fragment is rejected",
             "expect": "invalid",
             "disposition": disp(gate_target, "fragment", unit_mapped,
                                 "no-target-recorded",
                                 na_m.units[unit_mapped].digest)},
        ],
    })

    # Golden bundle fixture: byte-exact deterministic STORE ZIP
    members = [("a.txt", b"alpha\n"), ("b/beta.txt", b"beta\n")]
    zip_bytes = bundlezip.build_zip(members, "2026-07-21T00:00:00Z")
    dump("golden_bundle.json", {
        "comment": "Byte-exact golden fixture for the deterministic STORE "
                   "ZIP writer (TDD §10.9).",
        "members": [[n, d.decode("ascii")] for n, d in members],
        "declaredTimestamp": "2026-07-21T00:00:00Z",
        "sha256": canon.bytes_digest(zip_bytes),
        "hex": zip_bytes.hex(),
    })

    # Adversarial escaping fixture: authored-channel payloads
    dump("escaping_fixture.json", {
        "comment": "Adversarial payloads for every authored/quoted channel "
                   "(AC-09). The renderer must neutralize each.",
        "payloads": [
            "<script>alert(1)</script>",
            "</script><script>alert(2)</script>",
            "\" onmouseover=\"alert(3)",
            "<img src=x onerror=alert(4)>",
            "&lt;already-escaped&gt; & <b>bold</b>",
            "`code`**bold**<i>i</i>",
            "line sep  para </ScRiPt >",
        ],
    })


if __name__ == "__main__":
    main()
