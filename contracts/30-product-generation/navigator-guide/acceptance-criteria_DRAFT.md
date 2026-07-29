# AA11393US — HTML5 Navigator Guide: Acceptance Criteria (DRAFT)

> **OPERATIVE GUIDE CONTRACT · INTERNAL REVIEW DRAFT · NOT FOR FILING**

This document is the succinct acceptance half of the shared navigator-guide contract. The
[`technical description`](technical-description_DRAFT.md) defines the required system behavior;
the data-only counterpart
[`navigator/schema/guide-acceptance.json`](../../../navigator/schema/guide-acceptance.json)
owns the ordered criteria projected below.

All ten criteria are mandatory. A `product` criterion passes independently for every configured
product; a `shared` criterion passes once for the common guide implementation and complete
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

<!-- GUIDE-AC-TABLE:START -->
| ID | Scope | Executable technical outcome | Independent enforcer |
|---|---|---|---|
| **GUIDE-AC-01** | shared | One shared guide mechanism and its wording slots apply to all four products without changing semantic content, candidate semantics, emphasis policy, or authority direction. | navigator.lib.render.render_guide; navigator.tests.test_guide.GuideTests.test_shared_mechanism_is_product_isolated |
| **GUIDE-AC-02** | product | With JavaScript enabled, the overlay opens on load and presents the product-kind-correct profile: Profile S for specification products, Profile P for prior-art products. | navigator.lib.browserqa.browser_runtime; navigator.tests.test_guide.GuideTests.test_auto_open_presents_product_kind_profile |
| **GUIDE-AC-03** | product | The persistent masthead Guide control reopens the overlay after dismissal; focus is contained while open and returns to the invoking control on close. | navigator.lib.browserqa.browser_runtime; navigator.tests.test_guide.GuideTests.test_reopen_control_and_focus_cycle |
| **GUIDE-AC-04** | product | Escape, backdrop activation, and the explicit close control each dismiss the overlay without semantic-state, emphasis, navigation, or scroll-owner change. | navigator.lib.browserqa.browser_runtime; navigator.tests.test_guide.GuideTests.test_dismissal_routes_preserve_state |
| **GUIDE-AC-05** | product | With JavaScript removed, no overlay appears and the guide content remains readable in document order through the in-document carrier at the applicable typography tiers. | navigator.lib.presentationqa.validate_noninteractive_surfaces; navigator.tests.test_guide.GuideTests.test_no_script_guide_is_readable_in_document_order |
| **GUIDE-AC-06** | product | Print output contains no overlay and no guide content, while the counsel-review legend continues to print and no release-profile or disclaimer block appears. | navigator.lib.presentationqa.validate_noninteractive_surfaces; navigator.tests.test_guide.GuideTests.test_print_excludes_guide_furniture |
| **GUIDE-AC-07** | product | Overlay and carrier content respect the controlled measure and survive 200% text resize, 200% page zoom, the 320 CSS-pixel reflow, and the text-spacing override without clipping, overlap, or page-level horizontal scrolling; reduced motion disables entry animation. | navigator.lib.browserqa.browser_runtime; navigator.tests.test_guide.GuideTests.test_guide_surfaces_survive_enlargement_and_reflow |
| **GUIDE-AC-08** | shared | Every guide string resolves from a consumed, typed, exactly-sourced wording slot; no hardcoded, unused, or unresolved slot exists. | navigator.lib.validate.validate_product; navigator.tests.test_guide.GuideTests.test_guide_wording_slots_close |
| **GUIDE-AC-09** | shared | The guide is stateless: no storage is read or written, the overlay opens on every load, and candidate and sealed reproduction remain byte-stable. | navigator.lib.currentstate.validate_current_state; navigator.tests.test_guide.GuideTests.test_guide_is_stateless_and_byte_stable |
| **GUIDE-AC-10** | shared | The contract pair, registry, browser control, renderer, wording, exact verifier census, runbook, four candidates, four sealed products, checksums, bundle, and governed path census form one deterministic retained current state. | navigator.lib.currentstate.validate_current_state; navigator.tests.test_current_pipeline.CurrentPipelineTests.test_live_navigator_input_inventory_is_exact |
<!-- GUIDE-AC-TABLE:END -->
