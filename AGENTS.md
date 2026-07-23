# Repository Guidelines

## Project Structure & Module Organization

This repository is a patent-prosecution document corpus maintained under the maximum-honest-defensibility discipline stated in the root `README.md` under "Purpose"; read every rule below against that purpose. `US/normal-allowance/` and `US/allowance-first/` contain the two claim strategies. Shared IDS, filing-control, and public-comment materials belong in `US/common/`; do not fork them into strategy directories. `US/prior-art/` stores canonical source PDFs, `markdown/` review transcriptions, `searchable/` OCR convenience copies, and `.pipeline/` conversion utilities. `PCT/`, `PPA2/`, and `ITA/` hold filing and prosecution records. `navigator/` contains the edition-blind HTML5 navigator pipeline, closed schemas, reviewed mappings, verification records, tests, and committed current build products. Keep response drafts in their existing response directory.

## Build, Test, and Development Commands

Use the navigator's strict current-state and test gates together with the document-integrity checks:

```sh
sh navigator/tools/pre-commit-check.sh
python3 -m unittest discover -s navigator/tests -p 'test_*.py'
git diff --check
git diff --name-only -z -- '*.md' | xargs -0 -n 1 pandoc --from=gfm --to=html -o /dev/null
(cd US/prior-art && shasum -a 256 -c .pipeline/pdf-source-checksums.sha256)
python3 navigator/build.py verify-current
```

These validate deterministic checked-in candidates, full software behavior, whitespace, changed Markdown rendering, source checksums, and finally the immutable live navigator state. `verify-current` is the last command because it isolates discovered tests, revalidates the full closure, and certifies the final repository snapshot. Follow `navigator/RUNBOOK-content-sync-and-regeneration.md` for content changes and release regeneration. Regenerate transcriptions only deliberately: `cd US/prior-art && python3 .pipeline/convert.py A1`.

## Documentation Style & Naming Conventions

Use GitHub-flavored Markdown, descriptive headings, compact prose, and readable tables. Prefer relative links within repository documents. Follow established names such as `AA11393US-AF-US_claim-set_DRAFT.md`, using `AF` or `NA` consistently and retaining document-status suffixes such as `_DRAFT` and `_MEMO`. Artifact types and their naming patterns are classified in the root `README.md` under "Artifact taxonomy"; identifiers and controlled-vocabulary terms (strategy IDs, support-posture codes, DW register, AF-CONT controls, art inventory IDs) are defined in the root `GLOSSARY.md`, which points to each term's controlling document.

Never edit canonical prior-art PDFs or silently treat OCR text as authoritative.

## Hard Live-Status-Only Requirement

All authored package documents and live navigator configuration **must state only the current operative state**: conclusions, evidence, actions, owners, deadlines, triggers, active schemas, and active content versions. Never retain revision histories, maintenance logs, superseded wording, correction or activation narratives, commit narratives, explanations of wording or score evolution, compatibility aliases, or implicit upgrade paths. Git is the sole drafting and implementation history. Digest-addressed same-schema verification records may persist only as append-only evidence and cannot authorize content unless every current exact-side binding matches. Retain legally operative filing, publication, priority, and prosecution facts and source provenance only as current evidence.

## Testing Guidelines

After changing claims, verify claim count, dependency, antecedent basis, support mappings, and every affected matrix row. Re-score art when claim wording changes. Check quotations against the source PDF, especially OCR material. Confirm local links and render any changed complex table before review. Navigator changes must leave zero stale or pending owners, pass the full test suite, and reproduce candidates byte-for-byte through the pre-commit check. Unsupported schema, canon, registry, or record formats must fail closed before writes; do not add backward-compatibility branches.

## Commit & Pull Request Guidelines

Recent commits use imperative subjects such as `Refine`, `Update`, and `Add`. Keep each commit to one coherent document or prosecution objective. In a pull request, identify the strategy/version, summarize the current-state result, disclose whether claim text or matrix scores changed, list validation commands, and flag unresolved counsel gates. Include rendered evidence only when a table, figure, or layout materially changes.

## Confidentiality & Filing Controls

Respect internal-review and not-for-filing labels. Do not represent applicant analysis as counsel advice, duplicate canonical shared records, or circulate sensitive materials beyond the approved review purpose.
