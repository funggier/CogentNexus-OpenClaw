from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus-openclaw" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
HOST_PATH = SCRIPTS / "host.py"


def load_host():
    spec = importlib.util.spec_from_file_location("cnx_host_v095_bridge_contract", HOST_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def controller_path(root: Path) -> Path:
    return root / "host" / "controller.json"


def write_canonical(root: Path, *, mode: str = "active", generation: int = 7) -> None:
    path = controller_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "schemaVersion": 2,
                "cnxMode": mode,
                "desiredGateway": "running",
                "providerOwnership": "openclaw",
                "managedLocalAdapters": {"ollama": "auto"},
                "generation": generation,
                "updatedAt": "2026-09-09T11:00:00+00:00",
            }
        ),
        encoding="utf-8",
    )


def test_default_state_is_canonical_with_derived_legacy_mode_only():
    host = load_host()
    state = host.default_state()

    assert state["schemaVersion"] == 2
    assert state["cnxMode"] == "active"
    assert state["providerOwnership"] == "openclaw"
    assert state["mode"] == "managed"
    assert "desiredProvider" not in state
    assert "selectedProvider" not in state
    assert "providerTransition" not in state


def test_load_state_derives_compatibility_mode_without_persisting_it():
    host = load_host()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_canonical(root, mode="disabled", generation=11)

        state = host.load_state(root)
        persisted = json.loads(controller_path(root).read_text(encoding="utf-8"))

        assert state["cnxMode"] == "disabled"
        assert state["mode"] == "passthrough"
        assert state["generation"] == 11
        assert "mode" not in persisted
        assert "desiredProvider" not in persisted


def test_legacy_passthrough_load_uses_explicit_plugin_evidence_only():
    host = load_host()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        path = controller_path(root)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "mode": "passthrough",
                    "desiredGateway": "running",
                    "desiredProvider": "unchanged",
                    "generation": 5,
                }
            ),
            encoding="utf-8",
        )

        enabled = host.load_state(root, plugin_enabled=True)
        disabled = host.load_state(root, plugin_enabled=False)

        assert enabled["cnxMode"] == "active"
        assert enabled["mode"] == "managed"
        assert disabled["cnxMode"] == "disabled"
        assert disabled["mode"] == "passthrough"
        assert json.loads(path.read_text(encoding="utf-8"))["schemaVersion"] == 1


def test_save_state_persists_schema2_and_strips_legacy_provider_fields():
    host = load_host()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        returned = host.save_state(
            root,
            {
                "schemaVersion": 2,
                "cnxMode": "active",
                "mode": "managed",
                "desiredGateway": "running",
                "desiredProvider": "running",
                "selectedProvider": "ollama",
                "providerTransition": {"to": "ollama"},
                "providerOwnership": "openclaw",
                "managedLocalAdapters": {"ollama": "auto"},
                "generation": 9,
            },
        )
        persisted = json.loads(controller_path(root).read_text(encoding="utf-8"))

        assert returned["mode"] == "managed"
        assert returned["cnxMode"] == "active"
        assert persisted["schemaVersion"] == 2
        assert persisted["cnxMode"] == "active"
        assert persisted["generation"] == 9
        assert "mode" not in persisted
        assert "desiredProvider" not in persisted
        assert "selectedProvider" not in persisted
        assert "providerTransition" not in persisted


def test_provider_only_legacy_transition_is_generation_neutral_and_not_persisted():
    host = load_host()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_canonical(root, mode="active", generation=30)
        before = controller_path(root).read_bytes()

        result = host.transition(
            root,
            desiredProvider="running",
            selectedProvider="ollama",
            providerTransition={"from": None, "to": "ollama"},
        )

        assert result["generation"] == 30
        assert result["cnxMode"] == "active"
        assert controller_path(root).read_bytes() == before


def test_legacy_mode_transition_maps_to_canonical_authority_once():
    host = load_host()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_canonical(root, mode="active", generation=40)

        changed = host.transition(
            root,
            mode="maintenance",
            desiredGateway="stopped",
            desiredProvider="stopped",
        )
        persisted = json.loads(controller_path(root).read_text(encoding="utf-8"))

        assert changed["cnxMode"] == "maintenance"
        assert changed["mode"] == "maintenance"
        assert changed["generation"] == 41
        assert persisted["cnxMode"] == "maintenance"
        assert persisted["desiredGateway"] == "stopped"
        assert persisted["generation"] == 41
        assert "desiredProvider" not in persisted

        unchanged = host.transition(
            root,
            mode="maintenance",
            desiredGateway="stopped",
            desiredProvider="running",
        )
        assert unchanged["generation"] == 41
