# AA11393US — Patent Prosecution Corpus

> **INTERNAL COUNSEL-REVIEW MATERIAL — NOT FOR FILING.**
>
> Repository status date: **25 July 2026**. This corpus supports ordinary US national-stage prosecution under 35 U.S.C. § 371 of PCT/IB2025/051755 (published as WO 2025/181623 A1, with a priority claim to US 63/557,868). The § 119(e) benefit claim remains subject to official-record and claim-specific support verification. No document in this repository is counsel-approved or filing-ready; retained US counsel must confirm every legal conclusion, claim wording, and filing decision. Directory names and draft labels do not establish privilege or work-product protection.

This repository combines the prosecution document corpus, its uniform XML machine interface, and the local, confidentiality-controlled HTML5 claims navigator. Each registered package declares whether its authority is a source PDF, authored Markdown, or authored relation XML; exposing XML to machine consumers never changes that authority. Builds and tests run only in this checkout or an approved private runner; integrity checks are listed under [Validation](#validation). Contribution, naming, and hard live-status conventions are in [`AGENTS.md`](AGENTS.md).

## Purpose

This corpus supports the prosecution of the invention with one organizing discipline: **maximum honest defensibility**. Every document is prepared so that each stated position can withstand scrutiny — by the examiner, by retained counsel, and in any later challenge — without relying on overstated support, unverified copies, or advocacy presented as fact. The controls in this repository exist for that reason and are to be read against it: quotations are verified against canonical source PDFs because a misquote is an indefensible representation; written description and enablement are concluded separately for each filing because a conflated or family-level support statement does not survive review; contemporaneous evidence, current testing, inference, and attorney argument are kept separately identified because only the first is evidence; and applicant-prepared analysis is never represented as counsel advice. Where no explicit rule covers a situation, prefer the course that is more defensible over the one that reads stronger.

## Repository layout

| Location | Function |
|---|---|
| [`US/`](US/) | US claiming strategies: `normal-allowance/` (NA baseline), `allowance-first/` (AF alternative plus AF-CONT continuation candidate), `common/` shared filing and continuation controls |
| [`prior-art/`](prior-art/) | Canonical prior-art source store: 33 manifest-controlled packages (source PDF, transcription XML, Markdown review view, provenance) shared across jurisdictions |
| [`PCT/`](PCT/) | PCT filing and international-search record and publication provenance |
| [`PPA2/`](PPA2/as%20filed%2063%20557868.pdf) | Provisional 63/557,868 filing record and assignment papers |
| [`ITA/`](ITA/ITA%20depositi%20ufficiali/AA11393US-IT_Domanda%20di%20brevetto%20n.%20102025000003210.pdf) | Related Italian filing record |
| [`office action response/`](office%20action%20response/PF-MA-AA11393US-PCT%20prepared%20response%20tightened.md) | Prepared PCT office-action response drafts |
| [`structured_source/`](structured_source/) | Closed authority-scheme registry, XML schemas and profiles, converters, reference resolution, and recurring validation |
| [`navigator/`](navigator/RUNBOOK-content-sync-and-regeneration.md) | Edition-blind HTML5 navigator source, secure XML gateway, authoritative NA/AF relations and wording, tests, runbook, and stored current products |
| [`STRUCTURED-CONTENT-AUTHORITY-MANIFEST.md`](STRUCTURED-CONTENT-AUTHORITY-MANIFEST.md) | High-level authority and uniform XML-interface rules |
| [`contracts/`](contracts/README.md) | Dependency-phased normative contracts: source surfaces, semantic relations, and navigator product generation |

## Artifact taxonomy

Two cross-cutting classifiers apply to every artifact: the strategy ID (`NA`, `AF`, `AF-CONT`) and the status suffix (`_DRAFT`, `_MEMO`). A claim set and its companions form a version-locked bundle: the claim-set version header controls its maps and matrices, and all are rescored together after any amendment.

| Artifact type | Naming pattern | Current function |
|---|---|---|
| Claim set | `…-<strategy>-US_claim-set_DRAFT.md` with registered generated XML | Versioned authored-Markdown candidate claims for one strategy; the version header controls all companions |
| Priority-support map | `…-priority-support-map_DRAFT.relations.xml` plus generated `.md` | Per-claim PCT/provisional written-description and enablement conclusions with Mode A/B/C gating |
| Prior-art comparison matrix | `…-prior-art-comparison-matrix_DRAFT.relations.xml` plus generated `.md` | Art scoring valid only for the claim-set version named in its header |
| Claim-document mapping matrix | `…-claim-document-mapping-matrix_DRAFT.relations.xml` plus generated `.md` | Claim-to-disclosure/source mapping for the same version |
| Counsel briefing | `…-US_counsel-briefing_DRAFT.md` | Strategy evaluation and counsel decision package |
| Memo | `…_MEMO.md` | Controlling shared instrument for continuation preservation, deferred filing/disclosure/EP work, or prior-art transmittal records |
| Claim crosswalk | `…-claim-crosswalk_DRAFT.md` | Inter-strategy AF/NA mapping and successor-reservation support |
| Shared record | `US/common/…_DRAFT.md` / `…_MEMO.md` | Canonical IDS, public-comments, filing, and continuation controls; referenced, never duplicated |
| Canonical source record | Filing PDFs in `PCT/`, `PPA2/`, `ITA/`; art PDFs in `prior-art/<ID>/` | Authoritative evidence; never edited; registered PDFs are manifest-controlled |
| Structured-source package | One declared authority scheme and one registered XML interface, with exactly the files that scheme permits | PDF governs PDF-derived fidelity; Markdown governs authored content; relation XML governs authored assertions; generated representations never gain authority |
| Router / README | `README.md` per directory | Live index and routing for its directory |
| Controlled vocabulary | `GLOSSARY.md` (root) | Current operative meanings of identifiers and terms, each pointing to its controlling document |
| Navigator artifact | `navigator/dist/AA11393US-<edition>-claims-spec-navigator_<version>.html` | Deterministic current-edition counsel-review navigation aid with detached checksum |

## Claim-set generation workflow

The NA and AF-CONT claim sets (and any successor claim set) are produced and maintained by the following procedure. Each step names its canonical touchpoint; shared materials are referenced, never duplicated into strategy directories.

1. **Read the canonical source record.** The disclosure base is the PCT application and search record in [`PCT/`](PCT/) and the [as-filed provisional record](PPA2/as%20filed%2063%20557868.pdf). These are the only authoritative support sources.
2. **Use the registered art packages.** Each [`prior-art/`](prior-art/) ID package contains one manifest-bound source PDF, one asserted transcription XML, one generated Markdown review view, and any declared non-authoritative convenience derivative. Never edit canonical PDFs; verify every quotation, especially OCR-derived text, against the stored PDF.
3. **Select the claim strategy.** [`US/README.md`](US/README.md) defines the strategy IDs (NA, AF, AF-CONT), current claim-set versions, and status controls. Use `NA claim N`, `AF claim N`, and `AF-CONT claim N` outside claim text; an unqualified claim number must not transfer a conclusion between strategies.
4. **Draft the claims.** Maintain claim content and stable item identities in authoritative Markdown; regenerate, never manually edit, its XML machine representation. Use actor-focused independent claims, singly dependent fallbacks, and no multiple-dependent claims, with current counts, dependencies, ordinary fee consequences, and the exclusions recorded in each claim set (no suspect-side physical-camera identification, no joint ordered-source-pair-plus-timing matching, without a new claim-as-a-whole support determination).
5. **Produce the companion artifacts.** Each claim set is valid only with its versioned companions: priority-support map (separate PCT and provisional written-description/enablement conclusions, Mode A/B/C gating), prior-art comparison matrix, claim-document mapping matrix, and counsel briefing; AF-CONT is additionally mapped by the AF claim crosswalk. A matrix is valid only for the claim-set version named in its header.
6. **Apply the shared controls.** [`US/common/`](US/common/) holds the single IDS inventory, the single PCT informal-comments draft, the continuation-preservation memo, and the deferred filing/disclosure/formalities/EP work memo. Coordinate arguments, priority positions, continuation placement, and IDS decisions across strategies to avoid contradictory records.

## Validation

The host must provide the exact `uv` version required by [`pyproject.toml`](pyproject.toml). Provision the locked project-local environment after cloning or after an authorized lock change:

```sh
uv --no-cache sync --locked --all-groups
```

This explicit bootstrap may obtain locked dependencies; recurring validation never installs or updates them. After changing claims, verify claim count, dependency, antecedent basis, support mappings, and every affected matrix row; re-score art when claim wording changes. Follow [`navigator/RUNBOOK-content-sync-and-regeneration.md`](navigator/RUNBOOK-content-sync-and-regeneration.md) whenever a navigator input changes. From the repository root, run the sole aggregate current-state and document-integrity gate with the argument-free convenience launcher:

```sh
./validate.sh
```

The launcher executes this exact command:

```sh
uv --no-cache --offline run --locked --no-sync python -m navigator validate-current
```

The command captures governed current bytes, including relevant untracked files, validates declared authority direction, XML identity, deterministic representations, computed coverage and substantive-origin tracing, references, handoffs, the secure XML gateway, immutable models, current products, captured-file whitespace, Markdown rendering, source manifests, and every registered test in an isolated materialization. It then recaptures the worktree and fails on any path, mode, or byte change. Repository status, index state, commit identity, and history are outside the result.

Each operative contract pair, its machine-readable acceptance registry, applicable configuration,
implementation, controls, registered tests and vectors, generated representations, declared
handoffs, and stored products form one indivisible current state. A documentation-only,
registry-only, implementation-only, workflow-only, test-only, control-only, or product-only state
is invalid. The applicable contract pair controls detailed behavior; this README creates no
alternate implementation or release path.

A pass means only that the current package is technically coherent and reproducible for independent inventor and counsel review. It does not establish source authenticity, transcription fidelity, factual or legal correctness, completeness of prior-art or support analysis, inventor confirmation, counsel approval, filing readiness or authorization, or entitlement to rely without reviewing the evidence. The result is ephemeral; human review remains authoritative. The runbook's [final worktree validation](navigator/RUNBOOK-content-sync-and-regeneration.md#6-final-worktree-validation) places the gate in the content-update workflow.

## Status discipline

Package documents, live configuration, structured-source registries, navigator controls, and current build products contain only the current operative version, status, conclusion, supporting evidence, action, owner, deadline, trigger, schema, content binding, and product. Git is drafting history only; do not retain revision logs, wording-evolution narratives, non-current controls or artifacts, compatibility aliases, or implicit upgrades in the live checkout. The repository has no approval or reviewer system, implementation register, validation-result or receipt store, auxiliary release plan, stored lineage or coverage artifact, exported validation record, migration reader, or compatibility path. Computed coverage and substantive-origin tracing remain mandatory ephemeral checks. Retain legally operative filing, publication, priority, and prosecution facts and source provenance as current evidence. Every strategy document states its strategy ID, version, status, and review date.
