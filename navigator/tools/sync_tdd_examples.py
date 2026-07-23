#!/usr/bin/env python3
"""Re-project the TDD §8.3 example blocks from the regenerated fixtures
(authoring tool, class d). The examples are abridged renderings — this tool
keeps their shape (field selection, array truncation) and replaces every
value with the current fixture value, re-abbreviating digests. Run after
tools/make_fixtures.py whenever endpoint or review digests move; the AC-06
comparison test then holds by construction.
"""

import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
NAV = os.path.join(ROOT, "navigator")
sys.path.insert(0, NAV)

from lib import canon  # noqa: E402

TDD = os.path.join(
    ROOT, "AA11393US-claims-navigator_technical-description_DRAFT.md")
FIX = os.path.join(ROOT, "navigator", "tests", "fixtures")
DIGEST_RE = re.compile(r"^sha256/c1:[0-9a-f]{64}$")


def sync(doc, real):
    if isinstance(doc, str):
        if doc.endswith("…") and isinstance(real, str) and DIGEST_RE.match(real):
            return real[:14] + "…"
        return real if isinstance(real, str) else doc
    if isinstance(doc, dict):
        return {k: sync(v, real[k]) for k, v in doc.items()}
    if isinstance(doc, list):
        return [sync(v, real[i]) for i, v in enumerate(doc)]
    return real


def _abbreviate(value):
    """Return a reviewable documentation projection with short digests."""
    if isinstance(value, str) and DIGEST_RE.match(value):
        return value[:14] + "…"
    if isinstance(value, dict):
        return {key: _abbreviate(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_abbreviate(item) for item in value]
    return value


def relation_example(fixture):
    """Project a compact example from a current relation excerpt.

    Owners and optional fields may legitimately disappear during a structural
    claim migration.  Rebuilding the small example from the selected fixture
    avoids retaining an orphan owner merely because an older documentation
    block happened to name it.
    """
    projected = {
        "binding": fixture["binding"],
        "claimGates": {
            key: values[:1]
            for key, values in fixture["claimGates"].items()
        },
        "fragments": {},
        "dispositions": fixture["dispositions"][:2],
    }
    for key, fragment in fixture["fragments"].items():
        owner = dict(fragment)
        if "targets" in owner:
            owner["targets"] = owner["targets"][:2]
        if "phrases" in owner:
            owner["phrases"] = owner["phrases"][:1]
        projected["fragments"][key] = owner
    return _abbreviate(projected)


def main():
    with open(TDD, encoding="utf-8") as fh:
        s = fh.read()
    blocks = re.findall(r"```json\n(.*?)```", s, re.S)
    if len(blocks) != 2:
        raise SystemExit("expected exactly 2 json blocks in §8.3, found %d"
                         % len(blocks))
    for block, fxname in zip(blocks, ("na_excerpt.json", "af_excerpt.json")):
        with open(os.path.join(FIX, fxname), "rb") as fh:
            fx = canon.parse_json(fh.read())
        parsed = canon.parse_json(block)
        synced = relation_example(fx) if isinstance(fx, dict) and \
            set(("binding", "claimGates", "fragments", "dispositions")) \
            <= set(fx) else sync(parsed, fx)
        s = s.replace(block,
                      json.dumps(synced, indent=2, ensure_ascii=False) + "\n", 1)
    with open(TDD, "w", encoding="utf-8") as fh:
        fh.write(s)
    print("TDD §8.3 examples re-projected from fixtures")


if __name__ == "__main__":
    main()
