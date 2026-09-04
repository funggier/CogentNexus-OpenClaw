"""CNX-20260904-247 — real Windows PowerShell 5.1 native stderr boundary.

This is intentionally a contract test for the installer-relevant capture shape.
It must fail before the owning production capture boundary is repaired.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest


@pytest.mark.skipif(os.name != "nt", reason="requires Windows PowerShell 5.1")
def test_powershell51_native_stderr_capture_preserves_diagnostic_and_exit_code(tmp_path: Path):
    powershell = shutil.which("powershell.exe")
    if not powershell:
        pytest.skip("Windows PowerShell 5.1 is unavailable")
    child = tmp_path / "native_child.py"
    child.write_text(
        "import sys\n"
        "print('TASK247_STDOUT_MARKER', flush=True)\n"
        "print('Traceback (most recent call last):', file=sys.stderr, flush=True)\n"
        "print('TASK247_FRAME_SENTINEL', file=sys.stderr, flush=True)\n"
        "print('RuntimeError: TASK247_FINAL_SENTINEL', file=sys.stderr, flush=True)\n"
        "raise SystemExit(23)\n",
        encoding="utf-8",
    )
    script = tmp_path / "capture.ps1"
    script.write_text(
        "$ErrorActionPreference = 'Stop'\n"
        "$before = $ErrorActionPreference\n"
        f"$captured = (& python.exe -u '{child.as_posix()}' 2>&1 | Out-String)\n"
        "$childExit = $LASTEXITCODE\n"
        "[ordered]@{ captured=$captured; childExit=$childExit; preference=$ErrorActionPreference } | ConvertTo-Json -Compress\n",
        encoding="utf-8-sig",
    )
    result = subprocess.run(
        [powershell, "-NoLogo", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script)],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout.strip())
    assert payload["childExit"] == 23
    assert "Traceback (most recent call last):" in payload["captured"]
    assert "TASK247_FRAME_SENTINEL" in payload["captured"]
    assert "RuntimeError: TASK247_FINAL_SENTINEL" in payload["captured"]
    assert payload["preference"] == "Stop"


@pytest.mark.skipif(os.name != "nt", reason="requires Windows PowerShell 5.1")
def test_powershell51_native_stderr_exit_zero_is_success(tmp_path: Path):
    powershell = shutil.which("powershell.exe")
    if not powershell:
        pytest.skip("Windows PowerShell 5.1 is unavailable")
    child = tmp_path / "native_success.py"
    child.write_text(
        "import sys\n"
        "print('TASK247_CONTROL_STDERR', file=sys.stderr, flush=True)\n",
        encoding="utf-8",
    )
    script = tmp_path / "capture-control.ps1"
    script.write_text(
        "$ErrorActionPreference = 'Stop'\n"
        f"$captured = (& python.exe -u '{child.as_posix()}' 2>&1 | Out-String)\n"
        "$childExit = $LASTEXITCODE\n"
        "[ordered]@{ captured=$captured; childExit=$childExit; preference=$ErrorActionPreference } | ConvertTo-Json -Compress\n",
        encoding="utf-8-sig",
    )
    result = subprocess.run(
        [powershell, "-NoLogo", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script)],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout.strip())
    assert payload["childExit"] == 0
    assert "TASK247_CONTROL_STDERR" in payload["captured"]
    assert payload["preference"] == "Stop"
