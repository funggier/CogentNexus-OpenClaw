from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install.sh"


def test_posix_installer_has_no_provider_parameter_or_default():
    text = INSTALLER.read_text(encoding="utf-8")
    assert 'PROVIDER=' not in text
    assert "--provider" not in text
    assert "PROVIDER" not in text


def test_posix_installer_does_not_validate_or_require_provider_executable():
    text = INSTALLER.read_text(encoding="utf-8")
    assert "ollama" not in text.lower()
    assert "lmstudio" not in text.lower()
    assert 'command -v "$command_name"' not in text or "ollama" not in text


def test_posix_installer_messages_and_handoff_are_provider_neutral():
    text = INSTALLER.read_text(encoding="utf-8")
    assert "Ollama-only" not in text
    assert "Provider:" not in text
    assert "enable --provider" not in text
    assert "enable" in text


def test_posix_canonical_install_command_is_provider_free():
    text = (ROOT / "docs/operations/coordination/tasks/CNX-20260828-118-posix-installer-provider-neutrality-alignment.md").read_text(encoding="utf-8")
    assert './scripts/install.sh --workspace "$HOME/.openclaw/workspace"' in text
