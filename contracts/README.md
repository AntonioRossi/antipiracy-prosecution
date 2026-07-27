# Current Contract Router

> **OPERATIVE INTERNAL ROUTER · NOT FOR FILING**

This directory exposes the current normative documentation pairs in dependency order. The
phase numbers encode implementation dependency, not dates, versions, approval status, or
authority priority. The matter identifier remains in document headings and controlled artifact
names; repository-local contract filenames use their directory context instead.

```text
phase 10 validated XML item surfaces
        ├──exact endpoint resolution──▶ phase 20 authored relations
        │                                  │ aggregate prerequisite only
        │                                  │ zero navigator handoffs
        │                                  ▼
        └──exactly two XML handoffs───▶ phase 30 claims navigator
                                           │ + navigator-owned XML controls
                                           ▼
                                  stored deterministic products
```

The two source-surface contracts at phase 10 are independently applicable. Phase 20 consumes
validated, stable item identities only to resolve its exact authored-relation endpoints. Complete
phase-20 acceptance is an aggregate prerequisite for phase 30, but current authored-relation
packages have zero navigator consumer edges and supply no navigator runtime handoff. Phase 30
consumes exactly two structured-source XML handoffs per edition and separately governed
navigator-owned relation, wording, edition, and schema controls. Product generation does not
repair, reinterpret, copy, or silently retarget upstream semantics.

| Phase | Contract pair | Current role |
|---|---|---|
| 10 | [PDF transcription technical description](10-source-surfaces/pdf-transcription/technical-description.md) / [acceptance criteria](10-source-surfaces/pdf-transcription/acceptance-criteria.md) | Governs asserted transcription XML and its generated Markdown review view while the source PDF remains authoritative. |
| 10 | [Authored Markdown technical description](10-source-surfaces/authored-markdown/technical-description.md) / [acceptance criteria](10-source-surfaces/authored-markdown/acceptance-criteria.md) | Governs Markdown-authoritative packages, generated XML, and the non-stored back-render check. |
| 20 | [Authored relations technical description](20-semantic-relations/authored-relations/technical-description.md) / [acceptance criteria](20-semantic-relations/authored-relations/acceptance-criteria.md) | Governs relation-XML authority, exact cross-reference endpoints, and generated Markdown review views. |
| 30 | [Claims navigator technical description](30-product-generation/claims-navigator/technical-description_DRAFT.md) / [acceptance criteria](30-product-generation/claims-navigator/acceptance-criteria_DRAFT.md) | Governs edition-blind model construction, rendering, verification, and stored navigator products. |

Each linked pair is normative for its stated domain.

Each pair, its data-only acceptance registry, applicable registry/configuration slice, controls,
implementation, registered tests and vectors, generated representations or products, and declared
handoffs form one current state. No pair or implementation component is accepted independently.
Missing, additional, alternate, inactive, or contradictory members fail the shared gate. Phase
numbers express this dependency law; they are not publication chronology or Git state.

## Aggregate validation boundary

The root [`Validation`](../README.md#validation) section defines the one aggregate current-state
workflow across the complete dependency chain. Domain contracts contribute only their declared
criteria and link to this shared boundary; they do not define another aggregate command.
