# AA11393US — AF Actor-Focused Continuation Priority and Support Map (DRAFT)

> **STRATEGY AF-CONT · CLAIM-SET VERSION AF-CONT-2026-07-22-v2 · STATUS 23 JULY 2026**
>
> **INTERNAL COUNSEL ANALYSIS — NOT A LEGAL OPINION — NOT FILED. CONTINUATION STATUS: NOT YET PRESERVED.** This map addresses the candidate claims in [`AA11393US-AF-CONT-US_claim-set_DRAFT.md`](AA11393US-AF-CONT-US_claim-set_DRAFT.md). It does not establish copendency, a benefit relationship, provisional entitlement, or filing approval.

## 1. Sources and classifications

| Source | Date / status | Repository copy |
|---|---:|---|
| US provisional 63/557,868 | 26.02.2024 | `../../PPA2/as filed 63 557868.pdf` |
| PCT/IB2025/051755 | 19.02.2025 | `../../PCT/AA11393US-PCT_RAPPORTO DEPOSITO.pdf` and converted Markdown |
| AF-CONT candidate | Internal draft; no filing date | `AA11393US-AF-CONT-US_claim-set_DRAFT.md` |

| Code | Meaning |
|---|---|
| **D** | Direct express passage, claim, table, or concrete example |
| **C** | Contextual support for the architecture or result |
| **CE** | Combined-example relationship |
| **G** | Counsel determination required |

Every independent and dependent claim requires a claim-as-a-whole conclusion. Written description and enablement are separate inquiries in the PCT and provisional. A dependent inherits its parent's posture; direct support for its added limitation does not cure a parent defect.

## 2. Independent claims

### AF-CONT claim 1 — production system

| Limitation | Provisional basis | PCT basis | Current posture |
|---|---|---|---|
| Plural-camera input and structured edit list with source cameras and cut time codes | Claim 1(a)–(d), method claim 10(a)–(d), EDL discussion, and Example 2 | Claims 1 and 10, EDL discussion, and Example 2 | **D** |
| Produce reference content according to the original structured list | Pipeline-management and structured-list recording claims and passages, EDL reconstruction/automation discussion, and Example 2 | Claims 1 and 10, pipeline/structured-list/EDL passages, and Example 2 | **C/CE/G.** Reference production and structured-list use are disclosed; confirm their exact causal relationship in each filing |
| Vary a recorded cut time and produce a mate | Claim 1(e), method claim 10(e), and mate-generation discussion | Claims 1, 10, and 16–17 and mate-generation discussion | **D** |
| Same first-camera-to-second-camera transition at noncoincident timings | Example 2 tables and explanation | Example 2 | **D** for Camera 2→Camera 3; **CE/G** for general breadth |
| Temporally corresponding different-camera frames in the intervening interval | Example 2 extension and delayed commencement | Example 2 | **D/CE/G** |
| Claim as a whole | Claim 1 and Example 2 | Claims 1 and 10 and Example 2 | **D/CE/G; mode unassigned** |

### AF-CONT claim 6 — distribution system

| Limitation | Provisional basis | PCT basis | Current posture |
|---|---|---|---|
| Receive reference/mate versions containing retained transition at different timings | Example 2 | Example 2 | **D/CE/G** |
| Segment versions and generate manifests pointing to chunk combinations | Claim 1(g)–(j), method claim 10(g)–(h), and Examples 3–4 | Claims 11–12 and Examples 3–4 | **D** |
| Each assembled stream preserves one transition timing | Examples 2–4 read together | Examples 2–4 | **CE/G** |
| Deliver according to manifests and record manifest-recipient associations | Claim 1(i)–(k) and method claim 10(h)–(i) | Claims 11–14 and 16–17 | **D** |
| Claim as a whole | Claims 1 and 10 and Examples 2–4 | Claims 10–14 and 16–17 and Examples 2–4 | **D/CE/G; mode unassigned** |

### AF-CONT claim 11 — detector system

| Limitation | Provisional basis | PCT basis | Current posture |
|---|---|---|---|
| Ledger associates delivered reference/mate chunk-combination manifests with recipients; each mate has a cut-timing difference | Claim 1(e), (g)–(k), method claim 10(e), (g)–(i), and Examples 2–4 | Claims 10–14, ensemble/manifest passages, and Examples 2–4 | **D** |
| Receive suspect and identify plural camera-cut time codes using scene-change detection | Claim 1(l)–(m) and method claim 10(j) | Claim 15, Method 200, and claim 17 | **D** |
| Build reconstructed manifests from identified time codes | Claim 1(m) and method claim 10(j) | Claim 15, Method 200, and claim 17 | **D** |
| Find equal delivered manifest and identify its recipient | Claim 1(n) and method claim 10(k) | Claim 15, Method 200, and claim 17 | **D** |
| Claim as a whole | Claim 1(e), (g)–(n) | Claims 10–15 | Applicant-assigned **Mode A** by correspondence to NA claim 16; counsel confirmation required |

### AF-CONT claim 14 — detector-only reconstructed-manifest method

| Operation | Provisional basis | PCT basis | Current posture |
|---|---|---|---|
| Receive suspected unauthorized distribution | Method claim 10(j); system claim 1(l) | Method 200/claims 16–17; claim 15 | **D** |
| Apply scene-change detection and identify plural camera-cut time codes | Method claim 10(j); system claim 1(m) | Claim 15 and Method 200/claim 17 | **D** |
| Build reconstructed manifests from identified time codes | Method claim 10(j); system claim 1(m) | Claim 15 and Method 200/claim 17 | **D** |
| Search delivered-manifest/recipient ledger for an equal manifest to identify the recipient | Method claim 10(k), read with method claim 10(e), (g)–(i) and system claim 1(e), (g)–(k), (n) | Claims 10–15 and Method 200/claims 16–17 | **D/CE/G** for the method-form delivered-manifest environment |
| Claim as a whole | Method claim 10(j)–(k), read with the manifest/ledger steps and system claim 1 | Method 200/claims 16–17, read with claims 10–15 | **D/G; mode unassigned** |

The detector-only method is a subset of the disclosed complete method chain, but that observation does not assign an effective date. Counsel must determine whether each filing conveys possession and enablement of the affirmative method together with its delivered reference/mate manifest environment and whether the environment limits the intended monitoring actor's method as drafted.

AF parent claim 23 combines AF-CONT claim 14's detector-only base with AF-CONT claim 19's causal nexus. AF claim 23 and AF-CONT claim 14 require separate claim-as-a-whole mode assignments even where their base-method conclusions are consistent; neither inherits NA claim 16's or AF-CONT claim 11's system-format Mode A posture. The causal-nexus conclusion must be consistent across AF claim 23 and AF-CONT claim 19 unless the controlling language differs at filing.

Across AF-CONT claims 11, 14, 18, and 19, the reconstruction operation is disclosed more clearly as a required result than as a detailed noise-tolerant algorithm. Counsel must separately determine full-scope enablement and any § 112(f) consequence. The same claim set must use a consistent supported construction of an “equal” manifest file and address whether equality means byte identity, equivalent chunk selections, or equivalent represented timing choices when URLs, tokens, or metadata differ.

## 3. Dependent claims

| AF-CONT claim | Added limitation | Provisional basis | PCT basis | Added-limitation posture |
|---:|---|---|---|---|
| 2 | EDL label and source/in/out-point fields | EDL discussion and Example 2 | EDL discussion and Example 2 | **D** |
| 3 | Live viewpoints and director-commanded selections | Claims 1(a)–(d), method claim 10(a)–(d), and pipeline discussion | Claim 10, Method 200, and pipeline discussion | **D** |
| 4 | Complete retained ordered-transition/noncoincident-timing/different-camera interval relationship at each of plural director cuts | Claim 1(e), method claim 11, Example 2, and geometric-progression discussion | Claims 16–17, Example 2, and geometric-progression discussion | **D/CE/G** for applying the complete Example 2 relationship at each plural cut |
| 5 | Element absent from the reference before overlay; overlay onto both reference and mate | Claims 1(f), 8, and method claim 10(f), read together | Claim 4 and the passage stating both the overlay-on-both relationship and absence from the reference | **C/CE/G** in the provisional; **D** in the PCT; determine each filing separately |
| 7 | Adaptive CDN and tailored manifests | Claims 5 and 14 and distribution passages | Claim 11 | **D** |
| 8 | Mixing and progressive assignment | Examples 3–4 and mixing discussion | Claim 12 and Example 4 | **D** |
| 9 | Ledger identifies recipient/group receiving each manifest | Claim 1(k) and method claim 10(i) | Claims 14–15 | **D** |
| 10 | Unicast | Claim 7 and method claim 16 | Distribution description and claim 6 | **D** |
| 12 | Perceptual-hash cut-time detection | Claim 3, method claim 12, and comparison discussion | Claims 2 and 17 and Example 5 | **D** |
| 13 | Sliding-window fuzzy matching | Claim 4, method claim 13, and comparison discussion | Claim 3 and Example 5 | **D** |
| 15 | Method-form perceptual-hash detection | Method claim 12 and comparison discussion | Claims 2 and 17 and Example 5 | **D** |
| 16 | Method-form sliding-window fuzzy matching | Method claim 13 and comparison discussion | Claim 3 and Example 5 | **D** |
| 17 | Plural physical-camera timing-choice combinations; delivered recipient manifest contains an affirmative mate timing; record associates that manifest with the recipient | Geometric-progression, manifest-combination, and recipient-record passages; claims 1(g)–(k) and 10(g)–(i), read with Example 2 | Examples 2–4; claims 11–14 and 16–17 | **D/CE/G** for the complete physical-camera timing-choice → delivered mate-containing manifest → recipient-association relationship; inherits claim 6 |
| 18 | Equal delivered manifest contains an affirmative mate timing and the reconstructed manifest represents the same detected combination | Geometric-progression, manifest-combination, ledger, and reconstruction passages; claims 1(g)–(n) and 10(g)–(k) | Examples 3–5; claims 11–17 and Method 200 | **D/CE/G** for the delivered mate-containing combination → reconstruction of the same detected combination; inherits claim 11 but does not inherit its Mode A label automatically for the added relationship |
| 19 | Affirmative method counterpart of claim 18 | Method claim 10(g)–(k), read with claim 1(g)–(n) and the geometric-progression passages | Method 200 and claims 11–17, read with Examples 3–5 | **D/CE/G** for the added causal nexus; inherits claim 14's unassigned method posture |

## 4. DW-05A and intervening-art control

| Mode | Required counsel conclusion | Operative consequence |
|---|---|---|
| **A** | PCT and provisional each satisfy written description and enablement for the claim as a whole | Subject to other requirements, the claim may rely on 26.02.2024; B10 is not prior art merely by its 02.12.2024 publication date |
| **B** | PCT satisfies both requirements, but provisional benefit fails | Effective date is no earlier than 19.02.2025 absent another valid benefit; reassess B10 and every intervening item before approval |
| **C** | PCT fails written description, enablement, or both | Do not rely on the claim as drafted; copendency cannot repair the disclosure defect |

Current applicant assignments and open gates are:

| AF-CONT claims | Current mode / gate |
|---|---|
| 1–5 | Mode unassigned; claim 1's reference-production/structured-list relationship and production generalization gates control; claim 4 adds a separate plural complete-relationship gate; claim 5 requires separate provisional/PCT treatment |
| 6–10 | Mode unassigned; claim 6 Examples 2→3→4 integration gate controls |
| 11–13 | Applicant-assigned Mode A by correspondence to NA claim 16; counsel must confirm separately |
| 14–16 | Mode unassigned; detector-only affirmative-method and delivered-manifest-environment gate controls |
| 17 | Mode unassigned; inherits claim 6 and adds the plural mate-containing recipient-combination gate |
| 18 | Inherits counsel's disposition of claim 11; added causal nexus remains **D/CE/G** and requires a separate determination |
| 19 | Mode unassigned; inherits claim 14 and adds the method-form causal-nexus gate |

Parent-versus-continuation placement, parent claim status, restriction history, claim differentiation, double patenting, and terminal-disclaimer consequences control whether AF-CONT claim 19 remains in a filed successor as an overlapping backup to AF claim 23.

B10 remains low-materiality and cumulative-or-weaker because it lacks plural cameras, physical-camera edit boundaries, delivered reference/mate chunk-combination manifests, scene-change-derived manifest reconstruction, and equal-delivered-manifest lookup. Its chronology becomes potentially relevant to any claim assigned Mode B.

## 5. Filing control

The shared [`continuation-preservation memo`](../common/AA11393US-continuation-preservation_MEMO.md) controls the successor vehicle, copendency, ownership, docketing, filing evidence, benefit verification, recursive preservation, and chain closure. This map controls the AF claim 23/AF-CONT claim 19 support and overlap analysis but is not CONT-05 completion evidence. Until the memo's conditions are satisfied, the operative status remains **NOT YET PRESERVED**.
