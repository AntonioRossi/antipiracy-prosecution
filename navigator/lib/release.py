"""Release and bundle promotion transactions.

This module performs byte-level promotion work.  The independent acceptance
module owns registry, policy, context, callback, and receipt semantics.
"""

import locale
import platform
import subprocess
import sys

from . import acceptance, canon, gateway, inputlock


def _verify_release_preflight(root, model, derived_bytes, candidate_bytes,
                              content_lock, qa_envelope,
                              release_profile_contract):
    from . import render

    problems = []
    candidate_digest = canon.bytes_digest(candidate_bytes)
    if candidate_bytes != derived_bytes:
        problems.append("candidate bytes differ from the release derivation")
    first_build = render.render(model, mode="candidate")
    second_build = render.render(model, mode="candidate")
    if first_build != derived_bytes or second_build != derived_bytes:
        problems.append("in-process double build is not byte-identical")
    problems.extend(inputlock.exact_set_problems(
        content_lock, model.edition["declaredTransitiveInputs"]))
    profile_problems = acceptance.profile_contract_problems(
        release_profile_contract)
    problems.extend("release profile: %s" % problem
                    for problem in profile_problems)
    manual_qa = release_profile_contract.get("manualQaEvidence") \
        if not profile_problems else None
    if manual_qa == "required":
        qa_record = qa_envelope.get("record") \
            if isinstance(qa_envelope, dict) else None
        if not isinstance(qa_record, dict):
            problems.append("QA authorization is not an object")
        else:
            if qa_record.get("candidateDigest") != candidate_digest:
                problems.append(
                    "QA authorization does not bind candidate bytes")
            if qa_record.get("lockDigest") != content_lock.get("lockDigest"):
                problems.append(
                    "QA authorization does not bind the content lock")
            qa_lock = qa_record.get("qaInputLock")
            if not isinstance(qa_lock, dict) or \
                    qa_lock.get("candidateDigest") != candidate_digest or \
                    qa_lock.get("contentLockDigest") != content_lock.get(
                        "lockDigest"):
                problems.append("QA input lock does not bind release inputs")
    elif manual_qa == "deferred" and qa_envelope is not None:
        problems.append(
            "a profile with deferred observations must not claim a QA "
            "authorization")

    script = """
import sys
sys.path.insert(0, "navigator")
from lib import canon, gateway, model, render
root = %r
edition = %r
edition_path = "navigator/editions/%%s.json" %% edition
boot = gateway.ContentGateway(root)
allow = canon.parse_json(boot.read_text(edition_path))["declaredTransitiveInputs"]
gw = gateway.ContentGateway(root, allowlist=allow)
current = model.EditionModel(gw, edition_path)
data = render.render(current, mode="candidate")
lock = gw.lock()
print(canon.canonical_json({"candidateDigest": canon.bytes_digest(data),
                            "lockDigest": lock["lockDigest"]}).decode("utf-8"))
""" % (root, model.edition["editionId"])
    child = subprocess.run(
        [sys.executable, "-B", "-c", script], cwd=root,
        capture_output=True, text=True, timeout=300)
    if child.returncode != 0:
        problems.append("cross-process build failed: %s" %
                        child.stderr.strip()[-1000:])
    else:
        try:
            child_result = canon.parse_json(child.stdout.strip())
        except (canon.CanonError, TypeError, ValueError) as exc:
            problems.append("cross-process build result is malformed: %s" % exc)
        else:
            if child_result != {
                    "candidateDigest": candidate_digest,
                    "lockDigest": content_lock.get("lockDigest")}:
                problems.append("cross-process build or content lock differs")
    if problems:
        raise acceptance.AcceptanceError(
            "AC-16 release preflight failed: %s" % "; ".join(problems))


def _verify_release_postcondition(output, sealed_name, candidate_bytes,
                                  checksum_bytes):
    from . import bundlezip

    output.verify_written("sealed", sealed_name, candidate_bytes)
    output.verify_written(
        "artifact-checksum", sealed_name + ".sha256", checksum_bytes)
    bundlezip.verify_detached_checksum(
        checksum_bytes, sealed_name, canon.bytes_digest(candidate_bytes))


def _release_callback_context(model, candidate_bytes, content_lock):
    return {
        "kind": "release-preflight",
        "edition": model.edition["editionId"],
        "candidateDigest": canon.bytes_digest(candidate_bytes),
        "contentLockDigest": content_lock["lockDigest"],
    }


def run_release_acceptance_transaction(root, model, derived_bytes,
                                       candidate_bytes, content_lock,
                                       qa_envelope, output,
                                       release_profile=None):
    """Prove, write, read back, and receipt one standalone promotion."""
    edition_ids = (model.edition["editionId"],)
    before = acceptance.acceptance_context(
        root, edition_ids, release_profile)
    callback_ids = acceptance.callback_controls(
        before, "release-preflight")
    acceptance.run_registered_callbacks(
        root, callback_ids, edition_ids, before,
        _release_callback_context(model, candidate_bytes, content_lock))
    _verify_release_preflight(
        root, model, derived_bytes, candidate_bytes, content_lock, qa_envelope,
        before["releaseProfileContract"])
    sealed_name = model.edition["artifactName"]
    checksum_bytes = checksum_text(
        sealed_name, candidate_bytes).encode("utf-8")
    output.write("sealed", sealed_name, candidate_bytes)
    output.write("artifact-checksum", sealed_name + ".sha256", checksum_bytes)
    _verify_release_postcondition(
        output, sealed_name, candidate_bytes, checksum_bytes)
    after = acceptance.acceptance_context(
        root, edition_ids, before["releaseProfile"])
    if after != before:
        raise acceptance.AcceptanceError(
            "acceptance registry, policy, or runner inputs changed during "
            "release")
    if before["releaseProfileContract"]["manualQaEvidence"] == "required":
        qa_record_digest = qa_envelope["digest"]
        qa_input_lock_digest = qa_envelope["record"]["qaInputLock"][
            "lockDigest"]
    else:
        qa_record_digest = None
        qa_input_lock_digest = None
    subjects = acceptance.release_subjects(
        model.edition["editionId"], canon.bytes_digest(candidate_bytes),
        content_lock["lockDigest"], qa_record_digest,
        qa_input_lock_digest, before["releaseProfileContract"])
    return acceptance.make_receipt("release", before, subjects)


def _verify_bundle_postcondition(root, cfg, plan, zip_bytes, checksum_bytes,
                                 manifest_bytes, output):
    from . import bundlezip

    manifest_member = next(
        member for member in cfg["members"]
        if member["kind"] == "bundle-manifest")
    output.verify_written(
        "bundle-manifest", manifest_member["name"], manifest_bytes)
    output.verify_written("bundle", cfg["name"], zip_bytes)
    output.verify_written(
        "bundle-checksum", cfg["name"] + ".sha256", checksum_bytes)
    bundlezip.verify_detached_checksum(
        checksum_bytes, cfg["name"], canon.bytes_digest(zip_bytes))
    if bundlezip.read_zip_members(zip_bytes) != plan["members"]:
        raise acceptance.AcceptanceError(
            "AC-20 bundle members differ from resolved plan")
    if bundlezip.build_zip(
            plan["members"], cfg["declaredTimestamp"]) != zip_bytes:
        raise acceptance.AcceptanceError(
            "AC-20 deterministic ZIP rebuild differs")
    expected_members = [(member["name"], member["digest"])
                        for member in cfg["members"]]
    actual_members = [(name, canon.bytes_digest(data))
                      for name, data in plan["members"]]
    if actual_members != expected_members:
        raise acceptance.AcceptanceError(
            "AC-20 configured member subjects differ")
    expected_releases = [member["releaseRecord"] for member in cfg["members"]
                         if member["kind"] == "sealed"]
    if plan["releaseRecords"] != expected_releases:
        raise acceptance.AcceptanceError(
            "AC-20 configured release subjects differ")
    golden = canon.parse_json(gateway.ContentGateway(root).read_text(
        "navigator/tests/fixtures/golden_bundle.json"))
    golden_bytes = bundlezip.build_zip(
        [(name, data.encode("ascii")) for name, data in golden["members"]],
        golden["declaredTimestamp"])
    if golden_bytes.hex() != golden["hex"] or \
            canon.bytes_digest(golden_bytes) != golden["sha256"]:
        raise acceptance.AcceptanceError(
            "AC-20 golden ZIP conformance failed")


def _bundle_callback_context(cfg, bundle_config_digest, plan, zip_bytes,
                             checksum_bytes, manifest_bytes, output):
    return {
        "kind": "bundle-postcondition",
        "outputRoot": output.root,
        "config": cfg,
        "bundleConfigDigest": bundle_config_digest,
        "bundleDigest": canon.bytes_digest(zip_bytes),
        "bundleChecksumDigest": canon.bytes_digest(checksum_bytes),
        "manifestDigest": canon.bytes_digest(manifest_bytes),
        "plannedMembers": [
            {"name": name, "digest": canon.bytes_digest(data)}
            for name, data in plan["members"]
        ],
        "releaseRecords": list(plan["releaseRecords"]),
        "manifestApproval": plan["manifestApproval"],
        "chain": plan["acceptanceChain"],
    }


def run_bundle_acceptance_transaction(root, cfg, bundle_config_digest, plan,
                                      zip_bytes, checksum_bytes,
                                      manifest_bytes, output):
    """Prove, write, read back, and receipt one bundle promotion."""
    if not isinstance(plan, dict) or \
            not isinstance(plan.get("acceptanceChain"), dict):
        raise acceptance.AcceptanceError(
            "AC-20 resolved acceptance chain context is unavailable")
    runner_editions = cfg.get("editions") if isinstance(cfg, dict) else None
    release_profile = cfg.get("releaseProfile") \
        if isinstance(cfg, dict) else None
    if not isinstance(release_profile, str) or not release_profile:
        raise acceptance.AcceptanceError(
            "AC-20 bundle config has no explicit releaseProfile")
    before = acceptance.acceptance_context(
        root, runner_editions, release_profile)
    manifest_member = next(
        member for member in cfg["members"]
        if member["kind"] == "bundle-manifest")
    output.write("bundle-manifest", manifest_member["name"], manifest_bytes)
    output.write("bundle", cfg["name"], zip_bytes)
    output.write("bundle-checksum", cfg["name"] + ".sha256", checksum_bytes)
    _verify_bundle_postcondition(
        root, cfg, plan, zip_bytes, checksum_bytes, manifest_bytes, output)
    callback_ids = acceptance.callback_controls(
        before, "bundle-postcondition")
    acceptance.run_registered_callbacks(
        root, callback_ids, runner_editions, before,
        _bundle_callback_context(
            cfg, bundle_config_digest, plan, zip_bytes, checksum_bytes,
            manifest_bytes, output))
    after = acceptance.acceptance_context(
        root, runner_editions, release_profile)
    if after != before:
        raise acceptance.AcceptanceError(
            "acceptance registry, policy, or runner inputs changed during "
            "bundle")
    members = [{"name": name, "digest": canon.bytes_digest(data)}
               for name, data in plan["members"]]
    subjects = acceptance.bundle_subjects(
        bundle_config_digest, canon.bytes_digest(zip_bytes),
        plan["releaseRecords"], members, plan["manifestApproval"],
        before["releaseProfileContract"])
    return acceptance.make_receipt("bundle", before, subjects)


def reproduction_diagnostics():
    """Non-normative runtime diagnostics excluded from content locks."""
    return {
        "interpreter": sys.version.split()[0],
        "platform": platform.platform(),
        "locale": ".".join(str(item) for item in locale.getlocale() if item)
                  or "C",
        "unicodedata": __import__("unicodedata").unidata_version,
    }


def verify_envelope(qa_record, candidate_digest, lock_digest, attestations,
                    side_digests=None):
    problems = []
    record = qa_record["record"]
    if record.get("candidateDigest") != candidate_digest:
        problems.append(
            "QA record authorizes candidate %s, not %s" %
            (record.get("candidateDigest"), candidate_digest))
    if record.get("lockDigest") != lock_digest:
        problems.append("QA record lock digest does not match this build")
    referenced = set(record.get("attestations", []))
    present = {item["digest"]: item for item in attestations}
    for digest in referenced - set(present):
        problems.append("attestation %s referenced by QA record is missing" %
                        digest)
    if side_digests is not None:
        for digest in sorted(referenced & set(present)):
            for problem in attestation_current(present[digest], side_digests):
                problems.append(
                    "referenced attestation %s is not current: %s" %
                    (digest, problem))
    return problems


def attestation_current(attestation, side_digests):
    problems = []
    for side, digest in attestation["record"].get("sides", {}).items():
        current = side_digests.get(side)
        if current is None:
            problems.append("attestation side %r has no current digest" % side)
        elif current != digest:
            problems.append(
                "attestation side %r stale: recorded %s, current %s" %
                (side, digest, current))
    return problems


def checksum_text(name, data):
    return "%s  %s\n" % (canon.bytes_digest(data), name)
