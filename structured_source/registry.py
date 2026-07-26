"""Closed content registry for the three current authority schemes.

The registry describes only live package files and consumer edges.  It is not
an approval database, digest ledger, coverage store, or migration inventory.
"""

from __future__ import annotations

from collections import Counter
import os
import re

from .control import canonical_json, parse_json
from .errors import StructuredSourceError

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY_PATH = "structured_source/registry/content.json"

AUTHORITY_SCHEMES = frozenset({
    "pdf-evidence-transcription-v1",
    "authored-markdown-v1",
    "authored-relations-v1",
})
INPUT_REPRESENTATIONS = frozenset({"markdown", "xml"})

_ID = re.compile(r"[a-z][a-z0-9-]{0,159}\Z")
_TOP_FIELDS = {
    "registryVersion", "files", "packages", "routers", "consumers",
    "taxonomy",
}
_FILE_FIELDS = {"fileId", "path", "role"}
_PACKAGE_FIELDS = {
    "packageId", "authorityScheme", "xmlFile", "markdownFile", "scope",
    "status", "owner", "sourceManifestFile", "storedSourceFiles",
    "convenienceFiles", "assetFiles",
}
_ROUTER_FIELDS = {"routerId", "path", "scope", "packages"}
_CONSUMER_FIELDS = {"consumerId", "edges"}
_EDGE_FIELDS = {"packageId", "inputRepresentation", "dependencies"}
_TAXONOMY_FIELDS = {"controlledRoots", "forbiddenPaths"}

_FILE_ROLES = frozenset({
    "asset",
    "authored-markdown",
    "consumer-dependency",
    "convenience-derivative",
    "generated-markdown",
    "generated-xml",
    "relation-xml",
    "router",
    "source-manifest",
    "stored-evidence",
    "transcription-xml",
})
_FORBIDDEN_FIELD_PARTS = (
    "approval", "attestation", "audit", "compatibility", "coverage",
    "digest", "export", "lineage", "migration", "receipt", "reviewer",
    "verificationrecord",
)
_FORBIDDEN_PATH_PARTS = (
    "/approvals/", "/attestations/", "/audit-exports/", "/compatibility/",
    "/exports/", "/lineage/", "/migration/", "/receipts/",
    "/verification-records/", ".attestation.json", ".audit.json",
    ".coverage.json", ".lineage.json", ".receipt.json",
    ".verification.json",
    "structured-source-markdown_implementation-register",
)


def safe_path(value, label="registry path"):
    """Return one canonical repository-relative path or fail closed."""
    if not isinstance(value, str) or not value or os.path.isabs(value) or \
            "\\" in value or any(part in {"", ".", ".."}
                                  for part in value.split("/")):
        raise StructuredSourceError(
            "%s is not a canonical repository path" % label)
    return value


def _stable_id(value, label):
    if not isinstance(value, str) or _ID.fullmatch(value) is None:
        raise StructuredSourceError("%s is not a stable identity" % label)
    return value


def _sorted_unique_strings(value, label, *, allow_empty=True):
    if not isinstance(value, list) or (not allow_empty and not value) or \
            not all(isinstance(item, str) and item for item in value) or \
            value != sorted(set(value)):
        raise StructuredSourceError(
            "%s is not an exact sorted string set" % label)
    return value


def _reject_retired_fields(value, path="$"):
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str):
                raise StructuredSourceError(
                    "content registry field name is not text")
            folded = key.casefold()
            if any(part in folded for part in _FORBIDDEN_FIELD_PARTS):
                raise StructuredSourceError(
                    "content registry contains retired field %s.%s" %
                    (path, key))
            _reject_retired_fields(child, "%s.%s" % (path, key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _reject_retired_fields(child, "%s[%d]" % (path, index))


def _validate_file_reference(file_by_id, file_id, roles, label):
    if not isinstance(file_id, str) or file_id not in file_by_id:
        raise StructuredSourceError("%s references an unknown file" % label)
    if file_by_id[file_id]["role"] not in roles:
        raise StructuredSourceError("%s has an incompatible file role" % label)


def validate_registry(value):
    """Validate and return the exact current registry value."""
    if not isinstance(value, dict) or set(value) != _TOP_FIELDS or \
            value.get("registryVersion") != "1":
        raise StructuredSourceError(
            "content registry shape/version is not current")
    _reject_retired_fields(value)

    files = value.get("files")
    if not isinstance(files, list) or not files:
        raise StructuredSourceError("content registry file inventory is empty")
    file_ids = []
    paths = []
    for entry in files:
        if not isinstance(entry, dict) or set(entry) != _FILE_FIELDS:
            raise StructuredSourceError("content registry file entry is malformed")
        file_ids.append(_stable_id(entry.get("fileId"), "file id"))
        path = safe_path(entry.get("path"))
        paths.append(path)
        if entry.get("role") not in _FILE_ROLES:
            raise StructuredSourceError("content registry file role is not current")
        folded_path = "/" + path.casefold()
        if any(part in folded_path for part in _FORBIDDEN_PATH_PARTS):
            raise StructuredSourceError("content registry contains a retired path")
    if file_ids != sorted(file_ids) or len(file_ids) != len(set(file_ids)) or \
            len(paths) != len(set(paths)) or \
            len(paths) != len({path.casefold() for path in paths}):
        raise StructuredSourceError(
            "content registry file ids/paths are not unique and sorted")
    file_by_id = {entry["fileId"]: entry for entry in files}

    packages = value.get("packages")
    if not isinstance(packages, list) or not packages:
        raise StructuredSourceError("content registry package inventory is empty")
    package_ids = []
    owned_files = []
    package_by_id = {}
    for package in packages:
        if not isinstance(package, dict) or set(package) != _PACKAGE_FIELDS:
            raise StructuredSourceError("content registry package entry is malformed")
        package_id = _stable_id(package.get("packageId"), "package id")
        package_ids.append(package_id)
        package_by_id[package_id] = package
        scheme = package.get("authorityScheme")
        if scheme not in AUTHORITY_SCHEMES:
            raise StructuredSourceError("package authority scheme is not current")
        for field in ("scope", "status", "owner"):
            if not isinstance(package.get(field), str) or not package[field].strip():
                raise StructuredSourceError("package %s is missing" % field)
        xml_file = package.get("xmlFile")
        markdown_file = package.get("markdownFile")
        expected_roles = {
            "pdf-evidence-transcription-v1":
                ({"transcription-xml"}, {"generated-markdown"}),
            "authored-markdown-v1":
                ({"generated-xml"}, {"authored-markdown"}),
            "authored-relations-v1":
                ({"relation-xml"}, {"generated-markdown"}),
        }[scheme]
        _validate_file_reference(
            file_by_id, xml_file, expected_roles[0], "package XML")
        _validate_file_reference(
            file_by_id, markdown_file, expected_roles[1], "package Markdown")
        if xml_file == markdown_file:
            raise StructuredSourceError("package representations share one file")

        stored = _sorted_unique_strings(
            package.get("storedSourceFiles"), "stored source files")
        convenience = _sorted_unique_strings(
            package.get("convenienceFiles"), "convenience files")
        assets = _sorted_unique_strings(package.get("assetFiles"), "asset files")
        for file_id in stored:
            _validate_file_reference(
                file_by_id, file_id, {"stored-evidence"}, "stored source")
        for file_id in convenience:
            _validate_file_reference(
                file_by_id, file_id, {"convenience-derivative"},
                "convenience derivative")
        for file_id in assets:
            _validate_file_reference(file_by_id, file_id, {"asset"}, "asset")

        manifest = package.get("sourceManifestFile")
        if scheme == "pdf-evidence-transcription-v1":
            if len(stored) != 1 or manifest is None:
                raise StructuredSourceError(
                    "PDF package requires one stored source and one manifest")
            _validate_file_reference(
                file_by_id, manifest, {"source-manifest"}, "source manifest")
            if not file_by_id[stored[0]]["path"].casefold().endswith(".pdf") or \
                    not file_by_id[xml_file]["path"].casefold().endswith(".xml") or \
                    not file_by_id[markdown_file]["path"].casefold().endswith(".md") or \
                    file_by_id[manifest]["path"].rsplit("/", 1)[-1] != \
                    "source-manifest.json":
                raise StructuredSourceError(
                    "PDF package file types/names are not current")
        elif manifest is not None or stored or convenience or assets:
            raise StructuredSourceError(
                "package contains files forbidden by its authority scheme")
        owned_files.extend(
            [xml_file, markdown_file] + stored + convenience + assets +
            ([manifest] if manifest is not None else []))
    if package_ids != sorted(package_ids) or \
            len(package_ids) != len(set(package_ids)):
        raise StructuredSourceError(
            "package identities are not unique and sorted")
    if len(owned_files) != len(set(owned_files)):
        raise StructuredSourceError(
            "a package-owned file has more than one package owner")
    package_owned_roles = _FILE_ROLES - {"consumer-dependency", "router"}
    registered_package_files = {
        entry["fileId"] for entry in files
        if entry["role"] in package_owned_roles}
    if set(owned_files) != registered_package_files:
        raise StructuredSourceError(
            "package/file ownership census is not bidirectionally exact")

    routers = value.get("routers")
    if not isinstance(routers, list):
        raise StructuredSourceError("router registry is malformed")
    router_ids = []
    router_paths = []
    for router in routers:
        if not isinstance(router, dict) or set(router) != _ROUTER_FIELDS:
            raise StructuredSourceError("router entry is malformed")
        router_ids.append(_stable_id(router.get("routerId"), "router id"))
        path = safe_path(router.get("path"), "router path")
        router_paths.append(path)
        if not isinstance(router.get("scope"), str) or not router["scope"].strip():
            raise StructuredSourceError("router scope is missing")
        routed = _sorted_unique_strings(
            router.get("packages"), "router packages", allow_empty=False)
        if not set(routed).issubset(package_by_id):
            raise StructuredSourceError("router names an unknown package")
        matches = [entry for entry in files if entry["path"] == path]
        if len(matches) != 1 or matches[0]["role"] != "router":
            raise StructuredSourceError(
                "router path has no exact router-file registration")
    if router_ids != sorted(router_ids) or len(router_ids) != len(set(router_ids)) or \
            len(router_paths) != len(set(router_paths)) or \
            len(router_paths) != len({path.casefold() for path in router_paths}):
        raise StructuredSourceError(
            "router identities/paths are not unique and sorted")
    registered_router_files = {
        entry["fileId"] for entry in files if entry["role"] == "router"}
    resolved_router_files = {
        entry["fileId"] for entry in files if entry["path"] in router_paths}
    if registered_router_files != resolved_router_files:
        raise StructuredSourceError(
            "router/file ownership census is not bidirectionally exact")

    consumers = value.get("consumers")
    if not isinstance(consumers, list):
        raise StructuredSourceError("consumer registry is malformed")
    consumer_ids = []
    edge_pairs = []
    representation_files = {
        package_id: {package["xmlFile"], package["markdownFile"]}
        for package_id, package in package_by_id.items()
    }
    all_representation_files = set().union(*representation_files.values())
    for consumer in consumers:
        if not isinstance(consumer, dict) or set(consumer) != _CONSUMER_FIELDS:
            raise StructuredSourceError("consumer entry is malformed")
        consumer_id = _stable_id(consumer.get("consumerId"), "consumer id")
        consumer_ids.append(consumer_id)
        edges = consumer.get("edges")
        if not isinstance(edges, list) or not edges:
            raise StructuredSourceError("consumer edge inventory is empty")
        edge_package_ids = []
        for edge in edges:
            if not isinstance(edge, dict) or set(edge) != _EDGE_FIELDS:
                raise StructuredSourceError("consumer edge is malformed")
            package_id = edge.get("packageId")
            if package_id not in package_by_id:
                raise StructuredSourceError("consumer edge names an unknown package")
            edge_package_ids.append(package_id)
            if edge.get("inputRepresentation") not in INPUT_REPRESENTATIONS:
                raise StructuredSourceError(
                    "consumer edge representation is not current")
            dependencies = _sorted_unique_strings(
                edge.get("dependencies"), "consumer dependencies")
            if not set(dependencies).issubset(file_by_id):
                raise StructuredSourceError(
                    "consumer edge names an unknown dependency")
            if set(dependencies) & all_representation_files:
                raise StructuredSourceError(
                    "consumer dependency bypasses the declared representation")
            edge_pairs.append((consumer_id, package_id))
        if edge_package_ids != sorted(edge_package_ids) or \
                len(edge_package_ids) != len(set(edge_package_ids)):
            raise StructuredSourceError(
                "consumer package edges are not unique and sorted")
    if consumer_ids != sorted(consumer_ids) or \
            len(consumer_ids) != len(set(consumer_ids)) or \
            len(edge_pairs) != len(set(edge_pairs)):
        raise StructuredSourceError(
            "consumer identities/edges are not unique and sorted")
    registered_consumer_dependencies = {
        entry["fileId"] for entry in files
        if entry["role"] == "consumer-dependency"}
    declared_consumer_dependencies = [
        file_id for consumer in consumers for edge in consumer["edges"]
        for file_id in edge["dependencies"]]
    declared_dependency_counts = Counter(declared_consumer_dependencies)
    if registered_consumer_dependencies != set(declared_dependency_counts) or \
            any(count != 1 for count in declared_dependency_counts.values()):
        raise StructuredSourceError(
            "consumer dependency/file census is not bidirectionally exact")
    taxonomy = value.get("taxonomy")
    if not isinstance(taxonomy, dict) or set(taxonomy) != _TAXONOMY_FIELDS:
        raise StructuredSourceError("path taxonomy is malformed")
    controlled = _sorted_unique_strings(
        taxonomy.get("controlledRoots"), "controlled roots", allow_empty=False)
    forbidden = _sorted_unique_strings(
        taxonomy.get("forbiddenPaths"), "forbidden paths")
    for path in controlled + forbidden:
        safe_path(path, "taxonomy path")
    if set(paths) & set(forbidden):
        raise StructuredSourceError("a forbidden path is registered as current")
    if any(path == prefix or path.startswith(prefix.rstrip("/") + "/")
           for path in paths for prefix in forbidden):
        raise StructuredSourceError("a forbidden path is registered as current")
    routed_packages = [package_id for router in routers
                       for package_id in router["packages"]]
    if set(routed_packages) != set(package_by_id) or \
            len(routed_packages) != len(set(routed_packages)):
        raise StructuredSourceError(
            "routers do not expose every package exactly once")
    return value


def load_registry(root=ROOT, byte_source=None):
    """Load the canonical live content registry."""
    absolute = os.path.join(root, *REGISTRY_PATH.split("/"))
    try:
        if byte_source:
            data = byte_source(absolute)
        else:
            with open(absolute, "rb") as handle:
                data = handle.read()
    except (OSError, KeyError) as exc:
        raise StructuredSourceError("content registry is unreadable") from exc
    value = validate_registry(parse_json(data))
    if data != canonical_json(value):
        raise StructuredSourceError("content registry bytes are not canonical")
    return value


def files_by_id(value):
    return {entry["fileId"]: entry for entry in value["files"]}


def packages_by_id(value):
    return {entry["packageId"]: entry for entry in value["packages"]}


def consumer_edge(value, consumer_id, package_id):
    matches = [
        edge
        for consumer in value["consumers"]
        if consumer["consumerId"] == consumer_id
        for edge in consumer["edges"]
        if edge["packageId"] == package_id
    ]
    if len(matches) != 1:
        raise StructuredSourceError(
            "consumer/package edge does not resolve exactly")
    return matches[0]
