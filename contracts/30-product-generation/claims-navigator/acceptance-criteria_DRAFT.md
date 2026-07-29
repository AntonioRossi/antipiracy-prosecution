# AA11393US — Interactive Claims-to-Specification Navigator: Acceptance Criteria (DRAFT)

> **INTERNAL COUNSEL-REVIEW MATERIAL — NOT FOR FILING.**

This document is the succinct acceptance half of the navigator documentation pair. The
[`technical description`](technical-description_DRAFT.md) defines the
system; this document defines the outcomes that the current implementation must enforce. The
machine-readable counterpart is
[`navigator/schema/acceptance.json`](../../../navigator/schema/acceptance.json).

The `_DRAFT` suffix records internal counsel-review status; every technical criterion below is
operative for the current implementation.

All twenty criteria are mandatory. An `edition` criterion passes independently for every edition
in the current bundle inventory; a `shared` criterion passes once for the common implementation;
the `bundle` criterion passes for the one current delivery bundle. Missing, skipped, unknown, stale, ambiguous, or
partially satisfied criteria fail the aggregate gate. The machine-readable counterpart contains
the ordered IDs, scopes, executable outcomes, and independent enforcers. No criterion passes from
self-report, stored results, detached tokens, or a prior run.

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

<!-- NAV-AC-TABLE:START -->
| ID | Scope | Executable technical outcome | Independent enforcer |
|---|---|---|---|
| **AC-01** | edition | All structured-source domains validate exactly once per product process, and every configured product receives only its declared immutable handoffs from that same retained-byte context. | navigator.lib.currentstate.validate_structured_corpus; navigator.tests.test_current_pipeline.CurrentPipelineTests.test_one_source_pass_returns_same_context_frozen_handoffs |
| **AC-02** | edition | The exact XML-derived claim and PCT surfaces validate before one immutable edition model preserves their identities, hierarchy, order, content, provenance, assets, and typed digests. | navigator.lib.model.EditionModel; navigator.tests.test_xml_model.XMLModelTests.test_live_editions_have_exact_claim_and_mapping_census |
| **AC-03** | edition | Navigator-owned relation XML resolves only exact non-root, non-editorial current endpoints and rejects stale or wrong-document digests, repeats across candidates, overlapping phrases, upstream references, inference, duplicate semantics, reversal, and retargeting before writes. | navigator.lib.model.RelationSet; navigator.tests.test_xml_model.XMLModelTests.test_stale_relation_digest_fails_during_construction |
| **AC-04** | edition | Controlled semantic wording resolves only from current shared and edition-owned wording XML with exact contexts, typed slots, and computed origins. | navigator.lib.model.EditionModel.controlled_text; navigator.tests.test_xml_model.XMLModelTests.test_controlled_wording_has_exact_slots |
| **AC-05** | edition | Each specification product consumes exactly its two dependency-free retained XML handoffs plus declared navigator XML controls; every authored-relation input, reopen, undeclared read, fallback, or semantic-authority write in that product fails. | navigator.lib.gateway.ContentGateway; navigator.tests.test_xml_model.XMLModelTests.test_authored_handoff_uses_handed_xml_and_retained_controls_only |
| **AC-06** | edition | An explicit specification-product control, exactly two retained XML handoffs, and immutable controls produce one secure-parsed immutable model. Every document, item, wording, and relation lookup supplies exact nonempty IDs; only a resolved item may have no relations. Inherited Markdown/PDF validation reads grant no access, and reconversion, implicit validation, defaults, or unresolved-as-empty results fail. | navigator.lib.currentstate.build_model; navigator.tests.test_xml_model.XMLModelTests.test_model_lookups_require_explicit_nonempty_identities |
| **AC-07** | edition | The current bundle inventory exclusively determines the products, consumers, versions, dependencies, strategy prefixes, artifact names, ordering, and isolation enforced by every aggregate path. | navigator.lib.currentstate.load_product_plan; navigator.tests.test_current_pipeline.CurrentPipelineTests.test_product_plan_is_derived_from_an_arbitrary_edition_inventory |
| **AC-08** | edition | Every selectable fragment has exactly one mapped or counsel-review-required state with complete candidate, phrase, caution, gate, and disposition data; mapped specification fragments expose every recorded candidate and endpoint without truncation, cap, collapse, or selection gate. | navigator.lib.validate.validate_edition; navigator.tests.test_render_current.CurrentRenderTests.test_composites_are_one_candidate_and_reverse_index_every_endpoint |
| **AC-09** | edition | Every dynamic value is context-escaped and hostile markup, script, URL, style, handler, and raw-template inputs remain inert. | navigator.lib.render.render; navigator.tests.test_render_current.CurrentRenderTests.test_hostile_typed_values_are_inert_and_composite_data_is_exact |
| **AC-10** | edition | Mapped activation selects candidate 0 and passage 0 and partitions every endpoint into the selected passage, remaining selected-candidate passages, and all alternate-candidate passages; movement recomputes that complete partition, while reverse, no-candidate, gate, and clear preserve exact state, focus, owner, and geometry. | navigator.lib.render.render; navigator.tests.test_render_current.CurrentRenderTests.test_pinned_browser_matrix_proves_specification_runtime |
| **AC-11** | edition | Semantic non-nested controls support Enter, Space, scoped arrows, Escape, exact focus return, and live announcements; solid, double, and dashed non-color states distinguish selected, selected-candidate, and alternate-candidate passages with ordinary/reduced-motion equality. | navigator.lib.render.render; navigator.tests.test_render_current.CurrentRenderTests.test_pinned_browser_matrix_proves_specification_runtime |
| **AC-12** | edition | Each artifact contains claims, disclosure, legends including the visible three-state highlight key, provenance, complete schedule, and print overflow safeguards; no release-profile or disclaimer block appears on any surface. | navigator.lib.render.render; navigator.tests.test_render_current.CurrentRenderTests.test_live_products_are_complete_self_contained_and_accessible |
| **AC-13** | edition | Both specification products pass the pinned browser at all four boundary sizes and both motion preferences; exact side-by-side or stacked owners apply without fallback, fitting targets retain 10 px top/bottom clearance, and oversized targets retain 10 px leading clearance with their remainder traversable in that owner. | navigator.lib.browserqa.browser_runtime; navigator.tests.test_render_current.CurrentRenderTests.test_pinned_browser_matrix_proves_specification_runtime |
| **AC-14** | edition | All substantive and cautionary content exists outside scripts in readable document order. | navigator.lib.render.render; navigator.tests.test_render_current.CurrentRenderTests.test_live_products_are_complete_self_contained_and_accessible |
| **AC-15** | edition | Exact CSP, self-contained local-file operation, forbidden-capability rules, and secure XML parsing pass without network, cookie, storage, or telemetry capability. | navigator.lib.gateway.ContentGateway; navigator.tests.test_render_current.CurrentRenderTests.test_hostile_typed_values_are_inert_and_composite_data_is_exact |
| **AC-16** | edition | Exactly one fresh isolated worker per invoking product process reproduces the requested complete product set, whose canonical digest projection equals the retained-process projection. | navigator.lib.currentstate.fresh_product_projection; navigator.tests.test_xml_model.XMLModelTests.test_candidate_proof_binds_the_complete_fresh_projection |
| **AC-17** | edition | Exact confidentiality legend, provenance, caution, and strategy-neutral wording appear in ordinary, print, and no-script surfaces; no release-profile or disclaimer block appears on any surface. | navigator.lib.render.render; navigator.tests.test_render_current.CurrentRenderTests.test_live_products_are_complete_self_contained_and_accessible |
| **AC-18** | edition | Current-profile NA and AF relation XML and retained claim/PCT handoffs pass the secure parser, immutable model, renderer, and pinned browser while exercising six- and seven-candidate relations, complete concurrent endpoint sets, composite passages, reverse occurrences, phrases, no-candidate states, cautions, gates, and dispositions; adverse inputs fail before writes. | navigator.lib.currentstate.verify_current_closure; navigator.tests.test_render_current.CurrentRenderTests.test_current_profile_specification_vectors_reach_renderer |
| **AC-19** | shared | All three phase-30 contract pairs and acceptance registries, the browser policy and locked runtime, the exact implementation/workflow/control/test/vector census, declared XML inputs, and all stored products express one current state; split, partial, stale, additional, alternate, detached, or recapture-different states fail the Git-independent aggregate gate. | navigator.lib.currentstate.validate_current_state; navigator.tests.test_current_pipeline.CurrentPipelineTests.test_live_navigator_input_inventory_is_exact |
| **AC-20** | bundle | The deterministic STORE ZIP and detached checksum contain four ordered HTML/checksum product pairs followed by the exact neutral manifest, with no product-kind-specific bundle branch. | navigator.lib.bundlezip.build_zip; navigator.tests.test_current_pipeline.CurrentPipelineTests.test_configured_member_bundle_and_checksums_are_deterministic |
<!-- NAV-AC-TABLE:END -->
