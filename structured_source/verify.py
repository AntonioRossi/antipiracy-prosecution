"""Read-only recurring structured-source closure and callback receipt."""

from __future__ import annotations

from collections import Counter
import hashlib
from html import unescape as html_unescape
import json
import os
import posixpath
import re
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET

from . import CONTENT_NAMESPACE, RELATIONS_NAMESPACE
from .acceptance import load_registry as load_acceptance_registry
from .acceptance_callbacks import CALLBACKS
from .approvals import (INVENTORY_PATH, load_authorities, load_inventory, load_records,
                        resolve_current)
from .canonical import raw_digest, registered_kinds
from .control import canonical_json, control_digest, parse_json
from .environment import verify_environment
from .errors import StructuredSourceError
from .exporter import verify_export
from .parser import parse_artifact
from .profiles import load_projection_profile
from .registry import (REGISTRY_PATH, files_by_id, load_registry,
                       safe_path, validate_registry)
from .render import render_content, render_relations
from .routers import render_all

C = "{%s}" % CONTENT_NAMESPACE
R = "{%s}" % RELATIONS_NAMESPACE
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
_RAW = re.compile(r"sha256/raw:[0-9a-f]{64}\Z")
_SEMANTIC = re.compile(r"sha256/xc1/ssp-xd1:[0-9a-f]{64}\Z")
_CONTROL = re.compile(r"sha256/c1:[0-9a-f]{64}\Z")
_TEXT_SUFFIXES = {".json", ".md", ".py", ".toml", ".txt", ".xsd",
                  ".yaml", ".yml"}
_EXCLUDED_DIRS = {".git", ".venv", ".uv-cache", "__pycache__"}
_HTML_ID = re.compile(r"\bid=(['\"])(.*?)\1", re.IGNORECASE)
_COMMAND_CAPABILITIES = {
    "approve": (
        ["content-registry", "approval-authorities", "record-inventory",
         "source-xml", "relation-xml", "schemas", "profiles", "dependencies",
         "assets", "markdown", "coverage", "approvals"],
        ["approval-record", "record-inventory"]),
    "check-source": (
        ["content-registry", "source-xml", "schemas", "profiles",
         "dependencies", "assets"], []),
    "compare": (
        ["content-registry", "source-xml", "relation-xml", "schemas",
         "profiles", "dependencies", "assets", "markdown", "coverage"], []),
    "export": (
        ["content-registry", "approval-authorities", "record-inventory",
         "source-xml", "relation-xml", "schemas", "profiles", "dependencies",
         "assets", "markdown", "coverage", "approvals"],
        ["approved-export"]),
    "render": (
        ["content-registry", "source-xml", "relation-xml", "schemas",
         "profiles", "dependencies", "assets"],
        ["markdown", "coverage"]),
    "render-census": (
        ["content-registry", "source-xml", "relation-xml", "schemas",
         "profiles", "dependencies", "assets"], []),
    "resolve-approvals": (
        ["content-registry", "approval-authorities", "record-inventory",
         "source-xml", "relation-xml", "schemas", "profiles", "dependencies",
         "assets", "markdown", "coverage", "approvals"], []),
    "verify-callback": (["complete-repository-snapshot"], []),
    "verify-current": (["complete-repository-snapshot"], []),
}


def validate_command_policy(policy):
    expected = {
        "commandPolicyVersion": "1",
        "commands": [
            {"id": command_id, "reads": reads, "writes": writes}
            for command_id, (reads, writes) in
            sorted(_COMMAND_CAPABILITIES.items())
        ],
    }
    if policy != expected:
        raise StructuredSourceError(
            "command-plane registry/capabilities are not exact")
    return policy


def _walk_pandoc(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk_pandoc(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_pandoc(child)


def _pandoc_links_and_anchors(value):
    links = []
    anchors = []
    for node in _walk_pandoc(value):
        kind = node.get("t")
        content = node.get("c")
        if kind in {"Link", "Image"} and isinstance(content, list) and \
                len(content) == 3 and isinstance(content[2], list) and content[2]:
            links.append(content[2][0])
        if kind in {"Header", "CodeBlock", "Div", "Span"} and \
                isinstance(content, list) and len(content) > 1 and \
                isinstance(content[1 if kind == "Header" else 0], list):
            attributes = content[1 if kind == "Header" else 0]
            if attributes and attributes[0]:
                anchors.append(attributes[0])
        if kind in {"RawBlock", "RawInline"} and isinstance(content, list) and \
                len(content) == 2 and content[0] == "html":
            anchors.extend(html_unescape(match.group(2))
                           for match in _HTML_ID.finditer(content[1]))
    return links, anchors


class Reader:
    def __init__(self, root, byte_source=None):
        self.root = os.path.abspath(root)
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
            data = self.byte_source(absolute) if self.byte_source else open(absolute, "rb").read()
        except (OSError, KeyError) as exc:
            raise StructuredSourceError("controlled file is unreadable: %s" % path) from exc
        self.read_log[path] = raw_digest(data)
        return data

    def exists(self, path):
        try:
            self.read(path)
            return True
        except StructuredSourceError:
            return False


def _file_id(path):
    return "file-" + hashlib.sha256(path.encode("utf-8")).hexdigest()[:24]


def _plain_text(node):
    pieces = []
    for item in node.iter():
        local = item.tag.rsplit("}", 1)[-1]
        if local in {"text", "code", "math"} and item.text:
            pieces.append(item.text)
        elif local in {"space", "softBreak", "lineBreak"}:
            pieces.append(" ")
    return re.sub(r"\s+", " ", "".join(pieces)).strip()


class VerificationContext:
    def __init__(self, root, byte_source=None, repository_snapshot=None,
                 fresh_process=True):
        self.root = os.path.abspath(root)
        self.reader = Reader(root, byte_source)
        self.byte_source = byte_source
        self.repository_snapshot = repository_snapshot
        self.fresh_process = fresh_process
        self.acceptance = load_acceptance_registry(root, byte_source)
        registry_bytes = self.reader.read(REGISTRY_PATH)
        self.registry = validate_registry(parse_json(registry_bytes))
        if registry_bytes != canonical_json(self.registry):
            raise StructuredSourceError("content registry bytes are not canonical c1")
        self.files = files_by_id(self.registry)
        self.packages = {
            item.get("documentId", item.get("relationSetId")): item
            for item in self.registry["documents"] + self.registry["relationSets"]}
        if len(self.packages) != len(self.registry["documents"]) + len(self.registry["relationSets"]):
            raise StructuredSourceError("document and relation-set identities collide")
        self.artifacts = {}
        self.fragments = {}
        self.markdown_paths = {}
        self._markdown_analysis_cache = {}
        self._load_artifacts()
        self._results = {}

    def _snapshot_paths(self):
        if self.repository_snapshot is None:
            if self.byte_source is not None:
                raise StructuredSourceError(
                    "snapshot byte verification lacks its repository inventory")
            return None
        snapshot_root = os.path.abspath(
            getattr(self.repository_snapshot, "root", ""))
        digest = getattr(self.repository_snapshot, "digest", None)
        entries = getattr(self.repository_snapshot, "entries", None)
        if snapshot_root != self.root or not isinstance(digest, str) or \
                _CONTROL.fullmatch(digest) is None or not isinstance(entries, tuple):
            raise StructuredSourceError("repository snapshot binding is malformed")
        paths = [getattr(entry, "path", None) for entry in entries]
        if any(not isinstance(path, str) for path in paths) or \
                paths != sorted(paths) or len(paths) != len(set(paths)):
            raise StructuredSourceError("repository snapshot path census is malformed")
        return set(paths)

    def _markdown_analysis(self, path):
        cached = self._markdown_analysis_cache.get(path)
        if cached is not None:
            return cached
        markdown = self.reader.read(path)
        result = subprocess.run(
            ["pandoc", "--from=gfm", "--to=json"], input=markdown,
            capture_output=True, timeout=180)
        try:
            ast = json.loads(result.stdout)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise StructuredSourceError(
                "registered Markdown has no valid pinned GFM AST: %s" % path) from exc
        if result.returncode or ast.get("pandoc-api-version") != [1, 23, 1]:
            raise StructuredSourceError(
                "registered Markdown does not parse under pinned Pandoc: %s" % path)
        links, anchors = _pandoc_links_and_anchors(ast)
        if len(anchors) != len(set(anchors)):
            raise StructuredSourceError(
                "registered Markdown has duplicate fragment identities: %s" % path)
        value = (links, set(anchors))
        self._markdown_analysis_cache[path] = value
        return value

    def _resolve_markdown_target(self, source_path, target):
        try:
            parsed = urlsplit(target)
        except ValueError as exc:
            raise StructuredSourceError("registered Markdown link is malformed") from exc
        if parsed.scheme:
            if parsed.scheme not in set(load_projection_profile()["externalSchemes"]):
                raise StructuredSourceError("registered Markdown link scheme is not closed")
            return
        if parsed.netloc:
            raise StructuredSourceError("registered Markdown link has an undeclared authority")
        raw_path = unquote(parsed.path)
        if not raw_path:
            resolved = source_path
        else:
            if raw_path.startswith("/") or "\\" in raw_path:
                raise StructuredSourceError("registered Markdown link path is not relative")
            resolved = posixpath.normpath(posixpath.join(
                posixpath.dirname(source_path), raw_path))
            if resolved == ".." or resolved.startswith("../"):
                raise StructuredSourceError("registered Markdown link escapes the repository")
            if raw_path.endswith("/"):
                resolved = resolved.rstrip("/") + "/README.md"
        if not self.reader.exists(resolved):
            raise StructuredSourceError(
                "registered Markdown link is unresolved: %s -> %s" %
                (source_path, resolved))
        if not parsed.fragment:
            return
        fragment = unquote(parsed.fragment)
        if resolved.endswith(".md"):
            unused_links, anchors = self._markdown_analysis(resolved)
            if fragment not in anchors:
                raise StructuredSourceError(
                    "registered Markdown fragment is unresolved: %s#%s" %
                    (resolved, fragment))
        elif resolved.endswith(".xml"):
            data = self.reader.read(resolved)
            if ('xml:id="%s"' % fragment).encode("utf-8") not in data:
                raise StructuredSourceError(
                    "registered XML fragment is unresolved: %s#%s" %
                    (resolved, fragment))
        elif not (resolved.lower().endswith(".pdf") and
                  re.fullmatch(r"page=[1-9][0-9]*", fragment)):
            raise StructuredSourceError(
                "registered non-document fragment is unsupported: %s#%s" %
                (resolved, fragment))

    def file_path(self, file_id):
        try:
            return self.files[file_id]["path"]
        except KeyError as exc:
            raise StructuredSourceError("package references an unknown file") from exc

    def _load_artifacts(self):
        for package_id, package in sorted(self.packages.items()):
            path = self.file_path(package["sourceFile"])
            kind = "content-document" if "documentId" in package else "relation-set"
            artifact = parse_artifact(self.reader.read(path), kind)
            if artifact.semantic_digest != package["sourceDigest"]:
                raise StructuredSourceError("registered source digest is stale: %s" % package_id)
            self.artifacts[package_id] = artifact
            self.markdown_paths[package_id] = self.file_path(package["markdownFile"])
            if kind == "content-document":
                identity = artifact.root.find(C + "documentIdentity")
                if identity.get("documentId") != package_id:
                    raise StructuredSourceError("content document identity/path binding is stale")
                for node in artifact.root.iter():
                    identifier = node.get(XML_ID)
                    if identifier:
                        key = (package_id, identifier)
                        if key in self.fragments:
                            raise StructuredSourceError("global fragment tuple is duplicated")
                        self.fragments[key] = {
                            "digest": artifact.fragment_digests[identifier],
                            "text": _plain_text(node),
                            "markdownPath": self.markdown_paths[package_id],
                        }
            else:
                identity = artifact.root.find(R + "identity")
                if identity.get("relationSetId") != package_id:
                    raise StructuredSourceError("relation-set identity/path binding is stale")

    def _controlled_paths(self):
        return {item["path"] for item in self.registry["files"]}

    def _controlled_disk_paths(self):
        snapshot_paths = self._snapshot_paths()
        if snapshot_paths is not None:
            approval_prefix = "structured_source/approvals/records/"
            return {
                path for path in snapshot_paths
                if any(path == root or path.startswith(root.rstrip("/") + "/")
                       for root in self.registry["taxonomy"]["controlledRoots"])
                and not path.startswith(approval_prefix)
            }
        paths = set()
        approval_prefix = "structured_source/approvals/records/"
        for relative_root in self.registry["taxonomy"]["controlledRoots"]:
            absolute_root = self.reader.absolute(relative_root)
            if not os.path.isdir(absolute_root) or os.path.islink(absolute_root):
                raise StructuredSourceError(
                    "controlled root is absent or non-directory: %s" % relative_root)
            for directory, dirnames, filenames in os.walk(
                    absolute_root, followlinks=False):
                if any(os.path.islink(os.path.join(directory, name))
                       for name in dirnames):
                    raise StructuredSourceError("controlled tree contains a directory symlink")
                dirnames[:] = sorted(name for name in dirnames
                                     if name not in _EXCLUDED_DIRS)
                for name in sorted(filenames):
                    absolute = os.path.join(directory, name)
                    if os.path.islink(absolute) or not os.path.isfile(absolute):
                        raise StructuredSourceError(
                            "controlled tree contains a non-regular file")
                    path = os.path.relpath(absolute, self.root).replace(os.sep, "/")
                    if path.startswith(approval_prefix):
                        continue
                    paths.add(path)
        return paths

    def _check_ac01(self):
        paths = self._controlled_paths()
        for item in self.registry["files"]:
            if item["fileId"] != _file_id(item["path"]):
                raise StructuredSourceError("registry file identity is not path-derived")
            self.reader.read(item["path"])
        expected_controlled = {
            path for path in paths
            if any(path == root or path.startswith(root.rstrip("/") + "/")
                   for root in self.registry["taxonomy"]["controlledRoots"])
        }
        actual_controlled = self._controlled_disk_paths()
        if actual_controlled != expected_controlled:
            missing = sorted(expected_controlled - actual_controlled)
            additional = sorted(actual_controlled - expected_controlled)
            raise StructuredSourceError(
                "controlled filesystem inventory differs from registry: "
                "missing=%s additional=%s" % (missing[:10], additional[:10]))
        for package_id, package in self.packages.items():
            expected_consumers = {item["consumerId"] for item in self.registry["consumers"]
                                  if package_id in item["packageIds"]}
            if set(package["consumers"]) != expected_consumers:
                raise StructuredSourceError("consumer/package mapping is not bidirectional")
        inventory = load_inventory(self.root, self.byte_source)
        authorities = load_authorities(self.root, self.byte_source)
        actual_record_paths = {item["path"] for item in inventory["records"]}
        record_prefix = "structured_source/approvals/records/"
        snapshot_paths = self._snapshot_paths()
        if snapshot_paths is not None:
            disk = {path for path in snapshot_paths if path.startswith(record_prefix)}
            if any("/" in path[len(record_prefix):] for path in disk):
                raise StructuredSourceError(
                    "approval-record namespace contains a nested directory")
        else:
            record_root = os.path.join(
                self.root, "structured_source", "approvals", "records")
            disk = set()
            if os.path.lexists(record_root):
                if os.path.islink(record_root) or not os.path.isdir(record_root):
                    raise StructuredSourceError(
                        "approval-record namespace is not a directory")
                for directory, dirnames, filenames in os.walk(
                        record_root, followlinks=False):
                    if dirnames:
                        raise StructuredSourceError(
                            "approval-record namespace contains a nested directory")
                    for name in filenames:
                        path = os.path.join(directory, name)
                        if os.path.islink(path) or not os.path.isfile(path):
                            raise StructuredSourceError(
                                "approval-record namespace contains a non-regular file")
                        disk.add(os.path.relpath(path, self.root).replace(os.sep, "/"))
        if disk != actual_record_paths:
            raise StructuredSourceError("append-only approval-record inventory is not exact")
        load_records(self.root, self.byte_source)
        primary_roles = {"source-xml", "relation-xml", "markdown-view", "coverage",
                         "asset", "stored-evidence", "convenience-derivative",
                         "source-manifest", "router", "approved-export"}
        if len([item for item in self.registry["files"] if item["role"] in primary_roles]) != \
                len({item["path"] for item in self.registry["files"] if item["role"] in primary_roles}):
            raise StructuredSourceError("content-plane registry has a duplicate controlled path")
        return {"controlledFiles": len(paths), "packages": len(self.packages),
                "approvalAuthorities": len(authorities["authorities"]),
                "approvalRecords": len(actual_record_paths)}

    def _check_ac02(self):
        document_ids = set(self.artifacts) - {
            item["relationSetId"] for item in self.registry["relationSets"]}
        relation_ids = set()
        claim_census = {}
        for package_id, artifact in self.artifacts.items():
            if artifact.kind == "content-document":
                package = self.packages[package_id]
                if artifact.root.get(XML_ID) != package_id + "-root":
                    raise StructuredSourceError(
                        "content document has no stable whole-document fragment")
                dependencies = artifact.root.findall(
                    C + "dependencies/" + C + "dependency")
                actual_bindings = sorted(
                    "%s|%s|%s" % (item.get("kind"), item.get("subjectId"),
                                    item.get("digest"))
                    for item in dependencies)
                if actual_bindings != package["dependencyBindings"]:
                    raise StructuredSourceError(
                        "document dependency registry binding is stale")
                asset_bindings = {
                    binding.split("|", 1)[0]: self.file_path(
                        binding.split("|", 1)[1])
                    for binding in package["assetBindings"]}
                for dependency in dependencies:
                    kind = dependency.get("kind")
                    subject = dependency.get("subjectId")
                    digest = dependency.get("digest")
                    if kind in {"document", "relation-set"}:
                        resolved = self.artifacts.get(subject)
                        if resolved is None or resolved.semantic_digest != digest or \
                                (kind == "document") != \
                                (resolved.kind == "content-document"):
                            raise StructuredSourceError(
                                "document semantic dependency does not resolve exactly")
                    elif kind == "asset":
                        path = asset_bindings.get(subject)
                        if path is None or raw_digest(self.reader.read(path)) != digest:
                            raise StructuredSourceError(
                                "document asset dependency does not resolve exactly")
                    else:
                        raise StructuredSourceError(
                            "document dependency kind is not closed")
                claims = artifact.root.findall(".//" + C + "claim")
                if claims:
                    numbers = [int(item.get("number")) for item in claims]
                    if numbers != list(range(1, len(numbers) + 1)):
                        raise StructuredSourceError("claim numbers are not complete and ordered")
                    seen_claim_ids = {item.get("claimId") for item in claims}
                    for claim in claims:
                        dependencies = [item.text for item in claim.findall(C + "dependency")]
                        if claim.get("type") == "independent" and dependencies or \
                                claim.get("type") == "dependent" and len(dependencies) != 1:
                            raise StructuredSourceError("claim dependency/type is inconsistent")
                        for dependency in dependencies:
                            if dependency not in seen_claim_ids or \
                                    int(dependency.rsplit("-", 1)[1]) >= int(claim.get("number")):
                                raise StructuredSourceError("claim dependency is illegal")
                        limitations = claim.findall(C + "limitation")
                        if not limitations or len({item.get("limitationId") for item in limitations}) != len(limitations):
                            raise StructuredSourceError("claim limitation census is incomplete")
                    claim_census[package_id] = len(claims)
            else:
                for relation in artifact.root.findall(R + "relation"):
                    key = (package_id, relation.get("relationId"))
                    if key in relation_ids or relation.get(XML_ID) != relation.get("relationId"):
                        raise StructuredSourceError("relation identity is duplicated or inconsistent")
                    relation_ids.add(key)
                    endpoints = relation.findall(R + "endpoint")
                    for endpoint in endpoints:
                        key = (endpoint.get("documentId"), endpoint.get("fragmentId"))
                        resolved = self.fragments.get(key)
                        if resolved is None or resolved["digest"] != endpoint.get("fragmentContentDigest"):
                            raise StructuredSourceError("relation endpoint tuple does not resolve exactly")
                    if len({(item.get("documentId"), item.get("fragmentId"),
                             item.get("fragmentContentDigest")) for item in endpoints}) != len(endpoints):
                        raise StructuredSourceError("relation contains a duplicate endpoint tuple")
        if registered_kinds() != tuple(sorted({
                "content-document", "content-fragment", "relation",
                "relation-context-fragment", "relation-set"})):
            raise StructuredSourceError("XML digest-domain kind registry is not exact")
        return {"documents": len(document_ids), "fragments": len(self.fragments),
                "relations": len(relation_ids), "claimCensus": claim_census}

    def _check_ac03(self):
        pdf_count = 0
        authored_count = 0
        assets = 0
        for package in self.registry["documents"]:
            package_id = package["documentId"]
            artifact = self.artifacts[package_id]
            origin = artifact.root.find(C + "origin")
            pdf = origin.find(C + "pdfDerivative")
            authored = origin.find(C + "authoredSource")
            if (pdf is None) == (authored is None):
                raise StructuredSourceError("document origin is not exactly one closed branch")
            asset_map = {}
            for binding in package["assetBindings"]:
                asset_id, file_id = binding.split("|", 1)
                path = self.file_path(file_id)
                asset_map[asset_id] = path
                assets += 1
            dependency_assets = {item.get("subjectId"): item.get("digest")
                                 for item in artifact.root.findall(
                                     C + "dependencies/" + C + "dependency")
                                 if item.get("kind") == "asset"}
            if set(asset_map) != set(dependency_assets):
                raise StructuredSourceError("asset registry and XML dependency sets differ")
            for asset_id, path in asset_map.items():
                if raw_digest(self.reader.read(path)) != dependency_assets[asset_id]:
                    raise StructuredSourceError("registered asset bytes are stale")
            if pdf is not None:
                pdf_count += 1
                stored = pdf.find(C + "storedSource")
                if stored.get("path") not in {self.file_path(item) for item in package["storedSourceFiles"]} or \
                        raw_digest(self.reader.read(stored.get("path"))) != stored.get("rawDigest") or \
                        len(self.reader.read(stored.get("path"))) != int(stored.get("size")):
                    raise StructuredSourceError("stored evidentiary source binding is stale")
                convenience = pdf.findall(C + "convenienceDerivative")
                if {item.get("path") for item in convenience} != \
                        {self.file_path(item) for item in package["convenienceFiles"]}:
                    raise StructuredSourceError("convenience-derivative registry is stale")
                for item in convenience:
                    if item.get("nonAuthoritative") != "true" or \
                            raw_digest(self.reader.read(item.get("path"))) != item.get("rawDigest") or \
                            len(self.reader.read(item.get("path"))) != int(item.get("size")):
                        raise StructuredSourceError("convenience derivative is authoritative or stale")
                content_ids = {node.get(XML_ID) for node in
                               artifact.root.find(C + "content").iter()
                               if node.get(XML_ID)}
                evidence = artifact.root.findall(C + "provenance/" + C + "fragmentEvidence")
                evidence_ids = [item.get("fragmentId") for item in evidence]
                if set(evidence_ids) != content_ids or len(evidence_ids) != len(set(evidence_ids)):
                    raise StructuredSourceError("PDF fragment provenance is not one-to-one complete")
                if any(item.get("sourcePath") != stored.get("path") or
                       int(item.get("page")) < 1 for item in evidence):
                    raise StructuredSourceError("PDF fragment provenance locator is invalid")
            else:
                authored_count += 1
                if not authored.get("responsibleOwner") or authored.get("reviewScope") != "complete-current-content":
                    raise StructuredSourceError("authored source has no truthful responsible owner/scope")
        manifests = {}
        for entry in self.registry["files"]:
            if entry["role"] != "source-manifest":
                continue
            manifest_bytes = self.reader.read(entry["path"])
            value = parse_json(manifest_bytes)
            if not isinstance(value, dict) or set(value) != {
                    "manifestVersion", "documentId", "storedSource",
                    "convenienceDerivatives", "assets"} or \
                    value.get("manifestVersion") != "1":
                raise StructuredSourceError("source manifest shape/version is not current")
            if manifest_bytes != canonical_json(value):
                raise StructuredSourceError(
                    "source manifest bytes are not canonical c1")
            document_id = value.get("documentId")
            if document_id in manifests:
                raise StructuredSourceError("source manifest has duplicate document ownership")
            package = self.packages.get(document_id)
            artifact = self.artifacts.get(document_id)
            if package is None or artifact is None or artifact.kind != "content-document":
                raise StructuredSourceError("source manifest document does not resolve")
            pdf = artifact.root.find(C + "origin/" + C + "pdfDerivative")
            if pdf is None:
                raise StructuredSourceError("source manifest belongs to a non-PDF document")
            stored = pdf.find(C + "storedSource")
            expected_stored = {
                "path": stored.get("path"), "rawDigest": stored.get("rawDigest"),
                "size": int(stored.get("size")), "role": stored.get("role"),
                "officialCopyStatus": pdf.get("officialCopyStatus"),
            }
            expected_convenience = [{
                "path": item.get("path"), "rawDigest": item.get("rawDigest"),
                "size": int(item.get("size")), "role": item.get("role"),
                "nonAuthoritative": True,
            } for item in pdf.findall(C + "convenienceDerivative")]
            expected_assets = sorted(({
                "assetId": binding.split("|", 1)[0],
                "path": self.file_path(binding.split("|", 1)[1]),
            } for binding in package["assetBindings"]),
                                     key=lambda item: item["assetId"])
            if value["storedSource"] != expected_stored or \
                    value["convenienceDerivatives"] != expected_convenience or \
                    value["assets"] != expected_assets:
                raise StructuredSourceError("source manifest is stale")
            manifests[document_id] = entry["path"]
        expected_manifests = {
            item["documentId"] for item in self.registry["documents"]
            if item["origin"] == "pdf-derivative"
        }
        if set(manifests) != expected_manifests:
            raise StructuredSourceError("source-manifest document census is not exact")
        for document_id, path in manifests.items():
            if self.file_path(
                    self.packages[document_id]["sourceManifestFile"]) != path:
                raise StructuredSourceError(
                    "source-manifest package binding is stale")
        return {"pdfDerivatives": pdf_count, "authoredSources": authored_count,
                "assetBindings": assets, "sourceManifests": len(manifests)}

    def _check_ac04(self):
        assertions = set()
        endpoint_count = 0
        for package in self.registry["relationSets"]:
            artifact = self.artifacts[package["relationSetId"]]
            actual_documents = set()
            for relation in artifact.root.findall(R + "relation"):
                fields = tuple((item.get("name"), item.text or "")
                               for item in relation.findall(R + "assertionField"))
                endpoints = tuple((item.get("role"), item.get("documentId"),
                                   item.get("fragmentId"), item.get("fragmentContentDigest"))
                                  for item in relation.findall(R + "endpoint"))
                assertion = (relation.get("type"), relation.get("direction"), fields, endpoints)
                if assertion in assertions:
                    raise StructuredSourceError("a source-level relation assertion has duplicate ownership")
                assertions.add(assertion)
                actual_documents.update(item[1] for item in endpoints)
                endpoint_count += len(endpoints)
            if sorted(actual_documents) != package["endpointDocuments"]:
                raise StructuredSourceError("relation endpoint-document allowlist is stale")
            markdown = self.reader.read(self.file_path(package["markdownFile"])).decode("utf-8")
            for relation in artifact.root.findall(R + "relation"):
                if ('id="ssp-%s"' % relation.get("relationId")) not in markdown:
                    raise StructuredSourceError("relation review view lacks a forward relation anchor")
                for endpoint in relation.findall(R + "endpoint"):
                    if "#ssp-%s" % endpoint.get("fragmentId") not in markdown:
                        raise StructuredSourceError("relation review view lacks a reverse endpoint anchor")
        return {"relationAssertions": len(assertions), "endpoints": endpoint_count}

    def _render_package(self, package_id):
        package = self.packages[package_id]
        artifact = self.artifacts[package_id]
        output_path = self.file_path(package["markdownFile"])
        if artifact.kind == "content-document":
            assets = {binding.split("|", 1)[0]: self.file_path(binding.split("|", 1)[1])
                      for binding in package["assetBindings"]}
            return render_content(artifact, output_path, assets)
        views = {}
        for endpoint in artifact.root.findall(".//" + R + "endpoint"):
            key = (endpoint.get("documentId"), endpoint.get("fragmentId"))
            resolved = self.fragments.get(key)
            if resolved is None or resolved["digest"] != endpoint.get("fragmentContentDigest"):
                raise StructuredSourceError("relation projection endpoint is stale")
            views[(key[0], key[1], resolved["digest"])] = {
                "excerpt": resolved["text"], "markdownPath": resolved["markdownPath"],
            }
        return render_relations(artifact, output_path, views)

    def render_census(self):
        census = []
        for package_id in sorted(self.packages):
            projection = self._render_package(package_id)
            census.append({"packageId": package_id,
                           "markdownDigest": projection.markdown_digest,
                           "coverageDigest": projection.coverage_digest})
        return census

    def _check_ac05(self):
        census = []
        field_count = 0
        for package_id, package in sorted(self.packages.items()):
            projection = self._render_package(package_id)
            markdown = self.reader.read(self.file_path(package["markdownFile"]))
            coverage = self.reader.read(self.file_path(package["coverageFile"]))
            if markdown != projection.markdown or coverage != projection.coverage or \
                    raw_digest(markdown) != package["markdownDigest"] or \
                    raw_digest(coverage) != package["coverageDigest"]:
                raise StructuredSourceError("committed projection/coverage is stale: %s" % package_id)
            unused_links, markdown_anchors = self._markdown_analysis(
                self.file_path(package["markdownFile"]))
            line_count = len(markdown.splitlines())
            value = parse_json(coverage)
            fields = value.get("fields") if isinstance(value, dict) else None
            profile = load_projection_profile()
            if not isinstance(value, dict) or set(value) != {
                    "coverageVersion", "subjectId", "sourceDigest", "sourceProfile",
                    "projectionProfile", "markdownDigest", "fields"} or \
                    value.get("coverageVersion") != "1" or \
                    value.get("subjectId") != package_id or \
                    value.get("sourceDigest") != self.artifacts[package_id].semantic_digest or \
                    value.get("sourceProfile") != self.artifacts[package_id].profile or \
                    value.get("projectionProfile") != profile["profileId"] or \
                    value.get("markdownDigest") != raw_digest(markdown) or \
                    not isinstance(fields, list) or not fields:
                raise StructuredSourceError("coverage field census is empty")
            field_ids = [item.get("fieldId") for item in fields if isinstance(item, dict)]
            if len(field_ids) != len(fields) or len(field_ids) != len(set(field_ids)):
                raise StructuredSourceError("coverage field identity is incomplete or duplicated")
            for item in fields:
                if item.get("classification") not in {
                        "review-visible", "review-scheduled", "mechanically-derived",
                        "internal-justified"}:
                    raise StructuredSourceError("coverage classification is not closed")
                if item["classification"] in {"review-visible", "review-scheduled"} and \
                        not item.get("anchors"):
                    raise StructuredSourceError("review field has no projection anchor")
                for anchor in item.get("anchors", []):
                    if anchor not in markdown_anchors:
                        raise StructuredSourceError(
                            "coverage anchor is absent from the generated projection")
                for region in item.get("regions", []):
                    if not isinstance(region, dict) or set(region) != {
                            "startLine", "endLine"} or \
                            not all(isinstance(region.get(name), int)
                                    for name in ("startLine", "endLine")) or \
                            region["startLine"] < 1 or \
                            region["endLine"] < region["startLine"] or \
                            region["endLine"] > line_count:
                        raise StructuredSourceError(
                            "coverage line region is outside the generated projection")
            field_count += len(fields)
            census.append({"packageId": package_id,
                           "markdownDigest": projection.markdown_digest,
                           "coverageDigest": projection.coverage_digest})
        if self.fresh_process:
            expected = canonical_json({"renderCensusVersion": "1", "packages": census})
            temporary = None
            process_root = self.root
            if self.repository_snapshot is not None:
                materialize = getattr(self.repository_snapshot, "materialize", None)
                if not callable(materialize):
                    raise StructuredSourceError(
                        "repository snapshot cannot materialize fresh-process inputs")
                temporary = tempfile.TemporaryDirectory(
                    prefix="aa11393-ssp-render-snapshot-")
                process_root = temporary.name
                materialize(process_root)
                os.symlink(sys.prefix, os.path.join(process_root, ".venv"),
                           target_is_directory=True)
            try:
                for unused in range(2):
                    result = subprocess.run(
                        [sys.executable, "-B", "-m", "structured_source",
                         "render-census"],
                        cwd=process_root, capture_output=True, timeout=900,
                        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
                    if result.returncode or result.stdout != expected:
                        raise StructuredSourceError(
                            "fresh-process render census is not reproducible")
            finally:
                if temporary is not None:
                    temporary.cleanup()
        return {"packages": len(census), "coveredFields": field_count,
                "censusDigest": control_digest(census)}

    def _check_ac06(self):
        records = load_records(self.root, self.byte_source)
        current = {}
        for package_id, package in sorted(self.packages.items()):
            current[package_id] = resolve_current(
                self.root, self.registry, package, self.byte_source, records)
        return {"currentPackages": len(current), "recordCount": len(records),
                "currentApprovalDigest": control_digest(current)}

    def _check_ac07(self):
        forbidden = self.registry["taxonomy"]["forbiddenPaths"]
        snapshot_paths = self._snapshot_paths()
        if snapshot_paths is not None:
            for path in forbidden:
                if any(item == path or item.startswith(path.rstrip("/") + "/")
                       for item in snapshot_paths):
                    raise StructuredSourceError(
                        "obsolete controlled path remains: %s" % path)
        else:
            for path in forbidden:
                if os.path.lexists(os.path.join(self.root, *path.split("/"))):
                    raise StructuredSourceError("obsolete controlled path remains: %s" % path)
        for path, expected in render_all(self.registry).items():
            if self.reader.read(path) != expected:
                raise StructuredSourceError("generated router is stale: %s" % path)
        registered_paths = self._controlled_paths()
        for document in self.registry["documents"]:
            artifact = self.artifacts[document["documentId"]]
            actual = set()
            for link in artifact.root.findall(".//" + C + "link"):
                target = link.get("target")
                parsed = urlsplit(target)
                if parsed.scheme:
                    if parsed.scheme not in {"https", "http", "mailto"}:
                        raise StructuredSourceError("projection link scheme is not registered")
                elif parsed.path:
                    path = safe_path(unquote(parsed.path), "XML link path")
                    actual.add(path)
                    if path not in registered_paths or not self.reader.exists(path):
                        raise StructuredSourceError("registered local link is unresolved: %s" % path)
                    if parsed.fragment:
                        fragment = unquote(parsed.fragment)
                        if path.endswith(".md"):
                            unused_links, anchors = self._markdown_analysis(path)
                            if fragment not in anchors:
                                raise StructuredSourceError(
                                    "registered local link fragment is unresolved: %s#%s" %
                                    (path, fragment))
                        elif not (path.lower().endswith(".pdf") and
                                  re.fullmatch(r"page=[1-9][0-9]*", fragment)):
                            raise StructuredSourceError(
                                "registered local link fragment target is unsupported")
                elif parsed.fragment:
                    path = self.file_path(document["markdownFile"])
                    unused_links, anchors = self._markdown_analysis(path)
                    if unquote(parsed.fragment) not in anchors:
                        raise StructuredSourceError(
                            "registered same-document fragment is unresolved")
            if sorted(actual) != document["referenceAllowlist"]:
                raise StructuredSourceError("document reference allowlist is stale")
        for entry in self.registry["files"]:
            path = entry["path"]
            if not path.endswith(".md"):
                continue
            links, unused_anchors = self._markdown_analysis(path)
            for target in links:
                self._resolve_markdown_target(path, target)
        prior_ids = set(self.registry["taxonomy"]["priorArtIds"])
        actual_prior = {item["documentId"].rsplit("-", 1)[1].upper()
                        for item in self.registry["documents"]
                        if item["documentId"].startswith("us-prior-art-")}
        if actual_prior != prior_ids:
            raise StructuredSourceError("prior-art package identity census is not exact")
        for evidence_id in prior_ids:
            prefix = "US/prior-art/%s/" % evidence_id
            paths = [item["path"] for item in self.registry["files"]
                     if item["path"].startswith(prefix)]
            roles = Counter(item["role"] for item in self.registry["files"]
                            if item["path"].startswith(prefix))
            for role in ("source-xml", "markdown-view", "coverage",
                         "stored-evidence", "source-manifest"):
                if roles[role] != 1:
                    raise StructuredSourceError("prior-art package evidence closure is not exact")
            if any("/markdown/" in path or "/searchable/" in path for path in paths):
                raise StructuredSourceError("prior-art package retains an obsolete authoring path")
        return {"routers": len(self.registry["routers"]),
                "priorArtPackages": len(prior_ids)}

    def _check_ac08(self):
        digest = verify_export(self.root, self.registry, "structured-handoff",
                               self.byte_source)
        return {"consumer": "structured-handoff", "exportDigest": digest}

    def _check_ac09(self):
        environment = verify_environment(self.root, self.byte_source)
        policy = parse_json(self.reader.read("structured_source/policy/commands.json"))
        validate_command_policy(policy)
        commands = policy["commands"]
        return {"environment": environment, "commands": len(commands)}

    def _scan_migration_residue(self):
        forbidden_names = {
            "migration_archive.py", "convert_content.py", "convert_relations.py",
            "assemble_proposed.py", "compare_migration.py",
        }
        problems = []
        snapshot_paths = self._snapshot_paths()
        if snapshot_paths is None:
            repository_paths = []
            for directory, dirnames, filenames in os.walk(self.root):
                dirnames[:] = [name for name in dirnames if name not in _EXCLUDED_DIRS]
                relative_directory = os.path.relpath(
                    directory, self.root).replace(os.sep, "/")
                repository_paths.extend(
                    name if relative_directory == "." else
                    relative_directory + "/" + name
                    for name in filenames)
        else:
            repository_paths = snapshot_paths
        for path in repository_paths:
            name = posixpath.basename(path)
            if name in forbidden_names or path.endswith(
                    ("_migration-record.json", "_migration-report.json")):
                problems.append(path)
            if name.endswith("_DRAFT.md") and path.startswith(
                    "AA11393US-structured-source-markdown-migration"):
                problems.append(path)
        for path in ("/private/tmp/aa11393-ssp-migration-archive.locator.json",
                     "/private/tmp/aa11393-ssp-migration-archive.lease"):
            if os.path.lexists(path):
                problems.append(path)
        temporary_prefixes = (
            "aa11393-ssp-baseline-", "aa11393-ssp-content-",
            "aa11393-ssp-migration-", "aa11393-ssp-proposed-",
            "aa11393-ssp-relations-", "aa11393-ssp-review-",
        )
        try:
            for name in os.listdir("/private/tmp"):
                if name.startswith(temporary_prefixes):
                    problems.append("/private/tmp/" + name)
        except OSError as exc:
            raise StructuredSourceError(
                "migration temporary namespace cannot be inspected") from exc
        return sorted(set(problems))

    def _check_ac10(self):
        residues = self._scan_migration_residue()
        if residues:
            raise StructuredSourceError("migration residue remains: %s" % residues)
        operative = {
            "AA11393US-structured-source-markdown_technical-description.md",
            "AA11393US-structured-source-markdown_acceptance-criteria.md",
            "AA11393US-structured-source-markdown_implementation-register.md",
        }
        if not all(self.reader.exists(path) for path in operative):
            raise StructuredSourceError("operative structured-source contract pair is absent")
        acceptance_path = "AA11393US-structured-source-markdown_acceptance-criteria.md"
        acceptance_text = self.reader.read(acceptance_path).decode("utf-8")
        from .acceptance import render_table
        marker_start = "<!-- SSM-AC-TABLE:START -->\n"
        marker_end = "<!-- SSM-AC-TABLE:END -->"
        if marker_start not in acceptance_text or marker_end not in acceptance_text:
            raise StructuredSourceError("operative acceptance table markers are absent")
        region = acceptance_text.split(marker_start, 1)[1].split(marker_end, 1)[0]
        if region != render_table(self.acceptance):
            raise StructuredSourceError("operative acceptance table is stale")
        prohibited = ("SSM-MIG-01", "PROPOSED ARCHITECTURE",
                      "PROPOSED DEFINITION OF DONE")
        for path in operative:
            text = self.reader.read(path).decode("utf-8")
            if any(token in text for token in prohibited):
                raise StructuredSourceError("operative contract retains migration/future narrative")
        return {"criteria": len(self.acceptance["criteria"]),
                "callbackCount": len(CALLBACKS), "migrationResidue": 0}

    def run_check(self, criterion):
        if criterion in self._results:
            return self._results[criterion]
        method = getattr(self, "_check_" + criterion.lower().replace("-", ""), None)
        if method is None:
            method = {
                "SSM-AC-01": self._check_ac01, "SSM-AC-02": self._check_ac02,
                "SSM-AC-03": self._check_ac03, "SSM-AC-04": self._check_ac04,
                "SSM-AC-05": self._check_ac05, "SSM-AC-06": self._check_ac06,
                "SSM-AC-07": self._check_ac07, "SSM-AC-08": self._check_ac08,
                "SSM-AC-09": self._check_ac09, "SSM-AC-10": self._check_ac10,
            }[criterion]
        result = method()
        self._results[criterion] = result
        return result


def render_census(root):
    context = VerificationContext(root, fresh_process=False)
    return {"renderCensusVersion": "1", "packages": context.render_census()}


def implementation_census(root, reader, registry):
    paths = sorted(item["path"] for item in registry["files"]
                   if item["role"] in {
                       "acceptance-registry", "approval-authority",
                       "approval-inventory", "consumer-control",
                       "content-registry", "contract", "environment-control",
                       "implementation-source", "outer-gate-control",
                       "outer-gate-test", "policy", "profile",
                       "repository-control-reference", "schema", "test",
                   })
    return [{"path": path, "rawDigest": raw_digest(reader.read(path))}
            for path in paths]


def run_callback_receipt(root, byte_source=None, repository_snapshot=None,
                         fresh_process=True):
    context = VerificationContext(root, byte_source, repository_snapshot,
                                  fresh_process=fresh_process)
    results = []
    for criterion in context.acceptance["criteria"]:
        for callback in criterion["callbacks"]:
            evidence = CALLBACKS[callback](context)
            results.append({"callback": callback, "criterion": criterion["code"],
                            "status": "satisfied", "evidenceDigest": control_digest(evidence)})
    census = implementation_census(root, context.reader, context.registry)
    environment = verify_environment(root, byte_source)
    receipt = {
        "receiptVersion": "1", "namespace": "ssp",
        "repositorySnapshot": (getattr(repository_snapshot, "digest", None)
                               if repository_snapshot is not None else None),
        "acceptanceRegistryDigest": raw_digest(
            context.reader.read("structured_source/registry/acceptance.json")),
        "contentRegistryDigest": raw_digest(canonical_json(context.registry)),
        "implementationCensus": census,
        "implementationCensusDigest": control_digest(census),
        "environment": environment,
        "results": results,
    }
    if len(results) != len(CALLBACKS) or \
            {item["callback"] for item in results} != set(CALLBACKS):
        raise StructuredSourceError("structured-source callback result census is incomplete")
    return receipt


def environment_path_census(environment):
    environment = os.path.abspath(environment)
    if not os.path.isdir(environment) or os.path.islink(environment):
        raise StructuredSourceError("environment census root is absent or a symlink")
    entries = []
    for directory, dirnames, filenames in os.walk(environment, followlinks=False):
        dirnames[:] = sorted(name for name in dirnames if name != "__pycache__")
        for name in sorted(filenames):
            path = os.path.join(directory, name)
            if os.path.islink(path):
                target = os.readlink(path)
                entries.append({"path": os.path.relpath(path, environment).replace(os.sep, "/"),
                                "symlink": target})
            elif os.path.isfile(path) and "__pycache__" not in path.split(os.sep):
                with open(path, "rb") as handle:
                    data = handle.read()
                entries.append({"path": os.path.relpath(path, environment).replace(os.sep, "/"),
                                "rawDigest": raw_digest(data), "size": len(data)})
            else:
                raise StructuredSourceError("environment contains a non-regular entry")
    return control_digest(entries)


def environment_tree_census(root):
    environment = os.path.join(root, ".venv")
    if os.path.islink(environment):
        raise StructuredSourceError("project-local environment is a symlink")
    return environment_path_census(environment)
