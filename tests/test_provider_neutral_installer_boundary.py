import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install.ps1"


def test_installer_has_provider_neutral_parameter_boundary():
    text = INSTALLER.read_text(encoding="utf-8")
    param_block = text.split(")", 1)[0]
    assert not re.search(r"\$Provider|ValidateSet\s*\(\s*['\"]ollama", param_block, re.I)
    assert "Provider: ollama" not in text
    assert "Ollama-only" not in text


def test_installer_does_not_own_provider_executable_or_lifecycle_policy():
    text = INSTALLER.read_text(encoding="utf-8")
    assert not re.search(r"Require-Command\s+ollama|--provider\s+ollama|\$Provider", text, re.I)


def test_canonical_install_docs_are_provider_free():
    for path in (ROOT / "docs" / "INSTALL.md", ROOT / "docs" / "INSTALL.th.md"):
        text = path.read_text(encoding="utf-8")
        assert "-Provider" not in text
        assert "install.ps1 -Workspace" in text


def test_provider_neutral_install_command_has_no_ambient_provider_slot():
    command = r'powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"'
    assert "-Provider" not in command
    assert "ollama" not in command.lower()
