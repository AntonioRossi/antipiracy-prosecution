"""Regression tests for explicit, input-bound artifact provenance."""

import copy
import json
import os
import shutil
import sys
import tempfile
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "navigator"))

from lib import canon, control_inventory, currentstate, gateway, model  # noqa: E402
from lib import projections, recordprovenance, recordresolver  # noqa: E402
from lib import render, render_inventory  # noqa: E402


def load_model(edition, root=ROOT):
    path = "navigator/editions/%s.json" % edition
    boot = gateway.ContentGateway(root)
    config = json.loads(boot.read_text(path))
    content = gateway.ContentGateway(
        root, allowlist=config["declaredTransitiveInputs"])
    return model.EditionModel(content, path)


def copy_inputs(root):
    """Copy both editions' exact content sets and their QA-only resources."""
    paths = set()
    qa_paths = {
        "navigator/bundle-manifest.json",
        "navigator/bundles/na-af-2026.json",
    }
    for edition in ("na", "af"):
        config_path = "navigator/editions/%s.json" % edition
        with open(os.path.join(ROOT, config_path), encoding="utf-8") as fh:
            config = json.load(fh)
        paths.update(config["declaredTransitiveInputs"])
        qa_paths.add(config["qaRegistry"])
        with open(os.path.join(ROOT, config["qaRegistry"]),
                  encoding="utf-8") as fh:
            qa_registry = json.load(fh)
        for entry in qa_registry["corpora"].values():
            qa_paths.update(entry["files"])
    for relative in sorted(paths | qa_paths):
        destination = os.path.join(root, relative)
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.copy2(os.path.join(ROOT, relative), destination)


def rewrite_json(root, relative, mutate):
    path = os.path.join(root, relative)
    with open(path, encoding="utf-8") as fh:
        value = json.load(fh)
    mutate(value)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(value, fh, indent=1, ensure_ascii=False)
        fh.write("\n")


def snapshot(edition, root):
    m = load_model(edition, root)
    return m, render.render(m), m.gw.lock()


class TestProvenance(unittest.TestCase):
    def test_schema_and_edition_specific_strings_are_digest_bound(self):
        m = load_model("na")
        prov = projections.provenance(m)
        self.assertEqual(
            prov["schemaDigest"],
            m.gw.read_log["navigator/schema/relation.schema.json"])
        self.assertEqual(
            prov["stringsProjectionDigest"],
            canon.bytes_digest(canon.canonical_json(
                projections.artifact_strings(m))))

        # The implementation boundary is bidirectional: every production
        # source is declared by both editions, and no unrelated Python path
        # can become a content input merely by being added to an allowlist.
        filesystem_sources = {
            "navigator/build.py",
            "navigator/schema/invariants.py",
        } | {
            "navigator/lib/" + name
            for name in os.listdir(os.path.join(ROOT, "navigator", "lib"))
            if name.endswith(".py")
        }
        expected_render = set(render_inventory.RENDER_SOURCE_PATHS)
        self.assertEqual(
            expected_render | set(control_inventory.CONTROL_SOURCE_PATHS),
            filesystem_sources)
        self.assertFalse(
            expected_render & set(control_inventory.CONTROL_SOURCE_PATHS))
        for edition in ("na", "af"):
            current = load_model(edition)
            declared_python = {
                path for path in current.edition["declaredTransitiveInputs"]
                if path.endswith(".py")
            }
            self.assertEqual(declared_python, expected_render)
            self.assertEqual(
                set(projections.render_source_paths(
                    current.edition["declaredTransitiveInputs"])),
                expected_render)

        outsider = "navigator/maintenance/outsider.py"
        declared_with_outsider = sorted(expected_render | {outsider})

        class RecordingGateway:
            def __init__(self):
                self.reads = []

            def read_bytes(self, path):
                self.reads.append(path)
                return ("source:" + path).encode("utf-8")

        outsider_gateway = RecordingGateway()
        with self.assertRaisesRegex(ValueError, "outsider.py"):
            projections.render_tree_hash(
                outsider_gateway, declared_with_outsider)
        self.assertEqual(outsider_gateway.reads, [])
        self.assertNotIn(outsider, outsider_gateway.reads)

    def test_other_edition_and_bundle_text_do_not_change_projection(self):
        m = load_model("na")
        before = projections.provenance(m)["stringsProjectionDigest"]
        m.strings = copy.deepcopy(m.strings)
        m.strings["editionNamespaces"]["af"] = {
            "sourceGateCodes": {},
        }
        m.strings["editionNamespaces"]["af"]["sourceGateCodes"][
            "claim-as-a-whole"] = "changed elsewhere"
        m.strings["bundleManifestText"] = "changed bundle text"
        after = projections.provenance(m)["stringsProjectionDigest"]
        self.assertEqual(before, after)

    def test_other_edition_resources_do_not_move_content_lock(self):
        with tempfile.TemporaryDirectory() as root:
            copy_inputs(root)
            before_na = snapshot("na", root)
            before_af = snapshot("af", root)

            rewrite_json(
                root, "navigator/profiles/strings_af.json",
                lambda value: value["sourceGateCodes"].update({
                    "claim-as-a-whole": "Changed AF-only gate label",
                }))
            rewrite_json(
                root, "navigator/profiles/corpora_af.json",
                lambda value: value["corpora"]["af-claims"].update({
                    "version": "AF-only registry change",
                }))

            after_na = snapshot("na", root)
            after_af = snapshot("af", root)
            self.assertEqual(before_na[1:], after_na[1:])
            self.assertNotEqual(before_af[1], after_af[1])
            self.assertNotEqual(before_af[2]["lockDigest"],
                                after_af[2]["lockDigest"])
            self.assertNotIn("navigator/profiles/strings_af.json",
                             after_na[0].gw.read_log)
            self.assertNotIn("navigator/profiles/corpora_af.json",
                             after_na[0].gw.read_log)
            for current in (after_na[0], after_af[0]):
                self.assertEqual(
                    set(current.gw.read_log),
                    set(current.edition["declaredTransitiveInputs"]))

    def test_shared_resources_still_move_both_content_locks(self):
        with tempfile.TemporaryDirectory() as root:
            copy_inputs(root)
            before = {
                edition: snapshot(edition, root)[2]["lockDigest"]
                for edition in ("na", "af")
            }
            rewrite_json(
                root, "navigator/strings.json",
                lambda value: value["ui"].update({
                    "aboutTitle": "Changed shared title",
                }))
            after = {
                edition: snapshot(edition, root)[2]["lockDigest"]
                for edition in ("na", "af")
            }
            self.assertNotEqual(before["na"], after["na"])
            self.assertNotEqual(before["af"], after["af"])

    def test_bundle_only_wording_does_not_move_edition_content_locks(self):
        with tempfile.TemporaryDirectory() as root:
            copy_inputs(root)
            before = {
                edition: snapshot(edition, root)[1:]
                for edition in ("na", "af")
            }
            before_sides = currentstate.current_side_digests(
                load_model("na", root), include_bundle=True)
            rewrite_json(
                root, "navigator/bundle-manifest.json",
                lambda value: value.update({
                    "bundleManifestText":
                        value["bundleManifestText"] +
                        " Changed bundle-only wording.",
                }))
            after = {
                edition: snapshot(edition, root)[1:]
                for edition in ("na", "af")
            }
            after_sides = currentstate.current_side_digests(
                load_model("na", root), include_bundle=True)
            self.assertEqual(before, after)
            self.assertNotEqual(before_sides["manifestWording"],
                                after_sides["manifestWording"])
            self.assertEqual(before_sides["legendWording"],
                             after_sides["legendWording"])

    def test_qa_registry_is_edition_scoped_and_raw_byte_bound(self):
        with tempfile.TemporaryDirectory() as root:
            copy_inputs(root)
            na, _, na_content = snapshot("na", root)
            af, _, af_content = snapshot("af", root)
            candidate = canon.bytes_digest(b"candidate")
            before_na = currentstate.qa_input_lock(
                na, candidate, na_content["lockDigest"])
            before_af = currentstate.qa_input_lock(
                af, candidate, af_content["lockDigest"])

            rewrite_json(
                root, "navigator/profiles/qa_af.json",
                lambda unused_value: None)
            na_after_model, _, na_content_after = snapshot("na", root)
            af_after_model, _, af_content_after = snapshot("af", root)
            after_na = currentstate.qa_input_lock(
                na_after_model, candidate, na_content_after["lockDigest"])
            after_af = currentstate.qa_input_lock(
                af_after_model, candidate, af_content_after["lockDigest"])

            self.assertEqual(na_content, na_content_after)
            self.assertEqual(af_content, af_content_after)
            self.assertEqual(before_na, after_na)
            self.assertNotEqual(before_af["registryRead"],
                                after_af["registryRead"])
            self.assertNotEqual(before_af["lockDigest"],
                                after_af["lockDigest"])
            self.assertEqual(
                after_af["registryRead"]["path"],
                "navigator/profiles/qa_af.json")
            self.assertNotIn(
                "navigator/profiles/qa_af.json",
                currentstate.edition_qa_registry(na_after_model).gw.read_log)

    def test_csp_comes_from_the_registered_api_policy(self):
        m = load_model("na")
        marker = "default-src 'none'; test-directive 'none'"
        m.api_policy = copy.deepcopy(m.api_policy)
        m.api_policy["csp"] = marker
        html = render.render(m).decode("utf-8")
        self.assertIn('content="%s"' % marker, html)


def _qa_envelope(digest, **record_updates):
    record = {
        "releaseProfile": "validated-release",
        "edition": "na",
        "candidateDigest": "candidate-digest",
        "lockDigest": "lock-digest",
        "contentLock": [],
        "qaInputLock": {},
        "reproductionDiagnostics": {},
        "attestations": [],
        "supportMatrix": {},
        "legendApproval": {},
        "manualEvidenceVersion": "3",
        "manualChecks": {},
        "approvalStatus": "passed",
        "operator": "QA Reviewer",
        "operatorKind": "human",
    }
    record.update(record_updates)
    return {"kind": "qa-record", "digest": digest, "record": record}


def _qa_context(**updates):
    values = {
        "edition_id": "na",
        "candidate_digest": "candidate-digest",
        "lock_digest": "lock-digest",
        "release_profile": "validated-release",
        "authorization_problems": lambda envelope: [],
    }
    values.update(updates)
    return recordresolver.QaRecordContext(**values)


def _release_envelope(**record_updates):
    record = {
        "recordVersion": "3",
        "releaseProfile": "validated-release",
        "compatibilityAuthorization": "authorized",
        "deferredControls": [],
        "artifactLabel": "label",
        "edition": "na",
        "sealed": "sealed.html",
        "sealedDigest": "sealed-digest",
        "lockDigest": "lock-digest",
        "qaRecord": None,
        "attestations": [],
        "declaredReleaseTimestamp": "2026-07-22T00:00:00Z",
        "approvalStatus": "passed",
        "operator": "Release Reviewer",
        "operatorKind": "human",
        "acceptanceReceipt": {},
    }
    record.update(record_updates)
    return {
        "kind": "release-record",
        "digest": canon.composite_digest(
            "aa11393:release-record:c1", record),
        "record": record,
    }


def _release_context(**updates):
    values = {
        "edition_id": "na",
        "sealed": "sealed.html",
        "sealed_digest": "sealed-digest",
        "lock_digest": "lock-digest",
        "declared_release_timestamp": "2026-07-22T00:00:00Z",
        "release_profile": "validated-release",
        "authorization_problems": lambda envelope: [],
    }
    values.update(updates)
    return recordresolver.ReleaseRecordContext(**values)


def _bundle_envelope(digest, **record_updates):
    record = {
        "recordVersion": "3",
        "releaseProfile": "validated-release",
        "compatibilityAuthorization": "authorized",
        "deferredControls": [],
        "artifactLabel": "label",
        "bundle": "bundle.zip",
        "bundleDigest": "bundle-digest",
        "members": [{"name": "a", "digest": "member-digest"}],
        "releaseRecords": ["release-digest"],
        "manifestWording": "wording-digest",
        "manifestApproval": "approval-digest",
        "bundleConfigDigest": "config-digest",
        "approvalStatus": "passed",
        "operator": "Bundle Reviewer",
        "operatorKind": "human",
        "acceptanceReceipt": {},
    }
    record.update(record_updates)
    return {"kind": "bundle-record", "digest": digest, "record": record}


def _bundle_context(**updates):
    values = {
        "release_profile_fields": {
            "releaseProfile": "validated-release",
            "compatibilityAuthorization": "authorized",
            "deferredControls": [],
            "artifactLabel": "label",
        },
        "release_profile_problem": None,
        "release_profile": "validated-release",
        "bundle": "bundle.zip",
        "bundle_digest": "bundle-digest",
        "members": [{"name": "a", "digest": "member-digest"}],
        "release_records": ["release-digest"],
        "manifest_wording": "wording-digest",
        "manifest_approval": "approval-digest",
        "bundle_config_digest": "config-digest",
        "receipt_problems": lambda record: [],
    }
    values.update(updates)
    return recordresolver.BundleRecordContext(**values)


def _attestation_envelope(digest, **record_updates):
    record = {
        "type": "legend-approval",
        "edition": None,
        "sides": {"legendWording": "legend-digest"},
        "note": "Counsel review completed",
        "approvalStatus": "passed",
        "operator": "Counsel Reviewer",
        "operatorKind": "human",
        "producerCommand": recordprovenance.ATTESTATION_PRODUCER_COMMAND,
    }
    record.update(record_updates)
    return {"digest": digest, "record": record}


def _attestation_context(**updates):
    values = {
        "required_type": "legend-approval",
        "expected_edition": None,
        "check_scope": True,
        "expected_sides": frozenset(("legendWording",)),
        "side_digests": {"legendWording": "legend-digest"},
        "authorization_problems": lambda envelope: [],
    }
    values.update(updates)
    return recordresolver.AttestationContext(**values)


class TestRecordResolver(unittest.TestCase):
    """The closed adapter registry preserves per-kind bucket semantics."""

    def test_unknown_record_kind_fails_closed(self):
        for kind in ("qa-record", "release-record", "bundle-record",
                     "attestation"):
            self.assertIsNotNone(recordresolver.adapter_for(kind))
        with self.assertRaisesRegex(ValueError,
                                    "unknown verification record kind"):
            recordresolver.adapter_for("mystery-record")
        with self.assertRaisesRegex(ValueError,
                                    "unknown verification record kind"):
            recordresolver.classify("mystery-record", [], None)

    def test_context_of_the_wrong_type_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "context"):
            recordresolver.classify(
                "qa-record", [], _attestation_context())

    def test_qa_record_resolution_buckets(self):
        current = _qa_envelope("current-qa")
        stale = _qa_envelope("stale-qa", releaseProfile="technical-preview")
        wrong_kind = {"kind": "release-record", "digest": "bad",
                      "record": {}}
        denied = _qa_envelope("denied-qa")

        def authorization(envelope):
            if envelope["digest"] == "denied-qa":
                return ["QA authorization denied"]
            return []

        resolution = recordresolver.classify(
            "qa-record", [current, stale, wrong_kind, denied],
            _qa_context(authorization_problems=authorization))
        self.assertEqual(list(resolution.current_authorizations), [current])
        self.assertEqual(list(resolution.superseded_evidence), [stale])
        self.assertIs(resolution.superseded_evidence[0], stale)
        self.assertEqual(
            [item.digest for item in resolution.invalid_records], ["bad"])
        self.assertEqual(
            [item.digest for item in resolution.rejected_authorizations],
            ["denied-qa"])
        self.assertEqual(
            list(resolution.rejected_authorizations[0].problems),
            ["QA authorization denied"])

    def test_superseded_evidence_never_reaches_authorization(self):
        def forbidden(envelope):
            raise AssertionError("superseded evidence was re-authorized")

        stale = _qa_envelope("stale-qa", candidateDigest="old-candidate")
        resolution = recordresolver.classify(
            "qa-record", [stale],
            _qa_context(authorization_problems=forbidden))
        self.assertEqual(list(resolution.superseded_evidence), [stale])
        self.assertEqual(list(resolution.current_authorizations), [])

    def test_release_record_resolution_buckets(self):
        current = _release_envelope()
        stale = _release_envelope(lockDigest="earlier-lock")
        inconsistent = _release_envelope()
        inconsistent["digest"] = canon.bytes_digest(b"not the record")
        denied = _release_envelope(operator="Second Releaser")
        shapeless = {"kind": "release-record", "digest": "x", "record": []}

        def authorization(envelope):
            if envelope["digest"] == denied["digest"]:
                return ["release chain incomplete"]
            return []

        resolution = recordresolver.classify(
            "release-record",
            [current, stale, inconsistent, denied, shapeless],
            _release_context(authorization_problems=authorization))
        self.assertEqual(list(resolution.current_authorizations), [current])
        self.assertEqual(list(resolution.superseded_evidence), [stale])
        self.assertEqual(
            [item.digest for item in resolution.invalid_records],
            [inconsistent["digest"], "x"])
        self.assertEqual(
            [item.digest for item in resolution.rejected_authorizations],
            [denied["digest"]])

    def test_release_context_may_leave_lock_and_timestamp_unbound(self):
        promoted = _release_envelope(
            lockDigest="any-lock",
            declaredReleaseTimestamp="2026-01-01T00:00:00Z")
        context = _release_context(
            lock_digest=None, declared_release_timestamp=None)
        resolution = recordresolver.classify(
            "release-record", [promoted], context)
        self.assertEqual(list(resolution.current_authorizations), [promoted])

    def test_bundle_record_resolution_buckets(self):
        current = _bundle_envelope("current-bundle-record")
        stale = _bundle_envelope("stale-bundle-record",
                                 bundleDigest="earlier-bundle-digest")
        pending = _bundle_envelope("pending-bundle-record",
                                   approvalStatus="pending")
        wrong_kind = {"kind": "release-record", "digest": "bad",
                      "record": {}}
        resolution = recordresolver.classify(
            "bundle-record", [current, stale, pending, wrong_kind],
            _bundle_context())
        self.assertEqual(list(resolution.current_authorizations), [current])
        self.assertEqual(list(resolution.superseded_evidence), [stale])
        self.assertIs(resolution.superseded_evidence[0], stale)
        self.assertEqual(
            [item.digest for item in resolution.rejected_authorizations],
            ["pending-bundle-record"])
        self.assertEqual(
            [item.digest for item in resolution.invalid_records], ["bad"])

    def test_bundle_receipt_defects_are_rejected_not_superseded(self):
        envelope = _bundle_envelope("current-bundle-record")
        context = _bundle_context(
            receipt_problems=lambda record: ["receipt is stale"])
        resolution = recordresolver.classify(
            "bundle-record", [envelope], context)
        self.assertEqual(list(resolution.current_authorizations), [])
        self.assertEqual(list(resolution.superseded_evidence), [])
        self.assertEqual(
            [item.digest for item in resolution.rejected_authorizations],
            ["current-bundle-record"])

    def test_bundle_profile_unavailability_is_currency(self):
        envelope = _bundle_envelope("current-bundle-record")
        context = _bundle_context(
            release_profile_fields=None,
            release_profile_problem="profile is unavailable")
        resolution = recordresolver.classify(
            "bundle-record", [envelope], context)
        self.assertEqual(list(resolution.superseded_evidence), [envelope])

    def test_attestation_resolution_buckets(self):
        current = _attestation_envelope("current-att")
        stale_side = _attestation_envelope(
            "stale-att", sides={"legendWording": "old-legend"})
        other_type = _attestation_envelope(
            "other-att", type="manifest-approval",
            sides={"manifestWording": "m"})
        scoped = _attestation_envelope("scoped-att", edition="na")
        wrong_fields = _attestation_envelope("fields-att")
        wrong_fields["record"].pop("note")
        denied = _attestation_envelope("denied-att")

        def authorization(envelope):
            if envelope["digest"] == "denied-att":
                return ["approval is pending"]
            return []

        resolution = recordresolver.classify(
            "attestation",
            [current, stale_side, other_type, scoped, wrong_fields, denied],
            _attestation_context(authorization_problems=authorization))
        self.assertEqual(list(resolution.current_authorizations), [current])
        self.assertEqual(
            list(resolution.superseded_evidence),
            [stale_side, other_type, scoped])
        self.assertEqual(
            [item.digest for item in resolution.invalid_records],
            ["fields-att"])
        self.assertEqual(
            [item.digest for item in resolution.rejected_authorizations],
            ["denied-att"])


if __name__ == "__main__":
    unittest.main()
