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
import tempfile

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import acceptance, authority, canon, gateway, model  # noqa: E402
from lib import pinplan, profilepolicy, qaevidence, qaregistry  # noqa: E402
from lib import render, snapshot  # noqa: E402
from lib import claims as claims_mod, registry as registry_mod  # noqa: E402
from lib import control_inventory, inputlock  # noqa: E402
from lib import recordprovenance, recordresolver  # noqa: E402
from lib import schema_validate, validate  # noqa: E402
from lib import migrate as migrate_mod, release as release_mod  # noqa: E402
from lib import bundleplan, bundlezip  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "navigator", "dist")
RECORDS = os.path.join(ROOT, "navigator", "records")
BUNDLE_CONFIG = "navigator/bundles/na-af-2026.json"
BUNDLE_MANIFEST_RESOURCE = "navigator/bundle-manifest.json"
CI_MARKERS = ("CI", "GITHUB_ACTIONS", "GITLAB_CI", "JENKINS_URL",
              "BUILDKITE", "CIRCLECI", "TRAVIS", "TEAMCITY_VERSION")
DELIVERY_EDITION_COUNT = 2
VERIFICATION_RECORD_KINDS = (
    "attestation", "qa-record", "release-record", "bundle-record",
)
LIVE_VERSION_PATTERN = re.compile(
    r"\b(?P<strategy>NA|AF)-[0-9]{4}-[0-9]{2}-[0-9]{2}-v[1-9][0-9]*\b")
LIVE_TEXT_SUFFIXES = frozenset((
    ".json", ".md", ".py", ".sh", ".txt", ".yaml", ".yml",
))


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
    planes = canon.parse_json(
        gateway.ContentGateway(ROOT).read_text("navigator/schema/planes.json"))
    version_problems = canon.require_version(planes, "planesVersion", "1")
    if version_problems:
        raise SystemExit(
            "navigator/schema/planes.json: %s" % version_problems[0])
    return planes


def delivery_edition_ids(content=None):
    """Return the bundle-declared edition IDs after path-safe validation."""
    content = content or gateway.ContentGateway(ROOT)
    cfg = canon.parse_json(content.read_text(BUNDLE_CONFIG))
    editions = cfg.get("editions") if isinstance(cfg, dict) else None
    if not isinstance(editions, list) or \
            len(editions) != DELIVERY_EDITION_COUNT or \
            len(editions) != len(set(editions)):
        raise SystemExit(
            "delivery bundle must declare exactly %d unique editions" %
            DELIVERY_EDITION_COUNT)
    for edition_id in editions:
        edition_path(edition_id)
    return tuple(editions)


def bundle_manifest_input(content):
    """Return the closed bundle-only manifest text, bytes, and wording hash."""
    value = canon.parse_json(content.read_text(BUNDLE_MANIFEST_RESOURCE))
    release_profile = value.get("releaseProfile") \
        if isinstance(value, dict) else None
    try:
        policy = canon.parse_json(content.read_text(
            acceptance.RELEASE_POLICY_PATH))
        unused_profile, profile_contract = profilepolicy.profile_contract(
            policy, release_profile)
        expected_profile = profilepolicy.record_fields(profile_contract)
    except profilepolicy.ProfilePolicyError:
        expected_profile = None
    if not isinstance(value, dict) or \
            set(value) != {"manifestVersion", "releaseProfile",
                           "compatibilityAuthorization",
                           "deferredControls", "bundleManifestText"} or \
            canon.require_version(value, "manifestVersion", "3") or \
            expected_profile is None or \
            value.get("compatibilityAuthorization") != \
                expected_profile["compatibilityAuthorization"] or \
            value.get("deferredControls") != \
                expected_profile["deferredControls"] or \
            not isinstance(value.get("bundleManifestText"), str) or \
            not value["bundleManifestText"] or \
            not value["bundleManifestText"].startswith(
                expected_profile["artifactLabel"]) or \
            expected_profile["compatibilityAuthorization"] == \
                "not-authorized" and \
                "does not claim compatibility authorization" not in \
                    value["bundleManifestText"]:
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


def build_model(edition_id, planes=None):
    boot = gateway.ContentGateway(ROOT)
    allow = canon.parse_json(
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
    problems = inputlock.exact_set_problems(
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


def _claim_document_version(text, strategy_prefix):
    pattern = re.compile(
        r"CLAIM-SET VERSION (" + re.escape(strategy_prefix) +
        r"-[0-9]{4}-[0-9]{2}-[0-9]{2}-v[1-9][0-9]*)")
    matches = pattern.findall(text)
    if len(set(matches)) != 1:
        raise SystemExit(
            "claim document must declare exactly one %s claim-set version" %
            strategy_prefix)
    return matches[0]


def _plan_schema():
    """Load and meta-validate the closed current-pin plan schema."""
    schema = canon.parse_json(gateway.ContentGateway(ROOT).read_text(
        "navigator/schema/plan.schema.json"))
    try:
        schema_validate.check_schema(schema)
    except schema_validate.SchemaError as exc:
        raise SystemExit("invalid plan schema: %s" % exc)
    return schema


def current_pin_plan(edition_id):
    """Return a deterministic, read-only current-pin plan.

    Unlike ``build_model``, this command deliberately reads registered source
    bytes without accepting their digest pins: its purpose is to expose drift
    before those pins are changed. Closed schemas and canonical paths are
    still enforced before any edition-selected path is dereferenced. Every
    registry and QA corpus the edition depends on is planned by the same
    generic closure, so integrity currency never narrows to a primary file.
    """
    boot = gateway.ContentGateway(ROOT)
    epath = edition_path(edition_id)
    edition = canon.parse_json(boot.read_text(epath))
    edition_schema = canon.parse_json(
        boot.read_text("navigator/schema/edition.schema.json"))
    problems = schema_validate.validate(edition, edition_schema)
    if problems:
        raise SystemExit("invalid edition config: %s" % "; ".join(problems))

    declared = edition["declaredTransitiveInputs"]
    content = gateway.ContentGateway(ROOT, allowlist=declared)
    reg = registry_mod.Registry(
        content, registry_paths=edition["corpusRegistries"],
        allowed_corpora={edition["claimCorpus"], edition["targetCorpus"],
                         edition["authorityCorpus"]}, require_exact=True)
    claim_entry = reg.entry(edition["claimCorpus"])
    claim_path = claim_entry["primary"]
    claim_bytes = content.read_bytes(claim_path)
    try:
        claim_text = claim_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SystemExit("claim document is not UTF-8: %s" % exc)
    profile = canon.parse_json(content.read_text(claim_entry["profile"]))
    parsed = claims_mod.parse_claims(
        claim_text, profile.get("claimsHeading", "Candidate claims"))
    count, units, per_claim = claims_mod.census(parsed)
    dependencies = {}
    for claim in parsed:
        if len(claim.parsed_refs) > 1:
            raise SystemExit(
                "claim %d has multiple dependency references" % claim.number)
        dependencies[str(claim.number)] = (
            claim.parsed_refs[0] if claim.parsed_refs else None)
    groups = list(dict.fromkeys(claim.group for claim in parsed))
    dependency_document = canon.parse_json(
        content.read_text(edition["dependencyMap"]))
    configured_dependencies = dependency_document.get("claims") \
        if isinstance(dependency_document, dict) else None
    document_version = _claim_document_version(
        claim_text, edition["strategyPrefix"])
    expected_artifact = (
        "AA11393US-%s-claims-spec-navigator_%s.html" %
        (edition["strategyPrefix"], document_version))

    qa_ids = {value for value in edition["qaSources"].values()
              if value is not None}
    qa_allow = [edition["qaRegistry"]]
    qa_boot = gateway.ContentGateway(ROOT)
    qa_doc = canon.parse_json(qa_boot.read_text(edition["qaRegistry"]))
    if not isinstance(qa_doc, dict) or not isinstance(
            qa_doc.get("corpora"), dict):
        raise SystemExit("QA registry is malformed")
    for entry in qa_doc["corpora"].values():
        if isinstance(entry, dict):
            qa_allow.extend(entry.get("files", {}).keys())
    qa_gateway = gateway.ContentGateway(ROOT, allowlist=qa_allow)
    qa_registry = qaregistry.QaRegistry(
        qa_gateway, edition["qaRegistry"], qa_ids)
    delivery_cfg = canon.parse_json(qa_boot.read_text(BUNDLE_CONFIG))
    delivery_versions = {}
    for delivery_edition_id in delivery_cfg.get("editions", []):
        delivery_edition = canon.parse_json(qa_boot.read_text(
            edition_path(delivery_edition_id)))
        delivery_versions[delivery_edition["strategyPrefix"]] = \
            delivery_edition["claimSetVersion"]
    corpora = {}
    for corpus_id in (edition["claimCorpus"], edition["targetCorpus"],
                      edition["authorityCorpus"]):
        corpora[corpus_id] = pinplan.corpus_closure(
            corpus_id, reg.entry(corpus_id), content)
    for role, corpus_id in sorted(edition["qaSources"].items()):
        if corpus_id is None:
            continue
        if corpus_id in corpora:
            raise SystemExit(
                "QA corpus id %r collides with a registry corpus" % corpus_id)
        entry = qa_registry.entry(corpus_id)
        expected_versions = (
            delivery_versions if role == "crosswalk" else {
                edition["strategyPrefix"]: edition["claimSetVersion"]})
        corpora[corpus_id] = pinplan.corpus_closure(
            corpus_id, entry, qa_gateway,
            expected_versions=expected_versions)

    census = {
        "claims": count, "units": units,
        "perClaim": {str(number): value
                     for number, value in per_claim.items()},
    }
    plan = {
        "planVersion": pinplan.PLAN_VERSION,
        "edition": edition_id,
        "claimCorpus": edition["claimCorpus"],
        "targetCorpus": edition["targetCorpus"],
        "authorityCorpus": edition["authorityCorpus"],
        "qaSources": {role: edition["qaSources"][role]
                      for role in sorted(edition["qaSources"])},
        "corpora": corpora,
        "documentVersion": document_version,
        "configuredCorpusVersion": claim_entry["version"],
        "configuredEditionVersion": edition["claimSetVersion"],
        "census": census,
        "configuredCensus": edition["census"],
        "censusCurrent": census == edition["census"],
        "groups": groups,
        "configuredGroups": edition["groups"],
        "groupsCurrent": groups == edition["groups"],
        "dependencies": dependencies,
        "configuredDependencies": configured_dependencies,
        "dependenciesCurrent": dependencies == configured_dependencies,
        "independentClaims": [int(number) for number, parent in
                              dependencies.items() if parent is None],
        "configuredIndependentClaims": edition["independentClaims"],
        "independentClaimsCurrent": [
            int(number) for number, parent in dependencies.items()
            if parent is None] == edition["independentClaims"],
        "artifactName": expected_artifact,
        "configuredArtifactName": edition["artifactName"],
        "artifactNameCurrent": expected_artifact == edition["artifactName"],
    }
    schema_problems = schema_validate.validate(plan, _plan_schema())
    if schema_problems:
        raise SystemExit("%s pin plan violates the closed plan schema: %s"
                         % (edition_id, "; ".join(schema_problems)))
    return plan


def cmd_pin_plan(edition_id, argv):
    """Print the canonical representation of :func:`current_pin_plan`."""
    print(canon.canonical_json(current_pin_plan(edition_id)).decode("utf-8"))


def cmd_migrate(edition_id, argv):
    gw, m = build_model(edition_id)
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

ATTESTATION_RECORD_FIELDS = recordprovenance.ATTESTATION_RECORD_FIELDS
QA_RECORD_FIELDS = recordprovenance.QA_RECORD_FIELDS

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
    """Return the edition-scoped QA registry through its sole live API."""
    return m.qa_registry().corpora


def _qa_registry_read(m):
    """Return the raw selected QA-registry read bound by ``qaInputLock``."""
    qa_registry = m.qa_registry()
    path = m.edition["qaRegistry"]
    if set(qa_registry.gw.read_log) != {path}:
        raise SystemExit(
            "QA registry gateway read set is not exactly %r" % path)
    return {"path": path, "digest": qa_registry.gw.read_log[path]}


def _delivery_version_bindings(root=ROOT):
    """Return the sole live strategy-to-claim-version map."""
    content = gateway.ContentGateway(root)
    cfg = canon.parse_json(content.read_text(BUNDLE_CONFIG))
    editions = cfg.get("editions") if isinstance(cfg, dict) else None
    if not isinstance(editions, list) or not editions or \
            len(editions) != len(set(editions)):
        raise SystemExit("delivery edition set is malformed")
    bindings = {}
    for edition_id in editions:
        edition = canon.parse_json(content.read_text(edition_path(edition_id)))
        strategy = edition.get("strategyPrefix") \
            if isinstance(edition, dict) else None
        version = edition.get("claimSetVersion") \
            if isinstance(edition, dict) else None
        if not isinstance(strategy, str) or not strategy or \
                not isinstance(version, str) or not version or \
                strategy in bindings:
            raise SystemExit("delivery version binding is malformed")
        bindings[strategy] = version
    return {strategy: bindings[strategy] for strategy in sorted(bindings)}


def _expected_qa_version_bindings(m, role):
    if role == "priorityMap":
        return {
            m.edition["strategyPrefix"]: m.edition["claimSetVersion"],
        }
    if role == "crosswalk":
        return _delivery_version_bindings(m.gw.root)
    raise SystemExit("unknown QA source role %r" % role)


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
        expected_versions = _expected_qa_version_bindings(m, role)
        if entry.get("versionBindings") != expected_versions:
            raise SystemExit(
                "QA source %r version bindings are stale: configured %r, "
                "expected %r" %
                (corpus_id, entry.get("versionBindings"),
                 expected_versions))
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
                              required_types, manual_fields,
                              expected_release_profile):
    """Return every defect that prevents a QA record authorizing release."""
    raw_record = qa.get("record") if isinstance(qa, dict) else None
    problems = approval_evidence_problems(raw_record, require_note=False)
    if not isinstance(raw_record, dict) or set(raw_record) != QA_RECORD_FIELDS:
        problems.append("QA record has the wrong fields")
    record = raw_record if isinstance(raw_record, dict) else {}
    if record.get("releaseProfile") != expected_release_profile:
        problems.append("QA record is not scoped to the current profile")
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
    acceptance_registry = acceptance.load_registry(ROOT)
    release_profile, profile_contract = \
        acceptance.release_profile_contract(
            m.release_policy, acceptance_registry)
    manual_fields = tuple(profile_contract["requiredQaRecordFields"])
    expected_qa_lock = qa_input_lock(
        m, candidate_digest, content_lock["lockDigest"])
    support_matrix = canon.parse_json(m.support_matrix_bytes)
    api_probe_apis = sorted(render.api_probe_instruments(m.api_policy))
    legend_digest = canon.text_digest(
        canon.canon_prose(m.strings["counselLegend"]))
    def format_problems(envelope):
        if not isinstance(envelope, dict) or \
                envelope.get("kind") != "qa-record":
            return ["QA envelope has the wrong kind or shape"]
        return recordprovenance.current_record_format_problems(
            "qa-record", envelope.get("record"))

    def currency_problems(envelope):
        record = envelope["record"]
        if record.get("edition") != m.edition["editionId"] or \
                record.get("candidateDigest") != candidate_digest or \
                record.get("lockDigest") != content_lock["lockDigest"] or \
                record.get("releaseProfile") != release_profile:
            return ["QA record is valid same-schema superseded evidence"]
        return []

    def authorization_problems(envelope):
        return qa_authorization_problems(
            envelope, candidate_digest, content_lock, expected_qa_lock,
            support_matrix, api_probe_apis, legend_digest, attestations,
            side_digests, m.edition["editionId"], required, manual_fields,
            release_profile)

    resolution = recordresolver.classify(
        qa_records, format_problems, currency_problems,
        authorization_problems)
    rejected = [
        (item.digest, list(item.problems))
        for item in resolution.invalid_records +
        resolution.rejected_authorizations
    ]
    current = sorted(
        resolution.current_authorizations, key=_approval_selection_key)
    if not current:
        rejected.append(("<current-binding>", [
            "no qa-record matches and authorizes the current edition, "
            "profile, candidate digest, and content-input lock"
        ]))
    return current, rejected


def cmd_record_qa(edition_id, argv):
    options = parse_record_qa_options(argv)
    m, html, lock = derive(edition_id, "candidate")
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
    authorization_problems = qa_authorization_problems(
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
    m, html, lock = derive(edition_id, "release")
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
        valid_qa, rejected = current_authorized_qa_records(
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
        required = _required_attestation_types(m)
        chosen, attestation_problems = _confirmed_current_attestations(
            attestations, current_side_digests(m), edition_id, required,
            m.support_matrix.get("approver"))
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
            fresh_valid, unused_rejected = current_authorized_qa_records(
                fresh_m, candidate_digest, fresh_lock,
                fresh_qas, fresh_attestations)
            if not fresh_valid or fresh_valid[0]["digest"] != qa["digest"]:
                raise bundlezip.BundleError(
                    "selected QA authorization changed during promotion")
        else:
            fresh_chosen, fresh_attestation_problems = \
                _confirmed_current_attestations(
                    fresh_attestations, current_side_digests(fresh_m),
                    edition_id, _required_attestation_types(fresh_m),
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
            _required_attestation_types(fresh_m),
            current_side_digests(fresh_m), approval_evidence_problems,
            fresh_context, ({
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
            } if manual_qa_required else None))
        if chain_problems:
            raise bundlezip.BundleError("; ".join(chain_problems))
    except (bundlezip.BundleError, gateway.GatewayError, model.ModelError,
            acceptance.AcceptanceError, OSError, SystemExit) as exc:
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
    """Return edition-scoped acceptance contexts.

    Each context binds shared control inputs plus only that edition's declared
    fixtures.  Bundle composition verifies agreement and locks their union.
    """
    contexts = {}
    for edition_id in cfg.get("editions", []):
        contexts[edition_id] = acceptance.acceptance_context(
            ROOT, (edition_id,),
            release_profile=cfg.get("releaseProfile"))
    return contexts


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


def _current_bundle_plan_state(command):
    """Derive the one current bundle proposal through a read-only command.

    ``bundle-plan`` and ``verify-current`` share this boundary so status
    verification cannot quietly implement a weaker release-chain resolver.
    """
    planes = load_planes()
    boot = gateway.ContentGateway(ROOT)
    cfg = canon.parse_json(boot.read_text(BUNDLE_CONFIG))
    records = gateway.VerificationGateway(RECORDS, command, planes)
    artifacts = gateway.ArtifactGateway(DIST, command, planes)
    manifest, manifest_bytes, manifest_wording = bundle_manifest_input(boot)
    bundlezip.validate_bundle_config(
        cfg, expected_edition_count=DELIVERY_EDITION_COUNT)
    attestation_policy, current_attestation_sides = \
        bundle_attestation_context(cfg)
    acceptance_contexts = bundle_acceptance_context(cfg)
    bindings = current_release_bindings(cfg)
    qa_authorization_contexts = bundle_qa_authorization_context(
        cfg, bindings)
    release_records = records.read_all("release-record")
    qa_records = records.read_all("qa-record")
    attestations = records.read_all("attestation")
    proposed = _propose_current_bundle_config(
        cfg, release_records, qa_records, attestations, artifacts.read,
        manifest_bytes, manifest_wording, attestation_policy,
        current_attestation_sides, acceptance_contexts, bindings,
        qa_authorization_contexts)
    return {
        "planes": planes,
        "content": boot,
        "config": cfg,
        "recordsGateway": records,
        "artifactGateway": artifacts,
        "manifest": manifest,
        "manifestBytes": manifest_bytes,
        "manifestWording": manifest_wording,
        "attestationPolicy": attestation_policy,
        "currentAttestationSides": current_attestation_sides,
        "acceptanceContexts": acceptance_contexts,
        "bindings": bindings,
        "qaAuthorizationContexts": qa_authorization_contexts,
        "releaseRecords": release_records,
        "qaRecords": qa_records,
        "attestations": attestations,
        "proposed": proposed,
    }


def cmd_bundle_plan(argv):
    """Print a verified proposed bundle config; never write source/evidence."""
    try:
        state = _current_bundle_plan_state("bundle-plan")
    except (bundlezip.BundleError, gateway.GatewayError, model.ModelError,
            acceptance.AcceptanceError, OSError, SystemExit) as exc:
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
        acceptance_contexts = bundle_acceptance_context(cfg)
        bundle_receipt_context = acceptance.combine_acceptance_contexts(
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
            bundle_manifest_input(boot)
        if fresh_cfg != cfg or fresh_manifest != manifest:
            raise bundlezip.BundleError(
                "bundle content inputs changed during promotion")
        fresh_release_records = vgw.read_all("release-record")
        fresh_qa_records = vgw.read_all("qa-record")
        fresh_attestations = vgw.read_all("attestation")
        fresh_policy, fresh_sides = bundle_attestation_context(fresh_cfg)
        fresh_contexts = bundle_acceptance_context(fresh_cfg)
        fresh_bundle_receipt_context = \
            acceptance.combine_acceptance_contexts(
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
            expected_edition_count=DELIVERY_EDITION_COUNT,
            current_acceptance_context=fresh_bundle_receipt_context)
        if record_problems:
            raise bundlezip.BundleError("; ".join(record_problems))
    except (bundlezip.BundleError, gateway.GatewayError, model.ModelError,
            acceptance.AcceptanceError, OSError, SystemExit) as exc:
        raise SystemExit("bundle refused after output readback: %s" % exc)

    digest, rname = vgw.append("bundle-record", record)
    print("bundle -> dist/%s\n  bundle-record %s" % (cfg["name"], digest))


def _pin_plan_problems(plan):
    """Return every stale authored value exposed by one pin plan."""
    problems = []
    edition_id = plan.get("edition", "unknown") \
        if isinstance(plan, dict) else "unknown"
    if not isinstance(plan, dict):
        return ["%s pin plan is not an object" % edition_id]
    problems.extend(
        "%s %s" % (edition_id, problem)
        for problem in canon.require_version(
            plan, "planVersion", pinplan.PLAN_VERSION))
    problems.extend(
        "%s pin plan schema: %s" % (edition_id, problem)
        for problem in schema_validate.validate(plan, _plan_schema()))
    corpora = plan.get("corpora")
    if not isinstance(corpora, dict):
        problems.append("%s pin plan has no corpus closure" % edition_id)
        return problems
    declared_corpora = {
        plan.get("claimCorpus"), plan.get("targetCorpus"),
        plan.get("authorityCorpus")}
    qa_sources = plan.get("qaSources")
    if isinstance(qa_sources, dict):
        declared_corpora.update(
            corpus_id for corpus_id in qa_sources.values()
            if corpus_id is not None)
    if set(corpora) != declared_corpora:
        problems.append(
            "%s pin plan corpus inventory is not exact" % edition_id)
    for corpus_id, closure in sorted(corpora.items()):
        problems.extend(pinplan.closure_problems(
            closure, "%s corpus %s" % (edition_id, corpus_id)))
    if plan.get("configuredCorpusVersion") != plan.get("documentVersion"):
        problems.append("%s corpus version is not the document version"
                        % edition_id)
    if plan.get("configuredEditionVersion") != plan.get("documentVersion"):
        problems.append("%s edition version is not the document version"
                        % edition_id)
    for field in ("censusCurrent", "groupsCurrent",
                  "dependenciesCurrent", "independentClaimsCurrent",
                  "artifactNameCurrent"):
        if plan.get(field) is not True:
            problems.append("%s %s is false" % (edition_id, field))
    return problems


def _walk_repository_files(start, excluded_directory_names=(),
                           excluded_repository_paths=()):
    """Return regular repository-relative files and symlink/non-file defects."""
    files = set()
    problems = []
    excluded_names = set(excluded_directory_names)
    excluded_paths = set(excluded_repository_paths)
    for directory, dirnames, filenames in os.walk(start, followlinks=False):
        kept = []
        for name in dirnames:
            path = os.path.join(directory, name)
            rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
            if name in excluded_names or rel in excluded_paths:
                continue
            if os.path.islink(path):
                problems.append("unclassified symlink directory %s" % rel)
                continue
            kept.append(name)
        dirnames[:] = kept
        for name in filenames:
            path = os.path.join(directory, name)
            rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
            if os.path.islink(path):
                problems.append("unclassified symlink file %s" % rel)
                continue
            if not os.path.isfile(path):
                problems.append("unclassified non-regular path %s" % rel)
                continue
            files.add(rel)
    return files, problems


def _classified_navigator_source_problems(content, edition_ids):
    """Close the nonterminal navigator tree over executable declarations."""
    expected = {
        "navigator/RUNBOOK-content-sync-and-regeneration.md",
        "navigator/build.py",
        BUNDLE_CONFIG,
        BUNDLE_MANIFEST_RESOURCE,
        "navigator/schema/acceptance.json",
        "navigator/schema/plan.schema.json",
        "navigator/tools/pre-commit-check.sh",
    }
    expected.update(control_inventory.CONTROL_SOURCE_PATHS)
    for edition_id in edition_ids:
        path = edition_path(edition_id)
        edition = canon.parse_json(content.read_text(path))
        expected.add(path)
        expected.update(edition["declaredTransitiveInputs"])
        qa_path = edition["qaRegistry"]
        qa_registry = canon.parse_json(content.read_text(qa_path))
        expected.add(qa_path)
        for entry in qa_registry["corpora"].values():
            expected.update(entry["files"])
    acceptance = canon.parse_json(content.read_text(
        "navigator/schema/acceptance.json"))
    runner = acceptance["runner"]
    expected.update(entry["path"] for entry in runner["testModules"])
    expected.update(entry["path"] for entry in runner["fixtures"])
    expected.update(runner["supportFiles"])

    actual, problems = _walk_repository_files(
        os.path.join(ROOT, "navigator"),
        excluded_directory_names=("__pycache__",),
        excluded_repository_paths=("navigator/dist", "navigator/records"))
    # Every conventional discovery test is executable by verify-current and
    # therefore classified even when it is outside the release callback set.
    expected.update(
        path for path in actual
        if path.startswith("navigator/tests/test_") and
        path.endswith(".py"))
    expected = {path for path in expected if path.startswith("navigator/")}
    extras = sorted(actual - expected)
    missing = sorted(expected - actual)
    if extras:
        problems.append("unclassified navigator files: %s" % extras)
    if missing:
        problems.append("declared navigator files are missing: %s" % missing)
    return problems


def _live_version_problems(content, current_versions):
    """Reject obsolete NA/AF version tokens in every live textual source."""
    files, problems = _walk_repository_files(
        ROOT, excluded_directory_names=(".git", "__pycache__"),
        excluded_repository_paths=("navigator/dist", "navigator/records"))
    seen_current = set()
    for path in sorted(files):
        frozen_migration = path.startswith(
            "navigator/tests/fixtures/migration_") and path.endswith(
                "_snapshot.json")
        if frozen_migration or os.path.splitext(path)[1].lower() not in \
                LIVE_TEXT_SUFFIXES:
            continue
        try:
            text = content.read_text(path)
        except (OSError, UnicodeDecodeError, gateway.GatewayError) as exc:
            problems.append("live text %s is unreadable: %s" % (path, exc))
            continue
        for match in LIVE_VERSION_PATTERN.finditer(text):
            strategy = match.group("strategy")
            token = match.group(0)
            expected = current_versions.get(strategy)
            if token == expected:
                seen_current.add(strategy)
            else:
                problems.append(
                    "%s contains obsolete %s version %s (current %s)" %
                    (path, strategy, token, expected))
    for strategy in sorted(current_versions):
        if strategy not in seen_current:
            problems.append("current %s version is absent from live text"
                            % strategy)
    return problems


def _flat_inventory(root, label):
    """Return a flat regular-file inventory and structural defects."""
    if not os.path.isdir(root):
        return set(), ["%s directory is missing" % label]
    names = set()
    problems = []
    for name in sorted(os.listdir(root)):
        path = os.path.join(root, name)
        if os.path.islink(path) or not os.path.isfile(path):
            problems.append("%s contains non-regular entry %s" %
                            (label, name))
        else:
            names.add(name)
    return names, problems


def _exact_inventory_problems(actual, expected, label):
    problems = []
    extras = sorted(actual - expected)
    missing = sorted(expected - actual)
    if extras:
        problems.append("%s has unclassified/superseded files: %s" %
                        (label, extras))
    if missing:
        problems.append("%s is missing current files: %s" %
                        (label, missing))
    return problems


def _record_inventory_problems(records_by_kind):
    expected = set()
    problems = []
    for kind in VERIFICATION_RECORD_KINDS:
        for envelope in records_by_kind[kind]:
            digest = envelope["digest"].rsplit(":", 1)[1]
            expected.add("%s_%s.json" % (kind, digest))
            problems.extend(
                "%s: %s" % (envelope["digest"], problem)
                for problem in
                recordprovenance.current_record_format_problems(
                    kind, envelope.get("record")))
    actual, structural_problems = _flat_inventory(RECORDS, "records")
    problems.extend(structural_problems)
    problems.extend(_exact_inventory_problems(actual, expected, "records"))
    return problems


def _run_full_test_suite(root):
    """Run every discovered test in the supplied repository snapshot."""
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        with tempfile.TemporaryDirectory(
                prefix="aa11393-verify-pycache-") as pycache:
            result = subprocess.run(
                [sys.executable, "-B", "-X", "pycache_prefix=" + pycache,
                 "-m", "unittest", "discover", "-s", "navigator/tests",
                 "-p", "test_*.py"],
                cwd=root, capture_output=True, text=True, timeout=1800,
                env=environment)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError("full test suite could not complete: %s" % exc)
    output = "\n".join(
        part.strip() for part in (result.stdout, result.stderr)
        if part.strip())
    if result.returncode != 0:
        raise RuntimeError("full test suite failed: %s" %
                           (output[-8000:] or "no diagnostic"))
    ran = re.search(r"Ran [0-9]+ tests? in [^\n]+", output)
    return ran.group(0) if ran else "full discovered suite passed"


def _git_whitespace_problems():
    try:
        result = subprocess.run(
            ["git", "diff", "--check", "HEAD"], cwd=ROOT,
            capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ["git whitespace check could not complete: %s" % exc]
    if result.returncode:
        detail = "\n".join(
            part.strip() for part in (result.stdout, result.stderr)
            if part.strip())
        return ["git whitespace check failed: %s" %
                (detail[-4000:] or "no diagnostic")]
    return []


def _verify_current_closure():
    """Prove one exact live source/evidence/artifact closure or refuse."""
    content = gateway.ContentGateway(ROOT)
    edition_ids = delivery_edition_ids(content)
    pin_plans = {edition: current_pin_plan(edition)
                 for edition in edition_ids}
    problems = []
    for plan in pin_plans.values():
        problems.extend(_pin_plan_problems(plan))

    planes = load_planes()
    artifacts = gateway.ArtifactGateway(DIST, "verify-current", planes)
    candidate_state = {}
    expected_dist = set()
    current_versions = {}
    for edition_id in edition_ids:
        edition_model, html, lock = derive(edition_id, "candidate")
        name = "candidate_" + edition_model.edition["artifactName"]
        try:
            stored = artifacts.read("candidate", name)
        except (OSError, gateway.GatewayError) as exc:
            problems.append("%s current candidate is unavailable: %s" %
                            (edition_id, exc))
        else:
            if stored != html:
                problems.append("%s stored candidate bytes are stale"
                                % edition_id)
        expected_dist.add(name)
        candidate_state[edition_id] = {
            "version": edition_model.edition["claimSetVersion"],
            "candidate": name,
            "candidateDigest": canon.bytes_digest(html),
            "lockDigest": lock["lockDigest"],
        }
        current_versions[edition_model.edition["strategyPrefix"]] = \
            edition_model.edition["claimSetVersion"]

    problems.extend(_classified_navigator_source_problems(
        content, edition_ids))
    problems.extend(_live_version_problems(content, current_versions))
    problems.extend(_git_whitespace_problems())
    if problems:
        raise RuntimeError("; ".join(problems))

    state = _current_bundle_plan_state("verify-current")
    cfg = state["config"]
    if cfg["editions"] != list(edition_ids):
        raise RuntimeError(
            "bundle edition identities changed during verification")
    if state["proposed"] != cfg:
        raise RuntimeError(
            "bundle config is stale; apply the exact bundle-plan proposal")
    for edition_id, binding in state["bindings"].items():
        candidate = candidate_state[edition_id]
        if (binding["sealedDigest"], binding["lockDigest"]) != (
                candidate["candidateDigest"], candidate["lockDigest"]):
            raise RuntimeError(
                "%s bundle binding changed during verification" % edition_id)

    plan = bundlezip.resolve_bundle_members(
        cfg, state["releaseRecords"], state["qaRecords"],
        state["attestations"], state["artifactGateway"].read,
        state["manifestBytes"], state["manifestWording"],
        approval_evidence_problems, state["attestationPolicy"],
        state["currentAttestationSides"],
        expected_edition_count=DELIVERY_EDITION_COUNT,
        acceptance_context_by_edition=state["acceptanceContexts"],
        qa_authorization_context_by_edition=
            state["qaAuthorizationContexts"])
    expected_zip = bundlezip.build_zip(
        plan["members"], cfg["declaredTimestamp"])
    stored_zip = state["artifactGateway"].read("bundle", cfg["name"])
    if stored_zip != expected_zip or \
            bundlezip.read_zip_members(stored_zip) != plan["members"]:
        raise RuntimeError("stored bundle is not the deterministic current ZIP")
    bundle_digest = canon.bytes_digest(stored_zip)
    checksum_name = cfg["name"] + ".sha256"
    checksum = state["artifactGateway"].read(
        "bundle-checksum", checksum_name)
    bundlezip.verify_detached_checksum(
        checksum, cfg["name"], bundle_digest)
    manifest_member = next(
        member for member in cfg["members"]
        if member["kind"] == "bundle-manifest")
    if state["artifactGateway"].read(
            "bundle-manifest", manifest_member["name"]) != \
            state["manifestBytes"]:
        raise RuntimeError("stored bundle manifest bytes are stale")

    bundle_records = state["recordsGateway"].read_all("bundle-record")
    bundle_receipt_context = acceptance.combine_acceptance_contexts(
        state["acceptanceContexts"], cfg["editions"])
    current_bundle_records = [
        envelope for envelope in bundle_records
        if not bundlezip.bundle_record_problems(
            envelope["record"], cfg, bundle_digest,
            state["content"].read_log[BUNDLE_CONFIG],
            expected_edition_count=DELIVERY_EDITION_COUNT,
            current_acceptance_context=bundle_receipt_context)]
    if not current_bundle_records:
        raise RuntimeError("no current fully authorized bundle record")

    expected_dist.update(member["name"] for member in cfg["members"])
    expected_dist.update((cfg["name"], checksum_name))
    actual_dist, inventory_problems = _flat_inventory(DIST, "dist")
    inventory_problems.extend(_exact_inventory_problems(
        actual_dist, expected_dist, "dist"))
    records_by_kind = {
        "attestation": state["attestations"],
        "qa-record": state["qaRecords"],
        "release-record": state["releaseRecords"],
        "bundle-record": bundle_records,
    }
    inventory_problems.extend(_record_inventory_problems(records_by_kind))
    if inventory_problems:
        raise RuntimeError("; ".join(inventory_problems))

    return {
        "status": "current",
        "releaseProfile": cfg["releaseProfile"],
        "editions": candidate_state,
        "bundle": {
            "name": cfg["name"],
            "digest": bundle_digest,
            "record": min(current_bundle_records,
                          key=_approval_selection_key)["digest"],
        },
        "checks": {
            "pinPlans": "current",
            "liveVersions": "current-only",
            "navigatorSources": "classified",
            "distInventory": "exact",
            "recordInventory": "canonical",
            "deterministicBundle": "exact",
        },
    }


def verify_current_state(run_tests=True):
    """Prove the final state, with tests isolated from authoritative bytes.

    The complete repository is snapshotted before verification.  Discovered
    tests run only in a materialized copy and must leave that copy unchanged.
    The live closure is then re-derived and the live snapshot is compared
    again immediately before success is returned.  A passing test can
    therefore neither mutate nor stale an already-verified source, record, or
    artifact.
    """
    try:
        initial = snapshot.RepositorySnapshot.capture(ROOT)
    except snapshot.SnapshotError as exc:
        raise RuntimeError("cannot snapshot current repository: %s" % exc)
    _verify_current_closure()
    test_result = "not requested"
    if run_tests:
        try:
            with tempfile.TemporaryDirectory(
                    prefix="aa11393-verify-snapshot-") as sandbox_root:
                initial.materialize(sandbox_root)
                sandbox_before = snapshot.RepositorySnapshot.capture(
                    sandbox_root)
                test_result = _run_full_test_suite(sandbox_root)
                sandbox_after = snapshot.RepositorySnapshot.capture(
                    sandbox_root)
                mutations = sandbox_before.differences(sandbox_after)
                if mutations:
                    raise RuntimeError(
                        "discovered tests mutated the verified snapshot: %s" %
                        "; ".join(mutations))
        except snapshot.SnapshotError as exc:
            raise RuntimeError("isolated test snapshot failed: %s" % exc)

    before_final = snapshot.RepositorySnapshot.capture(ROOT)
    live_changes = initial.differences(before_final)
    if live_changes:
        raise RuntimeError(
            "live repository changed during verification: %s" %
            "; ".join(live_changes))
    report = _verify_current_closure()
    final = snapshot.RepositorySnapshot.capture(ROOT)
    live_changes = initial.differences(final)
    if live_changes:
        raise RuntimeError(
            "live repository changed before final-state certification: %s" %
            "; ".join(live_changes))
    report["checks"]["softwareTests"] = test_result
    report["checks"]["repositorySnapshot"] = final.digest
    return report


def cmd_verify_current(argv):
    try:
        report = verify_current_state(run_tests=True)
    except (bundlezip.BundleError, gateway.GatewayError, model.ModelError,
            acceptance.AcceptanceError, OSError, RuntimeError,
            snapshot.SnapshotError, SystemExit, KeyError, TypeError,
            ValueError) as exc:
        raise SystemExit("verify-current refused: %s" % exc)
    print(canon.canonical_json(report).decode("utf-8"))


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
        acceptance_contexts = bundle_acceptance_context(cfg)
        bundle_receipt_context = acceptance.combine_acceptance_contexts(
            acceptance_contexts, cfg["editions"])
    except (gateway.GatewayError, model.ModelError,
            acceptance.AcceptanceError, OSError, SystemExit) as exc:
        print("bundle: invalid edition policy (%s)" % exc)
        return
    release_bindings = {}
    qa_authorization_contexts = {}
    print("release profile: %s (%s)" % (
        cfg["releaseProfile"],
        acceptance_contexts[cfg["editions"][0]][
            "releaseProfileContract"]["compatibilityAuthorization"]))
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
        manual_qa = acceptance_contexts[ed][
            "releaseProfileContract"]["manualQaEvidence"]
        valid_qa = []
        if manual_qa == "required":
            valid_qa, _ = current_authorized_qa_records(
                m, cdig, lock, qa_records, attestations)
        qa_digest = valid_qa[0]["digest"] if valid_qa else None
        if manual_qa == "deferred":
            print("  qa-record: deferred by technical-preview (not required)")
        else:
            print("  qa-record: %s" % (
                qa_digest[:20] + "…" if qa_digest else
                "none with complete current authorized operator evidence"))

        valid_qa_digests = {record["digest"] for record in valid_qa}
        releases = []
        for envelope in release_records:
            record = envelope.get("record") if isinstance(envelope, dict) \
                else None
            if not isinstance(record, dict):
                continue
            if (record.get("edition"), record.get("sealed"),
                    record.get("sealedDigest"), record.get("lockDigest"),
                    record.get("declaredReleaseTimestamp"),
                    record.get("releaseProfile")) != (
                    ed, m.edition["artifactName"], cdig,
                    lock["lockDigest"],
                    m.edition["declaredReleaseTimestamp"],
                    cfg["releaseProfile"]):
                continue
            if manual_qa == "deferred" and \
                    record.get("qaRecord") is not None:
                continue
            if manual_qa == "required" and \
                    record.get("qaRecord") not in valid_qa_digests:
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
                model.ModelError, acceptance.AcceptanceError, OSError,
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
            "usage: build.py preview|candidate|migrate|pin-plan|record-qa|release "
            "<edition> | attest <type> [edition] | bundle-plan | bundle | "
            "status | verify-current")
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
    elif cmd == "propose-reuse":
        raise SystemExit("propose-reuse is deferred (TDD §10.7)")
    else:
        raise SystemExit("unknown command %r" % cmd)


if __name__ == "__main__":
    main(sys.argv[1:])
