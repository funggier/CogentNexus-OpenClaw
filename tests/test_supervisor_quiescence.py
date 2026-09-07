import json
import importlib.util
import multiprocessing
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


def _hold_operation_lock(root, ready, release):
    with q._operation_lock(Path(root)):
        ready.set()
        release.wait(3.0)


def _acquire_with_timeout(root, result):
    try:
        q.acquire(Path(root), "owner-b", now=101.0, ttl=30.0, timeout=0.05, poll=0.005)
    except BaseException as exc:
        result.put(type(exc).__name__)
    else:
        result.put("acquired")


def _release_with_barrier(root, token, checked, proceed, result):
    original_read = q._read_raw
    reads = 0

    def delayed_read(path):
        nonlocal reads
        value = original_read(path)
        reads += 1
        if reads == 2:
            checked.set()
            proceed.wait(2.0)
        return value

    q._read_raw = delayed_read
    try:
        q.release(Path(root), "owner-a", token=token, now=112.0)
    except BaseException as exc:
        result.put(type(exc).__name__)
    else:
        result.put("released")


def _acquire_replacement(root, result):
    try:
        q.acquire(Path(root), "owner-b", now=111.0, ttl=30.0)
    except BaseException as exc:
        result.put(type(exc).__name__)
    else:
        result.put("acquired")


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
            context = multiprocessing.get_context("spawn")
            checked = context.Event()
            proceed = context.Event()
            release_result = context.Queue()
            acquire_result = context.Queue()
            old_process = context.Process(
                target=_release_with_barrier,
                args=(str(root), lease_a["token"], checked, proceed, release_result),
            )
            replacement_process = context.Process(
                target=_acquire_replacement, args=(str(root), acquire_result)
            )
            old_process.start()
            try:
                self.assertTrue(checked.wait(2.0))
                replacement_process.start()
                time.sleep(0.1)
                self.assertTrue(replacement_process.is_alive())
                proceed.set()
                old_process.join(2.0)
                replacement_process.join(2.0)
            finally:
                proceed.set()
                for process in (old_process, replacement_process):
                    if process.is_alive():
                        process.terminate()
                    process.join(2.0)

            self.assertFalse(old_process.is_alive())
            self.assertFalse(replacement_process.is_alive())
            self.assertIn(release_result.get(timeout=1.0), {"released", "QuiescenceOwnerError"})
            self.assertEqual(acquire_result.get(timeout=1.0), "acquired")
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

    def test_release_absent_is_side_effect_free(self):
        with TemporaryDirectory() as d:
            root = Path(d) / ".cogentnexus-openclaw"
            self.assertFalse(root.exists())
            released = q.release(root, "owner-a", now=101.0)
            self.assertFalse(released["released"])
            self.assertFalse(root.exists())

    def test_acquire_timeout_is_bounded_when_operation_lock_is_held(self):
        with TemporaryDirectory() as d:
            root = Path(d) / ".cogentnexus-openclaw"
            context = multiprocessing.get_context("spawn")
            ready = context.Event()
            release = context.Event()
            result = context.Queue()
            holder = context.Process(target=_hold_operation_lock, args=(str(root), ready, release))
            waiter = context.Process(target=_acquire_with_timeout, args=(str(root), result))
            holder.start()
            try:
                self.assertTrue(ready.wait(2.0))
                waiter.start()
                waiter.join(0.5)
                if waiter.is_alive():
                    waiter.terminate()
                    waiter.join(2.0)
                    self.fail("acquire(timeout=0.05) blocked on the operation lock")
                release.set()
                holder.join(2.0)
            finally:
                release.set()
                if holder.is_alive():
                    holder.terminate()
                holder.join(2.0)
                if waiter.is_alive():
                    waiter.terminate()
                waiter.join(2.0)
            self.assertFalse(holder.is_alive())
            self.assertEqual(result.get(timeout=1.0), "QuiescenceTimeoutError")

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
