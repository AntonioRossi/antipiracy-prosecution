"""Focused regression tests for operator QA and release authorization."""

import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "navigator"))

import build  # noqa: E402
from lib import acceptance, authority, bundlezip, canon  # noqa: E402
from lib import control_inventory, currentstate, gateway  # noqa: E402
from lib import pinplan, profilepolicy  # noqa: E402
from lib import qaevidence, qaregistry  # noqa: E402
from lib import recordprovenance, release, render, snapshot  # noqa: E402
from tests import acceptance_support  # noqa: E402


MANUAL_FIELDS = ("ac11", "ac12", "ac13", "ac15")
TECHNICAL_PREVIEW_PROFILE = acceptance_support.TECHNICAL_PREVIEW_PROFILE
VALIDATED_RELEASE_PROFILE = acceptance_support.VALIDATED_RELEASE_PROFILE

with open(os.path.join(ROOT, "navigator", "schema", "support-matrix.json"),
          encoding="utf-8") as _support_fh:
    QA_SUPPORT_MATRIX = json.load(_support_fh)
with open(os.path.join(ROOT, "navigator", "schema", "api-policy.json"),
          encoding="utf-8") as _api_fh:
    QA_API_PROBES = sorted(render.api_probe_instruments(json.load(_api_fh)))


def _target_result(target, field):
    result = copy.deepcopy(target)
    browser_family = target["browser"].split(" ", 1)[0]
    browser_version = {
        "Chrome": "Chrome 150.0.1",
        "Edge": "Edge 150.0.1",
        "Firefox": "Firefox 147.0.1",
        "Safari": "Safari 26.5.2",
    }[browser_family]
    result.update({
        "browserVersion": browser_version,
        "osVersion": ("macOS 14.0" if target["os"].startswith("macOS")
                      else "Windows 11 23H2"),
        "atVersion": None if target["at"] == "none" else "NVDA 2024.4",
    })
    if field == "ac11":
        result.update({
            "traversalChord": "Tab/Shift-Tab",
            "traversalConfiguration":
                "Keyboard Navigation enabled for browser focus traversal",
            "checks": {
                "keyboardTraversal": "passed",
                "activationKeys": "passed",
                "focusDeterminism": "passed",
                "scopedArrowKeys": "passed",
                "computedNameRoleState": "passed",
                "liveRegion": "passed",
            },
        })
    else:
        result.update({
            "minimumViewport": copy.deepcopy(
                QA_SUPPORT_MATRIX["viewport"]["minimum"]),
            "stackedViewport": [1024, 700],
            "checks": {
                "localFile": "passed",
                "minimumViewport": "passed",
                "stackedBelowMinimum": "passed",
            },
        })
    return result


def _manual_checks(operator="QA Reviewer", operator_kind="human"):
    common = {
        "status": "passed",
        "evidence": "Completed against the exact candidate bytes",
        "operator": operator,
        "operatorKind": operator_kind,
    }
    installed = {"status": "installed", "error": None, "detail": None}
    return {
        "ac11": dict(common, targetResults=[
            _target_result(target, "ac11")
            for target in QA_SUPPORT_MATRIX["targets"]
        ]),
        "ac12": dict(common, printResult={
            "browser": "Safari", "browserVersion": "Safari 26.5.2",
            "os": "macOS", "osVersion": "macOS 26.5.2",
            "pageCount": 4,
            "checks": {
                "claimsReadable": "passed",
                "disclosureReadable": "passed",
                "disclaimerOnEveryPage": "passed",
                "legendOnEveryPage": "passed",
                "provenancePresent": "passed",
                "schedulePresent": "passed",
                "noContentClipping": "passed",
            },
        }),
        "ac13": dict(common, targetResults=[
            _target_result(target, "ac13")
            for target in QA_SUPPORT_MATRIX["targets"]
        ]),
        "ac15": dict(common, probeResult={
            "browser": "Safari", "browserVersion": "Safari 26.5.2",
            "os": "macOS", "osVersion": "macOS 26.5.2", "ready": True,
            "apis": {api: dict(installed) for api in QA_API_PROBES},
            "attempts": [], "resources": [], "cookieWrites": [],
            "webStorage": [], "indexedDB": [], "navigationMutations": [],
            "networkRequests": [],
        }),
    }


def _receipt_context(profile=VALIDATED_RELEASE_PROFILE):
    return acceptance_support.context(profile)


def _release_receipt(context, subjects):
    return acceptance_support.receipt("release", subjects, context)


class TestAuthorizedOperator(unittest.TestCase):
    def test_identity_shape_is_independent_from_evidence_language(self):
        identity = "codex:model:failed-over-run"
        self.assertTrue(authority.is_identified_operator_identity(identity))
        self.assertTrue(authority.is_authoritative_operator(
            "model", identity))
        self.assertFalse(authority.is_final_evidence_text(identity))

    def test_operator_has_no_implicit_default(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(SystemExit, "NAV_OPERATOR"):
                build.operator_id()

    def test_operator_kind_and_identity_are_both_explicit(self):
        identities = {
            "human": "reviewer@example.test",
            "model": "codex:gpt-5.6-sol:run-test-001",
        }
        for kind, identity in identities.items():
            with self.subTest(kind=kind), mock.patch.dict(os.environ, {
                    "NAV_OPERATOR": identity,
                    "NAV_OPERATOR_KIND": kind,
            }, clear=True):
                self.assertEqual(build.operator_id(), (identity, kind))

        for kind in ("tool", "automation", "", "HUMAN"):
            with self.subTest(kind=kind), mock.patch.dict(os.environ, {
                    "NAV_OPERATOR": "identified-run",
                    "NAV_OPERATOR_KIND": kind,
            }, clear=True):
                with self.assertRaisesRegex(
                        SystemExit, "human.*model|release-authoritative"):
                    build.operator_id()

        for identity in (
                "", "   ", "\u200b", "\u2060", "\u200e",
                "\u200b\u2060\u200e", "\u200bidentified-run",
                "identified-run\u2060", " identified-run",
                "identified-run ", "re\u0301viewer"):
            with self.subTest(identity=identity), mock.patch.dict(
                    os.environ, {
                        "NAV_OPERATOR": identity,
                        "NAV_OPERATOR_KIND": "model",
                    }, clear=True):
                with self.assertRaisesRegex(SystemExit, "NAV_OPERATOR"):
                    build.operator_id()

        mixed = "codex:gpt-5.6-sol:run-visible QA-42"
        with mock.patch.dict(os.environ, {
                "NAV_OPERATOR": mixed,
                "NAV_OPERATOR_KIND": "model",
        }, clear=True):
            self.assertEqual(build.operator_id(), (mixed, "model"))


class TestCliArity(unittest.TestCase):
    def test_missing_edition_is_a_usage_error(self):
        with self.assertRaisesRegex(SystemExit,
                                    "usage: build.py release <edition>"):
            build.main(["release"])

    def test_extra_arguments_are_rejected(self):
        with self.assertRaisesRegex(SystemExit, "usage: build.py bundle"):
            build.main(["bundle", "unexpected"])
        with self.assertRaisesRegex(SystemExit,
                                    "usage: build.py bundle-plan"):
            build.main(["bundle-plan", "unexpected"])
        with self.assertRaisesRegex(SystemExit,
                                    "usage: build.py candidate <edition>"):
            build.main(["candidate", "na", "unexpected"])

    def test_record_qa_missing_edition_uses_current_usage(self):
        with self.assertRaisesRegex(SystemExit, "--evidence-file"):
            build.main(["record-qa"])

    def test_release_profile_is_explicit_and_closed(self):
        for argv in ([], ["--profile="], ["--profile=UPPER"],
                     ["--profile=bad/profile"],
                     ["--profile=technical-preview", "unexpected"]):
            with self.subTest(argv=argv), self.assertRaises(SystemExit):
                build._release_profile_arg(argv)
        self.assertEqual(build._release_profile_arg(
            ["--profile=technical-preview"]), "technical-preview")
        self.assertEqual(build._release_profile_arg(
            ["--profile=validated-release"]), "validated-release")
        self.assertEqual(build._release_profile_arg(
            ["--profile=future-profile"]), "future-profile")
        with self.assertRaisesRegex(SystemExit, "--profile="):
            build.main(["release", "na"])


class TestAcceptanceReceipts(unittest.TestCase):
    def setUp(self):
        self.context = _receipt_context()
        self.subjects = acceptance.release_subjects(
            "na", canon.bytes_digest(b"candidate"),
            canon.bytes_digest(b"content lock"),
            canon.bytes_digest(b"qa record"),
            canon.bytes_digest(b"qa input lock"),
            VALIDATED_RELEASE_PROFILE)
        self.receipt = _release_receipt(self.context, self.subjects)

    def problems(self, receipt=None, context=None, subjects=None):
        return acceptance.acceptance_receipt_problems(
            self.receipt if receipt is None else receipt, "release",
            self.context if context is None else context,
            self.subjects if subjects is None else subjects)

    def test_receipt_binds_registry_runner_phases_and_all_release_subjects(self):
        self.assertEqual(self.problems(), [])
        mutations = (
            ("registryDigest", canon.bytes_digest(b"other registry")),
            ("policyDigest", canon.bytes_digest(b"other policy")),
            ("runnerDigest", canon.bytes_digest(b"other runner")),
            ("runnerEditions", ["af"]),
            ("runnerKind", "human"),
            ("releaseProfile", "technical-preview"),
            ("releaseProfileContract", TECHNICAL_PREVIEW_PROFILE),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                changed = copy.deepcopy(self.receipt)
                changed[field] = value
                self.assertTrue(self.problems(changed))
        changed = copy.deepcopy(self.receipt)
        changed["results"].pop(0)
        self.assertTrue(any("atomic result" in problem
                            for problem in self.problems(changed)))
        for field in self.subjects:
            with self.subTest(subject=field):
                changed = copy.deepcopy(self.receipt)
                changed["subjects"][field] = (
                    "different" if field == "edition"
                    else canon.bytes_digest(("other " + field).encode()))
                self.assertTrue(any("subjects" in problem
                                    for problem in self.problems(changed)))
        af_context = copy.deepcopy(self.context)
        af_context["runnerEditions"] = ["af"]
        af_context["runnerDigest"] = acceptance.runner_digest(
            af_context["registryDigest"], af_context["policyDigest"],
            af_context["runnerInputs"], af_context["controlPlan"],
            af_context["runnerEditions"],
            af_context["releaseProfile"],
            af_context["releaseProfileContract"])
        af_subjects = copy.deepcopy(self.subjects)
        af_subjects["edition"] = "af"
        af_receipt = _release_receipt(af_context, af_subjects)
        af_receipt["subjects"]["edition"] = "na"
        self.assertTrue(any(
            "receipt edition does not match" in problem
            for problem in self.problems(
                af_receipt, af_context, af_subjects)))

    def test_receipt_fails_closed_on_missing_context_and_malformed_subjects(self):
        self.assertTrue(any("context" in problem
                            for problem in self.problems(context={})))
        malformed_expected = copy.deepcopy(self.subjects)
        malformed_expected["qaInputLockDigest"] = None
        problems = self.problems(subjects=malformed_expected)
        self.assertTrue(any("qaInputLockDigest" in problem
                            for problem in problems), problems)
        malformed_receipt = copy.deepcopy(self.receipt)
        malformed_receipt["subjects"]["candidateDigest"] = "not-a-digest"
        self.assertTrue(any("candidateDigest" in problem
                            for problem in self.problems(malformed_receipt)))

    def test_preview_receipt_has_explicit_deferred_profile_and_no_qa_subject(self):
        context = _receipt_context(TECHNICAL_PREVIEW_PROFILE)
        subjects = acceptance.release_subjects(
            "na", canon.bytes_digest(b"candidate"),
            canon.bytes_digest(b"content lock"), None, None,
            TECHNICAL_PREVIEW_PROFILE)
        receipt = _release_receipt(context, subjects)
        self.assertEqual(acceptance.acceptance_receipt_problems(
            receipt, "release", context, subjects), [])
        self.assertEqual(receipt["receiptVersion"], "3")
        self.assertEqual(receipt["releaseProfile"], "technical-preview")
        self.assertEqual(receipt["releaseProfileContract"],
                         TECHNICAL_PREVIEW_PROFILE)
        self.assertIsNone(receipt["subjects"]["qaRecord"])
        self.assertIsNone(receipt["subjects"]["qaInputLockDigest"])
        self.assertEqual(receipt["subjects"]["compatibilityAuthorization"],
                         "not-authorized")
        self.assertEqual(receipt["subjects"]["deferredControls"],
                         TECHNICAL_PREVIEW_PROFILE["deferredControls"])
        deferred = [result["control"] for result in receipt["results"]
                    if result["status"] == "deferred"]
        self.assertEqual(deferred,
                         TECHNICAL_PREVIEW_PROFILE["deferredControls"])

        claimed = copy.deepcopy(subjects)
        claimed["qaRecord"] = canon.bytes_digest(b"inapplicable QA")
        claimed_receipt = copy.deepcopy(receipt)
        claimed_receipt["subjects"] = copy.deepcopy(claimed)
        problems = acceptance.acceptance_receipt_problems(
            claimed_receipt, "release", context, claimed)
        self.assertTrue(any("must be null" in problem for problem in problems),
                        problems)

    def test_release_preflight_applies_profile_specific_qa_policy(self):
        candidate = b"candidate bytes"
        candidate_digest = canon.bytes_digest(candidate)
        lock_digest = canon.bytes_digest(b"content lock")
        content_lock = {"reads": [], "lockDigest": lock_digest}
        model = SimpleNamespace(edition={
            "editionId": "na", "declaredTransitiveInputs": [],
        })
        child = SimpleNamespace(
            returncode=0,
            stdout=canon.canonical_json({
                "candidateDigest": candidate_digest,
                "lockDigest": lock_digest,
            }).decode("utf-8"),
            stderr="",
        )
        with mock.patch.object(render, "render", return_value=candidate), \
                mock.patch.object(release.subprocess, "run",
                                  return_value=child):
            release._verify_release_preflight(
                ROOT, model, candidate, candidate, content_lock, None,
                TECHNICAL_PREVIEW_PROFILE)
            with self.assertRaisesRegex(
                    acceptance.AcceptanceError, "must not claim"):
                release._verify_release_preflight(
                    ROOT, model, candidate, candidate, content_lock,
                    {"record": {}}, TECHNICAL_PREVIEW_PROFILE)
            with self.assertRaisesRegex(
                    acceptance.AcceptanceError, "QA authorization"):
                release._verify_release_preflight(
                    ROOT, model, candidate, candidate, content_lock, None,
                    VALIDATED_RELEASE_PROFILE)

    def test_preview_release_transaction_emits_no_qa_binding(self):
        context = _receipt_context(TECHNICAL_PREVIEW_PROFILE)
        candidate = b"candidate bytes"
        content_lock = {
            "reads": [], "lockDigest": canon.bytes_digest(b"content lock"),
        }
        model = SimpleNamespace(edition={
            "editionId": "na", "artifactName": "preview.html",
            "declaredTransitiveInputs": [],
        })
        output = mock.Mock()
        with mock.patch.object(
                acceptance, "acceptance_context",
                side_effect=[context, copy.deepcopy(context)]), \
                mock.patch.object(acceptance, "run_registered_callbacks"), \
                mock.patch.object(release, "_verify_release_preflight") \
                as preflight, \
                mock.patch.object(release, "_verify_release_postcondition"):
            receipt = release.run_release_acceptance_transaction(
                ROOT, model, candidate, candidate, content_lock, None, output,
                release_profile="technical-preview")
        self.assertEqual(receipt["releaseProfile"], "technical-preview")
        self.assertIsNone(receipt["subjects"]["qaRecord"])
        self.assertIsNone(receipt["subjects"]["qaInputLockDigest"])
        preflight.assert_called_once()
        self.assertIsNone(preflight.call_args.args[5])
        self.assertEqual(preflight.call_args.args[6],
                         TECHNICAL_PREVIEW_PROFILE)

    def test_receipt_is_acyclic_and_runner_is_distinct_from_approver(self):
        outer_record = {
            "operator": "human@example.test", "operatorKind": "human",
            "acceptanceReceipt": self.receipt,
        }
        outer_digest = canon.composite_digest(
            "aa11393:release-record:c1", outer_record)
        receipt_bytes = canon.canonical_json(self.receipt)
        self.assertNotIn(outer_digest.encode("ascii"), receipt_bytes)
        self.assertEqual(self.receipt["runnerKind"], "tool")
        self.assertEqual(outer_record["operatorKind"], "human")
        self.assertFalse(any("record" in key.casefold()
                             for key in self.receipt
                             if key != "subjects"))

    def test_bundle_keeps_distinct_release_contexts_and_unions_inputs(self):
        first = _receipt_context()
        second = copy.deepcopy(first)
        second["runnerEditions"] = ["af"]
        second["runnerInputs"][0]["digest"] = canon.bytes_digest(
            b"changed runner source")
        second["runnerDigest"] = acceptance.runner_digest(
            second["registryDigest"], second["policyDigest"],
            second["runnerInputs"], second["controlPlan"],
            second["runnerEditions"],
            second["releaseProfile"],
            second["releaseProfileContract"])
        with mock.patch.object(acceptance, "acceptance_context",
                                  side_effect=[first, second]):
            contexts = currentstate.bundle_acceptance_context({
                "editions": ["one", "two"],
                "releaseProfile": "validated-release",
            })
        self.assertEqual(contexts, {"one": first, "two": second})

    def test_registry_declares_and_locks_every_test_module_and_fixture(self):
        with open(os.path.join(
                ROOT, "navigator", "schema", "acceptance.json"),
                encoding="utf-8") as fh:
            registry = json.load(fh)
        with tempfile.TemporaryDirectory() as tmp:
            registry_path = "navigator/schema/acceptance.json"
            fixture_paths = [entry["path"]
                             for entry in registry["runner"]["fixtures"]]
            paths = (list(control_inventory.CONTROL_SOURCE_PATHS) +
                     [entry["path"]
                      for entry in registry["runner"]["testModules"]] +
                     fixture_paths +
                     registry["runner"]["supportFiles"] +
                     [acceptance.RELEASE_POLICY_PATH])
            for path in [registry_path] + paths:
                dst = os.path.join(tmp, path)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy(os.path.join(ROOT, path), dst)
            na_before = acceptance.acceptance_context(tmp, ("na",))
            af_before = acceptance.acceptance_context(tmp, ("af",))
            bundle_before = acceptance.acceptance_context(
                tmp, ("na", "af"))
            self.assertEqual(
                acceptance.combine_acceptance_contexts(
                    {"na": na_before, "af": af_before}, ("na", "af")),
                bundle_before)
            self.assertEqual(bundle_before["runnerEditions"], ["af", "na"])
            na_fixture = next(
                entry["path"] for entry in registry["runner"]["fixtures"]
                if entry["editions"] == ["na"])
            af_fixture = next(
                entry["path"] for entry in registry["runner"]["fixtures"]
                if entry["editions"] == ["af"])
            self.assertIn(na_fixture, {
                entry["path"] for entry in na_before["runnerInputs"]})
            self.assertNotIn(na_fixture, {
                entry["path"] for entry in af_before["runnerInputs"]})
            self.assertIn(af_fixture, {
                entry["path"] for entry in af_before["runnerInputs"]})
            self.assertNotIn(af_fixture, {
                entry["path"] for entry in na_before["runnerInputs"]})
            with open(os.path.join(tmp, na_fixture), "ab") as fh:
                fh.write(b" ")
            na_after = acceptance.acceptance_context(tmp, ("na",))
            af_after = acceptance.acceptance_context(tmp, ("af",))
            bundle_after = acceptance.acceptance_context(
                tmp, ("na", "af"))
            self.assertNotEqual(na_before["runnerDigest"],
                                na_after["runnerDigest"])
            self.assertEqual(af_before["runnerDigest"],
                             af_after["runnerDigest"])
            self.assertNotEqual(bundle_before["runnerDigest"],
                                bundle_after["runnerDigest"])
            os.unlink(os.path.join(tmp, na_fixture))
            self.assertEqual(
                acceptance.acceptance_context(tmp, ("af",)),
                af_after,
                "AF context must not stat or read an inactive NA fixture")

    def test_registered_callbacks_use_a_fresh_selected_edition_process(self):
        import tests.test_acceptance as acceptance_tests
        context = acceptance.acceptance_context(ROOT, ("af",))
        self.assertNotIn(
            "navigator/tests/fixtures/migration_na_snapshot.json",
            {entry["path"] for entry in context["runnerInputs"]})
        acceptance.run_registered_callbacks(
            ROOT, ("AC-07.automated", "AC-19.automated"), ("af",),
            context)
        with self.assertRaisesRegex(
                acceptance.AcceptanceError, "fresh-process"):
            acceptance.run_registered_callbacks(
                ROOT, ("AC-07.automated",), ("not_an_edition",), context)
        self.assertEqual(acceptance_tests.EDITIONS, ("na", "af"))

    def test_registry_shape_version_applicability_and_text_are_closed(self):
        with open(os.path.join(
                ROOT, "navigator", "schema", "acceptance.json"),
                encoding="utf-8") as fh:
            registry = json.load(fh)
        mutations = []
        extra_top = copy.deepcopy(registry)
        extra_top["unexpected"] = True
        mutations.append(extra_top)
        wrong_version = copy.deepcopy(registry)
        wrong_version["acceptanceVersion"] = "1"
        mutations.append(wrong_version)
        blank_comment = copy.deepcopy(registry)
        blank_comment["comment"] = " "
        mutations.append(blank_comment)
        extra_criterion = copy.deepcopy(registry)
        extra_criterion["criteria"][0]["unexpected"] = True
        mutations.append(extra_criterion)
        wrong_applicability = copy.deepcopy(registry)
        wrong_applicability["criteria"][18]["applicability"] = "edition"
        mutations.append(wrong_applicability)
        blank_text = copy.deepcopy(registry)
        blank_text["criteria"][19]["text"] = ""
        mutations.append(blank_text)
        swapped_callbacks = copy.deepcopy(registry)
        swapped_callbacks["criteria"][1]["enforcedBy"]["tests"], \
            swapped_callbacks["criteria"][2]["enforcedBy"]["tests"] = (
                swapped_callbacks["criteria"][2]["enforcedBy"]["tests"],
                swapped_callbacks["criteria"][1]["enforcedBy"]["tests"],
            )
        mutations.append(swapped_callbacks)
        canon_owned_by_wrong_criterion = copy.deepcopy(registry)
        canon_callback = next(
            name for name in
            canon_owned_by_wrong_criterion["criteria"][6]
            ["enforcedBy"]["tests"]
            if name.startswith("test_canon."))
        canon_owned_by_wrong_criterion["criteria"][7]["enforcedBy"] \
            ["tests"].append(canon_callback)
        mutations.append(canon_owned_by_wrong_criterion)
        for index, mutated in enumerate(mutations):
            with self.subTest(mutation=index):
                with self.assertRaises(acceptance.AcceptanceError):
                    acceptance.validate_registry(mutated)

    def test_release_policy_is_separate_current_and_extensible(self):
        with open(os.path.join(
                ROOT, "navigator", "schema", "acceptance.json"),
                encoding="utf-8") as fh:
            registry = json.load(fh)
        with open(os.path.join(
                ROOT, "navigator", "schema", "release-policy.json"),
                encoding="utf-8") as fh:
            policy = json.load(fh)
        self.assertEqual(registry["acceptanceVersion"], "3")
        self.assertEqual(registry["runner"]["runnerVersion"], "3")
        self.assertNotIn("activeReleaseProfile", registry["runner"])
        self.assertNotIn("releaseProfiles", registry["runner"])
        self.assertEqual(policy["activeReleaseProfile"],
                         "technical-preview")
        selected, contract = acceptance.release_profile_contract(
            policy, registry, "technical-preview")
        self.assertEqual(selected, "technical-preview")
        self.assertEqual(contract, TECHNICAL_PREVIEW_PROFILE)
        with self.assertRaisesRegex(
                acceptance.AcceptanceError,
                "not the active release profile"):
            acceptance.release_profile_contract(
                policy, registry, "validated-release")

        extended = copy.deepcopy(policy)
        extended["profiles"].insert(0, {
            "id": "review-only",
            "observedControls": {
                identifier: "deferred"
                for identifier in acceptance_support.OBSERVED
            },
            "artifactLabel": "REVIEW ONLY — Compatibility is not authorized.",
        })
        self.assertEqual(profilepolicy.validate_policy(extended), extended)
        malformed = copy.deepcopy(policy)
        malformed["profiles"][0]["observedControls"].pop(
            "AC-15.observed")
        with self.assertRaises(profilepolicy.ProfilePolicyError):
            profilepolicy.validate_policy(malformed)

    def test_registry_semantics_prevent_shrinking_without_blocking_additions(self):
        with open(os.path.join(
                ROOT, "navigator", "schema", "acceptance.json"),
                encoding="utf-8") as fh:
            registry = json.load(fh)
        missing_baseline = copy.deepcopy(registry)
        missing_baseline["criteria"].pop(0)
        weakened_observation = copy.deepcopy(registry)
        weakened_observation["criteria"][10]["enforcedBy"][
            "qaRecordFields"] = []
        reused = copy.deepcopy(registry)
        reused["criteria"][2]["enforcedBy"]["tests"] = \
            reused["criteria"][1]["enforcedBy"]["tests"][:]
        for label, mutated in (
                ("mandatory criterion deletion", missing_baseline),
                ("observed control deletion", weakened_observation),
                ("callback reuse", reused)):
            with self.subTest(label=label):
                with self.assertRaises(acceptance.AcceptanceError):
                    acceptance.validate_registry(mutated)

        extended = copy.deepcopy(registry)
        extended["criteria"].append({
            "id": "AC-21",
            "applicability": "edition",
            "text": "A future feature has an explicit executable owner.",
            "enforcedBy": {
                "tests": [
                    "test_acceptance.Acceptance.test_ac21_future_feature"],
                "qaRecordFields": [],
            },
        })
        self.assertEqual(acceptance.validate_registry(extended), extended)

    def test_bundle_transaction_runs_registered_ac20_and_failure_blocks(self):
        from tests import test_bundle_lifecycle as lifecycle

        cfg, release_records, qa_records, attestations, stored, \
            manifest_bytes, unused_wording = lifecycle._fixture(
                profile=lifecycle.TECHNICAL_PREVIEW_PROFILE)
        planned_members = [
            (member["name"], manifest_bytes
             if member["kind"] == "bundle-manifest"
             else stored[(member["kind"], member["name"])])
            for member in cfg["members"]
        ]
        selected_release = next(
            envelope for envelope in release_records
            if envelope["digest"] == cfg["members"][0]["releaseRecord"])
        release_record = selected_release["record"]
        plan = {
            "members": planned_members,
            "releaseRecords": [selected_release["digest"]],
            "manifestApproval": cfg["manifestApproval"],
            "acceptanceChain": {
                "releaseRecords": release_records,
                "qaRecords": qa_records,
                "attestations": attestations,
                "requiredAttestationsByEdition": {
                    "na": sorted(lifecycle.FIXTURE_ATTESTATION_POLICY["na"]),
                },
                "currentSidesByEdition":
                    lifecycle.FIXTURE_CURRENT_SIDES,
                "acceptanceContextByEdition":
                    {"na": lifecycle._acceptance_context(
                        lifecycle.TECHNICAL_PREVIEW_PROFILE)},
                "qaAuthorizationContextByEdition": {
                    "na": None,
                },
                "currentReleaseBindingsByEdition": {
                    "na": {
                        "sealed": release_record["sealed"],
                        "sealedDigest": release_record["sealedDigest"],
                        "lockDigest": release_record["lockDigest"],
                        "declaredReleaseTimestamp":
                            release_record["declaredReleaseTimestamp"],
                    },
                },
            },
        }
        zip_bytes = bundlezip.build_zip(
            planned_members, cfg["declaredTimestamp"])
        checksum_bytes = release.checksum_text(
            cfg["name"], zip_bytes).encode("utf-8")
        config_digest = canon.bytes_digest(b"bundle config")
        with open(os.path.join(
                ROOT, "navigator", "schema", "planes.json"),
                encoding="utf-8") as fh:
            planes = json.load(fh)
        def populate_inputs(root):
            for unused_kind, name in (
                    (member["kind"], member["name"])
                    for member in cfg["members"]
                    if member["kind"] != "bundle-manifest"):
                path = os.path.join(root, name)
                os.makedirs(os.path.dirname(path) or root, exist_ok=True)
                with open(path, "wb") as fh:
                    fh.write(stored[(unused_kind, name)])

        def transact(current_cfg, current_plan, root):
            populate_inputs(root)
            output = gateway.OutputGateway(root, "bundle", planes)
            return release.run_bundle_acceptance_transaction(
                ROOT, current_cfg, config_digest, current_plan, zip_bytes,
                checksum_bytes, manifest_bytes, output)

        with tempfile.TemporaryDirectory() as tmp:
            receipt = transact(cfg, plan, tmp)
            self.assertEqual(receipt["runnerEditions"], ["na"])
            self.assertEqual(receipt["results"], [
                {"control": "AC-20.automated",
                 "phase": "bundle-postcondition", "status": "passed"},
                {"control": "AC-20.bundle-postcondition",
                 "phase": "bundle-postcondition", "status": "passed"},
            ])

        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(
                acceptance, "run_registered_callbacks",
                side_effect=acceptance.AcceptanceError(
                    "injected registered AC-20 failure")) as callback:
            with self.assertRaisesRegex(
                    acceptance.AcceptanceError,
                    "injected registered AC-20 failure"):
                transact(cfg, plan, tmp)
            callback.assert_called_once()
            args = callback.call_args.args
            self.assertEqual(args[1], ("AC-20.automated",))
            self.assertEqual(args[2], cfg["editions"])
            self.assertEqual(args[4]["kind"], "bundle-postcondition")

        bad_plans = {}
        stale_release = copy.deepcopy(plan)
        stale_release["acceptanceChain"][
            "currentReleaseBindingsByEdition"]["na"]["sealedDigest"] = \
            canon.bytes_digest(b"stale current candidate")
        bad_plans["release"] = (copy.deepcopy(cfg), stale_release)

        stale_attestation = copy.deepcopy(plan)
        stale_attestation["acceptanceChain"][
            "currentSidesByEdition"]["na"]["priorityMap"] = \
            canon.bytes_digest(b"stale attestation side")
        bad_plans["attestation"] = (
            copy.deepcopy(cfg), stale_attestation)

        pending_manifest_cfg = copy.deepcopy(cfg)
        pending_manifest = copy.deepcopy(plan)
        manifest_envelope = next(
            envelope for envelope in pending_manifest[
                "acceptanceChain"]["attestations"]
            if envelope["record"].get("type") == "manifest-approval")
        manifest_envelope["record"]["approvalStatus"] = "pending"
        manifest_envelope["digest"] = canon.composite_digest(
            "aa11393:attestation:c1", manifest_envelope["record"])
        pending_manifest_cfg["manifestApproval"] = \
            manifest_envelope["digest"]
        pending_manifest["manifestApproval"] = manifest_envelope["digest"]
        bad_plans["manifest"] = (pending_manifest_cfg, pending_manifest)

        for label, (bad_cfg, bad_plan) in bad_plans.items():
            with self.subTest(stale_evidence=label), \
                    tempfile.TemporaryDirectory() as tmp:
                with self.assertRaisesRegex(
                        acceptance.AcceptanceError,
                        "fresh-process acceptance callbacks failed"):
                    transact(bad_cfg, bad_plan, tmp)


class TestVerifyCurrentFinalState(unittest.TestCase):
    def _closure_report(self):
        return {"status": "current", "checks": {}}

    def test_discovered_test_mutation_cannot_certify_current(self):
        with tempfile.TemporaryDirectory() as root:
            verified = os.path.join(root, "verified-source.txt")
            with open(verified, "wb") as fh:
                fh.write(b"verified\n")

            def mutate_sandbox(sandbox_root):
                with open(os.path.join(sandbox_root, "verified-source.txt"),
                          "wb") as fh:
                    fh.write(b"mutated by last test\n")
                return "Ran 1 test"

            with mock.patch.object(currentstate, "ROOT", root), \
                    mock.patch.object(
                        currentstate, "_verify_current_closure",
                        side_effect=lambda byte_source, load_planes:
                            self._closure_report()), \
                    mock.patch.object(
                        currentstate, "_run_full_test_suite",
                        side_effect=mutate_sandbox), \
                    self.assertRaisesRegex(
                        RuntimeError, "tests mutated the verified snapshot"):
                currentstate.verify_current_state(run_tests=True)
            with open(verified, "rb") as fh:
                self.assertEqual(fh.read(), b"verified\n")

    def test_absolute_live_mutation_cannot_escape_test_isolation(self):
        with tempfile.TemporaryDirectory() as root:
            verified = os.path.join(root, "verified-source.txt")
            with open(verified, "wb") as fh:
                fh.write(b"verified\n")

            def mutate_live(unused_sandbox_root):
                with open(verified, "wb") as fh:
                    fh.write(b"mutated live\n")
                return "Ran 1 test"

            with mock.patch.object(currentstate, "ROOT", root), \
                    mock.patch.object(
                        currentstate, "_verify_current_closure",
                        side_effect=lambda byte_source, load_planes:
                            self._closure_report()), \
                    mock.patch.object(
                        currentstate, "_run_full_test_suite",
                        side_effect=mutate_live), \
                    self.assertRaisesRegex(
                        RuntimeError, "live repository changed"):
                currentstate.verify_current_state(run_tests=True)

    def test_first_closure_consumes_the_initial_snapshot(self):
        with tempfile.TemporaryDirectory() as root:
            source = os.path.join(root, "verified-source.txt")
            with open(source, "wb") as fh:
                fh.write(b"captured\n")
            seen = []

            def closure(byte_source, load_planes):
                seen.append(byte_source(source))
                if len(seen) == 1:
                    # A live change after the initial capture must not reach
                    # the first closure: its byte source serves only the
                    # captured bytes, and the A/B bracket refuses the run.
                    with open(source, "wb") as fh:
                        fh.write(b"mutated live\n")
                    seen.append(byte_source(source))
                return self._closure_report()

            with mock.patch.object(currentstate, "ROOT", root), \
                    mock.patch.object(
                        currentstate, "_verify_current_closure",
                        side_effect=closure), \
                    self.assertRaisesRegex(
                        RuntimeError, "live repository changed"):
                currentstate.verify_current_state(run_tests=False)
            self.assertEqual(seen, [b"captured\n", b"captured\n"])

    def test_final_closure_consumes_a_snapshot_equal_to_the_initial(self):
        with tempfile.TemporaryDirectory() as root:
            source = os.path.join(root, "verified-source.txt")
            with open(source, "wb") as fh:
                fh.write(b"stable\n")
            received = []

            def closure(byte_source, load_planes):
                received.append(byte_source(source))
                return self._closure_report()

            with mock.patch.object(currentstate, "ROOT", root), \
                    mock.patch.object(
                        currentstate, "_verify_current_closure",
                        side_effect=closure):
                report = currentstate.verify_current_state(run_tests=False)
            self.assertEqual(received, [b"stable\n", b"stable\n"])
            self.assertEqual(report["status"], "current")
            self.assertIn("repositorySnapshot", report["checks"])

    def test_snapshot_capture_rejects_a_file_changed_while_reading(self):
        with tempfile.TemporaryDirectory() as root:
            target = os.path.join(root, "source.txt")
            with open(target, "wb") as fh:
                fh.write(b"stable bytes\n")
            os.chmod(target, 0o644)
            ordinary_open = open

            class MutatingHandle:
                def __init__(self, handle):
                    self.handle = handle

                def __enter__(self):
                    return self

                def __exit__(self, *args):
                    return self.handle.__exit__(*args)

                def fileno(self):
                    return self.handle.fileno()

                def read(self):
                    data = self.handle.read()
                    os.chmod(target, 0o600)
                    return data

            def changing_open(path, *args, **kwargs):
                handle = ordinary_open(path, *args, **kwargs)
                if os.path.abspath(os.fspath(path)) == target:
                    return MutatingHandle(handle)
                return handle

            with mock.patch("builtins.open", side_effect=changing_open), \
                    self.assertRaisesRegex(
                        snapshot.SnapshotError, "changed during snapshot"):
                snapshot.RepositorySnapshot.capture(root)


class TestValidateCurrentDocuments(unittest.TestCase):
    """validate-current adds live document-integrity gates to the closure."""

    def _closure_report(self):
        return {"status": "current", "checks": {}}

    @staticmethod
    def _git_root_with_changed_markdown(root, initial, changed):
        subprocess.run(["git", "init", "-q"], cwd=root, check=True,
                       capture_output=True)
        path = os.path.join(root, "doc.md")
        with open(path, "wb") as fh:
            fh.write(initial)
        subprocess.run(["git", "add", "doc.md"], cwd=root, check=True,
                       capture_output=True)
        subprocess.run(
            ["git", "-c", "user.name=Test",
             "-c", "user.email=test@example.invalid",
             "-c", "commit.gpgsign=false",
             "commit", "-qm", "baseline"],
            cwd=root, check=True, capture_output=True)
        if changed is not None:
            with open(path, "wb") as fh:
                fh.write(changed)

    @staticmethod
    def _prior_art_tree(root, digest=None):
        prior = os.path.join(root, "US", "prior-art")
        os.makedirs(os.path.join(prior, ".pipeline"))
        payload = b"canonical source pdf bytes\n"
        with open(os.path.join(prior, "A1.pdf"), "wb") as fh:
            fh.write(payload)
        hex_digest = digest or canon.bytes_digest(payload).rsplit(":", 1)[1]
        with open(os.path.join(prior, ".pipeline",
                               "pdf-source-checksums.sha256"),
                  "w", encoding="utf-8") as fh:
            fh.write("%s  %s\n" % (hex_digest, "A1.pdf"))

    def test_changed_markdown_renders_or_fails_closed(self):
        with tempfile.TemporaryDirectory() as root:
            self._git_root_with_changed_markdown(
                root, b"# Title\n", b"# Title\n\nchanged body\n")
            with mock.patch.object(currentstate, "ROOT", root):
                self.assertEqual(
                    currentstate._changed_markdown_render_problems(), [])
        with tempfile.TemporaryDirectory() as root:
            # A deleted tracked Markdown file is still named by git diff,
            # and pandoc cannot render a path that does not exist.
            self._git_root_with_changed_markdown(root, b"# Title\n", None)
            os.remove(os.path.join(root, "doc.md"))
            with mock.patch.object(currentstate, "ROOT", root):
                problems = currentstate._changed_markdown_render_problems()
            self.assertTrue(
                any("pandoc" in problem for problem in problems), problems)

    def test_changed_markdown_empty_set_passes_and_tool_failure_closes(self):
        with tempfile.TemporaryDirectory() as root:
            self._git_root_with_changed_markdown(root, b"# Title\n", None)
            with mock.patch.object(currentstate, "ROOT", root):
                self.assertEqual(
                    currentstate._changed_markdown_render_problems(), [])
        with mock.patch.object(
                currentstate.subprocess, "run",
                side_effect=OSError("tool missing")):
            problems = currentstate._changed_markdown_render_problems()
        self.assertTrue(
            any("could not complete" in problem for problem in problems),
            problems)

    def test_prior_art_checksums_verify_or_fail_closed(self):
        with tempfile.TemporaryDirectory() as root:
            self._prior_art_tree(root)
            with mock.patch.object(currentstate, "ROOT", root):
                self.assertEqual(
                    currentstate._prior_art_checksum_problems(), [])
        with tempfile.TemporaryDirectory() as root:
            self._prior_art_tree(root, digest="0" * 64)
            with mock.patch.object(currentstate, "ROOT", root):
                problems = currentstate._prior_art_checksum_problems()
            self.assertTrue(
                any("prior-art checksum check failed" in problem
                    for problem in problems), problems)
        with tempfile.TemporaryDirectory() as root:
            with mock.patch.object(currentstate, "ROOT", root):
                problems = currentstate._prior_art_checksum_problems()
            self.assertTrue(problems, "missing tree must fail closed")
        with mock.patch.object(
                currentstate.subprocess, "run",
                side_effect=OSError("tool missing")):
            problems = currentstate._prior_art_checksum_problems()
        self.assertTrue(
            any("could not complete" in problem for problem in problems),
            problems)

    def test_validate_current_runs_document_checks_inside_the_brackets(self):
        with tempfile.TemporaryDirectory() as root:
            source = os.path.join(root, "verified-source.txt")
            with open(source, "wb") as fh:
                fh.write(b"stable\n")
            order = []

            def closure(byte_source, load_planes):
                order.append("closure")
                return self._closure_report()

            with mock.patch.object(currentstate, "ROOT", root), \
                    mock.patch.object(
                        currentstate, "_verify_current_closure",
                        side_effect=closure), \
                    mock.patch.object(
                        currentstate, "_changed_markdown_render_problems",
                        side_effect=lambda: order.append(
                            "changedMarkdown") or []), \
                    mock.patch.object(
                        currentstate, "_prior_art_checksum_problems",
                        side_effect=lambda: order.append(
                            "priorArtChecksums") or []):
                report = currentstate.validate_current_state(run_tests=False)
            self.assertEqual(
                order, ["closure", "changedMarkdown", "priorArtChecksums",
                        "closure"])
            self.assertEqual(report["checks"]["changedMarkdown"], "current")
            self.assertEqual(
                report["checks"]["priorArtChecksums"], "current")

    def test_validate_current_refuses_when_a_document_check_fails(self):
        with tempfile.TemporaryDirectory() as root:
            with open(os.path.join(root, "verified-source.txt"), "wb") as fh:
                fh.write(b"stable\n")
            closures = []

            def closure(byte_source, load_planes):
                closures.append(byte_source)
                return self._closure_report()

            with mock.patch.object(currentstate, "ROOT", root), \
                    mock.patch.object(
                        currentstate, "_verify_current_closure",
                        side_effect=closure), \
                    mock.patch.object(
                        currentstate, "_changed_markdown_render_problems",
                        return_value=["broken.md does not render"]), \
                    self.assertRaisesRegex(RuntimeError, "changedMarkdown"):
                currentstate.validate_current_state(run_tests=False)
            # The final closure produces the report; it never ran, so no
            # status-current report can exist after a failing document gate.
            self.assertEqual(len(closures), 1)

    def test_verify_current_carries_no_document_checks_by_default(self):
        with tempfile.TemporaryDirectory() as root:
            with open(os.path.join(root, "verified-source.txt"), "wb") as fh:
                fh.write(b"stable\n")
            with mock.patch.object(currentstate, "ROOT", root), \
                    mock.patch.object(
                        currentstate, "_verify_current_closure",
                        side_effect=lambda byte_source, load_planes:
                            self._closure_report()):
                report = currentstate.verify_current_state(run_tests=False)
            self.assertNotIn("changedMarkdown", report["checks"])
            self.assertNotIn("priorArtChecksums", report["checks"])

    def test_module_entry_delegates_to_build_main(self):
        child = subprocess.run(
            [sys.executable, "-m", "navigator", "status", "--private-runner"],
            cwd=ROOT, capture_output=True, text=True, timeout=300)
        self.assertEqual(child.returncode, 0, child.stderr)
        self.assertIn("release profile:", child.stdout)
        usage = subprocess.run(
            [sys.executable, "-m", "navigator", "--private-runner"],
            cwd=ROOT, capture_output=True, text=True, timeout=300)
        self.assertNotEqual(usage.returncode, 0)
        self.assertIn("build.py validate-current", usage.stderr)


class TestSnapshotByteSource(unittest.TestCase):
    def _pinned_tree(self, root, contents):
        for relpath, data in contents.items():
            path = os.path.join(root, *relpath.split("/"))
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as fh:
                fh.write(data)

    def test_closure_reads_captured_bytes_not_live_changes(self):
        original = b"original claims\n"
        entry = {
            "role": "fragment-source",
            "visibility": "rendered",
            "version": "NA-2026-07-22-v4",
            "primary": "claims/na.md",
            "files": {"claims/na.md": canon.bytes_digest(original)},
        }
        with tempfile.TemporaryDirectory() as root:
            self._pinned_tree(root, {"claims/na.md": original})
            captured = snapshot.RepositorySnapshot.capture(
                root, retain_bytes=True)
            with open(os.path.join(root, "claims", "na.md"), "wb") as fh:
                fh.write(b"drifted claims\n")

            content = gateway.ContentGateway(
                root, byte_source=captured.byte_source())
            plan = pinplan.corpus_closure("na-claims", entry, content)
            self.assertTrue(plan["pinCurrent"])
            self.assertEqual(
                pinplan.closure_problems(plan, "na-claims"), [])

            fresh = snapshot.RepositorySnapshot.capture(
                root, retain_bytes=True)
            drifted = pinplan.corpus_closure(
                "na-claims", entry,
                gateway.ContentGateway(
                    root, byte_source=fresh.byte_source()))
            self.assertFalse(drifted["pinCurrent"])
            self.assertEqual(
                drifted["files"][0]["actualDigest"],
                canon.bytes_digest(b"drifted claims\n"))
            self.assertTrue(any(
                "claims/na.md" in problem
                for problem in pinplan.closure_problems(
                    drifted, "na-claims")))

    def test_snapshot_without_retained_bytes_has_no_byte_source(self):
        with tempfile.TemporaryDirectory() as root:
            self._pinned_tree(root, {"input.txt": b"data\n"})
            digest_only = snapshot.RepositorySnapshot.capture(root)
            with self.assertRaisesRegex(
                    snapshot.SnapshotError, "without byte retention"):
                digest_only.read_bytes("input.txt")
            retained = snapshot.RepositorySnapshot.capture(
                root, retain_bytes=True)
            with self.assertRaisesRegex(
                    snapshot.SnapshotError,
                    "absent from repository snapshot"):
                retained.read_bytes("missing.txt")

    def test_materialize_writes_captured_bytes_after_live_drift(self):
        with tempfile.TemporaryDirectory() as root, \
                tempfile.TemporaryDirectory() as destination:
            self._pinned_tree(root, {"docs/a.txt": b"captured\n"})
            captured = snapshot.RepositorySnapshot.capture(
                root, retain_bytes=True)
            with open(os.path.join(root, "docs", "a.txt"), "wb") as fh:
                fh.write(b"live drift\n")
            captured.materialize(destination)
            with open(os.path.join(destination, "docs", "a.txt"),
                      "rb") as fh:
                self.assertEqual(fh.read(), b"captured\n")


class TestQaPinPlanning(unittest.TestCase):
    def test_auxiliary_drift_is_reported_with_a_replacement_digest(self):
        primary = b"primary\n"
        auxiliary = b"auxiliary current bytes\n"
        entry = {
            "role": "qa-source",
            "visibility": "internal",
            "versionBindings": {"NA": "NA-2026-07-22-v4"},
            "primary": "qa/primary.md",
            "files": {
                "qa/auxiliary.md": canon.bytes_digest(b"stale auxiliary"),
                "qa/primary.md": canon.bytes_digest(primary),
            },
        }
        content = mock.Mock()
        content.read_bytes.side_effect = lambda path: {
            "qa/auxiliary.md": auxiliary,
            "qa/primary.md": primary,
        }[path]
        plan = pinplan.corpus_closure(
            "qa-priority", entry, content,
            {"NA": "NA-2026-07-22-v4"})
        self.assertEqual(
            [item["path"] for item in plan["files"]],
            ["qa/auxiliary.md", "qa/primary.md"])
        auxiliary_plan = plan["files"][0]
        self.assertFalse(auxiliary_plan["pinCurrent"])
        self.assertEqual(
            auxiliary_plan["actualDigest"], canon.bytes_digest(auxiliary))
        self.assertFalse(plan["pinCurrent"])
        self.assertTrue(any(
            "qa/auxiliary.md" in problem
            for problem in pinplan.closure_problems(plan, "priorityMap")))

    def test_qa_versions_are_structured_and_tied_to_current_claim_versions(self):
        with tempfile.TemporaryDirectory() as root:
            os.makedirs(os.path.join(root, "qa"))
            source = os.path.join(root, "qa", "primary.md")
            with open(source, "wb") as fh:
                fh.write(b"source\n")
            registry_path = os.path.join(root, "qa", "registry.json")
            malformed = {
                "qaRegistryVersion": "1",
                "corpora": {
                    "qa-priority": {
                        "role": "qa-source", "visibility": "internal",
                        "versionBindings": {"NA": "obsolete-label"},
                        "primary": "qa/primary.md",
                        "files": {
                            "qa/primary.md": canon.bytes_digest(b"source\n"),
                        },
                    },
                },
            }
            with open(registry_path, "w", encoding="utf-8") as fh:
                json.dump(malformed, fh)
            with self.assertRaisesRegex(
                    qaregistry.QaRegistryError, "version binding"):
                qaregistry.QaRegistry(
                    gateway.ContentGateway(root), "qa/registry.json",
                    {"qa-priority"})

        obsolete = copy.deepcopy(malformed["corpora"]["qa-priority"])
        obsolete_version = "NA-" + "2025-01-01-v1"
        obsolete["versionBindings"] = {"NA": obsolete_version}
        content = mock.Mock()
        content.read_bytes.return_value = b"source\n"
        plan = pinplan.corpus_closure(
            "qa-priority", obsolete, content,
            {"NA": "NA-2026-07-22-v4"})
        self.assertFalse(plan["versionCurrent"])
        self.assertEqual(plan["configuredVersions"], {
            "NA": obsolete_version})
        self.assertEqual(plan["expectedVersions"], {
            "NA": "NA-2026-07-22-v4"})


class TestRegistryCorpusClosure(unittest.TestCase):
    def test_target_corpus_figure_drift_fails_aggregate_currency(self):
        markdown = b"disclosure\n"
        figure = b"figure current bytes\n"
        entry = {
            "role": "derivative",
            "visibility": "rendered",
            "version": "transcription of PCT/IB2025/051755 as filed (pinned)",
            "primary": "pct/disclosure.md",
            "files": {
                "pct/disclosure.md": canon.bytes_digest(markdown),
                "pct/figures/Fig-1.png": canon.bytes_digest(b"stale figure"),
            },
        }
        content = mock.Mock()
        content.read_bytes.side_effect = lambda path: {
            "pct/disclosure.md": markdown,
            "pct/figures/Fig-1.png": figure,
        }[path]
        plan = pinplan.corpus_closure("pct-disclosure", entry, content)
        figure_plan = next(
            item for item in plan["files"] if item["path"].endswith(".png"))
        self.assertFalse(figure_plan["pinCurrent"])
        self.assertEqual(
            figure_plan["actualDigest"], canon.bytes_digest(figure))
        self.assertFalse(plan["pinCurrent"])
        # The external filing identity stays an opaque string: no structured
        # bindings are invented for a registry corpus.
        self.assertEqual(
            plan["configuredVersion"],
            "transcription of PCT/IB2025/051755 as filed (pinned)")
        self.assertEqual(plan["expectedVersion"], plan["configuredVersion"])
        self.assertTrue(plan["versionCurrent"])
        self.assertTrue(any(
            "pct/figures/Fig-1.png" in problem
            for problem in pinplan.closure_problems(plan, "pct-disclosure")))

    def test_claim_corpus_currency_covers_every_declared_file(self):
        primary = b"claims\n"
        auxiliary = b"claim notes\n"
        entry = {
            "role": "fragment-source",
            "visibility": "rendered",
            "version": "NA-2026-07-22-v4",
            "profile": "profiles/seg_claims.json",
            "primary": "claims/na.md",
            "files": {
                "claims/na.md": canon.bytes_digest(primary),
                "claims/notes.md": canon.bytes_digest(b"stale notes"),
            },
        }
        content = mock.Mock()
        content.read_bytes.side_effect = lambda path: {
            "claims/na.md": primary,
            "claims/notes.md": auxiliary,
        }[path]
        plan = pinplan.corpus_closure("na-claims", entry, content)
        # Drift in a non-primary declared file still fails aggregate
        # currency: the primary designation never narrows integrity currency.
        self.assertEqual(
            [item["path"] for item in plan["files"]],
            ["claims/na.md", "claims/notes.md"])
        auxiliary_plan = plan["files"][1]
        self.assertFalse(auxiliary_plan["primary"])
        self.assertFalse(auxiliary_plan["pinCurrent"])
        self.assertEqual(
            auxiliary_plan["actualDigest"], canon.bytes_digest(auxiliary))
        self.assertFalse(plan["pinCurrent"])
        self.assertTrue(any(
            "claims/notes.md" in problem
            for problem in pinplan.closure_problems(plan, "na-claims")))


class TestAttestationEvidence(unittest.TestCase):
    def _attestation(self):
        return {
            "digest": "attestation-digest",
            "record": {
                "type": "legend-approval",
                "edition": None,
                "sides": {"legendWording": "legend-digest"},
                "note": "Counsel review completed",
                "approvalStatus": "passed",
                "operator": "Counsel Reviewer",
                "operatorKind": "human",
                "producerCommand":
                    recordprovenance.ATTESTATION_PRODUCER_COMMAND,
            },
        }

    def test_confirmation_requires_structured_authorized_final_evidence(self):
        current = {"legendWording": "legend-digest"}
        attestation = self._attestation()
        self.assertEqual(currentstate.attestation_evidence_problems(
            attestation, current, "na"), [])

        model = copy.deepcopy(attestation)
        model["record"].update({
            "operator": "codex:gpt-5.6-sol:run-test-001",
            "operatorKind": "model",
        })
        self.assertEqual(currentstate.attestation_evidence_problems(
            model, current, "na"), [])

        legacy = copy.deepcopy(attestation)
        legacy["record"].pop("approvalStatus")
        legacy["record"].pop("operatorKind")
        self.assertTrue(currentstate.attestation_evidence_problems(
            legacy, current, "na"))

        pending = copy.deepcopy(attestation)
        pending["record"]["note"] = "Pending counsel confirmation"
        self.assertTrue(any("pending" in problem for problem in
                            currentstate.attestation_evidence_problems(
                                pending, current, "na")))

        failed = copy.deepcopy(attestation)
        failed["record"]["note"] = "Review failed; do not release"
        self.assertTrue(any("failure" in problem for problem in
                            currentstate.attestation_evidence_problems(
                                failed, current, "na")))

        no_errors = copy.deepcopy(attestation)
        no_errors["record"]["note"] = \
            "Counsel review passed with no errors"
        self.assertEqual(currentstate.attestation_evidence_problems(
            no_errors, current, "na"), [])

        invisible_operator = copy.deepcopy(attestation)
        invisible_operator["record"]["operator"] = "\u200b\u2060\u200e"
        self.assertTrue(any("identified operator" in problem for problem in
                            currentstate.attestation_evidence_problems(
                                invisible_operator, current, "na")))

        missing_note = copy.deepcopy(attestation)
        missing_note["record"].pop("note")
        self.assertTrue(any("note" in problem for problem in
                            currentstate.attestation_evidence_problems(
                                missing_note, current, "na")))

        wrong_sides = copy.deepcopy(attestation)
        wrong_sides["record"]["sides"]["extra"] = "digest"
        self.assertTrue(any("exactly" in problem for problem in
                            currentstate.attestation_evidence_problems(
                                wrong_sides, current, "na")))

        malformed = {"digest": "x", "record": []}
        self.assertTrue(currentstate.attestation_evidence_problems(
            malformed, current, "na"))

    def test_attestation_provenance_is_exact_and_mandatory(self):
        current = {"legendWording": "legend-digest"}
        for producer in (None, "navigator/build.py attest/v2",
                         "navigator/tools/stamp.py attest/v1"):
            with self.subTest(producer=producer):
                attestation = self._attestation()
                if producer is None:
                    attestation["record"].pop("producerCommand")
                else:
                    attestation["record"]["producerCommand"] = producer
                problems = currentstate.attestation_evidence_problems(
                    attestation, current, "na")
                self.assertTrue(any(
                    "producerCommand" in problem for problem in problems),
                    problems)

    def test_attest_cli_requires_explicit_approval(self):
        with self.assertRaisesRegex(SystemExit, "--approved"):
            build.cmd_attest([
                "legend-approval", "--note=Counsel review completed",
            ])

    def test_attest_cli_appends_human_and_model_with_current_hash(self):
        with open(os.path.join(ROOT, "navigator", "schema", "planes.json"),
                  encoding="utf-8") as fh:
            planes = json.load(fh)
        manifest_text = (
            TECHNICAL_PREVIEW_PROFILE["artifactLabel"] +
            " This bundle does not claim compatibility authorization."
        )
        for kind, identity in (
                ("human", "reviewer@example.test"),
                ("model", "codex:gpt-5.6-sol:run-attest-cli")):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as tmp:
                navigator = os.path.join(tmp, "navigator")
                records = os.path.join(navigator, "records")
                schema_dir = os.path.join(navigator, "schema")
                os.makedirs(records)
                os.makedirs(schema_dir)
                with open(os.path.join(navigator, "bundle-manifest.json"),
                          "w", encoding="utf-8") as fh:
                    json.dump({
                        "manifestVersion": "3",
                        "releaseProfile": "technical-preview",
                        "compatibilityAuthorization": "not-authorized",
                        "deferredControls": [
                            "AC-11.observed", "AC-12.observed",
                            "AC-13.observed", "AC-15.observed"],
                        "bundleManifestText": manifest_text,
                    }, fh)
                shutil.copyfile(
                    os.path.join(ROOT, "navigator", "schema",
                                 "release-policy.json"),
                    os.path.join(schema_dir, "release-policy.json"))
                with mock.patch.object(build, "ROOT", tmp), \
                        mock.patch.object(build, "RECORDS", records), \
                        mock.patch.object(build, "load_planes",
                                          return_value=planes), \
                        mock.patch.dict(os.environ, {
                            "NAV_OPERATOR": identity,
                            "NAV_OPERATOR_KIND": kind,
                        }, clear=True), \
                        mock.patch("builtins.print"):
                    build.cmd_attest([
                        "manifest-approval", "--approved",
                        "--note=Reviewed exact current wording",
                    ])
                envelopes = gateway.VerificationGateway(
                    records, "status", planes).read_all("attestation")
                self.assertEqual(len(envelopes), 1)
                record = envelopes[0]["record"]
                self.assertEqual(record["operator"], identity)
                self.assertEqual(record["operatorKind"], kind)
                self.assertEqual(
                    record["producerCommand"],
                    recordprovenance.ATTESTATION_PRODUCER_COMMAND)
                self.assertEqual(record["sides"], {
                    "manifestWording": canon.text_digest(
                        canon.canon_prose(manifest_text)),
                })
                self.assertEqual(currentstate.attestation_evidence_problems(
                    envelopes[0], record["sides"], "na"), [])

    def test_support_matrix_attest_requires_exact_named_approver(self):
        with open(os.path.join(ROOT, "navigator", "schema", "planes.json"),
                  encoding="utf-8") as fh:
            planes = json.load(fh)
        # An operator identity is not prose evidence.  A legitimate identity
        # may contain a word that would make an approval note non-final.
        approver = "qa-failure-reviewer@example.test"
        matrix = copy.deepcopy(QA_SUPPORT_MATRIX)
        matrix["comment"] = "Focused atomic support approval fixture"
        matrix["approver"] = approver
        with tempfile.TemporaryDirectory() as tmp:
            schema_dir = os.path.join(tmp, "navigator", "schema")
            records = os.path.join(tmp, "navigator", "records")
            os.makedirs(schema_dir)
            os.makedirs(records)
            with open(os.path.join(schema_dir, "support-matrix.json"),
                      "w", encoding="utf-8") as fh:
                json.dump(matrix, fh)
            shutil.copyfile(
                os.path.join(ROOT, "navigator", "schema",
                             "support-matrix.schema.json"),
                os.path.join(schema_dir, "support-matrix.schema.json"))
            patches = (
                mock.patch.object(build, "ROOT", tmp),
                mock.patch.object(build, "RECORDS", records),
                mock.patch.object(build, "load_planes", return_value=planes),
                mock.patch("builtins.print"),
            )
            with patches[0], patches[1], patches[2], patches[3], \
                    mock.patch.dict(os.environ, {
                        "NAV_OPERATOR": "different:model:run",
                        "NAV_OPERATOR_KIND": "model",
                    }, clear=True):
                with self.assertRaisesRegex(
                        SystemExit, "does not match support matrix approver"):
                    build.cmd_attest([
                        "support-matrix-approval", "--approved",
                        "--note=Reviewed the exact support target set",
                    ])

            with patches[0], patches[1], patches[2], patches[3], \
                    mock.patch.dict(os.environ, {
                        "NAV_OPERATOR": approver,
                        "NAV_OPERATOR_KIND": "model",
                    }, clear=True):
                build.cmd_attest([
                    "support-matrix-approval", "--approved",
                    "--note=Reviewed the exact support target set",
                ])
            envelopes = gateway.VerificationGateway(
                records, "status", planes).read_all("attestation")
            self.assertEqual(len(envelopes), 1)
            self.assertEqual(envelopes[0]["record"]["operator"], approver)
            self.assertEqual(envelopes[0]["record"]["operatorKind"], "model")
            with open(os.path.join(schema_dir, "support-matrix.json"),
                      "rb") as fh:
                matrix_digest = canon.bytes_digest(fh.read())
            self.assertEqual(envelopes[0]["record"]["sides"], {
                "supportMatrix": matrix_digest,
            })

    def test_current_selection_prefers_human_then_digest(self):
        current = {"legendWording": "legend-digest"}
        model = self._attestation()
        model["digest"] = "000-model"
        model["record"].update({
            "operator": "codex:gpt-5.6-sol:run-attest",
            "operatorKind": "model",
        })
        human_b = self._attestation()
        human_b["digest"] = "bbb-human"
        human_a = copy.deepcopy(human_b)
        human_a["digest"] = "aaa-human"
        chosen, problems = currentstate._confirmed_current_attestations(
            [model, human_b, human_a], current, "na",
            ("legend-approval",), None)
        self.assertEqual(problems, [])
        self.assertEqual(chosen["legend-approval"]["digest"], "aaa-human")

        chosen, problems = currentstate._confirmed_current_attestations(
            [model], current, "na", ("legend-approval",), None)
        self.assertEqual(problems, [])
        self.assertEqual(chosen["legend-approval"]["digest"], "000-model")

    def test_support_matrix_selection_requires_exact_named_approver(self):
        attestation = self._attestation()
        attestation["record"].update({
            "type": "support-matrix-approval",
            "sides": {"supportMatrix": "matrix-digest"},
            "operator": "Named Support Approver",
        })
        chosen, problems = currentstate._confirmed_current_attestations(
            [attestation], {"supportMatrix": "matrix-digest"}, "na",
            ("support-matrix-approval",), "Named Support Approver")
        self.assertEqual(problems, [])
        self.assertEqual(chosen["support-matrix-approval"], attestation)

        chosen, problems = currentstate._confirmed_current_attestations(
            [attestation], {"supportMatrix": "matrix-digest"}, "na",
            ("support-matrix-approval",), "Different Support Approver")
        self.assertEqual(chosen, {})
        self.assertTrue(any(
            "does not match support matrix approver" in problem
            for problem in problems), problems)


class TestManualEvidence(unittest.TestCase):
    @staticmethod
    def _arg(field, status="passed", evidence="Completed on candidate bytes"):
        value = copy.deepcopy(_manual_checks()[field])
        value.update({"status": status, "evidence": evidence})
        value.pop("operator")
        value.pop("operatorKind")
        value = json.dumps(value)
        return "--%s=%s" % (field, value)

    @staticmethod
    def _parse(args, operator="Reviewer", operator_kind="human"):
        return build.parse_manual_checks(
            args, MANUAL_FIELDS, operator, operator_kind,
            QA_SUPPORT_MATRIX, QA_API_PROBES)

    @staticmethod
    def _file_payload():
        payload = copy.deepcopy(_manual_checks())
        for evidence in payload.values():
            evidence.pop("operator")
            evidence.pop("operatorKind")
        return payload

    def test_record_qa_options_are_closed_and_mutually_exclusive(self):
        parsed = build.parse_record_qa_options([
            "--check-only", "--evidence-file=qa/manual.json"])
        self.assertTrue(parsed["checkOnly"])
        self.assertEqual(parsed["evidenceFile"], "qa/manual.json")
        self.assertEqual(parsed["manualArgs"], [])

        invalid = (
            ["--template", "--check-only"],
            ["--template", self._arg("ac11")],
            ["--evidence-file=qa/a.json", self._arg("ac11")],
            ["--evidence-file=qa/a.json", "--evidence-file=qa/b.json"],
            ["--template", "--template"],
            ["--check-only", "--check-only"],
            ["--evidence-file="],
        )
        for args in invalid:
            with self.subTest(args=args), self.assertRaises(SystemExit):
                build.parse_record_qa_options(args)

        duplicate = [self._arg(field) for field in MANUAL_FIELDS]
        duplicate.append(self._arg("ac11"))
        with self.assertRaisesRegex(SystemExit, "supplied more than once"):
            self._parse(duplicate)

    def test_pending_template_uses_live_policy_and_cannot_authorize(self):
        template = qaevidence.pending_manual_checks_template(
            QA_SUPPORT_MATRIX, QA_API_PROBES)
        self.assertEqual(set(template), set(MANUAL_FIELDS))
        self.assertEqual(
            [
                {key: result[key] for key in target}
                for result, target in zip(
                    template["ac11"]["targetResults"],
                    QA_SUPPORT_MATRIX["targets"])
            ],
            QA_SUPPORT_MATRIX["targets"])
        for result in template["ac13"]["targetResults"]:
            self.assertEqual(
                result["minimumViewport"],
                QA_SUPPORT_MATRIX["viewport"]["minimum"])
        self.assertEqual(
            sorted(template["ac15"]["probeResult"]["apis"]),
            QA_API_PROBES)
        encoded = json.dumps(template, sort_keys=True)
        self.assertNotIn('"passed"', encoded)
        self.assertNotIn('"operator"', encoded)
        self.assertNotIn('"operatorKind"', encoded)

        args = [
            "--%s=%s" % (field, json.dumps(template[field]))
            for field in MANUAL_FIELDS
        ]
        with self.assertRaisesRegex(SystemExit, "status is not 'passed'"):
            self._parse(args)

    def test_template_command_is_identity_free_and_read_only(self):
        model = SimpleNamespace(
            release_policy={}, support_matrix=QA_SUPPORT_MATRIX,
            api_policy={})
        with mock.patch.object(currentstate, "derive", return_value=(
                model, b"", {"reads": [], "lockDigest": "unused"})), \
                mock.patch.object(
                    build.acceptance, "release_profile_contract",
                    return_value=("technical-preview",
                                  TECHNICAL_PREVIEW_PROFILE)), \
                mock.patch.object(build.acceptance, "load_registry",
                                  return_value={}), \
                mock.patch.object(build.render, "api_probe_instruments",
                                  return_value={api: None
                                                for api in QA_API_PROBES}), \
                mock.patch.object(build, "operator_id",
                                  side_effect=AssertionError(
                                      "template requested identity")), \
                mock.patch.object(build, "load_planes",
                                  side_effect=AssertionError(
                                      "template loaded write planes")), \
                mock.patch("builtins.print") as printed:
            build.cmd_record_qa("na", ["--template"])
        output = json.loads(printed.call_args.args[0])
        self.assertEqual(set(output), set(MANUAL_FIELDS))

    def test_evidence_file_matches_inline_and_is_not_a_locked_input(self):
        payload = self._file_payload()
        with tempfile.TemporaryDirectory() as root:
            os.makedirs(os.path.join(root, "qa"))
            path = os.path.join(root, "qa", "manual.json")
            with open(path, "wb") as fh:
                fh.write(canon.canonical_json(payload))
            candidate_gateway = gateway.ContentGateway(root)
            before = candidate_gateway.lock()
            with mock.patch.object(build, "ROOT", root):
                file_args = build.manual_check_args_from_evidence_file(
                    "qa/manual.json", MANUAL_FIELDS)
            self.assertEqual(candidate_gateway.lock(), before)

        inline_args = [
            "--%s=%s" % (
                field,
                canon.canonical_json(payload[field]).decode("utf-8"))
            for field in MANUAL_FIELDS
        ]
        self.assertEqual(
            self._parse(file_args, "Reviewer", "model"),
            self._parse(inline_args, "Reviewer", "model"))

    def test_evidence_file_fails_closed_on_paths_and_bytes(self):
        payload = self._file_payload()
        with tempfile.TemporaryDirectory() as root:
            os.makedirs(os.path.join(root, "qa"))
            good = os.path.join(root, "qa", "manual.json")
            with open(good, "wb") as fh:
                fh.write(canon.canonical_json(payload))
            os.makedirs(os.path.join(root, "navigator", "dist"))
            terminal = os.path.join(root, "navigator", "dist", "manual.json")
            with open(terminal, "wb") as fh:
                fh.write(canon.canonical_json(payload))
            bad_utf8 = os.path.join(root, "qa", "bad-utf8.json")
            with open(bad_utf8, "wb") as fh:
                fh.write(b"{\xff}")
            duplicate = os.path.join(root, "qa", "duplicate.json")
            with open(duplicate, "wb") as fh:
                fh.write(b'{"ac11":{},"ac11":{}}')
            link = os.path.join(root, "qa", "link.json")
            try:
                os.symlink(good, link)
            except (OSError, NotImplementedError):
                link = None

            invalid = [
                os.path.abspath(good), "../qa/manual.json", "./qa/manual.json",
                "qa\\manual.json", "qa/missing.json",
                "navigator/dist/manual.json", "qa/bad-utf8.json",
                "qa/duplicate.json",
            ]
            if link is not None:
                invalid.append("qa/link.json")
            with mock.patch.object(build, "ROOT", root):
                for relpath in invalid:
                    with self.subTest(relpath=relpath), \
                            self.assertRaises(SystemExit):
                        build.manual_check_args_from_evidence_file(
                            relpath, MANUAL_FIELDS)

    def test_empty_record_qa_evidence_fails_closed(self):
        model = SimpleNamespace(
            release_policy={}, support_matrix=QA_SUPPORT_MATRIX,
            api_policy={})
        with mock.patch.object(currentstate, "derive", return_value=(
                model, b"", {"reads": [], "lockDigest": "unused"})), \
                mock.patch.object(
                    build.acceptance, "release_profile_contract",
                    return_value=("validated-release",
                                  VALIDATED_RELEASE_PROFILE)), \
                mock.patch.object(build.acceptance, "load_registry",
                                  return_value={}), \
                mock.patch.object(build.render, "api_probe_instruments",
                                  return_value={api: None
                                                for api in QA_API_PROBES}), \
                mock.patch.dict(os.environ, {
                    "NAV_OPERATOR": "codex:test:empty",
                    "NAV_OPERATOR_KIND": "model",
                }, clear=True), \
                self.assertRaisesRegex(SystemExit, "missing"):
            build.cmd_record_qa("na", [])

    def test_record_qa_is_deferred_for_the_technical_preview(self):
        model = SimpleNamespace(
            release_policy={}, support_matrix=QA_SUPPORT_MATRIX,
            api_policy={})
        with mock.patch.object(currentstate, "derive", return_value=(
                model, b"", {"reads": [], "lockDigest": "unused"})), \
                mock.patch.object(
                    build.acceptance, "release_profile_contract",
                    return_value=("technical-preview",
                                  TECHNICAL_PREVIEW_PROFILE)), \
                mock.patch.object(build.acceptance, "load_registry",
                                  return_value={}), \
                mock.patch.object(build.render, "api_probe_instruments",
                                  return_value={api: None
                                                for api in QA_API_PROBES}), \
                mock.patch.object(
                    build, "operator_id",
                    side_effect=AssertionError(
                        "deferred preview QA requested an identity")), \
                self.assertRaisesRegex(SystemExit, "deferred.*technical-preview"):
            build.cmd_record_qa("na", [])

    def test_check_only_validates_inline_and_file_without_append(self):
        payload = self._file_payload()
        inline_args = [
            "--%s=%s" % (
                field,
                canon.canonical_json(payload[field]).decode("utf-8"))
            for field in MANUAL_FIELDS
        ]
        matrix_bytes = canon.canonical_json(QA_SUPPORT_MATRIX)
        candidate = b"candidate bytes"
        lock = {
            "reads": [],
            "lockDigest": canon.bytes_digest(b"content lock"),
        }
        qa_lock = {
            "reads": [],
            "lockDigest": canon.bytes_digest(b"qa input lock"),
        }
        model = SimpleNamespace(
            release_policy={}, support_matrix=QA_SUPPORT_MATRIX,
            support_matrix_bytes=matrix_bytes, api_policy={},
            edition={"editionId": "na", "artifactName": "artifact.html"},
            strings={"counselLegend": "Approved legend"})
        artifact_gateway = mock.Mock()
        artifact_gateway.read.return_value = candidate
        verification_gateway = mock.Mock()
        verification_gateway.read_all.return_value = []
        chosen = {
            "support-matrix-approval": {"digest": "support-attestation"},
            "legend-approval": {"digest": "legend-attestation"},
        }
        authorization = mock.Mock(return_value=[])

        with tempfile.TemporaryDirectory() as root:
            os.makedirs(os.path.join(root, "qa"))
            with open(os.path.join(root, "qa", "manual.json"), "wb") as fh:
                fh.write(canon.canonical_json(payload))
            with mock.patch.object(build, "ROOT", root), \
                    mock.patch.object(currentstate, "derive", return_value=(
                        model, candidate, lock)), \
                    mock.patch.object(
                        build.acceptance, "release_profile_contract",
                        return_value=("validated-release",
                                      VALIDATED_RELEASE_PROFILE)), \
                    mock.patch.object(build.acceptance, "load_registry",
                                      return_value={}), \
                    mock.patch.object(build.render, "api_probe_instruments",
                                      return_value={api: None
                                                    for api in QA_API_PROBES}), \
                    mock.patch.object(build, "load_planes", return_value={}), \
                    mock.patch.object(build.os.path, "exists",
                                      return_value=True), \
                    mock.patch.object(build.gateway, "ArtifactGateway",
                                      return_value=artifact_gateway), \
                    mock.patch.object(build.gateway, "VerificationGateway",
                                      return_value=verification_gateway), \
                    mock.patch.object(currentstate, "qa_input_lock",
                                      return_value=qa_lock), \
                    mock.patch.object(currentstate, "current_side_digests",
                                      return_value={
                                          "legendWording":
                                              canon.text_digest(
                                                  "Approved legend")}), \
                    mock.patch.object(currentstate, "_required_attestation_types",
                                      return_value=tuple(chosen)), \
                    mock.patch.object(
                        currentstate, "_confirmed_current_attestations",
                        return_value=(chosen, [])), \
                    mock.patch.object(currentstate, "qa_authorization_problems",
                                      authorization), \
                    mock.patch.dict(os.environ, {
                        "NAV_OPERATOR": "codex:test:check-only",
                        "NAV_OPERATOR_KIND": "model",
                    }, clear=True), \
                    mock.patch("builtins.print") as printed:
                build.cmd_record_qa(
                    "na", ["--check-only"] + inline_args)
                build.cmd_record_qa("na", [
                    "--check-only", "--evidence-file=qa/manual.json"])
                self.assertEqual(authorization.call_count, 2)
                self.assertEqual(printed.call_count, 2)
                for call in authorization.call_args_list:
                    envelope = call.args[0]
                    self.assertEqual(envelope["kind"], "qa-record")
                    self.assertEqual(
                        envelope["record"]["operator"],
                        "codex:test:check-only")
                    self.assertEqual(
                        envelope["record"]["operatorKind"], "model")
                verification_gateway.append.assert_not_called()

                authorization.return_value = ["constructed record defect"]
                with self.assertRaisesRegex(
                        SystemExit, "constructed authorization"):
                    build.cmd_record_qa("na", inline_args)
                verification_gateway.append.assert_not_called()

    def test_registry_drives_the_required_manual_fields(self):
        with open(os.path.join(ROOT, "navigator", "schema", "acceptance.json"),
                  encoding="utf-8") as fh:
            registry = json.load(fh)
        self.assertEqual(acceptance.manual_qa_fields(registry), MANUAL_FIELDS)

    def test_registry_cannot_delete_criteria_or_manual_requirements(self):
        with open(os.path.join(ROOT, "navigator", "schema", "acceptance.json"),
                  encoding="utf-8") as fh:
            registry = json.load(fh)
        missing = copy.deepcopy(registry)
        missing["criteria"] = []
        with self.assertRaisesRegex(acceptance.AcceptanceError,
                                    "criterion set"):
            acceptance.manual_qa_fields(missing)

        weakened = copy.deepcopy(registry)
        weakened["criteria"][10]["enforcedBy"]["qaRecordFields"] = []
        with self.assertRaisesRegex(acceptance.AcceptanceError,
                                    "QA grammar"):
            acceptance.manual_qa_fields(weakened)

        drifted_version = copy.deepcopy(registry)
        drifted_version["runner"]["runnerVersion"] = "2"
        with self.assertRaisesRegex(acceptance.AcceptanceError,
                                    "runner is malformed"):
            acceptance.manual_qa_fields(drifted_version)

    def test_parser_records_explicit_operator_identity_and_kind(self):
        checks = self._parse(
            [self._arg(field) for field in MANUAL_FIELDS],
            "codex:gpt-5.6-sol:run-test-001", "model")
        self.assertEqual(set(checks), set(MANUAL_FIELDS))
        for evidence in checks.values():
            self.assertEqual(evidence["status"], "passed")
            self.assertEqual(
                evidence["operator"], "codex:gpt-5.6-sol:run-test-001")
            self.assertEqual(evidence["operatorKind"], "model")

    def test_parser_rejects_legacy_missing_and_pending_evidence(self):
        with self.assertRaisesRegex(SystemExit, "valid JSON"):
            self._parse(["--ac11=legacy prose"])
        with self.assertRaisesRegex(SystemExit, "missing"):
            self._parse([self._arg("ac11")])
        args = [self._arg(field) for field in MANUAL_FIELDS]
        args[-1] = self._arg("ac15", evidence="Browser pass pending")
        with self.assertRaisesRegex(SystemExit, "pending"):
            self._parse(args)

    def test_parser_rejects_incomplete_misaligned_and_unversioned_results(self):
        payloads = {
            field: copy.deepcopy(_manual_checks()[field])
            for field in MANUAL_FIELDS
        }
        for payload in payloads.values():
            payload.pop("operator")
            payload.pop("operatorKind")
        payloads["ac11"]["targetResults"].pop()
        args = ["--%s=%s" % (field, json.dumps(payloads[field]))
                for field in MANUAL_FIELDS]
        with self.assertRaisesRegex(SystemExit, "every current support target"):
            self._parse(args)

        payloads = {
            field: copy.deepcopy(_manual_checks()[field])
            for field in MANUAL_FIELDS
        }
        for payload in payloads.values():
            payload.pop("operator")
            payload.pop("operatorKind")
        payloads["ac13"]["targetResults"][0]["browser"] = "Wrong browser"
        args = ["--%s=%s" % (field, json.dumps(payloads[field]))
                for field in MANUAL_FIELDS]
        with self.assertRaisesRegex(SystemExit, "current support matrix"):
            self._parse(args)

        checks = _manual_checks()
        problems = qaevidence.manual_check_problems(
            checks, MANUAL_FIELDS, support_matrix=QA_SUPPORT_MATRIX,
            api_probe_apis=QA_API_PROBES, operator="QA Reviewer",
            operator_kind="human", manual_evidence_version=None)
        self.assertTrue(any("manualEvidenceVersion" in problem
                            for problem in problems), problems)

    def test_manual_evidence_v3_requires_per_page_print_checks(self):
        current = _manual_checks()
        common = {
            "support_matrix": QA_SUPPORT_MATRIX,
            "api_probe_apis": QA_API_PROBES,
            "operator": "QA Reviewer",
            "operator_kind": "human",
        }
        self.assertEqual(qaevidence.MANUAL_EVIDENCE_VERSION, "3")
        self.assertEqual(qaevidence.manual_check_problems(
            current, MANUAL_FIELDS, manual_evidence_version="3", **common),
            [])

        old_version = qaevidence.manual_check_problems(
            current, MANUAL_FIELDS, manual_evidence_version="2", **common)
        self.assertTrue(any("manualEvidenceVersion must be '3'" in problem
                            for problem in old_version), old_version)

        old_presence_checks = copy.deepcopy(current)
        print_checks = old_presence_checks["ac12"]["printResult"]["checks"]
        print_checks["disclaimerPresent"] = print_checks.pop(
            "disclaimerOnEveryPage")
        print_checks["legendPresent"] = print_checks.pop("legendOnEveryPage")
        old_fields = qaevidence.manual_check_problems(
            old_presence_checks, MANUAL_FIELDS,
            manual_evidence_version="3", **common)
        self.assertTrue(any("ac12 printResult checks must be exactly" in problem
                            for problem in old_fields), old_fields)
        self.assertTrue(any("disclaimerOnEveryPage" in problem and
                            "legendOnEveryPage" in problem
                            for problem in old_fields), old_fields)

    def test_actual_versions_and_traversal_chords_must_meet_live_targets(self):
        mutations = []
        below_browser = _manual_checks()
        below_browser["ac11"]["targetResults"][0][
            "browserVersion"] = "Chrome 106.0"
        mutations.append((below_browser, "below Chrome"))

        wrong_browser = _manual_checks()
        wrong_browser["ac13"]["targetResults"][0][
            "browserVersion"] = "Firefox 999.0"
        mutations.append((wrong_browser, "identify Chrome"))

        wrong_os = _manual_checks()
        wrong_os["ac13"]["targetResults"][1][
            "osVersion"] = "macOS 14.0"
        mutations.append((wrong_os, "Windows 11"))

        stale_at = _manual_checks()
        at_index = next(index for index, target in enumerate(
            QA_SUPPORT_MATRIX["targets"]) if target["at"] != "none")
        stale_at["ac11"]["targetResults"][at_index][
            "atVersion"] = "NVDA 2023.3"
        mutations.append((stale_at, "below NVDA"))

        wrong_at = _manual_checks()
        wrong_at["ac13"]["targetResults"][at_index][
            "atVersion"] = "Other AT 2026"
        mutations.append((wrong_at, "canonical NVDA"))

        wrong_chord = _manual_checks()
        wrong_chord["ac11"]["targetResults"][0][
            "traversalChord"] = "Option-Tab/Option-Shift-Tab"
        mutations.append((wrong_chord, "outside Safari/macOS"))

        unexplained_safari = _manual_checks()
        safari_index = next(index for index, target in enumerate(
            QA_SUPPORT_MATRIX["targets"])
            if target["browser"].startswith("Safari "))
        unexplained_safari["ac11"]["targetResults"][safari_index][
            "traversalConfiguration"] = "Default browser preferences"
        mutations.append((unexplained_safari, "Keyboard Navigation"))

        for checks, expected in mutations:
            with self.subTest(expected=expected):
                problems = qaevidence.manual_check_problems(
                    checks, MANUAL_FIELDS,
                    support_matrix=QA_SUPPORT_MATRIX,
                    api_probe_apis=QA_API_PROBES,
                    operator="QA Reviewer", operator_kind="human",
                    manual_evidence_version=qaevidence.MANUAL_EVIDENCE_VERSION)
                self.assertTrue(any(expected in problem
                                    for problem in problems), problems)

    def test_target_results_reject_extra_duplicate_and_reordered_rows(self):
        mutations = []
        extra = _manual_checks()
        extra["ac11"]["targetResults"].append(copy.deepcopy(
            extra["ac11"]["targetResults"][-1]))
        mutations.append((extra, "every current support target"))

        duplicate = _manual_checks()
        duplicate["ac13"]["targetResults"][1] = copy.deepcopy(
            duplicate["ac13"]["targetResults"][0])
        mutations.append((duplicate, "current support matrix"))

        reordered = _manual_checks()
        reordered["ac11"]["targetResults"][0], \
            reordered["ac11"]["targetResults"][1] = (
                reordered["ac11"]["targetResults"][1],
                reordered["ac11"]["targetResults"][0])
        mutations.append((reordered, "current support matrix"))

        for checks, expected in mutations:
            with self.subTest(expected=expected):
                problems = qaevidence.manual_check_problems(
                    checks, MANUAL_FIELDS,
                    support_matrix=QA_SUPPORT_MATRIX,
                    api_probe_apis=QA_API_PROBES,
                    operator="QA Reviewer", operator_kind="human",
                    manual_evidence_version=qaevidence.MANUAL_EVIDENCE_VERSION)
                self.assertTrue(any(expected in problem
                                    for problem in problems), problems)

    def test_environment_grammars_reject_annotations_ua_and_mismatches(self):
        safari_index = next(index for index, target in enumerate(
            QA_SUPPORT_MATRIX["targets"])
            if target["browser"].startswith("Safari "))
        at_index = next(index for index, target in enumerate(
            QA_SUPPORT_MATRIX["targets"]) if target["at"] != "none")
        mutations = []

        annotated = _manual_checks()
        annotated["ac11"]["targetResults"][0][
            "browserVersion"] = "Chrome 126 (not tested)"
        mutations.append((annotated, "failure language"))

        for value in (
                "Safari/605.1.15",
                "Version/16.6 Safari/605.1.15"):
            ua_engine = _manual_checks()
            ua_engine["ac13"]["targetResults"][safari_index][
                "browserVersion"] = value
            mutations.append((ua_engine, "canonical browser product"))

        engine_as_product = _manual_checks()
        engine_as_product["ac11"]["targetResults"][safari_index][
            "browserVersion"] = "Safari 605.1.15"
        mutations.append((engine_as_product, "Safari product version"))

        annotated_os = _manual_checks()
        annotated_os["ac13"]["targetResults"][0][
            "osVersion"] = "macOS 14.0 (not tested)"
        mutations.append((annotated_os, "osVersion contains"))

        annotated_at = _manual_checks()
        annotated_at["ac11"]["targetResults"][at_index][
            "atVersion"] = "NVDA 2024.4 (not tested)"
        mutations.append((annotated_at, "atVersion contains"))

        arbitrary_print = _manual_checks()
        arbitrary_print["ac12"]["printResult"]["browser"] = "x"
        arbitrary_print["ac12"]["printResult"]["browserVersion"] = "x"
        mutations.append((arbitrary_print, "known browser family"))

        mismatched_probe = _manual_checks()
        mismatched_probe["ac15"]["probeResult"].update({
            "browser": "Chrome", "browserVersion": "Firefox 147.0.1",
        })
        mutations.append((mismatched_probe, "does not identify Chrome"))

        unsupported_pair = _manual_checks()
        unsupported_pair["ac12"]["printResult"].update({
            "browser": "Safari", "browserVersion": "Safari 26.5.2",
            "os": "Windows", "osVersion": "Windows 11 24H2",
        })
        mutations.append((unsupported_pair, "current no-AT support target"))

        stale_print = _manual_checks()
        stale_print["ac12"]["printResult"][
            "browserVersion"] = "Safari 16.6"
        mutations.append((stale_print, "below Safari"))

        stale_probe_os = _manual_checks()
        stale_probe_os["ac15"]["probeResult"][
            "osVersion"] = "macOS 12.7.6"
        mutations.append((stale_probe_os, "below macOS"))

        ua_windows = _manual_checks()
        ua_windows["ac15"]["probeResult"].update({
            "browser": "Chrome", "browserVersion": "Chrome 150.0.1",
            "os": "Windows", "osVersion": "Windows NT 10.0",
        })
        mutations.append((ua_windows, "canonical Windows 11"))

        annotated_environment = _manual_checks()
        annotated_environment["ac15"]["probeResult"][
            "os"] = "macOS (not tested)"
        mutations.append((annotated_environment, "failure language"))

        for checks, expected in mutations:
            with self.subTest(expected=expected):
                problems = qaevidence.manual_check_problems(
                    checks, MANUAL_FIELDS,
                    support_matrix=QA_SUPPORT_MATRIX,
                    api_probe_apis=QA_API_PROBES,
                    operator="QA Reviewer", operator_kind="human",
                    manual_evidence_version=qaevidence.MANUAL_EVIDENCE_VERSION)
                self.assertTrue(any(expected in problem
                                    for problem in problems), problems)

    def test_exact_print_probe_and_authority_payloads_fail_closed(self):
        mutations = []
        bad_print = _manual_checks()
        bad_print["ac12"]["printResult"]["checks"][
            "claimsReadable"] = "failed"
        mutations.append((bad_print, "claimsReadable"))

        bad_probe = _manual_checks()
        bad_probe["ac15"]["probeResult"]["apis"].pop(QA_API_PROBES[0])
        mutations.append((bad_probe, "current probed hooks"))

        used_network = _manual_checks()
        used_network["ac15"]["probeResult"]["networkRequests"] = [
            "https://example.invalid"]
        mutations.append((used_network, "networkRequests"))

        failed_text = _manual_checks()
        failed_text["ac11"]["evidence"] = \
            "Failed on every required browser row"
        mutations.append((failed_text, "failure language"))

        tool_evidence = _manual_checks()
        tool_evidence["ac13"]["operatorKind"] = "tool"
        mutations.append((tool_evidence, "release-authoritative"))

        missing_identity = _manual_checks()
        missing_identity["ac15"]["operator"] = " "
        mutations.append((missing_identity, "identified operator"))

        for checks, expected in mutations:
            with self.subTest(expected=expected):
                problems = qaevidence.manual_check_problems(
                    checks, MANUAL_FIELDS,
                    support_matrix=QA_SUPPORT_MATRIX,
                    api_probe_apis=QA_API_PROBES,
                    operator="QA Reviewer", operator_kind="human",
                    manual_evidence_version=qaevidence.MANUAL_EVIDENCE_VERSION)
                self.assertTrue(any(expected in problem
                                    for problem in problems), problems)


class TestQaInputLock(unittest.TestCase):
    def _model(self, root, first, second):
        corpora = {
            "qa-priority": {
                "role": "qa-source",
                "visibility": "internal",
                "versionBindings": {"NA": "NA-2026-07-22-v4"},
                "primary": "qa/priority.txt",
                "files": {
                    "qa/priority.txt": canon.bytes_digest(first),
                    "qa/priority-notes.txt": canon.bytes_digest(second),
                },
            },
        }
        registry_path = "qa/registry.json"
        registry_digest = canon.bytes_digest(
            canon.canonical_json({"registryVersion": "1",
                                  "corpora": corpora}))
        qa_registry = SimpleNamespace(
            corpora=corpora,
            gw=SimpleNamespace(read_log={registry_path: registry_digest}))
        return SimpleNamespace(
            gw=gateway.ContentGateway(root),
            edition={
                "qaRegistry": registry_path,
                "strategyPrefix": "NA",
                "claimSetVersion": "NA-2026-07-22-v4",
                "qaSources": {
                    "priorityMap": "qa-priority", "crosswalk": None}},
            _qa_registry=qa_registry,
        )

    def test_lock_reads_all_pins_and_binds_candidate(self):
        with tempfile.TemporaryDirectory() as root:
            os.makedirs(os.path.join(root, "qa"))
            first = b"priority map\n"
            second = b"review notes\n"
            with open(os.path.join(root, "qa", "priority.txt"), "wb") as fh:
                fh.write(first)
            with open(os.path.join(root, "qa", "priority-notes.txt"),
                      "wb") as fh:
                fh.write(second)
            m = self._model(root, first, second)
            first_lock = currentstate.qa_input_lock(m, "candidate-a", "content-lock")
            again = currentstate.qa_input_lock(m, "candidate-a", "content-lock")
            changed = currentstate.qa_input_lock(m, "candidate-b", "content-lock")
            self.assertEqual(first_lock, again)
            self.assertEqual(len(first_lock["reads"]), 2)
            self.assertEqual(first_lock["candidateDigest"], "candidate-a")
            self.assertNotEqual(first_lock["lockDigest"],
                                changed["lockDigest"])

    def test_lock_rejects_registry_pin_drift(self):
        with tempfile.TemporaryDirectory() as root:
            os.makedirs(os.path.join(root, "qa"))
            first = b"priority map\n"
            second = b"review notes\n"
            with open(os.path.join(root, "qa", "priority.txt"), "wb") as fh:
                fh.write(b"tampered\n")
            with open(os.path.join(root, "qa", "priority-notes.txt"),
                      "wb") as fh:
                fh.write(second)
            m = self._model(root, first, second)
            with self.assertRaisesRegex(SystemExit, "drifted"):
                currentstate.qa_input_lock(m, "candidate", "content-lock")

    def test_bundle_context_is_derived_from_live_qa_and_support_inputs(self):
        binding = {
            "sealed": "current.html",
            "sealedDigest": canon.bytes_digest(b"current candidate"),
            "lockDigest": canon.bytes_digest(b"current content lock"),
            "declaredReleaseTimestamp": "2026-07-22T00:00:00Z",
        }
        expected_lock = {"lockDigest": canon.bytes_digest(b"current QA")}
        edition_model = SimpleNamespace(
            edition={
                "artifactName": binding["sealed"],
                "declaredReleaseTimestamp":
                    binding["declaredReleaseTimestamp"],
            },
            support_matrix={
                "approver": "Current Support Owner",
                "targets": copy.deepcopy(QA_SUPPORT_MATRIX["targets"]),
                "viewport": copy.deepcopy(QA_SUPPORT_MATRIX["viewport"]),
            },
            api_policy={})
        with mock.patch.object(
                currentstate, "derive", return_value=(
                    edition_model, b"current candidate",
                    {"lockDigest": binding["lockDigest"]})), \
                mock.patch.object(
                    currentstate, "qa_input_lock", return_value=expected_lock) as lock, \
                mock.patch.object(
                    build.render, "api_probe_instruments",
                    return_value={"document.cookie": "cookie-write"}):
            context = currentstate.bundle_qa_authorization_context(
                {"editions": ["na"]}, {"na": binding})
        self.assertEqual(context, {"na": {
            "qaInputLock": expected_lock,
            "supportMatrixApprover": "Current Support Owner",
            "supportMatrixTargets": QA_SUPPORT_MATRIX["targets"],
            "supportMatrixViewport": QA_SUPPORT_MATRIX["viewport"],
            "apiProbeApis": ["document.cookie"],
        }})
        lock.assert_called_once_with(
            edition_model, binding["sealedDigest"], binding["lockDigest"])

        drifted = copy.deepcopy(binding)
        drifted["sealedDigest"] = canon.bytes_digest(b"earlier candidate")
        with mock.patch.object(
                currentstate, "derive", return_value=(
                    edition_model, b"current candidate",
                    {"lockDigest": binding["lockDigest"]})), \
                mock.patch.object(
                    build.render, "api_probe_instruments",
                    return_value={"document.cookie": "cookie-write"}):
            with self.assertRaisesRegex(
                    build.model.ModelError,
                    "changed while deriving QA authorization context"):
                currentstate.bundle_qa_authorization_context(
                    {"editions": ["na"]}, {"na": drifted})


class TestReleaseEvidence(unittest.TestCase):
    def _fixture(self):
        sides = {
            "claimSet": "claim",
            "gateInventory": "inventory",
            "relationSet": "relations",
            "priorityMap": "priority",
            "legendWording": "legend",
            "supportMatrix": "matrix",
        }
        specs = {
            "inventory-completeness": ("na", {
                "claimSet": "claim", "gateInventory": "inventory"}),
            "qa-priority-map": ("na", {
                "relationSet": "relations", "priorityMap": "priority"}),
            "legend-approval": (None, {"legendWording": "legend"}),
            "support-matrix-approval": (None, {"supportMatrix": "matrix"}),
        }
        attestations = []
        for atype, (edition, att_sides) in specs.items():
            attestations.append({
                "digest": "digest-" + atype,
                "record": {
                    "type": atype,
                    "edition": edition,
                    "sides": att_sides,
                    "note": "Human review completed",
                    "approvalStatus": "passed",
                    "operator": ("Support Owner" if atype ==
                                 "support-matrix-approval" else
                                 "Attesting Reviewer"),
                    "operatorKind": "human",
                    "producerCommand":
                        recordprovenance.ATTESTATION_PRODUCER_COMMAND,
                },
            })
        refs = sorted(a["digest"] for a in attestations)
        content_lock = {"reads": [{"path": "source", "digest": "source"}],
                        "lockDigest": "content-lock"}
        qa_lock = {"lockType": "internal-qa-inputs",
                   "candidateDigest": "candidate", "lockDigest": "qa-lock"}
        checks = _manual_checks()
        support_matrix = copy.deepcopy(QA_SUPPORT_MATRIX)
        support_matrix["approver"] = "Support Owner"
        record = {
            "releaseProfile": "validated-release",
            "edition": "na",
            "candidateDigest": "candidate",
            "lockDigest": "content-lock",
            "contentLock": content_lock["reads"],
            "qaInputLock": qa_lock,
            "reproductionDiagnostics": {
                "interpreter": "test", "platform": "test",
                "locale": "C", "unicodedata": "test",
            },
            "attestations": refs,
            "supportMatrix": {
                "digest": "matrix",
                "approver": "Support Owner",
                "approvalAttestation": "digest-support-matrix-approval",
            },
            "legendApproval": {
                "digest": "legend",
                "approvalAttestation": "digest-legend-approval",
            },
            "manualEvidenceVersion": qaevidence.MANUAL_EVIDENCE_VERSION,
            "manualChecks": checks,
            "approvalStatus": "passed",
            "operator": "QA Reviewer",
            "operatorKind": "human",
        }
        return ({"digest": "qa-digest", "record": record}, content_lock,
                qa_lock, support_matrix, attestations, sides)

    def _problems(self, qa, content_lock, qa_lock, matrix, atts, sides):
        return currentstate.qa_authorization_problems(
            qa, "candidate", content_lock, qa_lock, matrix, QA_API_PROBES,
            "legend", atts, sides, "na",
            ("inventory-completeness", "qa-priority-map",
             "legend-approval", "support-matrix-approval"),
            MANUAL_FIELDS, "validated-release")

    def test_complete_human_evidence_authorizes_release(self):
        fixture = self._fixture()
        self.assertEqual(self._problems(*fixture), [])

    def test_qa_record_is_explicitly_scoped_to_validated_release(self):
        fixture = self._fixture()
        self.assertEqual(fixture[0]["record"]["releaseProfile"],
                         "validated-release")
        for bad_profile in (None, "technical-preview", "preview"):
            with self.subTest(release_profile=bad_profile):
                qa = copy.deepcopy(fixture[0])
                if bad_profile is None:
                    qa["record"].pop("releaseProfile")
                else:
                    qa["record"]["releaseProfile"] = bad_profile
                problems = self._problems(qa, *fixture[1:])
                self.assertTrue(any(
                    "current profile" in problem
                    for problem in problems), problems)

    def test_current_qa_selection_prefers_human_then_digest(self):
        content_lock = {"lockDigest": "current-lock", "reads": []}
        edition = SimpleNamespace(
            edition={"editionId": "na"}, release_policy={},
            support_matrix_bytes=b"{}",
            api_policy={},
            strings={"counselLegend": "legend"},
            gw=SimpleNamespace(root=ROOT, byte_source=None))

        def qa(digest, kind):
            return {"kind": "qa-record", "digest": digest, "record": {
                "edition": "na", "candidateDigest": "candidate",
                "lockDigest": "current-lock", "operatorKind": kind,
                "releaseProfile": "validated-release",
            }}

        records = [qa("000-model", "model"),
                   qa("bbb-human", "human"),
                   qa("aaa-human", "human")]
        with mock.patch.object(currentstate, "current_side_digests",
                               return_value={}), \
                mock.patch.object(build.acceptance, "load_registry",
                                  return_value={}), \
                mock.patch.object(
                    build.acceptance, "release_profile_contract",
                    return_value=("validated-release",
                                  VALIDATED_RELEASE_PROFILE)), \
                mock.patch.object(
                    build.recordprovenance,
                    "current_record_format_problems", return_value=[]), \
                mock.patch.object(currentstate, "qa_input_lock", return_value={}), \
                mock.patch.object(build.canon, "parse_json", return_value={}), \
                mock.patch.object(build.render, "api_probe_instruments",
                                  return_value={}), \
                mock.patch.object(currentstate, "qa_authorization_problems",
                                  return_value=[]):
            valid, rejected = currentstate.current_authorized_qa_records(
                edition, "candidate", content_lock, records, [])
        self.assertEqual(rejected, [])
        self.assertEqual(
            [record["digest"] for record in valid],
            ["aaa-human", "bbb-human", "000-model"])

    def test_current_qa_selection_reports_absent_current_binding(self):
        content_lock = {"lockDigest": "current-lock", "reads": []}
        edition = SimpleNamespace(
            edition={"editionId": "na"}, release_policy={},
            support_matrix_bytes=b"{}", api_policy={},
            strings={"counselLegend": "legend"},
            gw=SimpleNamespace(root=ROOT, byte_source=None))
        stale = [{"kind": "qa-record", "digest": "old-qa", "record": {
            "edition": "na", "candidateDigest": "old-candidate",
            "lockDigest": "old-lock", "operatorKind": "model",
            "releaseProfile": "validated-release",
        }}]
        with mock.patch.object(currentstate, "current_side_digests",
                               return_value={}), \
                mock.patch.object(build.acceptance, "load_registry",
                                  return_value={}), \
                mock.patch.object(
                    build.acceptance, "release_profile_contract",
                    return_value=("validated-release",
                                  VALIDATED_RELEASE_PROFILE)), \
                mock.patch.object(
                    build.recordprovenance,
                    "current_record_format_problems", return_value=[]), \
                mock.patch.object(currentstate, "qa_input_lock", return_value={}), \
                mock.patch.object(build.canon, "parse_json", return_value={}), \
                mock.patch.object(build.render, "api_probe_instruments",
                                  return_value={}):
            valid, rejected = currentstate.current_authorized_qa_records(
                edition, "candidate", content_lock, stale, [])
        self.assertEqual(valid, [])
        self.assertEqual(rejected, [("<current-binding>", [
            "no qa-record matches and authorizes the current edition, "
            "profile, candidate digest, and content-input lock"
        ])])

    def test_profile_switch_preserves_same_schema_qa_as_superseded_evidence(self):
        content_lock = {"lockDigest": "current-lock", "reads": []}
        edition = SimpleNamespace(
            edition={"editionId": "na"}, release_policy={},
            support_matrix_bytes=b"{}", api_policy={},
            strings={"counselLegend": "legend"},
            gw=SimpleNamespace(root=ROOT, byte_source=None))
        prior_profile = [{
            "kind": "qa-record", "digest": "validated-evidence",
            "record": {
                "edition": "na", "candidateDigest": "candidate",
                "lockDigest": "current-lock", "operatorKind": "human",
                "releaseProfile": "validated-release",
            },
        }]
        with mock.patch.object(currentstate, "current_side_digests",
                               return_value={}), \
                mock.patch.object(build.acceptance, "load_registry",
                                  return_value={}), \
                mock.patch.object(
                    build.acceptance, "release_profile_contract",
                    return_value=("technical-preview",
                                  TECHNICAL_PREVIEW_PROFILE)), \
                mock.patch.object(
                    build.recordprovenance,
                    "current_record_format_problems", return_value=[]), \
                mock.patch.object(currentstate, "qa_input_lock", return_value={}), \
                mock.patch.object(build.canon, "parse_json", return_value={}), \
                mock.patch.object(build.render, "api_probe_instruments",
                                  return_value={}), \
                mock.patch.object(
                    currentstate, "qa_authorization_problems",
                    side_effect=AssertionError(
                        "superseded evidence was re-authorized")):
            valid, rejected = currentstate.current_authorized_qa_records(
                edition, "candidate", content_lock, prior_profile, [])
        self.assertEqual(valid, [])
        self.assertEqual(rejected, [("<current-binding>", [
            "no qa-record matches and authorizes the current edition, "
            "profile, candidate digest, and content-input lock"
        ])])

    def test_complete_identified_model_evidence_authorizes_release(self):
        fixture = list(self._fixture())
        qa = copy.deepcopy(fixture[0])
        identity = "codex:gpt-5.6-sol:run-test-001"
        qa["record"].update({
            "operator": identity, "operatorKind": "model"})
        for evidence in qa["record"]["manualChecks"].values():
            evidence.update({
                "operator": identity, "operatorKind": "model"})
        attestations = copy.deepcopy(fixture[4])
        for attestation in attestations:
            attestation["record"].update({
                "operator": identity, "operatorKind": "model"})
        qa["record"]["supportMatrix"]["approver"] = identity
        fixture[3]["approver"] = identity
        fixture[0] = qa
        fixture[4] = attestations
        self.assertEqual(self._problems(*fixture), [])
        self.assertEqual(qa["record"]["operator"], identity)
        self.assertEqual(qa["record"]["releaseProfile"],
                         "validated-release")
        self.assertEqual(qa["record"]["candidateDigest"], "candidate")
        self.assertEqual(qa["record"]["lockDigest"], "content-lock")
        self.assertEqual(qa["record"]["qaInputLock"], fixture[2])

    def test_legacy_pending_and_nonauthoritative_evidence_cannot_authorize(self):
        fixture = self._fixture()
        qa = copy.deepcopy(fixture[0])
        qa["record"]["manualChecks"]["ac11"] = "legacy prose"
        self.assertTrue(any("structured" in p
                            for p in self._problems(qa, *fixture[1:])))

        fixture = self._fixture()
        qa = copy.deepcopy(fixture[0])
        qa["record"]["manualChecks"]["ac12"]["status"] = "pending"
        self.assertTrue(any("status" in p
                            for p in self._problems(qa, *fixture[1:])))

        fixture = self._fixture()
        atts = copy.deepcopy(fixture[4])
        atts[-1]["record"]["operatorKind"] = "tool"
        problems = self._problems(
            fixture[0], fixture[1], fixture[2], fixture[3], atts, fixture[5])
        self.assertTrue(any("operatorKind" in p for p in problems), problems)

        for bad_kind in (None, "tool", "automation"):
            with self.subTest(operator_kind=bad_kind):
                fixture = self._fixture()
                qa = copy.deepcopy(fixture[0])
                if bad_kind is None:
                    qa["record"].pop("operatorKind")
                else:
                    qa["record"]["operatorKind"] = bad_kind
                self.assertTrue(any(
                    "operatorKind" in problem for problem in
                    self._problems(qa, *fixture[1:])))

        fixture = self._fixture()
        qa = copy.deepcopy(fixture[0])
        qa["record"]["candidateDigest"] = "stale-candidate"
        self.assertTrue(any(
            "candidate digest is not current" in problem for problem in
            self._problems(qa, *fixture[1:])))

        fixture = self._fixture()
        qa = copy.deepcopy(fixture[0])
        qa["record"]["operator"] = " "
        self.assertTrue(any(
            "identified operator" in problem for problem in
            self._problems(qa, *fixture[1:])))

    def test_nested_manual_kind_must_match_qa_approval(self):
        fixture = self._fixture()
        qa = copy.deepcopy(fixture[0])
        qa["record"]["manualChecks"]["ac11"]["operatorKind"] = "model"
        problems = self._problems(qa, *fixture[1:])
        self.assertTrue(any("does not match" in p for p in problems), problems)

    def test_support_matrix_approval_operator_must_match_named_approver(self):
        fixture = self._fixture()
        attestations = copy.deepcopy(fixture[4])
        support = next(
            attestation for attestation in attestations
            if attestation["record"]["type"] == "support-matrix-approval")
        support["record"]["operator"] = "Different Support Reviewer"
        problems = self._problems(
            fixture[0], fixture[1], fixture[2], fixture[3],
            attestations, fixture[5])
        self.assertTrue(any(
            "does not match support matrix approver" in problem
            for problem in problems), problems)

    def test_support_matrix_approver_identity_is_not_evidence_prose(self):
        fixture = list(self._fixture())
        identity = "qa-failure-reviewer@example.test"
        qa = copy.deepcopy(fixture[0])
        qa["record"]["supportMatrix"]["approver"] = identity
        matrix = copy.deepcopy(fixture[3])
        matrix["approver"] = identity
        attestations = copy.deepcopy(fixture[4])
        support = next(
            attestation for attestation in attestations
            if attestation["record"]["type"] == "support-matrix-approval")
        support["record"]["operator"] = identity
        fixture[0] = qa
        fixture[3] = matrix
        fixture[4] = attestations
        self.assertEqual(self._problems(*fixture), [])

    def test_invalid_matrix_identity_and_changed_qa_lock_cannot_authorize(self):
        for bad_approver in (" ", "\u200b", " leading-space"):
            with self.subTest(approver=repr(bad_approver)):
                fixture = self._fixture()
                matrix = copy.deepcopy(fixture[3])
                matrix["approver"] = bad_approver
                problems = self._problems(
                    fixture[0], fixture[1], fixture[2], matrix,
                    fixture[4], fixture[5])
                self.assertTrue(any(
                    "no named approver" in problem
                    for problem in problems), problems)

        fixture = self._fixture()
        changed = dict(fixture[2], candidateDigest="other")
        problems = self._problems(
            fixture[0], fixture[1], changed, fixture[3],
            fixture[4], fixture[5])
        self.assertTrue(any("internal-input lock" in p for p in problems),
                        problems)

    def test_record_shape_and_diagnostics_are_closed(self):
        fixture = self._fixture()
        qa = copy.deepcopy(fixture[0])
        qa["record"]["unexpected"] = True
        self.assertTrue(any("wrong fields" in problem for problem in
                            self._problems(qa, *fixture[1:])))

        fixture = self._fixture()
        qa = copy.deepcopy(fixture[0])
        qa["record"]["reproductionDiagnostics"] = []
        self.assertTrue(any("diagnostics" in problem for problem in
                            self._problems(qa, *fixture[1:])))

        fixture = self._fixture()
        qa = {"digest": "qa-digest", "record": []}
        self.assertTrue(self._problems(qa, *fixture[1:]))


if __name__ == "__main__":
    unittest.main()
