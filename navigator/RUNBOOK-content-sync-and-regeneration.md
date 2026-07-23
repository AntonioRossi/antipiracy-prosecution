# Content Integration and Navigator Regeneration Runbook

> **CURRENT OPERATING PROCEDURE · INTERNAL COUNSEL-REVIEW SYSTEM**

This runbook applies the normative update contract in
[`../AA11393US-claims-navigator_technical-description_DRAFT.md`](../AA11393US-claims-navigator_technical-description_DRAFT.md),
especially §§10, 13, and 14. The technical description controls every conflict. This
runbook supplies commands and stop conditions; it creates no exception, authorization, or
alternative release path.

## 1. Invariants

- The claim sources and `navigator/` are regular files in one repository checkout.
- Integration uses an exact Git commit, recorded as a merge parent.
- Symlinks, external content roots, mutable cross-worktree reads, unrecorded copying, and
  implicit version upgrades are forbidden.
- The working tree is clean before integration and before release.
- `migrate` classifies current-schema content drift. It never approves a mapping or accepts
  an obsolete schema or canon version.
- Only an identified human or model operator may approve reviewed owners or verification
  evidence. Tool output is evidence, never authority.
- The active release profile is selected before evidence is created. Profile labels and
  requirements are not interchangeable.
- The live verification store contains only the current record format. Superseded records
  using that format remain append-only; Git alone retains records from retired formats.

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
QA registries. Update the edition census, independent claims, groups, artifact name, release
timestamp, dependency map, segmentation policy, gates, fixtures, bundle wording, and every
other reported exact-set dependency. Do not calculate a digest through an alternate helper
or edit generated output.

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

Declare the approving operator for commands that append verification evidence:

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

No old attestation, QA record, release record, bundle record, filename, or checksum may be
relabelled or reused for new bytes.

## 7. Current-state and cutover gate

Remove superseded files from `navigator/dist/`; append-only same-schema records remain only
as non-current evidence. Remove transient browser snapshots, caches, migration scratch data,
and every unclassified tracked file.

```sh
python3 navigator/build.py verify-current
python3 navigator/tools/pre-commit-check.sh
python3 -m unittest discover -s navigator/tests -p 'test_*.py'
git diff --check
git status --short --branch
```

`verify-current` must report one coherent current baseline, current candidates and sealed
artifacts, a current configured bundle and authorization chain, no obsolete live version,
no compatibility path, and no unclassified file. Stop on any warning or nonzero result.

When the selected source branch has not advanced, integrate the accepted navigator branch
with a fast-forward-only merge. If it has advanced, merge the new exact source commit into
the integration branch and repeat every affected gate. Remove the additional worktree only
after the final branch contains all current sources, artifacts, checksums, and required
evidence.

## 8. Recovery

- Before an integration commit exists, abort an unsuccessful merge with `git merge --abort`.
- After a merge commit exists, correct forward on the integration branch; do not rewrite or
  disguise reviewed history.
- A failed `candidate`, `verify-current`, release, or bundle command is a stop condition, not
  permission to bypass a validator.
- Within the current format, verification records are append-only. A defective or
  superseded record is left non-current and replaced with a new digest-addressed record; it
  is never edited in place. An intentional schema-breaking refactor removes retired-format
  records from the live store without rewriting or relabelling them; Git preserves them.
- Restore no artifact manually. Reproduce it through the current pipeline after correcting
  its declared inputs.
