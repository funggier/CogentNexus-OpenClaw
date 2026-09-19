from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "cogentnexus-openclaw" / "scripts" / "host_control.py"
spec = importlib.util.spec_from_file_location("cnx_host_control_schema_compat", SCRIPT)
cnx = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(cnx)


class HostWatchdogSchemaCompatTests(unittest.TestCase):
    def test_config_path_supported_distinguishes_removed_path_from_valid_unset(self):
        original_run = cnx.run
        try:
            cnx.run = lambda *_args, **_kwargs: subprocess.CompletedProcess(
                ["stub"], 1,
                stdout=json.dumps({"ok": False, "error": {"message": "Unknown config path: diagnostics.stuckSessionAbortMs. Run openclaw config schema to inspect valid paths."}}),
                stderr="",
            )
            self.assertFalse(cnx.config_path_supported(cnx.WATCHDOG_PATH))

            cnx.run = lambda *_args, **_kwargs: subprocess.CompletedProcess(
                ["stub"], 1,
                stdout=json.dumps({"ok": False, "error": {"message": "Config path is valid but unset: diagnostics.stuckSessionAbortMs."}}),
                stderr="",
            )
            self.assertTrue(cnx.config_path_supported(cnx.WATCHDOG_PATH))
        finally:
            cnx.run = original_run

    def test_apply_skips_removed_watchdog_schema_without_config_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            root.joinpath("host").mkdir(parents=True)
            cnx.snapshot_path(root).write_text(json.dumps({
                "schemaVersion": 1,
                "path": cnx.WATCHDOG_PATH,
                "originalPresent": False,
                "originalValue": None,
                "managedValue": cnx.MANAGED_WATCHDOG_ABORT_MS,
                "capturedAt": "2026-09-19T00:00:00+00:00",
                "applied": True,
            }), encoding="utf-8")

            original_supported = cnx.config_path_supported
            original_get = cnx.config_get
            original_set = cnx.config_set
            original_unset = cnx.config_unset
            try:
                cnx.config_path_supported = lambda _path: False
                cnx.config_get = lambda _path: (_ for _ in ()).throw(AssertionError("config_get must not run"))
                cnx.config_set = lambda *_args: (_ for _ in ()).throw(AssertionError("config_set must not run"))
                cnx.config_unset = lambda *_args: (_ for _ in ()).throw(AssertionError("config_unset must not run"))

                result = cnx.apply_watchdog_compat(root)
                self.assertEqual(result["reason"], "unsupported-by-host")
                self.assertFalse(result["changed"])
                snapshot = json.loads(cnx.snapshot_path(root).read_text(encoding="utf-8"))
                self.assertFalse(snapshot["applied"])
                self.assertTrue(snapshot["schemaUnsupported"])
            finally:
                cnx.config_path_supported = original_supported
                cnx.config_get = original_get
                cnx.config_set = original_set
                cnx.config_unset = original_unset

    def test_restore_skips_removed_watchdog_schema_without_config_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogentnexus-openclaw"
            root.joinpath("host").mkdir(parents=True)
            cnx.snapshot_path(root).write_text(json.dumps({
                "schemaVersion": 1,
                "path": cnx.WATCHDOG_PATH,
                "originalPresent": False,
                "originalValue": None,
                "managedValue": cnx.MANAGED_WATCHDOG_ABORT_MS,
                "capturedAt": "2026-09-19T00:00:00+00:00",
                "applied": False,
            }), encoding="utf-8")

            original_supported = cnx.config_path_supported
            original_get = cnx.config_get
            original_set = cnx.config_set
            original_unset = cnx.config_unset
            try:
                cnx.config_path_supported = lambda _path: False
                cnx.config_get = lambda _path: (_ for _ in ()).throw(AssertionError("config_get must not run"))
                cnx.config_set = lambda *_args: (_ for _ in ()).throw(AssertionError("config_set must not run"))
                cnx.config_unset = lambda *_args: (_ for _ in ()).throw(AssertionError("config_unset must not run"))

                result = cnx.restore_watchdog_compat(root)
                self.assertEqual(result, {"restored": False, "reason": "unsupported-by-host"})
            finally:
                cnx.config_path_supported = original_supported
                cnx.config_get = original_get
                cnx.config_set = original_set
                cnx.config_unset = original_unset


if __name__ == "__main__":
    unittest.main()
