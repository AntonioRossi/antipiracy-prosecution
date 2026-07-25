# AA11393US — Structured-Source HTML5 Migration: Technical Description (DRAFT)

> **PROPOSED ONE-WAY CUTOVER CONTRACT · INTERNAL DRAFT**
>
> This document defines the replacement of the navigator's Markdown and semantic-JSON content path
> with direct, read-only consumption of validated current XML representations and deterministic
> regeneration of the navigator HTML5 products.
>
> Its coupled acceptance contract is
> [`AA11393US-structured-source-html5-migration_acceptance-criteria_DRAFT.md`](AA11393US-structured-source-html5-migration_acceptance-criteria_DRAFT.md).
> Its mandatory upstream contract is the
> [structured-source technical description](AA11393US-structured-source-markdown_technical-description.md)
> and
> [acceptance criteria](AA11393US-structured-source-markdown_acceptance-criteria.md).
> The
> [claims-navigator technical description](AA11393US-claims-navigator_technical-description_DRAFT.md)
> and navigator `AC-01` through `AC-20` continue to control product behavior.

This pair is temporary implementation scaffolding for the one-way cutover. It never becomes a
third operative documentation pair. Before the final cutover snapshot, every enduring clause and
check unique to it is folded into the current claims-navigator technical description and sole
navigator acceptance registry, with exactly one current navigator criterion/callback owner. In the
same cutover this pair and all `SH5` IDs, registry entries, callbacks, fixtures, tests, support-file
bindings, and inbound references are removed. Retained test logic is re-homed under its navigator
owner; migration-only logic is deleted. Git alone retains the migration history.

## 1. Purpose and assurance boundary

The XML layer exists to give navigator one typed, item-addressable machine interface containing
stable identities, hierarchy, closed metadata, provenance, semantic digests, dependencies, and
exact relation endpoints. The navigator uses that interface to generate and manage HTML5 without
reconstructing semantics from presentation-oriented Markdown.

The final data path is:

```text
package-specific authority
        │
        ▼
validated current XML representation ──read-only──▶ navigator gateway
                                                        │
                                                        ▼
                                             immutable typed model
                                                        │
                                                        ▼
                                         deterministic HTML5 products
```

Consuming XML does not promote it to universal authority. The PDF still governs source fidelity;
authored Markdown still governs authored content; upstream relation XML still governs upstream
assertions; and navigator relation or wording XML governs only navigator-owned semantics.

The migration changes the navigator's input representation and replaces its legacy content-control
and authoring paths. It preserves user-visible product behavior unless the current navigator
contract expressly changes that behavior. Machine checks prove identity, schema validity,
reference resolution, origin traceability, security, and deterministic output. They do not prove
human attention, PDF transcription fidelity, authenticity, legal correctness, counsel approval,
filing readiness, or filing authorization. This pair creates no content-approval system.

## 2. Upstream dependency, authority, and ownership

Every navigator command validates one exact upstream structured-source result and resolves all
registered XML, dependencies, endpoints, assets, schemas, profiles, and mandatory computed coverage
from the same immutable repository snapshot. In each pre-test or final post-test phase, the global
gate builds that result and the XML indexes once and reuses them across editions and callbacks. The
final phase rebuilds from live bytes after tests; no pre-test result or index crosses that boundary.
A missing, stale, warning, skipped, unknown, dirty, or snapshot-mismatched upstream result fails
before model construction.

The navigator consumes these inputs according to their declared roles:

| Input | Governing authority | Navigator input role |
|---|---|---|
| PDF-derived package XML | Stored PDF governs fidelity; XML is the repository's asserted transcription and metadata | Validated runtime representation |
| Authored-package XML | Authored Markdown | Generated validated runtime representation |
| Upstream relation XML | Applicant-authored relation XML | Validated relation representation |
| Navigator relation XML | Navigator-owned relation XML | Authority for navigator-only assertions |
| Navigator wording XML | Navigator-owned wording XML | Authority only for controlled semantic wording |
| Schemas, profiles, and controls | Their registered current files | Closed mechanical control |
| Typed model and HTML5 | None; both are generated | Ephemeral model and deterministic products |

At cutover, every navigator semantic input edge—including corpus, relation, and wording
inputs—declares `inputRepresentation: "xml"` in its controlling registry. That declaration selects
bytes only. The gateway also receives each package's `authorityScheme` and XML role, and generated
HTML provenance preserves that distinction.

The same navigator registry holds their consumer edges and assigns navigator-owned relation XML the
exact scheme/role `navigator-relations-v1` / `authoritative-relations` and wording XML
`navigator-wording-v1` / `authoritative-wording`. These navigator-only packages are outside the
upstream content-package registry and its three scheme cardinalities, and do not inherit its
generated-Markdown or coverage-file requirements.

The navigator has read-only access to upstream files and to navigator relation and wording
authorities. A defect is corrected at its actual authority:

- authored content is corrected in Markdown and its XML is regenerated;
- a PDF transcription or provenance assertion is corrected in transcription XML against the PDF;
- an upstream relation is corrected in its authoritative relation XML; and
- navigator-only relations or wording are corrected in their navigator XML.

The navigator never patches a generated XML file, upstream assertion, typed model, or HTML5 product
to conceal a source defect.

All commands use the existing repository-root project and lock through the exact pre-provisioned
host `uv` and Python environment. Verification remains no-cache, offline, locked, and no-sync; it
does not install, resolve, download, or fall back to ambient packages or another environment.

## 3. XML item interface and feature contract

The gateway receives the uniform upstream item contract: stable document/item IDs, type, hierarchy,
order, exact content, typed metadata, provenance, semantic digest, dependencies, and relation
endpoints where applicable. Navigator-owned XML uses the same identity and secure-parser rules.

Stable item IDs remain stable through the typed model and HTML5. `itemId` is API notation for the
exact scheme-specific serialized identity, such as `fragmentId`, `relationId`, or `wordingId`; it is
not a second stored ID or compatibility alias. A DOM locator may add a fixed collision-safe prefix
or escape, but it remains a mechanical mapping from that ID. Line numbers, heading slugs, XPath
positions, visible text, array indexes, and current ordering are not identities.

Relations use exact `(documentId, fragmentId, fragmentContentDigest)` endpoints. Every endpoint,
forward link, reverse link, and displayed excerpt resolves against the current item index. Duplicate
semantic ownership, copied assertions, stale or ambiguous targets, inferred links, silent
retargeting, and endpoint-driven authority promotion fail.

The XML item model supports metadata-driven HTML5 capabilities such as:

- stable deep links;
- forward and reverse relation navigation;
- filtering and grouping;
- provenance and uncertainty display;
- caution and disposition indicators;
- claim and dependency navigation; and
- accessible names and relationships.

A feature-driving value is an exact schema field or registered mechanical derivation named by a
consumer binding. Adding one requires a coherent change to its declared human-maintained source,
schema/profile, conversion or navigator-owned XML, typed model, renderer, consumer binding, and
focused tests. Unknown fields, arbitrary extension maps, dynamic scripts, and generic executable
template values are not feature mechanisms.

## 4. Navigator-owned XML

### 4.1 Relation packages

Navigator-only edition mappings and navigation assertions have one owner in:

```text
navigator/relations/na__pct.relations.xml
navigator/relations/af__pct.relations.xml
```

These packages use the upstream relation identity and endpoint contract. They may reference an
upstream assertion by stable relation ID but cannot restate, override, or silently retarget it.
Source-level support, prior-art, priority, comparison, mapping, and crosswalk assertions remain
upstream-owned.

Each relation declares stable identity, owner, type, direction, ordered fields, exact endpoints,
and the navigator contexts that consume it. No separate Markdown or coverage companion is required;
the current XML, resolved endpoints, and generated HTML provide the inspection path.

### 4.2 Controlled semantic wording

Navigator wording XML owns only wording whose exact text carries machine-enforced substantive or
security meaning: provenance and disclaimer text, relation cautions and dispositions, and
edition-specific profile/artifact/release or manifest wording whose exact text carries declared
substantive or security meaning. The current owners are:

```text
navigator/wording/shared.wording.xml
navigator/wording/na.wording.xml
navigator/wording/af.wording.xml
```

Ordinary UI copy—navigation labels, button text, help text, headings, and layout instructions that
do not carry those meanings—is owned directly by its tracked template or code file. It remains
subject to navigator accessibility, security, neutrality, and deterministic-output tests, but
requires no `wordingId`, XML entry, or semantic-origin record.

Each controlled wording entry has a stable `wordingId`, locale, ownership scope, allowed usage
contexts, fixed text, and zero or more named typed slots. Shared wording exists only in the shared
bundle; edition-specific wording exists only in its edition bundle.

Wording XML uses its exact current namespace, schema, profile, subject ID, secure-parser policy,
canonicalization, raw digest, and semantic digest. Unknown or older wording formats fail closed.

A slot declares only its name, scalar value type, output-context escape class, and one exact allowed
origin. Order and cardinality derive from its declared occurrence; a closed formatter is declared
only when formatting is required. Allowed origins are an upstream item field, relation field,
registered control, closed mechanical derivation, or typed interaction-state field. Arbitrary
runtime strings, alternate origins, executable templates, raw HTML slots, and a generic “safe”
bypass are prohibited.

Navigator XML has no content-approval record, reviewer registry, confirmation token, or approval
resolver.

## 5. Secure gateway and typed model

All production semantic reads pass through one registered gateway. It:

1. verifies the same-snapshot upstream result and declared consumer inputs;
2. secure-parses the exact current upstream and navigator XML;
3. validates schemas, identities, metadata, digests, dependencies, endpoints, assets, controlled
   wording entries, and declared substantive or security-relevant slot origins;
4. records the ephemeral set of files actually read; and
5. constructs and seals one immutable in-memory model before rendering.

The gateway rejects undeclared files, symlinks or path escapes, external resources, unknown
versions or fields, duplicate IDs or owners, endpoint drift, invalid slot values, and representation
fallbacks.

The model provides typed operations equivalent to:

```text
getDocument(documentId)
getItem(documentId, itemId)
getMetadata(documentId, itemId)
resolveRelation(relationId)
relationsFor(documentId, itemId)
```

These names are illustrative; the implementation may use one equally narrow typed API. Renderers
do not traverse XML directly or invent their own parsing rules.

Production code cannot read semantic content from Markdown, PDF/OCR, content JSON, relation JSON,
wording JSON, caches, aliases, migration files, or network resources. It cannot persist the typed
model as a semantic source. Temporary diagnostic dumps used by tests stay outside the live tree and
are removed before success.

Production build, verification, release, and bundle commands cannot write upstream files or
navigator relation/wording XML; those authorities are edited directly and validated before use.
The typed model may select and order declared fields but cannot normalize substantive text, infer
a relation, retarget an endpoint, repair a dependency, or invent controlled semantic wording.

## 6. Deterministic and attributable HTML5

The renderer receives only the sealed typed model and declared templates, stylesheets, scripts,
assets, fonts, locale, edition/profile selection, and presentation controls. It cannot parse
Markdown, discover inputs, evaluate arbitrary template code, or substitute cached content.

For every registered edition and surface, generation preserves:

- exact visible source text and scheme-specific provenance;
- source item IDs and deterministic DOM locators;
- claim order, numbering, dependency, grouping, and status;
- relation direction, posture, gates, cautions, dispositions, and endpoint navigation;
- heading, landmark, list, table, link, figure, and caption structure;
- accessible names, descriptions, relationships, focus order, and interaction state;
- no-JavaScript readability and functional navigation;
- print content, order, and page-break behavior; and
- controlled semantic wording and template/code-owned ordinary UI copy required by the navigator
  contract.

The verifier computes a non-stored origin inventory covering source-derived content, relations,
identifiers and provenance, controlled semantic wording and slot values, security-sensitive dynamic
values, and registered feature-driving fields or derivations. Every covered value maps to its
stable item and authority scheme, navigator XML entry, registered control, typed interaction-state
field, or closed derivation. Ordinary template/code-owned copy is excluded from this semantic
inventory; its tracked source file remains its owner. The renderer adds only mechanical markup and
declared derived values.

All dynamic values—whether supplied by content XML, wording XML, controls, or code—use their
declared output-context escaping. No ordinary-copy exemption permits unescaped interpolation, raw
markup, script, event handlers, unsafe URLs, styles, or executable templates. XML validation
establishes provenance, not output-context safety.

Fresh processes with identical locked inputs reproduce byte-identical HTML5 candidates and
identical computed origin inventories. Ordering, line endings, timestamps, random values, paths,
locale, and tool metadata are fixed or excluded by declared mechanical rules. The inventory is
ephemeral machine evidence: it is not committed, stored as a receipt, or substituted for a product
manifest. The navigator product contract owns determinism for manifests, sealed artifacts,
releases, and bundles.

## 7. Navigator behavior, QA, and release

The cutover-updated claims-navigator technical description and its acceptance registry become the
sole navigator architecture and product contract for XML input, editions, navigation, interaction,
accessibility, no-JavaScript, print, security, QA profiles, candidates, releases, artifacts, and
bundles. This migration neither copies nor weakens those user-visible and release requirements.

Navigator product, QA, and release records remain only where the cutover-updated navigator contract
uses them for machine-observed product or release state. They do not authorize XML content.
Relation/content review fields, wording approvals, owner attestations, their record types and
dependencies, and their commands, resolvers, and callbacks are removed. This pair adds no XML
content-approval records or parallel authorization graph. Current navigator product outcomes
remain, while criterion text and enforcers are coherently cutover-updated; obsolete approval
mechanics are not preserved merely to retain old wording. An intentional user-visible product
change requires a corresponding current navigator contract change; it cannot be hidden inside the
input migration. No independent HTML5-input result remains after cutover.

After the XML path and cleanup are complete, the navigator's existing release procedure regenerates
all current candidates, QA outputs, artifacts, checksums, releases, manifests, and bundles from the
new inputs.

## 8. Commands and writes

The navigator retains one registered command surface for input validation, candidate generation and
comparison, release verification, bundle generation, and current-state verification. Exact command
names remain controlled by the navigator command registry and runbook.

Input validation is read-only. Build, verification, release, and bundle commands never write
semantic authorities; mutating commands write only their declared downstream generated products.
They validate inputs before writing and atomically replace each permitted file. A caught failure
restores only unchanged command-owned outputs and never overwrites external changes. Abrupt
termination may leave a mixed generated set; verification rejects it and a clean regeneration or
Git restores it.

Unsupported schemas, sources, relations, wording, profiles, artifacts, or tool versions fail before
writes. No command introduces an alternate environment, implicit synchronization, package
installation, compatibility reader, or fallback.

## 9. One-way cutover

Implementation follows one direct sequence:

1. make the upstream structured-source contract and XML representations pass;
2. preserve required navigator behavior in current product tests;
3. create current navigator relation and controlled-wording XML and their schemas;
4. implement the gateway, typed model, and XML-driven renderer;
5. fold every enduring clause and check unique to this pair into exactly one owner in the current
   claims-navigator technical description and existing acceptance registry, and update its schemas,
   corpus and edition registries, command registry, runbook, and retained tests to the XML input
   contract;
6. change the navigator consumer declarations to `xml` in the same change that removes the old
   readers and the relation/content authoring commands;
7. compare source-derived and controlled semantic content, semantic DOM, item identities,
   relations, navigation, accessibility, interaction, no-JavaScript, print, security, computed
   origin coverage, and deterministic output;
8. remove Markdown and semantic-JSON readers, duplicate semantic stores, adapters, caches, aliases,
   fallbacks, migration helpers, unused code, and tests serving only removed paths;
9. establish temporary cutover readiness against this pair, the exact upstream result, and the
   cutover-updated navigator result;
10. delete both SH5 documents and every `SH5` ID, registry entry, callback, fixture, test,
    support-file binding, and inbound reference, re-homing only enduring checks under their sole
    navigator owners; and
11. regenerate the current navigator products and run the repository-global gate against the
    upstream structured-source result and single current navigator result.

The comparison uses the current navigator contract, existing tests, committed products, and Git
history. It creates no baseline archive, lease system, transfer registry, approval record, or
detached evidence package. A source defect returns to its authority and restarts regeneration. A
product change is documented and tested as a product change.

This draft pair is not renamed or converted into an operative HTML5 pair. Cutover is complete only
after the transfer and deletion above; the live checkout then states the XML architecture solely
through the upstream structured-source pair and current claims-navigator contract and registry.

## 10. Audit, final gate, and live closure

The audit chain is:

```text
exact clean Git commit
→ current structured-source result and registered XML
→ navigator XML, controls, typed gateway, and renderer
→ current HTML5 products and independent navigator result
→ unchanged-snapshot validate-current result
```

`uv --no-cache --offline run --locked --no-sync python -m navigator validate-current` is the sole
repository-global current-state gate. After transfer it captures one immutable snapshot, runs the
exact upstream and single current navigator checks, executes tests in isolation, revalidates
current products after tests, verifies no-write postconditions, and accepts only the unchanged
final snapshot. Every retained HTML5-input check is owned by a current navigator callback.

Before deletion, the temporary `SH5-AC-01` through `SH5-AC-10` mapping may establish cutover
readiness. It is never bound into a release or retained as a third acceptance result. Final
current-state verification rejects every SH5 document, ID, registry entry, callback, fixture, test,
support binding, or reference.

The accepted implementation contains one semantic XML ingestion path, one typed model, and only
current renderers, schemas, controls, tests, products, and navigator records required by the product
contract. It contains no Markdown or semantic-JSON content reader, dual ingestion path, adapter,
compatibility branch, fallback, semantic cache, XML content-approval system, migration machinery,
stale artifact, duplicated assertion, auxiliary history document, SH5 scaffolding, or helper/test
used only by a removed path.
