"""Closed-format and path-safety tests for split corpus registries."""

import copy
import json
import os
import sys
import tempfile
import unittest
from types import SimpleNamespace


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "navigator"))

from lib import canon, gateway, model, registry  # noqa: E402


def authoritative_registry():
    return {
        "registryVersion": "1",
        "corpora": {
            "authority": {
                "role": "authoritative",
                "visibility": "internal",
                "version": "v1",
                "primary": "sources/authority.pdf",
                "files": {
                    "sources/authority.pdf": canon.bytes_digest(b"source"),
                },
            },
        },
    }


class TestRegistryStructure(unittest.TestCase):
    def load(self, data, **kwargs):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        path = os.path.join(temporary.name, "registry.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh)
        return registry.Registry(
            gateway.ContentGateway(temporary.name),
            registry_path="registry.json", **kwargs)

    def assert_rejected(self, mutate, message):
        value = authoritative_registry()
        mutate(value)
        with self.assertRaisesRegex(registry.RegistryError, message):
            self.load(value)

    def test_valid_registry_is_accepted(self):
        loaded = self.load(
            authoritative_registry(), allowed_corpora={"authority"},
            require_exact=True)
        self.assertEqual(set(loaded.corpora), {"authority"})

    def test_top_level_shape_and_version_are_closed(self):
        self.assert_rejected(
            lambda value: value.update({"extra": True}), "fields")
        self.assert_rejected(
            lambda value: value.update({"registryVersion": "2"}),
            "registryVersion")
        self.assert_rejected(
            lambda value: value.update({"corpora": {}}), "empty")

    def test_entry_fields_and_required_values_are_closed(self):
        self.assert_rejected(
            lambda value: value["corpora"]["authority"].update(
                {"extra": True}), "fields")
        self.assert_rejected(
            lambda value: value["corpora"]["authority"].update(
                {"version": ""}), "empty version")
        self.assert_rejected(
            lambda value: value["corpora"]["authority"].update(
                {"files": {}}), "no pinned files")
        self.assert_rejected(
            lambda value: value["corpora"]["authority"].update(
                {"primary": "sources/other.pdf"}), "not pinned")

    def test_pins_and_paths_must_be_canonical(self):
        self.assert_rejected(
            lambda value: value["corpora"]["authority"]["files"].update(
                {"sources/authority.pdf": "sha256/c1:" + "A" * 64}),
            "non-canonical digest")

        def unsafe_file(value):
            entry = value["corpora"]["authority"]
            digest = entry["files"].pop("sources/authority.pdf")
            entry["files"]["../authority.pdf"] = digest
            entry["primary"] = "../authority.pdf"

        self.assert_rejected(unsafe_file, "repository-relative path")

        def unsafe_profile(value):
            entry = value["corpora"]["authority"]
            entry["role"] = "derivative"
            entry["visibility"] = "rendered"
            entry["profile"] = "profiles/../profile.json"

        self.assert_rejected(unsafe_profile, "repository-relative path")

    def test_role_visibility_and_profile_contracts_are_enforced(self):
        self.assert_rejected(
            lambda value: value["corpora"]["authority"].update(
                {"visibility": "rendered"}), "requires visibility")

        def missing_profile(value):
            entry = value["corpora"]["authority"]
            entry["role"] = "derivative"
            entry["visibility"] = "rendered"

        self.assert_rejected(missing_profile, "fields")

        def forbidden_profile(value):
            entry = value["corpora"]["authority"]
            entry["role"] = "qa-source"
            entry["profile"] = "profiles/qa.json"

        self.assert_rejected(forbidden_profile, "fields")

    def test_merged_and_allowed_corpus_sets_are_exact(self):
        with self.assertRaisesRegex(registry.RegistryError, "not exact"):
            self.load(
                authoritative_registry(),
                allowed_corpora={"authority", "missing"},
                require_exact=True)

        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        data = authoritative_registry()
        for name in ("one.json", "two.json"):
            with open(os.path.join(temporary.name, name), "w",
                      encoding="utf-8") as fh:
                json.dump(copy.deepcopy(data), fh)
        with self.assertRaisesRegex(registry.RegistryError, "duplicate"):
            registry.Registry(
                gateway.ContentGateway(temporary.name),
                registry_paths=("one.json", "two.json"))

    def test_registry_paths_must_also_be_canonical(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        os.makedirs(os.path.join(temporary.name, "registries"))
        with open(os.path.join(temporary.name, "registries", "one.json"),
                  "w", encoding="utf-8") as fh:
            json.dump(authoritative_registry(), fh)
        with self.assertRaisesRegex(registry.RegistryError,
                                    "repository-relative path"):
            registry.Registry(
                gateway.ContentGateway(temporary.name),
                registry_path="registries/../registries/one.json")

    def test_lazy_qa_registry_cannot_duplicate_artifact_corpus_id(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        qa = authoritative_registry()
        entry = qa["corpora"]["authority"]
        entry["role"] = "qa-source"
        with open(os.path.join(temporary.name, "qa.json"), "w",
                  encoding="utf-8") as fh:
            json.dump(qa, fh)
        fake = SimpleNamespace(
            _qa_registry=None,
            edition={
                "qaSources": {"priorityMap": "authority"},
                "qaRegistry": "qa.json",
            },
            registry=SimpleNamespace(corpora={"authority": {}}),
            gw=SimpleNamespace(root=temporary.name),
        )
        with self.assertRaisesRegex(model.ModelError, "duplicate corpus"):
            model.EditionModel.qa_registry(fake)


if __name__ == "__main__":
    unittest.main()
