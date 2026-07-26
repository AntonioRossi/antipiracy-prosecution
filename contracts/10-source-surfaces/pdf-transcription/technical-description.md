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
| Semantic digest | Snapshot-computed, item-local digest covering identity, type, profile, content, and substantive metadata |
| Relation endpoints | Inapplicable to this content scheme; relations are owned by a relation package |

Stable identity, source numbering, mechanical ordering, and display labels are separate. Insertion,
deletion, or reordering may change a mechanical ordinal but cannot silently rename an item. A page
number or generated anchor can assist review but cannot substitute for the item ID in a machine
reference.

### Controlled semantic and metadata evolution

Adding or changing a transcription field requires one coherent current-state update to its
manually maintained XML owner, schema/profile, parser and renderer, item-digest rule, computed
coverage, declared consumer requirements, and focused positive and negative tests. If the field
affects a manifest, asset, provenance record, or reference, that binding changes in the same update.

An unknown field, arbitrary extension map, untyped metadata bag, renderer-only interpretation, or
field present without one declared owner fails closed. Consumer convenience cannot justify adding
source-domain semantics to a generated representation.

## 4. XML and manifest contract

Transcription XML uses the exact current namespace, XSD, and profile; UTF-8 XML 1.0; LF line
endings; NFC text; and the secure parser. DTDs, non-predefined entities, external resources,
XInclude, XLink, comments, processing instructions, CDATA, `xml:base`, recovery, duplicate IDs,
unknown fields or versions, aliases, and resource-limit violations fail closed.

Each artifact receives a raw stored-byte digest and a domain-separated canonical semantic digest
computed from the immutable snapshot. Item digests cover stable identity, type, profile, semantic
content, and substantive metadata while excluding presentation, paths, unrelated document
metadata, generator versions, and sibling items.

The canonical manifest binds the stored PDF path, raw digest, byte size, evidentiary role, copy
status, extraction method, assets, and each declared convenience derivative. A convenience
derivative is expressly non-authoritative and cannot supply transcription content or provenance.
No command writes the PDF, transcription XML, manifest, or registered source asset.

## 5. Projection and computed coverage

The current renderer deterministically projects the validated transcription XML to Markdown. The
registered Markdown bytes must equal fresh rendering. Generated anchors preserve the XML stable
item identities, and assets resolve only through the manifest.

Coverage is computed from the current snapshot and proves:

- every transcribed content item has exactly one applicable provenance record;
- provenance source paths equal the manifest-bound PDF path;
- every transcribed content item appears under its stable generated Markdown anchor; and
- every used asset is declared exactly by the manifest and package.

Coverage is validation evidence, not a stored package companion. An undeclared coverage file or a
missing or stale generated view fails.

## 6. Snapshot-bound consumer-neutral handoff

A declared consumer edge selects exactly one registered representation, `xml` or `markdown`, and
cannot read the other representation through an undeclared dependency. An XML handoff supplies the
authority scheme, transcription role, complete typed item surface, metadata, provenance,
uncertainty, dependencies, assets, hierarchy, order, and digests. A Markdown handoff supplies only
the declared review representation.

Trust attaches only to the validated item graph over the exact immutable snapshot bytes. Before a
consumer constructs a semantic model or writes an output, package, schema/profile, item/field
census, hierarchy, order, provenance, dependencies, assets, digests, generated representation, and
coverage must all pass. The consumer receives those same validated bytes and may mechanically look
up items, traverse declared hierarchy and order, select declared fields, and resolve registered
dependencies. It may not reopen a different path, accept a detached pass token, or infer missing
semantics.

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
persisted.

The repository-global gate owns immutable snapshot bracketing, registered isolated tests, final
snapshot revalidation, and the aggregate result. This domain contributes its own acceptance
statuses without defining any consumer product outcome.

## 8. Live implementation closure

This technical description, its acceptance criteria, its data-only acceptance registry, the
content registry's PDF-transcription slice, current schemas and profiles, manifest validator,
renderer, focused tests, and registered packages are the complete live implementation.

No alternate transcription, OCR-authority path, compatibility or migration reader, approval or
reviewer record, stored receipt, digest ledger, coverage store, export path, or inactive domain
artifact remains operative. Git alone retains implementation history.
