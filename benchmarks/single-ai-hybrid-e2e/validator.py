#!/usr/bin/env python3
"""Independent root gate for the single-AI hybrid E2E benchmark."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any


EXPECTED = {
    "EAST": {"id": "east", "score": 55},
    "WEST": {"id": "west", "score": 65},
    "ISLANDS": {"id": "islands", "score": 90},
}
PATHS = {
    "EAST": Path("candidates/EAST/east.json"),
    "WEST": Path("candidates/WEST/west.json"),
    "ISLANDS": Path("candidates/ISLANDS/islands.json"),
}
REQUIRED_EVENTS = {
    "candidate_created": {"EAST", "WEST", "ISLANDS"},
    "deterministic_gate_passed": {"EAST", "WEST", "ISLANDS", "INTEGRATION"},
    "deterministic_gate_failed": {"WEST"},
    "repair_started": {"WEST"},
    "repair_completed": {"WEST"},
    "review_requested": {"EAST", "WEST", "ISLANDS"},
    "review_verdict_received": {"EAST", "WEST", "ISLANDS"},
    "integration_passed": {"INTEGRATION"},
    "root_gate_passed": {"INTEGRATION"},
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_unit(value: Any) -> str:
    text = str(value).upper()
    return text[2:] if text.startswith("L-") else text


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else Path.cwd()
    errors: list[str] = []

    required_files = [
        Path("manifest.json"),
        Path("config/review-policy.json"),
        Path("contracts/EAST.json"),
        Path("contracts/WEST.json"),
        Path("contracts/ISLANDS.json"),
        Path("contracts/INTEGRATION.json"),
        Path("integration/report.json"),
        Path("events.jsonl"),
        Path("runner.py"),
    ]
    required_files += [Path(f"checkpoints/{unit}.json") for unit in (*EXPECTED, "INTEGRATION")]
    for relative in required_files:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative.as_posix()}")

    for unit, expected in EXPECTED.items():
        path = root / PATHS[unit]
        if not path.is_file():
            errors.append(f"missing candidate: {PATHS[unit].as_posix()}")
            continue
        try:
            actual = load_json(path)
            if actual != expected or type(actual.get("score")) is not int:
                errors.append(f"invalid {unit} candidate: {actual!r}")
        except (OSError, ValueError, AttributeError) as exc:
            errors.append(f"cannot read {unit} candidate: {exc}")

    report_path = root / "integration/report.json"
    if report_path.is_file():
        try:
            report = load_json(report_path)
            expected_report = {"total_leaf_count": 3, "sum_total": 210, "average_value": 70}
            if report != expected_report:
                errors.append(f"invalid integration report: {report!r}")
        except (OSError, ValueError) as exc:
            errors.append(f"cannot read integration report: {exc}")

    evidence_root = root / "evidence"
    for category in ("deterministic", "repairs", "reviews"):
        folder = evidence_root / category
        if not folder.is_dir() or not any(path.is_file() for path in folder.rglob("*")):
            errors.append(f"missing non-empty evidence/{category}/")

    repair_files = list((evidence_root / "repairs").glob("*.json")) if evidence_root.is_dir() else []
    repair_records = []
    for path in repair_files:
        try:
            repair_records.append(load_json(path))
        except (OSError, ValueError) as exc:
            errors.append(f"invalid repair evidence {path.name}: {exc}")
    repair_text = json.dumps(repair_records, sort_keys=True).lower()
    for token in ("before", "after", "east", "islands"):
        if token not in repair_text:
            errors.append(f"repair evidence does not identify {token} state")
    east_hash = sha256(root / PATHS["EAST"]) if (root / PATHS["EAST"]).is_file() else ""
    islands_hash = sha256(root / PATHS["ISLANDS"]) if (root / PATHS["ISLANDS"]).is_file() else ""
    for digest, label in ((east_hash, "EAST"), (islands_hash, "ISLANDS")):
        if digest and repair_text.count(digest) < 2:
            errors.append(f"repair evidence lacks matching before/after SHA-256 for {label}")

    events_path = root / "events.jsonl"
    observed = {name: set() for name in REQUIRED_EVENTS}
    if events_path.is_file():
        previous = 0
        try:
            for line_number, line in enumerate(events_path.read_text(encoding="utf-8").splitlines(), 1):
                event = json.loads(line)
                sequence = event.get("sequence")
                if type(sequence) is not int or sequence <= previous:
                    errors.append(f"events.jsonl:{line_number}: sequence is not strictly increasing")
                previous = sequence if type(sequence) is int else previous
                if not event.get("timestamp"):
                    errors.append(f"events.jsonl:{line_number}: missing timestamp")
                name = event.get("event")
                if name in observed:
                    observed[name].add(normalize_unit(event.get("unit_id")))
        except (OSError, ValueError) as exc:
            errors.append(f"invalid events.jsonl: {exc}")
    for name, units in REQUIRED_EVENTS.items():
        missing = units - observed[name]
        if missing:
            errors.append(f"event {name} missing units: {', '.join(sorted(missing))}")

    for unit in (*EXPECTED, "INTEGRATION"):
        checkpoint = root / "checkpoints" / f"{unit}.json"
        if checkpoint.is_file():
            try:
                text = json.dumps(load_json(checkpoint)).upper()
                if "PASS" not in text and "SUCCESS" not in text:
                    errors.append(f"checkpoint {unit} does not record PASS/SUCCESS")
            except (OSError, ValueError) as exc:
                errors.append(f"invalid checkpoint {unit}: {exc}")

    if errors:
        print("ROOT GATE: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("ROOT GATE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

