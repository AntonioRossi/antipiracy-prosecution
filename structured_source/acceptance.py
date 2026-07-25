"""Data-only SSM acceptance registry and deterministic table projection."""

from __future__ import annotations

import os
import re

from .control import canonical_json, parse_json
from .errors import StructuredSourceError

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY_PATH = "structured_source/registry/acceptance.json"
CRITERIA = tuple("SSM-AC-%02d" % number for number in range(1, 11))
_ID = re.compile(r"SSM-AC-(0[1-9]|10)\Z")
_REGISTRY_FIELDS = {"acceptanceVersion", "criteria"}
_CRITERION_FIELDS = {"id", "code", "outcome", "evidence"}


def validate_registry(value):
    if not isinstance(value, dict) or set(value) != _REGISTRY_FIELDS or \
            value.get("acceptanceVersion") != "2":
        raise StructuredSourceError(
            "acceptance registry shape/version is not current")
    criteria = value.get("criteria")
    if not isinstance(criteria, list) or \
            [entry.get("code") for entry in criteria
             if isinstance(entry, dict)] != list(CRITERIA):
        raise StructuredSourceError("acceptance criterion census is not exact")
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
