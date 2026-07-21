# AA11393US — Interactive Claims-to-Specification Navigator: Technical Description (DRAFT)

> **DELIVERABLE SPECIFICATION · STATUS 21 JULY 2026**
>
> Single live specification for the interactive HTML5 navigators linking the AA11393US
> candidate claim sets to the PCT application as filed (PCT/IB2025/051755, published as
> WO 2025/181623 A1). One shared technical contract, **two current editions** built from it:
> the **NA edition** (normal-allowance claim set, NA-2026-07-17-v1) and the **AF edition**
> (allowance-first claim set, AF-2026-07-17-v2). The editions are alternative counsel-review
> strategies, never cumulative layers. This document always describes the current intended
> state; superseded content is removed, not annotated. Implementation follows only from this
> document.
>
> **Interpretation clause:** this document is a specification. Normative language —
> including present-tense descriptions of tests, fixtures, gates, and tools — describes
> required behavior of an implementation that does not yet exist; nothing described here is
> an implemented fact until built and verified under §14.

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

- **Primary user:** US prosecution counsel reviewing claim-set versions NA-2026-07-17-v1
  and/or AF-2026-07-17-v2.
- **Secondary user:** the internal reviewer (Antonio) validating claim-support work product.

### 1.1 Legal and functional boundary

The tool **does**:

- present the pinned candidate claims of each edition and the pinned as-filed PCT
  disclosure;
- display author-recorded **candidate** relationships between claim fragments and disclosure
  passages, with their recording status and internal review state;
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
content from a priority-support map (§2). **AF claim 20 rule:** the AF edition always shows
all 20 AF claims; omission of AF claim 20 is a counsel filing choice recorded nowhere in the
navigator, per the claim-set's own instruction that no separate claim-set document be
created for it.

## 2. Sources and authority

Every input is a registered corpus (§8.1) with a globally unique id. Visibility is declared
per corpus and refined by its segmentation profile.

| Corpus id | Path | Role | Visibility | Used for |
|---|---|---|---|---|
| `pct-pdf` | `PCT/AA11393US-PCT_RAPPORTO DEPOSITO.pdf` (60 pp.) | `authoritative` | `internal` (identity/hash may appear as authority metadata in embedded provenance, §13) | As-filed authority of record; never rendered |
| `pct-disclosure` | `PCT/AA11393US-PCT_RAPPORTO_DEPOSITO_markdown/` (markdown + `figures/Fig-1..4.png`, each file pinned) | `derivative` | `rendered` | The as-filed disclosure package: title, description, Examples 1–5, PCT claims 1–18, abstract, four drawing sheets |
| `na-claims-v1` | `US/normal-allowance/AA11393US-NA-US_claim-set_DRAFT.md` | `fragment-source` | §3 claims `rendered`; profile-designated guidance blocks `quotable`; rest excluded | NA claims 1–30 verbatim; guidance blocks as caution/gate sources |
| `af-claims-v2` | `US/allowance-first/AA11393US-AF-US_claim-set_DRAFT.md` | `fragment-source` | §3 claims `rendered`; profile-designated guidance blocks `quotable` (including the §3 Example 2 priority-gate blockquote, excluded from the unit census); rest excluded | AF claims 1–20 verbatim; guidance blocks as caution/gate sources |
| `na-priority-map` | `US/normal-allowance/AA11393US-NA-priority-support-map_DRAFT.md` | `qa-source` | `internal` | QA cross-check of the NA mapping (§9); never rendered, never quoted, never identified in an artifact |
| `af-priority-map` | `US/allowance-first/AA11393US-AF-priority-support-map_DRAFT.md` | `qa-source` | `internal` | QA cross-check of the AF mapping (§9); never rendered, never quoted, never identified in an artifact |
| `af-na-crosswalk` | `US/allowance-first/AA11393US-AF-claim-crosswalk_DRAFT.md` | `qa-source` | `internal` | Non-conflation QA; **review context and a non-transfer warning for cross-edition reuse proposals (§10) — never evidence that reuse is substantively correct**; never rendered, never quoted, never identified in an artifact |

The AF prior-art matrix, counsel briefings, mapping matrices, and continuation memo are
**not** navigator inputs: they concern patentability and strategy, not claims-to-PCT
navigation.

Visibility semantics (validator-enforced, §10): `rendered` — appears in a pane; `quotable` —
never a pane, but blocks may be quoted in the UI (caution/gate sources); `internal` — no
UI-visible reference of any kind may point into it, and internal corpus identifiers never
appear in a delivered artifact (§13 provenance projection). A caution or target referencing
an `internal` corpus is schema-invalid. **Quotable status is designated by each corpus's
segmentation profile, never by fixed section numbers.**

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
| Claim corpus | `na-claims-v1` (NA-2026-07-17-v1) | `af-claims-v2` (AF-2026-07-17-v2) |
| Claims | 30 | 20 |
| Limitation units (census, test-enforced) | 65 | 60 |
| Independent claims | 1, 9, 16, 22 | 1, 20 |
| §3 group headings | 4 actor groups | 7 structural groups |
| Largest decompositions | claims 9, 16, 22 = 9 units each | claims 1, 20 = 15 units each |
| Display prefix (mandatory) | `NA claim N` | `AF claim N` |
| Relation set | `relations/na-v1__pct.json` | `relations/af-v2__pct.json` |
| Gate inventory | `profiles/gates_na-claims-v1.json` | `profiles/gates_af-claims-v2.json` |
| Dependency map (authored + cross-validated, §8.1) | `profiles/deps_na-claims-v1.json` | `profiles/deps_af-claims-v2.json` |
| Edition config | `editions/na-v1.json` | `editions/af-v2.json` |
| QA cross-check source | `na-priority-map` | `af-priority-map` |
| Forbidden terms in authored user-visible text | — (NA claims legitimately use both pattern terms, with distinct claim functions) | `camera-cut timing pattern` (crosswalk non-conflation boundary) |
| Artifact (default name, §17) | `AA11393US-NA-claims-spec-navigator_NA-2026-07-17-v1.html` | `AA11393US-AF-claims-spec-navigator_AF-2026-07-17-v2.html` |

Edition rules:

- **Alternatives, not layers.** Each edition builds its own single-edition artifact. There
  is no NA/AF toggle, merged view, or hybrid artifact.
- **Isolation, precisely scoped:** an edition-specific failure (its relation set, gate
  inventory, census, QA, attestations) never blocks or contaminates the other edition.
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
each clause. The census is normative per edition (§3): NA 30 claims / 65 units (claim 9 =
9 units); AF 20 claims / 60 units (claims 1 and 20 = 15 units each). The extraction test
asserts the census exactly.

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
- **`reviewState`** — internal authoring progress: `pending` | `internally-reviewed`. Never
  rendered as, and never implying, counsel approval.

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
decreasing specificity. The data records **all** recorded candidates (no authoring cap); if
more than 5 exist, the inline soft-highlight set shows the first 5 with a "+N more" control
in the bar, and the printable schedule (§11) always lists all.

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
wherever a human reviewed it**; **mechanisms are closed over their own data**; **boundaries
are axes on one schema, planes never feed backward, derived content is never stored**; **a
review covers content in its context**; **policies are total functions over evidence
states**; **invariant exceptions are typed and justified, never silent**; and **structural
graphs are dual-sourced** (§8.1, §8.4, §13).

### 8.1 Corpus registry, gate inventories, dependency maps

Each corpus is registered in `navigator/corpora.json`: globally unique id (§2), role
(`authoritative` | `derivative` | `fragment-source` | `qa-source`), visibility (`rendered` |
`quotable` | `internal`), per-file SHA-256 (a multi-file corpus pins every file
individually), version label, and a **segmentation profile** (declarative file listing which
sections are targetable, editorial, quotable, or excluded — policy lives in reviewable data,
not parser code; quotability and targetability are profile-designated, never hardcoded).

Each fragment corpus has a **gate inventory** (`profiles/gates_<corpusId>.json`) — authored,
reviewed data enumerating every guidance gate of that claim-set document. Exact entry shape:

- `gateId` — unique within the corpus;
- `source` — `(block, full textHash)` into a profile-designated `quotable` block;
- `code` — closed caution code (§8.5);
- `requiredScope` — `target` | `fragment` | `claim`;
- `appliesTo` — hashed endpoints, per scope: claim scope → claim ids with **aggregate claim
  hashes**; fragment scope → fragment ids with fragment hashes; **target scope → applicable
  fragment ids with hashes plus a required cardinality (≥ 1 target of each listed fragment
  must carry this gate; which target is a human's reviewed choice)**;
- `requirement` — `mandatory` | `optional`. Optional means: may be carried; if carried, it
  must match the inventory. No conditional-activation logic exists.
- `profileDigest` — the segmentation-profile digest the inventory's block references were
  authored against. Inventory source locators are eligible for mechanical re-anchoring
  (§10) under a unique canonical-hash match.

**Gate dispositions — policies are total over evidence states.** Satisfaction of a
mandatory gate is recorded as a reviewed, lifecycle-bearing **disposition** pinned to gate
and subject, from a closed enum: `satisfied-by-target` (a carrying target exists);
`satisfied-by-fragment-fallback` (the applicable fragment is `counsel-review-required`, and
the same gate is carried at fragment scope instead); `inapplicable-no-candidate` (the
applicable fragment is `counsel-review-required` and no honest target exists — recorded,
reviewed, releasable). **A mandatory requirement is never satisfiable only by creating
evidence**: an honest no-candidate fragment releases without a fabricated mapping, and a
fixture proves it.

Each fragment corpus also has an authored **dependency map**
(`profiles/deps_<corpusId>.json`) — the claim dependency graph, authored from the claim-set
document's own dependency tables and **cross-validated against the parsed "of claim N"
references in the claim text; any mismatch fails the build**. M39 dependency-chain hashes
(§8.2) are computed only from a validated map — structural graphs are dual-sourced, never
parsed-only (inference) or authored-only (typo risk).

The inventory is a reviewed interpretation of the claim-set's prose gates, recorded once and
hash-pinned to its source blocks. The validator proves gate coverage by **referential
integrity in both directions** over instances *and dispositions*: every `source-gate`
instance carries a `gateId` resolving to a matching inventory entry, and every `mandatory`
inventory entry has a reviewed disposition at its required scope and cardinality. Inventory
completeness itself is a **digest-bound human attestation** (claim-set digest + inventory
digest, §9).

Outside a relation file, fragment identity is always the scoped triple
`(fragmentCorpusId, fragmentId, fragmentTextHash)` — both editions contain a `c1u0`.

### 8.2 Canonical text, object serialization, and hashing — versioned law

One shared canonicalization module is the only hashing path for all digests — text, object,
and composite alike; a test asserts no digest is computed outside it. The rule set carries a
**canonVersion**, recorded with every stored digest (`sha256/c1:…`). Changing any rule bumps
the version; a version mismatch is ordinary staleness resolved through migration (§10).
**The canonVersion pins its Unicode version** (NFC tables change across Unicode releases)
and its whitespace character set (the Unicode White_Space property of that pinned version).

Per-type text rules (canonVersion c1):

- **Prose (paragraphs, list items, headings, captions):** decode UTF-8 → Unicode NFC →
  collapse every whitespace run to a single space → trim.
- **Code blocks:** NFC → normalize line endings to LF → strip trailing whitespace per line →
  **preserve line breaks and leading indentation**.
- **Tables:** canonical cell text joined with U+001F, rows with U+001E, caption appended as
  a final row. Row hashes use the row's serialization.
- **Figures:** domain-tagged composition (`aa11393:figure:c1`) over
  `SHA-256(file bytes) ‖ SHA-256(canonical caption text)`.

**Canonical object serialization (composite digests) — defined by rule, confirmed by
vector:** canonical JSON meaning UTF-8 output; all strings NFC-normalized; **objects whose
keys collide after NFC are rejected**; object keys sorted by Unicode code point of the NFC
key string; escaping exactly: the two-character forms `\"` `\\` `\n` `\r` `\t` and `\u00XX`
for remaining control characters below U+0020 — nothing else escaped; numbers are integers
with |n| < 2⁵³; array order preserved exactly as authored. Inner digests compose as **raw
32-byte values**, never hex strings. Every composite digest is framed
`tag ‖ 0x00 ‖ canonical-payload` (tags are ASCII, never containing NUL):
`aa11393:claim-agg:c1`, `aa11393:dep-chain:c1`, `aa11393:review:c1`,
`aa11393:inventory:c1`, `aa11393:lock:c1`, `aa11393:figure:c1`. Composite digest types:

- **Aggregate claim hash** — domain-tagged digest over the claim's ordered unit hashes.
- **Dependency-chain hash** — domain-tagged digest over the ordered aggregate claim hashes
  of the owner claim's ancestor chain (independent claim first, owner's claim last), per
  the validated dependency map (§8.1).

Golden test vectors confirm the law; they do not define it. Validation uses the **full
SHA-256 digest**; abbreviated prefixes are display-only.

### 8.3 Relation entries

One relation set per (fragment corpus, target corpus) pair, its binding declared in the file
header; entries referencing any other corpus are schema-invalid. The examples below are
**abridged renderings of the required fixtures** (`navigator/tests/fixtures/`); the test
suite must validate each fixture against the shipped schemas and pinned corpora **and
compare this document's code blocks against the fixtures' projections**. Hashes are
abbreviated here; data files carry full digests with their canonVersion prefix.

NA fixture (excerpt of `relations/na-v1__pct.json`):

```json
{
  "binding": {"fragmentCorpus": "na-claims-v1", "targetCorpus": "pct-disclosure",
              "schemaVersion": "1", "canonVersion": "c1"},
  "claimGates": {},
  "fragments": {
    "c9u6": {
      "status": "mapped",
      "reviewState": "internally-reviewed",
      "migrationState": "current",
      "review": {"by": "amc", "date": "2026-07-21", "contentHash": "sha256/c1:5aa0…"},
      "fragmentTextHash": "sha256/c1:19d2…",
      "targets": [
        {"block": "S054", "textHash": "sha256/c1:9f3a…", "role": "specific",
         "note": "Manifest files 121 point to unique interleaved chunk combinations"},
        {"block": "PC11", "textHash": "sha256/c1:d051…", "role": "context",
         "note": "PCT claim 11: transcoding components / manifest generation",
         "caution": {"gateId": "na-gate-combined-example",
                     "type": "source-gate", "code": "combined-example",
                     "source": {"corpus": "na-claims-v1", "block": "S142",
                                "textHash": "sha256/c1:66c1…"}}}
      ],
      "phrases": [
        {"id": "c9u6p1", "text": "camera-cut timing pattern", "occurrence": 1,
         "status": "mapped", "reviewState": "internally-reviewed",
         "migrationState": "current",
         "review": {"by": "amc", "date": "2026-07-21", "contentHash": "sha256/c1:c711…"},
         "targets": [{"block": "S042", "textHash": "sha256/c1:77b2…", "role": "specific",
                      "note": "Timing-pattern definition",
                      "caution": {"type": "generalization-note",
                                  "code": "beyond-literal-example"}}]}
      ]
    },
    "c16u6": {
      "status": "counsel-review-required",
      "reviewState": "internally-reviewed",
      "migrationState": "current",
      "review": {"by": "amc", "date": "2026-07-21", "contentHash": "sha256/c1:90bf…"},
      "fragmentTextHash": "sha256/c1:3ab0…",
      "caution": {"gateId": "na-gate-detection-support",
                  "type": "source-gate", "code": "detection-support",
                  "source": {"corpus": "na-claims-v1", "block": "S171",
                             "textHash": "sha256/c1:0e44…"}}
    }
  }
}
```

AF fixture (excerpt of `relations/af-v2__pct.json`):

```json
{
  "binding": {"fragmentCorpus": "af-claims-v2", "targetCorpus": "pct-disclosure",
              "schemaVersion": "1", "canonVersion": "c1"},
  "claimGates": {
    "c1": [{"gateId": "af-gate-claim-as-a-whole",
            "type": "source-gate", "code": "claim-as-a-whole",
            "claimHash": "sha256/c1:e7a2…",
            "reviewState": "internally-reviewed", "migrationState": "current",
            "review": {"by": "amc", "date": "2026-07-21", "contentHash": "sha256/c1:12d4…"},
            "source": {"corpus": "af-claims-v2", "block": "S103",
                       "textHash": "sha256/c1:41f7…"}}],
    "c2": [{"gateId": "af-gate-example2-priority",
            "type": "source-gate", "code": "example2-priority-gate",
            "claimHash": "sha256/c1:52b8…",
            "reviewState": "internally-reviewed", "migrationState": "current",
            "review": {"by": "amc", "date": "2026-07-21", "contentHash": "sha256/c1:7e6a…"},
            "source": {"corpus": "af-claims-v2", "block": "S018",
                       "textHash": "sha256/c1:8c2e…"}}]
  },
  "fragments": {
    "c1u8": {
      "status": "mapped",
      "reviewState": "internally-reviewed",
      "migrationState": "current",
      "review": {"by": "amc", "date": "2026-07-21", "contentHash": "sha256/c1:41c8…"},
      "fragmentTextHash": "sha256/c1:b4d9…",
      "targets": [
        {"block": "S060", "textHash": "sha256/c1:2f18…", "role": "combination",
         "note": "Detection component derives time codes from delivered-version timings"}
      ],
      "phrases": [
        {"id": "c1u8p1", "text": "camera-source-transition pattern", "occurrence": 1,
         "status": "mapped", "reviewState": "internally-reviewed",
         "migrationState": "current",
         "review": {"by": "amc", "date": "2026-07-21", "contentHash": "sha256/c1:d977…"},
         "targets": [{"block": "S058", "textHash": "sha256/c1:aa31…", "role": "context",
                      "note": "Camera-cuts detection algorithm 131 timing analysis"}]}
      ]
    },
    "c1u11": {
      "status": "counsel-review-required",
      "reviewState": "internally-reviewed",
      "migrationState": "current",
      "review": {"by": "amc", "date": "2026-07-21", "contentHash": "sha256/c1:03e5…"},
      "fragmentTextHash": "sha256/c1:77e0…",
      "caution": {"gateId": "af-gate-source-identity",
                  "type": "source-gate", "code": "source-identity-detection",
                  "source": {"corpus": "af-claims-v2", "block": "S104",
                             "textHash": "sha256/c1:c95d…"}}
    }
  }
}
```

A third required fixture exercises the **`inapplicable-no-candidate` gate disposition**: a
`counsel-review-required` fragment listed by a mandatory target-scope gate, released without
any fabricated mapping.

Optional per-target `role` is a closed descriptive enum — `specific` | `context` |
`combination` — with no legal implication. An optional `rationale` may accompany a target:
plain text, maximum 1 000 characters, whose declared purpose is explaining target selection —
never asserting legal sufficiency; rendered only in the flat mapping schedule. Duplicate
targets within a fragment are schema-invalid. Cross-edition reuse proposals (§10) carry
`proposedFrom` provenance and enter as `reviewState: pending`.

### 8.4 Statuses, review states, migration states — lifecycle by ownership

Lifecycle state lives on the **reviewed owners**: units, phrases, claim-gate assignments,
and gate dispositions. **Field applicability is declared in schema, not prose:** `status`
applies to units and phrases only; `reviewState`, `migrationState`, and `review` apply to
every owner type. Per-owner identity (used in review projections and all external
references): **unit** = relation binding + fragment corpus + fragment ID; **phrase** = unit
identity + phrase ID; **claim-gate assignment** = relation binding + claim ID + gate ID;
**gate disposition** = gate ID + subject identity. Targets and cautions are owned
sub-objects with no lifecycle of their own; any endpoint change in an owned sub-object
stales its owner.

- `status: mapped | counsel-review-required` — recording state only (§5.3). `targets` may
  exist only when `mapped`; a `mapped` fragment must have ≥ 1 target.
- `reviewState: pending | internally-reviewed` — internal authoring progress.
  **`review.contentHash`** is the domain-tagged digest over the owner's **review
  projection** (§13): all ship-visible fields except declared locators, the hidden binding
  endpoints (`fragmentTextHash`, target and caution-source `textHash`es, aggregate
  `claimHash`, and for phrases the parent fragment's hash), **the owner's identity tuple**,
  and **the owner claim's dependency-chain hash** (§8.2). Consequences, all intended: any
  reviewed content or endpoint change — visible or hidden — invalidates
  `internally-reviewed`; transplanting a reviewed entry to a textually identical fragment
  in another claim or edition invalidates it (AF claims 1 and 20 contain verbatim-identical
  units, so this case is real); **amending a parent claim invalidates the reviews of all
  its dependents** — deliberate churn; and **mechanical re-anchoring does not** (block ids
  are declared locators outside the review projection, their identity covered by the
  included `textHash`, §13). Reuse proposals always enter as `pending`.
- `migrationState: current | stale` — `stale` is set only by `migrate` (§10) with a
  closed-enum `reason`: `changed | ambiguous | fragment-removed | target-removed |
  target-changed | source-changed | endpoint-changed | unclassified` — and preserved prior
  state (`previousTargets` for fragments); forbidden in a release. Ancestor-claim changes
  surface as `endpoint-changed` on affected dependents.
- The **release predicate** — every owner carries its applicable lifecycle fields with
  valid `contentHash`, `reviewState: internally-reviewed` and `migrationState: current`
  everywhere, gate referential integrity and dispositions satisfied — is defined once, in
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
  source). The UI quotation is **derived at build time from the pinned source block — never
  stored**; the source digest is the normative review input. A changed source hash stales
  the owner (§8.4). The priority-support maps and crosswalk are `internal` and can never be
  quoted. QA-cross-check divergences are recorded in QA metadata or resolved by downgrading
  the affected fragment to `counsel-review-required` — never rendered.
- `generalization-note` — an author-observed, purely textual observation; no source; renders
  the approved microcopy registered for its `code`.

**Declared uniqueness keys** (every collection declares its identity; validated centrally):
gate assignments unique on `(owner, gateId)` per scope and on `(fragment, target, gateId)`
at target scope — mandatory cardinality is satisfied by distinct targets, never duplicate
instances; gate dispositions unique on `(gateId, subject)`; target blocks unique within a
fragment; phrase ids unique within a unit.

**Caution codes are closed:** every `source-gate` code must exist in the applicable gate
inventory, every `generalization-note` code in the generalization-code registry
(`strings.json`), each with a per-edition display entry — enum exhaustiveness (§10) covers
types, scopes, and codes. Claim-scope gates display at the claim header and as the
**claim-level gate chip class**; "claim-as-a-whole" is one code among several; gates are
**never inherited down to units**. A gate covering several claims attaches to each gated
claim individually with the same pinned source and its own aggregate claim hash.

**Derived content is never stored:** quotations, the reverse index, labels, and counts are
computed at build time and have no schema fields; proposals to store a derivable are visible
as schema changes.

Unit indices are zero-based; `u0` is always the preamble. The UI renders `u0` as "preamble"
and `u{n}` (n ≥ 1) as "limitation n". No other numbering appears anywhere.

Schemas are versioned and closed (`additionalProperties: false`). The build accepts exactly
the schema version it ships with — no backward compatibility: when a schema changes, all
relation files are migrated in place in the same commit.

### 8.6 Edition configs

An edition config (`editions/na-v1.json`, `editions/af-v2.json`) is the **complete parameter
set** for one artifact: fragment corpus, relation set(s), target corpus, gate inventory,
dependency map, normative census, display prefix and label formats, forbidden-terms list,
QA-source bindings, output filename, provenance wording keys, legend references, and the
**declared transitive input set** used by the exact-set check (§10). Kernel and renderer
read edition knowledge from the config only (§10, edition-blindness).

## 9. Mapping methodology and QA (performed per edition)

1. **Seed.** The edition's own claim-set guidance is transcribed into the gate inventory,
   dependency map, and claim-level candidate targets. **AF is mapped independently; NA
   conclusions are never inherited.**
2. **Refinement to block level.** Each limitation unit and phrase is mapped — or explicitly
   statused `counsel-review-required` — by reading the claim language against the
   disclosure, per claim family; mandatory-gate dispositions recorded honestly (§8.1).
3. **Independent verification pass.** Every proposed target is re-checked adversarially
   against the block text; phrase substrings verified verbatim; status and disposition
   honesty confirmed.
4. **Completeness audit.** Gate referential integrity and dispositions pass in both
   directions; every owner has its applicable lifecycle fields and valid `contentHash`; the
   dependency map cross-validation passes; the mapping is cross-checked against the
   edition's priority-support map and — for AF — the crosswalk non-conflation boundary.
   **All attestations are double-sided**, created through the typed `attest` / `record-qa`
   commands (§10) as immutable records in the verification plane. Any change on either side
   mechanically invalidates the attestation.
5. **Human review.** Final pass by the internal reviewer; `reviewState:
   internally-reviewed` with fresh `contentHash` recorded per owner.

### 9.1 Standing disclaimer (always visible on screen; repeated on every printed page)

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
digests on both sides; every guarantee names its enforcer; the kernel is edition-blind and
separation between editions is enforced, not assumed.**

```
navigator/
  corpora.json            # corpus registry: unique ids, role, visibility, per-file sha256
  profiles/               # segmentation profiles + gate inventories + dependency maps
                          #   (gates_/deps_ per fragment corpus)
  relations/
    na-v1__pct.json       # NA relation set (binding: na-claims-v1 → pct-disclosure)
    af-v2__pct.json       # AF relation set (binding: af-claims-v2 → pct-disclosure)
  editions/
    na-v1.json            # complete NA parameter set incl. declared transitive inputs
    af-v2.json            # complete AF parameter set incl. declared transitive inputs
  bundles/
    na-af-2026.json       # bundle config: enumerated members, versions, digests, manifest
  schema/                 # versioned, closed JSON Schemas with per-axis tags + declared
                          #   locator exceptions + applicability matrices + invariants
                          #   module; planes.json (command×kind privilege matrix);
                          #   acceptance.json (criteria registry); api-policy.json
                          #   (probed/CSP-governed/procedural API sets);
                          #   support-matrix.json (release-approved browser/OS/AT matrix)
  strings.json            # UI-authored fixed microcopy: per-edition namespaces,
                          #   generalization-code registry, counsel legend and
                          #   bundle-manifest text (digest-bound approvals)
  build.py                # content plane: `preview` / `candidate` / `migrate`;
                          #   verification plane: `release` / `bundle` / `attest` /
                          #   `record-qa`; `propose-reuse` (deferred)
  tests/                  # golden parser + canon() + serialization vectors, invariant +
                          #   acceptance tests, registry-access, edition-blindness,
                          #   writer-set, diff-classifier, projection, forbidden-terms,
                          #   escaping fixtures, golden bundle fixture, no-candidate
                          #   disposition fixture, traceability meta-test, TDD-example and
                          #   procedure-vs-matrix comparisons, per-edition fixtures
```

**Action taxonomy.** A closed classification of what any tool may do to reviewed data:
(a) **read**; (b) **mechanical re-anchoring** — locator-field updates under
exact-hash-proven identity (relation locators and gate-inventory source locators alike),
semantic content and review state untouched — consistent by construction, since locators
are outside the review projection (§13); (c) **proposal writing** — new `pending` entries
and `stale` marks only; (d) **human edit** via git. Attestation records are written only by
the typed `attest`/`record-qa` commands into the verification plane. Every command declares
its action classes; a **diff-classifier test** verifies observed writes fall within declared
classes. **No tool ever modifies the semantic content of a reviewed entry.**

**Plane separation and privilege matrix.** Two planes; the privilege matrix is **normative
data** (`schema/planes.json`), genuinely command × kind — every kind has a declared plane
membership, cells enumerate exact kind sets, and an omitted privilege is a denied privilege.
Kind → plane: content plane — registered sources and policy data; artifact outputs —
`preview`, `candidate`, `sealed`, `bundle`, `bundle-manifest`, `artifact-checksum`,
`bundle-checksum`; verification records (append-only) — `qa-record`, `attestation`,
`release-record`.

| Command | Reads (kinds) | Writes (kinds) |
|---|---|---|
| `preview` | content (edition allowlist) | `preview` |
| `candidate` | content (edition allowlist) | `candidate` |
| `migrate` | content (edition allowlist) | sources: edition's relation set + gate-inventory locators (action classes b + c only) |
| `propose-reuse` (deferred) | content (pair-scoped grant) | sources: destination relation set (class c only) |
| `attest` | content + verification records | `attestation` |
| `record-qa` | content + `candidate` + verification records | `qa-record` |
| `release` | content + `candidate` + verification records | `sealed`, `artifact-checksum`, `release-record` |
| `bundle` | content + `sealed` + `artifact-checksum` + verification records | `bundle-manifest`, `bundle`, `bundle-checksum` |

- **Content plane** — sources, relations, inventories, dependency maps, profiles, edition
  configs, schemas, strings projection, builder tree, declared timestamp. The
  **content-input lock** is derived from the gateway's read log over this plane, sorted
  deterministically; **candidate and release must reproduce it byte-identically**. The
  **exact-set check** compares the read log against the edition config's declared
  transitive input set.
- **Verification plane — append-only, forward-chaining.** Records are digest-addressed and
  immutable; an overwrite attempt is a gateway error; each record references its
  predecessors by digest: `record-qa` creates the authorization record **before** release;
  `release` reads and references it, writing the sealed artifact, its checksum, and a
  **`release-record`** (what was sealed, when, on which authorizations); bundle records
  reference release records. Verification artifacts are never content inputs — circularity
  is unrepresentable in the matrix. **The §13 update procedure's write-statements are
  validated against `planes.json` by the procedure-vs-matrix comparison test** — prose
  about who writes what is checked, not trusted.

Guardrails, each tied to the failure it prevents:

1. **Closed, versioned schemas** — typo'd fields and ad-hoc semantics fail loudly.
2. **Conditional schema rules** (§8) — inventing targets, targeting editorial blocks,
   referencing `internal` corpora from the UI, duplicate targets/gate instances/
   dispositions (declared keys, §8.5), unsourced or inventory-orphaned source-gates,
   claim-scope generalization-notes, entries outside the declared binding, or applicability
   violations (status on a gate assignment) are unrepresentable.
3. **Single canonicalization module for every digest** (§8.2) — text rules, the completed
   canonical-JSON law (pinned Unicode version, duplicate-key rejection, exact escapes,
   integer range, raw-digest composition), and NUL-framed domain tags versioned together; a
   test asserts no digest is computed elsewhere.
4. **Gateways for all file traffic, in two planes** (matrix above), enforced by the
   registry-access AST test and review; cross-edition reads only as pair-scoped grants.
5. **Requirements as data, closed both ways, total over evidence states.** Gate coverage is
   bidirectional referential integrity over instances *and dispositions* (§8.1); a
   mandatory requirement is never satisfiable only by creating evidence; censuses,
   forbidden terms, output kinds, declared transitive inputs, privilege rows, API policy,
   support matrix, acceptance criteria, and bundle membership are enumerated data; **all
   projections are derived from schema axis tags with declared, justified exceptions**
   (§13).
6. **Migration by closed case table** (`migrate`: classes b + c; idempotent; never guesses;
   staleness rolls up to the owning reviewed object; every unlisted situation degrades to
   `stale / unclassified`):

   | Situation | Action |
   |---|---|
   | Exactly one eligible canonical-hash match at a new position | Mechanical re-anchoring: locator fields only (relations and gate inventories); semantic content and review state untouched |
   | No match — fragment text changed | Owner `stale` / `changed`; `previousTargets` retained |
   | Multiple matches — repeated text (expected: identical EDL rows) | Owner `stale` / `ambiguous` |
   | Source fragment removed | Owner `stale` / `fragment-removed`; the human deletes the entry in the resolving commit |
   | Target block removed (fragment still exists) | Owning fragment `stale` / `target-removed`; human re-targets or downgrades to `counsel-review-required` |
   | Target block text changed | Owning fragment `stale` / `target-changed`; `previousTargets` retained |
   | Caution-source block removed or text changed | Owning fragment or gate assignment `stale` / `source-changed` |
   | Claim text changed (aggregate hash mismatch), ancestor claim changed (dependency-chain mismatch), or gate endpoints changed | Affected owners `stale` / `endpoint-changed` |
   | New fragment appears | Entry created as `counsel-review-required` + `pending` |
   | Splits, merges, anything not listed above | Owner `stale` / `unclassified` |

7. **Cross-edition reuse — deferred, bounded.** `propose-reuse` (class c only): explicit
   source and destination editions; pair-scoped read grant per invocation; proposals only
   into the destination; full source digests recorded; never during an edition build. The
   crosswalk is review context and a non-transfer warning.
8. **Release by verification (candidate → sealed), per edition.** Manual QA runs against
   candidate bytes; `release` re-derives, verifies the content-input lock byte-identically,
   byte-compares the candidate, verifies every double-sided attestation in the verification
   envelope, and promotes the same bytes, writing the sealed artifact, checksum, and
   release-record. `preview` is watermarked and passes the identical shipping projection —
   the watermark is additive, never the protection.
9. **Composition sealing.** `bundle` builds a **deterministic STORE ZIP** from the single
   in-repo writer (fixed member ordering, declared timestamps, fixed permissions, pinned
   UTF-8 filename flags and central-directory behavior — verified against a **byte-exact
   golden bundle fixture**) from the explicit bundle config enumerating exactly its
   members, verifies every member digest, and emits a detached checksum for the ZIP itself.
   The neutral manifest is generated as the `bundle-manifest` output kind before packaging.
10. **Content-input lock + verification envelope** (plane separation above). Complete lock
    in the private QA record; **runtime diagnostics live in a sibling
    `reproductionDiagnostics` section — outside the lock digest and the candidate↔release
    equality check** (interpreter version, locale, platform settings; non-normative;
    byte-identity remains the authority). Safe subset
    (relation/edition/inventory/strings-projection digests, builder source-tree hash) in
    embedded provenance. **Honest limit:** the lock makes policy drift visible,
    attributable, and attestation-invalidating — it cannot make modification impossible;
    the git-reviewed commit remains the human trust root.
11. **Central microcopy registry with digest-bound approvals.** All UI-authored fixed
    microcopy in `strings.json`; approvals bind to wording digests. Authored per-entry text
    (notes, rationales) is subject to the same neutrality and forbidden-terms checks.
12. **Terminology guard, full surface.** Forbidden-terms checks cover all authored
    non-verbatim user-visible text, excluding pinned verbatim quotations. A maintained
    heuristic sourced from the registered crosswalk.
13. **Enum exhaustiveness.** Every closed enum that reaches the UI (status, role, caution
    type, scope, code, migration reason, gate disposition) has a registered presentation
    entry; build checks assert exact coverage; the type×scope matrix, code closure, and
    applicability matrices (§8.4, §8.5) are schema-enforced.
14. **Edition-blindness.** Shared modules contain no edition tokens — AST/grep-test
    enforced.
15. **Generated-file discipline.** `GENERATED` banner + detached SHA-256 + local pre-commit
    rebuild-and-compare.
16. **Confidentiality guardrail.** Build aborts in CI environments; `--private-runner` is
    the logged override. An accidental-disclosure guardrail, not proof of runner trust.
17. **Documentation that cannot lie.** The §8.3 examples, the §14 criteria list, and the
    §13 procedure's write-statements are validated against their registered data (fixtures;
    `schema/acceptance.json`; `schema/planes.json`). (The TDD is never a build input.)
18. **Traceability closure, self-binding.** Criteria carry stable IDs in
    `schema/acceptance.json`; the traceability matrix maps registry IDs to named tests or
    QA-record fields; the meta-test closes both directions over the registry, itself
    included.
19. **Collision review (procedural).** Every new mechanism folded into this document is
    checked against the guarantee → enforcement map for conflicts with existing mechanisms
    before adoption — at this density, the table's second function is collision detection.

**Quantifier discipline (procedural):** any universal claim in this document must either
cite a row of the guarantee → enforcement map or carry an explicit scope.

**Guarantee → enforcement map:**

| Guarantee | Enforcer |
|---|---|
| Unregistered, out-of-edition, out-of-plane, or untyped file access cannot occur in the pipeline | Registry accessor + typed output-kind registry + command×kind privilege matrix (`planes.json`) + pair-scoped grants + registry-access AST test |
| Silent re-anchoring cannot occur | Hash-pinned references (schema) + migration case table + diff-classifier test |
| Associations cannot silently re-aim | Both-endpoint pinning with lifecycle (schema) + migration rows |
| Every mandatory gate is carried or honestly disposed at its required scope and cardinality | Gate inventory + bidirectional referential integrity over instances and dispositions + declared uniqueness keys |
| An honest no-candidate fragment is releasable without a fabricated mapping | Closed gate-disposition enum incl. `inapplicable-no-candidate` + dedicated fixture |
| The inventory reflects the prose gates | Digest-bound human attestation — human, stated as such |
| Reviewed status cannot outlive reviewed content, visible or hidden, or its context (owner identity, binding, claim ancestry) | Review projection derived from schema axes incl. identity tuples and dependency-chain hash + `contentHash` validation |
| Mechanical re-anchoring never invalidates review | Declared locator exception: `ship: artifact` + `review: exclude` permitted only with a named covering digest (schema) |
| Dependency-chain hashes rest on a validated graph | Authored dependency map cross-validated against parsed claim references; mismatch fails the build |
| Attestations cannot outlive either side | Double-sided digest binding + typed append-only records + envelope verification |
| Evidence that authorized a release survives it unchanged; release outcomes are themselves recorded | Append-only verification plane + forward-chaining records incl. `release-record`; overwrite is a gateway error |
| Provenance cannot be self-referential | Plane separation: verification artifacts are never content inputs (privilege matrix) |
| Exactly the required inputs were read | Content read log + exact-set check against the edition config's declared transitive inputs |
| Composite digests are implementation-independent | Completed canonical serialization law (pinned Unicode version, duplicate-key rejection, exact escapes, integer range, raw composition) + NUL-framed domain tags + single-digest-path test + golden vectors |
| Derived content cannot drift | No-stored-derivables rule (schema has no fields for them) |
| Policy drift is visible and attestation-invalidating | Content-input lock derived from the gateway read log (visibility, not prevention — git commit is the trust root); diagnostics excluded from the lock digest |
| Tools act only within declared action classes | Action taxonomy + diff-classifier + writer-set tests |
| No automatic cross-edition inheritance | `propose-reuse` deferred, pair-granted, proposal-only + `pending` blocks release |
| Shared code contains no edition knowledge | Edition-blindness AST test |
| Released bytes = manually tested bytes | Seal gate: content-lock reproduction + byte-compare + QA-record digest check |
| No `pending` / `stale` / unapproved legend ships | Release predicate (invariants module) + attestation checks |
| Editorial / `internal` content never rendered or quoted; internal identifiers never shipped | Visibility rules (schema) + provenance projection + projection test |
| Authoring-lifecycle fields never ship, in any artifact kind including previews | Ship-axis-derived projection (schema) + projection test |
| A bundle contains exactly its enumerated members | Bundle config + deterministic STORE ZIP + golden bundle fixture + seal gate digest verification |
| AF/NA terminology non-conflation in authored text | Forbidden-terms check (heuristic, crosswalk-sourced) |
| Examples, criteria, and procedure statements in this TDD match their registered data | Fixture validation + TDD-comparison tests (fixtures; acceptance registry; privilege matrix) |
| Every registered acceptance criterion is carried by a live test, and every acceptance test maps to a criterion | Criteria registry + traceability matrix + bidirectional meta-test |
| The page attempts no network requests, cookie writes, Web Storage use, or navigation-API calls in the enumerated policy | CSP (§11) + attempted-use instrumentation per `api-policy.json` — governs the page; extensions and user actions are outside it; residual APIs marked CSP-governed or procedural in the policy file |
| Not built on hosted CI | CI-environment guard — procedural, not proof of trust |
| Deterministic output, artifact and bundle | Declared release timestamp + double-build comparison + STORE ZIP rules + golden bundle fixture |
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
- **Build modes:** `preview` (watermarked, same projection), `candidate`, `release`,
  `bundle` — all read-only via the gateways; `attest`/`record-qa` write append-only
  verification records.
- **Delivery bundle:** a deterministic STORE ZIP containing exactly: both sealed artifacts,
  their detached checksums, and the **neutral manifest** (`bundle-manifest` output kind;
  microcopy-registry text, counsel-approvable) identifying them as *alternative
  counsel-review editions*; the bundle ships with its own detached checksum. Either
  artifact remains releasable alone. Default bundle name:
  `AA11393US-claims-navigators_NA-2026-07-17-v1_AF-2026-07-17-v2.zip`.
- **Network and runtime posture:** the application performs no network requests and
  attempts no use of the APIs enumerated in `schema/api-policy.json` (cookies,
  localStorage/sessionStorage/indexedDB, history/location mutation) — instrumented as
  **attempted use, not final state** (AC-15); CSP — `default-src 'none'; img-src data:;
  style-src 'unsafe-inline'; script-src 'unsafe-inline'; base-uri 'none'; form-action
  'none'; object-src 'none'; connect-src 'none'` (`base-uri` and `form-action` do not
  inherit from `default-src`). Governs the page; cannot govern extensions or user actions;
  the policy file marks each API as probed, CSP-governed, or procedural.
- **Output encoding (normative):** all source-derived text escaped for its context; no
  untrusted `innerHTML`; embedded JSON script-safe-escaped (including `</script`
  sequences). **Adversarial escaping fixtures** are part of the acceptance suite.
- **Progressive readability:** with JavaScript disabled, the claims, disclosure, standing
  disclaimer, provenance panel, and flat mapping schedule (static markup) remain fully
  readable and printable.
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
  navigation preserved. Both layouts acceptance-tested.
- Highlight palette: strong vs soft clearly distinct; every state has a non-color
  indicator; claim-level gate chips visually distinct from fragment/target chips.
- **Semantic controls:** discrete `<button>` elements; no nested interactive controls
  (§5.2); logical tab order; visible focus; minimum 24 px hit targets.
- **Focus determinism:** activation moves focus to the navigation bar; Esc clears and
  returns focus; pointer activation suppressed during text selection.
- **Keyboard:** Tab/Shift-Tab traverse; Enter/Space activate; ←/→ cycle **only while the
  navigation bar has focus**; Esc clears. No global arrow-key capture.
- **Screen readers:** polite `aria-live` announcements (mode, position, target label,
  caution/gate presence). The supported browser/OS/screen-reader set is **normative data**
  (`schema/support-matrix.json`), release-approved; the QA record references it rather than
  defining it.
- **Reduced motion:** `prefers-reduced-motion` disables smooth scrolling.
- **Print stylesheet:** claims, disclosure, disclaimer, provenance, and schedule print
  cleanly; the legend repeats on every page.

## 13. Versioning, provenance and regeneration

Every artifact is a **pure build product**. Boundaries are **axes on one schema**: every
relation-schema field carries a tag per axis — `ship: artifact | schedule-only | never` and
`review: include | exclude` — an untagged field on any axis is a schema error, and
**inter-axis invariants are declared and validated**: every `ship: artifact` or
`schedule-only` field is `review: include`, **except schema-declared locator fields**
(`ship: artifact` + `review: exclude`), each of which must name the review-included digest
covering its identity (block ids ↔ target `textHash`) — an exception without its covering
proof is schema-invalid. Binding endpoint hashes, declared context references, owner
identity tuples, and the dependency-chain hash are `review: include` though `ship: never`;
lifecycle metadata and `contentHash` itself are `review: exclude`. Projections are generated
from the axes, never hand-maintained.

- **Shipping projection (ship axis):** `artifact` — status; targets (block, role, note);
  target-, fragment-, and phrase-scope cautions (gateId, type, code — quotations derived at
  render from pinned sources); phrases (id, text, occurrence, status, targets with their
  cautions); claim gates (gateId, type, code); gate dispositions (gateId, disposition).
  `schedule-only` — rationale. `never` — `proposedFrom`, `previousTargets`, `reviewState`,
  `review`, `migrationState`, endpoint hashes, identity/binding fields.
- **Review projection (review axis):** everything shipped except declared locators, plus
  all endpoint hashes, parent-context references, owner identity tuples, and the
  dependency-chain hash — the `review.contentHash` domain (§8.4), domain-tagged and
  canonically serialized (§8.2).
- **Embedded provenance projection** (About panel + machine-readable): `rendered` and
  `quotable` corpora with versions and per-file SHA-256, public authority metadata for
  `pct-pdf`, relation-set, gate-inventory, dependency-map, edition, schema, canonVersion,
  and strings-projection digests, the builder source-tree hash, the declared release
  timestamp, and counts. **Internal QA-source identifiers, paths, and hashes never appear
  in an artifact.**
- **Private QA record** (`qa-record` kind; append-only): the complete content-input lock
  including internal QA sources; a sibling **`reproductionDiagnostics`** section
  (interpreter version, locale, platform settings — non-normative, **excluded from the lock
  digest and the candidate↔release equality check**); the release-verification envelope
  (candidate digest, lock digest, all double-sided attestations by digest reference); the
  reference to the release-approved support matrix; and the operator.
- **Deterministic build:** declared release timestamp; stable ordering; double-build
  byte-identity; candidate/release lock reproduction and byte comparison; deterministic
  STORE bundle with golden fixture.
- **Normative update procedure (per edition):** (1) amend source(s), gate inventory,
  dependency map, or relations; (2) `build.py candidate <edition>` — read-only; fails
  listing every hash-stale entry, referential-integrity or disposition gap, exact-set
  mismatch, and schema violation; (3) `build.py migrate <edition>` — applies the §10 case
  table; (4) resolve each `stale`/`pending`, restore `reviewState: internally-reviewed`
  with fresh `contentHash` (git diff is the review artifact); (5) `build.py candidate
  <edition>`; (6) manual QA against those exact bytes → `record-qa` (immutable
  authorization record); refresh attestations via `attest` as needed (new immutable
  records); (7) `build.py release <edition>` — reproduces the content lock, byte-compares
  the candidate, verifies the envelope, seals the same bytes, and writes the sealed
  artifact, its checksum, and the `release-record`; (8) `build.py bundle` when both
  editions are sealed; (9) commit sources + relations, then artifacts with checksums and
  records. (Write-statements in this procedure are validated against `planes.json`, §10.)
- Each file name and header embeds its claim-set version; a stale-claim-set navigator is
  immediately identifiable.

## 14. Acceptance criteria (definition of done)

Criteria carry stable IDs in the criteria registry (`schema/acceptance.json`); this section
must match the registry (comparison test, §10.17); the traceability matrix and meta-test
close both directions over the registry, **including AC-19 and AC-20 themselves**.
**Applicability: a standalone edition release requires AC-01 – AC-19; bundle creation
additionally requires AC-20.**

**Per edition (AC-01 … AC-18)** — all pass (automated except where noted):

1. **AC-01** Source extraction reproduces the edition's normative census exactly (§3),
   including the authored dependency map cross-validated against parsed claim references;
   PCT claims 1–18, Examples 1–5, Tables 1–3 with row anchors, four figures present and
   hash-verified.
2. **AC-02** Every owner carries its applicable lifecycle fields with a valid
   `review.contentHash` over the review projection (incl. identity tuples and
   dependency-chain hash); zero `pending`, zero `stale`.
3. **AC-03** Gate referential integrity passes in both directions with declared uniqueness
   keys; every mandatory gate has a reviewed disposition; the no-candidate disposition
   fixture releases without a fabricated mapping; the inventory-completeness human
   attestation is current.
4. **AC-04** Zero unresolved source drift: all corpus, fragment, aggregate-claim,
   dependency-chain, target, and caution-source digests current (full digests, matching
   canonVersion).
5. **AC-05** All schema and invariant validations pass: axis tags present with inter-axis
   invariants and declared locator exceptions satisfied; applicability matrices;
   relation-binding conformity; phrase rules; no duplicate targets, gate instances, or
   dispositions; note and rationale bounds; caution type×scope matrix and code closure;
   caution sources resolve into `quotable` blocks only; zero targets on editorial,
   excluded, or `internal` blocks; enum ↔ presentation coverage; forbidden-terms check
   clean.
6. **AC-06** The edition's fixtures (including the disposition fixture) validate against
   schemas and pinned corpora; this document's examples match the fixture projections.
7. **AC-07** Registry-access, edition-blindness, writer-set, diff-classifier,
   single-digest-path, and procedure-vs-matrix tests pass; canonical serialization golden
   vectors pass.
8. **AC-08** Projection tests pass: no `never`-tagged field and no internal QA-source
   identifier appears in any artifact kind, previews included.
9. **AC-09** Adversarial escaping fixtures render safely through every authored and quoted
   channel.
10. **AC-10** Forward and reverse navigation behave per §§5–6, including claim-level gate
    display (scripted checks on the built candidate).
11. **AC-11** Keyboard-only operation, focus determinism, and screen-reader announcements
    per §12 against the release-approved support matrix (manual, against candidate bytes,
    recorded in the QA record).
12. **AC-12** Print output per §12 (manual, against candidate bytes).
13. **AC-13** Local-file operation across the support matrix (`schema/support-matrix.json`),
    including minimum-viewport and stacked layouts.
14. **AC-14** With JavaScript disabled, the §11 static content is fully readable.
15. **AC-15** Attempted-use instrumentation per `schema/api-policy.json` records zero
    external requests, zero cookie writes, zero Web Storage/IndexedDB use, and zero
    navigation-API mutation attempts.
16. **AC-16** Double build byte-identical; content-input lock reproduces byte-identically
    between candidate and release (diagnostics excluded); exact-set check passes; `release`
    byte-compares against the QA'd candidate and seals the same bytes; lock, envelope, and
    release-record written append-only; checksums emitted and matching.
17. **AC-17** §9.1 disclaimer and approved legend present on screen, in print, and no-JS;
    legend approval matches the shipped wording digest.
18. **AC-18** Double-sided QA attestations current, authored via the typed commands:
    priority-map cross-check and, for AF, the crosswalk non-conflation check.

**Shared** — **AC-19** The traceability meta-test passes over the criteria registry: every
registered criterion (AC-01 through AC-20, including this one) maps to named live tests or
QA-record fields, and every acceptance-designated test maps back to a registered criterion.

**Bundle** — **AC-20** The bundle matches its config exactly (enumerated members only,
including the `bundle-manifest`), every member digest verified, deterministic STORE ZIP
conforming to the golden bundle fixture with its own detached checksum, and the neutral
manifest matching its approved wording digest.

## 15. Roadmap (not in the current deliverable)

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
| Requirements as data | Coverage proven by bidirectional referential integrity over instances and dispositions; **policies are total over evidence states — honest absence is a releasable, reviewed disposition**; inventory completeness is a digest-bound human attestation; acceptance criteria, API policy, and support matrix live in registries |
| Associations | Every association pins both endpoints by digest and carries lifecycle where reviewed; `gateId` required on every source-gate instance; declared uniqueness keys on every collection |
| Lifecycle | Ownership model with schema-declared applicability matrices and per-owner identity tuples; sub-object changes roll up; closed staleness-reason enum |
| Reviews & attestations | Double-sided digest binding; `review.contentHash` over the review projection — content, hidden endpoints, identity tuples, and dependency-chain hash; **declared locators excluded, so mechanical re-anchoring never invalidates review**; parent-claim amendments deliberately cascade re-review to dependents; typed append-only records |
| Trust root & planes | Content-input lock derived from the gateway read log with exact-set check, **diagnostics excluded from the lock digest**; forward-chaining verification records incl. `release-record`; command×kind privilege matrix; procedure prose validated against the matrix; git commit is the human trust root |
| Enumerations & boundaries | All projections derived from schema axis tags with declared, justified exceptions; gateway-enforced output-kind registry with plane membership; derived content never stored |
| Serialization | Completed canonical-JSON law (pinned Unicode version, post-NFC duplicate-key rejection, exact escapes, integer range, raw-digest composition) + NUL-framed domain tags incl. `figure`, versioned under canonVersion; single-digest-path test; golden vectors confirm |
| Structural graphs | Dual-sourced: authored dependency maps cross-validated against parsed claim references; mismatch fails the build |
| Cross-edition isolation | Unique corpus ids; scoped triples; binding rules; per-edition allowlists; edition failures never cross (shared-input failures affect both; bundle needs both) |
| Cross-edition reuse | Deferred optional hardening; pair-granted, proposal-only; crosswalk is context and warning, not evidence |
| Click granularity | Two-tier: limitation units + inner key phrases with stable phrase IDs |
| Evidence model | `status` (units/phrases) ⊥ `reviewState` ⊥ `migrationState` per applicability matrix; no forced positive mappings — including via gate cardinality; release predicate defined once |
| Cautions | Closed types × scopes × codes with schema-enforced matrix; claim-level gates never inherited to units; "claim-as-a-whole" is one code, not the class name |
| Identity | Positional IDs as declared locators; semantic identity pinned by full SHA-256 canonical hashes (incl. aggregate claim and dependency-chain hashes) |
| Tool behavior | Closed action taxonomy; commands declare classes; diff-classifier enforces; reviewed semantic content is never tool-modified |
| Migration | Closed case table with roll-up staleness and complete reason enum; auto-re-anchoring only on unique canonical-hash match |
| Release lifecycle | Promotion by verification per edition; edition release = AC-01–AC-19, bundle adds AC-20; deterministic STORE bundle with golden fixture; previews pass the same projection |
| Traceability | Guarantee table (claims→enforcers, and collision detection between mechanisms) + fixture/registry/procedure comparisons + bidirectional traceability meta-test: checked loops that include themselves |
| Environment | Negative guarantees instrumented as attempted use per the enumerated API policy; runtime determinants as non-normative diagnostics outside the lock digest; support matrix is release-approved normative data |
| Multi-candidate behavior | Jump to first + cycle; all candidates kept; display cap presentation-only |
| Right-column scope | As-filed disclosure package; editorial content labeled and non-targetable; PCT claims targetable per the disclosure profile |
| QA boundary | Corpus visibility validator-enforced; QA sources `internal`, never quoted, never identified in artifacts |
| Directionality | Left→right primary; reverse via edition-scoped badges only; disclosure text never clickable |
| Terminology | Neutral throughout; per-edition namespaces; forbidden-terms and neutrality checks over all authored user-visible text; approvals digest-bound |
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
