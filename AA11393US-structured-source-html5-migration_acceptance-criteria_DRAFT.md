# AA11393US — Structured-Source HTML5 Migration: Acceptance Criteria (DRAFT)

> **PROPOSED DEFINITION OF DONE · INTERNAL DRAFT**
>
> This contract is coupled to the
> [`AA11393US-structured-source-html5-migration_technical-description_DRAFT.md`](AA11393US-structured-source-html5-migration_technical-description_DRAFT.md).
> The upstream structured-source criteria and the cutover-updated navigator `AC-01` through
> `AC-20` remain independently mandatory.

## Pass rule

All ten criteria are temporary cutover-readiness criteria. Cutover may proceed only after they, the
exact upstream structured-source result, and the cutover-updated navigator result pass against one
clean immutable candidate snapshot. That readiness pass is not final conformance. Final conformance
exists only after enduring checks are transferred, every SH5 document and control is removed, and
the exact upstream and sole current navigator results pass against the unchanged final snapshot. A
warning, unknown or skipped result, authority promotion, undeclared read, unresolved origin, stale
output, retained old path, or post-test mutation is a failure.

A pass proves machine conformance only. It does not certify human attention, PDF fidelity,
authenticity, legal correctness, counsel approval, filing readiness, or filing authorization.

<!-- SH5-AC-TABLE:START -->
| ID | Required outcome | Required evidence and enforcer |
|---|---|---|
| **SH5-AC-01 — Exact upstream and authority closure** | The build resolves all registered XML, dependencies, endpoints, assets, controls, authority schemes, XML roles, and mandatory computed coverage from one snapshot. Each pre-test or final post-test phase builds one fresh upstream result and index set and reuses it across editions and callbacks; nothing crosses the test boundary. Navigator consumers declare `xml`; navigator-owned XML uses only its exact navigator scheme/role; representation never changes authority. | Same-snapshot phase instrumentation, registry/read census, and stale-result/index-reuse, repeated-pass, missing, wrong-scheme/role/representation, and authority-promotion fixtures. |
| **SH5-AC-02 — Item identity and metadata preservation** | Every consumed item preserves its scheme-declared stable ID, type, hierarchy, order, content, typed metadata, provenance, digest, and dependencies where applicable. DOM locators derive mechanically from item IDs. Unknown fields, position-derived IDs, manual edits to generated XML, and unowned metadata fail. | Schema/item-model comparison and ID, metadata, provenance, digest-locality, DOM-mapping, unknown-field, and generated-edit tests. |
| **SH5-AC-03 — Relation closure** | Every upstream and navigator relation has one semantic owner and exact typed, directional, digest-bound endpoints. All forward/reverse links and excerpts resolve. Copied assertions, duplicate owners, stale or ambiguous targets, inferred links, silent retargeting, and endpoint-driven authority promotion fail. | Relation/endpoint census, HTML link-origin comparison, and duplicate/stale/swap/inference/retarget fixtures. |
| **SH5-AC-04 — Controlled semantic wording** | Only wording carrying declared substantive, provenance, caution/disposition, disclaimer, profile/release/manifest, or security meaning is owned by navigator wording XML; edition specificity alone is insufficient. Each entry has a stable ID, closed usage contexts, and minimally declared typed slots with exact origins and escape classes. Ordinary UI copy is owned by tracked templates or code and requires no wording entry or semantic-origin record. Arbitrary runtime wording, executable templates, raw HTML slots, unsafe bypasses, and content-approval records are absent. | Controlled-wording category and usage validation; parser/digest checks; duplicate-semantic-wording scan; slot/origin/context/injection tests; existing navigator accessibility, security, manifest, and product checks. |
| **SH5-AC-05 — Secure direct consumer** | Production semantic reads pass through one read-only secure XML gateway. Markdown, PDF/OCR text, semantic JSON, persisted adapters, caches, aliases, fallbacks, undeclared files, path escapes, external resources, and unsupported versions cannot reach the model. Navigator commands cannot write any semantic authority. | Gateway read/write log, parser tests, production import/path scan, and forbidden-reader/write/fallback/network fixtures. |
| **SH5-AC-06 — Immutable typed model and origin closure** | The gateway constructs one ephemeral immutable typed model preserving exact content, IDs, metadata, provenance, relations, and declared substantive or security-relevant origins. Renderers use only its typed API. No persisted model, normalization, inference, repair, invented controlled wording, or direct XML traversal by renderers exists. | Model-to-origin comparison, API-boundary checks, mutation tests, and persisted-model/inference/repair/direct-parser fixtures. |
| **SH5-AC-07 — Deterministic and secure HTML5** | Identical locked inputs reproduce exact HTML5 candidate bytes and identical computed, non-stored origin inventories. The inventory covers source/relation semantics, controlled wording and slots, security-sensitive dynamic values, and registered feature-driving fields or derivations; ordinary template/code copy is excluded. Every covered value traces to its scheme-specific authority and XML item, navigator XML, registered control, typed interaction-state field, or closed derivation. Context-specific escaping prevents executable content. The inventory neither replaces nor becomes a product manifest. | Cross-process builds, ephemeral origin comparison, existing manifest checks, and nondeterminism, missing-origin, hostile-value, URL, markup, and script-injection tests. |
| **SH5-AC-08 — Independent product behavior** | The navigator criterion IDs and their user-visible and release outcomes remain and pass independently after obsolete approval mechanics are removed. User-visible behavior changes only through an express current navigator-contract change. | Complete current navigator result binding and content, semantic-DOM, navigation, accessibility, interaction, no-JS, print, security, release, control-residue, and product regression tests. |
| **SH5-AC-09 — Writes and final-snapshot closure** | Validation precedes writes; build, verification, release, and bundle commands never write semantic XML; mutating commands write only declared downstream products and replace files atomically. Tests run in isolation, and the global gate revalidates every current product and the unchanged snapshot without provisioning or environment mutation. | Command/write allowlists, rollback/external-mutation/crash-residue tests, isolated suites, environment checks, post-test revalidation, and final snapshot comparison. |
| **SH5-AC-10 — Transfer and deletion readiness** | The candidate tree contains one semantic XML ingestion path and one typed model; old readers/stores, adapters, compatibility, fallbacks, caches, migration helpers, duplicate assertions, stale artifacts, removed-path helpers/tests, and obsolete relation/content approval mechanics are absent. Every enduring SH5 check already has exactly one current navigator criterion/callback owner. The exact SH5 deletion set is closed, and a navigator-owned final-closure check requires its actual absence from the final tree. No operative HTML5 pair or independent HTML5-input result is defined. | Current navigator ownership/traceability comparison, exact SH5 deletion census, final-closure negative fixture, current product regeneration, and temporary readiness result. |
<!-- SH5-AC-TABLE:END -->

## Acceptance evidence boundary

While present, this table and any temporary SH5 mapping control cutover readiness only. They do not
create a permanent acceptance registry, bind a release, or survive the cutover. Enduring checks are
assigned directly to exactly one owner in the existing navigator acceptance registry; upstream
checks remain structured-source-owned and are result-bound rather than copied.

The final global runner emits only the exact upstream and single current navigator results. No SH5
result, approval record, baseline archive, migration receipt, or detached package substitutes for
the repository checkout and current execution. Until the transfer, deletion, and final execution
complete, these criteria claim no current HTML5-migration conformance.
