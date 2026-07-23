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
from lib import projections, render, render_inventory  # noqa: E402


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


if __name__ == "__main__":
    unittest.main()
