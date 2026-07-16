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

## 2. The distinguishing features form a single functional unit, not an aggregation

2.1 The WO identifies features **F1.1–F1.4** of claim 1 as not disclosed by D1: the pipeline receiving video captured from cameras (F1.1), the creation of the reference audio-video content by that pipeline (F1.2), the camera cuts (F1.3), and the detection apparatus identifying the matching version by detecting camera-switch timings and searching the record of associations (F1.4). The WO then reasons that these features lack "technical synergy" with the remainder of the claim and dismisses them individually (multiple cameras as well known; the reference to artificial intelligence as unspecific).

2.2 The applicant respectfully disagrees with the premise. The distinguishing features are not an aggregation of independent measures; they are the successive stages of **one mechanism**, in which the *timing of the directorial camera cuts is itself the identifying signal*:

- the multi-camera pipeline supplies the degrees of freedom — which camera is on air at which instant — and records them as time codes in the structured list of instructions (103);
- the mate creation component (110) **writes identity into that structure**, by applying per-version variations to the recorded cut time codes (Example 2 of the application: cut 2 extended by 10 frames, cut 3 shifted, re-synchronisation at cut 4);
- the record of associations (ledger 122) binds each resulting timing pattern to a recipient;
- the detection apparatus **reads the same quantity back**: it measures the camera-switch timings observable in a suspected unauthorized redistribution, identifies the version whose timing pattern matches, and resolves the recipient from the record.

2.3 Because the marking and the detection operate on the same structural quantity, the features co-operate to produce a **combined technical effect**: recipient-level traceability of a leaked stream that survives filtering, re-compression, re-encoding, cropping, resolution changes and collusion attacks — precisely the attacks that defeat pixel-domain watermarks, as discussed in the application's background — while leaving picture quality untouched, since every frame delivered is a genuine camera frame and no pixel-domain mark is embedded. The interaction of the features is therefore functional, not incidental, and the inventive-step assessment should consider them as a whole (PCT International Search and Preliminary Examination Guidelines, ch. 13; cf. EPO Guidelines G-VII, 7 on the treatment of combinations versus aggregations).

## 3. D1 operates on a different principle and does not point toward the claimed solution

3.1 D1 is directed to **collusion resistance**, not to identification. Its transformations (cropping/padding, brightness, rotation, scaling, banner location, frame rate, time delay — D1, [0042]–[0050]) are applied so that *combining* two copies yields degraded output ([0016], [0027]). Identification of a leaking user in D1 remains the task of the **watermark**: "in case a user leaks certain media content, his/her identity (ID) may be traced using embedded data" ([0002]); each stream includes "a unique watermark sequence" ([0053]). D1 expressly maintains that its transformations must not degrade "the detectability of the original watermark" ([0026], [0038]) — i.e., the transformations protect the watermark; they do not replace it as the identifier.

3.2 Consistently, D1's transformations are selected **randomly or pseudo-randomly** under a *statistical* criterion ([0035], [0080]: "the transformations are applied randomly"; the requirement is only that copies be statistically different). A randomly transformed copy cannot serve as a recipient identifier, and D1 discloses no record of which transformation was delivered to which recipient, nor any detector that measures transformations in a pirated stream to identify its recipient. The passage cited in the WO for the record of associations ([0031]: the client device "choses one of the copies, e.g., based on the ID **and/or randomly**") confirms this: where the choice is random there is nothing to record, and where it is derived from the client ID the identification route is the watermark sequence itself, not a searchable record of delivered versions.

3.3 The WO equates the claimed "camera-switch timings" with the "scene change" of D1, [0034]. The applicant respectfully submits that this passage teaches the opposite of the claimed use. In D1, [0034] and FIG. 8, scene changes are used as **camouflage sites**: transitions *between transformations* are aligned with scene changes so that the viewer does not notice the switch ("the transformations fade in and/or fade out or aligned with scene change for a smooth transition"). The scene-change structure itself originates from the single base copy (101, 105) and is therefore **identical in every copy** D1 produces; it varies between copies in no way and can identify no copy. In the claimed invention, that structure is deliberately made **different for each version** and is the very carrier of identity. D1 thus uses scene changes as an invariant to hide behind, whereas the invention uses camera-cut timing as a per-recipient variable to detect. A skilled person implementing D1 has no reason — and receives no hint — to alter the cut structure of the content: D1's stated design goals (imperceptibility; watermark preservation; statistical randomness) are all satisfied without doing so.

3.4 The remaining passages cited against the mate-creation feature do not disclose it: [0037] concerns the distribution of D1's components across devices of the media chain; [0083] concerns image-domain transformations applied segment-by-segment (e.g., slight stretch in fill mode). Neither passage discloses altering the timing of any camera cut, nor any modification of the content's edit structure.

3.5 For completeness as regards D1's time-delay transformation ([0048]–[0049], [0072]), which the WO does not rely upon: a uniform delay of an entire copy leaves the timing of every camera cut **relative to the other camera cuts** unchanged. A pirated re-stream carries no reliable absolute time reference; only the *relative* pattern of cut timings is recoverable from it. Claim 1, read in the light of the description (Example 2, Tables 1–3, where inter-cut intervals of the mate differ from those of the reference), requires precisely such a relative alteration ("altering at least one camera-cut timing **relative to the reference audio-video content**"). A globally delayed copy therefore neither anticipates nor suggests the claimed mate creation, and could not be identified by the claimed detection in any event.

3.6 Accordingly, starting from D1, the objective technical problem may be formulated as: *how to provide recipient-level traceability of leaked streaming content that remains recoverable after the signal-processing and collusion attacks that defeat embedded watermarks, without degrading the legitimate viewing experience.* Neither D1 (which answers leak-tracing with watermarks and answers collusion with random imperceptible transformations) nor D2 (see section 5) gives the skilled person any pointer toward encoding recipient identity in the timing of directorial camera cuts recorded in an edit list and recovering it by shot-boundary timing analysis. The "could-would" requirement is not met.

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
> 2. Paragraph 3.5 deliberately pre-empts the strongest argument available to national examiners from D1 (per-copy time delay) and locks in the applicant's claim construction; PRAXI to confirm they are comfortable addressing art the WO did not rely on. If not, drop 3.5 — the amended national claims (relative-timing clause) achieve the same protection.
> 3. Keep the constructive tone: these comments are public (PATENTSCOPE) and will be read by the EPO examiner handling the Rule 161 EPC response in the EP regional phase — they should read as the first half of that response.
