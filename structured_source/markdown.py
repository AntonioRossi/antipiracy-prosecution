"""Closed authored-Markdown to typed XML conversion.

Authored Markdown remains the content authority. Pandoc supplies the pinned
GFM parse and write boundary. Generated XML preserves the complete ordered
Pandoc AST and adds a recomputable fragment index for every exact stable
anchor; the index is never a second editable content owner.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import math
import os
import re
import subprocess
import unicodedata
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET

from . import CONTENT_NAMESPACE, SCHEMA_VERSION
from .canonical import raw_digest
from .errors import StructuredSourceError
from .parser import MAX_XML_BYTES, parse_artifact
from .profiles import load_projection_profile

C = "{%s}" % CONTENT_NAMESPACE
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
AUTHORED_PROFILE = "authored-markdown-v1"
_DOCUMENT_ID = re.compile(r"[a-z][a-z0-9-]{0,159}\Z")
_ANCHOR_OPEN = re.compile(r'<a id="(ssp-[a-z][a-z0-9-]{0,155})">\Z')
_CLAIM_ID = re.compile(r"claim-[1-9][0-9]*\Z")
_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_DROP = object()


@dataclass(frozen=True)
class AuthoredConversion:
    """One fully checked generated representation and semantic back-render."""

    xml: bytes
    markdown: bytes
    source_raw_digest: str
    generated_markdown_raw_digest: str
    semantic_digest: str
    item_ids: tuple[str, ...]
    fragment_digests: dict[str, str]


@dataclass(frozen=True)
class _AnchorOccurrence:
    presentation_id: str
    fragment_id: str
    block_position: int
    has_semantic_after: bool


@dataclass(frozen=True)
class _Analysis:
    semantic_model: dict
    fragments: tuple[dict[str, str], ...]


def _profile() -> dict:
    return load_projection_profile()


def _canonical_repo_path(path: str) -> str:
    if not isinstance(path, str) or not path or len(path) > 512 or \
            os.path.isabs(path) or "\\" in path or any(
                part in {"", ".", ".."} for part in path.split("/")):
        raise StructuredSourceError("authored Markdown path is not canonical")
    return path


def _source_text(markdown: bytes) -> str:
    if not isinstance(markdown, bytes):
        raise TypeError("authored Markdown input must be bytes")
    if not markdown or len(markdown) > MAX_XML_BYTES or markdown.startswith(
            (b"\xef\xbb\xbf", b"\xff\xfe", b"\xfe\xff")):
        raise StructuredSourceError("authored Markdown byte size or encoding is invalid")
    try:
        text = markdown.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise StructuredSourceError("authored Markdown is not UTF-8") from exc
    if "\r" in text or unicodedata.normalize("NFC", text) != text or \
            (_profile()["finalNewline"] and not text.endswith("\n")) or \
            _CONTROL.search(text):
        raise StructuredSourceError(
            "authored Markdown is not NFC LF text with the required final newline")
    return text


def _run_pandoc(arguments: list[str], payload: bytes) -> bytes:
    try:
        result = subprocess.run(
            ["pandoc", *arguments], input=payload, capture_output=True,
            timeout=60, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise StructuredSourceError("pinned Pandoc capability is unavailable") from exc
    if result.returncode:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise StructuredSourceError("Pandoc conversion failed: %s" % detail[:500])
    return result.stdout


def _read_pandoc(markdown: bytes) -> dict:
    _source_text(markdown)
    profile = _profile()
    output = _run_pandoc(
        ["--from=" + profile["pandocReader"], "--to=json"], markdown)
    try:
        ast = json.loads(output.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise StructuredSourceError("Pandoc emitted malformed JSON") from exc
    if not isinstance(ast, dict) or set(ast) != {
            "pandoc-api-version", "meta", "blocks"} or \
            ast["pandoc-api-version"] != profile["pandocApiVersion"] or \
            ast["meta"] != {} or not isinstance(ast["blocks"], list) or \
            not ast["blocks"]:
        raise StructuredSourceError(
            "Pandoc JSON API, metadata, or block set is outside gfm-v1")
    return ast


def _node_constructor(node: object, label: str) -> tuple[str, object]:
    if not isinstance(node, dict) or set(node) not in ({"t"}, {"t", "c"}) or \
            not isinstance(node.get("t"), str):
        raise StructuredSourceError("%s is not a closed Pandoc node" % label)
    return node["t"], node.get("c")


def _no_content(node: dict, label: str) -> None:
    if set(node) != {"t"}:
        raise StructuredSourceError("%s unexpectedly carries content" % label)


def _text(value: object, label: str, allow_empty: bool = True) -> str:
    if not isinstance(value, str) or (not allow_empty and not value) or \
            unicodedata.normalize("NFC", value) != value or _CONTROL.search(value):
        raise StructuredSourceError("%s is not closed NFC text" % label)
    return value


def _attribute(value: object, label: str) -> None:
    if not isinstance(value, list) or len(value) != 3:
        raise StructuredSourceError("%s has a malformed Pandoc attribute" % label)
    identifier, classes, pairs = value
    _text(identifier, label + " identifier")
    if not isinstance(classes, list) or not all(
            isinstance(item, str) and item for item in classes) or \
            len(classes) != len(set(classes)):
        raise StructuredSourceError("%s classes are malformed" % label)
    if not isinstance(pairs, list):
        raise StructuredSourceError("%s key/value attributes are malformed" % label)
    keys = []
    for pair in pairs:
        if not isinstance(pair, list) or len(pair) != 2:
            raise StructuredSourceError("%s key/value attribute is malformed" % label)
        keys.append(_text(pair[0], label + " key", allow_empty=False))
        _text(pair[1], label + " value")
    if len(keys) != len(set(keys)):
        raise StructuredSourceError("%s key/value attributes are duplicated" % label)


def _auxiliary(node: object, allowed: set[str], label: str) -> str:
    constructor, content = _node_constructor(node, label)
    if constructor not in allowed:
        raise StructuredSourceError("%s constructor is outside gfm-v1" % label)
    if constructor == "ColWidth":
        if set(node) != {"t", "c"} or isinstance(content, bool) or \
                not isinstance(content, (int, float)) or not math.isfinite(content) or \
                content <= 0 or content > 1:
            raise StructuredSourceError("table column width is invalid")
    else:
        _no_content(node, label)
    return constructor


def _target(value: object, label: str) -> None:
    if not isinstance(value, list) or len(value) != 2:
        raise StructuredSourceError("%s target is malformed" % label)
    target = _text(value[0], label + " URL", allow_empty=False)
    _text(value[1], label + " title")
    if "\\" in target or any(ord(character) < 32 for character in target):
        raise StructuredSourceError("%s target contains a forbidden character" % label)
    try:
        parsed = urlsplit(target)
    except ValueError as exc:
        raise StructuredSourceError("%s target URL is malformed" % label) from exc
    if parsed.scheme and parsed.scheme.lower() not in _profile()["externalSchemes"]:
        raise StructuredSourceError("%s target scheme is outside gfm-v1" % label)
    if not parsed.scheme and (parsed.netloc or parsed.path.startswith("/")):
        raise StructuredSourceError("%s target must be repository-relative" % label)


def _inlines(value: object, label: str) -> None:
    if not isinstance(value, list):
        raise StructuredSourceError("%s is not an inline list" % label)
    for index, node in enumerate(value):
        _inline(node, "%s inline %d" % (label, index))


def _inline(node: object, label: str) -> None:
    constructor, content = _node_constructor(node, label)
    if constructor not in _profile()["supportedInlineConstructors"]:
        raise StructuredSourceError(
            "%s constructor %s is outside gfm-v1" % (label, constructor))
    if constructor == "Str":
        _text(content, label + " text", allow_empty=False)
        if any(character.isspace() for character in content):
            raise StructuredSourceError("Pandoc Str content cannot contain whitespace")
    elif constructor in {"Space", "SoftBreak", "LineBreak"}:
        _no_content(node, label)
    elif constructor in {"Emph", "Strong", "Strikeout"}:
        _inlines(content, label)
        if not content:
            raise StructuredSourceError("%s cannot be empty" % label)
    elif constructor == "Code":
        if not isinstance(content, list) or len(content) != 2:
            raise StructuredSourceError("inline code is malformed")
        _attribute(content[0], label)
        _text(content[1], label + " text")
    elif constructor == "Math":
        if not isinstance(content, list) or len(content) != 2:
            raise StructuredSourceError("inline math is malformed")
        _auxiliary(content[0], {"InlineMath", "DisplayMath"}, label + " style")
        _text(content[1], label + " text", allow_empty=False)
    elif constructor in {"Link", "Image"}:
        if not isinstance(content, list) or len(content) != 3:
            raise StructuredSourceError("%s is malformed" % label)
        _attribute(content[0], label)
        _inlines(content[1], label)
        _target(content[2], label)
    elif constructor == "Note":
        _blocks(content, label + " note")
    elif constructor == "RawInline":
        if not isinstance(content, list) or len(content) != 2 or \
                content[0] != "html" or not isinstance(content[1], str) or \
                (content[1] != "</a>" and
                 _ANCHOR_OPEN.fullmatch(content[1]) is None):
            raise StructuredSourceError(
                "only exact paired stable-anchor RawInline nodes are allowed")
    else:  # pragma: no cover - profile and cases must evolve atomically
        raise StructuredSourceError("unimplemented inline constructor %s" % constructor)


def _blocks(value: object, label: str) -> None:
    if not isinstance(value, list) or not value:
        raise StructuredSourceError("%s is not a nonempty block list" % label)
    for index, node in enumerate(value):
        _block(node, "%s block %d" % (label, index), top_level=False)


def _rows(value: object, label: str) -> None:
    if not isinstance(value, list):
        raise StructuredSourceError("%s rows are malformed" % label)
    for row_index, row in enumerate(value):
        if not isinstance(row, list) or len(row) != 2:
            raise StructuredSourceError("%s row is malformed" % label)
        _attribute(row[0], "%s row %d" % (label, row_index))
        if not isinstance(row[1], list) or not row[1]:
            raise StructuredSourceError("%s row has no cells" % label)
        for cell_index, cell in enumerate(row[1]):
            if not isinstance(cell, list) or len(cell) != 5:
                raise StructuredSourceError("%s cell is malformed" % label)
            cell_label = "%s row %d cell %d" % (label, row_index, cell_index)
            _attribute(cell[0], cell_label)
            _auxiliary(cell[1], {
                "AlignCenter", "AlignDefault", "AlignLeft", "AlignRight"},
                cell_label + " alignment")
            if isinstance(cell[2], bool) or not isinstance(cell[2], int) or \
                    isinstance(cell[3], bool) or not isinstance(cell[3], int) or \
                    cell[2] < 1 or cell[3] < 1:
                raise StructuredSourceError("%s span is invalid" % cell_label)
            _blocks(cell[4], cell_label)


def _table(content: object, label: str) -> None:
    if not isinstance(content, list) or len(content) != 6:
        raise StructuredSourceError("%s table payload is malformed" % label)
    attributes, caption, columns, head, bodies, foot = content
    _attribute(attributes, label)
    if not isinstance(caption, list) or len(caption) != 2 or \
            caption[0] is not None and not isinstance(caption[0], list) or \
            not isinstance(caption[1], list):
        raise StructuredSourceError("%s caption is malformed" % label)
    if caption[0] is not None:
        _inlines(caption[0], label + " short caption")
    if caption[1]:
        _blocks(caption[1], label + " caption")
    if not isinstance(columns, list) or not columns:
        raise StructuredSourceError("%s column specification is malformed" % label)
    for index, column in enumerate(columns):
        if not isinstance(column, list) or len(column) != 2:
            raise StructuredSourceError("%s column is malformed" % label)
        _auxiliary(column[0], {
            "AlignCenter", "AlignDefault", "AlignLeft", "AlignRight"},
            "%s column %d alignment" % (label, index))
        _auxiliary(column[1], {"ColWidth", "ColWidthDefault"},
                   "%s column %d width" % (label, index))
    if not isinstance(head, list) or len(head) != 2:
        raise StructuredSourceError("%s head is malformed" % label)
    _attribute(head[0], label + " head")
    _rows(head[1], label + " head")
    if not isinstance(bodies, list):
        raise StructuredSourceError("%s bodies are malformed" % label)
    for index, body in enumerate(bodies):
        if not isinstance(body, list) or len(body) != 4:
            raise StructuredSourceError("%s body is malformed" % label)
        _attribute(body[0], "%s body %d" % (label, index))
        if isinstance(body[1], bool) or not isinstance(body[1], int) or body[1] < 0:
            raise StructuredSourceError("%s body row-head count is invalid" % label)
        _rows(body[2], "%s body %d intermediate head" % (label, index))
        _rows(body[3], "%s body %d" % (label, index))
    if not isinstance(foot, list) or len(foot) != 2:
        raise StructuredSourceError("%s foot is malformed" % label)
    _attribute(foot[0], label + " foot")
    _rows(foot[1], label + " foot")


def _block(node: object, label: str, *, top_level: bool) -> None:
    constructor, content = _node_constructor(node, label)
    allowed = (_profile()["topLevelBlockConstructors"] if top_level
               else _profile()["supportedBlockConstructors"])
    if constructor not in allowed:
        raise StructuredSourceError(
            "%s constructor %s is outside gfm-v1" % (label, constructor))
    if constructor in {"Para", "Plain"}:
        _inlines(content, label)
        if not content:
            raise StructuredSourceError("%s cannot be empty" % label)
    elif constructor == "Header":
        if not isinstance(content, list) or len(content) != 3 or \
                isinstance(content[0], bool) or not isinstance(content[0], int) or \
                not 1 <= content[0] <= 6:
            raise StructuredSourceError("%s header is malformed" % label)
        _attribute(content[1], label)
        _inlines(content[2], label)
        if not content[2]:
            raise StructuredSourceError("%s header cannot be empty" % label)
    elif constructor == "CodeBlock":
        if not isinstance(content, list) or len(content) != 2:
            raise StructuredSourceError("%s code block is malformed" % label)
        _attribute(content[0], label)
        _text(content[1], label + " text")
    elif constructor == "BlockQuote":
        _blocks(content, label)
    elif constructor == "BulletList":
        if not isinstance(content, list) or not content:
            raise StructuredSourceError("%s list has no items" % label)
        for index, item in enumerate(content):
            _blocks(item, "%s item %d" % (label, index))
    elif constructor == "OrderedList":
        if not isinstance(content, list) or len(content) != 2 or \
                not isinstance(content[0], list) or len(content[0]) != 3 or \
                isinstance(content[0][0], bool) or not isinstance(content[0][0], int) or \
                content[0][0] < 1 or not isinstance(content[1], list) or not content[1]:
            raise StructuredSourceError("%s ordered list is malformed" % label)
        _auxiliary(content[0][1], {"Decimal"}, label + " numbering")
        _auxiliary(content[0][2], {"OneParen", "Period"}, label + " delimiter")
        for index, item in enumerate(content[1]):
            _blocks(item, "%s item %d" % (label, index))
    elif constructor == "HorizontalRule":
        _no_content(node, label)
    elif constructor == "Table":
        _table(content, label)
    else:  # pragma: no cover - profile and cases must evolve atomically
        raise StructuredSourceError("unimplemented block constructor %s" % constructor)


def _raw_anchor(node: object) -> tuple[str, str | None] | None:
    if not isinstance(node, dict) or node.get("t") != "RawInline":
        return None
    if set(node) != {"t", "c"} or not isinstance(node["c"], list) or \
            len(node["c"]) != 2 or node["c"][0] != "html" or \
            not isinstance(node["c"][1], str):
        raise StructuredSourceError(
            "only exact paired stable-anchor RawInline nodes are allowed")
    if node["c"][1] == "</a>":
        return "close", None
    match = _ANCHOR_OPEN.fullmatch(node["c"][1])
    if match is None:
        raise StructuredSourceError(
            "only exact paired stable-anchor RawInline nodes are allowed")
    return "open", match.group(1)


def _separator(value: object) -> bool:
    return isinstance(value, dict) and value.get("t") in {"Space", "SoftBreak"}


def _semantic_content(value: object) -> bool:
    if isinstance(value, list):
        return any(_semantic_content(item) for item in value)
    if not isinstance(value, dict):
        return value not in (None, "", False)
    constructor = value.get("t")
    if constructor == "RawInline" or constructor in {"Space", "SoftBreak"}:
        return False
    if constructor in {"Para", "Plain"}:
        return _semantic_content(value.get("c", []))
    return True


def _clean_value(value: object) -> object:
    """Remove presentation anchors and their empty carrier blocks."""
    if isinstance(value, list):
        cleaned = []
        removed_anchor = False
        index = 0
        while index < len(value):
            anchor = _raw_anchor(value[index])
            if anchor is not None:
                if anchor[0] != "open" or index + 1 >= len(value) or \
                        _raw_anchor(value[index + 1]) != ("close", None):
                    raise StructuredSourceError(
                        "stable anchors must be exact adjacent open/close pairs")
                removed_anchor = True
                index += 2
                continue
            item = _clean_value(value[index])
            if item is not _DROP:
                cleaned.append(item)
            index += 1
        if removed_anchor:
            while cleaned and _separator(cleaned[0]):
                cleaned.pop(0)
            while cleaned and _separator(cleaned[-1]):
                cleaned.pop()
            normalized = []
            for item in cleaned:
                if normalized and _separator(normalized[-1]) and _separator(item):
                    if normalized[-1].get("t") == "SoftBreak" and \
                            item.get("t") == "Space":
                        normalized[-1] = item
                    continue
                if normalized and isinstance(normalized[-1], dict) and \
                        normalized[-1].get("t") == "Str" and \
                        isinstance(item, dict) and item.get("t") == "Str":
                    normalized[-1] = {
                        "t": "Str", "c": normalized[-1]["c"] + item["c"]}
                    continue
                normalized.append(item)
            cleaned = normalized
        return cleaned
    if isinstance(value, dict):
        constructor, content = _node_constructor(value, "Pandoc semantic value")
        if constructor == "RawInline":
            raise StructuredSourceError(
                "stable anchor RawInline nodes must occur in an inline list")
        result = {"t": constructor}
        if "c" in value:
            result["c"] = _clean_value(content)
        if constructor in {"Para", "Plain"} and \
                not _semantic_content(result.get("c", [])):
            return _DROP
        return result
    return value


def _plain_excerpt(value: object) -> str:
    parts: list[str] = []

    def visit(item: object) -> None:
        if isinstance(item, list):
            for child in item:
                visit(child)
            return
        if not isinstance(item, dict):
            return
        constructor = item.get("t")
        content = item.get("c")
        if constructor is None:
            for child in item.values():
                visit(child)
        elif constructor == "Str":
            parts.append(content)
        elif constructor in {"Space", "SoftBreak", "LineBreak"}:
            parts.append(" ")
        elif constructor in {"Code", "Math"} and isinstance(content, list) and \
                len(content) == 2 and isinstance(content[1], str):
            parts.extend((" ", content[1], " "))
        elif "c" in item:
            visit(content)
        elif constructor:
            parts.extend((" [", constructor, "] "))

    visit(value)
    excerpt = " ".join("".join(parts).split())
    return excerpt or "[structural content]"


def _binding_digest(value: object) -> str:
    payload = (json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True) +
        "\n").encode("utf-8")
    return raw_digest(payload)


def _analyse_ast(ast: dict, document_id: str) -> _Analysis:
    if _DOCUMENT_ID.fullmatch(document_id) is None:
        raise StructuredSourceError("authored document ID is not a stable explicit ID")
    for index, block in enumerate(ast["blocks"]):
        _block(block, "top-level block %d" % index, top_level=True)

    block_nodes: list[dict] = []
    occurrences: list[_AnchorOccurrence] = []
    seen: set[str] = set()
    block_constructors = set(_profile()["supportedBlockConstructors"])

    def walk(value: object, current_block: int | None = None) -> None:
        if isinstance(value, dict):
            constructor, content = _node_constructor(value, "Pandoc anchor scan")
            nested_block = current_block
            if constructor in block_constructors:
                nested_block = len(block_nodes)
                block_nodes.append(value)
            if "c" in value:
                walk(content, nested_block)
            return
        if not isinstance(value, list):
            return
        index = 0
        while index < len(value):
            anchor = _raw_anchor(value[index])
            if anchor is None:
                walk(value[index], current_block)
                index += 1
                continue
            if anchor[0] != "open" or index + 1 >= len(value) or \
                    _raw_anchor(value[index + 1]) != ("close", None):
                raise StructuredSourceError(
                    "stable anchors must be exact adjacent open/close pairs")
            if current_block is None:
                raise StructuredSourceError("stable anchor occurs outside a Pandoc block")
            presentation_id = anchor[1]
            if presentation_id in seen:
                raise StructuredSourceError(
                    "duplicate stable anchor %s" % presentation_id)
            seen.add(presentation_id)
            fragment_id = presentation_id[len(_profile()["stableAnchorPrefix"]):]
            if _DOCUMENT_ID.fullmatch(fragment_id) is None:
                raise StructuredSourceError("stable anchor has no valid XML fragment ID")
            occurrences.append(_AnchorOccurrence(
                presentation_id=presentation_id,
                fragment_id=fragment_id,
                block_position=current_block,
                has_semantic_after=_semantic_content(value[index + 2:])))
            index += 2

    for block in ast["blocks"]:
        walk(block)
    if not occurrences:
        raise StructuredSourceError("authored Markdown contains no stable anchors")
    expected_root = "ssp-%s-root" % document_id
    if occurrences[0].presentation_id != expected_root:
        raise StructuredSourceError(
            "first stable anchor must be the exact document root %s" % expected_root)

    cleaned_blocks = [_clean_value(block) for block in block_nodes]
    block_ordinals: dict[int, int] = {}
    ordinal = 0
    for position, cleaned in enumerate(cleaned_blocks):
        if cleaned is not _DROP:
            block_ordinals[position] = ordinal
            ordinal += 1
    semantic_blocks = []
    for block in ast["blocks"]:
        cleaned = _clean_value(block)
        if cleaned is not _DROP:
            semantic_blocks.append(cleaned)
    if not semantic_blocks:
        raise StructuredSourceError("authored Markdown has no semantic content")

    targets: list[tuple[str, object]] = []
    for occurrence in occurrences:
        position = occurrence.block_position
        if occurrence.has_semantic_after and position in block_ordinals:
            target_position = position
        else:
            target_position = next((candidate for candidate in range(
                position + 1, len(block_nodes)) if candidate in block_ordinals), -1)
        if target_position < 0:
            if occurrence.presentation_id == expected_root:
                targets.append(("$", semantic_blocks))
                continue
            raise StructuredSourceError(
                "stable anchor %s has no semantic target" % occurrence.presentation_id)
        targets.append((
            "block:%d" % block_ordinals[target_position],
            cleaned_blocks[target_position]))

    fragments: list[dict[str, str]] = []
    for index, occurrence in enumerate(occurrences):
        if index == 0:
            kind = "document"
            path = "$"
            binding = semantic_blocks
        elif _CLAIM_ID.fullmatch(occurrence.fragment_id):
            kind = "claim"
            path = "claim:%s" % occurrence.fragment_id
            prefix = occurrence.fragment_id + "-limitation-"
            claim_targets = []
            claim_paths = set()
            for target_index in range(index, len(occurrences)):
                candidate = occurrences[target_index]
                if target_index != index and not candidate.fragment_id.startswith(prefix):
                    break
                target_path, target = targets[target_index]
                if target_path not in claim_paths:
                    claim_paths.add(target_path)
                    claim_targets.append(target)
            if not claim_targets:
                raise StructuredSourceError(
                    "claim anchor %s has no claim content" % occurrence.presentation_id)
            binding = {"claim": occurrence.fragment_id, "blocks": claim_targets}
        else:
            kind = "block"
            path, binding = targets[index]
        fragments.append({
            "id": occurrence.fragment_id,
            "presentationId": occurrence.presentation_id,
            "bindingKind": kind,
            "semanticPath": path,
            "bindingDigest": _binding_digest(binding),
            "excerpt": _plain_excerpt(binding),
        })

    return _Analysis(
        semantic_model={
            "pandoc-api-version": ast["pandoc-api-version"],
            "meta": {},
            "blocks": semantic_blocks,
            "fragments": fragments,
        },
        fragments=tuple(fragments),
    )


def normalized_pandoc_ast(markdown: bytes, document_id: str) -> dict:
    """Return anchor-placement-neutral ordered semantics and bindings."""
    return _analyse_ast(_read_pandoc(markdown), document_id).semantic_model


def _value_element(parent: ET.Element, value: object) -> None:
    if value is None:
        ET.SubElement(parent, C + "null")
    elif isinstance(value, bool):
        ET.SubElement(parent, C + "boolean").text = "true" if value else "false"
    elif isinstance(value, int):
        ET.SubElement(parent, C + "integer").text = str(value)
    elif isinstance(value, float):
        if not math.isfinite(value):
            raise StructuredSourceError("Pandoc JSON contains a non-finite number")
        ET.SubElement(parent, C + "number").text = format(value, ".17f").rstrip(
            "0").rstrip(".")
    elif isinstance(value, str):
        ET.SubElement(parent, C + "string").text = value
    elif isinstance(value, list):
        array = ET.SubElement(parent, C + "array")
        for item in value:
            _value_element(array, item)
    elif isinstance(value, dict):
        constructor, content = _node_constructor(value, "Pandoc XML value")
        node = ET.SubElement(parent, C + "node", {"constructor": constructor})
        if "c" in value:
            _value_element(node, content)
    else:
        raise StructuredSourceError("Pandoc JSON contains an unsupported value type")


def _xml_bytes(ast: dict, analysis: _Analysis, markdown: bytes,
               markdown_path: str, document_id: str) -> bytes:
    path = _canonical_repo_path(markdown_path)
    ET.register_namespace("", CONTENT_NAMESPACE)
    root = ET.Element(C + "authored", {
        "schemaProfile": AUTHORED_PROFILE,
        "schemaVersion": SCHEMA_VERSION,
    })
    ET.SubElement(root, C + "documentIdentity", {"documentId": document_id})
    ET.SubElement(root, C + "markdownBinding", {
        "path": path,
        "rawDigest": raw_digest(markdown),
        "size": str(len(markdown)),
    })
    fragments = ET.SubElement(root, C + "fragments")
    for record in analysis.fragments:
        fragment = ET.SubElement(fragments, C + "fragment", {
            XML_ID: record["id"],
            "presentationId": record["presentationId"],
            "bindingKind": record["bindingKind"],
            "semanticPath": record["semanticPath"],
            "bindingDigest": record["bindingDigest"],
        })
        ET.SubElement(fragment, C + "excerpt").text = record["excerpt"]
    pandoc = ET.SubElement(root, C + "pandoc", {
        "profile": _profile()["profileId"],
        "apiVersion": ".".join(
            str(item) for item in _profile()["pandocApiVersion"]),
    })
    for entry in ast["blocks"]:
        constructor, content = _node_constructor(entry, "top-level block")
        block = ET.SubElement(pandoc, C + "block", {"constructor": constructor})
        if "c" in entry:
            _value_element(block, content)
    ET.indent(root, space="  ")
    body = ET.tostring(root, encoding="unicode", short_empty_elements=True)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n' + body + "\n").encode(
        "utf-8")


def _element_value(element: ET.Element) -> object:
    local = element.tag.rsplit("}", 1)[-1]
    if local == "null":
        return None
    if local == "boolean":
        return element.text in {"true", "1"}
    if local == "integer":
        return int(element.text)
    if local == "number":
        return float(element.text)
    if local == "string":
        return element.text or ""
    if local == "array":
        return [_element_value(child) for child in element]
    if local == "node":
        value = {"t": element.get("constructor")}
        children = list(element)
        if children:
            if len(children) != 1:
                raise StructuredSourceError("Pandoc XML node payload is not singular")
            value["c"] = _element_value(children[0])
        return value
    raise StructuredSourceError("authored XML contains an unknown value element")


def _decode_authored_root(root: ET.Element) -> tuple[str, dict]:
    identity = root.find(C + "documentIdentity")
    pandoc = root.find(C + "pandoc")
    if identity is None or pandoc is None:
        raise StructuredSourceError("authored XML omits identity or Pandoc content")
    document_id = identity.get("documentId", "")
    if _DOCUMENT_ID.fullmatch(document_id) is None:
        raise StructuredSourceError("authored XML document identity is invalid")
    blocks = []
    for block_element in pandoc.findall(C + "block"):
        block = {"t": block_element.get("constructor")}
        children = list(block_element)
        if children:
            if len(children) != 1:
                raise StructuredSourceError("authored XML block payload is not singular")
            block["c"] = _element_value(children[0])
        blocks.append(block)
    if not blocks:
        raise StructuredSourceError("authored XML contains no Pandoc blocks")
    return document_id, {
        "pandoc-api-version": _profile()["pandocApiVersion"],
        "meta": {},
        "blocks": blocks,
    }


def _root_fragments(root: ET.Element) -> tuple[dict[str, str], ...]:
    parent = root.find(C + "fragments")
    if parent is None:
        raise StructuredSourceError("authored XML omits the fragment index")
    records = []
    for fragment in parent.findall(C + "fragment"):
        excerpt = fragment.find(C + "excerpt")
        records.append({
            "id": fragment.get(XML_ID, ""),
            "presentationId": fragment.get("presentationId", ""),
            "bindingKind": fragment.get("bindingKind", ""),
            "semanticPath": fragment.get("semanticPath", ""),
            "bindingDigest": fragment.get("bindingDigest", ""),
            "excerpt": excerpt.text if excerpt is not None and excerpt.text else "",
        })
    return tuple(records)


def _validate_authored_root(root: ET.Element) -> None:
    """Recompute every fragment binding from the preserved Pandoc AST."""
    document_id, ast = _decode_authored_root(root)
    expected = _analyse_ast(ast, document_id)
    if _root_fragments(root) != expected.fragments:
        raise StructuredSourceError(
            "authored fragment index does not match the preserved Pandoc content")


def _document_from_xml(xml: bytes) -> tuple[object, str, dict, _Analysis]:
    artifact = parse_artifact(xml, "authored-document")
    document_id, ast = _decode_authored_root(artifact.root)
    return artifact, document_id, ast, _analyse_ast(ast, document_id)


def xml_to_pandoc_ast(xml: bytes) -> dict:
    """Decode current authored XML to its exact ordered Pandoc JSON model."""
    unused_artifact, unused_document_id, ast, unused_analysis = \
        _document_from_xml(xml)
    return ast


def _write_pandoc(ast: dict) -> bytes:
    payload = (json.dumps(
        ast, ensure_ascii=False, separators=(",", ":"), sort_keys=True) +
        "\n").encode("utf-8")
    markdown = _run_pandoc([
        "--from=json", "--to=" + _profile()["pandocWriter"], "--wrap=none"],
        payload)
    text = markdown.decode("utf-8")
    if "\r" in text:
        text = text.replace("\r\n", "\n").replace("\r", "\n")
    if not text.endswith("\n"):
        text += "\n"
    return unicodedata.normalize("NFC", text).encode("utf-8")


def xml_to_markdown(xml: bytes) -> bytes:
    """Back-render authored XML and prove ordered semantic AST equality."""
    unused_artifact, document_id, ast, expected = _document_from_xml(xml)
    markdown = _write_pandoc(ast)
    if _analyse_ast(_read_pandoc(markdown), document_id).semantic_model != \
            expected.semantic_model:
        raise StructuredSourceError(
            "authored XML back-render changed ordered Pandoc semantics")
    return markdown


def convert_authored_markdown(markdown: bytes, markdown_path: str,
                              document_id: str) -> AuthoredConversion:
    """Generate current XML and prove its semantic GFM round trip."""
    ast = _read_pandoc(markdown)
    analysis = _analyse_ast(ast, document_id)
    xml = _xml_bytes(ast, analysis, markdown, markdown_path, document_id)
    artifact, decoded_document_id, decoded_ast, decoded_analysis = \
        _document_from_xml(xml)
    if decoded_document_id != document_id or decoded_ast != ast or \
            decoded_analysis.semantic_model != analysis.semantic_model:
        raise StructuredSourceError(
            "authored XML changed the ordered Pandoc semantic model")
    generated = _write_pandoc(decoded_ast)
    if _analyse_ast(_read_pandoc(generated), document_id).semantic_model != \
            decoded_analysis.semantic_model:
        raise StructuredSourceError(
            "authored XML back-render changed ordered Pandoc semantics")
    return AuthoredConversion(
        xml=xml,
        markdown=generated,
        source_raw_digest=raw_digest(markdown),
        generated_markdown_raw_digest=raw_digest(generated),
        semantic_digest=artifact.semantic_digest,
        item_ids=tuple(item["id"] for item in analysis.fragments),
        fragment_digests=dict(artifact.fragment_digests),
    )
