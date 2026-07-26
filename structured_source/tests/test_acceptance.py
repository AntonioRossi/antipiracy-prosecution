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
        self.registries = acceptance.load_registries(ROOT)

    def test_registries_are_ordered_current_domain_criteria_data_only(self):
        self.assertEqual(
            tuple(registry["domain"] for registry in self.registries),
            tuple(contract["domain"] for contract in acceptance.CONTRACTS))
        self.assertEqual(
            tuple(entry["code"]
                  for registry in self.registries
                  for entry in registry["criteria"]),
            acceptance.CRITERIA)
        for contract, registry in zip(acceptance.CONTRACTS, self.registries):
            self.assertEqual(set(registry), {
                "acceptanceVersion", "authorityScheme", "criteria", "domain"})
            self.assertEqual(registry["acceptanceVersion"], "1")
            self.assertEqual(
                registry["authorityScheme"], contract["authorityScheme"])
            self.assertTrue(all(set(entry) == {
                "code", "evidence", "id", "outcome"}
                for entry in registry["criteria"]))

    def test_acceptance_tables_are_exact_domain_registry_projections(self):
        for contract, registry in zip(acceptance.CONTRACTS, self.registries):
            path = os.path.join(ROOT, contract["contractPath"])
            with self.subTest(domain=contract["domain"]), \
                    open(path, encoding="utf-8") as handle:
                text = handle.read()
            self.assertEqual(
                text.split(contract["tableStart"], 1)[1].split(
                    contract["tableEnd"], 1)[0],
                acceptance.render_table(registry))

    def test_contract_split_is_exact_and_consumer_product_agnostic(self):
        old_paths = (
            "AA11393US-structured-source-markdown_technical-description.md",
            "AA11393US-structured-source-markdown_acceptance-criteria.md",
            "structured_source/registry/acceptance.json",
        )
        self.assertTrue(all(not os.path.exists(os.path.join(ROOT, path))
                            for path in old_paths))
        paths = []
        for contract in acceptance.CONTRACTS:
            paths.extend((
                contract["contractPath"],
                contract["contractPath"].replace(
                    "_acceptance-criteria.md", "_technical-description.md"),
            ))
        self.assertEqual(len(paths), 6)
        for path in paths:
            with self.subTest(path=path), \
                    open(os.path.join(ROOT, path), encoding="utf-8") as handle:
                folded = handle.read().casefold()
            self.assertNotIn("navigator", folded)
            self.assertNotIn("html5", folded)
            self.assertNotIn(".html", folded)

    def test_runner_and_callback_metadata_fail_closed(self):
        registry = self.registries[0]
        domain = registry["domain"]
        for field, value in (("runner", {}), ("namespace", "ssp")):
            malformed = copy.deepcopy(registry)
            malformed[field] = value
            with self.subTest(field=field), self.assertRaises(
                    StructuredSourceError):
                acceptance.validate_registry(malformed, domain)
        malformed = copy.deepcopy(registry)
        malformed["criteria"][0]["callbacks"] = ["retired"]
        with self.assertRaises(StructuredSourceError):
            acceptance.validate_registry(malformed, domain)

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
                "criteria": len(acceptance.CRITERIA),
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
        self.assertEqual(
            [entry["domain"] for entry in result["domains"]],
            [contract["domain"] for contract in acceptance.CONTRACTS])
        self.assertTrue(all(entry["criteria"] == 6
                            for entry in result["domains"]))
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
                return_value=tuple(
                    {"criteria": [{}] * 6}
                    for unused_contract in acceptance.CONTRACTS)), \
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
