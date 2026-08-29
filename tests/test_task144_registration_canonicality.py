import importlib.util
import os
from pathlib import Path
import subprocess

import pytest


TASK143_TEST = Path(__file__).with_name("test_task143_direct_in_place_finalization.py")
SPEC = importlib.util.spec_from_file_location("task144_task143_fixture", TASK143_TEST)
assert SPEC and SPEC.loader
task143 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(task143)
ownership = task143.ownership


@pytest.mark.skipif(os.name == "nt", reason="POSIX symlink alias proof")
def test_direct_same_path_rejects_in_state_symlink_registration_alias(tmp_path: Path):
    paths, candidate, transaction, _, _ = task143._prepare_direct_transition(tmp_path)
    alias = paths["openclaw_state"] / "extensions" / f"{ownership.PRODUCT_ID}-registration-alias"
    os.symlink(paths["direct"], alias, target_is_directory=True)
    task143._replace_payload(paths["direct"], candidate)

    assert alias != paths["direct"]
    assert alias.resolve() == paths["direct"].resolve()

    with pytest.raises(RuntimeError, match="canonical|registration|alias"):
        ownership.finalize_plugin_rollover_transaction(
            transaction=transaction,
            plugin_inventory=task143._inventory(paths, alias),
        )


@pytest.mark.skipif(os.name == "nt", reason="POSIX symlink alias proof")
def test_direct_same_path_rejects_outside_state_symlink_registration_alias(tmp_path: Path):
    paths, candidate, transaction, _, _ = task143._prepare_direct_transition(tmp_path)
    alias = tmp_path / f"{ownership.PRODUCT_ID}-outside-registration-alias"
    os.symlink(paths["direct"], alias, target_is_directory=True)
    task143._replace_payload(paths["direct"], candidate)

    assert alias != paths["direct"]
    assert paths["openclaw_state"] not in alias.parents
    assert alias.resolve() == paths["direct"].resolve()

    with pytest.raises(RuntimeError, match="canonical|registration|alias"):
        ownership.finalize_plugin_rollover_transaction(
            transaction=transaction,
            plugin_inventory=task143._inventory(paths, alias),
        )


@pytest.mark.skipif(os.name != "nt", reason="Windows junction alias proof")
def test_direct_same_path_rejects_windows_junction_registration_alias(tmp_path: Path):
    paths, candidate, transaction, _, _ = task143._prepare_direct_transition(tmp_path)
    alias = paths["openclaw_state"] / "extensions" / f"{ownership.PRODUCT_ID}-registration-junction"

    result = subprocess.run(
        ["cmd.exe", "/c", "mklink", "/J", str(alias), str(paths["direct"])],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"unable to create Windows junction alias: {result.stdout}{result.stderr}")

    task143._replace_payload(paths["direct"], candidate)
    assert alias != paths["direct"]
    assert alias.resolve() == paths["direct"].resolve()

    with pytest.raises(RuntimeError, match="canonical|registration|alias"):
        ownership.finalize_plugin_rollover_transaction(
            transaction=transaction,
            plugin_inventory=task143._inventory(paths, alias),
        )
