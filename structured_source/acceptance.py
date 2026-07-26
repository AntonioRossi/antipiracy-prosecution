"""Three data-only structured-source acceptance registries and table projections."""

from __future__ import annotations

import os
import re

from .control import canonical_json, parse_json
from .errors import StructuredSourceError

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONTRACTS = (
    {
        "domain": "pdf-transcription",
        "authorityScheme": "pdf-evidence-transcription-v1",
        "registryPath": "structured_source/registry/acceptance-pdf-transcription.json",
        "contractPath": "contracts/10-source-surfaces/pdf-transcription/acceptance-criteria.md",
        "tableStart": "<!-- SSM-PDF-AC-TABLE:START -->\n",
        "tableEnd": "<!-- SSM-PDF-AC-TABLE:END -->",
        "criteria": tuple("SSM-PDF-AC-%02d" % number for number in range(1, 7)),
    },
    {
        "domain": "authored-markdown",
        "authorityScheme": "authored-markdown-v1",
        "registryPath": "structured_source/registry/acceptance-authored-markdown.json",
        "contractPath": "contracts/10-source-surfaces/authored-markdown/acceptance-criteria.md",
        "tableStart": "<!-- SSM-MD-AC-TABLE:START -->\n",
        "tableEnd": "<!-- SSM-MD-AC-TABLE:END -->",
        "criteria": tuple("SSM-MD-AC-%02d" % number for number in range(1, 7)),
    },
    {
        "domain": "authored-relations",
        "authorityScheme": "authored-relations-v1",
        "registryPath": "structured_source/registry/acceptance-authored-relations.json",
        "contractPath": "contracts/20-semantic-relations/authored-relations/acceptance-criteria.md",
        "tableStart": "<!-- SSM-REL-AC-TABLE:START -->\n",
        "tableEnd": "<!-- SSM-REL-AC-TABLE:END -->",
        "criteria": tuple("SSM-REL-AC-%02d" % number for number in range(1, 7)),
    },
)
CRITERIA = tuple(
    criterion
    for contract in CONTRACTS
    for criterion in contract["criteria"]
)
_REGISTRY_FIELDS = {
    "acceptanceVersion", "authorityScheme", "criteria", "domain",
}
_CRITERION_FIELDS = {"id", "code", "outcome", "evidence"}


def _contract(domain):
    matches = [item for item in CONTRACTS if item["domain"] == domain]
    if len(matches) != 1:
        raise StructuredSourceError("acceptance domain is not current")
    return matches[0]


def validate_registry(value, domain):
    contract = _contract(domain)
    if not isinstance(value, dict) or set(value) != _REGISTRY_FIELDS or \
            value.get("acceptanceVersion") != "1" or \
            value.get("domain") != domain or \
            value.get("authorityScheme") != contract["authorityScheme"]:
        raise StructuredSourceError(
            "%s acceptance registry shape/version is not current" % domain)
    criteria = value.get("criteria")
    if not isinstance(criteria, list) or \
            [entry.get("code") for entry in criteria
             if isinstance(entry, dict)] != list(contract["criteria"]):
        raise StructuredSourceError(
            "%s acceptance criterion census is not exact" % domain)
    identifier = re.compile(
        re.escape(contract["criteria"][0].rsplit("-", 1)[0]) +
        r"-(0[1-6])\Z")
    for criterion in criteria:
        if not isinstance(criterion, dict) or \
                set(criterion) != _CRITERION_FIELDS or \
                identifier.fullmatch(criterion.get("code", "")) is None or \
                not criterion.get("id", "").startswith(
                    criterion["code"] + " — ") or \
                not all(isinstance(criterion.get(field), str) and
                        criterion[field].strip()
                        for field in ("outcome", "evidence")):
            raise StructuredSourceError(
                "%s acceptance criterion is malformed" % domain)
    return value


def load_registries(root=ROOT, byte_source=None):
    registries = []
    for contract in CONTRACTS:
        absolute = os.path.join(root, *contract["registryPath"].split("/"))
        try:
            if byte_source:
                data = byte_source(absolute)
            else:
                with open(absolute, "rb") as handle:
                    data = handle.read()
        except (OSError, KeyError) as exc:
            raise StructuredSourceError(
                "%s acceptance registry is unreadable" %
                contract["domain"]) from exc
        value = validate_registry(parse_json(data), contract["domain"])
        if data != canonical_json(value):
            raise StructuredSourceError(
                "%s acceptance registry bytes are not canonical" %
                contract["domain"])
        registries.append(value)
    return tuple(registries)


def render_table(registry):
    validate_registry(registry, registry.get("domain") if isinstance(
        registry, dict) else None)
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
