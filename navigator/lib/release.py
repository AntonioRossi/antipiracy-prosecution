"""Mechanical candidate sealing and atomic generated-product writes."""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile

from . import canon


class ReleaseError(RuntimeError):
    """A candidate cannot be reproduced or a generated write is unsafe."""


_OUTPUT_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,239}\Z")


def validate_output_name(value):
    stem = value.split(".", 1)[0].casefold() \
        if isinstance(value, str) else ""
    reserved = {"con", "prn", "aux", "nul"} | {
        "%s%d" % (prefix, number)
        for prefix in ("com", "lpt") for number in range(1, 10)}
    if not isinstance(value, str) or _OUTPUT_NAME.fullmatch(value) is None or \
            value in {".", ".."} or value.endswith(".") or stem in reserved:
        raise ReleaseError("generated product name is not one safe basename")
    return value


def candidate_name(artifact_name):
    validate_output_name(artifact_name)
    if not artifact_name.endswith(".html") or \
            artifact_name.startswith(("candidate_", "preview_")):
        raise ReleaseError("artifact name is not a sealed HTML basename")
    return "candidate_" + artifact_name


def checksum_text(name, data):
    validate_output_name(name)
    if not isinstance(data, bytes):
        raise ReleaseError("checksum input is not bytes")
    return ("%s  %s\n" % (canon.bytes_digest(data), name)).encode("ascii")


def verify_checksum(checksum_bytes, name, data):
    expected = checksum_text(name, data)
    if checksum_bytes != expected:
        raise ReleaseError("detached checksum is stale for %s" % name)
    return canon.bytes_digest(data)


def safe_output_path(root, name):
    name = validate_output_name(name)
    root = os.path.abspath(root)
    if os.path.islink(root):
        raise ReleaseError("generated product directory may not be a symlink")
    path = os.path.abspath(os.path.join(root, name))
    expected_real = os.path.join(os.path.realpath(root), name)
    if os.path.dirname(path) != root or \
            os.path.realpath(path) != expected_real:
        raise ReleaseError("generated product path escapes through a symlink")
    return path


def read_output(root, name):
    path = safe_output_path(root, name)
    try:
        with open(path, "rb") as handle:
            return handle.read()
    except OSError as exc:
        raise ReleaseError("generated product is unavailable: %s" % name) from exc


def write_outputs_atomic(root, outputs):
    """Validate all bytes, stage all files, then replace generated outputs.

    Semantic authorities cannot be addressed because every key is one basename
    under the supplied generated-product directory.  Abrupt termination may
    leave a mixed generated set; current-state validation rejects that set.
    """
    if not isinstance(outputs, dict) or not outputs:
        raise ReleaseError("generated output set is empty or malformed")
    root = os.path.abspath(root)
    os.makedirs(root, exist_ok=True)
    if os.path.islink(root) or not os.path.isdir(root):
        raise ReleaseError("generated product root is not a real directory")
    staged = []
    try:
        for name in sorted(outputs):
            path = safe_output_path(root, name)
            data = outputs[name]
            if not isinstance(data, bytes):
                raise ReleaseError("generated product %s is not bytes" % name)
            descriptor, temporary = tempfile.mkstemp(
                prefix=".%s." % name, suffix=".tmp", dir=root)
            try:
                with os.fdopen(descriptor, "wb") as handle:
                    handle.write(data)
                    handle.flush()
                    os.fsync(handle.fileno())
                os.chmod(temporary, 0o644)
            except BaseException:
                try:
                    os.close(descriptor)
                except OSError:
                    pass
                try:
                    os.unlink(temporary)
                except FileNotFoundError:
                    pass
                raise
            staged.append((temporary, path, name, data))
        for temporary, path, unused_name, unused_data in staged:
            os.replace(temporary, path)
        staged.clear()
        written = []
        for name in sorted(outputs):
            data = read_output(root, name)
            if data != outputs[name]:
                raise ReleaseError("generated product readback differs: %s" % name)
            written.append({"digest": canon.bytes_digest(data), "name": name})
        return written
    finally:
        for temporary, unused_path, unused_name, unused_data in staged:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass


def fresh_candidate(root, edition_id, timeout=600):
    """Derive candidate bytes in a fresh interpreter without a CLI alias."""
    if edition_id not in {"na", "af"}:
        raise ReleaseError("edition is not current")
    root = os.path.abspath(root)
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    script = (
        "import sys\n"
        "from navigator.lib import currentstate,snapshot\n"
        "r=snapshot.RepositorySnapshot.capture(currentstate.ROOT,retain_bytes=True)\n"
        "unused_model,data,unused_lock=currentstate.derive(sys.argv[1],"
        "'candidate',r)\n"
        "sys.stdout.buffer.write(data)\n"
    )
    try:
        result = subprocess.run(
            [sys.executable, "-B", "-c", script, edition_id],
            cwd=root, capture_output=True, timeout=timeout, env=environment)
        if result.returncode:
            detail = result.stderr.decode("utf-8", "replace").strip()
            raise ReleaseError(
                "fresh candidate derivation failed: %s" %
                (detail[-4000:] or "no diagnostic"))
        return result.stdout
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ReleaseError("fresh candidate derivation could not complete") from exc


def prove_candidate(derived, stored, reproduced):
    if not all(isinstance(value, bytes)
               for value in (derived, stored, reproduced)):
        raise ReleaseError("candidate proof inputs are not bytes")
    if stored != derived:
        raise ReleaseError("stored candidate is stale")
    if reproduced != derived:
        raise ReleaseError("candidate is not reproducible across interpreters")
    return canon.bytes_digest(derived)
