# Content Sync and Navigator Regeneration Runbook

> **CURRENT OPERATING PROCEDURE · INTERNAL COUNSEL-REVIEW SYSTEM**

This runbook applies the normative claims-to-specification
[`technical description`](../contracts/30-product-generation/claims-navigator/technical-description_DRAFT.md)
and [`acceptance criteria`](../contracts/30-product-generation/claims-navigator/acceptance-criteria_DRAFT.md),
and the claims-to-prior-art
[`technical description`](../contracts/30-product-generation/claims-prior-art-navigator/technical-description_DRAFT.md)
and [`acceptance criteria`](../contracts/30-product-generation/claims-prior-art-navigator/acceptance-criteria_DRAFT.md),
and the shared navigator-presentation
[`technical description`](../contracts/30-product-generation/navigator-presentation/technical-description_DRAFT.md)
and [`acceptance criteria`](../contracts/30-product-generation/navigator-presentation/acceptance-criteria_DRAFT.md),
and the shared navigator-guide
[`technical description`](../contracts/30-product-generation/navigator-guide/technical-description_DRAFT.md)
and [`acceptance criteria`](../contracts/30-product-generation/navigator-guide/acceptance-criteria_DRAFT.md).
Those pairs control any conflict. This runbook supplies the shortest supported update path; it
creates no exception or alternative release path.

All four phase-30 contract pairs and navigator acceptance registries, structured-source contracts and
registries, navigator implementation and workflow, controls, tests and vectors, generated
representations, handoffs, and stored products are one current state. No documentation-only,
registry-only, implementation-only, workflow-only, control-only, test-only, or product-only state
is releasable.

Provision the exact locked project environment and the policy-bound browser before using any
navigator command:

```sh
uv --no-cache sync --locked
uv --no-cache run --locked python -m playwright install chromium
```

The installed Playwright distribution, Playwright-managed Chromium revision and browser version
must equal `navigator/policy/browser.json`. An absent or different runtime is a stop condition;
there is no system-browser or alternate-engine fallback. Subsequent navigator commands use
`--offline --no-sync` and validate the exact environment before accepting work.

## 1. Current contract

- Work from the current worktree. Aggregate validation captures its governed inventory and bytes;
  repository status, index state, commit identity, and history do not affect the result. Do not
  read semantic content from another worktree, an external directory, a symlink, a cache, or the
  network.
- Preserve each package's declared authority direction. XML is the uniform machine interface, not
  a universal replacement authority.
- Navigator production receives registered packages only through the frozen structured-source
  handoff. Its read-only gateway binds that validation census without reopening handed paths and
  reads only navigator-owned controls. The renderer consumes only the resulting immutable model.
- Keep only current schemas, current content, current relations, current wording, tests, and
  generated products.
- Coverage and substantive-origin tracing are computed during validation and are not stored as
  separate inventories.
- Do not create author approvals, reviewer records, validation receipts, handoff archives, or
  stored claims that a contributor reviewed the evidence.
- Before changing an operative field, behavior, command, input, workflow, control, or product,
  identify its controlling contract and registry row. The retained candidate must update every
  affected owner, enforcer, test, vector, generated representation, handoff, and product coherently.

The navigator exposes exactly these five commands:

| Command | Effect |
|---|---|
| `preview <product>` | Writes one non-persistent HTML preview to standard output |
| `candidate <product>` | Regenerates the product's current candidate HTML |
| `release <product>` | Reproduces the candidate and atomically writes the sealed HTML and detached checksum |
| `bundle` | Regenerates the configured-product delivery ZIP and its detached checksum |
| `validate-current` | Sole aggregate, read-only validation of one unchanged retained worktree capture |

`<product>` must be an exact member of `navigator/bundles/current.json`: `na-specification`,
`af-specification`, `na-prior-art`, or `af-prior-art`. There are no shorter command identities or
implicit product choices.

Every command validates all four phase-30 contract pairs and acceptance registries, the exact implementation
census, product plan, structured-source closure, and applicable retained inputs before model
construction or publication. Stop if those inputs describe different behavior; no later check or
rollback repairs a split state.

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

Edit only the configured product relation file or controlled-wording file that owns the changed
semantic value. The current paths are:

```text
navigator/relations/na__pct.relations.xml
navigator/relations/af__pct.relations.xml
navigator/wording/shared.wording.xml
navigator/wording/na.wording.xml
navigator/wording/af.wording.xml
navigator/wording/prior-art.wording.xml
```

Keep ordinary interface labels and layout instructions in the renderer. Put only substantive,
provenance, caution, disposition, disclaimer, product-label, artifact, manifest, security, or
guide wording in wording XML. Add only slots that are actually consumed and give each slot one typed
scalar type and one exact origin; every slot is rendered as escaped plain text.

Review each affected relation against the current source item. Do not infer a target, copy one
edition's mapping into the other, reuse a stale digest, or use visible text, order, line number, or
heading slug as identity. A fragment with no recorded candidate displays the computed
`counsel-review-required` unit state; every matrix obligation retains its authored exact state.

For a claims-to-prior-art change, reconcile the complete matrix relation/field/claim/document
obligation census in the strategy-owned passage-map relation XML, declare every matrix-scope
prior-art transcription XML consumer edge, bind zero or more distinct candidates to each exact unit
or phrase and to their exact mapped obligations, author any neutral fragment-review allocation only
for exact unresolved obligations, and regenerate the map Markdown review view. Do not retain a
unit-state assertion, synthetic preamble roll-up, duplicate candidate/allocation signature, or
record that cannot close against its exact obligation state.

## 4. Inspect and generate the configured products

A preview is read-only and writes HTML to standard output:

```sh
uv --no-cache --offline run --locked --no-sync python -m navigator preview na-specification
uv --no-cache --offline run --locked --no-sync python -m navigator preview af-specification
uv --no-cache --offline run --locked --no-sync python -m navigator preview na-prior-art
uv --no-cache --offline run --locked --no-sync python -m navigator preview af-prior-art
```

Inspect each changed product visually, including independent candidate and passage movement,
forward and reverse navigation, obligation/allocation/no-candidate states, mode-specific scroll
owners, contextual-reader opening and exact-fragment focus, cautions and gates, disclosure figures,
keyboard focus, readable typography at 100%, 200% text resize, 200% page zoom, 320 CSS-pixel
reflow, the controlled text-spacing override, the no-JavaScript document order, and unclipped print
content. Confirm the on-load guide overlay, each dismissal route, and the persistent masthead
Guide reopen control; with JavaScript removed, confirm the in-document guide section. Ordinary prose must wrap within the controlled measure without page-level horizontal
scrolling; only tables, code, and intrinsically two-dimensional figures may own scoped horizontal
overflow. In each specification product,
confirm that every recorded candidate endpoint remains concurrently indicated as selected,
selected-candidate context, or alternate-candidate passage; in each prior-art product, confirm that
only the selected candidate's passages receive forward emphasis. Treat visibility-policy leakage
between product kinds as a stop condition. Registered browser tests execute all four products at
the exact baseline, enlargement, reflow, spacing, no-JavaScript, and print vectors in
`navigator/policy/browser.json`, including ordinary and reduced motion where applicable. Visual
inspection remains useful substantive and product review, not a stored authorization step.

Regenerate every product in the current bundle inventory so shared-input drift cannot remain
hidden:

```sh
uv --no-cache --offline run --locked --no-sync python -m navigator candidate na-specification
uv --no-cache --offline run --locked --no-sync python -m navigator candidate af-specification
uv --no-cache --offline run --locked --no-sync python -m navigator candidate na-prior-art
uv --no-cache --offline run --locked --no-sync python -m navigator candidate af-prior-art
```

Stop if any product reads another product's private input, any semantic source bypasses the XML
gateway, a relation or wording entry is unused or unresolved, or regeneration is not byte-stable.
Every shared renderer, browser-control, interaction, wording, or acceptance change requires all
four candidates, all four sealed products and checksums, and the bundle to be regenerated.

## 5. Seal and bundle

Release reproduces the requested product through one fresh product-set worker before replacing
only its generated product and detached checksum:

```sh
uv --no-cache --offline run --locked --no-sync python -m navigator release na-specification
uv --no-cache --offline run --locked --no-sync python -m navigator release af-specification
uv --no-cache --offline run --locked --no-sync python -m navigator release na-prior-art
uv --no-cache --offline run --locked --no-sync python -m navigator release af-prior-art
uv --no-cache --offline run --locked --no-sync python -m navigator bundle
```

The bundle must contain one sealed HTML and corresponding detached-checksum pair for every current
configured product, in configured order, followed by `MANIFEST.txt`. Its own detached checksum
stays beside the ZIP. The ZIP is only a delivery product. `navigator/dist/` contains exactly the
configured candidates, sealed HTML/checksum pairs, bundle, and bundle checksum; a missing or
additional product fails aggregate validation.

## 6. Final worktree validation

Inspect the complete current package, regenerate every affected product, and run:

```sh
uv --no-cache --offline run --locked --no-sync python -m navigator validate-current
```

The command evaluates governed files solely from their current retained bytes, including relevant
untracked files. Repository status, index state, commit identity, and history remain outside the
result. It uses one closed exclusion policy, fails an unknown or unclassified artifact, performs
every validation read from retained bytes or their isolated materialization, and fails if the final
recapture adds, removes, replaces, renames, mode-changes, or byte-changes a governed file.

Stop on every skip, unknown criterion, validation failure, stale product, undeclared read or
write, failed test, source-manifest mismatch, retained-Markdown render failure, or worktree
mutation. A pass is ephemeral technical status for independent inventor and counsel review. Human
review of the source evidence and substantive analysis remains authoritative.

## 7. Failure handling

- Treat a failed command as a stop condition. Correct the declared source and rerun the affected
  generation steps; do not weaken a validator.
- Treat contract-pair, acceptance-registry, implementation-census, workflow, test, control, or
  stored-product disagreement as a pre-publication stop condition.
- Never repair generated HTML, checksums, the manifest, or ZIP by hand.
- Never repair semantic content in the typed model or renderer. Correct its owning XML or the
  package authority and regenerate.
- If source content changes after candidate generation, regenerate candidates, releases, and the
  bundle before aggregate validation.
- If any governed path, mode, or byte changes after validation, rerun `validate-current`; the
  earlier ephemeral result does not apply to the changed worktree.
