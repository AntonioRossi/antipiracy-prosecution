# AA11393US — Manifest Matching, Direction-Neutral Camera-Switch Timing, and Collusion Attribution Memorandum

> **INTERNAL DRAFT FOR US COUNSEL REVIEW · 8 AUGUST 2026 · NOT FOR FILING**
>
> This memorandum addresses manifest-matching language, direction-neutral camera-switch timing, and multi-contributor collusion attribution in relation to the PCT and provisional disclosures. It does not resolve claim construction, written description, priority entitlement, patentability, or filing strategy, which remain for US counsel.

References identified as “source” claims in this memorandum are to claims 19–38 in the unchanged 4 August 2026 [`260804-P3366-US new claims 19-38 FINAL CLEAN` counsel draft](260804-P3366-US%20new%20claims%2019-38%20FINAL%20CLEAN.md). References identified as “final” claims refer to the proposed twenty-claim topology stated below. The corresponding [abstract](260804-P3366-US%20abstract%20FINAL%20CLEAN.md) and [claim-support statement](260804-P3366-US%20support%20FINAL%20CLEAN.md) also remain unchanged source records. All applicant-proposed changes are stated only in this memorandum for counsel to implement, if adopted, in a separate revision.

Page-and-line references in the proposed claim-support text are keyed to the as-filed PCT specification print reproduced in the RAPPORTO DEPOSITO, in which specification page N appears at dossier PDF page N+7. Before using those references in the US filing package, counsel should confirm that the US-filed specification print preserves the same pagination.

## Current drafting issues

### Manifest equality

The source counsel draft's claims 19, 35, and 38 require a delivered manifest file to be “equal to” a reconstructed manifest file. The intrinsic disclosure does not state whether “equal” means:

- byte-for-byte file identity;
- syntactic or structural identity;
- identity of referenced chunk selections; or
- a match between the camera-switch timing choices represented by the two manifests.

The claims additionally require the delivered manifest to match or represent the same detected combination. That additional functional relationship does not necessarily redefine “equal”; the two expressions may instead be construed as cumulative limitations. On that construction, a delivered manifest representing the same camera-switch timing choices could fall outside the claims merely because its serialization, URIs, bitrate or rendition metadata, device-specific fields, or network-condition fields differ from those of the reconstructed manifest.

That result would not align cleanly with the disclosed detection mechanism. The reconstructed manifest is built from camera-cut time codes detected in the suspected unauthorized distribution. Those detected time codes do not disclose every transport, addressing, rendition, or serialization field that may have appeared in a previously delivered adaptive-streaming manifest.

### Equality-based and functional intrinsic formulations

The intrinsic record contains both equality-based and functional formulations. The PCT preferred manifest embodiment states that retrieval component 140 searches for delivered manifest files that are “equal to” reconstructed manifest files. See [retrieval embodiment](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-list-item-00964) and [original claim 15](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-list-item-01237). Provisional original system claim 1(n), at specification page 32 of the [as-filed provisional record](../../PPA2/as%20filed%2063%20557868.pdf#page=43), uses corresponding equality language.

The filings also contain functional formulations that do not separately require complete-file equality. PCT original claim 1 identifies the distinguishable version that matches the suspected unauthorized distribution, and PCT searching step 290 identifies a manifest having the detected scene changes. Provisional original method claim 10(k), at specification page 33 of the [as-filed provisional record](../../PPA2/as%20filed%2063%20557868.pdf#page=44), searches the ledger to identify the account or accounts associated with the reconstructed manifest file.

These passages establish that “equal to” has literal intrinsic support, but neither filing defines whether that expression requires identity of the complete manifest serialization or correspondence at the level of the represented cut or chunk pattern. The recommended wording therefore does not treat the equality language as erroneous; it asks counsel to select expressly the technical relationship intended for the independent claims.

### Delay direction

The source counsel draft's claims 19 and 35 require, at each selected camera cut, a “later mate camera-switch timing.” They further require extension of the first-source-camera selection from the reference timing to that later timing and commencement of the second-source-camera selection at the later timing. The source abstract is already direction-neutral, stating that mate versions “vary selected camera-cut timings while retaining the same ordered camera transitions.” Source claim 38 likewise uses the direction-neutral expression “different mate camera-cut timing.” The proposed amendments would therefore align source claims 19 and 35 with the source abstract and source claim 38.

The applicant's present recommendation is to make claims 19 and 35 direction-neutral while preserving the complete physical-camera relationship: the same ordered first-source-camera-to-second-source-camera transition, retained source-camera identifiers and order, paired modification of the corresponding out-point and in-point time codes, and an interval between the reference and mate timings in which the reference and mate contain temporally corresponding frames from different source cameras. A bare timing difference, without that structural relationship, is not recommended.

The reviewed prior-art analyses do not rely on delay direction as the patentability distinction. The NA matrix identifies the principal production distinction as movement of the same ordered physical-camera boundary to a noncoincident timing with different-camera frames in the intervening interval, and states that variable timing alone is crowded. See [NA principal distinction](../../US/normal-allowance/prior-art-analysis/AA11393US-NA-prior-art-comparison-matrix_DRAFT.md#ssp-aa11393us-na-prior-art-comparison-matrix-row-00001) and [NA structural relationship](../../US/normal-allowance/prior-art-analysis/AA11393US-NA-prior-art-comparison-matrix_DRAFT.md#ssp-aa11393us-na-prior-art-comparison-matrix-row-00005). The AF matrix likewise states that the retained physical-camera boundary and structured-list operation carry the production-side difference. See [AF timing assessment](../../US/allowance-first/parent/prior-art-analysis/AA11393US-AF-prior-art-comparison-matrix_DRAFT.md#ssp-aa11393us-af-prior-art-comparison-matrix-row-00002). These limited-search conclusions do not establish patentability or eliminate the need to reassess the exact amended claims.

Direction-neutral wording would cover a mate transition that occurs earlier than, as well as one that occurs later than, the corresponding reference transition. “Different from” should be the operative claim expression; “noncoincident” may remain analytical matrix terminology but should not be introduced as a separate claim term. Retaining “later” only in a dependent fallback would preserve the concretely illustrated delay species without making delay direction a limitation of the principal production-to-attribution claims.

### Multi-contributor attribution

Source claims 29 and 30 expressly address a suspected unauthorized distribution assembled from portions of streamed content delivered according to different manifest files, probabilistic identification of contributing recipients, and a segmented Tardos species. Because those claims depend from source claim 19, however, they inherit source claim 19's complete delivered-manifest-to-reconstructed-manifest match. A composite timing-choice sequence assembled from multiple recipients may correspond to no single delivered manifest. In that circumstance, merely retaining source claims 29 and 30 as dependents may preserve the very single-manifest condition that the collusion limitations are intended to overcome.

The applicant regards express multi-contributor attribution and segmented-Tardos processing as required parent coverage. The applicant therefore recommends a standalone multi-contributor method as final independent claim 33 and a segmented-Tardos dependent as final claim 34. The standalone claim should compare the detected timing-choice sequence for respective portions of the suspected unauthorized distribution with recipient-associated manifest sequences without requiring the composite detected sequence to match one delivered manifest at every selected camera cut. It should nevertheless retain the claimed system's specific code structure: recipient-associated manifest sequences composed of chunk selections representing choices between the reference and different mate timings of the same ordered physical-camera transitions, the intervening interval in which reference and mate contain temporally corresponding frames from different source cameras, and an express per-cut determination whether the detected time code represents the reference or mate timing.

The reviewed matrices record substantial pressure against probabilistic collusion attribution and segmented Tardos processing from A2–A4, A6, A9, A19, B6, and C3. They further state that any patentability value remains in the inherited production/reconstruction chain and the exact manifest-sequence-to-portion relationship. See [NA collusion assessment](../../US/normal-allowance/prior-art-analysis/AA11393US-NA-prior-art-comparison-matrix_DRAFT.md#ssp-aa11393us-na-prior-art-comparison-matrix-row-00053) and [AF collusion assessment](../../US/allowance-first/parent/prior-art-analysis/AA11393US-AF-prior-art-comparison-matrix_DRAFT.md#ssp-aa11393us-af-prior-art-comparison-matrix-row-00109). The collusion claims should therefore provide commercially important attack coverage without treating Tardos processing itself as the novelty center.

## Disclosed technical relationships

The cited passages provide the applicant’s present basis for claiming both direction-neutral variation of camera-switch timings and a functional relationship between detectable camera-switch patterns and recipient-associated manifest combinations, rather than demonstrated identity of complete manifest-file byte sequences. Written description, enablement, and priority for each relationship as claimed remain claim-as-a-whole determinations for US counsel.

### PCT disclosure

The PCT provides the following support:

- The mate-generation disclosure applies variations to camera-cut time codes to generate one or more mates. Its real-time metacode expressly alternates between adding and subtracting time, assigns a variation of `1` or `-1`, and applies that variation by `event.timestamp += variation`. See [direction-neutral mate-generation discussion and metacode](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-codeblock-01066). PCT original claim 1 correspondingly recites automatically altering at least one camera-cut timing relative to the reference audio-video content without limiting the alteration to delay. See [original claim 1 mate-generation limitation](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-list-item-01212).
- Example 2 supplies the concrete delayed species: the first-camera selection is extended, the second-camera selection begins later, and synchronization is restored at a subsequent cut. See [Example 2 explanation](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-para-01134). The positive/negative metacode does not separately tabulate an earlier-timing EDL having the complete paired-entry and intervening-interval relationship; counsel should therefore assess the direction-neutral formulation as a claim-as-a-whole and combined-disclosure question.
- The general system identifies which distinguishable version **matches** the suspected unauthorized distribution and searches the association record for the recipient of that matching version. See [general system description](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-list-item-00943) and [original claim 1](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-list-item-01218).
- The preferred manifest embodiment builds one or more reconstructed manifest files from camera-cut time codes detected in the pirate webcast and searches the ledger for the associated user. See [detection and retrieval embodiment](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-list-item-00962).
- The preferred retrieval embodiment and original claim 15 expressly state that the delivered manifest files are “equal to” the reconstructed manifest files. See [retrieval embodiment](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-list-item-00964) and [original claim 15](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-list-item-01237).
- Adaptive-streaming manifests are tailored to devices and network conditions and contain bitrate, resolution, and segment-duration information; the anti-piracy distinction lies in the particular chunks referenced at modified cuts. See [transcoding and manifest disclosure](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-list-item-00958) and [adaptive-streaming explanation](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-para-00966).
- A unique combination of chunks can be matched to the manifest distributed to a spectator or group. See [anti-piracy matching disclosure](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-para-00981).
- The colluding-redistribution disclosure states that multiple pirates may merge segments from distinct delivered versions, that each segment can be traced to its original distribution, and that the ledger and recorded chunk combinations can identify the accounts involved in the collusion. See [colluding-redistribution disclosure](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-para-00994).
- The detection component may use a probabilistic fingerprinting algorithm, preferably Tardos fingerprinting, to identify users who contributed to a composite pirate copy. The segmented-Tardos embodiment applies fingerprints to content segments to localize pirated segments and colluders. See [probabilistic and Tardos disclosure](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-para-00997), [collusion attribution](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-para-00998), and [segmented-Tardos embodiment](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-para-01001). PCT original claim 5 recites use of a probabilistic fingerprinting algorithm. See [original claim 5](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-para-01223).
- The general method searches for a manifest having the detected scene changes, thereby identifying the source of the pirated content. See [method step 290](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-list-item-01029) and [original claim 16](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-list-item-01255).
- Perceptual-hash and fuzzy-matching embodiments identify content matches despite discrepancies, temporal shifts, or alterations. See [fuzzy-matching disclosure](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-para-01059).

The perceptual-hash and fuzzy-matching passages concern detection of corresponding video content and cut timings. They do not independently establish a tolerance, normalization, or partial-match rule for comparing delivered and reconstructed manifest files. The separate colluding-redistribution and Tardos passages provide the asserted basis for portion-level multi-contributor analysis in claims 33 and 34.

The PCT also states that the core principle is the comparison of detectable edit patterns and does not depend on a particular CDN, manifest architecture, segmentation mechanism, or metadata arrangement. See [streaming-architecture independence](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-para-00898). Reliance on this broader manifest-independent passage should be assessed separately for provisional-priority entitlement.

### Provisional disclosure

The specification in the [as-filed provisional record](../../PPA2/as%20filed%2063%20557868.pdf) provides corresponding manifest-based disclosure; the page numbers below are specification page numbers:

- pages 14–15 contain the same real-time mate-generation metacode that alternates between adding and subtracting time, assigns `1` or `-1`, and adds the selected variation to the camera-cut timestamp; in the as-filed PDF these are document pages 25–26;
- pages 16–17 provide the concrete delayed EDL example, including extension of the first camera selection, later commencement of the following camera selection, and subsequent resynchronization;
- pages 4 and 31–32 describe detection of camera-cut time codes, reconstruction of the utilized manifest, ledger searching, and identification of the source account;
- pages 17–18 explain that reference and mate manifests preserve compatible chunk duration while referencing different chunks at altered cuts;
- page 23 states that the unique chunk combination can be matched to a manifest distributed to a particular user or group;
- pages 25–26 describe identifying the specific manifest file or fingerprint derived from the altered cuts, including matches despite minor discrepancies and temporal shifts;
- pages 27–28 describe colluders combining segments from different copies, tracing each segment to its original distribution, using the ledger to identify the accounts involved, Tardos fingerprinting for collusion-secure attribution, and segmented Tardos codes for localizing pirated segments and colluders;
- original system claim 1(n), at page 32, uses the equality-based delivered-manifest and reconstructed-manifest relationship; and
- original system claim 6 recites use of the Tardos fingerprinting algorithm, and original method claim 10(k), at page 33, searches the ledger to identify the account or accounts associated with the reconstructed manifest file without separately reciting complete-file equality.

These provisional passages provide a basis for counsel to evaluate direction-neutral camera-cut variation, manifest-based matching through the represented cut or chunk pattern, and segment-level identification of multiple colluders. The positive/negative metacode expressly discloses both variation directions, while the exact same-ordered-transition, paired-entry, and intervening-different-camera relationship remains a combined-disclosure determination. The standalone relationship in proposed claim 33 among the intervening different-camera interval, per-cut classification of detected time codes as reference or mate timings, recipient-associated manifest sequences, and probabilistic identification of multiple contributors likewise remains a claim-as-a-whole combined-disclosure determination. Original method claim 10(k) does not alone establish the complete cut-by-cut matching relationship recited in the proposed claims and must be read with the manifest, chunk-combination, altered-cut, and recipient-association passages. The provisional does not expressly define “equal” as semantic equivalence, prescribe a normalization algorithm, or state that every possible manifest field must be ignored. Claim language should recite the intended matching relationship directly rather than depend on an unstated special definition of “equal.”

## Recommended independent-claim relationships

The single-recipient independent claims 19, 30, and 35 should state both the direction-neutral physical-camera relationship and cut-by-cut semantic identity at the level of the represented timing choices. They should not rely on a bare timing difference or on “useful for identifying” standing alone, because either would omit the relationship that produces the claimed result. Multi-contributor independent claim 33 should instead recite its positive portion-level probabilistic relationship without importing a complete match to one delivered manifest, while retaining the intervening different-camera interval and expressly classifying each detected cut time code as the reference or mate timing.

### Claims 19 and 35

In the mate-generation step, replace the two delay-specific clauses beginning “a transition” and “in the at least one mate” with:

> a transition from the first source camera to the second source camera occurs at a reference camera-switch timing in the reference audio-video content and at a mate camera-switch timing different from the reference camera-switch timing in at least one of the one or more mates; and
>
> during a temporal interval between the reference camera-switch timing and the mate camera-switch timing, the reference audio-video content and the at least one mate contain temporally corresponding frames captured by different ones of the first and second source cameras;

This formulation covers mate transitions occurring either later or earlier than the reference transition while requiring the same ordered physical-camera transition and the resulting different-camera interval. The preceding claim language should continue to require paired modification of the corresponding out-point and in-point time codes while retaining the first and second source-camera identifiers and their order.

In the manifest-generation step of claim 19, use:

> generate a plurality of manifest files pointing to respective combinations of chunks selected from the ensemble, each respective combination of chunks preserving, for each of the plurality of selected camera cuts, a choice between the reference camera-switch timing and the mate camera-switch timing of that selected camera cut, so that the respective combinations of chunks represent respective combinations of timing choices across the plurality of selected camera cuts;

Use “generating” rather than “generate” in integrated-method claim 35.

Replace the equality-based search limitation with the following relationship, conformed grammatically for the system and method forms:

> search the ledger to identify a recipient associated with a delivered manifest file representing a recipient-associated combination of timing choices, wherein, for each of the plurality of selected camera cuts, the recipient-associated combination and the detected combination represented by the reconstructed manifest file include the same one of the reference camera-switch timing and the mate camera-switch timing for that selected camera cut, and wherein, for at least one of the plurality of selected camera cuts, that same one is the mate camera-switch timing different from the reference camera-switch timing.

For method claim 35, use “searching” rather than “search.”

This wording retains:

- direction-neutral coverage of the mate timing;
- the same ordered physical-camera transition and intervening different-camera interval;
- the delivered-manifest-to-recipient association;
- the affirmative mate-timing requirement;
- the detected combination reconstructed from the suspected distribution; and
- cut-by-cut semantic identity between the represented timing-choice combinations.

It does not require identity of irrelevant manifest syntax or metadata, and it does not introduce “normalized” as an unsupported implementation requirement.

### Final system claims 20–29

Use claim 20 as the delayed-species fallback without adding a claim. Replace claim 20 with:

> 20. (new) The system of claim 19, wherein one of the plurality of selected camera cuts is a delayed selected camera cut for which the mate camera-switch timing is later than the reference camera-switch timing, and wherein the instructions cause the system to preserve, in the mate containing the mate camera-switch timing for the delayed selected camera cut, a timing of a subsequent camera cut from the reference audio-video content, thereby restoring synchronization between that mate and the reference audio-video content from the subsequent camera cut onward.

Omit source claim 21's ten-frame species to create one of the two claim slots required for standalone collusion attribution. Claim 20 retains the broader and more commercially useful delayed-timing and subsequent-resynchronization fallback, while the ten-frame implementation remains disclosed in the specification.

Renumber source claims 22–26 as final claims 21–25, respectively. Retain their substantive limitations, change source claim 26's dependency from source claim 25 to final claim 24, and otherwise conform dependencies to the final numbering. Final claims 24 and 25 therefore retain the system-family perceptual-hash and fuzzy/sliding-window implementations.

Consolidate source claims 27 and 28 as final claim 26, preserving their combined adaptive-delivery and progressive-mixing relationship while creating the second required slot:

> 26. (new) The system of claim 19, wherein the chunks are distributed through a content delivery network using adaptive streaming, the plurality of manifest files is tailored to recipient devices or network conditions, and a mixing process integrates chunks of the reference audio-video content with chunks of the one or more mates and progressively assigns respective manifest files to recipients as additional selected camera cuts become available.

Renumber source claim 31 as final claim 27 without substantive change. Renumber source claim 32 as final claim 28, change its dependency from source claim 31 to final claim 27, and otherwise retain its substantive text.

Use final claim 29 for the corresponding-chunk-selection fallback previously proposed for claim 33:

> 29. (new) The system of claim 19, wherein the delivered manifest file and the reconstructed manifest file identify the same respective chunk selections at corresponding manifest positions associated with the plurality of selected camera cuts.

The source unicast claim 33 remains omitted and should not be moved to another claim unless counsel identifies a separate strategic reason to retain it.

### Final single-recipient monitor-side claims 30–32

Renumber source monitor-side independent claim 38 as final claim 30. Retain its existing direction-neutral “different mate camera-cut timing” terminology and do not introduce a “later” limitation. Remove “that is equal to the reconstructed manifest file” from its ledger-searching step, so that the step identifies a recipient associated with a delivered manifest file, and replace its final relationship with:

> wherein, for each of the plurality of camera cuts, the recipient-associated combination represented by the delivered manifest file and the detected combination represented by the reconstructed manifest file include the same one of the respective reference camera-cut timing and the respective different mate camera-cut timing, and wherein, for at least one of the plurality of camera cuts, that same one is the respective different mate camera-cut timing detected in the suspected unauthorized distribution.

This formulation makes cut-by-cut semantic identity express while retaining the affirmative mate-timing requirement and the monitor-side scope without importing the affirmative production steps of claims 19 and 35.

Add final claim 31 as the monitor-side corresponding-chunk-selection fallback:

> 31. (new) The method of claim 30, wherein the delivered manifest file and the reconstructed manifest file identify the same respective chunk selections at corresponding manifest positions associated with the plurality of camera cuts.

Add final claim 32 as the monitor-side matched-manifest physical-camera-geometry fallback:

> 32. (new) The method of claim 30, wherein the delivered manifest file identifies at least one chunk selected from a mate of the one or more mates, the at least one chunk spans a temporal region of the ensemble containing an ordered transition of one of the plurality of camera cuts, and, during an interval between the respective reference camera-cut timing of that ordered transition and the respective different mate camera-cut timing of that ordered transition in the mate, the reference audio-video content and the mate contain temporally corresponding frames captured by different ones of the respective first and second source cameras.

Final claim 32 carries the physical-camera relationship into the single-recipient monitor-side family as a combined-disclosure fallback; it should not be characterized as requiring the monitoring actor to identify the physical source cameras in the suspected unauthorized distribution.

### Final multi-contributor claims 33–34

Use final claim 33 as a standalone monitor-side method rather than as a dependent from claim 30. This avoids inheriting claim 30's requirement that the detected combination correspond cut-by-cut to one delivered manifest while retaining the physical-camera timing-choice structure as the fingerprint alphabet:

> 33. (new) A method of identifying a plurality of recipients whose respective delivered streamed audio-video content contributed respective portions to a suspected unauthorized distribution of audio-video content, the method comprising:
>
> accessing a ledger comprising associations between a plurality of delivered manifest files and respective recipients, each delivered manifest file identifying a recipient-associated sequence of chunk selections from an ensemble comprising reference audio-video content and one or more mates of the reference audio-video content, the recipient-associated sequence of chunk selections representing a recipient-associated sequence of timing choices across a plurality of selected camera cuts, wherein, for each selected camera cut, each timing choice is a choice between a reference camera-switch timing at which the reference audio-video content contains an ordered transition from a respective first source camera to a respective second source camera and a mate camera-switch timing different from the reference camera-switch timing at which a respective mate of the one or more mates contains the same ordered transition, and wherein, during an interval between the reference camera-switch timing and the mate camera-switch timing, the reference audio-video content and the respective mate contain temporally corresponding frames captured by different ones of the respective first and second source cameras;
>
> receiving the suspected unauthorized distribution;
>
> applying a scene-change detection algorithm to a plurality of temporal portions of the suspected unauthorized distribution to identify respective time codes of camera cuts corresponding to respective ones of the plurality of selected camera cuts;
>
> determining, for each identified time code, whether the corresponding camera cut in the suspected unauthorized distribution occurs at the reference camera-switch timing or the mate camera-switch timing, thereby deriving a detected sequence of timing choices for the plurality of temporal portions;
>
> applying a probabilistic fingerprinting algorithm to the detected sequence and to the recipient-associated sequences represented by the plurality of delivered manifest files; and
>
> identifying, based on an output of the probabilistic fingerprinting algorithm, a plurality of recipients whose delivered streamed audio-video content contributed respective ones of the plurality of temporal portions to the suspected unauthorized distribution.

Use final claim 34 as the segmented-Tardos species:

> 34. (new) The method of claim 33, wherein the probabilistic fingerprinting algorithm comprises a segmented Tardos fingerprinting algorithm that applies respective Tardos fingerprints to content segments corresponding to the plurality of temporal portions and identifies, for respective temporal portions, respective contributing recipients among the plurality of recipients.

Claim 33 does not require its composite detected sequence to equal or semantically match the complete timing-choice sequence of any one delivered manifest. Its positive limitations instead require the same ordered physical-camera transition at different timings and the resulting different-camera interval, per-cut classification of detected time codes as reference or mate timings, probabilistic evaluation of the resulting detected portion sequence against the recipient-associated manifest sequences, and identification of multiple contributing recipients. Claims 33 and 34 require separate claim-as-a-whole determinations for method support, actor attribution, written description, enablement, priority, definiteness, and patentability. The substantial Tardos and traitor-tracing art makes the recited physical-camera timing-choice alphabet, intervening different-camera interval, and manifest-sequence-to-portion relationship essential to their present justification.

### Final integrated-method claims 35–38

Retain claim 35 as the direction-neutral integrated-method independent, conformed to the claim-19 production and manifest-matching language above. Add final claim 36 as its delayed-timing and subsequent-resynchronization fallback:

> 36. (new) The method of claim 35, wherein one of the plurality of selected camera cuts is a delayed selected camera cut for which the mate camera-switch timing is later than the reference camera-switch timing, and wherein generating the one or more mates comprises preserving, in the mate containing the mate camera-switch timing for the delayed selected camera cut, a timing of a subsequent camera cut from the reference audio-video content, thereby restoring synchronization between that mate and the reference audio-video content from the subsequent camera cut onward.

Relocate source claim 36 as final claim 37, retaining its perceptual-hash limitation and dependency from claim 35. Relocate source claim 37 as final claim 38, retaining its fuzzy/sliding-window limitation and changing its dependency from source claim 36 to final claim 37.

Source claims 29 and 30 are replaced by standalone final claims 33 and 34 rather than retained as dependents from claim 19. Source claim 34, overlay before segmentation, remains omitted and reserved. Source claim 21's ten-frame species is omitted, and source claims 27 and 28 are consolidated in final claim 26. The system family retains perceptual-hash and fuzzy/sliding-window limitations in final claims 24 and 25, while the integrated-method family retains the corresponding implementations in final claims 37 and 38.

## Proposed conforming abstract

If counsel adopts the recommended claim wording, replace the abstract in the next counsel revision with:

> **ABSTRACT**
>
> An anti-piracy system generates recipient-associated distinguishable versions of audio-video content. A reference version follows structured edit instructions identifying source cameras and camera-cut time codes. Mate versions retain ordered camera transitions at selected cuts but place the transitions at different timings, producing intervals in which reference and mate versions contain temporally corresponding frames from different cameras. Manifest files select recipient-associated chunk combinations representing reference-or-mate timing choices across the selected cuts, and a ledger associates delivered manifests with recipients. Camera-cut time codes detected in suspected unauthorized content produce a reconstructed manifest representing detected timing choices. The ledger identifies a recipient whose delivered manifest represents the same timing choice at each selected cut, including at least one mate timing. For a composite distribution, probabilistic fingerprinting compares detected timing choices for portions with recipient-associated sequences to identify multiple contributing recipients, and segmented Tardos processing localizes contributions by content segment.

The proposed abstract tracks the direction-neutral physical-camera relationship, the cut-by-cut semantic relationship, the affirmative mate-timing requirement, and multi-contributor segment-level attribution without suggesting byte, syntax, or complete-file identity.

## Required claim-support conforming changes

If counsel adopts the recommended claims, the claim-support statement should make the following changes in the same revision.

First, replace its opening architecture paragraph with:

> The overall architecture recited in new independent claims 19 and 35 is summarized at page 8, lines 9-26, and is described in detail with reference to FIG. 1 at pages 13-15, in particular from page 14, line 2, through page 15. These passages describe the mate creation component 110, the transcoding components 120, the manifest files 121 pointing to unique interleaved combinations of chunks 113 of the ensemble 112, the ledger 122, the detection component 130 running a camera cuts detection algorithm 131 that devises time codes from the pirate webcasting and builds reconstructed manifest files 121′, and the retrieval component 140 searching the ledger to identify the associated spectator or group. The preferred manifest embodiment states that the retrieval component searches for delivered manifest files equal to the reconstructed manifest files 121′. Original claims 1, 10, 11, 14 and 15 recite this architecture in claim form: original claim 1 identifies a distinguishable version matching the suspected unauthorized distribution, while original claim 15 recites the equality-based manifest embodiment. In new claims 19 and 35, each selected camera cut retains the same ordered first-source-camera-to-second-source-camera transition at a mate camera-switch timing different from the reference camera-switch timing, with temporally corresponding frames from different source cameras during the interval between those timings. The searched delivered manifest file is one of the recipient-associated timing-choice manifest files generated, delivered and recorded by the claimed process; for each selected camera cut, its recipient-associated combination and the detected combination represented by the reconstructed manifest file include the same reference or mate camera-switch timing, with at least one mate camera-switch timing different from its corresponding reference timing. This complete chain from production to attribution is disclosed by original claim 1 read with page 12, line 16, through page 13, line 4, by pages 14-16, by original claims 11-15 and 17 and by Examples 1 and 3-5; the same-ordered-transition and different-camera interval are concretely illustrated by Example 2.

The support statement should cite the Example 1 positive/negative metacode expressly: PCT codeblock 01066 and the corresponding provisional specification pages 14–15, appearing at document pages 25–26 of the as-filed provisional PDF. It should distinguish that direction-neutral algorithmic disclosure from Example 2's concrete delayed EDL species and should characterize the complete direction-neutral paired-entry and intervening-interval relationship according to counsel's claim-as-a-whole written-description, enablement, and priority determination.

The support statement should add a separate paragraph for independent claim 33 and dependent claim 34. That paragraph should cite the colluding-redistribution disclosure that portions from different copies remain traceable to their original distributions and that the ledger and recorded chunk combinations identify the accounts involved, together with the probabilistic, Tardos, and segmented-Tardos disclosures. It should also identify the combined support used to connect that collusion processing to the specific recipient-associated sequences of chunk selections representing reference-or-mate timing choices for the same ordered physical-camera transitions, the intervening interval of temporally corresponding different-camera frames, and the per-cut determination from detected time codes whether the suspected distribution represents the reference or mate timing. The paragraph should not state or imply that generic Tardos processing itself supplies the claimed physical-camera timing-choice structure.

Second, delete the sentence stating that unicast delivery is recited in source claim 33. The distribution paragraph may retain the unicast disclosure as background only if relevant elsewhere; it should not attribute that feature to any proposed claim. Conform the same paragraph so that final claim 26 is supported by both the adaptive-CDN and manifest-tailoring passages formerly mapped to source claim 27 and the progressive-mixing and manifest-assignment passages formerly mapped to source claim 28.

Third, in the single-recipient detection-side support paragraph, replace the reference to monitor-side method claim 38 with final monitor-side method claim 30. The paragraph should describe the search as identifying the recipient associated with the delivered manifest representing the same cut-by-cut timing-choice combination, not as an equality search. It should address the multi-contributor operation of claims 33 and 34 separately and should not characterize those claims as requiring a complete match to one delivered manifest.

Fourth, replace the remaining-claims support paragraph so that the perceptual-hash and fuzzy/sliding-window discussion refers to final claims 24, 25, 37, and 38. Replace the support discussion for source claims 29 and 30 with the claim-as-a-whole support analysis for standalone final claims 33 and 34 described above. Delete the support discussion for omitted source claim 34 and the omitted ten-frame source claim 21. Retain the support discussion for final claims 21 and 22 and for the processor-and-memory environment.

Fifth, replace the final dependent-claim support paragraph with:

> New claim 20 is supported by Example 2 at pages 33-35, which illustrates a mate transition later than its corresponding reference transition and restoration of synchronization at a subsequent camera cut. New claim 23 is supported by page 16, lines 1-8, describing further camera cuts spawning additional mates and manifest files, read together with Example 2 at pages 33-35, which provides the concrete single-cut variation at the Cut 2 and Cut 3 boundary. New claim 26 combines the content-delivery-network, adaptive-streaming, device-or-network manifest-tailoring, progressive-mixing, and progressive manifest-assignment operations described at page 8, lines 9-21, page 14, lines 10-21, page 18, line 23, through page 19, line 12, page 29, lines 19-27, and page 40, lines 5-7, and in original claims 11 and 12. New claim 27 is supported by page 15, lines 12-16, which states expressly that the reference and mate manifest files point to sets of chunks of equal duration, together with Example 3 at pages 36-38, which shows the respective manifest files selecting different chunks at corresponding positions. New claim 28 is supported by the corresponding reference and mate chunk positions of Example 3 read together with the source-camera sequence and the different reference and mate switch timings of Example 2. New claims 29 and 31 are supported by the equality-based delivered-manifest and reconstructed-manifest relationship at pages 14-15, the specific chunks referenced at corresponding manifest positions in Example 3 at pages 36-38, and the disclosure at page 19, lines 20-28, that a unique combination of chunks can be matched to a specific manifest file distributed to a particular spectator or group. New claim 32 is supported by the delivered-manifest and mate-chunk disclosure at pages 14-15 and in Example 3, read with Example 2's retained ordered physical-camera transition at different timings and its intervening different-camera frames. New claim 33 is supported by the disclosure at pages 23-26 that colluders combine portions from different copies, that respective portions remain traceable to their original distributions, that the ledger and recorded chunk combinations identify the accounts involved, and that probabilistic Tardos processing identifies users contributing to a composite pirate copy, read with the recipient-associated manifest combinations of pages 14-19, the monitoring and searching operations that detect camera-cut time codes, and Example 2's reference-or-mate timing choices for the same ordered physical-camera transition and its intervening interval of temporally corresponding different-camera frames. New claim 34 is supported by the segmented-Tardos disclosure at pages 25-26, which applies fingerprints to content segments to localize pirated segments and colluders, read with the claim-33 passages. New claim 36 is supported by Example 2 at pages 33-35, which illustrates the later mate transition and restoration of synchronization at a subsequent camera cut in method-compatible production operations. For claims 23, 28, 29, 31, 32, 33, and 34, the recited relationships are shown by the cited passages read together rather than by a single passage.

The support statement should thus disclose the source record's literal equality formulation candidly while characterizing the proposed claims by the express timing-choice and corresponding-chunk relationships they actually recite.

## Claim-set architecture for counsel review

The proposed final topology is:

| Final claims | Family and function | Source or disposition |
| --- | --- | --- |
| 19 | Direction-neutral system independent | Amended source claim 19 |
| 20 | System delayed-timing/resynchronization fallback | Amended source claim 20 |
| 21–25 | System implementation dependents | Renumbered source claims 22–26; source claim 21 omitted |
| 26 | Adaptive CDN, manifest tailoring, and progressive mixing | Consolidated source claims 27 and 28 |
| 27 | Equal-duration corresponding chunks | Renumbered source claim 31 |
| 28 | Physical-camera content of corresponding chunks | Renumbered source claim 32; depends from final claim 27 |
| 29 | Same chunk selections at corresponding manifest positions | System dependent previously proposed as claim 33 |
| 30 | Direction-neutral single-recipient monitor independent | Renumbered and amended source claim 38 |
| 31 | Monitor-side corresponding-chunk-selection fallback | New dependent from final claim 30 |
| 32 | Monitor-side matched-manifest physical-camera geometry | New dependent from final claim 30 |
| 33 | Physical-camera multi-contributor attribution independent | Standalone rearchitecture of source claim 29 without inheriting claim 19's complete-match limitation |
| 34 | Segmented-Tardos contributor-localization fallback | Rearchitected source claim 30; depends from final claim 33 |
| 35 | Direction-neutral integrated-method independent | Amended source claim 35 |
| 36 | Method delayed-timing/resynchronization fallback | New dependent from final claim 35 |
| 37 | Method perceptual-hash fallback | Relocated source claim 36; depends from final claim 35 |
| 38 | Method fuzzy/sliding-window fallback | Relocated source claim 37; depends from final claim 37 |

This topology contains eleven system-family claims, three single-recipient monitor-side method claims, two multi-contributor method claims, four integrated-method claims, four independent claims, and twenty total claims. Each dependent claim is singly dependent. The fourth independent claim is expected to require an excess-independent-claim fee; counsel should confirm entity status, the current fee, and filing instructions.

No byte-for-byte manifest-identity claim is presently recommended. Literal “equal to” language remains in the intrinsic record, but that language does not by itself establish an operative reconstruction process for dynamic addressing, rendition, token, metadata, or serialization fields. The delayed-timing and subsequent-resynchronization species is preserved in system claim 20 and integrated-method claim 36. The corresponding-chunk-selection fallback is preserved in system claim 29 and single-recipient monitor-side claim 31, while monitor-side claim 32 carries the inherited physical-camera geometry into that family.

The exact ten-frame species is omitted from the claim set to accommodate multi-contributor coverage, but its broader delayed/resynchronization relationship remains in claims 20 and 36. Source claims 27 and 28 are preserved as the narrower conjunction recited in final claim 26. Source claims 29 and 30 are not reserved: their collusion-attribution functions are rearchitected as standalone final claims 33 and 34. Source claim 34 remains reserved rather than included in this twenty-claim topology.

The PCT's manifest-independent disclosure may support a separate claim directed to matching a detected camera-switch pattern to a recorded distinguishable version without requiring reconstructed or delivered manifest files. Claim 33 now provides a specific portion-based detection relationship for collusion attribution; a broader partial-detection claim outside that probabilistic multi-contributor context remains a possible alternative only after support and prior-art review. Neither the manifest-independent alternative nor the broader partial-detection alternative has a slot in the proposed twenty-claim topology; adopting either would require a further express reallocation. Because the manifest-independent statement is not expressed with the same breadth in the provisional, that alternative should not be treated as having established provisional-priority support without counsel's specific analysis.

## Conforming package action

The linked counsel-source files remain unchanged. If counsel adopts the direction-neutral, cut-by-cut semantic-identity, multi-contributor, and twenty-claim/four-independent topology recommendations, counsel should create a separate conformed revision of the claims, abstract, and claim-support statement using the exact proposed text and final numbering above. The priority/support analysis, claim-document mapping, prior-art matrix, and counsel-facing claim summary must be conformed in that same claim-set revision. The support statement should not characterize the amended single-recipient operation as an “equality search” or the multi-contributor operation as requiring complete correspondence with one delivered manifest. Every affected prior-art row must be reassessed under the direction-neutral physical-camera, timing-choice, intervening-different-camera, explicit per-cut reference-or-mate classification, corresponding-chunk-selection, single-recipient geometry, probabilistic multi-contributor, segmented-Tardos, consolidated-distribution, and method-resynchronization constructions. The prior-art thesis may remain structurally the same, but the exact amended claims require a current claim-by-claim rescore.

## Questions requiring counsel determination

Counsel should determine before the preliminary amendment is assembled or filed:

1. whether claims 19 and 35 should use a mate camera-switch timing different from the reference timing, together with the same-ordered-transition and intervening-different-camera relationship, instead of requiring only a later mate timing;
2. whether the direction-neutral formulation is adequately described and enabled by each of the PCT and provisional filings and is entitled to the provisional filing date, including whether the positive/negative Example 1 metacode and the delayed Example 2 may support the claimed relationship as a whole;
3. whether claims 20 and 36 provide adequate delayed-timing and subsequent-resynchronization fallbacks after omission of the ten-frame species to accommodate the standalone collusion family;
4. whether removing complete-file equality and claiming cut-by-cut semantic identity between the represented timing-choice combinations preserves the intended novelty and non-obviousness position;
5. whether the recommended manifest-based wording is entitled to the provisional filing date;
6. whether system claim 29 and monitor-side claim 31 provide useful corresponding-chunk-selection fallbacks without creating an impractical adaptive-streaming or infringement construction;
7. whether monitor-side claim 32's mate-chunk and physical-camera geometry is adequately described, enabled, entitled to the provisional filing date, and useful over the reviewed A4, B9, A20, and direct multicamera/EDL art;
8. whether standalone multi-contributor claim 33 adequately avoids the single-delivered-manifest coverage gap while retaining a sufficiently definite and supported relationship among the intervening different-camera interval, per-cut classification of detected time codes as reference or mate timings, detected portion sequence, recipient-associated manifest sequences, and multiple contributing recipients;
9. whether claims 33 and 34 as a whole are adequately described and enabled by each of the PCT and provisional filings, are entitled to the provisional filing date, identify an appropriate single actor, and retain patentable weight over A2–A4, A6, A9, A19, B6, B9, C3, A20, and direct multicamera/EDL art;
10. the applicable excess-independent-claim fee, entity status, filing instructions, and any other procedural consequence of the applicant's four-independent-claim selection;
11. whether counsel identifies any support, patentability, dependency, or prosecution objection to the selected two-slot reallocation—omission of the ten-frame claim and consolidation of source claims 27 and 28 into final claim 26—including whether the resulting adaptive-CDN/progressive-mixing conjunction retains useful scope;
12. whether a broader partial-detection claim outside claim 33's probabilistic multi-contributor context is desirable and supported after claim-as-a-whole and prior-art review, recognizing that it would require further claim reallocation;
13. whether a separate manifest-independent claim is desirable in view of its PCT disclosure and priority posture, likewise recognizing that it would require further claim reallocation; and
14. whether claims 19, 30, 33, and 35 are sufficiently connected in design, operation, and effect through their common recipient-associated use or detection of the same ordered physical-camera transition at reference and different mate timings to remain joined for examination; whether the production, single-recipient detection, multi-contributor detection, and integrated-method formulations nevertheless present a serious search or examination burden supporting restriction; and what election, traversal, rejoinder, or divisional strategy should be used if restriction is required.
