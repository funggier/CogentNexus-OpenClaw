#!/usr/bin/env python3
"""Positive and tamper tests for the independent benchmark root gate."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validator.py"
UNITS = {"EAST": ("east", 55), "WEST": ("west", 65), "ISLANDS": ("islands", 90)}


def write_json(root: Path, relative: str, value: object) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, separators=(",", ":")), encoding="utf-8")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_valid(root: Path) -> None:
    write_json(root, "manifest.json", {"model": "self-test", "review_mode": "single-reviewer", "units": ["EAST", "WEST", "ISLANDS", "INTEGRATION"], "deterministic_gates": True, "max_repairs_per_unit": 3})
    write_json(root, "config/review-policy.json", {"mode": "single-reviewer", "deterministic_gates_required": True})
    paths = {u: f"candidates/{u}/{name}.json" for u, (name, _) in UNITS.items()}
    paths["INTEGRATION"] = "integration/report.json"
    for unit, output in paths.items():
        write_json(root, f"contracts/{unit}.json", {"objective": f"produce {unit}", "output_path": output, "allowed_write_scope": [output], "acceptance_criteria": ["exact output"], "deterministic_validation_rules": ["schema and values"]})
    for unit, (name, score) in UNITS.items():
        write_json(root, paths[unit], {"id": name, "score": score})
    write_json(root, "integration/report.json", {"total_leaf_count": 3, "sum_total": 210, "average_value": 70})
    hashes = {u: digest(root / paths[u]) for u in UNITS}
    for unit in (*UNITS, "INTEGRATION"):
        artifact = root / paths[unit]
        evidence = f"evidence/deterministic/{unit}.json"
        write_json(root, evidence, {"unit_id": unit, "status": "PASS", "artifact_sha256": digest(artifact)})
        if unit != "INTEGRATION":
            write_json(root, f"evidence/reviews/{unit}.json", {"unit_id": unit, "verdict": "PASS", "deterministic_evidence": evidence})
            write_json(root, f"checkpoints/{unit}.json", {"unit_id": unit, "status": "ACCEPTED", "evidence": [evidence]})
    write_json(root, "evidence/deterministic/WEST-initial-failure.json", {"unit_id": "WEST", "status": "FAIL", "errors": ["score must be integer"]})
    write_json(root, "evidence/repairs/WEST.json", {"unit_id": "WEST", "before_hash": "0" * 64, "after_hash": hashes["WEST"], "sibling_hashes_before": {"EAST": hashes["EAST"], "ISLANDS": hashes["ISLANDS"]}, "sibling_hashes_after": {"EAST": hashes["EAST"], "ISLANDS": hashes["ISLANDS"]}})
    write_json(root, "checkpoints/INTEGRATION.json", {"unit_id": "INTEGRATION", "root_status": "SUCCESS", "evidence": ["evidence/deterministic/INTEGRATION.json"]})
    events = []
    def event(name: str, unit: str) -> None:
        events.append({"sequence": len(events) + 1, "timestamp": f"2026-08-13T12:{len(events):02d}:00Z", "event": name, "unit_id": unit})
    for unit in ("EAST", "ISLANDS"):
        event("candidate_created", unit); event("deterministic_gate_passed", unit); event("review_requested", unit); event("review_verdict_received", unit)
    event("candidate_created", "WEST"); event("deterministic_gate_failed", "WEST"); event("repair_started", "WEST"); event("repair_completed", "WEST"); event("deterministic_gate_passed", "WEST"); event("review_requested", "WEST"); event("review_verdict_received", "WEST")
    event("deterministic_gate_passed", "INTEGRATION"); event("integration_passed", "INTEGRATION"); event("root_gate_passed", "INTEGRATION")
    (root / "events.jsonl").write_text("\n".join(json.dumps(row) for row in events) + "\n", encoding="utf-8")
    (root / "runner.py").write_text("# reproducible runner supplied by benchmark self-test\n", encoding="utf-8")


def run_validator(root: Path) -> int:
    return subprocess.run([sys.executable, str(VALIDATOR), str(root)], check=False).returncode


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="cnx-benchmark-") as folder:
        root = Path(folder)
        make_valid(root)
        if run_validator(root) != 0:
            print("validator self-test: expected valid fixture to pass", file=sys.stderr)
            return 1
        write_json(root, "candidates/EAST/east.json", {"id": "east", "score": "55"})
        if run_validator(root) == 0:
            print("validator self-test: expected tampered fixture to fail", file=sys.stderr)
            return 1
    print("Benchmark validator self-test: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
