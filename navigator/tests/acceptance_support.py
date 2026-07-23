"""Shared current-format acceptance fixtures for focused unit tests."""

import copy
import os

from lib import acceptance, canon


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OBSERVED = [
    "AC-11.observed", "AC-12.observed", "AC-13.observed", "AC-15.observed",
]
MANUAL_FIELDS = ["ac11", "ac12", "ac13", "ac15"]
TECHNICAL_PREVIEW_PROFILE = {
    "id": "technical-preview",
    "manualQaEvidence": "deferred",
    "compatibilityAuthorization": "not-authorized",
    "deferredControls": list(OBSERVED),
    "requiredObservedControls": [],
    "requiredQaRecordFields": [],
    "artifactLabel": (
        "TECHNICAL PREVIEW — Manual cross-platform and "
        "assistive-technology QA is deferred; browser and "
        "assistive-technology compatibility is not validated."),
}
VALIDATED_RELEASE_PROFILE = {
    "id": "validated-release",
    "manualQaEvidence": "required",
    "compatibilityAuthorization": "support-matrix-authorized",
    "deferredControls": [],
    "requiredObservedControls": list(OBSERVED),
    "requiredQaRecordFields": list(MANUAL_FIELDS),
    "artifactLabel": (
        "VALIDATED-RELEASE PROFILE — Delivery requires current full "
        "seven-row cross-platform and assistive-technology QA."),
}


def context(profile=VALIDATED_RELEASE_PROFILE, editions=("na",)):
    registry = acceptance.load_registry(ROOT)
    runner_inputs = [{
        "path": "navigator/lib/acceptance.py",
        "digest": canon.bytes_digest(b"focused fixture runner input"),
    }]
    result = {
        "registryDigest": canon.bytes_digest(b"focused fixture registry"),
        "policyDigest": canon.bytes_digest(b"focused fixture policy"),
        "runnerInputs": runner_inputs,
        "runnerEditions": sorted(editions),
        "controlPlan": acceptance.control_plan(registry),
        "releaseProfile": profile["id"],
        "releaseProfileContract": copy.deepcopy(profile),
    }
    result["runnerDigest"] = acceptance.runner_digest(
        result["registryDigest"], result["policyDigest"],
        result["runnerInputs"], result["controlPlan"],
        result["runnerEditions"], result["releaseProfile"],
        result["releaseProfileContract"])
    return result


def receipt(kind, subjects, current_context):
    return acceptance.make_receipt(
        kind, current_context, copy.deepcopy(subjects))
