# AA11393US — AF Allowance-First US Claim Strategy and Candidate Claim Set (DRAFT)

> **STRATEGY AF · CLAIM-SET VERSION AF-2026-07-22-v6 · STATUS 22 JULY 2026**
>
> **INTERNAL COUNSEL-REVIEW DRAFT — NOT FOR FILING AS-IS.** Use `AF claim N` outside the claim text. This branch is an allowance-first alternative to the normal-allowance (`NA`) branch; it does not replace the actor-focused NA claims or determine a filing route.
>
> Prepared for the US phase of PCT/IB2025/051755. US counsel must confirm wording, claim construction, § 101, § 102, § 103, § 112(a)/(b)/(f), restriction, inventorship, priority entitlement, fees, amendment format, and conformity with the selected § 371 or § 111(a) route.

## 1. AF objective and architecture

This branch contains **one independent system claim and one independent method claim that each recite the complete production-to-attribution chain, together with one monitor-side independent method claim directed to the disclosed recipient-recovery operation**. Its allowance-first premise is that the strongest present distinction is not any isolated use of segmentation, manifests, timing fingerprints, shot detection, or a recipient ledger. For AF claims 1 and 19, it is the operational combination in which:

1. successive edit entries identify different physical source cameras and their in-point and out-point time codes;
2. recorded time codes at a plurality of director-commanded cuts are varied while the source-camera identifiers and their order are retained, producing reference and mate versions with noncoincident timings for the retained camera transitions;
3. manifest files direct delivery of respective combinations of reference and mate chunks and are associated with recipients in a ledger; and
4. plural camera-cut time codes detected in suspected content are used to build one or more reconstructed manifest files, and the ledger is searched for the recipient associated with an equal delivered manifest file.

AF claim 1 recites that integrated system, and AF claim 19 recites the same chain as affirmative method steps. AF claim 20 provides a causal-nexus fallback requiring an affirmative mate-timing choice in the delivered recipient-associated combination and reconstruction of the same detected timing-choice combination. AF claims 21–22 provide a support-safe perceptual-hash and sliding-window detection branch. Each output in the integrated claims is used by a later operation: the edit instructions determine the reference and mates; those versions supply the chunks selected by delivered manifests; the delivered manifests populate the recipient ledger; and plural detected cut time codes produce the reconstructed-manifest object used for recipient identification.

AF claim 23 places suspect acquisition, plural cut-time derivation, reconstruction, and ledger search to identify a recipient in one affirmative monitor-side method. Its searched-ledger environment requires delivered reference/mate chunk-combination manifests, and the equal delivered manifest must contain an affirmative mate timing and match the same detected plural timing combination represented by the reconstruction. It does not require the monitoring actor to produce, segment, deliver, or record the reference/mate versions and does not require suspect-side identification of physical camera sources.

The integrated claims trade enforcement breadth for a concentrated patentability position and may be best suited to a vertically integrated operator or a system whose components are operated or controlled by one entity. AF claim 23 targets a narrower direct-performer position but carries a materially more exposed recovery-side art, eligibility, support, restriction, and proof posture. The NA branch should remain available for production, distribution, detection-system, and broader method coverage, whether in the initial case or in properly supported continuation/divisional practice selected by counsel.

## 2. Claim count and dependency control

| AF claim | Status | Depends from | Principal added limitation |
|---:|---|---:|---|
| 1 | Independent system | — | Plural recorded camera-boundary variation, manifest delivery/association, plural cut-time reconstruction, and recipient lookup |
| 2 | Dependent | 1 | Later-cut resynchronization |
| 3 | Dependent | 2 | Exact ten-frame Example 2 implementation |
| 4 | Dependent | 1 | Edit Decision List implementation |
| 5 | Dependent | 1 | Live viewpoints and director-commanded switching |
| 6 | Dependent | 1 | Respective single-cut mates for the plural selected cuts |
| 7 | Dependent | 1 | Perceptual-hash cut-time detection |
| 8 | Dependent | 7 | Sliding-window fuzzy matching |
| 9 | Dependent | 1 | Adaptive CDN delivery and device/network-tailored manifests |
| 10 | Dependent | 1 | Reference/mate chunk mixing and progressive manifest assignment |
| 11 | Dependent | 1 | Mixed-version suspect and manifest-sequence collusion attribution |
| 12 | Dependent | 11 | Segmented Tardos collusion analysis |
| 13 | Dependent | 1 | Equal-duration reference/mate chunks for a common playback interval |
| 14 | Dependent | 13 | Paired chunks containing the retained transition at their respective timings |
| 15 | Dependent | 1 | Blockchain registration of manifest-recipient associations |
| 16 | Dependent | 1 | Unicast delivery |
| 17 | Dependent | 1 | Recipient-associated reference/mate timing choices across the plural selected cuts |
| 18 | Dependent | 1 | Additional overlaid audio/video elements before segmentation |
| 19 | Independent method | — | Method twin of AF claim 1's complete generation-to-attribution chain |
| 20 | Dependent | 19 | Affirmative mate timing in a recipient combination and reconstruction of the same detected timing-choice combination |
| 21 | Dependent | 19 | Perceptual-hash cut-time detection |
| 22 | Dependent | 21 | Sliding-window fuzzy matching |
| 23 | Independent method | — | Monitor-side reconstruction and ledger lookup with an affirmative mate timing in the equal delivered manifest and the same detected plural timing combination |

**Count:** 23 total claims; 3 independent claims; 20 singly dependent claims; no multiple-dependent claims. All claims are included in the complete counsel-review proposal. AF claims 19–22 form the integrated method family; AF claim 23 is a separately standing monitor-side method. Any filing decision that omits either family must be recorded in the filed topology and every claim-indexed package document. Omission or cancellation of AF claim 19 requires corresponding omission or cancellation of AF claims 20–22. No separate AF claim-set document should be created for a filing subset.

AF claims 20–22 provide method-narrowing tiers beneath AF claim 19. AF claim 20 preserves the delivered-combination-to-reconstructed-combination causal nexus but carries the relationship-specific support gate stated below. AF claims 21–22 form a separate directly supported detection branch so that they do not inherit AF claim 20's gate. None cures AF claim 19's performance-attribution or divided-infringement risk. AF claim 23 is drafted to reduce that actor split only where one monitoring entity performs every affirmative recovery operation, including the ledger search to identify the recipient, or another performer's conduct is legally attributable to that entity under the applicable method-claim standard. The continuation reservation separately carries broader and complementary actor-focused candidates—including the broader detector-only method and commercially useful NA claims 23–30—subject to copendency, support, art, and business-value controls.

## 3. Candidate claims

### Integrated allowance-first system

**1.** A system for generating recipient-associated distinguishable versions of audio-video content and identifying a recipient associated with a suspected unauthorized distribution of the audio-video content, the system comprising one or more processors and memory storing instructions that, when executed by the one or more processors, cause the system to:

receive video captured from a plurality of cameras and a structured list of edit instructions comprising, for each of a plurality of director-commanded camera cuts, a first edit entry comprising an out-point time code and a first source-camera identifier identifying a first camera of the plurality of cameras as a first source camera, and a following edit entry comprising an in-point time code and a second source-camera identifier identifying a second camera of the plurality of cameras as a second source camera different from the first source camera;

produce reference audio-video content according to the structured list of edit instructions;

generate one or more mates of the reference audio-video content by, for each of a plurality of selected camera cuts among the director-commanded camera cuts, modifying, in the structured list of edit instructions, the out-point time code of the corresponding first edit entry and the in-point time code of the corresponding following edit entry while retaining the first and second source-camera identifiers and the order of the first and second source cameras, such that, for each selected camera cut:

a transition from the first source camera to the second source camera occurs at a reference camera-switch timing in the reference audio-video content and at a later mate camera-switch timing in at least one of the one or more mates; and

in the at least one mate, selection of the first source camera is extended from the reference camera-switch timing to the later mate camera-switch timing and selection of the second source camera begins at the later mate camera-switch timing;

segment an ensemble comprising the reference audio-video content and the one or more mates into chunks;

generate a plurality of manifest files pointing to respective combinations of chunks selected from the ensemble;

cause delivery of streamed audio-video content to respective recipients according to respective manifest files of the plurality of manifest files;

store, in a ledger, associations between the respective manifest files and the recipients to which the streamed audio-video content was delivered according to the respective manifest files;

receive the suspected unauthorized distribution;

apply a scene-change detection algorithm to the suspected unauthorized distribution to identify a plurality of time codes of camera cuts in the suspected unauthorized distribution;

build one or more reconstructed manifest files from the plurality of identified time codes; and

search the ledger to identify a recipient associated with a delivered manifest file that is equal to one of the one or more reconstructed manifest files.

### Priority-gated production fallbacks

> **EXAMPLE 2 PRIORITY GATE — DO NOT FILE OR RELY ON AF CLAIMS 2–3 WITHOUT A WRITTEN COUNSEL DETERMINATION.** The provisional's mate EDL table and corrective sentence disclose restoration at `00:00:30:01`, but the same paragraph also contains the stray `00:00:30:11` “mistake” sentence; PCT Example 2 states restoration at `00:00:30:01` and does not contain the `00:00:30:11` value. Counsel must determine written-description support, priority entitlement, and whether the PCT wording is a permissible clarification before these claims are used as a material patentability position. Keep resynchronization out of AF claims 1 and 19 unless that review supports moving it.

**2.** The system of claim 1, wherein the instructions cause the system to preserve, in at least one of the one or more mates, a timing of a later camera cut from the reference audio-video content, thereby restoring synchronization between that mate and the reference audio-video content from the later camera cut onward.

**3.** The system of claim 2, wherein modifying the out-point and in-point time codes causes the mate camera-switch timing for one of the selected camera cuts to occur ten frames later than the corresponding reference camera-switch timing, extends selection of the first source camera by ten frames, correspondingly shortens a following selection of the second source camera, and restores synchronization at the later camera cut.

### Production-record fallbacks

**4.** The system of claim 1, wherein the structured list of edit instructions is an Edit Decision List.

**5.** The system of claim 1, wherein the video is captured live from diverse viewpoints and the structured list of edit instructions records the director-commanded camera cuts as real-time selections among the plurality of cameras.

**6.** The system of claim 1, wherein the instructions cause the system to generate a respective mate for each selected camera cut, each respective mate differing from the reference audio-video content in the modified out-point and in-point time codes for only that selected camera cut.

### Detection fallbacks

**7.** The system of claim 1, wherein identifying the plurality of time codes comprises comparing frames of the suspected unauthorized distribution with frames of one or both of the reference audio-video content and the one or more mates using perceptual hashes of the frames.

**8.** The system of claim 7, wherein the comparing comprises fuzzy matching in which perceptual hashes of groups of frames are compared using sliding windows.

### Delivery fallbacks

**9.** The system of claim 1, wherein the chunks are distributed through a content delivery network using adaptive streaming and the plurality of manifest files is tailored to recipient devices or network conditions.

**10.** The system of claim 1, wherein a mixing process integrates chunks of the reference audio-video content with chunks of the one or more mates and progressively assigns respective manifest files to recipients as additional selected camera cuts become available.

### Collusion fallbacks

**11.** The system of claim 1, wherein the suspected unauthorized distribution comprises portions obtained from streamed audio-video content delivered according to different manifest files, and wherein the instructions further cause the system to apply a probabilistic fingerprinting algorithm to recipient-associated sequences of chunk selections represented by the delivered manifest files and identify one or more recipients whose delivered streamed audio-video content contributed respective portions to the suspected unauthorized distribution.

**12.** The system of claim 11, wherein the probabilistic fingerprinting algorithm comprises a segmented Tardos fingerprinting algorithm that applies respective fingerprints to content segments and identifies at least one contributing recipient for at least one of the respective portions.

### Manifest/chunk fallbacks

**13.** The system of claim 1, wherein a first manifest file points to a first chunk selected from the reference audio-video content and a second manifest file points to a second chunk selected from one of the one or more mates, the first chunk and the second chunk spanning the same playback interval and having equal playback durations.

**14.** The system of claim 13, wherein, for one of the selected camera cuts:

the first chunk contains frames from the corresponding first source camera before the reference camera-switch timing and frames from the corresponding second source camera after the reference camera-switch timing; and

the second chunk contains frames from the corresponding first source camera before the mate camera-switch timing and frames from the corresponding second source camera after the mate camera-switch timing.

**15.** The system of claim 1, further comprising a blockchain registration component configured to register the associations between the respective manifest files and recipients in a blockchain and to read the respective manifest files and recipients in the ledger.

**16.** The system of claim 1, wherein causing delivery comprises unicasting respective streamed audio-video content to the respective recipients.

**17.** The system of claim 1, wherein each respective combination of chunks preserves, across the plurality of selected camera cuts, a recipient-associated combination of reference camera-switch timings and later mate camera-switch timings, and the ledger associates the respective manifest file representing that combination with the recipient.

**18.** The system of claim 1, wherein the instructions further cause one or more audio or video elements not present in the video received from the plurality of cameras to be overlaid onto at least one of the reference audio-video content or the one or more mates before segmentation into the chunks.

### Integrated allowance-first method

**19.** A method for generating recipient-associated distinguishable versions of audio-video content and identifying a recipient associated with a suspected unauthorized distribution of the audio-video content, the method comprising:

receiving video captured from a plurality of cameras and a structured list of edit instructions comprising, for each of a plurality of director-commanded camera cuts, a first edit entry comprising an out-point time code and a first source-camera identifier identifying a first camera of the plurality of cameras as a first source camera, and a following edit entry comprising an in-point time code and a second source-camera identifier identifying a second camera of the plurality of cameras as a second source camera different from the first source camera;

producing reference audio-video content according to the structured list of edit instructions;

generating one or more mates of the reference audio-video content by, for each of a plurality of selected camera cuts among the director-commanded camera cuts, modifying, in the structured list of edit instructions, the out-point time code of the corresponding first edit entry and the in-point time code of the corresponding following edit entry while retaining the first and second source-camera identifiers and the order of the first and second source cameras, such that, for each selected camera cut:

a transition from the first source camera to the second source camera occurs at a reference camera-switch timing in the reference audio-video content and at a later mate camera-switch timing in at least one of the one or more mates; and

in the at least one mate, selection of the first source camera is extended from the reference camera-switch timing to the later mate camera-switch timing and selection of the second source camera begins at the later mate camera-switch timing;

segmenting an ensemble comprising the reference audio-video content and the one or more mates into chunks;

generating a plurality of manifest files pointing to respective combinations of chunks selected from the ensemble;

delivering streamed audio-video content to respective recipients according to respective manifest files of the plurality of manifest files;

storing, in a ledger, associations between the respective manifest files and the recipients to which the streamed audio-video content was delivered according to the respective manifest files;

receiving the suspected unauthorized distribution;

applying a scene-change detection algorithm to the suspected unauthorized distribution to identify a plurality of time codes of camera cuts in the suspected unauthorized distribution;

building one or more reconstructed manifest files from the plurality of identified time codes; and

searching the ledger to identify a recipient associated with a delivered manifest file that is equal to one of the one or more reconstructed manifest files.

### Integrated-method fallback ladder

**20.** The method of claim 19, wherein:

each respective combination of chunks preserves, across the plurality of selected camera cuts, a recipient-associated combination of choices between the reference camera-switch timings and the later mate camera-switch timings;

building the one or more reconstructed manifest files comprises generating a reconstructed manifest file representing a detected combination of camera-switch timings across the plurality of selected camera cuts; and

the delivered manifest file that is equal to the reconstructed manifest file represents a recipient-associated combination that includes at least one of the later mate camera-switch timings and matches the detected combination represented by the reconstructed manifest file.

**21.** The method of claim 19, wherein identifying the plurality of time codes comprises comparing frames of the suspected unauthorized distribution with frames of one or both of the reference audio-video content and the one or more mates using perceptual hashes of the frames.

**22.** The method of claim 21, wherein the comparing comprises fuzzy matching in which perceptual hashes of groups of frames are compared using sliding windows.

### Monitor-side reconstructed-manifest method

**23.** A method of identifying a recipient associated with a suspected unauthorized distribution of audio-video content, the method comprising:

receiving the suspected unauthorized distribution;

applying a scene-change detection algorithm to the suspected unauthorized distribution to identify a plurality of time codes of camera cuts in the suspected unauthorized distribution;

building one or more reconstructed manifest files from the plurality of identified time codes, the one or more reconstructed manifest files including a reconstructed manifest file representing a detected combination of camera-cut timings across a plurality of camera cuts; and

searching a ledger comprising associations between a plurality of delivered manifest files and respective recipients to identify a recipient associated with a delivered manifest file that is equal to the reconstructed manifest file,

wherein each of the plurality of delivered manifest files identifies a respective combination of chunks selected from an ensemble comprising reference audio-video content and one or more mates of the reference audio-video content, each mate having at least one camera-cut timing different from a corresponding camera-cut timing of the reference audio-video content,

wherein each of the plurality of delivered manifest files represents, across the plurality of camera cuts, a recipient-associated combination of choices between respective reference camera-cut timings and respective different mate camera-cut timings, and

wherein the delivered manifest file that is equal to the reconstructed manifest file represents a recipient-associated combination that includes at least one of the respective different mate camera-cut timings and matches the detected combination represented by the reconstructed manifest file.

## 4. Why this order is allowance-first

| Tier | AF claims | Function in prosecution |
|---|---|---|
| Integrated reconstructed-manifest core | 1, 19 | Requires plural physical-camera edit-boundary variations, manifest delivery/association, plural suspect cut-time derivation, reconstructed-manifest building, and recipient lookup in complementary system and method forms |
| Production-record fallbacks | 2–6 | Adds resynchronization, the concrete EDL implementation, live direction, or respective single-cut mates |
| Detection fallbacks | 7–8 | Adds directly disclosed perceptual-hash and sliding-window comparison implementations to plural cut-time detection |
| Delivery fallbacks | 9–10, 13–17 | Adds adaptive CDN delivery, mixing, concrete paired chunks, blockchain registration, unicast, or plural recipient-associated timing choices |
| Collusion fallbacks | 11–12 | Requires a positive contributor-identification output and preserves a segmented Tardos implementation; does not treat “Tardos” as a novelty label by itself |
| Pipeline fallback | 18 | Adds pre-segmentation overlays |
| Integrated-method fallbacks | 20–22 | Add a delivered-to-reconstructed timing-choice causal nexus with an affirmative mate choice and a separate perceptual-hash/sliding-window implementation branch, without changing AF claim 19's actor-attribution posture |
| Monitor-side recovery independent | 23 | Places the affirmative suspect-analysis and lookup chain with one monitoring actor while retaining the mate-containing delivered-combination-to-reconstructed-combination nexus as the recovery-side patentability position |

Known implementations such as perceptual hashing, fuzzy matching, manifests, adaptive streaming, recipient ledgers, and probabilistic tracing are intentionally dependent limitations. Their role is to provide concrete implementation and combination fallbacks, not to imply that each is independently novel.

## 5. Support and filing gates

1. **AF claims 1 and 19 claim-as-a-whole gate.** Provisional system claim 1 and method claim 10 and PCT claims 1 and 10–17 disclose the generation, manifest/recipient association, plural cut-time detection, reconstructed-manifest building, and lookup architecture in system and method form. Counsel must separately determine the support and priority of each independent as a whole, including the relationship between the plural modified camera boundaries and the manifest reconstructed from plural suspect cut time codes.
2. **Production-boundary generalization gate.** Example 2 directly shows successive Camera 2 and Camera 3 entries, retention of those camera identities and their order, extension of the Camera 2 selection, and delayed commencement of Camera 3. Counsel must confirm the first-source-camera/second-source-camera generalization across a plurality of selected director-commanded cuts and the claim's out-point/in-point formulation.
3. **Per-filing support modes and separate enablement.** For AF claims 1 and 19, counsel must separately conclude PCT written description and enablement, provisional written description and enablement for benefit entitlement, and effective date, then assign each claim its own Mode A, B, or C under the shared DW-05A framework. Enablement is a separate, evidence-dependent inquiry and must not be inferred from either a positive or negative written-description conclusion.
4. **Plural-cut reconstructed-manifest integration gate.** Plural cut-time variation, manifest generation/delivery, plural suspect cut-time derivation, reconstructed-manifest building, and ledger lookup are express in the filings. Counsel must confirm that each filing conveys their complete relationship to the strengthened successive-source-camera edit-entry formulation recited in AF claims 1 and 19 and the exact timing-choice combination recited in AF claim 17.
5. **AF claim 6 respective-mate gate.** The filings disclose variation at individual and plural camera cuts and geometric growth in available versions. Counsel must confirm the claim's relationship in which a respective mate differs at only one corresponding selected cut.
6. **Example 2 priority gate.** Apply the express AF claims 2–3 gate above. Revisit the priority and disclosure posture if intervening information is identified with a potentially material effective prior-art date between 26 February 2024 and 19 February 2025, or if any Office questions priority.
7. **AF claim 14 gate.** Equal-duration corresponding reference/mate chunks are express, but the proposition that each paired same-interval chunk itself spans the retained transition between identified cameras at its respective internal timing is not stated verbatim in one passage. Treat AF claim 14 as a combined-example fallback pending counsel review.
8. **Collusion-output gate.** General Tardos/probabilistic collusion handling, manifest-associated chunk combinations, segmented Tardos codes, and positive source-account identification are disclosed. Confirm support for AF claim 11's use of recipient-associated manifest chunk-selection sequences as the probabilistic input and AF claim 12's relationship between respective portions and contributing recipients. Preserve positive identification rather than optional invocation of an algorithm.
9. **Overlay sequencing gate.** The overlay feature is express, but AF claim 18 specifies overlay before segmentation. Counsel must verify that the disclosed pipeline order supports that sequence and revise the wording if necessary.
10. **Method fallback ladder.** AF claim 20 combines disclosed plural timing choices, manifest associations, and reconstructed-manifest recovery, but the exact delivered recipient-combination → affirmative mate choice → reconstruction of the same detected combination relationship is **D/CE/G** and requires counsel determination. AF claims 21–22 add directly disclosed perceptual-hash and sliding-window implementations and depend from AF claim 19 and AF claim 21, respectively. Each inherits AF claim 19's claim-as-a-whole, priority, enablement, eligibility, performance-attribution, and art posture; none supplies an independent cure for divided infringement.
11. **Monitor-side method gate.** AF claim 23's affirmative suspect-acquisition, scene-change detection, plural cut-time derivation, reconstruction, and ledger-search-to-identify operations are direct components of provisional method claim 10(j)–(k) and PCT Method 200/claims 16–17. The detector-only base method is **D/G; mode unassigned**; the method-form searched-ledger and passive delivered-manifest relationship and the mate-containing delivered-combination → reconstruction of the same detected combination nexus are **D/CE/G**. AF claim 23 as a whole is **D/CE/G; mode unassigned** and inherits neither NA claim 16's system-format Mode A assignment nor AF claim 19's integrated-method mode. Counsel must determine written description and enablement in each filing, effective date, the limiting effect of the passive ledger and manifest environment, the construction of manifest equality, actor performance, § 101, § 112(f), and the claim as a whole before filing or reliance.

The separate AF priority/support map records the direct bases for the reconstructed-manifest chain and the remaining production-boundary, integration, monitor-method, collusion, chunk-geometry, and overlay gates. The NA actor-focused claims remain the production, distribution, detection-system, and broader-method alternatives.

## 6. Enforcement and portfolio cautions

1. **Actor and proof analysis.** AF claims 1 and 19–22 span production, delivery/association, detection, and lookup. Counsel should separately analyze direction/control or joint-enterprise attribution for AF claim 19's method steps, whole-system use for AF claim 1, divided infringement, and available evidence. AF claim 23 does not require production or delivery by the monitoring actor, but direct infringement still requires one entity to perform suspect acquisition, cut-time derivation, reconstruction, and the ledger search to identify the recipient, or requires another performer's conduct to be legally attributable to that entity under the applicable method-claim standard. A vendor that merely supplies cut times or a reconstructed object while another entity performs the search-to-identify operation may remain outside the complete method.
2. **Preserve the remaining NA actor split.** Do not abandon the NA production, distribution, detection-system, or broader method families merely because AF claim 23 targets one monitoring configuration. Use continuation, divisional, or parallel-claim planning only as supported and commercially justified.
3. **Proof burden.** The successive source-camera entries, modified out-point and in-point time codes, plural noncoincident transition timings, delivered manifests, detected suspect cut time codes, reconstructed manifest, recipient association, performer of the ledger search, and recipient-identification output each may require technical discovery. Plan controlled captures from multiple recipient sessions and preserve edit-list, manifest, chunk, detection, association, query, and result evidence where available.
4. **Functional claiming.** The processor-and-memory format does not itself eliminate § 112(f) or algorithm-sufficiency issues. Counsel should confirm structural and algorithmic support for every function.
5. **No negative watermark limitation.** The claims do not require absence of watermarking. The specification permits complementary watermarking, and the camera-boundary mechanism should be claimed positively.
6. **Eligibility, restriction, and unity.** The integrated and monitor-side methods add distinct eligibility, actor, and proof questions. AF claim 23 is a separately useful recovery subcombination with a materially different art and examination focus from the integrated production-to-attribution claims, so restriction or election exposure is meaningful although not automatic. Counsel must plan election, traversal, rejoinder, continuation/divisional treatment, and any § 121 consequences without assuming that AF claim 23 will be examined or issue with AF claim 1.
7. **AF claim 23 eligibility pre-mortem.** The claim may be characterized as receiving content, extracting timing data, building a data representation, searching associated records, and returning a recipient association. The delivered-manifest and mate-timing relationships do not by themselves establish eligibility. Counsel must identify the asserted judicial exception under Step 2A Prong One, analyze integration into a practical application under Step 2A Prong Two, analyze the additional elements individually and as an ordered combination under Step 2B, and identify specification support and evidence for any asserted improvement to content identification, streaming security, or computer operation. Do not rely solely on a field-of-use label, generic manifest or ledger implementation, or the desired identification result.

## 7. Track One and formal check

- **Numerical check:** 23 total / 3 independent / no multiple-dependent claim. The set is within the 30-total/4-independent/no-multiple-dependent numerical limits applicable to Track One and exceeds the basic 20-total allocation by three claims; counsel must confirm the resulting excess-claim fees and all other filing requirements.
- **No-headroom rule still matters:** if this set is used in prioritized examination, every amendment must remain within the then-applicable Track One limits. Counsel should verify the current rule and filing mechanics at filing and coordinate any additions with cancellations if required.
- **Route check:** Track One is a § 111(a) prioritized-examination procedure and is not available merely by making a direct § 371 national-stage entry. Counsel must confirm whether a bypass continuation is selected and satisfy all route-specific requirements.
- **PTA economics:** Track One targets accelerated final disposition, not necessarily patent issuance. It may produce little or no Office-delay patent term adjustment that might otherwise accrue, but it neither fixes PTA at zero nor determines the final adjustment. Counsel must use case-specific Office-delay, applicant-delay, remaining-term, cost, and continuation-timing assumptions.
- **Claim-form check:** AF claims 1, 19, and 23 are independent; all 20 dependents refer to one earlier claim; no multiple-dependent claims appear. AF claim 19 affirmatively mirrors AF claim 1's complete operational chain; AF claim 20 depends from AF claim 19; AF claims 21–22 form the separate chain `19 → 21 → 22`; and AF claim 23 affirmatively recites the monitor-side recovery chain without depending from the integrated method. Convert the draft to the filing route's required original-claim or amendment format and recheck antecedent basis, claim status, and fees.
- **Substantive caveat:** satisfying a numerical or formal check says nothing about patentability, support, priority, eligibility, enforceability, or allowance. This document recommends no legal conclusion without counsel review.
