# US/prior-art/markdown — Working Transcriptions

> **WORKING TRANSCRIPTIONS — NOT OFFICIAL COPIES AND NOT FOR FILING.**
>
> One markdown transcription per stored prior-art PDF, generated 16.07.2026 so that `../AA11393US-claim-document-mapping-matrix_DRAFT.md` can be scored against the documents' actual full text rather than their faces and abstracts. IDs match `../README.md` and the IDS inventory.
>
> **Never quote from these files into a filing, an Office response, or the matrix without checking the passage against the source PDF.** That applies to all of them, and with particular force to the OCR set: OCR infers characters, and reference numerals, dates, and publication numbers are exactly where it fails most quietly.

## Why these exist

Nine of the twenty stored PDFs are image-only scans with no text layer: they could not be read, searched, or quoted at all. The mapping matrix's `nr` cells and its `face only` / `abstract+face` review depths were a direct consequence. These transcriptions exist to retire that limitation and let counsel score the grid against what the documents actually say — the 16.07.2026 full-text re-score (mapping matrix §§7–8) was performed against them.

## The two generation paths

| Path | Documents | Method |
|---|---|---|
| **Text-layer extraction** (no OCR) | A2, A3, A4, A5, A6, A7, A8, A10, B1, B8, C8 | PyMuPDF, column-aware (`.pipeline/columns.py`). Characters are the publisher's own. |
| **OCR** | A1, A9, B2, B3, B4, B5, B6, B7, B9 | `pdftoppm -r 300 -gray` → `tesseract --psm 1`. Characters are machine-inferred. |

Languages: `eng`, except B5 and B6 (`chi_sim+eng`). B1 has a native Chinese text layer and needed no OCR.

**On column handling.** US patent PDFs interleave their two text columns line by line, so `pdftotext` — with or without `-layout` — and PyMuPDF's own `sort=True` all produce scrambled, unquotable prose. The text path therefore assigns each line to a column by x-midpoint and emits the columns separately; the OCR path relies on tesseract `--psm 1` layout detection, which handles columns natively. Both were validated on A4's claim 1, which reads as continuous claim text in the output.

**On drawing sheets.** Pages that are drawings are marked `*(Drawing sheet — no machine-readable text)*` rather than being presented as prose, since OCR of a figure yields plausible-looking noise. The classifier is script-aware (CJK is denser and needs different thresholds than Latin) and is deliberately eager: a false positive costs a page you must open the PDF to read, while a false negative silently passes figure noise off as text. Its per-document counts match the documents' own declarations — A1: 10 sheets (face says 10), A9: 8 (face says 8), B6: 9 (face says 附图9页).

## Fidelity — what is and is not established

- **Corroborated:** the fresh A1 OCR was compared against the repository's independently produced transcription at `../../PCT/AA11393US-PCT_office_action_markdown/cited_US2021-0352381A1.md`. Substantive paragraphs agree at **99.3–99.4%** ([0016], [0045]). Two independent OCR passes concurring is meaningful evidence of accuracy — it is not proof of correctness for any specific character.
- **Page counts** match the source PDFs exactly for all 19 documents.
- **Not established:** that any individual numeral, date, or quotation is correct. Known residual issues: patent line numbers (5, 10, 15 …) can land mid-sentence; paragraphs spanning a page break are split by the `### Page N` markers; Chinese OCR shows occasional character substitutions (e.g. 嵌入 rendered as 藤入/甬入).

## Source integrity

The source PDFs were **not modified**. SHA-256 of all 19 was recorded before any processing (`.pipeline/pdf-source-checksums.sha256`) and re-verified after: 19/19 identical. This preserves the provenance chain documented in `../README.md`.

Verify at any time:

```
cd US/prior-art && shasum -a 256 -c .pipeline/pdf-source-checksums.sha256
```

## Related

- `../searchable/` — the same nine image-only documents with an OCR text layer added (via `ocrmypdf --skip-text`), for searching inside a PDF viewer. Copies, not originals; same not-for-filing caveat.
- `.pipeline/convert.py`, `.pipeline/columns.py` — the generators, kept so the work is reproducible. Rerun: `python3 .pipeline/convert.py [ID ...]` (needs `pymupdf`; `tesseract` with `chi_sim` for the Chinese documents).
