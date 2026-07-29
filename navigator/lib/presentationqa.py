"""Executable, non-persistent presentation checks for current navigators."""

from __future__ import annotations

from types import MappingProxyType
import re


class PresentationQAError(RuntimeError):
    """The rendered product violates the closed presentation contract."""


TYPOGRAPHY_SELECTORS = MappingProxyType({
    "reading": (
        ".unit-body", ".dblock:not(.table-wrap)", ".reader-content",
        ".reader-block", "#about p", "#about li",
        ".guide-body", "#guide-overlay-title",
    ),
    "interface": (
        "#masthead h1", ".legend", ".chip", ".claim-group h2", ".claim-header",
        ".gate-chip",
        ".state-note", ".obligation-list", ".allocation-detail",
        ".reader-jump", ".full-reader > summary", ".reader-authority",
        ".reverse-badge", ".editorial-tag", "table", "figcaption",
        ".highlight-key", ".navigation-bar", ".caution-chip",
        ".caution-detail", ".disposition", "#aux-toggle",
        ".passage-meta", "#guide-open", ".guide > summary", ".guide-close",
        ".guide-glyph",
    ),
    "auxiliary": (
        ".chip-group-name", ".unit-label", ".anchor-label",
    ),
})

_ABSOLUTE_FONT = re.compile(
    r"(?:font-size|font)\s*:[^;}]*\b\d+(?:\.\d+)?px\b",
    flags=re.IGNORECASE,
)
_VIEWPORT_FONT = re.compile(
    r"(?:font-size|font)\s*:[^;}]*\b\d+(?:\.\d+)?v(?:w|h|min|max)\b",
    flags=re.IGNORECASE,
)
_FONT_SHORTHAND = re.compile(r"(?:^|[;{])\s*font\s*:", flags=re.IGNORECASE)


def _presentation(control):
    if not isinstance(control, dict) or not isinstance(
            control.get("presentation"), dict):
        raise PresentationQAError("presentation control is absent")
    return control["presentation"]


def validate_computed_typography(page, control):
    """Require exact relative-unit typography tiers in one rendered page."""
    policy = _presentation(control)
    css = page.locator("head > style").first.text_content()
    if not isinstance(css, str) or _ABSOLUTE_FONT.search(css) or \
            _VIEWPORT_FONT.search(css) or _FONT_SHORTHAND.search(css):
        raise PresentationQAError(
            "rendered CSS contains a forbidden font unit or shorthand")
    if "font-size:smaller" in css.replace(" ", "").casefold():
        raise PresentationQAError("rendered CSS contains relative font reduction")
    root_size = page.evaluate(
        "() => parseFloat(getComputedStyle(document.documentElement).fontSize)")
    if not isinstance(root_size, (int, float)) or root_size <= 0:
        raise PresentationQAError("browser root font size is not measurable")
    results = {}
    for tier, selectors in TYPOGRAPHY_SELECTORS.items():
        expected = policy["typography"][tier]
        values = page.evaluate("""selectors => {
          const nodes = Array.from(document.querySelectorAll(
            selectors.join(',')));
          return nodes.map(node => {
            const style = getComputedStyle(node);
            const size = parseFloat(style.fontSize);
            const height = parseFloat(style.lineHeight);
            return {
              selector:node.matches(selectors.join(',')),
              size:size,
              ratio:Number.isFinite(height) && size > 0 ? height / size : null,
              tag:node.tagName,
              className:node.className || '',
              id:node.id || ''
            };
          });
        }""", list(selectors))
        if not values:
            raise PresentationQAError(
                "rendered product has no %s typography role" % tier)
        minimum_size = (
            root_size * expected["minimumRemThousandths"] / 1000)
        minimum_line_height = expected["lineHeightThousandths"] / 1000
        defects = [
            value for value in values
            if value["size"] + 0.01 < minimum_size or
            value["ratio"] is None or
            value["ratio"] + 0.01 < minimum_line_height
        ]
        if defects:
            raise PresentationQAError(
                "%s typography tier is undersized: %s" %
                (tier, defects[:5]))
        results[tier] = {
            "count": len(values),
            "minimumLineHeight": minimum_line_height,
            "minimumPixels": minimum_size,
        }
    return MappingProxyType(results)


def validate_reading_surfaces(page, control):
    """Require bounded ordinary measure and only scoped horizontal overflow."""
    policy = _presentation(control)
    expected_measure = policy["maximumMeasureCh"]
    result = page.evaluate("""maximum => {
      const ordinarySelector = [
        '.reading-measure:not(.scoped-overflow)', '.legend',
        '#masthead h1', '#masthead .meta', '.state-note',
        '.allocation-detail', '.caution-detail', '.passage-meta',
        '.reader-authority', '.highlight-key', '.prior-art-document > h2'
      ].join(',');
      const values = Array.from(document.querySelectorAll(ordinarySelector))
        .filter(node => node.getClientRects().length)
        .map(node => {
          const probe = document.createElement('span');
          probe.textContent = '0';
          probe.style.cssText =
            'position:absolute;visibility:hidden;inline-size:1ch;padding:0;border:0';
          node.appendChild(probe);
          const ch = probe.getBoundingClientRect().width;
          probe.remove();
          const box = node.getBoundingClientRect();
          return {
            id:node.id || '', className:node.className || '',
            measure:ch > 0 ? box.width / ch : null,
            overflow:node.scrollWidth > node.clientWidth + 1
          };
        });
      const scoped = Array.from(document.querySelectorAll(
        '.table-wrap,pre.scoped-overflow')).map(node => ({
          overflowX:getComputedStyle(node).overflowX,
          pageContained:node.getBoundingClientRect().right <=
            document.documentElement.clientWidth + 1
        }));
      const accidental = Array.from(document.querySelectorAll('body *'))
        .filter(node => node.getClientRects().length &&
          node.scrollWidth > node.clientWidth + 1 &&
          !node.closest('.scoped-overflow') &&
          !node.matches('.visually-hidden'))
        .slice(0, 12).map(node => ({
          tag:node.tagName, id:node.id || '', className:node.className || '',
          clientWidth:node.clientWidth, scrollWidth:node.scrollWidth
        }));
      return {
        values:values,
        defects:values.filter(item => item.measure === null ||
          item.measure > maximum + 1 || item.overflow),
        pageOverflow:document.documentElement.scrollWidth >
          document.documentElement.clientWidth + 1,
        scoped:scoped, accidental:accidental
      };
    }""", expected_measure)
    if not result["values"] or result["defects"] or result["pageOverflow"] or \
            result["accidental"] or \
            any(item["overflowX"] not in {"auto", "scroll"} or
                not item["pageContained"] for item in result["scoped"]):
        diagnostic = {
            "count": len(result["values"]),
            "defects": result["defects"][:12],
            "pageOverflow": result["pageOverflow"],
            "scopedDefects": [
                item for item in result["scoped"]
                if item["overflowX"] not in {"auto", "scroll"} or
                not item["pageContained"]
            ][:12],
            "accidental": result["accidental"],
        }
        raise PresentationQAError(
            "reading measure or overflow contract failed: %s" % diagnostic)
    return MappingProxyType({
        "count": len(result["values"]),
        "maximumMeasureCh": expected_measure,
        "scopedOverflowCount": len(result["scoped"]),
    })


def validate_text_spacing_adaptation(page, control):
    """Apply the exact ephemeral text-spacing vector to one rendered page."""
    spacing = _presentation(control)["textSpacing"]
    values = {
        "letterSpacingEm": spacing["letterSpacingThousandths"] / 1000,
        "lineHeight": spacing["lineHeightThousandths"] / 1000,
        "paragraphSpacingEm": spacing["paragraphSpacingThousandths"] / 1000,
        "wordSpacingEm": spacing["wordSpacingThousandths"] / 1000,
    }
    page.evaluate("""spacing => {
      const prior = document.getElementById('presentation-spacing-vector');
      if (prior) prior.remove();
      const style = document.createElement('style');
      style.id = 'presentation-spacing-vector';
      style.textContent =
        'body *{line-height:' + spacing.lineHeight + ' !important;' +
        'letter-spacing:' + spacing.letterSpacingEm + 'em !important;' +
        'word-spacing:' + spacing.wordSpacingEm + 'em !important}' +
        'p{margin-block-end:' + spacing.paragraphSpacingEm + 'em !important}';
      document.head.appendChild(style);
    }""", values)
    applied = page.evaluate("""spacing => {
      const node = document.querySelector('.unit-body');
      const paragraph = document.querySelector('p');
      const style = getComputedStyle(node);
      const paragraphStyle = getComputedStyle(paragraph);
      const size = parseFloat(style.fontSize);
      return {
        lineHeight:parseFloat(style.lineHeight) / size,
        letterSpacing:parseFloat(style.letterSpacing) / size,
        wordSpacing:parseFloat(style.wordSpacing) / size,
        paragraphSpacing:parseFloat(paragraphStyle.marginBlockEnd) /
          parseFloat(paragraphStyle.fontSize)
      };
    }""", values)
    for key, expected in (
            ("lineHeight", values["lineHeight"]),
            ("letterSpacing", values["letterSpacingEm"]),
            ("wordSpacing", values["wordSpacingEm"]),
            ("paragraphSpacing", values["paragraphSpacingEm"])):
        if abs(applied[key] - expected) > 0.02:
            raise PresentationQAError(
                "text-spacing vector did not apply exactly: %s" % applied)
    return MappingProxyType(applied)


def validate_noninteractive_surfaces(page, control):
    """Apply the same typography and measure checks to no-script or print."""
    typography = validate_computed_typography(page, control)
    reading = validate_reading_surfaces(page, control)
    return MappingProxyType({"reading": reading, "typography": typography})
