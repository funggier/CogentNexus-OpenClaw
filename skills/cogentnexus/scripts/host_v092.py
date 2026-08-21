#!/usr/bin/env python3
"""Final CogentNexus v0.9.2 Host overlay."""
from __future__ import annotations

import host_provider_v092 as base

legacy = base.legacy
providers = base.providers
ORIGINAL_RESTART_MANAGED = legacy.restart_managed


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
    result = ORIGINAL_RESTART_MANAGED(root)
    result["provider"] = target
    result["providerLifecycle"] = started
    return result


legacy.restart_managed = restart_managed


if __name__ == "__main__":
    raise SystemExit(legacy.main())
