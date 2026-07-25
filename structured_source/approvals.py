"""Append-only exact-side identified-human approval records."""

from __future__ import annotations

from datetime import datetime
import os
import re
from xml.etree import ElementTree as ET

from . import CONTENT_NAMESPACE, RELATIONS_NAMESPACE
from .atomic import publish_set
from .canonical import raw_digest
from .control import canonical_json, control_digest, parse_json
from .errors import StructuredSourceError
from .parser import parse_artifact
from .registry import files_by_id, safe_path, validate_registry

C = "{%s}" % CONTENT_NAMESPACE
R = "{%s}" % RELATIONS_NAMESPACE
INVENTORY_PATH = "structured_source/approvals/inventory.json"
AUTHORITY_PATH = "structured_source/approvals/authorities.json"
RECORD_DIRECTORY = "structured_source/approvals/records"
STATUS_REGISTER_PATH = \
    "AA11393US-structured-source-markdown_implementation-register.md"
APPROVAL_TYPES = {
    "projection-completeness", "source-fidelity", "authored-content-review",
    "relation-content-review",
}
_DIGEST = re.compile(r"sha256/(?:raw|c1|xc1/ssp-xd1):[0-9a-f]{64}\Z")
_CONTROL_DIGEST = re.compile(r"sha256/c1:[0-9a-f]{64}\Z")
_RECORD_FIELDS = {
    "recordVersion", "approvalType", "subjectKind", "subjectId", "reviewer",
    "reviewedAt", "bindings", "projectionApprovalDigest", "confirmation",
}
_REVIEWER_FIELDS = {"identity", "role", "authorityKind"}
_BINDING_FIELDS = {
    "bindingVersion", "sourceRawDigest", "sourceSemanticDigest",
    "registryDigest", "schemaBindings", "controlBindings",
    "dependencyBindings", "endpointBindings", "assetBindings",
    "sourceEvidenceBindings", "markdownDigest", "coverageDigest",
    "reviewedCensusDigest",
}


def _utc_timestamp(value):
    try:
        timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc:
        raise StructuredSourceError(
            "approval review time is not an ISO timestamp") from exc
    if timestamp.utcoffset() is None or not value.endswith("Z"):
        raise StructuredSourceError("approval review time is not exact UTC")
    return timestamp


def validate_authorities(value):
    if not isinstance(value, dict) or set(value) != {
            "authorityRegistryVersion", "authorities"} or \
            value.get("authorityRegistryVersion") != "1" or \
            not isinstance(value.get("authorities"), list):
        raise StructuredSourceError("approval-authority registry is malformed")
    keys = []
    for item in value["authorities"]:
        if not isinstance(item, dict) or set(item) != {
                "identity", "role", "authorityKind"} or \
                item.get("authorityKind") != "identified-human" or \
                not all(isinstance(item.get(field), str) and item[field].strip()
                        for field in ("identity", "role")):
            raise StructuredSourceError("approval authority is malformed")
        keys.append((item["identity"], item["role"]))
    if keys != sorted(set(keys)):
        raise StructuredSourceError("approval authorities are not unique and sorted")
    return value


def load_authorities(root, byte_source=None):
    data = _read(root, AUTHORITY_PATH, byte_source)
    value = validate_authorities(parse_json(data))
    if data != canonical_json(value):
        raise StructuredSourceError(
            "approval-authority registry bytes are not canonical c1")
    return value


def _read(root, path, byte_source=None):
    absolute = os.path.join(root, *safe_path(path).split("/"))
    try:
        if byte_source:
            return byte_source(absolute)
        with open(absolute, "rb") as handle:
            return handle.read()
    except OSError as exc:
        raise StructuredSourceError("controlled approval input is unreadable: %s" % path) from exc


def _file_path(files, file_id):
    try:
        return files[file_id]["path"]
    except KeyError as exc:
        raise StructuredSourceError("approval binding references an unknown registry file") from exc


def package_binding(root, registry, package, byte_source=None):
    """Materialize every exact side that a human approval authorizes."""
    validate_registry(registry)
    files = files_by_id(registry)
    source_path = _file_path(files, package["sourceFile"])
    source_bytes = _read(root, source_path, byte_source)
    kind = "content-document" if "documentId" in package else "relation-set"
    artifact = parse_artifact(source_bytes, kind)
    markdown_path = _file_path(files, package["markdownFile"])
    coverage_path = _file_path(files, package["coverageFile"])
    schema_paths = sorted(item["path"] for item in registry["files"]
                          if item["role"] == "schema")
    control_paths = sorted(
        item["path"] for item in registry["files"]
        if item["role"] in {"implementation-source", "profile", "policy",
                            "environment-control", "approval-authority"} and
        item["path"] not in {INVENTORY_PATH, STATUS_REGISTER_PATH})
    dependencies = package.get("dependencyBindings", [])
    endpoints = []
    if kind == "relation-set":
        endpoints = sorted({
            "%s|%s|%s|%s" % (
                item.get("role"), item.get("documentId"), item.get("fragmentId"),
                item.get("fragmentContentDigest"))
            for item in artifact.root.findall(".//" + R + "endpoint")})
    asset_bindings = []
    for file_id in package.get("assetFiles", []):
        path = _file_path(files, file_id)
        asset_bindings.append("%s|%s" % (path, raw_digest(_read(root, path, byte_source))))
    evidence_bindings = []
    for file_id in package.get("storedSourceFiles", []) + package.get("convenienceFiles", []):
        path = _file_path(files, file_id)
        evidence_bindings.append("%s|%s" % (path, raw_digest(_read(root, path, byte_source))))
    manifest_file = package.get("sourceManifestFile")
    if manifest_file is not None:
        path = _file_path(files, manifest_file)
        evidence_bindings.append(
            "%s|%s" % (path, raw_digest(_read(root, path, byte_source))))
    census = (sorted("%s|%s" % item for item in artifact.fragment_digests.items())
              if kind == "content-document" else
              sorted("%s|%s" % (node.get("relationId"),
                                  artifact.fragment_digests[node.get("{http://www.w3.org/XML/1998/namespace}id")])
                     for node in artifact.root.findall(R + "relation")))
    registry_bytes = canonical_json(registry)
    return {
        "bindingVersion": "1",
        "sourceRawDigest": artifact.raw_digest,
        "sourceSemanticDigest": artifact.semantic_digest,
        "registryDigest": raw_digest(registry_bytes),
        "schemaBindings": sorted("%s|%s" % (path, raw_digest(_read(root, path, byte_source)))
                                 for path in schema_paths),
        "controlBindings": sorted("%s|%s" % (path, raw_digest(_read(root, path, byte_source)))
                                  for path in control_paths),
        "dependencyBindings": sorted(dependencies),
        "endpointBindings": endpoints,
        "assetBindings": sorted(asset_bindings),
        "sourceEvidenceBindings": sorted(evidence_bindings),
        "markdownDigest": raw_digest(_read(root, markdown_path, byte_source)),
        "coverageDigest": raw_digest(_read(root, coverage_path, byte_source)),
        "reviewedCensusDigest": control_digest(census),
    }


def validate_record(record):
    if not isinstance(record, dict) or set(record) != _RECORD_FIELDS or \
            record.get("recordVersion") != "1" or \
            record.get("approvalType") not in APPROVAL_TYPES or \
            record.get("subjectKind") not in {"document", "relation-set"}:
        raise StructuredSourceError("approval record shape/version is not current")
    if not isinstance(record.get("subjectId"), str) or not record["subjectId"]:
        raise StructuredSourceError("approval subject identity is absent")
    reviewer = record.get("reviewer")
    if not isinstance(reviewer, dict) or set(reviewer) != _REVIEWER_FIELDS or \
            reviewer.get("authorityKind") != "identified-human" or \
            not all(isinstance(reviewer.get(field), str) and reviewer[field].strip()
                    for field in ("identity", "role")):
        raise StructuredSourceError("approval reviewer is not an identified human")
    _utc_timestamp(record["reviewedAt"])
    if record.get("confirmation") != "exact-current-sides-reviewed-and-approved":
        raise StructuredSourceError("approval lacks the exact human confirmation")
    binding = record.get("bindings")
    if not isinstance(binding, dict) or set(binding) != _BINDING_FIELDS or \
            binding.get("bindingVersion") != "1":
        raise StructuredSourceError("approval exact-side binding is malformed")
    for field in ("sourceRawDigest", "sourceSemanticDigest", "registryDigest",
                  "markdownDigest", "coverageDigest", "reviewedCensusDigest"):
        if not isinstance(binding.get(field), str) or _DIGEST.fullmatch(binding[field]) is None:
            raise StructuredSourceError("approval digest field is malformed: %s" % field)
    for field in ("schemaBindings", "controlBindings", "dependencyBindings",
                  "endpointBindings", "assetBindings", "sourceEvidenceBindings"):
        values = binding.get(field)
        if not isinstance(values, list) or values != sorted(set(values)) or \
                not all(isinstance(item, str) and item for item in values):
            raise StructuredSourceError("approval binding set is malformed: %s" % field)
    projection = record.get("projectionApprovalDigest")
    if record["approvalType"] == "projection-completeness":
        if projection is not None:
            raise StructuredSourceError("projection approval cannot cite itself")
    elif not isinstance(projection, str) or \
            _CONTROL_DIGEST.fullmatch(projection) is None:
        raise StructuredSourceError("substantive approval lacks its projection approval")
    return record


def validate_inventory(value):
    if not isinstance(value, dict) or set(value) != {"inventoryVersion", "records"} or \
            value.get("inventoryVersion") != "1" or not isinstance(value.get("records"), list):
        raise StructuredSourceError("approval inventory shape/version is not current")
    keys = []
    paths = []
    for item in value["records"]:
        if not isinstance(item, dict) or set(item) != {
                "digest", "path", "approvalType", "subjectId"} or \
                item.get("approvalType") not in APPROVAL_TYPES:
            raise StructuredSourceError("approval inventory entry is malformed")
        digest = item.get("digest")
        if not isinstance(digest, str) or \
                _CONTROL_DIGEST.fullmatch(digest) is None:
            raise StructuredSourceError("approval inventory digest is malformed")
        path = safe_path(item.get("path"), "approval record path")
        expected = "%s/%s.json" % (RECORD_DIRECTORY, digest.rsplit(":", 1)[1])
        if path != expected:
            raise StructuredSourceError("approval record path is not digest-addressed")
        keys.append((item["subjectId"], item["approvalType"], digest))
        paths.append(path)
    if keys != sorted(keys) or len(paths) != len(set(paths)):
        raise StructuredSourceError("approval inventory is not unique and sorted")
    return value


def load_inventory(root, byte_source=None):
    data = _read(root, INVENTORY_PATH, byte_source)
    value = validate_inventory(parse_json(data))
    if data != canonical_json(value):
        raise StructuredSourceError(
            "approval inventory bytes are not canonical c1")
    return value


def load_records(root, byte_source=None):
    inventory = load_inventory(root, byte_source)
    records = []
    for item in inventory["records"]:
        data = _read(root, item["path"], byte_source)
        value = parse_json(data)
        if not isinstance(value, dict) or set(value) != {"digest", "record"} or \
                value.get("digest") != item["digest"]:
            raise StructuredSourceError("approval record envelope is malformed")
        if data != canonical_json(value):
            raise StructuredSourceError(
                "approval record envelope bytes are not canonical c1")
        record = validate_record(value.get("record"))
        if control_digest(record) != item["digest"] or \
                record["approvalType"] != item["approvalType"] or \
                record["subjectId"] != item["subjectId"]:
            raise StructuredSourceError("approval record digest/index binding is stale")
        records.append((item["digest"], record))
    return records


def resolve_current(root, registry, package, byte_source=None, records=None):
    package_id = package.get("documentId", package.get("relationSetId"))
    subject_kind = "document" if "documentId" in package else "relation-set"
    binding = package_binding(root, registry, package, byte_source)
    records = load_records(root, byte_source) if records is None else records
    authorities = {(item["identity"], item["role"])
                   for item in load_authorities(root, byte_source)["authorities"]}
    if any((record["reviewer"]["identity"], record["reviewer"]["role"])
           not in authorities for unused_digest, record in records):
        raise StructuredSourceError("approval record cites an unknown human authority")
    current = {}
    for approval_type in package["requiredApprovals"]:
        matches = [(digest, record) for digest, record in records
                   if record["approvalType"] == approval_type and
                   record["subjectKind"] == subject_kind and
                   record["subjectId"] == package_id and
                   record["bindings"] == binding]
        if len(matches) != 1:
            raise StructuredSourceError(
                "%s has %d exact-current %s approvals" %
                (package_id, len(matches), approval_type))
        current[approval_type] = matches[0]
    projection_digest, projection = current["projection-completeness"]
    for approval_type, (unused_digest, record) in current.items():
        if approval_type == "projection-completeness":
            continue
        if record["projectionApprovalDigest"] != projection_digest or \
                _utc_timestamp(record["reviewedAt"]) <= \
                _utc_timestamp(projection["reviewedAt"]):
            raise StructuredSourceError(
                "%s substantive approval does not follow its projection approval" % package_id)
    return {approval_type: digest for approval_type, (digest, unused) in current.items()}


def make_record(root, registry, package, approval_type, reviewer, role,
                reviewed_at, projection_digest=None):
    if approval_type not in package["requiredApprovals"]:
        raise StructuredSourceError("approval type is not required by this package")
    authorities = {(item["identity"], item["role"])
                   for item in load_authorities(root)["authorities"]}
    if (reviewer, role) not in authorities:
        raise StructuredSourceError("reviewer identity/role is not a current authority")
    record = {
        "recordVersion": "1", "approvalType": approval_type,
        "subjectKind": "document" if "documentId" in package else "relation-set",
        "subjectId": package.get("documentId", package.get("relationSetId")),
        "reviewer": {"identity": reviewer, "role": role,
                     "authorityKind": "identified-human"},
        "reviewedAt": reviewed_at,
        "bindings": package_binding(root, registry, package),
        "projectionApprovalDigest": projection_digest,
        "confirmation": "exact-current-sides-reviewed-and-approved",
    }
    return validate_record(record)


def append_record(root, record):
    validate_record(record)
    inventory_bytes = _read(root, INVENTORY_PATH)
    inventory = validate_inventory(parse_json(inventory_bytes))
    digest = control_digest(record)
    path = "%s/%s.json" % (RECORD_DIRECTORY, digest.rsplit(":", 1)[1])
    if any(item["digest"] == digest or item["path"] == path
           for item in inventory["records"]):
        raise StructuredSourceError("approval record already exists")
    inventory["records"].append({
        "digest": digest, "path": path,
        "approvalType": record["approvalType"], "subjectId": record["subjectId"],
    })
    inventory["records"].sort(
        key=lambda item: (item["subjectId"], item["approvalType"], item["digest"]))
    envelope = canonical_json({"digest": digest, "record": record})
    publish_set(root, {path: envelope, INVENTORY_PATH: canonical_json(inventory)},
                {path: None, INVENTORY_PATH: inventory_bytes})
    return digest
