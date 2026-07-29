# AA11393US — Claims-to-Prior-Art Navigator Acceptance Criteria

> **OPERATIVE INTERNAL CONTROL · NOT FOR FILING**

Acceptance is conjunctive. Machine pass status proves only the executable technical outcomes below;
it does not approve a passage association or establish any legal conclusion.

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

<!-- PA-NAV-AC-TABLE:START -->
| ID | Scope | Executable technical outcome | Independent enforcer |
|---|---|---|---|
| **PA-AC-01** | product | Each prior-art product consumes only its same-capture claim, matrix, current map, and complete matrix-scope transcription XML handoffs; undeclared reads and semantic copies fail. | navigator.lib.registry.Registry.load_relation; navigator.tests.test_prior_art.PriorArtNavigatorTests.test_exact_product_and_handoff_inventory |
| **PA-AC-02** | product | The matrix exclusively supplies obligations and the map exclusively supplies states, allocations, candidates, and ordered passages; copied status, target, primary-member, or selection planes are absent. | navigator.lib.priorart.PriorArtModel; navigator.tests.test_prior_art.PriorArtNavigatorTests.test_matrix_scope_obligations_and_candidates_are_exact |
| **PA-AC-03** | product | Exact fragments and phrases support zero, one, or many candidates; stale endpoints, duplicate or permuted semantics, inferred children, and synthetic preamble roll-ups fail. | navigator.lib.priorart.PriorArtModel; navigator.tests.test_prior_art.PriorArtNavigatorTests.test_matrix_scope_obligations_and_candidates_are_exact |
| **PA-AC-04** | product | Every passage and full reader resolves only from declared asserted transcription XML with exact fragment, digest, provenance, uncertainty, and PDF-fidelity authority. | navigator.lib.validate.validate_prior_art; navigator.tests.test_prior_art.PriorArtNavigatorTests.test_matrix_scope_obligations_and_candidates_are_exact |
| **PA-AC-05** | product | One product control and same-capture handoff set produce one sealed immutable model with exact forward and reverse indexes, controlled wording, origins, and read lock. | navigator.lib.currentstate.build_model; navigator.tests.test_prior_art.PriorArtNavigatorTests.test_exact_product_and_handoff_inventory |
| **PA-AC-06** | product | Candidate, allocation, candidate-position, passage-position, and claim-obligation counts remain separate and obligation totals close exactly. | navigator.lib.render.render; navigator.tests.test_prior_art.PriorArtNavigatorTests.test_static_html_has_exact_forward_and_reverse_passage_navigation |
| **PA-AC-07** | product | Activation selects candidate 0/passage 0; candidate movement wraps and resets passage 0; passage movement wraps without changing candidate identity or semantics. | navigator.lib.render.render; navigator.tests.test_prior_art.PriorArtNavigatorTests.test_pinned_browser_matrix_proves_runtime_layout_and_navigation |
| **PA-AC-08** | product | Each action leaves exact state and focus, one strong passage, related passages only from the selected candidate, no specification alternate-candidate state, the exact capable owner, and unobscured geometry; reduced motion is semantically identical. | navigator.lib.browserqa.browser_runtime; navigator.tests.test_prior_art.PriorArtNavigatorTests.test_pinned_browser_matrix_proves_runtime_layout_and_navigation |
| **PA-AC-09** | product | Reader opening focuses the exact asserted-XML fragment; reverse navigation preserves and cycles every exact relation/candidate/fragment/passage occurrence without collapsing shared passages. | navigator.lib.render.render; navigator.tests.test_prior_art.PriorArtNavigatorTests.test_pinned_browser_matrix_proves_runtime_layout_and_navigation |
| **PA-AC-10** | product | Both products pass ordinary and reduced-motion execution at 1280×720, 1279×720, 1280×719, and 1000×700; side-by-side owners apply only at width ≥1280 and height ≥720, otherwise #panes owns both axes. | navigator.lib.browserqa.browser_runtime; navigator.tests.test_prior_art.PriorArtNavigatorTests.test_pinned_browser_matrix_proves_runtime_layout_and_navigation |
| **PA-AC-11** | product | CSP, escaping, inert data, secure XML, and forbidden-capability checks keep hostile text inert and prohibit network, storage, cookie, telemetry, history, location, and external resources. | navigator.lib.render.render; navigator.tests.test_prior_art.PriorArtNavigatorTests.test_static_html_has_exact_forward_and_reverse_passage_navigation |
| **PA-AC-12** | product | Unsupported profile/shape, stale or root passage, wrong-document closure, endpoint permutation, duplicate allocation, preamble roll-up, inferred child, and parallel selection state fail before writes. | navigator.lib.priorart.PriorArtModel; navigator.tests.test_prior_art.PriorArtNavigatorTests.test_current_profile_adverse_vectors_fail_before_render |
| **PA-AC-13** | shared | The closed plan exposes exactly four full product IDs and two strategy-bound prior-art consumers, with no implicit or shortened identity. | navigator.lib.currentstate.load_product_plan; navigator.tests.test_prior_art.PriorArtNavigatorTests.test_exact_product_and_handoff_inventory |
| **PA-AC-14** | product | Fresh reproduction must equal the exact stored candidate before atomic publication of only the declared HTML/checksum pair. | navigator.lib.currentstate.fresh_product_projection; navigator.tests.test_current_pipeline.CurrentPipelineTests.test_generated_writes_are_atomic_generated_only_and_safe |
| **PA-AC-15** | bundle | The deterministic bundle contains four ordered HTML/checksum pairs, the neutral manifest, fixed metadata, exact bytes, and one detached checksum. | navigator.lib.bundlezip.build_zip; navigator.tests.test_current_pipeline.CurrentPipelineTests.test_configured_member_bundle_and_checksums_are_deterministic |
| **PA-AC-16** | product | A current-profile XML vector passes the secure parser, retained handoff, immutable model, renderer, and pinned browser with two same-fragment candidates, multiple and shared passages, one exact allocation, and one unresolved fragment. | navigator.lib.browserqa.browser_runtime; navigator.tests.test_prior_art.PriorArtNavigatorTests.test_pinned_browser_vector_proves_independent_candidate_movement |
| **PA-AC-17** | shared | The contract pair, registry, browser control, locked runtime, maps, handoffs, implementation, exact verifiers, vectors, generated views, four products, checksums, bundle, and path census form one retained current state. | navigator.lib.currentstate.validate_current_state; navigator.tests.test_current_pipeline.CurrentPipelineTests.test_live_navigator_input_inventory_is_exact |
<!-- PA-NAV-AC-TABLE:END -->
