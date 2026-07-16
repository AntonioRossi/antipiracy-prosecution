# PCT/IB2025/051755 — Informal Comments on the Written Opinion of the ISA (DRAFT)

> **DRAFT — for review and filing by the appointed agent (PRAXI Intellectual Property S.p.A. — E. Fiammenghi), via ePCT, as "informal comments" / observations to the International Bureau.**
> **Deadline: must reach the IB before expiry of 30 months from priority — 26 August 2026.**
> Purpose: these comments are made publicly available on PATENTSCOPE and communicated to the designated Offices; they place the applicant's substantive rebuttal of the Written Opinion on the international file, since no Chapter II demand was filed. Tone is deliberately technical and constructive — no procedural criticism of the ISA.

---

**To:** The International Bureau of WIPO — 34, chemin des Colombettes, 1211 Geneva 20, Switzerland (via ePCT)

**International application No.:** PCT/IB2025/051755
**Applicant:** STEALTH COMPANY SRL START UP INNOVATIVA
**Agent's file reference:** PF-MA-AA11393US-PCT
**Subject:** Informal comments of the applicant on the Written Opinion of the International Searching Authority (Form PCT/ISA/237, mailed 13 May 2025)

## 1. Introduction

1.1 The applicant respectfully submits the following informal comments on the Written Opinion of the ISA ("the WO"). These comments are submitted for the benefit of the designated and elected Offices. No amendment is made herewith; the applicant intends to present amended claims upon entry into the national/regional phases, as outlined in section 6 below.

1.2 The WO acknowledges that all claims 1–18 are **novel** (Article 33(2) PCT) and **industrially applicable** (Article 33(4) PCT) over the cited documents D1 (US 2021/0352381 A1) and D2 (CN 117 278 762 A). The sole substantive objection is lack of inventive step (Article 33(3) PCT) starting from D1. The applicant respectfully submits that this objection rests on an incomplete reading of both D1 and the present application, for the reasons below.

## 2. The nature of the invention: many different videos, not many marked copies of one video

2.1 Before addressing the reasoning of the WO in detail, the applicant respectfully invites consideration of the contrast between D1 and the invention at the architectural level, because it determines the entire inventive-step analysis that follows.

2.2 **D1 generates multiple marked copies of a single video.** Every variant in D1 is produced by "replicating and applying a first transformation to the base copy of the media content item" (D1, claim 1; likewise [0017], [0067]). The input is one finished video — the base copy (105) obtained from the storage (101) — and every output copy contains the same content: the same scenes, the same edit, the same cut structure, with imperceptibly altered presentation (cropping/padding, brightness, rotation, scaling, banner location, frame rate, delay — [0042]–[0050]) and an embedded watermark carrying the recipient's identity ([0002], [0053]). Under D1, each recipient receives *the same edit bearing a different mark*.

2.3 **The invention generates multiple different videos.** The mate creation component (110) operates at the production stage, on the structured list (103) of edit instructions produced by the multi-camera pipeline (102): it moves the actual edit points (Example 2, Tables 1–3: cut 2 extended by 10 frames, cut 3 shifted, re-synchronisation at cut 4). A mate therefore contains frames — genuine, unmodified camera frames — that the reference version does not contain (the additional frames of camera 2 shown in place of the first frames of camera 3), and each recipient receives *a differently edited video, with no embedded mark required*. Identity is carried by the editorial structure of the content itself — the relative pattern of its camera-cut timings — not by data added to the signal.

2.4 This is why the invention **decouples traceability from pixel-domain embedding**. Because the identifying information is not additive data hidden in the frames but the content's own cut structure, it cannot be stripped by the filtering, re-compression, re-encoding, cropping and AI-based watermark-removal attacks discussed in the application's background: removing it would require re-editing the video. Watermarking remains usable as a complementary layer, as the description expressly contemplates, but the traceability provided by the invention does not depend on it.

2.5 Seen in this light, the features **F1.1–F1.4** which the WO itself acknowledges to be absent from D1 — the multi-camera capture pipeline (F1.1), the creation of the reference content by that pipeline (F1.2), the camera cuts (F1.3), and the detection of camera-switch timings with resolution of the recipient from the record (F1.4) — are not an aggregation of independent measures, as the WO treats them, but the successive stages of **one mechanism**, in which the timing of the directorial camera cuts is itself the identifying signal:

- the multi-camera pipeline supplies the degrees of freedom — which camera is on air at which instant — and records them as time codes in the structured list of instructions (103); the cameras are the **enabling input** of the mechanism, since the alternative frames around a cut exist only because a second camera captured them;
- the mate creation component (110) **writes identity into that structure**, by applying per-version variations to the recorded cut time codes;
- the record of associations (ledger 122) **binds** each resulting timing pattern to a recipient;
- the detection apparatus **reads the same quantity back**: it measures the camera-switch timings observable in a suspected unauthorized redistribution, identifies the version whose timing pattern matches, and resolves the recipient from the record.

Because the marking and the detection operate on the same structural quantity, the features co-operate to produce a **combined technical effect**: recipient-level traceability of a leaked stream that survives the attacks that defeat pixel-domain watermarks, at unimpaired picture quality, since every frame delivered is genuine camera output. The inventive-step assessment should therefore consider the distinguishing features as a whole (PCT International Search and Preliminary Examination Guidelines, ch. 13; cf. EPO Guidelines G-VII, 7 on combinations versus aggregations), and not feature-by-feature.

## 3. D1's replicate-and-transform architecture neither discloses nor suggests the claimed mechanism

3.1 **D1 cannot produce a mate.** The only input available to D1's transformer (120) is the base copy; its outputs are transformations of that copy. Creating a mate, by contrast, requires material that is not in the reference version at all — the frames of the other camera lying beyond the moved edit point. A mate is not a transformed copy of the reference; it is a **different edit of the underlying multi-camera material**. D1's variant-generation architecture (a single finished video in, transformed copies out) is structurally incapable of the claimed mate creation, and extending D1 to perform it would not be a workshop modification: it would require abandoning D1's principle of operation — replicate-and-transform — in favour of a different one, re-editing at the production stage. A modification of the closest prior art that is contrary to its principle of operation cannot be regarded as obvious.

3.2 **D1's transformations serve degradation, not identification.** D1 is directed to collusion resistance: its transformations are applied so that *combining* two copies yields degraded output ([0016], [0027]), while identification of a leaking user remains the task of the **watermark**: "in case a user leaks certain media content, his/her identity (ID) may be traced using embedded data" ([0002]); each stream includes "a unique watermark sequence" ([0053]). D1 expressly requires that the transformations not degrade "the detectability of the original watermark" ([0026], [0038]) — the transformations protect the identifier; they are not the identifier. Consistently, they are selected **randomly or pseudo-randomly** under a merely *statistical* criterion ([0035], [0080]: "the transformations are applied randomly"). A randomly chosen transformation identifies nobody; D1 discloses no record of which transformation was delivered to which recipient, and no detector that measures transformations in a pirated stream. The passage cited in the WO for the record of associations ([0031]: the client device "choses one of the copies, e.g., based on the ID **and/or randomly**") confirms this: where the choice is random there is nothing to record, and where it is derived from the client ID the identification route is the watermark sequence itself, not a searchable record of delivered versions.

3.3 **The scene-change passage teaches the opposite role.** The WO equates the claimed "camera-switch timings" with the "scene change" of D1, [0034]. In D1, [0034] and FIG. 8, scene changes are used as **camouflage sites**: transitions *between transformations* are aligned with scene changes so that the viewer does not notice the switch ("the transformations fade in and/or fade out or aligned with scene change for a smooth transition"). The scene-change structure itself originates from the single base copy and is therefore **identical in every copy** D1 produces — indeed, content identity across copies is a stated premise of D1's design: "the assumption of any collusion attack is that multiple copies of the media content are aligned and the only difference is the watermark" ([0027]). The invention deliberately breaks that premise at the editorial level and makes the cut structure the per-recipient variable. D1 uses scene changes as an invariant to hide behind; the invention uses camera-cut timing as a variable to detect. A skilled person implementing D1 has no reason — and receives no hint — to alter the cut structure of the content: all of D1's stated design goals (imperceptibility; watermark preservation; statistical difference) are satisfied without doing so.

3.4 The remaining passages cited against the mate-creation feature do not disclose it: [0037] concerns the distribution of D1's components across devices of the media chain; [0083] concerns image-domain transformations applied segment-by-segment (e.g., slight stretch in fill mode). Neither passage discloses altering the timing of any camera cut, nor any modification of the content's edit structure.

3.5 For completeness as regards D1's time-delay transformation ([0048]–[0049]; [0072]: "the time delay may vary for different copies") and D1's general aim of causing misalignment between copies ([0027]) — passages on which the WO does not rely — the applicant submits that they neither anticipate nor suggest the claimed mate creation, for three independent reasons:

&nbsp;&nbsp;&nbsp;&nbsp;(a) a uniform delay of an entire copy leaves the timing of every camera cut **relative to the other camera cuts** unchanged. A pirated re-stream carries no reliable absolute time reference; only the *relative* pattern of cut timings is recoverable from it. Claim 1, read in the light of the description (Example 2, Tables 1–3, where the inter-cut intervals of the mate differ from those of the reference), requires precisely such a relative alteration ("altering at least one camera-cut timing **relative to the reference audio-video content**"). A globally delayed copy could not even be identified by the claimed detection;

&nbsp;&nbsp;&nbsp;&nbsp;(b) all of D1's misalignment tools, the time delay included, are replicate-and-transform operations on the base copy. None of them can supply the alternative-camera frames needed to move an edit point (§ 3.1 above). Cut-timing alteration is not a further item on D1's menu of transformations; it belongs to a different architecture;

&nbsp;&nbsp;&nbsp;&nbsp;(c) D1's misalignments are deliberately random and serve degradation upon collusion; D1 builds no record and no detection upon them. Using a timing alteration as a recipient identifier presupposes exactly what D1 delegates to the watermark.

3.6 Accordingly, starting from D1, the objective technical problem may be formulated as: *how to provide recipient-level traceability of leaked streaming content that remains recoverable after the signal-processing and collusion attacks that defeat embedded watermarks, without degrading the legitimate viewing experience.* Neither D1 — which answers leak-tracing with watermarks and answers collusion with random imperceptible transformations of a single edit — nor D2 (see section 5) gives the skilled person any pointer toward producing *differently edited videos* whose recipient identity is encoded in the timing of directorial camera cuts recorded in an edit list and recovered by shot-boundary timing analysis, without reliance on any embedded data. The "could-would" requirement is not met.

## 4. Observations under Item VIII (clarity) — applicant's position

4.1 **Re item 4.1** (how the time codes are altered; scene integrity; visual impact): the alteration is not a modification of metadata values; the actual edit point moves. As shown in Example 2 (Tables 1–3), extending cut 2 by 10 frames means the mate contains 10 additional genuine frames from camera 2 in place of the first 10 frames of camera 3; re-synchronisation occurs at cut 4. Scene integrity is inherent, because all cameras capture the same live event and every displayed frame is genuine camera output; a shot boundary displaced by a fraction of a second is editorially imperceptible to the viewer, while remaining measurable by the detection component. The applicant will make this explicit in the claims upon national/regional entry.

4.2 **Re items 4.2–4.3** (the terms "distinguishable" and "artificial intelligence algorithm"): the applicant intends, upon national/regional entry, to (i) define distinguishability by the pattern of camera-cut timings, and (ii) replace the general reference to an artificial intelligence algorithm with the concretely disclosed detection chain — the camera-cuts detection algorithm (131) employing scene-change detection to derive time codes, perceptual hashing, and sliding-window fuzzy matching (Example 5), with reconstruction of the corresponding manifest (121′) and search of the ledger (122) as per claims 10 and 15 as filed, which the applicant intends to incorporate into the independent claims.

4.3 **Re item 4.4** (claim 7): noted; the applicant will address this claim by amendment or cancellation in the national/regional phases.

## 5. Document D2

5.1 The applicant concurs with the categorisation of D2 (CN 117 278 762 A) as "A". D2 concerns provenance tracing along a codec chain by insertion of node metadata and watermarks at capture, encoding, decoding and display; it discloses no per-recipient differentiation of content and no modification of edit structure, and does not affect the analysis above.

## 6. Conclusion

6.1 For the reasons above, the applicant respectfully submits that the subject-matter of claims 1–18 — in particular when the independent claims are read together with claims 10 and 15 as filed, as the applicant intends to present them upon national/regional entry — involves an inventive step over D1 and D2 within the meaning of Article 33(3) PCT.

6.2 These comments are submitted on an informal basis under the procedure referred to in Form PCT/ISA/220, for transmission to and consideration by the designated Offices.

Respectfully submitted,

*(signature block — PRAXI Intellectual Property S.p.A., agent of record)*
*(place, date)*

---

> **Filing notes (internal — remove before filing):**
> 1. Only the appointed agent (PRAXI / E. Fiammenghi) can file via ePCT for this application. Send this draft to PRAXI with instruction to review, adapt house style, and file **well before 26.08.2026**.
> 2. Paragraph 3.5 deliberately pre-empts the strongest argument available to national examiners from D1 — the per-copy time delay and the "cut-timing alteration is just another misalignment tool per [0027]" reading — with a three-limb rebuttal (relative-timing construction; replicate-and-transform architecture; random-therefore-not-an-identifier), and locks in the applicant's claim construction. PRAXI to confirm they are comfortable addressing art the WO did not rely on. If not, drop 3.5 — the amended national claims (relative-timing clause) achieve the same protection.
> 3. Keep the constructive tone: these comments are public (PATENTSCOPE) and will be read by the EPO examiner handling the Rule 161 EPC response in the EP regional phase — they should read as the first half of that response.
