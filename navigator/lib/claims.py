"""Claim-set §3 parser — fragment corpus -> claims and limitation units.

Every claim is decomposed into limitation units: its markdown paragraphs —
preamble (u0) plus each clause (TDD §5.2). The census is normative per
edition and asserted exactly by the extraction test (AC-01). Group headings
are captured for the claims-pane grouping (§5.1); a blockquote inside the
claims section is guidance (profile-designated quotable, segmented by
lib.segmenter), never a unit.

Dependency references (``of claim N``) are parsed here for the dual-source
cross-validation of the authored dependency map (§8.1).
"""

import re

from . import canon

CLAIM_HEAD_RE = re.compile(r"^\*\*(\d+)\.\*\*\s+(.*)$", re.S)
DEP_REF_RE = re.compile(r"\bof claims? (\d+)")
H2_RE = re.compile(r"^## (.+)$")
H3_RE = re.compile(r"^### (.+)$")


class ClaimsParseError(ValueError):
    pass


class Unit:
    __slots__ = ("claim", "index", "text", "canonical", "digest")

    def __init__(self, claim, index, text):
        self.claim = claim
        self.index = index
        self.text = text
        self.canonical = canon.canon_prose(text)
        self.digest = canon.text_digest(self.canonical)

    @property
    def id(self):
        return "c%du%d" % (self.claim, self.index)

    @property
    def label(self):
        return "preamble" if self.index == 0 else "limitation %d" % self.index


class Claim:
    __slots__ = ("number", "group", "units", "parsed_refs")

    def __init__(self, number, group):
        self.number = number
        self.group = group
        self.units = []
        self.parsed_refs = []

    @property
    def aggregate_hash(self):
        return canon.composite_digest(
            "aa11393:claim-agg:c1", [u.digest for u in self.units])


def parse_claims(text, claims_heading="Candidate claims"):
    """Parse the §3 claims of one claim-set markdown document."""
    lines = text.split("\n")
    in_section = False
    group = None
    claims = []
    current = None
    para = []

    def flush_para():
        nonlocal para
        joined = " ".join(p.strip() for p in para if p.strip())
        para = []
        if not joined:
            return
        m = CLAIM_HEAD_RE.match(joined)
        if m:
            start_claim(int(m.group(1)), m.group(2))
        elif current is not None:
            current.units.append(Unit(current.number, len(current.units), joined))

    def start_claim(number, headtext):
        nonlocal current
        current = Claim(number, group)
        current.units.append(Unit(number, 0, headtext))
        claims.append(current)

    i = 0
    while i < len(lines):
        line = lines[i]
        m2 = H2_RE.match(line)
        if m2:
            flush_para()
            name = re.sub(r"^\d+\.\s+", "", m2.group(1)).strip()
            if in_section:
                break  # left the claims section
            in_section = name == claims_heading
            current = None
            i += 1
            continue
        if not in_section:
            i += 1
            continue
        m3 = H3_RE.match(line)
        if m3:
            flush_para()
            group = m3.group(1).strip()
            current = None
            i += 1
            continue
        if line.startswith(">"):
            flush_para()
            current = None  # guidance blockquote: not claim text
            while i < len(lines) and lines[i].startswith(">"):
                i += 1
            continue
        if not line.strip():
            flush_para()
            i += 1
            continue
        para.append(line)
        i += 1
    flush_para()

    if not claims:
        raise ClaimsParseError("no claims found under %r" % claims_heading)
    for c in claims:
        full = " ".join(u.text for u in c.units)
        c.parsed_refs = sorted({int(n) for n in DEP_REF_RE.findall(full)})
    numbers = [c.number for c in claims]
    if numbers != list(range(1, len(claims) + 1)):
        raise ClaimsParseError("claim numbering not contiguous: %r" % numbers)
    return claims


def census(claims):
    """(claim count, unit count, {claim: units}) for the census assertion."""
    per = {c.number: len(c.units) for c in claims}
    return len(claims), sum(per.values()), per
