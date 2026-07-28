"""Current navigator acceptance registry and ephemeral result projection."""

from __future__ import annotations

import importlib
import os

from . import canon


ACCEPTANCE_PATH = "navigator/schema/acceptance.json"
CONTRACT_PATH = (
    "contracts/30-product-generation/claims-navigator/"
    "acceptance-criteria_DRAFT.md"
)
PRIOR_ACCEPTANCE_PATH = "navigator/schema/prior-art-acceptance.json"
PRIOR_CONTRACT_PATH = (
    "contracts/30-product-generation/claims-prior-art-navigator/"
    "acceptance-criteria_DRAFT.md"
)
MAP_ACCEPTANCE_PATH = "navigator/schema/prior-art-map-acceptance.json"
MAP_CONTRACT_PATH = (
    "contracts/20-semantic-relations/claim-prior-art-passage-map/"
    "acceptance-criteria_DRAFT.md"
)
SPEC_CRITERIA = tuple("AC-%02d" % number for number in range(1, 21))
MAP_CRITERIA = tuple("PAM-AC-%02d" % number for number in range(1, 11))
PRIOR_CRITERIA = tuple("PA-AC-%02d" % number for number in range(1, 18))
CRITERIA = SPEC_CRITERIA + MAP_CRITERIA + PRIOR_CRITERIA
TEST_COVERAGE = {
    "navigator.tests.test_canon": frozenset({"AC-15", "AC-16"}),
    "navigator.tests.test_current_pipeline": frozenset({
        "AC-01", "AC-05", "AC-15", "AC-16", "AC-18", "AC-19", "AC-20",
    }),
    "navigator.tests.test_render_current": frozenset({
        "AC-02", "AC-03", "AC-04", "AC-06", "AC-07", "AC-08", "AC-09",
        "AC-10", "AC-11", "AC-12", "AC-13", "AC-14", "AC-15", "AC-17",
        "AC-18",
    }),
    "navigator.tests.test_xml_model": frozenset({
        "AC-01", "AC-02", "AC-03", "AC-04", "AC-05", "AC-06", "AC-07",
        "AC-08", "AC-18",
    }),
    "navigator.tests.test_prior_art": frozenset(
        MAP_CRITERIA + PRIOR_CRITERIA),
}

_SCOPES = {
    **{"AC-%02d" % number: "edition" for number in range(1, 19)},
    "AC-19": "shared",
    "AC-20": "bundle",
    **{"PAM-AC-%02d" % number: "semantic"
       for number in range(1, 11)},
    **{"PA-AC-%02d" % number: "product"
       for number in range(1, 13)},
    "PA-AC-13": "shared",
    "PA-AC-14": "product",
    "PA-AC-15": "bundle",
    "PA-AC-16": "product",
    "PA-AC-17": "shared",
}


class AcceptanceError(ValueError):
    """The current executable acceptance contract is malformed or failed."""


def _resolve_enforcer(path):
    """Resolve one exact dotted implementation symbol without aliases."""
    if not isinstance(path, str) or not path or any(
            not part or not part.replace("_", "a").isalnum()
            for part in path.split(".")):
        raise AcceptanceError("acceptance enforcer path is malformed")
    parts = path.split(".")
    for boundary in range(len(parts), 0, -1):
        try:
            value = importlib.import_module(".".join(parts[:boundary]))
        except ImportError:
            continue
        try:
            for part in parts[boundary:]:
                value = getattr(value, part)
        except AttributeError as exc:
            raise AcceptanceError(
                "acceptance enforcer symbol is absent: %s" % path) from exc
        if not callable(value):
            raise AcceptanceError(
                "acceptance enforcer is not executable: %s" % path)
        return value
    raise AcceptanceError("acceptance enforcer module is absent: %s" % path)


def validate_registry(value):
    identifiers = ([entry.get("id") for entry in value.get("criteria", [])]
                   if isinstance(value, dict) and
                   isinstance(value.get("criteria"), list) else [])
    if identifiers[:1] == ["AC-01"]:
        expected_criteria = SPEC_CRITERIA
        expected_version = "6"
    elif identifiers[:1] == ["PAM-AC-01"]:
        expected_criteria = MAP_CRITERIA
        expected_version = "2"
    else:
        expected_criteria = PRIOR_CRITERIA
        expected_version = "2"
    if not isinstance(value, dict) or set(value) != {
            "acceptanceVersion", "criteria"} or \
            value.get("acceptanceVersion") != expected_version:
        raise AcceptanceError(
            "acceptance registry shape/version is not current")
    criteria = value.get("criteria")
    if not isinstance(criteria, list) or len(criteria) != len(expected_criteria) or \
            [entry.get("id") for entry in criteria
             if isinstance(entry, dict)] != list(expected_criteria):
        raise AcceptanceError("acceptance criterion census/order is not exact")
    for criterion in criteria:
        if not isinstance(criterion, dict) or set(criterion) != {
                "enforcer", "id", "outcome", "scope"}:
            raise AcceptanceError("acceptance criterion shape is malformed")
        identifier = criterion["id"]
        outcome = criterion["outcome"]
        enforcer = criterion["enforcer"]
        covering_modules = {
            module for module, identifiers in TEST_COVERAGE.items()
            if identifier in identifiers
        }
        enforcer_parts = enforcer.split("; ") if isinstance(enforcer, str) else []
        if criterion["scope"] != _SCOPES[identifier] or \
                not isinstance(outcome, str) or not outcome.strip() or \
                outcome != outcome.strip() or \
                not isinstance(enforcer, str) or not enforcer.strip() or \
                enforcer != enforcer.strip() or len(enforcer_parts) != 2 or \
                enforcer_parts[1] not in covering_modules:
            raise AcceptanceError(
                "acceptance criterion %s is malformed" % identifier)
        _resolve_enforcer(enforcer_parts[0])
    return value


def _load_one(root, registry_path, contract_path, table_start,
              table_end, byte_source=None):
    absolute = os.path.join(root, *registry_path.split("/"))
    try:
        if byte_source is None:
            with open(absolute, "rb") as handle:
                data = handle.read()
        else:
            data = byte_source(absolute)
    except (OSError, KeyError) as exc:
        raise AcceptanceError("acceptance registry is unreadable") from exc
    try:
        value = canon.parse_json(data)
    except (ValueError, canon.CanonError) as exc:
        raise AcceptanceError("acceptance registry is not strict JSON") from exc
    if data != canon.canonical_json(value) + b"\n":
        raise AcceptanceError("acceptance registry bytes are not canonical")
    registry = validate_registry(value)
    contract_absolute = os.path.join(root, *contract_path.split("/"))
    try:
        if byte_source is None:
            with open(contract_absolute, "rb") as handle:
                contract_data = handle.read()
        else:
            contract_data = byte_source(contract_absolute)
        contract = contract_data.decode("utf-8")
    except (OSError, KeyError, UnicodeDecodeError) as exc:
        raise AcceptanceError("acceptance contract is unreadable") from exc
    start = table_start + "\n"
    end = table_end
    if contract.count(start) != 1 or contract.count(end) != 1 or \
            contract.split(start, 1)[1].split(end, 1)[0] != \
            render_table(registry):
        raise AcceptanceError(
            "acceptance contract and registry text differ")
    return registry


def load_registry(root, byte_source=None):
    return _load_one(
        root, ACCEPTANCE_PATH, CONTRACT_PATH,
        "<!-- NAV-AC-TABLE:START -->",
        "<!-- NAV-AC-TABLE:END -->", byte_source)


def load_registries(root, byte_source=None):
    return (
        load_registry(root, byte_source),
        _load_one(
            root, MAP_ACCEPTANCE_PATH, MAP_CONTRACT_PATH,
            "<!-- PA-MAP-AC-TABLE:START -->",
            "<!-- PA-MAP-AC-TABLE:END -->", byte_source),
        _load_one(
            root, PRIOR_ACCEPTANCE_PATH, PRIOR_CONTRACT_PATH,
            "<!-- PA-NAV-AC-TABLE:START -->",
            "<!-- PA-NAV-AC-TABLE:END -->", byte_source),
    )


def render_table(registry):
    validate_registry(registry)
    lines = [
        "| ID | Scope | Executable technical outcome | Independent enforcer |",
        "|---|---|---|---|",
    ]
    for criterion in registry["criteria"]:
        outcome = criterion["outcome"].replace("|", "\\|").replace("\n", " ")
        enforcer = criterion["enforcer"].replace("|", "\\|").replace("\n", " ")
        lines.append("| **%s** | %s | %s | %s |" % (
            criterion["id"], criterion["scope"], outcome, enforcer))
    return "\n".join(lines) + "\n"


def passed_result(registries, test_modules):
    """Create ephemeral technical status after the named current checks pass.

    The result deliberately carries no identity, timestamp, signature, source
    digest, or authorization semantics.  Its only lifetime is the invoking
    validation process.
    """
    registries = tuple(registries)
    if len(registries) != 3:
        raise AcceptanceError(
            "ephemeral acceptance requires all current registries")
    for registry in registries:
        validate_registry(registry)
    modules = tuple(test_modules)
    if len(modules) != len(set(modules)) or \
            set(modules) != set(TEST_COVERAGE):
        raise AcceptanceError(
            "ephemeral acceptance result lacks an exact test-module census")
    passed = set().union(*(TEST_COVERAGE[module] for module in modules))
    if passed != set(CRITERIA) or \
            any(not coverage for coverage in TEST_COVERAGE.values()):
        raise AcceptanceError(
            "registered test coverage does not cover the exact criterion set")
    return {
        "acceptanceResultVersion": "1",
        "status": "passed",
        "results": [
            {"id": identifier, "status": "passed"}
            for identifier in CRITERIA
        ],
    }
