from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = [
    ROOT / "docs" / "CLEAN_REINSTALL.md",
    ROOT / "docs" / "CLEAN_REINSTALL.th.md",
]
SCRIPT = ROOT / "scripts" / "clean-reinstall.ps1"


def test_clean_reinstall_docs_match_external_backup_path():
    script = SCRIPT.read_text(encoding="utf-8")
    implementation_name = "CogentNexus-OpenClaw-Clean-Reinstall-Backups"
    expected = r"%LOCALAPPDATA%\CogentNexus-OpenClaw-Clean-Reinstall-Backups\<timestamp>"
    obsolete = r"%LOCALAPPDATA%\CogentNexus-OpenClaw\clean-reinstall-backups\<timestamp>"

    assert implementation_name in script
    for path in DOCS:
        text = path.read_text(encoding="utf-8")
        assert expected in text, f"{path} must document the external backup root used by clean-reinstall.ps1"
        assert obsolete not in text, f"{path} must not place backups inside the application-data tree"


def test_clean_reinstall_docs_follow_current_version():
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    assert version

    for path in DOCS:
        text = path.read_text(encoding="utf-8")
        assert f"v{version}" in text, f"{path} must identify the current clean-reinstall candidate version"
        assert "v0.9.1" not in text, f"{path} must not teach the obsolete v0.9.1 reinstall target"
