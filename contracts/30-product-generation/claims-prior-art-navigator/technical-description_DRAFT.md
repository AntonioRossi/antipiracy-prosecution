# AA11393US — Claims-to-Prior-Art Navigator Technical Description

> **OPERATIVE INTERNAL CONTROL · NOT FOR FILING**
>
> This document defines the current NA and AF claims-to-prior-art HTML5 products. The paired
> executable outcomes are in the [acceptance criteria](acceptance-criteria_DRAFT.md).

## 1. Product outcome and legal boundary

The current product inventory contains one claims-to-prior-art navigator for the normal-allowance
claim set and one for the allowance-first claim set. Each product lets inventor and US counsel move
from an exact claim unit or exact selected phrase to applicant-recorded candidate passages, inspect
every matrix claim/document obligation and current state, open the complete asserted transcription
at a mapped passage, and move from each displayed passage back to the related claim fragments.

The navigator is a review aid. A recorded association is not a conclusion that a document discloses
a limitation, anticipates a claim, renders a claim obvious, establishes a legal combination, or has
any other legal effect. “Counsel review required” states that a material matrix relationship lacks
an exact bound passage candidate; it does not state that the feature is present or absent.
“Reviewed — no material passage required” is limited to its exact matrix field. Human review of the source PDF, transcription
uncertainty, the claim as a whole, and the applicable law remains authoritative.

## 2. Exact authority direction

The current data flow is:

```text
claim-set Markdown
  └─generated authoritative XML claim surface──────────────┐
                                                            │
strategy prior-art comparison-matrix relation XML──────────┼─▶ immutable product model
  └─owns the exact current document scope                   │
                                                            │
strategy claim/prior-art-passage-map relation XML──────────┤
  ├─owns every normalized matrix obligation and state       │
  └─owns every obligation-bound exact candidate             │
                                                            │
registered prior-art transcription XML─────────────────────┘
  └─supplies exact digest-bound passage content and provenance

immutable product model ─▶ self-contained HTML5 ─▶ checksum ─▶ four-product bundle
```

The comparison matrix remains the sole owner of the strategic document-level comparison and the
current 33-document scope. The dedicated passage map is the sole owner of normalized
matrix-relation/field/claim/document obligation states and exact claim-fragment candidate
associations. The product independently computes the complete obligation census from matrix XML,
but never derives a candidate from matrix prose, scores, whole-document endpoints, claim wording,
text similarity, search results, or rendered Markdown review views.

Each prior-art package's canonical source PDF remains the fidelity authority. Its asserted
`pdf-evidence-transcription-v1` XML is the sole machine-readable passage surface. The product never
reads an OCR convenience derivative or treats transcription text as a substitute for checking the
PDF.

## 3. Authoritative passage-map relation package

The two current relation packages are:

- `aa11393us-na-claim-prior-art-passage-map`;
- `aa11393us-af-claim-prior-art-passage-map`.

They use `claim-prior-art-passage-map-v1`. Every relation has one semantic `relationId`, one
anchor-only `xml:id`, the applicant as semantic owner, forward direction, the exact relation type,
and only profile-enumerated fields and endpoint roles.

### 3.1 Matrix obligations

Every obligation computed under the dedicated phase-20 semantic contract occurs exactly once as a
`record-kind=obligation` assertion. It binds one exact claim root and one exact matrix-named
prior-art document root to the controlling matrix relation and field. Its state is
`passage-mapped`, `counsel-review-required`, or `reviewed-no-material-passage`; the last state is
valid only when the exact matrix field is `—`.

The NA map contains 218 obligations: 33 passage-mapped, 152 counsel-review-required, and 33
reviewed-no-material-passage. The AF map contains 264 obligations: 29 passage-mapped, 199
counsel-review-required, and 36 reviewed-no-material-passage. These states expose the current
review gap instead of treating one passage for a claim unit as coverage of every matrix-named
document.

### 3.2 Candidate assertions

A `record-kind=candidate` assertion has:

- one exact claim-unit `subject` endpoint;
- one or more exact prior-art `evidence` endpoints;
- one `candidate-role` of `specific`, `combination`, or `context`;
- one sorted `obligation-ids` list covering the same claim and evidence-document set;
- one nonblank `proposition` describing why those passages were recorded together;
- optionally one `subject-exact-text` that must occur exactly once as a contiguous substring of the
  subject claim unit.

Each evidence endpoint resolves through the retained structured-source interface to one prior-art
transcription item and its typed-item digest. Every matrix-scope document has its own declared XML
consumer edge. A document-root endpoint is not a passage candidate. A stale digest, undeclared
package, non-unique phrase, target outside matrix scope, unbound obligation, relation-to-relation
target, or missing transcription handoff fails closed.

The current grounded candidate inventory contains 58 NA and 47 AF relations, resolving to 15
non-root passages across A4, A5, A6, A13, A20, A21, and B9. A claim unit's displayed mapped or
review-required state is computed from these candidates; it is not another authored state plane.
Candidate relations that cannot close against a matrix obligation do not remain in the map.

## 4. Current immutable model

One retained worktree capture supplies the product control, parser controls, content registry,
claim handoff, comparison-matrix handoff, passage-map handoff, all 33 matrix-scope prior-art
transcription handoffs, controlled wording, and schemas. All structured-source domains validate once before model
construction.

The immutable model preserves:

- product, strategy, claim-set, artifact, consumer, and relation-set identities;
- claim hierarchy, claim units, dependencies, group order, text, and typed digests;
- the exact 33-document matrix scope;
- every exact matrix obligation and current state, plus every exact phrase selector and candidate group;
- target passage text, page, region, transcription uncertainty, typed digest, and complete XML reader tree;
- forward and reverse relation indexes;
- controlled legal/status wording and its computed slot origins;
- every source XML role, registered path, XML byte digest, and complete read lock.

Construction accepts no unresolved-as-empty lookup, default, inferred package, reopened source path,
mutable parse tree, detached validation result, or product-local copy of relation semantics. The
render and release stages receive only the sealed model.

## 5. HTML5 review surface

Each product is a self-contained UTF-8 HTML5 file with two coordinated panes:

- the left pane displays the exact strategy claim hierarchy and makes every claim unit selectable;
- the right pane displays all 33 in-scope prior-art documents, every matrix obligation and state,
  every currently mapped passage, and one complete asserted-XML transcription reader per document.

For a mapped unit or phrase, candidate controls identify the role and proposition, navigate to all
passage endpoints in deterministic order, and cycle without changing the relation semantics. A
passage card shows its document ID, stable passage anchor, page, region, uncertainty when present,
and transcription text. Its reverse badge selects the related claim fragments. Its contextual-reader
control opens the complete transcription, scrolls to the same exact fragment, and places keyboard
focus there without changing browser history. Clearing selection removes transient state and
returns focus predictably.

The full readers are generated directly from every declared matrix-scope transcription handoff.
They are not activated by a document allowlist. Adding a matrix-scope document makes its reader
mandatory in the same current state, whatever its obligation states.

The ordinary document, complete mapping schedule, and print view contain every substantive claim,
status, candidate proposition, passage, provenance item, and disclaimer outside script data. With
JavaScript disabled, the complete state remains readable. Dependent-claim ancestry is computed from
claim XML and never presented as an authored passage mapping for a child claim.

Static HTML uses semantic controls, logical document order, keyboard-operable actions, visible focus,
non-color status indicators, a live region, reduced-motion rules, bounded independent pane scrolling,
minimum usable dimensions, and a deterministic stacked layout below the two-pane threshold.

## 6. Security and wording

The product contains no network request, telemetry, cookie, browser storage, location/history
mutation, external asset, form submission, or dynamic code loading capability. Its exact content
security policy denies all capabilities except inline product CSS/JavaScript and embedded data
images. All dynamic text is context-escaped before insertion into HTML or inert JSON.

The prior-art wording XML owns the confidentiality legend, standing disclaimer, mapping statuses,
candidate-role labels, evidence-authority statement, provenance wording, product label, preview
watermark, and neutral bundle statement. Product code cannot replace or soften this wording.

## 7. Product controls, commands, and publication

The current exact product IDs are:

- `na-specification`;
- `af-specification`;
- `na-prior-art`;
- `af-prior-art`.

`preview`, `candidate`, and `release` require one of those exact IDs. No shorter command identity or
implicit product choice exists. Each product control closes its strategy, consumer, claim package,
claim version, evidence kind, wording, artifact name, declared timestamp, claim census, and groups.

Candidate generation writes only the declared candidate path. Release requires that candidate's
exact bytes and a fresh isolated reproduction, then writes the sealed HTML and detached checksum as
one prevalidated output map. The bundle contains four ordered HTML/checksum pairs followed by the
neutral manifest. It is deterministic ZIP STORE output with fixed metadata and its own detached
checksum. Candidate, release, and bundle writes exact-read every output and reject any concurrent
change outside their declared paths.

No former two-product bundle, alternate HTML generator, duplicate renderer, stored validation
result, release receipt, approval record, or auxiliary lineage/coverage product belongs to the live
state.

## 8. Current-state closure and regeneration workflow

The dedicated contract pair, data registry, controls, implementation, tests, generated views,
stored products, and declared handoffs form one indivisible current implementation.

A passage-map content change is complete only when all affected current owners agree:

1. reconcile every computed matrix obligation and author or remove its exact candidate relation;
2. declare every matrix-scope prior-art XML package edge;
3. regenerate the map's Markdown review projection;
4. run focused map, model, render, security, release, and bundle tests;
5. regenerate candidate and sealed prior-art HTML, checksums, and the four-product bundle;
6. pass the sole aggregate gate with an unchanged final recapture.

Changing claim wording additionally requires the repository's claim count, dependency, antecedent
basis, support-mapping, matrix, and art-rescoring checks. Changing a prior-art transcription requires
checking the source PDF and preserving visible uncertainty. Machine acceptance cannot establish
that the mapping is complete or legally correct.

<!-- CURRENT-VALIDATION-BOUNDARY:START -->
The sole aggregate current-state workflow is the shared
[aggregate validation boundary](../../README.md#aggregate-validation-boundary):

```sh
uv --no-cache --offline run --locked --no-sync python -m navigator validate-current
```

It validates technical coherence and deterministic reproducibility only. It does not establish
source authenticity, transcription fidelity, factual or legal correctness, completeness of
prior-art or support analysis, inventor confirmation, counsel approval, filing readiness or
authorization, or entitlement to rely on the package without reviewing its evidence. Human review
of source evidence and substantive analysis remains authoritative.
<!-- CURRENT-VALIDATION-BOUNDARY:END -->

## 9. Failure conditions

Acceptance fails for any missing or extra product, consumer, map package, matrix obligation, scope
document, full reader, target handoff, generated view, stored product, checksum, bundle member,
implementation path, contract, registry, schema, test, or vector. It also fails for stale or
whole-document passage targets, inconsistent obligation/candidate closure, inferred or copied semantics, hostile unescaped content,
forbidden browser capability, nondeterministic bytes, partial publication, alternate command path,
or any retained obsolete or orphaned implementation.
