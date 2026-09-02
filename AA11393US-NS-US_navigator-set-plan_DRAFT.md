# AA11393US — National-Stage Filed Edition (NS) Navigator Set: Feasibility and Build Plan (DRAFT)

> **INTERNAL COUNSEL-REVIEW MATERIAL — NOT FOR FILING.**
> Repository status date: **3 September 2026**. This plan records the feasibility of generating a
> claims-to-specification and claims-to-prior-art navigator set for the actually deposited U.S.
> national-stage application 19/616,060 (filed claims 19–38; independents 19, 30, 33, 35), and the
> required build basis. **Option B is the owner's selected and required execution: both navigators
> in one pass with a fresh prior-art assessment.** Under the repository's
> no-auxiliary-release-plan rule, this draft informs the build and is removed once the artifacts
> exist; it is not a permanent retained document.

Complete execution is defined by the coupled
[`acceptance criteria`](AA11393US-NS-US_navigator-set-acceptance_DRAFT.md). The acceptance document
is temporary implementation input and is removed with this plan after its operative criteria have
been incorporated into the controlling contracts and machine-readable registries.

## 1. Request

Generate a new artifact set like the AF navigator set in [`navigator/dist/`](navigator/dist/) —
claims–spec HTML, claims–prior-art HTML, each with detached `.sha256`, and the configured delivery
bundle — focused on the actual deposited U.S. application rather than a strategy variant.

## 2. Vocabulary and authority model

- **NS is a filed-edition scope, not a strategy.** The strategy classifier remains `NA`/`AF`/
  `AF-CONT`. NS denotes the actual submitted claim edition of application 19/616,060 and is
  introduced in [`GLOSSARY.md`](GLOSSARY.md) and the [`README.md`](README.md) taxonomy as a
  distinct classifier. Outside claim text, cite **“filed claim 19”** (application 19/616,060); no
  conclusion transfers between filed claims and `NA`/`AF`/`AF-CONT` claim numbers.
- **The filed PDF is the only authority for the submitted claim text.** The authoritative evidence
  is the filed preliminary amendment
  [`from-US-Counsel/260818-19616060/03-P3366-US-2026-08-17-Prelim-Amnd-TBF.pdf`](from-US-Counsel/260818-19616060/03-P3366-US-2026-08-17-Prelim-Amnd-TBF.pdf).
  Its [Markdown review copy](from-US-Counsel/260818-19616060/03-P3366-US-2026-08-17-Prelim-Amnd-TBF.md)
  is a verified review transcription, not authority. Any registered claim representation is
  **declared derivative** under a PDF-governed transcription scheme (the
  `pdf-evidence-transcription-v1` direction used by `pct-as-filed-dossier`, or a closed sibling
  profile) — never `authored-markdown-v1`, which is reserved for applicant-authored strategy
  candidates.

## 3. Feasibility

**Verdict: technically feasible; the pipeline supports edition-blind products, but a PDF-derived
filed-claim edition is a contract-system change, not a registry-only addition.**

The navigator pipeline is edition-blind. Each existing edition (af/na × specification/prior-art) is
determined by the inputs below; the delta for NS is stated per input.

| Input | AF template | NS delta |
|---|---|---|
| Claim package | [`US/allowance-first/parent/claims/AA11393US-AF-US_claim-set_DRAFT.md`](US/allowance-first/parent/claims/AA11393US-AF-US_claim-set_DRAFT.md) (`authored-markdown-v1`) | **New authority direction for the subject input.** A PDF-governed filed-claim transcription package: filed prelim-amendment PDF as authority, derivative XML/Markdown representations. Not a re-use of the strategy claim-set scheme. |
| Claims→spec relations XML | [`navigator/relations/af__pct.relations.xml`](navigator/relations/af__pct.relations.xml) (1,249 lines) | New `ns__pct.relations.xml`: **passage identification only** — filed claim text ↔ PCT-as-filed passages. Written-description, enablement, priority, and new-matter conclusions are excluded and remain in the substantive review artifacts (DW-05A). Every filed claim re-mapped; the AF topology does not carry (see § 4). |
| Claims→prior-art passage map | [`US/allowance-first/parent/prior-art-analysis/AA11393US-AF-claim-prior-art-passage-map_DRAFT.relations.xml`](US/allowance-first/parent/prior-art-analysis/AA11393US-AF-claim-prior-art-passage-map_DRAFT.relations.xml) (2,630 lines) | **Fresh passage-level assessment** for the 33 registered art packages (A1–A21, B1–B10, C3, C8) against filed claims 19–38. No AF transfer. |
| Claims→prior-art comparison matrix | [`US/allowance-first/parent/prior-art-analysis/AA11393US-AF-prior-art-comparison-matrix_DRAFT.relations.xml`](US/allowance-first/parent/prior-art-analysis/AA11393US-AF-prior-art-comparison-matrix_DRAFT.relations.xml) (963 lines) | **Fresh claim-by-claim scoring**, version-locked to the filed-claim edition. |
| Wording XML | [`navigator/wording/af.wording.xml`](navigator/wording/af.wording.xml) | New `ns.wording.xml`; group/label wording for the filed-edition topology. |
| Edition JSONs | [`navigator/editions/af-specification.json`](navigator/editions/af-specification.json), [`navigator/editions/af-prior-art.json`](navigator/editions/af-prior-art.json) | Two new editions (`ns-specification`, `ns-prior-art`); census/units computed at build. |
| Contract and product system | [`contracts/`](contracts/) pairs, [`structured_source/registry/content.json`](structured_source/registry/content.json), acceptance registries, `navigator/bundles/current.json` | **One indivisible change:** authority contract, technical descriptions, data-only acceptance registries, configuration, implementation, tests and vectors, generated representations, sealed products, and the delivery bundle are updated together. No documentation-only, registry-only, or product-only state. |
| Products | `navigator/dist/*.html` + `.sha256` + delivery ZIP per [`navigator/RUNBOOK-content-sync-and-regeneration.md`](navigator/RUNBOOK-content-sync-and-regeneration.md) | Both NS HTML/checksum pairs **and** the regenerated delivery bundle: one exact reproducible set, candidate/release byte-for-byte; [`validate.sh`](validate.sh) must pass. |

## 4. Substantive constraints

- **Filed-claim topology.** Independents are 19, 30, 33, and 35. Claim 34 depends from claim 33
  (segmented-Tardos species). The multi-recipient probabilistic-fingerprinting family sits at
  independent claim 33 with dependent 34, where `AF-2026-07-30-v7` carries that family in dependent
  form; the set is renumbered 19–38 with a different independence structure than AF (1/17/20).
  Scores and mappings from any strategy version do not transfer.
- **IDS arithmetic.** The filed Form PTO-1449 discloses 34 items
  ([review copy](from-US-Counsel/260818-19616060/06-P3366-US-2026-08-17-IDS-Transmittal-1449.md)):
  the 33 substantive art packages (A1–A21 U.S. patent documents, B1–B10 foreign patent documents,
  C3 Tardos STOC 2003, C8 ETSI TS 104 002) plus the ISR/Written Opinion for PCT/IB2025/051755,
  which is a prosecution record, not an art package. The prior-art navigator covers the 33 art
  packages only.
- **Open substantive gates.** The written DW-05A claim-as-a-whole support/priority analysis and the
  DW-08A professional search remain open for the filed claims per the
  [filing-controls memo](US/common/filing-controls/AA11393US-deferred-filing-disclosure-and-EP-work_MEMO.md);
  the navigators do not close them.

## 5. Required Option B build basis

1. Register the filed-claim evidence package: filed prelim-amendment PDF as authority, derivative
   claim transcription XML and Markdown review view under a PDF-governed scheme; declare the
   consumer handoff.
2. Introduce the NS filed-edition scope in [`GLOSSARY.md`](GLOSSARY.md) and the
   [`README.md`](README.md) taxonomy as a classifier distinct from the strategy IDs.
3. Author `navigator/relations/ns__pct.relations.xml` (passage identification, § 3 language
   limits), `navigator/wording/ns.wording.xml`, and `navigator/editions/ns-specification.json`.
4. Author the fresh NS passage map and comparison matrix for the 33 art packages; add
   `navigator/editions/ns-prior-art.json`.
5. Update the contract pairs, data-only acceptance registries (regenerate Markdown table regions;
   never hand-edit generated rows), configuration, implementation, tests and vectors, and
   `navigator/bundles/current.json` in one coherent state.
6. Run the pipeline per the runbook; produce both NS HTML/checksum pairs and the regenerated
   delivery bundle; verify candidate/release byte-for-byte identity.
7. Run [`./validate.sh`](validate.sh) to green; leave all changes unstaged and report the validated
   change scope (the owner manages the Git index and history).
8. Remove this draft once the artifacts exist.

## 6. Execution decision

**Option B is required.** Complete execution delivers both editions in one pass, including fresh
claim-by-claim assessment of the 33 art packages against filed claims 19–38 and no provisional or
transferred content.

Option A is not an accepted delivery because a specification-only milestone omits the requested
prior-art product. Option C is prohibited because AF scores must not transfer, even provisionally:
the wording and topology changed enough to require a fresh claim-by-claim assessment, and a matrix
is valid only for the claim-set version named in its header.
