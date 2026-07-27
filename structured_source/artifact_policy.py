"""Exhaustive current-state artifact classification for verification policy."""

from __future__ import annotations

from enum import Enum
from types import MappingProxyType

from .errors import StructuredSourceError


class ArtifactClass(str, Enum):
    IMPLEMENTATION_CODE = "implementation-code"
    EXECUTABLE_CONTROL = "executable-control"
    OPERATIVE_DOCUMENTATION = "operative-documentation"
    AUTHORITY_CONTENT = "authority-content"
    GENERATED_EVIDENCE_REVIEW = "generated-evidence-review"
    GENERATED_PRODUCT = "generated-product"
    TEST_FIXTURE = "test-fixture"
    BINARY_SOURCE = "binary-source"
    REGISTERED_ASSET = "registered-asset"


_POLICY = MappingProxyType({
    ArtifactClass.IMPLEMENTATION_CODE: "structural-code",
    ArtifactClass.EXECUTABLE_CONTROL: "structural-control",
    ArtifactClass.OPERATIVE_DOCUMENTATION: "structural-document",
    ArtifactClass.AUTHORITY_CONTENT: "authority-content",
    ArtifactClass.GENERATED_EVIDENCE_REVIEW: "derived-content",
    ArtifactClass.GENERATED_PRODUCT: "derived-product",
    ArtifactClass.TEST_FIXTURE: "fixture-data",
    ArtifactClass.BINARY_SOURCE: "raw-binding",
    ArtifactClass.REGISTERED_ASSET: "raw-binding",
})

_CODE_SUFFIXES = (".css", ".js", ".mjs", ".py", ".sh")
_CONTROL_SUFFIXES = (
    ".json", ".lock", ".toml", ".xml", ".xsd", ".yaml", ".yml",
)
_DOCUMENT_SUFFIXES = (".md", ".txt")
_GENERATED_SUFFIXES = (".html", ".sha256")
_BINARY_SUFFIXES = (
    ".doc", ".docx", ".gif", ".ico", ".jpeg", ".jpg", ".odt", ".pdf",
    ".png", ".svg", ".webp", ".zip",
)
_CONTROL_BASENAMES = frozenset({
    ".gitattributes", ".gitignore", ".python-version",
})
_TEST_FIXTURE_ROOTS = (
    "navigator/tests/vectors/", "structured_source/tests/vectors/",
)


def artifact_policy():
    """Return the complete immutable class-to-policy dispatch."""
    if set(_POLICY) != set(ArtifactClass):
        raise StructuredSourceError("artifact-class policy census is incomplete")
    return _POLICY


def classify_artifacts(repository_paths, registry) -> MappingProxyType:
    """Classify every supplied snapshot path exactly once."""
    if not isinstance(repository_paths, set) or not isinstance(registry, dict):
        raise TypeError("artifact classification requires paths and registry")
    files = registry.get("files")
    packages = registry.get("packages")
    if not isinstance(files, list) or not isinstance(packages, list):
        raise StructuredSourceError("artifact classification registry is malformed")
    files_by_id = {
        entry.get("fileId"): entry for entry in files
        if isinstance(entry, dict) and isinstance(entry.get("fileId"), str)}
    if len(files_by_id) != len(files):
        raise StructuredSourceError("artifact classification file census differs")
    authority_by_file = {}
    for package in packages:
        if not isinstance(package, dict):
            raise StructuredSourceError(
                "artifact classification package is malformed")
        scheme = package.get("authorityScheme")
        for field in ("xmlFile", "markdownFile", "sourceManifestFile"):
            file_id = package.get(field)
            if file_id is not None:
                previous = authority_by_file.setdefault(file_id, scheme)
                if previous != scheme:
                    raise StructuredSourceError(
                        "artifact authority classification is ambiguous")
        for field in ("storedSourceFiles", "assetFiles", "convenienceFiles"):
            for file_id in package.get(field, []):
                previous = authority_by_file.setdefault(file_id, scheme)
                if previous != scheme:
                    raise StructuredSourceError(
                        "artifact authority classification is ambiguous")

    registered = {}
    for file_id, entry in files_by_id.items():
        path = entry.get("path")
        role = entry.get("role")
        scheme = authority_by_file.get(file_id)
        if not isinstance(path, str) or not isinstance(role, str):
            raise StructuredSourceError("registered artifact is malformed")
        if role in {"authored-markdown", "transcription-xml"}:
            classification = ArtifactClass.AUTHORITY_CONTENT
        elif role == "generated-markdown" and scheme == \
                "pdf-evidence-transcription-v1":
            classification = ArtifactClass.GENERATED_EVIDENCE_REVIEW
        elif role in {"stored-evidence", "convenience-derivative"}:
            classification = ArtifactClass.BINARY_SOURCE
        elif role == "asset":
            classification = ArtifactClass.REGISTERED_ASSET
        elif role in {"generated-markdown", "generated-xml"}:
            classification = ArtifactClass.GENERATED_PRODUCT
        elif role == "router":
            classification = ArtifactClass.OPERATIVE_DOCUMENTATION
        elif role in {"consumer-dependency", "relation-xml", "source-manifest"}:
            classification = ArtifactClass.EXECUTABLE_CONTROL
        else:
            raise StructuredSourceError(
                "registered artifact role has no current class: %s" % role)
        previous = registered.setdefault(path, classification)
        if previous is not classification:
            raise StructuredSourceError(
                "registered artifact classification is ambiguous: %s" % path)

    classified = {}
    for path in sorted(repository_paths):
        if not isinstance(path, str) or not path:
            raise StructuredSourceError("artifact path is malformed")
        classification = registered.get(path)
        if classification is None:
            lowered = path.casefold()
            if lowered.startswith("navigator/dist/") or \
                    lowered.endswith(_GENERATED_SUFFIXES):
                classification = ArtifactClass.GENERATED_PRODUCT
            elif lowered.endswith(_CODE_SUFFIXES):
                classification = ArtifactClass.IMPLEMENTATION_CODE
            elif lowered.startswith(_TEST_FIXTURE_ROOTS):
                classification = ArtifactClass.TEST_FIXTURE
            elif lowered.endswith(_CONTROL_SUFFIXES) or \
                    lowered.rsplit("/", 1)[-1] in _CONTROL_BASENAMES:
                classification = ArtifactClass.EXECUTABLE_CONTROL
            elif lowered.endswith(_DOCUMENT_SUFFIXES) or "/readme" in lowered or \
                    lowered.startswith(("license", "notice")):
                classification = ArtifactClass.OPERATIVE_DOCUMENTATION
            elif lowered.endswith(_BINARY_SUFFIXES):
                classification = ArtifactClass.BINARY_SOURCE
            else:
                raise StructuredSourceError(
                    "artifact path has no current class: %s" % path)
        classified[path] = classification
    if set(classified) != repository_paths or set(_POLICY) != set(ArtifactClass):
        raise StructuredSourceError("artifact classification census is incomplete")
    return MappingProxyType(classified)
