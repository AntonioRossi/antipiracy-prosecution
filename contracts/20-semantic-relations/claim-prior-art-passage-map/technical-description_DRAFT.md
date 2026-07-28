# AA11393US — Claim/Prior-Art Passage-Map Technical Description

> **OPERATIVE INTERNAL CONTROL · NOT FOR FILING**
>
> This document defines the current semantic contract joining strategy comparison matrices to exact
> prior-art transcription passages. The coupled executable outcomes are in the
> [acceptance criteria](acceptance-criteria_DRAFT.md).

## 1. Purpose and authority

The NA and AF comparison-matrix relation XML files remain the sole owners of strategic
claim-to-document assessments. The corresponding passage-map relation XML files own only the
normalized obligation state and any exact claim-fragment-to-passage candidate association. A
passage map does not amend a matrix assessment, and a transcription endpoint supplies evidence
content without adopting the applicant-authored association.

The current authority direction is:

```text
claim XML + comparison-matrix relation XML
              └──exact relation/field/claim/document normalization──▶ passage-map obligation

passage-map candidate ──exact obligation identities──▶ obligation(s)
              ├──subject endpoint──▶ exact claim unit or exact phrase
              └──evidence endpoint──▶ exact non-root transcription passage
```

These records are review aids. They do not establish disclosure, anticipation, obviousness,
motivation to combine, claim construction, validity, patentability, or a legal conclusion.

## 2. Exact obligation census

An obligation key is the exact tuple `(matrix relation ID, matrix field, claim number, prior-art
document ID)`. The immutable model independently computes the complete key census from the matrix:

- each NA independent-claim inventory field yields one obligation for its named claim and primary
  inventory document;
- each AF integrated-claim inventory field yields its own claim 1/document obligation;
- each scored AF method or monitor row yields one obligation for its exact subject claim and primary
  inventory document;
- each claimed relationship or claimed operation yields one obligation for every named prior-art
  document;
- each dependent-claim matrix row yields one obligation for every exact claim in its declared range
  and every named prior-art document.

Every computed key occurs exactly once in the passage map. A companion or cross-reference endpoint
does not become the primary inventory document; multi-document relationship endpoints each remain
separate obligations. Parent ancestry does not create an obligation or candidate for a child.

## 3. Obligation records and current states

Each `record-kind=obligation` relation has one exact claim-root `subject`, one exact prior-art
document-root `evidence` endpoint, and these fields:

- `matrix-relation-id` — the controlling comparison-matrix relation;
- `matrix-field` — the exact controlling assertion field;
- `obligation-status` — exactly one current state.

The state vocabulary is:

| State | Current meaning |
|---|---|
| `passage-mapped` | At least one exact candidate is bound to this obligation. |
| `counsel-review-required` | The matrix records a material relationship and no exact candidate is bound. |
| `reviewed-no-material-passage` | The exact controlling matrix field is `—`; no passage is required for that field. |

The no-material state says nothing about another claim, matrix field, relationship, or document.
Absence of a candidate never becomes an absence conclusion.

## 4. Candidate records

Each `record-kind=candidate` relation has one exact claim-unit subject, one or more digest-bound
non-root transcription evidence endpoints, a profiled candidate role, a neutral proposition, and a
sorted exact `obligation-ids` list. An optional exact phrase must occur once in its subject unit.

The obligation list and evidence endpoints close bidirectionally by document and claim. Every named
obligation is `passage-mapped`; every passage-mapped obligation is named by a candidate. A candidate
cannot satisfy a different claim, an unlisted document in a combination, a matrix relationship that
is only similar in wording, or an obligation with either non-mapped state.

## 5. Complete XML handoff boundary

Each strategy consumer receives its claim XML, comparison-matrix relation XML, passage-map relation
XML, and every prior-art transcription XML package in the matrix scope. The handoff set is computed
against the matrix census. Adding a matrix-scope document therefore requires its registered XML
handoff and exact obligation records; no source identifier allowlist, fallback reader, or
compatibility branch exists.

The source PDF remains the fidelity authority. Candidate quotations and transcription uncertainty
must be checked against that PDF, especially for OCR-derived content.

## 6. Closure and failure

The contract pair, data-only acceptance registry, exclusive relation profile, matrices, passage
maps, generated review projections, declared handoffs, model enforcement, tests, and consuming
products are accepted only as one retained current state. Coverage is recomputed and never stored
as an authority artifact.

Acceptance fails for a missing or extra obligation, stale digest, unsupported record kind or state,
candidate without exact obligation closure, mapped obligation without a candidate, no-material
state over non-dash matrix content, undeclared transcription, copied or inferred semantics,
compatibility path, or orphaned implementation.

The sole execution boundary is the shared [aggregate validation
boundary](../../README.md#aggregate-validation-boundary). It proves current technical coherence and
deterministic reproducibility only; substantive and legal review remains human and authoritative.
