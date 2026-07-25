"""Executable recurring acceptance registry and deterministic table view."""

from __future__ import annotations

import importlib
import os
import re

from .control import parse_json
from .errors import StructuredSourceError

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY_PATH = "structured_source/registry/acceptance.json"
CRITERIA = tuple("SSM-AC-%02d" % number for number in range(1, 11))
TEST_MODULES = (
    "structured_source.tests.test_acceptance",
    "structured_source.tests.test_approvals",
    "structured_source.tests.test_atomic",
    "structured_source.tests.test_exporter",
    "structured_source.tests.test_projection",
    "structured_source.tests.test_xml_contract",
)
_ID = re.compile(r"SSM-AC-(0[1-9]|10)\Z")
_REGISTRY_FIELDS = {"acceptanceVersion", "namespace", "runner", "criteria"}
_RUNNER_FIELDS = {"runnerVersion", "callbackModule", "testModules"}
_CRITERION_FIELDS = {"id", "code", "outcome", "evidence", "callbacks"}


def load_registry(root=ROOT, byte_source=None):
    path = os.path.join(root, *REGISTRY_PATH.split("/"))
    try:
        if byte_source:
            data = byte_source(path)
        else:
            with open(path, "rb") as handle:
                data = handle.read()
    except OSError as exc:
        raise StructuredSourceError("acceptance registry is unreadable: %s" % exc) from exc
    return validate_registry(parse_json(data))


def validate_registry(value):
    if not isinstance(value, dict) or set(value) != _REGISTRY_FIELDS or \
            value.get("acceptanceVersion") != "1" or value.get("namespace") != "ssp":
        raise StructuredSourceError("acceptance registry shape/version is not current")
    runner = value.get("runner")
    if not isinstance(runner, dict) or set(runner) != _RUNNER_FIELDS or \
            runner.get("runnerVersion") != "1" or \
            not isinstance(runner.get("callbackModule"), str) or \
            not runner["callbackModule"].startswith("structured_source."):
        raise StructuredSourceError("acceptance runner is malformed")
    modules = runner.get("testModules")
    if modules != list(TEST_MODULES):
        raise StructuredSourceError("acceptance test-module census is not exact")
    criteria = value.get("criteria")
    if not isinstance(criteria, list) or \
            [item.get("code") for item in criteria if isinstance(item, dict)] != list(CRITERIA):
        raise StructuredSourceError("acceptance criterion census is not exact")
    callbacks = []
    for criterion in criteria:
        if not isinstance(criterion, dict) or set(criterion) != _CRITERION_FIELDS or \
                _ID.fullmatch(criterion.get("code", "")) is None or \
                not criterion.get("id", "").startswith(criterion["code"] + " — ") or \
                not all(isinstance(criterion.get(field), str) and
                        criterion[field].strip() for field in ("outcome", "evidence")):
            raise StructuredSourceError("acceptance criterion is malformed")
        owned = criterion.get("callbacks")
        prefix = "ssp.%s." % criterion["code"]
        if not isinstance(owned, list) or not owned or owned != sorted(set(owned)) or \
                not all(isinstance(item, str) and item.startswith(prefix)
                        for item in owned):
            raise StructuredSourceError(
                "%s callback ownership is malformed" % criterion["code"])
        callbacks.extend(owned)
    if len(callbacks) != len(set(callbacks)):
        raise StructuredSourceError("an acceptance callback has multiple owners")
    module = importlib.import_module(runner["callbackModule"])
    available = getattr(module, "CALLBACKS", None)
    if not isinstance(available, dict) or set(available) != set(callbacks) or \
            not all(callable(value) for value in available.values()):
        raise StructuredSourceError("acceptance callback census is not bidirectionally closed")
    return value


def render_table(registry) -> str:
    validate_registry(registry)
    rows = ["| ID | Required outcome | Required evidence and enforcer |",
            "|---|---|---|"]
    for criterion in registry["criteria"]:
        outcome = criterion["outcome"].replace("|", "\\|").replace("\n", " ")
        evidence = criterion["evidence"].replace("|", "\\|").replace("\n", " ")
        rows.append("| **%s** | %s | %s |" %
                    (criterion["id"], outcome, evidence))
    return "\n".join(rows) + "\n"
