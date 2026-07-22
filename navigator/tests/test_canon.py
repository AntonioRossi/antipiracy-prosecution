"""Canonicalization law — golden vectors + property-based tests (AC-07)."""

import json
import os
import random
import sys
import unicodedata
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib import canon  # noqa: E402

HERE = os.path.dirname(__file__)


class TestVectors(unittest.TestCase):
    """Golden vectors confirm the law; they do not define it."""

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(HERE, "vectors", "canon_vectors.json"),
                  encoding="utf-8") as fh:
            cls.vectors = json.load(fh)["cases"]

    def test_unicode_pin(self):
        self.assertEqual(canon.UNICODE_VERSION, "15.1.0")
        self.assertEqual(unicodedata.unidata_version, canon.UNICODE_VERSION)

    def test_known_sha256(self):
        self.assertEqual(
            canon.text_digest("abc"),
            "sha256/c1:ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410"
            "ff61f20015ad")

    def test_golden_vectors(self):
        for case in self.vectors:
            kind, inp, want = case["kind"], case["input"], case["output"]
            with self.subTest(case["name"]):
                if kind == "prose":
                    got = canon.canon_prose(inp)
                elif kind == "code":
                    got = canon.canon_code(inp)
                elif kind == "table":
                    got = canon.canon_table(inp["rows"], inp["caption"])
                elif kind == "table-row":
                    got = canon.canon_table_row(inp)
                elif kind == "text-digest":
                    got = canon.text_digest(inp)
                elif kind == "json":
                    got = canon.canonical_json(inp).decode("utf-8")
                elif kind == "composite":
                    digests = [canon.text_digest(x) for x in inp["digests"]]
                    got = canon.composite_digest(inp["tag"], digests)
                elif kind == "composite-obj":
                    got = canon.composite_digest(inp["tag"], inp["obj"])
                else:
                    self.fail("unknown vector kind %r" % kind)
                self.assertEqual(got, want)

    def test_tag_registry(self):
        for tag, form in canon.TAGS.items():
            self.assertNotIn("\x00", tag)
            tag.encode("ascii")
            self.assertIn(form, ("digest-list", "object"))
        # one tag per verification-record kind (TDD §8.2)
        for kind in ("qa-record", "attestation", "release-record",
                     "bundle-record"):
            self.assertIn("aa11393:%s:c1" % kind, canon.TAGS)

    def test_law_edges(self):
        with self.assertRaises(canon.CanonError):
            canon.canonical_json({"n": 2 ** 53})
        with self.assertRaises(canon.CanonError):
            canon.canonical_json({"x": 1.5})
        with self.assertRaises(canon.CanonError):
            canon.canonical_json({"é": 1, "é": 2})  # NFC collision
        with self.assertRaises(canon.CanonError):
            canon.composite_digest("aa11393:unregistered:c1", [])
        with self.assertRaises(canon.CanonError):
            canon.parse_digest("sha256/c1:short")
        with self.assertRaises(canon.CanonError):
            canon.parse_digest("sha256/c0:" + "0" * 64)


class TestProperties(unittest.TestCase):
    """Property-based canonicalization tests over generated inputs
    (AC-07): idempotence, NFC duplicate-key rejection, escaping exactness,
    integer edge rules."""

    def setUp(self):
        self.rng = random.Random(11393)

    def _rand_text(self, n):
        pool = ("abcxyzé́ \t\n\r 　  "
                "\"\\`*<>&")
        return "".join(self.rng.choice(pool) for _ in range(n))

    def test_prose_idempotent(self):
        for _ in range(300):
            t = self._rand_text(self.rng.randrange(0, 60))
            once = canon.canon_prose(t)
            self.assertEqual(once, canon.canon_prose(once))
            # collapsed: no runs of whitespace; trimmed per the pinned
            # White_Space set (NOT str.strip(): Python also strips
            # \x1c-\x1f, which the White_Space property excludes)
            self.assertNotIn("  ", once)
            if once:
                self.assertNotIn(once[0], canon.WHITESPACE)
                self.assertNotIn(once[-1], canon.WHITESPACE)

    def test_code_idempotent(self):
        for _ in range(300):
            t = self._rand_text(self.rng.randrange(0, 80))
            once = canon.canon_code(t)
            self.assertEqual(once, canon.canon_code(once))
            self.assertNotIn("\r", once)

    def test_json_escaping_exactness(self):
        import json as stdjson
        for _ in range(300):
            obj = {"k%d" % i: self._rand_text(self.rng.randrange(0, 20))
                   for i in range(self.rng.randrange(1, 5))}
            out = canon.canonical_json(obj)
            # round-trip: standard JSON parses it back to the NFC form
            parsed = stdjson.loads(out.decode("utf-8"))
            want = {unicodedata.normalize("NFC", k):
                    unicodedata.normalize("NFC", v) for k, v in obj.items()}
            self.assertEqual(parsed, want)
            # only the exact two-char escapes + \u00xx below 0x20
            text = out.decode("utf-8")
            for i, ch in enumerate(text):
                self.assertGreaterEqual(ord(ch), 0x20,
                                        "raw control char in output")

    def test_json_key_sorting_codepoint(self):
        for _ in range(100):
            keys = ["k" + chr(self.rng.randrange(0x30, 0x2FA0))
                    for _ in range(4)]
            obj = {k: 1 for k in keys}
            out = canon.canonical_json(obj).decode("utf-8")
            order = [k for k in sorted(set(obj))]
            positions = [out.index(canon.canonical_json(k).decode("utf-8"))
                         for k in order]
            self.assertEqual(positions, sorted(positions))

    def test_integer_edges(self):
        self.assertEqual(canon.canonical_json({"n": -0}), b'{"n":0}')
        self.assertEqual(canon.canonical_json({"n": 2 ** 53 - 1}),
                         b'{"n":9007199254740991}')
        self.assertEqual(canon.canonical_json({"n": -(2 ** 53) + 1}),
                         b'{"n":-9007199254740991}')
        for bad in (2 ** 53, -(2 ** 53), 1.0, float("nan")):
            with self.assertRaises(canon.CanonError):
                canon.canonical_json({"n": bad})

    def test_digest_list_order_sensitivity(self):
        a, b = canon.text_digest("a"), canon.text_digest("b")
        self.assertNotEqual(
            canon.composite_digest("aa11393:claim-agg:c1", [a, b]),
            canon.composite_digest("aa11393:claim-agg:c1", [b, a]))

    def test_domain_separation(self):
        a, b = canon.text_digest("a"), canon.text_digest("b")
        self.assertNotEqual(
            canon.composite_digest("aa11393:claim-agg:c1", [a, b]),
            canon.composite_digest("aa11393:dep-chain:c1", [a, b]))


if __name__ == "__main__":
    unittest.main()
