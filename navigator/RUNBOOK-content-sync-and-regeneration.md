# Content Sync and Navigator Regeneration Runbook

> **CURRENT OPERATING PROCEDURE · INTERNAL COUNSEL-REVIEW SYSTEM**

This runbook applies the normative contract in
[`../AA11393US-claims-navigator_technical-description_DRAFT.md`](../AA11393US-claims-navigator_technical-description_DRAFT.md)
and its
[`acceptance criteria`](../AA11393US-claims-navigator_acceptance-criteria_DRAFT.md).
Those documents control any conflict. This runbook supplies the shortest supported update path;
it creates no exception or alternative release path.

## 1. Current contract

- Work from one repository checkout and one exact Git commit. Do not read semantic content from
  another worktree, an external directory, a symlink, a cache, or the network.
- Preserve each package's declared authority direction. XML is the uniform machine interface, not
  a universal replacement authority.
- Navigator production reads semantic content only through the secure XML gateway. The renderer
  consumes only the immutable typed model produced by that gateway.
- Keep only current schemas, current content, current relations, current wording, tests, and
  generated products. Git retains history.
- Coverage and substantive-origin tracing are computed during validation and are not committed as
  separate inventories.
- Do not create author approvals, self-review evidence, receipts, attestations, handoff archives,
  or other proof that the sole contributor reviewed their own work.

The navigator exposes exactly these five commands:

| Command | Effect |
|---|---|
| `preview <edition>` | Writes one non-persistent HTML preview to standard output |
| `candidate <edition>` | Regenerates the edition's current candidate HTML |
| `release <edition>` | Reproduces the candidate and atomically writes the sealed HTML and detached checksum |
| `bundle` | Regenerates the deterministic five-member delivery ZIP and its detached checksum |
| `validate-current` | Read-only validation of the exact unchanged current repository snapshot |

`<edition>` is exactly `na` or `af`. There are no command aliases or upgrade paths.

## 2. Change content according to its authority

Identify every affected package in the structured-source content registry before editing.

- **PDF evidence package:** never edit the canonical PDF. Correct the asserted transcription XML
  only against that PDF, preserve page/region provenance and uncertainty disclosures, and
  regenerate the Markdown review view.
- **Authored-Markdown package:** edit the authoritative Markdown, then regenerate its XML
  representation. Do not edit the generated XML or maintain a second Markdown owner.
- **Authored-relation package:** edit the authoritative relation XML and regenerate its Markdown
  review view. Every endpoint remains directional, identity-bound, and digest-bound.

Use the structured-source documentation pair for the applicable conversion procedure. Stop if a
generated representation differs from regeneration, a Markdown round trip loses semantics, PDF
provenance is incomplete, a relation endpoint is unresolved, or a consumer would need a fallback.

## 3. Update navigator-owned XML

Edit only the edition relation file or controlled-wording file that owns the changed semantic
value:

```text
navigator/relations/na__pct.relations.xml
navigator/relations/af__pct.relations.xml
navigator/wording/shared.wording.xml
navigator/wording/na.wording.xml
navigator/wording/af.wording.xml
```

Keep ordinary interface labels and layout instructions in the renderer. Put only substantive,
provenance, caution, disposition, disclaimer, product-label, artifact, manifest, or security
wording in wording XML. Add only slots that are actually consumed and give each slot one typed
scalar type and one exact origin; every slot is rendered as escaped plain text.

Review each affected relation against the current source item. Do not infer a target, copy one
edition's mapping into the other, reuse a stale digest, or use visible text, order, line number, or
heading slug as identity. A fragment with no recorded candidate remains explicitly
`counsel-review-required`.

## 4. Inspect and generate both editions

A preview is read-only and writes HTML to standard output:

```sh
uv --no-cache --offline run --locked --no-sync python -m navigator preview na
uv --no-cache --offline run --locked --no-sync python -m navigator preview af
```

Inspect the changed edition visually, including forward and reverse navigation, no-candidate
states, cautions and gates, disclosure figures, keyboard focus, the no-JavaScript document order,
and print content. Visual inspection is useful product review, not a stored authorization step.

Regenerate both current candidates so shared-input drift cannot remain hidden:

```sh
uv --no-cache --offline run --locked --no-sync python -m navigator candidate na
uv --no-cache --offline run --locked --no-sync python -m navigator candidate af
```

Stop if either edition reads the other's private input, any semantic source bypasses the XML
gateway, a relation or wording entry is unused or unresolved, or regeneration is not byte-stable.

## 5. Seal and bundle

Release reproduces each candidate in a fresh process before replacing only its generated product
and detached checksum:

```sh
uv --no-cache --offline run --locked --no-sync python -m navigator release na
uv --no-cache --offline run --locked --no-sync python -m navigator release af
uv --no-cache --offline run --locked --no-sync python -m navigator bundle
```

The bundle must contain exactly both sealed HTML files, both corresponding detached checksums, and
`MANIFEST.txt`. Its own detached checksum stays beside the ZIP. The ZIP is a delivery product, not
an audit package. Remove any superseded generated product before the final commit.

## 6. Final audit gate

Inspect the complete current diff, run `git diff --check`, and commit the coherent current state.
From that clean exact commit run:

```sh
uv --no-cache --offline run --locked --no-sync python -m navigator validate-current
```

Stop on every skip, unknown criterion, validation failure, stale product, undeclared read or
write, failed test, source-manifest mismatch, tracked-Markdown render failure, or repository
mutation. The gate certifies only the unchanged snapshot it actually read.

The audit unit is:

```text
exact clean Git commit
→ repository checkout and supplied Git history
→ current documentation pairs and executable acceptance registry
→ validate-current result
```

No separately packaged audit artifact or contributor self-attestation adds authority to that unit.

## 7. Failure handling

- Treat a failed command as a stop condition. Correct the declared source and rerun the affected
  generation steps; do not weaken a validator.
- Never repair generated HTML, checksums, the manifest, or ZIP by hand.
- Never repair semantic content in the typed model or renderer. Correct its owning XML or the
  package authority and regenerate.
- If source content changes after candidate generation, regenerate candidates, releases, and the
  bundle before committing.
- If the clean commit changes after validation, rerun `validate-current`; the earlier result does
  not apply to the new commit.
