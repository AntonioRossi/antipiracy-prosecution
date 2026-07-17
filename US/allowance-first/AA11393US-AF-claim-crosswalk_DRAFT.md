# AA11393US — AF/NA Claim and Coverage Crosswalk (DRAFT)

> **STRATEGY AF · CLAIM-SET VERSION AF-2026-07-17-v2 · STATUS 17 JULY 2026**
>
> **INTERNAL COUNSEL ANALYSIS — NOT FOR FILING AND NOT A CLAIM-CONSTRUCTION POSITION.** This crosswalk compares functional coverage; it does not state that any AF and NA claim has identical scope. Every external reference is strategy-qualified.
>
> **TERMINOLOGY / FAMILY-RECORD NON-CONCESSION.** `Camera-source-transition pattern` is used in AF because the AF claims positively require ordered source identities and switch timing. It is deliberately not treated here as synonymous with, narrower than, or exhaustive of the NA expression `camera-cut timing pattern`. This drafting choice does not redefine the common disclosure, disclaim other embodiments, or authorize transferring an AF construction or prosecution position to NA or another family member.

## 1. Purpose and controlling texts

This document records what AF-2026-07-17-v2 carries into the integrated allowance-first tree and what it deliberately leaves for the actor-focused NA branch. The exact wording in [`AA11393US-AF-US_claim-set_DRAFT.md`](AA11393US-AF-US_claim-set_DRAFT.md) and [`../normal-allowance/AA11393US-NA-US_claim-set_DRAFT.md`](../normal-allowance/AA11393US-NA-US_claim-set_DRAFT.md) controls.

AF claim 1 is narrower than any isolated NA subsystem claim because it requires production, delivery/association, detection, matching, and recipient lookup in one system. Functional overlap is not interchangeability, and support or art analysis for one strategy must not be transferred to the other without a limitation-by-limitation review.

## 2. Exact AF-to-NA functional crosswalk

| AF claim | AF added limitation | Closest NA coverage | Difference that matters |
|---:|---|---|---|
| AF claim 1 | Complete structured-list-created source-boundary → delivered candidate pattern → same-region source/time match → recipient lookup chain | NA claims 1 and 7 for production structure; NA claim 9 for delivery/association structure; NA claim 16 for detection; NA claim 22 for the end-to-end loop | No NA claim has the exact AF claim 1 system chain. EDL fields first become express in AF claim 4. AF claim 1 drops actor separation and adds a single integrated source-and-time lookup dependency. |
| AF claim 2 | Preserve later reference cut timing and restore synchronization | NA claim 2 and method NA claim 23 | AF claim 2 inherits the full AF claim 1 system; both strategies share the Example 2 gate. |
| AF claim 3 | Ten-frame extension/shortening and later resynchronization | NA claim 3 | AF claim 3 expressly states first-selection extension and following-selection shortening within the integrated system. |
| AF claim 4 | EDL source-camera, in-point, and out-point fields | NA claim 4 | Same production fallback, but AF claim 4 also inherits delivery and detection. |
| AF claim 5 | Live viewpoints and director-commanded switching | NA claim 5 | Same added production concept; AF claim 5 remains an end-to-end system claim. |
| AF claim 6 | Plural varied cuts, regions, and stored source-transition patterns | NA claim 6; plural-region aspects of NA claims 15–16 | AF claim 6 expressly links each varied cut to a candidate region and stored ordered-source/timing pattern. |
| AF claim 7 | Perceptual-hash comparison for transition/timing detection | NA claim 17 and method NA claim 26 | AF claim 7 compares against reference or mate and inherits AF claim 1's source-pair/timing match. |
| AF claim 8 | Sliding-window fuzzy hash matching | NA claim 18 and method NA claim 26 | Same implementation family; AF claim 8 remains dependent through AF claim 7. |
| AF claim 9 | Delivery by respective manifests, manifest-to-candidate-pattern association, derivation of a time code from the detected switch timing, and reconstructed-manifest building | NA claims 9, 19, and 24–25 | AF claim 9 combines delivery, candidate-pattern association, and reconstruction inside AF claim 1; it does not create a standalone platform or monitoring claim. |
| AF claim 10 | Delivered-manifest ledger/account lookup | NA claims 12, 20, and 25 | AF claim 10 requires the AF claim 9 reconstruction path; NA claim 12 is a broader standalone distribution-ledger fallback. |
| AF claim 11 | Mixed-version suspect, probabilistic analysis of recipient-associated candidate camera-source-transition patterns, and positive contributor identification | NA claims 21 and 28 | AF claim 11 omits NA claim 21's attribution-score requirement but expressly uses AF claim 1's newly formulated candidate patterns as the algorithm input; that integration remains support-gated. |
| AF claim 12 | Segmented Tardos fingerprints applied to content segments and identification of a contributor for at least one respective portion | NA claims 21 and 28 | No NA claim has this exact segmented-Tardos/portion relationship. AF claim 12 deliberately does not carry NA claim 21's attribution-score language. |
| AF claim 13 | Chunk/manifest delivery preserving one boundary timing and storing manifest/pattern/recipient association | NA claims 9, 24, and 29 | AF claim 13 supplies a complete manifest subsystem only after inheriting AF claim 1's generation and detection chain. |
| AF claim 14 | Same-interval, equal-duration reference/mate chunks, each straddling its respective transition | NA claim 13 | Substantially corresponding structural fallback; both require the combined-example geometry review. |
| AF claim 15 | CDN adaptive delivery and device/network tailoring | NA claim 10 | Same added implementation class; AF claim 15 inherits AF claim 13 and AF claim 1. |
| AF claim 16 | Reference/mate chunk mixing and progressive assignment | NA claim 11 | Same added implementation class within the integrated AF chain. |
| AF claim 17 | Unicast delivery | NA claim 14 and method NA claim 27 | Same delivery fallback, but no standalone AF delivery claim exists. |
| AF claim 18 | Recipient choices across plural source-transition regions | NA claim 15 | AF claim 18 uses the AF candidate-region vocabulary and inherits joint detection/lookup. |
| AF claim 19 | Additional audio/video overlay before segmentation | NA claims 8 and 30 | AF claim 19 adds a specific pipeline order and depends from AF claim 13; that order has its own support gate. |
| AF claim 20 | Independent performance of the complete AF claim 1 chain, including delivery of generated versions expressly including a reference version and a mate version, defining a candidate-distinguishing region that includes the alternate-camera interval, generating for each delivered version a source-ID/timing pattern actually present at that region, storing the delivered-version/pattern/recipient association, and matching both source order and timing at that region before lookup | NA claim 22 | Both are end-to-end methods and both require the ordered first-to-second-camera transition, noncoincident timings, alternate-camera frames in the interval, source-and-time detection, and recipient lookup. AF claim 20 additionally makes AF claim 1's candidate-region and per-delivered-version pattern-generation/three-way-association chain express; NA claim 22 instead delivers versions selected from the reference and at least the mate, records associations with a version **or** its camera-cut timing pattern, and uses its separately drafted adjacent-region formulation. Neither wording is a construction of the other, and the claims are not interchangeable. |

## 3. Coverage deliberately deferred by AF

Selecting AF for the initial case would not carry the following NA coverage as standalone claims:

| Deferred coverage | NA location | Commercial reason to preserve | AF consequence |
|---|---|---|---|
| Production/mate generation without proof of downstream delivery or detection | NA claims 1–8 | Targets broadcasters, production facilities, and mate-generation vendors | AF claim 1 requires the later association and detection chain. |
| Distribution/recipient association without proof that the same defendant generated or later detected the versions | NA claims 9–15 | Targets streaming platforms, origin services, licensees, and CDN operators | AF claims 13–19 remain tied to AF claim 1's production and recovery operations. |
| Detection/recipient resolution without proof that the detector generated and delivered the candidates | NA claims 16–21 | Targets monitoring providers, rights owners, and trust/safety systems | AF claims 7–12 remain tied to AF claim 1's upstream operations. |
| Broader or actor-specific method scope and method fallbacks | NA claims 22–30 | Preserves method formulations that may target a narrower performer or retain implementation fallbacks without every AF claim 20 limitation | AF claim 20 preserves the integrated end-to-end method category, but it does not preserve the different breadth of NA claim 22 or the resynchronization, hashing, manifest, unicast, collusion, and overlay fallbacks of NA claims 23–30. |
| Broader recipient-ledger, reconstructed-manifest, unicast, and collusion fallbacks under subsystem claims | NA claims 12, 14, 17–21, 25–28 | May be easier to plead or prove against a subsystem operator | AF carries these only in a narrower integrated tree. |
| Computer-readable-medium coverage | Not present in the current NA set; identified as a portfolio option | May target software distribution where system use is difficult to prove | AF contains no CRM claim; any CRM must be drafted support-safely and not as an unsupported end-to-end abstraction. |

This deferral is the central cost of AF. A continuation plan must identify which families have enough commercial value to justify prosecution; “preserve everything later” is not a completed decision.

## 4. Support and art transfer rules

1. The AF claims 1 and 20 same-region source-pair/timing formulation has no exact NA equivalent. Each claim's § 112 analysis must be performed as a whole and in its own statutory category.
2. The provisional Example 2 inconsistency follows AF claims 2–3 and NA claims 2–3 and 23; it is not cured by choosing one strategy.
3. The Examples 2→3→4 manifest integration affects AF claims 13–18 and related NA claims 9, 13, 15, 22, 24, and 29, but the exact limitations differ.
4. The weaker Examples 2→5 source-identity detection path is most acute for AF claims 1 and 20 and AF claims 7–10, and for NA claims 16–20 and 22–26.
5. AF claims 11–12 require review of the recipient-associated candidate-pattern input and the exact segmented-fingerprint/portion-to-contributor relationship. The attribution-score gate affects NA claim 21 only; no attribution-score limitation appears in the AF set, and it should not be reintroduced without an identified support basis.
6. The AF claim 14 and NA claim 13 chunk-geometry formulations are closely related, but neither receives support merely because equal-duration alternative chunks are conventional or disclosed.
7. Art scores may strengthen or weaken when limitations are combined. Neither AF nor NA matrix scores may be copied into the other matrix without rescoring the complete claim.
8. AF claim 20 changes claim category, not the technical novelty center. It inherits every claim-as-a-whole, source-identity, same-region, combined-example, and priority gate applicable to the corresponding AF claim 1 operations and requires its own § 101, restriction, and performance-proof review.

## 5. Continuation reservation recommendations

If counsel selects AF for the parent, the initial continuation reservation should at minimum evaluate:

1. an NA claim 1-style production system with NA claims 2–8 fallbacks;
2. an NA claim 9-style distribution system with NA claims 10–15 fallbacks;
3. an NA claim 16-style detection system with NA claims 17–21 fallbacks;
4. a broader or actor-specific method beginning from NA claim 22, together with each commercially useful and supportable NA claims 23–30 fallback not retained by AF claim 20; and
5. a production- or detection-focused CRM claim only if the filed algorithmic and structural disclosure supports it.

Which family is filed first should follow commercial actors, restriction/election history, prior-art developments, proof access, and budget—not the numerical order above. The continuation memo controls the pre-issue filing gate and completion evidence.

## 6. Change control

This crosswalk is valid only for `AF-2026-07-17-v2` and `NA-2026-07-17-v1`. AF claim 20 may be omitted or canceled at filing for a documented one-independent-claim strategy. That authorized selection must be annotated as the actual filed topology throughout the single AF-v2 package; it does not create or require a separate system-only AF package. Any other amendment, renumbering, omission, cancellation, restriction election, terminology characterization, or support-driven rewrite requires:

1. a new strategy version;
2. line-by-line crosswalk review;
3. updates to the affected strategy's support and art matrices; and
4. a recorded decision whether the change creates an additional continuation reservation.

No amendment or argument may treat the AF terminology hierarchy as a family-wide definition or disclaimer without an express counsel decision recorded across the affected cases.

## 7. Revision record

- **AF-2026-07-17-v2 (17 July 2026):** added an exact AF claim 20 to NA claim 22 comparison; recorded the one-package deletion option and continuation reservations for broader or actor-specific methods and NA claims 23–30; propagated the independent support and art gates; preserved the AF/NA terminology non-concession; and aligned AF claim 1's production description with its actual structured-list limitation rather than an unstated EDL requirement.
