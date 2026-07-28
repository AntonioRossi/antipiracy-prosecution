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
| **PA-AC-01** | product | Each strategy product consumes exactly its claim XML, comparison-matrix relation XML, current passage-map relation XML, and all matrix-scope transcription XML packages through immutable declared handoffs from one retained capture; undeclared reads and relation copies fail. | navigator.lib.registry.Registry.load_relation; navigator.tests.test_prior_art |
| **PA-AC-02** | product | The matrix supplies the obligation census and the passage map supplies current obligation state, allocations, candidates, and ordered passages; no authored unit-status plane, computed unit-target copy, primary-member alias, or cached selection field exists. | navigator.lib.priorart.PriorArtModel; navigator.tests.test_prior_art |
| **PA-AC-03** | product | Every exact fragment or unique phrase supports zero, one, or many candidates with exact obligations, role, proposition, and ordered XML passages; duplicates canonicalized over evidence identity, endpoint permutations, and synthetic preamble roll-ups fail. | navigator.lib.priorart.PriorArtModel; navigator.tests.test_prior_art |
| **PA-AC-04** | product | Every displayed passage card and complete contextual reader derives only from declared asserted transcription XML, preserving exact fragment identity, page, region, uncertainty, digest, and source-PDF fidelity authority. | navigator.lib.validate.validate_prior_art; navigator.tests.test_prior_art |
| **PA-AC-05** | product | One product specification and one same-capture handoff set produce a sealed immutable model with exact obligations by claim, candidates and allocations by fragment, ordered passages, full reader trees, exact reverse occurrences, controlled wording, provenance, origins, and content lock. | navigator.lib.currentstate.build_model; navigator.tests.test_prior_art |
| **PA-AC-06** | product | A selected fragment presents separate candidate, allocation, candidate-position, passage-position, and claim-obligation counts; obligation statuses sum to the exact claim census and no count substitutes for another domain. | navigator.lib.render.render; navigator.tests.test_prior_art |
| **PA-AC-07** | product | Fragment activation selects candidate zero and passage zero; candidate movement wraps and resets passage zero, while passage movement wraps within the candidate without changing candidate identity or semantics. | navigator.lib.render.render; navigator.tests.test_prior_art |
| **PA-AC-08** | product | After every activation or movement, the navigation bar has focus, the selected passage anchor is visible in the unobscured right-pane viewport, only it is strongly emphasized, related candidate passages are secondary, and ordinary and reduced-motion outcomes are equal. | navigator.lib.render.render; navigator.tests.test_prior_art |
| **PA-AC-09** | product | The reader opens the complete asserted XML transcription with the selected passage focused and visible; reverse navigation preserves every exact relation, candidate occurrence, claim fragment, and selected passage without collapsing shared references. | navigator.lib.render.render; navigator.tests.test_prior_art |
| **PA-AC-10** | product | Claims, obligations, allocations, candidate identities and propositions, passages, complete transcription context, uncertainty, disclaimers, and provenance remain readable in ordinary, no-script, print, keyboard, reduced-motion, minimum-size, and stacked-layout surfaces. | navigator.lib.render.render; navigator.tests.test_prior_art |
| **PA-AC-11** | product | Exact CSP, contextual escaping, inert embedded data, secure XML parsing, and forbidden-capability checks keep hostile source text inert and prohibit network, storage, cookie, telemetry, history, location, and external-resource behavior. | navigator.lib.render.render; navigator.tests.test_prior_art |
| **PA-AC-12** | product | Unsupported profiles or shapes, stale or root targets, wrong-document closure, inferred mappings, endpoint-permuted duplicates, synthetic ancestry mappings, and parallel selection state fail before writes with no compatibility path. | navigator.lib.validate.validate_prior_art; navigator.tests.test_prior_art |
| **PA-AC-13** | shared | The closed plan exposes exactly four full product IDs, two distinct prior-art consumers, strategy-bound inputs and names, no implicit product selection, and no shorter command identity. | navigator.lib.currentstate.load_product_plan; navigator.tests.test_prior_art |
| **PA-AC-14** | product | Candidate and sealed bytes reproduce exactly in one fresh isolated process; release requires the exact stored candidate and publishes only the declared HTML/checksum pair with exact readback. | navigator.lib.currentstate.fresh_product_projection; navigator.tests.test_prior_art |
| **PA-AC-15** | bundle | The deterministic delivery ZIP contains four ordered HTML/checksum pairs followed by the neutral manifest, with fixed metadata, exact member bytes, and one detached bundle checksum. | navigator.lib.bundlezip.build_zip; navigator.tests.test_prior_art |
| **PA-AC-16** | product | Current-profile rendered positive and adverse vectors enforce two candidates for one fragment, multi-passage and shared-passage behavior, an exact allocation, unresolved state, canonical duplicate and preamble rejection, independent movement, visible scrolling, reverse occurrences, and exact reader focus. | navigator.lib.priorart.PriorArtModel; navigator.tests.test_prior_art |
| **PA-AC-17** | shared | The phase-20 and phase-30 contract pairs, registries, exclusive profile and maps, handoffs, one model and renderer path, tests and vectors, generated views, products, checksums, bundle, and live-path census form one hard current state; missing, extra, stale, duplicated, alternate, partial, compatibility, or orphaned state fails. | navigator.lib.currentstate.validate_current_state; navigator.tests.test_prior_art |
<!-- PA-NAV-AC-TABLE:END -->
