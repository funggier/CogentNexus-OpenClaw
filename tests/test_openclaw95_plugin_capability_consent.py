from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_windows_installer_accepts_attested_plugin_capabilities():
    source = (ROOT / "scripts" / "install.ps1").read_text(encoding="utf-8")
    assert "openclaw plugins install $packagePath --force --accept-capabilities" in source


def test_posix_installer_accepts_attested_plugin_capabilities():
    source = (ROOT / "scripts" / "install.sh").read_text(encoding="utf-8")
    assert 'openclaw plugins install "npm-pack:$PLUGIN_DIR/$PACKAGE_FILE" --force --accept-capabilities' in source
