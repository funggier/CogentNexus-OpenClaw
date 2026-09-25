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


def test_installer_npm_ci_suppresses_dependency_lifecycle_scripts():
    """Candidate dependency install must not execute peer/dev dependency lifecycle side effects."""
    guarded_ci = 'Invoke-NativeInstallerDiagnostic -Executable "npm.cmd" -Arguments @("ci", "--ignore-scripts")'
    assert SOURCE.count(guarded_ci) == 2, (
        "both candidate-preparation npm ci paths must install dependencies without executing "
        "OpenClaw peer/dev dependency lifecycle scripts"
    )


def test_all_candidate_dependency_preparation_surfaces_suppress_dependency_lifecycle_scripts():
    root = INSTALLER.parents[1]
    surfaces = {
        "scripts/install.sh": (root / "scripts/install.sh").read_text(encoding="utf-8"),
        "scripts/publish-release.ps1": (root / "scripts/publish-release.ps1").read_text(encoding="utf-8"),
        ".github/workflows/validate.yml": (root / ".github/workflows/validate.yml").read_text(encoding="utf-8"),
        ".github/workflows/release.yml": (root / ".github/workflows/release.yml").read_text(encoding="utf-8"),
        ".github/workflows/windows-installer-pack-smoke.yml": (
            root / ".github/workflows/windows-installer-pack-smoke.yml"
        ).read_text(encoding="utf-8"),
    }
    for relative, text in surfaces.items():
        plain_ci = re.findall(r"(?m)^\\s*(?:- run:\\s*)?npm ci\\s*$", text)
        assert plain_ci == [], f"{relative} must not execute dependency lifecycle scripts during candidate preparation"
        assert "npm ci --ignore-scripts" in text, relative
