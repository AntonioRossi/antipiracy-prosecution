"""Exact host capability and project-local environment verification."""

from __future__ import annotations

import importlib.metadata
import importlib.util
import json
import os
import site
import subprocess
import sys
import tempfile

from .errors import EnvironmentError

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POLICY_RELATIVE_PATH = "structured_source/policy/environment.json"

_POLICY_FIELDS = {
    "environmentVersion", "uvVersion", "pythonVersion", "projectPath",
    "lockPath", "pythonVersionPath", "environmentPath", "distributions",
    "pandocVersion", "pandocApiVersion",
}


def _read_bytes(root: str, relative: str, byte_source=None) -> bytes:
    absolute = _canonical_path(relative, "environment input", root)
    try:
        if byte_source is not None:
            data = byte_source(absolute)
        else:
            if not os.path.isfile(absolute) or os.path.islink(absolute):
                raise OSError("input is absent or non-regular")
            with open(absolute, "rb") as handle:
                data = handle.read()
    except (OSError, KeyError) as exc:
        raise EnvironmentError(
            "declared environment input is unreadable: %s" % relative) from exc
    if not isinstance(data, bytes):
        raise EnvironmentError("environment byte source returned non-bytes")
    return data


def _load_policy(root=ROOT, byte_source=None) -> dict:
    try:
        value = json.loads(
            _read_bytes(root, POLICY_RELATIVE_PATH, byte_source).decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EnvironmentError("environment policy is unreadable: %s" % exc) from exc
    if not isinstance(value, dict) or set(value) != _POLICY_FIELDS or \
            value.get("environmentVersion") != "1":
        raise EnvironmentError("environment policy shape/version is not current")
    return value


def _canonical_path(path: str, label: str, root=ROOT) -> str:
    root = os.path.abspath(root)
    if not isinstance(path, str) or not path or os.path.isabs(path) or \
            "\\" in path or any(part in {"", ".", ".."} for part in path.split("/")):
        raise EnvironmentError("%s is not a canonical repository path" % label)
    absolute = os.path.abspath(os.path.join(root, *path.split("/")))
    if os.path.commonpath((root, absolute)) != root:
        raise EnvironmentError("%s escapes the repository" % label)
    return absolute


def verify_environment(root=ROOT, byte_source=None) -> dict:
    """Fail closed unless verification runs in the exact locked environment."""
    root = os.path.abspath(root)
    policy = _load_policy(root, byte_source)
    expected_python = policy["pythonVersion"]
    actual_python = ".".join(str(part) for part in sys.version_info[:3])
    if actual_python != expected_python:
        raise EnvironmentError(
            "Python version mismatch: expected %s, got %s" %
            (expected_python, actual_python))
    expected_environment = _canonical_path(
        policy["environmentPath"], "environment path", root)
    if os.path.realpath(sys.prefix) != os.path.realpath(expected_environment) or \
            sys.base_prefix == sys.prefix:
        raise EnvironmentError("structured-source command is outside the project environment")
    if os.environ.get("PYTHONPATH"):
        raise EnvironmentError("ambient PYTHONPATH is prohibited")
    if site.ENABLE_USER_SITE is not False:
        raise EnvironmentError("user-site packages are not disabled")

    declared = {
        field: _read_bytes(root, policy[field], byte_source)
        for field in ("projectPath", "lockPath", "pythonVersionPath")
    }
    try:
        declared_python = declared["pythonVersionPath"].decode("utf-8").strip()
    except UnicodeDecodeError as exc:
        raise EnvironmentError(".python-version is not UTF-8") from exc
    if declared_python != expected_python:
        raise EnvironmentError(".python-version does not match the environment policy")

    try:
        result = subprocess.run(
            ["uv", "--version"], cwd=root, capture_output=True, text=True,
            timeout=15, env={**os.environ, "UV_NO_CACHE": "1"})
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise EnvironmentError("host uv capability is unavailable: %s" % exc) from exc
    expected_uv = "uv %s " % policy["uvVersion"]
    if result.returncode or not result.stdout.startswith(expected_uv):
        raise EnvironmentError("host uv version does not match the environment policy")

    try:
        pandoc = subprocess.run(
            ["pandoc", "--version"], cwd=root, capture_output=True, text=True,
            timeout=15)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise EnvironmentError("host Pandoc capability is unavailable: %s" % exc) from exc
    if pandoc.returncode or not pandoc.stdout.startswith(
            "pandoc %s\n" % policy["pandocVersion"]):
        raise EnvironmentError("host Pandoc version does not match the environment policy")
    probe = subprocess.run(
        ["pandoc", "--from=gfm", "--to=json"], input="probe\n",
        cwd=root, capture_output=True, text=True, timeout=15)
    try:
        api_version = json.loads(probe.stdout).get("pandoc-api-version")
    except (AttributeError, json.JSONDecodeError) as exc:
        raise EnvironmentError("host Pandoc AST probe is malformed") from exc
    if probe.returncode or api_version != policy["pandocApiVersion"]:
        raise EnvironmentError("host Pandoc AST version does not match policy")

    distributions = policy["distributions"]
    if not isinstance(distributions, list) or not distributions:
        raise EnvironmentError("environment distribution census is empty")
    census = []
    seen = set()
    site_root = os.path.realpath(os.path.join(
        expected_environment, "lib", "python%s.%s" % sys.version_info[:2],
        "site-packages"))
    for entry in distributions:
        if not isinstance(entry, dict) or set(entry) != {"name", "version"} or \
                not all(isinstance(entry.get(key), str) and entry[key]
                        for key in ("name", "version")):
            raise EnvironmentError("environment distribution entry is malformed")
        name = entry["name"].lower().replace("_", "-")
        if name in seen:
            raise EnvironmentError("environment distribution names are not unique")
        seen.add(name)
        try:
            installed = importlib.metadata.distribution(entry["name"])
        except importlib.metadata.PackageNotFoundError as exc:
            raise EnvironmentError("locked distribution is not installed: %s" % name) from exc
        if installed.version != entry["version"]:
            raise EnvironmentError("installed distribution version is stale: %s" % name)
        location = os.path.realpath(str(installed.locate_file("")))
        if os.path.commonpath((site_root, location)) != site_root:
            raise EnvironmentError("distribution resolved outside the project environment: %s" % name)
        spec = importlib.util.find_spec(entry["name"].replace("-", "_"))
        if spec is None or spec.origin is None or \
                os.path.commonpath((site_root, os.path.realpath(spec.origin))) != site_root:
            raise EnvironmentError("distribution import origin is not project-local: %s" % name)
        census.append({"name": name, "version": installed.version,
                       "origin": os.path.relpath(spec.origin, root).replace(os.sep, "/")})
    if [entry["name"] for entry in census] != sorted(seen):
        raise EnvironmentError("environment distributions are not canonically ordered")
    installed_names = set()
    for installed in importlib.metadata.distributions():
        location = os.path.realpath(str(installed.locate_file("")))
        if os.path.commonpath((site_root, location)) == site_root:
            name = installed.metadata.get("Name")
            if not name:
                raise EnvironmentError("installed distribution has no canonical name")
            installed_names.add(name.lower().replace("_", "-"))
    if installed_names != seen:
        raise EnvironmentError(
            "project environment distribution inventory is not exact")
    lock_root = root
    temporary = None
    if byte_source is not None:
        temporary = tempfile.TemporaryDirectory(prefix="aa11393-lock-check-")
        lock_root = temporary.name
        for field in ("projectPath", "lockPath", "pythonVersionPath"):
            relative = policy[field]
            destination = os.path.join(lock_root, *relative.split("/"))
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            with open(destination, "wb") as handle:
                handle.write(declared[field])
    try:
        lock_check = subprocess.run(
            ["uv", "--no-cache", "--offline", "lock", "--check"],
            cwd=lock_root, capture_output=True, text=True, timeout=60,
            env={**os.environ, "UV_NO_CACHE": "1", "UV_OFFLINE": "1"})
    finally:
        if temporary is not None:
            temporary.cleanup()
    if lock_check.returncode:
        raise EnvironmentError("repository project and lock are inconsistent")
    return {
        "environmentVersion": policy["environmentVersion"],
        "uvVersion": policy["uvVersion"],
        "pandocVersion": policy["pandocVersion"],
        "pandocApiVersion": policy["pandocApiVersion"],
        "pythonVersion": actual_python,
        "interpreter": os.path.relpath(sys.executable, root).replace(os.sep, "/"),
        "distributions": census,
    }
