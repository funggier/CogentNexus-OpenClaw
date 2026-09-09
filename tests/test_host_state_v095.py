from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "skills" / "cogentnexus-openclaw" / "scripts" / "host_state_v095.py"


def load_module():
    if not MODULE_PATH.is_file():
        raise AssertionError(
            "v0.9.5 Host authority module is missing; expected "
            "skills/cogentnexus-openclaw/scripts/host_state_v095.py"
        )
    spec = importlib.util.spec_from_file_location("cnx_host_state_v095_contract", MODULE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def migrate(state: dict, *, plugin_enabled: bool):
    module = load_module()
    return module.migrate_v094_state(state, plugin_enabled)


def controller_path(root: Path) -> Path:
    return root / "host" / "controller.json"


def test_v094_managed_migrates_to_active_without_provider_authority():
    old = {
        "schemaVersion": 1,
        "mode": "managed",
        "desiredGateway": "running",
        "desiredProvider": "running",
        "generation": 9,
    }
    new = migrate(old, plugin_enabled=True)

    assert new["schemaVersion"] == 2
    assert new["cnxMode"] == "active"
    assert new["desiredGateway"] == "running"
    assert new["providerOwnership"] == "openclaw"
    assert new["generation"] == 9
    assert "desiredProvider" not in new
    assert "selectedProvider" not in new
    assert "providerTransition" not in new


def test_v094_maintenance_migrates_to_maintenance():
    old = {
        "schemaVersion": 1,
        "mode": "maintenance",
        "desiredGateway": "stopped",
        "desiredProvider": "stopped",
        "generation": 4,
    }
    new = migrate(old, plugin_enabled=True)

    assert new["cnxMode"] == "maintenance"
    assert new["desiredGateway"] == "stopped"
    assert new["providerOwnership"] == "openclaw"
    assert new["generation"] == 4
    assert "desiredProvider" not in new


def test_v094_cloud_passthrough_with_enabled_plugin_migrates_to_active():
    old = {
        "schemaVersion": 1,
        "mode": "passthrough",
        "desiredGateway": "running",
        "desiredProvider": "unchanged",
        "selectedProvider": "ollama",
        "providerTransition": {"from": "ollama", "to": "lmstudio"},
        "generation": 12,
    }
    new = migrate(old, plugin_enabled=True)

    assert new["cnxMode"] == "active"
    assert new["desiredGateway"] == "running"
    assert new["providerOwnership"] == "openclaw"
    assert new["generation"] == 12
    assert "desiredProvider" not in new
    assert "selectedProvider" not in new
    assert "providerTransition" not in new


def test_v094_passthrough_with_disabled_plugin_migrates_to_disabled():
    old = {
        "schemaVersion": 1,
        "mode": "passthrough",
        "desiredGateway": "running",
        "desiredProvider": "unchanged",
        "generation": 6,
    }
    new = migrate(old, plugin_enabled=False)

    assert new["cnxMode"] == "disabled"
    assert new["desiredGateway"] == "running"
    assert new["providerOwnership"] == "openclaw"
    assert new["generation"] == 6
    assert "desiredProvider" not in new


def test_v095_state_is_idempotent_and_does_not_reinterpret_provider_metadata():
    current = {
        "schemaVersion": 2,
        "cnxMode": "active",
        "desiredGateway": "running",
        "providerOwnership": "openclaw",
        "managedLocalAdapters": {"ollama": "auto"},
        "generation": 15,
        "updatedAt": "2026-09-09T11:00:00+00:00",
    }
    new = migrate(current, plugin_enabled=True)

    assert new["schemaVersion"] == 2
    assert new["cnxMode"] == "active"
    assert new["providerOwnership"] == "openclaw"
    assert new["generation"] == 15
    assert new["managedLocalAdapters"] == {"ollama": "auto"}


def test_missing_state_loads_provider_independent_default_without_writing():
    module = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        state = module.load_state(root, plugin_enabled=True)

        assert state["schemaVersion"] == 2
        assert state["cnxMode"] == "active"
        assert state["desiredGateway"] == "running"
        assert state["providerOwnership"] == "openclaw"
        assert state["generation"] == 1
        assert state["managedLocalAdapters"] == {"ollama": "auto"}
        assert not controller_path(root).exists()


def test_load_legacy_state_translates_read_only_using_exact_plugin_evidence():
    module = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        path = controller_path(root)
        path.parent.mkdir(parents=True)
        legacy = {
            "schemaVersion": 1,
            "mode": "passthrough",
            "desiredGateway": "running",
            "desiredProvider": "unchanged",
            "generation": 8,
        }
        path.write_text(json.dumps(legacy), encoding="utf-8")

        state = module.load_state(root, plugin_enabled=True)

        assert state["cnxMode"] == "active"
        assert state["generation"] == 8
        assert json.loads(path.read_text(encoding="utf-8"))["schemaVersion"] == 1


def test_save_state_persists_only_canonical_authority_fields_atomically():
    module = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        written = module.save_state(
            root,
            {
                "schemaVersion": 2,
                "cnxMode": "active",
                "desiredGateway": "running",
                "providerOwnership": "openclaw",
                "managedLocalAdapters": {"ollama": "disabled"},
                "generation": 3,
                "selectedProvider": "ollama",
                "desiredProvider": "running",
            },
        )

        persisted = json.loads(controller_path(root).read_text(encoding="utf-8"))
        assert persisted == written
        assert persisted["schemaVersion"] == 2
        assert persisted["providerOwnership"] == "openclaw"
        assert persisted["managedLocalAdapters"] == {"ollama": "disabled"}
        assert "selectedProvider" not in persisted
        assert "desiredProvider" not in persisted
        assert not controller_path(root).with_suffix(".tmp").exists()


def test_transition_mode_increments_generation_only_for_actual_authority_change():
    module = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        module.save_state(
            root,
            {
                "schemaVersion": 2,
                "cnxMode": "active",
                "desiredGateway": "running",
                "providerOwnership": "openclaw",
                "managedLocalAdapters": {"ollama": "auto"},
                "generation": 20,
            },
        )

        changed = module.transition_mode(root, "maintenance", desired_gateway="stopped")
        assert changed["cnxMode"] == "maintenance"
        assert changed["desiredGateway"] == "stopped"
        assert changed["generation"] == 21

        unchanged = module.transition_mode(root, "maintenance", desired_gateway="stopped")
        assert unchanged["generation"] == 21


def test_transition_mode_rejects_invalid_mode_without_mutation():
    module = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        initial = module.save_state(
            root,
            {
                "schemaVersion": 2,
                "cnxMode": "active",
                "desiredGateway": "running",
                "providerOwnership": "openclaw",
                "managedLocalAdapters": {"ollama": "auto"},
                "generation": 2,
            },
        )
        before = controller_path(root).read_bytes()

        with pytest.raises(ValueError):
            module.transition_mode(root, "cloud")

        assert controller_path(root).read_bytes() == before
        assert json.loads(before)["generation"] == initial["generation"]
