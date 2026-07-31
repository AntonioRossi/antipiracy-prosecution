<a id="ssp-aa11393us-na-us-claim-set-root"></a>

<a id="ssp-aa11393us-na-us-claim-set-header-00001"></a>
# AA11393US — NA Claim Strategy and Candidate Claim Set (DRAFT)

<a id="ssp-aa11393us-na-us-claim-set-blockquote-00002"></a>
> <a id="ssp-aa11393us-na-us-claim-set-para-00003"></a>
> **STRATEGY NA · CLAIM-SET VERSION NA-2026-07-30-v5 · STATUS 30 JULY 2026**
>
> <a id="ssp-aa11393us-na-us-claim-set-para-00004"></a>
> **COUNSEL-REVIEW DRAFT — NOT FOR FILING AS-IS.** Use `NA claim N` outside the claim text.
>
> <a id="ssp-aa11393us-na-us-claim-set-para-00005"></a>
> Prepared for ordinary US national-stage entry under 35 U.S.C. § 371 of PCT/IB2025/051755. This document proposes an actor-focused claim architecture organized around the editing-domain anchor — the per-cut ordered-transition timing-choice chain from edit instructions through manifest chunk selections to reconstructed-manifest attribution — with a candidate fallback ladder and express support gates. US counsel must confirm wording, claim construction, § 101, § 102, § 103, § 112(a)/(b)/(f), antecedent basis, restriction, fees, benefit entitlement, and national-stage amendment format. Filing and successor controls are canonical in [`../common/`](../../common/README.md).

<a id="ssp-aa11393us-na-us-claim-set-header-00006"></a>
## 1. Operative architecture

<a id="ssp-aa11393us-na-us-claim-set-para-00007"></a>
The candidate set uses three independent claims, each directed to a single likely commercial operator and each reciting the anchor on its own side:

<a id="ssp-aa11393us-na-us-claim-set-table-00008"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00009"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00013"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00017"></a>

| <a id="ssp-aa11393us-na-us-claim-set-plain-00010"></a> Independent NA claim | <a id="ssp-aa11393us-na-us-claim-set-plain-00011"></a> Primary actor / infringement target | <a id="ssp-aa11393us-na-us-claim-set-plain-00012"></a> Core limitation |
| --- | --- | --- |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00014"></a> 1 — production system | <a id="ssp-aa11393us-na-us-claim-set-plain-00015"></a> Broadcaster, production facility, mate-generation vendor | <a id="ssp-aa11393us-na-us-claim-set-plain-00016"></a> Same ordered first-camera-to-second-camera transition at noncoincident reference/mate timings, with temporally corresponding different-camera frames in the intervening interval |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00018"></a> 9 — distribution system | <a id="ssp-aa11393us-na-us-claim-set-plain-00019"></a> Streaming platform, licensee, CDN/origin operator | <a id="ssp-aa11393us-na-us-claim-set-plain-00020"></a> Manifest/chunk selections preserving, per defined temporal region, one of two positions of the same ordered camera-source transition, encoding timing-choice sequences associated with recipients via the stored record |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00022"></a> 15 — detection system | <a id="ssp-aa11393us-na-us-claim-set-plain-00023"></a> Monitoring provider, platform, rights owner | <a id="ssp-aa11393us-na-us-claim-set-plain-00024"></a> Delivered manifests over a per-cut ordered-transition ensemble representing recipient-associated timing-choice combinations; plural suspect cut-time detection; reconstructed-manifest building representing the detected combination; equal-manifest lookup requiring an affirmative mate timing |

<a id="ssp-aa11393us-na-us-claim-set-para-00025"></a>
The set contains **20 total claims / 3 independent claims / 17 singly dependent claims / no multiple-dependent claims**. It is within the basic 20-total/three-independent allocation; no excess-claim fees are expected. Counsel must verify unity, restriction exposure, and national-stage mechanics.

<a id="ssp-aa11393us-na-us-claim-set-para-00026"></a>
No operative NA claim requires suspect-side identification of physical camera sources. Physical-camera identity remains in production and distribution structures, in the per-cut delivered-side ensemble environment of NA claim 15, and in the matched-manifest geometry of NA claim 18. Suspect recovery in NA claims 15 and 18 uses the disclosed cut-time/reconstructed-manifest/equality path.

<a id="ssp-aa11393us-na-us-claim-set-header-00027"></a>
## 2. Drafting principles

1. <a id="ssp-aa11393us-na-us-claim-set-orderedlist-00028"></a> <a id="ssp-aa11393us-na-us-claim-set-list-item-00029"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00030"></a> **Production core.** “Different videos” is insufficient. NA claim 1 requires local reassignment of a temporal interval from one physical camera source to another around a recorded camera cut.
2. <a id="ssp-aa11393us-na-us-claim-set-list-item-00031"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00032"></a> **D1 response.** D1 does not itself disclose alternate-camera frame selection. Counsel must nevertheless test combinations with conventional multicamera production, A20, B9, A4, A6, B6, and A13.
3. <a id="ssp-aa11393us-na-us-claim-set-list-item-00033"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00034"></a> **Anchor fold.** The timing-choice nexus — manifest combinations preserving per-cut choices between the two timings of the same ordered transition, reconstructed-manifest representation of the detected combination, and a match requiring an affirmative mate timing — is recited in the independent claims, not held as fallback. Perceptual hashes, fuzzy matching, sliding windows, and Tardos variants appear only as dependent implementation rungs and are never load-bearing for patentability.
4. <a id="ssp-aa11393us-na-us-claim-set-list-item-00035"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00036"></a> **Direct detector object.** NA claim 15 operates on delivered manifests over a per-cut ordered-transition ensemble representing recipient-associated timing-choice combinations, plural detected camera-cut time codes, and reconstructed manifests. Perceptual hashing, fuzzy matching, matched-manifest physical-camera geometry, and probabilistic tracing remain dependent implementations.
5. <a id="ssp-aa11393us-na-us-claim-set-list-item-00037"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00038"></a> **Single-actor independents.** Each independent claim is performable by one commercial operator; no infringement case depends on direction-and-control attribution. The former end-to-end method family is removed from this set and reserved.
6. <a id="ssp-aa11393us-na-us-claim-set-list-item-00039"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00040"></a> **No mandatory watermark disclaimer.** The claims remain open to complementary watermarking.
7. <a id="ssp-aa11393us-na-us-claim-set-list-item-00041"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00042"></a> **Processor language.** Processor-and-memory wording does not eliminate § 112(f), definiteness, or algorithm-sufficiency review.
8. <a id="ssp-aa11393us-na-us-claim-set-list-item-00043"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00044"></a> **Per-filing support.** Direct component support does not decide a strengthened claim relationship as a whole. Written description and enablement require separate conclusions for the PCT and provisional.

<a id="ssp-aa11393us-na-us-claim-set-header-00045"></a>
## 3. Candidate claims

<a id="ssp-aa11393us-na-us-claim-set-header-00046"></a>
### Production / mate-generation system

<a id="ssp-claim-1"></a>
**1.** A system for generating distinguishable versions of audio-video content, the system comprising one or more processors and memory storing instructions that, when executed by the one or more processors, cause the system to:
<a id="ssp-claim-1-limitation-1"></a>

receive video captured from a plurality of cameras and a structured list of instructions describing edits that produce reference audio-video content from the captured video, the structured list identifying source cameras and time codes for camera cuts at which selection changes from one camera of the plurality of cameras to another;
<a id="ssp-claim-1-limitation-2"></a>

automatically vary a time code of at least one camera cut in the structured list to produce a varied structured list; and
<a id="ssp-claim-1-limitation-3"></a>

produce a mate of the reference audio-video content according to the varied structured list such that:
<a id="ssp-claim-1-limitation-4"></a>

the at least one camera cut comprises, in the reference audio-video content, an ordered transition from a first camera to a second camera at a first camera-switch timing;
<a id="ssp-claim-1-limitation-5"></a>

the mate contains the same ordered transition from the first camera to the second camera at a second camera-switch timing different from the first camera-switch timing; and
<a id="ssp-claim-1-limitation-6"></a>

during a temporal interval between the first camera-switch timing and the second camera-switch timing, one of the reference audio-video content and the mate contains frames captured by the first camera and the other of the reference audio-video content and the mate contains temporally corresponding frames captured by the second camera.

<a id="ssp-claim-2"></a>
**2.** <a id="ssp-claim-2-limitation-1"></a> The system of claim 1, wherein the instructions cause the system to preserve in the mate a timing of a later camera cut from the reference audio-video content, thereby restoring synchronization between the mate and the reference audio-video content from the later camera cut onward.

<a id="ssp-claim-3"></a>
**3.** <a id="ssp-claim-3-limitation-1"></a> The system of claim 2, wherein varying the time code extends a camera selection in the mate by ten frames, delays a following camera selection by ten frames, and restores synchronization at the later camera cut.

<a id="ssp-claim-4"></a>
**4.** <a id="ssp-claim-4-limitation-1"></a> The system of claim 1, wherein the structured list of instructions is an Edit Decision List identifying, for each of a plurality of cuts, a source camera, an in-point time code, and an out-point time code.

<a id="ssp-claim-5"></a>
**5.** <a id="ssp-claim-5-limitation-1"></a> The system of claim 1, wherein the video is captured live from diverse viewpoints and the structured list records director-commanded real-time camera selections.

<a id="ssp-claim-6"></a>
**6.** <a id="ssp-claim-6-limitation-1"></a> The system of claim 1, wherein the instructions cause the system to apply a time-code variation at each of a plurality of director-commanded camera cuts.

<a id="ssp-claim-7"></a>
**7.** <a id="ssp-claim-7-limitation-1"></a> The system of claim 1, wherein the structured list records the ordered transition using an identifier of the first camera, an identifier of the second camera, and a recorded time code corresponding to the first camera-switch timing, and wherein the varied structured list retains the identifiers of the first camera and the second camera on respective sides of the ordered transition and records, in place of the recorded time code, a different recorded time code corresponding to the second camera-switch timing.

<a id="ssp-claim-8"></a>
**8.** <a id="ssp-claim-8-limitation-1"></a> The system of claim 1, wherein the instructions further cause one or more audio or video elements not present in the video received from the plurality of cameras to be overlaid onto at least one of the reference audio-video content or the mate.

<a id="ssp-aa11393us-na-us-claim-set-header-00047"></a>
### Distribution / recipient-association system

<a id="ssp-claim-9"></a>
**9.** A content-distribution system comprising one or more servers, the one or more servers comprising one or more processors and memory storing instructions that, when executed by the one or more processors, cause the content-distribution system to:
<a id="ssp-claim-9-limitation-1"></a>

receive a plurality of versions of audio-video content including a reference version and one or more mate versions, wherein, within each of a plurality of defined temporal regions:
<a id="ssp-claim-9-limitation-2"></a>

the reference version contains an ordered transition from a first camera source to a second camera source at a first camera-switch timing;
<a id="ssp-claim-9-limitation-3"></a>

at least one of the one or more mate versions contains the same ordered transition from the first camera source to the second camera source at a second camera-switch timing different from the first camera-switch timing; and
<a id="ssp-claim-9-limitation-4"></a>

during an interval between the first camera-switch timing and the second camera-switch timing, the reference version and that mate version contain temporally corresponding frames captured by different cameras;
<a id="ssp-claim-9-limitation-5"></a>

segment the plurality of versions into chunks;
<a id="ssp-claim-9-limitation-6"></a>

generate a plurality of manifest files pointing to respective combinations of chunks selected from the plurality of versions, each respective combination causing an assembled audio-video stream to preserve, within each of the plurality of defined temporal regions, either the first camera-switch timing or the second camera-switch timing of the ordered transition, whereby each respective combination encodes a respective sequence of timing choices across the plurality of defined temporal regions;
<a id="ssp-claim-9-limitation-7"></a>

cause delivery, to respective recipients, of audio-video streams assembled according to respective manifest files; and
<a id="ssp-claim-9-limitation-8"></a>

store, in a record of associations, associations between the respective recipients and the manifest files delivered to the respective recipients.

<a id="ssp-claim-10"></a>
**10.** <a id="ssp-claim-10-limitation-1"></a> The content-distribution system of claim 9, wherein the chunks are distributed through a content delivery network using adaptive streaming and the manifest files are tailored to recipient devices or network conditions.

<a id="ssp-claim-11"></a>
**11.** <a id="ssp-claim-11-limitation-1"></a> The content-distribution system of claim 9, wherein a mixing process integrates chunks of the reference version with chunks of one or more mate versions and progressively assigns distinguishable manifest files to recipients as additional camera-cut variations become available.

<a id="ssp-claim-12"></a>
**12.** The content-distribution system of claim 9, wherein, for one of the plurality of defined temporal regions:
<a id="ssp-claim-12-limitation-1"></a>

a first manifest file of the plurality of manifest files points to a first chunk selected from the reference version;
<a id="ssp-claim-12-limitation-2"></a>

a second manifest file of the plurality of manifest files, different from the first manifest file, points to a second chunk selected from one of the one or more mate versions;
<a id="ssp-claim-12-limitation-3"></a>

the first chunk and the second chunk each span the same playback interval and have equal playback durations;
<a id="ssp-claim-12-limitation-4"></a>

the first chunk contains frames from the first camera source before the first camera-switch timing and frames from the second camera source after the first camera-switch timing; and
<a id="ssp-claim-12-limitation-5"></a>

the second chunk contains frames from the first camera source before the second camera-switch timing and frames from the second camera source after the second camera-switch timing.

<a id="ssp-claim-13"></a>
**13.** <a id="ssp-claim-13-limitation-1"></a> The content-distribution system of claim 9, wherein delivery of the audio-video streams comprises unicasting respective streams to the respective recipients.

<a id="ssp-claim-14"></a>
**14.** <a id="ssp-claim-14-limitation-1"></a> The content-distribution system of claim 9, wherein the record of associations is a ledger identifying an end user or group of end users that received each manifest file.

<a id="ssp-aa11393us-na-us-claim-set-header-00048"></a>
### Detection / recipient-resolution system

<a id="ssp-claim-15"></a>
**15.** A system for identifying a recipient associated with a suspected unauthorized distribution of audio-video content, the system comprising one or more processors and memory storing:
<a id="ssp-claim-15-limitation-1"></a>

a ledger comprising associations between a plurality of delivered manifest files and respective recipients, each delivered manifest file identifying a respective combination of chunks selected from an ensemble comprising reference audio-video content and one or more mates of the reference audio-video content, wherein, for each of a plurality of camera cuts, the reference audio-video content contains an ordered transition from a respective first camera source to a respective second camera source at a respective reference camera-cut timing, and at least one of the one or more mates contains the same ordered transition at a respective different mate camera-cut timing, and wherein each delivered manifest file represents, across the plurality of camera cuts, a recipient-associated combination of choices between the respective reference camera-cut timings and the respective different mate camera-cut timings; and
<a id="ssp-claim-15-limitation-2"></a>

instructions that, when executed by the one or more processors, cause the system to:
<a id="ssp-claim-15-limitation-3"></a>

receive the suspected unauthorized distribution;
<a id="ssp-claim-15-limitation-4"></a>

apply a scene-change detection algorithm to the suspected unauthorized distribution to identify a plurality of time codes of camera cuts in the suspected unauthorized distribution;
<a id="ssp-claim-15-limitation-5"></a>

build one or more reconstructed manifest files from the plurality of identified time codes, the one or more reconstructed manifest files including a reconstructed manifest file representing a detected combination of camera-cut timings across the plurality of camera cuts; and
<a id="ssp-claim-15-limitation-6"></a>

search the ledger to identify a recipient associated with a delivered manifest file that is equal to the reconstructed manifest file, the delivered manifest file that is equal to the reconstructed manifest file representing a recipient-associated combination that includes at least one of the respective different mate camera-cut timings and matches the detected combination represented by the reconstructed manifest file.

<a id="ssp-claim-16"></a>
**16.** <a id="ssp-claim-16-limitation-1"></a> The system of claim 15, wherein identifying the plurality of time codes comprises comparing frames of the suspected unauthorized distribution with frames of one or both of reference audio-video content and one or more mates of the reference audio-video content using perceptual hashes of the frames.

<a id="ssp-claim-17"></a>
**17.** <a id="ssp-claim-17-limitation-1"></a> The system of claim 16, wherein the comparing comprises fuzzy matching in which perceptual hashes of groups of frames are compared using sliding windows.

<a id="ssp-claim-18"></a>
**18.** <a id="ssp-claim-18-limitation-1"></a> The system of claim 15, wherein the delivered manifest file that is equal to the reconstructed manifest file identifies at least one chunk selected from a mate of the one or more mates, the at least one chunk spans a temporal region of the ensemble that contains an ordered transition of one of the plurality of camera cuts, and, during an interval between the respective reference camera-cut timing of that ordered transition and the respective different mate camera-cut timing of that ordered transition in the mate, the reference audio-video content and the mate contain temporally corresponding frames captured by different cameras.

<a id="ssp-claim-19"></a>
**19.** <a id="ssp-claim-19-limitation-1"></a> The system of claim 15, wherein the suspected unauthorized distribution comprises portions obtained from delivered versions associated with different delivered manifest files, and wherein the instructions further cause the system to apply a probabilistic fingerprinting algorithm to recipient-associated sequences of chunk selections represented by the delivered manifest files and identify one or more recipients whose delivered versions contributed respective portions to the suspected unauthorized distribution.

<a id="ssp-claim-20"></a>
**20.** <a id="ssp-claim-20-limitation-1"></a> The system of claim 19, wherein the probabilistic fingerprinting algorithm comprises a segmented Tardos fingerprinting algorithm that applies respective fingerprints to content segments and identifies at least one contributing recipient for at least one of the respective portions.

<a id="ssp-aa11393us-na-us-claim-set-header-00049"></a>
## 4. Fallback ladder and art purpose

<a id="ssp-aa11393us-na-us-claim-set-table-00050"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00051"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00055"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00059"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00063"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00067"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00071"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00075"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00079"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00083"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00087"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00091"></a>

| <a id="ssp-aa11393us-na-us-claim-set-plain-00052"></a> Fallback | <a id="ssp-aa11393us-na-us-claim-set-plain-00053"></a> NA claims | <a id="ssp-aa11393us-na-us-claim-set-plain-00054"></a> Principal purpose |
| --- | --- | --- |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00056"></a> Production-side ordered physical-camera transition at noncoincident timings | <a id="ssp-aa11393us-na-us-claim-set-plain-00057"></a> 1, 6–7, 9, 12 | <a id="ssp-aa11393us-na-us-claim-set-plain-00058"></a> Preserve the structural camera-boundary distinction over completed-copy transformations and generic stream switching |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00060"></a> Later-cut resynchronization | <a id="ssp-aa11393us-na-us-claim-set-plain-00061"></a> 2–3 | <a id="ssp-aa11393us-na-us-claim-set-plain-00062"></a> Distinguish uniform delay and global retiming; subject to the Example 2 priority gate |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00064"></a> Production-record implementations | <a id="ssp-aa11393us-na-us-claim-set-plain-00065"></a> 4–6 | <a id="ssp-aa11393us-na-us-claim-set-plain-00066"></a> EDL form, live director-commanded switching, and plural-cut variation |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00068"></a> Per-region mate reference and paired-chunk geometry | <a id="ssp-aa11393us-na-us-claim-set-plain-00069"></a> 9, 12 | <a id="ssp-aa11393us-na-us-claim-set-plain-00070"></a> Bind delivery objects to the physical-camera boundary represented by the chunks, with per-region assignment to one of one or more mates |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00072"></a> Detector-only per-cut ensemble and reconstruction | <a id="ssp-aa11393us-na-us-claim-set-plain-00073"></a> 15 | <a id="ssp-aa11393us-na-us-claim-set-plain-00074"></a> Single-actor recipient resolution over the per-cut ordered-transition ensemble with the folded detected-combination nexus and affirmative mate-timing match |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00076"></a> Matched-manifest physical-camera geometry | <a id="ssp-aa11393us-na-us-claim-set-plain-00077"></a> 18 | <a id="ssp-aa11393us-na-us-claim-set-plain-00078"></a> Require the equal delivered manifest to select a mate chunk spanning a per-cut retained transition at its noncoincident timing |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00080"></a> Perceptual-hash and fuzzy comparison | <a id="ssp-aa11393us-na-us-claim-set-plain-00081"></a> 16–17 | <a id="ssp-aa11393us-na-us-claim-set-plain-00082"></a> Concrete cut-time detection implementations |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00084"></a> Positive collusion attribution | <a id="ssp-aa11393us-na-us-claim-set-plain-00085"></a> 19 | <a id="ssp-aa11393us-na-us-claim-set-plain-00086"></a> Identify contributing recipients from recipient-associated manifest sequences |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00088"></a> Segmented Tardos implementation | <a id="ssp-aa11393us-na-us-claim-set-plain-00089"></a> 20 | <a id="ssp-aa11393us-na-us-claim-set-plain-00090"></a> Per-segment fingerprint localization of pirated segments and colluders |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00092"></a> Delivery implementations | <a id="ssp-aa11393us-na-us-claim-set-plain-00093"></a> 10, 11, 13, 14 | <a id="ssp-aa11393us-na-us-claim-set-plain-00094"></a> Adaptive CDN delivery, progressive mixing, unicast, and end-user ledger forms |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00096"></a> Pipeline fallback | <a id="ssp-aa11393us-na-us-claim-set-plain-00097"></a> 8 | <a id="ssp-aa11393us-na-us-claim-set-plain-00098"></a> Additional overlaid audio/video elements on reference or mate |

<a id="ssp-aa11393us-na-us-claim-set-header-00099"></a>
## 5. Support and filing gates

1. <a id="ssp-aa11393us-na-us-claim-set-orderedlist-00100"></a> <a id="ssp-aa11393us-na-us-claim-set-list-item-00101"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00102"></a> **Production relationship.** Example 2 directly shows Camera 2 followed by Camera 3, extension of Camera 2, delayed commencement of Camera 3, and noncoincident transition timings. Counsel must determine the generalized same-ordered-transition and different-camera-interval formulations in NA claims 1, 6, 7, 9, and 12.
2. <a id="ssp-aa11393us-na-us-claim-set-list-item-00103"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00104"></a> **Example 2 resynchronization.** NA claims 2–3 require a written determination addressing the provisional's stray `00:00:30:11` sentence and the table/corrective text showing restoration at `00:00:30:01`.
3. <a id="ssp-aa11393us-na-us-claim-set-list-item-00105"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00106"></a> **Distribution integration.** Examples 2–4 disclose camera-boundary variation, chunks, manifest combinations, and recipient association. NA claim 9 is a plural-region generalization of the formerly single-region distribution claim and encodes the respective sequence of timing choices in the generate step with association supplied by the store step; counsel must conclude written description and enablement per filing and determine the objective scope of the sequence formulation (the former NA claim 15 construction gate, now at independent level).
4. <a id="ssp-aa11393us-na-us-claim-set-list-item-00107"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00108"></a> **Detection independent — folded nexus.** NA claim 15 carries former NA claim 20's plural timing-combination gate and a per-cut ordered-transition ensemble environment at independent level; the applicant grades the folded relationships **D/CE/G**. Former NA claim 16's DW-05A Mode A assignment does not carry automatically to the strengthened wording; counsel must re-run the per-filing mode analysis for NA claim 15 as a whole, including provisional benefit entitlement.
5. <a id="ssp-aa11393us-na-us-claim-set-list-item-00109"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00110"></a> **Matched-manifest geometry.** NA claim 18 retains a combined-example gate for the matched manifest's mate chunk spanning a per-cut retained physical-camera transition.
6. <a id="ssp-aa11393us-na-us-claim-set-list-item-00111"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00112"></a> **Collusion.** Confirm NA claim 19's use of recipient-associated manifest chunk-selection sequences as the probabilistic input and its respective-portion contributor output. NA claim 20's segmented-Tardos species is directly disclosed; its segment/fingerprint/portion/contributor relationship inherits the analogue of operative AF claim 12's open gate.
7. <a id="ssp-aa11393us-na-us-claim-set-list-item-00113"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00114"></a> **Reconstruction and equality.** For NA claim 15 and its applicable dependents, counsel must determine full-scope enablement for building a reconstructed manifest from noisy detected cut times and any § 112(f) consequence. The election among the three recorded constructions of an “equal” manifest — byte identity, equivalent chunk selections, equivalent represented timing choices — remains open and reserved to counsel; claim text retains bare “equal to.” A chunk-identity construction interacts adversely with the adaptive-streaming dependent (NA claim 10), under which a reconstruction recovers the timing-choice pattern but not rendition-exact chunk identities; dynamic URLs, tokens, and metadata remain relevant to definiteness, art, and infringement analysis.
8. <a id="ssp-aa11393us-na-us-claim-set-list-item-00115"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00116"></a> **Per-filing modes and Mode B.** For every gated claim, separately conclude PCT written description, PCT enablement, provisional written description and enablement for benefit entitlement, and effective date without treating written description and enablement as interchangeable, and assign a DW-05A mode. An independent that fails provisional written description for a folded relationship takes the 19 February 2025 PCT date and faces § 102(a)(1) intervening art, including B10's recorded posture.
9. <a id="ssp-aa11393us-na-us-claim-set-list-item-00117"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00118"></a> **Claim-boundary clarity.** Before approving the affected claims, counsel must determine the objective boundary of the “defined temporal region” plurality in NA claim 9, the scope of the respective sequence of timing choices, and the relationship in NA claim 12 between the recited temporal region and chunks spanning “the same playback interval.”

<a id="ssp-aa11393us-na-us-claim-set-header-00119"></a>
## 6. Enforcement and portfolio cautions

1. <a id="ssp-aa11393us-na-us-claim-set-orderedlist-00120"></a> <a id="ssp-aa11393us-na-us-claim-set-list-item-00121"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00122"></a> NA claim 15 is detector-focused and does not require the accused monitoring actor to perform production or delivery. Its stored ledger must nevertheless contain delivered-manifest mappings over the per-cut ordered-transition ensemble representing recipient-associated timing-choice combinations. Its art position faces A4, A6, A13, B6, B8, B9, A20, and A21 combination pressure.
2. <a id="ssp-aa11393us-na-us-claim-set-list-item-00123"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00124"></a> The three independent claims are each performable by one operator; a vertically integrated operator infringes each of NA claims 1, 9, and 15 by performing each side, and a split supply chain is reachable actor by actor. The former end-to-end method family (former NA claims 22–30) is dropped from this set and reserved under the continuation-preservation controls; the AF branch carries the integrated production-to-attribution chain.
3. <a id="ssp-aa11393us-na-us-claim-set-list-item-00125"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00126"></a> The reference/mate relationship, chunk provenance, manifest-to-chunk mappings, recipient ledger, matched delivered manifest, per-cut moved boundaries, plural detected cut times, reconstructed manifest, equality comparison, and contributor analysis may require evidence controlled by different infrastructure operators; DW-08C governs that evidence, and observed facts, technical inference, and attorney argument must remain separately identified.
4. <a id="ssp-aa11393us-na-us-claim-set-list-item-00127"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00128"></a> Do not describe any independent as categorically eligible, enabled, supported, novel, nonobvious, or infringed without the corresponding counsel analysis.
5. <a id="ssp-aa11393us-na-us-claim-set-list-item-00129"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00130"></a> Convert the claims to the required § 371 national-stage amendment format and recheck status identifiers, antecedent basis, count (20 total / 3 independent / no multiple-dependent), unity, and restriction exposure.
