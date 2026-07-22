# AA11393US — NA Prior-Art Comparison Matrix (DRAFT)

> **STRATEGY NA · CLAIM-SET VERSION NA-2026-07-22-v4 · STATUS 22 JULY 2026**
>
> **INTERNAL COUNSEL ANALYSIS — NOT FOR FILING AS-IS AND NOT AN ADMISSION.** This is a limited, claim-directed review. Scores are issue-spotting tools, not conclusions of prior-art status, anticipation, inherency, obviousness, materiality, or validity.

## 1. Scope and independent claims

| NA claim | Independent subject | Principal present distinction |
|---:|---|---|
| 1 | Production system | Structured-list movement of the same ordered physical-camera boundary to a noncoincident timing, producing different-camera frames in the intervening interval |
| 9 | Distribution system | Manifest-selected chunks preserving one of the two timings of that physical-camera boundary and recorded by recipient |
| 16 | Detector system | Delivered reference/mate chunk combinations with a mate cut-timing difference → plural scene-change-derived cut times → reconstructed manifest → equality → ledger recipient |
| 22 | End-to-end method | Production boundary + manifest delivery/association + plural cut-time reconstruction + equality lookup |

Canonical evidence is stored in [`../prior-art/`](../prior-art/README.md). The exact claim text in [`AA11393US-NA-US_claim-set_DRAFT.md`](AA11393US-NA-US_claim-set_DRAFT.md) controls.

## 2. Limitation and combination audit

| Claimed relationship | Closest verified teaching | Relationship not identified in one reviewed document | Consequence |
|---|---|---|---|
| Move a recorded boundary between retained identified physical cameras | A20 individualized EDL versions and source/time fields; B9 user-different switch points; ordinary multicamera EDL practice | Per-recipient movement of a physical-camera selection boundary in the claimed structured list | A20+B9+direct multicamera/EDL art is the principal production route |
| Same ordered transition at noncoincident timings with different-camera frames between | B9 varies actual switch points; A4 has camera-perspective fragments; B6 varies local temporal regions | Retained same physical-camera order and resulting alternate-camera interval | Preserve the full structural relationship; variable timing alone is crowded |
| Manifest-selected chunks preserve one transition timing and are recipient-associated | A4/A6/C8 teach manifests, variants, recipient sequences, and records | Binding those known delivery objects to the claimed physical-camera boundary | Claims 9, 13, and 15 retain the production-derived structure |
| Delivered manifests identify chunk combinations from a reference/mate ensemble having a mate cut-timing difference | A4/A6/C8 teach recipient-associated manifest combinations; B6/B9 teach recipient-specific local timing or stream-switch variation | The claimed delivered-manifest universe tied to reference/mate camera-cut timing variation | This relationship strengthens NA claim 16 but remains exposed to A4/A6/C8+B6/B9 combinations |
| Detect plural cut times and reconstruct a manifest | A4 recovers version sequences; A6 detects temporal patterns; A13 regenerates manifests from segment identifiers; B6/B8 reacquire timing | Reconstruction from scene-change-derived plural cut times | NA claim 16 faces material combination pressure |
| Search for the recipient associated with an equal delivered manifest | A4/A6 resolve users from recovered patterns; A13 regenerates manifests; A20 has registry lookup | Exact equality at the end of the claimed cut-time reconstruction | Equality is direct filing support but not a stand-alone novelty center |
| Equal matched manifest selects a mate chunk spanning the same physical-camera transition at a noncoincident timing | A4 supplies camera-perspective fragments/manifests; B9 supplies actual switch-time variation; A20 supplies EDL source/time fields and forensic motivation | The matched manifest's concrete mate chunk, retained ordered physical-camera transition, noncoincident timing, and intervening different-camera frames | NA claim 19 carries this combined relationship; direct multicamera/EDL art remains a material search target |

## 3. Stored-art comparison

Legend: **P** = concrete partial or analogous mapping; **—** = no concrete whole-claim mapping identified. No `P` is an obviousness conclusion and no `—` is a clearance.

| Document | NA 1 production | NA 9 distribution | NA 16 detector | NA 22 method |
|---|:---:|:---:|:---:|:---:|
| **A1 / D1 — US 2021/0352381 A1** | P — completed-copy delay/frame-rate transforms | P — recipient variant sequences | P — recipient variants and recoverable identifiers; no claimed mate-manifest/cut-time reconstruction chain | P |
| **A2 — US 7,630,497 B2** | — | P — segment-version assignments | P — segment sequences and tracing; no camera-cut mate or reconstructed-manifest equality | P |
| **A3 — US 2009/0320130 A1** | — | P — coded segment assignments | P — coded assignments and scoring; no claimed mate-manifest reconstruction chain | P |
| **A4 — US 10,834,158 B1** | P — camera-perspective alternatives | P — customized manifests and user patterns | P — perspective manifests, sequence recovery, and user resolution; no mate cut-timing/equal-manifest chain | P |
| **A5 — US 2012/0087583 A1** | — | — | P — perceptual hashes and shot comparison; no manifest ledger or mate timing | — |
| **A6 — US 2014/0325550 A1** | P — recipient temporal events | P — tailored manifests and served sequences | P — tailored manifests, temporal-pattern detection, and device resolution; no physical-camera mate/equal-manifest chain | P |
| **A7 — US 2017/0118537 A1** | — | P — device-driven segment selection | P — selected segments and tracing; no camera-cut manifest reconstruction | P |
| **A8 — US 2018/0352307 A1** | P — randomized temporal variants | P — identifying variant sequences | P — recipient variants and sequence identification; no claimed manifest-equality chain | P |
| **A9 — US 12,412,229 B2** | P — rendered watermark variants | P — client policies/IDs | P — suspect watermark identification and collusion analysis; no camera-cut manifest reconstruction | P |
| **A10 — US 2010/0100971 A1** | P — time-domain colour modulation | P — device identity | P — device-mark capture/extraction; no chunk-manifest or camera-cut reconstruction relationship | P |
| **A11 — US 2023/0230193 A1** | — | — | — | — |
| **A12 — US 2022/0358762 A1** | — | P — subscriber/device context | P — piracy classification; no manifest ledger, mate timing, or equality reconstruction | — |
| **A13 — US 2023/0103449 A1** | — | P — segment and manifest generation | P — manifest regeneration from segment identifiers; no scene-change input, mate timing, or recipient equality loop | P |
| **A14 — US 2022/0207120 A1** | P — per-user chunk symbols | P — user database | P — A/B chunks, recipient database, and detection objective; no claimed cut-time equality chain | P |
| **A15 — US 2024/0114066 A1** | — | P — session-bound manifests and address records | P — session-associated manifests; no mate camera-cut structure or suspect recovery | — |
| **A16 — US 2024/0185891 A1** | — | P — per-request manifests and recording IDs | P — per-request manifests; no mate camera-cut structure or suspect recovery | P |
| **A17 — US 12,046,260 B2** | P — per-account substitution | P — personalized-segment records | P — personalized segments and account records; no mate camera-cut structure or suspect recovery | — |
| **A18 — US 12,328,488 B2** | P — dynamic-segment substitution | P — user-keyed metadata | P — dynamic segments and user metadata; no mate camera-cut structure or suspect recovery | — |
| **A19 — US 2023/0353582 A1** | — | P — assigned-bit/client records | P — pirate acquisition and client identification; no claimed manifest-equality chain | P |
| **A20 — US 2012/0114309 A1** | P — individualized EDL versions and time-defined elements | P — recipient/version registry | P — unique EDL versions, source/time fields, registry, and cross-reference analysis; no delivered reference/mate chunk manifests or cut-time reconstruction | P |
| **B1 / D2 — CN 117278762 A** | — | P — codec provenance | P — provenance recovery; no reference/mate manifest or scene-change reconstruction | — |
| **B2 — WO 2021/224688 A1** | P — D1-family disclosure | P | P | P |
| **B3 — WO 2017/017603 A1** | — | P — source watermark | P — watermark capture/extraction/comparison; no claimed manifest chain | — |
| **B4 — WO 2010/044102 A2** | P — per-playback visible marks | P — device/time identity | P — piracy-point identification; no reference/mate chunk-manifest reconstruction | P |
| **B5 — CN 202455480 U** | P — receiver watermark | P — smart-card identity | P — watermark monitoring/alarm; no camera-cut manifest chain | — |
| **B6 — CN 100583750 C / Microsoft family** | P — local frame-count/width variation | P — buyer/key relation | P — recipient-local timing variation, hash reacquisition, and contributor search; no physical-camera mate manifest or equality | P |
| **B7 — WO 2021/141686 A1** | P — shots/cuts | — | P — shot-sequence piracy comparison; no manifest ledger or mate chunk relationship | — |
| **B8 — EP 2 811 416 A1** | — | — | P — relative-time pattern matching; no manifests, recipient ledger, or mate chunk | — |
| **B9 — WO 2009/156973 A1** | P — user-different switches among transformed streams | P — user keys and origin codes | P — recipient stream combinations and user-different switch times; no suspect recovery or physical-camera source relationship | P |
| **B10 — KR 2024-0168593 A** | P — per-user object attributes | P — user-code mapping | P — per-user variants, leak detection, and code inference; no camera-cut manifest chain | P |
| **C8 — ETSI TS 104 002 V1.1.1** | P — aligned A/B variants | P — edge sequencing and account/session patterns | P — A/B manifest sequences and tracing objective; no camera-cut reconstruction | P |
| **C3 — Tardos 2003 extended version** | — | P — user code assignment | P — code assignment and accusation; no suspect acquisition or manifest loop | — |

No reviewed document maps any NA independent as a whole. That is not a clearance conclusion. NA claim 16 has the least production-derived insulation; its delivered reference/mate chunk-combination ledger provides distribution-derived structure but remains subject to combination analysis rather than single-document anticipation alone.

## 4. Plausible § 103 routes

### NA claim 1

1. **A20 + B9 + conventional multicamera/EDL art:** individualized edit lists plus variable switch points plus physical-camera fields.
2. **D1/B6 + direct multicamera production art:** recipient-specific temporal variation plus known camera-boundary editing.

The disputed relationship is movement of the retained physical-camera boundary and the resulting different-camera interval, not temporal variation in the abstract.

### NA claim 9

1. **A4/A6/C8 + B9 + direct multicamera art:** manifest variants and recipient records plus variable switch positions and a physical-camera source.
2. **A20 + A4/A6:** individualized EDL motivation plus manifest delivery and lookup.

The claim requires manifest-selected chunks to preserve the physical-camera transition timing.

### NA claim 16

1. **A4 + B9 + A13 + A5/B7:** perspective manifests and user resolution plus user-different switch timings, manifest regeneration, and scene/shot detection.
2. **A6 + A13 + B6/B8:** tailored recipient sequences plus manifest regeneration and local-timing or relative-time reacquisition.
3. **A20 + A13 + B7, with B6 or B9:** forensic EDL/registry motivation plus manifest regeneration, shot detection, and recipient-specific timing variation.
4. **A4/B9 + A13, with A5/B7/B8 as needed:** manifest/switch-position combinations plus manifest regeneration and a cut-time recovery technique.

The response must test whether the art supplies a delivered-manifest ledger tied to reference/mate chunks having a camera-cut timing difference and reconstruction of an equal delivered manifest from plural scene-change-derived camera-cut time codes with a reasoned motivation and reasonable expectation of success.

### NA claim 22

The leading route is **A20+B9+A4/A6/A13**, with direct multicamera/EDL art supplying physical-camera edit entries and A5/B7/B8 supplying cut detection if needed. The exact production-boundary-to-delivered-manifest-to-reconstructed-manifest relationship remains the central issue.

Do not characterize A20 as teaching away. Its unique-EDL and product-signature language supports forensic individualization. Apply the evidence requirements in [MPEP § 2143](https://www.uspto.gov/web/offices/pac/mpep/s2143.html) and [MPEP § 2144.03](https://www.uspto.gov/web/offices/pac/mpep/s2144.html).

## 5. Dependent ladder

| NA claims | Added subject matter | Stored-art posture |
|---|---|---|
| 2–3, 23 | Later resynchronization and ten-frame implementation | Strong technical fallback in the stored corpus; support-gated by Example 2 |
| 4–7 | EDL fields, live direction, plural variations, retained source IDs | Direct EDL/vision-mixer art remains a priority search |
| 8, 30 | Overlay, including pre-segmentation order in claim 30 | Conventional graphics/watermark pressure; claim 30 also has a support gate |
| 10–12 | Adaptive delivery, mixing, ledger | Crowded by A4, A6–A8, A13, A15–A16, B9, C8 |
| 13, 25 | Same-interval/equal-duration paired chunks with transition geometry | A4/B9/C8 pressure packaging; retained physical-camera boundary remains material |
| 14, 27 | Unicast | Conventional implementation |
| 15, 24, 29 | Recipient timing combinations and manifest preservation | Multi-position sequences are crowded; exact physical-camera relationship carries value |
| 17–18, 26 | Perceptual hashes and sliding-window fuzzy comparison | Crowded by A5, B6–B8 |
| 19 | Equal matched manifest selects a mate chunk spanning the same physical-camera transition at a noncoincident timing | A4/B9/A20 and direct multicamera/EDL art create combination pressure; the full matched-manifest geometry is the material relationship |
| 20 | Plural recipient timing combination represented by the reconstructed manifest | Timing sequences are crowded; the claim inherits claim 19 and additionally requires the detected plural combination to be represented by the reconstruction |
| 21, 28 | Manifest-sequence collusion attribution | A2–A4, A6, A9, A19, B6, C3 provide substantial pressure |

## 6. Support, priority, and proof overlay

The art scores do not decide support. Counsel must separately resolve:

- NA claims 1 and 9 as strengthened physical-camera/manifest combinations;
- Mode A NA claim 16's eligibility, actor, proof, and art posture;
- Mode A NA claim 22's end-to-end combination and method-form posture;
- the Example 2 gate for claims 2–3 and 23;
- claims 13 and 25's chunk geometry;
- claim 19's matched-manifest physical-camera mate-chunk relationship;
- claims 15, 20, 24, and 29's timing-combination relationships, including claim 20's inheritance of claim 19;
- claims 21 and 28's collusion input/output; and
- claim 30's pipeline order.

NA claims 16 and 22 are assigned Mode A, so B10 does not enter their prior-art set merely by its 2 December 2024 publication date. B10's current substantive mapping is also low. Its statutory relevance remains claim-specific for any different formulation receiving a later effective date.

## 7. Search priorities and triggers

DW-08A should cover:

1. personalized physical-camera boundary editing in live or post-production EDLs;
2. alternate-angle screener differentiation and switch-boundary fingerprints;
3. delivered manifests selecting reference/mate chunks with camera-cut timing differences;
4. matched-manifest physical-camera transition geometry;
5. scene-change-derived manifest reconstruction;
6. equal-manifest lookup from detected cut sequences; and
7. manifest-sequence collusion attribution.

Re-score upon any claim amendment or renumbering; completion of DW-08A; addition or replacement of a canonical source; receipt of an Italian or US citation; authoritative B6 review; C7 acquisition; or a substantive AF matrix change.
