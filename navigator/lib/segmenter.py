"""Disclosure/guidance segmentation — markdown -> addressable blocks.

Policy lives in the corpus's segmentation profile (reviewable data, TDD
§8.1): which sections are targetable, editorial, quotable, or excluded is
profile-designated, never hardcoded here. This module only mechanizes the
block grammar shared by all registered markdown corpora.

Anchors are build-specific deterministic: sequential ``S###`` over emitted
blocks in document order, plus ``PC<n>`` whole-claim anchors when the
profile declares a PCT claims section. Identity is never the anchor: every
block carries its canonical-text digest (TDD §7, §13).
"""

import re

from . import canon

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
HR_RE = re.compile(r"^\s*---\s*$")
BULLET_RE = re.compile(r"^- (.*)$")
ORDERED_RE = re.compile(r"^(\d+)\.\s+(.*)$")
CLAIM_HEAD_RE = re.compile(r"^\*\*(\d+)\.\*\*\s+(.*)$")
IMAGE_RE = re.compile(r"^!\[[^\]]*\]\(([^)]+)\)\s*$")
TABLE_LINE_RE = re.compile(r"^\s*\|.*\|\s*$")
TABLE_SEP_RE = re.compile(r"^\s*\|[\s:\-|]+\|\s*$")
CAPTION_RE = re.compile(r"^\*(.+)\*\s*$")
SUB_RE = re.compile(r"^<sub>(.*)</sub>\s*$", re.S)
ENUM_PREFIX_RE = re.compile(r"^\d+\.\s+")

CLASSES = ("targetable", "editorial", "quotable", "excluded", "claims")


class SegmentError(ValueError):
    pass


class Block:
    __slots__ = (
        "id", "kind", "cls", "path", "label", "text", "canonical", "digest",
        "rows", "meta",
    )

    def __init__(self, kind, cls, path, label, text, canonical, digest,
                 rows=None, meta=None):
        self.id = None
        self.kind = kind
        self.cls = cls
        self.path = path
        self.label = label
        self.text = text
        self.canonical = canonical
        self.digest = digest
        self.rows = rows or []
        self.meta = meta or {}

    def as_dict(self):
        d = {
            "id": self.id, "kind": self.kind, "class": self.cls,
            "path": list(self.path), "label": self.label,
            "text": self.text, "digest": self.digest,
        }
        if self.rows:
            d["rows"] = [
                {"id": r["id"], "label": r["label"], "digest": r["digest"],
                 "cells": r["cells"]}
                for r in self.rows
            ]
        if self.meta:
            d["meta"] = dict(self.meta)
        return d


def _norm_heading(text):
    """Heading text -> path component: strip enumeration and emphasis."""
    text = re.sub(r"[*_`]", "", text).strip()
    text = ENUM_PREFIX_RE.sub("", text)
    return text


def _match_rule(rule, kind, path):
    m = rule.get("match", {})
    if "kind" in m and m["kind"] != kind:
        return False
    if "path" in m:
        want = m["path"]
        if len(want) > len(path):
            return False
        import fnmatch
        for w, p in zip(want, path):
            if not fnmatch.fnmatch(p, w):
                return False
    return True


def classify(profile, kind, path):
    for rule in profile["rules"]:
        if _match_rule(rule, kind, path):
            return rule
    return {"class": "excluded"}


def _parse_raw(lines):
    """Yield raw markdown elements: (kind, payload) in document order."""
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if HR_RE.match(line):
            i += 1
            continue
        m = HEADING_RE.match(line)
        if m:
            yield ("heading", (len(m.group(1)), m.group(2).strip()))
            i += 1
            continue
        if line.startswith("```"):
            body = []
            i += 1
            while i < n and not lines[i].startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1  # closing fence
            yield ("code", "\n".join(body))
            continue
        if line.startswith(">"):
            body = []
            while i < n and lines[i].startswith(">"):
                body.append(lines[i].lstrip(">").strip())
                i += 1
            yield ("blockquote", " ".join(b for b in body if b))
            continue
        if TABLE_LINE_RE.match(line):
            rows = []
            while i < n and TABLE_LINE_RE.match(lines[i]):
                if not TABLE_SEP_RE.match(lines[i]):
                    cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                    rows.append(cells)
                i += 1
            caption = ""
            # a following italic *Table N. ...* line (blank lines allowed
            # between) is the caption
            j = i
            while j < n and not lines[j].strip():
                j += 1
            if j < n and lines[j].strip().startswith("*Table") and \
                    CAPTION_RE.match(lines[j].strip()):
                caption = CAPTION_RE.match(lines[j].strip()).group(1)
                i = j + 1
            yield ("table", (rows, caption))
            continue
        m = IMAGE_RE.match(line)
        if m:
            yield ("image", m.group(1))
            i += 1
            continue
        m = BULLET_RE.match(line)
        if m:
            item = [m.group(1)]
            i += 1
            while i < n and lines[i].strip() and not BULLET_RE.match(lines[i]) \
                    and not HEADING_RE.match(lines[i]) and not lines[i].startswith(("```", ">", "|", "!")):
                item.append(lines[i].strip())
                i += 1
            yield ("bullet", " ".join(item))
            continue
        m = ORDERED_RE.match(line)
        if m and not CLAIM_HEAD_RE.match(line):
            item = [m.group(2)]
            i += 1
            while i < n and lines[i].strip() and not ORDERED_RE.match(lines[i]) \
                    and not HEADING_RE.match(lines[i]) and not lines[i].startswith(("```", ">", "|", "!", "- ")):
                item.append(lines[i].strip())
                i += 1
            yield ("ordered", (int(m.group(1)), " ".join(item)))
            continue
        m = SUB_RE.match(line)
        if m:
            yield ("footer", m.group(1))
            i += 1
            continue
        m = CLAIM_HEAD_RE.match(line)
        if m:
            para = [line]
            i += 1
            while i < n and lines[i].strip() and not HEADING_RE.match(lines[i]):
                para.append(lines[i].strip())
                i += 1
            yield ("claimhead", " ".join(para))
            continue
        # paragraph
        para = [line.strip()]
        i += 1
        while i < n and lines[i].strip() and not HEADING_RE.match(lines[i]) \
                and not lines[i].startswith(("```", ">", "|", "!", "- ")) \
                and not ORDERED_RE.match(lines[i]) and not HR_RE.match(lines[i]) \
                and not SUB_RE.match(lines[i]):
            para.append(lines[i].strip())
            i += 1
        yield ("paragraph", " ".join(para))


def segment(text, profile, read_file):
    """Segment one markdown corpus file under its profile.

    ``read_file(relpath) -> bytes`` supplies sibling files (figures) through
    the caller's gateway so every read lands in the content lock.
    """
    lines = text.split("\n")
    path = []           # normalized heading path
    counters = {}       # per-(path, kind) ordinals for labels
    blocks = []
    pct_claims = []     # (claim_number, [Block]) while inside claims section
    current_claim = None

    def section_name():
        return path[-1] if path else ""

    def bump(kind):
        key = (tuple(path), kind)
        counters[key] = counters.get(key, 0) + 1
        return counters[key]

    def close_claim():
        nonlocal current_claim
        if current_claim is not None:
            pct_claims.append(current_claim)
            current_claim = None

    in_claims = False
    claims_path = profile.get("pctClaimsSection")

    for kind, payload in _parse_raw(lines):
        if kind == "heading":
            level, raw = payload
            close_claim()
            name = _norm_heading(raw)
            # maintain path by heading level
            del path[level - 1:]
            while len(path) < level - 1:
                path.append("")
            path.append(name)
            in_claims = bool(claims_path) and len(path) >= len(claims_path) \
                and path[-len(claims_path):] == list(claims_path)
            rule = classify(profile, "heading", path)
            if rule["class"] in ("excluded", "claims"):
                continue
            canonical = canon.canon_prose(name)
            blocks.append(Block(
                "heading", rule["class"], tuple(path), name,
                raw, canonical, canon.text_digest(canonical)))
            continue

        rule = classify(profile, kind, path)
        cls = rule["class"]
        if cls == "excluded":
            continue
        if cls == "claims":
            # claim-set §3 claims are the fragment corpus, parsed by
            # lib.claims — never generic blocks (blockquotes there may be
            # separately designated by kind-specific rules).
            continue

        if in_claims and kind == "claimhead":
            close_claim()
            m = CLAIM_HEAD_RE.match(payload)
            num = int(m.group(1))
            canonical = canon.canon_prose(payload)
            b = Block("claim-head", cls, tuple(path),
                      "PCT claim %d — head" % num,
                      payload, canonical, canon.text_digest(canonical),
                      meta={"pctClaim": num})
            blocks.append(b)
            current_claim = (num, [b])
            continue
        if in_claims and kind == "bullet" and current_claim is not None:
            num = current_claim[0]
            idx = len(current_claim[1])  # head is 1 -> first element idx 1
            canonical = canon.canon_prose(payload)
            b = Block("claim-element", cls, tuple(path),
                      "PCT claim %d — element %d" % (num, idx),
                      payload, canonical, canon.text_digest(canonical),
                      meta={"pctClaim": num, "element": idx})
            blocks.append(b)
            current_claim[1].append(b)
            continue
        close_claim()

        if kind == "paragraph" or kind == "claimhead":
            n = bump("paragraph")
            canonical = canon.canon_prose(payload)
            blocks.append(Block(
                "paragraph", cls, tuple(path),
                "%s · ¶%d" % (section_name(), n),
                payload, canonical, canon.text_digest(canonical)))
        elif kind == "blockquote":
            n = bump("note")
            canonical = canon.canon_prose(payload)
            label = rule.get("editorialLabel") or "%s · note %d" % (section_name(), n)
            blocks.append(Block(
                "note", cls, tuple(path), label,
                payload, canonical, canon.text_digest(canonical)))
        elif kind in ("bullet", "ordered"):
            textval = payload if kind == "bullet" else payload[1]
            n = bump("item")
            canonical = canon.canon_prose(textval)
            blocks.append(Block(
                "list-item", cls, tuple(path),
                "%s · item %d" % (section_name(), n),
                textval, canonical, canon.text_digest(canonical)))
        elif kind == "code":
            n = bump("code")
            canonical = canon.canon_code(payload)
            blocks.append(Block(
                "code", cls, tuple(path),
                "%s · code %d" % (section_name(), n),
                payload, canonical, canon.text_digest(canonical)))
        elif kind == "table":
            rows, caption = payload
            serialized = canon.canon_table(rows, caption)
            m = re.match(r"(Table \d+)", caption)
            n = bump("table")
            tlabel = m.group(1) if m else "table %d" % n
            header_word = rows[0][0].split()[0] if rows and rows[0] and rows[0][0] else "row"
            row_objs = []
            for ri, cells in enumerate(rows[1:], start=1):
                rlabel = "row %s %s" % (header_word, cells[0]) if cells else "row %d" % ri
                row_objs.append({
                    "id": "r%d" % ri, "label": rlabel, "cells": cells,
                    "digest": canon.text_digest(canon.canon_table_row(cells)),
                })
            blocks.append(Block(
                "table", cls, tuple(path),
                "%s · %s" % (section_name(), tlabel),
                serialized, serialized, canon.text_digest(serialized),
                rows=row_objs,
                meta={"caption": caption, "header": rows[0] if rows else []}))
        elif kind == "image":
            relpath = payload
            data = read_file(relpath)
            n = bump("figure")
            # caption: profile-declared editorial numeral caption follows
            blocks.append(Block(
                "figure", cls, tuple(path),
                "%s · image" % section_name(),
                relpath, "", None,
                meta={"file": relpath,
                      "fileDigest": canon.bytes_digest(data),
                      "bytes": len(data)}))
        elif kind == "footer":
            canonical = canon.canon_prose(payload)
            blocks.append(Block(
                "footer", cls, tuple(path),
                rule.get("editorialLabel", "Filing data"),
                payload, canonical, canon.text_digest(canonical)))
        else:  # pragma: no cover
            raise SegmentError("unhandled element kind %r" % kind)

    close_claim()

    # Assign anchors: sequential S### over emitted blocks in document order.
    for i, b in enumerate(blocks, start=1):
        b.id = "S%03d" % i

    # Attach figure captions (the paragraph following each figure in its
    # section is that figure's editorial numeral caption) and complete the
    # figure composite digest.
    for idx, b in enumerate(blocks):
        if b.kind != "figure":
            continue
        cap = None
        for nb in blocks[idx + 1:]:
            if nb.kind == "figure" or nb.kind == "heading":
                break
            if nb.kind == "paragraph":
                cap = nb
                break
        caption_text = cap.canonical if cap else ""
        b.canonical = caption_text
        b.digest = canon.composite_digest(
            "aa11393:figure:c1",
            [b.meta["fileDigest"], canon.text_digest(caption_text)])
        if cap is not None:
            cap.cls = "editorial"
            cap.kind = "figure-caption"
            cap.label = "%s · caption" % b.path[-1]
            b.meta["captionBlock"] = cap.id

    # Whole-claim anchors PC<n> for a declared PCT claims section.
    wholes = []
    for num, members in pct_claims:  # noqa: E305
        canonical = " ".join(m.canonical for m in members)
        wb = Block(
            "claim-whole", members[0].cls, members[0].path,
            "PCT claim %d (whole)" % num,
            canonical, canonical, canon.text_digest(canonical),
            meta={"pctClaim": num, "members": [m.id for m in members]})
        wb.id = "PC%d" % num
        wholes.append(wb)
    blocks.extend(wholes)
    return blocks
