# AA11393US — NA Balanced Actor-Split Counsel Briefing (DRAFT)

> **STRATEGY NA · CLAIM-SET VERSION NA-2026-07-21-v2 · STATUS 21 JULY 2026**
>
> **INTERNAL ATTORNEY BRIEFING — NOT FOR FILING.** Use `NA claim N` outside the claim text.

## 1. Requested outcome

Prepare and file a US application that protects the commercially meaningful multi-camera content-differentiation mechanism, preserves the benefit of provisional 63/557,868 where supported, presents claims enforceable against the principal commercial actors, and remains eligible for Track One if the applicant chooses a §111(a) bypass continuation.

The international Written Opinion found PCT claims 1–18 novel and industrially applicable but not inventive over D1, US 2021/0352381 A1, principally because the examiner treated the multiple-camera features as known and lacking technical synergy with the rest of the system. The proposed response is to claim and explain the closed technical loop more precisely.

## 2. Invention statement to use throughout prosecution

> A multi-camera production system records an ordered camera-source transition in a structured edit list, produces a mate in which that same ordered transition occurs at a different switch timing and the intervening interval contains temporally corresponding frames from another camera, preserves one of those transition positions through manifest/chunk selection and recipient association, and later derives and matches both the ordered source transition and its switch timing from suspected content.

The strongest concrete example extends one camera shot by ten frames, correspondingly delays the next camera shot, and restores the reference timing at a later cut. This is more defensible than a generic statement that a time code changes “relative to another cut,” because D1 also discloses frame-rate transformation.

Use the pattern terminology deliberately:

- a **camera-cut timing pattern** is the sequence or arrangement of camera-switch times produced in a version and, where applicable, represented by chunks or manifests for distribution; under NA claims 9 and 22 it identifies the relevant first and second camera sources and the switch timing preserved in the delivered version, rather than an arbitrary fragment-version sequence; and
- a **camera-source-transition pattern** is the detection-side structure identifying ordered camera-source transitions together with their corresponding camera-switch timings for operational comparison.

The terms perform different claim functions rather than defining a strict information-content hierarchy. In NA claims 9 and 22, a camera-cut timing pattern records the identified source pair and the switch timing contained in a delivered version. In NA claim 16, candidate and detected camera-source-transition patterns organize ordered source transitions and corresponding timings at candidate-distinguishing regions for operational derivation and matching. NA claim 1 recites its ordered-transition and noncoincident-timing output relationship directly rather than through either pattern term. NA claims 9 and 22 therefore do not rely on timing alone, and NA claim 16 does not rely merely on a label applied to generic timing data. Do not collapse the terms into synonyms without reviewing written-description support, prior art, and claim scope.

## 3. Commercial actor and enforcement map

| Commercial function | Likely actor | Candidate independent claim | Evidence likely available |
|---|---|---|---|
| Creates reference edit and mates | host broadcaster, outside-broadcast facility, production-software vendor | NA claim 1 | production configuration, EDLs, output comparisons, software documentation |
| Builds manifests, distributes streams, records recipient mapping | rights-holding licensee, streaming platform, origin/CDN operator | NA claim 9 | captured delivered streams, synchronized content comparisons, manifests, source-version/chunk mappings, network traffic, account records, platform documentation |
| Detects pirate stream and resolves source | rights owner, anti-piracy monitoring provider, platform trust/safety system | NA claim 16 | monitoring output, comparison logs, ledger queries, software behavior |
| Operates entire lifecycle | vertically integrated broadcaster/platform | NA claim 22 | combined operational evidence |

The subsystem claims are not merely drafting convenience. They reduce dependence on proving that one entity controls or performs production, distribution, and later detection. They do not eliminate the need for a fact-specific direct-infringement or attribution analysis. The end-to-end claim remains valuable for the full-combination patentability position and integrated deployments.

The structural strengthening of NA claim 9 trades evidentiary simplicity for a stronger patentability and validity position. The former timing-pattern formulation could be investigated principally from manifest and account mechanics; the revised claim will ordinarily require synchronized comparison of delivered streams, or discovery into source-version and chunk mappings, to prove the same ordered camera-source transition at noncoincident timings and different-camera frames in the intervening interval. Those content facts may be observable from controlled captures and may be confirmed through discovery, but counsel should evaluate practical access, preservation, reverse-engineering, and proof before treating the rewrite as a pure enforcement gain.

## 4. Recommended claim portfolio

Use the 30/4 candidate set as the starting Track One portfolio:

1. production/mate-generation system;
2. distribution/recipient-association system;
3. detection/recipient-resolution system; and
4. end-to-end method.

The set is exactly at the Track One ceiling and has **no net claim-count headroom**. A later amendment may add a claim only if the application remains at no more than 30 total claims and four independent claims and contains no multiple-dependent claim, such as through a coordinated cancellation. An amendment that results in exceeding those limits terminates prioritized examination. Counsel should manage amendments and any restriction response accordingly.

If fees or restriction risk require fewer claims, preserve the three subsystem independents first and evaluate whether the end-to-end method or a subsystem-specific computer-readable-medium claim has greater commercial value. Do not default to an end-to-end CRM claim.

Maintain the following fallback order:

1. structured edit list with source-camera/time-code entries;
2. the observable same ordered first-camera-to-second-camera transition at noncoincident reference/mate switch timings, with temporally corresponding different-camera frames in the intervening interval (NA claim 1);
3. retention, in the varied structured list, of the first/second camera identifiers on the respective sides while the recorded transition time code changes (NA claim 7);
4. later cut retains the reference timing or restores synchronization (NA claims 2–3);
5. different manifests select corresponding equal-duration reference and mate chunks spanning the same playback interval, each chunk itself containing the same ordered physical-camera transition at its respective noncoincident timing (NA claim 13), with NA claims 9 and 29 carrying manifest preservation of the selected transition position in the distribution and end-to-end families;
6. recipient ledger;
7. detection and matching, at the same candidate-distinguishing region, of both the ordered camera-source transition and its switch timing;
8. detected time code and reconstructed manifest;
9. perceptual hash/sliding-window matching; and
10. positive probabilistic collusion attribution, including attribution scores in NA claim 21.

The former broader production theory—local alternate-camera substitution without requiring the same ordered camera pair at two timings—should be reserved for a coordinated continuation or other counsel-approved claim strategy. It should not be used to characterize or argue the scope of present NA claim 1.

## 5. D1 position

Counsel should avoid the earlier categorical descriptions of D1.

D1 does disclose:

- a completed base copy that is replicated and transformed;
- watermark-like arbitrary identifiers in addition to watermarks;
- transformations selected by ID and/or randomly or pseudo-randomly;
- segmentwise transformations;
- uniform delay and frame-rate variation; and
- use of scene changes to mask transitions between transformations.

The proposed D1-alone distinction is that the reviewed disclosure was not identified as supplying the complete route of synchronized alternate-camera source material → recorded camera-selection boundary → local source-camera substitution → recipient-associated boundary pattern → recovery of that pattern from suspected content. Do not generalize that D1-alone observation into an assertion that the combined art supplies no motivation. A20 supplies documentary motivation to individualize an EDL-controlled final product for identification and license-enforcement tracing, and counsel should assess §103 combinations with conventional multi-camera production, EDL, personalization, and forensic-identification art.

Do not argue that random variants cannot identify a recipient. Argue that D1 does not disclose the claimed association and recovery loop for camera-boundary patterns. Do not argue that D1 preserves alignment. Argue that its misalignment transformations act on the completed edit and do not rewrite its camera-source selection using alternate synchronized footage.

## 6. Supplemental prior art and expected novelty center

The limited supplemental review found prior art for:

- file-segment variations and traitor tracing;
- recipient/device assignments for different content versions;
- identifiers encoded through customized manifest fragment patterns;
- shot detection and perceptual image hashing;
- piracy detection by comparison of shot sequences; and
- identification of video through timing patterns.

Accordingly, avoid treating any of those concepts in isolation as the invention. The expected novelty/nonobviousness center is their specific connection to deliberately moved multi-camera edit boundaries, preferably with a locally changed boundary and later resynchronization.

The full-text review materially sharpened five references:

- **A4, US 10,834,158 B1**, is a principal camera-perspective/distribution/detection reference. It discloses camera-perspective fragment alternatives, customized manifests encoding ordered or differential version patterns, temporal alignment of an unauthorized copy, recovery of its version sequence, comparison with stored manifests, and probabilistic user/group identification. A4 does not expressly disclose an EDL or movement of a recorded director cut, and a perspective change does not necessarily create a camera cut. It nevertheless creates serious broad-construction and §103 pressure on NA claims 1, 9, 16, and 22.
- **A6, US 2014/0325550 A1**, discloses recipient-specific temporal events, device/transaction-derived timing, unique manifest/segment sequences, variable-duration segments, detection of variations in a pirate stream, comparison with stored device-associated lists, and user identification. The present limited review identified in A6 many of the non-camera distribution, association, detection, and resolution elements; counsel should confirm their precise scope and role in any claim-specific combination.
- **B6, CN 100583750 C and its Microsoft family**, teaches recipient-specific local frame-count/timing changes and hash-based reacquisition from an illegal copy despite insertion, deletion, rearrangement, advertising, and timing attacks. Subject to authoritative English-family review and counsel's determinations of applicable prior-art status and analogous-art scope, B6 presents substantial pressure against positions relying only on timing variation, relative timing, or hash reacquisition; no synchronized alternate-camera/EDL boundary mechanism was identified in the present review.
- **B9, WO 2009/156973 A1**, does not use only a fixed time grid. It analyzes shot cuts and motion to identify probable switch points, combines them with a key-derived/random sequence to select practical exchange points, switches streams at those points, and states that users' copies differ through different exchangeable switch times. Its streams are desynchronized transformations of the same content rather than temporally corresponding physical-camera views; no EDL, moved recorded director cut, or claimed recovery loop was identified in the reviewed disclosure.
- **A20, US 2012/0114309 A1**, is examiner-favorable on the motivation limb. It discloses a unique EDL for each consumer, expressly motivated by identification and control of each version, and Example 1B uses a consumer/version registry and later cross-reference lookup for license-enforcement tracing. Its background describes generic EDL events using source identifiers, time-code-defined content elements, transitions including cuts, and transition durations. Its individualized-EDL embodiment lists “random sizes” for content elements as a way to create a “product signature.” “Sizes” is undefined; because A20 also describes time-code-defined content elements, a temporal interpretation is plausible, but A20 does not expressly say to vary element duration, camera-cut timing, or a boundary between identified synchronized cameras. The selected/front-page `F/C/A/C` bracketed time-range exemplar reproduces **Figure 2** on drawing Sheet 2 of 33. `330` is a final-product reference numeral, not a figure number. **Figure 3** is a separate multiple-source `A/B/C` drawing that also uses reference numeral `330`. The bracketed exemplar must be cited to the selected/front-page drawing or Figure 2 on Sheet 2, not as “Fig. 330” or as transcribed specification prose. “Product signature” supports motivation to make copies distinguishable, but it does not disclose a structural detector that recovers an ordered camera-source pair jointly with timing at the same region. Example 1B's express recovery path analyzes and cross-references a unique watermark.

The most plausible combination pressure is therefore claim-specific:

- for NA claim 1 as a whole, A20 combined with conventional multi-camera/vision-mixer/EDL practice and B9 or B6, and potentially A4's camera-perspective alternatives; for NA claim 7's added internal-record delta, A20 supplies individualized-EDL motivation and generic source/time/transition fields but not retention of an identified physical-camera pair around a changed camera-transition time;
- for NA claims 9, 13, and 15, A4 or A6, potentially with A20's forensic individualization and registry teaching, combined with B9 and ordinary multi-camera editing;
- for NA claim 16, A4 or A6 combined with the shot/hash-detection teachings identified in A5 or B7 and, where useful, B6 or B8; and
- for NA claim 22, A20 and conventional multi-camera EDL production combined with A4, A6, B9, and an articulated recovery path.

### Claim-specific KSR pre-mortem

Counsel should prepare for MPEP § 2143 rationales A, D, and F. An examiner may characterize the proposal as a combination of familiar elements yielding predictable results; application of the known per-recipient EDL-individualization technique to a multicamera editing system ready for improved traceability; or a predictable EDL variation prompted by A20's express design incentive. Those routes are plausible, not established. A20 makes the general motivation limb documentary, so the response should concede that motivation and require an evidence-backed account of why a skilled person would select and implement the exact claimed relationship, rather than generic timing variation or an unspecified EDL parameter, and why the proposed combination would have had a reasonable expectation of producing it.

Rationale E is conditional rather than automatic. “Obvious to try” requires a finite number of **identified, predictable** solutions and a reasonable expectation of success. Counsel should not concede that the existence of a finite number of generic EDL field types by itself identifies movement of a recorded transition between synchronized camera sources as a known forensic option.

A separate patent reference is not invariably required for every implementation detail: common knowledge or a predictable consequence may contribute to an articulated obviousness rationale when properly supported. Under current [MPEP § 2144.03](https://www.uspto.gov/web/offices/pac/mpep/s2144.html), however, unsupported official notice or common knowledge must be used judiciously, may fill only an insubstantial gap, and cannot be the principal evidence for a central missing claim relationship. If counsel contests such a factual assertion, the traverse should be specific—explaining why the asserted fact is not well known or indisputable, rather than merely requesting a citation—and an adequate traverse requires the examiner to provide documentary support if the rejection is maintained. This control does not require documentary evidence for every inference in an otherwise evidence-backed KSR analysis.

Under current [MPEP § 2143.03](https://www.uspto.gov/web/offices/pac/mpep/s2143.html), every limiting word and claimed relationship must be considered. Apply that rule claim by claim:

- **NA claims 1 and 7 are production claims, and NA claim 9 is a distribution claim.** They do not recite suspect-side detection. Their defense must rest on their own recited output, structured-list, delivery, and association relationships—including, as applicable, the same ordered physical-camera transition at noncoincident timings and temporally corresponding different-camera frames—not on structural recovery, joint detector matching, or the shortcomings of mark-based detection.
- **NA claim 16 and the full-chain NA claim 22** positively recite same-region source-pair-plus-timing detection or recovery relationships. A rejection of those claims must account for those operations as well as generation, delivery, and association. Do not overstate that point by asserting that all reviewed detection art is embedded-mark based: A4 includes camera-perspective/version-pattern recovery, A6 includes forced or natural event-pattern recovery, and B7 supplies shot/cut comparison. The narrower question is whether the articulated combination supplies the claimed joint source identities, timing, and same-region relationship.

Against the production and distribution combinations, preserve resulting structure rather than product-by-process implication. Against the detector and full-chain combinations, additionally preserve recovery and matching of source order plus timing at the distinguishing region. On the present limited record, variable switch timing, manifests, temporal fingerprints, or recipient lookup should not be relied upon alone as the patentability distinction absent contrary claim-specific search and legal analysis.

US counsel should own evidence development with the inventor or technical lead and, as appropriate, a search or test professional. They should promptly preserve genuinely dated materials and identify witnesses concerning: (1) which EDL parameters were actually recognized as per-recipient forensic variables; (2) whether moving the claimed synchronized-camera boundary would predictably preserve program continuity and create the claimed alternate-camera interval; (3) for NA claims 16 and 22, whether the art taught a workable route to recover both source identities and timing at the same region; and (4) any unexpected technical result tied to the claimed relationship. Counsel should complete the historical-evidence review before approving final claims. Later testing may show technical behavior, but a memorandum created in 2026 is not itself contemporaneous evidence of what a person of ordinary skill knew at the relevant time; formal testing or a declaration should be prepared only if counsel decides it is warranted. Do not characterize silence, use of another technique, or a portfolio's failure to select this technique as teaching away or failure of others. Any objective-indicia position should be supported by evidence of a recognized persistent need, documented unsuccessful attempts or skepticism, satisfaction of that need, and a nexus to the claimed relationship.

EP 2 811 416 A1 supplies part of the same motivation narrative by using a temporal pattern for identification in view of removable visual watermarks. Describe that disclosure precisely; do not say that B8 “anticipates the motivation.” Its grant, withdrawal, or national legal status does not alter the disclosure date of the published A1 document, although its EPO file history may reveal useful examination reasoning or additional cited art.

The detection independent requires particular attention. NA claim 16 now ties the stored inter-version difference, detection, and matching to the same candidate-distinguishing temporal region; requires the candidates to contain the same ordered first-camera-to-second-camera transition at different timings and different-camera frames in the intervening interval; and requires the match to agree in both source order and timing. Preserve that complete relationship. Counsel should confirm written-description support for each operation and avoid relying only on a statement that generic data were “produced by” the mate-generation process.

The attached prior-art matrix and IDS inventory identify the candidate documents. Before broadening the revised claims, commission a focused search directed to vision mixers, live-production EDLs, multi-camera or alternate-angle personalization, individualized screener edits, and systems that vary or record camera-selection boundaries. The present review found no direct reference with the complete mechanism, but it was limited and is not a clearance search.

## 7. Priority and written-description position

The provisional contains the core multi-camera, EDL, local ten-frame variation, manifest, ledger, detection, perceptual-hash/fuzzy-match, Tardos, overlay, and analytics passages. The revised structural language nevertheless combines relationships drawn from different examples: NA claims 1, 7, 9, 13, 15, 16, 22, and 29 require claim-as-a-whole review rather than a conclusion based on isolated nouns or operations. NA claim 1's generalized output relationship and NA claim 7's added structured-list identifier-retention delta should be reviewed separately. The provisional also contains support for later-cut alignment, but that support has an internal drafting inconsistency requiring express analysis. At provisional PDF p. 27 (printed p. 16), the mate EDL table places Cut 4 at `00:00:30:01` and labels it adjusted to the reference. The accompanying paragraph contains the `00:00:30:11` value, immediately characterizes that value in the provisional text as “a mistake in the alignment attempt,” and expressly states that the correct approach is `00:00:30:01`, matching the reference with no delay. The PCT Example 2 uses the corrected alignment. This is favorable evidence of the intended teaching, but it does not replace a claim-as-a-whole priority opinion or justify an unqualified support rating.

Use the attached provisional/PCT map to confirm:

- entitlement of each material limitation to 26 February 2024;
- PCT support for every bypass or preliminary-amendment limitation;
- whether proposed terminology is a fair expression of the disclosed examples;
- whether the Example 2 correction would be understood by a skilled reader as possession of later-cut resynchronization and the PCT wording is a permissible clarification rather than new matter; and
- whether any post-PCT improvement requires a separate continuation-in-part analysis.

Keep the Example 2 inconsistency in the internal priority analysis. Do not add it to the public WIPO informal comments unless counsel concludes that a public statement is strategically necessary.

### Intervening-information trigger

The limited review recorded in this package has identified one recorded intervening-window exception: B10 (KR 2024-0168593 A), whose only identified prior-art route is §102(a)(1) as of its 2 December 2024 laid-open publication. B10 is prior art only against claims whose provisional entitlement fails and is assessed LOW-materiality on the present full-text review because it does not disclose cameras, an edit list, or the claimed timing or structural relationships. The intervening-information trigger was activated and recorded on 21 July 2026; no claim-position change is presently indicated. This is not a clearance opinion and must not be treated as proof that no other potentially material information exists.

Reopen the priority and disclosure analysis promptly if:

- a patent document, publication, public-use or sale allegation, or other potentially material information is identified with an effective prior-art date in that interval;
- a US, PCT, EP, Italian, or other Office questions entitlement to the provisional date;
- a search report or counterpart proceeding takes a position that makes the effective filing date material; or
- the applicant proposes relying on the provisional date to overcome a reference or other patentability position.

At that point counsel should reassess, claim by claim, provisional support, the Example 2 inconsistency, applicable disclosure obligations including 37 CFR 1.56, and every representation concerning the effective filing date. This is an internal monitoring instruction, not a conclusion that the priority issue or an internal legal assessment must presently be volunteered in the WIPO informal comments.

## 8. §101 and §112 directions

For eligibility, characterize the invention as concrete processing of multi-camera source frames, edit instructions, adaptive-stream manifests, and detected shot boundaries to improve how streaming variants are generated and forensically resolved. Do not rely on the business objective of identifying a recipient and do not describe the claims as “§101-safe.”

For §112:

- prefer processor-and-instruction formulations over unsupported “component” structure;
- state in NA claim 9 that processors, rather than servers as such, execute the stored instructions;
- retain concrete algorithms where helpful, while recognizing that the reviewed A5, B6, and B7 materials contain perceptual-hashing and/or shot-detection teachings; do not assume those techniques independently distinguish the claims;
- confirm corresponding algorithm disclosure if §112(f) is invoked;
- ensure that “camera-selection boundary,” local substitution, and resynchronization remain within the language and teaching of the filed documents;
- confirm NA claim 1's output-level same ordered first-camera-to-second-camera transition at noncoincident timings and intervening temporally corresponding different-camera frames as a supported expression of Example 2 rather than an unsupported general rule;
- separately confirm NA claim 7's retention of the first/second camera identifiers in the varied structured list while the recorded transition time code changes;
- confirm that NA claims 9, 13, 15, and 29 support-safely connect PCT Example 2's moved source boundary to PCT Examples 3–4's manifest and mixing disclosures and that the corresponding provisional passages support the same relationship, including NA claim 13's different manifests, corresponding equal-duration reference/mate chunks spanning the same playback interval, and placement of the ordered transition within each chunk at the respective switch timing;
- preserve NA claim 16's functional relationship between the stored candidate distinction, detection, and matching at the same region, including identification of the sources on both sides and agreement in both source order and timing;
- preserve NA claim 22's closed loop from the moved ordered transition through recipient association to structural transition-and-timing recovery;
- draft collusion NA claims 21 and 28 as affirmative limitations requiring mixed-version suspected content and performance of probabilistic attribution, rather than optional “when” clauses; NA claim 21 additionally requires candidate contributions, respective attribution scores, and identification based on those scores, whose support counsel must confirm;
- preserve the distinct claim functions of camera-cut timing patterns and camera-source-transition patterns; and
- confirm that NA claims 17 and 18 may recite detection of both camera-source transitions and their corresponding timings, while keeping NA claim 19 timing-specific because reconstructed manifests are built from derived time codes.

## 9. Procedural choice

### §111(a) bypass

Advantages to evaluate:

- Track One eligibility;
- original US claim set can use the actor-focused architecture;
- conventional US restriction practice may permit later divisionals, subject to cost.

Points requiring attention:

- correct continuation/benefit statement to the PCT and provisional chain;
- certified-copy/priority-document requirements;
- conventional IDS treatment for all references;
- exact identity of the specification and drawings filed;
- no new matter unless deliberately filed as a continuation-in-part;
- a compliant inventor oath/declaration or permitted delayed/substitute handling; and
- confirmation and recordation, where appropriate, of the assignment chain from the inventors through the applicant and any current owner.

### §371 national stage

Advantages to evaluate:

- direct national-stage treatment and international filing date;
- unity-of-invention rather than ordinary restriction practice;
- possible automatic consideration of properly transmitted ISR references.

Points requiring attention:

- Track One unavailable for direct §371 entry;
- preliminary amendment must comply with 37 CFR 1.121;
- national-stage formalities and translation/priority-document record;
- compliant inventor oath/declaration handling; and
- confirmation and recordation, where appropriate, of the assignment chain and current applicant/owner identity.

The README contains the operative date summary. The route should be selected promptly enough to permit attorney-quality preparation rather than on filing day.

## 10. Public informal comments

The revised WIPO comments preserve the synergy and architecture argument while correcting the D1 inaccuracies and technical overstatements. Before filing, PRAXI and US/EP counsel should confirm:

- official D1 quotations and paragraph numbering;
- consistency with final US and EP amendments;
- no unintended negative watermark limitation;
- no assertion that every cut shift is inherently imperceptible;
- no assertion that all collusion composites necessarily resolve to one recipient; and
- removal of all internal notes.

The comments are explanatory only and do not amend the application.

Because the intervening-information trigger in section 7 has been activated for B10, counsel should reconsider the disclosure and argument strategy before filing or supplementing the comments, and should repeat that review if additional information activates the trigger. Activation of the trigger does not by itself require insertion of the internal Example 2 analysis into the public comments.

## 11. IDS instructions

Review the supplemental candidates, complete official bibliographic/copy/translation handling, obtain the Italian search report, and file the counsel-approved disclosure package under the procedure applicable to the selected route. The deferred tasks, suggested owners, triggers, and completion evidence are collected in [`../common/AA11393US-deferred-filing-disclosure-and-EP-work_MEMO.md`](../common/AA11393US-deferred-filing-disclosure-and-EP-work_MEMO.md). In particular:

- preserve the completed Espacenet/CNIPA record check for CN 100583750 C and complete the authoritative English-family and foreign-language handling before relying on fine-grained B6 wording;
- inspect the EP 2 811 416 A1 family and EPO file history, without treating current legal status as controlling its prior-art disclosure;
- confirm the stored patent working copies against official registers, complete B6's authoritative English-family/foreign-language handling, obtain Lin 2008 (C7) — Tardos 2003 (C3) was stored 20.07.2026 in its author-hosted extended form — and decide publication/grant-pair and supplemental-reference treatment; and
- route every citation from the Italian search report into the IDS review promptly upon receipt.

Treat the list as an inventory, not as a statement that every item is prior art or material.

## 12. Questions requiring counsel's written recommendation

1. §371 or bypass, and why?
2. Track One requested or not?
3. Which four independent claims best match the applicant's expected licensing and enforcement targets?
4. Is NA claim 1's same ordered first-camera-to-second-camera transition at noncoincident reference/mate timings, including the intervening temporally corresponding different-camera frames, support-safe and sufficiently definite?
5. In view of the provisional Example 2 inconsistency, is later resynchronization entitled to the provisional date, and should it remain dependent or also appear in parallel independent scope?
6. Does the 30/4 set create unacceptable restriction risk, how should its zero net claim-count headroom be managed, and what divisional strategy is recommended?
7. Which supplemental references should be submitted, and is a further search required before filing?
8. Does every selected claim receive the provisional date?
9. Which terms risk §112(f), and what restructuring is recommended?
10. Should overlay, probabilistic/Tardos, reconstructed-manifest, and CRM claims be retained or reserved for a continuation; should the former broader production theory also be reserved there; and do structural NA claims 7, 13, and 29 provide the preferred use of the replaced dependent-claim slots?
11. Is any “without pixel-domain embedding” dependent claim worth the scope cost, or should that remain only an explanatory advantage?
12. Are the WIPO informal comments approved for filing and aligned with the intended EP response?
13. Does candidate NA claim 16 support-safely tie the stored candidate difference, detection, and matching to the same candidate-distinguishing region and require agreement in both ordered camera-source transition and switch timing, or should it be restructured further?
14. Are the inventor declaration, applicant identity, assignment chain, and recordation record complete for the selected route?
15. Who will monitor the provisional-to-PCT interval for potentially material intervening information, and what event will trigger a renewed priority, IDS, and representation review?
16. Is the deliberate functional distinction between “camera-cut timing pattern” and “camera-source-transition pattern” support-safe and appropriately reflected in NA claims 9/15/16/22 and harmonized NA claims 17–18, with NA claim 1 reciting its corresponding output relationship directly?
17. Are NA claims 1, 7, 9, 13, 15, 22, and 29 supported as integrated operations, with a separate analysis of claim 1's same ordered transition at noncoincident positions, claim 7's structured-list identifier/time-code delta, and the manifest/chunk preservation limitations?
18. What focused direct-art search has been completed for vision-mixer/EDL/multi-camera boundary personalization; how should counsel answer the A20-led rationales A/D/F and any properly supported rationale E; and do the results permit any deletion of the structural limitations adopted over A4, A6, B6, B9, and A20?

## 13. Current procedural authorities to confirm

These links identify the current official materials used to prepare the internal directions; counsel should confirm the rules and fees in force on the filing date.

- [WIPO practical guidance on informal comments](https://www.wipo.int/en/web/pct-system/newslett/practical_advice/pa_012015)
- [WIPO PCT inventive-step guidelines, chapter 13](https://www.wipo.int/en/web/pct-system/texts/ispe/13_03_13)
- [USPTO MPEP §1893 — §371 national stage](https://www.uspto.gov/web/offices/pac/mpep/s1893.html)
- [USPTO MPEP §1895 — bypass applications](https://www.uspto.gov/web/offices/pac/mpep/s1895.html)
- [USPTO MPEP §1896 — comparison of §111(a) and §371](https://www.uspto.gov/web/offices/pac/mpep/s1896.html)
- [USPTO Track One program](https://www.uspto.gov/patents/initiatives/patent-application-initiatives/prioritized-patent-examination-program)
- [USPTO MPEP §708.02(b) — Track One claim limits and termination](https://www.uspto.gov/web/offices/pac/mpep/s708.html)
- [USPTO MPEP §609 — information disclosure statements](https://www.uspto.gov/web/offices/pac/mpep/s609.html)
- [USPTO MPEP §2001 — duty of disclosure, candor, and good faith](https://www.uspto.gov/web/offices/pac/mpep/s2001.html)
- [USPTO MPEP §2111 — claim interpretation and broadest reasonable interpretation](https://www.uspto.gov/web/offices/pac/mpep/s2111.html)
- [USPTO MPEP §2112 — inherency; necessity rather than possibility](https://www.uspto.gov/web/offices/pac/mpep/s2112.html)
- [USPTO MPEP §2113 — product-by-process limitations](https://www.uspto.gov/web/offices/pac/mpep/s2113.html)
- [USPTO MPEP §2143 — reasoned obviousness rationales and predictable combinations](https://www.uspto.gov/web/offices/pac/mpep/s2143.html)
- [USPTO MPEP §2143.03 — all claim limitations must be considered](https://www.uspto.gov/web/offices/pac/mpep/s2143.html)
- [USPTO MPEP §2144.03 — common knowledge and official notice](https://www.uspto.gov/web/offices/pac/mpep/s2144.html)
- [USPTO MPEP §2145 — rebuttal arguments must remain commensurate with the claims; unclaimed limitations are not imported](https://www.uspto.gov/web/offices/pac/mpep/s2145.html)
- [USPTO subject-matter eligibility resources](https://www.uspto.gov/patents/laws/examination-policy/subject-matter-eligibility)
- [Federal Circuit: CloudofChange v. NCR (distributed-system use)](https://www.cafc.uscourts.gov/opinions-orders/23-1111.OPINION.12-18-2024_2438003.pdf)

## 14. Revision record

- **21 July 2026 — A20/KSR defense calibration:** added A20's examiner-favorable forensic-EDL motivation, generic EDL-field disclosure, qualified element-size/product-signature treatment, and selected/front-page exemplar/Figure 2/Sheet 2 and Figure 3/`330` citation controls; added a claim-specific KSR A/D/F/E pre-mortem, current MPEP §§ 2143.03/2144.03/2145 controls, production-versus-detection argument controls, detector-art qualification, and counsel-owned historical-evidence preservation and review directions. No claim text, art score, or claim-set version changed.
- **21 July 2026 — B10 intervening-window reconciliation:** corrected the section 7 current-state statement to record B10 as the one identified intervening-window exception and conformed the section 10 handling instruction to the activation already recorded in the priority map, shared deferred-work memo, and IDS inventory; no claim text, prior-art score, or claim-position conclusion changed.
- **NA-2026-07-21-v2 (21 July 2026):** moved the observable same ordered first-camera-to-second-camera transition at noncoincident timings into NA claim 1; recast NA claim 7 as the narrower internal structured-list identifier/time-code fallback; preserved claims 2–3 as dependent resynchronization fallbacks; and reserved the former broader production theory for coordinated continuation review.
