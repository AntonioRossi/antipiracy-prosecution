# Repository Guidelines

## Project Structure & Module Organization

This repository is a patent-prosecution document corpus maintained under the maximum-honest-defensibility discipline stated in the root `README.md` under "Purpose"; read every rule below against that purpose. `US/normal-allowance/` and `US/allowance-first/` contain the two claim strategies. Shared IDS, filing-control, and public-comment materials belong in `US/common/`; do not fork them into strategy directories. Each `prior-art/<ID>/` package co-locates its canonical source PDF, asserted transcription XML, generated Markdown review view, source manifest, and any declared non-authoritative convenience derivative. `PCT/`, `PPA2/`, and `ITA/` hold filing and prosecution records. `structured_source/` contains the closed XML schemas, profiles, content registry, converters, and validation implementation. `navigator/` contains the edition-blind HTML5 navigator pipeline, closed schemas, authoritative navigator relations and wording, tests, and stored current build products. Keep response drafts in their existing response directory.

## Build, Test, and Development Commands

Use the canonical current-state and document-integrity gate:

```sh
uv --no-cache --offline run --locked --no-sync python -m navigator validate-current
```

One command captures and retains the governed current worktree, including relevant untracked files; validates authority schemes, XML identity, deterministic representations, computed coverage and substantive-origin tracing, references, declared consumer handoffs, the secure XML gateway, immutable models, stored products, captured-file whitespace, every retained Markdown document, source manifests, and all registered tests in an isolated materialization; then fails if the final recapture differs by path, mode, or bytes. Repository status, index state, commit identity, and history are outside the pass conditions. A pass is only ephemeral technical status for independent inventor and counsel review; human evidence and substantive review remain authoritative. Follow `navigator/RUNBOOK-content-sync-and-regeneration.md` for content changes and release regeneration.

## Git Manipulation Forbidden

Validation MUST NOT invoke, inspect, infer from, or depend on Git status, the index, staging, commits, branches, tags, hashes, diffs, hooks, configuration, or history, and any implementation that does so MUST fail acceptance.

## Documentation Style & Naming Conventions

Use GitHub-flavored Markdown, descriptive headings, compact prose, and readable tables. Prefer relative links within repository documents. Follow established names such as `AA11393US-AF-US_claim-set_DRAFT.md`, using `AF` or `NA` consistently and retaining document-status suffixes such as `_DRAFT` and `_MEMO`. Artifact types and their naming patterns are classified in the root `README.md` under "Artifact taxonomy"; identifiers and controlled-vocabulary terms (strategy IDs, support-posture codes, DW register, AF-CONT controls, art inventory IDs) are defined in the root `GLOSSARY.md`, which points to each term's controlling document.

Never edit canonical prior-art PDFs or silently treat OCR text as authoritative.

## Hard Live-Status-Only Requirement

All authored package documents, live configuration, structured-source registries, navigator controls, and current build products **must state or contain only the current operative state**: conclusions, evidence, actions, owners, deadlines, triggers, active schemas, active content versions, and generated products. Never retain revision histories, maintenance logs, superseded wording or controls, correction or activation narratives, commit narratives, explanations of wording or score evolution, compatibility aliases, implicit upgrade paths, or non-current artifacts in the live checkout. Git is drafting history only and has no validation authority. The repository has no approval inventory, reviewer record, implementation register, validation-result or receipt store, auxiliary release plan, stored lineage or coverage artifact, exported validation record, migration reader, or compatibility path. Retain legally operative filing, publication, priority, and prosecution facts and source provenance only as current evidence.

Each completed schema, field, behavior, command, workflow, handoff, or product change must leave its
controlling technical description, paired acceptance criteria, data-only acceptance registry,
configuration, implementation, tests and vectors, generated representations, and applicable stored
products in one coherent retained current state. Do not hand off a documentation-only,
implementation-only, workflow-only, or product-only result. Update data-only acceptance registries
before regenerating their Markdown table regions; never edit a generated acceptance row as an
independent owner.

## Testing Guidelines

After changing claims, verify claim count, dependency, antecedent basis, support mappings, and every affected matrix row. Re-score art when claim wording changes. Check quotations against the source PDF, especially OCR material. Confirm local links and render any changed complex table before review. Structured-source changes must preserve the declared authority direction, reproduce every generated representation, and keep coverage computed rather than stored. Navigator changes must pass the full test suite, preserve exact relation endpoints and controlled wording, and reproduce candidates byte-for-byte between candidate and release. Unsupported schema, canon, registry, or content formats must fail closed before writes; do not add backward-compatibility branches.

## Commit & Pull Request Guidelines

Repository agents do not stage files or create, amend, sign, tag, or otherwise manage commits. The
repository owner alone manages the Git index and history. Agents leave worktree changes unstaged and
report the validated change scope and any suggested commit subject for the owner's use.

Recent commits use imperative subjects such as `Refine`, `Update`, and `Add`. Keep each commit to one coherent document or prosecution objective. In a pull request, identify the strategy/version, summarize the current-state result, disclose whether claim text or matrix scores changed, list validation commands, and flag unresolved counsel gates. Include rendered evidence only when a table, figure, or layout materially changes.

## Confidentiality & Filing Controls

Respect internal-review and not-for-filing labels. Do not represent applicant analysis as counsel advice, duplicate canonical shared records, or circulate sensitive materials beyond the approved review purpose.
