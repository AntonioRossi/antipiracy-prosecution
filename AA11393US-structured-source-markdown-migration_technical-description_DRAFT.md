# AA11393US — Structured-Source Markdown Migration: Technical Description (DRAFT)

> **PROPOSED ARCHITECTURE · INTERNAL DRAFT · STATUS 24 JULY 2026**
>
> This document specifies the first of two one-way migrations. It establishes canonical XML
> sources, deterministic Markdown review projections, early human approval, and a discoverable
> `US/` content layout. It does not change the navigator's HTML5 consumption path.
>
> The coupled acceptance contract is
> [`AA11393US-structured-source-markdown-migration_acceptance-criteria_DRAFT.md`](AA11393US-structured-source-markdown-migration_acceptance-criteria_DRAFT.md).
> The subsequent navigator migration is specified separately in
> [`AA11393US-structured-source-html5-migration_technical-description_DRAFT.md`](AA11393US-structured-source-html5-migration_technical-description_DRAFT.md).
> Neither draft authorizes a filing, release, or claim that the proposed implementation exists.

## 1. Rationales

1. **Make semantic structure explicit before conversion.** Direct PDF-to-Markdown conversion
   hides extraction, ordering, and classification decisions inside prose. A typed XML passage
   makes those decisions inspectable before any review view or consumer artifact is generated.
2. **Move human review to the earliest stable representation.** Reviewers can compare a
   deterministic Markdown projection with the evidentiary PDF or authored content while every
   visible fragment still maps to a stable XML identity.
3. **Support exact cross-document references.** Claims, limitations, quotations, prior-art
   passages, support passages, and analytical assertions require stable fragment identities and
   stand-off relations. File names, XPath expressions, text offsets, and copied quotations are
   too brittle to be relation identity.
4. **Keep authority truthful.** A stored prior-art PDF remains the evidentiary source. Its XML is
   a canonical structured derivative, not an official replacement. For repository-authored
   material, XML is the primary canonical authoring source. Generated Markdown is never an
   independently editable authority.
5. **Separate content acceptance from renderer migration.** The repository can first prove that
   XML regenerates reviewed Markdown without changing the current navigator. The later HTML5
   cutover can then be tested against an already accepted upstream contract.
6. **Improve discoverability without duplicating ownership.** Shared records, strategy-specific
   material, and prior-art evidence need stable, role-revealing locations. A controlled taxonomy
   prevents strategy forks of shared facts and scattered prior-art derivatives.
7. **Fail closed and reproduce exactly.** Closed schemas, secure parsing, canonical digests,
   complete inventories, deterministic rendering, and exact-side approvals prevent an
   unreviewed or stale source from becoming consumer-eligible.
8. **Keep the live tree current-state-only.** Migration archives, comparison reports, aliases,
   compatibility readers, and implementation narratives are temporary. Git alone retains the
   history after acceptance.

## 2. Implementation goals

The implementation shall:

1. inventory every in-scope authored Markdown document, PDF-derived transcription, stored PDF,
   searchable/OCR convenience copy, asset, and cross-document semantic relation;
2. assign one stable document identity and stable fragment identities to every addressable
   semantic unit;
3. encode canonical content in closed `.source.xml` packages and source-level stand-off
   assertions in closed `.relations.xml` packages;
4. distinguish stored evidence, canonical derivatives, authored canonical sources, generated
   review views, convenience copies, and analytical relations without overstating authority;
5. validate XML with secure, resource-bounded parsers and current closed schemas before any
   generated output is written;
6. provision the Python implementation from repository-owned project metadata and an exact lock
   through a host-provided, version-checked `uv`, without a pip or ambient-site-packages fallback;
7. compute raw byte digests and domain-separated canonical semantic digests under one pinned
   canonicalization law;
8. render GitHub-flavored Markdown and review-coverage records deterministically from accepted
   XML and locked assets only;
9. make every author-controlled semantic field review-visible or explicitly justified as a
   mechanical/internal field;
10. require identified-human projection and source/content approvals bound to exact source,
   dependency, asset, renderer, Markdown, and coverage digests;
11. reorganize `US/` into discoverable shared, strategy, and per-prior-art packages while
    preserving a single owner for shared material;
12. export an exact approved structured package for downstream consumers without embedding
    semantic content in a JSON envelope;
13. export one consumer-neutral exact package while keeping generated Markdown solely as the
    approved human review projection;
14. archive the pre-migration Markdown state temporarily, compare every regenerated view with
    that baseline, obtain human visual disposition, and delete the archive and all migration
    residue before recurring acceptance; and
15. provide a closed handoff that the HTML5 migration can consume without redefining XML,
    identity, digest, approval, or Markdown rules.

## 3. Scope and boundary

### 3.1 Included content plane

This specification controls:

- current authored and PDF-derived Markdown under `US/` and the registered PCT material used by
  the US prosecution package;
- canonical `.source.xml` files created for that material;
- source-level `.relations.xml` files needed to express semantic assertions currently carried by
  those documents, including claim-to-support and claim-to-prior-art mappings;
- stored source PDFs, registered assets, and their provenance manifests;
- deterministic Markdown review views and coverage records;
- the structured-source registry, schemas, render profiles, and append-only exact-side human
  approval records;
- repository-owned Python project metadata, the exact `uv` lock, interpreter constraint, required
  host `uv` version, and the closed implementation-source/dependency inventory; and
- repository links and routers affected by the `US/` reorganization.

### 3.2 Explicit exclusions

This first migration does not:

- replace the navigator's Markdown reader with an XML reader;
- migrate navigator-owned relation JSON, UI wording, templates, release policy, QA evidence,
  candidate generation, bundles, or HTML5 rendering;
- change patent claims merely to ease conversion;
- edit a canonical prior-art PDF or promote OCR/searchable text to evidentiary authority; or
- authorize release artifacts solely because the structured-source package passes.

During implementation, current navigator behavior remains governed by
[`AA11393US-claims-navigator_technical-description_DRAFT.md`](AA11393US-claims-navigator_technical-description_DRAFT.md)
and its existing acceptance controls. Proving that it still functions from regenerated Markdown is
part of the one-time gate in §14, not a recurring structured-source criterion or dependency of the
approved export.

### 3.3 Authority vocabulary

| Term | Operative meaning |
|---|---|
| Stored evidentiary source | An exact registered PDF or other external source byte sequence used to assess derivative fidelity |
| Canonical structured derivative | XML derived from a stored source; authoritative for workflow structure but subordinate to the stored source for fidelity |
| Canonical authored source | XML that is the primary repository-authored expression of the content |
| Review projection | Deterministic Markdown generated from XML for human inspection; never edited independently |
| Convenience derivative | OCR, searchable PDF, or extraction aid that assists review but cannot authorize content |
| Stand-off relation | A separately owned assertion that binds exact identified fragments without copying their text |
| Approved structured package | Exact-current XML, locked dependencies/assets, coverage, Markdown, and human approvals eligible for downstream consumption |

The phrase “source of truth” is intentionally avoided where it would collapse evidentiary and
workflow authority. The applicable origin branch determines which authority controls each
question.

## 4. Forward architecture

The first migration has one forward-only path:

```text
stored PDF or repository-authored content
                    │
                    ▼
       canonical .source.xml package
                    │
       ┌────────────┴────────────┐
       ▼                         ▼
.relations.xml assertions   locked assets/dependencies
       └────────────┬────────────┘
                    ▼
 secure validation + canonical digest
                    ▼
 deterministic Markdown + coverage
                    ▼
 identified-human exact-side approvals
                    ▼
       approved structured package
                    │
                    └── consumer-neutral exact export
```

No reverse import from Markdown is part of the operative architecture. Conversion of current
Markdown into XML exists only in the draft-only migration gate in §14 and is removed at cutover.

### 4.1 Plane separation

The live implementation separates:

- **content XML**, which owns document semantics;
- **relation XML**, which owns cross-document assertions;
- **control JSON**, which may contain only paths, IDs, profiles, versions, digests, allowlists,
  limits, and policy switches defined by closed schemas;
- **generated Markdown**, which is a review surface;
- **approval records**, which bind exact reviewed sides but do not copy semantic content; and
- **consumer exports**, whose envelopes are control-only and whose semantic payload is XML.

Within the upstream source/export plane controlled by this document, persisted content, relation
meaning, quotations, prosecution prose, or human-visible wording shall not be encoded in JSON.
Navigator-owned relation and wording JSON remains outside this first-stage scope until the
separate HTML5 cutover.

## 5. Canonical XML contract

### 5.1 Files, namespaces, and profiles

Canonical content files use the suffix `.source.xml` and the namespace
`urn:aa11393:ssp:content:1`. Stand-off relation files use `.relations.xml` and the namespace
`urn:aa11393:ssp:relations:1`. Each file declares exactly one closed schema profile and one
current schema version. Unknown namespaces, elements, attributes, enumeration values, profiles,
or versions fail closed.

The content envelope contains, in schema-defined order:

- `documentIdentity`: global `documentId`, artifact family, jurisdiction, strategy/shared scope,
  status, language, and title;
- `origin`: exactly one `pdfDerivative` or `authoredSource` branch;
- `dependencies`: exact document, relation, and asset bindings allowed during projection;
- `provenance`: source roles, responsible owner, and origin-specific evidence;
- `content`: the typed ordered semantic tree; and
- `projectionPolicy`: the registered Markdown profile and allowed generated notices.

The typed tree supports headings, paragraphs, inline emphasis, defined terms, quotations,
citations, lists, tables, claims, claim dependencies, limitations, notes, cautions, actions,
figures, links, and profile-specific fields. Raw Markdown, raw HTML, CDATA-based semantic
escapes, executable templates, or opaque “miscellaneous” fields are prohibited.

### 5.2 Stable fragment identity

Every addressable semantic unit has one XML `xml:id`, unique within its document and stable while
the unit retains its identity. Identity is not an XPath, ordinal, page number, byte offset, or
text excerpt. A fragment's current semantic binding is:

```text
(documentId, fragmentId, fragmentContentDigest)
```

The fragment digest is computed from the schema-defined canonical fragment domain, including
the semantic element and attributes that determine its meaning. Changing text or a substantive
attribute changes the digest while preserving the stable ID when the same conceptual fragment is
being amended. Splitting, merging, or repurposing a fragment requires new IDs and updated
relations.

Claims additionally carry a stable claim ID, claim number, type, dependency set, and ordered
limitations. Validators prove claim count, dependency legality, antecedent-basis inputs, and
one-to-one fragment coverage before projection.

### 5.3 Origin branches and provenance

A `pdfDerivative` binds:

- the exact stored PDF path, raw SHA-256 digest, size, and registered source role;
- truthful official-copy status without inference from file name or location;
- page and, where needed, region locators for derived fragments;
- extraction method and identified uncertainty requiring human resolution;
- exact registered figures/assets and their digests; and
- any OCR/searchable/extraction aid as a non-authoritative convenience derivative.

An `authoredSource` binds:

- the responsible content owner;
- artifact family, current status, and review scope; and
- declared dependencies and assets without inventing an external authority.

No workflow may silently select OCR over a stored PDF, infer official status, or present an
authored analysis as counsel advice or source fact.

### 5.4 Stand-off relations

Cross-document assertions are stored outside endpoint documents so that claim text and prior-art
text remain independent of the analysis relating them. Each relation set has a stable
`relationSetId`, profile, semantic owner, scope, and complete endpoint-version bindings. Each
relation has a stable `relationId`, typed direction, typed assertion/profile fields, review owner,
and one or more endpoint tuples.

Relation identity is:

```text
(relationSetId, relationId, relationContentDigest)
```

An endpoint uses the exact tuple from §5.2. It never uses copied endpoint text as identity. XPath,
unversioned fragment IDs, fuzzy matching, offsets, or a file path alone are prohibited. A relation
becomes stale when any endpoint digest changes and cannot resolve until the assertion is reviewed
against the new endpoint.

The generic relation envelope is controlled here. Source-level profiles may express, for example:

- claim or limitation → written-description support;
- claim or limitation → prior-art passage;
- quotation → cited source passage;
- action or caution → supporting analysis; and
- shared fact → strategy-specific use.

Navigator-only relation profiles and their semantic approval remain outside this first migration.
They may reuse this envelope only under the second specification and may not override an SSP-owned
assertion.

## 6. Secure parsing, canonicalization, and identity

### 6.1 Closed validation

Schemas use [W3C XML Schema 1.1](https://www.w3.org/TR/xmlschema11-1/) and stable identities use
the [W3C `xml:id` recommendation](https://www.w3.org/TR/xml-id/). XML is UTF-8 XML 1.0 and Unicode
text is normalized to NFC before semantic validation. The parser:

- disables DTDs, entity declarations, non-predefined entity references, XInclude, XLink,
  `xml:base`, external schemas, external resources, network access, and parser recovery;
- rejects comments and processing instructions in canonical packages;
- enforces schema-defined maximum byte size, depth, node count, attributes, text length, table
  dimensions, dependency count, relation count, and endpoint count; and
- resolves paths only through the materialized registry view inside the repository root.

Validation order is bytes → secure parse → namespace/schema → semantic invariants → dependency
and endpoint closure → digest resolution → approval resolution. No writer runs before all input
checks applicable to its output have passed.

### 6.2 Canonical and raw digests

Every controlled XML file has:

- a raw byte digest labeled `sha256/raw`; and
- an authorizing semantic digest labeled `sha256/xc1/ssp-xd1`.

`xc1` is the pinned implementation profile of
[Canonical XML 1.1 without comments](https://www.w3.org/TR/xml-c14n11/), augmented only by the
closed preconditions above. `ssp-xd1` frames the canonical bytes with unambiguous length-prefixed
domain fields including artifact kind, namespace, schema profile/version, stable subject ID, and
canonicalization version. The shared domain registry maps each closed artifact kind to its exact
subject-ID field and canonical payload grammar: `documentId` for a whole content document and
`relationSetId` for a whole relation set. A downstream XML kind may use the same law only after its
unique artifact kind, stable subject-ID field, namespace/schema version, and whole-payload grammar
are registered here; this registration supplies identity framing, not ownership of the downstream
semantics. A raw digest cannot substitute for the domain-framed semantic digest, and neither label
may be inferred.

Control JSON uses a separate closed `canonVersion c1` for RFC-style deterministic object
serialization defined by the implementation contract. Control JSON cannot enter an XML semantic
digest as though it were content; it is bound as a separately typed dependency when needed.

### 6.3 Host-provided `uv` and repository-provisioned Python environment

The repository root owns `pyproject.toml`, `uv.lock`, `.python-version`, and the applicable `uv`
configuration. Together they close the supported Python version, the exact required host `uv`
version, every direct and transitive runtime/test dependency, dependency source, distribution hash,
and install group used by structured-source commands or callbacks. The implementation-source
inventory binds these files and every imported project module. An undeclared import, editable
third-party source, ambient `PYTHONPATH`, user-site package, or dependency resolved outside the
locked project environment is a failure.

The host provides the cross-platform `uv` executable as an execution capability. Repository
configuration checks its exact pinned version before any environment or structured-source command;
the executable and an operating-system-specific binary are not committed as repository content.
The only environment-creation operation is the documented explicit bootstrap equivalent to
`uv --no-cache sync --locked --all-groups`, which first rejects a stale lock and then creates the
project-local `.venv` from the committed lock without invoking pip or using a host cache. Network
access may occur only during that separately invoked bootstrap. The environment directory and any
ephemeral package-manager scratch directory are untracked, non-authoritative conveniences and
cannot enter a source, approval, export, or acceptance digest.

Recurring verification runs through the already provisioned environment, equivalent to
`uv --no-cache --offline run --locked --no-sync python -m navigator validate-current`. It checks
project/lock consistency but performs no dependency resolution, installation, persistent cache
write, or environment write and fails closed when `uv`, the interpreter, the lock, the environment,
or any installed distribution differs from the closed contract. It never falls back to `pip`, a
system interpreter, ambient site packages, or an unlocked install. The verifier binds the exact
project, lock, interpreter, `uv`, and installed-distribution census to its ephemeral callback
receipt, then proves that neither the repository nor its project environment changed during the
run.

### 6.4 Registry and closure

One closed repository registry enumerates every content package, relation set, dependency,
endpoint allowlist, source/asset role, Markdown view, coverage record, required approval type,
consumer, and export path. It locates relation sets but does not restate individual assertions.

Validation is bidirectional. A separate closed record inventory owns the append-only approval
namespace; schema-valid same-version records that are not exact-current remain superseded evidence,
not orphans and not current authorizations. For the content registry:

- every registered controlled file exists at its exact path;
- every controlled file is registered exactly once;
- global document, relation-set, asset, and output IDs/paths are unique;
- each `(documentId, fragmentId)` and `(relationSetId, relationId)` tuple is unique in scope;
- all dependencies and endpoints resolve to exact current digests;
- shared material has one owner; and
- no orphan source, relation, asset, view, or coverage record exists.

## 7. Deterministic Markdown review projection

### 7.1 Projection inputs and outputs

A renderer reads only:

- one validated source or relation XML package;
- exact registered dependency XML and endpoint bindings;
- exact registered assets;
- a closed Markdown projection profile; and
- control-only registry data explicitly allowed by that profile.

It produces a Markdown view and a machine-verifiable coverage record atomically. Fresh processes
given the same locked inputs must produce byte-identical outputs. The committed output must equal
fresh regeneration and render successfully as GitHub-flavored Markdown.

Each generated Markdown file begins with a fixed generated-file notice that identifies the source
document or relation set, its authorizing semantic digest, the projection profile, and the command
used to verify/regenerate it. The notice states that edits belong in XML. It shall not copy
uncontrolled migration commentary into the live document.

### 7.2 Rendering law

The closed profile defines:

- heading depth and stable generated anchors;
- paragraph, list, quotation, claim, limitation, table, figure, link, citation, status, caution,
  and action rendering;
- deterministic ordering for schema-unordered control collections;
- whitespace, escaping, Unicode, line endings, and final-newline behavior;
- stable relative-link computation after path validation;
- deterministic presentation of relation direction, endpoints, assertion fields, provenance, and
  review owner; and
- fixed generated provenance notices that may be excluded from old/new semantic comparison only
  by explicit field identity.

The renderer cannot evaluate arbitrary templates, execute embedded code, fetch external content,
or obtain semantics from another Markdown file.

### 7.3 Review completeness

The coverage record classifies every author-controlled XML element, attribute, and text field as
exactly one of:

- `review-visible`, with one or more Markdown anchors;
- `review-scheduled`, where a relation/dependency field is shown in a deterministic review table;
- `mechanically-derived`, with a registered derivation ID and inputs; or
- `internal-justified`, with a closed non-semantic justification code.

Coverage is bidirectional. Every relevant XML field resolves forward to its review location, and
every authored Markdown region resolves back to its typed XML origin. Free-form XPath is not an
accepted locator. Hidden prosecution content, hidden relation semantics, unreviewed provenance,
or an unexplained generated region is a failure.

For PDF derivatives, the review schedule also links each substantive fragment to its registered
page/region evidence. For relation sets it shows endpoint excerpts resolved from current XML,
without storing those excerpts as relation truth.

## 8. Human approval and current resolution

### 8.1 Required approvals

Approval records are append-only, digest-addressed evidence. They never authorize a package unless
all current exact-side bindings match. The applicable identified-human approval types are:

| Approval | Required review |
|---|---|
| `projection-completeness` | The Markdown and coverage expose every review-relevant source/relation field correctly |
| `source-fidelity` | A PDF-derived XML package faithfully represents the exact stored source and registered assets/regions |
| `authored-content-review` | An originally authored XML package states the intended current content |
| `relation-content-review` | An SSP-owned relation set correctly states its typed assertions and exact endpoints |

Projection approval precedes the applicable content/fidelity/relation approval. A model or tool may
prepare comparison evidence but cannot satisfy an identified-human gate.

### 8.2 Exact-side binding

An approval binds at least:

- approval type, reviewer identity/role, subject ID, and review time;
- raw and domain-framed XML digests;
- schema, namespace, secure-parser policy, `xc1`, `ssp-xd1`, and implementation identities;
- exact dependency, endpoint, PDF, asset, and page/region closure as applicable;
- renderer/profile, Markdown, and coverage digests;
- the current projection-approval digest for the later substantive approval; and
- the exact reviewed fragment/relation census.

Approval resolution fails on a missing side, stale digest, unsupported version, incomplete scope,
unknown reviewer authority, ambiguous multiple exact-current records, or record that copies and
thereby purports to own source semantics.

Same-schema records remain append-only across profile or consumer changes. A record that no longer
matches current exact sides is superseded evidence, not an invalid file and not a deletion target.

## 9. Discoverable `US/` and PCT organization

### 9.1 Ownership boundaries

The controlled top-level US boundaries remain:

- `US/common/` for one-owner IDS, filing-control, public-comment, and other strategy-neutral
  records;
- `US/normal-allowance/` for NA claim and response artifacts;
- `US/allowance-first/` for AF claim and response artifacts; and
- `US/prior-art/` for strategy-neutral evidence packages.

Shared content is referenced by stable ID and is never copied into both strategy trees. Strategy
analysis may relate to shared or prior-art fragments through stand-off relation XML.

### 9.2 Canonical bundle rule

Each registered document bundle has exactly one canonical primary:

- `<basename>.source.xml` for a content document; or
- `<basename>.relations.xml` for an analytical map, matrix, or crosswalk whose substance is a
  relation set.

The primary generates `<basename>.md` and `<basename>.coverage.json`. A bundle does not contain both
primary types under the same basename. When narrative and relations are both needed, they receive
distinct document/relation-set IDs and basenames and declare an exact dependency. This prevents a
matrix from acquiring a duplicate content owner merely to obtain a review view.

### 9.3 Exact target taxonomy

The registry closes the following directory families and assigns each current basename to the
stated canonical-primary type:

```text
structured_source/
  schemas/
  profiles/
  registry/
  approvals/
  tools/

US/common/
  ids/                         # AA11393US-US_IDS-reference-list (source)
  public-comments/             # AA11393US-PCT_informal-comments-IB (source)
  filing-controls/             # AA11393US-deferred-filing-disclosure-and-EP-work (source)
  continuation-controls/       # AA11393US-continuation-preservation (source)

US/normal-allowance/
  claims/                      # AA11393US-NA-US_claim-set (source)
  counsel/                     # AA11393US-NA-US_counsel-briefing (source)
  support/                     # AA11393US-NA-priority-support-map (relations)
  prior-art-analysis/          # AA11393US-NA-prior-art-comparison-matrix (relations)
  claim-document-mapping/      # AA11393US-NA-claim-document-mapping-matrix (relations)

US/allowance-first/
  parent/
    claims/                    # AA11393US-AF-US_claim-set (source)
    counsel/                   # AA11393US-AF-US_counsel-briefing (source)
    support/                   # AA11393US-AF-priority-support-map (relations)
    prior-art-analysis/        # AA11393US-AF-prior-art-comparison-matrix (relations)
    claim-document-mapping/    # AA11393US-AF-claim-document-mapping-matrix (relations)
  continuation-candidate/       # unfiled strategy material; not a pending continuation
    claims/                    # AA11393US-AF-CONT-US_claim-set (source)
    support/                   # AA11393US-AF-CONT-priority-support-map (relations)
    prior-art-analysis/        # AA11393US-AF-CONT-prior-art-comparison-matrix (relations)
  cross-strategy/
    claim-crosswalk/           # AA11393US-AF-claim-crosswalk (relations)

US/prior-art/<evidence-id>/
  <evidentiary-basename>.pdf
  <evidentiary-basename>.source.xml
  <evidentiary-basename>.md
  <evidentiary-basename>.coverage.json
  assets/
  convenience/                # optional searchable/OCR derivative
  source-manifest.json
```

Each authored US stem retains its current `_DRAFT` or `_MEMO` document-status suffix immediately
before the primary/view/coverage extension. The established visible Markdown basename is therefore
preserved while its authority and generated status are explicit.

The closed current prior-art ID set is `A1` through `A21`, `B1` through `B10`, `C3`, and `C8`.
Each has one co-located stored-source/source/view/coverage/manifest closure and at most one
registered searchable convenience copy. The evidentiary basenames remain exactly those registered
by the current checksum manifest, and each generated basename is bound explicitly by the content
registry. IDs are never inferred from lexical sorting.

Registered PCT review packages use:

```text
PCT/structured-source/as-filed-dossier/
  AA11393US-PCT_RAPPORTO_DEPOSITO.source.xml
  AA11393US-PCT_RAPPORTO_DEPOSITO.md
  AA11393US-PCT_RAPPORTO_DEPOSITO.coverage.json
  assets/

PCT/structured-source/office-action/
  AA11393US-PCT_office_action.source.xml
  AA11393US-PCT_office_action.md
  AA11393US-PCT_office_action.coverage.json
  assets/

PCT/structured-source/office-action-cited-art/us2021-0352381a1/
  cited_US2021-0352381A1.source.xml
  cited_US2021-0352381A1.md
  cited_US2021-0352381A1.coverage.json
  source-manifest.json
  assets/

PCT/structured-source/office-action-cited-art/cn117278762a/
  cited_CN117278762A.source.xml
  cited_CN117278762A.md
  cited_CN117278762A.coverage.json
  source-manifest.json
  assets/

PCT/structured-source/index/
  AA11393US-PCT-evidence-index.source.xml
  AA11393US-PCT-evidence-index.md
  AA11393US-PCT-evidence-index.coverage.json
```

The as-filed-dossier bundle owns the current disclosure/as-filed content, not merely a filing
receipt. The two cited-art bundles own the current `cited_US2021-0352381A1.md` and
`cited_CN117278762A.md` transcriptions and bind their exact PCT-stored PDF/TXT sources. They remain
distinct from the `US/prior-art/A1` and `US/prior-art/B1` packages; any correspondence is an exact
typed stand-off relation, never an inferred merge. The evidence-index bundle owns the current
authored provenance/publication facts from `PCT/README.md`; the target `PCT/README.md` is its
deterministic router/projection rather than an independently edited fact source.

The byte-distinct stored evidence remains at the exact registered paths
`PCT/AA11393US-PCT_RAPPORTO DEPOSITO.pdf`,
`PCT/PF-MA-AA11393US-PCT office action.pdf`,
`PCT/office action pct/CN117278762A.pdf`,
`PCT/office action pct/US20210352381A1 opposed prior art.pdf`,
`PCT/office action pct/CN117278762A.txt`, and
`PCT/office action pct/US20210352381A1 opposed prior art.txt`. The `.txt` files are registered
convenience derivatives. The two cited-art PDFs
are not merged with `US/prior-art/A1_*` or `US/prior-art/B1_*`; their byte identity, role, and exact
relationship are declared in the current registry.

Exact path templates and the finite basename/ID census are registry-controlled; no placeholder
authorizes ad hoc directories. Existing distinct PDFs or extraction aids are never merged merely
because names or subject matter appear similar.

Generated routers at the relevant directory boundaries list registered current artifacts by
artifact family, strategy/shared scope, status, source role, and stable ID. Routers contain no
hand-maintained duplicate facts.

### 9.4 Reference closure

Before any move is accepted, a repository-wide parser registry classifies every tracked file and
enumerates its reference syntax. Markdown links, XML path fields, control-JSON paths, schema
references, manifests, tests, runbooks, `README.md`, `GLOSSARY.md`, and navigator configuration are
updated atomically. Local paths resolve inside the repository; semantic references resolve by
registry ID and current digest. Unparsed text replacement is not proof of reference closure.

## 10. Source creation and amendment workflow

### 10.1 Registration

1. Allocate the stable document ID and fragment-ID namespace.
2. Select the exact artifact, origin, and projection profiles.
3. Register the proposed path, owner, dependencies, source/assets, outputs, and required approvals.
4. Validate global identity, ownership, and path closure before creating a live output.

### 10.2 PDF-derived source

1. Verify the stored PDF bytes against its registered checksum.
2. Use OCR or extraction only in temporary task-owned storage.
3. Encode ordered typed XML with page/region provenance and explicit uncertainty.
4. Compare all quotations, claim-like passages, tables, figures, and ambiguous OCR against the
   stored PDF; never silently normalize a substantive source error.
5. Securely validate XML and assets, generate Markdown and coverage, and obtain projection then
   source-fidelity approval.
6. Delete temporary extraction data before the package can resolve current.

### 10.3 Originally authored source

1. Author or amend typed XML under the responsible owner.
2. Validate claims, dependencies, defined terms, citations, tables, statuses, actions, and declared
   relation endpoints.
3. Generate Markdown and coverage.
4. Review the human-readable projection and correct XML, never the generated Markdown.
5. Obtain projection then authored-content approval.

### 10.4 Stand-off relation

1. Select exact current endpoint fragments and record their content digests.
2. Encode the assertion under one relation-set owner and closed profile.
3. Validate direction, endpoint types, duplicate ownership, and complete version bindings.
4. Generate the relation review schedule and coverage.
5. Obtain projection then relation-content approval.

### 10.5 Amendment

An amendment writes a new exact source/relation side, regenerates its views, and requires new
current approvals. Earlier same-schema records remain append-only evidence but cease to resolve
current when any bound side changes. There is no in-place editing of generated Markdown and no
compatibility alias for old IDs or paths.

## 11. Approved handoff package

The first migration exports the only upstream contract accepted by the second migration. An export
contains:

- exact approved source XML and declared source-level relation XML;
- exact locked dependency XML, endpoint bindings, PDFs/assets where consumer-visible, and the
  materialized registry view;
- stable document, fragment, relation-set, and relation identities;
- schema/profile/canonicalization/domain versions and both digest classes;
- exact current approval-record digests and coverage identities; and
- generated Markdown as review evidence only.

The export envelope is closed control JSON or XML and contains no copied prosecution text,
quotation, relation assertion, or endpoint excerpt. Downstream consumers must revalidate the exact
package; they cannot accept a claimed boolean such as `approved: true`.

The handoff contract is normative only here. The HTML5 migration imports it by exact current
technical-description and registry digest and must not restate or weaken its schema, identity,
digest, approval, or authority laws. A downstream defect in accepted XML is returned to this
workflow for amendment and reapproval; the consumer does not patch an ephemeral model or generated
view.

## 12. Commands, writes, and failure handling

The implementation provides closed command classes equivalent to:

```text
ssp check-source <document-id>
ssp render-markdown <document-id-or-relation-set-id>
ssp compare-markdown <document-id-or-relation-set-id>
ssp resolve-approvals <document-id-or-relation-set-id>
ssp export <consumer-id>
ssp verify-current
```

Exact names may follow repository conventions, but their registered scopes and postconditions are
mandatory. Each command declares all reads and writes, validates inputs before writes, publishes a
generated set by atomic exchange or a tested journaled rollback, and proves after failure that
command-owned live outputs are byte-identical to the pre-command state.

The documented command surface uses the locked `uv` project environment. Bootstrap is a distinct
preparatory command and is never an implicit side effect of `ssp verify-current` or the repository-
global current-state gate. Production commands reject direct invocation from an unverified Python
environment even when compatible packages happen to be importable there.

Cross-tree reorganization occurs in an isolated worktree. Concurrent external mutation stops
further attributable writes. Writers are plane-confined: a Markdown renderer cannot amend XML or
approvals; an approval resolver cannot write content; an export cannot silently regenerate a stale
view. Temporary paths are unpredictable, task-owned, outside the live tree, and registered for
cleanup.

The structured-source verifier emits namespaced callback evidence for a supplied immutable
snapshot and is non-authoritative for repository or navigator currentness. The repository-global
outer navigator gate alone owns test isolation, post-test complete revalidation, no-write
postconditions, final-snapshot equality, and promotion of structured-source criteria. It invokes
the structured-source verifier again after all discovered tests; a last-sorted passing test that
mutates any controlled source plane therefore causes outer failure.

## 13. Operative structured-source state

The structured-source contract resolves only when the repository contains one coherent state in
which:

- every in-scope document has one registered canonical XML owner and a deterministic current
  Markdown view;
- every in-scope cross-document assertion has one registered stand-off owner;
- all exact-current projection and substantive approvals resolve;
- every path and inbound reference conforms to the target taxonomy;
- no source extraction scratch data, old independently editable Markdown, Markdown-to-XML importer,
  dual authoring path, alias, fallback, unregistered file, or migration artifact remains; and
- the approved consumer-neutral structured export resolves exactly.

XML is the only place where controlled content may be amended. A consumer's independent behavior
and release acceptance are outside this recurring result.

## 14. Draft-only migration archive and intermediate gate

> This section governs implementation only. It is removed from the operative technical
> description before the first migration is accepted. Git retains the implementation history.

### 14.1 Baseline archive

Before changing an in-scope document, the cutover tool resolves the exact baseline Git tree and
creates one owner-only, read-only temporary archive outside the repository and every Git worktree.
The unpredictable archive path is atomically registered before creation under a repository-scoped
exclusive OS-held lease containing task, process, start-time, and owner identity. A live lease
blocks a second invocation; only a proven-stale lease may be recovered.

The archive contains the exact baseline bytes and repository-relative paths of every affected:

- Markdown document;
- stored or searchable PDF, OCR/extraction aid, figure, and asset;
- source checksum or item manifest;
- source-level relation source; and
- router or reference-bearing document whose content/path changes in this migration.

A closed manifest records path, Git blob ID, mode, size, raw digest, role, and exactly one
`preserve`, `move`, `merge`, or `retire` disposition. A total old-to-new mapping accounts for every
archived item. Split and merge cases enumerate every input and output explicitly. Similar names or
content never authorize deletion.

This archive is limited to the Markdown/source migration. It does not archive navigator code,
candidate/release state, UI wording, or navigator-owned relation JSON for future conversion. The
second migration captures its own baseline from the accepted intermediate repository state.

### 14.2 Automated equivalence

After XML and new Markdown exist in the isolated migration worktree, the intermediate gate proves:

1. **Inventory closure:** every archived item and disposition maps exactly once to the proposed
   state, with no missing, additional, or multiply owned content.
2. **Markdown semantic closure:** one pinned Markdown AST profile compares headings, paragraphs,
   claims, dependencies, limitations, quotations, citations, tables, lists, labels, statuses,
   actions, links/images, figures, ordering, and visible provenance. Only explicitly identified
   fixed generated notices may be masked.
3. **Source fidelity:** PDF-derived discrepancies are resolved against the stored PDF, not by
   treating old Markdown as authority. A discovered old transcription error is corrected in XML
   and explicitly dispositioned.
4. **Relation closure:** every source-level assertion carried by the old documents maps to exactly
   one new relation or typed source field; endpoints and every substantive relation value compare
   under a closed migration profile.
5. **Reference closure:** all old-to-new paths, semantic IDs, local links, images, manifests,
   checksums, and registered consumers resolve in the isolated proposed tree.
6. **Mutation effectiveness:** deletion, addition, owner change, endpoint drift, hidden XML field,
   or changed Markdown semantic makes the gate fail.

### 14.3 Human visual equivalence

Old and new Markdown are rendered with identical pinned Pandoc/browser, stylesheet, fonts, locale,
viewport, zoom, and print settings. Side-by-side views and diff overlays are produced for every
document. An identified human reviews every nonzero region and records a disposition for text
visibility, claims, quotations, table structure, links, figures, wrapping, clipping, ordering, and
pagination where applicable.

The required outcome is semantic and review equivalence, not blind reproduction of an old defect.
When a difference exposes a prior error, the reviewer verifies the applicable stored PDF or
authored intent, approves the corrected XML through the recurring workflow, and records why the
baseline differs.

The temporary migration-equivalence record binds the baseline tree, archive manifest, total path
mapping, old/new Markdown and render digests, XML and asset digests, AST/coverage/relation reports,
visual regions, reviewer identity, and all dispositions. It is migration evidence only and cannot
replace a recurring projection, fidelity, content, or relation approval.

### 14.4 One-way cutover and cleanup

1. Capture and verify the baseline archive before the first controlled change.
2. Close schemas, profiles, IDs, registry entries, origin classifications, and target paths.
3. Provision the migration and recurring implementation through the exact committed `uv` project
   and lock; keep migration-only dependencies in a separate locked group that is removed from the
   operative project and lock at cutover.
4. Convert current authored Markdown and PDF-derived transcriptions into canonical XML; preserve
   stored-source PDF bytes exactly.
5. Materialize source-level stand-off relations and deterministic review schedules.
6. Generate all Markdown and coverage from XML in the isolated worktree.
7. Pass automated equivalence and identified-human visual review; correct XML and regenerate until
   every difference is resolved.
8. Materialize the full `US/`/PCT target tree and update all registered inbound references.
9. Obtain recurring exact-current projection and substantive approvals.
10. As a one-time outer integration observation, prove the unchanged navigator passes from the
   generated Markdown. This observation is not part of recurring SSM acceptance and creates no
   upstream dependency on a navigator result.
11. Invoke the idempotent cleanup handler on normal exit, handled failure, abort, and catchable
    termination. It deletes only the exact registered task-owned archive, manifests, mappings,
    renders, diffs, screenshots, temporary record, import code/data, and migration-only controls.
12. After an uncatchable failure, a later invocation may clean only a proven-stale leased target.
    The locator and lease are removed only after every registered target is proven absent.
13. Remove all migration-only callbacks/configuration and dependencies and regenerate the exact
    operative `uv.lock`. Rewrite this draft pair into present-tense,
    consumer-neutral operative documents named
    `AA11393US-structured-source-markdown_technical-description.md` and
    `AA11393US-structured-source-markdown_acceptance-criteria.md`: remove the migration section,
    first/second-stage and future-cutover narrative, `_DRAFT` status, temporary-consumer language,
    all `SSM-MIG-01` text (including later traceability references), and obsolete numbering; update
    every inbound link and regenerate the acceptance-table region.
14. Run the recurring structured-source callbacks and the independent current navigator gate on
    the exact integrated snapshot. Only the repository-global outer gate owns final promotion and
    snapshot certification.

Cleanup is idempotent for absent, partial, and complete targets. Any inability to prove archive,
locator, lease, importer, or report absence prohibits acceptance. No temporary equivalence record
is committed, released, or used as a consumer authorization.

## 15. Acceptance traceability

The coupled acceptance document uses `SSM-AC-01` through `SSM-AC-10` for recurring controls and
`SSM-MIG-01` for the draft-only implementation gate. One closed executable registry is the sole
operative definition of the recurring criterion text and namespaced callback ownership; the
acceptance table is its deterministic human-readable projection. One repository-global
outer-postcondition map, owned by the navigator current-state gate, alone owns test isolation,
post-test revalidation, no-write, and final-snapshot controls.

Every structured-source callback has exactly one criterion owner, and reverse scanning identifies
unmapped production controls. The fresh runner emits only an ephemeral namespaced evidence receipt
bound to the immutable snapshot and complete callback census. The global outer verifier promotes
criteria to passed only after its separately owned post-test revalidation and final snapshot
equality. The receipt is never written to the repository and cannot replace human approval.

`SSM-MIG-01` is intentionally outside the recurring registry and result census. It must pass during
implementation, then its archive, evidence, code, and prose are removed. The accepted recurring
state proves their absence rather than purporting to preserve a maintenance history.

## 16. Standing decisions

| Topic | Decision |
|---|---|
| Canonical content | Closed `.source.xml`; PDF-derived XML is a structured derivative, authored XML is the primary authored source |
| Cross-references | Digest-bound `.relations.xml` using stable document/fragment identities |
| Markdown | Deterministic human review projection; never independently edited |
| Human supervision | Projection plus origin-appropriate exact-side approval before consumer eligibility |
| JSON | Closed controls only; no content or relation meaning |
| Stored PDF | Exact evidentiary bytes preserved; OCR/searchable copies remain convenience derivatives |
| Shared content | One owner under `US/common/`, referenced by ID rather than duplicated |
| Prior art | One discoverable evidence package per registered evidence ID |
| Structured-source result | Consumer-neutral approved XML export plus generated human-review Markdown |
| Compatibility | No dual authoring, fallback source, alias, or persistent importer |
| Python environment | Host-provided exact-version `uv`; repository-owned project/lock and pinned interpreter contract; project-local environment; no pip, ambient-package, or implicit-sync fallback |
| History | Git only; temporary migration evidence is deleted before acceptance |
