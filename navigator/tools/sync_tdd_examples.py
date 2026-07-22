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


def main():
    with open(TDD, encoding="utf-8") as fh:
        s = fh.read()
    blocks = re.findall(r"```json\n(.*?)```", s, re.S)
    if len(blocks) != 2:
        raise SystemExit("expected exactly 2 json blocks in §8.3, found %d"
                         % len(blocks))
    for block, fxname in zip(blocks, ("na_excerpt.json", "af_excerpt.json")):
        with open(os.path.join(FIX, fxname), encoding="utf-8") as fh:
            fx = json.load(fh)
        synced = sync(json.loads(block), fx)
        s = s.replace(block,
                      json.dumps(synced, indent=2, ensure_ascii=False) + "\n", 1)
    with open(TDD, "w", encoding="utf-8") as fh:
        fh.write(s)
    print("TDD §8.3 examples re-projected from fixtures")


if __name__ == "__main__":
    main()
