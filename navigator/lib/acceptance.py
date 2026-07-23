"""Executable acceptance controls, contexts, and receipts.

The acceptance registry owns criterion-to-evidence mappings.  Release policy
owns artifact-facing profile selection.  This module joins those independent
inputs into derived atomic controls; phase plans and manual-QA field sets are
never maintained as parallel authored lists.
"""

import copy
import importlib
import io
import os
import re
import subprocess
import sys
import tempfile
import unittest

from . import canon, control_inventory, gateway, profilepolicy, qaevidence


class AcceptanceError(ValueError):
    """An executable acceptance contract failed or its evidence drifted."""


ACCEPTANCE_PATH = "navigator/schema/acceptance.json"
RELEASE_POLICY_PATH = "navigator/schema/release-policy.json"
MINIMUM_CRITERIA = tuple("AC-%02d" % number for number in range(1, 21))
_CRITERION_ID = re.compile(r"AC-(0[1-9]|[1-9][0-9]+)\Z")
_REGISTRY_FIELDS = frozenset((
    "acceptanceVersion", "comment", "runner", "criteria",
))
_CRITERION_FIELDS = frozenset((
    "id", "applicability", "text", "enforcedBy",
))
_RUNNER_FIELDS = frozenset((
    "runnerVersion", "editions", "testModules", "fixtures",
    "testScopes", "supportFiles",
))
_TEST_MODULE_FIELDS = frozenset(("module", "path"))
_FIXTURE_FIELDS = frozenset(("path", "editions"))
_TEST_SCOPE_FIELDS = frozenset(("test", "editions"))
_RUNNER_INPUT_FIELDS = frozenset(("path", "digest"))
_CONTEXT_FIELDS = frozenset((
    "registryDigest", "policyDigest", "runnerDigest", "runnerInputs",
    "runnerEditions", "controlPlan", "releaseProfile",
    "releaseProfileContract",
))
_RECEIPT_FIELDS = frozenset((
    "receiptVersion", "registryDigest", "policyDigest", "runnerDigest",
    "runnerInputs", "runnerEditions", "runnerKind", "releaseProfile",
    "releaseProfileContract", "results", "subjects",
))
_RESULT_FIELDS = frozenset(("control", "phase", "status"))
_RELEASE_SUBJECT_FIELDS = frozenset((
    "edition", "candidateDigest", "contentLockDigest", "qaRecord",
    "qaInputLockDigest", "releaseProfile", "compatibilityAuthorization",
    "deferredControls", "artifactLabel",
))
_BUNDLE_SUBJECT_FIELDS = frozenset((
    "bundleConfigDigest", "bundleDigest", "releaseRecords", "members",
    "manifestApproval", "releaseProfile", "compatibilityAuthorization",
    "deferredControls", "artifactLabel",
))
_PHASES = (
    "release-preflight", "release-postcondition", "bundle-postcondition",
)
_BUILTIN_CONTROLS = (
    {
        "id": "AC-16.release-preflight",
        "criterion": "AC-16",
        "phase": "release-preflight",
        "executor": "builtin",
        "tests": [],
        "qaRecordField": None,
    },
    {
        "id": "AC-16.release-postcondition",
        "criterion": "AC-16",
        "phase": "release-postcondition",
        "executor": "builtin",
        "tests": [],
        "qaRecordField": None,
    },
    {
        "id": "AC-20.bundle-postcondition",
        "criterion": "AC-20",
        "phase": "bundle-postcondition",
        "executor": "builtin",
        "tests": [],
        "qaRecordField": None,
    },
)


def _safe_path(value, label, suffix=None):
    if not isinstance(value, str) or not value or os.path.isabs(value) or \
            "\\" in value or ".." in value.split("/") or \
            any(not part or part == "." for part in value.split("/")) or \
            suffix is not None and not value.endswith(suffix):
        raise AcceptanceError("%s is not a canonical repository path" % label)
    return value


def _criterion_sort_key(identifier):
    match = _CRITERION_ID.fullmatch(identifier) \
        if isinstance(identifier, str) else None
    return int(match.group(1)) if match else -1


def _derived_controls(registry):
    """Return atomic controls from the registry's sole evidence mapping."""
    controls = []
    for criterion in registry["criteria"]:
        criterion_id = criterion["id"]
        phase = ("bundle-postcondition"
                 if criterion["applicability"] == "bundle"
                 else "release-preflight")
        enforced = criterion["enforcedBy"]
        controls.append({
            "id": criterion_id + ".automated",
            "criterion": criterion_id,
            "phase": phase,
            "executor": "callbacks",
            "tests": list(enforced["tests"]),
            "qaRecordField": None,
        })
        fields = enforced["qaRecordFields"]
        if fields:
            controls.append({
                "id": criterion_id + ".observed",
                "criterion": criterion_id,
                "phase": "release-preflight",
                "executor": "observation",
                "tests": [],
                "qaRecordField": fields[0],
            })
    controls.extend(copy.deepcopy(_BUILTIN_CONTROLS))
    return tuple(sorted(controls, key=lambda item: (
        _PHASES.index(item["phase"]), item["id"])))


def control_plan(registry):
    plan = {phase: [] for phase in _PHASES}
    for control in _derived_controls(registry):
        plan[control["phase"]].append(control["id"])
    return plan


def _registry_controls_by_id(registry):
    return {control["id"]: control for control in _derived_controls(registry)}


def validate_registry(value):
    """Validate the extensible registry and its closed current baseline."""
    if not isinstance(value, dict) or set(value) != _REGISTRY_FIELDS or \
            canon.require_version(value, "acceptanceVersion", "3") or \
            not isinstance(value.get("comment"), str) or \
            not value.get("comment", "").strip():
        raise AcceptanceError(
            "acceptance registry top-level shape/version is not current")
    criteria = value.get("criteria")
    if not isinstance(criteria, list) or not criteria or \
            not all(isinstance(item, dict) for item in criteria):
        raise AcceptanceError("acceptance registry has no criterion set")
    ids = [item.get("id") for item in criteria]
    if any(_CRITERION_ID.fullmatch(item) is None
           for item in ids if isinstance(item, str)) or \
            not all(isinstance(item, str) for item in ids) or \
            ids != sorted(ids, key=_criterion_sort_key) or \
            len(ids) != len(set(ids)) or \
            not set(MINIMUM_CRITERIA).issubset(ids):
        raise AcceptanceError(
            "acceptance criterion ids must be sorted, unique, and include "
            "the complete mandatory baseline")
    expected_applicability = {
        **{identifier: "edition" for identifier in MINIMUM_CRITERIA[:18]},
        "AC-19": "shared",
        "AC-20": "bundle",
    }

    runner = value.get("runner")
    if not isinstance(runner, dict) or set(runner) != _RUNNER_FIELDS or \
            canon.require_version(runner, "runnerVersion", "3"):
        raise AcceptanceError("acceptance registry runner is malformed")
    editions = runner.get("editions")
    if not isinstance(editions, list) or not editions or \
            editions != sorted(editions) or len(editions) != len(set(editions)) or \
            not all(isinstance(item, str) and item.isidentifier() and
                    item.isascii() and item == item.lower()
                    for item in editions):
        raise AcceptanceError(
            "acceptance runner editions are not an exact sorted set")
    declared_editions = set(editions)

    modules = runner.get("testModules")
    if not isinstance(modules, list) or not modules:
        raise AcceptanceError("acceptance runner declares no test modules")
    module_names = []
    module_paths = []
    for entry in modules:
        if not isinstance(entry, dict) or set(entry) != _TEST_MODULE_FIELDS or \
                not isinstance(entry.get("module"), str) or \
                not entry["module"].isidentifier():
            raise AcceptanceError("acceptance test module is malformed")
        _safe_path(entry.get("path"), "acceptance test module", ".py")
        module_names.append(entry["module"])
        module_paths.append(entry["path"])
    if module_names != sorted(module_names) or \
            len(module_names) != len(set(module_names)) or \
            module_paths != sorted(module_paths) or \
            len(module_paths) != len(set(module_paths)):
        raise AcceptanceError(
            "acceptance test modules are not exact sorted sets")
    declared_modules = set(module_names)

    referenced_modules = set()
    registered_tests = set()
    observed_fields = []
    for criterion in criteria:
        criterion_id = criterion["id"]
        if set(criterion) != _CRITERION_FIELDS or \
                criterion.get("applicability") not in {
                    "edition", "shared", "bundle"} or \
                criterion_id in expected_applicability and \
                criterion.get("applicability") != \
                    expected_applicability[criterion_id] or \
                not isinstance(criterion.get("text"), str) or \
                not criterion.get("text", "").strip():
            raise AcceptanceError(
                "%s criterion shape/applicability/text is malformed" %
                criterion_id)
        enforced = criterion.get("enforcedBy")
        if not isinstance(enforced, dict) or set(enforced) != {
                "tests", "qaRecordFields"}:
            raise AcceptanceError(
                "%s has a malformed evidence map" % criterion_id)
        fields = enforced.get("qaRecordFields")
        if not isinstance(fields, list) or len(fields) > 1 or \
                len(fields) != len(set(fields)) or \
                not all(isinstance(field, str) and field for field in fields):
            raise AcceptanceError(
                "%s observed-evidence mapping is malformed" % criterion_id)
        observed_fields.extend(fields)
        tests = enforced.get("tests")
        if not isinstance(tests, list) or not tests or \
                len(tests) != len(set(tests)):
            raise AcceptanceError(
                "%s has no exact executable callback set" % criterion_id)
        for registered in tests:
            if not isinstance(registered, str) or \
                    len(registered.split(".")) != 3:
                raise AcceptanceError(
                    "%s has a malformed callback name" % criterion_id)
            module_name, class_name, method_name = registered.split(".")
            if module_name not in declared_modules or \
                    not class_name.isidentifier() or \
                    not method_name.isidentifier() or \
                    not method_name.startswith("test_"):
                raise AcceptanceError(
                    "%s callback %r is not declared by the runner" %
                    (criterion_id, registered))
            expected_prefix = "test_%s_" % criterion_id.lower().replace(
                "-", "")
            if module_name == "test_acceptance" and (
                    class_name != "Acceptance" or
                    not method_name.startswith(expected_prefix)):
                raise AcceptanceError(
                    "%s callback %r does not match its criterion identity" %
                    (criterion_id, registered))
            if module_name == "test_canon" and criterion_id != "AC-07":
                raise AcceptanceError(
                    "%s may not own canonicalization callback %r" %
                    (criterion_id, registered))
            if registered in registered_tests:
                raise AcceptanceError(
                    "acceptance callback %r has more than one owner" %
                    registered)
            registered_tests.add(registered)
            referenced_modules.add(module_name)
    if set(observed_fields) != qaevidence.MANUAL_QA_FIELDS or \
            len(observed_fields) != len(qaevidence.MANUAL_QA_FIELDS):
        raise AcceptanceError(
            "observed-evidence fields do not match the current QA grammar")
    if referenced_modules != declared_modules:
        raise AcceptanceError(
            "acceptance test modules and callbacks do not close")

    fixtures = runner.get("fixtures")
    if not isinstance(fixtures, list) or not fixtures:
        raise AcceptanceError("acceptance runner declares no fixtures")
    fixture_paths = []
    for entry in fixtures:
        if not isinstance(entry, dict) or set(entry) != _FIXTURE_FIELDS:
            raise AcceptanceError("acceptance fixture is malformed")
        path = _safe_path(entry.get("path"), "acceptance fixture")
        scopes = entry.get("editions")
        if not isinstance(scopes, list) or scopes != sorted(scopes) or \
                len(scopes) != len(set(scopes)) or \
                not set(scopes).issubset(declared_editions):
            raise AcceptanceError("acceptance fixture scope is malformed")
        fixture_paths.append(path)
    if fixture_paths != sorted(fixture_paths) or \
            len(fixture_paths) != len(set(fixture_paths)):
        raise AcceptanceError(
            "acceptance fixtures are not an exact sorted path set")

    test_scopes = runner.get("testScopes")
    if not isinstance(test_scopes, list):
        raise AcceptanceError("acceptance testScopes is malformed")
    scoped_tests = []
    for entry in test_scopes:
        if not isinstance(entry, dict) or set(entry) != _TEST_SCOPE_FIELDS or \
                entry.get("test") not in registered_tests or \
                not isinstance(entry.get("editions"), list) or \
                not entry["editions"] or \
                entry["editions"] != sorted(entry["editions"]) or \
                len(entry["editions"]) != len(set(entry["editions"])) or \
                not set(entry["editions"]).issubset(declared_editions):
            raise AcceptanceError("acceptance test scope is malformed")
        scoped_tests.append(entry["test"])
    if scoped_tests != sorted(scoped_tests) or \
            len(scoped_tests) != len(set(scoped_tests)):
        raise AcceptanceError(
            "acceptance testScopes is not an exact sorted set")

    support_files = runner.get("supportFiles")
    if not isinstance(support_files, list) or not support_files or \
            support_files != sorted(support_files) or \
            len(support_files) != len(set(support_files)):
        raise AcceptanceError(
            "acceptance supportFiles is not an exact sorted path set")
    for path in support_files:
        _safe_path(path, "acceptance support file")
    return value


def load_registry(root, byte_source=None):
    content = gateway.ContentGateway(root, byte_source=byte_source)
    return validate_registry(canon.parse_json(
        content.read_bytes(ACCEPTANCE_PATH)))


def release_profile_contract(policy, registry, requested_profile=None):
    """Join artifact policy to the registry-derived observation controls."""
    registry = validate_registry(registry)
    try:
        profile_id, contract = profilepolicy.copy_contract(
            policy, requested_profile)
    except profilepolicy.ProfilePolicyError as exc:
        raise AcceptanceError(str(exc))
    controls = _registry_controls_by_id(registry)
    observed = {
        identifier: control for identifier, control in controls.items()
        if control["executor"] == "observation"
    }
    try:
        policy_observed = set(profilepolicy.observed_controls(policy))
    except profilepolicy.ProfilePolicyError as exc:
        raise AcceptanceError(str(exc))
    if set(observed) != policy_observed:
        raise AcceptanceError(
            "release policy and observed acceptance controls differ")
    required = contract["requiredObservedControls"]
    contract["requiredQaRecordFields"] = sorted(
        observed[identifier]["qaRecordField"] for identifier in required)
    return profile_id, contract


def profile_record_fields(contract):
    required = {
        "id", "manualQaEvidence", "compatibilityAuthorization",
        "deferredControls", "requiredObservedControls",
        "requiredQaRecordFields", "artifactLabel",
    }
    if not isinstance(contract, dict) or set(contract) != required:
        raise AcceptanceError("release profile contract is malformed")
    try:
        return profilepolicy.record_fields(contract)
    except profilepolicy.ProfilePolicyError as exc:
        raise AcceptanceError(str(exc))


def manual_qa_fields(registry):
    registry = validate_registry(registry)
    return tuple(sorted(
        control["qaRecordField"] for control in _derived_controls(registry)
        if control["executor"] == "observation"))


def _runner_editions(registry, editions):
    if not isinstance(editions, (list, tuple)) or not editions or \
            not all(isinstance(item, str) and item for item in editions):
        raise AcceptanceError("acceptance runner editions are malformed")
    selected = tuple(sorted(editions))
    if len(selected) != len(set(selected)) or \
            not set(selected).issubset(registry["runner"]["editions"]):
        raise AcceptanceError(
            "acceptance runner editions are not a declared exact set")
    return selected


def _runner_input_paths(registry, runner_editions):
    runner = registry["runner"]
    selected = set(runner_editions)
    fixtures = {
        entry["path"] for entry in runner["fixtures"]
        if not entry["editions"] or selected.intersection(entry["editions"])
    }
    modules = {entry["path"] for entry in runner["testModules"]}
    return tuple(sorted(
        set(control_inventory.CONTROL_SOURCE_PATHS) | modules | fixtures |
        set(runner["supportFiles"])))


def runner_digest(registry_digest, policy_digest, runner_inputs,
                  control_plan_value, runner_editions, release_profile,
                  release_profile_contract_value):
    return canon.composite_digest("aa11393:lock:c1", {
        "runnerVersion": "3",
        "runnerEditions": runner_editions,
        "registryDigest": registry_digest,
        "policyDigest": policy_digest,
        "runnerInputs": runner_inputs,
        "controlPlan": control_plan_value,
        "releaseProfile": release_profile,
        "releaseProfileContract": release_profile_contract_value,
    })


def acceptance_context(root, editions, release_profile=None,
                       byte_source=None):
    """Snapshot the exact control implementation, registry, and policy."""
    content = gateway.ContentGateway(root, byte_source=byte_source)
    registry_bytes = content.read_bytes(ACCEPTANCE_PATH)
    policy_bytes = content.read_bytes(RELEASE_POLICY_PATH)
    registry = validate_registry(canon.parse_json(registry_bytes))
    policy = canon.parse_json(policy_bytes)
    try:
        profilepolicy.validate_policy(policy)
    except profilepolicy.ProfilePolicyError as exc:
        raise AcceptanceError(str(exc))
    selected_profile, profile_contract = release_profile_contract(
        policy, registry, release_profile)
    runner_editions = _runner_editions(registry, editions)
    reads = [
        {"path": path, "digest": canon.bytes_digest(content.read_bytes(path))}
        for path in _runner_input_paths(registry, runner_editions)
    ]
    registry_digest = canon.bytes_digest(registry_bytes)
    policy_digest = canon.bytes_digest(policy_bytes)
    plan = control_plan(registry)
    current_runner_digest = runner_digest(
        registry_digest, policy_digest, reads, plan, list(runner_editions),
        selected_profile, profile_contract)
    return {
        "registryDigest": registry_digest,
        "policyDigest": policy_digest,
        "runnerDigest": current_runner_digest,
        "runnerEditions": list(runner_editions),
        "runnerInputs": reads,
        "controlPlan": plan,
        "releaseProfile": selected_profile,
        "releaseProfileContract": profile_contract,
    }


def combine_acceptance_contexts(context_by_edition, editions):
    if not isinstance(editions, (list, tuple)) or not editions or \
            not all(isinstance(item, str) and item for item in editions):
        raise AcceptanceError("bundle runner editions are malformed")
    runner_editions = tuple(sorted(editions))
    if len(runner_editions) != len(set(runner_editions)) or \
            not isinstance(context_by_edition, dict) or \
            set(context_by_edition) != set(runner_editions):
        raise AcceptanceError(
            "bundle acceptance contexts do not match configured editions")
    common = None
    inputs_by_path = {}
    for edition in runner_editions:
        context = context_by_edition[edition]
        problems = _context_problems(context)
        if problems or context.get("runnerEditions") != [edition]:
            raise AcceptanceError(
                "standalone acceptance context for %s is malformed: %s" %
                (edition, "; ".join(problems) if problems else
                 "runner edition mismatch"))
        fields = {
            key: context[key] for key in (
                "registryDigest", "policyDigest", "controlPlan",
                "releaseProfile", "releaseProfileContract")
        }
        if common is None:
            common = fields
        elif fields != common:
            raise AcceptanceError(
                "standalone acceptance contexts do not share one contract")
        for entry in context["runnerInputs"]:
            previous = inputs_by_path.get(entry["path"])
            if previous is not None and previous != entry["digest"]:
                raise AcceptanceError(
                    "standalone contexts disagree on %s" % entry["path"])
            inputs_by_path[entry["path"]] = entry["digest"]
    reads = [{"path": path, "digest": inputs_by_path[path]}
             for path in sorted(inputs_by_path)]
    combined = {
        **common,
        "runnerDigest": runner_digest(
            common["registryDigest"], common["policyDigest"], reads,
            common["controlPlan"], list(runner_editions),
            common["releaseProfile"], common["releaseProfileContract"]),
        "runnerEditions": list(runner_editions),
        "runnerInputs": reads,
    }
    problems = _context_problems(combined)
    if problems:
        raise AcceptanceError(
            "combined acceptance context is malformed: %s" %
            "; ".join(problems))
    return combined


def _digest_problem(value, label):
    try:
        canon.parse_digest(value)
    except (canon.CanonError, TypeError, ValueError) as exc:
        return ["%s is not a canonical digest: %s" % (label, exc)]
    return []


def profile_contract_problems(contract, expected_observed_controls=None):
    expected = {
        "id", "manualQaEvidence", "compatibilityAuthorization",
        "deferredControls", "requiredObservedControls",
        "requiredQaRecordFields", "artifactLabel",
    }
    if not isinstance(contract, dict) or set(contract) != expected:
        return ["release profile contract has the wrong fields"]
    problems = []
    if not isinstance(contract.get("id"), str) or not contract["id"]:
        problems.append("release profile id is empty")
    deferred = contract.get("deferredControls")
    required = contract.get("requiredObservedControls")
    if not isinstance(deferred, list) or deferred != sorted(deferred) or \
            len(deferred) != len(set(deferred)) or \
            not isinstance(required, list) or required != sorted(required) or \
            len(required) != len(set(required)) or \
            not deferred and not required or \
            set(deferred) & set(required) or \
            any(not isinstance(identifier, str) or
                re.fullmatch(r"AC-(?:0[1-9]|[1-9][0-9]+)\.observed",
                             identifier) is None
                for identifier in deferred + required) or \
            expected_observed_controls is not None and \
            set(deferred) | set(required) != set(expected_observed_controls):
        problems.append("release profile observed-control partition is invalid")
    expected_manual = "required" if required else "deferred"
    if contract.get("manualQaEvidence") != expected_manual:
        problems.append("release profile manual-QA policy is inconsistent")
    expected_authorization = (
        "support-matrix-authorized" if not deferred else "not-authorized")
    if contract.get("compatibilityAuthorization") != expected_authorization:
        problems.append("release profile compatibility policy is inconsistent")
    fields = contract.get("requiredQaRecordFields")
    if not isinstance(fields, list) or fields != sorted(fields) or \
            len(fields) != len(set(fields)) or \
            not set(fields).issubset(qaevidence.MANUAL_QA_FIELDS):
        problems.append("release profile QA field set is invalid")
    label = contract.get("artifactLabel")
    if not isinstance(label, str) or not label or label.strip() != label or \
            canon.normalize_nfc(label) != label or \
            any(ord(character) < 32 or ord(character) == 127
                for character in label):
        problems.append("release profile artifact label is not canonical text")
    return problems


def _context_problems(context):
    if not isinstance(context, dict) or set(context) != _CONTEXT_FIELDS:
        return ["current acceptance context is unavailable or malformed"]
    problems = []
    for field, label in (
            ("registryDigest", "acceptance registry digest"),
            ("policyDigest", "release policy digest"),
            ("runnerDigest", "acceptance runner digest")):
        problems.extend(_digest_problem(context.get(field), label))
    profile_contract = context.get("releaseProfileContract")
    plan = context.get("controlPlan")
    expected_observed = None
    if isinstance(plan, dict) and all(
            isinstance(controls, list) for controls in plan.values()):
        expected_observed = {
            identifier for controls in plan.values() for identifier in controls
            if isinstance(identifier, str) and
            identifier.endswith(".observed")
        }
    problems.extend(profile_contract_problems(
        profile_contract, expected_observed))
    if isinstance(profile_contract, dict) and \
            context.get("releaseProfile") != profile_contract.get("id"):
        problems.append("release profile does not match its contract")
    editions = context.get("runnerEditions")
    if not isinstance(editions, list) or not editions or \
            editions != sorted(editions) or len(editions) != len(set(editions)):
        problems.append("acceptance runner editions are not an exact sorted set")
    if not isinstance(plan, dict) or set(plan) != set(_PHASES) or \
            any(not isinstance(plan.get(phase), list) or not plan[phase] or
                plan[phase] != sorted(plan[phase]) or
                len(plan[phase]) != len(set(plan[phase]))
                for phase in _PHASES):
        problems.append("acceptance control plan is malformed")
    reads = context.get("runnerInputs")
    if not isinstance(reads, list) or not reads:
        problems.append("acceptance runner inputs are empty")
    else:
        paths = []
        for index, entry in enumerate(reads):
            if not isinstance(entry, dict) or set(entry) != _RUNNER_INPUT_FIELDS:
                problems.append("acceptance runner input %d is malformed" % index)
                continue
            paths.append(entry.get("path"))
            problems.extend(_digest_problem(
                entry.get("digest"), "acceptance runner input %d" % index))
        if not all(isinstance(path, str) and path for path in paths) or \
                paths != sorted(paths) or len(paths) != len(set(paths)):
            problems.append("acceptance runner inputs are not exact and sorted")
    try:
        expected = runner_digest(
            context.get("registryDigest"), context.get("policyDigest"),
            context.get("runnerInputs"), context.get("controlPlan"),
            context.get("runnerEditions"), context.get("releaseProfile"),
            context.get("releaseProfileContract"))
        if context.get("runnerDigest") != expected:
            problems.append("acceptance runner digest does not derive from context")
    except (canon.CanonError, TypeError, ValueError) as exc:
        problems.append("acceptance runner digest cannot be derived: %s" % exc)
    return problems


def _subject_problems(kind, subjects, label, contract):
    fields = _RELEASE_SUBJECT_FIELDS if kind == "release" \
        else _BUNDLE_SUBJECT_FIELDS
    if not isinstance(subjects, dict) or set(subjects) != fields:
        return ["%s subjects have the wrong fields" % label]
    problems = []
    try:
        expected_profile = profile_record_fields(contract)
    except AcceptanceError as exc:
        problems.append("%s release profile is malformed: %s" % (label, exc))
        expected_profile = {}
    for field, expected in expected_profile.items():
        if subjects.get(field) != expected:
            problems.append("%s %s does not match the profile" % (label, field))
    if kind == "release":
        if not isinstance(subjects.get("edition"), str) or \
                not subjects.get("edition"):
            problems.append("%s edition is empty" % label)
        for field in ("candidateDigest", "contentLockDigest"):
            problems.extend(_digest_problem(
                subjects.get(field), "%s %s" % (label, field)))
        manual_qa = contract.get("manualQaEvidence") \
            if isinstance(contract, dict) else None
        if manual_qa == "required":
            for field in ("qaRecord", "qaInputLockDigest"):
                problems.extend(_digest_problem(
                    subjects.get(field), "%s %s" % (label, field)))
        elif manual_qa == "deferred" and (
                subjects.get("qaRecord") is not None or
                subjects.get("qaInputLockDigest") is not None):
            problems.append("%s deferred QA subjects must be null" % label)
        elif manual_qa not in ("required", "deferred"):
            problems.append("%s QA subjects have no current profile" % label)
        return problems
    for field in ("bundleConfigDigest", "bundleDigest", "manifestApproval"):
        problems.extend(_digest_problem(
            subjects.get(field), "%s %s" % (label, field)))
    releases = subjects.get("releaseRecords")
    if not isinstance(releases, list) or not releases or \
            len(releases) != len(set(releases)):
        problems.append("%s releaseRecords is not a unique digest list" % label)
    else:
        for index, digest in enumerate(releases):
            problems.extend(_digest_problem(
                digest, "%s releaseRecords[%d]" % (label, index)))
    members = subjects.get("members")
    if not isinstance(members, list) or not members:
        problems.append("%s members is empty" % label)
    else:
        names = []
        for index, member in enumerate(members):
            if not isinstance(member, dict) or set(member) != {"name", "digest"}:
                problems.append("%s member %d is malformed" % (label, index))
                continue
            name = member.get("name")
            if not isinstance(name, str) or not name or \
                    canon.normalize_nfc(name) != name:
                problems.append("%s member %d name is invalid" % (label, index))
            else:
                names.append(name.casefold())
            problems.extend(_digest_problem(
                member.get("digest"), "%s member %d" % (label, index)))
        if len(names) != len(set(names)):
            problems.append("%s members contain duplicate names" % label)
    return problems


def _receipt_results(kind, context):
    phases = (("release-preflight", "release-postcondition")
              if kind == "release" else ("bundle-postcondition",))
    deferred = set(context["releaseProfileContract"]["deferredControls"])
    results = []
    for phase in phases:
        for control in context["controlPlan"][phase]:
            status = "deferred" if control in deferred else "passed"
            results.append({"control": control, "phase": phase,
                            "status": status})
    return results


def acceptance_receipt_problems(receipt, kind, current_context,
                                expected_subjects):
    if kind not in ("release", "bundle"):
        return ["unknown acceptance receipt kind %r" % kind]
    if not isinstance(receipt, dict):
        return ["%s acceptance receipt is not an object" % kind]
    problems = []
    if set(receipt) != _RECEIPT_FIELDS:
        problems.append("%s acceptance receipt has the wrong fields" % kind)
    problems.extend(
        "%s acceptance receipt: %s" % (kind, problem)
        for problem in canon.require_version(receipt, "receiptVersion", "3"))
    if receipt.get("runnerKind") != "tool":
        problems.append("%s acceptance runnerKind is not 'tool'" % kind)
    problems.extend(_context_problems(current_context))
    if isinstance(current_context, dict):
        for field in (
                "registryDigest", "policyDigest", "runnerDigest",
                "runnerInputs", "runnerEditions", "releaseProfile",
                "releaseProfileContract"):
            if receipt.get(field) != current_context.get(field):
                problems.append("%s acceptance receipt %s is stale" %
                                (kind, field))
    expected_results = _receipt_results(kind, current_context) \
        if not _context_problems(current_context) else None
    results = receipt.get("results")
    if results != expected_results:
        problems.append(
            "%s acceptance receipt does not carry the exact atomic result set"
            % kind)
    elif any(not isinstance(result, dict) or set(result) != _RESULT_FIELDS
             for result in results):
        problems.append("%s acceptance result shape is invalid" % kind)
    contract = current_context.get("releaseProfileContract") \
        if isinstance(current_context, dict) else None
    problems.extend(_subject_problems(
        kind, receipt.get("subjects"), "%s acceptance receipt" % kind,
        contract))
    problems.extend(_subject_problems(
        kind, expected_subjects, "current %s acceptance" % kind, contract))
    if receipt.get("subjects") != expected_subjects:
        problems.append("%s acceptance subjects are stale or wrong" % kind)
    if kind == "release" and isinstance(receipt.get("subjects"), dict) and \
            receipt.get("runnerEditions") != [
                receipt["subjects"].get("edition")]:
        problems.append("release receipt edition does not match its subject")
    return problems


def release_subjects(edition, candidate_digest, content_lock_digest,
                     qa_record_digest, qa_input_lock_digest, contract):
    subjects = {
        "edition": edition,
        "candidateDigest": candidate_digest,
        "contentLockDigest": content_lock_digest,
        "qaRecord": qa_record_digest,
        "qaInputLockDigest": qa_input_lock_digest,
    }
    subjects.update(profile_record_fields(contract))
    return subjects


def bundle_subjects(bundle_config_digest, bundle_digest, release_records,
                    members, manifest_approval, contract):
    subjects = {
        "bundleConfigDigest": bundle_config_digest,
        "bundleDigest": bundle_digest,
        "releaseRecords": list(release_records),
        "members": [{"name": item["name"], "digest": item["digest"]}
                    for item in members],
        "manifestApproval": manifest_approval,
    }
    subjects.update(profile_record_fields(contract))
    return subjects


def make_receipt(kind, context, subjects):
    problems = _context_problems(context)
    if problems:
        raise AcceptanceError(
            "cannot create acceptance receipt: %s" % "; ".join(problems))
    receipt = {
        "receiptVersion": "3",
        "registryDigest": context["registryDigest"],
        "policyDigest": context["policyDigest"],
        "runnerDigest": context["runnerDigest"],
        "runnerInputs": context["runnerInputs"],
        "runnerEditions": context["runnerEditions"],
        "runnerKind": "tool",
        "releaseProfile": context["releaseProfile"],
        "releaseProfileContract": copy.deepcopy(
            context["releaseProfileContract"]),
        "results": _receipt_results(kind, context),
        "subjects": subjects,
    }
    problems = acceptance_receipt_problems(receipt, kind, context, subjects)
    if problems:
        raise AcceptanceError(
            "cannot create acceptance receipt: %s" % "; ".join(problems))
    return receipt


def _run_registered_callbacks_child(payload):
    required = {
        "root", "controlIds", "editionIds", "expectedContext",
        "callbackContext",
    }
    if not isinstance(payload, dict) or set(payload) != required:
        raise AcceptanceError("acceptance child payload is malformed")
    root = payload["root"]
    control_ids = payload["controlIds"]
    edition_ids = payload["editionIds"]
    expected_context = payload["expectedContext"]
    callback_context = payload["callbackContext"]
    registry = load_registry(root)
    controls = _registry_controls_by_id(registry)
    if not isinstance(root, str) or not root or \
            not isinstance(control_ids, list) or not control_ids or \
            any(identifier not in controls or
                controls[identifier]["executor"] != "callbacks"
                for identifier in control_ids) or \
            callback_context is not None and \
            not isinstance(callback_context, dict):
        raise AcceptanceError("acceptance child selection is malformed")
    runner_editions = _runner_editions(registry, edition_ids)
    expected_profile = expected_context.get("releaseProfile") \
        if isinstance(expected_context, dict) else None
    if acceptance_context(root, runner_editions, expected_profile) != \
            expected_context:
        raise AcceptanceError(
            "acceptance runner bytes differ before callback import")
    scopes = {entry["test"]: set(entry["editions"])
              for entry in registry["runner"]["testScopes"]}
    selected = set(runner_editions)
    module_paths = {entry["module"]: entry["path"]
                    for entry in registry["runner"]["testModules"]}
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

    for identifier in control_ids:
        suite = unittest.TestSuite()
        control = controls[identifier]
        for registered in control["tests"]:
            scoped = scopes.get(registered)
            if scoped is not None and not selected.intersection(scoped):
                continue
            module_name, class_name, method_name = registered.split(".")
            test_module = load(module_name)
            test_class = getattr(test_module, class_name, None)
            if not isinstance(test_class, type) or \
                    not issubclass(test_class, unittest.TestCase) or \
                    not hasattr(test_class, method_name):
                raise AcceptanceError(
                    "%s callback %r is not a live unittest" %
                    (identifier, registered))
            suite.addTest(test_class(method_name))
        if suite.countTestCases() == 0:
            raise AcceptanceError(
                "%s has no callback for selected editions" % identifier)
        stream = io.StringIO()
        result = unittest.TextTestRunner(stream=stream, verbosity=0).run(suite)
        if not result.wasSuccessful() or result.skipped or \
                result.expectedFailures or result.unexpectedSuccesses:
            detail = stream.getvalue().strip()
            raise AcceptanceError(
                "%s callback failed: %s" %
                (identifier, detail[-4000:] or "no diagnostic"))
    for test_module in loaded.values():
        cache = getattr(test_module, "_cache", None)
        if isinstance(cache, dict):
            cache.clear()
    if acceptance_context(root, runner_editions, expected_profile) != \
            expected_context:
        raise AcceptanceError(
            "acceptance registry, policy, or runner inputs changed during "
            "callbacks")


_CALLBACK_CHILD = """
import sys
sys.path.insert(0, "navigator")
from lib import acceptance, canon
payload = canon.parse_json(sys.stdin.buffer.read())
acceptance._run_registered_callbacks_child(payload)
"""


def run_registered_callbacks(root, control_ids, edition_ids,
                             expected_context, callback_context=None):
    payload = {
        "root": root,
        "controlIds": list(control_ids),
        "editionIds": list(edition_ids),
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
            "fresh-process acceptance callbacks could not complete: %s" % exc)
    if child.returncode != 0:
        detail = "\n".join(
            part.decode("utf-8", "replace").strip()
            for part in (child.stdout, child.stderr) if part.strip())
        raise AcceptanceError(
            "fresh-process acceptance callbacks failed: %s" %
            (detail[-8000:] or "no diagnostic"))


def callback_controls(context, phase):
    """Return registry-bound callback controls for one derived phase."""
    if phase not in _PHASES:
        raise AcceptanceError("unknown acceptance phase %r" % phase)
    # Control identity is completely represented by the derived plan.  The
    # executor kind is fixed by the id convention: authored criteria use the
    # ``.automated`` suffix; built-ins and observations never run callbacks.
    return tuple(identifier for identifier in context["controlPlan"][phase]
                 if identifier.endswith(".automated"))
