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
from .grammar import CONTENT_XSD_PATH, parse_content_grammar, render_content_xsd
from .parser import (PROJECTION_PROFILE_PATH, XML_PROFILE_PATH,
                     load_parser_controls)
from .profiles import parse_projection_profile, parse_xml_profiles
from .routers import render_all
from .verify import VerificationContext

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMANDS = ("check", "regenerate", "regenerate-controls")


def _parser():
    parser = argparse.ArgumentParser(prog="python -m structured_source")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("check", "regenerate"):
        child = commands.add_parser(name)
        child.add_argument("subject_id")
    commands.add_parser("regenerate-controls")
    return parser


def _regenerate_controls():
    context = VerificationContext(ROOT)
    content_registry = context.registry
    acceptance_registries = load_registries(
        ROOT, context.reader.read_absolute)
    outputs = render_all(content_registry)
    projection = parse_projection_profile(
        context.reader.read(PROJECTION_PROFILE_PATH))
    xml_profiles = parse_xml_profiles(
        context.reader.read(XML_PROFILE_PATH), projection)
    content_grammar = parse_content_grammar(
        xml_profiles["contentDocuments"][
            "pdf-evidence-transcription-v1"]["contentGrammar"])
    outputs[CONTENT_XSD_PATH] = render_content_xsd(content_grammar)
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

    def read_candidate(path):
        if path in outputs:
            return outputs[path]
        return context.reader.read(path)

    candidate_controls = load_parser_controls(read_candidate)
    if candidate_controls.content_grammar.production_paths != \
            content_grammar.production_paths:
        raise StructuredSourceError(
            "candidate parser controls differ from the authoritative grammar")
    del candidate_controls

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
    def validate_readback():
        def read(path):
            with open(os.path.join(ROOT, *path.split("/")), "rb") as handle:
                return handle.read()
        if any(read(path) != expected_bytes
               for path, expected_bytes in outputs.items()):
            raise StructuredSourceError(
                "regenerated parser controls failed exact readback")
        load_parser_controls(read)

    publish_set(
        ROOT, outputs, expected, guards, postcondition=validate_readback)
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
    else:  # The exact parser surface makes this unreachable.
        raise StructuredSourceError("unsupported command")
    sys.stdout.buffer.write(canonical_json(result))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, StructuredSourceError) as exc:
        raise SystemExit("structured-source command refused: %s" % exc)
