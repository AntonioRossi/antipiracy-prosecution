# AA11393US — Claim/Prior-Art Passage-Map Acceptance Criteria

> **OPERATIVE INTERNAL CONTROL · NOT FOR FILING**

Acceptance is conjunctive. Machine pass status proves only the current technical outcomes below;
it does not approve a passage association or establish a substantive or legal conclusion. The sole
execution boundary is the shared [aggregate validation
boundary](../../README.md#aggregate-validation-boundary).

<!-- PA-MAP-AC-TABLE:START -->
| ID | Scope | Executable technical outcome | Independent enforcer |
|---|---|---|---|
| **PAM-AC-01** | semantic | Each strategy passage map is the sole semantic owner of normalized matrix obligations and exact passage candidates; unit-level state assertions, copied matrix prose, inferred mappings, aliases, and relation-to-relation endpoints fail. | navigator.lib.priorart.PriorArtModel; navigator.tests.test_prior_art |
| **PAM-AC-02** | semantic | The current comparison matrix deterministically yields one exact obligation for every applicable matrix relation, field, claim, and prior-art document, including each member of a multi-document relationship and each claim named in a dependent-claim range. | navigator.lib.priorart._matrix_obligations; navigator.tests.test_prior_art |
| **PAM-AC-03** | semantic | Every computed matrix obligation has exactly one authored current state: passage-mapped, counsel-review-required, or reviewed-no-material-passage; the no-material state is permitted only for an exact matrix dash field. | navigator.lib.priorart.PriorArtModel; navigator.tests.test_prior_art |
| **PAM-AC-04** | semantic | Every candidate names exact obligation identities for the same claim and the exact set of evidence documents, and each digest-bound evidence endpoint resolves to a non-root passage in the declared XML transcription surface. | navigator.lib.priorart.PriorArtModel; navigator.tests.test_prior_art |
| **PAM-AC-05** | semantic | Passage-mapped obligations close bidirectionally against at least one candidate, while counsel-review-required and reviewed-no-material-passage obligations have no candidate that claims to satisfy them. | navigator.lib.priorart.PriorArtModel; navigator.tests.test_prior_art |
| **PAM-AC-06** | semantic | Dependent claims and multi-document relationships remain independently addressable: parent ancestry does not create a child mapping, and one mapped document cannot satisfy another document in a recorded combination. | navigator.lib.priorart.PriorArtModel; navigator.tests.test_prior_art |
| **PAM-AC-07** | semantic | Each prior-art consumer receives the claim XML, both relation XML owners, and every transcription XML package in the matrix scope; scope additions become operative through the declared XML handoff with no document allowlist or compatibility branch. | navigator.lib.registry.Registry.prior_art_packages; navigator.tests.test_prior_art |
| **PAM-AC-08** | semantic | The semantic contract pair, data registry, exclusive profile, current relation XML, generated Markdown, model enforcement, tests, handoffs, and products form one retained state; missing, weaker, duplicate, alternate, stale, or orphaned semantics fail. | navigator.lib.validate.validate_prior_art; navigator.tests.test_prior_art |
<!-- PA-MAP-AC-TABLE:END -->
