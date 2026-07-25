"""Deterministic registry-only Markdown routers."""

from __future__ import annotations

import posixpath

from .errors import StructuredSourceError
from .registry import files_by_id, packages_by_id, validate_registry


def _relative(path, router_path):
    return posixpath.relpath(path, posixpath.dirname(router_path) or ".")


def render_router(registry, router_id):
    validate_registry(registry)
    matches = [entry for entry in registry["routers"]
               if entry["routerId"] == router_id]
    if len(matches) != 1:
        raise StructuredSourceError("router identity does not resolve exactly")
    router = matches[0]
    files = files_by_id(registry)
    packages = packages_by_id(registry)
    lines = [
        "<!-- GENERATED ROUTER — edit the content registry, never this Markdown. -->",
        "",
        "# %s structured-source packages" % router["scope"],
        "",
        "| Stable ID | Authority scheme | XML interface | Markdown representation |",
        "|---|---|---|---|",
    ]
    for package_id in router["packages"]:
        package = packages[package_id]
        xml_entry = files[package["xmlFile"]]
        markdown_entry = files[package["markdownFile"]]
        lines.append(
            "| %s | `%s` | [%s](%s) · %s | [Markdown](%s) · %s |" % (
                package_id,
                package["authorityScheme"],
                posixpath.basename(xml_entry["path"]),
                _relative(xml_entry["path"], router["path"]),
                xml_entry["role"],
                _relative(markdown_entry["path"], router["path"]),
                markdown_entry["role"],
            ))
    return ("\n".join(lines) + "\n").encode("utf-8")


def render_all(registry):
    return {entry["path"]: render_router(registry, entry["routerId"])
            for entry in registry["routers"]}
