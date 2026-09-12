from __future__ import annotations

import importlib.util
import json
import sqlite3
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "skills" / "cogentnexus-openclaw" / "scripts" / "host_state_v095.py"


def load_module():
    spec = importlib.util.spec_from_file_location("cnx_upgrade_migration_v095", MODULE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_v094_state_matrix_migrates_without_inventing_provider_authority():
    module = load_module()
    cases = [
        ({"schemaVersion": 1, "mode": "managed", "desiredGateway": "running", "desiredProvider": "running", "generation": 9}, True, "active"),
        ({"schemaVersion": 1, "mode": "maintenance", "desiredGateway": "stopped", "desiredProvider": "stopped", "generation": 4}, True, "maintenance"),
        ({"schemaVersion": 1, "mode": "passthrough", "desiredGateway": "running", "desiredProvider": "unchanged", "generation": 6}, False, "disabled"),
        ({"schemaVersion": 1, "mode": "passthrough", "desiredGateway": "running", "desiredProvider": "unchanged", "generation": 12}, True, "active"),
    ]

    for legacy, plugin_enabled, expected_mode in cases:
        migrated = module.migrate_v094_state(legacy, plugin_enabled)
        assert migrated["schemaVersion"] == 2
        assert migrated["cnxMode"] == expected_mode
        assert migrated["desiredGateway"] == legacy["desiredGateway"]
        assert migrated["generation"] == legacy["generation"]
        assert migrated["providerOwnership"] == "openclaw"
        assert "desiredProvider" not in migrated
        assert "selectedProvider" not in migrated
        assert "providerTransition" not in migrated


def test_cloud_passthrough_preserves_openclaw_owned_config_snapshot_and_only_translates_cnx_state():
    module = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        config_path = root / "openclaw.json"
        config = {
            "agents": {"defaults": {"model": {"primary": "cloud-a/model-x"}}},
            "auth": {"profiles": {"cloud-a": {"provider": "cloud-a", "apiKey": "opaque-test-secret"}}},
            "routing": {"default": "cloud-a/model-x", "fallback": ["cloud-b/model-y"]},
        }
        original_bytes = json.dumps(config, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
        config_path.write_bytes(original_bytes)

        legacy = {
            "schemaVersion": 1,
            "mode": "passthrough",
            "desiredGateway": "running",
            "desiredProvider": "unchanged",
            "selectedProvider": "ollama",
            "providerTransition": {"from": "ollama", "to": "cloud-a"},
            "generation": 18,
        }
        migrated = module.migrate_v094_state(legacy, plugin_enabled=True)

        assert migrated["cnxMode"] == "active"
        assert migrated["generation"] == 18
        assert config_path.read_bytes() == original_bytes
        assert json.loads(config_path.read_text(encoding="utf-8")) == config
        assert migrated["providerOwnership"] == "openclaw"


def test_durable_ticket_delivery_and_session_rows_survive_state_translation_unchanged():
    module = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        db_path = root / "tickets.sqlite3"
        db = sqlite3.connect(db_path)
        db.executescript(
            """
            CREATE TABLE tickets(ticket_id TEXT PRIMARY KEY, status TEXT NOT NULL);
            CREATE TABLE cnx_sessions(session_key TEXT PRIMARY KEY, state TEXT NOT NULL, generation INTEGER NOT NULL);
            CREATE TABLE cnx_assistant_delivery(delivery_id INTEGER PRIMARY KEY AUTOINCREMENT, ticket_id TEXT NOT NULL, status TEXT NOT NULL, owner_session_key TEXT NOT NULL, owner_generation INTEGER NOT NULL);
            """
        )
        db.execute("INSERT INTO tickets(ticket_id,status) VALUES ('T-migrate','accepted')")
        db.execute("INSERT INTO cnx_sessions(session_key,state,generation) VALUES ('S-migrate','active',22)")
        db.execute("INSERT INTO cnx_assistant_delivery(ticket_id,status,owner_session_key,owner_generation) VALUES ('T-migrate','pending','S-migrate',22)")
        db.commit()
        before = [
            db.execute("SELECT ticket_id,status FROM tickets").fetchall(),
            db.execute("SELECT session_key,state,generation FROM cnx_sessions").fetchall(),
            db.execute("SELECT delivery_id,ticket_id,status,owner_session_key,owner_generation FROM cnx_assistant_delivery").fetchall(),
        ]

        module.migrate_v094_state(
            {
                "schemaVersion": 1,
                "mode": "managed",
                "desiredGateway": "running",
                "desiredProvider": "running",
                "generation": 22,
            },
            plugin_enabled=True,
        )
        after = [
            db.execute("SELECT ticket_id,status FROM tickets").fetchall(),
            db.execute("SELECT session_key,state,generation FROM cnx_sessions").fetchall(),
            db.execute("SELECT delivery_id,ticket_id,status,owner_session_key,owner_generation FROM cnx_assistant_delivery").fetchall(),
        ]
        db.close()
        assert after == before


def test_read_only_load_does_not_rewrite_legacy_controller_state():
    module = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        controller = root / "host" / "controller.json"
        controller.parent.mkdir(parents=True)
        legacy = {
            "schemaVersion": 1,
            "mode": "passthrough",
            "desiredGateway": "running",
            "desiredProvider": "unchanged",
            "generation": 8,
        }
        controller.write_text(json.dumps(legacy, sort_keys=True), encoding="utf-8")
        before = controller.read_bytes()
        state = module.load_state(root, plugin_enabled=True)
        assert state["cnxMode"] == "active"
        assert controller.read_bytes() == before


def test_invalid_legacy_state_fails_closed_without_mutation():
    module = load_module()
    with pytest.raises(ValueError):
        module.migrate_v094_state({"schemaVersion": 1, "mode": "unknown"}, plugin_enabled=True)
