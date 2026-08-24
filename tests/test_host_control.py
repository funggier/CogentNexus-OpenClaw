from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "cogentnexus-openclaw" / "scripts" / "host_control.py"
spec = importlib.util.spec_from_file_location("cnx_host_control", SCRIPT)
cnx = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(cnx)


class HostControlTests(unittest.TestCase):
    def setUp(self):
        self.original_get = cnx.config_get
        self.original_set = cnx.config_set
        self.original_unset = cnx.config_unset
        self.original_delegate = cnx.delegate
        self.original_subprocess_run = cnx.subprocess.run
        self.original_argv = list(sys.argv)

    def tearDown(self):
        cnx.config_get = self.original_get
        cnx.config_set = self.original_set
        cnx.config_unset = self.original_unset
        cnx.delegate = self.original_delegate
        cnx.subprocess.run = self.original_subprocess_run
        sys.argv = self.original_argv

    def test_apply_snapshots_absent_value_and_restore_unsets_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            state = {"present": False, "value": None}
            cnx.config_get = lambda _path: (state["present"], state["value"])
            cnx.config_set = lambda _path, value: state.update(present=True, value=value)
            cnx.config_unset = lambda _path: state.update(present=False, value=None)

            applied = cnx.apply_watchdog_compat(root)
            self.assertTrue(applied["changed"])
            self.assertEqual(state["value"], cnx.MANAGED_WATCHDOG_ABORT_MS)
            snapshot = json.loads(cnx.snapshot_path(root).read_text(encoding="utf-8"))
            self.assertFalse(snapshot["originalPresent"])
            self.assertTrue(snapshot["applied"])

            restored = cnx.restore_watchdog_compat(root)
            self.assertTrue(restored["restored"])
            self.assertFalse(state["present"])
            self.assertFalse(cnx.snapshot_path(root).exists())

    def test_restore_returns_original_operator_value(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            state = {"present": True, "value": 900000}
            cnx.config_get = lambda _path: (state["present"], state["value"])
            cnx.config_set = lambda _path, value: state.update(present=True, value=value)
            cnx.config_unset = lambda _path: state.update(present=False, value=None)

            cnx.apply_watchdog_compat(root)
            self.assertEqual(state["value"], cnx.MANAGED_WATCHDOG_ABORT_MS)
            cnx.restore_watchdog_compat(root)
            self.assertEqual(state["value"], 900000)

    def test_supervisor_never_overwrites_an_operator_change_after_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            state = {"present": True, "value": 600000}
            cnx.config_get = lambda _path: (state["present"], state["value"])
            cnx.config_set = lambda _path, value: state.update(present=True, value=value)
            cnx.config_unset = lambda _path: state.update(present=False, value=None)

            cnx.apply_watchdog_compat(root)
            state["value"] = 1800000  # operator changed OpenClaw config while managed
            with self.assertRaises(RuntimeError):
                cnx.apply_watchdog_compat(root)
            self.assertEqual(state["value"], 1800000)
            snapshot = json.loads(cnx.snapshot_path(root).read_text(encoding="utf-8"))
            self.assertFalse(snapshot["applied"])
            self.assertEqual(snapshot["operatorValue"], 1800000)

            result = cnx.restore_watchdog_compat(root)
            self.assertFalse(result["restored"])
            self.assertEqual(state["value"], 1800000)
            self.assertFalse(cnx.snapshot_path(root).exists())

    def test_failed_disable_reapplies_managed_watchdog_fence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            state = {"present": True, "value": 600000}
            cnx.config_get = lambda _path: (state["present"], state["value"])
            cnx.config_set = lambda _path, value: state.update(present=True, value=value)
            cnx.config_unset = lambda _path: state.update(present=False, value=None)

            cnx.apply_watchdog_compat(root)
            self.assertEqual(state["value"], cnx.MANAGED_WATCHDOG_ABORT_MS)

            cnx.delegate = lambda _argv: 7
            sys.argv = [str(SCRIPT), "--root", str(root), "disable"]
            code = cnx.main()

            self.assertEqual(code, 7)
            self.assertEqual(state["value"], cnx.MANAGED_WATCHDOG_ABORT_MS)
            snapshot = json.loads(cnx.snapshot_path(root).read_text(encoding="utf-8"))
            self.assertTrue(snapshot["applied"])
            self.assertEqual(snapshot["originalValue"], 600000)
            events = [json.loads(line) for line in cnx.audit_path(root).read_text(encoding="utf-8").splitlines()]
            self.assertEqual(events[-1]["action"], "watchdog-compat-disable-rollback")
            self.assertEqual(events[-1]["delegateExitCode"], 7)
            self.assertIsNone(events[-1]["rollbackError"])

    def test_passthrough_supervisor_does_not_apply_managed_compatibility(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            (root / "host").mkdir(parents=True)
            (root / "host" / "controller.json").write_text(
                json.dumps({"mode": "passthrough"}), encoding="utf-8"
            )
            self.assertFalse(cnx.should_apply(root, "supervisor", "tick"))
            self.assertTrue(cnx.should_apply(root, "enable", None))

    def test_delegate_relays_captured_host_stdout_and_stderr(self):
        seen = {}

        def fake_run(cmd, **kwargs):
            seen["cmd"] = cmd
            seen["kwargs"] = kwargs
            return subprocess.CompletedProcess(cmd, 7, stdout='{"result":"ok"}\n', stderr="host-warning\n")

        cnx.subprocess.run = fake_run
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = cnx.delegate(["status"])

        self.assertEqual(code, 7)
        self.assertEqual(stdout.getvalue(), '{"result":"ok"}\n')
        self.assertEqual(stderr.getvalue(), "host-warning\n")
        self.assertTrue(seen["kwargs"]["capture_output"])
        self.assertTrue(seen["kwargs"]["text"])
        self.assertEqual(Path(seen["cmd"][1]), cnx.HOST)

    def test_captured_text_accepts_missing_windows_stream(self):
        self.assertEqual(cnx.captured_text(None), "")
        self.assertEqual(cnx.captured_text(b"abc"), "abc")


if __name__ == "__main__":
    unittest.main()
