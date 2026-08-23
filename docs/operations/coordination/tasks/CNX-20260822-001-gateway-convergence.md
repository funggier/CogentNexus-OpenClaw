# CNX-20260822-001 — Gateway Durable Recovery Convergence

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Priority: current  

## Objective

Determine whether CogentNexus v0.9.3 clears its durable Gateway recovery/maintenance boundary by itself after an unplanned OpenClaw Gateway hard crash, without an operator `cnx start` being used to force convergence.

This task exists to distinguish two possibilities:

1. the v3 full-suite assertion ran too early and the runtime eventually converges correctly; or
2. the Gateway listener recovers but the durable maintenance/recovery marker remains stuck, which is a runtime recovery defect.

## Required source state

Repository:

```text
funggier/cogentnexus
```

Branch:

```text
agent/v0.9.3-recovery-reality-tests
```

Required code ancestor:

```text
306b091352a652a898c353aa49323c8d6a389106
```

Required diagnostic file:

```text
scripts/test-v093-gateway-convergence-windows.ps1
```

Expected Git blob SHA for that diagnostic:

```text
fdaa7c49c49e529e791b3ac3db482cd3758ec470
```

Documentation/coordination commits newer than the required code ancestor are allowed.

Before execution, verify:

```powershell
$Required = '306b091352a652a898c353aa49323c8d6a389106'
git merge-base --is-ancestor $Required HEAD
if ($LASTEXITCODE -ne 0) { throw 'Required code baseline is not an ancestor of HEAD.' }

$Blob = (git hash-object .\scripts\test-v093-gateway-convergence-windows.ps1).Trim()
if ($Blob -ne 'fdaa7c49c49e529e791b3ac3db482cd3758ec470') {
    throw "Gateway convergence diagnostic blob mismatch: $Blob"
}
```

## Preconditions

Record, but do not repair, all of the following before the disruptive run:

- repository path;
- branch;
- `git rev-parse HEAD`;
- `git status --short`;
- OpenClaw version;
- Ollama version;
- `cnx.cmd status`;
- `cnx.cmd provider status --json`;
- `cnx.cmd check recovery --json`.

The diagnostic itself will enforce the managed/Ollama/READY baseline before killing anything.

If the repository has unrelated uncommitted modifications, do not discard, reset, stash, or overwrite them. Report `BLOCKED` unless they are clearly only generated evidence files outside the repository and do not affect the task.

## Allowed actions

- fetch the target branch;
- update the local checkout to the current remote branch head using a safe fast-forward or detached exact-head workflow;
- read repository files;
- run read-only preflight commands;
- execute the exact Gateway convergence diagnostic below;
- answer `y` only to the diagnostic's explicit exact-Gateway-PID disruptive confirmation;
- read the produced TXT/JSON evidence;
- calculate SHA256 for evidence files;
- create the matching report under `docs/operations/coordination/reports/`;
- commit and push only the report file (plus no other source/runtime changes).

The diagnostic's own best-effort cleanup path is allowed if the diagnostic fails.

## Forbidden actions

Do not:

- modify CogentNexus runtime/source code;
- modify the diagnostic script;
- modify OpenClaw or Ollama configuration;
- install/uninstall software;
- kill any process manually outside the diagnostic;
- use `taskkill /T` or any process-tree kill;
- stop/restart Firefox, PowerShell, cmd, Explorer, Windows Terminal, OpenConsole, or unrelated processes;
- run the older unsafe Recovery Reality harness;
- run the v3 full disruptive suite for this task;
- call `cnx start`, `cnx stop`, or `cnx restart` manually to make the result pass;
- conceal a failed or skipped required observation.

## Procedure

1. Fetch the current coordination branch.
2. Ensure the current checkout contains required code ancestor `306b091352a652a898c353aa49323c8d6a389106`.
3. Verify the diagnostic blob SHA exactly.
4. Record source/preflight state.
5. Run exactly:

```powershell
powershell.exe `
    -NoProfile `
    -ExecutionPolicy Bypass `
    -File .\scripts\test-v093-gateway-convergence-windows.ps1 `
    -RunDisruptive
```

6. When and only when the script asks:

```text
This will hard-kill the exact validated OpenClaw Gateway PID once. Type y to continue
```

answer:

```text
y
```

7. Do not intervene while the script observes Gateway recovery and durable convergence.
8. Locate the newest matching evidence pair:

```text
%USERPROFILE%\Downloads\CNX_V093_GATEWAY_CONVERGENCE_*.txt
%USERPROFILE%\Downloads\CNX_V093_GATEWAY_CONVERGENCE_*.json
```

9. Read both evidence files and calculate SHA256 for both.
10. Write the execution report to:

```text
docs/operations/coordination/reports/CNX-20260822-001-gateway-convergence.md
```

11. Commit and push the report file only. Use a commit message beginning with:

```text
report: CNX-20260822-001
```

If the branch advanced while the test was running, fetch/rebase or otherwise integrate safely without rewriting other people's commits. Do not force-push.

## PASS criteria

PASS requires all of the following evidence:

- initial managed Ollama baseline is READY;
- the diagnostic validates the exact OpenClaw Gateway `node.exe` listener PID before termination;
- only that exact PID is hard-killed;
- Gateway listener returns with a different PID;
- without manual `cnx start`, `cnx stop`, or `cnx restart`, repeated read-only `cnx check recovery --json` observations eventually return `READY` inside the observation fuse;
- final state remains MANAGED;
- selected provider remains Ollama;
- Gateway is listening;
- Ollama is listening;
- diagnostic JSON records `result = PASS`;
- required evidence TXT/JSON hashes are recorded in the report.

## FAIL criteria

Report FAIL if execution completes but any required behavior is disproven, including:

- Gateway does not return;
- durable recovery never converges to READY inside the observation fuse;
- final managed baseline is not restored;
- the diagnostic itself records `result = FAIL`.

Do not convert FAIL into PASS by manually issuing a recovery command.

## BLOCKED criteria

Report BLOCKED without disruptive execution if:

- required source ancestor is absent;
- diagnostic blob differs from the expected blob;
- repository state cannot be updated safely;
- initial environment cannot be inspected safely;
- the script's target identity validation would not allow a safe exact-PID test;
- another condition makes the requested test unsafe.

## Evidence required

The report must include:

- repository path;
- branch and HEAD used for execution;
- required ancestor verification result;
- diagnostic blob SHA;
- initial `git status --short`;
- diagnostic exit code;
- old Gateway PID and validated process identity;
- recovered Gateway PID;
- first durable recovery verdict observed after listener recovery;
- final durable recovery verdict;
- convergence attempts and elapsed seconds if present in JSON evidence;
- final Gateway/Ollama listener states;
- TXT evidence path + SHA256;
- JSON evidence path + SHA256;
- any cleanup action performed by the diagnostic;
- everything that was not executed or remains unproven.

## Report destination

```text
docs/operations/coordination/reports/CNX-20260822-001-gateway-convergence.md
```

Do not edit this task file to record progress or results.
