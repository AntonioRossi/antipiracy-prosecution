"""Regression tests for review identity and migration lifecycle semantics."""

import copy
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "navigator"))

from lib import canon, gateway, migrate, model, validate  # noqa: E402
import build as build_mod  # noqa: E402
from tools import stamp as stamp_tool  # noqa: E402


def load_model(edition="na"):
    boot = gateway.ContentGateway(ROOT)
    path = "navigator/editions/%s.json" % edition
    allowlist = json.loads(boot.read_text(path))["declaredTransitiveInputs"]
    content = gateway.ContentGateway(ROOT, allowlist=allowlist)
    return model.EditionModel(content, path)


def load_model_from_root(root, path):
    boot = gateway.ContentGateway(root)
    config = json.loads(boot.read_text(path))
    content = gateway.ContentGateway(
        root, allowlist=config["declaredTransitiveInputs"])
    return model.EditionModel(content, path)


def restamp_in_memory(m):
    """Make the fixture current under the running projection algorithm.

    This is test setup, not an authoring operation: production review records
    must only be restamped by a reviewer after inspecting the diff.
    """
    for _, _, fields, projection in m.iter_owners():
        fields["reviewState"] = "internally-reviewed"
        fields["review"]["by"] = "synthetic-test-reviewer"
        fields["review"]["date"] = "2026-07-22"
        fields["review"]["operatorKind"] = "human"
        fields["review"]["contentHash"] = m.content_hash(projection)
        fields["migrationState"] = "current"
        fields.pop("migrationReason", None)
        fields.pop("previousTargets", None)


def rebuild_quotable_positions(m):
    """Keep the synthetic guidance order and its ambiguity index aligned."""
    positions = {}
    for anchor in m.guidance_order:
        if anchor.cls == "quotable":
            positions.setdefault(anchor.digest, []).append(anchor.id)
    m.quotable_digest_positions = positions


def duplicate_quotable_anchor(m, block_id, suffix):
    """Add a same-text eligible source at the next document occurrence."""
    original = m.quotable_anchor(block_id)
    duplicate = model.Anchor(
        "synthetic-quotable-%s" % suffix,
        original.digest, original.kind, original.cls,
        original.label + " (synthetic duplicate)",
        parent=original.parent, block=original.block)
    m.guidance_anchors[duplicate.id] = duplicate
    index = m.guidance_order.index(original)
    m.guidance_order.insert(index + 1, duplicate)
    rebuild_quotable_positions(m)
    return original, duplicate


def move_quotable_before(m, moving, reference):
    """Model a corpus edit that changes same-digest occurrence identity."""
    m.guidance_order.remove(moving)
    m.guidance_order.insert(m.guidance_order.index(reference), moving)
    rebuild_quotable_positions(m)


def copy_edition_tree(destination, edition="na"):
    """Copy one edition's declared content closure for authoring-tool tests."""
    edition_path = "navigator/editions/%s.json" % edition
    with open(os.path.join(ROOT, edition_path), encoding="utf-8") as fh:
        config = json.load(fh)
    for relative in config["declaredTransitiveInputs"]:
        source = os.path.join(ROOT, relative)
        target = os.path.join(destination, relative)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        shutil.copyfile(source, target)


class TestContextualIdentity(unittest.TestCase):
    def test_claim_members_use_whole_claim_as_parent_container(self):
        m = load_model()
        member = m.target_anchors["S215"]
        self.assertEqual(member.kind, "claim-element")
        self.assertEqual(member.parent, "PC1")

        ctx = m.contextual_identity(member.id, member.digest)
        self.assertIsNotNone(ctx)
        self.assertEqual(ctx["parentHash"], m.target_anchors["PC1"].digest)
        self.assertEqual(ctx["occurrence"],
                         m.digest_positions[member.digest].index(member.id) + 1)

    def test_whole_claim_is_not_parented_to_last_document_heading(self):
        m = load_model()
        whole = m.target_anchors["PC2"]
        self.assertEqual(whole.kind, "claim-whole")
        self.assertEqual(whole.parent, "S210")
        self.assertEqual(m.target_anchors[whole.parent].label, "Claims")

    def test_parent_graph_is_acyclic_and_root_fallback_is_a_hash(self):
        m = load_model()
        for anchor in m.target_order:
            seen = set()
            current = anchor
            while current.parent is not None:
                self.assertNotIn(current.id, seen)
                seen.add(current.id)
                current = m.target_anchors[current.parent]

        root = m.target_anchors["S001"]
        m.digest_positions[root.digest] = [root.id, "synthetic-duplicate"]
        context = m.contextual_identity(root.id, root.digest)
        self.assertRegex(context["parentHash"], r"^sha256/c1:[0-9a-f]{64}$")

    def test_repeated_table_row_uses_its_table_as_context(self):
        m = load_model()
        row = m.target_anchors["S166.r5"]
        ctx = m.contextual_identity(row.id, row.digest)
        self.assertEqual(row.parent, "S166")
        self.assertEqual(ctx["parentHash"], m.target_anchors["S166"].digest)

    def test_ambiguous_quotable_sources_cover_every_review_projection(self):
        m = load_model()
        target_entry = next(
            gate for gate in m.gates["gates"]
            if gate["requiredScope"] == "target")
        fragment_entry = next(
            gate for gate in m.gates["gates"]
            if gate["requiredScope"] == "fragment")
        claim_entry = next(
            gate for gate in m.gates["gates"]
            if gate["requiredScope"] == "claim")
        source_blocks = tuple(dict.fromkeys(
            gate["source"]["block"]
            for gate in (target_entry, fragment_entry, claim_entry)))
        duplicates = {}
        for block_id in source_blocks:
            unused_original, duplicate = duplicate_quotable_anchor(
                m, block_id, block_id.lower())
            duplicates[block_id] = duplicate

        # Target-level caution source.
        target_fid = target_entry["appliesTo"]["fragments"][0]["id"]
        fragment = m.relation["fragments"][target_fid]
        target = next(t for t in fragment["targets"]
                      if t.get("caution", {}).get("gateId") ==
                      target_entry["gateId"])
        target_source = target["caution"]["source"]
        target_projection = m.unit_projection(target_fid, fragment)
        projected_target = next(
            t for t in target_projection["targets"]
            if t.get("caution", {}).get("gateId") == target_entry["gateId"])
        target_context = projected_target["caution"]["source"] \
            ["contextualIdentity"]
        self.assertEqual(target_context["occurrence"], 1)

        # Owner-level caution source.
        fragment_fid = fragment_entry["appliesTo"]["fragments"][0]["id"]
        fragment = m.relation["fragments"][fragment_fid]
        fragment_projection = m.unit_projection(fragment_fid, fragment)
        self.assertEqual(
            fragment_projection["caution"]["source"]
            ["contextualIdentity"]["occurrence"], 1)

        # Claim-gate source and gate-inventory entry source.
        claim_key = "c%d" % claim_entry["appliesTo"]["claims"][0]["claim"]
        claim_gate = next(
            gate for gate in m.relation["claimGates"][claim_key]
            if gate["gateId"] == claim_entry["gateId"])
        claim_projection = m.claim_gate_projection(claim_key, claim_gate)
        self.assertEqual(
            claim_projection["source"]["contextualIdentity"]["occurrence"],
            1)
        entry = claim_entry
        entry_projection = m.gate_entry_projection(entry)
        self.assertEqual(
            entry_projection["source"]["contextualIdentity"],
            claim_projection["source"]["contextualIdentity"])

        # The locator remains excluded, but selecting the other identical
        # occurrence changes contextual identity and therefore both review
        # digests.  No authored contextual field is added to either source.
        target_hash = m.content_hash(target_projection)
        target_source["block"] = duplicates[
            target_entry["source"]["block"]].id
        changed_target = m.unit_projection(
            target_fid, m.relation["fragments"][target_fid])
        changed_projected_target = next(
            t for t in changed_target["targets"]
            if t.get("caution", {}).get("gateId") == target_entry["gateId"])
        self.assertEqual(
            changed_projected_target["caution"]["source"]
            ["contextualIdentity"]["occurrence"], 2)
        self.assertNotEqual(target_hash, m.content_hash(changed_target))

        entry_hash = m.gate_entry_hash(entry["gateId"])
        entry["source"]["block"] = duplicates[
            claim_entry["source"]["block"]].id
        self.assertEqual(
            m.gate_entry_projection(entry)["source"]
            ["contextualIdentity"]["occurrence"], 2)
        self.assertNotEqual(entry_hash, m.gate_entry_hash(entry["gateId"]))
        self.assertNotIn("contextualIdentity", target_source)
        self.assertNotIn("contextualIdentity", entry["source"])

    def test_quotable_root_fallback_is_the_claim_corpus_hash(self):
        m = load_model()
        original = next(a for a in m.guidance_order
                        if a.cls == "quotable")
        duplicate = model.Anchor(
            "synthetic-root-quotable", original.digest, original.kind,
            original.cls, original.label, parent=None, block=original.block)
        original.parent = None
        m.guidance_anchors[duplicate.id] = duplicate
        m.guidance_order.append(duplicate)
        rebuild_quotable_positions(m)

        context = m.quotable_contextual_identity(
            original.id, original.digest)
        self.assertEqual(context["parentHash"], m.guidance_root_hash)
        self.assertRegex(context["parentHash"],
                         r"^sha256/c1:[0-9a-f]{64}$")


class TestMigrationLifecycle(unittest.TestCase):
    def _diff_fixture(self):
        digest = canon.text_digest("migration-diff-fixture")
        fragment = {
            "status": "mapped",
            "reviewState": "internally-reviewed",
            "migrationState": "current",
            "review": {
                "by": "reviewer", "operatorKind": "human",
                "date": "2026-07-22", "contentHash": digest,
            },
            "fragmentTextHash": digest,
            "targets": [{"block": "S001", "textHash": digest}],
        }
        relation = {
            "fragments": {"c1u0": fragment},
            "claimGates": {},
            "dispositions": [],
        }
        inventory = {
            "gates": [{
                "gateId": "synthetic-gate",
                "source": {"block": "S010", "textHash": digest},
            }],
        }
        return digest, relation, inventory

    def test_diff_classifier_accepts_only_closed_migration_actions(self):
        digest, before_relation, before_inventory = self._diff_fixture()
        after_relation = copy.deepcopy(before_relation)
        owner = after_relation["fragments"]["c1u0"]
        owner["targets"][0]["block"] = "S002"
        owner["migrationState"] = "stale"
        owner["migrationReason"] = "target-changed"
        owner["previousTargets"] = copy.deepcopy(
            before_relation["fragments"]["c1u0"]["targets"])
        after_relation["fragments"]["c1u1"] = {
            "status": "counsel-review-required",
            "reviewState": "pending",
            "migrationState": "current",
            "review": {
                "by": "migrate", "operatorKind": "tool",
                "date": "", "contentHash": "",
            },
            "fragmentTextHash": digest,
        }
        after_inventory = copy.deepcopy(before_inventory)
        after_inventory["gates"][0]["source"]["block"] = "S011"

        self.assertEqual(migrate.migration_diff_problems(
            before_relation, after_relation,
            before_inventory, after_inventory,
            fragment_hashes={"c1u1": digest}), [])

        semantic = copy.deepcopy(after_relation)
        semantic["fragments"]["c1u0"]["status"] = \
            "counsel-review-required"
        review = copy.deepcopy(after_relation)
        review["fragments"]["c1u0"]["review"]["by"] = "migrate"
        target_digest = copy.deepcopy(after_relation)
        target_digest["fragments"]["c1u0"]["targets"][0]["textHash"] = \
            canon.text_digest("different")
        for illegal in (semantic, review, target_digest):
            self.assertTrue(migrate.migration_diff_problems(
                before_relation, illegal,
                before_inventory, after_inventory,
                fragment_hashes={"c1u1": digest}))

    def test_diff_classifier_rejects_forged_snapshot_or_proposal_digest(self):
        digest, before_relation, before_inventory = self._diff_fixture()
        after_relation = copy.deepcopy(before_relation)
        owner = after_relation["fragments"]["c1u0"]
        owner["migrationState"] = "stale"
        owner["migrationReason"] = "target-changed"
        owner["previousTargets"] = []
        problems = migrate.migration_diff_problems(
            before_relation, after_relation,
            before_inventory, before_inventory)
        self.assertTrue(any("previousTargets" in problem
                            for problem in problems))

        after_relation = copy.deepcopy(before_relation)
        after_relation["fragments"]["c1u1"] = {
            "status": "counsel-review-required",
            "reviewState": "pending",
            "migrationState": "current",
            "review": {
                "by": "migrate", "operatorKind": "tool",
                "date": "", "contentHash": "",
            },
            "fragmentTextHash": digest,
        }
        problems = migrate.migration_diff_problems(
            before_relation, after_relation,
            before_inventory, before_inventory,
            fragment_hashes={"c1u1": canon.text_digest("actual-unit")})
        self.assertTrue(any("outside action classes" in problem
                            for problem in problems))

    def test_migrate_command_refuses_illegal_diff_before_any_write(self):
        unused_digest, relation, inventory = self._diff_fixture()
        fake_model = SimpleNamespace(
            relation=relation,
            gates=inventory,
            schemas={"relation": {}, "gates": {}},
            units={},
        )

        def mutate_review(unused_model, unused_log):
            unused_model.relation["fragments"]["c1u0"]["review"]["by"] = \
                "unauthorized-migration"

        with mock.patch.object(build_mod, "build_model",
                               return_value=(object(), fake_model)), \
                mock.patch.object(build_mod.migrate_mod,
                                  "migrate_inventory"), \
                mock.patch.object(build_mod.migrate_mod, "migrate_relation",
                                  side_effect=mutate_review), \
                mock.patch.object(build_mod.schema_validate, "validate",
                                  return_value=[]), \
                mock.patch.object(build_mod.gateway,
                                  "write_source") as write_source, \
                mock.patch.object(build_mod.sys, "stderr", io.StringIO()):
            with self.assertRaisesRegex(
                    SystemExit, "closed migration action classes"):
                build_mod.cmd_migrate("synthetic", [])
            write_source.assert_not_called()

    def test_previous_targets_are_snapshotted_once(self):
        m = load_model()
        restamp_in_memory(m)
        frag = m.relation["fragments"]["c1u0"]
        original = copy.deepcopy(frag["targets"])
        removed = frag["targets"][0]
        del m.target_anchors[removed["block"]]
        m.digest_positions.pop(removed["textHash"], None)

        first_log = []
        migrate.migrate_relation(m, first_log)
        snapshot = copy.deepcopy(frag["previousTargets"])
        self.assertEqual(snapshot, original)
        self.assertEqual(frag["migrationReason"], "target-removed")

        second_log = []
        migrate.migrate_relation(m, second_log)
        self.assertEqual(frag["previousTargets"], snapshot)
        self.assertEqual(second_log, [])

    def test_current_target_still_rechecks_its_source_gate(self):
        m = load_model()
        restamp_in_memory(m)
        entry = next(g for g in m.gates["gates"]
                     if g["requiredScope"] == "target")
        fid = entry["appliesTo"]["fragments"][0]["id"]
        frag = m.relation["fragments"][fid]
        caution = next(t["caution"] for t in frag["targets"]
                       if t.get("caution", {}).get("gateId") ==
                       entry["gateId"])
        caution["source"]["textHash"] = \
            "sha256/c1:" + ("0" * 64)

        log = []
        migrate.migrate_relation(m, log)
        self.assertEqual(frag["migrationState"], "stale")
        self.assertEqual(frag["migrationReason"], "source-changed")
        self.assertIn(("stale", fid, "source-changed"), log)

    def test_quotable_context_drift_stales_caution_owner(self):
        m = load_model()
        entry = next(g for g in m.gates["gates"]
                     if g["requiredScope"] == "target")
        fid = entry["appliesTo"]["fragments"][0]["id"]
        fragment = m.relation["fragments"][fid]
        target = next(t for t in fragment["targets"]
                      if t.get("caution", {}).get("gateId") ==
                      entry["gateId"])
        source = target["caution"]["source"]
        original, duplicate = duplicate_quotable_anchor(
            m, source["block"], "caution-migration")
        restamp_in_memory(m)
        reviewed_hash = fragment["review"]["contentHash"]

        # Both the locator and covered text digest still resolve.  Only the
        # same-digest occurrence identity changed, which migration must not
        # silently treat as review-neutral.
        move_quotable_before(m, duplicate, original)
        self.assertEqual(
            m.quotable_anchor(source["block"]).digest, source["textHash"])
        self.assertNotEqual(
            reviewed_hash, m.content_hash(m.unit_projection(fid, fragment)))

        log = []
        migrate.migrate_relation(m, log)
        self.assertEqual(fragment["migrationState"], "stale")
        self.assertEqual(fragment["migrationReason"], "endpoint-changed")
        self.assertIn(("stale", "unit %s" % fid, "endpoint-changed"), log)

    def test_inventory_context_drift_stales_pinned_disposition(self):
        m = load_model()
        claim_entry = next(g for g in m.gates["gates"]
                           if g["requiredScope"] == "claim")
        disposition = next(
            d for d in m.relation["dispositions"]
            if d["gateId"] == claim_entry["gateId"])
        entry = m.gates_by_id[disposition["gateId"]]
        original, duplicate = duplicate_quotable_anchor(
            m, entry["source"]["block"], "inventory-migration")
        disposition["gateEntryHash"] = m.gate_entry_hash(
            disposition["gateId"])
        disposition["migrationState"] = "current"
        disposition.pop("migrationReason", None)
        disposition["review"]["contentHash"] = m.content_hash(
            m.disposition_projection(disposition))
        reviewed_entry_hash = disposition["gateEntryHash"]

        move_quotable_before(m, duplicate, original)
        self.assertNotEqual(
            reviewed_entry_hash, m.gate_entry_hash(disposition["gateId"]))

        inventory_log = []
        migrate.migrate_inventory(m, inventory_log)
        self.assertEqual(inventory_log, [])  # locator/digest still resolve
        relation_log = []
        migrate.migrate_relation(m, relation_log)
        self.assertEqual(disposition["migrationState"], "stale")
        self.assertEqual(disposition["migrationReason"], "endpoint-changed")
        subject_id = disposition["subject"]["id"]
        self.assertIn(
            ("stale", "disp:%s@%s" % (entry["gateId"], subject_id),
             "endpoint-changed"), relation_log)

    def test_inventory_migration_refuses_two_identical_source_matches(self):
        m = load_model()
        entry = next(g for g in m.gates["gates"]
                     if g["requiredScope"] == "claim")
        original_block = entry["source"]["block"]
        duplicate_quotable_anchor(m, original_block,
                                  "inventory-ambiguous")
        entry["source"]["block"] = "missing-after-corpus-shift"

        log = []
        migrate.migrate_inventory(m, log)

        self.assertEqual(entry["source"]["block"],
                         "missing-after-corpus-shift")
        self.assertIn(
            ("manual", "inventory:%s" % entry["gateId"],
             "source block unresolved (2 matches)"), log)

    def test_already_stale_owner_records_more_specific_removed_target(self):
        m = load_model()
        restamp_in_memory(m)
        frag = m.relation["fragments"]["c1u0"]
        frag["migrationState"] = "stale"
        frag["migrationReason"] = "endpoint-changed"
        original = copy.deepcopy(frag["targets"])
        removed = frag["targets"][0]
        del m.target_anchors[removed["block"]]
        m.digest_positions.pop(removed["textHash"], None)

        log = []
        migrate.migrate_relation(m, log)

        self.assertEqual(frag["migrationReason"], "target-removed")
        self.assertEqual(frag["previousTargets"], original)
        self.assertIn(("stale", "c1u0", "target-removed"), log)

    def test_changed_phrase_preserves_its_complete_target_snapshot(self):
        m = load_model()
        restamp_in_memory(m)
        fragment_id, phrase = next(
            (fid, phrase)
            for fid, fragment in m.relation["fragments"].items()
            for phrase in fragment.get("phrases", [])
            if phrase.get("targets"))
        original = copy.deepcopy(phrase["targets"])
        m.units[fragment_id].text = "phrase removed from this unit"

        log = []
        migrate.migrate_relation(m, log)

        self.assertEqual(phrase["migrationReason"], "changed")
        self.assertEqual(phrase["previousTargets"], original)

    def test_removed_whole_claim_marks_every_owner_without_projection_crash(self):
        m = load_model()
        restamp_in_memory(m)
        removed_ids = [fid for fid in m.units if fid.startswith("c1u")]
        for fid in removed_ids:
            del m.units[fid]
        del m.agg_hashes[1]
        del m.chain_hashes[1]

        log = []
        migrate.migrate_relation(m, log)

        for fid in removed_ids:
            fragment = m.relation["fragments"][fid]
            self.assertEqual(fragment["migrationReason"], "fragment-removed")
            for phrase in fragment.get("phrases", []):
                self.assertEqual(phrase["migrationReason"],
                                 "fragment-removed")
        for gate in m.relation["claimGates"]["c1"]:
            self.assertEqual(gate["migrationReason"], "fragment-removed")


class TestOwnerScopedReviewStamp(unittest.TestCase):
    def test_selected_human_review_preserves_every_unselected_owner(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy_edition_tree(tmp)
            relation_path = os.path.join(
                tmp, "navigator/relations/na__pct.json")
            with open(relation_path, encoding="utf-8") as fh:
                relation = json.load(fh)
            selected = relation["fragments"]["c1u0"]
            selected["migrationState"] = "current"
            selected.pop("migrationReason", None)
            selected["reviewState"] = "pending"
            proposal = {
                "sourceEdition": "af",
                "fragmentCorpus": "synthetic-fragments",
                "targetCorpus": "synthetic-targets",
                "owner": {"kind": "unit", "id": "c1u0"},
                "contentHash": "sha256/c1:" + ("1" * 64),
            }
            selected["proposedFrom"] = proposal
            unselected = relation["fragments"]["c1u1"]
            unselected["reviewState"] = "pending"
            unselected_before = copy.deepcopy(unselected)
            with open(relation_path, "w", encoding="utf-8") as fh:
                json.dump(relation, fh, indent=1, ensure_ascii=False)
                fh.write("\n")

            stamp_tool.stamp(
                tmp, "navigator/editions/na.json", mark_reviewed=True,
                owners=["unit:c1u0"], reviewer="Test Reviewer",
                review_date="2026-07-22", operator_kind="human")

            with open(relation_path, encoding="utf-8") as fh:
                stamped = json.load(fh)
            reviewed = stamped["fragments"]["c1u0"]
            self.assertEqual(reviewed["reviewState"], "internally-reviewed")
            self.assertEqual(reviewed["review"]["by"], "Test Reviewer")
            self.assertEqual(reviewed["review"]["operatorKind"], "human")
            self.assertEqual(reviewed["proposedFrom"], proposal)
            self.assertEqual(stamped["fragments"]["c1u1"],
                             unselected_before)

            # Recording a local operator review neither deletes provenance nor
            # pretends to authenticate its source edition.  Until the
            # pair-scoped verifier exists, the shared release predicate must
            # still fail closed on the preserved proposal.
            boot = gateway.ContentGateway(tmp)
            edition_path = "navigator/editions/na.json"
            config = json.loads(boot.read_text(edition_path))
            content = gateway.ContentGateway(
                tmp, allowlist=config["declaredTransitiveInputs"])
            stamped_model = model.EditionModel(content, edition_path)
            release_errors = validate.validate_edition(
                stamped_model, for_release=True)
            self.assertTrue(any(
                code == "release" and "unit c1u0" in message and
                "proposedFrom cannot be release-verified" in message
                for code, message in release_errors))

    def test_implicit_pin_only_and_stale_selected_owner_are_no_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy_edition_tree(tmp)
            relation_path = os.path.join(
                tmp, "navigator/relations/na__pct.json")
            with open(relation_path, "rb") as fh:
                original = fh.read()
            with self.assertRaisesRegex(SystemExit, "pin-only"):
                stamp_tool.stamp(tmp, "navigator/editions/na.json")
            with open(relation_path, "rb") as fh:
                self.assertEqual(fh.read(), original)

            with open(relation_path, encoding="utf-8") as fh:
                relation = json.load(fh)
            owner = relation["fragments"]["c1u0"]
            owner["migrationState"] = "stale"
            owner["migrationReason"] = "endpoint-changed"
            with open(relation_path, "w", encoding="utf-8") as fh:
                json.dump(relation, fh, indent=1, ensure_ascii=False)
                fh.write("\n")
            with open(relation_path, "rb") as fh:
                stale_bytes = fh.read()

            with self.assertRaisesRegex(SystemExit, "stale/non-current"):
                stamp_tool.stamp(
                    tmp, "navigator/editions/na.json", mark_reviewed=True,
                    owners=["unit:c1u0"], reviewer="Test Reviewer",
                    review_date="2026-07-22", operator_kind="human")
            with open(relation_path, "rb") as fh:
                self.assertEqual(fh.read(), stale_bytes)

    def test_authorized_metadata_and_explicit_owner_selection_are_mandatory(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy_edition_tree(tmp)
            common = (tmp, "navigator/editions/na.json")
            with self.assertRaisesRegex(SystemExit, "exactly one"):
                stamp_tool.stamp(
                    *common, mark_reviewed=True, reviewer="Test Reviewer",
                    review_date="2026-07-22", operator_kind="human")
            for kind in (None, "tool", "automation"):
                with self.subTest(kind=kind), self.assertRaisesRegex(
                        SystemExit, "explicitly 'human' or 'model'"):
                    stamp_tool.stamp(
                        *common, mark_reviewed=True, owners=["unit:c1u0"],
                        reviewer="operator", review_date="2026-07-22",
                        operator_kind=kind)
            for reviewer in (
                    "   ", "\u200b\u2060\u200e", "\u200bReviewer",
                    "Reviewer\u2060", " Reviewer", "Reviewer ",
                    "re\u0301viewer"):
                with self.subTest(reviewer=reviewer), \
                        self.assertRaisesRegex(
                            SystemExit, "non-empty --reviewer"):
                    stamp_tool.stamp(
                        *common, mark_reviewed=True, owners=["unit:c1u0"],
                        reviewer=reviewer, review_date="2026-07-22",
                        operator_kind="model")
            with self.assertRaisesRegex(SystemExit, "real YYYY-MM-DD"):
                stamp_tool.stamp(
                    *common, mark_reviewed=True, owners=["unit:c1u0"],
                    reviewer="Test Reviewer", review_date="2026-02-30",
                    operator_kind="human")

    def test_model_review_stamps_explicit_run_identity_and_current_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy_edition_tree(tmp)
            relation_path = os.path.join(
                tmp, "navigator/relations/na__pct.json")
            with open(relation_path, encoding="utf-8") as fh:
                relation = json.load(fh)
            fields = relation["fragments"]["c1u0"]
            fields["migrationState"] = "current"
            fields.pop("migrationReason", None)
            with open(relation_path, "w", encoding="utf-8") as fh:
                json.dump(relation, fh, indent=1, ensure_ascii=False)
                fh.write("\n")

            identity = "codex:gpt-5.6:run-authority-stamp"
            stamp_tool.stamp(
                tmp, "navigator/editions/na.json", mark_reviewed=True,
                owners=["unit:c1u0"], reviewer=identity,
                review_date="2026-07-22", operator_kind="model")

            stamped_model = load_model_from_root(
                tmp, "navigator/editions/na.json")
            reviewed = stamped_model.relation["fragments"]["c1u0"]
            self.assertEqual(reviewed["review"]["by"], identity)
            self.assertEqual(reviewed["review"]["operatorKind"], "model")
            self.assertEqual(reviewed["review"]["date"], "2026-07-22")
            self.assertEqual(
                reviewed["review"]["contentHash"],
                stamped_model.content_hash(
                    stamped_model.unit_projection("c1u0", reviewed)))


if __name__ == "__main__":
    unittest.main()
