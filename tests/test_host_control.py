from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "cogentnexus" / "scripts" / "host_control.py"
spec = importlib.util.spec_from_file_location("cnx_host_control", SCRIPT)
cnx = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(cnx)


class HostControlTests(unittest.TestCase):
    def setUp(self):
        self.original_get = cnx.config_get
        self.original_set = cnx.config_set
        self.original_unset = cnx.config_unset

    def tearDown(self):
        cnx.config_get = self.original_get
        cnx.config_set = self.original_set
        cnx.config_unset = self.original_unset

    def test_apply_snapshots_absent_value_and_restore_unsets_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogent"
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
            root = Path(tmp) / ".cogent"
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
            root = Path(tmp) / ".cogent"
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

            # Disable must preserve the operator's newer value rather than
            # restoring the pre-CNX snapshot over it.
            result = cnx.restore_watchdog_compat(root)
            self.assertFalse(result["restored"])
            self.assertEqual(state["value"], 1800000)
            self.assertFalse(cnx.snapshot_path(root).exists())

    def test_passthrough_supervisor_does_not_apply_managed_compatibility(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogent"
            (root / "host").mkdir(parents=True)
            (root / "host" / "controller.json").write_text(
                json.dumps({"mode": "passthrough"}), encoding="utf-8"
            )
            self.assertFalse(cnx.should_apply(root, "supervisor", "tick"))
            self.assertTrue(cnx.should_apply(root, "enable", None))


if __name__ == "__main__":
    unittest.main()
