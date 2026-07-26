"""Authored-Markdown authority, addressing, and round-trip tests."""

import json
from pathlib import Path
import re
import unittest
from xml.etree import ElementTree as ET

from structured_source import CONTENT_NAMESPACE, RELATIONS_NAMESPACE, parser
from structured_source.canonical import raw_digest
from structured_source.errors import ParseError, SchemaError, StructuredSourceError
from structured_source.markdown import (
    convert_authored_markdown,
    normalized_pandoc_ast,
    xml_to_markdown,
    xml_to_pandoc_ast,
)
from structured_source.tests.test_xml_contract import RELATIONS
from structured_source.verify import VerificationContext

C = "{%s}" % CONTENT_NAMESPACE
R = "{%s}" % RELATIONS_NAMESPACE
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
ROOT = Path(__file__).resolve().parents[2]
ANCHOR_PAIR = re.compile(br'<a id="(ssp-[a-z][a-z0-9-]*)"></a>')

SIMPLE = b'''<a id="ssp-example-document-root"></a>
<a id="ssp-title"></a>
# Exact title

<a id="ssp-body"></a>
Body with **strong**, *emphasis*, `code`, and [a link](https://example.test/a "title").

<a id="ssp-list"></a>

3. third
4. fourth
'''

COMPLEX = b'''<a id="ssp-complex-document-root"></a>
<a id="ssp-table"></a>

| Left | Right |
|:-----|------:|
| <a id="ssp-table-cell"></a> one | two |

<a id="ssp-quote"></a>

> <a id="ssp-quote-list"></a>
> - <a id="ssp-quote-item"></a><a id="ssp-quote-text"></a> nested item

<a id="ssp-note"></a>
Text with a note.[^1]

[^1]: Exact note text.
'''

CLAIMS = b'''<a id="ssp-claims-document-root"></a>
<a id="ssp-claims-heading"></a>
# Claims

<a id="ssp-claim-1"></a>
**1.** A method comprising a first operation.

<a id="ssp-claim-1-limitation-1"></a>
Performing a second operation.

<a id="ssp-claim-1-limitation-2"></a>
Returning an exact result.

<a id="ssp-claim-2"></a>
**2.** The method of claim 1, further comprising storage.
'''


def _serialize(root: ET.Element) -> bytes:
    ET.register_namespace("", CONTENT_NAMESPACE)
    ET.indent(root, space="  ")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n' +
            ET.tostring(root, encoding="unicode") + "\n").encode("utf-8")


class AuthoredMarkdownConversion(unittest.TestCase):
    def test_conversion_is_deterministic_and_binds_authority_bytes(self):
        first = convert_authored_markdown(
            SIMPLE, "US/common/example.md", "example-document")
        second = convert_authored_markdown(
            SIMPLE, "US/common/example.md", "example-document")
        self.assertEqual(first, second)
        self.assertEqual(first.item_ids, (
            "example-document-root", "title", "body", "list"))
        self.assertEqual(first.source_raw_digest, raw_digest(SIMPLE))

        artifact = parser.parse_artifact(first.xml, "authored-document")
        self.assertEqual(artifact.profile, "authored-markdown-v1")
        self.assertEqual(artifact.fragment_digests, first.fragment_digests)
        self.assertEqual(set(artifact.fragment_digests), set(first.item_ids))
        binding = artifact.root.find(C + "markdownBinding")
        self.assertEqual(binding.get("path"), "US/common/example.md")
        self.assertEqual(binding.get("rawDigest"), raw_digest(SIMPLE))
        self.assertEqual(binding.get("size"), str(len(SIMPLE)))

    def test_document_root_is_exact_and_digest_excludes_the_envelope(self):
        first = convert_authored_markdown(
            SIMPLE, "US/common/example.md", "example-document")
        moved = convert_authored_markdown(
            SIMPLE, "US/common/moved.md", "example-document")
        changed = convert_authored_markdown(
            SIMPLE.replace(b"Exact title", b"Changed title"),
            "US/common/example.md", "example-document")
        artifact = parser.parse_artifact(first.xml, "authored-document")
        root = artifact.typed_item_records["example-document-root"]
        self.assertEqual(root["itemType"], "document")
        self.assertEqual(root["substantiveMetadata"], {})
        self.assertIsInstance(root["typedContent"], list)
        self.assertEqual(
            first.fragment_digests["example-document-root"],
            moved.fragment_digests["example-document-root"])
        self.assertNotEqual(first.xml, moved.xml)
        self.assertNotEqual(
            first.fragment_digests["example-document-root"],
            changed.fragment_digests["example-document-root"])

    def test_authored_xsd_profile_and_value_grammar_agree_exactly(self):
        controls = {
            path: (ROOT / path).read_bytes()
            for path in parser.PARSER_CONTROL_PATHS}
        authored_path = parser.SCHEMA_PATHS["authored-document"]
        profile_path = parser.PROJECTION_PROFILE_PATH
        mutations = (
            (authored_path,
             b'<xs:enumeration value="AlignCenter"/>',
             b'<xs:enumeration value="AUnsupported"/>\n'
             b'      <xs:enumeration value="AlignCenter"/>',
             "constructor inventories differ"),
            (authored_path,
             b'<xs:element name="number" type="xs:decimal"/>',
             b'<xs:element name="number" type="xs:string"/>',
             "value grammar differs"),
            (authored_path,
             b'<xs:enumeration value="block"/>',
             b'<xs:enumeration value="alternate"/>\n'
             b'      <xs:enumeration value="block"/>',
             "identity or fragment grammar differs"),
            (profile_path,
             b'"supportedBlockConstructors": ["BlockQuote"',
             b'"supportedBlockConstructors": ["AUnsupported", "BlockQuote"',
             "constructor inventories differ"),
        )
        for path, current, replacement, message in mutations:
            with self.subTest(path=path, message=message):
                changed = dict(controls)
                changed[path] = changed[path].replace(
                    current, replacement, 1)
                self.assertNotEqual(changed[path], controls[path])
                with self.assertRaisesRegex(SchemaError, message):
                    parser.load_parser_controls(changed.__getitem__)

    def test_xml_preserves_full_ast_and_back_rendered_semantics(self):
        conversion = convert_authored_markdown(
            COMPLEX, "US/common/complex.md", "complex-document")
        ast = xml_to_pandoc_ast(conversion.xml)
        raw_nodes = []

        def walk(value):
            if isinstance(value, dict):
                if value.get("t") == "RawInline":
                    raw_nodes.append(value)
                if "c" in value:
                    walk(value["c"])
            elif isinstance(value, list):
                for item in value:
                    walk(item)

        walk(ast["blocks"])
        self.assertEqual(len(raw_nodes), 2 * len(conversion.item_ids))
        generated = xml_to_markdown(conversion.xml)
        self.assertEqual(
            normalized_pandoc_ast(generated, "complex-document"),
            normalized_pandoc_ast(COMPLEX, "complex-document"))
        self.assertEqual(
            set(conversion.item_ids),
            {"complex-document-root", "table", "table-cell", "quote",
             "quote-list", "quote-item", "quote-text", "note"})

    def test_root_pair_uniqueness_and_exact_raw_html_fail_closed(self):
        without_root = b'<a id="ssp-title"></a>\n# A title\n'
        with self.assertRaisesRegex(StructuredSourceError, "exact document root"):
            convert_authored_markdown(
                without_root, "US/common/no-root.md", "no-root-document")

        duplicate = SIMPLE.replace(b"ssp-list", b"ssp-body")
        with self.assertRaisesRegex(StructuredSourceError, "duplicate stable anchor"):
            convert_authored_markdown(
                duplicate, "US/common/duplicate.md", "example-document")

        unpaired = SIMPLE.replace(
            b'<a id="ssp-list"></a>', b'<a id="ssp-list">')
        with self.assertRaises(StructuredSourceError):
            convert_authored_markdown(
                unpaired, "US/common/unpaired.md", "example-document")

        for raw in (
                b'<span>opaque</span>', b'<div>opaque</div>',
                b'<a class="wrong" id="ssp-extra"></a>'):
            payload = SIMPLE.replace(b"Body with", raw + b"\n\nBody with")
            with self.subTest(raw=raw):
                with self.assertRaises(StructuredSourceError):
                    convert_authored_markdown(
                        payload, "US/common/raw.md", "example-document")

    def test_claim_fragment_binds_all_consecutive_claim_limitations(self):
        first = convert_authored_markdown(
            CLAIMS, "US/common/claims.md", "claims-document")
        changed_source = CLAIMS.replace(
            b"Returning an exact result.", b"Returning a changed result.")
        changed = convert_authored_markdown(
            changed_source, "US/common/claims.md", "claims-document")

        def fragment(conversion, identifier):
            root = ET.fromstring(conversion.xml)
            return next(node for node in root.find(C + "fragments")
                        if node.get(XML_ID) == identifier)

        claim = fragment(first, "claim-1")
        changed_claim = fragment(changed, "claim-1")
        self.assertEqual(claim.get("bindingKind"), "claim")
        self.assertEqual(claim.get("semanticPath"), "claim:claim-1")
        self.assertNotEqual(
            claim.get("bindingDigest"), changed_claim.get("bindingDigest"))
        self.assertIn("Returning an exact result", claim.find(C + "excerpt").text)
        self.assertEqual(fragment(first, "claim-2").get("bindingKind"), "claim")

    def test_source_path_and_link_contracts_fail_closed(self):
        invalid_sources = (
            SIMPLE.rstrip(b"\n"),
            SIMPLE.replace(b"Exact", "E\u0301xact".encode("utf-8")),
            SIMPLE.replace(b"\n", b"\r\n", 1),
        )
        for payload in invalid_sources:
            with self.subTest(payload=payload[:50]):
                with self.assertRaises(StructuredSourceError):
                    convert_authored_markdown(
                        payload, "US/common/rejected.md", "example-document")
        for path in ("/absolute.md", "../escape.md", "US//empty.md", "US\\bad.md"):
            with self.subTest(path=path):
                with self.assertRaisesRegex(StructuredSourceError, "path"):
                    convert_authored_markdown(SIMPLE, path, "example-document")
        with self.assertRaisesRegex(StructuredSourceError, "document ID"):
            convert_authored_markdown(
                SIMPLE, "US/common/example.md", "Derived_ID")
        unsafe = SIMPLE.replace(
            b"Body with", b"[unsafe](javascript:alert(1))\n\nBody with")
        with self.assertRaisesRegex(StructuredSourceError, "scheme"):
            convert_authored_markdown(
                unsafe, "US/common/example.md", "example-document")

    def test_authored_schema_and_recomputed_fragment_index_are_closed(self):
        xml = convert_authored_markdown(
            SIMPLE, "US/common/example.md", "example-document").xml
        with self.assertRaises((ParseError, SchemaError)):
            parser.parse_artifact(
                xml.replace(b"authored-markdown-v1", b"authored-markdown-v0"),
                "authored-document")
        with self.assertRaises((ParseError, SchemaError)):
            parser.parse_artifact(
                xml.replace(b'constructor="Header"', b'constructor="RawBlock"', 1),
                "authored-document")
        with self.assertRaises(SchemaError):
            parser.parse_artifact(
                xml.replace(raw_digest(SIMPLE).encode("ascii"), b"sha256/raw:bad", 1),
                "authored-document")

        root = ET.fromstring(xml)
        body = next(node for node in root.find(C + "fragments")
                    if node.get(XML_ID) == "body")
        digest = body.get("bindingDigest")
        body.set("bindingDigest", digest[:-1] + ("0" if digest[-1] != "0" else "1"))
        with self.assertRaisesRegex(ParseError, "fragment index"):
            parser.parse_artifact(_serialize(root), "authored-document")

    def test_generated_xml_cannot_become_an_editable_second_owner(self):
        xml = convert_authored_markdown(
            SIMPLE, "US/common/example.md", "example-document").xml
        root = ET.fromstring(xml)
        text = next(node for node in root.findall(".//" + C + "string")
                    if node.text == "Exact")
        text.text = "Changed"
        with self.assertRaisesRegex(ParseError, "fragment index"):
            parser.parse_artifact(_serialize(root), "authored-document")

    def test_all_registered_authored_authorities_convert_and_relations_resolve(self):
        registry = json.loads(
            (ROOT / "structured_source/registry/content.json").read_text())
        files = {item["fileId"]: item["path"] for item in registry["files"]}
        packages = [item for item in registry["packages"]
                    if item["authorityScheme"] == "authored-markdown-v1"]
        self.assertEqual(len(packages), 10)
        expected_counts = {
            "aa11393us-af-cont-us-claim-set": 170,
            "aa11393us-af-us-claim-set": 326,
            "aa11393us-af-us-counsel-briefing": 285,
            "aa11393us-continuation-preservation": 154,
            "aa11393us-deferred-filing-disclosure-and-ep-work": 401,
            "aa11393us-na-us-claim-set": 226,
            "aa11393us-na-us-counsel-briefing": 207,
            "aa11393us-pct-informal-comments-ib": 63,
            "aa11393us-us-ids-reference-list": 450,
            "pct-evidence-index": 19,
        }
        inventories = {}
        for package in packages:
            path = files[package["markdownFile"]]
            source = (ROOT / path).read_bytes()
            conversion = convert_authored_markdown(
                source, path, package["packageId"])
            anchors = tuple(match.group(1)[4:].decode("ascii")
                            for match in ANCHOR_PAIR.finditer(source))
            self.assertEqual(conversion.item_ids, anchors)
            self.assertEqual(len(anchors), expected_counts[package["packageId"]])
            inventories[package["packageId"]] = set(conversion.item_ids)
        self.assertEqual(sum(map(len, inventories.values())), 2301)

        referenced = set()
        for package in registry["packages"]:
            if package["authorityScheme"] != "authored-relations-v1":
                continue
            relation_root = ET.fromstring((ROOT / files[package["xmlFile"]]).read_bytes())
            for endpoint in relation_root.findall(".//" + R + "endpoint"):
                document_id = endpoint.get("documentId")
                if document_id in inventories:
                    fragment_id = endpoint.get("fragmentId")
                    self.assertNotIn("ssp-", fragment_id)
                    self.assertIn(fragment_id, inventories[document_id])
                    referenced.add((document_id, fragment_id))
        self.assertEqual(len(referenced), 71)

    def test_current_pdf_content_and_relation_parsers_are_closed(self):
        self.assertEqual(
            parser._schema("content-document").target_namespace,
            "urn:aa11393:ssp:content:1")
        self.assertEqual(
            parser.parse_artifact(RELATIONS, "relation-set").kind,
            "relation-set")


class AuthoredRelations(unittest.TestCase):
    def test_endpoint_package_validation_reads_are_transitively_closed(self):
        package_id = "aa11393us-na-priority-support-map"
        context = VerificationContext(ROOT)
        context.check(package_id)
        artifact = context._artifact(package_id)
        endpoint_package_ids = {
            endpoint.get("documentId")
            for endpoint in artifact.root.findall(".//" + R + "endpoint")}
        state = context._validated_package_state[package_id]
        endpoint_paths = set().union(*(
            set(context._validated_package_state[endpoint_id]["validationPaths"])
            for endpoint_id in endpoint_package_ids))
        self.assertIsNone(state["surface"])
        self.assertEqual(
            set(state["validationPackageIds"]), endpoint_package_ids)
        self.assertTrue(endpoint_paths.issubset(state["validationPaths"]))

    def test_live_registry_declares_no_relation_consumer_edge(self):
        registry = json.loads(
            (ROOT / "structured_source/registry/content.json").read_text())
        relation_packages = {
            package["packageId"] for package in registry["packages"]
            if package["authorityScheme"] == "authored-relations-v1"}
        relation_edges = [
            (consumer["consumerId"], edge["packageId"])
            for consumer in registry["consumers"]
            for edge in consumer["edges"]
            if edge["packageId"] in relation_packages]
        self.assertEqual(relation_edges, [])


if __name__ == "__main__":
    unittest.main()
