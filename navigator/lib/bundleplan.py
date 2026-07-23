"""Read-only planning for refreshing a pinned delivery-bundle config.

The bundle config is a promotion allow-list, not a discovery mechanism.  This
module produces a proposed replacement from independently derived current
release bindings and already-existing verification evidence.  It never writes
artifacts, records, approvals, or the config itself.
"""

import copy
from . import authority, bundlezip, canon, recordresolver


_CURRENT_BINDING_FIELDS = frozenset((
    "sealed", "sealedDigest", "lockDigest", "declaredReleaseTimestamp",
))


def _require_exact_context(mapping, editions, label):
    if not isinstance(mapping, dict) or set(mapping) != set(editions):
        raise bundlezip.BundleError(
            "%s must cover exactly the configured editions" % label)


def _validate_current_binding(edition, binding, sealed_name):
    label = "current release binding for edition %s" % edition
    if not isinstance(binding, dict) or set(binding) != \
            _CURRENT_BINDING_FIELDS:
        raise bundlezip.BundleError(
            "%s fields must be exactly %s"
            % (label, sorted(_CURRENT_BINDING_FIELDS)))
    if binding["sealed"] != sealed_name:
        raise bundlezip.BundleError(
            "%s names %r, but the config names %r"
            % (label, binding["sealed"], sealed_name))
    for field in ("sealedDigest", "lockDigest"):
        try:
            canon.parse_digest(binding[field])
        except (canon.CanonError, TypeError) as exc:
            raise bundlezip.BundleError(
                "%s.%s is not a canonical digest: %s"
                % (label, field, exc))
    bundlezip.parse_utc_second(
        binding["declaredReleaseTimestamp"],
        "%s.declaredReleaseTimestamp" % label)


def _canonical_envelope(records, envelope, kind, label):
    """Resolve *envelope* through the collection's exact digest index."""
    if not isinstance(envelope, dict):
        raise bundlezip.BundleError("%s envelope is not an object" % label)
    digest = envelope.get("digest")
    return bundlezip._record_by_digest(  # same-package validation primitive
        records, digest, label, kind)


def _choose_preferred(candidates, label, rejections):
    """Choose human, otherwise model, with digest as the final tie-break."""
    by_digest = {}
    for candidate in candidates:
        digest = candidate["digest"]
        if digest in by_digest:
            raise bundlezip.BundleError(
                "%s evidence contains duplicate digest %s" % (label, digest))
        by_digest[digest] = candidate
    if not by_digest:
        detail = "; ".join(rejections)
        suffix = ": %s" % detail if detail else ""
        raise bundlezip.BundleError("no eligible %s%s" % (label, suffix))

    def preference(envelope):
        record = envelope.get("record", {})
        kind = record.get("operatorKind") \
            if isinstance(record, dict) else None
        if not authority.is_authoritative_operator_kind(kind):
            raise bundlezip.BundleError(
                "%s contains non-authoritative eligible evidence" % label)
        return (0 if kind == "human" else 1, envelope["digest"])

    return min(by_digest.values(), key=preference)


def _read_bytes(read_artifact, kind, name):
    data = read_artifact(kind, name)
    if not isinstance(data, bytes):
        raise bundlezip.BundleError(
            "%s artifact %s was not read as bytes" % (kind, name))
    return data


def _manifest_approval_candidates(attestations, wording_digest,
                                  approval_evidence_problems):
    """Resolve current authorized manifest approvals from the collection."""
    if not isinstance(attestations, list):
        raise bundlezip.BundleError("attestation collection is not a list")

    def authorization_problems(envelope):
        try:
            resolved = _canonical_envelope(
                attestations, envelope, "attestation", "manifest approval")
        except (bundlezip.BundleError, KeyError, TypeError,
                ValueError) as exc:
            return ["%s is malformed: %s" % (envelope.get("digest"), exc)]
        return list(bundlezip._attestation_record_problems(
            resolved["record"], None, approval_evidence_problems))

    context = recordresolver.AttestationContext(
        required_type="manifest-approval", expected_edition=None,
        check_scope=True, expected_sides=frozenset(("manifestWording",)),
        side_digests={"manifestWording": wording_digest},
        authorization_problems=authorization_problems)
    resolution = recordresolver.classify("attestation", attestations, context)
    rejected = [
        "%s is malformed: %s" % (item.digest, "; ".join(item.problems))
        for item in resolution.invalid_records
    ]
    rejected.extend(
        "%s: %s" % (item.digest, "; ".join(item.problems))
        for item in resolution.rejected_authorizations)
    return list(resolution.current_authorizations), rejected


def propose_bundle_config(
        cfg, release_records, qa_records, attestations, read_artifact,
        manifest_bytes, manifest_wording_digest,
        approval_evidence_problems, required_attestations_by_edition,
        current_sides_by_edition, current_release_bindings_by_edition,
        acceptance_context_by_edition, qa_authorization_context_by_edition,
        expected_edition_count=2):
    """Return a fully verified refreshed config without writing anything.

    ``current_release_bindings_by_edition`` is independently derived from the
    current candidate build and content lock.  Each value has exactly
    ``sealed``, ``sealedDigest``, ``lockDigest``, and
    ``declaredReleaseTimestamp``.  This independent input is necessary: a
    self-consistent old QA/release chain cannot prove that its content lock or
    candidate bytes are current.

    ``qa_authorization_context_by_edition`` likewise comes from current live
    edition resources.  Its exact QA input lock (including the selected
    registry read) and support-matrix approver must match the QA record; a
    rehashed historical record is not a currency proof.

    If several current records are eligible, a valid human approval is
    selected ahead of a valid model approval; records of the same kind are
    ordered by digest.  This is independent of collection order and any stale
    or lower-precedence existing config pin.
    """
    bundlezip.validate_bundle_config(cfg, expected_edition_count)
    editions = cfg["editions"]
    _require_exact_context(
        required_attestations_by_edition, editions,
        "required-attestation policy")
    _require_exact_context(
        current_sides_by_edition, editions, "current attestation sides")
    _require_exact_context(
        current_release_bindings_by_edition, editions,
        "current release bindings")
    _require_exact_context(
        acceptance_context_by_edition, editions,
        "current acceptance receipt contexts")
    _require_exact_context(
        qa_authorization_context_by_edition, editions,
        "current QA authorization contexts")
    if not isinstance(release_records, list):
        raise bundlezip.BundleError("release-record collection is not a list")
    if not isinstance(qa_records, list):
        raise bundlezip.BundleError("QA-record collection is not a list")
    if not callable(read_artifact):
        raise bundlezip.BundleError("artifact reader is not callable")
    if not callable(approval_evidence_problems):
        raise bundlezip.BundleError(
            "approval-evidence validator is not callable")
    if not isinstance(manifest_bytes, bytes):
        raise bundlezip.BundleError("generated manifest must be bytes")
    try:
        manifest_text = manifest_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise bundlezip.BundleError("generated manifest is not UTF-8: %s" % exc)
    actual_wording_digest = canon.text_digest(canon.canon_prose(manifest_text))
    if actual_wording_digest != manifest_wording_digest:
        raise bundlezip.BundleError(
            "generated manifest bytes do not derive the supplied wording "
            "digest")

    proposed = copy.deepcopy(cfg)
    members_by_edition = {
        member["edition"]: member for member in proposed["members"]
        if member["kind"] == "sealed"
    }
    checksum_by_artifact = {
        member["artifact"]: member for member in proposed["members"]
        if member["kind"] == "artifact-checksum"
    }
    artifact_snapshot = {}

    for edition in editions:
        sealed_member = members_by_edition[edition]
        sealed_name = sealed_member["name"]
        checksum_member = checksum_by_artifact[sealed_name]
        binding = current_release_bindings_by_edition[edition]
        _validate_current_binding(edition, binding, sealed_name)

        sealed_bytes = _read_bytes(read_artifact, "sealed", sealed_name)
        checksum_bytes = _read_bytes(
            read_artifact, "artifact-checksum", checksum_member["name"])
        sealed_digest = canon.bytes_digest(sealed_bytes)
        if sealed_digest != binding["sealedDigest"]:
            raise bundlezip.BundleError(
                "stored sealed artifact for edition %s is not the current "
                "candidate bytes" % edition)
        bundlezip.verify_detached_checksum(
            checksum_bytes, sealed_name, sealed_digest)
        artifact_snapshot[("sealed", sealed_name)] = sealed_bytes
        artifact_snapshot[("artifact-checksum", checksum_member["name"])] = \
            checksum_bytes

        release_context = recordresolver.ReleaseRecordContext(
            edition_id=edition, sealed=binding["sealed"],
            sealed_digest=binding["sealedDigest"],
            lock_digest=binding["lockDigest"],
            declared_release_timestamp=binding["declaredReleaseTimestamp"],
            release_profile=cfg["releaseProfile"],
            authorization_problems=lambda envelope:
                bundlezip.release_chain_problems(
                    envelope, qa_records, attestations,
                    required_attestations_by_edition[edition],
                    current_sides_by_edition[edition],
                    approval_evidence_problems,
                    acceptance_context_by_edition[edition],
                    qa_authorization_context_by_edition[edition]))
        resolution = recordresolver.classify(
            "release-record", release_records, release_context)
        rejected = [
            "%s is malformed: %s" % (item.digest, "; ".join(item.problems))
            for item in resolution.invalid_records
        ]
        rejected.extend(
            "%s: %s" % (item.digest, "; ".join(item.problems))
            for item in resolution.rejected_authorizations)
        selected = _choose_preferred(
            list(resolution.current_authorizations),
            "current fully authorized release for edition %s" % edition,
            rejected)
        sealed_member["digest"] = sealed_digest
        sealed_member["releaseRecord"] = selected["digest"]
        checksum_member["digest"] = canon.bytes_digest(checksum_bytes)

    manifest_member = next(
        member for member in proposed["members"]
        if member["kind"] == "bundle-manifest")
    manifest_member["digest"] = canon.bytes_digest(manifest_bytes)
    manifest_member["wordingDigest"] = manifest_wording_digest
    approvals, rejected_approvals = _manifest_approval_candidates(
        attestations, manifest_wording_digest, approval_evidence_problems)
    selected_approval = _choose_preferred(
        approvals, "current authorized operator manifest approval",
        rejected_approvals)
    proposed["manifestApproval"] = selected_approval["digest"]

    # Reuse the same resolver as bundle promotion against the exact bytes read
    # above.  This closes gaps between candidate discovery and final config
    # semantics, without a second mutable artifact-store read.
    bundlezip.resolve_bundle_members(
        proposed, release_records, qa_records, attestations,
        lambda kind, name: artifact_snapshot[(kind, name)],
        manifest_bytes, manifest_wording_digest, approval_evidence_problems,
        required_attestations_by_edition, current_sides_by_edition,
        expected_edition_count=expected_edition_count,
        acceptance_context_by_edition=acceptance_context_by_edition,
        qa_authorization_context_by_edition=
            qa_authorization_context_by_edition)
    return proposed
