# AA11393US — HTML5 Navigator Presentation and Readability: Acceptance Criteria (DRAFT)

> **OPERATIVE PRESENTATION CONTRACT · INTERNAL REVIEW DRAFT · NOT FOR FILING**

This document is the succinct acceptance half of the shared navigator-presentation contract. The
[`technical description`](technical-description_DRAFT.md) defines the required system behavior;
the data-only counterpart
[`navigator/schema/presentation-acceptance.json`](../../../navigator/schema/presentation-acceptance.json)
owns the ordered criteria projected below.

All ten criteria are mandatory. A `product` criterion passes independently for every configured
product; a `shared` criterion passes once for the common presentation implementation and complete
current-state closure. Missing, skipped, unknown, stale, ambiguous, or partially satisfied criteria
fail. No criterion passes from self-report, stored results, detached tokens, or a prior run.

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

<!-- PRES-AC-TABLE:START -->
| ID | Scope | Executable technical outcome | Independent enforcer |
|---|---|---|---|
| **PRES-AC-01** | shared | One shared presentation contract, browser control, and renderer apply to all four products without changing semantic content, product-specific navigation policy, or authority direction. | navigator.lib.render.render; navigator.tests.test_presentation.PresentationTests.test_shared_contract_is_product_isolated |
| **PRES-AC-02** | product | At 100% zoom every rendered text role meets its exact rem/em-based minimum size and unitless line-height; browser font preferences remain effective and no responsive rule reduces either value. | navigator.lib.presentationqa.validate_computed_typography; navigator.tests.test_presentation.PresentationTests.test_all_products_meet_exact_typography_tiers |
| **PRES-AC-03** | product | Ordinary text stays within the exact readable measure and wraps without clipping or page-level horizontal scrolling; only declared tables, code, and intrinsically two-dimensional figures own scoped overflow. | navigator.lib.presentationqa.validate_reading_surfaces; navigator.tests.test_presentation.PresentationTests.test_readable_measure_wrapping_and_scoped_overflow |
| **PRES-AC-04** | product | Every product passes computed-style, clipping, overlap, positive-usable-area, and readable-measure checks at 100% zoom across the controlled viewport and motion matrix. | navigator.lib.browserqa.browser_runtime; navigator.tests.test_presentation.PresentationTests.test_baseline_viewport_matrix_is_readable |
| **PRES-AC-05** | product | Text-only resize and page zoom to 200% preserve all content, controls, state, focus, navigation, scroll-owner identity, and target geometry without a page error. | navigator.lib.browserqa.browser_runtime; navigator.tests.test_presentation.PresentationTests.test_text_resize_and_page_zoom_preserve_functionality |
| **PRES-AC-06** | product | At a 320 CSS-pixel reflow width, ordinary content requires no two-dimensional page scrolling, every required surface remains reachable, and the active application retains a positive usable target interval. | navigator.lib.browserqa.browser_runtime; navigator.tests.test_presentation.PresentationTests.test_reflow_preserves_content_and_positive_geometry |
| **PRES-AC-07** | product | The exact line-height, paragraph, letter, and word-spacing override causes no clipped, overlapped, hidden, or inoperable content, control, state, or focus target. | navigator.lib.presentationqa.validate_text_spacing_adaptation; navigator.tests.test_presentation.PresentationTests.test_text_spacing_override_preserves_content_and_controls |
| **PRES-AC-08** | product | Forward, reverse, reader, claim-gate, clear, and focus-return actions retain exact semantic state, emphasis, capable owner, and unobscured geometry at every controlled scale and motion preference. | navigator.lib.browserqa.browser_runtime; navigator.tests.test_presentation.PresentationTests.test_scaled_navigation_preserves_state_focus_owner_and_geometry |
| **PRES-AC-09** | product | No-JavaScript and print surfaces preserve every required substantive and cautionary item at the applicable typography tier without clipping, undersized legal wording, or hidden overflow; the counsel-review legend remains and no release-profile or disclaimer block appears on any surface. | navigator.lib.presentationqa.validate_noninteractive_surfaces; navigator.tests.test_presentation.PresentationTests.test_no_script_and_print_surfaces_are_readable |
| **PRES-AC-10** | shared | The contract pair, registry, browser control, renderer, exact verifier census, runbook, four candidates, four sealed products, checksums, bundle, and governed path census form one deterministic retained current state. | navigator.lib.currentstate.validate_current_state; navigator.tests.test_current_pipeline.CurrentPipelineTests.test_live_navigator_input_inventory_is_exact |
<!-- PRES-AC-TABLE:END -->
