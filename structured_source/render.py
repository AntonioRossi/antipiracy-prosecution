"""Deterministic GFM projections with in-memory coverage evidence."""

from __future__ import annotations

from collections.abc import Mapping
from contextvars import ContextVar
from dataclasses import dataclass
import posixpath
import re
from types import MappingProxyType
from urllib.parse import quote, urlsplit, urlunsplit
from xml.etree import ElementTree as ET

from . import CONTENT_NAMESPACE, RELATIONS_NAMESPACE
from .canonical import raw_digest
from .errors import StructuredSourceError
from .parser import ParsedArtifact
from .profiles import load_projection_profile

C = "{%s}" % CONTENT_NAMESPACE
R = "{%s}" % RELATIONS_NAMESPACE
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
_SAFE_ANCHOR = re.compile(r"[A-Za-z][A-Za-z0-9_.:-]*\Z")
_ACTIVE_PROFILE = ContextVar("structured_source_render_profile", default=None)


@dataclass(frozen=True, slots=True, init=False)
class Projection:
    """One projection whose computed coverage cannot be mutated in place."""

    markdown: bytes
    markdown_digest: str
    _coverage: Mapping

    def __init__(self, *, markdown, markdown_digest, coverage):
        object.__setattr__(self, "markdown", markdown)
        object.__setattr__(self, "markdown_digest", markdown_digest)
        object.__setattr__(self, "_coverage", _freeze_coverage(coverage))

    @property
    def coverage(self) -> dict:
        """Return detached coverage data, preserving the validated result."""
        return _copy_coverage(self._coverage)

    def _validated_coverage(self) -> Mapping:
        """Return frozen coverage to trusted validation implementation only."""
        return self._coverage


def _freeze_coverage(value):
    if isinstance(value, dict):
        return MappingProxyType({
            key: _freeze_coverage(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze_coverage(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze_coverage(item) for item in value)
    return value


def _copy_coverage(value):
    if isinstance(value, Mapping):
        return {key: _copy_coverage(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_copy_coverage(item) for item in value]
    return value


def _profile() -> dict:
    active = _ACTIVE_PROFILE.get()
    return active if active is not None else load_projection_profile()


def _anchor_line_pattern():
    return re.compile(
        r'<a id="%s[A-Za-z][A-Za-z0-9_.:-]*"></a>' %
        re.escape(_profile()["stableAnchorPrefix"]))


def _anchor_id_pattern():
    return re.compile(
        r'<a id="%s([A-Za-z][A-Za-z0-9_.:-]*)"></a>' %
        re.escape(_profile()["stableAnchorPrefix"]))


def _anchor(identifier: str) -> str:
    if not isinstance(identifier, str) or _SAFE_ANCHOR.fullmatch(identifier) is None:
        raise StructuredSourceError("fragment identity cannot form a stable review anchor")
    return _profile()["stableAnchorPrefix"] + identifier


def _anchor_element(identifier: str) -> str:
    return '<a id="%s"></a>' % _anchor(identifier)


def _escape_text(value: str) -> str:
    output = []
    for char in value:
        if char in "\\`*_{}[]<>#|~":
            output.append("\\")
        output.append(char)
    return "".join(output)


def _code(value: str) -> str:
    longest = max((len(match.group(0)) for match in re.finditer(r"`+", value)),
                  default=0)
    fence = "`" * max(1, longest + 1)
    padding = " " if value.startswith("`") or value.endswith("`") else ""
    return fence + padding + value + padding + fence


def _relative_target(target: str, output_path: str) -> str:
    try:
        parsed = urlsplit(target)
    except ValueError as exc:
        raise StructuredSourceError("projection link target is malformed") from exc
    if parsed.scheme in set(_profile()["externalSchemes"]):
        return urlunsplit((
            parsed.scheme, parsed.netloc,
            quote(parsed.path, safe="/%:@-._~"),
            quote(parsed.query, safe="=&-._~:%@/"),
            quote(parsed.fragment, safe="-._~:@/"),
        ))
    if parsed.scheme or parsed.netloc:
        raise StructuredSourceError("projection link target scheme is not registered")
    if not parsed.path and parsed.fragment:
        return "#" + quote(parsed.fragment, safe="-._~:@")
    if not parsed.path or parsed.path.startswith("/") or "\\" in parsed.path:
        raise StructuredSourceError("projection link target is not closed")
    normalized = posixpath.normpath(parsed.path)
    if normalized == ".." or normalized.startswith("../"):
        raise StructuredSourceError("projection link target escapes the repository")
    relative = posixpath.relpath(normalized, posixpath.dirname(output_path) or ".")
    return urlunsplit(("", "", quote(relative, safe="/-._~%"),
                       quote(parsed.query, safe="=&-._~:%"),
                       quote(parsed.fragment, safe="-._~:@")))


class _Renderer:
    def __init__(self, artifact: ParsedArtifact, output_path: str,
                 asset_paths: dict[str, str]):
        self.artifact = artifact
        self.output_path = output_path
        self.asset_paths = asset_paths
        self.lines: list[str] = []
        self.regions: dict[str, tuple[int, int]] = {}
        self.emitted_anchors: set[str] = set()

    def emit(self, *lines: str) -> None:
        self.lines.extend(lines)

    def mark(self, identifier: str, start: int) -> None:
        self.regions[identifier] = (start + 1, len(self.lines))

    def anchor_line(self, identifier: str | None) -> str | None:
        if not identifier:
            return None
        if identifier in self.emitted_anchors:
            raise StructuredSourceError("projection would emit a duplicate fragment anchor")
        self.emitted_anchors.add(identifier)
        return '<a id="%s"></a>' % _anchor(identifier)

    def inline(self, parent: ET.Element, link_label: bool = False) -> str:
        pieces = []
        for node in parent:
            local = node.tag.rsplit("}", 1)[-1]
            if local == "text":
                value = _escape_text(node.text or "")
                if link_label:
                    value = value.replace("@", "\\@").replace(".", "\\.")
                pieces.append(value)
            elif local == "space":
                pieces.append(" ")
            elif local == "softBreak":
                pieces.append("\n")
            elif local == "lineBreak":
                pieces.append("  \n")
            elif local in {"emphasis", "strong", "strikeout"}:
                marker = {"emphasis": "*", "strong": "**", "strikeout": "~~"}[local]
                pieces.extend((marker, self.inline(node, link_label), marker))
            elif local in {"superscript", "subscript"}:
                tag = "sup" if local == "superscript" else "sub"
                pieces.extend(("<%s>" % tag, self.inline(node, link_label), "</%s>" % tag))
            elif local == "definedTerm":
                pieces.extend(("**", self.inline(node, link_label), "**"))
            elif local == "quotation":
                pieces.extend(("“", self.inline(node, link_label), "”"))
            elif local == "reviewMark":
                if node.get("style") != "red":
                    raise StructuredSourceError("review mark style is not registered")
                pieces.extend(('<span style="color:red">', self.inline(node, link_label), "</span>"))
            elif local == "code":
                pieces.append(_code(node.text or ""))
            elif local == "math":
                pieces.extend(("$", node.text or "", "$"))
            elif local == "link":
                target = _relative_target(node.get("target"), self.output_path)
                title = ' "%s"' % node.get("title").replace('"', "\\\"") \
                    if node.get("title") else ""
                # GFM autolink recognition also runs inside explicit link
                # labels.  Escaping dot/@ prevents a URL or e-mail label from
                # becoming a nested link while preserving the visible text.
                label = self.inline(node, True)
                pieces.extend(("[", label, "](", target, title, ")"))
            elif local == "image":
                asset = self.asset_paths.get(node.get("assetId"))
                if asset is None:
                    raise StructuredSourceError(
                        "projection image asset is not registered: %s" % node.get("assetId"))
                target = _relative_target(asset, self.output_path)
                title = ' "%s"' % node.get("title").replace('"', "\\\"") \
                    if node.get("title") else ""
                pieces.extend(("![", _escape_text(node.get("alt")), "](",
                               target, title, ")"))
            elif local == "citation":
                pieces.extend(("[", self.inline(node, link_label), "]{#",
                               node.get("citationId"), "}"))
            elif local == "note":
                pieces.extend(("^[", self.inline_blocks(node, compact=True), "]"))
            else:
                raise StructuredSourceError("renderer has no inline rule for %s" % local)
        return "".join(pieces)

    def inline_blocks(self, parent: ET.Element, compact=False) -> str:
        rendered = []
        for block in parent:
            local = block.tag.rsplit("}", 1)[-1]
            if local not in {"paragraph", "plain"}:
                raise StructuredSourceError("inline note contains a non-inline block")
            rendered.append(self.inline(block))
        return ("; " if compact else "\n\n").join(rendered)

    def _render_table(self, table: ET.Element) -> list[str]:
        sections = []
        for section_name in ("head", "body"):
            section = table.find(C + section_name)
            if section is not None:
                sections.extend(section.findall(C + "row"))
        if not sections:
            raise StructuredSourceError("table has no rows")
        rows = []
        alignments = []
        width = None
        for row in sections:
            cells = []
            current_alignments = []
            for cell in row.findall(C + "cell"):
                blocks = []
                for block in cell:
                    local = block.tag.rsplit("}", 1)[-1]
                    if local not in {"paragraph", "plain"}:
                        raise StructuredSourceError(
                            "table cell contains a non-inline block")
                    anchor = self.anchor_line(block.get(XML_ID))
                    blocks.append(((anchor + " ") if anchor else "") +
                                  self.inline(block))
                text = "\n\n".join(blocks)
                text = text.replace("  \n", "<br>").replace("\n", "<br>")
                cells.append(text.replace("|", "\\|"))
                current_alignments.append(cell.get("alignment"))
            if width is None:
                width = len(cells)
                alignments = current_alignments
            if len(cells) != width:
                raise StructuredSourceError("table rows have inconsistent cell counts")
            rows.append(cells)
        separators = {
            "default": "---", "left": ":---", "center": ":---:",
            "right": "---:",
        }
        output = ["| " + " | ".join(rows[0]) + " |",
                  "| " + " | ".join(separators[item] for item in alignments) + " |"]
        output.extend("| " + " | ".join(row) + " |" for row in rows[1:])
        caption = table.find(C + "caption")
        if caption is not None:
            output.append("\n*%s*" % self.inline(caption))
        return output

    def block(self, node: ET.Element, indent="") -> list[str]:
        local = node.tag.rsplit("}", 1)[-1]
        identifier = node.get(XML_ID)
        anchor_line = self.anchor_line(identifier)
        output = [anchor_line] if anchor_line else []
        if local == "heading":
            # ATX headings end at a physical newline.  Preserve source soft
            # breaks as spaces and source hard breaks as an inline HTML break
            # so multiline OCR headings remain one heading in the GFM AST.
            heading = self.inline(node).replace("  \n", "<br>").replace("\n", " ")
            output.append("#" * int(node.get("level")) + " " + heading)
        elif local in {"paragraph", "plain"}:
            inline = self.inline(node)
            # Leading Markdown hard-break whitespace is discarded before a
            # paragraph starts.  Its closed HTML spelling remains an inline
            # break and preserves the typed leading LineBreak node.
            while inline.startswith("  \n"):
                inline = "<br>" + inline[3:]
            output.extend(inline.split("\n"))
        elif local == "codeBlock":
            value = node.text or ""
            longest = max((len(match.group(0)) for match in re.finditer(r"`+", value)),
                          default=0)
            fence = "`" * max(3, longest + 1)
            output.extend((fence + (node.get("language") or ""), value, fence))
        elif local == "blockQuotation":
            nested = self._blocks(node)
            output.extend(">" if not line else "> " + line for line in nested)
        elif local == "list":
            # A standalone HTML anchor before a list can change CommonMark
            # nesting.  Attach the list anchor to its first marker instead.
            output = []
            list_anchor = anchor_line
            ordered = node.get("ordered") == "true"
            number = int(node.get("start") or "1")
            delimiter = node.get("delimiter") or "period"
            for item_index, item in enumerate(node.findall(C + "item")):
                nested = self._blocks(item)
                item_anchor = self.anchor_line(item.get(XML_ID))
                leading = ([list_anchor] if item_index == 0 and list_anchor else [])
                if item_anchor:
                    leading.append(item_anchor)
                while nested and re.fullmatch(
                    _anchor_line_pattern(),
                        nested[0]):
                    leading.append(nested.pop(0))
                marker = (("%d. " if delimiter == "period" else "%d) ") % number
                          if ordered else _profile()["unorderedListMarker"] + " ")
                continuation = " " * max(4, len(marker))
                first_child = next(iter(item), None)
                if first_child is not None and first_child.tag == C + "list":
                    # A marker-only outer item is the CommonMark spelling for
                    # an item whose sole child is another list.  Putting an
                    # HTML anchor after that outer marker turns the nested
                    # marker into paragraph text, so carry the outer anchors
                    # onto the first nested marker instead.
                    output.append(marker.rstrip())
                    if leading and nested:
                        match = re.match(r"^([-+*] |\d+[.)] )(.*)$", nested[0])
                        if match is None:
                            raise StructuredSourceError(
                                "nested list projection has no first marker")
                        nested[0] = (match.group(1) + " ".join(leading) + " " +
                                     match.group(2)).rstrip()
                    output.extend(continuation + line for line in nested)
                    number += 1
                    continue
                first = nested.pop(0) if nested else ""
                output.append(marker + " ".join(leading + [first]).rstrip())
                output.extend(continuation + line for line in nested)
                number += 1
        elif local == "table":
            emitted_row_anchor = False
            for row in node.findall(".//" + C + "row"):
                row_anchor = self.anchor_line(row.get(XML_ID))
                if row_anchor:
                    output.append(row_anchor)
                    emitted_row_anchor = True
            if emitted_row_anchor:
                output.append("")
            output.extend(self._render_table(node))
        elif local == "claim":
            preamble = node.find(C + "preamble")
            limitations = node.findall(C + "limitation")
            preamble_text = self.inline(preamble)
            if preamble_text:
                output.append("**%s.** %s" % (node.get("number"), preamble_text))
            elif limitations:
                first = limitations.pop(0)
                limitation_anchor = self.anchor_line(first.get(XML_ID))
                output.append("**%s.** %s%s" % (
                    node.get("number"),
                    (limitation_anchor + " ") if limitation_anchor else "",
                    self.inline(first)))
            else:
                raise StructuredSourceError("claim has no review-visible limitation")
            for limitation in limitations:
                limitation_anchor = self.anchor_line(limitation.get(XML_ID))
                if limitation_anchor:
                    output.append(limitation_anchor)
                output.extend(("", self.inline(limitation)))
        elif local in {"noteBlock", "caution", "action"}:
            label = {"noteBlock": "Note", "caution": "Caution", "action": "Action"}[local]
            qualifiers = [node.get(field) for field in ("status", "owner") if node.get(field)]
            prefix = "**%s%s.** " % (label, " — " + " · ".join(qualifiers) if qualifiers else "")
            nested = self._blocks(node)
            if nested:
                output.append(prefix + nested[0])
                output.extend(nested[1:])
            else:
                output.append(prefix)
        elif local == "figure":
            asset = self.asset_paths.get(node.get("assetId"))
            if asset is None:
                raise StructuredSourceError("figure asset is not registered")
            caption = node.find(C + "caption")
            alt = node.get("alt")
            output.append("![%s](%s)" % (
                _escape_text(alt), _relative_target(asset, self.output_path)))
            if caption is not None:
                output.append("\n*%s*" % self.inline(caption))
        elif local == "division":
            output.extend(self._blocks(node))
        elif local == "separator":
            if anchor_line:
                output.append("")
            output.append("---")
        else:
            raise StructuredSourceError("renderer has no block rule for %s" % local)
        return [indent + line if line else "" for line in output]

    def _blocks(self, parent: ET.Element) -> list[str]:
        output = []
        for node in parent:
            block_lines = self.block(node)
            if output and output[-1] != "":
                output.append("")
            output.extend(block_lines)
        return output

    def _metadata(self, root: ET.Element, subject_id: str) -> None:
        identity = root.find(C + "documentIdentity")
        origin = root.find(C + "origin")
        self.emit(_anchor_element("review-metadata"),
                  "## Structured-source metadata", "",
                  "| Field | Current value |", "|---|---|")
        values = (
            ("Document ID", identity.get("documentId")),
            ("Artifact family", identity.get("artifactFamily")),
            ("Jurisdiction", identity.get("jurisdiction")),
            ("Scope", identity.get("scope")),
            ("Status", identity.get("status")),
            ("Language", identity.get("language")),
            ("Title", identity.findtext(C + "title")),
        )
        self.lines.extend("| %s | %s |" % (label, _escape_text(value))
                          for label, value in values)
        pdf = origin.find(C + "pdfDerivative")
        if pdf is None:
            raise StructuredSourceError(
                "PDF projection received a non-transcription XML artifact")
        self.emit("| Authority scheme | PDF evidence transcription |")
        self.emit("")

        dependencies = root.find(C + "dependencies")
        self.emit(_anchor_element("review-dependencies"),
                  "## Dependencies", "",
                  "| Kind | Subject | Exact binding digest |", "|---|---|---|")
        entries = dependencies.findall(C + "dependency")
        if entries:
            for item in entries:
                digest = item.get("digest")
                self.emit("| %s | %s | %s |" % (
                    item.get("kind"), item.get("subjectId"),
                    ("`%s`" % digest) if digest else "—"))
        else:
            self.emit("| None | — | — |")
        self.emit("")

        provenance = root.find(C + "provenance")
        self.emit(_anchor_element("review-provenance"),
                  "## Provenance", "",
                  "| Fragment | Stored source | Page | Region | Uncertainty |",
                  "|---|---|---:|---|---|")
        evidence = provenance.findall(C + "fragmentEvidence")
        if evidence:
            for item in evidence:
                self.emit("| [%s](#%s) | %s | %s | %s | %s |" % (
                    item.get("fragmentId"), _anchor(item.get("fragmentId")),
                    _escape_text(item.get("sourcePath")), item.get("page"),
                    _escape_text(item.get("region") or "—"),
                    _escape_text(item.get("uncertainty") or "None declared")))
        else:
            self.emit("| None | — | — | — | — |")
        self.emit("")

    def render_content(self) -> bytes:
        root = self.artifact._validated_root()
        identity = root.find(C + "documentIdentity")
        subject = identity.get("documentId")
        notice = (
            "<!-- GENERATED REVIEW PROJECTION — source %s; byte digest %s; "
            "source profile %s; projection profile %s/%s; regenerate with "
            "`uv --no-cache --offline run --locked "
            "--no-sync python -m structured_source regenerate %s`; edit the XML source, "
            "never this Markdown. -->" %
            (subject, self.artifact.raw_digest, self.artifact.profile,
             _profile()["profileId"], _profile()["generatedNoticeVersion"], subject))
        self.emit(notice, self.anchor_line(root.get(XML_ID)), "")
        content = root.find(C + "content")
        for node in content:
            start = len(self.lines)
            if self.lines and self.lines[-1] != "":
                self.emit("")
            self.lines.extend(self.block(node))
            for identified in node.iter():
                identifier = identified.get(XML_ID)
                if identifier:
                    self.mark(identifier, start)
        self.emit("")
        self._metadata(root, subject)
        return ("\n".join(self.lines).rstrip() + "\n").encode("utf-8")


def _typed_field_census(root: ET.Element, regions: dict[str, tuple[int, int]],
                        subject_id: str) -> list[dict]:
    fields = []
    sequence = 0

    def visit(node: ET.Element, nearest_fragment: str | None,
              plane: str) -> None:
        nonlocal sequence
        sequence += 1
        fragment = node.get(XML_ID) or nearest_fragment
        local = node.tag.rsplit("}", 1)[-1]
        node_ref = "%s:n%d:%s" % (subject_id, sequence, local)
        if plane in {"content", "document"} and fragment:
            classification = "review-visible"
            anchors = [_anchor(fragment)] if fragment else []
            line_regions = ([{"startLine": regions[fragment][0],
                              "endLine": regions[fragment][1]}]
                            if fragment in regions else [])
        elif plane == "content":
            classification = "mechanically-derived"
            anchors = []
            line_regions = []
        elif plane in {"dependencies", "provenance", "metadata"}:
            classification = "review-scheduled"
            region_id = {
                "dependencies": "review-dependencies",
                "provenance": "review-provenance",
                "metadata": "review-metadata",
            }[plane]
            anchor_name = _anchor(region_id)
            anchors = [anchor_name]
            line_regions = [{"startLine": regions[region_id][0],
                             "endLine": regions[region_id][1]}]
        elif plane == "projection":
            classification = "mechanically-derived"
            anchors = []
            line_regions = [{"startLine": 1, "endLine": 1}]
        else:
            classification = "internal-justified"
            anchors = []
            line_regions = []
        fields.append({
            "fieldId": node_ref + ":element",
            "origin": {"subjectId": subject_id, "nodeRef": node_ref,
                       "field": "element"},
            "classification": classification,
            "anchors": anchors,
            "regions": line_regions,
            **({"derivationId": "gfm-v1-structure"}
               if classification == "mechanically-derived" else {}),
            **({"justification": "schema-envelope-control"}
               if classification == "internal-justified" else {}),
        })
        for name in sorted(node.attrib):
            fields.append({
                "fieldId": node_ref + ":attribute:" + name.rsplit("}", 1)[-1],
                "origin": {"subjectId": subject_id, "nodeRef": node_ref,
                           "field": "attribute:" + name.rsplit("}", 1)[-1]},
                "classification": classification,
                "anchors": anchors,
                "regions": line_regions,
                **({"derivationId": "gfm-v1-structure"}
                   if classification == "mechanically-derived" else {}),
                **({"justification": "schema-envelope-control"}
                   if classification == "internal-justified" else {}),
            })
        if node.text is not None:
            fields.append({
                "fieldId": node_ref + ":text",
                "origin": {"subjectId": subject_id, "nodeRef": node_ref,
                           "field": "text"},
                "classification": classification,
                "anchors": anchors,
                "regions": line_regions,
                **({"derivationId": "gfm-v1-structure"}
                   if classification == "mechanically-derived" else {}),
                **({"justification": "schema-envelope-control"}
                   if classification == "internal-justified" else {}),
            })
        for child in node:
            child_local = child.tag.rsplit("}", 1)[-1]
            child_plane = plane
            if node is root:
                child_plane = {
                    "documentIdentity": "metadata", "origin": "metadata",
                    "dependencies": "dependencies", "provenance": "provenance",
                    "content": "content", "projectionPolicy": "projection",
                }.get(child_local, "internal")
            visit(child, None if node is root else fragment, child_plane)

    visit(root, root.get(XML_ID), "document")
    return fields


def _render_content(artifact: ParsedArtifact, output_path: str,
                    asset_paths: dict[str, str] | None = None) -> Projection:
    if artifact.kind != "content-document":
        raise StructuredSourceError("content renderer received a non-content artifact")
    renderer = _Renderer(artifact, output_path, asset_paths or {})
    markdown = renderer.render_content()
    markdown_lines = markdown.decode("utf-8").splitlines()
    anchor_lines = {}
    for line_number, line in enumerate(markdown_lines, start=1):
        for match in _anchor_id_pattern().finditer(line):
            identifier = match.group(1)
            if identifier in anchor_lines:
                raise StructuredSourceError(
                    "projection coverage anchor is duplicated")
            anchor_lines[identifier] = line_number
    review_lines = {}
    for identifier in ("review-metadata", "review-dependencies",
                       "review-provenance"):
        anchor = _anchor_element(identifier)
        positions = [index for index, line in enumerate(markdown_lines, start=1)
                     if line == anchor]
        if len(positions) != 1:
            raise StructuredSourceError(
                "projection review section anchor is not exact")
        review_lines[identifier] = positions[0]
    coverage_regions = {
        "review-metadata": (
            review_lines["review-metadata"],
            review_lines["review-dependencies"] - 1),
        "review-dependencies": (
            review_lines["review-dependencies"],
            review_lines["review-provenance"] - 1),
        "review-provenance": (
            review_lines["review-provenance"], len(markdown_lines)),
    }
    root = artifact._validated_root()
    content = root.find(C + "content")
    top_level = list(content)
    top_ids = [node.get(XML_ID) for node in top_level]
    try:
        starts = [anchor_lines[item_id] for item_id in top_ids]
    except KeyError as exc:
        raise StructuredSourceError(
            "projection coverage top-level anchor is absent") from exc
    if starts != sorted(set(starts)) or \
            (starts and starts[-1] >= review_lines["review-metadata"]):
        raise StructuredSourceError(
            "projection coverage block order is not exact")
    ends = [*([start - 1 for start in starts[1:]]),
            review_lines["review-metadata"] - 1]
    for node, start, end in zip(top_level, starts, ends):
        region = (start, end)
        for descendant in node.iter():
            item_id = descendant.get(XML_ID)
            if item_id:
                coverage_regions[item_id] = region
    root_id = root.get(XML_ID)
    if root_id not in anchor_lines:
        raise StructuredSourceError(
            "projection coverage document-item anchor is absent")
    coverage_regions[root_id] = (
        anchor_lines[root_id], review_lines["review-metadata"] - 1)
    identity = root.find(C + "documentIdentity")
    subject = identity.get("documentId")
    coverage_value = {
        "coverageVersion": "1",
        "subjectId": subject,
        "sourceRawDigest": artifact.raw_digest,
        "sourceProfile": artifact.profile,
        "projectionProfile": _profile()["profileId"],
        "markdownDigest": raw_digest(markdown),
        "fields": _typed_field_census(
            root, coverage_regions, subject),
    }
    return Projection(
        markdown=markdown,
        markdown_digest=raw_digest(markdown),
        coverage=coverage_value,
    )


def _render_relations(artifact: ParsedArtifact, output_path: str,
                      endpoint_views: dict[tuple[str, str, str], object]) -> Projection:
    """Render one relation owner and current endpoint excerpts mechanically."""
    if artifact.kind != "relation-set":
        raise StructuredSourceError("relation renderer received a non-relation artifact")
    renderer = _Renderer(artifact, output_path, {})
    root = artifact._validated_root()
    identity = root.find(R + "identity")
    subject = identity.get("relationSetId")
    renderer.emit(
        "<!-- GENERATED RELATION REVIEW PROJECTION — relation set %s; byte digest %s; "
        "source profile %s; projection profile %s/%s; regenerate with "
        "`uv --no-cache --offline run --locked "
        "--no-sync python -m structured_source regenerate %s`; edit the relation XML, "
        "never this Markdown. -->" %
        (subject, artifact.raw_digest, artifact.profile,
         _profile()["profileId"], _profile()["generatedNoticeVersion"], subject), "",
        _anchor_element("relation-metadata"),
        "# Relation-set review metadata", "",
        "| Field | Current value |", "|---|---|",
        "| Relation-set ID | %s |" % subject,
        "| Profile | %s |" % identity.get("profile"),
        "| Semantic owner | %s |" % _escape_text(identity.get("owner")),
        "| Scope | %s |" % identity.get("scope"),
        "| Status | %s |" % identity.get("status"), "")

    relation_regions = {}
    renderer.emit(_anchor_element("relation-schedule"),
                  "# Exact relations", "")
    for relation in root.findall(R + "relation"):
        start = len(renderer.lines)
        xml_id = relation.get(XML_ID)
        relation_id = relation.get("relationId")
        renderer.emit(renderer.anchor_line(xml_id),
                      "## %s" % _escape_text(relation_id), "",
                      "| Field | Current value |", "|---|---|",
                      "| Type | %s |" % relation.get("type"),
                      "| Direction | %s |" % relation.get("direction"),
                      "| Semantic owner | %s |" % _escape_text(relation.get("semanticOwner")),
                      "", "### Exact endpoints", "",
                      "| Role | Document | Fragment | Fragment digest | Current excerpt |",
                      "|---|---|---|---|---|")
        for endpoint in relation.findall(R + "endpoint"):
            key = (endpoint.get("documentId"), endpoint.get("fragmentId"),
                   endpoint.get("fragmentContentDigest"))
            if key not in endpoint_views:
                raise StructuredSourceError(
                    "relation endpoint excerpt did not resolve exactly: %s" % (key,))
            view = endpoint_views[key]
            if isinstance(view, str):
                excerpt = view
                target = "#" + _anchor(endpoint.get("fragmentId"))
            elif isinstance(view, dict) and set(view) == {"excerpt", "markdownPath"}:
                excerpt = view["excerpt"]
                target = (_relative_target(view["markdownPath"], output_path) +
                          "#" + _anchor(endpoint.get("fragmentId")))
            else:
                raise StructuredSourceError("relation endpoint view is malformed")
            excerpt = excerpt.replace("\n", " ")
            renderer.emit("| %s | %s | [%s](%s) | `%s` | %s |" % (
                endpoint.get("role"), endpoint.get("documentId"),
                endpoint.get("fragmentId"), target,
                endpoint.get("fragmentContentDigest"), _escape_text(excerpt)))
        renderer.emit("", "### Assertion fields", "",
                      "| Field | Current value |", "|---|---|")
        for field in relation.findall(R + "assertionField"):
            renderer.emit("| %s | %s |" % (
                field.get("name"), _escape_text(field.text or "")))
        renderer.emit("")
        # The separator blank is layout between relations, not assertion
        # content; canonical final trimming removes it for the last relation.
        relation_regions[xml_id] = (start + 1, len(renderer.lines) - 1)
    markdown = ("\n".join(renderer.lines).rstrip() + "\n").encode("utf-8")

    fields = []
    sequence = 0

    def census(node, plane, nearest):
        nonlocal sequence
        sequence += 1
        local = node.tag.rsplit("}", 1)[-1]
        identifier = node.get(XML_ID) or nearest
        node_ref = "%s:n%d:%s" % (subject, sequence, local)
        if plane == "relation" and identifier:
            classification = "review-scheduled"
            anchors = [_anchor(identifier)]
            region = relation_regions.get(identifier)
        elif plane == "identity":
            classification = "review-scheduled"
            anchors = [_anchor("relation-metadata")]
            region = None
        else:
            classification = "internal-justified"
            anchors = []
            region = None
        common = {
            "origin": {"subjectId": subject, "nodeRef": node_ref},
            "classification": classification, "anchors": anchors,
            "regions": ([{"startLine": region[0], "endLine": region[1]}]
                        if region else []),
        }
        if classification == "internal-justified":
            common["justification"] = "schema-envelope-control"
        for field_name in ["element"] + [
                "attribute:" + name.rsplit("}", 1)[-1]
                for name in sorted(node.attrib)] + \
                (["text"] if node.text is not None else []):
            entry = dict(common)
            entry["fieldId"] = node_ref + ":" + field_name
            entry["origin"] = {**common["origin"], "field": field_name}
            fields.append(entry)
        for child in node:
            child_local = child.tag.rsplit("}", 1)[-1]
            child_plane = plane
            if node is root:
                child_plane = {"identity": "identity",
                               "relation": "relation"}.get(child_local, "internal")
            census(child, child_plane, identifier)

    census(root, "internal", None)
    coverage_value = {
        "coverageVersion": "1", "subjectId": subject,
        "sourceRawDigest": artifact.raw_digest,
        "sourceProfile": artifact.profile,
        "projectionProfile": _profile()["profileId"],
        "markdownDigest": raw_digest(markdown), "fields": fields,
    }
    return Projection(markdown=markdown, markdown_digest=raw_digest(markdown),
                      coverage=coverage_value)


def render_content(artifact: ParsedArtifact, output_path: str,
                   asset_paths: dict[str, str] | None = None, *,
                   projection_profile=None) -> Projection:
    """Render with the retained projection profile when one is supplied."""
    profile = projection_profile or load_projection_profile()
    if not isinstance(profile, Mapping):
        raise StructuredSourceError("renderer projection profile is malformed")
    token = _ACTIVE_PROFILE.set(profile)
    try:
        return _render_content(artifact, output_path, asset_paths)
    finally:
        _ACTIVE_PROFILE.reset(token)


def render_relations(artifact: ParsedArtifact, output_path: str,
                     endpoint_views: dict[tuple[str, str, str], object], *,
                     projection_profile=None) -> Projection:
    """Render relations with the retained projection profile when supplied."""
    profile = projection_profile or load_projection_profile()
    if not isinstance(profile, Mapping):
        raise StructuredSourceError("renderer projection profile is malformed")
    token = _ACTIVE_PROFILE.set(profile)
    try:
        return _render_relations(artifact, output_path, endpoint_views)
    finally:
        _ACTIVE_PROFILE.reset(token)
