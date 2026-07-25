"""Focused contract tests for the XML-only typed navigator model."""

from dataclasses import FrozenInstanceError, replace
import os
import re
import unittest

from navigator.lib.gateway import ContentGateway, GatewayError
from navigator.lib.claims import ClaimsParseError, dependency_references
from navigator.lib.model import EditionModel, ModelError, bundle_manifest_text
from navigator.lib import bundlezip, canon, projections
from navigator.lib.validate import validate_edition


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))


class XMLModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.models = {
            edition: EditionModel(
                ContentGateway(ROOT),
                "navigator/editions/%s.json" % edition)
            for edition in ("na", "af")
        }

    def test_live_editions_have_exact_claim_and_mapping_census(self):
        expected = {"na": (30, 77), "af": (23, 61)}
        for edition, model in self.models.items():
            with self.subTest(edition=edition):
                claims, units = expected[edition]
                self.assertEqual(len(model.claims), claims)
                self.assertEqual(len(model.units_by_fragment), units)
                self.assertEqual(len(model.relations.mappings), units)
                self.assertEqual(
                    {item.subject.fragment_id
                     for item in model.relations.mappings},
                    set(model.units_by_fragment))
                self.assertEqual(validate_edition(model), ())

    def test_reverse_relations_order_claim_units_before_claim_phrases(self):
        for edition, model in self.models.items():
            with self.subTest(edition=edition):
                for references in model.reverse_index.values():
                    keys = []
                    for reference in references:
                        unit = model.units_by_fragment[
                            reference.subject_fragment_id]
                        keys.append((
                            unit.claim_number,
                            0 if reference.kind == "mapping" else 1,
                            unit.unit_index,
                            reference.relation_id,
                        ))
                    self.assertEqual(keys, sorted(keys))

    def test_sources_are_typed_registered_xml_only(self):
        for edition, model in self.models.items():
            with self.subTest(edition=edition):
                claim, pct = model.source_documents
                self.assertEqual(
                    (claim.authority_scheme, claim.xml_role),
                    ("authored-markdown-v1", "generated-xml"))
                self.assertEqual(
                    (pct.authority_scheme, pct.xml_role),
                    ("pdf-evidence-transcription-v1", "transcription-xml"))
                self.assertTrue(all(item.registered_path.endswith(".source.xml")
                                    for item in model.source_documents))
                paths = {path for path, _digest in model.read_inventory}
                self.assertFalse(any(path.endswith((".md", ".pdf"))
                                     for path in paths))
                self.assertFalse(any(path.startswith(("navigator/dist/",
                                                      "navigator/records/"))
                                     for path in paths))

    def test_pct_boundary_assets_and_code_are_typed(self):
        model = self.models["na"]
        self.assertEqual(set(model.assets), {
            "asset-fig-1-png", "asset-fig-2-png",
            "asset-fig-3-png", "asset-fig-4-png"})
        self.assertEqual(len(model._editorial_ids), 6)
        code = [node for node in model.disclosure_index.values()
                if node.kind == "codeBlock"]
        self.assertEqual(len(code), 12)
        self.assertTrue(all(node.text.strip() for node in code))

    def test_typed_values_and_indexes_are_immutable(self):
        model = self.models["af"]
        unit = next(iter(model.units_by_fragment.values()))
        with self.assertRaises(FrozenInstanceError):
            unit.text = "changed"
        with self.assertRaises(TypeError):
            model.units_by_fragment[unit.fragment_id] = unit
        with self.assertRaises(TypeError):
            model.reverse_index["new-target"] = ()
        with self.assertRaises(AttributeError):
            model.edition_id = "na"
        self.assertFalse(hasattr(model, "gw"))
        self.assertFalse(hasattr(model, "registry"))
        self.assertIsNone(model._document_artifacts)
        changed_lock = model.content_lock
        changed_lock["reads"].clear()
        self.assertTrue(model.content_lock["reads"])
        self.assertNotEqual(
            model.dom_id("a", "b-c"), model.dom_id("a-b", "c"))

    def test_controlled_wording_has_exact_slots(self):
        model = self.models["na"]
        self.assertEqual(
            model.profile_label,
            model.controlled_text("artifact-label-technical-preview"))
        text = model.controlled_text("standing-disclaimer")
        self.assertIn(model.claim_set_version, text)
        with self.assertRaises(ModelError):
            model.controlled_text("bundle-manifest-neutral")
        bundle = bundle_manifest_text(self.models["na"], self.models["af"])
        self.assertIn(self.models["na"].claim_set_version, bundle)
        self.assertIn(self.models["af"].claim_set_version, bundle)

    def test_substantive_origins_are_computed_and_non_persistent(self):
        expected_controls = {
            "edition:" + field for field in (
                "artifactName", "census", "claimPackageId",
                "claimSetVersion", "consumerId",
                "declaredReleaseTimestamp", "displayName", "editionId",
                "editionVersion", "editionWordingPath", "groups",
                "independentClaims",
                "relationPath", "strategyName", "strategyPrefix")
        }
        for edition, model in self.models.items():
            with self.subTest(edition=edition):
                identifiers = [item.value_id
                               for item in model.origin_inventory]
                self.assertEqual(len(identifiers), len(set(identifiers)))
                self.assertTrue(expected_controls.issubset(identifiers))
                self.assertTrue(any(item.kind == "source-item"
                                    for item in model.origin_inventory))
                self.assertTrue(any(item.kind == "relation-target"
                                    for item in model.origin_inventory))
                self.assertTrue(any(item.kind == "controlled-wording"
                                    for item in model.origin_inventory))
                standing = next(
                    item for item in model.origin_inventory
                    if item.value_id == "wording:standing-disclaimer")
                self.assertEqual(
                    standing.owner_path,
                    "navigator/wording/shared.wording.xml")

        config_path = os.path.join(
            ROOT, *bundlezip.BUNDLE_CONFIG_PATH.split("/"))
        with open(config_path, "rb") as handle:
            config_bytes = handle.read()
        config = canon.parse_json(config_bytes)
        bundle_origins = projections.bundle_origin_inventory(
            self.models["na"], self.models["af"], config,
            canon.bytes_digest(config_bytes), bundlezip.BUNDLE_CONFIG_PATH)
        self.assertEqual(len(bundle_origins), 12)
        self.assertEqual(
            {item.value_id for item in bundle_origins
             if item.value_id.startswith("wording:")},
            {
                "wording:bundle-manifest-neutral:slot:naEditionVersion",
                "wording:bundle-manifest-neutral:slot:afEditionVersion",
            })

    def test_gateway_rejects_unsafe_or_changing_inputs(self):
        gateway = ContentGateway(ROOT)
        for path in (
                "../README.md", "/README.md", "navigator\\editions\\na.json",
                ".git/config", "navigator/dist/product.html"):
            with self.subTest(path=path), self.assertRaises(GatewayError):
                gateway.read_bytes(path)

        calls = 0

        def changing_source(_absolute):
            nonlocal calls
            calls += 1
            return b"first\n" if calls == 1 else b"second\n"

        changing = ContentGateway(ROOT, byte_source=changing_source)
        changing.read_bytes("README.md")
        with self.assertRaises(GatewayError):
            changing.read_bytes("README.md")

        exact = ContentGateway(ROOT)
        exact.read_bytes("README.md")
        with self.assertRaises(GatewayError):
            exact.seal({"README.md", "GLOSSARY.md"})
        exact.seal({"README.md"})
        with self.assertRaises(GatewayError):
            exact.read_bytes("GLOSSARY.md")

    def test_dependency_grammar_is_exactly_singular(self):
        self.assertEqual(
            dependency_references("The method of claim 12, wherein"), (12,))
        for text in (
                "The method of claims 1 and 2",
                "The method of claim 1 or 2",
                "The method of claim 1-3",
                "The method of claim 1, 2, or 3"):
            with self.subTest(text=text), self.assertRaises(ClaimsParseError):
                dependency_references(text)

    def test_stale_relation_digest_fails_during_construction(self):
        relation_suffix = os.path.join(
            "navigator", "relations", "na__pct.relations.xml")

        def tampered_source(absolute):
            with open(absolute, "rb") as handle:
                data = handle.read()
            if absolute.endswith(relation_suffix):
                match = re.search(
                    rb'fragmentContentDigest="sha256/xc1/ssp-xd1:([0-9a-f]{64})"',
                    data)
                self.assertIsNotNone(match)
                position = match.start(1)
                replacement = b"1" if data[position:position + 1] == b"0" else b"0"
                data = data[:position] + replacement + data[position + 1:]
            return data

        with self.assertRaises(ModelError):
            EditionModel(
                ContentGateway(ROOT, byte_source=tampered_source),
                "navigator/editions/na.json")

    def test_validator_recomputes_dependency_projection(self):
        model = EditionModel(
            ContentGateway(ROOT), "navigator/editions/na.json")
        object.__setattr__(model, "parents", {})
        defects = validate_edition(model)
        self.assertTrue(any(code == "dependencies" for code, _message in defects))

    def test_validator_rejects_overlapping_phrases_and_cross_target_repeats(self):
        model = EditionModel(
            ContentGateway(ROOT), "navigator/editions/na.json")
        phrases = list(model.relations.phrase_mappings)
        first = phrases[0]
        unit = model.units_by_fragment[first.parent.fragment_id]
        phrases[1] = replace(
            phrases[1], parent=first.parent, unit_kind=first.unit_kind,
            unit_index=first.unit_index,
            exact_text=unit.text[first.start + 1:first.end],
            start=first.start + 1, end=first.end)
        object.__setattr__(model, "relations", replace(
            model.relations, phrase_mappings=tuple(phrases)))
        defects = validate_edition(model)
        self.assertTrue(any("overlaps" in message
                            for _code, message in defects))

        model = EditionModel(
            ContentGateway(ROOT), "navigator/editions/na.json")
        mappings = list(model.relations.mappings)
        index = next(index for index, item in enumerate(mappings)
                     if len(item.targets) > 1)
        selected = mappings[index]
        targets = list(selected.targets)
        targets[1] = replace(
            targets[1], endpoints=(targets[0].endpoints[0],))
        mappings[index] = replace(selected, targets=tuple(targets))
        object.__setattr__(model, "relations", replace(
            model.relations, mappings=tuple(mappings)))
        defects = validate_edition(model)
        self.assertTrue(any("across candidate targets" in message
                            for _code, message in defects))

    def test_wording_origins_and_editorial_targeting_fail_closed(self):
        wording_suffix = os.path.join(
            "navigator", "wording", "shared.wording.xml")

        def wrong_origin(absolute):
            with open(absolute, "rb") as handle:
                data = handle.read()
            if absolute.endswith(wording_suffix):
                data = data.replace(
                    b'originRef="edition.claimSetVersion"',
                    b'originRef="edition.unitCount"', 1)
            return data

        with self.assertRaises(ModelError):
            EditionModel(
                ContentGateway(ROOT, byte_source=wrong_origin),
                "navigator/editions/na.json")

        shared_suffix = os.path.join(
            "navigator", "wording", "shared.wording.xml")
        edition_suffix = os.path.join(
            "navigator", "wording", "na.wording.xml")
        with open(os.path.join(ROOT, shared_suffix), "rb") as handle:
            shared_bytes = handle.read()
        match = re.search(
            rb'  <entry wordingId="standing-disclaimer".*?  </entry>\n',
            shared_bytes, re.DOTALL)
        self.assertIsNotNone(match)
        moved_entry = match.group(0)

        def moved_to_wrong_scope(absolute):
            with open(absolute, "rb") as handle:
                data = handle.read()
            if absolute.endswith(shared_suffix):
                data = data.replace(moved_entry, b"", 1)
            elif absolute.endswith(edition_suffix):
                data = data.replace(b"</wording>\n", moved_entry + b"</wording>\n")
            return data

        with self.assertRaises(ModelError):
            EditionModel(
                ContentGateway(ROOT, byte_source=moved_to_wrong_scope),
                "navigator/editions/na.json")

        live = self.models["na"]
        editorial = next(node for node in live.disclosure_index.values()
                         if node.editorial)
        pct_id = live.source_documents[1].document_id.encode("utf-8")
        relation_suffix = os.path.join(
            "navigator", "relations", "na__pct.relations.xml")
        pattern = re.compile(
            rb'documentId="' + re.escape(pct_id) +
            rb'" fragmentId="[^"]+" fragmentContentDigest="[^"]+"')
        replacement = (
            b'documentId="' + pct_id + b'" fragmentId="' +
            editorial.fragment_id.encode("utf-8") +
            b'" fragmentContentDigest="' +
            editorial.content_digest.encode("ascii") + b'"')

        def editorial_target(absolute):
            with open(absolute, "rb") as handle:
                data = handle.read()
            if absolute.endswith(relation_suffix):
                data, count = pattern.subn(replacement, data, count=1)
                self.assertEqual(count, 1)
            return data

        with self.assertRaises(ModelError):
            EditionModel(
                ContentGateway(ROOT, byte_source=editorial_target),
                "navigator/editions/na.json")


if __name__ == "__main__":
    unittest.main()
