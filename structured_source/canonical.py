"""Readable XML storage, raw-byte bindings, and typed-item identities."""

from __future__ import annotations

import hashlib
from xml.etree import ElementTree as ET

from . import CONTENT_NAMESPACE, RELATIONS_NAMESPACE
from .control import canonical_json
from .errors import StructuredSourceError

XML_NAMESPACE = "http://www.w3.org/XML/1998/namespace"
RAW_DIGEST_PREFIX = "sha256/raw:"
TYPED_ITEM_DIGEST_PREFIX = "sha256/typed-item-v1:"
TYPED_ITEM_DIGEST_DOMAIN = "aa11393:ssp:typed-item:v1"
XML_DECLARATION = b'<?xml version="1.0" encoding="UTF-8"?>\n'

def raw_digest(data: bytes) -> str:
    if not isinstance(data, bytes):
        raise TypeError("raw digest input must be bytes")
    return RAW_DIGEST_PREFIX + hashlib.sha256(data).hexdigest()


def _split_qname(value: str) -> tuple[str, str]:
    if value.startswith("{"):
        namespace, local = value[1:].split("}", 1)
        return namespace, local
    return "", value


def strip_structural_whitespace(element: ET.Element) -> ET.Element:
    """Remove indentation from a parsed element-only tree in place.

    The content schemas represent semantic character data in leaf elements.
    Whitespace between child elements is therefore storage syntax, while all
    text in a leaf remains exact typed content.  A mixed-content shape is not
    silently normalized: it fails before any digest or surface is built.
    """
    if not isinstance(element, ET.Element):
        raise TypeError("readable XML input must be an Element")
    for node in element.iter():
        children = list(node)
        if children:
            if node.text is not None and node.text.strip():
                raise StructuredSourceError(
                    "readable XML container contains untyped character data")
            node.text = None
            for child in children:
                if child.tail is not None and child.tail.strip():
                    raise StructuredSourceError(
                        "readable XML child has untyped trailing character data")
                child.tail = None
    element.tail = None
    return element


def _readable_name(value: str, artifact_namespace: str) -> str:
    namespace, local = _split_qname(value)
    if namespace == artifact_namespace:
        return local
    if namespace == XML_NAMESPACE:
        return "xml:" + local
    if namespace == CONTENT_NAMESPACE:
        return "c:" + local
    if namespace == RELATIONS_NAMESPACE:
        return "r:" + local
    if not namespace:
        return local
    raise StructuredSourceError(
        "readable XML encountered an undeclared namespace %s" % namespace)


def _readable_text(value: str) -> str:
    return (value.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace("\t", "&#x9;")
            .replace("\n", "&#xA;").replace("\r", "&#xD;"))


def _readable_attribute(value: str) -> str:
    return (value.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;")
            .replace("\t", "&#x9;").replace("\n", "&#xA;")
            .replace("\r", "&#xD;"))


def readable_xml_bytes(element: ET.Element) -> bytes:
    """Serialize one stripped typed tree under the readable XML storage law."""
    if not isinstance(element, ET.Element):
        raise TypeError("readable XML input must be an Element")
    artifact_namespace, unused_local = _split_qname(element.tag)
    if artifact_namespace not in {CONTENT_NAMESPACE, RELATIONS_NAMESPACE}:
        raise StructuredSourceError(
            "readable XML root namespace is not registered")
    used_namespaces = {
        _split_qname(node.tag)[0] for node in element.iter()
        if isinstance(node.tag, str)
    }
    if not used_namespaces.issubset({CONTENT_NAMESPACE, RELATIONS_NAMESPACE}):
        raise StructuredSourceError(
            "readable XML contains an unregistered element namespace")
    prefixes = []
    if CONTENT_NAMESPACE in used_namespaces and \
            artifact_namespace != CONTENT_NAMESPACE:
        prefixes.append(("c", CONTENT_NAMESPACE))
    if RELATIONS_NAMESPACE in used_namespaces and \
            artifact_namespace != RELATIONS_NAMESPACE:
        prefixes.append(("r", RELATIONS_NAMESPACE))
    prefixes.sort()
    lines: list[str] = []

    def visit(node: ET.Element, depth: int, is_root: bool) -> None:
        if not isinstance(node.tag, str):
            raise StructuredSourceError(
                "readable XML excludes comments and processing instructions")
        children = list(node)
        if children and node.text is not None:
            raise StructuredSourceError(
                "readable XML tree retains structural character data")
        if node.tail is not None:
            raise StructuredSourceError(
                "readable XML tree retains structural trailing data")
        indent = "  " * depth
        name = _readable_name(node.tag, artifact_namespace)
        start = [indent, "<", name]
        if is_root:
            start.extend((' xmlns="', _readable_attribute(artifact_namespace), '"'))
            for prefix, namespace in prefixes:
                start.extend((" xmlns:", prefix, '="',
                              _readable_attribute(namespace), '"'))
        attributes = []
        for qname, value in node.attrib.items():
            namespace, local = _split_qname(qname)
            if namespace not in {"", XML_NAMESPACE}:
                raise StructuredSourceError(
                    "readable XML contains a foreign attribute namespace")
            attributes.append((namespace, local, qname, value))
        for unused_namespace, unused_name, qname, value in sorted(attributes):
            start.extend((" ", _readable_name(qname, artifact_namespace),
                          '="', _readable_attribute(value), '"'))
        if not children and not node.text:
            start.append(" />")
            lines.append("".join(start))
            return
        if not children:
            start.extend((">", _readable_text(node.text or ""), "</", name, ">"))
            lines.append("".join(start))
            return
        start.append(">")
        lines.append("".join(start))
        for child in children:
            visit(child, depth + 1, False)
        lines.append(indent + "</" + name + ">")

    visit(element, 0, True)
    return XML_DECLARATION + ("\n".join(lines) + "\n").encode("utf-8")


def typed_item_record(*, authority_scheme: str, schema_profile: str,
                      document_id: str, item_id: str, item_type: str,
                      typed_content, substantive_metadata) -> dict:
    """Construct exactly one closed content-item record."""
    return {
        "authorityScheme": authority_scheme,
        "digestDomain": TYPED_ITEM_DIGEST_DOMAIN,
        "documentId": document_id,
        "itemId": item_id,
        "itemType": item_type,
        "schemaProfile": schema_profile,
        "substantiveMetadata": substantive_metadata,
        "typedContent": typed_content,
    }


def typed_item_digest(*, authority_scheme: str, schema_profile: str,
                      document_id: str, item_id: str, item_type: str,
                      typed_content, substantive_metadata) -> str:
    """Hash exactly one closed content-item record under ``c1``."""
    record = typed_item_record(
        authority_scheme=authority_scheme, schema_profile=schema_profile,
        document_id=document_id, item_id=item_id, item_type=item_type,
        typed_content=typed_content, substantive_metadata=substantive_metadata)
    payload = canonical_json(record)
    return TYPED_ITEM_DIGEST_PREFIX + hashlib.sha256(payload).hexdigest()
