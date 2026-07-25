"""Verified structured-source command boundary."""

from __future__ import annotations

import argparse
import os
import sys

from .approvals import append_record, make_record, resolve_current
from .atomic import publish_set
from .control import canonical_json
from .environment import verify_environment
from .errors import StructuredSourceError
from .exporter import publish_export
from .registry import load_registry
from .verify import (VerificationContext, render_census,
                     run_callback_receipt)
from navigator.lib import snapshot

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _package(registry, subject_id):
    matches = [item for item in registry["documents"] + registry["relationSets"]
               if item.get("documentId", item.get("relationSetId")) == subject_id]
    if len(matches) != 1:
        raise StructuredSourceError("subject identity does not resolve exactly")
    return matches[0]


def _snapshot_callback_receipt():
    try:
        initial = snapshot.RepositorySnapshot.capture(ROOT, retain_bytes=True)
        receipt = run_callback_receipt(
            ROOT, byte_source=initial.byte_source(),
            repository_snapshot=initial, fresh_process=True)
        final = snapshot.RepositorySnapshot.capture(ROOT)
    except snapshot.SnapshotError as exc:
        raise StructuredSourceError(
            "repository snapshot verification failed: %s" % exc) from exc
    differences = initial.differences(final)
    if differences:
        raise StructuredSourceError(
            "repository changed during callback verification: %s" %
            "; ".join(differences))
    return receipt


def _parser():
    parser = argparse.ArgumentParser(prog="python -m structured_source")
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("check-source", "compare", "resolve-approvals"):
        child = commands.add_parser(command)
        child.add_argument("subject_id")
    render = commands.add_parser("render")
    render.add_argument("subject_id")
    render.add_argument("--check-only", action="store_true")
    export = commands.add_parser("export")
    export.add_argument("consumer_id")
    approve = commands.add_parser("approve")
    approve.add_argument("subject_id")
    approve.add_argument("--approval-type", required=True)
    approve.add_argument("--reviewer", required=True)
    approve.add_argument("--role", required=True)
    approve.add_argument("--reviewed-at", required=True)
    approve.add_argument("--projection-approval-digest")
    approve.add_argument("--confirmed-exact-current", action="store_true", required=True)
    commands.add_parser("render-census")
    commands.add_parser("verify-callback")
    commands.add_parser("verify-current")
    return parser


def main(argv=None):
    args = _parser().parse_args(argv)
    if args.command in {"verify-callback", "verify-current"}:
        sys.stdout.buffer.write(canonical_json(_snapshot_callback_receipt()))
        return 0
    verify_environment()
    if args.command == "render-census":
        sys.stdout.buffer.write(canonical_json(render_census(ROOT)))
        return 0
    registry = load_registry(ROOT)
    if args.command in {"check-source", "compare", "render"}:
        context = VerificationContext(ROOT, fresh_process=False)
        package = _package(registry, args.subject_id)
        projection = context._render_package(args.subject_id)
        result = {
            "commandResultVersion": "1", "subjectId": args.subject_id,
            "sourceDigest": context.artifacts[args.subject_id].semantic_digest,
            "markdownDigest": projection.markdown_digest,
            "coverageDigest": projection.coverage_digest,
        }
        if package["markdownDigest"] != projection.markdown_digest or \
                package["coverageDigest"] != projection.coverage_digest:
            raise StructuredSourceError(
                "registry output digests do not authorize this generated set")
        markdown_path = context.file_path(package["markdownFile"])
        coverage_path = context.file_path(package["coverageFile"])
        if args.command in {"compare", "render"} and \
                (args.command != "render" or args.check_only):
            if context.reader.read(markdown_path) != projection.markdown or \
                    context.reader.read(coverage_path) != projection.coverage:
                raise StructuredSourceError("committed generated set is stale")
        if args.command == "render" and not args.check_only:
            before = {}
            for path in (markdown_path, coverage_path):
                absolute = context.reader.absolute(path)
                if os.path.isfile(absolute):
                    with open(absolute, "rb") as handle:
                        before[path] = handle.read()
                else:
                    before[path] = None
            publish_set(
                ROOT,
                {markdown_path: projection.markdown,
                 coverage_path: projection.coverage},
                before)
        sys.stdout.buffer.write(canonical_json(result))
        return 0
    if args.command == "resolve-approvals":
        package = _package(registry, args.subject_id)
        sys.stdout.buffer.write(canonical_json({
            "resolutionVersion": "1", "subjectId": args.subject_id,
            "approvals": resolve_current(ROOT, registry, package),
        }))
        return 0
    if args.command == "approve":
        package = _package(registry, args.subject_id)
        record = make_record(
            ROOT, registry, package, args.approval_type, args.reviewer,
            args.role, args.reviewed_at, args.projection_approval_digest)
        digest = append_record(ROOT, record)
        sys.stdout.buffer.write(canonical_json({
            "approvalAppendVersion": "1", "subjectId": args.subject_id,
            "approvalType": args.approval_type, "digest": digest,
        }))
        return 0
    if args.command == "export":
        digest = publish_export(ROOT, registry, args.consumer_id)
        sys.stdout.buffer.write(canonical_json({
            "exportResultVersion": "1", "consumerId": args.consumer_id,
            "digest": digest,
        }))
        return 0
    raise StructuredSourceError("unsupported command")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, StructuredSourceError) as exc:
        raise SystemExit("structured-source command refused: %s" % exc)
