# AA11393US — PDF Evidence Transcription Acceptance Criteria

> **OPERATIVE INTERNAL CONTROL · NOT FOR FILING**
>
> This is the current acceptance contract coupled to
> [`AA11393US-structured-source-pdf-transcription_technical-description.md`](AA11393US-structured-source-pdf-transcription_technical-description.md).

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
| **SSM-PDF-AC-02 — XML identity, format, and metadata closure** | Every transcription XML uses the current schema/profile, UTF-8 XML 1.0 and NFC, secure parsing, stable non-positional identities, closed metadata, raw and semantic digests, page/region provenance, and any declared uncertainty. Unsafe, unknown, mixed-owner, duplicate, or stale constructs fail closed. | Current XSD/profile validation; secure-parser, NFC, digest, identity, provenance-structure, uncertainty-field, unknown-field, and resource-limit tests. |
| **SSM-PDF-AC-03 — Evidence binding and assurance closure** | Each manifest binds the exact stored PDF, evidentiary role, copy status, extraction method, assets, and non-authoritative convenience derivatives. OCR remains an inspection aid, and no machine result claims to prove transcription fidelity, source authenticity, legal correctness, approval, or filing readiness. | PDF checksum, byte-size, manifest, copy-status, extraction-method, source-path, asset, convenience-derivative, OCR-authority, and false-fidelity-result tests. |
| **SSM-PDF-AC-04 — Generated Markdown and coverage closure** | Fresh XML-to-Markdown rendering is byte-identical to the registered review view. Computed coverage maps every transcribed content item to exact PDF provenance and a stable generated Markdown anchor; no package-level coverage artifact is stored. | Fresh cross-process rendering, byte comparison, item/provenance/anchor census, and missing, stale, added, dropped, or reordered projection fixtures. |
| **SSM-PDF-AC-05 — Consumer handoff, commands, and writes** | A declared consumer receives the registered representation, authority scheme, representation role, typed items, metadata, provenance, and dependencies without fallback or authority promotion. The closed command surface reads authority bytes only and atomically replaces only the generated Markdown owned by the targeted package or derived control tables. | Declared-edge resolver and read log; command/write allowlists; target-scope, no-authority-write, validation-before-write, atomic-replacement, rollback, external-mutation, and representation-fallback tests. |
| **SSM-PDF-AC-06 — Audit and active implementation closure** | The current PDF-transcription contract, registry slice, schema/profile, implementation, tests, packages, and generated views agree exactly in one immutable repository snapshot. No retired format, alternate transcription path, approval record, stored receipt, coverage store, migration reader, compatibility path, or domain residue is operative. | Domain package, schema, profile, converter, source/import, command, test, and contract/registry/table census within the one immutable-snapshot aggregate verification pass. |
<!-- SSM-PDF-AC-TABLE:END -->

## Acceptance evidence boundary

The domain's data-only registry is the machine-readable source for the six criterion rows. The
marked table is its deterministic projection. The shared verifier checks this domain within one
corpus pass and emits ephemeral domain statuses bound to the supplied snapshot. No callback layer,
stored evidence file, approval record, or detached result substitutes for current execution.
