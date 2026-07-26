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
| **SSM-PDF-AC-01 — Authority and package closure** | Each `pdf-evidence-transcription-v1` package has one stored PDF, source manifest, manually maintained transcription XML, generated Markdown view, and only registered assets or convenience derivatives. The PDF governs fidelity; XML alone owns asserted transcription, provenance, stable IDs, and typed metadata. Package, router, and consumer ownership closes bidirectionally. | Bidirectional package/file, router/file, and consumer-dependency/file censuses; missing, duplicate, wrong-role, inferred-authority, undeclared-file, and mixed-owner fixtures. |
| **SSM-PDF-AC-02 — XML item-surface and readable-storage closure** | Each package exposes one addressable typed document root and content items with stable non-positional IDs, closed ordered hierarchy, exact typed content and metadata, provenance, uncertainty, and applicable dependencies/assets. XSD/profile agreement covers every reachable node, scalar, and value model; typed-item digests exclude the XML envelope and formatting. Every XML equals the readable storage law. | Exact document-root, XSD/profile, item/node/field/type/value-model/hierarchy/order/dependency census; parse-serialize byte equality; readable-spelling, whitespace, digest-scope, identity, provenance, missing/wrong-kind/cycle, and resource-limit fixtures. |
| **SSM-PDF-AC-03 — Evidence binding and assurance closure** | Each manifest binds the exact stored PDF path/signature, raw digest, size, evidentiary role, copy status, extraction method, assets, and non-authoritative derivatives. Exact-byte checks and OCR prove neither authenticity nor transcription fidelity, legal correctness, approval, or filing readiness. | PDF name/signature, checksum, size, manifest, copy-status, extraction-method, source-path, asset, derivative, OCR-authority, and false-assurance fixtures. |
| **SSM-PDF-AC-04 — Generated Markdown and coverage closure** | Fresh XML-to-Markdown rendering is byte-identical to the review view. Coverage independently recomputes readable serialization, every item and field, provenance, dependency/asset, manifest raw binding, typed-item digest, origin, and anchor; renderer self-report and stored evidence have no authority. | Cross-process rendering and independent serializer/item/field/provenance/dependency/asset/digest/anchor/region census; missing, extra, duplicate, reordered, stale, self-report, and stored-evidence fixtures. |
| **SSM-PDF-AC-05 — Snapshot-bound handoff, commands, and writes** | Before model construction or writes, each declared edge constructs one handoff from a root-bound retained-byte snapshot after package, parser-control, surface, binding, generated-view, and coverage validation. Controls and handed state are transitively immutable; XML receives the frozen surface/assets and Markdown only review bytes. Reopen, detached tokens, inference, fallback, promotion, and pre-write-state reuse fail. | Exact edge/handoff and validation-read censuses; retained-control, nested-mutation, byte-equality, representation-isolation, direct-read/reopen, conflicting-handoff, detached-token, undeclared-read, fallback, no-authority-write, atomic-rollback/readback, and external-mutation fixtures. |
| **SSM-PDF-AC-06 — Field evolution, audit, and implementation closure** | A transcription-field, storage-law, or typed-digest change coherently updates its XML owner, schema/profile, parser/serializer, renderer, coverage, bindings, consumers, and tests. Exact live closure has no parser-control bypass, second surface builder, mutable handoff, alternate path, untyped extension, consumer semantic field, unused digest mechanism, stored evidence, compatibility path, or residue. | Exact contract/registry/schema/profile/parser/serializer/renderer/surface/consumer/package/test census; storage-law, typed-field, whole-profile, partial-update, control-bypass, handoff-bypass, alternate-path, compatibility, and stored-record fixtures. |
<!-- SSM-PDF-AC-TABLE:END -->

## Acceptance evidence boundary

The domain's data-only registry is the machine-readable source for the six criterion rows. The
marked table is its deterministic projection. The shared verifier checks this domain within one
corpus pass and emits ephemeral domain statuses bound to the supplied snapshot. No callback layer,
stored evidence file, approval record, or detached result substitutes for current execution.
