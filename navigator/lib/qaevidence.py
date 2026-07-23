"""Closed, shared validation for release-authoritative manual QA evidence.

The QA writer and the bundle verifier both use this module.  Keeping the
contract here prevents a structurally weak QA record from passing one stage
and becoming authoritative at a later stage.
"""

import copy
import re

from . import authority, canon


MANUAL_EVIDENCE_VERSION = "3"
MANUAL_QA_FIELDS = frozenset(("ac11", "ac12", "ac13", "ac15"))

_OUTER_FIELDS = frozenset((
    "status", "evidence", "operator", "operatorKind",
))
_TARGET_IDENTITY_FIELDS = frozenset(("browser", "os", "at", "mode"))
_TARGET_VERSION_FIELDS = frozenset((
    "browserVersion", "osVersion", "atVersion",
))
_AC11_CHECKS = frozenset((
    "keyboardTraversal", "activationKeys", "focusDeterminism",
    "scopedArrowKeys", "computedNameRoleState", "liveRegion",
))
_AC13_CHECKS = frozenset((
    "localFile", "minimumViewport", "stackedBelowMinimum",
))
_AC12_CHECKS = frozenset((
    "claimsReadable", "disclosureReadable", "disclaimerOnEveryPage",
    "legendOnEveryPage", "provenancePresent", "schedulePresent",
    "noContentClipping",
))
_TRAVERSAL_CHORDS = frozenset((
    "Tab/Shift-Tab", "Option-Tab/Option-Shift-Tab",
))
_BROWSER_REQUIREMENT_RE = re.compile(
    r"^(Chrome|Edge|Firefox|Safari) ≥ ([0-9]+)$")
_BROWSER_FAMILIES = frozenset(("Chrome", "Edge", "Firefox", "Safari"))
_BROWSER_ACTUAL_RE = re.compile(
    r"(Chrome|Edge|Firefox|Safari) (0|[1-9][0-9]*)"
    r"(?:\.(?:0|[1-9][0-9]*)){0,3}")
_MACOS_REQUIREMENT_RE = re.compile(r"^macOS ([0-9]+)\+$")
_MACOS_ACTUAL_RE = re.compile(
    r"macOS (0|[1-9][0-9]*)(?:\.(?:0|[1-9][0-9]*)){0,2}")
_WINDOWS_11_ACTUAL_RE = re.compile(r"Windows 11(?: [0-9]{2}H[12])?")
_OS_FAMILIES = frozenset(("macOS", "Windows"))
_AT_REQUIREMENT_RE = re.compile(r"^NVDA ([0-9]{4})\+$")
_AT_ACTUAL_RE = re.compile(
    r"NVDA ([1-9][0-9]{3})(?:\.(?:0|[1-9][0-9]*)){0,2}")
_PROBE_LEDGER_FIELDS = frozenset((
    "attempts", "resources", "cookieWrites", "webStorage", "indexedDB",
    "navigationMutations", "networkRequests",
))
def _nonblank(value):
    return isinstance(value, str) and bool(value.strip())


def _positive_integer(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _viewport(value):
    return isinstance(value, list) and len(value) == 2 and all(
        _positive_integer(dimension) for dimension in value)


def _passed_checks(value, expected, label):
    problems = []
    if not isinstance(value, dict) or set(value) != expected:
        return ["%s checks must be exactly %s" %
                (label, sorted(expected))]
    for check in sorted(expected):
        if value.get(check) != "passed":
            problems.append("%s check %s is not 'passed'" % (label, check))
    return problems


def _support_contract(support_matrix):
    """Return ``(targets, minimum)`` or defects for unusable live policy."""
    problems = []
    if not isinstance(support_matrix, dict):
        return [], None, ["current support matrix is unavailable"]
    targets = support_matrix.get("targets")
    if not isinstance(targets, list) or not targets:
        problems.append("current support matrix targets are unavailable")
        targets = []
    elif not all(isinstance(target, dict) and
                 set(target) == _TARGET_IDENTITY_FIELDS and
                 all(_nonblank(target.get(field))
                     for field in _TARGET_IDENTITY_FIELDS)
                 for target in targets):
        problems.append("current support matrix targets are malformed")
        targets = []
    elif len({tuple(target[field] for field in sorted(
            _TARGET_IDENTITY_FIELDS)) for target in targets}) != len(targets):
        problems.append("current support matrix targets contain duplicates")
        targets = []

    viewport = support_matrix.get("viewport")
    minimum = viewport.get("minimum") if isinstance(viewport, dict) else None
    if not isinstance(viewport, dict) or set(viewport) != {
            "minimum", "stackedBelowMinimum"} or \
            viewport.get("stackedBelowMinimum") is not True or \
            not _viewport(minimum):
        problems.append("current support matrix minimum viewport is malformed")
        minimum = None
    return targets, minimum, problems


def _probe_contract(api_probe_apis):
    if not isinstance(api_probe_apis, (list, tuple)) or \
            not api_probe_apis or \
            not all(_nonblank(api) for api in api_probe_apis) or \
            len(set(api_probe_apis)) != len(api_probe_apis):
        return [], ["current probed API names are unavailable or malformed"]
    return list(api_probe_apis), []


def _browser_requirement(value):
    match = _BROWSER_REQUIREMENT_RE.fullmatch(
        value if isinstance(value, str) else "")
    if match is None:
        return None
    return match.group(1), int(match.group(2))


def _os_requirement(value):
    macos = _MACOS_REQUIREMENT_RE.fullmatch(
        value if isinstance(value, str) else "")
    if macos is not None:
        return "macOS", int(macos.group(1))
    if value == "Windows 11":
        return "Windows", 11
    return None


def _actual_browser_version_problems(value, family, minimum, label):
    if not authority.is_identified_operator_identity(value):
        return ["%s has no actual browserVersion" % label]
    problems = []
    if not authority.is_final_evidence_text(value):
        problems.append("%s browserVersion contains pending or failure "
                        "language" % label)
    match = _BROWSER_ACTUAL_RE.fullmatch(value)
    if match is None:
        problems.append("%s browserVersion is not a canonical browser "
                        "product version" % label)
        return problems
    actual_family = match.group(1)
    actual_major = int(match.group(2))
    if actual_family != family:
        problems.append("%s browserVersion does not identify %s" %
                        (label, family))
    if actual_major < minimum:
        problems.append("%s browserVersion is below %s ≥ %d" %
                        (label, family, minimum))
    if family == "Safari" and actual_major > 99:
        problems.append("%s browserVersion does not identify a Safari "
                        "product version" % label)
    return problems


def _actual_os_version_problems(value, family, minimum, label):
    if not authority.is_identified_operator_identity(value):
        return ["%s has no actual osVersion" % label]
    problems = []
    if not authority.is_final_evidence_text(value):
        problems.append("%s osVersion contains pending or failure language"
                        % label)
    if family == "macOS":
        match = _MACOS_ACTUAL_RE.fullmatch(value)
        if match is None:
            problems.append("%s osVersion is not a canonical macOS version"
                            % label)
        else:
            actual_major = int(match.group(1))
            if actual_major < minimum:
                problems.append("%s osVersion is below macOS %d+" %
                                (label, minimum))
            if actual_major > 99:
                problems.append("%s osVersion is not a credible macOS product "
                                "version" % label)
    elif family == "Windows":
        if minimum != 11 or _WINDOWS_11_ACTUAL_RE.fullmatch(value) is None:
            problems.append("%s osVersion is not a canonical Windows 11 "
                            "version" % label)
    else:
        problems.append("%s has an unsupported OS requirement" % label)
    return problems


def _actual_at_version_problems(value, expected, label):
    if expected == "none":
        return [] if value is None else [
            "%s atVersion must be null when at is 'none'" % label]
    requirement = _AT_REQUIREMENT_RE.fullmatch(
        expected if isinstance(expected, str) else "")
    if requirement is None:
        return ["%s has an unsupported AT requirement" % label]
    if not authority.is_identified_operator_identity(value):
        return ["%s has no actual atVersion" % label]
    problems = []
    if not authority.is_final_evidence_text(value):
        problems.append("%s atVersion contains pending or failure language"
                        % label)
    match = _AT_ACTUAL_RE.fullmatch(value)
    if match is None:
        problems.append("%s atVersion is not a canonical NVDA product "
                        "version" % label)
    elif int(match.group(1)) < int(requirement.group(1)):
        problems.append("%s atVersion is below %s" % (label, expected))
    return problems


def _target_version_problems(result, expected, label):
    problems = []
    actual_identity = {
        field: result.get(field) for field in _TARGET_IDENTITY_FIELDS
    }
    if actual_identity != expected:
        problems.append("%s target does not match the current support matrix"
                        % label)
    browser = _browser_requirement(expected.get("browser"))
    if browser is None:
        problems.append("%s has an unsupported browser requirement" % label)
    else:
        problems.extend(_actual_browser_version_problems(
            result.get("browserVersion"), browser[0], browser[1], label))
    operating_system = _os_requirement(expected.get("os"))
    if operating_system is None:
        problems.append("%s has an unsupported OS requirement" % label)
    else:
        problems.extend(_actual_os_version_problems(
            result.get("osVersion"), operating_system[0],
            operating_system[1], label))
    problems.extend(_actual_at_version_problems(
        result.get("atVersion"), expected.get("at"), label))
    return problems


def _environment_problems(result, targets, label):
    """Validate a print/probe environment against a current no-AT target."""
    problems = []
    browser = result.get("browser")
    operating_system = result.get("os")
    if browser not in _BROWSER_FAMILIES:
        problems.append("%s browser is not a known browser family" % label)
    if operating_system not in _OS_FAMILIES:
        problems.append("%s os is not a known OS family" % label)
    for field in ("browser", "os"):
        value = result.get(field)
        if authority.is_identified_operator_identity(value) and \
                not authority.is_final_evidence_text(value):
            problems.append("%s %s contains pending or failure language" %
                            (label, field))

    matching = []
    browser_policies = set()
    os_policies = set()
    for target in targets:
        browser_requirement = _browser_requirement(target.get("browser"))
        os_requirement = _os_requirement(target.get("os"))
        if target.get("at") != "none" or not browser_requirement or \
                not os_requirement:
            continue
        if browser_requirement[0] == browser:
            browser_policies.add(browser_requirement)
        if os_requirement[0] == operating_system:
            os_policies.add(os_requirement)
        if browser_requirement[0] == browser and \
                os_requirement[0] == operating_system:
            matching.append((browser_requirement, os_requirement))
    if len(matching) != 1:
        problems.append("%s browser/OS pair is not exactly one current no-AT "
                        "support target" % label)
    if len(browser_policies) == 1:
        browser_requirement = next(iter(browser_policies))
        problems.extend(_actual_browser_version_problems(
            result.get("browserVersion"), browser_requirement[0],
            browser_requirement[1], label))
    elif browser in _BROWSER_FAMILIES:
        problems.append("%s browser has no unambiguous current no-AT version "
                        "policy" % label)
    if len(os_policies) == 1:
        os_requirement = next(iter(os_policies))
        problems.extend(_actual_os_version_problems(
            result.get("osVersion"), os_requirement[0], os_requirement[1],
            label))
    elif operating_system in _OS_FAMILIES:
        problems.append("%s os has no unambiguous current no-AT version policy"
                        % label)
    return problems


def _ac11_problems(evidence, targets):
    results = evidence.get("targetResults")
    if not isinstance(results, list):
        return ["ac11 targetResults is not an array"]
    if len(results) != len(targets):
        return ["ac11 targetResults must cover every current support target "
                "exactly once in matrix order"]
    expected_fields = _TARGET_IDENTITY_FIELDS | _TARGET_VERSION_FIELDS | {
        "traversalChord", "traversalConfiguration", "checks",
    }
    problems = []
    for index, (result, target) in enumerate(zip(results, targets)):
        label = "ac11 targetResults[%d]" % index
        if not isinstance(result, dict) or set(result) != expected_fields:
            problems.append("%s has the wrong fields" % label)
            continue
        problems.extend(_target_version_problems(result, target, label))
        if result.get("traversalChord") not in _TRAVERSAL_CHORDS:
            problems.append("%s traversalChord must be one of %s" %
                            (label, sorted(_TRAVERSAL_CHORDS)))
        configuration = result.get("traversalConfiguration")
        if not authority.is_identified_operator_identity(configuration):
            problems.append("%s has no traversalConfiguration" % label)
        elif not authority.is_final_evidence_text(configuration):
            problems.append("%s traversalConfiguration contains pending or "
                            "failure language" % label)
        is_safari_macos = target.get("browser", "").startswith("Safari ") and \
            target.get("os", "").startswith("macOS ")
        if not is_safari_macos and result.get(
                "traversalChord") != "Tab/Shift-Tab":
            problems.append("%s must use Tab/Shift-Tab outside Safari/macOS"
                            % label)
        if is_safari_macos and authority.is_final_evidence_text(configuration):
            folded = configuration.casefold()
            if "keyboard navigation" not in folded and not (
                    "safari" in folded and "setting" in folded):
                problems.append("%s traversalConfiguration must explain the "
                                "Keyboard Navigation or Safari setting" %
                                label)
        problems.extend(_passed_checks(
            result.get("checks"), _AC11_CHECKS, label))
    return problems


def _ac13_problems(evidence, targets, minimum):
    results = evidence.get("targetResults")
    if not isinstance(results, list):
        return ["ac13 targetResults is not an array"]
    if len(results) != len(targets):
        return ["ac13 targetResults must cover every current support target "
                "exactly once in matrix order"]
    expected_fields = _TARGET_IDENTITY_FIELDS | _TARGET_VERSION_FIELDS | {
        "minimumViewport", "stackedViewport", "checks",
    }
    problems = []
    for index, (result, target) in enumerate(zip(results, targets)):
        label = "ac13 targetResults[%d]" % index
        if not isinstance(result, dict) or set(result) != expected_fields:
            problems.append("%s has the wrong fields" % label)
            continue
        problems.extend(_target_version_problems(result, target, label))
        if result.get("minimumViewport") != minimum:
            problems.append("%s minimumViewport does not match the current "
                            "support matrix" % label)
        stacked = result.get("stackedViewport")
        if not _viewport(stacked):
            problems.append("%s stackedViewport must contain two positive "
                            "integer dimensions" % label)
        elif minimum is not None and not (
                stacked[0] < minimum[0] or stacked[1] < minimum[1]):
            problems.append("%s stackedViewport is not below the current "
                            "minimum on either dimension" % label)
        problems.extend(_passed_checks(
            result.get("checks"), _AC13_CHECKS, label))
    return problems


def _ac12_problems(evidence, targets):
    result = evidence.get("printResult")
    expected_fields = frozenset((
        "browser", "browserVersion", "os", "osVersion", "pageCount",
        "checks",
    ))
    if not isinstance(result, dict) or set(result) != expected_fields:
        return ["ac12 printResult has the wrong fields"]
    problems = []
    problems.extend(_environment_problems(
        result, targets, "ac12 printResult"))
    if not _positive_integer(result.get("pageCount")):
        problems.append("ac12 printResult pageCount is not a positive integer")
    problems.extend(_passed_checks(
        result.get("checks"), _AC12_CHECKS, "ac12 printResult"))
    return problems


def _ac15_problems(evidence, api_probe_apis, targets):
    result = evidence.get("probeResult")
    expected_fields = frozenset((
        "browser", "browserVersion", "os", "osVersion", "ready", "apis",
    )) | _PROBE_LEDGER_FIELDS
    if not isinstance(result, dict) or set(result) != expected_fields:
        return ["ac15 probeResult has the wrong fields"]
    problems = []
    problems.extend(_environment_problems(
        result, targets, "ac15 probeResult"))
    if result.get("ready") is not True:
        problems.append("ac15 probeResult ready is not true")
    apis = result.get("apis")
    if not isinstance(apis, dict) or set(apis) != set(api_probe_apis):
        problems.append("ac15 probeResult APIs do not exactly match the "
                        "current probed hooks")
    else:
        installed = {"status": "installed", "error": None, "detail": None}
        for api in sorted(api_probe_apis):
            if apis.get(api) != installed:
                problems.append("ac15 probeResult API %s is not an exact "
                                "installed result" % api)
    for field in sorted(_PROBE_LEDGER_FIELDS):
        if result.get(field) != []:
            problems.append("ac15 probeResult %s ledger is not exactly empty"
                            % field)
    return problems


def pending_manual_checks_template(support_matrix, api_probe_apis):
    """Return an exact-shape, deliberately non-authorizing v3 skeleton.

    Live policy identities are copied to prevent transcription drift.  Every
    operator-performed result remains pending, blank, false, zero, or null, so
    the template cannot pass :func:`manual_check_problems` without deliberate
    review input.  Approval identities are never part of the input template;
    ``record-qa`` injects its explicit environment identity only after review.
    """
    targets, minimum, support_problems = _support_contract(support_matrix)
    api_names, api_problems = _probe_contract(api_probe_apis)
    problems = support_problems + api_problems
    if problems:
        raise ValueError("cannot derive manual-QA template: %s" %
                         "; ".join(problems))

    ac11_results = []
    ac13_results = []
    for target in targets:
        versions = {
            "browserVersion": "",
            "osVersion": "",
            "atVersion": None if target["at"] == "none" else "",
        }
        ac11_result = copy.deepcopy(target)
        ac11_result.update(versions)
        ac11_result.update({
            "traversalChord": "",
            "traversalConfiguration": "",
            "checks": {
                check: "pending" for check in sorted(_AC11_CHECKS)
            },
        })
        ac11_results.append(ac11_result)

        ac13_result = copy.deepcopy(target)
        ac13_result.update(versions)
        ac13_result.update({
            "minimumViewport": copy.deepcopy(minimum),
            "stackedViewport": [0, 0],
            "checks": {
                check: "pending" for check in sorted(_AC13_CHECKS)
            },
        })
        ac13_results.append(ac13_result)

    common = {"status": "pending", "evidence": ""}
    return {
        "ac11": dict(common, targetResults=ac11_results),
        "ac12": dict(common, printResult={
            "browser": "", "browserVersion": "",
            "os": "", "osVersion": "", "pageCount": 0,
            "checks": {
                check: "pending" for check in sorted(_AC12_CHECKS)
            },
        }),
        "ac13": dict(common, targetResults=ac13_results),
        "ac15": dict(common, probeResult={
            "browser": "", "browserVersion": "",
            "os": "", "osVersion": "", "ready": False,
            "apis": {
                api: {"status": "pending", "error": None, "detail": None}
                for api in sorted(api_names)
            },
            "attempts": None, "resources": None, "cookieWrites": None,
            "webStorage": None, "indexedDB": None,
            "navigationMutations": None, "networkRequests": None,
        }),
    }


def manual_check_problems(checks, required_fields, *, support_matrix,
                          api_probe_apis, operator=None, operator_kind=None,
                          manual_evidence_version=None):
    """Validate the complete versioned manual-QA authorization contract."""
    problems = []
    problems.extend(canon.require_version(
        {"manualEvidenceVersion": manual_evidence_version},
        "manualEvidenceVersion", MANUAL_EVIDENCE_VERSION))
    if not isinstance(checks, dict):
        return problems + ["manualChecks is not an object"]

    try:
        required = set(required_fields)
    except TypeError:
        return problems + ["required manual QA fields are malformed"]
    if required != MANUAL_QA_FIELDS:
        problems.append("required manual QA fields must be exactly %s" %
                        sorted(MANUAL_QA_FIELDS))
    actual = set(checks)
    if actual != required:
        missing = sorted(required - actual)
        extra = sorted(actual - required)
        if missing:
            problems.append("manual checks missing %s" % missing)
        if extra:
            problems.append("manual checks contain unknown fields %s" % extra)

    targets, minimum, support_problems = _support_contract(support_matrix)
    api_names, api_problems = _probe_contract(api_probe_apis)
    problems.extend(support_problems)
    problems.extend(api_problems)

    field_extras = {
        "ac11": frozenset(("targetResults",)),
        "ac12": frozenset(("printResult",)),
        "ac13": frozenset(("targetResults",)),
        "ac15": frozenset(("probeResult",)),
    }
    for field in sorted(actual & required):
        evidence = checks[field]
        if not isinstance(evidence, dict):
            problems.append("%s evidence is not a structured object" % field)
            continue
        if set(evidence) != _OUTER_FIELDS | field_extras[field]:
            problems.append("%s evidence has the wrong fields" % field)
            continue
        if evidence.get("status") != "passed":
            problems.append("%s status is not 'passed'" % field)
        text = evidence.get("evidence")
        if not authority.is_identified_operator_identity(text):
            problems.append("%s has no evidence text" % field)
        elif not authority.is_final_evidence_text(text):
            problems.append("%s evidence contains pending or failure language"
                            % field)
        evidence_operator = evidence.get("operator")
        evidence_kind = evidence.get("operatorKind")
        if not authority.is_identified_operator_identity(evidence_operator):
            problems.append("%s has no identified operator" % field)
        elif operator is not None and evidence_operator != operator:
            problems.append("%s operator does not match the QA approver" %
                            field)
        if not authority.is_authoritative_operator_kind(evidence_kind):
            problems.append("%s operatorKind is not release-authoritative" %
                            field)
        elif operator_kind is not None and evidence_kind != operator_kind:
            problems.append("%s operatorKind does not match the QA approver" %
                            field)

        if field == "ac11":
            problems.extend(_ac11_problems(evidence, targets))
        elif field == "ac12":
            problems.extend(_ac12_problems(evidence, targets))
        elif field == "ac13":
            problems.extend(_ac13_problems(evidence, targets, minimum))
        elif field == "ac15":
            problems.extend(_ac15_problems(evidence, api_names, targets))
    return problems
