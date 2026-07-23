# AA11393US — Interactive Claims-to-Specification Navigator: Technical Description (DRAFT)

> **DELIVERABLE SPECIFICATION · STATUS 23 JULY 2026**
>
> Single live specification for the interactive HTML5 navigators linking the AA11393US
> candidate claim sets to the PCT application as filed (PCT/IB2025/051755, published as
> WO 2025/181623 A1). One shared technical contract, **two current editions** built from it:
> the **NA edition** (normal-allowance claim set, NA-2026-07-22-v4) and the **AF edition**
> (allowance-first claim set, AF-2026-07-22-v6). The editions are alternative counsel-review
> strategies, never cumulative layers. This document always describes the current intended
> state; superseded content is removed, not annotated. Implementation follows only from this
> document.
>
> **Interpretation clause:** this document is a specification. Normative language —
> including present-tense descriptions of tests, fixtures, gates, and tools — describes
> required behavior; the implementation lives under `navigator/` and is verified against
> §14 by its acceptance suite (`navigator/tests/`). Where implementation and specification
> disagree, the specification governs and the implementation is defective.
>
> `navigator/RUNBOOK-content-sync-and-regeneration.md` is the non-normative operating
> procedure for this contract. It may make the required commands easier to execute but may
> not relax, extend, or reinterpret this specification; this specification controls every
> conflict.

## 1. Purpose and audience

Each navigator gives US counsel a fast way to answer two recurring questions during claim
review: *"which disclosure passages are recorded as candidate support for this claim
language?"* and, conversely, *"which claim language is indexed to this passage?"* Counsel
clicks any mapped fragment of a candidate claim in the left column; the right column scrolls
to and highlights the recorded candidate passage(s). In the other direction, an "indexed by"
badge on each cited specification block reveals the claim fragments indexed to it (§6.2).

Each edition is a **navigation aid for counsel review** of one claim strategy. The AF
edition may identify AF neutrally as an allowance-first drafting strategy whose stated aim
is anticipating examiner objections; whether it achieves that aim is counsel work, outside
the navigator. Every screen and every printed page carries the standing disclaimer (§9.1).

**Current release profile — technical preview.** The initial delivery is explicitly the
`technical-preview` profile and carries this exact label on screen, in print, in no-JS output,
in its manifest, config, verification records, and acceptance receipts:
**“TECHNICAL PREVIEW — Manual cross-platform and assistive-technology QA is deferred;
browser and assistive-technology compatibility is not validated.”** Automated quality,
determinism, security, privacy/offline, content-validation, and bundle-integrity checks remain
release-blocking. The future `validated-release` profile preserves the complete current
seven-row browser/OS/optional-AT policy and requires its structured version-3 evidence. This
release-profile meaning is distinct from the authoring-only `preview` build mode, which merely
adds a “not for QA or delivery” watermark and never authorizes delivery.

> Manual cross-platform and assistive-technology QA is deferred for the initial
> technical-preview release.

- **Primary user:** US prosecution counsel reviewing claim-set versions NA-2026-07-22-v4
  and/or AF-2026-07-22-v6.
- **Secondary user:** the internal reviewer (Antonio) validating claim-support work product.

### 1.1 Legal and functional boundary

The tool **does**:

- present the pinned candidate claims of each edition and the pinned as-filed PCT
  disclosure;
- display author-recorded **candidate** relationships between claim fragments and disclosure
  passages, with their recording status; `reviewState` is authoring-only and never ships;
- show, for every fragment, whether a candidate passage is recorded — including an honest,
  releasable no-candidate disposition (§8.1);
- preserve source-derived caution gates — including claim-level gates — with
  machine-verifiable pointers to their source text, enumerated in a reviewed gate inventory;
- expose unresolved items to counsel rather than resolving them;
- derive the reverse index mechanically from the forward mapping, within one edition.

The tool **does not** determine or imply:

- whether any fragment is adequately supported under §112(a), or unsupported;
- enablement, new matter, priority entitlement, or permissible amendment scope;
- claim construction, definiteness, §112(f) treatment, patentability, validity, or
  infringement;
- whether individually disclosed passages may legally be combined;
- whether a passage suffices as an official prosecution citation;
- the accuracy of the underlying transcription (§2), which is not independently verified;
- **selection between the AF and NA strategies for filing**, or any filing route;
- **allowance likelihood or examiner behavior**; AF is never represented as
  "examiner-objection-proof";
- §101/§102/§103 conclusions or any prior-art comparison;
- **equivalence between AF and NA claims or terminology** (the crosswalk's non-conflation
  boundary is binding: AF's "camera-source-transition pattern" usage is not synonymous with
  NA's "camera-cut timing pattern");
- any merged or hybrid claim set, or automatic transfer of support mappings between
  strategies;
- mappings to the provisional, prior art, ISR/Written Opinion, or office-action responses;
- any automated or runtime inference of support.

It provides no editing, collaboration, access control, encryption, or secure document
management. **Provisional boundary:** an artifact may display a source-derived external
priority caution originating from its own claim-set document's text (e.g., the AF Example 2
priority gate); it does not display or evaluate provisional mappings, and it never renders
content from a priority-support map (§2). **Complete-AF-set rule:** the AF edition always
shows all 23 AF claims. AF claims 19–22 are one integrated-method family and AF claim 23 is
the separately standing monitor-side method; any filing subset is a counsel filing choice
recorded nowhere in the navigator, and no separate AF claim-set document is created for it.

## 2. Sources and authority

Every input is a registered corpus (§8.1) with a globally unique id. Visibility is declared
per corpus and refined by its segmentation profile.

**Corpus and edition ids are stable, version-neutral names.** The claim-set version is a
registry label and an edition-config parameter, never part of an id. A claim-set version
change updates the pins and version label **in place** and enters the §13 update procedure
(`migrate` resolves the consequences); new ids are never minted for new versions. Artifact
names embed the claim-set version (§13), so a stale navigator remains identifiable. Renaming
an id is deliberately expensive: the relation binding participates in every review
projection, so a rename re-enters review for every owner — ids are stable by construction,
not convention.

| Corpus id | Path | Role | Visibility | Used for |
|---|---|---|---|---|
| `pct-pdf` | `PCT/AA11393US-PCT_RAPPORTO DEPOSITO.pdf` (60 pp.) | `authoritative` | `internal` (identity/hash may appear as authority metadata in embedded provenance, §13) | As-filed authority of record; never rendered |
| `pct-disclosure` | `PCT/AA11393US-PCT_RAPPORTO_DEPOSITO_markdown/` (markdown + `figures/Fig-1..4.png`, each file pinned) | `derivative` | `rendered` | The as-filed disclosure package: title, description, Examples 1–5, PCT claims 1–18, abstract, four drawing sheets |
| `na-claims` | `US/normal-allowance/AA11393US-NA-US_claim-set_DRAFT.md` | `fragment-source` | §3 claims `rendered`; profile-designated guidance blocks `quotable`; rest excluded | NA claims 1–30 verbatim; guidance blocks as caution/gate sources |
| `af-claims` | `US/allowance-first/AA11393US-AF-US_claim-set_DRAFT.md` | `fragment-source` | §3 claims `rendered`; profile-designated guidance blocks `quotable` (including the §3 Example 2 priority-gate blockquote, excluded from the unit census); rest excluded | AF claims 1–23 verbatim; guidance blocks as caution/gate sources |
| `na-priority-map` | `US/normal-allowance/AA11393US-NA-priority-support-map_DRAFT.md` | `qa-source` | `internal` | QA cross-check of the NA mapping (§9); never rendered, never quoted, never identified in an artifact |
| `af-priority-map` | `US/allowance-first/AA11393US-AF-priority-support-map_DRAFT.md` | `qa-source` | `internal` | QA cross-check of the AF mapping (§9); never rendered, never quoted, never identified in an artifact |
| `af-na-crosswalk` | `US/allowance-first/AA11393US-AF-claim-crosswalk_DRAFT.md` | `qa-source` | `internal` | Non-conflation QA; **review context and a non-transfer warning for cross-edition reuse proposals (§10) — never evidence that reuse is substantively correct**; never rendered, never quoted, never identified in an artifact |

The AF prior-art matrix, counsel briefings, mapping matrices, and continuation memo are
**not** navigator inputs: they concern patentability and strategy, not claims-to-PCT
navigation.

Visibility semantics (validator-enforced, §10): `rendered` — appears as claim or disclosure
content in a pane; `quotable` — never targetable and never presented as claim or disclosure
text, but a block may appear as a source-gate quotation or, where the profile explicitly
designates it, as a visibly labeled guidance note in the claims pane; `internal` — no
UI-visible relation may point into it. Internal QA-source identifiers, paths, and hashes
never appear in a delivered artifact. The sole identifier exception is public authority
metadata for the edition's configured `authorityCorpus` (`pct-pdf`, §13); the PDF content is
still never rendered. A caution or target referencing an `internal` corpus is schema-invalid.
**Quotable status is designated by each corpus's segmentation profile, never by fixed
section numbers.**

Excluded from rendering: PCT front matter (cover letter, contracting-states list, WIPO
receipt, Form PCT/RO/101). The filing-data footer is retained as a small labeled block.

**Editorial content rule.** Content present in the transcription but not in the filed text —
the transcription note, the drawing-sheet note, the per-figure reference-numeral captions,
the filing-data footer — is visibly labeled *editorial (not filed text)* and is
**non-targetable**: the validator rejects any mapping entry pointing at an editorial block.
The `pct-disclosure` segmentation profile declares the PCT claims section an approved
targetable part of the common disclosure corpus; both editions may target it.

## 3. Editions

The kernel is **edition-blind**: no shared code knows which edition it serves. Everything
edition-specific is declared in the edition config, whose normative parameters are:

| Parameter | NA edition | AF edition |
|---|---|---|
| Claim corpus | `na-claims` (NA-2026-07-22-v4) | `af-claims` (AF-2026-07-22-v6) |
| Authority corpus (read and pin-verified) | `pct-pdf` | `pct-pdf` |
| Claims | 30 | 23 |
| Limitation units (census, test-enforced) | 77 | 61 |
| Independent claims | 1, 9, 16, 22 | 1, 19, 23 |
| §3 group headings | 4 actor groups | 10 structural groups |
| Largest decompositions | claim 22 = 14 units; claim 9 = 9 units | claims 1 and 19 = 14 units; claim 23 = 8 units |
| Display prefix (mandatory) | `NA claim N` | `AF claim N` |
| Relation set | `relations/na__pct.json` | `relations/af__pct.json` |
| Gate inventory | `profiles/gates_na-claims.json` | `profiles/gates_af-claims.json` |
| Dependency map (authored + cross-validated, §8.1) | `profiles/deps_na-claims.json` | `profiles/deps_af-claims.json` |
| Corpus registries | shared `corpora.json` + `profiles/corpora_na.json` | shared `corpora.json` + `profiles/corpora_af.json` |
| Edition strings resource | `profiles/strings_na.json` | `profiles/strings_af.json` |
| Edition config | `editions/na.json` | `editions/af.json` |
| QA registry (verification-only) | `profiles/qa_na.json` | `profiles/qa_af.json` |
| QA cross-check source | `na-priority-map` | `af-priority-map` |
| QA crosswalk binding | `null` | `af-na-crosswalk` |
| Forbidden terms in authored user-visible text | — (NA claims legitimately use both pattern terms, with distinct claim functions) | `camera-cut timing pattern` (crosswalk non-conflation boundary) |
| Artifact (default name, §17) | `AA11393US-NA-claims-spec-navigator_NA-2026-07-22-v4.html` | `AA11393US-AF-claims-spec-navigator_AF-2026-07-22-v6.html` |

Edition rules:

- **Alternatives, not layers.** Each edition builds its own single-edition artifact. There
  is no NA/AF toggle, merged view, or hybrid artifact.
- **Isolation, precisely scoped:** an edition-specific failure (its relation set, gate
  inventory, claim registry, strings, census, QA registry, QA, attestations, acceptance
  fixtures, or acceptance callbacks) never blocks or contaminates the other edition.
  A standalone acceptance run binds and opens only shared runner inputs plus its selected
  edition's inputs; a bundle acceptance run binds both editions. Bundle-manifest wording is
  bundle-only and is not a standalone-edition content input.
  Failures of shared inputs (the PCT corpora, schemas, canonicalization profile, legend)
  legitimately affect both. The bundle (§11) requires both editions sealed.
- **Build isolation (enforced):** building an edition may open only the inputs named by that
  edition's config — the registry accessor enforces the per-edition allowlist, so the AF
  build cannot read the NA relation set even by mistake.
- **Every displayed claim reference outside verbatim claim text carries its strategy
  prefix** (`NA claim 9`, `AF claim 1`, `PCT claim 11`); bare claim numbers are ambiguous
  per the repository's own rule. Reverse badges and counts are inherently edition-scoped.
- **Independent mapping.** AF is mapped from the disclosure independently; there is no
  automatic NA→AF (or reverse) target inheritance. Cross-edition reuse exists only as
  reviewed proposals under the deferred `propose-reuse` boundary (§10).

## 4. Functional overview

Single self-contained HTML file per edition, two independently scrolling panes:

```
┌────────────────────────────────────────────────────────────────────┐
│ Header: edition title · claim-set version · WO number · legend     │
├──────────────────────────┬─────────────────────────────────────────┤
│ LEFT — claims of THIS    │ RIGHT — as-filed disclosure package     │
│ edition only             │ ┌─────────────────────────────────────┐ │
│ claim index strip        │ │ navigation bar (on selection):      │ │
│ (sticky, edition groups) │ │ Claims → Specification              │ │
│                          │ │ NA claim 9 · limitation 6           │ │
│ **9.** A content-        │ │ 2 of 4 : Example 3 · ¶1   ◀ ▶  ×    │ │
│ distribution system…     │ │ + note + caution chips              │ │
│ [status-bearing          │ └─────────────────────────────────────┘ │
│  limitations with        │                                         │
│  clickable inner         │ …scrolled to and highlighting the       │
│  key phrases]            │ recorded candidate passage…             │
└──────────────────────────┴─────────────────────────────────────────┘
```

**Directionality.** The primary flow is left→right — claims drive, the disclosure responds —
and disclosure body text is selectable but never clickable. Reverse lookup (spec→claims)
exists only through the "indexed by" badge affordance (§6.2), so the two flows cannot collide
on the same click. The navigation bar always displays its mode label: `Claims →
Specification` (forward, bar over the right pane) or `Specification → Claims` (reverse, bar
over the left pane).

## 5. Left column — claims pane

### 5.1 Content

- The edition's claims verbatim from its claim-set §3, under that document's own group
  subheadings (NA: four actor groups; AF: seven structural groups, including the
  quotable-designated priority-gate blockquote rendered as a visibly labeled guidance note,
  not as claim text).
- A sticky **claim index strip**: chips grouped per the edition's groups; clicking a chip
  scrolls the left pane to that claim. The edition's independent claims (from config)
  visually distinguished.
- Claims bearing a **claim-level gate** (§8.5) show a distinct gate chip at the claim
  header.

### 5.2 Clickable units — two-tier granularity

Every claim is decomposed into **limitation units** — its markdown paragraphs: preamble plus
each clause. The census is normative per edition (§3): NA 30 claims / 77 units (claim 22 =
14 units and claim 9 = 9 units); AF 23 claims / 61 units (claims 1 and 19 = 14 units each,
and claim 23 = 8 units). The extraction test asserts the census exactly.

- **Tier 1 — limitation unit.** One activation region per unit. Activating it opens the
  unit's recorded candidates, or its status notice (§5.3).
- **Tier 2 — inner key phrase.** Selected phrases within a unit are independently
  activatable with their own, more pinpoint candidate lists. Phrase activation does not
  trigger the enclosing unit.

Phrase rules: exact, contiguous, verbatim substring of its unit; no overlaps within a unit;
identified by stable phrase ID (`c9u6p1`) plus occurrence index. Estimated 2–6 phrases per
multi-clause unit.

Accessibility pattern (normative): no interactive control nests inside another in the
accessibility tree. Each unit exposes one discrete unit-level button (slim edge control
spanning the unit) and each phrase is its own inline button; the whole-paragraph pointer
surface is a convenience layer hidden from the control tree. Pointer activation is suppressed
while a text selection exists. On activation, focus moves to the navigation bar; Esc clears
the selection and returns focus to the originating fragment control. Full requirements in
§12.

### 5.3 Evidence states

Every unit and phrase carries `status` and `reviewState` (§8.4):

- **`status`** — recording state only: `mapped` (≥ 1 candidate passage recorded — no
  implication of legal sufficiency) or `counsel-review-required` (no candidate passage
  recorded). A `counsel-review-required` fragment renders with a distinct neutral marker;
  activation shows *"No candidate passage recorded — counsel review required"* plus any
  fragment-level caution. Never rendered as "unsupported".
- **`reviewState`** — internal authoring progress: `pending` | `internally-reviewed`.
  Authoring-only: it is excluded from every shipped projection, including previews and the
  schedule, is never rendered, and never implies counsel approval.

The honest configurations: candidates recorded but legally unresolved → `mapped` plus
sourced caution; no honest candidate → `counsel-review-required`, never an invented target,
**releasable via the gate-disposition rule** (§8.1) even when a mandatory target-scope gate
applies; every unit mapped but the complete claim legally gated → mapped units plus a
**claim-level gate** (§8.5), displayed at claim level precisely so the issue is not
misstated as local.

A released artifact contains no owner without its applicable lifecycle fields, no
`pending`, and no `migrationState: stale` (§10); the vocabulary never implies a legal
conclusion.

### 5.4 Selection state

The active fragment keeps an accent outline (plus a non-color marker) until another selection
is made or the selection is cleared (bar ×, or Esc). Forward and reverse selections are
mutually exclusive; activating either clears the other entirely.

## 6. Right column — disclosure pane

- The as-filed disclosure package rendered as a continuous document: headings, paragraphs,
  bullet lists, Example 1/3/4/5 code blocks, Example 2 EDL tables (Tables 1–3), PCT claims
  1–18, abstract, and Figures 1–4 (embedded as data URIs) with their editorial-labeled
  numeral captions.
- Every addressable block displays an unobtrusive margin marker with its anchor label (§7;
  visibility is a §17 default pending confirmation).
- On activation of a target: smooth scroll to center (instant under reduced motion, §12),
  **strong highlight** on the current target, **soft highlight** on the other recorded
  candidates of the same selection.

### 6.1 Navigation bar — jump + cycle

Pinned to the top of the right pane while a forward selection is active:

- Mode label `Claims → Specification`; context `NA claim 9 · limitation 6` / `AF claim 1 ·
  limitation 8` (or `… · "camera-cut timing pattern"` for a phrase) — always
  edition-prefixed.
- Position and target label: `2 of 4 : Example 3 · ¶1`; **◀ ▶** cycle the full recorded
  candidate list (wrapping); × clears. Keyboard bindings are scoped (§12).
- The current target's **note** (≤ 140 chars, descriptive only) and its **role** where
  recorded (§8.3).
- **Caution chips**, by scope and type (§8.5): target- and fragment-scope chips inline; a
  **claim-level gate chip class**, visually distinct, whenever the active fragment's claim
  carries a claim-scope gate (specific meaning carried by the gate's `code` microcopy —
  "claim-as-a-whole" is one code among several). Display paths: `source-gate` chips expand
  to quote their pinned source text (rendered at build from the pinned block — derived
  content is never stored, §8.5); `generalization-note` chips expand to the approved
  microcopy registered for their `code`. Every caution type, scope, and code has a
  registered display path (§10, enum exhaustiveness).

Ordering: first target is the most specific recorded candidate; the rest follow in
decreasing specificity — **derived at build from the role enum** (`specific` before
`combination` before `context`; targets with no role follow all named roles; stable in
authored order within each rank and within the unroled group), never separately authored.
The data records **all** recorded candidates (no authoring cap); if more than 5 exist, the
inline soft-highlight set shows the first 5 with a passive "+N more" indicator in the bar.
The ◀ ▶ controls still cycle through every recorded candidate, and the printable schedule
(§11) always lists all.

### 6.2 Reverse lookup — "indexed by" badges

Every disclosure block that appears as a target anywhere in this edition's relation set
renders a small **"◂ N" badge** (N = number of fragments indexed to it, in this edition
only). A block with no badge is simply **not indexed by any recorded mapping entry of this
edition** — the artifact draws no inference about support, use, non-use, or the other
edition.

- Activating a badge starts a **reverse selection**: left pane scrolls to the first indexed
  fragment; all indexed fragments soft-highlighted; the badge's block outlined; focus moves
  to the navigation bar.
- The navigation bar appears over the **left** pane: mode label `Specification → Claims`,
  count summary `5 fragments · 3 claims`, then `2 of 5 : NA claim 9 · limitation 6  ◀ ▶  ×`.
  Fragments are listed claims-ascending, units before phrases within a claim; phrase entries
  display as `NA claim 1 · "structured list"`.
- Whole-claim anchors (`PC1`–`PC18`) are targets like any block and carry their own
  badge, rendered at the claim head.
- Disclosure body text remains non-clickable; the badge is the only reverse affordance.
- The reverse index is derived at build time by inverting the forward relation set; it is
  never separately authored and cannot disagree with the forward direction.

## 7. Anchoring and referencing

The disclosure is segmented at build time into addressable blocks with **build-specific
deterministic anchors**: deterministic for a given pinned corpus, meaningful only relative to
the corpus hashes stated in the provenance manifest. Anchors are **declared locator fields**
(§13): they ship for navigation, but the reviewed identity of any reference is its pinned
canonical-text hash, and identity follows those hashes under the migration case table (§10),
never positions alone.

| Anchor type | ID form | Example label |
|---|---|---|
| Paragraph | `S###` (sequential) | `Detailed description · ¶14` |
| Bullet-list item (component/step lists) | `S###` | `Detailed description · item 3` |
| PCT claim element (claim bullet) | `S###` | `PCT claim 11 — element 2` |
| Table | `S###` | `Example 2 · Table 2` |
| Table row | `S###.rK` | `Example 2 · Table 2 · row Cut 3` |
| Code block | `S###` | `Example 5 · code 2` |
| Figure | `S###` | `Figure 3 · image` |
| Section heading (targets the whole section) | `S###` | `Example 2` |
| Whole PCT claim (head + elements) | `PC1`–`PC18` | `PCT claim 11 (whole)` |

Row-level anchors exist for the Example 2 EDL tables because NA claims 2, 3, and 23 and AF
claims 2–3 turn on specific cut rows; whole-table highlighting is too coarse there. Both
claim-set corpora's guidance blocks are segmented with the same scheme to serve as
caution/gate sources (§8.5).

Pinpoint display: each anchor label is accompanied, where useful, by the section name and the
passage's opening words. (As-filed PDF page pinpoints are additive corpus enrichment on the
roadmap, §15.)

**Numbering disclaimer:** anchor labels are generated for navigation only; the application as
filed has no official paragraph numbering, and these references must not be cited in
prosecution documents. Stated in the standing disclaimer (§9.1).

## 8. Data model — corpora, relations, editions

The system is three concepts; everything else derives from them. The governing rules:
**every association pins both of its endpoints by digest and carries lifecycle state
wherever an authorized operator reviewed it**; **mechanisms are closed over their own data**; **boundaries
are axes on one schema, planes never feed backward, derived content is never stored**; **a
review covers content in its context**; **policies are total functions over evidence
states**; **invariant exceptions are typed and justified, never silent**; and **structural
graphs are dual-sourced** (§8.1, §8.4, §13).

### 8.1 Corpus registry, gate inventories, dependency maps

Shared PCT corpora are registered in `navigator/corpora.json`; each config also selects one
edition claim registry (`profiles/corpora_<edition>.json`). Internal QA corpora live in the
separate selected `profiles/qa_<edition>.json`, read only by verification commands and, for
validated-release, bound by raw path/digest inside `qaInputLock`. Technical-preview does not
create or claim a QA input lock. Registry resources are closed and versioned; their
merged artifact corpus set must exactly equal the three corpus ids named by the edition.
Every entry has a globally unique id (§2), role
(`authoritative` | `derivative` | `fragment-source` | `qa-source`), visibility (`rendered` |
`quotable` | `internal`), per-file SHA-256 (a multi-file corpus pins every file
individually), version label, and a **segmentation profile** (declarative file listing which
sections are targetable, editorial, quotable, or excluded — policy lives in reviewable data,
not parser code; quotability and targetability are profile-designated, never hardcoded;
**content matched by no profile rule is excluded** — the fail-safe default: nothing
renders unless designated). `schema/segmentation-profile.schema.json` closes the profile,
rule, match, kind, and class vocabularies at version `"1"`; malformed/empty matches,
duplicate matches, unknown classes, and editorial rules without visible labels fail before
segmentation, so a typo can never turn an exclusion into rendered content.

Each registry object has exactly `{registryVersion, corpora}` with version `"1"`. Entries
are closed: nonempty version, nonempty pinned file map, a pinned primary, full canonical
`sha256/c1` digests, and canonical repository-relative file/profile paths. Rendered
`derivative` and `fragment-source` entries require a profile; `authoritative` and
`qa-source` entries are `internal` and forbid one. Other role/visibility combinations fail
before any corpus bytes are consumed.

Each fragment corpus has a **gate inventory** (`profiles/gates_<corpusId>.json`) — authored,
reviewed data enumerating every guidance gate of that claim-set document. Exact entry shape:

- `gateId` — unique within the corpus;
- `source` — `(block, full textHash)` into a profile-designated `quotable` block;
- `code` — closed caution code (§8.5);
- `requiredScope` — `target` | `fragment` | `claim`;
- `appliesTo` — hashed endpoints, per scope: claim scope → claim ids with **aggregate claim
  hashes**; fragment scope → fragment ids with fragment hashes; **target scope → applicable
  fragment ids with hashes plus a required cardinality (≥ 1 target of each listed fragment
  must carry this gate; which target is the identified authorized operator's reviewed
  choice)**;
- `requirement` — `mandatory` | `optional`. Optional means that evidence and a disposition
  may both be omitted; if an affirmative/carried disposition is authored, its matching
  gate/caution instance at the required scope and cardinality must actually exist. No
  conditional-activation logic exists.
- `profileDigest` — the segmentation-profile digest the inventory's block references were
  authored against. Inventory source locators are eligible for mechanical re-anchoring
  (§10) under a unique canonical-hash match.

**Gate dispositions — policies are total over evidence states.** How a mandatory gate is
carried is recorded as a reviewed, lifecycle-bearing **disposition** that pins the gate by
its inventory-entry digest — computed over the entry's review projection, source locator
excluded per the declared locator exception, `appliesTo` hashes included so applicability
changes deliberately cascade — and the subject by its identity tuple and content hash, from a
closed enum of recording facts: `carried-at-required-scope` (an instance of the gate is
carried at the inventory's required scope — for target scope, on ≥ 1 recorded target of the
applicable fragment); `carried-at-fragment-fallback` (target scope only: the applicable
fragment is `counsel-review-required`, so no target exists to carry the gate, and the same
gate is carried at fragment scope instead — the single declared exception to the
scope-match rule); `no-target-recorded` (target scope only: the applicable fragment is
`counsel-review-required` and carries no instance — the structural fact is recorded,
reviewed, releasable). A **requiredScope × evidence-state matrix** in the invariants module
declares exactly which dispositions are permitted in each configuration and is total: every
reachable configuration has at least one permitted disposition, none of which requires
creating evidence. **A mandatory requirement is never satisfiable only by creating
evidence**: an honest no-candidate fragment releases without a fabricated mapping. One
disposition fixture file contains five cases proving the matrix — one per enum value, the
no-candidate release case, and a rejected wrong-scope case.

Each fragment corpus also has an authored **dependency map**
(`profiles/deps_<corpusId>.json`) — the claim dependency graph, independently authored from
the claim text and **cross-validated against the parsed "of claim N" references in the
claim text; any mismatch fails the build**. For AF — whose claim-set document publishes its
own §2 dependency table — validation is three-way: authored map, parsed references, and the
document's table must agree. NA publishes no dependency table, so its map rests on the
two-way check. Validation also proves each graph total (every claim present exactly once),
with canonical positive-decimal object keys (`"1"`, never aliases such as `"01"`),
acyclic, and rooted at the edition's declared independent claims. Dependency-chain hashes
(§8.2) are computed only from a validated map — structural graphs are dual-sourced, never
parsed-only (inference) or authored-only (typo risk).

The inventory is a reviewed interpretation of the claim-set's prose gates, recorded once and
hash-pinned to its source blocks. The validator proves gate coverage by **referential
integrity in both directions** over instances *and dispositions*: every `source-gate`
instance carries a `gateId` resolving to a matching inventory entry, and every `mandatory`
inventory entry has a reviewed disposition at its required scope and cardinality. Every
affirmative disposition, including one on an optional entry, proves the corresponding actual
carried instance; optionality can permit absence, never a false claim of presence. Inventory
completeness itself is a **digest-bound identified-authorized-operator attestation** (claim-set digest + inventory
digest, §9).

Outside a relation file, fragment identity is always the scoped triple
`(fragmentCorpusId, fragmentId, fragmentTextHash)` — both editions contain a `c1u0`.

### 8.2 Canonical text, object serialization, and hashing — versioned law

One shared canonicalization module is the only hashing path for all digests — text, object,
and composite alike; a test asserts no digest is computed outside it. The rule set carries a
**canonVersion**, recorded with every stored digest (`sha256/c1:…`). Changing any rule bumps
the version and requires same-commit re-authoring under the new current schema. A command
encountering another canonVersion rejects it before any write; cross-canon comparison or
automatic migration is forbidden.
**canonVersion c1 pins Unicode 15.1.0**: NFC normalization uses vendored Unicode 15.1
tables and the White_Space property is a vendored constant. Neither is taken from the
interpreter's Unicode database, so supported interpreters canonicalize the same text even
when their bundled `unicodedata` versions differ.

Per-type text rules (canonVersion c1):

- **Prose (paragraphs, list items, headings, captions):** decode UTF-8 → Unicode NFC →
  collapse every whitespace run to a single space → trim.
- **Code blocks:** NFC → normalize line endings to LF → strip trailing whitespace per line →
  **preserve line breaks and leading indentation**.
- **Tables:** canonical cell text joined with U+001F, rows with U+001E, caption appended as
  a final row. U+001E and U+001F are reserved structural separators and are invalid in
  cells or captions, making the serialization unambiguous. Row hashes use the row's
  serialization.
- **Figures:** domain-tagged composition (`aa11393:figure:c1`) over
  `SHA-256(file bytes) ‖ SHA-256(canonical caption text)`.

**Canonical serialization (composite digests) — defined by rule, confirmed by vector.**
Every composite digest takes exactly one of two payload forms, declared per tag:

- **Digest-list composites** (`claim-agg`, `dep-chain`, `figure`): the payload is the raw
  binary concatenation of the listed 32-byte digest values, in declared order — no JSON
  involved.
- **Object composites** (`review`, `inventory`, `lock`, and the verification-record kinds):
  the payload is canonical JSON — UTF-8 output; all strings NFC-normalized; **objects whose
  keys collide after NFC are rejected**; object keys sorted by Unicode code point of the
  NFC key string; escaping exactly: the two-character forms `\"` `\\` `\n` `\r` `\t` and
  `\u00XX` for remaining control characters below U+0020 — nothing else escaped; numbers
  are integers only with |n| < 2⁵³, serialized in base-10 with no exponent or fraction
  forms and −0 serialized as `0`; array order preserved exactly as authored. Digests inside
  an object composite appear as their full prefixed string form (`sha256/c1:<64 hex>`).

The same value domain is enforced while parsing every JSON input, before an ordinary object
can discard evidence: raw duplicate keys and distinct keys that collide after NFC are
rejected; fractional or exponent-form numbers, non-finite values, booleans in
schema-integer positions, integers outside |n| < 2⁵³, and strings or keys containing lone
UTF-16 surrogates cannot enter canonical data; strings are Unicode scalar sequences. Thus a
verification record or policy file cannot exploit a permissive host JSON decoder to acquire
a second interpretation.

Every composite digest is framed `tag ‖ 0x00 ‖ payload` (tags are ASCII, never containing
NUL): `aa11393:claim-agg:c1`, `aa11393:dep-chain:c1`, `aa11393:review:c1`,
`aa11393:inventory:c1`, `aa11393:lock:c1`, `aa11393:figure:c1`, and one tag per
verification-record kind — `aa11393:qa-record:c1`, `aa11393:attestation:c1`,
`aa11393:release-record:c1`, `aa11393:bundle-record:c1`. Composite digest types:

- **Aggregate claim hash** — digest-list composite over the claim's ordered unit hashes.
- **Dependency-chain hash** — digest-list composite over the ordered aggregate claim hashes
  of the owner claim's ancestor chain (independent claim first, owner's claim last), per
  the validated dependency map (§8.1).

Golden test vectors confirm the law; they do not define it. Validation uses the **full
SHA-256 digest**; abbreviated prefixes are display-only.

### 8.3 Relation entries

One relation set per (fragment corpus, target corpus) pair, its binding declared in the file
header; entries referencing any other corpus are schema-invalid. The examples below are
**abridged renderings of the required fixtures** (fields may be omitted, arrays truncated from the end, and digests abbreviated) (`navigator/tests/fixtures/`); the test
suite must validate each fixture against the shipped schemas and pinned corpora **and
compare this document's code blocks against the fixtures' projections**. Hashes are
abbreviated here; data files carry full digests with their canonVersion prefix. The excerpts
preserve the checked-in model authorship as `operatorKind: model`; they test shape and
projection currency, but are not by themselves proof that the complete release predicate
or verification chain passes.

NA fixture (excerpt of `relations/na__pct.json`):

```json
{
  "binding": {
    "fragmentCorpus": "na-claims",
    "targetCorpus": "pct-disclosure",
    "schemaVersion": "1",
    "canonVersion": "c1"
  },
  "claimGates": {
    "c9": [
      {
        "gateId": "na-gate-production-relationship",
        "type": "source-gate",
        "code": "production-relationship",
        "claimHash": "sha256/c1:38f2…",
        "reviewState": "internally-reviewed",
        "migrationState": "current",
        "review": {
          "by": "codex:gpt-5.6:019f8e90-cb24-7e33-a61b-5d867ebfa690",
          "operatorKind": "model",
          "date": "2026-07-23",
          "contentHash": "sha256/c1:64e4…"
        },
        "source": {
          "corpus": "na-claims",
          "block": "S011",
          "textHash": "sha256/c1:eccf…"
        }
      }
    ]
  },
  "fragments": {
    "c9u6": {
      "status": "mapped",
      "targets": [
        {
          "block": "S081",
          "textHash": "sha256/c1:df14…",
          "role": "specific",
          "note": "Manifest files 121 point to unique interleaved combinations of chunks of the ensemble"
        },
        {
          "block": "S085",
          "textHash": "sha256/c1:dfee…",
          "role": "combination",
          "note": "Manifests for reference and mate differ in how they reference chunks where edits were made"
        }
      ],
      "reviewState": "internally-reviewed",
      "migrationState": "current",
      "review": {
        "by": "codex:gpt-5.6:019f8e90-cb24-7e33-a61b-5d867ebfa690",
        "operatorKind": "model",
        "date": "2026-07-23",
        "contentHash": "sha256/c1:fdc4…"
      },
      "fragmentTextHash": "sha256/c1:9de8…"
    },
    "c20u0": {
      "status": "counsel-review-required",
      "reviewState": "internally-reviewed",
      "migrationState": "current",
      "review": {
        "by": "codex:gpt-5.6:019f8e90-cb24-7e33-a61b-5d867ebfa690",
        "operatorKind": "model",
        "date": "2026-07-23",
        "contentHash": "sha256/c1:f09e…"
      },
      "fragmentTextHash": "sha256/c1:b6aa…"
    }
  },
  "dispositions": [
    {
      "gateId": "na-gate-production-relationship",
      "subject": {
        "kind": "claim",
        "id": "c9"
      },
      "disposition": "carried-at-required-scope",
      "gateEntryHash": "sha256/c1:00f2…",
      "subjectHash": "sha256/c1:38f2…",
      "reviewState": "internally-reviewed",
      "migrationState": "current",
      "review": {
        "by": "codex:gpt-5.6:019f8e90-cb24-7e33-a61b-5d867ebfa690",
        "operatorKind": "model",
        "date": "2026-07-23",
        "contentHash": "sha256/c1:0848…"
      }
    },
    {
      "gateId": "na-gate-distribution-integration",
      "subject": {
        "kind": "claim",
        "id": "c9"
      },
      "disposition": "carried-at-required-scope",
      "gateEntryHash": "sha256/c1:2aa2…",
      "subjectHash": "sha256/c1:38f2…",
      "reviewState": "internally-reviewed",
      "migrationState": "current",
      "review": {
        "by": "codex:gpt-5.6:019f8e90-cb24-7e33-a61b-5d867ebfa690",
        "operatorKind": "model",
        "date": "2026-07-23",
        "contentHash": "sha256/c1:af65…"
      }
    }
  ]
}
```

AF fixture (excerpt of `relations/af__pct.json`):

```json
{
  "binding": {
    "fragmentCorpus": "af-claims",
    "targetCorpus": "pct-disclosure",
    "schemaVersion": "1",
    "canonVersion": "c1"
  },
  "claimGates": {
    "c1": [
      {
        "gateId": "af-gate-claim-as-a-whole",
        "type": "source-gate",
        "code": "claim-as-a-whole",
        "claimHash": "sha256/c1:be97…",
        "reviewState": "internally-reviewed",
        "migrationState": "current",
        "review": {
          "by": "codex:gpt-5.6:019f8e90-cb24-7e33-a61b-5d867ebfa690",
          "operatorKind": "model",
          "date": "2026-07-23",
          "contentHash": "sha256/c1:55c2…"
        },
        "source": {
          "corpus": "af-claims",
          "block": "S019",
          "textHash": "sha256/c1:f6aa…"
        }
      }
    ],
    "c2": [
      {
        "gateId": "af-gate-example2-priority",
        "type": "source-gate",
        "code": "example2-priority",
        "claimHash": "sha256/c1:c88b…",
        "reviewState": "internally-reviewed",
        "migrationState": "current",
        "review": {
          "by": "codex:gpt-5.6:019f8e90-cb24-7e33-a61b-5d867ebfa690",
          "operatorKind": "model",
          "date": "2026-07-23",
          "contentHash": "sha256/c1:ca06…"
        },
        "source": {
          "corpus": "af-claims",
          "block": "S024",
          "textHash": "sha256/c1:830e…"
        }
      }
    ]
  },
  "fragments": {
    "c1u8": {
      "status": "mapped",
      "targets": [
        {
          "block": "S085",
          "textHash": "sha256/c1:dfee…",
          "role": "specific",
          "note": "Delivery of streams assembled from manifest-listed chunks"
        },
        {
          "block": "S149",
          "textHash": "sha256/c1:bf24…",
          "role": "context",
          "note": "Distribution step 260"
        }
      ],
      "reviewState": "internally-reviewed",
      "migrationState": "current",
      "review": {
        "by": "codex:gpt-5.6:019f8e90-cb24-7e33-a61b-5d867ebfa690",
        "operatorKind": "model",
        "date": "2026-07-23",
        "contentHash": "sha256/c1:07c9…"
      },
      "fragmentTextHash": "sha256/c1:ad3e…"
    },
    "c1u11": {
      "status": "mapped",
      "targets": [
        {
          "block": "S083",
          "textHash": "sha256/c1:dd0e…",
          "role": "specific",
          "note": "Algorithm analyzes camera-cut timings in the suspect and devises time codes"
        },
        {
          "block": "S071",
          "textHash": "sha256/c1:b05d…",
          "role": "context",
          "note": "Detecting camera-switch timings in the suspected distribution"
        }
      ],
      "reviewState": "internally-reviewed",
      "migrationState": "current",
      "review": {
        "by": "codex:gpt-5.6:019f8e90-cb24-7e33-a61b-5d867ebfa690",
        "operatorKind": "model",
        "date": "2026-07-23",
        "contentHash": "sha256/c1:65b1…"
      },
      "fragmentTextHash": "sha256/c1:2acd…"
    },
    "c23u7": {
      "status": "counsel-review-required",
      "reviewState": "internally-reviewed",
      "migrationState": "current",
      "review": {
        "by": "codex:gpt-5.6:019f8e90-cb24-7e33-a61b-5d867ebfa690",
        "operatorKind": "model",
        "date": "2026-07-23",
        "contentHash": "sha256/c1:3ecd…"
      },
      "fragmentTextHash": "sha256/c1:21b1…"
    }
  },
  "dispositions": [
    {
      "gateId": "af-gate-claim-as-a-whole",
      "subject": {
        "kind": "claim",
        "id": "c1"
      },
      "disposition": "carried-at-required-scope",
      "gateEntryHash": "sha256/c1:a61a…",
      "subjectHash": "sha256/c1:be97…",
      "reviewState": "internally-reviewed",
      "migrationState": "current",
      "review": {
        "by": "codex:gpt-5.6:019f8e90-cb24-7e33-a61b-5d867ebfa690",
        "operatorKind": "model",
        "date": "2026-07-23",
        "contentHash": "sha256/c1:174f…"
      }
    },
    {
      "gateId": "af-gate-production-boundary",
      "subject": {
        "kind": "claim",
        "id": "c1"
      },
      "disposition": "carried-at-required-scope",
      "gateEntryHash": "sha256/c1:57ad…",
      "subjectHash": "sha256/c1:be97…",
      "reviewState": "internally-reviewed",
      "migrationState": "current",
      "review": {
        "by": "codex:gpt-5.6:019f8e90-cb24-7e33-a61b-5d867ebfa690",
        "operatorKind": "model",
        "date": "2026-07-23",
        "contentHash": "sha256/c1:27a9…"
      }
    }
  ]
}
```

A third case in the required disposition fixture exercises the **`no-target-recorded` gate
disposition**: a
`counsel-review-required` fragment listed by a mandatory target-scope gate, released without
any fabricated mapping. It is one of the five cases required by §8.1.
The fixture is generated with truthful `operatorKind: tool`; it proves the disposition
policy's structural releasability but is not itself authorization evidence.

Optional per-target `role` is a closed descriptive enum — `specific` | `context` |
`combination` — with no legal implication. An optional `rationale` may accompany a target:
plain text, maximum 1 000 characters, whose declared purpose is explaining target selection —
never asserting legal sufficiency; rendered only in the flat mapping schedule. Duplicate
targets within a single unit-or-phrase owner are schema-invalid. Cross-edition reuse
proposals (§10) carry
`proposedFrom` provenance and enter as `reviewState: pending`. `proposedFrom` has one closed
shape and no additional fields: `{sourceEdition, fragmentCorpus, targetCorpus, owner,
contentHash}`, where `owner` is exactly `{kind, id}`, `kind` is `unit | phrase`, all strings
identifying editions or corpora use lowercase stable-id syntax, `id` matches its declared
kind (`c<n>u<n>` for a unit,
`c<n>u<n>p<n>` for a phrase), and `contentHash` is one full lowercase
`sha256/c1:<64 hex>` digest pinning the reviewed source owner. These are local syntactic
checks only: a single-edition build cannot authenticate the named source edition, corpora,
owner, or digest. Once created,
`proposedFrom` is immutable provenance: authorized-operator approval changes the destination owner's
lifecycle and review metadata but neither deletes nor rewrites this record. Its continued
presence after approval is valid authoring data and does not itself keep the owner
`pending`; however, **while the pair-scoped `propose-reuse` verifier is deferred, any owner
carrying `proposedFrom` is unconditionally non-releasable**. Local review cannot be
misrepresented as verification of the unread source side.

### 8.4 Statuses, review states, migration states — lifecycle by ownership

Lifecycle state lives on the **reviewed owners**: units, phrases, claim-gate assignments,
and gate dispositions. **Field applicability is declared in schema, not prose:** `status`
applies to units and phrases only; `reviewState`, `migrationState`, and `review` apply to
every owner type. Per-owner identity (used in review projections and all external
references): **unit** = relation binding + fragment corpus + fragment ID; **phrase** = unit
identity + phrase ID; **claim-gate assignment** = relation binding + claim ID + gate ID;
**gate disposition** = gate ID + subject identity. Targets and cautions are owned
sub-objects with no lifecycle of their own; any endpoint change in an owned sub-object
stales its owner. The relation schema also declares ownership boundaries: phrases are
independent reviewed owners, so a unit's review projection stops at the `phrases` boundary
rather than silently absorbing a child owner's lifecycle and content.

- `status: mapped | counsel-review-required` — recording state only (§5.3). `targets` may
  exist only when `mapped`; a `mapped` fragment must have ≥ 1 target.
- `reviewState: pending | internally-reviewed` — internal authoring progress.
  `review` is the closed required object `{by, operatorKind, date, contentHash}`. A new
  migration proposal carries the exact non-authoritative placeholder
  `{by: migrate, operatorKind: tool, date: "", contentHash: ""}` while it is `pending`;
  every `internally-reviewed` owner instead requires the complete metadata below;
  `operatorKind` is exactly `human | model | tool`, `by` names the operator, and `date` is a
  real calendar date in canonical `YYYY-MM-DD` form. Human and model operators are
  release-authoritative only when `by` is an explicit NFC identity with no surrounding
  whitespace or Unicode control/format characters and at least one visible character;
  both retain their truthful kind. Tool work may record internal progress, but
  **`operatorKind: tool` is never release-authoritative**. Missing, blank, invisible-only,
  unknown, and malformed kinds or identities are likewise non-authoritative.
  **`review.contentHash`** is the domain-tagged digest over the owner's **review
  projection** (§13): all ship-visible fields except declared locators, the hidden binding
  endpoints (`fragmentTextHash`, target and caution-source `textHash`es, aggregate
  `claimHash`, and for phrases the parent fragment's hash), **the owner's identity tuple**,
  and **the owner claim's dependency-chain hash** (§8.2). Consequences, all intended: any
  reviewed content or endpoint change — visible or hidden — invalidates
  `internally-reviewed`; transplanting a reviewed entry to a textually identical fragment
  in another claim or edition invalidates it (AF claims 1 and 19 contain verbatim-identical
  units, and NA claim 16's detect/derive units are byte-identical to AF claim 1's — the
  case is real both within and across editions); **amending a parent claim invalidates the reviews of all
  its dependents** — deliberate churn; and **mechanical re-anchoring does not** (target,
  caution-source, and gate-inventory source block ids are declared locators outside their
  review projections, their identity covered by the included `textHash` and, where
  ambiguous, contextual identity, §13). Reuse proposals always enter as `pending`; local authorized-operator review
  may record them as `internally-reviewed` while retaining `proposedFrom`, but the release
  predicate still rejects them until pair-scoped source verification is implemented.
  `review.by`, `review.date`, and `review.operatorKind` are
  `review: exclude`: recording reviewer metadata changes no digest — the git commit is the
  trust root for who reviewed (§10).
- `migrationState: current | stale` — `stale` is set only by `migrate` (§10) with a
  closed-enum `reason`: `changed | ambiguous | fragment-removed | target-removed |
  target-changed | source-changed | endpoint-changed | unclassified` — and preserved prior
  state (`previousTargets` for fragments); forbidden in a release. Ancestor-claim changes
  surface as `endpoint-changed` on affected dependents.
- The **release predicate** — every owner carries its applicable lifecycle fields with
  valid `contentHash`, `reviewState: internally-reviewed` and `migrationState: current`
  everywhere, plus an identified reviewer satisfying the canonical identity rule above
  with explicit `operatorKind: human | model` and a real canonical review date, and, while
  the pair-scoped verifier is deferred,
  no `proposedFrom`; gate
  referential integrity and dispositions satisfied — is defined once, in
  the schema/invariants module consumed by both the validator and the tests.

### 8.5 Cautions — closed types × closed scopes × closed codes; declared keys

Cautions are structured `{gateId?, type, code, source?}` and attach at exactly three scopes —
**target**, **fragment**, **claim** (`claimGates`) — under a schema-enforced compatibility
matrix:

| | target | fragment | claim |
|---|---|---|---|
| `source-gate` | valid (gateId required) | valid (gateId required) | valid (gateId required) |
| `generalization-note` | valid | valid | **unrepresentable** |

- `source-gate` — a gate enumerated in the gate inventory (§8.1); `gateId` and `source` are
  mandatory at every scope; the instance must match its inventory entry (code, scope,
  source), and its owner must be one of the hashed subjects in that entry's `appliesTo`.
  Merely resolving a `gateId` is not applicability. The only permitted scope mismatch is a
  target-required gate carried at fragment scope for an applicable
  `counsel-review-required` fragment with a matching reviewed
  `carried-at-fragment-fallback` disposition; there is no other fallback. The UI quotation
  is **derived at build time from the pinned source block — never
  stored**; the source digest is the normative review input. A changed source hash stales
  the owner (§8.4). The priority-support maps and crosswalk are `internal` and can never be
  quoted. QA-cross-check divergences are recorded in QA metadata or resolved by downgrading
  the affected fragment to `counsel-review-required` — never rendered.
- `generalization-note` — an author-observed, purely textual observation; no source; renders
  the approved microcopy registered for its `code`.

**Declared uniqueness keys** (every collection declares its identity; validated centrally):
gate assignments unique on `(ownerId, gateId)` per scope and on
`(ownerId, targetBlock, gateId)` at target scope; gate dispositions unique on
`(gateId, subjectKind, subjectId)`; phrase ids unique within their fragment; and target blocks
unique within each unit-or-phrase owner. The unit and each phrase are intentionally separate
ownership domains: the same block may be recorded for both with independently reviewed
notes, but may not be duplicated within either owner. Here `ownerId` is the exact unit or
phrase ID, not the enclosing fragment collapsed across the ownership boundary. Mandatory
target-scope cardinality counts distinct target blocks across the applicable fragment, so a
block recorded under both owners is not double-counted as two pieces of evidence.

**Caution codes are closed:** every `source-gate` code must exist in the applicable gate
inventory and selected edition strings resource; every `generalization-note` code must exist
in the shared generalization-code registry (`strings.json`) — enum exhaustiveness (§10) covers
types, scopes, and codes.

**Gate dispositions render only through registered microcopy** — one `strings.json` entry
per enum value, in neutral recording language (e.g. `carried-at-required-scope` → "Gate
recorded on candidate target"; `carried-at-fragment-fallback` → "Gate recorded on the
limitation — no candidate target recorded"). `no-target-recorded` renders as the structural
statement that no candidate target is recorded — never as a statement about the gate's
applicability, satisfaction, or any legal conclusion. Claim-scope gates display at the claim header and as the
**claim-level gate chip class**; "claim-as-a-whole" is one code among several; gates are
**never inherited down to units**. A gate covering several claims attaches to each gated
claim individually with the same pinned source and its own aggregate claim hash.

**Derived content is never stored:** quotations, the reverse index, labels, and counts are
computed at build time and have no schema fields; proposals to store a derivable are visible
as schema changes.

Unit indices are zero-based; `u0` is always the preamble. The UI renders `u0` as "preamble"
and `u{n}` (n ≥ 1) as "limitation n". No other **unit** numbering appears anywhere.

Schemas are versioned and closed (`additionalProperties: false`). The build accepts exactly
the schema version it ships with — no backward compatibility: when a schema changes, all
relation files are migrated in place in the same commit. The in-repo validator first
meta-validates every schema against its implemented keyword subset; an unknown/misspelled
keyword, unresolved `$ref`, open object shape, malformed constraint, or invalid regular
expression is fatal rather than silently ignored.

### 8.6 Edition configs

An edition config (`editions/na.json`, `editions/af.json`) is the **complete parameter
set** for one artifact: fragment corpus, relation set(s), target corpus, authoritative PDF
corpus (`authorityCorpus`), gate inventory, dependency map, normative census, display prefix
and label formats, forbidden-terms list, the required `priorityMap`/nullable `crosswalk`
QA-source bindings, output filename, provenance wording keys, legend references, and the
**declared transitive input set** used by the exact-set check (§10). The builder opens the
configured authority PDF through the registry and verifies its bytes against the registered
pin; authority provenance is not copied from metadata without that read. Declared inputs
must be unique, non-empty, canonical relative POSIX paths: absolute/drive paths, backslashes,
NULs, empty or dot segments, traversal, normalized aliases, and duplicate logical paths are
rejected before the gateway's exact-set comparison. The closed edition schema is
meta-validated and applied before any config-selected path or corpus id is dereferenced;
dependency, gate, relation, support-matrix, and segmentation instances are likewise
schema-validated before semantic consumers use their fields. Kernel and renderer read edition
knowledge from the config only (§10, edition-blindness).

## 9. Mapping methodology and QA (performed per edition)

1. **Seed.** The edition's own claim-set guidance is transcribed into the gate inventory,
   dependency map, and claim-level gate assignments. **AF is mapped independently; NA
   conclusions are never inherited.**
2. **Refinement to block level.** Each limitation unit and phrase is mapped — or explicitly
   statused `counsel-review-required` — by reading the claim language against the
   disclosure, per claim family; mandatory-gate dispositions recorded honestly (§8.1).
3. **Independent verification pass.** Every proposed target is re-checked adversarially
   against the block text; phrase substrings verified verbatim; status and disposition
   honesty confirmed. The pass receives the **complete pinned block texts — never
   truncated excerpts** — and every refutation is re-adjudicated against the pinned text
   before any data change: excerpt-induced refutation is a known failure mode of
   adversarial review.
4. **Completeness audit.** Gate referential integrity and dispositions pass in both
   directions; every owner has its applicable lifecycle fields and valid `contentHash`; the
   dependency map cross-validation passes; the mapping is cross-checked against the
   edition's priority-support map and — for AF — the crosswalk non-conflation boundary.
   The two-source inventory and QA cross-check attestations bind their exact declared side
   sets, and wording/data approvals bind their exact single side (§10). The typed `attest`
   command creates immutable attestation records. For validated-release only, `record-qa`
   consumes those attestations and creates the immutable QA record; technical-preview has no
   QA record. A change to any declared attestation side
   mechanically invalidates that attestation.
5. **Authorized-operator review.** Final pass by an identified human or model operator over
   each explicitly selected owner; `reviewState: internally-reviewed`, fresh `contentHash`,
   explicit `operatorKind`, and the operator's real canonical `YYYY-MM-DD` date are recorded.
   Tool work remains truthfully labeled and cannot authorize release.

### 9.1 Standing disclaimer (always visible on screen; repeated on every printed page)

The exact selected-profile `artifactLabel` precedes the disclaimer everywhere it appears,
including no-JS and every printed page. For the active profile it is: **“TECHNICAL PREVIEW —
Manual cross-platform and assistive-technology QA is deferred; browser and
assistive-technology compatibility is not validated.”**

> Draft navigation aid generated from claim-set {edition version} and PCT/IB2025/051755 as
> filed (WO 2025/181623 A1). Mappings are author-recorded candidate associations for counsel
> review — not a written-description, priority, or any other legal opinion. Fragments marked
> "counsel review required" carry no recorded candidate passage. Claim-level gates concern
> the complete claim and are quoted from the claim-set document. Anchor references are
> internal navigation labels, not official numbering, and must not be cited. This edition
> presents one candidate strategy; it does not compare strategies or recommend a filing
> choice.

The confidentiality legend accompanying this disclaimer is counsel-supplied text held in the
microcopy registry; its approval is an attestation bound to the digest of the approved
wording (§10). The same rule governs the bundle manifest's neutral description (§11).

## 10. Codebase architecture and guardrails

Goal: developers find the wrong thing hard and the right thing easy. The governing doctrine:
**promotion by verification, never by intention; enumeration over inference; requirements
live as data, not prose; associations pin both endpoints; mechanisms are closed over their
own data; boundaries are axes on one schema; planes never feed backward; derived content is
never stored; reviews cover content in context; evidence is append-only and chains forward
only; meta-rules bind themselves; policies are total over evidence states; invariant
exceptions are typed and justified; structural graphs are dual-sourced; attestations bind to
digests on their exact declared sides; every guarantee names its enforcer; the kernel is edition-blind and
separation between editions is enforced, not assumed.**

**Hard live-state boundary.** The checked-out tree supports exactly the schema, registry,
record, canon, claim-set, and artifact versions declared by its current normative data. There
are no compatibility aliases, legacy loaders, dual readers/writers, implicit upgrades, or
version-specific transition branches. Unsupported versions fail before writes. General
`migrate` behavior remains available only for content drift inside the current schema and
canon law. Current authored documents, configs, fixtures, bundle inputs, and distribution
artifacts state only the live baseline; Git is their sole history. Same-schema superseded
verification records may persist in the append-only store, but exact current-side matching
makes them incapable of authorizing current bytes.

```
navigator/
  corpora.json            # shared PCT registry: role, visibility, per-file sha256
  profiles/               # selected corpus/QA registries + edition strings;
                          #   segmentation profiles, gate inventories, dependency maps
  relations/
    na__pct.json       # NA relation set (binding: na-claims → pct-disclosure)
    af__pct.json       # AF relation set (binding: af-claims → pct-disclosure)
  editions/
    na.json               # complete NA parameter set incl. declared transitive inputs
    af.json               # complete AF parameter set incl. declared transitive inputs
  bundles/
    na-af-2026.json       # bundle config: enumerated members, versions, digests, manifest
  schema/                 # versioned, closed JSON Schemas with per-axis tags + declared
                          #   locator exceptions + applicability matrices + invariants
                          #   module; planes.json (command×kind privilege matrix);
                          #   acceptance.json (criteria registry); api-policy.json
                          #   (probed/CSP-governed/procedural API sets);
                          #   support-matrix.json (validated-release browser/OS/AT target policy)
                          #   + support-matrix.schema.json (closed matrix shape)
  strings.json            # shared artifact microcopy + counsel legend
  bundle-manifest.json    # version-2 bundle-only structured profile/status/deferred data
                          #   + neutral wording (digest-bound approval)
  build.py                # content plane: authoring `preview` / `candidate` / `migrate`;
                          #   verification plane: profile-explicit `release` / `bundle` / `attest` /
                          #   `record-qa`; `bundle-plan` / `status` /
                          #   `verify-current` (read-only proposal, report,
                          #   and hard current-state gate);
                          #   `propose-reuse` (deferred)
  tools/                  # authoring aids (action class d, outside the pipeline):
                          #   stamp (explicit selected-owner authorized review; separate
                          #   inventory pin operation), make_fixtures,
                          #   sync_tdd_examples, pre-commit-check
  tests/                  # golden parser + canon() + serialization vectors + property-
                          #   based canon tests, invariant + acceptance tests, registry-
                          #   access, edition-blindness, writer-set, diff-classifier,
                          #   projection, forbidden-terms, escaping fixtures, golden bundle
                          #   fixture, one five-case disposition fixture, locked scoped §3
                          #   edition-parameter fixtures, isolated synthetic NA migration snapshot,
                          #   traceability meta-test,
                          #   TDD-example and procedure-vs-matrix comparisons, per-edition
                          #   fixtures
```

**Action taxonomy.** A closed classification of what any tool may do to reviewed data:
(a) **read**; (b) **mechanical re-anchoring** — locator-field updates under
exact-hash-proven identity (relation locators and gate-inventory source locators alike),
semantic content and review state untouched — consistent by construction, since locators
are outside the review projection (§13); (c) **proposal writing** — new `pending` entries
and `stale` marks only; (d) **authorized-operator edit** via git. Attestation records are
written only by the typed `attest` command into the verification plane; validated-release
`record-qa` reads them and writes a QA record, while technical-preview creates none. Every command declares
its action classes; a **diff-classifier test** verifies observed writes fall within declared
classes. Before either source file is written, `migrate` also applies that same closed
classifier to deep snapshots of the relation set and gate inventory, validates both
resulting instances against their schemas, and aborts the entire write transaction on any
unclassified change. The only accepted deltas are existing locator replacements, exact
pre-migration `previousTargets` snapshots on stale owners, stale-state/reason updates, and
the exact pending-new-fragment proposal shape whose digest equals the current unit digest.
**No tool ever modifies the semantic content of a reviewed entry.**
`stamp` records, but does not infer, an authorized-operator decision: relation writes require
explicit owner selectors, identity, kind, and date; the separate inventory operation cannot
alter relation review state. A proposal's `proposedFrom` provenance remains byte-for-byte intact when its
destination owner is approved, and that locally approved owner remains release-blocked
until a pair-scoped verifier can authenticate the source side. `bundle-plan` is class (a)
only: proposal text on stdout does not authorize or perform the subsequent authorized-operator source
edit.

**Plane separation and privilege matrix.** Two planes; the privilege matrix is **normative
data** (`schema/planes.json`), genuinely command × kind — every kind has a declared plane
membership, cells enumerate exact kind sets, and an omitted privilege is a denied privilege.
Kind → plane: content plane — registered sources and policy data; artifact outputs —
`preview`, `candidate`, `sealed`, `bundle`, `bundle-manifest`, `artifact-checksum`,
`bundle-checksum`; verification records (append-only) — `qa-record`, `attestation`,
`release-record`, `bundle-record`.

Artifact-plane access additionally passes a central, closed kind/path check at the gateway:
all artifact paths are NFC root basenames, and the disjoint families are
`preview_<sealed-html>`, `candidate_<sealed-html>`, `<sealed-html>`,
`<sealed-html>.sha256`, `<bundle>.zip`, `<bundle>.zip.sha256`, and the exact
`MANIFEST.txt` for `bundle-manifest`. A path valid for one artifact kind is invalid for
every other kind; attaching a different kind label can therefore never overwrite or read
another kind's bytes. The AC-07 meta-test closes the artifact-kind set against this policy
and exercises both directions of the disjointness rule.

| Command | Reads (kinds) | Writes (kinds) |
|---|---|---|
| `preview` | `content` (edition allowlist) | `preview` |
| `candidate` | `content` (edition allowlist) | `candidate` |
| `migrate` | `content` (edition allowlist) | `source:relation-set` + `source:gate-inventory-locators` (action classes b + c only) |
| `propose-reuse` (deferred) | `content` (pair-scoped grant) | `source:relation-set-destination` (class c only) |
| `attest` | `content` + `attestation` | `attestation` |
| `record-qa` | `content` + `candidate` + `attestation` + `qa-record` | `qa-record` |
| `release` | `content` + `candidate` + `qa-record` + `attestation` | `sealed`, `artifact-checksum`, `release-record` |
| `bundle-plan` | `content` + `sealed` + `artifact-checksum` + `attestation` + `qa-record` + `release-record` | — |
| `bundle` | `content` + `sealed` + `artifact-checksum` + `attestation` + `qa-record` + `release-record` | `bundle-manifest`, `bundle`, `bundle-checksum`, `bundle-record` |
| `status` | `content` + `candidate` + `sealed` + `artifact-checksum` + `bundle` + `bundle-checksum` + `qa-record` + `attestation` + `release-record` + `bundle-record` | — |
| `verify-current` | `content` + `candidate` + `sealed` + `artifact-checksum` + `bundle` + `bundle-manifest` + `bundle-checksum` + `qa-record` + `attestation` + `release-record` + `bundle-record` | — |

Every cell above is an exact set, not a minimum or an illustrative subset; `content` is the
single content-plane kind narrowed by the row's declared scope, and an omitted kind is
denied. In particular, `bundle` must read each configured `release-record` and its exact
attestation predecessors, plus its `qa-record` predecessor only under validated-release; the
mere presence of a release record is not authority.
`record-qa` produces evidence only while validated-release is active, and `release` is
invoked as `release <edition> --profile=<technical-preview|validated-release>` with no
implicit profile.
`bundle-plan` has the same read boundary needed to evaluate current release chains but no
write privilege; its stdout is a proposal, not a content, artifact, or evidence write.
`verify-current` is the hard, read-only cutover gate: it exits nonzero unless pin plans,
candidate bytes, current-only version references, classified navigator sources, release and
attestation chains, the bundle config, deterministic ZIP, detached checksums, canonical
current-format record inventory, exact distribution inventory, Git whitespace, and the complete discovered
software suite all agree on one current baseline. `status` remains diagnostic and may report
partial state; it never substitutes for `verify-current`.

The `bundle-manifest` is counsel-facing and carries no verification-plane references; the
chain from bundle to its authorizing release records lives in the `bundle-record`.

`preview` in this command matrix is an **authoring artifact mode**, not a release profile.
It writes a watermarked file that is neither QA evidence nor delivery. Conversely,
`technical-preview` is a release-governance profile selected explicitly by `release
--profile=technical-preview`; it produces sealed, checksum-verified bytes and profile-labelled
records without claiming the deferred compatibility observations.

- **Content plane** — sources, relations, inventories, dependency maps, profiles, edition
  configs, schemas, strings projection, builder tree, declared timestamp. The builder tree
  is exactly `navigator/build.py`, `navigator/schema/invariants.py`, and the direct Python
  modules in `navigator/lib/`, enumerated as an explicit code-side 22-path inventory and
  compared bidirectionally with both edition declarations and the filesystem family. A
  declared Python path outside that inventory is rejected before either artifact provenance
  or the executable acceptance runner can read or hash-bind it; a `.py` suffix cannot appoint
  a new trusted implementation input.
  Every gateway
  path is one NFC, platform-neutral, canonical POSIX-relative identity: empty/dot/dot-dot
  components, normalization aliases, backslashes, controls, drive/stream separators,
  lexical escapes, in-tree symlink aliases, and symlink escapes are rejected. Content
  allowlists are validated before their first read and reject both noncanonical entries and
  duplicate/case-alias identities; no command (including `migrate`) relies on later edition
  validation to make an authored grant safe. Edition IDs are lowercase ASCII identifiers,
  never path fragments. The content gateway also rejects the terminal `navigator/dist/`
  artifact store and
  `navigator/records/` verification store even if an authored allowlist names them, so
  derived output cannot feed backward into a content lock.
  **content-input lock** is derived from the gateway's read log over this plane, sorted
  deterministically; **candidate and release must reproduce it byte-identically**. The
  gateway aborts if a path yields different bytes on repeated reads within one derivation,
  so a later read can never silently replace the digest of bytes already consumed. The
  **exact-set check** compares the read log against the edition config's declared
  transitive input set **in both directions**: an undeclared read fails, and a declared
  input that was never read fails.
- **Verification plane — append-only, forward-chaining.** Records are digest-addressed and
  immutable; every record filename carries its kind plus the complete 64-hex digest (never
  an abbreviated storage address), and an overwrite attempt is a gateway error; each record references its
  predecessors by digest. Under validated-release, `record-qa` creates the authorization
  record **before** release and `release` reads and references it. Under technical-preview,
  release has no QA predecessor. Both branches write the sealed artifact, its checksum, and a
  **`release-record`** (what was sealed, when, on which authorizations); the
  `bundle-record` references the release records of the bundle's members. Consumers
  resolve records by **explicit digest equality, never recency or record-store ordering**:
  validated-release considers only `qa-record`s whose candidate digest *and* content-lock
  digest match the derivation being sealed (a policy change can move the lock without moving
  the artifact bytes); technical-preview rejects any claimed QA predecessor. Every profile
  rejects incomplete authorization, and if several complete records remain deterministically
  prefers a valid human authorization, otherwise a valid model authorization, then uses
  canonical record-digest order as the tie-breaker. `bundle` resolves the exact
  `releaseRecord` digest pinned beside each sealed member in its config and then resolves
  release's exact profile-specific predecessors: attestations directly for technical-preview,
  or QA plus attestations for validated-release.
  Superseded records persist unchanged by design and match no current derivation;
  re-appending a byte-identical record is idempotent, since with digest-addressed names
  an identical write is not an overwrite. Attestation records additionally carry the
  edition id they attest for: an identity-affecting change orphans them by construction
  and fresh attestations are issued; the orphans persist like any superseded record.
  Release checks **attestation sufficiency, never universality**: for each required
  attestation type a current record with exactly its declared side set must exist; superseded
  attestations in the append-only store are ignored, not errors. Verification
  artifacts are never content inputs — circularity
  is unrepresentable in the matrix. The release or bundle command writes and reads back its
  artifact/checksum outputs first, then appends the authorized-operator outer record last;
  a failed
  postcondition may leave unauthorizing artifact bytes but can never leave a passed outer
  record. **The §13 update procedure's write-statements are
  validated against `planes.json` by the procedure-vs-matrix comparison test** — prose
  about who writes what is checked, not trusted.

**Authorized-operator evidence and release profiles are closed and structured.** `attest`,
`record-qa`, `release`, and `bundle` require an explicitly supplied, non-empty `NAV_OPERATOR`
and an explicit `NAV_OPERATOR_KIND=human|model`; tools, defaults, missing identities, and
unknown kinds are not accepted as authority. An identified operator is NFC, has no
surrounding whitespace or Unicode control/format characters, and contains at least one
visible character. Every authorizing record has `approvalStatus: passed`, an identified
operator, and its truthful `operatorKind`; authorizing evidence text must be non-empty and
final, and failure, rejection, skipped, pending, or do-not-release language invalidates it.

Acceptance version 2 / runner version 2 declares one explicit `activeReleaseProfile` and an
exact ordered two-entry `releaseProfiles` list. Each profile has exactly `{id,
manualQaEvidence, compatibilityAuthorization, deferredObservations,
requiredQaRecordFields, artifactLabel}`. The active profile is `technical-preview`, whose
manual QA is `deferred`, compatibility authorization is `not-authorized`, deferred set is
exactly `[AC-11, AC-12, AC-13, AC-15]`, required QA fields are exactly empty, and artifact
label is the exact sentence in §1. `validated-release` has manual QA `required`,
`support-matrix-authorized`, no deferred observations, required fields exactly `[ac11, ac12,
ac13, ac15]`, and label **“VALIDATED-RELEASE PROFILE — Delivery requires current full
seven-row cross-platform and assistive-technology QA.”** AC-14 is deliberately absent from
both the deferred set and the manual field set: its static no-JS completeness proof is
automated under both profiles.

Every attestation carries the exact closed producer marker
`producerCommand: "navigator/build.py attest/v1"`; a missing or unknown marker is rejected.
This digest-bound marker represents the typed attest-command output contract under the
repository/Git trust root; it is audit metadata, not a cryptographic signature or proof of
who executed the command. Attestation side keys are exact: inventory completeness =
`{claimSet, gateInventory}`; priority QA = `{relationSet, priorityMap}`; AF crosswalk QA =
`{relationSet, crosswalk}`; legend approval = `{legendWording}`; manifest approval =
`{manifestWording}`; support-matrix target-policy approval = `{supportMatrix}`. These content
and policy attestations remain required under both profiles; support-matrix approval approves
the future validated-release target policy, not evidence that its rows were exercised.

The `technical-preview` chain has **no QA record prerequisite and creates no QA record**.
The release command still runs every automated acceptance callback and requires current
content, lifecycle, attestation, determinism, security, privacy/offline, and output-integrity
evidence. Its release record carries the exact `releaseProfile`,
`compatibilityAuthorization`, `deferredObservations`, and `artifactLabel`; none of those
fields may be omitted, inferred, or relabelled as compatibility authorization. The eventual
bundle record carries those same four exact selected-profile values; the bundle config adds
only `releaseProfile`, while the structured manifest exposes the profile, compatibility
status, deferred set, and exact label to recipients.

A `qa-record` exists only for `validated-release`. It is candidate-bound, explicitly carries
`releaseProfile: "validated-release"`, declares `manualEvidenceVersion: "3"`, and contains
exactly the structured operator-performed fields `ac11`, `ac12`, `ac13`, and `ac15`; each has
`status: passed`, non-empty final evidence, and the same operator identity and kind as the
outer QA record. The version-3 grammar is decisive rather than free-form: AC-11 and AC-13
copy every current atomic support-matrix target in exact normative order and record actual
browser/OS/AT versions in their canonical product/version grammar, with minimum versions
enforced; AC-11 additionally records the configured traversal chord and typed keyboard,
focus, computed-semantics, and live-region results; AC-13 records the exact minimum and an
actual below-minimum viewport with typed local-file and layout results. AC-12 records the
actual print engine, positive page count, and typed readable-claims, readable-disclosure,
disclaimer-on-every-printed-page, legend-on-every-printed-page, provenance, schedule, and
no-content-clipping results. AC-12 and AC-15 browser/OS environments must match a current
`at: none` support target and meet its minimum versions. AC-15 records the actual runtime,
`ready: true`, the exact installed/no-error hook map, and exact empty
attempt/resource/network/cookie/storage/IndexedDB/navigation ledgers. Missing, extra,
duplicate, reordered, stale-target, failed, or malformed results are not authorization.

`record-qa --template` prints a deliberately pending validated-release version-3 skeleton
derived from the live support targets, minimum viewport, and API-probe set; it requires no
operator identity and writes nothing. An operator may supply the completed object with
mutually exclusive `--evidence-file=<workspace-relative.json>` input, which is read through a
fresh confined gateway and excluded from both candidate and QA-input locks, or retain the four
inline `--acNN=<JSON>` arguments. `--check-only` requires the explicit operator identity and
kind, performs the same candidate, attestation, and full validated-release authorization
self-check as append mode, prints the prospective digest, and writes nothing. Append mode
validates that same complete constructed QA record before writing it. The record references
exactly one current `inventory-completeness`, `qa-priority-map`, `legend-approval`, and
`support-matrix-approval` attestation (AF additionally requires `qa-crosswalk`); the
`manifest-approval` attestation is bundle-only. The QA record embeds the approved legend and
support-matrix bindings and carries both locks described below. A validated-release record
repeats the exact QA attestation set and cannot authorize different candidate bytes, a
different lock, or an unapproved side.

**Executable acceptance evidence is closed, current, profile-labelled, and nested rather
than a new record kind.** Every `release-record` and `bundle-record` has a required
`acceptanceReceipt`; the outer record remains identified human/model authorization, while the
receipt truthfully identifies its executable runner as `runnerKind: tool`. A tool runner
supplies executable evidence but is never authoritative. The receipt's exact closed fields
are `{receiptVersion, registryDigest, runnerDigest, runnerInputs, runnerEditions, runnerKind,
releaseProfileContract, results, subjects}`. `releaseProfileContract` is the complete exact
selected entry copied from the version-2 registry, so the receipt itself binds the profile
id, compatibility status, deferred set, manual-evidence policy, required fields, and artifact
label:

- `receiptVersion` is `"2"`; `registryDigest` is the ordinary raw-byte SHA-256 digest of
  the exact `navigator/schema/acceptance.json` bytes, including its closed
  `receiptPhases` map.
- `runnerEditions` is the exact sorted selected edition set: one edition for a standalone
  release and both configured editions for the bundle. `runnerInputs` is the exact
  path-sorted `{path, digest}` lock over every Python input in the selected edition builder
  input set(s), plus every registry-declared test module and support file, every shared
  fixture, and only the fixtures scoped to a selected edition. The registry's closed
  `runner` object declares `runnerVersion: "2"`, `manualQaEvidenceVersion: "3"`, the exact
  active/two-profile policy, its supported editions,
  fixture edition scopes, and callback edition scopes as data, together with the live acceptance and canonicalization modules,
  the TDD, excerpt/disposition/escaping/golden/edition-parameter/migration fixtures,
  canonical vectors, package initializer, and the fixture-generation, TDD-sync, and
  review-stamp tools. An independent exact
  floor of field-specific c1 lock commitments inside the already content-locked
  edition-blind `lib/release.py` fixes the complete
  supported-edition, module path, fixture path→scope, callback-scope, support-file,
  active/two-profile policy, manual-QA-evidence-version, and per-criterion
  callback/validated-release-QA-field inventories before any registry-selected callback is
  imported; callback ownership is unique. Thus deleting or redirecting the AC-19 callback
  cannot remove the auditor, and a registry entry cannot shrink its own lock. The floor
  compares inactive-edition metadata but does not open or hash inactive-edition fixture
  bytes.
  `runnerDigest` is the c1 object-composite digest with tag `aa11393:lock:c1` and payload
  `{runnerVersion: "2", runnerEditions, registryDigest, runnerInputs,
  releaseProfileContract, plans: receiptPhases}`. The selected-edition/profile context is
  snapshotted before execution,
  recomputed in an isolated fresh interpreter with an empty bytecode-cache location before
  any registered test module is imported, and recomputed again after execution; any
  registry, runner-edition, release-profile, or active runner-input change aborts the transaction. An
  inactive edition's fixture is neither opened nor bound by a standalone run.
- Release `results` is exactly
  `[{phase: "release-preflight", criteria: ["AC-01" … "AC-19"], status: "passed"},
  {phase: "release-postcondition", criteria: ["AC-16"], status: "passed"}]`.
  Registered fresh-interpreter callbacks execute AC-01–AC-15 and AC-17–AC-19, filtered by
  their declared edition scopes, including the individually registered canonical
  golden/property tests. Every `test_acceptance` method name begins with its owning
  criterion's `test_acNN_` identity; only AC-07 may own `test_canon` callbacks, preventing a
  set-preserving criterion swap. The synthetic migration callback and fixture are NA-scoped. The
  split AC-16 checks prove both pre-write reproducibility and post-write sealed/checksum
  readback.
  Release `subjects` always bind `{edition, candidateDigest, contentLockDigest,
  releaseProfile, compatibilityAuthorization, deferredObservations, artifactLabel}`.
  `technical-preview` has no QA predecessor. `validated-release` additionally binds the
  exact `qaRecord` and `qaInputLockDigest`.
- Bundle `results` is exactly
  `[{phase: "bundle-postcondition", criteria: ["AC-20"], status: "passed"}]`; it is
  produced only after manifest, ZIP, and checksum write/readback and deterministic member
  verification, followed by execution of the registry-named AC-20 callback in the same
  isolated fresh-interpreter runner. The callback consumes a closed transaction context
  containing the exact evidence collections and independently derived current per-edition
  acceptance, profile, attestation-side, and candidate/content-lock bindings. For
  `technical-preview` it proves that no QA predecessor is claimed; for `validated-release`
  it additionally consumes the exact QA, support-approver, target/viewport, API-probe, and
  manual-evidence bindings and re-resolves every release→QA→attestation chain. Both profiles
  independently re-resolve the identified authorized-operator manifest approval rather than
  trusting the previously resolved plan.
  It also reads back
  the just-written outputs and rechecks exact configured members, STORE and deterministic
  ZIP form, detached checksum, neutral manifest, release references, and the golden bundle
  fixture; callback failure prevents receipt creation. Bundle `subjects` binds
  `{bundleConfigDigest, bundleDigest, releaseRecords, members: [{name, digest}],
  manifestApproval, releaseProfile, compatibilityAuthorization, deferredObservations,
  artifactLabel}`.

No receipt contains its enclosing record's digest. Typed predecessor authorization digests
(`releaseRecords`, `manifestApproval`, and, only for validated-release, `qaRecord`) point only to already existing
records, and all other subjects are facts known before the outer record is hashed, so the
verification graph remains acyclic.

Guardrails, each tied to the failure it prevents:

1. **Closed, versioned schemas** — typo'd fields and ad-hoc semantics fail loudly.
2. **Conditional schema rules** (§8) — inventing targets, targeting editorial blocks,
   referencing `internal` corpora from the UI, duplicate targets/gate instances/
   dispositions (declared keys, §8.5), unsourced or inventory-orphaned source-gates,
   claim-scope generalization-notes, entries outside the declared binding, or applicability
   violations (status on a gate assignment) are unrepresentable.
3. **Single canonicalization module for every digest** (§8.2) — text rules, the completed
   canonical-JSON law (vendored Unicode 15.1 tables, raw and post-NFC duplicate-key
   rejection at parse time, exact escapes, integer-only safe range, raw-digest
   composition), and NUL-framed domain tags versioned together; a test asserts no digest is
   computed elsewhere.
4. **Gateways for all file traffic, in two planes** (matrix above), enforced by the
   registry-access AST test and review; cross-edition reads only as pair-scoped grants.
5. **Requirements as data, closed both ways, total over evidence states.** Gate coverage is
   bidirectional referential integrity over instances *and dispositions* (§8.1); a
   mandatory requirement is never satisfiable only by creating evidence; censuses,
   forbidden terms, output kinds, declared transitive inputs, privilege rows, API policy,
   support matrix, acceptance criteria, and bundle membership are enumerated data; **all
   projections are derived from schema axis tags with declared, justified exceptions**
   (§13). Declared input identities are duplicate-free canonical safe relative paths, and
   the gateway rejects aliases, duplicates, lexical escape, or symlink escape at construction
   or access even if malformed reviewed data reaches a command that does not run full edition
   validation.
6. **Migration by closed case table** (`migrate`: classes b + c; idempotent; never guesses;
   staleness rolls up to the owning reviewed object; every unlisted situation degrades to
   `stale / unclassified`):

   | Situation | Action |
   |---|---|
   | Exactly one eligible canonical-hash match at a new position | Mechanical re-anchoring: locator fields only (relations and gate inventories); semantic content and review state untouched |
   | No match — fragment text changed | Owner `stale` / `changed`; `previousTargets` retained |
   | Multiple matches — repeated text (expected: identical EDL rows; description recitals verbatim-identical to PCT claim elements) | Owner `stale` / `ambiguous` |
   | Source fragment removed | Owner `stale` / `fragment-removed`; an identified authorized operator deletes the entry in the resolving commit |
   | Target block removed (fragment still exists) | Owning fragment `stale` / `target-removed`; an identified authorized operator re-targets or downgrades to `counsel-review-required` |
   | Target block text changed | Owning fragment `stale` / `target-changed`; `previousTargets` retained |
   | Caution-source block removed or text changed | Owning fragment or gate assignment `stale` / `source-changed` |
   | Claim text changed (aggregate hash mismatch), ancestor claim changed (dependency-chain mismatch), or gate endpoints changed | Affected owners `stale` / `endpoint-changed` |
   | New fragment appears | Entry created as `counsel-review-required` + `pending` |
   | canonVersion mismatch on the relation binding | Reject before loading or writing; re-author the relation under the current canon law |
   | Splits, merges, anything not listed above | Owner `stale` / `unclassified` |

   Sequential locators make removal observable only where the locator itself
   disappears (a container-tail deletion): a mid-document deletion re-fills the
   locator with the shifted successor, so the vanished digest mechanically classifies
   as `target-changed` — equally reviewed, equally honest.

   The migration diff classifier is a runtime pre-write guard, not merely a test oracle.
   The registered AC-07 scenarios run it over each synthetic case-table result and include
   negative mutations of semantic and review fields; a classifier or schema defect leaves
   both authored files byte-for-byte untouched.

7. **Cross-edition reuse — deferred, bounded.** `propose-reuse` (class c only): explicit
   source and destination editions; pair-scoped read grant per invocation; proposals only
   into the destination; full source digests recorded; never during an edition build. The
   crosswalk is review context and a non-transfer warning. Authorized-operator approval clears the
   destination owner's pending state but retains its exact immutable `proposedFrom` record;
   no authoring tool rewrites or removes that provenance. Because the command and its
   pair-scoped verifier are deferred, the current release predicate rejects every
   `proposedFrom` regardless of otherwise-current local review metadata.
8. **Profile-explicit release by verification (candidate → sealed), per edition.** `release
   <edition> --profile=<technical-preview|validated-release>` has no implicit profile and
   refuses a selection that is not the registry's explicit active profile. It re-derives,
   verifies the content-input lock byte-identically, byte-compares the candidate, verifies
   every exact-side content/policy attestation in the verification envelope, and executes
   the registered `release-preflight` acceptance plan. `technical-preview` has no QA-record
   prerequisite; `validated-release` additionally verifies the candidate-bound QA input lock
   and full version-3 record. The command promotes the same bytes with the exact profile
   artifact label, reads back the sealed artifact and checksum, executes the AC-16
   `release-postcondition`, and only then appends the identified authorized human/model
   release record carrying the exact profile contract and current non-authoritative tool-run
   acceptance receipt. The separate authoring `preview` command is watermarked “not for QA or
   delivery” and passes the identical shipping projection — the watermark is additive, never
   release authority and never the `technical-preview` profile label.
9. **Composition planning and sealing.** `bundle-plan` is a read-only bridge from two
   independently current releases to the explicit bundle config. It derives each edition's
   current candidate digest and content-lock binding from content, verifies the stored
   sealed/checksum bytes, and considers only release records whose exact current
   side/profile/attestation/**acceptance-receipt** chain validates. For a validated-release
   chain only, it independently reproduces the selected-registry-bound `qaInputLock` from
   current private inputs and compares the support-matrix approver, exact ordered atomic
   targets/viewport, current API probe set, and locked manual-evidence version from live
   inputs; it does not accept QA-record copies as self-authenticating currency evidence. A
   technical-preview chain must have no QA predecessor and must carry the exact deferred
   observation set and not-authorized compatibility status. It likewise resolves only a
   current identified authorized human/model manifest approval, then validates the proposed config through
   the same final member resolver used by `bundle`. If multiple release records (or manifest
   approvals) authorize the same current subject, selection is deterministic: prefer valid
   human authorization, otherwise valid model authorization, then use canonical digest order
   as the final tie-breaker. An existing explicit config pin is preserved only when it is that
   selected winner; recency is never authority. It emits canonical proposed JSON to stdout
   only — never writing the config,
   artifacts, approvals, or evidence. An identified authorized operator inspects and applies
   that proposal as an ordinary reviewed source edit.

   `bundle` builds a **deterministic STORE ZIP** from the single
   in-repo writer (fixed member ordering, real canonical RFC 3339 UTC-second declared
   timestamps—with an even second and DOS-range year for ZIP metadata—fixed permissions, pinned
   UTF-8 filename flags and central-directory behavior — verified against a **byte-exact
   golden bundle fixture**) from the explicit, closed version-3 bundle config. The config
   carries its exact `releaseProfile` and pins the
   exact ordered edition/member set; every member's kind, name, and byte digest; the exact
   stored detached-checksum bytes and their sealed artifact; each sealed member's
   digest-addressed release record; the manifest's byte and wording digests; and the exact
   identified authorized human/model manifest-approval attestation. The version-2 manifest
   carries structured profile, compatibility-status, deferred-observation, and exact
   artifact-label fields together with its neutral text. Member names are safe
   NFC root basenames,
   unique case-insensitively, conform to their central artifact-kind path families (the
   manifest is exactly `MANIFEST.txt`, and every stored checksum is exactly
   `<sealed-name>.sha256`), and may not collide with the bundle or bundle-checksum output.
   Before writing any output, `bundle` verifies every stored member and the complete
   authorized profile-specific release chain, including a current release acceptance receipt.
   A technical-preview member resolves directly from its release record to current exact-side
   attestations and has no QA predecessor. A validated-release member additionally resolves
   `release-record → qa-record → attestation`; for every edition it independently re-reads the
   selected QA registry and pin-verified QA sources to reproduce the exact current
   `qaInputLock`, and re-reads the current support-matrix approver, exact ordered atomic
   targets/viewport, API probe set, and manual-evidence version, then independently
   revalidates every typed AC-11/12/13/15 result. Copied QA-record values are not their own
   currency proof.
   Pending/legacy evidence is not authority. It then emits and reads
   back the manifest, deterministic ZIP, and detached ZIP checksum, runs the AC-20
   `bundle-postcondition`, and appends the identified authorized human/model bundle record
   with its non-authoritative tool-run receipt last.
10. **Content lock, optional validated-QA lock, and verification envelope** (plane separation
    above). Both profiles carry a `contentLock`: the exact sorted content-gateway read set and
    its digest. A validated-release private QA record separately carries a candidate-bound
    `qaInputLock`: the raw selected QA-registry
    path/digest, verified internal QA-source reads, candidate digest, and `contentLock`
    digest, with its own lock digest. The other edition's QA registry is never opened.
    **Runtime diagnostics live in a sibling
    `reproductionDiagnostics` section — outside both lock digests and the candidate↔release
    equality check** (interpreter version, locale, platform settings; non-normative;
    byte-identity remains the authority). Safe subset
    (relation/edition/inventory/strings-projection digests, builder source-tree hash) in
    embedded provenance. **Honest limit:** the locks make policy drift visible,
    attributable, and attestation-invalidating — it cannot make modification impossible;
    the reviewed git commit remains the trust root.
11. **Central microcopy resources with digest-bound approvals.** Shared artifact microcopy
    is in `strings.json`; source-gate labels are in the selected edition strings resource;
    bundle-only neutral wording is in `bundle-manifest.json`. Approvals bind to wording
    digests without making bundle-only or other-edition wording an edition content input.
    The support matrix is
    separately byte-digested, names its approver, and is bound by an identified authorized
    human/model
    `support-matrix-approval` attestation as approval of the validated-release target policy;
    a validated-release QA record pins that digest, approver, and attestation digest, while
    technical-preview does not claim it as observed compatibility evidence. Authored
    per-entry text (notes, rationales) is subject to the same
    neutrality and forbidden-terms checks.
12. **Terminology guard, full authored-visible surface.** Forbidden-terms checks cover the
    complete shared-plus-selected-edition strings projection, target notes and rationales,
    visible edition
    display/strategy/prefix/version metadata, and public provenance corpus
    identifiers/roles/versions. Pinned claim, disclosure, phrase, and gate-source quotations
    are excluded because they are verbatim rather than authored UI text. A maintained
    heuristic sourced from the registered crosswalk.
13. **Enum exhaustiveness.** Every closed enum that reaches presentation or diagnostic
    output (status, role, caution type, scope, code, gate disposition, and migration reason
    in migration diagnostics) has a registered presentation/diagnostic entry; build checks
    assert exact coverage **in both directions** — an enum value in
    use without a registered entry and a registered entry with no use both fail; the type×scope matrix, code closure, and
    applicability matrices (§8.4, §8.5) are schema-enforced.
14. **Edition-blindness.** Shared modules contain no edition tokens — AST/grep-test
    enforced.
15. **Generated-file discipline.** `GENERATED` banner + detached SHA-256 + local pre-commit
    rebuild-and-compare; repository ignore rules must not exclude the committed generated
    artifacts (stock ignore templates match `dist/` and `lib/` at any depth).
16. **Confidentiality guardrail.** Build aborts in CI environments; `--private-runner` is
    the logged override. An accidental-disclosure guardrail, not proof of runner trust.
17. **Documentation that cannot lie.** The §8.3 examples, the §14 criteria list, and the
    §13 procedure's write-statements are validated against their registered data (fixtures;
    `schema/acceptance.json`; `schema/planes.json`). The TDD is never a content-build input;
    it is deliberately locked as an executable-acceptance runner input so a receipt cannot
    survive drift in the contract it claims to execute.
18. **Traceability closure, self-binding.** Criteria carry stable IDs in
    `schema/acceptance.json`; the traceability matrix maps registry IDs to named tests or
    validated-release QA-record fields; the meta-test closes both directions over the
    registry, itself included, including the exact active/two-profile policy and the
    technical-preview deferred set. The same registry declares the exact `receiptPhases`
    sets, and its byte digest, selected profile contract, and locked runner inputs are embedded
    in every acceptance receipt.
19. **Collision review (procedural).** Every new mechanism folded into this document is
    checked against the guarantee → enforcement map for conflicts with existing mechanisms
    before adoption — at this density, the table's second function is collision detection.

**Quantifier discipline (procedural):** any universal claim in this document must either
cite a row of the guarantee → enforcement map or carry an explicit scope.

**Guarantee → enforcement map:**

| Guarantee | Enforcer |
|---|---|
| Unregistered, out-of-edition, out-of-plane, untyped, or cross-kind-path file access cannot occur in the pipeline | Registry accessor + typed output-kind registry + central disjoint artifact kind/path policy + command×kind privilege matrix (`planes.json`) + pair-scoped grants + registry-access/artifact-path meta-test |
| Silent re-anchoring cannot occur | Hash-pinned references (schema) + migration case table + diff-classifier test |
| Associations cannot silently re-aim | Both-endpoint pinning with lifecycle (schema) + migration rows |
| Every mandatory gate is carried or honestly disposed at its required scope and cardinality | Gate inventory + bidirectional referential integrity over instances and dispositions + declared uniqueness keys |
| An honest no-candidate fragment is releasable without a fabricated mapping | Closed gate-disposition enum incl. `no-target-recorded` + requiredScope×evidence-state totality matrix + one disposition fixture file containing five cases |
| The inventory reflects the prose gates | Digest-bound attestation by an identified authorized human/model operator, with kind stated explicitly; tool rejected |
| Reviewed status cannot outlive reviewed content, visible or hidden, or its context (owner identity, binding, claim ancestry) | Review projection derived from schema axes incl. identity tuples and dependency-chain hash + `contentHash` validation |
| Mechanical re-anchoring never invalidates review | Declared locator exception: `ship: artifact` + `review: exclude` permitted only with a named covering digest, unique in the eligible block set or supplemented by review-included contextual identity (schema) |
| Dependency-chain hashes rest on a validated graph | Authored dependency map cross-validated against parsed claim references (AF three-way against its document table); totality/acyclicity/root checks; mismatch fails the build |
| Attestations cannot outlive any declared side or masquerade as output from another producer contract | Exact-side digest binding + typed passed identified-authorized-operator append-only records + exact `producerCommand: navigator/build.py attest/v1` validation + envelope verification; the marker is digest-bound repository/Git audit metadata, not a signature |
| Evidence that authorized a release survives it unchanged; release outcomes are themselves recorded | Append-only verification plane + forward-chaining records incl. `release-record`; output readback before the outer record is appended last; overwrite is a gateway error |
| A release or bundle cannot claim an unexecuted, stale, or differently profiled acceptance suite | Required closed version-2 `acceptanceReceipt` + exact copied release-profile contract + registry-byte digest + explicit runner-edition set + registry-declared shared/edition-scoped test-module/fixture/support-file lock + fresh-interpreter before-import/after-run context equality + closed phase/result sets + typed profile/subject bindings |
| Provenance cannot be self-referential | Plane separation: verification artifacts are never content inputs (privilege matrix); receipts omit their enclosing record digest and typed predecessor subjects point only backward |
| Exactly the required inputs were read | Content read log + two-sided exact-set check against the edition config's declared transitive inputs (undeclared reads and unread declarations both fail) |
| Composite digests are implementation-independent | Completed canonical serialization law (vendored interpreter-independent Unicode 15.1 NFC/White_Space data, raw and post-NFC duplicate-key rejection, exact escapes, integer edge rules, two declared payload forms) + NUL-framed domain tags incl. per-record-kind tags + single-digest-path test + golden vectors + property-based canon tests |
| Derived content cannot drift | No-stored-derivables rule (schema has no fields for them) |
| Policy drift is visible and attestation-invalidating | Edition content-input lock derived from its exact gateway read log; validated-release additionally binds the raw selected-QA-registry and pin-verified QA sources in `qaInputLock` (visibility, not prevention — git commit is the trust root); diagnostics excluded from applicable lock digests |
| Tools act only within declared action classes | Action taxonomy + diff-classifier + writer-set tests |
| No automatic cross-edition inheritance | `propose-reuse` deferred, pair-granted, proposal-only; immutable `proposedFrom` survives local authorized-operator review, and its presence unconditionally blocks release until a pair-scoped verifier can authenticate the source side |
| Shared code contains no edition knowledge | Edition-blindness AST test |
| Released bytes = profile-authorized candidate bytes | Seal gate: content-lock reproduction + byte-compare + exact profile contract; validated-release additionally checks the current QA-record digest, while technical-preview expressly has no manual-QA prerequisite |
| No `pending` / `stale` / non-authoritative owner review / unverifiable `proposedFrom` / unapproved legend ships | Release predicate (invariants module) + attestation checks |
| Editorial / `internal` content never rendered or quoted; internal QA identifiers never ship; only public configured authority metadata may identify the non-rendered authority corpus | Visibility rules (schema) + provenance projection + projection test |
| Authoring-lifecycle fields never ship, in any artifact kind including previews | Ship-axis-derived projection (schema) + projection test |
| Bundle-config refresh cannot silently mutate source, switch profiles, or arbitrarily choose among current authorizations | Read-only `bundle-plan` + independently derived current candidate/content-lock/profile bindings + exact current attestation sides and receipt-chain validation; validated-release additionally verifies QA-input lock, support approver/targets/viewport, API probe set, and manual-evidence version; deterministic human-over-model, then digest, precedence; an existing pin survives only when it is the selected winner |
| A bundle contains exactly its enumerated members and only releases authorized for its explicit profile | Closed version-3 exact-member/checksum/manifest-approval/profile config + version-2 structured labelled manifest + deterministic STORE ZIP + golden bundle fixture + complete profile-specific release chain and current release-receipt verification + AC-20 postcondition receipt |
| AF/NA terminology non-conflation in authored text | Forbidden-terms check (heuristic, crosswalk-sourced) |
| Examples, criteria, and procedure statements in this TDD match their registered data | Fixture validation + TDD-comparison tests (fixtures; acceptance registry; privilege matrix) |
| Every registered acceptance criterion is carried by a live test, and every acceptance test maps to a criterion | Criteria registry + traceability matrix + bidirectional meta-test |
| The page attempts no network requests, cookie writes, Web Storage use, or navigation-API calls in the enumerated policy | CSP (§11) + self-auditing attempted-use instrumentation per `api-policy.json`; the exact hook ledger must be ready before an empty attempt log is evidence — governs the page; extensions and user actions are outside it; residual APIs marked CSP-governed or procedural in the policy file |
| Not built on hosted CI | CI-environment guard — procedural, not proof of trust |
| Deterministic output, artifact and bundle | Declared release timestamp + cross-process double-build comparison + STORE ZIP rules + golden bundle fixture |
| Universal claims in this document are scoped or table-backed | Procedural TDD-review discipline |
| New mechanisms do not collide with existing guarantees | Collision review against this table (procedural) |

**Future layers:** the corpus/relation/edition kernel accommodates provisional-support,
prior-art, and office-action data, and post-continuation claim-set versions, as data
additions reusing the same lifecycle, hashing, visibility, isolation, inventory,
disposition, plane, and attestation machinery by construction. **New kinds of views may
require new presentation components** — added through the same registered display-path and
enum-exhaustiveness discipline.

*Non-normative implementation order:* parser/canonicalization → schemas + inventories +
dependency maps → NA candidate → AF candidate + claim gates → sealing → bundle;
`propose-reuse` deferred.

## 11. Build output, security, and delivery

- **One self-contained HTML5 file per edition** (§3 default names). All CSS, JavaScript,
  shipped relation data (ship-axis projection, §13), disclosure text, and the four figures
  (base64 data URIs, 882,762 bytes total pre-encoding) inlined. Estimated size ≈ 1.5–2 MB
  each.
- **Build modes and profiles:** authoring `preview` (watermarked “not for QA or delivery,”
  same projection), `candidate`, profile-explicit `release`, and `bundle` — all
  **content-plane read-only** via the gateways, writing only their declared
  output kinds per the privilege matrix (§10); `attest`/`record-qa` write append-only
  verification records; `status` resolves and reports the current digest chain
  (which records authorize the current derivation and under which profile), writing nothing.
  The authoring mode named `preview` and the `technical-preview` release profile are not
  synonyms (§10.8).
- **Technical-preview delivery bundle:** a deterministic STORE ZIP containing exactly: both
  sealed, exact-profile-labelled artifacts, their detached checksums, and the **neutral
  version-2 structured manifest** (`bundle-manifest` output kind; microcopy-registry text,
  counsel-approvable) identifying them as *alternative counsel-review editions* and carrying
  the exact profile id, `not-authorized` compatibility status, `[AC-11, AC-12, AC-13, AC-15]`
  deferred set, and technical-preview artifact label; the bundle ships with its own detached
  checksum. Either
  artifact remains releasable alone. The ordered names and exact bytes are digest-pinned by
  the version-3 bundle config, whose `releaseProfile` is exact; each sealed member names one
  exact release-record digest, each stored
  checksum is verified rather than regenerated, and manifest wording must match the config's
  exact identified authorized human/model approval. Packaging proceeds only after both configured
  release→attestation chains and profile-bound receipts validate completely; the active
  technical-preview chain contains no QA record. Default bundle name visibly includes
  `TECHNICAL-PREVIEW`.
- **Network and runtime posture:** the application performs no network requests and
  attempts no use of the APIs enumerated in `schema/api-policy.json` (cookies,
  localStorage/sessionStorage/indexedDB, history/location mutation) — instrumented as
  **attempted use, not final state** (AC-15). The runtime exposes
  `window.__apiProbeStatus` with the exact sorted registered API set and a per-API
  `{status, error, detail}` installation result. Initialization throws after publishing
  that ledger unless every registered hook verifies as installed; QA may trust an empty
  `window.__apiAttempts` as validated-release observation only when the ledger is exact and
  `ready: true`; technical-preview still executes the automated instrumentation and
  fail-closed harness but defers the actual-browser ledger observation. CSP —
  `default-src 'none'; img-src data:;
  style-src 'unsafe-inline'; script-src 'unsafe-inline'; base-uri 'none'; form-action
  'none'; object-src 'none'; connect-src 'none'` (`base-uri` and `form-action` do not
  inherit from `default-src`). Governs the page; cannot govern extensions or user actions;
  the policy file marks each API as probed, CSP-governed, or procedural (Location
  navigation methods are non-configurable on the platform and therefore procedural,
  never probed).
- The executable policy floor fixes the exact enumerated API-name → enforcement-class
  mapping independently of the registry: deleting an API, adding an unimplemented claim,
  or reclassifying a required probe is validation-fatal. Instrument labels and procedural
  explanations remain registry-authored, nonempty data.
- **Output encoding (normative):** all source-derived text escaped for its context; no
  untrusted `innerHTML`; embedded JSON script-safe-escaped (including `</script`
  sequences). **Adversarial escaping fixtures** are part of the acceptance suite.
- **Scripted testability:** the artifact script keeps its pure selection model in a
  delimited, extractable section; AC-10's scripted checks execute that model from the
  candidate bytes, never from source.
- **Progressive readability:** the automated script-stripped parser proves that, with
  JavaScript absent, the claims, disclosure, standing disclaimer, profile label, provenance
  panel, and flat mapping schedule remain present in readable document order. AC-14 has no
  deferred manual observation under either profile.
- **Confidentiality and delivery:** each artifact carries the §9.1 disclaimer and approved
  legend on screen and in print. Delivery is the bundle over a secure share, checksums via a
  separate channel. No artifact is ever published to any hosting or artifact service.
- **No build-time dependencies for the recipient**; counsel unzips and double-clicks.
- No cookies, no storage, no telemetry — per the enumerated, instrumented API policy above.

## 12. Visual design, accessibility, print

- Professional light theme; serif body for claim/disclosure text, sans for chrome. Pane
  split ≈ 45 % / 55 %. Edition title and strategy prefix always visible.
- **Scroll ownership (one owner per mode):** side-by-side — each pane owns its scroll;
  stacked — one dedicated combined container; the page body never scrolls in any mode.
- **Viewport:** minimum 1280 × 720 (About panel states it); below minimum, panes stack with
  navigation preserved. The breakpoint and stacking implementation are always
  acceptance-tested automatically; actual browser/OS layout observations are deferred under
  technical-preview and required under validated-release.
- Highlight palette: strong vs soft clearly distinct; every state has a non-color
  indicator; claim-level gate chips visually distinct from fragment/target chips.
- **Semantic controls:** discrete `<button>` elements; no nested interactive controls
  (§5.2); logical tab order; visible focus; minimum 24 px hit targets.
- **Focus determinism:** activation moves focus to the navigation bar; Esc clears and
  returns focus; pointer activation suppressed during text selection.
- **Keyboard:** Tab/Shift-Tab traverse when they are the configured browser/OS
  full-keyboard-navigation chord. On macOS, Keyboard Navigation must be enabled; Safari's
  “Press Tab to highlight each item” setting determines whether controls use
  Tab/Shift-Tab or Option-Tab/Option-Shift-Tab. Validated-release QA records both the
  configuration and chord actually exercised; technical-preview defers those observations.
  Enter/Space activate; ←/→
  cycle **only while the navigation bar has focus**; Esc clears. No global arrow-key capture.
- **Accessibility semantics and announcements:** controls expose browser-native names,
  roles, states, and polite `aria-live` updates (mode, position, target label, caution/gate
  presence). Under validated-release, for a support-matrix row whose `at` value is `none`, QA uses the browser's
  native DOM/ARIA semantics together with trusted keyboard, focus, and live-region
  checks; it does not require an external assistive technology. A row that explicitly names
  an assistive technology requires that named technology. **VoiceOver-specific operation and
  VoiceOver-driven release evidence are outside this delivery contract; Safari remains a
  required validated-release browser target with `at: "none"`. VoiceOver is not a deferred
  technical-preview observation and cannot be introduced by either profile.** The supported
  browser/OS/optional-AT set is **normative validated-release target-policy data**
  (`schema/support-matrix.json`); its approval does not assert that a technical-preview
  exercised it, and only a validated-release QA record references it as observed evidence.
  Version 2 has seven atomic rows, each naming exactly one OS;
  `at` is the fail-closed enum `none | NVDA 2024+`, so aliases cannot silently bring
  VoiceOver back into scope. Its version, target rows, exact row fields, non-empty target
  set, exact `[1280, 720]` minimum viewport, and required `stackedBelowMinimum: true` behavior
  are closed by `schema/support-matrix.schema.json`; approval cannot bless an untyped matrix.
- **Reduced motion:** `prefers-reduced-motion` disables smooth scrolling.
- **About & schedule surface:** the provenance panel and the flat mapping schedule
  render in a dedicated toggled view with its own scroll container (the page body still
  never scrolls); both are always present in print and in no-JS output.
- **Print stylesheet:** automated checks always require the claims, disclosure, disclaimer,
  profile label, provenance, and schedule print rules and the per-page disclaimer/legend
  mechanism. Actual print readability, page count, per-page presence, and clipping
  observations are deferred under technical-preview and required under validated-release.

## 13. Versioning, provenance and regeneration

Every artifact is a **pure build product**. Boundaries are **axes on one schema**: every
relation-schema field carries a tag per axis — `ship: artifact | schedule-only | never` and
`review: include | exclude` — an untagged field on any axis is a schema error, and
**inter-axis invariants are declared and validated**: every `ship: artifact` or
`schedule-only` field is `review: include`, **except schema-declared locator fields**
(`ship: artifact` + `review: exclude`), each of which must name the review-included digest
covering its identity (block ids ↔ target or source `textHash`) — an exception without its covering
proof is schema-invalid. The exception applies to **block locators only**, and the covering
digest suffices only where it is unique within the block's eligible set; where pinned text
legitimately repeats (the identical Example 2 EDL rows), every affected target,
caution-source, and gate-inventory source reference's review projection additionally
includes **contextual identity** — the parent container's canonical hash plus the occurrence
index — so the covering proof remains unique and re-anchoring stays review-neutral only
when identity is genuinely unambiguous. The contextual-parent graph is
acyclic; a block with no parent uses its canonical referenced-corpus root hash, never an empty
or positional surrogate. Binding endpoint hashes, declared context references, owner identity
tuples, and the dependency-chain hash are `review: include` though `ship: never`; lifecycle
metadata, immutable `proposedFrom` provenance, and `review.by`, `review.date`,
`review.operatorKind`, and `review.contentHash` itself are `review: exclude`. The schema
marks independent child owners (currently `phrases`) with an explicit review-owner boundary,
so a parent projection cannot traverse into them. Projections are generated from the axes,
never hand-maintained.

- **Shipping projection (ship axis):** `artifact` — status; targets (block, role, note);
  target-, fragment-, and phrase-scope cautions (gateId, type, code — quotations derived at
  render from pinned sources); phrases (id, text, occurrence, status, targets with their
  cautions); claim gates (gateId, type, code); gate dispositions (gateId, disposition).
  `schedule-only` — rationale. `never` — `proposedFrom`, `previousTargets`, `reviewState`,
  `review`, `migrationState`, endpoint hashes, identity/binding fields.
- **Review projection (review axis):** everything shipped except declared locators, plus
  all endpoint hashes, parent-context references, owner identity tuples, and the
  dependency-chain hash — stopping at schema-declared nested-owner boundaries — the
  `review.contentHash` domain (§8.4), domain-tagged and canonically serialized (§8.2).
  Reviewer identity, date, and operator kind are metadata outside that digest; changing
  them cannot disguise a content change because the content digest is independently
  recomputed.
- **Embedded provenance projection** (About panel + machine-readable): `rendered` and
  `quotable` corpora with versions and per-file SHA-256, public authority metadata for
  the configured and byte-verified `authorityCorpus` (`pct-pdf`), relation-set,
  gate-inventory, dependency-map, edition, schema, canonVersion,
  and strings-projection digests, the builder source-tree hash, the declared release
  timestamp, and counts. **Internal QA-source identifiers, paths, and hashes never appear
  in an artifact.**
- **Validated-release private QA record only** (`qa-record` kind; append-only): no QA record
  exists in a technical-preview chain. A validated-release record explicitly carries
  `releaseProfile: "validated-release"`, the complete `contentLock` over
  exact content-plane reads; a distinct, candidate-bound `qaInputLock` over the raw selected
  QA-registry path/digest and verified internal QA-source bytes plus candidate and
  content-lock digests; a sibling
  **`reproductionDiagnostics`** section
  (interpreter version, locale, platform settings — non-normative, **excluded from both lock
  digests and the candidate↔release equality check**); the release-verification envelope
  (candidate digest, content-lock digest, and exactly one **current exact-side** attestation
  of every required type by digest reference — superseded attestations are never
  referenced); the approved legend binding; the byte digest of the validated-release support
  matrix together with its named approver and exact approval-attestation digest; the four
  structured passed operator-performed checks bound to those candidate bytes; and the
  identified authorized human/model operator with explicit kind and identity.
- **Version-2 acceptance receipt** (required inside each `release-record` / `bundle-record`): the
  exact acceptance-registry byte digest, closed sorted executable-runner input lock and
  composite runner digest, tool runner kind, exact copied `releaseProfileContract`, exact
  passed phase/criterion set, and typed release or bundle subjects (§10). It is separate from
  content and optional validated-QA locks: it proves which executable acceptance contract and
  profile ran against which subjects, while the outer record remains
  the identified human/model operator's authorization; the tool runner is never authority.
- **Deterministic build:** declared release timestamp; stable ordering; double-build
  byte-identity **across separate interpreter processes** (an in-process double build
  shares interpreter state — notably hash seeds — and cannot detect seed-dependent
  ordering); candidate/release lock reproduction and byte comparison; deterministic
  STORE bundle with golden fixture.
- **Normative update procedure (per edition):** every registered content input is a regular
  file inside the same repository checkout as `navigator/build.py`. When an integration
  branch is behind the selected content baseline, first merge the exact source commit so the
  merge parents record both checkpoints. Live cross-worktree reads, symlinks, external
  content roots, selective unrecorded copying, and mutable filesystem aliases are forbidden.
  The runbook supplies the operational preflight and recovery commands but changes none of
  these requirements. Then (1) amend source(s), gate inventory,
  dependency map, relations, or builder code — the builder tree is a pinned content input,
  so tooling changes re-enter this procedure like any other amendment; (2) when gate-
  inventory endpoint pins need mechanical refresh, run the separate operation
  `python3 navigator/tools/stamp.py navigator/editions/<edition>.json --stamp-inventory`;
  it writes only the gate inventory and never relation review state; (3) `build.py candidate
  <edition>` — read-only; it fails listing every hash-stale entry, referential-integrity or
  disposition gap, exact-set mismatch, and schema violation; (4) `build.py migrate
  <edition>` — applies the §10 case table; (5) an identified human/model operator resolves
  each `stale`/`pending`
  owner, preserving any `proposedFrom` record (which remains intentionally non-releasable
  while pair-scoped verification is deferred); (6) after inspecting the resulting owner
  projection, that operator records approval with
  `python3 navigator/tools/stamp.py navigator/editions/<edition>.json --mark-reviewed
  --owner=<unit|phrase|claim-gate|disposition>:<key> [--owner=...] --reviewer="<identified
  operator>" --review-date=YYYY-MM-DD --operator-kind=<human|model>`, or substitutes
  `--all-owners` for the owner arguments only after reviewing every owner. Relation stamping
  has **no pin-only mode**: it updates endpoint pins and the review hash only inside this
  explicitly owner-scoped authorized-operator action; (7) `build.py candidate <edition>`;
  (8) refresh
  every required exact-side attestation via `attest` as needed (new immutable records);
  (9) if and only if releasing under `validated-release`, use `record-qa --template` if
  desired, perform and complete the four version-3 structured operator checks against those
  exact candidate bytes, including every atomic matrix target and the actual
  versions/configuration, optionally validate the completed inline or workspace-relative
  evidence with `record-qa --check-only`, then run `record-qa` without `--check-only`
  (immutable, candidate-bound validated-release authorization record); technical-preview
  skips this step and neither requires nor creates a QA record; (10) run `build.py release
  <edition> --profile=<technical-preview|validated-release>` with an explicit profile equal to
  the registry's active profile — reproduces the content lock (and the validated-QA lock only
  for validated-release), byte-compares the candidate, verifies the envelope,
  executes the registry-bound `release-preflight`, writes and reads back the sealed artifact
  and checksum, passes the AC-16 `release-postcondition`, then appends the identified
  authorized human/model `release-record` with its non-authoritative tool-run receipt last;
  (11) after both releases, run
  `python3 navigator/build.py bundle-plan`. Inspect its canonical proposed JSON and apply it
  to the bundle config only as an ordinary reviewed source edit; the command itself is
  read-only, applies deterministic human-over-model then digest precedence among valid
  current authorizations, rejects incomplete or malformed chains, and never writes config or
  evidence; (12) run
  `build.py bundle` when the applied version-3 config's exact profile, complete
  profile-specific authorization chains, and current release receipts validate; it
  writes/reads back the version-2 structured profile-labelled manifest, ZIP, and checksum, passes
  the AC-20 `bundle-postcondition` through its registry-named fresh-interpreter callback,
  then appends the identified authorized human/model `bundle-record` with its
  non-authoritative tool-run receipt last; (13) remove superseded files from the live
  distribution directory, run `python3 navigator/build.py verify-current`, and commit sources
  + relations and bundle config, then current artifacts with checksums and records.
  (Write-statements in this procedure are validated against `planes.json`, §10.)
- Each file name and header embeds its claim-set version. The live distribution directory
  contains only current-version products; superseded products remain identifiable in Git and
  cannot be selected by current bundle configuration or exact-side evidence resolution.

## 14. Acceptance criteria (definition of done)

Acceptance version 2 carries stable criterion IDs and the exact active/two-profile policy in
the criteria registry (`schema/acceptance.json`); this section
must match the registry (comparison test, §10.17); the traceability matrix and meta-test
close both directions over the registry, **including AC-19 and AC-20 themselves**.
The registry's closed `receiptPhases` map is also normative: `release-preflight` covers
AC-01–AC-19, `release-postcondition` covers AC-16 after output write/readback, and
`bundle-postcondition` covers AC-20 after bundle output write/readback.
**Applicability: a standalone edition release requires AC-01 – AC-19 under its explicit
profile; bundle creation additionally requires AC-20 under that same profile. Automated
checks always remain required. Only the technical-preview observations enumerated exactly as
AC-11/12/13/15 are deferred; AC-14 has no deferred manual observation. A claim of passage is
valid only in the current, profile-and-subject-bound version-2 acceptance receipt carried by
an identified authorized human/model outer record; its tool runner is evidence, never
authority.**

**Per edition (AC-01 … AC-18)** — all pass (automated except where noted):

1. **AC-01** Source extraction reproduces the edition's locked normative §3 parameter table
   and census exactly (corpus IDs/versions, group names/counts, display prefix, relation,
   gate, dependency, and config paths, QA bindings, forbidden terms, and artifact default),
   including the authored dependency map cross-validated against parsed claim references;
   PCT claims 1–18, Examples 1–5, Tables 1–3 with row anchors, four figures present and
   hash-verified.
2. **AC-02** Every owner carries its applicable lifecycle fields with a valid
   `review.contentHash` over the review projection (incl. identity tuples and
   dependency-chain hash), plus an identified authorized reviewer with explicit
   `operatorKind: human | model` and a real canonical `YYYY-MM-DD` review date; tool is
   never release-authoritative; zero `pending`, zero `stale`.
3. **AC-03** Gate referential integrity passes in both directions with declared uniqueness
   keys; every mandatory gate has a reviewed disposition, and every affirmative disposition,
   including one for an optional gate, has its actual matching carried evidence; the
   no-candidate disposition fixture releases without a fabricated mapping; the
   inventory-completeness attestation by an identified authorized human/model operator is
   current, and tool evidence is rejected.
4. **AC-04** Zero unresolved source drift: all corpus, fragment, aggregate-claim,
   dependency-chain, target, and caution-source digests current (full digests, matching
   canonVersion).
5. **AC-05** All schema and invariant validations pass: axis tags present with inter-axis invariants and declared locator exceptions satisfied; applicability matrices; relation-binding conformity; phrase rules; no duplicate targets, gate instances, or dispositions; note and rationale bounds; caution type×scope matrix and code closure; caution sources resolve into `quotable` blocks only; zero targets on editorial, excluded, or `internal` blocks; the support matrix has its closed structural shape; enum ↔ presentation coverage; forbidden-terms check clean; the centralized authority matrix admits only explicit human/model kinds paired with an NFC identity having no surrounding whitespace or control/format characters and at least one visible character, and rejects tool, missing, blank, invisible-only, unknown, and malformed kinds or identities.
6. **AC-06** The edition's fixtures (including the disposition fixture) validate against
   schemas and pinned corpora; this document's examples match the fixture projections.
7. **AC-07** Registry-access, artifact-kind/path, edition-blindness, writer-set, diff-classifier,
   single-digest-path, single-JSON-input-parser, procedure-vs-matrix, and hard current-state
   boundary tests pass; the hard boundary rejects obsolete primary-strategy versions, extra
   or missing inventory files, legacy-format verification records, stale pin plans, and
   write privilege; the NA-scoped migration
   case-table scenario test passes against a locked synthetic NA snapshot rather than live NA inputs,
   asserts the runtime classifier accepts every intended delta and rejects semantic/review
   mutations before any source write,
   while other edition releases neither execute nor bind it; the registered canonical
   serialization golden-vector and generated-input property tests pass (idempotence, NFC
   duplicate-key rejection, escaping exactness, and integer edge rules).
8. **AC-08** Projection tests pass: no `never`-tagged field and no internal QA-source
   identifier appears in any artifact kind, previews included.
9. **AC-09** Adversarial escaping fixtures render safely through every authored and quoted
   channel.
10. **AC-10** Forward and reverse navigation behave per §§5–6, including claim-level gate
    display (scripted checks on the built candidate).
11. **AC-11** Automated candidate-byte checks always verify the §12 semantic-control structure, focus and keyboard implementation, polite live-region implementation, reduced-motion rule, and closed support-matrix shape. Under technical-preview, the actual cross-platform browser/OS/assistive-technology observations are explicitly deferred and no browser or assistive-technology compatibility is authorized. Under validated-release, versioned QA evidence must copy every atomic support-matrix row in exact order, record actual browser/OS/AT versions and the configured traversal chord, and carry typed passed traversal, activation-key, focus, scoped-arrow, computed-name/role/state, and live-region results by one identified authorized human/model operator; tool is never authority. Rows with `at: "none"`, including Safari, require browser-native evidence but no external assistive technology; a named-AT row requires that exact named technology and version. VoiceOver remains outside both profiles.
12. **AC-12** Automated candidate-byte checks always verify the §12 print stylesheet, page margins, repeated-footer mechanism, print visibility rules, and overflow/clipping safeguards. Under technical-preview, actual print-engine/browser/OS observations are explicitly deferred and no print compatibility is authorized. Under validated-release, versioned structured QA evidence must record the actual browser/OS versions, a positive page count, and typed passed results for readable claims/disclosure, the disclaimer on every printed page, the legend on every printed page, provenance, schedule, and absence of content clipping, by the same identified authorized human/model operator; tool is never authority.
13. **AC-13** Automated candidate-byte checks always verify the local-file architecture, exact support-matrix viewport policy, derived responsive breakpoint, below-minimum stacking rule, and viewport notice. Under technical-preview, actual local-file launches and layout observations across the support matrix are explicitly deferred and no browser/OS layout compatibility is authorized. Under validated-release, versioned structured QA evidence must copy every atomic support-matrix row in exact order, record actual browser/OS/AT versions, the exact minimum and a below-minimum viewport, and typed passed local-file, minimum-layout, and stacked-layout results, by the same identified authorized human/model operator; tool is never authority.
14. **AC-14** Automated script-stripped candidate parsing always proves that the §11 claims, disclosure, schedule, provenance, disclaimer, legend, and noscript content remain present in readable document order. AC-14 has no deferred manual observation and no QA-record field under either release profile.
15. **AC-15** Automated candidate-byte checks always verify that self-auditing attempted-use instrumentation per `schema/api-policy.json` exposes the exact registered probe set, wires every required hook, records attempted use, and fails closed unless every hook reports installed with null error/detail; page code contains no registered forbidden use. Under technical-preview, actual browser/OS runtime and ledger observations are explicitly deferred and no runtime compatibility is authorized. Under validated-release, versioned structured candidate-bound QA evidence must record the actual browser/OS versions, ready=true, the exact installed hook map, and exact empty attempted-use, resource, external-request, cookie-write, Web Storage, IndexedDB, and navigation-mutation ledgers; it is authorized by an identified human/model operator, never tool.
16. **AC-16** Double build is byte-identical across separate interpreter processes; the content-input lock reproduces byte-identically between candidate and release (diagnostics excluded); the exact-set check passes in both directions; release byte-compares and seals the same current candidate bytes; lock, envelope, release-profile label, and release-record are written append-only; checksums are emitted and match. These determinism and output-integrity checks do not depend on manual cross-platform QA. Technical-preview has no QA-record prerequisite; validated-release additionally reproduces the candidate-bound `qaInputLock` over pin-verified internal QA inputs and binds the current validated QA record. The release record is appended last only after sealed/checksum readback, is authorized by an identified human/model operator, carries the exact releaseProfile, compatibilityAuthorization, deferredObservations, and artifactLabel contract, and carries a current registry/runner/profile/subject-bound acceptance receipt whose exact release-preflight result covers AC-01–AC-19 and whose post-write release-postcondition covers AC-16; the tool runner supplies evidence but is never authority.
17. **AC-17** The exact selected-profile artifact label, §9.1 disclaimer, and approved legend are present on screen, in print, and no-JS; the legend approval by an identified authorized human/model operator matches the shipped wording digest, and tool evidence is rejected. The technical-preview label explicitly states that manual cross-platform and assistive-technology QA is deferred and compatibility is not validated.
18. **AC-18** Double-sided content-QA attestations by identified authorized human/model operators are current and carry producerCommand: navigator/build.py attest/v1, the exact typed attest-command output contract: priority-map cross-check and, for AF, the crosswalk non-conflation check; missing or unknown producer metadata and tool evidence are rejected. These attestations remain required for both release profiles and do not represent deferred browser/OS/assistive-technology observations. The producer marker is digest-bound audit metadata under the repository/Git trust root, not a cryptographic signature.

**Shared** — **AC-19** Before importing any registry-selected callback, the production runner rejects drift from an independent locked executable floor: the supported-edition set, module path specifications, fixture path→scope map, callback test scopes, support-file inventory, manual-QA-evidence version, exact active/two-profile policy, and exact per-criterion callback/validated-release-QA-field map are deletion- and redirection-resistant, with unique callback ownership. The traceability meta-test then proves every registered criterion (AC-01 through AC-20, including this one) maps to its named live tests with criterion-matching `test_acNN_` identity or validated-release QA-record fields, the technical-preview deferred-observation set is exactly AC-11/12/13/15 while AC-14 is never deferred, only AC-07 owns canonicalization callbacks, every acceptance-designated test maps back to a registered criterion, and every floored support input and every shared or active-edition fixture exists and is locked without opening inactive-edition fixture bytes.

**Bundle** — **AC-20** Automated bundle integrity checks always require the bundle to match its config exactly (enumerated members only, including the bundle-manifest), verify every member digest, produce a deterministic STORE ZIP conforming to the golden bundle fixture with its own detached checksum, and match the neutral manifest's approved wording digest. Every configured release-record must resolve by explicit digest to a current release→exact-attestation chain with exact typed producer metadata and authorization by identified human/model operators, independently current candidate/content-lock bindings, and the same explicit release profile in the config, records, artifact labels, and receipts. Under technical-preview, no QA record or manualChecks is required or created; the manifest carries the profile, compatibility status, deferred-observation set, and exact technical-preview label, and neither the bundle nor its records claim browser or assistive-technology compatibility. Under validated-release, every release additionally resolves a current QA record with exact qaInputLock, support-matrix approver/targets/viewport, API probe set, and locked manual-evidence version, and bundle verification independently revalidates the complete typed AC-11/12/13/15 version-3 evidence rather than trusting QA-copied context. The manifest approval is current identified authorized human/model evidence. Every resolved release receipt is current, and the bundle record is appended last only after manifest/ZIP/checksum readback by an identified human/model operator with a current registry/runner/profile/subject-bound bundle-postcondition receipt covering AC-20; tool records and the tool runner are never authority.

## 15. Roadmap (not in the current deliverable)

- Activate `validated-release` only after current full version-3 AC-11/12/13/15 evidence has
  been performed across the preserved seven-row target policy; switch the explicit active
  profile and executable-floor commitment deliberately, then regenerate all affected records
  and artifacts. VoiceOver remains out of scope.
- `propose-reuse` cross-edition proposal tooling (optional hardening; boundary specified in
  §10.7).
- Provisional-support layer as additional relation sets per edition, after the PCT
  navigators are validated and counsel-approved.
- Prior-art (D1/A4/B9) and office-action layers; post-continuation claim-set editions. New
  view types may require new registered presentation components (§10).
- As-filed PDF page pinpoints (block→page enrichment).
- Pane-aware search; status and caution filters; copyable internal deep links; selection
  history; adjustable pane split.
- Digital signing of released artifacts, signed release manifests, signed build-input
  locks, and hash-chained verification ledgers.
- Counsel annotation/comment capture (its own decision; changes the confidentiality model).

## 16. Standing decisions

| Decision | Choice |
|---|---|
| Editions | Two current editions (NA, AF) of one shared contract; alternatives, never layers; one single-edition artifact each |
| Edition knowledge | Kernel edition-blind (AST-test-enforced); edition configs are the complete parameter set incl. declared transitive inputs; censuses, gate inventories, and dependency maps are normative data |
| Requirements as data | Coverage proven by bidirectional referential integrity over instances and dispositions; **policies are total over evidence states — honest absence is a releasable, reviewed disposition**; inventory completeness is a digest-bound identified-authorized-operator attestation; acceptance criteria, exact active/two-profile release policy, API policy, and validated-release support matrix live in registries |
| Associations | Every association pins both endpoints by digest and carries lifecycle where reviewed; `gateId` required on every source-gate instance; declared uniqueness keys on every collection |
| Lifecycle | Ownership model with schema-declared applicability matrices and per-owner identity tuples; sub-object changes roll up; closed staleness-reason enum |
| Reviews & attestations | Exact-declared-side digest binding; required owner review provenance `{by, operatorKind, date, contentHash}` with closed `human | model | tool` kinds and release authority only for an NFC identified human/model operator with no surrounding whitespace or control/format characters, at least one visible character, and a real canonical date; reviewer identity/date/kind excluded from `review.contentHash`, which covers the schema-derived review projection — content, hidden endpoints, identity tuples, and dependency-chain hash, stopping at declared nested-owner boundaries; **declared locators excluded, so mechanical re-anchoring never invalidates review**; parent-claim amendments deliberately cascade re-review to dependents; model/tool authorship stays truthful; tool never authorizes; typed passed identified-authorized-operator append-only authorization records; exact typed attest-producer marker is digest-bound Git-root metadata, not a signature |
| Trust root & planes | `contentLock` derived from the exact gateway read log under both profiles; validated-release additionally carries a candidate-bound `qaInputLock` over pin-verified internal QA bytes, **diagnostics excluded from applicable lock digests**; current registry-byte + exact profile + runner-input acceptance lock; forward-chaining verification records incl. `release-record`; exact command×kind privilege matrix; procedure prose validated against the matrix; reviewed git commit is the trust root |
| Enumerations & boundaries | All projections derived from schema axis tags with declared, justified locator and nested-owner-boundary rules; gateway-enforced output-kind registry with plane membership; derived content never stored |
| Serialization | Completed canonical law (vendored interpreter-independent Unicode 15.1 NFC/White_Space data, raw and post-NFC duplicate-key rejection, exact escapes, integer edge rules, two declared payload forms — digest-list vs canonical-JSON) + NUL-framed domain tags incl. `figure` and per-record-kind tags, versioned under canonVersion; single-digest-path test; golden vectors + property-based tests confirm |
| Structural graphs | Dual-sourced: authored dependency maps cross-validated against parsed claim references (AF three-way against its document table); totality/acyclicity/root checks; mismatch fails the build |
| Cross-edition isolation | Unique corpus ids; scoped triples; binding rules; per-edition allowlists; edition failures never cross (shared-input failures affect both; bundle needs both) |
| Cross-edition reuse | Deferred optional hardening; pair-granted, proposal-only; crosswalk is context and warning, not evidence; any `proposedFrom` is release-blocking until the pair-scoped verifier exists |
| Click granularity | Two-tier: limitation units + inner key phrases with stable phrase IDs |
| Evidence model | `status` (units/phrases) ⊥ authoring-only, never-shipped `reviewState` ⊥ `migrationState` per applicability matrix; no forced positive mappings — including via gate cardinality; release predicate defined once |
| Cautions | Closed types × scopes × codes with schema-enforced matrix; claim-level gates never inherited to units; "claim-as-a-whole" is one code, not the class name |
| Identity | Positional IDs as declared locators; semantic identity pinned by full SHA-256 canonical hashes (incl. aggregate claim and dependency-chain hashes); corpus/edition ids stable and version-neutral — claim-set versions update pins in place via migrate |
| Tool behavior | Closed action taxonomy; commands declare classes; diff-classifier enforces; reviewed semantic content is never tool-modified |
| Migration | Closed case table with roll-up staleness and complete reason enum; auto-re-anchoring only on unique canonical-hash match |
| Release lifecycle | Explicit `release --profile=<technical-preview\|validated-release>` promotion by passed identified-human/model operator, candidate-bound verification per edition; technical-preview has no QA predecessor and explicitly defers AC-11/12/13/15 observations without compatibility authorization; validated-release retains the full seven-row version-3 QA gate; required version-2 nested tool receipt binds exact registry, selected profile contract, runner inputs, phase results, and subjects but is never authority; release-preflight = AC-01–AC-19, post-write release-postcondition = AC-16, post-write bundle-postcondition = AC-20; outer authorized-operator record appended last after output readback; read-only `bundle-plan` derives current profile bindings/chains and proposes fail-closed config refresh for authorized-operator application; bundle resolves exact configured release digests and their full current profile-specific receipt/attestation chains (plus QA only for validated-release), including exact typed attestation-producer metadata, before deterministic STORE packaging; authoring previews pass the same projection but never authorize delivery |
| Traceability | Guarantee table (claims→enforcers, and collision detection between mechanisms) + fixture/registry/procedure comparisons + bidirectional traceability meta-test: checked loops that include themselves |
| Environment | Negative guarantees are always instrumented and tested per the enumerated API policy; actual-browser runtime observations are deferred under technical-preview and required under validated-release; runtime determinants are non-normative diagnostics outside applicable lock digests; the seven-row support matrix is validated-release normative target-policy data with a pinned digest, named approver, and exact policy-approval attestation; VoiceOver is outside both profiles |
| Multi-candidate behavior | Jump to first + cycle; all candidates kept; display cap presentation-only |
| Right-column scope | As-filed disclosure package; editorial content labeled and non-targetable; PCT claims targetable per the disclosure profile |
| QA boundary | Corpus visibility validator-enforced; QA sources `internal`, never quoted, never identified in artifacts; the configured authoritative PDF is read and pin-verified but only its public authority metadata may appear; no technical-preview QA record exists, while validated-release alone records the full structured manual evidence |
| Directionality | Left→right primary; reverse via edition-scoped badges only; disclosure text never clickable |
| Terminology | Neutral throughout; selected edition strings resources; forbidden-terms and neutrality checks over the full authored-visible surface, excluding pinned verbatim source text; approvals digest-bound |
| Guarantees | Every hard claim names its enforcer; procedural-only claims say so; universal claims cite the table or carry a scope; new mechanisms pass collision review |
| Infrastructure | Local or firm-approved private only; CI-environment guard with logged override |
| Hosting | None — standalone local files, deterministic bundled delivery, checksums via separate channel |

## 17. Open points

Stated values below are **normative defaults**: acceptance tests are written against them,
and approval either confirms or changes them.

1. Deliverable file names/locations (§3 defaults) and whether this description accompanies
   the transmission to counsel or remains internal.
2. Margin anchor labels: visible (current default) or suppressed with anchors kept internal.
3. Delivery channel (default: deterministic bundle over secure share, checksums via
   separate channel, §11).
4. Counsel approval of the confidentiality/work-product legend wording and of the bundle
   manifest's neutral description (release-blocking, digest-bound attestations, §9.1/§10).
