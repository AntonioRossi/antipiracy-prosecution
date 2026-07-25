"""Mutation and rollback fixtures for the command write boundary."""

import os
import tempfile
import unittest
from unittest import mock

from structured_source.atomic import publish_set
from structured_source.errors import StructuredSourceError


class AtomicPublication(unittest.TestCase):
    def test_symlink_root_is_rejected_before_writes(self):
        with tempfile.TemporaryDirectory() as container:
            real_root = os.path.join(container, "real")
            linked_root = os.path.join(container, "linked")
            os.mkdir(real_root)
            os.symlink(real_root, linked_root)
            with self.assertRaisesRegex(StructuredSourceError, "symlink"):
                publish_set(linked_root, {"escape.txt": b"new"},
                            {"escape.txt": None})
            self.assertFalse(os.path.lexists(
                os.path.join(real_root, "escape.txt")))

    def test_symlink_ancestor_and_target_are_rejected_before_writes(self):
        with tempfile.TemporaryDirectory() as root, \
                tempfile.TemporaryDirectory() as outside:
            linked = os.path.join(root, "linked")
            os.symlink(outside, linked)
            with self.assertRaisesRegex(StructuredSourceError, "symlink"):
                publish_set(root, {"linked/escape.txt": b"new"},
                            {"linked/escape.txt": None})
            self.assertFalse(os.path.lexists(
                os.path.join(outside, "escape.txt")))

            outside_file = os.path.join(outside, "outside.txt")
            with open(outside_file, "wb") as handle:
                handle.write(b"outside")
            target = os.path.join(root, "target.txt")
            os.symlink(outside_file, target)
            with self.assertRaisesRegex(StructuredSourceError, "symlink"):
                publish_set(root, {"target.txt": b"new"},
                            {"target.txt": b"outside"})
            with open(outside_file, "rb") as handle:
                self.assertEqual(handle.read(), b"outside")

    def test_ancestor_swap_cannot_redirect_an_inflight_replace(self):
        with tempfile.TemporaryDirectory() as root, \
                tempfile.TemporaryDirectory() as outside:
            nested = os.path.join(root, "nested")
            moved = os.path.join(root, "moved")
            os.mkdir(nested)
            target = os.path.join(nested, "target.txt")
            with open(target, "wb") as handle:
                handle.write(b"old")
            real_replace = os.replace
            attacked = {"done": False}

            def swap_ancestor(source, destination, **kwargs):
                if not attacked["done"]:
                    attacked["done"] = True
                    os.rename(nested, moved)
                    os.symlink(outside, nested)
                return real_replace(source, destination, **kwargs)

            with mock.patch("structured_source.atomic.os.replace",
                            side_effect=swap_ancestor):
                with self.assertRaisesRegex(StructuredSourceError, "symlink"):
                    publish_set(root, {"nested/target.txt": b"new"},
                                {"nested/target.txt": b"old"})
            self.assertFalse(os.path.lexists(
                os.path.join(outside, "target.txt")))
            with open(os.path.join(moved, "target.txt"), "rb") as handle:
                self.assertEqual(handle.read(), b"old")

    def test_validated_set_publishes_together(self):
        with tempfile.TemporaryDirectory() as root:
            publish_set(root, {"one.txt": b"one", "nested/two.txt": b"two"},
                        {"one.txt": None, "nested/two.txt": None})
            with open(os.path.join(root, "one.txt"), "rb") as handle:
                self.assertEqual(handle.read(), b"one")
            with open(os.path.join(root, "nested", "two.txt"), "rb") as handle:
                self.assertEqual(handle.read(), b"two")

    def test_validated_set_replaces_and_deletes_together(self):
        with tempfile.TemporaryDirectory() as root:
            deleted = os.path.join(root, "delete.txt")
            replaced = os.path.join(root, "replace.txt")
            for path, value in ((deleted, b"delete"), (replaced, b"old")):
                with open(path, "wb") as handle:
                    handle.write(value)
            publish_set(
                root, {"delete.txt": None, "replace.txt": b"new"},
                {"delete.txt": b"delete", "replace.txt": b"old"})
            self.assertFalse(os.path.lexists(deleted))
            with open(replaced, "rb") as handle:
                self.assertEqual(handle.read(), b"new")

    def test_external_mutation_prevents_first_write(self):
        with tempfile.TemporaryDirectory() as root:
            path = os.path.join(root, "one.txt")
            with open(path, "wb") as handle:
                handle.write(b"external")
            with self.assertRaisesRegex(StructuredSourceError, "changed"):
                publish_set(root, {"one.txt": b"new"}, {"one.txt": b"old"})
            with open(path, "rb") as handle:
                self.assertEqual(handle.read(), b"external")

    def test_deletion_requires_an_exact_existing_prestate(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaisesRegex(StructuredSourceError, "malformed"):
                publish_set(root, {"absent.txt": None}, {"absent.txt": None})

    def test_staging_failures_leave_no_temporary_or_created_directory(self):
        class FaultyHandle:
            def __init__(self, handle, operation):
                self.handle = handle
                self.operation = operation

            def __enter__(self):
                return self

            def __exit__(self, *unused):
                self.handle.close()

            def write(self, data):
                if self.operation == "write":
                    raise OSError("fixture write failure")
                return self.handle.write(data)

            def flush(self):
                if self.operation == "flush":
                    raise OSError("fixture flush failure")
                return self.handle.flush()

            def fileno(self):
                return self.handle.fileno()

        def assert_clean(root):
            self.assertFalse(os.path.lexists(os.path.join(root, "new")))
            self.assertFalse(any(
                name.startswith(".ssp-publish-")
                for unused_directory, unused_dirs, files in os.walk(root)
                for name in files))

        for operation in ("fchmod", "write", "flush", "fsync"):
            with self.subTest(operation=operation), \
                    tempfile.TemporaryDirectory() as root:
                real_fdopen = os.fdopen
                if operation in {"write", "flush"}:
                    patcher = mock.patch(
                        "structured_source.atomic.os.fdopen",
                        side_effect=lambda descriptor, mode, selected=operation:
                        FaultyHandle(real_fdopen(descriptor, mode), selected))
                else:
                    patcher = mock.patch(
                        "structured_source.atomic.os." + operation,
                        side_effect=OSError("fixture %s failure" % operation))
                with patcher, self.assertRaises(OSError):
                    publish_set(root, {"new/nested.txt": b"new"},
                                {"new/nested.txt": None})
                assert_clean(root)

    def test_interrupted_multi_file_replace_rolls_back(self):
        with tempfile.TemporaryDirectory() as root:
            paths = [os.path.join(root, name) for name in ("one.txt", "two.txt")]
            for path, value in zip(paths, (b"old-one", b"old-two")):
                with open(path, "wb") as handle:
                    handle.write(value)
            real_replace = os.replace
            calls = {"count": 0}

            def interrupted(source, target, **kwargs):
                calls["count"] += 1
                if calls["count"] == 2:
                    raise KeyboardInterrupt("fixture interruption")
                return real_replace(source, target, **kwargs)

            with mock.patch("structured_source.atomic.os.replace", side_effect=interrupted):
                with self.assertRaises(KeyboardInterrupt):
                    publish_set(
                        root, {"one.txt": b"new-one", "two.txt": b"new-two"},
                        {"one.txt": b"old-one", "two.txt": b"old-two"})
            for path, value in zip(paths, (b"old-one", b"old-two")):
                with open(path, "rb") as handle:
                    self.assertEqual(handle.read(), value)

    def test_interrupted_replace_after_delete_restores_complete_prestate(self):
        with tempfile.TemporaryDirectory() as root:
            deleted = os.path.join(root, "one-delete.txt")
            replaced = os.path.join(root, "two-replace.txt")
            for path, value in ((deleted, b"old-delete"),
                                (replaced, b"old-replace")):
                with open(path, "wb") as handle:
                    handle.write(value)
            real_replace = os.replace
            calls = {"count": 0}

            def interrupt_first_replace(source, target, **kwargs):
                calls["count"] += 1
                if calls["count"] == 1:
                    raise KeyboardInterrupt("fixture interruption")
                return real_replace(source, target, **kwargs)

            with mock.patch("structured_source.atomic.os.replace",
                            side_effect=interrupt_first_replace):
                with self.assertRaises(KeyboardInterrupt):
                    publish_set(
                        root,
                        {"one-delete.txt": None, "two-replace.txt": b"new"},
                        {"one-delete.txt": b"old-delete",
                         "two-replace.txt": b"old-replace"})
            with open(deleted, "rb") as handle:
                self.assertEqual(handle.read(), b"old-delete")
            with open(replaced, "rb") as handle:
                self.assertEqual(handle.read(), b"old-replace")

    def test_mutation_during_publication_stops_and_rolls_back_owned_write(self):
        with tempfile.TemporaryDirectory() as root:
            first = os.path.join(root, "one.txt")
            second = os.path.join(root, "two.txt")
            for path, value in ((first, b"old-one"), (second, b"old-two")):
                with open(path, "wb") as handle:
                    handle.write(value)
            real_replace = os.replace
            calls = {"count": 0}

            def mutate_after_first(source, target, **kwargs):
                calls["count"] += 1
                result = real_replace(source, target, **kwargs)
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

    def test_guard_mutation_rolls_back_owned_output(self):
        with tempfile.TemporaryDirectory() as root:
            output = os.path.join(root, "output.txt")
            guard = os.path.join(root, "guard.txt")
            for path, value in ((output, b"old-output"),
                                (guard, b"old-guard")):
                with open(path, "wb") as handle:
                    handle.write(value)
            real_replace = os.replace
            calls = {"count": 0}

            def mutate_guard(source, target, **kwargs):
                calls["count"] += 1
                result = real_replace(source, target, **kwargs)
                if calls["count"] == 1:
                    with open(guard, "wb") as handle:
                        handle.write(b"external-guard")
                return result

            with mock.patch("structured_source.atomic.os.replace",
                            side_effect=mutate_guard):
                with self.assertRaisesRegex(StructuredSourceError, "during"):
                    publish_set(
                        root, {"output.txt": b"new-output"},
                        {"output.txt": b"old-output"},
                        {"guard.txt": b"old-guard"})
            with open(output, "rb") as handle:
                self.assertEqual(handle.read(), b"old-output")
            with open(guard, "rb") as handle:
                self.assertEqual(handle.read(), b"external-guard")

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
