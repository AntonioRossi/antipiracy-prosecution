# AA11393US — Claims-to-Prior-Art Navigator Technical Description

> **OPERATIVE INTERNAL CONTROL · NOT FOR FILING**
>
> This document defines the current NA and AF claims-to-prior-art HTML5 products. The paired
> executable outcomes are in the [acceptance criteria](acceptance-criteria_DRAFT.md).

## 1. Product outcome and legal boundary

The current product inventory contains one claims-to-prior-art navigator for the normal-allowance
claim set and one for the allowance-first claim set. Each product lets inventor and US counsel:

- select an exact claim unit or exact phrase;
- inspect zero, one, or many independently identified candidate correspondences;
- move through every ordered passage within the selected candidate;
- distinguish fragment-specific candidates and review allocations from claim-level matrix
  obligation totals;
- open the complete asserted XML transcription at the selected passage;
- move from a passage back to every exact candidate and claim fragment using it.

The navigator is a review aid. A recorded association is not a conclusion that a document discloses
a limitation, anticipates a claim, renders a claim obvious, establishes a legal combination, or has
any other legal effect. `counsel-review-required` states that a material matrix relationship lacks
an exact bound candidate. `reviewed-no-material-passage` is limited to its exact matrix field. Human
review of the source PDF, transcription uncertainty, the claim as a whole, and applicable law
remains authoritative.

## 2. Exact authority direction

```text
claim-set Markdown
  └─generated authoritative XML claim surface──────────────┐
                                                            │
strategy comparison-matrix relation XML────────────────────┼─▶ immutable product model
  └─owns document scope and claim-level assessments         │
                                                            │
strategy passage-map-v2 relation XML───────────────────────┤
  ├─owns normalized obligation state                        │
  ├─owns exact fragment-review allocations                  │
  └─owns exact candidates and ordered passage members       │
                                                            │
registered prior-art transcription XML─────────────────────┘
  └─supplies exact passage content, provenance, and readers

immutable product model ─▶ self-contained HTML5 ─▶ checksum ─▶ four-product bundle
```

The product never derives a candidate or review allocation from matrix prose, scores, claim
wording, whole-document endpoints, text similarity, search output, rendered Markdown, ancestry, or
defaults. Each prior-art package's canonical source PDF remains the fidelity authority. Its
asserted transcription XML is the sole machine-readable passage surface.

## 3. Current passage-map product semantics

The two current relation packages are:

- `aa11393us-na-claim-prior-art-passage-map`;
- `aa11393us-af-claim-prior-art-passage-map`.

They exclusively use `claim-prior-art-passage-map-v2`. No other profile has a registry entry,
parser branch, alias, migration reader, fixture, or product path.

### 3.1 Claim-level matrix obligations

Every obligation computed under the phase-20 contract occurs exactly once and has one exact state:
`passage-mapped`, `counsel-review-required`, or `reviewed-no-material-passage`. The product computes
the complete per-claim and per-document census and the three status totals directly from the sealed
model. These totals are claim-level review coverage and are never presented as fragment candidate
or passage counts.

### 3.2 Fragment-review allocations

An exact fragment-review allocation identifies an unresolved claim-level obligation as relevant to
one exact claim unit. It carries no passage and no duplicated status. Allocations are displayed as
an outstanding fragment-specific review queue, separately from mapped candidates and claim-level
totals. An unallocated obligation remains visible in the claim-level and document-grouped schedule;
the product never narrows it by inference.

### 3.3 Exact candidates and passage members

One exact unit or unique phrase may own zero, one, or many candidate relations. Candidate identity,
role, proposition, obligation identities, and ordered evidence endpoints remain explicit in the
model and embedded product data. A candidate can have one passage or several passages that must be
reviewed together. Each member remains independently selectable while retaining the candidate's
combination semantics.

The per-unit display state is computed only from the exact unit-candidate index. It carries no
copied target list. The ordered passage list is the sole candidate-member state; no `primary`,
cached current passage, copied selected target, or equivalent alias is retained. Phrase candidates
do not cause their complete parent unit to appear mapped.

Candidate relations have unique semantic signatures based on canonical evidence-endpoint identity
while preserving authored endpoint order for presentation. Distinct candidates may share a mapped
obligation or passage, but proposition changes and endpoint permutations do not evade duplicate
rejection. A preamble is an exact preamble unit, not a whole-claim aggregation surface; synthetic
whole-claim and multi-limitation roll-ups fail. Candidate admissibility completes before obligation
coverage is computed, so a rejected candidate supplies no residual mapped state.

## 4. Current immutable model

One retained worktree capture supplies the product control, parser controls, content registry,
claim handoff, comparison-matrix handoff, current passage-map handoff, all matrix-scope transcription
handoffs, controlled wording, and schemas. All structured-source domains validate before model
construction.

The sealed model preserves:

- product, strategy, claim-set, artifact, consumer, relation-set, obligation, allocation, candidate,
  and passage identities;
- claim hierarchy, exact units, dependencies, order, text, and typed digests;
- matrix scope and every exact obligation and state;
- obligations and status totals by claim;
- candidates and allocations by exact fragment;
- ordered passage members within each candidate;
- target passage text, provenance, uncertainty, digest, and complete XML reader trees;
- passage-to-candidate-to-fragment reverse indexes;
- controlled wording, source XML roles, registered paths, XML byte digests, and the complete read
  lock.

Construction accepts no unresolved-as-empty lookup, default, inferred package, reopened source
path, mutable parse tree, detached validation result, product-local semantic copy, compatibility
shape, or duplicate semantic signature. Rendering and release consume only the sealed model.

## 5. HTML5 review surface

Each product is one self-contained UTF-8 HTML5 file with two coordinated panes:

- the left pane displays the exact claim hierarchy and makes every unit and authored exact phrase
  selectable;
- the right pane displays all in-scope documents, every matrix obligation and state, every mapped
  passage, and one complete asserted-XML transcription reader per document.

For a selected fragment the navigation bar displays separately:

- exact candidate count for that fragment;
- fragment-review allocation count;
- selected candidate position and identity;
- selected passage position within that candidate;
- claim-level mapped, review-required, and no-material obligation totals.

The interaction state has independent `candidateIndex` and `passageIndex` values. Candidate movement
wraps deterministically and resets the passage index. Passage movement wraps within the selected
candidate without changing its role, proposition, or obligation semantics. Selection highlights
the current passage strongly and other members of the same candidate as related context.

Activating an exact fragment selects candidate zero and passage zero. The selected candidate is
derived only from that fragment's candidate list and `candidateIndex`; the selected passage is
derived only from that candidate's ordered passage list and `passageIndex`. No cached selected
candidate, selected passage, first-member alias, or generic position value is authoritative.

Focus is applied with scroll prevention before right-pane navigation. The renderer then positions
the exact selected passage inside the visible right-pane viewport by assigning the explicit pane
owner's scroll offset directly. Movement is immediate under ordinary and reduced-motion settings,
so browser animation policy cannot leave the target off-screen. The contextual-reader control opens
the full reader at that selected passage and places keyboard focus on the same exact fragment
without browser history or location mutation.

Navigation success is the resulting state, focus, highlighting, and viewport position, not the
invocation of a scrolling API. After activation or movement, the navigation bar has keyboard focus,
the selected passage anchor is inside the unobscured right-pane viewport, only that passage has
strong emphasis, and the other members of the selected candidate have secondary emphasis. The same
postconditions apply under ordinary and reduced-motion settings.

Reverse navigation from a passage cycles every exact candidate occurrence using it. Each occurrence
retains the exact relation identity, candidate identity and position, claim fragment, and selected
passage identity; shared passages and multiple candidates for one fragment do not collapse into one
reference. Clearing a selection removes transient state and returns focus predictably.

The ordinary document, complete schedule, no-script view, and print view contain every substantive
claim, obligation state, allocation note, candidate identity, role, proposition, passage member,
provenance item, uncertainty, and disclaimer outside script data. Static HTML uses semantic
controls, logical order, visible focus, non-color indicators, a live region, reduced-motion rules,
bounded independent pane scrolling, minimum usable dimensions, and deterministic stacking.

## 6. Security and wording

The product contains no network request, telemetry, cookie, browser storage, location/history
mutation, external asset, form submission, or dynamic code loading capability. Its exact content
security policy denies all capabilities except inline product CSS/JavaScript and embedded data
images. All dynamic text is context-escaped before insertion into HTML or inert JSON.

The prior-art wording XML owns confidentiality, standing disclaimer, mapping statuses,
candidate-role labels, evidence authority, provenance, product label, preview watermark, and neutral
bundle wording. Ordinary candidate/passage controls and count labels remain renderer-owned interface
copy.

## 7. Product controls and publication

The exact product IDs are:

- `na-specification`;
- `af-specification`;
- `na-prior-art`;
- `af-prior-art`.

`preview`, `candidate`, and `release` require one exact ID. No shorter identity or implicit product
choice exists. Candidate generation writes only the declared candidate path. Release requires that
candidate's exact bytes and a fresh isolated reproduction, then publishes the sealed HTML and
detached checksum. The deterministic bundle contains four ordered HTML/checksum pairs followed by
the neutral manifest and has one detached checksum.

No alternate renderer, non-current profile, two-product bundle, migration utility, stored validation
result, release receipt, approval record, review log, suggestion store, or auxiliary
lineage/coverage product belongs to the live state.

## 8. Current-state authoring and regeneration

A passage-map change is complete only when all affected current owners agree:

1. reconcile the independently computed obligation census and each exact state;
2. author or remove exact fragment-review allocations and candidates in current profile XML;
3. reject preamble roll-ups, duplicate signatures, inferred semantics, and wrong-document closure;
4. regenerate both relation Markdown projections;
5. run positive and adverse model, rendering, security, interaction, release, and bundle vectors,
   including a current-profile rendered vector with two candidates for one fragment, a multi-passage
   candidate, a shared passage, an exact review allocation, and an unresolved fragment;
6. regenerate all four candidates and sealed products, checksums, and the bundle;
7. inspect candidate and passage movement, right-pane scrolling, reverse navigation, and exact
   full-reader focus in a browser;
8. pass the aggregate gate with an unchanged final recapture.

The contract pair, data registry, active profile and maps, declared handoffs, model, renderer,
tests and vectors, generated views, four products, checksums, and bundle form one indivisible current implementation.
No component is accepted independently.

Ephemeral search may help locate XML text, but no suggestion has authority or retained state. Only
human-confirmed allocations and candidates are authored. Machine acceptance cannot establish that
the mapping is substantively complete or legally correct.

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

## 9. Failure conditions

Acceptance fails for any missing or extra product, consumer, map package, matrix obligation,
allocation, candidate, passage, scope document, reader, handoff, generated view, stored product,
checksum, bundle member, implementation path, contract, registry, profile, test, or vector. It also
fails for stale or whole-document passage targets, inconsistent post-validation obligation closure,
duplicate or endpoint-permuted semantics, synthetic preamble roll-ups, inferred or copied mappings,
parallel selection state, conflated counts, an off-screen selected anchor, wrong focus or emphasis,
wrong full-reader focus, collapsed reverse occurrences, hostile unescaped content, forbidden browser
capability, nondeterministic bytes, partial publication, compatibility code, alternate paths, and
retained duplicated or orphaned implementation.
