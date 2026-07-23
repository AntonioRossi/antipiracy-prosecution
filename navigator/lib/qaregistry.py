"""Closed registry for verification-only QA corpora.

QA registries are intentionally distinct from artifact corpus registries.
Every corpus carries a structured strategy-to-current-version binding, so a
free-form or obsolete label cannot masquerade as a current QA source.
"""

import posixpath
import re

from . import canon


class QaRegistryError(RuntimeError):
    pass


_ENTRY_FIELDS = frozenset((
    "role", "visibility", "versionBindings", "files", "primary",
))
_STRATEGY = re.compile(r"[A-Z][A-Z0-9]*\Z")
_VERSION = re.compile(
    r"(?P<strategy>[A-Z][A-Z0-9]*)-[0-9]{4}-[0-9]{2}-[0-9]{2}-v[1-9][0-9]*\Z")


def _safe_path(value, label):
    if not isinstance(value, str) or not value or "\\" in value or \
            any(ord(character) < 0x20 for character in value) or \
            value.startswith("/") or posixpath.normpath(value) != value or \
            value in (".", "..") or value.startswith("../") or \
            any(not part or part in (".", "..")
                for part in value.split("/")) or \
            value.split("/", 1)[0].endswith(":"):
        raise QaRegistryError(
            "%s must be a canonical repository-relative path" % label)
    return value


def _validate_version_bindings(value, label):
    if not isinstance(value, dict) or not value:
        raise QaRegistryError("%s has no structured version bindings" % label)
    keys = list(value)
    if keys != sorted(keys) or len(keys) != len(set(keys)):
        raise QaRegistryError("%s version bindings are not sorted and unique" % label)
    for strategy, version in value.items():
        match = _VERSION.fullmatch(version) if isinstance(version, str) else None
        if _STRATEGY.fullmatch(strategy) is None or match is None or \
                match.group("strategy") != strategy:
            raise QaRegistryError(
                "%s version binding %r is malformed" % (label, strategy))


def _validate_corpus(corpus_id, entry):
    if not isinstance(corpus_id, str) or not corpus_id:
        raise QaRegistryError("QA corpus id must be a non-empty string")
    if not isinstance(entry, dict) or set(entry) != _ENTRY_FIELDS:
        raise QaRegistryError("QA corpus %r has the wrong fields" % corpus_id)
    if entry.get("role") != "qa-source" or \
            entry.get("visibility") != "internal":
        raise QaRegistryError(
            "QA corpus %r must be an internal qa-source" % corpus_id)
    _validate_version_bindings(
        entry.get("versionBindings"), "QA corpus %r" % corpus_id)
    files = entry.get("files")
    if not isinstance(files, dict) or not files:
        raise QaRegistryError("QA corpus %r has no pinned files" % corpus_id)
    paths = list(files)
    if paths != sorted(paths) or len(paths) != len(set(paths)):
        raise QaRegistryError(
            "QA corpus %r file pins are not sorted and unique" % corpus_id)
    for path, digest in files.items():
        _safe_path(path, "QA corpus %r file" % corpus_id)
        try:
            canon.parse_digest(digest)
        except (canon.CanonError, TypeError, ValueError) as exc:
            raise QaRegistryError(
                "QA corpus %r file %r has a non-canonical digest: %s" %
                (corpus_id, path, exc))
    primary = _safe_path(
        entry.get("primary"), "QA corpus %r primary" % corpus_id)
    if primary not in files:
        raise QaRegistryError(
            "QA corpus %r primary %r is not pinned" % (corpus_id, primary))


class QaRegistry:
    def __init__(self, content_gateway, registry_path, allowed_corpora):
        self.gw = content_gateway
        self.registry_path = _safe_path(registry_path, "QA registry path")
        self.allowed = set(allowed_corpora)
        data = canon.parse_json(self.gw.read_text(self.registry_path))
        if not isinstance(data, dict) or set(data) != {
                "qaRegistryVersion", "corpora"} or \
                data.get("qaRegistryVersion") != "1":
            raise QaRegistryError(
                "QA registry shape/version is not current")
        corpora = data.get("corpora")
        if not isinstance(corpora, dict) or not corpora:
            raise QaRegistryError("QA registry has no corpora")
        if list(corpora) != sorted(corpora) or set(corpora) != self.allowed:
            raise QaRegistryError(
                "QA registry corpus set is not the exact declared set")
        for corpus_id, entry in corpora.items():
            _validate_corpus(corpus_id, entry)
        self.corpora = corpora

    def entry(self, corpus_id):
        if corpus_id not in self.allowed:
            raise QaRegistryError(
                "QA corpus %r is not declared by this edition" % corpus_id)
        try:
            return self.corpora[corpus_id]
        except KeyError:
            raise QaRegistryError("unregistered QA corpus %r" % corpus_id)

    def read_file(self, corpus_id, relpath):
        entry = self.entry(corpus_id)
        if relpath not in entry["files"]:
            raise QaRegistryError(
                "file %r is not pinned by QA corpus %r" %
                (relpath, corpus_id))
        data = self.gw.read_bytes(relpath)
        actual = canon.bytes_digest(data)
        if actual != entry["files"][relpath]:
            raise QaRegistryError(
                "QA corpus %r file %r drifted: pinned %s, actual %s" %
                (corpus_id, relpath, entry["files"][relpath], actual))
        return data
