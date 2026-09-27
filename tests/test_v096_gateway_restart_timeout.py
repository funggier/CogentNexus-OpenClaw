from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace


def _load_runtime_module():
    runtime_path = (
        Path(__file__).resolve().parents[1]
        / "skills"
        / "cogentnexus-openclaw"
        / "scripts"
        / "runtime.py"
    )
    spec = importlib.util.spec_from_file_location("cnx_runtime_v096_restart_timeout", runtime_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_lifecycle_restart_uses_openclaw_2026_9_6_convergence_budget(monkeypatch, tmp_path):
    runtime = _load_runtime_module()
    observed = {}

    monkeypatch.setattr(
        runtime,
        "load_config",
        lambda root: {"supervisor": {"commandTimeoutSeconds": 30, "ollamaMode": "disabled"}},
    )
    monkeypatch.setattr(runtime, "maintenance_status", lambda root: None)
    monkeypatch.setattr(
        runtime,
        "set_maintenance",
        lambda root, reason, owner, recovery_policy: {
            "active": True,
            "recoveryPolicy": recovery_policy,
        },
    )
    monkeypatch.setattr(runtime, "openclaw_executable", lambda: "openclaw")

    def fake_run_command(argv, timeout=30):
        observed["argv"] = argv
        observed["timeout"] = timeout
        return {
            "ok": True,
            "exitCode": 0,
            "durationMs": 1,
            "stdout": "",
            "stderr": "",
        }

    monkeypatch.setattr(runtime, "run_command", fake_run_command)
    monkeypatch.setattr(runtime, "append_runtime_event", lambda *args, **kwargs: None)
    monkeypatch.setattr(runtime, "emit", lambda value: observed.setdefault("emitted", value))

    args = SimpleNamespace(
        root=tmp_path,
        command_name="restart",
        reason="OpenClaw 2026.9.6 compatibility test",
        owner="test",
    )
    assert runtime.lifecycle_cmd(args) == 0
    assert observed["argv"][-2:] == ["gateway", "restart"]
    assert observed["timeout"] == runtime.LIFECYCLE_RESTART_COMMAND_TIMEOUT_SECONDS
    assert runtime.LIFECYCLE_RESTART_COMMAND_TIMEOUT_SECONDS == 180.0
