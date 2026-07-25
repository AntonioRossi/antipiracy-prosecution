"""Closed content-registry shape, identity, and ownership validation."""

from __future__ import annotations

import os
import re

from .control import parse_json
from .errors import StructuredSourceError

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY_PATH = "structured_source/registry/content.json"
_ID = re.compile(r"[a-z][a-z0-9-]{0,159}\Z")
_TOP_FIELDS = {
    "registryVersion", "files", "documents", "relationSets", "routers",
    "consumers", "taxonomy",
}
_FILE_FIELDS = {"fileId", "path", "role", "owner"}
_DOCUMENT_FIELDS = {
    "documentId", "artifactFamily", "jurisdiction", "scope", "status",
    "owner", "origin", "sourceFile", "sourceDigest", "markdownFile",
    "markdownDigest", "coverageFile", "coverageDigest",
    "sourceManifestFile",
    "storedSourceFiles", "convenienceFiles", "assetFiles",
    "dependencyBindings", "assetBindings", "requiredApprovals", "consumers",
    "referenceAllowlist", "fragmentCount",
}
_RELATION_FIELDS = {
    "relationSetId", "profile", "scope", "status", "owner", "sourceFile",
    "sourceDigest", "markdownFile", "markdownDigest", "coverageFile",
    "coverageDigest", "endpointDocuments", "requiredApprovals", "consumers",
    "relationCount",
}
_ROUTER_FIELDS = {"routerId", "path", "scope", "packages"}
_CONSUMER_FIELDS = {"consumerId", "inputAuthority", "packageIds", "exportPath"}
_TAXONOMY_FIELDS = {
    "priorArtIds", "controlledRoots", "forbiddenPaths",
    "singlePrimarySuffixes",
}
_APPROVAL_TYPES = {
    "projection-completeness", "source-fidelity", "authored-content-review",
    "relation-content-review",
}
_RAW_DIGEST = re.compile(r"sha256/raw:[0-9a-f]{64}\Z")
_SEMANTIC_DIGEST = re.compile(r"sha256/xc1/ssp-xd1:[0-9a-f]{64}\Z")
_FILE_ROLES = {
    "acceptance-registry", "approval-authority", "approval-inventory",
    "approved-export", "asset", "consumer-control",
    "content-registry", "contract", "convenience-derivative", "coverage",
    "environment-control", "implementation-source", "markdown-view",
    "outer-gate-control", "outer-gate-test", "policy", "profile",
    "registered-reference", "relation-xml", "repository-control-reference",
    "router", "schema", "source-manifest", "source-xml", "stored-evidence",
    "test",
}
_SCOPES = {"AF", "AF-CONT", "NA", "PCT", "prior-art", "shared"}
_JURISDICTIONS = {"PCT", "US"}
_STATUSES = {"draft", "evidence-record", "memo", "review-aid"}


def safe_path(value, label="registry path"):
    if not isinstance(value, str) or not value or os.path.isabs(value) or \
            "\\" in value or any(part in {"", ".", ".."}
                                  for part in value.split("/")):
        raise StructuredSourceError("%s is not a canonical repository path" % label)
    return value


def _stable_id(value, label):
    if not isinstance(value, str) or _ID.fullmatch(value) is None:
        raise StructuredSourceError("%s is not a stable registry identity" % label)
    return value


def _sorted_unique_strings(value, label, allow_empty=True):
    if not isinstance(value, list) or (not allow_empty and not value) or \
            value != sorted(set(value)) or \
            not all(isinstance(item, str) and item for item in value):
        raise StructuredSourceError("%s is not an exact sorted string set" % label)
    return value


def validate_registry(value):
    if not isinstance(value, dict) or set(value) != _TOP_FIELDS or \
            value.get("registryVersion") != "1":
        raise StructuredSourceError("content registry shape/version is not current")
    files = value.get("files")
    if not isinstance(files, list) or not files:
        raise StructuredSourceError("content registry file inventory is empty")
    file_ids = []
    paths = []
    for item in files:
        if not isinstance(item, dict) or set(item) != _FILE_FIELDS:
            raise StructuredSourceError("content registry file entry is malformed")
        file_ids.append(_stable_id(item.get("fileId"), "file id"))
        paths.append(safe_path(item.get("path")))
        if item.get("role") not in _FILE_ROLES:
            raise StructuredSourceError("file role is not closed")
        if not isinstance(item.get("owner"), str) or not item["owner"].strip():
            raise StructuredSourceError("file owner is missing")
    if file_ids != sorted(file_ids) or len(file_ids) != len(set(file_ids)) or \
            len(paths) != len(set(paths)):
        raise StructuredSourceError("content registry file ids/paths are not unique and sorted")
    declared_files = set(file_ids)
    file_by_id = {item["fileId"]: item for item in files}
    singleton_roles = {
        "acceptance-registry", "approval-authority", "approval-inventory",
        "approved-export", "content-registry",
    }
    if any(sum(item["role"] == role for item in files) != 1
           for role in singleton_roles):
        raise StructuredSourceError("singleton control-file role census is not exact")

    def require_role(file_id, roles, label):
        if file_by_id[file_id]["role"] not in roles:
            raise StructuredSourceError("%s has an incompatible file role" % label)

    document_ids = []
    package_ids = set()
    for document in value.get("documents", []):
        if not isinstance(document, dict) or set(document) != _DOCUMENT_FIELDS:
            raise StructuredSourceError("content registry document entry is malformed")
        document_id = _stable_id(document.get("documentId"), "document id")
        document_ids.append(document_id)
        package_ids.add(document_id)
        _stable_id(document.get("artifactFamily"), "artifact family")
        if document.get("scope") not in _SCOPES or \
                document.get("jurisdiction") not in _JURISDICTIONS or \
                document.get("status") not in _STATUSES or \
                not isinstance(document.get("owner"), str) or \
                not document["owner"].strip():
            raise StructuredSourceError("document classification/owner is not closed")
        if document.get("origin") not in {"authored", "pdf-derivative"}:
            raise StructuredSourceError("document origin is not closed")
        if not isinstance(document.get("sourceDigest"), str) or \
                _SEMANTIC_DIGEST.fullmatch(document["sourceDigest"]) is None or \
                any(not isinstance(document.get(field), str) or
                    _RAW_DIGEST.fullmatch(document[field]) is None
                    for field in ("markdownDigest", "coverageDigest")):
            raise StructuredSourceError("document digest set is malformed")
        expected_approvals = ["authored-content-review", "projection-completeness"] \
            if document["origin"] == "authored" else \
            ["projection-completeness", "source-fidelity"]
        if sorted(document.get("requiredApprovals", [])) != sorted(expected_approvals):
            raise StructuredSourceError("document approval types do not match its origin")
        for field in ("sourceFile", "markdownFile", "coverageFile"):
            if document.get(field) not in declared_files:
                raise StructuredSourceError("document references an unknown %s" % field)
        require_role(document["sourceFile"], {"source-xml"}, "document source")
        require_role(document["markdownFile"], {"markdown-view"}, "document Markdown")
        require_role(document["coverageFile"], {"coverage"}, "document coverage")
        manifest_file = document.get("sourceManifestFile")
        if document["origin"] == "pdf-derivative":
            if manifest_file not in declared_files:
                raise StructuredSourceError(
                    "PDF-derived document has no registered source manifest")
            require_role(manifest_file, {"source-manifest"},
                         "document source manifest")
        elif manifest_file is not None:
            raise StructuredSourceError(
                "authored document cannot own a source manifest")
        for field in ("storedSourceFiles", "convenienceFiles", "assetFiles"):
            values = _sorted_unique_strings(document.get(field), "document " + field)
            if not set(values).issubset(declared_files):
                raise StructuredSourceError("document %s references an unknown file" % field)
        for file_id in document["storedSourceFiles"]:
            require_role(file_id, {"stored-evidence"}, "stored source")
        for file_id in document["convenienceFiles"]:
            require_role(file_id, {"convenience-derivative"}, "convenience source")
        for file_id in document["assetFiles"]:
            require_role(file_id, {"asset"}, "document asset")
        if (document["origin"] == "authored" and
                (document["storedSourceFiles"] or document["convenienceFiles"])) or \
                (document["origin"] == "pdf-derivative" and
                 len(document["storedSourceFiles"]) != 1):
            raise StructuredSourceError("document origin/file-role closure is inconsistent")
        _sorted_unique_strings(document.get("dependencyBindings"),
                               "document dependency bindings")
        asset_bindings = _sorted_unique_strings(
            document.get("assetBindings"), "document asset bindings")
        bound_asset_files = []
        for binding in asset_bindings:
            parts = binding.split("|")
            if len(parts) != 2 or not parts[0] or parts[1] not in declared_files:
                raise StructuredSourceError("document asset binding is malformed")
            bound_asset_files.append(parts[1])
        if sorted(bound_asset_files) != document["assetFiles"]:
            raise StructuredSourceError("document asset bindings do not close its asset files")
        _sorted_unique_strings(document.get("consumers"), "document consumers", False)
        _sorted_unique_strings(document.get("referenceAllowlist"),
                               "document reference allowlist")
        if not isinstance(document.get("fragmentCount"), int) or \
                document["fragmentCount"] < 1:
            raise StructuredSourceError("document fragment census is invalid")
    if document_ids != sorted(document_ids) or len(document_ids) != len(set(document_ids)):
        raise StructuredSourceError("document identities are not unique and sorted")

    relation_ids = []
    for relation in value.get("relationSets", []):
        if not isinstance(relation, dict) or set(relation) != _RELATION_FIELDS:
            raise StructuredSourceError("content registry relation-set entry is malformed")
        relation_id = _stable_id(relation.get("relationSetId"), "relation-set id")
        relation_ids.append(relation_id)
        package_ids.add(relation_id)
        _stable_id(relation.get("profile"), "relation profile")
        if relation.get("scope") not in _SCOPES or \
                relation.get("status") not in _STATUSES or \
                not isinstance(relation.get("owner"), str) or \
                not relation["owner"].strip():
            raise StructuredSourceError("relation-set classification/owner is not closed")
        if not isinstance(relation.get("sourceDigest"), str) or \
                _SEMANTIC_DIGEST.fullmatch(relation["sourceDigest"]) is None or \
                any(not isinstance(relation.get(field), str) or
                    _RAW_DIGEST.fullmatch(relation[field]) is None
                    for field in ("markdownDigest", "coverageDigest")):
            raise StructuredSourceError("relation-set digest set is malformed")
        if relation.get("requiredApprovals") != [
                "projection-completeness", "relation-content-review"]:
            raise StructuredSourceError("relation-set approval types are not exact")
        for field in ("sourceFile", "markdownFile", "coverageFile"):
            if relation.get(field) not in declared_files:
                raise StructuredSourceError("relation set references an unknown %s" % field)
        require_role(relation["sourceFile"], {"relation-xml"}, "relation source")
        require_role(relation["markdownFile"], {"markdown-view"}, "relation Markdown")
        require_role(relation["coverageFile"], {"coverage"}, "relation coverage")
        _sorted_unique_strings(relation.get("endpointDocuments"),
                               "relation endpoint-document allowlist", False)
        _sorted_unique_strings(relation.get("consumers"), "relation consumers", False)
        if not isinstance(relation.get("relationCount"), int) or relation["relationCount"] < 1:
            raise StructuredSourceError("relation census is invalid")
    if relation_ids != sorted(relation_ids) or len(relation_ids) != len(set(relation_ids)):
        raise StructuredSourceError("relation-set identities are not unique and sorted")

    packages = list(value["documents"]) + list(value["relationSets"])
    exact_role_owners = {
        "source-xml": {item["sourceFile"] for item in value["documents"]},
        "relation-xml": {item["sourceFile"] for item in value["relationSets"]},
        "markdown-view": {item["markdownFile"] for item in packages},
        "coverage": {item["coverageFile"] for item in packages},
        "stored-evidence": {file_id for item in value["documents"]
                            for file_id in item["storedSourceFiles"]},
        "convenience-derivative": {file_id for item in value["documents"]
                                   for file_id in item["convenienceFiles"]},
        "asset": {file_id for item in value["documents"]
                  for file_id in item["assetFiles"]},
        "source-manifest": {item["sourceManifestFile"]
                            for item in value["documents"]
                            if item["sourceManifestFile"] is not None},
    }
    for role, owned in exact_role_owners.items():
        registered = {item["fileId"] for item in files if item["role"] == role}
        references = [file_id for item in value["documents"]
                      for file_id in (([item["sourceFile"]] if role == "source-xml" else []) +
                                      ([item["markdownFile"]] if role == "markdown-view" else []) +
                                      ([item["coverageFile"]] if role == "coverage" else []) +
                                      (item["storedSourceFiles"] if role == "stored-evidence" else []) +
                                      (item["convenienceFiles"] if role == "convenience-derivative" else []) +
                                      (item["assetFiles"] if role == "asset" else []) +
                                      ([item["sourceManifestFile"]]
                                       if role == "source-manifest" and
                                       item["sourceManifestFile"] is not None else []))]
        if role in {"relation-xml", "markdown-view", "coverage"}:
            references.extend(
                item[{"relation-xml": "sourceFile", "markdown-view": "markdownFile",
                      "coverage": "coverageFile"}[role]]
                for item in value["relationSets"])
        if registered != owned or len(references) != len(set(references)):
            raise StructuredSourceError(
                "%s files do not have exactly one package owner" % role)

    routers = value.get("routers")
    if not isinstance(routers, list):
        raise StructuredSourceError("router registry is malformed")
    router_ids = []
    router_paths = []
    for router in routers:
        if not isinstance(router, dict) or set(router) != _ROUTER_FIELDS:
            raise StructuredSourceError("router entry is malformed")
        router_ids.append(_stable_id(router.get("routerId"), "router id"))
        router_paths.append(safe_path(router.get("path"), "router path"))
        packages = _sorted_unique_strings(router.get("packages"), "router packages")
        if not set(packages).issubset(package_ids):
            raise StructuredSourceError("router names an unknown package")
        matching_files = [item for item in files if item["path"] == router["path"]]
        if len(matching_files) != 1 or matching_files[0]["role"] != "router":
            raise StructuredSourceError("router path does not have one registered owner")
    if router_ids != sorted(router_ids) or len(router_ids) != len(set(router_ids)) or \
            len(router_paths) != len(set(router_paths)):
        raise StructuredSourceError("router identities/paths are not unique and sorted")

    consumers = value.get("consumers")
    if not isinstance(consumers, list) or not consumers:
        raise StructuredSourceError("consumer registry is empty")
    consumer_ids = []
    for consumer in consumers:
        if not isinstance(consumer, dict) or set(consumer) != _CONSUMER_FIELDS:
            raise StructuredSourceError("consumer entry is malformed")
        consumer_ids.append(_stable_id(consumer.get("consumerId"), "consumer id"))
        packages = _sorted_unique_strings(consumer.get("packageIds"),
                                          "consumer packages", False)
        if not set(packages).issubset(package_ids):
            raise StructuredSourceError("consumer names an unknown package")
        export_path = consumer.get("exportPath")
        if export_path is not None:
            safe_path(export_path, "consumer export path")
            matches = [item for item in files if item["path"] == export_path]
            if len(matches) != 1 or matches[0]["role"] != "approved-export" or \
                    consumer.get("inputAuthority") != "approved-xml-export":
                raise StructuredSourceError("export consumer/path authority is not exact")
        elif consumer.get("inputAuthority") != "markdown-review":
            raise StructuredSourceError("review consumer authority is not exact")
    if consumer_ids != sorted(consumer_ids) or len(consumer_ids) != len(set(consumer_ids)):
        raise StructuredSourceError("consumer identities are not unique and sorted")
    declared_consumers = set(consumer_ids)
    for package in list(value["documents"]) + list(value["relationSets"]):
        if not set(package["consumers"]).issubset(declared_consumers):
            raise StructuredSourceError("package names an unknown consumer")

    taxonomy = value.get("taxonomy")
    if not isinstance(taxonomy, dict) or set(taxonomy) != _TAXONOMY_FIELDS:
        raise StructuredSourceError("path taxonomy is malformed")
    for field in _TAXONOMY_FIELDS:
        _sorted_unique_strings(taxonomy.get(field), "taxonomy " + field, False)
    expected_prior_art = sorted(
        ["A%d" % number for number in range(1, 22)] +
        ["B%d" % number for number in range(1, 11)] + ["C3", "C8"])
    if taxonomy["priorArtIds"] != expected_prior_art or \
            taxonomy["controlledRoots"] != [
                "PCT/structured-source", "US/allowance-first", "US/common",
                "US/normal-allowance", "US/prior-art", "structured_source"] or \
            taxonomy["forbiddenPaths"] != [
                "PCT/AA11393US-PCT_RAPPORTO_DEPOSITO_markdown",
                "PCT/AA11393US-PCT_office_action_markdown",
                "US/prior-art/markdown", "US/prior-art/searchable"] or \
            taxonomy["singlePrimarySuffixes"] != [".relations.xml", ".source.xml"]:
        raise StructuredSourceError("path taxonomy is not the exact operative taxonomy")
    expected_consumers = {
        "navigator-af": ("markdown-review", None),
        "navigator-na": ("markdown-review", None),
        "structured-handoff": (
            "approved-xml-export",
            "structured_source/exports/us-prosecution-current.ssp.zip"),
    }
    if {item["consumerId"]: (item["inputAuthority"], item["exportPath"])
            for item in consumers} != expected_consumers:
        raise StructuredSourceError("consumer authority registry is not exact")
    return value


def load_registry(root=ROOT, byte_source=None):
    absolute = os.path.join(root, *REGISTRY_PATH.split("/"))
    try:
        if byte_source:
            data = byte_source(absolute)
        else:
            with open(absolute, "rb") as handle:
                data = handle.read()
    except OSError as exc:
        raise StructuredSourceError("content registry is unreadable: %s" % exc) from exc
    return validate_registry(parse_json(data))


def files_by_id(value):
    return {item["fileId"]: item for item in value["files"]}
