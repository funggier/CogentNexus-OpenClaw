from pathlib import Path
import re


INSTALLER = Path(__file__).resolve().parents[1] / "scripts" / "install.ps1"
SOURCE = INSTALLER.read_text(encoding="utf-8")


def test_ticket_db_bootstrap_routes_node_through_native_diagnostic_boundary():
    """Node SQLite warnings on stderr must not terminate PowerShell 5.1 before exit classification."""
    bare = re.findall(
        r'(?m)^\s*node\s+\(Join-Path\s+\$pluginDir\s+"scripts\\bootstrap-ticket-db\.mjs"\)\s+--workspace\s+\$Workspace\s*$',
        SOURCE,
    )
    assert bare == [], (
        "bare ticket-db bootstrap runs under ErrorActionPreference=Stop and can terminate "
        "on benign native stderr before LASTEXITCODE is observed"
    )

    window_match = re.search(
        r'if \(-not \$SkipPlugin\) \{(?P<body>[\s\S]{0,1800}?)\n\}',
        SOURCE,
    )
    assert window_match, "ticket-db bootstrap installer block is missing"
    body = window_match.group("body")

    assert 'Start-InstallerDiagnosticStage -Stage "ticket-db-bootstrap"' in body
    assert 'Invoke-NativeInstallerDiagnostic -Executable "node"' in body
    assert 'scripts\\bootstrap-ticket-db.mjs' in body
    assert '"--workspace"' in body
    assert '$Workspace' in body
    assert 'Complete-InstallerDiagnosticStage -Context $ticketDbDiagnostic -ExitCode $ticketDbExit' in body
    assert 'Get-BoundedInstallerDiagnostic' in body
    assert 'if ($ticketDbExit -ne 0)' in body


def test_ticket_db_bootstrap_does_not_globally_suppress_node_warnings():
    assert "NODE_NO_WARNINGS" not in SOURCE
    assert "--no-warnings" not in SOURCE
