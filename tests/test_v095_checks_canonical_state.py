import importlib.util
import json
import sys
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus-openclaw" / "scripts"
SCRIPT = SCRIPTS / "checks.py"
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location("cnx_v095_checks", SCRIPT)
checks = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(checks)


def test_read_state_accepts_canonical_v095_controller_without_mutation(tmp_path):
    root = tmp_path / ".cogentnexus-openclaw"
    controller = root / "host" / "controller.json"
    controller.parent.mkdir(parents=True)
    original = {
        "schemaVersion": 2,
        "cnxMode": "active",
        "desiredGateway": "running",
        "providerOwnership": "openclaw",
        "generation": 97,
    }
    controller.write_text(json.dumps(original), encoding="utf-8")

    state, error = checks.read_state(root)

    assert error is None
    assert state["mode"] == "managed"
    assert state["cnxMode"] == "active"
    assert json.loads(controller.read_text(encoding="utf-8")) == original


def test_read_state_rejects_unknown_canonical_mode(tmp_path):
    root = tmp_path / ".cogentnexus-openclaw"
    controller = root / "host" / "controller.json"
    controller.parent.mkdir(parents=True)
    controller.write_text(json.dumps({"schemaVersion": 2, "cnxMode": "unknown"}), encoding="utf-8")

    state, error = checks.read_state(root)

    assert state is None
    assert error == "invalid Host mode: None"
