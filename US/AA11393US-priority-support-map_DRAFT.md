# AA11393US — Provisional and PCT Priority/Support Map (DRAFT)

> **INTERNAL COUNSEL ANALYSIS — NOT A LEGAL OPINION.**
>
> This map distinguishes (1) written-description/no-new-matter support in PCT/IB2025/051755 as filed from (2) entitlement to the 26 February 2024 filing date of US provisional 63/557,868. Page references to the provisional are PDF page numbers in `../PPA2/as filed 63 557868.pdf`; counsel should verify them against the official USPTO image-file wrapper. PCT references are to the as-filed application in the international filing dossier.

## 1. Source identity

| Source | Filing date | Repository evidence | Status |
|---|---:|---|---|
| US provisional 63/557,868 | 2024-02-26 | `../PPA2/as filed 63 557868.pdf`; filing report in the same directory | Earliest claimed benefit source |
| PCT/IB2025/051755 | 2025-02-19 | `../PCT/AA11393US-PCT_RAPPORTO DEPOSITO.pdf` | International application as filed |
| IT 102025000003210 | 2025-02-19 | Italian filing dossier under `../ITA/` | Related application; not an earlier priority source |

The directory name `PPA2` is not evidence of a second provisional. No second provisional filing receipt has been identified.

## 2. Feature map

| Proposed claim feature | Provisional support | PCT support | Assessment / counsel action |
|---|---|---|---|
| Multiple cameras capturing an event from diverse viewpoints | pp. 15, 42–44; system and method claim passages | Detailed description of cameras 101 and pipeline 102; PCT claims 1, 10, 16 | Strong core support |
| Director-commanded switching / camera cuts | pp. 15, 20–25, 42–44 | Pipeline 102 description; camera-cut recording step 220; claims 10 and 16 | Strong core support |
| Structured list of instructions describing edits / EDL | pp. 12, 15, 20–27, 42–44 | List 103 and EDL passages; claims 1, 10, 16 | Strong core support |
| Entries identify source camera and in/out time codes | pp. 23, 26–27; Example EDL tables | EDL description and Example 2, Tables 1–3 | Strong support; preserve source-camera terminology |
| Automatic variation of camera-cut time code to generate mate | pp. 15, 24–27, 42–44; real-time pseudocode and claims | Mate creation component 110; Example 1; claims 1, 10, 16 | Strong core support |
| Mate differs in sequence/timing of camera cuts | pp. 24–27 | Description of mates 111 and timing patterns | Strong core support |
| Actual adjacent interval uses frames from a different source camera | pp. 26–27: Cut 2 extension replaces beginning interval of Cut 3 in the EDL | Example 2, Tables 1–3 and explanatory text | Supported by concrete example; counsel should confirm the proposed “temporally corresponding frames” wording |
| Later cut retains reference time / resynchronization | pp. 26–27: the Example 2 table places Cut 4 at the reference time and the accompanying text expressly states that `00:00:30:01` is the correct start, but the same paragraph also contains an inconsistent `00:00:30:11` “mistake” sentence | Example 2: Cut 4 starts at the same reference time; re-alignment explanation is internally consistent in the PCT text | Supported narrow fallback, subject to an express counsel opinion on the provisional's internal inconsistency; do not describe priority confidence as unqualified |
| Small/subtle/visually insignificant variations | pp. 12, 15, 24, 38 | Description characterizes differences as subtle/minimal/visually insignificant | Support exists for selected variations; do not claim every arbitrary shift is inherently imperceptible |
| Segmentation into chunks and adaptive CDN delivery | pp. 12, 15, 18–19, 28–34, 42–44 | Transcoding components 120, chunks 113; claims 11–12, 17 | Strong support |
| Manifest files point to interleaved reference/mate chunks | pp. 15, 28–34, 42–44 | Manifest files 121, mixing component 123, Example 4; claims 11–12, 17 | Strong support; generic manifest identifiers are prior art, so retain camera-cut origin |
| Record/ledger associates versions or manifests with recipients | pp. 12, 15, 18, 31–35, 38, 41–44 | Ledger 122; claims 1, 14, 15, 17 | Strong support |
| Blockchain registration of associations | pp. 18, 35 | Blockchain component 150; PCT claim 13 | Supported dependent fallback |
| Unicasting | pp. 16, 38, 43–44 | PCT claim 6 and method embodiment | Supported dependent fallback |
| Detect camera cuts in suspected/pirated content and derive time codes | pp. 15, 36–38, 43–44 | Detection component 130 and algorithm 131; claims 1, 15–17 | Strong core support; counsel should separately confirm the proposed operational linkage between detected transitions and regions where delivered versions select different camera views |
| Perceptual hash comparison | pp. 16, 36–37, 43–44 | PCT claim 2; Example 5 | Supported, but known-art implementation detail |
| Sliding-window fuzzy matching | pp. 16, 37, 43–44 | PCT claim 3; Example 5 | Supported, but known-art implementation detail |
| Reconstructed manifest and ledger search | pp. 15, 34–37, 41, 43–44 | Reconstructed manifest 121′, retrieval 140; PCT claim 15 and claim 17 | Strong narrow fallback |
| Probabilistic/Tardos handling of collusion | pp. 38–40, 43–44 | PCT claim 5 and Tardos passages | Supported generally; counsel should avoid claiming more specific algorithmic performance than disclosed |
| ML analytics determines variations/configurations | pp. 35–37, 42–44 | Analytics component 104; PCT claim 7 | Thin/result-oriented support; retain only as expendable dependent claims |
| Additional overlaid audio/video elements | pp. 43–44 and related description | PCT claim 4 and pipeline overlay description | Supported dependent fallback |
| Processor, memory, storage, and server implementation | pp. 24–25, 31–36 | Computing-environment and server-cluster passages; PCT claims 8–9 | General structural support; §112(f)/algorithm analysis remains necessary |
| Operation without requiring the boundary variation to embed pixel data | Architecture throughout; watermark discussed as complementary rather than sole mechanism | Description states mechanism does not only involve watermarking and permits complementary watermarking | Use as an advantage, not an unsupported blanket negative limitation |

## 3. Example 2 drafting inconsistency requiring counsel analysis

The provisional's Example 2 contains a drafting inconsistency directly relevant to candidate claims 2, 3, and 23:

- At provisional PDF p. 27 (printed p. 16), the mate EDL table places Cut 4 at `00:00:30:01` and labels it “Adjusted to the reference.”
- The explanatory bullet first says that the mate's Cut 4 begins at `00:00:30:11`, identifies that value as a mistake in the alignment attempt, and then expressly states that the correct approach is for Cut 4 to start at `00:00:30:01`, just as in the reference and with no delay.
- The PCT Example 2 states the corrected alignment without the provisional's inconsistent value.

The correct resynchronization rule therefore appears expressly in both the provisional table and the provisional's corrective explanation. The inconsistency should not be treated internally as an automatic loss of priority, but neither should the fallback receive an unqualified “strong” rating. Counsel should provide a claim-specific written view on whether a skilled reader would understand possession of later-cut resynchronization and whether the PCT wording is a permissible clarification rather than new matter. Until that review is complete, keep resynchronization as a dependent fallback rather than the sole basis of the principal independent claim.

This issue belongs in the confidential counsel analysis. Do not insert it into the public WIPO informal comments unless counsel concludes that doing so is strategically necessary.

### Trigger for renewed priority and disclosure analysis

The present limited review has not identified potentially material art or another prior-art event having an effective date after the provisional filing on 26 February 2024 but before the PCT filing on 19 February 2025. This is not a clearance conclusion.

If a reference, activity, or other information potentially material to patentability is identified with an effective prior-art date in that interval, or if any Office questions priority entitlement, counsel must reassess:

1. the claim-by-claim Example 2 and provisional-support position;
2. whether the effective filing date becomes outcome-determinative for any pending claim;
3. applicable disclosure obligations, including whether an IDS or other action is required; and
4. every representation concerning entitlement to the provisional date.

The direction to keep the present internal analysis out of the WIPO informal comments is subject to that reassessment. The trigger does not itself dictate public disclosure of attorney analysis; counsel must decide the correct disclosure and prosecution response based on the material information then known.

## 4. Candidate-claim mapping

| Candidate claims | Provisional basis | PCT basis | Priority confidence before counsel review |
|---|---|---|---|
| 1–6 production | pp. 15, 20–27, 42–44 | Claims 1, 10, 16; system 100; Examples 1–2 | High for core other than the specific resynchronization fallback in claims 2–3, which requires the Example 2 inconsistency analysis above; proposed wording to verify |
| 7 ML | pp. 35–37, 42–44 | Claim 7; analytics 104 | Medium/low due functional breadth |
| 8 overlay | pp. 43–44 | Claim 4 | Medium/high |
| 9–15 distribution | pp. 15, 18–19, 28–35, 42–44 | Claims 11–14, 17; Example 4 | High if tied to reference/mate cut patterns |
| 16–20 detection | pp. 15, 34–38, 41–44 | Claims 1–3, 15, 17; Example 5 | High for general architecture; verify written-description support for matching at regions where delivered versions select different camera views |
| 21 probabilistic collusion | pp. 38–40, 43–44 | Claim 5; Tardos passages | Medium; avoid unsupported details |
| 22–28 end-to-end | Combined passages above | Claims 1–6, 10–17 | High for the general disclosed combination; claim 23 resynchronization requires the Example 2 inconsistency analysis above; divided-infringement issue is separate |
| 29 ML method | pp. 35–37, 42–44 | Claim 7 and method programming passages | Medium/low |
| 30 overlay method | pp. 43–44 | Claim 4 and method overlay passage | Medium/high |

## 5. Items counsel must verify

1. Confirm that the provisional filing receipt, ADS, and specification in Patent Center match the repository copy and that benefit is timely and correctly claimed for the selected US route.
2. Confirm whether “temporally corresponding,” “camera-selection boundary,” “reference timing,” and “restoring synchronization” are acceptable constructions of the express examples rather than added concepts.
3. Confirm every independent claim as a whole—not merely each isolated noun—has adequate provisional support.
4. Confirm the PCT-to-bypass continuity statement and certified-copy requirements if bypass is selected.
5. Treat any proposed feature absent from both columns as potential new matter; do not insert it into a continuation claim while representing it as entitled to the provisional date.
6. If commercially important improvements were developed after the PCT filing, identify them separately for possible continuation-in-part strategy rather than mixing them into this support map.
7. Address expressly the provisional Example 2 inconsistency identified in section 3 before relying on the provisional date for claims 2, 3, or 23 or moving resynchronization into an independent claim.
8. Confirm whether the candidate claim 16 formulation—candidate and detected camera-source-transition patterns at regions where delivered versions select between camera views—is fully supported as an operational relationship, not merely as a description of stored data.
9. Establish responsibility for monitoring potentially material information with an effective prior-art date in the provisional-to-PCT interval and activate the reassessment above if such information appears or any Office questions priority.
