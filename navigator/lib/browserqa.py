"""Pinned executable-browser control for navigator interaction acceptance."""

from __future__ import annotations

from contextlib import contextmanager
from importlib import metadata
import os

from . import canon


BROWSER_CONTROL_PATH = "navigator/policy/browser.json"


class BrowserControlError(RuntimeError):
    """The exact browser control or its managed runtime is unavailable."""


def load_browser_control(root, byte_source=None):
    """Load the sole current browser, layout, and viewport matrix control."""
    absolute = os.path.join(root, *BROWSER_CONTROL_PATH.split("/"))
    try:
        if byte_source is None:
            with open(absolute, "rb") as handle:
                data = handle.read()
        else:
            data = byte_source(absolute)
        value = canon.parse_json(data)
    except (OSError, KeyError, ValueError, canon.CanonError) as exc:
        raise BrowserControlError("browser control is unreadable") from exc
    if data != canon.canonical_json(value) + b"\n" or \
            not isinstance(value, dict) or set(value) != {
                "automation", "browser", "browserControlVersion", "layout",
                "presentation", "viewports"} or \
            value.get("browserControlVersion") != "2":
        raise BrowserControlError("browser control shape/version is not current")
    automation = value["automation"]
    browser = value["browser"]
    layout = value["layout"]
    presentation = value["presentation"]
    viewports = value["viewports"]
    if automation != {"distribution": "playwright", "version": "1.50.0"} or \
            browser != {
                "name": "chromium", "revision": "1155",
                "version": "133.0.6943.16"} or \
            not isinstance(layout, dict) or set(layout) != {
                "clearancePixels", "minimumViewport", "sideBySide"} or \
            layout["clearancePixels"] != 10 or \
            layout["minimumViewport"] != {"height": 700, "width": 1000} or \
            layout["sideBySide"] != {
                "minimumHeight": 720, "minimumWidth": 1280} or \
            presentation != {
                "maximumMeasureCh": 80,
                "maximumChromeViewportPercent": 45,
                "pageZoomFactor": 2,
                "reflowViewport": {"height": 256, "width": 320},
                "textResizeFactor": 2,
                "textSpacing": {
                    "letterSpacingThousandths": 120,
                    "lineHeightThousandths": 1500,
                    "paragraphSpacingThousandths": 2000,
                    "wordSpacingThousandths": 160,
                },
                "typography": {
                    "auxiliary": {
                        "lineHeightThousandths": 1350,
                        "minimumRemThousandths": 750,
                    },
                    "interface": {
                        "lineHeightThousandths": 1350,
                        "minimumRemThousandths": 875,
                    },
                    "reading": {
                        "lineHeightThousandths": 1500,
                        "minimumRemThousandths": 1125,
                    },
                },
            } or \
            viewports != [
                {"height": 720, "mode": "side-by-side", "width": 1280},
                {"height": 720, "mode": "stacked", "width": 1279},
                {"height": 719, "mode": "stacked", "width": 1280},
                {"height": 700, "mode": "stacked", "width": 1000},
            ]:
        raise BrowserControlError("browser control values are not exact")
    return value


@contextmanager
def browser_runtime(root, byte_source=None):
    """Yield only the exact Playwright-managed Chromium runtime; never fall back."""
    control = load_browser_control(root, byte_source)
    expected_automation = control["automation"]["version"]
    try:
        actual_automation = metadata.version("playwright")
    except metadata.PackageNotFoundError as exc:
        raise BrowserControlError("pinned Playwright distribution is absent") from exc
    if actual_automation != expected_automation:
        raise BrowserControlError("Playwright distribution version is stale")
    try:
        from playwright.sync_api import sync_playwright
        manager = sync_playwright().start()
    except Exception as exc:
        raise BrowserControlError("pinned Playwright runtime cannot start") from exc
    browser = None
    try:
        browser_type = getattr(manager, control["browser"]["name"], None)
        executable = (browser_type.executable_path
                      if browser_type is not None else "")
        normalized = executable.replace("\\", "/")
        marker = "/chromium-%s/" % control["browser"]["revision"]
        if not executable or marker not in normalized or \
                not os.path.isfile(executable) or os.path.islink(executable):
            raise BrowserControlError(
                "pinned Playwright-managed browser revision is absent")
        browser = browser_type.launch(headless=True)
        if browser.version != control["browser"]["version"]:
            raise BrowserControlError("Chromium runtime version is stale")
        yield control, browser
    except BrowserControlError:
        raise
    except Exception as exc:
        raise BrowserControlError("pinned Chromium runtime failed") from exc
    finally:
        if browser is not None:
            browser.close()
        manager.stop()


def runtime_matrix(control):
    """Return the exact product-independent viewport and motion vector census."""
    if not isinstance(control, dict):
        raise BrowserControlError("browser matrix requires a validated control")
    return tuple(
        (item["width"], item["height"], item["mode"], reduced)
        for item in control["viewports"]
        for reduced in (False, True)
    )


def zoom_matrix(control):
    """Return exact page-zoom-equivalent layout viewports and motion vectors."""
    if not isinstance(control, dict):
        raise BrowserControlError("browser zoom matrix requires a validated control")
    factor = control["presentation"]["pageZoomFactor"]
    return tuple(
        (
            (item["width"] + factor - 1) // factor,
            (item["height"] + factor - 1) // factor,
            item["width"], item["height"], reduced,
        )
        for item in control["viewports"]
        for reduced in (False, True)
    )


def reflow_matrix(control):
    """Return the exact narrow reflow viewport under both motion preferences."""
    if not isinstance(control, dict):
        raise BrowserControlError("browser reflow matrix requires a validated control")
    viewport = control["presentation"]["reflowViewport"]
    return tuple(
        (viewport["width"], viewport["height"], reduced)
        for reduced in (False, True)
    )
