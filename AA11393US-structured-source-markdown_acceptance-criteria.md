# AA11393US — Structured-Source Markdown Acceptance Criteria

> **OPERATIVE INTERNAL CONTROL · NOT FOR FILING**
>
> This is the current acceptance contract coupled to
> [`AA11393US-structured-source-markdown_technical-description.md`](AA11393US-structured-source-markdown_technical-description.md).

## Pass rule

Conformance exists only when all ten criteria pass against one exact clean Git commit and immutable
final snapshot. A warning, unknown result, inferred authority, undeclared consumer read, stale
generated file, unresolved reference, unsupported conversion, dirty checkout, or assurance claim
beyond the machine evidence is a failure.

A pass proves only the machine properties below. It does not certify human attention, PDF
transcription fidelity, authenticity, legal correctness, counsel approval, filing readiness, or
filing authorization.

<!-- SSM-AC-TABLE:START -->
| ID | Required outcome | Required evidence and enforcer |
|---|---|---|
| **SSM-AC-01 — Authority and registry closure** | Every package has one declared authority scheme, one registered XML interface, exact scheme-permitted files, and exact consumer-to-package edges. Each edge declares `xml` or `markdown` and reads only that representation; dependencies cannot bypass it. Package registries contain no coverage-artifact field; a retained coverage view is a declared consumer output. File type or consumer choice never changes authority. | Bidirectional registry/file/consumer census; missing, duplicate, wrong-role, inferred-authority, dependency-bypass, undeclared-read, orphan coverage artifact, ignored, and untracked fixtures. |
| **SSM-AC-02 — XML item, format, and metadata closure** | Every XML file uses its current schema/profile, UTF-8 XML 1.0 and NFC, secure parsing, and raw/canonical semantic digests. Every item has its scheme-declared stable ID and one owner for each applicable content, metadata, provenance, dependency, and endpoint field. Old formats, unsafe constructs, position-derived IDs, arbitrary extensions, mixed ownership, and self-bound relation digests fail. | Schema/profile/parser validation; NFC, raw/semantic digest, ID-stability, field-ownership, unknown-field, mixed-ownership, and item-locality tests. |
| **SSM-AC-03 — PDF evidence closure** | Each PDF package has one exact manifest-bound stored PDF fidelity authority, one asserted transcription XML, one generated Markdown view, and one manifest. Every transcribed item has page/region provenance and disclosed uncertainty. Results never claim that machine checks prove fidelity or authenticity. | PDF checksum, manifest, provenance, uncertainty, asset, generated-view, OCR-authority, and false-fidelity-result tests. |
| **SSM-AC-04 — Authored-Markdown closure** | Markdown remains the sole authored-content authority. Generated XML preserves every supported item, stable ID, substantive metadata field, link, claim, table cell, advisory, heading, and order. Its non-stored back-render has ordered Pandoc-AST equality after exactly the profile-listed normalizations, and XML equals regeneration. | Pinned GFM/Pandoc comparison; add/drop/reorder, unsupported-construct, hidden-content, manual-generated-edit, and second-Markdown-owner tests. |
| **SSM-AC-05 — Relation and reference closure** | Relation XML owns each assertion and binds exact typed, directional, digest-aware endpoints. Every endpoint and generated forward/reverse link resolves. Duplicate ownership, copied assertions, stale or ambiguous targets, inferred retargeting, and endpoint-driven authority promotion fail. | Relation census, endpoint resolver, generated-view comparison, and duplicate/stale/swap/retarget/authority-promotion tests. |
| **SSM-AC-06 — Conversion, coverage, and downstream interface** | Generated representations reproduce byte-for-byte. Coverage is computed for every package and maps PDF XML items to provenance and Markdown, authored Markdown items to XML and semantic back-render, and relation fields to Markdown and endpoints. A declared downstream coverage view reproduces that computation; otherwise no stored coverage artifact exists. Registered XML consumers receive authority role, typed items, metadata, provenance, and relations without fallback or authority promotion. | Cross-process regeneration, computed-coverage census, conditional consumer-view comparison, consumer read log, and undeclared/stale coverage, wrong-representation, field-loss, fallback, and authority-promotion fixtures. |
| **SSM-AC-07 — Assurance separation** | Git supplies the operative committed bytes; machine results report conformance only. No reviewer registry, approval inventory or record, confirmation token, approval resolver, self-attestation, or implementation-bound human envelope exists. | Targeted approval-path/import/command scan and result-message tests; negative approval, reviewer, fidelity, and legal-authorization fixtures. |
| **SSM-AC-08 — Commands, writes, and efficiency** | Commands expose only the documented surface, never write authority files, validate before writes, and atomically replace only permitted derived files. Package commands inspect only their target and dependencies, compute coverage without persisting it, and perform no repeated whole-corpus pass. Each pre-test and final post-test phase builds fresh shared indexes. | Command/write allowlists; coverage no-write, rollback, external-mutation, crash-residue, target-scope, repeated-whole-corpus-pass, phase-isolation, and environment tests. |
| **SSM-AC-09 — Audit and final-snapshot closure** | One clean commit, Git-addressable evidence, the documentation pair, executable registries, locked environment, and one current `validate-current` result close the audit. The gate is read-only, runs all registered tests in isolation, and revalidates the unchanged final snapshot. No export or stored receipt substitutes for execution. | Git/index/worktree, controlled-path, environment, test-isolation, post-test mutation, detached-export, stored-receipt, and final-snapshot tests. |
| **SSM-AC-10 — Active implementation closure** | Registry, table, callbacks, tests, sources, schemas, profiles, commands, and consumers agree exactly. Old formats; structured-source approval/export/register/migration/compatibility paths; and unused package-level coverage fields, artifacts, persistence code, comparisons, fixtures, and tests are absent. Coverage computation remains mandatory, each current conversion has one pathway, and consumers have no undeclared reader. | Exact control/source census, targeted forbidden residue and coverage-persistence scans, current-family tests, registry/table regeneration, and global result. |
<!-- SSM-AC-TABLE:END -->

## Acceptance evidence boundary

The executable acceptance registry is the machine-readable source for `SSM-AC-01` through
`SSM-AC-10`; the marked table is its deterministic projection. Each criterion maps to one callback,
and every callback maps back to one criterion. Each registered test declares a nonempty criterion
set and may support more than one criterion.

The global runner emits one ephemeral machine result bound to the exact commit and snapshot. It is
not stored and is not human-review, fidelity, authenticity, legal, counsel, readiness, or
filing-authorization evidence. Git alone retains drafting and implementation history.
