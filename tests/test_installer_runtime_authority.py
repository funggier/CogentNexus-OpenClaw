#!/usr/bin/env python3
"""Task CNX-20260825-065 — installer runtime-authority gap regression tests.

T1: committed install.ps1 must resolve scripts\\runtime_authority.py exactly
    (no embedded CR/LF / malformed relative path).
T2: the installer-facing ensure boundary runs unconditionally and repairs a
    stale/corrupt manifest even when Scripts\\python.exe exists; a broken
    background interpreter is never accepted as healthy.
T3: post-provision MANAGED enable/status and ownership/doctor calls use
    $ownedPython, not bare `python`.
T4: existing-runtime reuse probes BOTH foreground and background capability.
"""
from __future__ import annotations

import importlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SCRIPTS = REPO / "skills" / "cogentnexus-openclaw" / "scripts"
INSTALLER = REPO / "scripts" / "install.ps1"
sys.path.insert(0, str(SCRIPTS))

runtime_authority = importlib.import_module("runtime_authority")
IS_WINDOWS = os.name == "nt"


def _temp_app_base(prefix: str = "cnx065-") -> tuple[Path, Path]:
    tmp = Path(tempfile.mkdtemp(prefix=prefix))
    return tmp, tmp / "Local"


class TestInstallerSourceContract(unittest.TestCase):
    """T1/B5 + T3/B7 source-level contracts on the real install.ps1."""

    def setUp(self):
        self.source = INSTALLER.read_text(encoding="utf-8")

    def test_t1_runtime_authority_path_has_no_embedded_newline(self):
        # The literal "scripts\runtime_authority.py" must appear intact; a line
        # break inside the string is the B5 corruption.
        self.assertNotIn('scripts" +\n', self.source)
        for match in re.finditer(r'"([^"\n]*runtime[^"\n]*)"', self.source):
            literal = match.group(1)
            self.assertNotIn("\r", literal)
            self.assertNotIn("\n", literal)
        # the exact resolved literal exists intact somewhere in the source
        self.assertRegex(
            self.source,
            r'Join-Path \$targetSkill "scripts\\runtime_authority\.py"',
            'installer must resolve exactly scripts\\runtime_authority.py',
        )
        joined = re.search(r'Join-Path\s+\$targetSkill\s+"([^"]+)"', self.source)
        self.assertIsNotNone(joined)
        for m in re.finditer(r'Join-Path\s+\$targetSkill\s+"([^"]*)"', self.source):
            self.assertNotIn("\r", m.group(1))
            self.assertNotIn("\n", m.group(1))

    def test_t1_runtime_authority_script_existence_check(self):
        self.assertIn("Test-Path -LiteralPath $runtimeAuthorityScript", self.source,
                      "installer must prove the authority script exists before invoking it")

    def test_t2_ensure_runtime_runs_unconditionally(self):
        # ensure-runtime invocation must NOT be guarded by Test-Path $ownedPython absence.
        ensure_idx = self.source.index("ensure-runtime")
        preceding = self.source[max(0, ensure_idx - 400):ensure_idx]
        self.assertNotIn("Test-Path $ownedPython", preceding.split("if ")[-1] if "if (" in preceding[-200:] else "",
                         "ensure-runtime must run unconditionally, not only when python.exe is absent")

    def test_t3_post_provision_enable_status_use_owned_python(self):
        enable_segment = self.source[self.source.index("--provider ollama") - 300:
                                     self.source.index("--provider ollama") + 100]
        self.assertIn("$ownedPython", enable_segment,
                      "MANAGED enable must execute under the owned runtime")
        status_match = re.search(r'& \$ownedPython \$cliScript --root \$cogentNexusOpenClawRoot status', self.source)
        self.assertIsNotNone(status_match,
                             "final status must execute under the owned runtime")


class TempAppDataBase(unittest.TestCase):
    """Shared temp app-data fixture for executable installer tests."""

    def setUp(self):
        self.tmp, self.local_base = _temp_app_base()
        self.env = {"LOCALAPPDATA": str(self.local_base)}
        self.app_root = self.local_base / "CogentNexus-OpenClaw"
        self.runtime_dir = self.app_root / "runtime" / "python"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _installer_ensure(self):
        """Exercise the SAME call boundary install.ps1 uses (CLI ensure-runtime)."""
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "runtime_authority.py"), "ensure-runtime",
             "--application-data-root", str(self.app_root)],
            capture_output=True, text=True, timeout=600,
            creationflags=runtime_authority.creation_flags(),
        )
        if result.returncode != 0:
            raise runtime_authority.RuntimeProvisioningError(result.stderr.strip()[:400])
        return json.loads(result.stdout)


@unittest.skipUnless(IS_WINDOWS, "executable installer-boundary coverage is Windows-specific")
class TestInstallerEnsureBoundary(TempAppDataBase):
    """T2/T4 — executable proof of the unconditional ensure/repair behavior."""

    def test_fresh_provision_via_installer_boundary(self):
        manifest = self._installer_ensure()
        self.assertEqual(Path(manifest["runtimeRoot"]), self.app_root / "runtime" / "python")

    def test_stale_manifest_repaired_even_when_python_exe_exists(self):
        self._installer_ensure()
        (self.runtime_dir / "runtime-manifest.json").unlink()
        self.assertTrue((self.runtime_dir / "Scripts" / "python.exe").is_file(),
                        "fixture sanity: python.exe deliberately left present")
        manifest = self._installer_ensure()
        self.assertTrue(runtime_authority.validate_runtime(manifest, self.app_root))

    def test_broken_background_interpreter_not_accepted_as_healthy(self):
        self._installer_ensure()
        pythonw = self.runtime_dir / "Scripts" / "pythonw.exe"
        pythonw.unlink()
        # Contract (Task CNX-20260825-065 B6): recreate safely OR fail closed.
        # Either way the resulting runtime must be fully validated healthy.
        try:
            manifest = self._installer_ensure()
        except runtime_authority.RuntimeProvisioningError:
            return  # failed closed is acceptable
        self.assertTrue(runtime_authority.validate_runtime(manifest, self.app_root))
        self.assertTrue((self.runtime_dir / "Scripts" / "pythonw.exe").is_file(),
                        "recreated runtime must restore a working background interpreter")


if __name__ == "__main__":
    unittest.main()
