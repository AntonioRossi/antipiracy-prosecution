"""Current navigator acceptance registry and ephemeral result projection."""

from __future__ import annotations

import os

from . import canon


ACCEPTANCE_PATH = "navigator/schema/acceptance.json"
CONTRACT_PATH = "AA11393US-claims-navigator_acceptance-criteria_DRAFT.md"
CRITERIA = tuple("AC-%02d" % number for number in range(1, 21))
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
}

_SCOPES = {
    **{"AC-%02d" % number: "edition" for number in range(1, 19)},
    "AC-19": "shared",
    "AC-20": "bundle",
}


class AcceptanceError(ValueError):
    """The current executable acceptance contract is malformed or failed."""


def validate_registry(value):
    if not isinstance(value, dict) or set(value) != {
            "acceptanceVersion", "criteria"} or \
            value.get("acceptanceVersion") != "4":
        raise AcceptanceError(
            "acceptance registry shape/version is not current")
    criteria = value.get("criteria")
    if not isinstance(criteria, list) or len(criteria) != len(CRITERIA) or \
            [entry.get("id") for entry in criteria
             if isinstance(entry, dict)] != list(CRITERIA):
        raise AcceptanceError("acceptance criterion census/order is not exact")
    for criterion in criteria:
        if not isinstance(criterion, dict) or set(criterion) != {
                "id", "scope", "text"}:
            raise AcceptanceError("acceptance criterion shape is malformed")
        identifier = criterion["id"]
        text = criterion["text"]
        if criterion["scope"] != _SCOPES[identifier] or \
                not isinstance(text, str) or not text.strip() or \
                text != text.strip():
            raise AcceptanceError(
                "acceptance criterion %s is malformed" % identifier)
    return value


def load_registry(root, byte_source=None):
    absolute = os.path.join(root, *ACCEPTANCE_PATH.split("/"))
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
    contract_absolute = os.path.join(root, *CONTRACT_PATH.split("/"))
    try:
        if byte_source is None:
            with open(contract_absolute, "rb") as handle:
                contract_data = handle.read()
        else:
            contract_data = byte_source(contract_absolute)
        contract = contract_data.decode("utf-8")
    except (OSError, KeyError, UnicodeDecodeError) as exc:
        raise AcceptanceError("acceptance contract is unreadable") from exc
    start = "<!-- NAV-AC-TABLE:START -->\n"
    end = "<!-- NAV-AC-TABLE:END -->"
    if contract.count(start) != 1 or contract.count(end) != 1 or \
            contract.split(start, 1)[1].split(end, 1)[0] != \
            render_table(registry):
        raise AcceptanceError(
            "acceptance contract and registry text differ")
    return registry


def render_table(registry):
    validate_registry(registry)
    lines = [
        "| ID | Scope | Required outcome |",
        "|---|---|---|",
    ]
    for criterion in registry["criteria"]:
        text = criterion["text"].replace("|", "\\|").replace("\n", " ")
        lines.append("| **%s** | %s | %s |" % (
            criterion["id"], criterion["scope"], text))
    return "\n".join(lines) + "\n"


def passed_result(registry, test_modules):
    """Create non-persistent evidence after the named current checks pass.

    The result deliberately carries no identity, timestamp, signature, source
    digest, or authorization semantics.  Its only lifetime is the invoking
    validation process.
    """
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
        "status": "conformant",
        "results": [
            {"id": identifier, "status": "passed"}
            for identifier in CRITERIA
        ],
    }
