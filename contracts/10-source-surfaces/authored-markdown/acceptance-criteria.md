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
| **SSM-MD-AC-01 — Authority and package closure** | Every authored-Markdown package declares `authored-markdown-v1`, one authoritative Markdown file, and one generated XML file. Markdown is the sole owner of adopted content, stable item identities, and substantive item metadata; generated XML contains only preserved authored semantics and classified mechanical envelope fields. | Bidirectional package/file census and missing, duplicate, wrong-role, inferred-authority, second-owner, undeclared-file, and mixed-owner fixtures. |
| **SSM-MD-AC-02 — Authored item-surface closure** | Every addressable authored item exposes one Markdown-owned stable ID, closed type, exact hierarchy and source order, exact supported content, closed typed metadata, applicable dependencies, authority binding, and an item-local semantic digest. Source-owned numbers, mechanical ordinals, display labels, and stable identities remain distinct; generated XML has no manually maintained, unclassified, or substantive XML-only field. | Pinned GFM/profile and current XSD validation; exact item/field/hierarchy/order census; secure-parser, NFC, digest, authority-binding, insertion, deletion, reorder, duplicate-ID, number/identity-confusion, metadata-ownership, unknown-field, unsupported-construct, and resource-limit tests. |
| **SSM-MD-AC-03 — Conversion and semantic back-render closure** | Fresh Markdown-to-XML conversion preserves every supported content-bearing node, identity, source-owned number, link, claim, table cell, advisory, heading, metadata field, dependency, hierarchy, and order. The non-stored XML back-render preserves the ordered Pandoc AST after only profile-listed presentational normalizations, and registered XML equals regeneration. | Ordered Pandoc-AST comparison after the exact normalization allowlist; add, drop, reorder, hidden-content, link, claim, table, advisory, heading, metadata, dependency, and manual-generated-edit fixtures. |
| **SSM-MD-AC-04 — Determinism and coverage closure** | Fresh generated XML is byte-identical across processes. Computed coverage maps every authoritative Markdown item and applicable field to its typed XML item, digest, dependencies, and semantic back-render node; no back-render or package-level coverage artifact is stored. | Fresh cross-process conversion, byte comparison, item/field/XML/back-render/dependency census, and missing, stale, lossy, duplicate-ID, second-Markdown-owner, or persisted-back-render fixtures. |
| **SSM-MD-AC-05 — Snapshot-bound handoff, commands, and writes** | Before consumer model construction or output writes, the Markdown profile, conversion, complete item surface, authority binding, dependencies, digests, generated XML, semantic back-render, and coverage pass over one immutable snapshot; the consumer receives those same bytes and may only look up items, traverse declared hierarchy/order, select declared fields, and resolve registered dependencies. No reopen, detached pass token, inference, fallback, or authority promotion is permitted. Commands atomically replace only package-owned generated XML or derived controls. | Declared-edge resolver and exact read log; pre-consumption failure, snapshot mutation, reopen, detached-token, inference, undeclared-read, field-loss, representation-fallback, no-authority-write, validation-before-write, atomic-replacement, rollback, and external-mutation tests. |
| **SSM-MD-AC-06 — Field evolution, audit, and implementation closure** | Adding or changing an authored field coherently updates its Markdown owner, schema/profile, converter/back-render, digest rule, coverage, affected relations/dependencies, declared consumers, and focused tests. The current contract, registry slice, implementation, packages, and generated XML agree exactly in one immutable snapshot; no alternate converter, editable generated owner, untyped extension, consumer-specific semantic field, approval record, stored receipt, coverage store, migration/compatibility path, or domain residue is operative. | Exact domain contract/registry/schema/profile/source/converter/consumer/test census; partial-field-update, XML-only-field, unknown-field, extension-map, untyped-metadata, converter/renderer-only-semantics, retired-path, and stored-record fixtures within the one aggregate pass. |
<!-- SSM-MD-AC-TABLE:END -->

## Acceptance evidence boundary

The domain's data-only registry is the machine-readable source for the six criterion rows. The
marked table is its deterministic projection. The shared verifier checks this domain within one
corpus pass and emits ephemeral domain statuses bound to the supplied snapshot. No callback layer,
stored evidence file, approval record, or detached result substitutes for current execution.
