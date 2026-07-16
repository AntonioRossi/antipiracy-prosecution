# AA11393US — Prior-Art Comparison Matrix (DRAFT)

> **INTERNAL COUNSEL ANALYSIS — NOT FOR FILING AS-IS.**
>
> This matrix records a limited review of the international-search references and supplemental candidates. A blank or “not identified” entry means the feature was not identified in the present review, not that the document has been exhaustively cleared. Counsel should verify the complete documents and commission any additional search needed before relying on the distinctions.

## 1. Proposed combination to test

The proposed inventive combination is:

1. video from multiple cameras capturing temporally corresponding views;
2. a structured edit list recording source-camera selections and cut time codes;
3. local movement of a camera-selection boundary so that a mate uses frames from a different camera during an adjacent interval;
4. optionally, preservation or restoration of a later boundary;
5. association of the resulting camera-cut timing pattern or manifest representation with a recipient; and
6. derivation and matching, from suspected content, of a camera-source-transition pattern that includes corresponding switch timings to resolve the recipient.

Terminology in this matrix follows the claim strategy: **camera-cut timing pattern** denotes the timing representation used by the production, distribution, and end-to-end families, while **camera-source-transition pattern** denotes the richer detection-side representation of source transitions and their corresponding switch timings. The latter is not merely a label applied to generic timing data.

## 2. Element matrix

Legend: **Y** = expressly or substantially disclosed in the limited review; **P** = partial/analogous; **—** = not identified.

| Reference | Completed-copy or generic content variants | Multi-camera source / camera cuts | Local boundary movement using alternate-camera frames | Segment / manifest variation | Recipient or device association | Detection from suspected/pirated content | Timing pattern used as identifier | Present distinction / claim effect |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **D1 — US 2021/0352381 A1** | Y | P: scene changes, not alternate camera production | — | P: segmentwise transformed copies | P: watermark and ID-based/random selection; no claimed association loop identified | P: watermark recovery; transformations principally frustrate collusion | P: delay/frame-rate transformations, but not recovered camera-cut identity | Do not characterize as watermark-only. D1 alone lacks multi-camera edit-list input, alternate-camera interval substitution, and structural-pattern recovery; assess combinations with conventional multi-camera production art. Later resynchronization is a useful fallback subject to the provisional Example 2 caveat in the priority map. |
| **D2 — CN 117278762 A** | P | — | — | — | P: codec-chain provenance | Y: metadata/watermark provenance | — | Secondary A reference. Distinguish recipient-specific camera-boundary variation and recovery. |
| **US 7,630,497 B2 / US 2007/0067242 A1** | Y | — | — | Y: file-segment variations | Y: sequence keys assigned to media players/models | Y: hybrid traitor tracing | — | Generic “many versions,” segment variation, and assignment are not safe novelty positions. Tie claims to the multi-camera boundary variable. |
| **US 2009/0320130 A1** | Y | — | — | Y: multiple variations for selected content segments | Y: inner/outer code assignments | Y: recovered pirate files and collusion scoring | — | Treat generic chunk combinations and collusion tracing as known. Preserve camera-source edit mechanism and use Tardos only as a dependent fallback. |
| **US 10,834,158 B1** | Y | **P: fragment versions "may differ in camera perspective" for a duration; correlation identifies the delivered perspective (full text, 16.07.2026)** | — : no edit list, no boundary movement, no switch-timing creation — the fragment grid is fixed | Y: customized manifest selects fragment/playback versions; server/edge per-request redirect sequencing | Y: manifest pattern represents user identifier | Y: identifier recovered from a copy; **probabilistic version-pattern estimation identifies colluding users** | P: temporal sequence of playback options | **Closest single reference after D1 (escalated per memo §7, 16.07.2026).** Distribution claims must require that manifest choices represent camera-cut **timing** variants created from multi-camera production; detection claims must require derivation of camera-source transitions **with switch timings** — A4 identifies the per-slot perspective but derives no timing. |
| **US 2012/0087583 A1** | — | P: video shots and shot boundaries | — | — | — | Y: suspected/reference comparison | P: shot-level signature using perceptual hashes | Detection by hashing and shot detection is not expected to be independently inventive. Use it as implementation detail tied to recipient-associated cut patterns. |
| **WO 2021/141686 A1** | P: abridged target/reference videos | P: shots separated by cuts; a shot may be frames from one camera | — | P: groups and sequences of shots | — | Y: unauthorized-copy/piracy identification | P: order/pattern of shots | Distinguish deliberate per-recipient generation by local camera-boundary movement and ledger resolution. |
| **EP 2 811 416 A1** | — | — | — | — | — | Y: video identification | Y: subtitle timing pattern | Discloses part of the motivation narrative: temporal identification as an alternative where visual watermarks are removable. Focus on per-recipient generation and recovery of multi-camera edit boundaries. Check the EPO file history for useful examination reasoning or cited art; current legal status does not alter the A1 publication's disclosure date. |
| **CN 100583750 C** | Y | — | — | P | P | Y: fingerprint recovery | Y/P: desynchronization-resistant fingerprint | Review closely against any broad “relative timing/fingerprint” language. Avoid relying on desynchronization resistance alone. The Microsoft family has been identified, but counsel must verify the exact CN publication number against an official register. |
| **WO 2017/017603 A1; WO 2010/044102 A2; CN 202455480 U** | P | — | — | — | P | Y/P: watermark-based detection or verification | — | Background-cited watermark art. Supports presenting pixel-independent edit structure as an alternative mechanism without making watermark absence a mandatory limitation. |
| **US 2014/0325550 A1 (A6, added 16.07.2026)** | Y: segments differing in at least one characteristic | — | — | Y: per-request segment delivery in broadcast/ABR | Y: requesting device | Y: real-time piracy response | P: sequence of delivered segment variants | Segment-variant delivery with recipient association and live response is known. Tie variants to multi-camera boundary movement and structural recovery. |
| **US 2017/0118537 A1 (A7, added 16.07.2026)** | Y: multiple versions of a segment | — | — | Y: requested addresses from a published manifest select among versions | Y: device identifier drives selection | P: watermarking service supports later tracing | — | Manifest-address-driven per-device version selection is known. The distinction is the camera-cut origin of the versions and transition-pattern recovery. |
| **US 2018/0352307 A1 (A8, added 16.07.2026)** | Y: content-segment variants | — | — | Y: variants encode an identifying sequence; manifest-entry durations randomized; variant sizes equalized | Y: identifying sequence per transmission | P: obfuscation directed against pirate variant-detection | P: deliberate manipulation of manifest duration values | Variant sequences as identifiers and manifest-timing manipulation are known. Claims must rest on camera-source substitution at recorded cuts, not variant sequencing as such. |
| **US 2023/0377085 A1 / US 12,412,229 B2 (A9, added 16.07.2026)** | Y: multiple watermark-image variants | — | — | — : client-side graphic layers rather than segment/manifest variation | Y: watermark identifier | P: anti-collusion binding policies | — | Client-side watermark-image variation for collusion resistance (published 23.11.2023, before the provisional). Distinguish structural camera-cut collusion handling; bears on claims 21/28. |
| **WO 2009/156973 A1 (B9, added 16.07.2026)** | Y: space-desynchronized streams | — | — | Y: sequential selection of consecutive segments across streams at predefined **exchangeable time points** (random access points chosen to hide switching) | Y: per-user fingerprint (IDs/keys unicasted per receiver) | — : embedding side only; detection not elaborated in '973 (full text, 16.07.2026; cf. sibling WO 2009/122385) | P: per-user switch sequence at fixed exchange points — the time grid itself is never the variable | Cited **category X against D1's own PCT claims** in the B2 ISR (transcribed 16.07.2026), with pinpoints including the exchangeable-time-points passages. No synchronized alternate-camera substitution and no movement of a recorded cut boundary. |
| **ETSI TS 104 002 V1.1.1, 2023-08 (C8, added 16.07.2026)** | Y: A/B watermarked variants | — | — | Y: standardized A/B delivery via edge/manifest; sequencer returns the Variant per request based on a watermark token | Y: WM pattern is a device/account/session identifier | P: watermark "forensically trace[s] the origin of content leakage"; extraction procedure outside spec scope (full text, 16.07.2026) | — | Standardization (08.2023) strengthens the obviousness backdrop for generic A/B claims. Independent claims must require camera-cut-derived variants. |
| **US 2010/0100971 A1 (A10, added 16.07.2026)** | Y: per-device time-domain full-frame colour modulation | — | — | — | Y: rendering-device identity carried in the mark itself | Y: network-side capture (streaming/P2P) and mark extraction | P: time-varying modulation cycle | Rated **category X against D1's own PCT claims** in the B2 ISR (initially set aside from the D1-grant face review; promoted 16.07.2026). Client-side embedding art analogous to A9; no versioning, manifests, or camera structure. |

## 3. D1 issue-by-issue correction

| Topic | Unsafe characterization | Counsel-facing accurate position |
|---|---|---|
| Identifier | “D1's transformations are not identifiers” | D1 discloses watermark-like arbitrary identifiers in addition to watermarks. They remain additive signal-domain information rather than camera-boundary structure. |
| Random selection | “Randomly selected transformations identify nobody” | Random assignments could be logged. The point is that D1 does not disclose the claimed record-and-recovery loop for locally varied camera boundaries. |
| Alignment | “Every D1 copy remains aligned and differs only by watermark” | D1 deliberately causes misalignment. Its scene changes remain trigger/camouflage locations, not recipient-specific camera-selection variables. |
| Time delay | “Relative cut timing defeats D1” | A uniform delay preserves inter-cut intervals, but this alone does not answer D1's frame-rate embodiment. |
| Frame rate | Not addressed | Global frame-rate variation may change measured inter-cut intervals. Require actual alternate-camera frame substitution and retain later-resynchronization fallback. |
| Motivation | “D1 is structurally incapable and must abandon its principle” | D1 does not provide a reason to route synchronized alternate-camera feeds to the transformer, rewrite recorded camera-selection boundaries, and make those boundaries the forensic variable. |

## 4. Claim impact

| Candidate claims | Closest concerns | Recommended response |
|---|---|---|
| Production claims 1–8 | D1; generic EDL/multi-camera production knowledge | Actual source-camera substitution around a local boundary; later resynchronization; avoid generic “change a timecode” as the only distinction |
| Distribution claims 9–15 | US 7,630,497; US 2009/0320130; US 10,834,158 | Require manifest/chunk choices to represent camera-cut timing patterns originating from the multi-camera mate process |
| Detection claims 16–21 | US 2012/0087583; WO 2021/141686; EP 2 811 416; CN 100583750 | Require operational derivation and matching of camera-source-transition structure at regions where delivered versions select between temporally corresponding camera views, followed by recipient resolution—not merely detection of copied video, generic timing data, or a timing fingerprint |
| End-to-end claims 22–30 | Combinations of the above; routine multi-camera production | Emphasize functional closed loop and lack of motivation to connect alternate-camera boundary generation to manifest/recipient association and recovery |

## 5. Search gaps for counsel

The ISA search-strategy sheet appears narrow relative to the full claim architecture. A supplemental professional search should expressly cover:

- forensic watermarking through alternate video segments or A/B variants;
- edit decision lists used to generate personalized media versions;
- camera-cut or shot-boundary timing as a fingerprint;
- manifest-coded identifiers and content-fragment version patterns;
- anti-collusion streaming variants and Tardos implementations;
- broadcast systems that shift director cuts or select alternate synchronized angles; and
- detection resilient to global time scaling, dropped frames, advertisements, overlays, and re-encoding.

All search results should be routed into the IDS inventory and this matrix, with the final claim effect recorded.

**Status 16.07.2026.** A claim-informed supplemental review executed the first, third, fourth, and fifth bullets in part, via citation mining (A4 grant face; D1 US-grant face, US 11,540,029 B2) and keyword sweeps; results were routed to the IDS as A6–A9, B9, C7, and C8 and added to the element matrix above. The camera-selection/vision-mixer/EDL and screener-versioning sweeps (second and sixth bullets) returned no on-point art; that observation is limited to the searches run and is not a clearance. A professional search covering all bullets remains advisable before substantive reliance.

A claim-level projection of this matrix — one Y/P/— cell per drafted claim per stored document, with per-document review depth — lives at `prior-art/AA11393US-claim-document-mapping-matrix_DRAFT.md`. This feature matrix remains the analytic source; on any conflict, correct the projection, and keep the two synchronized per that file's §8 re-score triggers.

**Full-text re-score, 16.07.2026** (transcriptions in `prior-art/markdown/`; see the projection's §7–§8 for the cell-level record). Headline findings: (i) **A4's full text discloses fragment versions differing by camera perspective, correlation-based identification of the delivered perspective, and probabilistic collusion recovery** — its row above was corrected accordingly and the finding is escalated to counsel per memo §7; (ii) B9's per-user structure sits on **fixed exchangeable time points** and its detection side is **not elaborated** — its row was corrected in both directions; (iii) **B2's ISR, readable for the first time, rates US 2005/0175224 A1 (B6's US family member), B9, A10, and Lin 2008 (C7) category X against D1's own PCT claims** — A10 was promoted into the inventory on that basis and C7's acquisition priority raised. The camera-boundary core (edit-list input, movement of a recorded cut boundary, switch-timing derivation) remains unidentified in every document after full-text review.

## 6. Verification and document-completion priorities

1. Confirm CN 100583750 C against an official register and obtain an official copy plus appropriate English translation, abstract, or concise explanation. **Register check and copy completed 16.07.2026 (Espacenet cross-check; CNIPA-issued copy stored); English handling remains open.**
2. Review the EP 2 811 416 A1 family and EPO file history. Record grant/withdrawal status for completeness, but do not treat that status as changing the disclosure made by the published A1 document.
3. Store official copies of A2, A3, A5, B7, and Tardos 2003 in `prior-art/` if counsel selects them for submission or continuing review. **A2, A3, A5, and B7 stored 16.07.2026; Tardos 2003 remains outstanding, now alongside Lin 2008 (C7).**
4. Obtain the Italian search report promptly and assess every newly cited document for the US IDS.
5. Review the 16.07.2026 supplemental references (A6–A9, B9, C7, C8) against the final claim set and record the claim effect and counsel disposition for each.
