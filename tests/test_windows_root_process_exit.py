import os
from pathlib import Path
import shutil
import subprocess

import pytest


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts" / "invoke-root-process-exact.ps1"


def test_wrapper_rejects_unobserved_exit_and_caches_handle_before_waiting():
    source = SCRIPT.read_text(encoding="utf-8")
    handle = source.index("$null = $process.Handle")
    wait = source.index("$process.WaitForExit()")
    refresh = source.index("$process.Refresh()")
    convert = source.index("$exitCode = ConvertTo-ObservedExitCode -Value $rawExitCode")
    assert handle < wait < refresh < convert
    assert source.index("if ($null -eq $Value)", source.index("function ConvertTo-ObservedExitCode")) < convert
    assert "-Wait -PassThru" not in source
    assert "observedExitCode = $exitCode" in source
    assert "ConvertTo-WindowsCommandLine" in source
    assert '$startParameters["ArgumentList"] = $commandLine' in source
    assert "[string[]]$ArgumentList" in source
    assert "unobserved null exit-code self-test: PASS" in source
    assert "argument round-trip self-test: PASS" in source


def test_ci_parses_and_runs_the_windows_numeric_exit_self_test():
    workflow = (ROOT / ".github" / "workflows" / "validate.yml").read_text(encoding="utf-8")
    assert "'scripts/invoke-root-process-exact.ps1'" in workflow
    assert "-File .\\scripts\\invoke-root-process-exact.ps1 -SelfTest" in workflow
    assert "skills/cogentnexus-openclaw/scripts/namespace_ownership.py" in workflow
    assert "python -m pytest -q" in workflow
    requirements = (ROOT / "requirements-dev.txt").read_text(encoding="utf-8")
    assert "pytest" in requirements


@pytest.mark.skipif(
    os.name != "nt" or shutil.which("pwsh") is None,
    reason="Windows PowerShell process semantics require a Windows host with pwsh",
)
def test_wrapper_self_test_observes_numeric_zero_and_nonzero_exit_codes():
    completed = subprocess.run(
        ["pwsh", "-NoProfile", "-File", str(SCRIPT), "-SelfTest"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "numeric exit-code self-test: PASS (0,7)" in completed.stdout
    assert "unobserved null exit-code self-test: PASS" in completed.stdout
    assert "argument round-trip self-test: PASS" in completed.stdout
