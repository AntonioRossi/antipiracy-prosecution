"""Closed release-profile policy used by both rendering and verification.

Profile selection is artifact-facing policy.  Executable acceptance mappings
live separately and must not be imported by the renderer.
"""

import copy
import re

from . import canon


class ProfilePolicyError(ValueError):
    pass


PROFILE_FIELDS = frozenset((
    "id", "observedControls", "artifactLabel",
))
_PROFILE_ID = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*\Z")
_OBSERVED_CONTROL_ID = re.compile(
    r"AC-(?:0[1-9]|[1-9][0-9]+)\.observed\Z")


def is_profile_id(value):
    return isinstance(value, str) and _PROFILE_ID.fullmatch(value) is not None


def validate_policy(policy):
    if not isinstance(policy, dict) or set(policy) != {
            "releasePolicyVersion", "activeReleaseProfile", "profiles"} or \
            canon.require_version(policy, "releasePolicyVersion", "1"):
        raise ProfilePolicyError("release profile policy shape/version is invalid")
    profiles = policy.get("profiles")
    if not isinstance(profiles, list) or not profiles:
        raise ProfilePolicyError("release profile policy has no profiles")
    ids = []
    observed_set = None
    for profile in profiles:
        if not isinstance(profile, dict) or set(profile) != PROFILE_FIELDS:
            raise ProfilePolicyError("release profile has the wrong fields")
        profile_id = profile.get("id")
        if not is_profile_id(profile_id):
            raise ProfilePolicyError("release profile has no id")
        ids.append(profile_id)
        states = profile.get("observedControls")
        if not isinstance(states, dict) or not states or \
                list(states) != sorted(states) or \
                any(_OBSERVED_CONTROL_ID.fullmatch(identifier) is None
                    for identifier in states):
            raise ProfilePolicyError(
                "release profile observed-control set is not canonical")
        if observed_set is None:
            observed_set = set(states)
        elif set(states) != observed_set:
            raise ProfilePolicyError(
                "release profiles do not cover one observed-control set")
        if any(state not in ("required", "deferred")
               for state in states.values()):
            raise ProfilePolicyError(
                "release profile observed-control state is invalid")
        label = profile.get("artifactLabel")
        if not isinstance(label, str) or not label or label.strip() != label or \
                canon.normalize_nfc(label) != label or \
                any(ord(character) < 32 or ord(character) == 127
                    for character in label):
            raise ProfilePolicyError("release profile artifact label is empty")
    if ids != sorted(ids) or len(ids) != len(set(ids)):
        raise ProfilePolicyError("release profile ids are not an exact sorted set")
    if policy.get("activeReleaseProfile") not in ids:
        raise ProfilePolicyError("active release profile is not declared")
    return policy


def observed_controls(policy):
    """Return the policy-declared observed-control vocabulary."""
    validate_policy(policy)
    return tuple(policy["profiles"][0]["observedControls"])


def profile_contract(policy, requested_profile=None):
    """Return the exact active contract; explicit selection cannot downgrade."""
    validate_policy(policy)
    active = policy["activeReleaseProfile"]
    if requested_profile is not None and requested_profile != active:
        raise ProfilePolicyError(
            "release profile %r is not the active release profile %r" %
            (requested_profile, active))
    profile = next(item for item in policy["profiles"] if item["id"] == active)
    states = profile["observedControls"]
    deferred = sorted(
        control for control, state in states.items() if state == "deferred")
    required = sorted(
        control for control, state in states.items() if state == "required")
    return active, {
        "id": active,
        "manualQaEvidence": "required" if required else "deferred",
        "compatibilityAuthorization": (
            "support-matrix-authorized" if not deferred
            else "not-authorized"),
        "deferredControls": deferred,
        "requiredObservedControls": required,
        "artifactLabel": profile["artifactLabel"],
    }


def copy_contract(policy, requested_profile=None):
    profile_id, contract = profile_contract(policy, requested_profile)
    return profile_id, copy.deepcopy(contract)


def record_fields(contract):
    """Project an artifact-facing profile contract into stored fields."""
    required = {
        "id", "compatibilityAuthorization", "deferredControls",
        "artifactLabel",
    }
    if not isinstance(contract, dict) or not required.issubset(contract):
        raise ProfilePolicyError("release profile contract is malformed")
    return {
        "releaseProfile": contract["id"],
        "compatibilityAuthorization": contract["compatibilityAuthorization"],
        "deferredControls": copy.deepcopy(contract["deferredControls"]),
        "artifactLabel": contract["artifactLabel"],
    }
