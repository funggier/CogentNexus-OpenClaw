#!/usr/bin/env python3
"""CogentNexus-OpenClaw v0.9.5 operator CLI boundary.

Ownership rules:
- CNX lifecycle commands own CNX/Gateway lifecycle only.
- `local <adapter> ...` owns local adapter process lifecycle only.
- OpenClaw owns provider/model/auth/routing.
- Provider metadata exposed by status/check is diagnostic, never lifecycle authority.

The legacy provider-transition functions below are compatibility APIs for older
callers/tests. The CLI never invokes them and rejects `--provider` on CNX
lifecycle commands, so they cannot act as a second provider-routing authority.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import checks_v092 as checks
import local_adapter
import openclaw_route_v092 as openclaw_route
import provider
import provider_recovery_v092 as recovery_policy

HERE = Path(__file__).resolve()
SKILL = HERE.parents[1]
WORKSPACE = SKILL.parents[1]
DEFAULT_ROOT = WORKSPACE / ".cogentnexus-openclaw"
HOST_CONTROL = HERE.with_name("host_control_v092.py")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def creation_flags() -> int:
    return getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0


def state_path(root: Path) -> Path:
    return root / "host" / "controller.json"


def load_state(root: Path) -> dict[str, Any]:
    try:
        value = json.loads(state_path(root).read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except FileNotFoundError:
        return {}


def save_state(root: Path, state: dict[str, Any]) -> dict[str, Any]:
    path = state_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    value = dict(state)
    value.setdefault("schemaVersion", 1)
    value["updatedAt"] = now_iso()
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)
    return value


def patch_state(root: Path, **changes: Any) -> dict[str, Any]:
    state = load_state(root)
    state.update(changes)
    state["generation"] = int(state.get("generation", 0)) + 1
    return save_state(root, state)


def parse_globals(argv: list[str]) -> tuple[Path, list[str], bool]:
    root = DEFAULT_ROOT
    json_mode = False
    cleaned: list[str] = []
    index = 0
    while index < len(argv):
        value = argv[index]
        if value == "--root" and index + 1 < len(argv):
            root = Path(argv[index + 1]).expanduser().resolve()
            index += 2
            continue
        if value == "--json":
            json_mode = True
            index += 1
            continue
        cleaned.append(value)
        index += 1
    return root.resolve(), cleaned, json_mode


def option_value(args: list[str], name: str) -> str | None:
    for index, value in enumerate(args):
        if value == name and index + 1 < len(args):
            return args[index + 1]
        if value.startswith(name + "="):
            return value[len(name) + 1 :]
    return None


def has_option(args: list[str], name: str) -> bool:
    return option_value(args, name) is not None or name in args


def run_host(root: Path, args: list[str], timeout: int = 420, target: str | None = None) -> dict[str, Any]:
    env = os.environ.copy()
    if target:
        env["CNXCLAW_PROVIDER_TARGET"] = target
    proc = subprocess.run(
        [sys.executable, str(HOST_CONTROL), "--root", str(root), *args],
        capture_output=True,
        text=True,
        timeout=timeout,
        creationflags=creation_flags(),
        env=env,
    )
    raw = proc.stdout.strip()
    parsed: Any = None
    if raw:
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = raw
    return {"ok": proc.returncode == 0, "exitCode": proc.returncode, "output": parsed, "stdout": raw, "stderr": proc.stderr.strip()}


def delegate(root: Path, args: list[str], interactive: bool = False) -> int:
    command = [sys.executable, str(HOST_CONTROL), "--root", str(root), *args]
    if interactive:
        return int(subprocess.run(command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, creationflags=creation_flags()).returncode)
    proc = subprocess.run(command, capture_output=True, text=True, creationflags=creation_flags())
    if proc.stdout:
        sys.stdout.write(proc.stdout)
    if proc.stderr:
        sys.stderr.write(proc.stderr)
    return int(proc.returncode)


# ---------------------------------------------------------------------------
# Legacy compatibility API. Not reachable from the v0.9.5 CLI lifecycle.
# ---------------------------------------------------------------------------

def resolve_target(root: Path, explicit: str | None) -> tuple[str, str]:
    if explicit:
        return provider.normalize_provider(explicit), "explicit"
    state = load_state(root)
    transition = state.get("providerTransition")
    if isinstance(transition, dict) and transition.get("to"):
        return provider.normalize_provider(str(transition["to"])), "resume-transition"
    selected = state.get("selectedProvider")
    if selected:
        return provider.normalize_provider(str(selected)), "persisted"
    installed = provider.installed_providers()
    if len(installed) == 1:
        return installed[0], "single-installed"
    if not installed:
        raise RuntimeError("no supported local provider is installed; use the explicit local adapter command instead")
    raise RuntimeError("multiple providers are installed but no legacy target is selected")


def commit_provider(root: Path, target: str, source: str) -> dict[str, Any]:
    state = load_state(root)
    state.update({
        "selectedProvider": target,
        "providerTransition": None,
        "desiredProvider": "running",
        "providerSelection": {"selectedAt": now_iso(), "selectionSource": source, "lastVerifiedAt": now_iso()},
    })
    state["generation"] = int(state.get("generation", 0)) + 1
    return save_state(root, state)


def begin_transition(root: Path, target: str, source: str) -> dict[str, Any]:
    state = load_state(root)
    previous = state.get("selectedProvider")
    transition = {"from": previous, "to": target, "source": source, "startedAt": now_iso()}
    patch_state(root, providerTransition=transition)
    return transition


def _transition_host_runtime(root: Path, action: str, target: str, route_changed: bool) -> tuple[dict[str, Any], dict[str, Any] | None]:
    if action == "restart":
        started = run_host(root, ["start"], target=target)
        if not started.get("ok"):
            return started, None
        boundary = run_host(root, ["restart"], target=target)
        return boundary, {"providerStart": started, "gatewayRestart": boundary}
    primary = run_host(root, [action], target=target)
    if not primary.get("ok"):
        return primary, None
    if route_changed or action == "enable":
        boundary = run_host(root, ["restart"], target=target)
        if not boundary.get("ok"):
            return boundary, {"primary": primary, "gatewayRestart": boundary}
        return primary, {"primary": primary, "gatewayRestart": boundary}
    return primary, {"primary": primary, "gatewayRestart": None}


def provider_transition(root: Path, action: str, explicit: str | None) -> tuple[int, dict[str, Any]]:
    """Compatibility-only provider transition API; CLI no longer calls this."""
    try:
        target, source = resolve_target(root, explicit)
    except Exception as error:
        return 2, {"result": "error", "phase": "provider-selection", "error": str(error), "stateChanged": False}
    preflight = checks.preflight_start(root, target)
    if preflight["verdict"] in {"NOT_READY", "INDETERMINATE"}:
        return preflight["exitCode"], {"result": "error", "phase": "preflight", "provider": target, "preflight": preflight, "stateChanged": False}
    route_plan = openclaw_route.plan(root, target)
    if not route_plan.get("ok"):
        return 2, {"result": "error", "phase": "route-preflight", "provider": target, "route": route_plan, "stateChanged": False}
    route_changed = route_plan.get("currentProvider") != target or route_plan.get("currentModel") != route_plan.get("model")
    transition = begin_transition(root, target, source)
    route = openclaw_route.begin(root, target)
    if not route.get("ok"):
        return 1, {"result": "error", "phase": "route-transition", "action": action, "provider": target, "transition": transition, "route": route, "selectionCommitted": False}
    host, process_boundary = _transition_host_runtime(root, action, target, route_changed)
    if not host.get("ok"):
        route_rollback = openclaw_route.rollback(root)
        return 1, {"result": "error", "phase": "host-transition", "action": action, "provider": target, "transition": transition, "host": host, "processBoundary": process_boundary, "routeRollback": route_rollback, "selectedProvider": load_state(root).get("selectedProvider"), "selectionCommitted": False}
    final_provider = provider.probe(target, timeout=5.0)
    gateway = checks.check_gateway()[0]
    route_after = openclaw_route.plan(root, target)
    route_ready = route_after.get("ok") and route_after.get("currentProvider") == target and route_after.get("currentModel") == route_after.get("model")
    if not final_provider.get("healthy") or gateway.get("status") != "PASS" or not route_ready:
        route_rollback = openclaw_route.rollback(root)
        return 1, {"result": "error", "phase": "post-transition-verification", "action": action, "provider": target, "transition": transition, "providerHealth": final_provider, "gateway": gateway, "route": route_after, "processBoundary": process_boundary, "routeRollback": route_rollback, "selectionCommitted": False}
    route_commit = openclaw_route.commit(root)
    if not route_commit.get("ok"):
        route_rollback = openclaw_route.rollback(root)
        return 1, {"result": "error", "phase": "route-commit", "provider": target, "transition": transition, "routeCommit": route_commit, "routeRollback": route_rollback, "selectionCommitted": False}
    state = commit_provider(root, target, source)
    recovery_budget = recovery_policy.clear_after_manual_transition(root, target)
    return 0, {"result": "ok", "action": action, "provider": target, "selectionSource": source, "providerSelection": state.get("providerSelection"), "host": host.get("output"), "processBoundary": process_boundary, "route": route_commit, "providerRecoveryPolicy": recovery_budget, "verification": {"provider": final_provider, "gateway": gateway, "route": route_after}}


def provider_snapshot() -> dict[str, Any]:
    values: dict[str, Any] = {}
    for name in provider.SUPPORTED_PROVIDERS:
        values[name] = provider.probe(name)
    return {"providerMetadata": values, "authority": "openclaw"}


def do_check(root: Path, args: list[str]) -> tuple[int, dict[str, Any]]:
    if len(args) < 2:
        return 2, {"result": "error", "error": "Usage: cnxclaw check system|cogentnexus-openclaw|config|openclaw|gateway|provider|model|storage|recovery|delivery|resources"}
    component = args[1].lower()
    explicit = option_value(args[2:], "--provider")
    if component == "provider" and len(args) >= 3 and not args[2].startswith("-"):
        explicit = args[2]
    try:
        report = checks.system_check(root, explicit) if component == "system" else checks.component_check(root, component, explicit)
        return int(report["exitCode"]), report
    except Exception as error:
        return 3, {"check": component, "verdict": "INDETERMINATE", "exitCode": 3, "error": str(error), "readOnly": True, "stateChanged": False}


def emit(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def help_text() -> str:
    return """CogentNexus-OpenClaw v0.9.5

CNX lifecycle (no provider/model selection):
  cnxclaw.cmd start
  cnxclaw.cmd stop
  cnxclaw.cmd restart
  cnxclaw.cmd status
  cnxclaw.cmd enable
  cnxclaw.cmd disable
  cnxclaw.cmd reset
  cnxclaw.cmd uninstall

Local adapter lifecycle (does not mutate OpenClaw routing):
  cnxclaw.cmd local ollama start
  cnxclaw.cmd local ollama stop
  cnxclaw.cmd local ollama restart
  cnxclaw.cmd local ollama status
  cnxclaw.cmd local ollama check

Inspection (read-only):
  cnxclaw.cmd check system
  cnxclaw.cmd check cogentnexus-openclaw
  cnxclaw.cmd check provider
  cnxclaw.cmd provider list
  cnxclaw.cmd provider status

Provider/model/auth/routing selection is owned by OpenClaw.
"""


def main(argv: list[str] | None = None) -> int:
    root, args, json_mode = parse_globals(list(sys.argv[1:] if argv is None else argv))
    if not args or args[0] in {"-h", "--help", "help"}:
        print(help_text())
        return 0
    command = args[0].lower()

    if command == "local":
        if len(args) != 3:
            emit({"result": "error", "error": "Usage: cnxclaw local ollama start|stop|restart|status|check"})
            return 2
        try:
            code, result = local_adapter.run(root, args[1], args[2])
        except ValueError as error:
            emit({"result": "error", "error": str(error)})
            return 2
        emit(result)
        return code

    if command in {"start", "stop", "restart", "status", "enable", "disable", "reset", "uninstall"} and has_option(args[1:], "--provider"):
        emit({"result": "error", "error": "--provider is no longer a CNX lifecycle authority in v0.9.5; select provider/model in OpenClaw instead", "compatibility": "legacy input rejected and no route/lifecycle transition was attempted"})
        return 2

    if command == "check":
        code, report = do_check(root, args)
        print(json.dumps(report, ensure_ascii=False, indent=2) if json_mode else checks.render(report))
        return code

    if command == "provider":
        action = args[1].lower() if len(args) > 1 else "status"
        if action not in {"list", "status"} or len(args) > 2:
            emit({"result": "error", "error": "Usage: cnxclaw provider list|status"})
            return 2
        emit(provider_snapshot())
        return 0

    if command == "status":
        if len(args) != 1:
            emit({"result": "error", "error": "Usage: cnxclaw status"})
            return 2
        host = run_host(root, ["status"], timeout=120)
        emit({"host": host.get("output") if host.get("ok") else host, **provider_snapshot()})
        return 0 if host.get("ok") else 1

    if command in {"start", "stop", "restart", "enable", "disable"}:
        if len(args) != 1:
            emit({"result": "error", "error": f"Usage: cnxclaw {command}"})
            return 2
        return delegate(root, [command])

    if command in {"reset", "uninstall"}:
        if len(args) != 1:
            emit({"result": "error", "error": f"Usage: cnxclaw {command}"})
            return 2
        return delegate(root, [command], interactive=True)

    if command == "cloud":
        emit({"result": "delegated-to-openclaw", "authority": "openclaw", "message": "Cloud provider/model selection is owned by OpenClaw; CogentNexus-OpenClaw does not implement a cloud routing transition."})
        return 0

    return delegate(root, args)


if __name__ == "__main__":
    raise SystemExit(main())
