# AA11393US — AF/NA Claim and Coverage Crosswalk (DRAFT)

> **STRATEGY AF · CLAIM-SET VERSION AF-2026-07-22-v4 · STATUS 22 JULY 2026**
>
> **INTERNAL COUNSEL ANALYSIS — NOT FOR FILING AND NOT A CLAIM-CONSTRUCTION POSITION.** This crosswalk compares functional coverage; it does not state that any AF and NA claim has identical scope. Every external reference is strategy-qualified.

## 1. Purpose and controlling texts

This document maps the integrated `AF-2026-07-22-v4` tree against the actor-focused `NA-2026-07-22-v4` tree. The exact wording in [`AA11393US-AF-US_claim-set_DRAFT.md`](AA11393US-AF-US_claim-set_DRAFT.md) and [`../normal-allowance/AA11393US-NA-US_claim-set_DRAFT.md`](../normal-allowance/AA11393US-NA-US_claim-set_DRAFT.md) controls.

Both strategies place physical-camera identity on the production side and use plural detected camera-cut time codes, reconstructed manifests, equality to a delivered manifest, and ledger lookup on the suspect side. AF claims 1 and 19 integrate those operations in complete system and method chains. NA supplies standalone production, distribution, and detection systems and an end-to-end method. Neither formulation defines or construes the other.

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

## 3. Coverage outside AF

Selecting AF for the initial case does not supply the following as standalone claims:

| Coverage | NA location | Commercial value | AF consequence |
|---|---|---|---|
| Production/mate generation without downstream delivery or detection | NA claims 1–8 | Broadcaster, production facility, mate-generation vendor | Every AF system dependent inherits delivery and recovery. |
| Distribution/recipient association without production or detection | NA claims 9–15 | Streaming platform, origin service, licensee, CDN | AF delivery limitations remain inside AF claim 1. |
| Detection/recipient resolution without production and delivery by the accused system | NA claims 16–21 | Monitoring provider, rights owner, trust/safety operator | AF detection limitations remain inside AF claim 1. |
| Broader end-to-end method fallbacks | NA claims 22–30 | Alternative performer and proof configurations | AF claim 19 preserves the narrower integrated plural-cut method. |
| Computer-readable-medium coverage | Not present in either current set | Potential software-distribution coverage | Requires a separately supported and art-scored claim. |

## 4. Support and art transfer rules

1. AF claims 1 and 19 require claim-as-a-whole support analysis for the plural production-to-reconstruction relationship.
2. NA claims 16 and 22 are assigned DW-05A Mode A. NA claim 16 has direct support for the delivered reference/mate chunk-combination ledger with a mate cut-timing difference, suspect acquisition, plural cut-time derivation, reconstructed-manifest building, equality, ledger search, and recipient identification; provisional method claim 10 and PCT Method 200/claims 16–17 support NA claim 22's complete chain. NA claim 19 retains a combined-example gate for the equal matched manifest's mate chunk and physical-camera geometry; NA claim 20 inherits that gate and retains its plural timing-reconstruction gate.
3. The provisional Example 2 issue follows AF claims 2–3 and NA claims 2–3 and 23.
4. Examples 2→3→4 remain relevant to the production-boundary-to-manifest relationships and paired-chunk geometry in each strategy.
5. Provisional system claim 1 and method claim 10, PCT claim 15, Method 200, and PCT claims 16–17 directly disclose the basic reconstruction loop. That direct component support does not decide the strengthened independent claims as a whole.
6. AF claims 11–12 and NA claims 21 and 28 require strategy-specific review of the probabilistic input and contributor output.
7. AF claim 19 changes statutory category, not technical content. It requires separate § 101, restriction, performance-proof, support, and priority review.
8. Art scores cannot transfer between AF and NA without rescoring the complete limitation set. AF's plural-cut chain and NA claim 22 face material combination pressure from A20+B9+A4/A6/A13. NA claim 16 separately faces A4+B9+A13+A5/B7, A6+A13+B6/B8, and A20/A4/B9+A13 routes; NA claims 19–20 also face direct multicamera/EDL pressure.
9. Written description and enablement remain separate inquiries; neither conclusion establishes the other.

## 5. Continuation reservations

If AF is selected for the parent, the continuation docket should evaluate:

1. an NA claim 1-style production system with useful NA claims 2–8;
2. an NA claim 9-style distribution system with useful NA claims 10–15;
3. an NA claim 16-style reconstructed-manifest detection system with useful NA claims 17–21;
4. a broader or actor-specific method beginning from NA claim 22 with useful NA claims 23–30;
5. a production- or detection-focused computer-readable-medium claim only if supported and commercially justified; and
6. any broader local alternate-camera substitution theory only after support and art review.

The continuation memo controls the pre-issue filing gate, copendency evidence, and chain-closure record.

## 6. Operative package control

This crosswalk applies to `AF-2026-07-22-v4` and `NA-2026-07-22-v4`. Any amendment, renumbering, omission, cancellation, restriction election, or support-driven formulation requires a dependency/count review, limitation-level crosswalk review, updated support and art matrices, and a continuation-reservation decision.
