"""Lazy package verification and one-pass recurring SSM acceptance.

Authored Markdown conversion is deliberately behind one narrow adapter call.
``structured_source.markdown.convert_authored_markdown`` accepts the authority
bytes, authority path, and package identity.  Its current result carries the
generated XML, semantic back-render, and exact fragment identities/digests.
Verification consumes that evidence in memory and never serializes or publishes
a coverage artifact.
"""

from __future__ import annotations

from collections import Counter
import ast
import importlib
import os
import re

from . import CONTENT_NAMESPACE, RELATIONS_NAMESPACE
from .acceptance import load_registry as load_acceptance_registry
from .acceptance_callbacks import CALLBACKS
from .atomic import publish_set
from .canonical import raw_digest
from .control import canonical_json, control_digest, parse_json
from .errors import StructuredSourceError
from .registry import (consumer_edge, files_by_id, load_registry,
                       packages_by_id, safe_path)

C = "{%s}" % CONTENT_NAMESPACE
R = "{%s}" % RELATIONS_NAMESPACE
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMAND_POLICY_PATH = "structured_source/policy/commands.json"
ACCEPTANCE_PATH = "AA11393US-structured-source-markdown_acceptance-criteria.md"

COMMAND_CAPABILITIES = {
    "check": (
        ["content-registry", "target-package", "declared-dependencies",
         "schemas", "profiles", "derived-representation"], []),
    "regenerate": (
        ["content-registry", "target-package", "declared-dependencies",
         "schemas", "profiles", "derived-representation"],
        ["derived-representation"]),
    "regenerate-controls": (
        ["content-registry", "acceptance-registry", "routers",
         "acceptance-table"],
        ["routers", "acceptance-table"]),
    "verify-callback": (["complete-repository-snapshot"], []),
    "verify-current": (["complete-repository-snapshot"], []),
}

_ANCHOR = re.compile(br'id="ssp-([A-Za-z][A-Za-z0-9_.:-]*)"')
_RETIRED_PATH_PATTERNS = (
    re.compile(r"(?:^|/)structured_source/approvals(?:/|$)"),
    re.compile(r"(?:^|/)structured_source/exports(?:/|$)"),
    re.compile(r"(?:^|/)structured_source/exporter\.py\Z"),
    re.compile(r"(?:^|/)structured_source/(?:compat|compatibility|migrate|migration)"
               r"(?:\.py|/)"),
    re.compile(r"(?:^|/)structured_source/tests/test_"
               r"(?:approvals|compatibility|exporter|migration|projection)\.py\Z"),
    re.compile(r"\.coverage\.json\Z"),
    re.compile(r"structured-source-markdown_implementation-register"),
)
_EXTRACTION_METHODS = frozenset({
    "born-digital-text-with-structured-review",
    "registered-text-transcription",
    "registered-transcription",
})
_STORED_SOURCE_ROLES = frozenset({
    "pct-cited-art-copy", "pct-filing-record",
    "pct-international-search-record", "prior-art-evidence-copy",
})
_OFFICIAL_COPY_STATUSES = frozenset({
    "filed-record-copy", "office-record-copy",
    "repository-stored-cited-art-copy", "repository-stored-evidence-copy",
})


def _parse_artifact(data, kind):
    # Keep registry/acceptance controls usable before the locked XML runtime is
    # imported; conversion paths still fail immediately if it is unavailable.
    from .parser import parse_artifact
    return parse_artifact(data, kind)


def _render_content(*args, **kwargs):
    from .render import render_content
    return render_content(*args, **kwargs)


def _render_relations(*args, **kwargs):
    from .render import render_relations
    return render_relations(*args, **kwargs)


def validate_command_policy(value):
    expected = {
        "commandPolicyVersion": "1",
        "commands": [
            {"id": command, "reads": reads, "writes": writes}
            for command, (reads, writes) in sorted(COMMAND_CAPABILITIES.items())
        ],
    }
    if value != expected:
        raise StructuredSourceError(
            "structured-source command policy is not exact")
    return value


class Reader:
    """Snapshot-capable controlled reader with an exact per-path read log."""

    def __init__(self, root, byte_source=None):
        self.root = os.path.abspath(root)
        if not os.path.isdir(self.root) or os.path.islink(self.root):
            raise StructuredSourceError(
                "controlled reader root is absent or a symlink")
        if byte_source is not None and not callable(byte_source):
            raise StructuredSourceError("byte source must be callable")
        self.byte_source = byte_source
        self.read_log = {}

    def absolute(self, path):
        path = safe_path(path)
        absolute = os.path.abspath(os.path.join(self.root, *path.split("/")))
        if os.path.commonpath((self.root, absolute)) != self.root:
            raise StructuredSourceError("controlled path escapes the repository")
        return absolute

    def read(self, path):
        absolute = self.absolute(path)
        try:
            if self.byte_source is not None:
                data = self.byte_source(absolute)
            else:
                probe = self.root
                for part in safe_path(path).split("/"):
                    probe = os.path.join(probe, part)
                    if os.path.islink(probe):
                        raise StructuredSourceError(
                            "controlled path contains a symlink: %s" % path)
                with open(absolute, "rb") as handle:
                    data = handle.read()
        except StructuredSourceError:
            raise
        except Exception as exc:
            raise StructuredSourceError(
                "controlled file is unreadable: %s" % path) from exc
        if not isinstance(data, bytes):
            raise StructuredSourceError("controlled reader returned non-bytes")
        digest = raw_digest(data)
        previous = self.read_log.setdefault(path, digest)
        if previous != digest:
            raise StructuredSourceError(
                "controlled file changed between reads: %s" % path)
        return data

    def read_absolute(self, absolute):
        relative = os.path.relpath(
            os.path.abspath(absolute), self.root).replace(os.sep, "/")
        return self.read(relative)

    def optional(self, path):
        try:
            return self.read(path)
        except StructuredSourceError:
            if self.byte_source is None and not os.path.lexists(
                    self.absolute(path)):
                return None
            raise


def _plain_text(node):
    pieces = []
    for item in node.iter():
        local = item.tag.rsplit("}", 1)[-1]
        if local in {"text", "string", "code", "math"} and item.text:
            pieces.append(item.text)
        elif local in {"space", "softBreak", "lineBreak"}:
            pieces.append(" ")
    return re.sub(r"\s+", " ", "".join(pieces)).strip()


def _conversion_value(result, name):
    if isinstance(result, dict):
        return result.get(name)
    return getattr(result, name, None)


class VerificationContext:
    """Lazy target verifier; ``verify_all`` is separately memoized."""

    def __init__(self, root=ROOT, *, registry=None, byte_source=None,
                 repository_snapshot=None, markdown_adapter=None):
        self.root = os.path.abspath(root)
        self.reader = Reader(root, byte_source)
        self.repository_snapshot = repository_snapshot
        self.registry = (load_registry(root, self.reader.read_absolute)
                         if registry is None else registry)
        # Fixture registries receive the same fail-closed validation through
        # these index helpers' caller, without requiring a live registry file.
        from .registry import validate_registry
        validate_registry(self.registry)
        self.files = files_by_id(self.registry)
        self.packages = packages_by_id(self.registry)
        self.markdown_adapter = markdown_adapter
        self._artifacts = {}
        self._fragments = {}
        self._package_results = {}
        self._global_result = None
        self._global_passes = 0

    def file_path(self, file_id):
        try:
            return self.files[file_id]["path"]
        except KeyError as exc:
            raise StructuredSourceError("unknown registered file") from exc

    def _artifact(self, package_id):
        cached = self._artifacts.get(package_id)
        if cached is not None:
            return cached
        try:
            package = self.packages[package_id]
        except KeyError as exc:
            raise StructuredSourceError("package identity does not resolve") from exc
        kind = {
            "pdf-evidence-transcription-v1": "content-document",
            "authored-markdown-v1": "authored-document",
            "authored-relations-v1": "relation-set",
        }[package["authorityScheme"]]
        artifact = _parse_artifact(
            self.reader.read(self.file_path(package["xmlFile"])), kind)
        if kind == "relation-set":
            identity = artifact.root.find(R + "identity")
            actual = identity.get("relationSetId") if identity is not None else None
        else:
            identity = artifact.root.find(C + "documentIdentity")
            actual = identity.get("documentId") if identity is not None else None
        if actual != package_id:
            raise StructuredSourceError(
                "package and XML identities do not match")
        self._artifacts[package_id] = artifact
        if kind in {"content-document", "authored-document"}:
            markdown_path = self.file_path(package["markdownFile"])
            for node in artifact.root.iter():
                identifier = node.get(XML_ID)
                if identifier:
                    key = (package_id, identifier)
                    if key in self._fragments:
                        raise StructuredSourceError("fragment identity is duplicated")
                    self._fragments[key] = {
                        "digest": artifact.fragment_digests[identifier],
                        "excerpt": _plain_text(node),
                        "markdownPath": markdown_path,
                    }
        return artifact

    def _markdown_converter(self):
        if self.markdown_adapter is not None:
            callback = getattr(
                self.markdown_adapter, "convert_authored_markdown",
                self.markdown_adapter if callable(self.markdown_adapter) else None)
        else:
            try:
                module = importlib.import_module("structured_source.markdown")
            except ImportError as exc:
                raise StructuredSourceError(
                    "authored Markdown converter is unavailable") from exc
            callback = getattr(module, "convert_authored_markdown", None)
        if not callable(callback):
            raise StructuredSourceError(
                "authored Markdown converter does not expose the current API")
        return callback

    def _manifest(self, package):
        manifest_path = self.file_path(package["sourceManifestFile"])
        data = self.reader.read(manifest_path)
        value = parse_json(data)
        if data != canonical_json(value) or not isinstance(value, dict) or \
                set(value) != {"assets", "convenienceDerivatives", "documentId",
                               "extractionMethod", "manifestVersion",
                               "storedSource"} or \
                value.get("manifestVersion") != "1" or \
                value.get("documentId") != package["packageId"] or \
                value.get("extractionMethod") not in _EXTRACTION_METHODS:
            raise StructuredSourceError("PDF source manifest is malformed")
        stored_path = self.file_path(package["storedSourceFiles"][0])
        stored = value.get("storedSource")
        stored_bytes = self.reader.read(stored_path)
        if not isinstance(stored, dict) or set(stored) != {
                "officialCopyStatus", "path", "rawDigest", "role", "size"} or \
                stored.get("path") != stored_path or \
                stored.get("rawDigest") != raw_digest(stored_bytes) or \
                stored.get("size") != len(stored_bytes) or \
                stored.get("role") not in _STORED_SOURCE_ROLES or \
                stored.get("officialCopyStatus") not in \
                _OFFICIAL_COPY_STATUSES:
            raise StructuredSourceError("PDF source manifest binding is stale")
        convenience_paths = {
            self.file_path(file_id) for file_id in package["convenienceFiles"]}
        convenience = value.get("convenienceDerivatives", [])
        if not isinstance(convenience, list) or \
                not all(isinstance(entry, dict) and set(entry) == {
                    "nonAuthoritative", "path", "rawDigest", "role", "size"}
                        for entry in convenience) or \
                [entry["path"] for entry in convenience] != \
                sorted(convenience_paths) or \
                {entry["path"] for entry in convenience} != convenience_paths:
            raise StructuredSourceError(
                "PDF convenience-derivative manifest is stale")
        for entry in convenience:
            path = entry["path"]
            content = self.reader.read(path)
            if entry.get("nonAuthoritative") is not True or \
                    entry.get("rawDigest") != raw_digest(content) or \
                    entry.get("size") != len(content) or \
                    entry.get("role") != "non-authoritative-text-aid":
                raise StructuredSourceError(
                    "PDF convenience derivative is stale or misclassified")
        asset_paths = {
            self.file_path(file_id) for file_id in package["assetFiles"]}
        assets = value.get("assets")
        if not isinstance(assets, list) or \
                not all(isinstance(entry, dict) and set(entry) == {
                    "assetId", "path", "rawDigest", "size"}
                        for entry in assets) or \
                [entry["path"] for entry in assets] != sorted(asset_paths) or \
                {entry["path"] for entry in assets} != asset_paths:
            raise StructuredSourceError("PDF asset manifest is stale")
        asset_ids = []
        for entry in assets:
            path = entry["path"]
            content = self.reader.read(path)
            asset_id = entry.get("assetId")
            if not isinstance(asset_id, str) or \
                    re.fullmatch(r"[a-z][a-z0-9-]{0,159}", asset_id) is None or \
                    entry.get("rawDigest") != raw_digest(content) or \
                    entry.get("size") != len(content):
                raise StructuredSourceError("PDF asset binding is stale")
            asset_ids.append(asset_id)
        if len(asset_ids) != len(set(asset_ids)):
            raise StructuredSourceError("PDF asset identity is duplicated")
        return value

    def _render_pdf(self, package, artifact, manifest):
        assets = {entry["assetId"]: entry["path"]
                  for entry in manifest["assets"]}
        used_assets = {
            node.get("assetId") for node in artifact.root.iter(C + "image")}
        if set(assets) != used_assets:
            raise StructuredSourceError(
                "PDF XML/manifest asset census is not exact")
        return _render_content(
            artifact, self.file_path(package["markdownFile"]), assets).markdown

    def _render_relation(self, package, artifact):
        views = {}
        assertions = set()
        relation_ids = []
        field_count = 0
        for relation in artifact.root.findall(R + "relation"):
            relation_ids.append(relation.get("relationId"))
            fields = tuple((entry.get("name"), entry.text or "")
                           for entry in relation.findall(R + "assertionField"))
            field_count += len(fields)
            endpoints = tuple(
                (entry.get("role"), entry.get("documentId"),
                 entry.get("fragmentId"), entry.get("fragmentContentDigest"))
                for entry in relation.findall(R + "endpoint"))
            assertion = (
                relation.get("type"), relation.get("direction"), fields,
                tuple(sorted(endpoints)))
            if assertion in assertions:
                raise StructuredSourceError(
                    "relation assertion has duplicate semantic ownership")
            assertions.add(assertion)
            if len({endpoint[1:] for endpoint in endpoints}) != len(endpoints):
                raise StructuredSourceError("relation endpoint is duplicated")
            for unused_role, document_id, fragment_id, digest in endpoints:
                if document_id not in self.packages or \
                        self.packages[document_id]["authorityScheme"] == \
                        "authored-relations-v1":
                    raise StructuredSourceError(
                        "relation endpoint document is not a content package")
                self.check(document_id)
                self._artifact(document_id)
                fragment = self._fragments.get((document_id, fragment_id))
                if fragment is None or fragment["digest"] != digest:
                    raise StructuredSourceError(
                        "relation endpoint does not resolve exactly")
                views[(document_id, fragment_id, digest)] = {
                    "excerpt": fragment["excerpt"],
                    "markdownPath": fragment["markdownPath"],
                }
        if len(relation_ids) != len(set(relation_ids)):
            raise StructuredSourceError("relation identity is duplicated")
        markdown = _render_relations(
            artifact, self.file_path(package["markdownFile"]), views).markdown
        return markdown, len(assertions), field_count, sum(
            len(relation.findall(R + "endpoint"))
            for relation in artifact.root.findall(R + "relation"))

    def _derive(self, package_id):
        package = self.packages[package_id]
        scheme = package["authorityScheme"]
        xml_path = self.file_path(package["xmlFile"])
        markdown_path = self.file_path(package["markdownFile"])
        if scheme == "authored-markdown-v1":
            markdown = self.reader.read(markdown_path)
            conversion = self._markdown_converter()(
                markdown, markdown_path, package_id)
            xml = _conversion_value(conversion, "xml")
            item_ids = _conversion_value(conversion, "item_ids")
            generated_markdown = _conversion_value(conversion, "markdown")
            source_digest = _conversion_value(
                conversion, "source_raw_digest")
            generated_markdown_digest = _conversion_value(
                conversion, "generated_markdown_raw_digest")
            conversion_semantic_digest = _conversion_value(
                conversion, "semantic_digest")
            conversion_fragments = _conversion_value(
                conversion, "fragment_digests")
            if not isinstance(xml, bytes) or \
                    not isinstance(item_ids, tuple) or not item_ids or \
                    not isinstance(generated_markdown, bytes) or \
                    source_digest != raw_digest(markdown) or \
                    generated_markdown_digest != raw_digest(
                        generated_markdown):
                raise StructuredSourceError(
                    "authored Markdown conversion is incomplete")
            artifact = _parse_artifact(xml, "authored-document")
            identity = artifact.root.find(C + "documentIdentity")
            if identity is None or identity.get("documentId") != package_id:
                raise StructuredSourceError(
                    "generated authored XML identity is stale")
            if artifact.semantic_digest != conversion_semantic_digest or \
                    artifact.fragment_digests != conversion_fragments or \
                    set(artifact.fragment_digests) != set(item_ids) or \
                    len(item_ids) != len(set(item_ids)):
                raise StructuredSourceError(
                    "authored Markdown computed item/XML coverage is incomplete")
            return xml_path, xml, {
                "scheme": scheme, "coveredItems": len(item_ids),
                "backRender": "equal",
            }

        artifact = self._artifact(package_id)
        if scheme == "pdf-evidence-transcription-v1":
            manifest = self._manifest(package)
            generated = self._render_pdf(package, artifact, manifest)
            content = artifact.root.find(C + "content")
            content_ids = {
                node.get(XML_ID) for node in content.iter()
                if node.get(XML_ID)}
            evidence_ids = [
                entry.get("fragmentId") for entry in artifact.root.findall(
                    C + "provenance/" + C + "fragmentEvidence")]
            evidence_paths = {
                entry.get("sourcePath") for entry in artifact.root.findall(
                    C + "provenance/" + C + "fragmentEvidence")}
            anchors = {
                match.group(1).decode("ascii") for match in _ANCHOR.finditer(generated)}
            if set(evidence_ids) != content_ids or \
                    len(evidence_ids) != len(set(evidence_ids)) or \
                    not content_ids.issubset(anchors) or \
                    evidence_paths != {manifest["storedSource"]["path"]}:
                raise StructuredSourceError(
                    "PDF computed item/provenance/Markdown coverage is incomplete")
            return markdown_path, generated, {
                "scheme": scheme, "coveredItems": len(content_ids),
                "storedSources": 1,
            }

        generated, assertions, fields, endpoints = self._render_relation(
            package, artifact)
        anchors = {
            match.group(1).decode("ascii") for match in _ANCHOR.finditer(generated)}
        relation_ids = {
            relation.get(XML_ID) for relation in artifact.root.findall(R + "relation")}
        if not relation_ids.issubset(anchors):
            raise StructuredSourceError(
                "relation computed Markdown coverage is incomplete")
        return markdown_path, generated, {
            "scheme": scheme, "coveredItems": assertions + fields,
            "assertions": assertions, "assertionFields": fields,
            "endpoints": endpoints,
        }

    def check(self, package_id):
        if package_id not in self.packages:
            raise StructuredSourceError("subject identity does not resolve")
        cached = self._package_results.get(package_id)
        if cached is not None:
            return cached
        output_path, generated, evidence = self._derive(package_id)
        current = self.reader.read(output_path)
        if current != generated:
            raise StructuredSourceError(
                "generated representation is stale: %s" % package_id)
        result = {
            "packageId": package_id,
            "authorityScheme": self.packages[package_id]["authorityScheme"],
            "status": "conformant",
            "computedCoverage": evidence,
        }
        self._package_results[package_id] = result
        return result

    def regenerate(self, package_id):
        if package_id not in self.packages:
            raise StructuredSourceError("subject identity does not resolve")
        output_path, generated, unused_evidence = self._derive(package_id)
        current = self.reader.optional(output_path)
        # _derive has already parsed and validated the authority-side input and
        # the complete proposed representation before this first write.
        guards = {
            path: self.reader.read(path)
            for path in tuple(self.reader.read_log)
            if path != output_path
        }
        publish_set(
            self.root, {output_path: generated}, {output_path: current}, guards)
        self.reader.read_log.pop(output_path, None)
        self._package_results.clear()
        self._artifacts.clear()
        self._fragments.clear()
        self._global_result = None
        return self.check(package_id)

    def read_for_consumer(self, consumer_id, package_id):
        """Resolve exactly one declared representation, with no fallback."""
        edge = consumer_edge(self.registry, consumer_id, package_id)
        package = self.packages[package_id]
        representation = edge["inputRepresentation"]
        file_id = package["xmlFile" if representation == "xml" else "markdownFile"]
        path = self.file_path(file_id)
        data = self.reader.read(path)
        dependencies = {
            self.file_path(file_id): self.reader.read(self.file_path(file_id))
            for file_id in edge["dependencies"]}
        return {
            "consumerId": consumer_id,
            "packageId": package_id,
            "authorityScheme": package["authorityScheme"],
            "inputRepresentation": representation,
            "representationRole": self.files[file_id]["role"],
            "path": path,
            "bytes": data,
            "dependencies": dependencies,
        }

    def _snapshot_paths(self):
        if self.repository_snapshot is None:
            return None
        entries = getattr(self.repository_snapshot, "entries", None)
        if not isinstance(entries, tuple):
            raise StructuredSourceError("repository snapshot inventory is malformed")
        paths = [getattr(entry, "path", None) for entry in entries]
        if any(not isinstance(path, str) for path in paths):
            raise StructuredSourceError("repository snapshot path is malformed")
        return set(paths)

    def _disk_paths(self):
        snapshot = self._snapshot_paths()
        if snapshot is not None:
            return snapshot
        paths = set()
        for controlled_root in self.registry["taxonomy"]["controlledRoots"]:
            absolute = self.reader.absolute(controlled_root)
            if not os.path.isdir(absolute) or os.path.islink(absolute):
                raise StructuredSourceError(
                    "controlled root is absent or not a directory")
            for directory, dirnames, filenames in os.walk(
                    absolute, followlinks=False):
                dirnames[:] = sorted(name for name in dirnames
                                     if name != "__pycache__")
                if any(os.path.islink(os.path.join(directory, name))
                       for name in dirnames):
                    raise StructuredSourceError(
                        "controlled root contains a directory symlink")
                for name in filenames:
                    path = os.path.join(directory, name)
                    if os.path.islink(path) or not os.path.isfile(path):
                        raise StructuredSourceError(
                            "controlled root contains a non-regular file")
                    paths.add(os.path.relpath(path, self.root).replace(os.sep, "/"))
        return paths

    def _reject_retired_imports(self, repository_paths):
        retired_modules = {
            "structured_source.approvals", "structured_source.compat",
            "structured_source.compatibility", "structured_source.exporter",
            "structured_source.migrate", "structured_source.migration",
        }
        for path in sorted(
                item for item in repository_paths
                if item.startswith("structured_source/") and
                item.endswith(".py")):
            try:
                tree = ast.parse(
                    self.reader.read(path).decode("utf-8"), filename=path)
            except (SyntaxError, UnicodeDecodeError) as exc:
                raise StructuredSourceError(
                    "registered implementation source is not valid UTF-8 Python: %s" %
                    path) from exc
            for node in ast.walk(tree):
                imported = []
                if isinstance(node, ast.Import):
                    imported = [entry.name for entry in node.names]
                elif isinstance(node, ast.ImportFrom):
                    module_parts = (node.module or "").split(".") \
                        if node.module else []
                    if node.level:
                        source_parts = path[:-3].split("/")
                        package_parts = source_parts[:-1]
                        keep = len(package_parts) - (node.level - 1)
                        module_parts = package_parts[:max(0, keep)] + \
                            module_parts
                    module = ".".join(module_parts)
                    imported = ([module] if module else []) + [
                        (module + "." if module else "") + entry.name
                        for entry in node.names]
                if any(name in retired_modules or any(
                        name.startswith(module + ".")
                        for module in retired_modules)
                       for name in imported):
                    raise StructuredSourceError(
                        "retired structured-source import remains: %s" % path)

    def _package_artifact_paths(self, repository_paths):
        """Discover package-like paths without inventorying unrelated files."""
        controlled_roots = self.registry["taxonomy"]["controlledRoots"]
        repository_paths = {
            path for path in repository_paths
            if any(path == root or path.startswith(root.rstrip("/") + "/")
                   for root in controlled_roots)}
        package_directories = set()
        for package in self.packages.values():
            for field in ("xmlFile", "markdownFile", "sourceManifestFile"):
                file_id = package[field]
                if file_id is not None:
                    path = self.file_path(file_id)
                    directory = path.rpartition("/")[0]
                    if directory:
                        package_directories.add(directory)

        candidates = set()
        for path in repository_paths:
            basename = path.rsplit("/", 1)[-1]
            in_package_directory = any(
                path.startswith(directory + "/")
                for directory in package_directories)
            package_spelling = path.endswith((
                ".source.xml", ".relations.xml", ".coverage.json")) or \
                basename == "source-manifest.json" or \
                (basename.startswith("AA11393US-") and
                 basename.endswith(".md"))
            generated_markdown = False
            if path.endswith(".md") and not in_package_directory:
                data = self.reader.read(path)
                generated_markdown = data.startswith((
                    b"<!-- GENERATED REVIEW PROJECTION",
                    b"<!-- GENERATED RELATION REVIEW PROJECTION",
                    b"<!-- GENERATED ROUTER"))
            if in_package_directory or package_spelling or generated_markdown:
                candidates.add(path)
        return candidates

    def _control_closure(self):
        repository_paths = self._disk_paths()
        retired = sorted(
            path for path in repository_paths
            if any(pattern.search(path) for pattern in _RETIRED_PATH_PATTERNS))
        if retired:
            raise StructuredSourceError(
                "retired structured-source path remains: %s" % retired[:10])
        self._reject_retired_imports(repository_paths)
        registered = {entry["path"] for entry in self.registry["files"]}
        if self.repository_snapshot is not None:
            missing = registered - repository_paths
        else:
            missing = {
                path for path in registered
                if os.path.islink(self.reader.absolute(path)) or
                not os.path.isfile(self.reader.absolute(path))}
        if missing:
            raise StructuredSourceError(
                "registered current files are absent: %s" % sorted(missing)[:10])
        orphans = self._package_artifact_paths(repository_paths) - registered
        if orphans:
            raise StructuredSourceError(
                "unregistered package artifacts remain: %s" %
                sorted(orphans)[:10])
        for path in self.registry["taxonomy"]["forbiddenPaths"]:
            if any(item == path or item.startswith(path.rstrip("/") + "/")
                   for item in repository_paths):
                raise StructuredSourceError(
                    "forbidden current path remains: %s" % path)
        policy_bytes = self.reader.read(COMMAND_POLICY_PATH)
        policy = validate_command_policy(parse_json(policy_bytes))
        if policy_bytes != canonical_json(policy):
            raise StructuredSourceError("command policy bytes are not canonical")
        acceptance = load_acceptance_registry(
            self.root, self.reader.read_absolute)
        from .acceptance import render_table
        from .routers import render_all
        for path, expected in render_all(self.registry).items():
            if self.reader.read(path) != expected:
                raise StructuredSourceError(
                    "registered package router is stale: %s" % path)
        text = self.reader.read(ACCEPTANCE_PATH).decode("utf-8")
        start = "<!-- SSM-AC-TABLE:START -->\n"
        end = "<!-- SSM-AC-TABLE:END -->"
        if text.count(start) != 1 or text.count(end) != 1 or \
                text.split(start, 1)[1].split(end, 1)[0] != \
                render_table(acceptance):
            raise StructuredSourceError("operative acceptance table is stale")
        return acceptance, policy

    def verify_all(self):
        if self._global_result is not None:
            return self._global_result
        self._global_passes += 1
        acceptance, policy = self._control_closure()
        results = [self.check(package_id) for package_id in sorted(self.packages)]
        schemes = Counter(result["authorityScheme"] for result in results)
        covered = sum(result["computedCoverage"].get("coveredItems", 0)
                      for result in results)
        self._global_result = {
            "status": "conformant",
            "packages": len(results),
            "authoritySchemes": dict(sorted(schemes.items())),
            "computedCoveredItems": covered,
            "consumerEdges": sum(len(consumer["edges"])
                                 for consumer in self.registry["consumers"]),
            "commands": len(policy["commands"]),
            "criteria": len(acceptance["criteria"]),
            "globalPasses": self._global_passes,
            "retiredResidue": 0,
        }
        return self._global_result

    def evidence_for(self, criterion):
        if criterion not in {"SSM-AC-%02d" % number for number in range(1, 11)}:
            raise StructuredSourceError("acceptance criterion is not current")
        result = self.verify_all()
        return {
            "criterion": criterion,
            "status": result["status"],
            "packages": result["packages"],
            "computedCoveredItems": result["computedCoveredItems"],
            "consumerEdges": result["consumerEdges"],
            "globalPasses": result["globalPasses"],
            "retiredResidue": result["retiredResidue"],
        }


def run_acceptance(root=ROOT, *, byte_source=None, repository_snapshot=None,
                   registry=None, markdown_adapter=None):
    """Return ephemeral machine conformance for one supplied snapshot."""
    context = VerificationContext(
        root, registry=registry, byte_source=byte_source,
        repository_snapshot=repository_snapshot,
        markdown_adapter=markdown_adapter)
    acceptance = load_acceptance_registry(root, context.reader.read_absolute)
    results = []
    for criterion in acceptance["criteria"]:
        callback_name = criterion["callbacks"][0]
        evidence = CALLBACKS[callback_name](context)
        if not isinstance(evidence, dict) or \
                evidence.get("criterion") != criterion["code"] or \
                evidence.get("status") != "conformant":
            raise StructuredSourceError(
                "acceptance callback did not prove its current criterion")
        results.append({
            "criterion": criterion["code"],
            "callback": callback_name,
            "status": "satisfied",
            "evidenceDigest": control_digest(evidence),
        })
    if len(results) != 10 or {entry["callback"] for entry in results} != set(CALLBACKS):
        raise StructuredSourceError(
            "acceptance result callback census is incomplete")
    return {
        "verificationResultVersion": "1",
        "namespace": "ssp",
        "repositorySnapshot": getattr(repository_snapshot, "digest", None),
        "status": "conformant",
        "results": results,
    }
