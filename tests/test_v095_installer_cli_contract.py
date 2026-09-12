from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_installers_use_provider_neutral_v095_cli_for_enable_and_launcher():
    windows = (ROOT / "scripts" / "install.ps1").read_text(encoding="utf-8")
    posix = (ROOT / "scripts" / "install.sh").read_text(encoding="utf-8")

    assert '$cliScript = Join-Path $targetSkill "scripts\\cnxclaw.py"' in windows
    assert 'CLI_SCRIPT="$TARGET_SKILL/scripts/cnxclaw.py"' in posix
    assert "cnxclaw_v093.py" not in windows
    assert "cnxclaw_v093.py" not in posix
