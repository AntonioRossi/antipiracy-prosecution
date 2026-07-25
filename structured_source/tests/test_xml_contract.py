"""Secure parsing, XSD 1.1, canonicalization, and environment tests."""

import os
import unittest
from unittest import mock

from structured_source import canonical, environment, parser
from structured_source.errors import ParseError, SchemaError


CONTENT = b'''<?xml version="1.0" encoding="UTF-8"?>
<source xmlns="urn:aa11393:ssp:content:1" xml:id="doc-alpha-root" schemaProfile="pdf-evidence-transcription-v1" schemaVersion="1">
  <documentIdentity documentId="doc-alpha" artifactFamily="counsel-briefing" jurisdiction="US" scope="shared" status="draft" language="en">
    <title>Alpha &amp; Beta</title>
  </documentIdentity>
  <origin><pdfDerivative/></origin>
  <dependencies/>
  <provenance>
    <fragmentEvidence fragmentId="frag-heading" sourcePath="US/prior-art/A1/source.pdf" page="1"/>
    <fragmentEvidence fragmentId="frag-paragraph" sourcePath="US/prior-art/A1/source.pdf" page="1"/>
  </provenance>
  <content>
    <heading xml:id="frag-heading" level="1"><text>Alpha</text><space/><strong><text>Beta</text></strong></heading>
    <paragraph xml:id="frag-paragraph"><text>One &lt; two</text><lineBreak/><code>x &amp; y</code></paragraph>
  </content>
  <projectionPolicy profile="gfm-v1" noticeVersion="generated-v1"/>
</source>
'''

RELATIONS = b'''<?xml version="1.0" encoding="UTF-8"?>
<relations xmlns="urn:aa11393:ssp:relations:1" schemaProfile="support-map-v1" schemaVersion="1">
  <identity relationSetId="relations-alpha" profile="support-map-v1" owner="Applicant" scope="NA" status="draft"/>
  <relation xml:id="rel-fragment-one" relationId="relation-one" type="claim-support" direction="forward" semanticOwner="Applicant">
    <endpoint role="subject" documentId="claim-doc" fragmentId="claim-one" fragmentContentDigest="sha256/xc1/ssp-xd1:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"/>
    <endpoint role="evidence" documentId="pct-doc" fragmentId="support-one" fragmentContentDigest="sha256/xc1/ssp-xd1:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"/>
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
            "sha256/raw:d7252092d874b6ee09c17f4c54aa9d023fc67945a1b25de4225de390b70ff35a")
        self.assertEqual(
            content.semantic_digest,
            "sha256/xc1/ssp-xd1:8df46194ee093f326228ff72ad719d6ce4433d19c90ae3fb87be2b832bb2a57c")
        self.assertEqual(
            content.fragment_digests,
            {
                "doc-alpha-root": "sha256/xc1/ssp-xd1:b513a8540f6b4bd5ea86f250aa741c5714da4065ce14a7580c783a4a72f30c9b",
                "frag-heading": "sha256/xc1/ssp-xd1:07f7f12eb5abb1dad174e5378803cda9dc200cea5dfb7a4aa5c083798673cdce",
                "frag-paragraph": "sha256/xc1/ssp-xd1:0839835cf2fc7428f005cb22a691da15083395819d2a8917c424d29a981ff20b",
            })
        self.assertEqual(
            relations.semantic_digest,
            "sha256/xc1/ssp-xd1:f5cec40556bd937b88e472046568574663c74f9557da45860c2e7c74a4f42de6")
        self.assertEqual(
            relations.fragment_digests,
            {"rel-fragment-one": "sha256/xc1/ssp-xd1:b42d04def07e7d30065ed6f70d28612a0dfe5414e371bcfe3ee3da5502939c6e"})

    def test_attribute_order_and_xml_declaration_do_not_change_semantics(self):
        first = parser.parse_artifact(CONTENT, "content-document")
        changed = CONTENT.replace(
            b'schemaProfile="pdf-evidence-transcription-v1" schemaVersion="1"',
            b'schemaVersion="1" schemaProfile="pdf-evidence-transcription-v1"').replace(
                b'<?xml version="1.0" encoding="UTF-8"?>\n', b'')
        second = parser.parse_artifact(changed, "content-document")
        self.assertNotEqual(first.raw_digest, second.raw_digest)
        self.assertEqual(first.semantic_digest, second.semantic_digest)

    def test_semantic_change_changes_fragment_and_document_digests(self):
        first = parser.parse_artifact(CONTENT, "content-document")
        changed = parser.parse_artifact(
            CONTENT.replace(b"One &lt; two", b"One &lt; three"),
            "content-document")
        self.assertNotEqual(first.semantic_digest, changed.semantic_digest)
        self.assertEqual(first.fragment_digests["frag-heading"],
                         changed.fragment_digests["frag-heading"])
        self.assertNotEqual(first.fragment_digests["frag-paragraph"],
                            changed.fragment_digests["frag-paragraph"])

    def test_domain_separation_changes_digest(self):
        artifact = parser.parse_artifact(CONTENT, "content-document")
        fragment = artifact.root.find(
            ".//{urn:aa11393:ssp:content:1}paragraph")
        self.assertNotEqual(
            artifact.semantic_digest,
            canonical.semantic_digest(
                fragment, "content-fragment", "pdf-evidence-transcription-v1"))


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
            CONTENT.replace(b"<dependencies/>", b"<dependencies/><unknown/>"),
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

    def test_size_depth_node_attribute_and_text_limits_are_enforced(self):
        with mock.patch.object(parser, "MAX_XML_BYTES", len(CONTENT) - 1):
            self.assertRejected(CONTENT)
        with mock.patch.object(parser, "MAX_DEPTH", 2):
            self.assertRejected(CONTENT)
        with mock.patch.object(parser, "MAX_NODES", 2):
            self.assertRejected(CONTENT)
        with mock.patch.object(parser, "MAX_ATTRIBUTES", 1):
            self.assertRejected(CONTENT)
        with mock.patch.object(parser, "MAX_TEXT_LENGTH", 2):
            self.assertRejected(CONTENT)

    def test_consumer_xml_uses_the_same_closed_secure_parser(self):
        root = parser.parse_validated_xml(
            CONSUMER_XML,
            CONSUMER_SCHEMA,
            expected_namespace="urn:example:consumer:1",
            expected_root="catalog",
        )
        self.assertEqual(root.tag, "{urn:example:consumer:1}catalog")

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
