"""Corpus registry accessor — typed access to registered corpora.

Every input is a registered corpus with a globally unique id, role,
visibility, and per-file SHA-256 pins (TDD §2, §8.1). All reads go through
the content gateway (read log -> content-input lock); a pin mismatch is a
hard error (source drift is never silent). Per-edition allowlists are
enforced by the gateway; this module additionally refuses corpus ids not
named by the edition config when one is bound.
"""

import json

from . import canon

ROLES = ("authoritative", "derivative", "fragment-source", "qa-source")
VISIBILITIES = ("rendered", "quotable", "internal")


class RegistryError(RuntimeError):
    pass


class Registry:
    def __init__(self, content_gateway, registry_path="navigator/corpora.json",
                 allowed_corpora=None):
        self.gw = content_gateway
        self.allowed = None if allowed_corpora is None else set(allowed_corpora)
        data = json.loads(self.gw.read_text(registry_path))
        self.corpora = data["corpora"]
        seen = set()
        for cid, entry in self.corpora.items():
            if cid in seen:
                raise RegistryError("duplicate corpus id %r" % cid)
            seen.add(cid)
            if entry["role"] not in ROLES:
                raise RegistryError("corpus %r: unknown role %r" % (cid, entry["role"]))
            if entry["visibility"] not in VISIBILITIES:
                raise RegistryError(
                    "corpus %r: unknown visibility %r" % (cid, entry["visibility"]))

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
        return json.loads(self.gw.read_text(entry["profile"]))

    def sibling_reader(self, corpus_id):
        """read_file(relpath) for files referenced relative to the corpus
        primary file's directory (figures) — pin-verified."""
        entry = self.entry(corpus_id)
        base = entry["primary"].rsplit("/", 1)[0]

        def read(rel):
            return self.read_file(corpus_id, base + "/" + rel)
        return read
