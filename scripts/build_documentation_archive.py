#!/usr/bin/env python3
"""Build the deterministic user/operator documentation release archive."""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)

CURRENT_GUIDES = (
    "README.md",
    "LICENSE",
    "VERSION",
    "docs/BASELINE.md",
    "docs/CHECK_SYSTEM.md",
    "docs/CLEAN_REINSTALL.md",
    "docs/CLEAN_REINSTALL.th.md",
    "docs/COMMANDS.th.md",
    "docs/CONTINUITY_TESTS.th.md",
    "docs/CURRENT_STATE.md",
    "docs/INSTALL.md",
    "docs/INSTALL.th.md",
    "docs/KNOWLEDGE.md",
    "docs/POST_RELEASE_BASELINE.md",
    "docs/PROVIDERS.md",
    "docs/TRANSIENT_STALL_RECOVERY.md",
    "docs/V093_OLLAMA_ONLY.md",
    "docs/V093_RECOVERY_REALITY_TESTS.md",
    "docs/operations/ROADMAP.md",
    "docs/operations/STATUS.md",
    "plugins/cogentnexus-openclaw/README.md",
    "skills/cogentnexus-openclaw/SKILL.md",
)

REFERENCE_TREES = (
    "docs/architecture",
    "docs/superpowers",
    "skills/cogentnexus-openclaw/references",
)

FORBIDDEN_PARTS = {".git", ".cogentnexus-openclaw", "node_modules", "__pycache__"}


def _archive_root(version: str) -> str:
    return f"cogentnexus-openclaw-v{version}-document"


def _validate_regular_file(path: Path, repo_root: Path) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"documentation source missing: {path.relative_to(repo_root)}")
    if path.is_symlink():
        raise RuntimeError(f"documentation source must not be a symlink: {path.relative_to(repo_root)}")


def collect_documentation(repo_root: Path, version: str) -> list[Path]:
    repo_root = repo_root.resolve()
    selected: set[Path] = set()
    for relative in CURRENT_GUIDES:
        path = repo_root / relative
        _validate_regular_file(path, repo_root)
        selected.add(path)
    release_note = repo_root / "docs" / "releases" / f"v{version}.md"
    _validate_regular_file(release_note, repo_root)
    selected.add(release_note)
    for relative in REFERENCE_TREES:
        root = repo_root / relative
        if not root.is_dir():
            raise FileNotFoundError(f"documentation tree missing: {relative}")
        for path in root.rglob("*.md"):
            if any(part in FORBIDDEN_PARTS for part in path.relative_to(repo_root).parts):
                continue
            _validate_regular_file(path, repo_root)
            selected.add(path)
    ordered = sorted(selected, key=lambda p: p.relative_to(repo_root).as_posix().lower())
    if not ordered:
        raise RuntimeError("documentation selection is empty")
    return ordered


def _zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, date_time=FIXED_ZIP_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = (0o100644 & 0xFFFF) << 16
    info.create_system = 3
    return info


def build_archive(repo_root: Path, version: str, output: Path) -> dict[str, object]:
    repo_root = repo_root.resolve()
    output = output.resolve()
    files = collect_documentation(repo_root, version)
    root_name = _archive_root(version)
    index_lines = [
        f"# CogentNexus-OpenClaw v{version} Documentation",
        "",
        "This archive contains current user/operator guidance plus architecture/reference documentation.",
        "Development coordination reports, task histories, runtime state, credentials, dependencies, and build caches are intentionally excluded.",
        "",
        "## Included files",
        "",
    ]
    index_lines.extend(f"- `{path.relative_to(repo_root).as_posix()}`" for path in files)
    index_payload = ("\n".join(index_lines) + "\n").encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        archive.writestr(_zip_info(f"{root_name}/DOCUMENTATION_INDEX.md"), index_payload)
        for path in files:
            relative = path.relative_to(repo_root).as_posix()
            archive.writestr(_zip_info(f"{root_name}/{relative}"), path.read_bytes())
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    return {
        "version": version,
        "archive": str(output),
        "archiveRoot": root_name,
        "fileCount": len(files) + 1,
        "sha256": digest,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--version", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build_archive(args.repo_root, args.version, args.output)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
