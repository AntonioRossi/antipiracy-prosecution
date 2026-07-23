"""Deterministic STORE ZIP — the single in-repo bundle writer (TDD §10.9).

Fixed member ordering (as enumerated by the bundle config), STORE method
(no compression), declared timestamps, fixed permissions (0644), pinned
UTF-8 filename flag (bit 11), and a plain central directory. Verified
against a byte-exact golden bundle fixture.
"""

import datetime
import io
import re
import struct
import zipfile
import zlib

from . import authority, canon, qaevidence, recordprovenance
from . import gateway
from . import release as release_mod

_UTF8_FLAG = 0x0800
_EXT_ATTRS = (0o100644 << 16)
_CHECKSUM_RE = re.compile(
    r"^(sha256/c1:[0-9a-f]{64})  ([^\r\n]+)\n$")
_UTC_SECOND_RE = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")


class BundleError(ValueError):
    """A bundle plan or ZIP member is unsafe, ambiguous, or stale."""


_RELEASE_FIELDS = recordprovenance.RELEASE_RECORD_FIELDS
_QA_FIELDS = recordprovenance.QA_RECORD_FIELDS
_ATTESTATION_FIELDS = recordprovenance.ATTESTATION_RECORD_FIELDS
_ATTESTATION_SIDES = {
    "inventory-completeness": frozenset(("claimSet", "gateInventory")),
    "qa-priority-map": frozenset(("relationSet", "priorityMap")),
    "qa-crosswalk": frozenset(("relationSet", "crosswalk")),
    "legend-approval": frozenset(("legendWording",)),
    "manifest-approval": frozenset(("manifestWording",)),
    "support-matrix-approval": frozenset(("supportMatrix",)),
}
_BASE_RELEASE_ATTESTATIONS = frozenset((
    "inventory-completeness", "qa-priority-map", "legend-approval",
    "support-matrix-approval",
))
_EDITION_ATTESTATIONS = frozenset((
    "inventory-completeness", "qa-priority-map", "qa-crosswalk",
))
def validate_member_name(name):
    """Reject names that are unsafe or ambiguous when a ZIP is extracted."""
    if not isinstance(name, str) or not name:
        raise BundleError("ZIP member name must be a non-empty string")
    if canon.normalize_nfc(name) != name:
        raise BundleError("ZIP member name must be NFC: %r" % name)
    if name.startswith("/") or "\\" in name:
        raise BundleError("ZIP member name must be a relative POSIX path: %r"
                          % name)
    parts = name.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise BundleError("ZIP member name has an unsafe path segment: %r"
                          % name)
    if ":" in parts[0] or any(":" in part for part in parts):
        raise BundleError("ZIP member name has a drive/stream separator: %r"
                          % name)
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in name):
        raise BundleError("ZIP member name has a control character: %r"
                          % name)
    if len(name.encode("utf-8")) > 0xFFFF:
        raise BundleError("ZIP member name is too long")
    return name


def _validate_members(members):
    members = list(members)
    if len(members) > 0xFFFF:
        raise BundleError("ZIP32 supports at most 65535 members")
    out = []
    seen = {}
    for item in members:
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            raise BundleError("each ZIP member must be an (arcname, bytes) pair")
        arcname, data = item
        validate_member_name(arcname)
        key = arcname.casefold()
        if key in seen:
            raise BundleError("duplicate ZIP member names %r and %r"
                              % (seen[key], arcname))
        seen[key] = arcname
        if not isinstance(data, bytes):
            raise BundleError("ZIP member %r data must be bytes" % arcname)
        if len(data) > 0xFFFFFFFF:
            raise BundleError("ZIP32 member %r is too large" % arcname)
        out.append((arcname, data))
    return out


def parse_utc_second(ts, label="declaredTimestamp"):
    """Parse one canonical RFC 3339 UTC timestamp at second precision."""
    if not isinstance(ts, str) or _UTC_SECOND_RE.fullmatch(ts) is None:
        raise BundleError("%s must be a canonical RFC 3339 UTC second" % label)
    try:
        parsed = datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        raise BundleError("%s must be a real RFC 3339 UTC second" % label)
    if parsed.strftime("%Y-%m-%dT%H:%M:%SZ") != ts:
        raise BundleError("%s must use canonical UTC-second form" % label)
    return parsed


def _dos_datetime(ts):
    """Declared timestamp 'YYYY-MM-DDTHH:MM:SSZ' -> DOS date/time words."""
    parsed = parse_utc_second(ts)
    if not 1980 <= parsed.year <= 2107:
        raise BundleError("declaredTimestamp is outside the ZIP DOS range")
    if parsed.second % 2:
        raise BundleError("declaredTimestamp needs an even ZIP DOS second")
    y, mo, d = parsed.year, parsed.month, parsed.day
    h, mi, s = parsed.hour, parsed.minute, parsed.second
    return (((y - 1980) << 9) | (mo << 5) | d,
            (h << 11) | (mi << 5) | (s // 2))


def build_zip(members, declared_timestamp):
    """members: ordered list of (arcname, bytes). Returns ZIP bytes."""
    members = _validate_members(members)
    ddate, dtime = _dos_datetime(declared_timestamp)
    out = bytearray()
    central = bytearray()
    for arcname, data in members:
        name = arcname.encode("utf-8")
        crc = zlib.crc32(data) & 0xFFFFFFFF
        offset = len(out)
        out += struct.pack(
            "<4sHHHHHIIIHH", b"PK\x03\x04", 20, _UTF8_FLAG, 0,
            dtime, ddate, crc, len(data), len(data), len(name), 0)
        out += name
        out += data
        central += struct.pack(
            "<4sHHHHHHIIIHHHHHII", b"PK\x01\x02", (3 << 8) | 20, 20,
            _UTF8_FLAG, 0, dtime, ddate, crc, len(data), len(data),
            len(name), 0, 0, 0, 0, _EXT_ATTRS, offset)
        central += name
    cd_offset = len(out)
    out += central
    out += struct.pack(
        "<4sHHHHIIH", b"PK\x05\x06", 0, 0, len(members), len(members),
        len(central), cd_offset, 0)
    return bytes(out)


def parse_detached_checksum(data):
    """Return the exact (digest, member name) from a stored checksum file."""
    if not isinstance(data, bytes):
        raise BundleError("detached checksum must be read as bytes")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        raise BundleError("detached checksum is not UTF-8")
    match = _CHECKSUM_RE.fullmatch(text)
    if match is None:
        raise BundleError("detached checksum must contain one canonical line")
    try:
        canon.parse_digest(match.group(1))
    except canon.CanonError as exc:
        raise BundleError("invalid detached checksum digest: %s" % exc)
    validate_member_name(match.group(2))
    return match.group(1), match.group(2)


def verify_detached_checksum(data, artifact_name, artifact_digest):
    """Verify stored checksum bytes against one exact configured artifact."""
    digest, name = parse_detached_checksum(data)
    if name != artifact_name:
        raise BundleError("detached checksum names %r, expected %r"
                          % (name, artifact_name))
    if digest != artifact_digest:
        raise BundleError("detached checksum for %s is stale" % artifact_name)


def _require_digest(value, field):
    try:
        canon.parse_digest(value)
    except canon.CanonError as exc:
        raise BundleError("%s: %s" % (field, exc))


def _require_artifact_path(kind, name, field):
    try:
        gateway.validate_artifact_path(kind, name)
    except gateway.GatewayError as exc:
        raise BundleError("%s: %s" % (field, exc))


def validate_bundle_config(cfg, expected_edition_count=2):
    """Validate the closed, member-enumerating bundle configuration."""
    if not isinstance(cfg, dict):
        raise BundleError("bundle config must be an object")
    allowed = {"bundleVersion", "releaseProfile", "name", "comment",
               "editions", "declaredTimestamp", "manifestApproval",
               "members"}
    if set(cfg) - allowed:
        raise BundleError("unknown bundle config fields: %s"
                          % sorted(set(cfg) - allowed))
    required = allowed - {"comment"}
    missing = required - set(cfg)
    if missing:
        raise BundleError("missing bundle config fields: %s" % sorted(missing))
    if cfg["bundleVersion"] != "3":
        raise BundleError("unsupported bundleVersion %r"
                          % cfg["bundleVersion"])
    release_profile = cfg.get("releaseProfile")
    if release_profile not in ("technical-preview", "validated-release"):
        raise BundleError("releaseProfile must be technical-preview or "
                          "validated-release")
    validate_member_name(cfg["name"])
    _require_artifact_path("bundle", cfg["name"], "name")
    if not cfg["name"].endswith(".zip"):
        raise BundleError("bundle output name must end in .zip")
    if release_profile == "technical-preview" and \
            "TECHNICAL-PREVIEW" not in cfg["name"]:
        raise BundleError(
            "technical-preview bundle name must contain TECHNICAL-PREVIEW")
    if "comment" in cfg and (not isinstance(cfg["comment"], str) or
                             not cfg["comment"]):
        raise BundleError("comment must be a non-empty string when present")
    _dos_datetime(cfg["declaredTimestamp"])
    _require_digest(cfg["manifestApproval"], "manifestApproval")
    if not isinstance(cfg["editions"], list) or not cfg["editions"] or \
            len(cfg["editions"]) != len(set(cfg["editions"])) or \
            not all(isinstance(e, str) and e for e in cfg["editions"]):
        raise BundleError("editions must be a unique non-empty string list")
    if not isinstance(expected_edition_count, int) or \
            isinstance(expected_edition_count, bool) or \
            expected_edition_count < 1:
        raise BundleError("expected edition count must be a positive integer")
    if len(cfg["editions"]) != expected_edition_count:
        raise BundleError("delivery bundle must contain exactly %d editions"
                          % expected_edition_count)
    members = cfg["members"]
    if not isinstance(members, list) or not members:
        raise BundleError("members must be a non-empty ordered list")

    names = set()
    folded_names = set()
    sealed = {}
    checksums = {}
    manifest_count = 0
    sealed_editions = []
    for index, member in enumerate(members):
        if not isinstance(member, dict):
            raise BundleError("members[%d] must be an object" % index)
        kind = member.get("kind")
        common = {"kind", "name", "digest"}
        if kind == "sealed":
            expected = common | {"edition", "releaseRecord"}
        elif kind == "artifact-checksum":
            expected = common | {"artifact"}
        elif kind == "bundle-manifest":
            expected = common | {"wordingDigest"}
        else:
            raise BundleError("members[%d] has unknown kind %r"
                              % (index, kind))
        if set(member) != expected:
            raise BundleError("members[%d] fields must be exactly %s"
                              % (index, sorted(expected)))
        name = validate_member_name(member["name"])
        folded = name.casefold()
        if name in names or folded in folded_names:
            raise BundleError("duplicate configured member name %r" % name)
        names.add(name)
        folded_names.add(folded)
        _require_digest(member["digest"], "members[%d].digest" % index)

        if kind == "sealed":
            edition = member["edition"]
            if not isinstance(edition, str) or not edition:
                raise BundleError("members[%d].edition must be non-empty"
                                  % index)
            if name in sealed or edition in sealed_editions:
                raise BundleError("duplicate sealed artifact/edition")
            _require_digest(member["releaseRecord"],
                            "members[%d].releaseRecord" % index)
            sealed[name] = member
            sealed_editions.append(edition)
        elif kind == "artifact-checksum":
            artifact = member["artifact"]
            if artifact not in sealed:
                raise BundleError("checksum member %r must follow its sealed "
                                  "artifact" % name)
            if name != artifact + ".sha256":
                raise BundleError(
                    "checksum member %r must use its sealed artifact's exact "
                    "checksum path %r" % (name, artifact + ".sha256"))
            if artifact in checksums:
                raise BundleError("sealed artifact %r has two checksums"
                                  % artifact)
            checksums[artifact] = member
        else:
            manifest_count += 1
            _require_digest(member["wordingDigest"],
                            "members[%d].wordingDigest" % index)
    if sealed_editions != cfg["editions"]:
        raise BundleError("editions must match sealed-member order")
    if set(checksums) != set(sealed):
        raise BundleError("every sealed artifact needs one configured checksum")
    if manifest_count != 1:
        raise BundleError("members must enumerate exactly one bundle-manifest")

    outputs = (cfg["name"], cfg["name"] + ".sha256")
    for index, output in enumerate(outputs):
        validate_member_name(output)
        _require_artifact_path(
            "bundle" if index == 0 else "bundle-checksum", output,
            "bundle output")
        if output.casefold() in folded_names:
            raise BundleError(
                "configured member name collides with bundle output %r"
                % output)
    # Preserve the more specific cross-output collision diagnostic above, then
    # enforce the disjoint kind/path families before any member is resolved or
    # any artifact output is written.
    for index, member in enumerate(members):
        _require_artifact_path(
            member["kind"], member["name"], "members[%d].name" % index)


def _record_by_digest(records, digest, label, kind):
    if not isinstance(records, list):
        raise BundleError("%s collection is not a list" % label)
    matches = [record for record in records
               if isinstance(record, dict) and
               record.get("digest") == digest]
    if len(matches) != 1:
        raise BundleError("%s digest %s resolved to %d records"
                          % (label, digest, len(matches)))
    envelope = matches[0]
    if set(envelope) != {"kind", "digest", "record"} or \
            envelope.get("kind") != kind:
        raise BundleError("%s has an invalid typed envelope" % label)
    try:
        actual = canon.composite_digest(
            "aa11393:%s:c1" % kind, envelope["record"])
    except (KeyError, TypeError, ValueError) as exc:
        raise BundleError("%s record is not canonical: %s" % (label, exc))
    if actual != digest:
        raise BundleError("%s digest does not match its record" % label)
    return envelope


def _digest_problem(value, label):
    try:
        canon.parse_digest(value)
    except (canon.CanonError, TypeError) as exc:
        return ["%s is not a canonical digest: %s" % (label, exc)]
    return []


def _authorized_record_problems(record, label):
    problems = []
    if record.get("approvalStatus") != "passed":
        problems.append("%s approvalStatus is not 'passed'" % label)
    operator = record.get("operator")
    if not authority.is_identified_operator_identity(operator):
        problems.append("%s has no identified operator" % label)
    if not authority.is_authoritative_operator_kind(
            record.get("operatorKind")):
        problems.append(
            "%s operatorKind is not release-authoritative" % label)
    return problems


def _typed_read_list_problems(reads, fields, label):
    if not isinstance(reads, list) or not reads:
        return ["%s must be a non-empty list" % label]
    problems = []
    paths = []
    for index, item in enumerate(reads):
        item_label = "%s[%d]" % (label, index)
        if not isinstance(item, dict) or set(item) != fields:
            problems.append("%s has the wrong fields" % item_label)
            continue
        for field in fields - {"digest"}:
            if not isinstance(item.get(field), str) or not item[field]:
                problems.append("%s.%s is not a non-empty string"
                                % (item_label, field))
        problems.extend(_digest_problem(item.get("digest"),
                                        item_label + ".digest"))
        identity = tuple(item.get(field) for field in sorted(fields - {
            "digest"}))
        if all(isinstance(value, str) for value in identity):
            paths.append(identity)
    if len(paths) != len(set(paths)):
        problems.append("%s contains duplicate entries" % label)
    return problems


def _digest_list_problems(values, label):
    if not isinstance(values, list) or not values:
        return ["%s must be a non-empty digest list" % label]
    problems = []
    for index, value in enumerate(values):
        problems.extend(_digest_problem(value, "%s[%d]" % (label, index)))
    if all(isinstance(value, str) for value in values):
        if len(values) != len(set(values)):
            problems.append("%s contains duplicate digests" % label)
        if values != sorted(values):
            problems.append("%s is not deterministically sorted" % label)
    return problems


def _attestation_record_problems(record, edition, approval_evidence_problems):
    if not isinstance(record, dict):
        return ["attestation record is not an object"]
    problems = []
    if set(record) != _ATTESTATION_FIELDS:
        problems.append("attestation record has the wrong fields")
    problems.extend(recordprovenance.attestation_producer_problems(record))
    problems.extend(_authorized_record_problems(record, "attestation"))
    if not authority.is_final_evidence_text(record.get("note")):
        problems.append("attestation note is not nonempty final evidence")
    try:
        problems.extend(approval_evidence_problems(record))
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        problems.append("attestation approval evidence is malformed: %s" % exc)
    atype = record.get("type")
    expected_sides = _ATTESTATION_SIDES.get(atype) \
        if isinstance(atype, str) else None
    if expected_sides is None:
        problems.append("attestation has unknown type %r" % atype)
        expected_sides = frozenset()
    expected_edition = edition if isinstance(atype, str) and \
        atype in _EDITION_ATTESTATIONS else None
    if record.get("edition") != expected_edition:
        problems.append("%s attestation has the wrong edition scope" % atype)
    sides = record.get("sides")
    if not isinstance(sides, dict) or set(sides) != expected_sides:
        problems.append("%s attestation has the wrong sides" % atype)
    else:
        for side in sorted(sides):
            problems.extend(_digest_problem(
                sides[side], "%s attestation side %s" % (atype, side)))
    return problems


def _attestation_currency_problems(record, current_side_digests):
    """Return defects where an attestation is not for the current sides.

    Record/envelope rehashing proves only that a changed record is internally
    self-consistent.  Bundle promotion also needs an independently derived
    digest for every projected side so a rehashed stale approval cannot be
    promoted as current evidence.
    """
    if not isinstance(record, dict):
        return []
    atype = record.get("type")
    expected_sides = _ATTESTATION_SIDES.get(atype)
    sides = record.get("sides")
    if expected_sides is None or not isinstance(sides, dict) or \
            set(sides) != expected_sides:
        return []
    if not isinstance(current_side_digests, dict):
        return ["current attestation side digests are unavailable"]
    problems = []
    for side in sorted(expected_sides):
        if side not in current_side_digests:
            problems.append("current digest for attestation side %r is "
                            "unavailable" % side)
            continue
        current = current_side_digests[side]
        current_problems = _digest_problem(
            current, "current attestation side %s" % side)
        problems.extend(current_problems)
        if not current_problems and sides[side] != current:
            problems.append("%s attestation side %s is not current"
                            % (atype, side))
    return problems


def release_chain_problems(release_envelope, qa_records, attestations,
                           required_attestation_types,
                           current_side_digests,
                           approval_evidence_problems,
                           current_acceptance_context=None,
                           current_qa_authorization_context=None):
    """Return structural/authorization defects in a release's full chain.

    Bundle promotion deliberately does not infer authorization from the mere
    presence of a release record.  The pinned release must be a current-format
    authorized operator approval and must resolve its exact authorized QA
    record and all of that QA record's typed, final attestations.  Its
    private-input lock and named support approver must also equal independently
    derived current values supplied by the caller, and the support approval's
    operator must be that current named approver.
    """
    if not isinstance(release_envelope, dict):
        return ["release envelope is not an object"]
    record = release_envelope.get("record")
    if not isinstance(record, dict):
        return ["release record is not an object"]
    problems = []
    if set(record) != _RELEASE_FIELDS:
        problems.append("release record has the wrong fields")
    if record.get("recordVersion") != "2":
        problems.append("release record has the wrong version")
    problems.extend(_authorized_record_problems(record, "release record"))
    edition = record.get("edition")
    if not isinstance(edition, str) or not edition:
        problems.append("release edition is not a non-empty string")
    sealed = record.get("sealed")
    if not isinstance(sealed, str) or not sealed:
        problems.append("release sealed name is not a non-empty string")
    problems.extend(_digest_problem(record.get("sealedDigest"),
                                    "release sealedDigest"))
    problems.extend(_digest_problem(record.get("lockDigest"),
                                    "release lockDigest"))
    release_refs = record.get("attestations")
    problems.extend(_digest_list_problems(
        release_refs, "release attestation references"))
    try:
        parse_utc_second(
            record.get("declaredReleaseTimestamp"),
            "release declaredReleaseTimestamp")
    except BundleError as exc:
        problems.append(str(exc))

    profile_contract = current_acceptance_context.get(
        "releaseProfileContract") \
        if isinstance(current_acceptance_context, dict) else None
    try:
        expected_profile_fields = release_mod.profile_record_fields(
            profile_contract)
    except release_mod.AcceptanceError as exc:
        problems.append("current release profile is unavailable: %s" % exc)
        expected_profile_fields = None
    if expected_profile_fields is not None:
        for field, expected in expected_profile_fields.items():
            if record.get(field) != expected:
                problems.append(
                    "release record %s does not match the current release "
                    "profile" % field)
    manual_qa = profile_contract.get("manualQaEvidence") \
        if isinstance(profile_contract, dict) else None

    if manual_qa == "deferred":
        if record.get("qaRecord") is not None:
            problems.append(
                "technical-preview release qaRecord must be null")
        receipt_subjects = release_mod.release_subjects(
            edition, record.get("sealedDigest"), record.get("lockDigest"),
            None, None, profile_contract)
        problems.extend(release_mod.acceptance_receipt_problems(
            record.get("acceptanceReceipt"), "release",
            current_acceptance_context, receipt_subjects))

        by_type = {}
        if isinstance(release_refs, list):
            for digest in release_refs:
                try:
                    att = _record_by_digest(
                        attestations, digest, "attestation", "attestation")
                except BundleError as exc:
                    problems.append(str(exc))
                    continue
                att_record = att.get("record")
                att_problems = _attestation_record_problems(
                    att_record, edition, approval_evidence_problems)
                att_problems.extend(_attestation_currency_problems(
                    att_record, current_side_digests))
                problems.extend("attestation %s: %s" % (digest, problem)
                                for problem in att_problems)
                if isinstance(att_record, dict) and \
                        isinstance(att_record.get("type"), str):
                    by_type.setdefault(
                        att_record["type"], []).append(att_record)
        required_types = frozenset(required_attestation_types) \
            if isinstance(required_attestation_types, (
                set, frozenset, list, tuple)) else frozenset()
        allowed_types = _BASE_RELEASE_ATTESTATIONS | {"qa-crosswalk"}
        if not _BASE_RELEASE_ATTESTATIONS.issubset(required_types) or \
                not required_types.issubset(allowed_types):
            problems.append("release attestation policy is invalid")
        if frozenset(by_type) != required_types or \
                any(len(records) != 1 for records in by_type.values()):
            problems.append(
                "technical-preview release does not reference exactly one "
                "current required attestation of each type")
        return problems

    if manual_qa != "required":
        problems.append("release manual-QA profile policy is unavailable")
        return problems
    problems.extend(_digest_problem(record.get("qaRecord"),
                                    "release qaRecord"))

    try:
        qa = _record_by_digest(
            qa_records, record.get("qaRecord"), "QA record", "qa-record")
    except BundleError as exc:
        problems.append(str(exc))
        return problems
    qa_record = qa.get("record")
    if not isinstance(qa_record, dict):
        problems.append("QA record is not an object")
        return problems
    if set(qa_record) != _QA_FIELDS:
        problems.append("QA record has the wrong fields")
    problems.extend(_authorized_record_problems(qa_record, "QA record"))
    if qa_record.get("releaseProfile") != "validated-release" or \
            qa_record.get("releaseProfile") != record.get("releaseProfile"):
        problems.append(
            "QA releaseProfile does not match the validated release")
    if qa_record.get("edition") != edition:
        problems.append("QA edition does not match the release")
    if qa_record.get("candidateDigest") != record.get("sealedDigest"):
        problems.append("QA candidate digest does not match the release")
    if qa_record.get("lockDigest") != record.get("lockDigest"):
        problems.append("QA content lock digest does not match the release")

    qa_context_fields = frozenset((
        "qaInputLock", "supportMatrixApprover", "supportMatrixTargets",
        "supportMatrixViewport", "apiProbeApis",
    ))
    if not isinstance(current_qa_authorization_context, dict) or \
            set(current_qa_authorization_context) != qa_context_fields:
        problems.append(
            "current QA authorization context has the wrong fields")
        current_qa_authorization_context = {}

    content_lock = qa_record.get("contentLock")
    problems.extend(_typed_read_list_problems(
        content_lock, frozenset(("path", "digest")), "QA contentLock"))
    if isinstance(content_lock, list):
        try:
            expected_lock = canon.composite_digest(
                "aa11393:lock:c1",
                {"reads": content_lock, "canonVersion": canon.CANON_VERSION})
            if qa_record.get("lockDigest") != expected_lock:
                problems.append("QA contentLock does not derive lockDigest")
        except (TypeError, ValueError) as exc:
            problems.append("QA contentLock is not canonical: %s" % exc)

    qa_lock = qa_record.get("qaInputLock")
    qa_lock_fields = frozenset((
        "lockType", "canonVersion", "candidateDigest",
        "contentLockDigest", "registryRead", "reads", "lockDigest",
    ))
    if not isinstance(qa_lock, dict) or set(qa_lock) != qa_lock_fields:
        problems.append("QA internal-input lock has the wrong fields")
    else:
        if qa_lock.get("lockType") != "internal-qa-inputs":
            problems.append("QA internal-input lock has the wrong type")
        if qa_lock.get("canonVersion") != canon.CANON_VERSION:
            problems.append("QA internal-input lock has the wrong canonVersion")
        if qa_lock.get("candidateDigest") != record.get("sealedDigest"):
            problems.append("QA internal-input lock does not bind candidate")
        if qa_lock.get("contentLockDigest") != record.get("lockDigest"):
            problems.append("QA internal-input lock does not bind content lock")
        problems.extend(_typed_read_list_problems(
            [qa_lock.get("registryRead")],
            frozenset(("path", "digest")),
            "QA internal-input registry read"))
        problems.extend(_typed_read_list_problems(
            qa_lock.get("reads"),
            frozenset(("role", "corpusId", "path", "digest")),
            "QA internal-input reads"))
        try:
            payload = {field: qa_lock[field]
                       for field in qa_lock_fields - {"lockDigest"}}
            expected_qa_lock = canon.composite_digest(
                "aa11393:lock:c1", payload)
            if qa_lock.get("lockDigest") != expected_qa_lock:
                problems.append("QA internal-input lock digest is invalid")
        except (KeyError, TypeError, ValueError) as exc:
            problems.append("QA internal-input lock is not canonical: %s" % exc)
    if qa_lock != current_qa_authorization_context.get("qaInputLock"):
        problems.append("QA internal-input lock is not current")

    qa_lock_digest = qa_lock.get("lockDigest") \
        if isinstance(qa_lock, dict) else None
    receipt_subjects = release_mod.release_subjects(
        edition, record.get("sealedDigest"), record.get("lockDigest"),
        record.get("qaRecord"), qa_lock_digest, profile_contract)
    problems.extend(release_mod.acceptance_receipt_problems(
        record.get("acceptanceReceipt"), "release",
        current_acceptance_context, receipt_subjects))

    diagnostics = qa_record.get("reproductionDiagnostics")
    diagnostic_fields = {"interpreter", "platform", "locale", "unicodedata"}
    if not isinstance(diagnostics, dict) or set(diagnostics) != diagnostic_fields \
            or not all(isinstance(value, str) and value
                       for value in diagnostics.values()):
        problems.append("QA reproductionDiagnostics is not fully typed")

    support_contract = {
        "targets": current_qa_authorization_context.get(
            "supportMatrixTargets"),
        "viewport": current_qa_authorization_context.get(
            "supportMatrixViewport"),
    }
    problems.extend(
        "QA %s" % problem
        for problem in qaevidence.manual_check_problems(
            qa_record.get("manualChecks"), qaevidence.MANUAL_QA_FIELDS,
            support_matrix=support_contract,
            api_probe_apis=current_qa_authorization_context.get(
                "apiProbeApis"),
            operator=qa_record.get("operator"),
            operator_kind=qa_record.get("operatorKind"),
            manual_evidence_version=qa_record.get(
                "manualEvidenceVersion")))

    support = qa_record.get("supportMatrix")
    if not isinstance(support, dict) or set(support) != {
            "digest", "approver", "approvalAttestation"}:
        problems.append("QA supportMatrix evidence has the wrong fields")
        support = {}
    problems.extend(_digest_problem(support.get("digest"),
                                    "QA supportMatrix digest"))
    problems.extend(_digest_problem(support.get("approvalAttestation"),
                                    "QA supportMatrix approval"))
    if not authority.is_identified_operator_identity(
            support.get("approver")):
        problems.append("QA supportMatrix has no named approver")
    current_support_approver = current_qa_authorization_context.get(
        "supportMatrixApprover")
    if not authority.is_identified_operator_identity(
            current_support_approver):
        problems.append("current supportMatrix approver is unavailable")
    elif support.get("approver") != current_support_approver:
        problems.append("QA supportMatrix approver is not current")
    legend = qa_record.get("legendApproval")
    if not isinstance(legend, dict) or set(legend) != {
            "digest", "approvalAttestation"}:
        problems.append("QA legendApproval evidence has the wrong fields")
        legend = {}
    problems.extend(_digest_problem(legend.get("digest"),
                                    "QA legendApproval digest"))
    problems.extend(_digest_problem(legend.get("approvalAttestation"),
                                    "QA legendApproval attestation"))

    qa_refs = qa_record.get("attestations")
    problems.extend(_digest_list_problems(
        qa_refs, "QA attestation references"))
    if release_refs != qa_refs:
        problems.append("release and QA attestation references differ")
    if not isinstance(qa_refs, list):
        return problems

    by_type = {}
    by_digest = {}
    for digest in qa_refs:
        try:
            att = _record_by_digest(
                attestations, digest, "attestation", "attestation")
        except BundleError as exc:
            problems.append(str(exc))
            continue
        att_record = att.get("record")
        att_problems = _attestation_record_problems(
            att_record, edition, approval_evidence_problems)
        att_problems.extend(_attestation_currency_problems(
            att_record, current_side_digests))
        problems.extend("attestation %s: %s" % (digest, problem)
                        for problem in att_problems)
        if isinstance(att_record, dict):
            atype = att_record.get("type")
            if isinstance(atype, str):
                by_type.setdefault(atype, []).append(att_record)
                by_digest[digest] = att_record
    required_types = frozenset(required_attestation_types) \
        if isinstance(required_attestation_types, (set, frozenset, list,
                                                    tuple)) else frozenset()
    allowed_types = _BASE_RELEASE_ATTESTATIONS | {"qa-crosswalk"}
    if not _BASE_RELEASE_ATTESTATIONS.issubset(required_types) or \
            not required_types.issubset(allowed_types):
        problems.append("release attestation policy is invalid")
    if frozenset(by_type) != required_types or \
            any(len(records) != 1 for records in by_type.values()):
        problems.append("QA does not reference exactly one required "
                        "attestation of each type")

    support_att = by_digest.get(support.get("approvalAttestation"))
    if not isinstance(support_att, dict) or \
            support_att.get("type") != "support-matrix-approval" or \
            support_att.get("sides", {}).get("supportMatrix") != \
            support.get("digest"):
        problems.append("QA supportMatrix is not bound to its approval")
    elif not authority.operator_identity_matches(
            support_att.get("operator"), current_support_approver):
        problems.append(
            "support-matrix-approval operator does not match support matrix "
            "approver")
    legend_att = by_digest.get(legend.get("approvalAttestation"))
    if not isinstance(legend_att, dict) or \
            legend_att.get("type") != "legend-approval" or \
            legend_att.get("sides", {}).get("legendWording") != \
            legend.get("digest"):
        problems.append("QA legend wording is not bound to its approval")
    return problems


def resolve_bundle_members(cfg, release_records, qa_records, attestations,
                           read_artifact, manifest_bytes,
                           manifest_wording_digest,
                           approval_evidence_problems,
                           required_attestations_by_edition,
                           current_sides_by_edition,
                           expected_edition_count=2,
                           acceptance_context_by_edition=None,
                           qa_authorization_context_by_edition=None):
    """Resolve and verify a configured bundle plan without writing outputs.

    ``read_artifact(kind, name)`` must return stored bytes.  In particular,
    detached checksums are consumed from storage rather than regenerated.
    Every edition must also have an independently derived current QA
    authorization context; record-embedded context alone is never trusted.
    """
    validate_bundle_config(cfg, expected_edition_count)
    if not isinstance(required_attestations_by_edition, dict) or \
            set(required_attestations_by_edition) != set(cfg["editions"]):
        raise BundleError("required-attestation policy must cover exactly "
                          "the configured editions")
    if not isinstance(current_sides_by_edition, dict) or \
            set(current_sides_by_edition) != set(cfg["editions"]):
        raise BundleError("current attestation sides must cover exactly "
                          "the configured editions")
    if not isinstance(acceptance_context_by_edition, dict) or \
            set(acceptance_context_by_edition) != set(cfg["editions"]):
        raise BundleError("acceptance receipt context must cover exactly "
                          "the configured editions")
    profile_contract = None
    for edition in cfg["editions"]:
        context = acceptance_context_by_edition[edition]
        if not isinstance(context, dict) or \
                context.get("releaseProfile") != cfg["releaseProfile"]:
            raise BundleError(
                "acceptance receipt context for %s does not bind the "
                "configured release profile" % edition)
        current_contract = context.get("releaseProfileContract")
        try:
            profile_fields = release_mod.profile_record_fields(
                current_contract)
        except release_mod.AcceptanceError as exc:
            raise BundleError(
                "acceptance receipt context for %s has an invalid release "
                "profile: %s" % (edition, exc))
        if profile_fields["releaseProfile"] != cfg["releaseProfile"]:
            raise BundleError(
                "acceptance receipt context for %s has the wrong release "
                "profile contract" % edition)
        if profile_contract is None:
            profile_contract = current_contract
        elif current_contract != profile_contract:
            raise BundleError(
                "acceptance receipt contexts do not share one release "
                "profile contract")
    try:
        manifest_text = manifest_bytes.decode("utf-8")
    except (AttributeError, UnicodeDecodeError) as exc:
        raise BundleError("generated manifest is not UTF-8: %s" % exc)
    if not manifest_text.startswith(profile_contract["artifactLabel"]):
        raise BundleError(
            "generated manifest does not begin with the exact release "
            "profile label")
    if not isinstance(qa_authorization_context_by_edition, dict) or \
            set(qa_authorization_context_by_edition) != set(cfg["editions"]):
        raise BundleError("current QA authorization context must cover exactly "
                          "the configured editions")
    approval = _record_by_digest(
        attestations, cfg["manifestApproval"], "manifest approval",
        "attestation")
    approval_record = approval.get("record")
    approval_shape_problems = _attestation_record_problems(
        approval_record, None, approval_evidence_problems)
    if approval_shape_problems:
        raise BundleError("manifest approval is malformed: %s"
                          % "; ".join(approval_shape_problems))
    if approval_record.get("type") != "manifest-approval" or \
            approval_record.get("edition") is not None:
        raise BundleError("configured approval is not a bundle manifest approval")
    sides = approval_record.get("sides", {})
    if set(sides) != {"manifestWording"} or \
            sides.get("manifestWording") != manifest_wording_digest:
        raise BundleError("configured manifest approval is stale")
    approval_problems = approval_evidence_problems(approval_record)
    if approval_problems:
        raise BundleError(
            "manifest approval is not confirmed authorized operator "
            "evidence: %s"
            % "; ".join(approval_problems))

    resolved = []
    sealed_data = {}
    release_digests = []
    for member in cfg["members"]:
        kind, name = member["kind"], member["name"]
        if kind == "sealed":
            release = _record_by_digest(
                release_records, member["releaseRecord"], "release record",
                "release-record")
            record = release.get("record")
            chain_problems = release_chain_problems(
                release, qa_records, attestations,
                required_attestations_by_edition.get(member["edition"]),
                current_sides_by_edition.get(member["edition"]),
                approval_evidence_problems,
                acceptance_context_by_edition.get(member["edition"]),
                qa_authorization_context_by_edition.get(member["edition"]))
            if chain_problems:
                raise BundleError(
                    "release record %s is not fully authorized: %s"
                    % (member["releaseRecord"], "; ".join(chain_problems)))
            expected = (member["edition"], name, member["digest"],
                        cfg["releaseProfile"])
            actual = (record.get("edition"), record.get("sealed"),
                      record.get("sealedDigest"),
                      record.get("releaseProfile"))
            if actual != expected:
                raise BundleError("release record %s does not bind configured "
                                  "edition/member/digest/profile"
                                  % member["releaseRecord"])
            data = read_artifact("sealed", name)
            if canon.bytes_digest(data) != member["digest"]:
                raise BundleError("sealed member %s does not match config digest"
                                  % name)
            sealed_data[name] = data
            release_digests.append(member["releaseRecord"])
        elif kind == "artifact-checksum":
            data = read_artifact("artifact-checksum", name)
            if canon.bytes_digest(data) != member["digest"]:
                raise BundleError("stored checksum %s does not match config digest"
                                  % name)
            artifact = member["artifact"]
            verify_detached_checksum(
                data, artifact, canon.bytes_digest(sealed_data[artifact]))
        else:
            data = manifest_bytes
            if member["wordingDigest"] != manifest_wording_digest:
                raise BundleError("configured manifest wording digest is stale")
            if canon.bytes_digest(data) != member["digest"]:
                raise BundleError("generated manifest does not match config digest")
        resolved.append((name, data))
    return {
        "members": resolved,
        "releaseRecords": release_digests,
        "manifestApproval": approval["digest"],
    }


def read_zip_members(data):
    """Read and validate an existing bundle's ordered STORE members."""
    if not isinstance(data, bytes):
        raise BundleError("bundle ZIP must be bytes")
    try:
        archive = zipfile.ZipFile(io.BytesIO(data), "r")
    except (OSError, zipfile.BadZipFile) as exc:
        raise BundleError("invalid bundle ZIP: %s" % exc)
    out = []
    seen = set()
    try:
        for info in archive.infolist():
            validate_member_name(info.filename)
            folded = info.filename.casefold()
            if folded in seen:
                raise BundleError("duplicate ZIP member name %r"
                                  % info.filename)
            seen.add(folded)
            if info.is_dir():
                raise BundleError("bundle ZIP may not contain directories")
            if info.compress_type != zipfile.ZIP_STORED:
                raise BundleError("bundle member %r is not STORE"
                                  % info.filename)
            out.append((info.filename, archive.read(info)))
    except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
        raise BundleError("invalid bundle ZIP member: %s" % exc)
    finally:
        archive.close()
    return out


def bundle_record_problems(record, cfg, bundle_digest,
                           bundle_config_digest=None,
                           expected_edition_count=2,
                           current_acceptance_context=None):
    """Return exact-chain defects for a bundle record and current config."""
    validate_bundle_config(cfg, expected_edition_count)
    if not isinstance(record, dict):
        return ["bundle record is not an object"]
    problems = []
    if set(record) != recordprovenance.BUNDLE_RECORD_FIELDS:
        problems.append("bundle record has the wrong fields")
    if record.get("recordVersion") != "2":
        problems.append("bundle record has the wrong version")
    if not authority.is_identified_operator_identity(
            record.get("operator")):
        problems.append("bundle record has no identified operator")
    if record.get("approvalStatus") != "passed":
        problems.append("bundle record approvalStatus is not 'passed'")
    if not authority.is_authoritative_operator_kind(
            record.get("operatorKind")):
        problems.append(
            "bundle record operatorKind is not release-authoritative")
    profile_contract = current_acceptance_context.get(
        "releaseProfileContract") \
        if isinstance(current_acceptance_context, dict) else None
    try:
        expected_profile_fields = release_mod.profile_record_fields(
            profile_contract)
    except release_mod.AcceptanceError as exc:
        problems.append("current bundle release profile is unavailable: %s"
                        % exc)
        expected_profile_fields = None
    if expected_profile_fields is not None:
        for field, expected in expected_profile_fields.items():
            if record.get(field) != expected:
                problems.append(
                    "bundle record %s does not match current release profile"
                    % field)
    if record.get("releaseProfile") != cfg.get("releaseProfile"):
        problems.append(
            "bundle record releaseProfile does not match current config")
    manifest = next(m for m in cfg["members"]
                    if m["kind"] == "bundle-manifest")
    expected_members = [{"name": m["name"], "digest": m["digest"]}
                        for m in cfg["members"]]
    expected_releases = [m["releaseRecord"] for m in cfg["members"]
                         if m["kind"] == "sealed"]
    checks = (
        ("bundle", cfg["name"]),
        ("bundleDigest", bundle_digest),
        ("members", expected_members),
        ("releaseRecords", expected_releases),
        ("manifestWording", manifest["wordingDigest"]),
        ("manifestApproval", cfg["manifestApproval"]),
    )
    problems.extend("bundle record %s does not match current config" % field
                    for field, expected in checks
                    if record.get(field) != expected)
    if bundle_config_digest is not None and \
            record.get("bundleConfigDigest") != bundle_config_digest:
        problems.append("bundle record config digest is stale")
    receipt_subjects = release_mod.bundle_subjects(
        bundle_config_digest, bundle_digest, expected_releases,
        expected_members, cfg.get("manifestApproval"), profile_contract)
    problems.extend(release_mod.acceptance_receipt_problems(
        record.get("acceptanceReceipt"), "bundle",
        current_acceptance_context, receipt_subjects))
    return problems
