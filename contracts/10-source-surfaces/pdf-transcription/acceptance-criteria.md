# AA11393US — PDF Evidence Transcription Acceptance Criteria

> **OPERATIVE INTERNAL CONTROL · NOT FOR FILING**
>
> This is the current acceptance contract coupled to
> [`technical description`](technical-description.md).

## Pass rule

Conformance exists only when all six criteria pass in the one aggregate structured-source
verification against the same immutable repository snapshot. A warning, unknown result, inferred
authority, stale generated view, unresolved provenance, unsupported format, undeclared read, or
assurance claim beyond the machine evidence is a failure.

A pass proves only the stated machine properties. It does not certify PDF authenticity,
transcription fidelity, human attention, legal correctness, counsel approval, filing readiness, or
filing authorization.

<!-- SSM-PDF-AC-TABLE:START -->
| ID | Required outcome | Required evidence and enforcer |
|---|---|---|
| **SSM-PDF-AC-01 — Authority and package closure** | Every PDF-transcription package declares `pdf-evidence-transcription-v1`, one stored PDF, one source manifest, one manually maintained transcription XML, one generated Markdown view, and only its registered assets or convenience derivatives. The PDF governs source fidelity; XML owns the asserted transcription, provenance, stable IDs, and permitted metadata. | Bidirectional package/file census and missing, duplicate, wrong-role, inferred-authority, undeclared-file, and mixed-owner fixtures. |
| **SSM-PDF-AC-02 — XML item-surface closure** | Every addressable transcription item exposes one stable non-positional ID, closed type, typed hierarchy and document order, exact asserted content, closed typed metadata, required page/region provenance, applicable uncertainty, registered dependencies/assets, and an item-local semantic digest. Source-visible numbers, mechanical ordinals, display labels, and stable identities remain distinct; unsafe, unknown, mixed-owner, duplicate, or stale constructs fail closed. | Current XSD/profile validation; exact item/field/hierarchy/order census; secure-parser, NFC, digest, provenance, uncertainty-field, insertion, deletion, reorder, duplicate-ID, number/identity-confusion, unknown-field, and resource-limit tests. |
| **SSM-PDF-AC-03 — Evidence binding and assurance closure** | Each manifest binds the exact stored PDF, evidentiary role, copy status, extraction method, assets, and non-authoritative convenience derivatives. OCR remains an inspection aid, and no machine result claims to prove transcription fidelity, source authenticity, legal correctness, approval, or filing readiness. | PDF checksum, byte-size, manifest, copy-status, extraction-method, source-path, asset, convenience-derivative, OCR-authority, and false-fidelity-result tests. |
| **SSM-PDF-AC-04 — Generated Markdown and coverage closure** | Fresh XML-to-Markdown rendering is byte-identical to the registered review view. Computed coverage maps every transcribed item and applicable field to exact PDF provenance, registered dependencies/assets, and a stable generated Markdown anchor; no package-level coverage artifact is stored. | Fresh cross-process rendering, byte comparison, item/provenance/anchor/dependency/asset census, and missing, stale, added, dropped, or reordered projection fixtures. |
| **SSM-PDF-AC-05 — Snapshot-bound handoff, commands, and writes** | Before consumer model construction or output writes, the package, complete item surface, provenance, dependencies/assets, digests, generated view, and coverage pass over one immutable snapshot; the consumer receives those same bytes and may only look up items, traverse declared hierarchy/order, select declared fields, and resolve registered dependencies. No reopen, detached pass token, inference, fallback, or authority promotion is permitted. Commands atomically replace only package-owned generated Markdown or derived controls. | Declared-edge resolver and exact read log; pre-consumption failure, snapshot mutation, reopen, detached-token, inference, undeclared-read, representation-fallback, no-authority-write, validation-before-write, atomic-replacement, rollback, and external-mutation tests. |
| **SSM-PDF-AC-06 — Field evolution, audit, and implementation closure** | Adding or changing a transcription field coherently updates its XML owner, schema/profile, parser/renderer, digest rule, coverage, affected bindings, declared consumers, and focused tests. The current contract, registry slice, implementation, packages, and generated views agree exactly in one immutable snapshot; no alternate path, untyped extension, consumer-specific semantic field, approval record, stored receipt, coverage store, migration/compatibility path, or domain residue is operative. | Exact domain contract/registry/schema/profile/source/converter/consumer/test census; partial-field-update, unknown-field, extension-map, untyped-metadata, renderer-only-semantics, retired-path, and stored-record fixtures within the one aggregate pass. |
<!-- SSM-PDF-AC-TABLE:END -->

## Acceptance evidence boundary

The domain's data-only registry is the machine-readable source for the six criterion rows. The
marked table is its deterministic projection. The shared verifier checks this domain within one
corpus pass and emits ephemeral domain statuses bound to the supplied snapshot. No callback layer,
stored evidence file, approval record, or detached result substitutes for current execution.
