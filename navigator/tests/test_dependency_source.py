"""Dependency-map checks must read the published claim-document table."""

import json
import copy
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib import claims, depgraph, gateway, model  # noqa: E402


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def af_model():
    boot = gateway.ContentGateway(ROOT)
    cfg = json.loads(boot.read_text("navigator/editions/af.json"))
    gw = gateway.ContentGateway(ROOT,
                                allowlist=cfg["declaredTransitiveInputs"])
    return model.EditionModel(gw, "navigator/editions/af.json")


class TestDependencyDocumentSource(unittest.TestCase):

    def test_published_table_matches_authored_map(self):
        m = af_model()
        source = m.registry.primary_text(m.edition["claimCorpus"])
        parsed = claims.parse_dependency_table(source)
        self.assertEqual(parsed,
                         {int(k): v for k, v in
                          m.deps["documentTable"].items()})

    def test_source_table_drift_fails_three_way_check(self):
        m = af_model()
        source = m.registry.primary_text(m.edition["claimCorpus"])
        old = "| 8 | Dependent | 7 | Sliding-window fuzzy matching |"
        new = "| 8 | Dependent | 6 | Sliding-window fuzzy matching |"
        self.assertIn(old, source)
        drifted = claims.parse_dependency_table(source.replace(old, new, 1))
        with self.assertRaisesRegex(depgraph.DepGraphError,
                                    "three-way check failed"):
            depgraph.validate(m.deps, m.claims,
                              m.edition["independentClaims"],
                              document_table=drifted)

    def test_na_document_has_no_dependency_table(self):
        boot = gateway.ContentGateway(ROOT)
        cfg = json.loads(boot.read_text("navigator/editions/na.json"))
        gw = gateway.ContentGateway(ROOT,
                                    allowlist=cfg["declaredTransitiveInputs"])
        m = model.EditionModel(gw, "navigator/editions/na.json")
        source = m.registry.primary_text(m.edition["claimCorpus"])
        self.assertIsNone(claims.parse_dependency_table(source))

    def test_noncanonical_claim_keys_cannot_collapse(self):
        m = af_model()
        for field in ("claims", "documentTable"):
            with self.subTest(field=field):
                mutated = copy.deepcopy(m.deps)
                mutated[field]["01"] = mutated[field]["1"]
                with self.assertRaisesRegex(depgraph.DepGraphError,
                                            "noncanonical claim key"):
                    depgraph.validate(
                        mutated, m.claims, m.edition["independentClaims"],
                        document_table={int(k): v for k, v in
                                        m.deps["documentTable"].items()})


if __name__ == "__main__":
    unittest.main()
