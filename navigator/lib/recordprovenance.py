"""Representational typed-command provenance for verification records.

The values in this module identify the command contract that produced a
record.  They are audit metadata, not a signature or a claim that record
contents are cryptographically unforgeable.
"""


ATTESTATION_PRODUCER_COMMAND = "navigator/build.py attest/v1"

ATTESTATION_RECORD_FIELDS = frozenset((
    "type", "edition", "sides", "note", "approvalStatus", "operator",
    "operatorKind", "producerCommand",
))
QA_RECORD_FIELDS = frozenset((
    "releaseProfile", "edition", "candidateDigest", "lockDigest",
    "contentLock", "qaInputLock", "reproductionDiagnostics",
    "attestations", "supportMatrix", "legendApproval",
    "manualEvidenceVersion", "manualChecks", "approvalStatus", "operator",
    "operatorKind",
))
RELEASE_RECORD_FIELDS = frozenset((
    "recordVersion", "releaseProfile", "compatibilityAuthorization",
    "deferredObservations", "artifactLabel", "edition", "sealed",
    "sealedDigest", "lockDigest", "qaRecord", "attestations",
    "declaredReleaseTimestamp", "approvalStatus", "operator",
    "operatorKind", "acceptanceReceipt",
))
BUNDLE_RECORD_FIELDS = frozenset((
    "recordVersion", "releaseProfile", "compatibilityAuthorization",
    "deferredObservations", "artifactLabel", "bundle", "bundleDigest",
    "members", "releaseRecords", "manifestWording", "manifestApproval",
    "bundleConfigDigest", "approvalStatus", "operator", "operatorKind",
    "acceptanceReceipt",
))
CURRENT_RECORD_FIELDS = {
    "attestation": ATTESTATION_RECORD_FIELDS,
    "qa-record": QA_RECORD_FIELDS,
    "release-record": RELEASE_RECORD_FIELDS,
    "bundle-record": BUNDLE_RECORD_FIELDS,
}


def attestation_producer_problems(record):
    """Return defects in an attestation's exact producer-command marker."""
    if not isinstance(record, dict):
        return ["attestation record is not an object"]
    if record.get("producerCommand") != ATTESTATION_PRODUCER_COMMAND:
        return [
            "attestation producerCommand must be exactly %r"
            % ATTESTATION_PRODUCER_COMMAND
        ]
    return []


def current_record_format_problems(kind, record):
    """Reject any verification record outside the sole live format.

    Superseded records may remain only when they use these exact current
    fields and version sentinels. Git, not a compatibility loader in the live
    record store, retains evidence written under retired formats.
    """
    fields = CURRENT_RECORD_FIELDS.get(kind)
    if fields is None:
        return ["unknown verification record kind %r" % kind]
    if not isinstance(record, dict):
        return ["%s record is not an object" % kind]
    problems = []
    if set(record) != fields:
        problems.append("%s record fields are not the current format" % kind)
    if kind == "attestation":
        problems.extend(attestation_producer_problems(record))
    elif kind == "qa-record":
        if record.get("releaseProfile") != "validated-release":
            problems.append("QA record has the wrong release profile")
        if record.get("manualEvidenceVersion") != "3":
            problems.append("QA record has the wrong evidence version")
    elif record.get("recordVersion") != "2":
        problems.append("%s has the wrong recordVersion" % kind)
    return problems
