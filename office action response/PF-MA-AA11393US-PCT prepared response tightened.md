# Written Reply under PCT Rule 43bis.1 (Tight point-by-point)

## To: International Searching Authority (European Patent Office)
## Re: PCT Application No. PCT/IB2025/051755
## Title: AI-DRIVEN SYSTEM AND METHOD FOR CONTENT DIFFERENTIATION AND PIRACY TRACEABILITY IN STREAMING MEDIA

---

This submission is made in response to the Written Opinion of the International Searching Authority dated **30 April 2025** (Form PCT/ISA/237). The Applicant provides the following **point-by-point comments** on Items V, VII, and VIII, and proposes the **amended claim set** in Annex A. This reply is without prejudice to amendments under PCT Article 19 and/or Chapter II practice.

## 0. Overview of the Written Opinion

The Written Opinion indicates:

- **Novelty**: Yes for claims 1–18.
- **Inventive step**: No for claims 1–18 over D1 (US 2021/352381 A1) with D2 (CN 117 278 762 A) mentioned.
- **Formal defects**: D1 not cited in the background; two-part form requested; missing reference signs (Item VII).
- **Clarity**: objections for claims 1 and 16–17 (and related AI/ML wording), in particular regarding “altering time codes at camera cuts” and “distinguishable” (Item VIII).

The Applicant addresses these points below and proposes amendments aimed at (i) aligning claim 1 with the technical contribution actually described for system (100) and (ii) resolving the clarity issues identified.

## 1. Item V — Inventive step (PCT Article 33(3))

### 1.1 What D1 teaches

D1 (US 2021/352381 A1) concerns reducing piracy primarily by:

- generating multiple copies of a media content item and applying a variety of **transformations** to resist collusion attacks (e.g., cropping/padding, shifting, color/brightness, time delay, frame rate), while maintaining a viewing-performance criterion for legitimate users; and
- combining the transformed copies with **watermarks** so that recipients can be traced by embedded identifiers.

D1’s “scene change” alignment is used to provide smooth transitions for transformations (e.g., fade-in/fade-out aligned with scene changes), not to implement camera switching between concurrently captured camera feeds.

D2 (CN 117278762 A) concerns traceability through watermark/metadata insertion across capture/encode/transmit/decode stages.

### 1.2 The issue with claim 1 as searched, and the Applicant’s amendment approach

As observed by the ISA, the current independent claim 1 is broad and allows a mapping onto D1’s headend-based generation of variant copies. To focus claim 1 on the actual technical contribution of the application, the Applicant proposes to amend claim 1 by incorporating features already present in the description and in dependent claims 10–15 as filed (multi-camera production pipeline; list (103) of edit instructions with time codes; manifest-file based distribution; ledger mapping; reconstruction of a manifest file from a pirate webcast based on detected camera-cut timings/time codes).

### 1.3 Distinguishing features of amended claim 1 over D1

Amended claim 1 (Annex A) requires, in combination:

1. **Multi-camera production pipeline and camera cuts**: an audio-video production pipeline (102) that performs real-time switching between camera views (camera cuts) and records camera-cut timings and transitions by inserting time codes into a list (103) of instructions describing edits.

2. **Mate creation by editing-domain time-code variation**: a mate creation component (110) that automatically applies variations to the time codes of camera cuts recorded in the list (103) to generate mates (111) of a reference audio-video content (1).

3. **Manifest-based distribution fingerprint**: transcoding components (120) segmenting an ensemble (112) into chunks (113) and generating different manifest files (121) pointing to unique interleaved combinations of chunks (113).

4. **Ledger mapping and forensic identification from a pirate stream**: a ledger (122) recording associations between manifest files (121) and end users (2), and a detection component (130) running a camera cuts detection algorithm (131) that analyzes camera-cut timings in a suspected unauthorized distribution, derives time codes, builds reconstructed manifest files (121′), and a retrieval component (140) that identifies the end user (2) by matching the reconstructed manifest file (121′) to the ledger (122).

D1 does not disclose a multi-camera production pipeline recording camera-cut time codes in an edit-instruction list and generating per-recipient fingerprints based on **camera-cut time-code variations**; nor does it disclose reconstructing a manifest file from a pirate webcast by detecting camera-cut timings and matching that reconstructed manifest file to a ledger of end-user associations.

### 1.4 Technical effect and synergy

The above features cooperate to yield a technical effect that is different from D1/D2:

- the “fingerprint” used for traceability is implemented in the **editing/production domain** (time-coded camera-cut schedule / resulting manifest-file selection of chunks) rather than in embedded watermark identifiers; and
- the system enables identification of the leaking end-user account from a single pirate webcast by reconstructing a manifest file from detected camera-cut timings and searching the ledger for the associated recipient.

This is not an aggregation of unrelated features. The multi-camera pipeline creates the camera-cut events; the mate creation component varies the time codes of those events; the manifest files encode the resulting chunk-selection sequence delivered to users; and the detection and retrieval components recover and match that sequence to identify the source.

### 1.5 Objective technical problem and “would” analysis

Starting from D1, an objective technical problem addressed by amended claim 1 can be formulated as:

> How to identify, from a suspected unauthorized distribution, the end user account that received a particular delivered version in an adaptive streaming system for multi-camera event content, using a reproducible delivery fingerprint tied to the production pipeline’s camera cuts.

D1’s solution space is to embed traceability in watermarks and to resist collusion by applying transformations. D1 contains no suggestion to use a **multi-camera production pipeline’s camera-cut schedule** recorded in an edit list as the basis for per-recipient fingerprinting, nor to reconstruct and match a manifest file based on detected camera-cut timings in a pirate webcast. D2 similarly teaches further watermark/metadata insertion across processing stages and provides no suggestion toward the claimed editing-domain camera-cut time-code variation and manifest reconstruction.

Accordingly, amended claim 1 involves an inventive step.

## 2. Item VIII — Clarity (PCT Article 6)

The Applicant addresses the ISA’s clarity points as follows, and reflects these clarifications in the amended claims of Annex A.

### 2.1 “Altering/adjusting time codes at camera cuts”

In the context of the present application, “time codes” are the time-coded entries in the list (103) of instructions describing edits (e.g., an EDL), which control **when** the production pipeline switches from one camera to another.

Amended claim 1 and dependent claim 3 clarify that the mate creation component (110) applies variations by modifying the time codes associated with camera-cut entries in the list (103), and that such variations can be implemented as frame-level offsets with compensating adjustments (e.g., as in Example 2) to preserve continuity and synchronization.

### 2.2 “Distinguishable”

The term “distinguishable” is removed from amended claim 1. Traceability is instead expressed in objective, technical terms: the end-user association is recorded for **manifest files (121)**, and identification is performed by building a **reconstructed manifest file (121′)** from detected camera-cut timings/time codes and matching it to the ledger (122).

### 2.3 “Artificial intelligence algorithm” / result-to-be-achieved

Amended claim 1 uses the concrete technical notion of a “camera cuts detection algorithm (131)” that (i) analyzes camera-cut timings in the suspected unauthorized distribution and (ii) builds reconstructed manifest files (121′) from derived time codes. Dependent claims 4–5 further specify implementations (perceptual hash and fuzzy matching) already described in the application.

### 2.4 Predictive ML wording (former claim 7)

To address the “result to be achieved” concern, the amended dependent claim 8 ties “historical data patterns / piracy attempt profiles” to concrete stored records of prior piracy incidents within the system’s own traceability workflow (e.g., reconstructed manifest files (121′) and identified end-user accounts (2)), and constrains the output to parameters defining time-code variations/mate configuration delivered to the mate creation component (110).

## 3. Item VII — Formal defects (PCT Rules 5.1(a)(ii), 6.3(b), 6.2(b))

The Applicant will address the formal matters noted by the ISA as follows:

1. **Citation of D1 in the background** (Rule 5.1(a)(ii)): the description will be amended to cite D1 and to explain the differences relative to the claimed editing-domain camera-cut time-code variation and manifest reconstruction approach.

2. **Two-part form** (Rule 6.3(b)): amended claim 1 is presented in two-part form, with the characterising part reciting the distinguishing technical features.

3. **Reference signs** (Rule 6.2(b)): reference signs are provided in parentheses in Annex A.

---

## Annex A — Proposed amended claims (clean set)

```text
1. An anti-piracy system (100) identifying unauthorized distributions of streaming audio-video content, comprising:
   - a distribution apparatus configured to deliver one or more content versions to at least one end user (2);
   - a record (122) of associations between said content versions and respective end users (2); and
   - a detection apparatus configured to analyze a suspected unauthorized distribution and to identify an end user (2) associated with a content version matching the suspected unauthorized distribution,
   characterised in that the system (100) comprises:
   - a set of cameras (101) configured to capture an event from diverse viewpoints;
   - an audio-video production pipeline (102) configured to receive, process, and manage content from the cameras (101), and to perform real-time switching between camera views, the switches being camera cuts, and to record camera-cut timings and transitions by inserting corresponding time codes into a list (103) of instructions describing edits;
   - a mate creation component (110) inside the pipeline (102), configured to automatically apply variations to the time codes of camera cuts recorded in the list (103) to generate one or more mates (111) of a reference audio-video content (1) produced by the pipeline (102), an ensemble (112) being a combination of the reference audio-video content (1) and its mates (111);
   - a set of transcoding components (120) configured to segment the ensemble (112) into chunks (113) for distribution through a Content Delivery Network, CDN, and to generate a set of different manifest files (121) tailored to end user devices and network conditions, each manifest file (121) pointing to a respective interleaved combination of chunks (113) of the ensemble (112), and
   - the record being a ledger (122) configured to record associations between the manifest files (121) and the end users (2);
   wherein the detection apparatus comprises:
   - a detection component (130) configured to run a camera cuts detection algorithm (131) that analyzes timings of camera cuts in the suspected unauthorized distribution, derives time codes, and builds one or more reconstructed manifest files (121′) from the derived time codes; and
   - a retrieval component (140) configured to search the ledger (122) for a manifest file (121) equal to a reconstructed manifest file (121′) and to identify an end user (2) associated with said manifest file (121).

2. The anti-piracy system (100) according to claim 1, wherein the list (103) of instructions describing edits is an Edit Decision List, EDL.

3. The anti-piracy system (100) according to claim 1 or 2, wherein applying said variations comprises modifying, in the list (103), an in-point time code and/or an out-point time code of at least one camera cut by an offset of an integer number of frames, and compensating by modifying at least one subsequent camera cut time code so that, from a subsequent camera cut onward, the time codes in the list (103) equal corresponding time codes of the reference audio-video content (1).

4. The anti-piracy system (100) according to any of the previous claims, wherein the camera cuts detection algorithm (131) compares the reference audio-video content (1) with the suspected unauthorized distribution using a perceptual hash method.

5. The anti-piracy system (100) according to claim 4, wherein the camera cuts detection algorithm (131) further compares the reference audio-video content (1) with the suspected unauthorized distribution using a fuzzy matching method.

6. The anti-piracy system (100) according to any of the previous claims, wherein the camera cuts detection algorithm (131) uses a probabilistic fingerprinting algorithm.

7. The anti-piracy system (100) according to any of the previous claims, wherein streamed content is distributed using unicasting.

8. The anti-piracy system (100) according to any of the previous claims, wherein the pipeline (102) further comprises an advanced analytics component (104) configured to output, to the mate creation component (110), parameters defining time-code variations of camera cuts and a configuration of mates (111), based on stored records of prior piracy incidents including reconstructed manifest files (121′) and identified end-user accounts (2).

9. The anti-piracy system (100) according to any of the previous claims, further comprising pipeline components in the pipeline (102) configured to overlay additional audio and/or video elements to the reference audio-video content (1) and its mates (111).

10. The anti-piracy system (100) according to any of the previous claims, being implemented within a computing environment comprising at least a processor, at least a memory, and at least a storage hardware, the computing environment being capable of executing instruction code.

11. The anti-piracy system (100) according to claim 10, being implemented within one or more server clusters.

12. The anti-piracy system (100) according to any of claims 1–11, wherein the transcoding components (120) further comprise a mixing component (123) configured to integrate chunks (113) of the reference audio-video content (1) with chunks (113) of content modified with mates (111), to generate the manifest files (121), and to associate end users (2) with manifest files (121) as different camera cuts are progressively provided.

13. The anti-piracy system (100) according to any of claims 1–12, further comprising a blockchain registration component (150) configured to register the association of manifest files (121) and end users (2) in a blockchain.

14. The anti-piracy system (100) according to claim 13, wherein the ledger (122) is implemented as a blockchain ledger.

15. The anti-piracy system (100) according to any of the previous claims, wherein the camera cuts detection algorithm (131) performs scene change detection on the suspected unauthorized distribution to obtain candidate camera-cut timings and derives the time codes from the candidate timings.

16. A method (200) of identifying unauthorized distribution of streaming audio-video content and identifying a source thereof, exploiting the system (100) according to any of claims 1–15, and comprising:
   - a capturing step (201) in which video of an event is captured from diverse viewpoints using the set of cameras (101);
   - a management step (210) in which the captured video is received and processed through the audio-video production pipeline (102), including commanding real-time camera cuts;
   - a camera cut recording step (220) in which camera cut timings and transitions are recorded by inserting corresponding time codes in the list (103) of instructions describing edits;
   - a programming step (230) in which the mate creation component (110) automatically applies variations to the time codes of camera cuts recorded in the list (103) to generate one or more mates (111) of the reference audio-video content (1);
   - a segmenting step (240) in which the ensemble (112) is segmented into chunks (113) for distribution through the CDN;
   - a generation step (250) in which different manifest files (121), tailored to end user devices and network conditions, are generated, each manifest file (121) pointing to a respective interleaved combination of chunks (113) of the ensemble (112);
   - a distribution step (260) in which streamed content is distributed to end users (2);
   - a ledger recording step (270) in which the distribution of manifest files (121) to end users (2) is recorded in the ledger (122);
   - a monitoring step (280) in which the detection component (130) monitors a suspected unauthorized distribution and runs the camera cuts detection algorithm (131) to analyze camera-cut timings, derive time codes, and build one or more reconstructed manifest files (121′); and
   - a searching step (290) in which the ledger (122) is searched by the retrieval component (140) to identify an end user (2) account or accounts associated with a manifest file (121) equal to a reconstructed manifest file (121′), thereby identifying a source of the suspected unauthorized distribution.

17. The method (200) according to claim 16, wherein the camera cuts detection algorithm (131) compares the reference audio-video content (1) with the suspected unauthorized distribution using a perceptual hash method and a fuzzy matching method.

18. A computer program comprising instructions which, when executed by a computer, cause the computer to carry out the method (200) according to claim 16 or 17.
```

