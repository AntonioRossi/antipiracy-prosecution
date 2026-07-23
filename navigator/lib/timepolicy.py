"""Canonical timestamp policy shared without importing bundle control code."""

import datetime
import re


UTC_SECOND_RE = re.compile(
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")


class TimestampError(ValueError):
    pass


def parse_utc_second(value, label="declaredTimestamp"):
    """Parse one canonical RFC 3339 UTC timestamp at second precision."""
    if not isinstance(value, str) or UTC_SECOND_RE.fullmatch(value) is None:
        raise TimestampError(
            "%s must be a canonical RFC 3339 UTC second" % label)
    try:
        parsed = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        raise TimestampError("%s must be a real RFC 3339 UTC second" % label)
    if parsed.strftime("%Y-%m-%dT%H:%M:%SZ") != value:
        raise TimestampError("%s must use canonical UTC-second form" % label)
    return parsed
