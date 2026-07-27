# AA11393US — Controlled Vocabulary

> **INTERNAL COUNSEL-REVIEW MATERIAL — NOT FOR FILING.**
>
> Repository status date: **23 July 2026**. This glossary records the current operative meaning of identifiers and terms used across the corpus and points to the controlling document for each. It restates no analysis; where a term's treatment could diverge, the controlling document governs.

## Strategy and version identifiers

| Term | Current meaning | Controlling document |
|---|---|---|
| **NA** | Normal-allowance strategy: balanced actor-split coverage; current substantive baseline | [`US/README.md`](US/README.md) |
| **AF** | Allowance-first strategy: integrated chain plus monitor-side method, with broader scope identified for a controlled successor | [`US/README.md`](US/README.md) |
| **AF-CONT** | AF actor-focused continuation claim candidate; unfiled and unpreserved; not the universal continuation procedure | [`US/allowance-first/continuation-candidate/claims/AA11393US-AF-CONT-US_claim-set_DRAFT.md`](US/allowance-first/continuation-candidate/claims/AA11393US-AF-CONT-US_claim-set_DRAFT.md) |
| Claim-set version | Version header (`NA-2026-07-22-v4`, `AF-2026-07-22-v6`, `AF-CONT-2026-07-22-v2`) locking a claim set to its maps and matrices | [`US/README.md`](US/README.md) |

## Support-posture codes

Grades assigned per limitation in each priority-support map. Combinations (e.g., **D/CE/G**) list every applicable code; `mode unassigned` records that no DW-05A mode has been assigned.

| Code | Meaning | Controlling document |
|---|---|---|
| **D** | Direct express passage, claim, table, or concrete example | § 1 of each `…-priority-support-map_DRAFT.md` |
| **C** | Contextual support for the architecture or result | same |
| **CE** | Combined-example relationship | same |
| **W** | Weak or not express | same |
| **G** | Counsel determination required | same |

## DW-05A effective-date modes

Counsel's per-claim support/priority outcome. "Support" requires written description **and** enablement, determined separately, in the filing named.

| Mode | Required conclusion | Consequence | Controlling document |
|---|---|---|---|
| **A — PCT and provisional support** | Both filings satisfy written description and enablement for the claim as a whole | Claim may rely on 26.02.2024; B10's 02.12.2024 publication is not prior art merely by that date | [`US/common/filing-controls/AA11393US-deferred-filing-disclosure-and-EP-work_MEMO.md`](US/common/filing-controls/AA11393US-deferred-filing-disclosure-and-EP-work_MEMO.md), DW-05A outcome record |
| **B — PCT support only** | PCT supports the claim as a whole; the provisional fails at least one requirement | Effective filing date no earlier than 19.02.2025; B10 becomes potentially citable § 102(a)(1) art; reassess all intervening art | same |
| **C — PCT support fails** | PCT fails written description, enablement, or both for the claim as a whole | Do not rely on the claim as drafted; select a supported contingency, amend without new matter, or record a later-date strategy | same |

The current applicant assessment assigns NA claims 16 and 22 to Mode A; counsel must confirm or reject that basis. Every other gated claim is unassigned or carries the posture recorded in its support map.

## Deferred-work register (DW-\*)

Open pre-filing and post-engagement work items with owners, triggers, and required outcomes. An open item does not bar the controlled initial transmission of the package to prospective or retained US counsel, except as DW-12 requires.

| Code | Subject | Code | Subject |
|---|---|---|---|
| **DW-01** | Execute ordinary § 371 national-stage filing | **DW-08A** | Focused professional art search; historical/technical evidence preservation |
| **DW-02** | Inventor oath/declaration | **DW-08B** | Objective indicia and technical-results evidence with claim nexus |
| **DW-03** | Applicant identity, ownership, assignment chain | **DW-08C** | Lawful infringement, actor, and proof record |
| **DW-04** | Entity status | **DW-09** | Italian search report for IT 102025000003210 |
| **DW-05** | Continuity, benefit claim, ADS data | **DW-10** | US IDS package |
| **DW-05A** | Claim § 112(a)/priority analysis; mode assignment (see above) | **DW-11A / DW-11B** | EP-phase entry (Rule 159) and Rule 161(1)/162 response |
| **DW-06** | B6 English-family handling | **DW-12** | Circulation, confidentiality, retention, and preservation controls |
| **DW-07** | EP 2 811 416 A1 family and EPO file history | **DW-08** | Source verification, nonpatent retrieval, pair selection, materiality |

Controlling document for the full register: [`US/common/filing-controls/AA11393US-deferred-filing-disclosure-and-EP-work_MEMO.md`](US/common/filing-controls/AA11393US-deferred-filing-disclosure-and-EP-work_MEMO.md).

## Continuation-preservation controls (CONT-\*)

Strategy-neutral controls applied whether the ordinary § 371 parent uses `NA`, `AF`, or an approved hybrid. **CONT-01** through **CONT-06** govern the controlled parent and benefit chain, owner and docket, filed-versus-reserved scope, successor vehicle and authorization, filing and verification, and generation outcome. Current status: **NOT YET PRESERVED**. Controlling document: [`US/common/continuation-controls/AA11393US-continuation-preservation_MEMO.md`](US/common/continuation-controls/AA11393US-continuation-preservation_MEMO.md).

## Prior-art inventory identifiers

| Identifier family | Current meaning | Controlling document |
|---|---|---|
| **A1 / D1** | US 2021/0352381 A1, ISR-cited | [`US/common/ids/AA11393US-US_IDS-reference-list_DRAFT.md`](US/common/ids/AA11393US-US_IDS-reference-list_DRAFT.md); [`US/prior-art/README.md`](US/prior-art/README.md) |
| **B1 / D2** | CN 117278762 A, ISR-cited | same |
| **A2–A21** | US patent documents in the working inventory | same |
| **B2–B10** | Foreign patent documents in the working inventory | same |
| **C-series** | Nonpatent literature (C3 author-hosted Tardos extended version; C7 Lin 2008 outstanding; C8 ETSI TS 104 002 DASH-IF A/B watermarking) | same |
| **B10** | KR 2024-0168593 A, published 02.12.2024; the intervening-art pivot for Mode B analysis | same |

Canonical PDFs in each co-located [`US/prior-art/`](US/prior-art/) package are manifest-controlled and never edited. Transcription XML provides the uniform machine interface, generated Markdown is the review view, and every declared convenience derivative is nonauthoritative.

## Structured-content terms

| Term | Current meaning | Controlling document |
|---|---|---|
| **Authority scheme** | The package declaration that identifies whether source fidelity is governed by a stored PDF, authored content by Markdown, or authored assertions by relation XML; file type and consumer choice cannot change it | [`PDF transcription`](contracts/10-source-surfaces/pdf-transcription/technical-description.md) §1; [`authored Markdown`](contracts/10-source-surfaces/authored-markdown/technical-description.md) §1; [`authored relations`](contracts/20-semantic-relations/authored-relations/technical-description.md) §1 |
| **Uniform XML machine interface** | The one registered, typed, item-addressable XML representation exposed by every package; interface uniformity does not make XML universally authoritative | same, §§1–3 |
| **Aggregate prerequisite** | A domain that must pass the shared current-state gate but supplies no consumer edge, handoff, or runtime semantic input; authored relations currently have this relationship to the navigator | [`contract router`](contracts/README.md); [`claims navigator technical description`](contracts/30-product-generation/claims-navigator/technical-description_DRAFT.md) §2.1 |
| **Semantic handoff** | Exact retained representation bytes, controls, role, authority scheme, dependencies, assets, and validation-read census supplied through one declared consumer edge; inherited validation reads grant no access | [`PDF transcription`](contracts/10-source-surfaces/pdf-transcription/technical-description.md) §6; [`authored Markdown`](contracts/10-source-surfaces/authored-markdown/technical-description.md) §6 |
| **Computed coverage** | Validation derived from the retained current worktree capture that checks the applicable authority-to-representation, item, provenance, and endpoint mappings; it is not a stored package artifact | same, §§2 and 5 |
| **Substantive-origin tracing** | A validation-time derivation that resolves substantive and security-relevant navigator values to their declared XML item, registered control, typed state, or closed mechanical derivation; it is not a stored lineage inventory | [`claims navigator technical description`](contracts/30-product-generation/claims-navigator/technical-description_DRAFT.md) §2.4 |
| **Worktree validation capture** | Closed governed path inventory, modes, and retained current bytes used for every aggregate-validation read and compared with a final recapture; repository status, index state, identity, and history are excluded | same, §10 |

## Filing and record terms

| Term | Current meaning |
|---|---|
| **Provisional / PPA2** | US 63/557,868, filed 26.02.2024; [as-filed record](PPA2/as%20filed%2063%20557868.pdf) |
| **PCT** | PCT/IB2025/051755, filed 19.02.2025, published as WO 2025/181623 A1 on 04.09.2025, with a priority claim to US 63/557,868; record and provenance in [`PCT/`](PCT/) |
| **ISR / Written Opinion** | International search report and the EPO's negative Written Opinion; D1/D2 derive from the ISR |
| **§ 371 parent** | Current US route: ordinary national-stage entry of PCT/IB2025/051755; counsel confirmation and filing evidence remain required under DW-01 |
| **§ 119(e) benefit** | Intended US benefit of provisional 63/557,868; official-record and claim-specific written-description and enablement verification remain required under DW-05 and DW-05A |
| **§ 111(a) successor** | Ordinary continuation or, when supported by the restriction record, divisional filed while a qualifying parent remains pending under `CONT-*` |
| **ADS** | Application Data Sheet carrying continuity/benefit data; verification under DW-05 |
| **IDS** | Information disclosure statement; the inventory in `US/common/` is the only disclosure inventory (DW-10) |
| **PRAXI / UIBM** | Italian counsel liaison and the Italian Patent and Trademark Office for IT 102025000003210 (DW-09) |
| **POSITA** | Person of ordinary skill in the art; repository memoranda are not contemporaneous evidence of POSITA knowledge (DW-08A) |

## Technical claim terms

| Term | Current meaning | Controlling document |
|---|---|---|
| **Reference / mate** | The reference is the audio-video content produced according to the structured edit list; a mate is produced from a varied list in which at least one camera-cut time code differs, preserving the same ordered camera transition at a noncoincident timing | The claim sets; Examples 2–4 of the PCT/provisional |
| **Structured list / EDL** | Edit Decision List identifying, per cut, a source camera and in/out time codes, including director-commanded real-time selections | The claim sets (NA claim 4, AF-CONT claim 2) |
| **Chunk / manifest** | Versions are segmented into chunks; manifest files point to recipient-specific chunk combinations so an assembled stream preserves one of the two timings of a retained transition | The claim sets (distribution independents) |
| **Ledger / record of associations** | Stored associations between delivered manifest files and recipients | The claim sets (NA claims 12, 16; AF-CONT claims 9, 11) |
| **Reconstructed manifest** | Manifest built by the detector from plural camera-cut time codes identified in a suspected unauthorized distribution | The claim sets (detection independents) |
| **"Equal" manifest** | The lookup key matching a delivered manifest to a reconstructed one; counsel must select one supported construction (byte identity, equivalent chunk selections, or equivalent represented timing choices) and account for dynamic URLs, tokens, and metadata | NA claim set § 5 and AF-CONT claim set § 3, reconstruction and equality gates; AF priority-support map |
| **Scene-change detection / perceptual hash / fuzzy matching** | The disclosed cut-time identification implementations: frame comparison by perceptual hashes, sliding-window fuzzy matching over frame groups | The claim sets (NA claims 17–18, 26; AF-CONT claims 12–13, 15–16) |
| **Causal nexus** | The claimed relationship tying a delivered mate-timing combination to the reconstructed same detected combination (AF claims 20–22, AF-CONT claims 17–19) | [`US/allowance-first/cross-strategy/claim-crosswalk/AA11393US-AF-claim-crosswalk_DRAFT.md`](US/allowance-first/cross-strategy/claim-crosswalk/AA11393US-AF-claim-crosswalk_DRAFT.md) |

## Navigator pipeline terms

| Term | Current meaning | Controlling document |
|---|---|---|
| **Repository snapshot** | Immutable capture of the complete repository tree with retained bytes; validation reads the captured bytes and rejects a changed final tree | [`claims navigator technical description`](contracts/30-product-generation/claims-navigator/technical-description_DRAFT.md) §10 |
| **Secure XML gateway** | The sole read-only production entry point for registered semantic content; it validates each package according to its authority scheme and rejects undeclared, unsafe, stale, or ambiguous input | same, §2.2 |
| **Navigator control** | A configured navigator-owned edition, relation, wording, or schema input read by the secure gateway after structured-source acceptance; it is not an upstream package handoff | same, §§2.2–2.3 |
| **Immutable edition model** | The sealed typed representation produced by the gateway and consumed by the edition-blind renderer; it cannot repair, infer, retarget, or persist semantic content | same, §§2.2 and 4 |
| **Live implementation closure** | The indivisible agreement among the applicable contract pair, acceptance registry, configuration, implementation, controls, registered tests and vectors, generated representations, handoffs, and stored products; a split or alternate state fails | same, §10 |
| **Technical-preview product** | The sole current navigator product class, carrying the exact technical-preview label and making no claim of observed browser, operating-system, print-engine, or assistive-technology behavior | same, §§1 and 3 |
| **Executable acceptance registry** | The current machine-readable projection of the ordered `AC-01` through `AC-20` IDs, scopes, and criterion text; every criterion must pass in the invoking validation process | [`claims navigator acceptance criteria`](contracts/30-product-generation/claims-navigator/acceptance-criteria_DRAFT.md) |
| **Delivery bundle** | The deterministic five-member STORE ZIP containing both sealed HTML products, their detached checksums, and `MANIFEST.txt`; its own detached checksum remains beside the ZIP | [`claims navigator technical description`](contracts/30-product-generation/claims-navigator/technical-description_DRAFT.md) §9 |

## Status suffixes and outcome labels

| Label | Current meaning |
|---|---|
| `_DRAFT` | Internal counsel-review status; not filed and not a legal opinion. In an operative technical contract, the suffix does not make current technical requirements optional |
| `_MEMO` | Controlling instrument governing execution decisions |
| `NOT YET PRESERVED` | No qualifying successor and verified benefit relationship complete the current generation |
| `CONTINUATION PRESERVED` | CONT-06 outcome: a verified successor with recognized benefit preserves the generation's identified families |
| `CHAIN CLOSED — DEFERRED SCOPE NOT PRESERVED` | CONT-06 outcome: applicant-approved relinquishment of the generation's identified deferred scope |
