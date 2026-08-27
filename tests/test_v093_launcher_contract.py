import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus-openclaw" / "scripts"
VALIDATE = SCRIPTS / "validate.py"
FACADE = SCRIPTS / "cnxclaw_v093.py"
LIFECYCLE_TEMPLATE = ROOT / "skills" / "cogentnexus-openclaw" / "templates" / "lifecycle" / "cnxclaw.cmd"
LIFECYCLE_README = LIFECYCLE_TEMPLATE.parent / "README.md"


def test_v093_facade_help_is_current_and_ollama_only():
    result = subprocess.run(
        [sys.executable, str(FACADE), "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    assert "v0.9.3" in result.stdout
    assert "Ollama-only" in result.stdout
    assert "--provider ollama" in result.stdout
    assert "--provider lmstudio" not in result.stdout.lower()


def test_v093_facade_rejects_lmstudio_before_legacy_backend_execution():
    result = subprocess.run(
        [sys.executable, str(FACADE), "start", "--provider", "lmstudio"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 2
    combined = f"{result.stdout}\n{result.stderr}".lower()
    assert "unsupported provider" in combined
    assert "only 'ollama' is supported" in combined


def test_validate_checks_current_v093_facade_not_legacy_provider_surface():
    source = VALIDATE.read_text(encoding="utf-8")
    assert '"scripts" / "cnxclaw_v093.py"' in source
    assert '"--provider ollama|lmstudio"' not in source
    assert "v0.9.2 CNXCLAW CLI validation failed" not in source


def test_released_lifecycle_template_preserves_v092_compatibility_backend():
    text = LIFECYCLE_TEMPLATE.read_text(encoding="utf-8")
    assert "scripts\\cnxclaw.py" in text
    assert "cnxclaw_v093.py" not in text


def test_lifecycle_readme_separates_compatibility_template_from_current_v093_launcher():
    text = LIFECYCLE_README.read_text(encoding="utf-8")
    assert "v0.9.2" in text
    assert "compatibility" in text.lower()
    assert "v0.9.3" in text
    assert "cnxclaw_v093.py" in text
