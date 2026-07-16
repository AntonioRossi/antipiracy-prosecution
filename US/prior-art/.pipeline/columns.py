#!/usr/bin/env python3
"""Column-aware text extraction for two-column patent PDFs.

US patent PDFs place the two text columns in the same PDF text blocks, so
neither `pdftotext -layout` nor PyMuPDF sort=True reads them in order: output
alternates between columns line by line. This module works at the LINE level,
assigns each line to a column by x-midpoint, and splits the occasional line
whose spans straddle the gutter (usually because of the line-number column).
"""
import re
import fitz

# A span belongs to the right column if its own midpoint is right of the gutter.
def page_columns(page, gutter_ratio=0.5):
    mid = page.rect.width * gutter_ratio
    left, right = [], []
    for b in page.get_text("dict")["blocks"]:
        if b.get("type") != 0:
            continue
        for l in b.get("lines", []):
            spans = [s for s in l["spans"] if s["text"].strip()]
            if not spans:
                continue
            lo = [s for s in spans if (s["bbox"][0] + s["bbox"][2]) / 2 < mid]
            ro = [s for s in spans if (s["bbox"][0] + s["bbox"][2]) / 2 >= mid]
            if lo:
                left.append((lo[0]["bbox"][1], "".join(s["text"] for s in lo).strip()))
            if ro:
                right.append((ro[0]["bbox"][1], "".join(s["text"] for s in ro).strip()))
    order = lambda col: [t for _, t in sorted(col, key=lambda p: p[0]) if t]
    return order(left), order(right)

def is_two_column(page, gutter_ratio=0.5, min_lines=8):
    l, r = page_columns(page, gutter_ratio)
    return len(l) >= min_lines and len(r) >= min_lines

def dehyphenate(lines):
    out = []
    for t in lines:
        if out and re.search(r"[a-z]-$", out[-1]):
            out[-1] = out[-1][:-1] + t.lstrip()
        else:
            out.append(t)
    return out

def strip_line_numbers(lines):
    # patent text columns carry 5/10/15... line numbers; drop bare-number lines
    return [t for t in lines if not re.fullmatch(r"\d{1,2}", t.strip())]

def page_text(page):
    if not is_two_column(page):
        return page.get_text("text", sort=True).strip()
    l, r = page_columns(page)
    l = dehyphenate(strip_line_numbers(l))
    r = dehyphenate(strip_line_numbers(r))
    return "\n".join(l + r).strip()

def doc_text(path):
    d = fitz.open(path)
    pages = []
    for i, p in enumerate(d, 1):
        t = page_text(p)
        pages.append(f"### Page {i}\n\n{t}" if t else f"### Page {i}\n\n*(No extractable text — drawing sheet or image; consult the PDF.)*")
    return "\n\n---\n\n".join(pages)

if __name__ == "__main__":
    import sys
    print(doc_text(sys.argv[1])[:3000])
