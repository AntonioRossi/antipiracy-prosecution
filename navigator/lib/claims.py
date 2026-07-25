"""Typed claim units decoded from the registered authored-XML Pandoc AST."""

from __future__ import annotations

from dataclasses import dataclass
import re
from types import MappingProxyType

from . import canon

C = "{urn:aa11393:ssp:content:1}"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
_CLAIM = re.compile(r"claim-([1-9][0-9]*)\Z")
_LIMITATION = re.compile(r"claim-([1-9][0-9]*)-limitation-([1-9][0-9]*)\Z")
_REFERENCE = re.compile(r"\bclaims?\s+([1-9][0-9]*)\b", re.IGNORECASE)
_UNSUPPORTED_REFERENCE = re.compile(
    r"\bclaims\s+[1-9]|"
    r"\bclaim\s+[1-9][0-9]*\s+(?:and|or|through|to)\s+[1-9]|"
    r"\bclaim\s+[1-9][0-9]*\s*[-–]\s*[1-9]|"
    r"\bclaim\s+[1-9][0-9]*\s*,\s*[1-9]",
    re.IGNORECASE,
)
_ANCHOR_OPEN = re.compile(r'<a id="(ssp-[a-z][a-z0-9-]*)">\Z')


class ClaimsParseError(ValueError):
    pass


def dependency_references(text):
    """Parse the sole current singular ``claim N`` dependency grammar."""
    if _UNSUPPORTED_REFERENCE.search(text):
        raise ClaimsParseError(
            "plural, conjunctive, list, or range claim references are unsupported")
    return tuple(sorted({int(value) for value in _REFERENCE.findall(text)}))


@dataclass(frozen=True, slots=True)
class ClaimUnit:
    fragment_id: str
    claim_number: int
    unit_kind: str
    unit_index: int
    text: str
    text_digest: str
    content_digest: str

    @property
    def id(self):
        return self.fragment_id

    @property
    def claim(self):
        return self.claim_number

    @property
    def index(self):
        return self.unit_index

    @property
    def label(self):
        return ("preamble" if self.unit_kind == "preamble" else
                "limitation %d" % self.unit_index)


@dataclass(frozen=True, slots=True)
class Claim:
    number: int
    group: str
    units: tuple[ClaimUnit, ...]
    dependencies: tuple[int, ...]
    fragment_id: str
    content_digest: str

    @property
    def text(self):
        return " ".join(unit.text for unit in self.units)


@dataclass(frozen=True, slots=True)
class ClaimSet:
    claims: tuple[Claim, ...]
    by_number: object
    units_by_fragment: object
    groups: tuple[tuple[str, tuple[int, ...]], ...]


def _value(element):
    local = element.tag.rsplit("}", 1)[-1]
    if local == "null":
        return None
    if local == "boolean":
        return element.text in {"1", "true"}
    if local == "integer":
        return int(element.text)
    if local == "number":
        return float(element.text)
    if local == "string":
        return element.text or ""
    if local == "array":
        return [_value(child) for child in element]
    if local == "node":
        children = list(element)
        if len(children) > 1:
            raise ClaimsParseError("Pandoc node has more than one payload")
        node = {"t": element.get("constructor")}
        if children:
            node["c"] = _value(children[0])
        return node
    raise ClaimsParseError("unknown authored Pandoc value %r" % local)


def decode_pandoc(authored_root) -> tuple[dict, ...]:
    pandoc = authored_root.find(C + "pandoc")
    if pandoc is None or pandoc.get("profile") != "gfm-v1" or \
            pandoc.get("apiVersion") != "1.23.1":
        raise ClaimsParseError("authored XML has no current Pandoc payload")
    blocks = []
    for element in pandoc.findall(C + "block"):
        children = list(element)
        if len(children) > 1:
            raise ClaimsParseError("Pandoc block has more than one payload")
        block = {"t": element.get("constructor")}
        if children:
            block["c"] = _value(children[0])
        blocks.append(block)
    if not blocks:
        raise ClaimsParseError("authored XML has no Pandoc blocks")
    return tuple(blocks)


def _raw_anchor(node):
    if not isinstance(node, dict) or node.get("t") != "RawInline":
        return None
    content = node.get("c")
    if not isinstance(content, list) or len(content) != 2 or \
            content[0] != "html" or not isinstance(content[1], str):
        raise ClaimsParseError("malformed RawInline in authored claim XML")
    if content[1] == "</a>":
        return "close"
    match = _ANCHOR_OPEN.fullmatch(content[1])
    if match is None:
        raise ClaimsParseError("non-anchor raw inline in authored claim XML")
    return match.group(1)[4:]


def _events(value):
    """Yield semantic text and exact stable-anchor events in source order."""
    if isinstance(value, list):
        index = 0
        while index < len(value):
            anchor = _raw_anchor(value[index])
            if anchor is None:
                yield from _events(value[index])
                index += 1
                continue
            if anchor == "close" or index + 1 >= len(value) or \
                    _raw_anchor(value[index + 1]) != "close":
                raise ClaimsParseError("stable anchors are not exact adjacent pairs")
            yield "anchor", anchor
            index += 2
        return
    if not isinstance(value, dict):
        return
    constructor = value.get("t")
    content = value.get("c")
    if constructor == "Str":
        yield "text", content
    elif constructor in {"Space", "SoftBreak", "LineBreak"}:
        yield "text", " "
    elif constructor in {"Code", "Math"}:
        yield "text", content[1]
    elif constructor in {"Link", "Image"}:
        yield from _events(content[1])
    elif constructor == "Header":
        yield from _events(content[2])
    elif "c" in value:
        yield from _events(content)


def _block_text(block) -> str:
    return canon.canon_prose("".join(
        value for kind, value in _events(block) if kind == "text"))


def _fragments(authored_root):
    parent = authored_root.find(C + "fragments")
    if parent is None:
        raise ClaimsParseError("authored XML omits its fragment index")
    result = {}
    for fragment in parent.findall(C + "fragment"):
        identifier = fragment.get(XML_ID)
        if not identifier or identifier in result:
            raise ClaimsParseError("authored fragment identity is absent or duplicated")
        result[identifier] = fragment
    return result


def parse_claims(authored_root, fragment_digests) -> ClaimSet:
    """Decode exact preamble/limitation units without reading Markdown."""
    blocks = decode_pandoc(authored_root)
    indexed_fragments = _fragments(authored_root)
    claim_fragment_ids = {
        identifier for identifier in indexed_fragments
        if _CLAIM.fullmatch(identifier) or _LIMITATION.fullmatch(identifier)}

    stream = []
    group = None
    for block in blocks:
        if block.get("t") == "Header" and block.get("c", [None])[0] == 3:
            group = _block_text(block)
        for event in _events(block):
            stream.append((event[0], event[1], group))
        stream.append(("text", " ", group))

    claims = []
    consumed = set()
    current = None
    active_id = None
    active_kind = None
    active_index = None
    text_parts = []
    units = []
    limitation_expected = 1

    def finish_unit():
        nonlocal text_parts, active_id, active_kind, active_index
        if current is None or active_id is None:
            text_parts = []
            return
        text = canon.canon_prose("".join(text_parts))
        if active_kind == "preamble":
            text = re.sub(r"^%d\.\s*" % current["number"], "", text)
            text = canon.canon_prose(text)
            if not text:
                text_parts = []
                return
        if not text:
            raise ClaimsParseError("claim unit %s has no exact text" % active_id)
        digest = fragment_digests.get(active_id)
        if digest is None:
            raise ClaimsParseError("claim unit %s has no XML fragment digest" % active_id)
        units.append(ClaimUnit(
            fragment_id=active_id,
            claim_number=current["number"],
            unit_kind=active_kind,
            unit_index=active_index,
            text=text,
            text_digest=canon.text_digest(text),
            content_digest=digest,
        ))
        consumed.add(active_id)
        text_parts = []

    def finish_claim():
        nonlocal current, units, active_id, active_kind, active_index
        if current is None:
            return
        finish_unit()
        if not units:
            raise ClaimsParseError("claim %d has no semantic units" % current["number"])
        full_text = " ".join(unit.text for unit in units)
        dependencies = dependency_references(full_text)
        number = current["number"]
        if any(parent >= number for parent in dependencies):
            raise ClaimsParseError("claim %d contains a non-ancestral claim reference" % number)
        fragment_id = "claim-%d" % number
        claims.append(Claim(
            number=number,
            group=current["group"],
            units=tuple(units),
            dependencies=dependencies,
            fragment_id=fragment_id,
            content_digest=fragment_digests[fragment_id],
        ))
        consumed.add(fragment_id)
        current = None
        units = []
        active_id = active_kind = active_index = None

    for kind, value, event_group in stream:
        if kind == "text":
            if current is not None:
                text_parts.append(value)
            continue
        claim_match = _CLAIM.fullmatch(value)
        limitation_match = _LIMITATION.fullmatch(value)
        if claim_match:
            finish_claim()
            number = int(claim_match.group(1))
            if not event_group:
                raise ClaimsParseError("claim %d has no group heading" % number)
            if value not in indexed_fragments or value not in fragment_digests:
                raise ClaimsParseError("claim %d has no exact fragment identity" % number)
            current = {"number": number, "group": event_group}
            active_id, active_kind, active_index = value, "preamble", 0
            limitation_expected = 1
            text_parts = []
        elif limitation_match:
            number, limitation = map(int, limitation_match.groups())
            if current is None or number != current["number"] or \
                    limitation != limitation_expected:
                raise ClaimsParseError("claim limitation identities are not contiguous")
            finish_unit()
            if value not in indexed_fragments or value not in fragment_digests:
                raise ClaimsParseError("claim limitation has no exact fragment identity")
            active_id, active_kind, active_index = value, "limitation", limitation
            limitation_expected += 1
        elif current is not None:
            finish_claim()
    finish_claim()

    numbers = [claim.number for claim in claims]
    if numbers != list(range(1, len(claims) + 1)):
        raise ClaimsParseError("claim numbering is not exact and contiguous")
    if consumed != claim_fragment_ids:
        raise ClaimsParseError(
            "claim unit coverage is not exact (missing=%r, extra=%r)" %
            (sorted(claim_fragment_ids - consumed), sorted(consumed - claim_fragment_ids)))
    unit_map = {unit.fragment_id: unit for claim in claims for unit in claim.units}
    groups = []
    for claim in claims:
        if not groups or groups[-1][0] != claim.group:
            groups.append((claim.group, []))
        groups[-1][1].append(claim.number)
    return ClaimSet(
        claims=tuple(claims),
        by_number=MappingProxyType({claim.number: claim for claim in claims}),
        units_by_fragment=MappingProxyType(unit_map),
        groups=tuple((label, tuple(numbers)) for label, numbers in groups),
    )


def census(claims):
    sequence = claims.claims if isinstance(claims, ClaimSet) else tuple(claims)
    return len(sequence), sum(len(claim.units) for claim in sequence), \
        MappingProxyType({claim.number: len(claim.units) for claim in sequence})
