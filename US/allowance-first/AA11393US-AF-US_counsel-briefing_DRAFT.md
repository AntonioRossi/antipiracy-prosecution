# AA11393US — AF Allowance-First US Counsel Briefing (DRAFT)

> **STRATEGY AF · CLAIM-SET VERSION AF-2026-07-17-v1 · STATUS 17 JULY 2026**
>
> **INTERNAL ATTORNEY BRIEFING — NOT FOR FILING.** “Allowance-first” is a proposed claim-selection strategy, not a prediction, promise, or legal conclusion. Use `AF claim N`, `NA claim N`, and `PCT claim N` outside the claim text.

## 1. Decision requested

Determine whether the initial US case should pursue AF claim 1 as a concentrated allowance-oriented anchor while preserving the actor-focused NA families through a timely continuation or other counsel-approved portfolio structure.

The requested first decisions are:

1. whether AF claim 1 is supported as a complete operational chain under § 112(a) and entitled, limitation by limitation, to the claimed filing dates;
2. whether its structural concentration materially improves the patentability position after a focused direct-art search;
3. whether its enforcement and proof costs are acceptable for the applicant's expected market; and
4. if AF is selected, who owns the continuation filing and what pre-issue gate will control it.

## 2. Allowance thesis—one operational chain

AF claim 1 requires a system to:

1. receive multi-camera video and a structured edit list identifying camera sources and cut time codes;
2. create a reference and a mate in which the **same ordered transition** from a first identified camera to a second identified camera occurs at noncoincident timings and the interval between those timings contains temporally corresponding frames from different cameras;
3. deliver generated versions and associate each recipient with a candidate pattern actually present in the delivered version;
4. examine suspected content at the corresponding distinguishing region and derive the detected source order and timing;
5. require both ordered source pair and timing to match at that region; and
6. use that match to search the association record and identify the recipient.

This is not a list of unrelated modules. Each claimed output constrains a later operation: the edit instructions determine generated content; generated content determines delivered candidate patterns; delivery populates the recipient record; and the same-region joint match supplies the lookup key.

The reviewed references densely teach pieces of the loop—variant delivery, customized manifests, timing patterns, shot/hash comparison, recipient records, and traitor tracing. No reviewed document was identified as disclosing the complete EDL-created physical-camera-boundary chain. That absence is a limited-search result, not a guarantee against anticipation or an obviousness combination.

## 3. Exact AF topology

The controlling candidate text is [`AA11393US-AF-US_claim-set_DRAFT.md`](AA11393US-AF-US_claim-set_DRAFT.md): **19 total claims / one independent system claim / 18 singly dependent claims / no multiple-dependent claim**.

| AF claims | Added function | Prosecution role |
|---|---|---|
| AF claim 1 | Integrated generation, delivery/association, same-region source-and-time detection, and recipient lookup | Claim-as-a-whole allowance candidate |
| AF claims 2–3 | Later-cut resynchronization; concrete ten-frame operation | Strong technical fallbacks, expressly priority-gated |
| AF claims 4–6 | EDL fields, live direction, plural cut regions | Concrete production fallbacks; direct EDL art remains an open search priority |
| AF claims 7–8 | Perceptual hashes and sliding-window fuzzy matching | Implementation detail; reviewed art is crowded |
| AF claims 9–10 | Manifest delivery, manifest-to-candidate-pattern association, switch-time derivation and reconstructed-manifest building, followed by delivered-manifest ledger lookup | Narrow implementation loop, inheriting the AF claim 1 source-identity gate |
| AF claims 11–12 | Mixed-copy positive attribution from recipient-associated candidate camera-source-transition patterns and a segmented Tardos implementation identifying a contributor for a respective portion | Collusion fallbacks; the pattern-input integration and exact portion-to-contributor relationship remain support-gated |
| AF claims 13–19 | Chunk/manifest delivery and implementation fallbacks | Preserve the physical-camera transition structure while adding packaging, delivery, mixing, repeated-region, or overlay detail |

Known mechanisms remain dependent because their presence alone is not the present novelty center. Do not promote manifests, hashing, timing fingerprints, CDN delivery, ledgers, or Tardos terminology as independent distinctions without claim-specific analysis.

## 4. Art pressure and examiner-facing position

The focused [`prior-art comparison matrix`](AA11393US-AF-prior-art-comparison-matrix_DRAFT.md) and [`claim-document mapping matrix`](AA11393US-AF-claim-document-mapping-matrix_DRAFT.md) identify the following principal pressure:

- **A4, US 10,834,158 B1**: customized manifests, camera-perspective alternatives, temporal alignment, version-pattern recovery, and probabilistic user resolution;
- **A6, US 2014/0325550 A1**: recipient-specific temporal events, tailored manifests, forced distinguishable events, detected-pattern comparison, and device/colluder identification;
- **B9, WO 2009/156973 A1**: key-derived actual switch points among desynchronized transformed streams;
- **B6, CN 100583750 C / Microsoft family**: individualized local frame-count/timing variation and robust hash reacquisition;
- **A5 and B7**: shot/cut and perceptual comparison; and
- **B8, EP 2 811 416 A1**: distortion-tolerant relative-time-pattern matching.

The most plausible § 103 route is conventional multicamera/vision-mixer/EDL practice combined with B9, A4, A6, or B6 for variation/delivery and A5, B7, B6, or B8 for recovery. The response should remain structural and operational:

- the same ordered transition between identified synchronized physical-camera sources;
- two noncoincident boundary timings and actual alternate-camera frames in the intervening interval;
- a candidate pattern generated from the delivered version;
- detection at the corresponding distinguishing region; and
- joint matching of both source order and timing before recipient lookup.

Do not argue that the number of combined references alone defeats obviousness. Require the rejection to identify every operation and an articulated reason and workable path to combine them. Conversely, do not characterize D1 or the supplemental art categorically; use the exact disclosures and qualifications recorded in the matrices.

A professional search directed to vision mixers, EDLs, personalized alternate-angle edits, screener differentiation, camera-boundary fingerprints, and recovery of source-camera identity remains a condition to any recommendation to broaden AF claim 1.

## 5. Mandatory § 112 and priority gates

AF's principal strength against the reviewed art is also its principal support risk. Counsel should use the [`AF priority/support map`](AA11393US-AF-priority-support-map_DRAFT.md) and record a written claim-as-a-whole analysis before filing.

### AF claim 1

The filings disclose the general closed loop. The exact candidate-pattern object, detection of both camera identities, same-region relation, and joint source-pair/timing match are combined formulations rather than one verbatim passage. Isolated disclosure of each noun or generic cut-time detection is insufficient. Prepare a support-safer alternative based on version timing or reconstructed-manifest matching if the exact formulation is not adequately conveyed.

### Example 2 and AF claims 2–3

At provisional PDF pp. 26–27, the mate table places Cut 4 at `00:00:30:01` and marks it adjusted to the reference. The accompanying text includes `00:00:30:11`, characterizes that value as a mistake, and then gives `00:00:30:01` as the correct approach; PCT Example 2 uses the cleaned value. Counsel must decide what a skilled reader would understand, whether the PCT text is permissible clarification, and whether AF claims 2–3 receive the provisional date. Keep resynchronization dependent unless that written analysis supports a different course.

### Combined examples and specific dependents

- The Examples 2→3→4 path for the moved boundary, chunks, manifests, and recipient assignment is the stronger combined-example route, but the exact AF relationship is not stated verbatim.
- The Examples 2→5 path for detecting both source identities and timing at the same region is materially weaker and affects AF claim 1 and AF claims 7–10.
- AF claim 11 applies probabilistic analysis to candidate camera-source-transition patterns associated with recipients and identifies recipients whose delivered versions contributed respective portions. That pattern-specific input is a combined-example relationship rather than a direct Tardos disclosure. AF claim 12 adds segmented Tardos fingerprints on content segments and positive identification of a contributor for at least one respective portion. The filings expressly discuss segmented Tardos handling and positive colluder identification, but counsel should confirm the pattern-input integration and the exact portion-to-contributor relationship. The earlier unsupported attribution-score formulation is not part of this AF set and should not be reintroduced without an identified basis.
- AF claim 14's equal-duration paired chunks are disclosed, but each chunk's claimed internal transition geometry at its respective timing is a combined-example formulation.
- AF claim 19's overlay is express; counsel must confirm the claimed before-segmentation sequence in the PCT disclosure and preserve a sequence-neutral alternative if needed.

Patentability value does not establish written description. A continuation cannot cure a § 112 deficiency in the common disclosure, and a continuation claim receives an earlier date only to the extent the required subject matter is adequately supported in the benefit chain.

Reopen priority and disclosure analysis if potentially material information appears with an effective date between 26 February 2024 and 19 February 2025 or an Office questions priority. Coordinate any resulting IDS or representation decision through the shared control documents.

## 6. Enforcement and evidence trade

AF claim 1 trades actor-specific scope and evidentiary simplicity for a concentrated patentability position. It may fit a vertically integrated broadcaster/platform or a system operated or controlled by one entity. It is not necessarily the strongest direct-infringement claim against a market divided among production, streaming, and monitoring providers.

Proof may require:

- the structured edit list or equivalent source/cut records;
- synchronized captures of different recipient versions;
- proof that the same ordered camera pair switches at different timings;
- the alternate-camera frame interval;
- delivery, manifest, candidate-pattern, and recipient-association records;
- suspect-side source identification and timing output at the same region; and
- the lookup linking the matched pattern to a recipient.

Before selecting AF as the sole initial independent, counsel should assess direction/control, system use, divided infringement, discovery access, reverse engineering, evidence preservation, and likely defendants. The crosswalk identifies NA subsystem coverage deliberately deferred rather than lost by accident.

## 7. Procedure and claim-count controls

AF-2026-07-17-v1 is numerically within the current 30-total/four-independent/no-multiple-dependent Track One limits and the basic 20-total/three-independent allocation. That formal fact does not establish eligibility, patentability, or allowance.

Counsel must decide and document:

- direct § 371 national-stage entry or a § 111(a) bypass continuation;
- whether Track One is available and worthwhile under the selected route;
- the compliant original-claim or preliminary-amendment format;
- continuity/benefit and priority-document data;
- oath/declaration, applicant, inventorship, assignment, entity-status, and fee handling; and
- restriction, unity, terminal-disclaimer, and double-patenting consequences.

Any amendment or renumbering requires a dependency check and coordinated update of both AF matrices, the support map, and the crosswalk.

## 8. Continuation is part of the AF decision

If AF is selected because actor-specific breadth is being deferred, continuation preservation is not an optional reminder. The applicant and US counsel should approve an owner, docket, trigger, proposed claim families, and completion evidence when the parent is filed.

The continuing application must satisfy the applicable copendency and benefit requirements. The internal safety rule is to file and verify the continuation **before the first parent patent issues**, with an earlier target no later than issue-fee handling unless counsel directs a safer event. A notice of allowance must trigger execution, not begin strategy discussion.

The controlling workflow is [`AA11393US-AF-continuation-preservation_MEMO.md`](AA11393US-AF-continuation-preservation_MEMO.md). It preserves, subject to support and business value:

1. standalone NA production coverage;
2. standalone NA distribution/recipient-association coverage;
3. standalone NA detection/recipient-resolution coverage;
4. method and software-medium alternatives; and
5. any properly elected/divided subject matter.

Continuation practice is not a cure for unsupported AF language, new matter, or a broken benefit chain.

## 9. Shared IDS, public comments, and consistency

Use only the canonical [`../common/AA11393US-US_IDS-reference-list_DRAFT.md`](../common/AA11393US-US_IDS-reference-list_DRAFT.md), [`../common/AA11393US-PCT_informal-comments-IB_DRAFT.md`](../common/AA11393US-PCT_informal-comments-IB_DRAFT.md), and [`../common/AA11393US-deferred-filing-disclosure-and-EP-work_MEMO.md`](../common/AA11393US-deferred-filing-disclosure-and-EP-work_MEMO.md).

The IDS inventory is not a concession that every listed item is prior art or material. Counsel must make and coordinate disclosure decisions for the parent and every continuation. Do not create an AF-specific public-comments draft. Any filed argument must remain consistent with the exact disclosure of D1 and the supplemental art and with positions taken in US, PCT, EP, and Italian proceedings.

## 10. Written recommendations requested from counsel

1. Is AF claim 1 adequately supported as a whole, including source identities, same-region detection, and joint source/time matching?
2. Which support-safer AF claim 1 alternative should be kept ready?
3. Does focused direct-art searching support the allowance thesis, and what combination is the examiner most likely to make?
4. Are AF claims 2–3 entitled to the provisional date despite the Example 2 inconsistency?
5. Are the Examples 2→3→4 relationships in AF claims 13–18 and the Examples 2→5 relationships in AF claims 1 and 7–10 adequately disclosed?
6. Are AF claim 11's recipient-associated candidate-pattern input and AF claim 12's segmented-fingerprint/portion-to-contributor relationship adequately conveyed, and is AF claim 14's exact chunk geometry supportable?
7. Is AF claim 19's before-segmentation order supported, or should a sequence-neutral fallback replace it?
8. Does AF claim 1 present an acceptable single-entity and evidence case for the applicant's likely targets?
9. Which NA families must be preserved in a continuation, and which have sufficient commercial value to justify filing cost?
10. Which application will be the parent, who owns the continuation docket, what is the target filing event, and what evidence will establish copendency before issue?
11. Which route and Track One posture should be used, and what restriction/double-patenting consequences are expected?
12. Are the shared IDS and public PCT comments approved, supplemented, or held, and who owns continuing disclosure monitoring?

## 11. Authorities for counsel to confirm at action time

- [USPTO MPEP § 201.07 — continuation applications](https://www.uspto.gov/web/offices/pac/mpep/s201.html)
- [USPTO MPEP § 211.01(b) — copendency and benefit](https://www.uspto.gov/web/offices/pac/mpep/s211.html)
- [USPTO MPEP § 1893 — § 371 national stage](https://www.uspto.gov/web/offices/pac/mpep/s1893.html)
- [USPTO MPEP § 1895 — bypass applications](https://www.uspto.gov/web/offices/pac/mpep/s1895.html)
- [USPTO Track One program](https://www.uspto.gov/patents/initiatives/patent-application-initiatives/prioritized-patent-examination-program)
- [USPTO MPEP § 708.02(b) — Track One controls](https://www.uspto.gov/web/offices/pac/mpep/s708.html)
- [USPTO MPEP § 609 — IDS practice](https://www.uspto.gov/web/offices/pac/mpep/s609.html)
- [USPTO MPEP § 2001 — duty of disclosure, candor, and good faith](https://www.uspto.gov/web/offices/pac/mpep/s2001.html)
- [USPTO MPEP § 2143 — obviousness rationales](https://www.uspto.gov/web/offices/pac/mpep/s2143.html)
