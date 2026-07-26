"""One read-only gateway for every navigator semantic input."""

from __future__ import annotations

import os
import posixpath
import re
from types import MappingProxyType

from structured_source.parser import parse_validated_xml

from . import canon

_MAX_INPUT_BYTES = 32 * 1024 * 1024
_FORBIDDEN_ROOTS = (".git", "navigator/dist", "navigator/records")
_RAW_DIGEST = re.compile(r"sha256/raw:([0-9a-f]{64})\Z")


class GatewayError(RuntimeError):
    pass


def _canonical_path(value: str) -> str:
    if not isinstance(value, str) or not value or \
            canon.normalize_nfc(value) != value or "\\" in value or \
            "\x00" in value or value.startswith("/") or ":" in value or \
            posixpath.normpath(value) != value or any(
                part in {"", ".", ".."} for part in value.split("/")) or \
            any(ord(character) < 0x20 or ord(character) == 0x7f
                for character in value):
        raise GatewayError(
            "content path is not one canonical repository-relative identity")
    folded = value.casefold()
    if any(folded == root.casefold() or
           folded.startswith(root.casefold() + "/")
           for root in _FORBIDDEN_ROOTS):
        raise GatewayError("derived or repository-internal content is unreadable")
    return value


def _resolve(root: str, relative: str) -> tuple[str, str]:
    relative = _canonical_path(relative)
    absolute = os.path.abspath(os.path.join(root, *relative.split("/")))
    root_real = os.path.realpath(root)
    absolute_real = os.path.realpath(absolute)
    try:
        within = os.path.commonpath((root_real, absolute_real)) == root_real
    except ValueError:
        within = False
    expected = os.path.abspath(os.path.join(root_real, *relative.split("/")))
    if not within or absolute_real != expected:
        raise GatewayError("content path escapes the repository or uses a symlink")
    return relative, absolute


class ContentGateway:
    """Secure, immutable-read access to the current repository snapshot.

    Every successful read has one canonical path identity and one stable byte
    digest. Re-reading changed bytes fails. The gateway has no write method,
    record store, output plane, compatibility source, or fallback path.
    """

    def __init__(self, root, *, byte_source=None, allowlist=None):
        root = os.path.abspath(os.fspath(root))
        if not os.path.isdir(root) or os.path.islink(root):
            raise GatewayError("content root must be a real repository directory")
        if byte_source is not None and not callable(byte_source):
            raise GatewayError("byte_source must be callable")
        if allowlist is None:
            allowed = None
        else:
            if not isinstance(allowlist, (list, tuple, set, frozenset)):
                raise GatewayError("allowlist must be a finite path collection")
            paths = [_canonical_path(item) for item in allowlist]
            if len(paths) != len(set(paths)) or \
                    len(paths) != len({item.casefold() for item in paths}):
                raise GatewayError("allowlist contains duplicate path identities")
            allowed = frozenset(paths)
        self.root = root
        self._byte_source = byte_source
        self._allowlist = allowed
        self._reads: dict[str, str] = {}
        self._handoff_paths: set[str] = set()
        self._sealed = False

    @property
    def read_log(self):
        return MappingProxyType(dict(self._reads))

    def read_bytes(self, relative: str) -> bytes:
        if self._sealed:
            raise GatewayError("content gateway is sealed")
        relative, absolute = _resolve(self.root, relative)
        if relative in self._handoff_paths:
            raise GatewayError(
                "validated consumer input must be consumed from its handoff")
        if self._allowlist is not None and relative not in self._allowlist:
            raise GatewayError("content path is outside the exact allowlist")
        try:
            if self._byte_source is None:
                if not os.path.isfile(absolute) or os.path.islink(absolute):
                    raise OSError("input is absent, non-regular, or a symlink")
                with open(absolute, "rb") as handle:
                    data = handle.read(_MAX_INPUT_BYTES + 1)
            else:
                data = self._byte_source(absolute)
        except (OSError, KeyError) as exc:
            raise GatewayError("content input is unreadable: %s" % relative) from exc
        if not isinstance(data, bytes):
            raise GatewayError("byte_source returned non-bytes")
        if not data or len(data) > _MAX_INPUT_BYTES:
            raise GatewayError("content input size is outside the closed limit")
        digest = canon.bytes_digest(data)
        previous = self._reads.get(relative)
        if previous is not None and previous != digest:
            raise GatewayError("content changed between exact reads: %s" % relative)
        self._reads[relative] = digest
        return data

    def bind_consumer_handoff(self, handoff) -> None:
        """Bind one immutable structured-source handoff without reopening it."""
        if self._sealed or not isinstance(handoff, MappingProxyType) or \
                set(handoff) != {
                    "assets", "authorityScheme", "bytes", "consumerId",
                    "dependencies", "inputRepresentation", "packageId",
                    "path", "representationRole", "surface",
                    "validationReads"}:
            raise GatewayError("structured-source consumer handoff is malformed")
        if handoff["inputRepresentation"] != "xml" or \
                not isinstance(handoff["bytes"], bytes) or \
                not isinstance(handoff["dependencies"], MappingProxyType) or \
                not isinstance(handoff["assets"], MappingProxyType):
            raise GatewayError("structured-source XML handoff is incomplete")
        reads = handoff["validationReads"]
        if not isinstance(reads, tuple) or not reads:
            raise GatewayError("structured-source validation-read census is absent")
        bound = {}
        folded = set()
        for entry in reads:
            if not isinstance(entry, tuple) or len(entry) != 2:
                raise GatewayError(
                    "structured-source validation-read entry is malformed")
            path, digest = entry
            path = _canonical_path(path)
            match = _RAW_DIGEST.fullmatch(digest) \
                if isinstance(digest, str) else None
            if match is None or path.casefold() in folded:
                raise GatewayError(
                    "structured-source validation-read identity is malformed")
            folded.add(path.casefold())
            bound[path] = "sha256/c1:" + match.group(1)
        path = _canonical_path(handoff["path"])
        if path not in bound or canon.bytes_digest(handoff["bytes"]) != bound[path]:
            raise GatewayError(
                "structured-source representation binding is stale")
        for byte_mapping in (handoff["dependencies"], handoff["assets"]):
            for byte_path, data in byte_mapping.items():
                byte_path = _canonical_path(byte_path)
                if not isinstance(data, bytes) or byte_path not in bound or \
                        canon.bytes_digest(data) != bound[byte_path]:
                    raise GatewayError(
                        "structured-source handed byte binding is stale")
        for bound_path, digest in bound.items():
            previous = self._reads.get(bound_path)
            if previous is not None:
                if bound_path not in self._handoff_paths:
                    raise GatewayError(
                        "structured-source handoff followed an ordinary read")
                if previous != digest:
                    raise GatewayError(
                        "structured-source handoffs bind different bytes")
            self._reads[bound_path] = digest
            self._handoff_paths.add(bound_path)

    def seal(self, expected_paths=None) -> None:
        """End ingestion after proving the exact semantic read closure."""
        if expected_paths is not None:
            try:
                supplied = tuple(expected_paths)
                expected = {_canonical_path(path) for path in supplied}
            except TypeError as exc:
                raise GatewayError("expected read closure is not finite") from exc
            if len(expected) != len(supplied) or \
                    set(self._reads) != expected:
                raise GatewayError(
                    "content reads differ from the exact declared closure")
        self._sealed = True

    def read_text(self, relative: str) -> str:
        data = self.read_bytes(relative)
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise GatewayError("content text is not UTF-8: %s" % relative) from exc
        if text.startswith("\ufeff") or "\r" in text or \
                canon.normalize_nfc(text) != text:
            raise GatewayError("content text is not exact NFC/LF text")
        return text

    def read_validated_xml(self, relative: str, schema_relative: str, *,
                           expected_namespace: str, expected_root: str,
                           parser_controls=None):
        """Read and secure-validate one consumer-owned XML vocabulary."""
        data = self.read_bytes(relative)
        schema = self.read_bytes(schema_relative)
        try:
            return parse_validated_xml(
                data, schema, expected_namespace=expected_namespace,
                expected_root=expected_root, controls=parser_controls)
        except Exception as exc:
            raise GatewayError(
                "registered XML input failed its closed XSD: %s" % relative) from exc

    def lock(self) -> dict:
        reads = tuple(
            {"path": path, "digest": self._reads[path]}
            for path in sorted(self._reads))
        payload = {"canonVersion": canon.CANON_VERSION, "reads": reads}
        return {
            "canonVersion": canon.CANON_VERSION,
            "reads": list(reads),
            "lockDigest": canon.composite_digest("aa11393:lock:c1", payload),
        }
