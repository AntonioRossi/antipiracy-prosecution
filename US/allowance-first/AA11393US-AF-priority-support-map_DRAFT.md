# AA11393US — AF Allowance-First Provisional/PCT Priority and Support Map (DRAFT)

> **STRATEGY AF · CLAIM-SET VERSION AF-2026-07-22-v6 · STATUS 22 JULY 2026**
>
> **INTERNAL COUNSEL ANALYSIS — NOT A LEGAL OPINION OR A PRIORITY CONCLUSION.** This map distinguishes support in PCT/IB2025/051755 as filed from entitlement to the 26 February 2024 filing date of US provisional 63/557,868. Counsel must verify the official file wrappers and analyze each claim as a whole.
>
> **INITIAL-CONTACT STATUS.** The applicant's limitation-level assessment is complete for controlled transmission. No counsel opinion is represented as obtained. DW-05A remains a pre-filing and reliance control.

## 1. Sources and citation convention

| Source | Date / status | Repository copy | Function |
|---|---:|---|---|
| US provisional 63/557,868 | 26.02.2024 | `../../PPA2/as filed 63 557868.pdf` | Earliest claimed benefit source |
| PCT/IB2025/051755 | 19.02.2025 | `../../PCT/AA11393US-PCT_RAPPORTO DEPOSITO.pdf` and converted Markdown | As-filed international disclosure and claims |
| AF candidate set `AF-2026-07-22-v6` | Internal draft; not a filing date | `AA11393US-AF-US_claim-set_DRAFT.md` | Proposed US wording; not a support source |

Page citations are repository bundle-PDF pages, not printed specification pages. The PCT has no numbered paragraphs. Counsel must confirm citations against the official USPTO and WIPO records.

## 2. Support classifications and legal boundary

| Code | Meaning |
|---|---|
| **D — direct** | Express passage, claim, table, or concrete example supports the stated feature. |
| **C — contextual** | The architecture or result is disclosed, but the precise proposed relationship is contextual. |
| **CE — combined-example** | The limitation requires reading disclosed examples or embodiments together. |
| **W — weak/not express** | The reviewed filing does not expressly state the operation or detail. |
| **G — gate** | A material support, generalization, priority, or consistency issue requires counsel determination. |

A direct grade for component operations does not decide written description for the claim as a whole. Written description asks whether the filing conveys possession of the claimed combination; enablement is a separate full-scope inquiry. Neither conclusion establishes the other. See [MPEP § 2163](https://www.uspto.gov/web/offices/pac/mpep/s2163.html) and [MPEP § 2164](https://www.uspto.gov/web/offices/pac/mpep/s2164.html).

## 3. AF claim 1 — limitation-level system map

The provisional places the complete basic recovery loop in one claim. Provisional claim 1(a)–(e) recites plural cameras, a production pipeline, recorded cut timings and transitions, and programmed cut-time variations; claim 1(g)–(k) recites ensemble segmentation, manifest combinations, and the manifest-recipient ledger; and claim 1(l)–(n) recites pirate-stream monitoring, cut-time derivation, reconstructed-manifest matching, and account identification. Provisional method claim 10 states the corresponding sequence. PCT claims 1 and 10–17 and Method 200 provide parallel system and method support, with PCT claim 15 expressly reciting devised cut time codes, one or more reconstructed manifests, equality to delivered manifests, and ledger lookup.

| AF claim 1 limitation | Provisional basis | PCT basis | Classification and action |
|---|---|---|---|
| Processor/memory system | Computing and server implementation, PDF pp. 24–25 and 35–36; system claim 1 | Computing environment, PDF p. 25; claims 8–9 | **D.** Review § 112(f), algorithm sufficiency, and single-system attribution. |
| Receive plural-camera video | Pipeline, pp. 15–16 and 20–25; claim 1(a)–(b) | General system, pp. 19–21; claims 1 and 10 | **D.** |
| For plural director cuts, successive edit entries identify first/second source cameras and out/in-point time codes | EDL discussion, pp. 20–26; Example 2 tables, pp. 26–27, identify source camera, in-point, and out-point | List/EDL discussion, pp. 20–24; Example 2, pp. 40–42; claim 10 | **D** for the concrete fields and camera order; **CE/G** for the generalized first/second-camera formulation across plural cuts. |
| Produce reference content according to the structured list | Pipeline and EDL discussion, pp. 15 and 20–24; claim 1 | General production and list discussion, pp. 19–24; claims 1 and 10 | **D/C.** |
| Generate one or more mates by modifying out/in-point times at plural selected cuts while retaining source-camera identifiers and order | Claim 1(e) varies the time code of any cut; method claim 10(e) varies time codes of camera cuts; Example 2 retains Camera 2→Camera 3 while moving the boundary | Mate-generation passages, pp. 19–25; Example 2, pp. 40–42; claims 1, 10, and 16–17 | **D** for plural cut-time variation and the concrete retained Camera 2→Camera 3 boundary; **CE/G** for the generalized retained-pair operation at each selected cut. |
| Reference transition and later mate transition; first-camera selection extended and second begins later | Example 2 tables and explanation, pp. 26–27 | Example 2, pp. 40–42 | **D** for the illustrated ten-frame operation; **CE/G** for general breadth. The independent claims do not require later resynchronization. |
| Segment reference/mate ensemble into chunks | Claim 1(g); method claim 10(g) | Distribution passages, pp. 21–27; claims 11–12 and 17 | **D.** |
| Generate manifests pointing to respective reference/mate chunk combinations | Claim 1(h)–(j); method claim 10(g)–(h); Examples 3–4 | Claims 11–12; Examples 3–4, pp. 42–47 | **D** for manifest combinations; **CE/G** for the complete relationship to the plural retained physical-camera boundaries. |
| Deliver according to respective manifests and store manifest-recipient associations in a ledger | Claim 1(i)–(k); method claim 10(h)–(i) | Claims 11–14 and 16–17; ledger passages, pp. 21–22 | **D.** |
| Receive suspected unauthorized distribution | Claim 1(l); method claim 10(j) | General detection, pp. 19–22; claims 1 and 15–17 | **D.** |
| Scene-change detection identifies a plurality of camera-cut time codes | Claim 1(m): algorithm devises “the time codes of the camera cuts”; method claim 10(j): identify “camera cut time codes” | Component 130/algorithm 131; Example 5; claim 15; Method 200/claim 17 | **D.** No suspect-side physical-camera labeling is required. |
| Build one or more reconstructed manifests from the plurality of identified time codes | Claim 1(m) and method claim 10(j) expressly connect detected cut time codes to manifest reconstruction | Claim 15 expressly builds one or more reconstructed manifests from devised time codes; claim 17 states the same method step | **D** for the operation; **D/CE/G** for its relationship to the particular plural production variations in the complete claim. |
| Search ledger for recipient associated with an equal delivered manifest | Claim 1(n) expressly searches for the spectator receiving a manifest equal to the reconstructed manifest; method claim 10(k) | Claim 15 and Method 200/claim 17 expressly recite equality, ledger search, and account identification | **D.** |
| AF claim 1 as a complete chain | Provisional claim 1 recites production, manifest delivery/recording, cut-time reconstruction, equality, and recipient identification in one system claim | PCT claim 1 supplies the general integrated system; claims 10–15 supply the concrete production/distribution/recovery chain | **D/CE/G.** The overall loop is direct. Counsel must decide the plural retained-camera-boundary-to-reconstructed-manifest relationship as a whole. |

## 4. AF method claims

### 4.1 AF claims 19–22 — integrated method map

Provisional method claim 10 directly recites the production-to-attribution sequence. PCT Method 200 and claims 16–17 directly recite management, camera-cut recording and variation, segmentation, manifest generation and distribution, ledger recording, scene-change/time-code detection, reconstructed-manifest building, and account identification.

| AF claim 19 operation | Provisional basis | PCT basis | Classification and action |
|---|---|---|---|
| Receive plural-camera video and the structured edit list | Method claim 10(a)–(d), pp. 43–44; EDL passages and Example 2 | Method 200; claims 16–17; Example 2 | **D** for capture, cut recording, and concrete fields; **CE/G** for generalized successive first/second-camera entries across plural cuts. |
| Produce reference and generate mates by plural retained-camera-boundary variations | Method claim 10(e), read with Example 2 and plural-cut description | Method 200 programming step; claims 16–17; Example 2 | **D/CE/G** on the same basis as AF claim 1. |
| Segment, generate manifests, deliver, and record manifest-recipient associations | Method claim 10(g)–(i); Examples 3–4 | Method 200; claims 16–17; Examples 3–4 | **D** for the operations; **CE/G** for their complete relationship to the plural retained boundaries. |
| Receive suspect, identify plural cut time codes, and build reconstructed manifests | Method claim 10(j) | Method 200 monitoring step; claim 17 | **D.** |
| Search ledger for recipient associated with an equal delivered manifest | Method claim 10(k) | Method 200 searching step; claims 16–17 | **D.** |
| AF claim 19 as a complete method | Provisional method claim 10 | Method 200 and claims 16–17 | **D/CE/G.** Obtain a separate claim-as-a-whole opinion; system-format support does not itself establish method support. |

AF claims 20–22 provide two method branches beneath AF claim 19. AF claim 20 supplies the causal-nexus fallback. AF claims 21–22 form a separate detection-implementation chain so they do not inherit AF claim 20's relationship-specific gate. Each inherits AF claim 19's complete-method posture.

| AF claim | Added method limitation | Provisional basis | PCT basis | Grade and action |
|---:|---|---|---|---|
| 20 | Delivered recipient timing-choice combination includes at least one mate timing; reconstructed manifest represents the same detected timing-choice combination | Geometric-progression, manifest-combination, ledger, and reconstruction passages; claims 1(g)–(n) and 10(g)–(k) | Examples 3–5; claims 11–17; Method 200 | **D/CE/G.** The operations and plural choice architecture are disclosed; confirm the exact delivered recipient-combination → affirmative mate choice → reconstruction of the same detected combination relationship. Inherits AF claim 19. |
| 21 | Perceptual-hash comparison for plural cut-time identification | Provisional claim 3; detection discussion and Example 5 | Example 5; detection description | **D.** Direct implementation support; depends separately from and inherits AF claim 19, not AF claim 20. |
| 22 | Sliding-window fuzzy matching of perceptual-hash groups | Provisional claim 4; Example 5 discussion | Example 5 | **D.** Direct implementation support; inherits AF claims 21 and 19, not AF claim 20. |

### 4.2 AF claim 23 — monitor-side reconstructed-manifest method

AF claim 23 combines the affirmative detector-only method environment with the mate-containing delivered-combination-to-reconstructed-combination nexus. It does not inherit AF claim 19's integrated-method mode or the applicant-assigned Mode A posture of system-format NA claim 16 or AF-CONT claim 11.

| AF claim 23 operation or relationship | Provisional basis | PCT basis | Classification and action |
|---|---|---|---|
| Receive the suspected unauthorized distribution | Method claim 10(j); system claim 1(l) | Method 200/claims 16–17; claim 15 | **D.** |
| Apply scene-change detection and identify plural camera-cut time codes | Method claim 10(j); system claim 1(m) | Claim 15 and Method 200/claim 17 | **D.** No suspect-side physical-camera labeling is required. |
| Build reconstructed manifests, including one representing a detected plural timing combination | Method claim 10(j), read with the geometric-progression and reconstruction passages | Claim 15 and Method 200/claim 17, read with Examples 3–5 | **D** for reconstruction from identified cut time codes; **D/CE/G** for representation of the same plural timing combination used in the mate-containing delivered-manifest relationship. |
| Search a delivered-manifest/recipient ledger for an equal manifest to identify the recipient | Method claim 10(k), read with method claim 10(e), (g)–(i) and system claim 1(e), (g)–(k), (n) | Claims 10–15 and Method 200/claims 16–17 | **D/CE/G** for the affirmative method together with the passive delivered-manifest environment. Determine who performs the search-to-identify operation and, if performers are split, whether the other conduct is legally attributable to one entity under the applicable method-claim standard. |
| Delivered manifests identify reference/mate chunk combinations; each represents plural reference/mate timing choices | Claims 1(e), (g)–(k) and 10(e), (g)–(i), read with Examples 2–4 and the geometric-progression passages | Claims 10–14 and 16–17, read with Examples 2–4 | **D/CE/G.** Confirm the complete method-environment relationship rather than treating system-format disclosure as automatically sufficient. |
| Equal delivered manifest contains an affirmative mate timing and matches the detected combination represented by the reconstruction | Claims 1(g)–(n) and 10(g)–(k), read with the geometric-progression, manifest-combination, ledger, and reconstruction passages | Examples 3–5; claims 11–17; Method 200 | **D/CE/G.** Confirm the delivered mate-containing combination → reconstruction of the same detected combination nexus. |
| AF claim 23 as a whole | Method claim 10(j)–(k), read with claims 1(e), (g)–(n), 10(e), (g)–(i), and Examples 2–4 | Method 200 and claims 15–17, read with claims 10–14 and Examples 2–5 | **D/CE/G; mode unassigned.** Determine written description and enablement in each filing, effective date, limiting effect of the passive environment, equality construction, actor performance, eligibility, and art as a whole. |

The reconstruction operation is disclosed more clearly as a required result than as a detailed noise-tolerant algorithm. Counsel must determine full-scope enablement and any § 112(f) consequence. The claim set must use a supported construction of an “equal” manifest file—such as byte identity, equivalent chunk selections, or equivalent represented timing choices—and address dynamic URLs, tokens, and metadata.

## 5. AF dependent claims

Every system dependent inherits AF claim 1's claim-as-a-whole posture. The grades below address the added limitation. AF claims 20–22 are mapped with the method family in § 4; AF claim 23 is independently mapped there.

| AF claim | Added limitation | Provisional basis | PCT basis | Grade and action |
|---:|---|---|---|---|
| 2 | Preserve later reference cut timing and restore synchronization | Example 2, pp. 26–27 | Example 2, pp. 41–42 | **D/G.** Resolve the provisional inconsistency in § 6.2. |
| 3 | Ten-frame extension/shortening and resynchronization | Example 2, pp. 26–27 | Example 2, pp. 40–42 | **D/G.** Inherits AF claim 2's gate. |
| 4 | Structured list is an EDL | EDL discussion and Example 2 | EDL discussion and Example 2 | **D.** |
| 5 | Live viewpoints and director-commanded switching | Pipeline discussion; claims 1(a)–(d), 10(a)–(d) | General system; claim 10; Method 200 | **D.** |
| 6 | Respective single-cut mate for each selected cut | Single variation at any cut, geometric progression discussion, and Examples 2–4 | Mate-generation and geometric-progression discussion; Examples 2–4 | **D/C/G.** Confirm the respective-mate/only-one-selected-cut relationship. |
| 7 | Perceptual-hash cut-time detection | Provisional claim 3; detection discussion and Example 5 | Example 5; detection description | **D.** |
| 8 | Sliding-window fuzzy hash matching | Provisional claim 4; Example 5 discussion | Example 5 | **D.** |
| 9 | Adaptive CDN and tailored manifests | Provisional claims 1(g)–(j), 5 and method claims 10(g)–(h), 14 | PCT claim 11 and distribution description | **D.** |
| 10 | Reference/mate chunk mixing and progressive assignment | Mixing and progressive user-manifest mapping passages; Examples 3–4 | PCT claim 12; Example 4 | **D.** |
| 11 | Mixed-version suspect and probabilistic analysis of recipient-associated manifest sequences | Collusion/Tardos discussion read with manifest-recipient ledger | Collusion/Tardos discussion read with claims 11–15 | **C/CE/G.** Mixed-copy tracing is disclosed; confirm manifest chunk-selection sequences as the algorithm input and respective-portion output. |
| 12 | Segmented Tardos and at least one portion-specific contributor | Segmented/collusion discussion and provisional claim 6 | PCT collusion discussion and claim 6 | **D/C/G.** Confirm the exact segment/fingerprint/portion/contributor relationship. |
| 13 | Equal-duration reference/mate chunks for the same playback interval | Example 3 | Example 3, pp. 42–45 | **D.** |
| 14 | Each paired chunk contains the retained transition at its respective timing | Example 2 read with Example 3 | Examples 2–3 | **CE/G.** The exact chunk-internal boundary geometry is not stated in one passage. |
| 15 | Blockchain registration/readout | Blockchain passages at PDF pp. 18 and 35 | PCT blockchain passage and claim 13 | **D.** |
| 16 | Unicast | Provisional claim 7 and method claim 16 | Distribution description | **D.** |
| 17 | Recipient-associated reference/mate timing choices across plural cuts | Geometric progression, manifest combinations, and ledger passages | Geometric progression and Examples 3–4 | **D/CE/G.** Confirm the exact combination represented by each delivered manifest. |
| 18 | Additional elements overlaid before segmentation | Provisional claim 1(f) followed by claim 1(g); method claim 10(f)–(g) | Overlay and segmentation passages; claims 5 and 17 | **D** in the provisional claim sequence; **D/C** in PCT. |

## 6. Mandatory gates

### 6.1 Claim-as-a-whole plural-cut integration — AF claims 1 and 19–22

The basic production-to-reconstruction loop is express in provisional claims 1 and 10 and in the PCT system/method disclosure. The remaining written-description question is whether each filing conveys the strengthened claim relationship in which:

1. physical source-camera identifiers and order are retained while out/in-point time codes are changed at a plurality of selected director-commanded cuts;
2. delivered manifest combinations embody reference/mate choices produced by those plural changes; and
3. plural cut time codes detected in the suspect are used to reconstruct the delivered manifest that identifies the recipient.

The source files disclose each stage and place the overall loop in single claims. Example 2 supplies the physical-camera boundary; Examples 3–4 connect varied cuts to chunks and manifests; and the detection claims connect plural cut time codes to reconstructed-manifest equality. The exact strengthened relationship is nevertheless a claim-as-a-whole **D/CE/G** determination, not an automatic consequence of direct support for each stage.

### 6.2 Example 2 resynchronization inconsistency — AF claims 2–3

The provisional mate table restores Cut 4 at `00:00:30:01`, and the explanatory sentence states that the synchronization is restored at the next cut. The same provisional paragraph also contains a stray `00:00:30:11` “mistake” sentence. PCT Example 2 uses `00:00:30:01` and omits the stray value. Counsel must determine written description, enablement, benefit entitlement, and whether the PCT text is a permissible clarification before AF claims 2–3 are filed or used materially.

### 6.3 Production-boundary generalization

Example 2 directly shows Camera 2 followed by Camera 3, the corresponding out/in-point fields, retention of their order, extension of Camera 2, and delayed commencement of Camera 3. Claims and description authorize variation of the time codes of camera cuts generally and at plural cuts. Counsel must determine whether the filing conveys the claimed first/second-source-camera formulation for each of a plurality of selected director-commanded cuts and the exact paired out-point/in-point modification.

### 6.4 Examples 2→3→4 and dependent relationships

| Relationship | Posture | Required determination |
|---|---|---|
| Retained physical-camera boundary → reference/mate chunks → manifest combinations | **D/CE/G** | Whether the examples convey the claimed complete production-to-manifest relationship across plural selected cuts |
| Equal-duration same-interval chunks | **D** | Ordinary breadth and antecedent review |
| Each paired chunk straddles the retained transition at its own timing | **CE/G** | AF claim 14's exact chunk geometry |
| Recipient-associated timing choices across plural cuts | **D/CE/G** | AF claim 17's manifest representation and ledger association |
| Delivered mate-containing recipient combination → reconstructed same detected timing-choice combination | **D/CE/G** | AF claim 20's inherited integrated-method fallback and AF claim 23's independent monitor-side causal nexus |
| Manifest sequence as probabilistic collusion input | **C/CE/G** | AF claim 11's exact input and respective-contribution output |

### 6.5 Monitor-side method — AF claim 23

AF claim 23 is a detector-only subset of the disclosed complete method chain, but the subset observation does not assign an effective date. The individual suspect-acquisition, cut-time detection, reconstruction, equality, and search-to-identify operations are direct. The method-form delivered-manifest environment and the mate-containing delivered-combination-to-reconstructed-same-combination nexus are **D/CE/G**, and the claim as a whole is **D/CE/G; mode unassigned**. Counsel must determine whether each filing conveys possession and enablement of the affirmative method together with that passive environment, whether the environment receives limiting effect, and whether one monitoring entity performs every affirmative operation or another performer's conduct is legally attributable to that entity under the applicable method-claim standard. AF claim 23 inherits neither NA claim 16's system-format Mode A assignment nor AF claim 19's integrated-method mode.

### 6.6 DW-05A modes and B10

Counsel must assign AF claims 1, 19, and 23 separately; AF claims 20–22 inherit claim 19's effective-date mode and add the separately graded limitations stated above:

| Mode | Required conclusion | Consequence |
|---|---|---|
| **A** | PCT and provisional each satisfy written description and enablement for the claim as a whole | Subject to other requirements, the claim may rely on 26.02.2024; B10's 02.12.2024 publication is not prior art merely by that date. |
| **B** | PCT satisfies both requirements, but the provisional fails at least one requirement for benefit entitlement | The effective date is no earlier than 19.02.2025 absent another valid benefit claim; B10 becomes potentially citable under § 102(a)(1), subject to complete statutory and exception analysis. |
| **C** | PCT fails written description, enablement, or both | The formulation has a current-disclosure defect independent of priority; it must not be relied on as drafted. |

B10 remains assessed as low-materiality and cumulative-or-weaker: it lacks plural cameras, a source-camera edit list, plural moved cut boundaries, manifest reconstruction from detected cut time codes, and the complete ledger-equality chain. Its chronology matters principally in Mode B; its present substance does not control the art assessment.

## 7. Claim-level filing posture

| AF claims | Present support posture | Filing treatment |
|---|---|---|
| 1 | Direct closed loop; **D/CE/G** for plural retained-camera-boundary-to-reconstructed-manifest integration | Principal AF system candidate; obtain a written claim-as-a-whole PCT/provisional opinion |
| 19 | Direct method loop; same **D/CE/G** integration | Complementary method candidate; obtain a separate opinion and § 101/performance review |
| 20 | Disclosed components; **D/CE/G** for the affirmative mate-containing delivered combination and reconstruction of the same detected combination | Principal causal-nexus method fallback; obtain a written relationship-specific support determination and inherit AF claim 19's review |
| 21–22 | Direct perceptual-hash and sliding-window method limitations; inherit AF claim 19 without AF claim 20 | Support-safe detection branch; ordinary wording and antecedent review plus inherited claim-as-a-whole, eligibility, performance, and art review |
| 23 | Direct individual recovery operations; **D/CE/G; mode unassigned** for the method-form delivered-manifest environment and mate-containing delivered-combination-to-reconstructed-same-combination nexus as a whole | Monitor-side independent candidate; obtain a separate claim-as-a-whole PCT/provisional written-description and enablement determination, effective-date mode, equality construction, actor, eligibility, restriction, proof, and art review |
| 2–3 | Direct mechanics with provisional inconsistency | Use only after written counsel determination |
| 4–5, 7–10, 13, 15–16 | Added limitations direct | Ordinary wording, breadth, antecedent, and inherited-parent review |
| 6, 11–12, 14, 17–18 | Added relationship direct/contextual/combined-example as specified above | Retain as expressly gated dependents; do not describe the added relationship as unqualified direct support |

## 8. Pending counsel determinations

1. Verify the provisional and PCT repository copies against the official records.
2. For AF claims 1, 19, and 23 separately, conclude PCT written description, PCT enablement, provisional written description and enablement for benefit entitlement, effective date, and DW-05A mode; apply AF claim 19's result to dependent AF claims 20–22 while separately confirming their added limitations. Do not transfer a system-format or integrated-method mode to AF claim 23.
3. Decide the claim-as-a-whole plural retained-boundary/manifest/reconstruction relationship.
4. Decide the first/second-source-camera and plural selected-cut generalization.
5. Resolve the provisional Example 2 inconsistency for AF claims 2–3.
6. Confirm AF claim 6's respective single-cut mate relationship.
7. Confirm AF claims 11–12's manifest-sequence and segmented-Tardos contribution relationships.
8. Confirm AF claim 14's paired-chunk geometry, AF claim 17's plural manifest choices, and AF claim 18's pipeline order.
9. Decide AF claim 20's affirmative mate-containing delivered-combination-to-reconstructed-combination relationship and confirm that AF claims 21–22 remain independent of that gate.
10. Determine AF claim 23's method-form delivered-manifest environment, mate-containing delivered-combination-to-reconstructed-same-combination nexus, equality construction, full-scope reconstruction enablement, and affirmative-operation performer or legally attributable performance.
11. Review § 112(f), definiteness, restriction, divided infringement, territorial performance, and proof independently of this map; AF claims 20–22 do not cure AF claim 19's performance-attribution risk, and AF claim 23 targets only the production/delivery actor split where one entity performs the complete recovery method or the remaining conduct is legally attributable to that entity under the applicable method-claim standard.
12. For AF claim 23, identify the asserted exception under Step 2A Prong One, analyze practical application under Step 2A Prong Two, analyze the additional elements individually and as an ordered combination under Step 2B, and identify specification support and evidence for any asserted technical improvement. The passive manifest/ledger environment and mate-timing nexus do not alone resolve eligibility.
13. Preserve the NA actor-focused claims as a portfolio option; adequate AF support does not resolve actor or proof limitations.

## 9. Intervening-information trigger

B10 (KR 2024-0168593 A) has a 2 December 2024 laid-open publication inside the provisional-to-PCT interval. If any information with a potentially relevant effective date after 26 February 2024 and before 19 February 2025 is identified, or if an Office questions priority, counsel must reassess claim-specific benefit entitlement, applicable disclosure duties, the art set, and every material priority or support representation.
