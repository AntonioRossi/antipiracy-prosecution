"""Shared operator-authority policy for review and release evidence.

Every approval must carry an explicit operator kind and identity.  Human and
model operators may authorize release evidence; tools may create or migrate
data but can never approve it.
"""

import re
import unicodedata

from .unicode15_1 import normalize_nfc


AUTHORITATIVE_OPERATOR_KINDS = frozenset(("human", "model"))

_NONFINAL_EVIDENCE_PATTERNS = tuple(re.compile(pattern, re.IGNORECASE) for
                                    pattern in (
    r"\bpending\b",
    r"\bawaiting\b",
    r"\bnot\s+approved\b",
    r"\bnot\s+confirmed\b",
    r"\bunconfirmed\b",
    r"\bnot\s+complete\b",
    r"\bincomplete\b",
    r"\bnot\s+run\b",
    r"\bnot\s+tested\b",
    r"\btodo\b",
    r"\btbd\b",
    r"\bfailed\b",
    r"\bfailures?\b",
    r"\brejected\b",
    r"\brejections?\b",
    r"\bskipped\b",
    r"\bdid\s+not\s+pass\b",
    r"\bunable\s+to\b",
    r"\bdo(?:\s+|-)+not(?:\s+|-)+release\b",
))


def is_identified_operator_identity(identity):
    """Return whether *identity* contains a visible identifying character.

    ``str.strip`` does not remove default-ignorable format characters such as
    ZERO WIDTH SPACE, WORD JOINER, or bidi marks.  An audit identity must be
    exact NFC with no leading/trailing whitespace and no Unicode ``C*``
    character anywhere.  It also needs at least one Unicode letter, number,
    punctuation character, or symbol; combining marks cannot identify an
    operator without a visible base.
    """
    if not isinstance(identity, str) or identity != identity.strip() or \
            normalize_nfc(identity) != identity:
        return False
    categories = tuple(unicodedata.category(character)
                       for character in identity)
    return all(not category.startswith("C") for category in categories) and \
        any(category[0] in "LNPS" for category in categories)


def is_final_evidence_text(value):
    """Return whether *value* is visible text without non-final language.

    This deliberately recognizes explicit failure language as non-final even
    when a surrounding status field says ``passed``.  Positive evidence such
    as ``"passed with no errors"`` remains valid.
    """
    return is_identified_operator_identity(value) and not any(
        pattern.search(value) for pattern in _NONFINAL_EVIDENCE_PATTERNS)


def is_authoritative_operator_kind(operator_kind):
    """Return whether *operator_kind* is explicitly release-authoritative."""
    return isinstance(operator_kind, str) and \
        operator_kind in AUTHORITATIVE_OPERATOR_KINDS


def is_authoritative_operator(operator_kind, identity):
    """Return whether explicit kind and identity form an authorized operator."""
    return is_authoritative_operator_kind(operator_kind) and \
        is_identified_operator_identity(identity)


def operator_identity_matches(identity, required_identity):
    """Return whether *identity* exactly equals a non-empty required identity.

    Approval identities are audit fields, so matching is intentionally exact:
    there is no trimming, case folding, aliasing, or implicit default.
    """
    return is_identified_operator_identity(identity) and \
        is_identified_operator_identity(required_identity) and \
        identity == required_identity
