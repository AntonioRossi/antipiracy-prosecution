# AA11393US — Proposed Final Revisions for Preliminary Amendment

> **FINAL DRAFT FOR US COUNSEL REVIEW · 4 AUGUST 2026 · NOT FOR FILING**
>
> We accept the Rev B approach in principle and propose the following limited revisions and support-section updates for finalization of the preliminary-amendment package.

## 1. Claim 38 — final wording refinement

The Rev B approach is acceptable in principle because it preserves the affirmative-mate requirement on the detection side and continues to exclude an all-reference detected combination. One small wording refinement remains requested.

Current Rev B ending:

> “the delivered manifest file that is equal to the reconstructed manifest file thereby represents the combination of camera-cut timings detected in the suspected unauthorized distribution.”

Proposed ending:

> “the delivered manifest file that is equal to the reconstructed manifest file represents the same detected combination.”

The complete proposed final limitation would read:

> “wherein the reconstructed manifest file represents, for at least one of the plurality of camera cuts, the respective different mate camera-cut timing detected in the suspected unauthorized distribution, and wherein the delivered manifest file that is equal to the reconstructed manifest file represents the same detected combination.”

### Reasons and advantages

- **Direct antecedent basis.** “The same detected combination” refers directly to the detected combination already introduced when the reconstructed manifest file is built, rather than introducing a potentially separate expression, “the combination of camera-cut timings detected.”
- **Preserved suspected-distribution nexus.** The antecedent detected combination is built from the identified camera-cut time codes obtained from the suspected unauthorized distribution, so the shorter wording retains that source relationship without repeating it in the final clause.
- **Removal of a conclusory connector.** Deleting “thereby” avoids presenting the represented-combination relationship merely as an inferred consequence of manifest equality.
- **Clearer equality nexus.** The delivered manifest is expressly required to represent the same detected combination, preserving the intended functional meaning of “equal.”
- **Consistency across the independent claims.** Claims 19 and 35 already require the delivered manifest found through the equality search to match the detected combination represented by the reconstructed manifest file. The proposed claim 38 wording expresses the same substantive nexus in the monitor-side claim without importing the production-side limitations of claims 19 and 35.
- **Preservation of the patentability gate.** The preceding language continues to require at least one different mate camera-cut timing in the detected combination and therefore excludes an all-reference combination.
- **Greater concision without intended scope change.** The proposed language shortens the clause while retaining the Rev B detection-side formulation and its substantive relationship.

The refinement is intended to clarify the represented-combination nexus without resolving the meaning of “equal,” for which byte identity, equivalent chunk selections and equivalent represented timing choices remain reserved constructions. Please adopt the refinement and confirm that it does not inadvertently foreclose any intended construction of “equal,” particularly for the adaptive-streaming dependent claims, or otherwise identify whether “thereby” and the longer expression serve a specific intended claim-construction purpose. This construction check is for counsel correspondence only and should not be incorporated into the preliminary-amendment remarks absent a deliberate claim-construction decision.

## 2. Abstract — proposed replacement

We also propose replacing the current Abstract with the following text:

> “An anti-piracy system generates recipient-associated distinguishable versions of audio-video content. A reference version is produced according to a structured list of edit instructions identifying source cameras and camera-cut time codes. Mate versions vary selected camera-cut timings while retaining the same ordered camera transitions. The reference and mate versions are segmented into chunks, and manifest files select recipient-associated combinations of those chunks. A ledger associates delivered manifest files with recipients. For suspected unauthorized content, camera-cut time codes are detected and used to build a reconstructed manifest file representing a detected combination of camera-cut timings. The ledger is searched for a delivered manifest file representing the same detected combination to identify the associated recipient.”

### Reasons and advantages

- **Complete opening sentence.** The proposal corrects the grammatically incomplete opening, “An anti-piracy system that safeguards …”.
- **Neutral terminology.** It removes laudatory expressions such as “safeguards” and “effective identification” and uses “distinguishable” instead of the more absolute “unique.”
- **Alignment with the new claims.** It follows the operative technical sequence: structured edit instructions, reference and mate timings, chunk combinations, delivered manifests, ledger, detection, reconstruction and recipient identification.
- **Consistency with proposed claim 38.** “Representing the same detected combination” reproduces the requested relational wording and has an express antecedent within the Abstract itself.
- **No added technical subject matter.** Each stated operation and relationship is drawn from the as-filed architecture and the proposed claims; the revision formalizes and condenses the disclosure without adding an implementation or technical effect.
- **Concise USPTO format.** The proposal is a single technical paragraph within the preferred abstract length.

Please use this text as the revised Abstract or identify any filing-specific wording adjustment considered necessary.

## 3. Proposed revisions to counsel's support section

Please revise `P3366-US support.pdf`, reviewed together with its text-accessible copy `P3366-US support.txt`, as follows before the support section is used in the preliminary-amendment remarks.

### 3.1 Replace and expand the distribution paragraph for claims 27, 28 and 33

The distribution paragraph should identify claims 27, 28 and 33 expressly and use the following support paths:

- **Claim 27:** pages 8, lines 9–21 and 14, lines 10–21; Method 200 at page 29, lines 19–27, where segmenting step 240 enables CDN adaptive streaming across varying network conditions and device capabilities and generation step 250 produces manifest files tailored to end-user devices and network conditions; and original claim 11, which recites the same CDN, adaptive-streaming and tailored-manifest relationship in claim form. This is an express claim-specific clarification of support already identified generally in counsel's draft, not a new support gate.
- **Claim 28:** page 18, line 23 through page 19, line 12, covering the mixing component's integration of reference and mate chunks, generation of manifest files and progressive user-manifest association as a sufficient variety of cuts is generated; page 40, lines 5–7, which independently confirms dynamic updating of user-manifest associations as more variations and cuts are created; and original claim 12, which recites integration, manifest generation and association of users with manifest files as the system progressively provides different camera cuts.
- **Claim 33:** page 30, lines 18–20, which states that streamed content is distributed using unicasting to provide each spectator with a unique content stream, and original claim 6, which recites distribution of streamed content using unicasting. This is an express claim-specific tie to support already cited generally in counsel's draft, not a new support gate.

The revised paragraph should therefore replace the present page 18, lines 23–28 reference with **page 18, line 23 through page 19, line 12**, retain the valid page 40, lines 5–7 citation, and tie original claims 11, 12 and 6 specifically to claims 27, 28 and 33, respectively.

**Rationale.** These changes make the distribution support claim-specific, avoid suggesting that page 18, lines 23–28 alone discloses the complete mixing function, preserve the valid Example 4 citation for progressive assignment and close the remaining claim-number omission for unicast delivery.

### 3.2 Correct the Example 5 endpoint

Replace “Example 5 at pages 40–43” with **“Example 5 at pages 40–42.”** Example 5 begins later on page 40, after the conclusion of Example 4, and continues through page 42. Page 43 begins the original claims and is not part of the example.

**Rationale.** The corrected endpoint confines the citation to the description actually forming Example 5 and avoids presenting the first original-claims page as part of the example.

### 3.3 Add express support statements for claims 24, 31 and 32

The revised support section should add a paragraph along the following lines:

> New claim 24 is supported by page 16, lines 1–8, describing further camera cuts spawning additional mates and manifest files, read together with Example 2 at pages 33–35, which provides the concrete single-cut variation at the Cut 2/Cut 3 boundary. New claim 31 is supported by page 15, lines 12–16, which states that reference and mate manifest files point to sets of chunks of equal duration, together with Example 3 at pages 36–38, which shows the respective manifests selecting different chunks at corresponding positions. New claim 32 is supported by Example 3's corresponding reference/mate chunk positions read together with Example 2's source-camera sequence and different reference and mate switch timings.

The support characterization should remain precise: claim 31 has the clearest support path, with equal duration stated expressly at page 15, lines 12–16 and the same playback interval shown by the corresponding manifest positions in Example 3. Claims 24 and 32 likewise rely on the identified passages read together and should not be described as appearing verbatim in a single passage.

**Rationale.** Express treatment closes the claim-specific omissions and identifies which elements are stated directly and which are shown by reading the cited passages together, avoiding overstatement in the prosecution record.

### 3.4 Add the complete production-to-attribution nexus for claims 19 and 35

The support section should state expressly that, in claims 19 and 35, the manifest found through the equality search is one of the recipient-associated timing-choice manifests generated, delivered and recorded by the claimed process, contains an affirmative mate timing and matches the detected combination reconstructed from the suspected distribution.

The supporting citations should connect PCT original claim 1 and page 12, line 16 through page 13, line 4 with pages 14–16, original claims 11–15 and 17, and Examples 3–5. Together, those passages disclose the active chain of mate production, manifest generation, recipient delivery, ledger registration, reconstruction from detected cut timings and equality-based recipient identification.

The different support posture of passive monitor-side claim 38 may guide your review but need not be volunteered or characterized as a comparative weakness in the filing remarks.

**Rationale.** Claims 19 and 35 recite the active production-to-attribution chain underlying the affirmative-mate nexus. Stating that complete chain is more probative of written description than citing its production and detection components separately, without creating an unnecessary comparative statement about claim 38 in the filing record.

### 3.5 Add the process-order support for claim 34

The claim 34 sentence should be expanded to state that the claimed overlay-before-segmentation order is supported by page 24, lines 12–16 and page 30, lines 11–13, read with Method 200 at page 29, lines 15–24. Method 200 places programming step 230, in which the overlay is applied to the ensemble of the reference content and mates, before segmenting step 240. Original claim 4 separately confirms the overlay feature.

This support statement should identify the disclosed process order, rather than cite overlay and segmentation only as separate features.

**Rationale.** Claim 34 requires a temporal relationship, not merely the presence of both operations. Linking the overlay disclosure to the ordered Method 200 steps supplies the basis for “before segmentation” without claiming that original claim 4 alone recites that order.

### 3.6 Revised support-section output

Please return a revised support section incorporating the replacement page ranges and the express claim-specific statements above. It should distinguish direct support from support obtained by reading identified passages together and should not imply that a combined relationship appears verbatim in a single passage.

## 4. Requested next step

Please incorporate the proposed claim 38 wording and Abstract, make the support-section revisions above, and return the revised materials for final applicant review. If any proposed adjustment is not adopted, please identify the filing-specific or claim-construction reason.
