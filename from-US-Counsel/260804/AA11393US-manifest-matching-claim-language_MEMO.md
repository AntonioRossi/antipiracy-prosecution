# AA11393US — Manifest Matching Claim-Language Memorandum

> **INTERNAL DRAFT FOR US COUNSEL REVIEW · 5 AUGUST 2026 · NOT FOR FILING**
>
> This memorandum addresses claim-language alignment with the PCT and provisional disclosures. It does not resolve claim construction, written description, priority entitlement, patentability, or filing strategy, which remain for US counsel.

## Current drafting issue

Claims 19, 35, and 38 presently require a delivered manifest file to be “equal to” a reconstructed manifest file. The intrinsic disclosure does not state whether “equal” means:

- byte-for-byte file identity;
- syntactic or structural identity;
- identity of referenced chunk selections; or
- a match between the camera-switch timing choices represented by the two manifests.

The claims additionally require the delivered manifest to match or represent the same detected combination. That additional functional relationship does not necessarily redefine “equal”; the two expressions may instead be construed as cumulative limitations. On that construction, a delivered manifest representing the same camera-switch timing choices could fall outside the claims merely because its serialization, URIs, bitrate or rendition metadata, device-specific fields, or network-condition fields differ from those of the reconstructed manifest.

That result would not align cleanly with the disclosed detection mechanism. The reconstructed manifest is built from camera-cut time codes detected in the suspected unauthorized distribution. Those detected time codes do not disclose every transport, addressing, rendition, or serialization field that may have appeared in a previously delivered adaptive-streaming manifest.

## Disclosed technical relationship

The common supported relationship is functional matching based on detectable camera-switch patterns and their association with a recipient, rather than demonstrated identity of two complete manifest-file byte sequences.

### PCT disclosure

The PCT provides the following support:

- The general system identifies which distinguishable version **matches** the suspected unauthorized distribution and searches the association record for the recipient of that matching version. See [general system description](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-list-item-00943) and [original claim 1](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-list-item-01218).
- The preferred manifest embodiment builds one or more reconstructed manifest files from camera-cut time codes detected in the pirate webcast and searches the ledger for the associated user. See [detection and retrieval embodiment](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-list-item-00962).
- Adaptive-streaming manifests are tailored to devices and network conditions and contain bitrate, resolution, and segment-duration information; the anti-piracy distinction lies in the particular chunks referenced at modified cuts. See [transcoding and manifest disclosure](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-list-item-00958) and [adaptive-streaming explanation](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-para-00966).
- A unique combination of chunks can be matched to the manifest distributed to a spectator or group. See [anti-piracy matching disclosure](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-para-00981).
- The general method searches for a manifest having the detected scene changes, thereby identifying the source of the pirated content. See [method step 290](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-list-item-01029) and [original claim 16](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-list-item-01255).
- Perceptual-hash and fuzzy-matching embodiments identify content matches despite discrepancies, temporal shifts, or alterations. See [fuzzy-matching disclosure](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-para-01059).

The PCT also states that the core principle is the comparison of detectable edit patterns and does not depend on a particular CDN, manifest architecture, segmentation mechanism, or metadata arrangement. See [streaming-architecture independence](../../PCT/structured-source/as-filed-dossier/AA11393US-PCT_RAPPORTO_DEPOSITO.md#ssp-pct-as-filed-dossier-para-00898). Reliance on this broader manifest-independent passage should be assessed separately for provisional-priority entitlement.

### Provisional disclosure

The [provisional specification](../../PPA2/AI-Driven%20Content%20Differentiation%20and%20Piracy%20Traceability%20System%20and%20Methods%20for%20Streaming%20Media.pdf) provides corresponding manifest-based support:

- pages 4 and 31–32 describe detection of camera-cut time codes, reconstruction of the utilized manifest, ledger searching, and identification of the source account;
- pages 17–18 explain that reference and mate manifests preserve compatible chunk duration while referencing different chunks at altered cuts;
- page 23 states that the unique chunk combination can be matched to a manifest distributed to a particular user or group;
- pages 25–26 describe identifying the specific manifest file or fingerprint derived from the altered cuts, including matches despite minor discrepancies and temporal shifts; and
- the original claims combine manifests tailored to device and network conditions with reconstruction from detected camera-cut time codes and source-account identification.

The provisional therefore supports manifest-based matching through the represented cut or chunk pattern. It does not expressly define “equal” as semantic equivalence, prescribe a normalization algorithm, or state that every possible manifest field must be ignored. Claim language should recite the supported matching relationship directly rather than depend on an unstated special definition of “equal.”

## Recommended independent-claim relationship

The independent claims should state the objective technical match directly. They should not rely on “useful for identifying” standing alone, because that would state a desired result without defining the relationship that produces it.

### Claims 19 and 35

Replace the equality-based search limitation with the following relationship, conformed grammatically for the system and method forms:

> search the ledger to identify a recipient associated with a delivered manifest file representing a recipient-associated combination of timing choices that (i) includes at least one of the later mate camera-switch timings and (ii) matches the detected combination represented by the reconstructed manifest file.

For method claim 35, use “searching” rather than “search.”

This wording retains:

- the delivered-manifest-to-recipient association;
- the affirmative mate-timing requirement;
- the detected combination reconstructed from the suspected distribution; and
- an objective match between the represented timing-choice combinations.

It does not require identity of irrelevant manifest syntax or metadata, and it does not introduce “normalized” as an unsupported implementation requirement.

### Claim 38

Replace the equality-based search relationship with:

> searching a ledger comprising associations between a plurality of delivered manifest files and respective recipients to identify a recipient associated with a delivered manifest file representing a combination of camera-cut timings that matches the detected combination represented by the reconstructed manifest file,

and retain an express limitation that the detected combination includes, for at least one camera cut, the respective different mate camera-cut timing detected in the suspected unauthorized distribution.

This formulation ties attribution to the detected timing pattern without importing the production-side limitations of claims 19 and 35.

## Claim-set architecture for counsel review

A robust claim set may use:

1. an independent timing-combination matching limitation supported by both the PCT and provisional;
2. a dependent fallback directed to matching corresponding chunk selections or positions; and
3. if useful after priority and prior-art review, a narrower dependent fallback requiring a stricter form of manifest identity.

The PCT's manifest-independent disclosure may support a separate claim directed to matching a detected camera-switch pattern to a recorded distinguishable version without requiring reconstructed or delivered manifest files. Because the corresponding manifest-independent statement is not expressed with the same breadth in the provisional, that alternative should not be treated as having established provisional-priority support without counsel's specific analysis.

## Questions requiring counsel determination

Counsel should determine before the preliminary amendment is assembled or filed:

1. whether removing “equal” and claiming the timing-combination match preserves the intended novelty and non-obviousness position;
2. whether the recommended manifest-based wording is entitled to the provisional filing date;
3. whether a corresponding-chunk-selection dependent claim provides a useful narrower fallback;
4. whether any stricter identity limitation should be retained only in a dependent claim; and
5. whether a separate manifest-independent claim is desirable in view of its PCT disclosure and priority posture.
