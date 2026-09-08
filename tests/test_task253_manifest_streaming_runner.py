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
        body = "param([string]$PidPath,[string]$ArgsPath); Set-Content -LiteralPath $PidPath -Value $PID; Set-Content -LiteralPath $ArgsPath -Value (@($args) | ConvertTo-Json -Compress); Write-Output 'STDOUT_MARKER_A'; [Console]::Error.WriteLine('STDERR_MARKER_B'); [Console]::Out.Flush(); [Console]::Error.Flush(); Start-Sleep -Seconds 30"
    else:
        body = "param([string]$PidPath,[string]$ArgsPath); Set-Content -LiteralPath $PidPath -Value $PID; Set-Content -LiteralPath $ArgsPath -Value (@($args) | ConvertTo-Json -Compress); Write-Output 'STDOUT_MARKER_A'; [Console]::Error.WriteLine('STDERR_MARKER_B'); exit 23"
    p.write_text(body, encoding="utf-8")
    return p


def _manifest(tmp: Path, child: Path, bad: bool = False, extra=None) -> Path:
    evidence = tmp / "evidence"
    executable = "C:\\Windows\\System32\\definitely-missing-cnxtest.exe" if bad else PS
    pid_path = tmp / "target-pid.json"
    args_path = tmp / "received-args.json"
    args = ["-NoLogo", "-NoProfile", "-File", str(child), str(pid_path), str(args_path)] + (extra or [])
    m = {"childExecutable": executable, "childArguments": args, "workingDirectory": str(tmp), "evidenceRoot": str(evidence)}
    out = tmp / "launch-manifest.json"
    out.write_text(json.dumps(m), encoding="utf-8")
    return out


def _start(tmp: Path, manifest: Path):
    evidence = tmp / "evidence"
    return subprocess.Popen([PS, "-NoLogo", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(RUNNER), "-LaunchManifest", str(manifest), "-EvidenceRoot", str(evidence)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def _wait_file(path: Path, timeout=8):
    end = time.time() + timeout
    while time.time() < end:
        if path.exists() and path.read_text(errors="replace").strip():
            return path.read_text(errors="replace").strip()
        time.sleep(0.1)
    pytest.fail(f"missing durable file: {path}")


def _wait_markers(evidence: Path, timeout=8):
    end = time.time() + timeout
    while time.time() < end:
        out = (evidence / "child-stdout.txt").read_text(errors="replace") if (evidence / "child-stdout.txt").exists() else ""
        err = (evidence / "child-stderr.txt").read_text(errors="replace") if (evidence / "child-stderr.txt").exists() else ""
        if "STDOUT_MARKER_A" in out and "STDERR_MARKER_B" in err:
            return out, err
        time.sleep(0.1)
    pytest.fail("child markers were not durable before timeout")


def _cleanup_pid(path: Path):
    if not path.exists():
        return
    pid = int(path.read_text().strip())
    subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True, text=True)


def test_live_stdout_stderr_visibility_and_actual_target_identity(tmp_path):
    p = _start(tmp_path, _manifest(tmp_path, _child(tmp_path)))
    try:
        out, err = _wait_markers(tmp_path / "evidence")
        target_pid = int(_wait_file(tmp_path / "target-pid.json"))
        started = json.loads(_wait_file(tmp_path / "evidence/child-started.json"))
        assert started["pid"] == target_pid
        assert started["executable"].lower() == PS.lower()
        assert started.get("launcherPid") != started["pid"]
        assert "STDOUT_MARKER_A" in out and "STDERR_MARKER_B" in err
        assert p.poll() is None
    finally:
        _cleanup_pid(tmp_path / "target-pid.json")
        if p.poll() is None:
            p.kill()
        p.wait(timeout=5)


def test_forced_outer_termination_preserves_markers_and_target_artifact(tmp_path):
    p = _start(tmp_path, _manifest(tmp_path, _child(tmp_path)))
    try:
        _wait_markers(tmp_path / "evidence")
        _wait_file(tmp_path / "target-pid.json")
        _wait_file(tmp_path / "evidence/child-started.json")
        p.kill(); p.wait(timeout=5)
        assert "STDOUT_MARKER_A" in (tmp_path / "evidence/child-stdout.txt").read_text()
        assert "STDERR_MARKER_B" in (tmp_path / "evidence/child-stderr.txt").read_text()
        assert (tmp_path / "evidence/child-started.json").exists()
    finally:
        _cleanup_pid(tmp_path / "target-pid.json")
        if p.poll() is None: p.kill(); p.wait(timeout=5)


def test_normal_nonzero_completion(tmp_path):
    p = _start(tmp_path, _manifest(tmp_path, _child(tmp_path, "exit")))
    p.wait(timeout=10)
    result = json.loads((tmp_path / "evidence/runner-result.json").read_text())
    assert result["childExitCode"] == 23
    assert result["childStarted"] is True
    assert "STDOUT_MARKER_A" in (tmp_path / "evidence/child-stdout.txt").read_text()
    assert "STDERR_MARKER_B" in (tmp_path / "evidence/child-stderr.txt").read_text()


def test_launch_failure_leaves_no_target_child_start_artifact(tmp_path):
    p = _start(tmp_path, _manifest(tmp_path, _child(tmp_path), bad=True))
    p.wait(timeout=10)
    result = json.loads((tmp_path / "evidence/runner-result.json").read_text())
    assert result["outcome"] == "child_launch_exception"
    assert result.get("childStarted") is False
    assert not (tmp_path / "evidence/child-started.json").exists()


def test_manifest_argument_binding_with_quote_edge(tmp_path):
    marker = tmp_path / "argument marker 'quoted'.txt"
    p = _child(tmp_path, "exit")
    p.write_text("param([string]$PidPath,[string]$ArgsPath); Set-Content -LiteralPath $PidPath -Value $PID; Set-Content -LiteralPath $ArgsPath -Value (@($args) | ConvertTo-Json -Compress); Set-Content -LiteralPath $args[0] -Value 'BOUND_OK'; exit 23", encoding="utf-8")
    proc = _start(tmp_path, _manifest(tmp_path, p, extra=[str(marker), 'literal"quote']))
    proc.wait(timeout=10)
    assert marker.read_text() == "BOUND_OK\n"
    received = json.loads((tmp_path / "received-args.json").read_text())
    assert received == [str(marker), 'literal"quote']
    _cleanup_pid(tmp_path / "target-pid.json")
