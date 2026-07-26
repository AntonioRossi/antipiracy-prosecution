# AA11393US — Authored Relation XML Acceptance Criteria

> **OPERATIVE INTERNAL CONTROL · NOT FOR FILING**
>
> This is the current acceptance contract coupled to
> [`AA11393US-structured-source-authored-relations_technical-description.md`](AA11393US-structured-source-authored-relations_technical-description.md).

## Pass rule

Conformance exists only when all six criteria pass in the one aggregate structured-source
verification against the same immutable repository snapshot. A warning, unknown result, inferred
authority, stale generated view, unresolved or role-invalid endpoint, duplicate semantic owner,
undeclared read, or assurance claim beyond the machine evidence is a failure.

A pass proves only the stated machine properties. It does not certify substantive or legal
correctness, counsel approval, filing readiness, or filing authorization.

<!-- SSM-REL-AC-TABLE:START -->
| ID | Required outcome | Required evidence and enforcer |
|---|---|---|
| **SSM-REL-AC-01 — Authority, package, and ownership closure** | Every authored-relation package declares `authored-relations-v1`, one authoritative relation XML file, and one generated Markdown view. Relation XML is the sole owner of each applicant-authored assertion, its stable identity, semantic owner, type, direction, ordered fields, and endpoints. | Bidirectional package/file/relation census and missing, duplicate, wrong-role, inferred-authority, copied-assertion, undeclared-file, and mixed-owner fixtures. |
| **SSM-REL-AC-02 — XML identity, format, and assertion closure** | Every relation XML uses the current schema/profile, UTF-8 XML 1.0 and NFC, secure parsing, stable non-positional identities, one semantic owner, closed types, directions and fields, raw and semantic digests, and no self-bound relation digest, arbitrary extension, or competing owner. | Current XSD/profile validation; secure-parser, NFC, digest, stable-ID, semantic-owner, type, direction, field-vocabulary, unknown-field, duplicate-ID, self-binding, and resource-limit tests. |
| **SSM-REL-AC-03 — Endpoint role and reference closure** | Every endpoint binds an exact registered `(documentId, fragmentId, fragmentContentDigest)` target and uses a permitted profile role. Missing, duplicate within one assertion, swapped-role, stale, ambiguous, undeclared, inferred, silently retargeted, or authority-promoting endpoints fail. | Relation census, profile-role checks, endpoint resolver, generated-view comparison, and missing, duplicate, stale, ambiguous, swap, retarget, and authority-promotion fixtures. |
| **SSM-REL-AC-04 — Generated Markdown and coverage closure** | Fresh relation-XML-to-Markdown rendering is byte-identical to the registered review view and exposes authority, ownership, fields, stable anchors, resolved excerpts, and forward and reverse endpoint links. Computed coverage includes every assertion, field, and endpoint; no package-level coverage artifact is stored. | Fresh cross-process rendering, byte comparison, assertion/field/endpoint/anchor/link census, and added, dropped, reordered, stale-excerpt, or second-owner projection fixtures. |
| **SSM-REL-AC-05 — Consumer handoff, commands, and writes** | A declared consumer receives the registered representation, authority scheme, authoritative role, typed assertions, fields, and resolved endpoints without fallback or authority promotion. The closed command surface reads relation authority and endpoint bytes only and atomically replaces only the generated Markdown owned by the targeted package or derived control tables. | Declared-edge resolver and read log; command/write allowlists; target-scope, no-authority-write, validation-before-write, atomic-replacement, rollback, external-mutation, endpoint-dependency, and representation-fallback tests. |
| **SSM-REL-AC-06 — Audit and active implementation closure** | The current authored-relations contract, registry slice, schema/profile, resolver, renderer, tests, packages, endpoints, and generated views agree exactly in one immutable repository snapshot. No retired format, alternate relation owner or reader, approval record, stored receipt, coverage store, migration reader, compatibility path, or domain residue is operative. | Domain package, schema, profile, resolver, renderer, source/import, command, test, and contract/registry/table census within the one immutable-snapshot aggregate verification pass. |
<!-- SSM-REL-AC-TABLE:END -->

## Acceptance evidence boundary

The domain's data-only registry is the machine-readable source for the six criterion rows. The
marked table is its deterministic projection. The shared verifier checks this domain within one
corpus pass and emits ephemeral domain statuses bound to the supplied snapshot. No callback layer,
stored evidence file, approval record, or detached result substitutes for current execution.
