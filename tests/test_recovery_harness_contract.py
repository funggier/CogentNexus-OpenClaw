from __future__ import annotations

from pathlib import Path


HARNESS = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "test-v093-ollama-recovery-windows-v3.ps1"
)


def _provider_recovery_converged(observation: dict[str, object]) -> bool:
    """Behavioral contract for the provider-crash convergence gate."""
    incident = observation["providerRecoveryIncident"]
    adapter = observation["providerEventAdapter"]
    return (
        observation["mode"] == "managed"
        and observation["hostSelectedProvider"] == "ollama"
        and observation["selectedProvider"] == "ollama"
        and observation["recoveryVerdict"] in {"READY", "READY_WITH_WARNINGS"}
        and adapter["details"]["expected"] is False
        and observation["gateway"]["listening"] is True
        and observation["ollama"]["listening"] is True
        and incident["details"]["circuitOpen"] is False
        and incident["details"]["incidentOpen"] is True
    )


def test_provider_crash_convergence_accepts_recovered_open_incident_state():
    observation = {
        "mode": "managed",
        "hostSelectedProvider": "ollama",
        "selectedProvider": "ollama",
        "recoveryVerdict": "READY_WITH_WARNINGS",
        "providerEventAdapter": {"details": {"expected": False}},
        "gateway": {"listening": True},
        "ollama": {"listening": True},
        "providerRecoveryIncident": {
            "details": {"circuitOpen": False, "incidentOpen": True}
        },
    }

    assert _provider_recovery_converged(observation)


def test_harness_accepts_recovered_open_incident_warning_state():
    source = HARNESS.read_text()
    assert "($RequireProviderIncident -and $observation.recoveryVerdict -eq 'READY_WITH_WARNINGS')" in source
