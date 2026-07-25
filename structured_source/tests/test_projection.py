"""Deterministic GFM projection and coverage tests."""

import json
import subprocess
import unittest

from structured_source import parser, render
from structured_source.tests.test_xml_contract import CONTENT, RELATIONS


class ProjectionContract(unittest.TestCase):
    def setUp(self):
        self.artifact = parser.parse_artifact(CONTENT, "content-document")

    def test_projection_and_coverage_are_deterministic(self):
        first = render.render_content(
            self.artifact, "US/common/example/alpha.md")
        second = render.render_content(
            parser.parse_artifact(CONTENT, "content-document"),
            "US/common/example/alpha.md")
        self.assertEqual(first, second)
        self.assertTrue(first.markdown.endswith(b"\n"))
        self.assertTrue(first.coverage.endswith(b"\n"))
        self.assertIn(b"GENERATED REVIEW PROJECTION", first.markdown)
        self.assertIn(b'<a id="ssp-doc-alpha-root"></a>', first.markdown)
        self.assertIn(b'<a id="ssp-frag-heading"></a>', first.markdown)
        self.assertIn(b"# Alpha **Beta**", first.markdown)
        self.assertIn(b"One \\< two  \n`x & y`", first.markdown)
        self.assertIn(b"## Structured-source review metadata", first.markdown)

    def test_coverage_is_bidirectional_and_complete_for_xml_fields(self):
        projection = render.render_content(
            self.artifact, "US/common/example/alpha.md")
        coverage = json.loads(projection.coverage)
        self.assertEqual(coverage["sourceDigest"],
                         self.artifact.semantic_digest)
        self.assertEqual(coverage["markdownDigest"],
                         projection.markdown_digest)
        self.assertTrue(coverage["fields"])
        self.assertEqual(
            len({field["fieldId"] for field in coverage["fields"]}),
            len(coverage["fields"]))
        classifications = {field["classification"]
                           for field in coverage["fields"]}
        self.assertEqual(
            classifications,
            {"internal-justified", "mechanically-derived",
             "review-scheduled", "review-visible"})
        visible = [field for field in coverage["fields"]
                   if field["classification"] == "review-visible"]
        self.assertTrue(all(field["anchors"] and field["regions"]
                            for field in visible))
        line_count = len(projection.markdown.splitlines())
        self.assertTrue(all(
            region["endLine"] <= line_count
            for field in coverage["fields"]
            for region in field["regions"]))

    def test_hidden_semantic_field_changes_source_and_projection_bindings(self):
        changed = CONTENT.replace(b"Applicant", b"Applicant owner", 1)
        changed_artifact = parser.parse_artifact(changed, "content-document")
        original = render.render_content(
            self.artifact, "US/common/example/alpha.md")
        modified = render.render_content(
            changed_artifact, "US/common/example/alpha.md")
        self.assertNotEqual(original.markdown, modified.markdown)
        self.assertNotEqual(original.coverage, modified.coverage)
        self.assertIn(b"Applicant owner", modified.markdown)

    def test_relation_coverage_regions_end_within_projection(self):
        artifact = parser.parse_artifact(RELATIONS, "relation-set")
        endpoints = {
            ("claim-doc", "claim-one",
             "sha256/xc1/ssp-xd1:" + "a" * 64): "claim excerpt",
            ("pct-doc", "support-one",
             "sha256/xc1/ssp-xd1:" + "b" * 64): "support excerpt",
        }
        projection = render.render_relations(
            artifact, "US/common/example/relations.md", endpoints)
        coverage = json.loads(projection.coverage)
        line_count = len(projection.markdown.splitlines())
        self.assertTrue(all(
            region["endLine"] <= line_count
            for field in coverage["fields"]
            for region in field["regions"]))

    def test_output_path_changes_are_declared_projection_inputs(self):
        # With no links/assets the paths do not affect bytes; a linked source
        # must bind output location because relative targets are recomputed.
        linked = CONTENT.replace(
            b"<text>One &lt; two</text>",
            b'<link target="US/common/target.md"><text>One &lt; two</text></link>')
        artifact = parser.parse_artifact(linked, "content-document")
        first = render.render_content(artifact, "US/common/a/alpha.md")
        second = render.render_content(artifact, "US/common/a/b/alpha.md")
        self.assertNotEqual(first.markdown, second.markdown)

    def test_gfm_boundary_constructs_keep_their_block_and_link_semantics(self):
        blocks = b'''<content>
    <heading xml:id="frag-multiline-heading" level="2"><text>First</text><softBreak/><text>Second</text><lineBreak/><text>Third</text></heading>
    <paragraph xml:id="frag-link"><link target="US/common/target file.md"><text>review@example.com</text></link><space/><link target="http://example.test/path#${variantId}"><text>variant</text></link></paragraph>
    <table xml:id="frag-table"><head><row xml:id="frag-head-row"><cell alignment="default"><plain xml:id="frag-head"><text>Head</text></plain></cell></row></head><body><row xml:id="frag-body-row"><cell alignment="default"><plain xml:id="frag-body"><text>Body</text></plain></cell></row></body></table>
    <list xml:id="frag-outer-list" ordered="true" start="1" delimiter="period"><item xml:id="frag-outer-item"><list xml:id="frag-inner-list" ordered="true" start="3" delimiter="period"><item xml:id="frag-inner-item"><plain xml:id="frag-inner-text"><text>Solve</text></plain></item></list></item></list>
    <separator xml:id="frag-separator"/>
    <paragraph xml:id="frag-mark"><lineBreak/><reviewMark style="red"><text>Red review text</text></reviewMark></paragraph>
  </content>'''
        payload = CONTENT.replace(
            CONTENT.split(b"  <content>", 1)[1].split(b"  </content>", 1)[0]
            .join((b"  <content>", b"  </content>")),
            blocks)
        artifact = parser.parse_artifact(payload, "content-document")
        projection = render.render_content(
            artifact, "US/common/example/boundaries.md")
        parsed = subprocess.run(
            ["pandoc", "--from=gfm", "--to=json"],
            input=projection.markdown, capture_output=True, check=True,
            timeout=30)
        ast = json.loads(parsed.stdout)
        block_types = [block["t"] for block in ast["blocks"]]
        self.assertIn("Table", block_types)
        self.assertIn(
            b'<a id="ssp-frag-head"></a>', projection.markdown)
        self.assertIn(
            b'<a id="ssp-frag-body"></a>', projection.markdown)
        self.assertIn("HorizontalRule", block_types)
        outer = next(block for block in ast["blocks"]
                     if block["t"] == "OrderedList")
        self.assertEqual(outer["c"][1][0][0]["t"], "OrderedList")
        links = [inline for block in ast["blocks"] if block["t"] == "Para"
                 for inline in block["c"] if inline["t"] == "Link"]
        self.assertTrue(links)
        self.assertFalse(any(child["t"] == "Link"
                             for child in links[0]["c"][1]))
        self.assertIn(
            b'<span style="color:red">Red review text</span>',
            projection.markdown)
        self.assertIn(b"## First Second<br>Third", projection.markdown)
        self.assertIn(b"target%20file.md", projection.markdown)
        self.assertIn(b"%24%7BvariantId%7D", projection.markdown)
        self.assertIn(
            b'<br><span style="color:red">Red review text</span>',
            projection.markdown)


if __name__ == "__main__":
    unittest.main()
