# AA11393US — PDF Evidence Transcription Acceptance Criteria

> **OPERATIVE INTERNAL CONTROL · NOT FOR FILING**
>
> This is the current acceptance contract coupled to
> [`technical description`](technical-description.md).

## Domain pass rule

All six executable outcomes must pass within the shared
[aggregate validation boundary](../../README.md#aggregate-validation-boundary) on the retained
worktree capture. Each registry row names its independent enforcer. A warning, unknown result, inference,
self-report, stored result, detached token, prior run, stale view, unresolved provenance,
unsupported format, or undeclared read cannot satisfy a criterion.

<!-- SSM-PDF-AC-TABLE:START -->
| ID | Executable technical outcome | Independent enforcer |
|---|---|---|
| **SSM-PDF-AC-01 — Authority and package closure** | Each `pdf-evidence-transcription-v1` package has one stored PDF, source manifest, manually maintained transcription XML, generated Markdown view, and only registered assets or convenience derivatives. The PDF governs fidelity; XML alone owns asserted transcription, provenance, stable IDs, and typed metadata. Package, router, and consumer ownership closes bidirectionally. | structured_source.verify.VerificationContext._control_closure; structured_source.tests.test_registry |
| **SSM-PDF-AC-02 — XML item-surface and readable-storage closure** | Each package exposes one stable typed document root and closed ordered content items with exact profile-owned content, metadata, provenance, uncertainty, dependencies, and assets. The sole profile owns the grammar; `content.xsd` is its deterministic projection, independent invariants enforce identity, hierarchy, order, cardinality, and typed records, and every XML equals readable storage. | structured_source.parser.parse_artifact; structured_source.tests.test_xml_contract |
| **SSM-PDF-AC-03 — Evidence binding and human-review boundary** | Each manifest binds the exact stored PDF path/signature, raw digest, size, evidentiary role, copy status, extraction method, assets, and non-authoritative derivatives. Exact-byte checks and OCR prove neither authenticity nor transcription fidelity, legal correctness, approval, or filing readiness. Authority content and generated evidence text are content; parsed code, executable controls, and only machine-addressed operative-document structures undergo retired-implementation checks. | structured_source.verify.VerificationContext._control_closure; structured_source.tests.test_pdf_transcription |
| **SSM-PDF-AC-04 — Generated Markdown and coverage closure** | Fresh XML-to-Markdown rendering is byte-identical to the review view. Independent coverage recomputes every item, field, binding, digest, and line region; proves document/top-level anchor order and each descendant anchor's containment in its top-level owner; and rejects renderer self-report or stored evidence. | structured_source.render.render_content; structured_source.tests.test_pdf_transcription |
| **SSM-PDF-AC-05 — Worktree-capture-bound handoff and writes** | Each edge receives one retained-capture-bound handoff after full package and coverage validation. Lookup and traversal require explicit exact IDs; only a resolved leaf has no children. Regeneration prevalidates the complete candidate, atomically publishes, exact-reads every output, freshly loads replacement controls, and rolls back on failure. Reopen, inference, fallback, detached state, and prior-state reuse fail. | structured_source.verify.VerificationContext.read_for_consumer; structured_source.tests.test_pdf_transcription |
| **SSM-PDF-AC-06 — Field evolution and implementation closure** | Every field or grammar change coherently updates all affected owners, the contract pair, registries, controls, implementation, coverage, consumers, generated state, and tests. Retained-capture-wide closure exactly matches all domain/shared code, schemas, launchers, registered tests, vectors, generated representations, and handoffs; missing, extra, alternate, inactive, bypass, compatibility, stored-evidence, or orphaned states fail. | structured_source.verify.VerificationContext._control_closure; structured_source.tests.test_acceptance |
<!-- SSM-PDF-AC-TABLE:END -->

## Registry and execution boundary

The domain's data-only registry is the machine-readable source for the six criterion rows. The
marked table is its deterministic projection. The shared validator checks this domain within the
current retained capture and emits only ephemeral technical status. No callback, self-report,
stored result, approval record, detached token, or prior run substitutes for current execution.
