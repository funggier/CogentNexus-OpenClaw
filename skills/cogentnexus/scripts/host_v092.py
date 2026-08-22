#!/usr/bin/env python3
"""Final CogentNexus v0.9.2 Host overlay."""
from __future__ import annotations

from datetime import datetime, timezone

import host_provider_v092 as base
import provider_event_liveness_v092 as provider_event_liveness

provider_event_liveness.patch_provider_events(base.provider_events)

legacy = base.legacy
providers = base.providers
provider_events = base.provider_events
ORIGINAL_ENABLE_MANAGED = legacy.enable
ORIGINAL_RESTART_MANAGED = legacy.restart_managed
BASE_PROVIDER_RUNTIME = base.provider_aware_runtime


def _parse_utc(value):
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def progress_for_call(root, target, started_at):
    """Match provider proof-of-life to a call using normalized UTC time."""
    progress = provider_events.latest_progress(root, target)
    if not isinstance(progress, dict):
        return None
    event_time = _parse_utc(progress.get("at"))
    started_time = _parse_utc(started_at)
    if event_time is None or started_time is None or event_time < started_time:
        return None
    return progress


# The provider overlay originally compared ISO strings. Different valid UTC
# spellings (`Z` vs `+00:00`) are not lexicographically ordered by time, so the
# final v0.9.2 overlay replaces only that evidence matcher.
base._progress_for_call = progress_for_call


def provider_event_aware_runtime(root, *args, timeout=180, check=True):
    """Linearize provider start, event adapter, then Gateway activation.

    The provider must be reachable before LM Studio's blocking runtime log stream
    can be attached. Starting the adapter before the Gateway closes the small
    activation window where managed inference could begin without provider event
    evidence being observable.
    """
    values = list(args)
    provider_requested = "--provider" in values
    lifecycle = len(values) >= 2 and values[0] == "lifecycle"
    action = values[1] if lifecycle else None
    if not provider_requested or action != "start":
        return BASE_PROVIDER_RUNTIME(root, *args, timeout=timeout, check=check)

    target = base._state_provider(root)
    cleaned = [value for value in values if value != "--provider"]
    command = [base.sys.executable, str(base.legacy.runtime_path()), "--root", str(root), *cleaned]
    if not target:
        return base._finish(base._completed(command, 2, {
            "result": "error",
            "error": "provider selection required; use cnx start --provider ollama|lmstudio",
            "provider": None,
        }), check)

    base._set_legacy_ollama_mode(root, target)
    provider_result = providers.start(target, timeout=min(60.0, float(timeout)))
    if not provider_result.get("ok"):
        return base._finish(base._completed(command, 2, {
            "result": "error",
            "phase": "provider-start",
            "provider": target,
            "providerLifecycle": provider_result,
        }), check)

    adapter = provider_events.ensure_adapter(root, target)
    runtime_result = base.ORIGINAL_RUNTIME(root, *cleaned, timeout=timeout, check=False)
    adapter_rollback = None
    if runtime_result.returncode != 0:
        # The Gateway/runtime activation did not commit. Do not leave a CNX
        # provider watcher behind solely because provider start succeeded.
        adapter_rollback = provider_events.stop_adapter(root, target)
    return base._finish(base._completed(command, runtime_result.returncode, {
        "provider": target,
        "providerLifecycle": provider_result,
        "providerEventAdapter": adapter,
        "providerEventAdapterRollback": adapter_rollback,
        "runtime": base._parse_stdout(runtime_result.stdout),
    }, runtime_result.stderr or ""), check)


# host_provider_v092 installed its provider-aware wrapper during import. Replace
# only the final v0.9.2 runtime surface so the event adapter is attached before
# Gateway activation while all v0.9.1 lifecycle internals remain unchanged.
legacy.runtime = provider_event_aware_runtime


def enable_managed(root):
    """Ensure transactional enable failure cannot leak a managed watcher."""
    try:
        return ORIGINAL_ENABLE_MANAGED(root)
    except Exception:
        try:
            provider_events.stop_adapter(root)
        except Exception:
            # Cleanup evidence must never mask the original transactional enable
            # failure. A later disable/reconciliation pass can retry cleanup.
            pass
        raise


def restart_managed(root):
    target = base._state_provider(root)
    if not target:
        raise RuntimeError("provider selection required before managed restart")
    # Restart intent means the remembered provider must be running. Persist that
    # desired state before action so a power loss is recoverable by the supervisor.
    legacy.transition(root, desiredProvider="running")
    started = providers.start(target, timeout=45)
    if not started.get("ok"):
        raise RuntimeError(f"selected provider '{target}' failed to start before restart: {started}")
    adapter = provider_events.ensure_adapter(root, target)
    result = ORIGINAL_RESTART_MANAGED(root)
    result["provider"] = target
    result["providerLifecycle"] = started
    result["providerEventAdapter"] = adapter
    return result


legacy.enable = enable_managed
legacy.restart_managed = restart_managed


if __name__ == "__main__":
    raise SystemExit(legacy.main())
