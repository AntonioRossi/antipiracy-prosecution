"""Secure parsing, XSD 1.1, canonicalization, and environment tests."""

import os
import unittest
from unittest import mock

from structured_source import canonical, environment, parser
from structured_source.errors import ParseError, SchemaError


CONTENT = b'''<?xml version="1.0" encoding="UTF-8"?>
<source xmlns="urn:aa11393:ssp:content:1" xml:id="doc-alpha-root" schemaProfile="authored-v1" schemaVersion="1">
  <documentIdentity documentId="doc-alpha" artifactFamily="counsel-briefing" jurisdiction="US" scope="shared" status="draft" language="en">
    <title>Alpha &amp; Beta</title>
  </documentIdentity>
  <origin><authoredSource responsibleOwner="Applicant" reviewScope="complete"/></origin>
  <dependencies/>
  <provenance/>
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
  <relation xml:id="rel-fragment-one" relationId="relation-one" type="claim-support" direction="forward" reviewOwner="Applicant">
    <endpoint role="subject" documentId="claim-doc" fragmentId="claim-one" fragmentContentDigest="sha256/xc1/ssp-xd1:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"/>
    <endpoint role="evidence" documentId="pct-doc" fragmentId="support-one" fragmentContentDigest="sha256/xc1/ssp-xd1:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"/>
    <assertionField name="posture">direct</assertionField>
  </relation>
</relations>
'''


class CanonicalContract(unittest.TestCase):
    def test_content_and_relation_vectors_are_stable(self):
        content = parser.parse_artifact(CONTENT, "content-document")
        relations = parser.parse_artifact(RELATIONS, "relation-set")
        self.assertEqual(
            content.raw_digest,
            "sha256/raw:a99ca2a39386af26e67dc515f4f4412c7d8505bae854505ab7d3e440b3acd7fd")
        self.assertEqual(
            content.semantic_digest,
            "sha256/xc1/ssp-xd1:85b4650641d2731047730479669c50323a303c518f436a3af0523bfc90f167c1")
        self.assertEqual(
            content.fragment_digests,
            {
                "doc-alpha-root": "sha256/xc1/ssp-xd1:85c9342a1d9b2eaa3ecfb813265f7525f90ab8a62e62aeeede681a5191d29723",
                "frag-heading": "sha256/xc1/ssp-xd1:88e336121633eb61e68baa3ad0c6ad0c925ab04bf33248434f19ec3ab761f2f3",
                "frag-paragraph": "sha256/xc1/ssp-xd1:f261f41ba291c22d1075fd60a5e0f604da6e66c6775f1fb4ab4e26600146ceb4",
            })
        self.assertEqual(
            relations.semantic_digest,
            "sha256/xc1/ssp-xd1:1244c8fdf49840d47b45ba58029faf07612c3c03b8fb65dc381f15efe5ca7dd0")
        self.assertEqual(
            relations.fragment_digests,
            {"rel-fragment-one": "sha256/xc1/ssp-xd1:29fb4719463ac9ed4381583599a2232f50aee1691d2339857fb8d33561ef7d16"})

    def test_attribute_order_and_xml_declaration_do_not_change_semantics(self):
        first = parser.parse_artifact(CONTENT, "content-document")
        changed = CONTENT.replace(
            b'schemaProfile="authored-v1" schemaVersion="1"',
            b'schemaVersion="1" schemaProfile="authored-v1"').replace(
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
            canonical.semantic_digest(fragment, "content-fragment", "authored-v1"))


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
            CONTENT.replace(b'schemaProfile="authored-v1"',
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
