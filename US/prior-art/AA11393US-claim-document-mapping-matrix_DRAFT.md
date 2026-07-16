# AA11393US — Claim–Document Mapping Matrix (DRAFT)

> **INTERNAL COUNSEL ANALYSIS — NOT FOR FILING AND NOT AN ADMISSION.**
>
> This grid records, claim by claim, the degree to which each document stored in this folder was observed — in a limited review at the stated depth — to disclose the corresponding subject matter. Nothing here is an admission that any document is prior art, that any claim is unpatentable, or that any characterization is complete. A **—** cell means *not identified in the limited review*, never *cleared*. Counsel must verify the complete documents before relying on any distinction.

## 1. Scope, versions, and division of labor

- **Claims:** the 30-claim candidate set in `../AA11393US-US_claim-set_DRAFT.md` as of 16.07.2026 (independent claims 1, 9, 16, 22).
- **Documents:** the 19 copies stored in this folder (IDS IDs A1–A9, B1–B9, C8), plus unscored placeholder rows for C3 and C7 (copies outstanding).
- **Division of labor:** `../AA11393US-prior-art-comparison-matrix_DRAFT.md` is the analytic source (feature-level findings, D1 corrections, claim-impact narrative); this file is its claim-level projection; IDS §5 is the counsel-facing summary. On any conflict, the feature matrix governs and this grid gets corrected.
- This grid is valid only for the claim text and inventory state above. Re-scoring triggers are listed in §8.

## 2. Legend and scoring rules

| Symbol | Meaning |
|---|---|
| **Y** | Feature expressly or substantially identified at the stated review depth |
| **P** | Partial or analogous disclosure identified |
| **—** | Not identified in the limited review at the stated depth — *not* a clearance |
| **nr** | Not reviewable at current depth (document not read deeply enough to score either way) |

1. **Independent-claim cells (1, 9, 16, 22) score the whole claim**, with a short basis.
2. **Dependent-claim cells score the added limitation only** (the delta). The whole-claim mapping of a dependent is never better than min(parent cell, delta cell); this rule is stated once here and not repeated.
3. Cell bases use disclosure vocabulary only — never "anticipates", "renders obvious", or "invalidates".
4. Pinpoint citations (page/paragraph) may be added only from a full-text review of the stored copy; several copies are image-only scans not yet read through (see depth column).
5. **B2** is the PCT family publication of A1 and is scored with A1 (single consolidated row) unless a divergent disclosure is found.
6. **C3 (Tardos 2003)** and **C7 (Lin 2008)**: copies outstanding — rows present, unscored. Both are expected to bear on the claims 21/28 deltas per the IDS; score upon receipt.

**Review-depth values** (from `README.md` provenance rows): `full (transcription)` — dossier transcription available and reviewed; `full text` — native text layer reviewed in relevant part; `content-verified` — content verified against Google Patents 16.07.2026; `abstract+face` — bibliographic face and abstract only; `face only` — bibliographic face only; `title+scope` — title/scope pages only.

## 3. Production / mate-generation system (claims 1–8)

Deltas: 2 resync at later cut · 3 ten-frame move · 4 EDL structure · 5 live director cuts · 6 variation at each cut · 7 ML from piracy profiles · 8 overlay of added elements.

| Document (depth) | 1 (indep.) | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| A1 (full, transcription) | **P** — completed-copy retiming (delay/frame rate); no edit list, cameras, or frame substitution | — | — | — | — | P — transformations located at scene changes | — | P — additive arbitrary identifiers/watermarks |
| A2 (content-verified) | — segment versioning; no production stage | — | — | — | — | — | — | P — watermarked segment versions |
| A3 (content-verified) | — segment variations; no production stage | — | — | — | — | — | — | P — marked segment variations |
| A4 (full text) | — distribution-side only | — | — | — | — | — | — | P — dynamic content inserted into streams |
| A5 (content-verified) | — detection technique only | — | — | — | — | — | — | — |
| A6 (abstract+face) | — variant creation method not stated | — | — | — | — | — | nr | nr |
| A7 (abstract+face) | — | — | — | — | — | — | — | P — per-device segment watermarking |
| A8 (abstract+face) | — | — | — | — | — | — | — | nr |
| A9 (abstract+face) | — client-side rendering only | — | — | — | — | — | — | Y — watermark images overlaid via graphic layers/opacity |
| B1 (full, transcription) | — codec-chain provenance only | — | — | — | — | — | — | P — node metadata/watermark insertion |
| B2 | *scored with A1 (PCT family publication)* | | | | | | | |
| B3 (face only) | — | — | — | — | — | — | — | nr |
| B4 (face only) | — | — | — | — | — | — | — | P — visible per-playback fingerprint elements |
| B5 (abstract+face) | — | — | — | — | — | — | — | P — receiver-inserted smart-card-ID watermark |
| B6 (abstract+face) | **P** — per-buyer desynchronizing transforms of finished content | — | — | — | — | P — transforms at hash-selected regions | — | P — embedded per-buyer fingerprint |
| B7 (content-verified) | — comparison technique only | — | — | — | — | — | — | — |
| B8 (full text, 6 pp.) | — uses inherent subtitle timing; generates nothing | — | — | — | — | — | — | — |
| B9 (abstract+face) | **P** — versions from space-desynchronized streams; no cameras | — | — | — | — | — | — | P — watermarks in selected segments |
| C8 (title+scope) | — variant creation out of spec scope | — | — | — | — | — | — | P — A/B watermarked variant creation |
| C3 / C7 | *not scored — copies outstanding* | | | | | | | |

**Production footer.** Closest: A1 and B6 (recipient-distinguishing transformation of completed content); B9 (multi-stream assembly). No stored document was identified disclosing the claim-1 core (edit-list input, camera-cut timecode variation, alternate-camera frame substitution) or the deltas of claims 2–5. Combination watch: A1 + conventional live multi-camera production practice (the §103 theory counsel must test); A1 + B6 (desynchronization vocabulary). Caution: the claim 2/3 fallback additionally carries the provisional Example 2 caveat (see the priority map). The — cells for claim 7 reflect thin support, not strength — the claim set already flags 7/29 as cancellation candidates.

## 4. Distribution / recipient-association system (claims 9–15)

Deltas: 10 CDN/ABR tailoring · 11 mixing + progressive assignment · 12 ledger of end users · 13 blockchain registration · 14 unicast · 15 interleave choice-sequence encoding.

| Document (depth) | 9 (indep.) | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|
| A1 (full, transcription) | **P** — segmentwise transformed copies; ID/random selection; association loop not identified | — | — | — | — | — | P — per-copy variant selection; no camera-cut regions |
| A2 (content-verified) | **P** — segment versions assigned by sequence keys | — | P — key-driven interleave of segment versions | P — key↔player/model assignment | — | — | P — key-encoded version-choice sequence |
| A3 (content-verified) | **P** — segment variations + multilevel assignment | — | P — variant combination per assignment | P — inner/outer code assignment records | — | — | P — code-determined variant sequence |
| A4 (full text) | **P** — manifests select fragment versions per user; no camera-cut origin | Y — CDN/ABR manifests | P — dynamic-content variants | Y — manifest↔user association (anti-piracy) | — | nr | P — playback-option pattern as identifier |
| A5 (content-verified) | — | — | — | — | — | — | — |
| A6 (abstract+face) | **P** — per-request differing segments | nr | nr | nr | — | nr | P — differing-segment sequence per requester |
| A7 (abstract+face) | **P** — device-ID selection at manifest addresses | Y — multi-bitrate published manifest | nr | P — device identifier drives selection | — | nr | P — per-device address-choice pattern |
| A8 (abstract+face) | **P** — variant sequence identifies transmission | P — manifest entries (durations randomized) | nr | nr | — | nr | Y — variant sequence encodes identifying sequence |
| A9 (abstract+face) | — client-side rendering, not delivery | — | nr | nr | — | — | — |
| B1 (full, transcription) | — | — | — | P — codec-chain node records | — | — | — |
| B2 | *scored with A1* | | | | | | |
| B3 (face only) | — | — | — | nr | — | — | — |
| B4 (face only) | P — unique per-playback copies | — | — | P — device/date-time identity in mark | — | — | — |
| B5 (abstract+face) | — broadcast, not per-recipient delivery | — | — | P — smart-card-ID association | — | — | — |
| B6 (abstract+face) | P — per-buyer copies | — | — | P — buyer↔key record | — | — | — |
| B7 (content-verified) | — | — | — | — | — | — | — |
| B8 (full text) | — | — | — | — | — | — | — |
| B9 (abstract+face) | **P** — per-user sequential segment selection across streams | — | P — cross-stream segment mixing | P — user↔fingerprint association | — | — | P — consecutive-choice sequence forms fingerprint |
| C8 (title+scope) | **P** — per-session A/B variant delivery | Y — ABR/CDN architecture | nr | P — session↔recipient resolution | — | nr | Y — session variant sequence encodes identity (spec scope) |
| C3 / C7 | *not scored — copies outstanding* | | | | | | |

**Distribution footer.** Closest single document: A4; densest cluster: A4 + A6/A7/A8 + C8 (per-session segment-variant delivery with recipient association is repeatedly disclosed and standardized). What no document shows: variants *originating as camera-cut timing patterns from multi-camera production* — claim 9's surviving distinction rides on that receive/represent language, not on manifest mechanics. Combination watch: A4+A1; A4+C8; A2/A3+A1. Caution: — cells in columns 10, 13, 14 likely reflect conventionality (CDN, blockchain registration, unicast are routine technologies) rather than patentable distinction; do not treat them as strong fallbacks.

## 5. Detection / recipient-resolution system (claims 16–21)

Deltas: 17 perceptual-hash comparison · 18 sliding-window fuzzy matching · 19 reconstructed manifests from timecodes · 20 ledger search by manifest · 21 collusion / probabilistic attribution.

| Document (depth) | 16 (indep.) | 17 | 18 | 19 | 20 | 21 |
|---|---|---|---|---|---|---|
| A1 (full, transcription) | **P** — identifier/watermark recovery; no camera-source transitions | — | — | — | — | P — collusion-frustrating transformations |
| A2 (content-verified) | **P** — pirate-file key tracing | — | — | — | P — search of key↔player assignments | Y — hybrid traitor tracing of coalitions |
| A3 (content-verified) | **P** — recovered files scored against assignments | — | — | — | P — assignment-record search | Y — multilevel collusion scoring |
| A4 (full text) | **P** — manifest-pattern recovery from a copy | — | — | P — pattern (not timecode) reconstruction | Y — user resolved from manifest record | nr |
| A5 (content-verified) | **P** — suspect/reference comparison; no recipient step | Y — perceptual frame hashes | nr — sliding-window form unconfirmed | — | — | — |
| A6 (abstract+face) | nr — response implies detection; mechanism unstated | nr | nr | nr | nr | nr |
| A7 (abstract+face) | nr — tracing implied, mechanism unstated | nr | nr | nr | nr | nr |
| A8 (abstract+face) | — addresses pirate-side variant detection (obfuscation), not owner-side recovery | nr | nr | nr | nr | — |
| A9 (abstract+face) | nr | nr | nr | — | nr | P — anti-collusion variant policies |
| B1 (full, transcription) | P — codec-chain provenance recovery | — | — | — | — | — |
| B2 | *scored with A1* | | | | | |
| B3 (face only) | P — extracted-watermark comparison against reference | — | — | — | nr | — |
| B4 (face only) | P — visible-mark point-of-piracy identification | — | — | — | — | — |
| B5 (abstract+face) | P — watermark monitoring and alarm | — | — | — | — | — |
| B6 (abstract+face) | P — buyer key-space search on suspect copy | P — multimedia-hash-selected regions | — | — | — | P — collaborator identification |
| B7 (content-verified) | **P** — target/reference shot-order comparison; no recipient step | nr | nr | — | — | — |
| B8 (full text) | **P** — subtitle-timing lookup against database | — | — | — | — | — |
| B9 (abstract+face) | P — fingerprint detection from suspect copy | nr | — | — | nr | nr |
| C8 (title+scope) | P — standardized extraction to session resolution | nr | nr | nr | P — session records | nr |
| C3 / C7 | *not scored — copies outstanding; both expected to bear on column 21* | | | | | |

**Detection footer.** Two distinct clusters: identification *techniques* without recipient resolution (A5, B7, B8 — comparison, shot order, timing lookup) and recipient-resolution *loops* without camera-source-transition structure (A4, A2/A3, B6, C8). No document was identified deriving or matching camera-source transitions with their switch timings at regions where versions select different synchronized camera views — claim 16's operational core. Combination watch: A5/B7 (technique) + A4 or A2/A3 (resolution loop); B8 supplies the temporal-identifier motivation narrative. Columns 17/18/26 are supported implementation detail, not expected to be independently novel (claim-set §4).

## 6. End-to-end method (claims 22–30)

Dependent columns mirror earlier families — **23←2 · 24←9/12 · 25←19+20 · 26←17+18 · 27←14 · 28←21 · 29←7 · 30←8** — and inherit those delta scores unless a deviation is noted here. Only claim 22 (whole end-to-end combination) is scored fresh.

| Document (depth) | 22 (indep.) | Mirror deviations |
|---|---|---|
| A1 (full, transcription) | **P** — closest end-to-end disclosure (ISR X against the PCT claims); lacks camera production and structural recovery | none |
| A2 (content-verified) | P — assign→trace loop over segment versions | none |
| A3 (content-verified) | P — assign→trace loop, multilevel | none |
| A4 (full text) | P — manifest loop with user resolution; no camera-cut production | none |
| A5 (content-verified) | — technique only | none |
| A6 (abstract+face) | P — variant delivery with live response (abstract depth) | none |
| A7 (abstract+face) | P — device-driven variant delivery (abstract depth) | none |
| A8 (abstract+face) | P — variant-sequence identification (abstract depth) | none |
| A9 (abstract+face) | — client watermark rendering only | none |
| B1 (full, transcription) | — provenance metadata only | none |
| B2 | *scored with A1* | |
| B3 (face only) | — monitoring only | none |
| B4 (face only) | P — per-playback mark to point-of-piracy loop | none |
| B5 (abstract+face) | — broadcast monitoring only | none |
| B6 (abstract+face) | P — per-buyer transform to detection loop | none |
| B7 (content-verified) | — comparison technique only | none |
| B8 (full text) | — content identification only | none |
| B9 (abstract+face) | P — per-user assembly to fingerprint-detection loop | none |
| C8 (title+scope) | P — standardized A/B session loop | none |
| C3 / C7 | *not scored — copies outstanding* | |

**Method footer.** The Written Opinion found the PCT claims novel but not inventive; claim 22's exposure is therefore combination-based, principally A1 + the distribution cluster (A4/C8) + detection techniques (A5/B7). Its surviving distinction is the same camera-boundary core as claims 1/9/16 — the 16.07.2026 sweep identified no document disclosing it (limited-search observation, not a clearance).

## 7. Reading the grid — counsel notes

1. The strongest repeated pattern: many documents reach **P** on the independent claims through *marking or assembling otherwise-identical footage*; none was identified reaching the multi-camera boundary mechanism. Every independent claim's distinction currently rests there, consistent with the feature matrix.
2. **nr** density in the A6–A9 rows reflects abstract-depth review only — those four are the newest additions. Full-text reads should be the first depth upgrades, since they sit in the closest distribution cluster.
3. Where a delta column is all **—** (claims 2–5, 13, 19 in part), that means *no identified art at current depth*, but for conventional technologies (13, 14, 10) it more likely signals routineness; distinguish the two cases before relying on a rung.

## 8. Maintenance

Re-score triggers — any of: claim amendment or renumbering; arrival of the Italian search report (C6) or its citations; C3/C7 copies received; any row's review depth upgraded; any new document entering this folder; any feature-matrix correction. Record each pass below.

| Date | Event | Scope of change |
|---|---|---|
| 16.07.2026 | Created; scored against the 16.07.2026 30-claim draft and the 19 stored documents | Initial population: A1/B1/B8 and content-verified rows scored from repo transcriptions and prior verified review; A6–A9, B9 at abstract+face depth; C8 at title+scope depth; C3/C7 unscored |
