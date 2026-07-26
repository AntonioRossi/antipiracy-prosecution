# AA11393US — Interactive Claims-to-Specification Navigator: Technical Description (DRAFT)

> **CURRENT IMPLEMENTATION CONTRACT · INTERNAL DRAFT**
>
> This document defines the two current, standalone claims-to-specification navigator
> products and the architecture that generates them. It states current required behavior
> only. The coupled [`acceptance criteria`](acceptance-criteria_DRAFT.md) are projected in
> [`navigator/schema/acceptance.json`](../../../navigator/schema/acceptance.json).

The navigator uses **XML as the one uniform machine interface** to the repository content it
consumes. XML supplies stable item identities, hierarchy, typed metadata, provenance, semantic
digests, dependencies, and exact relation endpoints. XML does not become universal source
authority: each package retains the authority direction declared for its content class.

## 1. Purpose and legal boundary

Each navigator lets US prosecution counsel answer two questions:

1. Which disclosure passages are recorded as candidate associations for this claim fragment?
2. Which claim fragments are indexed to this disclosure passage?

The NA and AF editions present alternative claim strategies. Inclusion of both expresses no
comparison, preference, equivalence, or filing recommendation. Each edition is a navigation aid,
not a legal-opinion or filing-authority system.

The navigator presents author-recorded candidate associations, honest no-candidate states,
source-derived cautions, and unresolved dispositions. It does not determine or imply written-
description support, enablement, new matter, priority entitlement, permissible amendment scope,
claim construction, definiteness, Section 112(f) treatment, patentability, validity,
infringement, filing readiness, allowance likelihood, examiner behavior, or whether separately
disclosed passages may legally be combined. It does not infer mappings or transfer them between
strategies. It provides no editing, collaboration, access-control, encryption, or secure-document-
management function.

The current product profile is `technical-preview`. Every screen, no-JavaScript view, printed
page, and bundle manifest carries this exact label:

> **TECHNICAL PREVIEW — Manual cross-platform and assistive-technology QA is deferred;
> browser and assistive-technology compatibility is not validated.**

Automated content, transformation, interaction-model, accessibility-structure, security,
offline, deterministic-output, and bundle-integrity checks remain mandatory. The profile makes
no browser, operating-system, print-engine, or assistive-technology compatibility claim.

## 2. Authority and XML architecture

### 2.1 Authority is package-specific

The machine path is uniform while authority direction remains explicit:

```text
package-specific authority
        │
        ▼
validated current XML ──read-only──▶ navigator gateway
                                         │
                                         ▼
                              immutable typed model
                                         │
                                         ▼
                              deterministic HTML5
```

| Content class | Governing authority | XML role |
|---|---|---|
| PDF-derived package | Stored source PDF for fidelity | Asserted transcription and validated runtime representation |
| Authored-content package | Authored Markdown | Generated, round-trip-validated runtime representation |
| Upstream authored relation package | Applicant-authored relation XML | Authoritative upstream assertions and validated runtime representation |
| Navigator relation package | Navigator-owned relation XML | Authority for navigator-only associations |
| Navigator wording package | Navigator-owned wording XML | Authority only for controlled semantic or security-relevant wording |
| Typed model and HTML5 | No independent authority | Ephemeral model and deterministic products |

For PDF-derived packages, generated Markdown is a human review view derived from the XML and is
not a runtime source. For authored packages, conversion completeness and semantic round-trip are
proved between authoritative Markdown and generated XML before the navigator consumes the XML.

Every navigator semantic consumer edge declares XML as its input representation. Choosing XML
selects the machine-readable bytes; it never changes the governing authority. Generated HTML
provenance preserves the package authority scheme and XML role.

A defect is corrected at its authority:

- authored content is corrected in Markdown and XML is regenerated;
- a PDF transcription or provenance defect is corrected in transcription XML against the PDF;
- an upstream relation is corrected in its authoritative relation XML; and
- navigator-only relations or controlled wording are corrected in navigator XML.

Generated XML, the typed model, and HTML5 are never patched to conceal an upstream defect.

### 2.2 One read-only gateway

All production semantic reads pass through one registered gateway. For one immutable repository
snapshot, the gateway:

1. resolves the declared consumer inputs and their package authority schemes and XML roles;
2. secure-parses only registered current XML;
3. validates schemas, namespaces, versions, identities, hierarchy, metadata, semantic digests,
   dependencies, relation endpoints, assets, wording entries, and controlled slot origins;
4. records the ephemeral exact read set; and
5. constructs and seals one immutable in-memory model before rendering.

The gateway rejects undeclared files, symlinks, path escapes, external resources, unknown fields
or versions, duplicate IDs or semantic owners, digest drift, unresolved dependencies, stale or
ambiguous endpoints, invalid wording slots, and representation fallbacks.

The model exposes one narrow typed API equivalent to:

```text
getDocument(documentId)
getItem(documentId, itemId)
getMetadata(documentId)
resolveRelation(relationId)
relationsFor(documentId, itemId)
```

Metadata in this pseudo-API is document metadata. Item properties are returned by `getItem`.

The renderer receives only this sealed model and declared presentation resources. Production
renderers do not parse XML, Markdown, PDF/OCR text, semantic JSON, caches, aliases, migration
files, or network resources. The model is never persisted as a semantic store. It may select and
order declared fields, but cannot rewrite substantive text, repair dependencies, infer or retarget
relations, promote an endpoint's authority, or invent controlled wording.

### 2.3 Navigator-owned XML

The navigator owns exactly one relation package per edition:

```text
navigator/relations/na__pct.relations.xml
navigator/relations/af__pct.relations.xml
```

They use `schemaProfile="navigator-claim-pct-relations-v1"`; each file's `relationSetId` and
`edition` declare its navigator ownership scope. They own only navigator-specific associations and
may reference an upstream assertion by stable relation ID; they do not restate or override
source-level support, priority, prior-art, comparison, mapping, or crosswalk assertions.

Controlled navigator wording is owned by:

```text
navigator/wording/shared.wording.xml
navigator/wording/na.wording.xml
navigator/wording/af.wording.xml
```

These packages use `schemaProfile="navigator-controlled-wording-v1"`; each file's `wordingSetId`
and `scope` declare shared or edition ownership. They contain only exact wording with substantive,
provenance, caution, disposition, disclaimer, profile, artifact, manifest, or security meaning.
Ordinary navigation labels, buttons, headings, help, and layout instructions remain owned by
tracked templates or code.

Each controlled entry has a stable `wordingId`, locale, ownership scope, closed usage contexts,
fixed text, and only the typed slots actually required. A slot declares its name, scalar type,
and one exact origin; every slot is rendered as escaped plain text. Runtime strings, alternate
origins, raw HTML, executable templates, arbitrary extension maps, and generic safe-content
bypasses are forbidden.

### 2.4 Computed coverage and origin tracing

Conversion and reference coverage are computed during validation. The validator proves that every
required consumer item is present, every dependency and relation endpoint resolves exactly, and no
undeclared semantic source was read. Coverage is not maintained as a separate committed artifact.

The validator computes a non-stored, per-value origin inventory over the sealed typed semantic
state for:

- source-derived content, IDs, metadata, and provenance;
- relation endpoints and relation semantics;
- controlled wording and every slot value;
- security-sensitive dynamic values; and
- registered feature-driving fields or closed derivations.

Every covered value resolves to an XML item and its authority scheme, navigator XML entry,
registered control, typed interaction-state field, or closed mechanical derivation. Ordinary
template/code copy is excluded because its tracked source file is already its owner. The computed
inventory includes paired bundle-wording slot and bundle-control origins when both editions are
available. Tests separately compare the substantive typed relation values with their rendered
counterparts. The inventory is ephemeral evidence, never embedded in a product or committed as a
lineage file, receipt, or product manifest.

## 3. Current editions and product profile

The shared rendering kernel is edition-blind. Edition-specific content and behavior come from
validated typed data, not conditionals embedded in shared rendering code.

| Property | NA edition | AF edition |
|---|---|---|
| Strategy | Normal-allowance | Allowance-first |
| Claim-set version | `NA-2026-07-22-v4` | `AF-2026-07-22-v6` |
| Claims | 30 | 23 |
| Selectable units | 77 | 61 |
| Independent claims | 1, 9, 16, 22 | 1, 19, 23 |
| Claim groups | 4 | 10 |
| Largest decompositions | Claim 22: 14 units; claim 9: 9 | Claims 1 and 19: 14 units; claim 23: 8 |
| Display prefix | `NA claim N` | `AF claim N` |
| Navigator relations | `navigator/relations/na__pct.relations.xml` | `navigator/relations/af__pct.relations.xml` |
| Forbidden authored UI term | None | `camera-cut timing pattern` |
| HTML artifact | `AA11393US-NA-claims-spec-navigator_NA-2026-07-22-v4.html` | `AA11393US-AF-claims-spec-navigator_AF-2026-07-22-v6.html` |

Edition rules are closed:

- each edition produces one standalone HTML file;
- there is no edition toggle, merged view, hybrid claim set, or cross-edition inheritance;
- AF relations are authored independently from NA relations;
- a single-edition build reads only shared inputs and that edition's declared inputs;
- all displayed claim references outside verbatim claim text carry `NA`, `AF`, or `PCT`;
- AF's `camera-source-transition pattern` is not treated as synonymous with NA's
  `camera-cut timing pattern`;
- the complete current claim set is displayed, including all 23 AF claims; and
- an edition-specific defect does not alter the other edition, while a shared-input defect
  correctly blocks both.

## 4. Item, claim, and relation model

Every consumed XML item preserves its stable scheme-defined identity, type, hierarchy, order,
exact content, typed metadata, provenance, semantic digest, dependencies, and relation endpoints
where applicable. `itemId` is API shorthand for the serialized scheme identity, such as
`fragmentId`, `relationId`, or `wordingId`; it is not another stored identifier.

Item IDs map mechanically to deterministic, collision-safe DOM locators. Line numbers, heading
slugs, XPath positions, visible text, array indexes, and current ordering are never identities.
Internal navigator anchor labels are navigation aids only. The filed application has no official
paragraph numbering, and navigator labels must not be cited in prosecution documents.

Relations bind exact `(documentId, fragmentId, fragmentContentDigest)` endpoints. Each relation
has one semantic owner, stable identity, direction, type, ordered fields, and declared navigator
contexts. Forward and reverse navigation and displayed excerpts resolve from the same relation.
Copied assertions, duplicate ownership, stale or ambiguous targets, inferred links, silent
retargeting, and endpoint-driven authority promotion fail validation.

Claims preserve exact visible text, number, order, dependency, grouping, and fragment identity.
Each claim is divided into selectable preamble and limitation units; selected exact, contiguous,
non-overlapping phrases inside a unit may have independent IDs and relations. The configured claim
and unit census in Section 3 is mandatory.

Every selectable unit or phrase has exactly one current recording state:

- `mapped`: one or more candidate passages are recorded; or
- `counsel-review-required`: no candidate passage is recorded.

The latter displays “No candidate passage recorded — counsel review required,” never
“unsupported.” A mapped fragment may still carry a substantive caution. A claim-wide issue is
shown as a claim-level gate rather than being misstated as a local fragment defect. Cautions,
gates, and dispositions preserve their declared type and scope; a source gate quotes the exact
source item, while controlled explanatory wording resolves through wording XML.

## 5. Navigator content and interaction

Each artifact is a two-pane application. The left pane contains the edition's claims; the right
pane contains the as-filed PCT disclosure. The primary flow is claims to disclosure. Reverse
lookup is available only through disclosure badges, so the two directions do not compete for the
same body-text click.

### 5.1 Claims pane

The claims pane contains:

- the edition's complete claims under their declared group headings;
- a sticky, grouped claim index with independent claims visually distinguished;
- a distinct claim-level gate indicator where applicable; and
- one discrete unit control plus independent inline phrase controls.

No interactive element is nested inside another in the accessibility tree. A pointer convenience
surface may enlarge a unit target, but is hidden from the control tree and is suppressed while the
user is selecting text.

Activating a unit or phrase opens all of its recorded candidates or its honest no-candidate
notice. The selected fragment remains strongly marked by color and a non-color indicator until a
new selection or explicit clear action.

### 5.2 Disclosure pane

The disclosure pane renders one continuous dossier containing the retained as-filed title,
description, Examples 1–5, tables, code blocks, PCT claims 1–18, abstract, and Figures 1–4. Stored
PDF content is not rendered directly; validated XML supplies the runtime item structure and
assets.

Filing front matter is excluded. Transcription notes, drawing-sheet notes, reference-numeral
captions, and the filing-data footer are visibly marked “editorial (not filed text)” and cannot be
relation targets. PCT claim items are targetable. Each addressable source item carries its
mechanically derived navigation label and, where useful, section context and opening words.

The current target receives a strong highlight; the other targets for the active fragment receive
soft highlights. Under reduced-motion preference, scrolling is immediate rather than smooth.

### 5.3 Forward navigation

While a claim fragment is active, a navigation bar above the disclosure pane shows:

- mode `Claims → Specification`;
- the edition-prefixed claim, unit, or phrase context;
- current position and disclosure target label;
- previous, next, and clear controls;
- the target's required short descriptive note and required declared role; and
- applicable fragment-, target-, or claim-scope caution indicators.

Targets are ordered by role: `specific`, then `combination`, then `context`; authored order is
stable within each role. The relation stores all candidates. If more than five exist, only the
first five are soft-highlighted together and the bar shows
“+N more”; previous/next still cycles through every candidate and the printable schedule lists
all of them.

### 5.4 Reverse navigation

Each disclosure item used by a current edition relation displays a `◂ N` badge, where `N` is the
number of that edition's fragments indexed to it. Absence of a badge makes no statement about
support or another edition.

Activating the badge starts `Specification → Claims` mode. The claims pane scrolls to the current
fragment, all related fragments receive soft highlights, and the bar reports the fragment and
claim counts plus previous, next, and clear controls. Ordering is claims ascending, units before
phrases within a claim. Disclosure body text remains non-interactive.

The reverse index is derived mechanically from the forward relations and is never separately
authored or stored.

### 5.5 Focus and selection

Forward and reverse selections are mutually exclusive. Activation moves focus to the applicable
navigation bar. Previous and next wrap through the current result set. Clear or `Esc` removes the
selection and returns focus to its originating control.

`Enter` and `Space` activate focused controls. Left and right arrows cycle only while the
navigation bar has focus; there is no global arrow-key capture. Live-region announcements state
mode, position, target, and caution/gate presence without repeating the full source text.

## 6. Controlled product wording and provenance

The exact profile label in Section 1 precedes this standing disclaimer everywhere it appears:

> Draft navigation aid generated from claim-set {edition version} and PCT/IB2025/051755 as
> filed (WO 2025/181623 A1). Mappings are author-recorded candidate associations for counsel
> review — not a written-description, priority, or any other legal opinion. Fragments marked
> "counsel review required" carry no recorded candidate passage. Claim-level gates concern
> the complete claim and are quoted from the claim-set document. Anchor references are
> internal navigation labels, not official numbering, and must not be cited. This edition
> presents one candidate strategy; it does not compare strategies or recommend a filing
> choice.

The disclaimer, confidentiality legend, provenance wording, caution/disposition wording, profile
label, artifact wording, and neutral bundle wording resolve from their current controlled wording
entries. Slots may insert only declared typed values such as the edition version. Ordinary UI
copy remains in templates or code and is tested there for clarity, neutrality, accessibility,
escaping, and determinism.

Each artifact exposes a provenance panel identifying its edition, claim-set version, source
packages, governing authority direction, semantic digests, relation set, and generation profile.
It does not expose internal QA-only paths or claim that generated XML supersedes its PDF or
Markdown authority.

## 7. Visual, accessibility, no-JavaScript, and print contract

- The visual design uses a professional light theme, serif claim/disclosure text, sans-serif
  application chrome, distinct strong/soft highlights, and non-color state indicators.
- At or above 1280 × 720, panes are approximately 45/55 and scroll independently; below that
  minimum they stack in one dedicated scrolling container. The page body does not own scrolling.
- Controls are semantic buttons with logical focus order, visible focus, browser-native accessible
  names and states, no nested interaction, and a minimum 24 px target.
- Pane headings, landmarks, lists, tables, figures, captions, relationships, and announcements use
  appropriate HTML and ARIA semantics. `prefers-reduced-motion` disables smooth scrolling.
- The About/provenance surface and complete flat mapping schedule are available in the interactive
  artifact and remain in the document source.
- With JavaScript removed, claims, disclosure, profile label, disclaimer, confidentiality legend,
  provenance, and the complete mapping schedule remain readable in document order.
- Print output includes claims, disclosure, profile label, disclaimer, confidentiality legend,
  provenance, and the complete schedule, with clipping and overflow safeguards. The profile label
  and disclaimer repeat through the print-page mechanism.

These structural and byte-level requirements are automated. The technical-preview profile still
defers actual browser, operating-system, print-engine, and assistive-technology observation.

## 8. Offline and security contract

Each edition is one self-contained HTML5 file. All CSS, JavaScript, typed rendered data, and four
figures are inline. The recipient needs no server, build tool, package installation, or network
connection; the artifact opens as a local file.

The document declares this exact Content Security Policy:

```text
default-src 'none'; img-src data:; style-src 'unsafe-inline'; script-src 'unsafe-inline'; base-uri 'none'; form-action 'none'; object-src 'none'; connect-src 'none'
```

The application makes no network request, writes no cookie or browser storage, performs no
telemetry, and does not mutate browser history or location. The renderer rejects those capability
tokens in the application script, and product tests confirm their absence. The policy governs
application code, not browser extensions or user actions.

All dynamic values are escaped for their declared HTML, attribute, URL, CSS, or script context.
There is no untrusted `innerHTML`, raw-markup slot, event-handler value, executable template, or
unsafe-URL bypass. Embedded data is script-safe, including `</script` sequences. Hostile-value
fixtures exercise every output context.

The XML parser disables external entities, DTD and XInclude resolution, network access, and path
escape. Security validation and all semantic validation complete before any product write.

## 9. Deterministic products and bundle

The committed current products live under `navigator/dist/`. Fresh processes using the same
locked inputs produce byte-identical HTML, detached checksums, manifest, ZIP, and computed origin
inventory. Ordering, line endings, locale, timestamps, member metadata, paths, and other runtime
variation are fixed by closed mechanical rules or excluded.

The current bundle is:

```text
AA11393US-claims-navigators_NA-2026-07-22-v4_AF-2026-07-22-v6_TECHNICAL-PREVIEW.zip
```

It is a deterministic STORE ZIP containing exactly five members:

1. `AA11393US-NA-claims-spec-navigator_NA-2026-07-22-v4.html`
2. `AA11393US-NA-claims-spec-navigator_NA-2026-07-22-v4.html.sha256`
3. `AA11393US-AF-claims-spec-navigator_AF-2026-07-22-v6.html`
4. `AA11393US-AF-claims-spec-navigator_AF-2026-07-22-v6.html.sha256`
5. `MANIFEST.txt`

The ZIP has its own detached `.sha256` beside it, not inside it. The manifest carries the exact
technical-preview label in Section 1, identifies the two products as alternative counsel-review
editions without preference or recommendation, and lists checksums for the four non-manifest
members. It contains no compatibility authorization, deferred-control registry, or future release
profile.

Either HTML artifact remains independently usable. Member names, order, bytes, checksums, ZIP
metadata, and neutral manifest text are deterministic and validation-enforced.

Input validation is read-only. Product generation writes only declared downstream files, validates
all inputs before writing, and atomically replaces each owned output. Failure cannot modify a
semantic XML authority. A partial generated set is invalid and must be regenerated from the same
current sources.

## 10. Validation, audit, and implementation closure

The sole repository-global gate is:

```sh
uv --no-cache --offline run --locked --no-sync python -m navigator validate-current
```

It captures one repository snapshot, validates the structured-source XML contract, builds the
gateway indexes once per phase, exercises the complete registered test and acceptance suite in an
isolated materialized checkout, regenerates and compares both editions and the bundle, checks
whole-tree whitespace, renders every tracked Markdown document, verifies source-PDF checksums,
revalidates live bytes after tests, and accepts only an unchanged final snapshot. Skipped tests,
unknown acceptance criteria, validation failures, stale products, undeclared reads or writes,
dirty state, and snapshot drift fail.

The audit unit is:

```text
exact clean Git commit
→ repository checkout
→ current documentation and executable acceptance registry
→ registered XML and navigator controls
→ read-only gateway, immutable model, and deterministic products
→ unchanged-snapshot validate-current result
```

Git is the sole implementation and drafting history. The live tree contains no reviewer approval
system, self-attestation, append-only authorization records, receipts, pin plans, migration state,
stored lineage or coverage inventories, compatibility readers, alternate semantic ingestion path,
semantic cache, fallback, generated handoff archive, or duplicate relation owner. The product ZIP
in Section 9 is a delivery product, not an audit package.

The accepted implementation has one XML semantic ingestion path, one immutable typed model, one
edition-blind rendering kernel, current schemas and controls, and only tests and products required
by this contract. Unsupported inputs and obsolete formats fail closed before writes; no backward-
compatibility branch or implicit upgrade path is permitted.

The executable acceptance registry contains only the ordered current IDs, scopes, and criterion
text. The global gate and registered tests check user-visible content, semantic DOM, identity,
relations, static navigation and interaction instructions, accessibility markup, no-script and
print structure, security, deterministic output, products, and bundle requirements from current
inputs. Machine conformance does not execute or certify a browser, print engine, or assistive
technology, and does not certify human attention, source-PDF authenticity, substantive
transcription correctness, legal correctness, counsel approval, filing readiness, or filing
authorization.
