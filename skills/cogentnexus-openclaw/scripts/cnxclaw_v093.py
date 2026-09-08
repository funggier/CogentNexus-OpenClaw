#!/usr/bin/env python3
"""CogentNexus-OpenClaw v0.9.4 provider-boundary CLI facade.

Managed lifecycle operations remain Ollama-only. Cloud providers use the
OpenClaw-owned pass-through mode and are not controlled by this CLI facade.
"""
from __future__ import annotations

import json
import sys
from typing import Any

import cnxclaw as legacy
import host
import provider_v093 as ollama_provider

openclaw_route = legacy.openclaw_route

# Narrow the v0.9.2 facade/check modules without rewriting accepted lifecycle
# internals.  Host-control receives CNXCLAW_PROVIDER_TARGET=ollama from transitions.
legacy.provider = ollama_provider
legacy.checks.provider = ollama_provider
if hasattr(legacy.checks, "base") and hasattr(legacy.checks.base, "provider"):
    legacy.checks.base.provider = ollama_provider


def _emit_error(message: str) -> int:
    print(json.dumps({"result": "error", "error": message}, ensure_ascii=False, indent=2))
    return 2


def _provider_option(args: list[str]) -> str | None:
    for index, value in enumerate(args):
        if value == "--provider" and index + 1 < len(args):
            return args[index + 1]
        if value.startswith("--provider="):
            return value.split("=", 1)[1]
    return None


def _has_provider_option(args: list[str]) -> bool:
    return _provider_option(args) is not None


def _force_ollama(args: list[str]) -> list[str]:
    explicit = _provider_option(args)
    if explicit is not None:
        ollama_provider.normalize_provider(explicit)
        return args
    return [*args, "--provider", "ollama"]


def help_text() -> str:
    return """CogentNexus-OpenClaw v0.9.4 (managed Ollama + Cloud pass-through)

Lifecycle:
  cnxclaw.cmd start
  cnxclaw.cmd stop
  cnxclaw.cmd restart
  cnxclaw.cmd enable
  cnxclaw.cmd disable
  cnxclaw.cmd cloud
  cnxclaw.cmd reset
  cnxclaw.cmd uninstall

Provider:
  Ollama is the only provider managed by CogentNexus-OpenClaw in v0.9.4.
  Configured Cloud routes use OpenClaw-owned pass-through via 'cnxclaw cloud'.
  Explicit '--provider ollama' remains accepted for compatibility.
  LM Studio is not started, stopped, probed, selected, or managed by CogentNexus-OpenClaw.

Inspection (read-only):
  cnxclaw.cmd status
  cnxclaw.cmd check system
  cnxclaw.cmd check provider [ollama]
  cnxclaw.cmd check cogentnexus-openclaw|config|openclaw|gateway|model|storage|recovery|delivery|resources
  cnxclaw.cmd provider list
  cnxclaw.cmd provider status

Existing Ticket/session/policy/gateway/supervisor commands remain available.
"""


def cloud_transition(root: Any) -> tuple[int, dict[str, Any]]:
    """Leave provider ownership with OpenClaw while retaining passive hooks."""
    try:
        restored = openclaw_route.restore_native(root)
    except Exception:
        return 1, {
            "result": "error",
            "phase": "restore-native-openclaw-route",
            "safety": "Cloud transition stopped before Host or plugin mutation",
        }
    if not restored.get("ok"):
        return 1, {
            "result": "error",
            "phase": "restore-native-openclaw-route",
            "safety": "Cloud transition stopped before Host or plugin mutation",
        }

    try:
        host.startup(root, "disable", check=True)
        policy_changed = host.remove_policy(root.parent)
        host.configure_cloud_plugin()
        state = host.transition(
            root,
            mode="passthrough",
            desiredGateway="running",
            desiredProvider="unchanged",
        )
        host.plugin_enabled(True)
        host.run(
            [host.openclaw_executable(), "gateway", "restart"],
            timeout=180,
            check=True,
        )
    except Exception:
        return 1, {
            "result": "error",
            "phase": "cloud-transition",
            "safety": "Cloud transition failed without exposing provider or credential details",
        }

    return 0, {
        "result": "ok",
        "action": "cloud",
        "mode": state.get("mode"),
        "desiredGateway": state.get("desiredGateway"),
        "desiredProvider": state.get("desiredProvider"),
        "pluginEnabled": True,
        "policyChanged": policy_changed,
        "gatewayRestarted": True,
    }


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    # Preserve global --root/--json parsing in the accepted backend while finding
    # the first non-global command token for v0.9.4 policy enforcement.
    _, cleaned, _ = legacy.parse_globals(args)
    if not cleaned or cleaned[0] in {"-h", "--help", "help"}:
        print(help_text())
        return 0

    command = cleaned[0].lower()

    if command == "cloud":
        if len(cleaned) != 1:
            return _emit_error("Usage: cnxclaw cloud")
        root, _, _ = legacy.parse_globals(args)
        code, result = cloud_transition(root)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return code

    try:
        explicit = _provider_option(cleaned[1:])
        if explicit is not None:
            ollama_provider.normalize_provider(explicit)

        if command == "check" and len(cleaned) >= 3 and cleaned[1].lower() == "provider" and not cleaned[2].startswith("-"):
            ollama_provider.normalize_provider(cleaned[2])

        # All provider-bearing lifecycle commands become deterministic.  This
        # also migrates a persisted v0.9.2 lmstudio selection to Ollama during
        # the first verified v0.9.4 transition.
        if command in {"start", "restart", "enable", "reset"} and not _has_provider_option(cleaned[1:]):
            args = [*args, "--provider", "ollama"]
    except ValueError as error:
        return _emit_error(str(error))

    return legacy.main(args)


if __name__ == "__main__":
    raise SystemExit(main())
