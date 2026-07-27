"""Closed profile-owned content grammar and deterministic XSD rendering."""

from __future__ import annotations

from dataclasses import dataclass
import re
from types import MappingProxyType
from typing import Mapping

from .errors import StructuredSourceError


XSD_NAMESPACE = "http://www.w3.org/2001/XMLSchema"
VERSIONING_NAMESPACE = "http://www.w3.org/2007/XMLSchema-versioning"
XML_NAMESPACE = "http://www.w3.org/XML/1998/namespace"
CONTENT_NAMESPACE = "urn:aa11393:ssp:content:1"
CONTENT_XSD_PATH = "structured_source/schemas/content.xsd"

_GRAMMAR_FIELDS = {"namespaces", "root"}
_NODE_FIELDS = {"attributes", "children", "tag"}
_NAMESPACES = {
    "c": CONTENT_NAMESPACE,
    "vc": VERSIONING_NAMESPACE,
    "xml": XML_NAMESPACE,
    "xs": XSD_NAMESPACE,
}
_TAGS = frozenset({
    "assert", "attribute", "choice", "complexContent", "complexType",
    "element", "enumeration", "extension", "group", "import",
    "maxInclusive", "maxLength", "minInclusive", "minLength", "pattern",
    "restriction", "schema", "sequence", "simpleContent", "simpleType",
    "union",
})
_ATTRIBUTES = frozenset({
    "attributeFormDefault", "base", "elementFormDefault", "fixed",
    "maxOccurs", "memberTypes", "minOccurs", "name", "namespace", "ref",
    "schemaLocation", "targetNamespace", "test", "type", "use", "value",
    "version", "vc:minVersion",
})
_LOCAL_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_.-]*\Z")
_PREFIXES = frozenset(_NAMESPACES)
_MAX_GRAMMAR_NODES = 4096
_MAX_GRAMMAR_DEPTH = 64


@dataclass(frozen=True, slots=True)
class GrammarNode:
    """One immutable node in the current closed XSD grammar AST."""

    tag: str
    attributes: Mapping[str, str]
    children: tuple["GrammarNode", ...]


@dataclass(frozen=True, slots=True)
class ContentGrammar:
    """The complete immutable profile-owned content grammar."""

    namespaces: Mapping[str, str]
    root: GrammarNode
    production_paths: tuple[str, ...]


def _validate_qname(value: str, label: str) -> None:
    for token in value.split():
        parts = token.split(":", 1)
        if len(parts) == 2:
            prefix, local = parts
            if prefix not in _PREFIXES or _LOCAL_NAME.fullmatch(local) is None:
                raise StructuredSourceError(
                    "content grammar QName is malformed at %s" % label)
        elif _LOCAL_NAME.fullmatch(token) is None:
            raise StructuredSourceError(
                "content grammar name is malformed at %s" % label)


def parse_content_grammar(value) -> ContentGrammar:
    """Validate and freeze the sole current content-grammar representation."""
    if not isinstance(value, dict) or set(value) != _GRAMMAR_FIELDS or \
            value.get("namespaces") != _NAMESPACES:
        raise StructuredSourceError("content grammar envelope is not current")
    node_count = 0
    paths = []

    def parse_node(node, path: str, depth: int) -> GrammarNode:
        nonlocal node_count
        node_count += 1
        if node_count > _MAX_GRAMMAR_NODES or depth > _MAX_GRAMMAR_DEPTH:
            raise StructuredSourceError(
                "content grammar exceeds the closed resource limits")
        if not isinstance(node, dict) or set(node) != _NODE_FIELDS:
            raise StructuredSourceError(
                "content grammar node shape is not current at %s" % path)
        tag = node.get("tag")
        attributes = node.get("attributes")
        children = node.get("children")
        if tag not in _TAGS or not isinstance(attributes, dict) or \
                not isinstance(children, list) or any(
                    name not in _ATTRIBUTES or not isinstance(item, str)
                    for name, item in attributes.items()):
            raise StructuredSourceError(
                "content grammar node is unsupported at %s" % path)
        if len(attributes) != len(set(attributes)):
            raise StructuredSourceError(
                "content grammar attribute is duplicated at %s" % path)
        for name in ("name", "ref", "type", "base"):
            if name in attributes:
                _validate_qname(attributes[name], path + "." + name)
        if "memberTypes" in attributes:
            _validate_qname(attributes["memberTypes"], path + ".memberTypes")
        identifier = attributes.get("name") or attributes.get("ref") or str(
            len(paths))
        current_path = "%s/%s[%s]" % (path, tag, identifier)
        paths.append(current_path)
        frozen_children = tuple(
            parse_node(child, current_path, depth + 1)
            for child in children)
        return GrammarNode(
            tag=tag,
            attributes=MappingProxyType(dict(attributes)),
            children=frozen_children,
        )

    root = parse_node(value.get("root"), "$", 0)
    if root.tag != "schema" or root.attributes != {
            "attributeFormDefault": "unqualified",
            "elementFormDefault": "qualified",
            "targetNamespace": CONTENT_NAMESPACE,
            "vc:minVersion": "1.1",
            "version": "1",
    }:
        raise StructuredSourceError("content grammar root is not current")
    return ContentGrammar(
        namespaces=MappingProxyType(dict(_NAMESPACES)),
        root=root,
        production_paths=tuple(paths),
    )


def _escape_attribute(value: str) -> str:
    return (value.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;")
            .replace("\t", "&#x9;").replace("\n", "&#xA;")
            .replace("\r", "&#xD;"))


def render_content_xsd(grammar: ContentGrammar) -> bytes:
    """Render deterministic XSD bytes from the validated authoritative AST."""
    if not isinstance(grammar, ContentGrammar):
        raise TypeError("content XSD renderer requires validated grammar")
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']

    def render(node: GrammarNode, depth: int, root: bool = False) -> None:
        indent = "  " * depth
        start = [indent, "<xs:", node.tag]
        if root:
            for prefix in ("xs", "vc", "c", "xml"):
                start.extend((" xmlns:", prefix, '="',
                              _escape_attribute(grammar.namespaces[prefix]), '"'))
        for name in sorted(node.attributes):
            start.extend((" ", name, '="',
                          _escape_attribute(node.attributes[name]), '"'))
        if not node.children:
            start.append("/>")
            lines.append("".join(start))
            return
        start.append(">")
        lines.append("".join(start))
        for child in node.children:
            render(child, depth + 1)
        lines.append("%s</xs:%s>" % (indent, node.tag))

    render(grammar.root, 0, True)
    return ("\n".join(lines) + "\n").encode("utf-8")
