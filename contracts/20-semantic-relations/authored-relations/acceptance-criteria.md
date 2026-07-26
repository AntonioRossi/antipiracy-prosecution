# AA11393US — Authored Relation XML Acceptance Criteria

> **OPERATIVE INTERNAL CONTROL · NOT FOR FILING**
>
> This is the current acceptance contract coupled to
> [`technical description`](technical-description.md).

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
| **SSM-REL-AC-02 — Relation item-surface closure** | Every assertion exposes one stable non-positional relation ID, one semantic owner, closed type and direction, authored relation/field/endpoint order, profile-enumerated typed fields, exact role-bearing endpoints, and a relation semantic digest. Authored numbers, mechanical ordinals, display labels, and stable identities remain distinct; self-binding, arbitrary extensions, untyped fields, unknown semantics, or competing owners fail closed. | Current XSD/profile validation; exact assertion/field/endpoint/order census; secure-parser, NFC, digest, insertion, deletion, reorder, duplicate-ID, number/identity-confusion, semantic-owner, type, direction, field-vocabulary, unknown-field, self-binding, and resource-limit tests. |
| **SSM-REL-AC-03 — Endpoint role and reference closure** | Every endpoint binds an exact registered `(documentId, fragmentId, fragmentContentDigest)` target and uses a permitted profile role. Missing, duplicate within one assertion, swapped-role, stale, ambiguous, undeclared, inferred, silently retargeted, relation-to-relation, or authority-promoting endpoints fail. | Relation census, profile-role checks, endpoint resolver, generated-view comparison, and missing, duplicate, stale, ambiguous, swap, undeclared-target, retarget, and authority-promotion fixtures. |
| **SSM-REL-AC-04 — Generated Markdown and coverage closure** | Fresh relation-XML-to-Markdown rendering is byte-identical to the registered review view and exposes authority, ownership, ordered fields, stable anchors, resolved excerpts, and forward and reverse endpoint links. Computed coverage includes every assertion, field, endpoint, excerpt, and link; no package-level coverage artifact is stored. | Fresh cross-process rendering, byte comparison, assertion/field/endpoint/anchor/excerpt/link census, and added, dropped, reordered, stale-excerpt, or second-owner projection fixtures. |
| **SSM-REL-AC-05 — Snapshot-bound handoff, commands, and writes** | Before consumer model construction or output writes, the relation schema/profile, complete assertion surface, ownership, roles, directions, endpoint targets/digests, generated view, and coverage pass over one immutable snapshot; the consumer receives those same bytes and may only look up assertions, traverse authored order, select declared fields, and resolve exact endpoints. No reopen, detached pass token, inference, repair, fallback, or authority promotion is permitted. Commands atomically replace only package-owned generated Markdown or derived controls. | Declared-edge resolver and exact read log; pre-consumption failure, snapshot mutation, reopen, detached-token, inferred-relation, target-repair, undeclared-read, representation-fallback, no-authority-write, validation-before-write, atomic-replacement, rollback, and external-mutation tests. |
| **SSM-REL-AC-06 — Field evolution, audit, and implementation closure** | Adding or changing a relation type, direction, role, field, or endpoint property coherently updates its relation XML owner, schema/profile, parser/resolver, digest rule, projection, coverage, affected content-field contract, declared consumers, and focused tests. The current contract, registry slice, implementation, packages, endpoints, and generated views agree exactly in one immutable snapshot; no alternate owner/reader, untyped extension, consumer-specific relation, approval record, stored receipt, coverage store, migration/compatibility path, or domain residue is operative. | Exact domain contract/registry/schema/profile/source/resolver/renderer/consumer/test census; partial-field-update, unknown-relation, extension-map, untyped-field, copied or renderer-only semantics, retired-path, and stored-record fixtures within the one aggregate pass. |
<!-- SSM-REL-AC-TABLE:END -->

## Acceptance evidence boundary

The domain's data-only registry is the machine-readable source for the six criterion rows. The
marked table is its deterministic projection. The shared verifier checks this domain within one
corpus pass and emits ephemeral domain statuses bound to the supplied snapshot. No callback layer,
stored evidence file, approval record, or detached result substitutes for current execution.
