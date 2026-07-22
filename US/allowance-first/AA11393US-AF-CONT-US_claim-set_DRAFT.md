# AA11393US — AF Actor-Focused Continuation Candidate Claim Set (DRAFT)

> **STRATEGY AF-CONT · CLAIM-SET VERSION AF-CONT-2026-07-22-v2 · STATUS 22 JULY 2026**
>
> **INTERNAL COUNSEL-REVIEW DRAFT — NOT FILED — CONTINUATION NOT PRESERVED.** No successor application, application number, filing date, fee receipt, or recognized benefit relationship is recorded. This candidate does not establish copendency, benefit, priority, patentability, or filing approval.
>
> This reservation is controlled by [`AA11393US-AF-continuation-preservation_MEMO.md`](AA11393US-AF-continuation-preservation_MEMO.md). The responsible US attorney must confirm claim wording, § 101, § 102, § 103, § 112(a)/(b)/(f), support, effective date, inventorship, restriction, double patenting, fees, route, copendency, ADS/benefit data, and filing evidence.

## 1. Operative reservation architecture

The candidate preserves four actor-focused positions not exhausted by the AF parent. The production, distribution, and detector-system positions remain outside the parent; AF-CONT claim 14 is broader than AF claim 23, and AF-CONT claim 19 overlaps AF claim 23's causal-nexus formulation:

| Independent claim | Principal actor | Reserved operation |
|---:|---|---|
| 1 | Broadcaster, production facility, mate-generation vendor | Same ordered physical-camera transition at noncoincident reference/mate timings |
| 6 | Streaming platform, licensee, origin/CDN operator | Manifest delivery preserving one of two timings of the retained transition and recipient association |
| 11 | Monitoring provider, platform, rights owner | Delivered reference/mate manifest ledger, plural suspect cut-time derivation, reconstructed-manifest equality, and recipient lookup |
| 14 | Actor performing suspect analysis and ledger lookup | Affirmative detector-only method counterpart of claim 11 |

The candidate contains **19 total claims / 4 independent claims / 15 singly dependent claims / no multiple-dependent claims**. It leaves eleven total-claim positions below the 30-total Track One ceiling but no additional independent-claim position below the four-independent ceiling, subject to counsel confirming the rules and fees in force at filing. It is below the 20-total basic allocation but exceeds the three-independent basic allocation by one independent claim.

The final successor must record whether AF-CONT claims 14 and 19 are retained, differentiated, substituted, or omitted in light of AF claim 23's status, any parent restriction/election, claim differentiation, double patenting, terminal-disclaimer consequences, and current commercial need. This unfiled baseline preserves drafting options; it does not direct filing of duplicative scope.

No claim requires suspect-side identification of physical camera sources. AF-CONT claims 11–16 and 18–19 use plural detected camera-cut time codes, reconstructed manifests, equality to a delivered manifest, and recipient lookup. Physical-camera identity remains in the production and distribution structures of AF-CONT claims 1–10 and 17.

## 2. Candidate claims

### Production / mate-generation system

**1.** A system for generating distinguishable versions of audio-video content, the system comprising one or more processors and memory storing instructions that, when executed by the one or more processors, cause the system to:

receive video captured from a plurality of cameras and a structured list of instructions describing edits that produce reference audio-video content from the captured video, the structured list identifying source cameras and time codes for camera cuts at which selection changes from one camera of the plurality of cameras to another;

produce the reference audio-video content from the captured video according to the structured list of instructions;

automatically vary a time code of at least one camera cut in the structured list to produce a varied structured list; and

produce a mate of the reference audio-video content according to the varied structured list such that:

the at least one camera cut comprises, in the reference audio-video content, an ordered transition from a first camera to a second camera at a first camera-switch timing;

the mate contains the same ordered transition from the first camera to the second camera at a second camera-switch timing different from the first camera-switch timing; and

during a temporal interval between the first camera-switch timing and the second camera-switch timing, one of the reference audio-video content and the mate contains frames captured by the first camera and the other of the reference audio-video content and the mate contains temporally corresponding frames captured by the second camera.

**2.** The system of claim 1, wherein the structured list of instructions is an Edit Decision List identifying, for each of a plurality of cuts, a source camera, an in-point time code, and an out-point time code.

**3.** The system of claim 1, wherein the video is captured live from diverse viewpoints and the structured list records director-commanded real-time camera selections.

**4.** The system of claim 1, wherein automatically varying the time code comprises applying a respective time-code variation at each of a plurality of director-commanded camera cuts, such that, at each camera cut of the plurality of director-commanded camera cuts:

the reference audio-video content contains an ordered transition from a respective first camera to a respective second camera at a respective first camera-switch timing;

the mate contains the same ordered transition at a respective second camera-switch timing different from the respective first camera-switch timing; and

during a temporal interval between the respective first camera-switch timing and the respective second camera-switch timing, the reference audio-video content and the mate contain temporally corresponding frames captured by different cameras.

**5.** The system of claim 1, wherein the instructions further cause one or more audio or video elements not present in the reference audio-video content to be overlaid onto both the reference audio-video content and the mate.

### Distribution / recipient-association system

**6.** A content-distribution system comprising one or more servers, the one or more servers comprising one or more processors and memory storing instructions that, when executed by the one or more processors, cause the content-distribution system to:

receive a plurality of versions of audio-video content including a reference version and at least one mate version, wherein, within a defined temporal region:

the reference version contains an ordered transition from a first camera source to a second camera source at a first camera-switch timing;

the at least one mate version contains the same ordered transition from the first camera source to the second camera source at a second camera-switch timing different from the first camera-switch timing; and

during an interval between the first camera-switch timing and the second camera-switch timing, the reference version and the at least one mate version contain temporally corresponding frames captured by different cameras;

segment the plurality of versions into chunks;

generate a plurality of manifest files pointing to respective combinations of chunks selected from the plurality of versions, each respective combination causing an assembled audio-video stream to preserve, within the defined temporal region, either the first camera-switch timing or the second camera-switch timing of the ordered transition;

cause delivery, to respective recipients, of audio-video streams assembled according to respective manifest files; and

store, in a record of associations, associations between the respective recipients and the manifest files delivered to the respective recipients.

**7.** The content-distribution system of claim 6, wherein the chunks are distributed through a content delivery network using adaptive streaming and the manifest files are tailored to recipient devices or network conditions.

**8.** The content-distribution system of claim 6, wherein a mixing process integrates chunks of the reference version with chunks of the at least one mate version and progressively assigns distinguishable manifest files to recipients as additional camera-cut variations become available.

**9.** The content-distribution system of claim 6, wherein the record of associations is a ledger identifying an end user or group of end users that received each manifest file.

**10.** The content-distribution system of claim 6, wherein delivery of the audio-video streams comprises unicasting respective streams to the respective recipients.

### Detection / recipient-resolution system

**11.** A system for identifying a recipient associated with a suspected unauthorized distribution of audio-video content, the system comprising one or more processors and memory storing:

a ledger comprising associations between a plurality of delivered manifest files and respective recipients, each delivered manifest file identifying a respective combination of chunks selected from an ensemble comprising reference audio-video content and one or more mates of the reference audio-video content, each mate having at least one camera-cut timing different from a corresponding camera-cut timing of the reference audio-video content; and

instructions that, when executed by the one or more processors, cause the system to:

receive the suspected unauthorized distribution;

apply a scene-change detection algorithm to the suspected unauthorized distribution to identify a plurality of time codes of camera cuts in the suspected unauthorized distribution;

build one or more reconstructed manifest files from the plurality of identified time codes; and

search the ledger to identify a recipient associated with a delivered manifest file that is equal to one of the one or more reconstructed manifest files.

**12.** The system of claim 11, wherein identifying the plurality of time codes comprises comparing frames of the suspected unauthorized distribution with frames of one or both of the reference audio-video content and the one or more mates of the reference audio-video content using perceptual hashes of the frames.

**13.** The system of claim 12, wherein the comparing comprises fuzzy matching in which perceptual hashes of groups of frames are compared using sliding windows.

### Detector-only reconstructed-manifest method

**14.** A method of identifying a recipient associated with a suspected unauthorized distribution of audio-video content, the method comprising:

receiving the suspected unauthorized distribution;

applying a scene-change detection algorithm to the suspected unauthorized distribution to identify a plurality of time codes of camera cuts in the suspected unauthorized distribution;

building one or more reconstructed manifest files from the plurality of identified time codes; and

searching a ledger comprising associations between a plurality of delivered manifest files and respective recipients to identify a recipient associated with a delivered manifest file that is equal to one of the one or more reconstructed manifest files,

wherein each delivered manifest file identifies a respective combination of chunks selected from an ensemble comprising reference audio-video content and one or more mates of the reference audio-video content, each mate having at least one camera-cut timing different from a corresponding camera-cut timing of the reference audio-video content.

**15.** The method of claim 14, wherein identifying the plurality of time codes comprises comparing frames of the suspected unauthorized distribution with frames of one or both of the reference audio-video content and the one or more mates using perceptual hashes of the frames.

**16.** The method of claim 15, wherein the comparing comprises fuzzy matching in which perceptual hashes of groups of frames are compared using sliding windows.

### Recipient-to-recovered-combination fallbacks

**17.** The content-distribution system of claim 6, wherein:

at each of a plurality of camera cuts, the reference version contains an ordered transition from a respective first camera source to a respective second camera source at a respective reference camera-switch timing, and at least one mate version contains the same ordered transition at a respective different mate camera-switch timing;

each respective combination of chunks preserves, across the plurality of camera cuts, a recipient-associated combination of choices between the respective reference camera-switch timings and the respective different mate camera-switch timings;

at least one of the manifest files delivered to a respective recipient represents a recipient-associated combination that includes at least one of the respective different mate camera-switch timings; and

the record of associations associates the respective recipient with the at least one delivered manifest file.

**18.** The system of claim 11, wherein:

each delivered manifest file represents, across a plurality of camera cuts, a recipient-associated combination of choices between respective reference camera-cut timings and respective different mate camera-cut timings;

building the one or more reconstructed manifest files comprises generating a reconstructed manifest file representing a detected combination of camera-cut timings across the plurality of camera cuts; and

the delivered manifest file that is equal to the reconstructed manifest file represents a recipient-associated combination that includes at least one of the respective different mate camera-cut timings and matches the detected combination represented by the reconstructed manifest file.

**19.** The method of claim 14, wherein:

each delivered manifest file represents, across a plurality of camera cuts, a recipient-associated combination of choices between respective reference camera-cut timings and respective different mate camera-cut timings;

building the one or more reconstructed manifest files comprises generating a reconstructed manifest file representing a detected combination of camera-cut timings across the plurality of camera cuts; and

the delivered manifest file that is equal to the reconstructed manifest file represents a recipient-associated combination that includes at least one of the respective different mate camera-cut timings and matches the detected combination represented by the reconstructed manifest file.

## 3. Claim-as-a-whole support and effective-date gates

| Candidate claims | Current applicant support posture | Required filing decision |
|---|---|---|
| 1–5 | Claim 1 is **C/CE/G** for producing the reference according to the structured list and **D/CE/G** for the generalized same ordered first-camera-to-second-camera transition and temporally corresponding different-camera interval; claims 2–3 add direct limitations; claim 4 is **D/CE/G** for applying the complete retained-transition relationship at each of plural cuts; claim 5 is PCT-direct and provisional-combined for the same otherwise-absent element overlaid onto both versions | Determine PCT and provisional written description and enablement separately for claim 1 as a whole and assign Mode A, B, or C; determine claim 4 and claim 5's added relationships separately; record each dependent's inherited posture separately |
| 6–10 | Claim 6 is **D/CE/G** for the Examples 2→3→4 relationship from retained physical-camera transition through chunks, delivered manifest, and recipient record; claims 7–10 add direct limitations | Determine the complete relationship in each filing and assign Mode A, B, or C; record inherited and added-limitation conclusions separately |
| 11–13 | Claim 11 corresponds to applicant-assigned Mode A NA claim 16; claims 12–13 add directly disclosed comparison implementations | Counsel must confirm or reject Mode A through separate PCT/provisional written-description and enablement conclusions and record § 101, § 112(f), art, actor, and proof treatment |
| 14–16 | Claim 14 is **D/G; mode unassigned** as a method-form detector reservation; claims 15–16 add directly disclosed comparison implementations | Determine affirmative method support, delivered-manifest environment, written description, enablement, effective date, actor attribution, § 101, and art as a whole; assign Mode A, B, or C |
| 17 | Claim 6 plus a plural physical-camera timing-choice combination, an affirmative mate timing in a delivered recipient-associated manifest, and association of that manifest with the recipient; **D/CE/G** | Determine the complete recipient-associated timing-choice relationship and its inherited claim 6 posture; do not treat the added relationship as unqualified direct support |
| 18 | Claim 11 plus an equal delivered manifest containing an affirmative mate timing and a reconstructed manifest representing the same detected combination; **D/CE/G** | Confirm or reject inherited Mode A for claim 11 and separately determine the mate-containing delivered-combination → reconstructed same-combination relationship |
| 19 | Affirmative method counterpart of claim 18 beneath claim 14; **D/CE/G** | Assign claim 14 its own Mode A, B, or C and separately determine the added causal nexus, actor proof, eligibility, and art posture |

Claim 14's principal bases are provisional method claim 10(j)–(k), read with provisional claim 1(e), (g)–(n) and method claim 10(e), (g)–(i), and PCT Method 200 and claims 15–17, read with PCT claims 10–14. Claims 15–16 are supported by the provisional comparison claims and discussion and by PCT claims 2–3, the monitoring passages, and Example 5. The method claim does not inherit NA claim 16's Mode A label automatically.

A Mode B conclusion requires intervening-art review, including B10, before filing approval. A Mode C conclusion bars reliance on the affected formulation as drafted. Filing a continuation preserves qualifying pendency only; it does not create written description, enablement, or entitlement to the provisional date.

**Reconstruction and equality gate.** Counsel must determine whether each filing enables the full claimed operation of building a reconstructed manifest from noisy detected cut times and whether any functional language implicates § 112(f). Counsel must also select and use one supported construction of an “equal” manifest file—such as byte identity, equivalent chunk selections, or equivalent represented timing choices—and account for dynamic URLs, tokens, and metadata in definiteness, art, and infringement analysis.

## 4. Additional excluded gated reservations and headroom

The following limitations remain available for counsel review but are not included in this 19-claim baseline:

- later-cut resynchronization and the ten-frame implementation;
- retained source-camera identifiers in the varied structured list;
- paired same-interval chunks containing the transition at their respective timings;
- an equal matched manifest selecting a mate chunk with the full physical-camera transition geometry;
- probabilistic manifest-sequence contributor identification;
- overlay-before-segmentation method ordering;
- broader local alternate-camera substitution; and
- computer-readable-medium coverage.

Each additional claim requires an updated count and dependency check, inherited-parent analysis, separate support/effective-date disposition, current art scoring, and parent-versus-continuation placement decision. AF claim 23 and AF-CONT claim 19 require an express overlap and double-patenting treatment. No addition may introduce suspect-side physical-camera labeling or joint ordered-source-pair-plus-timing matching without a new written claim-as-a-whole support and enablement determination.

## 5. Actor and proof controls

AF-CONT claim 11 requires proof of the claimed detector system as a whole, including its stored ledger environment. If a monitoring provider only calls a ledger controlled by another entity, counsel must analyze whole-system use and control. AF-CONT claims 14 and 19, like AF claim 23, require affirmative performance of suspect acquisition, cut-time detection, reconstruction, and ledger search to identify a recipient, but not production or delivery. A monitor that supplies cut times or a reconstructed object while another entity's backend performs the search-to-identify operation does not necessarily perform the complete method; analyze API behavior, legally attributable performance, and the domestic location of every step.

AF-CONT claims 17–19 require proof that the actually delivered equal manifest contains an affirmative mate timing and, for claims 18–19, that the reconstructed manifest represents the same detected plural timing combination. DW-08C controls lawful multi-recipient captures, original manifests and chunks, session metadata, recipient associations, reconstruction and equality results, API and backend allocation evidence, actor/custodian and territorial mapping, and chain of custody. Observed facts, inference, and attorney argument must remain separately identified.

## 6. Filing and recursive preservation controls

This candidate becomes a preserved continuation position only when the conditions for `CONTINUATION PRESERVED` in the continuation memo are satisfied. Before then, its operative status is **NOT FILED — CONTINUATION NOT PRESERVED**.

If a qualifying successor containing some or all of these claims is filed and other supported commercial scope remains deferred, counsel must designate the next controlled parent and reapply AF-CONT-02 through AF-CONT-11. If no successor is authorized, the package must use the memo's `CHAIN CLOSED — DEFERRED SCOPE NOT PRESERVED` outcome and identify the relinquished positions.
