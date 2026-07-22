# AA11393US — NA Claim Strategy and Candidate Claim Set (DRAFT)

> **STRATEGY NA · CLAIM-SET VERSION NA-2026-07-22-v4 · STATUS 22 JULY 2026**
>
> **COUNSEL-REVIEW DRAFT — NOT FOR FILING AS-IS.** Use `NA claim N` outside the claim text.
>
> Prepared for the US phase of PCT/IB2025/051755. This document proposes an actor-focused claim architecture and a candidate fallback ladder with express support gates. US counsel must confirm wording, claim construction, § 101, § 102, § 103, § 112(a)/(b)/(f), antecedent basis, restriction, fees, priority entitlement, amendment format, and conformity with the selected § 371 or § 111(a) route.

## 1. Operative architecture

The candidate set uses four independent claims directed to likely commercial operators:

| Independent NA claim | Primary actor / infringement target | Core limitation |
|---|---|---|
| 1 — production system | Broadcaster, production facility, mate-generation vendor | Same ordered first-camera-to-second-camera transition at noncoincident reference/mate timings, with temporally corresponding different-camera frames in the intervening interval |
| 9 — distribution system | Streaming platform, licensee, CDN/origin operator | Manifest/chunk selections preserving one of two positions of the same ordered camera-source transition and associated with recipients |
| 16 — detection system | Monitoring provider, platform, rights owner | Reference/mate chunk-combination manifests with a mate cut-timing difference, plural suspect cut-time detection, reconstructed-manifest building, equal-delivered-manifest lookup, and recipient identification |
| 22 — end-to-end method | Vertically integrated operator | Production variation, manifest delivery/association, plural cut-time reconstruction, and equal-manifest recipient lookup |

The set contains **30 total claims / 4 independent claims / 26 singly dependent claims / no multiple-dependent claims**. It is at the current Track One numerical ceiling and has no net claim-count headroom. Counsel should verify current limits, fees, and route mechanics at filing and coordinate any addition with a cancellation.

No operative NA claim requires suspect-side identification of physical camera sources or joint matching of an ordered physical-source pair with timing. Physical-camera identity remains in production and distribution structures, including the stored matched-manifest relationship in NA claim 19. Suspect recovery in NA claims 16, 19–20, and 22 uses the disclosed cut-time/reconstructed-manifest/equality path.

## 2. Drafting principles

1. **Production core.** “Different videos” is insufficient. NA claims 1 and 22 require local reassignment of a temporal interval from one physical camera source to another around a recorded camera cut.
2. **D1 response.** D1 does not itself disclose alternate-camera frame selection. Counsel must nevertheless test combinations with conventional multicamera production, A20, B9, A4, A6, B6, and A13.
3. **Direct detector object.** NA claim 16 operates on delivered manifests identifying reference/mate chunk combinations, plural detected camera-cut time codes, and reconstructed manifests. Perceptual hashing, fuzzy matching, matched-manifest physical-camera geometry, plural timing combinations, manifest sequences, and probabilistic tracing remain dependent implementations.
4. **No mandatory watermark disclaimer.** The claims remain open to complementary watermarking.
5. **Processor language.** Processor-and-memory wording does not eliminate § 112(f), definiteness, or algorithm-sufficiency review.
6. **Per-filing support.** Direct component support does not decide a strengthened claim relationship as a whole. Written description and enablement require separate conclusions for the PCT and provisional.

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

**4.** The system of claim 1, wherein the structured list of instructions is an Edit Decision List identifying, for each of a plurality of cuts, a source camera, an in-point time code, and an out-point time code.

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

generate a plurality of manifest files pointing to respective combinations of chunks selected from the plurality of versions, each respective combination causing an assembled audio-video stream to preserve, within the defined temporal region, either the first camera-switch timing or the second camera-switch timing of the ordered transition;

cause delivery, to respective recipients, of audio-video streams assembled according to respective manifest files; and

store, in a record of associations, associations between the respective recipients and the manifest files delivered to the respective recipients.

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

**16.** A system for identifying a recipient associated with a suspected unauthorized distribution of audio-video content, the system comprising one or more processors and memory storing:

a ledger comprising associations between a plurality of delivered manifest files and respective recipients, each delivered manifest file identifying a respective combination of chunks selected from an ensemble comprising reference audio-video content and one or more mates of the reference audio-video content, each mate having at least one camera-cut timing different from a corresponding camera-cut timing of the reference audio-video content; and

instructions that, when executed by the one or more processors, cause the system to:

receive the suspected unauthorized distribution;

apply a scene-change detection algorithm to the suspected unauthorized distribution to identify a plurality of time codes of camera cuts in the suspected unauthorized distribution;

build one or more reconstructed manifest files from the plurality of identified time codes; and

search the ledger to identify a recipient associated with a delivered manifest file that is equal to one of the one or more reconstructed manifest files.

**17.** The system of claim 16, wherein identifying the plurality of time codes comprises comparing frames of the suspected unauthorized distribution with frames of one or both of reference audio-video content and one or more mates of the reference audio-video content using perceptual hashes of the frames.

**18.** The system of claim 17, wherein the comparing comprises fuzzy matching in which perceptual hashes of groups of frames are compared using sliding windows.

**19.** The system of claim 16, wherein the delivered manifest file that is equal to one of the one or more reconstructed manifest files identifies at least one chunk selected from a mate of the one or more mates, and wherein:

the reference audio-video content contains, within a temporal region, an ordered transition from a first physical camera source to a second physical camera source at a first camera-switch timing;

the mate contains, within the temporal region, the same ordered transition from the first physical camera source to the second physical camera source at a second camera-switch timing different from the first camera-switch timing;

the at least one chunk spans the temporal region; and

during an interval between the first camera-switch timing and the second camera-switch timing, the reference audio-video content and the mate contain temporally corresponding frames captured by different physical camera sources.

**20.** The system of claim 19, wherein each respective combination of chunks preserves, across a plurality of camera cuts, a recipient-associated combination of camera-switch timings from the reference audio-video content and the one or more mates, and building the one or more reconstructed manifest files comprises generating a reconstructed manifest file representing a detected combination of camera-switch timings across the plurality of camera cuts.

**21.** The system of claim 16, wherein the suspected unauthorized distribution comprises portions obtained from delivered versions associated with different delivered manifest files, and wherein the instructions further cause the system to apply a probabilistic fingerprinting algorithm to recipient-associated sequences of chunk selections represented by the delivered manifest files and identify one or more recipients whose delivered versions contributed respective portions to the suspected unauthorized distribution.

### End-to-end method

**22.** A method of identifying a recipient associated with a suspected unauthorized distribution of streaming audio-video content, the method comprising:

receiving video captured from a plurality of cameras and a structured list of instructions that identifies source cameras and time codes for camera cuts;

producing reference audio-video content according to the structured list of instructions;

generating a mate by varying a time code of at least one camera cut in the structured list such that:

an ordered transition from a first camera source to a second camera source occurs at a reference camera-switch timing in the reference audio-video content and at a different mate camera-switch timing in the mate; and

during an interval between the reference camera-switch timing and the mate camera-switch timing, the mate and the reference audio-video content contain temporally corresponding frames captured by different cameras;

segmenting an ensemble comprising the reference audio-video content and the mate into chunks;

generating a plurality of manifest files pointing to respective combinations of chunks selected from the ensemble;

delivering streamed audio-video content to respective recipients according to respective manifest files of the plurality of manifest files;

storing, in a ledger, associations between the respective manifest files and the recipients to which the streamed audio-video content was delivered according to the respective manifest files;

receiving the suspected unauthorized distribution;

applying a scene-change detection algorithm to the suspected unauthorized distribution to identify a plurality of time codes of camera cuts in the suspected unauthorized distribution;

building one or more reconstructed manifest files from the plurality of identified time codes; and

searching the ledger to identify a recipient associated with a delivered manifest file that is equal to one of the one or more reconstructed manifest files.

**23.** The method of claim 22, wherein generating the mate comprises preserving a timing of a later camera cut from the reference audio-video content, thereby restoring synchronization between the mate and the reference audio-video content from the later camera cut onward.

**24.** The method of claim 22, wherein each manifest file points to chunks that cause streamed audio-video content assembled according to the manifest file to preserve, within a temporal region adjacent to the camera cut whose time code was varied, either the reference camera-switch timing or the mate camera-switch timing of the ordered transition from the first camera source to the second camera source.

**25.** The method of claim 24, wherein:

a first manifest file points to a first chunk selected from the reference audio-video content;

a second manifest file points to a second chunk selected from the mate;

the first chunk and the second chunk span the same playback interval and have equal playback durations;

the first chunk contains frames from the first camera source before the reference camera-switch timing and frames from the second camera source after the reference camera-switch timing; and

the second chunk contains frames from the first camera source before the mate camera-switch timing and frames from the second camera source after the mate camera-switch timing.

**26.** The method of claim 22, wherein identifying the plurality of time codes comprises comparing perceptual hashes of frames from the reference audio-video content and the suspected unauthorized distribution using sliding-window fuzzy matching.

**27.** The method of claim 22, wherein delivering the streamed audio-video content comprises unicasting respective streamed audio-video content to the respective recipients.

**28.** The method of claim 22, wherein the suspected unauthorized distribution comprises portions obtained from streamed audio-video content delivered according to different manifest files, the method further comprising applying a probabilistic fingerprinting algorithm to recipient-associated sequences of chunk selections represented by the delivered manifest files and identifying one or more recipients whose streamed audio-video content contributed respective portions to the suspected unauthorized distribution.

**29.** The method of claim 22, wherein generating the mate comprises varying time codes at a plurality of camera cuts, and wherein each respective combination of chunks preserves, across the plurality of camera cuts, a recipient-associated combination of reference camera-switch timings and mate camera-switch timings.

**30.** The method of claim 22, further comprising overlaying one or more additional audio or video elements not present in the video received from the plurality of cameras onto at least one of the reference audio-video content or the mate before segmenting the ensemble.

## 4. Fallback ladder and art purpose

| Fallback | NA claims | Principal purpose |
|---|---|---|
| Production-side ordered physical-camera transition at noncoincident timings | 1, 7, 9, 13, 15, 22, 24–25, 29 | Preserve the structural camera-boundary distinction over completed-copy transformations and generic stream switching |
| Later-cut resynchronization | 2–3, 23 | Distinguish uniform delay and global retiming; subject to the Example 2 priority gate |
| Manifest/chunk preservation of the moved transition | 9, 13, 15, 24–25, 29 | Bind delivery objects to the physical-camera boundary represented by the chunks |
| Detector-only reconstructed-manifest recovery | 16–18 | Provide actor-focused recipient resolution using delivered reference/mate chunk-combination manifests and the directly disclosed cut-time/reconstruction/equality path |
| Matched-manifest physical-camera geometry | 19 | Require the equal delivered manifest to select a mate chunk spanning the retained physical-camera transition at its noncoincident timing |
| Plural recipient timing reconstruction | 20 | Require the reconstructed manifest to represent a detected recipient-associated combination across plural cuts |
| Perceptual-hash and fuzzy comparison | 17–18, 26 | Concrete cut-time detection implementations |
| Positive collusion attribution | 21, 28 | Identify contributing recipients from recipient-associated manifest sequences |
| End-to-end reconstructed-manifest method | 22–30 | Preserve the production-to-attribution chain in affirmative method steps |

## 5. Support and filing gates

1. **Production relationship.** Example 2 directly shows Camera 2 followed by Camera 3, extension of Camera 2, delayed commencement of Camera 3, and noncoincident transition timings. Counsel must determine the generalized same-ordered-transition and different-camera-interval formulations in NA claims 1, 7, 9, 13, 15, 22, 24–25, and 29.
2. **Example 2 resynchronization.** NA claims 2–3 and 23 require a written determination addressing the provisional's stray `00:00:30:11` sentence and the table/corrective text showing restoration at `00:00:30:01`.
3. **Distribution integration.** Examples 2–4 disclose camera-boundary variation, chunks, manifest combinations, and recipient association. Confirm the exact relationships in NA claims 9, 13, 15, 22, 24–25, and 29.
4. **Detection independent — Mode A.** Provisional claim 1(e), (g)–(n), method claim 10(e), (g)–(k), PCT claims 10–15, Method 200, and PCT claims 16–17 directly disclose NA claim 16's reference/mate ensemble, delivered chunk-combination manifests, mate cut-timing difference, suspect-acquisition, plural-cut-time, reconstructed-manifest, equality, ledger-search, and recipient-identification chain. NA claim 19 retains a combined-example gate for the matched manifest's mate chunk and physical-camera transition geometry; NA claim 20 retains the plural timing-combination gate and inherits NA claim 19.
5. **End-to-end method — Mode A.** Provisional method claim 10 and the PCT Method 200/claims 16–17 disclose the complete production, manifest delivery/recording, plural-cut-time reconstruction, equality, and recipient-identification chain recited by NA claim 22. Examples 2–4 supply the concrete physical-camera and manifest relationships within that disclosed chain.
6. **Collusion.** Confirm NA claims 21 and 28's use of recipient-associated manifest chunk-selection sequences as the probabilistic input and their respective-portion contributor output.
7. **Overlay sequence.** Confirm NA claim 30's overlay-before-segmentation relationship.
8. **Per-filing modes.** The applicant support assessment assigns NA claims 16 and 22 to DW-05A Mode A. For every other gated claim, separately conclude PCT written description, PCT enablement, provisional written description and enablement for benefit entitlement, and effective date without treating written description and enablement as interchangeable.

## 6. Enforcement and portfolio cautions

1. NA claim 16 is detector-focused and does not require the accused monitoring actor to perform production or delivery. Its stored ledger must nevertheless contain delivered-manifest mappings to reference/mate chunk combinations with the claimed mate timing difference. Its art position faces A4, A6, A13, B6, B8, B9, and A20 combination pressure.
2. NA claim 22 may require performance by, or attribution to, one entity across production, delivery, detection, and lookup. Analyze divided infringement and proof separately from validity.
3. The reference/mate relationship, chunk provenance, manifest-to-chunk mappings, recipient ledger, matched delivered manifest, source-camera entries and moved boundaries for NA claim 19, plural detected cut times, reconstructed manifest, equality comparison, and contributor analysis may require evidence controlled by different infrastructure operators.
4. Do not describe any independent as categorically eligible, enabled, supported, novel, nonobvious, or infringed without the corresponding counsel analysis.
5. Convert the claims to the selected route's original-claim or amendment format and recheck status identifiers, antecedent basis, count, fees, and Track One requirements.
