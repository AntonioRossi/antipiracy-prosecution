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
| **SSM-PDF-AC-01 — Authority and package closure** | Every PDF-transcription package declares `pdf-evidence-transcription-v1`, one stored PDF, one source manifest, one manually maintained transcription XML, one generated Markdown view, and only its registered assets or convenience derivatives. The PDF governs source fidelity; XML owns the asserted transcription, provenance, stable IDs, and permitted metadata. Package, router, and consumer-dependency ownership closes bidirectionally. | Bidirectional package/file, router/file, and consumer-dependency/file censuses; missing, duplicate, wrong-role, inferred-authority, undeclared-file, and mixed-owner fixtures. |
| **SSM-PDF-AC-02 — XML item-surface closure** | Every addressable transcription item exposes one stable non-positional ID, closed type, hierarchy/order, asserted content, typed metadata, PDF provenance, applicable uncertainty, dependencies/assets, and an item-local semantic digest. The exclusive profile controls field, identity, numbering, provenance, dependency, and digest laws; unsafe, unknown, duplicate, cyclic, or stale constructs fail closed. | Exact XSD/profile and item/field/hierarchy/order/dependency census; lexical, digest, provenance, uncertainty, insertion/deletion/reorder, duplicate-ID, number/identity, unknown-field, cycle, and resource-limit fixtures. |
| **SSM-PDF-AC-03 — Evidence binding and assurance closure** | Each manifest binds the exact stored PDF path and format signature, raw digest, size, evidentiary role, copy status, extraction method, assets, and non-authoritative derivatives. Format checks and OCR prove neither authenticity nor fidelity, and no machine result claims legal correctness, approval, or filing readiness. | PDF name/signature, checksum, size, manifest, copy-status, extraction-method, source-path, asset, derivative, OCR-authority, and false-assurance fixtures. |
| **SSM-PDF-AC-04 — Generated Markdown and coverage closure** | Fresh XML-to-Markdown rendering is byte-identical to the registered review view. Coverage is independently recomputed from XML for every item and applicable field, provenance, dependency/asset, digest, origin, and anchor; renderer self-report and stored coverage artifacts confer no authority. | Cross-process rendering and byte comparison; independent field/envelope/origin/anchor/region and item/provenance/dependency/asset censuses; missing, extra, duplicate, reordered, and stale fixtures. |
| **SSM-PDF-AC-05 — Snapshot-bound handoff, commands, and writes** | Before model construction or writes, the package, surface, bindings, digests, view, and coverage pass over a root-bound snapshot whose retained bytes equal every handoff path. XML receives the frozen surface/assets; Markdown receives only review bytes. Reopen, detached tokens, inference, fallback, authority promotion, and reuse of pre-write state fail. | Declared-edge resolver and exact read log; pre-consumption, snapshot mutation, byte-equality, representation-isolation, reopen, detached-token, undeclared-read, fallback, no-authority-write, atomic rollback, readback, and external-mutation fixtures. |
| **SSM-PDF-AC-06 — Field evolution, audit, and implementation closure** | A transcription-field change coherently updates its XML owner, exclusive schema/profile, parser/renderer, digest rule, coverage, bindings, consumers, and focused tests. The exact current contract, registry, implementation-path, package, and view census contains no alternate path, untyped extension, consumer semantic field, approval/receipt/coverage store, compatibility path, or residue. | Exact contract/registry/schema/profile/source/converter/consumer/test/path census; whole-profile and partial-field updates, unknown/extension/untyped/renderer-only fields, retired paths, and stored-record fixtures in one aggregate pass. |
<!-- SSM-PDF-AC-TABLE:END -->

## Acceptance evidence boundary

The domain's data-only registry is the machine-readable source for the six criterion rows. The
marked table is its deterministic projection. The shared verifier checks this domain within one
corpus pass and emits ephemeral domain statuses bound to the supplied snapshot. No callback layer,
stored evidence file, approval record, or detached result substitutes for current execution.
