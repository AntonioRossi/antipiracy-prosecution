"""File gateways — the only file-traffic path in the pipeline (TDD §10,
guardrail 4; enforced by the registry-access AST test).

Two planes:

* content plane — registered sources and policy data, read through
  ``ContentGateway`` which records every read in a read log; the
  content-input lock is derived from that log.
* verification plane — append-only, digest-addressed records written
  through ``VerificationGateway``; an overwrite attempt is an error.

Artifact outputs are written through ``OutputGateway`` under a typed
output-kind registry; the command x kind privilege matrix
(``schema/planes.json``) is enforced here.
"""

import os

from . import canon


class GatewayError(RuntimeError):
    pass


class ContentGateway:
    """Reads content-plane files, recording every read (path, digest)."""

    def __init__(self, root, allowlist=None):
        self.root = os.path.abspath(root)
        self.allowlist = None if allowlist is None else {
            os.path.normpath(p) for p in allowlist
        }
        self.read_log = {}

    def _resolve(self, relpath):
        rel = os.path.normpath(relpath)
        if rel.startswith("..") or os.path.isabs(rel):
            raise GatewayError("content path escapes the tree: %r" % relpath)
        if self.allowlist is not None and rel not in self.allowlist:
            raise GatewayError(
                "path not in the edition's declared input allowlist: %r" % relpath
            )
        return rel, os.path.join(self.root, rel)

    def read_bytes(self, relpath):
        rel, path = self._resolve(relpath)
        with open(path, "rb") as fh:
            data = fh.read()
        self.read_log[rel] = canon.bytes_digest(data)
        return data

    def read_text(self, relpath):
        return self.read_bytes(relpath).decode("utf-8")

    def lock(self):
        """Content-input lock: the read log, sorted deterministically."""
        entries = [
            {"path": p, "digest": self.read_log[p]} for p in sorted(self.read_log)
        ]
        return {
            "canonVersion": canon.CANON_VERSION,
            "reads": entries,
            "lockDigest": canon.composite_digest(
                "aa11393:lock:c1",
                {"reads": entries, "canonVersion": canon.CANON_VERSION},
            ),
        }


class OutputGateway:
    """Writes artifact outputs under declared output kinds."""

    def __init__(self, root, command, planes):
        self.root = os.path.abspath(root)
        self.command = command
        self.planes = planes
        self.written = []

    def write(self, kind, relpath, data):
        allowed = self.planes["commands"].get(self.command, {}).get("writes", [])
        if kind not in allowed:
            raise GatewayError(
                "command %r may not write kind %r (privilege matrix)"
                % (self.command, kind)
            )
        plane = self.planes["kinds"].get(kind)
        if plane != "artifact":
            raise GatewayError(
                "kind %r is not an artifact output kind" % kind
            )
        path = os.path.join(self.root, os.path.normpath(relpath))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if isinstance(data, str):
            data = data.encode("utf-8")
        with open(path, "wb") as fh:
            fh.write(data)
        digest = canon.bytes_digest(data)
        self.written.append({"kind": kind, "path": relpath, "digest": digest})
        return digest


class ArtifactGateway:
    """Reads artifact outputs under declared read privileges (e.g. release
    reads the QA'd candidate; bundle reads sealed artifacts)."""

    def __init__(self, root, command, planes):
        self.root = os.path.abspath(root)
        self.command = command
        self.planes = planes

    def read(self, kind, relpath):
        allowed = self.planes["commands"].get(self.command, {}).get("reads", [])
        if kind not in allowed:
            raise GatewayError(
                "command %r may not read kind %r (privilege matrix)"
                % (self.command, kind))
        if self.planes["kinds"].get(kind) != "artifact":
            raise GatewayError("kind %r is not an artifact kind" % kind)
        path = os.path.join(self.root, os.path.normpath(relpath))
        with open(path, "rb") as fh:
            return fh.read()


def write_source(command, planes, root, relpath, data):
    """Content-plane source write (migrate: action classes b + c only).
    Permitted only for commands whose privilege row declares a source
    write."""
    writes = planes["commands"].get(command, {}).get("writes", [])
    if not any(w.startswith("source:") for w in writes):
        raise GatewayError(
            "command %r may not write content-plane sources" % command)
    path = os.path.join(os.path.abspath(root), os.path.normpath(relpath))
    if isinstance(data, str):
        data = data.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)


class VerificationGateway:
    """Append-only verification records, digest-addressed and immutable."""

    def __init__(self, root, command, planes):
        self.root = os.path.abspath(root)
        self.command = command
        self.planes = planes

    def append(self, kind, record):
        allowed = self.planes["commands"].get(self.command, {}).get("writes", [])
        if kind not in allowed:
            raise GatewayError(
                "command %r may not write kind %r (privilege matrix)"
                % (self.command, kind)
            )
        if self.planes["kinds"].get(kind) != "verification":
            raise GatewayError("kind %r is not a verification-record kind" % kind)
        tag = "aa11393:%s:c1" % kind
        digest = canon.composite_digest(tag, record)
        name = "%s_%s.json" % (kind, digest.rsplit(":", 1)[1][:24])
        path = os.path.join(self.root, name)
        payload = canon.canonical_json({"kind": kind, "digest": digest,
                                        "record": record})
        if os.path.exists(path):
            with open(path, "rb") as fh:
                existing = fh.read()
            if existing == payload:
                return digest, name  # identical write: idempotent, not an overwrite
            raise GatewayError(
                "verification records are immutable; %s already exists with "
                "different content" % name
            )
        os.makedirs(self.root, exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(payload)
        return digest, name

    def read_all(self, kind):
        """Read records of one kind (declared read privilege required)."""
        allowed = self.planes["commands"].get(self.command, {}).get("reads", [])
        if kind not in allowed:
            raise GatewayError(
                "command %r may not read kind %r (privilege matrix)"
                % (self.command, kind)
            )
        out = []
        if not os.path.isdir(self.root):
            return out
        import json
        for name in sorted(os.listdir(self.root)):
            if name.startswith(kind + "_") and name.endswith(".json"):
                with open(os.path.join(self.root, name), "rb") as fh:
                    out.append(json.loads(fh.read().decode("utf-8")))
        return out
