from pathlib import Path
import re


INSTALLER = Path(__file__).resolve().parents[1] / "scripts" / "install.ps1"
SOURCE = INSTALLER.read_text(encoding="utf-8")


def test_windows_installer_routes_npm_through_native_diagnostic_boundary():
    """npm warnings on stderr with exit 0 must not terminate PowerShell 5.1."""
    bare_npm = re.findall(r"(?m)^\s*npm\s+(?:ci|run\s+plugin:validate)\s*$", SOURCE)
    assert bare_npm == [], (
        "bare npm calls run under ErrorActionPreference=Stop and can terminate on "
        "benign stderr before LASTEXITCODE is observed"
    )
    assert SOURCE.count('Invoke-NativeInstallerDiagnostic -Executable "npm.cmd"') >= 2
    assert "candidate npm ci failed before classification" in SOURCE
    assert "candidate plugin validation failed before classification" in SOURCE
