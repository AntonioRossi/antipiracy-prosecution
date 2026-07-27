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
| **AC-01** | edition | All structured-source domains validate exactly once per product process, and every configured edition receives only its declared immutable handoffs from that same retained-byte context. | navigator.lib.currentstate.validate_structured_corpus; navigator.tests.test_current_pipeline |
| **AC-02** | edition | The exact XML-derived claim and PCT surfaces validate before one immutable edition model preserves their identities, hierarchy, order, content, provenance, assets, and typed digests. | navigator.lib.model.EditionModel; navigator.tests.test_xml_model |
| **AC-03** | edition | Navigator-owned edition relation XML resolves exact current endpoints and rejects upstream-relation references, copied ownership, duplicates, stale digests, inference, ambiguity, reversal, and retargeting. | navigator.lib.model.RelationSet; navigator.tests.test_xml_model |
| **AC-04** | edition | Controlled semantic wording resolves only from current shared and edition-owned wording XML with exact contexts, typed slots, and computed origins. | navigator.lib.model.EditionModel.controlled_text; navigator.tests.test_xml_model |
| **AC-05** | edition | Each edition consumes exactly its two dependency-free retained XML handoffs plus declared navigator XML controls; every upstream-relation input, reopen, undeclared read, fallback, or semantic-authority write fails. | navigator.lib.gateway.ContentGateway; navigator.tests.test_current_pipeline |
| **AC-06** | edition | An explicit edition specification, exactly two retained XML handoffs, and immutable controls produce one secure-parsed immutable model. Every document, item, wording, and relation lookup supplies exact nonempty IDs; only a resolved item may have no relations. Inherited Markdown/PDF validation reads grant no access, and reconversion, implicit validation, defaults, or unresolved-as-empty results fail. | navigator.lib.currentstate.build_model; navigator.tests.test_xml_model |
| **AC-07** | edition | The current bundle inventory exclusively determines the editions, consumers, versions, dependencies, strategy prefixes, artifact names, ordering, and isolation enforced by every aggregate path. | navigator.lib.currentstate.load_product_plan; navigator.tests.test_render_current |
| **AC-08** | edition | Every selectable fragment has exactly one mapped or counsel-review-required state with complete candidate, caution, gate, disposition, and phrase behavior. | navigator.lib.validate.validate_edition; navigator.tests.test_render_current |
| **AC-09** | edition | Every dynamic value is context-escaped and hostile markup, script, URL, style, handler, and raw-template inputs remain inert. | navigator.lib.render.render; navigator.tests.test_render_current |
| **AC-10** | edition | Forward and reverse interactions, target order, cycling, highlight bounds, clearing, focus return, and printable schedule derive from one relation set. | navigator.lib.render.render; navigator.tests.test_render_current |
| **AC-11** | edition | Static HTML exposes semantic non-nested controls, logical order, scoped keyboard instructions, accessible state, a live region, non-color indicators, and reduced-motion rules. | navigator.lib.render.render; navigator.tests.test_render_current |
| **AC-12** | edition | Each artifact contains claims, disclosure, label, disclaimer, legend, provenance, complete schedule, and print overflow safeguards. | navigator.lib.render.render; navigator.tests.test_render_current |
| **AC-13** | edition | Each artifact contains the exact two-pane, independent-scroll, fixed-scroll-owner, minimum-size, and below-minimum stacking rules. | navigator.lib.render.render; navigator.tests.test_render_current |
| **AC-14** | edition | All substantive and cautionary content exists outside scripts in readable document order. | navigator.lib.render.render; navigator.tests.test_render_current |
| **AC-15** | edition | Exact CSP, self-contained local-file operation, forbidden-capability rules, and secure XML parsing pass without network, cookie, storage, or telemetry capability. | navigator.lib.gateway.ContentGateway; navigator.tests.test_canon |
| **AC-16** | edition | Exactly one fresh isolated worker per invoking product process reproduces the requested complete product set, whose canonical digest projection equals the retained-process projection. | navigator.lib.currentstate.fresh_product_projection; navigator.tests.test_current_pipeline |
| **AC-17** | edition | Exact product label, disclaimer, confidentiality legend, provenance, caution, and strategy-neutral wording appear in ordinary, print, and no-script surfaces. | navigator.lib.render.render; navigator.tests.test_render_current |
| **AC-18** | edition | One configuration-resolved plan and same-snapshot XML source boundary own every immutable edition model, content lock, computed coverage and origin projection, candidate proof, fresh-worker projection, and bundle derivation. No object or proof crosses a capture or output-state boundary, even when bytes match. | navigator.lib.currentstate.verify_current_closure; navigator.tests.test_current_pipeline |
| **AC-19** | shared | The product contract pair, acceptance registry, exact capture-wide implementation/workflow/control/test/vector census, declared XML inputs, and stored products express one current state. Each command prevalidates one closed output map, writes only declared generated paths, and exact-reads the complete set; split, partial, stale, additional, alternate, or detached states fail before the sole Git-independent aggregate gate accepts unchanged recapture. | navigator.lib.currentstate.validate_current_state; navigator.tests.test_current_pipeline |
| **AC-20** | bundle | The deterministic STORE ZIP and detached checksum contain one ordered HTML and checksum pair for every configured edition followed by the exact neutral manifest, with no edition-specific bundle branch. | navigator.lib.bundlezip.build_zip; navigator.tests.test_current_pipeline |
<!-- NAV-AC-TABLE:END -->
