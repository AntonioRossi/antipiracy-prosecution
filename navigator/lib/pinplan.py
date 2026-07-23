"""Generic, complete corpus closure planning for current-only inputs."""

from . import canon


PLAN_VERSION = "3"


class PinPlanError(ValueError):
    pass


def _version_map(value, label):
    if not isinstance(value, dict) or not value or not all(
            isinstance(strategy, str) and strategy and strategy.isascii() and
            strategy == strategy.upper() and
            isinstance(version, str) and version
            for strategy, version in value.items()):
        raise PinPlanError("%s is not a structured version map" % label)
    return {strategy: value[strategy] for strategy in sorted(value)}


def corpus_closure(corpus_id, entry, content, expected_versions=None):
    """Return complete file and version currency for one corpus.

    ``content`` supplies ``read_bytes(path)``.  Every pinned file is read; the
    primary designation never narrows integrity currency.
    """
    if not isinstance(entry, dict):
        raise PinPlanError("corpus %r entry is not an object" % corpus_id)
    pins = entry.get("files")
    primary = entry.get("primary")
    if not isinstance(pins, dict) or not pins or primary not in pins:
        raise PinPlanError("corpus %r has no complete file closure" % corpus_id)
    files = []
    for path in sorted(pins):
        actual = canon.bytes_digest(content.read_bytes(path))
        files.append({
            "path": path,
            "primary": path == primary,
            "pinnedDigest": pins[path],
            "actualDigest": actual,
            "pinCurrent": pins[path] == actual,
        })
    result = {
        "corpusId": corpus_id,
        "role": entry.get("role"),
        "primary": primary,
        "files": files,
        "pinCurrent": all(item["pinCurrent"] for item in files),
    }
    if expected_versions is None:
        configured = entry.get("version")
        result.update({
            "configuredVersion": configured,
            "expectedVersion": configured,
            "versionCurrent": isinstance(configured, str) and bool(configured),
        })
    else:
        configured = _version_map(
            entry.get("versionBindings"),
            "corpus %r versionBindings" % corpus_id)
        expected = _version_map(
            expected_versions, "corpus %r expected versions" % corpus_id)
        result.update({
            "configuredVersions": configured,
            "expectedVersions": expected,
            "versionCurrent": configured == expected,
        })
    return result


def closure_problems(plan, label):
    if not isinstance(plan, dict):
        return ["%s corpus plan is not an object" % label]
    problems = []
    files = plan.get("files")
    if not isinstance(files, list) or not files:
        problems.append("%s corpus plan has no files" % label)
    else:
        paths = []
        primary_count = 0
        for item in files:
            if not isinstance(item, dict) or set(item) != {
                    "path", "primary", "pinnedDigest", "actualDigest",
                    "pinCurrent"}:
                problems.append("%s corpus plan has malformed file data" % label)
                continue
            paths.append(item["path"])
            primary_count += item["primary"] is True
            if item["pinCurrent"] is not True:
                problems.append(
                    "%s file digest pin is stale: %s" % (label, item["path"]))
        if paths != sorted(paths) or len(paths) != len(set(paths)):
            problems.append("%s corpus plan file inventory is not exact" % label)
        if primary_count != 1:
            problems.append("%s corpus plan does not identify one primary" % label)
    if plan.get("pinCurrent") is not True:
        problems.append("%s aggregate corpus digest pin is stale" % label)
    if plan.get("versionCurrent") is not True:
        problems.append("%s corpus version binding is stale" % label)
    return problems
