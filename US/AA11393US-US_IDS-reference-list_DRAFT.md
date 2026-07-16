# AA11393US — IDS and Disclosure Inventory (DRAFT)

> **COUNSEL-REVIEW SOURCE LIST — NOT A COMPLETED IDS AND NOT FOR FILING AS-IS.**
>
> Application: proposed US phase of PCT/IB2025/051755, filed 19 February 2025, claiming benefit of US provisional 63/557,868 filed 26 February 2024. Applicant: STEALTH COMPANY SRL START UP INNOVATIVA. Inventor: Antonio Rossi.

## 1. Purpose and disclosure posture

This inventory collects references known from the application, international search, related proceedings, and a limited supplemental review. US counsel should independently determine materiality, prior-art status, correct bibliographic data, copies, translations or concise explanations, and the appropriate PTO/SB/08 or Patent Center submission format.

Submission of a reference in an IDS is not an admission that it is prior art or material. The duty of disclosure under 37 CFR 1.56 continues during prosecution, but an omission does not automatically establish inequitable conduct. The recommended practice is conservative disclosure of information counsel considers material or potentially material, without argumentative characterizations on the IDS form.

The list is intentionally broader than the ISA results. It is not a patentability or freedom-to-operate search and is not represented as exhaustive.

## 2. US patent documents

| ID | Publication / patent | Date | Applicant / assignee | Title | Why included | Handling status |
|---|---|---:|---|---|---|---|
| A1 | US 2021/0352381 A1 | 2021-11-11 | Synamedia Limited; Kilstein et al. | *Methods and Systems for Reducing Piracy of Media Content* | D1, ISR category X for claims 1–18; completed-copy transformations, arbitrary identifiers, delay, frame-rate change, collusion resistance | Official copy in PCT office-action dossier; US copy normally not required |
| A2 | US 2007/0067242 A1 / US 7,630,497 B2 | 2007-03-22 / 2009-12-08 | International Business Machines Corporation | *System and Method for Assigning Sequence Keys to a Media Player to Enable Hybrid Traitor Tracing* | File-segment variations, multiple file versions, assignment and traitor tracing; relevant to generic version/segment claims | Supplemental candidate; counsel materiality review required |
| A3 | US 2009/0320130 A1 / US 8,122,501 B2 | 2009-12-24 / 2012-02-21 | International Business Machines Corporation | *Traitor Detection for Multilevel Assignment* | Content divided into segments with variations, version assignments, recovered pirate files, and collusion/traitor detection | Supplemental candidate; counsel materiality review required |
| A4 | US 10,834,158 B1 | 2020-11-10 | Amazon Technologies, Inc. | *Encoding Identifiers into Customized Manifest Data* | Manifest-selected content-fragment patterns encode user identifiers and permit source determination; relevant to distribution/manifest claims | Supplemental candidate; counsel materiality review required |
| A5 | US 2012/0087583 A1 / US 8,837,769 B2 | 2012-04-12 / 2014-09-16 | Futurewei Technologies, Inc. | *Video Signature Based on Image Hashing and Shot Detection* | Perceptual image hashing, shot detection, and suspected/reference video comparison; relevant to detection dependents | Supplemental candidate; counsel materiality review required |

## 3. Foreign patent documents

| ID | Document | Date | Applicant / assignee | Title / relevance | Handling status |
|---|---|---:|---|---|---|
| B1 | CN 117278762 A | 2023-12-22 | Shenzhen Arboo Technology Co., Ltd. | *Secure and Traceable Video Encoding/Decoding System*; D2, ISR category A; codec-chain node metadata and watermarks | Copy in PCT dossier; obtain reliable English abstract or translation/explanation as counsel directs |
| B2 | WO 2021/224688 A1 | 2021-11-11 | Synamedia Limited | PCT family publication of D1 | Candidate defensive family citation; verify whether needed in addition to A1 |
| B3 | WO 2017/017603 A1 | 2017-02-02 | Vikramjeet S. Puri | *System to Detect Unauthorized Distribution of Media Content*; cited in the application's background | Bibliographic data completed; obtain official copy |
| B4 | WO 2010/044102 A2 | 2010-04-22 | Valuable Innovations Private Limited | *Visibly Non-Intrusive Digital Watermark Based Proficient, Unique & Robust Manual System for Forensic Detection of the Point of Piracy (POP) of a Copyrighted, Digital Video Content*; background citation | Bibliographic data completed; obtain official copy |
| B5 | CN 202455480 U | 2012-09-26 | Chengdu Doyen Information Technology Co., Ltd. | *Digital Watermark System for Verifying Digital Television Copyright*; background citation | Obtain official copy and English abstract/translation or explanation |
| B6 | CN 100583750 C | 2010-01-20 | Microsoft Corporation | *Desynchronized Fingerprinting Method and System for Digital Multimedia Data*; background citation; potentially relevant to desynchronization/fingerprinting | Microsoft family identified, but exact CN number remains to be verified against an official register; obtain official copy and English abstract/translation or explanation |
| B7 | WO 2021/141686 A1 | 2021-07-15 | Microsoft Technology Licensing, LLC | *Method of Identifying an Abridged Version of a Video*; shots separated by cuts, automatic comparison of target and reference video, piracy use | Supplemental candidate; obtain official WIPO copy; counsel materiality review required |
| B8 | EP 2 811 416 A1 | 2014-12-10 | Vestel Elektronik Sanayi ve Ticaret A.Ş. | *An Identification Method*; identifies video using subtitle timing patterns and explains temporal identification in view of removable visual watermarks | Official EPO A1 copy stored; inspect family/file history for examination reasoning and cited art; current legal status does not alter the A1 disclosure; counsel materiality review required |

## 4. Non-patent literature and prosecution documents

| ID | Reference | Reason / status |
|---|---|---|
| C1 | International Search Report, Form PCT/ISA/210, PCT/IB2025/051755, ISA/EP, mailed 13 May 2025 | Cites A1 and B1; official copy present |
| C2 | Written Opinion of the ISA, Form PCT/ISA/237, PCT/IB2025/051755, mailed 13 May 2025 | Finds claims 1–18 novel and industrially applicable but not inventive; official copy present |
| C3 | Tardos, G., “Optimal Probabilistic Fingerprint Codes,” STOC 2003, pp. 116–125 | Expressly cited in the description and relevant to probabilistic/collusion dependents; obtain complete publication copy and verify citation |
| C4 | EPO Information on Search Strategy for PCT/IB2025/051755 | Optional prosecution document; useful to show search scope if counsel elects to submit |
| C5 | Applicant's informal comments on the Written Opinion, if filed | Later-created prosecution document; counsel to decide whether a copy should accompany or be cross-referenced in the US record |
| C6 | Italian search report / written opinion for IT 102025000003210 | **Not presently in the repository.** Request from PRAXI/UIBM file and add all newly cited art when received |

## 5. Relevance recap for counsel—not text for the IDS form

| Art group | Features apparently known | Remaining proposed distinction to test |
|---|---|---|
| D1 / B6 | Completed-copy transformations, desynchronization, arbitrary identifiers, delay and frame-rate changes | Local reassignment of a temporal interval to frames from another synchronized camera by changing a recorded camera-selection boundary, followed by recovery of that boundary pattern |
| A2 / A3 | Segment variants, recipient/device assignments, recovered pirate versions, collusion tracing | Variants defined specifically by multi-camera edit-boundary movement rather than encrypted/watermarked file-segment versions |
| A4 | Recipient identifiers represented by patterns of manifest playback options/content fragments | Manifest pattern derived from camera-cut timing variants created at the multi-camera production stage |
| A5 / B7 | Shot detection, hashing, and comparison of suspected/target video to reference shots | Operational derivation and matching of camera-source-transition structure at regions where delivered versions select different synchronized camera views, followed by recipient resolution |
| B8 | Temporal patterns used as a content identifier; motivation to use temporal information where visual watermarks are removable | Per-recipient generation of multi-camera boundary patterns plus distribution association and forensic recovery |

## 6. Route-specific handling

1. **§371 national stage.** Confirm the PCT/DO/EO/903 or equivalent record shows which ISR references and copies were transmitted. Properly transmitted ISR references may be considered by the examiner without a duplicative IDS, but a conservative IDS may still be appropriate for clarity and for supplemental references.
2. **§111(a) bypass.** Do not assume the national-stage automatic-consideration procedure applies. Prepare a conventional IDS satisfying 37 CFR 1.97 and 1.98 for references counsel elects to submit.
3. **Foreign-language documents.** Provide copies and English translations, abstracts, or concise explanations as required and as available. If an English translation is already in the applicant's or counsel's possession or readily available, preserve and provide it for counsel review. Do not describe an unverified machine translation as authoritative.
4. **Timing.** Prefer filing the initial IDS with the US papers. Track later EP, Italian, or other national-phase citations and submit supplemental IDSs within the applicable 37 CFR 1.97 windows.

## 7. Completion checklist

The deferred retrieval, ownership/formalities, and EP-coordination tasks are organized in `AA11393US-deferred-filing-disclosure-and-EP-work_MEMO.md`. This checklist remains the disclosure inventory's operative reminder.

- [ ] Select §371 or bypass route and apply the correct IDS treatment.
- [ ] Verify all publication numbers, kind codes, dates, titles, inventors/applicants, and family relationships against official records.
- [ ] Obtain official copies of B3–B7 and complete foreign-document handling; the B8 A1 copy is already stored, but its EPO file-history review remains open.
- [ ] Obtain a complete copy of Tardos 2003.
- [ ] Request the Italian search report and add every new citation.
- [ ] Verify B6's exact CN publication number against an official register and obtain the appropriate copy and English handling.
- [ ] Inspect the B8 family and EPO file history; record status for completeness and review examination reasoning and newly identified citations.
- [ ] Obtain and preserve official copies of A2, A3, A5, B7, and Tardos 2003 if selected for submission or continuing materiality review.
- [ ] Review A2–A5 and B7–B8 for materiality in light of the final claims.
- [ ] Check whether other members of the A4 manifest-art citation family warrant review, particularly real-time anti-piracy, adaptive watermarking, and content-segment-variant references cited on its face.
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
