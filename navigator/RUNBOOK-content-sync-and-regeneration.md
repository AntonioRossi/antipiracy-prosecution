# Content Integration and Navigator Regeneration Runbook

> **CURRENT OPERATING PROCEDURE · INTERNAL COUNSEL-REVIEW SYSTEM**

This runbook applies the normative update contract in
[`../AA11393US-claims-navigator_technical-description_DRAFT.md`](../AA11393US-claims-navigator_technical-description_DRAFT.md),
especially §§10, 13, and 14. The technical description controls every conflict. This
runbook supplies commands and stop conditions; it creates no exception, authorization, or
alternative release path.

## 1. Invariants

- Registered authority sources, generated representations, and `navigator/` are regular files in
  one repository checkout.
- Integration uses an exact Git commit, recorded as a merge parent.
- Symlinks, external content roots, mutable cross-worktree reads, unrecorded copying, and
  implicit version upgrades are forbidden.
- The working tree is clean before integration and before release.
- `migrate` classifies current-schema content drift. It never approves a mapping or accepts
  an obsolete schema or canon version.
- Navigator-specific reviewed-owner and verification controls apply only to navigator release
  authorization. They do not approve structured-source content or alter a package's authority.
- The active release profile is selected before evidence is created. Profile labels and
  requirements are not interchangeable.
- The live navigator verification store equals the exact active reachable record graph. Every
  record is full-digest-addressed, canonical, and immutable while present; Git alone retains
  displaced records and retired formats.

## 2. Baseline gate

From the navigator integration checkout:

```sh
git status --short --branch
git rev-parse HEAD
git rev-parse <source-commit>
git merge-base HEAD <source-commit>
```

Stop if the worktree is not clean, either commit is unresolved, or the selected source
commit has not passed the repository's document-integrity review. Record both exact SHAs in
the merge commit through Git ancestry; do not substitute a moving branch name after review.

## 3. Integration gate

```sh
git merge --no-ff <source-commit>
git diff --name-status HEAD^1..HEAD
```

Inspect every imported path. Stop on an unexpected source, deletion, generated artifact, or
canonical authority-file change. A conflict-free merge proves only text integration; the
navigator is expected to reject stale pins and mappings until the remaining gates pass.

## 4. Pin and parameter plan

Generate the read-only plans:

```sh
python3 navigator/build.py pin-plan na
python3 navigator/build.py pin-plan af
```

Apply the reported current versions and raw-byte digests to the edition-selected corpus and
QA registries. The plan's `corpora` map covers every corpus the edition depends on — the
claim corpus, the target corpus (every pinned disclosure file), the authority corpus, and
each QA source named by `qaSources` — keyed by corpus id. For every corpus closure, inspect
every sorted entry in `files`, not only the entry marked `primary`. If any `pinCurrent` is
false, use that entry's `actualDigest` as the replacement pin for its exact path. For QA
corpora, require `configuredVersions` to equal `expectedVersions` exactly; for registry
corpora, require the version label current, with the plan's document, corpus, and edition
versions in agreement. A missing auxiliary entry, a free-form version label, or
a version binding not equal to the selected current claim version is a stop condition.
Update the edition census, independent claims, groups, artifact name, release timestamp,
dependency map, segmentation policy, gates, fixtures, bundle wording, and every other
reported exact-set dependency. Do not calculate a digest through an alternate helper or edit
generated output.

Run `pin-plan` again. Stop unless it reports that every proposed version, digest, census,
group, dependency, and artifact-name value is already represented by the current sources or
explicitly lists the remaining authored work.

## 5. Migration and review gate

For each edition:

```sh
python3 navigator/build.py candidate <edition>
python3 navigator/build.py migrate <edition>
```

Inspect the complete migration diagnostic. Resolve every `stale` and `pending` owner by
reviewing the current claim text, dependency context, PCT target, gate source, disposition,
and prior target snapshot. New owners begin with no candidate passage recorded. Automatic
target inheritance and cross-edition copying are forbidden.

After resolving the authored data, stamp only the owners actually reviewed:

```sh
python3 navigator/tools/stamp.py navigator/editions/<edition>.json \
  --mark-reviewed \
  --owner=<type>:<key> \
  --reviewer="<identified-operator>" \
  --review-date=YYYY-MM-DD \
  --operator-kind=<human|model>
```

`--all-owners` is permitted only after the operator has inspected every owner projection.
Then require a clean candidate:

```sh
python3 navigator/build.py candidate <edition>
```

Stop on any stale pin, exact-set mismatch, missing disposition, unreviewed owner, schema
error, forbidden term, dependency disagreement, or undeclared input.

## 6. Verification and release gate

Declare the navigator operator for commands that publish current verification evidence:

```sh
export NAV_OPERATOR="<identified-operator>"
export NAV_OPERATOR_KIND="<human|model>"
```

Create fresh exact-side inventory and QA-source attestations for each edition. AF also
requires the crosswalk attestation. Refresh global wording approvals only when their exact
sides changed. The technical-preview profile creates no QA record; validated-release
requires the complete current structured QA record before release.

```sh
python3 navigator/build.py release na --profile=<active-profile>
python3 navigator/build.py release af --profile=<active-profile>
python3 navigator/build.py bundle-plan
```

Inspect and apply the exact canonical `bundle-plan` proposal as an authored config edit, then:

```sh
python3 navigator/build.py bundle
```

No attestation, QA record, release record, bundle record, filename, or checksum may be relabelled
or reused for new bytes. Each writer validates the complete new record before replacing any record
in the same logical scope. Current authorization is resolved from exact profile and predecessor
bindings, never recency or directory ordering. `bundle` retains exactly one selected bundle
record, the releases pinned by the active config, only their profile-required QA records, their
exact attestation predecessors, and the separately pinned manifest approval. Git alone retains
displaced records.

## 7. Current-state and cutover gate

Remove non-current files from `navigator/dist/`. Require `navigator/records/` to equal the exact
active reachable graph produced by the current bundle. Remove transient browser snapshots, caches,
migration scratch data, and every unclassified tracked file.

```sh
git status --short --branch
uv --no-cache --offline run --locked --no-sync python -m navigator validate-current
```

`validate-current` is the canonical cutover gate. It must report one coherent current
baseline, current candidates and sealed artifacts, a current configured bundle and
authorization chain, no obsolete live version, no compatibility path, and no unclassified
file. It captures the complete live repository, proves the full closure against the
captured bytes, runs the document-integrity legs (the current changed-Markdown render check and
the co-located prior-art source-manifest checks) and both registered test families only in a
materialized snapshot,
rejects mutation of that snapshot or
the live tree, re-derives the full live closure, and compares a final snapshot immediately
before reporting success. Run it last; stop on any warning or nonzero result. The audit unit is
that exact clean commit and checkout with supplied Git history, the controlling documentation and
executable registries, and this current result; no detached export or stored receipt substitutes
for execution.

When the selected source branch has not advanced, integrate the accepted navigator branch
with a fast-forward-only merge. If it has advanced, merge the new exact source commit into
the integration branch and repeat every affected gate. Remove the additional worktree only
after the final branch contains all current sources, artifacts, checksums, and required
evidence.

## 8. Recovery

- Before an integration commit exists, abort an unsuccessful merge with `git merge --abort`.
- After a merge commit exists, correct forward on the integration branch; do not rewrite or
  disguise reviewed history.
- A failed `candidate`, `validate-current`, release, or bundle command is a stop condition, not
  permission to bypass a validator.
- Never edit a verification record in place. Correct the inputs and publish a new fully validated
  digest-addressed record in the same logical scope; the writer displaces the prior record only
  after validation. The final bundle prunes everything outside the validated active graph. Git
  alone preserves displaced, defective, or retired-format records.
- Restore no artifact manually. Reproduce it through the current pipeline after correcting
  its declared inputs.
