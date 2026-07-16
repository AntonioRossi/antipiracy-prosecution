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
5. association of the resulting timing pattern or manifest representation with a recipient; and
6. recovery of that pattern from suspected content to resolve the recipient.

## 2. Element matrix

Legend: **Y** = expressly or substantially disclosed in the limited review; **P** = partial/analogous; **—** = not identified.

| Reference | Completed-copy or generic content variants | Multi-camera source / camera cuts | Local boundary movement using alternate-camera frames | Segment / manifest variation | Recipient or device association | Detection from suspected/pirated content | Timing pattern used as identifier | Present distinction / claim effect |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **D1 — US 2021/0352381 A1** | Y | P: scene changes, not alternate camera production | — | P: segmentwise transformed copies | P: watermark and ID-based/random selection; no claimed association loop identified | P: watermark recovery; transformations principally frustrate collusion | P: delay/frame-rate transformations, but not recovered camera-cut identity | Do not characterize as watermark-only. D1 alone lacks multi-camera edit-list input, alternate-camera interval substitution, and structural-pattern recovery; assess combinations with conventional multi-camera production art. Later resynchronization is a useful fallback subject to the provisional Example 2 caveat in the priority map. |
| **D2 — CN 117278762 A** | P | — | — | — | P: codec-chain provenance | Y: metadata/watermark provenance | — | Secondary A reference. Distinguish recipient-specific camera-boundary variation and recovery. |
| **US 7,630,497 B2 / US 2007/0067242 A1** | Y | — | — | Y: file-segment variations | Y: sequence keys assigned to media players/models | Y: hybrid traitor tracing | — | Generic “many versions,” segment variation, and assignment are not safe novelty positions. Tie claims to the multi-camera boundary variable. |
| **US 2009/0320130 A1** | Y | — | — | Y: multiple variations for selected content segments | Y: inner/outer code assignments | Y: recovered pirate files and collusion scoring | — | Treat generic chunk combinations and collusion tracing as known. Preserve camera-source edit mechanism and use Tardos only as a dependent fallback. |
| **US 10,834,158 B1** | Y | — | — | Y: customized manifest selects fragment/playback versions | Y: manifest pattern represents user identifier | Y: identifier can be recovered from a copy in disclosed embodiments | P: temporal sequence of playback options | Distribution claims must require that the manifest choices represent camera-cut timing variants created from multi-camera production, not merely any fragment-version pattern. |
| **US 2012/0087583 A1** | — | P: video shots and shot boundaries | — | — | — | Y: suspected/reference comparison | P: shot-level signature using perceptual hashes | Detection by hashing and shot detection is not expected to be independently inventive. Use it as implementation detail tied to recipient-associated cut patterns. |
| **WO 2021/141686 A1** | P: abridged target/reference videos | P: shots separated by cuts; a shot may be frames from one camera | — | P: groups and sequences of shots | — | Y: unauthorized-copy/piracy identification | P: order/pattern of shots | Distinguish deliberate per-recipient generation by local camera-boundary movement and ledger resolution. |
| **EP 2 811 416 A1** | — | — | — | — | — | Y: video identification | Y: subtitle timing pattern | Discloses part of the motivation narrative: temporal identification as an alternative where visual watermarks are removable. Focus on per-recipient generation and recovery of multi-camera edit boundaries. Check the EPO file history for useful examination reasoning or cited art; current legal status does not alter the A1 publication's disclosure date. |
| **CN 100583750 C** | Y | — | — | P | P | Y: fingerprint recovery | Y/P: desynchronization-resistant fingerprint | Review closely against any broad “relative timing/fingerprint” language. Avoid relying on desynchronization resistance alone. The Microsoft family has been identified, but counsel must verify the exact CN publication number against an official register. |
| **WO 2017/017603 A1; WO 2010/044102 A2; CN 202455480 U** | P | — | — | — | P | Y/P: watermark-based detection or verification | — | Background-cited watermark art. Supports presenting pixel-independent edit structure as an alternative mechanism without making watermark absence a mandatory limitation. |

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

## 6. Verification and document-completion priorities

1. Confirm CN 100583750 C against an official register and obtain an official copy plus appropriate English translation, abstract, or concise explanation.
2. Review the EP 2 811 416 A1 family and EPO file history. Record grant/withdrawal status for completeness, but do not treat that status as changing the disclosure made by the published A1 document.
3. Store official copies of A2, A3, A5, B7, and Tardos 2003 in `prior-art/` if counsel selects them for submission or continuing review.
4. Obtain the Italian search report promptly and assess every newly cited document for the US IDS.
