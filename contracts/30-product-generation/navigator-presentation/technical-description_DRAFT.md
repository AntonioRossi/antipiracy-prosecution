# AA11393US — HTML5 Navigator Presentation and Readability: Technical Description (DRAFT)

> **OPERATIVE PRESENTATION CONTRACT · INTERNAL REVIEW DRAFT · NOT FOR FILING**
>
> This document defines the shared presentation contract for the four current HTML5 navigator
> products. Its paired executable outcomes are in the
> [acceptance criteria](acceptance-criteria_DRAFT.md) and are projected from
> [`navigator/schema/presentation-acceptance.json`](../../../navigator/schema/presentation-acceptance.json).

The `_DRAFT` suffix records internal review status. Every rule in this pair states required current
product behavior. The pair owns presentation only; it creates no semantic content or legal
conclusion.

## 1. Purpose and boundary

The presentation contract makes the complete navigator surfaces comfortably readable at ordinary
browser settings and resilient to user enlargement. It governs typography, readable measure,
wrapping, responsive layout, zoom and text resize, text-spacing adaptation, presentation geometry,
no-JavaScript reading, and print.

The claims-to-specification and claims-to-prior-art contracts continue to own their respective
content, candidate semantics, emphasis policy, navigation state, exact relation endpoints, evidence
authority, and legal boundary. This pair does not change claim wording, disclosure text, prior-art
text, mappings, scores, cautions, dispositions, provenance, product identity, or authority
direction. It does not establish formal accessibility, alternate-browser, operating-system,
assistive-technology, or print-engine conformance.

The current product profile remains `technical-preview`. The pinned browser supplies executable
technical acceptance; browser-neutral HTML and CSS remain mandatory, but observation in Brave or
another unpinned browser creates no compatibility claim.

## 2. Shared ownership and product isolation

One shared renderer owns the HTML structure, presentation tokens, CSS, ordinary interface labels,
and presentation behavior of all four configured products:

```text
product-owned sealed semantic model
        │
        ▼
shared renderer + one presentation control
        │
        ▼
self-contained HTML5 product
        │
        ├─ ordinary interactive surface
        ├─ resized and reflowed surface
        ├─ no-JavaScript reading surface
        └─ print surface
```

The renderer may select a presentation rule from the explicit product kind only where the
controlling product contract requires different semantic behavior. It cannot use presentation to
truncate, suppress, reorder, retarget, summarize, or reinterpret semantic content. A readability
change applies to NA, AF, specification, and prior-art products unless an exact product-owned
semantic difference requires otherwise.

`navigator/policy/browser.json` is the sole live browser, viewport, motion, typography, resize,
reflow, and text-spacing execution control. Renderer constants, tests, runbook instructions, and
stored products cannot carry a conflicting copy. Contract, control, renderer, test, or product
disagreement fails; no precedence rule or fallback chooses one.

## 3. Typography contract

The browser root default remains user-controlled. Visible text uses inherited relative units;
absolute pixel font sizes, viewport-relative font sizes, responsive font reduction, and a shorthand
that resets a required line-height are forbidden. Pixels remain appropriate for borders, minimum
control dimensions, focus outlines, and the exact navigation clearance owned by the product
contracts.

At a `16px` browser root, the exact minimum tiers are:

| Tier | Included surfaces | Minimum size | Minimum unitless line-height |
|---|---|---:|---:|
| Reading | Claim text, specification disclosure, selected prior-art passages, full transcription readers, schedule substance, provenance substance | `1.125rem` (`18px`) | `1.5` |
| Interface | Product title, group and claim headings, controls, navigation state, candidate and passage context, obligations, cautions, dispositions, required legends, profile label, disclaimer, table and figure text | `0.875rem` (`14px`) | `1.35` |
| Auxiliary | Internal anchor labels and genuinely secondary location metadata | `0.75rem` (`12px`) | `1.35` |

A heading cannot be smaller than the tier of the content it heads. Required legal, cautionary,
authority, or recording-state wording is never auxiliary. Symbol-only controls retain a readable
visible symbol and an exact accessible name. Visually hidden live-region text is exempt from visual
size measurement but not from semantic completeness.

Changing the browser's default font size increases every tier proportionally. No media query,
product kind, document kind, print rule, no-script rule, long label, or crowded viewport may reduce
a tier below its minimum. Increased document length and additional scrolling are accepted
consequences of readable text.

## 4. Reading measure, wrapping, and overflow

Every ordinary block of prose has an available inline measure no greater than `80ch`. This bound
applies to claims, specification passages, prior-art excerpts, full transcription readers,
disclaimers, caution details, provenance prose, and schedule prose. A narrower containing pane may
reduce the measure but cannot reduce its typography tier.

Words, candidate identities, relation identities, source labels, controlled wording, and accessible
control text wrap without clipping, collision, or page-level horizontal scrolling. Presentation
must not insert semantic punctuation or alter the underlying text to obtain wrapping.

Tables, code blocks, and figures whose two-dimensional layout is intrinsic may own a visibly scoped
horizontal overflow container. That exception applies only to the intrinsic surface; headings,
captions, notes, adjacent prose, and the page remain reflowable. Nested or accidental overflow,
clipped focus outlines, hidden columns without a reachable scrollbar, and body-level horizontal
scrolling fail.

## 5. Baseline layout at ordinary zoom

At `100%` page zoom, every configured product satisfies the controlled `1280×720`, `1279×720`,
`1280×719`, and `1000×700` viewport matrix under ordinary and reduced motion. The product contracts
retain ownership of the exact side-by-side threshold, stacked mode, capable scroll owners, target
clearance, and product-specific emphasis sets.

For every baseline vector:

- each typography role resolves to its exact minimum tier or larger;
- ordinary prose respects the maximum measure;
- required text and controls are neither clipped nor overlapped;
- the application and each required scroll owner have a positive usable area;
- the masthead, profile label, legends, disclaimer, navigation bars, panes, auxiliary surface, and
  controls remain reachable;
- focus indicators remain fully visible; and
- no page error, unintended horizontal page overflow, network request, or semantic-state change
  occurs.

Comfortable readability at `100%` is a product requirement. Browser zoom is a supported user
preference, not a prerequisite for reading ordinary product text.

## 6. Text resize, page zoom, and reflow

Each product supports both text-only resize to `200%` and page zoom to `200%`. Enlargement preserves
all substantive and cautionary content, controls, accessible names and states, forward and reverse
occurrences, candidate and passage positions, focus, exact capable owners, and product-owned
highlight semantics. Text does not overlap, clip, disappear, or become available only through an
unreachable control.

The controlled reflow vector presents the product at `320` CSS pixels of inline viewport. Ordinary
content reflows without two-dimensional page scrolling. Every required surface remains reachable,
and the active application retains a positive usable target interval after the exact navigation
clearances. Tables, code, and intrinsically two-dimensional figures retain only their scoped
exception from Section 4.

The nonshrinking masthead cannot consume the complete compact-layout viewport. In stacked and
enlarged presentation it participates in an exact reachable scroll flow or uses an equivalent
structure that preserves every required masthead item and leaves positive product space. Body or
window scrolling cannot silently replace the exact product-owned navigation scroll owner.

A navigation bar remains readable and operable but cannot reserve the complete target interval. At
a constrained scale it may use a compact, wrapping, progressively disclosed, or non-sticky
presentation only when every state value and control remains reachable and the selected target can
still satisfy the product-owned geometry. Presentation disclosure never changes semantic state.

## 7. Text-spacing adaptation

All four products preserve content and functionality when the following declarations are applied
simultaneously to applicable text, with no other presentation change:

```text
line-height: 1.5
margin after paragraphs: 2em
letter-spacing: 0.12em
word-spacing: 0.16em
```

The vector causes no clipping, overlap, hidden content, inaccessible control, lost focus target,
unreachable scrollbar, semantic-state change, or navigation geometry failure. Intrinsic table,
code, and figure exceptions do not exempt their labels, captions, controls, or surrounding prose.

## 8. Interaction and presentation geometry

Every presentation vector exercises mapped forward activation, candidate and passage movement,
reverse activation and movement, no-candidate state, claim gate where applicable, prior-art full
reader opening, clear, `Esc`, and exact focus return. The action postconditions remain those of the
controlling product contract.

Ordinary motion and reduced motion produce equal semantic state, selected identities, emphasis
sets, reverse occurrences, focus owner, capable scroll owner, and geometric containment. Exact
pixel offsets need not be equal. A zero-height pane, absent target, incapable owner, owner fallback,
off-screen returned focus, target hidden by masthead or navigation chrome, or uncaught geometry
error fails.

## 9. No-JavaScript and print surfaces

With JavaScript removed, every substantive and cautionary item remains in readable document order
at its applicable typography tier. The no-script surface may discard interaction-only layout but
cannot hide, shrink, truncate, or reorder semantic content.

Print contains the complete product-owned inventory required by the two navigator contracts. Fixed
headers or footers, repeated profile wording, disclaimers, legends, tables, code, figures, and page
break controls cannot clip or conceal content. Print rules may adapt measure and page flow but may
not reduce required legal or substantive wording below the applicable tier. Executable print
inspection proves overflow and clipping outcomes; the presence of an `@media print` rule alone is
insufficient.

## 10. Browser control and executable enforcement

The current browser control has one closed presentation section containing:

- the three exact typography tiers and unitless line heights;
- maximum ordinary-text measure `80ch`;
- the baseline viewport and motion matrix;
- text-only resize factor `2`;
- page-zoom factor `2`;
- reflow inline width `320` CSS pixels;
- the four exact text-spacing values in Section 7; and
- the existing product-owned navigation clearance.

Unsupported control shape or version, absent vector, unknown tier, nonpositive value, alternate
default, runtime fallback, skipped product, skipped motion preference, or self-reported result
fails closed. Computed-style and browser assertions inspect representative instances of every role
in every product; a static CSS token alone cannot satisfy acceptance.

The executable vectors additionally reject clipped or overlapping required elements, page-level
ordinary-text overflow, nonpositive usable areas, unreachable scoped overflow, page errors,
network requests, state drift, and incorrect focus or geometry. Browser automation remains pinned
as declared by the current technical-preview profile.

## 11. Worktree validation and implementation closure

This contract pair, its data-only acceptance registry, both navigator product contracts, browser
control, shared renderer, exact implementation and workflow census, registered tests and vectors,
runbook, four candidates, four sealed products and checksums, and delivery bundle form one indivisible current implementation.
No documentation-only, registry-only, control-only,
implementation-only, test-only, workflow-only, or product-only state is accepted.

The acceptance registry owns the ordered criterion IDs, scopes, outcomes, and enforcers. Its
Markdown table is a generated projection and has no independent row ownership. Every shared
presentation change regenerates all four candidates, all four sealed products and checksums, and
the configured bundle.

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

Acceptance fails for an undersized role, normal line-height, absolute or viewport-relative font
size, unbounded ordinary measure, clipped or overlapping text, unintended page overflow,
zero-height product area, masthead or navigation obstruction, lost content or function under
resize, zoom, reflow, spacing, no-script, or print, product-policy leakage, browser fallback,
missing vector, stale generated product, or incomplete deterministic closure.
