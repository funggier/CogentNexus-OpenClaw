from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus-openclaw" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_runtime_restart_reconciles_cli_timeout_when_gateway_becomes_healthy(monkeypatch, tmp_path):
    runtime = _load("cnx_runtime_v099_readiness", "runtime.py")
    calls: list[tuple[list[str], float]] = []
    emitted: list[dict] = []

    config = {"supervisor": {"commandTimeoutSeconds": 30, "verifyDelaySeconds": 0, "ollamaMode": "disabled"}}
    monkeypatch.setattr(runtime, "load_config", lambda _root: config)
    monkeypatch.setattr(runtime, "maintenance_status", lambda _root: None)
    monkeypatch.setattr(
        runtime,
        "set_maintenance",
        lambda _root, reason, owner, recovery_policy: {
            "active": True,
            "reason": reason,
            "owner": owner,
            "recoveryPolicy": recovery_policy,
        },
    )
    monkeypatch.setattr(runtime, "clear_maintenance", lambda _root: True)
    monkeypatch.setattr(runtime, "openclaw_executable", lambda: "openclaw")
    monkeypatch.setattr(runtime, "append_runtime_event", lambda *args, **kwargs: None)
    monkeypatch.setattr(runtime, "emit", emitted.append)
    monkeypatch.setattr(
        runtime,
        "wait_for_runtime_health",
        lambda _config, timeout_seconds, require_ollama: (
            {"gateway": {"healthy": True}, "ollama": {"healthy": True}},
            4,
            True,
        ),
    )

    def fake_run(argv, timeout=30):
        calls.append((list(argv), timeout))
        return {
            "ok": False,
            "exitCode": 1,
            "durationMs": 90000,
            "stdout": "",
            "stderr": "OpenClaw CLI health timeout",
        }

    monkeypatch.setattr(runtime, "run_command", fake_run)
    args = SimpleNamespace(
        root=tmp_path,
        command_name="restart",
        reason="v0.9.9 physical install-over",
        owner="test",
    )

    assert runtime.lifecycle_cmd(args) == 0
    assert [item[0][-2:] for item in calls] == [["gateway", "restart"], ["gateway", "start"]]
    assert all(item[1] == runtime.LIFECYCLE_RESTART_COMMAND_TIMEOUT_SECONDS for item in calls)
    assert emitted[-1]["restartRequested"] is True
    assert emitted[-1]["reconciled"] is True
    assert emitted[-1]["verification"]["healthy"] is True


def test_native_gateway_restore_reconciles_nonzero_commands_when_readiness_is_healthy(monkeypatch):
    host = _load("cnx_host_v091_v099_readiness", "host_v091.py")
    calls: list[tuple[list[str], int]] = []

    def failed_command(argv, timeout=30, **_kwargs):
        calls.append((list(argv), timeout))
        return subprocess.CompletedProcess(argv, 1, "", "OpenClaw CLI readiness timeout")

    monkeypatch.setattr(host.legacy, "openclaw_executable", lambda: "openclaw")
    monkeypatch.setattr(host.legacy, "run", failed_command)
    monkeypatch.setattr(
        host,
        "_wait_native_gateway_ready",
        lambda: {
            "healthy": True,
            "attempts": 7,
            "elapsedSeconds": 112.5,
            "probeTimeoutSeconds": 20,
            "lastStatus": {"healthy": True},
        },
    )

    result = host._restore_native_gateway()

    assert [item[0][-2:] for item in calls] == [["gateway", "restart"], ["gateway", "start"]]
    assert all(item[1] == 180 for item in calls)
    assert result["healthy"] is True
    assert result["reconciledByReadiness"] is True
    assert result["commandExitCode"] == 1


def test_runtime_restart_stays_failed_when_gateway_never_becomes_healthy(monkeypatch, tmp_path):
    runtime = _load("cnx_runtime_v099_failclosed", "runtime.py")
    emitted: list[dict] = []
    config = {"supervisor": {"commandTimeoutSeconds": 30, "verifyDelaySeconds": 0, "ollamaMode": "disabled"}}
    monkeypatch.setattr(runtime, "load_config", lambda _root: config)
    monkeypatch.setattr(runtime, "maintenance_status", lambda _root: {"active": True})
    monkeypatch.setattr(
        runtime,
        "set_maintenance",
        lambda _root, reason, owner, recovery_policy: {
            "active": True,
            "reason": reason,
            "owner": owner,
            "recoveryPolicy": recovery_policy,
        },
    )
    monkeypatch.setattr(runtime, "openclaw_executable", lambda: "openclaw")
    monkeypatch.setattr(runtime, "append_runtime_event", lambda *args, **kwargs: None)
    monkeypatch.setattr(runtime, "emit", emitted.append)
    monkeypatch.setattr(
        runtime,
        "run_command",
        lambda argv, timeout=30: {
            "ok": False,
            "exitCode": 1,
            "durationMs": 90000,
            "stdout": "",
            "stderr": "OpenClaw CLI health timeout",
        },
    )
    monkeypatch.setattr(
        runtime,
        "wait_for_runtime_health",
        lambda _config, timeout_seconds, require_ollama: (
            {"gateway": {"healthy": False}, "ollama": {"healthy": True}},
            10,
            False,
        ),
    )
    args = SimpleNamespace(
        root=tmp_path,
        command_name="restart",
        reason="fail-closed test",
        owner="test",
    )

    assert runtime.lifecycle_cmd(args) == 2
    assert emitted[-1]["restartRequested"] is False
    assert emitted[-1]["reconciled"] is False
    assert emitted[-1]["verification"]["healthy"] is False


def test_native_gateway_restore_stays_failed_when_readiness_never_recovers(monkeypatch):
    host = _load("cnx_host_v091_v099_failclosed", "host_v091.py")

    monkeypatch.setattr(host.legacy, "openclaw_executable", lambda: "openclaw")
    monkeypatch.setattr(
        host.legacy,
        "run",
        lambda argv, timeout=30, **_kwargs: subprocess.CompletedProcess(
            argv, 1, "", "OpenClaw CLI readiness timeout"
        ),
    )
    monkeypatch.setattr(
        host,
        "_wait_native_gateway_ready",
        lambda: {
            "healthy": False,
            "attempts": 10,
            "elapsedSeconds": 180.0,
            "probeTimeoutSeconds": 20,
            "lastStatus": {"healthy": False},
        },
    )

    try:
        host._restore_native_gateway()
    except RuntimeError as error:
        assert "failed health verification" in str(error)
    else:
        raise AssertionError("unhealthy native Gateway restore must fail closed")


def test_runtime_restart_rejects_unrelated_command_failure_even_if_gateway_is_healthy(monkeypatch, tmp_path):
    runtime = _load("cnx_runtime_v099_unrelated_failure", "runtime.py")
    emitted: list[dict] = []
    config = {"supervisor": {"commandTimeoutSeconds": 30, "verifyDelaySeconds": 0, "ollamaMode": "disabled"}}
    monkeypatch.setattr(runtime, "load_config", lambda _root: config)
    monkeypatch.setattr(runtime, "maintenance_status", lambda _root: {"active": True})
    monkeypatch.setattr(
        runtime,
        "set_maintenance",
        lambda _root, reason, owner, recovery_policy: {
            "active": True,
            "reason": reason,
            "owner": owner,
            "recoveryPolicy": recovery_policy,
        },
    )
    monkeypatch.setattr(runtime, "openclaw_executable", lambda: "openclaw")
    monkeypatch.setattr(runtime, "append_runtime_event", lambda *args, **kwargs: None)
    monkeypatch.setattr(runtime, "emit", emitted.append)
    monkeypatch.setattr(
        runtime,
        "run_command",
        lambda argv, timeout=30: {
            "ok": False,
            "exitCode": 1,
            "durationMs": 10,
            "stdout": "",
            "stderr": "permission denied",
        },
    )
    monkeypatch.setattr(
        runtime,
        "wait_for_runtime_health",
        lambda _config, timeout_seconds, require_ollama: (
            {"gateway": {"healthy": True}, "ollama": {"healthy": True}},
            1,
            True,
        ),
    )
    args = SimpleNamespace(
        root=tmp_path,
        command_name="restart",
        reason="unrelated failure",
        owner="test",
    )

    assert runtime.lifecycle_cmd(args) == 2
    assert emitted[-1]["restartRequested"] is False
    assert emitted[-1]["verification"]["healthy"] is True
    assert emitted[-1]["verification"]["commandAuthorized"] is False


def test_native_gateway_restore_rejects_unrelated_command_failure_even_if_healthy(monkeypatch):
    host = _load("cnx_host_v091_v099_unrelated_failure", "host_v091.py")

    monkeypatch.setattr(host.legacy, "openclaw_executable", lambda: "openclaw")
    monkeypatch.setattr(
        host.legacy,
        "run",
        lambda argv, timeout=30, **_kwargs: subprocess.CompletedProcess(
            argv, 1, "", "permission denied"
        ),
    )
    monkeypatch.setattr(
        host,
        "_wait_native_gateway_ready",
        lambda: {
            "healthy": True,
            "attempts": 1,
            "elapsedSeconds": 0.0,
            "probeTimeoutSeconds": 20,
            "lastStatus": {"healthy": True},
        },
    )

    try:
        host._restore_native_gateway()
    except RuntimeError as error:
        assert "commandAuthorized=False" in str(error)
    else:
        raise AssertionError("unrelated native Gateway command failure must fail closed")
