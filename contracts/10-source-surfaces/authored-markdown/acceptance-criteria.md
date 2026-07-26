# AA11393US — Authored Markdown to XML Acceptance Criteria

> **OPERATIVE INTERNAL CONTROL · NOT FOR FILING**
>
> This is the current acceptance contract coupled to
> [`technical description`](technical-description.md).

## Pass rule

Conformance exists only when all six criteria pass in the one aggregate structured-source
verification against the same immutable repository snapshot. A warning, unknown result, inferred
authority, stale generated XML, unsupported or lossy conversion, undeclared read, stored
back-render, or assurance claim beyond the machine evidence is a failure.

A pass proves only the stated machine properties. It does not certify human attention, legal
correctness, counsel approval, filing readiness, or filing authorization.

<!-- SSM-MD-AC-TABLE:START -->
| ID | Required outcome | Required evidence and enforcer |
|---|---|---|
| **SSM-MD-AC-01 — Authority and package closure** | Each `authored-markdown-v1` package has one authoritative Markdown and one generated XML. Markdown alone owns adopted content, stable IDs, and substantive metadata; XML contains only preserved semantics and classified envelope fields. Package, router, and consumer ownership closes bidirectionally. | Bidirectional package/file, router/file, and consumer-dependency/file censuses; missing, duplicate, wrong-role, second-owner, undeclared-file, and mixed-owner fixtures. |
| **SSM-MD-AC-02 — Authored item-surface closure** | Every item has one Markdown-owned stable ID, closed type, hierarchy/order, content, metadata, authority binding, and applicable closed typed-record digest. The exclusive profile controls Pandoc capability, anchors, links, normalization, identity, and numbering; XML-only, unknown, or unsafe semantics fail. | Exact GFM/profile, XSD, and item/field/hierarchy/order census; typed-digest, binding, insertion/deletion/reorder, duplicate-ID, number/identity, ownership, unknown-field, unsupported-construct, and resource-limit fixtures. |
| **SSM-MD-AC-03 — Conversion, readable XML, and back-render closure** | Fresh conversion preserves the complete supported ordered Pandoc AST and emits XML equal to the readable storage law. The non-stored back-render preserves that AST after only listed normalizations; authored links remain content rather than inferred dependencies, and registered XML equals regeneration. | Exact normalized AST and parse-serialize byte comparison; minified, indent, tab, line-ending, namespace, attribute, empty-element, text-whitespace, add/drop/reorder, link/dependency, and manual-generated-edit fixtures. |
| **SSM-MD-AC-04 — Determinism and coverage closure** | Fresh readable XML is byte-identical across processes. Coverage independently recomputes every item/field, semantic path, authority binding, typed-item digest, back-render node, dependency, hierarchy, and order. Storage formatting cannot change semantic identity; converter self-report and stored evidence have no authority. | Cross-process conversion and independent item/field/XML/back-render/binding/dependency census; digest-invariance, missing, extra, duplicate, reordered, lossy, stale, self-report, second-owner, and stored-evidence fixtures. |
| **SSM-MD-AC-05 — Snapshot-bound handoff, commands, and writes** | Before model construction or writes, conversion, typed surface, authority binding, typed-item digests, back-render, and coverage pass over a root-bound retained-byte snapshot. XML receives frozen generated state; Markdown receives only authority bytes. Reopen, detached tokens, inference, fallback, promotion, and pre-write-state reuse fail. | Declared-edge resolver and exact read log; pre-consumption, snapshot-mutation, byte-equality, representation-isolation, reopen, detached-token, undeclared-read, field-loss, fallback, no-authority-write, atomic-rollback, readback, and external-mutation fixtures. |
| **SSM-MD-AC-06 — Field evolution, audit, and implementation closure** | An authored-field, storage-law, or typed-digest change coherently updates its Markdown owner, schema/profile, converter/serializer, back-render, coverage, consumers, and tests. Exact live closure has no alternate converter, generated owner, untyped extension, consumer semantic field, unused digest mechanism, stored evidence, compatibility path, or residue. | Exact contract/registry/schema/profile/converter/serializer/back-render/surface/consumer/package/test census; storage-law, typed-field, whole-profile, partial-update, alternate-path, compatibility, and stored-record fixtures. |
<!-- SSM-MD-AC-TABLE:END -->

## Acceptance evidence boundary

The domain's data-only registry is the machine-readable source for the six criterion rows. The
marked table is its deterministic projection. The shared verifier checks this domain within one
corpus pass and emits ephemeral domain statuses bound to the supplied snapshot. No callback layer,
stored evidence file, approval record, or detached result substitutes for current execution.
