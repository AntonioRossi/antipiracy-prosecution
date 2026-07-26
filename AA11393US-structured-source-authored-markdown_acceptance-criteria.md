# AA11393US — Authored Markdown to XML Acceptance Criteria

> **OPERATIVE INTERNAL CONTROL · NOT FOR FILING**
>
> This is the current acceptance contract coupled to
> [`AA11393US-structured-source-authored-markdown_technical-description.md`](AA11393US-structured-source-authored-markdown_technical-description.md).

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
| **SSM-MD-AC-02 — Markdown profile and XML closure** | Authoritative Markdown uses the one stable-anchor syntax and closed pinned GFM subset. Generated XML uses the current schema/profile, UTF-8 XML 1.0 and NFC, secure parsing, stable non-positional identities, closed typed metadata, raw and semantic digests, and no manually maintained or unclassified region. | Pinned GFM/profile and current XSD validation; secure-parser, NFC, raw/semantic digest, stable-ID, metadata-ownership, unknown-field, unsupported-construct, and resource-limit tests. |
| **SSM-MD-AC-03 — Conversion and semantic back-render closure** | Fresh Markdown-to-XML conversion preserves every supported content-bearing node, identity, link, claim, table cell, advisory, heading, metadata field, hierarchy, and order. The non-stored XML back-render preserves the ordered Pandoc AST after only profile-listed presentational normalizations, and registered XML equals regeneration. | Ordered Pandoc-AST comparison after the exact normalization allowlist; add, drop, reorder, hidden-content, link, claim, table, advisory, heading, metadata, and manual-generated-edit fixtures. |
| **SSM-MD-AC-04 — Determinism and coverage closure** | Fresh generated XML is byte-identical across processes. Computed coverage maps every authoritative Markdown item to its XML item and semantic back-render; no back-render or package-level coverage artifact is stored. | Fresh cross-process conversion, byte comparison, item/XML/back-render census, and missing, stale, lossy, duplicate-ID, second-Markdown-owner, or persisted-back-render fixtures. |
| **SSM-MD-AC-05 — Consumer handoff, commands, and writes** | A declared consumer receives the registered representation, authority scheme, representation role, typed items, metadata, dependencies, and digests without fallback or authority promotion. The closed command surface reads Markdown authority bytes only and atomically replaces only the generated XML owned by the targeted package or derived control tables. | Declared-edge resolver and read log; command/write allowlists; target-scope, no-authority-write, validation-before-write, atomic-replacement, rollback, external-mutation, field-loss, and representation-fallback tests. |
| **SSM-MD-AC-06 — Audit and active implementation closure** | The current authored-Markdown contract, registry slice, schema/profile, converter, tests, packages, and generated XML agree exactly in one immutable repository snapshot. No retired format, alternate converter, editable generated owner, approval record, stored receipt, coverage store, migration reader, compatibility path, or domain residue is operative. | Domain package, schema, profile, converter, source/import, command, test, and contract/registry/table census within the one immutable-snapshot aggregate verification pass. |
<!-- SSM-MD-AC-TABLE:END -->

## Acceptance evidence boundary

The domain's data-only registry is the machine-readable source for the six criterion rows. The
marked table is its deterministic projection. The shared verifier checks this domain within one
corpus pass and emits ephemeral domain statuses bound to the supplied snapshot. No callback layer,
stored evidence file, approval record, or detached result substitutes for current execution.
