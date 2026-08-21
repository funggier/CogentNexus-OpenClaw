#!/usr/bin/env python3
"""CogentNexus v0.9.2 provider-neutral Host overlay.

The accepted v0.9.1 Ticket, delivery, single-authority and Direct-stall recovery
logic remains unchanged. This layer replaces only the local provider lifecycle
boundary so `--provider` means the durable selected provider (Ollama or LM
Studio), not hard-coded Ollama.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import host_stall_v091 as stall
import provider as providers

legacy = stall.legacy
v091 = stall.v091
ORIGINAL_RUNTIME = legacy.runtime
BASE_SUPERVISOR_TICK = stall.BASE_SUPERVISOR_TICK
HERE = Path(__file__).resolve()


def startup_path_v092() -> Path:
    return HERE.with_name("startup_v092.py")


legacy.startup_path = startup_path_v092


def _state_provider(root: Path) -> str | None:
    override = os.environ.get("CNX_PROVIDER_TARGET")
    if override:
        return providers.normalize_provider(override)
    state = legacy.load_state(root)
    transition = state.get("providerTransition")
    if isinstance(transition, dict) and transition.get("to"):
        return providers.normalize_provider(str(transition["to"]))
    selected = state.get("selectedProvider")
    if selected:
        return providers.normalize_provider(str(selected))
    installed = providers.installed_providers()
    return installed[0] if len(installed) == 1 else None


def _runtime_config_path(root: Path) -> Path:
    return root / "runtime" / "config.json"


def _set_legacy_ollama_mode(root: Path, selected: str | None) -> dict[str, Any]:
    """Keep the v0.9.1 generic supervisor from reviving an unselected Ollama."""
    path = _runtime_config_path(root)
    try:
        value = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"schemaVersion": 1}
    except Exception as error:
        raise RuntimeError(f"invalid CogentNexus runtime config: {error}") from error
    if not isinstance(value, dict):
        raise RuntimeError("CogentNexus runtime config must be a JSON object")
    supervisor = value.get("supervisor") if isinstance(value.get("supervisor"), dict) else {}
    desired = "auto" if selected == "ollama" else "disabled"
    previous = supervisor.get("ollamaMode")
    if previous == desired:
        return {"changed": False, "before": previous, "after": desired}
    supervisor["ollamaMode"] = desired
    value["supervisor"] = supervisor
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)
    return {"changed": True, "before": previous, "after": desired}


def _parse_stdout(value: str | None) -> Any:
    text = (value or "").strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def _completed(args: list[str], returncode: int, payload: dict[str, Any], stderr: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(args=args, returncode=returncode, stdout=json.dumps(payload, ensure_ascii=False, indent=2) + "\n", stderr=stderr)


def _finish(result: subprocess.CompletedProcess[str], check: bool) -> subprocess.CompletedProcess[str]:
    if check and result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout or "provider-aware runtime lifecycle failed").strip())
    return result


def provider_aware_runtime(root: Path, *args: str, timeout: int = 180, check: bool = True) -> subprocess.CompletedProcess[str]:
    """Translate legacy lifecycle --provider into the selected provider adapter.

    Gateway is always quiesced before provider stop, and provider readiness is
    verified before Gateway start. This preserves the v0.9.1 recovery ordering.
    """
    values = list(args)
    provider_requested = "--provider" in values
    lifecycle = len(values) >= 2 and values[0] == "lifecycle"
    action = values[1] if lifecycle else None
    if not provider_requested or action not in {"start", "stop"}:
        return ORIGINAL_RUNTIME(root, *args, timeout=timeout, check=check)

    target = _state_provider(root)
    cleaned = [value for value in values if value != "--provider"]
    command = [sys.executable, str(legacy.runtime_path()), "--root", str(root), *cleaned]
    if not target:
        return _finish(_completed(command, 2, {
            "result": "error",
            "error": "provider selection required; use cnx start --provider ollama|lmstudio",
            "provider": None,
        }), check)

    _set_legacy_ollama_mode(root, target)
    if action == "start":
        provider_result = providers.start(target, timeout=min(60.0, float(timeout)))
        if not provider_result.get("ok"):
            return _finish(_completed(command, 2, {
                "result": "error",
                "phase": "provider-start",
                "provider": target,
                "providerLifecycle": provider_result,
            }), check)
        runtime_result = ORIGINAL_RUNTIME(root, *cleaned, timeout=timeout, check=False)
        payload = {
            "provider": target,
            "providerLifecycle": provider_result,
            "runtime": _parse_stdout(runtime_result.stdout),
        }
        return _finish(_completed(command, runtime_result.returncode, payload, runtime_result.stderr or ""), check)

    # Stop inference-capable Gateway first, then stop the selected local provider.
    runtime_result = ORIGINAL_RUNTIME(root, *cleaned, timeout=timeout, check=False)
    if runtime_result.returncode != 0:
        return _finish(runtime_result, check)
    provider_result = providers.stop(target, timeout=min(60.0, float(timeout)))
    code = 0 if provider_result.get("ok") else 2
    payload = {
        "provider": target,
        "runtime": _parse_stdout(runtime_result.stdout),
        "providerLifecycle": provider_result,
        "safeToPowerOff": code == 0,
    }
    return _finish(_completed(command, code, payload), check)


legacy.runtime = provider_aware_runtime


def _run_base_supervisor(root: Path, execute_safe: bool, provider_healthy: bool) -> dict[str, Any]:
    """Reuse v0.9.1 idle/hard-hang logic without an Ollama-only fast-probe bias."""
    original_probe = v091.ollama_fast_probe
    v091.ollama_fast_probe = lambda: provider_healthy
    try:
        return BASE_SUPERVISOR_TICK(root, execute_safe)
    finally:
        v091.ollama_fast_probe = original_probe


def supervisor_tick(root: Path, execute_safe: bool) -> dict[str, Any]:
    state = legacy.load_state(root)
    if state.get("mode") != "managed" or state.get("desiredGateway") != "running":
        return _run_base_supervisor(root, execute_safe, True)

    target = _state_provider(root)
    if not target:
        _set_legacy_ollama_mode(root, None)
        result = _run_base_supervisor(root, execute_safe, True)
        result["selectedProvider"] = None
        result["providerHealth"] = {"healthy": False, "error": "provider selection required"}
        result["providerRecovery"] = "none"
        result["result"] = "provider-selection-required"
        return result

    _set_legacy_ollama_mode(root, target)
    before = providers.probe(target, timeout=3.0)
    recovery: dict[str, Any] | None = None
    current = before
    if state.get("desiredProvider") == "running" and not before.get("healthy") and execute_safe:
        recovery = providers.start(target, timeout=45)
        current = providers.probe(target, timeout=3.0)

    if state.get("desiredProvider") == "running" and not current.get("healthy"):
        result = _run_base_supervisor(root, execute_safe, True)
        result["selectedProvider"] = target
        result["providerHealth"] = current
        result["providerRecovery"] = recovery or "none"
        result["result"] = "provider-degraded"
        return result

    # The accepted Direct-stall classifier is reused unchanged. Its stop/start
    # calls flow through provider_aware_runtime above, preserving quiescence while
    # replacing only the concrete local provider adapter.
    if execute_safe and current.get("healthy") and v091.gateway_fast_probe():
        claim = stall.claim_expired_direct_model_call(root)
        if claim is not None:
            try:
                recovered = stall.recover_expired_direct_model_call(root, claim)
                recovered["selectedProvider"] = target
                recovered["providerHealthBefore"] = before
                recovered["providerRecoveryBeforeStall"] = recovery
                return recovered
            except Exception as error:
                try:
                    stall._release_model_call_claim(root, claim, str(error))
                except Exception:
                    pass
                raise

    result = _run_base_supervisor(root, execute_safe, bool(current.get("healthy")))
    result["selectedProvider"] = target
    result["providerHealth"] = current
    result["providerRecovery"] = recovery or "none"
    return result


legacy.supervisor_tick = supervisor_tick


if __name__ == "__main__":
    raise SystemExit(legacy.main())
