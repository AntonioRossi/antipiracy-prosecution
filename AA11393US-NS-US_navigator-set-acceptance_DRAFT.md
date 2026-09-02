# AA11393US — National-Stage Filed Edition (NS) Navigator Set: Acceptance Criteria (DRAFT)

> **INTERNAL COUNSEL-REVIEW MATERIAL — NOT FOR FILING.**
>
> Temporary implementation input coupled to the
> [`NS navigator build plan`](AA11393US-NS-US_navigator-set-plan_DRAFT.md). This document defines
> acceptance outcomes; it is not a validation result, approval record, or retained auxiliary
> release plan.

## 1. Acceptance rule

The implementation is complete only when every criterion below is satisfied in order. Criteria
`NS-AC-01` through `NS-AC-23` establish the technical and evidentiary-review surface. Human review
is deliberately the last and final criterion, `NS-AC-24`, and cannot begin as the acceptance step
until the preceding criteria pass.

No criterion passes from an implementer statement, a stored result, a prior run, a partial build,
or the existence of an output file. Machine-verifiable criteria must be incorporated into the
applicable data-only acceptance registries, projected into their paired acceptance documents, and
enforced by independent tests. The completed retained repository contains neither this document
nor the coupled plan; their operative requirements must then reside in the current contracts,
registries, configuration, implementation, tests, vectors, generated representations, and stored
products.

The aggregate technical gate is:

```sh
uv --no-cache --offline run --locked --no-sync python -m navigator validate-current
```

A passing gate establishes current technical coherence and deterministic reproduction only. It
does not establish source authenticity, transcription fidelity, factual or legal correctness,
completeness of prior-art or support analysis, inventor confirmation, counsel approval, filing
readiness, or authorization. Those matters remain within final human review.

## 2. Fixed acceptance basis

| Item | Required current value |
|---|---|
| Filed-edition classifier | `NS`, distinct from strategy IDs `NA`, `AF`, and `AF-CONT` |
| Application | U.S. application 19/616,060, national stage of PCT/IB2025/051755 |
| Claim-edition version | `NS-2026-08-17-v1` |
| Filed-claim authority | [`03-P3366-US-2026-08-17-Prelim-Amnd-TBF.pdf`](from-US-Counsel/260818-19616060/03-P3366-US-2026-08-17-Prelim-Amnd-TBF.pdf) |
| Filed posture | Claims 1–18 cancelled; claims 19–38 submitted and pending |
| Independent claims | 19, 30, 33, and 35 |
| Dependent claims | 20–29, 31–32, 34, and 36–38 |
| Specification evidence | PCT-as-filed dossier for PCT/IB2025/051755 |
| Prior-art scope | Exactly 33 registered art packages: A1–A21, B1–B10, C3, and C8 |
| IDS boundary | 34 disclosed entries: the 33 art packages plus the ISR/Written Opinion prosecution record |
| Required execution | **Option B:** both navigators in one pass with a fresh NS prior-art assessment; Options A and C are not accepted |
| Required NS products | `ns-specification` and `ns-prior-art` |
| Required NS artifact names | `AA11393US-NS-claims-spec-navigator_NS-2026-08-17-v1.html` and `AA11393US-NS-claims-prior-art-navigator_NS-2026-08-17-v1.html` |
| Current product-set result | Six configured products: the existing four NA/AF products plus the two NS products |
| Bundle result | Six ordered HTML/checksum pairs followed by `MANIFEST.txt`—13 ZIP members—and one detached ZIP checksum |

## 3. Promotion and removal

During implementation, each machine-verifiable outcome below must be assigned to its proper
existing contract domain or to a necessary closed filed-edition extension. The corresponding
data-only acceptance registry owns the criterion identity, scope, outcome, and independent
enforcer; its Markdown table is regenerated rather than maintained separately.

Once the operative system incorporates those requirements and the technical gate is green, this
document and the coupled plan are removed before `NS-AC-24` final human review. Their removal does
not remove any acceptance requirement: the current contract pairs and registries must contain the
operative technical criteria, while the repository-wide human-review boundary continues to govern
the final assessment.

## 4. Mandatory acceptance criteria

| ID | Scope | Required acceptance outcome | Required proof |
|---|---|---|---|
| **NS-AC-01 — Required Option B closure** | shared | Option B is the sole accepted execution. The delivered result contains both requested NS navigators in one pass, their detached checksums, the fresh NS prior-art assessment, and the regenerated configured delivery bundle. A specification-only milestone, a deferred prior-art product, or a transferred/provisional AF assessment is incomplete. | Exact configured-product, NS substantive-source, and stored-product inventory tests. |
| **NS-AC-02 — Filed-edition identity** | shared | `NS` is modeled as the filed edition of application 19/616,060 and is not admitted through a strategy-only field, alias, fallback, or compatibility branch. AF, NA, and AF-CONT retain their existing strategy meanings. | Closed schema/configuration tests and adverse vectors that reject NS-as-strategy input. |
| **NS-AC-03 — PDF authority** | source | The preliminary-amendment PDF is the sole fidelity authority for the submitted claim wording. The registered package uses `pdf-evidence-transcription-v1` unless a demonstrated claim-shape limitation is resolved by one new closed PDF-governed profile. `authored-markdown-v1` is rejected for this package. | Structured-source registry, profile, manifest, authority-direction, and adverse-profile tests. |
| **NS-AC-04 — Source-package closure** | source | The filed-claim package contains one exact stored PDF, one source manifest, one asserted transcription XML, and one XML-generated Markdown review view, with stable typed identities, provenance, uncertainty where applicable, and an explicit navigator consumer handoff. No semantic copy or undeclared source is consumed. | PDF-transcription package, coverage, registry-closure, and consumer-handoff tests. |
| **NS-AC-05 — Deterministic representations** | source | Fresh XML-to-Markdown generation is byte-identical to the retained review view; source and representation digests bind exact bytes; unsupported or stale forms fail before writes. Technical equality is not represented as human verification of fidelity. | Structured-source deterministic regeneration, digest, fail-closed, and rollback tests. |
| **NS-AC-06 — Claim inventory and status** | edition | The machine claim surface exposes exactly the twenty pending claims 19–38 for navigation and records claims 1–18 as cancelled filing posture rather than selectable current claims. It identifies exactly four independent claims: 19, 30, 33, and 35. | Computed claim/status/count/independence tests against the registered transcription. |
| **NS-AC-07 — Dependency and antecedent structure** | edition | The dependency graph is exact: claims 20–24, 26–27, and 29 depend from 19; 25 from 24; 28 from 27; 31–32 from 30; 34 from 33; 36–37 from 35; and 38 from 37. Dependency cycles, absent parents, and unresolved antecedent references fail. | Claim parser, dependency-graph, claim-unit, and antecedent-basis tests. |
| **NS-AC-08 — Cross-edition isolation** | shared | No AF, NA, or AF-CONT claim number, relation, mapping state, score, conclusion, or version identity is inherited by NS. Shared source evidence may be consumed only through declared source-package handoffs and fresh NS-owned relations. No NS content is inserted into a strategy-owned claim, relation, matrix, or passage-map package. | Origin tracing, cross-edition isolation tests, and adverse stale/cross-edition vectors. |
| **NS-AC-09 — Specification relation scope** | specification | `ns__pct.relations.xml` covers every selectable NS claim unit exactly once with a mapped or expressly unresolved current state. Coverage is computed rather than stored, and every mapping is version-bound to the filed NS claim surface. | Relation-schema, complete-unit coverage, version-binding, and one-state-per-unit tests. |
| **NS-AC-10 — Exact specification evidence** | specification | Every mapped PCT endpoint resolves to an exact non-root, non-editorial asserted-transcription fragment with the current typed digest. Wrong-document, stale-digest, inferred, duplicated, reversed, or undeclared endpoints fail before rendering. | Secure relation parsing, endpoint closure, digest, provenance, and adverse-vector tests. |
| **NS-AC-11 — Specification conclusion boundary** | specification | The navigator describes passage identification only. It does not characterize a passage association as proof of written description, enablement, priority entitlement, absence of new matter, validity, or filing approval. DW-05A remains visibly open. | Controlled-wording origins and forbidden-conclusion tests across interactive, no-script, and print surfaces. |
| **NS-AC-12 — Prior-art inventory** | prior art | The NS prior-art product consumes exactly A1–A21, B1–B10, C3, and C8—33 PDF-governed art packages. The ISR/Written Opinion is identified as the additional IDS prosecution record but is not silently counted or rendered as a thirty-fourth art package. | Exact source-scope, registry-handoff, document-census, and IDS-boundary tests. |
| **NS-AC-13 — Fresh comparison matrix** | prior art | The NS comparison matrix is newly assessed against filed claims 19–38 and bound only to the NS filed-edition version. Every required claim/art obligation has one current allowed state; no AF/NA score or status is copied, adapted, defaulted, or labeled provisional. | Matrix schema, exact obligation census, version lock, origin tracing, and no-transfer tests. |
| **NS-AC-14 — Passage-map closure** | prior art | The NS passage map exclusively supplies the current state, allocation, candidate, phrase, and ordered-passage planes for every matrix obligation. Every mapped candidate resolves to exact asserted XML evidence; unresolved review remains visible without synthetic passages or inferred children. | Passage-map acceptance tests, obligation/candidate closure, exact endpoint tests, and adverse vectors. |
| **NS-AC-15 — Search and analysis boundary** | prior art | The product states that its 33-document analysis neither completes nor substitutes for DW-08A professional searching and does not close unresolved support, priority, validity, or legal-conclusion work. | Controlled-wording and required-open-gate tests on all rendered surfaces. |
| **NS-AC-16 — Closed filed-edition model** | shared | Schemas, immutable models, validators, renderers, and product controls distinguish strategy scope from filed-edition scope and permit the declared PDF-governed claim handoff. Existing exact authority checks are generalized explicitly; they are not removed, weakened, or bypassed. Unknown scope kinds and authority combinations fail closed. | Model/schema tests plus positive NS and adverse unknown-scope/authority vectors. |
| **NS-AC-17 — Controlled product wording** | shared | NS titles, legends, guide text, provenance, labels, and bundle description consistently say filed edition or filed claims. NS never appears as an unfiled draft, candidate strategy, filing recommendation, legal opinion, or counsel-approved text. Existing AF/NA strategy wording remains semantically correct. | Exact wording-slot, slot, origin, forbidden-phrase, no-script, print, and bundle-manifest tests. |
| **NS-AC-18 — Contract-system coherence** | shared | Every affected technical description, paired acceptance document, data-only acceptance registry, taxonomy, glossary entry, configuration, implementation path, runbook instruction, test, vector, generated representation, and stored product states the same six-product current system. Fixed obsolete counts and shared assumptions that every edition is a strategy are absent. | Exact governed-path census, contract/registry projection, current-wording, and implementation-closure tests. |
| **NS-AC-19 — Security and immutable handoffs** | product | Each NS product consumes only declared same-capture immutable XML handoffs through the secure gateway. Hostile content remains inert; undeclared reads, reparsing shortcuts, network access, storage, telemetry, executable source content, and writes outside declared generated products fail. | Gateway, CSP, hostile-vector, source-read lock, immutable-model, and atomic-write tests. |
| **NS-AC-20 — Complete product behavior** | product | Both NS products preserve the established forward/reverse navigation, candidate and passage movement, focus, keyboard operation, state announcements, no-JavaScript reading, print content, typography, reflow, zoom, spacing, reduced-motion behavior, and unobscured target geometry without changing substantive data. | Shared renderer, presentation, guide, accessibility, and pinned-browser matrix tests for all six products. |
| **NS-AC-21 — Fresh deterministic reproduction** | product | An isolated fresh process reproduces every configured candidate byte-for-byte from the retained capture; each sealed HTML equals its candidate; each detached checksum names and authenticates exactly its associated artifact. Missing, extra, stale, alternate, or manually modified products fail. | Fresh-projection, candidate/release equality, checksum, atomic-publication, and exact-inventory tests. |
| **NS-AC-22 — Bundle closure** | bundle | The current bundle contains exactly six ordered sealed HTML/checksum pairs followed by `MANIFEST.txt`, with no missing or additional member, fixed deterministic metadata, a schedule naming all six products, and one exact detached bundle checksum. | Bundle configuration, member-order/count, deterministic ZIP, manifest-origin, and checksum tests. |
| **NS-AC-23 — Aggregate current-state closure** | shared | The Git-independent aggregate gate passes from one retained worktree capture, including all registered tests and final byte/mode/path recapture. The final retained state contains no obsolete four-product control, no shared control that assumes every edition is a strategy, no unregistered NS artifact, and neither this temporary acceptance document nor the coupled plan. | `python -m navigator validate-current`, exact current-state census, and final recapture equality. |
| **NS-AC-24 — Final human review** | final | After `NS-AC-01` through `NS-AC-23` pass, a human reviewer compares the complete filed-claim transcription with the authoritative PDF; reviews all claim status, numbering, dependency, and antecedent results; examines the PCT passage associations and every NS prior-art assessment against the cited evidence; confirms that uncertainties and open DW-05A/DW-08A gates remain visible; and determines whether the two navigators accurately and usefully present the filed application without overstating legal conclusions. Automated validation, implementer self-report, product existence, or prior review cannot satisfy this final criterion. Human review remains authoritative and is not converted into a stored repository approval or validation receipt. | Direct human review of the authoritative PDFs, asserted transcriptions, substantive relations, rendered NS products, and open-gate wording after technical closure. |
