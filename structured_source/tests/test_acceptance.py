"""Focused recurring-acceptance and command-surface fixtures."""

import copy
import os
import tempfile
import unittest
from unittest import mock

from structured_source import acceptance
from structured_source.__main__ import _parser
from structured_source.acceptance_callbacks import CALLBACKS
from structured_source.control import canonical_json, parse_json
from structured_source.errors import StructuredSourceError
from structured_source.verify import COMMAND_CAPABILITIES, validate_command_policy
from structured_source.verify import VerificationContext
from structured_source.tests.test_registry import registry_fixture


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class AcceptanceContract(unittest.TestCase):
    def setUp(self):
        self.registry = acceptance.load_registry(ROOT)

    def test_ten_criteria_each_own_one_exact_callback(self):
        self.assertEqual(
            [entry["code"] for entry in self.registry["criteria"]],
            list(acceptance.CRITERIA))
        callbacks = [entry["callbacks"][0]
                     for entry in self.registry["criteria"]]
        self.assertEqual(len(callbacks), 10)
        self.assertEqual(set(callbacks), set(CALLBACKS))

    def test_acceptance_table_is_the_exact_registry_projection(self):
        path = os.path.join(
            ROOT, "AA11393US-structured-source-markdown_acceptance-criteria.md")
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        start = "<!-- SSM-AC-TABLE:START -->\n"
        end = "<!-- SSM-AC-TABLE:END -->"
        self.assertEqual(
            text.split(start, 1)[1].split(end, 1)[0],
            acceptance.render_table(self.registry))

    def test_every_registered_test_family_declares_current_criteria(self):
        runner = self.registry["runner"]
        self.assertIn(
            "structured_source.tests.test_conversion", runner["testModules"])
        self.assertNotIn(
            "structured_source.tests.test_projection", runner["testModules"])
        self.assertEqual(set(runner["testModules"]),
                         set(runner["testCriteria"]))
        self.assertTrue(all(runner["testCriteria"][module]
                            for module in runner["testModules"]))

    def test_missing_or_duplicate_callback_fails_closed(self):
        value = copy.deepcopy(self.registry)
        value["criteria"][0]["callbacks"] = []
        with self.assertRaisesRegex(StructuredSourceError, "exactly one"):
            acceptance.validate_registry(value)
        value = copy.deepcopy(self.registry)
        value["criteria"][1]["callbacks"] = \
            value["criteria"][0]["callbacks"]
        with self.assertRaises(StructuredSourceError):
            acceptance.validate_registry(value)

    def test_command_policy_and_cli_are_exact(self):
        path = os.path.join(ROOT, "structured_source", "policy", "commands.json")
        with open(path, "rb") as handle:
            data = handle.read()
        policy = validate_command_policy(parse_json(data))
        self.assertEqual(data, canonical_json(policy))
        self.assertEqual(
            {entry["id"] for entry in policy["commands"]},
            set(COMMAND_CAPABILITIES))
        actions = _parser()._subparsers._group_actions[0].choices
        self.assertEqual(set(actions), set(COMMAND_CAPABILITIES))
        self.assertTrue({"approve", "export", "migrate"}.isdisjoint(actions))

    def test_callbacks_reuse_one_context_result(self):
        class Context:
            def __init__(self):
                self.calls = []

            def evidence_for(self, code):
                self.calls.append(code)
                return {"criterion": code, "status": "conformant"}

        context = Context()
        for callback in CALLBACKS.values():
            callback(context)
        self.assertEqual(context.calls, list(acceptance.CRITERIA))

    def test_real_context_memoizes_one_corpus_pass_for_all_callbacks(self):
        context = VerificationContext(ROOT, registry=registry_fixture())
        package_results = {
            package_id: {
                "packageId": package_id,
                "authorityScheme": package["authorityScheme"],
                "status": "conformant",
                "computedCoverage": {"coveredItems": 1},
            }
            for package_id, package in context.packages.items()
        }
        with mock.patch.object(
                context, "_control_closure",
                return_value=(
                    {"criteria": [{}] * 10},
                    {"commands": [{}] * 5})), \
                mock.patch.object(
                    context, "check",
                    side_effect=lambda package_id: package_results[package_id]
                ) as check:
            for callback in CALLBACKS.values():
                callback(context)
        self.assertEqual(context._global_passes, 1)
        self.assertEqual(check.call_count, len(context.packages))

    def test_targeted_retired_import_scan_fails_closed(self):
        for statement in (
                b"from structured_source import approvals\n",
                b"from .approvals import resolve\n"):
            with self.subTest(statement=statement), \
                    tempfile.TemporaryDirectory() as root:
                path = os.path.join(root, "structured_source")
                os.makedirs(path)
                with open(os.path.join(path, "legacy.py"), "wb") as handle:
                    handle.write(statement)
                context = VerificationContext(root, registry=registry_fixture())
                with self.assertRaisesRegex(StructuredSourceError, "retired"):
                    context._reject_retired_imports({
                        "structured_source/legacy.py"})


if __name__ == "__main__":
    unittest.main()
