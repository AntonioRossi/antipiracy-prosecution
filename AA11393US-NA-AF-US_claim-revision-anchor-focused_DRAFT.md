# AA11393US — NA/AF Claim-Revision Plan: Anchor-Focused Reformulation (DRAFT)

> **STRATEGIES NA + AF · PROPOSAL STATUS 30 JULY 2026 · NOT ADOPTED**
>
> **INTERNAL COUNSEL-REVIEW MATERIAL — NOT FOR FILING.** This is applicant-prepared analysis, not counsel advice. It proposes complete replacement claim sets for the `AF` and `NA` branches. Nothing in this document is operative: the controlling claim-set versions remain `NA-2026-07-22-v4`, `AF-2026-07-22-v6`, and `AF-CONT-2026-07-22-v2`, with their version-locked companions, and this document modifies no claim set, map, matrix, briefing, crosswalk, navigator content, or shared control. Every conclusion, wording, gate, and adoption step below requires retained US counsel confirmation.

## 1. Purpose and scope

This plan reformulates both claim strategies around a single distinguishing feature — the **editing-domain anchor** — and brings each set within the basic fee allocation of **20 total claims and 3 independent claims, with no excess-claim fees**. The anchor is the chain that no reviewed reference teaches, in any combination:

1. The fingerprint symbol at each position is a **choice between two timings of the same ordered transition from a first source camera to a second source camera** — an editing-domain object recorded in the edit instructions, not a signal-domain delta.
2. That choice is **carried by manifest chunk selections**: each delivered manifest encodes a recipient-associated combination of timing choices across plural camera cuts.
3. Attribution maps a **detected combination of camera-cut timings** in the suspect, rebuilt as a reconstructed manifest, onto those recipient-associated timing-choice combinations — by manifest equality or as inputs to the probabilistic fingerprinting algorithm.

The obvious-combination rejection this plan is built to defeat is the natural one: desynchronization-robust hash reacquisition (B6), plus generic probabilistic collusion tracing (C3), plus shot-boundary detection (A5, A21), each applied for its known purpose. That combination teaches nothing about anchoring fingerprint symbols to moved boundaries between identified physical camera sources, carrying them as manifest chunk selections, and matching them as recipient-associated timing-choice sequences. Every independent claim below therefore recites the anchor chain itself; the art-exposed elements (perceptual hashes, fuzzy matching, sliding windows, Tardos variants) appear only as dependent implementation rungs.

Scope of this document: the two reformulated claim sets in full, the design decisions that produced them, and the procedure for applying them to this codebase. Review and re-scoring of cross-referenced companion documents is out of scope (§ 10).

## 2. Design decisions common to both sets

1. **Fold the timing-choice nexus into the independents.** Former AF claims 17 and 20 (manifest combinations preserving recipient-associated timing choices; reconstructed manifest representing the detected combination; matched delivered manifest containing an affirmative mate timing) are folded into AF claims 1, 17, and 20. Former NA claims 15 and 20 are folded into NA claims 9 and 15. The nexus is the patentability center; it cannot remain a fallback that an obviousness rejection of the independents would force the applicant to retreat to.
2. **Keep the art-exposed elements dependent.** Perceptual-hash comparison, sliding-window fuzzy matching, and segmented Tardos remain dependent rungs. They provide implementation fallback depth and are never load-bearing for patentability.
3. **Strengthen the detector-side environment without suspect-side camera identification.** The detection independents (NA 15, AF 20) now require the ledger's delivered manifests to reference an ensemble in which, **for each of a plurality of camera cuts**, the reference contains an **ordered transition between respective first and second camera sources** and at least one of the mates contains the same ordered transition at a different timing — so every counted position is an ordered-transition timing choice. The anchor is established on the delivered side; no suspect-side identification of physical camera sources is introduced, preserving the recorded exclusion (root `README.md`, claim-set generation workflow item 4).
4. **Spend the fee budget on the anchor, drop the periphery.** Claims with no anchor payload are dropped and reserved (§ 6). Each set lands at exactly 20 total / 3 independent / 17 singly dependent / no multiple-dependent claims.
5. **Reformulation, not new ground.** Except as noted in § 7, every limitation below is carried over from the operative v4/v6 sets with renumbering and the stated folds. New or strengthened relationships are confined to the independent claims and are individually flagged with their inherited gates.

## 3. AF reformulated claim set — 20 claims

Architecture: AF claim 1 (integrated system) and AF claim 17 (integrated method twin) each recite the complete production-to-attribution chain **with the timing-choice nexus built in**. AF claim 20 is the single-actor monitor-side method with the per-cut ordered-transition ensemble environment. Count: **20 total / 3 independent (1, 17, 20) / 17 singly dependent / no multiple-dependent claims**.

### 3.1 Dependency and origin map

| AF claim | Status | Depends from | Origin in `AF-2026-07-22-v6` | Change |
|---:|:---:|---:|:---:|---|
| 1 | Independent system | — | 1 + 17 + 20 | Timing-choice nexus folded in; search step anchored to the specific reconstruction |
| 2 | Dependent | 1 | 2 | Carried (Example 2 priority gate retained) |
| 3 | Dependent | 2 | 3 | Carried (Example 2 priority gate retained) |
| 4 | Dependent | 1 | 4 | Carried |
| 5 | Dependent | 1 | 5 | Carried |
| 6 | Dependent | 1 | 6 | Carried |
| 7 | Dependent | 1 | 7 | Carried |
| 8 | Dependent | 7 | 8 | Carried |
| 9 | Dependent | 1 | 9 | Carried |
| 10 | Dependent | 1 | 10 | Carried |
| 11 | Dependent | 1 | 11 | Carried |
| 12 | Dependent | 11 | 12 | Carried |
| 13 | Dependent | 1 | 13 | Carried |
| 14 | Dependent | 13 | 14 | Carried |
| 15 | Dependent | 1 | 16 | Renumbered |
| 16 | Dependent | 1 | 18 | Renumbered |
| 17 | Independent method | — | 19 + 20 | Timing-choice nexus folded in; search step anchored to the specific reconstruction |
| 18 | Dependent | 17 | 21 | Renumbered |
| 19 | Dependent | 18 | 22 | Renumbered |
| 20 | Independent method | — | 23 | Per-cut ordered-transition ensemble environment bound to the detected-combination positions |

### 3.2 AF claim text

> **1.** A system for generating recipient-associated distinguishable versions of audio-video content and identifying a recipient associated with a suspected unauthorized distribution of the audio-video content, the system comprising one or more processors and memory storing instructions that, when executed by the one or more processors, cause the system to:
>
> receive video captured from a plurality of cameras and a structured list of edit instructions comprising, for each of a plurality of director-commanded camera cuts, a first edit entry comprising an out-point time code and a first source-camera identifier identifying a first camera of the plurality of cameras as a first source camera, and a following edit entry comprising an in-point time code and a second source-camera identifier identifying a second camera of the plurality of cameras as a second source camera different from the first source camera;
>
> produce reference audio-video content according to the structured list of edit instructions;
>
> generate one or more mates of the reference audio-video content by, for each of a plurality of selected camera cuts among the director-commanded camera cuts, modifying, in the structured list of edit instructions, the out-point time code of the corresponding first edit entry and the in-point time code of the corresponding following edit entry while retaining the first and second source-camera identifiers and the order of the first and second source cameras, such that, for each selected camera cut:
>
> a transition from the first source camera to the second source camera occurs at a reference camera-switch timing in the reference audio-video content and at a later mate camera-switch timing in at least one of the one or more mates; and
>
> in the at least one mate, selection of the first source camera is extended from the reference camera-switch timing to the later mate camera-switch timing and selection of the second source camera begins at the later mate camera-switch timing;
>
> segment an ensemble comprising the reference audio-video content and the one or more mates into chunks;
>
> generate a plurality of manifest files pointing to respective combinations of chunks selected from the ensemble, each respective combination of chunks preserving, for each of the plurality of selected camera cuts, a choice between the reference camera-switch timing and the later mate camera-switch timing of that selected camera cut, so that the respective combinations of chunks represent respective combinations of timing choices across the plurality of selected camera cuts;
>
> cause delivery of streamed audio-video content to respective recipients according to respective manifest files of the plurality of manifest files;
>
> store, in a ledger, associations between the respective manifest files and the recipients to which the streamed audio-video content was delivered according to the respective manifest files;
>
> receive the suspected unauthorized distribution;
>
> apply a scene-change detection algorithm to the suspected unauthorized distribution to identify a plurality of time codes of camera cuts in the suspected unauthorized distribution;
>
> build one or more reconstructed manifest files from the plurality of identified time codes, the one or more reconstructed manifest files including a reconstructed manifest file representing a detected combination of camera-switch timings across the plurality of selected camera cuts; and
>
> search the ledger to identify a recipient associated with a delivered manifest file that is equal to the reconstructed manifest file, the delivered manifest file that is equal to the reconstructed manifest file representing a recipient-associated combination of timing choices that includes at least one of the later mate camera-switch timings and matches the detected combination represented by the reconstructed manifest file.

> **2.** The system of claim 1, wherein the instructions cause the system to preserve, in at least one of the one or more mates, a timing of a later camera cut from the reference audio-video content, thereby restoring synchronization between that mate and the reference audio-video content from the later camera cut onward.

> **3.** The system of claim 2, wherein modifying the out-point and in-point time codes causes the mate camera-switch timing for one of the selected camera cuts to occur ten frames later than the corresponding reference camera-switch timing, extends selection of the first source camera by ten frames, correspondingly shortens a following selection of the second source camera, and restores synchronization at the later camera cut.

> **4.** The system of claim 1, wherein the structured list of edit instructions is an Edit Decision List.

> **5.** The system of claim 1, wherein the video is captured live from diverse viewpoints and the structured list of edit instructions records the director-commanded camera cuts as real-time selections among the plurality of cameras.

> **6.** The system of claim 1, wherein the instructions cause the system to generate a respective mate for each selected camera cut, each respective mate differing from the reference audio-video content in the modified out-point and in-point time codes for only that selected camera cut.

> **7.** The system of claim 1, wherein identifying the plurality of time codes comprises comparing frames of the suspected unauthorized distribution with frames of one or both of the reference audio-video content and the one or more mates using perceptual hashes of the frames.

> **8.** The system of claim 7, wherein the comparing comprises fuzzy matching in which perceptual hashes of groups of frames are compared using sliding windows.

> **9.** The system of claim 1, wherein the chunks are distributed through a content delivery network using adaptive streaming and the plurality of manifest files is tailored to recipient devices or network conditions.

> **10.** The system of claim 1, wherein a mixing process integrates chunks of the reference audio-video content with chunks of the one or more mates and progressively assigns respective manifest files to recipients as additional selected camera cuts become available.

> **11.** The system of claim 1, wherein the suspected unauthorized distribution comprises portions obtained from streamed audio-video content delivered according to different manifest files, and wherein the instructions further cause the system to apply a probabilistic fingerprinting algorithm to recipient-associated sequences of chunk selections represented by the delivered manifest files and identify one or more recipients whose delivered streamed audio-video content contributed respective portions to the suspected unauthorized distribution.

> **12.** The system of claim 11, wherein the probabilistic fingerprinting algorithm comprises a segmented Tardos fingerprinting algorithm that applies respective fingerprints to content segments and identifies at least one contributing recipient for at least one of the respective portions.

> **13.** The system of claim 1, wherein a first manifest file points to a first chunk selected from the reference audio-video content and a second manifest file points to a second chunk selected from one of the one or more mates, the first chunk and the second chunk spanning the same playback interval and having equal playback durations.

> **14.** The system of claim 13, wherein, for one of the selected camera cuts:
>
> the first chunk contains frames from the corresponding first source camera before the reference camera-switch timing and frames from the corresponding second source camera after the reference camera-switch timing; and
>
> the second chunk contains frames from the corresponding first source camera before the mate camera-switch timing and frames from the corresponding second source camera after the mate camera-switch timing.

> **15.** The system of claim 1, wherein causing delivery comprises unicasting respective streamed audio-video content to the respective recipients.

> **16.** The system of claim 1, wherein the instructions further cause one or more audio or video elements not present in the video received from the plurality of cameras to be overlaid onto at least one of the reference audio-video content or the one or more mates before segmentation into the chunks.

> **17.** A method for generating recipient-associated distinguishable versions of audio-video content and identifying a recipient associated with a suspected unauthorized distribution of the audio-video content, the method comprising:
>
> receiving video captured from a plurality of cameras and a structured list of edit instructions comprising, for each of a plurality of director-commanded camera cuts, a first edit entry comprising an out-point time code and a first source-camera identifier identifying a first camera of the plurality of cameras as a first source camera, and a following edit entry comprising an in-point time code and a second source-camera identifier identifying a second camera of the plurality of cameras as a second source camera different from the first source camera;
>
> producing reference audio-video content according to the structured list of edit instructions;
>
> generating one or more mates of the reference audio-video content by, for each of a plurality of selected camera cuts among the director-commanded camera cuts, modifying, in the structured list of edit instructions, the out-point time code of the corresponding first edit entry and the in-point time code of the corresponding following edit entry while retaining the first and second source-camera identifiers and the order of the first and second source cameras, such that, for each selected camera cut:
>
> a transition from the first source camera to the second source camera occurs at a reference camera-switch timing in the reference audio-video content and at a later mate camera-switch timing in at least one of the one or more mates; and
>
> in the at least one mate, selection of the first source camera is extended from the reference camera-switch timing to the later mate camera-switch timing and selection of the second source camera begins at the later mate camera-switch timing;
>
> segmenting an ensemble comprising the reference audio-video content and the one or more mates into chunks;
>
> generating a plurality of manifest files pointing to respective combinations of chunks selected from the ensemble, each respective combination of chunks preserving, for each of the plurality of selected camera cuts, a choice between the reference camera-switch timing and the later mate camera-switch timing of that selected camera cut, so that the respective combinations of chunks represent respective combinations of timing choices across the plurality of selected camera cuts;
>
> delivering streamed audio-video content to respective recipients according to respective manifest files of the plurality of manifest files;
>
> storing, in a ledger, associations between the respective manifest files and the recipients to which the streamed audio-video content was delivered according to the respective manifest files;
>
> receiving the suspected unauthorized distribution;
>
> applying a scene-change detection algorithm to the suspected unauthorized distribution to identify a plurality of time codes of camera cuts in the suspected unauthorized distribution;
>
> building one or more reconstructed manifest files from the plurality of identified time codes, the one or more reconstructed manifest files including a reconstructed manifest file representing a detected combination of camera-switch timings across the plurality of selected camera cuts; and
>
> searching the ledger to identify a recipient associated with a delivered manifest file that is equal to the reconstructed manifest file, the delivered manifest file that is equal to the reconstructed manifest file representing a recipient-associated combination of timing choices that includes at least one of the later mate camera-switch timings and matches the detected combination represented by the reconstructed manifest file.

> **18.** The method of claim 17, wherein identifying the plurality of time codes comprises comparing frames of the suspected unauthorized distribution with frames of one or both of the reference audio-video content and the one or more mates using perceptual hashes of the frames.

> **19.** The method of claim 18, wherein the comparing comprises fuzzy matching in which perceptual hashes of groups of frames are compared using sliding windows.

> **20.** A method of identifying a recipient associated with a suspected unauthorized distribution of audio-video content, the method comprising:
>
> receiving the suspected unauthorized distribution;
>
> applying a scene-change detection algorithm to the suspected unauthorized distribution to identify a plurality of time codes of camera cuts in the suspected unauthorized distribution;
>
> building one or more reconstructed manifest files from the plurality of identified time codes, the one or more reconstructed manifest files including a reconstructed manifest file representing a detected combination of camera-cut timings across a plurality of camera cuts; and
>
> searching a ledger comprising associations between a plurality of delivered manifest files and respective recipients to identify a recipient associated with a delivered manifest file that is equal to the reconstructed manifest file,
>
> wherein each of the plurality of delivered manifest files identifies a respective combination of chunks selected from an ensemble comprising reference audio-video content and one or more mates of the reference audio-video content, and wherein, for each of the plurality of camera cuts, the reference audio-video content contains an ordered transition from a respective first source camera to a respective second source camera at a respective reference camera-cut timing, and at least one of the one or more mates contains the same ordered transition at a respective different mate camera-cut timing,
>
> wherein each of the plurality of delivered manifest files represents, across the plurality of camera cuts, a recipient-associated combination of choices between the respective reference camera-cut timings and the respective different mate camera-cut timings, and
>
> wherein the delivered manifest file that is equal to the reconstructed manifest file represents a recipient-associated combination that includes at least one of the respective different mate camera-cut timings and matches the detected combination represented by the reconstructed manifest file.

### 3.3 AF antecedent-basis check (changed limitations only)

| Term in the changed limitation | Anchor |
|---|---|
| "the plurality of selected camera cuts"; "the reference camera-switch timing"; "the later mate camera-switch timing" | AF 1 / AF 17 mate-generation step |
| "the respective combinations of chunks" | AF 1 / AF 17 manifest-generation step |
| "a reconstructed manifest file representing a detected combination" → "the reconstructed manifest file" | AF 1 / AF 17 / AF 20 build step |
| "a recipient-associated combination of timing choices" | Ledger association step (AF 1 / AF 17); ledger environment (AF 20) |
| "an ordered transition from a respective first source camera to a respective second source camera"; "a respective reference camera-cut timing"; "a respective different mate camera-cut timing" (AF 20) | New per-cut delivered-side environment; support and gate flagged in § 7 |
| "the plurality of camera cuts" (AF 20 environment and combination clause) | AF 20 build step |

Unchanged carried claims retain the antecedent basis verified for `AF-2026-07-22-v6`; renumbering is mechanical (former 16→15, 18→16, 21→18, 22→19 with bases 19→17 and 21→18).

## 4. NA reformulated claim set — 20 claims

Architecture: three **single-actor** independent claims, one per commercial side, each reciting the anchor on its own side. This is the divided-infringement control: no independent claim requires one entity to perform another entity's phase, so no infringement case depends on direction-and-control attribution. Count: **20 total / 3 independent (1, 9, 15) / 17 singly dependent / no multiple-dependent claims**.

| NA claim | Single actor | Anchor carried on that side |
|---:|---|---|
| 1 — production system | Broadcaster, production facility, mate-generation vendor | Same ordered first→second camera transition at noncoincident reference/mate timings, with temporally corresponding different-camera frames in the interval |
| 9 — distribution system | Streaming platform, CDN/origin operator | Manifest combinations preserving, per defined temporal region, the choice between the two timings of the same ordered transition, encoding timing-choice sequences associated with recipients via the store step |
| 15 — detection system | Monitoring provider, rights owner | Ledger manifests representing recipient-associated timing-choice combinations over a per-cut ordered-transition ensemble; reconstructed manifest representing the detected combination; match requiring an affirmative mate timing |

The former end-to-end method (former NA 22) — the only NA independent spanning all four phases and therefore the set's only divided-infringement exposure — is dropped from this set and reserved (§ 6). A vertically integrated operator still infringes each of claims 1, 9, and 15 by performing each side, so the integrated case loses nothing; a split supply chain is now reachable actor by actor.

### 4.1 Dependency and origin map

| NA claim | Status | Depends from | Origin in `NA-2026-07-22-v4` | Change |
|---:|:---:|---:|:---:|---|
| 1 | Independent system | — | 1 | Carried (already recites the production-side anchor) |
| 2 | Dependent | 1 | 2 | Carried (Example 2 priority gate retained) |
| 3 | Dependent | 2 | 3 | Carried (Example 2 priority gate retained) |
| 4 | Dependent | 1 | 4 | Carried |
| 5 | Dependent | 1 | 5 | Carried |
| 6 | Dependent | 1 | 6 | Carried |
| 7 | Dependent | 1 | 7 | Carried |
| 8 | Dependent | 1 | 8 | Carried |
| 9 | Independent system | — | 9 + 15 | Plural defined temporal regions with per-region mate reference; timing-choice sequences folded in (association supplied by the store step) |
| 10 | Dependent | 9 | 10 | Carried |
| 11 | Dependent | 9 | 11 | Carried |
| 12 | Dependent | 9 | 13 | Antecedents conformed to plural regions and per-region mate reference |
| 13 | Dependent | 9 | 14 | Carried |
| 14 | Dependent | 9 | 12 | Renumbered |
| 15 | Independent system | — | 16 + 20 | Per-cut ordered-transition ensemble environment; detected-combination nexus folded in |
| 16 | Dependent | 15 | 17 | Renumbered |
| 17 | Dependent | 16 | 18 | Renumbered |
| 18 | Dependent | 15 | 19 | Redrafted onto the per-cut environment |
| 19 | Dependent | 15 | 21 | Renumbered |
| 20 | Dependent | 19 | — (mirrors AF 12) | New; dossier segmented-Tardos passage; gate flagged in § 7 |

### 4.2 NA claim text

> **1.** A system for generating distinguishable versions of audio-video content, the system comprising one or more processors and memory storing instructions that, when executed by the one or more processors, cause the system to:
>
> receive video captured from a plurality of cameras and a structured list of instructions describing edits that produce reference audio-video content from the captured video, the structured list identifying source cameras and time codes for camera cuts at which selection changes from one camera of the plurality of cameras to another;
>
> automatically vary a time code of at least one camera cut in the structured list to produce a varied structured list; and
>
> produce a mate of the reference audio-video content according to the varied structured list such that:
>
> the at least one camera cut comprises, in the reference audio-video content, an ordered transition from a first camera to a second camera at a first camera-switch timing;
>
> the mate contains the same ordered transition from the first camera to the second camera at a second camera-switch timing different from the first camera-switch timing; and
>
> during a temporal interval between the first camera-switch timing and the second camera-switch timing, one of the reference audio-video content and the mate contains frames captured by the first camera and the other of the reference audio-video content and the mate contains temporally corresponding frames captured by the second camera.

> **2.** The system of claim 1, wherein the instructions cause the system to preserve in the mate a timing of a later camera cut from the reference audio-video content, thereby restoring synchronization between the mate and the reference audio-video content from the later camera cut onward.

> **3.** The system of claim 2, wherein varying the time code extends a camera selection in the mate by ten frames, delays a following camera selection by ten frames, and restores synchronization at the later camera cut.

> **4.** The system of claim 1, wherein the structured list of instructions is an Edit Decision List identifying, for each of a plurality of cuts, a source camera, an in-point time code, and an out-point time code.

> **5.** The system of claim 1, wherein the video is captured live from diverse viewpoints and the structured list records director-commanded real-time camera selections.

> **6.** The system of claim 1, wherein the instructions cause the system to apply a time-code variation at each of a plurality of director-commanded camera cuts.

> **7.** The system of claim 1, wherein the structured list records the ordered transition using an identifier of the first camera, an identifier of the second camera, and a recorded time code corresponding to the first camera-switch timing, and wherein the varied structured list retains the identifiers of the first camera and the second camera on respective sides of the ordered transition and records, in place of the recorded time code, a different recorded time code corresponding to the second camera-switch timing.

> **8.** The system of claim 1, wherein the instructions further cause one or more audio or video elements not present in the video received from the plurality of cameras to be overlaid onto at least one of the reference audio-video content or the mate.

> **9.** A content-distribution system comprising one or more servers, the one or more servers comprising one or more processors and memory storing instructions that, when executed by the one or more processors, cause the content-distribution system to:
>
> receive a plurality of versions of audio-video content including a reference version and one or more mate versions, wherein, within each of a plurality of defined temporal regions:
>
> the reference version contains an ordered transition from a first camera source to a second camera source at a first camera-switch timing;
>
> at least one of the one or more mate versions contains the same ordered transition from the first camera source to the second camera source at a second camera-switch timing different from the first camera-switch timing; and
>
> during an interval between the first camera-switch timing and the second camera-switch timing, the reference version and that mate version contain temporally corresponding frames captured by different cameras;
>
> segment the plurality of versions into chunks;
>
> generate a plurality of manifest files pointing to respective combinations of chunks selected from the plurality of versions, each respective combination causing an assembled audio-video stream to preserve, within each of the plurality of defined temporal regions, either the first camera-switch timing or the second camera-switch timing of the ordered transition, whereby each respective combination encodes a respective sequence of timing choices across the plurality of defined temporal regions;
>
> cause delivery, to respective recipients, of audio-video streams assembled according to respective manifest files; and
>
> store, in a record of associations, associations between the respective recipients and the manifest files delivered to the respective recipients.

> **10.** The content-distribution system of claim 9, wherein the chunks are distributed through a content delivery network using adaptive streaming and the manifest files are tailored to recipient devices or network conditions.

> **11.** The content-distribution system of claim 9, wherein a mixing process integrates chunks of the reference version with chunks of one or more mate versions and progressively assigns distinguishable manifest files to recipients as additional camera-cut variations become available.

> **12.** The content-distribution system of claim 9, wherein, for one of the plurality of defined temporal regions:
>
> a first manifest file of the plurality of manifest files points to a first chunk selected from the reference version;
>
> a second manifest file of the plurality of manifest files, different from the first manifest file, points to a second chunk selected from one of the one or more mate versions;
>
> the first chunk and the second chunk each span the same playback interval and have equal playback durations;
>
> the first chunk contains frames from the first camera source before the first camera-switch timing and frames from the second camera source after the first camera-switch timing; and
>
> the second chunk contains frames from the first camera source before the second camera-switch timing and frames from the second camera source after the second camera-switch timing.

> **13.** The content-distribution system of claim 9, wherein delivery of the audio-video streams comprises unicasting respective streams to the respective recipients.

> **14.** The content-distribution system of claim 9, wherein the record of associations is a ledger identifying an end user or group of end users that received each manifest file.

> **15.** A system for identifying a recipient associated with a suspected unauthorized distribution of audio-video content, the system comprising one or more processors and memory storing:
>
> a ledger comprising associations between a plurality of delivered manifest files and respective recipients, each delivered manifest file identifying a respective combination of chunks selected from an ensemble comprising reference audio-video content and one or more mates of the reference audio-video content, wherein, for each of a plurality of camera cuts, the reference audio-video content contains an ordered transition from a respective first camera source to a respective second camera source at a respective reference camera-cut timing, and at least one of the one or more mates contains the same ordered transition at a respective different mate camera-cut timing, and wherein each delivered manifest file represents, across the plurality of camera cuts, a recipient-associated combination of choices between the respective reference camera-cut timings and the respective different mate camera-cut timings; and
>
> instructions that, when executed by the one or more processors, cause the system to:
>
> receive the suspected unauthorized distribution;
>
> apply a scene-change detection algorithm to the suspected unauthorized distribution to identify a plurality of time codes of camera cuts in the suspected unauthorized distribution;
>
> build one or more reconstructed manifest files from the plurality of identified time codes, the one or more reconstructed manifest files including a reconstructed manifest file representing a detected combination of camera-cut timings across the plurality of camera cuts; and
>
> search the ledger to identify a recipient associated with a delivered manifest file that is equal to the reconstructed manifest file, the delivered manifest file that is equal to the reconstructed manifest file representing a recipient-associated combination that includes at least one of the respective different mate camera-cut timings and matches the detected combination represented by the reconstructed manifest file.

> **16.** The system of claim 15, wherein identifying the plurality of time codes comprises comparing frames of the suspected unauthorized distribution with frames of one or both of reference audio-video content and one or more mates of the reference audio-video content using perceptual hashes of the frames.

> **17.** The system of claim 16, wherein the comparing comprises fuzzy matching in which perceptual hashes of groups of frames are compared using sliding windows.

> **18.** The system of claim 15, wherein the delivered manifest file that is equal to the reconstructed manifest file identifies at least one chunk selected from a mate of the one or more mates, the at least one chunk spans a temporal region of the ensemble that contains an ordered transition of one of the plurality of camera cuts, and, during an interval between the respective reference camera-cut timing of that ordered transition and the respective different mate camera-cut timing of that ordered transition in the mate, the reference audio-video content and the mate contain temporally corresponding frames captured by different cameras.

> **19.** The system of claim 15, wherein the suspected unauthorized distribution comprises portions obtained from delivered versions associated with different delivered manifest files, and wherein the instructions further cause the system to apply a probabilistic fingerprinting algorithm to recipient-associated sequences of chunk selections represented by the delivered manifest files and identify one or more recipients whose delivered versions contributed respective portions to the suspected unauthorized distribution.

> **20.** The system of claim 19, wherein the probabilistic fingerprinting algorithm comprises a segmented Tardos fingerprinting algorithm that applies respective fingerprints to content segments and identifies at least one contributing recipient for at least one of the respective portions.

### 4.3 NA antecedent-basis check (changed limitations only)

| Term in the changed limitation | Anchor |
|---|---|
| "the plurality of defined temporal regions"; "the first camera-switch timing"; "the second camera-switch timing"; "the ordered transition"; "one or more mate versions"; "that mate version" | NA 9 receive step (per-region recital) |
| "one of the one or more mate versions" (NA 12) | NA 9 receive step |
| "the record of associations" (NA 14) | NA 9 store step |
| "an ordered transition from a respective first camera source to a respective second camera source"; "a respective reference camera-cut timing"; "a respective different mate camera-cut timing"; "the plurality of camera cuts" (NA 15, 18) | NA 15 ledger environment (per-cut recital) |
| "an ordered transition of one of the plurality of camera cuts" → "that ordered transition" (NA 18) | NA 15 ledger environment |
| "a reconstructed manifest file representing a detected combination" → "the reconstructed manifest file" (NA 15, 18) | NA 15 build step |
| "the respective portions" (NA 20) | NA 19 ("contributed respective portions") |
| "identifying the plurality of time codes" (NA 16) | NA 15 scene-change detection step |

Unchanged carried claims retain the antecedent basis verified for `NA-2026-07-22-v4`; renumbering is mechanical (former 12→14, 13→12, 17→16, 18→17, 19→18, 21→19 with bases 16→15, 17→16, 21→19).

## 5. Divided-infringement analysis (NA set)

- **NA 1** is performed entirely by the production-side operator: it receives the video and the structured list, varies the list, and produces the mate. No delivery, association, or detection act is required of that actor.
- **NA 9** is performed entirely by the distribution-side operator: it receives the versions, segments, generates manifests, causes delivery, and stores the associations. Receiving versions from a producer is that actor's own act; "cause delivery" covers delivery through a CDN the platform engages — counsel must confirm the system-claim "use" posture against the intended accused configuration.
- **NA 15** is performed entirely by the monitoring entity operating the detection system: the ledger is stored in the system's own memory, and every affirmative operation (receive suspect, detect cut times, build the reconstructed manifest, search the ledger to identify the recipient) is that entity's. No production or delivery act is required, and no suspect-side physical-camera identification is introduced.
- The dropped former NA 22 required one entity across production, delivery, detection, and lookup; removing it eliminates the set's only inherent split-performance problem. The integrated chain remains claimed in the AF branch (AF 17), and the omitted NA method family is reserved (§ 6).
- Residual cautions carried from the operative set: system-claim infringement turns on "use" of the claimed system; evidence for the ledger contents, detected cut times, and the matched manifest may sit with different infrastructure operators (DW-08C governs). Analyze proof separately from validity, per the operative NA set's enforcement cautions.

## 6. Dropped and folded subject matter

| Former claim | Set | Disposition |
|---|---|---|
| NA 22–30 (entire end-to-end method family) | NA | Dropped from this set; reserve under the continuation-preservation memo |
| NA 15 | NA | Folded into NA 9 |
| NA 20 | NA | Folded into NA 15 |
| AF 15 (blockchain registration) | AF | Dropped from this set; reserve under the continuation-preservation memo |
| AF 17 | AF | Folded into AF 1 |
| AF 20 | AF | Folded into AF 1 and AF 17 |

Recording the dropped families under [`US/common/continuation-controls/AA11393US-continuation-preservation_MEMO.md`](US/common/continuation-controls/AA11393US-continuation-preservation_MEMO.md) is a mandatory adoption step (§ 9), but the recording itself is out of scope for this draft.

## 7. Support-gate consequences of the reformulation

The folds move gates that previously sat on dependent claims into the independent claims. This is the deliberate price of the anchor focus, and counsel must accept it claim by claim before adoption:

1. **AF 1 and AF 17** now carry former AF 20's exact-relationship gate (graded **D/CE/G** in the operative set: delivered recipient-combination → affirmative mate choice → reconstruction of the same detected combination) and former AF 17's plural-timing-choice confirmation gate, in addition to the existing claim-as-a-whole, production-boundary generalization, and per-filing mode gates.
2. **NA 9** now carries former NA 15's construction gate (the operative NA set's § 5 item 10: the objective scope of the recipient-associated sequence formulation) and a plural-region generalization of the formerly single-region distribution claim; counsel must conclude written description and enablement per filing.
3. **NA 15** now carries former NA 20's plural timing-combination gate and the strengthened per-cut ordered-transition ensemble environment. Former NA 16's DW-05A Mode A assignment does **not** carry automatically to the strengthened wording; counsel must re-run the per-filing mode analysis for NA 15 as a whole, including the provisional benefit entitlement.
4. **AF 20** replaces former AF 23's generic mate-timing environment with a per-cut ordered-transition environment bound to the detected-combination positions. The transition relationship is the specification's core disclosure, but AF 20 keeps former AF 23's whole-claim **D/CE/G; mode unassigned** grade, its § 101 pre-mortem, its construction-of-equality gate, and its single-performer requirement; none of that is cured by the strengthening.
5. **NA 20** is new to the NA branch (mirroring operative AF 12). The segmented-Tardos passage is directly disclosed; the segment/fingerprint/portion/contributor relationship inherits the analogue of AF 12's open gate.
6. **NA 2–3 and AF 2–3** retain the Example 2 priority gate verbatim; nothing in this plan changes that posture.
7. The construction of "equal" manifest and "matches the detected combination" (operative NA § 5 item 9; operative AF 23 gate) now sits at independent level in NA 15, AF 1, AF 17, and AF 20. The election among the three recorded constructions — byte identity, equivalent chunk selections, equivalent represented timing choices — remains **open and is reserved to counsel**; claim text retains bare "equal to" and no alternative is inscribed or foreclosed. On the merits, "equivalent represented timing choices" fits the claim architecture, because the trailing nexus clause already speaks timing-combination language; a chunk-identity construction interacts adversely with the adaptive-streaming dependents (AF 9, NA 10), under which a reconstruction recovers the timing-choice pattern but not rendition-exact chunk identities.
8. **Mode B consequence of the folds.** An independent that fails provisional written description for a folded relationship takes the 19 February 2025 PCT date and faces § 102(a)(1) intervening art, including B10's recorded posture. This prices the gates in items 1–4 and must be presented to counsel alongside them.

## 8. Formal and fee consequences

- **Each set: 20 total / 3 independent / 17 singly dependent / no multiple-dependent claims** — within the basic 20-total / 3-independent allocation. Ordinary excess-claim fees drop to zero (from +10 total and +1 independent in `NA-2026-07-22-v4`, and +3 total in `AF-2026-07-22-v6`).
- Dropping the NA end-to-end method removes the set's most distinct restriction target; consolidating the AF families narrows the examined groups. Counsel must reassess unity/restriction, election, and rejoinder for each restructured set rather than assume the operative posture carries over.
- § 371 national-stage amendment format, status identifiers, and a final antecedent-basis pass are rechecked on adoption (§ 9).

## 9. How to apply this plan to this codebase

Adoption is a version-locked bundle change, not a claim-text edit. The phases below follow the repository's authority order: authored sources first, their generated representations immediately after, navigator products last, the aggregate gate at the end. Each phase names its exit condition; a phase that cannot meet it is a stop condition per the [navigator runbook](navigator/RUNBOOK-content-sync-and-regeneration.md) § 7 — correct the owning source and rerun the affected generation steps, never hand-repair a representation or product. The substantive re-grading and re-scoring work (phases 2–3) requires the § 7 gate conclusions and counsel participation; everything downstream of it is mechanical regeneration.

**Phase 0 — gating decisions (no codebase change).** Record the § 7 gate conclusions and the § 8 counsel determinations; select the final claim roster for each strategy (20 total / 3 independent per set as drafted in §§ 3–4); decide the AF-CONT disposition (reserved baseline or amended). If counsel rejects any folded nexus at independent level, the corresponding operative independent formulation (former AF 1/19/23 without the fold; former NA 9/16 without the fold) is the recorded fallback, with the fold retained as a dependent — that variant is not drafted here and would be produced before phase 1. Counsel separately converts the adopted set to the required § 371 national-stage amendment format and rechecks claim counts (20/3 per set), dependency form, antecedent basis, and status identifiers.

**Phase 1 — claim sets (authored-Markdown authority).** Amend the candidate-claims, architecture, count, fallback-ladder, gate, and caution sections of [`US/normal-allowance/claims/AA11393US-NA-US_claim-set_DRAFT.md`](US/normal-allowance/claims/AA11393US-NA-US_claim-set_DRAFT.md) and [`US/allowance-first/parent/claims/AA11393US-AF-US_claim-set_DRAFT.md`](US/allowance-first/parent/claims/AA11393US-AF-US_claim-set_DRAFT.md) to § 4.2 and § 3.2 of this plan, and bump the version headers to new dated versions succeeding `NA-2026-07-22-v4` and `AF-2026-07-22-v6`. *Exit:* each registered claim-set `.source.xml` regenerates byte-identical to its Markdown under the structured-source conversion procedure (never hand-edited).

**Phase 2 — version-locked companions (authored-relation XML authority).** Per strategy, in order: priority-support map (renumber all rows; new NA 20 row; re-grade the folded nexuses; re-run the DW-05A per-filing mode analysis, including the NA 15 Mode A re-analysis); prior-art comparison matrix (full re-score against the new wording — B6, C3, A5, A21, C7, A9, A19 at minimum; complete relation/field/claim/document obligation census per runbook § 3); claim-document mapping matrix. Then the AF claim crosswalk (AF↔NA and AF↔AF-CONT remap; record the AF-CONT decision). If AF-CONT is amended, its claim set, support map, and matrix re-version as one bundle. *Exit:* every edited relation XML regenerates its Markdown review view byte-identical; no row references a superseded claim number; each companion is valid for the new claim-set version it names.

**Phase 3 — shared controls and counsel briefings.** Record the § 6 dropped families (NA 22–30; AF 15; the folded NA 15/20 and AF 17/20) under the [continuation-preservation memo](US/common/continuation-controls/AA11393US-continuation-preservation_MEMO.md) (CONT-03); update the deferred-filing memo's version references; verify — expected unchanged — the IDS reference list and the PCT informal-comments draft. Update both counsel briefings (architecture, divided-infringement analysis, zero-excess fee posture, gates). *Exit:* each amended Markdown regenerates its `.source.xml` byte-identical.

**Phase 4 — routers, glossary, registry.** Update `US/README.md` (versions and counts), `US/normal-allowance/README.md` and `US/allowance-first/README.md` (status headers, count/fee text, the AF-CONT decision), and the `GLOSSARY.md` claim-set-version row; verify `STRUCTURED-CONTENT-AUTHORITY-MANIFEST.md` registration for the new artifact names and the root `README.md` (expected unchanged). *Exit:* no live document names a superseded claim-set version.

**Phase 5 — navigator.** Update the four `navigator/editions/*.json` (`claimSetVersion`, `artifactName`); re-map `navigator/relations/na__pct.relations.xml` and `navigator/relations/af__pct.relations.xml` to the new claim text and numbering (exact identity binding; reconcile the complete matrix-obligation census with every declared art-transcription consumer edge); audit the wording XML (expected minimal); bump `navigator/bundles/current.json` (bundleVersion, timestamp, member names); update the pinned version/artifact tables in `contracts/30-product-generation/claims-navigator/technical-description_DRAFT.md` coherently with its acceptance pair. Remove stale `navigator/dist/` products, then per runbook §§ 4–5: `preview` all four products with visual inspection, `candidate` all four, `release` all four, `bundle`. Precondition: the exact locked environment and the policy-matching Chromium per the runbook. *Exit:* every candidate reproduces byte-for-byte under release; `navigator/dist/` contains exactly the configured new-version products and checksums plus the bundle and its checksum.

**Phase 6 — close-out.** Run the canonical current-state and document-integrity gate to a green result before handoff to counsel:

```sh
uv --no-cache --offline run --locked --no-sync python -m navigator validate-current
```

Then record the adoption outcome and the new operative versions in this plan's status block.

## 10. Out of scope for this draft

The following are mandatory consequences of adoption under the repository's version-locked bundle discipline but are **not** performed or reviewed here:

- Priority-support maps, prior-art comparison matrices, and claim-document mapping matrices for both strategies (re-scoring against the new claim wording, including the B6/C3/A5/A21/C7/A9/A19 inventory).
- Counsel briefings, fallback-ladder tables, and the AF claim crosswalk.
- Navigator content and stored build products.
- The continuation-preservation memo recording of § 6.
