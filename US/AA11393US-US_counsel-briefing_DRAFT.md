# AA11393US — US Counsel Briefing (DRAFT)

> **INTERNAL ATTORNEY BRIEFING — NOT FOR FILING.**

## 1. Requested outcome

Prepare and file a US application that protects the commercially meaningful multi-camera content-differentiation mechanism, preserves the benefit of provisional 63/557,868 where supported, presents claims enforceable against the principal commercial actors, and remains eligible for Track One if the applicant chooses a §111(a) bypass continuation.

The international Written Opinion found claims 1–18 novel and industrially applicable but not inventive over D1, US 2021/0352381 A1, principally because the examiner treated the multiple-camera features as known and lacking technical synergy with the rest of the system. The proposed response is to claim and explain the closed technical loop more precisely.

## 2. Invention statement to use throughout prosecution

> A multi-camera production system records camera selections as edit time codes, locally moves selected camera-selection boundaries using temporally corresponding frames from another camera, associates the resulting camera-cut timing patterns with recipients, and later derives and matches camera-source transitions and their corresponding switch timings from suspected content.

The strongest concrete example extends one camera shot by ten frames, correspondingly delays the next camera shot, and restores the reference timing at a later cut. This is more defensible than a generic statement that a time code changes “relative to another cut,” because D1 also discloses frame-rate transformation.

Use the pattern terminology deliberately:

- a **camera-cut timing pattern** is the sequence or arrangement of camera-switch times produced in a version and, where applicable, represented by chunks or manifests for distribution; and
- a **camera-source-transition pattern** is the richer detection-side structure identifying camera-source transitions together with their corresponding camera-switch timings.

The latter includes the former's timing information but adds source-transition structure. This hierarchy preserves broader timing-based language in claims 1/9/15/22 while requiring an operationally stronger detection limitation in claim 16. Do not collapse the terms into synonyms without reviewing written-description support, prior art, and claim scope.

## 3. Commercial actor and enforcement map

| Commercial function | Likely actor | Candidate independent claim | Evidence likely available |
|---|---|---|---|
| Creates reference edit and mates | host broadcaster, outside-broadcast facility, production-software vendor | Claim 1 | production configuration, EDLs, output comparisons, software documentation |
| Builds manifests, distributes streams, records recipient mapping | rights-holding licensee, streaming platform, origin/CDN operator | Claim 9 | manifests, network traffic, account records, platform documentation |
| Detects pirate stream and resolves source | rights owner, anti-piracy monitoring provider, platform trust/safety system | Claim 16 | monitoring output, comparison logs, ledger queries, software behavior |
| Operates entire lifecycle | vertically integrated broadcaster/platform | Claim 22 | combined operational evidence |

The subsystem claims are not merely drafting convenience. They reduce dependence on proving that one entity controls or performs production, distribution, and later detection. They do not eliminate the need for a fact-specific direct-infringement or attribution analysis. The end-to-end claim remains valuable for the full-combination patentability position and integrated deployments.

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
2. actual local substitution of frames from one camera for frames selected from another;
3. later cut retains the reference timing or restores synchronization;
4. camera-cut pattern represented through interleaved manifests;
5. recipient ledger;
6. detected cut time codes and reconstructed manifest;
7. perceptual hash/sliding-window matching; and
8. probabilistic collusion attribution.

## 5. D1 position

Counsel should avoid the earlier categorical descriptions of D1.

D1 does disclose:

- a completed base copy that is replicated and transformed;
- watermark-like arbitrary identifiers in addition to watermarks;
- transformations selected by ID and/or randomly or pseudo-randomly;
- segmentwise transformations;
- uniform delay and frame-rate variation; and
- use of scene changes to mask transitions between transformations.

The proposed distinction is that D1 alone does not disclose or motivate the complete route of synchronized alternate-camera source material → recorded camera-selection boundary → local source-camera substitution → recipient-associated boundary pattern → recovery of that pattern from suspected content. This is not a conclusion that the claims are “untouchable”: counsel should assess §103 combinations with conventional multi-camera production, EDL, personalization, and forensic-identification art.

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

EP 2 811 416 A1 supplies part of the same motivation narrative by using a temporal pattern for identification in view of removable visual watermarks. Describe that disclosure precisely; do not say that B8 “anticipates the motivation.” Its grant, withdrawal, or national legal status does not alter the disclosure date of the published A1 document, although its EPO file history may reveal useful examination reasoning or additional cited art.

The detection independent requires particular attention. Generic stored timing patterns are vulnerable to an argument that the asserted distinction resides only in informational content. Preserve an operational relationship in which the system derives and matches camera-source-transition structure at regions where delivered versions differ in their selection between temporally corresponding camera views. Counsel should confirm written-description support for the exact formulation and avoid relying only on a statement that generic data were “produced by” the mate-generation process.

The attached prior-art matrix and IDS inventory identify the candidate documents. Counsel should commission a focused supplemental search before finalizing the claims and should review all identified documents for disclosure.

## 7. Priority and written-description position

The provisional contains the core multi-camera, EDL, local ten-frame variation, manifest, ledger, detection, perceptual-hash/fuzzy-match, Tardos, overlay, and ML passages. It also contains support for later-cut alignment, but that support has an internal drafting inconsistency requiring express analysis. At provisional PDF p. 27 (printed p. 16), the mate EDL table places Cut 4 at `00:00:30:01` and labels it adjusted to the reference. The accompanying paragraph also calls `00:00:30:11` a mistake and expressly states that the correct approach is `00:00:30:01`, matching the reference with no delay. The PCT Example 2 uses the corrected alignment. This is favorable evidence of the intended teaching, but it does not replace a claim-as-a-whole priority opinion or justify an unqualified support rating.

Use the attached provisional/PCT map to confirm:

- entitlement of each material limitation to 26 February 2024;
- PCT support for every bypass or preliminary-amendment limitation;
- whether proposed terminology is a fair expression of the disclosed examples;
- whether the Example 2 correction would be understood by a skilled reader as possession of later-cut resynchronization and the PCT wording is a permissible clarification rather than new matter; and
- whether any post-PCT improvement requires a separate continuation-in-part analysis.

Keep the Example 2 inconsistency in the internal priority analysis. Do not add it to the public WIPO informal comments unless counsel concludes that a public statement is strategically necessary.

### Intervening-information trigger

The limited review recorded in this package has not identified potentially material art or another prior-art event having an effective date after 26 February 2024 but before 19 February 2025. That statement is not a clearance opinion and must not be treated as proof that no such information exists.

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
- state in claim 9 that processors, rather than servers as such, execute the stored instructions;
- retain concrete algorithms where helpful, but recognize that perceptual hashing and shot detection are known;
- confirm corresponding algorithm disclosure if §112(f) is invoked;
- treat the ML claims as expendable because their disclosure is result-oriented;
- ensure that “camera-selection boundary,” local substitution, and resynchronization remain within the language and teaching of the filed documents;
- preserve the functional relationship in claim 16 between detected transitions, camera-view selection regions, candidate patterns, and recipient resolution;
- draft collusion claims 21 and 28 as affirmative limitations requiring mixed-version suspected content and performance of probabilistic attribution, rather than optional “when” clauses;
- preserve the stated hierarchy between camera-cut timing patterns and camera-source-transition patterns; and
- confirm that claims 17 and 18 may recite detection of both camera-source transitions and their corresponding timings, while keeping claim 19 timing-specific because reconstructed manifests are built from derived time codes.

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

If the intervening-information trigger in section 7 is activated, counsel should reconsider the disclosure and argument strategy before filing or supplementing the comments. Activation of the trigger does not by itself require insertion of the internal Example 2 analysis into the public comments.

## 11. IDS instructions

Review the supplemental candidates, complete official bibliographic/copy/translation handling, obtain the Italian search report, and file the counsel-approved disclosure package under the procedure applicable to the selected route. The deferred tasks, suggested owners, triggers, and completion evidence are collected in `AA11393US-deferred-filing-disclosure-and-EP-work_MEMO.md`. In particular:

- verify CN 100583750 C against an official register and obtain the appropriate copy and English handling;
- inspect the EP 2 811 416 A1 family and EPO file history, without treating current legal status as controlling its prior-art disclosure;
- obtain official copies of A2, A3, A5, B7, Tardos 2003, and the remaining references selected for submission; and
- route every citation from the Italian search report into the IDS review promptly upon receipt.

Treat the list as an inventory, not as a statement that every item is prior art or material.

## 12. Questions requiring counsel's written recommendation

1. §371 or bypass, and why?
2. Track One requested or not?
3. Which four independent claims best match the applicant's expected licensing and enforcement targets?
4. Is the local alternate-camera substitution wording support-safe and sufficiently definite?
5. In view of the provisional Example 2 inconsistency, is later resynchronization entitled to the provisional date, and should it remain dependent or also appear in parallel independent scope?
6. Does the 30/4 set create unacceptable restriction risk, how should its zero net claim-count headroom be managed, and what divisional strategy is recommended?
7. Which supplemental references should be submitted, and is a further search required before filing?
8. Does every selected claim receive the provisional date?
9. Which terms risk §112(f), and what restructuring is recommended?
10. Should ML, blockchain, overlay, Tardos, and CRM claims be retained, replaced, or reserved for a continuation?
11. Is any “without pixel-domain embedding” dependent claim worth the scope cost, or should that remain only an explanatory advantage?
12. Are the WIPO informal comments approved for filing and aligned with the intended EP response?
13. Does candidate claim 16 establish a patentable operational relationship to camera-source-transition structure with adequate provisional and PCT support, or should it be restructured further?
14. Are the inventor declaration, applicant identity, assignment chain, and recordation record complete for the selected route?
15. Who will monitor the provisional-to-PCT interval for potentially material intervening information, and what event will trigger a renewed priority, IDS, and representation review?
16. Is the deliberate relationship between “camera-cut timing pattern” and “camera-source-transition pattern” support-safe and appropriately reflected in claims 1/9/15/16/22 and harmonized claims 17–18?

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
- [USPTO subject-matter eligibility resources](https://www.uspto.gov/patents/laws/examination-policy/subject-matter-eligibility)
- [Federal Circuit: CloudofChange v. NCR (distributed-system use)](https://www.cafc.uscourts.gov/opinions-orders/23-1111.OPINION.12-18-2024_2438003.pdf)
