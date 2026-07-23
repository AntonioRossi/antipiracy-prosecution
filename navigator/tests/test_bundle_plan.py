"""Focused tests for the read-only bundle-config refresh planner."""

import copy
import io
import json
import os
import sys
import unittest
from unittest import mock


sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib import acceptance, authority, bundleplan, bundlezip, canon  # noqa: E402
from lib import qaevidence, recordprovenance, release, render  # noqa: E402
from tests import acceptance_support  # noqa: E402
import build as build_mod  # noqa: E402


REQUIRED = frozenset((
    "inventory-completeness", "qa-priority-map", "legend-approval",
    "support-matrix-approval",
))
TECHNICAL_PREVIEW_PROFILE = acceptance_support.TECHNICAL_PREVIEW_PROFILE
VALIDATED_RELEASE_PROFILE = acceptance_support.VALIDATED_RELEASE_PROFILE


def _acceptance_context(profile=VALIDATED_RELEASE_PROFILE):
    return acceptance_support.context(profile)


ACCEPTANCE_CONTEXT = _acceptance_context()

NAV = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
        "evidence": "Completed against exact candidate bytes",
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
    return {
        "kind": kind,
        "digest": canon.composite_digest("aa11393:%s:c1" % kind, record),
        "record": record,
    }


def _release_receipt(subjects, context=ACCEPTANCE_CONTEXT):
    return acceptance_support.receipt("release", subjects, context)


def _approval_problems(record):
    problems = []
    if record.get("approvalStatus") != "passed":
        problems.append("approvalStatus is not 'passed'")
    if not isinstance(record.get("operator"), str) or \
            not record["operator"].strip():
        problems.append("approval has no named operator")
    if not authority.is_authoritative_operator_kind(
            record.get("operatorKind")):
        problems.append("approval operatorKind is not release-authoritative")
    if not isinstance(record.get("note"), str) or not record["note"].strip():
        problems.append("approval note is missing")
    return problems


def _fixture(profile=VALIDATED_RELEASE_PROFILE):
    context = _acceptance_context(profile)
    artifact_name = "current.html"
    artifact = b"current sealed artifact\n"
    artifact_digest = canon.bytes_digest(artifact)
    checksum_name = artifact_name + ".sha256"
    checksum = release.checksum_text(artifact_name, artifact).encode("utf-8")
    manifest_text = profile["artifactLabel"] + " Planner fixture manifest."
    if profile["id"] == "technical-preview":
        manifest_text += (
            " This technical-preview bundle does not claim compatibility "
            "authorization.")
    manifest = (manifest_text + "\n").encode("utf-8")
    wording = canon.text_digest(canon.canon_prose(manifest_text))
    sides = {
        "claimSet": canon.bytes_digest(b"claims"),
        "gateInventory": canon.bytes_digest(b"gates"),
        "relationSet": canon.bytes_digest(b"relations"),
        "priorityMap": canon.bytes_digest(b"priorities"),
        "legendWording": canon.bytes_digest(b"legend"),
        "supportMatrix": canon.bytes_digest(b"support"),
    }
    specs = (
        ("inventory-completeness", "na", {
            "claimSet": sides["claimSet"],
            "gateInventory": sides["gateInventory"],
        }),
        ("qa-priority-map", "na", {
            "relationSet": sides["relationSet"],
            "priorityMap": sides["priorityMap"],
        }),
        ("legend-approval", None, {
            "legendWording": sides["legendWording"],
        }),
        ("support-matrix-approval", None, {
            "supportMatrix": sides["supportMatrix"],
        }),
    )
    attestations = [
        _envelope("attestation", {
            "type": atype, "edition": edition, "sides": attested_sides,
            "note": "Human review completed", "approvalStatus": "passed",
            "operator": "attestor@example.test", "operatorKind": "human",
            "producerCommand":
                recordprovenance.ATTESTATION_PRODUCER_COMMAND,
        })
        for atype, edition, attested_sides in specs
    ]
    by_type = {item["record"]["type"]: item for item in attestations}
    refs = sorted(item["digest"] for item in attestations)
    content_lock = [{
        "path": "current-source.json",
        "digest": canon.bytes_digest(b"current source"),
    }]
    lock_digest = canon.composite_digest(
        "aa11393:lock:c1",
        {"reads": content_lock, "canonVersion": canon.CANON_VERSION})
    qa_lock_payload = {
        "lockType": "internal-qa-inputs",
        "canonVersion": canon.CANON_VERSION,
        "candidateDigest": artifact_digest,
        "contentLockDigest": lock_digest,
        "registryRead": {
            "path": "navigator/profiles/qa_na.json",
            "digest": canon.bytes_digest(b"qa registry"),
        },
        "reads": [{
            "role": "priorityMap", "corpusId": "priority",
            "path": "priority.md", "digest": sides["priorityMap"],
        }],
    }
    qa_lock = dict(qa_lock_payload)
    qa_lock["lockDigest"] = canon.composite_digest(
        "aa11393:lock:c1", qa_lock_payload)
    qa_operator = "qa@example.test"
    qa = _envelope("qa-record", {
        "releaseProfile": "validated-release",
        "edition": "na", "candidateDigest": artifact_digest,
        "lockDigest": lock_digest, "contentLock": content_lock,
        "qaInputLock": qa_lock,
        "reproductionDiagnostics": {
            "interpreter": "3.test", "platform": "test",
            "locale": "C", "unicodedata": "15.1",
        },
        "attestations": refs,
        "supportMatrix": {
            "digest": sides["supportMatrix"],
            "approver": "attestor@example.test",
            "approvalAttestation": by_type[
                "support-matrix-approval"]["digest"],
        },
        "legendApproval": {
            "digest": sides["legendWording"],
            "approvalAttestation": by_type["legend-approval"]["digest"],
        },
        "manualEvidenceVersion": qaevidence.MANUAL_EVIDENCE_VERSION,
        "manualChecks": _manual_evidence(qa_operator, "human"),
        "approvalStatus": "passed", "operator": qa_operator,
        "operatorKind": "human",
    })
    release_record = {
        "recordVersion": "3",
        **acceptance.profile_record_fields(profile),
        "edition": "na", "sealed": artifact_name,
        "sealedDigest": artifact_digest, "lockDigest": lock_digest,
        "qaRecord": (qa["digest"] if profile["manualQaEvidence"] ==
                     "required" else None),
        "attestations": refs,
        "declaredReleaseTimestamp": "2026-07-22T00:00:00Z",
        "approvalStatus": "passed", "operator": "release@example.test",
        "operatorKind": "human",
    }
    release_record["acceptanceReceipt"] = _release_receipt(
        acceptance.release_subjects(
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
        "note": "Counsel approved this exact wording",
        "approvalStatus": "passed", "operator": "counsel@example.test",
        "operatorKind": "human",
        "producerCommand": recordprovenance.ATTESTATION_PRODUCER_COMMAND,
    })
    attestations.append(manifest_approval)
    cfg = {
        "bundleVersion": "3",
        "releaseProfile": profile["id"],
        "name": ("delivery-TECHNICAL-PREVIEW.zip"
                 if profile["id"] == "technical-preview"
                 else "delivery-VALIDATED-RELEASE.zip"),
        "comment": "planner fixture", "editions": ["na"],
        "declaredTimestamp": "2026-07-22T00:00:00Z",
        "manifestApproval": manifest_approval["digest"],
        "members": [
            {
                "kind": "sealed", "name": artifact_name, "edition": "na",
                "digest": artifact_digest,
                "releaseRecord": release_envelope["digest"],
            },
            {
                "kind": "artifact-checksum", "name": checksum_name,
                "artifact": artifact_name,
                "digest": canon.bytes_digest(checksum),
            },
            {
                "kind": "bundle-manifest", "name": "MANIFEST.txt",
                "digest": canon.bytes_digest(manifest),
                "wordingDigest": wording,
            },
        ],
    }
    stored = {
        ("sealed", artifact_name): artifact,
        ("artifact-checksum", checksum_name): checksum,
    }
    bindings = {"na": {
        "sealed": artifact_name, "sealedDigest": artifact_digest,
        "lockDigest": lock_digest,
        "declaredReleaseTimestamp": "2026-07-22T00:00:00Z",
    }}
    qa_records = [qa] if profile["manualQaEvidence"] == "required" else []
    qa_authorization = ({
        "qaInputLock": copy.deepcopy(qa_lock),
        "supportMatrixApprover": "attestor@example.test",
        "supportMatrixTargets": copy.deepcopy(
            FIXTURE_SUPPORT_MATRIX["targets"]),
        "supportMatrixViewport": copy.deepcopy(
            FIXTURE_SUPPORT_MATRIX["viewport"]),
        "apiProbeApis": copy.deepcopy(FIXTURE_API_PROBES),
    } if profile["manualQaEvidence"] == "required" else None)
    return {
        "cfg": cfg,
        "release_records": [release_envelope],
        "qa_records": qa_records,
        "attestations": attestations,
        "stored": stored,
        "manifest_bytes": manifest,
        "manifest_wording_digest": wording,
        "required": {"na": REQUIRED},
        "sides": {"na": sides},
        "bindings": bindings,
        "acceptance": {"na": context},
        "qa_authorization": {"na": qa_authorization},
    }


def _propose(fixture, cfg=None, read_artifact=None):
    if cfg is None:
        cfg = fixture["cfg"]
    if read_artifact is None:
        read_artifact = lambda kind, name: fixture["stored"][(kind, name)]
    return bundleplan.propose_bundle_config(
        cfg, fixture["release_records"], fixture["qa_records"],
        fixture["attestations"], read_artifact,
        fixture["manifest_bytes"], fixture["manifest_wording_digest"],
        _approval_problems, fixture["required"], fixture["sides"],
        fixture["bindings"], fixture["acceptance"],
        fixture["qa_authorization"],
        expected_edition_count=1)


def _make_config_stale(cfg):
    stale = copy.deepcopy(cfg)
    for index, member in enumerate(stale["members"]):
        member["digest"] = canon.bytes_digest(
            ("stale member %d" % index).encode("ascii"))
        if member["kind"] == "sealed":
            member["releaseRecord"] = canon.bytes_digest(b"stale release")
        elif member["kind"] == "bundle-manifest":
            member["wordingDigest"] = canon.bytes_digest(b"stale wording")
    stale["manifestApproval"] = canon.bytes_digest(b"stale approval")
    return stale


class BundlePlanTests(unittest.TestCase):
    maxDiff = None

    def test_refreshes_all_pins_without_mutating_input_or_rereading_store(self):
        fixture = _fixture()
        stale = _make_config_stale(fixture["cfg"])
        original = copy.deepcopy(stale)
        reads = []

        def read_artifact(kind, name):
            reads.append((kind, name))
            return fixture["stored"][(kind, name)]

        proposed = _propose(fixture, stale, read_artifact)
        self.assertEqual(stale, original)
        self.assertEqual(proposed, fixture["cfg"])
        self.assertEqual(reads, [
            ("sealed", "current.html"),
            ("artifact-checksum", "current.html.sha256"),
        ])
        self.assertIsNot(proposed, stale)

    def test_technical_preview_selects_current_model_release_without_qa(self):
        fixture = _fixture(TECHNICAL_PREVIEW_PROFILE)
        self.assertEqual(fixture["cfg"]["bundleVersion"], "3")
        self.assertEqual(fixture["cfg"]["releaseProfile"],
                         "technical-preview")
        self.assertEqual(fixture["qa_records"], [])
        self.assertEqual(fixture["qa_authorization"], {"na": None})

        model_record = copy.deepcopy(
            fixture["release_records"][0]["record"])
        model_record.update({
            "operator": "codex:gpt-5.6-sol:run-preview-plan",
            "operatorKind": "model",
        })
        model_release = _envelope("release-record", model_record)

        # An authorized human record for another profile cannot outrank the
        # exact-profile model release selected for this preview bundle.
        wrong_profile_record = copy.deepcopy(model_record)
        wrong_profile_record.update(
            acceptance.profile_record_fields(VALIDATED_RELEASE_PROFILE))
        wrong_profile_record.update({
            "operator": "release@example.test",
            "operatorKind": "human",
        })
        wrong_profile_release = _envelope(
            "release-record", wrong_profile_record)
        fixture["release_records"] = [
            wrong_profile_release, model_release,
        ]

        proposed = _propose(fixture)
        self.assertEqual(proposed["members"][0]["releaseRecord"],
                         model_release["digest"])
        self.assertIsNone(model_record["qaRecord"])
        self.assertEqual(model_record["compatibilityAuthorization"],
                         "not-authorized")
        self.assertEqual(model_record["deferredControls"],
                         TECHNICAL_PREVIEW_PROFILE["deferredControls"])
        self.assertEqual(model_record["operator"],
                         "codex:gpt-5.6-sol:run-preview-plan")

    def test_release_selection_uses_kind_then_digest_not_existing_pin(self):
        fixture = _fixture()
        alternative_record = copy.deepcopy(
            fixture["release_records"][0]["record"])
        alternative_record["operator"] = "second-releaser@example.test"
        alternative = _envelope("release-record", alternative_record)
        fixture["release_records"].append(alternative)

        stale = _make_config_stale(fixture["cfg"])
        proposed = _propose(fixture, stale)
        self.assertEqual(
            proposed["members"][0]["releaseRecord"],
            min(fixture["release_records"], key=lambda item: item["digest"])
            ["digest"])

        model_record = copy.deepcopy(
            fixture["release_records"][0]["record"])
        model_record.update({
            "operator": "codex:gpt-5.6-sol:run-model-pin",
            "operatorKind": "model",
        })
        model = _envelope("release-record", model_record)
        fixture["release_records"] = [model] + fixture["release_records"]
        pinned_model = copy.deepcopy(fixture["cfg"])
        pinned_model["members"][0]["releaseRecord"] = model["digest"]
        proposed = _propose(fixture, pinned_model)
        self.assertNotEqual(
            proposed["members"][0]["releaseRecord"], model["digest"])
        selected = next(
            item for item in fixture["release_records"]
            if item["digest"] == proposed["members"][0]["releaseRecord"])
        self.assertEqual(selected["record"]["operatorKind"], "human")

    def test_manifest_selection_uses_kind_then_digest(self):
        fixture = _fixture()
        alternative_record = copy.deepcopy(
            fixture["attestations"][-1]["record"])
        alternative_record["operator"] = "second-counsel@example.test"
        alternative = _envelope("attestation", alternative_record)
        fixture["attestations"].append(alternative)

        stale = copy.deepcopy(fixture["cfg"])
        stale["manifestApproval"] = canon.bytes_digest(b"stale approval")
        proposed = _propose(fixture, stale)
        self.assertEqual(
            proposed["manifestApproval"], min(
                fixture["attestations"][-2:],
                key=lambda item: item["digest"])["digest"])

        model_record = copy.deepcopy(
            fixture["attestations"][-1]["record"])
        model_record.update({
            "operator": "codex:gpt-5.6-sol:run-manifest",
            "operatorKind": "model",
        })
        model = _envelope("attestation", model_record)
        fixture["attestations"].append(model)
        stale["manifestApproval"] = model["digest"]
        proposed = _propose(fixture, stale)
        selected = next(
            item for item in fixture["attestations"]
            if item["digest"] == proposed["manifestApproval"])
        self.assertEqual(selected["record"]["operatorKind"], "human")

    def test_never_invents_or_accepts_nonauthoritative_manifest_approval(self):
        fixture = _fixture()
        pending_record = copy.deepcopy(fixture["attestations"][-1]["record"])
        pending_record["approvalStatus"] = "pending"
        pending_record["operatorKind"] = "tool"
        pending = _envelope("attestation", pending_record)
        fixture["attestations"][-1] = pending
        stale = copy.deepcopy(fixture["cfg"])
        stale["manifestApproval"] = canon.bytes_digest(b"no approval")

        with self.assertRaisesRegex(
                bundlezip.BundleError,
                "no eligible current authorized operator manifest "
                "approval.*operatorKind"):
            _propose(fixture, stale)

    def test_independent_current_binding_excludes_old_authorized_release(self):
        fixture = _fixture()
        fixture["bindings"]["na"]["lockDigest"] = canon.bytes_digest(
            b"independently derived new content lock")
        with self.assertRaisesRegex(
                bundlezip.BundleError,
                "no eligible current fully authorized release"):
            _propose(fixture)

    def test_current_binding_timestamp_must_be_canonical(self):
        fixture = _fixture()
        fixture["bindings"]["na"]["declaredReleaseTimestamp"] = \
            "2026-7-2T0:0:0Z"
        with self.assertRaisesRegex(bundlezip.BundleError,
                                    "canonical RFC 3339 UTC second"):
            _propose(fixture)

    def test_current_side_mismatch_rejects_rehashed_release_chain(self):
        fixture = _fixture()
        fixture["sides"]["na"]["relationSet"] = canon.bytes_digest(
            b"new current relation projection")
        with self.assertRaisesRegex(bundlezip.BundleError,
                                    "attestation side relationSet is not current"):
            _propose(fixture)

    def test_current_qa_context_rejects_stale_lock_and_support_approver(self):
        fixture = _fixture()
        fixture["qa_authorization"]["na"]["qaInputLock"][
            "registryRead"]["digest"] = canon.bytes_digest(
                b"current replacement QA registry")
        with self.assertRaisesRegex(
                bundlezip.BundleError,
                "QA internal-input lock is not current"):
            _propose(fixture)

        fixture = _fixture()
        fixture["qa_authorization"]["na"][
            "supportMatrixApprover"] = "Current Support Owner"
        with self.assertRaisesRegex(
                bundlezip.BundleError,
                "QA supportMatrix approver is not current"):
            _propose(fixture)

        fixture = _fixture()
        fixture["qa_authorization"]["na"]["supportMatrixTargets"] = \
            list(reversed(fixture["qa_authorization"]["na"][
                "supportMatrixTargets"]))
        with self.assertRaisesRegex(
                bundlezip.BundleError, "current support matrix"):
            _propose(fixture)

        fixture = _fixture()
        fixture["qa_authorization"]["na"]["apiProbeApis"].append(
            "new.probedApi")
        with self.assertRaisesRegex(
                bundlezip.BundleError, "current probed hooks"):
            _propose(fixture)

    def test_current_qa_context_must_cover_exactly_the_editions(self):
        fixture = _fixture()
        fixture["qa_authorization"] = {}
        with self.assertRaisesRegex(
                bundlezip.BundleError,
                "current QA authorization contexts must cover exactly"):
            _propose(fixture)

    def test_refuses_stale_checksum_and_inconsistent_manifest_wording(self):
        fixture = _fixture()
        fixture["stored"][("artifact-checksum", "current.html.sha256")] = \
            release.checksum_text("current.html", b"old bytes").encode("utf-8")
        with self.assertRaisesRegex(bundlezip.BundleError, "stale"):
            _propose(fixture)

        fixture = _fixture()
        fixture["manifest_wording_digest"] = canon.bytes_digest(
            b"unrelated wording")
        with self.assertRaisesRegex(
                bundlezip.BundleError,
                "manifest bytes do not derive.*wording digest"):
            _propose(fixture)

    def test_cli_emits_only_canonical_json_and_uses_read_only_gateways(self):
        fixture = _fixture()

        class Content:
            def read_text(self, path):
                if path == build_mod.BUNDLE_CONFIG:
                    return json.dumps(fixture["cfg"])
                if path == build_mod.BUNDLE_MANIFEST_RESOURCE:
                    return json.dumps({
                        "manifestVersion": "3",
                        "releaseProfile": fixture["cfg"][
                            "releaseProfile"],
                        "compatibilityAuthorization":
                            VALIDATED_RELEASE_PROFILE[
                                "compatibilityAuthorization"],
                        "deferredControls": [],
                        "bundleManifestText":
                            fixture["manifest_bytes"].decode("utf-8").rstrip(
                                "\n"),
                    })
                if path == acceptance.RELEASE_POLICY_PATH:
                    return json.dumps({
                        "releasePolicyVersion": "1",
                        "activeReleaseProfile": "validated-release",
                        "profiles": [{
                            "id": "validated-release",
                            "observedControls": {
                                identifier: "required"
                                for identifier in
                                acceptance_support.OBSERVED
                            },
                            "artifactLabel": VALIDATED_RELEASE_PROFILE[
                                "artifactLabel"],
                        }],
                    })
                raise AssertionError("unexpected content read %r" % path)

        class Records:
            def read_all(self, kind):
                return {
                    "release-record": fixture["release_records"],
                    "qa-record": fixture["qa_records"],
                    "attestation": fixture["attestations"],
                }[kind]

        class Artifacts:
            def read(self, kind, name):
                return fixture["stored"][(kind, name)]

        stdout = io.StringIO()
        with mock.patch.object(build_mod, "load_planes", return_value={}), \
                mock.patch.object(build_mod.gateway, "ContentGateway",
                                  return_value=Content()), \
                mock.patch.object(build_mod.gateway, "VerificationGateway",
                                  return_value=Records()), \
                mock.patch.object(build_mod.gateway, "ArtifactGateway",
                                  return_value=Artifacts()), \
                mock.patch.object(
                    build_mod, "bundle_attestation_context",
                    return_value=(fixture["required"], fixture["sides"])), \
                mock.patch.object(
                    build_mod, "bundle_acceptance_context",
                    return_value=fixture["acceptance"]), \
                mock.patch.object(
                    build_mod, "current_release_bindings",
                    return_value=fixture["bindings"]), \
                mock.patch.object(
                    build_mod, "bundle_qa_authorization_context",
                    return_value=fixture["qa_authorization"]), \
                mock.patch.object(build_mod, "DELIVERY_EDITION_COUNT", 1), \
                mock.patch.object(sys, "stdout", stdout):
            build_mod.cmd_bundle_plan([])

        self.assertEqual(stdout.getvalue().encode("utf-8"),
                         canon.canonical_json(fixture["cfg"]) + b"\n")


if __name__ == "__main__":
    unittest.main()
