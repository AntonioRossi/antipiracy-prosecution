# AA11393US — AF Allowance-First Provisional/PCT Priority and Support Map (DRAFT)

> **STRATEGY AF · CLAIM-SET VERSION AF-2026-07-17-v2 · STATUS 17 JULY 2026**
>
> **INTERNAL COUNSEL ANALYSIS — NOT A LEGAL OPINION OR A PRIORITY CONCLUSION.** This map addresses the AF candidate claims in `AA11393US-AF-US_claim-set_DRAFT.md`. It distinguishes support in PCT/IB2025/051755 as filed from entitlement to the 26 February 2024 filing date of US provisional 63/557,868. Counsel must verify the official file wrappers and analyze each claim as a whole under the governing law.
>
> **INITIAL-CONTACT STATUS.** This map records the applicant's present limitation-level assessment and is complete for applicant-controlled initial transmission to prospective or retained US counsel under the package-handling controls. No counsel opinion is represented as already obtained. The pending determinations below are pre-filing and reliance controls—not prerequisites to delivering this decision package for advice.

## 1. Sources and citation convention

| Source | Date / status | Repository copy | Function in this map |
|---|---:|---|---|
| US provisional 63/557,868 | 26.02.2024 | `../../PPA2/as filed 63 557868.pdf` | Earliest claimed benefit source |
| PCT/IB2025/051755 | 19.02.2025 | `../../PCT/AA11393US-PCT_RAPPORTO DEPOSITO.pdf` and converted Markdown | As-filed international disclosure and claim set |
| AF candidate set `AF-2026-07-17-v2` | Internal draft dated 17.07.2026; not a filing date | `AA11393US-AF-US_claim-set_DRAFT.md` | Proposed US allowance-first wording; not itself a support source |

Page citations are **repository bundle-PDF pages**, not printed specification pages. The as-filed PCT has no numbered paragraphs. PCT references therefore use PDF pages, paragraph subjects, Examples 1–5, and as-filed claims. Provisional references use PDF pages. Counsel should confirm every citation against the official USPTO and WIPO records.

## 2. Support classifications

| Code | Meaning | Permitted use in this map |
|---|---|---|
| **D — direct** | The feature is stated expressly in one passage, claim, table, or concrete example. | Direct support for the stated feature, not automatically for its full breadth or its combination with other features. |
| **C — contextual** | The architecture, component, or result is disclosed, but the proposed operational relationship is not stated. | Corroborating context only; not a substitute for written description of the claimed relationship. |
| **CE — combined-example** | The proposed limitation requires reading disclosed examples or embodiments together. | Counsel must decide whether the filing conveys the combination as possessed; separate disclosure of parts is insufficient by itself. |
| **W — weak/not express** | The proposed operation or detail has not been located expressly in the reviewed filing. | Do not characterize as settled support; rewrite, omit, or retain only after a reasoned counsel determination. |
| **G — express gate** | A material support, generalization, priority, or internal-consistency issue remains. | The feature may be presented to counsel for advice, but do not file it or rely on it materially until the identified counsel review is completed. |

Combinations such as **D/CE/G** mean that the component operations are express, but the claimed integration remains a gated combined-example position.

## 3. AF claim 1 — limitation-level system map

AF claim 1's general production-to-recipient-attribution architecture is unusually well anchored. Provisional system claim 1 at PDF pp. 42–43 and provisional method claim 10 at pp. 43–44 recite cameras, production, cut-time variation, manifest delivery, recipient recording, pirate-copy cut-time detection, reconstructed-manifest matching, and account identification in a single claim. The PCT's general system passage at PDF pp. 19–20 and PCT claim 1 at pp. 50–51 likewise combine mate generation, delivery, association, suspect analysis, version matching, and recipient lookup.

The principal support issue is narrower and patentability-critical: neither filing expressly states that the stored candidate difference, suspect detection, and match all concern the **same candidate-distinguishing region** and that the match jointly requires both the **ordered camera-source pair** and the **switch timing**. That relationship is deliberately assembled from Example 2, the delivered-version record, the detection passages/Example 5, and recipient lookup. It is graded **CE/G**, not direct, below.

| AF claim 1 limitation | Provisional basis | PCT basis | Classification and required action |
|---|---|---|---|
| Processor-and-memory system executing the recited operations | Computing and server implementation at PDF pp. 24–25 and 35–36; provisional system claim 1, pp. 42–43 | Computing environment at PDF p. 25; PCT claims 8–9 at p. 51 | **D** for generic implementation. Counsel must still review § 112(f), algorithm sufficiency, and whether one claimed system performs or controls all functions. |
| Receive video from plural cameras | Summary/detailed pipeline at pp. 15–16 and 20–25; provisional claim 1(a)–(b), p. 42; provisional method claim 10(a)–(b), pp. 43–44 | General system and detailed embodiment, pp. 19–21; PCT claims 1, 10, and 16, pp. 50–54 | **D.** |
| Structured list of edit instructions identifies source-camera identifiers and recorded cut time codes | EDL discussion at pp. 20–26; Example 2 reference/mate tables at pp. 26–27 expressly list source camera, in-point, and out-point; provisional claims 1(d)–(e) and 10(d)–(e), pp. 42–44 | EDL/list description at pp. 20–24; Example 2, pp. 40–42; PCT claim 10, pp. 51–52, and PCT method claims 16–17, pp. 53–54 | **D** for the concrete list fields and cut-time recording. |
| Produce reference content according to the structured list | Pipeline summary at p. 15; EDL discussion at pp. 20–24; provisional claims 1 and 10, pp. 42–44 | General system at pp. 19–21; EDL discussion at pp. 23–24; PCT claims 1, 10, and 16–17 | **D/C.** Reference creation and the EDL are express; “according to” is a drafting relationship supported by the EDL's stated editing function. |
| Generate mate by varying the recorded time of a selected cut comprising an ordered first-camera-to-second-camera transition while retaining that transition | Mate-generation passages at pp. 15, 24–27, and 42–44; Example 2 retains Camera 2 followed by Camera 3 while moving the boundary from `00:00:20:01` to `00:00:20:11` | Mate-generation passages at pp. 19–21 and 25; Example 2 Tables 1–2, pp. 40–41; PCT claims 1, 10, and 16–17 | **D for the concrete Camera 2→Camera 3 example; CE/G for generalized first/second-camera wording.** Counsel must confirm that the general ordered-pair formulation is a supported abstraction. |
| Reference transition at `tR`, mate transition at different `tM` | Example 2 reference and mate EDLs, pp. 26–27 | Example 2, pp. 40–42 | **D for the shown times; CE/G for generalization.** |
| During the interval between `tR` and `tM`, reference and mate contain temporally corresponding frames from different cameras | Example 2 tables, pp. 26–27: after the reference changes to Camera 3, the mate continues Camera 2 for the intervening ten frames | Same Example 2 tables, pp. 40–41 | **Concrete-table inference/G.** “Temporally corresponding frames” is not verbatim. Counsel must confirm the synchronized-feed inference and breadth. That inference is a proposed disclosure basis, not an additional synchronization limitation in AF claim 1. |
| Define a candidate-distinguishing temporal region including the interval | Altered-cut and fingerprint discussion at pp. 27–28 and 36–41 | Altered-cut, distinguishing-version, and comparison discussion at pp. 19–23, 27–30, and 47–49 | **C/CE/G.** The named region is a claim-drafting construct used to tie later operations to the actual inter-version difference; no passage uses this term. |
| Deliver generated versions including reference and mate versions to respective recipients | Licensor/licensee and distribution passages at pp. 18, 27–35, and 40–41; provisional claims 1(g)–(k) and 10(g)–(i), pp. 43–44 | Generic delivery in the system passage at p. 19; detailed distribution at pp. 21–27; PCT claims 1 and 11–14, pp. 50 and 52–53 | **D/C.** Delivery of distinguishable versions is direct. The express requirement that the delivered set include both a reference version and a mate version is consistent with the ensemble/distribution architecture but should be confirmed as a claim relationship. |
| For each delivered version, generate a candidate pattern from the source identifiers and switch timing actually present at the distinguishing region | Example 2 source/timing tables, pp. 26–27; unique cut-sequence/fingerprint and delivery-record discussion at pp. 31–41 | Example 2, pp. 40–42; version/manifest fingerprint and association discussion at pp. 21–27 and 45–47 | **CE/G.** Version/cut fingerprints and recipient associations are disclosed, but no passage expressly derives and stores an ordered-source-pair-plus-timing pattern for each delivered version. |
| Store an association among the delivered version, candidate pattern, and recipient | Ledger and user-manifest association passages at pp. 15, 18, and 31–35; provisional claim 1(k), p. 43; provisional method claim 10(i), p. 44 | Generic version-recipient record at pp. 19–20 and PCT claim 1, p. 50; manifest ledger at pp. 21–22 and PCT claim 14, p. 52 | **D** for delivered version/manifest-to-recipient association; **CE/G** for storing the newly formulated source-transition pattern in the same association. |
| Receive and analyze suspected unauthorized content | Detection discussion at pp. 15 and 34–38; provisional claims 1(l)–(m) and 10(j), pp. 43–44 | General system at pp. 19–20; detailed detection at pp. 21–22; PCT claims 1 and 15–17, pp. 50 and 53–54 | **D.** |
| Detect, at the same candidate-distinguishing region, an ordered transition between source identities and its timing | Generic scene-change/cut-time detection at pp. 15 and 34–37; Example 2 source identities at pp. 26–27; comparison of altered cuts at pp. 36–37 | Cut-time detection at pp. 19–21 and PCT claims 1 and 15; Example 2 at pp. 40–42; Example 5 at pp. 47–49 | **CE/G.** Cut-time detection is direct. Detection of both camera identities on the two sides, at the same region that stored the inter-version difference, is not express and is a material counsel gate. |
| Derive a detected pattern identifying both source sides and timing | Same combined passages as the preceding row | Same combined passages; PCT claim 15 directly derives time codes but not source identities | **CE/G.** Do not treat generic scene-change or time-code detection as direct support for source-identity recovery. |
| Identify a candidate only when both ordered source pair and timing jointly match at that same region | Timing/fingerprint comparison and ledger narrative at pp. 34–41, read with Example 2 | PCT claim 1 version matching and PCT claim 15 manifest matching, read with Example 2 and Example 5 | **CE/G.** Direct matching is to a version or reconstructed manifest. The claimed two-field, same-region joint match is not express. |
| Search the association record and identify the recipient linked to the matched candidate/version | Ledger/retrieval passages at pp. 15 and 34–35; provisional claim 1(k)–(n), pp. 43; provisional method claim 10(i)–(k), p. 44 | General system at pp. 19–20; detailed ledger/retrieval at pp. 21–22; PCT claims 1 and 14–15, pp. 50 and 52–53 | **D** for record search and recipient identification; **CE/G** for using the newly formulated joint source/time match as the search key. |
| AF claim 1 as a complete operational chain | Provisional system claim 1 and method claim 10 directly disclose the overall closed loop, pp. 42–44 | PCT general system passage, pp. 19–20; PCT claim 1, pp. 50–51; detailed embodiment, pp. 20–22 | **D/CE/G.** The general closed loop is direct. The novelty-carrying same-region source-pair/timing relationships require combined-example review. |

## 4. AF claim 20 — limitation-level method map

AF claim 20 is not treated as supported merely because its substantive limitations mirror AF claim 1. The method is mapped independently to provisional method claim 10 and the PCT method disclosure. Those sources directly place capture/management, cut recording and variation, delivery, recipient recording, monitoring, and searching in one method. The same patentability-critical refinements as AF claim 1—the named distinguishing region, recovery of both source identities, and a joint source-order/timing match—remain **CE/G** in method form.

| AF claim 20 method limitation | Provisional method basis | PCT method basis | Classification and required action |
|---|---|---|---|
| Receive plural-camera video and a structured list of edit instructions containing source identifiers and recorded cut times | Method claim 10(a)–(d), pp. 43–44, read with the EDL passages and Example 2 tables at pp. 20–27 | Method 200 capture/management/camera-cut-recording steps; PCT claims 16–17, pp. 53–54; Example 2, pp. 40–42 | **D** for plural-camera capture, receipt, recorded cuts/transitions, and the concrete EDL fields. |
| Produce reference content according to the structured list | Method claim 10(a)–(e), pp. 43–44; pipeline and EDL passages at pp. 15 and 20–24 | Method 200 management/programming steps; PCT claims 16–17; general production description | **D/C.** Reference production and the list's editing role are express; the proposed “according to” relationship is contextual drafting. |
| Generate a mate by varying the recorded time of a selected cut comprising an ordered first-camera-to-second-camera transition while retaining that transition | Method claim 10(e), p. 44, read with Example 2 at pp. 26–27 | Method 200 programming step and PCT claims 16–17, pp. 53–54, read with Example 2, pp. 40–42 | **D for the concrete Camera 2→Camera 3 example; CE/G for generalized first/second-camera wording.** |
| Place the retained transition at noncoincident reference and mate timings and provide the intervening alternate-camera frames | Example 2 reference/mate tables, pp. 26–27 | Example 2 reference/mate tables, pp. 40–42, read with the method 200 programming step | **D** for the shown noncoincident timings; **concrete-table inference/G** for “temporally corresponding frames” and its generalized breadth. The synchronized-feed inference is a proposed disclosure basis, not an extra AF claim 20 step. |
| Define a candidate-distinguishing temporal region containing the interval | Altered-cut/fingerprint discussion at pp. 27–28 and 36–41, read with method claim 10 | Altered-cut and comparison discussion, including Example 5, read with method 200 | **C/CE/G.** The named region is a drafting construct that connects the disclosed method steps; it is not express terminology. |
| Deliver generated versions including a reference version and a mate version to respective recipients | Method claim 10(h), p. 44; distribution passages at pp. 27–35 | Method 200 distribution step; PCT claim 16, p. 53; detailed distribution description | **D/C.** Distribution of distinguishable mates/versions is direct; counsel should confirm the express requirement that both reference and mate versions occur in the delivered set. |
| For each delivered version, generate the claimed candidate source-transition pattern from the source identities and timing actually present at the region | Example 2 and unique cut-sequence/fingerprint discussion, pp. 26–27 and 31–41, read with method claim 10 | Example 2 and version/manifest-fingerprint discussion, read with method 200 and PCT claims 16–17 | **CE/G.** No method passage expressly derives the complete ordered-source-pair-plus-timing pattern for each delivered version. |
| Store the delivered-version/candidate-pattern/recipient association | Method claim 10(i), p. 44; ledger and delivery-record passages at pp. 31–35 | Method 200 recording/ledger-recording step; PCT claims 16–17, pp. 53–54 | **D** for recording delivery or a manifest against a recipient; **CE/G** for including the newly formulated candidate source-transition pattern in that association. |
| Receive the suspected unauthorized distribution and detect, at the same region, an ordered transition between source identities and its timing | Method claim 10(j), p. 44; detection passages at pp. 34–38, read with Example 2 | Method 200 monitoring step; PCT claims 16–17; Example 5, read with Example 2 | **D** for monitoring/detecting scene changes and timings; **CE/G** for receipt and detection of both source identities at the same stored distinguishing region. |
| Derive a detected pattern identifying both source sides and timing | Method claim 10(j) and timing/fingerprint passages, read with Example 2 | Method 200 monitoring step and PCT claim 17's devised time codes/reconstructed manifest, read with Examples 2 and 5 | **CE/G.** Time-code derivation is direct; the ordered-source-pair-plus-timing object is not express. |
| Select a candidate only when both source order and timing jointly match at that same region | Method claim 10(j)–(k) and comparison/search narrative, read with Example 2 | Method 200 monitoring/searching steps and PCT claims 16–17, read with Examples 2 and 5 | **CE/G.** Direct matching concerns scene changes, a version, or a reconstructed manifest; the proposed two-field same-region test requires combined-example review. |
| Search the association record and identify the linked recipient | Method claim 10(i)–(k), p. 44 | Method 200 recording and searching steps; PCT claims 16–17, pp. 53–54 | **D** for the search and recipient-identification result; **CE/G** for using the newly formulated joint source/time pattern as the search key. |
| AF claim 20 as a complete method chain | Provisional method claim 10 directly recites the production-to-recipient-identification method, pp. 43–44 | Method 200 narrative and Figure 4; PCT claims 16–17, pp. 53–54 | **D/CE/G.** The overall method loop is direct. The same-region source-pair/timing relationships are not made direct by restating the chain in method form. Obtain a claim-as-a-whole opinion independently of AF claim 1. |

## 5. AF dependent claims — claim-by-claim map

Every dependent claim inherits all AF claim 1 gates. The classification below concerns the **added limitation**, not the inherited claim as a whole.

| AF claim | Added limitation | Provisional basis | PCT basis | Classification and counsel action |
|---:|---|---|---|---|
| 2 | Preserve a later reference cut time and restore synchronization from that cut onward | Example 2 table and explanation, pp. 26–27 | Example 2, pp. 41–42, states that Cut 4 begins at the reference time with no delay | **D/G.** The provisional contains the internal inconsistency detailed in § 6.1. Obtain a written priority/support view before filing or relying on AF claim 2. |
| 3 | `tM` ten frames later; first selection extended ten frames; following selection shortened; later resynchronization | Example 2 reference/mate tables and explanation, pp. 26–27 | Example 2, pp. 40–42 | **D/G.** The ten-frame mechanics are express, but AF claim 3 inherits the AF claim 2 inconsistency gate. |
| 4 | EDL with source camera, in-point, and out-point for plural cuts | Example 2 tables, pp. 26–27; general EDL discussion, pp. 20–25 | EDL discussion, pp. 23–24; Example 2, pp. 40–42 | **D.** |
| 5 | Live diverse viewpoints and director-commanded real-time camera selection | Summary/detailed pipeline, pp. 15–16 and 20–26; provisional claim 1(a)–(d), p. 42 | Detailed pipeline, pp. 20–24; Example 1, pp. 38–40; PCT claim 10, pp. 51–52 | **D.** |
| 6 | Vary plural director-commanded cuts; define and store patterns at plural regions | Variation of any cut at pp. 25–26; repeated generation at pp. 30–33; provisional method claim 11, p. 44 | Repeated/successive cut discussion at pp. 22–23; Example 4, pp. 45–47; PCT claim 12, p. 52 | **D** for applying variations at plural cuts; **CE/G** for generating AF claim 1's ordered-source/timing pattern at every respective region. |
| 7 | Detect transition/timing by perceptual-hash frame comparison | Automated comparison at pp. 36–37; provisional claims 3 and 12, pp. 43–44 | Example 5, pp. 47–49; PCT claim 2, p. 50 | **D** for perceptual-hash comparison; **CE/G** for using it to recover both camera identities and the transition timing required by AF claim 1. |
| 8 | Fuzzy comparison of perceptual hashes of frame groups using sliding windows | PDF p. 37; provisional claims 4 and 13, pp. 43–44 | Example 5, p. 48; PCT claim 3, p. 51 | **D** for the sliding-window technique; inherits AF claim 7's source-identity gate. |
| 9 | Manifest-based delivery/association; derive time code and build reconstructed manifest | Manifest delivery/association at pp. 15, 28–35, and 42–44; time-code derivation/reconstruction at pp. 15 and 34–37 and provisional claim 1(m), p. 43 | Manifest delivery/association at pp. 21–27 and PCT claims 11–14; time-code derivation/reconstruction at pp. 21 and 37 and PCT claim 15, p. 53 | **D** for manifest delivery, association, derived time code, and reconstructed manifest. Association of each manifest with AF claim 1's newly formulated candidate source-transition pattern is **CE/G**. |
| 10 | Ledger associates delivered manifests/accounts and is searched for a matching reconstructed manifest | Ledger/retrieval at pp. 15 and 34–35; provisional claim 1(k)–(n), p. 43 | Ledger/retrieval at pp. 21–22 and 37; PCT claims 14–15, pp. 52–53 | **D.** |
| 11 | Mixed-version suspect; apply probabilistic analysis to recipient-associated candidate camera-source-transition patterns; positively identify recipients whose delivered versions contributed respective portions | Colluding Redistribution discussion at pp. 38–41 states that mixed-copy segments remain traceable and accounts involved can be identified; provisional claims 6 and 15, pp. 43–44 | Collusion discussion at pp. 30–34; PCT claim 5, p. 51 | **D/CE/G.** Mixed copies, probabilistic/Tardos handling, and positive source-account identification are disclosed at the functional-result level. Applying the algorithm specifically to AF claim 1's newly formulated recipient-associated candidate source-transition patterns is combined-example support. |
| 12 | Segmented Tardos fingerprints applied to content segments, with positive identification of a contributor for a respective portion | Segmented Tardos discussion at p. 39; collusion/account-identification discussion at pp. 38–41; provisional claims 6 and 15, pp. 43–44 | Segmented Tardos and collusion discussion at pp. 30–34; PCT claim 5, p. 51 | **D/C.** Segmented Tardos codes and positive colluder identification are express. Counsel should confirm the exact relationship between a fingerprinted segment, a suspect portion, and the identified contributing recipient. |
| 13 | Segment reference/mate; manifests select combinations preserving `tR` or `tM`; deliver assembled streams; store manifest/pattern/recipient association | Distribution machinery at pp. 15 and 28–35 and provisional claim 1(g)–(k), pp. 42–43, read with Example 2 at pp. 26–27 | Distribution machinery at pp. 21–27; Examples 3–4, pp. 43–47; PCT claims 11–14, pp. 52–53, read with Example 2, pp. 40–42 | **D** for chunks, manifests, delivery, and associations; **CE/G** for requiring each assembled stream to preserve the specific ordered transition at `tR` or `tM`. The Examples 2→3→4 linkage is signposted but not stated in the exact AF relationship. |
| 14 | Different manifests select equal-duration chunks spanning the same playback interval, and each chunk straddles its respective transition | Equal-duration corresponding manifest positions at pp. 28–30, read with moved boundary at pp. 26–27 | Example 3 equal-duration reference/mate chunks, pp. 43–45, read with Example 2, pp. 40–42 | **CE/G.** No single passage states that each paired chunk contains frames on both sides of its respective internal transition between identified cameras. Keep only as a counsel-gated fallback. |
| 15 | CDN adaptive delivery; manifests tailored to device/network conditions | Summary at p. 15; adaptive delivery at pp. 19–20 and 28–30; provisional claim 1(g)–(i) and provisional claim 5, p. 43 | Detailed embodiment at pp. 21–22; PCT claim 11, p. 52 | **D.** |
| 16 | Mix reference/mate chunks and progressively assign individualized manifests as more cuts become available | Mixing and progressive assignment at pp. 31–34 | Mixing component at pp. 25–27; Example 4, pp. 45–47; PCT claim 12, p. 52 | **D.** |
| 17 | Unicast respective streams | Summary at p. 16; provisional claims 7 and 16, pp. 43–44 | Distribution embodiment at p. 34; PCT claim 6, p. 51 | **D.** |
| 18 | Recipient-associated manifest choices at plural distinguishing regions between reference/mate timings for ordered source transitions | Repeated cut variations and unique cut sequences at pp. 30–33 and 40–41, read with Example 2, pp. 26–27 | Repeated/successive cut variations at pp. 22–23 and Example 4, pp. 45–47, read with Example 2, pp. 40–42 | **C/CE/G.** Plural variations and sequences are express. The ordered-source-pair/noncoincident-timing relationship at each region is generalized from one concrete Example 2 transition. |
| 19 | Overlay additional elements onto reference/mate before segmentation | Overlay/pipeline summary at p. 15; provisional claim 1(f) before segmentation element (g), p. 43; provisional method claim 10(f) before segmentation element (g), pp. 43–44 | Overlay discussion at p. 31; PCT claim 4, p. 51, read with PCT segmentation claim 11; method architecture | **D/C.** Overlay and segmentation are express; the stated pipeline sequence has direct provisional claim ordering and contextual PCT support. Counsel should preserve a less sequence-specific alternative if PCT support is disputed. |

## 6. Mandatory support and priority gates

### 6.1 Example 2 resynchronization inconsistency — AF claims 2–3

At provisional PDF pp. 26–27:

- the mate EDL table places Cut 4 at `00:00:30:01` and labels it adjusted to the reference;
- the explanatory bullet first states `00:00:30:11`, calls that value a mistake in the alignment attempt, and then says the correct approach is `00:00:30:01`, just like the reference and with no delay; and
- the PCT Example 2 presents the corrected resynchronization without the stray value.

The correct rule therefore appears in the provisional table and corrective text. That does not establish an automatic loss of priority, but the inconsistency prevents an unqualified support conclusion. Until counsel provides a claim-specific written view on what a skilled reader would understand and whether the PCT wording is permissible clarification rather than new matter:

1. keep resynchronization out of AF claims 1 and 20;
2. retain AF claims 2–3 only as expressly gated dependents; and
3. do not make resynchronization the sole basis of a material patentability representation.

### 6.2 Source-identity and same-region detection — AF claims 1, 20, and 7–10

Generic scene-change detection, camera-cut timing analysis, time-code derivation, reconstructed-manifest matching, and recipient lookup are direct. The following are not stated with the same specificity:

1. detecting the identities of both cameras on the respective sides of the suspect transition;
2. performing that detection at the same region where delivered versions were known to differ;
3. deriving the proposed ordered-source-pair-plus-time pattern; and
4. requiring both ordered source pair and timing to match before lookup.

This is the most important support gate for both AF independent claims. The limitation may be strategically justified against the art, but patentability value cannot substitute for written-description support. Counsel should consider whether the as-filed disclosure conveys source identity through EDL-referenced camera frames and the Example 5 visual comparison, and should preserve support-safer system and method alternatives keyed to cut timing/version or reconstructed-manifest matching if not.

### 6.3 Examples 2–5 integration — AF claims 1, 20, 7–10, and 13–18

The relative combined-example positions are:

| Combined disclosure | Relative support posture | Reason |
|---|---|---|
| Example 2 → Examples 3–4: moved boundary to manifest/chunk selection | Stronger **CE**, still gated | Example 3 expressly says a different mate chunk reflects the delayed third cut; Example 4 applies EDL cut variations before generating and assigning manifests. The exact `tR`/`tM` preservation language is not verbatim. |
| Example 2 → Example 5: moved boundary to same-region source-pair detection | Materially weaker **CE** | Example 5 compares reference/mate frames and discusses timing and characteristics of altered cuts, but never expressly recovers camera identifiers on both sides or defines the joint source/time match. |
| Example 2 → Example 3: each paired same-interval chunk straddles its own transition | Weakest manifest **CE** | Equal duration and different corresponding chunks are direct; the claimed internal boundary geometry of both chunks is not. |

Counsel must evaluate each claimed integration as a whole for both PCT support and provisional priority. Do not infer that because Examples 2–5 appear in one specification every recombination is automatically disclosed.

### 6.4 Collusion wording — AF claims 11–12

The filings expressly discuss colluders mixing copies or segments, probabilistic/Tardos fingerprinting, segmented Tardos codes, tracing individual portions, and identifying implicated source accounts. AF claims 11–12 therefore preserve positive contributor identification and a segmented Tardos implementation. Counsel should still confirm applying the algorithm to AF claim 1's newly formulated recipient-associated candidate source-transition patterns and the exact respective-portion relationship as integrated operations.

An earlier attribution-score formulation was not carried into this AF set because this review located no express score computation in either as-filed source. Do not reintroduce score language without identifying and recording an adequate support basis.

### 6.5 Pre-counsel support-safer contingency paths

The preferred AF proposal remains the structural chain recited by AF claims 1 and 20. The following paths are prepared now so that the initial package gives counsel concrete alternatives if a combined-example or generalization position is rejected. They are drafting directions, not claims approved for filing, and none is represented as equally strong against the reviewed art.

| Trigger in the support review | Prepared support-safer direction | Patentability, coverage, and control consequence |
|---|---|---|
| The candidate/detected source-transition object or the same-region joint source/time match is not adequately conveyed | Retain the multi-camera production structure and delivered-version/recipient association, but replace suspect-side source-identity recovery with the directly disclosed route: derive a cut time code, build or identify a reconstructed manifest or delivered version, match that object, and search the recipient ledger. Provisional claims 1(m)–(n) and 10(j)–(k), and PCT claim 15/Method 200, are the principal starting sources. | Loses the two-field ordered-source identity distinction and requires fresh scoring, especially against A4, A6, B6, B8, and B9. Do not present generic timing or reconstructed-manifest recovery as the existing AF novelty center. |
| The Examples 2→3→4 integration is not adequately conveyed | Separate the concrete production-boundary, manifest/distribution, and detection/lookup operations into the applicable NA actor-focused families rather than deleting connective limitations while continuing to label the result an integrated AF claim. | Preserves claim-specific direct relationships and actor coverage but changes the allowance and infringement architecture. Re-map support and art claim by claim. |
| The Examples 2→5 route does not support recovery of both camera identities | Retain the same ordered camera transition, noncoincident reference/mate timings, and intervening different-camera frames on the production side; use direct cut-time/version or reconstructed-manifest recovery on the suspect side, or select the supportable NA production/distribution families. | Keeps the strongest disclosed production structure but weakens the recovery-side distinction. Generic timing recovery cannot carry patentability by itself. |
| AF claim 14's paired-chunk geometry is not adequately conveyed | Omit AF claim 14 rather than rely on equal duration and a common playback interval alone. | A4, B9, and C8 give those packaging features little independent patentability value. |
| AF claim 19's before-segmentation order is not adequately conveyed | Remove that ordering or retain a sequence-neutral overlay fallback, then recheck dependency, support, and art. | Preserves overlay coverage without overstating pipeline order; overlay remains an implementation feature, not the novelty center. |

Any path that removes the same ordered source pair, noncoincident reference/mate timings, intervening different-camera frames, or operationally linked recipient recovery is a new claim strategy—not a harmless AF wording change. Assign a new version, perform a limitation-level support review, and rescore both matrices before treating it as a filing candidate.

## 7. Claim-level filing posture

This is a drafting triage, not a legal conclusion.

| AF claims | Present support posture before counsel review | Filing treatment |
|---|---|---|
| 1 | Direct overall closed-loop architecture; CE/G for source-pair pattern generation, same-region source-identity detection, and joint source/time match | Preserve as the allowance-first patentability candidate, but prepare a support-safer alternative and obtain a claim-as-a-whole opinion |
| 20 | Direct overall method loop in provisional method claim 10 and PCT method 200/claims 16–17; the same CE/G refinements as AF claim 1 | Include as the complementary method independent in the complete proposal; obtain a separate claim-as-a-whole opinion and permit counsel to omit it at filing if a one-independent posture is selected. No AF claim as drafted depends from AF claim 20. Counsel may narrow or amend it or add supported method dependents in the parent under the applicable controls; the continuation reservation separately carries broader and intermediate candidates. |
| 2–3 | Direct concrete Example 2 mechanics with an internal provisional inconsistency | Dependent only; written priority/support determination required |
| 4–5 | Direct | Ordinary wording/antecedent review |
| 6 | Direct plural variation; CE/G for AF claim 1 pattern structure at every region | Retain with combined-example warning |
| 7–8 | Direct comparison algorithms; CE/G for using them to recover the full AF claim 1 source/timing structure | Retain as implementation fallbacks, not independent novelty propositions |
| 9–10 | Direct manifest reconstruction and ledger lookup; CE/G only where tied to AF claim 1's new pattern object | Strong narrow implementation fallbacks subject to inherited AF claim 1 gate |
| 11 | Functional-result support for mixed-copy tracing and positive account identification; CE/G for applying the algorithm to AF claim 1's recipient-associated candidate source-transition patterns | Retain; confirm the combined-example pattern-input and delivered-version/portion formulation |
| 12 | Segmented Tardos implementation and positive identification are express; exact portion-to-contributor relationship merits wording review | Retain as a known implementation fallback, not an independent novelty proposition |
| 13 | Direct distribution machinery; CE/G for preserving the specific ordered transition at `tR`/`tM` | Retain as a combined Examples 2–4 fallback |
| 14 | CE/G; exact boundary-spanning geometry not express in one passage | Keep only as an expressly gated, narrow fallback |
| 15–17 | Direct added limitations | Ordinary wording/antecedent review; inherited AF claim 1/AF claim 13 gates remain |
| 18 | CE/G for the ordered-pair/timing relationship across plural regions | Retain only with generalization review |
| 19 | Overlay direct; exact before-segmentation sequence strongest in provisional claim order | Retain; preserve a sequence-neutral alternative if needed |

## 8. Pending counsel determinations after initial transmission

These requested determinations are intentionally pending. Their absence does not make this initial decision package incomplete or prevent its controlled transmission for advice. They must be resolved, to the extent implicated, before counsel approves filed language, makes a material support or priority representation, or recommends broader wording.

1. Verify that the provisional ADS, filing receipt, specification, and drawings in Patent Center match the repository copy and that benefit is timely and correctly claimed for the selected route.
2. Verify the PCT application text and drawings against the official WIPO as-filed record; do not rely solely on the converted Markdown.
3. Provide a written claim-as-a-whole § 112(a) analysis for AF claim 1, separately identifying direct architecture support and the combined-example source-pair/same-region/joint-match formulation.
4. Provide a separate written claim-as-a-whole § 112(a) and priority analysis for AF claim 20 against provisional method claim 10, the PCT method 200 disclosure, PCT claims 16–17, and the combined examples; do not infer the conclusion solely from AF claim 1's system analysis.
5. Decide whether “temporally corresponding frames” is conveyed by synchronized multicamera feeds and Example 2, and whether the proposed first/second-camera generalization is commensurate with the concrete Camera 2→Camera 3 example.
6. Resolve the provisional Example 2 inconsistency before filing or materially relying on AF claims 2–3, and do not insert resynchronization into AF claim 20 without the same written determination.
7. Determine whether Example 5 supports detection of camera-source identity on both sides of a transition or only visually similar frames, altered-cut characteristics, and timing.
8. Determine whether the candidate and detected pattern objects in AF claims 1 and 20 have an adequate operational basis, or substitute support-safer version/timing/reconstructed-manifest language.
9. Confirm the Examples 2→3→4 integration for AF claims 13 and 18 and the more specific paired-chunk geometry of AF claim 14.
10. Confirm AF claims 11–12's recipient-associated candidate-pattern input and portion-to-contributor wording; do not add attribution-score language absent an identified support basis.
11. Confirm the overlay/segmentation sequence in AF claim 19 or preserve a sequence-neutral version.
12. Review processor/instruction language, algorithm disclosure, § 112(f), definiteness, eligibility, and enablement independently of this written-description map; separately analyze AF claim 20's eligibility, restriction, divided-infringement, and method-step attribution consequences.
13. Preserve the NA actor-focused claims as a portfolio option; adequate AF support would not resolve divided-infringement or proof concerns.

## 9. Intervening-information trigger

This limited support review is not a clearance search and does not establish that no potentially material information exists between the provisional and PCT filing dates. **One window reference is on record: B10 (KR 2024-0168593 A), §102(a)(1) art as of its 02.12.2024 laid-open publication — LOW-materiality on full-text review; label corrected from an erroneous §102(a)(2) posture on 21.07.2026; escalation recorded in the shared deferred-work memo §4.**

If information is identified with a potentially relevant effective prior-art date after 26 February 2024 and before 19 February 2025—including a later-published patent document with an earlier effective filing date—or if any Office questions priority, counsel must promptly reassess:

1. claim-by-claim entitlement to the provisional date;
2. whether the Example 2 or combined-example gates become outcome-determinative;
3. applicable disclosure duties and any IDS or other filing action; and
4. every representation concerning priority or support.

Activation of this trigger does not itself dictate public disclosure of attorney analysis. Counsel must decide the correct disclosure and prosecution response based on the material information then known.

## 10. Revision record

- **AF-2026-07-17-v2 (17 July 2026):** added an independent limitation-level map for method AF claim 20 against provisional method claim 10 and the PCT method disclosure; carried the same-region, source-identity, joint-match, combined-example, and priority gates into that analysis; updated the filing posture and counsel checklist; and conformed the AF claim 1 ordered-transition wording repair. The presence of an exact substantive method twin does not substitute for a separate claim-as-a-whole support and priority determination.
- **Initial-contact defensibility pass (17 July 2026):** identified the map as complete for controlled initial counsel transmission while leaving legal conclusions pending; pinned the candidate source to `AF-2026-07-17-v2`; aligned the structured-list terminology; added prepared support-safer contingency paths and their art costs; and recorded AF claim 20's lack of a dependent fallback tier. No claim text or support classification changed.
