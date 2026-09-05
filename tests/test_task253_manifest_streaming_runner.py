import json
import os
import shutil
import subprocess
import time
from pathlib import Path

import pytest


PS = shutil.which("powershell.exe")
pytestmark = pytest.mark.skipif(PS is None, reason="Windows PowerShell 5.1 is required")
RUNNER = Path(__file__).parents[1] / "scripts" / "manifest-streaming-runner.ps1"


def _child(tmp: Path, mode: str = "hold") -> Path:
    p = tmp / "synthetic-child.ps1"
    if mode == "hold":
        body = "Write-Output 'STDOUT_MARKER_A'; [Console]::Error.WriteLine('STDERR_MARKER_B'); [Console]::Out.Flush(); [Console]::Error.Flush(); Start-Sleep -Seconds 30"
    else:
        body = "Write-Output 'STDOUT_MARKER_A'; [Console]::Error.WriteLine('STDERR_MARKER_B'); exit 23"
    p.write_text(body, encoding="utf-8")
    return p


def _manifest(tmp: Path, child: Path, bad: bool = False, extra=None) -> Path:
    evidence = tmp / "evidence"
    executable = "C:\\Windows\\System32\\definitely-missing-cnxtest.exe" if bad else PS
    args = ["-NoLogo", "-NoProfile", "-File", str(child)] + (extra or [])
    m = {"childExecutable": executable, "childArguments": args, "workingDirectory": str(tmp), "evidenceRoot": str(evidence)}
    out = tmp / "launch-manifest.json"
    out.write_text(json.dumps(m), encoding="utf-8")
    return out


def _start(tmp: Path, manifest: Path):
    evidence = tmp / "evidence"
    return subprocess.Popen([PS, "-NoLogo", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(RUNNER), "-LaunchManifest", str(manifest), "-EvidenceRoot", str(evidence)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def _wait_markers(evidence: Path, timeout=8):
    end = time.time() + timeout
    while time.time() < end:
        out = (evidence / "child-stdout.txt").read_text(errors="replace") if (evidence / "child-stdout.txt").exists() else ""
        err = (evidence / "child-stderr.txt").read_text(errors="replace") if (evidence / "child-stderr.txt").exists() else ""
        if "STDOUT_MARKER_A" in out and "STDERR_MARKER_B" in err:
            return out, err
        time.sleep(0.1)
    pytest.fail("child markers were not durable before timeout")


def test_live_stdout_stderr_visibility(tmp_path):
    p = _start(tmp_path, _manifest(tmp_path, _child(tmp_path)))
    try:
        out, err = _wait_markers(tmp_path / "evidence")
        assert "STDOUT_MARKER_A" in out
        assert "STDERR_MARKER_B" in err
        assert p.poll() is None
    finally:
        p.kill(); p.wait(timeout=5)


def test_forced_outer_termination_preserves_markers(tmp_path):
    p = _start(tmp_path, _manifest(tmp_path, _child(tmp_path)))
    try:
        _wait_markers(tmp_path / "evidence")
        p.kill(); p.wait(timeout=5)
        assert "STDOUT_MARKER_A" in (tmp_path / "evidence/child-stdout.txt").read_text()
        assert "STDERR_MARKER_B" in (tmp_path / "evidence/child-stderr.txt").read_text()
    finally:
        if p.poll() is None: p.kill(); p.wait(timeout=5)


def test_normal_nonzero_completion(tmp_path):
    p = _start(tmp_path, _manifest(tmp_path, _child(tmp_path, "exit")))
    p.wait(timeout=10)
    result = json.loads((tmp_path / "evidence/runner-result.json").read_text())
    assert result["childExitCode"] == 23
    assert "STDOUT_MARKER_A" in (tmp_path / "evidence/child-stdout.txt").read_text()
    assert "STDERR_MARKER_B" in (tmp_path / "evidence/child-stderr.txt").read_text()


def test_launch_failure_is_distinct(tmp_path):
    p = _start(tmp_path, _manifest(tmp_path, _child(tmp_path), bad=True))
    p.wait(timeout=10)
    result = json.loads((tmp_path / "evidence/runner-result.json").read_text())
    assert result["outcome"] == "child_launch_exception"
    assert result.get("childStarted") is False


def test_manifest_argument_binding(tmp_path):
    marker = tmp_path / "argument marker.txt"
    p = _child(tmp_path, "exit")
    # The synthetic child writes its received arguments to a path containing spaces/quotes.
    p.write_text("param([string]$Path); Set-Content -LiteralPath $Path -Value 'BOUND_OK'; exit 23", encoding="utf-8")
    manifest = _manifest(tmp_path, p, extra=[str(marker)])
    proc = _start(tmp_path, manifest); proc.wait(timeout=10)
    assert marker.read_text() == "BOUND_OK\n"
