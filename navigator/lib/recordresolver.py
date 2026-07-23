"""Typed separation between record inventory and current authorization."""

from dataclasses import dataclass


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


def classify(envelopes, format_problems, currency_problems,
             authorization_problems=None):
    """Classify records without allowing inventory presence to imply authority.

    ``format_problems`` and ``currency_problems`` receive one envelope and
    return problem sequences.  Valid-format non-current records are preserved
    as superseded evidence; malformed records remain explicit failures.
    """
    current = []
    superseded = []
    invalid = []
    rejected = []
    for envelope in envelopes:
        digest = envelope.get("digest", "unknown") \
            if isinstance(envelope, dict) else "unknown"
        malformed = tuple(format_problems(envelope))
        if malformed:
            invalid.append(RejectedRecord(digest, malformed))
            continue
        stale = tuple(currency_problems(envelope))
        if stale:
            superseded.append(envelope)
            continue
        unauthorized = tuple(authorization_problems(envelope)) \
            if authorization_problems is not None else ()
        if unauthorized:
            rejected.append(RejectedRecord(digest, unauthorized))
            continue
        current.append(envelope)
    return RecordResolution(
        tuple(current), tuple(superseded), tuple(invalid), tuple(rejected))
