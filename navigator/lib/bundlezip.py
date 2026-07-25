"""Strict deterministic delivery-bundle construction."""

from __future__ import annotations

from datetime import datetime, timezone
import io
import re
import stat
import unicodedata
import zipfile


BUNDLE_CONFIG_PATH = "navigator/bundles/na-af-2026.json"
BUNDLE_VERSION = "4"
BUNDLE_WORDING_ID = "bundle-manifest-neutral"
EDITION_IDS = ("na", "af")

_BASENAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,239}\Z")
_TIMESTAMP = re.compile(
    r"(19[89][0-9]|20[0-9]{2}|21[0-9]{2})-"
    r"(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])T"
    r"([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]Z\Z")
_EDITION_ARTIFACT = {
    "na": re.compile(
        r"AA11393US-NA-claims-spec-navigator_(NA-[A-Za-z0-9.-]+)\.html\Z"),
    "af": re.compile(
        r"AA11393US-AF-claims-spec-navigator_(AF-[A-Za-z0-9.-]+)\.html\Z"),
}


class BundleError(ValueError):
    """Bundle structure, bytes, or deterministic metadata are invalid."""


def validate_member_name(value):
    stem = value.split(".", 1)[0].casefold() \
        if isinstance(value, str) else ""
    reserved = {"con", "prn", "aux", "nul"} | {
        "%s%d" % (prefix, number)
        for prefix in ("com", "lpt") for number in range(1, 10)}
    if not isinstance(value, str) or _BASENAME.fullmatch(value) is None or \
            unicodedata.normalize("NFC", value) != value or \
            value in {".", ".."} or value.endswith(".") or stem in reserved:
        raise BundleError("bundle member must be one canonical safe basename")
    return value


def parse_utc_second(value):
    if not isinstance(value, str) or _TIMESTAMP.fullmatch(value) is None:
        raise BundleError("bundle timestamp must be a canonical UTC second")
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc)
    except ValueError as exc:
        raise BundleError("bundle timestamp is not a real UTC second") from exc
    if parsed.year < 1980:
        raise BundleError("bundle timestamp predates the ZIP epoch")
    return parsed


def _zip_datetime(value):
    parsed = parse_utc_second(value)
    # ZIP stores seconds in two-second increments.  Odd seconds would not
    # round-trip exactly and are therefore outside the current contract.
    if parsed.second % 2:
        raise BundleError("bundle timestamp second must be even")
    return (parsed.year, parsed.month, parsed.day,
            parsed.hour, parsed.minute, parsed.second)


def _validated_members(members):
    if not isinstance(members, (list, tuple)) or len(members) != 5:
        raise BundleError("delivery bundle must contain exactly five members")
    normalized = []
    names = []
    for index, member in enumerate(members):
        if not isinstance(member, (list, tuple)) or len(member) != 2:
            raise BundleError("bundle member %d is not a (name, bytes) pair" % index)
        name, data = member
        validate_member_name(name)
        if not isinstance(data, bytes):
            raise BundleError("bundle member %s is not bytes" % name)
        names.append(name)
        normalized.append((name, data))
    if len(names) != len(set(name.casefold() for name in names)):
        raise BundleError("bundle member names are not unique")
    if names[-1] != "MANIFEST.txt":
        raise BundleError("MANIFEST.txt must be the final configured member")
    return normalized


def build_zip(members, declared_timestamp):
    """Return byte-identical ZIP_STORED bytes for five ordered members."""
    members = _validated_members(members)
    date_time = _zip_datetime(declared_timestamp)
    output = io.BytesIO()
    with zipfile.ZipFile(
            output, mode="w", compression=zipfile.ZIP_STORED,
            allowZip64=False, strict_timestamps=True) as archive:
        archive.comment = b""
        for name, data in members:
            info = zipfile.ZipInfo(name, date_time=date_time)
            info.create_system = 3
            info.create_version = 20
            info.extract_version = 20
            info.compress_type = zipfile.ZIP_STORED
            info.comment = b""
            info.extra = b""
            info.internal_attr = 0
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, data)
    return output.getvalue()


def read_zip_members(data):
    """Return ordered member pairs after enforcing current ZIP metadata."""
    if not isinstance(data, bytes):
        raise BundleError("bundle ZIP is not bytes")
    try:
        with zipfile.ZipFile(io.BytesIO(data), mode="r") as archive:
            if archive.comment:
                raise BundleError("bundle ZIP comment must be empty")
            infos = archive.infolist()
            if len(infos) != 5:
                raise BundleError("delivery bundle must contain exactly five members")
            members = []
            for info in infos:
                validate_member_name(info.filename)
                if info.is_dir() or info.compress_type != zipfile.ZIP_STORED or \
                        info.comment or info.extra or info.flag_bits & 0x1 or \
                        (info.external_attr >> 16) != (stat.S_IFREG | 0o644):
                    raise BundleError(
                        "bundle member metadata is not the deterministic profile")
                members.append((info.filename, archive.read(info)))
    except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
        raise BundleError("delivery bundle is not a readable ZIP") from exc
    return _validated_members(members)


def validate_bundle_config(value):
    if not isinstance(value, dict) or set(value) != {
            "bundleVersion", "declaredTimestamp", "editions",
            "manifestWordingId", "members", "name"} or \
            value.get("bundleVersion") != BUNDLE_VERSION or \
            value.get("editions") != list(EDITION_IDS) or \
            value.get("manifestWordingId") != BUNDLE_WORDING_ID:
        raise BundleError("bundle configuration shape/version is not current")
    _zip_datetime(value.get("declaredTimestamp"))
    name = validate_member_name(value.get("name"))
    if not name.endswith("_TECHNICAL-PREVIEW.zip"):
        raise BundleError("bundle name does not identify the current profile")

    members = value.get("members")
    if not isinstance(members, list) or len(members) != 5:
        raise BundleError("bundle configuration must enumerate five members")
    expected_kinds = (
        "sealed", "artifact-checksum", "sealed", "artifact-checksum",
        "manifest")
    seen_names = []
    for index, (entry, expected_kind) in enumerate(zip(members, expected_kinds)):
        if not isinstance(entry, dict) or entry.get("kind") != expected_kind:
            raise BundleError("bundle member %d has the wrong kind" % index)
        if expected_kind == "sealed":
            if set(entry) != {"edition", "kind", "name"} or \
                    entry.get("edition") != EDITION_IDS[index // 2] or \
                    not entry.get("name", "").endswith(".html"):
                raise BundleError("sealed bundle member is malformed")
        elif expected_kind == "artifact-checksum":
            if set(entry) != {"artifact", "edition", "kind", "name"} or \
                    entry.get("edition") != EDITION_IDS[index // 2] or \
                    entry.get("artifact") != members[index - 1].get("name") or \
                    entry.get("name") != entry.get("artifact") + ".sha256":
                raise BundleError("artifact-checksum member is malformed")
        elif set(entry) != {"kind", "name"} or \
                entry.get("name") != "MANIFEST.txt":
            raise BundleError("bundle manifest member is malformed")
        seen_names.append(validate_member_name(entry.get("name")))
    if len(seen_names) != len(set(name.casefold() for name in seen_names)):
        raise BundleError("bundle configuration has duplicate member names")
    versions = []
    for edition, entry in zip(EDITION_IDS, (members[0], members[2])):
        match = _EDITION_ARTIFACT[edition].fullmatch(entry["name"])
        if match is None:
            raise BundleError("sealed member name is not bound to its edition")
        versions.append(match.group(1))
    expected_name = (
        "AA11393US-claims-navigators_%s_%s_TECHNICAL-PREVIEW.zip" %
        tuple(versions))
    if name != expected_name:
        raise BundleError("bundle name is not derived from the exact editions")
    return value
