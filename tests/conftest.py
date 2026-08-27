from __future__ import annotations

import os

import pytest


_WINDOWS_POWERSHELL_NODEIDS = frozenset(
    {
        "tests/test_fresh_transaction_failure_coverage.py::test_f1_harness_injected_failure_triggers_production_rollback",
        "tests/test_fresh_transaction_failure_coverage.py::test_f1b_harness_no_plugin_inverse_when_not_registered_this_attempt",
        "tests/test_installer_mode_isolation.py::test_m1b_harness_upgrade_mode_reaches_installer_body",
        "tests/test_installer_mode_isolation.py::test_m2_nonfresh_failure_never_fresh_rolls_back",
        "tests/test_installer_mode_isolation.py::test_m6_installer_parses_clean",
        "tests/test_installer_transaction_wiring.py::test_p8_production_ast_proves_independent_lifecycle_gates_and_order",
        "tests/test_installer_transaction_wiring.py::test_p7_production_crash_rerun_recovery",
        "tests/test_npm_pack_installer_boundary.py::test_npm11_array_resolves_existing_exact_artifact",
        "tests/test_npm_pack_installer_boundary.py::test_npm12_keyed_object_resolves_existing_exact_artifact",
        "tests/test_npm_pack_installer_boundary.py::test_malformed_pack_shapes_fail_closed",
        "tests/test_npm_pack_installer_boundary.py::test_missing_artifact_fails_closed",
        "tests/test_plugin_generation_rollover.py::test_task085_production_action_truth_table_exists_and_pending_is_rollover_only",
        "tests/test_plugin_generation_rollover.py::test_task085_production_action_truth_table_all_supported_states",
        "tests/test_recovery_preflight_semantics.py::test_t5b_gate_fail_closed_executable",
        "tests/test_recovery_preflight_semantics.py::test_t6_production_clean_fresh_passes_gate",
        "tests/test_upgrade_legacy_mode_isolation_proof.py::test_u2_upgrade_boundary_no_begin_no_fresh_rollback_on_failure",
        "tests/test_upgrade_legacy_mode_isolation_proof.py::test_l2_legacy_reaches_shared_body_and_stays_nonfresh",
    }
)


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Keep Windows PowerShell integration contracts on Windows only.

    The node-id allowlist is deliberately exact so structural and pure-Python
    coverage in the same modules continues to execute on Linux and macOS.
    """
    if os.name == "nt":
        return

    windows_only = pytest.mark.skip(reason="Windows PowerShell integration test")
    for item in items:
        if item.nodeid in _WINDOWS_POWERSHELL_NODEIDS:
            item.add_marker(windows_only)
