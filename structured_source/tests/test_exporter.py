"""Approved-export envelope and member mutation fixtures."""

from io import BytesIO
import json
import unittest
import zipfile

from structured_source.canonical import raw_digest
from structured_source.control import canonical_json
from structured_source.errors import StructuredSourceError
from structured_source.approvals import STATUS_REGISTER_PATH
from structured_source.exporter import (EXPORT_TIMESTAMP, _registered_export_paths,
                                        validate_export_bytes)


def members(payload_path="packages/doc.source.xml", payload=b"<source/>"):
    manifest = {
        "exportVersion": "1", "consumerId": "structured-handoff",
        "semanticAuthority": "xml-only",
        "markdownRole": "human-review-evidence",
        "registryPath": "structured_source/registry/content.json",
        "approvalInventoryPath": "structured_source/approvals/inventory.json",
        "packages": [{
            "packageId": "doc-alpha",
            "approvalBindings": {
                "projection-completeness": "sha256/c1:" + "a" * 64,
                "authored-content-review": "sha256/c1:" + "b" * 64,
            },
        }],
        "members": [{"path": payload_path, "rawDigest": raw_digest(payload),
                     "size": len(payload)}],
    }
    return {"manifest.json": canonical_json(manifest), payload_path: payload}


def archive(value):
    output = BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9, strict_timestamps=True) as handle:
        for path, data in sorted(value.items()):
            info = zipfile.ZipInfo(path, EXPORT_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.flag_bits = 0x800
            handle.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED,
                            compresslevel=9)
    return output.getvalue()


class ExportEnvelope(unittest.TestCase):
    def test_dynamic_status_register_is_not_an_export_member(self):
        export_path = "structured_source/exports/current.ssp.zip"
        registry = {"files": [
            {"path": "contract.md", "role": "contract"},
            {"path": STATUS_REGISTER_PATH, "role": "contract"},
            {"path": export_path, "role": "approved-export"},
        ]}
        self.assertEqual(
            _registered_export_paths(registry, export_path), {"contract.md"})

    def test_exact_control_envelope_is_accepted(self):
        expected = members()
        manifest = validate_export_bytes(archive(expected), expected)
        self.assertEqual(manifest["semanticAuthority"], "xml-only")

    def test_additional_changed_and_denied_members_fail_closed(self):
        expected = members()
        additional = dict(expected)
        additional["extra.xml"] = b"extra"
        with self.assertRaises(StructuredSourceError):
            validate_export_bytes(archive(additional), expected)
        changed = dict(expected)
        changed["packages/doc.source.xml"] = b"changed"
        with self.assertRaises(StructuredSourceError):
            validate_export_bytes(archive(changed), expected)
        denied = members("packages/source.pdf", b"pdf")
        with self.assertRaises(StructuredSourceError):
            validate_export_bytes(archive(denied), denied)

    def test_manifest_shape_and_inventory_are_closed(self):
        expected = members()
        manifest = json.loads(expected["manifest.json"])
        manifest["compatibility"] = True
        malformed = dict(expected)
        malformed["manifest.json"] = canonical_json(manifest)
        with self.assertRaises(StructuredSourceError):
            validate_export_bytes(archive(malformed), malformed)


if __name__ == "__main__":
    unittest.main()
