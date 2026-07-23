"""Regression tests for gateway and verification-plane enforcement."""

import copy
import json
import os
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib import (bundlezip, canon, gateway, model, projections,
                 recordprovenance, release)  # noqa: E402


PLANES = {
    "kinds": {
        "candidate": "artifact",
        "attestation": "verification",
    },
    "commands": {
        "candidate": {"reads": [], "writes": ["candidate"]},
        "reader": {"reads": ["candidate", "attestation"], "writes": []},
        "attest": {"reads": ["attestation"], "writes": ["attestation"]},
        "migrate": {"reads": [], "writes": ["source:relation-set"]},
    },
}


class TestGatewayPaths(unittest.TestCase):

    def test_content_gateway_rejects_a_file_that_changes_between_reads(self):
        with tempfile.TemporaryDirectory() as root:
            path = os.path.join(root, "input.txt")
            with open(path, "wb") as fh:
                fh.write(b"first")
            content = gateway.ContentGateway(root)
            self.assertEqual(content.read_bytes("input.txt"), b"first")
            with open(path, "wb") as fh:
                fh.write(b"second")
            with self.assertRaisesRegex(gateway.GatewayError,
                                        "changed between reads"):
                content.read_bytes("input.txt")

    def test_all_file_gateways_reject_tree_escapes(self):
        with tempfile.TemporaryDirectory() as root:
            content = gateway.ContentGateway(root)
            output = gateway.OutputGateway(root, "candidate", PLANES)
            artifact = gateway.ArtifactGateway(root, "reader", PLANES)
            attempts = (
                lambda p: content.read_bytes(p),
                lambda p: output.write("candidate", p, b"x"),
                lambda p: artifact.read("candidate", p),
                lambda p: gateway.write_source(
                    "migrate", PLANES, root, "source:relation-set", p, b"x"),
            )
            for attempt in attempts:
                for bad in ("../escape", "/absolute/path", ""):
                    with self.subTest(attempt=attempt, path=bad):
                        with self.assertRaises(gateway.GatewayError):
                            attempt(bad)

    def test_gateway_rejects_noncanonical_relative_path_aliases(self):
        with tempfile.TemporaryDirectory() as root:
            for bad in ("a/../b", "./b", "a//b", "a\\b", "a\x00b",
                        "C:/b"):
                with self.subTest(path=bad):
                    with self.assertRaisesRegex(
                            gateway.GatewayError,
                            "canonical platform-neutral relative identity"):
                        gateway._safe_path(root, bad)

    def test_content_allowlist_rejects_aliases_and_duplicate_identities(self):
        with tempfile.TemporaryDirectory() as root:
            for bad in (["a/../b"], ["./b"], ["a\\b"], ["b", "b"],
                        ["Path", "path"], "not-a-sequence"):
                with self.subTest(allowlist=bad):
                    with self.assertRaises(gateway.GatewayError):
                        gateway.ContentGateway(root, allowlist=bad)

    def test_edition_id_cannot_inject_a_path_component(self):
        import build as build_mod
        for bad in ("../na", "sub/na", "NA", "_na", "na\\other", ""):
            with self.subTest(edition=bad):
                with self.assertRaisesRegex(SystemExit, "edition id"):
                    build_mod.edition_path(bad)
        self.assertEqual(build_mod.edition_path("na"),
                         "navigator/editions/na.json")

    def test_content_plane_cannot_read_artifact_or_verification_outputs(self):
        with tempfile.TemporaryDirectory() as root:
            for relative in ("navigator/dist/candidate.html",
                             "navigator/DIST/candidate.html",
                             "NAVIGATOR/dist/candidate.html",
                             "navigator/records/qa-record_deadbeef.json",
                             "navigator/RECORDS/qa-record_deadbeef.json"):
                path = os.path.join(root, relative)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "wb") as fh:
                    fh.write(b"derived")
                for allowlist in (None, [relative]):
                    with self.subTest(path=relative, allowlist=allowlist):
                        content = gateway.ContentGateway(
                            root, allowlist=allowlist)
                        with self.assertRaisesRegex(
                                gateway.GatewayError, "terminal plane"):
                            content.read_bytes(relative)

            alias = os.path.join(root, "content-alias")
            try:
                os.symlink(os.path.join(root, "navigator", "dist"), alias)
            except (OSError, NotImplementedError):  # pragma: no cover
                return
            with self.assertRaisesRegex(gateway.GatewayError,
                                        "symlink alias|terminal plane"):
                gateway.ContentGateway(
                    root, allowlist=["content-alias/candidate.html"]
                ).read_bytes("content-alias/candidate.html")

    def test_artifact_kind_cannot_alias_another_kinds_path(self):
        nav = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(nav, "schema", "planes.json"),
                  encoding="utf-8") as fh:
            planes = json.load(fh)
        candidate_name = "candidate_release.html"
        with tempfile.TemporaryDirectory() as root:
            candidate_path = os.path.join(root, candidate_name)
            with open(candidate_path, "wb") as fh:
                fh.write(b"QA-bound candidate")
            output = gateway.OutputGateway(root, "bundle", planes)
            with self.assertRaisesRegex(gateway.GatewayError,
                                        "bundle-manifest.*may not use path"):
                output.write("bundle-manifest", candidate_name, b"manifest")
            with open(candidate_path, "rb") as fh:
                self.assertEqual(fh.read(), b"QA-bound candidate")

    def test_bundle_config_rejects_manifest_candidate_path(self):
        nav = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(nav, "bundles", "na-af-2026.json"),
                  encoding="utf-8") as fh:
            config = json.load(fh)
        sealed = next(member["name"] for member in config["members"]
                      if member["kind"] == "sealed")
        manifest = next(member for member in config["members"]
                        if member["kind"] == "bundle-manifest")
        manifest["name"] = "candidate_" + sealed
        with self.assertRaisesRegex(bundlezip.BundleError,
                                    "bundle-manifest.*may not use path"):
            bundlezip.validate_bundle_config(config)

    def test_source_write_privileges_are_exact_and_path_scoped(self):
        planes = copy.deepcopy(PLANES)
        planes["commands"]["migrate"]["writes"] = [
            "source:relation-set", "source:gate-inventory-locators"]
        with tempfile.TemporaryDirectory() as root:
            os.makedirs(os.path.join(root, "navigator", "relations"))
            os.makedirs(os.path.join(root, "navigator", "profiles"))
            with self.assertRaisesRegex(gateway.GatewayError, "source kind"):
                gateway.write_source(
                    "migrate", planes, root, "source:unknown",
                    "navigator/relations/example.json", b"{}")
            with self.assertRaisesRegex(gateway.GatewayError, "may not write path"):
                gateway.write_source(
                    "migrate", planes, root, "source:relation-set",
                    "navigator/profiles/gates_example.json", b"{}")
            with self.assertRaisesRegex(gateway.GatewayError, "may not write path"):
                gateway.write_source(
                    "migrate", planes, root,
                    "source:gate-inventory-locators",
                    "navigator/relations/example.json", b"{}")
            gateway.write_source(
                "migrate", planes, root, "source:relation-set",
                "navigator/relations/example.json", b"{}")
            self.assertTrue(os.path.exists(os.path.join(
                root, "navigator", "relations", "example.json")))

    def test_symlink_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as root, \
                tempfile.TemporaryDirectory() as outside:
            link = os.path.join(root, "link")
            try:
                os.symlink(outside, link)
            except (OSError, NotImplementedError):  # pragma: no cover
                self.skipTest("symlinks unavailable on this platform")
            with self.assertRaises(gateway.GatewayError):
                gateway.OutputGateway(root, "candidate", PLANES).write(
                    "candidate", "link/escaped.html", b"x")

    def test_in_tree_symlink_alias_is_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            target = os.path.join(root, "source.txt")
            with open(target, "wb") as fh:
                fh.write(b"source")
            alias = os.path.join(root, "alias.txt")
            try:
                os.symlink(target, alias)
            except (OSError, NotImplementedError):  # pragma: no cover
                self.skipTest("symlinks unavailable on this platform")
            with self.assertRaisesRegex(gateway.GatewayError,
                                        "symlink alias"):
                gateway.ContentGateway(
                    root, allowlist=["alias.txt"]).read_bytes("alias.txt")


class TestVerificationRecords(unittest.TestCase):

    def test_append_uses_atomic_exclusive_creation(self):
        with tempfile.TemporaryDirectory() as root, \
                mock.patch.object(gateway.os, "open",
                                  wraps=gateway.os.open) as open_file:
            gateway.VerificationGateway(root, "attest", PLANES).append(
                "attestation", {"record": "atomic"})
            flags = open_file.call_args.args[1]
            self.assertTrue(flags & os.O_CREAT)
            self.assertTrue(flags & os.O_EXCL)

    def test_new_record_filenames_use_the_full_digest_address(self):
        with tempfile.TemporaryDirectory() as root:
            writer = gateway.VerificationGateway(root, "attest", PLANES)
            prefix = "a" * 24
            digests = (
                "sha256/c1:" + prefix + ("1" * 40),
                "sha256/c1:" + prefix + ("2" * 40),
            )
            with mock.patch.object(
                    canon, "composite_digest", side_effect=digests):
                first_digest, first_name = writer.append(
                    "attestation", {"record": 1})
                second_digest, second_name = writer.append(
                    "attestation", {"record": 2})
            self.assertNotEqual(first_name, second_name)
            self.assertEqual(first_name,
                             "attestation_%s.json" % first_digest[10:])
            self.assertEqual(second_name,
                             "attestation_%s.json" % second_digest[10:])

    def test_read_recomputes_digest_address_and_canonical_bytes(self):
        with tempfile.TemporaryDirectory() as root:
            writer = gateway.VerificationGateway(root, "attest", PLANES)
            _, name = writer.append(
                "attestation", {"type": "example", "sides": {"a": "b"}})
            reader = gateway.VerificationGateway(root, "reader", PLANES)
            self.assertEqual(len(reader.read_all("attestation")), 1)

            path = os.path.join(root, name)
            with open(path, "rb") as fh:
                envelope = json.loads(fh.read().decode("utf-8"))
            envelope["record"]["sides"]["a"] = "tampered"
            with open(path, "wb") as fh:
                fh.write(canon.canonical_json(envelope))
            with self.assertRaisesRegex(gateway.GatewayError,
                                        "digest does not match"):
                reader.read_all("attestation")

    def test_current_repository_records_verify(self):
        nav = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(nav, "schema", "planes.json"),
                  encoding="utf-8") as fh:
            planes = json.load(fh)
        records = os.path.join(nav, "records")
        reader = gateway.VerificationGateway(records, "status", planes)
        with open(os.path.join(nav, "schema", "acceptance.json"),
                  encoding="utf-8") as fh:
            acceptance = json.load(fh)
        active = acceptance["runner"]["activeReleaseProfile"]
        profile = next(
            item for item in acceptance["runner"]["releaseProfiles"]
            if item["id"] == active)
        for kind in ("attestation", "qa-record", "release-record",
                     "bundle-record"):
            envelopes = reader.read_all(kind)
            if kind == "qa-record" and \
                    profile["manualQaEvidence"] == "deferred":
                self.assertEqual(envelopes, [], kind)
            else:
                self.assertTrue(envelopes, kind)
            for envelope in envelopes:
                self.assertEqual(
                    recordprovenance.current_record_format_problems(
                        kind, envelope["record"]), [], envelope["digest"])

    def test_release_rejects_stale_attestation_referenced_by_qa(self):
        att_record = {"type": "example", "sides": {"left": "old"}}
        att_digest = canon.composite_digest(
            "aa11393:attestation:c1", att_record)
        att = {"kind": "attestation", "digest": att_digest,
               "record": att_record}
        qa = {"record": {"candidateDigest": "candidate",
                         "lockDigest": "lock",
                         "attestations": [att_digest]}}
        problems = release.verify_envelope(
            qa, "candidate", "lock", [att], {"left": "new"})
        self.assertTrue(any("not current" in p for p in problems), problems)


class TestAuthorityPin(unittest.TestCase):

    def test_each_edition_reads_and_verifies_its_explicit_authority(self):
        root = os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))))
        for edition in ("na", "af"):
            path = "navigator/editions/%s.json" % edition
            boot = gateway.ContentGateway(root)
            config = json.loads(boot.read_text(path))
            content = gateway.ContentGateway(
                root, allowlist=config["declaredTransitiveInputs"])
            m = model.EditionModel(content, path)
            authority_id = config["authorityCorpus"]
            entry = m.registry.entry(authority_id)
            self.assertEqual(m.authority_digest,
                             entry["files"][entry["primary"]])
            self.assertEqual(content.read_log[entry["primary"]],
                             m.authority_digest)

            # Provenance is driven by the edition's explicit authority,
            # never whichever authoritative corpus happens to sort last.
            m.registry.corpora["unrelated-authority"] = {
                "role": "authoritative", "visibility": "internal",
                "version": "unrelated", "primary": "elsewhere.pdf",
                "files": {"elsewhere.pdf": "sha256/c1:" + ("f" * 64)},
            }
            self.assertEqual(projections.provenance(m)["authority"]["id"],
                             authority_id)


if __name__ == "__main__":
    unittest.main()
