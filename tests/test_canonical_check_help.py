import importlib
import re
import subprocess
import sys
from pathlib import Path


SCRIPTS = Path(__file__).parents[1] / "skills/cogentnexus-openclaw/scripts"
sys.path.insert(0, str(SCRIPTS))
base = importlib.import_module("cnxclaw")


GENERIC_COMPONENT = re.compile(r"check " + r"cogentnexus(?=\||\s|$)")


def test_current_help_surfaces_advertise_only_canonical_check_component():
    v093_help = subprocess.run(
        [sys.executable, str(SCRIPTS / "cnxclaw_v093.py"), "--help"],
        text=True,
        capture_output=True,
        check=True,
    ).stdout
    for help_text in (base.help_text(), v093_help):
        assert "check cogentnexus-openclaw" in help_text
        assert not GENERIC_COMPONENT.search(help_text)


def test_missing_component_usage_advertises_canonical_check_component(tmp_path):
    exit_code, result = base.do_check(tmp_path, ["check"])
    assert exit_code == 2
    assert "cogentnexus-openclaw" in result["error"]
    assert not GENERIC_COMPONENT.search(result["error"])


def test_actual_mapping_accepts_canonical_and_rejects_generic_component(tmp_path):
    canonical_exit, canonical = base.do_check(tmp_path, ["check", "cogentnexus-openclaw"])
    generic_name = "cogent" + "nexus"
    generic_exit, generic = base.do_check(tmp_path, ["check", generic_name])

    assert canonical["check"] == "cogentnexus-openclaw"
    assert "error" not in canonical
    assert canonical_exit in {0, 1, 2, 3}
    assert generic_exit == 3
    assert generic["error"] == f"unsupported check component: {generic_name}"
