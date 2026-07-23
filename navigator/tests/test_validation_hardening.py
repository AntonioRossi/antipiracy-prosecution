"""Focused negative tests for schema/model validation boundaries.

These tests mutate an already-loaded edition model in memory.  They do not
rewrite reviewed source data, and each assertion names the invariant that
must fail closed.
"""

import copy
import glob
import json
import os
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import build as build_mod  # noqa: E402
from lib import authority, canon, currentstate, gateway, model, \
    pinplan, schema_validate, segmenter, validate  # noqa: E402


HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))


def load_model(edition="na"):
    path = "navigator/editions/%s.json" % edition
    bootstrap = gateway.ContentGateway(ROOT)
    config = json.loads(bootstrap.read_text(path))
    gw = gateway.ContentGateway(
        ROOT, allowlist=config["declaredTransitiveInputs"])
    return model.EditionModel(gw, path)


class ValidationHardening(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = load_model("na")

    def clone(self):
        """Copy only authored mutable documents; parsed corpus state is shared."""
        m = copy.copy(self.base)
        m.edition = copy.deepcopy(self.base.edition)
        m.relation = copy.deepcopy(self.base.relation)
        m.binding = m.relation["binding"]
        m.gates = copy.deepcopy(self.base.gates)
        m.gates_by_id = {g["gateId"]: g for g in m.gates["gates"]}
        m.deps = copy.deepcopy(self.base.deps)
        m.strings = copy.deepcopy(self.base.strings)
        m.api_policy = copy.deepcopy(self.base.api_policy)
        m.support_matrix = copy.deepcopy(self.base.support_matrix)
        m.claim_profile = copy.deepcopy(self.base.claim_profile)
        m.target_profile = copy.deepcopy(self.base.target_profile)
        m.schemas = copy.deepcopy(self.base.schemas)
        relation_schema = m.schemas["relation"]
        m.review_schemas = {
            "binding": relation_schema["properties"]["binding"],
            "unit": next(iter(relation_schema["properties"]["fragments"]
                              ["patternProperties"].values())),
            "phrase": relation_schema["definitions"]["phrase"],
            "target": relation_schema["definitions"]["target"],
            "claim-gate": next(iter(
                relation_schema["properties"]["claimGates"]
                ["patternProperties"].values()))["items"],
            "disposition": relation_schema["properties"]["dispositions"]
            ["items"],
        }
        return m

    @staticmethod
    def messages(m, code):
        return [message for got_code, message in validate.validate_edition(m)
                if got_code == code]

    @staticmethod
    def source_caution(m, entry):
        return {
            "gateId": entry["gateId"],
            "type": "source-gate",
            "code": entry["code"],
            "source": {
                "corpus": m.edition["claimCorpus"],
                "block": entry["source"]["block"],
                "textHash": entry["source"]["textHash"],
            },
        }

    def gate(self, m, scope):
        return next(g for g in m.gates["gates"]
                    if g["requiredScope"] == scope)

    def test_edition_schema_is_checked_before_path_selectors_are_used(self):
        with tempfile.TemporaryDirectory() as root:
            schema_dir = os.path.join(root, "navigator", "schema")
            edition_dir = os.path.join(root, "navigator", "editions")
            os.makedirs(schema_dir)
            os.makedirs(edition_dir)
            with open(os.path.join(
                    ROOT, "navigator", "schema", "edition.schema.json"),
                      "rb") as source:
                schema_bytes = source.read()
            with open(os.path.join(schema_dir, "edition.schema.json"),
                      "wb") as destination:
                destination.write(schema_bytes)
            with open(os.path.join(edition_dir, "bad.json"), "w",
                      encoding="utf-8") as destination:
                json.dump({"editionVersion": "1"}, destination)
            with self.assertRaisesRegex(
                    model.ModelError, "invalid edition config"):
                model.EditionModel(
                    gateway.ContentGateway(root),
                    "navigator/editions/bad.json")

    def test_profile_documents_are_bound_to_edition_corpora(self):
        for attr, label in (
            ("claim_profile", "claim segmentation profile"),
            ("target_profile", "target segmentation profile"),
            ("gates", "gate inventory"),
            ("deps", "dependency map"),
        ):
            with self.subTest(attr=attr):
                m = self.clone()
                getattr(m, attr)["corpusId"] = "wrong-corpus"
                if attr == "gates":
                    m.gates_by_id = {
                        g["gateId"]: g for g in m.gates["gates"]}
                self.assertTrue(any(label in message for message in
                                    self.messages(m, "binding")))

    def test_rendered_corpora_require_rendered_visibility_and_roles(self):
        for field in ("claimCorpus", "targetCorpus"):
            with self.subTest(field=field):
                m = self.clone()
                m.registry = copy.copy(self.base.registry)
                m.registry.corpora = copy.deepcopy(
                    self.base.registry.corpora)
                corpus_id = m.edition[field]
                m.registry.corpora[corpus_id]["visibility"] = "internal"
                self.assertTrue(any(field in message for message in
                                    self.messages(m, "binding")))

    def test_anchor_and_pct_claim_identities_cannot_collapse(self):
        block = copy.deepcopy(self.base.target_blocks[0])
        with self.assertRaisesRegex(model.ModelError, "duplicate anchor"):
            model._anchor_index([block, copy.deepcopy(block)])

        m = self.clone()
        m.target_blocks = list(self.base.target_blocks)
        last_index = max(
            index for index, target in enumerate(m.target_blocks)
            if target.kind == "claim-whole")
        replacement = copy.copy(m.target_blocks[last_index])
        replacement.meta = copy.deepcopy(replacement.meta)
        replacement.meta["pctClaim"] = 17
        m.target_blocks[last_index] = replacement
        self.assertTrue(any("exactly 1..18" in message for message in
                            self.messages(m, "census")))

    def test_inventory_identity_and_applicability_duplicates_fail(self):
        m = self.clone()
        m.gates["gates"].append(copy.deepcopy(m.gates["gates"][0]))
        self.assertTrue(any("gateId" in message for message in
                            self.messages(m, "duplicate")))

        for scope, collection, identity, hash_field in (
            ("target", "fragments", "id", "hash"),
            ("claim", "claims", "claim", "claimHash"),
        ):
            with self.subTest(scope=scope):
                m = self.clone()
                entry = self.gate(m, scope)
                first = copy.deepcopy(entry["appliesTo"][collection][0])
                first[hash_field] = "sha256/c1:" + "0" * 64
                entry["appliesTo"][collection].append(first)
                self.assertTrue(any("duplicate applicability subject" in msg
                                    for msg in self.messages(m, "duplicate")))

    def test_target_cardinality_is_strictly_positive(self):
        m = self.clone()
        entry = self.gate(m, "target")
        entry["appliesTo"]["cardinality"]["minTargetsPerFragment"] = 0
        errors = validate.validate_edition(m)
        self.assertTrue(any(code == "schema:gates" and "minimum 1" in msg
                            for code, msg in errors))
        self.assertTrue(any(code == "inventory" and "integer >= 1" in msg
                            for code, msg in errors))

    def test_source_gate_must_apply_to_claim_owner(self):
        m = self.clone()
        entry = self.gate(m, "claim")
        listed = {"c%d" % row["claim"]
                  for row in entry["appliesTo"]["claims"]}
        claim_key = next("c%d" % number for number in m.claims_by_number
                         if "c%d" % number not in listed)
        assignment = copy.deepcopy(next(iter(
            m.relation["claimGates"].values()))[0])
        assignment.update(
            gateId=entry["gateId"], code=entry["code"],
            claimHash=m.agg_hashes[int(claim_key[1:])],
            source={
                "corpus": m.edition["claimCorpus"],
                "block": entry["source"]["block"],
                "textHash": entry["source"]["textHash"],
            })
        m.relation["claimGates"].setdefault(claim_key, []).append(assignment)
        self.assertTrue(any("not applicable to %s" % claim_key in msg
                            for msg in self.messages(m, "caution")))

    def test_source_gate_must_apply_to_fragment_owner(self):
        m = self.clone()
        entry = self.gate(m, "fragment")
        listed = {row["id"] for row in entry["appliesTo"]["fragments"]}
        fragment_id = next(fid for fid in m.relation["fragments"]
                           if fid not in listed)
        m.relation["fragments"][fragment_id]["caution"] = \
            self.source_caution(m, entry)
        self.assertTrue(any("not applicable to %s" % fragment_id in msg
                            for msg in self.messages(m, "caution")))

    def test_source_gate_must_apply_to_target_owner(self):
        m = self.clone()
        entry = self.gate(m, "target")
        listed = {row["id"] for row in entry["appliesTo"]["fragments"]}
        fragment_id, fragment = next(
            (fid, frag) for fid, frag in m.relation["fragments"].items()
            if fid not in listed and frag.get("targets"))
        fragment["targets"][0]["caution"] = self.source_caution(m, entry)
        self.assertTrue(any("not applicable to %s" % fragment_id in msg
                            for msg in self.messages(m, "caution")))

    def test_documented_no_candidate_fallback_is_the_only_scope_exception(self):
        m = self.clone()
        entry = self.gate(m, "target")
        fragment_id = entry["appliesTo"]["fragments"][0]["id"]
        fragment = m.relation["fragments"][fragment_id]
        fragment["status"] = "counsel-review-required"
        fragment.pop("targets", None)
        fragment["caution"] = self.source_caution(m, entry)
        disposition = next(
            d for d in m.relation["dispositions"]
            if d["gateId"] == entry["gateId"] and
            d["subject"]["id"] == fragment_id)
        disposition["disposition"] = "carried-at-fragment-fallback"

        errors = validate.validate_edition(m)
        relevant = [(code, msg) for code, msg in errors
                    if code in ("caution", "disposition", "integrity") and
                    (entry["gateId"] in msg or fragment_id in msg)]
        self.assertEqual(relevant, [])

        fragment["status"] = "mapped"
        self.assertTrue(any("carried at fragment scope" in msg for msg in
                            self.messages(m, "caution")))

    def test_optional_affirmative_disposition_requires_carried_evidence(self):
        for scope in ("claim", "fragment", "target"):
            with self.subTest(scope=scope):
                m = self.clone()
                entry = self.gate(m, scope)
                entry["requirement"] = "optional"
                disposition = next(
                    item for item in m.relation["dispositions"]
                    if item["gateId"] == entry["gateId"] and
                    item["disposition"] == "carried-at-required-scope")
                subject_id = disposition["subject"]["id"]
                self.assertFalse(any(
                    entry["gateId"] in message and
                    "optional gate has affirmative" in message
                    for message in self.messages(m, "integrity")))
                removed = 0
                if scope == "claim":
                    gates = m.relation["claimGates"][subject_id]
                    kept = [gate for gate in gates
                            if gate.get("gateId") != entry["gateId"]]
                    removed = len(gates) - len(kept)
                    m.relation["claimGates"][subject_id] = kept
                elif scope == "fragment":
                    fragment = m.relation["fragments"][subject_id]
                    if fragment.get("caution", {}).get("gateId") == \
                            entry["gateId"]:
                        fragment.pop("caution")
                        removed = 1
                else:
                    fragment = m.relation["fragments"][subject_id]
                    targets = list(fragment.get("targets", []))
                    for phrase in fragment.get("phrases", []):
                        targets.extend(phrase.get("targets", []))
                    for target in targets:
                        if target.get("caution", {}).get("gateId") == \
                                entry["gateId"]:
                            target.pop("caution")
                            removed += 1
                self.assertGreater(removed, 0, entry["gateId"])
                messages = self.messages(m, "integrity")
                self.assertTrue(any(
                    entry["gateId"] in message and
                    "optional gate has affirmative" in message
                    for message in messages), messages)

    def test_optional_fallback_disposition_requires_fragment_caution(self):
        m = self.clone()
        entry = self.gate(m, "target")
        entry["requirement"] = "optional"
        disposition = next(
            item for item in m.relation["dispositions"]
            if item["gateId"] == entry["gateId"])
        fragment_id = disposition["subject"]["id"]
        fragment = m.relation["fragments"][fragment_id]
        fragment["status"] = "counsel-review-required"
        fragment.pop("targets", None)
        for phrase in fragment.get("phrases", []):
            phrase.pop("targets", None)
        fragment["caution"] = self.source_caution(m, entry)
        disposition["disposition"] = "carried-at-fragment-fallback"
        self.assertFalse(any(
            entry["gateId"] in message and
            "optional gate has affirmative" in message
            for message in self.messages(m, "integrity")))

        fragment.pop("caution")
        self.assertTrue(any(
            entry["gateId"] in message and
            "optional gate has affirmative" in message
            for message in self.messages(m, "integrity")))

    def test_optional_target_disposition_enforces_declared_cardinality(self):
        m = self.clone()
        entry = self.gate(m, "target")
        entry["requirement"] = "optional"
        disposition = next(
            item for item in m.relation["dispositions"]
            if item["gateId"] == entry["gateId"] and
            item["disposition"] == "carried-at-required-scope")
        fragment = m.relation["fragments"][disposition["subject"]["id"]]
        targets = list(fragment.get("targets", []))
        for phrase in fragment.get("phrases", []):
            targets.extend(phrase.get("targets", []))
        actual = len({
            target["block"] for target in targets
            if target.get("caution", {}).get("gateId") == entry["gateId"]
        })
        self.assertEqual(actual, 1)
        entry["appliesTo"]["cardinality"]["minTargetsPerFragment"] = \
            2
        messages = self.messages(m, "integrity")
        self.assertTrue(any(
            entry["gateId"] in message and
            "1 matching target(s), requires at least 2" in message
            for message in messages), messages)

    def test_declared_inputs_reject_duplicates_and_unsafe_aliases(self):
        mutations = (
            lambda values: values.append(values[0]),
            lambda values: values.append("../outside.json"),
            lambda values: values.append(
                "navigator/schema/../schema/relation.schema.json"),
            lambda values: values.append("navigator\\schema\\unsafe.json"),
            lambda values: values.append("/absolute/input.json"),
        )
        for mutate in mutations:
            with self.subTest(mutation=mutate.__code__.co_firstlineno):
                m = self.clone()
                mutate(m.edition["declaredTransitiveInputs"])
                self.assertTrue(self.messages(m, "inputs"))

    def test_edition_release_timestamp_is_real_and_canonical(self):
        for invalid in ("2026-7-2T0:0:0Z", "2026-02-30T00:00:00Z"):
            with self.subTest(invalid=invalid):
                m = self.clone()
                m.edition["declaredReleaseTimestamp"] = invalid
                self.assertTrue(self.messages(m, "edition"))

    def test_api_policy_is_closed_and_normative(self):
        mutations = (
            lambda policy: policy.update(unexpected=True),
            lambda policy: policy.update(csp="default-src *"),
            lambda policy: policy["apis"]["indexedDB.open"].update(
                **{"class": "probe"}),
            lambda policy: policy["apis"]["indexedDB.open"].pop(
                "instrument"),
            lambda policy: policy["apis"]["location.assign"].update(
                instrument="obsolete"),
            lambda policy: policy["apis"].pop("document.cookie"),
            lambda policy: policy["apis"]["history.pushState"].update(
                **{"class": "procedural", "note": "skip"}),
            lambda policy: policy["apis"].update({
                "totally.fake": {
                    "class": "csp-governed", "instrument": "network"}}),
        )
        for mutate in mutations:
            with self.subTest(mutation=mutate.__code__.co_firstlineno):
                m = self.clone()
                mutate(m.api_policy)
                self.assertTrue(self.messages(m, "api-policy"))

    def test_lifecycle_reason_and_nonempty_review_fields(self):
        fragment_id = next(iter(self.base.relation["fragments"]))

        m = self.clone()
        m.relation["fragments"][fragment_id]["migrationState"] = "current"
        m.relation["fragments"][fragment_id]["migrationReason"] = "changed"
        self.assertTrue(any("current owner forbids migrationReason" in msg
                            for msg in self.messages(m, "lifecycle")))

        m = self.clone()
        fragment = m.relation["fragments"][fragment_id]
        fragment["migrationState"] = "stale"
        fragment.pop("migrationReason", None)
        self.assertTrue(any("stale owner requires migrationReason" in msg
                            for msg in self.messages(m, "lifecycle")))

        for field, value in (("by", "   "), ("date", "")):
            with self.subTest(review_field=field):
                m = self.clone()
                m.relation["fragments"][fragment_id]["review"][field] = value
                self.assertTrue(any("review.%s must be non-empty" % field
                                    in msg for msg in
                                    self.messages(m, "lifecycle")))

        for invalid_date in ("2026-7-2", "2026-02-30", "not-a-date"):
            with self.subTest(review_date=invalid_date):
                m = self.clone()
                m.relation["fragments"][fragment_id]["review"]["date"] = \
                    invalid_date
                self.assertTrue(any("real canonical YYYY-MM-DD" in msg
                                    for msg in
                                    self.messages(m, "lifecycle")))

    def test_operator_authorization_matrix_is_explicit_and_fail_closed(self):
        self.assertEqual(
            authority.AUTHORITATIVE_OPERATOR_KINDS,
            frozenset(("human", "model")))
        for kind in ("human", "model"):
            with self.subTest(kind=kind):
                self.assertTrue(authority.is_authoritative_operator_kind(kind))
                self.assertTrue(authority.is_authoritative_operator(
                    kind, "codex:model:run-123"))
        for kind in ("tool", None, "automation", 1, [], {}):
            with self.subTest(kind=kind):
                self.assertFalse(
                    authority.is_authoritative_operator_kind(kind))
                self.assertFalse(authority.is_authoritative_operator(
                    kind, "identified"))
        for identity in (
                None, "", "   ", "\u200b", "\u2060", "\u200e",
                "\u200b\u2060\u200e", "\ufe0f",
                "\u200bcodex:model:run-hidden", "codex:model:run\u2060",
                " codex:model:run", "codex:model:run ",
                "codex:\x00model:run", "re\u0301viewer", 7, [], {}):
            with self.subTest(identity=identity):
                self.assertFalse(authority.is_authoritative_operator(
                    "model", identity))
                self.assertFalse(
                    authority.is_identified_operator_identity(identity))
        for identity in (
                "reviewer@example.test",
                "codex:gpt-5.6-sol:run-authority-matrix",
                "QA Reviewer 42", "r\u00e9viewer"):
            with self.subTest(visible_identity=identity):
                self.assertTrue(authority.is_authoritative_operator(
                    "model", identity))
                self.assertTrue(authority.operator_identity_matches(
                    identity, identity))

    def test_final_evidence_language_is_shared_and_fail_closed(self):
        for evidence in (
                "Required review passed with no errors",
                "All current hashes and results were verified"):
            with self.subTest(final=evidence):
                self.assertTrue(authority.is_final_evidence_text(evidence))
        for evidence in (
                None, "", "   ", "\u200b\u2060\u200e",
                "Review failed; do not release",
                "Failure found in the current candidate",
                "Checks did not pass on Safari",
                "Unable to complete the review",
                "The candidate was rejected",
                "A rejection was recorded",
                "Required checks were skipped",
                "Do-not-release this candidate",
                "Review pending"):
            with self.subTest(nonfinal=evidence):
                self.assertFalse(authority.is_final_evidence_text(evidence))

    def test_owner_validation_accepts_current_human_or_model_review(self):
        fragment_id = next(iter(self.base.relation["fragments"]))
        for kind, identity in (
                ("human", "reviewer@example.test"),
                ("model", "codex:gpt-5.6:run-authority-matrix")):
            with self.subTest(kind=kind):
                m = self.clone()
                fields = m.relation["fragments"][fragment_id]
                fields["reviewState"] = "internally-reviewed"
                fields["migrationState"] = "current"
                fields.pop("migrationReason", None)
                fields["review"].update({
                    "by": identity,
                    "operatorKind": kind,
                    "date": "2026-07-22",
                })
                fields["review"]["contentHash"] = m.content_hash(
                    m.unit_projection(fragment_id, fields))
                owner_prefix = "unit %s:" % fragment_id
                errors = validate.validate_edition(m, for_release=True)
                self.assertFalse([
                    (code, message) for code, message in errors
                    if owner_prefix in message and code in {
                        "lifecycle", "pending", "content-hash", "release"}
                ])

    def test_owner_validation_rejects_unauthorized_or_unidentified_review(self):
        fragment_id = next(iter(self.base.relation["fragments"]))
        mutations = (
            ("tool", "migration-tool"),
            (None, "missing-kind"),
            ("automation", "unknown-kind"),
            ("model", "   "),
            ("model", "\u200b\u2060\u200e"),
            ("human", None),
        )
        for kind, identity in mutations:
            with self.subTest(kind=kind, identity=identity):
                m = self.clone()
                fields = m.relation["fragments"][fragment_id]
                fields["reviewState"] = "internally-reviewed"
                fields["migrationState"] = "current"
                fields.pop("migrationReason", None)
                if kind is None:
                    fields["review"].pop("operatorKind", None)
                else:
                    fields["review"]["operatorKind"] = kind
                if identity is None:
                    fields["review"].pop("by", None)
                else:
                    fields["review"]["by"] = identity
                fields["review"]["date"] = "2026-07-22"
                fields["review"]["contentHash"] = m.content_hash(
                    m.unit_projection(fragment_id, fields))
                owner_prefix = "unit %s:" % fragment_id
                errors = validate.validate_edition(m, for_release=True)
                self.assertTrue(any(
                    code == "release" and owner_prefix in message and
                    ("operatorKind" in message or "review.by" in message)
                    for code, message in errors), errors)

    def test_owner_validation_rejects_stale_model_content_hash(self):
        fragment_id = next(iter(self.base.relation["fragments"]))
        m = self.clone()
        fields = m.relation["fragments"][fragment_id]
        fields["reviewState"] = "internally-reviewed"
        fields["migrationState"] = "current"
        fields.pop("migrationReason", None)
        fields["review"].update({
            "by": "codex:gpt-5.6:run-stale",
            "operatorKind": "model",
            "date": "2026-07-22",
            "contentHash": "sha256/c1:" + "0" * 64,
        })
        errors = validate.validate_edition(m, for_release=True)
        self.assertTrue(any(
            code == "content-hash" and "unit %s:" % fragment_id in message
            for code, message in errors), errors)

    def test_phrase_text_must_be_nonempty(self):
        m = self.clone()
        phrase = next(
            phrase
            for fragment in m.relation["fragments"].values()
            for phrase in fragment.get("phrases", []))
        phrase["text"] = ""
        errors = validate.validate_edition(m)
        self.assertTrue(any(code == "schema:relation" and "minLength 1" in msg
                            for code, msg in errors))
        self.assertTrue(any(code == "phrase" and "must be non-empty" in msg
                            for code, msg in errors))

    def test_migration_snapshots_and_reuse_provenance_are_closed(self):
        schema = self.base.schemas["relation"]
        relation = copy.deepcopy(self.base.relation)
        fragment = next(f for f in relation["fragments"].values()
                        if f.get("targets"))
        fragment["previousTargets"] = [copy.deepcopy(fragment["targets"][0])]
        fragment["proposedFrom"] = {
            "sourceEdition": "af",
            "fragmentCorpus": "af-claims",
            "targetCorpus": "pct-disclosure",
            "owner": {"kind": "unit", "id": "c1u0"},
            "contentHash": "sha256/c1:" + "0" * 64,
        }
        self.assertEqual(schema_validate.validate(relation, schema), [])

        m = self.clone()
        current = next(f for f in m.relation["fragments"].values()
                       if f.get("targets"))
        current["proposedFrom"] = copy.deepcopy(fragment["proposedFrom"])
        current["reviewState"] = "internally-reviewed"
        # A well-shaped proposal is valid authoring data and need not remain
        # in the pending authoring state after local human review.
        self.assertFalse(any("proposedFrom" in msg for msg in
                             self.messages(m, "lifecycle")))
        self.assertTrue(any(
            code == "release" and
            "proposedFrom cannot be release-verified" in message
            for code, message in validate.validate_edition(
                m, for_release=True)))

        bad_snapshot = copy.deepcopy(relation)
        snap_fragment = next(f for f in bad_snapshot["fragments"].values()
                             if "previousTargets" in f)
        snap_fragment["previousTargets"][0]["undeclared"] = True
        self.assertTrue(any("unexpected field 'undeclared'" in msg for msg in
                            schema_validate.validate(bad_snapshot, schema)))

        bad_provenance = copy.deepcopy(relation)
        provenance_fragment = next(
            f for f in bad_provenance["fragments"].values()
            if "proposedFrom" in f)
        provenance_fragment["proposedFrom"]["owner"]["undeclared"] = True
        self.assertTrue(any("unexpected field 'undeclared'" in msg for msg in
                            schema_validate.validate(bad_provenance, schema)))

        for label, mutate in (
            ("digest", lambda p: p.__setitem__(
                "contentHash", "sha256/c1:" + "0" * 63)),
            ("edition id", lambda p: p.__setitem__(
                "sourceEdition", "../af")),
            ("corpus id", lambda p: p.__setitem__(
                "fragmentCorpus", "AF claims")),
            ("owner id", lambda p: p["owner"].__setitem__(
                "id", "unit-one")),
        ):
            with self.subTest(label=label):
                malformed = copy.deepcopy(relation)
                malformed_fragment = next(
                    f for f in malformed["fragments"].values()
                    if "proposedFrom" in f)
                mutate(malformed_fragment["proposedFrom"])
                self.assertTrue(any(
                    "does not match pattern" in message for message in
                    schema_validate.validate(malformed, schema)))

        mismatched = self.clone()
        mismatched_fragment = next(
            f for f in mismatched.relation["fragments"].values()
            if f.get("targets"))
        mismatched_fragment["proposedFrom"] = copy.deepcopy(
            fragment["proposedFrom"])
        mismatched_fragment["proposedFrom"]["owner"] = {
            "kind": "phrase", "id": "c1u0",
        }
        self.assertTrue(any(
            "does not match kind 'phrase'" in message for message in
            self.messages(mismatched, "provenance")))

        same_edition = self.clone()
        same_fragment = next(
            f for f in same_edition.relation["fragments"].values()
            if f.get("targets"))
        same_fragment["proposedFrom"] = copy.deepcopy(
            fragment["proposedFrom"])
        same_fragment["proposedFrom"]["sourceEdition"] = "na"
        self.assertTrue(any(
            "must differ from the destination edition" in message
            for message in self.messages(same_edition, "provenance")))

    def test_review_axis_tags_control_owner_projection(self):
        schema = copy.deepcopy(self.base.schemas["relation"])
        unit_schema = next(iter(schema["properties"]["fragments"]
                                ["patternProperties"].values()))
        fragment = self.base.relation["fragments"]["c1u0"]
        projection = schema_validate.review_axis(
            unit_schema, fragment, root=schema)
        self.assertIn("status", projection)
        self.assertIn("fragmentTextHash", projection)
        self.assertNotIn("reviewState", projection)
        self.assertNotIn("migrationState", projection)
        self.assertNotIn("review", projection)
        self.assertNotIn("block", projection["targets"][0])
        self.assertIn("textHash", projection["targets"][0])

        # Both changes remain legal on the inter-axis matrix (ship:never),
        # and the generic projection follows x-review rather than a field
        # name allow/deny list.
        unit_schema["properties"]["reviewState"]["x-review"] = "include"
        unit_schema["properties"]["fragmentTextHash"]["x-review"] = "exclude"
        schema_validate.check_axes(schema)
        changed = schema_validate.review_axis(
            unit_schema, fragment, root=schema)
        self.assertIn("reviewState", changed)
        self.assertNotIn("fragmentTextHash", changed)

    def test_lifecycle_schema_enums_are_bound_to_invariants(self):
        m = self.clone()
        m.schemas["relation"]["definitions"]["review"]["properties"] \
            ["operatorKind"]["enum"] = ["human", "model"]
        self.assertTrue(any("operatorKind enum drifts" in message
                            for message in self.messages(m, "schema:axes")))

        m = self.clone()
        phrase = m.schemas["relation"]["definitions"]["phrase"]
        phrase["properties"].pop("reviewState")
        self.assertTrue(any("phrase lifecycle applicability" in message
                            for message in self.messages(m, "schema:axes")))

    def test_actual_owner_projection_obeys_schema_boundaries_and_axes(self):
        m = self.clone()
        fragment = m.relation["fragments"]["c1u0"]
        projection = m.unit_projection("c1u0", fragment)
        self.assertNotIn("phrases", projection)
        phrases_schema = m.review_schemas["unit"]["properties"]["phrases"]
        self.assertIs(phrases_schema["x-reviewOwnerBoundary"], True)

        targets_schema = m.review_schemas["unit"]["properties"]["targets"]
        targets_schema["x-ship"] = "never"
        targets_schema["x-review"] = "exclude"
        schema_validate.check_axes(m.schemas["relation"])
        changed = m.unit_projection("c1u0", fragment)
        self.assertNotIn("targets", changed)

    def test_forbidden_terms_cover_microcopy_and_edition_labels(self):
        term = "forbidden synthetic phrase"

        m = self.clone()
        m.edition["forbiddenTerms"] = [term]
        m.strings["ui"]["aboutTitle"] = term
        errors = validate.validate_edition(m)
        self.assertTrue(any(code == "forbidden-terms" and
                            "strings.ui.aboutTitle" in message
                            for code, message in errors))

        m = self.clone()
        m.edition["forbiddenTerms"] = [term]
        m.edition["displayName"] = term
        errors = validate.validate_edition(m)
        self.assertTrue(any(code == "forbidden-terms" and
                            "displayName" in message
                            for code, message in errors))

    def test_forbidden_terms_ignore_unselected_edition_strings(self):
        term = "forbidden synthetic phrase"
        m = self.clone()
        m.edition["forbiddenTerms"] = [term]
        m.strings["editionNamespaces"]["other-edition"] = {
            "sourceGateCodes": {"other-gate": term},
        }
        errors = validate.validate_edition(m)
        self.assertFalse(any(
            code == "forbidden-terms" and "other-edition" in message
            for code, message in errors))

    def test_support_matrix_is_closed_and_structurally_typed(self):
        self.assertEqual(schema_validate.validate(
            self.base.support_matrix,
            self.base.schemas["support-matrix"]), [])
        mutations = (
            lambda matrix: matrix.update({"undeclared": True}),
            lambda matrix: matrix.update({"targets": []}),
            lambda matrix: matrix["targets"][0].update(
                {"browzer": matrix["targets"][0].pop("browser")}),
            lambda matrix: matrix["viewport"].update(
                {"minimum": [1280]}),
            lambda matrix: matrix["viewport"].update(
                {"minimum": [1280, 720, 1]}),
            lambda matrix: matrix["viewport"].update(
                {"minimum": [1024, 600]}),
            lambda matrix: matrix["viewport"].update(
                {"stackedBelowMinimum": False}),
            lambda matrix: matrix["targets"][0].update(
                {"at": "VoiceOver"}),
            lambda matrix: matrix["targets"][0].update(
                {"at": " voiceover "}),
            lambda matrix: matrix["targets"][0].update(
                {"at": "Apple VoiceOver 2026"}),
            lambda matrix: matrix["targets"][0].update(
                {"at": "Voice Over"}),
            lambda matrix: matrix["targets"][0].update(
                {"at": "VOICE-OVER"}),
            lambda matrix: matrix["targets"][0].update(
                {"at": "voice_over"}),
            lambda matrix: matrix["targets"][0].update(
                {"at": "None"}),
            lambda matrix: matrix["targets"][0].update(
                {"at": "no AT"}),
            lambda matrix: matrix["targets"][0].update(
                {"at": " none "}),
            lambda matrix: matrix["targets"][0].update(
                {"os": "macOS 13+ / Windows 11"}),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                m = self.clone()
                mutate(m.support_matrix)
                self.assertTrue(
                    self.messages(m, "schema:support-matrix"),
                    m.support_matrix)

    def test_schema_documents_reject_silent_or_open_constraints(self):
        mutations = (
            lambda schema: schema.update({"minLenght": 1}),
            lambda schema: schema.update({"schemaVersion": "2"}),
            lambda schema: schema.update({"additionalProperties": True}),
            lambda schema: schema["properties"]["targets"]["items"].update(
                {"unsupportedConstraint": True}),
        )
        for mutate in mutations:
            with self.subTest(mutation=mutate.__code__.co_firstlineno):
                m = self.clone()
                schema = m.schemas["support-matrix"]
                mutate(schema)
                self.assertTrue(
                    self.messages(m, "schema:support-matrix"), schema)

    def test_segmentation_profile_policy_is_closed_and_fail_safe(self):
        schema = self.base.schemas["segmentation-profile"]
        mutations = (
            lambda profile: profile.update({"profileVersion": "999"}),
            lambda profile: profile.update({"unknownPolicy": True}),
            lambda profile: profile["rules"][0].update(
                {"class": "exclued"}),
            lambda profile: profile["rules"][0].update(
                {"unknownRuleField": True}),
            lambda profile: profile["rules"][0].update({"match": {}}),
        )
        for mutate in mutations:
            with self.subTest(mutation=mutate.__code__.co_firstlineno):
                profile = copy.deepcopy(self.base.target_profile)
                mutate(profile)
                problems = schema_validate.validate(profile, schema)
                problems.extend(segmenter.profile_problems(
                    profile, self.base.edition["targetCorpus"]))
                self.assertTrue(problems, profile)
                with self.assertRaises(segmenter.SegmentError):
                    segmenter.segment("# heading\n\nsecret", profile,
                                      lambda path: b"")

    def test_target_uniqueness_is_scoped_to_each_reviewed_owner(self):
        m = self.clone()
        fragment = next(
            fragment for fragment in m.relation["fragments"].values()
            if fragment.get("targets") and fragment.get("phrases"))
        phrase = fragment["phrases"][0]
        phrase["status"] = "mapped"
        target = copy.deepcopy(fragment["targets"][0])
        phrase["targets"] = [target, copy.deepcopy(target)]
        errors = validate.validate_edition(m)
        self.assertTrue(any(code == "duplicate" and
                            "duplicate target block" in message
                            for code, message in errors))


# Registered check for every top-level "*Version" key in the enumerated
# versioned JSON formats.  "sentinel" entries are enforced fail-closed
# through canon.require_version by the named consumer; "enum" entries are
# pinned by the closed schema's enum; "live" entries are edition data values
# (document versions bound by QA versionBindings), not format versions.
VERSION_KEY_CHECKS = {
    "acceptanceVersion": ("sentinel", "3", "acceptance.validate_registry"),
    "apiPolicyVersion": ("sentinel", "1", "render.api_policy_problems"),
    "bundleVersion": ("sentinel", "3", "bundlezip.validate_bundle_config"),
    "depsVersion": ("enum", "1", "navigator/schema/deps.schema.json"),
    "editionVersion": ("enum", "2", "navigator/schema/edition.schema.json"),
    "inventoryVersion": ("enum", "1", "navigator/schema/gates.schema.json"),
    "manifestVersion": ("sentinel", "3", "currentstate.bundle_manifest_input"),
    "planesVersion": ("sentinel", "1", "build.load_planes"),
    "profileVersion": ("sentinel", "1", "segmenter.profile_problems"),
    "qaRegistryVersion": ("sentinel", "1", "qaregistry.QaRegistry"),
    "registryVersion": ("sentinel", "1", "registry.Registry"),
    "releasePolicyVersion": ("sentinel", "1", "profilepolicy.validate_policy"),
    "schemaVersion": ("sentinel", "1", "schema_validate.check_schema"),
    "stringsVersion": ("sentinel", "1", "model.EditionModel strings"),
    "supportMatrixVersion": (
        "enum", "2", "navigator/schema/support-matrix.schema.json"),
    "claimSetVersion": ("live", None, "edition document version"),
}

VERSIONED_FORMAT_FILES = (
    "navigator/corpora.json",
    "navigator/bundle-manifest.json",
)
VERSIONED_FORMAT_GLOBS = (
    "navigator/schema/*.json",
    "navigator/profiles/*.json",
    "navigator/editions/*.json",
    "navigator/relations/*.json",
    "navigator/bundles/*.json",
)


class VersionRegistryWalk(unittest.TestCase):
    """The version-key inventory and its registered checks cannot drift."""

    @staticmethod
    def _format_paths():
        paths = [os.path.join(ROOT, path) for path in VERSIONED_FORMAT_FILES]
        for pattern in VERSIONED_FORMAT_GLOBS:
            paths.extend(sorted(glob.glob(os.path.join(ROOT, pattern))))
        return paths

    def test_require_version_fails_closed(self):
        self.assertEqual(
            canon.require_version({"fmtVersion": "1"}, "fmtVersion", "1"), [])
        for document in (
            {"fmtVersion": "2"},
            {"fmtVersion": 1},
            {"fmtVersion": None},
            {},
            [],
            None,
            "fmtVersion",
        ):
            with self.subTest(document=document):
                self.assertEqual(
                    canon.require_version(document, "fmtVersion", "1"),
                    ["fmtVersion must be '1'"])

    def test_every_version_key_has_a_registered_current_check(self):
        seen = {}
        for path in self._format_paths():
            rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
            with open(path, encoding="utf-8") as fh:
                document = json.load(fh)
            self.assertIsInstance(document, dict, rel)
            for key, value in document.items():
                if not key.endswith("Version"):
                    continue
                self.assertIn(
                    key, VERSION_KEY_CHECKS,
                    "%s declares %r with no registered version check"
                    % (rel, key))
                kind, expected, _consumer = VERSION_KEY_CHECKS[key]
                seen.setdefault(key, set()).add(rel)
                if kind == "live":
                    self.assertTrue(
                        isinstance(value, str) and value.strip(),
                        "%s %s must be a non-empty live version" % (rel, key))
                else:
                    self.assertEqual(
                        value, expected,
                        "%s %s is not the registered current version"
                        % (rel, key))
        self.assertEqual(
            set(seen), set(VERSION_KEY_CHECKS),
            "registered version checks drifted from the versioned formats")

    def test_enum_pinned_version_keys_are_closed_in_their_schemas(self):
        for key, (kind, expected, location) in VERSION_KEY_CHECKS.items():
            if kind != "enum":
                continue
            with self.subTest(key=key):
                with open(os.path.join(ROOT, location),
                          encoding="utf-8") as fh:
                    schema = json.load(fh)
                self.assertEqual(
                    schema["properties"][key].get("enum"), [expected], key)

    def test_load_planes_enforces_planes_version(self):
        self.assertEqual(build_mod.load_planes()["planesVersion"], "1")
        with open(os.path.join(ROOT, "navigator", "schema", "planes.json"),
                  encoding="utf-8") as fh:
            current = json.load(fh)
        mutations = (
            ("unknown", lambda doc: doc.update({"planesVersion": "2"})),
            ("missing", lambda doc: doc.pop("planesVersion")),
        )
        for label, mutate in mutations:
            with self.subTest(mutation=label):
                document = copy.deepcopy(current)
                mutate(document)
                with tempfile.TemporaryDirectory() as root:
                    schema_dir = os.path.join(root, "navigator", "schema")
                    os.makedirs(schema_dir)
                    with open(os.path.join(schema_dir, "planes.json"), "w",
                              encoding="utf-8") as fh:
                        json.dump(document, fh)
                    with mock.patch.object(build_mod, "ROOT", root):
                        with self.assertRaises(SystemExit):
                            build_mod.load_planes()

    @staticmethod
    def _closure(corpus_id, role, paths, version_fields):
        files = []
        for index, path in enumerate(paths):
            digest = canon.bytes_digest(path.encode("utf-8"))
            files.append({
                "path": path,
                "primary": index == 0,
                "pinnedDigest": digest,
                "actualDigest": digest,
                "pinCurrent": True,
            })
        closure = {
            "corpusId": corpus_id,
            "role": role,
            "primary": paths[0],
            "files": files,
            "pinCurrent": True,
            "versionCurrent": True,
        }
        closure.update(version_fields)
        return closure

    @classmethod
    def _current_pin_plan(cls):
        opaque = {"configuredVersion": "v1", "expectedVersion": "v1"}
        return {
            "planVersion": pinplan.PLAN_VERSION,
            "edition": "na",
            "claimCorpus": "na-claims",
            "targetCorpus": "pct-disclosure",
            "authorityCorpus": "pct-pdf",
            "qaSources": {"priorityMap": "na-priority-map", "crosswalk": None},
            "corpora": {
                "na-claims": cls._closure(
                    "na-claims", "fragment-source", ["claims/na.md"],
                    dict(opaque)),
                "pct-disclosure": cls._closure(
                    "pct-disclosure", "derivative",
                    ["pct/disclosure.md", "pct/figures/fig-1.png"],
                    dict(opaque)),
                "pct-pdf": cls._closure(
                    "pct-pdf", "authoritative", ["pct/rapporto.pdf"],
                    dict(opaque)),
                "na-priority-map": cls._closure(
                    "na-priority-map", "qa-source", ["qa/priority.md"],
                    {"configuredVersions": {"NA": "v1"},
                     "expectedVersions": {"NA": "v1"}}),
            },
            "documentVersion": "v1",
            "configuredCorpusVersion": "v1",
            "configuredEditionVersion": "v1",
            "census": {"claims": 1, "units": 1, "perClaim": {"1": 1}},
            "configuredCensus": {"claims": 1, "units": 1,
                                 "perClaim": {"1": 1}},
            "censusCurrent": True,
            "groups": ["g"],
            "configuredGroups": ["g"],
            "groupsCurrent": True,
            "dependencies": {"1": None},
            "configuredDependencies": {"1": None},
            "dependenciesCurrent": True,
            "independentClaims": [1],
            "configuredIndependentClaims": [1],
            "independentClaimsCurrent": True,
            "artifactName": "a.html",
            "configuredArtifactName": "a.html",
            "artifactNameCurrent": True,
        }

    def test_pin_plan_enforces_plan_version(self):
        self.assertEqual(
            currentstate._pin_plan_problems(self._current_pin_plan()), [])
        for bad in (None, "1", "2"):
            with self.subTest(planVersion=bad):
                plan = self._current_pin_plan()
                if bad is None:
                    del plan["planVersion"]
                else:
                    plan["planVersion"] = bad
                problems = currentstate._pin_plan_problems(plan)
                self.assertTrue(
                    any("planVersion" in problem for problem in problems),
                    problems)

    def test_pin_plan_schema_is_closed_and_current(self):
        with open(os.path.join(ROOT, "navigator", "schema",
                               "plan.schema.json"), encoding="utf-8") as fh:
            schema = json.load(fh)
        schema_validate.check_schema(schema)
        self.assertEqual(schema["schemaVersion"], "1")
        self.assertEqual(
            schema["properties"]["planVersion"]["enum"],
            [pinplan.PLAN_VERSION])
        self.assertEqual(
            schema_validate.validate(self._current_pin_plan(), schema), [])
        for edition in ("na", "af"):
            with self.subTest(edition=edition):
                self.assertEqual(
                    schema_validate.validate(
                        currentstate.current_pin_plan(edition), schema), [])

    def test_pin_plan_missing_declared_corpus_fails(self):
        plan = self._current_pin_plan()
        del plan["corpora"]["pct-disclosure"]
        problems = currentstate._pin_plan_problems(plan)
        self.assertTrue(
            any("corpus inventory is not exact" in problem
                for problem in problems), problems)

    def test_pin_plan_missing_declared_corpus_file_fails(self):
        plan = self._current_pin_plan()
        plan["corpora"]["pct-pdf"]["files"] = []
        problems = currentstate._pin_plan_problems(plan)
        self.assertTrue(
            any("schema" in problem for problem in problems), problems)
        self.assertTrue(
            any("has no files" in problem for problem in problems), problems)


if __name__ == "__main__":
    unittest.main()
