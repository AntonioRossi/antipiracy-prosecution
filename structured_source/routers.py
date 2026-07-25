"""Deterministic registry-only Markdown routers."""

from __future__ import annotations

import posixpath

from .errors import StructuredSourceError
from .registry import validate_registry, files_by_id


def _relative(path, router_path):
    return posixpath.relpath(path, posixpath.dirname(router_path) or ".")


def render_router(registry, router_id):
    validate_registry(registry)
    matches = [item for item in registry["routers"]
               if item["routerId"] == router_id]
    if len(matches) != 1:
        raise StructuredSourceError("router identity does not resolve exactly")
    router = matches[0]
    files = files_by_id(registry)
    packages = {
        item["documentId"]: ("content", item)
        for item in registry["documents"]}
    packages.update({
        item["relationSetId"]: ("relations", item)
        for item in registry["relationSets"]})
    lines = [
        "<!-- GENERATED ROUTER — materialized from the closed structured-source registry; edit the registry, never this Markdown. -->",
        "",
        "# %s structured-source packages" % router["scope"], "",
        "| Stable ID | Primary type | Scope | Status | Canonical XML | Review view | Coverage |",
        "|---|---|---|---|---|---|---|",
    ]
    for package_id in router["packages"]:
        kind, package = packages[package_id]
        source = files[package["sourceFile"]]["path"]
        markdown = files[package["markdownFile"]]["path"]
        coverage = files[package["coverageFile"]]["path"]
        lines.append("| %s | %s | %s | %s | [%s](%s) | [Markdown](%s) | [Coverage](%s) |" % (
            package_id, kind, package["scope"], package["status"],
            posixpath.basename(source), _relative(source, router["path"]),
            _relative(markdown, router["path"]),
            _relative(coverage, router["path"])))
    return ("\n".join(lines) + "\n").encode("utf-8")


def render_all(registry):
    return {item["path"]: render_router(registry, item["routerId"])
            for item in registry["routers"]}

