#!/usr/bin/env python3
"""Task CNX-20260825-063/064 runtime-ownership unit tests.

Unit-level contract checks complementing the executable integration coverage
in ``test_runtime_authority_integration.py``.
"""
from __future__ import annotations

import importlib
import os
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent / "skills" / "cogentnexus-openclaw" / "scripts"
sys.path.insert(0, str(SCRIPTS))

runtime_authority = importlib.import_module("runtime_authority")


class RuntimeAuthorityTests(unittest.TestCase):
    def test_01_executor_venv_is_never_durable_authority(self):
        """A bootstrap interpreter inside an executor venv must resolve to its base, not the venv."""
        import json as _json
        from unittest import mock

        base = Path("X:/realbase/python.exe")
        calls = iter([
            _json.dumps({"is_venv": True, "base_exec": str(base)}),
            _json.dumps({"is_venv": False, "base_exec": ""}),
        ])

        def fake_run(cmd, **kwargs):
            class R:
                returncode = 0
                stdout = next(calls)
                stderr = ""
            return R()

        with mock.patch.object(runtime_authority.subprocess, "run", side_effect=fake_run), \
             mock.patch.object(Path, "exists", lambda self: True):
            resolved = runtime_authority.resolve_base_interpreter(Path("X:/executor/venv/Scripts/python.exe"))
        self.assertNotIn("executor", str(resolved).lower())
        self.assertNotIn("venv", str(resolved).lower())

    def test_02_launcher_generation_uses_owned_interpreter(self):
        """install.ps1 launcher text must interpolate the owned foreground interpreter."""
        text = (HERE.parent / "scripts" / "install.ps1").read_text(encoding="utf-8")
        marker = "$launcherText ="
        first_line = text[text.index(marker):].splitlines()[0]
        self.assertIn("$ownedPython", first_line,
                      "launcher generation must interpolate the owned foreground interpreter")
        # provisioning happens before durable launcher generation, fail-closed
        self.assertIn("ensure-runtime", text)
        self.assertIn("--application-data-root", text)

    def test_03_startup_task_uses_owned_background_interpreter(self):
        """startup.py must source {{PYTHON}} from the owned runtime authority, fail-closed."""
        source = (SCRIPTS / "startup.py").read_text(encoding="utf-8")
        self.assertIn("runtime_authority", source)
        self.assertNotIn('values={"{{PYTHON}}":str(sys.executable)', source)
        self.assertNotIn("q=p.with_name(\"pythonw.exe\")", source,
                         "the transient sys.executable sibling fallback must be removed")

    def test_04_missing_runtime_fails_closed(self):
        tmp = Path(os.environ.get("TMP", "/tmp")) / "cnx064-unit-t4"
        env = {"LOCALAPPDATA": str(tmp)}
        self.assertRaises(
            runtime_authority.RuntimeProvisioningError,
            runtime_authority.require_background_interpreter,
            runtime_authority.app_data_root(env),
        )

    def test_05_manifest_outside_boundary_rejected(self):
        app_root = Path("C:/x/Local/CogentNexus-OpenClaw")
        bad = {
            "runtimeRoot": "X:\\somewhere\\else\\python",
            "foregroundInterpreter": "X:\\executor\\venv\\Scripts\\python.exe",
            "backgroundInterpreter": "X:\\executor\\venv\\Scripts\\pythonw.exe",
        }
        self.assertFalse(runtime_authority.validate_runtime(bad, app_root))
        foreign_in_runtime_dir = {
            "runtimeRoot": str(app_root / "runtime" / "python"),
            "foregroundInterpreter": "X:\\executor\\venv\\Scripts\\python.exe",
            "backgroundInterpreter": str(app_root / "runtime" / "python" / "Scripts" / "pythonw.exe"),
        }
        self.assertFalse(runtime_authority.validate_runtime(foreign_in_runtime_dir, app_root))

    @unittest.skipUnless(os.name == "nt", "CREATE_NO_WINDOW is Windows-only")
    def test_06_supervisor_spawn_helpers_use_no_window(self):
        import subprocess

        for module_name in ("host_control", "cnxclaw"):
            module = importlib.import_module(module_name)
            flags = module.creation_flags()
            self.assertEqual(flags & subprocess.CREATE_NO_WINDOW, subprocess.CREATE_NO_WINDOW, module_name)
        runtime_module = importlib.import_module("runtime")
        options = runtime_module.background_options()
        self.assertEqual(options.get("creationflags", 0) & subprocess.CREATE_NO_WINDOW,
                         subprocess.CREATE_NO_WINDOW)

    def test_07_startup_v092_still_targets_host_control_v092(self):
        source = (SCRIPTS / "startup_v092.py").read_text(encoding="utf-8")
        self.assertIn("host_control_v092.py", source)


if __name__ == "__main__":
    unittest.main()
