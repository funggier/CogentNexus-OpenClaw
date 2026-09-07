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
