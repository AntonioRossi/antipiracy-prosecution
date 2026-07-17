# AA11393US — IDS and Disclosure Inventory (DRAFT)

> **CANONICAL SHARED RECORD · STATUS 17 JULY 2026**
>
> **COUNSEL-REVIEW SOURCE LIST — NOT A COMPLETED IDS AND NOT FOR FILING AS-IS.** This one inventory controls for both `NA` and `AF`; do not fork it by strategy.
>
> Application: proposed US phase of PCT/IB2025/051755, filed 19 February 2025, claiming benefit of US provisional 63/557,868 filed 26 February 2024. Applicant: STEALTH COMPANY SRL START UP INNOVATIVA. Inventor: Antonio Rossi.

## 1. Purpose and disclosure posture

This inventory collects references known from the application, international search, related proceedings, and a limited supplemental review. US counsel should independently determine materiality, prior-art status, correct bibliographic data, copies, translations or concise explanations, and the appropriate PTO/SB/08 or Patent Center submission format.

Submission of a reference in an IDS is not an admission that it is prior art or material. The duty of disclosure under 37 CFR 1.56 continues during prosecution, but an omission does not automatically establish inequitable conduct. The recommended practice is conservative disclosure of information counsel considers material or potentially material, without argumentative characterizations on the IDS form.

The list is intentionally broader than the ISA results. It is not a patentability or freedom-to-operate search and is not represented as exhaustive.

A further claim-informed supplemental review was performed on 16 July 2026 in view of the then-current NA candidate set (four-actor architecture; camera-cut timing patterns; manifest interleaving; camera-source-transition detection). Its source inventory also controls for the later AF alternative. It comprised citation mining of the A4 grant face and of the face of D1's US grant (US 11,540,029 B2), plus targeted keyword sweeps for the comparison-matrix search-gap areas. References added from that review are marked accordingly below. This too was a limited review and is not represented as exhaustive.

## 2. US patent documents

| ID | Publication / patent | Date | Applicant / assignee | Title | Why included | Handling status |
|---|---|---:|---|---|---|---|
| A1 | US 2021/0352381 A1 | 2021-11-11 | Synamedia Limited; Kilstein et al. | *Methods and Systems for Reducing Piracy of Media Content* | D1, ISR category X for PCT claims 1–18; completed-copy transformations, arbitrary identifiers, delay, frame-rate change, collusion resistance | Official copy in PCT office-action dossier; US copy normally not required. Granted as US 11,540,029 B2 (December 2022); grant face citations reviewed 16.07.2026 (source of B9 and C7) — counsel to decide whether the grant is listed in addition to the publication (same category as the B2 family-duplicate decision) |
| A2 | US 2007/0067242 A1 / US 7,630,497 B2 | 2007-03-22 / 2009-12-08 | International Business Machines Corporation | *System and Method for Assigning Sequence Keys to a Media Player to Enable Hybrid Traitor Tracing* | File-segment variations, multiple file versions, assignment and traitor tracing; relevant to generic version/segment claims | Supplemental candidate; counsel materiality review required |
| A3 | US 2009/0320130 A1 / US 8,122,501 B2 | 2009-12-24 / 2012-02-21 | International Business Machines Corporation | *Traitor Detection for Multilevel Assignment* | Content divided into segments with variations, version assignments, recovered pirate files, and collusion/traitor detection | Supplemental candidate; counsel materiality review required |
| A4 | US 10,834,158 B1 | 2020-11-10 | Amazon Technologies, Inc. | *Encoding Identifiers into Customized Manifest Data* | Manifest-selected content-fragment patterns encode user identifiers and permit source determination; relevant to distribution/manifest claims. **Full-text review 16.07.2026: also discloses fragment versions differing by camera perspective with correlation-based identification of the delivered perspective, server/edge redirect sequencing, and probabilistic version-pattern estimation identifying colluding users — treat as the closest single reference after D1 (see matrices; flagged to counsel per memo §7)** | Supplemental candidate; counsel materiality review required |
| A5 | US 2012/0087583 A1 / US 8,837,769 B2 | 2012-04-12 / 2014-09-16 | Futurewei Technologies, Inc. | *Video Signature Based on Image Hashing and Shot Detection* | Perceptual image hashing, shot detection, and suspected/reference video comparison; relevant to detection dependents | Supplemental candidate; counsel materiality review required |
| A6 | US 2014/0325550 A1 | 2014-10-30 | Verance Corporation; Winograd et al. | *Real-Time Anti-Piracy for Broadcast Streams* | Examiner-cited on A4's face. Recipient-specific temporal event timing, distinct and suspect-tailored manifests, unique segment concatenations, variable segment durations, pirate-stream feature extraction, stored-list comparison, and user identification; a principal non-camera concern for AF claim 1 and NA claims 9–22 | Supplemental candidate identified 16.07.2026 from the A4 face-citation review; copy stored; counsel materiality review required |
| A7 | US 2017/0118537 A1 | 2017-04-27 | Nagravision S.A.; Stransky-Heilkron et al. | *Adaptive Watermarking for Streaming Data* | Examiner-cited on A4's face. Watermarking service selects among multiple segment versions using a device identifier and requested addresses from a published manifest; relevant to manifest/recipient-association claims | Supplemental candidate identified 16.07.2026 from the A4 face-citation review; copy stored; counsel materiality review required |
| A8 | US 2018/0352307 A1 | 2018-12-06 | Comcast Cable Communications, LLC; Giladi | *Content Segment Variant Obfuscation* | Examiner-cited on A4's face. Content-segment variants encode an identifying sequence in a transmission; manifest-entry duration randomization and variant size equalization obfuscate the variant pattern; relevant to AF claims 13 and 18, NA claims 9 and 15, and segment-timing handling | Supplemental candidate identified 16.07.2026 from the A4 face-citation review; copy stored; counsel materiality review required |
| A9 | US 2023/0377085 A1 / US 12,412,229 B2 | 2023-11-23 / 2025-09-09 | Synamedia Limited; Aronshtam et al. | *Anti-Collusion System Using Multiple Watermark Images* | Forward citation of D1 (its face cites A1 and D1's grant). Client-side generation of multiple watermark-image variants (color channels, rotation angles, graphic layers) with time-varying variant binding for anti-collusion; relevant to AF claims 11–12, NA claims 21 and 28, and D1-combination analysis. The 23.11.2023 publication and 17.05.2022 filing both precede the 26.02.2024 provisional (§102(a)(1) and (a)(2)) | Grant copy stored 16.07.2026 (USPTO Patent Public Search); pre-grant publication not separately stored — publication/grant pair decision as for A2/A3/A5/B6; counsel materiality review required |
| A10 | US 2010/0100971 A1 | 2010-04-22 | Geyzel et al. (inventors as applicants; no assignee on face) | *System for Embedding Data* | Identified on the face of D1's US grant and initially set aside; **promoted 16.07.2026 after the B2 ISR (transcribed that day) rated it category X against D1's PCT claims 1–5, 7, 8, 11, 13–16, 20–22, 24–30**. Rendering-device embedding of device-identifying marks by time-varying full-frame colour modulation; network-side capture (streaming/P2P) and extraction; collusion-robustness assertion | Copy stored and transcribed 16.07.2026 (`patentimages`; face verified); counsel materiality review required |

## 3. Foreign patent documents

| ID | Document | Date | Applicant / assignee | Title / relevance | Handling status |
|---|---|---:|---|---|---|
| B1 | CN 117278762 A | 2023-12-22 | Shenzhen Arboo Technology Co., Ltd. | *Secure and Traceable Video Encoding/Decoding System*; D2, ISR category A; codec-chain node metadata and watermarks | Copy in PCT dossier; obtain reliable English abstract or translation/explanation as counsel directs |
| B2 | WO 2021/224688 A1 | 2021-11-11 | Synamedia Limited | PCT family publication of D1 | Candidate defensive family citation; verify whether needed in addition to A1. **Stored copy's ISR (pp. 47–48) transcribed 16.07.2026; its category-X citations against D1's own PCT claims — US 2005/0175224 A1 (B6 family), B9, A10, Lin 2008 (C7) — are recorded on the respective rows** |
| B3 | WO 2017/017603 A1 | 2017-02-02 | Vikramjeet S. Puri | *System to Detect Unauthorized Distribution of Media Content*; cited in the application's background | Bibliographic data completed; obtain official copy |
| B4 | WO 2010/044102 A2 | 2010-04-22 | Valuable Innovations Private Limited | *Visibly Non-Intrusive Digital Watermark Based Proficient, Unique & Robust Manual System for Forensic Detection of the Point of Piracy (POP) of a Copyrighted, Digital Video Content*; background citation | Bibliographic data completed; obtain official copy |
| B5 | CN 202455480 U | 2012-09-26 | Chengdu Doyen Information Technology Co., Ltd. | *Digital Watermark System for Verifying Digital Television Copyright*; background citation | Obtain official copy and English abstract/translation or explanation |
| B6 | CN 100583750 C | 2010-01-20 | Microsoft Corporation | *Desynchronized Fingerprinting Method and System for Digital Multimedia Data*; recipient-specific pseudorandom local widths/frame counts and robust hash reacquisition after insertion, deletion, rearrangement, advertising, and other temporal changes | CN number **verified against Espacenet** 16.07.2026 (INPADOC family 034750448; US 7,382,905 B2 / AU 2004240154 / KR 101143233 confirmed in-family); copy stored; authoritative English-family review or suitable English handling remains required. Family also contains `CN 1655500 A` (pre-grant publication) — counsel to select the member to submit. **The B2 ISR rates family member US 2005/0175224 A1 category X against D1's own PCT claims (¶¶[0007]–[0012], [0027]–[0052], [0069]); that rating warrants review but is not an ISA materiality conclusion for the present claims** |
| B7 | WO 2021/141686 A1 | 2021-07-15 | Microsoft Technology Licensing, LLC | *Method of Identifying an Abridged Version of a Video*; shots separated by cuts, automatic comparison of target and reference video, piracy use | Supplemental candidate; obtain official WIPO copy; counsel materiality review required |
| B8 | EP 2 811 416 A1 | 2014-12-10 | Vestel Elektronik Sanayi ve Ticaret A.Ş. | *An Identification Method*; identifies video using subtitle start/end timings, relative gaps, and ratios of successive gaps despite frame-rate differences, while disregarding additional portions such as advertisements; temporal identification is proposed where visual watermarks are removable | Official EPO A1 copy stored; inspect family/file history for examination reasoning and cited art; current legal status does not alter the A1 disclosure; counsel materiality review required |
| B9 | WO 2009/156973 A1 | 2009-12-30 | France Telecom SA (inventors Liu, Lian, Wang, Ren) | *Fingerprinting Method and System*; shot cuts/moving frames yield probable exchange points, a key-derived/random sequence selects practical exchange points, and different users' copies actually switch among space-desynchronized streams at different selected times; stream-of-origin codes and embedded watermarks are disclosed. No synchronized physical-camera views, EDL, or moved director cut; detection is not elaborated in this publication | Supplemental candidate identified 16.07.2026 from the D1-grant face-citation review; copy stored. **The B2 ISR rates B9 itself category X against D1's PCT claims 1–10, 13–17, 19–21, 24–30, pinpointing i.a. the exchangeable-time-points passages; that rating concerns D1's claims, not the present claims.** Sibling WO 2009/122385 A2 (fingerprint encoding by watermark elimination) reviewed and provisionally set aside as cumulative of A2/C3 concepts — counsel to confirm both decisions |

## 4. Non-patent literature and prosecution documents

| ID | Reference | Reason / status |
|---|---|---|
| C1 | International Search Report, Form PCT/ISA/210, PCT/IB2025/051755, ISA/EP, mailed 13 May 2025 | Cites A1 and B1; official copy present |
| C2 | Written Opinion of the ISA, Form PCT/ISA/237, PCT/IB2025/051755, mailed 13 May 2025 | Finds PCT claims 1–18 novel and industrially applicable but not inventive; official copy present |
| C3 | Tardos, G., “Optimal Probabilistic Fingerprint Codes,” STOC 2003, pp. 116–125 | Expressly cited in the description and relevant to probabilistic/collusion dependents; obtain complete publication copy and verify citation |
| C4 | EPO Information on Search Strategy for PCT/IB2025/051755 | Optional prosecution document; useful to show search scope if counsel elects to submit |
| C5 | Applicant's informal comments on the Written Opinion, if filed | Later-created prosecution document; counsel to decide whether a copy should accompany or be cross-referenced in the US record |
| C6 | Italian search report / written opinion for IT 102025000003210 | **Not presently in the repository.** Request from PRAXI/UIBM file and add all newly cited art when received |
| C7 | Lin, Y.-T., et al., “Collusion-Resistant Video Fingerprinting Based on Temporal Oscillation,” Proc. ICIP 2008 (citation recorded as it appears on the face of D1's US grant US 11,540,029 B2) | Temporal-domain collusion-resistant video fingerprinting, examiner-cited against D1's family; relevant to timing-pattern and collusion dependents. **The B2 ISR rates it category X against D1's PCT claims 1–17 and 19–30 — acquisition priority raised.** Obtain complete publication copy (IEEE Xplore; paywalled) and verify full bibliographic data before submission |
| C8 | ETSI TS 104 002 V1.1.1 (2023-08), “Publicly Available Specification (PAS); DASH-IF Forensic A/B Watermarking” | Standardized architecture in which at least two watermarked variants (A/B) of ABR segments are delivered and per-session variant sequences identify recipients; published August 2023, before the 26.02.2024 provisional. Official ETSI copy stored 16.07.2026; relevant §103 context for AF claims 13–18 and NA claims 9–15 |

## 5. Relevance recap for counsel—not text for the IDS form

| Art group | Features apparently known | Remaining proposed distinction to test |
|---|---|---|
| D1 / B6 | Completed-copy transformations, device-based assignment, desynchronization, arbitrary identifiers, delay/frame-rate changes, recipient-specific local frame-count variation, and robust hash reacquisition after temporal attacks | Local reassignment of a bounded interval to temporally corresponding frames from another camera by changing a recorded camera-selection boundary, followed by recovery of the ordered source transition and its position |
| A2 / A3 | Segment variants, recipient/device assignments, recovered pirate versions, collusion tracing | Variants defined specifically by multi-camera edit-boundary movement rather than encrypted/watermarked file-segment versions |
| A4 | Camera-perspective fragment alternatives, differential/ordered manifest coding, per-user delivery, temporal alignment, recovered version patterns, database comparison, and probabilistic source resolution | Same ordered camera-source transition at noncoincident positions with temporally corresponding different-camera frames in the intervening interval; the manifest and recipient record preserve that source-pair/position structure rather than a generic duration-slot sequence |
| A5 / B7 | Shot detection, hashing, and comparison of suspected/target video to reference shots | Detection and matching at the same candidate-distinguishing region using both the ordered camera-source identities and transition time, followed by recipient resolution |
| B8 | Relative timing gaps and gap ratios used as identifiers despite frame-rate differences and additional advertisement portions | Per-recipient generation and recovery of an ordered multi-camera source transition at a deliberately moved recorded boundary, not relative timing or temporal robustness alone |
| A6 | Recipient-specific temporal events, distinct/tailored manifests, variable-duration segments, detected identifier-list construction, stored-list comparison, user identification, and live response | Ordered source-camera pair plus noncoincident moved edit boundary; A6 can supply most of the non-camera distribution/detection loop |
| A7 / A8 / C8 | Per-session delivery of differing or watermarked segment variants selected via manifests or requested addresses; device/recipient association; variant-pattern obfuscation including randomized manifest-entry durations; standardized A/B watermark delivery | Manifest/chunk preservation and recovery of the claimed ordered camera-source transition and position rather than a generic A/B or variant sequence |
| A9 | Client-side multiple watermark-image variants with time-varying binding as an anti-collusion measure (published 23.11.2023) | Collusion handling grounded in camera-cut structural patterns and the probabilistic-fingerprinting dependents rather than watermark-image variants |
| B9 | Shot-cut-informed, key-dependent selection of actual switch positions that can differ between users; sequential assembly from space-desynchronized streams; stream-origin codes; embedding side only in this publication | Synchronized different-camera provenance plus movement of a recorded EDL boundary while retaining the same ordered source transition, followed by manifest/ledger association and structural recovery |

Note on the 16.07.2026 sweep: citation mining (A4 face; D1 US-grant face) and keyword searches directed to camera-selection variation, vision-mixer/EDL-based versioning, and screener-edit versioning identified **no reference disclosing per-recipient variation of camera-selection boundaries**. This is a limited-search observation, not a clearance, and does not alter the non-exhaustive posture stated in §1.

## 6. Route-specific handling

1. **§371 national stage.** Confirm the PCT/DO/EO/903 or equivalent record shows which ISR references and copies were transmitted. Properly transmitted ISR references may be considered by the examiner without a duplicative IDS, but a conservative IDS may still be appropriate for clarity and for supplemental references.
2. **§111(a) bypass.** Do not assume the national-stage automatic-consideration procedure applies. Prepare a conventional IDS satisfying 37 CFR 1.97 and 1.98 for references counsel elects to submit.
3. **Foreign-language documents.** Provide copies and English translations, abstracts, or concise explanations as required and as available. If an English translation is already in the applicant's or counsel's possession or readily available, preserve and provide it for counsel review. Do not describe an unverified machine translation as authoritative.
4. **Timing.** Prefer filing the initial IDS with the US papers. Track later EP, Italian, or other national-phase citations and submit supplemental IDSs within the applicable 37 CFR 1.97 windows.

## 7. Completion checklist

The deferred retrieval, ownership/formalities, and EP-coordination tasks are organized in `AA11393US-deferred-filing-disclosure-and-EP-work_MEMO.md`. This checklist remains the disclosure inventory's operative reminder.

- [ ] Select §371 or bypass route and apply the correct IDS treatment.
- [ ] Verify all publication numbers, kind codes, dates, titles, inventors/applicants, and family relationships against official records.
- [x] Obtain copies of B3–B7 — stored 16.07.2026 in [`../prior-art/`](../prior-art/) (see that folder's README for per-document provenance and the register-confirmation caveat). Foreign-document handling for B1/B5/B6 and the B8 EPO file-history review remain open.
- [ ] Complete foreign-language handling (English abstract, translation, or concise explanation) for B1, B5, and B6.
- [ ] Obtain a complete copy of Tardos 2003 (ACM Digital Library; paywalled — needs institutional or counsel library access).
- [ ] Request the Italian search report and add every new citation.
- [x] Verify B6's exact CN publication number against an official register — confirmed against Espacenet 16.07.2026 (CN 100583750 C, Microsoft Corp, pub. 20.01.2010, INPADOC family 034750448, matching the previously recorded US/AU/KR family members); copy stored. English handling still required.
- [ ] Decide which member to submit where the IDS names a publication/grant pair and only one is stored: A2, A3, A5, B6 (`CN 1655500 A` is the B6 pre-grant publication), and A9 (`US 2023/0377085 A1` is the A9 pre-grant publication; the grant is stored).
- [ ] Inspect the B8 family and EPO file history; record status for completeness and review examination reasoning and newly identified citations.
- [ ] Obtain and preserve official copies of A2, A3, A5, B7, and Tardos 2003 if selected for submission or continuing materiality review.
- [ ] Review A2–A5 and B7–B8 for materiality in light of the final claims.
- [x] Check whether other members of the A4 manifest-art citation family warrant review, particularly real-time anti-piracy, adaptive watermarking, and content-segment-variant references cited on its face — completed 16.07.2026: all six examiner citations on A4's face reviewed. US 2014/0325550 A1 (Verance), US 2017/0118537 A1 (Nagravision), and US 2018/0352307 A1 (Comcast) added as A6–A8. US 2014/0229976 A1 (Azuki), US 2017/0353516 A1 (DLVR), and US 2018/0176623 A1 (Arris) reviewed and set aside as manifest-customization mechanics without identification purpose, cumulative of A4 — counsel may revisit.
- [ ] Review the 16.07.2026 supplemental references A6–A10, B9, C7, C8 for materiality against the final claim set and record submit/skip decisions; decide whether D1's grant US 11,540,029 B2 is listed in addition to A1. A10 was promoted from the B2-ISR X citations after initially being set aside; the ISR's X ratings for B6-family, B9, and C7 concern D1's own PCT claims and warrant review but do not decide materiality to the present claims. **The 16.07.2026 full-text scoring was propagated into separate `NA-2026-07-17-v1` and `AF-2026-07-17-v1` matrices; re-score the selected strategy after any claim amendment and note the A4 camera-perspective finding flagged per memo §7.**
- [ ] Obtain a complete copy of C7 (Lin et al., ICIP 2008; IEEE Xplore, paywalled) and verify its bibliographic data against the published paper.
- [ ] Record counsel's decision for every candidate: submit, duplicate/family not needed, nonmaterial, or await further review.
- [ ] Preserve copies of the filed IDS, references, and Patent Center receipt.
- [ ] If potentially material information is identified with an effective prior-art date after 26 February 2024 but before 19 February 2025, or any Office questions priority, notify US counsel and reassess provisional entitlement, materiality, disclosure timing, and effective-filing-date representations before taking a substantive position.

## 8. Related-application note

The repository presently evidences one US provisional, 63/557,868, filed 26 February 2024. The `PPA2` directory contains that provisional's filing materials and a later working draft; it does not presently contain proof of a separately filed second provisional. Counsel should claim only continuity supported by official filing receipts.

## 9. Working retrieval links

These links are for review convenience only; counsel should verify bibliographic data and obtain official copies where required.

- [D1 — US 2021/0352381 A1](https://patents.google.com/patent/US20210352381A1/en)
- [US 7,630,497 B2](https://patents.google.com/patent/US7630497B2/en)
- [US 2009/0320130 A1](https://patents.google.com/patent/US20090320130A1/en)
- [US 10,834,158 B1](https://patents.google.com/patent/US10834158B1/en)
- [US 2012/0087583 A1](https://patents.google.com/patent/US20120087583A1/en)
- [WO 2021/141686 A1](https://patents.google.com/patent/WO2021141686A1/en)
- [EP 2 811 416 A1 official PDF](https://data.epo.org/publication-server/rest/v1.2/publication-dates/20141210/patents/EP2811416NWA1/document.pdf)
- [CN 202455480 U — Espacenet](https://worldwide.espacenet.com/patent/search?q=pn%3DCN202455480U) (English abstract and Patent Translate available)
- [CN 100583750 C — Espacenet](https://worldwide.espacenet.com/patent/search?q=pn%3DCN100583750C) (English abstract, Patent Translate, and INPADOC family 034750448)
- [CN 1655500 A — Espacenet](https://worldwide.espacenet.com/patent/search?q=pn%3DCN1655500A) (B6 pre-grant publication; retrieve if counsel selects this member)
- [US 2014/0325550 A1](https://patents.google.com/patent/US20140325550A1/en) (A6)
- [US 2017/0118537 A1](https://patents.google.com/patent/US20170118537A1/en) (A7)
- [US 2018/0352307 A1](https://patents.google.com/patent/US20180352307A1/en) (A8)
- [US 12,412,229 B2](https://patents.google.com/patent/US12412229B2/en) (A9; stored copy is from USPTO Patent Public Search)
- [US 2010/0100971 A1](https://patents.google.com/patent/US20100100971A1/en) (A10)
- [WO 2009/156973 A1](https://patents.google.com/patent/WO2009156973A1/en) (B9) and sibling [WO 2009/122385 A2](https://patents.google.com/patent/WO2009122385A2/en) (reviewed, set aside)
- [ETSI TS 104 002 V1.1.1 official PDF](https://www.etsi.org/deliver/etsi_ts/104000_104099/104002/01.01.01_60/ts_104002v010101p.pdf) (C8)
- C7 (Lin et al., ICIP 2008): IEEE Xplore; no open-access copy located 16.07.2026 — obtain via institutional/counsel library access
