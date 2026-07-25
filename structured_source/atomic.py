"""Plane-confined journaled publication with rollback and mutation checks."""

from __future__ import annotations

from contextlib import contextmanager
import fcntl
import os
import secrets
import stat
import tempfile

from .errors import StructuredSourceError


@contextmanager
def command_lock(root: str):
    unused_root, real_root = _safe_root(root)
    identity = real_root.encode("utf-8")
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


def _safe_root(root: str) -> tuple[str, str]:
    if not isinstance(root, str) or not root:
        raise StructuredSourceError("writer root is malformed")
    absolute = os.path.abspath(root)
    if not os.path.lexists(absolute) or os.path.islink(absolute) or \
            not os.path.isdir(absolute):
        raise StructuredSourceError(
            "writer root is absent, non-directory, or a symlink")
    return absolute, os.path.realpath(absolute)


def _safe_target(root: str, relative: str) -> str:
    if not isinstance(relative, str) or not relative or os.path.isabs(relative) or \
            "\\" in relative or any(part in {"", ".", ".."}
                                      for part in relative.split("/")):
        raise StructuredSourceError("writer target is not a canonical repository path")
    absolute_root, real_root = _safe_root(root)
    target = os.path.abspath(os.path.join(absolute_root, *relative.split("/")))
    if os.path.commonpath((absolute_root, target)) != absolute_root:
        raise StructuredSourceError("writer target escapes the repository")
    probe = absolute_root
    parts = relative.split("/")
    for index, part in enumerate(parts):
        probe = os.path.join(probe, part)
        if not os.path.lexists(probe):
            continue
        if os.path.islink(probe):
            raise StructuredSourceError(
                "writer target has a symlink component: %s" % relative)
        if index < len(parts) - 1 and not os.path.isdir(probe):
            raise StructuredSourceError(
                "writer target ancestor is not a directory: %s" % relative)
    real_target = os.path.realpath(target)
    try:
        contained = os.path.commonpath((real_root, real_target)) == real_root
    except ValueError:
        contained = False
    if not contained:
        raise StructuredSourceError("writer target realpath escapes the repository")
    return target


_DIRECTORY_FLAGS = (os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) |
                    getattr(os, "O_NOFOLLOW", 0))
_FILE_READ_FLAGS = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
_FILE_CREATE_FLAGS = (os.O_CREAT | os.O_EXCL | os.O_WRONLY |
                      getattr(os, "O_NOFOLLOW", 0))


def _open_root(root: str) -> tuple[int, tuple[int, int]]:
    descriptor = None
    try:
        descriptor = os.open(root, _DIRECTORY_FLAGS)
        opened = os.fstat(descriptor)
        current = os.stat(root, follow_symlinks=False)
        if not stat.S_ISDIR(opened.st_mode) or \
                (opened.st_dev, opened.st_ino) != \
                (current.st_dev, current.st_ino):
            raise StructuredSourceError("writer root identity changed")
        return descriptor, (opened.st_dev, opened.st_ino)
    except BaseException:
        if descriptor is not None:
            os.close(descriptor)
        raise


def _assert_root_identity(root: str, identity: tuple[int, int]):
    try:
        current = os.stat(root, follow_symlinks=False)
    except OSError as exc:
        raise StructuredSourceError("writer root identity changed") from exc
    if not stat.S_ISDIR(current.st_mode) or \
            (current.st_dev, current.st_ino) != identity:
        raise StructuredSourceError("writer root identity changed")


def _open_parent_at(root_descriptor: int, relative: str, create: bool,
                    created_directories: set[str] | None = None):
    parts = relative.split("/")
    descriptor = os.dup(root_descriptor)
    prefix = []
    try:
        for part in parts[:-1]:
            prefix.append(part)
            try:
                child = os.open(part, _DIRECTORY_FLAGS, dir_fd=descriptor)
            except FileNotFoundError:
                if not create:
                    os.close(descriptor)
                    return None, parts[-1]
                try:
                    os.mkdir(part, 0o755, dir_fd=descriptor)
                    if created_directories is not None:
                        created_directories.add("/".join(prefix))
                except FileExistsError:
                    pass
                try:
                    child = os.open(part, _DIRECTORY_FLAGS,
                                    dir_fd=descriptor)
                except OSError as exc:
                    raise StructuredSourceError(
                        "writer target ancestor is a symlink or non-directory: %s" %
                        relative) from exc
            except OSError as exc:
                raise StructuredSourceError(
                    "writer target ancestor is a symlink or non-directory: %s" %
                    relative) from exc
            opened = os.fstat(child)
            if not stat.S_ISDIR(opened.st_mode):
                os.close(child)
                raise StructuredSourceError(
                    "writer target ancestor is not a directory: %s" % relative)
            os.close(descriptor)
            descriptor = child
        return descriptor, parts[-1]
    except BaseException:
        try:
            os.close(descriptor)
        except OSError:
            pass
        raise


def _entry_bytes(parent_descriptor: int, name: str, relative: str):
    descriptor = None
    try:
        descriptor = os.open(name, _FILE_READ_FLAGS,
                             dir_fd=parent_descriptor)
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise StructuredSourceError(
            "writer target is not a regular file: %s" % relative) from exc
    try:
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode):
            raise StructuredSourceError(
                "writer target is not a regular file: %s" % relative)
        chunks = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                return b"".join(chunks)
            chunks.append(chunk)
    finally:
        os.close(descriptor)


def _stage_file_at(parent_descriptor: int, prefix: str, data: bytes) -> str:
    descriptor = None
    temporary = None
    try:
        for unused_attempt in range(128):
            temporary = prefix + secrets.token_hex(12)
            try:
                descriptor = os.open(
                    temporary, _FILE_CREATE_FLAGS, 0o600,
                    dir_fd=parent_descriptor)
                break
            except FileExistsError:
                temporary = None
        if descriptor is None or temporary is None:
            raise StructuredSourceError(
                "writer could not allocate a unique staged output")
        os.fchmod(descriptor, 0o644)
        handle = os.fdopen(descriptor, "wb")
        descriptor = None
        with handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        return temporary
    except BaseException:
        if descriptor is not None:
            try:
                os.close(descriptor)
            except OSError:
                pass
        if temporary is not None:
            try:
                os.unlink(temporary, dir_fd=parent_descriptor)
            except FileNotFoundError:
                pass
        raise


def publish_set_locked(root: str, outputs: dict[str, bytes | None],
                       expected: dict[str, bytes | None],
                       guards: dict[str, bytes] | None = None,
                       postcondition=None):
    """Publish while the caller owns :func:`command_lock` for ``root``.

    ``expected`` is the exact pre-command state for every owned path.  A
    mismatch is external mutation and prevents the first write.  A ``None``
    output deletes the corresponding regular file.  ``guards`` are exact
    read-only prestates checked before and throughout publication.
    """
    guards = {} if guards is None else guards
    if not outputs or set(outputs) != set(expected) or \
            not isinstance(guards, dict) or set(outputs) & set(guards) or \
            (postcondition is not None and not callable(postcondition)) or \
            not all(data is None or isinstance(data, bytes)
                    for data in outputs.values()) or \
            not all(data is None or isinstance(data, bytes)
                    for data in expected.values()) or \
            not all(isinstance(data, bytes) for data in guards.values()) or \
            any(outputs[path] is None and expected[path] is None
                for path in outputs):
        raise StructuredSourceError("atomic output/expectation set is malformed")
    root, unused_real_root = _safe_root(root)
    targets = set(outputs) | set(guards)
    for path in targets:
        _safe_target(root, path)
    root_descriptor, root_identity = _open_root(root)

    def current_bytes(relative):
        _assert_root_identity(root, root_identity)
        _safe_target(root, relative)
        parent, name = _open_parent_at(root_descriptor, relative, False)
        if parent is None:
            return None
        try:
            return _entry_bytes(parent, name, relative)
        finally:
            os.close(parent)

    def audit(replaced):
        for relative in targets:
            if relative in guards:
                required = guards[relative]
            else:
                required = (outputs[relative] if relative in replaced else
                            expected[relative])
            if current_bytes(relative) != required:
                raise StructuredSourceError(
                    "writer target changed during publication: %s" % relative)

    temporaries = {}
    replaced = []
    created_directories = set()
    operation_directories = []

    def replaced_paths():
        return {relative for relative, unused_parent, unused_name in replaced}

    try:
        for relative in targets:
            required = guards.get(relative, expected.get(relative))
            if current_bytes(relative) != required:
                raise StructuredSourceError(
                    "writer target changed before publication: %s" % relative)
        for relative in outputs:
            if outputs[relative] is None:
                continue
            _safe_target(root, relative)
            parent, unused_name = _open_parent_at(
                root_descriptor, relative, True, created_directories)
            try:
                temporary = _stage_file_at(
                    parent, ".ssp-publish-", outputs[relative])
            except BaseException:
                os.close(parent)
                raise
            temporaries[relative] = (parent, temporary)
        for relative in sorted(outputs):
            audit(replaced_paths())
            parent, name = _open_parent_at(
                root_descriptor, relative, outputs[relative] is not None,
                created_directories)
            if parent is None:
                raise StructuredSourceError(
                    "writer target parent disappeared during publication: %s" %
                    relative)
            operation_directories.append(parent)
            if outputs[relative] is None:
                try:
                    os.unlink(name, dir_fd=parent)
                except FileNotFoundError:
                    pass
            else:
                temporary_parent, temporary = temporaries[relative]
                os.replace(
                    temporary, name, src_dir_fd=temporary_parent,
                    dst_dir_fd=parent)
                os.close(temporary_parent)
                del temporaries[relative]
            replaced.append((relative, parent, name))
        audit(replaced_paths())
        if postcondition is not None:
            postcondition()
            audit(replaced_paths())
        seen_directories = set()
        for descriptor in operation_directories:
            identity = os.fstat(descriptor)
            key = (identity.st_dev, identity.st_ino)
            if key not in seen_directories:
                os.fsync(descriptor)
                seen_directories.add(key)
        if postcondition is not None:
            postcondition()
            audit(replaced_paths())
    except BaseException as original:
        for parent, temporary in temporaries.values():
            try:
                os.unlink(temporary, dir_fd=parent)
            except FileNotFoundError:
                pass
            os.close(parent)
        incomplete = []
        for relative, parent, name in reversed(replaced):
            before = expected[relative]
            try:
                current = _entry_bytes(parent, name, relative)
            except StructuredSourceError:
                incomplete.append(relative)
                continue
            if current != outputs[relative]:
                incomplete.append(relative)
                continue
            if before is None:
                try:
                    os.unlink(name, dir_fd=parent)
                except FileNotFoundError:
                    pass
            else:
                rollback_temporary = None
                try:
                    rollback_temporary = _stage_file_at(
                        parent, ".ssp-rollback-", before)
                    os.replace(
                        rollback_temporary, name, src_dir_fd=parent,
                        dst_dir_fd=parent)
                except BaseException:
                    try:
                        if rollback_temporary is not None:
                            os.unlink(rollback_temporary, dir_fd=parent)
                    except FileNotFoundError:
                        pass
                    incomplete.append(relative)
                    continue
        seen_directories = set()
        for descriptor in operation_directories:
            try:
                identity = os.fstat(descriptor)
                key = (identity.st_dev, identity.st_ino)
                if key not in seen_directories:
                    os.fsync(descriptor)
                    seen_directories.add(key)
            except OSError:
                pass
        for directory in sorted(created_directories,
                                key=lambda item: item.count("/"), reverse=True):
            parent = None
            try:
                parent, name = _open_parent_at(
                    root_descriptor, directory, False)
                if parent is not None:
                    os.rmdir(name, dir_fd=parent)
            except OSError:
                pass
            finally:
                if parent is not None:
                    os.close(parent)
        if incomplete:
            raise StructuredSourceError(
                "external mutation prevented complete attributable rollback: %s" %
                sorted(incomplete)) from original
        raise
    finally:
        for descriptor in operation_directories:
            try:
                os.close(descriptor)
            except OSError:
                pass
        os.close(root_descriptor)


def publish_set(root: str, outputs: dict[str, bytes | None],
                expected: dict[str, bytes | None],
                guards: dict[str, bytes] | None = None,
                postcondition=None):
    """Acquire the writer lock and publish one validated atomic set."""
    with command_lock(root):
        return publish_set_locked(
            root, outputs, expected, guards, postcondition)
