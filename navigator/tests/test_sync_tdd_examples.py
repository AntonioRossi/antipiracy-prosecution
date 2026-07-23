"""Duplicate-safe ingestion tests for the TDD fixture projection tool."""

import os
import sys
import tempfile
import unittest

NAV = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, NAV)
sys.path.insert(0, os.path.join(NAV, "tools"))

from lib import canon  # noqa: E402
import sync_tdd_examples as sync_tool  # noqa: E402


class TestSyncTddExamples(unittest.TestCase):

    def _run(self, first_block, first_fixture):
        with tempfile.TemporaryDirectory() as temp:
            tdd = os.path.join(temp, "TDD.md")
            fixtures = os.path.join(temp, "fixtures")
            os.mkdir(fixtures)
            with open(tdd, "w", encoding="utf-8") as fh:
                fh.write("```json\n%s\n```\n```json\n{\"x\":1}\n```\n"
                         % first_block)
            with open(os.path.join(fixtures, "na_excerpt.json"), "w",
                      encoding="utf-8") as fh:
                fh.write(first_fixture)
            with open(os.path.join(fixtures, "af_excerpt.json"), "w",
                      encoding="utf-8") as fh:
                fh.write('{"x":1}')

            previous_tdd, previous_fix = sync_tool.TDD, sync_tool.FIX
            sync_tool.TDD, sync_tool.FIX = tdd, fixtures
            try:
                sync_tool.main()
                with open(tdd, encoding="utf-8") as fh:
                    return fh.read()
            finally:
                sync_tool.TDD, sync_tool.FIX = previous_tdd, previous_fix

    def test_rejects_duplicate_key_in_tdd_block(self):
        with self.assertRaises(canon.CanonError):
            self._run('{"x":1,"x":2}', '{"x":1}')

    def test_rejects_duplicate_key_in_fixture(self):
        with self.assertRaises(canon.CanonError):
            self._run('{"x":1}', '{"x":1,"x":2}')

    def test_projects_duplicate_free_inputs(self):
        output = self._run('{"x":0}', '{"x":2}')
        self.assertIn('"x": 2', output)


if __name__ == "__main__":
    unittest.main()
