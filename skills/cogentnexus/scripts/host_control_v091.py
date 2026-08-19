#!/usr/bin/env python3
"""CogentNexus v0.9.1 Host control shim with symmetric enable rollback.

Periodic supervisor ticks deliberately bypass the legacy watchdog re-apply path:
the watchdog fence is installed on enable/start/restart and does not need an
OpenClaw CLI process every minute merely to confirm an unchanged value.

The delegated Host entry layers Direct model-call stall recovery on top of the
single-authority activation overlay. MANAGED remains the sole inference/recovery
authority, while steady-state supervision can quiesce and classify an expired
provider call even when Gateway/Ollama health endpoints still respond.

MANAGED activation is also a durable invariant: if OpenClaw's plugin config
later drifts to disabled while Host authority still requests a running managed
Gateway, the scheduled --execute-safe tick repairs that drift and verifies the
plugin after a Gateway process boundary. Healthy steady state remains file-only.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import host_control as legacy

HERE = Path(__file__).resolve()
legacy.HOST = HERE.with_name("host_stall_v091.py")
PLUGIN_ID = "cogentnexus-rotation"


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except Exception:
        return {}


def _controller(root: Path) -> dict[str, Any]:
    return _read_json(root / "host" / "controller.json")


def _openclaw_config_path() -> Path:
    configured = os.environ.get("OPENCLAW_CONFIG_PATH")
    return Path(configured).expanduser() if configured else Path.home() / ".openclaw" / "openclaw.json"


def _managed_plugin_config_enabled(root: Path) -> bool | None:
    state = _controller(root)
    if state.get("mode") != "managed" or state.get("desiredGateway") != "running":
        return None
    config = _read_json(_openclaw_config_path())
    plugins = config.get("plugins") if isinstance(config.get("plugins"), dict) else {}
    entries = plugins.get("entries") if isinstance(plugins.get("entries"), dict) else {}
    entry = entries.get(PLUGIN_ID) if isinstance(entries.get(PLUGIN_ID), dict) else {}
    return entry.get("enabled") is True


def _inspect_plugin_runtime() -> dict[str, Any]:
    result = legacy.run(
        [legacy.openclaw_executable(), "plugins", "inspect", PLUGIN_ID, "--runtime", "--json"],
        timeout=60,
        check=True,
    )
    raw = legacy.captured_text(result.stdout).strip()
    if not raw:
        raise RuntimeError("OpenClaw plugin runtime inspection returned no JSON")
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"OpenClaw plugin runtime inspection returned invalid JSON: {raw[:500]}") from error
    if not isinstance(value, dict):
        raise RuntimeError("OpenClaw plugin runtime inspection returned a non-object payload")
    return value


def _repair_managed_plugin_activation(root: Path, execute_safe: bool) -> dict[str, Any] | None:
    enabled = _managed_plugin_config_enabled(root)
    if enabled is None or enabled is True:
        return None
    if not execute_safe:
        return {"detected": True, "repaired": False, "reason": "execute-safe-required"}

    exe = legacy.openclaw_executable()
    legacy.run([exe, "plugins", "enable", PLUGIN_ID], timeout=60, check=True)
    legacy.run([exe, "config", "validate"], timeout=60, check=True)

    restart = legacy.run([exe, "gateway", "restart"], timeout=180)
    if restart.returncode != 0:
        restart = legacy.run([exe, "gateway", "start"], timeout=180, check=True)
    if restart.returncode != 0:
        detail = legacy.captured_text(restart.stderr) or legacy.captured_text(restart.stdout) or "Gateway restart failed"
        raise RuntimeError(detail.strip())

    if _managed_plugin_config_enabled(root) is not True:
        raise RuntimeError("OpenClaw plugin config remained disabled after MANAGED activation repair")

    inspected = _inspect_plugin_runtime()
    plugin = inspected.get("plugin") if isinstance(inspected.get("plugin"), dict) else {}
    if plugin.get("enabled") is not True or plugin.get("activated") is not True or plugin.get("status") != "loaded":
        raise RuntimeError(
            "CogentNexus plugin failed runtime activation verification after MANAGED repair: "
            f"enabled={plugin.get('enabled')} activated={plugin.get('activated')} status={plugin.get('status')}"
        )

    payload = {
        "detected": True,
        "repaired": True,
        "mode": _controller(root).get("mode"),
        "pluginEnabled": True,
        "pluginActivated": True,
        "pluginStatus": plugin.get("status"),
    }
    legacy.append_audit(root, "managed-plugin-activation-repaired", payload)
    return payload


def main() -> int:
    argv = legacy.sys.argv[1:]
    root = legacy.root_from_argv(argv)
    command, action = legacy.command_from_argv(argv)

    # Before first initialization there is no authority to assume MANAGED. Route
    # non-enable commands directly to the hardened Host, which seeds PASSTHROUGH.
    if command != "enable" and not (root / "host" / "controller.json").exists():
        return legacy.delegate(argv)

    # The scheduled supervisor must remain file/socket-only while healthy.
    # Calling legacy.main() here would run apply_watchdog_compat(), which invokes
    # `openclaw config get` and spins up Node once per schedule even when idle.
    # A direct openclaw.json read is cheap; Node is invoked only when MANAGED
    # activation drift is actually detected.
    if command == "supervisor" and action == "tick":
        try:
            _repair_managed_plugin_activation(root, "--execute-safe" in argv)
        except Exception as error:
            legacy.append_audit(root, "managed-plugin-activation-repair-failed", {"error": str(error)})
            print(json.dumps({
                "result": "error",
                "error": f"CogentNexus MANAGED plugin activation repair failed: {error}",
            }, ensure_ascii=False, indent=2))
            return 1
        return legacy.delegate(argv)

    if command != "enable":
        return legacy.main()

    try:
        legacy.apply_watchdog_compat(root)
    except Exception as error:
        print(json.dumps({
            "result": "error",
            "error": f"CogentNexus watchdog compatibility failed before enable: {error}",
        }, ensure_ascii=False, indent=2))
        return 1

    code = legacy.delegate(argv)
    if code == 0:
        return 0

    rollback_error = None
    try:
        legacy.restore_watchdog_compat(root)
    except Exception as error:
        rollback_error = str(error)

    legacy.append_audit(root, "watchdog-compat-enable-rollback", {
        "delegateExitCode": code,
        "rollbackError": rollback_error,
    })
    if rollback_error:
        print(json.dumps({
            "result": "error",
            "error": "CogentNexus enable failed and watchdog compatibility rollback also failed",
            "delegateExitCode": code,
            "rollbackError": rollback_error,
        }, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
