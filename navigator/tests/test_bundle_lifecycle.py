"""Focused regressions for deterministic bundle planning and ZIP safety."""

import copy
import json
import os
import sys
import tempfile
import unittest
from unittest import mock


sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import build as build_mod  # noqa: E402
from lib import acceptance, bundlezip, canon, gateway, qaevidence  # noqa: E402
from lib import currentstate, recordresolver  # noqa: E402
from lib import recordprovenance, release, render  # noqa: E402
from tests import acceptance_support  # noqa: E402


HERE = os.path.dirname(os.path.abspath(__file__))
NAV = os.path.dirname(HERE)
ROOT = os.path.dirname(NAV)

BASE_REQUIRED_ATTESTATIONS = frozenset((
    "inventory-completeness", "qa-priority-map", "legend-approval",
    "support-matrix-approval",
))
FIXTURE_ATTESTATION_POLICY = {"na": BASE_REQUIRED_ATTESTATIONS}
FIXTURE_SIDE_DIGESTS = {
    "claimSet": canon.bytes_digest(b"claim set"),
    "gateInventory": canon.bytes_digest(b"gate inventory"),
    "relationSet": canon.bytes_digest(b"relation set"),
    "priorityMap": canon.bytes_digest(b"priority map"),
    "legendWording": canon.bytes_digest(b"legend wording"),
    "supportMatrix": canon.bytes_digest(b"support matrix"),
}
FIXTURE_CURRENT_SIDES = {"na": FIXTURE_SIDE_DIGESTS}
TECHNICAL_PREVIEW_PROFILE = acceptance_support.TECHNICAL_PREVIEW_PROFILE
VALIDATED_RELEASE_PROFILE = acceptance_support.VALIDATED_RELEASE_PROFILE


def _acceptance_context(profile=VALIDATED_RELEASE_PROFILE):
    return acceptance_support.context(profile)


FIXTURE_ACCEPTANCE_CONTEXT = _acceptance_context()
FIXTURE_ACCEPTANCE_CONTEXTS = {"na": FIXTURE_ACCEPTANCE_CONTEXT}

with open(os.path.join(NAV, "schema", "support-matrix.json"),
          encoding="utf-8") as _support_fh:
    FIXTURE_SUPPORT_MATRIX = json.load(_support_fh)
with open(os.path.join(NAV, "schema", "api-policy.json"),
          encoding="utf-8") as _api_fh:
    FIXTURE_API_PROBES = sorted(render.api_probe_instruments(
        json.load(_api_fh)))


def _manual_evidence(operator, operator_kind):
    common = {
        "status": "passed",
        "evidence": "Completed against the exact candidate bytes",
        "operator": operator,
        "operatorKind": operator_kind,
    }
    ac11_results = []
    ac13_results = []
    for target in FIXTURE_SUPPORT_MATRIX["targets"]:
        browser_family = target["browser"].split(" ", 1)[0]
        browser_version = {
            "Chrome": "Chrome 150.0.1",
            "Edge": "Edge 150.0.1",
            "Firefox": "Firefox 147.0.1",
            "Safari": "Safari 26.5.2",
        }[browser_family]
        versions = {
            "browserVersion": browser_version,
            "osVersion": ("macOS 14.0" if target["os"].startswith("macOS")
                          else "Windows 11 23H2"),
            "atVersion": (None if target["at"] == "none"
                          else "NVDA 2024.4"),
        }
        ac11_results.append(dict(copy.deepcopy(target), **versions,
            traversalChord="Tab/Shift-Tab",
            traversalConfiguration="Keyboard Navigation enabled",
            checks={
                "keyboardTraversal": "passed", "activationKeys": "passed",
                "focusDeterminism": "passed", "scopedArrowKeys": "passed",
                "computedNameRoleState": "passed", "liveRegion": "passed",
            }))
        ac13_results.append(dict(copy.deepcopy(target), **versions,
            minimumViewport=copy.deepcopy(
                FIXTURE_SUPPORT_MATRIX["viewport"]["minimum"]),
            stackedViewport=[1024, 700],
            checks={
                "localFile": "passed", "minimumViewport": "passed",
                "stackedBelowMinimum": "passed",
            }))
    installed = {"status": "installed", "error": None, "detail": None}
    return {
        "ac11": dict(common, targetResults=ac11_results),
        "ac12": dict(common, printResult={
            "browser": "Safari", "browserVersion": "Safari 26.5.2",
            "os": "macOS", "osVersion": "macOS 26.5.2", "pageCount": 4,
            "checks": {
                "claimsReadable": "passed", "disclosureReadable": "passed",
                "disclaimerOnEveryPage": "passed",
                "legendOnEveryPage": "passed",
                "provenancePresent": "passed", "schedulePresent": "passed",
                "noContentClipping": "passed",
            },
        }),
        "ac13": dict(common, targetResults=ac13_results),
        "ac15": dict(common, probeResult={
            "browser": "Safari", "browserVersion": "Safari 26.5.2",
            "os": "macOS", "osVersion": "macOS 26.5.2", "ready": True,
            "apis": {api: dict(installed) for api in FIXTURE_API_PROBES},
            "attempts": [], "resources": [], "cookieWrites": [],
            "webStorage": [], "indexedDB": [], "navigationMutations": [],
            "networkRequests": [],
        }),
    }


def _envelope(kind, record):
    digest = canon.composite_digest("aa11393:%s:c1" % kind, record)
    return {"kind": kind, "digest": digest, "record": record}


def _acceptance_receipt(kind, subjects, context=FIXTURE_ACCEPTANCE_CONTEXT):
    return acceptance_support.receipt(kind, subjects, context)


def _fixture(operator_kind="human", support_approver=None,
             profile=VALIDATED_RELEASE_PROFILE):
    context = _acceptance_context(profile)
    if operator_kind == "human":
        attestor = "attestor@example.test"
        qa_operator = "qa@example.test"
        release_operator = "releaser@example.test"
        manifest_operator = "reviewer@example.test"
    else:
        attestor = "codex:gpt-5.6-sol:run-attest"
        qa_operator = "codex:gpt-5.6-sol:run-qa"
        release_operator = "codex:gpt-5.6-sol:run-release"
        manifest_operator = "codex:gpt-5.6-sol:run-manifest"
    artifact_name = "a.html"
    artifact = b"sealed artifact\n"
    artifact_digest = canon.bytes_digest(artifact)
    checksum_name = artifact_name + ".sha256"
    checksum = release.checksum_text(artifact_name, artifact).encode("utf-8")
    manifest_text = profile["artifactLabel"] + " Fixture manifest."
    if profile["id"] == "technical-preview":
        manifest_text += (
            " This technical-preview bundle does not claim compatibility "
            "authorization.")
    manifest = (manifest_text + "\n").encode("utf-8")
    wording = canon.text_digest(canon.canon_prose(manifest_text))
    side_digests = dict(FIXTURE_SIDE_DIGESTS)
    attestation_specs = (
        ("inventory-completeness", "na", {
            "claimSet": side_digests["claimSet"],
            "gateInventory": side_digests["gateInventory"],
        }),
        ("qa-priority-map", "na", {
            "relationSet": side_digests["relationSet"],
            "priorityMap": side_digests["priorityMap"],
        }),
        ("legend-approval", None, {
            "legendWording": side_digests["legendWording"],
        }),
        ("support-matrix-approval", None, {
            "supportMatrix": side_digests["supportMatrix"],
        }),
    )
    attestations = []
    for atype, edition, sides in attestation_specs:
        operator = support_approver \
            if atype == "support-matrix-approval" and support_approver \
            else attestor
        attestations.append(_envelope("attestation", {
            "type": atype, "edition": edition, "sides": sides,
            "note": "Authorized review completed",
            "approvalStatus": "passed",
            "operator": operator, "operatorKind": operator_kind,
            "producerCommand":
                recordprovenance.ATTESTATION_PRODUCER_COMMAND,
        }))
    attestation_refs = sorted(att["digest"] for att in attestations)
    attestations_by_type = {
        att["record"]["type"]: att for att in attestations
    }

    content_lock = [{
        "path": "source.txt", "digest": canon.bytes_digest(b"source"),
    }]
    lock_digest = canon.composite_digest(
        "aa11393:lock:c1",
        {"reads": content_lock, "canonVersion": canon.CANON_VERSION})
    qa_reads = [{
        "role": "priorityMap", "corpusId": "qa-priority",
        "path": "priority.md", "digest": side_digests["priorityMap"],
    }]
    qa_lock_payload = {
        "lockType": "internal-qa-inputs",
        "canonVersion": canon.CANON_VERSION,
        "candidateDigest": artifact_digest,
        "contentLockDigest": lock_digest,
        "registryRead": {
            "path": "navigator/profiles/qa_na.json",
            "digest": canon.bytes_digest(b"qa registry"),
        },
        "reads": qa_reads,
    }
    qa_lock = dict(qa_lock_payload)
    qa_lock["lockDigest"] = canon.composite_digest(
        "aa11393:lock:c1", qa_lock_payload)
    manual_checks = _manual_evidence(qa_operator, operator_kind)
    qa = _envelope("qa-record", {
        "releaseProfile": "validated-release",
        "edition": "na", "candidateDigest": artifact_digest,
        "lockDigest": lock_digest, "contentLock": content_lock,
        "qaInputLock": qa_lock,
        "reproductionDiagnostics": {
            "interpreter": "3.test", "platform": "test",
            "locale": "C", "unicodedata": "test",
        },
        "attestations": attestation_refs,
        "supportMatrix": {
            "digest": side_digests["supportMatrix"],
            "approver": support_approver or attestor,
            "approvalAttestation": attestations_by_type[
                "support-matrix-approval"]["digest"],
        },
        "legendApproval": {
            "digest": side_digests["legendWording"],
            "approvalAttestation": attestations_by_type[
                "legend-approval"]["digest"],
        },
        "manualEvidenceVersion": qaevidence.MANUAL_EVIDENCE_VERSION,
        "manualChecks": manual_checks, "approvalStatus": "passed",
        "operator": qa_operator, "operatorKind": operator_kind,
    })
    release_record = {
        "recordVersion": "3",
        **acceptance.profile_record_fields(profile),
        "edition": "na", "sealed": artifact_name,
        "sealedDigest": artifact_digest, "lockDigest": lock_digest,
        "qaRecord": (qa["digest"] if profile["manualQaEvidence"] ==
                     "required" else None),
        "attestations": attestation_refs,
        "declaredReleaseTimestamp": "2026-07-22T00:00:00Z",
        "approvalStatus": "passed", "operator": release_operator,
        "operatorKind": operator_kind,
    }
    release_record["acceptanceReceipt"] = _acceptance_receipt(
        "release", acceptance.release_subjects(
            "na", artifact_digest, lock_digest,
            qa["digest"] if profile["manualQaEvidence"] == "required"
            else None,
            qa_lock["lockDigest"] if profile["manualQaEvidence"] ==
            "required" else None,
            profile), context)
    release_envelope = _envelope("release-record", release_record)

    manifest_approval = _envelope("attestation", {
        "type": "manifest-approval", "edition": None,
        "sides": {"manifestWording": wording},
        "approvalStatus": "passed", "operator": manifest_operator,
        "operatorKind": operator_kind, "note": "Operator approved",
        "producerCommand": recordprovenance.ATTESTATION_PRODUCER_COMMAND,
    })
    attestations.append(manifest_approval)
    config = {
        "bundleVersion": "3",
        "releaseProfile": profile["id"],
        "name": ("bundle-TECHNICAL-PREVIEW.zip"
                 if profile["id"] == "technical-preview"
                 else "bundle-VALIDATED-RELEASE.zip"),
        "comment": "test fixture",
        "editions": ["na"],
        "declaredTimestamp": "2026-07-22T00:00:00Z",
        "manifestApproval": manifest_approval["digest"],
        "members": [
            {"kind": "sealed", "name": artifact_name, "edition": "na",
             "digest": artifact_digest,
             "releaseRecord": release_envelope["digest"]},
            {"kind": "artifact-checksum", "name": checksum_name,
             "artifact": artifact_name,
             "digest": canon.bytes_digest(checksum)},
            {"kind": "bundle-manifest", "name": "MANIFEST.txt",
             "digest": canon.bytes_digest(manifest),
             "wordingDigest": wording},
        ],
    }
    releases = [
        {"kind": "release-record", "digest": canon.bytes_digest(
            b"decoy-before"), "record": {}},
        release_envelope,
        {"kind": "release-record", "digest": canon.bytes_digest(
            b"decoy-after"), "record": {}},
    ]
    stored = {
        ("sealed", artifact_name): artifact,
        ("artifact-checksum", checksum_name): checksum,
    }
    qas = [qa] if profile["manualQaEvidence"] == "required" else []
    return config, releases, qas, attestations, stored, manifest, wording


def _qa_authorization_context(qas):
    record = qas[0]["record"]
    return {
        "qaInputLock": copy.deepcopy(record["qaInputLock"]),
        "supportMatrixApprover": record["supportMatrix"]["approver"],
        "supportMatrixTargets": copy.deepcopy(
            FIXTURE_SUPPORT_MATRIX["targets"]),
        "supportMatrixViewport": copy.deepcopy(
            FIXTURE_SUPPORT_MATRIX["viewport"]),
        "apiProbeApis": copy.deepcopy(FIXTURE_API_PROBES),
    }


def _qa_authorization_contexts(qas):
    return {"na": (_qa_authorization_context(qas) if qas else None)}


class BundleLifecycleTests(unittest.TestCase):
    maxDiff = None

    def test_repository_config_enumerates_exact_members_and_manifest_output(self):
        config_path = os.path.join(NAV, "bundles", "na-af-2026.json")
        with open(config_path, encoding="utf-8") as fh:
            config = json.load(fh)
        bundlezip.validate_bundle_config(config)
        self.assertEqual(config["bundleVersion"], "3")
        self.assertEqual(config["releaseProfile"], "technical-preview")
        self.assertIn("TECHNICAL-PREVIEW", config["name"])
        policy = currentstate.bundle_attestation_policy(config)
        self.assertEqual(frozenset(policy["na"]),
                         BASE_REQUIRED_ATTESTATIONS)
        self.assertEqual(
            frozenset(policy["af"]),
            BASE_REQUIRED_ATTESTATIONS | {"qa-crosswalk"})
        kinds = [member["kind"] for member in config["members"]]
        self.assertEqual(kinds, [
            "sealed", "artifact-checksum", "sealed",
            "artifact-checksum", "bundle-manifest"])

        with open(os.path.join(NAV, "schema", "planes.json"),
                  encoding="utf-8") as fh:
            planes = json.load(fh)
        self.assertIn("bundle-manifest", planes["commands"]["bundle"]["writes"])
        self.assertIn("attestation", planes["commands"]["bundle"]["reads"])
        self.assertIn("qa-record", planes["commands"]["bundle"]["reads"])
        self.assertEqual(planes["kinds"]["bundle-manifest"], "artifact")

        bundle_path = os.path.join(NAV, "dist", config["name"])
        with open(bundle_path, "rb") as fh:
            members = bundlezip.read_zip_members(fh.read())
        self.assertEqual([name for name, unused in members],
                         [member["name"] for member in config["members"]])

    def test_resolver_uses_explicit_release_and_stored_checksum_bytes(self):
        config, releases, qas, attestations, stored, manifest, wording = \
            _fixture()
        reads = []

        def read_artifact(kind, name):
            reads.append((kind, name))
            return stored[(kind, name)]

        plan = bundlezip.resolve_bundle_members(
            config, releases, qas, attestations, read_artifact, manifest,
            wording, currentstate.approval_evidence_problems,
            FIXTURE_ATTESTATION_POLICY, FIXTURE_CURRENT_SIDES,
            expected_edition_count=1,
            acceptance_context_by_edition=FIXTURE_ACCEPTANCE_CONTEXTS,
            qa_authorization_context_by_edition=
                _qa_authorization_contexts(qas))
        self.assertEqual(plan["releaseRecords"],
                         [config["members"][0]["releaseRecord"]])
        self.assertEqual(plan["manifestApproval"],
                         config["manifestApproval"])
        self.assertEqual(reads, [
            ("sealed", "a.html"),
            ("artifact-checksum", "a.html.sha256")])
        self.assertEqual(plan["members"][1][1],
                         stored[("artifact-checksum", "a.html.sha256")])
        self.assertEqual([name for name, unused in plan["members"]],
                         [m["name"] for m in config["members"]])

    def test_complete_model_authorized_ac20_chain_resolves_end_to_end(self):
        config, releases, qas, attestations, stored, manifest, wording = \
            _fixture("model")
        plan = bundlezip.resolve_bundle_members(
            config, releases, qas, attestations,
            lambda kind, name: stored[(kind, name)], manifest, wording,
            currentstate.approval_evidence_problems,
            FIXTURE_ATTESTATION_POLICY, FIXTURE_CURRENT_SIDES,
            expected_edition_count=1,
            acceptance_context_by_edition=FIXTURE_ACCEPTANCE_CONTEXTS,
            qa_authorization_context_by_edition=
                _qa_authorization_contexts(qas))
        selected_release = next(
            envelope for envelope in releases
            if envelope["digest"] == plan["releaseRecords"][0])
        self.assertEqual(
            selected_release["record"]["operator"],
            "codex:gpt-5.6-sol:run-release")
        self.assertEqual(selected_release["record"]["operatorKind"], "model")
        self.assertEqual(qas[0]["record"]["operatorKind"], "model")
        self.assertTrue(all(
            attestation["record"]["operatorKind"] == "model"
            for attestation in attestations))

        zip_bytes = bundlezip.build_zip(
            plan["members"], config["declaredTimestamp"])
        bundle_digest = canon.bytes_digest(zip_bytes)
        config_digest = canon.bytes_digest(b"model chain config")
        record = {
            "recordVersion": "3",
            **acceptance.profile_record_fields(VALIDATED_RELEASE_PROFILE),
            "bundle": config["name"], "bundleDigest": bundle_digest,
            "members": [{"name": member["name"],
                         "digest": member["digest"]}
                        for member in config["members"]],
            "releaseRecords": plan["releaseRecords"],
            "manifestWording": wording,
            "manifestApproval": plan["manifestApproval"],
            "bundleConfigDigest": config_digest,
            "approvalStatus": "passed",
            "operator": "codex:gpt-5.6-sol:run-bundle",
            "operatorKind": "model",
        }
        record["acceptanceReceipt"] = _acceptance_receipt(
            "bundle", acceptance.bundle_subjects(
                config_digest, bundle_digest, record["releaseRecords"],
                record["members"], record["manifestApproval"],
                VALIDATED_RELEASE_PROFILE))
        self.assertEqual(bundlezip.bundle_record_problems(
            record, config, bundle_digest, config_digest,
            expected_edition_count=1,
            current_acceptance_context=FIXTURE_ACCEPTANCE_CONTEXT), [])

    def test_technical_preview_chain_has_no_qa_and_resolves_end_to_end(self):
        config, releases, qas, attestations, stored, manifest, wording = \
            _fixture("model", profile=TECHNICAL_PREVIEW_PROFILE)
        context = _acceptance_context(TECHNICAL_PREVIEW_PROFILE)
        self.assertEqual(qas, [])
        self.assertIn(b"TECHNICAL PREVIEW", manifest)
        plan = bundlezip.resolve_bundle_members(
            config, releases, qas, attestations,
            lambda kind, name: stored[(kind, name)], manifest, wording,
            currentstate.approval_evidence_problems,
            FIXTURE_ATTESTATION_POLICY, FIXTURE_CURRENT_SIDES,
            expected_edition_count=1,
            acceptance_context_by_edition={"na": context},
            qa_authorization_context_by_edition={"na": None})
        release_envelope = next(
            envelope for envelope in releases
            if envelope["digest"] == plan["releaseRecords"][0])
        record = release_envelope["record"]
        self.assertEqual(record["recordVersion"], "3")
        self.assertEqual(record["releaseProfile"], "technical-preview")
        self.assertEqual(record["compatibilityAuthorization"],
                         "not-authorized")
        self.assertEqual(record["deferredControls"],
                         TECHNICAL_PREVIEW_PROFILE["deferredControls"])
        self.assertIsNone(record["qaRecord"])
        self.assertEqual(bundlezip.release_chain_problems(
            release_envelope, qas, attestations,
            BASE_REQUIRED_ATTESTATIONS, FIXTURE_SIDE_DIGESTS,
            currentstate.approval_evidence_problems, context, None), [])

        # A preview cannot acquire a compatibility implication merely by
        # pointing at an otherwise valid validated-release QA envelope.
        unused, unused_releases, validated_qas, unused_attestations, \
            unused_stored, unused_manifest, unused_wording = _fixture()
        changed = copy.deepcopy(release_envelope)
        changed["record"]["qaRecord"] = validated_qas[0]["digest"]
        changed = _envelope("release-record", changed["record"])
        problems = bundlezip.release_chain_problems(
            changed, validated_qas, attestations,
            BASE_REQUIRED_ATTESTATIONS, FIXTURE_SIDE_DIGESTS,
            currentstate.approval_evidence_problems, context, None)
        self.assertTrue(any(
            "deferred observations must have null qaRecord" in problem
            for problem in problems), problems)

    def test_resolver_never_regenerates_a_stale_stored_checksum(self):
        config, releases, qas, attestations, stored, manifest, wording = \
            _fixture()
        stale = release.checksum_text("a.html", b"different bytes").encode()
        stored[("artifact-checksum", "a.html.sha256")] = stale
        config["members"][1]["digest"] = canon.bytes_digest(stale)

        with self.assertRaisesRegex(bundlezip.BundleError, "stale"):
            bundlezip.resolve_bundle_members(
                config, releases, qas, attestations,
                lambda kind, name: stored[(kind, name)], manifest,
                wording, currentstate.approval_evidence_problems,
                FIXTURE_ATTESTATION_POLICY, FIXTURE_CURRENT_SIDES,
                expected_edition_count=1,
                acceptance_context_by_edition=FIXTURE_ACCEPTANCE_CONTEXTS,
                qa_authorization_context_by_edition=
                    _qa_authorization_contexts(qas))

    def test_resolver_rejects_a_stale_current_qa_context(self):
        config, releases, qas, attestations, stored, manifest, wording = \
            _fixture()
        contexts = _qa_authorization_contexts(qas)
        contexts["na"]["qaInputLock"]["registryRead"]["digest"] = \
            canon.bytes_digest(b"new current QA registry")
        with self.assertRaisesRegex(
                bundlezip.BundleError,
                "QA internal-input lock is not current"):
            bundlezip.resolve_bundle_members(
                config, releases, qas, attestations,
                lambda kind, name: stored[(kind, name)], manifest,
                wording, currentstate.approval_evidence_problems,
                FIXTURE_ATTESTATION_POLICY, FIXTURE_CURRENT_SIDES,
                expected_edition_count=1,
                acceptance_context_by_edition=FIXTURE_ACCEPTANCE_CONTEXTS,
                qa_authorization_context_by_edition=contexts)

    def test_resolver_does_not_fall_back_to_record_recency(self):
        config, releases, qas, attestations, stored, manifest, wording = \
            _fixture()
        config["members"][0]["releaseRecord"] = canon.bytes_digest(
            b"missing-explicit-record")
        with self.assertRaisesRegex(bundlezip.BundleError,
                                    "resolved to 0 records"):
            bundlezip.resolve_bundle_members(
                config, releases, qas, attestations,
                lambda kind, name: stored[(kind, name)], manifest,
                wording, currentstate.approval_evidence_problems,
                FIXTURE_ATTESTATION_POLICY, FIXTURE_CURRENT_SIDES,
                expected_edition_count=1,
                acceptance_context_by_edition=FIXTURE_ACCEPTANCE_CONTEXTS,
                qa_authorization_context_by_edition=
                    _qa_authorization_contexts(qas))

    def test_manifest_approval_must_be_current_authorized_evidence(self):
        config, releases, qas, attestations, stored, manifest, wording = \
            _fixture()
        pending = copy.deepcopy(attestations[-1]["record"])
        pending.update({
            "approvalStatus": "pending", "operatorKind": "automation",
            "note": "Pending counsel confirmation",
        })
        attestations[-1] = _envelope("attestation", pending)
        config["manifestApproval"] = attestations[-1]["digest"]
        with self.assertRaisesRegex(bundlezip.BundleError, "approvalStatus"):
            bundlezip.resolve_bundle_members(
                config, releases, qas, attestations,
                lambda kind, name: stored[(kind, name)], manifest,
                wording, currentstate.approval_evidence_problems,
                FIXTURE_ATTESTATION_POLICY, FIXTURE_CURRENT_SIDES,
                expected_edition_count=1,
                acceptance_context_by_edition=FIXTURE_ACCEPTANCE_CONTEXTS,
                qa_authorization_context_by_edition=
                    _qa_authorization_contexts(qas))

        config, releases, qas, attestations, stored, manifest, wording = \
            _fixture()
        stale = copy.deepcopy(attestations[-1]["record"])
        stale["sides"] = {"manifestWording": canon.bytes_digest(b"stale")}
        attestations[-1] = _envelope("attestation", stale)
        config["manifestApproval"] = attestations[-1]["digest"]
        with self.assertRaisesRegex(bundlezip.BundleError,
                                    "manifest approval is stale"):
            bundlezip.resolve_bundle_members(
                config, releases, qas, attestations,
                lambda kind, name: stored[(kind, name)], manifest,
                wording, currentstate.approval_evidence_problems,
                FIXTURE_ATTESTATION_POLICY, FIXTURE_CURRENT_SIDES,
                expected_edition_count=1,
                acceptance_context_by_edition=FIXTURE_ACCEPTANCE_CONTEXTS,
                qa_authorization_context_by_edition=
                    _qa_authorization_contexts(qas))

    def test_repository_manifest_labels_the_deferred_preview_contract(self):
        with open(os.path.join(NAV, "bundle-manifest.json"),
                  encoding="utf-8") as fh:
            manifest = json.load(fh)
        self.assertEqual(manifest["manifestVersion"], "3")
        self.assertEqual(manifest["releaseProfile"], "technical-preview")
        self.assertEqual(manifest["compatibilityAuthorization"],
                         "not-authorized")
        self.assertEqual(manifest["deferredControls"],
                         TECHNICAL_PREVIEW_PROFILE["deferredControls"])
        self.assertTrue(manifest["bundleManifestText"].startswith(
            TECHNICAL_PREVIEW_PROFILE["artifactLabel"]))
        self.assertIn("does not claim compatibility authorization",
                      manifest["bundleManifestText"])

    def test_release_qa_and_attestations_are_authorized_and_typed(self):
        config, releases, qas, attestations, unused, unused_manifest, \
            unused_wording = _fixture()
        release_envelope = next(
            envelope for envelope in releases
            if envelope["digest"] == config["members"][0]["releaseRecord"])
        self.assertEqual(bundlezip.release_chain_problems(
            release_envelope, qas, attestations,
            BASE_REQUIRED_ATTESTATIONS,
            FIXTURE_SIDE_DIGESTS,
            currentstate.approval_evidence_problems,
            FIXTURE_ACCEPTANCE_CONTEXT,
            _qa_authorization_context(qas)), [])

        for field, value in (
                ("operatorKind", "tool"),
                ("operatorKind", "automation"),
                ("operator", " "),
                ("operator", "\u200b\u2060\u200e")):
            with self.subTest(field=field, value=value):
                changed = copy.deepcopy(release_envelope)
                changed["record"][field] = value
                problems = bundlezip.release_chain_problems(
                    changed, qas, attestations,
                    BASE_REQUIRED_ATTESTATIONS, FIXTURE_SIDE_DIGESTS,
                    currentstate.approval_evidence_problems,
                    FIXTURE_ACCEPTANCE_CONTEXT,
                    _qa_authorization_context(qas))
                self.assertTrue(any(
                    "operator" in problem for problem in problems), problems)
        missing_kind = copy.deepcopy(release_envelope)
        missing_kind["record"].pop("operatorKind")
        self.assertTrue(any(
            "operatorKind" in problem for problem in
            bundlezip.release_chain_problems(
                missing_kind, qas, attestations,
                BASE_REQUIRED_ATTESTATIONS, FIXTURE_SIDE_DIGESTS,
                currentstate.approval_evidence_problems,
                FIXTURE_ACCEPTANCE_CONTEXT,
                _qa_authorization_context(qas))))

        unbound_registry_record = copy.deepcopy(qas[0]["record"])
        unbound_registry_record["qaInputLock"].pop("registryRead")
        unbound_registry = _envelope("qa-record", unbound_registry_record)
        release_for_unbound_registry = copy.deepcopy(release_envelope)
        release_for_unbound_registry["record"]["qaRecord"] = \
            unbound_registry["digest"]
        self.assertIn("internal-input lock has the wrong fields", " ".join(
            bundlezip.release_chain_problems(
                release_for_unbound_registry, [unbound_registry],
                attestations, BASE_REQUIRED_ATTESTATIONS,
                FIXTURE_SIDE_DIGESTS,
                currentstate.approval_evidence_problems,
                FIXTURE_ACCEPTANCE_CONTEXT,
                _qa_authorization_context(qas))))

        pending_release = copy.deepcopy(release_envelope)
        pending_release["record"]["approvalStatus"] = "pending"
        self.assertIn("release record approvalStatus", " ".join(
            bundlezip.release_chain_problems(
                pending_release, qas, attestations,
                BASE_REQUIRED_ATTESTATIONS,
                FIXTURE_SIDE_DIGESTS,
                currentstate.approval_evidence_problems,
                FIXTURE_ACCEPTANCE_CONTEXT,
                _qa_authorization_context(qas))))

        pending_qa_record = copy.deepcopy(qas[0]["record"])
        pending_qa_record["approvalStatus"] = "pending"
        pending_qa = _envelope("qa-record", pending_qa_record)
        release_for_qa = copy.deepcopy(release_envelope)
        release_for_qa["record"]["qaRecord"] = pending_qa["digest"]
        self.assertIn("QA record approvalStatus", " ".join(
            bundlezip.release_chain_problems(
                release_for_qa, [pending_qa], attestations,
                BASE_REQUIRED_ATTESTATIONS,
                FIXTURE_SIDE_DIGESTS,
                currentstate.approval_evidence_problems,
                FIXTURE_ACCEPTANCE_CONTEXT,
                _qa_authorization_context(qas))))

        inventory = next(att for att in attestations
                         if att["record"]["type"] ==
                         "inventory-completeness")
        pending_att_record = copy.deepcopy(inventory["record"])
        pending_att_record["approvalStatus"] = "pending"
        pending_att_record["note"] = "Pending human review"
        pending_att = _envelope("attestation", pending_att_record)
        changed_attestations = [
            pending_att if att["digest"] == inventory["digest"] else att
            for att in attestations
        ]
        changed_qa_record = copy.deepcopy(qas[0]["record"])
        changed_qa_record["attestations"] = sorted(
            pending_att["digest"] if digest == inventory["digest"] else digest
            for digest in changed_qa_record["attestations"])
        changed_qa = _envelope("qa-record", changed_qa_record)
        release_for_att = copy.deepcopy(release_envelope)
        release_for_att["record"]["qaRecord"] = changed_qa["digest"]
        release_for_att["record"]["attestations"] = \
            changed_qa_record["attestations"]
        self.assertIn("approvalStatus", " ".join(
            bundlezip.release_chain_problems(
                release_for_att, [changed_qa], changed_attestations,
                BASE_REQUIRED_ATTESTATIONS,
                FIXTURE_SIDE_DIGESTS,
                currentstate.approval_evidence_problems,
                FIXTURE_ACCEPTANCE_CONTEXT,
                _qa_authorization_context(qas))))

    def test_bundle_validator_rejects_missing_or_forged_provenance(self):
        unused_config, unused_releases, unused_qas, attestations, \
            unused_stored, unused_manifest, unused_wording = _fixture()
        record = attestations[0]["record"]
        self.assertEqual(bundlezip._attestation_record_problems(
            record, "na", currentstate.approval_evidence_problems), [])
        for producer in (None, "navigator/build.py attest/v2",
                         "navigator/build.py release/v1"):
            with self.subTest(producer=producer):
                changed = copy.deepcopy(record)
                if producer is None:
                    changed.pop("producerCommand")
                else:
                    changed["producerCommand"] = producer
                problems = bundlezip._attestation_record_problems(
                    changed, "na", currentstate.approval_evidence_problems)
                self.assertTrue(any(
                    "producerCommand" in problem for problem in problems),
                    problems)

    def test_bundle_validator_independently_rejects_nonfinal_notes(self):
        unused_config, unused_releases, unused_qas, attestations, \
            unused_stored, unused_manifest, unused_wording = _fixture()
        record = copy.deepcopy(attestations[0]["record"])

        record["note"] = "Review failed; do not release"
        problems = bundlezip._attestation_record_problems(
            record, "na", lambda unused_record: [])
        self.assertTrue(any("final evidence" in problem
                            for problem in problems), problems)

        record["note"] = "Review passed with no errors"
        self.assertEqual(bundlezip._attestation_record_problems(
            record, "na", lambda unused_record: []), [])

    def test_release_chain_treats_support_approver_as_identity(self):
        config, releases, qas, attestations, unused, unused_manifest, \
            unused_wording = _fixture(
                support_approver="qa-failure-reviewer@example.test")
        release_envelope = next(
            envelope for envelope in releases
            if envelope["digest"] == config["members"][0]["releaseRecord"])
        self.assertEqual(bundlezip.release_chain_problems(
            release_envelope, qas, attestations,
            BASE_REQUIRED_ATTESTATIONS, FIXTURE_SIDE_DIGESTS,
            currentstate.approval_evidence_problems,
            FIXTURE_ACCEPTANCE_CONTEXT, _qa_authorization_context(qas)), [])

    def test_release_chain_compares_independently_current_qa_context(self):
        config, releases, qas, attestations, unused, unused_manifest, \
            unused_wording = _fixture()
        release_envelope = next(
            envelope for envelope in releases
            if envelope["digest"] == config["members"][0]["releaseRecord"])

        unavailable = bundlezip.release_chain_problems(
            release_envelope, qas, attestations,
            BASE_REQUIRED_ATTESTATIONS, FIXTURE_SIDE_DIGESTS,
            currentstate.approval_evidence_problems,
            FIXTURE_ACCEPTANCE_CONTEXT)
        self.assertIn(
            "current QA authorization context has the wrong fields",
            unavailable)

        current = _qa_authorization_context(qas)
        current["qaInputLock"]["registryRead"]["digest"] = \
            canon.bytes_digest(b"replacement selected QA registry")
        payload = {
            field: value for field, value in current["qaInputLock"].items()
            if field != "lockDigest"
        }
        current["qaInputLock"]["lockDigest"] = canon.composite_digest(
            "aa11393:lock:c1", payload)
        problems = bundlezip.release_chain_problems(
            release_envelope, qas, attestations,
            BASE_REQUIRED_ATTESTATIONS, FIXTURE_SIDE_DIGESTS,
            currentstate.approval_evidence_problems,
            FIXTURE_ACCEPTANCE_CONTEXT, current)
        self.assertIn("QA internal-input lock is not current", problems)

        current = _qa_authorization_context(qas)
        current["supportMatrixApprover"] = "Replacement Support Owner"
        problems = bundlezip.release_chain_problems(
            release_envelope, qas, attestations,
            BASE_REQUIRED_ATTESTATIONS, FIXTURE_SIDE_DIGESTS,
            currentstate.approval_evidence_problems,
            FIXTURE_ACCEPTANCE_CONTEXT, current)
        self.assertIn("QA supportMatrix approver is not current", problems)

        current = _qa_authorization_context(qas)
        current["supportMatrixTargets"] = list(reversed(
            current["supportMatrixTargets"]))
        problems = bundlezip.release_chain_problems(
            release_envelope, qas, attestations,
            BASE_REQUIRED_ATTESTATIONS, FIXTURE_SIDE_DIGESTS,
            currentstate.approval_evidence_problems,
            FIXTURE_ACCEPTANCE_CONTEXT, current)
        self.assertTrue(any("current support matrix" in problem
                            for problem in problems), problems)

        current = _qa_authorization_context(qas)
        current["supportMatrixViewport"]["minimum"] = [1440, 900]
        problems = bundlezip.release_chain_problems(
            release_envelope, qas, attestations,
            BASE_REQUIRED_ATTESTATIONS, FIXTURE_SIDE_DIGESTS,
            currentstate.approval_evidence_problems,
            FIXTURE_ACCEPTANCE_CONTEXT, current)
        self.assertTrue(any("minimumViewport" in problem
                            for problem in problems), problems)

        current = _qa_authorization_context(qas)
        current["apiProbeApis"].append("new.probedApi")
        problems = bundlezip.release_chain_problems(
            release_envelope, qas, attestations,
            BASE_REQUIRED_ATTESTATIONS, FIXTURE_SIDE_DIGESTS,
            currentstate.approval_evidence_problems,
            FIXTURE_ACCEPTANCE_CONTEXT, current)
        self.assertTrue(any("current probed hooks" in problem
                            for problem in problems), problems)

    def test_rehashed_qa_cannot_omit_or_relabel_structured_manual_evidence(self):
        config, releases, qas, attestations, unused, unused_manifest, \
            unused_wording = _fixture()
        release_envelope = next(
            envelope for envelope in releases
            if envelope["digest"] == config["members"][0]["releaseRecord"])
        mutations = []
        incomplete = copy.deepcopy(qas[0]["record"])
        incomplete["manualChecks"]["ac11"]["targetResults"].pop()
        mutations.append((incomplete, "every current support target"))
        relabeled = copy.deepcopy(qas[0]["record"])
        relabeled["manualChecks"]["ac13"]["targetResults"][0][
            "browser"] = "Safari ≥ 17"
        mutations.append((relabeled, "current support matrix"))
        legacy_version = copy.deepcopy(qas[0]["record"])
        legacy_version["manualEvidenceVersion"] = "1"
        mutations.append((legacy_version, "manualEvidenceVersion"))

        for qa_record, expected in mutations:
            with self.subTest(expected=expected):
                changed_qa = _envelope("qa-record", qa_record)
                changed_release_record = copy.deepcopy(
                    release_envelope["record"])
                changed_release_record["qaRecord"] = changed_qa["digest"]
                changed_release_record["acceptanceReceipt"] = \
                    _acceptance_receipt(
                        "release", acceptance.release_subjects(
                            changed_release_record["edition"],
                            changed_release_record["sealedDigest"],
                            changed_release_record["lockDigest"],
                            changed_qa["digest"],
                            qa_record["qaInputLock"]["lockDigest"],
                            VALIDATED_RELEASE_PROFILE))
                changed_release = _envelope(
                    "release-record", changed_release_record)
                problems = bundlezip.release_chain_problems(
                    changed_release, [changed_qa], attestations,
                    BASE_REQUIRED_ATTESTATIONS, FIXTURE_SIDE_DIGESTS,
                    currentstate.approval_evidence_problems,
                    FIXTURE_ACCEPTANCE_CONTEXT,
                    _qa_authorization_context(qas))
                self.assertTrue(any(expected in problem
                                    for problem in problems), problems)

    def test_release_chain_binds_support_approval_to_named_approver(self):
        config, releases, qas, attestations, unused, unused_manifest, \
            unused_wording = _fixture()
        current_release = next(
            envelope for envelope in releases
            if envelope["digest"] == config["members"][0]["releaseRecord"])
        support = next(
            envelope for envelope in attestations
            if envelope["record"]["type"] == "support-matrix-approval")

        exact_problems = bundlezip.release_chain_problems(
            current_release, qas, attestations,
            BASE_REQUIRED_ATTESTATIONS, FIXTURE_SIDE_DIGESTS,
            currentstate.approval_evidence_problems,
            FIXTURE_ACCEPTANCE_CONTEXT, _qa_authorization_context(qas))
        self.assertEqual(exact_problems, [])

        changed_support_record = copy.deepcopy(support["record"])
        changed_support_record["operator"] = "different@example.test"
        changed_support = _envelope("attestation", changed_support_record)
        changed_attestations = [
            changed_support if item["digest"] == support["digest"] else item
            for item in attestations
        ]

        changed_qa_record = copy.deepcopy(qas[0]["record"])
        changed_qa_record["attestations"] = sorted(
            changed_support["digest"] if digest == support["digest"]
            else digest for digest in changed_qa_record["attestations"])
        changed_qa_record["supportMatrix"]["approvalAttestation"] = \
            changed_support["digest"]
        changed_qa = _envelope("qa-record", changed_qa_record)

        changed_release_record = copy.deepcopy(current_release["record"])
        changed_release_record["qaRecord"] = changed_qa["digest"]
        changed_release_record["attestations"] = \
            changed_qa_record["attestations"]
        changed_release_record["acceptanceReceipt"] = _acceptance_receipt(
            "release", acceptance.release_subjects(
                "na", changed_release_record["sealedDigest"],
                changed_release_record["lockDigest"], changed_qa["digest"],
                changed_qa_record["qaInputLock"]["lockDigest"],
                VALIDATED_RELEASE_PROFILE))
        changed_release = _envelope(
            "release-record", changed_release_record)

        problems = bundlezip.release_chain_problems(
            changed_release, [changed_qa], changed_attestations,
            BASE_REQUIRED_ATTESTATIONS, FIXTURE_SIDE_DIGESTS,
            currentstate.approval_evidence_problems,
            FIXTURE_ACCEPTANCE_CONTEXT,
            _qa_authorization_context([changed_qa]))
        self.assertIn(
            "support-matrix-approval operator does not match support matrix "
            "approver", problems)

    def test_release_chain_rejects_missing_stale_or_wrong_receipts(self):
        config, releases, qas, attestations, unused, unused_manifest, \
            unused_wording = _fixture()
        current = next(
            envelope for envelope in releases
            if envelope["digest"] == config["members"][0]["releaseRecord"])
        mutations = []
        missing = copy.deepcopy(current)
        missing["record"].pop("acceptanceReceipt")
        mutations.append(missing)
        stale = copy.deepcopy(current)
        stale["record"]["acceptanceReceipt"]["runnerDigest"] = \
            canon.bytes_digest(b"stale runner")
        mutations.append(stale)
        wrong = copy.deepcopy(current)
        wrong["record"]["acceptanceReceipt"]["subjects"][
            "qaRecord"] = canon.bytes_digest(b"wrong QA subject")
        mutations.append(wrong)
        for changed in mutations:
            with self.subTest(receipt=changed["record"].get(
                    "acceptanceReceipt", "missing")):
                problems = bundlezip.release_chain_problems(
                    changed, qas, attestations,
                    BASE_REQUIRED_ATTESTATIONS, FIXTURE_SIDE_DIGESTS,
                    currentstate.approval_evidence_problems,
                    FIXTURE_ACCEPTANCE_CONTEXT,
                    _qa_authorization_context(qas))
                self.assertTrue(any("acceptance" in problem
                                    for problem in problems), problems)

    def test_rehashed_release_chain_cannot_replace_a_current_side_digest(self):
        config, releases, qas, attestations, stored, manifest, wording = \
            _fixture()
        release_envelope = next(
            envelope for envelope in releases
            if envelope["digest"] == config["members"][0]["releaseRecord"])
        inventory = next(
            attestation for attestation in attestations
            if attestation["record"]["type"] == "inventory-completeness")

        stale_record = copy.deepcopy(inventory["record"])
        stale_record["sides"]["claimSet"] = canon.bytes_digest(
            b"stale but well-formed claim projection")
        stale_attestation = _envelope("attestation", stale_record)
        changed_attestations = [
            stale_attestation if item["digest"] == inventory["digest"] else item
            for item in attestations
        ]

        changed_qa_record = copy.deepcopy(qas[0]["record"])
        changed_qa_record["attestations"] = sorted(
            stale_attestation["digest"] if digest == inventory["digest"]
            else digest
            for digest in changed_qa_record["attestations"])
        changed_qa = _envelope("qa-record", changed_qa_record)

        changed_release_record = copy.deepcopy(release_envelope["record"])
        changed_release_record["qaRecord"] = changed_qa["digest"]
        changed_release_record["attestations"] = \
            changed_qa_record["attestations"]
        changed_release = _envelope("release-record", changed_release_record)
        config["members"][0]["releaseRecord"] = changed_release["digest"]

        with self.assertRaisesRegex(
                bundlezip.BundleError,
                "inventory-completeness attestation side claimSet is not "
                "current"):
            bundlezip.resolve_bundle_members(
                config, [changed_release], [changed_qa], changed_attestations,
                lambda kind, name: stored[(kind, name)], manifest, wording,
                currentstate.approval_evidence_problems,
                FIXTURE_ATTESTATION_POLICY, FIXTURE_CURRENT_SIDES,
                expected_edition_count=1,
                acceptance_context_by_edition=FIXTURE_ACCEPTANCE_CONTEXTS,
                qa_authorization_context_by_edition=
                    _qa_authorization_contexts(qas))

    def test_malformed_inner_records_are_rejected_without_crashing(self):
        for malformed_kind in ("release", "qa", "manifest"):
            with self.subTest(malformed_kind=malformed_kind):
                config, releases, qas, attestations, stored, manifest, \
                    wording = _fixture()
                qa_authorization_contexts = _qa_authorization_contexts(qas)
                if malformed_kind == "release":
                    malformed = _envelope("release-record", [])
                    releases = [malformed]
                    config["members"][0]["releaseRecord"] = \
                        malformed["digest"]
                elif malformed_kind == "qa":
                    malformed = _envelope("qa-record", [])
                    qas = [malformed]
                    valid_release = next(
                        item for item in releases
                        if item["digest"] ==
                        config["members"][0]["releaseRecord"])
                    release_record = copy.deepcopy(valid_release["record"])
                    release_record["qaRecord"] = malformed["digest"]
                    replacement = _envelope("release-record", release_record)
                    releases = [replacement]
                    config["members"][0]["releaseRecord"] = \
                        replacement["digest"]
                else:
                    malformed = _envelope("attestation", [])
                    attestations[-1] = malformed
                    config["manifestApproval"] = malformed["digest"]
                with self.assertRaisesRegex(bundlezip.BundleError,
                                            "not an object|malformed"):
                    bundlezip.resolve_bundle_members(
                        config, releases, qas, attestations,
                        lambda kind, name: stored[(kind, name)], manifest,
                        wording, currentstate.approval_evidence_problems,
                        FIXTURE_ATTESTATION_POLICY, FIXTURE_CURRENT_SIDES,
                        expected_edition_count=1,
                        acceptance_context_by_edition=
                        FIXTURE_ACCEPTANCE_CONTEXTS,
                        qa_authorization_context_by_edition=
                        qa_authorization_contexts)

    def test_config_rejects_bundle_output_and_checksum_member_collisions(self):
        base, unused_releases, unused_qas, unused_attestations, \
            unused_stored, unused_manifest, unused_wording = _fixture()
        for collision in (base["name"].upper(),
                          (base["name"] + ".sha256").upper()):
            with self.subTest(collision=collision):
                config, unused_releases, unused_qas, unused_attestations, \
                    unused_stored, unused_manifest, unused_wording = _fixture()
                config["members"][-1]["name"] = collision
                with self.assertRaisesRegex(bundlezip.BundleError, "collides"):
                    bundlezip.validate_bundle_config(
                        config, expected_edition_count=1)

    def test_delivery_config_requires_both_edition_members(self):
        config, unused_releases, unused_qas, unused_attestations, \
            unused_stored, unused_manifest, unused_wording = _fixture()
        with self.assertRaisesRegex(bundlezip.BundleError,
                                    "exactly 2 editions"):
            bundlezip.validate_bundle_config(config)

    def test_optional_bundle_comment_is_closed_to_nonempty_strings(self):
        config, unused_releases, unused_qas, unused_attestations, \
            unused_stored, unused_manifest, unused_wording = _fixture()
        for invalid in (None, False, 1, [], {}, ""):
            with self.subTest(invalid=invalid):
                changed = copy.deepcopy(config)
                changed["comment"] = invalid
                with self.assertRaisesRegex(bundlezip.BundleError, "comment"):
                    bundlezip.validate_bundle_config(
                        changed, expected_edition_count=1)

        del config["comment"]
        bundlezip.validate_bundle_config(config, expected_edition_count=1)

    def test_bundle_timestamp_requires_canonical_real_utc_second(self):
        config, unused_releases, unused_qas, unused_attestations, \
            unused_stored, unused_manifest, unused_wording = _fixture()
        for invalid in (
                "2026-7-2T0:0:0Z", "2026-02-30T00:00:00Z",
                "2026-07-22T00:00:00+00:00", 20260722):
            with self.subTest(invalid=invalid):
                changed = copy.deepcopy(config)
                changed["declaredTimestamp"] = invalid
                with self.assertRaisesRegex(bundlezip.BundleError,
                                            "RFC 3339 UTC second"):
                    bundlezip.validate_bundle_config(
                        changed, expected_edition_count=1)

    def test_crosswalk_policy_cannot_be_satisfied_by_base_chain(self):
        config, releases, qas, attestations, unused_stored, \
            unused_manifest, unused_wording = _fixture()
        release_envelope = next(
            envelope for envelope in releases
            if envelope["digest"] == config["members"][0]["releaseRecord"])
        required = BASE_REQUIRED_ATTESTATIONS | {"qa-crosswalk"}
        problems = bundlezip.release_chain_problems(
            release_envelope, qas, attestations, required,
            FIXTURE_SIDE_DIGESTS,
            currentstate.approval_evidence_problems,
            FIXTURE_ACCEPTANCE_CONTEXT,
            _qa_authorization_context(qas))
        self.assertTrue(any("required attestation" in problem
                            for problem in problems), problems)

    def test_zip_writer_rejects_unsafe_and_duplicate_names(self):
        unsafe = ("../a", "/a", "a\\b", "C:/a", "a//b", "a/./b",
                  "a/../b", "a\x00b",
                  # U+1E08F has CCC=230 in Unicode 15.1 but was unassigned
                  # in Python 3.10's Unicode 13 tables.  The cedilla must
                  # sort before it, so this spelling is not pinned NFC.
                  "a\U0001e08f\u0327.txt")
        for name in unsafe:
            with self.subTest(name=repr(name)):
                with self.assertRaises(bundlezip.BundleError):
                    bundlezip.build_zip(
                        [(name, b"x")], "2026-07-22T00:00:00Z")
        for members in (
                [("a.txt", b"one"), ("a.txt", b"two")],
                [("A.txt", b"one"), ("a.txt", b"two")]):
            with self.assertRaisesRegex(bundlezip.BundleError, "duplicate"):
                bundlezip.build_zip(members, "2026-07-22T00:00:00Z")

    def test_release_status_requires_the_stored_checksum_pair(self):
        artifact = b"sealed"
        digest = canon.bytes_digest(artifact)
        checksum = release.checksum_text("a.html", artifact).encode("utf-8")

        class Stored:
            def __init__(self, values):
                self.values = values

            def read(self, kind, name):
                try:
                    return self.values[(kind, name)]
                except KeyError:
                    raise gateway.GatewayError("missing")

        complete = Stored({
            ("sealed", "a.html"): artifact,
            ("artifact-checksum", "a.html.sha256"): checksum,
        })
        self.assertEqual(currentstate.release_artifact_status(
            complete, "a.html", digest), (True, True))
        missing_checksum = Stored({("sealed", "a.html"): artifact})
        self.assertEqual(currentstate.release_artifact_status(
            missing_checksum, "a.html", digest), (True, False))

    def test_bundle_record_chain_is_ordered_and_exact(self):
        config, unused, unused_qas, attestations, stored, manifest, wording = \
            _fixture()
        members = [(m["name"], manifest if m["kind"] == "bundle-manifest"
                    else stored[(m["kind"], m["name"])])
                   for m in config["members"]]
        bundle_digest = canon.bytes_digest(bundlezip.build_zip(
            members, config["declaredTimestamp"]))
        record = {
            "recordVersion": "3",
            **acceptance.profile_record_fields(VALIDATED_RELEASE_PROFILE),
            "bundle": config["name"], "bundleDigest": bundle_digest,
            "members": [{"name": m["name"], "digest": m["digest"]}
                        for m in config["members"]],
            "releaseRecords": [config["members"][0]["releaseRecord"]],
            "manifestWording": wording,
            "manifestApproval": attestations[-1]["digest"],
            "bundleConfigDigest": canon.bytes_digest(b"config"),
            "approvalStatus": "passed",
            "operator": "Bundle Operator",
            "operatorKind": "human",
        }
        record["acceptanceReceipt"] = _acceptance_receipt(
            "bundle", acceptance.bundle_subjects(
                record["bundleConfigDigest"], bundle_digest,
                record["releaseRecords"], record["members"],
                record["manifestApproval"], VALIDATED_RELEASE_PROFILE))
        self.assertEqual(bundlezip.bundle_record_problems(
            record, config, bundle_digest, canon.bytes_digest(b"config"),
            expected_edition_count=1,
            current_acceptance_context=FIXTURE_ACCEPTANCE_CONTEXT), [])
        broken = copy.deepcopy(record)
        broken["members"] = list(reversed(broken["members"]))
        self.assertIn("members", " ".join(bundlezip.bundle_record_problems(
            broken, config, bundle_digest, canon.bytes_digest(b"config"),
            expected_edition_count=1,
            current_acceptance_context=FIXTURE_ACCEPTANCE_CONTEXT)))
        self.assertEqual(bundlezip.bundle_record_problems(
            [], config, bundle_digest, canon.bytes_digest(b"config"),
            expected_edition_count=1,
            current_acceptance_context=FIXTURE_ACCEPTANCE_CONTEXT),
            ["bundle record is not an object"])

        missing_receipt = copy.deepcopy(record)
        missing_receipt.pop("acceptanceReceipt")
        self.assertIn("acceptance receipt", " ".join(
            bundlezip.bundle_record_problems(
                missing_receipt, config, bundle_digest,
                canon.bytes_digest(b"config"), expected_edition_count=1,
                current_acceptance_context=FIXTURE_ACCEPTANCE_CONTEXT)))

        pending = copy.deepcopy(record)
        pending["approvalStatus"] = "pending"
        self.assertIn("approvalStatus", " ".join(
            bundlezip.bundle_record_problems(
                pending, config, bundle_digest,
                canon.bytes_digest(b"config"), expected_edition_count=1,
                current_acceptance_context=FIXTURE_ACCEPTANCE_CONTEXT)))

        invisible_operator = copy.deepcopy(record)
        invisible_operator["operator"] = "\u200b\u2060\u200e"
        self.assertIn("identified operator", " ".join(
            bundlezip.bundle_record_problems(
                invisible_operator, config, bundle_digest,
                canon.bytes_digest(b"config"), expected_edition_count=1,
                current_acceptance_context=FIXTURE_ACCEPTANCE_CONTEXT)))

        unavailable_config = bundlezip.bundle_record_problems(
            record, config, bundle_digest, None, expected_edition_count=1,
            current_acceptance_context=FIXTURE_ACCEPTANCE_CONTEXT)
        self.assertTrue(any("bundleConfigDigest" in problem
                            for problem in unavailable_config),
                        unavailable_config)

        malformed_subjects = copy.deepcopy(record)
        malformed_subjects["acceptanceReceipt"]["subjects"][
            "releaseRecords"] *= 2
        malformed_problems = bundlezip.bundle_record_problems(
            malformed_subjects, config, bundle_digest,
            canon.bytes_digest(b"config"), expected_edition_count=1,
            current_acceptance_context=FIXTURE_ACCEPTANCE_CONTEXT)
        self.assertTrue(any("unique digest list" in problem
                            for problem in malformed_problems),
                        malformed_problems)

        outer_digest = canon.composite_digest(
            "aa11393:bundle-record:c1", record)
        self.assertNotIn(outer_digest.encode("ascii"),
                         canon.canonical_json(record["acceptanceReceipt"]))

    def test_release_resolution_consumes_only_current_authorizations(self):
        config, releases, qas, attestations, stored, manifest, wording = \
            _fixture()
        current = next(
            envelope for envelope in releases
            if envelope["digest"] == config["members"][0]["releaseRecord"])
        context = recordresolver.ReleaseRecordContext(
            edition_id="na", sealed="a.html",
            sealed_digest=config["members"][0]["digest"],
            lock_digest=None, declared_release_timestamp=None,
            release_profile=config["releaseProfile"],
            authorization_problems=lambda envelope:
                bundlezip.release_chain_problems(
                    envelope, qas, attestations, BASE_REQUIRED_ATTESTATIONS,
                    FIXTURE_SIDE_DIGESTS,
                    currentstate.approval_evidence_problems,
                    FIXTURE_ACCEPTANCE_CONTEXT,
                    _qa_authorization_context(qas)))
        resolution = recordresolver.classify(
            "release-record", releases, context)
        self.assertEqual(list(resolution.current_authorizations), [current])
        self.assertEqual(
            sorted(item.digest for item in resolution.invalid_records),
            sorted(envelope["digest"] for envelope in releases
                   if envelope is not current))

        # A rehashed record for older sealed bytes is preserved as
        # superseded evidence and can never seal the configured member.
        stale_record = copy.deepcopy(current["record"])
        stale_record["sealedDigest"] = canon.bytes_digest(b"earlier bytes")
        stale = _envelope("release-record", stale_record)
        stale_resolution = recordresolver.classify(
            "release-record", [stale], context)
        self.assertEqual(
            list(stale_resolution.superseded_evidence), [stale])
        shifted = copy.deepcopy(config)
        shifted["members"][0]["releaseRecord"] = stale["digest"]
        with self.assertRaisesRegex(
                bundlezip.BundleError,
                "does not bind configured edition/member/digest/profile"):
            bundlezip.resolve_bundle_members(
                shifted, [stale], qas, attestations,
                lambda kind, name: stored[(kind, name)], manifest, wording,
                currentstate.approval_evidence_problems,
                FIXTURE_ATTESTATION_POLICY, FIXTURE_CURRENT_SIDES,
                expected_edition_count=1,
                acceptance_context_by_edition=FIXTURE_ACCEPTANCE_CONTEXTS,
                qa_authorization_context_by_edition=
                    _qa_authorization_contexts(qas))

    def test_bundle_record_resolution_buckets(self):
        config, unused, unused_qas, attestations, stored, manifest, wording = \
            _fixture()
        members = [(m["name"], manifest if m["kind"] == "bundle-manifest"
                    else stored[(m["kind"], m["name"])])
                   for m in config["members"]]
        bundle_digest = canon.bytes_digest(bundlezip.build_zip(
            members, config["declaredTimestamp"]))
        config_digest = canon.bytes_digest(b"config")
        record = {
            "recordVersion": "3",
            **acceptance.profile_record_fields(VALIDATED_RELEASE_PROFILE),
            "bundle": config["name"], "bundleDigest": bundle_digest,
            "members": [{"name": m["name"], "digest": m["digest"]}
                        for m in config["members"]],
            "releaseRecords": [config["members"][0]["releaseRecord"]],
            "manifestWording": wording,
            "manifestApproval": attestations[-1]["digest"],
            "bundleConfigDigest": config_digest,
            "approvalStatus": "passed",
            "operator": "Bundle Operator",
            "operatorKind": "human",
        }
        record["acceptanceReceipt"] = _acceptance_receipt(
            "bundle", acceptance.bundle_subjects(
                config_digest, bundle_digest, record["releaseRecords"],
                record["members"], record["manifestApproval"],
                VALIDATED_RELEASE_PROFILE))
        envelope = _envelope("bundle-record", record)
        context = currentstate._bundle_record_context(
            config, bundle_digest, config_digest, FIXTURE_ACCEPTANCE_CONTEXT)
        resolution = recordresolver.classify(
            "bundle-record", [envelope], context)
        self.assertEqual(list(resolution.current_authorizations), [envelope])
        self.assertEqual(bundlezip.bundle_record_problems(
            record, config, bundle_digest, config_digest,
            expected_edition_count=1,
            current_acceptance_context=FIXTURE_ACCEPTANCE_CONTEXT), [])

        stale = _envelope("bundle-record", dict(
            record, bundleDigest=canon.bytes_digest(b"earlier bundle")))
        stale_resolution = recordresolver.classify(
            "bundle-record", [stale], context)
        self.assertEqual(list(stale_resolution.current_authorizations), [])
        self.assertEqual(list(stale_resolution.superseded_evidence), [stale])

        pending = _envelope("bundle-record", dict(
            record, approvalStatus="pending"))
        pending_resolution = recordresolver.classify(
            "bundle-record", [pending], context)
        self.assertEqual(list(pending_resolution.superseded_evidence), [])
        self.assertEqual(
            [item.digest
             for item in pending_resolution.rejected_authorizations],
            [pending["digest"]])

    def test_cmd_bundle_records_the_confirmed_manifest_approval(self):
        config, releases, qas, attestations, stored, manifest, unused = \
            _fixture(profile=TECHNICAL_PREVIEW_PROFILE)
        preview_context = _acceptance_context(TECHNICAL_PREVIEW_PROFILE)
        preview_contexts = {"na": preview_context}
        with open(os.path.join(NAV, "schema", "planes.json"),
                  encoding="utf-8") as fh:
            planes = json.load(fh)
        with tempfile.TemporaryDirectory() as tmp:
            dist = os.path.join(tmp, "navigator", "dist")
            records = os.path.join(tmp, "navigator", "records")
            bundles = os.path.join(tmp, "navigator", "bundles")
            schema = os.path.join(tmp, "navigator", "schema")
            os.makedirs(dist)
            os.makedirs(records)
            os.makedirs(bundles)
            os.makedirs(schema)

            release_envelope = next(
                envelope for envelope in releases
                if envelope["digest"] == config["members"][0]["releaseRecord"])
            release_record = release_envelope["record"]
            current_bindings = {
                release_record["edition"]: {
                    "sealed": release_record["sealed"],
                    "sealedDigest": release_record["sealedDigest"],
                    "lockDigest": release_record["lockDigest"],
                    "declaredReleaseTimestamp":
                        release_record["declaredReleaseTimestamp"],
                }
            }
            current_qa_authorization = _qa_authorization_contexts(qas)
            release_digest, unused_name = gateway.VerificationGateway(
                records, "release", planes).append(
                    "release-record", release_record)
            for qa in qas:
                digest, unused_name = gateway.VerificationGateway(
                    records, "record-qa", planes).append(
                        "qa-record", qa["record"])
                self.assertEqual(digest, qa["digest"])
            for attestation in attestations:
                digest, unused_name = gateway.VerificationGateway(
                    records, "attest", planes).append(
                        "attestation", attestation["record"])
                self.assertEqual(digest, attestation["digest"])
            approval_digest = config["manifestApproval"]

            for (kind, name), data in stored.items():
                with open(os.path.join(dist, name), "wb") as fh:
                    fh.write(data)
            with open(os.path.join(bundles, "na-af-2026.json"),
                      "w", encoding="utf-8") as fh:
                json.dump(config, fh)
            with open(os.path.join(tmp, "navigator", "bundle-manifest.json"),
                      "w", encoding="utf-8") as fh:
                json.dump({
                    "manifestVersion": "3",
                    "releaseProfile": "technical-preview",
                    "compatibilityAuthorization": "not-authorized",
                    "deferredControls":
                        TECHNICAL_PREVIEW_PROFILE["deferredControls"],
                    "bundleManifestText":
                        manifest.decode("utf-8").rstrip("\n"),
                }, fh)
            with open(os.path.join(NAV, "schema", "release-policy.json"),
                      "rb") as source, \
                    open(os.path.join(schema, "release-policy.json"),
                         "wb") as target:
                target.write(source.read())

            def acceptance_transaction(
                    unused_root, current_cfg, config_digest,
                    plan, zip_bytes, checksum_bytes, manifest_bytes, output):
                manifest_member = next(
                    member for member in current_cfg["members"]
                    if member["kind"] == "bundle-manifest")
                output.write("bundle-manifest", manifest_member["name"],
                             manifest_bytes)
                output.write("bundle", current_cfg["name"], zip_bytes)
                output.write("bundle-checksum",
                             current_cfg["name"] + ".sha256", checksum_bytes)
                member_subjects = [
                    {"name": name, "digest": canon.bytes_digest(data)}
                    for name, data in plan["members"]]
                return _acceptance_receipt(
                    "bundle", acceptance.bundle_subjects(
                        config_digest, canon.bytes_digest(zip_bytes),
                        plan["releaseRecords"], member_subjects,
                        plan["manifestApproval"],
                        TECHNICAL_PREVIEW_PROFILE), preview_context)

            verify_calls = []
            real_verify_written = gateway.OutputGateway.verify_written

            def tracking_verify_written(output, kind, name, expected):
                verify_calls.append((kind, name))
                return real_verify_written(output, kind, name, expected)

            with mock.patch.object(build_mod, "ROOT", tmp), \
                    mock.patch.object(build_mod, "DIST", dist), \
                    mock.patch.object(build_mod, "RECORDS", records), \
                    mock.patch.object(build_mod, "load_planes",
                                      return_value=planes), \
                    mock.patch.object(currentstate, "DELIVERY_EDITION_COUNT", 1), \
                    mock.patch.object(
                        currentstate, "bundle_attestation_context",
                        return_value=(FIXTURE_ATTESTATION_POLICY,
                                      FIXTURE_CURRENT_SIDES)), \
                    mock.patch.object(
                        currentstate, "bundle_acceptance_context",
                        return_value=preview_contexts), \
                    mock.patch.object(
                        currentstate, "current_release_bindings",
                        return_value=current_bindings), \
                    mock.patch.object(
                        currentstate, "bundle_qa_authorization_context",
                        return_value=current_qa_authorization), \
                    mock.patch.object(
                        build_mod.release_mod,
                        "run_bundle_acceptance_transaction",
                        side_effect=acceptance_transaction), \
                    mock.patch.object(
                        gateway.OutputGateway, "verify_written",
                        new=tracking_verify_written), \
                    mock.patch.dict(os.environ, {
                        "NAV_OPERATOR": "reviewer@example.test",
                        "NAV_OPERATOR_KIND": "human",
                    }, clear=False), \
                    mock.patch("builtins.print"):
                build_mod.cmd_bundle([])

            self.assertEqual(verify_calls, [
                ("bundle-manifest", "MANIFEST.txt"),
                ("bundle", config["name"]),
                ("bundle-checksum", config["name"] + ".sha256"),
            ])

            envelopes = gateway.VerificationGateway(
                records, "status", planes).read_all("bundle-record")
            self.assertEqual(len(envelopes), 1)
            record = envelopes[0]["record"]
            self.assertEqual(record["recordVersion"], "3")
            self.assertEqual(record["releaseProfile"], "technical-preview")
            self.assertEqual(record["compatibilityAuthorization"],
                             "not-authorized")
            self.assertEqual(record["deferredControls"],
                             TECHNICAL_PREVIEW_PROFILE["deferredControls"])
            self.assertEqual(record["manifestApproval"], approval_digest)
            self.assertEqual(record["releaseRecords"], [release_digest])
            self.assertEqual(record["approvalStatus"], "passed")
            self.assertEqual(record["operatorKind"], "human")
            self.assertEqual(record["acceptanceReceipt"]["runnerKind"],
                             "tool")
            with open(os.path.join(dist, config["name"]), "rb") as fh:
                bundled = dict(bundlezip.read_zip_members(fh.read()))
            self.assertEqual(bundled["a.html.sha256"],
                             stored[("artifact-checksum", "a.html.sha256")])
            self.assertEqual(bundled["MANIFEST.txt"], manifest)

            with mock.patch.object(build_mod, "ROOT", tmp), \
                    mock.patch.object(build_mod, "DIST", dist), \
                    mock.patch.object(build_mod, "RECORDS", records), \
                    mock.patch.object(build_mod, "load_planes",
                                      return_value=planes), \
                    mock.patch.object(currentstate, "DELIVERY_EDITION_COUNT", 1), \
                    mock.patch.object(
                        currentstate, "bundle_attestation_context",
                        return_value=(FIXTURE_ATTESTATION_POLICY,
                                      FIXTURE_CURRENT_SIDES)), \
                    mock.patch.object(
                        currentstate, "bundle_acceptance_context",
                        return_value=preview_contexts), \
                    mock.patch.object(
                        currentstate, "current_release_bindings",
                        return_value=current_bindings), \
                    mock.patch.object(
                        currentstate, "bundle_qa_authorization_context",
                        return_value=current_qa_authorization), \
                    mock.patch.dict(os.environ, {
                        "NAV_OPERATOR": "reviewer@example.test",
                        "NAV_OPERATOR_KIND": "human",
                    }, clear=False), \
                    mock.patch.object(
                        bundlezip, "build_zip",
                        side_effect=bundlezip.BundleError("late ZIP defect")), \
                    mock.patch.object(gateway.OutputGateway, "write") as write:
                with self.assertRaisesRegex(SystemExit, "late ZIP defect"):
                    build_mod.cmd_bundle([])
                write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
