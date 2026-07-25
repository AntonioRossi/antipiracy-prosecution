"""Closed structured-source command boundary."""

from __future__ import annotations

import argparse
import os
import sys

from .acceptance import load_registry as load_acceptance_registry, render_table
from .atomic import publish_set
from .control import canonical_json
from .environment import verify_environment
from .errors import StructuredSourceError
from .routers import render_all
from .verify import VerificationContext, run_acceptance

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACCEPTANCE_PATH = "AA11393US-structured-source-markdown_acceptance-criteria.md"
_TABLE_START = "<!-- SSM-AC-TABLE:START -->\n"
_TABLE_END = "<!-- SSM-AC-TABLE:END -->"


def _parser():
    parser = argparse.ArgumentParser(prog="python -m structured_source")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("check", "regenerate"):
        child = commands.add_parser(name)
        child.add_argument("subject_id")
    commands.add_parser("regenerate-controls")
    commands.add_parser("verify-callback")
    commands.add_parser("verify-current")
    return parser


def _regenerate_controls():
    context = VerificationContext(ROOT)
    content_registry = context.registry
    acceptance_registry = load_acceptance_registry(
        ROOT, context.reader.read_absolute)
    outputs = render_all(content_registry)
    acceptance_before = context.reader.read(ACCEPTANCE_PATH)
    try:
        acceptance_text = acceptance_before.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise StructuredSourceError(
            "acceptance contract is not UTF-8") from exc
    if acceptance_text.count(_TABLE_START) != 1 or \
            acceptance_text.count(_TABLE_END) != 1:
        raise StructuredSourceError(
            "acceptance table marker census is not exact")
    prefix, remainder = acceptance_text.split(_TABLE_START, 1)
    unused_region, suffix = remainder.split(_TABLE_END, 1)
    acceptance_after = (
        prefix + _TABLE_START + render_table(acceptance_registry) +
        _TABLE_END + suffix).encode("utf-8")
    outputs[ACCEPTANCE_PATH] = acceptance_after
    expected = {
        path: acceptance_before if path == ACCEPTANCE_PATH else
        context.reader.optional(path)
        for path in outputs
    }
    guards = {
        path: context.reader.read(path)
        for path in tuple(context.reader.read_log)
        if path not in outputs
    }
    publish_set(ROOT, outputs, expected, guards)
    return {
        "commandResultVersion": "1",
        "command": "regenerate-controls",
        "status": "regenerated",
        "outputs": sorted(outputs),
    }


def main(argv=None):
    args = _parser().parse_args(argv)
    verify_environment(ROOT)
    if args.command == "check":
        result = VerificationContext(ROOT).check(args.subject_id)
    elif args.command == "regenerate":
        result = VerificationContext(ROOT).regenerate(args.subject_id)
    elif args.command == "regenerate-controls":
        result = _regenerate_controls()
    elif args.command in {"verify-callback", "verify-current"}:
        result = run_acceptance(ROOT)
    else:  # argparse and the exact command policy make this unreachable.
        raise StructuredSourceError("unsupported command")
    sys.stdout.buffer.write(canonical_json(result))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, StructuredSourceError) as exc:
        raise SystemExit("structured-source command refused: %s" % exc)
