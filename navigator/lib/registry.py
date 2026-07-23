"""Corpus registry accessor — typed access to registered corpora.

Every input is a registered corpus with a globally unique id, role,
visibility, and per-file SHA-256 pins (TDD §2, §8.1). All reads go through
the content gateway (read log -> content-input lock); a pin mismatch is a
hard error (source drift is never silent). Per-edition allowlists are
enforced by the gateway; this module additionally refuses corpus ids not
named by the edition config when one is bound.
"""

import posixpath

from . import canon

ROLES = ("authoritative", "derivative", "fragment-source", "qa-source")
VISIBILITIES = ("rendered", "quotable", "internal")
ROLE_VISIBILITY = {
    "authoritative": "internal",
    "derivative": "rendered",
    "fragment-source": "rendered",
    "qa-source": "internal",
}
BASE_ENTRY_FIELDS = frozenset((
    "role", "visibility", "version", "files", "primary",
))
PROFILE_ROLES = frozenset(("derivative", "fragment-source"))


class RegistryError(RuntimeError):
    pass


def _safe_registry_path(value, label):
    if not isinstance(value, str) or not value or "\\" in value or \
            any(ord(character) < 0x20 for character in value) or \
            value.startswith("/") or posixpath.normpath(value) != value or \
            value in (".", "..") or value.startswith("../") or \
            any(not part or part in (".", "..")
                for part in value.split("/")):
        raise RegistryError(
            "%s must be a canonical repository-relative path" % label)
    first = value.split("/", 1)[0]
    if first.endswith(":"):
        raise RegistryError(
            "%s must be a canonical repository-relative path" % label)
    return value


def _validate_corpus(cid, entry):
    if not isinstance(cid, str) or not cid:
        raise RegistryError("corpus id must be a non-empty string")
    if not isinstance(entry, dict):
        raise RegistryError("corpus %r is not an object" % cid)
    role = entry.get("role")
    if role not in ROLES:
        raise RegistryError("corpus %r: unknown role %r" % (cid, role))
    visibility = entry.get("visibility")
    if visibility not in VISIBILITIES:
        raise RegistryError(
            "corpus %r: unknown visibility %r" % (cid, visibility))
    if visibility != ROLE_VISIBILITY[role]:
        raise RegistryError(
            "corpus %r: role %r requires visibility %r"
            % (cid, role, ROLE_VISIBILITY[role]))
    expected_fields = set(BASE_ENTRY_FIELDS)
    if role in PROFILE_ROLES:
        expected_fields.add("profile")
    if set(entry) != expected_fields:
        raise RegistryError(
            "corpus %r fields must be exactly %r"
            % (cid, sorted(expected_fields)))
    if not isinstance(entry["version"], str) or not entry["version"].strip():
        raise RegistryError("corpus %r has an empty version" % cid)
    files = entry["files"]
    if not isinstance(files, dict) or not files:
        raise RegistryError("corpus %r has no pinned files" % cid)
    for path, digest in files.items():
        _safe_registry_path(path, "corpus %r file" % cid)
        try:
            canon.parse_digest(digest)
        except (TypeError, ValueError) as exc:
            raise RegistryError(
                "corpus %r file %r has a non-canonical digest: %s"
                % (cid, path, exc))
    primary = _safe_registry_path(
        entry["primary"], "corpus %r primary" % cid)
    if primary not in files:
        raise RegistryError(
            "corpus %r primary %r is not pinned" % (cid, primary))
    if role in PROFILE_ROLES:
        _safe_registry_path(entry["profile"], "corpus %r profile" % cid)


class Registry:
    def __init__(self, content_gateway, registry_path="navigator/corpora.json",
                 registry_paths=None, allowed_corpora=None,
                 require_exact=False):
        self.gw = content_gateway
        self.allowed = None if allowed_corpora is None else set(allowed_corpora)
        if registry_paths is None:
            registry_paths = (registry_path,)
        if not isinstance(registry_paths, (list, tuple)) or not registry_paths:
            raise RegistryError("registry paths must be a non-empty sequence")
        self.registry_paths = tuple(registry_paths)
        for path in self.registry_paths:
            _safe_registry_path(path, "registry path")
        self.corpora = {}
        seen = set()
        registry_version = None
        for path in self.registry_paths:
            data = canon.parse_json(self.gw.read_text(path))
            if not isinstance(data, dict) or \
                    set(data) != {"registryVersion", "corpora"}:
                raise RegistryError(
                    "registry %r fields must be exactly registryVersion and "
                    "corpora" % path)
            version = data["registryVersion"]
            if version != "1":
                raise RegistryError(
                    "registry %r has unsupported registryVersion %r"
                    % (path, version))
            if registry_version is None:
                registry_version = version
            elif version != registry_version:
                raise RegistryError(
                    "registry %r has version %r, expected %r"
                    % (path, version, registry_version))
            corpora = data.get("corpora")
            if not isinstance(corpora, dict) or not corpora:
                raise RegistryError(
                    "registry %r has an empty or invalid corpus map" % path)
            for cid, entry in corpora.items():
                if cid in seen:
                    raise RegistryError("duplicate corpus id %r" % cid)
                seen.add(cid)
                _validate_corpus(cid, entry)
                self.corpora[cid] = entry
        if require_exact and self.allowed is not None and \
                set(self.corpora) != self.allowed:
            missing = sorted(self.allowed - set(self.corpora))
            extra = sorted(set(self.corpora) - self.allowed)
            raise RegistryError(
                "registry corpus set is not exact (missing=%r, extra=%r)"
                % (missing, extra))

    def entry(self, corpus_id):
        if self.allowed is not None and corpus_id not in self.allowed:
            raise RegistryError(
                "corpus %r is not in this edition's declared corpus set" % corpus_id)
        try:
            return self.corpora[corpus_id]
        except KeyError:
            raise RegistryError("unregistered corpus id %r" % corpus_id)

    def read_file(self, corpus_id, relpath):
        """Read one pinned file of a corpus, verifying its digest pin."""
        entry = self.entry(corpus_id)
        pins = entry["files"]
        if relpath not in pins:
            raise RegistryError(
                "file %r is not pinned by corpus %r" % (relpath, corpus_id))
        data = self.gw.read_bytes(relpath)
        actual = canon.bytes_digest(data)
        if actual != pins[relpath]:
            raise RegistryError(
                "corpus %r file %r drifted: pinned %s, actual %s"
                % (corpus_id, relpath, pins[relpath], actual))
        return data

    def primary_text(self, corpus_id):
        entry = self.entry(corpus_id)
        return self.read_file(corpus_id, entry["primary"]).decode("utf-8")

    def profile(self, corpus_id):
        entry = self.entry(corpus_id)
        if "profile" not in entry:
            raise RegistryError("corpus %r has no segmentation profile" % corpus_id)
        return canon.parse_json(self.gw.read_text(entry["profile"]))

    def sibling_reader(self, corpus_id):
        """read_file(relpath) for files referenced relative to the corpus
        primary file's directory (figures) — pin-verified."""
        entry = self.entry(corpus_id)
        base = entry["primary"].rsplit("/", 1)[0]

        def read(rel):
            return self.read_file(corpus_id, base + "/" + rel)
        return read
