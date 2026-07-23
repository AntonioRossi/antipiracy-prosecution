"""Invariants module — the single home of the closed enums, totality
matrices, bounds, uniqueness keys, and the release predicate (TDD §8.4,
§8.5, §8.1). Consumed by both the validator and the tests; nothing here is
defined a second time elsewhere.
"""

import datetime

try:
    from lib import authority
except ModuleNotFoundError:  # package import outside the standalone navigator
    from navigator.lib import authority

STATUSES = ("mapped", "counsel-review-required")
REVIEW_STATES = ("pending", "internally-reviewed")
REVIEW_OPERATOR_KINDS = ("human", "model", "tool")
AUTHORITATIVE_OPERATOR_KINDS = authority.AUTHORITATIVE_OPERATOR_KINDS
MIGRATION_STATES = ("current", "stale")
MIGRATION_REASONS = (
    "changed", "ambiguous", "fragment-removed", "target-removed",
    "target-changed", "source-changed", "endpoint-changed", "unclassified",
)
ROLES = ("specific", "context", "combination")
CAUTION_TYPES = ("source-gate", "generalization-note")
CAUTION_SCOPES = ("target", "fragment", "claim")
GATE_REQUIREMENTS = ("mandatory", "optional")
DISPOSITIONS = (
    "carried-at-required-scope", "carried-at-fragment-fallback",
    "no-target-recorded",
)

NOTE_MAX = 140
RATIONALE_MAX = 1000


# Semantic identity keys for every relation collection named in §8.5.
# A unit and each nested phrase are distinct reviewed fragment owners; their
# stable owner id is therefore part of every target identity.
def target_block_key(owner_id, target):
    return owner_id, target.get("block")


def target_gate_key(owner_id, target):
    caution = target.get("caution") or {}
    if caution.get("type") != "source-gate":
        return None
    return owner_id, target.get("block"), caution.get("gateId")


def phrase_key(fragment_id, phrase_id):
    return fragment_id, phrase_id


def owner_gate_key(owner_id, gate_id):
    return owner_id, gate_id


def disposition_key(disposition):
    subject = disposition.get("subject") or {}
    return disposition.get("gateId"), subject.get("kind"), subject.get("id")

# Caution type x scope compatibility matrix (§8.5). A claim-scope
# generalization-note is unrepresentable.
CAUTION_MATRIX = {
    ("source-gate", "target"): True,
    ("source-gate", "fragment"): True,
    ("source-gate", "claim"): True,
    ("generalization-note", "target"): True,
    ("generalization-note", "fragment"): True,
    ("generalization-note", "claim"): False,
}

# Field applicability by owner type (§8.4) — declared, not prose.
APPLICABILITY = {
    "unit": ("status", "reviewState", "migrationState", "review"),
    "phrase": ("status", "reviewState", "migrationState", "review"),
    "claim-gate": ("reviewState", "migrationState", "review"),
    "disposition": ("reviewState", "migrationState", "review"),
}


def permitted_dispositions(required_scope, evidence_state):
    """requiredScope x evidence-state -> permitted dispositions (§8.1).

    Total: every reachable configuration has at least one permitted
    disposition, none of which requires creating evidence. The fragment
    fallback is the single declared exception to the scope-match rule and
    exists only at target scope over a no-candidate fragment.
    """
    if required_scope not in ("target", "fragment", "claim"):
        raise ValueError("unknown requiredScope %r" % required_scope)
    if required_scope == "claim":
        return ("carried-at-required-scope",)
    if required_scope == "fragment":
        return ("carried-at-required-scope",)
    # target scope
    if evidence_state == "mapped":
        return ("carried-at-required-scope",)
    if evidence_state == "counsel-review-required":
        return ("carried-at-fragment-fallback", "no-target-recorded")
    raise ValueError("unknown evidence state %r" % evidence_state)


def release_ready(owner_fields, expected_content_hash):
    """The release predicate for one owner (§8.4), defined once: applicable
    lifecycle fields present, an identified authorized operator,
    ``internally-reviewed``, ``current``, and a contentHash equal to the
    recomputed review-projection digest. Deferred cross-edition provenance is
    deliberately fail-closed: its local shape cannot authenticate the source
    side, so any ``proposedFrom`` remains non-releasable until the pair-scoped
    verifier exists. Returns a list of defect strings (empty = ready)."""
    defects = []
    if owner_fields.get("reviewState") != "internally-reviewed":
        defects.append("reviewState is %r" % owner_fields.get("reviewState"))
    if owner_fields.get("migrationState") != "current":
        defects.append("migrationState is %r" % owner_fields.get("migrationState"))
    review = owner_fields.get("review") or {}
    defects.extend(review_metadata_defects(review))
    got = review.get("contentHash")
    if got != expected_content_hash:
        defects.append(
            "review.contentHash %s does not match the review projection (%s)"
            % (got, expected_content_hash))
    if "proposedFrom" in owner_fields:
        defects.append(
            "proposedFrom cannot be release-verified while pair-scoped "
            "propose-reuse verification is deferred")
    return defects


def review_metadata_defects(review):
    """Return defects in identified authorized review evidence for one owner."""
    defects = []
    reviewer = review.get("by") if isinstance(review, dict) else None
    if not authority.is_identified_operator_identity(reviewer):
        defects.append("review.by must be non-empty and identify the operator")
    operator_kind = review.get("operatorKind") \
        if isinstance(review, dict) else None
    if not authority.is_authoritative_operator_kind(operator_kind):
        defects.append(
            "review.operatorKind is %r, not an authorized operator kind"
            % operator_kind)
    review_date = review.get("date") if isinstance(review, dict) else None
    parsed_date = None
    if not isinstance(review_date, str) or not review_date.strip():
        defects.append("review.date must be non-empty")
    else:
        try:
            parsed_date = datetime.date.fromisoformat(review_date)
        except ValueError:
            pass
    if isinstance(review_date, str) and review_date.strip() and \
            (parsed_date is None or parsed_date.isoformat() != review_date):
        defects.append("review.date is not a real canonical YYYY-MM-DD date")
    return defects
