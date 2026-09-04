"""CNX-20260904-247 — real Windows PowerShell 5.1 native stderr boundary."""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).parents[1]
INSTALL_PS1 = (REPO / "scripts" / "install.ps1").read_text(encoding="utf-8")


def _helper_source() -> str:
    match = re.search(
        r"function Invoke-NativeInstallerDiagnostic\s*\{.*?(?=\nfunction Get-BoundedInstallerDiagnostic)",
        INSTALL_PS1,
        flags=re.DOTALL,
    )
    assert match, "production native diagnostic helper is missing"
    return match.group(0)


def _run_capture(tmp_path: Path, child: Path) -> tuple[subprocess.CompletedProcess[str], dict]:
    powershell = shutil.which("powershell.exe")
    if not powershell:
        pytest.skip("Windows PowerShell 5.1 is unavailable")
    script = tmp_path / "capture.ps1"
    script.write_text(
        "$ErrorActionPreference = 'Stop'\n"
        + _helper_source()
        + "\n$before = $ErrorActionPreference\n"
        + f"$capture = Invoke-NativeInstallerDiagnostic -Executable 'python.exe' -Arguments @('-u', '{child.as_posix()}')\n"
        + "[ordered]@{ output=$capture.Output; exitCode=$capture.ExitCode; preference=$ErrorActionPreference.ToString(); before=$before.ToString() } | ConvertTo-Json -Compress\n",
        encoding="utf-8-sig",
    )
    result = subprocess.run(
        [powershell, "-NoLogo", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script)],
        capture_output=True,
        text=True,
        timeout=120,
    )
    payload = json.loads(result.stdout.strip()) if result.stdout.strip() else {}
    return result, payload


@pytest.mark.skipif(os.name != "nt", reason="requires Windows PowerShell 5.1")
def test_powershell51_native_stderr_capture_preserves_diagnostic_and_exit_code(tmp_path: Path):
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
    result, payload = _run_capture(tmp_path, child)
    assert result.returncode == 0, result.stdout + result.stderr
    assert payload["exitCode"] == 23
    assert "Traceback (most recent call last):" in payload["output"]
    assert "TASK247_FRAME_SENTINEL" in payload["output"]
    assert "RuntimeError: TASK247_FINAL_SENTINEL" in payload["output"]
    assert payload["preference"] == payload["before"] == "Stop"


@pytest.mark.skipif(os.name != "nt", reason="requires Windows PowerShell 5.1")
def test_powershell51_native_stderr_exit_zero_is_success(tmp_path: Path):
    child = tmp_path / "native_success.py"
    child.write_text(
        "import sys\n"
        "print('TASK247_CONTROL_STDERR', file=sys.stderr, flush=True)\n",
        encoding="utf-8",
    )
    result, payload = _run_capture(tmp_path, child)
    assert result.returncode == 0, result.stdout + result.stderr
    assert payload["exitCode"] == 0
    assert "TASK247_CONTROL_STDERR" in payload["output"]
    assert payload["preference"] == payload["before"] == "Stop"
