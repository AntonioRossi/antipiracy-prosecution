"""Focused data-only acceptance and command-surface fixtures."""

import copy
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from navigator.lib.snapshot import RepositorySnapshot
from structured_source import acceptance
from structured_source import __main__ as structured_source_main
from structured_source import parser
from structured_source.__main__ import COMMANDS, _parser
from structured_source.artifact_policy import (ArtifactClass, artifact_policy,
                                               classify_artifacts)
from structured_source.atomic import publish_set
from structured_source.canonical import raw_digest
from structured_source.control import canonical_json
from structured_source.errors import StructuredSourceError
from structured_source.markdown import convert_authored_markdown
from structured_source.verify import (_LIVE_IMPLEMENTATION,
                                      VerificationContext, validate_corpus)
from structured_source.tests.test_registry import registry_fixture


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AUTHORED_MARKDOWN = b'''<a id="ssp-authored-doc-root"></a>
<a id="ssp-title"></a>
# Exact title

<a id="ssp-body"></a>
Exact body.
'''


def _write_authored_fixture(root):
    root_path = Path(root)
    for control_path in parser.PARSER_CONTROL_PATHS:
        target = root_path / control_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(Path(ROOT, control_path).read_bytes())
    content = root_path / "content"
    content.mkdir(parents=True)
    (content / "authored.md").write_bytes(AUTHORED_MARKDOWN)
    conversion = convert_authored_markdown(
        AUTHORED_MARKDOWN, "content/authored.md", "authored-doc")
    (content / "authored.xml").write_bytes(conversion.xml)
    (content / "consumer.json").write_bytes(b"declared dependency\n")
    return registry_fixture()


def _authored_snapshot_context(root, registry):
    snapshot = RepositorySnapshot.capture(root, retain_bytes=True)
    return VerificationContext(
        root, registry=registry, byte_source=snapshot.byte_source(),
        repository_snapshot=snapshot)


class AcceptanceContract(unittest.TestCase):
    def setUp(self):
        self.registries = acceptance.load_registries(ROOT)

    def test_registries_are_ordered_current_domain_criteria_data_only(self):
        self.assertEqual(
            tuple(registry["domain"] for registry in self.registries),
            tuple(contract["domain"] for contract in acceptance.CONTRACTS))
        self.assertEqual(
            tuple(entry["code"]
                  for registry in self.registries
                  for entry in registry["criteria"]),
            acceptance.CRITERIA)
        for contract, registry in zip(acceptance.CONTRACTS, self.registries):
            self.assertEqual(set(registry), {
                "acceptanceVersion", "authorityScheme", "criteria", "domain"})
            self.assertEqual(registry["acceptanceVersion"], "2")
            self.assertEqual(
                registry["authorityScheme"], contract["authorityScheme"])
            self.assertTrue(all(set(entry) == {
                "code", "enforcer", "id", "outcome"}
                for entry in registry["criteria"]))

    def test_acceptance_tables_are_exact_domain_registry_projections(self):
        for contract, registry in zip(acceptance.CONTRACTS, self.registries):
            path = os.path.join(ROOT, contract["contractPath"])
            with self.subTest(domain=contract["domain"]), \
                    open(path, encoding="utf-8") as handle:
                text = handle.read()
            self.assertEqual(
                text.split(contract["tableStart"], 1)[1].split(
                    contract["tableEnd"], 1)[0],
                acceptance.render_table(registry))

    def test_contract_layout_is_exact_and_links_shared_aggregate_boundary(self):
        acceptance_paths = (
            "contracts/10-source-surfaces/pdf-transcription/acceptance-criteria.md",
            "contracts/10-source-surfaces/authored-markdown/acceptance-criteria.md",
            "contracts/20-semantic-relations/authored-relations/acceptance-criteria.md",
        )
        self.assertEqual(
            tuple(contract["contractPath"] for contract in acceptance.CONTRACTS),
            acceptance_paths)
        paths = []
        for contract in acceptance.CONTRACTS:
            paths.extend((
                contract["contractPath"],
                os.path.join(
                    os.path.dirname(contract["contractPath"]),
                    "technical-description.md"),
            ))
        self.assertEqual(len(paths), 6)
        for path in paths:
            with self.subTest(path=path):
                with open(os.path.join(ROOT, path), encoding="utf-8") as handle:
                    folded = handle.read().casefold()
                self.assertEqual(folded.count(
                    "](../../readme.md#aggregate-validation-boundary)"), 1)
                self.assertNotIn("python -m navigator validate-current", folded)
                self.assertNotIn("html5", folded)
                self.assertNotIn(".html", folded)

        for path in paths[1::2]:
            with open(os.path.join(ROOT, path), encoding="utf-8") as handle:
                self.assertIn(
                    "accepted only as one retained current state",
                    " ".join(handle.read().split()), path)
        for registry in self.registries:
            self.assertIn("contract pair", registry["criteria"][-1]["outcome"])

    def test_runner_and_callback_metadata_fail_closed(self):
        registry = self.registries[0]
        domain = registry["domain"]
        for field, value in (("runner", {}), ("namespace", "ssp")):
            malformed = copy.deepcopy(registry)
            malformed[field] = value
            with self.subTest(field=field), self.assertRaises(
                    StructuredSourceError):
                acceptance.validate_registry(malformed, domain)
        malformed = copy.deepcopy(registry)
        malformed["criteria"][0]["callbacks"] = ["retired"]
        with self.assertRaises(StructuredSourceError):
            acceptance.validate_registry(malformed, domain)
        for enforcer in (
                "structured_source.verify.absent; "
                "structured_source.tests.test_registry",
                "structured_source.verify.VerificationContext._control_closure; "
                "structured_source.tests.test_atomic"):
            malformed = copy.deepcopy(registry)
            malformed["criteria"][0]["enforcer"] = enforcer
            with self.subTest(enforcer=enforcer), \
                    self.assertRaises(StructuredSourceError):
                acceptance.validate_registry(malformed, domain)

    def test_parser_is_the_exact_command_surface(self):
        actions = _parser()._subparsers._group_actions[0].choices
        self.assertEqual(tuple(actions), COMMANDS)
        self.assertEqual(
            COMMANDS,
            ("check", "regenerate", "regenerate-controls"))
        self.assertFalse(os.path.exists(os.path.join(
            ROOT, "structured_source", "policy", "commands.json")))

    def test_regenerate_controls_uses_distinct_candidate_and_replacement_state(self):
        actual_loader = structured_source_main.load_parser_controls
        parent = mock.Mock()
        loaded_controls = []

        def load_controls_from_reader(reader):
            controls = actual_loader(reader)
            loaded_controls.append(controls)
            return controls

        def publish_and_validate(*unused_args, **kwargs):
            kwargs["postcondition"]()

        with mock.patch.object(
                structured_source_main, "load_parser_controls",
                side_effect=load_controls_from_reader) as load_controls, \
                mock.patch.object(
                    structured_source_main, "publish_set",
                    side_effect=publish_and_validate) as publish:
            parent.attach_mock(load_controls, "load")
            parent.attach_mock(publish, "publish")
            result = structured_source_main._regenerate_controls()
        self.assertEqual(result["status"], "regenerated")
        self.assertEqual(load_controls.call_count, 2)
        self.assertIsNot(loaded_controls[0], loaded_controls[1])
        self.assertEqual(publish.call_count, 1)
        self.assertEqual(
            [entry[0] for entry in parent.mock_calls],
            ["load", "publish", "load"])

        with mock.patch.object(
                structured_source_main, "load_parser_controls",
                side_effect=StructuredSourceError(
                    "candidate controls are invalid")), mock.patch.object(
                        structured_source_main, "publish_set") as publish, \
                self.assertRaisesRegex(
                    StructuredSourceError, "candidate controls"):
            structured_source_main._regenerate_controls()
        publish.assert_not_called()

        calls = {"count": 0}

        def fail_replacement_load(reader):
            calls["count"] += 1
            if calls["count"] == 1:
                return actual_loader(reader)
            raise StructuredSourceError("replacement controls are invalid")

        with mock.patch.object(
                structured_source_main, "load_parser_controls",
                side_effect=fail_replacement_load), mock.patch.object(
                    structured_source_main, "publish_set",
                    side_effect=publish_and_validate) as publish, \
                self.assertRaisesRegex(
                    StructuredSourceError, "replacement controls"):
            structured_source_main._regenerate_controls()
        publish.assert_called_once()

    def test_failed_replacement_validation_rolls_back_the_complete_output_set(self):
        with tempfile.TemporaryDirectory() as root:
            outputs = {
                "controls/content.xsd": (b"old-xsd", b"new-xsd"),
                "contracts/acceptance.md": (b"old-table", b"new-table"),
            }
            for relative, (before, unused_after) in outputs.items():
                path = Path(root, relative)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(before)

            def reject_replacement():
                raise StructuredSourceError("replacement controls are invalid")

            with self.assertRaisesRegex(
                    StructuredSourceError, "replacement controls"):
                publish_set(
                    root,
                    {path: after for path, (unused_before, after)
                     in outputs.items()},
                    {path: before for path, (before, unused_after)
                     in outputs.items()},
                    postcondition=reject_replacement)
            for relative, (before, unused_after) in outputs.items():
                self.assertEqual(Path(root, relative).read_bytes(), before)

    def test_authored_regenerate_rebuilds_equal_byte_state_and_handoff(self):
        with tempfile.TemporaryDirectory() as root:
            registry = _write_authored_fixture(root)
            context = _authored_snapshot_context(root, registry)
            old_result = context.check("authored-doc")
            old_result["status"] = "changed"
            self.assertEqual(
                context.check("authored-doc")["status"], "passed")
            old_state = context._validated_package_state["authored-doc"]
            old_handoff = context.read_for_consumer(
                "example-consumer", "authored-doc")
            before = Path(root, "content/authored.xml").read_bytes()

            result = context.regenerate("authored-doc")
            after = Path(root, "content/authored.xml").read_bytes()
            new_state = context._validated_package_state["authored-doc"]
            new_handoff = context.read_for_consumer(
                "example-consumer", "authored-doc")

        self.assertEqual(result["status"], "passed")
        self.assertEqual(after, before)
        self.assertIsNot(result, old_result)
        self.assertIsNot(new_state, old_state)
        self.assertIsNot(new_handoff, old_handoff)

    def test_authored_verifier_rejects_converter_self_report_as_authority(self):
        with tempfile.TemporaryDirectory() as root:
            registry = _write_authored_fixture(root)
            original_xml = Path(root, "content/authored.xml").read_bytes()
            original = convert_authored_markdown(
                AUTHORED_MARKDOWN, "content/authored.md", "authored-doc")

            changed_authority = AUTHORED_MARKDOWN.replace(
                b"Exact body.", b"Changed body.")
            Path(root, "content/authored.md").write_bytes(changed_authority)

            def stale_adapter(markdown, unused_path, unused_document_id):
                return {
                    "xml": original_xml,
                    "markdown": original.markdown,
                    "source_raw_digest": raw_digest(markdown),
                    "generated_markdown_raw_digest":
                        original.generated_markdown_raw_digest,
                    "item_ids": original.item_ids,
                    "fragment_digests": original.fragment_digests,
                }

            context = VerificationContext(
                root, registry=registry, markdown_adapter=stale_adapter)
            with self.assertRaisesRegex(
                    StructuredSourceError, "deterministic authority conversion"):
                context.check("authored-doc")

            Path(root, "content/authored.md").write_bytes(AUTHORED_MARKDOWN)
            false_reports = (
                {
                    "markdown": b"fabricated back-render\n",
                    "generated_markdown_raw_digest":
                        raw_digest(b"fabricated back-render\n"),
                },
                {"item_ids": tuple(reversed(original.item_ids))},
            )
            for report in false_reports:
                def false_adapter(
                        unused_markdown, unused_path, unused_document_id,
                        report=report):
                    value = {
                        "xml": original.xml,
                        "markdown": original.markdown,
                        "source_raw_digest": original.source_raw_digest,
                        "generated_markdown_raw_digest":
                            original.generated_markdown_raw_digest,
                        "item_ids": original.item_ids,
                        "fragment_digests": original.fragment_digests,
                    }
                    value.update(report)
                    return value

                with self.subTest(report=report):
                    context = VerificationContext(
                        root, registry=registry,
                        markdown_adapter=false_adapter)
                    with self.assertRaisesRegex(
                            StructuredSourceError,
                            "report differs from independent coverage"):
                        context.check("authored-doc")

    def test_authored_regenerate_rolls_back_failed_fresh_validation(self):
        with tempfile.TemporaryDirectory() as root:
            registry = _write_authored_fixture(root)
            context = VerificationContext(root, registry=registry)
            output = Path(root, "content/authored.xml")
            before = output.read_bytes()

            with mock.patch.object(
                    context, "check", side_effect=StructuredSourceError(
                        "replacement authored XML is invalid")), \
                    self.assertRaisesRegex(
                        StructuredSourceError,
                        "replacement authored XML is invalid"):
                context.regenerate("authored-doc")

            self.assertEqual(output.read_bytes(), before)
            self.assertNotIn("authored-doc", context._package_results)
            self.assertNotIn("authored-doc", context._derived_package_state)
            self.assertNotIn("authored-doc", context._validated_package_state)

    def test_authored_regenerate_rejects_pre_replacement_conversion_reuse(self):
        with tempfile.TemporaryDirectory() as root:
            registry = _write_authored_fixture(root)
            output = Path(root, "content/authored.xml")
            before = output.read_bytes()
            retained_conversion = convert_authored_markdown(
                AUTHORED_MARKDOWN, "content/authored.md", "authored-doc")

            def caching_adapter(
                    unused_markdown, unused_path, unused_document_id):
                return retained_conversion

            context = VerificationContext(
                root, registry=registry, markdown_adapter=caching_adapter)
            with self.assertRaisesRegex(
                    StructuredSourceError, "crossed a validation lifetime"):
                context.regenerate("authored-doc")

            self.assertEqual(output.read_bytes(), before)
            self.assertNotIn("authored-doc", context._package_results)
            self.assertNotIn("authored-doc", context._derived_package_state)
            self.assertNotIn("authored-doc", context._validated_package_state)

    def test_validate_corpus_uses_one_pass_and_emits_plain_statuses(self):
        snapshot = type("Snapshot", (), {"digest": "sha256:test"})()
        with mock.patch(
                "structured_source.verify.VerificationContext") as context_type:
            context = context_type.return_value
            context.verify_all.return_value = {
                "consumerEdges": 4,
                "consumerHandoffs": 4,
                "criteria": len(acceptance.CRITERIA),
                "globalPasses": 1,
                "status": "passed",
            }
            corpus = validate_corpus(
                ROOT, byte_source=lambda unused_path: b"retained",
                repository_snapshot=snapshot)
            result = corpus.public_result()
        context.verify_all.assert_called_once_with()
        self.assertEqual(result["snapshotDigest"], "sha256:test")
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["results"], [
            {"id": criterion, "status": "passed"}
            for criterion in acceptance.CRITERIA
        ])
        self.assertEqual(
            [entry["domain"] for entry in result["domains"]],
            [contract["domain"] for contract in acceptance.CONTRACTS])
        self.assertTrue(all(entry["criteria"] == 6
                            for entry in result["domains"]))
        self.assertTrue(all(
            set(entry) == {"id", "status"} for entry in result["results"]))

    def test_validate_corpus_requires_bytes_and_exact_handoffs(self):
        with self.assertRaisesRegex(
                StructuredSourceError, "retained snapshot"):
            validate_corpus(
                ROOT, byte_source=None, repository_snapshot=None)
        snapshot = type("Snapshot", (), {"digest": "sha256:test"})()
        with mock.patch(
                "structured_source.verify.VerificationContext") as context_type:
            context_type.return_value.verify_all.return_value = {
                "consumerEdges": 1,
                "consumerHandoffs": 0,
                "criteria": len(acceptance.CRITERIA),
                "globalPasses": 1,
                "status": "passed",
            }
            with self.assertRaisesRegex(
                    StructuredSourceError, "current criteria"):
                validate_corpus(
                    ROOT, byte_source=lambda unused_path: b"retained",
                    repository_snapshot=snapshot)

    def test_real_global_pass_checks_each_package_once(self):
        context = VerificationContext(ROOT, registry=registry_fixture())
        package_results = {
            package_id: {
                "packageId": package_id,
                "authorityScheme": package["authorityScheme"],
                "status": "passed",
                "computedCoverage": {"coveredItems": 1},
            }
            for package_id, package in context.packages.items()
        }
        with mock.patch.object(
                context, "_control_closure",
                return_value=tuple(
                    {"criteria": [{}] * 6}
                    for unused_contract in acceptance.CONTRACTS)), \
                mock.patch.object(
                    context, "check",
                    side_effect=lambda package_id: package_results[package_id]
                ) as check:
            first = context.verify_all()
            second = context.verify_all()
        self.assertIsNot(first, second)
        self.assertEqual(first, second)
        self.assertEqual(first["globalPasses"], 1)
        self.assertEqual(check.call_count, len(context.packages))

    def test_global_pass_constructs_every_declared_consumer_handoff(self):
        context = VerificationContext(
            ROOT, registry=registry_fixture(), repository_snapshot=object())
        package_results = {
            package_id: {
                "packageId": package_id,
                "authorityScheme": package["authorityScheme"],
                "status": "passed",
                "computedCoverage": {"coveredItems": 1},
            }
            for package_id, package in context.packages.items()
        }
        expected = [
            (consumer["consumerId"], edge["packageId"])
            for consumer in context.registry["consumers"]
            for edge in consumer["edges"]]
        with mock.patch.object(
                context, "_control_closure",
                return_value=tuple(
                    {"criteria": [{}] * 6}
                    for unused_contract in acceptance.CONTRACTS)), \
                mock.patch.object(
                    context, "check",
                    side_effect=lambda package_id: package_results[package_id]), \
                mock.patch.object(
                    context, "read_for_consumer",
                    side_effect=lambda consumer_id, package_id: {
                        "consumerId": consumer_id, "packageId": package_id,
                    }) as handoff:
            result = context.verify_all()
        self.assertEqual(handoff.call_args_list, [
            mock.call(consumer_id, package_id)
            for consumer_id, package_id in expected])
        self.assertEqual(result["consumerEdges"], len(expected))
        self.assertEqual(result["consumerHandoffs"], len(expected))

    def test_targeted_retired_import_scan_fails_closed(self):
        for statement in (
                b"from structured_source import approvals\n",
                b"from .approvals import resolve\n"):
            with self.subTest(statement=statement), \
                    tempfile.TemporaryDirectory() as root:
                path = os.path.join(root, "structured_source")
                os.makedirs(path)
                with open(os.path.join(path, "legacy.py"), "wb") as handle:
                    handle.write(statement)
                context = VerificationContext(root, registry=registry_fixture())
                with self.assertRaisesRegex(StructuredSourceError, "retired"):
                    context._reject_retired_imports({
                        "structured_source/legacy.py"})

    def test_artifact_policy_is_exhaustive_and_evidence_wording_is_unscanned(self):
        token = "semantic" + "Digest"
        with tempfile.TemporaryDirectory() as root:
            os.makedirs(os.path.join(root, "content"))
            with open(os.path.join(root, "content", "evidence.xml"), "wb") as handle:
                handle.write(("<text>canonical XML %s</text>\n" % token).encode())
            with open(os.path.join(root, "content", "evidence.md"), "wb") as handle:
                handle.write(("canonical XML %s\n" % token).encode())
            with open(os.path.join(root, "content", "authored.md"), "wb") as handle:
                handle.write(("Authority code says ``%s``.\n" % token).encode())
            with open(os.path.join(root, "review.html"), "wb") as handle:
                handle.write(("<p>%s</p>\n" % token).encode())
            vector = os.path.join(root, "navigator", "tests", "vectors")
            os.makedirs(vector)
            with open(os.path.join(vector, "non_nfc.json"), "wb") as handle:
                handle.write('{"input":"A\\u0301"}\n'.encode())
            context = VerificationContext(root, registry=registry_fixture())
            evidence_paths = {
                "content/authored.md", "content/evidence.xml",
                "content/evidence.md", "review.html",
                "navigator/tests/vectors/non_nfc.json"}
            context._reject_retired_control_residue(evidence_paths)
            index = classify_artifacts(evidence_paths, context.registry)
            self.assertEqual(set(artifact_policy()), set(ArtifactClass))
            self.assertEqual(index["content/evidence.xml"],
                             ArtifactClass.AUTHORITY_CONTENT)
            self.assertEqual(index["content/authored.md"],
                             ArtifactClass.AUTHORITY_CONTENT)
            self.assertEqual(index["content/evidence.md"],
                             ArtifactClass.GENERATED_EVIDENCE_REVIEW)
            self.assertEqual(index["review.html"],
                             ArtifactClass.GENERATED_PRODUCT)
            self.assertEqual(index["navigator/tests/vectors/non_nfc.json"],
                             ArtifactClass.TEST_FIXTURE)

            implementation = os.path.join(root, "structured_source")
            os.makedirs(implementation)
            with open(os.path.join(implementation, "obsolete.py"), "wb") as handle:
                handle.write(("def %s():\n    pass\n" % token).encode())
            with self.assertRaisesRegex(StructuredSourceError, "residue"):
                context._reject_retired_control_residue(
                    evidence_paths | {"structured_source/obsolete.py"})

            with open(os.path.join(root, "content", "consumer.json"), "wb") as handle:
                handle.write(canonical_json({token: "active"}))
            with self.assertRaisesRegex(StructuredSourceError, "residue"):
                context._reject_retired_control_residue(
                    evidence_paths | {"content/consumer.json"})

            docs = os.path.join(root, "docs")
            os.makedirs(docs)
            with open(os.path.join(docs, "current.md"), "wb") as handle:
                handle.write(("Current machine field: `%s`.\n" % token).encode())
            with self.assertRaisesRegex(StructuredSourceError, "residue"):
                context._reject_retired_control_residue(
                    evidence_paths | {"docs/current.md"})
            machine_documents = (
                "Current machine field: ``%s``.\n" % token,
                "```text\n%s\n```\n" % token,
                "~~~text\n%s\n" % token,
                "[Current field](%s)\n" % token,
            )
            for index, document in enumerate(machine_documents):
                relative = "docs/machine-%d.md" % index
                with open(os.path.join(root, relative), "wb") as handle:
                    handle.write(document.encode())
                fresh = VerificationContext(root, registry=registry_fixture())
                with self.subTest(document=document), self.assertRaisesRegex(
                        StructuredSourceError, "residue"):
                    fresh._reject_retired_control_residue(
                        evidence_paths | {relative})
            with open(os.path.join(docs, "current-prose.md"), "wb") as handle:
                handle.write(("Quoted evidence says %s.\n" % token).encode())
            context._reject_retired_control_residue(
                evidence_paths | {"docs/current-prose.md"})
            with self.assertRaisesRegex(StructuredSourceError, "no current class"):
                classify_artifacts(
                    evidence_paths | {"content/unknown.future"},
                    context.registry)

    def test_structured_source_path_inventory_has_no_alternate_reader(self):
        paths = set()
        source_root = os.path.join(ROOT, "structured_source")
        for directory, dirnames, filenames in os.walk(source_root):
            dirnames[:] = [name for name in dirnames if name != "__pycache__"]
            paths.update(
                os.path.relpath(os.path.join(directory, name), ROOT)
                .replace(os.sep, "/") for name in filenames)
        context = VerificationContext(ROOT, registry=registry_fixture())
        context._reject_alternate_structured_source_paths(paths)
        for changed in (
                paths | {"structured_source/alternate_reader.py"},
                paths - {"structured_source/parser.py"}):
            with self.assertRaisesRegex(
                    StructuredSourceError, "inventory differs"):
                context._reject_alternate_structured_source_paths(changed)

    def test_transitive_code_and_vector_inventory_has_no_alternate_path(self):
        context = VerificationContext(
            ROOT, registry=registry_fixture(), repository_snapshot=object())
        paths = set(_LIVE_IMPLEMENTATION)
        context._reject_alternate_implementation_paths(paths)
        for label, changed in (
                ("extra code", paths | {"helpers/alternate_reader.py"}),
                ("extra vector", paths | {
                    "navigator/tests/vectors/alternate.json"}),
                ("extra contract", paths | {
                    "contracts/alternate/technical-description.md"}),
                ("extra schema", paths | {"helpers/alternate.xsd"}),
                ("missing code", paths - {"structured_source/parser.py"}),
                ("missing contract", paths - {
                    "contracts/10-source-surfaces/pdf-transcription/"
                    "technical-description.md"}),
                ("missing schema", paths - {
                    "structured_source/schemas/content.xsd"}),
                ("missing vector", paths - {
                    "navigator/tests/vectors/canon_vectors.json"})):
            with self.subTest(label=label), self.assertRaisesRegex(
                    StructuredSourceError, "inventory differs"):
                context._reject_alternate_implementation_paths(changed)

    def test_live_closure_contains_all_domains_and_shared_consumer_code(self):
        required = {
            "AGENTS.md",
            "GLOSSARY.md",
            "README.md",
            "STRUCTURED-CONTENT-AUTHORITY-MANIFEST.md",
            "contracts/README.md",
            "contracts/10-source-surfaces/authored-markdown/acceptance-criteria.md",
            "contracts/10-source-surfaces/authored-markdown/technical-description.md",
            "contracts/10-source-surfaces/pdf-transcription/acceptance-criteria.md",
            "contracts/10-source-surfaces/pdf-transcription/technical-description.md",
            "contracts/20-semantic-relations/authored-relations/acceptance-criteria.md",
            "contracts/20-semantic-relations/authored-relations/technical-description.md",
            "contracts/20-semantic-relations/claim-prior-art-passage-map/acceptance-criteria_DRAFT.md",
            "contracts/20-semantic-relations/claim-prior-art-passage-map/technical-description_DRAFT.md",
            "contracts/30-product-generation/claims-navigator/acceptance-criteria_DRAFT.md",
            "contracts/30-product-generation/claims-navigator/technical-description_DRAFT.md",
            "contracts/30-product-generation/claims-prior-art-navigator/acceptance-criteria_DRAFT.md",
            "contracts/30-product-generation/claims-prior-art-navigator/technical-description_DRAFT.md",
            "contracts/30-product-generation/navigator-guide/acceptance-criteria_DRAFT.md",
            "contracts/30-product-generation/navigator-guide/technical-description_DRAFT.md",
            "contracts/30-product-generation/navigator-presentation/acceptance-criteria_DRAFT.md",
            "contracts/30-product-generation/navigator-presentation/technical-description_DRAFT.md",
            "navigator/__init__.py", "navigator/__main__.py",
            "navigator/build.py",
            "navigator/RUNBOOK-content-sync-and-regeneration.md",
            "structured_source/registry/acceptance-authored-markdown.json",
            "structured_source/registry/acceptance-authored-relations.json",
            "structured_source/registry/acceptance-pdf-transcription.json",
            "navigator/schema/prior-art-map-acceptance.json",
            "navigator/schema/presentation-acceptance.json",
            "structured_source/relation_projection.py",
        }
        for relative in ("navigator/lib", "navigator/schema",
                         "navigator/tests"):
            absolute = os.path.join(ROOT, *relative.split("/"))
            for directory, dirnames, filenames in os.walk(absolute):
                dirnames[:] = sorted(
                    name for name in dirnames if name != "__pycache__")
                for name in filenames:
                    path = os.path.relpath(
                        os.path.join(directory, name), ROOT).replace(
                            os.sep, "/")
                    if relative == "navigator/tests" and not (
                            name == "__init__.py" or
                            name.startswith("test_") or
                            "/vectors/" in "/" + path):
                        continue
                    required.add(path)
        self.assertFalse(
            required - _LIVE_IMPLEMENTATION,
            sorted(required - _LIVE_IMPLEMENTATION))


if __name__ == "__main__":
    unittest.main()
