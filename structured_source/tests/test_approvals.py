"""Closed identified-human record and inventory mutation fixtures."""

import copy
import os
import unittest

from structured_source.approvals import (INVENTORY_PATH, STATUS_REGISTER_PATH,
                                         package_binding, validate_authorities,
                                         validate_inventory, validate_record)
from structured_source.control import parse_json
from structured_source.errors import StructuredSourceError
from structured_source.registry import load_registry


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


BINDING = {
    "bindingVersion": "1",
    "sourceRawDigest": "sha256/raw:" + "a" * 64,
    "sourceSemanticDigest": "sha256/xc1/ssp-xd1:" + "b" * 64,
    "registryDigest": "sha256/raw:" + "c" * 64,
    "schemaBindings": ["schema|sha256/raw:" + "d" * 64],
    "controlBindings": ["control|sha256/raw:" + "e" * 64],
    "dependencyBindings": [], "endpointBindings": [], "assetBindings": [],
    "sourceEvidenceBindings": [],
    "markdownDigest": "sha256/raw:" + "f" * 64,
    "coverageDigest": "sha256/raw:" + "1" * 64,
    "reviewedCensusDigest": "sha256/c1:" + "2" * 64,
}


def record(approval_type="projection-completeness"):
    return {
        "recordVersion": "1", "approvalType": approval_type,
        "subjectKind": "document", "subjectId": "doc-alpha",
        "reviewer": {"identity": "Antonio Rossi", "role": "content owner",
                     "authorityKind": "identified-human"},
        "reviewedAt": "2026-07-24T12:00:00Z", "bindings": copy.deepcopy(BINDING),
        "projectionApprovalDigest": (None if approval_type == "projection-completeness"
                                     else "sha256/c1:" + "3" * 64),
        "confirmation": "exact-current-sides-reviewed-and-approved",
    }


class ApprovalRecords(unittest.TestCase):
    def test_current_relation_endpoint_bindings_are_canonical_sets(self):
        registry = load_registry(ROOT)
        for package in registry["relationSets"]:
            with self.subTest(relation_set=package["relationSetId"]):
                endpoints = package_binding(ROOT, registry, package)[
                    "endpointBindings"]
                self.assertTrue(endpoints)
                self.assertEqual(endpoints, sorted(set(endpoints)))

    def test_dynamic_status_register_is_not_a_package_approval_side(self):
        registry = load_registry(ROOT)
        package = registry["documents"][0]
        controls = package_binding(ROOT, registry, package)["controlBindings"]
        self.assertFalse(any(
            item.startswith(STATUS_REGISTER_PATH + "|") for item in controls))
        self.assertTrue(any(
            item["path"] == STATUS_REGISTER_PATH and item["role"] == "contract"
            for item in registry["files"]))

    def test_post_approval_outputs_cannot_self_invalidate_package_bindings(self):
        registry = load_registry(ROOT)
        with open(os.path.join(ROOT, *INVENTORY_PATH.split("/")), "rb") as handle:
            inventory = parse_json(handle.read())
        export_paths = {
            item["exportPath"] for item in registry["consumers"]
            if item["exportPath"] is not None
        }
        mutable_outputs = ({INVENTORY_PATH, STATUS_REGISTER_PATH} | export_paths |
                           {item["path"] for item in inventory["records"]})
        for package in registry["documents"] + registry["relationSets"]:
            package_id = package.get("documentId", package.get("relationSetId"))
            binding = package_binding(ROOT, registry, package)
            bound_paths = {
                item.split("|", 1)[0]
                for field in ("schemaBindings", "controlBindings",
                              "assetBindings", "sourceEvidenceBindings")
                for item in binding[field]
            }
            with self.subTest(package=package_id):
                self.assertFalse(mutable_outputs & bound_paths)

    def test_authority_registry_is_identified_human_and_exact(self):
        value = {"authorityRegistryVersion": "1", "authorities": [{
            "identity": "Antonio Rossi", "role": "content owner",
            "authorityKind": "identified-human",
        }]}
        self.assertEqual(validate_authorities(value), value)
        model = copy.deepcopy(value)
        model["authorities"][0]["authorityKind"] = "model"
        with self.assertRaises(StructuredSourceError):
            validate_authorities(model)
        duplicate = copy.deepcopy(value)
        duplicate["authorities"].append(copy.deepcopy(duplicate["authorities"][0]))
        with self.assertRaises(StructuredSourceError):
            validate_authorities(duplicate)

    def test_projection_and_later_substantive_shapes_are_closed(self):
        self.assertEqual(validate_record(record())["approvalType"],
                         "projection-completeness")
        self.assertEqual(validate_record(record("authored-content-review"))["approvalType"],
                         "authored-content-review")
        fractional = record("authored-content-review")
        fractional["reviewedAt"] = "2026-07-24T12:00:00.100000Z"
        self.assertEqual(validate_record(fractional)["reviewedAt"],
                         "2026-07-24T12:00:00.100000Z")

    def test_model_authority_missing_side_and_self_binding_are_rejected(self):
        model = record()
        model["reviewer"]["authorityKind"] = "model"
        with self.assertRaises(StructuredSourceError):
            validate_record(model)
        missing = record()
        missing["bindings"].pop("coverageDigest")
        with self.assertRaises(StructuredSourceError):
            validate_record(missing)
        self_bound = record()
        self_bound["projectionApprovalDigest"] = "sha256/c1:" + "4" * 64
        with self.assertRaises(StructuredSourceError):
            validate_record(self_bound)

    def test_record_inventory_is_digest_addressed_and_unique(self):
        digest = "sha256/c1:" + "5" * 64
        path = "structured_source/approvals/records/%s.json" % ("5" * 64)
        inventory = {"inventoryVersion": "1", "records": [{
            "digest": digest, "path": path,
            "approvalType": "projection-completeness", "subjectId": "doc-alpha",
        }]}
        self.assertEqual(validate_inventory(inventory), inventory)
        broken = copy.deepcopy(inventory)
        broken["records"][0]["path"] = "structured_source/approvals/records/wrong.json"
        with self.assertRaises(StructuredSourceError):
            validate_inventory(broken)


if __name__ == "__main__":
    unittest.main()
