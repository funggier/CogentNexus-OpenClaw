from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus" / "scripts"
sys.path.insert(0, str(SCRIPTS))
SCRIPT = SCRIPTS / "lifecycle_v091.py"
spec = importlib.util.spec_from_file_location("cnx_lifecycle_v091", SCRIPT)
cnx = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(cnx)


class LifecycleV091Tests(unittest.TestCase):
    def test_confirmation_requires_exact_y_semantics(self):
        with mock.patch("builtins.input", return_value="y"):
            self.assertTrue(cnx.confirm("reset"))
        with mock.patch("builtins.input", return_value="Y"):
            self.assertTrue(cnx.confirm("uninstall"))
        for answer in ("", "n", "yes", "1"):
            with self.subTest(answer=answer), mock.patch("builtins.input", return_value=answer):
                self.assertFalse(cnx.confirm("reset"))

    def test_cancelled_reset_performs_no_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogent"
            with (
                mock.patch.object(cnx, "confirm", return_value=False),
                mock.patch.object(cnx, "disable_managed") as disable,
                mock.patch.object(cnx, "disable_startup") as startup,
                mock.patch.object(cnx, "reset_plugin_configuration") as config,
            ):
                self.assertEqual(cnx.reset(root), 0)
                disable.assert_not_called()
                startup.assert_not_called()
                config.assert_not_called()

    def test_reset_recreates_fresh_state_then_enables(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogent"
            root.mkdir(parents=True)
            calls: list[str] = []

            def fake_run(cmd, timeout=180, check=True):
                command = " ".join(str(item) for item in cmd)
                if " init" in command:
                    calls.append("init")
                elif " policy apply" in command:
                    calls.append("policy")
                elif " enable" in command:
                    calls.append("enable")
                return subprocess.CompletedProcess(cmd, 0, "", "")

            with (
                mock.patch.object(cnx, "confirm", return_value=True),
                mock.patch.object(cnx, "disable_managed", side_effect=lambda _root: calls.append("disable")),
                mock.patch.object(cnx, "disable_startup", side_effect=lambda _root: calls.append("startup-disable")),
                mock.patch.object(cnx, "reset_plugin_configuration", side_effect=lambda: calls.append("config-reset")),
                mock.patch.object(cnx, "bootstrap_ticket_database", side_effect=lambda: calls.append("bootstrap")),
                mock.patch.object(cnx, "run", side_effect=fake_run),
                mock.patch.object(cnx, "verify_plugin_loaded", return_value={"status": "loaded"}),
                mock.patch.object(cnx, "gateway_health", return_value={"healthy": True}),
            ):
                self.assertEqual(cnx.reset(root), 0)

            self.assertEqual(
                calls,
                ["disable", "startup-disable", "config-reset", "init", "bootstrap", "policy", "enable"],
            )
            self.assertFalse(root.exists(), "fake init intentionally proves old state was removed before reinitialization")

    def test_cancelled_uninstall_performs_no_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogent"
            with (
                mock.patch.object(cnx, "confirm", return_value=False),
                mock.patch.object(cnx, "disable_managed") as disable,
                mock.patch.object(cnx, "uninstall_plugin") as uninstall_plugin,
            ):
                self.assertEqual(cnx.uninstall(root), 0)
                disable.assert_not_called()
                uninstall_plugin.assert_not_called()

    def test_uninstall_schedules_all_owned_cleanup_only_after_native_health(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogent"
            local_app = Path(tmp) / "LocalAppData"
            calls: list[str] = []
            with (
                mock.patch.object(cnx, "confirm", return_value=True),
                mock.patch.object(cnx, "disable_managed", side_effect=lambda _root: calls.append("disable")),
                mock.patch.object(cnx, "disable_startup", side_effect=lambda _root: calls.append("startup-disable")),
                mock.patch.object(cnx, "uninstall_plugin", side_effect=lambda: calls.append("plugin-uninstall")),
                mock.patch.object(cnx, "gateway_health", side_effect=lambda: calls.append("gateway-health") or {"healthy": True}),
                mock.patch.object(cnx, "schedule_windows_cleanup", side_effect=lambda _paths: calls.append("cleanup")) as cleanup,
                mock.patch.object(cnx.os, "name", "nt"),
                mock.patch.dict(os.environ, {"LOCALAPPDATA": str(local_app)}, clear=False),
            ):
                self.assertEqual(cnx.uninstall(root), 0)

            self.assertEqual(calls, ["disable", "startup-disable", "plugin-uninstall", "gateway-health", "cleanup"])
            paths = [path.resolve() for path in cleanup.call_args.args[0]]
            self.assertIn(root.resolve(), paths)
            self.assertIn((local_app / "CogentNexus").resolve(), paths)
            self.assertIn(cnx.SKILL.resolve(), paths)
            self.assertIn(cnx.LAUNCHER.resolve(), paths)

    def test_uninstall_never_schedules_file_cleanup_when_native_gateway_is_unhealthy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".cogent"
            with (
                mock.patch.object(cnx, "confirm", return_value=True),
                mock.patch.object(cnx, "disable_managed"),
                mock.patch.object(cnx, "disable_startup"),
                mock.patch.object(cnx, "uninstall_plugin"),
                mock.patch.object(cnx, "gateway_health", return_value={"healthy": False}),
                mock.patch.object(cnx, "schedule_windows_cleanup") as cleanup,
                mock.patch.object(cnx.os, "name", "nt"),
            ):
                self.assertEqual(cnx.uninstall(root), 1)
                cleanup.assert_not_called()


if __name__ == "__main__":
    unittest.main()
