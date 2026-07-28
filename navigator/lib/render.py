"""Deterministic self-contained HTML5 renderer for an immutable EditionModel.

The renderer has one semantic input: the typed model.  It does not open source
files, parse an authority format, repair relations, or maintain a second view
of content.  Static interface copy is kept in :data:`UI`; controlled legal,
status, caution, disposition, profile, and provenance wording is resolved by
``EditionModel.controlled_text`` before any HTML is emitted.
"""

from __future__ import annotations

import base64
import html
import json
from types import MappingProxyType


EXACT_CSP = (
    "default-src 'none'; img-src data:; style-src 'unsafe-inline'; "
    "script-src 'unsafe-inline'; base-uri 'none'; form-action 'none'; "
    "object-src 'none'; connect-src 'none'"
)
FORBIDDEN_SCRIPT_TOKENS = (
    "fetch(", "XMLHttpRequest", "WebSocket", "EventSource",
    "navigator.sendBeacon", "localStorage", "sessionStorage",
    "document.cookie", "history.", "location.",
)

# This is the sole ordinary-interface wording inventory.  Semantic wording is
# intentionally absent and must come from model.controlled_text().
UI = MappingProxyType({
    "about": "About and provenance",
    "aboutScheduleToggle": "Mappings and about",
    "authoritySchemeHeader": "Authority direction",
    "candidateClaimsLabel": "Candidate claims",
    "cautionPresent": "caution present",
    "claimGateAnnouncement": "{prefix} claim {number} claim-level gate",
    "claimGateContext": "{prefix} claim {number} — claim-level gate",
    "claimIndex": "Claim index",
    "claimReference": "{prefix} claim {number}",
    "claimSetLabel": "Claim set",
    "clearSelection": "Clear selection",
    "completeSchedule": "Complete mapping schedule",
    "compositeJoin": " + ",
    "forwardMode": "Claims → Specification",
    "gateHeader": "Gate",
    "gatePresent": "claim-level gate present",
    "goToClaim": "Go to {prefix} claim {number}",
    "limitationLabel": "limitation {number}",
    "machineData": "Machine-readable navigation and provenance data",
    "mappingCautions": "Cautions and dispositions",
    "mappingStatus": "Recording state",
    "next": "Next",
    "position": "{position} of {total} — {label}",
    "preambleLabel": "preamble",
    "previous": "Previous",
    "provenanceDocument": "Source document",
    "provenanceDigest": "XML byte digest",
    "provenanceRelationSet": "Relation set",
    "reverseBadge": "Show {count} related claim fragments for {label}",
    "reverseCounts": "{fragments} fragments across {claims} claims",
    "reverseMode": "Specification → Claims",
    "scheduleClaimGates": "Claim-level gates",
    "scheduleDisposition": "Disposition",
    "scheduleFragment": "Claim fragment",
    "scheduleTargets": "All recorded candidates",
    "selectionCleared": "Selection cleared",
    "showCandidates": "Show recorded candidates for {label}",
    "showRecordingState": "Show mapping state for {label}: {status}",
    "sourcePathHeader": "Registered source",
    "xmlRoleHeader": "XML interface role",
    "unitContext": "{claim}, {unit}",
    "phraseContext": "{claim}, phrase “{text}”",
})

PRIOR_UI = MappingProxyType({
    "candidatePosition": "Candidate {position} of {total} — {label}",
    "claimObligationSummary": (
        "Claim-level matrix obligations: {mapped} mapped · {review} review required · "
        "{noMaterial} no-material"),
    "exactCandidateCount": "Exact candidates for this fragment: {count}",
    "fullReader": "Full asserted XML transcription",
    "matrixObligations": "Matrix claim/document obligations",
    "noExactPassage": (
        "No exact candidate passage from this document is recorded for a "
        "passage-mapped obligation."),
    "nextCandidate": "Next candidate",
    "nextPassage": "Next passage in candidate",
    "openFullReader": "Open full transcription at this passage",
    "passagePosition": "Passage {position} of {total} — {label}",
    "previousCandidate": "Previous candidate",
    "previousPassage": "Previous passage in candidate",
    "reviewAllocationCount": "Review-required allocations for this fragment: {count}",
    "reverseCounts": "{fragments} candidates across {claims} claims",
    "scheduleTargets": "Candidates and fragment-review allocations",
})

_ROLE_RANK = {"specific": 0, "combination": 1, "context": 2}
_CELL_ALIGNMENT = {
    "default": "cell-align-default",
    "left": "cell-align-left",
    "center": "cell-align-center",
    "right": "cell-align-right",
}
_GENERALIZATION_WORDING = {
    "beyond-literal-example": "generalization-beyond-literal-example",
}


class RenderError(ValueError):
    """Raised when a typed model cannot satisfy the closed render contract."""


def _esc(value) -> str:
    return html.escape(str(value), quote=True)


def _fmt(template: str, **values) -> str:
    result = template
    for key, value in values.items():
        token = "{%s}" % key
        if result.count(token) != 1:
            raise RenderError("UI template slot is absent or duplicated: %s" % key)
        result = result.replace(token, str(value))
    if "{" in result or "}" in result:
        raise RenderError("UI template retains an unresolved slot")
    return result


def _script_json(value) -> str:
    """Serialize data for an application/json script element, inertly."""
    return (json.dumps(value, ensure_ascii=False, separators=(",", ":"),
                       sort_keys=True)
            .replace("&", "\\u0026")
            .replace("<", "\\u003c")
            .replace(">", "\\u003e")
            .replace(chr(0x2028), "\\u2028")
            .replace(chr(0x2029), "\\u2029"))


def _control_id(model, relation_id: str) -> str:
    return "control-" + model.dom_id(model.relation_set_id, relation_id)


def _claim_key(number: int) -> str:
    return "claim-%d" % number


def _claim_label(model, number: int) -> str:
    return _fmt(UI["claimReference"], prefix=model.strategy_prefix,
                number=number)


def _unit_label(unit) -> str:
    if unit.unit_kind == "preamble":
        return UI["preambleLabel"]
    return _fmt(UI["limitationLabel"], number=unit.unit_index)


def _unit_context(model, unit) -> str:
    return _fmt(UI["unitContext"],
                claim=_claim_label(model, unit.claim_number),
                unit=_unit_label(unit))


def _phrase_context(model, phrase, unit) -> str:
    return _fmt(UI["phraseContext"],
                claim=_claim_label(model, unit.claim_number),
                text=phrase.exact_text)


def _anchor_label(fragment_id: str) -> str:
    """Return a concise display aid; identity remains the model DOM locator."""
    tail = fragment_id.rsplit("-", 1)[-1]
    kinds = (
        ("table-row-", "R"), ("list-item-", "L"),
        ("codeblock-", "C"), ("blockquote-", "Q"),
        ("horizontalrule-", "§"), ("header-", "H"),
        ("table-", "T"), ("para-", "P"), ("plain-", "I"),
    )
    lowered = fragment_id.casefold()
    for marker, prefix in kinds:
        if marker in lowered:
            return prefix + tail
    return tail


def _wording(model, wording_id: str) -> str:
    try:
        return model.controlled_text(wording_id)
    except Exception as exc:
        raise RenderError("controlled wording does not resolve: %s" % wording_id) from exc


def _gate_view(model, gate) -> dict:
    try:
        source = model.get_item(gate.source.document_id, gate.source.fragment_id)
        quote = source.text
    except Exception as exc:
        raise RenderError("gate source does not resolve through the model") from exc
    return {
        "gateId": gate.gate_id,
        "code": gate.code,
        "name": _wording(
            model, "gate-label-%s-%s" % (model.edition_id, gate.code)),
        "scope": _wording(model, "caution-scope-" + gate.required_scope),
        "typeLabel": _wording(model, "caution-type-source-gate"),
        "quote": quote,
    }


def _caution_view(model, caution, scope: str) -> dict | None:
    if caution is None:
        return None
    if caution.kind == "source-gate":
        gate = model.gates_by_id.get(caution.gate_id)
        if gate is None or caution.code is not None:
            raise RenderError("source-gate caution has no exact gate definition")
        view = _gate_view(model, gate)
        view["scope"] = _wording(model, "caution-scope-" + scope)
        return view
    if caution.kind == "generalization-note":
        wording_id = _GENERALIZATION_WORDING.get(caution.code)
        if wording_id is None or caution.gate_id is not None:
            raise RenderError("generalization caution code is not closed")
        return {
            "gateId": None,
            "code": caution.code,
            "name": _wording(model, wording_id),
            "scope": _wording(model, "caution-scope-" + scope),
            "typeLabel": _wording(model, "caution-type-generalization-note"),
            "quote": _wording(model, wording_id),
        }
    raise RenderError("unsupported caution kind")


def _disposition_view(model, disposition) -> dict:
    return {
        "gateId": disposition.gate_id,
        "value": disposition.value,
        "text": _wording(model, "gate-disposition-" + disposition.value),
    }


def _target_view(model, target, candidate=None) -> dict:
    if target.role not in _ROLE_RANK or not isinstance(target.note, str) or \
            not target.note.strip():
        raise RenderError("target role and descriptive note are not exact")
    endpoint_ids = tuple(
        model.dom_id(endpoint.document_id, endpoint.fragment_id)
        for endpoint in target.endpoints)
    if not endpoint_ids:
        raise RenderError("target is empty")
    labels = tuple(
        ((endpoint.document_id.removeprefix("us-prior-art-").upper() + " · ")
         if model.product_kind == "prior-art" else "") +
        _anchor_label(endpoint.fragment_id)
        for endpoint in target.endpoints)
    value = {
        "role": target.role,
        "roleLabel": _wording(model, "mapping-role-" + target.role),
        "blocks": list(endpoint_ids),
        "labels": list(labels),
        "label": UI["compositeJoin"].join(labels),
        "note": target.note,
        "caution": _caution_view(model, target.caution, "target"),
    }
    if candidate is not None:
        value["candidateId"] = candidate.relation_id
        value["obligationIds"] = list(candidate.obligation_ids)
    return value


def _sorted_target_views(model, targets) -> list[dict]:
    if any(target.role not in _ROLE_RANK for target in targets):
        raise RenderError("target role is outside the closed rank")
    ranked = sorted(enumerate(targets),
                    key=lambda pair: (_ROLE_RANK[pair[1].role], pair[0]))
    return [_target_view(model, target)
            for _, target in ranked]


def _sorted_candidate_views(model, candidates) -> list[dict]:
    ranked = sorted(candidates, key=lambda candidate: (
        _ROLE_RANK[candidate.targets[0].role],
        tuple((endpoint.document_id, endpoint.fragment_id)
              for endpoint in candidate.targets[0].endpoints),
        candidate.relation_id))
    return [_target_view(model, candidate.targets[0], candidate)
            for candidate in ranked]


def _review_allocation_views(model, fragment_id) -> list[dict]:
    return [{
        "allocationId": item.relation_id,
        "obligationIds": list(item.obligation_ids),
        "note": item.relevance_note,
    } for item in model.review_allocations_by_unit.get(fragment_id, ())]


def _relation_data(model) -> tuple[dict, dict, dict]:
    """Compute render relations, reverse links, gates, and dispositions."""
    claim_document_id = model.source_documents[0].document_id
    relations = {}

    for mapping in model.relations.mappings:
        unit = model.units_by_fragment[mapping.subject.fragment_id]
        relation_id = mapping.relation_id
        if relation_id in relations:
            raise RenderError("duplicate relation identity")
        source_dom = model.dom_id(claim_document_id, unit.fragment_id)
        dispositions = tuple(model.dispositions_by_subject.get(
            ("claim-unit", unit.fragment_id), ()))
        targets = (_sorted_candidate_views(
            model, model.candidates_by_unit.get(unit.fragment_id, ()))
            if model.product_kind == "prior-art" else
            _sorted_target_views(model, mapping.targets))
        relations[relation_id] = {
            "relationId": relation_id,
            "kind": "unit",
            "status": mapping.status,
            "statusLabel": _wording(model, "mapping-status-" + mapping.status),
            "claimKey": _claim_key(unit.claim_number),
            "subjectDomId": source_dom,
            "subjectControlId": _control_id(model, relation_id),
            "subjectLabel": _unit_context(model, unit),
            "targets": targets,
            "reviewAllocations": (_review_allocation_views(
                model, unit.fragment_id)
                if model.product_kind == "prior-art" else []),
            "caution": _caution_view(model, mapping.caution, "fragment"),
            "dispositions": [
                _disposition_view(model, item) for item in dispositions],
        }

    for phrase in model.relations.phrase_mappings:
        unit = model.units_by_fragment[phrase.parent.fragment_id]
        relation_id = phrase.relation_id
        if relation_id in relations:
            raise RenderError("duplicate relation identity")
        candidate = (model.candidates_by_id.get(relation_id)
                     if model.product_kind == "prior-art" else None)
        targets = ([_target_view(model, candidate.targets[0], candidate)]
                   if candidate is not None else
                   _sorted_target_views(model, phrase.targets))
        relations[relation_id] = {
            "relationId": relation_id,
            "kind": "phrase",
            "status": "mapped",
            "statusLabel": _wording(model, "mapping-status-mapped"),
            "claimKey": _claim_key(unit.claim_number),
            "subjectDomId": _control_id(model, relation_id),
            "subjectControlId": _control_id(model, relation_id),
            "subjectLabel": _phrase_context(model, phrase, unit),
            "targets": targets,
            "reviewAllocations": [],
            "caution": None,
            "dispositions": [],
        }

    reverse = {}
    for relation_id, relation in relations.items():
        for candidate_index, candidate in enumerate(relation["targets"]):
            for block_id in candidate["blocks"]:
                reverse.setdefault(block_id, []).append({
                    "relationId": relation_id,
                    "candidateIndex": candidate_index,
                    "candidateId": candidate.get("candidateId", relation_id),
                })

    claim_gates = {}
    for disposition in model.relations.dispositions:
        if disposition.subject_kind != "claim":
            continue
        gate = model.gates_by_id.get(disposition.gate_id)
        if gate is None:
            raise RenderError("disposition gate does not resolve")
        item = {
            "gate": _gate_view(model, gate),
            "disposition": _disposition_view(model, disposition),
        }
        claim_number = int(disposition.subject.fragment_id.rsplit("-", 1)[1])
        claim_gates.setdefault(_claim_key(claim_number), []).append(item)
    return relations, reverse, claim_gates


def _relation_aria(relation: dict) -> str:
    if relation["status"] == "mapped":
        return _fmt(UI["showCandidates"], label=relation["subjectLabel"])
    return _fmt(UI["showRecordingState"],
                label=relation["subjectLabel"],
                status=relation["statusLabel"])


def _unit_text_html(model, unit, phrases, relations) -> str:
    spans = []
    for phrase in phrases:
        if phrase.start < 0 or phrase.end > len(unit.text) or \
                phrase.start >= phrase.end:
            raise RenderError("phrase span is outside its typed unit")
        spans.append((phrase.start, phrase.end, phrase))
    spans.sort(key=lambda item: (item[0], item[1], item[2].relation_id))
    prior_end = 0
    output = []
    for start, end, phrase in spans:
        if start < prior_end:
            raise RenderError("phrase render spans overlap")
        output.append(_esc(unit.text[prior_end:start]))
        relation = relations[phrase.relation_id]
        output.append(
            '<button type="button" class="phrase-btn" id="%s" '
            'data-relation="%s" aria-label="%s">%s</button>' % (
                _esc(relation["subjectControlId"]),
                _esc(phrase.relation_id), _esc(_relation_aria(relation)),
                _esc(unit.text[start:end])))
        prior_end = end
    output.append(_esc(unit.text[prior_end:]))
    return "".join(output)


def _claims_html(model, relations, claim_gates) -> str:
    claims_by_group = {name: tuple(numbers)
                       for name, numbers in model.claim_groups}
    if tuple(claims_by_group) != tuple(name for name, _ in model.claim_groups):
        raise RenderError("claim groups are duplicated")
    chips = []
    sections = []
    independent = set(model.independent_claims)
    for group_name, numbers in claims_by_group.items():
        chips.append('<span class="chip-group"><span class="chip-group-name">%s</span>'
                     % _esc(group_name))
        for number in numbers:
            css = "chip chip-independent" if number in independent else "chip"
            chips.append(
                '<button type="button" class="%s" data-goto="claim-view-%d" '
                'aria-label="%s">%d</button>' % (
                    css, number, _esc(_fmt(UI["goToClaim"],
                        prefix=model.strategy_prefix, number=number)), number))
        chips.append("</span>")

        body = ['<section class="claim-group"><h2>%s</h2>' % _esc(group_name)]
        for number in numbers:
            claim = model.claims_by_number[number]
            gates = claim_gates.get(_claim_key(number), ())
            gate_html = "".join(
                '<button type="button" class="gate-chip" id="gate-control-%s-%d" '
                'data-gate="%s" data-claim="%s" aria-label="%s">⚑ %s</button>'
                % (_esc(item["gate"]["gateId"]), number,
                   _esc(item["gate"]["gateId"]), _claim_key(number),
                   _esc(_fmt(UI["claimGateAnnouncement"],
                       prefix=model.strategy_prefix, number=number)),
                   _esc(item["gate"]["name"]))
                for item in gates)
            independent_class = " claim-independent" if number in independent else ""
            body.append(
                '<article class="claim%s" id="claim-view-%d">'
                '<header class="claim-header"><span class="claim-no">%s</span>%s'
                '</header>' % (independent_class, number,
                               _esc(_claim_label(model, number)), gate_html))
            for unit in claim.units:
                mappings = model.mappings_by_unit.get(unit.fragment_id, ())
                if len(mappings) != 1:
                    raise RenderError("claim unit does not have exactly one mapping")
                mapping = mappings[0]
                relation = relations[mapping.relation_id]
                phrases = model.phrases_by_unit.get(unit.fragment_id, ())
                marker = ""
                if relation["status"] != "mapped":
                    marker = '<p class="state-note" role="note">◇ %s</p>' % \
                        _esc(relation["statusLabel"])
                body.append(
                    '<div class="unit state-%s" id="%s" data-fragment="%s">'
                    '<button type="button" class="unit-btn" id="%s" '
                    'data-relation="%s" aria-label="%s"></button>'
                    '<div class="unit-body"><span class="unit-label">%s</span>'
                    '<span class="pointer-surface" data-relation="%s">%s</span>%s'
                    '</div></div>' % (
                        _esc(relation["status"]),
                        _esc(relation["subjectDomId"]),
                        _esc(unit.fragment_id),
                        _esc(relation["subjectControlId"]),
                        _esc(mapping.relation_id), _esc(_relation_aria(relation)),
                        _esc(_unit_label(unit)), _esc(mapping.relation_id),
                        _unit_text_html(model, unit, phrases, relations), marker))
            body.append("</article>")
        body.append("</section>")
        sections.append("".join(body))
    return (
        '<nav class="claim-strip" aria-label="%s">%s</nav>%s' % (
            _esc(UI["claimIndex"]), "".join(chips), "".join(sections)))


def _attributes(node) -> dict:
    return dict(node.attributes)


def _inline_html(model, node, target_document_id: str) -> str:
    kind = node.kind
    if kind == "text":
        content = _esc(node.text)
    elif kind == "space":
        content = " "
    elif kind in {"softBreak", "lineBreak"}:
        content = "<br>"
    elif kind == "image":
        attributes = _attributes(node)
        asset_id = attributes.get("assetId")
        asset = model.assets.get(asset_id)
        if asset is None or asset.media_type != "image/png":
            raise RenderError("image does not resolve to a typed PNG asset")
        data = base64.b64encode(asset.data).decode("ascii")
        content = '<img src="data:image/png;base64,%s" alt="%s">' % (
            data, _esc(attributes.get("alt", node.text)))
    else:
        child_html = "".join(
            _inline_html(model, child, target_document_id)
            for child in node.children)
        content = child_html if node.children else _esc(node.text)
        wrappers = {
            "strong": "strong", "emphasis": "em", "subscript": "sub",
            "superscript": "sup", "code": "code", "plain": "span",
        }
        if kind in wrappers:
            tag = wrappers[kind]
            content = "<%s>%s</%s>" % (tag, content, tag)
    if node.fragment_id:
        dom_id = model.dom_id(target_document_id, node.fragment_id)
        return '<span id="%s">%s</span>' % (_esc(dom_id), content)
    return content


def _node_chrome(model, node, target_document_id: str, reverse: dict,
                 *, parent_editorial: bool = False) -> tuple[str, str, str]:
    if not node.fragment_id:
        return "", "", ""
    dom_id = model.dom_id(target_document_id, node.fragment_id)
    anchor = _anchor_label(node.fragment_id)
    margin = '<span class="anchor-label" aria-hidden="true">%s</span>' % _esc(anchor)
    references = reverse.get(dom_id, ())
    badge = ""
    if references:
        badge = (
            '<button type="button" class="reverse-badge" id="reverse-control-%s" '
            'data-block="%s" aria-label="%s">◂ %d</button>' % (
                _esc(dom_id), _esc(dom_id),
                _esc(_fmt(UI["reverseBadge"], count=len(references), label=anchor)),
                len(references)))
    editorial = ""
    if node.editorial and not parent_editorial:
        editorial = '<span class="editorial-tag">%s</span>' % _esc(
            _wording(model, "editorial-not-filed"))
    return dom_id, margin + editorial, badge


def _table_html(model, node, target_document_id: str, reverse: dict) -> str:
    dom_id, chrome, badge = _node_chrome(
        model, node, target_document_id, reverse)
    output = ['<div class="table-wrap dblock%s"%s>%s%s<table>' % (
        " editorial" if node.editorial else "",
        ' id="%s"' % _esc(dom_id) if dom_id else "", chrome, badge)]
    for section in node.children:
        if section.kind not in {"head", "body"}:
            raise RenderError("table has an unsupported typed section")
        section_tag = "thead" if section.kind == "head" else "tbody"
        output.append("<%s>" % section_tag)
        for row in section.children:
            if row.kind != "row":
                raise RenderError("table section has a non-row child")
            row_dom, row_chrome, row_badge = _node_chrome(
                model, row, target_document_id, reverse,
                parent_editorial=node.editorial)
            output.append('<tr%s>' % (
                ' id="%s"' % _esc(row_dom) if row_dom else ""))
            for index, cell in enumerate(row.children):
                if cell.kind != "cell":
                    raise RenderError("table row has a non-cell child")
                tag = "th" if section.kind == "head" else "td"
                scope = ' scope="col"' if tag == "th" else ""
                attributes = dict(cell.attributes)
                if set(attributes) != {"alignment"} or \
                        attributes["alignment"] not in _CELL_ALIGNMENT:
                    raise RenderError("table-cell alignment metadata is not closed")
                alignment = ' class="%s"' % _CELL_ALIGNMENT[
                    attributes["alignment"]]
                cell_body = "".join(
                    _inline_html(model, child, target_document_id)
                    for child in cell.children)
                if index == 0:
                    cell_body = row_chrome + row_badge + cell_body
                output.append('<%s%s%s>%s</%s>' % (
                    tag, scope, alignment, cell_body, tag))
            output.append("</tr>")
        output.append("</%s>" % section_tag)
    output.append("</table></div>")
    return "".join(output)


def _block_html(model, node, target_document_id: str, reverse: dict,
                *, parent_editorial: bool = False) -> str:
    if node.kind == "table":
        return _table_html(model, node, target_document_id, reverse)
    dom_id, chrome, badge = _node_chrome(
        model, node, target_document_id, reverse,
        parent_editorial=parent_editorial)
    id_attr = ' id="%s"' % _esc(dom_id) if dom_id else ""
    editorial_class = " editorial" if node.editorial else ""
    children = "".join(
        _inline_html(model, child, target_document_id)
        for child in node.children)
    content = children if node.children else _esc(node.text)

    if node.kind == "heading":
        level = node.level
        if not isinstance(level, int) or not 1 <= level <= 6:
            raise RenderError("typed heading level is invalid")
        return '<h%d class="dblock%s"%s>%s%s%s</h%d>' % (
            level, editorial_class, id_attr, chrome, content, badge, level)
    if node.kind == "paragraph":
        images = [child for child in node.children if child.kind == "image"]
        if images:
            if len(images) != 1:
                raise RenderError("figure paragraph has a non-exact image inventory")
            return '<figure class="dblock%s"%s>%s%s%s<figcaption>%s</figcaption></figure>' % (
                editorial_class, id_attr, chrome, badge,
                _inline_html(model, images[0], target_document_id),
                _esc(images[0].text))
        return '<p class="dblock%s"%s>%s%s%s</p>' % (
            editorial_class, id_attr, chrome, content, badge)
    if node.kind == "codeBlock":
        language = _attributes(node).get("language", "")
        class_attr = ' class="language-%s"' % _esc(language) if language else ""
        return '<pre class="dblock%s"%s>%s%s<code%s>%s</code></pre>' % (
            editorial_class, id_attr, chrome, badge, class_attr, _esc(node.text))
    if node.kind == "blockQuotation":
        nested = "".join(_block_html(
            model, child, target_document_id, reverse,
            parent_editorial=node.editorial) for child in node.children)
        return '<blockquote class="dblock%s"%s>%s%s%s</blockquote>' % (
            editorial_class, id_attr, chrome, badge, nested)
    if node.kind == "list":
        ordered = _attributes(node).get("ordered")
        if not isinstance(ordered, bool):
            raise RenderError("typed list ordering metadata is invalid")
        tag = "ol" if ordered else "ul"
        nested = "".join(_block_html(
            model, child, target_document_id, reverse,
            parent_editorial=node.editorial) for child in node.children)
        return '<div class="dblock%s"%s>%s%s<%s>%s</%s></div>' % (
            editorial_class, id_attr, chrome, badge, tag, nested, tag)
    if node.kind == "item":
        nested = "".join(_block_html(
            model, child, target_document_id, reverse,
            parent_editorial=node.editorial) for child in node.children)
        return '<li class="dblock%s"%s>%s%s%s</li>' % (
            editorial_class, id_attr, chrome, badge, nested)
    if node.kind == "separator":
        return '<div class="dblock%s"%s>%s%s<hr></div>' % (
            editorial_class, id_attr, chrome, badge)
    if node.kind == "plain":
        return '<span%s>%s%s%s</span>' % (id_attr, chrome, content, badge)
    nested = ("".join(_block_html(
        model, child, target_document_id, reverse,
        parent_editorial=node.editorial) for child in node.children)
              if node.children else content)
    return '<div class="dblock%s"%s>%s%s%s</div>' % (
        editorial_class, id_attr, chrome, badge, nested)


def _reader_dom_id(model, document_id: str, fragment_id: str) -> str:
    return "reader-" + model.dom_id(document_id, fragment_id)


def _reader_node_html(model, node, document_id: str, reverse: dict) -> str:
    attributes = dict(node.attributes)
    item_id = node.item_id
    id_attr = (' id="%s" tabindex="-1"' % _esc(
        _reader_dom_id(model, document_id, item_id))) if item_id else ""
    chrome = ""
    if item_id:
        chrome = '<span class="anchor-label" aria-hidden="true">%s</span>' % \
            _esc(_anchor_label(item_id))
        excerpt_dom_id = model.dom_id(document_id, item_id)
        references = reverse.get(excerpt_dom_id, ())
        if references:
            chrome += (
                '<button type="button" class="reverse-badge" '
                'data-block="%s" aria-label="%s">◂ %d</button>' % (
                    _esc(excerpt_dom_id),
                    _esc(_fmt(UI["reverseBadge"], count=len(references),
                              label=_anchor_label(item_id))),
                    len(references)))
    children = "".join(
        _reader_node_html(model, child, document_id, reverse)
        for child in node.children)
    content = children if node.children else _esc(node.text or "")
    kind = node.element
    if kind == "text":
        return _esc(node.text or "")
    if kind == "space":
        return " "
    if kind in {"softBreak", "lineBreak"}:
        return "<br>"
    if kind in {"strong", "emphasis", "code"}:
        tag = {"strong": "strong", "emphasis": "em", "code": "code"}[kind]
        return "<%s>%s</%s>" % (tag, content, tag)
    if kind == "math":
        return '<code class="math">%s</code>' % content
    if kind == "link":
        return '<span class="transcribed-link">%s</span>' % content
    if kind == "heading":
        level = attributes.get("level")
        if not isinstance(level, int) or not 1 <= level <= 6:
            raise RenderError("prior-art reader heading level is invalid")
        return '<h%d class="reader-block"%s>%s%s</h%d>' % (
            level, id_attr, chrome, content, level)
    if kind == "paragraph":
        return '<p class="reader-block"%s>%s%s</p>' % (
            id_attr, chrome, content)
    if kind == "codeBlock":
        return '<pre class="reader-block"%s>%s<code>%s</code></pre>' % (
            id_attr, chrome, _esc(node.text or ""))
    if kind == "blockQuotation":
        return '<blockquote class="reader-block"%s>%s%s</blockquote>' % (
            id_attr, chrome, content)
    if kind == "list":
        ordered = attributes.get("ordered")
        if not isinstance(ordered, bool):
            raise RenderError("prior-art reader list ordering is invalid")
        tag = "ol" if ordered else "ul"
        return '<div class="reader-block"%s>%s<%s>%s</%s></div>' % (
            id_attr, chrome, tag, content, tag)
    if kind == "item":
        return '<li class="reader-block"%s>%s%s</li>' % (
            id_attr, chrome, content)
    if kind == "separator":
        return '<div class="reader-block"%s>%s<hr></div>' % (
            id_attr, chrome)
    if kind == "plain":
        return '<span%s>%s%s</span>' % (id_attr, chrome, content)
    raise RenderError("prior-art reader node kind is unsupported")


def _obligation_label(model, status: str) -> str:
    return _wording(model, "obligation-status-" + status)


def _obligation_data(model):
    by_claim = {}
    dom_by_id = {}
    for item in model.prior_art_obligations:
        dom_id = model.dom_id(model.relation_set_id, item.relation_id)
        dom_by_id[item.relation_id] = dom_id
        claim = by_claim.setdefault(_claim_key(item.claim_number), {
            "ids": [],
            "counts": {
                "passageMapped": 0,
                "counselReviewRequired": 0,
                "reviewedNoMaterialPassage": 0,
            },
        })
        claim["ids"].append(dom_id)
        count_key = {
            "passage-mapped": "passageMapped",
            "counsel-review-required": "counselReviewRequired",
            "reviewed-no-material-passage": "reviewedNoMaterialPassage",
        }[item.status]
        claim["counts"][count_key] += 1
    return {
        "byClaim": {key: value for key, value in sorted(by_claim.items())},
        "domById": {key: value for key, value in sorted(dom_by_id.items())},
    }


def _disclosure_html(model, reverse: dict) -> str:
    if model.product_kind == "prior-art":
        by_document = {}
        for passage in model.prior_art_passages:
            by_document.setdefault(passage.document_id, []).append(passage)
        obligations_by_document = {}
        for obligation in model.prior_art_obligations:
            obligations_by_document.setdefault(
                obligation.evidence.document_id, []).append(obligation)
        readers = {item.document_id: item for item in model.prior_art_readers}
        output = []
        for document in model.prior_art_scope:
            passages = by_document.get(document.document_id, ())
            reader = readers.get(document.document_id)
            if reader is None:
                raise RenderError("matrix document has no full XML reader")
            document_dom_id = model.dom_id(
                model.relation_set_id, document.document_id)
            output.append(
                '<section class="prior-art-document" id="%s"><h2>%s · %s</h2>' % (
                    _esc(document_dom_id), _esc(document.label),
                    _esc(document.document_id)))
            output.append('<h3>%s</h3><ul class="obligation-list">' %
                          _esc(PRIOR_UI["matrixObligations"]))
            for obligation in obligations_by_document.get(
                    document.document_id, ()):
                obligation_dom_id = model.dom_id(
                    model.relation_set_id, obligation.relation_id)
                output.append(
                    '<li class="obligation obligation-%s" id="%s">'
                    '<strong>%s · %s</strong><br>'
                    '<span>%s · %s</span><br><span>%s</span></li>' % (
                        _esc(obligation.status), _esc(obligation_dom_id),
                        _esc(_claim_label(model, obligation.claim_number)),
                        _esc(_obligation_label(model, obligation.status)),
                        _esc(obligation.matrix_relation_id),
                        _esc(obligation.matrix_field),
                        _esc(obligation.matrix_value)))
            output.append("</ul>")
            if not passages:
                output.append(
                    '<p class="state-note">%s</p>' %
                    _esc(PRIOR_UI["noExactPassage"]))
            for passage in passages:
                dom_id = model.dom_id(
                    passage.document_id, passage.fragment_id)
                references = reverse.get(dom_id, ())
                badge = ""
                if references:
                    badge = (
                        '<button type="button" class="reverse-badge" '
                        'id="reverse-control-%s" data-block="%s" '
                        'aria-label="%s">◂ %d</button>' % (
                            _esc(dom_id), _esc(dom_id),
                            _esc(_fmt(UI["reverseBadge"],
                                     count=len(references),
                                     label=_anchor_label(
                                         passage.fragment_id))),
                            len(references)))
                metadata = "page %d" % passage.page
                if passage.region:
                    metadata += " · " + passage.region
                if passage.uncertainty:
                    metadata += " · transcription uncertainty: " + passage.uncertainty
                output.append(
                    '<article class="dblock prior-art-passage" id="%s">'
                    '<span class="anchor-label" aria-hidden="true">%s</span>%s'
                    '<p class="passage-meta">%s</p><p>%s</p>'
                    '<button type="button" class="reader-jump" data-reader="%s" '
                    'data-reader-details="%s">%s</button></article>' % (
                        _esc(dom_id),
                        _esc(_anchor_label(passage.fragment_id)), badge,
                        _esc(metadata), _esc(passage.text),
                        _esc(_reader_dom_id(
                            model, passage.document_id, passage.fragment_id)),
                        _esc("full-reader-" + document_dom_id),
                        _esc(PRIOR_UI["openFullReader"])))
            reader_body = "".join(
                _reader_node_html(model, node, document.document_id, reverse)
                for node in reader.content)
            output.append(
                '<details class="full-reader" id="full-reader-%s"><summary>%s — %s</summary>'
                '<p class="reader-authority">%s</p><div class="reader-content">%s</div>'
                '</details>' % (
                    _esc(document_dom_id), _esc(PRIOR_UI["fullReader"]),
                    _esc(reader.title),
                    _esc(_wording(model, "authority-target-sources")),
                    reader_body))
            output.append("</section>")
        return "".join(output)
    target_document_id = model.source_documents[1].document_id
    return "".join(_block_html(
        model, node, target_document_id, reverse)
        for node in model.disclosure_blocks)


def _caution_schedule_html(caution: dict) -> str:
    detail = "%s — %s" % (caution["typeLabel"], caution["scope"])
    quote = ""
    if caution["quote"] and caution["quote"] != caution["name"]:
        quote = '<q class="caution-quote">%s</q>' % _esc(caution["quote"])
    return '<span class="schedule-caution">⚑ %s — %s%s</span>' % (
        _esc(detail), _esc(caution["name"]), quote)


def _target_schedule_html(target: dict) -> str:
    parts = []
    if target.get("candidateId"):
        parts.append('<strong>%s</strong>' % _esc(target["candidateId"]))
    if target["roleLabel"]:
        parts.append("[%s]" % _esc(target["roleLabel"]))
    if target["note"]:
        parts.append(_esc(target["note"]))
    parts.append("passages: %s" % " + ".join(
        _esc(label) for label in target["labels"]))
    if target.get("obligationIds"):
        parts.append("obligations: %s" % _esc(
            " ".join(target["obligationIds"])))
    if target["caution"]:
        parts.append(_caution_schedule_html(target["caution"]))
    return " · ".join(parts)


def _schedule_html(model, relations: dict, claim_gates: dict) -> str:
    rows = []
    for claim in model.claims:
        for unit in claim.units:
            mapping = model.mappings_by_unit[unit.fragment_id][0]
            ordered_ids = [mapping.relation_id]
            ordered_ids.extend(
                phrase.relation_id
                for phrase in model.phrases_by_unit.get(unit.fragment_id, ()))
            for relation_id in ordered_ids:
                relation = relations[relation_id]
                targets = "<br>".join(
                    _target_schedule_html(target)
                    for target in relation["targets"])
                allocations = "<br>".join(
                    '<span class="review-allocation"><strong>%s</strong> · %s · '
                    'obligations: %s</span>' % (
                        _esc(item["allocationId"]), _esc(item["note"]),
                        _esc(" ".join(item["obligationIds"])))
                    for item in relation["reviewAllocations"])
                targets = "<br>".join(
                    item for item in (targets, allocations) if item)
                cautions = []
                if relation["caution"]:
                    cautions.append(_caution_schedule_html(
                        relation["caution"]))
                cautions.extend(_esc(item["text"])
                                for item in relation["dispositions"])
                rows.append(
                    '<tr class="mapping-row"><th scope="row">%s</th><td>%s</td><td>%s</td><td>%s</td></tr>'
                    % (_esc(relation["subjectLabel"]),
                       _esc(relation["statusLabel"]), targets,
                       "<br>".join(cautions)))
    gate_rows = []
    for claim in model.claims:
        for item in claim_gates.get(_claim_key(claim.number), ()):
            gate_rows.append(
                '<tr><th scope="row">%s</th><td>%s</td><td>%s</td></tr>' % (
                    _esc(_claim_label(model, claim.number)),
                    _caution_schedule_html(item["gate"]),
                    _esc(item["disposition"]["text"])))
    return (
        '<section id="schedule"><h2 id="schedule-title">%s</h2>'
        '<table class="schedule" aria-labelledby="schedule-title"><thead><tr>'
        '<th scope="col">%s</th><th scope="col">%s</th>'
        '<th scope="col">%s</th><th scope="col">%s</th>'
        '</tr></thead><tbody>%s</tbody></table>'
        '<h3 id="claim-gates-title">%s</h3>'
        '<table class="schedule" aria-labelledby="claim-gates-title"><thead><tr>'
        '<th scope="col">%s</th><th scope="col">%s</th>'
        '<th scope="col">%s</th></tr></thead><tbody>%s</tbody></table></section>'
        % (_esc(UI["completeSchedule"]), _esc(UI["scheduleFragment"]),
           _esc(UI["mappingStatus"]), _esc(UI["scheduleTargets"]),
           _esc(UI["mappingCautions"]), "".join(rows),
           _esc(UI["scheduleClaimGates"]), _esc(UI["scheduleFragment"]),
           _esc(UI["gateHeader"]), _esc(UI["scheduleDisposition"]),
           "".join(gate_rows)))


def _provenance(model, profile_label: str) -> tuple[dict, str]:
    documents = []
    rows = []
    for source in model.source_documents:
        item = {
            "documentId": source.document_id,
            "authorityScheme": source.authority_scheme,
            "xmlRole": source.xml_role,
            "xmlRawDigest": source.xml_raw_digest,
            "registeredPath": source.registered_path,
        }
        documents.append(item)
        rows.append(
            '<tr><th scope="row">%s</th><td>%s</td><td>%s</td>'
            '<td><code>%s</code></td><td>%s</td></tr>' % (
                _esc(source.document_id), _esc(source.authority_scheme),
                _esc(source.xml_role), _esc(source.xml_raw_digest),
                _esc(source.registered_path)))
    assets = [{
        "assetId": asset.asset_id,
        "path": asset.path,
        "mediaType": asset.media_type,
        "rawDigest": asset.raw_digest,
    } for asset in model.assets.values()]
    summary = _wording(model, "provenance-summary")
    provenance = {
        "editionId": model.edition_id,
        "claimSetVersion": model.claim_set_version,
        "relationSetId": model.relation_set_id,
        "profileLabel": profile_label,
        "documents": documents,
        "assets": assets,
        "summary": summary,
    }
    source_label = _wording(model, "source-input-provenance")
    authority = _wording(model, "authority-target-sources")
    markup = (
        '<section id="about"><h2>%s</h2><p><strong>%s</strong></p>'
        '<p>%s</p><p>%s</p>'
        '<table class="schedule" aria-label="%s"><thead><tr>'
        '<th scope="col">%s</th><th scope="col">%s</th>'
        '<th scope="col">%s</th><th scope="col">%s</th><th scope="col">%s</th>'
        '</tr></thead><tbody>%s</tbody></table>'
        '<p>%s: <code>%s</code></p></section>' % (
            _esc(UI["about"]), _esc(authority), _esc(source_label),
            _esc(summary), _esc(source_label),
            _esc(UI["provenanceDocument"]),
            _esc(UI["authoritySchemeHeader"]),
            _esc(UI["xmlRoleHeader"]), _esc(UI["provenanceDigest"]),
            _esc(UI["sourcePathHeader"]),
            "".join(rows), _esc(UI["provenanceRelationSet"]),
            _esc(model.relation_set_id)))
    return provenance, markup


def render(model, mode="candidate") -> bytes:
    """Render one candidate or preview from the sealed typed model."""
    if mode not in {"candidate", "preview"}:
        raise RenderError("render mode must be candidate or preview")
    relations, reverse, claim_gates = _relation_data(model)
    statuses = {
        status: _wording(model, "mapping-status-" + status)
        for status in ("mapped", "counsel-review-required")
    }
    legend = _wording(model, "counsel-legend")
    profile_label = _wording(model, "artifact-label-technical-preview")
    if profile_label != model.profile_label:
        raise RenderError("typed profile label and controlled wording differ")
    disclaimer = _wording(model, "standing-disclaimer")
    watermark_text = _wording(
        model, "artifact-watermark-technical-preview") if mode == "preview" else ""
    watermark = ('<div class="watermark" aria-hidden="true"><span>%s</span></div>'
                 % _esc(watermark_text)) if watermark_text else ""
    provenance, provenance_html = _provenance(model, profile_label)
    forbidden = [token for token in FORBIDDEN_SCRIPT_TOKENS if token in JS]
    if forbidden:
        raise RenderError(
            "application script uses forbidden browser capabilities: %s" %
            ", ".join(forbidden))
    ui = dict(UI)
    if model.product_kind == "prior-art":
        ui.update(PRIOR_UI)
    ui["forwardMode"] = model.forward_mode_label
    ui["reverseMode"] = model.reverse_mode_label
    navigation = {
        "ui": ui,
        "edition": {
            "id": model.edition_id,
            "prefix": model.strategy_prefix,
            "version": model.claim_set_version,
            "name": model.display_name,
        },
        "statuses": statuses,
        "relations": relations,
        "reverse": reverse,
        "claimGates": claim_gates,
    }
    if model.product_kind == "prior-art":
        navigation["obligations"] = _obligation_data(model)
    title = "%s — %s" % (model.display_name, model.claim_set_version)
    html_text = HTML_TEMPLATE.format(
        csp=EXACT_CSP,
        css=CSS,
        title=_esc(title),
        watermark=watermark,
        legend=_esc(legend),
        profile=_esc(profile_label),
        display_name=_esc(model.display_name),
        strategy=_esc("%s — %s" % (
            model.strategy_prefix, model.strategy_name)),
        claim_set_label=_esc(UI["claimSetLabel"]),
        version=_esc(model.claim_set_version),
        authority=_esc(model.authority_header),
        aux_label=_esc(UI["aboutScheduleToggle"]),
        disclaimer=_esc(disclaimer),
        claims_label=_esc(UI["candidateClaimsLabel"]),
        disclosure_label=_esc(model.target_pane_label),
        claims=_claims_html(model, relations, claim_gates),
        disclosure=_disclosure_html(model, reverse),
        schedule=_schedule_html(model, relations, claim_gates),
        provenance=provenance_html,
        machine_data_label=_esc(UI["machineData"]),
        nav_data=_script_json(navigation),
        provenance_data=_script_json(provenance),
        js=JS,
    )
    return html_text.encode("utf-8")


HTML_TEMPLATE = """<!DOCTYPE html>
<!-- GENERATED current product; do not edit by hand. -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="{csp}">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
{watermark}
<header id="masthead">
<p class="legend">{legend}</p>
<p class="release-profile">{profile}</p>
<h1>{display_name} <span class="strategy">{strategy}</span></h1>
<p class="meta">{claim_set_label} <strong>{version}</strong> · {authority}
<button type="button" id="aux-toggle" data-aux="1" aria-pressed="false">{aux_label}</button></p>
<p class="disclaimer">{disclaimer}</p>
</header>
<div id="content-root">
<main id="panes">
<section id="claims-pane" aria-label="{claims_label}">
<div id="reverse-bar" class="navigation-bar" hidden></div>
{claims}
</section>
<section id="disclosure-pane" aria-label="{disclosure_label}">
<div id="forward-bar" class="navigation-bar" hidden></div>
<div id="disclosure-scroll">{disclosure}</div>
</section>
</main>
<div id="live" aria-live="polite" aria-atomic="true" class="visually-hidden"></div>
<div id="aux">{schedule}{provenance}</div>
</div>
<footer><p class="legend">{legend}</p><p class="release-profile">{profile}</p>
<p class="disclaimer">{disclaimer}</p></footer>
<noscript><style>
#content-root{{display:block;overflow-y:auto;min-height:0;flex:1 1 auto}}
#panes,#claims-pane,#disclosure-pane,#disclosure-scroll,#aux{{height:auto;min-height:0;overflow:visible}}
#aux{{display:block}} #aux-toggle{{display:none}} .pointer-surface{{cursor:auto}}
@media print {{#content-root,#panes,#claims-pane,#disclosure-pane,#disclosure-scroll,#aux{{display:block;overflow:visible;height:auto}}}}
</style></noscript>
<script type="application/json" id="nav-data" aria-label="{machine_data_label}">{nav_data}</script>
<script type="application/json" id="provenance-data">{provenance_data}</script>
<script>{js}</script>
</body>
</html>
"""


CSS = r"""
:root {
  --accent:#1a4f8b; --strong:#ffe08a; --soft:#fff3c9; --gate:#8b2c1a;
  --state:#6a4a00; --chrome:#f4f2ec; --line:#c9c4b8; --paper:#fff;
}
* { box-sizing:border-box; }
html,body { height:100%; margin:0; padding:0; }
body {
  color:#1c1c1c; background:var(--paper);
  display:flex; flex-direction:column; overflow:hidden;
  font-family:Georgia,'Times New Roman',serif;
}
.visually-hidden {
  position:absolute; width:1px; height:1px; padding:0; margin:-1px;
  overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap; border:0;
}
#masthead,footer {
  flex:none; padding:6px 14px; background:var(--chrome);
  border-bottom:1px solid var(--line); font-family:Arial,sans-serif;
}
#masthead h1 { margin:2px 0; font-size:15px; }
#masthead .meta { margin:2px 0; font-size:12px; }
.strategy { color:var(--accent); font-weight:normal; }
.legend {
  margin:2px 0; color:#7a1f1f; font-size:10px; font-weight:bold;
  letter-spacing:.4px;
}
.release-profile {
  margin:2px 0; color:#704d00; font-size:10.5px; font-weight:bold;
}
.disclaimer { margin:2px 0; color:#444; font-size:10.5px; }
#content-root { flex:1 1 auto; display:flex; flex-direction:column; min-height:0; }
#panes { flex:1 1 auto; display:flex; min-height:0; }
#claims-pane {
  width:45%; overflow-y:auto; padding:10px 14px; position:relative;
  border-right:2px solid var(--line);
}
#disclosure-pane {
  width:55%; display:flex; flex-direction:column; min-height:0; position:relative;
}
#disclosure-scroll { flex:1; overflow-y:auto; padding:10px 40px 10px 58px; }
.claim-strip {
  position:sticky; top:-10px; z-index:5; display:block;
  padding:6px 0; background:#fff; border-bottom:1px solid var(--line);
  font-family:Arial,sans-serif;
}
.chip-group { display:inline-block; margin-right:8px; white-space:nowrap; }
.chip-group-name {
  margin-right:2px; color:#666; font-size:9px; text-transform:uppercase;
}
.chip {
  min-width:24px; min-height:24px; border:1px solid var(--line);
  border-radius:4px; background:#fff; cursor:pointer; font-size:12px;
}
.chip-independent { border:2px solid var(--accent); font-weight:bold; }
.claim-group h2 {
  color:var(--accent); border-bottom:1px solid var(--line);
  font:600 13px Arial,sans-serif;
}
.claim { margin:0 0 14px; }
.claim-header { margin:8px 0 4px; font:bold 13px Arial,sans-serif; }
.claim-independent > .claim-header .claim-no { color:var(--accent); }
.gate-chip {
  min-height:24px; margin-left:8px; padding:1px 5px;
  border:2px dashed var(--gate); border-radius:4px;
  color:var(--gate); background:#fdf3f0; cursor:pointer; font-size:11px;
}
.unit { display:flex; margin:2px 0; }
.unit-btn {
  flex:none; width:24px; min-height:24px; border:0;
  border-left:4px solid var(--line); background:transparent; cursor:pointer;
}
.unit:hover .unit-btn,.unit-btn:focus {
  border-left-color:var(--accent); background:#eef3fa;
}
.unit-body { padding:2px 4px; }
.unit-label {
  display:block; color:#777; font:9px Arial,sans-serif; text-transform:uppercase;
}
.state-counsel-review-required > .unit-body { background:#fbf6e8; }
.state-note {
  margin:2px 0; color:var(--state); font:11px Arial,sans-serif;
}
.obligation-list {
  margin:4px 0 10px; padding:0; list-style:none; font:10.5px Arial,sans-serif;
}
.obligation {
  margin:3px 0; padding:5px 7px; border-left:4px solid var(--line);
  background:#f8f7f3;
}
.obligation-passage-mapped { border-left-color:#287448; }
.obligation-counsel-review-required { border-left-color:#b16a00; }
.obligation-reviewed-no-material-passage { border-left-color:#777; }
.highlight-obligation { outline:2px dotted var(--accent); outline-offset:1px; }
.allocation-detail {
  margin:3px 0; padding:4px 6px; border-left:3px solid #b16a00;
  background:#fbf6e8; font-size:11px;
}
.reader-jump {
  min-height:24px; border:1px solid var(--accent); border-radius:4px;
  color:var(--accent); background:#fff; cursor:pointer; font-size:11px;
}
.full-reader {
  margin:10px 0 18px; padding:6px 8px; border:1px solid var(--line);
  background:#fcfbf7;
}
.full-reader > summary {
  color:var(--accent); cursor:pointer; font:600 12px Arial,sans-serif;
}
.reader-authority { color:#555; font:10px Arial,sans-serif; }
.reader-content {
  position:relative; margin:8px 0 0; padding:6px 0 6px 50px;
  border-top:1px solid var(--line);
}
.reader-block { position:relative; }
.reader-block:focus { outline:3px solid #d98c00; outline-offset:2px; }
.transcribed-link { text-decoration:underline dotted; }
.phrase-btn {
  min-height:24px; padding:0 1px; border:0;
  border-bottom:2px dotted var(--accent); color:var(--accent);
  background:transparent; cursor:pointer; font:inherit;
}
.pointer-surface { cursor:pointer; }
button:focus-visible,.navigation-bar:focus-visible {
  outline:3px solid #d98c00; outline-offset:1px;
}
.dblock { position:relative; }
.anchor-label {
  position:absolute; left:-48px; top:2px; width:42px;
  color:#777; text-align:right; font:9px Menlo,monospace;
}
.table-wrap .anchor-label,td .anchor-label,th .anchor-label {
  position:static; display:inline-block; width:auto; margin-right:5px; text-align:left;
}
.reverse-badge {
  min-width:24px; min-height:24px; margin-left:6px;
  border:1px solid var(--accent); border-radius:12px;
  color:var(--accent); background:#fff; cursor:pointer; font:10px Arial,sans-serif;
}
.editorial-tag {
  display:inline-block; margin-right:6px; padding:1px 4px; border-radius:3px;
  color:#555; background:#e8e4da; vertical-align:middle;
  font:9px Arial,sans-serif; text-transform:uppercase;
}
.editorial { color:#3d3d3d; }
.table-wrap { max-width:100%; overflow-x:auto; }
table { border-collapse:collapse; font-size:12.5px; }
th,td { padding:3px 7px; border:1px solid var(--line); text-align:left; }
.cell-align-default,.cell-align-left { text-align:left; }
.cell-align-center { text-align:center; }
.cell-align-right { text-align:right; }
figure { margin:12px 0; }
figure img { display:block; max-width:100%; border:1px solid var(--line); }
figcaption { margin-top:3px; color:#555; font:11px Arial,sans-serif; }
pre {
  max-width:100%; overflow-x:auto; padding:8px;
  border:1px solid var(--line); background:#f7f6f2; font-size:11.5px;
}
.highlight-strong {
  background:var(--strong); border-left:4px solid var(--accent);
  box-shadow:0 0 0 2px var(--strong);
}
.highlight-soft { background:var(--soft); border-left:4px double var(--accent); }
.highlight-subject { outline:2px solid var(--accent); outline-offset:1px; }
.highlight-related { background:var(--soft); outline:2px dotted var(--accent); }
.navigation-bar {
  position:sticky; top:0; z-index:10; padding:6px 10px;
  border:2px solid var(--accent); border-radius:0 0 6px 6px;
  background:#fff; box-shadow:0 2px 6px rgba(0,0,0,.15);
  font:12px Arial,sans-serif;
}
.navigation-bar .mode {
  color:var(--accent); font-size:10px; letter-spacing:.5px; text-transform:uppercase;
}
.navigation-bar .context { font-weight:bold; }
.navigation-bar button {
  min-width:28px; min-height:24px; border:1px solid var(--line);
  border-radius:4px; background:#fff; cursor:pointer;
}
.selection-controls { display:inline-flex; gap:3px; margin:4px 0; }
.caution-chip {
  display:inline-block; margin:2px 4px 2px 0; padding:1px 5px;
  border:1px solid var(--gate); border-radius:4px;
  color:var(--gate); background:#fdf3f0; font-size:11px;
}
.caution-detail {
  display:block; margin:4px 0; padding:4px 6px;
  border-left:3px solid var(--gate); background:#faf7f2; font-size:11px;
}
.disposition { color:var(--gate); font-size:11px; }
#aux { display:none; flex:1; min-height:0; overflow-y:auto; }
body.aux-open #aux { display:block; }
body.aux-open #panes { display:none; }
#aux-toggle {
  min-height:24px; margin-left:12px; border:1px solid var(--line);
  border-radius:4px; background:#fff; cursor:pointer; font-size:11px;
}
#schedule,#about { display:block; padding:10px 16px; font-family:Arial,sans-serif; }
.schedule { width:100%; font-size:11px; }
.schedule-caution { color:var(--gate); }
.caution-quote { display:block; margin:3px 0; color:#333; }
.watermark {
  position:fixed; inset:0; z-index:99; display:flex;
  align-items:center; justify-content:center; pointer-events:none;
}
.watermark span {
  color:rgba(180,30,30,.18); white-space:nowrap;
  transform:rotate(-28deg); font:bold 42px Arial,sans-serif;
}
footer { display:none; }
@media (max-width:1279px),(max-height:719px) {
  #panes { display:block; overflow-y:auto; }
  #claims-pane,#disclosure-pane {
    display:block; width:100%; height:auto; overflow:visible; border-right:0;
  }
  #disclosure-scroll { overflow:visible; }
}
@media (prefers-reduced-motion: reduce) { html { scroll-behavior:auto; } }
@page { margin:12mm 10mm; }
@media print {
  body { display:block; overflow:visible; }
  #content-root {
    display:block; overflow:visible; padding-bottom:37mm;
    -webkit-box-decoration-break:clone; box-decoration-break:clone;
  }
  #aux,#panes { display:block !important; overflow:visible; }
  #claims-pane,#disclosure-pane,#disclosure-scroll {
    display:block; width:100%; overflow:visible; border:0;
  }
  button:not(.phrase-btn),.navigation-bar,.claim-strip,.watermark {
    display:none !important;
  }
  .phrase-btn {
    min-height:0; padding:0; border:0; color:inherit; background:transparent;
    cursor:default;
  }
  #masthead > .legend,#masthead > .release-profile,#masthead > .disclaimer {
    display:none;
  }
  footer {
    position:fixed; right:0; bottom:0; left:0; display:block;
    height:35mm; overflow:hidden; padding:2mm 0 0;
    border-top:1px solid var(--line); border-bottom:0; background:#fff;
  }
  table,figure,pre { break-inside:avoid; }
  details > :not(summary) { display:block !important; }
  details > summary { list-style:none; }
}
noscript .navigation-bar { display:none; }
"""


JS = r"""
'use strict';
var DATA = JSON.parse(document.getElementById('nav-data').textContent);
var state = {
  mode:null, key:null, candidateIndex:0, passageIndex:0,
  reverseIndex:0, reverseList:[], returnFocus:null
};
var forwardBar = document.getElementById('forward-bar');
var reverseBar = document.getElementById('reverse-bar');
var disclosureScroll = document.getElementById('disclosure-scroll');
var claimsPane = document.getElementById('claims-pane');
var live = document.getElementById('live');

function ui(key){ return DATA.ui[key]; }
function format(template, values){
  Object.keys(values).forEach(function(key){
    template = template.split('{' + key + '}').join(String(values[key]));
  });
  return template;
}
function element(tag, className, text){
  var node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined && text !== null) node.textContent = text;
  return node;
}
function button(className, label, text, handler){
  var node = element('button', className, text);
  node.type = 'button';
  node.setAttribute('aria-label', label);
  node.addEventListener('click', handler);
  return node;
}
function announce(text){ live.textContent = text; }
function positionText(position, total, label){
  return format(ui('position'), {position:position, total:total, label:label});
}
function relation(relationId){ return DATA.relations[relationId] || null; }
function claimGates(current){ return DATA.claimGates[current.claimKey] || []; }
function selectedCandidate(current){
  return current.targets[state.candidateIndex] || null;
}
function selectedPassageId(current){
  var candidate = selectedCandidate(current);
  return candidate ? candidate.blocks[state.passageIndex] : null;
}
function focusWithoutScroll(node){
  node.setAttribute('tabindex', '-1');
  node.focus({preventScroll:true});
}
function scrollWithin(owner, node, alignment){
  if (!owner || !node) return;
  var ownerBox = owner.getBoundingClientRect();
  var nodeBox = node.getBoundingClientRect();
  var offset = alignment === 'start' ? 10 :
    Math.max(10, (owner.clientHeight - nodeBox.height) / 2);
  owner.scrollTop = owner.scrollTop + nodeBox.top - ownerBox.top - offset;
}
function scrollDisclosureToNode(id){
  scrollWithin(disclosureScroll, document.getElementById(id), 'center');
}
function scrollClaimsToNode(id, alignment){
  scrollWithin(claimsPane, document.getElementById(id), alignment || 'center');
}

function clearHighlights(){
  ['highlight-strong','highlight-soft','highlight-subject','highlight-related',
   'highlight-obligation']
    .forEach(function(className){
      Array.prototype.slice.call(document.querySelectorAll('.' + className))
        .forEach(function(node){ node.classList.remove(className); });
    });
}
function emptyState(){
  return {
    mode:null, key:null, candidateIndex:0, passageIndex:0,
    reverseIndex:0, reverseList:[], returnFocus:null
  };
}
function clearSelection(returnFocus){
  var focusId = state.returnFocus;
  state = emptyState();
  forwardBar.hidden = true;
  reverseBar.hidden = true;
  forwardBar.textContent = '';
  reverseBar.textContent = '';
  clearHighlights();
  if (returnFocus && focusId){
    var focusNode = document.getElementById(focusId);
    if (focusNode) focusNode.focus({preventScroll:true});
  }
  announce(ui('selectionCleared'));
}
function clearControl(){
  var wrap = element('div', 'selection-controls');
  wrap.appendChild(button(null, ui('clearSelection'), '×', function(){
    clearSelection(true);
  }));
  return wrap;
}
function forwardControls(current){
  var wrap = element('div', 'selection-controls');
  var candidate = selectedCandidate(current);
  if (current.targets.length > 1){
    wrap.appendChild(button(null, ui('previousCandidate') || ui('previous'),
      '◀C', function(){ moveCandidate(-1); }));
    wrap.appendChild(button(null, ui('nextCandidate') || ui('next'),
      'C▶', function(){ moveCandidate(1); }));
  }
  if (candidate && candidate.blocks.length > 1){
    wrap.appendChild(button(null, ui('previousPassage') || ui('previous'),
      '◀P', function(){ movePassage(-1); }));
    wrap.appendChild(button(null, ui('nextPassage') || ui('next'),
      'P▶', function(){ movePassage(1); }));
  }
  wrap.appendChild(button(null, ui('clearSelection'), '×', function(){
    clearSelection(true);
  }));
  return wrap;
}
function reverseControls(){
  var wrap = element('div', 'selection-controls');
  if (state.reverseList.length > 1){
    wrap.appendChild(button(null, ui('previousCandidate') || ui('previous'),
      '◀', function(){ moveCandidate(-1); }));
    wrap.appendChild(button(null, ui('nextCandidate') || ui('next'),
      '▶', function(){ moveCandidate(1); }));
  }
  wrap.appendChild(button(null, ui('clearSelection'), '×', function(){
    clearSelection(true);
  }));
  return wrap;
}
function cautionControl(caution){
  var wrap = element('span');
  var chipLabel = caution.typeLabel + ' — ' + caution.name + ' — ' + caution.scope;
  var chip = button('caution-chip', chipLabel, '⚑ ' + caution.name, function(){
    var detail = wrap.querySelector('.caution-detail');
    if (detail){
      detail.remove();
      chip.setAttribute('aria-expanded', 'false');
      return;
    }
    detail = element('span', 'caution-detail',
      caution.typeLabel + ' — ' + caution.scope + ' — ' + caution.quote);
    wrap.appendChild(detail);
    chip.setAttribute('aria-expanded', 'true');
  });
  chip.setAttribute('aria-expanded', 'false');
  wrap.appendChild(chip);
  return wrap;
}
function cautionPresence(current, target){
  var values = [];
  if (current.caution || (target && target.caution))
    values.push(ui('cautionPresent'));
  if (claimGates(current).length) values.push(ui('gatePresent'));
  return values.length ? ' — ' + values.join(', ') : '';
}
function candidatePositionText(current, candidate){
  var label = candidate.candidateId ?
    candidate.candidateId + ' · ' + candidate.label : candidate.label;
  if (ui('candidatePosition')) return format(ui('candidatePosition'), {
    position:state.candidateIndex + 1, total:current.targets.length, label:label
  });
  return positionText(state.candidateIndex + 1, current.targets.length, label);
}
function passagePositionText(candidate){
  if (!ui('passagePosition')) return '';
  return format(ui('passagePosition'), {
    position:state.passageIndex + 1,
    total:candidate.blocks.length,
    label:candidate.labels[state.passageIndex]
  });
}
function claimObligationData(current){
  if (!DATA.obligations) return null;
  return DATA.obligations.byClaim[current.claimKey] || {
    ids:[], counts:{
      passageMapped:0, counselReviewRequired:0, reviewedNoMaterialPassage:0
    }
  };
}
function forwardAnnouncement(current){
  var parts = [ui('forwardMode'), current.subjectLabel];
  var candidate = selectedCandidate(current);
  if (!candidate){
    parts.push(current.statusLabel);
  } else {
    parts.push(candidatePositionText(current, candidate));
    if (ui('passagePosition')) parts.push(passagePositionText(candidate));
  }
  return parts.join(' — ') + cautionPresence(current, candidate);
}
function renderForwardBar(){
  var current = relation(state.key);
  var candidate = selectedCandidate(current);
  forwardBar.textContent = '';
  forwardBar.appendChild(element('div', 'mode', ui('forwardMode')));
  forwardBar.appendChild(element('div', 'context', current.subjectLabel));
  if (DATA.obligations){
    var claimData = claimObligationData(current);
    forwardBar.appendChild(element('div', null, format(
      ui('claimObligationSummary'), {
        mapped:claimData.counts.passageMapped,
        review:claimData.counts.counselReviewRequired,
        noMaterial:claimData.counts.reviewedNoMaterialPassage
      })));
    forwardBar.appendChild(element('div', null, format(
      ui('exactCandidateCount'), {count:current.targets.length})));
    forwardBar.appendChild(element('div', null, format(
      ui('reviewAllocationCount'), {count:current.reviewAllocations.length})));
  }
  if (!candidate){
    forwardBar.appendChild(element('div', null, current.statusLabel));
  } else {
    var targetLine = candidatePositionText(current, candidate);
    if (candidate.roleLabel) targetLine += ' [' + candidate.roleLabel + ']';
    forwardBar.appendChild(element('div', null, targetLine));
    if (ui('passagePosition'))
      forwardBar.appendChild(element('div', null, passagePositionText(candidate)));
    if (candidate.note) forwardBar.appendChild(element('div', null, candidate.note));
    if (candidate.obligationIds && candidate.obligationIds.length)
      forwardBar.appendChild(element(
        'div', null, 'Obligations: ' + candidate.obligationIds.join(' ')));
    if (candidate.caution) forwardBar.appendChild(cautionControl(candidate.caution));
  }
  current.reviewAllocations.forEach(function(item){
    forwardBar.appendChild(element(
      'div', 'allocation-detail', item.allocationId + ' — ' + item.note +
      ' — obligations: ' + item.obligationIds.join(' ')));
  });
  if (current.caution) forwardBar.appendChild(cautionControl(current.caution));
  current.dispositions.forEach(function(item){
    forwardBar.appendChild(element('div', 'disposition', item.text));
  });
  claimGates(current).forEach(function(item){
    forwardBar.appendChild(cautionControl(item.gate));
  });
  forwardBar.appendChild(forwardControls(current));
  forwardBar.hidden = false;
}
function exactObligationDomIds(current, candidate){
  if (!DATA.obligations) return [];
  var identifiers = candidate ? candidate.obligationIds : [];
  if (!candidate){
    current.reviewAllocations.forEach(function(item){
      identifiers = identifiers.concat(item.obligationIds);
    });
  }
  return identifiers.map(function(identifier){
    return DATA.obligations.domById[identifier];
  }).filter(function(identifier){ return !!identifier; });
}
function applyForwardHighlights(){
  clearHighlights();
  var current = relation(state.key);
  var candidate = selectedCandidate(current);
  var subject = document.getElementById(current.subjectDomId);
  if (subject) subject.classList.add('highlight-subject');
  var obligationDomIds = exactObligationDomIds(current, candidate);
  obligationDomIds.forEach(function(id){
    var obligation = document.getElementById(id);
    if (obligation) obligation.classList.add('highlight-obligation');
  });
  if (!candidate){
    if (obligationDomIds.length) scrollDisclosureToNode(obligationDomIds[0]);
    return;
  }
  candidate.blocks.forEach(function(blockId, index){
    var block = document.getElementById(blockId);
    if (!block) return;
    block.classList.add(index === state.passageIndex ?
      'highlight-strong' : 'highlight-soft');
  });
  scrollDisclosureToNode(selectedPassageId(current));
}
function activateForward(relationId, fromId){
  var current = relation(relationId);
  if (!current) return;
  clearSelection(false);
  state = emptyState();
  state.mode = 'forward';
  state.key = relationId;
  state.returnFocus = fromId;
  renderForwardBar();
  focusWithoutScroll(forwardBar);
  applyForwardHighlights();
  announce(forwardAnnouncement(current));
}

function reverseEntry(){
  return state.reverseList[state.reverseIndex];
}
function reverseCandidate(){
  var entry = reverseEntry();
  var current = entry ? relation(entry.relationId) : null;
  return current ? current.targets[entry.candidateIndex] : null;
}
function reverseAnnouncement(){
  var entry = reverseEntry();
  var current = relation(entry.relationId);
  var candidate = reverseCandidate();
  var claims = {};
  state.reverseList.forEach(function(item){
    claims[relation(item.relationId).claimKey] = true;
  });
  return [
    ui('reverseMode'),
    positionText(state.reverseIndex + 1, state.reverseList.length,
      current.subjectLabel + ' · ' + entry.candidateId),
    format(ui('reverseCounts'), {
      fragments:state.reverseList.length, claims:Object.keys(claims).length
    })
  ].join(' — ') + cautionPresence(current, candidate);
}
function renderReverseBar(){
  var entry = reverseEntry();
  var current = relation(entry.relationId);
  var candidate = reverseCandidate();
  var claims = {};
  state.reverseList.forEach(function(item){
    claims[relation(item.relationId).claimKey] = true;
  });
  reverseBar.textContent = '';
  reverseBar.appendChild(element('div', 'mode', ui('reverseMode')));
  reverseBar.appendChild(element('div', 'context', current.subjectLabel));
  reverseBar.appendChild(element('div', null, format(ui('reverseCounts'), {
    fragments:state.reverseList.length, claims:Object.keys(claims).length
  })));
  reverseBar.appendChild(element('div', null,
    positionText(state.reverseIndex + 1, state.reverseList.length,
      entry.candidateId + ' · ' + candidate.label)));
  reverseBar.appendChild(reverseControls());
  reverseBar.hidden = false;
}
function applyReverseHighlights(){
  clearHighlights();
  var disclosure = document.getElementById(state.key);
  if (disclosure) disclosure.classList.add('highlight-subject');
  state.reverseList.forEach(function(entry){
    var current = relation(entry.relationId);
    var subject = document.getElementById(current.subjectDomId);
    if (subject) subject.classList.add('highlight-related');
  });
  var current = relation(reverseEntry().relationId);
  var selected = document.getElementById(current.subjectDomId);
  if (selected){
    selected.classList.remove('highlight-related');
    selected.classList.add('highlight-strong');
    scrollClaimsToNode(current.subjectDomId, 'center');
  }
}
function activateReverse(blockId, fromId){
  var list = DATA.reverse[blockId] || [];
  if (!list.length) return;
  clearSelection(false);
  state = emptyState();
  state.mode = 'reverse';
  state.key = blockId;
  state.reverseList = list;
  state.returnFocus = fromId;
  renderReverseBar();
  focusWithoutScroll(reverseBar);
  applyReverseHighlights();
  announce(reverseAnnouncement());
}
function moveCandidate(delta){
  if (state.mode === 'forward'){
    var current = relation(state.key);
    if (!current.targets.length) return;
    state.candidateIndex =
      (state.candidateIndex + delta + current.targets.length) %
      current.targets.length;
    state.passageIndex = 0;
    renderForwardBar();
    focusWithoutScroll(forwardBar);
    applyForwardHighlights();
    announce(forwardAnnouncement(current));
  } else if (state.mode === 'reverse'){
    state.reverseIndex =
      (state.reverseIndex + delta + state.reverseList.length) %
      state.reverseList.length;
    renderReverseBar();
    focusWithoutScroll(reverseBar);
    applyReverseHighlights();
    announce(reverseAnnouncement());
  }
}
function movePassage(delta){
  if (state.mode !== 'forward') return;
  var current = relation(state.key);
  var candidate = selectedCandidate(current);
  if (!candidate || !candidate.blocks.length) return;
  state.passageIndex =
    (state.passageIndex + delta + candidate.blocks.length) %
    candidate.blocks.length;
  renderForwardBar();
  focusWithoutScroll(forwardBar);
  applyForwardHighlights();
  announce(forwardAnnouncement(current));
}
function activateGate(claimKey, gateId, fromId){
  var entries = DATA.claimGates[claimKey] || [];
  for (var index = 0; index < entries.length; index += 1){
    if (entries[index].gate.gateId !== gateId) continue;
    clearSelection(false);
    state = emptyState();
    state.mode = 'claim-gate';
    state.key = claimKey;
    state.returnFocus = fromId;
    forwardBar.textContent = '';
    forwardBar.appendChild(element('div', 'mode', ui('forwardMode')));
    forwardBar.appendChild(element('div', 'context',
      format(ui('claimGateContext'), {
        prefix:DATA.edition.prefix, number:claimKey.split('-')[1]
      })));
    forwardBar.appendChild(cautionControl(entries[index].gate));
    forwardBar.appendChild(element(
      'div', 'disposition', entries[index].disposition.text));
    forwardBar.appendChild(clearControl());
    forwardBar.hidden = false;
    focusWithoutScroll(forwardBar);
    announce(format(ui('claimGateAnnouncement'), {
      prefix:DATA.edition.prefix, number:claimKey.split('-')[1]
    }) + ' — ' + ui('gatePresent'));
    return;
  }
}

document.addEventListener('click', function(event){
  var control = event.target.closest ? event.target.closest('button') : null;
  if (control){
    if (control.dataset.reader){
      var details = document.getElementById(control.dataset.readerDetails);
      var readerTarget = document.getElementById(control.dataset.reader);
      if (details) details.open = true;
      if (readerTarget){
        readerTarget.focus({preventScroll:true});
        scrollDisclosureToNode(control.dataset.reader);
      }
      return;
    }
    if (control.dataset.relation){
      activateForward(control.dataset.relation, control.id);
      return;
    }
    if (control.dataset.block){
      activateReverse(control.dataset.block, control.id);
      return;
    }
    if (control.dataset.goto){
      scrollClaimsToNode(control.dataset.goto, 'start');
      return;
    }
    if (control.dataset.gate){
      activateGate(control.dataset.claim, control.dataset.gate, control.id);
      return;
    }
    if (control.dataset.aux){
      var open = document.body.classList.toggle('aux-open');
      control.setAttribute('aria-pressed', open ? 'true' : 'false');
      return;
    }
    return;
  }
  var surface = event.target.closest ? event.target.closest('.pointer-surface') : null;
  if (!surface) return;
  var selection = window.getSelection && window.getSelection();
  if (selection && selection.toString().length) return;
  var current = relation(surface.dataset.relation);
  activateForward(surface.dataset.relation,
    current ? current.subjectControlId : null);
});

document.addEventListener('keydown', function(event){
  if (event.key === 'Escape' && state.mode){
    clearSelection(true);
    return;
  }
  if ((event.key === 'ArrowLeft' || event.key === 'ArrowRight') &&
      (state.mode === 'forward' || state.mode === 'reverse')){
    var bar = state.mode === 'forward' ? forwardBar : reverseBar;
    if (bar.contains(document.activeElement)){
      event.preventDefault();
      moveCandidate(event.key === 'ArrowLeft' ? -1 : 1);
    }
  }
  if ((event.key === 'ArrowUp' || event.key === 'ArrowDown') &&
      state.mode === 'forward' && forwardBar.contains(document.activeElement)){
    event.preventDefault();
    movePassage(event.key === 'ArrowUp' ? -1 : 1);
  }
});
"""
