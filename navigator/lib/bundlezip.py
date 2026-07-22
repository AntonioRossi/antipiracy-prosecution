"""Deterministic STORE ZIP — the single in-repo bundle writer (TDD §10.9).

Fixed member ordering (as enumerated by the bundle config), STORE method
(no compression), declared timestamps, fixed permissions (0644), pinned
UTF-8 filename flag (bit 11), and a plain central directory. Verified
against a byte-exact golden bundle fixture.
"""

import struct
import zlib

_UTF8_FLAG = 0x0800
_EXT_ATTRS = (0o100644 << 16)


def _dos_datetime(ts):
    """Declared timestamp 'YYYY-MM-DDTHH:MM:SSZ' -> DOS date/time words."""
    y, mo, d = int(ts[0:4]), int(ts[5:7]), int(ts[8:10])
    h, mi, s = int(ts[11:13]), int(ts[14:16]), int(ts[17:19])
    return (((y - 1980) << 9) | (mo << 5) | d,
            (h << 11) | (mi << 5) | (s // 2))


def build_zip(members, declared_timestamp):
    """members: ordered list of (arcname, bytes). Returns ZIP bytes."""
    ddate, dtime = _dos_datetime(declared_timestamp)
    out = bytearray()
    central = bytearray()
    for arcname, data in members:
        name = arcname.encode("utf-8")
        crc = zlib.crc32(data) & 0xFFFFFFFF
        offset = len(out)
        out += struct.pack(
            "<4sHHHHHIIIHH", b"PK\x03\x04", 20, _UTF8_FLAG, 0,
            dtime, ddate, crc, len(data), len(data), len(name), 0)
        out += name
        out += data
        central += struct.pack(
            "<4sHHHHHHIIIHHHHHII", b"PK\x01\x02", (3 << 8) | 20, 20,
            _UTF8_FLAG, 0, dtime, ddate, crc, len(data), len(data),
            len(name), 0, 0, 0, 0, _EXT_ATTRS, offset)
        central += name
    cd_offset = len(out)
    out += central
    out += struct.pack(
        "<4sHHHHIIH", b"PK\x05\x06", 0, 0, len(members), len(members),
        len(central), cd_offset, 0)
    return bytes(out)
