# AA11393US — Structured-Source HTML5 Migration: Acceptance Criteria (DRAFT)

> **PROPOSED DEFINITION OF DONE · INTERNAL DRAFT · STATUS 24 JULY 2026**
>
> This is the succinct acceptance contract coupled to
> [`AA11393US-structured-source-html5-migration_technical-description_DRAFT.md`](AA11393US-structured-source-html5-migration_technical-description_DRAFT.md).
> It authorizes no filing, release, or claim of implementation. The technical description controls
> migration architecture and terminology. Structured-source Markdown acceptance and navigator
> `AC-01` through `AC-20` remain independently mandatory.

## Pass rule

Conformance exists only when all ten recurring criteria, all navigator `AC-01` through `AC-20`,
and the exact upstream structured-source result pass against the same immutable final snapshot. No
criterion or callback may be skipped, copied, inferred, or treated as not applicable.
Automated and identified-human evidence are cumulative. A warning, unknown result, stale or
profile-inconsistent record, unexplained comparison difference, unclassified field/literal,
undeclared read/write, or post-test mutation is a failure.

<!-- SH5-AC-TABLE:START -->
| ID | Required outcome | Required evidence and enforcer |
|---|---|---|
| **SH5-AC-01 — Exact upstream dependency** | The build recomputes and validates the exact accepted structured-source result/export on the same immutable snapshot. Upstream XML, dependencies, source-level relations, assets, identities, digests, coverage, approvals, root project/lock, Python pin, required host `uv`, installed distributions, and implementation/import census are exact-current. The navigator has read-only access to that export and toolchain result; it cannot consume upstream Markdown, repair/write an upstream plane, or substitute a second project, lock, environment, interpreter, package source, or tool version. | Typed upstream child-result, export, and toolchain validation; same-snapshot/digest binding; missing, stale, warning, skipped, alternate-package, alternate-environment, Markdown-read, upstream-write, and source-repair fixtures. |
| **SH5-AC-02 — Navigator XML ownership and approval** | Every exact `na__pct`/`af__pct` relation and `shared`/`na`/`af` wording bundle has one navigator XML owner, deterministic Markdown/coverage companion, exact profile, registered consumer scope, current projection record, and current semantic/content record under the closed approval types. Relations bind current upstream endpoint tuples without duplicating/overriding SSP truth. Wording slots bind exact type, formatter, escape class, cardinality/order, and value origin. Same-schema superseded records remain valid append-only evidence. | Navigator relation/wording schema, path, view/coverage, and registry validation; exact-side approval resolver; owner-conflict, duplicate assertion, endpoint drift, slot-origin/type/order/escape, stale/ambiguous record, and profile-switch fixtures. |
| **SH5-AC-03 — Current production-input ownership** | A schema/AST-derived census assigns every current production JSON/XML leaf and production source/template/schema-default/configuration string literal exactly once to upstream export XML, navigator relation XML, navigator wording XML, retained control, non-consumer code, or a closed mechanical derivation. Every current owner, target ID, consumer use, and derivation is exact; no migration/retirement classification or unowned operative semantic remains. | Complete current field/literal/consumer ownership registry; language-aware use analysis; reverse rendered-origin scan; field/literal mutation tests; missing/additional/multiple/unclassified/wrong-owner/wrong-use fixtures. |
| **SH5-AC-04 — Direct secure consumer** | Production semantics enter only through the allowlisted secure XML gateway and immutable ephemeral model. Exact text, identities, dependencies, relation endpoints, and wording origins are preserved. No Markdown, PDF/OCR, semantic JSON, persisted XML-to-JSON model, arbitrary runtime string, fallback, cache, alias, automatic retargeting, or upstream write remains. | Production-source/import inventory; static scan and runtime read/write log; model-to-origin reverse trace; forbidden-reader/store/fallback, undeclared-read/write, normalization, inference, and retarget fixtures. |
| **SH5-AC-05 — Deterministic and attributable HTML5** | Fresh processes in the exact accepted upstream `uv` environment reproduce every registered candidate, HTML5 surface, inventory, manifest, and sealed artifact byte-for-byte from exact locked upstream export, navigator XML/approvals, controls, code, templates, assets, and toolchain. The build binds the root project/lock, Python, host `uv`, installed-distribution, and import-origin identities. Every authored visible string and relation reverse-maps to exact XML and slot-origin bindings; only closed mechanical markup/derivations are added. | Cross-process double build through no-cache/offline/locked/no-sync `uv`; project/lock/tool/interpreter/distribution/import-origin closure; exact byte/inventory comparison; rendered-string/relation provenance scan; hostile-value/context-escape, ordering, locale, timestamp/path, alternate-environment, undeclared-input, missing/additional-output, and nondeterminism fixtures. |
| **SH5-AC-06 — Independent product acceptance** | The complete independent navigator `AC-01`–`AC-20` result passes on the same snapshot, preserving every navigator-owned edition, navigation, interaction, accessibility, no-JS, print, security, content, QA, release, artifact, and bundle requirement. Mandatory navigator callback ownership cannot silently shrink, and SH5 neither restates nor infers those results. | Exact navigator registry/result binding; bidirectional navigator-callback ownership; full navigator suites; removed-callback, copied-result, missing-result, warning/skipped-result, and snapshot-mismatch fixtures. |
| **SH5-AC-07 — Downstream exact-side binding** | Every navigator-owned candidate, attestation, QA, sealed artifact/checksum, release, bundle, and current record selected by the independent navigator result binds the exact current upstream export plus navigator relation/wording XML and approvals. SH5 defines no competing QA, pin, version-label, release, or bundle policy. | Input-lock and record-provenance checks; exact navigator child-result and artifact-inventory binding; missing/additional/stale/wrong-input, profile-selection, and record-resolution fixtures owned by the navigator contract. |
| **SH5-AC-08 — Fail-closed writes** | Input and imported-toolchain validation precede writes; command scopes are downstream-only; output sets publish atomically or roll back every command-owned change. Commands run only through the exact no-cache/offline/locked/no-sync upstream `uv` environment. Invalid input, missing or drifted tool/environment side, interruption, or unsupported version leaves command-owned outputs and the project environment unchanged. Detected external mutation stops further attributable writes and makes the global final-snapshot comparison fail. No implicit sync, install, cache fallback, ambient-Python fallback, or backward-compatibility branch writes or authorizes output. | Command/plane registry; toolchain and import-origin preflight; repository/environment before/after snapshots; missing/drifted/alternate-toolchain, forbidden-sync/install/cache/ambient-import, pre-write, atomicity, rollback, interruption, concurrent-mutation, undeclared-read/write, unsupported-version, partial-publication, and output-confinement fixtures. |
| **SH5-AC-09 — Complete post-test final state** | The repository-global outer gate solely owns materialized test execution, repository/environment no-write postconditions, complete post-test re-derivation of upstream toolchain/export, SH5, navigator, rendered provenance, candidate, QA/release/bundle/record, and exact byte/inventory closures, plus final live-snapshot equality. SH5 supplies namespaced callbacks and cannot certify these outer observations early. | Global full post-test revalidation including root project/lock, host `uv`, Python, distribution, and import-origin closure; last-sorted passing mutator fixtures for every controlled plane and the project environment; isolated-test and live-mutation tests; sole outer-control ownership and no-write/result-census/final-snapshot postconditions. |
| **SH5-AC-10 — Active final closure and traceability** | The final tree contains only the single direct XML data path, exact current artifacts, and the one upstream-owned root `uv` project/lock contract. No old reader/store, semantic JSON, adapter, dual path, fallback, alias, migration field, archive, baseline runner, mapping, diff/render, temporary record/lease/locator, nested project, second lock/environment, migration-only dependency, implicit bootstrap, or non-operative narrative remains. A distinct executable registry owns all ten criteria and namespaced callbacks; its generated table, complete ephemeral receipt, result census, and bindings to—not copies of—the upstream toolchain/export and navigator results are exact. Only the global outer gate may promote criteria or report repository currentness. | Forbidden-state/residue, nested-project/alternate-lock, and history-field scan; registry/table regeneration; project/lock/distribution/import inventory; bidirectional child-callback meta-tests; missing/duplicate/unregistered-control fixtures; exact child-result/toolchain bindings, ephemeral receipt validation, and final integrated `uv` current-state command. |
<!-- SH5-AC-TABLE:END -->

## Draft-only implementation gate

`SH5-MIG-01` is mandatory during implementation but is not a recurring criterion. After the first
stage passes, a separate immutable navigator baseline is captured outside the repository and
all worktrees. Its closed manifest binds every old production input, schema-derived field, source/
template literal, consumer, relation and wording value, candidate/HTML5 artifact, release/QA/bundle
side, toolchain, interaction fixture, and render setting. Every old field/literal maps exactly once
to source XML, relation XML, wording XML, retained control, non-consumer code, a closed derivation,
or identified-human `retired-transition-only`. Retirement requires proven migration/history/review-
transport classification and final non-use; no operative semantic may retire.

The old navigator runs only in an isolated baseline process and may read baseline generated
Markdown. The isolated migration comparator's new runner reads only the exact upstream export and
securely validated, digest-locked provisional navigator XML; it writes only temporary ineligible
comparison outputs and neither consumes nor issues recurring approval. The gate compares exact
text/relation inventories, normalized semantic DOM, accessibility tree, routes and links,
interaction states, no-JS behavior, security observations, print output, screenshots, and
every production field/wording/relation semantic. Mutation tests prove completeness. An identified
human dispositions every nonzero semantic, behavioral, accessibility, print, or visual difference.
No similarity threshold or broad mask can excuse a substantive change.

Old/new comparison dependencies execute only from a separately declared migration group in the
upstream-owned root `uv.lock`. Before recurring acceptance, that group and every migration-only
distribution are removed, the operative root lock is regenerated, and upstream toolchain
acceptance plus the downstream no-cache/offline/locked/no-sync distribution and import-origin
census are re-proved.

The baseline path is registered before creation under an exclusive OS-held lease. Cleanup is
idempotent and may recover only a proven-stale lease. Before recurring acceptance, the old runner,
archive, field mappings, renders, diffs, screenshots, temporary record, adapter/dual-reader code,
old semantic stores, migration fields/controls, locator/lease, and the migration sections are
removed. The draft pair is rewritten/renamed as present-tense operative documents; draft status,
old/new and future-cutover narrative, temporary-evidence language, obsolete numbering, and stale
links are removed. From the cleaned final code/usage registry, relation/wording views and coverage
are regenerated and receive fresh recurring approvals before downstream regeneration. Failure to
prove absence prohibits acceptance. The temporary comparison never replaces current navigator QA
or release evidence. `SH5-MIG-01` is excluded from the recurring receipt and result census.

## Acceptance evidence boundary

The executable registry is the sole operative source of `SH5-AC-01` through `SH5-AC-10`; the
marked table is its deterministic GFM projection. Its namespaced callbacks are owned
bidirectionally and cannot omit mandatory evidence. The registry binds complete upstream and
navigator results without duplicating their criterion lists. One separately registered global
outer-postcondition map is the sole owner of test isolation, post-test revalidation, no-write,
criterion promotion, and final-snapshot controls.

A fresh runner emits an ephemeral ten-criterion callback receipt bound to exact inputs and one
immutable snapshot, including the exact imported project/lock, host `uv`, Python, installed-
distribution, and import-origin sides. The outer gate validates it, runs complete post-test
revalidation, and promotes criteria only after final snapshot equality. Neither the receipt nor
this registry can report repository currentness independently. Only
`uv --no-cache --offline run --locked --no-sync python -m navigator validate-current` may compose
all same-snapshot upstream, SH5, navigator, QA/release/bundle, and outer-postcondition evidence into
`status: current`.
