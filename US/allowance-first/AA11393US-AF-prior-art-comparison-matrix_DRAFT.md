# AA11393US — Allowance-First Prior-Art Comparison Matrix (DRAFT)

> **STRATEGY AF · CLAIM-SET VERSION AF-2026-07-17-v1 · STATUS 17 JULY 2026**
>
> **INTERNAL COUNSEL ANALYSIS — NOT FOR FILING AS-IS AND NOT AN ADMISSION.** This is a limited, claim-directed review. `Y`, `P`, `—`, “not identified,” and statements about combinations are issue-spotting tools, not conclusions that a document is prior art, anticipates a claim, supplies inherency, or establishes obviousness. Counsel must verify the source documents and the proposed combinations.

## 1. Scope and allowance-first topology

This matrix addresses the allowance-first (`AF`) claim topology rather than the actor-split normal-allowance topology. AF claim 1 places in one system the production-side boundary change, generic delivery and recipient association, and detection/recovery loop. AF claims 2–12 add production, detection, and collusion fallbacks. AF claim 13 adds the manifest/chunk distribution subsystem to AF claim 1; AF claims 14–19 narrow that subsystem. The exact text in [`AA11393US-AF-US_claim-set_DRAFT.md`](AA11393US-AF-US_claim-set_DRAFT.md), version `AF-2026-07-17-v1`, controls over this summary.

Canonical evidence remains in [`../prior-art/`](../prior-art/README.md), with searchable review text in [`../prior-art/markdown/`](../prior-art/markdown/README.md) and OCR-sensitive source copies in [`../prior-art/searchable/`](../prior-art/searchable/README.md). This file does not duplicate PDFs or make IDS-submission conclusions.

AF claim 1 is intentionally narrower than any one actor-split claim. That makes AF claim 1 materially harder to map against the reviewed corpus, but not immune from a multi-reference §103 rejection or from §112 and priority objections. The allowance thesis is the claimed operational chain, not the abstract ideas of temporal variation, manifest assignment, or recipient tracing.

AF claim 1 expressly uses the following transition terminology; the related portfolio term is retained only to distinguish the distribution-side representation:

- a **camera-source-transition pattern** organizes the candidate or detected ordered source transition and corresponding switch timing recited by AF claim 1; and
- a **camera-cut timing pattern** is the related distribution-side timing representation used elsewhere in the portfolio. It should not be substituted for AF claim 1's operational source-and-time pattern.

The terms perform different claim functions; neither is a label that converts generic timing data into the claimed physical-camera structure.

## 2. AF claim 1 limitation audit

| AF claim 1 operation | Closest verified teaching | What was not identified in one reviewed document | Principal pressure / drafting consequence |
|---|---|---|---|
| Receive synchronized views from plural cameras and a structured list identifying source cameras and cut time codes | B9 analyzes shot cuts and possible switch points; A4 mentions camera-perspective fragment alternatives; ordinary multicamera/EDL practice is the principal open search area | A machine-readable edit list used to individualize a recorded physical-camera selection boundary was not identified in the stored art | Conventional multicamera/EDL art is the most important missing search input. Keep the structured-list operation and identified source cameras express. |
| Generate reference and mate versions having the same ordered `A→B` transition at noncoincident timings, with temporally corresponding frames from different cameras in between | B9 selects different actual switch points among transformed streams; B6 varies local frame counts/widths; D1 applies delay/frame-rate transforms; A4 supplies camera-perspective alternatives | No reviewed document was identified moving the same ordered boundary between synchronized physical-camera views in an EDL and thereby substituting the intervening frames | A4+B9 plus conventional multicamera editing is the leading production-side combination. Do not rely on “variable timing” alone. |
| Deliver generated versions including a reference version and a mate version, and store a three-way delivered-version / candidate-pattern / recipient association | A4 discloses customized manifests, version-pattern records, and user resolution; A6 discloses recipient-specific temporal-event patterns and tailored manifests; A2/A3 disclose assignment/tracing | Association and distribution are crowded outside the physical-camera mechanism | These operations help close the loop but do not carry patentability by themselves. Preserve delivery of both version types and the express association among the delivered version, its generated source-and-time pattern, and its recipient. |
| Detect, in suspected content and at the candidate-distinguishing region, the source identities on both sides and the switch timing | A5/B7 disclose shot or suspect/reference comparison; A4 identifies perspective/version occupancy; B6 supplies hash reacquisition; B8 supplies distortion-tolerant relative-time matching | Detection of both ordered physical-camera identities and the moved boundary time at the same candidate-distinguishing region was not identified | A4 or A6 combined with A5/B7 and B6/B8 is plausible. Preserve the same-region and joint source-pair/time requirements; confirm algorithmic support. |
| Match both ordered source pair and timing, then resolve a recipient | A4 and A6 disclose recovered-pattern comparison and recipient/device resolution; A2/A3 disclose traitor tracing | The reviewed art did not disclose this recovery step operating on the claimed EDL-created physical-camera boundary | Generic lookup is known. The match must remain operationally tied to the generated candidate structure, not merely to informational labels. |

## 3. Stored-art comparison focused on AF claim 1

Legend: **Y** = the identified sub-operation is expressly or substantially taught; **P** = partial, analogous, or material construction/combination pressure; **—** = not identified in this limited review. These are feature-level scores, not whole-claim scores.

| ID / canonical document | Production or individualized variation | Delivery / association | Suspected-copy recovery | AF claim 1 effect |
|---|:---:|:---:|:---:|---|
| **A1 — D1, US 2021/0352381 A1** | P — recipient-varying delay/frame-rate and other completed-copy transforms | P/Y — device-ID selection and user-specific segment sequences | P — recoverable watermark/arbitrary identifiers | No multicamera EDL, alternate-camera interval, or recovery of an ordered physical-camera boundary. Relevant with conventional production art. |
| **A2 — US 7,630,497 B2** | — | Y — segment-version sequence keys and assignments | Y — hybrid traitor tracing | Dense on assignment/collusion, not the camera mechanism. |
| **A3 — US 2009/0320130 A1** | — | Y — coded segment variations and assignments | Y — recovered-file scoring | Strong non-Tardos analogue for AF claims 11–12: segment-level inner/outer codes, probabilistic scores, and traitor identification. |
| **A4 — US 10,834,158 B1** | P — alternatives may differ in camera perspective | Y — customized manifests and stored user patterns | Y — temporal alignment, version recovery, probabilistic user/group resolution | Closest single non-production reference. It lacks express movement of the same recorded physical-camera boundary; its express use of Tardos codes within content fragments also creates partial AF claim 12 pressure, but not the complete claimed segmented relationship. |
| **A5 — US 2012/0087583 A1** | — | — | Y — perceptual hashes and suspect/reference shot comparison | Direct pressure on AF claims 7–8 implementation details, not AF claim 1 as a whole. |
| **A6 — US 2014/0325550 A1** | P — recipient-specific forced/natural temporal events and variable segment duration | Y — tailored manifests and unique served sequences | Y — detected-pattern comparison and device/colluder identification | Supplies much of the non-camera delivery/recovery loop. The reviewed text did not disclose synchronized alternate-camera EDL variation. |
| **A7 — US 2017/0118537 A1** | — | Y — device-driven segment-version selection | P — later watermark tracing | Generic manifest/address selection is known. |
| **A8 — US 2018/0352307 A1** | P — randomized manifest durations and variant obfuscation | Y — identifying variant sequences | P — pirate-side detection countermeasures | Undercuts reliance on manifest timing or variant sequences alone. |
| **A9 — US 12,412,229 B2** | P — client-rendered watermark variants | P — per-client policies/identifiers | P/Y — server-side collusion detection | Relevant to AF claims 11–12 and AF claim 19, not the physical-camera boundary. |
| **A10 — US 2010/0100971 A1** | P — per-device time-domain colour modulation | P — device identity | Y — network capture and mark extraction | A complete marking/recovery loop of a different type; no EDL or camera-source structure. |
| **B1 — D2, CN 117278762 A** | — | P — codec-chain provenance | P — authorized decoder/display metadata analysis | Does not clearly disclose independent suspect-copy acquisition or recipient-specific camera variation. |
| **B2 — WO 2021/224688 A1** | P — same disclosure family as A1 | P/Y | P | Scored with A1 for substance. Its ISR X ratings address D1-family claims, not the AF claims. |
| **B3 — WO 2017/017603 A1** | — | P — source watermark | P — capture/extract/compare | Background watermark route only. |
| **B4 — WO 2010/044102 A2** | P — per-playback visible marks | P — device/time identity | P — point-of-piracy identification | Different marking architecture. |
| **B5 — CN 202455480 U** | P — receiver-inserted watermark | P — smart-card identity | P — monitoring/alarm | Different marking architecture. |
| **B6 — CN 100583750 C / Microsoft family** | Y/P — per-user local frame-count/width variation | P — buyer/key relationship | Y — hash reacquisition and likelihood-based contributor search | Strong analogous timing/hash art. No synchronized camera views, EDL, or moved ordered source boundary was identified. |
| **B7 — WO 2021/141686 A1** | P — shots/cuts | — | Y — shot-sequence piracy comparison | Direct pressure on generic shot/cut detection. |
| **B8 — EP 2 811 416 A1** | — | — | Y — relative subtitle-time patterns tolerant of frame-rate/ad changes | Direct pressure on broad timing resilience; no recipient-specific camera production. |
| **B9 — WO 2009/156973 A1** | Y/P — key-derived actual switches at user-different points among transformed streams | P — user keys and stream-origin codes | —: detection not elaborated in the reviewed publication | Critical production-side combination reference. The streams are transformed copies of the same content, not temporally corresponding physical-camera views; no EDL or claimed recovery loop was identified. |
| **C8 — ETSI TS 104 002 V1.1.1** | P — aligned A/B segment variants | Y — standardized edge sequencing and device/account/session patterns | P — forensic tracing objective; extraction out of scope | Generic A/B delivery is standardized. Same-position/equal-duration packaging is not a patentability center. |

## 4. Plausible §103 routes counsel should test

1. **Conventional multicamera/EDL practice + B9 + A4 or A6.** Conventional production may supply synchronized cameras and edit lists; B9 supplies a reason and mechanism to vary actual switch points; A4/A6 supply recipient assignment and recovery. The unanswered question is whether the references provide a reason and reasonable path to retain the same ordered physical-camera transition at noncoincident EDL positions and later recover both source identities and timing.
2. **A4 + B9 + A5/B7.** A4 supplies camera-perspective alternatives, customized manifests, recovery, and user lookup; B9 supplies key-dependent actual switches; A5/B7 supply known cut comparison. AF claim 1 should preserve physical-camera provenance, EDL boundary movement, the intervening alternate-camera interval, and same-region joint matching.
3. **Conventional EDL practice + B6 + A6.** B6 supplies individualized local timing and robust reacquisition; A6 supplies a temporal-event delivery/recovery loop. AF claim 1 remains exposed if direct art shows using those teachings on synchronized multicamera selections.
4. **D1 + conventional multicamera practice + A4/A6.** D1's scene-aligned transformations and device-driven variant selection cannot be dismissed as watermark-only. The response is the claimed resulting physical-camera structure and its operational recovery, not an absolute incompatibility assertion.

The number of references alone does not defeat obviousness. Counsel must separately test analogous-art status, the articulated reason to combine, modification required, reasonable expectation of success, and whether every AF claim 1 operation is actually supplied.

## 5. Dependent ladder — honest allowance value

| AF claim(s) | Added subject matter | Stored-art posture / counsel direction |
|---|---|---|
| **AF claims 2–3** | Later-boundary resynchronization; ten-frame implementation | Strongest technical fallback in this corpus. Preserve the provisional Example 2 inconsistency and obtain counsel's priority/new-matter opinion before making it the sole allowance basis. |
| **AF claims 4–6** | EDL fields; live director selections; variation at plural cuts | Useful concrete production limitations, but direct vision-mixer/EDL art remains the most important search gap. AF claim 6 is analogous to plural transformations/events in D1, A6, B6, and B9. |
| **AF claims 7–8** | Perceptual hashes; sliding-window fuzzy matching | A5, B6, B7, and B8 make these implementation details crowded. They add concreteness, not a reliable novelty center. |
| **AF claims 9–10** | Manifest delivery; association of each manifest with the candidate pattern of its assembled delivered version; reconstruction from a time code derived from the detected switch timing; delivered-manifest ledger lookup | A4 is functionally close on customized-manifest delivery, recovered version-pattern estimation, and customized-manifest database comparison, but the reviewed text does not build a reconstructed manifest from the time code of the claimed detected physical-camera transition. Retain these as implementation fallbacks tied to AF claim 1's moved ordered boundary. |
| **AF claims 11–12** | Probabilistic analysis applied to recipient-associated candidate camera-source-transition patterns to identify recipients whose delivered versions contributed portions; segmented Tardos fingerprints applied to content segments with at least one portion-specific contributor output | A2/A3/A4/A6/B6 teach close segmented, probabilistic, or positive-attribution operations; A4 and A6 expressly mention Tardos codes; A9 identifies watermark IDs of colluding sources at different times. No reviewed stored document supplies the complete physical-camera-pattern input or AF claim 12's full segmented-Tardos/output relationship. Treat both as dependent combination fallbacks, not as immunity from Tardos and traitor-tracing art. |
| **AF claim 13** | Manifest/chunk distribution preserving one of the generated boundary positions and recording recipient association | Patentability continues to come from inherited AF claim 1. A4/A6/B9/C8 densely populate manifests, sequencing, and recipient records. Confirm Examples 2–4 integration and priority. |
| **AF claim 14** | Different manifest-selected same-interval/equal-duration reference and mate chunks, each containing the ordered transition at its respective time | A4 and C8 substantially teach the packaging mechanics; B9 supplies analogous aligned segmentation. Value lies in binding the inherited physical-camera boundary to each selected chunk. |
| **AF claims 15–17** | CDN/ABR tailoring; mixing/progressive assignment; unicast | Conventional or densely taught by A4, A6, A7, A8, B9, and C8. Commercial implementation coverage only. |
| **AF claim 18** | Recipient-associated choices across plural distinguishing regions | A2/A3/A4/A6/A7/A8/B9/C8 teach recipient-associated multi-position sequences. Preserve the inherited same ordered physical-camera transition at each region. |
| **AF claim 19** | Additional audio/video overlay before chunk segmentation | D1, A4, A9, and conventional watermark/graphics art make the overlay operation crowded. The claimed pre-segmentation sequence needs separate art and written-description verification; implementation coverage only. |

## 6. §112 and priority gates that the allowance strategy cannot hide

1. **AF claim 1 as a whole.** Filed PCT claim 1 supports an integrated system architecture, but counsel must confirm the strengthened operational chain as a whole in the PCT and provisional—not merely isolated nouns or steps.
2. **Detected source identities.** Confirm support for detecting and matching the camera sources on both sides together with switch timing at the same candidate-distinguishing region. Generic scene-change or cut-time detection does not automatically support that operation.
3. **Production-to-candidate relationship.** Confirm that the candidate patterns used for detection are support-safely tied to the reference/mate versions generated by the claimed EDL variation.
4. **AF claims 2–3.** Address the provisional Example 2 “mistake” sentence before relying on resynchronization for priority or allowance.
5. **AF claim 8.** Confirm that Example 5 supports sliding-window perceptual-hash analysis of the ordered source transition, not only switch instants or generic frames.
6. **AF claim 9.** Confirm the exact relationship among a delivered manifest, the candidate pattern of the version assembled under that manifest, the time code derived from the detected switch timing, and the reconstructed manifest; generic manifest and reconstruction passages do not alone establish the complete combination.
7. **AF claims 11–12.** Confirm support for applying the probabilistic algorithm to recipient-associated candidate camera-source-transition patterns and identifying recipients whose delivered versions contributed respective portions. For AF claim 12, separately confirm the exact segmented-Tardos relationship among respective fingerprints, content segments, respective suspect portions, and the identified contributor; a general Tardos citation does not automatically support that relationship.
8. **AF claims 13–18.** Confirm that Examples 2–4 and the corresponding provisional passages disclose the exact operational connection between the moved physical-camera boundary and manifest-selected chunks/recipient sequences. AF claim 14's transition placement within each chunk is not quoted verbatim in one passage.
9. **AF claim 19.** Confirm support for performing the overlay before segmentation into the claimed chunks; express support for overlays does not by itself settle that pipeline order.

If a strengthened limitation lacks provisional support, importing it into the sole independent may expose the entire tree to a priority or §112 rejection. That risk is the principal cost of the allowance-first topology.

## 7. Bottom line and search priority

AF claim 1 is materially harder to reject over the reviewed documents than the separate production or detection independents because no reviewed document supplies its complete production-to-recovery chain. Its strongest factual distinction is the same ordered transition between synchronized physical cameras at noncoincident EDL positions, followed by detection and joint source-pair/time matching at the corresponding distinguishing region. AF claim 1 remains vulnerable to a combination assembled from conventional multicamera/EDL practice, B9/A4/B6 on individualized switch structure, and A4/A6/A5/B7/B8 on recovery.

The most important unresolved search is direct multicamera vision-mixer/EDL art that creates personalized versions by moving or selecting camera boundaries. A professional search should also cover synchronized alternate-angle screeners, switch-boundary fingerprints, and recovery of source-camera identity after re-encoding or temporal edits.

## 8. Maintenance

Revisit this matrix on any AF claim amendment or renumbering, new prior-art document, Italian search-report citation, receipt of C3/Tardos or C7/Lin, authoritative English-family review of B6, or correction to the canonical normal-allowance matrix.

| Date | Event | Scope |
|---|---|---|
| 17.07.2026 | **AF-2026-07-17-v1 created** | Reframed the verified canonical art around one integrated AF claim 1 system and AF claims 2–19 dependent ladder; preserved combination, §112, and priority gates; no IDS conclusion made |
| 17.07.2026 | **Reconciled to final AF text** | Reflected AF claim 1's reference-and-mate delivery and three-way association; conformed AF claims 9 and 11 summaries; replaced the superseded AF claim 12 formulation with segmented-Tardos analysis and support gates |
