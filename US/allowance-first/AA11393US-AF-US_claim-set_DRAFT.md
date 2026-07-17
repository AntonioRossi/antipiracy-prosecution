# AA11393US — AF Allowance-First US Claim Strategy and Candidate Claim Set (DRAFT)

> **STRATEGY AF · CLAIM-SET VERSION AF-2026-07-17-v2 · STATUS 17 JULY 2026**
>
> **INTERNAL COUNSEL-REVIEW DRAFT — NOT FOR FILING AS-IS.** Use `AF claim N` outside the claim text. This branch is an allowance-first alternative to the normal-allowance (`NA`) branch; it does not replace the actor-focused NA claims or determine a filing route.
>
> Prepared for the US phase of PCT/IB2025/051755. US counsel must confirm wording, claim construction, § 101, § 102, § 103, § 112(a)/(b)/(f), restriction, inventorship, priority entitlement, fees, amendment format, and conformity with the selected § 371 or § 111(a) route.

## 1. AF objective and architecture

This branch deliberately places the disclosed production-to-attribution loop in **one independent system claim and one independent method claim that mirrors the complete operational chain**. Its allowance-first premise is that the strongest present distinction is not any isolated use of segmentation, manifests, timing fingerprints, shot detection, or a recipient ledger. It is the operational combination in which:

1. the same ordered transition between identified camera sources is deliberately placed at different times in generated versions;
2. the interval between those times consequently contains temporally corresponding frames from different cameras;
3. candidate transition patterns are derived from those generated and delivered versions and associated with recipients; and
4. a suspect is examined at the corresponding distinguishing region, with both source order and timing required to match before the recipient record is searched.

AF claim 1 therefore integrates the substance of NA claims 1, 7, 16, and 22 in system form, and AF claim 20 recites the same chain as affirmative method steps. Each output is used by a later operation: the varied edit instructions determine generated content; generated content determines delivered versions and candidate patterns; those patterns and deliveries populate the recipient record; and a jointly source-and-time-matched suspect pattern selects the record entry used for recipient identification. Neither independent claim is intended as a list of unrelated production, distribution, and detection operations.

This architecture trades enforcement breadth for a concentrated patentability position. It may be best suited to a vertically integrated operator or a system whose components are operated or controlled by one entity. The NA branch should remain available for subsystem and actor-focused coverage, whether in the initial case or in properly supported continuation/divisional practice selected by counsel.

## 2. Claim count and dependency control

| AF claim | Status | Depends from | Principal added limitation |
|---:|---|---:|---|
| 1 | Independent system | — | Integrated generation, delivery association, same-region structural detection, and recipient lookup |
| 2 | Dependent | 1 | Later-cut resynchronization |
| 3 | Dependent | 2 | Exact ten-frame Example 2 implementation |
| 4 | Dependent | 1 | EDL source-camera/in-point/out-point fields |
| 5 | Dependent | 1 | Live viewpoints and director-commanded switching |
| 6 | Dependent | 1 | Variations and patterns at plural recorded cuts |
| 7 | Dependent | 1 | Perceptual-hash transition detection |
| 8 | Dependent | 7 | Sliding-window fuzzy matching |
| 9 | Dependent | 1 | Manifest-based delivery and reconstructed manifest |
| 10 | Dependent | 9 | Delivered-manifest ledger lookup |
| 11 | Dependent | 1 | Mixed-version suspect and positive collusion attribution |
| 12 | Dependent | 11 | Segmented Tardos collusion analysis |
| 13 | Dependent | 1 | Chunk/manifest delivery preserving the claimed transition timing |
| 14 | Dependent | 13 | Equal-duration, same-interval chunks each spanning its transition |
| 15 | Dependent | 13 | Adaptive CDN delivery |
| 16 | Dependent | 13 | Reference/mate chunk mixing and progressive assignment |
| 17 | Dependent | 13 | Unicast delivery |
| 18 | Dependent | 13 | Manifest choices at plural distinguishing regions |
| 19 | Dependent | 13 | Additional overlaid audio/video elements |
| 20 | Independent method | — | Method twin of AF claim 1's complete generation-to-attribution chain |

**Count:** 20 total claims; 2 independent claims; 18 singly dependent claims; no multiple-dependent claims. AF claim 20 is included in the complete counsel-review proposal. Counsel may omit AF claim 20 at filing if the marginal simplicity of a one-independent posture is judged more important than the complementary method coverage; no separate AF claim-set document should be created for that filing choice.

## 3. Candidate claims

### Integrated allowance-first system

**1.** A system for generating recipient-associated distinguishable versions of audio-video content and identifying a source of a suspected unauthorized distribution of the audio-video content, the system comprising one or more processors and memory storing instructions that, when executed by the one or more processors, cause the system to:

receive video captured from a plurality of cameras and a structured list of edit instructions identifying source-camera identifiers and recorded time codes for camera cuts at which selection changes between cameras of the plurality of cameras;

produce reference audio-video content according to the structured list of edit instructions;

generate a mate of the reference audio-video content by varying, in the structured list of edit instructions, a recorded time code of a selected camera cut, the selected camera cut comprising an ordered transition at which selection changes from a first camera identified by a first source-camera identifier to a second camera identified by a second source-camera identifier, while retaining the ordered transition from the first camera to the second camera, such that:

the ordered transition occurs at a reference camera-switch timing in the reference audio-video content and at a different mate camera-switch timing in the mate; and

during an interval between the reference camera-switch timing and the mate camera-switch timing, the reference audio-video content and the mate contain temporally corresponding frames captured by different ones of the first camera and the second camera;

define a candidate-distinguishing temporal region that includes the interval;

cause delivery, to respective recipients, of respective generated versions including a version of the reference audio-video content and a version of the mate;

for each delivered version, generate a candidate camera-source-transition pattern from the source-camera identifiers and a camera-switch timing actually present in the delivered version at the candidate-distinguishing temporal region, the candidate camera-source-transition pattern identifying the first camera, the second camera, the ordered transition from the first camera to the second camera, and either the reference camera-switch timing or the mate camera-switch timing;

store, in a record of associations, an association among the delivered version, its candidate camera-source-transition pattern, and the recipient to which the delivered version was delivered;

receive the suspected unauthorized distribution;

detect, at the candidate-distinguishing temporal region in the suspected unauthorized distribution, an ordered transition between camera sources and a camera-switch timing of the detected ordered transition;

derive a detected camera-source-transition pattern identifying the camera sources on respective sides of the detected ordered transition and the camera-switch timing of the detected ordered transition;

identify, from candidate camera-source-transition patterns generated for the delivered versions, a candidate camera-source-transition pattern for which both the ordered transition between the camera sources and the camera-switch timing at the candidate-distinguishing temporal region match the detected camera-source-transition pattern; and

search the record of associations to identify a recipient associated with the matching candidate camera-source-transition pattern or its delivered version.

### Priority-gated production fallbacks

> **EXAMPLE 2 PRIORITY GATE — DO NOT FILE OR RELY ON AF CLAIMS 2–3 WITHOUT A WRITTEN COUNSEL DETERMINATION.** The provisional's mate EDL table and corrective sentence disclose restoration at `00:00:30:01`, but the same paragraph also contains the stray `00:00:30:11` “mistake” sentence; the PCT text is cleaned. Counsel must determine written-description support, priority entitlement, and whether the PCT wording is a permissible clarification before these claims are used as a material patentability position. Keep resynchronization out of AF claims 1 and 20 unless that review supports moving it.

**2.** The system of claim 1, wherein the instructions cause the system to preserve, in the mate, a timing of a later camera cut from the reference audio-video content, thereby restoring synchronization between the mate and the reference audio-video content from the later camera cut onward.

**3.** The system of claim 2, wherein varying the recorded time code causes the mate camera-switch timing to occur ten frames later than the reference camera-switch timing, extends a selection of the first camera by ten frames, correspondingly shortens a following selection of the second camera, and restores synchronization at the later camera cut.

### Production-record and repeated-region fallbacks

**4.** The system of claim 1, wherein the structured list of edit instructions is an edit decision list identifying, for each of a plurality of camera cuts, a source camera, an in-point time code, and an out-point time code.

**5.** The system of claim 1, wherein the video is captured live from diverse viewpoints and the structured list of edit instructions records director-commanded real-time selections among the plurality of cameras.

**6.** The system of claim 1, wherein the instructions cause the system to vary respective recorded time codes of a plurality of director-commanded camera cuts, define a respective candidate-distinguishing temporal region for each varied camera cut, and generate and store, for each delivered version, a candidate camera-source-transition pattern identifying an ordered camera-source transition and a camera-switch timing at each respective candidate-distinguishing temporal region.

### Detection fallbacks

**7.** The system of claim 1, wherein detecting the ordered transition between the camera sources and the camera-switch timing comprises comparing frames of the suspected unauthorized distribution with temporally corresponding frames of one or both of the reference audio-video content and the mate using perceptual hashes of the frames.

**8.** The system of claim 7, wherein the comparing comprises fuzzy matching in which perceptual hashes of groups of frames are compared using sliding windows.

**9.** The system of claim 1, wherein:

causing delivery of the respective generated versions comprises causing delivery according to respective manifest files;

the record of associations further associates each respective manifest file with the candidate camera-source-transition pattern of the delivered version assembled according to the respective manifest file; and

the instructions further cause the system to derive a time code from the camera-switch timing of the detected ordered transition and build one or more reconstructed manifest files from the derived time code.

**10.** The system of claim 9, wherein the record of associations is a ledger associating manifest files delivered to end-user accounts with the end-user accounts, and searching the record of associations comprises searching the ledger for an end-user account associated with a delivered manifest file matching the one or more reconstructed manifest files.

### Collusion fallbacks

**11.** The system of claim 1, wherein the suspected unauthorized distribution comprises portions obtained from different delivered versions, and wherein the instructions further cause the system to apply a probabilistic fingerprinting algorithm to candidate camera-source-transition patterns associated with a plurality of recipients and identify one or more recipients whose delivered versions contributed respective portions to the suspected unauthorized distribution.

**12.** The system of claim 11, wherein the probabilistic fingerprinting algorithm comprises a segmented Tardos fingerprinting algorithm that applies respective fingerprints to content segments and identifies at least one contributing recipient for at least one of the respective portions.

### Manifest/chunk distribution fallbacks

**13.** The system of claim 1, wherein the instructions further cause the system to:

segment the reference audio-video content and the mate into chunks;

generate a plurality of manifest files pointing to respective combinations of chunks selected from the reference audio-video content and the mate, each respective combination causing an assembled audio-video stream to preserve, at the candidate-distinguishing temporal region, either the reference camera-switch timing or the mate camera-switch timing of the ordered transition from the first camera to the second camera;

cause delivery of the respective generated versions as audio-video streams assembled according to respective manifest files; and

for each delivered audio-video stream, store, in the record of associations, an association among the respective manifest file, the candidate camera-source-transition pattern preserved by the assembled audio-video stream, and the recipient to which the assembled audio-video stream was delivered.

**14.** The system of claim 13, wherein, for the candidate-distinguishing temporal region:

a first manifest file points to a first chunk selected from the reference audio-video content;

a second manifest file, different from the first manifest file, points to a second chunk selected from the mate;

the first chunk and the second chunk span the same playback interval and have equal playback durations;

the first chunk contains frames from the first camera before the reference camera-switch timing and frames from the second camera after the reference camera-switch timing; and

the second chunk contains frames from the first camera before the mate camera-switch timing and frames from the second camera after the mate camera-switch timing.

**15.** The system of claim 13, wherein the chunks are distributed through a content delivery network using adaptive streaming and the manifest files are tailored to recipient devices or network conditions.

**16.** The system of claim 13, wherein a mixing process integrates chunks of the reference audio-video content with chunks of one or more mates and progressively assigns distinguishable manifest files to recipients as additional varied camera cuts become available.

**17.** The system of claim 13, wherein causing delivery of the respective generated versions comprises unicasting respective audio-video streams to the respective recipients.

**18.** The system of claim 13, wherein the respective combinations of chunks preserve recipient-associated choices, at a plurality of candidate-distinguishing temporal regions, between a reference camera-switch timing and a different mate camera-switch timing of a respective ordered transition between identified camera sources.

**19.** The system of claim 13, wherein the instructions further cause one or more audio or video elements not present in the video received from the plurality of cameras to be overlaid onto at least one of the reference audio-video content or the mate before segmentation into the chunks.

### Integrated allowance-first method

**20.** A method for generating recipient-associated distinguishable versions of audio-video content and identifying a source of a suspected unauthorized distribution of the audio-video content, the method comprising:

receiving video captured from a plurality of cameras and a structured list of edit instructions identifying source-camera identifiers and recorded time codes for camera cuts at which selection changes between cameras of the plurality of cameras;

producing reference audio-video content according to the structured list of edit instructions;

generating a mate of the reference audio-video content by varying, in the structured list of edit instructions, a recorded time code of a selected camera cut, the selected camera cut comprising an ordered transition at which selection changes from a first camera identified by a first source-camera identifier to a second camera identified by a second source-camera identifier, while retaining the ordered transition from the first camera to the second camera, such that:

the ordered transition occurs at a reference camera-switch timing in the reference audio-video content and at a different mate camera-switch timing in the mate; and

during an interval between the reference camera-switch timing and the mate camera-switch timing, the reference audio-video content and the mate contain temporally corresponding frames captured by different ones of the first camera and the second camera;

defining a candidate-distinguishing temporal region that includes the interval;

causing delivery, to respective recipients, of respective generated versions including a version of the reference audio-video content and a version of the mate;

for each delivered version, generating a candidate camera-source-transition pattern from the source-camera identifiers and a camera-switch timing actually present in the delivered version at the candidate-distinguishing temporal region, the candidate camera-source-transition pattern identifying the first camera, the second camera, the ordered transition from the first camera to the second camera, and either the reference camera-switch timing or the mate camera-switch timing;

storing, in a record of associations, an association among the delivered version, its candidate camera-source-transition pattern, and the recipient to which the delivered version was delivered;

receiving the suspected unauthorized distribution;

detecting, at the candidate-distinguishing temporal region in the suspected unauthorized distribution, an ordered transition between camera sources and a camera-switch timing of the detected ordered transition;

deriving a detected camera-source-transition pattern identifying the camera sources on respective sides of the detected ordered transition and the camera-switch timing of the detected ordered transition;

identifying, from candidate camera-source-transition patterns generated for the delivered versions, a candidate camera-source-transition pattern for which both the ordered transition between the camera sources and the camera-switch timing at the candidate-distinguishing temporal region match the detected camera-source-transition pattern; and

searching the record of associations to identify a recipient associated with the matching candidate camera-source-transition pattern or its delivered version.

## 4. Why this order is allowance-first

| Tier | AF claims | Function in prosecution |
|---|---|---|
| Integrated structural core | 1, 20 | Requires the full closed loop and joint source-pair/timing match at the same distinguishing region in complementary system and method forms |
| Production-record fallbacks | 2–6 | Adds resynchronization, the concrete EDL, live direction, or repeated cut regions before relying on generic distribution machinery |
| Detection fallbacks | 7–10 | Adds disclosed comparison and reconstruction operations while retaining AF claim 1's structural source-and-time match |
| Collusion fallbacks | 11–12 | Requires a positive contributor-identification output and preserves a segmented Tardos implementation; does not treat “Tardos” as a novelty label by itself |
| Distribution fallbacks | 13–19 | Adds chunks, manifests, CDN, mixing, unicast, repeated regions, or overlays only after the camera-source boundary mechanism is already present |

Known implementations such as perceptual hashing, fuzzy matching, manifests, adaptive streaming, recipient ledgers, and probabilistic tracing are intentionally dependent limitations. Their role is to provide concrete implementation and combination fallbacks, not to imply that each is independently novel.

## 5. Support and filing gates

1. **AF claims 1 and 20 claim-as-a-whole gate.** The PCT and provisional disclose the overall generation, manifest/recipient association, detection, and lookup architecture in system and method form. The exact same-region relationship and joint matching of both source order and timing are an abstraction formed by reading the Example 2 production disclosure with the detection and retrieval disclosure. Counsel must provide separate claim-as-a-whole § 112(a) and priority analyses for AF claims 1 and 20; isolated support for each noun and the method's substantive correspondence to the system do not replace those analyses.
2. **Source-identity detection gate.** Generic cut-time detection is express. Detecting the identities of both camera sources on the two sides of a suspect transition, and matching that ordered pair together with timing, is not stated with the same specificity in the detection example. AF claims 1, 20, and 7–10 must not be represented as having settled direct support for that operation.
3. **Examples 2–5 integration gate.** AF claims 1, 20, 7–10, and 13–18 combine the moved boundary between identified cameras in Example 2 with later manifest, mixing, comparison, or reconstruction passages. Counsel must decide whether the application presents those operations as one integrated system or method and whether the provisional supports the same combination.
4. **Example 2 priority gate.** Apply the express AF claims 2–3 gate above. Revisit the priority and disclosure posture if intervening information is identified with a potentially material effective prior-art date between 26 February 2024 and 19 February 2025, or if any Office questions priority.
5. **AF claim 14 gate.** Equal-duration corresponding reference/mate chunks are express, but the proposition that each paired same-interval chunk itself spans the ordered transition between identified cameras at its respective internal timing is not stated verbatim in one passage. Treat AF claim 14 as a combined-example fallback pending counsel review.
6. **Collusion-output gate.** General Tardos/probabilistic collusion handling and segmented Tardos codes are disclosed. Confirm support for AF claim 11's use of recipient-associated candidate camera-source-transition patterns as the algorithm input and AF claim 12's relationship between respective portions and contributing recipients; preserve positive identification rather than optional invocation of an algorithm.
7. **Overlay sequencing gate.** The overlay feature is express, but AF claim 19 specifies overlay before segmentation. Counsel must verify that the disclosed pipeline order supports that sequence and revise the dependency or wording if necessary.

The separate AF priority/support map records the limitation-level basis and grades direct, contextual, combined-example, and gated support. It should be reviewed together with the as-filed source documents, not used as a substitute for them.

## 6. Enforcement and portfolio cautions

1. **Actor and proof analysis.** AF claims 1 and 20 each span production, delivery/association, detection, and lookup. A validity-oriented allowance anchor is not necessarily the best infringement claim. Counsel should separately analyze direction/control or joint-enterprise attribution for the method steps, whole-system use for the system claim, divided infringement, and available evidence. AF claim 20 adds a complementary claim format; it does not cure the actor-split risk or improve the prior-art position.
2. **Preserve the NA actor split.** Do not abandon the NA production, distribution, and detection families merely because AF claims 1 and 20 are narrower. Use continuation, divisional, or parallel-claim planning only as supported and commercially justified.
3. **Proof burden.** The same ordered source pair, two noncoincident timings, alternate-camera interval, candidate pattern, same-region detection, and recipient association each may require technical discovery. Plan controlled captures from multiple recipient sessions and preserve edit-list, manifest, chunk, and association evidence where available.
4. **Functional claiming.** The processor-and-memory format does not itself eliminate § 112(f) or algorithm-sufficiency issues. Counsel should confirm structural and algorithmic support for every function.
5. **No negative watermark limitation.** The claims do not require absence of watermarking. The specification permits complementary watermarking, and the camera-boundary mechanism should be claimed positively.
6. **Eligibility, restriction, and unity.** The method twin can add eligibility and divided-infringement questions and may modestly increase restriction or election complexity. The production, distribution, and detection subject matter in either independent can still raise search, unity, restriction, or election issues. Route-specific consequences remain for counsel.

## 7. Track One and formal check

- **Numerical check:** 20 total / 2 independent / no multiple-dependent claim. The set is within the 30-total/4-independent/no-multiple-dependent numerical limits applicable to Track One and exactly uses the basic 20-total allocation while remaining below the basic 3-independent allocation.
- **No-headroom rule still matters:** if this set is used in prioritized examination, every amendment must remain within the then-applicable Track One limits. Counsel should verify the current rule and filing mechanics at filing and coordinate any additions with cancellations if required.
- **Route check:** Track One is a § 111(a) prioritized-examination procedure and is not available merely by making a direct § 371 national-stage entry. Counsel must confirm whether a bypass continuation is selected and satisfy all route-specific requirements.
- **Claim-form check:** AF claims 1 and 20 are independent; all 18 dependents refer to one earlier claim; no multiple-dependent claims appear. AF claim 20 affirmatively mirrors AF claim 1's complete operational chain. Convert the draft to the filing route's required original-claim or amendment format and recheck antecedent basis, claim status, and fees.
- **Substantive caveat:** satisfying a numerical or formal check says nothing about patentability, support, priority, eligibility, enforceability, or allowance. This document recommends no legal conclusion without counsel review.

## 8. Revision record

- **AF-2026-07-17-v2 (17 July 2026):** repaired first recitation of the ordered transition in AF claim 1; added independent method AF claim 20 as an affirmative twin of the complete AF claim 1 chain; updated the 20-total/2-independent topology, support gates, enforcement cautions, filing-choice direction, and narrative exact-language alignment. No separate system-only AF package is created; counsel may omit AF claim 20 from the single AF proposal if a one-independent filing posture is selected.
