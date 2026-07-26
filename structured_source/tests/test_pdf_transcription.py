"""Focused PDF-transcription authority, surface, coverage, and handoff tests."""

from dataclasses import FrozenInstanceError, replace
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from navigator.lib.snapshot import RepositorySnapshot
from structured_source import parser, profiles
from structured_source.canonical import raw_digest
from structured_source.control import canonical_json
from structured_source.errors import StructuredSourceError
from structured_source.render import render_content
from structured_source.render import Projection
from structured_source.registry import validate_registry
from structured_source.tests.test_registry import registry_fixture
from structured_source.tests.test_xml_contract import CONTENT
from structured_source.verify import VerificationContext


ROOT = Path(__file__).resolve().parents[2]
PDF_BYTES = b"%PDF-1.4\n% closed test evidence\n"


def fixture_xml():
    return (CONTENT
            .replace(b"doc-alpha-root", b"pdf-doc-root")
            .replace(b"doc-alpha", b"pdf-doc")
            .replace(b"US/prior-art/A1/source.pdf", b"content/evidence.pdf")
            .replace(
                b'fragmentId="frag-heading" page="1" sourcePath="content/evidence.pdf"',
                b'fragmentId="frag-heading" page="1" region="heading region" '
                b'sourcePath="content/evidence.pdf"')
            .replace(
                b'fragmentId="frag-paragraph" page="1" sourcePath="content/evidence.pdf"',
                b'fragmentId="frag-paragraph" page="1" region="paragraph region" '
                b'sourcePath="content/evidence.pdf" '
                b'uncertainty="line break reviewed from image"'))


def fixture_manifest(pdf_bytes=PDF_BYTES):
    return {
        "assets": [],
        "convenienceDerivatives": [],
        "documentId": "pdf-doc",
        "extractionMethod": "registered-transcription",
        "manifestVersion": "1",
        "storedSource": {
            "officialCopyStatus": "repository-stored-evidence-copy",
            "path": "content/evidence.pdf",
            "rawDigest": raw_digest(pdf_bytes),
            "role": "prior-art-evidence-copy",
            "size": len(pdf_bytes),
        },
    }


def write_fixture(root, *, xml=None, manifest_change=None, markdown_change=None):
    root = Path(root)
    for control_path in parser.PARSER_CONTROL_PATHS:
        target = root / control_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / control_path).read_bytes())
    content = root / "content"
    content.mkdir(parents=True)
    xml = fixture_xml() if xml is None else xml
    (content / "evidence.pdf").write_bytes(PDF_BYTES)
    (content / "evidence.xml").write_bytes(xml)
    manifest = fixture_manifest()
    if manifest_change is not None:
        manifest_change(manifest)
    (content / "source-manifest.json").write_bytes(canonical_json(manifest))
    try:
        artifact = parser.parse_artifact(xml, "content-document")
        markdown = render_content(
            artifact, "content/evidence.md", {}).markdown
    except StructuredSourceError:
        markdown = b"invalid fixture\n"
    if markdown_change is not None:
        markdown = markdown_change(markdown)
    (content / "evidence.md").write_bytes(markdown)
    return registry_fixture()


def snapshot_context(root, registry, byte_source=None):
    snapshot = RepositorySnapshot.capture(root, retain_bytes=True)
    if byte_source is None:
        byte_source = snapshot.byte_source()
    return VerificationContext(
        root, registry=registry, byte_source=byte_source,
        repository_snapshot=snapshot)


class PDFItemSurface(unittest.TestCase):
    def test_every_live_pdf_package_builds_the_closed_surface(self):
        context = VerificationContext(os.fspath(ROOT))
        package_ids = [
            package_id for package_id, package in context.packages.items()
            if package["authorityScheme"] == "pdf-evidence-transcription-v1"]
        self.assertEqual(len(package_ids), 37)
        for package_id in package_ids:
            with self.subTest(package_id=package_id):
                result = context.check(package_id)
                surface = context._validated_package_state[package_id]["surface"]
                self.assertEqual(result["computedCoverage"]["coveredItems"],
                                 len(surface.items))
                self.assertGreater(surface.coverage_field_count, len(surface.items))
                self.assertEqual(surface.package_id, package_id)
                self.assertEqual(surface.authority_scheme,
                                 "pdf-evidence-transcription-v1")

    def test_surface_is_typed_ordered_immutable_and_exactly_provenanced(self):
        with tempfile.TemporaryDirectory() as root:
            registry = write_fixture(root)
            context = snapshot_context(root, registry)
            handoff = context.read_for_consumer("example-consumer", "pdf-doc")
        surface = handoff["surface"]
        self.assertEqual(
            [(item.item_id, item.item_type, item.parent_id, item.ordinal)
             for item in surface.items],
            [("frag-heading", "heading", None, 1),
             ("frag-paragraph", "paragraph", None, 2)])
        self.assertEqual(surface.item("frag-heading").metadata, (("level", 1),))
        self.assertEqual(
            (surface.document_item.item_id, surface.document_item.item_type,
             surface.document_item.child_ids),
            ("pdf-doc-root", "document",
             ("frag-heading", "frag-paragraph")))
        self.assertEqual(surface.item("pdf-doc-root"), surface.document_item)
        self.assertEqual(
            surface.children("pdf-doc-root"), surface.items)
        self.assertEqual(surface.document_item.source, surface.source)
        self.assertEqual(surface.item("frag-paragraph").provenance.uncertainty,
                         "line break reviewed from image")
        self.assertEqual(surface.children(), surface.items)
        self.assertEqual(handoff["bytes"], fixture_xml())
        self.assertEqual(handoff["assets"], {})
        with self.assertRaises(FrozenInstanceError):
            surface.items[0].ordinal = 9
        with self.assertRaises(TypeError):
            handoff["surface"] = None
        with self.assertRaises(TypeError):
            handoff["assets"]["changed"] = b"changed"
        with self.assertRaisesRegex(StructuredSourceError, "resolve exactly"):
            surface.item("missing")

    def test_insert_delete_reorder_and_source_number_do_not_rename_items(self):
        heading = b'''    <heading level="1" xml:id="frag-heading">
      <text>Alpha</text>
      <space />
      <strong>
        <text>Beta</text>
      </strong>
    </heading>'''
        paragraph = b'''    <paragraph xml:id="frag-paragraph">
      <text>One &lt; two</text>
      <lineBreak />
      <code>x &amp; y</code>
    </paragraph>'''
        original = parser.parse_artifact(CONTENT, "content-document")
        reordered = parser.parse_artifact(
            CONTENT.replace(heading + b"\n" + paragraph,
                            paragraph + b"\n" + heading),
            "content-document")
        inserted_xml = CONTENT.replace(
            b"  </provenance>",
            b'    <fragmentEvidence fragmentId="stable-new" page="1" '
            b'sourcePath="US/prior-art/A1/source.pdf" />\n'
            b"  </provenance>").replace(
                paragraph, paragraph +
                b'''\n    <paragraph xml:id="stable-new">
      <text>Inserted</text>
    </paragraph>''')
        inserted = parser.parse_artifact(inserted_xml, "content-document")
        deleted_xml = (CONTENT
                       .replace(
                           b'    <fragmentEvidence fragmentId="frag-heading" page="1" '
                           b'sourcePath="US/prior-art/A1/source.pdf" />\n', b"")
                       .replace(heading + b"\n", b""))
        deleted = parser.parse_artifact(deleted_xml, "content-document")
        numbered = parser.parse_artifact(
            CONTENT.replace(b"One &lt; two", b"17. One &lt; two"),
            "content-document")
        metadata_changed = parser.parse_artifact(
            CONTENT.replace(b'level="1"', b'level="2"'),
            "content-document")
        type_changed = parser.parse_artifact(
            CONTENT.replace(b'<paragraph xml:id="frag-paragraph">',
                            b'<plain xml:id="frag-paragraph">').replace(
                                b"</paragraph>", b"</plain>"),
            "content-document")
        for changed in (reordered, inserted, deleted):
            self.assertEqual(
                changed.fragment_digests["frag-paragraph"],
                original.fragment_digests["frag-paragraph"])
            self.assertNotEqual(
                changed.fragment_digests["doc-alpha-root"],
                original.fragment_digests["doc-alpha-root"])
        self.assertEqual(set(reordered.fragment_digests),
                         set(original.fragment_digests))
        self.assertIn("stable-new", inserted.fragment_digests)
        self.assertNotIn("frag-heading", deleted.fragment_digests)
        self.assertIn("frag-paragraph", numbered.fragment_digests)
        self.assertNotEqual(numbered.fragment_digests["frag-paragraph"],
                            original.fragment_digests["frag-paragraph"])
        self.assertNotEqual(metadata_changed.fragment_digests["frag-heading"],
                            original.fragment_digests["frag-heading"])
        self.assertNotEqual(type_changed.fragment_digests["frag-paragraph"],
                            original.fragment_digests["frag-paragraph"])

    def test_unknown_item_metadata_and_untyped_extension_fail_closed(self):
        mutations = (
            fixture_xml().replace(
                b'<paragraph xml:id="frag-paragraph"',
                b'<paragraph xml:id="frag-paragraph" confidence="high"'),
            fixture_xml().replace(
                b"<content>", b"<content><extension><text>hidden</text></extension>"),
            fixture_xml().replace(b"frag-paragraph", b"Frag.Paragraph"),
        )
        for xml in mutations:
            with self.subTest(xml=xml[-180:]), self.assertRaises(
                    StructuredSourceError):
                parser.parse_artifact(xml, "content-document")

    def test_missing_and_duplicate_item_provenance_fail_closed(self):
        evidence = (
            b'    <fragmentEvidence fragmentId="frag-heading" page="1" '
            b'region="heading region" sourcePath="content/evidence.pdf" />\n')
        mutations = (
            fixture_xml().replace(evidence, b""),
            fixture_xml().replace(evidence, evidence + evidence),
        )
        for xml in mutations:
            with self.subTest(xml=xml[:180]), tempfile.TemporaryDirectory() as root:
                registry = write_fixture(root, xml=xml)
                with self.assertRaises(StructuredSourceError):
                    VerificationContext(root, registry=registry).check("pdf-doc")

    def test_missing_wrong_kind_and_cyclic_document_dependencies_fail(self):
        for subject_id, message in (
                ("missing-doc", "digest is stale"),
                ("relation-doc", "digest is stale"),
                ("pdf-doc", "cycle")):
            dependency = (
                '<dependencies>\n    <dependency kind="document" '
                'subjectId="%s" />\n  </dependencies>' % subject_id).encode()
            xml = fixture_xml().replace(b"<dependencies />", dependency)
            with self.subTest(subject_id=subject_id), \
                    tempfile.TemporaryDirectory() as root:
                registry = write_fixture(root, xml=xml)
                with self.assertRaisesRegex(StructuredSourceError, message):
                    VerificationContext(
                        root, registry=registry).check("pdf-doc")


class PDFEvidenceAndCoverage(unittest.TestCase):
    def test_manifest_checksum_size_role_copy_method_and_ocr_authority_fail(self):
        changes = {
            "checksum": lambda value: value["storedSource"].update(
                rawDigest="sha256/raw:" + "0" * 64),
            "size": lambda value: value["storedSource"].update(size=1),
            "role": lambda value: value["storedSource"].update(role="authority"),
            "copy": lambda value: value["storedSource"].update(
                officialCopyStatus="approved"),
            "method": lambda value: value.update(extractionMethod="automatic-ocr"),
            "derivative": lambda value: value["convenienceDerivatives"].append({
                "nonAuthoritative": False, "path": "content/evidence.pdf",
                "rawDigest": value["storedSource"]["rawDigest"],
                "role": "transcription-authority", "size": value["storedSource"]["size"],
            }),
        }
        for label, change in changes.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as root:
                registry = write_fixture(root, manifest_change=change)
                with self.assertRaises(StructuredSourceError):
                    VerificationContext(root, registry=registry).check("pdf-doc")
        with tempfile.TemporaryDirectory() as root:
            registry = write_fixture(root)
            pdf = Path(root) / "content/evidence.pdf"
            not_pdf = b"registered bytes with a PDF extension\n"
            pdf.write_bytes(not_pdf)
            manifest = fixture_manifest(not_pdf)
            (Path(root) / "content/source-manifest.json").write_bytes(
                canonical_json(manifest))
            with self.assertRaisesRegex(StructuredSourceError, "binding"):
                VerificationContext(root, registry=registry).check("pdf-doc")

    def test_machine_result_makes_no_false_fidelity_or_approval_claim(self):
        with tempfile.TemporaryDirectory() as root:
            registry = write_fixture(root)
            result = VerificationContext(root, registry=registry).check("pdf-doc")
        folded = json.dumps(result, sort_keys=True).casefold()
        for claim in ("authentic", "fidelity", "legal", "approval", "filing-ready"):
            self.assertNotIn(claim, folded)

    def test_missing_stale_added_dropped_and_reordered_views_fail(self):
        changes = {
            "missing": None,
            "stale": lambda data: data.replace(b"Alpha", b"Changed", 1),
            "added": lambda data: data + b'<a id="ssp-added"></a>\n',
            "dropped": lambda data: data.replace(
                b'<a id="ssp-frag-heading"></a>', b"", 1),
            "reordered": lambda data: b"\n".join(reversed(data.split(b"\n"))),
        }
        for label, change in changes.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as root:
                registry = write_fixture(root)
                path = Path(root) / "content/evidence.md"
                if change is None:
                    path.unlink()
                else:
                    path.write_bytes(change(path.read_bytes()))
                with self.assertRaises(StructuredSourceError):
                    VerificationContext(root, registry=registry).check("pdf-doc")

    def test_fresh_cross_process_rendering_is_byte_identical(self):
        with tempfile.TemporaryDirectory() as root:
            write_fixture(root)
            xml_path = Path(root) / "content/evidence.xml"
            expected = (Path(root) / "content/evidence.md").read_bytes()
            script = (
                "import pathlib,sys\n"
                "from structured_source.parser import parse_artifact\n"
                "from structured_source.render import render_content\n"
                "a=parse_artifact(pathlib.Path(sys.argv[1]).read_bytes(),'content-document')\n"
                "sys.stdout.buffer.write(render_content(a,'content/evidence.md',{}).markdown)\n"
            )
            completed = subprocess.run(
                [sys.executable, "-B", "-c", script, os.fspath(xml_path)],
                cwd=ROOT, capture_output=True, check=False, timeout=60)
        self.assertEqual(completed.returncode, 0, completed.stderr.decode())
        self.assertEqual(completed.stdout, expected)

    def test_renderer_coverage_self_report_cannot_attest_to_its_region(self):
        with tempfile.TemporaryDirectory() as root:
            registry = write_fixture(root)
            artifact = parser.parse_artifact(fixture_xml(), "content-document")
            projection = render_content(artifact, "content/evidence.md", {})
            coverage = copy.deepcopy(projection.coverage)
            field = next(item for item in coverage["fields"]
                         if item["regions"] and
                         item["classification"] == "review-visible")
            region = field["regions"][0]
            self.assertGreater(region["endLine"], region["startLine"])
            anchor_line = projection.markdown.decode().splitlines().index(
                '<a id="%s"></a>' % field["anchors"][0]) + 1
            self.assertLessEqual(region["startLine"], anchor_line)
            self.assertGreaterEqual(region["endLine"], anchor_line)
            region["endLine"] = region["startLine"]
            tampered = Projection(
                markdown=projection.markdown,
                markdown_digest=projection.markdown_digest,
                coverage=coverage)
            with mock.patch(
                    "structured_source.verify._render_content",
                    return_value=tampered), self.assertRaisesRegex(
                        StructuredSourceError, "region is stale"):
                VerificationContext(root, registry=registry).check("pdf-doc")

    def test_renderer_cannot_add_an_unowned_stable_anchor(self):
        with tempfile.TemporaryDirectory() as root:
            registry = write_fixture(root)
            artifact = parser.parse_artifact(fixture_xml(), "content-document")
            projection = render_content(artifact, "content/evidence.md", {})
            markdown = projection.markdown.replace(
                b'<a id="ssp-review-metadata"></a>',
                b'<a id="ssp-unowned"></a>\n\n'
                b'<a id="ssp-review-metadata"></a>', 1)
            coverage = copy.deepcopy(projection.coverage)
            coverage["markdownDigest"] = raw_digest(markdown)
            tampered = Projection(
                markdown=markdown, markdown_digest=raw_digest(markdown),
                coverage=coverage)
            with mock.patch(
                    "structured_source.verify._render_content",
                    return_value=tampered), self.assertRaisesRegex(
                        StructuredSourceError, "anchor census"):
                VerificationContext(root, registry=registry).check("pdf-doc")

    def test_whitespace_only_leaf_text_remains_in_computed_field_census(self):
        original = parser.parse_artifact(fixture_xml(), "content-document")
        whitespace = parser.parse_artifact(
            fixture_xml().replace(b"One &lt; two", b" "),
            "content-document")
        counts = []
        for artifact in (original, whitespace):
            fields = render_content(
                artifact, "content/evidence.md", {}).coverage["fields"]
            counts.append(sum(
                item["classification"] == "review-visible" and
                item["fieldId"].endswith(":text")
                for item in fields))
        self.assertEqual(counts[0], counts[1])


class PDFSnapshotHandoff(unittest.TestCase):
    def test_validation_precedes_handoff_and_no_representation_fallback_exists(self):
        with tempfile.TemporaryDirectory() as root:
            registry = write_fixture(root)
            with self.assertRaisesRegex(StructuredSourceError, "immutable snapshot"):
                VerificationContext(root, registry=registry).read_for_consumer(
                    "example-consumer", "pdf-doc")
            detached = type(
                "DetachedPassToken", (), {"digest": "sha256:detached"})()
            with self.assertRaisesRegex(StructuredSourceError, "immutable snapshot"):
                VerificationContext(
                    root, registry=registry,
                    byte_source=lambda absolute: Path(absolute).read_bytes(),
                    repository_snapshot=detached).read_for_consumer(
                        "example-consumer", "pdf-doc")
        with tempfile.TemporaryDirectory() as root:
            registry = write_fixture(root)
            snapshot = RepositorySnapshot.capture(root, retain_bytes=True)
            with self.assertRaises(TypeError):
                snapshot.retained_bytes["content/evidence.xml"] = b"changed"
            stale_identity = replace(
                snapshot, digest="sha256/c1:" + "0" * 64)
            with self.assertRaisesRegex(
                    StructuredSourceError, "retained-byte identity"):
                VerificationContext(
                    root, registry=registry,
                    byte_source=stale_identity.byte_source(),
                    repository_snapshot=stale_identity).read_for_consumer(
                        "example-consumer", "pdf-doc")
        with tempfile.TemporaryDirectory() as root:
            registry = write_fixture(
                root, markdown_change=lambda data: data + b"stale\n")
            context = snapshot_context(root, registry)
            with self.assertRaisesRegex(StructuredSourceError, "stale"):
                context.read_for_consumer("example-consumer", "pdf-doc")
            Path(root, "content/evidence.xml").unlink()
            with self.assertRaises(StructuredSourceError):
                snapshot_context(root, registry).read_for_consumer(
                    "example-consumer", "pdf-doc")

    def test_handoff_uses_validated_snapshot_bytes_without_reopen(self):
        with tempfile.TemporaryDirectory() as root:
            registry = write_fixture(root)
            calls = {}

            def byte_source(absolute):
                relative = os.path.relpath(absolute, root).replace(os.sep, "/")
                calls[relative] = calls.get(relative, 0) + 1
                return Path(absolute).read_bytes()

            context = snapshot_context(root, registry, byte_source)
            context.check("pdf-doc")
            before = dict(calls)
            Path(root, "content/evidence.xml").write_bytes(b"changed outside snapshot")
            handoff = context.read_for_consumer("example-consumer", "pdf-doc")
        self.assertEqual(calls, before)
        self.assertEqual(handoff["bytes"], fixture_xml())
        self.assertEqual(handoff["path"], "content/evidence.xml")
        self.assertEqual(set(dict(handoff["validationReads"])), {
            "content/evidence.md", "content/evidence.pdf",
            "content/evidence.xml", "content/source-manifest.json",
            *parser.PARSER_CONTROL_PATHS,
        })

    def test_prevalidated_declared_dependency_is_not_reopened_for_handoff(self):
        with tempfile.TemporaryDirectory() as root:
            registry = write_fixture(root)
            dependency_path = Path(root) / "content/consumer.json"
            dependency_path.write_bytes(b"declared dependency\n")
            authored_edge, pdf_edge, unused_relation_edge = \
                registry["consumers"][0]["edges"]
            authored_edge["dependencies"] = []
            pdf_edge["dependencies"] = ["file-dependency"]
            calls = {}

            snapshot = RepositorySnapshot.capture(root, retain_bytes=True)

            def byte_source(absolute):
                relative = os.path.relpath(absolute, root).replace(os.sep, "/")
                calls[relative] = calls.get(relative, 0) + 1
                return snapshot.read_bytes(relative)

            context = VerificationContext(
                root, registry=registry, byte_source=byte_source,
                repository_snapshot=snapshot)
            context.reader.read("content/consumer.json")
            before = dict(calls)
            handoff = context.read_for_consumer("example-consumer", "pdf-doc")
        self.assertEqual(calls["content/consumer.json"],
                         before["content/consumer.json"])
        self.assertEqual(handoff["dependencies"], {
            "content/consumer.json": b"declared dependency\n"})

    def test_handoff_rejects_valid_live_bytes_that_differ_from_the_snapshot(self):
        with tempfile.TemporaryDirectory() as root:
            registry = write_fixture(root)
            context = snapshot_context(
                root, registry,
                byte_source=lambda absolute: Path(absolute).read_bytes())
            changed_pdf = PDF_BYTES + b"% later live mutation\n"
            Path(root, "content/evidence.pdf").write_bytes(changed_pdf)
            Path(root, "content/source-manifest.json").write_bytes(
                canonical_json(fixture_manifest(changed_pdf)))
            with self.assertRaisesRegex(
                    StructuredSourceError, "differs from the snapshot"):
                context.read_for_consumer("example-consumer", "pdf-doc")

    def test_handoff_rejects_validation_controls_outside_retained_snapshot(self):
        with tempfile.TemporaryDirectory() as root:
            registry = write_fixture(root)
            snapshot = RepositorySnapshot.capture(root, retain_bytes=True)
            schema_path = Path(root) / parser.SCHEMA_PATHS["content-document"]
            schema_path.write_bytes(
                schema_path.read_bytes().replace(
                    b'<xs:complexType name="pdfOrigin"/>',
                    b'<xs:complexType name="pdfOrigin">\n'
                    b'    <xs:sequence />\n  </xs:complexType>'))
            context = VerificationContext(
                root, registry=registry,
                byte_source=lambda absolute: Path(absolute).read_bytes(),
                repository_snapshot=snapshot)
            with self.assertRaisesRegex(
                    StructuredSourceError, "differs from the snapshot"):
                context.read_for_consumer("example-consumer", "pdf-doc")

    def test_markdown_edge_receives_only_the_declared_review_representation(self):
        with tempfile.TemporaryDirectory() as root:
            registry = write_fixture(root)
            edge = next(
                edge for edge in registry["consumers"][0]["edges"]
                if edge["packageId"] == "pdf-doc")
            edge["inputRepresentation"] = "markdown"
            context = snapshot_context(root, registry)
            handoff = context.read_for_consumer("example-consumer", "pdf-doc")
            expected = Path(root, "content/evidence.md").read_bytes()
        self.assertEqual(handoff["bytes"], expected)
        self.assertEqual(handoff["representationRole"], "generated-markdown")
        self.assertIsNone(handoff["surface"])
        self.assertEqual(handoff["assets"], {})

    def test_pdf_package_file_and_ownership_census_is_bidirectional(self):
        registry = registry_fixture()
        registry["files"].append({
            "fileId": "file-unowned-xml", "path": "content/orphan.xml",
            "role": "transcription-xml"})
        registry["files"] = sorted(registry["files"], key=lambda item: item["fileId"])
        with self.assertRaisesRegex(StructuredSourceError, "bidirectionally"):
            validate_registry(registry)
        registry = registry_fixture()
        pdf_file = next(item for item in registry["files"]
                        if item["fileId"] == "file-pdf")
        pdf_file["path"] = "content/evidence.bin"
        with self.assertRaisesRegex(StructuredSourceError, "types/names"):
            validate_registry(registry)

    def test_partial_profile_field_update_fails_closed(self):
        xml_profile = json.loads(
            (ROOT / "structured_source/profiles/xml-v1.json").read_text())
        gfm_profile = json.loads(
            (ROOT / "structured_source/profiles/gfm-v1.json").read_text())
        changed = copy.deepcopy(xml_profile)
        changed["contentDocuments"]["pdf-evidence-transcription-v1"][
            "itemMetadataFields"]["paragraph"] = ["extension"]

        def read_profile(name):
            return changed if name == "xml-v1.json" else gfm_profile

        profiles.load_xml_profiles.cache_clear()
        try:
            with mock.patch.object(profiles, "_read", side_effect=read_profile), \
                    self.assertRaisesRegex(StructuredSourceError, "malformed"):
                profiles.load_xml_profiles()
        finally:
            profiles.load_xml_profiles.cache_clear()


if __name__ == "__main__":
    unittest.main()
