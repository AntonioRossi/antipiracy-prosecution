"""Mutation and rollback fixtures for the command write boundary."""

import os
import tempfile
import unittest
from unittest import mock

from structured_source.atomic import publish_set
from structured_source.errors import StructuredSourceError


class AtomicPublication(unittest.TestCase):
    def test_validated_set_publishes_together(self):
        with tempfile.TemporaryDirectory() as root:
            publish_set(root, {"one.txt": b"one", "nested/two.txt": b"two"},
                        {"one.txt": None, "nested/two.txt": None})
            with open(os.path.join(root, "one.txt"), "rb") as handle:
                self.assertEqual(handle.read(), b"one")
            with open(os.path.join(root, "nested", "two.txt"), "rb") as handle:
                self.assertEqual(handle.read(), b"two")

    def test_external_mutation_prevents_first_write(self):
        with tempfile.TemporaryDirectory() as root:
            path = os.path.join(root, "one.txt")
            with open(path, "wb") as handle:
                handle.write(b"external")
            with self.assertRaisesRegex(StructuredSourceError, "changed"):
                publish_set(root, {"one.txt": b"new"}, {"one.txt": b"old"})
            with open(path, "rb") as handle:
                self.assertEqual(handle.read(), b"external")

    def test_interrupted_multi_file_replace_rolls_back(self):
        with tempfile.TemporaryDirectory() as root:
            paths = [os.path.join(root, name) for name in ("one.txt", "two.txt")]
            for path, value in zip(paths, (b"old-one", b"old-two")):
                with open(path, "wb") as handle:
                    handle.write(value)
            real_replace = os.replace
            calls = {"count": 0}

            def interrupted(source, target):
                calls["count"] += 1
                if calls["count"] == 2:
                    raise KeyboardInterrupt("fixture interruption")
                return real_replace(source, target)

            with mock.patch("structured_source.atomic.os.replace", side_effect=interrupted):
                with self.assertRaises(KeyboardInterrupt):
                    publish_set(
                        root, {"one.txt": b"new-one", "two.txt": b"new-two"},
                        {"one.txt": b"old-one", "two.txt": b"old-two"})
            for path, value in zip(paths, (b"old-one", b"old-two")):
                with open(path, "rb") as handle:
                    self.assertEqual(handle.read(), value)

    def test_mutation_during_publication_stops_and_rolls_back_owned_write(self):
        with tempfile.TemporaryDirectory() as root:
            first = os.path.join(root, "one.txt")
            second = os.path.join(root, "two.txt")
            for path, value in ((first, b"old-one"), (second, b"old-two")):
                with open(path, "wb") as handle:
                    handle.write(value)
            real_replace = os.replace
            calls = {"count": 0}

            def mutate_after_first(source, target):
                calls["count"] += 1
                result = real_replace(source, target)
                if calls["count"] == 1:
                    with open(second, "wb") as handle:
                        handle.write(b"external-two")
                return result

            with mock.patch("structured_source.atomic.os.replace",
                            side_effect=mutate_after_first):
                with self.assertRaisesRegex(StructuredSourceError, "during"):
                    publish_set(
                        root, {"one.txt": b"new-one", "two.txt": b"new-two"},
                        {"one.txt": b"old-one", "two.txt": b"old-two"})
            with open(first, "rb") as handle:
                self.assertEqual(handle.read(), b"old-one")
            with open(second, "rb") as handle:
                self.assertEqual(handle.read(), b"external-two")

    def test_failed_new_nested_output_leaves_no_directory(self):
        with tempfile.TemporaryDirectory() as root:
            with mock.patch("structured_source.atomic.os.replace",
                            side_effect=OSError("fixture")):
                with self.assertRaises(OSError):
                    publish_set(root, {"nested/new.txt": b"new"},
                                {"nested/new.txt": None})
            self.assertFalse(os.path.lexists(os.path.join(root, "nested")))


if __name__ == "__main__":
    unittest.main()
