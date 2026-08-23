# CNX-20260822-002 — Gateway Convergence from Clean Isolated Worktree

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Priority: current  
Predecessor: `CNX-20260822-001` (safely BLOCKED)

## Objective

Run the dedicated v0.9.3 Gateway durable-recovery convergence diagnostic on the real Windows machine from a newly created clean isolated checkout/worktree.

Determine whether the durable Gateway recovery/maintenance boundary returns to `READY` by itself after automatic Gateway restoration, without an operator `cnx start`, `cnx stop`, or `cnx restart` forcing convergence.

## Preserve the blocked worktree

The existing worktree below contains tracked test-file deletions and is outside this task's authority:

`C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-v093-test`

Do not reset, clean, stash, repair, overwrite, delete, reuse, or otherwise modify that worktree.

## Required source state

Repository: `funggier/cogentnexus`  
Coordination branch: `agent/v0.9.3-recovery-reality-tests`  
Required code ancestor: `306b091352a652a898c353aa49323c8d6a389106`  
Diagnostic: `scripts/test-v093-gateway-convergence-windows.ps1`  
Expected diagnostic Git blob: `fdaa7c49c49e529e791b3ac3db482cd3758ec470`

Documentation, coordination, report, and review commits newer than the required code ancestor are allowed.

## Clean isolated execution requirement

Create a new single-purpose clean clone or Git worktree at a new path whose leaf clearly identifies `CNX-20260822-002`. It must not reuse an existing dirty directory.

Allowed examples include a newly generated path under:

`C:\Users\CDQ-P\.openclaw\worktrees\`

The exact path may vary to avoid collision. Do not remove an existing directory merely to claim the preferred path.

Synchronize the new checkout from the current remote coordination branch using a normal non-force workflow. Before any disruptive action, verify:

1. `git merge-base --is-ancestor 306b091352a652a898c353aa49323c8d6a389106 HEAD` succeeds;
2. `git hash-object .\scripts\test-v093-gateway-convergence-windows.ps1` equals `fdaa7c49c49e529e791b3ac3db482cd3758ec470`;
3. `git status --short` is empty.

If a clean isolated checkout cannot be created without altering existing work, report `BLOCKED` and stop.

## Read-only preflight

Record all of the following before starting the diagnostic:

- repository path;
- branch/ref and `git rev-parse HEAD`;
- `git status --short`;
- required ancestor result;
- diagnostic blob SHA;
- OpenClaw version;
- Ollama version;
- `cnx.cmd status`;
- `cnx.cmd provider status --json`;
- `cnx.cmd check recovery --json`.

The baseline must be MANAGED, selected provider Ollama, Gateway listening, Ollama listening, and recovery verdict `READY`.

Do not repair an unhealthy runtime manually. If the safe baseline is absent, report `BLOCKED`.

## Authorized disruptive procedure

Run exactly:

```powershell
powershell.exe `
    -NoProfile `
    -ExecutionPolicy Bypass `
    -File .\scripts\test-v093-gateway-convergence-windows.ps1 `
    -RunDisruptive
```

Answer `y` only when the diagnostic displays its explicit exact-Gateway-PID confirmation:

```text
This will hard-kill the exact validated OpenClaw Gateway PID once. Type y to continue
```

After confirmation, do not intervene while the diagnostic observes listener recovery and durable convergence.

The diagnostic's own best-effort cleanup path is allowed if the diagnostic fails.

## Safety invariants

- Kill only the exact Gateway PID validated by the diagnostic.
- Never use `taskkill /T` or another process-tree kill.
- Do not manually terminate any process outside the diagnostic.
- Do not stop or restart Firefox, PowerShell, cmd, conhost, Explorer, Windows Terminal, OpenConsole, or unrelated processes.
- Do not run the original unsafe Recovery Reality harness.
- Do not run the v3 full disruptive suite.
- Do not modify CogentNexus runtime/source or the diagnostic.
- Do not modify OpenClaw/Ollama configuration.
- Do not install or uninstall software.
- Do not manually issue `cnx start`, `cnx stop`, or `cnx restart` to influence the result.

## Evidence collection

Locate the newest evidence pair produced by this run:

```text
%USERPROFILE%\Downloads\CNX_V093_GATEWAY_CONVERGENCE_*.txt
%USERPROFILE%\Downloads\CNX_V093_GATEWAY_CONVERGENCE_*.json
```

Read both files and calculate SHA256 for each.

## PASS criteria

PASS requires all of the following:

- clean isolated checkout and clean initial Git status;
- initial MANAGED/Ollama/`READY` baseline;
- exact OpenClaw Gateway `node.exe` listener PID validated;
- only that exact PID hard-killed;
- Gateway listener returns with a different PID;
- without a manual runtime transition command, repeated read-only recovery checks reach `READY` within the observation fuse;
- final state remains MANAGED;
- selected provider remains Ollama;
- Gateway and Ollama are listening;
- diagnostic JSON records `result = PASS`;
- evidence TXT/JSON paths and SHA256 hashes are recorded.

## FAIL criteria

Report FAIL when the diagnostic runs safely but disproves a required behavior, including failure of Gateway restoration, failure of durable convergence inside the observation fuse, failure to restore the final managed baseline, or JSON `result = FAIL`.

Do not convert FAIL into PASS through manual intervention.

## BLOCKED criteria

Report BLOCKED without disruptive execution if the isolated checkout is not clean, required ancestor/blob differs, baseline is unsafe, exact target identity cannot be validated, or another safety precondition is not satisfied.

## Report contract

Write:

`docs/operations/coordination/reports/CNX-20260822-002-gateway-convergence.md`

Include:

- isolated repository/worktree path;
- source branch/ref and execution HEAD;
- initial Git status;
- ancestor and diagnostic blob verification;
- complete preflight classification;
- diagnostic exit code;
- old Gateway PID and validated identity;
- recovered Gateway PID;
- first and final durable recovery verdict;
- convergence attempts and elapsed seconds;
- final mode/provider/Gateway/Ollama state;
- TXT/JSON paths and SHA256 hashes;
- diagnostic cleanup action, if any;
- everything skipped or unproven.

Commit and push only the report file plus no source/runtime changes. Use a commit message beginning:

`report: CNX-20260822-002`

If the remote coordination branch advances, integrate normally without force-pushing or rewriting another commit. Stop after publishing the report and wait for ChatGPT review.
