# AA11393US — NA/AF Claim-Revision Proposal: Temporally Realigned Collusion Attribution (DRAFT)

> **STRATEGIES NA + AF · PROPOSAL STATUS 29 JULY 2026 · NOT ADOPTED**
>
> **INTERNAL COUNSEL-REVIEW MATERIAL — NOT FOR FILING.** This is applicant-prepared analysis, not counsel advice. It proposes additional dependent claims for the `NA` and `AF` branches. Nothing in this document is operative: the controlling claim-set versions remain `NA-2026-07-22-v4`, `AF-2026-07-22-v6`, and `AF-CONT-2026-07-22-v2`, with their version-locked companions, and this document modifies no claim set, map, matrix, briefing, crosswalk, navigator content, or shared control. Every conclusion, wording, gate, and adoption step below requires retained US counsel confirmation.

## 1. Purpose and scope

This proposal adds a fallback family, **temporally realigned collusion attribution**, to both claim strategies. The family covers a colluder who splices portions from differently fingerprinted delivered versions *and* locally or globally retimes each portion to disturb absolute camera-cut time codes before redistribution. Per portion, the claimed operations (1) realign the portion against the reference/mate ensemble by comparison at a plurality of temporal offsets, (2) determine the reference-versus-mate camera-cut timing choice the portion exhibits, and (3) feed the identified chunk selections as inputs to the probabilistic fingerprinting algorithm for comparison against the recipient-associated delivered sequences.

This proposal deliberately claims *operations*, not attack outcomes. It nowhere recites that mates are "resistant to temporal attacks," that collusion is "prevented," or any inherent-immunity result. Such result language would add no patentable weight, would create § 112(b)/(a) exposure, and would move the claim toward D1's (A1, US 2021/0352381 A1) home territory of collusion-prevention-by-copy-transformation, which expressly includes per-copy time delay and frame-rate variation.

## 2. The gap this proposal addresses

Both operative sets claim the two underlying mechanisms in separate branches:

| Mechanism | NA | AF |
|---|---|---|
| Mixed-version collusion attribution | 21, 28 (28 method) | 11–12 (12: segmented Tardos) |
| Temporal-shift-tolerant matching | 17–18, 26 | 7–8, 21–22 |

No operative claim connects them. NA claims 21/28 and AF claims 11–12 presuppose recoverable cut times in a mixed suspect; NA claims 17–18/26 and AF claims 7–8/21–22 supply shift-tolerant matching without the collusion context. A per-portion-retiming colluder sits in the uncovered junction. The proposed family closes that junction as a narrowing fallback beneath the existing collusion claims.

## 3. Evidence, inference, and argument

Per the repository's evidence discipline, the three categories are stated separately.

### 3.1 Contemporaneous disclosure (evidence)

All citations are to [`PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md`](PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md) (line numbers as retained):

- **Mixed-portion tracing** (line 828): even when colluders mix different copies, each segment can still be traced back to its original distribution, via the ledger of unique chunk combinations; unicast/adaptive delivery further complicates seamless mixing.
- **Shift-tolerant matching** (lines 924, 1226): the fuzzy matching method compares content segments between the reference content and pirated webcasting, "allowing for the identification of matches despite temporal shifts or alterations"; it is implemented through comparison of perceptual hashes of groups of frames using sliding windows.
- **Segmented Tardos** (line 849): segmenting content and applying unique Tardos fingerprints per segment enhances localization of pirated segments and, consequently, of colluders.
- **Genus framing of the comparison technique** (lines 816, 822, 1248, 653): perceptual hash and fuzzy matching are "preferred embodiment[s]"; the invention "extend[s] to encompass machine learning algorithms for image and video recognition and advanced signal processing methods for feature extraction and comparison"; the methodology is "not confined solely to the use of perceptual hashing and fuzzy matching"; the core principle "does not depend upon … any specific algorithm/apparatus." As-filed PCT claims 2–3 (dossier lines 1264–1270) recite perceptual hash and fuzzy matching as dependents of a generically recited comparison.
- **Existing support-map postures** (evidence of already-recorded gates): NA claim 21 grades `C/CE/G` ([NA priority-support map](US/normal-allowance/support/AA11393US-NA-priority-support-map_DRAFT.md)); AF claims 11 and 12 grade `C/CE/G` and `D/C/G` ([AF priority-support map](US/allowance-first/parent/support/AA11393US-AF-priority-support-map_DRAFT.md)); the sliding-window species (NA 18, AF 8) grades `D`.

### 3.2 Technical inference (applicant inference — not disclosure)

- A global or per-portion temporal shift does not destroy the reference-versus-mate timing choice a portion carries; an offset sweep can recover the corresponding playback interval, after which the exhibited choice remains readable.
- Where shift noise approaches the reference/mate timing gap (ten frames in Example 2), individual portion attributions become ambiguous; feeding recovered choices as *probabilistic* inputs to the Tardos-type algorithm, rather than demanding deterministic manifest equality, absorbs that ambiguity. This is an engineering argument for the claimed architecture, not a disclosed statement.
- These inferences require confirmation by testing before use as evidence in any proceeding.

### 3.3 Attorney-argument material (argument — not claim text, not disclosure)

- In the interval between the reference and mate switch timings, the versions show frames from different physical cameras; the inter-version difference is genuine scene content, not an extractable embedded delta, and cannot be realigned away within that interval. This is reserved for future § 103 technical-effect argumentation and is intentionally absent from the proposed claim text.
- D1's solution space (arbitrary per-copy transformations causing misalignment among copies) differs from the claimed editing-domain mechanism; the proposed claims remain anchored to the manifest/camera-cut-timing chain for that reason.

## 4. Proposed claims

Wording follows the Tier 1 generalization of § 7: the comparison step recites frames and sliding windows at a plurality of temporal offsets, without limiting the comparison to perceptual hashes. The hash implementation is preserved as a further dependent rung. All claims are singly dependent; no multiple-dependent claims; independent claim counts are unchanged.

### 4.1 NA claim 31 (system; depends from NA claim 21)

> **31.** The system of claim 21, wherein identifying the plurality of time codes comprises, for each of the respective portions:
>
> comparing frames of the respective portion with frames of one or both of the reference audio-video content and the one or more mates using sliding windows at a plurality of temporal offsets to identify a corresponding playback interval;
>
> determining a camera-cut timing exhibited by the respective portion for at least one camera cut within the corresponding playback interval, the determined camera-cut timing corresponding to one of a camera-cut timing of the reference audio-video content and a different camera-cut timing of one of the one or more mates; and
>
> identifying, based on the determined camera-cut timing, a chunk selection of the respective portion, the chunk selections identified for the respective portions serving as inputs to the probabilistic fingerprinting algorithm for comparison with the recipient-associated sequences of chunk selections to identify the one or more recipients.

### 4.2 NA claim 32 (method twin; depends from NA claim 28)

> **32.** The method of claim 28, wherein identifying the plurality of time codes comprises, for each of the respective portions:
>
> comparing frames of the respective portion with frames of one or both of the reference audio-video content and the mate using sliding windows at a plurality of temporal offsets to identify a corresponding playback interval;
>
> determining a camera-cut timing exhibited by the respective portion for at least one camera cut within the corresponding playback interval, the determined camera-cut timing corresponding to one of a camera-cut timing of the reference audio-video content and a different camera-cut timing of the mate; and
>
> identifying, based on the determined camera-cut timing, a chunk selection of the respective portion, the chunk selections identified for the respective portions serving as inputs to the probabilistic fingerprinting algorithm for comparison with the recipient-associated sequences of chunk selections to identify the one or more recipients.

### 4.3 NA claim 33 (implementation fallback; depends from NA claim 31)

> **33.** The system of claim 31, wherein comparing the frames comprises fuzzy matching in which perceptual hashes of groups of frames are compared using the sliding windows.

### 4.4 AF claim 24 (system; depends from AF claim 11)

> **24.** The system of claim 11, wherein identifying the plurality of time codes comprises, for each of the respective portions:
>
> comparing frames of the respective portion with frames of one or both of the reference audio-video content and the one or more mates using sliding windows at a plurality of temporal offsets to identify a corresponding playback interval;
>
> determining a camera-cut timing exhibited by the respective portion for at least one camera cut within the corresponding playback interval, the determined camera-cut timing corresponding to one of a camera-cut timing of the reference audio-video content and a different camera-cut timing of one of the one or more mates; and
>
> identifying, based on the determined camera-cut timing, a chunk selection of the respective portion, the chunk selections identified for the respective portions serving as inputs to the probabilistic fingerprinting algorithm for comparison with the recipient-associated sequences of chunk selections to identify the one or more recipients.

### 4.5 AF claim 25 (implementation fallback; depends from AF claim 24)

> **25.** The system of claim 24, wherein comparing the frames comprises fuzzy matching in which perceptual hashes of groups of frames are compared using the sliding windows.

### 4.6 AF claim 26 (segmented-Tardos width; depends from AF claim 12)

> **26.** The system of claim 12, wherein identifying the plurality of time codes comprises, for each of the respective portions:
>
> comparing frames of the respective portion with frames of one or both of the reference audio-video content and the one or more mates using sliding windows at a plurality of temporal offsets to identify a corresponding playback interval;
>
> determining a camera-cut timing exhibited by the respective portion for at least one camera cut within the corresponding playback interval, the determined camera-cut timing corresponding to one of a camera-cut timing of the reference audio-video content and a different camera-cut timing of one of the one or more mates; and
>
> identifying, based on the determined camera-cut timing, a chunk selection of the respective portion, the chunk selections identified for the respective portions serving as inputs to the probabilistic fingerprinting algorithm for comparison with the recipient-associated sequences of chunk selections to identify the one or more recipients,
>
> wherein the respective fingerprints applied to the content segments comprise the chunk selections identified for the respective portions.

## 5. Antecedent basis and dependency check

| Term in the new limitation | Anchor |
|---|---|
| "identifying the plurality of time codes" | NA 16 / AF 1 (system); NA 22 (method step) |
| "the respective portions"; "the probabilistic fingerprinting algorithm"; "the recipient-associated sequences of chunk selections"; "the one or more recipients" | NA 21 / AF 11 (system); NA 28 (method) |
| "the reference audio-video content"; "the one or more mates" / "the mate" | NA 16 / AF 1 (ensemble); NA 22 (method) |
| "the sliding windows" (NA 33 / AF 25) | Introduced in NA 31 / AF 24 first step |
| "the respective fingerprints"; "the content segments" (AF 26) | AF 12 |

The discriminating-choice clause ("corresponding to one of a camera-cut timing of the reference … and a different camera-cut timing of … the mate(s)") is the limitation that ties the family to the camera-boundary core and away from generic desynchronization-fingerprint art; it must not be diluted in any amendment of these claims.

## 6. Support posture (proposed grades for counsel determination)

| Claim | Proposed grade | Basis and gate |
|---|---|---|
| NA 31, NA 32, AF 24 | **D/CE/G** | Each element is directly disclosed (offset/sliding-window matching; per-portion tracing; manifest-sequence probabilistic input; genus-over-hash framing). The per-portion realign → timing-choice → chunk-selection-input chain is a combined-example relationship not stated in one passage; counsel must conclude written description and enablement separately for the PCT and for the provisional (benefit entitlement), and assign a DW-05A mode per claim |
| NA 33, AF 25 | **D** | Tracks the operative NA 18 / AF 8 species wording |
| AF 26 | **D/CE/G**, additionally inheriting AF 12's open gate | The equation of segmented-Tardos "respective fingerprints" with identified chunk selections is precisely AF 12's unresolved "confirm the exact segment/fingerprint/portion/contributor relationship" gate |
| All six | Inherited gates | The noisy/ambiguous cut-time reconstruction enablement question (NA claim-set § 5 item 9 and AF equivalents) and the collusion-output gates (NA § 5 item 6; AF § 5 item 8) apply to the whole family |

## 7. Alternative Tier 2 first step (wider genus, heavier gate)

Counsel may consider replacing the first step in NA 31/32 and AF 24/26 with:

> comparing visual content of the respective portion with visual content of one or both of the reference audio-video content and the one or more mates at a plurality of temporal offsets to identify a corresponding playback interval;

The dossier's genus statements (§ 3.1) support moving beyond perceptual hashes; the thinner point is that the sliding window is the only concretely disclosed offset-sweep mechanism, so dropping it presents an Ariad-type possession question and a full-scope enablement question across all comparators. Tier 1 (frames + sliding windows) is the broadest scope this proposal can present as defensible without that exposure; Tier 2 is recorded as an option, not recommended as the filed form. Under either tier, NA 33 / AF 25 remain the species fallback.

## 8. Prior-art posture

This family is fallback depth against the per-portion-retiming colluder, not a new independent inventive center. The generalized comparison step is the most art-exposed element; the anchor remains the timing-choice → chunk-selection → recipient-sequence chain, which no reviewed reference maps. Re-scoring must cover at minimum, from the [IDS reference list](US/common/ids/AA11393US-US_IDS-reference-list_DRAFT.md):

| Art | Relevance to the family |
|---|---|
| B6 (Microsoft desynchronized fingerprinting) | Closest stored art to the realignment element: recipient-specific temporal variation with robust hash reacquisition after insertion/deletion/rearrangement and other temporal changes; authoritative English-family review remains outstanding |
| C7 (ICIP 2008 temporal-oscillation collusion-resistant fingerprinting) | Timing-pattern collusion resistance; rated X against D1's PCT claims; full text outstanding |
| C3 (Tardos, STOC 2003) | The probabilistic algorithm itself; already cited in the description |
| A9 / A19 | Collusion-resistant variants and score-based contributor identification |
| A21 | Shot-boundary time-slice fingerprint with exact database comparison and shot-detection-error tolerance |
| A5 | Perceptual image hashing and shot detection |

No identified reference discloses mapping a per-portion realigned camera-cut timing choice to a manifest chunk selection used as a probabilistic-attribution input; the matrices must nevertheless be re-scored against the exact wording if adopted.

## 9. Formal and fee consequences

- **NA:** 30 → 33 total claims; 4 independent (unchanged); 29 singly dependent; excess over the 20-claim basic allocation rises from 10 to 13.
- **AF:** 23 → 26 total claims; 3 independent (unchanged); 23 singly dependent; excess rises from 3 to 6.
- No new independent claim is introduced, so no new unity/restriction election is expected, but counsel must confirm.
- Ordinary excess-claim fees, § 371 national-stage amendment format, antecedent basis, and status identifiers must be rechecked on adoption.
- A method-form hash fallback depending from NA claim 32 (parallel to NA 33) was considered and is not proposed, to bound excess-claim exposure; counsel may reinstate it.

## 10. Open counsel determinations

1. Genus written description and enablement for the generalized comparison step, per filing (PCT written description and enablement; provisional written description and enablement for benefit entitlement), including the Tier 1 versus Tier 2 selection.
2. Combined-example support for the per-portion realign → timing-choice → chunk-selection-input chain (D/CE/G grade).
3. AF claim 26's segment/fingerprint/portion/contributor equation, inheriting AF claim 12's open gate.
4. Enablement of recovery under ambiguous attribution, including the relationship between shift noise and the reference/mate timing gap; construction of the probabilistic input.
5. § 112(b) boundaries of "plurality of temporal offsets" and "corresponding playback interval"; any § 112(f) consequence of the functional steps.
6. DW-05A mode assignment and effective date for each new claim; intervening-art reassessment for any Mode B outcome (including B10's potential § 102(a)(1) posture).
7. Excess-claim fees, unity/restriction, and § 371 amendment mechanics.
8. AF-CONT and crosswalk treatment: record the family under the [continuation-preservation memo](US/common/continuation-controls/AA11393US-continuation-preservation_MEMO.md) whether adopted into AF-CONT or reserved.

## 11. Integration procedure if adopted

Adoption is a version-locked bundle change, not a claim-text edit. In order, per the repository's claim-set generation workflow and [navigator runbook](navigator/RUNBOOK-content-sync-and-regeneration.md):

1. Record the § 10 counsel determinations; select Tier 1 or Tier 2 and the final claim roster.
2. Amend the NA and AF claim-set Markdown and bump the version headers (NA-2026-07-22-v4 and AF-2026-07-22-v6 to new dated versions); regenerate, never hand-edit, the claim-set XML representations.
3. Add the § 6 rows to the NA and AF priority-support-map relation XML and regenerate their Markdown review views.
4. Re-score every affected row of the NA and AF prior-art comparison matrices (§ 8 inventory at minimum) for the new claim-set versions; regenerate review views.
5. Add claim-document mapping rows for the new claims; update both counsel briefings and the fallback-ladder tables ("Temporally realigned collusion attribution": NA 31–33; AF 24–26).
6. Record the cross-strategy and AF-CONT decision per § 10 item 8.
7. Regenerate navigator content and products per the runbook.
8. Run `./validate.sh` to a green result before handoff to counsel.
