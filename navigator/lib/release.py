"""Release lifecycle — promotion by verification (TDD §10.8, §10.10, §13).

candidate -> manual QA against those exact bytes (record-qa writes the
immutable authorization) -> release re-derives, verifies the content-input
lock byte-identically, byte-compares the candidate, verifies every
double-sided attestation in the envelope, and seals the same bytes, writing
the sealed artifact, its checksum, and the release-record.
"""

import locale
import platform
import sys

from . import canon


def reproduction_diagnostics():
    """Non-normative runtime diagnostics — a sibling of the lock, excluded
    from the lock digest and the candidate<->release equality check."""
    return {
        "interpreter": sys.version.split()[0],
        "platform": platform.platform(),
        "locale": ".".join(str(x) for x in locale.getlocale() if x) or "C",
        "unicodedata": __import__("unicodedata").unidata_version,
    }


def exact_set_check(lock, declared_inputs):
    """The read log must equal the edition config's declared transitive
    input set exactly."""
    read = {e["path"] for e in lock["reads"]}
    declared = set(declared_inputs)
    missing = declared - read
    extra = read - declared
    problems = []
    if missing:
        problems.append("declared but never read: %s" % sorted(missing))
    if extra:
        problems.append("read but not declared: %s" % sorted(extra))
    return problems


def verify_envelope(qa_record, candidate_digest, lock_digest, attestations):
    """Release-verification envelope: the QA record must authorize exactly
    these candidate bytes and this lock, and every referenced double-sided
    attestation must be present and current."""
    problems = []
    rec = qa_record["record"]
    if rec.get("candidateDigest") != candidate_digest:
        problems.append(
            "QA record authorizes candidate %s, not %s"
            % (rec.get("candidateDigest"), candidate_digest))
    if rec.get("lockDigest") != lock_digest:
        problems.append("QA record lock digest does not match this build")
    referenced = set(rec.get("attestations", []))
    present = {a["digest"] for a in attestations}
    for digest in referenced - present:
        problems.append("attestation %s referenced by QA record is missing"
                        % digest)
    return problems


def attestation_current(att, side_digests):
    """Double-sided binding: every side recorded in the attestation must
    equal the current digest of that side."""
    problems = []
    for side, digest in att["record"].get("sides", {}).items():
        current = side_digests.get(side)
        if current is None:
            problems.append("attestation side %r has no current digest" % side)
        elif current != digest:
            problems.append(
                "attestation side %r stale: recorded %s, current %s"
                % (side, digest, current))
    return problems


def checksum_text(name, data):
    return "%s  %s\n" % (canon.bytes_digest(data), name)
