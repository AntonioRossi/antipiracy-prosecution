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
| **SSM-REL-AC-02 — Relation grammar and readable-storage closure** | Each package has one `relationSetId` envelope and assertions with distinct semantic `relationId` and anchor-only `xml:id`, profiled type/direction, owner, authored order, endpoints, and enumerated text fields. The relation XSD and exclusive profiles agree exactly on the complete grammar, and stored XML obeys readable serialization. No typed relation surface, self digest, extension, alias, or consumer semantic field exists. | Exact envelope/assertion/XSD/profile/identity/element/attribute/order/cardinality/scalar/digest census; parse-serialize equality; whole-profile, XSD-mutation, readable-spelling, ownership, unknown-field, and resource-limit fixtures. |
| **SSM-REL-AC-03 — Endpoint role and content-sensitive reference closure** | Each endpoint resolves exact registered `(documentId, fragmentId, fragmentContentDigest)` through a validated content interface and permitted role. Relation validation state includes every endpoint package and its transitive validation paths without granting consumer access. Missing, stale, omitted, inferred, retargeted, or authority-promoting endpoints fail. | Relation/profile and endpoint-package/read censuses, typed-target-digest computation, and endpoint resolver; omission, substantive-change, formatting-invariance, missing, duplicate, role-swap, stale, ambiguity, retarget, relation-target, and authority-promotion fixtures. |
| **SSM-REL-AC-04 — Generated Markdown and coverage closure** | Fresh XML-to-Markdown rendering is byte-identical to the review view. Coverage independently recomputes readable serialization, every assertion/field/order, endpoint and target-item digest, anchor, excerpt, and forward/reverse link; self-report and stored evidence have no authority. | Cross-process rendering and independent ordered XML/interface/Markdown census; missing, extra, duplicate, reordered, stale-target, stale-excerpt, stale-link, self-report, and stored-evidence fixtures. |
| **SSM-REL-AC-05 — Snapshot-bound handoff, commands, and writes** | The current authored-relation consumer-edge and constructed-handoff censuses are both zero. The shared resolver's relation XML handoff is retained bytes, role, declared dependencies, and exact validation reads, paired with same-context retained controls and carrying no surface or assets. Handoffs are immutable; direct reads, reopen, detached tokens, fallback, repair, promotion, and pre-write-state reuse fail. | Live relation-edge census and bytes-only relation-handoff fixture; exact edge/handoff/read census, retained-control, immutability, representation-isolation, direct-read/reopen, conflicting-handoff, snapshot-mutation, fallback, atomic-rollback/readback, and external-mutation fixtures. |
| **SSM-REL-AC-06 — Field evolution, audit, and implementation closure** | A relation field, endpoint, storage law, or typed-digest change coherently updates its XML owner, schema/profile agreement, parser/serializer, validated package state, resolver, projection, coverage, affected content contract, and tests. Exact live closure has no alternate owner/reader, parser-control bypass, parallel registry, mutable handoff, unused digest mechanism, compatibility path, generic extension, or stored record. | Exact contract/registry/schema/profile/agreement-checker/parser/serializer/validated-state/resolver/renderer/handoff/package/test census; storage-law, field, whole-profile, partial-update, control-bypass, alternate-path, generic-extension, compatibility, mutable-handoff, and stored-record fixtures. |
<!-- SSM-REL-AC-TABLE:END -->

## Acceptance evidence boundary

The domain's data-only registry is the machine-readable source for the six criterion rows. The
marked table is its deterministic projection. The shared verifier checks this domain within one
corpus pass and emits ephemeral domain statuses bound to the supplied snapshot. No callback layer,
stored evidence file, approval record, or detached result substitutes for current execution.
