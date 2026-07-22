#!/usr/bin/env python3
"""AA11393US claims navigator — build pipeline (TDD §10, §11, §13).

Content plane: ``preview`` / ``candidate`` / ``migrate``; verification
plane: ``attest`` / ``record-qa`` / ``release`` / ``bundle``. All file
traffic goes through the gateways; the command x kind privilege matrix
(schema/planes.json) is enforced there. Build commands are content-plane
read-only. ``propose-reuse`` is deferred (TDD §10.7).

Confidentiality guardrail (TDD §10.16): the build aborts in CI
environments; ``--private-runner`` is the logged override.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import canon, gateway, model, render, validate  # noqa: E402
from lib import migrate as migrate_mod, projections, release as release_mod  # noqa: E402
from lib import bundlezip  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "navigator", "dist")
RECORDS = os.path.join(ROOT, "navigator", "records")
CI_MARKERS = ("CI", "GITHUB_ACTIONS", "GITLAB_CI", "JENKINS_URL",
              "BUILDKITE", "CIRCLECI", "TRAVIS", "TEAMCITY_VERSION")


def ci_guard(argv):
    hits = [k for k in CI_MARKERS if os.environ.get(k)]
    if hits and "--private-runner" not in argv:
        raise SystemExit(
            "CI environment detected (%s): builds run locally or on a "
            "firm-approved private runner only. Override (logged): "
            "--private-runner" % ", ".join(hits))
    if hits:
        sys.stderr.write("[logged override] --private-runner on %s\n"
                         % ", ".join(hits))


def load_planes():
    return json.loads(
        gateway.ContentGateway(ROOT).read_text("navigator/schema/planes.json"))


def edition_path(edition_id):
    return "navigator/editions/%s.json" % edition_id


def build_model(edition_id, planes=None):
    boot = gateway.ContentGateway(ROOT)
    allow = json.loads(
        boot.read_text(edition_path(edition_id)))["declaredTransitiveInputs"]
    gw = gateway.ContentGateway(ROOT, allowlist=allow)
    m = model.EditionModel(gw, edition_path(edition_id))
    return gw, m


def derive(edition_id, mode):
    """Shared derivation for preview/candidate/release: validate, render,
    lock, exact-set check. Returns (m, html_bytes, lock)."""
    gw, m = build_model(edition_id)
    errors = validate.validate_edition(m)
    if errors:
        for code, msg in errors:
            sys.stderr.write("  [%s] %s\n" % (code, msg))
        raise SystemExit("%s: %d validation defect(s); build refused"
                         % (edition_id, len(errors)))
    html = render.render(m, mode="preview" if mode == "preview" else "candidate")
    lock = gw.lock()
    problems = release_mod.exact_set_check(
        lock, m.edition["declaredTransitiveInputs"])
    if problems:
        for p in problems:
            sys.stderr.write("  [exact-set] %s\n" % p)
        raise SystemExit("%s: exact-set check failed" % edition_id)
    return m, html, lock


def cmd_preview(edition_id, argv):
    planes = load_planes()
    m, html, _ = derive(edition_id, "preview")
    out = gateway.OutputGateway(DIST, "preview", planes)
    name = "preview_" + m.edition["artifactName"]
    digest = out.write("preview", name, html)
    print("preview %s -> dist/%s (%s)" % (edition_id, name, digest[:20]))


def cmd_candidate(edition_id, argv):
    planes = load_planes()
    m, html, lock = derive(edition_id, "candidate")
    out = gateway.OutputGateway(DIST, "candidate", planes)
    name = "candidate_" + m.edition["artifactName"]
    digest = out.write("candidate", name, html)
    print("candidate %s -> dist/%s" % (edition_id, name))
    print("  candidateDigest %s" % digest)
    print("  lockDigest %s" % lock["lockDigest"])


def cmd_migrate(edition_id, argv):
    gw, m = build_model(edition_id)
    log = []
    migrate_mod.migrate_inventory(m, log)
    migrate_mod.migrate_relation(m, log)
    for action, key, detail in log:
        print("  %-10s %-28s %s" % (action, key, detail))
    if not log:
        print("migrate %s: nothing to do" % edition_id)
        return
    # class b/c writes to the edition's relation set + inventory locators
    planes = load_planes()
    for path, obj in ((m.edition["relationSet"], m.relation),
                      (m.edition["gateInventory"], m.gates)):
        gateway.write_source("migrate", planes, ROOT, path,
                             json.dumps(obj, indent=1, ensure_ascii=False)
                             + "\n")
    print("migrate %s: %d action(s) applied" % (edition_id, len(log)))


ATTEST_TYPES = ("inventory-completeness", "qa-priority-map", "qa-crosswalk",
                "legend-approval", "manifest-approval",
                "support-matrix-approval")


def cmd_attest(argv):
    atype = argv[0]
    edition_id = argv[1] if len(argv) > 1 and not argv[1].startswith("--") \
        else None
    note = ""
    for a in argv:
        if a.startswith("--note="):
            note = a[len("--note="):]
    if atype not in ATTEST_TYPES:
        raise SystemExit("unknown attestation type %r" % atype)
    planes = load_planes()
    gw = gateway.ContentGateway(ROOT)  # attest reads content w/o allowlist
    sides = {}
    if atype == "inventory-completeness":
        _, m = build_model(edition_id)
        entry = m.registry.entry(m.edition["claimCorpus"])
        sides["claimSet"] = entry["files"][entry["primary"]]
        sides["gateInventory"] = m.gw.read_log[m.edition["gateInventory"]]
    elif atype == "qa-priority-map":
        _, m = build_model(edition_id)
        qa_id = m.edition["qaSources"]["priorityMap"]
        reg = json.loads(gw.read_text("navigator/corpora.json"))["corpora"]
        entry = reg[qa_id]
        gw.read_bytes(entry["primary"])  # consult the map (read logged)
        sides["relationSet"] = m.gw.read_log[m.edition["relationSet"]]
        sides["priorityMap"] = entry["files"][entry["primary"]]
    elif atype == "qa-crosswalk":
        _, m = build_model(edition_id)
        qa_id = m.edition["qaSources"]["crosswalk"]
        reg = json.loads(gw.read_text("navigator/corpora.json"))["corpora"]
        entry = reg[qa_id]
        gw.read_bytes(entry["primary"])
        sides["relationSet"] = m.gw.read_log[m.edition["relationSet"]]
        sides["crosswalk"] = entry["files"][entry["primary"]]
    elif atype == "legend-approval":
        strings = json.loads(gw.read_text("navigator/strings.json"))
        sides["legendWording"] = canon.text_digest(
            canon.canon_prose(strings["counselLegend"]))
    elif atype == "manifest-approval":
        strings = json.loads(gw.read_text("navigator/strings.json"))
        sides["manifestWording"] = canon.text_digest(
            canon.canon_prose(strings["bundleManifestText"]))
    elif atype == "support-matrix-approval":
        data = gw.read_bytes("navigator/schema/support-matrix.json")
        sides["supportMatrix"] = canon.bytes_digest(data)
    vgw = gateway.VerificationGateway(RECORDS, "attest", planes)
    record = {"type": atype, "edition": edition_id, "sides": sides,
              "note": note, "operator": operator_id()}
    digest, name = vgw.append("attestation", record)
    print("attestation %s -> records/%s\n  %s" % (atype, name, digest))


def operator_id():
    return os.environ.get("NAV_OPERATOR", "claude-opus-4.8")


def cmd_record_qa(edition_id, argv):
    planes = load_planes()
    m, html, lock = derive(edition_id, "candidate")
    name = "candidate_" + m.edition["artifactName"]
    if not os.path.exists(os.path.join(DIST, name)):
        raise SystemExit("no candidate found at dist/%s" % name)
    candidate_bytes = gateway.ArtifactGateway(
        DIST, "record-qa", planes).read("candidate", name)
    if candidate_bytes != html:
        raise SystemExit("dist/%s does not match the current derivation; "
                         "rebuild the candidate first" % name)
    candidate_digest = canon.bytes_digest(candidate_bytes)
    # complete lock, including the internal QA sources consulted
    qa_reads = {}
    reg = m.registry.corpora
    for role_key, qa_id in m.edition["qaSources"].items():
        entry = reg[qa_id]
        qa_reads[qa_id] = entry["files"][entry["primary"]]
    vgw = gateway.VerificationGateway(RECORDS, "record-qa", planes)
    # the envelope references only CURRENT attestations — superseded ones
    # persist in the append-only store but are never referenced (TDD §13)
    side_digests = current_side_digests(m)
    attestations = [a["digest"] for a in vgw.read_all("attestation")
                    if a["record"].get("edition") in (edition_id, None) and
                    not release_mod.attestation_current(a, side_digests)]
    fields = {}
    for a in argv:
        if a.startswith("--ac") and "=" in a:
            k, v = a[2:].split("=", 1)
            fields[k] = v
    record = {
        "edition": edition_id,
        "candidateDigest": candidate_digest,
        "lockDigest": lock["lockDigest"],
        "contentLock": lock["reads"],
        "internalQaSources": qa_reads,
        "reproductionDiagnostics": release_mod.reproduction_diagnostics(),
        "attestations": sorted(attestations),
        "supportMatrix": {
            "digest": canon.bytes_digest(m.support_matrix_bytes),
            "approver": json.loads(m.support_matrix_bytes)["approver"],
        },
        "manualChecks": fields,
        "operator": operator_id(),
    }
    digest, rname = vgw.append("qa-record", record)
    print("qa-record %s -> records/%s\n  %s" % (edition_id, rname, digest))


def cmd_release(edition_id, argv):
    planes = load_planes()
    m, html, lock = derive(edition_id, "release")
    name = "candidate_" + m.edition["artifactName"]
    if not os.path.exists(os.path.join(DIST, name)):
        raise SystemExit("no candidate to release")
    candidate_bytes = gateway.ArtifactGateway(
        DIST, "release", planes).read("candidate", name)
    if candidate_bytes != html:
        raise SystemExit("release derivation does not byte-match the QA'd "
                         "candidate")
    candidate_digest = canon.bytes_digest(candidate_bytes)
    vgw = gateway.VerificationGateway(RECORDS, "release", planes)
    qa_records = [r for r in vgw.read_all("qa-record")
                  if r["record"]["edition"] == edition_id and
                  r["record"]["candidateDigest"] == candidate_digest and
                  r["record"]["lockDigest"] == lock["lockDigest"]]
    if not qa_records:
        raise SystemExit("no qa-record authorizes this derivation (candidate "
                         "+ lock) for %s: run record-qa first" % edition_id)
    qa = qa_records[-1]
    attestations = vgw.read_all("attestation")
    problems = release_mod.verify_envelope(
        qa, candidate_digest, lock["lockDigest"], attestations)
    # attestation sufficiency, not universality: for each required type a
    # CURRENT double-sided attestation must exist; superseded attestations
    # persist in the append-only store and are ignored (TDD §10)
    side_digests = current_side_digests(m)
    required = ["inventory-completeness", "qa-priority-map",
                "legend-approval", "support-matrix-approval"]
    if "crosswalk" in m.edition["qaSources"]:
        required.append("qa-crosswalk")
    current_atts = []
    for atype in required:
        live = [a for a in attestations
                if a["record"]["type"] == atype and
                a["record"].get("edition") in (edition_id, None) and
                not release_mod.attestation_current(a, side_digests)]
        if not live:
            problems.append("no current %s attestation" % atype)
        else:
            current_atts.append(live[-1]["digest"])
    # AC-17: legend approval must match the shipped wording digest
    legend_digest = canon.text_digest(
        canon.canon_prose(m.strings["counselLegend"]))
    approved = [a for a in attestations
                if a["record"]["type"] == "legend-approval" and
                a["record"]["sides"].get("legendWording") == legend_digest]
    if not approved:
        problems.append("no current legend-approval attestation for the "
                        "shipped wording")
    errors = validate.validate_edition(m, for_release=True)
    problems += ["release predicate: [%s] %s" % (c, msg) for c, msg in errors]
    if problems:
        for p in problems:
            sys.stderr.write("  [release] %s\n" % p)
        raise SystemExit("release refused (%d problem(s))" % len(problems))
    out = gateway.OutputGateway(DIST, "release", planes)
    sealed_name = m.edition["artifactName"]
    out.write("sealed", sealed_name, candidate_bytes)
    out.write("artifact-checksum", sealed_name + ".sha256",
              release_mod.checksum_text(sealed_name, candidate_bytes))
    record = {
        "edition": edition_id,
        "sealed": sealed_name,
        "sealedDigest": candidate_digest,
        "lockDigest": lock["lockDigest"],
        "qaRecord": qa["digest"],
        "attestations": sorted(current_atts),
        "declaredReleaseTimestamp": m.edition["declaredReleaseTimestamp"],
        "operator": operator_id(),
    }
    digest, rname = vgw.append("release-record", record)
    print("release %s -> dist/%s sealed\n  release-record %s"
          % (edition_id, sealed_name, digest))


def current_side_digests(m):
    reg = m.registry.corpora
    sides = {
        "relationSet": m.gw.read_log[m.edition["relationSet"]],
        "gateInventory": m.gw.read_log[m.edition["gateInventory"]],
        "claimSet": reg[m.edition["claimCorpus"]]["files"][
            reg[m.edition["claimCorpus"]]["primary"]],
        "legendWording": canon.text_digest(
            canon.canon_prose(m.strings["counselLegend"])),
        "manifestWording": canon.text_digest(
            canon.canon_prose(m.strings["bundleManifestText"])),
        "supportMatrix": canon.bytes_digest(m.support_matrix_bytes),
    }
    for role_key, qa_id in m.edition["qaSources"].items():
        entry = reg[qa_id]
        key = "priorityMap" if role_key == "priorityMap" else "crosswalk"
        sides[key] = entry["files"][entry["primary"]]
    return sides


def cmd_bundle(argv):
    planes = load_planes()
    boot = gateway.ContentGateway(ROOT)
    cfg = json.loads(boot.read_text("navigator/bundles/na-af-2026.json"))
    vgw = gateway.VerificationGateway(RECORDS, "bundle", planes)
    release_records = vgw.read_all("release-record")
    members = []
    member_releases = []
    for ed in cfg["editions"]:
        recs = [r for r in release_records if r["record"]["edition"] == ed]
        if not recs:
            raise SystemExit("bundle needs both editions sealed; %s has no "
                             "release-record" % ed)
        sealed_name = recs[-1]["record"]["sealed"]
        data = gateway.ArtifactGateway(
            DIST, "bundle", planes).read("sealed", sealed_name)
        digest = canon.bytes_digest(data)
        matching = [r for r in recs
                    if r["record"]["sealedDigest"] == digest]
        if not matching:
            raise SystemExit("sealed %s matches no release-record"
                             % sealed_name)
        rec = matching[-1]
        members.append((sealed_name, data))
        members.append((sealed_name + ".sha256",
                        release_mod.checksum_text(sealed_name, data).encode()))
        member_releases.append(rec["digest"])
    strings = json.loads(boot.read_text("navigator/strings.json"))
    manifest_text = strings["bundleManifestText"] + "\n"
    # the counsel-facing manifest carries no verification-plane references
    attestations = vgw.read_all("attestation") if "attestation" in \
        planes["commands"]["bundle"]["reads"] else []
    del attestations
    out = gateway.OutputGateway(DIST, "bundle", planes)
    out.write("bundle-manifest", "MANIFEST.txt", manifest_text)
    members.append(("MANIFEST.txt", manifest_text.encode("utf-8")))
    zip_bytes = bundlezip.build_zip(members, cfg["declaredTimestamp"])
    out.write("bundle", cfg["name"], zip_bytes)
    out.write("bundle-checksum", cfg["name"] + ".sha256",
              release_mod.checksum_text(cfg["name"], zip_bytes))
    record = {
        "bundle": cfg["name"],
        "bundleDigest": canon.bytes_digest(zip_bytes),
        "members": [{"name": n, "digest": canon.bytes_digest(d)}
                    for n, d in members],
        "releaseRecords": sorted(member_releases),
        "manifestWording": canon.text_digest(
            canon.canon_prose(strings["bundleManifestText"])),
        "operator": operator_id(),
    }
    digest, rname = vgw.append("bundle-record", record)
    print("bundle -> dist/%s\n  bundle-record %s" % (cfg["name"], digest))


def cmd_status(argv):
    """Resolve and report the current digest chain (read-only): which
    records authorize the current derivation. Records are selected by
    digest equality, never recency (TDD §10)."""
    planes = load_planes()
    boot = gateway.ContentGateway(ROOT)
    cfg = json.loads(boot.read_text("navigator/bundles/na-af-2026.json"))
    vgw = gateway.VerificationGateway(RECORDS, "status", planes)
    ags = gateway.ArtifactGateway(DIST, "status", planes)
    sealed_digests = {}
    for ed in cfg["editions"]:
        print("edition %s" % ed)
        try:
            m, html, lock = derive(ed, "candidate")
        except SystemExit as e:
            print("  derivation: INVALID (%s)" % e)
            continue
        cdig = canon.bytes_digest(html)
        print("  derivation: valid; candidate %s… lock %s…"
              % (cdig[:20], lock["lockDigest"][:20]))
        name = "candidate_" + m.edition["artifactName"]
        if os.path.exists(os.path.join(DIST, name)):
            current = ags.read("candidate", name) == html
            print("  dist candidate: %s" % ("current" if current else "STALE"))
        else:
            print("  dist candidate: missing")
        qa = [r for r in vgw.read_all("qa-record")
              if r["record"]["edition"] == ed and
              r["record"]["candidateDigest"] == cdig and
              r["record"]["lockDigest"] == lock["lockDigest"]]
        print("  qa-record: %s" % (qa[-1]["digest"][:20] + "…" if qa
                                   else "none for this derivation"))
        rel = [r for r in vgw.read_all("release-record")
               if r["record"]["edition"] == ed and
               r["record"]["sealedDigest"] == cdig]
        if rel:
            sealed_name = rel[-1]["record"]["sealed"]
            ok = os.path.exists(os.path.join(DIST, sealed_name)) and \
                canon.bytes_digest(ags.read("sealed", sealed_name)) == cdig
            print("  release-record: %s… sealed file %s"
                  % (rel[-1]["digest"][:20], "current" if ok else "STALE"))
            if ok:
                sealed_digests[ed] = rel[-1]["digest"]
        else:
            print("  release-record: none for this derivation")
        current_sides = current_side_digests(m)
        atts = [a for a in vgw.read_all("attestation")
                if a["record"].get("edition") in (ed, None)]
        live = [a for a in atts if not release_mod.attestation_current(
            a, current_sides)]
        print("  attestations current: %d of %d applicable"
              % (len(live), len(atts)))
    bpath = os.path.join(DIST, cfg["name"])
    if os.path.exists(bpath):
        bdig = canon.bytes_digest(ags.read("bundle", cfg["name"]))
        brec = [r for r in vgw.read_all("bundle-record")
                if r["record"]["bundleDigest"] == bdig]
        chained = brec and set(brec[-1]["record"]["releaseRecords"]) == \
            set(sealed_digests.values()) and len(sealed_digests) == \
            len(cfg["editions"])
        print("bundle: %s… record %s; chains to current releases: %s"
              % (bdig[:20], "found" if brec else "MISSING",
                 "yes" if chained else "NO"))
    else:
        print("bundle: not built")


def main(argv):
    ci_guard(argv)
    argv = [a for a in argv if a != "--private-runner"]
    if not argv:
        raise SystemExit(
            "usage: build.py preview|candidate|migrate|record-qa|release "
            "<edition> | attest <type> [edition] | bundle | status")
    cmd, rest = argv[0], argv[1:]
    if cmd == "preview":
        cmd_preview(rest[0], rest[1:])
    elif cmd == "candidate":
        cmd_candidate(rest[0], rest[1:])
    elif cmd == "migrate":
        cmd_migrate(rest[0], rest[1:])
    elif cmd == "attest":
        cmd_attest(rest)
    elif cmd == "record-qa":
        cmd_record_qa(rest[0], rest[1:])
    elif cmd == "release":
        cmd_release(rest[0], rest[1:])
    elif cmd == "bundle":
        cmd_bundle(rest)
    elif cmd == "status":
        cmd_status(rest)
    elif cmd == "propose-reuse":
        raise SystemExit("propose-reuse is deferred (TDD §10.7)")
    else:
        raise SystemExit("unknown command %r" % cmd)


if __name__ == "__main__":
    main(sys.argv[1:])
