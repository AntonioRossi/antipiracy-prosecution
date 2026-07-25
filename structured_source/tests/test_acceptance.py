"""Executable acceptance ownership and table-projection tests."""

import copy
import json
import os
from types import SimpleNamespace
import unittest

from structured_source import acceptance
from structured_source import registry as content_registry
from structured_source.errors import StructuredSourceError
from structured_source.verify import VerificationContext, validate_command_policy


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class AcceptanceRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = acceptance.load_registry()

    def test_exact_recurring_census_and_namespaced_ownership(self):
        self.assertEqual(
            [item["code"] for item in self.registry["criteria"]],
            list(acceptance.CRITERIA))
        callbacks = [callback for item in self.registry["criteria"]
                     for callback in item["callbacks"]]
        self.assertEqual(len(callbacks), len(set(callbacks)))
        self.assertEqual(
            self.registry["runner"]["testModules"],
            list(acceptance.TEST_MODULES))

    def test_registry_rejects_shrunk_reassigned_or_unmapped_callbacks(self):
        shrunk = copy.deepcopy(self.registry)
        shrunk["criteria"].pop()
        with self.assertRaises(StructuredSourceError):
            acceptance.validate_registry(shrunk)
        reassigned = copy.deepcopy(self.registry)
        reassigned["criteria"][0]["callbacks"][0] = \
            "ssp.SSM-AC-02.stolen"
        with self.assertRaises(StructuredSourceError):
            acceptance.validate_registry(reassigned)
        unmapped = copy.deepcopy(self.registry)
        unmapped["criteria"][0]["callbacks"].append(
            "ssp.SSM-AC-01.undeclared")
        with self.assertRaises(StructuredSourceError):
            acceptance.validate_registry(unmapped)
        missing_test = copy.deepcopy(self.registry)
        missing_test["runner"]["testModules"].remove(
            "structured_source.tests.test_exporter")
        with self.assertRaises(StructuredSourceError):
            acceptance.validate_registry(missing_test)

    def test_operative_table_is_the_exact_registry_projection(self):
        path = os.path.join(
            ROOT,
            "AA11393US-structured-source-markdown_acceptance-criteria.md")
        with open(path, "r", encoding="utf-8") as handle:
            document = handle.read()
        start = "<!-- SSM-AC-TABLE:START -->\n"
        end = "<!-- SSM-AC-TABLE:END -->"
        projected = document.split(start, 1)[1].split(end, 1)[0]
        self.assertEqual(projected, acceptance.render_table(self.registry))

    def test_pdf_documents_have_one_explicit_source_manifest_owner(self):
        value = content_registry.load_registry()
        pdf_documents = [item for item in value["documents"]
                         if item["origin"] == "pdf-derivative"]
        self.assertEqual(len(pdf_documents), 37)
        self.assertEqual(
            len({item["sourceManifestFile"] for item in pdf_documents}), 37)
        broken = copy.deepcopy(value)
        next(item for item in broken["documents"]
             if item["origin"] == "pdf-derivative")["sourceManifestFile"] = None
        with self.assertRaises(StructuredSourceError):
            content_registry.validate_registry(broken)

    def test_command_capabilities_reject_widening(self):
        path = os.path.join(ROOT, "structured_source", "policy", "commands.json")
        with open(path, "r", encoding="utf-8") as handle:
            policy = json.load(handle)
        self.assertEqual(validate_command_policy(policy), policy)
        widened = copy.deepcopy(policy)
        widened["commands"][0]["writes"].append("source-xml")
        with self.assertRaises(StructuredSourceError):
            validate_command_policy(widened)

    def test_snapshot_inventory_is_authoritative_for_controlled_paths(self):
        context = VerificationContext.__new__(VerificationContext)
        context.root = ROOT
        context.byte_source = object()
        context.registry = {"taxonomy": {"controlledRoots": ["controlled"]}}
        context.repository_snapshot = SimpleNamespace(
            root=ROOT, digest="sha256/c1:" + "a" * 64,
            entries=(SimpleNamespace(path="controlled/frozen.txt"),))
        self.assertEqual(context._controlled_disk_paths(),
                         {"controlled/frozen.txt"})
        context.repository_snapshot = None
        with self.assertRaisesRegex(
                StructuredSourceError, "lacks its repository inventory"):
            context._controlled_disk_paths()


if __name__ == "__main__":
    unittest.main()
