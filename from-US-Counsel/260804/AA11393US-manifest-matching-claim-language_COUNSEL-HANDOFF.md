# AA11393US — Manifest Matching, Direction-Neutral Camera-Switch Timing, and Collusion Attribution

> **INTERNAL DRAFT FOR US COUNSEL REVIEW · 9 AUGUST 2026 · NOT FOR FILING**
>
> This handoff memorandum presents applicant-proposed claim language and the principal support, priority, patentability, and procedural questions for US counsel determination. It does not resolve claim construction, written description, enablement, priority entitlement, patentability, restriction, fees, or filing strategy.

## Handoff package and document status

The unchanged 4 August 2026 US-counsel source records are:

- `260804-P3366-US new claims 19-38 FINAL CLEAN.md`;
- `260804-P3366-US abstract FINAL CLEAN.md`; and
- `260804-P3366-US support FINAL CLEAN.md`.

The following companion Markdown documents implement the applicant-proposed wording and twenty-claim topology for counsel review:

- `revised-versions/260808-P3366-US new claims 19-38 REVISED DRAFT.md`;
- `revised-versions/260808-P3366-US abstract REVISED DRAFT.md`; and
- `revised-versions/260808-P3366-US support REVISED DRAFT.md`.

The companion documents are applicant-prepared review drafts. They do not amend, supersede, or represent approval of the 4 August counsel source records and are not authorized for filing. If counsel adopts any proposal, counsel should determine and control the resulting filing text.

Page-and-line references in the companion support statement are keyed to the as-filed PCT specification print reproduced in the RAPPORTO DEPOSITO, in which specification page N appears at dossier PDF page N+7. Counsel should confirm that the US-filed specification print preserves the same pagination before using those references.

## Executive recommendation

The applicant recommends that the parent retain twenty total claims and adopt four independent claims directed respectively to:

1. a production-to-single-recipient-attribution system;
2. a single-recipient monitor-side method;
3. a multi-contributor monitor-side method; and
4. an integrated production-to-single-recipient-attribution method.

The proposed independent claims use a mate camera-switch timing **different from**, rather than necessarily later than, the corresponding reference timing. Direction neutrality is coupled to the retained ordered transition between identified physical cameras and to the interval between the two timings in which the reference and mate contain temporally corresponding frames from different source cameras. A bare timing difference is not recommended.

For single-recipient attribution, the proposed claims replace undefined complete-file equality with an express cut-by-cut relationship between the timing choices represented by the delivered and reconstructed manifests. They require the same reference-or-mate timing choice for each selected cut and at least one detected mate timing. They do not require byte, syntax, URI, rendition-metadata, device-field, or network-field identity.

For multi-contributor attribution, proposed independent claim 33 avoids requiring a colluded composite to match the complete timing-choice sequence of one delivered manifest. It instead classifies detected cut time codes as reference or mate choices for respective temporal portions, probabilistically compares the detected sequence with recipient-associated manifest sequences, and identifies multiple contributing recipients. Proposed dependent claim 34 adds segmented-Tardos processing.

The delayed species remains available in system claim 20 and integrated-method claim 36. The corresponding-chunk-selection species remains available in system claim 29 and monitor-side claim 31. No byte-identity claim is presently recommended.

## Reasons for changing the manifest relationship

Source claims 19, 35, and 38 use a delivered manifest file “equal to” a reconstructed manifest file. The intrinsic record contains literal support for that wording but does not define whether equality means:

- byte-for-byte identity;
- syntactic or structural identity;
- identity of referenced chunk selections; or
- correspondence between the represented camera-switch timing choices.

The additional functional language in the source claims may be read as cumulative with, rather than explanatory of, “equal to.” Under that construction, a delivered manifest representing the same timing choices could fall outside the claim because its serialization, URIs, bitrate ladder, rendition metadata, device-specific fields, or network-condition fields differ from the reconstructed manifest.

That result does not align cleanly with the disclosed detection process. The reconstructed manifest is built from camera-cut time codes detected in suspected unauthorized content. Those time codes do not provide every transport, addressing, rendition, token, metadata, or serialization field that may have appeared in a delivered adaptive-streaming manifest.

The intrinsic record candidly contains both approaches:

- PCT retrieval component 140 and PCT original claim 15 state that delivered manifest files are “equal to” reconstructed manifest files. See PCT list-item 00964 and original-claim list-item 01237.
- Provisional original system claim 1(n), at specification page 32, uses corresponding equality language.
- PCT original claim 1 identifies a distinguishable version matching the suspected unauthorized distribution. See PCT list-item 01218.
- PCT searching step 290 searches for a manifest having the detected scene changes. See PCT list-item 01029 and original claim 16 at list-item 01255.
- Provisional original method claim 10(k), at specification page 33, searches the ledger to identify the account or accounts associated with the reconstructed manifest without separately reciting complete-file equality.

The proposed wording therefore does not characterize the equality disclosure as erroneous. It states expressly the technical relationship intended for the independent claims and preserves complete chunk-selection correspondence as a dependent fallback.

## Reasons for direction-neutral timing

Source claims 19 and 35 require a later mate timing. The source abstract is already direction-neutral, stating that mate versions vary selected camera-cut timings while retaining the same ordered camera transitions. Source claim 38 likewise uses a different mate camera-cut timing.

The PCT and provisional contain an algorithmic disclosure of both timing directions:

- PCT Example 1 metacode alternates between adding and subtracting time, assigns a variation of `1` or `-1`, and applies the variation through `event.timestamp += variation`. See PCT codeblock 01066.
- PCT original claim 1 recites automatically altering at least one camera-cut timing relative to the reference content without limiting the alteration to delay. See PCT list-item 01212.
- The corresponding provisional metacode appears at specification pages 14–15, which are document pages 25–26 of the as-filed provisional PDF.

Example 2 supplies the concrete delayed species: extension of the first-camera selection, later commencement of the following camera selection, and restoration of synchronization at a subsequent cut. See PCT paragraph 01134 and specification pages 33–35; see also provisional specification pages 16–17.

The positive/negative metacode does not separately tabulate an earlier-timing EDL having the complete paired-entry and intervening-different-camera relationship. The proposed direction-neutral claim therefore requires a claim-as-a-whole determination whether the algorithmic disclosure and the concrete physical-camera disclosure may properly be read together for written description, enablement, and priority.

The reviewed prior-art matrices do not rely on delay direction as the patentability distinction. The NA matrix identifies movement of the same ordered physical-camera boundary to a noncoincident timing, with different-camera frames in the intervening interval, as the principal production distinction and states that variable timing alone is crowded. See NA matrix rows 00001 and 00005. The AF matrix likewise states that the retained physical-camera boundary and structured-list operation carry the production-side distinction. See AF matrix row 00002.

Direction neutrality therefore appears to improve literal coverage without surrendering a distinction used against the currently reviewed art. Exact claim-by-claim rescoring remains required, particularly against direct multicamera, EDL, stream-switching, and variable-timing art.

## Multi-contributor and segmented-Tardos coverage

Source claims 29 and 30 address content assembled from portions delivered under different manifests, probabilistic identification of contributing recipients, and segmented Tardos processing. Because they depend from source claim 19, however, they inherit its complete single-manifest matching condition. A colluded composite may correspond to no single delivered manifest across all selected cuts.

Proposed independent claim 33 is therefore a standalone monitor-side method. Its fingerprint alphabet remains tied to the claimed physical-camera structure:

- recipient-associated manifest sequences represent reference-or-mate timing choices;
- each choice concerns the same ordered transition from an identified first source camera to an identified second source camera;
- reference and mate timings differ;
- during the interval between them, reference and mate contain temporally corresponding frames from different source cameras;
- each identified cut time code is classified as representing the reference or mate timing; and
- probabilistic comparison identifies recipients contributing respective temporal portions.

The PCT support relied upon includes:

- the colluding-redistribution disclosure that multiple pirates may merge segments from distinct delivered versions and that recorded chunk combinations and the ledger may identify the involved accounts, at PCT paragraph 00994;
- probabilistic and Tardos attribution of users contributing to a composite pirate copy, at PCT paragraphs 00997 and 00998;
- segmented-Tardos localization of pirated segments and colluders, at PCT paragraph 01001; and
- probabilistic fingerprinting in PCT original claim 5, at paragraph 01223.

The corresponding provisional disclosures appear at specification pages 27–28, together with original system claim 6. Those passages must be read with the provisional manifest, chunk-combination, altered-cut, recipient-association, and monitoring disclosures.

The reviewed matrices record substantial pressure against generic collusion attribution and Tardos processing from A2–A4, A6, A9, A19, B6, and C3. See NA matrix row 00053 and AF matrix row 00109. Proposed claims 33 and 34 do not treat Tardos processing as the novelty center; their present justification depends on the physical-camera timing-choice structure and the manifest-sequence-to-portion relationship. B9, A20, and direct multicamera or EDL art should also be assessed against the exact wording.

Claim 33 requires separate claim-as-a-whole determinations concerning actor attribution, written description, enablement, provisional priority, definiteness, patentability, and restriction.

## Proposed twenty-claim topology

| Final claims | Family and function | Source or disposition |
| --- | --- | --- |
| 19 | Direction-neutral system independent | Amended source claim 19 |
| 20 | System delayed-timing and resynchronization fallback | Amended source claim 20 |
| 21–25 | System implementation dependents | Renumbered source claims 22–26; source claim 21 omitted |
| 26 | Adaptive CDN, manifest tailoring, and progressive mixing | Consolidated source claims 27 and 28 |
| 27 | Equal-duration corresponding chunks | Renumbered source claim 31 |
| 28 | Physical-camera content of corresponding chunks | Renumbered source claim 32; depends from claim 27 |
| 29 | Same chunk selections at corresponding manifest positions | System dependent |
| 30 | Direction-neutral single-recipient monitor independent | Renumbered and amended source claim 38 |
| 31 | Monitor-side corresponding-chunk-selection fallback | New dependent from claim 30 |
| 32 | Monitor-side matched-manifest physical-camera geometry | New dependent from claim 30 |
| 33 | Physical-camera multi-contributor attribution independent | Standalone rearchitecture of source claim 29 |
| 34 | Segmented-Tardos contributor-localization fallback | Rearchitected source claim 30; depends from claim 33 |
| 35 | Direction-neutral integrated-method independent | Amended source claim 35 |
| 36 | Method delayed-timing and resynchronization fallback | New dependent from claim 35 |
| 37 | Method perceptual-hash fallback | Relocated source claim 36; depends from claim 35 |
| 38 | Method fuzzy and sliding-window fallback | Relocated source claim 37; depends from claim 37 |

The topology contains eleven system-family claims, three single-recipient monitor-side claims, two multi-contributor claims, and four integrated-method claims. It contains four independent claims and twenty total claims; every dependent claim is singly dependent.

The fourth independent claim is expected to incur an excess-independent-claim fee. Counsel should confirm entity status, the applicable fee, filing instructions, and any other procedural consequence.

The exact ten-frame species is omitted, while its broader delayed-timing and subsequent-resynchronization relationship remains in claims 20 and 36. Source claims 27 and 28 are consolidated in claim 26. Source claims 29 and 30 are rearchitected as claims 33 and 34. The source unicast claim 33 and source overlay-before-segmentation claim 34 are omitted. No manifest-independent or broader partial-detection claim is allocated within the proposed twenty claims.

## Companion abstract and support statement

The companion abstract tracks:

- direction-neutral physical-camera timing;
- the intervening different-camera interval;
- cut-by-cut semantic correspondence;
- an affirmative mate-timing requirement; and
- multi-contributor segment-level attribution.

The abstract contains 145 words, excluding the heading.

The companion support statement:

- preserves the intrinsic record's literal equality formulation;
- identifies the Example 1 positive/negative metacode separately from Example 2's delayed EDL species;
- maps the new numbering and dependencies;
- provides a separate claim-as-a-whole discussion for claims 33 and 34;
- does not characterize single-recipient matching as an undefined complete-file equality search;
- does not characterize generic Tardos processing as supplying the physical-camera timing-choice structure; and
- identifies the limitations supported only by cited passages read together rather than by a single express passage.

## Principal risks and tradeoffs

### Direction-neutral written description and priority

Both timing directions are disclosed algorithmically, but only the delayed species is fully tabulated through the paired EDL entries and intervening physical-camera interval. Counsel should decide whether the complete direction-neutral relationship is adequately supported as a combined disclosure by both priority documents.

### Cut-by-cut matching scope

The proposed single-recipient claims require the same timing choice at every selected cut. This supplies objective semantic identity but may exclude partial detections or excerpts not spanning the full selected-cut set. A broader partial-detection claim is not presently allocated and should not be added without separate support and prior-art review.

### Monitor-side scope

Independent claim 30 avoids affirmative production steps but retains manifest and ordered-physical-camera relationships. Dependent claim 32 adds the intervening different-camera geometry. Counsel should assess whether that allocation supplies useful monitor-side scope and adequate patentable weight.

### Multi-contributor scope

Independent claim 33 avoids complete correspondence to one delivered manifest, but its physical-camera, timing-classification, probabilistic-sequence, and contributor-identification limitations form a combined relationship. Counsel should examine actor attribution, technical operability, antecedent basis, definiteness, support, priority, and infringement proof as a whole.

### Restriction

Claims 19, 30, 33, and 35 share recipient-associated use or detection of the same ordered physical-camera transition at reference and different mate timings. Nevertheless, the production, single-recipient monitoring, multi-contributor monitoring, and integrated-method formulations may present distinct search or examination burdens. Counsel should determine the likely restriction posture and any election, traversal, rejoinder, continuation, or divisional strategy.

### Prior art

The existing matrices support the structural thesis but do not establish patentability of the exact proposed claims. Every affected matrix row should be rescored against the current claim language, including the direction-neutral timing, intervening different-camera interval, explicit reference-or-mate classification, corresponding-chunk fallbacks, multi-contributor relationship, segmented-Tardos species, consolidated claim 26, and method-resynchronization fallback.

## Determinations requested from US counsel

Before assembling or filing a preliminary amendment, counsel is requested to determine:

1. whether claims 19 and 35 should use a mate timing different from the reference timing together with the retained ordered-camera and intervening-different-camera relationship;
2. whether that direction-neutral relationship is adequately described, enabled, and entitled to the provisional filing date;
3. whether claims 20 and 36 provide sufficient delayed-timing and resynchronization fallbacks without the ten-frame species;
4. whether removing complete-file equality in favor of express cut-by-cut timing-choice identity preserves the intended novelty, non-obviousness, definiteness, and infringement positions;
5. whether claims 29 and 31 provide useful corresponding-chunk-selection fallbacks without creating impractical adaptive-streaming or infringement constructions;
6. whether monitor-side independent claim 30 and physical-camera dependent claim 32 have adequate support, priority, definiteness, and patentable weight;
7. whether independent claim 33 properly avoids the single-manifest collusion gap while defining a technically coherent and legally sufficient relationship among detected portions, per-cut classifications, recipient-associated manifest sequences, probabilistic evaluation, and multiple contributors;
8. whether claims 33 and 34 satisfy actor, written-description, enablement, provisional-priority, definiteness, and patentability requirements as a whole;
9. whether the omission of the ten-frame, unicast, and overlay-before-segmentation claims and consolidation of the adaptive-CDN and progressive-mixing limitations provide the preferred twenty-claim allocation;
10. the applicable excess-independent-claim fee, entity status, and filing instructions for four independent claims;
11. whether a broader partial-detection or manifest-independent claim should displace another claim after separate support and prior-art analysis;
12. whether the four independent claims are sufficiently linked for examination and what restriction, election, traversal, rejoinder, continuation, or divisional strategy should apply; and
13. whether the page-and-line citations in the companion support statement correspond to the US-filed specification print.

## Requested disposition

The companion claims, abstract, and support statement are supplied to make the proposed language directly reviewable. Counsel may accept, reject, revise, or selectively adopt the proposals. No companion document should be used as filing text until counsel has completed the determinations above, conformed the affected support and prior-art analyses, and authorized a counsel-controlled filing version.
