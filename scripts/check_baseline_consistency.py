#!/usr/bin/env python3
"""Fail when current CogentNexus-OpenClaw surfaces drift from the accepted baseline."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "0.9.3"
TEXT_SUFFIXES = {".md", ".py", ".ts", ".json", ".ps1", ".sh", ".yml", ".yaml"}
CURRENT_TOP_LEVEL = {"docs", "skills", "plugins", "scripts", "templates", ".github"}
SKIP_PREFIXES = (
    "docs/releases/",
    "plugins/cogentnexus-openclaw/node_modules/",
    ".git/",
)
SKIP_PATHS = {"scripts/check_baseline_consistency.py"}
CURRENT_OPERATOR_DOCS = (
    "README.md",
    "docs/CURRENT_STATE.md",
    "docs/INSTALL.md",
    "docs/INSTALL.th.md",
    "docs/PROVIDERS.md",
    "docs/CHECK_SYSTEM.md",
    "skills/cogentnexus-openclaw/SKILL.md",
    "plugins/cogentnexus-openclaw/README.md",
)
CURRENT_LMSTUDIO_COMMAND = re.compile(r"(?:--provider|-provider)(?:\s+|=)lmstudio\b", re.IGNORECASE)
LEGACY_GENERIC_LAUNCHER = re.compile("cnx" + r"\.cmd\b", re.IGNORECASE)
FORBIDDEN = {
    "mandatory cognitive runtime": "CogentNexus-OpenClaw is not a mandatory heavy runtime for every request",
    "Use this entry point for every request": "DIRECT admission must happen before heavy skill loading",
    "Load and apply the `cogentnexus-openclaw` skill before reasoning": "bootstrap inversion is forbidden",
    "Disabled by default during Phase 0": "Phase 0 defaults are historical",
    "CogentNexus-OpenClaw Rotation Controller": "current display name is CogentNexus-OpenClaw Bridge",
    "Choose Direct, Verified, or Durable": "current request lanes are DIRECT/LOOKUP/ACTION/STAGED",
}
TEMP_WORKFLOW_PREFIXES = ("patch-", "sync-", "normalize-", "update-delivery-")


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

    core_version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    package = json.loads((ROOT / "plugins/cogentnexus-openclaw/package.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "plugins/cogentnexus-openclaw/openclaw.plugin.json").read_text(encoding="utf-8"))
    lock = json.loads((ROOT / "plugins/cogentnexus-openclaw/package-lock.json").read_text(encoding="utf-8"))

    # The v0.9.3 candidate is one versioned unit. Every package metadata surface
    # must agree with the root VERSION rather than validating an older bridge
    # payload as an independently versioned release.
    if core_version != EXPECTED_VERSION:
        failures.append(f"current candidate VERSION must be {EXPECTED_VERSION}, got {core_version!r}")
    version_surfaces = (
        ("package.json", package.get("version")),
        ("openclaw.plugin.json", manifest.get("version")),
        ("package-lock.json", lock.get("version")),
        ("package-lock root", lock.get("packages", {}).get("", {}).get("version")),
    )
    for label, actual in version_surfaces:
        if actual != core_version:
            failures.append(f"current version mismatch: VERSION={core_version} but {label}={actual}")

    bridge_version = package.get("version")
    if package.get("name") != "openclaw-plugin-cogentnexus-openclaw":
        failures.append(f"plugin package namespace drift: {package.get('name')!r}")
    if manifest.get("name") != "CogentNexus-OpenClaw Bridge":
        failures.append(f"plugin display name drift: {manifest.get('name')!r}")

    source = (ROOT / "plugins/cogentnexus-openclaw/src/index.ts").read_text(encoding="utf-8")
    if 'name: "CogentNexus-OpenClaw Bridge"' not in source:
        failures.append("src/index.ts does not generate the OpenClaw Bridge display name")
    if "Host-managed continuity" not in source or "Host-managed continuity" not in manifest.get("description", ""):
        failures.append("source/generated plugin descriptions do not share Host-managed continuity terminology")

    provider_v093 = (ROOT / "skills/cogentnexus-openclaw/scripts/provider_v093.py").read_text(encoding="utf-8")
    ollama_only = re.search(
        r"(?m)^SUPPORTED_PROVIDERS\s*=\s*\(\s*['\"]ollama['\"]\s*,?\s*\)\s*$",
        provider_v093,
    )
    if not ollama_only:
        failures.append("v0.9.3 provider facade is not Ollama-only")

    release_entry = (ROOT / "plugins/cogentnexus-openclaw/src/v091-release-entry.ts").read_text(encoding="utf-8")
    if not re.search(r'id\s*:\s*["\']cogentnexus-openclaw["\']', release_entry):
        failures.append("release entry plugin id is not namespace-isolated")
    if not re.search(r"installV091DashboardVerifiedDelivery\s*\(\s*api\s*,\s*config\s*\)\s*;", release_entry):
        failures.append("release entry no longer registers Dashboard verified delivery")

    ticket_source = (ROOT / "plugins/cogentnexus-openclaw/src/ticket-store.ts").read_text(encoding="utf-8")
    delivery_source = (ROOT / "plugins/cogentnexus-openclaw/src/delivery-continuity.ts").read_text(encoding="utf-8")
    continuity_markers = {
        "index.ts": (
            'api.on("reply_dispatch"', "waitForIdle", 'api.on("message_sent"', 'api.on("after_compaction"',
            "schedulePostCompactionResume", "recoverUndeliveredDirect", "[CogentNexus-OpenClaw Continuation: post-compaction]",
        ),
        "ticket-store.ts": (
            "response_ready_at", "delivery_confirmed_at", "delivery_last_error", "confirmDirectDelivery",
            "failDirectDelivery", "recoverUndeliveredDirect",
        ),
        "delivery-continuity.ts": (
            "ticketDeliveryMarker", "workflowDeliveryMarker", "settleDeliveryTarget", "hasPendingSessionWork",
        ),
    }
    continuity_text = {"index.ts": source, "ticket-store.ts": ticket_source, "delivery-continuity.ts": delivery_source}
    for label, markers in continuity_markers.items():
        for marker in markers:
            if marker not in continuity_text[label]:
                failures.append(f"{label} missing delivery/compaction continuity marker: {marker}")

    root_policy = (ROOT / "templates/AGENTS.cogentnexus-openclaw.md").read_text(encoding="utf-8")
    skill_policy = (ROOT / "skills/cogentnexus-openclaw/templates/AGENTS.cogentnexus-openclaw.md").read_text(encoding="utf-8")
    if root_policy != skill_policy:
        failures.append("root and installed-skill AGENTS policy templates differ")
    lane_index = skill_policy.find("Choose the lightest reliable lane")
    load_index = skill_policy.find("Load the `cogentnexus-openclaw` skill")
    if lane_index < 0 or load_index < 0 or lane_index > load_index:
        failures.append("managed policy does not select the lane before loading the CogentNexus-OpenClaw skill")

    host = (ROOT / "skills/cogentnexus-openclaw/scripts/host.py").read_text(encoding="utf-8")
    for required in (
        'policy_snapshot_path', '"register"', '"reset"', '"apply"', 'CogentNexus-OpenClaw is disabled (PASSTHROUGH)',
        "promote_interrupted_direct", "hooks.allowConversationAccess",
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

    for rel in CURRENT_OPERATOR_DOCS:
        path = ROOT / rel
        if not path.is_file():
            failures.append(f"missing current operator document: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        if CURRENT_LMSTUDIO_COMMAND.search(text):
            failures.append(f"current LM Studio provider command in {rel}")
        if LEGACY_GENERIC_LAUNCHER.search(text):
            failures.append(f"legacy generic launcher command in {rel}")

    for path in (ROOT / "README.md", ROOT / "docs/INSTALL.md", ROOT / "docs/INSTALL.th.md"):
        text = path.read_text(encoding="utf-8")
        stale = re.findall(r"\bv0\.[0-7]\.\d+\b", text)
        if stale:
            failures.append(f"stale pre-v0.8 install/current example in {relative(path)}: {sorted(set(stale))}")

    required_current = (
        ROOT / "docs/BASELINE.md", ROOT / "docs/INSTALL.md", ROOT / "docs/INSTALL.th.md",
        ROOT / f"docs/releases/v{core_version}.md", ROOT / "skills/cogentnexus-openclaw/SKILL.md",
        ROOT / "skills/cogentnexus-openclaw/scripts/cnxclaw.py", ROOT / "skills/cogentnexus-openclaw/scripts/host.py",
        ROOT / "skills/cogentnexus-openclaw/scripts/startup.py", ROOT / "skills/cogentnexus-openclaw/scripts/provider_v093.py",
        ROOT / "plugins/cogentnexus-openclaw/src/delivery-continuity.ts",
        ROOT / "plugins/cogentnexus-openclaw/src/v091-release-entry.ts",
    )
    for path in required_current:
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            failures.append(f"missing/empty baseline artifact: {relative(path)}")

    if failures:
        print("CogentNexus-OpenClaw baseline consistency FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"CogentNexus-OpenClaw v{core_version} baseline consistency: PASS (Bridge v{bridge_version})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
