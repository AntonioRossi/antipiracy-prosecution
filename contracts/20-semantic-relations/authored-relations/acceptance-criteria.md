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
| **SSM-REL-AC-01 — Authority, package, and ownership closure** | Each `authored-relations-v1` package has one authoritative relation XML and one generated Markdown review view. XML alone owns each profiled assertion and field. Existing package/file/router/consumer declarations close exactly; endpoints do not authorize reads and dependencies do not create semantics. | Exact registry, package/file, router, consumer-edge, dependency, relation-owner, and endpoint censuses; missing, duplicate, mixed-owner, undeclared, and endpoint/dependency-confusion fixtures. |
| **SSM-REL-AC-02 — Relation surface and readable-storage closure** | Each assertion has one stable non-positional ID, semantic owner, profiled type/direction, authored field/endpoint order, and closed typed content through readable XML. Relation XML has no self or formatting-derived digest. Minified, aliased, extended, untyped, or consumer-specific semantics fail. | Exact XSD/profile and assertion/field/endpoint/order census; parse-serialize byte equality; minified, indent, tab, line-ending, namespace, attribute, empty-element, text-whitespace, identity, ownership, partial-profile, and resource-limit fixtures. |
| **SSM-REL-AC-03 — Endpoint role and content-sensitive reference closure** | Each endpoint resolves exact registered `(documentId, fragmentId, fragmentContentDigest)` through a validated content interface and permitted role. The digest hashes only the target's closed typed record, changes with substantive target content, and ignores XML formatting. Missing, stale, inferred, retargeted, or authority-promoting endpoints fail. | Relation/profile census, typed-target-digest computation, and endpoint resolver; substantive-change, formatting-invariance, missing, duplicate, role-swap, stale, ambiguity, retarget, relation-target, and authority-promotion fixtures. |
| **SSM-REL-AC-04 — Generated Markdown and coverage closure** | Fresh XML-to-Markdown rendering is byte-identical to the review view. Coverage independently recomputes readable serialization, every assertion/field/order, endpoint and target-item digest, anchor, excerpt, and forward/reverse link; self-report and stored evidence have no authority. | Cross-process rendering and independent ordered XML/interface/Markdown census; missing, extra, duplicate, reordered, stale-target, stale-excerpt, stale-link, self-report, and stored-evidence fixtures. |
| **SSM-REL-AC-05 — Snapshot-bound handoff, commands, and writes** | Production semantic edges receive only declared validated XML and dependencies; review-only Markdown cannot feed a semantic path. Handoff uses one root-bound retained-byte snapshot and forbids reopen, detached tokens, fallback, repair, or promotion. Regeneration rereads and revalidates after atomic replacement; the repository gate rebuilds fresh indexes. | Declared-edge resolver and exact read log; representation-isolation, pre-consumption, snapshot-mutation, reopen, fallback, pre-write-state, atomic-replacement, rollback, readback, and external-mutation fixtures. |
| **SSM-REL-AC-06 — Field evolution, audit, and implementation closure** | A relation-field, endpoint, storage-law, or typed-digest change coherently updates its XML owner, schema/profile, parser/serializer, resolver, projection, coverage, affected content contract, consumers, and tests. Exact live closure has no alternate owner/reader, parallel registry, unused digest mechanism, compatibility path, generic extension, or stored record. | Exact contract/registry/schema/profile/parser/serializer/surface/resolver/renderer/consumer/package/test census; storage-law, typed-field, partial-update, alternate-path, generic-extension, compatibility, and stored-record fixtures. |
<!-- SSM-REL-AC-TABLE:END -->

## Acceptance evidence boundary

The domain's data-only registry is the machine-readable source for the six criterion rows. The
marked table is its deterministic projection. The shared verifier checks this domain within one
corpus pass and emits ephemeral domain statuses bound to the supplied snapshot. No callback layer,
stored evidence file, approval record, or detached result substitutes for current execution.
