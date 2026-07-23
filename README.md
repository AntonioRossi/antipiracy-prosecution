# AA11393US — Patent Prosecution Corpus

> **INTERNAL COUNSEL-REVIEW MATERIAL — NOT FOR FILING.**
>
> Repository status date: **23 July 2026**. This corpus supports ordinary US national-stage prosecution under 35 U.S.C. § 371 of PCT/IB2025/051755 (published as WO 2025/181623 A1, with a priority claim to US 63/557,868). The § 119(e) benefit claim remains subject to official-record and claim-specific support verification. No document in this repository is counsel-approved or filing-ready; retained US counsel must confirm every legal conclusion, claim wording, and filing decision. Directory names and draft labels do not establish privilege or work-product protection.

This repository combines the prosecution document corpus with the local, confidentiality-controlled HTML5 claims navigator that consumes its pinned current claim and PCT sources. Navigator builds and tests run only in this checkout or an approved private runner; integrity checks are listed under [Validation](#validation). Contribution, naming, and hard live-status conventions are in [`AGENTS.md`](AGENTS.md).

## Purpose

This corpus supports the prosecution of the invention with one organizing discipline: **maximum honest defensibility**. Every document is prepared so that each stated position can withstand scrutiny — by the examiner, by retained counsel, and in any later challenge — without relying on overstated support, unverified copies, or advocacy presented as fact. The controls in this repository exist for that reason and are to be read against it: quotations are verified against canonical source PDFs because a misquote is an indefensible representation; written description and enablement are concluded separately for each filing because a conflated or family-level support statement does not survive review; contemporaneous evidence, current testing, inference, and attorney argument are kept separately identified because only the first is evidence; and applicant-prepared analysis is never represented as counsel advice. Where no explicit rule covers a situation, prefer the course that is more defensible over the one that reads stronger.

## Repository layout

| Location | Function |
|---|---|
| [`US/`](US/) | US claiming strategies: `normal-allowance/` (NA baseline), `allowance-first/` (AF alternative plus AF-CONT continuation candidate), `common/` shared filing and continuation controls, `prior-art/` canonical art store |
| [`PCT/`](PCT/) | PCT filing and international-search record and publication provenance |
| [`PPA2/`](PPA2/) | Provisional 63/557,868 filing record and assignment papers |
| [`ITA/`](ITA/) | Related Italian filing record |
| [`office action response/`](office%20action%20response/) | Prepared PCT office-action response drafts |
| [`navigator/`](navigator/) | Edition-blind HTML5 navigator source, closed schemas, reviewed NA/AF mappings, verification records, tests, runbook, and committed current artifacts |
| [`AA11393US-claims-navigator_technical-description_DRAFT.md`](AA11393US-claims-navigator_technical-description_DRAFT.md) | Normative navigator contract; controls over the non-normative runbook |

## Artifact taxonomy

Two cross-cutting classifiers apply to every artifact: the strategy ID (`NA`, `AF`, `AF-CONT`) and the status suffix (`_DRAFT`, `_MEMO`). A claim set and its companions form a version-locked bundle: the claim-set version header controls its maps and matrices, and all are rescored together after any amendment.

| Artifact type | Naming pattern | Current function |
|---|---|---|
| Claim set | `…-<strategy>-US_claim-set_DRAFT.md` | Versioned candidate claims for one strategy; the version header controls all companions |
| Priority-support map | `…-priority-support-map_DRAFT.md` | Per-claim PCT/provisional written-description and enablement conclusions with Mode A/B/C gating |
| Prior-art comparison matrix | `…-prior-art-comparison-matrix_DRAFT.md` | Art scoring valid only for the claim-set version named in its header |
| Claim-document mapping matrix | `…-claim-document-mapping-matrix_DRAFT.md` | Claim-to-disclosure/source mapping for the same version |
| Counsel briefing | `…-US_counsel-briefing_DRAFT.md` | Strategy evaluation and counsel decision package |
| Memo | `…_MEMO.md` | Controlling shared instrument for continuation preservation or deferred filing/disclosure/EP work |
| Claim crosswalk | `…-claim-crosswalk_DRAFT.md` | Inter-strategy AF/NA mapping and successor-reservation support |
| Shared record | `US/common/…_DRAFT.md` / `…_MEMO.md` | Canonical IDS, public-comments, filing, and continuation controls; referenced, never duplicated |
| Canonical source record | Filing PDFs in `PCT/`, `PPA2/`, `ITA/`; art PDFs in `US/prior-art/` | Authoritative evidence; never edited; art PDFs checksum-controlled |
| Review aid | `US/prior-art/markdown/`, `US/prior-art/searchable/` | Transcription and OCR convenience copies; never authoritative over the source PDF |
| Router / README | `README.md` per directory | Live index and routing for its directory |
| Controlled vocabulary | `GLOSSARY.md` (root) | Current operative meanings of identifiers and terms, each pointing to its controlling document |
| Navigator artifact | `navigator/dist/AA11393US-<edition>-claims-spec-navigator_<version>.html` | Deterministic current-edition counsel-review navigation aid with detached checksum and exact-side release evidence |

## Claim-set generation workflow

The NA and AF-CONT claim sets (and any successor claim set) are produced and maintained by the following procedure. Each step names its canonical touchpoint; shared materials are referenced, never duplicated into strategy directories.

1. **Read the canonical source record.** The disclosure base is the PCT application and search record in [`PCT/`](PCT/) and the provisional record in [`PPA2/`](PPA2/). These are the only authoritative support sources.
2. **Assemble the art corpus.** Canonical prior-art PDFs live in [`US/prior-art/`](US/prior-art/) with Markdown review transcriptions, OCR searchable copies, provenance, and the `.pipeline/` checksum manifest and converter. Never edit canonical PDFs; verify every quotation, especially OCR-derived text, against the source PDF.
3. **Select the claim strategy.** [`US/README.md`](US/README.md) defines the strategy IDs (NA, AF, AF-CONT), current claim-set versions, and status controls. Use `NA claim N`, `AF claim N`, and `AF-CONT claim N` outside claim text; an unqualified claim number must not transfer a conclusion between strategies.
4. **Draft the claims.** Actor-focused independent claims, singly dependent fallbacks, and no multiple-dependent claims, with current counts, dependencies, ordinary fee consequences, and the exclusions recorded in each claim set (no suspect-side physical-camera identification, no joint ordered-source-pair-plus-timing matching, without a new claim-as-a-whole support determination).
5. **Produce the companion artifacts.** Each claim set is valid only with its versioned companions: priority-support map (separate PCT and provisional written-description/enablement conclusions, Mode A/B/C gating), prior-art comparison matrix, claim-document mapping matrix, and counsel briefing; AF-CONT is additionally mapped by the AF claim crosswalk. A matrix is valid only for the claim-set version named in its header.
6. **Apply the shared controls.** [`US/common/`](US/common/) holds the single IDS inventory, the single PCT informal-comments draft, the continuation-preservation memo, and the deferred filing/disclosure/formalities/EP work memo. Coordinate arguments, priority positions, continuation placement, and IDS decisions across strategies to avoid contradictory records.

## Validation

After changing claims, verify claim count, dependency, antecedent basis, support mappings, and every affected matrix row; re-score art when claim wording changes. Follow [`navigator/RUNBOOK-content-sync-and-regeneration.md`](navigator/RUNBOOK-content-sync-and-regeneration.md) whenever a navigator input changes. The canonical current-state and document-integrity gate is:

```sh
python3 -m navigator validate-current
```

One command proves the complete live navigator closure inside immutable repository snapshots — pin plans, candidate and sealed bytes, bundle and authorization chains, record and distribution inventories, `git diff --check` whitespace — runs the full discovered test suite in a materialized sandbox, renders every changed Markdown file through pandoc, verifies the `US/prior-art` source checksums, and certifies only the final unchanged snapshot. The runbook's [current-state and cutover gate](navigator/RUNBOOK-content-sync-and-regeneration.md#7-current-state-and-cutover-gate) section places this gate in the full content-integration workflow.

Regenerate prior-art transcriptions only deliberately: `cd US/prior-art && python3 .pipeline/convert.py A1`.

## Status discipline

Package documents and live navigator configuration are live-state artifacts: state only the current version, status, conclusion, supporting evidence, open action, owner, deadline, trigger, schema, or content binding. Git is the sole drafting and implementation history; do not add revision records, dated maintenance histories, wording-evolution narratives, compatibility aliases, or implicit upgrades. Digest-addressed same-schema records may persist as append-only verification evidence but authorize nothing unless every current exact-side binding matches. Retain legally operative filing, publication, priority, and prosecution facts and source provenance as current evidence. Every strategy document states its strategy ID, version, status, and review date.
