"""Focused authority, file-role, and consumer-edge registry fixtures."""

import copy
import os
import tempfile
import unittest
from unittest import mock

from structured_source.control import canonical_json
from structured_source.errors import StructuredSourceError
from structured_source.registry import (AUTHORITY_SCHEMES, consumer_edge,
                                         load_registry, validate_registry)
from structured_source.verify import VerificationContext


def registry_fixture():
    files = [
        {"fileId": "file-authored-md", "path": "content/authored.md",
         "role": "authored-markdown"},
        {"fileId": "file-authored-xml", "path": "content/authored.xml",
         "role": "generated-xml"},
        {"fileId": "file-dependency", "path": "content/consumer.json",
         "role": "consumer-dependency"},
        {"fileId": "file-pdf", "path": "content/evidence.pdf",
         "role": "stored-evidence"},
        {"fileId": "file-pdf-manifest", "path": "content/evidence.manifest.json",
         "role": "source-manifest"},
        {"fileId": "file-pdf-md", "path": "content/evidence.md",
         "role": "generated-markdown"},
        {"fileId": "file-pdf-xml", "path": "content/evidence.xml",
         "role": "transcription-xml"},
        {"fileId": "file-relation-md", "path": "content/relations.md",
         "role": "generated-markdown"},
        {"fileId": "file-relation-xml", "path": "content/relations.xml",
         "role": "relation-xml"},
        {"fileId": "file-router", "path": "router/README.md",
         "role": "router"},
    ]
    packages = [
        {
            "packageId": "authored-doc",
            "authorityScheme": "authored-markdown-v1",
            "xmlFile": "file-authored-xml",
            "markdownFile": "file-authored-md",
            "scope": "shared", "status": "draft", "owner": "Applicant",
            "sourceManifestFile": None, "storedSourceFiles": [],
            "convenienceFiles": [], "assetFiles": [],
        },
        {
            "packageId": "pdf-doc",
            "authorityScheme": "pdf-evidence-transcription-v1",
            "xmlFile": "file-pdf-xml", "markdownFile": "file-pdf-md",
            "scope": "prior-art", "status": "evidence-record",
            "owner": "Applicant",
            "sourceManifestFile": "file-pdf-manifest",
            "storedSourceFiles": ["file-pdf"], "convenienceFiles": [],
            "assetFiles": [],
        },
        {
            "packageId": "relation-set",
            "authorityScheme": "authored-relations-v1",
            "xmlFile": "file-relation-xml",
            "markdownFile": "file-relation-md",
            "scope": "shared", "status": "draft", "owner": "Applicant",
            "sourceManifestFile": None, "storedSourceFiles": [],
            "convenienceFiles": [], "assetFiles": [],
        },
    ]
    return {
        "registryVersion": "1",
        "files": files,
        "packages": packages,
        "routers": [{
            "routerId": "content-router", "path": "router/README.md",
            "scope": "shared",
            "packages": ["authored-doc", "pdf-doc", "relation-set"],
        }],
        "consumers": [{
            "consumerId": "example-consumer",
            "edges": [
                {"packageId": "authored-doc", "inputRepresentation": "xml",
                 "dependencies": ["file-dependency"]},
                {"packageId": "pdf-doc", "inputRepresentation": "xml",
                 "dependencies": []},
                {"packageId": "relation-set", "inputRepresentation": "xml",
                 "dependencies": []},
            ],
        }],
        "taxonomy": {
            "controlledRoots": ["content", "router"],
            "forbiddenPaths": ["retired"],
        },
    }


class RegistryContract(unittest.TestCase):
    def test_three_authority_schemes_and_roles_close(self):
        value = validate_registry(registry_fixture())
        self.assertEqual(
            {entry["authorityScheme"] for entry in value["packages"]},
            set(AUTHORITY_SCHEMES))
        self.assertEqual(
            consumer_edge(value, "example-consumer", "authored-doc")
            ["inputRepresentation"], "xml")

    def test_retired_coverage_and_digest_fields_fail(self):
        for field in ("coverageFile", "sourceDigest"):
            with self.subTest(field=field):
                value = registry_fixture()
                value["packages"][0][field] = "retired"
                with self.assertRaisesRegex(StructuredSourceError, "retired field"):
                    validate_registry(value)

    def test_scheme_role_mismatch_fails(self):
        value = registry_fixture()
        value["packages"][0]["authorityScheme"] = \
            "pdf-evidence-transcription-v1"
        with self.assertRaises(StructuredSourceError):
            validate_registry(value)

    def test_consumer_dependency_cannot_bypass_representation(self):
        value = registry_fixture()
        value["consumers"][0]["edges"][0]["dependencies"] = [
            "file-authored-md"]
        with self.assertRaisesRegex(StructuredSourceError, "bypasses"):
            validate_registry(value)
        value = registry_fixture()
        value["consumers"][0]["edges"][0]["dependencies"] = [
            "file-pdf-xml"]
        with self.assertRaisesRegex(StructuredSourceError, "bypasses"):
            validate_registry(value)

    def test_unknown_representation_fails_but_review_only_package_is_valid(self):
        value = registry_fixture()
        value["consumers"][0]["edges"][0]["inputRepresentation"] = "auto"
        with self.assertRaisesRegex(StructuredSourceError, "representation"):
            validate_registry(value)
        value = registry_fixture()
        value["consumers"][0]["edges"].pop()
        validate_registry(value)
        with self.assertRaisesRegex(StructuredSourceError, "resolve exactly"):
            consumer_edge(value, "example-consumer", "relation-set")

    def test_loader_requires_canonical_current_bytes(self):
        value = registry_fixture()
        with tempfile.TemporaryDirectory() as root:
            directory = os.path.join(root, "structured_source", "registry")
            os.makedirs(directory)
            with open(os.path.join(directory, "content.json"), "wb") as handle:
                handle.write(canonical_json(value))
            self.assertEqual(load_registry(root), value)

    def test_duplicate_package_owned_file_fails(self):
        value = registry_fixture()
        value["packages"][2]["markdownFile"] = "file-pdf-md"
        with self.assertRaises(StructuredSourceError):
            validate_registry(value)

    def test_non_pdf_assets_and_incomplete_router_fail(self):
        value = registry_fixture()
        value["files"].insert(0, {
            "fileId": "file-asset", "path": "content/asset.png",
            "role": "asset",
        })
        value["packages"][0]["assetFiles"] = ["file-asset"]
        with self.assertRaisesRegex(StructuredSourceError, "authority scheme"):
            validate_registry(value)
        value = registry_fixture()
        value["routers"][0]["packages"].pop()
        with self.assertRaisesRegex(StructuredSourceError, "exactly once"):
            validate_registry(value)

    def test_artifact_discovery_ignores_broad_root_documentation(self):
        with tempfile.TemporaryDirectory() as root:
            os.makedirs(os.path.join(root, "router"))
            with open(os.path.join(root, "router", "README.md"), "wb") as handle:
                handle.write(b"# Ordinary documentation\n")
            context = VerificationContext(root, registry=registry_fixture())
            discovered = context._package_artifact_paths({
                "content/orphan.bin",
                "router/README.md",
                "router/orphan.source.xml",
            })
            self.assertEqual(discovered, {
                "content/orphan.bin", "router/orphan.source.xml"})

    def test_regenerate_guards_every_read_authority_path(self):
        with tempfile.TemporaryDirectory() as root:
            os.makedirs(os.path.join(root, "content"))
            authority = os.path.join(root, "content", "authored.md")
            output = os.path.join(root, "content", "authored.xml")
            with open(authority, "wb") as handle:
                handle.write(b"authority\n")
            with open(output, "wb") as handle:
                handle.write(b"old")
            context = VerificationContext(root, registry=registry_fixture())
            context.reader.read("content/authored.md")
            with mock.patch.object(
                    context, "_derive",
                    return_value=("content/authored.xml", b"new", {})):
                result = context.regenerate("authored-doc")
            self.assertEqual(result["status"], "conformant")
            with open(output, "rb") as handle:
                self.assertEqual(handle.read(), b"new")

    def test_consumer_resolver_reads_only_declared_representation_and_dependencies(self):
        with tempfile.TemporaryDirectory() as root:
            os.makedirs(os.path.join(root, "content"))
            for name, data in (
                    ("authored.xml", b"xml"),
                    ("authored.md", b"markdown"),
                    ("consumer.json", b"dependency")):
                with open(os.path.join(root, "content", name), "wb") as handle:
                    handle.write(data)
            context = VerificationContext(root, registry=registry_fixture())
            resolved = context.read_for_consumer(
                "example-consumer", "authored-doc")
            self.assertEqual(resolved["bytes"], b"xml")
            self.assertEqual(resolved["dependencies"], {
                "content/consumer.json": b"dependency"})
            self.assertEqual(set(context.reader.read_log), {
                "content/authored.xml", "content/consumer.json"})
            with self.assertRaisesRegex(StructuredSourceError, "resolve exactly"):
                context.read_for_consumer("missing", "authored-doc")


if __name__ == "__main__":
    unittest.main()
