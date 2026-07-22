# Repository Guidelines

## Project Structure & Module Organization

This repository is a patent-prosecution document corpus. `US/normal-allowance/` and `US/allowance-first/` contain the two claim strategies. Shared IDS, filing-control, and public-comment materials belong in `US/common/`; do not fork them into strategy directories. `US/prior-art/` stores canonical source PDFs, `markdown/` review transcriptions, `searchable/` OCR convenience copies, and `.pipeline/` conversion utilities. `PCT/`, `PPA2/`, and `ITA/` hold filing and prosecution records. Keep response drafts in their existing response directory.

## Build, Test, and Development Commands

There is no software build or unit-test suite. Use document-integrity checks:

```sh
git diff --check
git diff --name-only -z -- '*.md' | xargs -0 -n 1 pandoc --from=gfm --to=html -o /dev/null
cd US/prior-art && shasum -a 256 -c .pipeline/pdf-source-checksums.sha256
```

These validate whitespace, changed Markdown rendering, and source checksums. Regenerate transcriptions only deliberately: `cd US/prior-art && python3 .pipeline/convert.py A1`.

## Documentation Style & Naming Conventions

Use GitHub-flavored Markdown, descriptive headings, compact prose, and readable tables. Prefer relative links within repository documents. Follow established names such as `AA11393US-AF-US_claim-set_DRAFT.md`, using `AF` or `NA` consistently and retaining document-status suffixes such as `_DRAFT` and `_MEMO`.

Never edit canonical prior-art PDFs or silently treat OCR text as authoritative.

## Hard Live-Status-Only Requirement

All authored package documents **must state only the current operative state**: conclusions, evidence, actions, owners, deadlines, and triggers. Never retain revision histories, maintenance logs, superseded wording, correction or activation narratives, commit narratives, or explanations of wording or score evolution. Git is the sole drafting history. Retain legally operative filing, publication, priority, and prosecution facts and source provenance only as current evidence.

## Testing Guidelines

After changing claims, verify claim count, dependency, antecedent basis, support mappings, and every affected matrix row. Re-score art when claim wording changes. Check quotations against the source PDF, especially OCR material. Confirm local links and render any changed complex table before review.

## Commit & Pull Request Guidelines

Recent commits use imperative subjects such as `Refine`, `Update`, and `Add`. Keep each commit to one coherent document or prosecution objective. In a pull request, identify the strategy/version, summarize the current-state result, disclose whether claim text or matrix scores changed, list validation commands, and flag unresolved counsel gates. Include rendered evidence only when a table, figure, or layout materially changes.

## Confidentiality & Filing Controls

Respect internal-review and not-for-filing labels. Do not represent applicant analysis as counsel advice, duplicate canonical shared records, or circulate sensitive materials beyond the approved review purpose.
