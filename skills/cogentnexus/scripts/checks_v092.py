#!/usr/bin/env python3
"""v0.9.2 read-only checks with prospective route and event-recovery semantics."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import checks as base
import openclaw_route_v092 as route
import provider
import provider_events_v092 as provider_events
import provider_recovery_v092 as recovery_policy

VERDICT_EXIT = base.VERDICT_EXIT
item = base.item
render = base.render
preflight_start = base.preflight_start


def _controller(root: Path) -> dict[str, Any]:
    path = root / "host" / "controller.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except Exception:
        return {}


def check_model(root: Path, override: str | None = None) -> list[dict[str, Any]]:
    target, results = base.resolve_provider(root, override)

    if override and target:
        planned = route.plan(root, target)
        if not planned.get("ok"):
            results.append(item(
                "OpenClaw prospective model route",
                "FAIL",
                f"No usable OpenClaw route is resolvable for prospective provider '{target}'",
                provider=target,
                evidence=planned,
                mutatesState=False,
            ))
        else:
            results.append(item(
                "OpenClaw prospective model route",
                "PASS",
                f"Provider '{target}' can use {planned.get('model')}",
                provider=target,
                prospectiveModel=planned.get("model"),
                currentModel=planned.get("currentModel"),
                currentProvider=planned.get("currentProvider"),
                mutatesState=False,
            ))
    else:
        status = provider.openclaw_model_status()
        if not status.get("ok"):
            results.append(item(
                "OpenClaw model routing",
                "INDETERMINATE",
                "Could not read OpenClaw model status",
                evidence=status,
            ))
            return results
        model_ref = status.get("defaultModel")
        routed = provider.model_provider(model_ref)
        if not model_ref:
            results.append(item(
                "OpenClaw model routing",
                "WARN",
                "OpenClaw default model could not be resolved from model status",
            ))
        elif target and routed and routed != target:
            results.append(item(
                "OpenClaw model routing",
                "FAIL",
                f"OpenClaw default model routes to '{routed}' while selected provider is '{target}'",
                defaultModel=model_ref,
                provider=target,
            ))
        else:
            results.append(item(
                "OpenClaw model routing",
                "PASS",
                f"OpenClaw default model: {model_ref}",
                defaultModel=model_ref,
                modelProvider=routed,
                provider=target,
            ))

    if target:
        p = provider.probe(target, timeout=3.0)
        if p["healthy"] and p["modelCount"] > 0:
            results.append(item(
                "Provider model catalog",
                "PASS",
                f"{target} exposes {p['modelCount']} model(s)",
                models=p["models"][:20],
            ))
        elif p["healthy"]:
            results.append(item(
                "Provider model catalog",
                "WARN",
                f"{target} is reachable but currently exposes no models",
                provider=target,
            ))
        else:
            results.append(item(
                "Provider model catalog",
                "WARN",
                f"{target} is not running, so model availability cannot be verified",
                provider=target,
            ))
    return results


def check_recovery(root: Path) -> list[dict[str, Any]]:
    results = list(base.check_recovery(root))
    controller = _controller(root)
    selected = controller.get("selectedProvider")
    if not selected:
        results.append(item(
            "Provider recovery incident",
            "PASS",
            "No selected provider; no provider recovery incident has authority",
            incidentOpen=False,
        ))
        return results

    try:
        selected = provider.normalize_provider(str(selected))
        gate = recovery_policy.gate(root, selected)
        if gate.get("circuitOpen"):
            status = "WARN"
            summary = f"{selected} recovery circuit is open for incident {gate.get('incidentId')}"
        elif gate.get("incidentOpen"):
            status = "WARN"
            summary = f"{selected} has an active provider incident with bounded recovery authority"
        else:
            status = "PASS"
            summary = f"{selected} has no active provider recovery incident"
        results.append(item(
            "Provider recovery incident",
            status,
            summary,
            **gate,
        ))
    except Exception as exc:
        results.append(item(
            "Provider recovery incident",
            "INDETERMINATE",
            f"Provider incident state could not be inspected: {exc}",
        ))

    mode = controller.get("mode")
    desired = controller.get("desiredProvider")
    if selected == "lmstudio":
        adapter = provider_events.adapter_status(root, selected)
        expected = mode == "managed" and desired == "running"
        if expected and adapter.get("running"):
            status = "PASS"
            summary = "LM Studio blocking provider-event adapter is running"
        elif expected:
            status = "WARN"
            summary = "LM Studio is selected/running but its provider-event adapter is not running; reconciliation fallback remains available"
        else:
            status = "PASS"
            summary = "LM Studio provider-event adapter is not required in the current controller state"
        results.append(item(
            "Provider event adapter",
            status,
            summary,
            expected=expected,
            **adapter,
        ))
    else:
        results.append(item(
            "Provider event adapter",
            "PASS",
            "Selected provider does not require the LM Studio runtime progress adapter",
            provider=selected,
            expected=False,
        ))
    return results


def system_check(root: Path, provider_override: str | None = None) -> dict[str, Any]:
    root = root.resolve()
    entries: list[dict[str, Any]] = []
    entries.extend(base.check_cogentnexus(root))
    entries.extend(base.check_config(root))
    entries.extend(base.check_openclaw())
    entries.extend(base.check_provider(root, provider_override, include_inventory=True))
    entries.extend(check_model(root, provider_override))
    entries.extend(base.check_gateway())
    entries.extend(base.check_storage(root))
    entries.extend(check_recovery(root))
    entries.extend(base.check_delivery(root))
    entries.extend(base.check_resources(root))
    verdict = base.aggregate(entries)
    return {
        "check": "system",
        "providerOverride": provider_override,
        "verdict": verdict,
        "exitCode": VERDICT_EXIT[verdict],
        "checks": entries,
        "readOnly": True,
        "stateChanged": False,
    }


def component_check(root: Path, component: str, provider_override: str | None = None) -> dict[str, Any]:
    root = root.resolve()
    if component == "model":
        entries = check_model(root, provider_override)
    elif component == "recovery":
        entries = check_recovery(root)
    else:
        return base.component_check(root, component, provider_override)
    verdict = base.aggregate(entries)
    return {
        "check": component,
        "providerOverride": provider_override,
        "verdict": verdict,
        "exitCode": VERDICT_EXIT[verdict],
        "checks": entries,
        "readOnly": True,
        "stateChanged": False,
    }
