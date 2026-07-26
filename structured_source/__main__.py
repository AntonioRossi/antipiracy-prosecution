"""Closed structured-source command boundary."""

from __future__ import annotations

import argparse
import os
import sys

from .acceptance import CONTRACTS, load_registries, render_table
from .atomic import publish_set
from .control import canonical_json
from .environment import verify_environment
from .errors import StructuredSourceError
from .routers import render_all
from .verify import VerificationContext, run_acceptance

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMANDS = ("check", "regenerate", "regenerate-controls", "verify-current")


def _parser():
    parser = argparse.ArgumentParser(prog="python -m structured_source")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in COMMANDS[:2]:
        child = commands.add_parser(name)
        child.add_argument("subject_id")
    for name in COMMANDS[2:]:
        commands.add_parser(name)
    return parser


def _regenerate_controls():
    context = VerificationContext(ROOT)
    content_registry = context.registry
    acceptance_registries = load_registries(
        ROOT, context.reader.read_absolute)
    outputs = render_all(content_registry)
    acceptance_before = {}
    for contract, registry in zip(CONTRACTS, acceptance_registries):
        path = contract["contractPath"]
        before = context.reader.read(path)
        acceptance_before[path] = before
        try:
            text = before.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise StructuredSourceError(
                "%s acceptance contract is not UTF-8" %
                contract["domain"]) from exc
        start = contract["tableStart"]
        end = contract["tableEnd"]
        if text.count(start) != 1 or text.count(end) != 1:
            raise StructuredSourceError(
                "%s acceptance table marker census is not exact" %
                contract["domain"])
        prefix, remainder = text.split(start, 1)
        unused_region, suffix = remainder.split(end, 1)
        outputs[path] = (
            prefix + start + render_table(registry) + end + suffix
        ).encode("utf-8")
    expected = {
        path: (acceptance_before[path] if path in acceptance_before else
               context.reader.optional(path))
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
    elif args.command == "verify-current":
        result = run_acceptance(ROOT)
    else:  # The exact parser surface makes this unreachable.
        raise StructuredSourceError("unsupported command")
    sys.stdout.buffer.write(canonical_json(result))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, StructuredSourceError) as exc:
        raise SystemExit("structured-source command refused: %s" % exc)
