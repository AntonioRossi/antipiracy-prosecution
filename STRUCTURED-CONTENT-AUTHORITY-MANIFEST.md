# Structured Content Authority and XML Machine-Interface Router

> **CURRENT REPOSITORY GUIDANCE · NOT FOR FILING**

This document routes the repository's current authority schemes and uniform XML machine interface.
The applicable [`contracts`](contracts/README.md), their data-only acceptance registries, and their
executable enforcers control. This router adds no authority, acceptance criterion, command,
consumer edge, implementation path, or release exception.

## 1. Current authority directions

| Domain | Governing authority | XML role | Markdown role | Current navigator role |
|---|---|---|---|---|
| PDF evidence transcription | Stored PDF governs fidelity; transcription XML owns the asserted transcription, provenance, stable IDs, uncertainty, and typed metadata | Manually maintained validated transcription and consumer interface | Deterministic review view | Declared navigator edges hand transcription XML only |
| Authored Markdown | Authored Markdown owns adopted content, anchors, order, and substantive metadata | Deterministic, round-trip-validated consumer interface | Authority | Declared navigator edges hand generated XML only |
| Authored relations | Relation XML owns each profiled assertion, field, direction, owner, and exact endpoint | Authority and validated relation interface | Deterministic review view | Aggregate prerequisite with zero navigator edges or handoffs |
| Navigator relations and wording | Navigator-owned XML owns only navigator associations and controlled wording | Validated navigator control input | No semantic input | Read through the navigator gateway after structured-source acceptance |

XML is the one uniform machine interface, not a universal authority. Selecting XML for a consumer
never changes the authority direction. Generated XML, generated Markdown, immutable typed models,
HTML5 products, checksums, and bundles acquire no independent semantic authority.

## 2. Current navigator machine path

```text
package-specific authorities
        │
        ▼
all three structured-source domains pass aggregate acceptance
        │
        ▼
exactly two retained XML handoffs per edition
(authored generated XML; PDF-transcription XML plus declared assets)
        │
        ▼
navigator gateway reads navigator-owned XML controls
        │
        ▼
immutable typed model ──deterministic projection──▶ stored HTML5 products
```

The current navigator never receives, reopens, or reconverts authored Markdown and never parses a
PDF, OCR derivative, generated Markdown review view, or upstream authored-relation package as a
semantic input. Markdown and PDF paths can occur in inherited validation-read evidence because
upstream validation proves generated XML against its authority and binds transcription XML to
stored evidence. That census grants no consumer access.

Navigator claim-to-PCT associations come only from the configured files under
`navigator/relations/`. Those files use the navigator-owned relation grammar and contain no field
for an upstream authored-relation reference. Phase-20 authored relations remain independently
validated and have a current consumer-edge and handoff census of zero.

## 3. Ownership and correction boundary

Each package has one governing authority and every substantive field has one maintained owner.
Each mechanical field has one deterministic owner. Correct a defect only at that owner:

- authored content, anchors, order, and substantive metadata are corrected in Markdown before XML
  regeneration;
- asserted PDF transcription, provenance, uncertainty, and stable IDs are corrected in
  transcription XML against the stored PDF;
- source-level assertions and endpoints are corrected in authored relation XML;
- navigator-only associations and controlled wording are corrected in navigator-owned XML.

Generated XML, generated review Markdown, typed models, HTML5, checksums, manifests, and ZIP files
are never manually patched to conceal an upstream defect. Unknown fields, formats, schemas,
authority schemes, consumer inputs, dependencies, or conversion paths fail closed.

## 4. Identity, reference, and validation boundary

Stable IDs are maintained by the authority scheme named in the package registry. Cross-package
references resolve exact document IDs, fragment IDs, typed-item digests, and profiled endpoint
roles. Visible text, headings, ordering, line numbers, and generated anchors cannot substitute for
identity. Missing, duplicate, ambiguous, inferred, reversed, retargeted, or stale references fail.

Validation computes coverage, fragment bindings, typed records, digests, back-render comparison,
and substantive-origin tracing from current retained bytes. These are ephemeral checks, not stored
registries, receipts, lineage files, or approval records. Machine validation proves technical
coherence and deterministic reproducibility only; human review of evidence and substantive
analysis remains authoritative.

## 5. Contract and implementation closure

Each technical description, paired acceptance criteria, data-only acceptance registry, applicable
content or product configuration, schemas and profiles, implementation, registered tests and
vectors, generated representations, declared handoffs, and stored products form one indivisible
current state. A documentation-only, registry-only, implementation-only, workflow-only, test-only,
control-only, generated-only, handoff-only, or product-only state fails.

The [`contract router`](contracts/README.md) defines the dependency boundary. Phase 20 validates
authored relations but supplies no navigator runtime relation graph. Phase 30 consumes exactly its
declared XML handoffs and navigator-owned controls. Missing, additional, alternate, inactive, or
contradictory implementation members fail before publication.

## 6. Commands and writes

Structured-source component commands validate one subject, regenerate one subject's derived
representation, or regenerate genuinely derived controls. They never write an authority file.
Candidate controls and generated representations are fully validated before the first write,
atomically replaced, reread from replacement bytes, and validated without reusing candidate state.

Navigator product commands validate the product contract pair, acceptance registry, exact live
implementation census, product plan, structured-source closure, and applicable retained inputs
before model construction or publication. They write only declared files under `navigator/dist/`.

The sole aggregate current-state command is:

```sh
uv --no-cache --offline run --locked --no-sync python -m navigator validate-current
```

It validates one retained worktree capture and requires an unchanged final recapture. Repository
status, index state, commit identity, and history are outside the pass conditions. A pass is an
ephemeral technical result and creates no approval, filing authorization, or entitlement to rely
without reviewing the evidence.
