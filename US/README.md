# US — Counsel Briefing Package for PCT/IB2025/051755

This directory is the working prosecution package for the United States phase of PCT/IB2025/051755 (filed 19 February 2025; benefit claimed to US provisional 63/557,868 filed 26 February 2024). It is designed to let appointed US counsel evaluate and implement the filing strategy without having to reconstruct the technical, priority, prior-art, and enforcement analysis from the underlying record.

Except for a document expressly approved and signed for filing, everything here is **draft counsel work product**. Recommendations are deliberately candid. Filing-facing language, particularly the WIPO informal comments, is separately restrained because it will become public.

## 1. Controlling inventive-core statement

The proposed US strategy should consistently center on:

> version-specific, local movement of camera-selection boundaries using synchronized multi-camera source footage, recorded in a structured list of edit instructions, associated with recipients, and later recovered from the camera-cut timing pattern of suspected content.

The shorthand “many differently edited versions, not merely many marked copies of one completed edit” is useful to explain the architecture. It is not, by itself, the legal distinction. The claimable distinction is the complete data flow from multi-camera source material, through local edit-boundary variation and recipient association, to recovery of the same structural timing quantity.

## 2. Package map

| File | Function | Status / requested use |
|---|---|---|
| `AA11393US-US_counsel-briefing_DRAFT.md` | Executive strategy, risk ranking, actor map, route choice, and questions requiring counsel judgment | Start here |
| `AA11393US-US_claim-set_DRAFT.md` | Recommended four-independent-claim architecture, fallbacks, support notes, actor/enforcement analysis, and alternative claim-count options | Counsel to redraft and select claims; not for filing as-is |
| `AA11393US-priority-support-map_DRAFT.md` | Claim-feature mapping to both provisional 63/557,868 and the PCT application as filed | Counsel to confirm entitlement and continuity data |
| `AA11393US-prior-art-comparison-matrix_DRAFT.md` | Element-by-element comparison of D1, D2, and supplemental candidate art | Patentability analysis and IDS materiality review |
| `AA11393US-US_IDS-reference-list_DRAFT.md` | Disclosure inventory, document-handling status, relevance notes, and open items | Source data for counsel's IDS; not represented as complete |
| `AA11393US-PCT_informal-comments-IB_DRAFT.md` | Corrected public response to the ISA Written Opinion | PRAXI and US/EP counsel to align, verify quotations, and approve before ePCT filing |
| `prior-art/` | Local store of cited and candidate prior-art documents, keyed to the IDS inventory IDs (D1/D2 official copies extracted from the ISR transmittal; verified EP 2 811 416 A1; retrieval status for the rest) | Working copies — counsel obtains/verifies official copies for filing |

## 3. Source record

The working Markdown transcriptions under `../PCT/` are convenient search copies. The PDFs are the official record and control. D1 in particular was OCR-transcribed from a scanned copy; every quotation and paragraph reference must be checked against the official document before use.

| Source | Official document | Principal use |
|---|---|---|
| `../PCT/AA11393US-PCT_RAPPORTO_DEPOSITO_markdown/AA11393US-PCT_RAPPORTO_DEPOSITO.md` | `../PCT/AA11393US-PCT_RAPPORTO DEPOSITO.pdf` | PCT application as filed; §112 support; no-new-matter review |
| `../PCT/AA11393US-PCT_office_action_markdown/AA11393US-PCT_office_action.md` | `../PCT/PF-MA-AA11393US-PCT office action.pdf` | ISR, Written Opinion, examiner mapping, and clarity objections |
| `../PCT/AA11393US-PCT_office_action_markdown/cited_US2021-0352381A1.md` | D1 in the office-action PDF, pp. 17–40 | Closest-art response; signal transformation, delay, and frame-rate analysis |
| `../PCT/AA11393US-PCT_office_action_markdown/cited_CN117278762A.md` | D2 in the office-action PDF, pp. 41–65 | Secondary-art review and IDS |
| `../PPA2/as filed 63 557868.pdf` | Provisional application 63/557,868 as filed | Earliest-benefit support review |
| `../ITA/ITA depositi ufficiali/AA11393US-IT_Domanda di brevetto n. 102025000003210.pdf` | Italian filing dossier | Related-application data; no Italian search report is presently in the repository |

The folder name `PPA2` does not establish a second provisional. The local filing receipt and as-filed document identify provisional 63/557,868. Counsel should treat any assertion of a second provisional as unverified unless a separate filing receipt is produced.

## 4. Current prosecution assessment

| Priority | Issue | Direction supplied by this package |
|---|---|---|
| High | D1 is broader than a watermark-only characterization | Acknowledge D1's arbitrary identifiers, random/pseudorandom selection, delay, and frame-rate transformations; distinguish the synchronized multi-camera edit-boundary mechanism and closed recovery loop |
| High | All original US draft independent claims spanned production, distribution, and detection | Organize claims around the production operator, distributor/platform, detector/monitoring provider, and the end-to-end combination |
| High | Generic segment variants, manifest-coded identifiers, shot detection, hashing, and temporal fingerprints were known | Preserve novelty focus on local camera-source boundary substitution and later recovery; use supplemental art in the matrix and IDS review |
| High | PCT support is not the same as entitlement to the provisional date | Confirm every material claim limitation against both the provisional and PCT disclosures |
| High | Provisional Example 2 contains an internally inconsistent Cut 4 time, although its table and corrective text expressly state the reference-aligned time | Require a written counsel view on priority for resynchronization claims 2, 3, and 23; keep the issue in internal analysis unless counsel directs otherwise |
| High | Detection claim 16 can otherwise be characterized as generic matching of informational timing data | Require operational derivation and matching of camera-source-transition structure at regions where delivered versions select different synchronized camera views |
| Medium | D1's frame-rate transformation can change inter-cut intervals | Maintain a fallback requiring a local boundary shift and a later cut that retains reference timing or restores synchronization |
| Medium | Public comments can affect later claim interpretation | Avoid absolute statements about watermark exclusion, unmodified pixels, imperceptibility, attack resistance, or inherent scene integrity |
| Medium | §112(f), functional claiming, and algorithm disclosure | Prefer processor/configured-operation formulations and have counsel confirm corresponding structure and algorithmic support |
| Medium | Eligibility | Present the claims as a specific improvement to streaming-content differentiation and forensic recovery; describe the posture as improved, never “§101-safe” |
| Medium | Candidate set is exactly at the Track One 30/4 ceiling | Treat the set as having no net claim-count headroom; coordinate additions with cancellations and never amend above 30/4 or introduce a multiple-dependent claim while prioritized examination remains active |

## 5. Dates and procedural posture

| Date | Matter |
|---|---|
| **26 June 2026** | WIPO's recommended 28-month date for informal comments passed. This is a recommendation, not a formal bar. |
| **26 August 2026** | Thirty months from priority: practical last date for informal comments to be transmitted to designated Offices; US §371 entry or timely bypass filing must also be completed. Comments received after 30 months may remain in the IB file but are not transmitted in the normal course. |
| With US filing | File the counsel-approved IDS/disclosure package conservatively, subject to the different treatment of ISR references in a §371 national stage and a §111(a) bypass. |
| EP regional phase | Prepare the separate Rule 161 response; reuse only arguments and amendments approved for consistency with the public PCT record. |

## 6. Decisions requested from US counsel

1. Select §371 national stage or §111(a) bypass after comparing Track One, fees, priority-document requirements, restriction/unity practice, and prosecution objectives. Track One is not available for direct §371 entry but is available to an eligible bypass continuation.
2. Confirm the four-independent-claim actor architecture and whether the end-to-end claim should be a system or method claim.
3. Decide whether to retain any independent computer-readable-medium claim or use that claim slot for a commercially stronger subsystem claim.
4. Confirm the strongest support-safe wording for local camera-boundary movement, alternate-camera frame substitution, and later resynchronization.
5. Address expressly the provisional Example 2 inconsistency and its effect, if any, on the provisional date for resynchronization claims.
6. Preserve an operational camera-source-transition limitation in the detection independent rather than relying only on the informational origin of stored timing data.
7. Confirm §112(f), §112(a)/(b), and §101 posture and revise nonce terms such as “component” and “apparatus” where appropriate.
8. Confirm benefit to provisional 63/557,868 feature by feature and ensure ADS/continuity language is correct for the selected route.
9. Review every supplemental reference for materiality and complete the IDS, copies, translations, and concise explanations as required.
10. Verify entity status from current ownership, employees, licenses, and obligations to assign. The provisional claimed small-entity status, but that does not replace a current determination; separately assess micro-entity eligibility.
11. Confirm the inventor oath/declaration, applicant identity, assignment chain, and any necessary USPTO recordation for the selected filing route.
12. Align the WIPO informal comments with the intended US and EP positions and avoid unintended disclaimer.

## 7. Filing-readiness checklist

- [ ] Obtain counsel's claim-specific priority view on the provisional Example 2 inconsistency.
- [ ] Finalize claim 16 with a supported operational camera-source-transition relationship.
- [ ] Confirm that claims 21 and 28 affirmatively require mixed-version suspected content and performance of probabilistic attribution.
- [ ] Manage the 30/4 Track One set with no net claim-count headroom.
- [ ] Confirm a compliant inventor oath/declaration or authorized delayed/substitute handling.
- [ ] Confirm applicant identity, continuity/benefit data, assignment chain, obligations to assign, and any appropriate USPTO recordation.
- [ ] Verify CN 100583750 C against an official register and inspect the EP 2 811 416 A1 file history.
- [ ] Obtain the missing A2, A3, A5, B7, and Tardos 2003 copies selected for review or submission.
- [ ] Obtain the Italian search report and route every newly cited reference into the IDS review.
- [ ] Prepare the separate EP Rule 161 workstream consistently with the approved public PCT position.

## 8. Filing hygiene

- Do not file any Markdown document without attorney conversion to the required filing format and final record verification.
- Do not add unsupported matter to a bypass specification. If counsel proposes new technical matter, identify it as a possible continuation-in-part issue rather than silently treating it as PCT-supported.
- Do not characterize an IDS citation as an admission of prior-art status or materiality.
- Do not add an unnecessary US-specification admission that D1 is prior art; let counsel determine any required background treatment. Disclosure through an IDS is separate from an applicant admission.
- Maintain one consistent vocabulary: **reference content**, **mate**, **camera-selection boundary/camera cut**, **structured list of edit instructions**, **timing pattern**, **record of associations/ledger**, and **suspected unauthorized distribution**.
