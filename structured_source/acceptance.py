"""Executable SSM acceptance registry and deterministic table projection."""

from __future__ import annotations

import importlib
import os
import re

from .control import canonical_json, parse_json
from .errors import StructuredSourceError

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY_PATH = "structured_source/registry/acceptance.json"
CRITERIA = tuple("SSM-AC-%02d" % number for number in range(1, 11))
TEST_MODULES = (
    "structured_source.tests.test_acceptance",
    "structured_source.tests.test_atomic",
    "structured_source.tests.test_conversion",
    "structured_source.tests.test_registry",
    "structured_source.tests.test_xml_contract",
)

_ID = re.compile(r"SSM-AC-(0[1-9]|10)\Z")
_REGISTRY_FIELDS = {"acceptanceVersion", "namespace", "runner", "criteria"}
_RUNNER_FIELDS = {
    "runnerVersion", "callbackModule", "testModules", "testCriteria",
}
_CRITERION_FIELDS = {"id", "code", "outcome", "evidence", "callbacks"}


def validate_registry(value):
    if not isinstance(value, dict) or set(value) != _REGISTRY_FIELDS or \
            value.get("acceptanceVersion") != "1" or \
            value.get("namespace") != "ssp":
        raise StructuredSourceError(
            "acceptance registry shape/version is not current")
    runner = value.get("runner")
    if not isinstance(runner, dict) or set(runner) != _RUNNER_FIELDS or \
            runner.get("runnerVersion") != "1" or \
            runner.get("callbackModule") != \
            "structured_source.acceptance_callbacks" or \
            runner.get("testModules") != list(TEST_MODULES):
        raise StructuredSourceError("acceptance runner is malformed")
    test_criteria = runner.get("testCriteria")
    if not isinstance(test_criteria, dict) or \
            set(test_criteria) != set(TEST_MODULES):
        raise StructuredSourceError(
            "acceptance test criterion declarations are incomplete")
    covered = set()
    for module in TEST_MODULES:
        codes = test_criteria[module]
        if not isinstance(codes, list) or not codes or \
                codes != sorted(set(codes)) or not set(codes).issubset(CRITERIA):
            raise StructuredSourceError(
                "registered test has no exact nonempty criterion set")
        covered.update(codes)
    if covered != set(CRITERIA):
        raise StructuredSourceError(
            "registered tests do not cover every acceptance criterion")

    criteria = value.get("criteria")
    if not isinstance(criteria, list) or \
            [entry.get("code") for entry in criteria
             if isinstance(entry, dict)] != list(CRITERIA):
        raise StructuredSourceError("acceptance criterion census is not exact")
    callback_names = []
    for criterion in criteria:
        if not isinstance(criterion, dict) or \
                set(criterion) != _CRITERION_FIELDS or \
                _ID.fullmatch(criterion.get("code", "")) is None or \
                not criterion.get("id", "").startswith(
                    criterion["code"] + " — ") or \
                not all(isinstance(criterion.get(field), str) and
                        criterion[field].strip()
                        for field in ("outcome", "evidence")):
            raise StructuredSourceError("acceptance criterion is malformed")
        callbacks = criterion.get("callbacks")
        prefix = "ssp.%s." % criterion["code"]
        if not isinstance(callbacks, list) or len(callbacks) != 1 or \
                not isinstance(callbacks[0], str) or \
                not callbacks[0].startswith(prefix):
            raise StructuredSourceError(
                "%s must own exactly one callback" % criterion["code"])
        callback_names.extend(callbacks)
    if len(callback_names) != len(set(callback_names)):
        raise StructuredSourceError("an acceptance callback has multiple owners")
    module = importlib.import_module(runner["callbackModule"])
    available = getattr(module, "CALLBACKS", None)
    if not isinstance(available, dict) or \
            set(available) != set(callback_names) or \
            not all(callable(callback) for callback in available.values()):
        raise StructuredSourceError(
            "acceptance callback census is not bidirectionally closed")
    return value


def load_registry(root=ROOT, byte_source=None):
    absolute = os.path.join(root, *REGISTRY_PATH.split("/"))
    try:
        if byte_source:
            data = byte_source(absolute)
        else:
            with open(absolute, "rb") as handle:
                data = handle.read()
    except (OSError, KeyError) as exc:
        raise StructuredSourceError("acceptance registry is unreadable") from exc
    value = validate_registry(parse_json(data))
    if data != canonical_json(value):
        raise StructuredSourceError("acceptance registry bytes are not canonical")
    return value


def render_table(registry):
    validate_registry(registry)
    rows = [
        "| ID | Required outcome | Required evidence and enforcer |",
        "|---|---|---|",
    ]
    for criterion in registry["criteria"]:
        outcome = criterion["outcome"].replace("|", "\\|").replace("\n", " ")
        evidence = criterion["evidence"].replace("|", "\\|").replace("\n", " ")
        rows.append("| **%s** | %s | %s |" %
                    (criterion["id"], outcome, evidence))
    return "\n".join(rows) + "\n"
