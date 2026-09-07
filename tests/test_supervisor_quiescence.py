import json
import importlib.util
import sys
import threading
import time
import unittest
from unittest import mock
from pathlib import Path
from tempfile import TemporaryDirectory

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus-openclaw" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import supervisor_quiescence as q
HOST_SPEC = importlib.util.spec_from_file_location("host_quiescence_under_test", SCRIPTS / "host.py")
assert HOST_SPEC and HOST_SPEC.loader
host = importlib.util.module_from_spec(HOST_SPEC)
HOST_SPEC.loader.exec_module(host)


class SupervisorQuiescenceTests(unittest.TestCase):
    def test_acquire_release_restores_and_is_observable(self):
        with TemporaryDirectory() as d:
            root = Path(d) / ".cogentnexus-openclaw"
            lease = q.acquire(root, "owner-a", now=100.0, ttl=30.0)
            self.assertEqual(lease["owner"], "owner-a")
            self.assertEqual(q.read(root, now=101.0)["status"], "active")
            released = q.release(root, "owner-a", now=101.0)
            self.assertTrue(released["released"])
            self.assertEqual(q.read(root)["status"], "absent")

    def test_concurrent_second_writer_fails_closed(self):
        with TemporaryDirectory() as d:
            root = Path(d) / ".cogentnexus-openclaw"
            q.acquire(root, "owner-a", now=100.0, ttl=30.0)
            with self.assertRaises(q.QuiescenceBusyError):
                q.acquire(root, "owner-b", now=101.0, ttl=30.0)

    def test_stale_lease_is_reclaimed_only_by_new_owner(self):
        with TemporaryDirectory() as d:
            root = Path(d) / ".cogentnexus-openclaw"
            q.acquire(root, "owner-a", now=100.0, ttl=10.0)
            lease = q.acquire(root, "owner-b", now=111.0, ttl=10.0)
            self.assertEqual(lease["owner"], "owner-b")
            with self.assertRaises(q.QuiescenceOwnerError):
                q.release(root, "owner-a", now=112.0)

    def test_release_cannot_unlink_replacement_lease_during_owner_check(self):
        with TemporaryDirectory() as d:
            root = Path(d) / ".cogentnexus-openclaw"
            lease_a = q.acquire(root, "owner-a", now=100.0, ttl=10.0)
            checked = threading.Event()
            continue_release = threading.Event()
            replacement_done = threading.Event()
            errors = []
            original_read = q._read_raw

            def delayed_read(path):
                value = original_read(path)
                if threading.current_thread().name == "old-release":
                    checked.set()
                    if not continue_release.wait(2.0):
                        errors.append("release test barrier timed out")
                return value

            def release_old():
                try:
                    q.release(root, "owner-a", token=lease_a["token"], now=112.0)
                except BaseException as exc:
                    errors.append(exc)

            def acquire_replacement():
                try:
                    q.acquire(root, "owner-b", now=111.0, ttl=30.0)
                    replacement_done.set()
                except BaseException as exc:
                    errors.append(exc)

            with mock.patch.object(q, "_read_raw", side_effect=delayed_read):
                old_thread = threading.Thread(target=release_old, name="old-release")
                old_thread.start()
                self.assertTrue(checked.wait(1.0))
                replacement_thread = threading.Thread(target=acquire_replacement, name="replacement")
                replacement_thread.start()
                self.assertFalse(replacement_done.wait(0.1))
                continue_release.set()
                old_thread.join(2.0)
                replacement_thread.join(2.0)

            self.assertFalse(old_thread.is_alive())
            self.assertFalse(replacement_thread.is_alive())
            self.assertEqual(errors, [])
            self.assertEqual(q.read(root, now=112.0)["owner"], "owner-b")


    def test_timeout_is_reported_without_partial_active_lease(self):
        with TemporaryDirectory() as d:
            root = Path(d) / ".cogentnexus-openclaw"
            q.acquire(root, "owner-a", now=100.0, ttl=100.0)
            with self.assertRaises(q.QuiescenceTimeoutError):
                q.acquire(root, "owner-b", now=101.0, ttl=100.0, timeout=0.01)
            self.assertEqual(q.read(root, now=101.0)["owner"], "owner-a")

    def test_release_is_idempotent_after_rollback(self):
        with TemporaryDirectory() as d:
            root = Path(d) / ".cogentnexus-openclaw"
            q.acquire(root, "owner-a", now=100.0, ttl=30.0)
            self.assertTrue(q.release(root, "owner-a", now=101.0)["released"])
            self.assertFalse(q.release(root, "owner-a", now=102.0)["released"])

    def test_supervisor_tick_is_quiesced_before_any_runtime_probe(self):
        with TemporaryDirectory() as d:
            root = Path(d) / ".cogentnexus-openclaw"
            q.acquire(root, "enable-owner", ttl=30.0)
            with mock.patch.object(host, "initialize"), mock.patch.object(
                host, "load_state", return_value={"mode": "managed", "desiredGateway": "running"}
            ), mock.patch.object(host, "gateway_status") as gateway:
                result = host.supervisor_tick(root, execute_safe=True)
            self.assertEqual(result["result"], "quiesced")
            gateway.assert_not_called()


if __name__ == "__main__":
    unittest.main()
