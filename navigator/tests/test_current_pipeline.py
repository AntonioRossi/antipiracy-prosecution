"""Small end-to-end contracts for the sole current navigator pipeline."""

from __future__ import annotations

import os
import inspect
import io
import stat
import tempfile
import unittest
from types import MappingProxyType
from unittest import mock

from navigator import build
from navigator.lib import (
    acceptance, bundlezip, canon, currentstate, release, schema_validate,
)
from structured_source import __main__ as structured_source_main


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))


def _json(relative):
    with open(os.path.join(ROOT, *relative.split("/")), "rb") as handle:
        return canon.parse_json(handle.read())


class CurrentPipelineTests(unittest.TestCase):
    def _lightweight_validation(self, root, during_closure=None):
        closure = {
            "acceptanceRegistry": object(),
            "bundle": {"name": "bundle.zip"},
            "editions": {},
            "structuredSource": {
                "domains": [],
                "results": [],
                "status": "passed",
                "technicalValidationResultVersion": "1",
            },
            "testSession": MappingProxyType({}),
        }
        modules = [
            {"count": 1, "module": module}
            for module in sorted(acceptance.TEST_COVERAGE)
        ]

        def validate(frozen, reproduction_root):
            self.assertFalse(os.path.exists(os.path.join(
                reproduction_root, ".git")))
            frozen.validate_retained()
            if during_closure is not None:
                during_closure(frozen)
            return closure

        with mock.patch.object(currentstate, "ROOT", root), \
                mock.patch.object(
                    currentstate, "_snapshot_whitespace_problems",
                    return_value=[]), \
                mock.patch.object(
                    currentstate, "_contract_preflight_problems",
                    return_value=[]), \
                mock.patch.object(
                    currentstate, "_snapshot_markdown_problems",
                    return_value=[]), \
                mock.patch.object(
                    currentstate, "verify_current_closure",
                    side_effect=validate), \
                mock.patch.object(
                    currentstate, "_run_discovered_tests",
                    side_effect=(
                        {"count": 1, "modules": [{
                            "count": 1,
                            "module": currentstate.PREFLIGHT_TEST_MODULES[0],
                        }], "status": "passed"},
                        {"count": len(modules), "modules": modules,
                         "status": "passed"},
                    )), \
                mock.patch.object(
                    currentstate.acceptance, "passed_result",
                    return_value={"status": "passed"}):
            frozen = currentstate.snapshot.RepositorySnapshot.capture(
                root, retain_bytes=True)
            with tempfile.TemporaryDirectory() as sandbox_root:
                frozen.materialize(sandbox_root)
                return currentstate._validate_captured_worktree(
                    frozen, sandbox_root)

    def test_live_navigator_input_inventory_is_exact(self):
        class Entry:
            def __init__(self, path):
                self.path = path

        class Snapshot:
            def __init__(self, paths):
                self.entries = tuple(Entry(path) for path in paths)

        expected = currentstate.NAVIGATOR_FIXED_INPUT_PATHS | {
            "navigator/editions/na.json",
            "navigator/relations/na__pct.relations.xml",
            "navigator/wording/na.wording.xml",
        }
        plan = currentstate.ProductPlan(
            snapshot_digest="sha256/test", bundle_config=MappingProxyType({}),
            editions=(), by_id=MappingProxyType({}),
            input_paths=frozenset(expected))
        currentstate._verify_navigator_input_inventory(Snapshot(expected), plan)
        for paths in (
                expected - {"navigator/wording/na.wording.xml"},
                expected | {
                    "navigator/relations/copy.relations.xml"}):
            with self.subTest(paths=paths), \
                    self.assertRaises(currentstate.CurrentStateError):
                currentstate._verify_navigator_input_inventory(
                    Snapshot(paths), plan)

    def test_product_plan_is_derived_from_an_arbitrary_edition_inventory(self):
        editions = ("alpha", "beta", "gamma")
        timestamp = "2026-07-28T00:00:00Z"
        with tempfile.TemporaryDirectory() as root:
            for path in ("navigator/bundles", "navigator/editions",
                         "navigator/schema"):
                os.makedirs(os.path.join(root, *path.split("/")))
            with open(os.path.join(ROOT, "navigator", "schema",
                                   "edition.schema.json"), "rb") as handle:
                schema_bytes = handle.read()
            with open(os.path.join(root, "navigator", "schema",
                                   "edition.schema.json"), "wb") as handle:
                handle.write(schema_bytes)
            members = []
            for edition in editions:
                prefix = edition.upper()
                version = prefix + "-2026-07-27-v1"
                artifact = ("AA11393US-%s-claims-spec-navigator_%s.html" %
                            (prefix, version))
                members.extend((
                    {"edition": edition, "kind": "sealed",
                     "name": artifact},
                    {"artifact": artifact, "edition": edition,
                     "kind": "artifact-checksum",
                     "name": artifact + ".sha256"},
                ))
                control = {
                    "artifactName": artifact,
                    "census": {"claims": 1, "units": 1},
                    "claimPackageId": (
                        "aa11393us-%s-us-claim-set" % edition),
                    "claimSetVersion": version,
                    "consumerId": "navigator-" + edition,
                    "declaredReleaseTimestamp": timestamp,
                    "displayName": edition + " edition",
                    "editionId": edition,
                    "editionVersion": "2",
                    "editionWordingPath": (
                        "navigator/wording/%s.wording.xml" % edition),
                    "groups": ["Current group"],
                    "independentClaims": [1],
                    "relationPath": (
                        "navigator/relations/%s__pct.relations.xml" % edition),
                    "strategyName": edition + " strategy",
                    "strategyPrefix": prefix,
                }
                with open(os.path.join(root, "navigator", "editions",
                                       edition + ".json"), "wb") as handle:
                    handle.write(canon.canonical_json(control) + b"\n")
            members.append({"kind": "manifest", "name": "MANIFEST.txt"})
            config = {
                "bundleVersion": bundlezip.BUNDLE_VERSION,
                "declaredTimestamp": timestamp,
                "editions": list(editions),
                "manifestWordingId": bundlezip.BUNDLE_WORDING_ID,
                "members": members,
                "name": ("AA11393US-claims-navigators_%s_"
                         "TECHNICAL-PREVIEW.zip" % "_".join(
                             item.upper() + "-2026-07-27-v1"
                             for item in editions)),
            }
            bundle_path = os.path.join(
                root, *bundlezip.BUNDLE_CONFIG_PATH.split("/"))
            with open(bundle_path, "wb") as handle:
                handle.write(canon.canonical_json(config) + b"\n")
            frozen = currentstate.snapshot.RepositorySnapshot.capture(
                root, retain_bytes=True)
            with mock.patch.object(currentstate, "ROOT", root):
                plan = currentstate.load_product_plan(frozen)
            self.assertEqual(plan.edition_ids, editions)
            self.assertEqual(
                plan.consumer_ids,
                tuple("navigator-" + item for item in editions))
            self.assertTrue(all(
                "navigator/editions/%s.json" % item in plan.input_paths
                for item in editions))

    def test_command_boundary_is_exact_and_legacy_commands_are_rejected(self):
        self.assertEqual(build.COMMANDS, (
            "preview", "candidate", "release", "bundle",
            "validate-current"))
        self.assertEqual(set(build.USAGE), set(build.COMMANDS))
        for command in (
                "approve", "attest", "callback", "migrate", "pin",
                "plan", "qa", "record", "verify-release"):
            with self.subTest(command=command), \
                    self.assertRaises(build.CommandError):
                build._dispatch([command])
        with self.assertRaises(build.CommandError):
            build._dispatch(["preview", "na", "--callback"])
        self.assertEqual(structured_source_main.COMMANDS, (
            "check", "regenerate", "regenerate-controls"))
        self.assertNotIn("verify-current", structured_source_main.COMMANDS)

    def test_root_validation_launcher_is_exact_and_executable(self):
        path = os.path.join(ROOT, "validate.sh")
        with open(path, "rb") as handle:
            actual = handle.read()
        expected = b"""#!/usr/bin/env bash

set -euo pipefail

if (( $# != 0 )); then
    printf 'Usage: %s\\n' "${0##*/}" >&2
    exit 64
fi

readonly repository_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
cd -- "$repository_root"

exec uv --no-cache --offline run --locked --no-sync \\
    python -m navigator validate-current
"""
        self.assertEqual(actual, expected)
        self.assertEqual(stat.S_IMODE(os.stat(path).st_mode), 0o755)

    def test_aggregate_failure_is_ordinary_ephemeral_technical_status(self):
        stream = type("CapturedStderr", (), {"buffer": io.BytesIO()})()
        with mock.patch.object(
                build, "_dispatch",
                side_effect=currentstate.CurrentStateError("broken link")), \
                mock.patch.object(build.sys, "stderr", stream):
            exit_status = build.main(["validate-current"])
        result = canon.parse_json(stream.buffer.getvalue())
        self.assertEqual(exit_status, 1)
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["validationResultVersion"], "4")
        self.assertEqual(result["purpose"], currentstate.VALIDATION_PURPOSE)
        self.assertEqual(result["nonProofBoundary"],
                         list(currentstate.NON_PROOF_BOUNDARY))
        self.assertEqual(
            set(("phase", "checkId", "subject", "expected", "actual",
                 "remediation")),
            set(result) & {"phase", "checkId", "subject", "expected",
                           "actual", "remediation"})
        self.assertEqual(result["checkId"], "unclassifiedFailure")
        self.assertNotIn("repositorySnapshot", result)

    def test_validation_ignores_repository_metadata_and_uses_current_bytes(self):
        with tempfile.TemporaryDirectory() as root:
            with open(os.path.join(root, "governed.txt"), "wb") as handle:
                handle.write(b"dirty current bytes\n")
            os.mkdir(os.path.join(root, ".git"))
            with open(os.path.join(root, ".git", "index"), "wb") as handle:
                handle.write(b"staged-state-one")
            captured = []

            def inspect_capture(frozen):
                captured.append(frozen.read_bytes("governed.txt"))

            with mock.patch.object(
                    currentstate.subprocess, "run",
                    side_effect=AssertionError("repository command consulted")):
                first = self._lightweight_validation(root, inspect_capture)
            with open(os.path.join(root, ".git", "index"), "wb") as handle:
                handle.write(b"different staged and commit state")
            with mock.patch.object(
                    currentstate.subprocess, "run",
                    side_effect=AssertionError("repository command consulted")):
                second = self._lightweight_validation(root, inspect_capture)

        self.assertEqual(first, second)
        self.assertEqual(captured, [b"dirty current bytes\n"] * 2)
        self.assertEqual(first["status"], "passed")

    def test_public_gate_executes_only_the_materialized_capture_without_git(self):
        with tempfile.TemporaryDirectory() as root:
            with open(os.path.join(root, "governed.txt"), "wb") as handle:
                handle.write(b"captured current bytes\n")
            os.mkdir(os.path.join(root, ".git"))
            with open(os.path.join(root, ".git", "index"), "wb") as handle:
                handle.write(b"irrelevant repository state")
            expected = {"status": "passed"}

            def isolated(unused_command, *, cwd, **unused_kwargs):
                self.assertFalse(os.path.exists(os.path.join(cwd, ".git")))
                with open(os.path.join(cwd, "governed.txt"), "rb") as handle:
                    self.assertEqual(handle.read(), b"captured current bytes\n")
                return type("Completed", (), {
                    "returncode": 0,
                    "stderr": b"",
                    "stdout": canon.canonical_json(expected) + b"\n",
                })()

            with mock.patch.object(currentstate, "ROOT", root), \
                    mock.patch.object(
                        currentstate.subprocess, "run", side_effect=isolated):
                result = currentstate.validate_current_state()
        self.assertEqual(result, expected)

    def test_relevant_untracked_bytes_are_captured_and_materialized_without_git(self):
        with tempfile.TemporaryDirectory() as root:
            path = os.path.join(root, "untracked-current.txt")
            with open(path, "wb") as handle:
                handle.write(b"participates\n")
            observed = []

            def inspect_capture(frozen):
                observed.append((
                    "untracked-current.txt" in {
                        entry.path for entry in frozen.entries},
                    frozen.read_bytes("untracked-current.txt"),
                ))

            self._lightweight_validation(root, inspect_capture)
        self.assertEqual(observed, [(True, b"participates\n")])

    def test_worktree_exclusion_policy_is_one_exact_closed_set(self):
        self.assertEqual(currentstate.snapshot.EXCLUDED_DIRECTORY_NAMES,
                         frozenset({
                             ".agents", ".claude", ".codex", ".git",
                             ".uv-cache", ".venv", "__pycache__",
                         }))
        self.assertEqual(currentstate.snapshot.EXCLUDED_FILE_NAMES,
                         frozenset({".DS_Store"}))

    def test_captured_whitespace_policy_preserves_evidentiary_line_endings(self):
        self.assertEqual(currentstate._TRAILING_WHITESPACE_EXEMPT_SUFFIXES,
                         frozenset({".md"}))
        self.assertEqual(currentstate._TRAILING_WHITESPACE_EXEMPT_ROOTS,
                         ("PCT/office action pct/",))
        with tempfile.TemporaryDirectory() as root:
            os.makedirs(os.path.join(root, "PCT", "office action pct"))
            paths = {
                "evidence.md": b"faithful hard break  \n",
                "PCT/office action pct/extraction.txt": b"layout  \n",
                "control.py": b"invalid  \n",
            }
            for relative, data in paths.items():
                absolute = os.path.join(root, *relative.split("/"))
                with open(absolute, "wb") as handle:
                    handle.write(data)
            frozen = currentstate.snapshot.RepositorySnapshot.capture(
                root, retain_bytes=True)
        self.assertEqual(currentstate._snapshot_whitespace_problems(frozen), [
            "trailing whitespace: control.py:1",
        ])

    def test_captured_markdown_links_and_fragments_fail_closed(self):
        def problems(first):
            with tempfile.TemporaryDirectory() as root:
                with open(os.path.join(root, "first.md"), "wb") as handle:
                    handle.write(first)
                with open(os.path.join(root, "second.md"), "wb") as handle:
                    handle.write(b"# Exact target\n")
                frozen = currentstate.snapshot.RepositorySnapshot.capture(
                    root, retain_bytes=True)
                with mock.patch.object(currentstate, "ROOT", root):
                    serial = currentstate._snapshot_markdown_problems(
                        frozen, worker_count=1)
                    default = currentstate._snapshot_markdown_problems(frozen)
                    parallel = currentstate._snapshot_markdown_problems(
                        frozen, worker_count=3)
                    self.assertEqual(default, serial)
                    self.assertEqual(parallel, serial)
                    return parallel

        self.assertEqual(problems(b"[valid](second.md#exact-target)\n"), [])
        self.assertTrue(any("target is absent" in item for item in
                            problems(b"[missing](absent.md)\n")))
        self.assertTrue(any("fragment is absent" in item for item in
                            problems(b"[missing](second.md#absent)\n")))

    def test_contract_preflight_failure_starts_no_expensive_phase(self):
        with tempfile.TemporaryDirectory() as root:
            with open(os.path.join(root, "governed.txt"), "wb") as handle:
                handle.write(b"current\n")
            frozen = currentstate.snapshot.RepositorySnapshot.capture(
                root, retain_bytes=True)
            issue = currentstate.ValidationIssue(
                "contract-aggregate-reference", "contracts/example.md",
                "one shared link", "zero links", "restore the shared link")
            with mock.patch.object(
                    currentstate, "_snapshot_whitespace_problems",
                    return_value=[]), mock.patch.object(
                        currentstate, "_contract_preflight_problems",
                        return_value=[issue]), mock.patch.object(
                            currentstate, "_snapshot_markdown_problems") as markdown, \
                    mock.patch.object(
                        currentstate, "verify_current_closure") as closure, \
                    mock.patch.object(
                        currentstate, "_run_discovered_tests") as tests, \
                    self.assertRaisesRegex(
                        currentstate.CurrentStateError,
                        "phase=preflight.*contracts/example.md"):
                currentstate._validate_captured_worktree(frozen, root)
            markdown.assert_not_called()
            closure.assert_not_called()
            tests.assert_not_called()

    def test_focused_contract_test_failure_starts_no_expensive_phase(self):
        with tempfile.TemporaryDirectory() as root:
            with open(os.path.join(root, "governed.txt"), "wb") as handle:
                handle.write(b"current\n")
            frozen = currentstate.snapshot.RepositorySnapshot.capture(
                root, retain_bytes=True)
            failure = currentstate.CurrentStateError("focused contract failed")
            with mock.patch.object(
                    currentstate, "_snapshot_whitespace_problems",
                    return_value=[]), mock.patch.object(
                        currentstate, "_contract_preflight_problems",
                        return_value=[]), mock.patch.object(
                            currentstate, "_run_discovered_tests",
                            side_effect=failure) as tests, mock.patch.object(
                                currentstate,
                                "_snapshot_markdown_problems") as markdown, \
                    mock.patch.object(
                        currentstate, "verify_current_closure") as closure, \
                    self.assertRaisesRegex(
                        currentstate.CurrentStateError,
                        "phase=preflight.*focused contract failed"):
                currentstate._validate_captured_worktree(frozen, root)
            tests.assert_called_once_with(
                root, currentstate.PREFLIGHT_TEST_MODULES,
                verify_census=True)
            markdown.assert_not_called()
            closure.assert_not_called()

    def test_live_modification_addition_removal_and_mode_change_fail(self):
        def replace(unused_root, path):
            with open(path, "wb") as handle:
                handle.write(b"after\n")

        def add(root, unused_path):
            with open(os.path.join(root, "added.txt"), "wb") as handle:
                handle.write(b"added\n")

        def change_and_restore(unused_root, path):
            with open(path, "wb") as handle:
                handle.write(b"transient\n")
            with open(path, "wb") as handle:
                handle.write(b"before\n")

        def run_mutation(mutate):
            with tempfile.TemporaryDirectory() as root:
                path = os.path.join(root, "governed.txt")
                with open(path, "wb") as handle:
                    handle.write(b"before\n")

                def during(unused_frozen):
                    mutate(root, path)

                with self.assertRaisesRegex(
                        currentstate.CurrentStateError,
                        "worktree changed during validation"):
                    self._lightweight_validation(root, during)

        mutations = (
            replace,
            change_and_restore,
            add,
            lambda unused_root, path: os.unlink(path),
            lambda unused_root, path: os.chmod(path, 0o755),
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                run_mutation(mutation)

    def test_passing_result_states_technical_scope_and_complete_nonproof_boundary(self):
        with tempfile.TemporaryDirectory() as root:
            with open(os.path.join(root, "governed.txt"), "wb") as handle:
                handle.write(b"current\n")
            result = self._lightweight_validation(root)
        self.assertEqual(result["purpose"], currentstate.VALIDATION_PURPOSE)
        self.assertEqual(result["technicalScope"],
                         list(currentstate.TECHNICAL_SCOPE))
        self.assertEqual(result["nonProofBoundary"],
                         list(currentstate.NON_PROOF_BOUNDARY))
        self.assertEqual(result["humanReviewBoundary"],
                         currentstate.HUMAN_REVIEW_BOUNDARY)
        self.assertNotIn("repositorySnapshot", result["checks"])
        self.assertNotIn("gitCommit", result["checks"])

    def test_contracts_resolve_one_shared_current_validation_boundary(self):
        product_paths = (
            "contracts/30-product-generation/claims-navigator/technical-description_DRAFT.md",
            "contracts/30-product-generation/claims-navigator/acceptance-criteria_DRAFT.md",
        )
        start = "<!-- CURRENT-VALIDATION-BOUNDARY:START -->"
        end = "<!-- CURRENT-VALIDATION-BOUNDARY:END -->"
        regions = []
        for path in product_paths:
            with open(os.path.join(ROOT, *path.split("/")),
                      encoding="utf-8") as handle:
                text = handle.read()
            self.assertEqual((text.count(start), text.count(end)), (1, 1))
            regions.append(text.split(start, 1)[1].split(end, 1)[0])
            folded = text.casefold()
            for retired in (
                    "certified", "certification", "attested", "attestation",
                    "audit unit"):
                self.assertNotIn(retired, folded, path)
        with open(os.path.join(ROOT, *product_paths[0].split("/")),
                  encoding="utf-8") as handle:
            technical_contract = handle.read()
        self.assertIn(
            "form one indivisible current implementation",
            " ".join(technical_contract.split()))
        self.assertTrue(all(region == regions[0] for region in regions[1:]))
        normalized = " ".join(regions[0].split())
        for phrase in currentstate.NON_PROOF_BOUNDARY:
            self.assertIn(phrase, normalized)
        self.assertIn(
            "uv --no-cache --offline run --locked --no-sync "
            "python -m navigator validate-current", regions[0])
        frozen = currentstate.snapshot.RepositorySnapshot.capture(
            ROOT, retain_bytes=True)
        self.assertEqual(currentstate._contract_preflight_problems(frozen), [])

    def test_no_repository_command_or_retired_gate_wording_remains(self):
        implementation = inspect.getsource(currentstate)
        for token in (
                "git status", "git diff", "git ls-files", "git rev-parse",
                "clean HEAD", "audit unit"):
            self.assertNotIn(token, implementation)

        documents = (
            "AGENTS.md", "GLOSSARY.md", "README.md",
            "STRUCTURED-CONTENT-AUTHORITY-MANIFEST.md",
            "navigator/RUNBOOK-content-sync-and-regeneration.md",
        )
        for path in documents:
            with open(os.path.join(ROOT, *path.split("/")),
                      encoding="utf-8") as handle:
                text = handle.read().casefold()
            for retired in (
                    "audit unit", "exact clean git", "supplied history",
                    "git diff --check", "tracked markdown", "certifies"):
                self.assertNotIn(retired, text, path)

        with open(os.path.join(ROOT, "contracts", "README.md"),
                  encoding="utf-8") as handle:
            router = handle.read()
        self.assertIn("zero navigator consumer edges", router)
        self.assertIn(
            "exactly two structured-source XML handoffs per edition", router)
        self.assertNotIn("committed artifacts", router.casefold())

        with open(os.path.join(
                ROOT, "STRUCTURED-CONTENT-AUTHORITY-MANIFEST.md"),
                encoding="utf-8") as handle:
            authority_router = handle.read()
        self.assertNotIn("## Adoption", authority_router)
        self.assertNotIn("reusable architecture", authority_router.casefold())

    def test_one_source_pass_returns_same_context_frozen_handoffs(self):
        frozen = currentstate.snapshot.RepositorySnapshot(
            ROOT, (), "sha256/snapshot:test")
        handoff = MappingProxyType({
            "inputRepresentation": "xml", "dependencies": MappingProxyType({}),
        })
        raw_handoffs = MappingProxyType({
            "claim": handoff, "pct-as-filed-dossier": handoff,
        })
        public = {
            "technicalValidationResultVersion": "1",
            "snapshotDigest": frozen.digest,
            "status": "passed",
            "domains": [
                {"domain": "pdf-transcription",
                 "authorityScheme": "pdf-evidence-transcription-v1",
                 "status": "passed"},
                {"domain": "authored-markdown",
                 "authorityScheme": "authored-markdown-v1",
                 "status": "passed"},
                {"domain": "authored-relations",
                 "authorityScheme": "authored-relations-v1",
                 "status": "passed"},
            ],
        }
        corpus = type("Corpus", (), {
            "consumer_handoffs": MappingProxyType({
                "navigator-na": raw_handoffs}),
            "parser_controls": object(),
            "public_result": lambda unused_self: public,
        })()
        with mock.patch(
                "structured_source.verify.validate_corpus",
                return_value=corpus) as validate_once:
            result = currentstate.validate_structured_corpus(frozen)
        validate_once.assert_called_once()
        self.assertIs(result.corpus, corpus)
        self.assertIs(
            result.consumer_inputs["navigator-na"].handoffs, raw_handoffs)

        malformed = dict(public)
        malformed["domains"] = []
        malformed_corpus = type("MalformedCorpus", (), {
            "public_result": lambda unused_self: malformed,
        })()
        with mock.patch(
                "structured_source.verify.validate_corpus",
                return_value=malformed_corpus), self.assertRaisesRegex(
                    currentstate.CurrentStateError, "domain acceptance"):
            currentstate.validate_structured_corpus(frozen)

    def test_materialized_reproduction_constructs_each_boundary_once(self):
        request = currentstate.ReproductionRequest(("alpha", "beta"), True)
        frozen = object()
        plan = object()
        sources = object()
        projection = {"bundle": {}, "editions": {}}
        with mock.patch.object(
                currentstate.snapshot.RepositorySnapshot, "capture",
                return_value=frozen) as capture, mock.patch.object(
                    currentstate, "load_product_plan",
                    return_value=plan) as load_plan, mock.patch.object(
                        currentstate, "validate_structured_corpus",
                        return_value=sources) as validate_once, mock.patch.object(
                            currentstate, "derive_reproduction_projection",
                            return_value=projection) as derive_once:
            self.assertIs(currentstate.reproduce_materialized(request), projection)
        capture.assert_called_once_with(currentstate.ROOT, retain_bytes=True)
        load_plan.assert_called_once_with(frozen)
        validate_once.assert_called_once_with(frozen)
        derive_once.assert_called_once_with(frozen, plan, sources, request)

    def test_product_builders_have_no_implicit_validation_or_legacy_worker(self):
        required = (
            (currentstate.build_model, "consumer_input"),
            (currentstate.derive, "consumer_input"),
            (currentstate.derive_editions, "sources"),
            (currentstate.build_bundle_state, "states"),
            (currentstate.verify_stored_artifact_members, "bundle_state"),
        )
        for function, parameter in required:
            with self.subTest(function=function.__name__, parameter=parameter):
                self.assertIs(
                    inspect.signature(function).parameters[parameter].default,
                    inspect.Parameter.empty)
        self.assertFalse(hasattr(release, "fresh_candidate"))
        self.assertFalse(hasattr(currentstate, "_fresh_bundle_projection"))
        self.assertNotIn(
            "_artifact_bytes", inspect.getsource(currentstate.build_bundle_state))
        closure_source = inspect.getsource(currentstate.verify_current_closure)
        self.assertEqual(closure_source.count("fresh_pool.submit("), 1)
        self.assertLess(
            closure_source.index("fresh_pool.submit("),
            closure_source.index("validate_structured_corpus("))
        implementation_root = os.path.join(ROOT, "navigator", "lib")
        constructors = []
        for name in os.listdir(implementation_root):
            if not name.endswith(".py"):
                continue
            with open(os.path.join(implementation_root, name),
                      encoding="utf-8") as handle:
                if "VerificationContext(" in handle.read():
                    constructors.append(name)
        self.assertEqual(constructors, [])

    def test_acceptance_registry_names_outcomes_and_independent_enforcers(self):
        registry = acceptance.load_registry(ROOT)
        self.assertEqual(
            [item["id"] for item in registry["criteria"]],
            ["AC-%02d" % number for number in range(1, 21)])
        self.assertEqual(
            [item["scope"] for item in registry["criteria"]],
            ["edition"] * 18 + ["shared", "bundle"])
        self.assertTrue(all(set(item) == {
            "enforcer", "id", "outcome", "scope"}
                            for item in registry["criteria"]))

        for field in ("approval", "check", "evidence", "owner", "receipt"):
            changed = {
                "acceptanceVersion": registry["acceptanceVersion"],
                "criteria": [dict(item) for item in registry["criteria"]],
            }
            changed["criteria"][0][field] = "legacy-control"
            with self.subTest(field=field), \
                    self.assertRaises(acceptance.AcceptanceError):
                acceptance.validate_registry(changed)

        for enforcer in (
                "navigator.lib.currentstate.absent; "
                "navigator.tests.test_current_pipeline",
                "navigator.lib.currentstate.validate_current_state; "
                "navigator.tests.test_render_current"):
            changed = {
                "acceptanceVersion": registry["acceptanceVersion"],
                "criteria": [dict(item) for item in registry["criteria"]],
            }
            changed["criteria"][0]["enforcer"] = enforcer
            with self.subTest(enforcer=enforcer), \
                    self.assertRaises(acceptance.AcceptanceError):
                acceptance.validate_registry(changed)

        changed = {
            "acceptanceVersion": registry["acceptanceVersion"],
            "criteria": [dict(item) for item in registry["criteria"]],
        }
        changed["criteria"][8]["outcome"] = "Arbitrary untested outcome."
        changed_bytes = canon.canonical_json(changed) + b"\n"

        def mismatched_contract(absolute):
            if absolute.endswith(acceptance.ACCEPTANCE_PATH):
                return changed_bytes
            with open(absolute, "rb") as handle:
                return handle.read()

        with self.assertRaises(acceptance.AcceptanceError):
            acceptance.load_registry(ROOT, mismatched_contract)
        with self.assertRaises(acceptance.AcceptanceError):
            acceptance.passed_result(
                registry, tuple(sorted(acceptance.TEST_COVERAGE))[:-1])
        result = acceptance.passed_result(
            registry, tuple(sorted(acceptance.TEST_COVERAGE)))
        self.assertEqual(
            [item["id"] for item in result["results"]],
            list(acceptance.CRITERIA))

    def test_preview_derives_bytes_without_writing(self):
        source = object()

        class Frozen:
            @staticmethod
            def byte_source():
                return source

        frozen = Frozen()
        edition = currentstate.EditionSpec(
            edition_id="na", path="navigator/editions/na.json",
            consumer_id="navigator-na", claim_package_id="claim",
            relation_path="navigator/relations/na__pct.relations.xml",
            wording_path="navigator/wording/na.wording.xml",
            artifact_name="na.html", declared_timestamp="2026-01-01T00:00:00Z")
        plan = type("Plan", (), {"edition": lambda unused_self, unused_id: edition})()
        consumer_input = object()
        sources = type("Sources", (), {
            "input_for": lambda unused_self, unused_id: consumer_input})()
        with mock.patch.object(build, "_snapshot", return_value=frozen), \
                mock.patch.object(
                    build.currentstate, "validate_product_contract") \
                as contract, \
                mock.patch.object(
                    build.currentstate, "load_product_plan",
                    return_value=plan) as load_plan, \
                mock.patch.object(
                    build.currentstate, "validate_structured_corpus",
                    return_value=sources) as upstream, \
                mock.patch.object(
                    build.currentstate, "bind_sources_to_plan") as bind_sources, \
                mock.patch.object(
                    build.currentstate, "derive",
                    return_value=(object(), b"<html>preview</html>", {})) \
                as derive, \
                mock.patch.object(build, "_assert_unchanged") as unchanged, \
                mock.patch.object(build, "_assert_only_outputs_changed") \
                as output_check, \
                mock.patch.object(build.release, "write_outputs_atomic") \
                as write:
            result = build.cmd_preview("na")

        self.assertEqual(result, b"<html>preview</html>")
        contract.assert_called_once_with(frozen)
        load_plan.assert_called_once_with(frozen)
        upstream.assert_called_once_with(frozen)
        bind_sources.assert_called_once_with(plan, sources)
        derive.assert_called_once_with(
            edition, "preview", frozen, consumer_input)
        unchanged.assert_called_once_with(frozen, "preview")
        output_check.assert_not_called()
        write.assert_not_called()

    def test_product_contract_failure_makes_every_command_path_unreachable(self):
        failure = currentstate.CurrentStateError(
            "product contract pair differs")
        for command, arguments in (
                (build.cmd_preview, ("na",)),
                (build.cmd_candidate, ("na",)),
                (build.cmd_release, ("na",)),
                (build.cmd_bundle, ())):
            with self.subTest(command=command.__name__), \
                    mock.patch.object(build, "_snapshot", return_value=object()), \
                    mock.patch.object(
                        build.currentstate, "validate_product_contract",
                        side_effect=failure) as contract, \
                    mock.patch.object(
                        build.currentstate, "load_product_plan") as load_plan, \
                    mock.patch.object(
                        build.currentstate, "validate_structured_corpus") \
                    as validate_sources, \
                    mock.patch.object(
                        build.release, "write_outputs_atomic") as write:
                with self.assertRaisesRegex(
                        currentstate.CurrentStateError,
                        "product contract pair differs"):
                    command(*arguments)
            contract.assert_called_once()
            load_plan.assert_not_called()
            validate_sources.assert_not_called()
            write.assert_not_called()

    def test_generated_writes_are_atomic_generated_only_and_safe(self):
        with tempfile.TemporaryDirectory(
                prefix="aa11393-current-products-") as directory:
            outputs = {"b.html": b"second", "a.html": b"first"}
            written = release.write_outputs_atomic(directory, outputs)
            self.assertEqual(
                [item["name"] for item in written], ["a.html", "b.html"])
            for name, data in outputs.items():
                path = os.path.join(directory, name)
                with open(path, "rb") as handle:
                    self.assertEqual(handle.read(), data)
                self.assertEqual(stat.S_IMODE(os.stat(path).st_mode), 0o644)

            a_path = os.path.join(directory, "a.html")
            with open(a_path, "wb") as handle:
                handle.write(b"operative")
            with self.assertRaises(release.ReleaseError):
                release.write_outputs_atomic(
                    directory, {"a.html": b"staged", "c.html": "not-bytes"})
            with open(a_path, "rb") as handle:
                self.assertEqual(handle.read(), b"operative")
            self.assertFalse(any(name.startswith(".")
                                 for name in os.listdir(directory)))

            with mock.patch.object(
                    release.os, "chmod", side_effect=OSError("chmod failed")):
                with self.assertRaises(OSError):
                    release.write_outputs_atomic(directory, {"d.html": b"x"})
            self.assertFalse(any(name.startswith(".")
                                 for name in os.listdir(directory)))
            self.assertFalse(os.path.exists(os.path.join(directory, "d.html")))

            for name in ("../escape", "/absolute", "nested/file", "CON"):
                with self.subTest(name=name), \
                        self.assertRaises(release.ReleaseError):
                    release.write_outputs_atomic(directory, {name: b"x"})

        with tempfile.TemporaryDirectory(
                prefix="aa11393-current-products-link-") as container:
            real = os.path.join(container, "real")
            link = os.path.join(container, "link")
            os.mkdir(real)
            os.symlink(real, link)
            with self.assertRaises(release.ReleaseError):
                release.write_outputs_atomic(link, {"x.html": b"x"})

    def test_configured_member_bundle_and_checksums_are_deterministic(self):
        na = b"<html>NA</html>"
        af = b"<html>AF</html>"
        members = [
            ("na.html", na),
            ("na.html.sha256", release.checksum_text("na.html", na)),
            ("af.html", af),
            ("af.html.sha256", release.checksum_text("af.html", af)),
            ("MANIFEST.txt", b"current configured-edition bundle\n"),
        ]
        first = bundlezip.build_zip(members, "2026-07-24T16:46:48Z")
        second = bundlezip.build_zip(members, "2026-07-24T16:46:48Z")
        self.assertEqual(first, second)
        self.assertEqual(bundlezip.read_zip_members(first), members)
        checksum = release.checksum_text("bundle.zip", first)
        self.assertEqual(
            release.verify_checksum(checksum, "bundle.zip", first),
            canon.bytes_digest(first))
        with self.assertRaises(bundlezip.BundleError):
            bundlezip.build_zip(members[:-1], "2026-07-24T16:46:48Z")
        bad_checksum = list(members)
        bad_checksum[1] = (bad_checksum[1][0], b"stale\n")
        with self.assertRaises(bundlezip.BundleError):
            bundlezip.build_zip(bad_checksum, "2026-07-24T16:46:48Z")

    def test_bundle_config_accepts_an_arbitrary_configured_edition_census(self):
        editions = ("alpha", "beta", "gamma")
        versions = tuple(item.upper() + "-2026-07-27-v1"
                         for item in editions)
        members = []
        for edition, version in zip(editions, versions):
            name = ("AA11393US-%s-claims-spec-navigator_%s.html" %
                    (edition.upper(), version))
            members.extend((
                {"edition": edition, "kind": "sealed", "name": name},
                {"artifact": name, "edition": edition,
                 "kind": "artifact-checksum", "name": name + ".sha256"},
            ))
        members.append({"kind": "manifest", "name": "MANIFEST.txt"})
        config = {
            "bundleVersion": bundlezip.BUNDLE_VERSION,
            "declaredTimestamp": "2026-07-28T00:00:00Z",
            "editions": list(editions),
            "manifestWordingId": bundlezip.BUNDLE_WORDING_ID,
            "members": members,
            "name": ("AA11393US-claims-navigators_%s_TECHNICAL-PREVIEW.zip" %
                     "_".join(versions)),
        }
        self.assertIs(bundlezip.validate_bundle_config(config), config)
        wrong = dict(config)
        wrong["members"] = [dict(item) for item in members]
        wrong["members"][0]["name"] = wrong["members"][0]["name"].replace(
            "-ALPHA-", "-BETA-")
        with self.assertRaises(bundlezip.BundleError):
            bundlezip.validate_bundle_config(wrong)

    def test_closed_configs_reject_removed_fields_and_surfaces_are_absent(self):
        schema = _json("navigator/schema/edition.schema.json")
        edition = _json("navigator/editions/na.json")
        schema_validate.check_schema(schema)
        self.assertEqual(schema_validate.validate(edition, schema), [])
        for field in (
                "approvalInventory", "compatibilityAuthorization",
                "migrationSource", "pinPlan", "qaProfile"):
            changed = dict(edition)
            changed[field] = "removed"
            with self.subTest(edition_field=field):
                self.assertTrue(schema_validate.validate(changed, schema))

        config = _json(bundlezip.BUNDLE_CONFIG_PATH)
        bundlezip.validate_bundle_config(config)
        changed = dict(config)
        changed["name"] = "arbitrary_TECHNICAL-PREVIEW.zip"
        with self.assertRaises(bundlezip.BundleError):
            bundlezip.validate_bundle_config(changed)
        for field in (
                "authorizationChain", "compatibilityAuthorization",
                "receipt", "releasePlan"):
            changed = dict(config)
            changed[field] = "removed"
            with self.subTest(bundle_field=field), \
                    self.assertRaises(bundlezip.BundleError):
                bundlezip.validate_bundle_config(changed)

        removed_files = (
            "navigator/bundle-manifest.json",
            "navigator/corpora.json",
            "navigator/relations/na__pct.json",
            "navigator/schema/commands.json",
            "navigator/schema/planes.json",
            "navigator/schema/release-policy.json",
            "navigator/strings.json",
        )
        self.assertFalse(any(os.path.isfile(os.path.join(ROOT, *path.split("/")))
                             for path in removed_files))
        for path in ("navigator/profiles", "navigator/records",
                     "navigator/tools"):
            absolute = os.path.join(ROOT, *path.split("/"))
            files = []
            if os.path.isdir(absolute):
                files = [name for name in os.listdir(absolute)
                         if os.path.isfile(os.path.join(absolute, name))]
            self.assertEqual(files, [], path)


if __name__ == "__main__":
    unittest.main()
