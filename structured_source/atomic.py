"""Plane-confined journaled publication with rollback and mutation checks."""

from __future__ import annotations

from contextlib import contextmanager
import fcntl
import os
import tempfile

from .errors import StructuredSourceError


@contextmanager
def command_lock(root: str):
    identity = os.path.realpath(root).encode("utf-8")
    import hashlib
    name = "aa11393-ssp-write-" + hashlib.sha256(identity).hexdigest()[:24] + ".lock"
    path = os.path.join(tempfile.gettempdir(), name)
    descriptor = os.open(path, os.O_CREAT | os.O_RDWR, 0o600)
    try:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise StructuredSourceError("another structured-source writer owns the command lock") from exc
        yield
    finally:
        fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def _safe_target(root: str, relative: str) -> str:
    if not isinstance(relative, str) or not relative or os.path.isabs(relative) or \
            "\\" in relative or any(part in {"", ".", ".."}
                                      for part in relative.split("/")):
        raise StructuredSourceError("writer target is not a canonical repository path")
    target = os.path.abspath(os.path.join(root, *relative.split("/")))
    if os.path.commonpath((os.path.abspath(root), target)) != os.path.abspath(root):
        raise StructuredSourceError("writer target escapes the repository")
    return target


def publish_set(root: str, outputs: dict[str, bytes], expected: dict[str, bytes | None]):
    """Publish a validated set, rolling back every attributable replacement.

    ``expected`` is the exact pre-command state for every owned path.  A
    mismatch is external mutation and prevents the first write.
    """
    if not outputs or set(outputs) != set(expected) or \
            not all(isinstance(data, bytes) for data in outputs.values()):
        raise StructuredSourceError("atomic output/expectation set is malformed")
    root = os.path.abspath(root)
    targets = {path: _safe_target(root, path) for path in outputs}

    def current_bytes(relative):
        target = targets[relative]
        if not os.path.lexists(target):
            return None
        if os.path.islink(target) or not os.path.isfile(target):
            raise StructuredSourceError(
                "writer target is not a regular file: %s" % relative)
        with open(target, "rb") as handle:
            return handle.read()

    def audit(replaced):
        for relative in targets:
            required = outputs[relative] if relative in replaced else expected[relative]
            if current_bytes(relative) != required:
                raise StructuredSourceError(
                    "writer target changed during publication: %s" % relative)

    with command_lock(root):
        for relative in targets:
            if current_bytes(relative) != expected[relative]:
                raise StructuredSourceError("writer target changed before publication: %s" % relative)

        temporaries = {}
        replaced = []
        created_directories = set()
        try:
            for relative, target in targets.items():
                parent = os.path.dirname(target)
                probe = parent
                while probe != root and not os.path.exists(probe):
                    created_directories.add(probe)
                    probe = os.path.dirname(probe)
                os.makedirs(parent, exist_ok=True)
                descriptor, temporary = tempfile.mkstemp(
                    prefix=".ssp-publish-", dir=parent)
                try:
                    os.fchmod(descriptor, 0o644)
                    with os.fdopen(descriptor, "wb") as handle:
                        handle.write(outputs[relative])
                        handle.flush()
                        os.fsync(handle.fileno())
                except BaseException:
                    try:
                        os.close(descriptor)
                    except OSError:
                        pass
                    raise
                temporaries[relative] = temporary
            for relative in sorted(targets):
                audit(set(replaced))
                os.replace(temporaries[relative], targets[relative])
                del temporaries[relative]
                replaced.append(relative)
            audit(set(replaced))
            for directory in sorted({os.path.dirname(path) for path in targets.values()}):
                descriptor = os.open(directory, os.O_RDONLY)
                try:
                    os.fsync(descriptor)
                finally:
                    os.close(descriptor)
        except BaseException as original:
            for temporary in temporaries.values():
                try:
                    os.unlink(temporary)
                except FileNotFoundError:
                    pass
            incomplete = []
            for relative in reversed(replaced):
                target = targets[relative]
                before = expected[relative]
                try:
                    current = current_bytes(relative)
                except StructuredSourceError:
                    incomplete.append(relative)
                    continue
                if current != outputs[relative]:
                    incomplete.append(relative)
                    continue
                if before is None:
                    try:
                        os.unlink(target)
                    except FileNotFoundError:
                        pass
                else:
                    descriptor, temporary = tempfile.mkstemp(
                        prefix=".ssp-rollback-", dir=os.path.dirname(target))
                    os.fchmod(descriptor, 0o644)
                    with os.fdopen(descriptor, "wb") as handle:
                        handle.write(before)
                        handle.flush()
                        os.fsync(handle.fileno())
                    os.replace(temporary, target)
            for directory in sorted({os.path.dirname(path) for path in targets.values()}):
                if not os.path.isdir(directory):
                    continue
                descriptor = os.open(directory, os.O_RDONLY)
                try:
                    os.fsync(descriptor)
                finally:
                    os.close(descriptor)
            for directory in sorted(created_directories,
                                    key=lambda item: item.count(os.sep), reverse=True):
                try:
                    os.rmdir(directory)
                except OSError:
                    pass
            if incomplete:
                raise StructuredSourceError(
                    "external mutation prevented complete attributable rollback: %s" %
                    sorted(incomplete)) from original
            raise
