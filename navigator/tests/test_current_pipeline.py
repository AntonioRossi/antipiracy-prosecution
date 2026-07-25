"""Small end-to-end contracts for the sole current navigator pipeline."""

from __future__ import annotations

import os
import stat
import tempfile
import unittest
from unittest import mock

from navigator import build
from navigator.lib import (
    acceptance, bundlezip, canon, currentstate, release, schema_validate,
)


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))


def _json(relative):
    with open(os.path.join(ROOT, *relative.split("/")), "rb") as handle:
        return canon.parse_json(handle.read())


class CurrentPipelineTests(unittest.TestCase):
    def test_live_navigator_input_inventory_is_exact(self):
        class Entry:
            def __init__(self, path):
                self.path = path

        class Snapshot:
            def __init__(self, paths):
                self.entries = tuple(Entry(path) for path in paths)

        currentstate._verify_navigator_input_inventory(
            Snapshot(currentstate.NAVIGATOR_INPUT_PATHS))
        for paths in (
                currentstate.NAVIGATOR_INPUT_PATHS - {
                    "navigator/wording/af.wording.xml"},
                currentstate.NAVIGATOR_INPUT_PATHS | {
                    "navigator/relations/copy.relations.xml"}):
            with self.subTest(paths=paths), \
                    self.assertRaises(currentstate.CurrentStateError):
                currentstate._verify_navigator_input_inventory(Snapshot(paths))

    def test_command_boundary_is_exact_and_legacy_commands_are_rejected(self):
        self.assertEqual(build.COMMANDS, (
            "preview", "candidate", "release", "bundle",
            "validate-current"))
        self.assertEqual(set(build.USAGE), set(build.COMMANDS))
        for command in (
                "approve", "attest", "callback", "migrate", "pin",
                "plan", "qa", "record", "verify-release"):
            with self.subTest(command=command), \
                    self.assertRaises(build.CommandError):
                build._dispatch([command])
        with self.assertRaises(build.CommandError):
            build._dispatch(["preview", "na", "--callback"])

    def test_acceptance_registry_is_exact_text_only_contract(self):
        registry = acceptance.load_registry(ROOT)
        self.assertEqual(
            [item["id"] for item in registry["criteria"]],
            ["AC-%02d" % number for number in range(1, 21)])
        self.assertEqual(
            [item["scope"] for item in registry["criteria"]],
            ["edition"] * 18 + ["shared", "bundle"])
        self.assertTrue(all(set(item) == {"id", "scope", "text"}
                            for item in registry["criteria"]))

        for field in ("approval", "check", "evidence", "owner", "receipt"):
            changed = {
                "acceptanceVersion": registry["acceptanceVersion"],
                "criteria": [dict(item) for item in registry["criteria"]],
            }
            changed["criteria"][0][field] = "legacy-control"
            with self.subTest(field=field), \
                    self.assertRaises(acceptance.AcceptanceError):
                acceptance.validate_registry(changed)

        changed = {
            "acceptanceVersion": registry["acceptanceVersion"],
            "criteria": [dict(item) for item in registry["criteria"]],
        }
        changed["criteria"][8]["text"] = "Arbitrary untested outcome."
        changed_bytes = canon.canonical_json(changed) + b"\n"

        def mismatched_contract(absolute):
            if absolute.endswith(acceptance.ACCEPTANCE_PATH):
                return changed_bytes
            with open(absolute, "rb") as handle:
                return handle.read()

        with self.assertRaises(acceptance.AcceptanceError):
            acceptance.load_registry(ROOT, mismatched_contract)
        with self.assertRaises(acceptance.AcceptanceError):
            acceptance.passed_result(
                registry, tuple(sorted(acceptance.TEST_COVERAGE))[:-1])
        result = acceptance.passed_result(
            registry, tuple(sorted(acceptance.TEST_COVERAGE)))
        self.assertEqual(
            [item["id"] for item in result["results"]],
            list(acceptance.CRITERIA))

    def test_preview_derives_bytes_without_writing(self):
        source = object()

        class Frozen:
            @staticmethod
            def byte_source():
                return source

        frozen = Frozen()
        with mock.patch.object(build, "_snapshot", return_value=frozen), \
                mock.patch.object(
                    build.currentstate, "verify_structured_source") as upstream, \
                mock.patch.object(
                    build.currentstate, "derive",
                    return_value=(object(), b"<html>preview</html>", {})) \
                as derive, \
                mock.patch.object(build, "_assert_unchanged") as unchanged, \
                mock.patch.object(build, "_assert_only_outputs_changed") \
                as output_check, \
                mock.patch.object(build.release, "write_outputs_atomic") \
                as write:
            result = build.cmd_preview("na")

        self.assertEqual(result, b"<html>preview</html>")
        upstream.assert_called_once_with(frozen, ("navigator-na",))
        derive.assert_called_once_with("na", "preview", source)
        unchanged.assert_called_once_with(frozen, "preview")
        output_check.assert_not_called()
        write.assert_not_called()

    def test_generated_writes_are_atomic_generated_only_and_safe(self):
        with tempfile.TemporaryDirectory(
                prefix="aa11393-current-products-") as directory:
            outputs = {"b.html": b"second", "a.html": b"first"}
            written = release.write_outputs_atomic(directory, outputs)
            self.assertEqual(
                [item["name"] for item in written], ["a.html", "b.html"])
            for name, data in outputs.items():
                path = os.path.join(directory, name)
                with open(path, "rb") as handle:
                    self.assertEqual(handle.read(), data)
                self.assertEqual(stat.S_IMODE(os.stat(path).st_mode), 0o644)

            a_path = os.path.join(directory, "a.html")
            with open(a_path, "wb") as handle:
                handle.write(b"operative")
            with self.assertRaises(release.ReleaseError):
                release.write_outputs_atomic(
                    directory, {"a.html": b"staged", "c.html": "not-bytes"})
            with open(a_path, "rb") as handle:
                self.assertEqual(handle.read(), b"operative")
            self.assertFalse(any(name.startswith(".")
                                 for name in os.listdir(directory)))

            with mock.patch.object(
                    release.os, "chmod", side_effect=OSError("chmod failed")):
                with self.assertRaises(OSError):
                    release.write_outputs_atomic(directory, {"d.html": b"x"})
            self.assertFalse(any(name.startswith(".")
                                 for name in os.listdir(directory)))
            self.assertFalse(os.path.exists(os.path.join(directory, "d.html")))

            for name in ("../escape", "/absolute", "nested/file", "CON"):
                with self.subTest(name=name), \
                        self.assertRaises(release.ReleaseError):
                    release.write_outputs_atomic(directory, {name: b"x"})

        with tempfile.TemporaryDirectory(
                prefix="aa11393-current-products-link-") as container:
            real = os.path.join(container, "real")
            link = os.path.join(container, "link")
            os.mkdir(real)
            os.symlink(real, link)
            with self.assertRaises(release.ReleaseError):
                release.write_outputs_atomic(link, {"x.html": b"x"})

    def test_five_member_bundle_and_checksums_are_deterministic(self):
        na = b"<html>NA</html>"
        af = b"<html>AF</html>"
        members = [
            ("na.html", na),
            ("na.html.sha256", release.checksum_text("na.html", na)),
            ("af.html", af),
            ("af.html.sha256", release.checksum_text("af.html", af)),
            ("MANIFEST.txt", b"current two-edition bundle\n"),
        ]
        first = bundlezip.build_zip(members, "2026-07-24T16:46:48Z")
        second = bundlezip.build_zip(members, "2026-07-24T16:46:48Z")
        self.assertEqual(first, second)
        self.assertEqual(bundlezip.read_zip_members(first), members)
        checksum = release.checksum_text("bundle.zip", first)
        self.assertEqual(
            release.verify_checksum(checksum, "bundle.zip", first),
            canon.bytes_digest(first))
        with self.assertRaises(bundlezip.BundleError):
            bundlezip.build_zip(members[:-1], "2026-07-24T16:46:48Z")

    def test_closed_configs_reject_removed_fields_and_surfaces_are_absent(self):
        schema = _json("navigator/schema/edition.schema.json")
        edition = _json("navigator/editions/na.json")
        schema_validate.check_schema(schema)
        self.assertEqual(schema_validate.validate(edition, schema), [])
        for field in (
                "approvalInventory", "compatibilityAuthorization",
                "migrationSource", "pinPlan", "qaProfile"):
            changed = dict(edition)
            changed[field] = "removed"
            with self.subTest(edition_field=field):
                self.assertTrue(schema_validate.validate(changed, schema))

        config = _json("navigator/bundles/na-af-2026.json")
        bundlezip.validate_bundle_config(config)
        changed = dict(config)
        changed["name"] = "arbitrary_TECHNICAL-PREVIEW.zip"
        with self.assertRaises(bundlezip.BundleError):
            bundlezip.validate_bundle_config(changed)
        for field in (
                "authorizationChain", "compatibilityAuthorization",
                "receipt", "releasePlan"):
            changed = dict(config)
            changed[field] = "removed"
            with self.subTest(bundle_field=field), \
                    self.assertRaises(bundlezip.BundleError):
                bundlezip.validate_bundle_config(changed)

        removed_files = (
            "navigator/bundle-manifest.json",
            "navigator/corpora.json",
            "navigator/relations/na__pct.json",
            "navigator/schema/commands.json",
            "navigator/schema/planes.json",
            "navigator/schema/release-policy.json",
            "navigator/strings.json",
        )
        self.assertFalse(any(os.path.isfile(os.path.join(ROOT, *path.split("/")))
                             for path in removed_files))
        for path in ("navigator/profiles", "navigator/records",
                     "navigator/tools"):
            absolute = os.path.join(ROOT, *path.split("/"))
            files = []
            if os.path.isdir(absolute):
                files = [name for name in os.listdir(absolute)
                         if os.path.isfile(os.path.join(absolute, name))]
            self.assertEqual(files, [], path)


if __name__ == "__main__":
    unittest.main()
