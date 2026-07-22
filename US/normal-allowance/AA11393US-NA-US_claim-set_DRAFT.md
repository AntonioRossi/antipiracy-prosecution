# AA11393US — NA Claim Strategy and Candidate Claim Set (DRAFT)

> **STRATEGY NA · CLAIM-SET VERSION NA-2026-07-21-v2 · STATUS 22 JULY 2026**
>
> **COUNSEL-REVIEW DRAFT — NOT FOR FILING AS-IS.** Use `NA claim N` outside the claim text.
>
> Prepared for the US phase of PCT/IB2025/051755. This document proposes an actor-focused claim architecture and a candidate fallback ladder with express support gates. US counsel must confirm wording, §101, §112(a)/(b)/(f), antecedent basis, restriction, fees, priority entitlement, and conformity with the selected §371 or §111(a) route.

## 1. Recommended architecture

The candidate set uses four independent claims, each directed to a likely operator, so that subsystem coverage does not require proof that one commercial actor performs the full production, distribution, recipient-recording, and detection lifecycle:

| Independent NA claim | Primary actor / infringement target | Core limitation |
|---|---|---|
| 1 — production system | broadcaster, production facility, mate-generation vendor | the same ordered first-camera-to-second-camera transition at noncoincident reference/mate timings, with temporally corresponding different-camera frames in the intervening interval |
| 9 — distribution system | streaming platform, licensee, CDN/origin operator | manifest/chunk selections preserving one of two positions of the same ordered camera-source transition and associated with recipients |
| 16 — detection system | monitoring provider, platform, rights owner | recovery, at a candidate-distinguishing region, of an ordered camera-source transition and its timing, followed by recipient resolution |
| 22 — end-to-end method | vertically integrated operator; full-combination patentability position | production variation + association + structural transition-and-timing recovery in one claim |

The set contains **30 total claims / 4 independent claims / no multiple-dependent claims**, exactly at the current Track One numerical ceiling and therefore with **no net claim-count headroom**. During prioritized examination, an amendment may add a claim only if the application still contains no more than 30 total claims and four independent claims and contains no multiple-dependent claim—for example, through a coordinated cancellation. An amendment that results in exceeding those limits terminates prioritized examination. Excess-claim fees may nevertheless apply above the basic 20/3 fee allocation. Counsel should select claims for commercial value, not preserve 20/3 solely to avoid modest claim fees.

No independent computer-readable-medium claim is included. If software-vendor coverage justifies one, counsel should consider replacing the end-to-end method with a subsystem-specific medium claim—preferably production or detection software—rather than restoring an end-to-end medium claim that requires one software product to perform the entire commercial lifecycle.

## 2. Drafting principles

1. **Precise inventive core.** “Different videos” is not enough. The claims focus on local reassignment of a temporal interval from one camera source to another around a recorded camera cut.
2. **D1 delay/frame-rate response.** D1 alone does not disclose actual alternate-camera frame selection, which distinguishes its global retiming of a completed base copy. Counsel should nevertheless assess §103 combinations with conventional multi-camera production art. Later resynchronization is preserved as an express fallback, subject to the provisional-disclosure caveat identified in the separate priority map.
3. **No mandatory watermark disclaimer.** The edit-boundary mechanism may operate without pixel-domain embedding, but the claims remain open to complementary watermarking unless counsel deliberately chooses a narrower dependent claim.
4. **Concrete detection.** The claim set uses structural fallbacks rather than generic “AI.” Perceptual hashing, sliding-window fuzzy matching, reconstructed manifests, and probabilistic fingerprinting remain supported implementation details. Direct support for an added operation does not cure a support gate inherited from the claim on which it depends.
5. **Processor language.** Candidate claims use processors and memory rather than relying on “component” or “apparatus” as possible nonce terms. Counsel should still review §112(f) risk.
6. **Priority review.** Support citations below are to the PCT application. The separate priority map identifies corresponding provisional support; counsel must confirm that every claim receiving the provisional date is fully supported there.
7. **Pattern terminology.** The two pattern terms are deliberately related but not interchangeable, and they perform different claim functions rather than defining a strict information-content hierarchy. A **camera-cut timing pattern** is the sequence or arrangement of camera-switch times produced in a version and, where applicable, represented by chunks or manifests for distribution. Under NA claims 9 and 22, the claimed timing pattern is structurally constrained by an ordered transition between identified camera sources; the term is not intended to cover an arbitrary fragment-version sequence merely labeled as camera timing. Under NA claim 16, candidate and detected **camera-source-transition patterns** organize ordered camera-source transitions and their corresponding camera-switch timings at candidate-distinguishing regions for operational derivation and matching. NA claim 1 recites the corresponding ordered-transition and noncoincident-timing output relationship directly rather than through a pattern term. Counsel should preserve these distinct claim functions unless a final support or claim-construction review supports unification.

## 3. Candidate claims

### Production / mate-generation system

**1.** A system for generating distinguishable versions of audio-video content, the system comprising one or more processors and memory storing instructions that, when executed by the one or more processors, cause the system to:

receive video captured from a plurality of cameras and a structured list of instructions describing edits that produce reference audio-video content from the captured video, the structured list identifying source cameras and time codes for camera cuts at which selection changes from one camera of the plurality of cameras to another;

automatically vary a time code of at least one camera cut in the structured list to produce a varied structured list; and

produce a mate of the reference audio-video content according to the varied structured list such that:

the at least one camera cut comprises, in the reference audio-video content, an ordered transition from a first camera to a second camera at a first camera-switch timing;

the mate contains the same ordered transition from the first camera to the second camera at a second camera-switch timing different from the first camera-switch timing; and

during a temporal interval between the first camera-switch timing and the second camera-switch timing, one of the reference audio-video content and the mate contains frames captured by the first camera and the other of the reference audio-video content and the mate contains temporally corresponding frames captured by the second camera.

**2.** The system of claim 1, wherein the instructions cause the system to preserve in the mate a timing of a later camera cut from the reference audio-video content, thereby restoring synchronization between the mate and the reference audio-video content from the later camera cut onward.

**3.** The system of claim 2, wherein varying the time code extends a camera selection in the mate by ten frames, delays a following camera selection by ten frames, and restores synchronization at the later camera cut.

**4.** The system of claim 1, wherein the structured list of instructions is an edit decision list identifying, for each of a plurality of cuts, a source camera, an in-point time code, and an out-point time code.

**5.** The system of claim 1, wherein the video is captured live from diverse viewpoints and the structured list records director-commanded real-time camera selections.

**6.** The system of claim 1, wherein the instructions cause the system to apply a time-code variation at each of a plurality of director-commanded camera cuts.

**7.** The system of claim 1, wherein the structured list records the ordered transition using an identifier of the first camera, an identifier of the second camera, and a recorded time code corresponding to the first camera-switch timing, and wherein the varied structured list retains the identifiers of the first camera and the second camera on respective sides of the ordered transition and records, in place of the recorded time code, a different recorded time code corresponding to the second camera-switch timing.

**8.** The system of claim 1, wherein the instructions further cause one or more audio or video elements not present in the video received from the plurality of cameras to be overlaid onto at least one of the reference audio-video content or the mate.

### Distribution / recipient-association system

**9.** A content-distribution system comprising one or more servers, the one or more servers comprising one or more processors and memory storing instructions that, when executed by the one or more processors, cause the content-distribution system to:

receive a plurality of versions of audio-video content including a reference version and at least one mate version, wherein, within a defined temporal region:

the reference version contains an ordered transition from a first camera source to a second camera source at a first camera-switch timing;

the at least one mate version contains the same ordered transition from the first camera source to the second camera source at a second camera-switch timing different from the first camera-switch timing; and

during an interval between the first camera-switch timing and the second camera-switch timing, the reference version and the at least one mate version contain temporally corresponding frames captured by different cameras;

segment the plurality of versions into chunks;

generate a plurality of manifest files pointing to respective combinations of chunks selected from the plurality of versions, each respective combination causing an assembled audio-video stream to preserve, within the defined temporal region, either the first camera-switch timing or the second camera-switch timing of the ordered transition and thereby representing a camera-cut timing pattern;

cause delivery, to respective recipients, of audio-video streams assembled according to respective manifest files; and

store, in a record of associations, associations between the respective recipients and the manifest files or camera-cut timing patterns delivered to the respective recipients, each stored camera-cut timing pattern identifying the first camera source, the second camera source, and the camera-switch timing preserved in the corresponding assembled audio-video stream.

**10.** The content-distribution system of claim 9, wherein the chunks are distributed through a content delivery network using adaptive streaming and the manifest files are tailored to recipient devices or network conditions.

**11.** The content-distribution system of claim 9, wherein a mixing process integrates chunks of the reference version with chunks of one or more mate versions and progressively assigns distinguishable manifest files to recipients as additional camera-cut variations become available.

**12.** The content-distribution system of claim 9, wherein the record of associations is a ledger identifying an end user or group of end users that received each manifest file.

**13.** The content-distribution system of claim 9, wherein, for the defined temporal region:

a first manifest file of the plurality of manifest files points to a first chunk selected from the reference version;

a second manifest file of the plurality of manifest files, different from the first manifest file, points to a second chunk selected from the at least one mate version;

the first chunk and the second chunk each span the same playback interval and have equal playback durations;

the first chunk contains frames from the first camera source before the first camera-switch timing and frames from the second camera source after the first camera-switch timing; and

the second chunk contains frames from the first camera source before the second camera-switch timing and frames from the second camera source after the second camera-switch timing.

**14.** The content-distribution system of claim 9, wherein delivery of the audio-video streams comprises unicasting respective streams to the respective recipients.

**15.** The content-distribution system of claim 9, wherein the respective combinations encode recipient-associated sequences of choices, at a plurality of defined temporal regions, between a reference camera-switch timing and a different mate camera-switch timing, each defined temporal region containing the same ordered transition between respective first and second camera sources at the reference camera-switch timing in the reference version and at the mate camera-switch timing in the at least one mate version.

### Detection / recipient-resolution system

**16.** A system for identifying a source of a suspected unauthorized distribution of audio-video content, the system comprising one or more processors and memory storing:

a plurality of candidate camera-source-transition patterns associated with respective delivered versions of audio-video content, each candidate camera-source-transition pattern identifying, at each of a plurality of temporal regions adjacent to camera cuts defined by a structured list of edit instructions, an ordered transition from a camera source preceding a corresponding camera cut to a camera source following the corresponding camera cut and a camera-switch timing of the ordered transition, wherein at least two of the respective delivered versions contain, at a candidate-distinguishing temporal region, the same ordered transition from a first camera source to a second camera source at different respective camera-switch timings and, during an interval between the different respective camera-switch timings, contain temporally corresponding frames captured by different cameras;

a record associating the respective delivered versions or candidate camera-source-transition patterns with respective recipients; and

instructions that, when executed by the one or more processors, cause the system to:

receive the suspected unauthorized distribution;

detect, at the candidate-distinguishing temporal region in the suspected unauthorized distribution, an ordered transition between camera sources and a camera-switch timing of the detected ordered transition;

derive a detected camera-source-transition pattern identifying the camera sources on respective sides of the detected ordered transition and the camera-switch timing of the detected ordered transition;

identify a candidate camera-source-transition pattern for which both the ordered transition between the camera sources and the camera-switch timing at the candidate-distinguishing temporal region match the detected camera-source-transition pattern; and

search the record for a recipient associated with the matching candidate camera-source-transition pattern or its respective delivered version.

**17.** The system of claim 16, wherein detecting the ordered transition between the camera sources and the camera-switch timing comprises comparing reference audio-video content with the suspected unauthorized distribution using perceptual hashes of frames.

**18.** The system of claim 17, wherein detecting the ordered transition between the camera sources and the camera-switch timing further comprises fuzzy matching in which perceptual hashes of groups of frames are compared using sliding windows.

**19.** The system of claim 16, wherein the instructions cause the system to derive a time code from the detected camera-switch timing and build one or more reconstructed manifest files from the derived time code.

**20.** The system of claim 19, wherein the record is a ledger of manifest files delivered to end-user accounts and the instructions cause the system to search the ledger for an end-user account associated with a manifest file matching the one or more reconstructed manifest files.

**21.** The system of claim 16, wherein the suspected unauthorized distribution comprises portions obtained from different delivered versions, and wherein the instructions further cause the system to apply a probabilistic fingerprinting algorithm to candidate contributions from a plurality of recipients, compute respective attribution scores for the candidate contributions, and identify, based on the respective attribution scores, one or more recipients that contributed to the suspected unauthorized distribution.

### End-to-end method

**22.** A method of identifying a source of an unauthorized distribution of streaming audio-video content, the method comprising:

receiving video captured from a plurality of cameras and producing reference audio-video content according to a structured list of instructions that identifies source cameras and time codes for camera cuts;

generating a mate by varying a time code of at least one camera cut in the structured list such that an ordered transition from a first camera source to a second camera source occurs at a reference camera-switch timing in the reference audio-video content and at a different, varied camera-switch timing in the mate and, during an interval between the reference camera-switch timing and the varied camera-switch timing, the mate and the reference audio-video content contain temporally corresponding frames captured by different cameras;

delivering respective versions selected from the reference audio-video content and at least the mate to respective recipients;

recording associations between the respective versions or their camera-cut timing patterns and the respective recipients, each recorded camera-cut timing pattern identifying the first camera source, the second camera source, and the reference camera-switch timing or the varied camera-switch timing contained in the corresponding version;

detecting, in suspected unauthorized audio-video content and within a temporal region adjacent to the varied camera cut, an ordered transition between camera sources and a camera-switch timing of the detected ordered transition;

deriving a detected camera-source-transition pattern identifying camera sources on respective sides of the detected ordered transition and the camera-switch timing of the detected ordered transition;

identifying a version or camera-cut timing pattern for which both the ordered transition between the camera sources and the camera-switch timing match the detected camera-source-transition pattern; and

searching the recorded associations for a recipient associated with the identified version or camera-cut timing pattern.

**23.** The method of claim 22, wherein generating the mate comprises preserving a timing of a later camera cut from the reference audio-video content, thereby restoring synchronization between the mate and the reference audio-video content from the later camera cut onward.

**24.** The method of claim 22, further comprising:

segmenting the respective versions into chunks;

generating manifest files pointing to interleaved combinations of the chunks; and

recording which recipient or group of recipients received each manifest file.

**25.** The method of claim 24, wherein identifying the version or camera-cut timing pattern comprises deriving a time code from the camera-switch timing of the detected ordered transition, building a reconstructed manifest file, and searching a ledger for an end-user account associated with a manifest file matching the reconstructed manifest file.

**26.** The method of claim 22, wherein detecting the ordered transition between the camera sources and the camera-switch timing comprises comparing perceptual hashes of frames from the reference audio-video content and the suspected unauthorized audio-video content using sliding-window fuzzy matching.

**27.** The method of claim 22, wherein delivering the respective versions comprises unicasting the respective versions to the respective recipients.

**28.** The method of claim 22, wherein the suspected unauthorized audio-video content comprises portions obtained from different respective versions, the method further comprising applying a probabilistic fingerprinting algorithm to identify one or more contributing recipients.

**29.** The method of claim 24, wherein generating each manifest file comprises selecting chunks that cause an audio-video stream assembled according to the manifest file to preserve, within the temporal region adjacent to the varied camera cut, either the reference camera-switch timing or the varied camera-switch timing of the ordered transition from the first camera source to the second camera source.

**30.** The method of claim 22, further comprising overlaying one or more additional audio or video elements not present in the video received from the plurality of cameras onto at least one of the reference audio-video content or the mate.

## 4. Fallback ladder and prior-art purpose

| Fallback | NA draft claims | Principal purpose |
|---|---|---|
| Structured edit list with source-camera IDs and cut time codes | 1, 4, 7, 22 | Avoid mapping a generic stored finished video onto the production pipeline |
| Same ordered camera-source transition at noncoincident positions | 1, 7, 9, 15, 16, 22, 29 | Preserve the structural distinction over A4's fragment-perspective choices and B9's variable switching among transformed copies; claim 7 additionally preserves the corresponding structured-list identifiers |
| Actual alternate-camera frame substitution between the noncoincident positions | 1, 9, 16, 22 | Distinguish completed-copy transformations, arbitrary variant sequences, and generic timing shifts |
| Later cut retains reference timing / resynchronization | 2, 3, 23 | Distinguish uniform delay and global frame-rate retiming; track Example 2 subject to its provisional drafting inconsistency |
| Manifest/chunk selection preserves a claimed transition position | 9, 15, 24, 29 | Tie known manifest/segment technology to the noncoincident ordered camera-source transition rather than to a generic version sequence |
| Corresponding reference/mate chunks span the same playback interval and each contains the ordered transition at its respective timing | 13 | Bind the distinguishing physical-camera boundary to the chunks actually selected by different manifests; same-duration correspondence alone is known from A4 and does not carry patentability |
| Recipient record / ledger | 9, 12, 16, 20, 22, 25 | Preserve the forensic association step |
| Operational matching of both ordered source transition and timing at the same candidate-distinguishing region | 16, 22 | Avoid relying on informational labels, generic shot detection, or matching performed at a region unrelated to the stored difference |
| Camera-source-transition detection plus perceptual hash and sliding fuzzy match | 17, 18 | Concrete detection fallback tied to NA claim 16's operational transition-and-timing structure; not expected to be independently novel |
| Ordered-transition and timing detection using perceptual hash and sliding fuzzy match | 26 | Concrete end-to-end detection fallback under NA claim 22; not expected to be independently novel |
| Reconstructed manifest | 19, 20, 25 | Detection-system dependents (19–20) and an end-to-end-method dependent (25); their added derive/build/search operations are directly supported, but the inherited parent gates remain |
| Positive probabilistic/collusion attribution output | 21, 28 | Require identification of one or more contributing recipients rather than merely invoking an algorithm |

## 5. Support map to PCT application as filed

This table is a drafting guide, not counsel's final written-description opinion.

| NA claims | PCT support |
|---|---|
| 1, 4, 5, 22 | PCT claims 1 and 10; system 100 description of cameras 101, pipeline 102, list 103, camera cuts, mate creation 110; EDL description; Example 1 |
| 1–3, 22–23 | Example 2, Tables 1–3: cut 2 extended ten frames, cut 3 delayed, cut 4 starts at reference time; Example 2 explanation of restoring alignment. The provisional contains an internally inconsistent sentence concerning Cut 4; see the separate priority map and obtain counsel's priority opinion. |
| 6 | Preferred embodiment applying a single time-code variation at each director-commanded camera cut; PCT claim 17 context |
| 1, 7, 9, 15, 16, 22, 29 | Example 2 and its EDL tables show a camera selection extended and the next selection correspondingly delayed, so the source-camera order is retained while the boundary time changes and the intervening frames come from a different camera. Counsel must confirm support and priority for generalizing that example to the claimed “same ordered transition” and noncoincident-position formulations; claim 7 separately requires retention of the corresponding source-camera identifiers in the varied structured list. |
| 8, 30 | PCT claim 4 and description of pipeline overlays/additional elements |
| 9–15, 24, 29 | PCT claims 11–12, 14, and 17; transcoding 120, chunks 113, mixing component 123, manifest files 121, ledger 122; manifest Example 3 and mixing Example 4. NA claims 9, 13, 15, and 29 require an assembled stream or manifest-selected chunk to preserve a claimed transition position; NA claim 13 further requires different manifests to select equal-duration reference and mate chunks spanning the same playback interval, each chunk containing the ordered transition at its respective timing. Counsel must confirm that PCT Examples 2–4 and the corresponding provisional passages, read together, provide written-description support for each exact operational relationship and entitlement to priority. |
| 14, 27 | PCT claim 6 and method distribution embodiment using unicasting |
| 16, 22 | PCT claim 1; detection apparatus; camera-cuts detection algorithm 131; record of associations. Counsel must confirm support for identifying camera sources on both sides of a detected transition and for matching both the ordered transition and its timing at the same candidate-distinguishing temporal region; these limitations are deliberately not treated as settled merely because generic cut-time detection is disclosed. |
| 17–18 | PCT claims 2–3; Example 5 perceptual hashing and sliding-window fuzzy matching. Counsel should confirm support for using those comparisons to detect both camera-source transitions and their corresponding timings. |
| 26 | PCT claims 2–3; Example 5 perceptual hashing and sliding-window fuzzy matching. Counsel should confirm support for using those operations to detect the ordered source transition as well as its switch timing in the end-to-end method. |
| 19–20, 25 | Direct support for the **added** operations of deriving a time code, building reconstructed manifest 121′, and searching the ledger: PCT claim 15 and the detection-component 130 and retrieval-component 140 passages. Context for the underlying manifest structure: PCT Example 3 and the provisional's unnumbered manifest-files passage at PDF pp. 28–29. Those contextual passages do not independently supply the claimed derive/build/search operations. As drafted, claims 19–20 inherit claim 16 and claim 25 inherits claim 22; their direct added limitations do not cure the parents' source-identity/same-region gate. A support-safer route requires approved independent or intermediate wording that substitutes the direct derive/build/search path. |
| 21, 28 | PCT claim 5; Tardos/probabilistic-fingerprinting passages; collusion discussion. Counsel should confirm express or inherent support for computing the “respective attribution scores” recited in NA claim 21; retain a support-safe alternative phrasing if necessary. |

## 6. Counsel decisions and cautions

1. **Local substitution wording.** Confirm that “temporally corresponding frames” and the first-camera/second-camera formulation are the best US expressions of Example 2 and do not introduce an unintended synchronization requirement.
2. **Broader production theory.** NA claim 1 deliberately requires the observable same ordered first-camera-to-second-camera transition at noncoincident timings. Reserve the broader production theory—local alternate-camera substitution without the same-pair requirement—only for a coordinated continuation or other counsel-approved claim strategy; do not argue that present claim 1 omits the same-pair limitation. A generic relative-timing clause alone may be vulnerable to D1's frame-rate transformation.
3. **Restriction.** The production, distribution, and detection claims may invite a restriction requirement in a bypass case. Assess whether §371 unity practice or bypass restriction practice better serves the portfolio and whether divisional filings are budgeted.
4. **Divided infringement.** NA claim 22 preserves the full combination but is not the primary enforcement claim where different parties perform the steps. NA claims 1, 9, and 16 are intended to reduce that exposure.
5. **§112(f).** The processor/instruction format reduces reliance on nonce nouns, but counsel should still confirm whether any functional limitation invokes §112(f) and whether the disclosed algorithms are sufficient.
6. **Combined-example support gate.** NA claims 1, 7, 9, 13, 15, 16, 22, and 29 express structural relationships abstracted from the production, distribution, and detection examples. Before filing, counsel must determine whether each relationship is disclosed as an integrated operation under §112(a) and in the provisional, rather than assume that separately disclosed components may automatically be combined.
7. **Per-filing support modes.** For every gated claim, counsel must separately conclude PCT written description and enablement, provisional written description and enablement for benefit entitlement, and effective date, then assign that claim its own Mode A, B, or C under the shared DW-05A framework. A shared CE/gated citation is not one undifferentiated conclusion. Written description is the principal identified source-identity issue; enablement remains a separate, evidence-dependent inquiry.
8. **No-watermark limitation.** Do not add a negative limitation to an independent claim merely to contrast D1. The specification expressly allows watermarking as a complementary layer.
9. **Eligibility.** Emphasize concrete processing of synchronized camera-source frames, edit instructions, adaptive-stream manifests, and detected shot boundaries. Do not describe the set as categorically §101-safe.
10. **CRM alternative.** If a medium claim is desired, draft it for the software operations of NA claim 1 or NA claim 16 rather than the entire production/distribution/detection chain.
11. **Official format.** If used as a §371 preliminary amendment, convert to compliant claim-status identifiers and amendment markings under 37 CFR 1.121. If used in a bypass filing, prepare it as original claim text with the correct continuity statement and specification package.
12. **Detection-claim functional relationship.** NA claim 16 deliberately ties the stored inter-version difference, detection, and matching to the same candidate-distinguishing temporal region and requires agreement in both ordered camera-source transition and switch timing. Counsel should preserve that operational relationship if supported, confirm written-description support, and avoid relying only on an intended-use or data-label statement that stored timings were “produced by” the mate process. If PCT support fails, do not rely on claims 19–20/25 as presently dependent; prepare a new-version independent recovery claim using direct cut-time/version or reconstructed-manifest matching and ledger search.
13. **Positive collusion output.** NA claims 21 and 28 affirmatively require suspected content assembled from different delivered versions and identification of one or more contributing recipients. NA claim 21 additionally recites attribution scores; NA claim 28 does not. Counsel should preserve positive performance of the attribution operation, confirm support for the scoring formulation only where recited, and avoid optional “when” language in a method claim.
14. **Detection-dependent terminology.** NA claims 17 and 18 expressly address detection of the ordered camera-source transition and corresponding camera-switch timing to remain aligned with NA claim 16. NA claim 19 intentionally remains timing-specific because it derives a time code and reconstructs manifest information from that time code; do not broaden it merely for terminological symmetry.
15. **A4/B9 construction discipline.** NA claims 1, 9, and 16 recite the same ordered transition at noncoincident positions and the alternate-camera interval between them because generic camera-perspective fragments, per-user manifest sequences, and variable stream-switch positions are known. Counsel should resist deleting those structural limitations unless a materially broader position is supported by a completed professional claim-directed search and a reasoned validity analysis.
16. **NA claim 9 proof trade.** The structural limitations improve the patentability and validity position but increase the infringement-proof burden. Before finalizing NA claim 9, counsel should plan controlled captures from multiple recipient sessions and assess discovery access to manifest/source-chunk mappings and recipient-association records; actor splitting should not be treated as a pure enforcement gain.
17. **NA claim 1 proof ladder.** The same ordered transition and noncoincident timings in NA claim 1 are output-level relationships that may be investigated through synchronized reference/mate comparison and source-feed evidence. The structured-list input and automatic time-code variation will ordinarily require internal records or discovery; NA claim 7 intentionally adds the narrower proof that the varied structured list retained the corresponding source-camera identifiers.
