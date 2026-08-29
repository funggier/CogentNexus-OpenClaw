from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "scripts" / "test-v093-ollama-recovery-windows-v3.ps1"


@pytest.mark.skipif(shutil.which("powershell.exe") is None, reason="Windows PowerShell 5.1 is required")
def test_harness_owned_convergence_contract_self_test_passes():
    result = subprocess.run(
        [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(HARNESS),
            "-ContractSelfTest",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "convergence contract self-test: PASS" in result.stdout
