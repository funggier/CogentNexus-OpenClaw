# CNX-20260822-003 — Restore Gateway Baseline and Retry Convergence

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Priority: current  
Predecessor: `CNX-20260822-002` (safely BLOCKED)

## Objective

Restore the real Windows machine to a verified MANAGED/Ollama/Gateway/`READY` baseline using one explicitly authorized baseline `cnx start` when necessary, then run the focused Gateway durable-recovery convergence diagnostic.

The result must still prove or disprove post-crash natural convergence without using any manual runtime transition after failure injection.

## Source and worktree

Repository: `funggier/cogentnexus`  
Coordination branch: `agent/v0.9.3-recovery-reality-tests`  
Required code ancestor: `306b091352a652a898c353aa49323c8d6a389106`  
Diagnostic: `scripts/test-v093-gateway-convergence-windows.ps1`  
Expected diagnostic blob: `fdaa7c49c49e529e791b3ac3db482cd3758ec470`

Use a clean isolated checkout/worktree. The Task 002 isolated worktree may be reused only if it is still present, safely synchronized, and `git status --short` is empty. Otherwise create a new isolated worktree.

Do not modify, clean, reset, stash, delete, or reuse:

`C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-v093-test`

Before runtime actions, verify the required ancestor, exact diagnostic blob, and clean Git status.

## Phase A — Read-only baseline classification

Record:

- repository/worktree path, ref, HEAD, and Git status;
- OpenClaw and Ollama versions;
- `cnx.cmd status`;
- `cnx.cmd provider status --json`;
- `cnx.cmd check recovery --json`;
- Gateway scheduled-task state, listener state, and listener PID if present;
- Ollama listener state and PID.

Explicitly record whether recovery verdict `READY` agrees with actual Gateway health.

## Phase B — Authorized baseline restoration

If Gateway is not healthy/listening while desired state is running, run exactly one operator baseline transition:

```powershell
.\cnx.cmd start
```

This `cnx start` is authorized only before failure injection. Capture its exit code and output.

Then use bounded read-only observation to verify:

- mode MANAGED;
- desired Gateway/provider running;
- selected provider Ollama;
- Gateway scheduled task running;
- Gateway listening on 127.0.0.1:18789;
- Ollama listening on 127.0.0.1:11434;
- `cnx check recovery --json` verdict `READY`.

The observation bound is a test fuse only.

If a stable healthy baseline does not appear, report `BLOCKED`. Do not kill any process and do not improvise additional repair commands.

If the baseline was already healthy, do not issue `cnx start`.

## Phase C — Exact convergence diagnostic

After the healthy baseline is recorded, run exactly:

```powershell
powershell.exe `
    -NoProfile `
    -ExecutionPolicy Bypass `
    -File .\scripts\test-v093-gateway-convergence-windows.ps1 `
    -RunDisruptive
```

Answer `y` only at the diagnostic's explicit confirmation to hard-kill the exact validated OpenClaw Gateway PID once.

After injection:

- do not issue manual `cnx start`, `cnx stop`, or `cnx restart`;
- do not intervene while the script observes the replacement listener and durable convergence;
- allow only the diagnostic's documented best-effort cleanup after it has classified the result.

## Safety invariants

- exact validated Gateway PID only;
- no process-tree kill or `taskkill /T`;
- no manual process termination outside the diagnostic;
- protect Firefox, PowerShell, cmd, conhost, Explorer, Windows Terminal/OpenConsole, the harness, and harness ancestors;
- do not run the original unsafe harness or v3 full disruptive suite;
- do not modify runtime/source, the diagnostic, OpenClaw configuration, or Ollama configuration;
- do not install or uninstall software in this task;
- do not conceal a failed or skipped observation.

## PASS criteria

PASS requires:

- clean source/worktree gates;
- healthy initial baseline, whether already present or restored by the one authorized pre-injection `cnx start`;
- exact Gateway `node.exe` listener PID identity validated;
- only that exact PID hard-killed;
- replacement Gateway listener appears with a different PID;
- without any post-injection manual runtime transition, durable recovery reaches `READY` inside the observation fuse;
- final state remains MANAGED with Ollama selected and both listeners healthy;
- diagnostic JSON records `result = PASS`;
- TXT/JSON evidence paths and SHA256 hashes are recorded.

## FAIL criteria

Report FAIL if the diagnostic runs safely and disproves required recovery/convergence behavior. Never convert FAIL to PASS through manual intervention.

## BLOCKED criteria

Report BLOCKED before injection if source gates fail, baseline restoration fails, exact target identity is unsafe, or another precondition cannot be met safely.

## Evidence and report

Collect the newest:

```text
%USERPROFILE%\Downloads\CNX_V093_GATEWAY_CONVERGENCE_*.txt
%USERPROFILE%\Downloads\CNX_V093_GATEWAY_CONVERGENCE_*.json
```

Calculate SHA256 for both when produced.

Write:

`docs/operations/coordination/reports/CNX-20260822-003-gateway-convergence.md`

Include all source gates, initial mismatch classification, whether the one pre-injection `cnx start` was used, stable baseline evidence, diagnostic exit code, old/new Gateway PIDs, first/final recovery verdicts, convergence attempts/time, final runtime state, evidence hashes, cleanup, and everything unproven.

Commit and push only the matching report plus changes explicitly authorized by this task. Use a commit message beginning:

`report: CNX-20260822-003`

Never force-push. Stop after the report is published.
