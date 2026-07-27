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
                  └──aggregate acceptance prerequisite; current consumer-edge census = 0
```

Relation XML is the sole owner of each applicant-authored cross-document assertion. It owns the
stable relation identity, semantic owner, type, direction, ordered fields, and exact endpoints. An
endpoint supplies the assertion's evidence basis or subject but never adopts, authorizes, or owns
the assertion. Only relation categories enumerated by the current schema and profile may use this
authority scheme. Generated Markdown is a review representation and never becomes another owner.

These packages do not supply the current navigator's relation semantics. The navigator-owned files
under `navigator/relations/` use the distinct `navigator-claim-pct-relations-v1` profile and own only
the current product's claim-to-PCT candidate associations. No navigator edge, runtime handoff,
upstream-relation reference, copy, restatement, or inheritance connects those product relations to an
`authored-relations-v1` package.

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

The complete parser-control set is the parser policy, GFM projection profile, XML profile registry,
shared XML schema, and every artifact XSD, including `authored.xsd`, `content.xsd`, and
`relations.xsd`. It is loaded exactly once through the validation context's retained-byte reader.
Control loading proves complete relation XSD/profile agreement before package parsing. The retained
policy, profiles, and schema mapping are transitively immutable; a package parser or consumer cannot
use a default, later-opened, substituted, partial, or consumer-local control.

Each endpoint supplies one nonempty `(documentId, fragmentId, fragmentContentDigest)` and resolves
that exact tuple once through a registered validated content item. Each relation profile declares
its permitted roles and required-role set. An omitted, null, empty, malformed, ambiguous, or
unresolved identity cannot become an inferred target, default result, empty excerpt, or fallback
link. Repeated endpoint targets inside one assertion, missing required roles, unknown or swapped
roles, stale digests, undeclared documents, relation-to-relation endpoints, inferred retargeting,
and endpoint-driven authority promotion fail.

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
Markdown bytes must equal fresh rendering. The view exposes assertion identity and ownership,
ordered fields, stable anchors, current endpoint excerpts, evidence basis, and exact endpoint
links. It does not become a second assertion owner. The authored `direction` field is assertion
semantics; it does not imply that the review projection contains a second reverse-link index.

Coverage is independently recomputed from the current authoritative XML, resolved validated
content interfaces, and freshly rendered Markdown. Its ordered census includes every assertion,
field, exact endpoint and target-item digest, generated anchor and anchor region, excerpt, and
endpoint link. The generated anchor inventory must equal the metadata anchor, schedule anchor, and
all assertion `xml:id` carriers in exact order. Missing, extra, displaced, duplicate, reordered, or
stale members fail. The verifier derives the census directly from XML, endpoint views, and Markdown;
renderer or resolver coverage self-report is not evidence, and coverage is never stored as a package
companion, receipt, or digest ledger.

## 6. Retained-worktree consumer-neutral handoff

The current registry declares no authored-relation consumer edge; the current authored-relation
edge and constructed-handoff censuses are therefore both exactly zero. The shared declared-edge
resolver acts only on a declared edge and consequently constructs no current relation handoff. Its
closed relation-package behavior remains representation-exact: an XML edge hands authoritative
retained bytes, authority scheme, relation-XML role, declared dependency bytes, and the exact
validation-read census; a Markdown edge hands review bytes only. Neither behavior carries a
prebuilt relation surface or assets or reads the other representation through an undeclared
dependency.

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

Each parsed relation artifact, resolved endpoint view, projection, coverage result, package result,
and handoff mapping belongs to one retained capture and one generated-view output state.
Immutability prevents mutation but never permits reuse after generated-view replacement.
Replacement ends every affected object's lifetime; subsequent validation constructs new endpoint
views, projections, results, and mappings even when the replacement bytes equal the prior bytes.
Retained parser-control and relation-authority bytes remain capture-bound inputs, while candidate
controls, output-derived objects, cached semantics, and detached pass tokens cannot cross a
replacement boundary.

A consumer may not copy or rewrite an assertion, infer or retarget an endpoint, change a role or
direction, add source-domain fields, silently fall back, or promote endpoint content into assertion
authority. The XML contains no consumer-specific layout, styling, interaction, control-flow, or
release fields. Product behavior, presentation, interaction, security, release, and delivery are
outside this contract.

## 7. Component commands, writes, and aggregate validation

The structured-source component command surface is exactly `check <subject-id>`, `regenerate
<subject-id>`, and `regenerate-controls`. It exposes no aggregate command or alias.

For this scheme, `check` validates one relation package and its exact endpoint dependencies without
writing or repeating a whole-corpus pass. `regenerate` strict-parses the authoritative relation XML,
resolves every exact endpoint, constructs the complete candidate Markdown, and independently proves
its assertion, field, endpoint, digest, anchor, excerpt, link, and order coverage before the first
write. Only then may it atomically replace that package's generated view. Before success, the same
transaction discards all candidate and pre-replacement derived state, exact-reads the replacement
Markdown, and repeats complete package, endpoint, projection, coverage, and dependency validation
from the replacement bytes. A readback mismatch or fresh-validation failure restores the exact
prestate; partial or unvalidated replacement is never current.

`regenerate-controls` first assembles one closed map of every candidate output path and byte
sequence, overlays it on unchanged retained controls, and freshly loads and strictly compiles the
complete candidate parser-control set, including relation XSD/profile agreement. Candidate failure
makes publication unreachable; the candidate control object is then discarded. A post-write check
or rollback cannot substitute for this pre-write proof. `relations.xsd` remains an unchanged
agreement input rather than a generated output.

One atomic transaction may replace only that passing map: the profile-generated content XSD,
derived routers, and the three acceptance table regions. Before success, the transaction reopens
every output path, compares every byte with the candidate map, and freshly loads the complete control
set using only replacement-path reads. A byte mismatch or fresh-load failure restores the complete
exact prestate; partial replacement is never current. Relation authority, endpoint documents, and
externally changed guard bytes are preserved and cause refusal. No candidate control, pre-write
validator, parsed artifact, endpoint view, projection, coverage result, package result, handoff,
cached semantics, or detached pass token can satisfy replacement validation. No rollback receipt,
recovery record, or alternate retained state is produced. Coverage remains computed and is never
persisted.

The shared [aggregate validation boundary](../../README.md#aggregate-validation-boundary) owns
retained-worktree bracketing, registered isolated tests, final
recapture comparison, and the aggregate result. This domain contributes its own acceptance
statuses without defining any consumer product outcome.

## 8. Live implementation closure

This technical description, its acceptance criteria, its data-only acceptance registry, the
content registry's authored-relations slice, current schema/profile agreement checker, parser,
validated package state, endpoint resolver, renderer, shared declared-edge resolver, focused tests,
and registered packages are the exact live implementation census. No authored-relation consumer is
registered. Closure uses these existing controls and contains no parallel registry, generic
ownership framework, or generic reachability subsystem.

The contract pair, data-only acceptance registry, registry slice, controls, implementation,
focused tests and vectors, generated review state, and zero-edge handoff census are accepted only
as one retained current state. A contract-only, registry-only, implementation-only, test-only,
generated-only, or edge-only state fails. Any operative relation field, endpoint, storage law,
command, or projection change must update every affected member of that state coherently.

Required shared implementation closure is transitive and executable. It includes every module
required by endpoint validation, projection, aggregate acceptance, or the declared-edge resolver;
every schema and profile those modules use; the shared aggregate launcher; and every registered test
and required vector. Over the complete retained capture, the closure enforcer recomputes all
implementation-code, contract, schema, and required-vector paths wherever they occur and compares
those censuses exactly with the live implementation inventory. The exact `structured_source/`
subtree census is an additional check, never a substitute for capture-wide closure. Every captured
domain test module has exactly one current registration, and every registered test executes without
skip, expected failure, or inactive registration. A directly named subset, path convention, import
success, or runtime reachability alone cannot establish closure; a missing, additional, alternate,
inactive, or contradictory implementation, contract, registry, schema, launcher, test, vector,
projection, edge census, class, or policy fails.

No alternate assertion owner or reader, compatibility or migration reader, approval or reviewer
record, stored receipt, digest ledger, coverage store, mutable handoff, parser-control bypass,
consumer reconstructor, export path, or inactive domain artifact remains operative. Git alone
retains implementation history.

The focused negative suite rejects at least: a duplicate assertion identity or semantic owner; a
missing, swapped, duplicated, or unprofiled endpoint role; an absent fragment or stale target digest;
an unresolved endpoint represented as an empty or default target;
an omitted, additional, reordered, or displaced generated field, endpoint, link, excerpt, or anchor;
renderer self-report offered for defective Markdown; attempted publication of invalid candidate
Markdown or parser controls; replacement-byte mismatch or fresh replacement validation failure
without complete rollback; any current authored-relation consumer edge or handoff; a missing or
extra shared module, contract, registry, schema, launcher, registered test, or vector anywhere in the
retained capture; and reuse of a pre-replacement parsed artifact, endpoint view, projection, coverage
result, package result, handoff mapping, semantic object, or validation state even when replacement
bytes are unchanged.
