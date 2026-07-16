# AA11393US — US Claim Strategy and Candidate Claim Set (DRAFT)

> **COUNSEL-REVIEW DRAFT — NOT FOR FILING AS-IS.**
>
> Prepared for the US phase of PCT/IB2025/051755. This document proposes an actor-focused claim architecture and support-safe fallback ladder. US counsel must confirm wording, §101, §112(a)/(b)/(f), antecedent basis, restriction, fees, priority entitlement, and conformity with the selected §371 or §111(a) route.

## 1. Recommended architecture

The earlier draft placed production, distribution, recipient recording, and detection in every independent claim. That expressed the full inventive combination but risked requiring proof across different commercial actors. This draft uses four independent claims, each directed to a likely operator:

| Independent claim | Primary actor / infringement target | Core limitation |
|---|---|---|
| 1 — production system | broadcaster, production facility, mate-generation vendor | local movement of a camera-selection boundary using temporally corresponding frames from another camera |
| 9 — distribution system | streaming platform, licensee, CDN/origin operator | manifests/chunk selections representing camera-cut timing patterns and associated with recipients |
| 16 — detection system | monitoring provider, platform, rights owner | operational recovery of camera-source transitions and recipient resolution |
| 22 — end-to-end method | vertically integrated operator; full-combination patentability position | production variation + association + recovery in one claim |

The set contains **30 total claims / 4 independent claims / no multiple-dependent claims**, exactly at the current Track One numerical ceiling and therefore with **no net claim-count headroom**. During prioritized examination, an amendment may add a claim only if the application still contains no more than 30 total claims and four independent claims and contains no multiple-dependent claim—for example, through a coordinated cancellation. An amendment that results in exceeding those limits terminates prioritized examination. Excess-claim fees may nevertheless apply above the basic 20/3 fee allocation. Counsel should select claims for commercial value, not preserve 20/3 solely to avoid modest claim fees.

No independent computer-readable-medium claim is included. If software-vendor coverage justifies one, counsel should consider replacing the end-to-end method with a subsystem-specific medium claim—preferably production or detection software—rather than restoring an end-to-end medium claim that requires one software product to perform the entire commercial lifecycle.

## 2. Drafting principles

1. **Precise inventive core.** “Different videos” is not enough. The claims focus on local reassignment of a temporal interval from one camera source to another around a recorded camera cut.
2. **D1 delay/frame-rate response.** D1 alone does not disclose actual alternate-camera frame selection, which distinguishes its global retiming of a completed base copy. Counsel should nevertheless assess §103 combinations with conventional multi-camera production art. Later resynchronization is preserved as an express fallback, subject to the provisional-disclosure caveat identified in the separate priority map.
3. **No mandatory watermark disclaimer.** The edit-boundary mechanism may operate without pixel-domain embedding, but the claims remain open to complementary watermarking unless counsel deliberately chooses a narrower dependent claim.
4. **Concrete detection.** Generic “AI” has been removed from the independent claims. Perceptual hashing, sliding-window fuzzy matching, reconstructed manifests, and probabilistic fingerprinting remain supported fallbacks.
5. **Processor language.** Candidate claims use processors and memory rather than relying on “component” or “apparatus” as possible nonce terms. Counsel should still review §112(f) risk.
6. **Priority review.** Support citations below are to the PCT application. The separate priority map identifies corresponding provisional support; counsel must confirm that every claim receiving the provisional date is fully supported there.
7. **Pattern terminology.** The two pattern terms are deliberately related but not interchangeable. A **camera-cut timing pattern** is the sequence or arrangement of camera-switch times produced in a version and, where applicable, represented by chunks or manifests for distribution. A **camera-source-transition pattern** is the richer detection-side structure that identifies camera-source transitions together with their corresponding camera-switch timings. Counsel should preserve this hierarchy unless a final support or claim-construction review supports unification.

## 3. Candidate claims

### Production / mate-generation system

**1.** A system for generating distinguishable versions of audio-video content, the system comprising one or more processors and memory storing instructions that, when executed by the one or more processors, cause the system to:

receive video captured from a plurality of cameras and a structured list of instructions describing edits that produce reference audio-video content from the captured video, the structured list identifying source cameras and time codes for camera cuts at which selection changes from one camera of the plurality of cameras to another;

generate a mate of the reference audio-video content by automatically varying a time code of at least one camera cut in the structured list; and

produce the mate according to the varied structured list such that, during a temporal interval adjacent to the varied camera cut, the mate contains temporally corresponding frames from a first camera where the reference audio-video content contains frames from a second camera, a camera-cut timing pattern of the mate thereby differing from a camera-cut timing pattern of the reference audio-video content.

**2.** The system of claim 1, wherein the instructions cause the system to preserve in the mate a timing of a later camera cut from the reference audio-video content, thereby restoring synchronization between the mate and the reference audio-video content from the later camera cut onward.

**3.** The system of claim 2, wherein varying the time code extends a camera selection in the mate by ten frames, delays a following camera selection by ten frames, and restores synchronization at the later camera cut.

**4.** The system of claim 1, wherein the structured list of instructions is an edit decision list identifying, for each of a plurality of cuts, a source camera, an in-point time code, and an out-point time code.

**5.** The system of claim 1, wherein the video is captured live from diverse viewpoints and the structured list records director-commanded real-time camera selections.

**6.** The system of claim 1, wherein the instructions cause the system to apply a time-code variation at each of a plurality of director-commanded camera cuts.

**7.** The system of claim 1, further comprising a machine-learning analytics process configured to determine time-code variations or mate configurations based on historical data patterns and piracy-attempt profiles, wherein the determined time-code variations or mate configurations are supplied for generation of one or more further mates.

**8.** The system of claim 1, wherein the instructions further cause one or more audio or video elements not present in the video received from the plurality of cameras to be overlaid onto at least one of the reference audio-video content or the mate.

### Distribution / recipient-association system

**9.** A content-distribution system comprising one or more servers, the one or more servers comprising one or more processors and memory storing instructions that, when executed by the one or more processors, cause the content-distribution system to:

receive a plurality of versions of audio-video content including a reference version and at least one mate version, the reference version and the at least one mate version differing by a pattern of timings of camera cuts between views captured by different cameras;

segment the plurality of versions into chunks;

generate a plurality of manifest files pointing to respective interleaved combinations of chunks selected from the plurality of versions, each respective interleaved combination representing a camera-cut timing pattern;

cause delivery, to respective recipients, of audio-video streams assembled according to respective manifest files; and

store, in a record of associations, associations between the respective recipients and the manifest files or camera-cut timing patterns delivered to the respective recipients.

**10.** The content-distribution system of claim 9, wherein the chunks are distributed through a content delivery network using adaptive streaming and the manifest files are tailored to recipient devices or network conditions.

**11.** The content-distribution system of claim 9, wherein a mixing process integrates chunks of the reference version with chunks of one or more mate versions and progressively assigns distinguishable manifest files to recipients as additional camera-cut variations become available.

**12.** The content-distribution system of claim 9, wherein the record of associations is a ledger identifying an end user or group of end users that received each manifest file.

**13.** The content-distribution system of claim 12, further comprising a blockchain registration process configured to register associations between manifest files and end users from the ledger.

**14.** The content-distribution system of claim 9, wherein delivery of the audio-video streams comprises unicasting respective streams to the respective recipients.

**15.** The content-distribution system of claim 9, wherein the respective interleaved combinations encode recipient-associated sequences of choices between chunks of the reference version and chunks of the at least one mate version at temporal regions corresponding to camera cuts.

### Detection / recipient-resolution system

**16.** A system for identifying a source of a suspected unauthorized distribution of audio-video content, the system comprising one or more processors and memory storing:

a plurality of candidate camera-source-transition patterns associated with respective delivered versions of audio-video content, each candidate camera-source-transition pattern identifying camera-source transitions and corresponding camera-switch timings at temporal regions adjacent to camera cuts defined by a structured list of edit instructions, at least two of the respective delivered versions differing at one or more of the temporal regions by selection between temporally corresponding frames captured by different cameras;

a record associating the respective delivered versions or candidate camera-source-transition patterns with respective recipients; and

instructions that, when executed by the one or more processors, cause the system to:

receive the suspected unauthorized distribution;

detect camera-source transitions and corresponding camera-switch timings in the suspected unauthorized distribution at one or more of the temporal regions;

derive from the detected camera-source transitions and corresponding camera-switch timings a detected camera-source-transition pattern;

identify a candidate camera-source-transition pattern matching the detected camera-source-transition pattern; and

search the record for a recipient associated with the matching candidate camera-source-transition pattern or its respective delivered version.

**17.** The system of claim 16, wherein detecting the camera-source transitions and corresponding camera-switch timings comprises comparing reference audio-video content with the suspected unauthorized distribution using perceptual hashes of frames.

**18.** The system of claim 17, wherein detecting the camera-source transitions and corresponding camera-switch timings further comprises fuzzy matching in which perceptual hashes of groups of frames are compared using sliding windows.

**19.** The system of claim 16, wherein the instructions cause the system to derive time codes from the detected camera-switch timings and build one or more reconstructed manifest files from the derived time codes.

**20.** The system of claim 19, wherein the record is a ledger of manifest files delivered to end-user accounts and the instructions cause the system to search the ledger for an end-user account associated with a manifest file matching the one or more reconstructed manifest files.

**21.** The system of claim 16, wherein the suspected unauthorized distribution comprises portions obtained from different delivered versions, and wherein the instructions further cause the system to apply a probabilistic fingerprinting algorithm to candidate contributions from a plurality of recipients.

### End-to-end method

**22.** A method of identifying a source of an unauthorized distribution of streaming audio-video content, the method comprising:

receiving video captured from a plurality of cameras and producing reference audio-video content according to a structured list of instructions that identifies source cameras and time codes for camera cuts;

generating a mate by varying a time code of at least one camera cut in the structured list such that, during a temporal interval adjacent to the varied camera cut, the mate contains temporally corresponding frames from a first camera where the reference audio-video content contains frames from a second camera;

delivering respective versions selected from the reference audio-video content and at least the mate to respective recipients;

recording associations between the respective versions or their camera-cut timing patterns and the respective recipients;

detecting camera-switch timings in suspected unauthorized audio-video content;

identifying a version or camera-cut timing pattern matching the detected camera-switch timings; and

searching the recorded associations for a recipient associated with the identified version or camera-cut timing pattern.

**23.** The method of claim 22, wherein generating the mate comprises preserving a timing of a later camera cut from the reference audio-video content, thereby restoring synchronization between the mate and the reference audio-video content from the later camera cut onward.

**24.** The method of claim 22, further comprising:

segmenting the respective versions into chunks;

generating manifest files pointing to interleaved combinations of the chunks; and

recording which recipient or group of recipients received each manifest file.

**25.** The method of claim 24, wherein identifying the version or camera-cut timing pattern comprises deriving time codes from the detected camera-switch timings, building a reconstructed manifest file, and searching a ledger for an end-user account associated with a manifest file matching the reconstructed manifest file.

**26.** The method of claim 22, wherein detecting the camera-switch timings comprises comparing perceptual hashes of frames from the reference audio-video content and the suspected unauthorized audio-video content using sliding-window fuzzy matching.

**27.** The method of claim 22, wherein delivering the respective versions comprises unicasting the respective versions to the respective recipients.

**28.** The method of claim 22, wherein the suspected unauthorized audio-video content comprises portions obtained from different respective versions, the method further comprising applying a probabilistic fingerprinting algorithm to identify one or more contributing recipients.

**29.** The method of claim 22, further comprising determining, using a machine-learning process and based on historical data patterns and piracy-attempt profiles, time-code variations or mate configurations for generating further mates.

**30.** The method of claim 22, further comprising overlaying one or more additional audio or video elements not present in the video received from the plurality of cameras onto at least one of the reference audio-video content or the mate.

## 4. Fallback ladder and prior-art purpose

| Fallback | Draft claims | Principal purpose |
|---|---|---|
| Structured edit list with source-camera IDs and cut time codes | 1, 4, 22 | Avoid mapping a generic stored finished video onto the production pipeline |
| Actual alternate-camera frame substitution around a cut | 1, 22 | Distinguish D1's completed-copy signal transformations and generic timing shifts |
| Later cut retains reference timing / resynchronization | 2, 3, 23 | Distinguish uniform delay and global frame-rate retiming; track Example 2 subject to its provisional drafting inconsistency |
| Camera-cut timing pattern represented through interleaved manifests | 9, 11, 15, 24 | Tie known manifest/segment technology to the multi-camera structural variable |
| Recipient record / ledger | 9, 12, 16, 20, 22, 25 | Preserve the forensic association step |
| Operational camera-source-transition matching | 16 | Tie stored and detected patterns to regions where delivered versions select between temporally corresponding camera views, rather than to generic timing data alone |
| Camera-source-transition detection plus perceptual hash and sliding fuzzy match | 17, 18 | Concrete detection fallback tied to the richer claim 16 structure; not expected to be independently novel |
| Camera-switch-timing detection using perceptual hash and sliding fuzzy match | 26 | Timing-specific end-to-end fallback under claim 22; not expected to be independently novel |
| Reconstructed manifest | 19, 20, 25 | Narrow end-to-end distribution/detection implementation |
| Probabilistic/collusion processing | 21, 28 | Avoid overclaiming single-version matching as a complete collusion solution |

## 5. Support map to PCT application as filed

This table is a drafting guide, not counsel's final written-description opinion.

| Claims | PCT support |
|---|---|
| 1, 4, 5, 22 | PCT claims 1 and 10; system 100 description of cameras 101, pipeline 102, list 103, camera cuts, mate creation 110; EDL description; Example 1 |
| 1–3, 22–23 | Example 2, Tables 1–3: cut 2 extended ten frames, cut 3 delayed, cut 4 starts at reference time; Example 2 explanation of restoring alignment. The provisional contains an internally inconsistent sentence concerning Cut 4; see the separate priority map and obtain counsel's priority opinion. |
| 6 | Preferred embodiment applying a single time-code variation at each director-commanded camera cut; PCT claim 17 context |
| 7, 29 | Analytics component 104 and PCT claim 7; acknowledged as thin support and a cancellation candidate |
| 8, 30 | PCT claim 4 and description of pipeline overlays/additional elements |
| 9–15, 24 | PCT claims 11–14 and 17; transcoding 120, chunks 113, mixing component 123, manifest files 121, ledger 122; Example 4 |
| 13 | PCT claim 13 and blockchain registration component 150 |
| 14, 27 | PCT claim 6 and method distribution embodiment using unicasting |
| 16, 22 | PCT claim 1; detection apparatus; camera-cuts detection algorithm 131; record of associations. Counsel must confirm support for the proposed claim 16 expression of candidate and detected “camera-source-transition patterns.” |
| 17–18 | PCT claims 2–3; Example 5 perceptual hashing and sliding-window fuzzy matching. Counsel should confirm support for using those comparisons to detect both camera-source transitions and their corresponding timings. |
| 26 | PCT claims 2–3; Example 5 perceptual hashing and sliding-window fuzzy matching applied to camera-switch timings in the end-to-end method. |
| 19–20, 25 | PCT claim 15; detection component 130, retrieval component 140, reconstructed manifest 121′ and ledger search |
| 21, 28 | PCT claim 5; Tardos/probabilistic-fingerprinting passages; collusion discussion |

## 6. Counsel decisions and cautions

1. **Local substitution wording.** Confirm that “temporally corresponding frames” and the first-camera/second-camera formulation are the best US expressions of Example 2 and do not introduce an unintended synchronization requirement.
2. **Breadth versus D1.** Consider a broader production independent claim without actual frame-substitution language only if a narrower claim like claim 1 remains available. A generic relative-timing clause alone may be vulnerable to D1's frame-rate transformation.
3. **Restriction.** The production, distribution, and detection claims may invite a restriction requirement in a bypass case. Assess whether §371 unity practice or bypass restriction practice better serves the portfolio and whether divisional filings are budgeted.
4. **Divided infringement.** Claim 22 preserves the full combination but is not the primary enforcement claim where different parties perform the steps. Claims 1, 9, and 16 are intended to reduce that exposure.
5. **§112(f).** The processor/instruction format reduces reliance on nonce nouns, but counsel should still confirm whether any functional limitation invokes §112(f) and whether the disclosed algorithms are sufficient.
6. **Machine learning.** Claims 7 and 29 remain the thinnest-supported claims. Retain only as expendable dependents unless counsel identifies better support.
7. **No-watermark limitation.** Do not add a negative limitation to an independent claim merely to contrast D1. The specification expressly allows watermarking as a complementary layer.
8. **Eligibility.** Emphasize concrete processing of synchronized camera-source frames, edit instructions, adaptive-stream manifests, and detected shot boundaries. Do not describe the set as categorically §101-safe.
9. **CRM alternative.** If a medium claim is desired, draft it for the software operations of claim 1 or claim 16 rather than the entire production/distribution/detection chain.
10. **Official format.** If used as a §371 preliminary amendment, convert to compliant claim-status identifiers and amendment markings under 37 CFR 1.121. If used in a bypass filing, prepare it as original claim text with the correct continuity statement and specification package.
11. **Detection-claim functional relationship.** Claim 16 deliberately requires pattern derivation and matching at temporal regions where versions differ in selected camera views. Counsel should preserve that operational relationship, confirm written-description support, and avoid relying only on an intended-use or data-label statement that stored timings were “produced by” the mate process.
12. **Conditional collusion limitations.** Claims 21 and 28 affirmatively require suspected content assembled from different delivered versions before reciting probabilistic attribution. Counsel should preserve positive performance of the attribution operation and avoid optional “when” language in a method claim.
13. **Detection-dependent terminology.** Claims 17 and 18 expressly address detection of camera-source transitions and corresponding camera-switch timings to remain aligned with claim 16. Claim 19 intentionally remains timing-specific because it derives time codes and reconstructs manifest information from those time codes; do not broaden it merely for terminological symmetry.
