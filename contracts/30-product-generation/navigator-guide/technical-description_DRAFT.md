# AA11393US — HTML5 Navigator Guide: Technical Description (DRAFT)

> **OPERATIVE GUIDE CONTRACT · INTERNAL REVIEW DRAFT · NOT FOR FILING**
>
> This document defines the shared guide contract for the four current HTML5 navigator
> products: an on-load orientation overlay with a persistent reopen control, carried without
> JavaScript by an in-document fallback. Its paired executable outcomes are in the
> [acceptance criteria](acceptance-criteria_DRAFT.md) and are projected from
> [`navigator/schema/guide-acceptance.json`](../../../navigator/schema/guide-acceptance.json).

The `_DRAFT` suffix records internal review status. Every rule in this pair states required
current product behavior. The pair owns the guide mechanism and guide wording closure only; it
creates no semantic content or legal conclusion.

## 1. Purpose and boundary

The guide contract orients a first-time reviewer of each navigator product: what the page
binds, what each pane shows, what the visual states mean, and how to move between a claim and
its evidence. It governs the on-load overlay, the persistent reopen control, the no-JavaScript
and print carriers, the two product-kind content profiles, and the wording-slot sourcing of all
guide text.

The claims-to-specification, claims-to-prior-art, and navigator-presentation pairs continue to
own their content, candidate semantics, emphasis policy, navigation state, exact relation
endpoints, typography, measure, resize, reflow, spacing, no-JavaScript reading, print
requirements, evidence authority, and legal boundary. This pair does not change claim wording,
disclosure text, prior-art text, mappings, scores, cautions, dispositions, provenance, product
identity, or authority direction, and it does not restate another pair's rule; it cites the
owning pair.

The current product profile remains `technical-preview`. The pinned browser supplies executable
technical acceptance; observation in any unpinned browser creates no compatibility claim.

## 2. Shared ownership and product isolation

One shared renderer owns the guide mechanism — overlay structure, behavior, and chrome — for
all four configured products. The renderer selects a content profile from the explicit product
kind only: specification products present Profile S; prior-art products present Profile P.
Editions within one kind (NA, AF) differ only through wording-slot substitution, never through
structure. The mechanism cannot truncate, suppress, reorder, retarget, summarize, or reinterpret
semantic content, and guide behavior never changes semantic state: opening, dismissing, or
reopening the guide alters no candidate selection, emphasis set, navigation target, scroll
owner, or obligation state owned by the product contracts.

## 3. Launch and reopen behavior

The guide is stateless. There is no stored preference, no first-visit detection, and no
dismissal persistence; the sealed single-file products have no storage model.

| Context | On load | Reopen | Carrier |
|---|---|---|---|
| JavaScript enabled | The overlay opens on every load | The persistent masthead Guide control reopens it | Modal `<dialog>` overlay |
| JavaScript removed | Nothing opens; reading is unaffected | The in-document guide section is directly operable | `<details class="guide">` in document order |
| Print | — | — | Overlay and guide content are excluded; the counsel-review legend continues to print |
| Reduced motion | No entry animation | No animation | Same carriers |

## 4. Overlay mechanics

The overlay is a native `<dialog>` element opened modally. Escape, backdrop activation, and an
explicit close control each dismiss it. Focus is contained while the overlay is open and returns
to the invoking Guide control on close. The overlay presents the product-kind profile as
ordinary prose within the controlled readable measure, at the applicable typography tiers, and
never owns page-level horizontal scrolling. All behavior executes as CSP-compatible inline
script; the overlay issues no network request and reads or writes no storage.

## 5. No-JavaScript and print carriers

With JavaScript removed, the same guide content remains in readable document order as a
`<details class="guide">` block immediately following the masthead legend, closed by default and
natively keyboard-operable. The no-script carrier does not hide, shrink, truncate, or reorder
semantic content; the navigator-presentation pair owns the general no-JavaScript reading rule
and this pair adds no exception to it. Print excludes the overlay and the guide section as
interface furniture; the counsel-review legend owned by the product
contracts continues to print under the owning pairs' rules.

## 6. Content profiles

Profile content is wording, not semantics. Where a profile line describes candidate indication
or emphasis, the owning product-kind pair's rule controls; a contradiction between guide wording
and an owning pair fails.

**Profile S — claims ↔ specification** (`na-specification`, `af-specification`):

1. What this page binds: strategy, claim-set version, edition; a counsel-review aid, not filing
   material.
2. The two panes: claims and specification passages; their scroll ownership.
3. Candidate indication: selected candidate, selected-candidate context, and
   alternate-candidate passage; every recorded candidate endpoint is concurrently indicated.
4. Movement: claim-to-evidence activation, forward and reverse navigation, and the movement and
   clear controls shown as inert glyph tokens — candidate (`◀C`/`C▶`) and passage (`◀P`/`P▶`)
   movement in the forward bar, reverse movement (`◀`/`▶`), and clear (`×`).
5. Gates and cautions displayed with claims.
6. The color and state legend.
7. Review posture: draft counsel-review aid and ephemeral technical preview, no legal opinion of
   any kind, one-strategy presentation, anchor references not citable; human review of the source
   evidence remains authoritative.

**Profile P — claims ↔ prior art** (`na-prior-art`, `af-prior-art`):

1. What this page binds: claim-set version, comparison matrix, and passage map; scores are
   issue-spotting, not conclusions, and the page is not an admission.
2. The two panes: claim obligations and prior-art passages.
3. Obligation states: authored exact states, the `counsel-review-required` unit state where no
   candidate is recorded, and neutral fragment-review allocations.
4. Emphasis: only the selected candidate's passages receive forward emphasis — the opposite
   convention from Profile S, stated explicitly.
5. The scoring legend: `P` marks a concrete partial or analogous mapping and `—` marks no
   concrete whole-claim mapping; neither is an obviousness conclusion or a clearance.
6. Movement: claim ↔ matrix row ↔ art passage; the contextual reader; and the movement and
   clear controls shown as inert glyph tokens — candidate (`◀C`/`C▶`) and passage (`◀P`/`P▶`)
   movement in the forward bar, reverse movement (`◀`/`▶`), and clear (`×`).
7. Review posture and version binding: a matrix is valid only for the claim-set version named
   in its header; draft counsel-review aid and ephemeral technical preview, no legal opinion of
   any kind and no admission, PDF fidelity authority, anchor references not citable; human review
   of the source evidence remains authoritative.

## 7. Wording governance

All guide text arrives as typed wording slots, never hardcoded in the renderer. Chrome labels
(Guide, close, modal title pattern), the control glyphs (`◀C`, `C▶`, `◀P`, `P▶`, `◀`, `▶`,
`×`), and the Profile S body live in `shared.wording.xml` with strategy and version substitution;
the Profile P body lives in `prior-art.wording.xml`, which also carries the prior-art copies of
the chrome labels and control glyphs because the prior-art products read only that wording file.
Edition-specific cautions, if any, live in the per-edition wording files. Each slot carries one
typed scalar type and one exact origin, is rendered as escaped plain text, and is consumed;
hardcoded, unused, or unresolved slots fail. Each control glyph has one wording origin: the
renderer resolves it into the navigation controls, and the guide Movement items substitute it
through their typed slots, so the chrome and the guide copy cannot drift apart. Guide glyph
tokens are inert presentation spans, never controls.

## 8. Browser control and executable enforcement

`navigator/policy/browser.json` remains the sole live browser, viewport, motion, typography,
resize, reflow, and text-spacing execution control; the guide adds no conflicting copy. The
executable vectors exercise, for every configured product under ordinary and reduced motion:
on-load opening, Guide-control reopening, each dismissal route, focus containment and return,
the no-JavaScript carrier, print exclusion, 200% text resize, 200% page zoom, the 320 CSS-pixel
reflow, and the text-spacing override. Unsupported control shape, absent vector, skipped
product, skipped motion preference, runtime fallback, or self-reported result fails closed.

## 9. Determinism and statelessness

Under JavaScript the overlay opens on every load. No preference is read or written, no state
persists between loads, and the guide adds no runtime state to the sealed semantic model.
Candidate generation and sealed reproduction remain byte-stable with the guide present; the
candidate and its sealed product remain byte-identical.

## 10. Worktree validation and implementation closure

This contract pair, its data-only acceptance registry
[`navigator/schema/guide-acceptance.json`](../../../navigator/schema/guide-acceptance.json),
both navigator product contracts, the navigator-presentation pair, browser control, shared
renderer, guide wording slots, exact implementation and workflow census, registered tests and
vectors, runbook, four candidates, four sealed products and checksums, and delivery bundle
form one indivisible current implementation. No documentation-only, registry-only, control-only,
implementation-only, test-only, workflow-only, or product-only state is accepted.

The acceptance registry owns the ordered criterion IDs, scopes, outcomes, and enforcers. Its
Markdown table is a generated projection and has no independent row ownership. Every shared guide
change regenerates all four candidates, all four sealed products and checksums, and the
configured bundle.

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

Acceptance fails for an overlay that blocks no-JavaScript reading or print, a missing reopen
control, lost or trapped focus, semantic-state change on guide interaction, hardcoded or
unresolved wording, a content-profile contradiction with an owning pair, an undersized or
unbounded overlay text surface, persistence or storage of guide state, a stale generated
product, or incomplete deterministic closure.
