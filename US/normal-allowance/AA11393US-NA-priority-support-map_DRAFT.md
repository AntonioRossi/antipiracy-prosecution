# AA11393US — NA Provisional and PCT Priority/Support Map (DRAFT)

> **STRATEGY NA · CLAIM-SET VERSION NA-2026-07-21-v2 · STATUS 21 JULY 2026**
>
> **INTERNAL COUNSEL ANALYSIS — NOT A LEGAL OPINION OR FILING DOCUMENT.** Use `NA claim N` outside the claim text.
>
> This map distinguishes (1) written-description/no-new-matter support in PCT/IB2025/051755 as filed from (2) entitlement to the 26 February 2024 filing date of US provisional 63/557,868. Page references to the provisional are PDF page numbers in `../../PPA2/as filed 63 557868.pdf`; counsel should verify them against the official USPTO image-file wrapper. PCT references are to the as-filed application in the international filing dossier.

## 1. Source identity

| Source | Filing date | Repository evidence | Status |
|---|---:|---|---|
| US provisional 63/557,868 | 2024-02-26 | `../../PPA2/as filed 63 557868.pdf`; filing report in the same directory | Earliest claimed benefit source |
| PCT/IB2025/051755 | 2025-02-19 | `../../PCT/AA11393US-PCT_RAPPORTO DEPOSITO.pdf` | International application as filed |
| IT 102025000003210 | 2025-02-19 | Italian filing dossier under `../../ITA/` | Related application; not an earlier priority source |

The directory name `PPA2` is not evidence of a second provisional. No second provisional filing receipt has been identified.

## 2. Feature map

| Proposed claim feature | Provisional support | PCT support | Assessment / counsel action |
|---|---|---|---|
| Multiple cameras capturing an event from diverse viewpoints | pp. 15, 42–44; system and method claim passages | Detailed description of cameras 101 and pipeline 102; PCT claims 1, 10, 16 | Strong core support |
| Director-commanded switching / camera cuts | pp. 15, 20–25, 42–44 | Pipeline 102 description; camera-cut recording step 220; PCT claims 10 and 16 | Strong core support |
| Structured list of instructions describing edits / EDL | pp. 12, 15, 20–27, 42–44 | List 103 and EDL passages; PCT claims 1, 10, and 16 | Strong core support |
| Entries identify source camera and in/out time codes | pp. 23, 26–27; Example EDL tables | EDL description and Example 2, Tables 1–3 | Strong support; preserve source-camera terminology |
| Automatic variation of camera-cut time code to generate mate | pp. 15, 24–27, 42–44; real-time pseudocode and claims | Mate creation component 110; Example 1; PCT claims 1, 10, and 16 | Strong core support |
| Mate differs in sequence/timing of camera cuts | pp. 24–27 | Description of mates 111 and timing patterns | Strong core support |
| Same ordered camera-source transition occurs at noncoincident reference/mate switch timings (NA claims 1, 7, 9, 15, 16, 22, 29) | pp. 26–27: the reference and mate EDL tables retain the Camera 2-to-Camera 3 order while Cut 2 is extended and Cut 3 begins ten frames later in the mate | Example 2, Tables 1–3 and explanatory text | Supported by the concrete example; counsel must confirm that generalizing the shown ordered transition and two timings is an adequate written-description expression rather than an unsupported abstraction, including for NA claim 1 as a whole |
| Varied structured list retains the first/second source-camera identifiers on the respective sides while changing the recorded transition time code (NA claim 7) | pp. 26–27: the reference and mate EDL tables retain the Camera 2 and Camera 3 source entries around the moved Cut 3 boundary while its start time changes | Example 2, Tables 1–3 and explanatory text | Concrete internal-record fallback; counsel must separately confirm support for the exact identifier-retention and recorded-time-code formulation rather than treating the output relationship alone as sufficient |
| Actual interval between the noncoincident switch timings uses temporally corresponding frames from different cameras (NA claims 1, 9, 16, 22) | pp. 26–27: extending Cut 2 replaces the beginning interval of Cut 3 with the continuing Camera 2 selection | Example 2, Tables 1–3 and explanatory text | Supported by the concrete example; counsel should confirm the proposed “temporally corresponding frames” wording and the claim-as-a-whole combination |
| Later cut retains reference time / resynchronization | pp. 26–27: the Example 2 table places Cut 4 at the reference time and the accompanying text expressly states that `00:00:30:01` is the correct start, but the same paragraph also contains an inconsistent `00:00:30:11` “mistake” sentence | Example 2: Cut 4 starts at the same reference time; re-alignment explanation is internally consistent in the PCT text | Supported narrow fallback, subject to an express counsel opinion on the provisional's internal inconsistency; do not describe priority confidence as unqualified |
| Small/subtle/visually insignificant variations | pp. 12, 15, 24, 38 | Description characterizes differences as subtle/minimal/visually insignificant | Support exists for selected variations; do not claim every arbitrary shift is inherently imperceptible |
| Segmentation into chunks and adaptive CDN delivery | pp. 12, 15, 18–19, 28–34, 42–44 | Transcoding components 120, chunks 113; PCT claims 11–12 and 17 | Strong support |
| Manifest files point to interleaved reference/mate chunks and an assembled stream preserves one of the claimed transition timings (NA claims 9, 15, 29) | pp. 15, 28–34, 42–44, read with the Example 2 EDLs at pp. 26–27 | Manifest files 121, mixing component 123, manifest Example 3 and mixing Example 4, read with Example 2; PCT claims 11–12 and 17 | The components are disclosed, but the exact operational connection between PCT Example 2's noncoincident ordered transition and PCT Examples 3–4's chunk/manifest assembly—and between the corresponding provisional passages—requires express §112(a) and priority review; do not rely on a generic “camera-cut origin” label |
| Different manifests select equal-duration reference and mate chunks spanning the same playback interval, each chunk containing the same ordered source transition at its respective noncoincident timing (NA claim 13) | The unnumbered manifest-files example at pp. 28–29 describes equal-duration corresponding manifest positions using different reference and mate chunks, including a different chunk for the altered third cut, read with the moved cut boundary in the Example 2 EDLs at pp. 26–27 and the mixing passages at pp. 30–34 | Chunks 113, manifest files 121, PCT manifest Example 3 and mixing Example 4, read with PCT Example 2 | Concrete chunk-level fallback, but the complete relationship—including that each corresponding chunk contains the ordered transition at its respective internal timing—is not quoted verbatim in one passage; counsel must confirm PCT Examples 2–4, the corresponding provisional passages, and priority entitlement |
| Record/ledger associates versions or manifests with recipients | pp. 12, 15, 18, 31–35, 38, 41–44 | Ledger 122; PCT claims 1, 14, 15, and 17 | Strong support |
| Unicasting | pp. 16, 38, 43–44 | PCT claim 6 and method embodiment | Supported dependent fallback |
| Detect, at the same candidate-distinguishing region, the ordered camera sources on respective sides of a cut and its switch timing, then match both source order and timing (NA claims 16 and 22) | pp. 15, 34–38, 41–44, read with Example 2 at pp. 26–27 | Detection component 130, camera-cuts detection algorithm 131, retrieval 140, PCT claims 1 and 15–17, read with PCT Example 2 | Generic cut/time-code detection and ledger lookup are strongly supported; identifying both camera sources and matching both ordered transition and timing at the same candidate-distinguishing region is a deliberate combined-example support gate, not a settled conclusion |
| Perceptual hash comparison | pp. 16, 36–37, 43–44 | PCT claim 2; Example 5 | Supported, but known-art implementation detail |
| Sliding-window fuzzy matching | pp. 16, 37, 43–44 | PCT claim 3; Example 5 | Supported, but known-art implementation detail |
| Reconstructed manifest and ledger search | Direct reconstruction/search support at pp. 15, 34–37, 41, 43–44; the unnumbered manifest-files passage at pp. 28–29 supplies manifest-structure context only | Reconstructed manifest 121′ and retrieval 140; PCT claims 15 and 17, read with PCT Example 3 for manifest-structure context only | Strong narrow fallback for the expressly disclosed derive/build/search operations; PCT Example 3 and the provisional manifest passage do not independently disclose reconstruction |
| Probabilistic/Tardos handling of collusion, including mixed-version suspected content and positive recipient attribution (NA claims 21, 28) | pp. 38–40, 43–44 | PCT claim 5 and Tardos passages | Supported generally; NA claim 21's computation of respective attribution scores for candidate recipient contributions requires specific counsel confirmation or support-safe alternative wording |
| Additional overlaid audio/video elements | pp. 43–44 and related description | PCT claim 4 and pipeline overlay description | Supported dependent fallback |
| Processor, memory, storage, and server implementation | pp. 24–25, 31–36 | Computing-environment and server-cluster passages; PCT claims 8–9 | General structural support; §112(f)/algorithm analysis remains necessary |
| Operation without requiring the boundary variation to embed pixel data | Architecture throughout; watermark discussed as complementary rather than sole mechanism | Description states mechanism does not only involve watermarking and permits complementary watermarking | Use as an advantage, not an unsupported blanket negative limitation |

## 3. Example 2 drafting inconsistency requiring counsel analysis

The provisional's Example 2 contains a drafting inconsistency directly relevant to candidate NA claims 2, 3, and 23:

- At provisional PDF p. 27 (printed p. 16), the mate EDL table places Cut 4 at `00:00:30:01` and labels it “Adjusted to the reference.”
- The explanatory bullet first says that the mate's Cut 4 begins at `00:00:30:11`, identifies that value as a mistake in the alignment attempt, and then expressly states that the correct approach is for Cut 4 to start at `00:00:30:01`, just as in the reference and with no delay.
- The PCT Example 2 states the corrected alignment without the provisional's inconsistent value.

The correct resynchronization rule therefore appears expressly in both the provisional table and the provisional's corrective explanation. The inconsistency should not be treated internally as an automatic loss of priority, but neither should the fallback receive an unqualified “strong” rating. Counsel should provide a claim-specific written view on whether a skilled reader would understand possession of later-cut resynchronization and whether the PCT wording is a permissible clarification rather than new matter. Until that review is complete, keep resynchronization as a dependent fallback rather than the sole basis of the principal independent claim.

This issue belongs in the confidential counsel analysis. Do not insert it into the public WIPO informal comments unless counsel concludes that doing so is strategically necessary.

### Trigger for renewed priority and disclosure analysis

The present limited review has not identified potentially material art or another prior-art event having an effective date after the provisional filing on 26 February 2024 but before the PCT filing on 19 February 2025, **with one recorded exception: B10 (KR 2024-0168593 A), whose only prior-art route is §102(a)(1) as of its 02.12.2024 laid-open publication — inside the interval. B10 is LOW-materiality on full-text review (attribute-domain marking; no cameras, no edit list, no timing/structure), and its label was corrected from an initial erroneous §102(a)(2) posture on 21.07.2026. The escalation is recorded in the shared deferred-work memo §4 (recorded activations).** This is not a clearance conclusion.

If a reference, activity, or other information potentially material to patentability is identified with an effective prior-art date in that interval, or if any Office questions priority entitlement, counsel must reassess:

1. the claim-by-claim Example 2 and provisional-support position;
2. whether the effective filing date becomes outcome-determinative for any pending claim;
3. applicable disclosure obligations, including whether an IDS or other action is required; and
4. every representation concerning entitlement to the provisional date.

The direction to keep the present internal analysis out of the WIPO informal comments is subject to that reassessment. The trigger does not itself dictate public disclosure of attorney analysis; counsel must decide the correct disclosure and prosecution response based on the material information then known.

## 4. Candidate-claim mapping

| Candidate claims | Provisional basis | PCT basis | Priority confidence before counsel review |
|---|---|---|---|
| NA claims 1–6 — production | pp. 15, 20–27, 42–44 | PCT claims 1, 10, and 16; system 100; PCT Examples 1–2 | Strong support for the general production architecture; NA claim 1 separately requires claim-as-a-whole review of the generalized same first-camera-to-second-camera transition at noncoincident timings and the intervening different-camera interval; NA claims 2–3 separately require the Example 2 inconsistency analysis above |
| NA claim 7 — retained source-camera identifiers / changed recorded transition time code | pp. 26–27, 42–44 | PCT Example 2, Tables 1–3; PCT claims 10 and 16 | Inherits claim 1's output relationship and adds the internal structured-list delta; counsel must confirm support and priority for retaining the generalized first/second identifiers on the respective sides while changing the recorded transition time code |
| NA claim 8 — overlay | pp. 43–44 | PCT claim 4 | Medium/high |
| NA claims 9–12 and 14–15 — distribution | pp. 15, 18–19, 26–35, 42–44 | PCT claims 11–12, 14, and 17; PCT Examples 2–4 | Strong support for the separate production and distribution operations; NA claims 9 and 15 require counsel to confirm the integrated relationship among the same ordered transition, noncoincident switch timings, alternate-camera interval, manifest preservation, and stored source/timing data |
| NA claim 13 — corresponding reference/mate chunks for the same playback interval, each containing the ordered transition at its respective timing | pp. 26–34, 42–44 | Chunks 113, manifests 121, mixing 123; PCT Examples 2–4 | Medium pending claim-as-a-whole review of different manifests selecting the equal-duration corresponding chunks and of the transition's claimed placement within each chunk |
| NA claims 16–20 — detection | pp. 15, 26–27, 34–38, 41–44 | PCT claims 1–3, 15, and 17; PCT Examples 2 and 5 | High for the general architecture; expressly verify support for the same-region relationship and for detecting and matching the source identities on both sides together with timing |
| NA claim 21 — probabilistic collusion | pp. 38–40, 43–44 | PCT claim 5; Tardos passages | Medium; confirm support for candidate contributions, respective attribution scores, and identification based on those scores |
| NA claims 22–28 — end-to-end | Combined passages above | PCT claims 1–6, 10–12, and 14–17; PCT Examples 2–5 | Strong support for the component operations, but NA claim 22's closed loop and NA claim 28's positive collusion output require claim-as-a-whole review; blockchain-specific PCT claim 13 is not relied upon for this row; NA claim 23 resynchronization separately requires the Example 2 inconsistency analysis; divided-infringement is separate |
| NA claim 29 — manifest preserves reference or varied ordered-transition position | pp. 26–34, 42–44 | PCT Examples 2–4; PCT claims 11–12 and 17 | Medium pending confirmation that the combined disclosure supports manifest-selected chunks causing the assembled stream to preserve either claimed transition timing |
| NA claim 30 — overlay method | pp. 43–44 | PCT claim 4 and method overlay passage | Medium/high |

## 5. Items counsel must verify

1. Confirm that the provisional filing receipt, ADS, and specification in Patent Center match the repository copy and that benefit is timely and correctly claimed for the selected US route.
2. Confirm whether “temporally corresponding,” “camera-selection boundary,” “reference timing,” and “restoring synchronization” are acceptable constructions of the express examples rather than added concepts.
3. Confirm every independent claim as a whole—not merely each isolated noun—has adequate provisional support, including NA claim 1's same ordered first-camera-to-second-camera transition at noncoincident timings and intervening temporally corresponding different-camera frames.
4. Confirm the PCT-to-bypass continuity statement and certified-copy requirements if bypass is selected.
5. Treat any proposed feature absent from both columns as potential new matter; do not insert it into a continuation claim while representing it as entitled to the provisional date.
6. If commercially important improvements were developed after the PCT filing, identify them separately for possible continuation-in-part strategy rather than mixing them into this support map.
7. Address expressly the provisional Example 2 inconsistency identified in section 3 before relying on the provisional date for NA claims 2, 3, or 23 or moving resynchronization into an independent claim.
8. Confirm separately whether Example 2 support-safely generalizes (a) the output-level same ordered first-camera-to-second-camera transition at noncoincident timings in NA claim 1 and (b) the structured-list retention of the first/second source identifiers while changing the recorded transition time in NA claim 7.
9. Confirm whether NA claims 9, 13, 15, and 29 support-safely connect PCT Example 2's moved ordered source transition to PCT Examples 3–4's chunk/manifest assembly and whether the corresponding provisional passages support the same relationship, including NA claim 13's different manifests selecting equal-duration reference and mate chunks for the same playback interval, with each chunk containing the transition at its respective timing.
10. Confirm whether NA claim 16's candidate pattern, detected pattern, and match are fully supported as operations at the same candidate-distinguishing region, including identification and agreement of both source order and switch timing, rather than merely as descriptions of stored data.
11. Confirm NA claim 22's complete production-to-association-to-structural-recovery loop and NA claim 21's respective attribution-score formulation as claims as a whole.
12. Establish responsibility for monitoring potentially material information with an effective prior-art date in the provisional-to-PCT interval and activate the reassessment above if such information appears or any Office questions priority.

The former broader production theory—local alternate-camera substitution without requiring the same ordered camera pair at two timings—is not mapped as the scope of `NA-2026-07-21-v2`. If pursued, counsel should evaluate it separately as a coordinated continuation position and avoid using it to characterize present NA claim 1.

## 6. Revision record

- **NA-2026-07-21-v2 (21 July 2026):** added NA claim 1 to the generalized same-ordered-transition support gate, separated that output-level relationship from NA claim 7's internal identifier-retention/time-code delta, left the added resynchronization analysis for claims 2–3 unchanged while those dependent claims inherit amended claim 1, and reserved the former broader production theory for separate continuation review.
