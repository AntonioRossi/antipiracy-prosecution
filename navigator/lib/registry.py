"""Consume structured-source packages only through frozen declared handoffs."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

from structured_source import CONTENT_NAMESPACE
from structured_source.canonical import raw_digest
from structured_source.parser import (PARSER_CONTROL_PATHS, ParserControls,
                                      parse_artifact)
from structured_source.pdf_transcription import (
    PDFTranscriptionSurface, AUTHORITY_SCHEME as PDF_AUTHORITY_SCHEME)


REGISTRY_PATH = "structured_source/registry/content.json"
C = "{%s}" % CONTENT_NAMESPACE


class RegistryError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class SourceDocument:
    document_id: str
    authority_scheme: str
    xml_role: str
    xml_raw_digest: str
    registered_path: str


@dataclass(frozen=True, slots=True)
class ConsumerInput:
    """One snapshot-bound set of handoffs for a declared navigator consumer."""

    consumer_id: str
    snapshot_digest: str
    handoffs: MappingProxyType
    parser_controls: ParserControls


class Registry:
    """Resolve only the already-validated inputs handed to one consumer."""

    def __init__(self, gw, consumer_input):
        if not isinstance(consumer_input, ConsumerInput) or \
                consumer_input.consumer_id not in {"navigator-na", "navigator-af"} or \
                not isinstance(consumer_input.snapshot_digest, str) or \
                not consumer_input.snapshot_digest or \
                not isinstance(consumer_input.handoffs, MappingProxyType) or \
                not isinstance(consumer_input.parser_controls, ParserControls):
            raise RegistryError("navigator consumer input is not a frozen handoff set")
        handoffs = consumer_input.handoffs
        if len(handoffs) != 2 or set(handoffs) != {
                "pct-as-filed-dossier",
                "aa11393us-%s-us-claim-set" %
                consumer_input.consumer_id.rsplit("-", 1)[-1]}:
            raise RegistryError("navigator consumer handoff inventory is not exact")
        validation_paths = set()
        for package_id, handoff in handoffs.items():
            if handoff.get("consumerId") != consumer_input.consumer_id or \
                    handoff.get("packageId") != package_id or \
                    handoff.get("inputRepresentation") != "xml":
                raise RegistryError("navigator consumer handoff identity is stale")
            try:
                gw.bind_consumer_handoff(handoff)
            except Exception as exc:
                raise RegistryError(
                    "navigator consumer handoff binding failed") from exc
            validation_paths.update(path for path, unused_digest
                                    in handoff["validationReads"])
        self._gw = gw
        self._consumer_id = consumer_input.consumer_id
        self._handoffs = handoffs
        self._parser_controls = consumer_input.parser_controls
        self._validation_paths = tuple(sorted(validation_paths))
        self._documents = {}
        self._semantic_inputs = {}

    def consumer_packages(self, consumer_id: str,
                          claim_package: str) -> tuple[str, str]:
        expected = {claim_package, "pct-as-filed-dossier"}
        if consumer_id != self._consumer_id or set(self._handoffs) != expected:
            raise RegistryError(
                "navigator consumer must resolve exactly claim and PCT handoffs")
        return claim_package, "pct-as-filed-dossier"

    def load_document(self, package_id: str):
        if package_id in self._semantic_inputs:
            return self._documents[package_id], self._semantic_inputs[package_id]
        handoff = self._handoffs.get(package_id)
        if handoff is None:
            raise RegistryError("handed package does not resolve: %s" % package_id)
        data = handoff["bytes"]
        scheme = handoff["authorityScheme"]
        role = handoff["representationRole"]
        path = handoff["path"]
        if scheme == "authored-markdown-v1":
            if role != "generated-xml" or handoff["surface"] is not None or \
                    handoff["assets"]:
                raise RegistryError("authored claim handoff is malformed")
            try:
                semantic_input = parse_artifact(
                    data, "authored-document", controls=self._parser_controls)
            except Exception as exc:
                raise RegistryError(
                    "handed claim XML failed its retained controls") from exc
            identity = semantic_input.root.find(C + "documentIdentity")
            if identity is None or identity.get("documentId") != package_id:
                raise RegistryError("handed claim XML identity is stale")
            xml_digest = semantic_input.raw_digest
        elif scheme == PDF_AUTHORITY_SCHEME:
            semantic_input = handoff["surface"]
            if role != "transcription-xml" or not isinstance(
                    semantic_input, PDFTranscriptionSurface) or \
                    semantic_input.package_id != package_id or \
                    semantic_input.authority_scheme != scheme or \
                    semantic_input.representation_role != role or \
                    semantic_input.xml_path != path or \
                    semantic_input.xml_raw_digest != raw_digest(data) or \
                    set(handoff["assets"]) != {
                        asset.path for asset in semantic_input.assets}:
                raise RegistryError("PDF transcription handoff is malformed")
            xml_digest = semantic_input.xml_raw_digest
        else:
            raise RegistryError("handed package authority scheme is unsupported")
        document = SourceDocument(
            document_id=package_id, authority_scheme=scheme, xml_role=role,
            xml_raw_digest=xml_digest, registered_path=path)
        self._documents[package_id] = document
        self._semantic_inputs[package_id] = semantic_input
        return document, semantic_input

    def handoff(self, package_id: str):
        try:
            return self._handoffs[package_id]
        except KeyError as exc:
            raise RegistryError("handed package does not resolve") from exc

    def get_document(self, document_id: str) -> SourceDocument:
        if document_id not in self._documents:
            self.load_document(document_id)
        return self._documents[document_id]

    @property
    def documents(self):
        return tuple(self._documents[key] for key in sorted(self._documents))

    @property
    def parser_controls(self):
        return self._parser_controls

    @property
    def validation_paths(self):
        return self._validation_paths
