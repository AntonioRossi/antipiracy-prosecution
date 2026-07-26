# AA11393US — Authored Markdown to XML Technical Description

> **OPERATIVE INTERNAL CONTROL · NOT FOR FILING**
>
> This document defines the current authored-Markdown authority scheme and its consumer-neutral XML
> handoff. The coupled acceptance contract is
> [`AA11393US-structured-source-authored-markdown_acceptance-criteria.md`](AA11393US-structured-source-authored-markdown_acceptance-criteria.md).

## 1. Purpose and authority boundary

The current direction is:

```text
authored Markdown authority ──deterministic conversion──▶ generated XML
                                                              │
                                                              ├──non-stored semantic back-render check
                                                              └──validated, read-only──▶ declared consumer interface
```

Markdown is the sole owner of adopted content-bearing material, stable item identities, and
substantive item metadata. XML is the generated typed machine representation. The semantic
back-render is ephemeral comparison evidence and is never stored as a second Markdown owner.

Machine validation proves supported-profile parsing, identity and metadata preservation,
conversion completeness, semantic round-trip equivalence, coverage, and deterministic XML. It does
not prove human attention, substantive or legal correctness, counsel approval, filing readiness,
or filing authorization.

## 2. Package and ownership contract

Every package declares `authorityScheme="authored-markdown-v1"` and has exactly one authoritative
`markdownFile` and one generated `xmlFile`. It has no stored PDF, source manifest, generated review
Markdown companion, or manually maintained XML region.

Authoritative Markdown contains the package's stable `ssp-*` anchors and every adopted
content-bearing structure and substantive metadata field. XML preserves those semantics and may
add only classified mechanical envelope fields: schema/profile/version declarations, authority
binding and raw digest, deterministic ordinals, and generated semantic digests.

Stable IDs are not derived from line numbers, heading slugs, XML positions, array indexes, visible
text, or current ordering. Unknown fields, untyped extension maps, hidden content, competing
owners, and substantive information present only in generated XML fail closed.

## 3. Markdown profile and generated XML

Markdown uses the pinned GFM reader, one stable-anchor syntax, LF line endings, final newline, NFC,
closed link schemes, and only the current profile's supported constructors. Unsupported raw HTML,
unpaired or duplicate anchors, unsafe links, lossy structures, ambiguous claims, and constructs
outside the profile fail before generation.

Generated XML uses the exact current namespace, XSD, and profile; UTF-8 XML 1.0; NFC text; and the
secure parser. DTDs, non-predefined entities, external resources, XInclude, XLink, comments,
processing instructions, CDATA, `xml:base`, recovery, duplicate IDs, unknown fields or versions,
aliases, and resource-limit violations fail closed.

The XML authority binding records the exact Markdown path, raw digest, and size. Raw and
domain-separated canonical semantic digests are computed from the immutable snapshot. Item digests
cover stable identity, type, profile, semantic content, and substantive metadata while excluding
presentation, paths, unrelated document metadata, generator versions, and sibling items.

## 4. Conversion, semantic back-render, and coverage

The pinned converter preserves the complete supported ordered Pandoc AST: headings, paragraphs,
lists, tables and cells, claims and limitations, links, notes, code, advisories, identities,
metadata, hierarchy, and order. Fresh XML must equal the registered generated XML byte-for-byte.

Rendering that XML to the same pinned GFM semantic form must preserve the ordered Pandoc AST after
only the profile-listed presentation normalizations: anchor-carrier placement, equivalent Markdown
escaping, and final newline. A normalization cannot add, remove, reorder, or rewrite a
content-bearing node.

Coverage is computed from the current snapshot and maps every authoritative Markdown item to its
generated XML item, semantic digest, and back-rendered semantic node. Neither the back-render nor a
package-level coverage artifact is stored.

## 5. Consumer-neutral handoff

A declared consumer edge selects exactly one registered representation, `xml` or `markdown`, and
cannot read the other representation through an undeclared dependency. An XML handoff supplies the
authority scheme, generated role, stable typed items, hierarchy, content, metadata, dependencies,
and digests. A Markdown handoff supplies the authority bytes directly.

Selection of XML never promotes it above Markdown authority. A consumer may not repair generated
XML, infer missing authored content, add source-domain fields, reparse an undeclared representation,
or silently fall back. Product behavior, presentation, interaction, security, release, and
delivery are outside this contract.

## 6. Commands, writes, and aggregate verification

The shared structured-source command surface remains exactly `check <subject-id>`, `regenerate
<subject-id>`, `regenerate-controls`, and `verify-current`.

For this scheme, `check` validates one package and its declared dependencies without writing;
`regenerate` validates Markdown and the complete proposed XML before atomically replacing only that
package's generated XML; `regenerate-controls` replaces only derived routers and the three
acceptance table regions; and `verify-current` participates in one memoized whole-corpus pass.
Markdown authority and externally changed bytes are never overwritten. Coverage and back-render
evidence are computed and never persisted.

The repository-global gate owns immutable snapshot bracketing, registered isolated tests, final
snapshot revalidation, and the aggregate result. This domain contributes its own acceptance
statuses without defining any consumer product outcome.

## 7. Live implementation closure

This technical description, its acceptance criteria, its data-only acceptance registry, the
content registry's authored-Markdown slice, current schemas and profiles, converter, focused tests,
and registered packages are the complete live implementation.

No alternate converter, editable generated owner, compatibility or migration reader, approval or
reviewer record, stored receipt, digest ledger, persisted back-render, coverage store, export path,
or inactive domain artifact remains operative. Git alone retains implementation history.
