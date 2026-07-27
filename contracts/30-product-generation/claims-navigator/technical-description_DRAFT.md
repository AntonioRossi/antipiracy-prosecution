# AA11393US — Interactive Claims-to-Specification Navigator: Technical Description (DRAFT)

> **OPERATIVE TECHNICAL CONTRACT · INTERNAL COUNSEL-REVIEW DRAFT**
>
> This document defines the two current, standalone claims-to-specification navigator
> products and the architecture that generates them. It states current required behavior
> only. The coupled [`acceptance criteria`](acceptance-criteria_DRAFT.md) are projected in
> [`navigator/schema/acceptance.json`](../../../navigator/schema/acceptance.json).

The `_DRAFT` suffix records internal counsel-review status. Every technical rule in this pair is
operative for the current navigator implementation and product workflow.

The navigator uses **XML as the one uniform machine interface** to the repository content it
consumes. XML supplies stable item identities, hierarchy, typed metadata, provenance, typed-item
digests, declared dependencies, and exact relation endpoints. XML does not become universal source
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
package-specific authorities
        │
        ▼
all three structured-source domains pass aggregate acceptance
        │
        ▼
exactly two dependency-free XML handoffs per edition
(authored generated-XML bytes; PDF-transcription XML surface and declared assets)
        │
        ▼
navigator read-only gateway binds the handoff census and reads navigator controls
        │
        ▼
immutable typed model ──deterministic projection──▶ HTML5
```

| Content class | Governing authority | XML role |
|---|---|---|
| PDF-derived package | Stored source PDF for fidelity | Asserted transcription and validated runtime representation |
| Authored-content package | Authored Markdown | Generated, round-trip-validated runtime representation |
| Upstream authored relation package | Applicant-authored relation XML | Aggregate validation prerequisite only; no navigator edge or runtime input |
| Navigator relation package | Navigator-owned relation XML | Authority for navigator-only associations |
| Navigator wording package | Navigator-owned wording XML | Authority only for controlled semantic or security-relevant wording |
| Typed model and HTML5 | No independent authority | Ephemeral model and deterministic products |

The product semantic-input invariant is exact. Every HTML5 semantic value comes only from the
authored claim package's generated, round-trip-validated XML handoff; the PDF-transcription
XML-derived frozen typed surface, exact XML handoff, and declared assets; or navigator-owned
relation and controlled-wording XML. Authored Markdown and the stored PDF remain upstream authority
or fidelity evidence, never navigator semantic inputs. Generated review Markdown is never a runtime
input.

For PDF-derived packages, generated Markdown is a human review view derived from the XML and is
not a runtime source. For authored packages, the pinned Markdown profile, exact generated-XML
bytes, complete item/field census, and back-rendered ordered Pandoc AST under only declared
presentation normalizations must agree before the navigator consumes the XML.

Each navigator has exactly two semantic consumer edges, both selecting XML: its edition claim set
and `pct-as-filed-dossier`. Choosing XML selects the machine-readable bytes; it never changes the
governing authority. Generated HTML provenance preserves the package authority scheme and XML role.
Aggregate validation of upstream authored-relation packages does not create a navigator edge or make
those packages product inputs. Navigator relation semantics come only from the separately governed
edition relation XML under `navigator/relations/`.

A defect is corrected at its authority:

- authored content is corrected in Markdown and XML is regenerated;
- a PDF transcription or provenance defect is corrected in transcription XML against the PDF;
- navigator-only relations or controlled wording are corrected in navigator XML.

Generated XML, the typed model, and HTML5 are never patched to conceal an upstream defect.

### 2.2 Retained-worktree handoff and one read-only gateway

Production uses one retained worktree capture. Before either handoff is constructed, aggregate
structured-source acceptance validates the complete current PDF-transcription, authored-Markdown,
and authored-relation domains. The verifier then resolves exactly two dependency-free edges for
the edition: its authored claim package and `pct-as-filed-dossier`, both through XML.

The authored-claim handoff contains the exact generated XML bytes, generated-XML role, authority
scheme, empty dependency and asset mappings, `surface=None`, and exact validation reads. The
consumer input pairs the handoff set with the same-context retained parser controls. The PCT
handoff contains the exact transcription XML bytes, transcription role, authority scheme, the same
frozen `PDFTranscriptionSurface` validated upstream, its exact four asset-byte entries, no
dependencies, and exact validation reads. No authored-relation edge or handoff exists for either
claims-to-specification consumer. Each specification navigator secure-parses only the handed claim
XML under the retained controls, never reconverts Markdown or loads default controls, and never
reopens a handed path.

Markdown and PDF paths can occur in a handoff's inherited validation-read census because upstream
validation proves generated XML against its authority and binds transcription XML to stored evidence.
That census is validation evidence, not a semantic handoff: the navigator does not receive those
bytes as model inputs, reopen them, or grant the renderer access to them.

The navigator gateway first binds those validation reads without reopening them. It then reads
only navigator-owned edition, relation, wording, and schema controls from the same retained-byte
snapshot, validates them with the retained parser controls, records the combined ephemeral exact
read set, and seals one immutable in-memory model before rendering. An ordinary read of a handed
path fails.

The handoff and gateway reject undeclared files, symlinks, path escapes, external resources,
unknown fields or versions, duplicate IDs or semantic owners, digest drift, unresolved
dependencies, stale or ambiguous endpoints, invalid wording slots, detached handoff state, and
representation fallbacks.

The model exposes one narrow typed API equivalent to:

```text
getDocument(documentId)
getItem(documentId, itemId)
getMetadata(documentId)
resolveRelation(relationId)
relationsFor(documentId, itemId)
```

Metadata in this pseudo-API is document metadata. Item properties are returned by `getItem`.
Every invocation supplies the displayed explicit nonempty string identities. An omitted, null,
non-string, empty, ambiguous, or unresolved edition, document, item, wording, or relation identity
fails; no current object or representation is inferred. `relationsFor` may return an empty tuple
only after `getItem` resolves the requested document and item exactly. An unresolved item cannot be
represented as having no relations.

The renderer receives only this sealed model and declared presentation resources. Production
renderers do not parse XML, Markdown, PDF/OCR text, semantic JSON, caches, aliases, migration
files, or network resources. The model is never persisted as a semantic store. It may select and
order declared fields, but cannot rewrite substantive text, repair dependencies, infer or retarget
relations, promote an endpoint's authority, or invent controlled wording.

Each product plan, handoff set, retained control set, parsed input, edition model, computed coverage
and origin projection, content lock, rendered HTML, candidate proof, bundle state, and reproduction
projection belongs to one retained capture and one derivation state. Immutability prevents mutation
but never permits reuse across another capture or generated-output state, even when bytes match. A
digest, stored candidate, or detached proof cannot extend an object's lifetime.

### 2.3 Navigator-owned XML

The navigator owns exactly one relation package per edition:

```text
navigator/relations/na__pct.relations.xml
navigator/relations/af__pct.relations.xml
```

They use `schemaProfile="navigator-claim-pct-relations-v1"`; each file's `relationSetId` and
`edition` declare its navigator ownership scope. This grammar is distinct from
`authored-relations-v1` and has no field for an upstream relation reference. These files own only
navigator-specific claim-to-PCT candidate associations; they neither consume, copy, restate, nor
override source-level support, priority, prior-art, comparison, mapping, or crosswalk assertions.

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
undeclared semantic source was read. Coverage is not maintained as a separate stored artifact.

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
inventory includes one bundle-wording slot origin per configured edition plus the bundle-control
origins. Tests separately compare the substantive typed relation values with their rendered
counterparts. The inventory is ephemeral check data, never embedded in a product or stored as a
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

The complete claim XML item surface and complete frozen PCT transcription surface validate before
construction, including their addressable document roots, closed item hierarchy, typed metadata,
provenance, dependencies/assets, and complete typed-item-digest census. The immutable product model
retains only its declared product subset: claim text, structure, dependencies, fragment identities
and digests; disclosure content, structure, identities, digests, and editorial state; source-package
authority and XML-byte bindings; and the exact four figure assets. It does not retain either complete
upstream surface, its document-root record, or its full item-digest map after construction.

Within that retained source subset, `itemId` is API shorthand for the serialized `fragmentId`; it
is not another stored identifier.

Item IDs map mechanically to deterministic, collision-safe DOM locators. Line numbers, heading
slugs, XPath positions, visible text, array indexes, and current ordering are never identities.
Internal navigator anchor labels are navigation aids only. The filed application has no official
paragraph numbering, and navigator labels must not be cited in prosecution documents.

Each edition's navigator relation-set envelope owns one `relationSetId` and `edition`; it is a
product-control envelope, not a source typed item, and has no typed-item digest. Its two declared
documents fix one claim-set `subject` and `pct-as-filed-dossier` `target`. The closed grammar contains
gate definitions, one status-bearing mapping per claim unit, optional exact-text phrase mappings,
typed candidate roles and notes, scoped cautions, and gate dispositions. Mapping, phrase, gate, and
disposition identities are stable within that package. Every endpoint binds exact
`(documentId, fragmentId, fragmentContentDigest)` values, where the digest is a typed-item digest.
Forward navigation, mechanically derived reverse navigation, and displayed excerpts resolve from
the same package. Upstream relation references, copied assertions, duplicate ownership, stale or
ambiguous targets, inferred links, silent retargeting, and endpoint-driven authority promotion fail.

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
packages, governing authority direction, XML byte bindings, typed-item endpoint digests, relation
set, and generation profile.
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

The stored current products live under `navigator/dist/`. Fresh processes using the same
locked inputs produce byte-identical HTML, detached checksums, manifest, ZIP, and computed origin
inventory. Ordering, line endings, locale, timestamps, member metadata, paths, and other runtime
variation are fixed by closed mechanical rules or excluded.

The current shared four-product bundle is:

```text
AA11393US-claims-evidence-navigators_na-specification-NA-2026-07-22-v4_af-specification-AF-2026-07-22-v6_na-prior-art-NA-2026-07-22-v4_af-prior-art-AF-2026-07-22-v6_TECHNICAL-PREVIEW.zip
```

It is a deterministic STORE ZIP containing these nine members in configured-product order:

1. `AA11393US-NA-claims-spec-navigator_NA-2026-07-22-v4.html`
2. `AA11393US-NA-claims-spec-navigator_NA-2026-07-22-v4.html.sha256`
3. `AA11393US-AF-claims-spec-navigator_AF-2026-07-22-v6.html`
4. `AA11393US-AF-claims-spec-navigator_AF-2026-07-22-v6.html.sha256`
5. `AA11393US-NA-claims-prior-art-navigator_NA-2026-07-22-v4.html`
6. `AA11393US-NA-claims-prior-art-navigator_NA-2026-07-22-v4.html.sha256`
7. `AA11393US-AF-claims-prior-art-navigator_AF-2026-07-22-v6.html`
8. `AA11393US-AF-claims-prior-art-navigator_AF-2026-07-22-v6.html.sha256`
9. `MANIFEST.txt`

The ZIP has its own detached `.sha256` beside it, not inside it. The manifest carries the exact
technical-preview label in Section 1, identifies the configured products as alternative
counsel-review editions without preference or recommendation, and lists checksums for every
non-manifest member. It contains no compatibility authorization, deferred-control registry, or
future release profile. The bundle implementation admits only the general shape of one HTML and
checksum pair per configured product followed by the manifest; it has no product-kind branch.

Each HTML artifact remains independently usable. Member names, order, bytes, checksums, ZIP
metadata, and neutral manifest text are deterministic and validation-enforced.

Input validation is read-only. Every product command validates both product contract pairs, both
machine-readable acceptance registries, the exact live implementation census, product plan,
structured-source closure, and applicable stored inputs from the same retained bytes before model
construction or product publication. Each command constructs one closed map of declared generated-
product paths and bytes, validates the complete candidate map before the first write, stages every output, and
atomically replaces each owned file. Before success, it exact-reads every declared output and proves
that only those paths changed with the required bytes, modes, names, checksums, and complete-set
membership. Candidate, release, and bundle publication are unreachable from a split or
contradictory input state; post-write validation cannot substitute for pre-write proof. Failure
cannot modify a semantic XML authority.

Publication is per-output atomic and does not claim multi-file rollback. An interruption, partial
replacement, readback mismatch, or mixed generated set is not current and must be regenerated from
the same retained inputs; a valid individual member cannot rescue an incomplete set. Candidate
proof binds the exact product, product plan, retained capture, derived HTML, stored candidate bytes,
content-lock digest, and fresh-worker digest. A matching digest or detached prior proof alone cannot
authorize release. Bundle construction is a pure function of the explicit product plan and derived
product states; a separate exact verifier compares every stored sealed/checksum member before the
bundle command writes or aggregate validation passes.

## 10. Worktree validation and implementation closure

Both phase-30 technical descriptions, their acceptance criteria and data registries, the exact
implementation and workflow census, structured-source boundary, navigator controls, registered
tests and vectors, and stored products form one indivisible current implementation. Navigator code,
workflow, controls, tests, or products constitute no accepted state independently of this closure.
A documentation-only, registry-only, implementation-only, workflow-only, test-only, control-only,
or product-only state fails before product publication.

An operative navigator behavior, command, input, control, or product change must update every
affected member of this closure coherently in one retained current-state candidate. Git state,
repository history, and external approval records cannot establish or repair that agreement.

Every product command captures retained bytes, resolves one closed product plan from the current
bundle and product controls, validates the complete structured corpus once, binds the plan to the
same-snapshot immutable consumer handoffs, and derives only from those explicit inputs. Model,
product, and bundle builders accept no missing-input default and cannot construct a verifier or
reopen a structured-source path.

The bundle product inventory controls aggregate iteration. Each product entry must agree exactly
with its control file, consumer, claim package, relation and wording controls, sealed artifact,
checksum member, and declared timestamp. Unknown, duplicate, incomplete, or unowned products fail
before model construction. The renderer and bundle builder contain no edition-specific aggregate
branch.

The aggregate gate uses this fixed dependency order inside the retained isolated materialization:

1. validate retained-byte identity, whitespace, command and contract structure, and the exact test
   and implementation census;
2. concurrently execute the two independent read-only expensive branches: (a) render every
   retained Markdown document with three bounded Pandoc workers and resolve every local path and
   fragment in deterministic path order; and (b) validate all three structured-source domains once,
   freeze their parser controls and declared consumer handoffs, derive every configured product,
   build the configured manifest, checksums, origin inventory, and ZIP once while exactly one fresh
   interpreter concurrently repeats that complete source/product derivation once for canonical
   digest comparison;
3. execute every registered test without skips, reusing the already-validated immutable session
   for model and renderer assertions rather than validating the corpus again; and
4. recapture the live governed worktree and require identical paths, modes, and bytes.

Cheap preflight defects stop before Pandoc, structured-source validation, or fresh reproduction.
Each aggregate failure identifies its phase, check, subject, expected condition, actual condition,
and corrective action.

<!-- CURRENT-VALIDATION-BOUNDARY:START -->
The sole aggregate current-state workflow is the shared
[aggregate validation boundary](../../README.md#aggregate-validation-boundary):

```sh
uv --no-cache --offline run --locked --no-sync python -m navigator validate-current
```

It validates technical coherence and deterministic reproducibility only. It does not establish
source authenticity, transcription fidelity, factual or legal correctness, completeness of
prior-art or support analysis, inventor confirmation, counsel approval, filing readiness or
authorization, or entitlement to rely on the package without reviewing its evidence. Human review
of source evidence and substantive analysis remains authoritative.
<!-- CURRENT-VALIDATION-BOUNDARY:END -->

Skipped tests, unknown or unclassified artifacts, unknown acceptance criteria, validation
failures, stale products, undeclared reads or writes, and worktree drift fail. Repository status,
index state, identity, and history are never pass inputs.

The live tree contains no reviewer approval system, append-only authorization records, validation
receipts, pin plans, migration state,
stored lineage or coverage inventories, compatibility readers, alternate semantic ingestion path,
semantic cache, fallback, generated handoff archive, or duplicate relation owner. The product ZIP
in Section 9 is only a delivery product.

The accepted implementation has one retained-worktree structured-source validation path, one
snapshot-bound immutable handoff result, one configuration-resolved product plan, one
navigator-owned control gateway, one immutable typed model per configured product, one
edition-blind rendering kernel, and one fresh product-set reproduction worker. Unsupported inputs
and obsolete formats fail closed before writes; no backward-compatibility branch, implicit upgrade
path, optional validation fallback, or retired reproduction worker is permitted.

The executable closure requires exact retained-capture agreement across all product and shared code,
both product contract pairs, both acceptance registries, schemas, launchers, workflows, controls,
registered tests, required vectors, declared XML inputs, products, checksums, manifest, and bundle.
Missing, additional, alternate, inactive, or contradictory members fail. The readable navigator
inventory below is supplemental and cannot replace capture-wide classification and exact census
enforcement; import success, runtime reachability, a generated artifact, or a detached pass result
cannot establish closure alone.

The focused negative boundary rejects Markdown or PDF used as navigator semantic input; an
authored-relation runtime handoff in a specification product; a missing, additional, dependency-bearing, or non-XML structured-
source handoff; an omitted or unresolved model identity; an unresolved item represented as an empty
relation set; a model, content lock, candidate proof, bundle state, or reproduction projection from
another capture; a partial, mixed, stale, mismatched, or unreadable candidate, release, checksum,
manifest, or bundle set; and a missing or additional capture-wide implementation member.

The exact live navigator implementation census is:

| Layer | Current files |
|---|---|
| Product contracts | Both phase-30 contract pairs and `navigator/schema/{acceptance.json,prior-art-acceptance.json}` |
| Authority and workflow guidance | `AGENTS.md`, `README.md`, `GLOSSARY.md`, `STRUCTURED-CONTENT-AUTHORITY-MANIFEST.md`, `contracts/README.md`, and `navigator/RUNBOOK-content-sync-and-regeneration.md` |
| Package and commands | `navigator/__init__.py`, `navigator/__main__.py`, `navigator/build.py` |
| Typed pipeline | `navigator/lib/__init__.py`, `acceptance.py`, `bundlezip.py`, `canon.py`, `claims.py`, `currentstate.py`, `depgraph.py`, `gateway.py`, `model.py`, `priorart.py`, `projections.py`, `registry.py`, `release.py`, `render.py`, `schema_validate.py`, `snapshot.py`, `unicode15_1.py`, and `validate.py` under `navigator/lib/` |
| Closed navigator controls | `navigator/bundles/current.json`; the product, relation, and wording files selected by that bundle control; `navigator/schema/{acceptance.json,prior-art-acceptance.json,edition.schema.json,navigator-relations.xsd,wording.xsd}`; and current shared/prior-art wording XML |
| Registered navigator tests | `navigator.tests.{test_canon,test_current_pipeline,test_prior_art,test_render_current,test_xml_model}` |
| Registered structured-source tests | `structured_source.tests.{test_acceptance,test_atomic,test_conversion,test_pdf_transcription,test_registry,test_xml_contract}` |

The control-input census is derived path-for-path from the configuration-resolved product plan;
an extra, missing, renamed, or alternate navigator control fails before derivation.

The executable acceptance registries contain only the ordered current IDs, scopes, outcomes, and
independent enforcers. The aggregate gate and registered tests check user-visible content, semantic DOM, identity,
relations, static navigation and interaction instructions, accessibility markup, no-script and
print structure, security, deterministic output, products, and bundle requirements from current
inputs. Browser, print-engine, and assistive-technology behavior remains subject to direct human
testing and is outside a technical pass.
