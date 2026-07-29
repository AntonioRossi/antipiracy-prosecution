"""Lazy package verification and one-pass recurring SSM acceptance.

Authored Markdown conversion is deliberately behind one narrow adapter call.
``structured_source.markdown.convert_authored_markdown`` accepts the authority
bytes, authority path, and package identity.  Its current result carries the
generated XML, semantic back-render, and exact fragment identities/digests.
Verification consumes that evidence in memory and never serializes or publishes
a coverage artifact.
"""

from __future__ import annotations

from collections.abc import Mapping
from collections import Counter
import ast
from dataclasses import dataclass
import importlib
import os
import re
from types import MappingProxyType
from xml.etree import ElementTree as ET

from . import CONTENT_NAMESPACE, RELATIONS_NAMESPACE
from .acceptance import CONTRACTS, CRITERIA, load_registries, render_table
from .artifact_policy import (ArtifactClass, artifact_policy,
                              classify_artifacts)
from .atomic import publish_set
from .canonical import raw_digest
from .control import canonical_json, parse_json
from .errors import StructuredSourceError
from .registry import (REGISTRY_PATH, consumer_edge, files_by_id, load_registry,
                       packages_by_id, safe_path)

C = "{%s}" % CONTENT_NAMESPACE
R = "{%s}" % RELATIONS_NAMESPACE
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_RETIRED_PATH_PATTERNS = (
    re.compile(r"(?:^|/)structured_source/approvals(?:/|$)"),
    re.compile(r"(?:^|/)structured_source/exports(?:/|$)"),
    re.compile(r"(?:^|/)structured_source/exporter\.py\Z"),
    re.compile(r"(?:^|/)structured_source/(?:compat|compatibility|migrate|migration)"
               r"(?:\.py|/)"),
    re.compile(r"(?:^|/)structured_source/tests/test_"
               r"(?:approvals|compatibility|exporter|migration|projection)\.py\Z"),
    re.compile(r"\.(?:attestation|audit|coverage|lineage|receipt|verification)"
               r"\.json\Z"),
    re.compile(r"(?:^|/)structured_source/(?:attestations|audit-exports|lineage|"
               r"receipts|verification-records)(?:/|$)"),
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


@dataclass(frozen=True, slots=True)
class ValidatedCorpus:
    """One complete snapshot-bound structured-source validation result.

    The object exposes only frozen consumer handoffs and retained parser
    controls.  The mutable verification context that constructed them never
    crosses this boundary.
    """

    snapshot_digest: str
    domains: tuple
    result_ids: tuple
    package_summaries: tuple
    consumer_handoffs: MappingProxyType
    parser_controls: object
    technical_validation_result_version: str = "1"

    def public_result(self):
        """Return the ephemeral plain-data result for the aggregate caller."""
        return {
            "technicalValidationResultVersion":
                self.technical_validation_result_version,
            "snapshotDigest": self.snapshot_digest,
            "status": "passed",
            "domains": [dict(item) for item in self.domains],
            "results": [
                {"id": identifier, "status": "passed"}
                for identifier in self.result_ids
            ],
        }


@dataclass(frozen=True, slots=True)
class _RelationDerivation:
    """Fresh relation-only state retained through one output lifetime."""

    artifact: object
    projection: object
    coverage: object
    endpoint_views: MappingProxyType
    endpoint_package_ids: tuple
_LIVE_IMPLEMENTATION = frozenset({
    "AGENTS.md",
    "GLOSSARY.md",
    "README.md",
    "STRUCTURED-CONTENT-AUTHORITY-MANIFEST.md",
    "validate.sh",
    "contracts/README.md",
    "contracts/10-source-surfaces/authored-markdown/acceptance-criteria.md",
    "contracts/10-source-surfaces/authored-markdown/technical-description.md",
    "contracts/10-source-surfaces/pdf-transcription/acceptance-criteria.md",
    "contracts/10-source-surfaces/pdf-transcription/technical-description.md",
    "contracts/20-semantic-relations/authored-relations/acceptance-criteria.md",
    "contracts/20-semantic-relations/authored-relations/technical-description.md",
    "contracts/20-semantic-relations/claim-prior-art-passage-map/acceptance-criteria_DRAFT.md",
    "contracts/20-semantic-relations/claim-prior-art-passage-map/technical-description_DRAFT.md",
    "contracts/30-product-generation/claims-navigator/acceptance-criteria_DRAFT.md",
    "contracts/30-product-generation/claims-navigator/technical-description_DRAFT.md",
    "contracts/30-product-generation/claims-prior-art-navigator/acceptance-criteria_DRAFT.md",
    "contracts/30-product-generation/claims-prior-art-navigator/technical-description_DRAFT.md",
    "contracts/30-product-generation/navigator-guide/acceptance-criteria_DRAFT.md",
    "contracts/30-product-generation/navigator-guide/technical-description_DRAFT.md",
    "contracts/30-product-generation/navigator-presentation/acceptance-criteria_DRAFT.md",
    "contracts/30-product-generation/navigator-presentation/technical-description_DRAFT.md",
    "navigator/RUNBOOK-content-sync-and-regeneration.md",
    "navigator/__init__.py",
    "navigator/__main__.py",
    "navigator/build.py",
    "navigator/lib/__init__.py",
    "navigator/lib/acceptance.py",
    "navigator/lib/bundlezip.py",
    "navigator/lib/browserqa.py",
    "navigator/lib/canon.py",
    "navigator/lib/claims.py",
    "navigator/lib/currentstate.py",
    "navigator/lib/depgraph.py",
    "navigator/lib/gateway.py",
    "navigator/lib/model.py",
    "navigator/lib/projections.py",
    "navigator/lib/priorart.py",
    "navigator/lib/presentationqa.py",
    "navigator/lib/registry.py",
    "navigator/lib/release.py",
    "navigator/lib/render.py",
    "navigator/lib/schema_validate.py",
    "navigator/lib/snapshot.py",
    "navigator/lib/unicode15_1.py",
    "navigator/lib/validate.py",
    "navigator/schema/acceptance.json",
    "navigator/schema/guide-acceptance.json",
    "navigator/schema/prior-art-map-acceptance.json",
    "navigator/schema/prior-art-acceptance.json",
    "navigator/schema/presentation-acceptance.json",
    "navigator/schema/edition.schema.json",
    "navigator/schema/navigator-relations.xsd",
    "navigator/schema/wording.xsd",
    "navigator/policy/browser.json",
    "navigator/tests/test_canon.py",
    "navigator/tests/test_current_pipeline.py",
    "navigator/tests/test_guide.py",
    "navigator/tests/test_prior_art.py",
    "navigator/tests/test_presentation.py",
    "navigator/tests/__init__.py",
    "navigator/tests/test_render_current.py",
    "navigator/tests/test_xml_model.py",
    "navigator/tests/vectors/canon_vectors.json",
    "structured_source/__init__.py",
    "structured_source/__main__.py",
    "structured_source/acceptance.py",
    "structured_source/artifact_policy.py",
    "structured_source/atomic.py",
    "structured_source/canonical.py",
    "structured_source/control.py",
    "structured_source/environment.py",
    "structured_source/errors.py",
    "structured_source/grammar.py",
    "structured_source/markdown.py",
    "structured_source/parser.py",
    "structured_source/pdf_transcription.py",
    "structured_source/policy/environment.json",
    "structured_source/policy/parser.json",
    "structured_source/profiles.py",
    "structured_source/profiles/gfm-v1.json",
    "structured_source/profiles/xml-v3.json",
    "structured_source/registry.py",
    "structured_source/registry/acceptance-authored-markdown.json",
    "structured_source/registry/acceptance-authored-relations.json",
    "structured_source/registry/acceptance-pdf-transcription.json",
    "structured_source/registry/content.json",
    "structured_source/relation_projection.py",
    "structured_source/render.py",
    "structured_source/routers.py",
    "structured_source/schemas/content.xsd",
    "structured_source/schemas/authored.xsd",
    "structured_source/schemas/relations.xsd",
    "structured_source/schemas/xml.xsd",
    "structured_source/tests/test_acceptance.py",
    "structured_source/tests/test_atomic.py",
    "structured_source/tests/test_conversion.py",
    "structured_source/tests/__init__.py",
    "structured_source/tests/test_pdf_transcription.py",
    "structured_source/tests/test_registry.py",
    "structured_source/tests/test_xml_contract.py",
    "structured_source/verify.py",
})
_PDF_NAMED_PATHS = frozenset({
    "contracts/10-source-surfaces/pdf-transcription/acceptance-criteria.md",
    "contracts/10-source-surfaces/pdf-transcription/technical-description.md",
    "structured_source/pdf_transcription.py",
    "structured_source/registry/acceptance-pdf-transcription.json",
    "structured_source/tests/test_pdf_transcription.py",
})
_AUTHORED_MARKDOWN_NAMED_PATHS = frozenset({
    "contracts/10-source-surfaces/authored-markdown/acceptance-criteria.md",
    "contracts/10-source-surfaces/authored-markdown/technical-description.md",
    "structured_source/markdown.py",
    "structured_source/registry/acceptance-authored-markdown.json",
    "structured_source/schemas/authored.xsd",
})
_AUTHORED_RELATIONS_NAMED_PATHS = frozenset({
    "contracts/20-semantic-relations/authored-relations/acceptance-criteria.md",
    "contracts/20-semantic-relations/authored-relations/technical-description.md",
    "structured_source/registry/acceptance-authored-relations.json",
    "structured_source/relation_projection.py",
    "structured_source/schemas/relations.xsd",
})
_STRUCTURED_SOURCE_LIVE_PATHS = frozenset({
    "structured_source/PACKAGES.md",
    "structured_source/__init__.py",
    "structured_source/__main__.py",
    "structured_source/acceptance.py",
    "structured_source/artifact_policy.py",
    "structured_source/atomic.py",
    "structured_source/canonical.py",
    "structured_source/control.py",
    "structured_source/environment.py",
    "structured_source/errors.py",
    "structured_source/grammar.py",
    "structured_source/markdown.py",
    "structured_source/parser.py",
    "structured_source/pdf_transcription.py",
    "structured_source/policy/environment.json",
    "structured_source/policy/parser.json",
    "structured_source/profiles.py",
    "structured_source/profiles/gfm-v1.json",
    "structured_source/profiles/xml-v3.json",
    "structured_source/registry.py",
    "structured_source/registry/acceptance-authored-markdown.json",
    "structured_source/registry/acceptance-authored-relations.json",
    "structured_source/registry/acceptance-pdf-transcription.json",
    "structured_source/registry/content.json",
    "structured_source/relation_projection.py",
    "structured_source/render.py",
    "structured_source/routers.py",
    "structured_source/schemas/authored.xsd",
    "structured_source/schemas/content.xsd",
    "structured_source/schemas/relations.xsd",
    "structured_source/schemas/xml.xsd",
    "structured_source/tests/__init__.py",
    "structured_source/tests/test_acceptance.py",
    "structured_source/tests/test_atomic.py",
    "structured_source/tests/test_conversion.py",
    "structured_source/tests/test_pdf_transcription.py",
    "structured_source/tests/test_registry.py",
    "structured_source/tests/test_xml_contract.py",
    "structured_source/verify.py",
})
_RETIRED_IDENTIFIERS = frozenset({
    "semantic" + "Digest",
    "semantic" + "_digest",
})
_RETIRED_VALUE_PREFIXES = (
    "sha256/" + "xc1:",
    "ssp-" + "xd1",
)


def _parse_artifact(data, kind, *, controls):
    # Keep registry/acceptance controls usable before the locked XML runtime is
    # imported; conversion paths still fail immediately if it is unavailable.
    from .parser import parse_artifact
    return parse_artifact(data, kind, controls=controls)


def _render_content(*args, **kwargs):
    from .render import render_content
    return render_content(*args, **kwargs)


def _render_relations(*args, **kwargs):
    from .render import render_relations
    return render_relations(*args, **kwargs)


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
        self._snapshot_bytes = {}

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
        self._snapshot_bytes.setdefault(path, data)
        return data

    def validated(self, path):
        """Return already-read snapshot bytes without reopening any path."""
        path = safe_path(path)
        if path not in self._snapshot_bytes:
            raise StructuredSourceError(
                "controlled bytes were not validated before handoff: %s" % path)
        return self._snapshot_bytes[path]

    def discard(self, path):
        """Forget an owned output after atomic replacement and before readback."""
        path = safe_path(path)
        self.read_log.pop(path, None)
        self._snapshot_bytes.pop(path, None)

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


def _freeze_result(value):
    """Freeze cached validation data without changing its JSON value."""
    if isinstance(value, dict):
        return MappingProxyType({
            key: _freeze_result(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze_result(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze_result(item) for item in value)
    return value


def _copy_result(value):
    """Detach public result data from the context's validated cache."""
    if isinstance(value, Mapping):
        return {key: _copy_result(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return tuple(_copy_result(item) for item in value)
    return value


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
        self._derived_package_state = {}
        self._validated_package_state = {}
        self._checking = set()
        self._global_result = None
        self._global_passes = 0
        self._parser_controls = None
        self._snapshot_identity_validated = False
        self._consumer_handoffs = {}
        self._authored_conversion_objects = []
        self._relation_artifact_objects = []
        self._relation_endpoint_view_objects = []
        self._relation_projection_objects = []
        self._relation_coverage_objects = []
        self._relation_derivation_objects = []
        self._relation_derived_state_objects = []
        self._relation_validated_state_objects = []
        self._relation_package_result_objects = []
        self._relation_handoff_objects = []

    @staticmethod
    def _retain_fresh_relation_object(value, retained, label):
        if any(value is previous for previous in retained):
            raise StructuredSourceError(
                "%s crossed a generated-view validation lifetime" % label)
        retained.append(value)
        return value

    def _controls(self):
        if self._parser_controls is None:
            from .parser import load_parser_controls
            self._parser_controls = load_parser_controls(self.reader.read)
        return self._parser_controls

    @property
    def parser_controls(self):
        """Return the retained controls used by this validation context."""
        return self._controls()

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
            self.reader.read(self.file_path(package["xmlFile"])), kind,
            controls=self._controls())
        if kind == "relation-set":
            self._retain_fresh_relation_object(
                artifact, self._relation_artifact_objects,
                "relation parsed artifact")
            identity = artifact._validated_root().find(R + "identity")
            actual = identity.get("relationSetId") if identity is not None else None
        else:
            identity = artifact._validated_root().find(C + "documentIdentity")
            actual = identity.get("documentId") if identity is not None else None
        if actual != package_id:
            raise StructuredSourceError(
                "package and XML identities do not match")
        self._artifacts[package_id] = artifact
        if kind in {"content-document", "authored-document"}:
            markdown_path = self.file_path(package["markdownFile"])
            for node in artifact._validated_root().iter():
                identifier = node.get(XML_ID)
                if identifier:
                    key = (package_id, identifier)
                    if key in self._fragments:
                        raise StructuredSourceError("fragment identity is duplicated")
                    self._fragments[key] = MappingProxyType({
                        "digest": artifact.fragment_digests[identifier],
                        "excerpt": _plain_text(node),
                        "markdownPath": markdown_path,
                    })
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
                not stored_bytes.startswith(b"%PDF-") or \
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
            node.get("assetId") for node in artifact._validated_root().iter()
            if node.tag in {C + "image", C + "figure"}}
        if set(assets) != used_assets:
            raise StructuredSourceError(
                "PDF XML/manifest asset census is not exact")
        return _render_content(
            artifact, self.file_path(package["markdownFile"]), assets,
            projection_profile=self._controls().projection_profile)

    def _resolve_pdf_dependencies(self, package_id, artifact, manifest):
        from .pdf_transcription import DependencyBinding
        asset_digests = {
            entry["assetId"]: entry["rawDigest"] for entry in manifest["assets"]}
        resolved = []
        dependencies = artifact._validated_root().find(C + "dependencies")
        for entry in dependencies.findall(C + "dependency"):
            kind = entry.get("kind")
            subject_id = entry.get("subjectId")
            item_id = entry.get("itemId")
            declared_digest = entry.get("digest")
            if kind == "asset":
                actual_digest = (asset_digests.get(subject_id)
                                 if item_id is None else None)
            elif kind == "document":
                dependency_package = self.packages.get(subject_id)
                if dependency_package is None or \
                        dependency_package["authorityScheme"] == \
                        "authored-relations-v1":
                    actual_digest = "invalid"
                else:
                    self.check(subject_id)
                    actual_digest = (self._artifact(
                        subject_id).fragment_digests.get(item_id)
                                     if item_id is not None else None)
            elif kind == "relation-set":
                dependency_package = self.packages.get(subject_id)
                if dependency_package is None or \
                        dependency_package["authorityScheme"] != \
                        "authored-relations-v1" or item_id is not None or \
                        declared_digest is not None:
                    actual_digest = "invalid"
                else:
                    self.check(subject_id)
                    actual_digest = None
            else:
                actual_digest = None
            if actual_digest != declared_digest:
                raise StructuredSourceError(
                    "PDF registered dependency digest is stale: %s" % package_id)
            resolved.append(DependencyBinding(
                kind=kind, subject_id=subject_id, item_id=item_id,
                digest=declared_digest))
        return tuple(resolved)

    def _render_relation(self, package, artifact):
        views = {}
        assertions = set()
        relation_ids = []
        endpoint_package_ids = set()
        root = artifact._validated_root()
        identity = root.find(R + "identity")
        if identity is None or (
                identity.get("relationSetId"), identity.get("owner"),
                identity.get("scope"), identity.get("status")) != (
                    package["packageId"], package["owner"],
                    package["scope"], package["status"]):
            raise StructuredSourceError(
                "relation package identity and ownership do not close exactly")
        try:
            relation_profile = self._controls().xml_profiles[
                "relationSets"][artifact.profile]
            role_targets = relation_profile["endpointRoleTargets"]
        except KeyError as exc:
            raise StructuredSourceError(
                "relation endpoint-role profile does not resolve") from exc
        for relation in root.findall(R + "relation"):
            relation_ids.append(relation.get("relationId"))
            fields = tuple((entry.get("name"), entry.text or "")
                           for entry in relation.findall(R + "assertionField"))
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
            for role, document_id, fragment_id, digest in endpoints:
                endpoint_package = self.packages.get(document_id)
                if endpoint_package is None or \
                        endpoint_package["authorityScheme"] == \
                        "authored-relations-v1":
                    raise StructuredSourceError(
                        "relation endpoint document is not a content package")
                if endpoint_package["authorityScheme"] not in role_targets[role]:
                    raise StructuredSourceError(
                        "relation endpoint role and target authority are swapped")
                self.check(document_id)
                self._artifact(document_id)
                endpoint_package_ids.add(document_id)
                fragment = self._fragments.get((document_id, fragment_id))
                if fragment is None or fragment["digest"] != digest:
                    raise StructuredSourceError(
                        "relation endpoint does not resolve exactly")
                key = (document_id, fragment_id, digest)
                if key not in views:
                    view = MappingProxyType({
                        "excerpt": fragment["excerpt"],
                        "markdownPath": fragment["markdownPath"],
                    })
                    self._retain_fresh_relation_object(
                        view, self._relation_endpoint_view_objects,
                        "resolved relation endpoint view")
                    views[key] = view
        if len(relation_ids) != len(set(relation_ids)):
            raise StructuredSourceError("relation identity is duplicated")
        endpoint_views = MappingProxyType(views)
        self._retain_fresh_relation_object(
            endpoint_views, self._relation_endpoint_view_objects,
            "resolved relation endpoint-view mapping")
        profile = self._controls().projection_profile
        projection = _render_relations(
            artifact, self.file_path(package["markdownFile"]), endpoint_views,
            projection_profile=profile)
        from .render import Projection
        if type(projection) is not Projection:
            raise StructuredSourceError(
                "relation renderer did not construct an immutable projection")
        self._retain_fresh_relation_object(
            projection, self._relation_projection_objects,
            "relation projection")
        from .relation_projection import (RelationCoverage,
                                          validate_relation_projection)
        coverage = validate_relation_projection(
            artifact, projection.markdown,
            self.file_path(package["markdownFile"]), endpoint_views,
            projection_profile=profile)
        if type(coverage) is not RelationCoverage:
            raise StructuredSourceError(
                "relation coverage did not construct an immutable census")
        self._retain_fresh_relation_object(
            coverage, self._relation_coverage_objects,
            "relation coverage")
        derivation = _RelationDerivation(
            artifact=artifact,
            projection=projection,
            coverage=coverage,
            endpoint_views=endpoint_views,
            endpoint_package_ids=tuple(sorted(endpoint_package_ids)),
        )
        self._retain_fresh_relation_object(
            derivation, self._relation_derivation_objects,
            "relation derivation")
        return derivation

    def _derive(self, package_id):
        package = self.packages[package_id]
        scheme = package["authorityScheme"]
        xml_path = self.file_path(package["xmlFile"])
        markdown_path = self.file_path(package["markdownFile"])
        if scheme == "authored-markdown-v1":
            markdown = self.reader.read(markdown_path)
            converter = self._markdown_converter()
            if self.markdown_adapter is None:
                conversion = converter(
                    markdown, markdown_path, package_id,
                    parser_controls=self._controls())
            else:
                conversion = converter(markdown, markdown_path, package_id)
            if any(conversion is previous
                   for previous in self._authored_conversion_objects):
                raise StructuredSourceError(
                    "authored Markdown conversion object crossed a validation lifetime")
            self._authored_conversion_objects.append(conversion)
            xml = _conversion_value(conversion, "xml")
            item_ids = _conversion_value(conversion, "item_ids")
            generated_markdown = _conversion_value(conversion, "markdown")
            source_digest = _conversion_value(
                conversion, "source_raw_digest")
            generated_markdown_digest = _conversion_value(
                conversion, "generated_markdown_raw_digest")
            conversion_fragments = _conversion_value(
                conversion, "fragment_digests")
            if not isinstance(xml, bytes):
                raise StructuredSourceError(
                    "authored Markdown conversion is incomplete")
            from .markdown import validate_authored_coverage
            coverage = validate_authored_coverage(
                markdown, markdown_path, package_id, xml,
                parser_controls=self._controls())
            if not isinstance(item_ids, tuple) or \
                    item_ids != coverage.item_ids or \
                    not isinstance(generated_markdown, bytes) or \
                    generated_markdown != coverage.markdown or \
                    source_digest != raw_digest(markdown) or \
                    generated_markdown_digest != raw_digest(
                        coverage.markdown) or \
                    not isinstance(conversion_fragments, Mapping) or \
                    dict(conversion_fragments) != dict(
                        coverage.fragment_digests):
                raise StructuredSourceError(
                    "authored Markdown converter report differs from independent coverage")
            self._derived_package_state[package_id] = {
                "representations": {"markdown": markdown, "xml": xml},
                "surface": None,
            }
            return xml_path, xml, {
                "scheme": scheme, "coveredItems": len(coverage.items),
                "backRender": "equal",
            }

        artifact = self._artifact(package_id)
        if scheme == "pdf-evidence-transcription-v1":
            from .pdf_transcription import build_surface
            manifest = self._manifest(package)
            projection = self._render_pdf(package, artifact, manifest)
            resolved_dependencies = self._resolve_pdf_dependencies(
                package_id, artifact, manifest)
            surface = build_surface(
                artifact, manifest, projection, package_id=package_id,
                xml_path=xml_path,
                manifest_path=self.file_path(package["sourceManifestFile"]),
                manifest_raw_digest=raw_digest(self.reader.validated(
                    self.file_path(package["sourceManifestFile"]))),
                markdown_path=markdown_path,
                resolved_dependencies=resolved_dependencies)
            self._derived_package_state[package_id] = {
                "representations": {
                    "markdown": projection.markdown,
                    "xml": artifact.raw_bytes,
                },
                "surface": surface,
            }
            return markdown_path, projection.markdown, {
                "scheme": scheme, "coveredItems": len(surface.items),
                "coveredFields": surface.coverage_field_count,
                "storedSources": 1,
            }

        derivation = self._render_relation(package, artifact)
        coverage = derivation.coverage
        state = MappingProxyType({
            "representations": MappingProxyType({
                "markdown": derivation.projection.markdown,
                "xml": artifact.raw_bytes,
            }),
            "surface": None,
            "validationPackageIds": derivation.endpoint_package_ids,
            "relationArtifact": artifact,
            "relationProjection": derivation.projection,
            "relationCoverage": coverage,
            "endpointViews": derivation.endpoint_views,
        })
        self._retain_fresh_relation_object(
            state, self._relation_derived_state_objects,
            "relation derived package state")
        self._derived_package_state[package_id] = state
        return markdown_path, derivation.projection.markdown, {
            "scheme": scheme,
            "coveredItems": coverage.assertion_count +
                coverage.assertion_field_count,
            "assertions": coverage.assertion_count,
            "assertionFields": coverage.assertion_field_count,
            "endpoints": coverage.endpoint_count,
        }

    def check(self, package_id):
        if package_id not in self.packages:
            raise StructuredSourceError("subject identity does not resolve")
        cached = self._package_results.get(package_id)
        if cached is not None:
            return _copy_result(cached)
        if package_id in self._checking:
            raise StructuredSourceError("package dependency graph contains a cycle")
        self._checking.add(package_id)
        try:
            output_path, generated, evidence = self._derive(package_id)
            current = self.reader.read(output_path)
            if current != generated:
                raise StructuredSourceError(
                    "generated representation is stale: %s" % package_id)
            state = self._derived_package_state.get(package_id)
            representations = (state.get("representations")
                               if isinstance(state, Mapping) else None)
            if not isinstance(state, Mapping) or \
                    not isinstance(representations, Mapping) or \
                    representations.get(
                        "markdown" if output_path == self.file_path(
                            self.packages[package_id]["markdownFile"]) else "xml") \
                    != current:
                raise StructuredSourceError(
                    "validated package representation state is incomplete")
            package = self.packages[package_id]
            owned_ids = [
                package["xmlFile"], package["markdownFile"],
                *package["storedSourceFiles"], *package["convenienceFiles"],
                *package["assetFiles"],
            ]
            if package["sourceManifestFile"] is not None:
                owned_ids.append(package["sourceManifestFile"])
            validation_paths = {self.file_path(file_id) for file_id in owned_ids}
            if self._parser_controls is not None:
                from .parser import PARSER_CONTROL_PATHS
                validation_paths.update(PARSER_CONTROL_PATHS)
            if REGISTRY_PATH in self.reader.read_log:
                validation_paths.add(REGISTRY_PATH)
            surface = state.get("surface")
            validation_package_ids = set(
                state.get("validationPackageIds", ()))
            if surface is not None:
                for dependency in surface.dependencies:
                    if dependency.kind in {"document", "relation-set"}:
                        validation_package_ids.add(dependency.subject_id)
            for dependency_id in validation_package_ids:
                dependency_state = self._validated_package_state.get(
                    dependency_id)
                if dependency_state is None:
                    raise StructuredSourceError(
                        "validated package dependency state is incomplete")
                validation_paths.update(dependency_state["validationPaths"])
            if not validation_paths.issubset(self.reader.read_log):
                raise StructuredSourceError(
                    "package validation read census is incomplete")
            validated_state = MappingProxyType({
                **dict(state),
                "representations": MappingProxyType(dict(representations)),
                "validationPaths": tuple(sorted(validation_paths)),
            })
            if package["authorityScheme"] == "authored-relations-v1":
                self._retain_fresh_relation_object(
                    validated_state, self._relation_validated_state_objects,
                    "relation validated package state")
            self._validated_package_state[package_id] = validated_state
            result = {
                "packageId": package_id,
                "authorityScheme": self.packages[package_id]["authorityScheme"],
                "status": "passed",
                "computedCoverage": evidence,
            }
            frozen_result = _freeze_result(result)
            if package["authorityScheme"] == "authored-relations-v1":
                self._retain_fresh_relation_object(
                    frozen_result, self._relation_package_result_objects,
                    "relation package result")
            self._package_results[package_id] = frozen_result
            return _copy_result(self._package_results[package_id])
        finally:
            self._checking.remove(package_id)

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
        replacement_result = None

        def discard_generated_state():
            self.reader.discard(output_path)
            self._package_results.clear()
            self._artifacts.clear()
            self._fragments.clear()
            self._derived_package_state.clear()
            self._validated_package_state.clear()
            self._consumer_handoffs.clear()
            self._global_result = None

        def validate_readback():
            nonlocal replacement_result
            discard_generated_state()
            replacement_result = self.check(package_id)
            state = self._validated_package_state.get(package_id)
            cached_result = self._package_results.get(package_id)
            if state is None or cached_result is None or \
                    replacement_result != _copy_result(cached_result):
                raise StructuredSourceError(
                    "replacement validation did not rebuild package state")
            if self.packages[package_id]["authorityScheme"] == \
                    "authored-relations-v1" and (
                        not any(state is item for item in
                                self._relation_validated_state_objects) or
                        not any(cached_result is item for item in
                                self._relation_package_result_objects)):
                raise StructuredSourceError(
                    "replacement relation state is not fresh")

        try:
            publish_set(
                self.root, {output_path: generated}, {output_path: current},
                guards, postcondition=validate_readback)
        except BaseException:
            # Publication has restored the exact prestate when its
            # postcondition fails.  Do not retain replacement-derived state.
            discard_generated_state()
            raise
        if replacement_result is None:
            raise StructuredSourceError(
                "generated representation replacement was not validated")
        return replacement_result

    def read_for_consumer(self, consumer_id, package_id):
        """Return one fully validated snapshot handoff, with no fallback."""
        from navigator.lib.snapshot import RepositorySnapshot

        edge = consumer_edge(self.registry, consumer_id, package_id)
        cached = self._consumer_handoffs.get((consumer_id, package_id))
        if cached is not None:
            return cached
        snapshot = self.repository_snapshot
        snapshot_entries = getattr(snapshot, "entries", None)
        snapshot_root = getattr(snapshot, "root", None)
        retained_bytes = getattr(snapshot, "retained_bytes", None)
        if self.reader.byte_source is None or not isinstance(
                snapshot, RepositorySnapshot) or not isinstance(
                getattr(snapshot, "digest", None), str) or \
                not snapshot.digest or not isinstance(snapshot_entries, tuple) or \
                not isinstance(snapshot_root, str) or \
                os.path.abspath(snapshot_root) != self.root:
            raise StructuredSourceError(
                "consumer handoff requires one identified immutable snapshot")
        if not self._snapshot_identity_validated:
            try:
                snapshot.validate_retained()
            except Exception as exc:
                raise StructuredSourceError(
                    "consumer snapshot retained-byte identity is invalid") from exc
            self._snapshot_identity_validated = True
        snapshot_paths = self._snapshot_paths()
        if snapshot_paths != set(retained_bytes) or any(
                not isinstance(data, bytes) for data in retained_bytes.values()):
            raise StructuredSourceError(
                "consumer snapshot retained-byte inventory is not exact")
        self.check(package_id)
        package = self.packages[package_id]
        representation = edge["inputRepresentation"]
        file_id = package["xmlFile" if representation == "xml" else "markdownFile"]
        path = self.file_path(file_id)
        state = self._validated_package_state.get(package_id)
        if state is None:
            raise StructuredSourceError(
                "consumer handoff has no validated package state")
        data = state["representations"][representation]
        dependencies = {}
        for dependency_file_id in edge["dependencies"]:
            dependency_path = self.file_path(dependency_file_id)
            dependencies[dependency_path] = (
                self.reader.validated(dependency_path)
                if dependency_path in self.reader.read_log
                else self.reader.read(dependency_path))
        surface = state["surface"]
        handed_surface = surface if representation == "xml" else None
        assets = ({asset.path: self.reader.validated(asset.path)
                   for asset in handed_surface.assets}
                  if handed_surface is not None else {})
        handoff_paths = set(state["validationPaths"]) | set(dependencies)
        for validated_path in handoff_paths:
            if validated_path not in snapshot_paths:
                raise StructuredSourceError(
                    "validated consumer byte is absent from the snapshot")
            try:
                retained = retained_bytes[validated_path]
            except KeyError as exc:
                raise StructuredSourceError(
                    "consumer snapshot byte is unavailable") from exc
            if not isinstance(retained, bytes) or \
                    retained != self.reader.validated(validated_path):
                raise StructuredSourceError(
                    "validated consumer byte differs from the snapshot")
        handoff = MappingProxyType({
            "consumerId": consumer_id,
            "packageId": package_id,
            "authorityScheme": package["authorityScheme"],
            "inputRepresentation": representation,
            "representationRole": self.files[file_id]["role"],
            "path": path,
            "bytes": data,
            "dependencies": MappingProxyType(dependencies),
            "assets": MappingProxyType(assets),
            "surface": handed_surface,
            "validationReads": tuple(
                (path, self.reader.read_log[path])
                for path in sorted(handoff_paths)),
        })
        if package["authorityScheme"] == "authored-relations-v1":
            self._retain_fresh_relation_object(
                handoff, self._relation_handoff_objects,
                "relation consumer handoff")
        self._consumer_handoffs[(consumer_id, package_id)] = handoff
        return handoff

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

    def _reject_retired_control_residue(self, repository_paths):
        """Reject retired mechanisms only through typed artifact policy."""
        index = classify_artifacts(set(repository_paths), self.registry)
        policy = artifact_policy()
        fence = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
        inline_code = re.compile(r"(?<!`)(`+)([^`\n]+)\1(?!`)")
        link_target = re.compile(r"\]\(\s*(?:<([^>]+)>|([^\s)]+))")

        def retired(value):
            return isinstance(value, str) and (
                value in _RETIRED_IDENTIFIERS or any(
                    prefix in value for prefix in _RETIRED_VALUE_PREFIXES))

        def inspect_json(value):
            if isinstance(value, dict):
                return any(retired(key) or inspect_json(item)
                           for key, item in value.items())
            if isinstance(value, list):
                return any(inspect_json(item) for item in value)
            return retired(value)

        def inspect_document(data, path):
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise StructuredSourceError(
                    "operative documentation is not UTF-8: %s" % path) from exc
            machine_values = []
            fence_character = None
            fence_length = 0
            for line in text.splitlines():
                match = fence.match(line)
                if fence_character is not None:
                    if match is not None and \
                            match.group(1)[0] == fence_character and \
                            len(match.group(1)) >= fence_length and \
                            not match.group(2).strip():
                        fence_character = None
                        fence_length = 0
                    else:
                        machine_values.append(line)
                    continue
                if match is not None:
                    marker = match.group(1)
                    if marker[0] == "`" and "`" in match.group(2):
                        machine_values.extend(
                            value for unused_marker, value
                            in inline_code.findall(line))
                        continue
                    fence_character = marker[0]
                    fence_length = len(marker)
                    machine_values.append(line[line.index(marker) + len(marker):])
                    continue
                machine_values.extend(
                    value for unused_marker, value in inline_code.findall(line))
                machine_values.extend(
                    first or second
                    for first, second in link_target.findall(line))
            return any(retired(value) for value in machine_values)

        for path, classification in index.items():
            mode = policy[classification]
            if mode not in {
                    "structural-code", "structural-control",
                    "structural-document"}:
                continue
            data = self.reader.read(path)
            found = False
            if mode == "structural-document":
                found = inspect_document(data, path)
            elif mode == "structural-code" and path.endswith(".py"):
                try:
                    tree = ast.parse(data.decode("utf-8"), filename=path)
                except (SyntaxError, UnicodeDecodeError) as exc:
                    raise StructuredSourceError(
                        "implementation source is not valid UTF-8 Python: %s" %
                        path) from exc
                for node in ast.walk(tree):
                    values = []
                    if isinstance(node, ast.Name):
                        values.append(node.id)
                    elif isinstance(node, ast.Attribute):
                        values.append(node.attr)
                    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                                           ast.ClassDef)):
                        values.append(node.name)
                    elif isinstance(node, ast.arg):
                        values.append(node.arg)
                    elif isinstance(node, ast.Constant) and isinstance(
                            node.value, str):
                        values.append(node.value)
                    if any(retired(value) for value in values):
                        found = True
                        break
            elif path.endswith(".json"):
                found = inspect_json(parse_json(data))
            elif path.endswith((".xml", ".xsd")):
                try:
                    root = ET.fromstring(data)
                except (ET.ParseError, UnicodeDecodeError) as exc:
                    raise StructuredSourceError(
                        "executable XML control is malformed: %s" % path) from exc
                found = any(
                    retired(node.tag.rsplit("}", 1)[-1]) or any(
                        retired(name.rsplit("}", 1)[-1]) or retired(value)
                        for name, value in node.attrib.items())
                    for node in root.iter())
            else:
                try:
                    text = data.decode("utf-8")
                except UnicodeDecodeError:
                    continue
                found = any(
                    identifier in text for identifier in _RETIRED_IDENTIFIERS) or \
                    any(prefix in text for prefix in _RETIRED_VALUE_PREFIXES)
            if found:
                raise StructuredSourceError(
                    "retired implementation/control residue remains in %s" % path)

    def _reject_alternate_structured_source_paths(self, repository_paths):
        actual = {
            path for path in repository_paths
            if path.startswith("structured_source/")}
        if actual != _STRUCTURED_SOURCE_LIVE_PATHS:
            raise StructuredSourceError(
                "structured-source live implementation inventory differs: "
                "missing=%s extra=%s" % (
                    sorted(_STRUCTURED_SOURCE_LIVE_PATHS - actual)[:10],
                    sorted(actual - _STRUCTURED_SOURCE_LIVE_PATHS)[:10]))

    def _reject_alternate_implementation_paths(self, repository_paths):
        """Close captured implementation, contract, schema, and vector paths."""
        repository_paths = set(repository_paths)
        index = classify_artifacts(repository_paths, self.registry)
        expected_paths = (_LIVE_IMPLEMENTATION
                          if self.repository_snapshot is not None else
                          _LIVE_IMPLEMENTATION & repository_paths)
        expected_code = {
            path for path in expected_paths
            if path.endswith((".css", ".js", ".mjs", ".py", ".sh"))}
        actual_code = {
            path for path, classification in index.items()
            if classification is ArtifactClass.IMPLEMENTATION_CODE}
        expected_contracts = {
            path for path in expected_paths if path.startswith("contracts/")}
        actual_contracts = {
            path for path in repository_paths if path.startswith("contracts/")}
        expected_schemas = {
            path for path in expected_paths if path.endswith(".xsd")}
        actual_schemas = {
            path for path in repository_paths if path.endswith(".xsd")}
        vector_prefixes = (
            "navigator/tests/vectors/", "structured_source/tests/vectors/")
        expected_vectors = {
            path for path in expected_paths
            if path.startswith(vector_prefixes)}
        actual_vectors = {
            path for path, classification in index.items()
            if classification is ArtifactClass.TEST_FIXTURE}
        expected = (expected_code | expected_contracts | expected_schemas |
                    expected_vectors)
        actual = (actual_code | actual_contracts | actual_schemas |
                  actual_vectors)
        if actual != expected:
            raise StructuredSourceError(
                "live implementation/contract/schema/vector inventory differs: "
                "missing=%s extra=%s" % (
                    sorted(expected - actual)[:10],
                    sorted(actual - expected)[:10]))

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
        relation_packages = {
            package_id for package_id, package in self.packages.items()
            if package["authorityScheme"] == "authored-relations-v1"}
        relation_edges = [
            (consumer["consumerId"], edge["packageId"])
            for consumer in self.registry["consumers"]
            for edge in consumer["edges"]
            if edge["packageId"] in relation_packages]
        expected_relation_edges = [
            ("navigator-af-prior-art",
             "aa11393us-af-claim-prior-art-passage-map"),
            ("navigator-af-prior-art",
             "aa11393us-af-prior-art-comparison-matrix"),
            ("navigator-na-prior-art",
             "aa11393us-na-claim-prior-art-passage-map"),
            ("navigator-na-prior-art",
             "aa11393us-na-prior-art-comparison-matrix"),
        ]
        if relation_edges != expected_relation_edges:
            raise StructuredSourceError(
                "current authored-relation consumer-edge census is not exact")
        repository_paths = self._disk_paths()
        snapshot_paths = self._snapshot_paths()
        if snapshot_paths is not None and not _LIVE_IMPLEMENTATION.issubset(
                snapshot_paths):
            raise StructuredSourceError(
                "live implementation census is incomplete")
        if snapshot_paths is not None:
            named_domains = (
                ("PDF", _PDF_NAMED_PATHS, lambda path:
                 "pdf-transcription" in path.casefold() or
                 "pdf_transcription" in path.casefold()),
                ("authored Markdown", _AUTHORED_MARKDOWN_NAMED_PATHS,
                 lambda path: "authored-markdown" in path.casefold() or
                 "authored_markdown" in path.casefold() or path in {
                     "structured_source/markdown.py",
                     "structured_source/schemas/authored.xsd"}),
                ("authored relations", _AUTHORED_RELATIONS_NAMED_PATHS,
                 lambda path: "authored-relations" in path.casefold() or
                 "authored_relations" in path.casefold() or
                 path.startswith("structured_source/relation_") or
                 path == "structured_source/schemas/relations.xsd"),
            )
            for label, expected, applies in named_domains:
                named_paths = {path for path in snapshot_paths if applies(path)}
                if named_paths != expected:
                    raise StructuredSourceError(
                        "%s named implementation/domain residue census differs" %
                        label)
        for path in sorted(_LIVE_IMPLEMENTATION):
            self.reader.read(path)
        retired = sorted(
            path for path in repository_paths
            if any(pattern.search(path) for pattern in _RETIRED_PATH_PATTERNS))
        if retired:
            raise StructuredSourceError(
                "retired structured-source path remains: %s" % retired[:10])
        self._reject_retired_imports(repository_paths)
        self._reject_alternate_structured_source_paths(repository_paths)
        self._reject_alternate_implementation_paths(repository_paths)
        self._reject_retired_control_residue(repository_paths)
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
        acceptance = load_registries(
            self.root, self.reader.read_absolute)
        from .routers import render_all
        for path, expected in render_all(self.registry).items():
            if self.reader.read(path) != expected:
                raise StructuredSourceError(
                    "registered package router is stale: %s" % path)
        for contract, registry in zip(CONTRACTS, acceptance):
            text = self.reader.read(contract["contractPath"]).decode("utf-8")
            start = contract["tableStart"]
            end = contract["tableEnd"]
            if text.count(start) != 1 or text.count(end) != 1 or \
                    text.split(start, 1)[1].split(end, 1)[0] != \
                    render_table(registry):
                raise StructuredSourceError(
                    "%s operative acceptance table is stale" %
                    contract["domain"])
        return acceptance

    def verify_all(self):
        if self._global_result is not None:
            return _copy_result(self._global_result)
        self._global_passes += 1
        acceptance = self._control_closure()
        results = [self.check(package_id) for package_id in sorted(self.packages)]
        handoffs = 0
        if self.repository_snapshot is not None:
            for consumer in self.registry["consumers"]:
                for edge in consumer["edges"]:
                    self.read_for_consumer(
                        consumer["consumerId"], edge["packageId"])
                    handoffs += 1
        schemes = Counter(result["authorityScheme"] for result in results)
        covered = sum(result["computedCoverage"].get("coveredItems", 0)
                      for result in results)
        self._global_result = _freeze_result({
            "status": "passed",
            "packages": len(results),
            "authoritySchemes": dict(sorted(schemes.items())),
            "computedCoveredItems": covered,
            "consumerEdges": sum(len(consumer["edges"])
                                 for consumer in self.registry["consumers"]),
            "consumerHandoffs": handoffs,
            "criteria": sum(len(registry["criteria"])
                            for registry in acceptance),
            "globalPasses": self._global_passes,
            "retiredResidue": 0,
        })
        return _copy_result(self._global_result)


def validate_corpus(root, *, byte_source, repository_snapshot,
                    registry=None, markdown_adapter=None):
    """Validate once and return the immutable same-context consumer boundary."""
    snapshot_digest = getattr(repository_snapshot, "digest", None)
    if not isinstance(snapshot_digest, str) or not snapshot_digest or \
            not callable(byte_source):
        raise StructuredSourceError(
            "structured-source validation requires retained snapshot bytes")
    context = VerificationContext(
        root, registry=registry, byte_source=byte_source,
        repository_snapshot=repository_snapshot,
        markdown_adapter=markdown_adapter)
    summary = context.verify_all()
    if not isinstance(summary, dict) or \
            summary.get("status") != "passed" or \
            summary.get("criteria") != len(CRITERIA) or \
            summary.get("globalPasses") != 1 or \
            type(summary.get("consumerEdges")) is not int or \
            summary.get("consumerEdges") != summary.get("consumerHandoffs"):
        raise StructuredSourceError(
            "structured-source validation did not pass the current criteria")
    handoffs = {}
    for consumer in context.registry["consumers"]:
        consumer_id = consumer["consumerId"]
        handoffs[consumer_id] = MappingProxyType({
            edge["packageId"]: context.read_for_consumer(
                consumer_id, edge["packageId"])
            for edge in consumer["edges"]
        })
    domains = tuple(MappingProxyType({
        "authorityScheme": contract["authorityScheme"],
        "criteria": len(contract["criteria"]),
        "domain": contract["domain"],
        "status": "passed",
    }) for contract in CONTRACTS)
    package_summaries = tuple(MappingProxyType({
        "authorityScheme": result["authorityScheme"],
        "coveredItems": result["computedCoverage"]["coveredItems"],
        "packageId": result["packageId"],
        "status": result["status"],
    }) for unused_package_id, result in sorted(
        context._package_results.items()))
    return ValidatedCorpus(
        snapshot_digest=snapshot_digest,
        domains=domains,
        result_ids=CRITERIA,
        package_summaries=package_summaries,
        consumer_handoffs=MappingProxyType(handoffs),
        parser_controls=context.parser_controls,
    )
