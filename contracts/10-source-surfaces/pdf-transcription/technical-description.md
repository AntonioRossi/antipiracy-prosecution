# AA11393US — PDF Evidence Transcription Technical Description

> **OPERATIVE INTERNAL CONTROL · NOT FOR FILING**
>
> This document defines the current PDF-evidence transcription authority scheme and its
> consumer-neutral XML handoff. The coupled acceptance contract is
> [`acceptance criteria`](acceptance-criteria.md).

## 1. Purpose and authority boundary

The current direction is:

```text
stored PDF fidelity authority
        │ manual human/OCR-assisted transcription
        ▼
asserted transcription XML ──deterministic projection──▶ generated Markdown review view
        │
        └──validated, read-only──▶ declared consumer interface
```

The stored PDF governs source fidelity. The XML owns the repository's manually asserted
transcription, stable identities, provenance, uncertainty where known, and permitted metadata. The
generated Markdown is a review representation and never becomes another authority. The current
navigator edges select transcription XML; generated Markdown is not a navigator semantic input.
PDF and Markdown paths may occur in inherited validation-read evidence, but that census neither
hands those representations to the consumer nor authorizes a later read. OCR may assist inspection
but is not authoritative and cannot be accepted automatically.

Machine validation proves registered-byte identity, manifest and checksum consistency, XML
validity, provenance structure, reference closure, coverage, and deterministic Markdown. It does
not prove PDF authenticity, transcription fidelity, human attention, substantive or legal
correctness, counsel approval, filing readiness, or filing authorization.

## 2. Package and ownership contract

Every package declares `authorityScheme="pdf-evidence-transcription-v1"` and has exactly:

- one stored PDF;
- one source manifest;
- one manually maintained transcription `xmlFile`;
- one generated review `markdownFile`; and
- only the registered assets and expressly non-authoritative convenience derivatives applicable to
  that package.

The registry resolves every file through its exact file ID and role. It contains no second PDF or
transcription owner, generated-file authority, coverage-artifact field, cached package digest,
approval field, or consumer-specific semantic content.

Package/file, router/file, and consumer-dependency/file ownership each close in both directions.
Every registered file in those classes has exactly one applicable owner or declaration, and every
owner or declaration resolves exactly one registered file of the required role. An unowned
registered file and a declaration without its reciprocal file both fail.

The XML maintains stable document and item IDs. IDs are not derived from page number, line number,
XPath position, array index, visible text, heading slug, or sort order. Every transcribed content
item has page or region provenance tied to the manifest-bound PDF. Any known transcription
uncertainty is stated in the XML; its absence is never treated as machine proof of fidelity.

## 3. Required XML item surface

The validated XML is an itemized semantic surface, not merely a well-formed transcription file.
Every applicable property has one closed representation:

| Property | PDF-transcription requirement |
|---|---|
| Document identity | One stable `documentId` matching the registered package |
| Document item | One addressable root item bound to the stored source and the exact ordered content tree |
| Item identity | One unique XML-maintained item ID for every addressable transcribed unit |
| Item type | One schema-enumerated content type |
| Hierarchy and order | Typed XML containment and document order preserve the asserted source structure |
| Numbering | A source-visible number is content or typed metadata; a mechanical ordinal may express order but is never identity |
| Content | Exact asserted semantic content of the transcribed unit |
| Metadata | Only schema/profile-enumerated typed fields owned by the transcription XML |
| Provenance | Page or region evidence bound to the stored PDF for every transcribed content item |
| Uncertainty | Present when known and typed by the current schema/profile |
| Dependencies and assets | Exact registered references when applicable |
| Content-sensitive digest | Item-local digest of the closed typed record, used only when exact item content is referenced |
| Relation endpoints | Inapplicable to this content scheme; relations are owned by a relation package |

Stable identity, source numbering, mechanical ordering, and display labels are separate. Insertion,
deletion, or reordering may change a mechanical ordinal but cannot silently rename an item. A page
number or generated anchor can assist review but cannot substitute for the item ID in a machine
reference.

Each surface has exactly one typed document item. Its stable ID is the root `xml:id`, its type is
`document`, its children are the top-level content-item IDs in document order, its typed content is
the exact ordered content tree, its substantive metadata is empty, and its source binding is the
manifest-bound stored PDF. Its typed-item digest follows the item-digest law; it is not a whole-XML
digest and excludes envelope metadata, provenance, paths, formatting, and parser controls.

Item lookup and hierarchy traversal are exact operations. Every invocation supplies one nonempty
stable item ID; an omitted, null, non-string, empty, or unresolved ID fails. Traversal first
resolves that requested parent and then returns its declared child IDs in document order. Traversal
from the typed document item explicitly supplies the root `xml:id` and returns exactly its
top-level content items; there is no default-root overload. An empty child collection proves only
that the supplied ID resolved an item whose declared child collection is empty.

The current profile is the sole authored executable inventory of the document item, complete XSD
grammar, document and provenance metadata with their scalar types, stable identity, item types and
metadata, every reachable typed-content node with its typed attributes and text/children/empty
value model, direct-child order and cardinality, document order, source-number treatment,
dependency target and digest rules, origin, readable XML storage, and typed-item digest inputs. The
retained `content.xsd` is only the deterministic validation representation rendered from that
profile. Its bytes must equal a fresh profile render before strict compilation. Independent parser
invariants must agree with the generated grammar and enforce every semantic child handler,
occurrence bound, order, item identity, and typed-record rule.

Each dependency declares one kind and subject identity. Asset dependencies resolve by the exact
registered raw-byte digest. Document and relation-package dependencies resolve through their
registered validated interfaces; when exact content matters, the reference names the stable item
and its typed-item digest. No whole-XML digest substitutes for item-level content sensitivity. The
dependency and asset censuses must be unique and exact, their kinds must agree with the target
authority, and a dependency cycle fails.

### Controlled semantic and metadata evolution

Adding or changing a transcription field or production requires one coherent current-state update
to its manually maintained XML owner, authoritative profile grammar, independent parser invariant
or semantic handler, serializer and renderer, item-digest rule, computed coverage, declared
consumer requirements, generated XSD, and focused positive and negative tests. If the field affects
a manifest, asset, provenance record, or reference, that binding changes in the same update. The
generated XSD is never edited as an independent owner.

An unknown field, arbitrary extension map, untyped metadata bag, renderer-only interpretation, or
field present without one declared owner fails closed. Consumer convenience cannot justify adding
source-domain semantics to a generated representation.

## 4. XML and manifest contract

Transcription XML uses the exact current namespace, profile-owned grammar, generated XSD, secure
parser, and readable storage law. The parser policy, projection profile, XML profile, immutable
grammar tree, shared XML schema bytes, and artifact XSD bytes are loaded through the
retained-snapshot reader as one transitively immutable control set. Every production parse compiles
a fresh strict validator from those retained bytes; live or default controls, retained mutable
validator objects, and ambient validator caches cannot satisfy retained-capture validation.

The complete parser-control set consists of that parser policy, projection profile, XML profile,
immutable profile grammar, shared XML schema, and every artifact schema, including the generated
content XSD. Candidate and replacement controls use the same strict loader and independent
profile/grammar/semantic-invariant checks as package parsing. A partial schema compile, direct XSD
parse, or validation of only changed bytes cannot establish control-set validity.

Every registered XML file must equal deterministic serialization of its validated typed tree with:

- the exact `<?xml version="1.0" encoding="UTF-8"?>` declaration;
- UTF-8 without a byte order mark, NFC text, LF only, and one final newline;
- required namespace declarations on the root, default first and named prefixes lexicographically;
- two-space indentation, no tabs or blank structural lines, and one child per structural line;
- each container start and end tag on its own line and each text-only leaf on one unwrapped line;
- attributes ordered by expanded name and empty elements written exactly as `<name />`.

Parse-to-typed-tree-to-serialization must reproduce the stored bytes. Structural indentation is not
typed content; text-leaf whitespace remains exact. Minified structural XML, alternate indentation,
line wrapping, attribute order, namespace placement, or empty-element spelling fails. `check`
enforces this law but never rewrites the manually maintained XML.

Integrity is deliberately narrow. Stored PDFs, assets, and convenience derivatives retain raw
SHA-256 bindings because their exact bytes matter. Generated representations use fresh byte
comparison, not stored digests. A content-sensitive item digest is
`sha256/typed-item-v1:<64-lowercase-hex>`, computed over one `c1` JSON record containing exactly
`digestDomain="aa11393:ssp:typed-item:v1"`, `authorityScheme`, `schemaProfile`, `documentId`,
`itemId`, `itemType`, `typedContent`, and `substantiveMetadata`. `c1` uses UTF-8 JSON, NFC keys and
strings, standard JSON escaping with non-ASCII preserved, object keys in Unicode code-point order,
semantic array order, integers within ±9,007,199,254,740,991, compact separators, no floats, and one
final LF. XML formatting, paths, mechanical envelope fields, unrelated document metadata,
generator versions, and sibling items are excluded. No XML-wide semantic digest is kept merely
because an artifact was parsed.

The canonical manifest binds the stored PDF path, raw digest, byte size, evidentiary role, copy
status, extraction method, assets, and each declared convenience derivative. A convenience
derivative is expressly non-authoritative and cannot supply transcription content or provenance.
The registered stored-source path ends in `.pdf`, its bytes begin with the PDF format signature,
and the manifest has the exact current source-manifest name. Those checks prove only container and
registration consistency; they do not prove PDF authenticity, source fidelity, or transcription
fidelity. No command writes the PDF, transcription XML, manifest, or registered source asset.

## 5. Projection and computed coverage

The current renderer deterministically projects the validated transcription XML to Markdown. The
registered Markdown bytes must equal fresh rendering. Generated anchors preserve the XML stable
item identities, and assets resolve only through the manifest.

Coverage is computed from the current snapshot and proves:

- every transcribed content item has exactly one applicable provenance record;
- provenance source paths equal the manifest-bound PDF path;
- the document-root anchor precedes the first top-level content block;
- top-level content anchors follow XML document order;
- every transcribed content item has exactly one stable generated Markdown anchor inside the line
  region of its top-level projection owner; and
- every used asset is declared exactly by the manifest and package.

The top-level projection owner of an item is the top-level XML content child that contains it. Its
Markdown region begins at that top-level anchor and ends immediately before the next top-level
anchor or the review-metadata section. The verifier derives anchor lines and owner regions directly
from the XML and generated Markdown. Anchor presence, a matching Markdown digest, or a
renderer-supplied region cannot establish placement or hierarchy.

The verifier independently recomputes the complete ordered field census from the validated XML; a
renderer-produced coverage value cannot validate its own region. The recomputed census checks readable
serialization, manifest raw bindings, typed-item digests, Markdown byte identity, field identity
and origin, classification, anchors, line regions, and each required derivation or justification.
Together with the item/provenance and dependency/asset censuses, a missing, extra, duplicate,
reordered, or stale field or projection fails.

Coverage is validation evidence, not a stored package companion. An undeclared coverage file or a
missing or stale generated view fails.

## 6. Retained-worktree consumer-neutral handoff

A declared consumer edge selects exactly one registered representation, `xml` or `markdown`, and
cannot read the other representation through an undeclared dependency. An XML handoff supplies the
authority scheme, transcription role, complete typed item surface, metadata, provenance,
uncertainty, dependencies, assets, hierarchy, order, manifest raw bindings, and typed-item digests.
A Markdown handoff supplies only the declared review representation and receives no XML item
surface or source assets.

An acceptable retained worktree capture supplies a nonempty internal digest, the worktree root, a closed path
inventory, and retained bytes addressable through that inventory. A digest string, pass result, or
other detached token is not a snapshot. Every package-validation and declared-dependency path in a
handoff must occur in the snapshot inventory, and its validated bytes must equal the retained
snapshot bytes exactly.

Technical status attaches only to the validated item graph over the exact retained capture bytes. Before a
consumer constructs a semantic model or writes an output, package, schema/profile, item/field
census, hierarchy, order, provenance, dependencies, assets, manifest raw bindings, typed-item
digests, generated representation, and coverage must all pass. The consumer receives those same
validated bytes and may mechanically look up items, traverse declared hierarchy and order, select
declared fields, and resolve registered dependencies. It may not reopen a different path, accept a
detached pass token, or infer missing semantics. An unresolved lookup or traversal fails; it cannot
be converted to a default value, empty collection, inferred leaf, or fallback representation.

Package validation constructs and transitively freezes the representation bytes, complete typed
surface, nested typed content and metadata, dependencies, assets, and handoff mappings. The handoff
uses that validated state without reopening even the same live path or reconstructing semantics
from a later read, and exposes the exact validation-read census for the edge.

Each parsed representation, surface, coverage result, package result, and handoff belongs to one
retained capture and one generated-output state. Immutability prevents mutation but never permits
reuse after a generated-output replacement. Replacement ends the lifetime of every affected
derived object; subsequent validation constructs new surfaces, results, and handoffs even when the
replacement bytes equal the prior bytes. Retained control bytes remain captured inputs, while each
strict validator is freshly compiled and never handed across that boundary.

Selection of a representation never changes authority. The consumer may not reparse the PDF or an
OCR derivative as a substitute, infer missing content, add source-domain fields, silently fall
back, or promote XML or Markdown above the stored PDF's fidelity authority. The XML contains no
consumer-specific layout, styling, interaction, control-flow, or release fields. Product behavior,
presentation, interaction, security, release, and delivery are outside this contract.

## 7. Component commands, writes, and aggregate validation

The structured-source component command surface is exactly `check <subject-id>`, `regenerate
<subject-id>`, and `regenerate-controls`. It exposes no aggregate command or alias.

For this scheme, `check` validates one package and its declared dependencies without writing, and
`regenerate` validates authority-side inputs before replacing only that package's generated
Markdown. `regenerate-controls` first assembles one closed map of every candidate output path and
byte sequence, overlays that map on the retained unchanged controls, and freshly loads and strictly
compiles the complete candidate parser-control set. Candidate profile, generated XSD, independent
semantic invariants, and every shared schema must agree before the first write; the candidate
control object is then discarded. A post-write check or rollback cannot substitute for this
pre-write proof.

One atomic transaction may replace only a passing candidate map: the profile-generated content
XSD, derived routers, and the three acceptance table regions. Before success, the transaction
reopens every output path, compares every byte with the candidate map, and then freshly loads and
strictly compiles the complete parser-control set using only the replacement-path reader. A byte
mismatch or fresh-load failure restores the complete exact prestate; partial replacement is never
current. Externally changed authority or guard bytes are preserved and cause refusal. Replacement
validation cannot reuse a candidate object, pre-write control or pass token, parsed representation,
semantic surface, coverage result, package result, handoff, cached semantics, or validator. No
rollback receipt, recovery record, or alternate retained state is produced. Coverage remains
computed and is never persisted.

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
content registry's PDF-transcription slice, authoritative profile grammar, generated content XSD,
grammar renderer, parser and independent semantic invariants, manifest validator, renderer,
item-surface builder, exhaustive artifact classifier, immutable-snapshot handoff, focused tests,
registered consumers, and registered packages are the complete live implementation. The immutable
retained worktree capture must contain the exact named domain artifacts and every required shared
implementation path. Every snapshot path has exactly one current artifact class and one exact
class policy; an unknown class, role, or policy fails.

The contract pair, data-only acceptance registry, registry slice, controls, implementation,
focused tests and vectors, generated review state, and declared handoffs are accepted only as one
retained current state. A contract-only, registry-only, implementation-only, test-only,
generated-only, or handoff-only state fails. Any operative field, grammar, command, or handoff
change must update every affected member of that state coherently.

Required shared implementation closure is transitive. It includes every module required by this
domain or a declared consumer boundary, every schema those modules use, the shared aggregate
launcher, and every registered test and required test vector. Over the complete retained capture,
the closure enforcer recomputes all implementation-code, contract, schema, and required-vector
paths wherever they occur and compares those censuses exactly with the live implementation
inventory. The exact
`structured_source/` subtree census is an additional check, never a substitute for capture-wide
closure. Every captured domain test module has exactly one current registration, and every
registered test executes without skip, expected failure, or inactive registration. A directly
named subset, path convention, import success, or runtime reachability alone cannot establish
closure; an absent, additional, alternate, inactive, or contradictory implementation, contract,
registry, schema, launcher, test, vector, generated representation, or handoff fails.

Structural retired-implementation checks inspect parsed code, executable controls, and only code
spans, fenced code, and link targets in operative documentation. Authority content, generated
evidence reviews, generated products, test fixtures, and natural-language prose are never rejected
for containing text that resembles an implementation term; no raw repository-wide token scan or
content-specific suppression exists.

No alternate transcription, OCR-authority path, independently authored content XSD, prior-profile
reader, production parser-control bypass, second item-surface builder, mutable handoff,
compatibility or migration reader, approval or reviewer record, stored receipt, digest ledger,
coverage store, export path, or inactive domain artifact remains operative. Git alone retains
implementation history.

The focused negative suite rejects at least: a nested item anchor moved outside its top-level owner
even when renderer coverage and the Markdown digest are updated; omitted, null, or unresolved
traversal IDs and representation of an absent item as an empty leaf; publication after candidate
parser-control loading fails; replacement-byte mismatch or fresh replacement-control loading
failure without complete rollback; a missing or extra shared module, schema, launcher, registered
test, or vector anywhere in the retained capture; and reuse of a pre-replacement surface, result,
handoff, semantic object, or validation state.
