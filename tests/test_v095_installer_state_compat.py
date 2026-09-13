from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_windows_installer_reads_canonical_v095_controller_mode():
    installer = (ROOT / "scripts" / "install.ps1").read_text(encoding="utf-8")

    assert "cnxMode" in installer
    assert "disabled" in installer
    assert "active" in installer
