# AA11393US — Authored Relation XML Technical Description

> **OPERATIVE INTERNAL CONTROL · NOT FOR FILING**
>
> This document defines the current authored-relation authority scheme and its consumer-neutral XML
> handoff. The coupled acceptance contract is
> [`AA11393US-structured-source-authored-relations_acceptance-criteria.md`](AA11393US-structured-source-authored-relations_acceptance-criteria.md).

## 1. Purpose and authority boundary

The current direction is:

```text
applicant-authored relation XML authority ──deterministic projection──▶ generated Markdown review view
                  │
                  ├──exact endpoint resolution──▶ registered validated content items
                  └──validated, read-only────────▶ declared consumer interface
```

Relation XML is the sole owner of each applicant-authored cross-document assertion. It owns the
stable relation identity, semantic owner, type, direction, ordered fields, and exact endpoints. An
endpoint supplies the assertion's evidence basis or subject but never adopts, authorizes, or owns
the assertion. Generated Markdown is a review representation and never becomes another owner.

Machine validation proves schema and profile validity, identity, semantic ownership, role and
direction constraints, exact digest-bound endpoint resolution, coverage, and deterministic
Markdown. It does not prove an assertion substantively or legally correct, approved, filing-ready,
or authorized for filing.

## 2. Package and assertion contract

Every package declares `authorityScheme="authored-relations-v1"` and has exactly one authoritative
`xmlFile` and one generated review `markdownFile`. It has no stored PDF, source manifest, generated
XML, second relation owner, or package-level coverage artifact.

Every relation declares one stable relation identity, one semantic owner, one profile-enumerated
type and direction, ordered profile-enumerated assertion fields, and profile-conforming endpoints.
IDs are not derived from line numbers, XML positions, array indexes, visible text, or current
ordering. Copying one assertion into another package, assigning competing semantic owners, or
restating an assertion only for a consumer feature fails.

## 3. XML and endpoint contract

Relation XML uses the exact current namespace, XSD, and profile; UTF-8 XML 1.0; NFC text; and the
secure parser. DTDs, non-predefined entities, external resources, XInclude, XLink, comments,
processing instructions, CDATA, `xml:base`, recovery, duplicate IDs, unknown fields, types,
directions or versions, aliases, and resource-limit violations fail closed.

Each endpoint binds the exact `(documentId, fragmentId, fragmentContentDigest)` of a registered
validated content item. Each relation profile declares its permitted roles and required-role set.
Repeated endpoint targets inside one assertion, missing required roles, unknown or swapped roles,
stale digests, ambiguous targets, undeclared documents, relation-to-relation endpoints, inferred
retargeting, and endpoint-driven authority promotion fail.

Raw and domain-separated canonical semantic digests are computed from the immutable snapshot.
Relation XML does not self-bind its own digest. Relation digests cover the assertion identity,
profile, owner, type, direction, ordered fields, and endpoints; endpoint fragment digests remain
item-local so unrelated sibling changes do not stale the relation.

## 4. Projection and computed coverage

The current renderer deterministically projects validated relation XML to Markdown. The registered
Markdown bytes must equal fresh rendering. The view exposes the authority scheme and role,
assertion identity and ownership, ordered fields, stable anchors, current endpoint excerpts,
evidence basis, and forward and reverse links. It does not become a second assertion owner.

Coverage is computed from the current snapshot and includes every relation assertion, assertion
field, exact endpoint, generated anchor, excerpt, and link. Reuse of one endpoint across distinct
assertions is valid; duplicate semantic ownership of the same assertion is not. Coverage is not a
stored package companion.

## 5. Consumer-neutral handoff

A declared consumer edge selects exactly one registered representation, `xml` or `markdown`, and
cannot read the other representation through an undeclared dependency. An XML handoff supplies the
authority scheme, authoritative role, typed assertions, owners, directions, fields, endpoints, and
resolved identities and digests. A Markdown handoff supplies only the declared review view.

A consumer may not copy or rewrite an assertion, infer or retarget an endpoint, change a role or
direction, add source-domain fields, silently fall back, or promote endpoint content into assertion
authority. Product behavior, presentation, interaction, security, release, and delivery are
outside this contract.

## 6. Commands, writes, and aggregate verification

The shared structured-source command surface remains exactly `check <subject-id>`, `regenerate
<subject-id>`, `regenerate-controls`, and `verify-current`.

For this scheme, `check` validates one relation package and its exact endpoint dependencies without
writing; `regenerate` validates relation authority and endpoint bytes before atomically replacing
only that package's generated Markdown; `regenerate-controls` replaces only derived routers and
the three acceptance table regions; and `verify-current` participates in one memoized whole-corpus
pass. Relation authority, endpoint documents, and externally changed bytes are never overwritten.
Coverage is computed and never persisted.

The repository-global gate owns immutable snapshot bracketing, registered isolated tests, final
snapshot revalidation, and the aggregate result. This domain contributes its own acceptance
statuses without defining any consumer product outcome.

## 7. Live implementation closure

This technical description, its acceptance criteria, its data-only acceptance registry, the
content registry's authored-relations slice, current schemas and profiles, resolver, renderer,
focused tests, and registered packages are the complete live implementation.

No alternate assertion owner or reader, compatibility or migration reader, approval or reviewer
record, stored receipt, digest ledger, coverage store, export path, or inactive domain artifact
remains operative. Git alone retains implementation history.
