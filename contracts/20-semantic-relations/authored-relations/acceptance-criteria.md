# AA11393US — Authored Relation XML Acceptance Criteria

> **OPERATIVE INTERNAL CONTROL · NOT FOR FILING**
>
> This is the current acceptance contract coupled to
> [`technical description`](technical-description.md).


## Domain pass rule

All six executable outcomes must pass within the shared
[aggregate validation boundary](../../README.md#aggregate-validation-boundary) on the retained
worktree capture. Each registry row names its independent enforcer. A warning, unknown result, inference,
self-report, stored result, detached token, prior run, stale view, invalid endpoint, duplicate
semantic owner, or undeclared read cannot satisfy a criterion.

<!-- SSM-REL-AC-TABLE:START -->
| ID | Executable technical outcome | Independent enforcer |
|---|---|---|
| **SSM-REL-AC-01 — Authority, package, and ownership closure** | Each `authored-relations-v1` package has one authoritative relation XML and one generated Markdown review view. XML alone owns each profiled assertion and field. Package/file/router declarations close exactly; endpoints do not authorize reads, dependencies do not create semantics, and the prior-art navigator consumes only its four declared relation XML handoffs. | structured_source.verify.VerificationContext._control_closure; structured_source.tests.test_registry |
| **SSM-REL-AC-02 — Relation grammar and readable-storage closure** | Each package has one `relationSetId` envelope and assertions with distinct semantic `relationId` and anchor-only `xml:id`, profiled type/direction, owner, order, endpoints, and enumerated fields. The relation XSD and exclusive profiles agree on the complete readable grammar; typed relation surfaces, self digests, extensions, aliases, and consumer fields fail. | structured_source.parser.parse_artifact; structured_source.tests.test_xml_contract |
| **SSM-REL-AC-03 — Endpoint role and content-sensitive reference closure** | Each permitted role resolves one exact registered `(documentId, fragmentId, fragmentContentDigest)` through a validated content interface and only to the role's profiled content-authority scheme. Validation includes every endpoint package's transitive paths without granting access; missing, duplicate, stale, swapped, inferred, retargeted, relation-to-relation, or authority-promoting endpoints fail. | structured_source.verify.VerificationContext._render_relation; structured_source.tests.test_conversion |
| **SSM-REL-AC-04 — Generated Markdown and coverage closure** | Fresh rendering is byte-identical to the review view. Independent coverage recomputes every assertion, field, endpoint, digest, excerpt/link, and exact anchor inventory, order, and region from XML and Markdown; renderer self-report and stored evidence have no authority. | structured_source.relation_projection.validate_relation_projection; structured_source.tests.test_conversion |
| **SSM-REL-AC-05 — Worktree-capture-bound handoff and writes** | The current authored-relation consumer-edge and handoff censuses are exactly the AF and NA prior-art consumers receiving their strategy comparison matrix and passage map. Review regeneration prevalidates the complete candidate, preserves relation authority and endpoint bytes, atomically publishes, exact-reads the replacement, rebuilds fresh state, and fully rolls back on failure. Invalid candidates, reopen, inference, fallback, repair, promotion, detached state, and prior-state reuse fail. | structured_source.verify.VerificationContext.regenerate; structured_source.tests.test_conversion |
| **SSM-REL-AC-06 — Field evolution and implementation closure** | Every relation field, endpoint, storage law, or digest change coherently updates all affected owners, the contract pair, registries, controls, resolver, projection, coverage, consumers, tests, and generated state. Controls publish only as a closed prevalidated map with fresh readback and rollback. Capture-wide closure exactly matches domain/shared code, contracts, schemas, launchers, registered tests, and vectors; missing, extra, alternate, inactive, bypass, compatibility, stored-record, or orphaned states fail. | structured_source.verify.VerificationContext._control_closure; structured_source.tests.test_acceptance |
<!-- SSM-REL-AC-TABLE:END -->

## Registry and execution boundary

The domain's data-only registry is the machine-readable source for the six criterion rows. The
marked table is its deterministic projection. The shared validator checks this domain within the
current retained capture and emits only ephemeral technical status. No callback, self-report,
stored result, approval record, detached token, or prior run substitutes for current execution.
