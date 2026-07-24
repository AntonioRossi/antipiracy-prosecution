# AA11393US — Structured-Source HTML5 Migration: Technical Description (DRAFT)

> **PROPOSED ARCHITECTURE · INTERNAL DRAFT · STATUS 24 JULY 2026**
>
> This document specifies the second of two one-way migrations. It changes the navigator from a
> Markdown/content-JSON data path to direct consumption of an exact approved structured-source
> export and approved navigator-owned XML, then regenerates the current HTML5/release state.
>
> Its coupled acceptance contract is
> [`AA11393US-structured-source-html5-migration_acceptance-criteria_DRAFT.md`](AA11393US-structured-source-html5-migration_acceptance-criteria_DRAFT.md).
> Its mandatory upstream contract is
> [`AA11393US-structured-source-markdown-migration_technical-description_DRAFT.md`](AA11393US-structured-source-markdown-migration_technical-description_DRAFT.md),
> with acceptance defined by
> [`AA11393US-structured-source-markdown-migration_acceptance-criteria_DRAFT.md`](AA11393US-structured-source-markdown-migration_acceptance-criteria_DRAFT.md).
> The existing
> [`AA11393US-claims-navigator_technical-description_DRAFT.md`](AA11393US-claims-navigator_technical-description_DRAFT.md)
> remains the product/UI behavior authority until its data-input provisions are updated in the
> implementation. This migration document does not restate or weaken navigator `AC-01` through
> `AC-20`.

## 1. Rationales

1. **Consume the reviewed semantic representation.** Once XML, its Markdown projection, and human
   approvals are exact-current, reparsing Markdown for production discards typed identity and
   recreates ambiguity already resolved upstream.
2. **Make the final build mechanical.** A renderer that receives validated content fragments,
   exact relation endpoints, typed wording entries, and closed controls has substantially less
   interpretive work than one that reconstructs semantics from presentation text.
3. **Prevent cross-document drift.** HTML5 claim-to-source, claim-to-prior-art, support, and
   strategy navigation should resolve stable digest-bound fragment tuples rather than copied text,
   file-relative assumptions, or offsets.
4. **Separate upstream correction from downstream presentation.** A source defect returns to the
   structured-source workflow for amendment and human reapproval. The navigator cannot patch an
   ephemeral model or generated HTML to compensate.
5. **Give navigator-owned semantics one explicit owner.** Navigator relation instances and
   human-visible interface wording are not source-document truth. They require their own XML,
   ownership, review, and exact consumer contract.
6. **Prove no semantic field is lost during encoding changes.** A schema-derived input census and
   source/template literal census are necessary because a visually plausible build can omit
   dormant fields, release labels, relation cautions, accessibility wording, or profile-specific
   behavior.
7. **Compare behavior, not just bytes across architectures.** Old and new implementations may
   serialize equivalent HTML differently. Migration equivalence therefore compares normalized
   semantic DOM, visible text, relations, accessibility, interaction, print, and pinned visual
   output; the final new implementation must then reproduce its own artifacts byte-for-byte.
8. **Certify only the post-test state.** Tests can mutate files. Release success requires complete
   upstream, navigator-input, candidate, QA, bundle, and artifact revalidation after every
   discovered test and before final snapshot equality.
9. **Remove the migration bridge.** The accepted implementation has no Markdown consumer,
   semantic JSON, dual reader, fallback, alias, old runner, comparison archive, or transition
   narrative. Git is the sole implementation history.

## 2. Implementation goals

The implementation shall:

1. require a fresh exact-current result and export from the first migration on the same immutable
   repository snapshot;
2. import the upstream XML/digest/identity/approval contract by exact version without redefining
   or weakening it;
3. execute every downstream command through the exact host-provided `uv` and repository-owned
   project/lock/interpreter environment accepted upstream, without an alternate lock, implicit
   synchronization, package-manager cache dependency, or ambient-Python fallback;
4. migrate navigator-owned cross-document relation instances to closed `.relations.xml` packages
   using the upstream endpoint tuple and canonical relation envelope;
5. migrate every human-visible navigator string and interpolation contract to closed wording XML;
6. census every production input field and every production source/template/configuration string
   literal, mapping each exactly once to its final owner or a narrowly proven non-semantic class;
7. read approved XML only through secure, allowlisted gateways into an ephemeral typed model;
8. prevent production reads of review Markdown, OCR/searchable content, semantic content/relation/
   wording JSON, temporary imports, or arbitrary runtime wording;
9. preserve exact source text, fragment identity, relation meaning, profile selection, release
   policy, and consumer-visible wording under closed comparison profiles;
10. render deterministic HTML5, no-JavaScript and print surfaces, interaction state, accessibility
   semantics, and manifests from the typed model and declared controls;
11. preserve every independently mandatory navigator acceptance control and identified-human
    relation, visual, accessibility, and QA review;
12. regenerate candidates, attestations, QA evidence, sealed artifacts, checksums, release records,
    bundle configuration, bundles, and current bundle records only after the new data path is final;
13. compare the old accepted navigator state with the new implementation under an isolated,
    temporary migration gate and identified-human disposition;
14. delete every old reader, adapter, semantic JSON source, archive, comparison record, and
    migration control before recurring acceptance; and
15. let only the outer current-state gate compose same-snapshot upstream, migration, navigator,
    release, QA, bundle, and final-state evidence into repository `current` status.

## 3. Normative boundaries

### 3.1 Exact upstream prerequisite

The second migration begins only after the first migration has an accepted intermediate state. Its
build must recompute, not merely trust, the current upstream result and validate the exact approved
export on the same immutable snapshot. The dependency is one-way:

```text
accepted structured-source export
                │ read-only
                ▼
 navigator secure ingestion + navigator-owned XML
                ▼
       ephemeral typed render model
                ▼
    candidate HTML5 and current artifacts
```

The upstream export never binds a navigator receipt or artifact. The navigator binds the upstream
result and export digest, so no approval/result cycle exists. Missing, stale, warning, skipped,
unknown, or snapshot-mismatched upstream evidence fails before model construction.

The imported upstream result includes the exact repository project metadata, `uv.lock`, Python
pin, required host `uv` version, installed-distribution census, implementation-source inventory,
and locked/offline/no-sync verification contract. A downstream command cannot substitute a second
project, lock, environment, interpreter, package source, or tool version. Any authorized dependency
change amends the upstream-owned root project/lock and requires a fresh upstream result before the
downstream runner may start.

The navigator has read-only access to upstream source/dependency/source-level-relation XML and
declared assets through the export. It cannot:

- read upstream Markdown as semantic input;
- write or normalize upstream XML, coverage, approvals, or assets;
- select an unapproved alternative package;
- substitute a PDF/OCR/searchable copy for structured content; or
- repair, retarget, or silently tolerate an invalid endpoint.

If downstream work exposes a source defect, processing stops. The source is amended and reapproved
through the first workflow, then the upstream and downstream results are recomputed.

### 3.2 Product-behavior boundary

The claims-navigator technical description and navigator `AC-01` through `AC-20` continue to own
edition behavior, information architecture, user interaction, accessibility, no-JavaScript and
print behavior, security, candidate/release rules, QA policy, and bundle composition. This document
owns only the structured-input migration, the new navigator-owned XML inputs, proof of semantic/
visual equivalence, removal of old input paths, and integration into the final gate.

At cutover, contradictory Markdown, relation-JSON, wording-JSON, or other input clauses in the
claims-navigator technical description, schemas, runbooks, and configuration are replaced with the
exact accepted interface here. The operative repository cannot retain two live HTML5 input
contracts.

### 3.3 Plane ownership

| Plane | Sole semantic owner after cutover |
|---|---|
| Corpus prose, claims, source quotations, provenance | Upstream `.source.xml` |
| Source-level support/art assertions | Upstream SSP-owned `.relations.xml` |
| Navigator-only edition mappings and navigation assertions | Navigator-owned `.relations.xml` |
| UI, screen, print, no-JS, accessibility, edition/group/editorial, artifact, release, and bundle wording | Navigator wording XML |
| Paths, IDs, digests, profiles, allowlists, limits, release switches | Closed control schemas |
| Render model | Ephemeral memory only; never a persisted semantic source |
| Markdown | Human review evidence only; forbidden production input |
| HTML5 and release products | Deterministic downstream artifacts; never upstream authority |

### 3.4 Imported execution environment

The first migration remains the sole owner of the repository-root `uv` project and toolchain
contract. This migration consumes that exact accepted side read-only. The host supplies the exact
`uv` version required by the root project; the downstream implementation supplies no binary,
bootstrap fallback, nested project, second lockfile, or independently managed virtual environment.

After the explicit upstream bootstrap, every downstream command runs through the already
provisioned environment, equivalent to
`uv --no-cache --offline run --locked --no-sync python -m navigator <command>`. The invocation
checks project/lock currency but cannot synchronize, resolve, download, install, use a persistent
host cache, or write the environment. Import-origin and distribution-census checks reject ambient
site packages or an executable imported outside the exact project environment. The downstream
receipt binds the upstream toolchain result rather than copying its dependency list or claiming
separate authority over it.

## 4. Navigator-owned XML inputs

### 4.1 Relation packages

Navigator-owned relation instances are stored under `navigator/relations/` as registered
`.relations.xml` packages. They import the generic relation envelope, stable identities, endpoint
tuple, secure-parser contract, canonicalization, digest-domain law, and base schema from the exact
accepted upstream interface. This document does not duplicate those rules.

The exact navigator relation bundles are:

```text
navigator/relations/na__pct.relations.xml
navigator/relations/na__pct.md
navigator/relations/na__pct.coverage.json

navigator/relations/af__pct.relations.xml
navigator/relations/af__pct.md
navigator/relations/af__pct.coverage.json
```

`na__pct` and `af__pct` own only navigator edition-to-PCT mapping/navigation assertions. The
source-level claim-to-support, claim-to-prior-art, priority-support, comparison-matrix,
claim-document-mapping, and crosswalk relation sets enumerated by the upstream registry remain
SSP-owned. A navigator relation may reference an SSP assertion by its exact relation identity but
cannot restate it. Every current relation-set ID appears in exactly one of the two registries, and a
cross-registry duplicate-assertion scan is mandatory.

Navigator profiles define only navigator-specific meaning and constraints. Their current instance
scope includes the registered edition mappings, including the NA-to-PCT and AF-to-PCT relation
sets. Each profile closes:

- allowed endpoint document/profile types and direction;
- relation type, posture, gate, caution, disposition, and responsible semantic owner fields;
- required endpoint cardinality and current digest bindings;
- allowed consumer views and interaction states; and
- a deterministic human review schedule that resolves endpoint excerpts from current upstream XML.

A navigator relation package may not duplicate or override an SSP-owned assertion. If both planes
appear to state the same assertion, the ownership validator requires one declared owner and either
a typed reference to that assertion or removal of the duplicate.

Every current navigator relation instance requires upstream-compatible projection approval and an
independent navigator semantic-review record binding the complete relation census, every semantic
field, endpoints, anchors, owner, profile, XML digest, and exact upstream export. A source approval
or migration-equivalence record cannot substitute for this review.

The shared structured-source projection library generates the navigator-owned `.md` and
`.coverage.json` companions deterministically from relation XML and exact endpoint XML. Navigator
owns these instances, output paths, coverage, and approval records; importing the renderer does not
transfer their semantic ownership upstream.

### 4.2 Wording XML

All human-visible navigator wording is stored under `navigator/wording/` in the closed namespace
`urn:aa11393:navigator:wording:1`. The exact bundles are:

```text
navigator/wording/shared.wording.xml
navigator/wording/shared.md
navigator/wording/shared.coverage.json

navigator/wording/na.wording.xml
navigator/wording/na.md
navigator/wording/na.coverage.json

navigator/wording/af.wording.xml
navigator/wording/af.md
navigator/wording/af.coverage.json
```

One wording entry has a stable `wordingId`, locale, ownership scope, usage-context allowlist, and
an ordered mixed sequence of typed `text` and `slot` nodes. Shared wording appears only in
`shared.wording.xml`; NA- or AF-specific wording appears only in its edition bundle.

Each whole file also has one stable `wordingBundleId`: `nav-wording-shared`, `nav-wording-na`, or
`nav-wording-af`. The shared `ssp-xd1` domain registry assigns the unique artifact kind
`navigator-wording-bundle-v1`, the `wordingBundleId` subject-ID field, this wording namespace/schema
version, and the whole securely parsed `xc1` bundle as its payload grammar. The resulting
`sha256/xc1/ssp-xd1` digest is therefore an unambiguous authorizing side. This shared identity law
does not transfer wording ownership to the upstream content registry.

A slot declares:

- stable `xml:id` and argument name;
- value type;
- formatter ID;
- output-context escape class;
- cardinality and occurrence order; and
- one exact value-origin profile.

Allowed origin kinds are closed:

- `source-field` — an exact field from the approved upstream typed model;
- `relation-field` — an exact field from approved navigator or upstream relation XML;
- `registry-control` — an exact schema-classified control field;
- `derived-control` — a closed named derivation over declared control inputs; and
- `view-state` — an exact field in the closed navigator interaction-state schema.

The gateway supplies a value only from the declared origin, validates its type, applies the one
registered formatter, then applies context-specific escaping. Arbitrary runtime strings, alternate
origins, executable templates, brace/percent interpolation languages, raw HTML slots, or a generic
“safe” bypass are prohibited.

Static consumer wording outside wording XML is limited to proven non-consumer identifiers and
diagnostics that cannot reach an artifact. The production census in §5 proves this limitation.
Every rendered authored string reverse-maps to source XML, relation XML, or a wording ID and exact
slot-origin binding.

### 4.3 Approval and registry ownership

Navigator relation and wording registries locate exact packages, profiles, current approvals,
consumer contexts, and outputs. They do not copy semantic entries into JSON. Approval records are
append-only exact-side evidence under closed schemas. Same-schema records that cease to match
current exact sides remain valid superseded evidence and do not block current resolution merely
because a different technical profile no longer references them.

This specification owns the new XML-input approval types. A navigator relation has
`navigator-relation-projection-completeness` followed by
`navigator-relation-semantic-review`. A wording bundle has
`navigator-wording-projection-completeness` followed by `navigator-wording-content-review`. The
first record in each sequence binds raw/domain XML digests, imported schema/parser/canon/domain and
renderer identities, exact upstream export where applicable, generated Markdown/coverage digests,
and complete schema-field-to-anchor coverage. The second binds the first record plus every relation
semantic field/endpoint or every wording entry/static-text/slot/value-origin/usage-context field.
Both bind reviewer identity and authority. The navigator registry and claims-navigator technical
description point to this sole approval contract at activation.

A profile switch selects required current records through exact references; it does not authorize
deleting unreferenced same-schema records. Model/tool output, a source approval, or a temporary
migration-equivalence review cannot satisfy either identified-human record.

## 5. Current production-input ownership

### 5.1 Schema-derived census

A closed registry enumerates every current production input and consumer, including:

- corpus and edition configuration;
- dependency, gate, segmentation, relation, wording, support, release, QA, and bundle controls;
- candidate, attestation, release, and bundle schemas;
- production Python/JavaScript or other source files;
- the imported root project/lock/interpreter/tool identities and the downstream implementation-
  source/import census;
- templates, stylesheets, schema defaults, and configuration; and
- all data paths capable of reaching HTML5, no-JS, print, accessibility, manifest, artifact,
  release, QA, or bundle output.

For each registered JSON input, the controlling schema derives a complete leaf-path/type/usage
census. For XML, the schema derives the complete semantic field census. Registered language-aware
parsers derive a complete string-literal and usage census for production source, templates, schema
defaults, and configuration. Text search alone is supporting evidence, not the authoritative
census.

Each current input leaf and production literal has exactly one current owner/use classification:

- `upstream-export` with an exact source/dependency/SSP-relation XML field identity;
- `navigator-relation-xml` with an exact relation-set/relation/field identity;
- `navigator-wording-xml` with an exact wording/slot identity;
- `retained-control` with a closed control-schema field and consumer allowlist;
- `non-consumer-code` with a usage proof that it cannot reach an output; or
- `mechanically-derived` with a closed derivation ID and exact inputs.

The registry identifies the exact current path/field or literal ID, owner, consumers, and
derivation where applicable. Missing, additional, multiply owned, unclassified, wrongly
classified, or changed-use fields fail. No migration, history, review-transport, or retired-field
classification exists in the recurring registry.

### 5.2 Wording and relation completeness

Current-state validators prove, entry by entry:

- navigator relation census, IDs, endpoints, direction, type, posture, owner, gates, cautions,
  dispositions, and every profile field;
- wording IDs, ownership, locale, exact static text, usage contexts, and consumer bindings;
- slot names, occurrences, order, cardinality, value types, formatter IDs, escape classes, and
  exact value-origin profiles; and
- edition/group display names, segmentation/editorial labels, accessible names/descriptions,
  artifact labels, release strings, and bundle-manifest wording.

Mutation of every relation, wording, slot, origin, control, or current ownership field must make
the relevant validator fail. A rendered authored string or relation that does not reverse-map to
one current XML owner is prohibited.

## 6. Secure direct-consumer architecture

### 6.1 Read gateway

All semantic reads pass through one registered gateway that:

1. recomputes the same-snapshot upstream result and validates the exact export envelope;
2. secure-parses the exact approved upstream and navigator XML with the imported parser policy;
3. validates schemas, semantic invariants, domain-separated digests, dependencies, endpoints,
   assets, wording slots/origins, and exact approvals;
4. records a typed allowlisted read log;
5. constructs an immutable ephemeral model; and
6. seals the model before any renderer or candidate writer runs.

The gateway rejects undeclared files, unexpected symlinks, path escapes, external resources,
unsupported versions, stale approvals, endpoint drift, duplicate owners, arbitrary slot values,
and any persisted XML-to-JSON content adapter.

### 6.2 Ephemeral model invariants

The model preserves exact source text and stable identities; typed view models may select and
order declared fields but cannot normalize substantive text, infer a missing relation, retarget an
endpoint, repair an invalid claim dependency, or invent wording. Mechanical derived fields name
their derivation and inputs. Every model field has a typed origin and every consumer read is
allowlisted by the controlling registry.

No semantic model is serialized as a production source. Diagnostic dumps, when explicitly enabled
for tests, are temporary, non-authoritative, outside the live tree, and removed before command
success.

### 6.3 Forbidden readers and writes

Production code cannot read:

- upstream or generated relation Markdown;
- corpus prose, relation meaning, or wording from JSON;
- canonical or searchable PDFs/OCR as rendered text;
- old-path aliases, caches, conversion scratch data, or migration archives; or
- fallback/default prose in schemas, templates, source code, or configuration.

The downstream command plane cannot write upstream XML, relations, assets, coverage, Markdown, or
approval records. The runtime read/write log, production-source inventory, import graph, and
language-aware static scan enforce both rules.

## 7. Mechanical HTML5 generation

### 7.1 Locked render inputs

A candidate build binds:

- exact upstream result and export digest;
- exact accepted root project, lock, Python, host `uv`, installed-distribution, and import-origin
  identities;
- exact navigator relation and wording XML digests and approvals;
- schemas, registries, control profiles, code, templates, stylesheets, scripts, assets, fonts,
  locale, and renderer/toolchain identities;
- exact edition/profile selection and interaction-state schema; and
- complete source/relation/wording/output inventories.

The renderer receives only the sealed typed model and declared presentation resources. It cannot
perform network reads, parse Markdown, discover unregistered inputs, evaluate arbitrary template
code, or substitute stale cached content.

### 7.2 Output semantics

For each registered edition and surface, generation preserves the product contract's:

- exact visible source text and document/fragment provenance;
- claim order, numbering, dependency, limitation grouping, and status;
- relation direction, posture, gates, cautions, disposition, and endpoint navigation;
- heading hierarchy, landmarks, lists, tables, links, figures, captions, and identifiers;
- accessible names, descriptions, relationships, focus order, and live-state behavior;
- no-JavaScript readability and functional navigation;
- print content, ordering, page-break rules, and visible provenance; and
- release labels, artifact identities, manifests, and bundle wording.

Every authored visible string and semantic relation in an output reverse-maps to its exact XML
origin. The renderer may add only closed mechanical markup and values defined by registered
derivations.

### 7.3 Escaping and security

Escaping is output-context-specific for HTML text, attribute, URL, embedded structured data, and
any other allowed context. A value cannot change contexts without a distinct registered escape
class. URLs and local paths are scheme/path allowlisted before serialization. No wording or source
field can inject raw markup, script, event handler, unsafe URL, stylesheet escape, or executable
template construct.

The implementation preserves all existing navigator security and content-security acceptance.
This document adds no exception for “trusted XML”; XML trust establishes provenance, not output
context safety.

### 7.4 Determinism

Fresh processes with the same locked inputs produce byte-identical candidate directories,
inventories, HTML5 files, manifests, and sealed artifacts. Ordering, serialization, line endings,
timestamps, random values, paths, locale, and toolchain metadata are fixed or excluded by a closed
mechanical rule. Candidate comparison is exact bytes and exact inventory, not semantic similarity.

## 8. Navigator acceptance, QA, and release

Navigator `AC-01` through `AC-20` remain independently mandatory and are the sole authority for
product behavior, QA profile semantics, candidate/attestation/release progression, pin plans,
version labels, sealed artifacts, and bundle composition. The second-migration runner accepts only
a complete same-snapshot navigator result from that executable registry; it cannot copy the
criterion list, infer pass from generated files, omit supplemental callback owners, or reduce the
mandatory evidence map.

The migration changes only the exact input sides bound by those controls. At activation, the
claims-navigator technical description, acceptance registry, schemas, and record resolvers are
updated so every relevant candidate, attestation, QA, artifact, release, bundle, and record binds
the approved upstream export plus current navigator relation/wording XML and approvals. Any QA
profile, append-only-record, multi-file pin-plan, or current-version-label rule needed for a
releasable state is defined and tested there, not duplicated here.

After code/configuration cleanup and fresh navigator XML review/approval, the navigator's own
current release procedure performs all downstream regeneration as the last declared writes. No
test, cleanup handler, updater, or callback may mutate a previously verified input, record,
candidate, release, QA, bundle, or artifact after its final check.

## 9. Commands, transactions, and final-state gate

The implementation provides registered command classes equivalent to:

```text
navigator validate-inputs
navigator build-candidate <edition>
navigator compare-candidate <edition>
navigator verify-release <edition>
navigator build-bundle
navigator verify-current
```

Exact repository command names may differ. Each command has a closed read/write scope, validates
before writes, uses atomic exchange or tested journaled rollback for output sets, refuses live
external mutation, and proves on failure that its owned live outputs are unchanged. Unsupported
schema, source, relation, wording, record, profile, or artifact versions fail before writes; no
backward-compatibility branch is added.

The command registry exposes only entry points executed through the imported upstream `uv`
environment. Bootstrap remains a separate upstream-owned preparatory operation. Verification uses
the no-cache/offline/locked/no-sync invocation in §3.4 and fails before semantic reads when the
host tool, project, lock, interpreter, installed distributions, or import origins are not exact.

### 9.1 Materialized test snapshot

Discovered tests execute only against a materialized immutable snapshot or isolated worktree whose
writes cannot alter the live candidate under certification. The runner still compares the live
snapshot before and after test execution. A test is not trusted because it passed or because its
name appears in a callback map.

### 9.2 Complete post-test revalidation

After all discovered tests and subprocesses finish, the outer gate recomputes, in order, against
the unchanged live snapshot:

1. structured-source registry/filesystem, XML, endpoint, asset, projection, coverage, approval,
   export, toolchain, and exact upstream result closure;
2. navigator relation/wording registry, XML, endpoint, approval, slot/value-origin, consumer-read,
   and production-source/string-provenance closure;
3. candidate bytes and inventory for every registered edition;
4. attestation, profile-derived QA, sealed artifact, checksum, release-record, bundle-config,
   bundle, and current-bundle-record exact-side closure;
5. complete navigator `AC-01` through `AC-20` evidence, including mandatory supplemental callback
   ownership; and
6. acceptance result census, no-write postconditions, controlled-tree digest, and final snapshot
   equality.

A last-sorted passing test that overwrites any already checked input, record, or artifact therefore
causes failure. Child receipts cannot certify outer postconditions early. Only after every item
above passes may the outer
`uv --no-cache --offline run --locked --no-sync python -m navigator validate-current` result report
`status: current`.

## 10. Accepted final state

The second migration is complete only when:

- the exact upstream structured-source result/export and all navigator-owned XML resolve current;
- the exact upstream-owned root project/lock and host `uv`/Python environment resolve current and
  every downstream import resolves inside that environment;
- production code consumes approved XML through the secure gateway and an ephemeral model;
- all registered editions, surfaces, relations, wording, candidates, approvals, QA evidence,
  releases, artifacts, bundles, and records are exact-current;
- every navigator product acceptance criterion passes independently on the same snapshot;
- no Markdown/content-JSON/relation-JSON/wording-JSON semantic reader or store remains;
- no dual reader, adapter, fallback, alias, silent normalization/repair path, old release input,
  migration-only field, archive, baseline runner, comparator, temporary record, lease, locator,
  render, diff, or implementation narrative remains; and
- the complete post-test revalidation certifies an unchanged final snapshot.

The claims-navigator technical description, runbook, schemas, `AGENTS.md`, tests, configuration,
and commands state only this active data path. Git alone records the replaced implementation.

## 11. Draft-only HTML5 migration gate

> This section governs implementation only. It is removed before recurring second-migration and
> navigator acceptance. Git retains the implementation history.

### 11.1 Independent navigator baseline

After the first migration passes, the HTML5 cutover resolves that exact intermediate Git tree and
creates a separate owner-only temporary baseline outside the repository and every worktree. It
does not reuse the first migration's deleted archive. The path is atomically registered before
creation under a repository-scoped exclusive OS-held lease with task, process, start-time, and
owner identity. A live lease blocks another invocation; only a proven-stale lease may be recovered.

The closed baseline manifest binds:

- every current navigator input/configuration, relation JSON, wording JSON, source/template/schema
  default, stylesheet, script, asset, and production consumer;
- every candidate, HTML5 file, output inventory, manifest, sealed artifact, checksum, release/QA/
  bundle input and record used for the reference state;
- schemas, canonical materialized old models, registered renderers/toolchains, fonts, locale,
  viewports, interaction fixtures, and print settings;
- a schema-derived JSON/XML leaf census and language-aware source/template string-literal/usage
  census; and
- exact baseline-tree path, blob, mode, size, raw digest, role, and disposition for each affected
  file.

The old navigator runs only in an isolated baseline process and may read the baseline's generated
Markdown. The migration comparator's new runner uses the exact accepted upstream export plus
securely validated, digest-locked provisional navigator XML in an isolated non-authorizing mode.
It may write only temporary comparison outputs, cannot enter candidate/release paths, and cannot
issue or consume a recurring approval. Their read/write logs prove separation. After cleanup, the
production runner accepts only fresh approved navigator XML under §§4 and 6.

Old/new comparison dependencies use a separately declared migration-only group in the upstream-
owned `uv.lock`. That group cannot enter a recurring candidate, approval, receipt, or release side.
Before activation it and every migration-only distribution are removed, the operative lock is
regenerated, and upstream acceptance plus the downstream installed-distribution/import census are
re-proved through the no-cache/offline/locked/no-sync environment.

### 11.2 Input and semantic equivalence

The migration-only transfer registry maps every old field and literal exactly once to
`source-xml`, `relation-xml`, `wording-xml`, `retained-control`, `non-consumer-code`,
`mechanically-derived`, or `retired-transition-only`. Each entry binds the exact old schema/AST
field or literal ID/path, final target ID or derivation, value, consumer uses, and comparison rule.
This temporary registry is distinct from the current production-ownership registry in §5.

`retired-transition-only` is permitted only when schema and code-use analysis classifies the exact
field as migration/history/review transport, proves it cannot affect current content, relation,
wording, provenance, policy, release, QA, bundle, or other output/authorization, and an identified
human dispositions it. Names such as `migrationState`, `previousTargets`, or `review` are not proof.
Every retired field and reader/writer must be absent at cleanup; no operative semantic may retire.

The gate compares:

1. complete production input and consumer inventory;
2. every corpus semantic value to exact upstream XML identity/text;
3. every navigator relation field and endpoint to navigator relation XML;
4. every consumer wording field/literal and placeholder contract to wording XML and typed slots;
5. retained controls and closed derived values; and
6. every identified-human `retired-transition-only` disposition and final non-use proof.

Mutation at every source, relation, wording, slot, control, and retirement field must fail the
comparison. An uncensused, multiply mapped, or visually hidden semantic value is a failure.

### 11.3 HTML5 behavioral and visual equivalence

For every edition, route, interaction state, no-JavaScript state, viewport, and print profile, the
gate compares old and new outputs using:

- exact visible-text and source-fragment inventories;
- exact relation/endpoint and navigation-target inventories;
- normalized semantic DOM, landmark/heading/list/table/link/form structure, IDs, and provenance;
- accessibility tree, accessible names/descriptions/relationships, focus order, and keyboard
  behavior;
- route/link/image/asset closure and interaction-state transitions;
- security-relevant URL, escaping, and executable-content observations;
- print content/order/page-break observations; and
- pinned screenshots, side-by-side renders, and pixel-diff regions.

Closed masks may exclude only declared mechanical differences that cannot conceal text, relation,
accessibility, security, or behavior changes. Similarity thresholds cannot excuse a semantic
difference.

An identified human reviews every nonzero semantic, behavioral, accessibility, print, or visual
difference and records an explicit disposition. A difference that exposes an upstream source
defect stops the migration and returns to upstream amendment/reapproval. A product-behavior change
requires a separate current technical-description and acceptance change; it is not smuggled through
the data migration.

The temporary equivalence record binds the baseline tree/manifest, complete transfer registry,
old/new input and output digests, toolchain/render locks, all comparison reports/regions, reviewer
identity, and dispositions. It cannot replace current relation/wording approval, navigator QA,
release evidence, or any recurring acceptance control.

### 11.4 One-way cutover and cleanup

1. Capture and verify the independent baseline from the accepted first-migration state.
2. Close navigator relation/wording schemas, profiles, registries, owners, draft review schedules,
   and transfer census before changing consumers.
3. Materialize navigator relation/wording XML plus provisional review views and coverage needed for
   migration comparison; do not issue recurring approval against pre-cleanup consumer bindings.
4. Implement the secure gateway and ephemeral model; migrate each consumer under the total transfer
   registry.
5. Generate only isolated temporary comparison candidates from the accepted upstream export,
   digest-locked provisional navigator XML, and declared controls. Mark them ineligible for live
   candidate, QA, release, bundle, or approval use.
6. Pass input, semantic, DOM, accessibility, interaction, security, print, and visual comparisons;
   disposition every difference.
7. Update the claims-navigator technical description, runbook, schemas, configuration, tests, and
   commands to the single new data path.
8. Remove old Markdown/content-JSON/relation-JSON/wording-JSON readers and semantic stores,
   adapters, caches, lifecycle/migration fields, aliases, fallbacks, migration-only dependencies,
   and migration-only branches; regenerate the exact operative root lock.
9. Invoke the idempotent cleanup handler on normal exit, handled failure, abort, and catchable
   termination. Remove the exact registered baseline, old runner, transfer mappings, renders,
   screenshots, diffs, temporary record, locators, and migration-only code/configuration. A later
   invocation recovers only a proven-stale lease after an uncatchable failure.
10. Prove all cleanup targets absent. Rewrite this draft pair into present-tense operative
    documents named `AA11393US-structured-source-html5_technical-description.md` and
    `AA11393US-structured-source-html5_acceptance-criteria.md`: remove this section and all
    old/new, migration, retirement, future-cutover, `_DRAFT`, temporary-evidence, and historical
    narrative and all `SH5-MIG-01` text (including later traceability references); renumber
    sections, update every inbound link, and regenerate the acceptance table.
11. From the cleaned final code/configuration and current usage registry, regenerate navigator
    relation/wording Markdown and coverage and obtain fresh exact-current projection/content/
    semantic approvals. Earlier provisional comparison views cannot authorize the build.
12. Invoke the navigator-owned procedure to regenerate candidates, attestations, QA, artifacts,
    checksums, releases, bundle configuration, bundles, and current records as the last declared
    writes.
13. Run the complete non-writing post-test gate on the exact integrated snapshot.

Cleanup is idempotent for absent, partial, and complete targets. A locator/lease is removed only
after its exact target is proven absent. Any retained archive, comparator, migration record, old
reader, or dual path prohibits regeneration, publication, and acceptance.

## 12. Acceptance traceability

The coupled acceptance document uses `SH5-AC-01` through `SH5-AC-10` for recurring controls and
`SH5-MIG-01` for the draft-only implementation gate. A distinct executable registry owns only the
second-migration criteria and namespaced callbacks. It binds—but never copies or merges—the
criteria of the exact upstream and navigator acceptance results. The one repository-global
outer-postcondition map remains solely owned by the navigator current-state gate.

Bidirectional meta-tests require every second-migration callback to have exactly one criterion
owner and reject unregistered production controls. The runner emits a complete ephemeral
namespaced receipt bound to the upstream export/result, navigator result, runner inputs, and
immutable snapshot. Its runner inputs bind the exact imported root project, lock, host `uv`, Python,
installed-distribution, and import-origin census. The outer current-state gate validates that
receipt, executes its separately owned test-isolation/post-test/no-write/final-snapshot controls,
and constructs the exact ten-result census only after final snapshot equality.

Neither a child receipt nor this migration registry may report repository currentness. Only the
outer navigator gate can compose the same-snapshot upstream, second-migration, independent navigator,
release/QA/bundle, and outer-postcondition results into `status: current`.

The draft-only gate and all temporary evidence/machinery are excluded from the recurring registry
and census and are removed during activation.

## 13. Standing decisions

| Topic | Decision |
|---|---|
| Upstream authority | Exact accepted structured-source export; imported read-only and revalidated |
| Runtime corpus input | Approved XML through a secure gateway, never Markdown/PDF/OCR/content JSON |
| Runtime model | Immutable and ephemeral; no persisted semantic adapter |
| Navigator relations | Navigator-owned XML with exact upstream endpoint tuples and independent semantic review |
| Navigator wording | Closed XML with typed slots and exact value origins |
| Product behavior | Existing navigator technical description and `AC-01`–`AC-20` remain authoritative |
| Migration equivalence | Semantic DOM, accessibility, interaction, print, and human visual review; not raw old/new byte identity alone |
| New-build determinism | Byte-identical artifacts and exact inventories from identical locked inputs |
| QA records | Same-schema records remain append-only; current profiles select exact required evidence |
| Compatibility | No accepted dual reader, adapter, fallback, alias, or semantic JSON |
| Python environment | Exact upstream-owned root project/lock under host-provided pinned `uv`; downstream commands are no-cache, offline, locked, and no-sync |
| Final certification | Complete post-test revalidation on one unchanged live snapshot |
| History | Git only; temporary baselines and migration evidence are deleted before acceptance |
