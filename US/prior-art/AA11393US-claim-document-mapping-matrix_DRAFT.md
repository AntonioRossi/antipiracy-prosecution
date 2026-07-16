# AA11393US — Claim–Document Mapping Matrix (DRAFT)

> **INTERNAL COUNSEL ANALYSIS — NOT FOR FILING AND NOT AN ADMISSION.**
>
> This grid records, claim by claim, the degree to which each document stored in this folder was observed — in a limited review at the stated depth — to disclose the corresponding subject matter. Nothing here is an admission that any document is prior art, that any claim is unpatentable, or that any characterization is complete. A **—** cell means *not identified in the limited review*, never *cleared*. Counsel must verify the complete documents before relying on any distinction.

## 1. Scope, versions, and division of labor

- **Claims:** the 30-claim candidate set in `../AA11393US-US_claim-set_DRAFT.md` as of 16.07.2026 (independent claims 1, 9, 16, 22).
- **Documents:** the 20 copies stored in this folder (IDS IDs A1–A10, B1–B9, C8), plus unscored placeholder rows for C3 and C7 (copies outstanding). Full text for all 20 is in `markdown/` — score against those transcriptions, and confirm any passage relied on against the source PDF.
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
4. Pinpoint citations (page/paragraph) may be added only from a full-text review of the stored copy; several copies are image-only scans whose transcriptions are OCR (see `markdown/README.md`) — **verify every quotation against the source PDF**.
5. **B2** is the PCT family publication of A1 and is scored with A1 (single consolidated row); equivalence was confirmed against B2's full text 16.07.2026 (no divergent disclosure identified; zero camera mentions). B2's ISR (pp. 47–48 of the stored copy) is transcribed and mined — see §7 note 4.
6. **C3 (Tardos 2003)** and **C7 (Lin 2008)**: copies outstanding — rows present, unscored. **C7's priority is raised:** the B2 ISR rated it category X against D1's own PCT claims 1–17 and 19–30 (§7 note 4).

**Review-depth values.** The depth recorded against each row is the depth *at which that row's cells were actually scored*. The 16.07.2026 full-text re-score (§8 log) has been executed: every previously sub-full-text row was re-scored against its `markdown/` transcription, resolving all former `nr` cells. Depth values now in use:

- `full (transcription)` — dossier transcription reviewed (A1, B1);
- `full text` / `full text/OCR (re-scored 16.07.2026)` — cells scored against the complete transcription, via targeted claim-term reads;
- `full text (confirmed 16.07.2026)` — earlier content-verified scoring spot-checked against the transcription with no changes required;
- `full text (targeted read 16.07.2026)` — A10 only: ISA-pinpointed passages and claim-relevant sections read; a sequential full read remains open.

Remaining depth work: score C3/C7 upon receipt of copies; A10 sequential read; pinpoint verification against PDFs whenever a passage is quoted.

## 3. Production / mate-generation system (claims 1–8)

Deltas: 2 resync at later cut · 3 ten-frame move · 4 EDL structure · 5 live director cuts · 6 variation at each cut · 7 ML from piracy profiles · 8 overlay of added elements.

| Document (depth) | 1 (indep.) | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| A1 (full, transcription) | **P** — completed-copy retiming (delay/frame rate); no edit list, cameras, or frame substitution | — | — | — | — | P — transformations located at scene changes | — | P — additive arbitrary identifiers/watermarks |
| A2 (full text, confirmed 16.07.2026) | — segment versioning; no production stage | — | — | — | — | — | — | P — watermarked segment versions |
| A3 (full text, confirmed 16.07.2026) | — segment variations; no production stage | — | — | — | — | — | — | P — marked segment variations |
| A4 (full text, re-scored 16.07.2026) | **P** — alternative fragment versions "may differ in camera perspective" for a duration; creation mechanism, edit lists, and boundary movement absent | — | — | — | — | — | — | Y — fragment versions may include overlays / censored blackout frames; overlay-borne version information |
| A5 (full text, confirmed 16.07.2026) | — detection technique only | — | — | — | — | — | — | — |
| A6 (full text, re-scored 16.07.2026) | — variant creation method not stated | — | — | — | — | — | — | P — forensic marks embedded in served segment versions |
| A7 (full text, re-scored 16.07.2026) | — | — | — | — | — | — | — | P — per-device selection among pre-watermarked segment versions |
| A8 (full text, re-scored 16.07.2026) | — | — | — | — | — | — | P — generic ML/AI boilerplate ([0089]); not piracy-profile-driven | — variants padded/duration-shifted; no AV overlay identified |
| A9 (full text, re-scored 16.07.2026) | — client-side rendering only | — | — | — | — | — | — | Y — watermark images overlaid via graphic layers/opacity |
| A10 (full text, targeted read 16.07.2026) | — rendering-device embedding only | — | — | — | — | — | — | P — time-varying full-frame colour modulation carries device ID |
| B1 (full, transcription) | — codec-chain provenance only | — | — | — | — | — | — | P — node metadata/watermark insertion |
| B2 | *scored with A1 (family; equivalence confirmed against full text 16.07.2026)* | | | | | | | |
| B3 (full text/OCR, re-scored 16.07.2026) | — | — | — | — | — | — | — | — embedding locus implied at head-end; not elaborated |
| B4 (full text/OCR, re-scored 16.07.2026) | — | — | — | — | — | — | — | P — visible per-playback fingerprint elements |
| B5 (full text/OCR, re-scored 16.07.2026) | — | — | — | — | — | — | — | P — receiver-inserted smart-card-ID watermark |
| B6 (full text/OCR, re-scored 16.07.2026) | **P** — per-buyer desynchronizing transforms of finished content | — | — | — | — | P — transforms at hash-selected regions | — | P — embedded per-buyer fingerprint |
| B7 (full text, confirmed 16.07.2026) | — comparison technique only; a shot is defined as frames from a single camera | — | — | — | — | — | — | — |
| B8 (full text) | — uses inherent subtitle timing; generates nothing | — | — | — | — | — | — | — |
| B9 (full text/OCR, re-scored 16.07.2026) | **P** — versions from space-desynchronized streams; no cameras | — | — | — | — | — | — | P — watermarks in selected segments |
| C8 (full text, re-scored 16.07.2026) | — variant creation out of spec scope | — | — | — | — | — | — | P — A/B watermarked variant creation |
| C3 / C7 | *not scored — copies outstanding* | | | | | | | |

**Production footer.** Closest: A1 and B6 (recipient-distinguishing transformation of completed content); B9 (multi-stream assembly at fixed exchange points). **Full-text finding 16.07.2026: A4 expressly contemplates fragment versions differing by camera perspective** — but only as pre-existing alternative versions; no multi-camera capture, no edit list, no boundary movement, and no switch-timing creation. No stored document was identified disclosing the claim-1 core (edit-list input, camera-cut timecode variation, alternate-camera frame substitution) or the deltas of claims 2–5. Combination watch: A1 + conventional live multi-camera production practice; A1 + B6; now also A1 + A4 (camera-perspective versions). Caution: the claim 2/3 fallback additionally carries the provisional Example 2 caveat (see the priority map). The claim-7 column reflects thin support and generic-AI boilerplate in the art (A8), not strength — the claim set already flags 7/29 as cancellation candidates.

## 4. Distribution / recipient-association system (claims 9–15)

Deltas: 10 CDN/ABR tailoring · 11 mixing + progressive assignment · 12 ledger of end users · 13 blockchain registration · 14 unicast · 15 interleave choice-sequence encoding.

| Document (depth) | 9 (indep.) | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|
| A1 (full, transcription) | **P** — segmentwise transformed copies; ID/random selection; association loop not identified | — | — | — | — | — | P — per-copy variant selection; no camera-cut regions |
| A2 (full text, confirmed 16.07.2026) | **P** — segment versions assigned by sequence keys | — | P — key-driven interleave of segment versions | P — key↔player/model assignment | — | — | P — key-encoded version-choice sequence |
| A3 (full text, confirmed 16.07.2026) | **P** — segment variations + multilevel assignment | — | P — variant combination per assignment | P — inner/outer code assignment records | — | — | P — code-determined variant sequence |
| A4 (full text, re-scored 16.07.2026) | **P** — manifests select fragment versions per user; versions may differ in camera perspective per duration; cut-timing variation absent | Y — CDN/ABR manifests | P — server/edge per-request redirect to the variant required by the stored per-user manifest | Y — manifest↔user association (anti-piracy) | — | — searched; not identified | Y — per-duration version-choice pattern encodes user ID, including at perspective-differing durations |
| A5 (full text, confirmed 16.07.2026) | — | — | — | — | — | — | — |
| A6 (full text, re-scored 16.07.2026) | **P** — per-request segment versions; unique served sequence identifies the requesting device | P — CDN + ABR expressly; tailored manifests not identified | — | P — marks/served sequence tied to device credential; stored ledger not identified | — | Y — "uni-cast channel" expressly an option to effect delivery | Y — unique served-version sequence identifies the requesting device |
| A7 (full text, re-scored 16.07.2026) | **P** — device-ID selection at addresses from a published manifest | P — CDN + ABR; deliberately **common (untailored) manifest** | — | P — watermark sequence associated with the request device | — | — | P — per-device address/watermark sequence |
| A8 (full text, re-scored 16.07.2026) | **P** — variant sequence identifies transmission | P — edge/CDN caching; ABR not identified | — | — | — | Y — edge streaming expressly "unicast, multicast" | Y — variant sequence encodes identifying sequence |
| A9 (full text, re-scored 16.07.2026) | — client-side rendering, not delivery | — | — | P — policies datastore records per-client watermark policies/IDs | — | — | — |
| A10 (full text, targeted read 16.07.2026) | — embedding at rendering, not delivery-side versioning | — | — | P — device identity carried in the rendering-time mark itself | — | — | — |
| B1 (full, transcription) | — | — | — | P — codec-chain node records | — | — | — |
| B2 | *scored with A1* | | | | | | |
| B3 (full text/OCR, re-scored 16.07.2026) | — | — | — | — searched; watermark encodes source identity directly | — | — | — |
| B4 (full text/OCR, re-scored 16.07.2026) | P — unique per-playback copies | — | — | P — device/date-time identity in mark | — | — | — |
| B5 (full text/OCR, re-scored 16.07.2026) | — broadcast, not per-recipient delivery | — | — | P — smart-card-ID association | — | — | — |
| B6 (full text/OCR, re-scored 16.07.2026) | P — per-buyer copies | — | — | P — buyer↔key record | — | — | — |
| B7 (full text, confirmed 16.07.2026) | — | — | — | — | — | — | — |
| B8 (full text) | — | — | — | — | — | — | — |
| B9 (full text/OCR, re-scored 16.07.2026) | **P** — per-user sequential segment selection across desynchronized streams at predefined **exchangeable time points** (random access points; chosen to hide switching) | — | P — cross-stream segment mixing at exchange points | P — per-user ID/key association (unique per receiver) | — | P — user IDs/keys expressly unicasted; content broadcast/multicast | P — per-user choice sequence at fixed exchange points forms the fingerprint |
| C8 (full text, re-scored 16.07.2026) | **P** — per-session A/B variant delivery | Y — ABR/CDN architecture (DASH/HLS) | P — sequencer returns the Variant per request based on a watermark token | P — WM pattern is context-dependent: a device, account, or session identifier | — | — searched; not identified | Y — session variant sequence encodes identity |
| C3 / C7 | *not scored — copies outstanding* | | | | | | |

**Distribution footer.** Closest single document: **A4, now by a wider margin** — per-user manifests, edge redirect sequencing, camera-perspective fragment versions, and user resolution in one reference; densest cluster: A4 + A6/A7/A8 + C8. What no document shows: variants whose *camera-cut timings* differ — every reference either swaps what fills a fixed temporal slot (A4 perspectives, B9 exchange points, C8 A/B variants) or marks identical footage; the cut-position grid is never the per-recipient variable. Claim 9's surviving distinction rides on the versions "differing by a pattern of timings of camera cuts," not on manifest mechanics. Combination watch: A4+A1; A4+C8; A2/A3+A1. Caution: columns 10/13/14 are conventional delivery technology — A6/A8 expressly name unicast and A4/C8 the CDN/ABR stack; do not treat 10/13/14 as distinctions.

## 5. Detection / recipient-resolution system (claims 16–21)

Deltas: 17 perceptual-hash comparison · 18 sliding-window fuzzy matching · 19 reconstructed manifests from timecodes · 20 ledger search by manifest · 21 collusion / probabilistic attribution.

| Document (depth) | 16 (indep.) | 17 | 18 | 19 | 20 | 21 |
|---|---|---|---|---|---|---|
| A1 (full, transcription) | **P** — identifier/watermark recovery; no camera-source transitions | — | — | — | — | P — collusion-frustrating transformations |
| A2 (full text, confirmed 16.07.2026) | **P** — pirate-file key tracing | — | — | — | P — search of key↔player assignments | Y — hybrid traitor tracing of coalitions |
| A3 (full text, confirmed 16.07.2026) | **P** — recovered files scored against assignments | — | — | — | P — assignment-record search | Y — multilevel collusion scoring (score → coalition probability) |
| A4 (full text, re-scored 16.07.2026) | **P** — manifest-pattern recovery from a copy; **correlation identifies which camera perspective a duration contains**; switch timings not derived | — frame-difference/correlation, not hashing | — | P — pattern (not timecode) reconstruction; abridged manifest data narrows the compared durations | Y — user resolved from stored customized-manifest record | Y — colluding users identified via duration-group assignment; probabilistic version-pattern estimation under collusion |
| A5 (full text, confirmed 16.07.2026) | **P** — suspect/reference comparison; no recipient step | Y — perceptual frame hashes | P — minimum hash-distance series over key-frame sets; express sliding window not identified | — | — | — |
| A6 (full text, re-scored 16.07.2026) | **P** — real-time forensic-mark detection from the pirated broadcast resolves the requesting device; response actions (revocation, entitlement termination) | — | — | — | — | Y — colluders identified deterministically (designed codes) or **probabilistically** (pseudorandom distinguishable events) ([0126]) |
| A7 (full text, re-scored 16.07.2026) | **P** — copies traced to the receiving device via the embedded watermark sequence | — | — | — | — | P — collusion attacks addressed; common manifest thwarts manifest-level collusion; attribution algorithm not identified |
| A8 (full text, re-scored 16.07.2026) | — obfuscation against pirate-side variant detection; owner-side recovery not elaborated | — | — | — | — | P — anti-collusion hardening (variant size equalization, per-segment multi-variants); no attribution algorithm |
| A9 (full text, re-scored 16.07.2026) | **P** — server-side detector identifies WMIDs from colluded video | — | — | — | — | P — colluding-source WMIDs identified via policy-diversified variants, eliminating false positives |
| A10 (full text, targeted read 16.07.2026) | **P** — detection device captures streams (streaming/P2P networks) and extracts device-identifying marks | — | — | — | — | P — collusion-attack robustness of full-screen time-domain WM asserted ([0158]); no attribution algorithm |
| B1 (full, transcription) | P — codec-chain provenance recovery | — | — | — | — | — |
| B2 | *scored with A1* | | | | | |
| B3 (full text/OCR, re-scored 16.07.2026) | **P** — captures content as transmitted, extracts the watermark, compares against reference watermarks (anti-piracy server) | — | — | — | — | — |
| B4 (full text/OCR, re-scored 16.07.2026) | P — visible-mark point-of-piracy identification, including geographic analysis | — | — | — | — | — |
| B5 (full text/OCR, re-scored 16.07.2026) | P — watermark monitoring and alarm | — | — | — | — | — |
| B6 (full text/OCR, re-scored 16.07.2026) | P — buyer key-space search on suspect copy | P — multimedia-hash-selected regions | — | — | — | P — likelihood-thresholded key-space search identifies a collaborator list (合作者列表) |
| B7 (full text, confirmed 16.07.2026) | **P** — target/reference shot-order comparison with predetermined tolerances (e.g., flipped video); no recipient step | — no hashing; direct shot comparison | — | — | — | — |
| B8 (full text) | **P** — subtitle-timing lookup against database | — | — | — | — | — |
| B9 (full text/OCR, re-scored 16.07.2026) | — **embedding side only; detection not elaborated in '973** (cf. sibling WO 2009/122385) | — | — | — | — | P — LCCA collusion attacks discussed; design motivated by collusion resilience |
| C8 (full text, re-scored 16.07.2026) | P — session watermark "forensically trace[s] the origin of content leakage"; extraction procedure outside spec scope | — | — | — | P — WM pattern maps to device/account/session identity (operator record implied) | — searched; not identified |
| C3 / C7 | *not scored — copies outstanding; both expected to bear on column 21; C7 was rated X against D1's PCT claims (§7 note 4)* | | | | | |

**Detection footer.** Two clusters, both now sharper: identification *techniques* without recipient resolution (A5, B7, B8) and recipient-resolution *loops* without camera-source-transition structure (A4, A2/A3, A6, A7, A9, A10, B6, C8). **Column 21 is dense** — A2, A3, A4, and A6 all reach Y on collusion/probabilistic attribution — so claims 21/28 must lean on the camera-cut structural substrate, not on probabilistic attribution as such. B9's detection cell was *downgraded* on full-text review (embedding-only disclosure). No document was identified deriving camera-source transitions **with their switch timings** at regions where versions select between synchronized camera views — A4 comes closest (per-duration perspective identification) but derives no timing. Combination watch: A5/B7 (technique) + A4 or A2/A3 (resolution loop); B8 supplies the temporal-identifier motivation narrative.

## 6. End-to-end method (claims 22–30)

Dependent columns mirror earlier families — **23←2 · 24←9/12 · 25←19+20 · 26←17+18 · 27←14 · 28←21 · 29←7 · 30←8** — and inherit those delta scores unless a deviation is noted here. Only claim 22 (whole end-to-end combination) is scored fresh.

| Document (depth) | 22 (indep.) | Mirror deviations |
|---|---|---|
| A1 (full, transcription) | **P** — closest end-to-end disclosure (ISR X against the PCT claims); lacks camera production and structural recovery | none |
| A2 (full text, confirmed 16.07.2026) | P — assign→trace loop over segment versions | none |
| A3 (full text, confirmed 16.07.2026) | P — assign→trace loop, multilevel | none |
| A4 (full text, re-scored 16.07.2026) | **P** — closest single reference after D1: camera-perspective fragment versions, per-user manifests, edge redirect delivery, user resolution, probabilistic collusion recovery; no cut-timing variation or switch-timing derivation | none |
| A5 (full text, confirmed 16.07.2026) | — technique only | none |
| A6 (full text, re-scored 16.07.2026) | P — variant delivery + real-time detection/response + probabilistic colluder identification | none |
| A7 (full text, re-scored 16.07.2026) | P — device-driven variant delivery with device tracing | none |
| A8 (full text, re-scored 16.07.2026) | P — variant-sequence identification with obfuscation hardening | none |
| A9 (full text, re-scored 16.07.2026) | P — client-side WM variants + policies datastore + server-side collusion detector; no version production or delivery | none |
| A10 (full text, targeted read 16.07.2026) | P — per-device rendering marks with network-capture detection loop | none |
| B1 (full, transcription) | — provenance metadata only | none |
| B2 | *scored with A1* | |
| B3 (full text/OCR, re-scored 16.07.2026) | — channel monitoring via watermark comparison; per-recipient versioning not identified | none |
| B4 (full text/OCR, re-scored 16.07.2026) | P — per-playback mark to point-of-piracy loop | none |
| B5 (full text/OCR, re-scored 16.07.2026) | — broadcast monitoring only | none |
| B6 (full text/OCR, re-scored 16.07.2026) | P — per-buyer transform to detection loop | none |
| B7 (full text, confirmed 16.07.2026) | — comparison technique only | none |
| B8 (full text) | — content identification only | none |
| B9 (full text/OCR, re-scored 16.07.2026) | P — per-user assembly at exchange points with ID association; detection not elaborated | none |
| C8 (full text, re-scored 16.07.2026) | P — standardized A/B session loop | none |
| C3 / C7 | *not scored — copies outstanding* | |

**Method footer.** The Written Opinion found the PCT claims novel but not inventive; claim 22's exposure is combination-based, principally A1 + the distribution cluster (A4/C8) + detection techniques (A5/B7). **The now-transcribed B2 ISR shows the ISA rated B9, B6's US family member (US 2005/0175224 A1), A10, and C7 (Lin 2008) category X against D1's own PCT claims** — the same cluster converges from every direction (§7 note 4). Claim 22's surviving distinction is the same camera-boundary core as claims 1/9/16.

## 7. Reading the grid — counsel notes

1. The strongest repeated pattern holds after full-text review: documents reach **P** on the independent claims through *marking or assembling otherwise-identical footage*; none reaches the multi-camera boundary mechanism. **Exception requiring counsel attention (memo §7 escalation): A4's full text discloses fragment versions differing by camera perspective, with correlation-based identification of which perspective a pirated copy contains.** That maps the "selection between temporally corresponding frames captured by different cameras" element more closely than previously recorded. A4 still shows no edit-list production, no movement of a recorded cut boundary, and no derivation of camera-*switch timings* — the cut grid in A4 is fixed; only the occupant of each slot varies. The distinctions to preserve are (i) boundary movement as the variant-creating act and (ii) switch-timing patterns as the recovered structure.
2. The 16.07.2026 re-score resolved every `nr` cell; A2, A3, A5, and B7 were spot-confirmed with no cell changes. Notable movements: A4 21→Y, 15→Y, 8→Y, 1→P; A6 14/15/21→Y and 16→P; A8 14/15→Y, 7→P; A9/A7 16→P; A5 18→P; **B9 16 downgraded to —** (embedding-only); A7 10 downgraded to P (deliberately common manifest).
3. Where a delta column is all **—** (claims 2–5 and 13), distinguish two cases before relying on a rung: no identified art (claims 2–5 — the production ladder remains untouched) versus routine technology unlikely to distinguish (13 blockchain; likewise the now partially-matched 10/14).
4. **B2-ISR mining (16.07.2026).** B2's international search report — readable for the first time via the transcription — cites, as category X against D1's PCT claims: US 2005/0175224 A1 (B6's US family member; ¶¶[0007]–[0012], [0027]–[0052], [0069]); **B9** (claims 1–10, 13–17, 19–21, 24–30; p.1 l.24–p.2 l.6, p.3 l.23–p.4 l.27, p.5 l.3–p.7 l.2 — the exchangeable-time-points disclosure — p.10 l.1–18); **A10** (promoted into the inventory on this basis after having been provisionally set aside); and **C7/Lin 2008** (claims 1–17, 19–30). Independent ISA corroboration of this cluster's materiality; C7 copy acquisition is now higher priority.
5. Pinpoint rule unchanged: any quotation used in a filing or argument must be verified against the source PDF, not the transcription.

## 8. Maintenance

Re-score triggers — any of: claim amendment or renumbering; arrival of the Italian search report (C6) or its citations; C3/C7 copies received; A10 sequential read; any new document entering this folder; any feature-matrix correction. Record each pass below.

| Date | Event | Scope of change |
|---|---|---|
| 16.07.2026 | Created; scored against the 16.07.2026 30-claim draft and the 19 stored documents | Initial population: A1/B1/B8 and content-verified rows scored from repo transcriptions and prior verified review; A6–A9, B9 at abstract+face depth; C8 at title+scope depth; C3/C7 unscored |
| 16.07.2026 | Full text made available for all documents (`markdown/`) | Nine image-only documents OCR'd; ten extracted from text layers. No cells changed in this step; backlog opened |
| 16.07.2026 | **Full-text re-score executed** | All former `nr` cells resolved; ~40 cells changed (see §7 note 2 for the movements); A2/A3/A5/B7 confirmed unchanged; B2 equivalence to A1 confirmed and its ISR mined (§7 note 4); **A10 (US 2010/0100971 A1, Geyzel) added** from the ISR's X citations, stored, transcribed, and scored at targeted-read depth; depth column now records scoring provenance per row |
