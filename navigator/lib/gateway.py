"""File gateways — the only file-traffic path in the pipeline (TDD §10,
guardrail 4; enforced by the registry-access AST test).

Two planes:

* content plane — registered sources and policy data, read through
  ``ContentGateway`` which records every read in a read log; the
  content-input lock is derived from that log.
* verification plane — append-only, digest-addressed records written
  through ``VerificationGateway``; an overwrite attempt is an error.

Artifact outputs are written through ``OutputGateway`` under a typed
output-kind registry and a disjoint kind/path policy; the command x kind
privilege matrix (``schema/planes.json``) is enforced here.
"""

import os
import posixpath

from . import canon


class GatewayError(RuntimeError):
    pass


# Artifact kinds are not merely labels on an arbitrary artifact-plane path.
# Each kind owns one disjoint root-basename family.  Keeping this policy at the
# gateway boundary prevents a reviewed bundle member name from relabelling and
# overwriting (for example) a QA-bound candidate artifact.
ARTIFACT_PATH_POLICIES = {
    "preview": "preview-html",
    "candidate": "candidate-html",
    "sealed": "sealed-html",
    "artifact-checksum": "sealed-html-checksum",
    "bundle": "bundle-zip",
    "bundle-checksum": "bundle-zip-checksum",
    "bundle-manifest": "manifest-text",
}


def _artifact_basename(relpath):
    windows_stem = relpath.split(".", 1)[0].casefold() \
        if isinstance(relpath, str) else ""
    reserved = {"con", "prn", "aux", "nul"} | {
        "%s%d" % (prefix, number)
        for prefix in ("com", "lpt") for number in range(1, 10)
    }
    if not isinstance(relpath, str) or not relpath or \
            canon.normalize_nfc(relpath) != relpath or \
            any(character in relpath for character in '<>:"/\\|?*') or \
            windows_stem in reserved or \
            any(ord(character) < 0x20 or ord(character) == 0x7f
                for character in relpath):
        raise GatewayError(
            "artifact path must be one canonical root basename: %r" % relpath)
    return relpath


def _sealed_basename(name):
    folded = name.casefold()
    return name.endswith(".html") and len(name) > len(".html") and not (
        folded.startswith("candidate_") or folded.startswith("preview_"))


def validate_artifact_path(kind, relpath):
    """Return *relpath* after enforcing the kind's exact path family.

    Path safety and kind/path identity are separate checks: ``_safe_path``
    resolves the former against a concrete root, while this pure check makes
    artifact-kind aliases impossible even before filesystem access.
    """
    policy = ARTIFACT_PATH_POLICIES.get(kind)
    if policy is None:
        raise GatewayError("artifact kind %r has no path policy" % kind)
    name = _artifact_basename(relpath)
    valid = False
    if policy == "preview-html":
        prefix = "preview_"
        valid = name.startswith(prefix) and _sealed_basename(name[len(prefix):])
    elif policy == "candidate-html":
        prefix = "candidate_"
        valid = name.startswith(prefix) and _sealed_basename(name[len(prefix):])
    elif policy == "sealed-html":
        valid = _sealed_basename(name)
    elif policy == "sealed-html-checksum":
        suffix = ".sha256"
        valid = name.endswith(suffix) and _sealed_basename(name[:-len(suffix)])
    elif policy == "bundle-zip":
        valid = name.endswith(".zip") and len(name) > len(".zip")
    elif policy == "bundle-zip-checksum":
        suffix = ".sha256"
        base = name[:-len(suffix)] if name.endswith(suffix) else ""
        valid = base.endswith(".zip") and len(base) > len(".zip")
    elif policy == "manifest-text":
        valid = name == "MANIFEST.txt"
    if not valid:
        raise GatewayError(
            "artifact kind %r may not use path %r (policy %s)" %
            (kind, relpath, policy))
    return name


def _canonical_relative_path(relpath):
    """Return one platform-neutral repository-relative path identity."""
    if not isinstance(relpath, str) or not relpath or \
            canon.normalize_nfc(relpath) != relpath or \
            "\\" in relpath or "\x00" in relpath or \
            any(ord(character) < 0x20 or ord(character) == 0x7f
                for character in relpath) or \
            relpath.startswith("/") or ":" in relpath or \
            posixpath.normpath(relpath) != relpath or \
            any(part in ("", ".", "..") for part in relpath.split("/")):
        raise GatewayError(
            "path must be one canonical platform-neutral relative identity: %r"
            % relpath)
    return relpath


def _safe_path(root, relpath):
    """Resolve a file path beneath *root*, rejecting lexical and symlink
    escapes.

    Artifact names and source-write paths ultimately come from reviewed
    configuration/records, but the gateway is the enforcement boundary: a
    malformed configuration must not turn a typed write/read into arbitrary
    filesystem access.
    """
    rel = _canonical_relative_path(relpath)
    root_abs = os.path.abspath(root)
    path = os.path.abspath(os.path.join(root_abs, rel))
    try:
        lexical_ok = os.path.commonpath((root_abs, path)) == root_abs
    except ValueError:  # different drives on Windows
        lexical_ok = False
    if not lexical_ok:
        raise GatewayError("path escapes the gateway root: %r" % relpath)

    # realpath also resolves an existing symlink in any parent component.
    # It remains useful for not-yet-created outputs because existing parents
    # are still resolved.
    root_real = os.path.realpath(root_abs)
    path_real = os.path.realpath(path)
    try:
        real_ok = os.path.commonpath((root_real, path_real)) == root_real
    except ValueError:
        real_ok = False
    if not real_ok:
        raise GatewayError("path escapes the gateway root via symlink: %r"
                           % relpath)
    expected_real = os.path.abspath(os.path.join(root_real, rel))
    if path_real != expected_real:
        raise GatewayError(
            "path uses a symlink alias beneath the gateway root: %r"
            % relpath)
    return rel, path


class ContentGateway:
    """Reads content-plane files, recording every read (path, digest)."""

    def __init__(self, root, allowlist=None):
        self.root = os.path.abspath(root)
        if allowlist is None:
            self.allowlist = None
        else:
            if not isinstance(allowlist, (list, tuple)):
                raise GatewayError("content allowlist must be a path sequence")
            canonical = []
            seen = set()
            for index, entry in enumerate(allowlist):
                try:
                    path = _canonical_relative_path(entry)
                except GatewayError as exc:
                    raise GatewayError(
                        "content allowlist entry %d is invalid: %s" %
                        (index, exc))
                identity = path.casefold()
                if identity in seen:
                    raise GatewayError(
                        "content allowlist contains duplicate path identity %r"
                        % path)
                seen.add(identity)
                canonical.append(path)
            self.allowlist = frozenset(canonical)
        self.read_log = {}

    def _resolve(self, relpath):
        rel, path = _safe_path(self.root, relpath)
        # Artifact and verification stores are terminal planes.  Even an
        # authored allowlist must not turn their derived bytes back into a
        # content input.
        rel_key = rel.replace(os.sep, "/").casefold()
        for terminal in (
                os.path.join("navigator", "dist"),
                os.path.join("navigator", "records")):
            terminal_path = os.path.realpath(os.path.join(
                self.root, terminal))
            resolved_path = os.path.realpath(path)
            terminal_key = terminal.replace(os.sep, "/").casefold()
            try:
                enters_terminal = os.path.commonpath(
                    (terminal_path, resolved_path)) == terminal_path
            except ValueError:
                enters_terminal = False
            terminal_real_key = terminal_path.casefold()
            resolved_real_key = resolved_path.casefold()
            enters_terminal_casefold = (
                resolved_real_key == terminal_real_key or
                resolved_real_key.startswith(terminal_real_key + os.sep))
            if rel_key == terminal_key or \
                    rel_key.startswith(terminal_key + "/") or \
                    enters_terminal or enters_terminal_casefold:
                raise GatewayError(
                    "content reads may not enter terminal plane %r" % rel)
        if self.allowlist is not None and rel not in self.allowlist:
            raise GatewayError(
                "path not in the edition's declared input allowlist: %r" % relpath
            )
        return rel, path

    def read_bytes(self, relpath):
        rel, path = self._resolve(relpath)
        with open(path, "rb") as fh:
            data = fh.read()
        digest = canon.bytes_digest(data)
        previous = self.read_log.get(rel)
        if previous is not None and previous != digest:
            raise GatewayError(
                "content changed between reads of %r: %s -> %s"
                % (rel, previous, digest))
        self.read_log[rel] = digest
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
        validate_artifact_path(kind, relpath)
        _, path = _safe_path(self.root, relpath)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if isinstance(data, str):
            data = data.encode("utf-8")
        with open(path, "wb") as fh:
            fh.write(data)
        digest = canon.bytes_digest(data)
        self.written.append({"kind": kind, "path": relpath, "digest": digest})
        return digest

    def verify_written(self, kind, relpath, expected):
        """Read back one output written by this gateway and compare bytes.

        This is deliberately narrower than an artifact-plane read privilege:
        a command may verify only an exact ``(kind, path)`` that this gateway
        instance has already written.  Promotion transactions use the method
        for their postcondition before appending an authorization record.
        """
        if isinstance(expected, str):
            expected = expected.encode("utf-8")
        if not isinstance(expected, bytes):
            raise GatewayError("expected output bytes must be bytes or text")
        matches = [entry for entry in self.written
                   if entry["kind"] == kind and entry["path"] == relpath]
        if len(matches) != 1:
            raise GatewayError(
                "output %s:%s was not written exactly once by this gateway"
                % (kind, relpath))
        _, path = _safe_path(self.root, relpath)
        with open(path, "rb") as fh:
            actual = fh.read()
        if actual != expected:
            raise GatewayError("written output %s:%s failed read-back"
                               % (kind, relpath))
        digest = canon.bytes_digest(actual)
        if digest != matches[0]["digest"]:
            raise GatewayError("written output %s:%s digest changed"
                               % (kind, relpath))
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
        validate_artifact_path(kind, relpath)
        _, path = _safe_path(self.root, relpath)
        with open(path, "rb") as fh:
            return fh.read()


def write_source(command, planes, root, kind, relpath, data):
    """Content-plane source write (migrate: action classes b + c only).
    The exact typed source privilege and its narrow path family must both be
    declared; possession of one ``source:*`` privilege never grants another.
    """
    writes = planes["commands"].get(command, {}).get("writes", [])
    if not isinstance(kind, str) or not kind.startswith("source:") or \
            kind not in writes:
        raise GatewayError(
            "command %r may not write source kind %r" % (command, kind))
    rel, path = _safe_path(root, relpath)
    source_paths = {
        "source:relation-set": (
            os.path.join("navigator", "relations"), "", ".json"),
        "source:gate-inventory-locators": (
            os.path.join("navigator", "profiles"), "gates_", ".json"),
    }
    policy = source_paths.get(kind)
    if policy is None:
        raise GatewayError("source kind %r has no path policy" % kind)
    directory, prefix, suffix = policy
    basename = os.path.basename(rel)
    if os.path.dirname(rel) != directory or \
            not basename.startswith(prefix) or not basename.endswith(suffix):
        raise GatewayError(
            "source kind %r may not write path %r" % (kind, relpath))
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
        full_hex = digest.rsplit(":", 1)[1]
        name = "%s_%s.json" % (kind, full_hex)
        payload = canon.canonical_json({"kind": kind, "digest": digest,
                                        "record": record})
        os.makedirs(self.root, exist_ok=True)
        _, path = _safe_path(self.root, name)
        try:
            # Exclusive creation makes append-only behavior atomic.  A plain
            # exists-then-"wb" sequence could overwrite a record created in
            # the intervening race window.
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o666)
        except FileExistsError:
            # Re-resolve before reading so an existing symlink cannot turn an
            # idempotence check into a read outside the record store.
            _, existing_path = _safe_path(self.root, name)
            with open(existing_path, "rb") as fh:
                existing = fh.read()
            if existing == payload:
                return digest, name  # identical append is idempotent
            raise GatewayError(
                "verification records are immutable; %s already exists with "
                "different content" % name
            )
        with os.fdopen(fd, "wb") as fh:
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
                _, path = _safe_path(self.root, name)
                with open(path, "rb") as fh:
                    payload = fh.read()
                try:
                    envelope = canon.parse_json(payload)
                except (UnicodeDecodeError, ValueError) as exc:
                    raise GatewayError("invalid verification record %s: %s"
                                       % (name, exc))
                if not isinstance(envelope, dict) or \
                        set(envelope) != {"kind", "digest", "record"}:
                    raise GatewayError(
                        "verification record %s has an invalid envelope" % name)
                if envelope["kind"] != kind:
                    raise GatewayError(
                        "verification record %s declares kind %r, expected %r"
                        % (name, envelope["kind"], kind))
                try:
                    digest = canon.composite_digest(
                        "aa11393:%s:c1" % kind, envelope["record"])
                    canonical = canon.canonical_json(envelope)
                except (canon.CanonError, KeyError, TypeError) as exc:
                    raise GatewayError("invalid verification record %s: %s"
                                       % (name, exc))
                full_hex = digest.rsplit(":", 1)[1]
                expected_name = "%s_%s.json" % (kind, full_hex)
                if envelope["digest"] != digest:
                    raise GatewayError(
                        "verification record %s digest does not match its content"
                        % name)
                if name != expected_name:
                    raise GatewayError(
                        "verification record %s is not stored at digest "
                        "address %s" % (name, expected_name))
                if payload != canonical:
                    raise GatewayError(
                        "verification record %s is not canonical/immutable bytes"
                        % name)
                out.append(envelope)
        return out
