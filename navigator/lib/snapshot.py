"""Immutable repository manifests and hermetic workspace materialization."""

from dataclasses import dataclass, field
import os
import stat as statlib

from . import canon


EXCLUDED_DIRECTORY_NAMES = frozenset((
    ".git", ".uv-cache", ".venv", "__pycache__",
))


class SnapshotError(RuntimeError):
    pass


def _file_fingerprint(value):
    """Return identity and mutation-sensitive metadata for one file read."""
    return (
        value.st_dev,
        value.st_ino,
        statlib.S_IFMT(value.st_mode),
        value.st_mode & 0o777,
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
    )


@dataclass(frozen=True)
class SnapshotEntry:
    path: str
    digest: str
    mode: int
    size: int

    def as_record(self):
        return {
            "path": self.path,
            "digest": self.digest,
            "mode": self.mode,
            "size": self.size,
        }


@dataclass(frozen=True)
class RepositorySnapshot:
    root: str
    entries: tuple
    digest: str
    # Captured file bytes, present only when requested at capture time.  The
    # mapping is excluded from equality and representation: snapshot identity
    # is the entry set and its digest, not a second copy of every byte.
    retained_bytes: object = field(default=None, compare=False, repr=False)

    @classmethod
    def capture(cls, root, retain_bytes=False):
        root = os.path.abspath(root)
        entries = []
        identities = set()
        retained = {} if retain_bytes else None
        for directory, dirnames, filenames in os.walk(root, followlinks=False):
            kept = []
            for name in sorted(dirnames):
                path = os.path.join(directory, name)
                if name in EXCLUDED_DIRECTORY_NAMES:
                    continue
                rel = os.path.relpath(path, root).replace(os.sep, "/")
                if os.path.islink(path):
                    raise SnapshotError(
                        "repository snapshot contains symlink directory %s" % rel)
                if not os.path.isdir(path):
                    raise SnapshotError(
                        "repository snapshot contains non-directory %s" % rel)
                kept.append(name)
            dirnames[:] = kept
            for name in sorted(filenames):
                path = os.path.join(directory, name)
                rel = os.path.relpath(path, root).replace(os.sep, "/")
                before = os.stat(path, follow_symlinks=False)
                if not statlib.S_ISREG(before.st_mode):
                    raise SnapshotError(
                        "repository snapshot contains non-regular file %s" % rel)
                identity = rel.casefold()
                if identity in identities:
                    raise SnapshotError(
                        "repository snapshot contains duplicate path identity %s" % rel)
                identities.add(identity)
                with open(path, "rb") as handle:
                    opened = os.fstat(handle.fileno())
                    data = handle.read()
                    after_read = os.fstat(handle.fileno())
                after_path = os.stat(path, follow_symlinks=False)
                fingerprints = {
                    _file_fingerprint(value)
                    for value in (before, opened, after_read, after_path)
                }
                if len(fingerprints) != 1 or len(data) != after_read.st_size:
                    raise SnapshotError(
                        "repository file changed during snapshot capture %s" % rel)
                entries.append(SnapshotEntry(
                    rel, canon.bytes_digest(data), after_read.st_mode & 0o777,
                    len(data)))
                if retained is not None:
                    retained[rel] = data
        entries.sort(key=lambda entry: entry.path)
        records = [entry.as_record() for entry in entries]
        digest = canon.composite_digest(
            "aa11393:lock:c1", {"repositorySnapshot": records})
        return cls(root, tuple(entries), digest, retained)

    def by_path(self):
        return {entry.path: entry for entry in self.entries}

    def read_bytes(self, relpath):
        """Return the frozen bytes captured for *relpath*.

        Bytes come from the capture itself, never from a live re-read, so a
        tree change after capture can neither alter nor revoke what a
        consumer verifies.  A snapshot captured without byte retention has
        no byte source.
        """
        if self.retained_bytes is None:
            raise SnapshotError(
                "repository snapshot was captured without byte retention")
        data = self.retained_bytes.get(relpath)
        if data is None:
            raise SnapshotError(
                "path is absent from repository snapshot: %s" % relpath)
        return data

    def byte_source(self):
        """Return the immutable gateway byte source bound to this snapshot.

        Gateways hand their policy-resolved absolute paths to this callable
        instead of opening the live file, so every byte a planning or
        verification function consumes is exactly the captured byte.
        """
        root = self.root
        read_bytes = self.read_bytes

        def read(path):
            rel = os.path.relpath(os.path.abspath(path), root)
            return read_bytes(rel.replace(os.sep, "/"))

        return read

    def materialize(self, destination):
        """Copy the exact snapshot into an existing empty directory.

        Requires a snapshot captured with byte retention: the frozen bytes
        are the only bytes written, never a live re-read.
        """
        destination = os.path.abspath(destination)
        if not os.path.isdir(destination) or os.listdir(destination):
            raise SnapshotError(
                "snapshot destination must be an existing empty directory")
        for entry in self.entries:
            target = os.path.join(destination, *entry.path.split("/"))
            os.makedirs(os.path.dirname(target), exist_ok=True)
            data = self.read_bytes(entry.path)
            with open(target, "wb") as handle:
                handle.write(data)
            os.chmod(target, entry.mode)
        return destination

    def differences(self, other):
        if not isinstance(other, RepositorySnapshot):
            return ["comparison value is not a repository snapshot"]
        left = self.by_path()
        right = other.by_path()
        problems = []
        missing = sorted(set(left) - set(right))
        extra = sorted(set(right) - set(left))
        if missing:
            problems.append("repository paths removed during verification: %s" % missing)
        if extra:
            problems.append("repository paths added during verification: %s" % extra)
        for path in sorted(set(left) & set(right)):
            before = left[path]
            after = right[path]
            if (before.digest, before.mode, before.size) != (
                    after.digest, after.mode, after.size):
                problems.append(
                    "repository path changed during verification: %s" % path)
        if not problems and self.digest != other.digest:
            problems.append("repository snapshot digest changed without a path delta")
        return problems
