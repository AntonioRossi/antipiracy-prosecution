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
| **PA-AC-01** | product | Each strategy product consumes exactly its claim XML, comparison-matrix relation XML, passage-map relation XML, and every passage-target transcription XML through immutable declared handoffs from one retained capture; undeclared reads and relation copies fail. | navigator.lib.registry.Registry.load_relation; navigator.tests.test_prior_art |
| **PA-AC-02** | product | The comparison matrix supplies one exact 33-document strategy scope, while the dedicated passage map supplies exactly one mapped or counsel-review-required state for every typed claim unit; whole-document endpoints never become passage candidates. | navigator.lib.priorart.PriorArtModel; navigator.tests.test_prior_art |
| **PA-AC-03** | product | Every candidate resolves one exact claim unit or uniquely selected phrase, one profiled role and proposition, and one or more digest-bound non-root prior-art passages within matrix scope; stale, missing, ambiguous, contradictory, or inferred mappings fail. | navigator.lib.priorart.PriorArtModel; navigator.tests.test_prior_art |
| **PA-AC-04** | product | Displayed passage text, page, region, uncertainty, identity, and digest derive only from asserted registered transcription XML, while the source PDF remains the stated fidelity authority and no legal disclosure conclusion is emitted. | navigator.lib.validate.validate_prior_art; navigator.tests.test_prior_art |
| **PA-AC-05** | product | One explicit product specification and same-capture handoff set produce one sealed immutable model with exact identities, claim hierarchy, scope, map state, reverse index, controlled wording, provenance, origins, and content lock. | navigator.lib.currentstate.build_model; navigator.tests.test_prior_art |
| **PA-AC-06** | product | The two-pane HTML presents selectable claim units and phrases, document-grouped passage cards, deterministic forward/reverse interaction, clear recording state, and one complete schedule from the same immutable relations. | navigator.lib.render.render; navigator.tests.test_prior_art |
| **PA-AC-07** | product | Claims, states, candidates, passages, uncertainty, disclaimers, and provenance remain readable outside scripts in ordinary, no-script, print, keyboard, reduced-motion, minimum-size, and stacked-layout surfaces. | navigator.lib.render.render; navigator.tests.test_prior_art |
| **PA-AC-08** | product | Exact CSP, contextual escaping, inert embedded data, secure XML parsing, and forbidden-capability checks keep hostile source text inert and prohibit network, storage, cookie, telemetry, and external-resource behavior. | navigator.lib.render.render; navigator.tests.test_prior_art |
| **PA-AC-09** | shared | The closed plan exposes exactly four full product IDs, two distinct prior-art consumers, strategy-bound inputs and names, no implicit product selection, and no shorter command identity. | navigator.lib.currentstate.load_product_plan; navigator.tests.test_prior_art |
| **PA-AC-10** | product | Candidate and sealed bytes reproduce exactly in one fresh isolated process; release requires the exact stored candidate and publishes only the declared HTML/checksum pair with exact readback. | navigator.lib.currentstate.fresh_product_projection; navigator.tests.test_prior_art |
| **PA-AC-11** | bundle | The deterministic delivery ZIP contains four ordered HTML/checksum pairs followed by the neutral manifest, with fixed metadata, exact member bytes, and one detached bundle checksum. | navigator.lib.bundlezip.build_zip; navigator.tests.test_prior_art |
| **PA-AC-12** | shared | The dedicated contract pair, data registry, XML profile and maps, handoffs, model, shared renderer, tests, generated views, four HTML products, checksums, bundle, and live-path census form one retained current state; missing, extra, stale, duplicate, alternate, partial, or orphaned state fails. | navigator.lib.currentstate.validate_current_state; navigator.tests.test_prior_art |
<!-- PA-NAV-AC-TABLE:END -->

