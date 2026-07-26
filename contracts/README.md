# Current Contract Router

> **OPERATIVE INTERNAL ROUTER · NOT FOR FILING**

This directory exposes the current normative documentation pairs in dependency order. The
phase numbers encode implementation dependency, not dates, versions, approval status, or
authority priority. The matter identifier remains in document headings and controlled artifact
names; repository-local contract filenames use their directory context instead.

```text
10-source-surfaces
├── pdf-transcription
└── authored-markdown
         │ validated item surfaces
         ▼
20-semantic-relations
└── authored-relations
         │ validated relation graph
         ▼
30-product-generation
└── claims-navigator
         │ deterministic product generation
         ▼
   committed artifacts
```

The two source-surface contracts at phase 10 are independently applicable. Phase 20 consumes
validated, stable item identities and exact endpoints. Phase 30 consumes the validated XML
surfaces and relation graph so product generation remains mechanical and does not repair,
reinterpret, or silently retarget upstream semantics.

| Phase | Contract pair | Current role |
|---|---|---|
| 10 | [PDF transcription technical description](10-source-surfaces/pdf-transcription/technical-description.md) / [acceptance criteria](10-source-surfaces/pdf-transcription/acceptance-criteria.md) | Governs asserted transcription XML and its generated Markdown review view while the source PDF remains authoritative. |
| 10 | [Authored Markdown technical description](10-source-surfaces/authored-markdown/technical-description.md) / [acceptance criteria](10-source-surfaces/authored-markdown/acceptance-criteria.md) | Governs Markdown-authoritative packages, generated XML, and the non-stored back-render check. |
| 20 | [Authored relations technical description](20-semantic-relations/authored-relations/technical-description.md) / [acceptance criteria](20-semantic-relations/authored-relations/acceptance-criteria.md) | Governs relation-XML authority, exact cross-reference endpoints, and generated Markdown review views. |
| 30 | [Claims navigator technical description](30-product-generation/claims-navigator/technical-description_DRAFT.md) / [acceptance criteria](30-product-generation/claims-navigator/acceptance-criteria_DRAFT.md) | Governs edition-blind model construction, rendering, verification, and committed navigator products. |

Each linked pair is normative for its stated domain. The root repository gate remains the one
aggregate current-state validation workflow across the dependency chain.
