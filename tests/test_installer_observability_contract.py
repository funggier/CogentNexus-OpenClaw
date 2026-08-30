"""CNX-20260830-158 — Windows install-over observability contract.

Task 157 timed out after the installer had crossed the native handoff boundary,
but the durable output could not identify which later external substage was
active.  The production installer must therefore own stable START/COMPLETE
records around the critical late substages without changing their semantics.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).parents[1]
INSTALL_PS1 = (REPO / "scripts" / "install.ps1").read_text(encoding="utf-8")


def test_installer_diagnostic_record_format_is_machine_searchable():
    assert "CNX_INSTALL_STAGE_START" in INSTALL_PS1
    assert "CNX_INSTALL_STAGE_COMPLETE" in INSTALL_PS1
    assert "utc=" in INSTALL_PS1
    assert "elapsed_ms=" in INSTALL_PS1
    assert "exit_code=" in INSTALL_PS1


def _position(pattern: str) -> int:
    match = re.search(pattern, INSTALL_PS1)
    assert match, f"production installer pattern not found: {pattern}"
    return match.start()


def _assert_stage_brackets_command(stage: str, command_pattern: str) -> None:
    command_pos = _position(command_pattern)
    start_pattern = rf"Start-InstallerDiagnosticStage\s+-Stage\s+[\"']{re.escape(stage)}[\"']"
    complete_pattern = r"Complete-InstallerDiagnosticStage\s+-Context\s+\$[A-Za-z0-9_]+\s+-ExitCode\s+\$[A-Za-z0-9_]+"

    starts = [m.start() for m in re.finditer(start_pattern, INSTALL_PS1)]
    assert starts, f"missing diagnostic START for stage {stage}"
    start_pos = max((p for p in starts if p < command_pos), default=-1)
    assert start_pos >= 0, f"diagnostic START for {stage} must precede its command"

    next_stage_start = min(
        (m.start() for m in re.finditer(r"Start-InstallerDiagnosticStage\s+-Stage", INSTALL_PS1) if m.start() > command_pos),
        default=len(INSTALL_PS1),
    )
    completion = re.search(complete_pattern, INSTALL_PS1[command_pos:next_stage_start])
    assert completion, f"diagnostic COMPLETE for {stage} must follow its command before the next stage"

    between = INSTALL_PS1[command_pos : command_pos + completion.end()]
    assert "$LASTEXITCODE" in between, f"stage {stage} must snapshot child exit code before diagnostic completion"


def test_critical_late_install_over_substages_are_bracketed():
    stages = [
        (
            "ticket-db-bootstrap",
            r"node\s+\(Join-Path\s+\$pluginDir\s+[\"']scripts\\bootstrap-ticket-db\.mjs[\"']\)\s+--workspace",
        ),
        ("plugin-npm-pack", r"npm\s+pack\s+--json"),
        ("plugin-rollover-prepare", r"[\"']rollover-prepare[\"']"),
        ("plugin-install-local-package", r"openclaw\s+plugins\s+install\s+\$packagePath\s+--force"),
        ("plugin-disable-post-install", r"openclaw\s+plugins\s+disable\s+cogentnexus-openclaw"),
        ("plugin-rollover-finalize", r"[\"']rollover-finalize[\"']"),
        ("owned-runtime-ensure", r"ensure-runtime\s+--application-data-root"),
    ]

    for stage, command_pattern in stages:
        _assert_stage_brackets_command(stage, command_pattern)
