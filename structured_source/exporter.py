"""Deterministic approved structured-package export and exact verification."""

from __future__ import annotations

from io import BytesIO
import os
import re
import zipfile

from .approvals import (INVENTORY_PATH, STATUS_REGISTER_PATH, load_inventory,
                        load_records, resolve_current)
from .atomic import publish_set
from .canonical import raw_digest
from .control import canonical_json, parse_json
from .errors import StructuredSourceError
from .registry import files_by_id, safe_path, validate_registry

EXPORT_TIMESTAMP = (2026, 7, 24, 0, 0, 0)
_CONTROL_DIGEST = re.compile(r"sha256/c1:[0-9a-f]{64}\Z")
EXPORT_ROLES = {
    "source-xml", "relation-xml", "markdown-view", "coverage", "asset",
    "source-manifest", "schema", "profile", "policy", "content-registry",
    "acceptance-registry", "approval-authority", "contract",
}


def _registered_export_paths(registry, export_path):
    return {
        item["path"] for item in registry["files"]
        if item["role"] in EXPORT_ROLES and
        item["path"] not in {export_path, STATUS_REGISTER_PATH}
    }


def _read(root, path, byte_source=None):
    absolute = os.path.join(root, *safe_path(path).split("/"))
    try:
        if byte_source:
            return byte_source(absolute)
        with open(absolute, "rb") as handle:
            return handle.read()
    except OSError as exc:
        raise StructuredSourceError("export input is unreadable: %s" % path) from exc


def _consumer(registry, consumer_id):
    matches = [item for item in registry["consumers"]
               if item["consumerId"] == consumer_id]
    if len(matches) != 1 or matches[0]["exportPath"] is None:
        raise StructuredSourceError("consumer does not resolve to one export")
    return matches[0]


def export_members(root, registry, consumer_id, byte_source=None):
    validate_registry(registry)
    consumer = _consumer(registry, consumer_id)
    packages = {item.get("documentId", item.get("relationSetId")): item
                for item in registry["documents"] + registry["relationSets"]}
    if set(consumer["packageIds"]) != set(packages):
        raise StructuredSourceError("structured export consumer does not close every package")
    records = load_records(root, byte_source)
    approval_bindings = {}
    for package_id in consumer["packageIds"]:
        approval_bindings[package_id] = resolve_current(
            root, registry, packages[package_id], byte_source, records)

    files = files_by_id(registry)
    selected = set()
    for package_id in consumer["packageIds"]:
        package = packages[package_id]
        selected.update(files[package[field]]["path"]
                        for field in ("sourceFile", "markdownFile", "coverageFile"))
        selected.update(files[file_id]["path"] for file_id in package.get("assetFiles", []))
    selected.update(_registered_export_paths(registry, consumer["exportPath"]))
    inventory = load_inventory(root, byte_source)
    selected.add(INVENTORY_PATH)
    selected.update(item["path"] for item in inventory["records"])
    payload = {path: _read(root, path, byte_source) for path in sorted(selected)}
    manifest = {
        "exportVersion": "1", "consumerId": consumer_id,
        "semanticAuthority": "xml-only",
        "markdownRole": "human-review-evidence",
        "registryPath": "structured_source/registry/content.json",
        "approvalInventoryPath": INVENTORY_PATH,
        "packages": [{
            "packageId": package_id,
            "approvalBindings": approval_bindings[package_id],
        } for package_id in sorted(approval_bindings)],
        "members": [{"path": path, "rawDigest": raw_digest(data),
                     "size": len(data)}
                    for path, data in sorted(payload.items())],
    }
    return {"manifest.json": canonical_json(manifest), **payload}


def build_export(root, registry, consumer_id, byte_source=None):
    members = export_members(root, registry, consumer_id, byte_source)
    output = BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9, strict_timestamps=True) as archive:
        for name, data in sorted(members.items()):
            info = zipfile.ZipInfo(name, EXPORT_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.flag_bits = 0x800
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED,
                             compresslevel=9)
    return output.getvalue()


def validate_export_bytes(data, expected_members):
    try:
        with zipfile.ZipFile(BytesIO(data), "r") as archive:
            names = archive.namelist()
            if names != sorted(expected_members) or len(names) != len(set(names)):
                raise StructuredSourceError("export member inventory/order is not exact")
            for info in archive.infolist():
                if info.date_time != EXPORT_TIMESTAMP or info.create_system != 3 or \
                        info.external_attr >> 16 != 0o100644 or info.filename.startswith("/") or \
                        any(part in {"", ".", ".."} for part in info.filename.split("/")):
                    raise StructuredSourceError("export member metadata/path is not canonical")
                if archive.read(info.filename) != expected_members[info.filename]:
                    raise StructuredSourceError("export member bytes are stale")
            manifest = parse_json(archive.read("manifest.json"))
    except (OSError, zipfile.BadZipFile, KeyError) as exc:
        raise StructuredSourceError("structured export is unreadable") from exc
    if not isinstance(manifest, dict) or set(manifest) != {
            "exportVersion", "consumerId", "semanticAuthority", "markdownRole",
            "registryPath", "approvalInventoryPath", "packages", "members"} or \
            manifest.get("exportVersion") != "1" or \
            not isinstance(manifest.get("consumerId"), str) or \
            manifest.get("semanticAuthority") != "xml-only" or \
            manifest.get("markdownRole") != "human-review-evidence" or \
            manifest.get("registryPath") != "structured_source/registry/content.json" or \
            manifest.get("approvalInventoryPath") != INVENTORY_PATH:
        raise StructuredSourceError("structured export envelope is malformed")
    packages = manifest.get("packages")
    package_ids = ([item.get("packageId") for item in packages
                    if isinstance(item, dict)]
                   if isinstance(packages, list) else [])
    if not isinstance(packages, list) or not packages or \
            package_ids != sorted(set(package_ids)) or \
            any(not isinstance(item, dict) or set(item) != {
                    "packageId", "approvalBindings"} or \
                not isinstance(item.get("packageId"), str) or \
                not isinstance(item.get("approvalBindings"), dict) or \
                not item["approvalBindings"] or \
                any(not isinstance(value, str) or
                    _CONTROL_DIGEST.fullmatch(value) is None
                    for value in item["approvalBindings"].values())
                for item in packages):
        raise StructuredSourceError("structured export package approvals are malformed")
    payload = {path: content for path, content in expected_members.items()
               if path != "manifest.json"}
    expected_inventory = [{"path": path, "rawDigest": raw_digest(content),
                           "size": len(content)}
                          for path, content in sorted(payload.items())]
    if manifest.get("members") != expected_inventory:
        raise StructuredSourceError("structured export manifest inventory is stale")
    denied = ("/convenience/", "/searchable/", ".txt", ".pdf")
    if any(any(token in path for token in denied)
           for path in names):
        raise StructuredSourceError("structured export contains a denied upstream input")
    return manifest


def verify_export(root, registry, consumer_id, byte_source=None):
    consumer = _consumer(registry, consumer_id)
    expected = export_members(root, registry, consumer_id, byte_source)
    data = _read(root, consumer["exportPath"], byte_source)
    validate_export_bytes(data, expected)
    rebuilt = build_export(root, registry, consumer_id, byte_source)
    if data != rebuilt:
        raise StructuredSourceError("committed structured export is not deterministic")
    return raw_digest(data)


def publish_export(root, registry, consumer_id):
    consumer = _consumer(registry, consumer_id)
    output_path = consumer["exportPath"]
    target = os.path.join(root, *output_path.split("/"))
    before = None
    if os.path.isfile(target):
        with open(target, "rb") as handle:
            before = handle.read()
    data = build_export(root, registry, consumer_id)
    validate_export_bytes(data, export_members(root, registry, consumer_id))
    publish_set(root, {output_path: data}, {output_path: before})
    return raw_digest(data)
