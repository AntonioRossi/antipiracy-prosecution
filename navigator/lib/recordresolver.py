"""Typed separation between record inventory and current authorization.

One closed adapter table discriminates every verification record kind:
format defects invalidate a record, currency defects preserve it as
superseded evidence, authorization defects reject an otherwise current
record, and only clean records resolve as current authorizations.  Each
kind's authorization evidence stays in its owning control module and
reaches the adapter through the explicit context object, so this module
never reads content, record, or artifact bytes itself.
"""

from dataclasses import dataclass

from . import authority, canon, recordprovenance


@dataclass(frozen=True)
class RejectedRecord:
    digest: str
    problems: tuple


@dataclass(frozen=True)
class RecordResolution:
    current_authorizations: tuple
    superseded_evidence: tuple
    invalid_records: tuple
    rejected_authorizations: tuple

    def require_current(self, label):
        if not self.current_authorizations:
            detail = [
                "%s: %s" % (item.digest, "; ".join(item.problems))
                for item in self.invalid_records + self.rejected_authorizations
            ]
            raise ValueError(
                "no current %s authorization%s" %
                (label, ": " + " | ".join(detail) if detail else ""))
        return self.current_authorizations


@dataclass(frozen=True)
class QaRecordContext:
    """Current binding and authorization predicate for QA records."""
    edition_id: str
    candidate_digest: str
    lock_digest: str
    release_profile: str
    authorization_problems: object


@dataclass(frozen=True)
class ReleaseRecordContext:
    """Current binding and authorization predicate for release records.

    ``lock_digest`` and ``declared_release_timestamp`` are ``None`` when the
    caller does not independently bind them: bundle promotion pins only the
    configured edition, sealed artifact name, sealed digest, and profile,
    while bundle planning binds the complete independently derived release
    identity.
    """
    edition_id: str
    sealed: str
    sealed_digest: str
    lock_digest: object
    declared_release_timestamp: object
    release_profile: str
    authorization_problems: object


@dataclass(frozen=True)
class BundleRecordContext:
    """Current chain values and receipt predicate for bundle records."""
    release_profile_fields: object
    release_profile_problem: object
    release_profile: str
    bundle: str
    bundle_digest: str
    members: object
    release_records: object
    manifest_wording: str
    manifest_approval: str
    bundle_config_digest: object
    receipt_problems: object


@dataclass(frozen=True)
class AttestationContext:
    """Required type, current sides, and authorization predicate."""
    required_type: str
    expected_edition: object
    check_scope: object
    expected_sides: object
    side_digests: object
    authorization_problems: object


def _qa_format_problems(envelope, context):
    if not isinstance(envelope, dict) or envelope.get("kind") != "qa-record":
        return ["QA envelope has the wrong kind or shape"]
    return list(recordprovenance.current_record_format_problems(
        "qa-record", envelope.get("record")))


def _qa_currency_problems(envelope, context):
    record = envelope["record"]
    if record.get("edition") != context.edition_id or \
            record.get("candidateDigest") != context.candidate_digest or \
            record.get("lockDigest") != context.lock_digest or \
            record.get("releaseProfile") != context.release_profile:
        return ["QA record is valid same-schema superseded evidence"]
    return []


def _release_format_problems(envelope, context):
    """Check the envelope shape and its digest-addressed self-consistency.

    Release selection has always resolved candidates through the exact
    digest index, so a release envelope whose digest does not derive its
    record is malformed evidence rather than a rejected authorization.
    """
    if not isinstance(envelope, dict) or \
            set(envelope) != {"kind", "digest", "record"} or \
            envelope.get("kind") != "release-record":
        return ["release record envelope has the wrong kind or shape"]
    problems = list(recordprovenance.current_record_format_problems(
        "release-record", envelope.get("record")))
    if problems:
        return problems
    try:
        actual = canon.composite_digest(
            "aa11393:release-record:c1", envelope["record"])
    except (KeyError, TypeError, ValueError) as exc:
        return ["release record is not canonical: %s" % exc]
    if actual != envelope.get("digest"):
        problems.append("release record digest does not match its record")
    return problems


def _release_currency_problems(envelope, context):
    record = envelope["record"]
    bound = (
        ("edition", context.edition_id),
        ("sealed", context.sealed),
        ("sealedDigest", context.sealed_digest),
        ("lockDigest", context.lock_digest),
        ("declaredReleaseTimestamp", context.declared_release_timestamp),
        ("releaseProfile", context.release_profile),
    )
    return [
        "release record %s does not match the current release binding"
        % field
        for field, expected in bound
        if expected is not None and record.get(field) != expected
    ]


def _bundle_format_problems(envelope, context):
    if not isinstance(envelope, dict) or \
            envelope.get("kind") != "bundle-record":
        return ["bundle record envelope has the wrong kind or shape"]
    return list(recordprovenance.current_record_format_problems(
        "bundle-record", envelope.get("record")))


def _bundle_currency_problems(envelope, context):
    record = envelope["record"]
    problems = []
    if context.release_profile_problem is not None:
        problems.append(context.release_profile_problem)
    elif context.release_profile_fields is not None:
        problems.extend(
            "bundle record %s does not match current release profile"
            % field
            for field, expected in context.release_profile_fields.items()
            if record.get(field) != expected)
    if record.get("releaseProfile") != context.release_profile:
        problems.append(
            "bundle record releaseProfile does not match current config")
    checks = (
        ("bundle", context.bundle),
        ("bundleDigest", context.bundle_digest),
        ("members", context.members),
        ("releaseRecords", context.release_records),
        ("manifestWording", context.manifest_wording),
        ("manifestApproval", context.manifest_approval),
    )
    problems.extend(
        "bundle record %s does not match current config" % field
        for field, expected in checks
        if record.get(field) != expected)
    if context.bundle_config_digest is not None and \
            record.get("bundleConfigDigest") != context.bundle_config_digest:
        problems.append("bundle record config digest is stale")
    return problems


def _bundle_authorization_problems(envelope, context):
    record = envelope["record"]
    problems = []
    if not authority.is_identified_operator_identity(record.get("operator")):
        problems.append("bundle record has no identified operator")
    if record.get("approvalStatus") != "passed":
        problems.append("bundle record approvalStatus is not 'passed'")
    if not authority.is_authoritative_operator_kind(
            record.get("operatorKind")):
        problems.append(
            "bundle record operatorKind is not release-authoritative")
    problems.extend(context.receipt_problems(record))
    return problems


def _attestation_format_problems(envelope, context):
    """Check only the readable-evidence shape of an attestation envelope.

    Attestation collections mix types and are filtered per required type, so
    record-level field and producer defects stay visible to that selection
    instead of being hidden behind an envelope-shape failure.
    """
    if not isinstance(envelope, dict):
        return ["attestation envelope is not an object"]
    record = envelope.get("record")
    if not isinstance(record, dict):
        return ["attestation record is not an object"]
    problems = []
    if set(record) != recordprovenance.ATTESTATION_RECORD_FIELDS:
        problems.append("attestation record has the wrong fields")
    problems.extend(recordprovenance.attestation_producer_problems(record))
    return problems


def _attestation_currency_problems(envelope, context):
    record = envelope["record"]
    atype = record.get("type")
    if atype != context.required_type:
        return ["attestation type %r is not the required %r"
                % (atype, context.required_type)]
    problems = []
    if context.check_scope and \
            record.get("edition") != context.expected_edition:
        problems.append("attestation has the wrong edition scope")
    sides = record.get("sides")
    if not isinstance(sides, dict) or set(sides) != context.expected_sides:
        problems.append(
            "%s attestation sides must be exactly %s"
            % (atype, sorted(context.expected_sides)))
        return problems
    for side in sorted(context.expected_sides):
        if side not in context.side_digests:
            problems.append(
                "current digest for attestation side %r is unavailable"
                % side)
        elif sides[side] != context.side_digests[side]:
            problems.append("attestation side %r is not current" % side)
    return problems


def _context_authorization_problems(envelope, context):
    return list(context.authorization_problems(envelope))


@dataclass(frozen=True)
class RecordAdapter:
    """Closed per-kind discrimination predicates over record envelopes."""
    context_type: type
    format_problems: object
    currency_problems: object
    authorization_problems: object


_ADAPTERS = {
    "qa-record": RecordAdapter(
        QaRecordContext, _qa_format_problems, _qa_currency_problems,
        _context_authorization_problems),
    "release-record": RecordAdapter(
        ReleaseRecordContext, _release_format_problems,
        _release_currency_problems, _context_authorization_problems),
    "bundle-record": RecordAdapter(
        BundleRecordContext, _bundle_format_problems,
        _bundle_currency_problems, _bundle_authorization_problems),
    "attestation": RecordAdapter(
        AttestationContext, _attestation_format_problems,
        _attestation_currency_problems, _context_authorization_problems),
}


def adapter_for(kind):
    """Return the closed adapter for *kind*; unknown kinds fail closed."""
    adapter = _ADAPTERS.get(kind)
    if adapter is None:
        raise ValueError("unknown verification record kind %r" % kind)
    return adapter


def classify(kind, envelopes, context):
    """Classify records without allowing inventory presence to imply authority.

    The closed adapter for *kind* supplies the three discrimination
    predicates; *context* carries the explicit current binding and the
    authorization predicate they evaluate against.  Valid-format
    non-current records are preserved as superseded evidence; malformed
    records remain explicit failures.  An unknown kind or a context of the
    wrong type fails closed.
    """
    adapter = adapter_for(kind)
    if not isinstance(context, adapter.context_type):
        raise ValueError(
            "%s resolution requires a %s context"
            % (kind, adapter.context_type.__name__))
    current = []
    superseded = []
    invalid = []
    rejected = []
    for envelope in envelopes:
        digest = envelope.get("digest", "unknown") \
            if isinstance(envelope, dict) else "unknown"
        malformed = tuple(adapter.format_problems(envelope, context))
        if malformed:
            invalid.append(RejectedRecord(digest, malformed))
            continue
        stale = tuple(adapter.currency_problems(envelope, context))
        if stale:
            superseded.append(envelope)
            continue
        unauthorized = tuple(adapter.authorization_problems(
            envelope, context))
        if unauthorized:
            rejected.append(RejectedRecord(digest, unauthorized))
            continue
        current.append(envelope)
    return RecordResolution(
        tuple(current), tuple(superseded), tuple(invalid), tuple(rejected))
