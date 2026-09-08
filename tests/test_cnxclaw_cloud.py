from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from unittest import mock

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus-openclaw" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import cnxclaw as legacy_module  # noqa: E402

_ORIGINAL_PROVIDER = legacy_module.provider
_ORIGINAL_CHECKS_PROVIDER = legacy_module.checks.provider
_ORIGINAL_BASE_PROVIDER = (
    legacy_module.checks.base.provider
    if hasattr(legacy_module.checks, "base") and hasattr(legacy_module.checks.base, "provider")
    else None
)

import cnxclaw_v093 as facade  # noqa: E402

# Importing the compatibility facade intentionally narrows legacy globals for its
# process. Restore them immediately so pytest collection cannot contaminate
# historical module tests loaded before this module's fixtures execute.
legacy_module.provider = _ORIGINAL_PROVIDER
legacy_module.checks.provider = _ORIGINAL_CHECKS_PROVIDER
if _ORIGINAL_BASE_PROVIDER is not None:
    legacy_module.checks.base.provider = _ORIGINAL_BASE_PROVIDER


def test_cloud_restores_native_route_then_enters_enabled_passive_passthrough(tmp_path: Path):
    root = tmp_path / ".cogentnexus-openclaw"
    order: list[str] = []
    state = {
        "schemaVersion": 1,
        "mode": "passthrough",
        "desiredGateway": "running",
        "desiredProvider": "unchanged",
        "generation": 8,
    }

    with (
        mock.patch.object(facade.openclaw_route, "restore_native", side_effect=lambda value: order.append("route") or {"ok": True, "restored": True}) as restore,
        mock.patch.object(facade.host, "startup", side_effect=lambda *args, **kwargs: order.append("startup-disable") or subprocess.CompletedProcess([], 0, "{}", "")) as startup,
        mock.patch.object(facade.host, "remove_policy", side_effect=lambda workspace: order.append("policy-remove") or True) as remove_policy,
        mock.patch.object(facade.host, "configure_cloud_plugin", side_effect=lambda: order.append("plugin-config") or None) as configure,
        mock.patch.object(facade.host, "transition", side_effect=lambda *args, **kwargs: order.append("state") or state) as transition,
        mock.patch.object(facade.host, "plugin_enabled", side_effect=lambda enabled: order.append(f"plugin-{enabled}") or None) as plugin_enabled,
        mock.patch.object(facade.host, "openclaw_executable", return_value="openclaw"),
        mock.patch.object(facade.host, "run", side_effect=lambda *args, **kwargs: order.append("gateway-restart") or subprocess.CompletedProcess([], 0, "ok", "")) as run,
        mock.patch.object(facade.host, "runtime", side_effect=AssertionError("cloud must not enter CNX lifecycle or recovery")),
        mock.patch.object(facade.ollama_provider, "probe", side_effect=AssertionError("cloud must not probe provider")),
        mock.patch.object(facade.ollama_provider, "start", side_effect=AssertionError("cloud must not start provider")),
        mock.patch.object(facade.legacy.recovery_policy, "clear_after_manual_transition", side_effect=AssertionError("cloud must not invoke provider recovery")),
    ):
        code = facade.main(["--root", str(root), "cloud"])

    assert code == 0
    assert order == ["route", "startup-disable", "policy-remove", "plugin-config", "state", "plugin-True", "gateway-restart"]
    restore.assert_called_once_with(root.resolve())
    startup.assert_called_once_with(root.resolve(), "disable", check=True)
    remove_policy.assert_called_once_with(root.resolve().parent)
    configure.assert_called_once_with()
    transition.assert_called_once_with(
        root.resolve(), mode="passthrough", desiredGateway="running", desiredProvider="unchanged"
    )
    plugin_enabled.assert_called_once_with(True)
    run.assert_called_once_with(["openclaw", "gateway", "restart"], timeout=180, check=True)


@pytest.mark.parametrize("extra", [["--provider", "ollama"], ["--model", "gpt"], ["--credential", "secret"], ["unexpected"]])
def test_cloud_accepts_no_arguments(tmp_path: Path, extra: list[str]):
    with mock.patch.object(facade.openclaw_route, "restore_native") as restore:
        assert facade.main(["--root", str(tmp_path), "cloud", *extra]) == 2
    restore.assert_not_called()


def test_cloud_fails_closed_before_any_transition_when_route_restoration_fails(tmp_path: Path):
    root = tmp_path / ".cogentnexus-openclaw"
    with (
        mock.patch.object(facade.openclaw_route, "restore_native", return_value={"ok": False, "error": "invalid config"}),
        mock.patch.object(facade.host, "startup") as startup,
        mock.patch.object(facade.host, "remove_policy") as remove_policy,
        mock.patch.object(facade.host, "plugin_enabled") as plugin_enabled,
        mock.patch.object(facade.host, "transition") as transition,
        mock.patch.object(facade.host, "run") as run,
    ):
        assert facade.main(["--root", str(root), "cloud"]) == 1
    startup.assert_not_called()
    remove_policy.assert_not_called()
    plugin_enabled.assert_not_called()
    transition.assert_not_called()
    run.assert_not_called()


def test_cloud_fails_closed_when_route_restoration_raises(tmp_path: Path):
    with (
        mock.patch.object(facade.openclaw_route, "restore_native", side_effect=RuntimeError("route unavailable")),
        mock.patch.object(facade.host, "startup") as startup,
    ):
        assert facade.main(["--root", str(tmp_path), "cloud"]) == 1
    startup.assert_not_called()


def test_cloud_does_not_log_transition_exception_details(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    with (
        mock.patch.object(facade.openclaw_route, "restore_native", return_value={"ok": True}),
        mock.patch.object(facade.host, "startup", side_effect=RuntimeError("credential=do-not-log")),
    ):
        assert facade.main(["--root", str(tmp_path), "cloud"]) == 1
    assert "do-not-log" not in capsys.readouterr().out


def test_managed_configuration_reclaims_provider_mode_after_cloud():
    calls: list[list[str]] = []
    with (
        mock.patch.object(facade.host, "openclaw_executable", return_value="openclaw"),
        mock.patch.object(facade.host, "run", side_effect=lambda argv, **kwargs: calls.append(argv)),
    ):
        facade.host.configure_managed_plugin()

    assert [
        "openclaw",
        "config",
        "set",
        "plugins.entries.cogentnexus-openclaw.config.providerMode",
        "managed",
    ] in calls
