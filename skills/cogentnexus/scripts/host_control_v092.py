#!/usr/bin/env python3
"""CogentNexus v0.9.2 Host control shim.

Preserves every v0.9.1 watchdog/plugin safety fence while routing normal Host
work through the provider-neutral v0.9.2 overlay and destructive lifecycle
through the provider-aware v0.9.2 wrapper.

The PASSTHROUGH boundary restores v0.9.2-owned OpenClaw route/timeout/schema
fields, stops CNX provider event adapters, and forces one verified Gateway
process boundary. A config-file restore alone is not sufficient evidence that
the running Gateway has loaded the native route.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import host_control_v091 as v091
import lifecycle_v092 as lifecycle
import openclaw_route_v092 as openclaw_route
import openclaw_runtime_boundary_v092 as runtime_boundary
import provider_events_v092 as provider_events

HERE = Path(__file__).resolve()
v091.legacy.HOST = HERE.with_name("host_v092.py")
ADAPTER_STOP_VERIFY_SECONDS = 5.0


def option_value(argv: list[str], name: str) -> str | None:
    for index, value in enumerate(argv):
        if value == name and index + 1 < len(argv):
            return argv[index + 1]
        prefix = name + "="
        if value.startswith(prefix):
            return value[len(prefix):]
    return None


def _stop_provider_events_verified(root: Path) -> dict:
    """Synchronize intentional shutdown with actual watcher ownership release.

    This bounded wait is a lifecycle handoff, not recovery authority. Provider
    shutdown is blocked until the LM Studio adapter no longer owns its OS lock,
    preventing a normal provider stop from being observed as `provider_dead`.
    """
    requested = provider_events.stop_adapter(root)
    deadline = time.monotonic() + ADAPTER_STOP_VERIFY_SECONDS
    status = provider_events.adapter_status(root, "lmstudio")
    while status.get("ownershipHeld") is True and time.monotonic() < deadline:
        time.sleep(0.025)
        status = provider_events.adapter_status(root, "lmstudio")

    released = status.get("ownershipHeld") is False and not status.get("running")
    cleanup = None
    if released:
        # A second pass can safely remove stale PID/lock files. Its ownership
        # guard prevents a reused PID from being terminated.
        cleanup = provider_events.stop_adapter(root)
    return {
        "ok": released,
        "requested": requested,
        "finalStatus": status,
        "cleanup": cleanup,
        "verification": "ownership-released" if released else "ownership-not-released",
    }


def _finish_disable_native_boundary(root: Path, delegate_code: int) -> int:
    if delegate_code != 0:
        return delegate_code

    # PASSTHROUGH means CNX must no longer react to provider runtime events even
    # if restoring/reloading native OpenClaw configuration later fails.
    adapter_stop = _stop_provider_events_verified(root)
    if not adapter_stop.get("ok"):
        print(json.dumps({
            "result": "error",
            "phase": "stop-provider-event-adapter",
            "providerEventAdapterStop": adapter_stop,
            "safety": "CogentNexus is PASSTHROUGH, but native route activation is blocked until the provider event adapter releases ownership",
        }, ensure_ascii=False, indent=2))
        return 1

    restored = openclaw_route.restore_native(root)
    if not restored.get("ok"):
        print(json.dumps({
            "result": "error",
            "phase": "restore-native-openclaw-route",
            "routeRestore": restored,
            "providerEventAdapterStop": adapter_stop,
            "safety": "CogentNexus is PASSTHROUGH; destructive cleanup is blocked until the native route is restored",
        }, ensure_ascii=False, indent=2))
        return 1

    boundary = runtime_boundary.activate_current_config()
    if not boundary.get("ok"):
        print(json.dumps({
            "result": "error",
            "phase": "activate-native-openclaw-route",
            "routeRestore": restored,
            "providerEventAdapterStop": adapter_stop,
            "runtimeBoundary": boundary,
            "safety": "CogentNexus is PASSTHROUGH and native config is durable, but Gateway reload/health could not be verified",
        }, ensure_ascii=False, indent=2))
        return 1

    return 0


def main() -> int:
    argv = v091.legacy.sys.argv[1:]
    root = v091.legacy.root_from_argv(argv)
    command, _ = v091.legacy.command_from_argv(argv)
    if command in {"reset", "uninstall"}:
        return lifecycle.main(command, root, option_value(argv, "--provider"))
    if command == "stop":
        # Intentional maintenance must silence provider watchers before the
        # provider is shut down, otherwise a normal stop can look like a crash.
        adapter_stop = _stop_provider_events_verified(root)
        if not adapter_stop.get("ok"):
            print(json.dumps({
                "result": "error",
                "phase": "stop-provider-event-adapter",
                "providerEventAdapterStop": adapter_stop,
                "safety": "provider shutdown was not attempted because the CNX event adapter could not be verified stopped",
            }, ensure_ascii=False, indent=2))
            return 1
        return v091.main()
    if command == "disable":
        return _finish_disable_native_boundary(root, v091.main())
    return v091.main()


if __name__ == "__main__":
    raise SystemExit(main())
