from __future__ import annotations

import importlib.util
from pathlib import Path

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
