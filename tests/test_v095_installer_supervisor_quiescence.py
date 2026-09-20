from pathlib import Path

ROOT = Path(__file__).parents[1]
SOURCE = (ROOT / "scripts" / "install.ps1").read_text(encoding="utf-8")


def test_upgrade_handoff_prequiesces_current_supervisor_before_transactional_disable():
    assert "function Enter-ExistingSupervisorQuiescence" in SOURCE
    assert "function Wait-ExistingSupervisorQuiescence" in SOURCE
    assert "function Wait-GatewayStableForNativeHandoff" in SOURCE
    assert "scripts\\startup_v091.py" in SOURCE

    block_start = SOURCE.index("function Enter-NativeInstallBoundary")
    enter = SOURCE.index("Enter-ExistingSupervisorQuiescence", block_start)
    wait = SOURCE.index("Wait-ExistingSupervisorQuiescence", enter)
    stable = SOURCE.index("Wait-GatewayStableForNativeHandoff", wait)
    disable = SOURCE.index("& $handoffLauncher disable", stable)
    assert enter < wait < stable < disable


def test_prequiescence_waits_for_the_real_scheduled_host_process_and_is_bounded():
    start = SOURCE.index("function Wait-ExistingSupervisorQuiescence")
    end = SOURCE.index("function Wait-GatewayStableForNativeHandoff", start)
    block = SOURCE[start:end]
    assert "TimeoutSeconds" in block
    assert "Stopwatch" in block
    assert "Start-Sleep" in block
    assert "Win32_Process" in block
    assert "host_control_v092.py" in block
    assert "supervisor tick" in block
    assert "--execute-safe" in block
    assert "throw" in block


def test_gateway_stability_requires_two_successful_probes_before_handoff():
    start = SOURCE.index("function Wait-GatewayStableForNativeHandoff")
    end = SOURCE.index("function Restore-ExistingSupervisorAfterFailedHandoff", start)
    block = SOURCE[start:end]
    assert '"gateway", "health", "--json"' in block
    assert "consecutiveHealthy" in block
    assert "2" in block
    assert "TimeoutSeconds" in block


def test_failed_prequiesced_handoff_restores_supervisor_if_not_passthrough():
    start = SOURCE.index("function Enter-NativeInstallBoundary")
    end = SOURCE.index('Write-Host "Installing CogentNexus-OpenClaw', start)
    block = SOURCE[start:end]
    assert "try {" in block
    assert "catch {" in block
    assert "Restore-ExistingSupervisorAfterFailedHandoff" in block
    assert "Get-ExistingCnxMode" in block
    assert '"passthrough"' in block


def test_prequiescence_uses_installed_startup_adapter_before_launcher_disable():
    start = SOURCE.index("function Enter-ExistingSupervisorQuiescence")
    end = SOURCE.index("function Wait-ExistingSupervisorQuiescence", start)
    block = SOURCE[start:end]
    assert "$targetSkill" in block
    assert "startup_v091.py" in block
    assert '"disable"' in block
    assert "Invoke-NativeInstallerDiagnostic" in block
