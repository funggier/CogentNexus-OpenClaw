#!/usr/bin/env python3
"""Fail when current CogentNexus surfaces drift from the v0.8 baseline."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".py", ".ts", ".json", ".ps1", ".sh", ".yml", ".yaml"}
CURRENT_TOP_LEVEL = {"docs", "skills", "plugins", "scripts", "templates", ".github"}
SKIP_PREFIXES = (
    "docs/releases/",       # immutable historical release descriptions
    "plugins/cogentnexus-rotation/node_modules/",
    ".git/",
)
SKIP_PATHS = {
    "scripts/check_baseline_consistency.py",  # contains the forbidden strings below
}
FORBIDDEN = {
    "mandatory cognitive runtime": "CogentNexus is not a mandatory heavy runtime for every request",
    "Use this entry point for every request": "DIRECT admission must happen before heavy skill loading",
    "Load and apply the `cogentnexus` skill before reasoning": "bootstrap inversion is forbidden",
    "Disabled by default during Phase 0": "Phase 0 defaults are historical",
    "CogentNexus Rotation Controller": "current display name is CogentNexus OpenClaw Bridge",
    "Choose Direct, Verified, or Durable": "current request lanes are DIRECT/LOOKUP/ACTION/STAGED",
}
TEMP_WORKFLOW_PREFIXES = ("patch-", "sync-", "normalize-")


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def current_text_files():
    yield ROOT / "README.md"
    for top in CURRENT_TOP_LEVEL:
        base = ROOT / top
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            rel = relative(path)
            if rel in SKIP_PATHS or rel.startswith(SKIP_PREFIXES):
                continue
            if "/tests/" in f"/{rel}/" or rel.startswith("tests/"):
                continue
            yield path


def main() -> int:
    failures: list[str] = []

    expected = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    package = json.loads((ROOT / "plugins/cogentnexus-rotation/package.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "plugins/cogentnexus-rotation/openclaw.plugin.json").read_text(encoding="utf-8"))
    lock = json.loads((ROOT / "plugins/cogentnexus-rotation/package-lock.json").read_text(encoding="utf-8"))
    for label, actual in (
        ("package.json", package.get("version")),
        ("openclaw.plugin.json", manifest.get("version")),
        ("package-lock.json", lock.get("version")),
        ("package-lock root", lock.get("packages", {}).get("", {}).get("version")),
    ):
        if actual != expected:
            failures.append(f"version mismatch: VERSION={expected} but {label}={actual}")

    if manifest.get("name") != "CogentNexus OpenClaw Bridge":
        failures.append(f"plugin display name drift: {manifest.get('name')!r}")

    source = (ROOT / "plugins/cogentnexus-rotation/src/index.ts").read_text(encoding="utf-8")
    if 'name: "CogentNexus OpenClaw Bridge"' not in source:
        failures.append("src/index.ts does not generate the OpenClaw Bridge display name")
    if "Host-managed continuity" not in source or "Host-managed continuity" not in manifest.get("description", ""):
        failures.append("source/generated plugin descriptions do not share Host-managed continuity terminology")

    root_policy = (ROOT / "templates/AGENTS.cogentnexus.md").read_text(encoding="utf-8")
    skill_policy = (ROOT / "skills/cogentnexus/templates/AGENTS.cogentnexus.md").read_text(encoding="utf-8")
    if root_policy != skill_policy:
        failures.append("root and installed-skill AGENTS policy templates differ")
    lane_index = skill_policy.find("Choose the lightest reliable lane")
    load_index = skill_policy.find("Load the `cogentnexus` skill")
    if lane_index < 0 or load_index < 0 or lane_index > load_index:
        failures.append("managed policy does not select the lane before loading the CogentNexus skill")

    host = (ROOT / "skills/cogentnexus/scripts/host.py").read_text(encoding="utf-8")
    for required in (
        'policy_snapshot_path',
        '"register"',
        '"reset"',
        '"apply"',
        'CogentNexus is disabled (PASSTHROUGH)',
        "promote_interrupted_direct",
    ):
        if required not in host:
            failures.append(f"Host Controller missing baseline contract marker: {required}")

    for installer in (ROOT / "scripts/install.ps1", ROOT / "scripts/install.sh"):
        text = installer.read_text(encoding="utf-8")
        if "policy apply" not in text:
            failures.append(f"{relative(installer)} bypasses Host-owned managed policy")

    for workflow in (ROOT / ".github/workflows").glob("*"):
        if workflow.is_file() and workflow.name.startswith(TEMP_WORKFLOW_PREFIXES):
            failures.append(f"temporary workflow left in baseline: {relative(workflow)}")

    for path in current_text_files():
        text = path.read_text(encoding="utf-8", errors="strict")
        rel = relative(path)
        for phrase, reason in FORBIDDEN.items():
            if phrase in text:
                failures.append(f"legacy phrase in {rel}: {phrase!r} ({reason})")

    for path in (ROOT / "README.md", ROOT / "docs/INSTALL.md", ROOT / "docs/INSTALL.th.md"):
        text = path.read_text(encoding="utf-8")
        stale = re.findall(r"\bv0\.[0-7]\.\d+\b", text)
        if stale:
            failures.append(f"stale pre-v0.8 install/current example in {relative(path)}: {sorted(set(stale))}")

    required_current = (
        ROOT / "docs/BASELINE.md",
        ROOT / "docs/INSTALL.md",
        ROOT / "docs/INSTALL.th.md",
        ROOT / f"docs/releases/v{expected}.md",
        ROOT / "skills/cogentnexus/scripts/host.py",
        ROOT / "skills/cogentnexus/scripts/startup.py",
    )
    for path in required_current:
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            failures.append(f"missing/empty baseline artifact: {relative(path)}")

    if failures:
        print("CogentNexus v0.8 baseline consistency FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"CogentNexus v{expected} baseline consistency: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
