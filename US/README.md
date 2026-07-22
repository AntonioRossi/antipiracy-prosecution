# AA11393US — US Prosecution Strategy Router

> **MASTER INDEX — INTERNAL COUNSEL-REVIEW MATERIAL — NOT FOR FILING.**
>
> Repository status date: **22 July 2026**. Directory names and draft labels do not establish attorney-client privilege, work-product protection, or any other protected status. Retained US counsel must determine treatment, circulation, retention, and legal-hold requirements.

This directory separates two alternative US claiming strategies for PCT/IB2025/051755 while preserving one canonical evidence and disclosure record. The alternatives are not cumulative filing instructions. Counsel should select, revise, or deliberately hybridize them and record which claim set controls.

**Initial-contact status.** The strategy branches and shared controls contain the applicant's present claims, support maps, art analysis, fallback directions, and execution register and are ready for applicant-controlled initial transmission to prospective or retained US counsel under DW-12. Open counsel opinions, route choices, and professional-search tasks are pending pre-filing decisions; their absence does not make the initial decision package incomplete, but no branch is counsel-approved or filing-ready.

## Strategy routing

| Strategy ID | Directory | Objective | Current status |
|---|---|---|---|
| **NA** | [`normal-allowance/`](normal-allowance/) | Balanced actor-split coverage: standalone production, distribution, and detection claims plus an end-to-end patentability anchor | **Current substantive baseline**; internal draft only |
| **AF** | [`allowance-first/`](allowance-first/) | One narrow operational chain in system and method independent formats, aimed at increasing early-allowance probability, with broader actor-specific coverage reserved for a copending continuation | **Alternative for counsel evaluation**; internal draft only |

Use `NA claim N` and `AF claim N` in every analysis or communication outside the claim text itself. An unqualified claim number is ambiguous and must not be used to transfer a conclusion between strategies.

## Canonical shared record

| Location | Controlling function |
|---|---|
| [`common/`](common/) | Single IDS inventory, public PCT informal-comments draft, and deferred filing/disclosure/formalities/EP work memo |
| [`prior-art/`](prior-art/) | Single source store for prior-art PDFs, searchable copies, Markdown review aids, provenance, and checksums |
| [`../PCT/`](../PCT/) | PCT application and international-search record |
| [`../PPA2/`](../PPA2/) | Provisional 63/557,868 filing record |
| [`../ITA/`](../ITA/) | Related Italian filing record |

Shared materials must not be copied into a strategy directory. Strategy documents may characterize claim effect differently, but factual source descriptions, document identifiers, IDS handling, public comments, and deadlines must point back to the canonical shared record.

## Version and status controls

- **NA claim-set version:** `NA-2026-07-21-v2`; four independent / 30 total / no multiple-dependent claims.
- **AF claim-set version:** `AF-2026-07-17-v2`; two independent / 20 total / no multiple-dependent claims. AF claim 20 is the method twin in the single AF proposal; counsel may omit it at filing by recorded decision without creating a second AF package.
- Every strategy document must state its strategy ID, version, status, and review date.
- Every claim matrix is valid only for the claim-set version named in its header and must be rescored after claim amendment or renumbering.
- Package documents are live-state artifacts. State only the current version, status, conclusion, supporting evidence, open action, owner, deadline, or re-evaluation trigger. Git is the sole drafting/change history; do not add revision records, dated maintenance histories, recorded activations, commit narratives, or descriptions of how current wording or scores evolved. Retain legally operative filing, publication, priority, and prosecution facts and source provenance where they support the current analysis; those facts are evidence, not package-maintenance history.
- Neither strategy directory is an approved filing package. Counsel must prepare compliant claims, continuity data, ADS, declarations, amendments, and filing forms.

## Non-duplication and filing controls

1. The IDS inventory in `common/` is the only disclosure inventory. Art relevance may be analyzed differently by strategy, but disclosure decisions must be coordinated across every related US application.
2. The PCT informal-comments draft in `common/` is the only public-comments draft. Do not create strategy-specific public versions; counsel must approve one consistent filing-facing text.
3. The prior-art PDFs remain clean and unchanged. Quotations from Markdown/OCR aids must be checked against the source PDF or an official copy.
4. The AF strategy is viable only with a controlled continuation plan. For each generation in which supported, commercially valuable scope remains deliberately deferred, an approved successor must be filed and verified while a qualifying benefit-chain application remains pending, or counsel and the applicant must record `CHAIN CLOSED — DEFERRED SCOPE NOT PRESERVED`. The AF memo applies this control recursively without requiring an endless chain or mislabeling closure as preservation.
5. Arguments, priority positions, and IDS decisions must be coordinated across NA and AF to avoid contradictory records.

## Recommended counsel reading order

1. This router and [`common/README.md`](common/README.md).
2. The README and counsel briefing for the strategy being evaluated.
3. That strategy's exact claim set and priority/support map.
4. That strategy's feature matrix and claim-document mapping matrix.
5. For AF, the claim crosswalk and continuation/coverage-reservation memo.
6. The canonical IDS inventory, prior-art provenance record, and underlying official filing sources.
