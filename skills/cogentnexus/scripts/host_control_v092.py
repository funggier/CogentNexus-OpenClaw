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
from pathlib import Path

import host_control_v091 as v091
import lifecycle_v092 as lifecycle
import openclaw_route_v092 as openclaw_route
import openclaw_runtime_boundary_v092 as runtime_boundary
import provider_events_v092 as provider_events

HERE = Path(__file__).resolve()
v091.legacy.HOST = HERE.with_name("host_v092.py")


def option_value(argv: list[str], name: str) -> str | None:
    for index, value in enumerate(argv):
        if value == name and index + 1 < len(argv):
            return argv[index + 1]
        prefix = name + "="
        if value.startswith(prefix):
            return value[len(prefix):]
    return None


def _finish_disable_native_boundary(root: Path, delegate_code: int) -> int:
    if delegate_code != 0:
        return delegate_code

    # PASSTHROUGH means CNX must no longer react to provider runtime events even
    # if restoring/reloading native OpenClaw configuration later fails.
    adapter_stop = provider_events.stop_adapter(root)

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
        provider_events.stop_adapter(root)
        return v091.main()
    if command == "disable":
        return _finish_disable_native_boundary(root, v091.main())
    return v091.main()


if __name__ == "__main__":
    raise SystemExit(main())
