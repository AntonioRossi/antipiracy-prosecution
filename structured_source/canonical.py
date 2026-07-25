"""Pinned XML canonicalization and domain-separated semantic identities.

``xc1`` is the repository profile of Canonical XML 1.1 without comments.
The secure parser excludes the C14N 1.1 features that require inherited
``xml:*`` fixup or arbitrary namespace-prefix recovery.  Canonical packages
use one default artifact namespace plus the reserved ``xml`` namespace, so
this serializer implements the complete remaining C14N 1.1 byte law rather
than depending on a platform XML utility.
"""

from __future__ import annotations

import hashlib
import struct
from xml.etree import ElementTree as ET

from . import (CANON_VERSION, CONTENT_NAMESPACE, DIGEST_DOMAIN_VERSION,
               RELATIONS_NAMESPACE, SCHEMA_VERSION)
from .errors import StructuredSourceError

XML_NAMESPACE = "http://www.w3.org/XML/1998/namespace"
SEMANTIC_DIGEST_PREFIX = "sha256/xc1/ssp-xd1:"
RAW_DIGEST_PREFIX = "sha256/raw:"

_KIND_CONTRACT = {
    "content-document": {
        "namespace": CONTENT_NAMESPACE,
        "root": "source",
        "identityPath": "documentIdentity",
        "identityAttribute": "documentId",
    },
    "relation-set": {
        "namespace": RELATIONS_NAMESPACE,
        "root": "relations",
        "identityPath": "identity",
        "identityAttribute": "relationSetId",
    },
    "content-fragment": {
        "namespace": CONTENT_NAMESPACE,
        "root": None,
        "identityPath": None,
        "identityAttribute": "{http://www.w3.org/XML/1998/namespace}id",
    },
    "relation": {
        "namespace": RELATIONS_NAMESPACE,
        "root": "relation",
        "identityPath": None,
        "identityAttribute": "relationId",
    },
    "relation-context-fragment": {
        "namespace": CONTENT_NAMESPACE,
        "root": None,
        "identityPath": None,
        "identityAttribute": "{http://www.w3.org/XML/1998/namespace}id",
    },
}


def raw_digest(data: bytes) -> str:
    if not isinstance(data, bytes):
        raise TypeError("raw digest input must be bytes")
    return RAW_DIGEST_PREFIX + hashlib.sha256(data).hexdigest()


def _split_qname(value: str) -> tuple[str, str]:
    if value.startswith("{"):
        namespace, local = value[1:].split("}", 1)
        return namespace, local
    return "", value


def _element_name(value: str, artifact_namespace: str) -> str:
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
        "xc1 encountered an undeclared namespace %s" % namespace)


def _escape_text(value: str) -> str:
    # C14N 1.1 escapes '>' only where it would close a CDATA section.
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(
        "\r", "&#xD;").replace("]]>", "]]&gt;")


def _escape_attribute(value: str) -> str:
    return (value.replace("&", "&amp;").replace("<", "&lt;")
            .replace('"', "&quot;").replace("\t", "&#x9;")
            .replace("\n", "&#xA;").replace("\r", "&#xD;"))


def canonical_bytes(element: ET.Element) -> bytes:
    """Serialize a validated artifact root or fragment under ``xc1``."""
    if not isinstance(element, ET.Element):
        raise TypeError("xc1 input must be an Element")
    artifact_namespace, unused_local = _split_qname(element.tag)
    if artifact_namespace not in {CONTENT_NAMESPACE, RELATIONS_NAMESPACE}:
        raise StructuredSourceError("xc1 root namespace is not registered")
    output: list[str] = []
    used_namespaces = {
        _split_qname(node.tag)[0] for node in element.iter()
        if isinstance(node.tag, str)
    }
    if not used_namespaces.issubset({CONTENT_NAMESPACE, RELATIONS_NAMESPACE}):
        raise StructuredSourceError("xc1 artifact contains an unregistered namespace")

    def visit(node: ET.Element, is_root: bool) -> None:
        if not isinstance(node.tag, str):
            raise StructuredSourceError("xc1 excludes comments and processing instructions")
        namespace, unused = _split_qname(node.tag)
        if namespace not in used_namespaces:
            raise StructuredSourceError("xc1 artifact contains a foreign element namespace")
        name = _element_name(node.tag, artifact_namespace)
        output.extend(("<", name))
        if is_root:
            output.extend((' xmlns="', _escape_attribute(artifact_namespace), '"'))
            if CONTENT_NAMESPACE in used_namespaces and \
                    artifact_namespace != CONTENT_NAMESPACE:
                output.extend((' xmlns:c="', CONTENT_NAMESPACE, '"'))
            if RELATIONS_NAMESPACE in used_namespaces and \
                    artifact_namespace != RELATIONS_NAMESPACE:
                output.extend((' xmlns:r="', RELATIONS_NAMESPACE, '"'))
        attributes = []
        for qname, value in node.attrib.items():
            attr_namespace, local = _split_qname(qname)
            if attr_namespace not in {"", XML_NAMESPACE}:
                raise StructuredSourceError("xc1 artifact contains a foreign attribute namespace")
            attributes.append((attr_namespace, local, qname, value))
        for unused_namespace, unused_local, qname, value in sorted(attributes):
            output.extend((" ", _element_name(qname, artifact_namespace),
                           '="', _escape_attribute(value), '"'))
        output.append(">")
        if node.text:
            output.append(_escape_text(node.text))
        for child in node:
            visit(child, False)
            if child.tail:
                output.append(_escape_text(child.tail))
        output.extend(("</", name, ">"))

    visit(element, True)
    return "".join(output).encode("utf-8")


def _frame_field(value: str) -> bytes:
    encoded = value.encode("utf-8")
    return struct.pack(">Q", len(encoded)) + encoded


def subject_id(element: ET.Element, artifact_kind: str) -> str:
    try:
        contract = _KIND_CONTRACT[artifact_kind]
    except KeyError as exc:
        raise StructuredSourceError(
            "semantic digest artifact kind is not registered: %s" % artifact_kind) from exc
    namespace, local = _split_qname(element.tag)
    if namespace != contract["namespace"]:
        raise StructuredSourceError("artifact kind and namespace disagree")
    required_root = contract["root"]
    if required_root is not None and local != required_root:
        raise StructuredSourceError("artifact kind and root element disagree")
    identity_path = contract["identityPath"]
    identity_node = element
    if identity_path is not None:
        identity_node = element.find("{%s}%s" % (namespace, identity_path))
        if identity_node is None:
            raise StructuredSourceError("artifact identity element is missing")
    value = identity_node.get(contract["identityAttribute"])
    if not value:
        raise StructuredSourceError("artifact stable subject identity is missing")
    return value


def semantic_digest(element: ET.Element, artifact_kind: str,
                    schema_profile: str) -> str:
    """Return the ``sha256/xc1/ssp-xd1`` digest for one exact subject."""
    contract = _KIND_CONTRACT.get(artifact_kind)
    if contract is None:
        raise StructuredSourceError(
            "semantic digest artifact kind is not registered: %s" % artifact_kind)
    fields = (
        "aa11393:ssp:xml-digest",
        DIGEST_DOMAIN_VERSION,
        CANON_VERSION,
        artifact_kind,
        contract["namespace"],
        schema_profile,
        SCHEMA_VERSION,
        subject_id(element, artifact_kind),
    )
    payload = b"".join(_frame_field(field) for field in fields)
    canonical = canonical_bytes(element)
    payload += struct.pack(">Q", len(canonical)) + canonical
    return SEMANTIC_DIGEST_PREFIX + hashlib.sha256(payload).hexdigest()


def registered_kinds() -> tuple[str, ...]:
    return tuple(sorted(_KIND_CONTRACT))
