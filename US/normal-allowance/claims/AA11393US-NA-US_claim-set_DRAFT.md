<!-- GENERATED REVIEW PROJECTION — source aa11393us-na-us-claim-set; digest sha256/xc1/ssp-xd1:42cecad0960e5dece4dc45dc482cbeb6362a3074dd7c67110b55fe0043b40bc4; source profile authored-v1; projection profile gfm-v1/generated-v1; regenerate with `uv --no-cache --offline run --locked --no-sync python -m structured_source render aa11393us-na-us-claim-set`; edit the XML source, never this Markdown. -->
<a id="ssp-aa11393us-na-us-claim-set-root"></a>

<a id="ssp-aa11393us-na-us-claim-set-header-00001"></a>
# AA11393US — NA Claim Strategy and Candidate Claim Set (DRAFT)

<a id="ssp-aa11393us-na-us-claim-set-blockquote-00002"></a>
> <a id="ssp-aa11393us-na-us-claim-set-para-00003"></a>
> **STRATEGY NA · CLAIM-SET VERSION NA-2026-07-22-v4 · STATUS 23 JULY 2026**
>
> <a id="ssp-aa11393us-na-us-claim-set-para-00004"></a>
> **COUNSEL-REVIEW DRAFT — NOT FOR FILING AS-IS.** Use `NA claim N` outside the claim text.
>
> <a id="ssp-aa11393us-na-us-claim-set-para-00005"></a>
> Prepared for ordinary US national-stage entry under 35 U.S.C. § 371 of PCT/IB2025/051755. This document proposes an actor-focused claim architecture and a candidate fallback ladder with express support gates. US counsel must confirm wording, claim construction, § 101, § 102, § 103, § 112(a)/(b)/(f), antecedent basis, restriction, fees, benefit entitlement, and national-stage amendment format. Filing and successor controls are canonical in [`../common/`](../../common/README.md).

<a id="ssp-aa11393us-na-us-claim-set-header-00006"></a>
## 1. Operative architecture

<a id="ssp-aa11393us-na-us-claim-set-para-00007"></a>
The candidate set uses four independent claims directed to likely commercial operators:

<a id="ssp-aa11393us-na-us-claim-set-table-00008"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00009"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00013"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00017"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00021"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00025"></a>

| <a id="ssp-aa11393us-na-us-claim-set-plain-00010"></a> Independent NA claim | <a id="ssp-aa11393us-na-us-claim-set-plain-00011"></a> Primary actor / infringement target | <a id="ssp-aa11393us-na-us-claim-set-plain-00012"></a> Core limitation |
| --- | --- | --- |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00014"></a> 1 — production system | <a id="ssp-aa11393us-na-us-claim-set-plain-00015"></a> Broadcaster, production facility, mate-generation vendor | <a id="ssp-aa11393us-na-us-claim-set-plain-00016"></a> Same ordered first-camera-to-second-camera transition at noncoincident reference/mate timings, with temporally corresponding different-camera frames in the intervening interval |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00018"></a> 9 — distribution system | <a id="ssp-aa11393us-na-us-claim-set-plain-00019"></a> Streaming platform, licensee, CDN/origin operator | <a id="ssp-aa11393us-na-us-claim-set-plain-00020"></a> Manifest/chunk selections preserving one of two positions of the same ordered camera-source transition and associated with recipients |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00022"></a> 16 — detection system | <a id="ssp-aa11393us-na-us-claim-set-plain-00023"></a> Monitoring provider, platform, rights owner | <a id="ssp-aa11393us-na-us-claim-set-plain-00024"></a> Reference/mate chunk-combination manifests with a mate cut-timing difference, plural suspect cut-time detection, reconstructed-manifest building, equal-delivered-manifest lookup, and recipient identification |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00026"></a> 22 — end-to-end method | <a id="ssp-aa11393us-na-us-claim-set-plain-00027"></a> Vertically integrated operator | <a id="ssp-aa11393us-na-us-claim-set-plain-00028"></a> Production variation, manifest delivery/association, plural cut-time reconstruction, and equal-manifest recipient lookup |

<a id="ssp-aa11393us-na-us-claim-set-para-00029"></a>
The set contains **30 total claims / 4 independent claims / 26 singly dependent claims / no multiple-dependent claims**. It exceeds the basic 20-total/three-independent allocation by ten total claims and one independent claim. Counsel must verify ordinary excess-claim fees, unity, restriction exposure, and national-stage mechanics.

<a id="ssp-aa11393us-na-us-claim-set-para-00030"></a>
No operative NA claim requires suspect-side identification of physical camera sources or joint matching of an ordered physical-source pair with timing. Physical-camera identity remains in production and distribution structures, including the stored matched-manifest relationship in NA claim 19. Suspect recovery in NA claims 16, 19–20, and 22 uses the disclosed cut-time/reconstructed-manifest/equality path.

<a id="ssp-aa11393us-na-us-claim-set-header-00031"></a>
## 2. Drafting principles

1. <a id="ssp-aa11393us-na-us-claim-set-orderedlist-00032"></a> <a id="ssp-aa11393us-na-us-claim-set-list-item-00033"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00034"></a> **Production core.** “Different videos” is insufficient. NA claims 1 and 22 require local reassignment of a temporal interval from one physical camera source to another around a recorded camera cut.
2. <a id="ssp-aa11393us-na-us-claim-set-list-item-00035"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00036"></a> **D1 response.** D1 does not itself disclose alternate-camera frame selection. Counsel must nevertheless test combinations with conventional multicamera production, A20, B9, A4, A6, B6, and A13.
3. <a id="ssp-aa11393us-na-us-claim-set-list-item-00037"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00038"></a> **Direct detector object.** NA claim 16 operates on delivered manifests identifying reference/mate chunk combinations, plural detected camera-cut time codes, and reconstructed manifests. Perceptual hashing, fuzzy matching, matched-manifest physical-camera geometry, plural timing combinations, manifest sequences, and probabilistic tracing remain dependent implementations.
4. <a id="ssp-aa11393us-na-us-claim-set-list-item-00039"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00040"></a> **No mandatory watermark disclaimer.** The claims remain open to complementary watermarking.
5. <a id="ssp-aa11393us-na-us-claim-set-list-item-00041"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00042"></a> **Processor language.** Processor-and-memory wording does not eliminate § 112(f), definiteness, or algorithm-sufficiency review.
6. <a id="ssp-aa11393us-na-us-claim-set-list-item-00043"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00044"></a> **Per-filing support.** Direct component support does not decide a strengthened claim relationship as a whole. Written description and enablement require separate conclusions for the PCT and provisional.

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

receive a plurality of versions of audio-video content including a reference version and at least one mate version, wherein, within a defined temporal region:
<a id="ssp-claim-9-limitation-2"></a>

the reference version contains an ordered transition from a first camera source to a second camera source at a first camera-switch timing;
<a id="ssp-claim-9-limitation-3"></a>

the at least one mate version contains the same ordered transition from the first camera source to the second camera source at a second camera-switch timing different from the first camera-switch timing; and
<a id="ssp-claim-9-limitation-4"></a>

during an interval between the first camera-switch timing and the second camera-switch timing, the reference version and the at least one mate version contain temporally corresponding frames captured by different cameras;
<a id="ssp-claim-9-limitation-5"></a>

segment the plurality of versions into chunks;
<a id="ssp-claim-9-limitation-6"></a>

generate a plurality of manifest files pointing to respective combinations of chunks selected from the plurality of versions, each respective combination causing an assembled audio-video stream to preserve, within the defined temporal region, either the first camera-switch timing or the second camera-switch timing of the ordered transition;
<a id="ssp-claim-9-limitation-7"></a>

cause delivery, to respective recipients, of audio-video streams assembled according to respective manifest files; and
<a id="ssp-claim-9-limitation-8"></a>

store, in a record of associations, associations between the respective recipients and the manifest files delivered to the respective recipients.

<a id="ssp-claim-10"></a>
**10.** <a id="ssp-claim-10-limitation-1"></a> The content-distribution system of claim 9, wherein the chunks are distributed through a content delivery network using adaptive streaming and the manifest files are tailored to recipient devices or network conditions.

<a id="ssp-claim-11"></a>
**11.** <a id="ssp-claim-11-limitation-1"></a> The content-distribution system of claim 9, wherein a mixing process integrates chunks of the reference version with chunks of one or more mate versions and progressively assigns distinguishable manifest files to recipients as additional camera-cut variations become available.

<a id="ssp-claim-12"></a>
**12.** <a id="ssp-claim-12-limitation-1"></a> The content-distribution system of claim 9, wherein the record of associations is a ledger identifying an end user or group of end users that received each manifest file.

<a id="ssp-claim-13"></a>
**13.** The content-distribution system of claim 9, wherein, for the defined temporal region:
<a id="ssp-claim-13-limitation-1"></a>

a first manifest file of the plurality of manifest files points to a first chunk selected from the reference version;
<a id="ssp-claim-13-limitation-2"></a>

a second manifest file of the plurality of manifest files, different from the first manifest file, points to a second chunk selected from the at least one mate version;
<a id="ssp-claim-13-limitation-3"></a>

the first chunk and the second chunk each span the same playback interval and have equal playback durations;
<a id="ssp-claim-13-limitation-4"></a>

the first chunk contains frames from the first camera source before the first camera-switch timing and frames from the second camera source after the first camera-switch timing; and
<a id="ssp-claim-13-limitation-5"></a>

the second chunk contains frames from the first camera source before the second camera-switch timing and frames from the second camera source after the second camera-switch timing.

<a id="ssp-claim-14"></a>
**14.** <a id="ssp-claim-14-limitation-1"></a> The content-distribution system of claim 9, wherein delivery of the audio-video streams comprises unicasting respective streams to the respective recipients.

<a id="ssp-claim-15"></a>
**15.** <a id="ssp-claim-15-limitation-1"></a> The content-distribution system of claim 9, wherein the respective combinations encode recipient-associated sequences of choices, at a plurality of defined temporal regions, between a reference camera-switch timing and a different mate camera-switch timing, each defined temporal region containing the same ordered transition between respective first and second camera sources at the reference camera-switch timing in the reference version and at the mate camera-switch timing in the at least one mate version.

<a id="ssp-aa11393us-na-us-claim-set-header-00048"></a>
### Detection / recipient-resolution system

<a id="ssp-claim-16"></a>
**16.** A system for identifying a recipient associated with a suspected unauthorized distribution of audio-video content, the system comprising one or more processors and memory storing:
<a id="ssp-claim-16-limitation-1"></a>

a ledger comprising associations between a plurality of delivered manifest files and respective recipients, each delivered manifest file identifying a respective combination of chunks selected from an ensemble comprising reference audio-video content and one or more mates of the reference audio-video content, each mate having at least one camera-cut timing different from a corresponding camera-cut timing of the reference audio-video content; and
<a id="ssp-claim-16-limitation-2"></a>

instructions that, when executed by the one or more processors, cause the system to:
<a id="ssp-claim-16-limitation-3"></a>

receive the suspected unauthorized distribution;
<a id="ssp-claim-16-limitation-4"></a>

apply a scene-change detection algorithm to the suspected unauthorized distribution to identify a plurality of time codes of camera cuts in the suspected unauthorized distribution;
<a id="ssp-claim-16-limitation-5"></a>

build one or more reconstructed manifest files from the plurality of identified time codes; and
<a id="ssp-claim-16-limitation-6"></a>

search the ledger to identify a recipient associated with a delivered manifest file that is equal to one of the one or more reconstructed manifest files.

<a id="ssp-claim-17"></a>
**17.** <a id="ssp-claim-17-limitation-1"></a> The system of claim 16, wherein identifying the plurality of time codes comprises comparing frames of the suspected unauthorized distribution with frames of one or both of reference audio-video content and one or more mates of the reference audio-video content using perceptual hashes of the frames.

<a id="ssp-claim-18"></a>
**18.** <a id="ssp-claim-18-limitation-1"></a> The system of claim 17, wherein the comparing comprises fuzzy matching in which perceptual hashes of groups of frames are compared using sliding windows.

<a id="ssp-claim-19"></a>
**19.** The system of claim 16, wherein the delivered manifest file that is equal to one of the one or more reconstructed manifest files identifies at least one chunk selected from a mate of the one or more mates, and wherein:
<a id="ssp-claim-19-limitation-1"></a>

the reference audio-video content contains, within a temporal region, an ordered transition from a first physical camera source to a second physical camera source at a first camera-switch timing;
<a id="ssp-claim-19-limitation-2"></a>

the mate contains, within the temporal region, the same ordered transition from the first physical camera source to the second physical camera source at a second camera-switch timing different from the first camera-switch timing;
<a id="ssp-claim-19-limitation-3"></a>

the at least one chunk spans the temporal region; and
<a id="ssp-claim-19-limitation-4"></a>

during an interval between the first camera-switch timing and the second camera-switch timing, the reference audio-video content and the mate contain temporally corresponding frames captured by different physical camera sources.

<a id="ssp-claim-20"></a>
**20.** <a id="ssp-claim-20-limitation-1"></a> The system of claim 19, wherein each respective combination of chunks preserves, across a plurality of camera cuts, a recipient-associated combination of camera-switch timings from the reference audio-video content and the one or more mates, and building the one or more reconstructed manifest files comprises generating a reconstructed manifest file representing a detected combination of camera-switch timings across the plurality of camera cuts.

<a id="ssp-claim-21"></a>
**21.** <a id="ssp-claim-21-limitation-1"></a> The system of claim 16, wherein the suspected unauthorized distribution comprises portions obtained from delivered versions associated with different delivered manifest files, and wherein the instructions further cause the system to apply a probabilistic fingerprinting algorithm to recipient-associated sequences of chunk selections represented by the delivered manifest files and identify one or more recipients whose delivered versions contributed respective portions to the suspected unauthorized distribution.

<a id="ssp-aa11393us-na-us-claim-set-header-00049"></a>
### End-to-end method

<a id="ssp-claim-22"></a>
**22.** A method of identifying a recipient associated with a suspected unauthorized distribution of streaming audio-video content, the method comprising:
<a id="ssp-claim-22-limitation-1"></a>

receiving video captured from a plurality of cameras and a structured list of instructions that identifies source cameras and time codes for camera cuts;
<a id="ssp-claim-22-limitation-2"></a>

producing reference audio-video content according to the structured list of instructions;
<a id="ssp-claim-22-limitation-3"></a>

generating a mate by varying a time code of at least one camera cut in the structured list such that:
<a id="ssp-claim-22-limitation-4"></a>

an ordered transition from a first camera source to a second camera source occurs at a reference camera-switch timing in the reference audio-video content and at a different mate camera-switch timing in the mate; and
<a id="ssp-claim-22-limitation-5"></a>

during an interval between the reference camera-switch timing and the mate camera-switch timing, the mate and the reference audio-video content contain temporally corresponding frames captured by different cameras;
<a id="ssp-claim-22-limitation-6"></a>

segmenting an ensemble comprising the reference audio-video content and the mate into chunks;
<a id="ssp-claim-22-limitation-7"></a>

generating a plurality of manifest files pointing to respective combinations of chunks selected from the ensemble;
<a id="ssp-claim-22-limitation-8"></a>

delivering streamed audio-video content to respective recipients according to respective manifest files of the plurality of manifest files;
<a id="ssp-claim-22-limitation-9"></a>

storing, in a ledger, associations between the respective manifest files and the recipients to which the streamed audio-video content was delivered according to the respective manifest files;
<a id="ssp-claim-22-limitation-10"></a>

receiving the suspected unauthorized distribution;
<a id="ssp-claim-22-limitation-11"></a>

applying a scene-change detection algorithm to the suspected unauthorized distribution to identify a plurality of time codes of camera cuts in the suspected unauthorized distribution;
<a id="ssp-claim-22-limitation-12"></a>

building one or more reconstructed manifest files from the plurality of identified time codes; and
<a id="ssp-claim-22-limitation-13"></a>

searching the ledger to identify a recipient associated with a delivered manifest file that is equal to one of the one or more reconstructed manifest files.

<a id="ssp-claim-23"></a>
**23.** <a id="ssp-claim-23-limitation-1"></a> The method of claim 22, wherein generating the mate comprises preserving a timing of a later camera cut from the reference audio-video content, thereby restoring synchronization between the mate and the reference audio-video content from the later camera cut onward.

<a id="ssp-claim-24"></a>
**24.** <a id="ssp-claim-24-limitation-1"></a> The method of claim 22, wherein each manifest file points to chunks that cause streamed audio-video content assembled according to the manifest file to preserve, within a temporal region adjacent to the camera cut whose time code was varied, either the reference camera-switch timing or the mate camera-switch timing of the ordered transition from the first camera source to the second camera source.

<a id="ssp-claim-25"></a>
**25.** The method of claim 24, wherein:
<a id="ssp-claim-25-limitation-1"></a>

a first manifest file points to a first chunk selected from the reference audio-video content;
<a id="ssp-claim-25-limitation-2"></a>

a second manifest file points to a second chunk selected from the mate;
<a id="ssp-claim-25-limitation-3"></a>

the first chunk and the second chunk span the same playback interval and have equal playback durations;
<a id="ssp-claim-25-limitation-4"></a>

the first chunk contains frames from the first camera source before the reference camera-switch timing and frames from the second camera source after the reference camera-switch timing; and
<a id="ssp-claim-25-limitation-5"></a>

the second chunk contains frames from the first camera source before the mate camera-switch timing and frames from the second camera source after the mate camera-switch timing.

<a id="ssp-claim-26"></a>
**26.** <a id="ssp-claim-26-limitation-1"></a> The method of claim 22, wherein identifying the plurality of time codes comprises comparing perceptual hashes of frames from the reference audio-video content and the suspected unauthorized distribution using sliding-window fuzzy matching.

<a id="ssp-claim-27"></a>
**27.** <a id="ssp-claim-27-limitation-1"></a> The method of claim 22, wherein delivering the streamed audio-video content comprises unicasting respective streamed audio-video content to the respective recipients.

<a id="ssp-claim-28"></a>
**28.** <a id="ssp-claim-28-limitation-1"></a> The method of claim 22, wherein the suspected unauthorized distribution comprises portions obtained from streamed audio-video content delivered according to different manifest files, the method further comprising applying a probabilistic fingerprinting algorithm to recipient-associated sequences of chunk selections represented by the delivered manifest files and identifying one or more recipients whose streamed audio-video content contributed respective portions to the suspected unauthorized distribution.

<a id="ssp-claim-29"></a>
**29.** <a id="ssp-claim-29-limitation-1"></a> The method of claim 22, wherein generating the mate comprises varying time codes at a plurality of camera cuts, and wherein each respective combination of chunks preserves, across the plurality of camera cuts, a recipient-associated combination of reference camera-switch timings and mate camera-switch timings.

<a id="ssp-claim-30"></a>
**30.** <a id="ssp-claim-30-limitation-1"></a> The method of claim 22, further comprising overlaying one or more additional audio or video elements not present in the video received from the plurality of cameras onto at least one of the reference audio-video content or the mate before segmenting the ensemble.

<a id="ssp-aa11393us-na-us-claim-set-header-00050"></a>
## 4. Fallback ladder and art purpose

<a id="ssp-aa11393us-na-us-claim-set-table-00051"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00052"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00056"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00060"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00064"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00068"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00072"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00076"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00080"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00084"></a>
<a id="ssp-aa11393us-na-us-claim-set-table-row-00088"></a>

| <a id="ssp-aa11393us-na-us-claim-set-plain-00053"></a> Fallback | <a id="ssp-aa11393us-na-us-claim-set-plain-00054"></a> NA claims | <a id="ssp-aa11393us-na-us-claim-set-plain-00055"></a> Principal purpose |
| --- | --- | --- |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00057"></a> Production-side ordered physical-camera transition at noncoincident timings | <a id="ssp-aa11393us-na-us-claim-set-plain-00058"></a> 1, 7, 9, 13, 15, 22, 24–25, 29 | <a id="ssp-aa11393us-na-us-claim-set-plain-00059"></a> Preserve the structural camera-boundary distinction over completed-copy transformations and generic stream switching |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00061"></a> Later-cut resynchronization | <a id="ssp-aa11393us-na-us-claim-set-plain-00062"></a> 2–3, 23 | <a id="ssp-aa11393us-na-us-claim-set-plain-00063"></a> Distinguish uniform delay and global retiming; subject to the Example 2 priority gate |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00065"></a> Manifest/chunk preservation of the moved transition | <a id="ssp-aa11393us-na-us-claim-set-plain-00066"></a> 9, 13, 15, 24–25, 29 | <a id="ssp-aa11393us-na-us-claim-set-plain-00067"></a> Bind delivery objects to the physical-camera boundary represented by the chunks |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00069"></a> Detector-only reconstructed-manifest recovery | <a id="ssp-aa11393us-na-us-claim-set-plain-00070"></a> 16–18 | <a id="ssp-aa11393us-na-us-claim-set-plain-00071"></a> Provide actor-focused recipient resolution using delivered reference/mate chunk-combination manifests and the directly disclosed cut-time/reconstruction/equality path |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00073"></a> Matched-manifest physical-camera geometry | <a id="ssp-aa11393us-na-us-claim-set-plain-00074"></a> 19 | <a id="ssp-aa11393us-na-us-claim-set-plain-00075"></a> Require the equal delivered manifest to select a mate chunk spanning the retained physical-camera transition at its noncoincident timing |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00077"></a> Plural recipient timing reconstruction | <a id="ssp-aa11393us-na-us-claim-set-plain-00078"></a> 20 | <a id="ssp-aa11393us-na-us-claim-set-plain-00079"></a> Require the reconstructed manifest to represent a detected recipient-associated combination across plural cuts |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00081"></a> Perceptual-hash and fuzzy comparison | <a id="ssp-aa11393us-na-us-claim-set-plain-00082"></a> 17–18, 26 | <a id="ssp-aa11393us-na-us-claim-set-plain-00083"></a> Concrete cut-time detection implementations |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00085"></a> Positive collusion attribution | <a id="ssp-aa11393us-na-us-claim-set-plain-00086"></a> 21, 28 | <a id="ssp-aa11393us-na-us-claim-set-plain-00087"></a> Identify contributing recipients from recipient-associated manifest sequences |
| <a id="ssp-aa11393us-na-us-claim-set-plain-00089"></a> End-to-end reconstructed-manifest method | <a id="ssp-aa11393us-na-us-claim-set-plain-00090"></a> 22–30 | <a id="ssp-aa11393us-na-us-claim-set-plain-00091"></a> Preserve the production-to-attribution chain in affirmative method steps |

<a id="ssp-aa11393us-na-us-claim-set-header-00092"></a>
## 5. Support and filing gates

1. <a id="ssp-aa11393us-na-us-claim-set-orderedlist-00093"></a> <a id="ssp-aa11393us-na-us-claim-set-list-item-00094"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00095"></a> **Production relationship.** Example 2 directly shows Camera 2 followed by Camera 3, extension of Camera 2, delayed commencement of Camera 3, and noncoincident transition timings. Counsel must determine the generalized same-ordered-transition and different-camera-interval formulations in NA claims 1, 7, 9, 13, 15, 22, 24–25, and 29.
2. <a id="ssp-aa11393us-na-us-claim-set-list-item-00096"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00097"></a> **Example 2 resynchronization.** NA claims 2–3 and 23 require a written determination addressing the provisional's stray `00:00:30:11` sentence and the table/corrective text showing restoration at `00:00:30:01`.
3. <a id="ssp-aa11393us-na-us-claim-set-list-item-00098"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00099"></a> **Distribution integration.** Examples 2–4 disclose camera-boundary variation, chunks, manifest combinations, and recipient association. Confirm the exact relationships in NA claims 9, 13, 15, 22, 24–25, and 29.
4. <a id="ssp-aa11393us-na-us-claim-set-list-item-00100"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00101"></a> **Detection independent — Mode A.** Provisional claim 1(e), (g)–(n), method claim 10(e), (g)–(k), PCT claims 10–15, Method 200, and PCT claims 16–17 directly disclose NA claim 16's reference/mate ensemble, delivered chunk-combination manifests, mate cut-timing difference, suspect-acquisition, plural-cut-time, reconstructed-manifest, equality, ledger-search, and recipient-identification chain. NA claim 19 retains a combined-example gate for the matched manifest's mate chunk and physical-camera transition geometry; NA claim 20 retains the plural timing-combination gate and inherits NA claim 19.
5. <a id="ssp-aa11393us-na-us-claim-set-list-item-00102"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00103"></a> **End-to-end method — Mode A.** Provisional method claim 10 and the PCT Method 200/claims 16–17 disclose the complete production, manifest delivery/recording, plural-cut-time reconstruction, equality, and recipient-identification chain recited by NA claim 22. Examples 2–4 supply the concrete physical-camera and manifest relationships within that disclosed chain.
6. <a id="ssp-aa11393us-na-us-claim-set-list-item-00104"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00105"></a> **Collusion.** Confirm NA claims 21 and 28's use of recipient-associated manifest chunk-selection sequences as the probabilistic input and their respective-portion contributor output.
7. <a id="ssp-aa11393us-na-us-claim-set-list-item-00106"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00107"></a> **Overlay sequence.** Confirm NA claim 30's overlay-before-segmentation relationship.
8. <a id="ssp-aa11393us-na-us-claim-set-list-item-00108"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00109"></a> **Per-filing modes.** The applicant support assessment assigns NA claims 16 and 22 to DW-05A Mode A. For every other gated claim, separately conclude PCT written description, PCT enablement, provisional written description and enablement for benefit entitlement, and effective date without treating written description and enablement as interchangeable.
9. <a id="ssp-aa11393us-na-us-claim-set-list-item-00110"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00111"></a> **Reconstruction and equality.** For NA claims 16 and 22 and their applicable dependents, counsel must determine full-scope enablement for building a reconstructed manifest from noisy detected cut times and any § 112(f) consequence. Counsel must select and consistently apply a supported construction of an “equal” manifest—byte identity, equivalent chunk selections, or equivalent represented timing choices—and account for dynamic URLs, tokens, and metadata in definiteness, art, and infringement analysis.
10. <a id="ssp-aa11393us-na-us-claim-set-list-item-00112"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00113"></a> **Claim-boundary clarity.** Before approving the affected claims, counsel must determine the objective boundary of the “temporal region adjacent to the camera cut” in NA claim 24, the scope of the recipient-associated sequence and combination formulations in NA claims 15 and 29, and the relationship in NA claims 13 and 24–25 between the recited temporal region and chunks spanning “the same playback interval.”

<a id="ssp-aa11393us-na-us-claim-set-header-00114"></a>
## 6. Enforcement and portfolio cautions

1. <a id="ssp-aa11393us-na-us-claim-set-orderedlist-00115"></a> <a id="ssp-aa11393us-na-us-claim-set-list-item-00116"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00117"></a> NA claim 16 is detector-focused and does not require the accused monitoring actor to perform production or delivery. Its stored ledger must nevertheless contain delivered-manifest mappings to reference/mate chunk combinations with the claimed mate timing difference. Its art position faces A4, A6, A13, B6, B8, B9, A20, and A21 combination pressure.
2. <a id="ssp-aa11393us-na-us-claim-set-list-item-00118"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00119"></a> NA claim 22 may require performance by, or attribution to, one entity across production, delivery, detection, and lookup. Analyze divided infringement and proof separately from validity.
3. <a id="ssp-aa11393us-na-us-claim-set-list-item-00120"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00121"></a> The reference/mate relationship, chunk provenance, manifest-to-chunk mappings, recipient ledger, matched delivered manifest, source-camera entries and moved boundaries for NA claim 19, plural detected cut times, reconstructed manifest, equality comparison, and contributor analysis may require evidence controlled by different infrastructure operators; DW-08C governs that evidence, and observed facts, technical inference, and attorney argument must remain separately identified.
4. <a id="ssp-aa11393us-na-us-claim-set-list-item-00122"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00123"></a> Do not describe any independent as categorically eligible, enabled, supported, novel, nonobvious, or infringed without the corresponding counsel analysis.
5. <a id="ssp-aa11393us-na-us-claim-set-list-item-00124"></a> <a id="ssp-aa11393us-na-us-claim-set-plain-00125"></a> Convert the claims to the required § 371 national-stage amendment format and recheck status identifiers, antecedent basis, count, ordinary excess-claim fees, unity, and restriction exposure.

<a id="ssp-review-metadata"></a>
## Structured-source review metadata

| Field | Current value |
|---|---|
| Document ID | aa11393us-na-us-claim-set |
| Artifact family | claim-set |
| Jurisdiction | US |
| Scope | NA |
| Status | draft |
| Language | en |
| Title | AA11393US — NA Claim Strategy and Candidate Claim Set (DRAFT) |
| Origin | Authored source |
| Responsible owner | Applicant — Antonio Rossi |
| Review scope | complete-current-content |

<a id="ssp-review-dependencies"></a>
## Dependency review schedule

| Kind | Subject | Exact semantic digest |
|---|---|---|
| None | — | — |

<a id="ssp-review-provenance"></a>
## Provenance review schedule

| Fragment | Stored source | Page | Region | Uncertainty |
|---|---|---:|---|---|
| None | — | — | — | — |
