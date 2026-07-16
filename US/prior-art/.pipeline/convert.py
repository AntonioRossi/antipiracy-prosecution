#!/usr/bin/env python3
"""Convert stored prior-art PDFs to review-grade markdown.

Native-text PDFs -> pdftotext -layout.
Image-only PDFs  -> pdftoppm (300dpi gray) | tesseract --psm 1 (auto layout,
                    handles two-column patent text).
Never modifies the source PDFs.
"""
import re, subprocess, sys, unicodedata
from pathlib import Path
import columns

SRC = Path("/Users/antonio/development/antipiracy-prosecution/US/prior-art")
OUT = SRC / "markdown"
TMP = Path("/private/tmp/claude-501/-Users-antonio-development-antipiracy-prosecution/25f559b8-1569-445e-b6ae-8edcf80e0ebf/scratchpad/pages")

# id -> (pdf stem, method, lang, human title)
DOCS = {
    "A1": ("A1_US2021-0352381A1_D1_from-ISR", "ocr", "eng", "US 2021/0352381 A1 — Methods and Systems for Reducing Piracy of Media Content"),
    "A2": ("A2_US7630497B2", "text", None, "US 7,630,497 B2 — System and Method for Assigning Sequence Keys to a Media Player to Enable Hybrid Traitor Tracing"),
    "A3": ("A3_US20090320130A1", "text", None, "US 2009/0320130 A1 — Traitor Detection for Multilevel Assignment"),
    "A4": ("A4_US10834158B1", "text", None, "US 10,834,158 B1 — Encoding Identifiers into Customized Manifest Data"),
    "A5": ("A5_US20120087583A1", "text", None, "US 2012/0087583 A1 — Video Signature Based on Image Hashing and Shot Detection"),
    "A6": ("A6_US20140325550A1", "text", None, "US 2014/0325550 A1 — Real-Time Anti-Piracy for Broadcast Streams"),
    "A7": ("A7_US20170118537A1", "text", None, "US 2017/0118537 A1 — Adaptive Watermarking for Streaming Data"),
    "A8": ("A8_US20180352307A1", "text", None, "US 2018/0352307 A1 — Content Segment Variant Obfuscation"),
    "A9": ("A9_US12412229B2", "ocr", "eng", "US 12,412,229 B2 — Anti-Collusion System Using Multiple Watermark Images"),
    "A10": ("A10_US20100100971A1", "text", None, "US 2010/0100971 A1 — System for Embedding Data"),
    "B1": ("B1_CN117278762A_D2_from-ISR", "text", None, "CN 117278762 A — Secure and Traceable Video Encoding/Decoding System"),
    "B2": ("B2_WO2021224688A1", "ocr", "eng", "WO 2021/224688 A1 — Methods and Systems for Reducing Piracy of Media Content (PCT family of A1)"),
    "B3": ("B3_WO2017017603A1", "ocr", "eng", "WO 2017/017603 A1 — System to Detect Unauthorized Distribution of Media Content"),
    "B4": ("B4_WO2010044102A2", "ocr", "eng", "WO 2010/044102 A2 — Visibly Non-Intrusive Digital Watermark Based System for Forensic Detection of the Point of Piracy"),
    "B5": ("B5_CN202455480U", "ocr", "chi_sim+eng", "CN 202455480 U — Digital Watermark System for Verifying Digital Television Copyright"),
    "B6": ("B6_CN100583750C", "ocr", "chi_sim+eng", "CN 100583750 C — Desynchronized Fingerprinting Method and System for Digital Multimedia Data"),
    "B7": ("B7_WO2021141686A1", "ocr", "eng", "WO 2021/141686 A1 — Method of Identifying an Abridged Version of a Video"),
    "B8": ("B8_EP2811416A1", "text", None, "EP 2 811 416 A1 — An Identification Method"),
    "B9": ("B9_WO2009156973A1", "ocr", "eng", "WO 2009/156973 A1 — Fingerprinting Method and System"),
    "C8": ("C8_ETSI-TS-104-002_DASH-IF-AB-Watermarking", "text", None, "ETSI TS 104 002 V1.1.1 (2023-08) — DASH-IF Forensic A/B Watermarking"),
}

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def page_count(pdf):
    out = run(["pdfinfo", str(pdf)]).stdout
    m = re.search(r"^Pages:\s+(\d+)", out, re.M)
    return int(m.group(1)) if m else 0

def looks_like_figure(txt):
    """Classify drawing sheets so they are never presented as readable prose.

    Signals, strongest first:
      1. the USPTO/WIPO drawing-sheet stamp ("Sheet 7 of 10", "FIG. 3");
      2. very little text at all;
      3. low ratio of alphabetic characters (callout numbers, leader lines);
      4. no sentence-like structure (figures are label fragments, not prose).
    A false negative is worse than a false positive here: an unmarked figure
    page reads as if it were prose, so the thresholds are deliberately eager.
    """
    stripped = re.sub(r"\s", "", txt)
    if not stripped:
        return True

    # CJK is far more information-dense than Latin: a full page of Chinese
    # claims is ~300 chars, so length/prose thresholds must be script-aware.
    cjk = len(re.findall(r"[㐀-鿿]", stripped))
    is_cjk = cjk / len(stripped) > 0.25

    if re.search(r"Sheet\s+\d+\s+of\s+\d+", txt, re.I):
        return True
    if len(stripped) < (120 if is_cjk else 400):
        return True

    letters = sum(c.isalpha() for c in stripped)  # True for CJK too
    if letters / len(stripped) < 0.62:
        return True

    if is_cjk:
        # Chinese prose: sentence-ending punctuation and claim/section markers.
        markers = len(re.findall(r"[。；，]", txt)) + len(re.findall(r"权利要求|说明书|附图|所述", txt))
        return markers < 3
    sentences = len(re.findall(r"[a-z]{3,}[,;]?\s+[a-z]{3,}[^.]{20,}\.", txt))
    return sentences < 2

def clean(txt):
    txt = txt.replace("\x0c", "\n")
    txt = unicodedata.normalize("NFC", txt)
    txt = re.sub(r"[ \t]+\n", "\n", txt)
    txt = re.sub(r"\n{3,}", "\n\n", txt)
    return txt.strip()

def extract_text(pdf):
    """Column-aware extraction (see columns.py): two-column patent pages are
    split at the gutter and each column emitted in reading order."""
    return clean(columns.doc_text(str(pdf))), []

def extract_ocr(pdf, lang, stem):
    TMP.mkdir(parents=True, exist_ok=True)
    for old in TMP.glob(f"{stem}*"):
        old.unlink()
    n = page_count(pdf)
    run(["pdftoppm", "-r", "300", "-gray", "-png", str(pdf), str(TMP / stem)])
    pages, figures = [], []
    for img in sorted(TMP.glob(f"{stem}-*.png")):
        pno = int(re.search(r"-(\d+)\.png$", img.name).group(1))
        base = str(img)[:-4]
        run(["tesseract", str(img), base, "-l", lang, "--psm", "1"])
        t = Path(base + ".txt")
        raw = clean(t.read_text(encoding="utf-8", errors="replace")) if t.exists() else ""
        if looks_like_figure(raw):
            figures.append(pno)
            pages.append(f"### Page {pno}\n\n*(Drawing sheet — no machine-readable text; consult the PDF.)*")
        else:
            pages.append(f"### Page {pno}\n\n{raw}")
    return "\n\n---\n\n".join(pages), figures

def main():
    OUT.mkdir(exist_ok=True)
    ids = sys.argv[1:] or list(DOCS)
    for did in ids:
        stem, method, lang, title = DOCS[did]
        pdf = SRC / f"{stem}.pdf"
        if method == "text":
            body, figs = extract_text(pdf)
            prov = ("Extracted from the stored PDF's embedded text layer with PyMuPDF, using column-aware "
                    "line placement (two-column pages are split at the gutter and each column emitted in "
                    "reading order). No OCR.")
            fidelity = ("Text-layer extraction: characters are the publisher's own, not inferred. "
                        "Reading order is reconstructed from line geometry, so paragraph flow across page "
                        "and column breaks — and table alignment — still needs visual confirmation against "
                        "the PDF. Line-number artifacts (5, 10, 15 …) may remain mid-sentence.")
        else:
            body, figs = extract_ocr(pdf, lang, stem)
            prov = (f"OCR of the stored PDF (image-only scan): `pdftoppm -r 300 -gray` piped to "
                    f"`tesseract -l {lang} --psm 1` (automatic layout detection, for two-column text).")
            fidelity = ("**OCR output — machine-inferred characters.** Suitable for review, search, and "
                        "locating passages. **Not authoritative:** verify every quotation and every "
                        "number/date/reference numeral against the PDF before relying on it in a filing "
                        "or in the mapping matrix.")
        figline = f"\n> **Drawing sheets (no text):** pages {', '.join(map(str, figs))}.\n" if figs else ""
        md = f"""# {did} — {title}

> **WORKING TRANSCRIPTION — NOT AN OFFICIAL COPY AND NOT FOR FILING.**
>
> Source: `../{stem}.pdf` (see `../README.md` for that copy's provenance and verification status).
> Generated 16.07.2026. {prov}
>
> {fidelity}
{figline}
---

{body}
"""
        (OUT / f"{did}_{stem.split('_', 1)[1] if '_' in stem else stem}.md").write_text(md, encoding="utf-8")
        chars = len(re.sub(r"\s", "", body))
        print(f"{did:>3} {method:>4} {str(lang or '-'):>11}  {chars:>7} chars  figs:{len(figs)}")

if __name__ == "__main__":
    main()
