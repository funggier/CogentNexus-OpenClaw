from __future__ import annotations

import argparse
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


def load_runtime():
    spec = importlib.util.spec_from_file_location("cnx_runtime_windows_stop_test", ROOT / "skills/cogentnexus/scripts/runtime.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


runtime = load_runtime()


class WindowsStopLifecycleTests(unittest.TestCase):
    def config(self):
        return runtime.deep_merge(runtime.DEFAULT_CONFIG, {"supervisor": {"commandTimeoutSeconds": 1}})

    def test_windows_stop_force_terminates_desktop_and_server_trees(self):
        config = self.config()
        healthy = {"name": "ollama", "enabled": True, "healthy": True, "evidence": "fixture"}
        with mock.patch.object(runtime.os, "name", "nt"), \
             mock.patch.object(runtime, "ollama_probe", return_value=healthy), \
             mock.patch.object(runtime.shutil, "which", return_value=r"C:\\Windows\\System32\\taskkill.exe"), \
             mock.patch.object(runtime, "run_command", side_effect=[
                 {"ok": False, "exitCode": 128, "stderr": "not running"},
                 {"ok": True, "exitCode": 0, "stderr": ""},
             ]) as runner:
            result = runtime.stop_ollama(config)
        self.assertTrue(result["ok"])
        self.assertEqual(runner.call_count, 2)
        first = runner.call_args_list[0].args[0]
        second = runner.call_args_list[1].args[0]
        self.assertEqual(first[-4:], ["/IM", "ollama app.exe", "/T", "/F"])
        self.assertEqual(second[-4:], ["/IM", "ollama.exe", "/T", "/F"])

    def test_shutdown_verification_requires_requested_provider_to_be_down(self):
        config = self.config()
        with mock.patch.object(runtime, "gateway_probe", return_value={"enabled": True, "healthy": False}), \
             mock.patch.object(runtime, "ollama_probe", return_value={"enabled": True, "healthy": True}):
            _, stopped, _, safe = runtime.wait_for_runtime_stopped(config, timeout_seconds=0, require_ollama=True)
        self.assertTrue(stopped["gateway"])
        self.assertFalse(stopped["ollama"])
        self.assertFalse(safe)

    def test_lifecycle_stop_does_not_claim_safe_poweroff_when_provider_remains_up(self):
        config = self.config()
        args = argparse.Namespace(
            root=Path(tempfile.mkdtemp()), command_name="stop", reason="planned shutdown", owner="operator", provider=True
        )
        emitted = []
        with mock.patch.object(runtime, "load_config", return_value=config), \
             mock.patch.object(runtime, "maintenance_status", return_value=None), \
             mock.patch.object(runtime, "set_maintenance", return_value={"active": True}), \
             mock.patch.object(runtime, "openclaw_executable", return_value="openclaw"), \
             mock.patch.object(runtime, "run_command", return_value={"ok": True, "exitCode": 0}), \
             mock.patch.object(runtime, "stop_ollama", return_value={"ok": False, "exitCode": 128}), \
             mock.patch.object(runtime, "wait_for_runtime_stopped", return_value=(
                 {"gateway": {"healthy": False}, "ollama": {"enabled": True, "healthy": True}},
                 {"gateway": True, "ollama": False}, 2, False,
             )), \
             mock.patch.object(runtime, "append_runtime_event"), \
             mock.patch.object(runtime, "emit", side_effect=emitted.append):
            code = runtime.lifecycle_cmd(args)
        self.assertEqual(code, 2)
        self.assertFalse(emitted[-1]["safeToPowerOff"])
        self.assertFalse(emitted[-1]["verifiedStopped"]["ollama"])

    def test_lifecycle_stop_uses_verified_shutdown_as_terminal_truth(self):
        config = self.config()
        args = argparse.Namespace(
            root=Path(tempfile.mkdtemp()), command_name="stop", reason="planned shutdown", owner="operator", provider=True
        )
        emitted = []
        with mock.patch.object(runtime, "load_config", return_value=config), \
             mock.patch.object(runtime, "maintenance_status", return_value=None), \
             mock.patch.object(runtime, "set_maintenance", return_value={"active": True}), \
             mock.patch.object(runtime, "openclaw_executable", return_value="openclaw"), \
             mock.patch.object(runtime, "run_command", return_value={"ok": True, "exitCode": 0}), \
             mock.patch.object(runtime, "stop_ollama", return_value={"ok": True}), \
             mock.patch.object(runtime, "wait_for_runtime_stopped", return_value=(
                 {"gateway": {"healthy": False}, "ollama": {"enabled": True, "healthy": False}},
                 {"gateway": True, "ollama": True}, 1, True,
             )), \
             mock.patch.object(runtime, "append_runtime_event"), \
             mock.patch.object(runtime, "emit", side_effect=emitted.append):
            code = runtime.lifecycle_cmd(args)
        self.assertEqual(code, 0)
        self.assertTrue(emitted[-1]["safeToPowerOff"])
        self.assertTrue(emitted[-1]["verifiedStopped"]["ollama"])


if __name__ == "__main__":
    unittest.main()
