#!/usr/bin/env python3
"""Independent root gate for the single-AI hybrid E2E benchmark."""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime
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


def require_reference(root: Path, value: Any, label: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value or Path(value).is_absolute() or ".." in Path(value).parts:
        errors.append(f"{label} is not a safe relative evidence path")
    elif not (root / value).is_file():
        errors.append(f"{label} does not exist: {value}")


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

    manifest_path = root / "manifest.json"
    if manifest_path.is_file():
        try:
            manifest = load_json(manifest_path)
            expected_units = ["EAST", "WEST", "ISLANDS", "INTEGRATION"]
            if not isinstance(manifest.get("model"), str) or not manifest["model"].strip():
                errors.append("manifest model must be a non-empty string")
            if manifest.get("review_mode") != "single-reviewer":
                errors.append("manifest review_mode must be single-reviewer")
            if manifest.get("units") != expected_units:
                errors.append(f"manifest units must equal {expected_units!r}")
            if manifest.get("deterministic_gates") is not True:
                errors.append("manifest must require deterministic_gates")
            if manifest.get("max_repairs_per_unit") != 3:
                errors.append("manifest max_repairs_per_unit must equal 3")
        except (OSError, ValueError, AttributeError, TypeError) as exc:
            errors.append(f"invalid manifest.json: {exc}")

    policy_path = root / "config/review-policy.json"
    if policy_path.is_file():
        try:
            policy = load_json(policy_path)
            if policy.get("mode") != "single-reviewer":
                errors.append("review policy mode must be single-reviewer")
            if policy.get("deterministic_gates_required") is not True:
                errors.append("review policy must require deterministic gates")
        except (OSError, ValueError, AttributeError) as exc:
            errors.append(f"invalid review policy: {exc}")

    contract_outputs = {**{unit: path.as_posix() for unit, path in PATHS.items()}, "INTEGRATION": "integration/report.json"}
    for unit, output in contract_outputs.items():
        contract_path = root / "contracts" / f"{unit}.json"
        if not contract_path.is_file():
            continue
        try:
            contract = load_json(contract_path)
            if not isinstance(contract.get("objective"), str) or not contract["objective"].strip():
                errors.append(f"contract {unit} lacks objective")
            if contract.get("output_path") != output:
                errors.append(f"contract {unit} output_path must be {output}")
            if not isinstance(contract.get("allowed_write_scope"), list) or output not in contract["allowed_write_scope"]:
                errors.append(f"contract {unit} allowed_write_scope must contain {output}")
            for field in ("acceptance_criteria", "deterministic_validation_rules"):
                if not isinstance(contract.get(field), list) or not contract[field]:
                    errors.append(f"contract {unit} requires non-empty {field}")
        except (OSError, ValueError, AttributeError, TypeError) as exc:
            errors.append(f"invalid contract {unit}: {exc}")

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

    artifact_paths = {**PATHS, "INTEGRATION": Path("integration/report.json")}
    for unit, artifact_relative in artifact_paths.items():
        evidence_path = evidence_root / "deterministic" / f"{unit}.json"
        if not evidence_path.is_file():
            errors.append(f"missing deterministic PASS evidence for {unit}")
            continue
        try:
            evidence = load_json(evidence_path)
            if normalize_unit(evidence.get("unit_id")) != unit or evidence.get("status") != "PASS":
                errors.append(f"invalid deterministic PASS evidence for {unit}")
            artifact = root / artifact_relative
            if artifact.is_file() and evidence.get("artifact_sha256") != sha256(artifact):
                errors.append(f"deterministic evidence hash mismatch for {unit}")
        except (OSError, ValueError, AttributeError) as exc:
            errors.append(f"invalid deterministic evidence for {unit}: {exc}")

    failure_path = evidence_root / "deterministic" / "WEST-initial-failure.json"
    if not failure_path.is_file():
        errors.append("missing WEST initial deterministic failure evidence")
    else:
        try:
            failure = load_json(failure_path)
            if normalize_unit(failure.get("unit_id")) != "WEST" or failure.get("status") != "FAIL" or not isinstance(failure.get("errors"), list) or not failure["errors"]:
                errors.append("invalid WEST initial deterministic failure evidence")
        except (OSError, ValueError, AttributeError, TypeError) as exc:
            errors.append(f"invalid WEST initial failure evidence: {exc}")

    for unit in EXPECTED:
        review_path = evidence_root / "reviews" / f"{unit}.json"
        if not review_path.is_file():
            errors.append(f"missing reviewer verdict for {unit}")
            continue
        try:
            review = load_json(review_path)
            if normalize_unit(review.get("unit_id")) != unit or review.get("verdict") != "PASS":
                errors.append(f"invalid reviewer PASS verdict for {unit}")
            require_reference(root, review.get("deterministic_evidence"), f"review {unit} deterministic_evidence", errors)
        except (OSError, ValueError, AttributeError) as exc:
            errors.append(f"invalid reviewer verdict for {unit}: {exc}")

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

    west_repair = evidence_root / "repairs" / "WEST.json"
    if west_repair.is_file():
        try:
            repair = load_json(west_repair)
            if normalize_unit(repair.get("unit_id")) != "WEST":
                errors.append("WEST repair evidence has wrong unit_id")
            if not repair.get("before_hash") or repair.get("before_hash") == repair.get("after_hash"):
                errors.append("WEST repair before_hash and after_hash must differ")
            if (root / PATHS["WEST"]).is_file() and repair.get("after_hash") != sha256(root / PATHS["WEST"]):
                errors.append("WEST repair after_hash does not match accepted candidate")
            before = repair.get("sibling_hashes_before")
            after = repair.get("sibling_hashes_after")
            if not isinstance(before, dict) or not isinstance(after, dict) or any(before.get(u) != after.get(u) for u in ("EAST", "ISLANDS")):
                errors.append("WEST repair did not preserve EAST and ISLANDS sibling hashes")
        except (OSError, ValueError, AttributeError) as exc:
            errors.append(f"invalid WEST repair evidence: {exc}")

    events_path = root / "events.jsonl"
    observed = {name: set() for name in REQUIRED_EVENTS}
    if events_path.is_file():
        previous = 0
        positions: dict[tuple[str, str], int] = {}
        try:
            for line_number, line in enumerate(events_path.read_text(encoding="utf-8").splitlines(), 1):
                event = json.loads(line)
                sequence = event.get("sequence")
                if type(sequence) is not int or sequence <= previous:
                    errors.append(f"events.jsonl:{line_number}: sequence is not strictly increasing")
                previous = sequence if type(sequence) is int else previous
                timestamp = event.get("timestamp")
                if not isinstance(timestamp, str):
                    errors.append(f"events.jsonl:{line_number}: missing timestamp")
                else:
                    try:
                        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                    except ValueError:
                        errors.append(f"events.jsonl:{line_number}: timestamp is not ISO-8601")
                name = event.get("event")
                if name in observed:
                    unit = normalize_unit(event.get("unit_id"))
                    observed[name].add(unit)
                    positions.setdefault((name, unit), line_number)
        except (OSError, ValueError) as exc:
            errors.append(f"invalid events.jsonl: {exc}")
    for name, units in REQUIRED_EVENTS.items():
        missing = units - observed[name]
        if missing:
            errors.append(f"event {name} missing units: {', '.join(sorted(missing))}")
    if events_path.is_file() and "positions" in locals():
        order_rules = [
            (("candidate_created", "WEST"), ("deterministic_gate_failed", "WEST")),
            (("deterministic_gate_failed", "WEST"), ("repair_started", "WEST")),
            (("repair_started", "WEST"), ("repair_completed", "WEST")),
            (("repair_completed", "WEST"), ("deterministic_gate_passed", "WEST")),
            (("deterministic_gate_passed", "INTEGRATION"), ("integration_passed", "INTEGRATION")),
            (("integration_passed", "INTEGRATION"), ("root_gate_passed", "INTEGRATION")),
        ]
        for unit in EXPECTED:
            order_rules.extend([
                (("candidate_created", unit), ("deterministic_gate_passed", unit)),
                (("deterministic_gate_passed", unit), ("review_requested", unit)),
                (("review_requested", unit), ("review_verdict_received", unit)),
            ])
        for before, after in order_rules:
            if before in positions and after in positions and positions[before] >= positions[after]:
                errors.append(f"event order invalid: {before[0]}/{before[1]} must precede {after[0]}/{after[1]}")

    for unit in (*EXPECTED, "INTEGRATION"):
        checkpoint = root / "checkpoints" / f"{unit}.json"
        if checkpoint.is_file():
            try:
                value = load_json(checkpoint)
                if normalize_unit(value.get("unit_id")) != unit:
                    errors.append(f"checkpoint {unit} has wrong unit_id")
                expected_field, expected_status = ("root_status", "SUCCESS") if unit == "INTEGRATION" else ("status", "ACCEPTED")
                if value.get(expected_field) != expected_status:
                    errors.append(f"checkpoint {unit} must record {expected_field}={expected_status}")
                refs = value.get("evidence")
                if not isinstance(refs, list) or not refs:
                    errors.append(f"checkpoint {unit} requires evidence references")
                else:
                    for index, reference in enumerate(refs):
                        require_reference(root, reference, f"checkpoint {unit} evidence[{index}]", errors)
            except (OSError, ValueError, AttributeError) as exc:
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
