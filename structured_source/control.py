"""Closed deterministic JSON control serialization (``c1``)."""

from __future__ import annotations

import hashlib
import json
import math
import unicodedata

from .errors import StructuredSourceError


def _validate(value, path="$" ):
    if value is None or isinstance(value, (bool, str)):
        if isinstance(value, str) and unicodedata.normalize("NFC", value) != value:
            raise StructuredSourceError("control string is not NFC at %s" % path)
        return
    if isinstance(value, int) and not isinstance(value, bool):
        if abs(value) > 9007199254740991:
            raise StructuredSourceError("control integer exceeds the c1 range at %s" % path)
        return
    if isinstance(value, float):
        raise StructuredSourceError("control JSON floats are prohibited at %s" % path)
    if isinstance(value, list):
        for index, item in enumerate(value):
            _validate(item, "%s[%d]" % (path, index))
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise StructuredSourceError("control object key is not a string at %s" % path)
            _validate(key, "%s.<key>" % path)
            _validate(item, "%s.%s" % (path, key))
        return
    raise StructuredSourceError("unsupported control value at %s" % path)


def canonical_json(value) -> bytes:
    _validate(value)
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def control_digest(value) -> str:
    return "sha256/c1:" + hashlib.sha256(canonical_json(value)).hexdigest()


def parse_json(data: bytes):
    if not isinstance(data, bytes):
        raise TypeError("control JSON input must be bytes")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise StructuredSourceError("control JSON is not UTF-8") from exc

    def pairs(items):
        result = {}
        normalized = set()
        for key, value in items:
            if not isinstance(key, str):
                raise StructuredSourceError("control JSON key is not a string")
            nfc = unicodedata.normalize("NFC", key)
            if nfc != key or nfc in normalized:
                raise StructuredSourceError("control JSON has a non-NFC or duplicate key")
            normalized.add(nfc)
            result[key] = value
        return result

    try:
        value = json.loads(text, object_pairs_hook=pairs,
                           parse_float=lambda unused: (_ for _ in ()).throw(
                               StructuredSourceError("control JSON floats are prohibited")),
                           parse_constant=lambda unused: (_ for _ in ()).throw(
                               StructuredSourceError("control JSON constants are prohibited")))
    except (json.JSONDecodeError, StructuredSourceError) as exc:
        if isinstance(exc, StructuredSourceError):
            raise
        raise StructuredSourceError("control JSON is malformed: %s" % exc) from exc
    _validate(value)
    return value
