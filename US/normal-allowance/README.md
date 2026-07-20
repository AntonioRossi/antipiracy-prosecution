# AA11393US — Normal-Allowance / Balanced Actor-Split Package

> **STRATEGY NA · CLAIM-SET VERSION NA-2026-07-17-v1 · STATUS 17 JULY 2026**
>
> **INTERNAL COUNSEL-REVIEW DRAFT — NOT FOR FILING.** Use `NA claim N` outside the claim text. This is the current substantive baseline, not a prediction or guarantee of allowance.

This directory is the balanced, actor-split working package for the United States phase of PCT/IB2025/051755 (filed 19 February 2025; benefit claimed to US provisional 63/557,868 filed 26 February 2024). It should be read as an alternative to [`../allowance-first/`](../allowance-first/), not combined with that claim set by implication.

Except for a document expressly approved and signed for filing, everything here is an **internal counsel-review draft**. Recommendations are deliberately candid. Filing-facing language, particularly the WIPO informal comments, is separately restrained because it will become public.

**Circulation and record control.** The labels used in this repository do not establish attorney-client privilege, work-product protection, or any other protected status. At the applicant's initial secure transmission to retained US counsel, and before any wider circulation, US counsel should determine the package's appropriate treatment under applicable law, approve the intended recipients and purpose, and control further circulation. Preserve originals, versions, comments, transmission records, and final filed copies under counsel-approved retention and any applicable legal-hold instructions.

## 1. Controlling inventive-core statement

The proposed US strategy should consistently center on:

> version-specific, local movement of a recorded camera-selection boundary so that the same ordered transition from a first camera source to a second camera source occurs at noncoincident switch timings in a reference and a mate, with temporally corresponding frames from different cameras in the intervening interval; preservation of one of those transition positions through manifest/chunk selection and recipient association; and later recovery and matching of both the ordered source transition and its switch timing from suspected content.

The shorthand “many differently edited versions, not merely many marked copies of one completed edit” is useful to explain the architecture. It is not, by itself, the legal distinction. The claimable distinction is the complete data flow from multi-camera source material, through local edit-boundary variation and recipient association, to recovery of the same structural timing quantity.

### Pattern terminology used in this package

- **Camera-cut timing pattern** means the sequence or arrangement of camera-switch times produced in a version and, where applicable, represented by chunks or manifests for distribution. In NA claims 9 and 22 it is structurally constrained by identified camera sources and by the switch timing actually preserved in the corresponding delivered version; it is not an arbitrary fragment-version sequence relabeled as camera timing.
- **Camera-source-transition pattern** means the detection-side structure that identifies ordered camera-source transitions together with their corresponding camera-switch timings for operational comparison.

The terms serve different claim functions rather than defining a strict information-content hierarchy. In NA claims 9 and 22, a camera-cut timing pattern records the identified source pair and the switch timing contained in a delivered version. In NA claim 16, candidate and detected camera-source-transition patterns organize ordered source transitions and corresponding timings at candidate-distinguishing regions for operational derivation and matching. NA claims 9 and 22 therefore do not rely on timing alone, and NA claim 16 does not rely merely on a label applied to generic timing data. Counsel should not treat the terms as accidental synonyms or unify them without reviewing support, prior art, and scope.

## 2. Package map

| File | Function | Status / requested use |
|---|---|---|
| [`AA11393US-NA-US_counsel-briefing_DRAFT.md`](AA11393US-NA-US_counsel-briefing_DRAFT.md) | Executive strategy, risk ranking, actor map, route choice, and questions requiring counsel judgment | Start here |
| [`AA11393US-NA-US_claim-set_DRAFT.md`](AA11393US-NA-US_claim-set_DRAFT.md) | Four-independent-claim architecture, fallbacks, support notes, and enforcement analysis | Counsel to redraft and select claims; not for filing as-is |
| [`AA11393US-NA-priority-support-map_DRAFT.md`](AA11393US-NA-priority-support-map_DRAFT.md) | NA-claim mapping to provisional 63/557,868 and the PCT application as filed | Counsel to confirm entitlement and continuity data |
| [`AA11393US-NA-prior-art-comparison-matrix_DRAFT.md`](AA11393US-NA-prior-art-comparison-matrix_DRAFT.md) | Feature and claim-impact comparison of D1, D2, and supplemental candidate art | Analytic source for the NA claim grid |
| [`AA11393US-NA-claim-document-mapping-matrix_DRAFT.md`](AA11393US-NA-claim-document-mapping-matrix_DRAFT.md) | Claim-by-claim projection against each reviewed document | Valid only for `NA-2026-07-17-v1` |
| [`../common/`](../common/) | Canonical IDS, public comments, and deferred filing/disclosure/formalities/EP controls | Shared; do not duplicate here |
| [`../prior-art/`](../prior-art/) | Canonical source PDFs, transcriptions, provenance, checksums, and remaining retrieval work | Shared; do not annotate or duplicate here |

## 3. Source record

The working Markdown transcriptions under `../../PCT/` are convenient search copies. The PDFs are the official record and control. D1 in particular was OCR-transcribed from a scanned copy; every quotation and paragraph reference must be checked against the official document before use.

| Source | Official document | Principal use |
|---|---|---|
| `../../PCT/AA11393US-PCT_RAPPORTO_DEPOSITO_markdown/AA11393US-PCT_RAPPORTO_DEPOSITO.md` | `../../PCT/AA11393US-PCT_RAPPORTO DEPOSITO.pdf` | PCT application as filed; §112 support; no-new-matter review |
| `../../PCT/AA11393US-PCT_office_action_markdown/AA11393US-PCT_office_action.md` | `../../PCT/PF-MA-AA11393US-PCT office action.pdf` | ISR, Written Opinion, examiner mapping, and clarity objections |
| `../../PCT/AA11393US-PCT_office_action_markdown/cited_US2021-0352381A1.md` | D1 in the office-action PDF, pp. 17–40 | Closest-art response; signal transformation, delay, and frame-rate analysis |
| `../../PCT/AA11393US-PCT_office_action_markdown/cited_CN117278762A.md` | D2 in the office-action PDF, pp. 41–65 | Secondary-art review and IDS |
| `../../PPA2/as filed 63 557868.pdf` | Provisional application 63/557,868 as filed | Earliest-benefit support review |
| `../../ITA/ITA depositi ufficiali/AA11393US-IT_Domanda di brevetto n. 102025000003210.pdf` | Italian filing dossier | Related-application data; no Italian search report is presently in the repository |

The folder name `PPA2` does not establish a second provisional. The local filing receipt and as-filed document identify provisional 63/557,868. Counsel should treat any assertion of a second provisional as unverified unless a separate filing receipt is produced.

## 4. Current prosecution assessment

| Priority | Issue | Direction supplied by this package |
|---|---|---|
| High | D1 is broader than a watermark-only characterization | Acknowledge D1's arbitrary identifiers, random/pseudorandom selection, delay, and frame-rate transformations; distinguish the synchronized multi-camera edit-boundary mechanism and closed recovery loop |
| High | All original US draft independent claims spanned production, distribution, and detection | Organize claims around the production operator, distributor/platform, detector/monitoring provider, and the end-to-end combination |
| High | Generic segment variants, manifest-coded identifiers, shot detection, hashing, and temporal fingerprints were known | Preserve novelty focus on local camera-source boundary substitution and later recovery; use supplemental art in the matrix and IDS review |
| High | A4 combines camera-perspective fragment alternatives, customized manifests, unauthorized-copy pattern recovery, and probabilistic recipient resolution; A6 supplies recipient-specific temporal events/manifests and a detection-to-user loop | Do not rely on a generic “camera-cut origin” label. In NA claims 9, 16, and 22 preserve the same ordered camera-source transition at different switch timings, the intervening alternate-camera interval, and matching of transition identity plus timing at the distinguishing region |
| High | B9 teaches key-derived, user-different actual stream-switch positions selected with reference to shot cuts; its time/switch pattern is not fixed | Distinguish B9 through synchronized physical-camera provenance, the structured edit list and moved recorded camera boundary, not through variable switch timing by itself |
| High | PCT support is not the same as entitlement to the provisional date | Confirm every material claim limitation against both the provisional and PCT disclosures |
| High | Provisional Example 2 contains an internally inconsistent Cut 4 time, although its table and corrective text expressly state the reference-aligned time | Require a written counsel view on priority for resynchronization NA claims 2, 3, and 23; keep the issue in internal analysis unless counsel directs otherwise |
| High | Detection NA claim 16 can otherwise be characterized as generic matching of informational timing data | Require operational derivation and matching of camera-source-transition structure at regions where delivered versions select different synchronized camera views |
| High | Later-discovered information may make entitlement to the provisional date outcome-determinative | If potentially material art or another prior-art event has an effective date after 26 February 2024 but before 19 February 2025, or an Office challenges priority, require counsel to reassess priority, disclosure obligations, and every effective-filing-date representation |
| Medium | D1's frame-rate transformation can change inter-cut intervals | Maintain a fallback requiring a local boundary shift and a later cut that retains reference timing or restores synchronization |
| Medium | B6 teaches recipient-specific local frame-count/timing variation and hash reacquisition robust to temporal edits and advertisements | Treat timing-only, relative-timing, and hash-reacquisition fallbacks as known; preserve different-camera provenance and the moved ordered source transition |
| Medium | No reviewed document supplies the full claimed multi-camera boundary mechanism, but the review was limited | Commission a focused search of vision-mixer, live-production EDL, multi-camera personalization, alternate-angle streaming, individualized screener editing, and camera-boundary-shifting art before deleting the structural limitations in NA claims 7, 9, 13, 15, 16, 22, or 29 |
| Medium | Public comments can affect later claim interpretation | Avoid absolute statements about watermark exclusion, unmodified pixels, imperceptibility, attack resistance, or inherent scene integrity |
| Medium | §112(f), functional claiming, and algorithm disclosure | Prefer processor/configured-operation formulations and have counsel confirm corresponding structure and algorithmic support |
| Medium | Eligibility | Present the claims as a specific improvement to streaming-content differentiation and forensic recovery; describe the posture as improved, never “§101-safe” |
| Medium | Candidate set is exactly at the Track One 30/4 ceiling | Treat the set as having no net claim-count headroom; coordinate additions with cancellations and never amend above 30/4 or introduce a multiple-dependent claim while prioritized examination remains active |

## 5. Dates and procedural posture

The controlling strategy-neutral deadline snapshot and the separate US-filing, EP-entry, and Rule 161/162 work gates are in the canonical [`deferred filing, disclosure, and EP work memo`](../common/AA11393US-deferred-filing-disclosure-and-EP-work_MEMO.md). Do not maintain an NA-only date copy. Counsel must independently confirm every deadline, docket earlier internal targets, and record completion evidence there.

## 6. Decisions requested from US counsel

1. Select §371 national stage or §111(a) bypass after comparing Track One, fees, priority-document requirements, restriction/unity practice, and prosecution objectives. Track One is not available for direct §371 entry but is available to an eligible bypass continuation.
2. Confirm the four-independent-claim actor architecture and whether the end-to-end claim should be a system or method claim.
3. Decide whether to retain any independent computer-readable-medium claim or use that claim slot for a commercially stronger subsystem claim.
4. Confirm the strongest support-safe wording for local camera-boundary movement, alternate-camera frame substitution, and later resynchronization.
5. Address expressly the provisional Example 2 inconsistency and its effect, if any, on the provisional date for resynchronization claims.
6. Preserve an operational camera-source-transition limitation in the detection independent rather than relying only on the informational origin of stored timing data.
7. Confirm that NA claim 16 support-safely ties the candidate inter-version difference, detection, and matching to the same candidate-distinguishing region and requires agreement in both the ordered camera-source transition and its switch timing.
8. Confirm that “camera-cut timing pattern” and “camera-source-transition pattern” retain the distinct claim functions stated above and that NA claims 17–18 are support-safe as harmonized.
9. Confirm written-description and priority support for the structural replacements in NA claims 7, 13, and 29: retained source identifiers around a moved ordered transition; different manifests selecting equal-duration reference and mate chunks spanning the same playback interval, with each chunk containing the transition at its respective timing; and manifest assembly preserving either the reference or varied position of that transition.
10. Confirm §112(f), §112(a)/(b), and §101 posture and revise nonce terms such as “component” and “apparatus” where appropriate.
11. Confirm benefit to provisional 63/557,868 feature by feature and ensure ADS/continuity language is correct for the selected route.
12. Establish a monitoring rule for potentially material information having an effective prior-art date in the provisional-to-PCT interval and for any Office priority challenge.
13. Review every supplemental reference for materiality, commission the focused multi-camera/EDL search, and complete copies, translations, concise explanations, and IDS decisions as required.
14. Verify entity status from current ownership, employees, licenses, and obligations to assign. The provisional claimed small-entity status, but that does not replace a current determination; separately assess micro-entity eligibility.
15. Confirm the inventor oath/declaration, applicant identity, assignment chain, and any necessary USPTO recordation for the selected filing route.
16. Align the WIPO informal comments with the intended US and EP positions and avoid unintended disclaimer.
17. Evaluate NA claim 9's increased infringement-proof burden and adopt an evidence plan, including controlled captures from multiple recipient sessions and anticipated discovery into manifest/source-chunk mappings and recipient-association records.
18. Determine and document the package's confidentiality, privilege/work-product, circulation, access, version-control, retention, and legal-hold treatment without relying on repository labels as establishing protection.

## 7. Filing-readiness checklist

- [ ] Obtain counsel's claim-specific priority view on the provisional Example 2 inconsistency.
- [ ] Reassess that priority view if potentially material information has an effective prior-art date between 26 February 2024 and 19 February 2025 or an Office challenges priority.
- [ ] Confirm support for NA claim 16's same-region operational relationship: stored noncoincident positions of the same ordered camera-source transition, detection at that candidate-distinguishing region, and matching of both source order and timing.
- [ ] Confirm support for the structural fallbacks in NA claims 7, 13, and 29 and the relationship between PCT Examples 2–4 and the corresponding provisional passages in NA claims 9, 13, 15, and 29.
- [ ] Approve an NA claim 9 infringement-evidence plan addressing controlled multi-recipient captures, content comparison, and discovery into manifest/source-chunk mappings and recipient associations.
- [ ] Obtain US counsel's written package-handling determination and implement approved recipient, access, circulation, version, retention, and legal-hold controls.
- [ ] Confirm the distinct claim functions of camera-cut timing patterns and camera-source-transition patterns and approve the harmonized NA claims 17–18.
- [ ] Confirm that NA claims 21 and 28 affirmatively require mixed-version suspected content and performance of probabilistic attribution, and confirm written-description support for NA claim 21's candidate contributions and respective attribution scores.
- [ ] Manage the 30/4 Track One set with no net claim-count headroom.
- [ ] Confirm a compliant inventor oath/declaration or authorized delayed/substitute handling.
- [ ] Confirm applicant identity, continuity/benefit data, assignment chain, obligations to assign, and any appropriate USPTO recordation.
- [ ] Complete authoritative English-family and foreign-language handling for B6 and inspect the EP 2 811 416 A1 file history.
- [ ] Confirm the stored patent working copies against official registers; obtain Lin 2008 (C7) — Tardos 2003 (C3) was stored 20.07.2026 in its author-hosted extended form, with the STOC version reserved for counsel's filing-copy decision; and decide publication/grant-pair and supplemental-reference treatment.
- [ ] Commission and document the focused search for direct vision-mixer/EDL/multi-camera boundary-personalization art and reassess NA claims 1, 7, 9, 13, 15, 16, 22, and 29 against its results.
- [ ] Obtain the Italian search report and route every newly cited reference into the IDS review.
- [ ] Confirm and docket the nominal and apparently weekend-adjusted European-phase entry dates, set an earlier internal deadline, and complete the applicable Rule 159 entry acts and Rule 162 entry-stage claims-fee plan.
- [ ] On receipt of the EPO communication, docket and prepare the separate six-month Rule 161/162 response workstream consistently with the approved public PCT and US positions.

The document-retrieval, disclosure, formalities, ownership, and EP tasks above are controlled in more detail by [`../common/AA11393US-deferred-filing-disclosure-and-EP-work_MEMO.md`](../common/AA11393US-deferred-filing-disclosure-and-EP-work_MEMO.md).

## 8. Filing hygiene

- Do not file any Markdown document without attorney conversion to the required filing format and final record verification.
- Do not add unsupported matter to a bypass specification. If counsel proposes new technical matter, identify it as a possible continuation-in-part issue rather than silently treating it as PCT-supported.
- Do not characterize an IDS citation as an admission of prior-art status or materiality.
- Do not add an unnecessary US-specification admission that D1 is prior art; let counsel determine any required background treatment. Disclosure through an IDS is separate from an applicant admission.
- Maintain one consistent vocabulary: **reference content**, **mate**, **camera-selection boundary/camera cut**, **structured list of edit instructions**, **camera-cut timing pattern**, **camera-source-transition pattern**, **record of associations/ledger**, and **suspected unauthorized distribution**. Preserve the distinct claim functions of the two pattern terms rather than flattening them into synonyms or treating one as categorically richer than the other.
