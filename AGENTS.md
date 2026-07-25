# Repository Guidelines

## Project Structure & Module Organization

This repository is a patent-prosecution document corpus maintained under the maximum-honest-defensibility discipline stated in the root `README.md` under "Purpose"; read every rule below against that purpose. `US/normal-allowance/` and `US/allowance-first/` contain the two claim strategies. Shared IDS, filing-control, and public-comment materials belong in `US/common/`; do not fork them into strategy directories. Each `US/prior-art/<ID>/` package co-locates its canonical source PDF, asserted transcription XML, generated Markdown review view, source manifest, and any declared non-authoritative convenience derivative. `PCT/`, `PPA2/`, and `ITA/` hold filing and prosecution records. `structured_source/` contains the closed XML schemas, profiles, content registry, converters, and validation implementation. `navigator/` contains the edition-blind HTML5 navigator pipeline, closed schemas, reviewed mappings, exact active verification-record graph, tests, and committed current build products. Keep response drafts in their existing response directory.

## Build, Test, and Development Commands

Use the canonical current-state and document-integrity gate:

```sh
uv --no-cache --offline run --locked --no-sync python -m navigator validate-current
```

One command covers snapshot-bracketed verification of the immutable structured-source and navigator state: authority schemes, XML identity, deterministic representations, computed coverage, reference and consumer closure, pin plans, deterministic checked-in candidates, bundle and authorization chains, exact navigator record and distribution inventories, both registered test families in a materialized sandbox, `git diff --check` whitespace, current changed-Markdown rendering, and co-located `US/prior-art` source manifests. It certifies only the final unchanged repository snapshot. The audit boundary is the exact clean Git commit, its checkout and supplied history, the documentation pair and executable registries, and the current gate result. Follow `navigator/RUNBOOK-content-sync-and-regeneration.md` for content changes and release regeneration.

## Documentation Style & Naming Conventions

Use GitHub-flavored Markdown, descriptive headings, compact prose, and readable tables. Prefer relative links within repository documents. Follow established names such as `AA11393US-AF-US_claim-set_DRAFT.md`, using `AF` or `NA` consistently and retaining document-status suffixes such as `_DRAFT` and `_MEMO`. Artifact types and their naming patterns are classified in the root `README.md` under "Artifact taxonomy"; identifiers and controlled-vocabulary terms (strategy IDs, support-posture codes, DW register, AF-CONT controls, art inventory IDs) are defined in the root `GLOSSARY.md`, which points to each term's controlling document.

Never edit canonical prior-art PDFs or silently treat OCR text as authoritative.

## Hard Live-Status-Only Requirement

All authored package documents, live configuration, structured-source registries, navigator verification stores, and current build products **must state or contain only the current operative state**: conclusions, evidence, actions, owners, deadlines, triggers, active schemas, active content versions, and records required by the current navigator authorization graph. Never retain revision histories, maintenance logs, superseded wording or records, correction or activation narratives, commit narratives, explanations of wording or score evolution, compatibility aliases, implicit upgrade paths, or non-current artifacts in the live checkout. Git is the sole drafting, implementation, and displaced-record history. Structured source has no approval inventory, reviewer record, self-attestation, implementation register, or export bundle. If the navigator contract requires verification records, its live store equals the exact active reachable graph; stale, duplicate, rejected, retired-format, and unreachable records are absent. Retain legally operative filing, publication, priority, and prosecution facts and source provenance only as current evidence.

## Testing Guidelines

After changing claims, verify claim count, dependency, antecedent basis, support mappings, and every affected matrix row. Re-score art when claim wording changes. Check quotations against the source PDF, especially OCR material. Confirm local links and render any changed complex table before review. Structured-source changes must preserve the declared authority direction, reproduce every generated representation, and keep coverage computed rather than stored. Navigator changes must leave zero stale or pending owners, retain only the active reachable verification graph, pass the full test suite, and reproduce candidates byte-for-byte between candidate and release. Unsupported schema, canon, registry, or record formats must fail closed before writes; do not add backward-compatibility branches.

## Commit & Pull Request Guidelines

Recent commits use imperative subjects such as `Refine`, `Update`, and `Add`. Keep each commit to one coherent document or prosecution objective. In a pull request, identify the strategy/version, summarize the current-state result, disclose whether claim text or matrix scores changed, list validation commands, and flag unresolved counsel gates. Include rendered evidence only when a table, figure, or layout materially changes.

## Confidentiality & Filing Controls

Respect internal-review and not-for-filing labels. Do not represent applicant analysis as counsel advice, duplicate canonical shared records, or circulate sensitive materials beyond the approved review purpose.
