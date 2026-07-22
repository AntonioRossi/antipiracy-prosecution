"""Canonicalization and hashing law — canonVersion c1.

This module is the ONLY digest path in the navigator codebase (TDD §8.2,
guardrail 3; enforced by the single-digest-path test). Every stored digest
carries the canonVersion prefix ``sha256/c1:``.

canonVersion c1 pins Unicode 15.1.0: NFC tables and the White_Space set are
read from that Unicode version. The interpreter's Unicode data version is
asserted at import; a mismatch aborts rather than silently hashing under a
different normalization table.
"""

import hashlib
import unicodedata

CANON_VERSION = "c1"
UNICODE_VERSION = "15.1.0"
DIGEST_PREFIX = "sha256/" + CANON_VERSION + ":"

if unicodedata.unidata_version != UNICODE_VERSION:  # pragma: no cover
    raise RuntimeError(
        "canonVersion %s pins Unicode %s but the interpreter provides %s"
        % (CANON_VERSION, UNICODE_VERSION, unicodedata.unidata_version)
    )

# Unicode 15.1.0 White_Space property — pinned as data, not derived at runtime.
WHITESPACE = frozenset(
    chr(c)
    for c in (
        [0x0009, 0x000A, 0x000B, 0x000C, 0x000D, 0x0020, 0x0085, 0x00A0, 0x1680]
        + list(range(0x2000, 0x200B))
        + [0x2028, 0x2029, 0x202F, 0x205F, 0x3000]
    )
)

# Domain tags (ASCII, never containing NUL) and their declared payload form.
# ``digest-list``: raw binary concatenation of 32-byte digests, in order.
# ``object``: canonical JSON (digests appear as full prefixed strings).
TAGS = {
    "aa11393:claim-agg:c1": "digest-list",
    "aa11393:dep-chain:c1": "digest-list",
    "aa11393:figure:c1": "digest-list",
    "aa11393:review:c1": "object",
    "aa11393:inventory:c1": "object",
    "aa11393:lock:c1": "object",
    "aa11393:qa-record:c1": "object",
    "aa11393:attestation:c1": "object",
    "aa11393:release-record:c1": "object",
    "aa11393:bundle-record:c1": "object",
}

# Cell / row separators of the table serialization.
CELL_SEP = ""
ROW_SEP = ""


class CanonError(ValueError):
    """A value outside the canonical law."""


# ---------------------------------------------------------------------------
# Per-type text rules (canonVersion c1)
# ---------------------------------------------------------------------------

def canon_prose(text):
    """Prose (paragraphs, list items, headings, captions):
    NFC -> collapse every whitespace run to a single space -> trim."""
    text = unicodedata.normalize("NFC", text)
    out = []
    in_ws = False
    for ch in text:
        if ch in WHITESPACE:
            in_ws = True
            continue
        if in_ws and out:
            out.append(" ")
        in_ws = False
        out.append(ch)
    return "".join(out)


def canon_code(text):
    """Code blocks: NFC -> line endings to LF -> strip trailing whitespace
    per line -> preserve line breaks and leading indentation."""
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    stripped = []
    for line in lines:
        end = len(line)
        while end > 0 and line[end - 1] in WHITESPACE:
            end -= 1
        stripped.append(line[:end])
    return "\n".join(stripped)


def canon_table_row(cells):
    """One table row: canonical cell text joined with U+001F."""
    return CELL_SEP.join(canon_prose(c) for c in cells)


def canon_table(rows, caption):
    """Table: rows joined with U+001E, caption appended as a final row."""
    serialized = [canon_table_row(r) for r in rows]
    serialized.append(canon_prose(caption))
    return ROW_SEP.join(serialized)


# ---------------------------------------------------------------------------
# Digests
# ---------------------------------------------------------------------------

def _sha256(data):
    return hashlib.sha256(data).digest()


def format_digest(raw):
    if len(raw) != 32:
        raise CanonError("raw digest must be 32 bytes")
    return DIGEST_PREFIX + raw.hex()


def parse_digest(value):
    """Full prefixed digest string -> raw 32 bytes. Rejects anything else."""
    if not isinstance(value, str) or not value.startswith(DIGEST_PREFIX):
        raise CanonError("not a %s digest: %r" % (DIGEST_PREFIX, value))
    hexpart = value[len(DIGEST_PREFIX):]
    if len(hexpart) != 64 or hexpart.lower() != hexpart:
        raise CanonError("digest must carry the full lowercase sha-256: %r" % value)
    try:
        return bytes.fromhex(hexpart)
    except ValueError:
        raise CanonError("bad digest hex: %r" % value)


def text_digest(canonical_text):
    """Digest of already-canonicalized text (UTF-8)."""
    return format_digest(_sha256(canonical_text.encode("utf-8")))


def bytes_digest(data):
    """Digest of raw bytes (corpus files, artifacts)."""
    return format_digest(_sha256(data))


def composite_digest(tag, payload_or_digests):
    """Framed composite digest: sha256(tag || 0x00 || payload).

    ``digest-list`` tags take a list of prefixed digest strings (composed as
    raw 32-byte values). ``object`` tags take a JSON-able object serialized
    under the canonical-JSON law (digests stay prefixed strings inside it).
    """
    if tag not in TAGS:
        raise CanonError("unregistered domain tag: %r" % tag)
    form = TAGS[tag]
    if form == "digest-list":
        if not isinstance(payload_or_digests, (list, tuple)):
            raise CanonError("%s takes an ordered digest list" % tag)
        payload = b"".join(parse_digest(d) for d in payload_or_digests)
    else:
        payload = canonical_json(payload_or_digests)
    return format_digest(_sha256(tag.encode("ascii") + b"\x00" + payload))


# ---------------------------------------------------------------------------
# Canonical JSON (object composites) — defined by rule, confirmed by vector
# ---------------------------------------------------------------------------

_ESCAPES = {'"': '\\"', "\\": "\\\\", "\n": "\\n", "\r": "\\r", "\t": "\\t"}


def _canon_string(s):
    s = unicodedata.normalize("NFC", s)
    out = ['"']
    for ch in s:
        if ch in _ESCAPES:
            out.append(_ESCAPES[ch])
        elif ord(ch) < 0x20:
            out.append("\\u%04x" % ord(ch))
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def _canon_value(value, out):
    if value is None:
        out.append("null")
    elif value is True:
        out.append("true")
    elif value is False:
        out.append("false")
    elif isinstance(value, int):
        if not (-(2 ** 53) < value < 2 ** 53):
            raise CanonError("integer out of range |n| < 2^53: %r" % value)
        out.append(str(value))  # base-10, no exponent/fraction; int has no -0
    elif isinstance(value, float):
        raise CanonError("numbers are integers only; got float %r" % value)
    elif isinstance(value, str):
        out.append(_canon_string(value))
    elif isinstance(value, (list, tuple)):
        out.append("[")
        for i, item in enumerate(value):
            if i:
                out.append(",")
            _canon_value(item, out)
        out.append("]")
    elif isinstance(value, dict):
        normalized = {}
        for key in value:
            if not isinstance(key, str):
                raise CanonError("object keys must be strings: %r" % key)
            nk = unicodedata.normalize("NFC", key)
            if nk in normalized:
                raise CanonError("object keys collide after NFC: %r" % key)
            normalized[nk] = value[key]
        out.append("{")
        for i, key in enumerate(sorted(normalized)):  # code-point order
            if i:
                out.append(",")
            out.append(_canon_string(key))
            out.append(":")
            _canon_value(normalized[key], out)
        out.append("}")
    else:
        raise CanonError("unserializable value: %r" % (value,))


def canonical_json(value):
    """Canonical JSON bytes (UTF-8) under the c1 law."""
    out = []
    _canon_value(value, out)
    return "".join(out).encode("utf-8")
