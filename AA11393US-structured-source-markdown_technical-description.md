# AA11393US — Structured-Source Markdown Technical Description

> **OPERATIVE INTERNAL CONTROL · NOT FOR FILING**
>
> This document defines the current authority direction, uniform XML machine interface,
> deterministic representations, exact references, and repository-based audit boundary for the
> AA11393US prosecution corpus. The coupled acceptance contract is
> [`AA11393US-structured-source-markdown_acceptance-criteria.md`](AA11393US-structured-source-markdown_acceptance-criteria.md).

## 1. Purpose and assurance boundary

XML is the repository's uniform, typed, item-addressable machine representation. It provides stable
identities, closed metadata, provenance, semantic digests, and exact cross-reference endpoints for
registered machine consumers, including navigator HTML5 generation.

XML's interface role does not make it universally authoritative. Authority remains package-specific:

```text
PDF authority ──manual transcription──▶ transcription XML ──▶ generated Markdown
Markdown authority ──conversion───────▶ generated XML ──▶ non-stored back-render check
Relation XML authority ───────────────────────────────────▶ generated Markdown

each validated XML representation ──read-only──▶ registered machine consumer
```

Generated representations expose, structure, or transform information but never become an
additional authority. A consumer's selected representation identifies the bytes it reads and does
not change authority.

Git identifies the operative committed bytes and their history. The global gate proves
machine-verifiable identity, schema validity, reference closure, conversion completeness, and
determinism. Neither Git nor the gate proves human attention, PDF transcription fidelity, source
authenticity, substantive or legal correctness, counsel approval, filing readiness, or filing
authorization.

The implementation uses the content registry, current schemas and profiles, computed coverage,
tests, Git, and the repository-global gate. It adds no approval system, auxiliary registry, digest
ledger, stored receipt, workflow engine, or generic code-ownership or reachability framework.

## 2. Package authority and representation model

Each package declares exactly one `authorityScheme` in the content registry:

| `authorityScheme` | Governing authority | XML role | Markdown role |
|---|---|---|---|
| `pdf-evidence-transcription-v1` | The package's one stored PDF governs source fidelity | Manually asserted transcription, provenance, and permitted metadata | Generated review representation |
| `authored-markdown-v1` | Authored Markdown | Generated structured representation | Authority |
| `authored-relations-v1` | Applicant-authored relation XML | Authority | Generated review representation |

Every package exposes exactly one registered `xmlFile` through the uniform XML interface. Uniform
means one registry slot, resolver, identity model, and validation contract; it does not require one
namespace, schema, or authority role for every package.

Package fields contain file IDs resolved through the registry's existing file table:

- PDF packages have one `storedSourceFiles` entry, one manually maintained `xmlFile`, one generated
  `markdownFile`, and one `sourceManifestFile`;
- authored-Markdown packages have one authoritative `markdownFile`, one generated `xmlFile`, and
  no second Markdown owner; and
- relation packages have one authoritative `xmlFile` and one generated `markdownFile`.

Coverage is computed and validated from the current snapshot for every package; it is not a
mandatory stored package companion and the package registry has no `coverageFile` field. A
human-facing coverage view may be generated on demand outside the live tree or retained as a
declared downstream-consumer output only when currently used. Such an output is owned by that
consumer's output contract and must reproduce the computed coverage deterministically. Otherwise
no stored coverage artifact exists.

Every consumer-to-package edge declares exactly one current `inputRepresentation`, either `xml` or
`markdown`, and reads only that representation. Separately declared non-representation
dependencies cannot point to the package's other representation. Each declaration must match actual
reads and cannot infer authority from file type, path, conversion direction, or consumer
preference.

The registry does not cache package-content or generated-output digests. Verification computes
them once from the immutable snapshot. PDF manifests retain checksums needed to identify stored
evidence. The registry contains no approval fields or records.

## 3. Uniform XML item and metadata contract

Each addressable XML item exposes the fields applicable to its schema:

- stable document and item identity;
- item type, hierarchy, and order;
- exact content;
- typed metadata;
- provenance and uncertainty where applicable;
- semantic digest;
- dependencies; and
- relation endpoints.

Each scheme declares where stable item IDs are maintained:

- authored-Markdown IDs originate in the Markdown and are preserved in generated XML;
- PDF-transcription IDs originate in the manually maintained transcription XML; and
- relation IDs originate in the authoritative relation XML.

IDs are never derived from a line number, heading slug, XPath position, array index, visible text,
or current sort order. Generated Markdown anchors and downstream locators preserve or
deterministically derive from those stable IDs.

Every XML field has one owner:

| Field category | Governing source |
|---|---|
| PDF transcription, page/region provenance, and uncertainty | PDF-transcription XML, subject to the PDF's fidelity authority |
| Authored content, stable IDs, and substantive item metadata | Authored Markdown |
| Cross-document assertions and their semantic metadata | Authoritative relation XML |
| Schema/profile/version declarations stored in manually maintained XML | That XML |
| Mechanical envelope fields serialized in generated authored XML or generated views | Deterministic generator |
| Raw and semantic digests used for verification | Validator, computed from the snapshot rather than kept in a mutable ledger |

Generated XML contains no manually maintained region. Substantive metadata for an authored
Markdown package must originate in the authoritative Markdown or in a separately registered
authoritative relation package; it cannot be inserted only into generated XML. Arbitrary extension
maps, untyped fields, unclassified metadata, and competing owners fail closed.

Adding an item field requires one coherent update to its declared human-maintained source,
schema/profile, converter, coverage rule, registered consumers, and focused tests. Unknown fields
are never silently ignored.

## 4. Scheme-specific conversion

### 4.1 PDF evidence transcription

The stored PDF governs source fidelity. Its manifest binds the exact path, raw digest, byte size,
asserted evidentiary role and copy status, extraction method, assets, and any non-authoritative
OCR/searchable convenience derivative.

The XML is the repository's manually asserted transcription and item metadata, not a replacement
PDF authority. Every transcribed item has page/region provenance and any known uncertainty. The
machine verifies the PDF checksum, manifest, provenance structure, XML validity, coverage, and
XML-to-Markdown determinism. It does not claim that these checks prove the transcription faithful.

No command writes the PDF or transcription XML. OCR may assist inspection but cannot become an
authority or an automatically accepted source of content.

### 4.2 Authored Markdown

The Markdown contains all adopted content-bearing material, stable `ssp-*` item identities, and
substantive item metadata. It uses the one anchor syntax and closed GFM subset allowed by the
Markdown profile.

The pinned GFM parser generates typed XML. Rendering that XML back to the same pinned GFM semantic
form preserves the ordered Pandoc AST after only profile-listed presentational normalizations.
Those normalizations may cover line wrapping and equivalent escaping; they cannot remove, add, or
reorder content-bearing nodes, identities, links, claims, table cells, advisories, metadata, or
headings.

Only schema/profile/version data, authority bindings, generated digests, ordinals, and fields
explicitly classified as mechanical may exist solely in the generated XML envelope. The generated
XML is never manually edited and must equal fresh regeneration from Markdown.

### 4.3 Applicant-authored relations

Relation XML owns each applicant-authored cross-document assertion. It declares one semantic owner,
stable relation identity, type, direction, ordered fields, and exact
`(documentId, fragmentId, fragmentContentDigest)` endpoints.

Endpoints provide the assertion's evidence basis but do not adopt or authorize its conclusion.
Reusing one endpoint in several assertions is valid. Missing, duplicate within one assertion,
swapped-role, stale, ambiguous, or undeclared endpoints fail.

Generated relation Markdown exposes the scheme, authority role, assertion fields, ownership,
forward anchors, reverse endpoint links, current excerpts, and evidence basis. It never becomes a
second relation owner.

## 5. XML validity, identity, and coverage

Content and relation XML use their exact current namespaces, schemas, and profiles. Stored XML is
UTF-8 XML 1.0 and already NFC. The secure parser rejects DTDs, non-predefined entities, external
resources, XInclude, XLink, comments, processing instructions, CDATA, `xml:base`, recovery,
duplicate IDs, unknown constructs, and resource-limit violations. Earlier or unknown formats,
aliases, and compatibility readers fail closed.

Every XML artifact has a raw stored-byte digest and a domain-separated canonical semantic digest.
Derived XML binds its external authority path and raw digest. Relation XML never self-binds its own
digest.

Fragment digests cover stable item identity, type, profile, semantic content, and substantive item
metadata. They exclude file paths, presentation formatting, unrelated document metadata,
generator versions, and sibling items so unrelated changes do not stale an endpoint.

Mandatory computed coverage proves the applicable mappings:

- PDF transcription item → PDF provenance and generated Markdown;
- authored Markdown item → generated XML and semantic back-render; and
- relation assertion and field → generated Markdown and exact endpoints.

Content-bearing fields cannot be classified as mechanical or internal to avoid coverage.

Coverage is calculated from the current snapshot and does not require a stored artifact. Any
declared downstream coverage view must equal the same computation. An undeclared stored coverage
artifact, a missing declared consumer output, or a view that differs from computation fails.

## 6. Consumer and downstream contract

Review consumers use the declared Markdown representation: authoritative Markdown for authored
packages and generated Markdown for PDF and relation packages. Machine consumers that require typed
item identity, hierarchy, metadata, provenance, or relation resolution use the registered XML
representation when declared.

An XML consumer:

- reads through the registered resolver and secure parser;
- receives the package's authority scheme and XML role with every document;
- treats all inputs as read-only;
- preserves item identities and semantic relationships; and
- rejects undeclared files, fields, dependencies, endpoints, or representation fallbacks.

Representation changes are owned by the consumer's contract and registry edge. This upstream
contract validates the current declaration and does not duplicate downstream rendering,
interaction, accessibility, security, or release requirements. Direct XML consumption never
promotes a generated authored-package XML or PDF transcription above its declared authority.

## 7. Organization and references

Shared prosecution records have one owner under `US/common/`. Strategy material remains under
`US/normal-allowance/` or `US/allowance-first/`. Each prior-art ID has one co-located PDF,
transcription XML, generated Markdown, source manifest, and any declared convenience derivative.
Registered PCT packages retain their controlled locations.

Routers expose active packages without becoming semantic owners. All registered paths, links,
items, manifests, assets, controls, consumers, schemas, tests, and runbook references resolve
exactly. Aliases, symlinks, path escapes, silent merges, competing authorities, editable generated
files, and consumer-driven authority promotion are prohibited.

## 8. Commands and writes

The closed structured-source command surface is:

- `check <subject-id>` — validate one package and compare its generated files without writing;
- `regenerate <subject-id>` — regenerate only that package's permitted derived files;
- `regenerate-controls` — regenerate routers and the marked acceptance-table region; and
- `verify-callback` and `verify-current` — verify without writing.

`check` and `regenerate` always compute and validate package coverage but do not persist a package
coverage artifact. A currently declared downstream coverage-view consumer owns any retained view
under its own output and write rules.

There is no approval, reviewer, record-resolution, export, migration, compatibility, or implicit
bootstrap command. Package commands validate only their target and declared dependencies; they do
not repeat whole-corpus validation.

Commands validate before writing and replace each permitted generated file atomically. A detected
or catchable failure restores only command-owned bytes that have not been externally changed.
Authority files and external changes are never overwritten. Abrupt termination may leave a mixed
generated set; the gate detects it, and regeneration or Git repairs it.

## 9. Repository audit and current-state gate

The audit unit is:

```text
exact clean Git commit → repository checkout and supplied history
→ documentation pair and executable registries
→ current snapshot-bracketed validate-current result
```

Every required authority, representation, PDF, manifest, asset, schema, profile, policy, test, and
implementation file is Git-addressable at that commit. Controlled ignored or untracked files fail.

The exact host `uv`, Python, Pandoc, and locked project-local environment are pre-provisioned
prerequisites under the root README's Validation procedure. Recurring verification never
provisions or changes them.

`uv --no-cache --offline run --locked --no-sync python -m navigator validate-current` is the sole
repository-global gate. It captures one immutable snapshot, runs both registered test families in
isolation, revalidates the final snapshot, and reports the commit and snapshot identities. The
pre-test and final post-test phases each rebuild their indexes from the live bytes; no index crosses
the test boundary. Within either phase, package and consumer checks reuse one corpus-wide pass
instead of repeating it per package or consumer.

The result is ephemeral machine evidence. No detached archive, stored receipt, self-attestation, or
mutable external path substitutes for the exact checkout and current execution.

## 10. Live-contract and implementation closure

The operative structured-source contract is this technical description and its coupled acceptance
criteria. The executable acceptance registry maps each `SSM-AC` criterion to one callback, and
`regenerate-controls` projects that registry into the marked acceptance table.

Only registered implementation required by the three authority schemes, uniform XML interface,
consumers, and closed command surface remains. Structured-source approval, export,
implementation-register, migration, and compatibility paths do not exist or survive under new
names. Tests, fixtures, and helpers used only by those removed paths do not remain. Each current
format and conversion direction has one registered parser/converter pathway, and no consumer has
an undeclared reader.

Package-level coverage paths, registry fields, persistence handlers, comparisons, fixtures, and
tests do not remain. Coverage computation and validation remain mandatory; a retained coverage-view
renderer and its tests exist only as a currently declared downstream consumer.

The existing registries, targeted source/import/command scans, and current tests enforce closure;
no generic ownership or reachability subsystem is added. Git alone retains inactive history.
