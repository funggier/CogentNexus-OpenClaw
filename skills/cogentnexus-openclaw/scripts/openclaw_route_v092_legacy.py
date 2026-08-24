#!/usr/bin/env python3
"""Transactional OpenClaw provider-route profile for CogentNexus-OpenClaw v0.9.2.

This module owns only the narrow OpenClaw fields needed by the selected local
provider while CogentNexus-OpenClaw is MANAGED:
- the default model route;
- provider/agent timeout values needed by a slow local provider;
- LM Studio llama.cpp tool-schema compatibility keywords.

The accepted v0.9.1 Host watchdog compatibility remains authoritative for
`diagnostics.stuckSessionAbortMs`; this module deliberately does not manage it.

A short-lived byte-for-byte rollback copy protects an in-progress provider
switch. A separate field-level baseline restores pre-CNXCLAW values on the native
PASSTHROUGH boundary without replacing unrelated OpenClaw configuration.
"""
from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROVIDER_PREFIX = {"ollama": "ollama", "lmstudio": "lmstudio_local"}
LMSTUDIO_COMPAT_KEYWORDS = ("pattern", "maxLength")
LMSTUDIO_PROVIDER_TIMEOUT_SECONDS = 1100
LMSTUDIO_AGENT_TIMEOUT_SECONDS = 1200


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def creation_flags() -> int:
    return getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0


def openclaw_config_path() -> Path:
    explicit = os.environ.get("OPENCLAW_CONFIG_PATH")
    if explicit:
        return Path(explicit).expanduser().resolve()
    return (Path.home() / ".openclaw" / "openclaw.json").resolve()


def state_path(root: Path) -> Path:
    return root / "host" / "openclaw-route-v092.json"


def rollback_path(root: Path) -> Path:
    return root / "host" / "openclaw-route-v092.before.json"


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise RuntimeError(f"JSON document must be an object: {path}")
    return value


def _mode_for_replace(path: Path) -> int:
    if path.exists():
        try:
            return path.stat().st_mode & 0o777
        except OSError:
            pass
    return 0o600


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = _mode_for_replace(path)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if os.name != "nt":
        os.chmod(temporary, mode)
    os.replace(temporary, path)


def _atomic_bytes(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = _mode_for_replace(path)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(value)
    if os.name != "nt":
        os.chmod(temporary, mode)
    os.replace(temporary, path)


def _snapshot(container: dict[str, Any], key: str) -> dict[str, Any]:
    if key in container:
        return {"exists": True, "value": copy.deepcopy(container[key])}
    return {"exists": False}


def _restore(container: dict[str, Any], key: str, snapshot: dict[str, Any] | None) -> None:
    if not isinstance(snapshot, dict):
        return
    if snapshot.get("exists"):
        container[key] = copy.deepcopy(snapshot.get("value"))
    else:
        container.pop(key, None)


def _ensure_dict(container: dict[str, Any], key: str) -> dict[str, Any]:
    current = container.get(key)
    if isinstance(current, dict):
        return current
    current = {}
    container[key] = current
    return current


def _primary_model(config: dict[str, Any]) -> str | None:
    agents = config.get("agents")
    defaults = agents.get("defaults") if isinstance(agents, dict) else None
    model = defaults.get("model") if isinstance(defaults, dict) else None
    if isinstance(model, str):
        return model
    if isinstance(model, dict):
        primary = model.get("primary")
        return primary if isinstance(primary, str) and primary else None
    return None


def _set_primary_model(config: dict[str, Any], model_ref: str) -> None:
    defaults = _ensure_dict(_ensure_dict(config, "agents"), "defaults")
    current = defaults.get("model")
    if isinstance(current, dict):
        current["primary"] = model_ref
    elif isinstance(current, str):
        defaults["model"] = model_ref
    else:
        defaults["model"] = {"primary": model_ref}


def _prefix_owner(model_ref: str | None) -> str | None:
    if not isinstance(model_ref, str) or "/" not in model_ref:
        return None
    prefix = model_ref.split("/", 1)[0].strip().lower()
    for provider_name, provider_prefix in PROVIDER_PREFIX.items():
        if prefix == provider_prefix:
            return provider_name
    return None


def _provider_config(config: dict[str, Any], provider_name: str) -> tuple[str, dict[str, Any] | None]:
    key = PROVIDER_PREFIX[provider_name]
    models = config.get("models")
    providers = models.get("providers") if isinstance(models, dict) else None
    value = providers.get(key) if isinstance(providers, dict) else None
    return key, value if isinstance(value, dict) else None


def _route_from_provider_catalog(config: dict[str, Any], provider_name: str) -> str | None:
    prefix, provider_config = _provider_config(config, provider_name)
    if not provider_config:
        return None
    rows = provider_config.get("models")
    if not isinstance(rows, list):
        return None
    for row in rows:
        if not isinstance(row, dict):
            continue
        value = row.get("id") or row.get("name") or row.get("model")
        if isinstance(value, str) and value:
            return f"{prefix}/{value}"
    return None


def _env_route(provider_name: str) -> str | None:
    key = "CNXCLAW_LMSTUDIO_MODEL" if provider_name == "lmstudio" else "CNXCLAW_OLLAMA_MODEL"
    value = os.environ.get(key)
    if not value:
        return None
    value = value.strip()
    prefix = PROVIDER_PREFIX[provider_name]
    return value if value.startswith(prefix + "/") else f"{prefix}/{value}"


def _load_state(root: Path) -> dict[str, Any]:
    path = state_path(root)
    if not path.exists():
        return {"schemaVersion": 1, "routes": {}, "baseline": {}}
    value = _load_json(path)
    value.setdefault("schemaVersion", 1)
    value.setdefault("routes", {})
    value.setdefault("baseline", {})
    return value


def _save_state(root: Path, state: dict[str, Any]) -> None:
    state["updatedAt"] = now_iso()
    _atomic_json(state_path(root), state)


def _find_model_entry(config: dict[str, Any], model_ref: str) -> dict[str, Any] | None:
    if "/" not in model_ref:
        return None
    prefix, model_id = model_ref.split("/", 1)
    models = config.get("models")
    providers = models.get("providers") if isinstance(models, dict) else None
    provider_cfg = providers.get(prefix) if isinstance(providers, dict) else None
    rows = provider_cfg.get("models") if isinstance(provider_cfg, dict) else None
    if not isinstance(rows, list):
        return None
    for row in rows:
        if not isinstance(row, dict):
            continue
        value = row.get("id") or row.get("name") or row.get("model")
        if value == model_id:
            return row
    return None


def _capture_baseline(config: dict[str, Any], state: dict[str, Any], model_ref: str | None = None) -> None:
    baseline = state.setdefault("baseline", {})
    defaults = _ensure_dict(_ensure_dict(config, "agents"), "defaults")
    baseline.setdefault("model", _snapshot(defaults, "model"))
    baseline.setdefault("agentTimeoutSeconds", _snapshot(defaults, "timeoutSeconds"))

    provider_timeouts = baseline.setdefault("providerTimeouts", {})
    providers = _ensure_dict(_ensure_dict(config, "models"), "providers")
    for provider_key in PROVIDER_PREFIX.values():
        provider_cfg = providers.get(provider_key)
        if isinstance(provider_cfg, dict) and provider_key not in provider_timeouts:
            provider_timeouts[provider_key] = _snapshot(provider_cfg, "timeoutSeconds")

    if model_ref and model_ref.startswith(PROVIDER_PREFIX["lmstudio"] + "/"):
        compat = baseline.setdefault("modelCompat", {})
        if model_ref not in compat:
            row = _find_model_entry(config, model_ref)
            if row is not None:
                compat[model_ref] = _snapshot(row, "compat")


def _restore_managed_knobs(config: dict[str, Any], state: dict[str, Any], restore_model: bool) -> None:
    baseline = state.get("baseline")
    if not isinstance(baseline, dict):
        return
    defaults = _ensure_dict(_ensure_dict(config, "agents"), "defaults")

    if restore_model:
        _restore(defaults, "model", baseline.get("model"))
    _restore(defaults, "timeoutSeconds", baseline.get("agentTimeoutSeconds"))

    providers = _ensure_dict(_ensure_dict(config, "models"), "providers")
    provider_timeouts = baseline.get("providerTimeouts")
    if isinstance(provider_timeouts, dict):
        for provider_key, snapshot in provider_timeouts.items():
            provider_cfg = providers.get(provider_key)
            if isinstance(provider_cfg, dict):
                _restore(provider_cfg, "timeoutSeconds", snapshot)

    compat = baseline.get("modelCompat")
    if isinstance(compat, dict):
        for model_ref, snapshot in compat.items():
            row = _find_model_entry(config, model_ref)
            if row is not None:
                _restore(row, "compat", snapshot)


def _resolve_route(config: dict[str, Any], state: dict[str, Any], provider_name: str) -> str:
    prefix = PROVIDER_PREFIX[provider_name]
    current = _primary_model(config)
    if isinstance(current, str) and current.startswith(prefix + "/"):
        return current

    routes = state.get("routes")
    if isinstance(routes, dict):
        stored = routes.get(provider_name)
        if isinstance(stored, str) and stored.startswith(prefix + "/"):
            return stored

    environment = _env_route(provider_name)
    if environment:
        return environment

    catalog = _route_from_provider_catalog(config, provider_name)
    if catalog:
        return catalog

    baseline = state.get("baseline")
    model_snapshot = baseline.get("model") if isinstance(baseline, dict) else None
    if isinstance(model_snapshot, dict) and model_snapshot.get("exists"):
        value = model_snapshot.get("value")
        candidate = value if isinstance(value, str) else value.get("primary") if isinstance(value, dict) else None
        if isinstance(candidate, str) and candidate.startswith(prefix + "/"):
            return candidate

    raise RuntimeError(
        f"OpenClaw has no resolvable model route for provider '{provider_name}'. "
        f"Configure a {prefix}/... model first or set "
        f"{'CNXCLAW_LMSTUDIO_MODEL' if provider_name == 'lmstudio' else 'CNXCLAW_OLLAMA_MODEL'}."
    )


def _openclaw_executable() -> str | None:
    candidates = ("openclaw.cmd", "openclaw.exe", "openclaw") if os.name == "nt" else ("openclaw",)
    for name in candidates:
        value = shutil.which(name)
        if value:
            return value
    return None


def validate_openclaw_config() -> dict[str, Any]:
    executable = _openclaw_executable()
    if not executable:
        return {"ok": False, "error": "OpenClaw CLI unavailable"}
    try:
        proc = subprocess.run(
            [executable, "config", "validate"],
            capture_output=True,
            text=True,
            timeout=60,
            creationflags=creation_flags(),
        )
        return {
            "ok": proc.returncode == 0,
            "exitCode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
        }
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def plan(root: Path, provider_name: str) -> dict[str, Any]:
    if provider_name not in PROVIDER_PREFIX:
        return {"ok": False, "error": f"unsupported provider: {provider_name}"}
    path = openclaw_config_path()
    if not path.is_file():
        return {"ok": False, "error": f"OpenClaw config not found: {path}", "path": str(path)}
    try:
        config = _load_json(path)
        state = _load_state(root)
        current = _primary_model(config)
        current_owner = _prefix_owner(current)
        route = _resolve_route(config, state, provider_name)
        key, provider_cfg = _provider_config(config, provider_name)
        if provider_name == "lmstudio" and provider_cfg is None:
            raise RuntimeError(
                "LM Studio provider route requires an existing OpenClaw models.providers.lmstudio_local configuration"
            )
        return {
            "ok": True,
            "provider": provider_name,
            "providerKey": key,
            "model": route,
            "currentModel": current,
            "currentProvider": current_owner,
            "configPath": str(path),
            "mutatesState": False,
        }
    except Exception as exc:
        return {"ok": False, "provider": provider_name, "error": str(exc), "configPath": str(path)}


def recover_pending(root: Path) -> dict[str, Any]:
    state = _load_state(root)
    transaction = state.get("transaction")
    backup = rollback_path(root)
    if not isinstance(transaction, dict) or transaction.get("status") != "pending":
        return {"ok": True, "recovered": False}
    if not backup.is_file():
        return {"ok": False, "recovered": False, "error": "pending OpenClaw route transaction has no rollback copy"}
    config_path = openclaw_config_path()
    _atomic_bytes(config_path, backup.read_bytes())
    validation = validate_openclaw_config()
    if not validation.get("ok"):
        return {"ok": False, "recovered": False, "error": "rollback config failed validation", "validation": validation}
    backup.unlink(missing_ok=True)
    state["transaction"] = None
    state["lastRollbackAt"] = now_iso()
    _save_state(root, state)
    return {"ok": True, "recovered": True, "validation": validation}


def begin(root: Path, provider_name: str) -> dict[str, Any]:
    pending = recover_pending(root)
    if not pending.get("ok"):
        return {"ok": False, "phase": "recover-pending", "details": pending}

    plan_result = plan(root, provider_name)
    if not plan_result.get("ok"):
        return {"ok": False, "phase": "plan", "details": plan_result}

    path = openclaw_config_path()
    original = path.read_bytes()
    config = _load_json(path)
    state = _load_state(root)

    current = _primary_model(config)
    current_owner = _prefix_owner(current)
    if current and current_owner:
        state.setdefault("routes", {})[current_owner] = current

    route = str(plan_result["model"])
    _capture_baseline(config, state, route)
    _restore_managed_knobs(config, state, restore_model=False)
    _set_primary_model(config, route)

    if provider_name == "lmstudio":
        defaults = _ensure_dict(_ensure_dict(config, "agents"), "defaults")
        _, provider_cfg = _provider_config(config, provider_name)
        if provider_cfg is None:
            return {"ok": False, "phase": "apply", "error": "LM Studio provider config disappeared during route transaction"}
        defaults["timeoutSeconds"] = LMSTUDIO_AGENT_TIMEOUT_SECONDS
        provider_cfg["timeoutSeconds"] = LMSTUDIO_PROVIDER_TIMEOUT_SECONDS

        row = _find_model_entry(config, route)
        if row is None:
            return {"ok": False, "phase": "apply", "error": f"LM Studio model entry not found for {route}"}
        compat = row.get("compat")
        if not isinstance(compat, dict):
            compat = {}
            row["compat"] = compat
        existing = compat.get("unsupportedToolSchemaKeywords")
        values = [str(value) for value in existing] if isinstance(existing, list) else []
        for keyword in LMSTUDIO_COMPAT_KEYWORDS:
            if keyword not in values:
                values.append(keyword)
        compat["unsupportedToolSchemaKeywords"] = values

    rollback = rollback_path(root)
    _atomic_bytes(rollback, original)
    state["transaction"] = {
        "status": "pending",
        "provider": provider_name,
        "model": route,
        "startedAt": now_iso(),
    }
    _save_state(root, state)

    try:
        _atomic_json(path, config)
        validation = validate_openclaw_config()
        if not validation.get("ok"):
            raise RuntimeError(f"OpenClaw config validate failed: {validation}")
    except Exception as exc:
        _atomic_bytes(path, original)
        rollback.unlink(missing_ok=True)
        state["transaction"] = None
        state["lastError"] = str(exc)
        _save_state(root, state)
        return {"ok": False, "phase": "validate", "error": str(exc)}

    return {
        "ok": True,
        "provider": provider_name,
        "model": route,
        "validation": validation,
        "transactionPending": True,
    }


def commit(root: Path) -> dict[str, Any]:
    state = _load_state(root)
    transaction = state.get("transaction")
    if not isinstance(transaction, dict) or transaction.get("status") != "pending":
        return {"ok": True, "committed": False, "reason": "no pending route transaction"}
    provider_name = str(transaction.get("provider"))
    model_ref = str(transaction.get("model"))
    state["activeProvider"] = provider_name
    state["activeModel"] = model_ref
    state.setdefault("routes", {})[provider_name] = model_ref
    state["transaction"] = None
    state["lastCommittedAt"] = now_iso()
    rollback_path(root).unlink(missing_ok=True)
    _save_state(root, state)
    return {"ok": True, "committed": True, "provider": provider_name, "model": model_ref}


def rollback(root: Path) -> dict[str, Any]:
    state = _load_state(root)
    backup = rollback_path(root)
    if not backup.is_file():
        state["transaction"] = None
        _save_state(root, state)
        return {"ok": True, "rolledBack": False, "reason": "rollback copy absent"}
    path = openclaw_config_path()
    _atomic_bytes(path, backup.read_bytes())
    validation = validate_openclaw_config()
    if not validation.get("ok"):
        return {"ok": False, "rolledBack": False, "validation": validation}
    backup.unlink(missing_ok=True)
    state["transaction"] = None
    state["lastRollbackAt"] = now_iso()
    _save_state(root, state)
    return {"ok": True, "rolledBack": True, "validation": validation}


def restore_native(root: Path) -> dict[str, Any]:
    pending = recover_pending(root)
    if not pending.get("ok"):
        return {"ok": False, "phase": "recover-pending", "details": pending}

    path = openclaw_config_path()
    route_state = state_path(root)
    if not route_state.is_file():
        return {"ok": True, "restored": False, "reason": "no managed OpenClaw route state"}
    state = _load_state(root)
    if not state.get("baseline"):
        return {"ok": True, "restored": False, "reason": "no baseline snapshot"}

    original = path.read_bytes()
    config = _load_json(path)
    _restore_managed_knobs(config, state, restore_model=True)
    try:
        _atomic_json(path, config)
        validation = validate_openclaw_config()
        if not validation.get("ok"):
            raise RuntimeError(f"OpenClaw config validate failed after restore: {validation}")
    except Exception as exc:
        _atomic_bytes(path, original)
        return {"ok": False, "restored": False, "error": str(exc)}

    rollback_path(root).unlink(missing_ok=True)
    route_state.unlink(missing_ok=True)
    return {"ok": True, "restored": True, "validation": validation}
