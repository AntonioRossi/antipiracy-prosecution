"""Secure parsing, XSD 1.1, canonicalization, and environment tests."""

import os
from pathlib import Path
from types import MappingProxyType
import unittest
from unittest import mock

from structured_source import canonical, environment, parser
from structured_source.errors import ParseError, SchemaError, StructuredSourceError


CONTENT = b'''<?xml version="1.0" encoding="UTF-8"?>
<source xmlns="urn:aa11393:ssp:content:1" schemaProfile="pdf-evidence-transcription-v1" schemaVersion="1" xml:id="doc-alpha-root">
  <documentIdentity artifactFamily="counsel-briefing" documentId="doc-alpha" jurisdiction="US" language="en" scope="shared" status="draft">
    <title>Alpha &amp; Beta</title>
  </documentIdentity>
  <origin>
    <pdfDerivative />
  </origin>
  <dependencies />
  <provenance>
    <fragmentEvidence fragmentId="frag-heading" page="1" sourcePath="US/prior-art/A1/source.pdf" />
    <fragmentEvidence fragmentId="frag-paragraph" page="1" sourcePath="US/prior-art/A1/source.pdf" />
  </provenance>
  <content>
    <heading level="1" xml:id="frag-heading">
      <text>Alpha</text>
      <space />
      <strong>
        <text>Beta</text>
      </strong>
    </heading>
    <paragraph xml:id="frag-paragraph">
      <text>One &lt; two</text>
      <lineBreak />
      <code>x &amp; y</code>
    </paragraph>
  </content>
  <projectionPolicy noticeVersion="generated-v1" profile="gfm-v1" />
</source>
'''

RELATIONS = b'''<?xml version="1.0" encoding="UTF-8"?>
<relations xmlns="urn:aa11393:ssp:relations:1" schemaProfile="support-map-v1" schemaVersion="1">
  <identity owner="Applicant" profile="support-map-v1" relationSetId="relations-alpha" scope="NA" status="draft" />
  <relation direction="forward" relationId="relation-one" semanticOwner="Applicant" type="claim-support" xml:id="rel-fragment-one">
    <endpoint documentId="claim-doc" fragmentContentDigest="sha256/typed-item-v1:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" fragmentId="claim-one" role="subject" />
    <endpoint documentId="pct-doc" fragmentContentDigest="sha256/typed-item-v1:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb" fragmentId="support-one" role="evidence" />
    <assertionField name="posture">direct</assertionField>
  </relation>
</relations>
'''

CONSUMER_SCHEMA = b'''<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           xmlns:c="urn:example:consumer:1"
           targetNamespace="urn:example:consumer:1"
           elementFormDefault="qualified"
           version="1.1">
  <xs:element name="catalog">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="item" minOccurs="1" maxOccurs="unbounded">
          <xs:complexType>
            <xs:attribute name="id" type="xs:ID" use="required" />
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
'''

CONSUMER_XML = b'''<?xml version="1.0" encoding="UTF-8"?>
<catalog xmlns="urn:example:consumer:1"><item id="one" /></catalog>
'''


class CanonicalContract(unittest.TestCase):
    def test_content_and_relation_vectors_are_stable(self):
        content = parser.parse_artifact(CONTENT, "content-document")
        relations = parser.parse_artifact(RELATIONS, "relation-set")
        self.assertEqual(
            content.raw_digest,
            "sha256/raw:d066b26bf72ec20a639dd51938f7ba925cbbbcdf3e120fbd7c23e2013cb34cb9")
        self.assertEqual(
            content.fragment_digests,
            {
                "doc-alpha-root": "sha256/typed-item-v1:4addd5f971a904b3a56ca1ad0b930add16b45435f0af1fe8c087f1e12c4a2ecc",
                "frag-heading": "sha256/typed-item-v1:dab46ff5d9987c433930138c730e9003542d930a6c883baedc336f82903a128d",
                "frag-paragraph": "sha256/typed-item-v1:e4b2e8890cea75f97a8f16ed845112455ad79222a31a9722bc83e5ca8f3322db",
            })
        self.assertEqual(relations.fragment_digests, {})
        self.assertEqual(relations.typed_item_records, {})

    def test_non_readable_attribute_order_and_missing_declaration_fail_closed(self):
        changed = CONTENT.replace(
            b'schemaProfile="pdf-evidence-transcription-v1" schemaVersion="1"',
            b'schemaVersion="1" schemaProfile="pdf-evidence-transcription-v1"').replace(
                b'<?xml version="1.0" encoding="UTF-8"?>\n', b'')
        with self.assertRaises(ParseError):
            parser.parse_artifact(changed, "content-document")

    def test_every_readable_storage_spelling_is_exact(self):
        prefixed = CONTENT.replace(
            b'<source xmlns="urn:aa11393:ssp:content:1"',
            b'<c:source xmlns:c="urn:aa11393:ssp:content:1"').replace(
                b'</source>\n', b'</c:source>\n')
        mutations = (
            CONTENT.replace(b"\n", b""),
            CONTENT.replace(b"  <documentIdentity", b"    <documentIdentity", 1),
            CONTENT.replace(b"  <documentIdentity", b"\t<documentIdentity", 1),
            CONTENT.replace(b"<dependencies />", b"<dependencies/>", 1),
            CONTENT.replace(
                b' artifactFamily="counsel-briefing" documentId="doc-alpha"',
                b'\n    artifactFamily="counsel-briefing" documentId="doc-alpha"', 1),
            prefixed,
        )
        for payload in mutations:
            with self.subTest(payload=payload[:100]), self.assertRaises(ParseError):
                parser.parse_artifact(payload, "content-document")

    def test_text_leaf_whitespace_is_typed_content_not_indentation(self):
        first = parser.parse_artifact(CONTENT, "content-document")
        second = parser.parse_artifact(
            CONTENT.replace(b"One &lt; two", b" One &lt; two"),
            "content-document")
        self.assertNotEqual(first.raw_digest, second.raw_digest)
        self.assertNotEqual(first.fragment_digests["frag-paragraph"],
                            second.fragment_digests["frag-paragraph"])
        self.assertEqual(first.fragment_digests["frag-heading"],
                         second.fragment_digests["frag-heading"])

    def test_text_leaf_controls_are_escaped_without_wrapping(self):
        for character, entity in ((b"\t", b"&#x9;"), (b"\n", b"&#xA;")):
            with self.subTest(character=character):
                literal = CONTENT.replace(
                    b"<text>Alpha</text>",
                    b"<text>Alpha" + character + b"Beta</text>")
                with self.assertRaises(StructuredSourceError):
                    parser.parse_artifact(literal, "content-document")
                escaped = CONTENT.replace(
                    b"<text>Alpha</text>",
                    b"<text>Alpha" + entity + b"Beta</text>")
                artifact = parser.parse_artifact(escaped, "content-document")
                self.assertIn(character.decode(),
                              artifact.root.find(".//{*}text").text)
                self.assertEqual(artifact.raw_bytes, escaped)

    def test_parser_controls_are_one_closed_xsd_profile_snapshot(self):
        controls = {
            path: (Path(parser.ROOT) / path).read_bytes()
            for path in parser.PARSER_CONTROL_PATHS}
        calls = []

        def read(path):
            calls.append(path)
            return controls[path]

        loaded = parser.load_parser_controls(read)
        self.assertEqual(calls, list(parser.PARSER_CONTROL_PATHS))
        with self.assertRaises(TypeError):
            loaded.projection_profile["profileId"] = "changed"
        with self.assertRaises(TypeError):
            loaded.xml_profiles["contentDocuments"][
                "pdf-evidence-transcription-v1"]["itemOrder"] = "changed"
        with self.assertRaises(TypeError):
            loaded.xml_profiles["relationSets"]["support-map-v1"][
                "directions"][0] = "changed"
        self.assertTrue(all(
            isinstance(pair, tuple) and len(pair) == 2 and
            all(isinstance(data, bytes) for data in pair)
            for pair in loaded.schemas.values()))
        self.assertFalse(hasattr(loaded, "__dict__"))
        with self.assertRaises(TypeError):
            loaded.schemas["content-document"][0] = b"changed"
        parser.parse_artifact(
            CONTENT, "content-document", controls=loaded)

        changed = dict(controls)
        changed[parser.SCHEMA_PATHS["content-document"]] = changed[
            parser.SCHEMA_PATHS["content-document"]].replace(
                b'<xs:attribute ref="xml:id" use="required"/>',
                b'<xs:attribute ref="xml:id" use="required"/>'
                b'<xs:attribute name="extension" type="xs:string"/>', 1)
        with self.assertRaisesRegex(SchemaError, "metadata differ"):
            parser.load_parser_controls(changed.__getitem__)

        changed = dict(controls)
        changed[parser.SCHEMA_PATHS["content-document"]] = changed[
            parser.SCHEMA_PATHS["content-document"]].replace(
                b'<xs:attribute name="title" type="xs:string"/>',
                b'<xs:attribute name="title" type="xs:string"/>'
                b'<xs:attribute name="extension" type="xs:string"/>', 1)
        with self.assertRaisesRegex(SchemaError, "typed-content fields differ"):
            parser.load_parser_controls(changed.__getitem__)

        changed = dict(controls)
        changed[parser.SCHEMA_PATHS["content-document"]] = changed[
            parser.SCHEMA_PATHS["content-document"]].replace(
                b'<xs:element name="text" type="xs:string"/>',
                b'<xs:element name="text" type="c:inlineContainer"/>', 1)
        with self.assertRaisesRegex(SchemaError, "value models differ"):
            parser.load_parser_controls(changed.__getitem__)

        changed = dict(controls)
        changed[parser.SCHEMA_PATHS["content-document"]] = changed[
            parser.SCHEMA_PATHS["content-document"]].replace(
                b'<xs:attribute name="page" type="xs:positiveInteger" '
                b'use="required"/>',
                b'<xs:attribute name="page" type="xs:string" '
                b'use="required"/>', 1)
        with self.assertRaisesRegex(SchemaError, "provenance fields differ"):
            parser.load_parser_controls(changed.__getitem__)

    def test_relation_xsd_profile_and_value_grammar_agree_exactly(self):
        controls = {
            path: (Path(parser.ROOT) / path).read_bytes()
            for path in parser.PARSER_CONTROL_PATHS}
        relation_path = parser.SCHEMA_PATHS["relation-set"]
        mutations = (
            (
                b'<xs:attribute name="semanticOwner" type="xs:string" '
                b'use="required"/>',
                b'<xs:attribute name="semanticOwner" type="xs:string" '
                b'use="required"/>\n'
                b'    <xs:attribute name="extension" type="xs:string"/>',
                "relation grammar differs",
            ),
            (
                b'<xs:element name="endpoint" type="r:endpoint" '
                b'minOccurs="2" maxOccurs="32"/>',
                b'<xs:element name="endpoint" type="r:endpoint" '
                b'minOccurs="2" maxOccurs="31"/>',
                "relation grammar differs",
            ),
            (
                b'sha256/typed-item-v1:[0-9a-f]{64}',
                b'sha256/typed-item-v1:[0-9A-Fa-f]{64}',
                "scalar grammar differs",
            ),
        )
        for current, replacement, message in mutations:
            with self.subTest(message=message):
                changed = dict(controls)
                changed[relation_path] = changed[relation_path].replace(
                    current, replacement, 1)
                self.assertNotEqual(changed[relation_path], controls[relation_path])
                with self.assertRaisesRegex(SchemaError, message):
                    parser.load_parser_controls(changed.__getitem__)

        changed = dict(controls)
        changed[parser.XML_PROFILE_PATH] = changed[
            parser.XML_PROFILE_PATH].replace(
                b'"directions": ["forward"]',
                b'"directions": ["Forward"]', 1)
        self.assertNotEqual(
            changed[parser.XML_PROFILE_PATH], controls[parser.XML_PROFILE_PATH])
        with self.assertRaisesRegex(
                StructuredSourceError, "profile vocabulary is malformed"):
            parser.load_parser_controls(changed.__getitem__)

    def test_typed_item_record_is_exact_and_excludes_envelope_fields(self):
        first = parser.parse_artifact(CONTENT, "content-document")
        record = first.typed_item_records["frag-heading"]
        self.assertEqual(set(record), {
            "authorityScheme", "digestDomain", "documentId", "itemId",
            "itemType", "schemaProfile", "substantiveMetadata",
            "typedContent",
        })
        self.assertEqual(record["digestDomain"],
                         "aa11393:ssp:typed-item:v1")
        self.assertEqual(record["substantiveMetadata"], {"level": 1})
        envelope_changed = parser.parse_artifact(
            CONTENT.replace(b'status="draft"', b'status="review"').replace(
                b'page="1" sourcePath="US/prior-art/A1/source.pdf"',
                b'page="2" sourcePath="US/prior-art/A2/source.pdf"'),
            "content-document")
        self.assertNotEqual(first.raw_digest, envelope_changed.raw_digest)
        self.assertEqual(first.fragment_digests,
                         envelope_changed.fragment_digests)

    def test_dependency_digest_rules_exclude_whole_xml_substitution(self):
        typed = "sha256/typed-item-v1:" + "a" * 64
        raw = "sha256/raw:" + "b" * 64
        valid = CONTENT.replace(
            b"<dependencies />",
            ('<dependencies>\n    <dependency digest="%s" itemId="item-one" '
             'kind="document" subjectId="doc-one" />\n  </dependencies>' %
             typed).encode())
        parser.parse_artifact(valid, "content-document")
        invalid_entries = (
            '<dependency digest="%s" kind="document" subjectId="doc-one" />' % typed,
            '<dependency itemId="item-one" kind="document" subjectId="doc-one" />',
            '<dependency digest="%s" kind="document" subjectId="doc-one" />' % raw,
            '<dependency digest="%s" kind="relation-set" subjectId="rels-one" />' % typed,
        )
        for entry in invalid_entries:
            payload = CONTENT.replace(
                b"<dependencies />",
                ("<dependencies>\n    %s\n  </dependencies>" % entry).encode())
            with self.subTest(entry=entry), self.assertRaises(SchemaError):
                parser.parse_artifact(payload, "content-document")

    def test_semantic_change_changes_only_the_affected_typed_item_and_raw_bytes(self):
        first = parser.parse_artifact(CONTENT, "content-document")
        changed = parser.parse_artifact(
            CONTENT.replace(b"One &lt; two", b"One &lt; three"),
            "content-document")
        self.assertNotEqual(first.raw_digest, changed.raw_digest)
        self.assertEqual(first.fragment_digests["frag-heading"],
                         changed.fragment_digests["frag-heading"])
        self.assertNotEqual(first.fragment_digests["frag-paragraph"],
                            changed.fragment_digests["frag-paragraph"])

    def test_typed_item_and_raw_byte_digest_domains_are_separate(self):
        artifact = parser.parse_artifact(CONTENT, "content-document")
        self.assertNotEqual(
            artifact.fragment_digests["frag-paragraph"],
            artifact.raw_digest)
        self.assertTrue(artifact.fragment_digests["frag-paragraph"].startswith(
            "sha256/typed-item-v1:"))
        self.assertTrue(artifact.raw_digest.startswith("sha256/raw:"))


class SecureParser(unittest.TestCase):
    def assertRejected(self, payload, error=ParseError):
        with self.assertRaises(error):
            parser.parse_artifact(payload, "content-document")

    def test_external_and_opaque_constructs_fail_closed(self):
        mutations = (
            b'<!DOCTYPE source SYSTEM "https://example.invalid/source.dtd">\n' + CONTENT,
            b'<!DOCTYPE source [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>\n' + CONTENT,
            CONTENT.replace(b"Alpha</text>", b"<![CDATA[Alpha]]></text>"),
            CONTENT.replace(b"  <documentIdentity", b"  <!--hidden-->\n  <documentIdentity"),
            CONTENT.replace(b"  <documentIdentity", b"  <?hidden value?>\n  <documentIdentity"),
            CONTENT.replace(b"<text>Alpha</text>", b"<text>&undeclared;</text>"),
            CONTENT.replace(b"<content>", b'<content xml:base="../escape">'),
            CONTENT.replace(
                b"<content>",
                b'<content xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include href="secret"/>'),
        )
        for payload in mutations:
            with self.subTest(payload=payload[:80]):
                self.assertRejected(payload)

    def test_unknown_elements_attributes_and_profiles_fail_closed(self):
        self.assertRejected(
            CONTENT.replace(b"<dependencies />", b"<dependencies /><unknown />"),
            SchemaError)
        self.assertRejected(
            CONTENT.replace(b'<content>', b'<content unknown="value">'),
            SchemaError)
        self.assertRejected(
            CONTENT.replace(b'schemaVersion="1"', b'schemaVersion="2"'),
            ParseError)
        self.assertRejected(
            CONTENT.replace(b'schemaProfile="pdf-evidence-transcription-v1"',
                            b'schemaProfile="unknown-v1"'),
            ParseError)

    def test_relation_profile_type_role_and_field_are_closed(self):
        mutations = (
            RELATIONS.replace(b'type="claim-support"',
                              b'type="unknown"'),
            RELATIONS.replace(b'role="evidence"', b'role="unknown"'),
            RELATIONS.replace(b'name="posture"', b'name="unknown"'),
        )
        for payload in mutations:
            with self.subTest(payload=payload[-300:]):
                with self.assertRaises(ParseError):
                    parser.parse_artifact(payload, "relation-set")

    def test_duplicate_ids_and_non_nfc_fail_closed(self):
        self.assertRejected(CONTENT.replace(b"frag-paragraph", b"frag-heading"))
        self.assertRejected(CONTENT.replace(b"Alpha", "A\u0301lpha".encode("utf-8")))

    def test_utf8_xml10_and_lf_lexical_contract_fails_closed(self):
        self.assertRejected(b"\xef\xbb\xbf" + CONTENT)
        self.assertRejected(CONTENT.replace(b"\n", b"\r\n"))
        self.assertRejected(CONTENT.replace(
            b'<?xml version="1.0" encoding="UTF-8"?>',
            b'<?xml version="1.1" encoding="UTF-8"?>'))
        self.assertRejected(CONTENT.replace(
            b'<?xml version="1.0" encoding="UTF-8"?>',
            b'<?xml version="1.0" encoding="ISO-8859-1"?>'))

    def test_size_depth_node_attribute_and_text_limits_are_enforced(self):
        base = parser._default_parser_controls()
        cases = {
            "bytes": len(CONTENT) - 1,
            "depth": 2,
            "nodes": 2,
            "attributesPerElement": 1,
            "textNodeCharacters": 2,
        }
        for field, value in cases.items():
            with self.subTest(field=field):
                limits = dict(base.limits)
                limits[field] = value
                controls = parser.ParserControls(
                    limits=MappingProxyType(limits),
                    projection_profile=base.projection_profile,
                    xml_profiles=base.xml_profiles,
                    schemas=base.schemas)
                with self.assertRaises(ParseError):
                    parser.parse_artifact(
                        CONTENT, "content-document", controls=controls)

    def test_consumer_xml_uses_the_same_closed_secure_parser(self):
        root = parser.parse_validated_xml(
            CONSUMER_XML,
            CONSUMER_SCHEMA,
            expected_namespace="urn:example:consumer:1",
            expected_root="catalog",
        )
        self.assertEqual(root.tag, "{urn:example:consumer:1}catalog")

        # The same resource limits cover the schema document itself, not only
        # the instance being validated.  The instance has exactly two nodes;
        # the larger schema must therefore be the tree rejected here.
        with mock.patch.object(parser, "MAX_NODES", 2):
            with self.assertRaises(ParseError):
                parser.parse_validated_xml(
                    CONSUMER_XML,
                    CONSUMER_SCHEMA,
                    expected_namespace="urn:example:consumer:1",
                    expected_root="catalog",
                )

    def test_consumer_xml_rejects_wrong_contract_and_composed_schema(self):
        with self.assertRaises(ParseError):
            parser.parse_validated_xml(
                CONSUMER_XML,
                CONSUMER_SCHEMA,
                expected_namespace="urn:example:consumer:1",
                expected_root="wrong",
            )
        composed = CONSUMER_SCHEMA.replace(
            b'<xs:element name="catalog">',
            b'<xs:include schemaLocation="other.xsd" />\n  <xs:element name="catalog">',
        )
        with self.assertRaises(SchemaError):
            parser.parse_validated_xml(
                CONSUMER_XML,
                composed,
                expected_namespace="urn:example:consumer:1",
                expected_root="catalog",
            )


class LockedEnvironment(unittest.TestCase):
    def test_exact_environment_is_current(self):
        receipt = environment.verify_environment()
        self.assertEqual(receipt["uvVersion"], "0.11.32")
        self.assertEqual(receipt["pythonVersion"], "3.13.12")
        self.assertEqual(
            [(item["name"], item["version"])
             for item in receipt["distributions"]],
            [("elementpath", "5.1.3"), ("xmlschema", "4.3.2")])

    def test_ambient_pythonpath_is_rejected(self):
        with mock.patch.dict(os.environ, {"PYTHONPATH": "/tmp/ambient"}):
            with self.assertRaisesRegex(Exception, "PYTHONPATH"):
                environment.verify_environment()

    def test_snapshot_environment_inputs_are_authoritative(self):
        def byte_source(path):
            relative = os.path.relpath(path, environment.ROOT).replace(os.sep, "/")
            if relative == ".python-version":
                return b"0.0.0\n"
            with open(path, "rb") as handle:
                return handle.read()

        with self.assertRaisesRegex(Exception, "python-version"):
            environment.verify_environment(environment.ROOT, byte_source)


if __name__ == "__main__":
    unittest.main()
