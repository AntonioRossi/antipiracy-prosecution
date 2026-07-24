# AA11393US — Structured-Source Markdown Migration: Acceptance Criteria (DRAFT)

> **PROPOSED DEFINITION OF DONE · INTERNAL DRAFT · STATUS 24 JULY 2026**
>
> This is the succinct acceptance contract coupled to
> [`AA11393US-structured-source-markdown-migration_technical-description_DRAFT.md`](AA11393US-structured-source-markdown-migration_technical-description_DRAFT.md).
> It authorizes no filing, release, or claim of implementation. The technical description controls
> architecture and terminology. Navigator acceptance remains independently mandatory.

## Pass rule

Conformance exists only when all ten recurring criteria pass against the same immutable final
repository snapshot. Automated and required identified-human evidence are cumulative. No criterion
may be skipped or treated as not applicable; origin-specific checks run for every package of that
origin. A warning, unknown result, deferred observation, stale binding, unregistered controlled
file, post-test mutation, or unexplained comparison difference is a failure.

<!-- SSM-AC-TABLE:START -->
| ID | Required outcome | Required evidence and enforcer |
|---|---|---|
| **SSM-AC-01 — Scope and registry closure** | One closed content registry enumerates every in-scope source, source-level relation set, dependency/endpoint allowlist, stored source, asset, generated Markdown/coverage output, required approval type, consumer, and export path. Every controlled content-plane file exists and is registered exactly once; IDs, paths, tuples, roles, and owners are unique; shared material is not forked; no orphan or duplicate semantic owner exists. A separate exact inventory closes the append-only record namespace; schema-valid superseded records are evidence, not content-registry orphans and not current authorizations. | Bidirectional registry/filesystem and record inventories; ID/path/owner uniqueness tests; dependency, endpoint, asset, record-cycle, content-orphan, embedded-relation, and unregistered-file negative fixtures. |
| **SSM-AC-02 — XML validity and identity** | Every `.source.xml` and `.relations.xml` file validates under the current closed namespace/schema/profile, secure parser policy, `xc1` canonicalization, and `ssp-xd1` digest domain. Every addressable fragment and relation has stable identity and a current canonical digest; all endpoint tuples resolve exactly. The parser and canonicalizer execute only through the exact host-provided `uv` version and repository-owned project, lock, interpreter, and installed-distribution contract. Unsupported constructs, external resources, unknown fields, duplicate IDs, raw Markdown/HTML, unresolved dependencies, stale endpoints, resource-limit violations, undeclared imports, or ambient packages fail closed. | XSD 1.1 and semantic validation; secure-parser/XXE/entity/XInclude/recovery tests; canonicalization/domain vectors; locked-environment and import-origin census; fragment/relation/claim/dependency/endpoint mutation fixtures. |
| **SSM-AC-03 — Origin, provenance, and asset integrity** | Each content package declares exactly one PDF-derivative or authored-source origin. PDF derivatives bind exact stored bytes, truthful role/status, page/region evidence, uncertainties, and assets; authored sources bind a responsible owner without fictitious external authority. OCR/searchable copies remain non-authoritative, and canonical PDFs are unchanged. | Source checksum and manifest verification; provenance/page-region/asset closure; missing, drifted, ambiguous, false-authority, role-confusion, and PDF-byte-change fixtures. |
| **SSM-AC-04 — Stand-off relation closure** | Each source-level cross-document assertion has one `.relations.xml` owner and binds exact `(documentId, fragmentId, fragmentContentDigest)` endpoints. No endpoint document, independently authored Markdown, JSON, or configuration duplicates relation truth; the generated relation Markdown may render it mechanically for review. Relation census, direction, type, assertion fields, owners, and current endpoint versions are complete and reviewable. | Relation inventory and endpoint resolver; duplicate-owner/restatement scan; relation-field and endpoint mutation/swap/staleness fixtures; forward/reverse review-anchor checks. |
| **SSM-AC-05 — Deterministic Markdown and coverage** | Fresh processes generate byte-identical GFM Markdown and coverage from only locked XML, dependencies, assets, profiles, and control data. Committed views equal regeneration, carry the source/digest warning, and are never independent inputs. Every review-relevant XML field maps to a Markdown anchor or justified closed classification, and every authored Markdown region maps back to a typed XML origin. | Cross-process double render; committed-output and Pandoc checks; schema-derived field census; bidirectional coverage; mixed-content, Unicode, table, claim, relation, link, escaping, hidden-field, and undeclared-read fixtures. |
| **SSM-AC-06 — Exact human approval** | Every consumer-eligible package has a current identified-human `projection-completeness` record followed by the origin-appropriate `source-fidelity`, `authored-content-review`, or `relation-content-review` record. Records bind all exact source, dependency, endpoint, asset, schema/parser/canon/domain, renderer, Markdown, coverage, and reviewed-census sides. Drift or ambiguity prevents resolution; same-schema superseded records remain append-only evidence. | Closed record schemas and exact-side resolver; reviewer-authority check; stale/missing/incomplete/ambiguous/model-authority fixtures; append-only record inventory across consumer/profile changes. |
| **SSM-AC-07 — Discoverability and reference closure** | Every controlled `US/` and registered PCT artifact conforms to the exact path taxonomy and one-primary bundle rule. Shared records have one `US/common/` owner; strategy material remains in its strategy tree; each prior-art ID has one co-located evidence closure. Generated routers are deterministic, and every registered inbound path, local link, semantic ID, manifest, checksum, schema, test, and runbook reference resolves without aliases, symlinks, path escapes, or silent merges. | Current path/ID/ownership registry validators; deterministic router comparison; parser-registry reference scan; misplaced, dangling, escaped, duplicated, obsolete-path, dual-primary, and apparent-duplicate fixtures. |
| **SSM-AC-08 — Approved structured export** | The export contains exact approved source/dependency/source-level-relation XML, stable identities, assets, materialized registry view, coverage and approval bindings. Its envelope is control-only and Markdown is review evidence, not export semantic authority. Within the upstream source/export plane, no unapproved XML, OCR, searchable PDF, content/relation JSON, or persisted XML-to-JSON model can supply semantics. | Export schema/digest and exact-approval validation; upstream consumer read/origin allowlist; denied-input fixtures; endpoint/dependency/asset/approval traceability and missing/additional/stale-payload tests. |
| **SSM-AC-09 — Fail-closed writes and reproducibility** | Validation completes before writes; generated sets publish atomically or roll back every command-owned change; invalid input or interruption leaves command-owned outputs unchanged. Detected external mutation stops further attributable writes and makes the global final-snapshot comparison fail. Fresh processes in the exact pre-provisioned project-local `uv` environment reproduce every view, coverage, router, manifest, and export byte-for-byte. Recurring verification is no-cache, locked, no-sync, and offline, checks project/lock consistency, performs no persistent package-manager or environment writes, and rejects a missing/mismatched `uv`, Python, lock, environment, distribution, or import origin without pip, system-Python, ambient-site-packages, implicit-sync, or unlocked-install fallback. The namespaced callbacks support complete post-test re-execution by the repository-global outer gate, which solely owns test isolation, environment/repository no-write postconditions, and final snapshot equality. | Command-plane registry; `uv`/Python/project/lock/distribution/import-origin closure; bootstrap-versus-verification separation; before/after repository and environment snapshots; missing/drifted toolchain and forbidden-fallback fixtures; atomicity/rollback/interruption/concurrency tests; cross-process reproduction; child callback receipt; global last-sorted mutating-test fixtures and outer final-state postconditions. |
| **SSM-AC-10 — Active structured-source closure** | The current structured-source state has one XML authoring path, exact views/approvals/export, complete `US/`/PCT references, one exact host-provided `uv` capability, and one repository-owned project/lock contract. It contains no independently editable migrated Markdown, importer, dual authoring source, embedded duplicate relation, alias, fallback, stale view, unapproved export, migration archive/report/record/code/dependency, temporary locator/lease, pip or implicit-bootstrap fallback, ambient dependency, or non-operative implementation narrative. The executable registry, generated acceptance table, toolchain/source inventories, namespaced callback ownership, receipt, and result census are exact; currentness is promoted only by the repository-global outer gate. | Forbidden-state and residue scan; registry/table and lock consistency regeneration; project/lock/source/distribution inventory; bidirectional child-callback meta-tests; complete ephemeral receipt/result census; global outer-result binding and final integrated snapshot verification. |
<!-- SSM-AC-TABLE:END -->

## Draft-only implementation gate

`SSM-MIG-01` is mandatory during implementation but is not a recurring criterion. Before cutover,
the affected files are copied from one immutable baseline Git tree to an owner-only temporary
archive outside the repository and all worktrees. A closed manifest and total disposition map bind
every affected Markdown, stored
or searchable PDF, extraction aid, asset, source manifest, source-level relation, router, and
reference-bearing document by path, blob, mode, size, digest, role, and old-to-new destination.

In an isolated worktree, pinned Markdown-AST comparison proves semantic closure and identical
pinned renderers produce side-by-side views and diff overlays. An identified human reviews every
nonzero visual region and resolves each text, claim, quotation, table, ordering, link/image, figure,
status, provenance, or relation difference against the stored PDF or authored intent. Old Markdown
is regression evidence, not authority. Mutation fixtures prove the inventory, semantic, relation,
reference, and visual comparisons are effective.

Migration-only conversion and comparison dependencies execute from their separately declared
locked `uv` group. Before recurring acceptance that group and every migration-only dependency are
removed, `uv.lock` is regenerated from the operative project, and locked/offline consistency plus
the installed-distribution census are re-proved without implicit synchronization.

The archive path is registered before creation under an exclusive OS-held lease. Cleanup is
idempotent for absent, partial, and complete targets and may recover only a proven-stale lease.
Before recurring acceptance, the archive, locator, lease, mappings, renders, diffs, screenshots,
temporary equivalence record, importer, and migration controls are removed. The draft pair is
rewritten/renamed as the present-tense operative pair; draft status, migration/future narrative,
this whole section, temporary-consumer language, and stale links/numbering are removed. Failure to
prove absence prohibits acceptance. `SSM-MIG-01` never appears in the recurring result census.

## Acceptance evidence boundary

The executable registry is the sole operative source of `SSM-AC-01` through `SSM-AC-10`; the
marked table is its deterministic GFM projection of ID, outcome, and evidence fields. Namespaced
callback ownership is checked in both directions so mandatory evidence cannot silently shrink. A
fresh runner emits a complete ephemeral callback receipt bound to one immutable snapshot. The one
repository-global outer-postcondition map, owned by the navigator current-state gate, alone owns
test isolation, post-test revalidation, no-write, final snapshot equality, and criterion promotion.
The receipt additionally binds the exact repository project/lock, Python, `uv`, installed-
distribution, and implementation-source census; it is not persisted and cannot replace an
identified-human approval. Navigator `AC-01` through `AC-20` remain independently mandatory and
are not weakened or repeated here.
