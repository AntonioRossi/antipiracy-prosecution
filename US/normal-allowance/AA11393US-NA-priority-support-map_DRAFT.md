# AA11393US — NA Provisional/PCT Priority and Support Map (DRAFT)

> **STRATEGY NA · CLAIM-SET VERSION NA-2026-07-22-v4 · STATUS 22 JULY 2026**
>
> **INTERNAL COUNSEL ANALYSIS — NOT A LEGAL OPINION OR PRIORITY CONCLUSION.** This map distinguishes PCT support from entitlement to the 26 February 2024 provisional date. Counsel must verify the official records and analyze every selected claim as a whole.

## 1. Sources and grading

| Source | Date | Repository copy |
|---|---:|---|
| US provisional 63/557,868 | 26.02.2024 | `../../PPA2/as filed 63 557868.pdf` |
| PCT/IB2025/051755 | 19.02.2025 | `../../PCT/AA11393US-PCT_RAPPORTO DEPOSITO.pdf` and converted Markdown |
| NA candidate set `NA-2026-07-22-v4` | Internal draft | `AA11393US-NA-US_claim-set_DRAFT.md` |

| Code | Meaning |
|---|---|
| **D** | Direct express passage, claim, table, or concrete example |
| **C** | Contextual support for the architecture or result |
| **CE** | Combined-example relationship |
| **W** | Weak or not express |
| **G** | Counsel determination required |

Direct support for separate operations does not decide possession of their claimed combination. Written description and enablement are separate inquiries. See [MPEP § 2163](https://www.uspto.gov/web/offices/pac/mpep/s2163.html) and [MPEP § 2164](https://www.uspto.gov/web/offices/pac/mpep/s2164.html).

## 2. Independent-claim map

### NA claim 1 — production system

| Limitation | Provisional basis | PCT basis | Grade |
|---|---|---|---|
| Plural-camera input and structured edit list with source cameras and cut time codes | Claim 1(a)–(d); EDL discussion; Example 2 | Claims 1 and 10; EDL discussion; Example 2 | **D** |
| Vary a recorded cut time to produce a mate | Claim 1(e); method claim 10(e); mate-generation discussion | Claims 1, 10, 16–17; mate-generation discussion | **D** |
| Same first-camera-to-second-camera transition at noncoincident timings | Example 2 tables and explanation | Example 2 | **D** for Camera 2→Camera 3; **CE/G** for general breadth |
| Temporally corresponding different-camera frames in the intervening interval | Example 2 extension/delayed commencement | Example 2 | **D/CE/G** |
| Claim 1 as a whole | Claim 1 and Example 2 | Claims 1 and 10; Example 2 | **D/CE/G** |

### NA claim 9 — distribution system

| Limitation | Provisional basis | PCT basis | Grade |
|---|---|---|---|
| Receive reference/mate versions containing the retained transition at different timings | Example 2 | Example 2 | **D/CE/G** |
| Segment versions and generate manifests pointing to chunk combinations | Claim 1(g)–(j); method claim 10(g)–(h); Examples 3–4 | Claims 11–12; Examples 3–4 | **D** |
| Each assembled stream preserves one transition timing | Examples 2–4 read together | Examples 2–4 | **CE/G** |
| Deliver according to manifests and record manifest-recipient associations | Claim 1(i)–(k); method claim 10(h)–(i) | Claims 11–14 and 16–17 | **D** |
| Claim 9 as a whole | Claims 1 and 10; Examples 2–4 | Claims 10–14 and 16–17; Examples 2–4 | **D/CE/G** |

### NA claim 16 — detector system

| Limitation | Provisional basis | PCT basis | Grade |
|---|---|---|---|
| Ledger associates delivered manifests with recipients | Claim 1(k); method claim 10(i) | Claims 14–15; ledger passages | **D** |
| Each delivered manifest identifies a chunk combination selected from a reference/mate ensemble, with each mate having a camera-cut timing different from the corresponding reference timing | Claim 1(e), (g)–(k); method claim 10(e), (g)–(i); Examples 2–4 | Claims 10–14; ensemble, manifest, and mixing passages; Examples 2–4 | **D** |
| Receive suspected unauthorized distribution | Claim 1(l); method claim 10(j) | Claims 15–17; detection component 130 | **D** |
| Scene-change detection identifies a plurality of camera-cut time codes | Claim 1(m); method claim 10(j) | Claim 15; Method 200/claim 17 | **D** |
| Build reconstructed manifests from identified time codes | Claim 1(m); method claim 10(j) | Claim 15; Method 200/claim 17 | **D** |
| Find equal delivered manifest and identify associated recipient | Claim 1(n); method claim 10(k) | Claim 15; Method 200/claim 17 | **D** |
| Claim 16 as a whole | Claim 1(e), (g)–(n) places the reference/mate ensemble, delivered-manifest ledger, and complete detector loop in one system claim | Claims 10–15 place reference/mate chunk combinations, manifest-recipient association, derivation, reconstruction, equality, ledger search, and account identification in one dependent chain | **D; Mode A** |

### NA claim 22 — end-to-end method

| Operation | Provisional basis | PCT basis | Grade |
|---|---|---|---|
| Plural-camera production and mate generation with retained transition at a different timing | Method claim 10(a)–(e); Example 2 | Method 200; claims 16–17; Example 2 | **D/CE** |
| Segment, generate manifests, deliver, and record recipients | Method claim 10(g)–(i); Examples 3–4 | Method 200; claims 16–17; Examples 3–4 | **D/CE** |
| Detect plural suspect cut times and reconstruct manifests | Method claim 10(j) | Method 200; claim 17 | **D** |
| Equal-manifest ledger search and recipient identification | Method claim 10(k) | Method 200; claims 16–17 | **D** |
| Claim 22 as a whole | Method claim 10, with Examples 2–4 supplying the concrete physical-camera and manifest relationships | Method 200 and claims 16–17, with Examples 2–4 | **D/CE; Mode A** |

## 3. Dependent claims

Every dependent inherits its independent's posture. The grade below addresses the added limitation.

| NA claim | Added limitation | Provisional basis | PCT basis | Grade/action |
|---:|---|---|---|---|
| 2 | Later-cut resynchronization | Example 2 | Example 2 | **D/G**; resolve § 4.1 |
| 3 | Ten-frame implementation | Example 2 | Example 2 | **D/G** |
| 4 | EDL label and fields | EDL discussion; Example 2 | EDL discussion; Example 2 | **D** |
| 5 | Live viewpoints/director selections | Pipeline and live-production discussion | Pipeline; claim 10; Method 200 | **D** |
| 6 | Variation at plural director cuts | Claim 1(e); geometric-progression discussion | Claims 16–17; geometric progression | **D** |
| 7 | Retained source-camera identifiers in the varied list | Example 2 tables | Example 2 | **D/CE/G** for general breadth |
| 8 | Overlay | Claim 1(f); method claim 10(f) | Claim 4 and overlay passages | **D** |
| 10 | Adaptive CDN/tailored manifests | Claims 5 and 14; distribution passages | Claim 11 | **D** |
| 11 | Mixing/progressive assignment | Examples 3–4; mixing discussion | Claim 12; Example 4 | **D** |
| 12 | Ledger identifies each recipient/group receiving a manifest | Claim 1(k); method claim 10(i) | Claims 14–15 | **D** |
| 13 | Equal-duration same-interval chunks containing the transition at respective timings | Examples 2–3 | Examples 2–3 | **CE/G** |
| 14 | Unicast | Claim 7; method claim 16 | Distribution description | **D** |
| 15 | Recipient timing-choice sequences across plural regions | Geometric progression; Examples 3–4 | Geometric progression; Examples 3–4 | **D/CE/G** |
| 17 | Perceptual-hash cut-time detection | Claim 3; Example 5 | Claims 2–3; Example 5 | **D** |
| 18 | Sliding-window fuzzy matching | Claim 4; Example 5 | Claim 3; Example 5 | **D** |
| 19 | Equal matched delivered manifest selects a mate chunk spanning the same ordered physical-camera transition at a noncoincident timing, with different-camera frames in the intervening interval | Claims 1(e), (g)–(n); Examples 2–4 | Claims 10–15; Examples 2–4 | **D/CE/G**; separately disclosed physical-camera, chunk/manifest, equality, and lookup features require a combined-example determination |
| 20 | Recipient timing combination across plural cuts represented by reconstructed manifest | Geometric progression, manifest, ledger, and detector passages | Examples 3–5; claims 11–15 | **D/CE/G**; inherits claim 19's matched-manifest physical-camera gate |
| 21 | Manifest-sequence probabilistic contributor identification | Collusion passages read with manifest ledger | Collusion passages and claims 11–15 | **C/CE/G** |
| 23 | Later-cut resynchronization | Example 2; method claim 10 | Example 2; Method 200 | **D/G** |
| 24 | Each manifest preserves reference or mate timing at the varied transition | Examples 2–4 | Examples 2–4 | **D/CE/G** |
| 25 | Paired same-interval chunks contain transition at respective timings | Examples 2–3 | Examples 2–3 | **CE/G** |
| 26 | Perceptual-hash sliding-window detection | Claims 3–4; Example 5 | Claims 2–3; Example 5 | **D** |
| 27 | Unicast | Claim 7; method claim 16 | Distribution description | **D** |
| 28 | Manifest-sequence collusion contributor output | Collusion passages and claim 6 | Claim 5 and collusion passages | **C/CE/G** |
| 29 | Plural varied cuts and recipient timing combinations | Claim 10(e); geometric progression; Examples 3–4 | Method 200; claim 17; Examples 3–4 | **D/CE/G** |
| 30 | Overlay before segmentation | Method claim 10(f)–(g) | Claim 17 and pipeline passages | **D/C/G** |

## 4. Mandatory determinations

### 4.1 Example 2

The provisional table and corrective text restore Cut 4 at `00:00:30:01`; the same paragraph contains a stray `00:00:30:11` “mistake” sentence. PCT Example 2 uses `00:00:30:01`. Obtain a written determination before materially relying on NA claims 2–3 or 23.

### 4.2 Production and distribution integration

The remaining limitation-specific determinations are:

1. the generalized same ordered first-camera-to-second-camera transition and different-camera interval in NA claim 1;
2. the retained source-camera identifiers in NA claim 7;
3. the Examples 2→3→4 relationship in NA claims 9, 13, 15, 24–25, and 29; and
4. the matched equal delivered manifest's mate chunk and physical-camera transition geometry in NA claim 19; and
5. the plural recipient timing combination represented by the reconstructed manifest in NA claim 20, including its inheritance of NA claim 19.

### 4.3 Collusion and pipeline order

Confirm the manifest-sequence probabilistic input and respective-portion contributor output in NA claims 21 and 28, and overlay before segmentation in NA claim 30.

### 4.4 DW-05A modes and B10

| Mode | Required conclusion | Consequence |
|---|---|---|
| **A** | PCT and provisional each satisfy written description and enablement for the claim as a whole | Subject to other requirements, 26.02.2024 benefit may apply; B10 is not prior art merely by its 02.12.2024 publication date |
| **B** | PCT satisfies both requirements, but provisional benefit fails | Effective date is no earlier than 19.02.2025 absent other valid benefit; B10 becomes potentially citable subject to complete statutory analysis |
| **C** | PCT fails written description, enablement, or both | Do not rely on the formulation as drafted |

B10 remains low-materiality and cumulative-or-weaker. It lacks plural cameras, physical-camera edit boundaries, scene-change-derived manifest reconstruction, and the complete claimed chains.

The current applicant assessment assigns NA claims 16 and 22 to **Mode A**. B10's 2 December 2024 publication therefore does not enter the prior-art set for those claims merely by publication date. This assignment does not decide B10's statutory posture for a different claim that ultimately receives a later effective date.

## 5. Current filing posture

| NA claims | Support posture | Treatment |
|---|---|---|
| 1, 9 | Direct component operations with **D/CE/G** strengthened relationships | Obtain written claim-as-a-whole PCT/provisional determinations |
| 16, 22 | Complete operative chains supported in the provisional and PCT; **Mode A** | Principal detector and end-to-end candidates; retain eligibility, actor, proof, and art review |
| 2–3, 23 | Direct mechanics with provisional inconsistency | Use only after written determination |
| 4–6, 8, 10–12, 14, 17–18, 26–27 | Added limitations direct | Ordinary wording, breadth, antecedent, and inherited-parent review |
| 7, 13, 15, 19–21, 24–25, 28–30 | Added relationship direct/contextual/combined-example as stated above | Retain only with the recorded gate |
