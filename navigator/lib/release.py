"""Release lifecycle — promotion by verification (TDD §10.8, §10.10, §13).

candidate -> profile-governed promotion.  A validated release requires manual
QA against those exact bytes; a technical preview binds the explicit deferred
observation contract and makes no compatibility authorization claim.  Both
profiles re-derive and byte-compare the candidate, verify the content-input
lock and current attestations, and seal the same bytes with a checksum and an
append-only release record.
"""

import copy
import io
import importlib
import locale
import os
import platform
import subprocess
import sys
import tempfile
import unittest

from . import canon, gateway, projections


class AcceptanceError(ValueError):
    """An executable acceptance phase failed or its evidence drifted."""


_ACCEPTANCE_IDS = tuple("AC-%02d" % number for number in range(1, 21))
_RELEASE_PREFLIGHT_IDS = _ACCEPTANCE_IDS[:-1]
_RECEIPT_FIELDS = frozenset((
    "receiptVersion", "registryDigest", "runnerDigest", "runnerInputs",
    "runnerEditions", "runnerKind", "releaseProfile",
    "releaseProfileContract", "results", "subjects",
))
_RUNNER_INPUT_FIELDS = frozenset(("path", "digest"))
_REGISTRY_FIELDS = frozenset((
    "acceptanceVersion", "comment", "receiptPhases", "runner", "criteria",
))
_CRITERION_FIELDS = frozenset((
    "id", "applicability", "text", "enforcedBy",
))
_RUNNER_FIELDS = frozenset((
    "runnerVersion", "manualQaEvidenceVersion", "activeReleaseProfile",
    "releaseProfiles", "editions", "testModules", "fixtures",
    "testScopes", "supportFiles",
))
_RELEASE_PROFILE_FIELDS = frozenset((
    "id", "manualQaEvidence", "compatibilityAuthorization",
    "deferredObservations", "requiredQaRecordFields", "artifactLabel",
))
_RELEASE_PROFILE_IDS = ("technical-preview", "validated-release")
_MANUAL_QA_FIELDS = ("ac11", "ac12", "ac13", "ac15")
_PROFILE_SEMANTICS = {
    "technical-preview": {
        "manualQaEvidence": "deferred",
        "compatibilityAuthorization": "not-authorized",
        "deferredObservations": ["AC-11", "AC-12", "AC-13", "AC-15"],
        "requiredQaRecordFields": [],
        "artifactLabel": (
            "TECHNICAL PREVIEW — Manual cross-platform and "
            "assistive-technology QA is deferred; browser and "
            "assistive-technology compatibility is not validated."),
    },
    "validated-release": {
        "manualQaEvidence": "required",
        "compatibilityAuthorization": "support-matrix-authorized",
        "deferredObservations": [],
        "requiredQaRecordFields": list(_MANUAL_QA_FIELDS),
        "artifactLabel": (
            "VALIDATED-RELEASE PROFILE — Delivery requires current full "
            "seven-row cross-platform and assistive-technology QA."),
    },
}
_TEST_MODULE_FIELDS = frozenset(("module", "path"))
_FIXTURE_FIELDS = frozenset(("path", "editions"))
_TEST_SCOPE_FIELDS = frozenset(("test", "editions"))
_RESULT_FIELDS = frozenset(("phase", "criteria", "status"))
_RELEASE_SUBJECT_FIELDS = frozenset((
    "edition", "candidateDigest", "contentLockDigest", "qaRecord",
    "qaInputLockDigest", "releaseProfile", "compatibilityAuthorization",
    "deferredObservations", "artifactLabel",
))
_BUNDLE_SUBJECT_FIELDS = frozenset((
    "bundleConfigDigest", "bundleDigest", "releaseRecords", "members",
    "manifestApproval", "releaseProfile", "compatibilityAuthorization",
    "deferredObservations", "artifactLabel",
))

# The registry is data, so it cannot be the authority for whether its own
# executable inventory is complete.  These field-specific c1 lock
# commitments live in an edition-blind builder module covered by every
# content lock.  They bind exact values without teaching the shared kernel
# any edition name or edition-specific path.  An intentional runner change
# therefore requires code + registry review; deletion or wholesale callback
# redirection cannot shrink the evidence lock silently.
_EXECUTABLE_FLOOR_DIGESTS = {
    "supported editions":
        "sha256/c1:00d4f2ec45c5c78449e81fc84fc413befa3feb8c1bb4b8a2dbf1e44c900c927b",
    "test modules":
        "sha256/c1:104d57a52b8caa6fed711933181ea2116e03c1d455cd8d5a7fb00f8ebd419429",
    "fixtures":
        "sha256/c1:a8d9017494752934cb7fdee08e55353128df8c0ebdc58f4554d84a130b6c3262",
    "test scopes":
        "sha256/c1:50fc947b461eec7eff4395a9be60b154f20463834504a2053029b5c464f99786",
    "support files":
        "sha256/c1:1921d431ddad8f569963232f3a8af70a4320233d250aacd97ead40c583fb6d69",
    "criterion enforcement":
        "sha256/c1:98358b743aade21520cbfc27782061f8166f1b245023075a275fbeef7a760e79",
    "release profiles":
        "sha256/c1:e24c7708bcd272b3fe53f9aa5bb9f76ba3b75937d1d1e9e6013f96bddafbda7f",
}


def expected_release_profile_contract(profile_id):
    """Return the code-locked exact contract for one known profile id."""
    if profile_id not in _RELEASE_PROFILE_IDS:
        raise AcceptanceError("unknown release profile %r" % profile_id)
    return {
        "id": profile_id,
        **copy.deepcopy(_PROFILE_SEMANTICS[profile_id]),
    }


def _receipt_results(kind, receipt_phases):
    phase_names = (("release-preflight", "release-postcondition")
                   if kind == "release" else ("bundle-postcondition",))
    return [
        {"phase": phase, "criteria": list(receipt_phases[phase]),
         "status": "passed"}
        for phase in phase_names
    ]


def _receipt_plans():
    return {
        "release-preflight": list(_RELEASE_PREFLIGHT_IDS),
        "release-postcondition": ["AC-16"],
        "bundle-postcondition": ["AC-20"],
    }


def _release_profile_entry_problems(contract):
    """Return defects in one closed release-profile contract."""
    if not isinstance(contract, dict) or set(contract) != \
            _RELEASE_PROFILE_FIELDS:
        return ["release profile has the wrong fields"]
    profile_id = contract.get("id")
    if profile_id not in _RELEASE_PROFILE_IDS:
        return ["release profile has unknown id %r" % profile_id]
    problems = []
    expected = expected_release_profile_contract(profile_id)
    for field in ("manualQaEvidence", "compatibilityAuthorization",
                  "deferredObservations", "requiredQaRecordFields",
                  "artifactLabel"):
        if contract.get(field) != expected[field]:
            problems.append(
                "%s release profile %s must be exactly %r" %
                (profile_id, field, expected[field]))
    label = contract.get("artifactLabel")
    if not isinstance(label, str) or not label or label.strip() != label or \
            canon.normalize_nfc(label) != label or \
            any(ord(character) < 32 or ord(character) == 127
                for character in label):
        problems.append(
            "%s release profile artifactLabel is not canonical visible text"
            % profile_id)
    return problems


def _release_profiles_problems(runner):
    """Return structural and semantic defects in the ordered profile set."""
    if not isinstance(runner, dict):
        return ["acceptance runner is unavailable for release profiles"]
    profiles = runner.get("releaseProfiles")
    if not isinstance(profiles, list):
        return ["releaseProfiles is not an ordered array"]
    ids = [profile.get("id") if isinstance(profile, dict) else None
           for profile in profiles]
    problems = []
    if ids != list(_RELEASE_PROFILE_IDS):
        problems.append(
            "releaseProfiles must contain exactly %s in order" %
            list(_RELEASE_PROFILE_IDS))
    for index, profile in enumerate(profiles):
        problems.extend(
            "releaseProfiles[%d]: %s" % (index, problem)
            for problem in _release_profile_entry_problems(profile))
    active = runner.get("activeReleaseProfile")
    if active not in _RELEASE_PROFILE_IDS:
        problems.append(
            "activeReleaseProfile must name one declared release profile")
    return problems


def release_profile_contract(registry, release_profile=None):
    """Return the active profile id and an isolated exact contract copy.

    An explicit selection is an assertion about the live governance mode, not
    a caller-controlled downgrade.  It must therefore equal the registry's
    active profile.  Changing modes requires an intentional registry and
    executable-floor update.
    """
    registry = _validate_registry(registry)
    runner = registry["runner"]
    active = runner["activeReleaseProfile"]
    if release_profile is not None and release_profile != active:
        raise AcceptanceError(
            "release profile %r is not the active release profile %r" %
            (release_profile, active))
    selected = active if release_profile is None else release_profile
    contract = next(profile for profile in runner["releaseProfiles"]
                    if profile["id"] == selected)
    return selected, copy.deepcopy(contract)


def profile_record_fields(contract):
    """Project one validated profile into release/bundle record fields."""
    problems = _release_profile_entry_problems(contract)
    if problems:
        raise AcceptanceError("release profile contract is malformed: %s"
                              % "; ".join(problems))
    return {
        "releaseProfile": contract["id"],
        "compatibilityAuthorization":
            contract["compatibilityAuthorization"],
        "deferredObservations": copy.deepcopy(
            contract["deferredObservations"]),
        "artifactLabel": contract["artifactLabel"],
    }


def _runner_digest(registry_digest, runner_inputs, receipt_phases,
                   runner_editions, release_profile,
                   release_profile_contract):
    return canon.composite_digest(
        "aa11393:lock:c1", {
            "runnerVersion": "2",
            "runnerEditions": runner_editions,
            "registryDigest": registry_digest,
            "runnerInputs": runner_inputs,
            "plans": receipt_phases,
            "releaseProfile": release_profile,
            "releaseProfileContract": release_profile_contract,
    })


def _registry_floor_problems(value):
    """Return drift from the code-locked executable acceptance floor."""
    if not isinstance(value, dict) or not isinstance(value.get("runner"), dict):
        return ["runner is unavailable for executable-floor comparison"]
    runner = value["runner"]
    try:
        fields = {
            "supported editions": runner.get("editions"),
            "test modules": runner.get("testModules"),
            "fixtures": runner.get("fixtures"),
            "test scopes": runner.get("testScopes"),
            "support files": runner.get("supportFiles"),
            "criterion enforcement": {
                "manualQaEvidenceVersion": runner.get(
                    "manualQaEvidenceVersion"),
                "criteria": [{
                    "id": criterion.get("id"),
                    "tests": criterion.get("enforcedBy", {}).get("tests"),
                    "qaRecordFields": criterion.get("enforcedBy", {}).get(
                        "qaRecordFields"),
                } for criterion in value.get("criteria", ())],
            },
            "release profiles": {
                "activeReleaseProfile": runner.get(
                    "activeReleaseProfile"),
                "releaseProfiles": runner.get("releaseProfiles"),
            },
        }
    except (AttributeError, TypeError):
        return ["runner inventory is malformed for executable-floor comparison"]
    problems = []
    for label, field_value in fields.items():
        try:
            actual = canon.composite_digest(
                "aa11393:lock:c1", {"floor": label, "value": field_value})
        except (canon.CanonError, TypeError, ValueError):
            problems.append(
                "%s are malformed for executable-floor comparison" % label)
            continue
        if actual != _EXECUTABLE_FLOOR_DIGESTS[label]:
            problems.append("%s differ from the locked executable floor" % label)
    return problems


def _validate_registry(value):
    """Validate the closed acceptance plan and its data-declared runner."""
    criteria = value.get("criteria") if isinstance(value, dict) else None
    if not isinstance(value, dict) or set(value) != _REGISTRY_FIELDS or \
            value.get("acceptanceVersion") != "2" or \
            not isinstance(value.get("comment"), str) or \
            not value.get("comment", "").strip():
        raise AcceptanceError(
            "acceptance registry top-level shape/version is not closed")
    if value.get("receiptPhases") != \
            _receipt_plans():
        raise AcceptanceError(
            "acceptance registry receiptPhases is not the exact closed plan")
    if not isinstance(criteria, list) or \
            tuple(item.get("id") for item in criteria
                  if isinstance(item, dict)) != _ACCEPTANCE_IDS or \
            len(criteria) != len(_ACCEPTANCE_IDS):
        raise AcceptanceError("acceptance registry criterion set is not closed")

    expected_applicability = {
        **{criterion_id: "edition" for criterion_id in _ACCEPTANCE_IDS[:18]},
        "AC-19": "shared", "AC-20": "bundle",
    }
    for criterion in criteria:
        if set(criterion) != _CRITERION_FIELDS or \
                criterion.get("applicability") != expected_applicability[
                    criterion["id"]] or \
                not isinstance(criterion.get("text"), str) or \
                not criterion.get("text", "").strip():
            raise AcceptanceError(
                "%s criterion shape/applicability/text is malformed"
                % criterion["id"])

    runner = value.get("runner")
    if not isinstance(runner, dict) or set(runner) != _RUNNER_FIELDS or \
            runner.get("runnerVersion") != "2" or \
            runner.get("manualQaEvidenceVersion") != "3":
        raise AcceptanceError("acceptance registry runner is malformed")
    profile_problems = _release_profiles_problems(runner)
    if profile_problems:
        raise AcceptanceError(
            "acceptance registry release profiles are malformed: %s" %
            "; ".join(profile_problems))
    editions = runner.get("editions")
    if not isinstance(editions, list) or not editions or \
            editions != sorted(editions) or \
            len(editions) != len(set(editions)) or \
            not all(isinstance(edition, str) and edition.isidentifier()
                    for edition in editions):
        raise AcceptanceError(
            "acceptance registry editions are not an exact sorted set")
    declared_editions = set(editions)
    modules = runner.get("testModules")
    if not isinstance(modules, list) or not modules:
        raise AcceptanceError("acceptance registry declares no test modules")
    module_names = []
    module_paths = []
    for entry in modules:
        if not isinstance(entry, dict) or set(entry) != _TEST_MODULE_FIELDS or \
                not isinstance(entry.get("module"), str) or \
                not entry.get("module", "").isidentifier() or \
                not isinstance(entry.get("path"), str) or \
                not entry.get("path") or os.path.isabs(entry["path"]) or \
                ".." in entry["path"].split("/") or \
                not entry["path"].endswith(".py"):
            raise AcceptanceError(
                "acceptance registry test module declaration is malformed")
        module_names.append(entry["module"])
        module_paths.append(entry["path"])
    if module_names != sorted(module_names) or \
            len(module_names) != len(set(module_names)) or \
            module_paths != sorted(module_paths) or \
            len(module_paths) != len(set(module_paths)):
        raise AcceptanceError(
            "acceptance registry test modules are not exact sorted sets")

    declared_modules = set(module_names)
    referenced_modules = set()
    registered_tests = set()
    declared_qa_fields = []
    for criterion in criteria:
        enforced = criterion.get("enforcedBy")
        if not isinstance(enforced, dict) or set(enforced) != {
                "tests", "qaRecordFields"}:
            raise AcceptanceError(
                "%s has a malformed enforcement map" % criterion["id"])
        qa_fields = enforced.get("qaRecordFields")
        if not isinstance(qa_fields, list) or \
                len(qa_fields) != len(set(qa_fields)) or \
                not all(isinstance(field, str) and field
                        for field in qa_fields):
            raise AcceptanceError(
                "%s has malformed QA-record fields" % criterion["id"])
        declared_qa_fields.extend(qa_fields)
        tests = enforced.get("tests")
        if not isinstance(tests, list) or not tests or \
                len(tests) != len(set(tests)):
            raise AcceptanceError(
                "%s has no exact executable callback set" % criterion["id"])
        for registered in tests:
            if not isinstance(registered, str) or \
                    len(registered.split(".")) != 3:
                raise AcceptanceError(
                    "%s has a malformed callback name" % criterion["id"])
            module_name, class_name, method_name = registered.split(".")
            if not class_name.isidentifier() or \
                    not method_name.isidentifier() or \
                    not method_name.startswith("test_") or \
                    module_name not in declared_modules:
                raise AcceptanceError(
                    "%s callback %r is not declared by the runner" %
                    (criterion["id"], registered))
            expected_prefix = "test_%s_" % criterion["id"].lower().replace(
                "-", "")
            if module_name == "test_acceptance" and (
                    class_name != "Acceptance" or
                    not method_name.startswith(expected_prefix)):
                raise AcceptanceError(
                    "%s callback %r does not match its criterion identity" %
                    (criterion["id"], registered))
            if module_name == "test_canon" and criterion["id"] != "AC-07":
                raise AcceptanceError(
                    "%s may not own canonicalization callback %r" %
                    (criterion["id"], registered))
            if registered in registered_tests:
                raise AcceptanceError(
                    "acceptance callback %r is owned by more than one criterion"
                    % registered)
            referenced_modules.add(module_name)
            registered_tests.add(registered)
    if tuple(declared_qa_fields) != _MANUAL_QA_FIELDS:
        raise AcceptanceError(
            "validated-release QA-record fields do not match the exact "
            "criterion enforcement order")
    if referenced_modules != declared_modules:
        raise AcceptanceError(
            "acceptance registry test modules and callbacks do not close")

    fixtures = runner.get("fixtures")
    if not isinstance(fixtures, list) or not fixtures:
        raise AcceptanceError("acceptance registry declares no fixtures")
    fixture_paths = []
    for entry in fixtures:
        if not isinstance(entry, dict) or set(entry) != _FIXTURE_FIELDS:
            raise AcceptanceError(
                "acceptance registry fixture declaration is malformed")
        path = entry.get("path")
        scopes = entry.get("editions")
        if not isinstance(path, str) or not path or os.path.isabs(path) or \
                ".." in path.split("/") or \
                not isinstance(scopes, list) or scopes != sorted(scopes) or \
                len(scopes) != len(set(scopes)) or \
                not set(scopes).issubset(declared_editions):
            raise AcceptanceError(
                "acceptance registry fixture scope is malformed")
        fixture_paths.append(path)
    if fixture_paths != sorted(fixture_paths) or \
            len(fixture_paths) != len(set(fixture_paths)):
        raise AcceptanceError(
            "acceptance registry fixtures are not an exact sorted path set")

    test_scopes = runner.get("testScopes")
    if not isinstance(test_scopes, list):
        raise AcceptanceError("acceptance registry testScopes is malformed")
    scoped_tests = []
    for entry in test_scopes:
        if not isinstance(entry, dict) or set(entry) != _TEST_SCOPE_FIELDS or \
                entry.get("test") not in registered_tests or \
                not isinstance(entry.get("editions"), list) or \
                not entry["editions"] or \
                entry["editions"] != sorted(entry["editions"]) or \
                len(entry["editions"]) != len(set(entry["editions"])) or \
                not set(entry["editions"]).issubset(declared_editions):
            raise AcceptanceError(
                "acceptance registry test scope is malformed")
        scoped_tests.append(entry["test"])
    if scoped_tests != sorted(scoped_tests) or \
            len(scoped_tests) != len(set(scoped_tests)):
        raise AcceptanceError(
            "acceptance registry testScopes is not an exact sorted set")

    paths = runner.get("supportFiles")
    if not isinstance(paths, list) or not paths or \
            paths != sorted(paths) or len(paths) != len(set(paths)) or \
            not all(isinstance(path, str) and path and
                    not os.path.isabs(path) and ".." not in path.split("/")
                    for path in paths):
        raise AcceptanceError(
            "acceptance registry supportFiles is not an exact sorted path set")
    floor_problems = _registry_floor_problems(value)
    if floor_problems:
        raise AcceptanceError(
            "acceptance registry violates the locked executable floor: %s" %
            "; ".join(floor_problems))
    return value


def _runner_editions(registry, editions):
    if not isinstance(editions, (list, tuple)) or not editions or \
            not all(isinstance(edition, str) and edition for edition in editions):
        raise AcceptanceError(
            "acceptance runner editions are missing or malformed")
    selected = tuple(sorted(editions))
    if len(selected) != len(set(selected)) or \
            not set(selected).issubset(registry["runner"]["editions"]):
        raise AcceptanceError(
            "acceptance runner editions are not a declared exact set")
    return selected


def _runner_input_paths(registry, declared_inputs, runner_editions):
    """Return the closed implementation/test-input set for the live runner.

    The edition lock already declares the complete shared builder tree.  The
    registry declares the executable acceptance modules, fixtures, and support
    files they consume.  Artifact outputs and verification records are
    deliberately absent: receipts bind those through typed subjects instead.
    """
    if not isinstance(declared_inputs, (list, tuple)) or \
            not all(isinstance(path, str) and path for path in declared_inputs):
        raise AcceptanceError("declared acceptance inputs are malformed")
    runner = registry["runner"]
    try:
        builder = set(projections.builder_source_paths(declared_inputs))
    except ValueError as exc:
        raise AcceptanceError(
            "acceptance builder source inventory is invalid: %s" % exc)
    test_modules = {entry["path"] for entry in runner["testModules"]}
    selected = set(runner_editions)
    fixtures = {
        entry["path"] for entry in runner["fixtures"]
        if not entry["editions"] or selected.intersection(entry["editions"])
    }
    return tuple(sorted(
        builder | test_modules | fixtures |
        set(runner["supportFiles"])))


def acceptance_context(root, declared_inputs, editions,
                       release_profile=None):
    """Snapshot the exact live registry and executable runner inputs.

    This context is computed before and after each promotion transaction.  A
    receipt is emitted only if both snapshots are identical, preventing a
    phase from being attributed to implementation bytes that changed while it
    ran.
    """
    content = gateway.ContentGateway(root)
    registry_path = "navigator/schema/acceptance.json"
    registry_bytes = content.read_bytes(registry_path)
    registry_digest = canon.bytes_digest(registry_bytes)
    registry = canon.parse_json(registry_bytes)
    selected_profile, profile_contract = release_profile_contract(
        registry, release_profile)
    runner_editions = _runner_editions(registry, editions)
    reads = []
    for path in _runner_input_paths(
            registry, declared_inputs, runner_editions):
        reads.append({"path": path,
                      "digest": canon.bytes_digest(content.read_bytes(path))})
    plans = registry["receiptPhases"]
    runner_digest = _runner_digest(
        registry_digest, reads, plans, list(runner_editions),
        selected_profile, profile_contract)
    return {
        "registryDigest": registry_digest,
        "runnerDigest": runner_digest,
        "runnerEditions": list(runner_editions),
        "runnerInputs": reads,
        "receiptPhases": plans,
        "releaseProfile": selected_profile,
        "releaseProfileContract": profile_contract,
    }


def combine_acceptance_contexts(context_by_edition, editions):
    """Derive the bundle runner context from exact standalone contexts.

    This is an independent composition of the already-read edition contexts:
    shared inputs must agree byte-for-byte, edition-only inputs are unioned,
    and the resulting digest explicitly binds every configured edition.
    """
    if not isinstance(editions, (list, tuple)) or not editions or \
            not all(isinstance(edition, str) and edition for edition in editions):
        raise AcceptanceError(
            "bundle acceptance runner editions are missing or malformed")
    runner_editions = tuple(sorted(editions))
    if len(runner_editions) != len(set(runner_editions)) or \
            not isinstance(context_by_edition, dict) or \
            set(context_by_edition) != set(runner_editions):
        raise AcceptanceError(
            "bundle acceptance contexts do not match configured editions")

    registry_digest = None
    receipt_phases = None
    release_profile = None
    release_profile_contract_value = None
    inputs_by_path = {}
    for edition in runner_editions:
        context = context_by_edition[edition]
        problems = _context_problems(context)
        if problems or context.get("runnerEditions") != [edition]:
            raise AcceptanceError(
                "standalone acceptance context for %s is malformed: %s" %
                (edition, "; ".join(problems) if problems else
                 "runner edition mismatch"))
        if registry_digest is None:
            registry_digest = context["registryDigest"]
            receipt_phases = context["receiptPhases"]
            release_profile = context["releaseProfile"]
            release_profile_contract_value = context[
                "releaseProfileContract"]
        elif context["registryDigest"] != registry_digest or \
                context["receiptPhases"] != receipt_phases or \
                context["releaseProfile"] != release_profile or \
                context["releaseProfileContract"] != \
                release_profile_contract_value:
            raise AcceptanceError(
                "standalone acceptance contexts do not share one registry "
                "and release profile")
        for entry in context["runnerInputs"]:
            path = entry["path"]
            previous = inputs_by_path.get(path)
            if previous is not None and previous != entry["digest"]:
                raise AcceptanceError(
                    "standalone acceptance contexts disagree on %s" % path)
            inputs_by_path[path] = entry["digest"]

    runner_inputs = [
        {"path": path, "digest": inputs_by_path[path]}
        for path in sorted(inputs_by_path)
    ]
    combined = {
        "registryDigest": registry_digest,
        "runnerDigest": _runner_digest(
            registry_digest, runner_inputs, receipt_phases,
            list(runner_editions), release_profile,
            release_profile_contract_value),
        "runnerEditions": list(runner_editions),
        "runnerInputs": runner_inputs,
        "receiptPhases": receipt_phases,
        "releaseProfile": release_profile,
        "releaseProfileContract": copy.deepcopy(
            release_profile_contract_value),
    }
    problems = _context_problems(combined)
    if problems:
        raise AcceptanceError(
            "combined bundle acceptance context is malformed: %s" %
            "; ".join(problems))
    return combined


def _digest_problem(value, label):
    try:
        canon.parse_digest(value)
    except (canon.CanonError, TypeError, ValueError) as exc:
        return ["%s is not a canonical digest: %s" % (label, exc)]
    return []


def _context_problems(context):
    if not isinstance(context, dict) or set(context) != {
            "registryDigest", "runnerDigest", "runnerInputs",
            "runnerEditions", "receiptPhases", "releaseProfile",
            "releaseProfileContract"}:
        return ["current acceptance context is unavailable or malformed"]
    problems = []
    problems.extend(_digest_problem(context.get("registryDigest"),
                                    "current acceptance registry digest"))
    problems.extend(_digest_problem(context.get("runnerDigest"),
                                    "current acceptance runner digest"))
    profile_contract = context.get("releaseProfileContract")
    profile_problems = _release_profile_entry_problems(profile_contract)
    problems.extend(
        "current acceptance release profile: %s" % problem
        for problem in profile_problems)
    if not profile_problems and context.get("releaseProfile") != \
            profile_contract.get("id"):
        problems.append(
            "current acceptance releaseProfile does not match its contract")
    runner_editions = context.get("runnerEditions")
    if not isinstance(runner_editions, list) or not runner_editions or \
            runner_editions != sorted(runner_editions) or \
            len(runner_editions) != len(set(runner_editions)) or \
            not all(isinstance(edition, str) and edition
                    for edition in runner_editions):
        problems.append(
            "current acceptance runner editions are not an exact sorted set")
    if context.get("receiptPhases") != _receipt_plans():
        problems.append("current acceptance receipt phases are not the exact "
                        "closed plan")
    reads = context.get("runnerInputs")
    if not isinstance(reads, list) or not reads:
        problems.append("current acceptance runner inputs are empty")
    else:
        paths = []
        for index, entry in enumerate(reads):
            if not isinstance(entry, dict) or set(entry) != _RUNNER_INPUT_FIELDS:
                problems.append("current acceptance runner input %d is malformed"
                                % index)
                continue
            path = entry.get("path")
            if not isinstance(path, str) or not path:
                problems.append("current acceptance runner input %d has no path"
                                % index)
            else:
                paths.append(path)
            problems.extend(_digest_problem(
                entry.get("digest"),
                "current acceptance runner input %d digest" % index))
        if paths != sorted(paths) or len(paths) != len(set(paths)):
            problems.append("current acceptance runner inputs are not an exact "
                            "sorted set")
    try:
        expected_runner_digest = _runner_digest(
            context.get("registryDigest"), context.get("runnerInputs"),
            context.get("receiptPhases"), context.get("runnerEditions"),
            context.get("releaseProfile"),
            context.get("releaseProfileContract"))
        if context.get("runnerDigest") != expected_runner_digest:
            problems.append("current acceptance runner digest does not derive "
                            "from its exact inputs and phase plan")
    except (canon.CanonError, TypeError, ValueError) as exc:
        problems.append("current acceptance runner digest cannot be derived: %s"
                        % exc)
    return problems


def _subject_problems(kind, subjects, label, release_profile_contract=None):
    expected_fields = (_RELEASE_SUBJECT_FIELDS if kind == "release"
                       else _BUNDLE_SUBJECT_FIELDS)
    if not isinstance(subjects, dict) or set(subjects) != expected_fields:
        return ["%s subjects have the wrong fields" % label]
    problems = []
    try:
        expected_profile_fields = profile_record_fields(
            release_profile_contract)
    except AcceptanceError as exc:
        problems.append("%s release profile contract is malformed: %s"
                        % (label, exc))
        expected_profile_fields = None
    if expected_profile_fields is not None:
        for field, expected in expected_profile_fields.items():
            if subjects.get(field) != expected:
                problems.append(
                    "%s %s does not match the current release profile" %
                    (label, field))
    if kind == "release":
        if not isinstance(subjects.get("edition"), str) or \
                not subjects.get("edition", "").strip():
            problems.append("%s edition is not a non-empty string" % label)
        for field in ("candidateDigest", "contentLockDigest"):
            problems.extend(_digest_problem(
                subjects.get(field), "%s %s" % (label, field)))
        manual_qa = release_profile_contract.get("manualQaEvidence") \
            if isinstance(release_profile_contract, dict) else None
        if manual_qa == "required":
            for field in ("qaRecord", "qaInputLockDigest"):
                problems.extend(_digest_problem(
                    subjects.get(field), "%s %s" % (label, field)))
        elif manual_qa == "deferred":
            if subjects.get("qaRecord") is not None or \
                    subjects.get("qaInputLockDigest") is not None:
                problems.append(
                    "%s technical-preview QA subjects must be null" % label)
        else:
            problems.append("%s manual-QA policy is unavailable" % label)
        return problems

    for field in ("bundleConfigDigest", "bundleDigest", "manifestApproval"):
        problems.extend(_digest_problem(
            subjects.get(field), "%s %s" % (label, field)))
    releases = subjects.get("releaseRecords")
    if not isinstance(releases, list) or not releases:
        problems.append("%s releaseRecords is not a non-empty digest list"
                        % label)
    else:
        for index, digest in enumerate(releases):
            problems.extend(_digest_problem(
                digest, "%s releaseRecords[%d]" % (label, index)))
        if len(releases) != len(set(
                value for value in releases if isinstance(value, str))):
            problems.append("%s releaseRecords contains duplicates" % label)
    members = subjects.get("members")
    if not isinstance(members, list) or not members:
        problems.append("%s members is not a non-empty list" % label)
    else:
        names = []
        for index, member in enumerate(members):
            if not isinstance(member, dict) or set(member) != {
                    "name", "digest"}:
                problems.append("%s member %d has the wrong fields"
                                % (label, index))
                continue
            name = member.get("name")
            if not isinstance(name, str) or not name or \
                    canon.normalize_nfc(name) != name:
                problems.append("%s member %d has an invalid name"
                                % (label, index))
            else:
                names.append(name.casefold())
            problems.extend(_digest_problem(
                member.get("digest"), "%s member %d digest" % (label, index)))
        if len(names) != len(set(names)):
            problems.append("%s members contains duplicate names" % label)
    return problems


def acceptance_receipt_problems(receipt, kind, current_context,
                                expected_subjects):
    """Return closed-shape, currency, phase, and subject-binding defects.

    The receipt contains no digest of its enclosing/self record.  Typed
    predecessor subjects (QA, configured releases, manifest approval) point
    backward and are known before the outer record is hashed, keeping the
    evidence graph acyclic while the append-only envelope authenticates it.
    """
    if kind not in ("release", "bundle"):
        return ["unknown acceptance receipt kind %r" % kind]
    if not isinstance(receipt, dict):
        return ["%s acceptance receipt is not an object" % kind]
    problems = []
    if set(receipt) != _RECEIPT_FIELDS:
        problems.append("%s acceptance receipt has the wrong fields" % kind)
    if receipt.get("receiptVersion") != "2":
        problems.append("%s acceptance receipt has the wrong version" % kind)
    if receipt.get("runnerKind") != "tool":
        problems.append("%s acceptance receipt runnerKind is not 'tool'" % kind)
    problems.extend(_context_problems(current_context))
    if isinstance(current_context, dict):
        for field in ("registryDigest", "runnerDigest", "runnerInputs",
                      "runnerEditions", "releaseProfile",
                      "releaseProfileContract"):
            if receipt.get(field) != current_context.get(field):
                problems.append("%s acceptance receipt %s is stale"
                                % (kind, field))
    expected_results = None
    if isinstance(current_context, dict):
        phases = current_context.get("receiptPhases")
        if phases == _receipt_plans():
            expected_results = _receipt_results(kind, phases)
    results = receipt.get("results")
    if expected_results is None or results != expected_results:
        problems.append("%s acceptance receipt does not carry the exact "
                        "phase/criterion pass set" % kind)
    elif any(not isinstance(result, dict) or
             set(result) != _RESULT_FIELDS for result in results):
        problems.append("%s acceptance receipt result shape is invalid" % kind)
    subjects = receipt.get("subjects")
    profile_contract = current_context.get("releaseProfileContract") \
        if isinstance(current_context, dict) else None
    problems.extend(_subject_problems(
        kind, subjects, "%s acceptance receipt" % kind,
        profile_contract))
    expected_problems = _subject_problems(
        kind, expected_subjects, "current %s acceptance" % kind,
        profile_contract)
    problems.extend(expected_problems)
    if subjects != expected_subjects:
        problems.append("%s acceptance receipt subjects are stale or wrong"
                        % kind)
    if kind == "release" and isinstance(subjects, dict) and \
            receipt.get("runnerEditions") != [subjects.get("edition")]:
        problems.append(
            "release acceptance receipt runner edition does not match its "
            "subject")
    return problems


def release_subjects(edition, candidate_digest, content_lock_digest,
                     qa_record_digest, qa_input_lock_digest,
                     release_profile_contract):
    subjects = {
        "edition": edition,
        "candidateDigest": candidate_digest,
        "contentLockDigest": content_lock_digest,
        "qaRecord": qa_record_digest,
        "qaInputLockDigest": qa_input_lock_digest,
    }
    subjects.update(profile_record_fields(release_profile_contract))
    return subjects


def bundle_subjects(bundle_config_digest, bundle_digest, release_records,
                    members, manifest_approval, release_profile_contract):
    subjects = {
        "bundleConfigDigest": bundle_config_digest,
        "bundleDigest": bundle_digest,
        "releaseRecords": list(release_records),
        "members": [{"name": item["name"], "digest": item["digest"]}
                    for item in members],
        "manifestApproval": manifest_approval,
    }
    subjects.update(profile_record_fields(release_profile_contract))
    return subjects


def _make_receipt(kind, context, subjects):
    context_problems = _context_problems(context)
    if context_problems:
        raise AcceptanceError("cannot create acceptance receipt: %s"
                              % "; ".join(context_problems))
    receipt = {
        "receiptVersion": "2",
        "registryDigest": context["registryDigest"],
        "runnerDigest": context["runnerDigest"],
        "runnerInputs": context["runnerInputs"],
        "runnerEditions": context["runnerEditions"],
        "runnerKind": "tool",
        "releaseProfile": context["releaseProfile"],
        "releaseProfileContract": copy.deepcopy(
            context["releaseProfileContract"]),
        "results": _receipt_results(kind, context["receiptPhases"]),
        "subjects": subjects,
    }
    problems = acceptance_receipt_problems(
        receipt, kind, context, subjects)
    if problems:
        raise AcceptanceError("cannot create acceptance receipt: %s"
                              % "; ".join(problems))
    return receipt


def _registry(root):
    content = gateway.ContentGateway(root)
    return _validate_registry(canon.parse_json(content.read_text(
        "navigator/schema/acceptance.json")))


def _run_registered_callbacks_child(payload):
    """Fresh-interpreter entry point for the registry-named test suites."""
    required = {"root", "criterionIds", "editionIds", "declaredInputs",
                "expectedContext", "callbackContext"}
    if not isinstance(payload, dict) or set(payload) != required:
        raise AcceptanceError("acceptance child payload is malformed")
    root = payload["root"]
    edition_ids = payload["editionIds"]
    criterion_ids = payload["criterionIds"]
    declared_inputs = payload["declaredInputs"]
    expected_context = payload["expectedContext"]
    callback_context = payload["callbackContext"]
    if not isinstance(root, str) or not root or \
            not isinstance(criterion_ids, list) or not criterion_ids or \
            not all(item in _ACCEPTANCE_IDS for item in criterion_ids) or \
            callback_context is not None and \
            not isinstance(callback_context, dict):
        raise AcceptanceError("acceptance child selection is malformed")
    registry = _registry(root)
    runner_editions = _runner_editions(registry, edition_ids)
    expected_profile = expected_context.get("releaseProfile") \
        if isinstance(expected_context, dict) else None
    context = acceptance_context(
        root, declared_inputs, runner_editions, expected_profile)
    if context != expected_context:
        raise AcceptanceError(
            "acceptance runner bytes differ before callback import")

    by_id = {criterion["id"]: criterion for criterion in registry["criteria"]}
    test_scopes = {
        entry["test"]: set(entry["editions"])
        for entry in registry["runner"]["testScopes"]
    }
    selected_editions = set(runner_editions)
    module_paths = {
        entry["module"]: entry["path"]
        for entry in registry["runner"]["testModules"]
    }
    loaded = {}

    def load(module_name):
        if module_name not in loaded:
            try:
                test_module = importlib.import_module("tests." + module_name)
            except ImportError as exc:
                raise AcceptanceError(
                    "cannot load acceptance module %s: %s" %
                    (module_name, exc))
            expected_file = os.path.realpath(os.path.join(
                root, module_paths[module_name]))
            if os.path.realpath(test_module.__file__) != expected_file:
                raise AcceptanceError(
                    "acceptance module %s loaded from the wrong path" %
                    module_name)
            if module_name == "test_acceptance":
                nav = os.path.join(root, "navigator")
                test_module.ROOT = root
                test_module.NAV = nav
                test_module.DIST = os.path.join(nav, "dist")
                test_module.RECORDS = os.path.join(nav, "records")
                test_module.TDD = os.path.join(
                    root,
                    "AA11393US-claims-navigator_technical-description_DRAFT.md")
                test_module.EDITIONS = runner_editions
                test_module.ACCEPTANCE_CALLBACK_CONTEXT = callback_context
                test_module._cache.clear()
            loaded[module_name] = test_module
        return loaded[module_name]

    for criterion_id in criterion_ids:
        suite = unittest.TestSuite()
        for registered in by_id[criterion_id]["enforcedBy"]["tests"]:
            scoped = test_scopes.get(registered)
            if scoped is not None and not selected_editions.intersection(
                    scoped):
                continue
            module_name, class_name, method_name = registered.split(".")
            test_module = load(module_name)
            test_class = getattr(test_module, class_name, None)
            if not isinstance(test_class, type) or \
                    not issubclass(test_class, unittest.TestCase) or \
                    not hasattr(test_class, method_name):
                raise AcceptanceError(
                    "%s callback %r is not a live unittest" %
                    (criterion_id, registered))
            suite.addTest(test_class(method_name))
        if suite.countTestCases() == 0:
            raise AcceptanceError(
                "%s has no callback for the selected runner editions"
                % criterion_id)
        stream = io.StringIO()
        result = unittest.TextTestRunner(
            stream=stream, verbosity=0).run(suite)
        if not result.wasSuccessful() or result.skipped or \
                result.expectedFailures or result.unexpectedSuccesses:
            detail = stream.getvalue().strip()
            raise AcceptanceError(
                "%s callback failed: %s" %
                (criterion_id, detail[-4000:] or "no diagnostic"))
    for test_module in loaded.values():
        cache = getattr(test_module, "_cache", None)
        if isinstance(cache, dict):
            cache.clear()
    if acceptance_context(
            root, declared_inputs, runner_editions,
            expected_profile) != expected_context:
        raise AcceptanceError(
            "acceptance registry or runner inputs changed during callbacks")


_CALLBACK_CHILD = """
import sys
sys.path.insert(0, "navigator")
from lib import canon, release
payload = canon.parse_json(sys.stdin.buffer.read())
release._run_registered_callbacks_child(payload)
"""


def _run_registered_callbacks(root, criterion_ids, edition_ids,
                              declared_inputs, expected_context,
                              callback_context=None):
    """Execute locked registry callbacks in a fresh interpreter process."""
    payload = {
        "root": root,
        "criterionIds": list(criterion_ids),
        "editionIds": list(edition_ids),
        "declaredInputs": list(declared_inputs),
        "expectedContext": expected_context,
        "callbackContext": callback_context,
    }
    try:
        with tempfile.TemporaryDirectory(
                prefix="aa11393-acceptance-pycache-") as pycache:
            child = subprocess.run(
                [sys.executable, "-I", "-B", "-X",
                 "pycache_prefix=" + pycache, "-c", _CALLBACK_CHILD],
                cwd=root, input=canon.canonical_json(payload),
                capture_output=True, timeout=1800)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise AcceptanceError(
            "fresh-process acceptance callbacks could not complete: %s" %
            exc)
    if child.returncode != 0:
        detail = "\n".join(
            part.decode("utf-8", "replace").strip()
            for part in (child.stdout, child.stderr)
            if part.strip())
        raise AcceptanceError(
            "fresh-process acceptance callbacks failed: %s" %
            (detail[-8000:] or "no diagnostic"))


def _verify_release_preflight(root, model, derived_bytes, candidate_bytes,
                              content_lock, qa_envelope,
                              release_profile_contract):
    from . import render

    problems = []
    candidate_digest = canon.bytes_digest(candidate_bytes)
    if candidate_bytes != derived_bytes:
        problems.append("candidate bytes differ from the release derivation")
    first_build = render.render(model, mode="candidate")
    second_build = render.render(model, mode="candidate")
    if first_build != derived_bytes or second_build != derived_bytes:
        problems.append("in-process double build is not byte-identical")
    problems.extend(exact_set_check(
        content_lock, model.edition["declaredTransitiveInputs"]))
    profile_problems = _release_profile_entry_problems(
        release_profile_contract)
    problems.extend("release profile: %s" % problem
                    for problem in profile_problems)
    manual_qa = release_profile_contract.get("manualQaEvidence") \
        if not profile_problems else None
    if manual_qa == "required":
        qa_record = qa_envelope.get("record") \
            if isinstance(qa_envelope, dict) else None
        if not isinstance(qa_record, dict):
            problems.append("QA authorization is not an object")
        else:
            if qa_record.get("candidateDigest") != candidate_digest:
                problems.append(
                    "QA authorization does not bind candidate bytes")
            if qa_record.get("lockDigest") != content_lock.get("lockDigest"):
                problems.append(
                    "QA authorization does not bind the content lock")
            qa_lock = qa_record.get("qaInputLock")
            if not isinstance(qa_lock, dict) or \
                    qa_lock.get("candidateDigest") != candidate_digest or \
                    qa_lock.get("contentLockDigest") != content_lock.get(
                        "lockDigest"):
                problems.append("QA input lock does not bind release inputs")
    elif manual_qa == "deferred" and qa_envelope is not None:
        problems.append(
            "technical-preview release must not claim a QA authorization")

    script = """
import sys
sys.path.insert(0, "navigator")
from lib import canon, gateway, model, render
root = %r
edition = %r
edition_path = "navigator/editions/%%s.json" %% edition
boot = gateway.ContentGateway(root)
allow = canon.parse_json(boot.read_text(edition_path))["declaredTransitiveInputs"]
gw = gateway.ContentGateway(root, allowlist=allow)
current = model.EditionModel(gw, edition_path)
data = render.render(current, mode="candidate")
lock = gw.lock()
print(canon.canonical_json({"candidateDigest": canon.bytes_digest(data),
                            "lockDigest": lock["lockDigest"]}).decode("utf-8"))
""" % (root, model.edition["editionId"])
    child = subprocess.run(
        [sys.executable, "-c", script], cwd=root, capture_output=True,
        text=True, timeout=300)
    if child.returncode != 0:
        problems.append("cross-process build failed: %s" %
                        child.stderr.strip()[-1000:])
    else:
        try:
            child_result = canon.parse_json(child.stdout.strip())
        except (canon.CanonError, TypeError, ValueError) as exc:
            problems.append("cross-process build result is malformed: %s" % exc)
        else:
            if child_result != {
                    "candidateDigest": candidate_digest,
                    "lockDigest": content_lock.get("lockDigest")}:
                problems.append("cross-process build or content lock differs")
    if problems:
        raise AcceptanceError("AC-16 release preflight failed: %s"
                              % "; ".join(problems))


def _verify_release_postcondition(output, sealed_name, candidate_bytes,
                                  checksum_bytes):
    from . import bundlezip

    output.verify_written("sealed", sealed_name, candidate_bytes)
    output.verify_written(
        "artifact-checksum", sealed_name + ".sha256", checksum_bytes)
    bundlezip.verify_detached_checksum(
        checksum_bytes, sealed_name, canon.bytes_digest(candidate_bytes))


def run_release_acceptance_transaction(root, model, derived_bytes,
                                       candidate_bytes, content_lock,
                                       qa_envelope, output,
                                       release_profile=None):
    """Run release criteria, write/read-back outputs, and return the receipt.

    The append-only release record is intentionally outside this transaction
    and must be appended by the caller *after* it receives the receipt.  Thus
    a failed phase can leave only unauthorizing artifact bytes, never a passed
    release record.
    """
    declared = model.edition["declaredTransitiveInputs"]
    edition_ids = (model.edition["editionId"],)
    before = acceptance_context(
        root, declared, edition_ids, release_profile)
    registered_ids = tuple(
        criterion for criterion in
        before["receiptPhases"]["release-preflight"]
        if criterion != "AC-16")
    _run_registered_callbacks(
        root, registered_ids, edition_ids, declared, before)
    _verify_release_preflight(
        root, model, derived_bytes, candidate_bytes, content_lock, qa_envelope,
        before["releaseProfileContract"])
    sealed_name = model.edition["artifactName"]
    checksum_bytes = checksum_text(
        sealed_name, candidate_bytes).encode("utf-8")
    output.write("sealed", sealed_name, candidate_bytes)
    output.write("artifact-checksum", sealed_name + ".sha256", checksum_bytes)
    _verify_release_postcondition(
        output, sealed_name, candidate_bytes, checksum_bytes)
    after = acceptance_context(
        root, declared, edition_ids, before["releaseProfile"])
    if after != before:
        raise AcceptanceError(
            "acceptance registry or runner inputs changed during release")
    if before["releaseProfileContract"]["manualQaEvidence"] == "required":
        qa_record_digest = qa_envelope["digest"]
        qa_input_lock_digest = qa_envelope["record"]["qaInputLock"][
            "lockDigest"]
    else:
        qa_record_digest = None
        qa_input_lock_digest = None
    subjects = release_subjects(
        model.edition["editionId"], canon.bytes_digest(candidate_bytes),
        content_lock["lockDigest"], qa_record_digest,
        qa_input_lock_digest, before["releaseProfileContract"])
    return _make_receipt("release", before, subjects)


def _verify_bundle_postcondition(root, cfg, plan, zip_bytes, checksum_bytes,
                                 manifest_bytes, output):
    from . import bundlezip

    manifest_member = next(
        member for member in cfg["members"]
        if member["kind"] == "bundle-manifest")
    output.verify_written(
        "bundle-manifest", manifest_member["name"], manifest_bytes)
    output.verify_written("bundle", cfg["name"], zip_bytes)
    output.verify_written(
        "bundle-checksum", cfg["name"] + ".sha256", checksum_bytes)
    bundlezip.verify_detached_checksum(
        checksum_bytes, cfg["name"], canon.bytes_digest(zip_bytes))
    if bundlezip.read_zip_members(zip_bytes) != plan["members"]:
        raise AcceptanceError("AC-20 bundle members differ from resolved plan")
    if bundlezip.build_zip(
            plan["members"], cfg["declaredTimestamp"]) != zip_bytes:
        raise AcceptanceError("AC-20 deterministic ZIP rebuild differs")
    expected_members = [(member["name"], member["digest"])
                        for member in cfg["members"]]
    actual_members = [(name, canon.bytes_digest(data))
                      for name, data in plan["members"]]
    if actual_members != expected_members:
        raise AcceptanceError("AC-20 configured member subjects differ")
    expected_releases = [member["releaseRecord"] for member in cfg["members"]
                         if member["kind"] == "sealed"]
    if plan["releaseRecords"] != expected_releases:
        raise AcceptanceError("AC-20 configured release subjects differ")
    golden = canon.parse_json(gateway.ContentGateway(root).read_text(
        "navigator/tests/fixtures/golden_bundle.json"))
    golden_bytes = bundlezip.build_zip(
        [(name, data.encode("ascii")) for name, data in golden["members"]],
        golden["declaredTimestamp"])
    if golden_bytes.hex() != golden["hex"] or \
            canon.bytes_digest(golden_bytes) != golden["sha256"]:
        raise AcceptanceError("AC-20 golden ZIP conformance failed")


def _bundle_callback_context(cfg, bundle_config_digest, plan, zip_bytes,
                             checksum_bytes, manifest_bytes, output):
    """Build the closed canonical context consumed by registered AC-20.

    Artifact bytes stay out of the subprocess argument.  The fresh callback
    reads them back from the transaction's output root and compares their
    digests and structure with this exact transaction description.
    """
    return {
        "kind": "bundle-postcondition",
        "outputRoot": output.root,
        "config": cfg,
        "bundleConfigDigest": bundle_config_digest,
        "bundleDigest": canon.bytes_digest(zip_bytes),
        "bundleChecksumDigest": canon.bytes_digest(checksum_bytes),
        "manifestDigest": canon.bytes_digest(manifest_bytes),
        "plannedMembers": [
            {"name": name, "digest": canon.bytes_digest(data)}
            for name, data in plan["members"]
        ],
        "releaseRecords": list(plan["releaseRecords"]),
        "manifestApproval": plan["manifestApproval"],
        "chain": plan["acceptanceChain"],
    }


def run_bundle_acceptance_transaction(root, declared_inputs, cfg,
                                      bundle_config_digest, plan, zip_bytes,
                                      checksum_bytes, manifest_bytes, output):
    """Write/read-back bundle outputs and return an AC-20 receipt."""
    if not isinstance(plan, dict) or \
            not isinstance(plan.get("acceptanceChain"), dict):
        raise AcceptanceError(
            "AC-20 resolved acceptance chain context is unavailable")
    runner_editions = cfg.get("editions") if isinstance(cfg, dict) else None
    release_profile = cfg.get("releaseProfile") \
        if isinstance(cfg, dict) else None
    if not isinstance(release_profile, str) or not release_profile:
        raise AcceptanceError(
            "AC-20 bundle config has no explicit releaseProfile")
    before = acceptance_context(
        root, declared_inputs, runner_editions, release_profile)
    manifest_member = next(
        member for member in cfg["members"]
        if member["kind"] == "bundle-manifest")
    output.write(
        "bundle-manifest", manifest_member["name"], manifest_bytes)
    output.write("bundle", cfg["name"], zip_bytes)
    output.write("bundle-checksum", cfg["name"] + ".sha256", checksum_bytes)
    _verify_bundle_postcondition(
        root, cfg, plan, zip_bytes, checksum_bytes, manifest_bytes, output)
    _run_registered_callbacks(
        root, ("AC-20",), runner_editions, declared_inputs, before,
        _bundle_callback_context(
            cfg, bundle_config_digest, plan, zip_bytes, checksum_bytes,
            manifest_bytes, output))
    after = acceptance_context(
        root, declared_inputs, runner_editions, release_profile)
    if after != before:
        raise AcceptanceError(
            "acceptance registry or runner inputs changed during bundle")
    members = [{"name": name, "digest": canon.bytes_digest(data)}
               for name, data in plan["members"]]
    subjects = bundle_subjects(
        bundle_config_digest, canon.bytes_digest(zip_bytes),
        plan["releaseRecords"], members, plan["manifestApproval"],
        before["releaseProfileContract"])
    return _make_receipt("bundle", before, subjects)


def reproduction_diagnostics():
    """Non-normative runtime diagnostics — a sibling of the lock, excluded
    from the lock digest and the candidate<->release equality check."""
    return {
        "interpreter": sys.version.split()[0],
        "platform": platform.platform(),
        "locale": ".".join(str(x) for x in locale.getlocale() if x) or "C",
        "unicodedata": __import__("unicodedata").unidata_version,
    }


def exact_set_check(lock, declared_inputs):
    """The read log must equal the edition config's declared transitive
    input set exactly."""
    read = {e["path"] for e in lock["reads"]}
    declared = set(declared_inputs)
    missing = declared - read
    extra = read - declared
    problems = []
    if missing:
        problems.append("declared but never read: %s" % sorted(missing))
    if extra:
        problems.append("read but not declared: %s" % sorted(extra))
    return problems


def verify_envelope(qa_record, candidate_digest, lock_digest, attestations,
                    side_digests=None):
    """Release-verification envelope: the QA record must authorize exactly
    these candidate bytes and this lock, and every referenced double-sided
    attestation must be present and current."""
    problems = []
    rec = qa_record["record"]
    if rec.get("candidateDigest") != candidate_digest:
        problems.append(
            "QA record authorizes candidate %s, not %s"
            % (rec.get("candidateDigest"), candidate_digest))
    if rec.get("lockDigest") != lock_digest:
        problems.append("QA record lock digest does not match this build")
    referenced = set(rec.get("attestations", []))
    present = {a["digest"]: a for a in attestations}
    for digest in referenced - set(present):
        problems.append("attestation %s referenced by QA record is missing"
                        % digest)
    if side_digests is not None:
        for digest in sorted(referenced & set(present)):
            for problem in attestation_current(present[digest], side_digests):
                problems.append("referenced attestation %s is not current: %s"
                                % (digest, problem))
    return problems


def attestation_current(att, side_digests):
    """Double-sided binding: every side recorded in the attestation must
    equal the current digest of that side."""
    problems = []
    for side, digest in att["record"].get("sides", {}).items():
        current = side_digests.get(side)
        if current is None:
            problems.append("attestation side %r has no current digest" % side)
        elif current != digest:
            problems.append(
                "attestation side %r stale: recorded %s, current %s"
                % (side, digest, current))
    return problems


def checksum_text(name, data):
    return "%s  %s\n" % (canon.bytes_digest(data), name)
