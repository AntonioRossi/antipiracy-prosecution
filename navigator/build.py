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
import re
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import acceptance, authority, canon, gateway, model  # noqa: E402
from lib import bundlezip, currentstate, qaevidence  # noqa: E402
from lib import recordprovenance, render, schema_validate  # noqa: E402
from lib import snapshot, validate  # noqa: E402
from lib import migrate as migrate_mod, release as release_mod  # noqa: E402

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


def load_planes(byte_source=None):
    planes = canon.parse_json(
        gateway.ContentGateway(ROOT, byte_source=byte_source).read_text(
            "navigator/schema/planes.json"))
    version_problems = canon.require_version(planes, "planesVersion", "1")
    if version_problems:
        raise SystemExit(
            "navigator/schema/planes.json: %s" % version_problems[0])
    return planes


_COMMAND_ID = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*\Z")


def load_commands(byte_source=None):
    """Load the closed command metadata registry (schema/commands.json).

    Every CLI command has exactly one entry carrying its canonical summary
    and usage strings; the registry, the planes matrix, and main's dispatch
    set are one closed command vocabulary, bound together by test.
    """
    document = canon.parse_json(
        gateway.ContentGateway(ROOT, byte_source=byte_source).read_text(
            "navigator/schema/commands.json"))
    problems = canon.require_version(document, "commandsVersion", "1")
    if not isinstance(document, dict) or \
            not {"commandsVersion", "commands"}.issubset(document) or \
            not set(document) <= {"commandsVersion", "comment", "commands"}:
        problems.append("commands registry fields are not closed")
    commands = document.get("commands") if isinstance(document, dict) else None
    if not isinstance(commands, dict) or not commands:
        problems.append("commands registry has no command entries")
        commands = {}
    for name, entry in sorted(commands.items()):
        if not isinstance(name, str) or _COMMAND_ID.fullmatch(name) is None:
            problems.append("command name %r is malformed" % (name,))
            continue
        if not isinstance(entry, dict) or set(entry) != {"summary", "usage"}:
            problems.append("command %r fields are not closed" % name)
            continue
        if any(not isinstance(entry[field], str) or
               not entry[field].strip() or
               canon.normalize_nfc(entry[field]) != entry[field]
               for field in ("summary", "usage")):
            problems.append("command %r metadata is malformed" % name)
    if problems:
        raise SystemExit("navigator/schema/commands.json: %s" % problems[0])
    return document


def _command_snapshot():
    """Capture the one immutable byte source for a read-only command.

    Read-only verification commands capture the repository once at their
    boundary and consume only the captured bytes through gateway byte
    sources, so a repeated or inconsistent live read is structurally
    impossible within one command invocation.
    """
    try:
        return snapshot.RepositorySnapshot.capture(ROOT, retain_bytes=True)
    except snapshot.SnapshotError as exc:
        raise SystemExit("cannot snapshot current repository: %s" % exc)


def cmd_preview(edition_id, argv):
    planes = load_planes()
    m, html, _ = currentstate.derive(edition_id, "preview")
    out = gateway.OutputGateway(DIST, "preview", planes)
    name = "preview_" + m.edition["artifactName"]
    digest = out.write("preview", name, html)
    print("preview %s -> dist/%s (%s)" % (edition_id, name, digest[:20]))


def cmd_candidate(edition_id, argv):
    planes = load_planes()
    m, html, lock = currentstate.derive(edition_id, "candidate")
    out = gateway.OutputGateway(DIST, "candidate", planes)
    name = "candidate_" + m.edition["artifactName"]
    digest = out.write("candidate", name, html)
    print("candidate %s -> dist/%s" % (edition_id, name))
    print("  candidateDigest %s" % digest)
    print("  lockDigest %s" % lock["lockDigest"])


def cmd_pin_plan(edition_id, argv):
    """Print the canonical representation of :func:`current_pin_plan`."""
    snap = _command_snapshot()
    print(canon.canonical_json(currentstate.current_pin_plan(
        edition_id, byte_source=snap.byte_source(),
        planes=load_planes(snap.byte_source()))
    ).decode("utf-8"))


def cmd_migrate(edition_id, argv):
    gw, m = currentstate.build_model(edition_id)
    before_relation = copy.deepcopy(m.relation)
    before_inventory = copy.deepcopy(m.gates)
    log = []
    migrate_mod.migrate_inventory(m, log)
    migrate_mod.migrate_relation(m, log)
    diff_problems = migrate_mod.migration_diff_problems(
        before_relation, m.relation, before_inventory, m.gates,
        fragment_hashes={fid: unit.digest for fid, unit in m.units.items()})
    schema_problems = []
    for name, instance in (("relation", m.relation),
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
    if atype in currentstate.EDITION_ATTEST_TYPES and edition_id is None:
        raise SystemExit("%s requires an edition" % atype)
    if atype not in currentstate.EDITION_ATTEST_TYPES and \
            edition_id is not None:
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
        _, m = currentstate.build_model(edition_id)
        entry = m.registry.entry(m.edition["claimCorpus"])
        sides["claimSet"] = m.gw.read_log[entry["primary"]]
        sides["gateInventory"] = m.gw.read_log[m.edition["gateInventory"]]
    elif atype == "qa-priority-map":
        _, m = currentstate.build_model(edition_id)
        sides["relationSet"] = m.gw.read_log[m.edition["relationSet"]]
        sides["priorityMap"] = currentstate._verified_qa_primary_digest(
            m, "priorityMap")
    elif atype == "qa-crosswalk":
        _, m = currentstate.build_model(edition_id)
        sides["relationSet"] = m.gw.read_log[m.edition["relationSet"]]
        sides["crosswalk"] = currentstate._verified_qa_primary_digest(
            m, "crosswalk")
    elif atype == "legend-approval":
        strings = canon.parse_json(gw.read_text("navigator/strings.json"))
        sides["legendWording"] = canon.text_digest(
            canon.canon_prose(strings["counselLegend"]))
    elif atype == "manifest-approval":
        unused_manifest, unused_bytes, manifest_wording = \
            currentstate.bundle_manifest_input(gw)
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
        approver_problems = currentstate._support_matrix_approver_problems(
            matrix["approver"])
        if approver_problems:
            raise SystemExit("; ".join(approver_problems))
        binding_problems = \
            currentstate._support_matrix_operator_binding_problems(
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


def cmd_record_qa(edition_id, argv):
    options = parse_record_qa_options(argv)
    m, html, lock = currentstate.derive(edition_id, "candidate")
    acceptance_registry = acceptance.load_registry(ROOT)
    release_profile, profile_contract = \
        acceptance.release_profile_contract(
            m.release_policy, acceptance_registry)
    manual_fields = tuple(profile_contract["requiredQaRecordFields"])
    api_probe_apis = sorted(render.api_probe_instruments(m.api_policy))
    if options["template"]:
        template = qaevidence.pending_manual_checks_template(
            m.support_matrix, api_probe_apis)
        print(json.dumps(template, indent=2, ensure_ascii=False,
                         sort_keys=True))
        return

    if profile_contract["manualQaEvidence"] != "required":
        raise SystemExit(
            "record-qa is deferred for the active %s profile; switch the "
            "reviewed acceptance contract to validated-release before "
            "recording compatibility authorization" % release_profile)

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
    internal_lock = currentstate.qa_input_lock(
        m, candidate_digest, lock["lockDigest"])
    vgw = gateway.VerificationGateway(RECORDS, "record-qa", planes)
    side_digests = currentstate.current_side_digests(m)
    all_attestations = vgw.read_all("attestation")
    required = currentstate._required_attestation_types(m)
    support_matrix = canon.parse_json(m.support_matrix_bytes)
    chosen, attestation_problems = \
        currentstate._confirmed_current_attestations(
            all_attestations, side_digests, edition_id, required,
            support_matrix.get("approver"))
    evidence_problems = list(attestation_problems)
    evidence_problems.extend(currentstate._support_matrix_approver_problems(
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
        "releaseProfile": release_profile,
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
    authorization_problems = currentstate.qa_authorization_problems(
        envelope, candidate_digest, lock, internal_lock, support_matrix,
        api_probe_apis, legend_digest, all_attestations, side_digests,
        edition_id, required, manual_fields, release_profile)
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


RELEASE_USAGE = (
    "usage: build.py release <edition> "
    "--profile=<active-release-profile>"
)


def _release_profile_arg(argv):
    if len(argv) != 1 or not isinstance(argv[0], str) or \
            not argv[0].startswith("--profile="):
        raise SystemExit(RELEASE_USAGE)
    release_profile = argv[0].split("=", 1)[1]
    if not release_profile or not release_profile.isascii() or \
            not all(character.islower() or character.isdigit() or
                    character == "-" for character in release_profile) or \
            release_profile.startswith("-") or release_profile.endswith("-"):
        raise SystemExit("release profile id is malformed")
    return release_profile


def cmd_release(edition_id, argv):
    requested_profile = _release_profile_arg(argv)
    planes = load_planes()
    m, html, lock = currentstate.derive(edition_id, "release")
    acceptance_registry = acceptance.load_registry(ROOT)
    release_profile, profile_contract = \
        acceptance.release_profile_contract(
            m.release_policy, acceptance_registry, requested_profile)
    manual_qa_required = profile_contract["manualQaEvidence"] == "required"
    name = "candidate_" + m.edition["artifactName"]
    if not os.path.exists(os.path.join(DIST, name)):
        raise SystemExit("no candidate to release")
    candidate_bytes = gateway.ArtifactGateway(
        DIST, "release", planes).read("candidate", name)
    if candidate_bytes != html:
        raise SystemExit("release derivation does not byte-match the "
                         "profile candidate")
    candidate_digest = canon.bytes_digest(candidate_bytes)
    vgw = gateway.VerificationGateway(RECORDS, "release", planes)
    qa_records = vgw.read_all("qa-record")
    attestations = vgw.read_all("attestation")
    qa = None
    if manual_qa_required:
        valid_qa, rejected = currentstate.current_authorized_qa_records(
            m, candidate_digest, lock, qa_records, attestations)
        if not valid_qa:
            for digest, qa_problems in rejected:
                for problem in qa_problems:
                    sys.stderr.write("  [release] qa-record %s: %s\n"
                                     % (digest, problem))
            raise SystemExit(
                "release refused: validated-release requires a matching "
                "qa-record with complete passed authorized operator evidence")
        qa = valid_qa[0]
        attestation_refs = sorted(qa["record"]["attestations"])
    else:
        required = currentstate._required_attestation_types(m)
        chosen, attestation_problems = \
            currentstate._confirmed_current_attestations(
                attestations, currentstate.current_side_digests(m),
                edition_id, required, m.support_matrix.get("approver"))
        if attestation_problems:
            for problem in attestation_problems:
                sys.stderr.write("  [release] %s\n" % problem)
            raise SystemExit(
                "release refused: technical-preview requires current "
                "authorized content attestations")
        attestation_refs = sorted(
            envelope["digest"] for envelope in chosen.values())
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
            ROOT, m, html, candidate_bytes, lock, qa, out,
            release_profile=release_profile)
    except (acceptance.AcceptanceError, gateway.GatewayError,
            bundlezip.BundleError, OSError, subprocess.SubprocessError) as exc:
        raise SystemExit("release refused: acceptance transaction failed: %s"
                         % exc)
    record = {
        "recordVersion": "3",
        **acceptance.profile_record_fields(profile_contract),
        "edition": edition_id,
        "sealed": sealed_name,
        "sealedDigest": candidate_digest,
        "lockDigest": lock["lockDigest"],
        "qaRecord": qa["digest"] if qa is not None else None,
        "attestations": attestation_refs,
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
        fresh_m, fresh_html, fresh_lock = currentstate.derive(
            edition_id, "release")
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
        fresh_acceptance_registry = acceptance.load_registry(ROOT)
        fresh_profile, fresh_profile_contract = \
            acceptance.release_profile_contract(
                fresh_m.release_policy, fresh_acceptance_registry,
                requested_profile)
        if fresh_profile != release_profile or \
                fresh_profile_contract != profile_contract:
            raise bundlezip.BundleError(
                "release profile changed during promotion")
        if manual_qa_required:
            fresh_valid, unused_rejected = \
                currentstate.current_authorized_qa_records(
                    fresh_m, candidate_digest, fresh_lock,
                    fresh_qas, fresh_attestations)
            if not fresh_valid or fresh_valid[0]["digest"] != qa["digest"]:
                raise bundlezip.BundleError(
                    "selected QA authorization changed during promotion")
        else:
            fresh_chosen, fresh_attestation_problems = \
                currentstate._confirmed_current_attestations(
                    fresh_attestations,
                    currentstate.current_side_digests(fresh_m),
                    edition_id,
                    currentstate._required_attestation_types(fresh_m),
                    fresh_m.support_matrix.get("approver"))
            fresh_refs = sorted(
                envelope["digest"] for envelope in fresh_chosen.values())
            if fresh_attestation_problems or fresh_refs != attestation_refs:
                raise bundlezip.BundleError(
                    "selected preview attestations changed during promotion")
        fresh_context = acceptance.acceptance_context(
            ROOT, (edition_id,), release_profile=release_profile)
        envelope = {
            "kind": "release-record",
            "digest": canon.composite_digest(
                "aa11393:release-record:c1", record),
            "record": record,
        }
        chain_problems = bundlezip.release_chain_problems(
            envelope, fresh_qas, fresh_attestations,
            currentstate._required_attestation_types(fresh_m),
            currentstate.current_side_digests(fresh_m),
            currentstate.approval_evidence_problems,
            fresh_context, ({
                "qaInputLock": currentstate.qa_input_lock(
                    fresh_m, candidate_digest, fresh_lock["lockDigest"]),
                "supportMatrixApprover":
                    fresh_m.support_matrix.get("approver"),
                "supportMatrixTargets": copy.deepcopy(
                    fresh_m.support_matrix.get("targets")),
                "supportMatrixViewport": copy.deepcopy(
                    fresh_m.support_matrix.get("viewport")),
                "apiProbeApis": sorted(render.api_probe_instruments(
                    fresh_m.api_policy)),
            } if manual_qa_required else None))
        if chain_problems:
            raise bundlezip.BundleError("; ".join(chain_problems))
    except (bundlezip.BundleError, gateway.GatewayError, model.ModelError,
            acceptance.AcceptanceError, OSError, SystemExit) as exc:
        raise SystemExit("release refused after output readback: %s" % exc)
    digest, rname = vgw.append("release-record", record)
    print("release %s -> dist/%s sealed\n  release-record %s"
          % (edition_id, sealed_name, digest))


def cmd_bundle_plan(argv):
    """Print a verified proposed bundle config; never write source/evidence."""
    try:
        state = currentstate._current_bundle_plan_state(
            "bundle-plan", _command_snapshot().byte_source(), load_planes)
    except (bundlezip.BundleError, gateway.GatewayError, model.ModelError,
            acceptance.AcceptanceError, OSError, SystemExit,
            snapshot.SnapshotError) as exc:
        raise SystemExit("bundle-plan refused: %s" % exc)
    # Stdout is the sole output of this read-only command.  Emit the same
    # canonical JSON encoding used by digest-bearing structures so repeated
    # plans have one byte representation independent of mapping insertion
    # order or interpreter formatting choices.
    encoded = canon.canonical_json(state["proposed"]) + b"\n"
    stdout_buffer = getattr(sys.stdout, "buffer", None)
    if stdout_buffer is None:  # e.g. an in-process StringIO test harness
        sys.stdout.write(encoded.decode("utf-8"))
    else:
        stdout_buffer.write(encoded)


def cmd_bundle(argv):
    planes = load_planes()
    boot = gateway.ContentGateway(ROOT)
    config_path = currentstate.BUNDLE_CONFIG
    cfg = canon.parse_json(boot.read_text(config_path))
    vgw = gateway.VerificationGateway(RECORDS, "bundle", planes)
    manifest, manifest_bytes, manifest_wording = \
        currentstate.bundle_manifest_input(boot)
    artifacts = gateway.ArtifactGateway(DIST, "bundle", planes)
    release_records = vgw.read_all("release-record")
    qa_records = vgw.read_all("qa-record")
    attestations = vgw.read_all("attestation")
    try:
        bundlezip.validate_bundle_config(
            cfg, expected_edition_count=currentstate.DELIVERY_EDITION_COUNT)
        attestation_policy, current_attestation_sides = \
            currentstate.bundle_attestation_context(cfg)
        acceptance_contexts = currentstate.bundle_acceptance_context(cfg)
        bundle_receipt_context = acceptance.combine_acceptance_contexts(
            acceptance_contexts, cfg["editions"])
        bindings = currentstate.current_release_bindings(cfg)
        qa_authorization_contexts = \
            currentstate.bundle_qa_authorization_context(
                cfg, bindings)
        proposed = currentstate._propose_current_bundle_config(
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
            currentstate.approval_evidence_problems, attestation_policy,
            current_attestation_sides,
            expected_edition_count=currentstate.DELIVERY_EDITION_COUNT,
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
            acceptance.AcceptanceError, OSError, SystemExit) as exc:
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
            ROOT, cfg, boot.read_log[config_path], plan,
            zip_bytes, checksum_bytes, manifest_bytes, out)
    except (acceptance.AcceptanceError, bundlezip.BundleError,
            gateway.GatewayError, OSError) as exc:
        raise SystemExit("bundle refused: acceptance transaction failed: %s"
                         % exc)
    # Re-derive the complete bundle plan after output readback.  A concurrent
    # content/artifact change may leave unauthorizing output bytes, but can
    # never acquire the append-only bundle record that authorizes delivery.
    try:
        fresh_cfg = canon.parse_json(boot.read_text(config_path))
        fresh_manifest, fresh_manifest_bytes, fresh_manifest_wording = \
            currentstate.bundle_manifest_input(boot)
        if fresh_cfg != cfg or fresh_manifest != manifest:
            raise bundlezip.BundleError(
                "bundle content inputs changed during promotion")
        fresh_release_records = vgw.read_all("release-record")
        fresh_qa_records = vgw.read_all("qa-record")
        fresh_attestations = vgw.read_all("attestation")
        fresh_policy, fresh_sides = \
            currentstate.bundle_attestation_context(fresh_cfg)
        fresh_contexts = currentstate.bundle_acceptance_context(fresh_cfg)
        fresh_bundle_receipt_context = \
            acceptance.combine_acceptance_contexts(
                fresh_contexts, fresh_cfg["editions"])
        fresh_bindings = currentstate.current_release_bindings(fresh_cfg)
        fresh_qa_authorization_contexts = \
            currentstate.bundle_qa_authorization_context(
                fresh_cfg, fresh_bindings)
        fresh_proposed = currentstate._propose_current_bundle_config(
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
            "recordVersion": "3",
            **acceptance.profile_record_fields(
                fresh_bundle_receipt_context["releaseProfileContract"]),
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
            expected_edition_count=currentstate.DELIVERY_EDITION_COUNT,
            current_acceptance_context=fresh_bundle_receipt_context)
        if record_problems:
            raise bundlezip.BundleError("; ".join(record_problems))
    except (bundlezip.BundleError, gateway.GatewayError, model.ModelError,
            acceptance.AcceptanceError, OSError, SystemExit) as exc:
        raise SystemExit("bundle refused after output readback: %s" % exc)

    digest, rname = vgw.append("bundle-record", record)
    print("bundle -> dist/%s\n  bundle-record %s" % (cfg["name"], digest))


def cmd_verify_current(argv):
    try:
        report = currentstate.verify_current_state(
            run_tests=True, load_planes=load_planes)
    except (bundlezip.BundleError, gateway.GatewayError, model.ModelError,
            acceptance.AcceptanceError, OSError, RuntimeError,
            snapshot.SnapshotError, SystemExit, KeyError, TypeError,
            ValueError) as exc:
        raise SystemExit("verify-current refused: %s" % exc)
    print(canon.canonical_json(report).decode("utf-8"))


def cmd_validate_current(argv):
    try:
        report = currentstate.validate_current_state(
            run_tests=True, load_planes=load_planes)
    except (bundlezip.BundleError, gateway.GatewayError, model.ModelError,
            acceptance.AcceptanceError, OSError, RuntimeError,
            snapshot.SnapshotError, SystemExit, KeyError, TypeError,
            ValueError) as exc:
        raise SystemExit("validate-current refused: %s" % exc)
    print(canon.canonical_json(report).decode("utf-8"))


def cmd_status(argv):
    """Resolve and report the current digest chain (read-only): which
    records authorize the current derivation. Records are selected by
    digest equality, never recency (TDD §10)."""
    snap = _command_snapshot()
    try:
        currentstate._status_report(snap, load_planes)
    except snapshot.SnapshotError as exc:
        raise SystemExit(
            "status refused: repository changed during status: %s" % exc)


USAGE = """usage: build.py <command> [arguments]
  build.py attest <type> [edition] --approved --note=<evidence>
  build.py bundle
  build.py bundle-plan
  build.py candidate <edition>
  build.py migrate <edition>
  build.py pin-plan <edition>
  build.py preview <edition>
  build.py propose-reuse (deferred)
  build.py record-qa <edition> [--template | [--check-only] (--evidence-file=<workspace-relative.json> | --acNN=<JSON> ...) ]
  build.py release <edition> --profile=<active-release-profile>
  build.py status
  build.py validate-current
  build.py verify-current"""


def main(argv):
    ci_guard(argv)
    argv = [a for a in argv if a != "--private-runner"]
    if not argv:
        raise SystemExit(USAGE)
    cmd, rest = argv[0], argv[1:]
    single_edition = {
        "preview": cmd_preview,
        "candidate": cmd_candidate,
        "migrate": cmd_migrate,
        "pin-plan": cmd_pin_plan,
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
    elif cmd == "release":
        if not rest or rest[0].startswith("--"):
            raise SystemExit(RELEASE_USAGE)
        cmd_release(rest[0], rest[1:])
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
    elif cmd == "verify-current":
        if rest:
            raise SystemExit("usage: build.py verify-current")
        cmd_verify_current(rest)
    elif cmd == "validate-current":
        if rest:
            raise SystemExit("usage: build.py validate-current")
        cmd_validate_current(rest)
    elif cmd == "propose-reuse":
        raise SystemExit("propose-reuse is deferred (TDD §10.7)")
    else:
        raise SystemExit("unknown command %r" % cmd)


if __name__ == "__main__":
    main(sys.argv[1:])
