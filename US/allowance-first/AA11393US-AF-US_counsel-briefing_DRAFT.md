# AA11393US — AF Allowance-First US Counsel Briefing (DRAFT)

> **STRATEGY AF · CLAIM-SET VERSION AF-2026-07-22-v4 · STATUS 22 JULY 2026**
>
> **INTERNAL ATTORNEY BRIEFING — NOT FOR FILING.** “Allowance-first” is a proposed claim-selection strategy, not a prediction, promise, or legal conclusion. Use `AF claim N`, `NA claim N`, and `PCT claim N` outside claim text.
>
> **FAMILY TERMINOLOGY BOUNDARY.** AF and NA place physical-camera identifiers in their production-side limitations and use plural detected camera-cut time codes and reconstructed manifests for suspect recovery. AF integrates plural paired edit-entry changes into one system and method; NA preserves separate production, distribution, and detector actors. Neither strategy defines or construes the other.
>
> **INITIAL-CONTACT STATUS.** The package is ready for applicant-controlled initial transmission under DW-12. DW-05A's § 112/priority opinion and DW-08A's direct-art search remain pending pre-filing controls. No counsel opinion or filing choice is represented as obtained.

## 1. Decision requested

Determine whether the initial US case should pursue AF claim 1 as a concentrated system anchor and AF claim 19 as its method counterpart, while preserving actor-focused NA families through a timely continuation or other counsel-approved structure.

Counsel should decide:

1. whether AF claims 1 and 19 are each supported as complete claims and entitled to the asserted benefit date;
2. whether the plural-cut reconstructed-manifest architecture provides a defensible patentability position after DW-08A;
3. whether the enforcement and proof costs fit the applicant's expected actors;
4. whether AF claim 19 justifies a second independent after § 101, restriction, proof, and examination-focus review; and
5. who owns continuation preservation and what pre-issue gate controls it.

## 2. Allowance thesis

AF claims 1 and 19 require the following linked chain:

1. receive plural-camera video and a structured edit list containing, for plural director-commanded cuts, successive entries identifying different physical source cameras and paired out/in-point time codes;
2. at plural selected cuts, modify those paired time codes while retaining the camera identifiers and order, producing reference and mate transition timings;
3. segment the reference/mate ensemble, generate manifests pointing to respective chunk combinations, deliver according to those manifests, and associate each delivered manifest with its recipient in a ledger;
4. detect a plurality of camera-cut time codes in suspected content and build one or more reconstructed manifests from those time codes; and
5. identify the recipient associated with a delivered manifest equal to a reconstructed manifest.

Each output constrains a later operation. The structured list generates the reference and mates; the reference/mate ensemble supplies manifest-selected chunks; delivery populates the ledger; and plural detected cut times produce the reconstructed object used in the ledger search.

The reviewed art densely teaches manifest delivery, temporal variants, scene-change or timing analysis, manifest reconstruction, recipient records, and tracing. No reviewed document was identified disclosing the complete claimed conjunction with plural recorded boundary changes between retained identified physical cameras. That limited-search result is not a clearance or allowance prediction.

AF claim 19 provides a method-performance category, not a different technical novelty theory.

## 3. Exact topology

The controlling text is [`AA11393US-AF-US_claim-set_DRAFT.md`](AA11393US-AF-US_claim-set_DRAFT.md): **19 total claims / two independent claims / 17 singly dependent claims / no multiple-dependent claim**.

| AF claims | Added function | Role |
|---|---|---|
| 1 | Complete plural physical-camera boundary variation, manifest delivery/association, plural cut-time reconstruction, and recipient lookup system | Principal system candidate |
| 2–3 | Later-cut resynchronization and ten-frame implementation | Technical fallbacks subject to the Example 2 priority gate |
| 4–6 | EDL label, live direction, and respective single-cut mates | Concrete production fallbacks |
| 7–8 | Perceptual hashes and sliding-window fuzzy matching | Detection implementations; reviewed art is crowded |
| 9–10 | Adaptive CDN delivery, reference/mate mixing, and progressive manifest assignment | Delivery implementations |
| 11–12 | Manifest-sequence collusion attribution and segmented Tardos | Collusion fallbacks with relationship-specific support gates |
| 13–17 | Same-interval chunks, retained transition geometry, blockchain, unicast, and plural timing-choice records | Packaging and record fallbacks |
| 18 | Pre-segmentation overlay | Pipeline implementation |
| 19 | Complete method counterpart to AF claim 1 | Additional enforcement category |

No claim depends from AF claim 19. Counsel may omit or cancel AF claim 19 if a one-independent posture is selected, but the actual filed topology must be reflected throughout the AF package.

## 4. Art pressure and examiner-facing position

The leading references are:

- **A20, US 2012/0114309 A1:** unique EDL per consumer, time-code-defined content elements, product-signature motivation, recipient/version registry, and later cross-reference lookup;
- **B9, WO 2009/156973 A1:** key-derived actual switch points among transformed streams;
- **A4, US 10,834,158 B1:** camera-perspective alternatives, customized manifests, temporal alignment, recovered version sequences, and user/group resolution;
- **A6, US 2014/0325550 A1:** recipient temporal events, tailored manifests, detected-pattern comparison, and device/colluder identification;
- **A13, US 2023/0103449 A1:** manifest generation and regeneration from segment identifiers;
- **B6, CN 100583750 C / Microsoft family:** local timing variation, hash reacquisition, and contributor search; and
- **A5, B7, and B8:** shot, perceptual-hash, and distortion-tolerant timing comparison.

A20 is examiner-favorable motivation evidence and should not be characterized as teaching away. Its “random sizes” language is undefined, and a temporal interpretation is plausible because its elements are time-code-defined. Its drawings do not expressly disclose plural temporal movement of physical-camera selection boundaries. Figure 2 on drawing Sheet 2 contains the F/C/A/C exemplar; Figure 3 separately depicts A/B/C sources; `330` is a final-product reference numeral, not a figure number. Its express Example 1B recovery path is watermark cross-reference, not cut-time reconstructed-manifest equality.

The leading combination route is **A20 + B9 + A4/A6/A13**, with direct multicamera/vision-mixer/EDL art potentially supplying physical-camera edit entries. The examiner-facing distinction should remain the exact operational relationship:

- paired out/in-point changes at plural cuts;
- retention of identified physical-camera order;
- manifests representing combinations of reference/mate chunks produced by those changes;
- reconstruction from plural scene-change-derived cut time codes; and
- equal-manifest ledger lookup.

Do not rely on the labels `EDL`, `manifest`, `timing pattern`, `scene change`, or `reconstructed manifest` alone.

### KSR pre-mortem

MPEP § 2143 rationales based on combining known elements, applying a known technique, and predictable variation are facially plausible. A20 supplies a documentary reason to individualize an EDL for tracing. An “obvious to try” rationale still requires identified predictable options and a reasonable expectation of success; the existence of generic EDL fields does not itself establish that plural physical-camera cut boundaries were a known forensic code.

The response should require an evidence-backed path to every claimed relationship and should not rely on the number of references. Under [MPEP § 2143.03](https://www.uspto.gov/web/offices/pac/mpep/s2143.html), every limitation and relationship must be considered. Under [MPEP § 2144.03](https://www.uspto.gov/web/offices/pac/mpep/s2144.html), unsupported common knowledge or official notice should not supply the central missing relationship after an adequate specific traverse.

US counsel should preserve genuinely dated evidence concerning which edit parameters were recognized as per-recipient forensic variables, whether plural camera-boundary movement was predictable and operationally robust, and whether scene-change-derived cut sequences were used to reconstruct delivered manifests. Later testing may establish technical behavior but is not contemporaneous evidence of filing-date knowledge.

DW-08A should cover vision mixers, live and post-production EDLs, personalized alternate-angle edits, screener differentiation, plural switch-boundary fingerprints, and scene-change-derived manifest reconstruction.

## 5. § 112 and priority determinations

The provisional directly recites the basic complete loop in system claim 1 and method claim 10. In particular, provisional claim 1(m)–(n) and method claim 10(j)–(k) connect plural camera-cut time-code detection, reconstructed-manifest matching, ledger search, and account identification. PCT claim 15 and Method 200/claims 16–17 supply parallel direct recovery support.

### AF claims 1 and 19

The operative claim-as-a-whole question is whether each filing conveys the strengthened relationship among:

1. plural paired out/in-point modifications that retain physical-camera identifiers and order;
2. delivery of manifests representing reference/mate chunk combinations produced by those modifications; and
3. reconstruction of an equal delivered manifest from plural suspect cut time codes.

The overall loop and each operational stage are express. Example 2 supplies the physical-camera boundary; Examples 3–4 supply chunk/manifest combinations; and the filed recovery claims supply plural cut-time reconstruction and equality. Counsel must still decide the exact integration and generalized breadth as claims as a whole.

For each independent, counsel must separately conclude PCT written description, PCT enablement, provisional written description and enablement for benefit entitlement, effective date, and DW-05A Mode A, B, or C. Written description and enablement are separate inquiries; neither answer establishes the other.

### Specific dependent gates

- **AF claims 2–3:** provisional Example 2 contains a stray `00:00:30:11` “mistake” sentence despite the table and surrounding restoration explanation using `00:00:30:01`. PCT Example 2 uses `00:00:30:01`. Obtain a written priority/support determination.
- **AF claim 6:** confirm the respective-mate/only-one-selected-cut relationship.
- **AF claims 11–12:** confirm recipient-associated manifest chunk-selection sequences as the probabilistic input and the exact segmented-fingerprint/portion-to-contributor relationship. No AF attribution-score limitation is asserted.
- **AF claim 14:** confirm that each paired same-interval chunk contains the retained transition at its respective timing.
- **AF claim 17:** confirm the plural reference/mate timing-choice combination represented by each delivered manifest.
- **AF claim 18:** confirm overlay before segmentation in both asserted support sources.

B10's 2 December 2024 publication is potentially citable principally in Mode B. It is too late by publication date in Mode A; in Mode C the PCT current-disclosure defect independently controls. B10 remains low-materiality on the current substantive mapping.

If counsel rejects the integrated support position, the operative alternatives are the actor-focused NA families or a directly disclosed detector-side claim using suspect acquisition, plural cut-time derivation, reconstructed-manifest building, ledger search, and recipient identification. Either choice requires its own actor, § 101, art, count, dependency, and continuation analysis.

## 6. Enforcement and evidence trade

AF claims 1 and 19 trade actor-specific breadth for a concentrated chain.

### AF claim 1 — whole-system use

Counsel should analyze whether a target makes, sells, offers, or uses the claimed system as a whole. Under the fact-specific `Centillion` framework, a party may use a distributed system by putting the whole system into service, controlling that use, and obtaining its benefit. `CloudofChange` confirms that supplying or hosting part of a system does not necessarily make the vendor the user when customers initiate and benefit from the whole-system operation.

### AF claim 19 — method performance and attribution

Direct method infringement ordinarily requires every step to be performed by one entity or attributable to one entity. Under `Akamai`, attribution may arise through agency, contract, joint enterprise, or direction/control, including conditioning participation or a benefit on performance while establishing the manner or timing. A commercial relationship or platform alone is insufficient.

Do not transpose the tests: method-step attribution does not itself establish whole-system use, and system use does not dispense with proof of every method step.

Proof may require:

- structured edit entries with physical source-camera identifiers and paired out/in-point time codes;
- reference and mate versions showing plural retained-camera boundary changes;
- chunk and manifest generation records;
- delivery and manifest-recipient ledger records;
- suspect-side scene-change output identifying plural cut time codes;
- reconstructed manifests and equality comparison; and
- the ledger result identifying the recipient.

AF claim 19 additionally requires evidence identifying the performer of each step and any attribution facts. The crosswalk identifies NA actor-focused coverage outside AF.

## 7. Procedure and claim-count controls

`AF-2026-07-22-v4` contains 19 total claims, two independent claims, 17 singly dependent claims, and no multiple-dependent claim. It is within the current Track One ceiling of four independent claims, 30 total claims, and no multiple-dependent claim and remains within the basic 20-total/three-independent allocation. This does not establish Track One eligibility or strategic merit.

Track One is available for qualifying original nonprovisional applications under § 111(a), including qualifying continuing applications; it is not available merely by requesting it in a direct § 371 national-stage application. Counsel must decide the route, filing format, benefit claim, declarations, inventorship, applicant, assignment, entity status, fees, restriction, unity, double patenting, and terminal-disclaimer posture.

AF claim 19 may be omitted only through a recorded strategy decision reflected in the filed claim listing and all claim-indexed AF records. Any other amendment, cancellation, renumbering, or claim-status change requires count, dependency, antecedent, support, matrix, crosswalk, and filed-topology review.

## 8. Continuation preservation

If AF is selected, the continuation docket should preserve commercially valuable supported scope before the parent issues. The controlling workflow is [`AA11393US-AF-continuation-preservation_MEMO.md`](AA11393US-AF-continuation-preservation_MEMO.md).

Current reservation families are:

1. standalone NA production coverage;
2. standalone NA distribution and recipient-association coverage;
3. standalone NA reconstructed-manifest detection and recipient-resolution coverage;
4. broader or actor-specific methods and useful NA claims 23–30 fallbacks;
5. additional supported detector-side implementations if commercially justified; and
6. supported software-medium coverage if commercially justified.

For each generation in which valuable scope remains deferred, file and verify a qualifying successor while a parent remains pending or record `CHAIN CLOSED — DEFERRED SCOPE NOT PRESERVED`. Continuation practice cannot cure missing disclosure or a broken benefit chain.

## 9. Shared disclosure and consistency

Use only the canonical shared [`IDS inventory`](../common/AA11393US-US_IDS-reference-list_DRAFT.md), [`PCT informal-comments draft`](../common/AA11393US-PCT_informal-comments-IB_DRAFT.md), and [`filing/disclosure controls`](../common/AA11393US-deferred-filing-disclosure-and-EP-work_MEMO.md). The IDS inventory is not an admission that every item is prior art or material. Counsel must coordinate disclosure and public positions across the parent and every continuation.

## 10. Pending written recommendations

1. Are AF claims 1 and 19 adequately supported as complete plural-cut reconstructed-manifest chains, and which DW-05A mode applies to each?
2. Does DW-08A support the allowance thesis, and how should A20+B9+A4/A6/A13 be answered?
3. Are AF claims 2–3 entitled to the provisional date?
4. Are the generalization across plural selected physical-camera cuts and the paired out/in-point formulation supported?
5. Are AF claims 6, 11–12, 14, and 17–18 supportable as drafted?
6. Do the whole-system and method-performance theories fit likely actors and obtainable evidence?
7. Should AF claim 19 be filed, omitted, or canceled?
8. Which NA and detector-side families warrant continuation cost, and who owns the docket?
9. Which route and Track One posture should be used, and what restriction/double-patenting consequences are expected?
10. What IDS, PCT-comment, and continuing disclosure actions are approved?

## 11. Authorities for counsel to confirm at action time

- [MPEP § 201.07 — continuation applications](https://www.uspto.gov/web/offices/pac/mpep/s201.html)
- [MPEP § 211.01(b) — copendency and benefit](https://www.uspto.gov/web/offices/pac/mpep/s211.html)
- [MPEP § 1893 — § 371 national stage](https://www.uspto.gov/web/offices/pac/mpep/s1893.html)
- [MPEP § 1895 — bypass applications](https://www.uspto.gov/web/offices/pac/mpep/s1895.html)
- [USPTO Track One program](https://www.uspto.gov/patents/initiatives/usptos-prioritized-patent-examination-program)
- [MPEP § 708.02(b) — Track One](https://www.uspto.gov/web/offices/pac/mpep/s708.html)
- [MPEP § 609 — IDS practice](https://www.uspto.gov/web/offices/pac/mpep/s609.html)
- [MPEP § 2001 — disclosure and candor](https://www.uspto.gov/web/offices/pac/mpep/s2001.html)
- [MPEP § 2106 — eligibility](https://www.uspto.gov/web/offices/pac/mpep/s2106.html)
- [MPEP § 2163 — written description](https://www.uspto.gov/web/offices/pac/mpep/s2163.html)
- [MPEP § 2164 — enablement](https://www.uspto.gov/web/offices/pac/mpep/s2164.html)
- [MPEP § 2143 — obviousness rationales](https://www.uspto.gov/web/offices/pac/mpep/s2143.html)
- [MPEP § 2144.03 — common knowledge and official notice](https://www.uspto.gov/web/offices/pac/mpep/s2144.html)
- [MPEP § 802 — restriction](https://www.uspto.gov/web/offices/pac/mpep/s802.html)
- [Akamai v. Limelight — method-step attribution](https://www.cafc.uscourts.gov/opinions-orders/9-1372.opinion.8-11-2015.1.pdf)
- [Centillion v. Qwest — use of a distributed system](https://www.cafc.uscourts.gov/opinions-orders/10-1110-1131.pdf)
- [CloudofChange v. NCR — system-use limits](https://www.cafc.uscourts.gov/opinions-orders/23-1111.OPINION.12-18-2024_2438003.pdf)
