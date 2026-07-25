"""Focused data-only acceptance and command-surface fixtures."""

import copy
import os
import tempfile
import unittest
from unittest import mock

from structured_source import acceptance
from structured_source.__main__ import COMMANDS, _parser
from structured_source.errors import StructuredSourceError
from structured_source.verify import VerificationContext, run_acceptance
from structured_source.tests.test_registry import registry_fixture


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class AcceptanceContract(unittest.TestCase):
    def setUp(self):
        self.registry = acceptance.load_registry(ROOT)

    def test_registry_is_ordered_current_criteria_data_only(self):
        self.assertEqual(set(self.registry), {"acceptanceVersion", "criteria"})
        self.assertEqual(self.registry["acceptanceVersion"], "2")
        self.assertEqual(
            [entry["code"] for entry in self.registry["criteria"]],
            list(acceptance.CRITERIA))
        self.assertTrue(all(set(entry) == {
            "code", "evidence", "id", "outcome"}
            for entry in self.registry["criteria"]))

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

    def test_runner_and_callback_metadata_fail_closed(self):
        for field, value in (("runner", {}), ("namespace", "ssp")):
            malformed = copy.deepcopy(self.registry)
            malformed[field] = value
            with self.subTest(field=field), self.assertRaises(
                    StructuredSourceError):
                acceptance.validate_registry(malformed)
        malformed = copy.deepcopy(self.registry)
        malformed["criteria"][0]["callbacks"] = ["retired"]
        with self.assertRaises(StructuredSourceError):
            acceptance.validate_registry(malformed)

    def test_parser_is_the_exact_command_surface(self):
        actions = _parser()._subparsers._group_actions[0].choices
        self.assertEqual(tuple(actions), COMMANDS)
        self.assertEqual(
            COMMANDS,
            ("check", "regenerate", "regenerate-controls", "verify-current"))
        self.assertFalse(os.path.exists(os.path.join(
            ROOT, "structured_source", "policy", "commands.json")))

    def test_run_acceptance_uses_one_pass_and_emits_plain_statuses(self):
        snapshot = type("Snapshot", (), {"digest": "sha256:test"})()
        with mock.patch(
                "structured_source.verify.VerificationContext") as context_type:
            context = context_type.return_value
            context.verify_all.return_value = {
                "criteria": 10,
                "globalPasses": 1,
                "status": "conformant",
            }
            result = run_acceptance(ROOT, repository_snapshot=snapshot)
        context.verify_all.assert_called_once_with()
        self.assertEqual(result["repositorySnapshot"], "sha256:test")
        self.assertEqual(result["results"], [
            {"id": criterion, "status": "passed"}
            for criterion in acceptance.CRITERIA
        ])
        self.assertTrue(all(
            set(entry) == {"id", "status"} for entry in result["results"]))

    def test_real_global_pass_checks_each_package_once(self):
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
                return_value={"criteria": [{}] * 10}), \
                mock.patch.object(
                    context, "check",
                    side_effect=lambda package_id: package_results[package_id]
                ) as check:
            first = context.verify_all()
            second = context.verify_all()
        self.assertIs(first, second)
        self.assertEqual(first["globalPasses"], 1)
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
