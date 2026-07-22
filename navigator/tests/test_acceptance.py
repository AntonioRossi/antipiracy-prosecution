"""Acceptance criteria AC-01 … AC-20 (TDD §14) — the live tests behind
schema/acceptance.json. Function names are registered in the criteria
registry; the traceability meta-test (AC-19) closes both directions over
the registry, itself included.
"""

import copy
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib import bundlezip, canon, gateway, model, projections  # noqa: E402
from lib import release as release_mod, render, schema_validate, validate  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
NAV = os.path.dirname(HERE)
ROOT = os.path.dirname(NAV)
DIST = os.path.join(NAV, "dist")
RECORDS = os.path.join(NAV, "records")
EDITIONS = ("na", "af")
TDD = os.path.join(
    ROOT, "AA11393US-claims-navigator_technical-description_DRAFT.md")

_cache = {}


def get_model(edition_id):
    if edition_id not in _cache:
        boot = gateway.ContentGateway(ROOT)
        allow = json.loads(boot.read_text(
            "navigator/editions/%s.json" % edition_id))
        gw = gateway.ContentGateway(
            ROOT, allowlist=allow["declaredTransitiveInputs"])
        _cache[edition_id] = model.EditionModel(
            gw, "navigator/editions/%s.json" % edition_id)
    return _cache[edition_id]


def get_html(edition_id, mode="candidate"):
    key = (edition_id, mode)
    if key not in _cache:
        _cache[key] = render.render(get_model(edition_id), mode=mode)
    return _cache[key]


def get_errors(edition_id):
    key = (edition_id, "errors")
    if key not in _cache:
        _cache[key] = validate.validate_edition(get_model(edition_id))
    return _cache[key]


def read_records(kind):
    out = []
    if os.path.isdir(RECORDS):
        for name in sorted(os.listdir(RECORDS)):
            if name.startswith(kind + "_") and name.endswith(".json"):
                with open(os.path.join(RECORDS, name), encoding="utf-8") as fh:
                    out.append(json.load(fh))
    return out


def fixture(name):
    with open(os.path.join(HERE, "fixtures", name), encoding="utf-8") as fh:
        return json.load(fh)


def candidate_path(m):
    return os.path.join(DIST, "candidate_" + m.edition["artifactName"])


class Acceptance(unittest.TestCase):
    maxDiff = None

    # ------------------------------------------------------------------
    def test_ac01_census_extraction(self):
        for ed in EDITIONS:
            m = get_model(ed)
            census = m.edition["census"]
            per = {str(c.number): len(c.units) for c in m.claims}
            self.assertEqual(len(m.claims), census["claims"])
            self.assertEqual(sum(per.values()), census["units"])
            self.assertEqual(per, census["perClaim"])
            self.assertEqual(
                sorted(n for n, p in m.parents.items() if p is None),
                sorted(m.edition["independentClaims"]))
            wholes = [b for b in m.target_blocks if b.kind == "claim-whole"]
            self.assertEqual({b.id for b in wholes},
                             {"PC%d" % i for i in range(1, 19)})
            headings = {b.label for b in m.target_blocks
                        if b.kind == "heading"}
            for ex in ("Example 1", "Example 2", "Example 3", "Example 4",
                       "Example 5"):
                self.assertIn(ex, headings)
            tables = [b for b in m.target_blocks
                      if b.kind == "table" and "Example 2" in b.label]
            self.assertEqual(len(tables), 3)
            for t in tables:
                self.assertEqual(len(t.rows), 5)
            figures = [b for b in m.target_blocks if b.kind == "figure"]
            self.assertEqual(len(figures), 4)
            pins = m.registry.corpora[m.edition["targetCorpus"]]["files"]
            for f in figures:
                pinned = [d for p, d in pins.items()
                          if p.endswith(f.meta["file"].split("/")[-1])]
                self.assertEqual(pinned, [f.meta["fileDigest"]])

    def test_ac02_lifecycle(self):
        for ed in EDITIONS:
            m = get_model(ed)
            bad = [e for e in get_errors(ed)
                   if e[0] in ("pending", "stale", "content-hash",
                               "completeness")]
            self.assertEqual(bad, [])
            for otype, key, fields, projection in m.iter_owners():
                self.assertEqual(fields.get("reviewState"),
                                 "internally-reviewed", "%s %s" % (otype, key))
                self.assertEqual(fields.get("migrationState"), "current")
                self.assertEqual(fields["review"]["contentHash"],
                                 m.content_hash(projection))

    def test_ac03_gate_integrity(self):
        for ed in EDITIONS:
            bad = [e for e in get_errors(ed)
                   if e[0] in ("integrity", "inventory", "disposition",
                               "duplicate")]
            self.assertEqual(bad, [])
        # the five disposition fixtures, incl. the honest no-candidate
        # release and the rejected wrong-scope case
        fx = fixture("dispositions_fixture.json")
        m = get_model("na")
        inv = validate._load_invariants(m.gw)
        gates = {g["gateId"]: g for g in fx["gates"]["gates"]}
        for case in fx["cases"]:
            d = case["disposition"]
            entry = gates[d["gateId"]]
            subject = d["subject"]
            if subject["kind"] == "fragment":
                frag = m.relation["fragments"][subject["id"]]
                evidence = frag["status"]
                self.assertEqual(d["subjectHash"],
                                 m.units[subject["id"]].digest)
            else:
                evidence = "mapped"
                self.assertEqual(d["subjectHash"],
                                 m.agg_hashes[int(subject["id"][1:])])
            permitted = inv.permitted_dispositions(
                entry["requiredScope"], evidence)
            if case["expect"] == "valid":
                self.assertIn(d["disposition"], permitted, case["name"])
                if d["disposition"] in ("no-target-recorded",
                                        "carried-at-fragment-fallback"):
                    # honest no-candidate: releasable without any target
                    self.assertEqual(frag["status"],
                                     "counsel-review-required")
                    self.assertNotIn("targets", frag)
            else:
                self.assertNotIn(d["disposition"], permitted, case["name"])
        # totality of the matrix over every reachable configuration
        for scope in ("target", "fragment", "claim"):
            for evidence in ("mapped", "counsel-review-required"):
                self.assertTrue(inv.permitted_dispositions(scope, evidence))
        # inventory-completeness attestation current (double-sided)
        for ed in EDITIONS:
            m = get_model(ed)
            atts = [a for a in read_records("attestation")
                    if a["record"]["type"] == "inventory-completeness" and
                    a["record"]["edition"] == ed]
            self.assertTrue(atts, "no inventory-completeness attestation "
                            "for %s" % ed)
            sides = atts[-1]["record"]["sides"]
            reg = m.registry.corpora[m.edition["claimCorpus"]]
            self.assertEqual(sides["claimSet"], reg["files"][reg["primary"]])
            self.assertEqual(sides["gateInventory"],
                             m.gw.read_log[m.edition["gateInventory"]])

    def test_ac04_source_drift(self):
        for ed in EDITIONS:
            bad = [e for e in get_errors(ed) if e[0] == "drift"]
            self.assertEqual(bad, [])
            m = get_model(ed)
            for _, _, fields, _ in m.iter_owners():
                for hkey in ("fragmentTextHash", "claimHash",
                             "gateEntryHash", "subjectHash"):
                    if hkey in fields:
                        self.assertTrue(
                            fields[hkey].startswith(canon.DIGEST_PREFIX))
                        canon.parse_digest(fields[hkey])

    def test_ac05_schema_invariants(self):
        for ed in EDITIONS:
            self.assertEqual(get_errors(ed), [])
            m = get_model(ed)
            leaves = schema_validate.check_axes(m.schemas["relation"])
            schema_validate.check_locator_coverage(m.schemas["relation"])
            excs = [p for p, ship, review, exc in leaves if exc]
            self.assertTrue(excs)
            for p, ship, review, exc in leaves:
                if exc:
                    self.assertTrue(p.rsplit(".", 1)[-1].startswith("block"))

    def test_ac06_fixtures(self):
        for name, ed in (("na_excerpt.json", "na"),
                         ("af_excerpt.json", "af")):
            fx = fixture(name)
            m = get_model(ed)
            errs = schema_validate.validate(fx, m.schemas["relation"])
            self.assertEqual(errs, [], name)
            self.assertEqual(fx["binding"], m.relation["binding"])
            for fid, frag in fx["fragments"].items():
                self.assertEqual(frag, m.relation["fragments"][fid])
                self.assertEqual(frag["fragmentTextHash"],
                                 m.units[fid].digest)
        # this document's examples match the fixture projections
        tdd = open(TDD, encoding="utf-8").read()
        blocks = re.findall(r"```json\n(.*?)```", tdd, re.S)
        self.assertGreaterEqual(len(blocks), 2)
        na_doc, af_doc = json.loads(blocks[0]), json.loads(blocks[1])

        def matches(doc, real, path="$"):
            if isinstance(doc, str) and doc.endswith("…"):
                self.assertTrue(
                    isinstance(real, str) and real.startswith(doc[:-1]),
                    "%s: %r !~ %r" % (path, doc, real))
            elif isinstance(doc, dict):
                self.assertIsInstance(real, dict, path)
                for k, v in doc.items():
                    self.assertIn(k, real, "%s.%s" % (path, k))
                    matches(v, real[k], "%s.%s" % (path, k))
            elif isinstance(doc, list):
                self.assertIsInstance(real, list, path)
                self.assertLessEqual(len(doc), len(real), path)
                for i, v in enumerate(doc):
                    matches(v, real[i], "%s[%d]" % (path, i))
            else:
                self.assertEqual(doc, real, path)

        matches(na_doc, fixture("na_excerpt.json"), "na")
        matches(af_doc, fixture("af_excerpt.json"), "af")

    def test_ac07_meta_tests(self):
        # single-digest-path + registry-access AST discipline
        scope = [os.path.join(NAV, "build.py")]
        for name in sorted(os.listdir(os.path.join(NAV, "lib"))):
            if name.endswith(".py"):
                scope.append(os.path.join(NAV, "lib", name))
        for path in scope:
            src = open(path, encoding="utf-8").read()
            base = os.path.basename(path)
            if base != "canon.py":
                self.assertNotIn("hashlib", src,
                                 "%s computes digests outside canon" % base)
            if base != "gateway.py":
                self.assertNotRegex(
                    src, r"(?<![\w.])open\(",
                    "%s opens files outside the gateways" % base)
        # edition-blindness: shared modules contain no edition tokens
        for path in scope:
            base = os.path.basename(path)
            src = open(path, encoding="utf-8").read()
            for token in ("na-claims", "af-claims", "na-v2", "af-v2",
                          "normal-allowance", "allowance-first",
                          "NA edition", "AF edition", "na_", "af_"):
                self.assertNotIn(token, src,
                                 "%s contains edition token %r" % (base, token))
        # writer-set: a full derivation writes nothing to the content plane
        m = get_model("na")
        inputs = m.edition["declaredTransitiveInputs"]
        before = {p: canon.bytes_digest(open(os.path.join(ROOT, p), "rb").read())
                  for p in inputs}
        render.render(m, mode="candidate")
        after = {p: canon.bytes_digest(open(os.path.join(ROOT, p), "rb").read())
                 for p in inputs}
        self.assertEqual(before, after)
        # diff-classifier: migrate on a re-anchored corpus touches locator
        # fields only (class b) — simulated by digest-preserving anchor swap
        from lib import migrate as migrate_mod
        m2 = get_model("af")
        rel_before = copy.deepcopy(m2.relation)
        log = []
        migrate_mod.migrate_inventory(m2, log)
        migrate_mod.migrate_relation(m2, log)
        self.assertEqual(log, [])  # pinned corpora: nothing to do
        self.assertEqual(rel_before, m2.relation)
        # procedure-vs-matrix: §10 privilege table + §13 procedure prose
        # against planes.json — prose is checked, not trusted
        planes = m.planes
        tdd = open(TDD, encoding="utf-8").read()
        matrix = tdd[tdd.index("| Command | Reads (kinds) | Writes (kinds) |"):]
        matrix = matrix.split("\n\n")[0] + "\n"
        rows = re.findall(r"\| `([a-z-]+)`( \(deferred\))? \| (.*?) \| (.*?) \|\n",
                          matrix)
        self.assertEqual(len(rows), 9)
        for cmd, _, reads, writes in rows:
            self.assertIn(cmd, planes["commands"], cmd)
            declared_w = set(planes["commands"][cmd]["writes"])
            for kind in re.findall(r"`([a-z-]+)`", writes):
                self.assertIn(kind, declared_w,
                              "TDD row %s writes %s not in matrix" % (cmd, kind))
            for kind in re.findall(r"`([a-z-]+)`", reads):
                self.assertIn(kind,
                              set(planes["commands"][cmd]["reads"]),
                              "TDD row %s reads %s not in matrix" % (cmd, kind))
            if "sources:" in writes:
                self.assertTrue(
                    any(w.startswith("source:") for w in declared_w), cmd)
        proc = tdd[tdd.index("Normative update procedure"):]
        proc = proc[:proc.index("## 14.")]
        for cmd in ("candidate", "migrate", "record-qa", "release", "bundle"):
            self.assertIn(cmd, proc)
        self.assertIn("release-record",
                      planes["commands"]["release"]["writes"])
        self.assertIn("bundle-record", planes["commands"]["bundle"]["writes"])
        for kind, plane in planes["kinds"].items():
            self.assertIn(plane, ("artifact", "verification"))

    # -- AC-07: migration case-table scenarios (mutated corpus copies) ----

    NA_MD = "US/normal-allowance/AA11393US-NA-US_claim-set_DRAFT.md"
    PCT_MD = ("PCT/AA11393US-PCT_RAPPORTO_DEPOSITO_markdown/"
              "AA11393US-PCT_RAPPORTO_DEPOSITO.md")

    def _migration_tree(self, tmp):
        """Copy the NA content plane + sources into a temp tree."""
        import shutil
        for rel in ("navigator/corpora.json", "navigator/strings.json",
                    "navigator/relations/na__pct.json",
                    "navigator/editions/na.json", "navigator/build.py",
                    self.NA_MD, self.PCT_MD):
            dst = os.path.join(tmp, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy(os.path.join(ROOT, rel), dst)
        for d in ("navigator/schema", "navigator/profiles", "navigator/lib"):
            shutil.copytree(os.path.join(ROOT, d), os.path.join(tmp, d),
                            ignore=shutil.ignore_patterns("__pycache__"))
        figdir = os.path.dirname(self.PCT_MD) + "/figures"
        shutil.copytree(os.path.join(ROOT, figdir), os.path.join(tmp, figdir))
        return tmp

    def _mutate(self, tmp, rel, edits):
        path = os.path.join(tmp, rel)
        with open(path, encoding="utf-8") as fh:
            s = fh.read()
        for old, new in edits:
            self.assertIn(old, s, "mutation target not found: %r" % old[:60])
            s = s.replace(old, new, 1)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(s)

    def _repin(self, tmp, *rels):
        cpath = os.path.join(tmp, "navigator/corpora.json")
        with open(cpath, encoding="utf-8") as fh:
            reg = json.load(fh)
        for rel in rels:
            with open(os.path.join(tmp, rel), "rb") as fh:
                digest = canon.bytes_digest(fh.read())
            for entry in reg["corpora"].values():
                if rel in entry["files"]:
                    entry["files"][rel] = digest
        with open(cpath, "w", encoding="utf-8") as fh:
            json.dump(reg, fh, indent=1, ensure_ascii=False)

    def _migrated(self, tmp):
        from lib import migrate as migrate_mod
        gw = gateway.ContentGateway(tmp)
        m = model.EditionModel(gw, "navigator/editions/na.json")
        log = []
        migrate_mod.migrate_inventory(m, log)
        migrate_mod.migrate_relation(m, log)
        return m, log

    def test_ac07_migration_scenarios(self):
        import tempfile
        # ---- scenario 1: every mechanically reachable case-table row ----
        with tempfile.TemporaryDirectory() as tmp:
            self._migration_tree(tmp)
            self._mutate(tmp, self.PCT_MD, [
                # shift all later disclosure anchors (re-anchoring, class b)
                ("### Field of the invention\n\n",
                 "### Field of the invention\n\nA synthetic migration-test "
                 "paragraph inserted to shift subsequent anchors.\n\n"),
                # target block text changed
                ("the streamed content in the form of said chunks 113 is "
                 "distributed using unicasting.",
                 "the streamed content in the form of said chunks 113 is "
                 "distributed using unicasting (edited for the migration "
                 "scenario)."),
                # mid-document deletion: digest vanishes, locator re-filled
                ("In a preferred embodiment of the present invention, a "
                 "single time code variation is applied at each "
                 "director-commanded camera cut to ensure each content mate "
                 "remains unique and traceable.\n\n", ""),
                # repeated text: duplicate a targeted block
                ("In some embodiments of the present invention, said record "
                 "is a ledger 122.\n",
                 "In some embodiments of the present invention, said record "
                 "is a ledger 122.\n\nIn some embodiments of the present "
                 "invention, said record is a ledger 122.\n"),
            ])
            self._mutate(tmp, self.NA_MD, [
                # fragment text changed (claim 1 -> dependents cascade)
                ("receive video captured from a plurality of cameras and a "
                 "structured list of instructions describing edits",
                 "receive video captured from a plurality of cameras "
                 "together with a structured list of instructions "
                 "describing edits"),
                # fragment removed (claim 24 loses its last unit)
                ("recording which recipient or group of recipients received "
                 "each manifest file.\n", ""),
                # new fragment appears (claim 30 gains a unit); anchor on the
                # full claim-30 text — claim 8 shares the trailing words
                ("**30.** The method of claim 22, further comprising "
                 "overlaying one or more additional audio or video elements "
                 "not present in the video received from the plurality of "
                 "cameras onto at least one of the reference audio-video "
                 "content or the mate.\n",
                 "**30.** The method of claim 22, further comprising "
                 "overlaying one or more additional audio or video elements "
                 "not present in the video received from the plurality of "
                 "cameras onto at least one of the reference audio-video "
                 "content or the mate.\n\nwherein the overlaying is "
                 "performed before delivery of the respective versions.\n"),
                # shift guidance anchors (inventory source re-anchoring)
                ("## 2. Drafting principles\n\n",
                 "## 2. Drafting principles\n\nA synthetic migration-test "
                 "note inserted to shift guidance anchors.\n\n"),
                # caution-source block text changed
                ("stored timings were “produced by” the mate process.",
                 "stored timings were “produced by” the mate process "
                 "(edited for the migration scenario)."),
            ])
            self._repin(tmp, self.PCT_MD, self.NA_MD)
            m, log = self._migrated(tmp)
            rel = m.relation
            reasons = {fid: (rel["fragments"][fid].get("migrationState"),
                             rel["fragments"][fid].get("migrationReason"))
                       for fid in rel["fragments"]}
            # mechanical re-anchoring: locators updated, review untouched
            self.assertTrue(any(a == "re-anchor" for a, _, _ in log))
            c17 = rel["fragments"]["c17u0"]
            self.assertEqual(c17["migrationState"], "current")
            self.assertEqual(c17["reviewState"], "internally-reviewed")
            for t in c17["targets"]:
                anchor = m.target_anchor(t["block"])
                self.assertEqual(anchor.digest, t["textHash"])
            # inventory: unique-match re-anchor vs unresolved manual
            self.assertEqual(
                m.gates_by_id["na-gate-combined-example"]["source"]["block"],
                "S021")
            self.assertIn(("manual", "inventory:na-gate-detection-support"),
                          [(a, k) for a, k, _ in log])
            # case rows
            self.assertEqual(reasons["c1u1"], ("stale", "changed"))
            self.assertTrue(rel["fragments"]["c1u1"].get("previousTargets"))
            self.assertEqual(reasons["c14u0"], ("stale", "target-changed"))
            self.assertTrue(rel["fragments"]["c14u0"].get("previousTargets"))
            # mid-document deletion mechanically classifies as target-changed
            # (removal is observable only at a container tail — TDD §10.6)
            self.assertEqual(reasons["c6u0"], ("stale", "target-changed"))
            self.assertEqual(reasons["c12u0"], ("stale", "ambiguous"))
            self.assertEqual(reasons["c24u3"], ("stale", "fragment-removed"))
            # c16u5 targets S071, whose text is verbatim-identical to PCT
            # claim 1 element 5 (repeated text): after the shift its digest
            # matches two positions, so migrate correctly refuses to guess
            self.assertEqual(reasons["c16u5"], ("stale", "ambiguous"))
            self.assertEqual(reasons["c22u6"], ("stale", "source-changed"))
            # ancestor-claim change cascades to dependents
            self.assertEqual(reasons["c5u0"], ("stale", "endpoint-changed"))
            gate_c1 = rel["claimGates"]["c1"][0]
            self.assertEqual((gate_c1["migrationState"],
                              gate_c1.get("migrationReason")),
                             ("stale", "endpoint-changed"))
            # new fragment appears as counsel-review-required + pending
            self.assertIn("c30u1", rel["fragments"])
            self.assertEqual(rel["fragments"]["c30u1"]["status"],
                             "counsel-review-required")
            self.assertEqual(rel["fragments"]["c30u1"]["reviewState"],
                             "pending")
            # re-anchored caution sources did NOT invalidate dispositions
            # (gate-entry hash excludes the source locator)
            prio = [d for d in rel["dispositions"]
                    if d["gateId"] == "na-gate-example2-priority" and
                    d["subject"]["id"] == "c23u0"]
            self.assertEqual(prio[0]["migrationState"], "current")
            # but the parent-claim amendment cascades to c2's disposition
            prio2 = [d for d in rel["dispositions"]
                     if d["gateId"] == "na-gate-example2-priority" and
                     d["subject"]["id"] == "c2u0"]
            self.assertEqual((prio2[0]["migrationState"],
                              prio2[0].get("migrationReason")),
                             ("stale", "endpoint-changed"))

            # ---- §13 steps 4-5: resolve every stale/pending, restamp,
            # and reach a green candidate on the mutated tree -------------
            def find_block(snippet, quotable=False):
                order = m.guidance_order if quotable else m.target_order
                cls = "quotable" if quotable else "targetable"
                hits = [a for a in order if a.cls == cls and
                        snippet in (a.block.canonical or "")]
                self.assertEqual(len(hits), 1, snippet)
                return hits[0]

            def dead(x):
                anchor = m.target_anchor(x["block"])
                return anchor is None or anchor.digest != x["textHash"]

            frags = rel["fragments"]
            # target-changed: the human re-targets to the edited block
            t = [x for x in frags["c14u0"]["targets"] if dead(x)][0]
            t["block"] = find_block(
                "unicasting (edited for the migration scenario)").id
            # vanished-digest target: drop the dead candidate, keep survivors
            frags["c6u0"]["targets"] = [
                x for x in frags["c6u0"]["targets"] if not dead(x)]
            self.assertTrue(frags["c6u0"]["targets"])
            # ambiguous: the human picks one occurrence
            for fid in ("c12u0", "c16u5"):
                for x in frags[fid].get("targets", []):
                    if dead(x):
                        positions = m.digest_positions.get(x["textHash"], [])
                        self.assertGreater(len(positions), 1, fid)
                        x["block"] = positions[0]
            # fragment removed: delete the entry in the resolving commit
            del frags["c24u3"]
            # new fragment: author the honest no-candidate entry
            frags["c30u1"]["review"].update(by="scenario-review",
                                            date="2026-07-22")
            # caution source: re-point the inventory at the edited block
            m.gates_by_id["na-gate-detection-support"]["source"]["block"] = \
                find_block("(edited for the migration scenario)",
                           quotable=True).id
            # resolving review: lifecycle reset (restamp re-reviews below)
            def reset(owner):
                owner["migrationState"] = "current"
                owner.pop("migrationReason", None)
                owner.pop("previousTargets", None)
            for frag in frags.values():
                reset(frag)
                for ph in frag.get("phrases", []):
                    reset(ph)
            for gl in rel["claimGates"].values():
                for g in gl:
                    reset(g)
            for d in rel["dispositions"]:
                reset(d)
            # census follows the amended claim set (git-reviewed edit)
            epath = os.path.join(tmp, "navigator/editions/na.json")
            with open(epath, encoding="utf-8") as fh:
                ecfg = json.load(fh)
            ecfg["census"]["perClaim"]["24"] = 3
            ecfg["census"]["perClaim"]["30"] = 2
            with open(epath, "w", encoding="utf-8") as fh:
                json.dump(ecfg, fh, indent=1, ensure_ascii=False)
            for relpath, obj in (("navigator/relations/na__pct.json", rel),
                                 ("navigator/profiles/gates_na-claims.json",
                                  m.gates)):
                with open(os.path.join(tmp, relpath), "w",
                          encoding="utf-8") as fh:
                    json.dump(obj, fh, indent=1, ensure_ascii=False)
            # restamp endpoint pins + fresh contentHashes, marked reviewed
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "stamp_tool", os.path.join(NAV, "tools", "stamp.py"))
            stamp_tool = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(stamp_tool)
            cwd = os.getcwd()
            try:
                stamp_tool.stamp(tmp, "navigator/editions/na.json",
                                 mark_reviewed=True)
            finally:
                os.chdir(cwd)
            # the resolved edition validates clean and yields a candidate
            gw2 = gateway.ContentGateway(tmp)
            m2 = model.EditionModel(gw2, "navigator/editions/na.json")
            self.assertEqual(validate.validate_edition(m2), [])
            self.assertEqual(validate.validate_edition(m2, for_release=True),
                             [])
            resolved = render.render(m2, mode="candidate")
            self.assertGreater(len(resolved), 1_000_000)
        # ---- scenario 2: target removed (container-tail deletion) -------
        with tempfile.TemporaryDirectory() as tmp:
            self._migration_tree(tmp)
            path = os.path.join(tmp, self.PCT_MD)
            with open(path, encoding="utf-8") as fh:
                s = fh.read()
            cut = s.index("**16.** Method (200)")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(s[:cut])
            self._repin(tmp, self.PCT_MD)
            m, log = self._migrated(tmp)
            c22u0 = m.relation["fragments"]["c22u0"]
            self.assertEqual((c22u0["migrationState"],
                              c22u0.get("migrationReason")),
                             ("stale", "target-removed"))
        # ---- scenario 3: canonVersion mismatch -> unclassified, totally --
        with tempfile.TemporaryDirectory() as tmp:
            self._migration_tree(tmp)
            rpath = os.path.join(tmp, "navigator/relations/na__pct.json")
            with open(rpath, encoding="utf-8") as fh:
                relx = json.load(fh)
            relx["binding"]["canonVersion"] = "c0"
            with open(rpath, "w", encoding="utf-8") as fh:
                json.dump(relx, fh, indent=1, ensure_ascii=False)
            from lib import migrate as migrate_mod
            gw = gateway.ContentGateway(tmp)
            m = model.EditionModel(gw, "navigator/editions/na.json")
            log = []
            migrate_mod.migrate_relation(m, log)
            owners = list(m.iter_owners())
            self.assertEqual(len(log), len(owners))
            for _, _, fields, _ in owners:
                self.assertEqual(fields["migrationState"], "stale")
                self.assertEqual(fields["migrationReason"], "unclassified")

    def test_ac08_projections(self):
        never_tokens = ("reviewState", "migrationState", "contentHash",
                        "proposedFrom", "previousTargets", "fragmentTextHash",
                        "textHash", "claimHash", "gateEntryHash",
                        "subjectHash")
        internal_tokens = ("priority-map", "priority-support", "crosswalk",
                           "qa-source", "na-priority", "af-priority")
        for ed in EDITIONS:
            for mode in ("candidate", "preview"):
                html = get_html(ed, mode).decode("utf-8")
                for tok in never_tokens:
                    self.assertNotIn(tok, html, "%s %s leaks %r"
                                     % (ed, mode, tok))
                for tok in internal_tokens:
                    self.assertNotIn(tok, html.lower(), "%s %s leaks %r"
                                     % (ed, mode, tok))
            # schedule projection = artifact + rationale only
            m = get_model(ed)
            ship = projections.ship_relation(m, "artifact")
            self.assertNotIn("rationale", json.dumps(ship))

    def test_ac09_escaping(self):
        payloads = fixture("escaping_fixture.json")["payloads"]
        m = get_model("na")
        # authored channels: note, rationale, phrase text, quoted source
        for payload in payloads:
            self.assertNotIn(payload, render.esc(payload))
            out = render.esc(payload)
            self.assertNotIn("<script", out.lower())
            self.assertNotIn("<img", out.lower())
            self.assertNotIn('"', out.replace("&quot;", ""))
        # embedded JSON channel: </script never appears unescaped
        blob = render.script_json({"x": payloads})
        self.assertNotIn("</script", blob)
        self.assertNotIn("<", blob.split('"x"', 1)[1].split("]", 1)[0]
                         .replace("\\u003c", ""))
        # md_inline never introduces tags beyond strong/code
        for payload in payloads:
            out = render.md_inline(payload)
            for tag in re.findall(r"<(/?[a-zA-Z]+)", out):
                self.assertIn(tag.lstrip("/"), ("strong", "code"))
        # and the artifact contains none of the raw payloads
        html = get_html("na").decode("utf-8")
        for payload in payloads:
            if "<" in payload:
                self.assertNotIn(payload, html)

    def test_ac10_navigation(self):
        for ed in EDITIONS:
            m = get_model(ed)
            html = get_html(ed).decode("utf-8")
            ship = projections.ship_relation(m, "artifact")
            reverse = projections.reverse_index(ship)
            ids = set(re.findall(r'id="([^"]+)"', html))
            # every unit and phrase has its button; statuses render
            for fid, frag in ship["fragments"].items():
                self.assertIn("btn-" + fid, ids)
                for ph in frag.get("phrases", []):
                    self.assertIn("btn-" + ph["id"], ids)
            # every recorded target block resolves in the DOM
            for frag in ship["fragments"].values():
                for t in frag.get("targets", []):
                    self.assertIn(t["block"], ids)
            # badges: one per indexed block, count = fragment count
            badges = dict(re.findall(
                r'class="rev-badge" data-block="([^"]+)"[^>]*>◂ (\d+)<', html))
            self.assertEqual(set(badges), set(reverse))
            for block, n in badges.items():
                self.assertEqual(int(n), len(reverse[block]))
            # claim-level gate chips render at claim headers
            n_gates = sum(len(v) for v in ship.get("claimGates", {}).values())
            self.assertEqual(html.count('class="gate-chip"'), n_gates)
            # mode labels + navbar containers
            for tok in ('id="forward-bar"', 'id="reverse-bar"'):
                self.assertIn(tok, html)
            # pure selection model behaves (scripted, on candidate bytes)
            self._node_check(ed, html)

    def _node_check(self, ed, html):
        data = re.search(
            r'<script type="application/json" id="nav-data">(.*?)</script>',
            html, re.S).group(1)
        nm = re.search(r"/\*NAVMODEL-START\*/(.*?)/\*NAVMODEL-END\*/",
                       html, re.S).group(1)
        js = """
'use strict';
var DATA = JSON.parse(%s);
%s
var fails = [];
function check(cond, msg){ if(!cond) fails.push(msg); }
Object.keys(DATA.fragments).forEach(function(fid){
  var info = NavModel.forwardTargets(DATA, fid);
  check(info !== null, 'no forward info for ' + fid);
  if (info.status === 'mapped') check(info.targets.length >= 1, fid);
  else check(info.targets.length === 0, fid + ' crr has targets');
  (DATA.fragments[fid].phrases || []).forEach(function(ph){
    var pi = NavModel.forwardTargets(DATA, ph.id);
    check(pi !== null, 'no phrase info ' + ph.id);
    if (pi.status === 'mapped') check(pi.targets.length >= 1, ph.id);
  });
});
check(NavModel.cycle(0, 4, -1) === 3, 'cycle wrap back');
check(NavModel.cycle(3, 4, 1) === 0, 'cycle wrap fwd');
Object.keys(DATA.reverse).forEach(function(block){
  var list = NavModel.reverseFragments(DATA, block);
  var last = null;
  list.forEach(function(e){
    var c = parseInt(e.fragment.slice(1), 10);
    if (last !== null) check(c >= last, 'reverse not claims-ascending ' + block);
    last = c;
  });
});
Object.keys(DATA.claimGates).forEach(function(ck){
  check(NavModel.claimGates(DATA, ck + 'u0').length ===
        DATA.claimGates[ck].length, 'claim gates lookup ' + ck);
});
console.log(JSON.stringify({fails: fails}));
""" % (json.dumps(data), nm)
        with tempfile.NamedTemporaryFile("w", suffix=".js",
                                         delete=False) as fh:
            fh.write(js)
            tmp = fh.name
        try:
            out = subprocess.run(["node", tmp], capture_output=True,
                                 text=True, timeout=60)
            self.assertEqual(out.returncode, 0, out.stderr)
            result = json.loads(out.stdout.strip().splitlines()[-1])
            self.assertEqual(result["fails"], [], ed)
        finally:
            os.unlink(tmp)

    def _current_qa(self, ed):
        digest = canon.bytes_digest(get_html(ed))
        qa = [r for r in read_records("qa-record")
              if r["record"]["edition"] == ed and
              r["record"]["candidateDigest"] == digest]
        self.assertTrue(qa, "no qa-record for the current %s candidate" % ed)
        return qa[-1]

    def test_ac11_accessibility_static(self):
        for ed in EDITIONS:
            html = get_html(ed).decode("utf-8")
            self.assertIn('aria-live="polite"', html)
            self.assertNotIn("<button", re.sub(
                r"<button[^>]*>[^<]*</button>", "", html).replace(
                "</button>", ""))  # no nested interactive controls
            self.assertIn("min-height:24px", html)
            self.assertIn("Escape", html)
            self.assertIn("ArrowLeft", html)
            self.assertIn("prefers-reduced-motion", html)
            for b in re.findall(r"<button[^>]*>", html):
                self.assertTrue("aria-label" in b or "data-goto" in b or
                                "data-aux" in b, b)
        # human confirmation across the support matrix lives in the QA record
        for ed in EDITIONS:
            qa = self._current_qa(ed)
            self.assertIn("ac11", qa["record"]["manualChecks"])

    def test_ac12_print_static(self):
        for ed in EDITIONS:
            html = get_html(ed).decode("utf-8")
            self.assertIn("@media print", html)
            self.assertIn("position:fixed; bottom:0", html)
            qa = self._current_qa(ed)
            self.assertIn("ac12", qa["record"]["manualChecks"])

    def test_ac13_layout_static(self):
        for ed in EDITIONS:
            html = get_html(ed).decode("utf-8")
            self.assertIn("(max-width:1279px),(max-height:719px)", html)
            self.assertIn("1280", html)  # About panel states the minimum
            qa = self._current_qa(ed)
            self.assertIn("ac13", qa["record"]["manualChecks"])

    def test_ac14_nojs_static(self):
        for ed in EDITIONS:
            m = get_model(ed)
            html = get_html(ed).decode("utf-8")
            static = re.sub(r"<script.*?</script>", "", html, flags=re.S)
            # claims verbatim, disclosure, disclaimer, provenance, schedule
            first_claim = m.claims[0].units[0].text
            self.assertIn(render.esc(first_claim)[:80], static)
            self.assertIn("Detailed description of Preferred Embodiments",
                          static)
            self.assertIn("Draft navigation aid generated from claim-set",
                          static)
            self.assertIn('id="about"', static)
            self.assertIn('id="schedule"', static)
            self.assertIn("<noscript>", static)

    def test_ac15_api_policy(self):
        for ed in EDITIONS:
            m = get_model(ed)
            html = get_html(ed).decode("utf-8")
            js = html.split("<script>")[-1].split("</script>")[0]
            probe, page = js.split("})();", 1)
            for api, spec in m.api_policy["apis"].items():
                if spec["class"] != "probed":
                    continue
                token = api.split(".")[-1]
                self.assertIn(token, probe,
                              "no instrumentation for probed API %s" % api)
            # page code never uses the enumerated APIs
            for tok in ("fetch(", "XMLHttpRequest", "WebSocket", "EventSource",
                        "sendBeacon", "localStorage", "sessionStorage",
                        "indexedDB", "document.cookie", "pushState",
                        "replaceState", "location.assign", "location.replace"):
                self.assertNotIn(tok, page,
                                 "page code references %s" % tok)
            self.assertIn("__apiAttempts", probe)
            qa = self._current_qa(ed)
            self.assertIn("ac15", qa["record"]["manualChecks"])

    def test_ac16_determinism(self):
        for ed in EDITIONS:
            m = get_model(ed)
            one = render.render(m, mode="candidate")
            two = render.render(m, mode="candidate")
            self.assertEqual(one, two, "double build not byte-identical")
            # across separate interpreter processes: an in-process double
            # build shares hash seeds and cannot detect seed-dependent
            # ordering (AC-16)
            child = subprocess.run(
                [sys.executable, "-c", """
import json, sys
sys.path.insert(0, "navigator")
from lib import canon, gateway, model, render
ed = %r
boot = gateway.ContentGateway(".")
allow = json.loads(boot.read_text("navigator/editions/" + ed + ".json"))
gw = gateway.ContentGateway(".", allowlist=allow["declaredTransitiveInputs"])
m = model.EditionModel(gw, "navigator/editions/" + ed + ".json")
print(canon.bytes_digest(render.render(m, mode="candidate")))
""" % ed], capture_output=True, text=True, cwd=ROOT, timeout=300)
            self.assertEqual(child.returncode, 0, child.stderr)
            self.assertEqual(child.stdout.strip(), canon.bytes_digest(one),
                             "cross-process double build not byte-identical")
            cpath = candidate_path(m)
            self.assertTrue(os.path.exists(cpath))
            with open(cpath, "rb") as fh:
                candidate_bytes = fh.read()
            self.assertEqual(candidate_bytes, one,
                             "dist candidate differs from derivation")
            lock = m.gw.lock()
            self.assertEqual(release_mod.exact_set_check(
                lock, m.edition["declaredTransitiveInputs"]), [])
            qa = [r for r in read_records("qa-record")
                  if r["record"]["edition"] == ed and
                  r["record"]["candidateDigest"] ==
                  canon.bytes_digest(candidate_bytes)]
            self.assertTrue(qa, "no qa-record for the current candidate")
            self.assertIn(lock["lockDigest"],
                          {r["record"]["lockDigest"] for r in qa},
                          "no qa-record reproduces this derivation's lock")
            self.assertNotIn("reproductionDiagnostics",
                             json.dumps(lock))  # diagnostics excluded
            rel = [r for r in read_records("release-record")
                   if r["record"]["edition"] == ed and
                   r["record"]["sealedDigest"] ==
                   canon.bytes_digest(candidate_bytes)]
            self.assertTrue(rel, "no release-record seals the current "
                            "candidate bytes for %s" % ed)
            sealed = os.path.join(DIST, rel[-1]["record"]["sealed"])
            with open(sealed, "rb") as fh:
                sealed_bytes = fh.read()
            self.assertEqual(sealed_bytes, candidate_bytes,
                             "sealed bytes differ from QA'd candidate")
            with open(sealed + ".sha256", encoding="utf-8") as fh:
                checksum = fh.read()
            self.assertIn(canon.bytes_digest(sealed_bytes), checksum)

    def test_ac17_disclaimer_legend(self):
        strings = json.loads(open(os.path.join(NAV, "strings.json"),
                                  encoding="utf-8").read())
        legend_digest = canon.text_digest(
            canon.canon_prose(strings["counselLegend"]))
        atts = [a for a in read_records("attestation")
                if a["record"]["type"] == "legend-approval"]
        self.assertTrue(atts, "no legend-approval attestation")
        self.assertEqual(atts[-1]["record"]["sides"]["legendWording"],
                         legend_digest)
        for ed in EDITIONS:
            html = get_html(ed).decode("utf-8")
            self.assertGreaterEqual(
                html.count(render.esc(strings["counselLegend"])), 2)
            self.assertIn("Draft navigation aid generated from claim-set",
                          html)
            static = re.sub(r"<script.*?</script>", "", html, flags=re.S)
            self.assertIn(render.esc(strings["counselLegend"]), static)

    def test_ac18_attestations(self):
        # attestation sufficiency: a CURRENT attestation of each required
        # type exists; superseded ones persist in the append-only store
        atts = read_records("attestation")
        for ed in EDITIONS:
            m = get_model(ed)
            from build import current_side_digests  # noqa: E402
            sides_now = current_side_digests(m)

            def current(atype):
                return [a for a in atts
                        if a["record"]["type"] == atype and
                        a["record"].get("edition") in (ed, None) and
                        all(sides_now.get(s) == d for s, d in
                            a["record"]["sides"].items())]
            self.assertTrue(current("qa-priority-map"),
                            "no current priority-map attestation for %s" % ed)
            if "crosswalk" in m.edition["qaSources"]:
                self.assertTrue(current("qa-crosswalk"),
                                "no current crosswalk attestation for %s" % ed)

    def test_ac19_traceability_meta(self):
        registry = json.loads(open(
            os.path.join(NAV, "schema", "acceptance.json"),
            encoding="utf-8").read())
        import tests.test_acceptance as this_mod
        registered_tests = set()
        for crit in registry["criteria"]:
            enforced = crit["enforcedBy"]
            self.assertTrue(enforced["tests"] or enforced["qaRecordFields"],
                            crit["id"])
            for tname in enforced["tests"]:
                mod, fn = tname.rsplit(".", 1)
                self.assertEqual(mod, "test_acceptance")
                self.assertTrue(hasattr(Acceptance, fn),
                                "%s: registered test %s does not exist"
                                % (crit["id"], fn))
                registered_tests.add(fn)
            for field in enforced["qaRecordFields"]:
                qa = read_records("qa-record")
                self.assertTrue(qa)
                self.assertIn(field, qa[-1]["record"]["manualChecks"],
                              "%s: QA-record field %r missing"
                              % (crit["id"], field))
        # reverse direction: every acceptance-designated test maps back
        for name in dir(this_mod.Acceptance):
            if re.match(r"test_ac\d\d_", name):
                self.assertIn(name, registered_tests,
                              "%s not registered in acceptance.json" % name)
        ids = [c["id"] for c in registry["criteria"]]
        self.assertEqual(ids, ["AC-%02d" % i for i in range(1, 21)])
        # §14 must match the registry (comparison test, guardrail 17)
        tdd = open(TDD, encoding="utf-8").read()
        sec = tdd[tdd.index("## 14. Acceptance criteria"):]
        sec = sec[:sec.index("## 15.")]

        def norm(t):
            t = re.sub(r"[*`§]", "", t)
            return re.sub(r"\s+", " ", t).strip()
        flat = norm(sec)
        for crit in registry["criteria"]:
            self.assertIn(crit["id"], sec)
            self.assertIn(norm(crit["text"])[:120], flat,
                          "%s text drifted from §14" % crit["id"])

    def test_ac20_bundle(self):
        cfg = json.loads(open(os.path.join(NAV, "bundles", "na-af-2026.json"),
                              encoding="utf-8").read())
        bpath = os.path.join(DIST, cfg["name"])
        self.assertTrue(os.path.exists(bpath), "bundle not built")
        with open(bpath, "rb") as fh:
            zip_bytes = fh.read()
        recs = [r for r in read_records("bundle-record")
                if r["record"]["bundleDigest"] == canon.bytes_digest(zip_bytes)]
        self.assertTrue(recs, "no bundle-record for the current bundle bytes")
        rec = recs[-1]["record"]
        zf = zipfile.ZipFile(bpath)
        names = zf.namelist()
        release_recs = read_records("release-record")
        expected = []
        for ed in cfg["editions"]:
            sealed = [r for r in release_recs
                      if r["record"]["edition"] == ed][-1]["record"]["sealed"]
            expected += [sealed, sealed + ".sha256"]
        expected.append("MANIFEST.txt")
        self.assertEqual(names, expected)  # exactly the enumerated members
        for info in zf.infolist():
            self.assertEqual(info.compress_type, zipfile.ZIP_STORED)
            data = zf.read(info.filename)
            member = [x for x in rec["members"] if x["name"] == info.filename]
            self.assertEqual(member[0]["digest"], canon.bytes_digest(data))
        # golden bundle fixture: byte-exact writer conformance
        gold = fixture("golden_bundle.json")
        built = bundlezip.build_zip(
            [(n, d.encode("ascii")) for n, d in gold["members"]],
            gold["declaredTimestamp"])
        self.assertEqual(built.hex(), gold["hex"])
        self.assertEqual(canon.bytes_digest(built), gold["sha256"])
        # detached checksum + neutral manifest wording digest
        with open(bpath + ".sha256", encoding="utf-8") as fh:
            self.assertIn(canon.bytes_digest(zip_bytes), fh.read())
        strings = json.loads(open(os.path.join(NAV, "strings.json"),
                                  encoding="utf-8").read())
        want = canon.text_digest(
            canon.canon_prose(strings["bundleManifestText"]))
        self.assertEqual(rec["manifestWording"], want)
        atts = [a for a in read_records("attestation")
                if a["record"]["type"] == "manifest-approval"]
        self.assertTrue(atts, "no manifest-approval attestation")
        self.assertEqual(atts[-1]["record"]["sides"]["manifestWording"], want)
        manifest = zf.read("MANIFEST.txt").decode("utf-8")
        self.assertNotIn("sha256/c1:", manifest)  # no verification refs


if __name__ == "__main__":
    unittest.main()
