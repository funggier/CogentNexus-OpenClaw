# v0.9.3 Recovery Reality Tests

This document defines the first automated live-recovery test surface for the v0.9.3 development cycle. The product baseline remains the released and verified CogentNexus v0.9.2; these tests do not modify the v0.9.2 release.

## Harness

Windows entry point:

```powershell
.\scripts\test-v093-recovery-reality-windows.ps1
```

Evidence is written under `Downloads` as:

- `CNX_V093_RECOVERY_REALITY_<timestamp>.txt`
- `CNX_V093_RECOVERY_REALITY_<timestamp>.json`
- `CNX_V093_RECOVERY_REALITY_<timestamp>\` for downloaded consumer-release material when `-InstallRelease` is used.

The harness follows the same evidence discipline as the v0.9.2 acceptance suite: a top-level PASS is not authoritative by itself; scenario assertions and durable/runtime observations are persisted in JSON.

## Safety model

The recovery system remains event-driven. Harness timeouts are **observation fuses only**. They never authorize recovery, restart, re-inference, Ticket claiming, or external side effects.

Failure injection is explicit:

- `baseline` is read-only except for normal diagnostic commands.
- `gateway-crash`, `provider-crash`, and `operator-stop` require `-RunDisruptive`.
- A disruptive suite also requires one exact lowercase `y` confirmation before any process is killed.
- The harness does not call `reset` or `uninstall`.
- On a failed disruptive scenario it attempts a bounded `cnx start --provider <selected>` reconciliation and records whether cleanup succeeded.

## Optional release-consumer setup

`-InstallRelease` exercises the real public-release path before recovery testing:

1. fetch GitHub Release metadata for `v0.9.2`;
2. require a published non-draft, non-prerelease release;
3. require the expected release target commit;
4. download `cogentnexus-v0.9.2.zip` and `SHA256SUMS.txt`;
5. verify the ZIP SHA256;
6. extract the archive;
7. verify `VERSION` matches the tag;
8. run the released `scripts/install.ps1 -Provider <provider>`;
9. verify a MANAGED baseline.

This mode intentionally requires that `~\.openclaw\workspace\cnx.cmd` does not already exist, because its purpose is to test a clean consumer installation rather than silently mutate an existing deployment.

## Scenario 0 — baseline

Verify before any failure injection:

- CNX controller mode is `managed`;
- durable `selectedProvider` matches the requested provider;
- OpenClaw Gateway listener exists;
- selected provider listener exists;
- LM Studio provider-event adapter is expected and running when LM Studio is selected;
- Ollama does not require the LM Studio provider-event adapter.

## Scenario 1 — Gateway hard crash

1. capture Gateway listener port/PID/process name;
2. force-kill only that listener process;
3. observe for a replacement Gateway listener with a different PID;
4. re-run CNX status/provider/recovery diagnostics;
5. require the controller to remain MANAGED with the same selected provider.

This tests an unplanned process death, not `cnx gateway stop` and not an operator-requested stop.

## Scenario 2 — provider hard crash

1. capture selected provider listener PID (`1234` LM Studio or `11434` Ollama);
2. force-kill only the listening process;
3. observe for a replacement listener with a different PID;
4. require durable `selectedProvider` to remain unchanged;
5. inspect the durable provider-recovery incident diagnostic;
6. fail if the circuit is already open after one injected provider crash;
7. re-establish the full MANAGED baseline.

This is the first direct reality check that process/endpoint failure can drive recovery without using elapsed model-call silence as authority.

## Scenario 3 — intentional operator stop

1. call `cnx stop` normally;
2. require durable state `mode=maintenance`, `desiredGateway=stopped`, `desiredProvider=stopped`;
3. observe the Gateway listener disappear;
4. keep an observation window open and require it to stay down — CNX must **not** auto-recover an intentional stop;
5. call `cnx start`;
6. observe Gateway/provider listeners return;
7. require the MANAGED baseline again.

## Initial run

For a clean machine after v0.9.2 uninstall, the intended first run is:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\scripts\test-v093-recovery-reality-windows.ps1 `
  -Provider lmstudio `
  -InstallRelease `
  -Scenario all `
  -RunDisruptive
```

The user must still type exact lowercase `y` once before the disruptive scenarios begin.

## Planned next scenarios

The first harness deliberately stops before model-call/side-effect continuity. After the process-level suite is proven stable, extend it with durable Ticket fixtures for:

- Gateway death while a model call is active;
- provider death while a model call is active;
- healthy provider + long silent prefill (must not restart);
- Host death/restart and durable reconciliation;
- result committed but delivery interrupted (deliver existing result, do not re-infer);
- abrupt process-tree/power-loss simulation with pending Ticket state;
- real Windows reboot continuation using a durable resume token and Scheduled Task.

Those scenarios require deterministic Ticket/model-call fixtures so that the harness can prove exactly-once-ish side-effect and result/delivery boundaries rather than merely observing process liveness.
