# v0.9.3 Ollama-only Recovery Reality Tests

CogentNexus v0.9.3 intentionally narrows local inference support to **Ollama only**.

The released v0.9.2 remains immutable and may still contain LM Studio compatibility code because it was part of that historical release.  v0.9.3 does not select, start, stop, probe, advertise, or test LM Studio.  An upgrade from a managed v0.9.2 deployment first enters the accepted PASSTHROUGH/native boundary with the old launcher, then v0.9.3 enters MANAGED with Ollama.

LM Studio, if separately installed on a user's machine, is left untouched.

## Why the provider surface is being narrowed

- reduce steady-state RAM pressure and operational complexity;
- remove a second recovery/event-adapter path that exhibited the same core failure classes;
- make recovery evidence easier to classify and reproduce;
- concentrate v0.9.3 engineering on execution continuity rather than provider breadth.

## Windows harness

Entry point:

```powershell
.\scripts\test-v093-recovery-reality-windows.ps1
```

Evidence is written to `Downloads` as:

- `CNX_V093_OLLAMA_RECOVERY_<timestamp>.txt`
- `CNX_V093_OLLAMA_RECOVERY_<timestamp>.json`
- `CNX_V093_OLLAMA_RECOVERY_<timestamp>\` for downloaded v0.9.2 release material when `-InstallRelease` is used.

A top-level PASS is not authoritative by itself.  Scenario assertions, exact listener PIDs, process identity, durable CNX diagnostics, and bounded observations are persisted in JSON.

## Safety model

Recovery remains event-driven. Harness timeouts are **observation fuses only** and never authorize recovery.

For disruptive scenarios:

- exact lowercase `y` is required once before any failure injection;
- only the exact listener PID is eligible for force-kill;
- Gateway PID must resolve to `node.exe` with an OpenClaw command line;
- provider PID must resolve to an Ollama process/command line;
- PowerShell, cmd, conhost, Firefox, Explorer, Windows Terminal/OpenConsole and harness ancestor PIDs are explicitly forbidden kill targets;
- process-tree kill is never used;
- active operation + child/target PID evidence is committed before blocking waits or failure injection;
- the harness never calls `reset` or `uninstall`.

## Consumer-path setup

With `-InstallRelease`, the harness exercises the real public `v0.9.2` release before recovery testing:

1. fetch release metadata;
2. require the exact accepted release target commit;
3. download `cogentnexus-v0.9.2.zip` and `SHA256SUMS.txt`;
4. verify ZIP SHA256;
5. extract the archive;
6. run the released installer explicitly with `-Provider ollama`;
7. verify MANAGED + Ollama before injecting failures.

This deliberately requires no existing `~\.openclaw\workspace\cnx.cmd`.

## Scenario 0 — MANAGED baseline

Require:

- controller mode `managed`;
- durable `selectedProvider=ollama`;
- Gateway listener present;
- Ollama listener on `11434` present;
- LM Studio provider-event adapter is **not expected**.

## Scenario 1 — Gateway hard crash

1. capture Gateway listener PID and full process identity;
2. reject unsafe/unverified targets;
3. force-kill that exact PID only;
4. observe a replacement listener with a different PID;
5. require MANAGED + Ollama again.

## Scenario 2 — Ollama hard crash

1. capture listener PID on `11434` and full process identity;
2. reject unsafe/unverified targets;
3. force-kill that exact PID only;
4. observe a replacement Ollama listener with a different PID;
5. inspect the durable provider-recovery incident row;
6. fail if the recovery circuit is already open after one injected crash;
7. require MANAGED + Ollama again.

## Scenario 3 — intentional operator stop

1. call `cnx stop`;
2. require `mode=maintenance`, `desiredGateway=stopped`, `desiredProvider=stopped`;
3. require the Gateway to remain down through a bounded observation window;
4. call `cnx start`;
5. require Gateway + Ollama + MANAGED state again.

## Intended first live run

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\scripts\test-v093-recovery-reality-windows.ps1 `
  -InstallRelease `
  -Scenario all `
  -RunDisruptive
```

No provider argument is needed because v0.9.3 is Ollama-only.

## Next continuity scenarios

After the process-level suite is stable, extend the same harness with deterministic Ticket/model-call fixtures for:

- Gateway death while a model call is active;
- Ollama death while a model call is active;
- healthy Ollama + long silent model processing (must not restart);
- Host death/restart and durable reconciliation;
- committed result but interrupted delivery (deliver existing result, never re-infer merely because delivery broke);
- abrupt process/power-loss simulation with a pending Ticket;
- real Windows reboot continuation using durable resume state.
