"""Three data-only structured-source acceptance registries and table projections."""

from __future__ import annotations

import importlib
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
_CRITERION_FIELDS = {"id", "code", "outcome", "enforcer"}
_DOMAIN_TEST_MODULES = {
    "authored-markdown": frozenset({
        "structured_source.tests.test_acceptance",
        "structured_source.tests.test_conversion",
        "structured_source.tests.test_registry",
        "structured_source.tests.test_xml_contract",
    }),
    "authored-relations": frozenset({
        "structured_source.tests.test_acceptance",
        "structured_source.tests.test_conversion",
        "structured_source.tests.test_registry",
        "structured_source.tests.test_xml_contract",
    }),
    "pdf-transcription": frozenset({
        "structured_source.tests.test_acceptance",
        "structured_source.tests.test_pdf_transcription",
        "structured_source.tests.test_registry",
        "structured_source.tests.test_xml_contract",
    }),
}


def _contract(domain):
    matches = [item for item in CONTRACTS if item["domain"] == domain]
    if len(matches) != 1:
        raise StructuredSourceError("acceptance domain is not current")
    return matches[0]


def _resolve_enforcer(path):
    if not isinstance(path, str) or not path or any(
            not part or not part.replace("_", "a").isalnum()
            for part in path.split(".")):
        raise StructuredSourceError("acceptance enforcer path is malformed")
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
            raise StructuredSourceError(
                "acceptance enforcer symbol is absent: %s" % path) from exc
        if not callable(value):
            raise StructuredSourceError(
                "acceptance enforcer is not executable: %s" % path)
        return value
    raise StructuredSourceError("acceptance enforcer module is absent: %s" % path)


def validate_registry(value, domain):
    contract = _contract(domain)
    if not isinstance(value, dict) or set(value) != _REGISTRY_FIELDS or \
            value.get("acceptanceVersion") != "2" or \
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
        if not isinstance(criterion, dict):
            raise StructuredSourceError(
                "%s acceptance criterion is malformed" % domain)
        enforcer = criterion.get("enforcer")
        enforcer_parts = enforcer.split("; ") if isinstance(enforcer, str) else []
        if set(criterion) != _CRITERION_FIELDS or \
                identifier.fullmatch(criterion.get("code", "")) is None or \
                not criterion.get("id", "").startswith(
                    criterion["code"] + " — ") or \
                not all(isinstance(criterion.get(field), str) and
                        criterion[field].strip()
                        for field in ("outcome", "enforcer")) or \
                len(enforcer_parts) != 2 or \
                enforcer_parts[1] not in _DOMAIN_TEST_MODULES[domain]:
            raise StructuredSourceError(
                "%s acceptance criterion is malformed" % domain)
        _resolve_enforcer(enforcer_parts[0])
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
        "| ID | Executable technical outcome | Independent enforcer |",
        "|---|---|---|",
    ]
    for criterion in registry["criteria"]:
        outcome = criterion["outcome"].replace("|", "\\|").replace("\n", " ")
        enforcer = criterion["enforcer"].replace("|", "\\|").replace("\n", " ")
        rows.append("| **%s** | %s | %s |" %
                    (criterion["id"], outcome, enforcer))
    return "\n".join(rows) + "\n"
