#!/usr/bin/env python3
"""Read-only evidence checker for the v0.9.5 idle-quiescence contract."""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

UTC = timezone.utc
IDLE_REASON = "idle/no-actionable-work"


@dataclass(frozen=True)
class Evidence:
    heavy_supervisor_calls: int = 0
    provider_recovery_actions: int = 0
    config_mutations: int = 0
    gateway_lifecycle_actions: int = 0
    idle_ticks: int = 0
    records: int = 0
    parse_errors: int = 0


def _parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def _record_time(record: dict[str, Any]) -> datetime | None:
    for key in ("timestamp", "time", "createdAt", "updatedAt", "startedAt", "endedAt"):
        value = record.get(key)
        if isinstance(value, str):
            parsed = _parse_time(value)
            if parsed is not None:
                return parsed
    return None


def _flatten_text(record: dict[str, Any]) -> str:
    return json.dumps(record, ensure_ascii=False, sort_keys=True).lower()


def _is_idle(record: dict[str, Any]) -> bool:
    return record.get("result") == "idle" and (
        record.get("wakeReason") == IDLE_REASON or record.get("action") == "none"
    )


def _is_heavy(record: dict[str, Any]) -> bool:
    if record.get("heavyPath") is True:
        return True
    result = str(record.get("result", "")).lower()
    action = str(record.get("action", "")).lower()
    return result in {"recovery", "maintenance"} or action in {
        "delivery",
        "direct-recovery",
        "provider-recovery",
        "session",
        "ticket",
        "gateway-recovery",
    }


def _is_provider_recovery(record: dict[str, Any], text: str) -> bool:
    if record.get("providerRecovery") not in (None, False, {}, []):
        return True
    authority = str(record.get("wakeAuthority", "")).lower()
    action = str(record.get("action", "")).lower()
    return authority == "provider_local" or action in {"provider-recovery", "provider-start", "provider-restart"} or "provider recovery" in text


def _is_config_mutation(record: dict[str, Any], text: str) -> bool:
    mutation = record.get("configMutation")
    if mutation not in (None, False, {}, []):
        return True
    event = str(record.get("event", record.get("eventType", ""))).lower()
    return bool(re.search(r"config(?:uration)?[_ -](?:set|write|update|mutation)|config mutation", event + " " + text))


def _is_gateway_lifecycle(record: dict[str, Any], text: str) -> bool:
    lifecycle = record.get("gatewayLifecycle")
    if lifecycle not in (None, False, {}, []):
        return True
    action = str(record.get("action", "")).lower()
    return action in {"gateway-start", "gateway-stop", "gateway-restart", "gateway-recovery"} or bool(
        re.search(r"gateway[_ -](?:start|stop|restart|recover)|gateway lifecycle", text)
    )


def read_records(path: Path, since: datetime | None = None, until: datetime | None = None) -> tuple[list[dict[str, Any]], int]:
    if not path.is_file():
        return [], 0
    parse_errors = 0
    records: list[dict[str, Any]] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            parse_errors += 1
            continue
        if not isinstance(value, dict):
            parse_errors += 1
            continue
        stamp = _record_time(value)
        if since is not None and stamp is not None and stamp < since:
            continue
        if until is not None and stamp is not None and stamp > until:
            continue
        records.append(value)
    return records, parse_errors


def inspect(root: Path, log_path: Path, since: datetime | None = None, until: datetime | None = None) -> dict[str, Any]:
    records, parse_errors = read_records(log_path, since=since, until=until)
    state_paths = [root / "host" / "controller.json", root / "host-state.json"]
    state_present = any(path.is_file() for path in state_paths)

    evidence = Evidence(records=len(records), parse_errors=parse_errors)
    counts = evidence.__dict__.copy()
    for record in records:
        text = _flatten_text(record)
        if _is_idle(record):
            counts["idle_ticks"] += 1
        if _is_heavy(record):
            counts["heavy_supervisor_calls"] += 1
        if _is_provider_recovery(record, text):
            counts["provider_recovery_actions"] += 1
        if _is_config_mutation(record, text):
            counts["config_mutations"] += 1
        if _is_gateway_lifecycle(record, text):
            counts["gateway_lifecycle_actions"] += 1

    if not records:
        verdict = "INDETERMINATE"
        reason = "no parseable evidence records in observation window"
    elif counts["parse_errors"] and counts["parse_errors"] >= counts["records"]:
        verdict = "INDETERMINATE"
        reason = "observation input contains no usable structured evidence"
    elif counts["idle_ticks"] == 0:
        verdict = "INDETERMINATE"
        reason = "observation window contains no confirmed idle Supervisor tick"
    else:
        verdict = "PASS"
        reason = "bounded observation evidence is sufficient"

    return {
        "verdict": verdict,
        "heavySupervisorCalls": counts["heavy_supervisor_calls"],
        "providerRecoveryActions": counts["provider_recovery_actions"],
        "configMutations": counts["config_mutations"],
        "gatewayLifecycleActions": counts["gateway_lifecycle_actions"],
        "idleTicks": counts["idle_ticks"],
        "observationRecords": counts["records"],
        "parseErrors": counts["parse_errors"],
        "stateEvidencePresent": state_present,
        "readOnly": True,
        "reason": reason,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--log", required=True, type=Path)
    parser.add_argument("--since")
    parser.add_argument("--until")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output = inspect(args.root.resolve(), args.log.resolve(), _parse_time(args.since), _parse_time(args.until))
    print(json.dumps(output, ensure_ascii=False, indent=2) if args.json else json.dumps(output, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
