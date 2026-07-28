# AA11393US — Claim/Prior-Art Passage-Map Technical Description

> **OPERATIVE INTERNAL CONTROL · NOT FOR FILING**
>
> This document defines the current semantic contract joining strategy comparison matrices to exact
> prior-art transcription passages. The coupled executable outcomes are in the
> [acceptance criteria](acceptance-criteria_DRAFT.md).

## 1. Purpose and authority

The NA and AF comparison-matrix relation XML files remain the sole owners of strategic
claim-to-document assessments. The corresponding passage-map relation XML files are the sole
owners of normalized obligation state, exact fragment-review allocations, and exact
claim-fragment-to-passage candidates. A passage map does not amend a matrix assessment, and a
transcription endpoint supplies evidence content without adopting the applicant-authored
association.

The current authority direction is:

```text
claim XML + comparison-matrix relation XML
              └──exact relation/field/claim/document normalization──▶ obligation

fragment-review allocation ──exact obligation identities──▶ review-relevant claim unit

candidate ──exact obligation identities──▶ obligation(s)
          ├──subject endpoint────────────▶ exact claim unit or exact phrase
          └──ordered evidence endpoints──▶ exact non-root transcription passages
```

These records are review aids. They do not establish disclosure, anticipation, obviousness,
motivation to combine, claim construction, validity, patentability, or a legal conclusion.

## 2. Current relation profile

Both strategy maps use the sole active `claim-prior-art-passage-map-v2` relation profile. Its closed
record kinds are `obligation`, `fragment-review-allocation`, and `candidate`. Unsupported profiles,
record kinds, fields, aliases, migration readers, dual-format parsing, and compatibility branches
fail before model construction or product writes.

Every relation has one semantic `relationId`, one anchor-only `xml:id`, forward direction, the exact
relation type, the applicant as semantic owner, one exact subject endpoint, and only fields and
endpoint roles enumerated by the active profile.

## 3. Exact obligation census and state

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

Every computed key occurs exactly once. A companion endpoint does not become the primary inventory
document, and every document in a multi-document relationship remains a separate obligation.

Each `record-kind=obligation` relation has one exact claim-root subject, one exact prior-art
document-root evidence endpoint, `matrix-relation-id`, `matrix-field`, and exactly one current
`obligation-status`:

| State | Current meaning |
|---|---|
| `passage-mapped` | At least one exact candidate is bound to this obligation. |
| `counsel-review-required` | The matrix records a material relationship and no exact candidate is bound. |
| `reviewed-no-material-passage` | The exact controlling matrix field is `—`; no passage is required for that field. |

The no-material state says nothing about another claim, field, relationship, or document. Absence
of a candidate never becomes an absence conclusion.

Candidate admissibility closes before obligation coverage. Only a candidate that passes exact
subject, phrase, role, obligation, document, endpoint, digest, duplicate, and preamble validation
may contribute a referenced obligation. Coverage is recomputed from that accepted candidate set.
A rejected or removed candidate contributes no residual `passage-mapped` state; an authored state
that no longer closes against the accepted set fails the model.

## 4. Exact fragment-review allocations

A `record-kind=fragment-review-allocation` relation records that one or more unresolved
claim-level obligations are relevant to one exact claim unit. It has:

- one exact claim-unit subject endpoint;
- no evidence endpoint and no exact-phrase selector;
- one sorted, duplicate-free `obligation-ids` list naming only `counsel-review-required`
  obligations for the same claim;
- one nonblank neutral `relevance-note`;
- no status field and no passage assertion.

An allocation owns relevance only. It does not duplicate obligation state, assert that a feature is
present or absent, or satisfy an obligation. The semantic signature is `(subject endpoint,
obligation-ids)`; a repeated signature fails even when the relation identity or note differs.
Allocations arise only through explicit authorship. Claim ancestry, matrix prose, textual
similarity, search results, defaults, and candidate inheritance never create them.

## 5. Exact candidates and multiplicity

A `record-kind=candidate` relation has:

- one exact claim-unit subject endpoint and, optionally, one exact phrase that occurs once in that
  unit;
- one or more ordered, digest-bound, non-root transcription evidence endpoints;
- one `candidate-role` of `specific`, `combination`, or `context`;
- one nonblank neutral `proposition`;
- one sorted, duplicate-free `obligation-ids` list.

One exact unit or phrase may own zero, one, or many candidates. One mapped obligation may support
several substantively distinct fragment candidates. Candidate identity remains independent from
passage-member identity: a true combination is one candidate with several ordered passages, and
each passage remains individually navigable without splitting or changing the combination.
The ordered evidence list is the sole candidate-member state. No primary-member alias, cached
current passage, copied target list, or equivalent second selection plane exists in the semantic
model.

The candidate obligation list and evidence endpoints close bidirectionally by claim and exact
document set. Every named obligation is `passage-mapped`; every passage-mapped obligation is named
by at least one candidate. A candidate cannot satisfy a different claim, an unlisted document, a
matrix relationship that is merely similar in wording, or a non-mapped obligation.

The candidate semantic signature is `(subject endpoint, exact phrase, role, obligation-ids,
canonical evidence-endpoint identity set)`. Authored evidence order remains operative for
presentation and passage movement, but reordering the same endpoints does not create a distinct
candidate. A repeated signature fails even when relation identity, proposition, or endpoint order
differs. Repeating an evidence endpoint within one candidate also fails.

A claim-root preamble is an exact text unit, not a whole-claim aggregation surface. A preamble
candidate therefore cannot be a combination, name more than one obligation, or target more than
one evidence document. Whole-claim or multi-limitation roll-ups do not remain in the map.

## 6. XML handoff and authoring boundary

Each strategy consumer receives its claim XML, comparison-matrix relation XML, passage-map relation
XML, and every prior-art transcription XML package in matrix scope. The handoff set is computed
against the matrix census. A scope addition requires its registered XML handoff and exact
obligations; no document allowlist or fallback reader exists.

Search or ranking may assist human review only ephemerally. Suggestions have no live authority and
are not retained. Only explicitly authored allocations and candidates enter the relation XML. The
source PDF remains the fidelity authority; candidate passages and visible transcription uncertainty
must be checked against it, especially for OCR-derived content.

## 7. Current-state closure

The contract pair, data-only acceptance registry, active profile, matrices, passage maps, generated
review projections, declared handoffs, model enforcement, adverse vectors, consuming products, and
live-path census are accepted only as one retained current state. Coverage and status counts are
recomputed and never stored as separate authority artifacts.

Acceptance fails for a missing or extra obligation, stale digest, unsupported profile or record,
duplicate or endpoint-permuted semantic signature, synthetic preamble roll-up, invalid allocation,
candidate without exact obligation closure, mapped obligation without an accepted candidate,
no-material state over non-dash matrix content, undeclared transcription, copied selection state,
inferred semantics, compatibility path, or orphaned implementation.

The sole execution boundary is the shared [aggregate validation
boundary](../../README.md#aggregate-validation-boundary). It proves current technical coherence and
deterministic reproducibility only; substantive and legal review remains human and authoritative.
