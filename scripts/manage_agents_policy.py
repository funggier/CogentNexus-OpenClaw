#!/usr/bin/env python3
"""Safely install or update the CogentNexus managed AGENTS.md block."""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime, timezone
from pathlib import Path

BEGIN = "<!-- cogentnexus:begin -->"
END = "<!-- cogentnexus:end -->"


def render(policy: str) -> str:
    return f"{BEGIN}\n{policy.strip()}\n{END}"


def merge(existing: str, policy: str) -> tuple[str, bool]:
    block = render(policy)
    start = existing.find(BEGIN)
    finish = existing.find(END)
    if (start < 0) != (finish < 0) or (start >= 0 and finish < start):
        raise ValueError("AGENTS.md contains an incomplete CogentNexus managed block")
    if start >= 0:
        finish += len(END)
        updated = existing[:start] + block + existing[finish:]
    else:
        separator = "\n\n" if existing.strip() else ""
        updated = existing.rstrip() + separator + block + "\n"
    if not updated.endswith("\n"):
        updated += "\n"
    return updated, updated != existing


def install(workspace: Path, policy_path: Path, backup_root: Path | None) -> dict[str, str | bool | None]:
    workspace = workspace.resolve()
    agents = workspace / "AGENTS.md"
    policy = policy_path.read_text(encoding="utf-8")
    existing = agents.read_text(encoding="utf-8") if agents.exists() else ""
    updated, changed = merge(existing, policy)
    backup = None
    if changed and agents.exists():
        root = (backup_root or workspace / ".cogent" / "install-backups").resolve()
        root.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup = root / f"AGENTS.pre-cogentnexus-{stamp}.md"
        shutil.copy2(agents, backup)
    if changed:
        workspace.mkdir(parents=True, exist_ok=True)
        temporary = agents.with_suffix(".md.tmp")
        temporary.write_text(updated, encoding="utf-8", newline="\n")
        temporary.replace(agents)
    return {"changed": changed, "agents": str(agents), "backup": str(backup) if backup else None}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--backup-root", type=Path)
    args = parser.parse_args()
    result = install(args.workspace, args.policy, args.backup_root)
    print(f"AGENTS_POLICY_CHANGED={str(result['changed']).lower()}")
    print(f"AGENTS_PATH={result['agents']}")
    if result["backup"]:
        print(f"AGENTS_BACKUP={result['backup']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
