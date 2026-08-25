#!/usr/bin/env python3
"""Task CNX-20260825-063 regression tests: owned runtime authority.

Covers:
- Test 1: installer/startup invoked from an executor venv must not persist the
  venv path as durable runtime (RED against current behavior).
- Test 2: generated launcher must use exact owned foreground interpreter,
  never bare ``python``.
- Test 3: startup task substitution must select product-owned background
  interpreter, never registration-time venv pythonw.
- Test 4: missing/corrupt owned runtime fails closed.
- Test 5: manifest validation rejects paths outside the ownership boundary.
- Test 6: supervisor-path spawn helpers apply CREATE_NO_WINDOW on Windows.
- Test 7: startup_v092 still resolves host_control_v092.py.
"""
from __future__ import annotations

import importlib
import json
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent / "skills" / "cogentnexus-openclaw" / "scripts"
sys.path.insert(0, str(SCRIPTS))

runtime_authority = importlib.import_module("runtime_authority")


def _fake_env(tmp: Path) -> dict[str, str]:
    return {"LOCALAPPDATA": str(tmp / "AppData" / "Local"), "SystemRoot": os.environ.get("SystemRoot", "C:\\Windows")}


class RuntimeAuthorityTests(unittest.TestCase):
    def test_01_executor_venv_is_never_durable_authority(self):
        """A bootstrap interpreter inside an executor venv must resolve to its base, not the venv."""
        calls = iter([
            json.dumps({"is_venv": True}),
            json.dumps(str(Path("X:/realbase/python.exe").resolve())),
            json.dumps({"is_venv": False}),
        ])

        def fake_run(cmd, **kwargs):
            class R:
                returncode = 0
                stdout = next(calls)
                stderr = ""
            return R()

        with mock.patch.object(runtime_authority.subprocess, "run", side_effect=fake_run):
            resolved = runtime_authority.resolve_base_interpreter(Path("X:/executor/venv/Scripts/python.exe"))
        self.assertNotIn("executor", str(resolved).lower())
        self.assertNotIn("venv", str(resolved).lower())

    def test_02_launcher_generation_uses_owned_interpreter(self):
        """install.ps1 launcher text must reference the owned interpreter variable, not bare python."""
        text = (HERE.parent / "scripts" / "install.ps1").read_text(encoding="utf-8")
        # The generated cnxclaw.cmd line must not invoke bare `python`.
        marker = "$launcherText ="
        start = text.index(marker)
        segment = text[start:text.index("`r`n`r`n", start) if "`r`n`r`n" in text[start:] else len(text)]
        first_line = text[text.index(marker):].splitlines()[0]
        self.assertIn("$ownedPython", first_line, "launcher generation must interpolate the owned foreground interpreter")

    def test_03_startup_task_uses_owned_background_interpreter(self):
        """startup.py must source {{PYTHON}} from the owned runtime authority."""
        source = (SCRIPTS / "startup.py").read_text(encoding="utf-8")
        self.assertIn("runtime_authority", source, "startup.py must delegate {{PYTHON}} to the owned runtime")
        self.assertNotIn('values={"{{PYTHON}}":str(sys.executable)', source)

    def test_04_missing_runtime_fails_closed(self):
        env = _fake_env(Path(os.environ.get("TMP", "/tmp")) / "cnx063-t4")
        with self.assertRaises(runtime_authority.RuntimeProvisioningError):
            runtime_authority.require_background_interpreter(env)

    def test_05_manifest_outside_boundary_rejected(self):
        env = _fake_env(Path(os.environ.get("TMP", "/tmp")) / "cnx063-t5")
        bad = {
            "runtimeRoot": "X:\\somewhere\\else\\python",
            "foregroundInterpreter": "X:\\executor\\venv\\Scripts\\python.exe",
            "backgroundInterpreter": "X:\\executor\\venv\\Scripts\\pythonw.exe",
        }
        self.assertFalse(runtime_authority.validate_runtime(bad, env))
        foreign = {
            "runtimeRoot": str(runtime_authority.runtime_root(env)),
            "foregroundInterpreter": "X:\\executor\\venv\\Scripts\\python.exe",
            "backgroundInterpreter": "X:\\executor\\venv\\Scripts\\pythonw.exe",
        }
        self.assertFalse(runtime_authority.validate_runtime(foreign, env))

    @unittest.skipUnless(os.name == "nt", "CREATE_NO_WINDOW is Windows-only")
    def test_06_supervisor_spawn_helpers_use_no_window(self):
        import subprocess

        for module_name in ("host_control", "cnxclaw", "runtime"):
            module = importlib.import_module(module_name)
            helper = getattr(module, "creation_flags", None) or (
                getattr(module, "background_options", None) and (lambda m=module: m.background_options().get("creationflags"))
            )
            self.assertIsNotNone(helper, f"{module_name} must expose a spawn-flags helper")
            flags = helper() if callable(helper) else helper
            self.assertEqual(flags & subprocess.CREATE_NO_WINDOW, subprocess.CREATE_NO_WINDOW)

    def test_07_startup_v092_still_targets_host_control_v092(self):
        source = (SCRIPTS / "startup_v092.py").read_text(encoding="utf-8")
        self.assertIn("host_control_v092.py", source)


if __name__ == "__main__":
    unittest.main()
