# AA11393US — Authored Relation XML Technical Description

> **OPERATIVE INTERNAL CONTROL · NOT FOR FILING**
>
> This document defines the current authored-relation authority scheme and its consumer-neutral XML
> handoff. The coupled acceptance contract is
> [`acceptance criteria`](acceptance-criteria.md).

## 1. Purpose and authority boundary

The current direction is:

```text
applicant-authored relation XML authority ──deterministic projection──▶ generated Markdown review view
                  │
                  ├──exact endpoint resolution──▶ registered validated content items
                  └──validated, read-only────────▶ shared declared-edge resolver
```

Relation XML is the sole owner of each applicant-authored cross-document assertion. It owns the
stable relation identity, semantic owner, type, direction, ordered fields, and exact endpoints. An
endpoint supplies the assertion's evidence basis or subject but never adopts, authorizes, or owns
the assertion. Only relation categories enumerated by the current schema and profile may use this
authority scheme. Generated Markdown is a review representation and never becomes another owner.

Machine validation proves schema and profile validity, identity, semantic ownership, role and
direction constraints, exact digest-bound endpoint resolution, coverage, and deterministic
Markdown. It does not prove an assertion substantively or legally correct, approved, filing-ready,
or authorized for filing.

## 2. Package and assertion contract

Every package declares `authorityScheme="authored-relations-v1"` and has exactly one authoritative
`xmlFile` and one generated review `markdownFile`. It has no stored PDF, source manifest, generated
XML, second relation owner, or package-level coverage artifact.

The existing structured-source registry is the sole package registry. Its package/file roles,
router membership, consumer edges, and dependency files close exactly against registered relation
packages and endpoint documents; no parallel authority registry is permitted. Relation XML owns
semantic endpoints, while a consumer dependency authorizes one declared read. An endpoint does not
grant consumer access, and a dependency does not create an assertion, endpoint, or authority.

Every relation declares one stable relation identity, one semantic owner, one profile-enumerated
type and direction, ordered profile-enumerated assertion fields, and profile-conforming endpoints.
IDs are not derived from line numbers, XML positions, array indexes, visible text, or current
ordering. Copying one assertion into another package, assigning competing semantic owners, or
restating an assertion only for a consumer feature fails.

## 3. Required relation graph

The authoritative XML is a schema- and profile-validated relation graph, not a table serialization
or a prebuilt typed-item surface. Every applicable property has one closed representation:

| Property | Authored-relations requirement |
|---|---|
| Envelope identity | One stable `relationSetId` matching the registered `packageId` |
| Assertion identity | One unique relation XML-maintained `relationId` for every assertion |
| Projection identity | One unique `xml:id` anchor carrier for every assertion, distinct from `relationId` |
| Assertion type | One profile-enumerated relation type and direction |
| Hierarchy and order | Relation-set containment plus authored relation, field, and endpoint order |
| Numbering | A visible row, claim, or source number is an authored field when substantive; a mechanical ordinal may express order but is never identity |
| Content and metadata | One semantic owner and only profile-enumerated ordered field names with schema-bound text values |
| Provenance and dependencies | Exact registered endpoint documents and their authority roles |
| Cross-references | Role-bearing `(documentId, fragmentId, fragmentContentDigest)` endpoints |
| Content-sensitive integrity | Each endpoint carries the target item's typed-content digest; relation XML has no self or formatting-derived digest |

The relation-set root is an envelope, not a typed item: it has no `xml:id`, typed-item record, or
typed-item digest. `relationId` alone is the semantic assertion identity; `xml:id` carries the stable
review anchor and cannot replace it. Stable relation identity, authored numbers, mechanical
ordinals, and display labels remain separate. Insertion, deletion, or reordering may change a
mechanical ordinal but cannot silently rename an assertion.

The relation profile registry is exclusive. Each profile enumerates its one relation type,
directions, endpoint roles and required-role set, and assertion-field vocabulary; the schema,
target-item digest rule, readable XML storage law, and projection contract close the remaining
interface behavior. The relation XSD and every exclusive profile must agree exactly on the complete
envelope, assertion, endpoint, field, identity, order, cardinality, scalar, and digest grammar. A
partial profile change, alternate vocabulary, alias, extension map, consumer-defined relation
field, or unprofiled scalar interpretation fails closed.

### Controlled semantic and metadata evolution

Adding or changing a relation type, direction, role, assertion field, or endpoint property requires
one coherent current-state update to the relation XML owner, schema/profile, parser and resolver,
target-item digest rule, generated review projection, computed coverage, declared consumer
requirements, and focused positive and negative tests. Every newly referenceable content field must
already have one owner and stable item identity in its content package.

Unknown relation semantics, arbitrary extension maps, untyped assertion fields, copied consumer
interpretations, and renderer-only relations fail closed. A consumer need cannot create an
undeclared assertion or make endpoint content its semantic owner.

## 4. XML and endpoint contract

Relation XML uses the exact current namespace, XSD, profile, secure parser, and readable storage
law. Every registered XML file must equal deterministic serialization of its validated typed tree
with:

- the exact `<?xml version="1.0" encoding="UTF-8"?>` declaration;
- UTF-8 without a byte order mark, NFC text, LF only, and one final newline;
- required namespace declarations on the root, default first and named prefixes lexicographically;
- two-space indentation, no tabs or blank structural lines, and one child per structural line;
- each container start and end tag on its own line and each text-only leaf on one unwrapped line;
- attributes ordered by expanded name and empty elements written exactly as `<name />`.

Parse-to-typed-tree-to-serialization must reproduce the stored bytes. Structural indentation is not
typed content; text-leaf whitespace remains exact. Minified structural XML, alternate indentation,
line wrapping, attribute order, namespace placement, or empty-element spelling fails. `check`
enforces this law but never rewrites the authoritative relation XML.

The parser policy, GFM projection profile, XML profile registry, shared XML schema, and relation XSD
are loaded exactly once through the validation context's retained-byte reader. Control loading
proves the complete relation XSD/profile agreement before package parsing. The retained policy,
profiles, and schema mapping are transitively immutable; a package parser or consumer cannot use a
default, later-opened, substituted, partial, or consumer-local control.

Each endpoint binds the exact `(documentId, fragmentId, fragmentContentDigest)` of a registered
validated content item. Each relation profile declares its permitted roles and required-role set.
Repeated endpoint targets inside one assertion, missing required roles, unknown or swapped roles,
stale digests, ambiguous targets, undeclared documents, relation-to-relation endpoints, inferred
retargeting, and endpoint-driven authority promotion fail.

Integrity is deliberately narrow. `fragmentContentDigest` is the target content item's
`sha256/typed-item-v1:<64-lowercase-hex>`, computed over one `c1` JSON record containing exactly
`digestDomain="aa11393:ssp:typed-item:v1"`, the target authority scheme, schema profile, document
ID, item ID, item type, typed content tree, and substantive metadata under keys `authorityScheme`,
`schemaProfile`, `documentId`, `itemId`, `itemType`, `typedContent`, and `substantiveMetadata`. `c1`
uses UTF-8 JSON, NFC keys and strings, standard JSON escaping with non-ASCII preserved, object keys
in Unicode code-point order, semantic array order, integers within ±9,007,199,254,740,991, compact
separators, no floats, and one final LF. XML formatting, paths, mechanical envelope fields,
unrelated document metadata, generator versions, and sibling items are excluded. Relation XML has
no self or whole-XML semantic digest, and generated Markdown integrity uses fresh byte comparison
rather than a stored digest.

## 5. Projection and computed coverage

The current renderer deterministically projects validated relation XML to Markdown. The registered
Markdown bytes must equal fresh rendering. The view exposes the authority scheme and role,
assertion identity and ownership, ordered fields, stable anchors, current endpoint excerpts,
evidence basis, and forward and reverse links. It does not become a second assertion owner.

Coverage is independently recomputed from the current authoritative XML, resolved validated
content interfaces, and freshly rendered Markdown. Its ordered census includes every assertion,
field, exact endpoint and target-item digest, generated anchor, excerpt, and forward and reverse link;
missing, extra, duplicate, reordered, or stale members fail. Renderer or resolver self-report is
not evidence, and coverage is never stored as a package companion, receipt, or digest ledger.

## 6. Snapshot-bound consumer-neutral handoff

The current registry declares no authored-relation consumer edge; the current authored-relation
edge and constructed-handoff censuses are therefore both zero. The shared declared-edge resolver
nevertheless has one closed relation-package shape: an XML edge hands the authoritative retained
bytes, authority scheme, relation-XML role, declared dependency bytes, and exact validation-read
census; a Markdown edge hands review bytes only. Neither shape carries a prebuilt relation surface
or assets, and neither may read the other representation through an undeclared dependency.

Trust attaches only to the validated relation graph over one identified repository root, complete
snapshot path inventory, and exact retained bytes for every validation and handoff path. Before a
handoff, relation schema/profile, assertion/field/endpoint census, identities, owners, roles,
directions, endpoint targets and target-item digests, generated view, and coverage must all pass.
The validation-read census includes the relation package, registry, retained parser controls, and
every resolved endpoint package's transitive validation paths. That census is validation evidence,
not read authority: endpoint documents require their own declared consumer edges.

The consumer construction boundary receives the same-context retained parser controls alongside
the handoff set and secure-parses only the handed XML bytes. Handoff and dependency mappings,
validation-read tuples, and retained controls are transitively immutable. The consumer may not use
a default control, reopen a path, accept a detached pass token, infer a relation, repair a target,
or expose a mutable parse tree as a trusted final model.

A consumer may not copy or rewrite an assertion, infer or retarget an endpoint, change a role or
direction, add source-domain fields, silently fall back, or promote endpoint content into assertion
authority. The XML contains no consumer-specific layout, styling, interaction, control-flow, or
release fields. Product behavior, presentation, interaction, security, release, and delivery are
outside this contract.

## 7. Commands, writes, and aggregate verification

The shared structured-source command surface remains exactly `check <subject-id>`, `regenerate
<subject-id>`, `regenerate-controls`, and `verify-current`.

For this scheme, `check` validates one relation package and its exact endpoint dependencies without
writing or repeating a whole-corpus pass. `regenerate` validates the proposed Markdown before
atomically replacing only that package's generated view, discards pre-write derived state, rereads
the output, and revalidates the target and dependencies. `regenerate-controls` replaces only
derived routers and the three acceptance table regions; `verify-current` rebuilds fresh shared
indexes and participates in one whole-corpus pass over one unchanged snapshot. No pre-test index
crosses the test boundary. Relation authority, endpoint documents, and externally changed bytes
are never overwritten; coverage is computed and never persisted.

The repository-global gate owns immutable snapshot bracketing, registered isolated tests, final
snapshot revalidation, and the aggregate result. This domain contributes its own acceptance
statuses without defining any consumer product outcome.

## 8. Live implementation closure

This technical description, its acceptance criteria, its data-only acceptance registry, the
content registry's authored-relations slice, current schema/profile agreement checker, parser,
validated package state, endpoint resolver, renderer, shared declared-edge resolver, focused tests,
and registered packages are the exact live implementation census. No authored-relation consumer is
registered. Closure uses these existing controls and contains no parallel registry, generic
ownership framework, or generic reachability subsystem.

No alternate assertion owner or reader, compatibility or migration reader, approval or reviewer
record, stored receipt, digest ledger, coverage store, mutable handoff, parser-control bypass,
consumer reconstructor, export path, or inactive domain artifact remains operative. Git alone
retains implementation history.
