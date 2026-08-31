import importlib.util
import subprocess
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
VALIDATE = ROOT / "skills" / "cogentnexus-openclaw" / "scripts" / "validate.py"


def _load_validate():
    spec = importlib.util.spec_from_file_location("cnx_validate_under_test", VALIDATE)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_windows_validate_retries_known_detached_controller_teardown_race_once():
    module = _load_validate()
    first = subprocess.CompletedProcess(
        args=["workflow.py", "self-test"],
        returncode=1,
        stdout="",
        stderr=(
            'File "workflow.py", line 589, in self_test\n'
            'assert Workflow(root,"WF-TEST-SUPERVISE").state()["status"]=="completed" '
            "and not process_alive(child_pid)\n"
            "AssertionError\n"
        ),
    )
    second = subprocess.CompletedProcess(
        args=["workflow.py", "self-test"],
        returncode=0,
        stdout="Cogent workflow self-test: PASS\n",
        stderr="",
    )

    with (
        mock.patch.object(module.sys, "platform", "win32"),
        mock.patch.object(module.subprocess, "run", side_effect=[first, second]) as run,
        mock.patch.object(module.time, "sleep") as sleep,
    ):
        module.run_workflow_self_test()

    assert run.call_count == 2
    sleep.assert_called_once_with(1.0)
