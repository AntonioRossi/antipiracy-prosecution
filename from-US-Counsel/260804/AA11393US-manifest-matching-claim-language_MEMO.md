# AA11393US — Manifest Matching Claim-Language Memorandum

> **INTERNAL DRAFT FOR US COUNSEL REVIEW · 6 AUGUST 2026 · NOT FOR FILING**
>
> This memorandum addresses claim-language alignment with the PCT and provisional disclosures. It does not resolve claim construction, written description, priority entitlement, patentability, or filing strategy, which remain for US counsel.

The source claim references in this memorandum are to claims 19–38 in the unchanged 4 August 2026 [`260804-P3366-US new claims 19-38 FINAL CLEAN` counsel draft](260804-P3366-US%20new%20claims%2019-38%20FINAL%20CLEAN.md). The corresponding [abstract](260804-P3366-US%20abstract%20FINAL%20CLEAN.md) and [claim-support statement](260804-P3366-US%20support%20FINAL%20CLEAN.md) also remain unchanged source records. All applicant-proposed changes are stated only in this memorandum for counsel to implement, if adopted, in a separate revision.

## Current drafting issue

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

## Disclosed technical relationship

The cited passages provide the applicant’s present basis for claiming a functional relationship between detectable camera-switch patterns and recipient-associated manifest combinations, rather than demonstrated identity of complete manifest-file byte sequences. Written description, enablement, and priority for the relationship as claimed remain claim-as-a-whole determinations for US counsel.

### PCT disclosure

The PCT provides the following support:

- The general system identifies which distinguishable version **matches** the suspected unauthorized distribution and searches the association record for the recipient of that matching version. See [general system description](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-list-item-00943) and [original claim 1](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-list-item-01218).
- The preferred manifest embodiment builds one or more reconstructed manifest files from camera-cut time codes detected in the pirate webcast and searches the ledger for the associated user. See [detection and retrieval embodiment](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-list-item-00962).
- The preferred retrieval embodiment and original claim 15 expressly state that the delivered manifest files are “equal to” the reconstructed manifest files. See [retrieval embodiment](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-list-item-00964) and [original claim 15](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-list-item-01237).
- Adaptive-streaming manifests are tailored to devices and network conditions and contain bitrate, resolution, and segment-duration information; the anti-piracy distinction lies in the particular chunks referenced at modified cuts. See [transcoding and manifest disclosure](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-list-item-00958) and [adaptive-streaming explanation](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-para-00966).
- A unique combination of chunks can be matched to the manifest distributed to a spectator or group. See [anti-piracy matching disclosure](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-para-00981).
- The general method searches for a manifest having the detected scene changes, thereby identifying the source of the pirated content. See [method step 290](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-list-item-01029) and [original claim 16](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-list-item-01255).
- Perceptual-hash and fuzzy-matching embodiments identify content matches despite discrepancies, temporal shifts, or alterations. See [fuzzy-matching disclosure](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-para-01059).

The perceptual-hash and fuzzy-matching passages concern detection of corresponding video content and cut timings. They do not independently establish a tolerance, normalization, or partial-match rule for comparing delivered and reconstructed manifest files.

The PCT also states that the core principle is the comparison of detectable edit patterns and does not depend on a particular CDN, manifest architecture, segmentation mechanism, or metadata arrangement. See [streaming-architecture independence](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-para-00898). Reliance on this broader manifest-independent passage should be assessed separately for provisional-priority entitlement.

### Provisional disclosure

The specification in the [as-filed provisional record](../../PPA2/as%20filed%2063%20557868.pdf) provides corresponding manifest-based disclosure; the page numbers below are specification page numbers:

- pages 4 and 31–32 describe detection of camera-cut time codes, reconstruction of the utilized manifest, ledger searching, and identification of the source account;
- pages 17–18 explain that reference and mate manifests preserve compatible chunk duration while referencing different chunks at altered cuts;
- page 23 states that the unique chunk combination can be matched to a manifest distributed to a particular user or group;
- pages 25–26 describe identifying the specific manifest file or fingerprint derived from the altered cuts, including matches despite minor discrepancies and temporal shifts;
- original system claim 1(n), at page 32, uses the equality-based delivered-manifest and reconstructed-manifest relationship; and
- original method claim 10(k), at page 33, searches the ledger to identify the account or accounts associated with the reconstructed manifest file without separately reciting complete-file equality.

These provisional passages provide a basis for counsel to evaluate manifest-based matching through the represented cut or chunk pattern. Original method claim 10(k) does not alone establish the complete cut-by-cut relationship recited in the proposed claims and must be read with the manifest, chunk-combination, altered-cut, and recipient-association passages. The provisional does not expressly define “equal” as semantic equivalence, prescribe a normalization algorithm, or state that every possible manifest field must be ignored. Claim language should recite the intended matching relationship directly rather than depend on an unstated special definition of “equal.”

## Recommended independent-claim relationship

The independent claims should state cut-by-cut semantic identity at the level of the represented timing choices. They should not rely on “useful for identifying” standing alone, because that would state a desired result without defining the relationship that produces it.

### Claims 19 and 35

Replace the equality-based search limitation with the following relationship, conformed grammatically for the system and method forms:

> search the ledger to identify a recipient associated with a delivered manifest file representing a recipient-associated combination of timing choices, wherein, for each of the plurality of selected camera cuts, the recipient-associated combination and the detected combination represented by the reconstructed manifest file include the same one of the reference camera-switch timing and the later mate camera-switch timing for that selected camera cut, and wherein, for at least one of the plurality of selected camera cuts, that same one is the later mate camera-switch timing.

For method claim 35, use “searching” rather than “search.”

This wording retains:

- the delivered-manifest-to-recipient association;
- the affirmative mate-timing requirement;
- the detected combination reconstructed from the suspected distribution; and
- cut-by-cut semantic identity between the represented timing-choice combinations.

It does not require identity of irrelevant manifest syntax or metadata, and it does not introduce “normalized” as an unsupported implementation requirement.

### Claim 38

Remove “that is equal to the reconstructed manifest file” from the ledger-searching step and replace the final relationship with:

> wherein, for each of the plurality of camera cuts, the recipient-associated combination represented by the delivered manifest file and the detected combination represented by the reconstructed manifest file include the same one of the respective reference camera-cut timing and the respective different mate camera-cut timing, and wherein, for at least one of the plurality of camera cuts, that same one is the respective different mate camera-cut timing detected in the suspected unauthorized distribution.

This formulation makes cut-by-cut semantic identity express while retaining the affirmative mate-timing requirement and the monitor-side scope of claim 38 without importing the affirmative production steps of claims 19 and 35.

### Claim 33

Delete the current unicast limitation in claim 33 and replace claim 33 in its entirety with:

> 33. (new) The system of claim 19, wherein the delivered manifest file and the reconstructed manifest file identify the same respective chunk selections at corresponding manifest positions associated with the plurality of selected camera cuts.

This is a one-for-one substitution, not an additional claim. Claims 19–38 therefore remain a twenty-claim set with three independent claims. The unicast limitation should not be moved to another claim unless counsel identifies a separate strategic reason to retain it.

## Proposed conforming abstract

If counsel adopts the recommended claim wording, replace the abstract in the next counsel revision with:

> **ABSTRACT**
>
> An anti-piracy system generates recipient-associated distinguishable versions of audio-video content. A reference version is produced from structured edit instructions identifying source cameras and camera-cut time codes. Mate versions vary selected camera-cut timings while retaining the ordered camera transitions. The versions are segmented into chunks, and manifest files select recipient-associated chunk combinations, each representing, for each selected camera cut, a choice between the reference timing and a later mate timing. A ledger associates delivered manifest files with recipients. For suspected unauthorized content, camera-cut time codes are detected and used to build a reconstructed manifest file representing detected timing choices across the selected camera cuts. The ledger is searched for a delivered manifest file representing, for each selected camera cut, the same timing choice represented by the reconstructed manifest file and including at least one later mate timing, thereby identifying the associated recipient.

The proposed abstract tracks the cut-by-cut semantic relationship and the affirmative mate-timing requirement without suggesting byte, syntax, or complete-file identity.

## Required claim-support conforming changes

If counsel adopts the recommended claims, the claim-support statement should make the following changes in the same revision.

First, replace its opening architecture paragraph with:

> The overall architecture recited in new independent claims 19 and 35 is summarized at page 8, lines 9-26, and is described in detail with reference to FIG. 1 at pages 13-15, in particular from page 14, line 2, through page 15. These passages describe the mate creation component 110, the transcoding components 120, the manifest files 121 pointing to unique interleaved combinations of chunks 113 of the ensemble 112, the ledger 122, the detection component 130 running a camera cuts detection algorithm 131 that devises time codes from the pirate webcasting and builds reconstructed manifest files 121′, and the retrieval component 140 searching the ledger to identify the associated spectator or group. The preferred manifest embodiment states that the retrieval component searches for delivered manifest files equal to the reconstructed manifest files 121′. Original claims 1, 10, 11, 14 and 15 recite this architecture in claim form: original claim 1 identifies a distinguishable version matching the suspected unauthorized distribution, while original claim 15 recites the equality-based manifest embodiment. In new claims 19 and 35, the searched delivered manifest file is one of the recipient-associated timing-choice manifest files generated, delivered and recorded by the claimed process; for each selected camera cut, its recipient-associated combination and the detected combination represented by the reconstructed manifest file include the same reference or later mate camera-switch timing, with at least one later mate camera-switch timing. This complete chain from production to attribution is disclosed by original claim 1 read with page 12, line 16, through page 13, line 4, by pages 14-16, by original claims 11-15 and 17 and by Examples 3-5.

Second, delete the sentence stating that unicast delivery is recited in claim 33. The remaining distribution paragraph may retain the unicast disclosure as background only if it is relevant elsewhere; it should not attribute that feature to proposed claim 33.

Third, replace the final dependent-claim support paragraph with:

> New claim 24 is supported by page 16, lines 1-8, describing further camera cuts spawning additional mates and manifest files, read together with Example 2 at pages 33-35, which provides the concrete single-cut variation at the Cut 2 and Cut 3 boundary. New claim 31 is supported by page 15, lines 12-16, which states expressly that the reference and mate manifest files point to sets of chunks of equal duration, together with Example 3 at pages 36-38, which shows the respective manifest files selecting different chunks at corresponding positions. New claim 32 is supported by the corresponding reference and mate chunk positions of Example 3 read together with the source camera sequence and the different reference and mate switch timings of Example 2. New claim 33 is supported by the equality-based delivered-manifest and reconstructed-manifest relationship at pages 14-15, the specific chunks referenced at corresponding manifest positions in Example 3 at pages 36-38, and the disclosure at page 19, lines 20-28, that a unique combination of chunks can be matched to a specific manifest file distributed to a particular spectator or group. For claims 24, 32 and 33 the recited relationships are shown by the cited passages read together rather than by a single passage.

The support statement should thus disclose the source record's literal equality formulation candidly while characterizing the proposed claims by the narrower technical relationship they actually recite.

## Claim-set architecture for counsel review

The present claim set should use:

1. an independent cut-by-cut semantic-identity limitation at the level of the represented timing choices;
2. replacement claim 33 as a dependent fallback requiring the delivered and reconstructed manifest files to identify the same respective chunk selections at corresponding manifest positions; and
3. a separate partial-detection claim only if counsel confirms its written-description, enablement, priority, and prior-art posture.

No byte-for-byte manifest-identity claim is presently recommended. Literal “equal to” language remains in the intrinsic record, but that language does not by itself establish an operative reconstruction process for dynamic addressing, rendition, token, metadata, or serialization fields. Within the current twenty-claim, three-independent-claim allocation, the current unicast claim 33 should be replaced by the corresponding-chunk-selection fallback quoted above.

The PCT's manifest-independent disclosure may support a separate claim directed to matching a detected camera-switch pattern to a recorded distinguishable version without requiring reconstructed or delivered manifest files. Because the corresponding manifest-independent statement is not expressed with the same breadth in the provisional, that alternative should not be treated as having established provisional-priority support without counsel's specific analysis.

## Conforming package action

The linked counsel-source files remain unchanged. If counsel adopts the cut-by-cut semantic-identity wording, counsel should create a separate conformed revision of the claims, abstract, and claim-support statement using the exact proposed text above. The priority/support analysis, claim-document mapping, prior-art matrix, and counsel-facing claim summary must be conformed in that same claim-set revision. The support statement should not characterize the amended operation as an “equality search,” and every affected prior-art row must be reassessed under the timing-choice and corresponding-chunk-selection constructions.

## Questions requiring counsel determination

Counsel should determine before the preliminary amendment is assembled or filed:

1. whether removing complete-file equality and claiming cut-by-cut semantic identity between the represented timing-choice combinations preserves the intended novelty and non-obviousness position;
2. whether the recommended manifest-based wording is entitled to the provisional filing date;
3. whether claim 33's corresponding-chunk-selection limitation provides a useful narrower fallback;
4. whether a separate partial-detection claim is desirable and supported after claim-as-a-whole and prior-art review; and
5. whether a separate manifest-independent claim is desirable in view of its PCT disclosure and priority posture.
