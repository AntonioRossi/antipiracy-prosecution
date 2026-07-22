# AA11393US — AF/NA Claim and Coverage Crosswalk (DRAFT)

> **STRATEGY AF · CLAIM-SET VERSION AF-2026-07-22-v6 · STATUS 22 JULY 2026**
>
> **INTERNAL COUNSEL ANALYSIS — NOT FOR FILING AND NOT A CLAIM-CONSTRUCTION POSITION.** This crosswalk compares functional coverage; it does not state that any AF and NA claim has identical scope. Every external reference is strategy-qualified.

## 1. Purpose and controlling texts

This document maps the `AF-2026-07-22-v6` tree against the actor-focused `NA-2026-07-22-v4` tree. The exact wording in [`AA11393US-AF-US_claim-set_DRAFT.md`](AA11393US-AF-US_claim-set_DRAFT.md) and [`../normal-allowance/AA11393US-NA-US_claim-set_DRAFT.md`](../normal-allowance/AA11393US-NA-US_claim-set_DRAFT.md) controls.

Both strategies place physical-camera identity on the production side and use plural detected camera-cut time codes, reconstructed manifests, equality to a delivered manifest, and ledger lookup on the suspect side. AF claims 1 and 19 integrate those operations in complete system and method chains. AF claim 23 separately recites the affirmative monitor-side method with a mate-containing reconstructed-same-combination nexus. NA supplies standalone production, distribution, and detection systems and an end-to-end method. Neither formulation defines or construes the other.

## 2. AF-to-NA functional crosswalk

| AF claim | AF limitation | Closest NA coverage | Difference that matters |
|---:|---|---|---|
| 1 | Plural structured-list camera-boundary variation → manifest delivery/recipient association → plural cut-time reconstruction → equal-manifest ledger lookup | NA claims 1 and 7 for production; 9 and 12 for delivery/ledger; 16 for delivered reference/mate chunk-combination manifests and detector recovery; 19–20 for matched-manifest physical-camera/plural-timing fallbacks; 22 for an end-to-end method | No NA system claim recites the complete AF chain; the NA system independents separate the principal actors. |
| 2 | Preserve a later reference cut timing and restore synchronization | NA claims 2 and 23 | Both strategies share the Example 2 support gate. |
| 3 | Ten-frame extension/shortening and later resynchronization | NA claim 3 | AF claim 3 applies the concrete Example 2 implementation inside the complete AF system. |
| 4 | Structured list is an EDL | NA claim 4 | AF claim 1 already recites source-camera and in/out-point fields; AF claim 4 adds the EDL label. |
| 5 | Live viewpoints and director-commanded real-time selections | NA claim 5 | Same added production context; AF remains end-to-end. |
| 6 | A respective single-cut mate for each selected cut | NA claim 6 | AF isolates each selected-cut variation in a respective mate; NA claim 6 varies plural cuts within the production dependency. |
| 7 | Perceptual-hash comparison for plural cut-time detection | NA claims 17 and 26 | The claims use the same comparison class within different inherited chains. |
| 8 | Sliding-window fuzzy hash matching | NA claims 18 and 26 | Same implementation family with different antecedents. |
| 9 | Adaptive CDN delivery and device/network-tailored manifests | NA claim 10 | AF claim 9 inherits the complete production and recovery chain. |
| 10 | Reference/mate chunk mixing and progressive manifest assignment | NA claim 11 | Same implementation class inside different inherited architectures. |
| 11 | Mixed-version suspect and probabilistic analysis of recipient-associated manifest chunk-selection sequences | NA claims 21 and 28 | The exact probabilistic input, contributor output, and claim category differ. |
| 12 | Segmented Tardos fingerprints and contributor identification for a respective portion | NA claims 21 and 28 | No NA claim recites the exact segmented-Tardos/portion relationship. |
| 13 | Equal-duration reference/mate chunks spanning the same playback interval | NA claims 13 and 25 | AF claim 13 does not itself require each chunk to straddle the retained transition; AF claim 14 does. |
| 14 | Paired chunks contain the retained transition at respective reference and mate timings | NA claims 13 and 25 | Closely related geometry; exact antecedents and inherited chains differ. |
| 15 | Blockchain registration of manifest-recipient associations | No current NA blockchain claim; PCT claim 13 support is relevant | AF preserves the disclosed implementation only inside the integrated system. |
| 16 | Unicast delivery | NA claims 14 and 27 | Same delivery mode; no standalone AF distribution claim exists. |
| 17 | Recipient-associated timing choices across plural selected cuts | NA claims 15, 20, and 29 | AF represents the plural choices through delivered manifest combinations and ledger association. |
| 18 | Additional audio/video elements overlaid before segmentation | NA claims 8 and 30 | AF expressly requires the pre-segmentation order. |
| 19 | Method performance of AF claim 1's complete plural-cut reconstructed-manifest chain | NA claim 22 | Both methods use cut-time reconstruction and equal-manifest lookup; AF requires variation at plural selected cuts, with each selected-cut variation present in at least one mate, whereas NA claim 22 requires at least one varied cut and carries additional fallbacks in claims 23–30. |
| 20 | AF claim 19 method with a delivered recipient timing-choice combination containing an affirmative mate choice and reconstruction of the same detected combination | NA claims 20 and 29 for plural timing reconstruction and the method timing-choice combination | AF claim 20 expressly connects the equal delivered manifest's mate-containing recipient combination to reconstruction of the same detected combination; that exact relationship is **D/CE/G** and parallels AF claim 17's system-side record. |
| 21 | AF claim 19 method with perceptual-hash cut-time detection | NA claim 26 | Both add perceptual-hash comparison; AF claim 21 independently preserves a directly supported detection fallback without inheriting AF claim 20's relationship-specific gate. |
| 22 | AF claim 21 method with sliding-window fuzzy matching | NA claim 26 | NA claim 26 recites perceptual hashing and fuzzy matching in one dependent; AF separates them into the two-step method branch `19 → 21 → 22`. |
| 23 | Monitor-side suspect acquisition, plural cut-time derivation, reconstructed-manifest building, and equal delivered-manifest ledger search to identify a recipient; the equal delivered manifest contains an affirmative mate timing and matches the same detected plural timing combination | NA claim 16 supplies the closest detector-system operations; NA claims 19–20 supply related matched-manifest and plural timing fallbacks; AF-CONT claims 14 and 19 supply the broader method and overlapping causal-nexus formulations | AF claim 23 is an affirmative method that omits production and delivery performance but requires one monitoring entity to perform the complete recovery chain or another performer's conduct to be legally attributable to that entity under the applicable method-claim standard. It is narrower than AF-CONT claim 14, overlaps AF-CONT claim 19's causal nexus, and does not inherit NA claim 16's system-format Mode A assignment. |

## 3. Coverage outside AF

Selecting AF for the initial case does not supply the following as standalone claims:

| Coverage | NA location | Commercial value | AF consequence |
|---|---|---|---|
| Production/mate generation without downstream delivery or detection | NA claims 1–8 | Broadcaster, production facility, mate-generation vendor | Every AF system dependent inherits delivery and recovery. |
| Distribution/recipient association without production or detection | NA claims 9–15 | Streaming platform, origin service, licensee, CDN | AF delivery limitations remain inside AF claim 1. |
| Standalone detection system without production and delivery by the accused system | NA claims 16–21 | Monitoring provider, rights owner, trust/safety operator | AF claim 23 recites a monitor-side method, not the standalone detector-system category or NA claims 16–21's complete fallback ladder. |
| Broader end-to-end and monitor-side method fallbacks | NA claims 22–30 and AF-CONT claims 14–16 and 19 | Alternative performer, implementation, and proof configurations | AF claims 19–22 preserve the integrated plural-cut method family; AF claim 23 preserves the narrower causal-nexus monitor method. AF-CONT claim 14 remains broader and AF-CONT claims 15–16 retain monitor-side implementation fallbacks. |
| Computer-readable-medium coverage | Not present in either current set | Potential software-distribution coverage | Requires a separately supported and art-scored claim. |

## 4. Support and art transfer rules

1. AF claims 1 and 19 require claim-as-a-whole support analysis for the plural production-to-reconstruction relationship.
2. NA claims 16 and 22 are assigned DW-05A Mode A. NA claim 16 has direct support for the delivered reference/mate chunk-combination ledger with a mate cut-timing difference, suspect acquisition, plural cut-time derivation, reconstructed-manifest building, equality, ledger search, and recipient identification; provisional method claim 10 and PCT Method 200/claims 16–17 support NA claim 22's complete chain. NA claim 19 retains a combined-example gate for the equal matched manifest's mate chunk and physical-camera geometry; NA claim 20 inherits that gate and retains its plural timing-reconstruction gate.
3. The provisional Example 2 issue follows AF claims 2–3 and NA claims 2–3 and 23.
4. Examples 2→3→4 remain relevant to the production-boundary-to-manifest relationships and paired-chunk geometry in each strategy.
5. Provisional system claim 1 and method claim 10, PCT claim 15, Method 200, and PCT claims 16–17 directly disclose the basic reconstruction loop. That direct component support does not decide the strengthened independent claims as a whole.
6. AF claims 11–12 and NA claims 21 and 28 require strategy-specific review of the probabilistic input and contributor output.
7. AF claim 19 changes statutory category, not technical content. AF claim 20 adds a relationship-specific **D/CE/G** causal nexus; AF claims 21–22 add directly disclosed detection implementations without inheriting claim 20. None cures AF claim 19's § 101, restriction, performance-proof, priority, or divided-infringement posture.
8. AF claim 23's individual recovery operations are direct, but its method-form delivered-manifest environment and mate-containing reconstructed-same-combination nexus are **D/CE/G** and the whole claim is **D/CE/G; mode unassigned**. It requires a separate claim-as-a-whole mode, equality construction, full-scope reconstruction, actor, § 101, restriction, territorial, proof, and art determination; no mode transfers from NA claim 16 or AF claim 19.
9. Art scores cannot transfer between AF and NA without rescoring the complete limitation set. AF's integrated plural-cut chain and NA claim 22 face material combination pressure from A20+B9+A4/A6/A13/A21. AF claim 23 separately faces A4/A6+A13+A21, with A20 or B9 supplying personalization or timing motivation. NA claim 16 faces A4+B9+A13+A21/A5/B7, A6+A13+A21/B6/B8, and A20/A4/B9+A13+A21 routes; NA claims 19–20 also face direct multicamera/EDL pressure.
10. Written description and enablement remain separate inquiries; neither conclusion establishes the other.

## 5. Continuation reservations

If AF is selected for the parent, the continuation docket should evaluate:

1. an NA claim 1-style production system with useful NA claims 2–8;
2. an NA claim 9-style distribution system with useful NA claims 10–15;
3. an NA claim 16-style reconstructed-manifest detection system with useful NA claims 17–21;
4. the broader AF-CONT claim 14 monitor method and useful claims 15–16, with AF-CONT claim 19 retained, substituted, or omitted only after a recorded overlap, restriction, and double-patenting decision relative to AF claim 23;
5. a broader or actor-specific method beginning from NA claim 22 with useful NA claims 23–30;
6. a production- or detection-focused computer-readable-medium claim only if supported and commercially justified; and
7. any broader local alternate-camera substitution theory only after support and art review.

The continuation memo controls the pre-issue filing gate, copendency evidence, and chain-closure record.

## 6. Operative package control

This crosswalk applies to `AF-2026-07-22-v6` and `NA-2026-07-22-v4`. Any amendment, renumbering, omission, cancellation, restriction election, or support-driven formulation requires a dependency/count review, limitation-level crosswalk review, updated support and art matrices, and a continuation-reservation decision.
