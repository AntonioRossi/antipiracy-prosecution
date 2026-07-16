# AA11393US — US National Entry: Restructured Claim Set (DRAFT)

> **DRAFT — for review by US counsel. Not for filing as-is.**
> Prepared 15 July 2026 from PCT/IB2025/051755 as filed (19.02.2025; priority US 63/557,868 of 26.02.2024) and the ISA/EP Written Opinion mailed 13.05.2025 (examiner Folea).
>
> **Use:** as the claim text of a **preliminary amendment** if entering under 35 U.S.C. § 371, or as the **claims as filed** if filing a § 111(a) bypass continuation (bypass enables Track One prioritized examination).
>
> **Structure:** 20 claims, 3 independent (system / method / CRM), all single dependencies — no multiple-dependent-claim fees, no excess-claim fees.
> **No new matter:** every limitation is traced to the PCT application as filed in the Support Map (§ 3 below).

---

## 1. Design rationale (summary for the reviewing attorney)

1. **Merged PCT claims 1 + 10 + (15, generalized) into independent claim 1.** The inventive core defensible over D1 (US 2021/0352381 A1, Synamedia) is the *cut-timing-as-fingerprint* mechanism: identity is written into the timing of directorial camera cuts recorded in a structured edit list, and read back from a pirate stream by detecting shot-boundary timings. As filed, claim 1 claimed this only at result level.
2. **"Artificial intelligence" removed from all claim language.** The WO (Items V §1.1, VIII §§4.2–4.3) gave the term zero patentable weight, correctly: the disclosed detection is scene-change detection + perceptual hashing + sliding-window fuzzy matching (Example 5). The claims now recite the disclosed algorithms by name ("camera-cuts detection algorithm", perceptual hash, fuzzy matching). AI/ML remains only in dependent claims 6 and 18 where the specification actually describes an ML component (analytics component 104).
3. **Global-delay guard.** D1 ¶[0048]–[0049] and ¶[0072] (not relied on by the ISA, but sitting in the cited document) disclose a per-copy uniform *time-delay* transformation. Claim 1 therefore requires that the timing of at least one camera cut change **relative to at least one other camera cut** — a uniform stream delay preserves all relative cut timings and cannot meet the limitation. Support: Example 2, Tables 1–3 (cut 2 extended 10 frames, cut 3 shifted, re-sync at cut 4 → inter-cut intervals change).
4. **"Distinguishable" defined.** WO Item VIII §4.2 held "distinguishable" vacuous (any single bit differs). Now defined as *distinguishable by the pattern of camera-cut timings* (support: "Each mate 111 is characterized by subtle differences in the sequence and timing of camera cuts, rendering each version uniquely distinguishable from others").
5. **§ 101.** PCT claim 18 ("Computer program…") is non-statutory in the US; replaced by Beauregard claim 19 ("non-transitory computer-readable medium"). Alice posture of the set: the claims recite a specific technical mechanism (modulating edit points recorded in an EDL-type list; segment/manifest interleaving; shot-boundary detection; reconstruction and ledger matching), i.e., a McRO/Enfish-style improvement to streaming content-protection technology, not a bare abstract idea of "identifying copies". Independent claims are kept mechanism-level, not result-level, for this reason.
6. **§ 112(f) anchors.** "…apparatus/component" are nonce-ish terms. Claim 1 anchors the distribution apparatus to "one or more servers" and the detection apparatus to "at least one processor and a memory" (support: computing-environment and server-cluster passages, PCT claims 8–9, which are otherwise dropped). The mate creation component is anchored "in the audio-video production pipeline" with the Example 1 algorithm as corresponding structure. **Reviewer to confirm** whether to recast fully as "one or more processors configured to…" style.
7. **"One or more cameras" → "a plurality of cameras."** Camera *cuts* logically require ≥ 2 cameras; the original wording was internally inconsistent and gratuitously invited the single-source reading that helped the ISA map D1's single storage 101. Deliberate, harmless narrowing.
8. **Fee structure:** 20 claims / 3 independent — within basic filing fees. All "according to any of the previous claims" multiple dependencies flattened to single dependencies (chains chosen to preserve the most valuable fallback positions).

---

## 2. Claim set

### Independent system claim

**1.** A system for identifying a source of an unauthorized distribution of streaming audio-video content, the system comprising:

an audio-video production pipeline configured to receive video captured, live or pre-recorded, from a plurality of cameras and to produce a reference audio-video content, wherein switches between cameras of the plurality of cameras are camera cuts, and wherein the audio-video production pipeline is configured to record camera-cut timings by inserting corresponding time codes into a structured list of instructions describing edits;

a mate creation component in the audio-video production pipeline, the mate creation component configured to generate at least one mate of the reference audio-video content by automatically applying a variation to the time code of at least one camera cut recorded in the structured list of instructions, such that a timing of the at least one camera cut relative to at least one other camera cut differs between the at least one mate and the reference audio-video content, each mate being a version of the same underlying audio-video content, the reference audio-video content and the at least one mate together forming a plurality of distinguishable versions, each of the distinguishable versions being distinguishable by a pattern of its camera-cut timings;

a distribution apparatus comprising one or more servers, the distribution apparatus configured to deliver respective ones of the distinguishable versions to respective recipients and to make a record of associations between the distinguishable versions and the respective recipients; and

a detection apparatus comprising at least one processor and a memory, the detection apparatus configured to:

&nbsp;&nbsp;&nbsp;&nbsp;receive a suspected unauthorized distribution of audio-video content and detect camera-switch timings therein by applying a camera-cuts detection algorithm;

&nbsp;&nbsp;&nbsp;&nbsp;identify which of the distinguishable versions matches the suspected unauthorized distribution by comparing the detected camera-switch timings with the patterns of camera-cut timings of the distinguishable versions; and

&nbsp;&nbsp;&nbsp;&nbsp;search the record of associations for a recipient associated with the identified distinguishable version, thereby identifying a source of the suspected unauthorized distribution.

### System dependent claims

**2.** The system of claim 1, wherein the camera-cuts detection algorithm compares the reference audio-video content with the suspected unauthorized distribution using a perceptual hash method.

**3.** The system of claim 2, wherein the camera-cuts detection algorithm further compares the reference audio-video content with the suspected unauthorized distribution using a fuzzy matching method in which perceptual hashes of groups of frames are compared using sliding windows.

**4.** The system of claim 1, further comprising a set of pipeline components in the audio-video production pipeline configured to overlay one or more additional audio or video elements onto the reference audio-video content and the at least one mate, the one or more additional audio or video elements being nonexistent in the reference audio-video content as captured.

**5.** The system of claim 1, wherein the detection apparatus is further configured to apply a probabilistic fingerprinting algorithm in identifying the source of the suspected unauthorized distribution.

**6.** The system of claim 1, further comprising an analytics component comprising a machine learning algorithm configured to determine, based on historical data patterns and piracy attempt profiles, time-code variations and mate configurations, and to send the determined time-code variations and mate configurations to the mate creation component.

**7.** The system of claim 1, wherein the distribution apparatus comprises a set of transcoding components configured to:

segment the distinguishable versions into chunks for distribution to end users through a content delivery network (CDN) enabling adaptive streaming; and

generate a set of different manifest files tailored to end-user devices and network conditions, the manifest files pointing to unique interleaved combinations of the chunks.

**8.** The system of claim 7, wherein the transcoding components further comprise a mixing component configured to integrate chunks of the reference audio-video content with chunks of the at least one mate, to generate the manifest files, and to associate end users with the manifest files as different camera cuts are progressively provided.

**9.** The system of claim 7, wherein the record of associations is a ledger containing records of the set of different manifest files and of the end users receiving each manifest file, the ledger identifying which end user or group of end users received a given manifest file.

**10.** The system of claim 9, further comprising a blockchain registration component configured to read the manifest files and the associated end users from the ledger and to register associations of the manifest files and the end users in a blockchain.

**11.** The system of claim 9, wherein the detection apparatus comprises:

a detection component configured to run the camera-cuts detection algorithm, the camera-cuts detection algorithm analyzing timings of camera cuts in the suspected unauthorized distribution, devising time codes therefrom, and building one or more reconstructed manifest files from the devised time codes; and

a retrieval component configured to search the ledger for one or more manifest files equal to the one or more reconstructed manifest files and to identify thereby an end-user account, or a set of end-user accounts, used for accessing the audio-video content.

### Independent method claim

**12.** A method of identifying a source of an unauthorized distribution of streaming audio-video content, the method comprising:

capturing video of an event from diverse viewpoints using a plurality of cameras;

processing the captured video through an audio-video production pipeline to produce a reference audio-video content, including switching between cameras of the plurality of cameras in real time, switches between the cameras being camera cuts;

recording camera-cut timings by inserting corresponding time codes into a structured list of instructions describing edits;

generating at least one mate of the reference audio-video content by automatically applying a variation to the time code of at least one camera cut recorded in the structured list of instructions, such that a timing of the at least one camera cut relative to at least one other camera cut differs between the at least one mate and the reference audio-video content, the reference audio-video content and the at least one mate together forming a plurality of distinguishable versions, each of the distinguishable versions being distinguishable by a pattern of its camera-cut timings;

distributing respective ones of the distinguishable versions to respective recipients;

recording, in a record of associations, which of the distinguishable versions was distributed to which recipient;

monitoring for a suspected unauthorized webcast of the event and detecting camera-switch timings in the suspected unauthorized webcast by applying a camera-cuts detection algorithm;

identifying which of the distinguishable versions matches the suspected unauthorized webcast by comparing the detected camera-switch timings with the patterns of camera-cut timings of the distinguishable versions; and

searching the record of associations for a recipient associated with the identified distinguishable version, thereby identifying a source of the suspected unauthorized webcast.

### Method dependent claims

**13.** The method of claim 12, wherein generating the at least one mate comprises applying a single time-code variation at each director-commanded camera cut.

**14.** The method of claim 12, further comprising:

segmenting the distinguishable versions into chunks;

generating a set of different manifest files tailored to end-user devices and network conditions, the manifest files pointing to unique interleaved combinations of the chunks;

distributing the chunks to end users through a content delivery network (CDN) enabling adaptive streaming; and

recording, in a ledger constituting the record of associations, which end user or group of end users received each manifest file.

**15.** The method of claim 14, wherein identifying which of the distinguishable versions matches the suspected unauthorized webcast comprises:

devising time codes from the detected camera-switch timings;

building one or more reconstructed manifest files from the devised time codes; and

searching the ledger for an end-user account associated with a manifest file equal to the one or more reconstructed manifest files.

**16.** The method of claim 12, wherein detecting the camera-switch timings comprises comparing the reference audio-video content with the suspected unauthorized webcast using a perceptual hash method and a fuzzy matching method.

**17.** The method of claim 12, wherein distributing comprises delivering the distinguishable versions by unicasting.

**18.** The method of claim 12, further comprising adjusting, by a machine learning algorithm and based on historical data patterns and piracy attempt profiles, time-code variations applied in generating one or more further mates.

### Independent computer-readable-medium claim

**19.** A non-transitory computer-readable medium storing instructions that, when executed by one or more processors of a content production and distribution system, cause the content production and distribution system to perform operations comprising:

receiving video captured, live or pre-recorded, from a plurality of cameras and producing therefrom a reference audio-video content, switches between cameras of the plurality of cameras being camera cuts;

recording camera-cut timings by inserting corresponding time codes into a structured list of instructions describing edits;

generating at least one mate of the reference audio-video content by automatically applying a variation to the time code of at least one camera cut recorded in the structured list of instructions, such that a timing of the at least one camera cut relative to at least one other camera cut differs between the at least one mate and the reference audio-video content, the reference audio-video content and the at least one mate together forming a plurality of distinguishable versions, each of the distinguishable versions being distinguishable by a pattern of its camera-cut timings;

causing delivery of respective ones of the distinguishable versions to respective recipients;

recording, in a record of associations, which of the distinguishable versions was delivered to which recipient;

detecting camera-switch timings in a suspected unauthorized distribution of audio-video content by applying a camera-cuts detection algorithm;

identifying which of the distinguishable versions matches the suspected unauthorized distribution by comparing the detected camera-switch timings with the patterns of camera-cut timings of the distinguishable versions; and

searching the record of associations for a recipient associated with the identified distinguishable version, thereby identifying a source of the suspected unauthorized distribution.

**20.** The non-transitory computer-readable medium of claim 19, wherein the operations further comprise:

segmenting the distinguishable versions into chunks;

generating a set of different manifest files pointing to unique interleaved combinations of the chunks;

recording, in a ledger constituting the record of associations, which end user or group of end users received each manifest file;

and wherein identifying which of the distinguishable versions matches the suspected unauthorized distribution comprises building one or more reconstructed manifest files from the detected camera-switch timings and searching the ledger for an end-user account associated with a manifest file equal to the one or more reconstructed manifest files.

---

## 3. Support map (35 U.S.C. § 112(a) — all support in the PCT application as filed)

| US claim | Source in PCT/IB2025/051755 as filed |
|---|---|
| 1 — pipeline / cameras / camera cuts / time codes in structured list | Claims 1, 10 as filed; Detailed description, system 100 bullet list ("pipeline 102 records all camera cut timings and transitions by inserting corresponding time codes in a list 103 of instructions describing edits"); "diverse viewpoints" (set of cameras 101) |
| 1 — mate creation, **relative-timing clause** | Claim 1 as filed; mate creation component 110 passages; **Example 2, Tables 1–3** (cut 2 extended 10 frames; cut 3 in-point delayed; re-sync at cut 4 → inter-cut intervals differ from reference) |
| 1 — "distinguishable by a pattern of its camera-cut timings" | "Each mate 111 is characterized by subtle differences in the sequence and timing of camera cuts, rendering each version uniquely distinguishable from others"; Summary: "identifying illicit copies by comparing detectable edit patterns" |
| 1 — servers / processor / memory anchors | Claims 8–9 as filed; "computing environment that encompasses at least a processor, at least a memory, at least a storage hardware"; "deployed across one or more server clusters" |
| 1 — record of associations; ledger generalization | Claim 1 as filed ("a record of associations, made by said distribution apparatus"); ledger 122 passages |
| 1 — detection by camera-cuts detection algorithm; comparison to versions | Claim 1 as filed (detection of camera-switch timings); camera cuts detection algorithm 131; Summary ("comparing detectable edit patterns"); Example 5 |
| 2, 3 | Claims 2, 3 as filed; Example 5 (perceptual hash; "comparison of perceptual hashes of groups of frames using sliding windows") |
| 4 | Claim 4 as filed; "said additional elements are nonexistent in the reference audio-video content" |
| 5 | Claim 5 as filed; Tardos passages (probabilistic fingerprinting) |
| 6 | Claim 7 as filed; advanced analytics component 104 passages |
| 7 | Claim 11 as filed; transcoding components 120 / manifest files 121 passages |
| 8 | Claim 12 as filed; mixing component 123 passages; Example 4 |
| 9 | Claim 14 as filed; ledger 122 passages |
| 10 | Claim 13 as filed; blockchain registration component 150 passages |
| 11 | Claim 15 as filed; detection component 130 / retrieval component 140 / reconstructed manifest files 121′ passages |
| 12 | Claim 16 as filed, augmented with claim 10 features (real-time switching; time codes in list 103) and claim-1 merged features; method steps 201–290 |
| 13 | "In a preferred embodiment … a single time code variation is applied at each director-commanded camera cut" |
| 14, 15 | Claim 17 as filed (segmenting 240, generation 250, ledger recording 270, monitoring 280, searching 290) |
| 16 | Claims 2–3 as filed; monitoring step 280 embodiments (perceptual hash; fuzzy matching) |
| 17 | Claim 6 as filed; distribution step 260 unicasting embodiment |
| 18 | Claim 7 as filed; programming step 230 embodiment (ML dynamically adjusts content variations) |
| 19, 20 | Claim 18 as filed (computer program executing method steps except capturing), recast as non-transitory CRM; claim 17 as filed for claim 20 operations |

### Disposition of PCT claims

| PCT claim | Disposition |
|---|---|
| 1 | → US 1 (merged with 10, generalized 15; "AI" removed; relative-timing clause added) |
| 2, 3 | → US 2, 3 (chained; sliding-window detail added from Example 5) |
| 4 | → US 4 |
| 5 | → US 5 |
| 6 | → US 17 (method side only) |
| 7 | → US 6 and US 18 (recast as concrete data flow) |
| 8, 9 | Folded into US 1 as structural anchors (processor/memory; servers) — not separate claims |
| 10 | Merged into US 1 and US 12 |
| 11 | → US 7 |
| 12 | → US 8 |
| 13 | → US 10 |
| 14 | → US 9 |
| 15 | → US 11 (and generalized into US 1 detection limb) |
| 16 | → US 12 (merged with 1+10 features) |
| 17 | → US 14 + US 15 |
| 18 | → US 19 (+ US 20) as non-transitory CRM (§ 101 fix) |

---

## 4. Open points for the US associate

1. **§ 112(f) review** — "mate creation component", "detection apparatus", "distribution apparatus", "analytics component": confirm the structural anchors suffice or recast as "one or more processors configured to…". Corresponding structure/algorithms if § 112(f) is invoked: Example 1 (mate creation), Example 5 + detection component 130/retrieval 140 (detection), transcoding 120/mixing 123 (distribution).
2. **Claims 6 / 18 (ML analytics)** are the thinnest-supported claims in the set (the EPO attacked them under clarity as result-language; US analogue is § 112(a)/(b)). They are kept as dependents because they cost nothing; be ready to cancel rather than argue if rejected.
3. **Preamble weight** — "for identifying a source of an unauthorized distribution" is intended as non-limiting field language; confirm house style.
4. **"equal to" in claims 11/15/20** is specification-verbatim (reconstructed manifest matching). Consider whether "matching" is safely supported if broader scope is wanted; recommendation: keep "equal to" (narrow fallbacks should be genuinely narrow).
5. **Do NOT import the EPO's Rule 5.1(a)(ii) fix into the US specification** (no acknowledgment of D1 in the US spec — avoids Applicant Admitted Prior Art). That amendment belongs to the EP regional phase only.
6. **371 vs. bypass decision** determines whether this text is filed as a preliminary amendment or as the original claims; Track One is available only via bypass (§ 111(a)).
