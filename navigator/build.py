#!/usr/bin/env python3
"""AA11393US claims navigator — build pipeline (TDD §10, §11, §13).

Content plane: ``preview`` / ``candidate`` / ``migrate``; verification
plane: ``attest`` / ``record-qa`` / ``release`` / ``bundle``. The
``bundle-plan`` command is a read-only promotion planner. All file
traffic goes through the gateways; the command x kind privilege matrix
(schema/planes.json) is enforced there. Build commands are content-plane
read-only. ``propose-reuse`` is deferred (TDD §10.7).

Confidentiality guardrail (TDD §10.16): the build aborts in CI
environments; ``--private-runner`` is the logged override.
"""

import copy
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import authority, canon, gateway, model, qaevidence, render  # noqa: E402
from lib import recordprovenance  # noqa: E402
from lib import schema_validate, validate  # noqa: E402
from lib import migrate as migrate_mod, projections, release as release_mod  # noqa: E402
from lib import bundleplan, bundlezip  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "navigator", "dist")
RECORDS = os.path.join(ROOT, "navigator", "records")
BUNDLE_CONFIG = "navigator/bundles/na-af-2026.json"
BUNDLE_MANIFEST_RESOURCE = "navigator/bundle-manifest.json"
CI_MARKERS = ("CI", "GITHUB_ACTIONS", "GITLAB_CI", "JENKINS_URL",
              "BUILDKITE", "CIRCLECI", "TRAVIS", "TEAMCITY_VERSION")
DELIVERY_EDITION_COUNT = 2


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
    return canon.parse_json(
        gateway.ContentGateway(ROOT).read_text("navigator/schema/planes.json"))


def bundle_manifest_input(content):
    """Return the closed bundle-only manifest text, bytes, and wording hash."""
    value = canon.parse_json(content.read_text(BUNDLE_MANIFEST_RESOURCE))
    if not isinstance(value, dict) or \
            set(value) != {"manifestVersion", "bundleManifestText"} or \
            value.get("manifestVersion") != "1" or \
            not isinstance(value.get("bundleManifestText"), str) or \
            not value["bundleManifestText"]:
        raise SystemExit("bundle manifest resource is malformed")
    manifest_text = value["bundleManifestText"]
    return (
        value,
        (manifest_text + "\n").encode("utf-8"),
        canon.text_digest(canon.canon_prose(manifest_text)),
    )


def edition_path(edition_id):
    if not isinstance(edition_id, str) or not edition_id or \
            not edition_id.isascii() or not edition_id.isidentifier() or \
            edition_id.startswith("_") or edition_id != edition_id.lower():
        raise SystemExit(
            "edition id must be a lowercase ASCII identifier, got %r" %
            edition_id)
    return "navigator/editions/%s.json" % edition_id


def build_model(edition_id, planes=None, allow_legacy_canon=False):
    boot = gateway.ContentGateway(ROOT)
    allow = canon.parse_json(
        boot.read_text(edition_path(edition_id)))["declaredTransitiveInputs"]
    gw = gateway.ContentGateway(ROOT, allowlist=allow)
    m = model.EditionModel(
        gw, edition_path(edition_id),
        allow_legacy_canon=allow_legacy_canon)
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
    gw, m = build_model(edition_id, allow_legacy_canon=True)
    before_relation = copy.deepcopy(m.relation)
    before_inventory = copy.deepcopy(m.gates)
    log = []
    migrate_mod.migrate_inventory(m, log)
    migrate_mod.migrate_relation(m, log)
    diff_problems = migrate_mod.migration_diff_problems(
        before_relation, m.relation, before_inventory, m.gates,
        fragment_hashes={fid: unit.digest for fid, unit in m.units.items()})
    schema_problems = []
    relation_for_schema = m.relation
    before_canon = before_relation.get("binding", {}).get("canonVersion") \
        if isinstance(before_relation, dict) else None
    after_canon = m.relation.get("binding", {}).get("canonVersion") \
        if isinstance(m.relation, dict) else None
    if before_canon == after_canon and isinstance(after_canon, str) and \
            after_canon and after_canon != canon.CANON_VERSION:
        # The migration-only loader admits exactly this legacy sentinel so
        # owners can be made stale without comparing incompatible digests.
        # Validate every other field by substituting the current sentinel in
        # a throw-away copy; the authored binding stays untouched for the
        # authorized-operator resolving commit.
        relation_for_schema = copy.deepcopy(m.relation)
        relation_for_schema["binding"]["canonVersion"] = canon.CANON_VERSION
    for name, instance in (("relation", relation_for_schema),
                           ("gates", m.gates)):
        schema_problems.extend(
            "%s: %s" % (name, problem)
            for problem in schema_validate.validate(instance, m.schemas[name]))
    if diff_problems or schema_problems:
        for problem in diff_problems:
            sys.stderr.write("  [migration-diff] %s\n" % problem)
        for problem in schema_problems:
            sys.stderr.write("  [migration-schema] %s\n" % problem)
        raise SystemExit(
            "migrate %s: output violates the closed migration action "
            "classes; no source files written" % edition_id)
    for action, key, detail in log:
        print("  %-10s %-28s %s" % (action, key, detail))
    dirty = (before_relation != m.relation or before_inventory != m.gates)
    if not dirty:
        print("migrate %s: nothing to do" % edition_id)
        return
    if not log:
        # Diagnostics are not a persistence signal.  This guard makes that
        # separation explicit if a future migration mutates bookkeeping only.
        print("  %-10s %-28s %s" %
              ("bookkeep", edition_id, "migration metadata updated"))
    # class b/c writes to the edition's relation set + inventory locators
    planes = load_planes()
    for kind, path, obj in (
            ("source:relation-set", m.edition["relationSet"], m.relation),
            ("source:gate-inventory-locators",
             m.edition["gateInventory"], m.gates)):
        gateway.write_source(
            "migrate", planes, ROOT, kind, path,
            json.dumps(obj, indent=1, ensure_ascii=False) + "\n")
    print("migrate %s: %d action(s) applied" %
          (edition_id, max(1, len(log))))


ATTEST_TYPES = ("inventory-completeness", "qa-priority-map", "qa-crosswalk",
                "legend-approval", "manifest-approval",
                "support-matrix-approval")

EDITION_ATTEST_TYPES = frozenset((
    "inventory-completeness", "qa-priority-map", "qa-crosswalk",
))

ATTESTATION_SIDES = {
    "inventory-completeness": frozenset(("claimSet", "gateInventory")),
    "qa-priority-map": frozenset(("relationSet", "priorityMap")),
    "qa-crosswalk": frozenset(("relationSet", "crosswalk")),
    "legend-approval": frozenset(("legendWording",)),
    "manifest-approval": frozenset(("manifestWording",)),
    "support-matrix-approval": frozenset(("supportMatrix",)),
}

ATTESTATION_RECORD_FIELDS = frozenset((
    "type", "edition", "sides", "note", "approvalStatus", "operator",
    "operatorKind", "producerCommand",
))
QA_RECORD_FIELDS = frozenset((
    "edition", "candidateDigest", "lockDigest", "contentLock",
    "qaInputLock", "reproductionDiagnostics", "attestations",
    "supportMatrix", "legendApproval", "manualEvidenceVersion",
    "manualChecks", "approvalStatus", "operator", "operatorKind",
))

EXPECTED_ACCEPTANCE_IDS = tuple("AC-%02d" % number
                                for number in range(1, 21))
REQUIRED_MANUAL_QA_FIELDS = {
    "AC-11": ("ac11",),
    "AC-12": ("ac12",),
    "AC-13": ("ac13",),
    "AC-15": ("ac15",),
}


def operator_id():
    """Return the explicitly declared authoritative ``(operator, kind)``.

    Verification records are approvals, so silently attributing them to a
    default identity or kind creates false evidence.  Both fields are required
    even when the caller happens to be a human-operated tool or a model run.
    """
    operator = os.environ.get("NAV_OPERATOR")
    if not authority.is_identified_operator_identity(operator):
        raise SystemExit(
            "NAV_OPERATOR must identify the operator performing this approval")
    kind = os.environ.get("NAV_OPERATOR_KIND")
    if not authority.is_authoritative_operator_kind(kind):
        raise SystemExit(
            "NAV_OPERATOR_KIND must be explicitly set to 'human' or 'model'; "
            "tool, missing, and unknown kinds are not release-authoritative")
    return operator, kind


def approval_evidence_problems(record, require_note=True):
    """Return defects in a structured approval carried by *record*.

    This predicate is intentionally incompatible with legacy records that
    merely contain an operator-shaped string: accepting those records would
    turn unknown or tool-authored work into an authorized approval.
    """
    problems = []
    if not isinstance(record, dict):
        return ["approval record is not an object"]
    if record.get("approvalStatus") != "passed":
        problems.append("approvalStatus is not 'passed'")
    if "status" in record and record.get("status") != "passed":
        problems.append("approval status is not 'passed'")
    operator = record.get("operator")
    operator_kind = record.get("operatorKind")
    if not authority.is_identified_operator_identity(operator):
        problems.append("approval has no identified operator")
    if not authority.is_authoritative_operator_kind(operator_kind):
        problems.append("approval operatorKind is not release-authoritative")
    note = record.get("note")
    if require_note and not authority.is_identified_operator_identity(note):
        problems.append("approval note is missing or empty")
    elif note is not None:
        if not authority.is_identified_operator_identity(note):
            problems.append("approval note is empty")
        elif not authority.is_final_evidence_text(note):
            problems.append(
                "approval note contains pending or failure language")
    return problems


def _support_matrix_approver_problems(approver):
    problems = []
    if not authority.is_identified_operator_identity(approver):
        problems.append("support matrix has no named approver")
    return problems


def _support_matrix_operator_binding_problems(operator, approver):
    """Require the approval operator to be the matrix's named approver."""
    if not authority.operator_identity_matches(operator, approver):
        return [
            "support-matrix-approval operator does not match support matrix "
            "approver"
        ]
    return []


def _qa_corpora(m):
    """Return the edition-scoped QA registry.

    The fallback keeps narrow unit-test doubles compatible; production
    ``EditionModel`` instances always provide the isolated lazy registry.
    """
    loader = getattr(m, "qa_registry", None)
    return loader().corpora if callable(loader) else m.registry.corpora


def _qa_registry_read(m):
    """Return the raw selected QA-registry read bound by ``qaInputLock``."""
    loader = getattr(m, "qa_registry", None)
    if callable(loader):
        qa_registry = loader()
        path = m.edition["qaRegistry"]
        if set(qa_registry.gw.read_log) != {path}:
            raise SystemExit(
                "QA registry gateway read set is not exactly %r" % path)
        return {"path": path, "digest": qa_registry.gw.read_log[path]}
    # Narrow test doubles predating the model boundary get a deterministic
    # synthetic registry read. Production models always take the branch above.
    return {
        "path": "test/qa-registry.json",
        "digest": canon.bytes_digest(canon.canonical_json(_qa_corpora(m))),
    }


def _verified_qa_source_files(m):
    """Read every declared internal QA file and verify its registry pin.

    QA sources deliberately sit outside the artifact's declared transitive
    inputs.  Verification-plane commands may consult them, but only through
    this pin-checking boundary; copying the registry value is not evidence
    that the declared bytes were actually read.
    """
    reads = []
    qa_gateway = gateway.ContentGateway(m.gw.root)
    qa_corpora = _qa_corpora(m)
    for role, corpus_id in sorted(m.edition.get("qaSources", {}).items()):
        if corpus_id is None:
            continue
        entry = qa_corpora.get(corpus_id)
        if not isinstance(entry, dict):
            raise SystemExit("QA source %r is not registered" % corpus_id)
        if entry.get("role") != "qa-source" or \
                entry.get("visibility") != "internal":
            raise SystemExit(
                "QA source %r must be an internal qa-source corpus"
                % corpus_id)
        primary = entry.get("primary")
        pins = entry.get("files")
        if not isinstance(pins, dict) or not pins or primary not in pins:
            raise SystemExit(
                "QA source %r has no pinned primary file" % corpus_id)
        for path in sorted(pins):
            data = qa_gateway.read_bytes(path)
            actual = canon.bytes_digest(data)
            if actual != pins[path]:
                raise SystemExit(
                    "QA source %r file %r drifted: pinned %s, actual %s"
                    % (corpus_id, path, pins[path], actual))
            reads.append({
                "role": role,
                "corpusId": corpus_id,
                "path": path,
                "digest": actual,
            })
    return reads


def qa_input_lock(m, candidate_digest, content_lock_digest):
    """Candidate-bound deterministic lock over verified internal QA bytes."""
    payload = {
        "lockType": "internal-qa-inputs",
        "canonVersion": canon.CANON_VERSION,
        "candidateDigest": candidate_digest,
        "contentLockDigest": content_lock_digest,
        "registryRead": _qa_registry_read(m),
        "reads": _verified_qa_source_files(m),
    }
    result = dict(payload)
    result["lockDigest"] = canon.composite_digest(
        "aa11393:lock:c1", payload)
    return result


def _verified_qa_primary_digest(m, role):
    qa_corpora = _qa_corpora(m)
    matches = [entry for entry in _verified_qa_source_files(m)
               if entry["role"] == role and
               entry["path"] == qa_corpora[
                   entry["corpusId"]]["primary"]]
    if len(matches) != 1:
        raise SystemExit(
            "edition must declare exactly one pinned QA primary for role %r"
            % role)
    return matches[0]["digest"]


def _attestation_scope_matches(record, atype, edition_id):
    expected = edition_id if atype in EDITION_ATTEST_TYPES else None
    return record.get("edition") == expected


def attestation_evidence_problems(attestation, side_digests, edition_id=None):
    """Validate approval, exact sides, scope, and currency of an attestation."""
    raw_record = attestation.get("record") if isinstance(attestation, dict) \
        else None
    problems = approval_evidence_problems(raw_record)
    if not isinstance(raw_record, dict) or \
            set(raw_record) != ATTESTATION_RECORD_FIELDS:
        problems.append("attestation record has the wrong fields")
    problems.extend(recordprovenance.attestation_producer_problems(
        raw_record))
    record = raw_record if isinstance(raw_record, dict) else {}
    atype = record.get("type")
    expected_sides = ATTESTATION_SIDES.get(atype)
    sides = record.get("sides")
    if expected_sides is None:
        problems.append("unknown attestation type %r" % atype)
    elif not isinstance(sides, dict) or set(sides) != expected_sides:
        problems.append(
            "%s attestation sides must be exactly %s"
            % (atype, sorted(expected_sides)))
    else:
        for side in sorted(expected_sides):
            if side not in side_digests:
                problems.append("current digest for attestation side %r is "
                                "unavailable" % side)
            elif sides[side] != side_digests[side]:
                problems.append("attestation side %r is not current" % side)
    if edition_id is not None and atype in ATTESTATION_SIDES and \
            not _attestation_scope_matches(record, atype, edition_id):
        problems.append("attestation has the wrong edition scope")
    return problems


def _required_attestation_types(m):
    required = ["inventory-completeness", "qa-priority-map",
                "legend-approval", "support-matrix-approval"]
    if m.edition.get("qaSources", {}).get("crosswalk") is not None:
        required.append("qa-crosswalk")
    return required


def _confirmed_current_attestations(attestations, side_digests, edition_id,
                                    required_types,
                                    support_matrix_approver):
    """Choose one current attestation per type, preferring human approval."""
    chosen = {}
    problems = []
    for atype in required_types:
        applicable = [a for a in attestations
                      if isinstance(a, dict) and
                      isinstance(a.get("record"), dict) and
                      a["record"].get("type") == atype and
                      _attestation_scope_matches(
                          a["record"], atype, edition_id)]

        def evidence_problems(attestation):
            current = attestation_evidence_problems(
                attestation, side_digests, edition_id)
            if atype == "support-matrix-approval":
                current.extend(_support_matrix_operator_binding_problems(
                    attestation["record"].get("operator"),
                    support_matrix_approver))
            return current

        live = [a for a in applicable if not evidence_problems(a)]
        if not live:
            detail = []
            for att in applicable:
                detail.extend(evidence_problems(att))
            suffix = ": %s" % "; ".join(sorted(set(detail))) if detail else ""
            problems.append("no confirmed current %s attestation%s"
                            % (atype, suffix))
        else:
            chosen[atype] = min(live, key=_approval_selection_key)
    return chosen, problems


def _approval_selection_key(envelope):
    """Human first, then model, then digest for one valid current subject."""
    record = envelope.get("record", {}) \
        if isinstance(envelope, dict) else {}
    kind = record.get("operatorKind") if isinstance(record, dict) else None
    rank = 0 if kind == "human" else 1
    digest = envelope.get("digest", "") \
        if isinstance(envelope, dict) else ""
    return rank, digest


def cmd_attest(argv):
    if not argv:
        raise SystemExit("usage: build.py attest <type> [edition] "
                         "--approved --note=<evidence>")
    atype = argv[0]
    if atype not in ATTEST_TYPES:
        raise SystemExit("unknown attestation type %r" % atype)
    positional = [a for a in argv[1:] if not a.startswith("--")]
    unknown = [a for a in argv[1:] if a.startswith("--") and
               a != "--approved" and not a.startswith("--note=")]
    notes = [a[len("--note="):] for a in argv[1:]
             if a.startswith("--note=")]
    if unknown or len(positional) > 1 or len(notes) != 1 or \
            argv[1:].count("--approved") != 1:
        raise SystemExit("attest requires one --approved flag, one "
                         "--note=<evidence>, and at most one edition")
    edition_id = positional[0] if positional else None
    if atype in EDITION_ATTEST_TYPES and edition_id is None:
        raise SystemExit("%s requires an edition" % atype)
    if atype not in EDITION_ATTEST_TYPES and edition_id is not None:
        raise SystemExit("%s is global and must not name an edition" % atype)
    note = notes[0].strip()
    if not authority.is_final_evidence_text(note):
        raise SystemExit("attestation evidence must be nonempty and final, "
                         "not pending or failed")
    operator, operator_kind = operator_id()
    planes = load_planes()
    gw = gateway.ContentGateway(ROOT)  # attest reads content w/o allowlist
    sides = {}
    if atype == "inventory-completeness":
        _, m = build_model(edition_id)
        entry = m.registry.entry(m.edition["claimCorpus"])
        sides["claimSet"] = m.gw.read_log[entry["primary"]]
        sides["gateInventory"] = m.gw.read_log[m.edition["gateInventory"]]
    elif atype == "qa-priority-map":
        _, m = build_model(edition_id)
        sides["relationSet"] = m.gw.read_log[m.edition["relationSet"]]
        sides["priorityMap"] = _verified_qa_primary_digest(m, "priorityMap")
    elif atype == "qa-crosswalk":
        _, m = build_model(edition_id)
        sides["relationSet"] = m.gw.read_log[m.edition["relationSet"]]
        sides["crosswalk"] = _verified_qa_primary_digest(m, "crosswalk")
    elif atype == "legend-approval":
        strings = canon.parse_json(gw.read_text("navigator/strings.json"))
        sides["legendWording"] = canon.text_digest(
            canon.canon_prose(strings["counselLegend"]))
    elif atype == "manifest-approval":
        unused_manifest, unused_bytes, manifest_wording = \
            bundle_manifest_input(gw)
        sides["manifestWording"] = manifest_wording
    elif atype == "support-matrix-approval":
        data = gw.read_bytes("navigator/schema/support-matrix.json")
        matrix = canon.parse_json(data)
        matrix_schema = canon.parse_json(gw.read_text(
            "navigator/schema/support-matrix.schema.json"))
        matrix_problems = schema_validate.validate(matrix, matrix_schema)
        if matrix_problems:
            raise SystemExit("support matrix schema invalid: %s"
                             % "; ".join(matrix_problems))
        approver_problems = _support_matrix_approver_problems(
            matrix["approver"])
        if approver_problems:
            raise SystemExit("; ".join(approver_problems))
        binding_problems = _support_matrix_operator_binding_problems(
            operator, matrix["approver"])
        if binding_problems:
            raise SystemExit("; ".join(binding_problems))
        sides["supportMatrix"] = canon.bytes_digest(data)
    vgw = gateway.VerificationGateway(RECORDS, "attest", planes)
    record = {"type": atype, "edition": edition_id, "sides": sides,
              "note": note, "approvalStatus": "passed",
              "operator": operator, "operatorKind": operator_kind,
              "producerCommand":
                  recordprovenance.ATTESTATION_PRODUCER_COMMAND}
    digest, name = vgw.append("attestation", record)
    print("attestation %s -> records/%s\n  %s" % (atype, name, digest))


def registry_manual_fields(acceptance):
    """Validate the acceptance registry floor and return manual QA fields.

    The registry is content-plane input, not authority to delete release
    requirements.  The executable floor therefore fixes the complete AC
    identifier set and the four criteria that require operator QA evidence.
    """
    if not isinstance(acceptance, dict) or \
            not isinstance(acceptance.get("criteria"), list):
        raise SystemExit("acceptance registry has no criteria array")
    runner = acceptance.get("runner")
    if not isinstance(runner, dict) or runner.get(
            "manualQaEvidenceVersion") != qaevidence.MANUAL_EVIDENCE_VERSION:
        raise SystemExit(
            "acceptance registry manualQaEvidenceVersion must be %r"
            % qaevidence.MANUAL_EVIDENCE_VERSION)
    criteria = acceptance["criteria"]
    if not all(isinstance(criterion, dict) for criterion in criteria):
        raise SystemExit("acceptance registry criteria must be objects")
    ids = [criterion.get("id") for criterion in criteria]
    if tuple(ids) != EXPECTED_ACCEPTANCE_IDS:
        raise SystemExit(
            "acceptance registry criteria must be exactly %s in order"
            % (list(EXPECTED_ACCEPTANCE_IDS),))
    fields = []
    for criterion in criteria:
        enforced = criterion.get("enforcedBy")
        if not isinstance(enforced, dict) or \
                not isinstance(enforced.get("qaRecordFields"), list):
            raise SystemExit("acceptance registry criterion %s has no "
                             "qaRecordFields array" % criterion["id"])
        actual = tuple(enforced["qaRecordFields"])
        expected = REQUIRED_MANUAL_QA_FIELDS.get(criterion["id"], ())
        if actual != expected:
            raise SystemExit(
                "acceptance registry criterion %s must require exactly %s"
                % (criterion["id"], list(expected)))
        for field in actual:
            if not isinstance(field, str) or not field:
                raise SystemExit("acceptance registry has an invalid manual "
                                 "QA field")
            if field in fields:
                raise SystemExit("acceptance registry repeats manual QA field "
                                 "%r" % field)
            fields.append(field)
    return tuple(sorted(fields))


RECORD_QA_USAGE = (
    "usage: build.py record-qa <edition> "
    "[--template | [--check-only] "
    "(--evidence-file=<workspace-relative.json> | --acNN=<JSON> ...) ]"
)


def parse_record_qa_options(argv):
    """Return closed record-QA mode options without inferring defaults."""
    template = False
    check_only = False
    evidence_file = None
    manual_args = []
    for arg in argv:
        if arg == "--template":
            if template:
                raise SystemExit("--template supplied more than once")
            template = True
        elif arg == "--check-only":
            if check_only:
                raise SystemExit("--check-only supplied more than once")
            check_only = True
        elif isinstance(arg, str) and arg.startswith("--evidence-file="):
            if evidence_file is not None:
                raise SystemExit("--evidence-file supplied more than once")
            evidence_file = arg.split("=", 1)[1]
            if not evidence_file:
                raise SystemExit("--evidence-file path must be non-empty")
        else:
            manual_args.append(arg)
    if template and (check_only or evidence_file is not None or manual_args):
        raise SystemExit(
            "--template is mutually exclusive with evidence and --check-only")
    if evidence_file is not None and manual_args:
        raise SystemExit(
            "--evidence-file is mutually exclusive with inline --acNN evidence")
    return {
        "template": template,
        "checkOnly": check_only,
        "evidenceFile": evidence_file,
        "manualArgs": manual_args,
    }


def manual_check_args_from_evidence_file(relpath, required_fields):
    """Read one workspace-local evidence object outside the candidate lock.

    A fresh, discarded content gateway supplies canonical relative-path and
    symlink confinement.  Its read log is intentionally never merged into the
    edition gateway, so an operator working file cannot become a candidate
    content input.
    """
    try:
        evidence_gateway = gateway.ContentGateway(
            ROOT, allowlist=[relpath])
        value = canon.parse_json(evidence_gateway.read_bytes(relpath))
    except (gateway.GatewayError, OSError) as exc:
        raise SystemExit("cannot read manual QA evidence file: %s" % exc)
    except ValueError as exc:
        raise SystemExit("manual QA evidence file is not valid JSON: %s" % exc)
    required = set(required_fields)
    if not isinstance(value, dict) or set(value) != required:
        raise SystemExit(
            "manual QA evidence file must contain exactly %s"
            % sorted(required))
    args = []
    for field in required_fields:
        try:
            encoded = canon.canonical_json(value[field]).decode("utf-8")
        except (TypeError, ValueError, canon.CanonError) as exc:
            raise SystemExit("%s evidence is not canonical JSON: %s"
                             % (field, exc))
        args.append("--%s=%s" % (field, encoded))
    return args


def parse_manual_checks(argv, required_fields, operator, operator_kind,
                        support_matrix, api_probe_apis):
    """Parse ``--acNN=<JSON>`` evidence into normalized QA-record fields.

    Each JSON value has a field-specific, closed evidence payload.  For
    example AC-11 carries ordered results for every current support target::

        --ac11='{"status":"passed","evidence":"...","targetResults":[...]}'
    """
    parsed = {}
    required = set(required_fields)
    for arg in argv:
        if not isinstance(arg, str) or not arg.startswith("--") or \
                "=" not in arg:
            raise SystemExit(
                "manual QA arguments must be --acNN=<JSON evidence>")
        field, raw = arg[2:].split("=", 1)
        if field not in required:
            raise SystemExit("unknown manual QA field %r" % field)
        if field in parsed:
            raise SystemExit("manual QA field %r supplied more than once"
                             % field)
        try:
            evidence = canon.parse_json(raw)
        except ValueError as exc:
            raise SystemExit("%s evidence is not valid JSON: %s"
                             % (field, exc))
        payload_field = {
            "ac11": "targetResults",
            "ac12": "printResult",
            "ac13": "targetResults",
            "ac15": "probeResult",
        }[field]
        if not isinstance(evidence, dict) or set(evidence) != {
                "status", "evidence", payload_field}:
            raise SystemExit(
                "%s evidence must contain exactly status, evidence, and %s"
                % (field, payload_field))
        normalized = dict(evidence)
        normalized["operator"] = operator
        normalized["operatorKind"] = operator_kind
        parsed[field] = normalized
    problems = qaevidence.manual_check_problems(
        parsed, required_fields, support_matrix=support_matrix,
        api_probe_apis=api_probe_apis, operator=operator,
        operator_kind=operator_kind,
        manual_evidence_version=qaevidence.MANUAL_EVIDENCE_VERSION)
    if problems:
        raise SystemExit("; ".join(problems))
    return parsed


def qa_authorization_problems(qa, candidate_digest, content_lock,
                              qa_lock, support_matrix, api_probe_apis,
                              legend_digest,
                              attestations, side_digests, edition_id,
                              required_types, manual_fields):
    """Return every defect that prevents a QA record authorizing release."""
    raw_record = qa.get("record") if isinstance(qa, dict) else None
    problems = approval_evidence_problems(raw_record, require_note=False)
    if not isinstance(raw_record, dict) or set(raw_record) != QA_RECORD_FIELDS:
        problems.append("QA record has the wrong fields")
    record = raw_record if isinstance(raw_record, dict) else {}
    operator = record.get("operator")
    operator_kind = record.get("operatorKind")
    problems.extend(qaevidence.manual_check_problems(
        record.get("manualChecks"), manual_fields,
        support_matrix=support_matrix, api_probe_apis=api_probe_apis,
        operator=operator, operator_kind=operator_kind,
        manual_evidence_version=record.get("manualEvidenceVersion")))

    if record.get("candidateDigest") != candidate_digest:
        problems.append("QA candidate digest is not current")
    if record.get("edition") != edition_id:
        problems.append("QA record has the wrong edition scope")
    if record.get("contentLock") != content_lock["reads"] or \
            record.get("lockDigest") != content_lock["lockDigest"]:
        problems.append("QA content-input lock is not current")
    if record.get("qaInputLock") != qa_lock:
        problems.append("QA internal-input lock is missing or not current")
    diagnostics = record.get("reproductionDiagnostics")
    diagnostic_fields = {"interpreter", "platform", "locale", "unicodedata"}
    if not isinstance(diagnostics, dict) or \
            set(diagnostics) != diagnostic_fields or \
            not all(isinstance(value, str) and value
                    for value in diagnostics.values()):
        problems.append("QA reproduction diagnostics are not fully typed")

    matrix_digest = side_digests.get("supportMatrix")
    if matrix_digest is None:
        problems.append("current support matrix digest is unavailable")
    problems.extend(_support_matrix_approver_problems(
        support_matrix.get("approver")))
    matrix_record = record.get("supportMatrix")
    if not isinstance(matrix_record, dict):
        problems.append("QA supportMatrix evidence is missing")
        matrix_record = {}
    elif set(matrix_record) != {"digest", "approver",
                                "approvalAttestation"}:
        problems.append("QA supportMatrix evidence has the wrong fields")
    if matrix_record.get("digest") != matrix_digest:
        problems.append("QA support matrix digest is not current")
    if matrix_record.get("approver") != support_matrix.get("approver"):
        problems.append("QA support matrix approver is not current")

    legend_record = record.get("legendApproval")
    if not isinstance(legend_record, dict):
        problems.append("QA legend approval evidence is missing")
        legend_record = {}
    elif set(legend_record) != {"digest", "approvalAttestation"}:
        problems.append("QA legend approval evidence has the wrong fields")
    if legend_record.get("digest") != legend_digest:
        problems.append("QA legend wording digest is not current")

    refs = record.get("attestations")
    if not isinstance(refs, list) or not all(
            isinstance(digest, str) for digest in refs):
        problems.append("QA attestation references are not a digest list")
        refs = []
    elif len(refs) != len(set(refs)):
        problems.append("QA attestation references contain duplicates")
    present = {a.get("digest"): a for a in attestations
               if isinstance(a, dict) and isinstance(a.get("digest"), str)}
    referenced_by_type = {}
    for digest in refs:
        att = present.get(digest)
        if att is None:
            problems.append("QA references missing attestation %s" % digest)
            continue
        att_problems = attestation_evidence_problems(
            att, side_digests, edition_id)
        problems.extend("attestation %s: %s" % (digest, p)
                        for p in att_problems)
        atype = att.get("record", {}).get("type")
        referenced_by_type.setdefault(atype, []).append(digest)
    if set(referenced_by_type) != set(required_types):
        problems.append("QA attestation types must be exactly %s"
                        % sorted(required_types))
    for atype in required_types:
        if len(referenced_by_type.get(atype, [])) != 1:
            problems.append("QA must reference exactly one %s attestation"
                            % atype)

    support_ref = matrix_record.get("approvalAttestation")
    if support_ref not in referenced_by_type.get(
            "support-matrix-approval", []):
        problems.append("QA support matrix does not name its confirmed "
                        "approval attestation")
    else:
        support_attestation = present.get(support_ref, {}).get("record", {})
        problems.extend(_support_matrix_operator_binding_problems(
            support_attestation.get("operator"),
            support_matrix.get("approver")))
    legend_ref = legend_record.get("approvalAttestation")
    if legend_ref not in referenced_by_type.get("legend-approval", []):
        problems.append("QA legend does not name its confirmed approval "
                        "attestation")
    return problems


def current_authorized_qa_records(m, candidate_digest, content_lock,
                                  qa_records, attestations):
    """Return deterministic current QA authorizations and rejected details.

    Release and status share this predicate so a read-only report cannot
    mistake a merely present or legacy record for authorization.
    """
    side_digests = current_side_digests(m)
    required = _required_attestation_types(m)
    manual_fields = registry_manual_fields(m.acceptance)
    expected_qa_lock = qa_input_lock(
        m, candidate_digest, content_lock["lockDigest"])
    support_matrix = canon.parse_json(m.support_matrix_bytes)
    api_probe_apis = sorted(render.api_probe_instruments(m.api_policy))
    legend_digest = canon.text_digest(
        canon.canon_prose(m.strings["counselLegend"]))
    candidates = [
        record for record in qa_records
        if isinstance(record, dict) and
        isinstance(record.get("record"), dict) and
        record["record"].get("edition") == m.edition["editionId"] and
        record["record"].get("candidateDigest") == candidate_digest and
        record["record"].get("lockDigest") == content_lock["lockDigest"]
    ]
    if not candidates:
        return [], [("<current-binding>", [
            "no qa-record matches the current edition, candidate digest, "
            "and content-input lock"
        ])]
    valid = []
    rejected = []
    for candidate_qa in candidates:
        problems = qa_authorization_problems(
            candidate_qa, candidate_digest, content_lock, expected_qa_lock,
            support_matrix, api_probe_apis, legend_digest, attestations,
            side_digests,
            m.edition["editionId"], required, manual_fields)
        if problems:
            rejected.append((candidate_qa.get("digest", "<unknown>"),
                             problems))
        else:
            valid.append(candidate_qa)
    return sorted(valid, key=_approval_selection_key), rejected


def cmd_record_qa(edition_id, argv):
    options = parse_record_qa_options(argv)
    m, html, lock = derive(edition_id, "candidate")
    manual_fields = registry_manual_fields(m.acceptance)
    api_probe_apis = sorted(render.api_probe_instruments(m.api_policy))
    if options["template"]:
        template = qaevidence.pending_manual_checks_template(
            m.support_matrix, api_probe_apis)
        print(json.dumps(template, indent=2, ensure_ascii=False,
                         sort_keys=True))
        return

    operator, operator_kind = operator_id()
    manual_args = options["manualArgs"]
    if options["evidenceFile"] is not None:
        manual_args = manual_check_args_from_evidence_file(
            options["evidenceFile"], manual_fields)
    fields = parse_manual_checks(
        manual_args, manual_fields, operator, operator_kind,
        m.support_matrix, api_probe_apis)
    planes = load_planes()
    name = "candidate_" + m.edition["artifactName"]
    if not os.path.exists(os.path.join(DIST, name)):
        raise SystemExit("no candidate found at dist/%s" % name)
    candidate_bytes = gateway.ArtifactGateway(
        DIST, "record-qa", planes).read("candidate", name)
    if candidate_bytes != html:
        raise SystemExit("dist/%s does not match the current derivation; "
                         "rebuild the candidate first" % name)
    candidate_digest = canon.bytes_digest(candidate_bytes)
    internal_lock = qa_input_lock(
        m, candidate_digest, lock["lockDigest"])
    vgw = gateway.VerificationGateway(RECORDS, "record-qa", planes)
    side_digests = current_side_digests(m)
    all_attestations = vgw.read_all("attestation")
    required = _required_attestation_types(m)
    support_matrix = canon.parse_json(m.support_matrix_bytes)
    chosen, attestation_problems = _confirmed_current_attestations(
        all_attestations, side_digests, edition_id, required,
        support_matrix.get("approver"))
    evidence_problems = list(attestation_problems)
    evidence_problems.extend(_support_matrix_approver_problems(
        support_matrix.get("approver")))
    if evidence_problems:
        for problem in evidence_problems:
            sys.stderr.write("  [record-qa] %s\n" % problem)
        raise SystemExit("record-qa refused (%d problem(s))"
                         % len(evidence_problems))
    attestation_refs = sorted(a["digest"] for a in chosen.values())
    support_attestation = chosen["support-matrix-approval"]["digest"]
    legend_attestation = chosen["legend-approval"]["digest"]
    legend_digest = side_digests["legendWording"]
    record = {
        "edition": edition_id,
        "candidateDigest": candidate_digest,
        "lockDigest": lock["lockDigest"],
        "contentLock": lock["reads"],
        "qaInputLock": internal_lock,
        "reproductionDiagnostics": release_mod.reproduction_diagnostics(),
        "attestations": attestation_refs,
        "supportMatrix": {
            "digest": canon.bytes_digest(m.support_matrix_bytes),
            "approver": support_matrix["approver"],
            "approvalAttestation": support_attestation,
        },
        "legendApproval": {
            "digest": legend_digest,
            "approvalAttestation": legend_attestation,
        },
        "manualEvidenceVersion": qaevidence.MANUAL_EVIDENCE_VERSION,
        "manualChecks": fields,
        "approvalStatus": "passed",
        "operator": operator,
        "operatorKind": operator_kind,
    }
    expected_digest = canon.composite_digest(
        "aa11393:qa-record:c1", record)
    envelope = {
        "kind": "qa-record", "digest": expected_digest, "record": record,
    }
    authorization_problems = qa_authorization_problems(
        envelope, candidate_digest, lock, internal_lock, support_matrix,
        api_probe_apis, legend_digest, all_attestations, side_digests,
        edition_id, required, manual_fields)
    if authorization_problems:
        for problem in authorization_problems:
            sys.stderr.write("  [record-qa self-check] %s\n" % problem)
        raise SystemExit("record-qa refused its constructed authorization "
                         "(%d problem(s))" % len(authorization_problems))
    if options["checkOnly"]:
        print("qa-record %s VALID (check-only)\n  %s"
              % (edition_id, expected_digest))
        return

    digest, rname = vgw.append("qa-record", record)
    if digest != expected_digest:
        raise gateway.GatewayError(
            "qa-record append digest differs from validated digest")
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
    qa_records = vgw.read_all("qa-record")
    attestations = vgw.read_all("attestation")
    valid_qa, rejected = current_authorized_qa_records(
        m, candidate_digest, lock, qa_records, attestations)
    if not valid_qa:
        for digest, qa_problems in rejected:
            for problem in qa_problems:
                sys.stderr.write("  [release] qa-record %s: %s\n"
                                 % (digest, problem))
        raise SystemExit("release refused: no matching qa-record carries "
                         "complete passed authorized operator evidence")
    qa = valid_qa[0]
    problems = []
    errors = validate.validate_edition(m, for_release=True)
    problems += ["release predicate: [%s] %s" % (c, msg) for c, msg in errors]
    if problems:
        for p in problems:
            sys.stderr.write("  [release] %s\n" % p)
        raise SystemExit("release refused (%d problem(s))" % len(problems))
    operator, operator_kind = operator_id()
    out = gateway.OutputGateway(DIST, "release", planes)
    sealed_name = m.edition["artifactName"]
    try:
        acceptance_receipt = release_mod.run_release_acceptance_transaction(
            ROOT, m, html, candidate_bytes, lock, qa, out)
    except (release_mod.AcceptanceError, gateway.GatewayError,
            bundlezip.BundleError, OSError, subprocess.SubprocessError) as exc:
        raise SystemExit("release refused: acceptance transaction failed: %s"
                         % exc)
    record = {
        "edition": edition_id,
        "sealed": sealed_name,
        "sealedDigest": candidate_digest,
        "lockDigest": lock["lockDigest"],
        "qaRecord": qa["digest"],
        "attestations": sorted(qa["record"]["attestations"]),
        "declaredReleaseTimestamp": m.edition["declaredReleaseTimestamp"],
        "approvalStatus": "passed",
        "operator": operator,
        "operatorKind": operator_kind,
        "acceptanceReceipt": acceptance_receipt,
    }
    # Re-derive and re-resolve immediately before the append-only outer
    # authorization.  This validates the receipt returned by the transaction
    # against the *current* runner bytes and catches content, QA, attestation,
    # candidate, or output drift that occurred after the initial preflight.
    try:
        fresh_m, fresh_html, fresh_lock = derive(edition_id, "release")
        fresh_candidate = gateway.ArtifactGateway(
            DIST, "release", planes).read("candidate", name)
        if fresh_html != html or fresh_lock != lock or \
                fresh_candidate != candidate_bytes:
            raise bundlezip.BundleError(
                "release inputs changed during promotion")
        checksum_bytes = release_mod.checksum_text(
            sealed_name, candidate_bytes).encode("utf-8")
        out.verify_written("sealed", sealed_name, candidate_bytes)
        out.verify_written(
            "artifact-checksum", sealed_name + ".sha256", checksum_bytes)
        bundlezip.verify_detached_checksum(
            checksum_bytes, sealed_name, candidate_digest)

        fresh_qas = vgw.read_all("qa-record")
        fresh_attestations = vgw.read_all("attestation")
        fresh_valid, unused_rejected = current_authorized_qa_records(
            fresh_m, candidate_digest, fresh_lock,
            fresh_qas, fresh_attestations)
        if not fresh_valid or fresh_valid[0]["digest"] != qa["digest"]:
            raise bundlezip.BundleError(
                "selected QA authorization changed during promotion")
        fresh_context = release_mod.acceptance_context(
            ROOT, fresh_m.edition["declaredTransitiveInputs"],
            (edition_id,))
        envelope = {
            "kind": "release-record",
            "digest": canon.composite_digest(
                "aa11393:release-record:c1", record),
            "record": record,
        }
        chain_problems = bundlezip.release_chain_problems(
            envelope, fresh_qas, fresh_attestations,
            _required_attestation_types(fresh_m),
            current_side_digests(fresh_m), approval_evidence_problems,
            fresh_context, {
                "qaInputLock": qa_input_lock(
                    fresh_m, candidate_digest, fresh_lock["lockDigest"]),
                "supportMatrixApprover":
                    fresh_m.support_matrix.get("approver"),
                "supportMatrixTargets": copy.deepcopy(
                    fresh_m.support_matrix.get("targets")),
                "supportMatrixViewport": copy.deepcopy(
                    fresh_m.support_matrix.get("viewport")),
                "apiProbeApis": sorted(render.api_probe_instruments(
                    fresh_m.api_policy)),
            })
        if chain_problems:
            raise bundlezip.BundleError("; ".join(chain_problems))
    except (bundlezip.BundleError, gateway.GatewayError, model.ModelError,
            release_mod.AcceptanceError, OSError, SystemExit) as exc:
        raise SystemExit("release refused after output readback: %s" % exc)
    digest, rname = vgw.append("release-record", record)
    print("release %s -> dist/%s sealed\n  release-record %s"
          % (edition_id, sealed_name, digest))


def current_side_digests(m, include_bundle=False):
    """Derive current approval sides for one edition.

    Bundle-only wording is loaded only for bundle chain verification; it is
    intentionally irrelevant to standalone QA and release authorization.
    """
    reg = m.registry.corpora
    qa_reg = _qa_corpora(m)
    claim_entry = reg[m.edition["claimCorpus"]]
    sides = {
        "relationSet": m.gw.read_log[m.edition["relationSet"]],
        "gateInventory": m.gw.read_log[m.edition["gateInventory"]],
        "claimSet": m.gw.read_log[claim_entry["primary"]],
        "legendWording": canon.text_digest(
            canon.canon_prose(m.strings["counselLegend"])),
        "supportMatrix": canon.bytes_digest(m.support_matrix_bytes),
    }
    if include_bundle:
        unused_manifest, unused_manifest_bytes, manifest_wording = \
            bundle_manifest_input(gateway.ContentGateway(m.gw.root))
        sides["manifestWording"] = manifest_wording
    for qa_read in _verified_qa_source_files(m):
        entry = qa_reg[qa_read["corpusId"]]
        if qa_read["path"] == entry["primary"]:
            sides[qa_read["role"]] = qa_read["digest"]
    return sides


def bundle_attestation_context(cfg):
    """Derive each edition's policy and exact current attestation sides.

    Bundle verification cannot infer an edition-specific crosswalk
    requirement from a record chain.  The content-plane edition configs
    are the authority for whether that fifth attestation is required.  The
    same live models independently bind every referenced attestation side;
    envelope-chain rehashing is not evidence that those sides are current.
    """
    policies = {}
    current_sides = {}
    for edition_id in cfg.get("editions", []):
        _, edition_model = build_model(edition_id)
        policies[edition_id] = _required_attestation_types(edition_model)
        current_sides[edition_id] = current_side_digests(
            edition_model, include_bundle=True)
    return policies, current_sides


def bundle_attestation_policy(cfg):
    """Return the edition-specific required attestation types."""
    return bundle_attestation_context(cfg)[0]


def bundle_acceptance_context(cfg):
    """Return edition-scoped release contexts and the bundle input union.

    Each release context binds shared runner inputs plus only that edition's
    declared fixtures.  The bundle transaction deliberately selects every
    configured edition and locks the union, without making one edition's
    fixture currency a precondition for the other's standalone release.
    """
    contexts = {}
    bundle_inputs = set()
    for edition_id in cfg.get("editions", []):
        _, edition_model = build_model(edition_id)
        declared = edition_model.edition["declaredTransitiveInputs"]
        contexts[edition_id] = release_mod.acceptance_context(
            ROOT, declared, (edition_id,))
        bundle_inputs.update(declared)
    return contexts, sorted(bundle_inputs)


def current_release_bindings(cfg):
    """Independently derive the current release identity for each edition.

    A self-consistent historical release chain is not proof that it matches
    today's complete content lock.  Bundle planning and promotion use these
    fresh candidate/lock bindings to exclude stale releases, including drift
    outside the narrower authorized-operator attestation side projections.
    """
    bindings = {}
    for edition_id in cfg.get("editions", []):
        m, html, lock = derive(edition_id, "candidate")
        bindings[edition_id] = {
            "sealed": m.edition["artifactName"],
            "sealedDigest": canon.bytes_digest(html),
            "lockDigest": lock["lockDigest"],
            "declaredReleaseTimestamp":
                m.edition["declaredReleaseTimestamp"],
        }
    return bindings


def bundle_qa_authorization_context(cfg, release_bindings):
    """Independently derive the current private-QA context per edition.

    A QA envelope can be internally self-consistent after its registry/source
    inputs, support policy, or probed API policy have changed.  Bundle
    planning and promotion therefore receive these current values from live
    edition resources, rather than treating values copied into the QA record
    as their own currency proof.
    """
    editions = cfg.get("editions", []) if isinstance(cfg, dict) else []
    if not isinstance(release_bindings, dict) or \
            set(release_bindings) != set(editions):
        raise model.ModelError(
            "current release bindings must cover exactly the configured "
            "editions before deriving QA authorization context")
    contexts = {}
    binding_fields = {
        "sealed", "sealedDigest", "lockDigest", "declaredReleaseTimestamp",
    }
    for edition_id in editions:
        binding = release_bindings[edition_id]
        if not isinstance(binding, dict) or set(binding) != binding_fields:
            raise model.ModelError(
                "current release binding for %s has the wrong fields"
                % edition_id)
        edition_model, html, content_lock = derive(edition_id, "candidate")
        actual_binding = {
            "sealed": edition_model.edition["artifactName"],
            "sealedDigest": canon.bytes_digest(html),
            "lockDigest": content_lock["lockDigest"],
            "declaredReleaseTimestamp":
                edition_model.edition["declaredReleaseTimestamp"],
        }
        if actual_binding != binding:
            raise model.ModelError(
                "current release inputs changed while deriving QA "
                "authorization context for %s" % edition_id)
        contexts[edition_id] = {
            "qaInputLock": qa_input_lock(
                edition_model, actual_binding["sealedDigest"],
                actual_binding["lockDigest"]),
            "supportMatrixApprover":
                edition_model.support_matrix.get("approver"),
            "supportMatrixTargets": copy.deepcopy(
                edition_model.support_matrix.get("targets")),
            "supportMatrixViewport": copy.deepcopy(
                edition_model.support_matrix.get("viewport")),
            "apiProbeApis": sorted(render.api_probe_instruments(
                edition_model.api_policy)),
        }
    return contexts


def _propose_current_bundle_config(
        cfg, release_records, qa_records, attestations, artifact_reader,
        manifest_bytes, manifest_wording, attestation_policy,
        current_attestation_sides, acceptance_contexts,
        release_bindings, qa_authorization_contexts):
    return bundleplan.propose_bundle_config(
        cfg, release_records, qa_records, attestations, artifact_reader,
        manifest_bytes, manifest_wording, approval_evidence_problems,
        attestation_policy, current_attestation_sides, release_bindings,
        acceptance_contexts, qa_authorization_contexts,
        expected_edition_count=DELIVERY_EDITION_COUNT)


def release_artifact_status(artifact_gateway, sealed_name, sealed_digest):
    """Return independent currency flags for sealed bytes and checksum."""
    sealed_ok = False
    checksum_ok = False
    try:
        sealed_bytes = artifact_gateway.read("sealed", sealed_name)
        sealed_ok = canon.bytes_digest(sealed_bytes) == sealed_digest
        checksum_bytes = artifact_gateway.read(
            "artifact-checksum", sealed_name + ".sha256")
        bundlezip.verify_detached_checksum(
            checksum_bytes, sealed_name, sealed_digest)
        checksum_ok = sealed_ok
    except (bundlezip.BundleError, gateway.GatewayError, OSError):
        pass
    return sealed_ok, checksum_ok


def cmd_bundle_plan(argv):
    """Print a verified proposed bundle config; never write source/evidence."""
    planes = load_planes()
    boot = gateway.ContentGateway(ROOT)
    cfg = canon.parse_json(boot.read_text(BUNDLE_CONFIG))
    records = gateway.VerificationGateway(RECORDS, "bundle-plan", planes)
    artifacts = gateway.ArtifactGateway(DIST, "bundle-plan", planes)
    unused_manifest, manifest_bytes, manifest_wording = \
        bundle_manifest_input(boot)
    try:
        bundlezip.validate_bundle_config(
            cfg, expected_edition_count=DELIVERY_EDITION_COUNT)
        attestation_policy, current_attestation_sides = \
            bundle_attestation_context(cfg)
        acceptance_contexts, unused_runner_inputs = \
            bundle_acceptance_context(cfg)
        bindings = current_release_bindings(cfg)
        qa_authorization_contexts = bundle_qa_authorization_context(
            cfg, bindings)
        proposed = _propose_current_bundle_config(
            cfg, records.read_all("release-record"),
            records.read_all("qa-record"), records.read_all("attestation"),
            artifacts.read, manifest_bytes, manifest_wording,
            attestation_policy, current_attestation_sides,
            acceptance_contexts, bindings, qa_authorization_contexts)
    except (bundlezip.BundleError, gateway.GatewayError, model.ModelError,
            release_mod.AcceptanceError, OSError, SystemExit) as exc:
        raise SystemExit("bundle-plan refused: %s" % exc)
    # Stdout is the sole output of this read-only command.  Emit the same
    # canonical JSON encoding used by digest-bearing structures so repeated
    # plans have one byte representation independent of mapping insertion
    # order or interpreter formatting choices.
    encoded = canon.canonical_json(proposed) + b"\n"
    stdout_buffer = getattr(sys.stdout, "buffer", None)
    if stdout_buffer is None:  # e.g. an in-process StringIO test harness
        sys.stdout.write(encoded.decode("utf-8"))
    else:
        stdout_buffer.write(encoded)


def cmd_bundle(argv):
    planes = load_planes()
    boot = gateway.ContentGateway(ROOT)
    config_path = BUNDLE_CONFIG
    cfg = canon.parse_json(boot.read_text(config_path))
    vgw = gateway.VerificationGateway(RECORDS, "bundle", planes)
    manifest, manifest_bytes, manifest_wording = bundle_manifest_input(boot)
    artifacts = gateway.ArtifactGateway(DIST, "bundle", planes)
    release_records = vgw.read_all("release-record")
    qa_records = vgw.read_all("qa-record")
    attestations = vgw.read_all("attestation")
    try:
        bundlezip.validate_bundle_config(
            cfg, expected_edition_count=DELIVERY_EDITION_COUNT)
        attestation_policy, current_attestation_sides = \
            bundle_attestation_context(cfg)
        acceptance_contexts, bundle_runner_inputs = \
            bundle_acceptance_context(cfg)
        bundle_receipt_context = release_mod.combine_acceptance_contexts(
            acceptance_contexts, cfg["editions"])
        bindings = current_release_bindings(cfg)
        qa_authorization_contexts = bundle_qa_authorization_context(
            cfg, bindings)
        proposed = _propose_current_bundle_config(
            cfg, release_records, qa_records, attestations, artifacts.read,
            manifest_bytes, manifest_wording, attestation_policy,
            current_attestation_sides, acceptance_contexts, bindings,
            qa_authorization_contexts)
        if proposed != cfg:
            raise bundlezip.BundleError(
                "bundle config is stale; run bundle-plan, review, and apply "
                "the proposed config before promotion")
        plan = bundlezip.resolve_bundle_members(
            cfg, release_records, qa_records, attestations,
            artifacts.read, manifest_bytes, manifest_wording,
            approval_evidence_problems, attestation_policy,
            current_attestation_sides,
            expected_edition_count=DELIVERY_EDITION_COUNT,
            acceptance_context_by_edition=acceptance_contexts,
            qa_authorization_context_by_edition=
                qa_authorization_contexts)
        plan["acceptanceChain"] = {
            "releaseRecords": release_records,
            "qaRecords": qa_records,
            "attestations": attestations,
            "requiredAttestationsByEdition": {
                edition: sorted(attestation_policy[edition])
                for edition in cfg["editions"]
            },
            "currentSidesByEdition": current_attestation_sides,
            "acceptanceContextByEdition": acceptance_contexts,
            "qaAuthorizationContextByEdition":
                qa_authorization_contexts,
            "currentReleaseBindingsByEdition": bindings,
        }
    except (bundlezip.BundleError, gateway.GatewayError, model.ModelError,
            release_mod.AcceptanceError, OSError, SystemExit) as exc:
        raise SystemExit("bundle refused: %s" % exc)

    # Resolve every input and the operator approval before writing any output.
    # The manifest is both an enumerated ZIP member and a typed artifact.
    operator, operator_kind = operator_id()
    members = plan["members"]
    try:
        zip_bytes = bundlezip.build_zip(members, cfg["declaredTimestamp"])
        checksum_bytes = release_mod.checksum_text(
            cfg["name"], zip_bytes).encode("utf-8")
        bundlezip.verify_detached_checksum(
            checksum_bytes, cfg["name"], canon.bytes_digest(zip_bytes))
    except bundlezip.BundleError as exc:
        raise SystemExit("bundle refused: %s" % exc)
    out = gateway.OutputGateway(DIST, "bundle", planes)
    try:
        acceptance_receipt = release_mod.run_bundle_acceptance_transaction(
            ROOT, bundle_runner_inputs, cfg, boot.read_log[config_path], plan,
            zip_bytes, checksum_bytes, manifest_bytes, out)
    except (release_mod.AcceptanceError, bundlezip.BundleError,
            gateway.GatewayError, OSError) as exc:
        raise SystemExit("bundle refused: acceptance transaction failed: %s"
                         % exc)
    # Re-derive the complete bundle plan after output readback.  A concurrent
    # content/artifact change may leave unauthorizing output bytes, but can
    # never acquire the append-only bundle record that authorizes delivery.
    try:
        fresh_cfg = canon.parse_json(boot.read_text(config_path))
        fresh_manifest, fresh_manifest_bytes, fresh_manifest_wording = \
            bundle_manifest_input(boot)
        if fresh_cfg != cfg or fresh_manifest != manifest:
            raise bundlezip.BundleError(
                "bundle content inputs changed during promotion")
        fresh_release_records = vgw.read_all("release-record")
        fresh_qa_records = vgw.read_all("qa-record")
        fresh_attestations = vgw.read_all("attestation")
        fresh_policy, fresh_sides = bundle_attestation_context(fresh_cfg)
        fresh_contexts, fresh_runner_inputs = \
            bundle_acceptance_context(fresh_cfg)
        fresh_bundle_receipt_context = \
            release_mod.combine_acceptance_contexts(
                fresh_contexts, fresh_cfg["editions"])
        fresh_bindings = current_release_bindings(fresh_cfg)
        fresh_qa_authorization_contexts = bundle_qa_authorization_context(
            fresh_cfg, fresh_bindings)
        fresh_proposed = _propose_current_bundle_config(
            fresh_cfg, fresh_release_records, fresh_qa_records,
            fresh_attestations, artifacts.read, fresh_manifest_bytes,
            fresh_manifest_wording, fresh_policy, fresh_sides, fresh_contexts,
            fresh_bindings, fresh_qa_authorization_contexts)
        if fresh_proposed != cfg or fresh_contexts != acceptance_contexts or \
                fresh_bundle_receipt_context != bundle_receipt_context or \
                fresh_qa_authorization_contexts != \
                qa_authorization_contexts:
            raise bundlezip.BundleError(
                "bundle inputs changed during promotion")
        # The fresh plan can take appreciable time.  Re-read all three
        # outputs again at the last authorization boundary so a change after
        # the transaction's first postcondition cannot acquire a bundle
        # record merely because the earlier read-back succeeded.
        out.verify_written(
            "bundle-manifest",
            next(member["name"] for member in cfg["members"]
                 if member["kind"] == "bundle-manifest"),
            manifest_bytes)
        out.verify_written("bundle", cfg["name"], zip_bytes)
        out.verify_written(
            "bundle-checksum", cfg["name"] + ".sha256", checksum_bytes)
        bundlezip.verify_detached_checksum(
            checksum_bytes, cfg["name"], canon.bytes_digest(zip_bytes))
        record = {
            "bundle": cfg["name"],
            "bundleDigest": canon.bytes_digest(zip_bytes),
            "members": [{"name": n, "digest": canon.bytes_digest(d)}
                        for n, d in members],
            "releaseRecords": plan["releaseRecords"],
            "manifestWording": manifest_wording,
            "manifestApproval": plan["manifestApproval"],
            "bundleConfigDigest": boot.read_log[config_path],
            "approvalStatus": "passed",
            "operator": operator,
            "operatorKind": operator_kind,
            "acceptanceReceipt": acceptance_receipt,
        }
        record_problems = bundlezip.bundle_record_problems(
            record, fresh_cfg, canon.bytes_digest(zip_bytes),
            boot.read_log[config_path],
            expected_edition_count=DELIVERY_EDITION_COUNT,
            current_acceptance_context=fresh_bundle_receipt_context)
        if record_problems:
            raise bundlezip.BundleError("; ".join(record_problems))
    except (bundlezip.BundleError, gateway.GatewayError, model.ModelError,
            release_mod.AcceptanceError, OSError, SystemExit) as exc:
        raise SystemExit("bundle refused after output readback: %s" % exc)

    digest, rname = vgw.append("bundle-record", record)
    print("bundle -> dist/%s\n  bundle-record %s" % (cfg["name"], digest))


def cmd_status(argv):
    """Resolve and report the current digest chain (read-only): which
    records authorize the current derivation. Records are selected by
    digest equality, never recency (TDD §10)."""
    planes = load_planes()
    boot = gateway.ContentGateway(ROOT)
    config_path = BUNDLE_CONFIG
    cfg = canon.parse_json(boot.read_text(config_path))
    try:
        bundlezip.validate_bundle_config(
            cfg, expected_edition_count=DELIVERY_EDITION_COUNT)
    except bundlezip.BundleError as exc:
        print("bundle: invalid config (%s)" % exc)
        return
    vgw = gateway.VerificationGateway(RECORDS, "status", planes)
    ags = gateway.ArtifactGateway(DIST, "status", planes)
    qa_records = vgw.read_all("qa-record")
    attestations = vgw.read_all("attestation")
    release_records = vgw.read_all("release-record")
    try:
        attestation_policy, current_attestation_sides = \
            bundle_attestation_context(cfg)
        acceptance_contexts, bundle_runner_inputs = \
            bundle_acceptance_context(cfg)
        bundle_receipt_context = release_mod.combine_acceptance_contexts(
            acceptance_contexts, cfg["editions"])
    except (gateway.GatewayError, model.ModelError,
            release_mod.AcceptanceError, OSError, SystemExit) as exc:
        print("bundle: invalid edition policy (%s)" % exc)
        return
    release_bindings = {}
    qa_authorization_contexts = {}
    for ed in cfg["editions"]:
        print("edition %s" % ed)
        try:
            m, html, lock = derive(ed, "candidate")
        except SystemExit as e:
            print("  derivation: INVALID (%s)" % e)
            continue
        cdig = canon.bytes_digest(html)
        release_bindings[ed] = {
            "sealed": m.edition["artifactName"],
            "sealedDigest": cdig,
            "lockDigest": lock["lockDigest"],
            "declaredReleaseTimestamp":
                m.edition["declaredReleaseTimestamp"],
        }
        qa_authorization_contexts[ed] = {
            "qaInputLock": qa_input_lock(
                m, cdig, lock["lockDigest"]),
            "supportMatrixApprover": m.support_matrix.get("approver"),
            "supportMatrixTargets": copy.deepcopy(
                m.support_matrix.get("targets")),
            "supportMatrixViewport": copy.deepcopy(
                m.support_matrix.get("viewport")),
            "apiProbeApis": sorted(render.api_probe_instruments(
                m.api_policy)),
        }
        print("  derivation: valid; candidate %s… lock %s…"
              % (cdig[:20], lock["lockDigest"][:20]))
        name = "candidate_" + m.edition["artifactName"]
        if os.path.exists(os.path.join(DIST, name)):
            current = ags.read("candidate", name) == html
            print("  dist candidate: %s" % ("current" if current else "STALE"))
        else:
            print("  dist candidate: missing")
        valid_qa, _ = current_authorized_qa_records(
            m, cdig, lock, qa_records, attestations)
        qa_digest = valid_qa[0]["digest"] if valid_qa else None
        print("  qa-record: %s" % (
            qa_digest[:20] + "…" if qa_digest
            else "none with complete current authorized operator evidence"))

        valid_qa_digests = {record["digest"] for record in valid_qa}
        releases = []
        for envelope in release_records:
            record = envelope.get("record") if isinstance(envelope, dict) \
                else None
            if not isinstance(record, dict):
                continue
            if (record.get("edition"), record.get("sealed"),
                    record.get("sealedDigest"), record.get("lockDigest"),
                    record.get("declaredReleaseTimestamp")) != (
                    ed, m.edition["artifactName"], cdig,
                    lock["lockDigest"],
                    m.edition["declaredReleaseTimestamp"]):
                continue
            if record.get("qaRecord") not in valid_qa_digests:
                continue
            if bundlezip.release_chain_problems(
                    envelope, qa_records, attestations,
                    attestation_policy[ed],
                    current_attestation_sides[ed],
                    approval_evidence_problems,
                    acceptance_contexts[ed],
                    qa_authorization_contexts[ed]):
                continue
            releases.append(envelope)
        releases.sort(key=_approval_selection_key)
        if releases:
            release_record = releases[0]
            sealed_name = release_record["record"]["sealed"]
            sealed_ok, checksum_ok = release_artifact_status(
                ags, sealed_name, cdig)
            print("  release-record: %s… sealed file %s; checksum %s"
                  % (release_record["digest"][:20],
                     "current" if sealed_ok else "STALE",
                     "current" if checksum_ok else "STALE"))
        else:
            print("  release-record: none with a current authorized chain")
        current_sides = current_side_digests(m)
        required_types = _required_attestation_types(m)
        chosen, _ = _confirmed_current_attestations(
            attestations, current_sides, ed, required_types,
            m.support_matrix.get("approver"))
        print("  attestations authorized/current: %d of %d required"
              % (len(chosen), len(required_types)))
    unused_manifest, manifest_bytes, manifest_wording = \
        bundle_manifest_input(boot)
    config_current = False
    if set(release_bindings) == set(cfg["editions"]):
        try:
            proposed = _propose_current_bundle_config(
                cfg, release_records, qa_records, attestations, ags.read,
                manifest_bytes, manifest_wording, attestation_policy,
                current_attestation_sides, acceptance_contexts,
                release_bindings, qa_authorization_contexts)
            config_current = proposed == cfg
        except (bundlezip.BundleError, gateway.GatewayError,
                model.ModelError, release_mod.AcceptanceError, OSError,
                KeyError, TypeError, ValueError):
            pass
    print("bundle config: %s"
          % ("current" if config_current else "STALE/unavailable"))

    bpath = os.path.join(DIST, cfg["name"])
    if os.path.exists(bpath):
        bundle_bytes = ags.read("bundle", cfg["name"])
        bdig = canon.bytes_digest(bundle_bytes)
        expected_members = [(m["name"], m["digest"])
                            for m in cfg["members"]]
        try:
            actual_members = [(name, canon.bytes_digest(data))
                              for name, data in
                              bundlezip.read_zip_members(bundle_bytes)]
            members_current = actual_members == expected_members
        except bundlezip.BundleError:
            members_current = False
        try:
            checksum = ags.read("bundle-checksum", cfg["name"] + ".sha256")
            bundlezip.verify_detached_checksum(checksum, cfg["name"], bdig)
            checksum_current = True
        except (bundlezip.BundleError, gateway.GatewayError, OSError):
            checksum_current = False

        exact_records = [
            envelope for envelope in vgw.read_all("bundle-record")
            if not bundlezip.bundle_record_problems(
                envelope["record"], cfg, bdig,
                boot.read_log[config_path],
                current_acceptance_context=bundle_receipt_context)]
        selected_record = min(
            exact_records, key=_approval_selection_key, default=None)
        record_digest = selected_record["digest"] \
            if selected_record is not None else None
        print("bundle: %s… record %s; members %s; checksum %s; "
              "configured release/approval chain: %s"
              % (bdig[:20],
                 record_digest[:20] + "…" if record_digest else "MISSING",
                 "current" if members_current else "STALE",
                 "current" if checksum_current else "STALE",
                 "yes" if config_current and record_digest else "NO"))
    else:
        print("bundle: not built")


def main(argv):
    ci_guard(argv)
    argv = [a for a in argv if a != "--private-runner"]
    if not argv:
        raise SystemExit(
            "usage: build.py preview|candidate|migrate|record-qa|release "
            "<edition> | attest <type> [edition] | bundle-plan | bundle | "
            "status")
    cmd, rest = argv[0], argv[1:]
    single_edition = {
        "preview": cmd_preview,
        "candidate": cmd_candidate,
        "migrate": cmd_migrate,
        "release": cmd_release,
    }
    if cmd in single_edition:
        if len(rest) != 1 or rest[0].startswith("--"):
            raise SystemExit("usage: build.py %s <edition>" % cmd)
        single_edition[cmd](rest[0], [])
    elif cmd == "attest":
        cmd_attest(rest)
    elif cmd == "record-qa":
        if not rest or rest[0].startswith("--"):
            raise SystemExit(RECORD_QA_USAGE)
        cmd_record_qa(rest[0], rest[1:])
    elif cmd == "bundle-plan":
        if rest:
            raise SystemExit("usage: build.py bundle-plan")
        cmd_bundle_plan(rest)
    elif cmd == "bundle":
        if rest:
            raise SystemExit("usage: build.py bundle")
        cmd_bundle(rest)
    elif cmd == "status":
        if rest:
            raise SystemExit("usage: build.py status")
        cmd_status(rest)
    elif cmd == "propose-reuse":
        raise SystemExit("propose-reuse is deferred (TDD §10.7)")
    else:
        raise SystemExit("unknown command %r" % cmd)


if __name__ == "__main__":
    main(sys.argv[1:])
