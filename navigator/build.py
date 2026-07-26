"""Minimal current-only navigator command boundary."""

from __future__ import annotations

import os
import sys


if __package__ in {None, ""}:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from lib import acceptance, bundlezip, canon, currentstate, gateway
    from lib import release, snapshot
else:
    from .lib import acceptance, bundlezip, canon, currentstate, gateway
    from .lib import release, snapshot


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "navigator", "dist")
COMMANDS = ("preview", "candidate", "release", "bundle", "validate-current")
USAGE = {
    "preview": "python -m navigator preview <edition>",
    "candidate": "python -m navigator candidate <edition>",
    "release": "python -m navigator release <edition>",
    "bundle": "python -m navigator bundle",
    "validate-current": "python -m navigator validate-current",
}


class CommandError(RuntimeError):
    """The requested current navigator operation is invalid."""


def _snapshot():
    try:
        return snapshot.RepositorySnapshot.capture(ROOT, retain_bytes=True)
    except snapshot.SnapshotError as exc:
        raise CommandError("repository snapshot could not be captured") from exc


def _assert_unchanged(before, label):
    try:
        after = snapshot.RepositorySnapshot.capture(ROOT)
    except snapshot.SnapshotError as exc:
        raise CommandError("repository changed during %s" % label) from exc
    changes = before.differences(after)
    if changes:
        raise CommandError(
            "repository changed during %s: %s" % (label, "; ".join(changes)))


def _assert_only_outputs_changed(before, outputs, label):
    """Reject any concurrent change outside this command's exact outputs."""
    allowed = {"navigator/dist/" + release.validate_output_name(name)
               for name in outputs}
    try:
        after = snapshot.RepositorySnapshot.capture(ROOT)
    except snapshot.SnapshotError as exc:
        raise CommandError("repository changed during %s" % label) from exc
    left = before.by_path()
    right = after.by_path()
    changed = set(left) ^ set(right)
    changed.update(
        path for path in set(left) & set(right)
        if (left[path].digest, left[path].mode, left[path].size) !=
        (right[path].digest, right[path].mode, right[path].size))
    unexpected = sorted(changed - allowed)
    if unexpected:
        raise CommandError(
            "repository changed outside %s outputs: %s" %
            (label, unexpected))
    for name, data in outputs.items():
        path = "navigator/dist/" + name
        entry = right.get(path)
        if entry is None or entry.digest != canon.bytes_digest(data) or \
                entry.size != len(data) or entry.mode != 0o644:
            raise CommandError("%s output changed after readback: %s" %
                               (label, name))


def cmd_preview(edition_id):
    frozen = _snapshot()
    inputs = currentstate.verify_structured_source(
        frozen, ("navigator-" + edition_id,))
    unused_model, html_bytes, unused_lock = currentstate.derive(
        edition_id, "preview", frozen,
        inputs["navigator-" + edition_id])
    _assert_unchanged(frozen, "preview")
    return html_bytes


def cmd_candidate(edition_id):
    frozen = _snapshot()
    inputs = currentstate.verify_structured_source(
        frozen, ("navigator-" + edition_id,))
    edition_model, html_bytes, content_lock = currentstate.derive(
        edition_id, "candidate", frozen,
        inputs["navigator-" + edition_id])
    name = release.candidate_name(edition_model.artifact_name)
    _assert_unchanged(frozen, "candidate derivation")
    outputs = {name: html_bytes}
    written = release.write_outputs_atomic(DIST, outputs)
    _assert_only_outputs_changed(frozen, outputs, "candidate")
    return {
        "command": "candidate",
        "commandResultVersion": "2",
        "contentLockDigest": content_lock["lockDigest"],
        "edition": edition_id,
        "outputs": written,
        "status": "generated",
    }


def cmd_release(edition_id):
    frozen = _snapshot()
    inputs = currentstate.verify_structured_source(
        frozen, ("navigator-" + edition_id,))
    edition_model, html_bytes, content_lock = currentstate.derive(
        edition_id, "release", frozen,
        inputs["navigator-" + edition_id])
    candidate = release.candidate_name(edition_model.artifact_name)
    try:
        stored_candidate = frozen.read_bytes("navigator/dist/" + candidate)
    except snapshot.SnapshotError as exc:
        raise CommandError("current candidate is unavailable") from exc
    reproduced = release.fresh_candidate(ROOT, edition_id)
    candidate_digest = release.prove_candidate(
        html_bytes, stored_candidate, reproduced)
    checksum_name = edition_model.artifact_name + ".sha256"
    checksum = release.checksum_text(edition_model.artifact_name, html_bytes)
    _assert_unchanged(frozen, "release proof")
    outputs = {
        edition_model.artifact_name: html_bytes,
        checksum_name: checksum,
    }
    written = release.write_outputs_atomic(DIST, outputs)
    _assert_only_outputs_changed(frozen, outputs, "release")
    return {
        "candidateDigest": candidate_digest,
        "command": "release",
        "commandResultVersion": "2",
        "contentLockDigest": content_lock["lockDigest"],
        "edition": edition_id,
        "outputs": written,
        "status": "sealed",
    }


def cmd_bundle():
    frozen = _snapshot()
    inputs = currentstate.verify_structured_source(
        frozen, ("navigator-na", "navigator-af"))
    states = currentstate._derive_editions(frozen, inputs)
    bundle_state = currentstate.build_bundle_state(frozen, states)
    name = bundle_state["config"]["name"]
    checksum_name = name + ".sha256"
    checksum = release.checksum_text(name, bundle_state["zip"])
    _assert_unchanged(frozen, "bundle derivation")
    outputs = {
        name: bundle_state["zip"],
        checksum_name: checksum,
    }
    written = release.write_outputs_atomic(DIST, outputs)
    _assert_only_outputs_changed(frozen, outputs, "bundle")
    return {
        "command": "bundle",
        "commandResultVersion": "2",
        "members": [member for member, unused_data in bundle_state["members"]],
        "outputs": written,
        "status": "generated",
    }


def cmd_validate_current():
    return currentstate.validate_current_state(run_tests=True)


def _usage():
    return "usage:\n" + "\n".join(
        "  " + USAGE[name] for name in COMMANDS)


def _dispatch(argv):
    if not argv or argv[0] not in COMMANDS:
        raise CommandError(_usage())
    command, arguments = argv[0], argv[1:]
    expected_count = 1 if command in {"preview", "candidate", "release"} else 0
    if len(arguments) != expected_count or any(
            argument.startswith("-") for argument in arguments):
        raise CommandError(USAGE[command])
    if command == "preview":
        return cmd_preview(arguments[0])
    if command == "candidate":
        return cmd_candidate(arguments[0])
    if command == "release":
        return cmd_release(arguments[0])
    if command == "bundle":
        return cmd_bundle()
    return cmd_validate_current()


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        result = _dispatch(argv)
    except (acceptance.AcceptanceError, bundlezip.BundleError, canon.CanonError,
            CommandError, currentstate.CurrentStateError, gateway.GatewayError,
            OSError, release.ReleaseError,
            snapshot.SnapshotError) as exc:
        command = argv[0] if argv else "navigator"
        raise SystemExit("%s refused: %s" % (command, exc)) from exc
    if isinstance(result, bytes):
        sys.stdout.buffer.write(result)
    else:
        sys.stdout.buffer.write(canon.canonical_json(result) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
