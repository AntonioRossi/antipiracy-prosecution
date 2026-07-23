#!/usr/bin/env python3
"""Regenerate the required test fixtures (TDD §8.3) as verbatim excerpts of
the live relation sets, plus the five disposition fixtures and the golden
bundle fixture. Authoring tool (class d), run when live data changes; the
fixtures then validate against schemas and pinned corpora (AC-06) and the
TDD §8.3 code blocks are compared against the excerpt projections."""

import base64
import copy
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


def json_bytes(obj):
    return (json.dumps(obj, indent=1, ensure_ascii=False) + "\n").encode(
        "utf-8")


def edition_parameters(path, edition):
    """Locked projection of every normative §3 edition-table value."""
    return {
        "editionConfig": path,
        "claimCorpus": edition["claimCorpus"],
        "claimSetVersion": edition["claimSetVersion"],
        "targetCorpus": edition["targetCorpus"],
        "authorityCorpus": edition["authorityCorpus"],
        "corpusRegistries": edition["corpusRegistries"],
        "census": edition["census"],
        "independentClaims": edition["independentClaims"],
        "groups": edition["groups"],
        "strategyPrefix": edition["strategyPrefix"],
        "relationSet": edition["relationSet"],
        "gateInventory": edition["gateInventory"],
        "dependencyMap": edition["dependencyMap"],
        "qaSources": edition["qaSources"],
        "qaRegistry": edition["qaRegistry"],
        "stringsResource": edition["stringsResource"],
        "forbiddenTerms": edition["forbiddenTerms"],
        "artifactName": edition["artifactName"],
    }


def migration_snapshot(na_m):
    """Return an isolated NA content snapshot for AC-07 migration tests.

    Large authority/figure binaries are replaced with deterministic synthetic
    bytes and their registry pins are updated.  The migration behavior under
    test depends on the markdown and authored graph data, not image/PDF
    contents; keeping tiny stand-ins makes the fixture reviewable and fast.
    """
    edition_path = "navigator/editions/na.json"
    edition = copy.deepcopy(na_m.edition)
    files = {}
    skip_prefixes = ("navigator/lib/", "navigator/schema/")
    for path in edition["declaredTransitiveInputs"]:
        if path == "navigator/build.py" or path.startswith(skip_prefixes):
            continue
        with open(os.path.join(ROOT, path), "rb") as fh:
            files[path] = fh.read()

    qa_registry_path = edition["qaRegistry"]
    with open(os.path.join(ROOT, qa_registry_path), "rb") as fh:
        files[qa_registry_path] = fh.read()
    qa_registry = canon.parse_json(files[qa_registry_path])
    for corpus in qa_registry["corpora"].values():
        for path in corpus["files"]:
            with open(os.path.join(ROOT, path), "rb") as fh:
                files[path] = fh.read()

    registry_path = "navigator/corpora.json"
    registry = canon.parse_json(files[registry_path])
    authority_entry = registry["corpora"][edition["authorityCorpus"]]
    synthetic_files = {
        authority_entry["primary"]: b"synthetic migration authority\n",
    }
    target_entry = registry["corpora"][edition["targetCorpus"]]
    figure_paths = sorted(
        path for path in target_entry["files"] if path.endswith(".png"))
    for index, path in enumerate(figure_paths, 1):
        synthetic_files[path] = (
            "synthetic migration figure %d\n" % index).encode("ascii")
    for path, data in synthetic_files.items():
        files[path] = data
        for entry in registry["corpora"].values():
            if path in entry.get("files", {}):
                entry["files"][path] = canon.bytes_digest(data)
    files[registry_path] = json_bytes(registry)
    files[edition_path] = json_bytes(edition)

    claim_entry = na_m.registry.corpora[edition["claimCorpus"]]
    target_path = target_entry["primary"]
    return {
        "snapshotVersion": "1",
        "comment": "Locked synthetic NA content-plane baseline for AC-07; "
                   "it is independent of live NA edition inputs and is not "
                   "release evidence.",
        "editionPath": edition_path,
        "relationPath": edition["relationSet"],
        "gateInventoryPath": edition["gateInventory"],
        "claimPath": claim_entry["primary"],
        "targetPath": target_path,
        "files": {
            path: base64.b64encode(data).decode("ascii")
            for path, data in sorted(files.items())
        },
    }


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


def reviewed_excerpt(m, fragments, claims=()):
    """Create a projection-current documentation/test excerpt.

    This is fixture data only, never release evidence. Semantic fields remain
    verbatim excerpts of the live relation; lifecycle fields are normalized
    and hashed under the running schema-derived review projection so examples
    remain internally valid while the live relation may honestly be stale.
    Reviewer provenance is deliberately copied unchanged: the checked-in
    examples remain truthfully model-authored fixture projections and are not
    append-only review evidence for the live relation.
    """
    out = copy.deepcopy(excerpt(m.relation, fragments, claims))
    original = m.relation
    try:
        m.relation = out
        for unused_type, unused_key, fields, projection in m.iter_owners():
            fields["reviewState"] = "internally-reviewed"
            fields["migrationState"] = "current"
            fields.pop("migrationReason", None)
            fields.pop("previousTargets", None)
            fields["review"]["contentHash"] = m.content_hash(projection)
    finally:
        m.relation = original
    return out


def main():
    os.chdir(ROOT)
    os.makedirs(FIX, exist_ok=True)
    gw = gateway.ContentGateway(ROOT)
    na_m = model.EditionModel(gw, "navigator/editions/na.json")
    gw2 = gateway.ContentGateway(ROOT)
    af_m = model.EditionModel(gw2, "navigator/editions/af.json")

    for edition_id, edition_model in (("af", af_m), ("na", na_m)):
        dump("edition_parameters_%s.json" % edition_id, {
            "fixtureVersion": "1",
            "comment": "Locked exact projection of the normative §3 %s "
                       "edition parameter table." % edition_id.upper(),
            "edition": edition_parameters(
                "navigator/editions/%s.json" % edition_id,
                edition_model.edition),
        })
    dump("migration_na_snapshot.json", migration_snapshot(na_m))

    dump("na_excerpt.json", reviewed_excerpt(
        na_m, ["c9u6", "c16u6"], ["c9"]))
    dump("af_excerpt.json",
         reviewed_excerpt(
             af_m, ["c1u8", "c1u11", "c1u12"], ["c1", "c2"]))

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
        disposition = {
            "gateId": gate["gateId"],
            "subject": {"kind": subject_kind, "id": subject_id},
            "disposition": value,
            "gateEntryHash": canon.composite_digest(
                "aa11393:inventory:c1", na_m.gate_entry_projection(gate)),
            "subjectHash": subject_hash,
            "reviewState": "internally-reviewed",
            "migrationState": "current",
            "review": {"by": "fixture-generator", "operatorKind": "tool",
                       "date": "2026-07-21",
                       "contentHash": ""},
        }
        disposition["review"]["contentHash"] = na_m.content_hash(
            na_m.disposition_projection(disposition))
        return disposition

    def case(name, expect, disposition, evidence, has_targets):
        return {
            "name": name,
            "expect": expect,
            "evidence": evidence,
            "hasTargets": has_targets,
            "reviewProjection": na_m.disposition_projection(disposition),
            "disposition": disposition,
        }

    dump("dispositions_fixture.json", {
        "fixtureVersion": "1",
        "comment": "Five disposition fixtures over the requiredScope x "
                   "evidence-state matrix (TDD §8.1): one per enum value, "
                   "the honest no-candidate release case, and a rejected "
                   "wrong-scope case. Pinned to real corpora digests; "
                   "tool-authored fixture provenance is not release "
                   "authorization.",
        "edition": "na",
        "binding": copy.deepcopy(na_m.binding),
        "gates": fixture_gates,
        "cases": [
            case("carried-at-required-scope (claim scope)", "valid",
                 disp(gate_claim, "claim", "c9",
                      "carried-at-required-scope", na_m.agg_hashes[9]),
                 "mapped", True),
            case("carried-at-required-scope (target scope, mapped)",
                 "valid", disp(gate_target, "fragment", unit_mapped,
                               "carried-at-required-scope",
                               na_m.units[unit_mapped].digest),
                 "mapped", True),
            case("carried-at-fragment-fallback (no-candidate fragment)",
                 "valid", disp(gate_target, "fragment", unit_crr,
                               "carried-at-fragment-fallback",
                               na_m.units[unit_crr].digest),
                 "counsel-review-required", False),
            case("no-target-recorded releases without a fabricated mapping",
                 "valid", disp(gate_target, "fragment", unit_crr,
                               "no-target-recorded",
                               na_m.units[unit_crr].digest),
                 "counsel-review-required", False),
            case("wrong scope: no-target-recorded over a mapped fragment is "
                 "rejected", "invalid",
                 disp(gate_target, "fragment", unit_mapped,
                      "no-target-recorded", na_m.units[unit_mapped].digest),
                 "mapped", True),
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
