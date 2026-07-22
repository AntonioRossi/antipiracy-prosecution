# AA11393US — AF Actor-Focused Continuation Prior-Art Comparison Matrix (DRAFT)

> **STRATEGY AF-CONT · CLAIM-SET VERSION AF-CONT-2026-07-22-v2 · STATUS 22 JULY 2026**
>
> **INTERNAL COUNSEL ANALYSIS — NOT FOR FILING AS-IS AND NOT AN ADMISSION.** This is a limited claim-directed review. The scores do not concede prior-art status, anticipation, inherency, obviousness, materiality, or validity. Counsel must verify source text, dates, statutory availability, effective-date posture, combinations, and claim construction.

## 1. Scope and scoring

This matrix applies to the 19 claims in [`AA11393US-AF-CONT-US_claim-set_DRAFT.md`](AA11393US-AF-CONT-US_claim-set_DRAFT.md), version `AF-CONT-2026-07-22-v2`, and the 33 canonical sources A1–A21, B1–B10, C8, and C3 in [`../prior-art/`](../prior-art/README.md). It uses the current NA and `AF-2026-07-22-v6` matrices as its claim-directed review record. OCR-sensitive points must be checked against the canonical PDF.

Legend: **Y** = the scored whole claim or added limitation is expressly or substantially taught; **P** = a concrete partial or analogous mapping; **—** = no concrete mapping identified in this review. A dependent score addresses only its added limitation. No `P` is an obviousness conclusion and no `—` is a clearance.

## 2. Independent claims as wholes

No reviewed document scores `Y` against AF-CONT claim 1, 6, 11, or 14 as a whole.

| Independent | `P` sources | `—` sources | Carrying limitation or relationship not found in one document |
|---:|---|---|---|
| **1 — production system** | A1, A4, A8, A20, B2, B6, B9, B10, C8 | A2, A3, A5–A7, A9–A19, A21, B1, B3–B5, B7, B8, C3 | Varying a recorded physical-camera cut while retaining the same ordered camera transition at noncoincident timings and producing the temporally corresponding different-camera interval; affirmative reference production is an additional operation, not the principal art distinction |
| **6 — distribution system** | A1–A4, A6–A10, A12–A20, B1–B6, B9, B10, C8, C3 | A5, A11, A21, B7, B8 | Reference/mate versions having the same physical-camera transition at different timings, with each delivered manifest preserving one timing and the recipient record identifying that delivered manifest |
| **11 — detector system** | A1–A10, A12–A21, B1–B10, C8, C3 | A11 | A delivered reference/mate chunk-combination manifest ledger, plural scene-change-derived cut times, a reconstructed manifest equal to a delivered manifest, and recipient lookup as one claimed system |
| **14 — detector-only method** | A1–A10, A12–A21, B1–B10, C8, C3 | A11 | The same affirmative detector chain as claim 11, including the delivered reference/mate manifest environment and equality-based recipient lookup |

The production, distribution, and detector-system independents preserve materially different direct-infringement targets from the AF parent. AF-CONT claim 14 remains broader than AF claim 23; AF-CONT claim 19 overlaps AF claim 23's causal-nexus formulation. The detector claims avoid requiring the monitoring actor to perform production or delivery, but their insulation is narrower because A4, A6, A13, A20, and A21 collectively pressure most of the recovery chain.

## 3. Direct dependent limitations

Sources not listed for a dependent limitation score `—` for that added limitation.

### Claims 2–5 — production dependents

| Claim | Added limitation | `Y` sources | `P` sources | Assessment |
|---:|---|---|---|---|
| **2** | EDL with source-camera and in/out-point fields | A20 | — | Useful structural fallback, but A20 directly crowds the EDL field structure. Patentability remains in inherited claim 1. |
| **3** | Live diverse viewpoints and director-commanded real-time selections | — | A4 | Direct live production/vision-mixer art remains a material DW-08A gap. |
| **4** | Complete retained ordered-transition, noncoincident-timing, and different-camera-interval relationship at each of plural director-commanded cuts | — | A1, A8, A20, B6, B9, C8 | Generic plural variation positions are crowded, but no reviewed source maps the complete physical-camera relationship at each plural director cut. The claim adds substantive art insulation and a separate support gate. |
| **5** | Overlay the additional element onto both reference and mate | — | A1–A4, A6, A7, A9–A11, A14, A17–A20, B1, B3–B6, C8 | Overlaying is crowded, but the same added element on both versions is not expressly identified. The inherited claim 1 relationship remains the principal distinction. |

### Claims 7–10 — distribution dependents

| Claim | Added limitation | `Y` sources | `P` sources | Assessment |
|---:|---|---|---|---|
| **7** | CDN/adaptive streaming and recipient tailoring | A4, A6, C8 | A7, A8, A13, A15, A16, A18 | Conventional delivery implementation; value remains in inherited claim 6. |
| **8** | Mixing chunks of the reference version and the mate version with progressive manifest assignment | — | A1–A4, A6, A14, A16, B2, B9, C8 | Mixing and per-request selection are crowded; progressive availability does not cure the inherited physical-camera gate. |
| **9** | Ledger identifying the user or group receiving each manifest | A4 | A1–A3, A6, A7, A9, A10, A12, A14–A20, B1, B4–B6, B9, B10, C8, C3 | Recipient records are crowded; the important nexus is to the particular delivered manifest preserving a claimed transition timing. |
| **10** | Unicast delivery | — | A4, A6, A7, A13–A18, C8 | Conventional implementation fallback. |

### Claims 12–13 and 15–16 — detector dependents

| Claims | Added limitation | `Y` sources | `P` sources | Assessment |
|---:|---|---|---|---|
| **12, 15** | Perceptual-hash frame comparison | A5 | A12, A21, B6, B7 | A21 uses cumulative-histogram frame comparison rather than the claimed perceptual hashes. These claims principally narrow implementation, not the manifest-equality concept. |
| **13, 16** | Sliding-window fuzzy comparison of groups of perceptual hashes | — | A5, A21, B6–B8 | A21's sliding window is a shot-boundary detector, not fuzzy matching of perceptual-hash groups. The combined implementation is narrower but remains exposed to routine-combination arguments. |

### Claims 17–19 — recipient-to-recovered-combination fallbacks

Each row accounts for all 33 canonical sources. No reviewed document scores `Y` for any of these added limitations.

| Claim | Added causal-nexus limitation | `P` sources | `—` sources | Assessment |
|---:|---|---|---|---|
| **17 → 6** | Plural physical-camera timing-choice combinations, a delivered recipient-associated manifest containing an affirmative mate timing, and association of that manifest with the recipient | A1–A4, A6–A10, A13, A14, A16–A20, B2, B4, B6, B8–B10, C8, C3 | A5, A11, A12, A15, A21, B1, B3, B5, B7 | Generic multi-position recipient codes, variant sequences, records, and switch timings provide partial pressure. No reviewed source maps the complete physical-camera timing-choice → mate-containing delivered manifest → recipient-record relationship. |
| **18 → 11** | An equal delivered manifest containing an affirmative mate timing and a reconstructed manifest representing the same detected plural timing combination | A1–A4, A6–A8, A10, A13, A14, A20, A21, B2, B6, B9, C8, C3 | A5, A9, A11, A12, A15–A19, B1, B3–B5, B7, B8, B10 | A21 directly pressures cut-duration sequencing and exact fingerprint equality, but does not reconstruct a delivered manifest or supply the recipient/mate-combination relationships. The complete delivered mate-containing combination → reconstruction of the same detected combination remains unlocated. |
| **19 → 14** | Affirmative method counterpart of claim 18 | A1–A4, A6–A8, A10, A13, A14, A20, A21, B2, B6, B9, C8, C3 | A5, A9, A11, A12, A15–A19, B1, B3–B5, B7, B8, B10 | The added art posture is the same as claim 18, but claim 19 inherits claim 14's affirmative method, actor-attribution, eligibility, and effective-date gates. AF parent claim 23 has the same composite technical focus and requires coordinated scoring if either wording changes. |

## 4. A21 treatment

A21, US 2021/0166036 A1, directly teaches feature-level shot-boundary detection, deriving shot durations from boundary positions, composing a duration/time-slice sequence fingerprint, and exact equality between an input fingerprint and a database fingerprint. It therefore scores `P`, not `Y`, against claims 11 and 14 as wholes and against the reconstructed-manifest/equal-delivered-manifest limitations. A generic video fingerprint is not a delivered reference/mate chunk-combination manifest associated with a recipient.

A21 supplies no production, personalization, manifest generation or delivery, recipient ledger, or physical-camera teaching. Its cumulative-histogram comparisons and sliding-window boundary detection score only `P` against claims 12–13 and 15–16; they are not an express perceptual-hash plus fuzzy-group-matching disclosure. Its cropping/rotation discussion nevertheless weakens any technical-effect position resting only on robust shot-boundary fingerprint retrieval.

## 5. Leading combination pressure

1. **Claims 1 and 4:** A20+B9 with direct multicamera vision-mixer/EDL art. A20 supplies individualized EDL versions, source/time fields, registry, and forensic motivation; B9 supplies user-different switch positions. Producing reference content through an edit list is not treated as the novelty center. The disputed modification is movement of a retained physical-camera transition boundary and—against claim 4—repetition of the complete ordered-transition/noncoincident-timing/different-camera-interval relationship at plural director-commanded cuts.
2. **Claims 6 and 17:** A4/A6/C8+B9 with direct multicamera art, or A20+A4/A6. These routes supply manifests, recipient association, variant sequences, variable switch positions, or individualized versions. Claim 17 additionally requires plural physical-camera timing choices, an affirmative mate timing in the actually delivered manifest, and association of that manifest with the recipient.
3. **Claims 11, 14, 18, and 19; AF parent claim 23:** A4/A6+A13+A21, with A20 or B9 supplying personalization and timing motivation and A5/B6–B8 supplying alternative detection techniques. A21 materially strengthens shot-boundary sequencing and exact database equality. Claims 18–19 and AF claim 23 additionally require the equal delivered manifest to contain an affirmative mate timing and the reconstruction to represent the same detected plural combination.

The claims should not be defended merely by listing missing elements across references. A defensible response must address why the proposed combination would select the claimed physical-camera cut timing as the recipient code, preserve it through manifest assembly, and later reconstruct the delivered manifest rather than a generic fingerprint, with a reasoned motivation and reasonable expectation of success.

## 6. DW-08A and remaining evidence gaps

DW-08A remains the highest-value search. It should expressly cover:

1. personalized multicamera or alternate-angle versions created by moving director or vision-mixer cut boundaries;
2. EDL source-camera/in-point/out-point fields used to generate such versions;
3. manifest or chunk-combination records preserving recipient-specific physical-camera switch timings;
4. recipient ledgers keyed to the actually delivered manifest;
5. scene-change or shot-boundary timing sequences used to reconstruct a manifest rather than only a fingerprint;
6. equality between the reconstruction and a delivered manifest followed by recipient lookup;
7. delivered manifests containing affirmative mate timings and reconstructions representing the same detected plural timing combination;
8. A21 family members, backward/forward citations, cited nonpatent literature, and products implementing duration-sequence fingerprints; and
9. contemporaneous broadcast, sports, live-production, forensic screener, and CDN systems that split production, delivery, and monitoring across actors.

Direct multicamera/vision-mixer art could materially narrow claims 1 and 6. A document coupling A21-like shot-duration fingerprints to a delivery-manifest database could materially narrow claims 11 and 14. Product evidence and nonpatent literature therefore matter alongside patent searching.

## 7. Priority, statutory, and filing caveats

The priority/support map controls the current support posture: claims 1–5 and 6–10 are mode unassigned; claim 1 includes a combined-support gate for producing the reference according to the structured list; claim 4 adds a separate plural complete-relationship gate; claim 5 is PCT-direct but provisional-combined for its full added relationship; claims 11–13 are applicant-assigned Mode A subject to counsel confirmation; claims 14–16 are mode unassigned; claim 17 inherits claim 6 and adds the plural mate-containing recipient-combination gate; claim 18 inherits counsel's disposition of claim 11 and adds a separate causal-nexus gate; and claim 19 inherits claim 14's unassigned method posture and adds the method-form causal-nexus gate. A dependent's direct support does not cure its parent's claim-as-a-whole gate.

B10 becomes potentially relevant principally if counsel assigns Mode B to an affected claim; its present mapping is cumulative or weaker and it does not supply the claimed camera/manifest/reconstruction relationships. A15–A18 and other later materials require source-specific statutory analysis rather than treatment as automatically available prior art.

This matrix does not decide IDS submission, clearance, freedom to operate, continuation entitlement, copendency, parent-versus-continuation placement, restriction, double patenting, § 101, § 112, or direct/induced infringement. AF-CONT claim 19's overlap with AF claim 23 requires a filing-stage retain, differentiate, substitute, or omit decision without bootstrapping either claim's support mode. Re-score upon claim amendment, a DW-08A result, a new canonical source, a priority-mode decision, or authoritative source correction.
