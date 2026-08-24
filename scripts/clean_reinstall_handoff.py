#!/usr/bin/env python3
"""Auditable backup boundary and failure accounting for clean reinstall."""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path


def canonical(path: Path) -> Path:
    return path.expanduser().resolve(strict=False)


def validate_backup_boundary(app_data: Path, backup_root: Path) -> dict[str, str]:
    app = canonical(app_data)
    backup = canonical(backup_root)
    try:
        backup.relative_to(app)
    except ValueError:
        pass
    else:
        raise RuntimeError("clean-reinstall backup root must be outside active application-data root")
    if os.path.normcase(str(app)) == os.path.normcase(str(backup)):
        raise RuntimeError("clean-reinstall backup root must differ from active application-data root")
    return {"applicationData": str(app), "backupRoot": str(backup), "boundary": "external"}


def write_recovery(backup: Path, workspace: Path, error: str) -> Path:
    backup = canonical(backup)
    backup.mkdir(parents=True, exist_ok=True)
    target = backup / "clean-reinstall-recovery.json"
    payload = {
        "schemaVersion": 1,
        "status": "REINSTALL_FAILED_BACKUP_PRESERVED",
        "productId": "cogentnexus-openclaw",
        "workspace": str(canonical(workspace)),
        "backup": str(backup),
        "error": error,
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "humanDecisionRequired": True,
    }
    temporary = target.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(target)
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    boundary = sub.add_parser("validate-boundary")
    boundary.add_argument("--app-data", type=Path, required=True)
    boundary.add_argument("--backup-root", type=Path, required=True)
    recovery = sub.add_parser("write-recovery")
    recovery.add_argument("--backup", type=Path, required=True)
    recovery.add_argument("--workspace", type=Path, required=True)
    recovery.add_argument("--error", required=True)
    args = parser.parse_args()
    if args.command == "validate-boundary":
        result = validate_backup_boundary(args.app_data, args.backup_root)
    else:
        target = write_recovery(args.backup, args.workspace, args.error)
        result = {"recovery": str(target)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
