# Structured Content Authority and XML Machine-Interface Manifest

> **NON-OPERATIVE REUSABLE ARCHITECTURE GUIDE**
>
> **Purpose:** Define the simplest reliable model for exposing heterogeneous authoritative
> documents through a uniform XML machine interface while preserving authority, fidelity,
> metadata ownership, stable identity, and cross-reference integrity.

## 1. Core architecture and assurance boundary

A repository may contain heterogeneous authority sources, including immutable source PDFs,
authored Markdown, and narrowly scoped authored relation or metadata XML. XML gives registered
tools one uniform, typed, item-addressable interface over that content:

```text
scheme-specific authority
        │
        ▼
transcription or deterministic conversion
        │
        ▼
validated XML machine interface
        │
        ▼
registered consumers → derived products
```

The interface provides stable identities, closed metadata, provenance, typed-item digests,
dependencies, and exact cross-reference endpoints. Uniform means one registry slot, resolver,
identity model, and validation boundary for XML; it does not require one universal namespace,
schema, or conversion direction.

The XML interface is consumer-neutral. Registered consumers may include renderers, fixture
builders, indexers, cross-reference resolvers, search tools, and report generators. These are
examples, not purposes built into the XML model. A different repository may use the same model to
build fixtures by sourcing requirements and examples from authoritative documentation.

Each package has one governing authority, and every field has one declared owner. Human-authored
fields have one maintained owner; mechanical fields have one deterministic owner. XML's interface
role does not make XML universally authoritative. File type, conversion direction, or consumer
choice never changes authority. Generated representations and products may expose, structure, or
transform information, but they never become additional authorities.

Validation proves machine-checkable properties such as identity, schema validity, transformation
completeness, reference resolution, and deterministic output. It does not prove source
authenticity, PDF transcription fidelity, human attention, legal correctness, or approval.

## 2. Authority and conversion directions

| Document origin | Governing authority and maintained source | XML interface role | Markdown role | Direction |
|---|---|---|---|---|
| PDF-derived | Original PDF for source fidelity; XML for the repository's asserted transcription and provenance | Manually maintained structured transcription | Generated review representation | PDF → human/OCR-assisted XML transcription → Markdown |
| Authored Markdown | Markdown | Generated structured representation | Authority | Markdown → XML |
| Closed authored relations or metadata | Dedicated relation/metadata XML | Authority and interface for those schema-enumerated assertions only | Optional generated review representation | Relation/metadata XML → Markdown |

Every registered package declares exactly one authority scheme and one validated XML
representation. Its authority scheme declares the maintained source for stable item IDs. That
source may differ from the substantive authority: a PDF-transcription ID is maintained in
transcription XML while the PDF continues to govern fidelity.

Authoritative relation or metadata XML is permitted only for closed categories enumerated by the
current schema and profile. Inconvenience, presentation needs, or a consumer feature does not
justify moving ordinary authored content or metadata out of its existing authority.

OCR may assist PDF transcription but is never authoritative.

A generated XML file must not contain manually maintained regions. A generated Markdown file must
not be independently edited. Mixing generated content and manually maintained metadata in the same
file is prohibited.

## 3. XML interface, metadata ownership, and enrichment

Each XML representation exposes the fields applicable to its scheme:

- stable document and item identities;
- item type, hierarchy, order, and exact content;
- closed typed metadata;
- provenance and uncertainty where applicable;
- typed-item digests;
- declared dependencies; and
- typed relation endpoints where applicable.

Core XML describes document semantics rather than a consumer's output. It must not encode HTML
elements, CSS classes, DOM layout, fixture filenames, testing-framework syntax, report layout, or
consumer control flow. Consumer-specific mappings and mechanical derivations belong in the
consumer's own contract. A field used by a consumer belongs in core XML only when it expresses
source-domain semantics and has a declared owner.

Every metadata field must be classified by its actual origin:

- PDF provenance, page regions, transcription uncertainty, and extraction information belong in
  the manually maintained PDF-transcription XML.
- Metadata derived mechanically from authored Markdown belongs in the generated XML.
- Substantive metadata about authored Markdown must either be expressed in the authoritative
  Markdown or placed in a separate authoritative relation/metadata XML document.
- Generator versions, derived ordinals, and similar envelope fields belong to the deterministic
  generator. Raw verification digests and typed-item digests are computed by the validator. A
  relation endpoint records the target typed-item digest only as an exact content reference.
- No substantive information may exist only in generated XML.

Do not preserve manually edited metadata by merging it into regenerated XML. That creates mixed
ownership and makes regeneration unsafe.

Adding an item field requires one coherent update to its human-maintained owner, schema/profile,
transcription or converter where applicable, coverage rule, registered consumers, and focused
tests. Unknown fields, arbitrary extension maps, unclassified metadata, and competing owners fail
closed. Generic reuse comes from the typed interface, not from an untyped extension mechanism.

## 4. Stable identity and cross-references

Every addressable document entry has:

- a stable document ID;
- a stable entry ID originating in the maintained source declared by its authority scheme;
- a declared entry type; and
- typed metadata allowed by the current schema.

Authored-Markdown IDs originate in Markdown, PDF-transcription IDs originate in the maintained
transcription XML, and relation IDs originate in the authoritative relation XML. ID location never
changes substantive authority.

Generated Markdown exposes the same IDs through one declared anchor syntax.

Cross-references use document and entry IDs, never file line numbers, generated heading slugs, list
positions, or XPath expressions dependent on incidental layout.

A semantic assertion that depends on the exact target content also records the target entry's
typed-item digest. Navigational links may use IDs alone.

Entry typed-item digests cover stable identity, item type, schema/profile, typed content, and
substantive item metadata. They exclude presentation formatting, file paths, unrelated document
metadata, generator versions, and sibling entries so that unrelated changes do not invalidate
references.

Duplicate IDs, unresolved targets, stale typed-item digests, ambiguous owners, and unsupported
reference types fail validation.

## 5. Conversion requirements

### PDF-derived documents

The system must:

- preserve the original PDF unchanged;
- verify its checksum and source manifest;
- require page or region provenance for every transcribed entry;
- record known transcription uncertainty;
- validate the XML against the current schema;
- generate Markdown deterministically from XML; and
- make the PDF, XML, and Markdown available for audit.

The system must not claim that checksums, schema validation, OCR, or deterministic rendering prove
transcription fidelity.

### Authored Markdown documents

The system must:

- preserve stable entry IDs in the authoritative Markdown;
- accept only the declared Markdown subset;
- generate typed XML deterministically;
- reject unsupported or lossy constructs;
- verify that Markdown → XML → Markdown preserves the semantic document structure;
- compare semantic trees after only explicitly permitted presentational normalization; and
- reject generated XML that differs from regeneration.

The conversion must preserve headings, paragraphs, lists, tables, claims, links, advisories,
identifiers, ordering, and all other content-bearing structures.

It must not create or require a second independently editable Markdown representation.

### Authored relations and metadata

Only relation or metadata categories explicitly enumerated by the current schema and profile may
have one dedicated authoritative XML document.

Such XML must:

- identify one semantic owner for every assertion;
- use typed and directional relations;
- reference exact document and entry IDs;
- detect content-sensitive target changes through typed-item digests; and
- generate any human-readable view deterministically.

Endpoint documents do not become authorities for assertions made about them.

## 6. Registered consumers and repository controls

After scheme-specific transcription or conversion, a production semantic consumer reads the
validated XML interface rather than reparsing PDF, OCR, or Markdown. A declared review-only
consumer may present authoritative or generated Markdown but cannot supply a production semantic
pipeline. Human reviewers may inspect the source authority or a generated Markdown view.
Converters that create XML read the authority declared by the package scheme and are not alternate
downstream content readers.

Every consumer edge declares its consumer, package, input representation, required fields,
dependencies, and authority scheme/representation role. Production semantic edges declare XML;
review-only edges may declare Markdown. A consumer reads only those declared inputs, preserves
stable identities and provenance, and rejects undeclared files, fields, dependencies, aliases, and
representation fallbacks. Consuming a representation or producing a derivative never promotes it
above the package's authority.

For example, a fixture builder may select schema-typed requirement and example items and emit
fixtures that retain their exact source IDs and typed-item digests. An HTML renderer may map the same
interface to accessible navigation. Neither output becomes authority, and neither use case may add
consumer-specific structure to core XML. Output behavior, presentation, framework syntax, QA, and
release requirements belong in the consumer's own contract.

Use the registry that owns each package to declare:

- document ID;
- authority scheme;
- authority file;
- XML representation;
- Markdown representation;
- schema and conversion profile;
- source PDF and manifest where applicable;
- dependencies and cross-reference endpoints; and
- declared consumer edges and required interface fields.

Do not duplicate a package across parallel registries. Consumer-owned XML may remain in the
consumer's existing registry outside an upstream package registry; exact cross-boundary consumer
edges connect them without copying authority declarations.

Do not create parallel authority registries, digest ledgers, approval inventories, stored
validation receipts, or per-package workflow records.

Digests derivable from the current repository snapshot should be calculated during validation
rather than copied into another mutable registry. Source manifests may retain checksums needed to
identify external evidence such as PDFs.

## 7. Command and write boundary

Keep the command surface small:

- validate one document without writing;
- regenerate one document's derived files;
- validate the complete current repository; and
- regenerate genuinely derived control files, if any.

Commands must never write an authority file.

Document-level commands validate only their target and declared dependencies. Each pre-test or
final post-test repository-validation phase builds fresh shared indexes from current bytes and does
not repeat a full-corpus pass for every document or consumer. No pre-test index crosses the test
boundary.

Generated files are validated before publication and replaced atomically. A detected failure must
not overwrite authority files or unrelated external changes.

Validation must not install dependencies, access the network, mutate the environment, or silently
fall back to unpinned tools.

## 8. Audit and history

The audit unit is:

```text
exact clean Git commit
→ repository checkout and history
→ authority declarations and documentation
→ current repository-wide validation result
```

Git is the sole history for superseded content, implementation, and validation state.

The live checkout contains only current authorities, current generated representations, current
schemas, current configuration, and current implementation.

Do not retain:

- self-approval or reviewer records;
- superseded validation records;
- implementation registers;
- migration reports or compatibility paths;
- lesson, status, or issue logs presenting obsolete state;
- detached audit ZIP files;
- stored validation receipts;
- stale generated files; or
- renamed equivalents of removed mechanisms.

## 9. Implementation simplicity

Use the existing registry, schemas, conversion profiles, tests, Git history, and repository-wide
gate.

Keep the XML model consumer-neutral and scheme-specific. Do not create a universal document schema,
consumer plug-in framework, or consumer-specific fields in the core merely to call the system
generic.

Do not introduce:

- a workflow engine;
- a second authority database;
- a digest ledger;
- per-document approval ceremonies;
- a generic code-ownership framework;
- a generic reachability-analysis subsystem;
- backward-compatible readers for retired formats;
- automatic migration during validation; or
- package exports that duplicate the repository checkout.

Only code required by the current authority schemes and command surface remains. Obsolete handlers,
compatibility branches, duplicate conversion paths, unused helpers, and tests serving only removed
behavior must be deleted.

## 10. Minimum acceptance conditions

The implementation is complete only when:

1. Every package declares exactly one authority scheme with one maintained stable-ID source, and
   one validated XML representation.
2. Every package has one governing authority; every field has one declared maintained or
   deterministic owner and a closed schema type.
3. XML presents the scheme's stable items, metadata, provenance, dependencies, and relations
   without consumer-specific output structure.
4. Every production semantic consumer reads only its declared XML interface and dependencies;
   every review-only Markdown edge is explicit and cannot feed that semantic path.
5. Authority files are never command outputs, and all generated files equal fresh deterministic
   regeneration.
6. Every PDF transcription entry has source provenance and disclosed uncertainty; validation does
   not claim to prove fidelity.
7. Authored Markdown survives the declared semantic round trip without content loss.
8. Every stable ID is unique, every cross-reference resolves, and content-sensitive references
   fail when their target content changes.
9. Unknown schemas, formats, fields, authority schemes, consumer inputs, and conversion paths fail
   closed.
10. No approval system, export bundle, compatibility layer, stale artifact, parallel authority
    store, or auxiliary history remains.
11. Per-document or per-consumer checks do not repeatedly validate the entire corpus, and final
    validation rebuilds its indexes from current bytes.
12. One repository-wide command verifies one unchanged snapshot and reports only
    machine-conformance claims.

## Adoption

This manifest is reusable design guidance, not an operative repository contract. A target
repository adopts it by folding sections 1–9 into its technical description and section 10 into its
executable acceptance criteria. That operative pair and registry then control. Remove a copied
standalone manifest after integration so it does not become a third source of truth.
