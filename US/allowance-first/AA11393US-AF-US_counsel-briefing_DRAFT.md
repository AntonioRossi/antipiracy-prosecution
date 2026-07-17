# AA11393US — AF Allowance-First US Counsel Briefing (DRAFT)

> **STRATEGY AF · CLAIM-SET VERSION AF-2026-07-17-v2 · STATUS 17 JULY 2026**
>
> **INTERNAL ATTORNEY BRIEFING — NOT FOR FILING.** “Allowance-first” is a proposed claim-selection strategy, not a prediction, promise, or legal conclusion. Use `AF claim N`, `NA claim N`, and `PCT claim N` outside the claim text.
>
> **TERMINOLOGY / FAMILY-RECORD NON-CONCESSION.** AF's use of `camera-source-transition pattern` is a deliberate claim-drafting label for the ordered source identities and switch timing positively recited in the AF claims. It does not declare that term synonymous with, narrower than, or exhaustive of `camera-cut timing pattern`; redefine either term in the specification or NA branch; disclaim timing-only, manifest-based, or other disclosed embodiments; or state a claim-construction position. Counsel must preserve this distinction in any filed amendment or argument and assess family-wide disclaimer and construction effects before characterizing either expression.

## 1. Decision requested

Determine whether the initial US case should pursue AF claim 1 as a concentrated allowance-oriented system anchor and AF claim 20 as its independent method counterpart, while preserving the actor-focused NA families through a timely continuation or other counsel-approved portfolio structure. Counsel may omit or cancel AF claim 20 at filing if the documented strategy choice is to retain one-independent-claim simplicity; AF claim 20 is an evaluated option, not an instruction to sacrifice that objective automatically.

The requested first decisions are:

1. whether AF claim 1 and AF claim 20 are each supported as a complete operational chain under § 112(a) and entitled, limitation by limitation, to the claimed filing dates;
2. whether the structural concentration of the AF independents materially improves the patentability position after a focused direct-art search;
3. whether the enforcement and proof costs of AF claim 1 and AF claim 20 are acceptable for the applicant's expected market;
4. whether AF claim 20's additional method-enforcement category justifies a second independent claim after considering § 101, restriction, proof, and examination focus; and
5. if AF is selected, who owns the continuation filing and what pre-issue gate will control it.

## 2. Allowance thesis—one operational chain in two claim categories

AF claim 1 requires a system to:

1. receive multi-camera video and a structured edit list identifying camera sources and cut time codes;
2. create a reference and a mate in which the **same ordered transition** from a first identified camera to a second identified camera occurs at noncoincident timings and the interval between those timings contains temporally corresponding frames from different cameras;
3. deliver generated versions and associate each recipient with a candidate pattern actually present in the delivered version;
4. examine suspected content at the corresponding distinguishing region and derive the detected source order and timing;
5. require both ordered source pair and timing to match at that region; and
6. use that match to search the association record and identify the recipient.

This is not a list of unrelated modules. Each claimed output constrains a later operation: the edit instructions determine generated content; generated content determines delivered candidate patterns; delivery populates the recipient record; and the same-region joint match supplies the lookup key.

The reviewed references densely teach pieces of the loop—variant delivery, customized manifests, timing patterns, shot/hash comparison, recipient records, and traitor tracing. No reviewed document was identified as disclosing the complete structured-list-created identified-camera-boundary chain recited by the AF independents. An EDL is a likely implementation and important search field, but EDL fields first become an express limitation in AF claim 4. The limited-search absence is not a guarantee against anticipation or an obviousness combination.

AF claim 20 places the integrated operations in method form. It does not add a separate technical distinction over the reviewed art or improve the patentability thesis merely by changing statutory category. Its purpose is to preserve a method-performance theory if the applicant and counsel conclude that the added enforcement category is worth the second independent claim.

## 3. Exact AF topology

The controlling candidate text is [`AA11393US-AF-US_claim-set_DRAFT.md`](AA11393US-AF-US_claim-set_DRAFT.md): **20 total claims / two independent claims (AF claim 1 system; AF claim 20 method) / 18 singly dependent claims / no multiple-dependent claim**. Counsel may omit or cancel AF claim 20 at filing for a documented one-independent-claim strategy; if so, annotate the actual filed topology across the claim-indexed AF documents rather than silently treating all 20 claims as filed or creating a second AF package.

| AF claims | Added function | Prosecution role |
|---|---|---|
| AF claim 1 | Integrated generation, delivery/association, same-region source-and-time detection, and recipient lookup | Claim-as-a-whole allowance candidate |
| AF claims 2–3 | Later-cut resynchronization; concrete ten-frame operation | Strong technical fallbacks, expressly priority-gated |
| AF claims 4–6 | EDL fields, live direction, plural cut regions | Concrete production fallbacks; direct EDL art remains an open search priority |
| AF claims 7–8 | Perceptual hashes and sliding-window fuzzy matching | Implementation detail; reviewed art is crowded |
| AF claims 9–10 | Manifest delivery, manifest-to-candidate-pattern association, switch-time derivation and reconstructed-manifest building, followed by delivered-manifest ledger lookup | Narrow implementation loop, inheriting the AF claim 1 source-identity gate |
| AF claims 11–12 | Mixed-copy positive attribution from recipient-associated candidate camera-source-transition patterns and a segmented Tardos implementation identifying a contributor for a respective portion | Collusion fallbacks; the pattern-input integration and exact portion-to-contributor relationship remain support-gated |
| AF claims 13–19 | Chunk/manifest delivery and implementation fallbacks | Preserve the identified-camera transition structure while adding packaging, delivery, mixing, repeated-region, or overlay detail |
| AF claim 20 | Independent performance of the integrated generation-through-recipient-identification method | Additional enforcement category based on the same technical chain; not an additional patentability thesis and subject to every AF claim 1 support/priority gate |

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

- the same ordered transition between identified camera sources;
- two noncoincident boundary timings and actual alternate-camera frames in the intervening interval;
- a candidate pattern generated from the delivered version;
- detection at the corresponding distinguishing region; and
- joint matching of both source order and timing before recipient lookup.

Do not argue that the number of combined references alone defeats obviousness. Require the rejection to identify every operation and an articulated reason and workable path to combine them. Conversely, do not characterize D1 or the supplemental art categorically; use the exact disclosures and qualifications recorded in the matrices.

A professional search directed to vision mixers, EDLs, personalized alternate-angle edits, screener differentiation, camera-boundary fingerprints, and recovery of source-camera identity remains a condition to any recommendation to broaden either AF independent.

## 5. Mandatory § 112 and priority gates

AF's principal strength against the reviewed art is also its principal support risk. Counsel should use the [`AF priority/support map`](AA11393US-AF-priority-support-map_DRAFT.md) and record a written claim-as-a-whole analysis before filing.

### AF claim 1

The filings disclose the general closed loop. The exact candidate-pattern object, detection of both camera identities, same-region relation, and joint source-pair/timing match are combined formulations rather than one verbatim passage. Isolated disclosure of each noun or generic cut-time detection is insufficient. Prepare a support-safer alternative based on version timing or reconstructed-manifest matching if the exact formulation is not adequately conveyed.

### AF claim 20

AF claim 20 independently recites the integrated operations in method form. Although it does not depend from AF claim 1, every AF claim 1 claim-as-a-whole, candidate-pattern, source-identity, same-region, joint-matching, combined-example, and priority gate applies to the corresponding AF claim 20 limitations. Changing statutory category does not supply missing disclosure or an earlier effective date. Counsel must also assess the method claim as a whole under § 101, including whether its concrete video-generation, delivery-record, suspect-analysis, and lookup operations provide the required eligible-application context under then-current law.

### Example 2 and AF claims 2–3

At provisional PDF pp. 26–27, the mate table places Cut 4 at `00:00:30:01` and marks it adjusted to the reference. The accompanying text includes `00:00:30:11`, characterizes that value as a mistake, and then gives `00:00:30:01` as the correct approach; PCT Example 2 uses the cleaned value. Counsel must decide what a skilled reader would understand, whether the PCT text is permissible clarification, and whether AF claims 2–3 receive the provisional date. Keep resynchronization dependent unless that written analysis supports a different course.

### Combined examples and specific dependents

- The Examples 2→3→4 path for the moved boundary, chunks, manifests, and recipient assignment is the stronger combined-example route, but the exact AF relationship is not stated verbatim.
- The Examples 2→5 path for detecting both source identities and timing at the same region is materially weaker and affects AF claim 1 and AF claims 7–10.
- AF claim 20 affirmatively repeats the complete generation, delivery/association, detection, matching, and lookup sequence; the method format does not reduce either combined-example concern above.
- AF claim 11 applies probabilistic analysis to candidate camera-source-transition patterns associated with recipients and identifies recipients whose delivered versions contributed respective portions. That pattern-specific input is a combined-example relationship rather than a direct Tardos disclosure. AF claim 12 adds segmented Tardos fingerprints on content segments and positive identification of a contributor for at least one respective portion. The filings expressly discuss segmented Tardos handling and positive colluder identification, but counsel should confirm the pattern-input integration and the exact portion-to-contributor relationship. The earlier unsupported attribution-score formulation is not part of this AF set and should not be reintroduced without an identified basis.
- AF claim 14's equal-duration paired chunks are disclosed, but each chunk's claimed internal transition geometry at its respective timing is a combined-example formulation.
- AF claim 19's overlay is express; counsel must confirm the claimed before-segmentation sequence in the PCT disclosure and preserve a sequence-neutral alternative if needed.

Patentability value does not establish written description. A continuation cannot cure a § 112 deficiency in the common disclosure, and a continuation claim receives an earlier date only to the extent the required subject matter is adequately supported in the benefit chain.

Reopen priority and disclosure analysis if potentially material information appears with an effective date between 26 February 2024 and 19 February 2025 or an Office questions priority. Coordinate any resulting IDS or representation decision through the shared control documents.

## 6. Enforcement and evidence trade

AF claim 1 and AF claim 20 trade actor-specific scope and evidentiary simplicity for a concentrated technical chain. Neither is necessarily the strongest direct-infringement claim against a market divided among production, streaming, and monitoring providers, and adding method form does not convert separated commercial conduct into single-actor infringement.

### AF claim 1—whole-system use

For a system claim, counsel should analyze whether a target makes, sells, offers, or **uses the claimed system as a whole**. Under the fact-specific `Centillion` framework, a party may use a distributed system by putting the entire claimed system into service, controlling that system-level use, and obtaining its benefit even without physically possessing every component. `CloudofChange` confirms the limit: a vendor is not necessarily the user merely because it supplies or hosts part of the system when independent customers initiate and benefit from the claimed whole-system operation and their acts are not attributable to the vendor. The package therefore must not assume that ownership of servers, provision of software, or customer access alone establishes AF claim 1 infringement.

### AF claim 20—performance or attribution of method steps

For a method claim, direct infringement ordinarily requires every claimed step to be performed by one entity or to be attributable to one entity. Under the fact-specific `Akamai` framework, attribution may exist through agency, contract, joint enterprise, or direction/control, including circumstances in which an alleged infringer conditions participation in an activity or receipt of a benefit on performance of claimed steps and establishes the manner or timing of that performance. The presence of a commercial relationship, instructions, or a platform by itself does not establish the test. AF claim 20 adds a method-performance and potential attribution category; it does not guarantee an attribution theory, alter the prior-art comparison, or independently improve patentability.

Do not transpose the two analyses: `Akamai` method-step attribution does not by itself establish that a party uses AF claim 1's claimed system as a whole, and `Centillion` system use does not dispense with proof that every AF claim 20 step was performed by or attributable to one entity.

Proof may require:

- the structured edit list or equivalent source/cut records;
- synchronized captures of different recipient versions;
- proof that the same ordered camera pair switches at different timings;
- the alternate-camera frame interval;
- delivery, manifest, candidate-pattern, and recipient-association records;
- suspect-side source identification and timing output at the same region; and
- the lookup linking the matched pattern to a recipient.

AF claim 20 additionally requires proof of who performed each affirmative step, when it was performed, and the facts supporting attribution if multiple actors were involved. Before selecting AF claim 1 and AF claim 20—or omitting AF claim 20 for one-independent simplicity—counsel should assess direction/control, whole-system use, method-step attribution, divided infringement, discovery access, reverse engineering, evidence preservation, § 101, restriction, and likely defendants. The crosswalk identifies broader and actor-focused NA coverage deliberately deferred rather than lost by accident.

## 7. Procedure and claim-count controls

AF-2026-07-17-v2 contains 20 total claims, two independent claims, 18 singly dependent claims, and no multiple-dependent claim. It is numerically within the current 30-total/four-independent/no-multiple-dependent Track One limits and exactly uses the basic 20-total allocation while remaining below the basic three-independent allocation. That formal fact does not establish eligibility, patentability, allowance, or that two independent categories best serve the allowance-first objective.

Counsel is expressly authorized to omit AF claim 20 from the original filing or cancel it in the filing amendment if a documented decision favors one-independent-claim simplicity. Conversely, AF claim 20 should not be retained merely because numerical room exists. The filed claim listing, count, matrices, support map, crosswalk, and strategy record must identify which topology was actually submitted.

Counsel must decide and document:

- direct § 371 national-stage entry or a § 111(a) bypass continuation;
- whether Track One is available and worthwhile under the selected route;
- the compliant original-claim or preliminary-amendment format;
- continuity/benefit and priority-document data;
- oath/declaration, applicant, inventorship, assignment, entity-status, and fee handling; and
- restriction, unity, terminal-disclaimer, and double-patenting consequences.

System and method claims directed to corresponding operations may still draw restriction, classification, search, or election treatment; counsel must not equate two statutory categories with two patentably distinct inventions or assume they will be examined together.

This briefing and the associated AF analyses are valid only for `AF-2026-07-17-v2`. The expressly authorized omission or cancellation of AF claim 20 must be recorded across the single AF-v2 package but does not require creation of a separate system-only package. Any other amendment, omission, cancellation, renumbering, terminology characterization, or route-driven claim-status change requires a dependency/count check, an actual-filed-topology record, and coordinated updates of both AF matrices, the support map, and the crosswalk. No filed argument should turn AF's transition-pattern label into a narrowing family-wide definition or disclaimer without an express, recorded counsel decision.

## 8. Continuation is part of the AF decision

If AF is selected because actor-specific breadth is being deferred, continuation preservation is not an optional reminder. The applicant and US counsel should approve an owner, docket, trigger, proposed claim families, and completion evidence when the parent is filed.

The continuing application must satisfy the applicable copendency and benefit requirements. The internal safety rule is to file and verify the continuation **before the first parent patent issues**, with an earlier target no later than issue-fee handling unless counsel directs a safer event. A notice of allowance must trigger execution, not begin strategy discussion.

The controlling workflow is [`AA11393US-AF-continuation-preservation_MEMO.md`](AA11393US-AF-continuation-preservation_MEMO.md). It preserves, subject to support and business value:

1. standalone NA production coverage;
2. standalone NA distribution/recipient-association coverage;
3. standalone NA detection/recipient-resolution coverage;
4. broader or actor-specific method scope, the NA claims 23–30 method fallbacks not carried by AF claim 20, and support-safe software-medium alternatives; and
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
8. Do AF claim 1's whole-system-use theory and AF claim 20's performance/attribution theory fit the applicant's likely actors and available evidence under the fact-specific `Centillion`, `CloudofChange`, and `Akamai` frameworks?
9. Does AF claim 20 satisfy the same claim-as-a-whole support and priority gates as AF claim 1, and what § 101, restriction, search, and proof consequences follow from retaining it?
10. Should AF claim 20 be filed, omitted, or canceled to preserve one-independent-claim simplicity, and how will the actual filed topology be propagated through the AF package?
11. Which NA families—including broader or actor-specific methods and useful NA claims 23–30 fallbacks—must be preserved in a continuation, and which have sufficient commercial value to justify filing cost?
12. Which application will be the parent, who owns the continuation docket, what is the target filing event, and what evidence will establish copendency before issue?
13. Which route and Track One posture should be used, and what restriction/double-patenting consequences are expected?
14. Are the shared IDS and public PCT comments approved, supplemented, or held, and who owns continuing disclosure monitoring?

## 11. Authorities for counsel to confirm at action time

- [USPTO MPEP § 201.07 — continuation applications](https://www.uspto.gov/web/offices/pac/mpep/s201.html)
- [USPTO MPEP § 211.01(b) — copendency and benefit](https://www.uspto.gov/web/offices/pac/mpep/s211.html)
- [USPTO MPEP § 1893 — § 371 national stage](https://www.uspto.gov/web/offices/pac/mpep/s1893.html)
- [USPTO MPEP § 1895 — bypass applications](https://www.uspto.gov/web/offices/pac/mpep/s1895.html)
- [USPTO Track One program](https://www.uspto.gov/patents/initiatives/patent-application-initiatives/prioritized-patent-examination-program)
- [USPTO MPEP § 708.02(b) — Track One controls](https://www.uspto.gov/web/offices/pac/mpep/s708.html)
- [USPTO MPEP § 609 — IDS practice](https://www.uspto.gov/web/offices/pac/mpep/s609.html)
- [USPTO MPEP § 2001 — duty of disclosure, candor, and good faith](https://www.uspto.gov/web/offices/pac/mpep/s2001.html)
- [USPTO MPEP § 2106 — patent-subject-matter eligibility](https://www.uspto.gov/web/offices/pac/mpep/s2106.html)
- [USPTO MPEP § 2143 — obviousness rationales](https://www.uspto.gov/web/offices/pac/mpep/s2143.html)
- [USPTO MPEP § 802 — restriction practice](https://www.uspto.gov/web/offices/pac/mpep/s802.html)
- [Akamai Technologies, Inc. v. Limelight Networks, Inc. — method-step attribution (Fed. Cir. en banc 2015)](https://www.cafc.uscourts.gov/opinions-orders/9-1372.opinion.8-11-2015.1.pdf)
- [Centillion Data Systems, LLC v. Qwest Communications International, Inc. — use of a distributed claimed system (Fed. Cir. 2011)](https://www.cafc.uscourts.gov/opinions-orders/10-1110-1131.pdf)
- [CloudofChange, LLC v. NCR Corp. — system use and attribution limits (Fed. Cir. 2024)](https://www.cafc.uscourts.gov/opinions-orders/23-1111.OPINION.12-18-2024_2438003.pdf)

## 12. Revision record

- **AF-2026-07-17-v2 (17 July 2026):** added independent method AF claim 20 to the single AF proposal; stated the recorded deletion-at-filing option; separated method-step attribution from whole-system use; propagated the claim-as-a-whole, direct-art, priority, eligibility, restriction, proof, and continuation gates; and aligned the allowance thesis with the independents' exact structured-list and temporally-corresponding-different-camera-frame language.
