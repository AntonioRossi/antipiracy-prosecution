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
generated Markdown is a review representation and never becomes another authority. OCR may assist
inspection but is not authoritative and cannot be accepted automatically.

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

The current profile is the exclusive executable inventory of document metadata, the item identity
attribute, item types and their permitted metadata, document order, source-number treatment,
provenance fields, dependency kinds, readable XML storage, and typed-item digest inputs. The XSD and
profile must agree exactly; neither independently authorizes a field omitted by the other.

Each dependency declares one kind and subject identity. Asset dependencies resolve by the exact
registered raw-byte digest. Document and relation-package dependencies resolve through their
registered validated interfaces; when exact content matters, the reference names the stable item
and its typed-item digest. No whole-XML digest substitutes for item-level content sensitivity. The
dependency and asset censuses must be unique and exact, their kinds must agree with the target
authority, and a dependency cycle fails.

### Controlled semantic and metadata evolution

Adding or changing a transcription field requires one coherent current-state update to its
manually maintained XML owner, schema/profile, parser and renderer, item-digest rule, computed
coverage, declared consumer requirements, and focused positive and negative tests. If the field
affects a manifest, asset, provenance record, or reference, that binding changes in the same update.

An unknown field, arbitrary extension map, untyped metadata bag, renderer-only interpretation, or
field present without one declared owner fails closed. Consumer convenience cannot justify adding
source-domain semantics to a generated representation.

## 4. XML and manifest contract

Transcription XML uses the exact current namespace, XSD, profile, secure parser, and readable
storage law. Every registered XML file must equal deterministic serialization of its validated
typed tree with:

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
- every transcribed content item appears under its stable generated Markdown anchor; and
- every used asset is declared exactly by the manifest and package.

The verifier independently recomputes the complete ordered field census from the validated XML; a
renderer-produced coverage value does not attest to itself. The recomputed census checks readable
serialization, manifest raw bindings, typed-item digests, Markdown byte identity, field identity
and origin, classification, anchors, line regions, and each required derivation or justification.
Together with the item/provenance and dependency/asset censuses, a missing, extra, duplicate,
reordered, or stale field or projection fails.

Coverage is validation evidence, not a stored package companion. An undeclared coverage file or a
missing or stale generated view fails.

## 6. Snapshot-bound consumer-neutral handoff

A declared consumer edge selects exactly one registered representation, `xml` or `markdown`, and
cannot read the other representation through an undeclared dependency. An XML handoff supplies the
authority scheme, transcription role, complete typed item surface, metadata, provenance,
uncertainty, dependencies, assets, hierarchy, order, manifest raw bindings, and typed-item digests.
A Markdown handoff supplies only the declared review representation and receives no XML item
surface or source assets.

An acceptable immutable snapshot supplies a nonempty digest, the checkout root, a closed path
inventory, and retained bytes addressable through that inventory. A digest string, pass result, or
other detached token is not a snapshot. Every package-validation and declared-dependency path in a
handoff must occur in the snapshot inventory, and its validated bytes must equal the retained
snapshot bytes exactly.

Trust attaches only to the validated item graph over the exact immutable snapshot bytes. Before a
consumer constructs a semantic model or writes an output, package, schema/profile, item/field
census, hierarchy, order, provenance, dependencies, assets, manifest raw bindings, typed-item
digests, generated representation, and coverage must all pass. The consumer receives those same
validated bytes and may mechanically look up items, traverse declared hierarchy and order, select
declared fields, and resolve registered dependencies. It may not reopen a different path, accept a
detached pass token, or infer missing semantics.

Package validation constructs and freezes the representation bytes and complete typed surface
before handoff. The handoff uses that validated state without reopening even the same live path or
reconstructing semantics from a later read, and exposes the exact validation-read census for the
edge.

Selection of a representation never changes authority. The consumer may not reparse the PDF or an
OCR derivative as a substitute, infer missing content, add source-domain fields, silently fall
back, or promote XML or Markdown above the stored PDF's fidelity authority. The XML contains no
consumer-specific layout, styling, interaction, control-flow, or release fields. Product behavior,
presentation, interaction, security, release, and delivery are outside this contract.

## 7. Commands, writes, and aggregate verification

The shared structured-source command surface remains exactly `check <subject-id>`, `regenerate
<subject-id>`, `regenerate-controls`, and `verify-current`.

For this scheme, `check` validates one package and its declared dependencies without writing;
`regenerate` validates authority-side inputs before atomically replacing only that package's
generated Markdown; `regenerate-controls` replaces only derived routers and the three acceptance
table regions; and `verify-current` participates in one memoized whole-corpus pass. Authority files
and externally changed bytes are never overwritten. Coverage is always computed and never
persisted. After an atomic generated-output replacement, every pre-replacement representation and
surface state is discarded and the replacement is read back and validated anew.

The repository-global gate owns immutable snapshot bracketing, registered isolated tests, final
snapshot revalidation, and the aggregate result. This domain contributes its own acceptance
statuses without defining any consumer product outcome.

## 8. Live implementation closure

This technical description, its acceptance criteria, its data-only acceptance registry, the
content registry's PDF-transcription slice, current schemas and profiles, manifest validator,
renderer, item-surface builder, immutable-snapshot handoff, focused tests, registered consumers,
and registered packages are the complete live implementation. The immutable repository snapshot
must contain the exact named domain artifacts and every required shared implementation path.

No alternate transcription, OCR-authority path, compatibility or migration reader, approval or
reviewer record, stored receipt, digest ledger, coverage store, export path, or inactive domain
artifact remains operative. Git alone retains implementation history.
