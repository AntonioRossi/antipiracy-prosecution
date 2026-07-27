# AA11393US — Authored Markdown to XML Technical Description

> **OPERATIVE INTERNAL CONTROL · NOT FOR FILING**
>
> This document defines the current authored-Markdown authority scheme and its consumer-neutral XML
> handoff. The coupled acceptance contract is
> [`acceptance criteria`](acceptance-criteria.md).

## 1. Purpose and authority boundary

The current direction is:

```text
authored Markdown authority ──deterministic conversion──▶ generated XML
                                                              │
                                                              ├──non-stored semantic back-render check
                                                              └──validated, read-only──▶ declared consumer interface
```

Markdown is the sole authority for adopted content-bearing material, stable anchors and item
identities, authored order, and substantive item metadata. XML is the deterministic generated typed
machine representation, not another authority. A declared consumer receives only the representation
selected by its registry edge. The current navigator edges select generated XML exclusively; the
navigator never receives or reconverts Markdown when constructing its semantic model. Markdown may
occur in the inherited validation-read census because package validation proves XML against its
authority, but that evidence neither hands Markdown to the consumer nor authorizes a later read. The
semantic back-render is ephemeral comparison evidence and is never stored as a second Markdown
owner.

Machine validation proves supported-profile parsing, identity and metadata preservation,
conversion completeness, semantic round-trip equivalence, coverage, and deterministic XML. It does
not prove human attention, substantive or legal correctness, counsel approval, filing readiness,
or filing authorization.

## 2. Package and ownership contract

Every package declares `authorityScheme="authored-markdown-v1"` and has exactly one authoritative
`markdownFile` and one generated `xmlFile`. It has no stored PDF, source manifest, generated review
Markdown companion, or manually maintained XML region.

Package/file, router/file, and consumer-dependency/file ownership each close in both directions.
Every registered file in those classes has exactly one applicable owner or declaration, and every
owner or declaration resolves exactly one registered file of the required role. An unowned
registered file and a declaration without its reciprocal file both fail.

Authoritative Markdown contains the package's stable `ssp-*` anchors and every adopted
content-bearing structure and substantive metadata field. XML preserves those semantics and may
add only classified mechanical envelope fields: schema/profile/version declarations, authority
binding and raw digest, deterministic ordinals, and typed-item digests.

Stable IDs are not derived from line numbers, heading slugs, XML positions, array indexes, visible
text, or current ordering. Unknown fields, untyped extension maps, hidden content, competing
owners, and substantive information present only in generated XML fail closed.

## 3. Required XML item surface

The generated XML is an itemized semantic surface, not merely a serialization of one Markdown
file. Every applicable property has one closed representation:

| Property | Authored-Markdown requirement |
|---|---|
| Document identity | One stable `documentId` matching the registered package |
| Document item | One Markdown-owned root item bound to the complete ordered semantic document |
| Item identity | One unique Markdown-owned item ID preserved from its `ssp-*` anchor |
| Item type | One profile-supported typed Markdown/Pandoc construct or declared fragment type |
| Hierarchy and order | Exact authored AST containment and source order |
| Numbering | A claim or other visible number remains source-owned content/metadata; a generated ordinal may express order but is never identity |
| Content | Exact supported semantic content, including links, claims, tables, notes, code, and advisories |
| Metadata | Only closed typed fields originating in authoritative Markdown or classified mechanical envelope fields |
| Provenance | Exact Markdown authority path, raw digest, and size at the document binding |
| Dependencies | Exact supported links and registered dependencies when applicable |
| Content-sensitive digest | Item-local digest of the closed typed record, used only when exact item content is referenced |
| Relation endpoints | Inapplicable to this content scheme; relations are owned by a relation package |

Stable identity, source-owned numbering, mechanical ordinals, and display labels are separate.
Insertion, deletion, or reordering may change a mechanical ordinal but cannot silently rename an
item. A heading slug, array position, generated anchor carrier, or presentation label cannot become
a machine reference.

The exact first stable anchor is `<a id="ssp-<documentId>-root"></a>`. It owns one document item
with ID `<documentId>-root`, type `document`, semantic path `$`, the complete ordered supported
Pandoc block tree as typed content, and empty substantive metadata. Its typed-item digest follows
the item-digest law; it is not an XML-wide digest and excludes the Markdown path and raw binding,
generated envelope, formatting, parser controls, and presentation-only anchor placement.

Every stable anchor is one exact adjacent open/close pair inside a supported Pandoc block. The root
anchor binds the complete ordered semantic document. A non-claim anchor binds semantic content
following it in the current block or, when its carrier has no semantic content, the next supported
semantic block. A claim anchor binds its claim block and every immediately consecutive limitation
anchor whose ID has that claim's exact prefix. A non-root anchor without a target, a claim without
claim content, or a duplicate or ambiguous binding fails.

The generated fragment index records each anchor's exact fragment ID, presentation ID, binding kind,
semantic path, binding digest, and excerpt in authored order. Parsing generated XML independently
reconstructs those bindings from the preserved Pandoc tree and requires exact index equality.
Every semantic endpoint supplies one nonempty `documentId`, `fragmentId`, and typed-item digest and
resolves that exact tuple once or fails. An omitted, null, empty, malformed, ambiguous, or unresolved
identity cannot become an inferred target, default result, empty leaf, or empty collection. This
source contract defines no prebuilt hierarchy-traversal surface.

The current GFM profile is the exclusive executable inventory of Pandoc version and API, reader and
writer, supported and top-level constructors, stable-anchor syntax and XML identity policy, link
schemes, line endings and final newline, list and table style, and permitted presentational
normalizations. The XSD, converter, and profile agree exactly on those inventories and on Pandoc
value models, fragment kinds and fields, authority binding, document identity, and generated
envelope shape; none independently authorizes a construct, scalar, container, field, or rule
omitted by another.

An authored link is Markdown-owned semantic content subject to the profile's link rules; it is not
silently promoted to a package dependency. A consumer dependency is a separately registered file
reference selected by the declared edge, cannot bypass that edge's representation, and is handed
over only as an exact snapshot byte. A semantic cross-package dependency requires an explicit
schema, profile, and registry binding; when exact content matters, it names the stable item and its
typed-item digest rather than inferring a dependency from a link.

### Controlled semantic and metadata evolution

Adding or changing an authored semantic or metadata field requires one coherent current-state
update to its authoritative Markdown expression, schema/profile, converter and semantic
back-render, item-digest rule, computed coverage, declared consumer requirements, and focused
positive and negative tests. Any affected relation endpoint or dependency changes in the same
update.

No substantive field may originate only in generated XML. Unknown fields, arbitrary extension
maps, untyped metadata bags, converter-only enrichment, and renderer-only interpretations fail
closed. Mechanical envelope fields remain closed and cannot carry authored meaning.

## 4. Markdown profile and generated XML

Markdown uses the pinned GFM reader, one stable-anchor syntax, UTF-8 without a byte order mark, LF
line endings with no carriage returns, final newline, NFC, closed link schemes, and only the current
profile's supported constructors. Unsupported raw HTML, unpaired or duplicate anchors, unsafe
links, lossy structures, ambiguous claims, and constructs outside the profile fail before
generation.

Generated XML uses the exact current namespace, XSD, profile, secure parser, and readable storage
law. The complete parser-control set is the parser policy, GFM profile, XML profile, shared XML
schema, and every artifact XSD, including `authored.xsd`, `content.xsd`, and `relations.xsd`. It is
loaded through the retained-snapshot reader as one transitively immutable control set. The authored
XSD is a current agreement peer of the profile and converter; it is not the profile-generated
`content.xsd` and `regenerate-controls` does not generate it. Every production
conversion, generated-XML parse, and back-render uses the retained profile and validators from that
set; live or default controls and ambient validator caches cannot satisfy retained-capture
validation.

Every registered XML file must equal deterministic serialization of its validated typed tree with:

- the exact `<?xml version="1.0" encoding="UTF-8"?>` declaration;
- UTF-8 without a byte order mark, NFC text, LF only, and one final newline;
- required namespace declarations on the root, default first and named prefixes lexicographically;
- two-space indentation, no tabs or blank structural lines, and one child per structural line;
- each container start and end tag on its own line and each text-only leaf on one unwrapped line;
- attributes ordered by expanded name and empty elements written exactly as `<name />`.

Parse-to-typed-tree-to-serialization must reproduce the registered bytes. Structural indentation is
not typed content; text-leaf whitespace remains exact. Minified structural XML, alternate
indentation, line wrapping, attribute order, namespace placement, or empty-element spelling fails,
and regeneration always emits the required readable form.

The XML authority binding records the exact Markdown path, raw SHA-256 digest, and size because
those authority bytes matter. Generated XML integrity uses fresh byte comparison, not a stored XML
digest. A content-sensitive item digest is `sha256/typed-item-v1:<64-lowercase-hex>`, computed over
one `c1` JSON record containing exactly `digestDomain="aa11393:ssp:typed-item:v1"`, authority
scheme, schema profile, document ID, item ID, item type, typed content tree, and substantive
metadata under keys `authorityScheme`, `schemaProfile`, `documentId`, `itemId`, `itemType`,
`typedContent`, and `substantiveMetadata`. `c1` uses UTF-8 JSON, NFC keys and strings, standard JSON
escaping with non-ASCII preserved, object keys in Unicode code-point order, semantic array order,
integers within ±9,007,199,254,740,991, compact separators, no floats, and one final LF. XML
formatting, paths, mechanical envelope fields, unrelated document metadata, generator versions,
and sibling items are excluded. No XML-wide semantic digest is kept merely because an artifact was
generated.

Successful parsing, conversion, and round-trip comparison prove only preservation within the
supported profile. They do not prove authorial intent, substantive correctness, human attention,
legal correctness, approval, filing readiness, or filing authorization.

## 5. Conversion, semantic back-render, and coverage

The pinned converter preserves the complete supported ordered Pandoc AST: headings, paragraphs,
lists, tables and cells, claims and limitations, links, notes, code, advisories, identities,
metadata, hierarchy, and order. Fresh XML must equal the registered generated XML byte-for-byte.

Rendering that XML to the same pinned GFM semantic form must preserve the ordered Pandoc AST after
only the profile-listed presentation normalizations: anchor-carrier placement, equivalent Markdown
escaping, and final newline. A normalization cannot add, remove, reorder, or rewrite a
content-bearing node.

Coverage is computed from the current snapshot and maps every authoritative Markdown item to its
generated XML item, typed-item digest, and back-rendered semantic node. Neither the back-render nor
a package-level coverage artifact is stored.

The verifier independently recomputes the complete ordered coverage census from the authoritative
Markdown AST and validated XML rather than accepting converter-reported identities or digests as
validation input. The census checks each stable anchor, semantic path, authority binding, readable
XML item and field, typed-item digest, back-render node, dependency, generated-byte identity,
hierarchy, and order. A missing, extra, duplicate, reordered, lossy, stale, or non-readable item,
field, or representation fails.

Moving an authoritative anchor changes its semantic binding. The generated fragment index, binding
and typed-item digests, generated XML, and every affected exact endpoint must then agree with that
current binding. Authored-anchor validation is based on the preserved Pandoc tree and binding rules,
not on PDF-review projection regions.

## 6. Retained-worktree consumer-neutral handoff

A declared consumer edge selects exactly one registered representation, `xml` or `markdown`, and
cannot read the other representation through an undeclared dependency. An XML handoff supplies the
authority scheme, generated role, exact validated generated-XML bytes, dependencies, and exact read
census; it carries no prebuilt source surface or assets. A consumer that constructs a semantic model
receives the retained parser controls from the same validation context and secure-parses only those
handed XML bytes. A Markdown handoff supplies the authority bytes directly and receives no generated
XML state.

An acceptable retained worktree capture supplies a nonempty internal digest, the worktree root, a closed path
inventory, and retained bytes addressable through that inventory. A digest string, pass result, or
other detached token is not a snapshot. Every package-validation and declared-dependency path in a
handoff must occur in the snapshot inventory, and its validated bytes must equal the retained
snapshot bytes exactly.

Technical status attaches only to the validated item graph over the exact retained capture bytes. Before a
consumer constructs a semantic model or writes an output, Markdown profile, conversion,
item/field census, hierarchy, order, authority raw binding, typed-item digests, generated XML,
semantic back-render, dependencies, and coverage must all pass. The consumer receives those same
validated bytes and, for XML, uses the supplied retained controls to construct one immutable typed
model before mechanically looking up an explicitly identified item, following its preserved
hierarchy and order, selecting declared fields, or resolving an exact dependency endpoint. An
unresolved lookup fails. The consumer may not reopen a path, accept a detached pass token, rerun
Markdown conversion, or infer missing semantics.

Package validation constructs and transitively freezes the authority and generated representation
bytes, dependency and handoff mappings, and retained control profiles. It validates the complete
typed-item record and digest census without handing over a prebuilt source surface. The handoff uses
that validated state without reopening even the same live path or reconstructing semantics from a
later read, and exposes the exact validation-read census for the edge.

Each conversion result, parsed generated artifact, fragment index, coverage result, package result,
and handoff belongs to one retained capture and one generated-XML output state. Immutability prevents
mutation but never permits reuse after generated-XML replacement. Replacement ends every affected
object's lifetime; subsequent validation constructs new derived state and handoffs even when the
replacement bytes equal the prior bytes. Retained parser-control bytes remain capture-bound inputs,
while candidate controls, output-derived objects, cached semantics, and detached pass tokens cannot
cross a replacement boundary.

Selection of XML never promotes it above Markdown authority. A consumer may not repair generated
XML, infer missing authored content, add source-domain fields, reparse an undeclared representation,
or silently fall back. The XML contains no consumer-specific layout, styling, interaction,
control-flow, or release fields. Product behavior, presentation, interaction, security, release,
and delivery are outside this contract.

## 7. Component commands, writes, and aggregate validation

The structured-source component command surface is exactly `check <subject-id>`, `regenerate
<subject-id>`, and `regenerate-controls`. It exposes no aggregate command or alias.

For this scheme, `check` validates one package and its declared dependencies without writing.
`regenerate` parses the authority Markdown, constructs the complete candidate XML, strict-parses it
under the retained control set, independently recomputes its fragment index and typed records, and
proves semantic back-render equality before the first write. Only then may it atomically replace that
package's generated XML. Before success, the same transaction discards all candidate and
pre-replacement derived state, exact-reads the replacement XML, and repeats complete package,
fragment, typed-record, back-render, coverage, and dependency validation from the replacement bytes.
A readback mismatch or fresh-validation failure restores the exact prestate; partial or unvalidated
replacement is never current.

`regenerate-controls` first assembles one closed map of every candidate output path and byte
sequence, overlays it on unchanged retained controls, and freshly loads and strictly compiles the
complete candidate parser-control set. Candidate profiles, every artifact XSD, shared schema, and
independent agreement checks must pass before the first write; `authored.xsd` remains an unchanged
agreement input rather than a generated output. The candidate control object is then discarded. A
post-write check or rollback cannot substitute for this pre-write proof.

One atomic transaction may replace only that passing map: the profile-generated content XSD,
derived routers, and the three acceptance table regions. Before success, the transaction reopens
every output path, compares every byte with the candidate map, and freshly loads the complete control
set using only replacement-path reads. A byte mismatch or fresh-load failure restores the complete
exact prestate; partial replacement is never current. Markdown authority and externally changed
guard bytes are preserved and cause refusal. No candidate control, pre-write validator, parsed
artifact, conversion result, fragment index, coverage result, package result, handoff, cached
semantics, or detached pass token can satisfy replacement validation. No rollback receipt, recovery
record, or alternate retained state is produced. Coverage and back-render evidence remain computed
and are never persisted.

The shared [aggregate validation boundary](../../README.md#aggregate-validation-boundary) owns
retained-worktree bracketing, registered isolated tests, final
recapture comparison, and the aggregate result. This domain contributes its own acceptance
statuses without defining any consumer product outcome.

Aggregate validation constructs exactly one passing handoff for every declared consumer edge;
resolving or counting an edge is insufficient. The declared-edge and constructed-handoff censuses
must agree exactly. At the consumption boundary, the handoff census is bound before ordinary reads;
an ordinary read of a handed path or conflicting bytes for the same path fails.

## 8. Live implementation closure

This technical description, its acceptance criteria, its data-only acceptance registry, the
content registry's authored-Markdown slice, current schemas and profiles, converter, focused tests,
typed-item record and digest builder, generated-XML validator, semantic back-render, immutable
snapshot handoff, registered consumers, and registered packages are the complete live implementation.
The retained worktree capture must contain the exact named domain artifacts and every required
shared implementation path.

The contract pair, data-only acceptance registry, registry slice, controls, implementation,
focused tests and vectors, generated XML, back-render proof, and declared handoffs are accepted only
as one retained current state. A contract-only, registry-only, implementation-only, test-only,
generated-only, or handoff-only state fails. Any operative field, storage law, binding, command, or
handoff change must update every affected member of that state coherently.

Required shared implementation closure is transitive and executable. It includes every module
required by this domain or a declared consumer boundary, every schema and profile those modules use,
the shared aggregate launcher, and every registered test and required vector. Over the complete
retained capture, the closure enforcer recomputes all implementation-code, contract, schema, and
required-vector paths wherever they occur and compares those censuses exactly with the live
implementation inventory. The exact `structured_source/` subtree census is an additional check,
never a substitute for capture-wide closure. Every captured domain test module has exactly one
current registration, and every registered test executes without skip, expected failure, or inactive
registration. A directly named subset, path convention, import success, or runtime reachability
alone cannot establish closure; a missing, additional, alternate, inactive, or contradictory
implementation, contract, registry, schema, launcher, test, vector, generated representation,
handoff, class, or policy fails.

No alternate converter, editable generated owner, production parser-control bypass, consumer-side
Markdown reconverter, alternate generated-XML reader, mutable handoff, compatibility or migration
reader, approval or reviewer record, stored receipt, digest ledger, persisted back-render, coverage
store, export path, or inactive domain artifact remains operative. Git alone retains implementation
history.

The focused negative suite rejects at least: a malformed, duplicate, or targetless anchor; a
fragment index or digest inconsistent with the preserved Pandoc tree; an omitted, malformed,
unresolved, or stale exact endpoint and representation of absence as an empty or default result;
publication of invalid candidate XML or parser controls; replacement-byte mismatch or fresh
replacement validation failure without complete rollback; a missing or extra shared module,
contract, registry, schema, launcher, registered test, or vector anywhere in the retained capture;
and reuse of a pre-replacement conversion, parsed artifact, fragment index, coverage result, package
result, handoff, semantic object, or validation state.
