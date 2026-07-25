"""Resolve navigator inputs exclusively through the live content registry."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

from structured_source import CONTENT_NAMESPACE
from structured_source.parser import parse_artifact
from structured_source.registry import validate_registry

from . import canon

REGISTRY_PATH = "structured_source/registry/content.json"
C = "{%s}" % CONTENT_NAMESPACE


class RegistryError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class SourceDocument:
    document_id: str
    authority_scheme: str
    xml_role: str
    semantic_digest: str
    registered_path: str


class Registry:
    """Current package/consumer resolver with no corpus or path fallback."""

    def __init__(self, gw):
        try:
            value = canon.parse_json(gw.read_text(REGISTRY_PATH))
            validate_registry(value)
        except Exception as exc:
            raise RegistryError("live structured-source registry is invalid") from exc
        self._gw = gw
        self._files = MappingProxyType({
            item["fileId"]: MappingProxyType(dict(item))
            for item in value["files"]})
        self._packages = MappingProxyType({
            item["packageId"]: MappingProxyType(dict(item))
            for item in value["packages"]})
        self._consumers = MappingProxyType({
            item["consumerId"]: tuple(MappingProxyType(dict(edge))
                                      for edge in item["edges"])
            for item in value["consumers"]})
        self._artifacts = {}
        self._documents = {}

    def consumer_packages(self, consumer_id: str, claim_package: str) -> tuple[str, str]:
        edges = self._consumers.get(consumer_id)
        expected = {claim_package, "pct-as-filed-dossier"}
        if edges is None or len(edges) != 2 or \
                {edge["packageId"] for edge in edges} != expected or any(
                    edge["inputRepresentation"] != "xml" or edge["dependencies"]
                    for edge in edges):
            raise RegistryError(
                "navigator consumer must resolve exactly claim and PCT packages as XML")
        return claim_package, "pct-as-filed-dossier"

    def xml_path(self, package_id: str) -> tuple[str, str, str]:
        package = self._packages.get(package_id)
        if package is None:
            raise RegistryError("registered package does not resolve: %s" % package_id)
        file_entry = self._files.get(package["xmlFile"])
        scheme = package["authorityScheme"]
        expected_role = {
            "authored-markdown-v1": "generated-xml",
            "pdf-evidence-transcription-v1": "transcription-xml",
        }.get(scheme)
        if file_entry is None or expected_role is None or \
                file_entry["role"] != expected_role:
            raise RegistryError("package has no current registered XML interface")
        return file_entry["path"], scheme, expected_role

    def load_document(self, package_id: str):
        if package_id in self._artifacts:
            return self._documents[package_id], self._artifacts[package_id]
        path, scheme, role = self.xml_path(package_id)
        data = self._gw.read_bytes(path)
        kind = ("authored-document" if scheme == "authored-markdown-v1"
                else "content-document")
        try:
            artifact = parse_artifact(data, kind)
        except Exception as exc:
            raise RegistryError(
                "registered XML failed its secure structured-source contract") from exc
        identity = artifact.root.find(C + "documentIdentity")
        if identity is None or identity.get("documentId") != package_id:
            raise RegistryError("registered XML document identity is stale")
        document = SourceDocument(
            document_id=package_id,
            authority_scheme=scheme,
            xml_role=role,
            semantic_digest=artifact.semantic_digest,
            registered_path=path,
        )
        self._artifacts[package_id] = artifact
        self._documents[package_id] = document
        return document, artifact

    def asset_paths(self, package_id: str) -> tuple[str, ...]:
        package = self._packages.get(package_id)
        if package is None:
            raise RegistryError("registered package does not resolve: %s" % package_id)
        paths = []
        for file_id in package["assetFiles"]:
            entry = self._files.get(file_id)
            if entry is None or entry["role"] != "asset":
                raise RegistryError("package asset registration is malformed")
            paths.append(entry["path"])
        return tuple(sorted(paths))

    def get_document(self, document_id: str) -> SourceDocument:
        if document_id not in self._documents:
            self.load_document(document_id)
        return self._documents[document_id]

    @property
    def documents(self):
        return tuple(self._documents[key] for key in sorted(self._documents))
