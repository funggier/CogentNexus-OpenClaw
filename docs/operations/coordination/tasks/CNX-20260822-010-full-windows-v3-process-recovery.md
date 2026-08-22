# CNX-20260822-010 — Full Real-Windows V3 Process-Recovery Suite

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Priority: current  
Predecessor: `CNX-20260822-009` (ACCEPT; complete clean checkout procedure proven)

## Objective

Run the accepted v3 Ollama-only process-recovery suite exactly once on the real Windows target from a newly created complete clean isolated clone, and preserve complete evidence for:

1. healthy MANAGED/Ollama baseline;
2. exact-PID OpenClaw Gateway hard crash and natural durable convergence;
3. exact-PID Ollama listener hard crash, provider-incident evidence, and natural durable convergence;
4. intentional `cnx stop` remaining stopped;
5. one documented `cnx start` returning to MANAGED/Ollama/`READY`.

This task authorizes only this process-level recovery run. It does not authorize install, reset, uninstall, reinstall, source edits, tag, merge, or release actions.

## Predecessor and one-time authorization

Task 008 is permanently `BLOCKED`: its single PowerShell command attempt exited before the harness loaded because that checkout lacked the physical script. No scenario, process kill, confirmation, `cnx stop`/`cnx start`, evidence generation, or runtime/lifecycle mutation occurred.

Task 009 is accepted. It proved that a new full isolated clone at an exact synchronized HEAD is clean, contains the exact harness blob, and passes parser plus `-SyntaxOnly`.

Task 010 is the sole new authorization for one disruptive suite invocation. Do not resume Tasks 007 or 008. Do not execute anything if a matching Task 010 report already exists.

## Duplicate-execution fence

Before inspecting an existing checkout, creating a new clone, observing CI or Windows state, asking for confirmation, or performing any other local action, fetch the branch and check for:

`docs/operations/coordination/reports/CNX-20260822-010-full-windows-v3-process-recovery.md`

If it exists, perform no local action and stop awaiting ChatGPT review.

## Immutable source

Repository: `funggier/cogentnexus`  
Branch: `agent/v0.9.3-recovery-reality-tests`  
Accepted Task 009 report commit: `3a1062b9f217b86c23f793b47befad5c7d39505c`  
Accepted Task 009 review commit: `6356ca9e06c6d28003b9f861f5fd3a15a3496e41`  
Required accepted validation ancestor: `5a22d9479ad7d62c7a159e4b49e2bc3f79fb6171`  
Required harness implementation ancestor: `592a6fbd37da05013b7a8a5875ccd8b17e188cfa`  
Required workflow-fix ancestor: `929fbcc663251941d88f38f09544068a9b3e069d`  
Harness: `scripts/test-v093-ollama-recovery-windows-v3.ps1`  
Required harness blob: `6d4c9347de12bbe4e3e5c428f2fe80333f92757f`  
Task 009 harness SHA256: `5F2DBA46602CA88113B21A0DB8B729BC5AB8DA5FC45E9356F4072DDDD31E929F`  
Task 009 harness size: `18782` bytes

Later ChatGPT-owned coordination/documentation commits are allowed.

Read every literal SHA directly from this task and compare byte-for-byte. Do not concatenate, shorten, autocomplete, substitute, or reconstruct a SHA from memory or another commit. If a literal differs from the fetched task, report `BLOCKED` before any Windows runtime action.

## Exact clean-checkout procedure

After the duplicate fence:

1. Fresh-fetch `origin/agent/v0.9.3-recovery-reality-tests`.
2. Record the exact Task 010 start HEAD.
3. Verify the Task 009 report/review commits and all three required implementation ancestors are ancestors of that start HEAD.
4. Obtain the existing configured origin URL without exposing credentials.
5. Choose one new unique previously nonexistent Task 010 directory under the established CogentNexus worktree/checkout parent.
6. Create a full isolated clone using `git clone --no-local <redacted-origin> <new-task-010-path>`.
7. Detach the new clone at the exact Task 010 start HEAD.
8. Do not use sparse checkout. Do not reuse, modify, repair, reset, clean, delete, or prune any existing Task 007, 008, or 009 checkout/worktree.
9. If the destination already exists, report `BLOCKED`; do not delete or reuse it.

In the new clone, before CI or runtime action, prove and record:

- `git rev-parse HEAD` equals the exact Task 010 start HEAD;
- `git status --porcelain=v1` is empty;
- `git diff --name-only --diff-filter=D` is empty;
- the harness is tracked and is a physical leaf at the exact relative path;
- `git rev-parse HEAD:scripts/test-v093-ollama-recovery-windows-v3.ps1` equals the required blob;
- file SHA256 equals the Task 009 value and byte size equals `18782`;
- PowerShell parser validation returns zero errors;
- the exact load-only command exits 0:
  `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test-v093-ollama-recovery-windows-v3.ps1 -SyntaxOnly`;
- the checkout remains clean after validation.

If any checkout/source/load gate fails, report `BLOCKED` without Windows runtime preflight or the disruptive command.

## CI precondition

Before the disruptive command, use bounded read-only observation until all applicable workflows for the exact Task 010 start HEAD complete.

Every required workflow must conclude `success`. Do not run the disruptive suite if any workflow is failed, cancelled, unexpectedly skipped, or still in progress. Do not manually rerun workflows.

Record the complete workflow name, run ID, status, and conclusion table. Superseded duplicate runs may be recorded separately but may not substitute for one successful applicable run per required workflow.

## Read-only real-Windows preflight

Before confirmation or injection, record exact commands, exit codes, and output/evidence for:

- `openclaw.cmd --version`;
- `openclaw.cmd config validate`;
- `ollama.exe --version`;
- installed `%USERPROFILE%\.openclaw\workspace\cnx.cmd` path and SHA256;
- `cnx.cmd status`;
- `cnx.cmd provider status --json`;
- `cnx.cmd check recovery --json`, with exit code 0 or 1 recorded;
- Gateway listener on the configured port, normally `127.0.0.1:18789`;
- Ollama listener on `127.0.0.1:11434`;
- exact listener PIDs, process names, executable paths, parent PIDs, and command lines.

Preflight must show:

- Host mode `managed`;
- Host and provider selected provider `ollama`;
- recovery verdict `READY`;
- Gateway and Ollama listeners healthy;
- Gateway PID resolves to the OpenClaw `node.exe` role;
- Ollama PID resolves to Ollama;
- neither target is the harness, a harness ancestor, or a protected process.

If preflight is not healthy, report `BLOCKED`. Do not use `cnx start` or another mutation to manufacture a passing precondition.

## Exact authorized command

From the newly proven Task 010 clone, run exactly once:

`powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test-v093-ollama-recovery-windows-v3.ps1 -Scenario all -RunDisruptive`

When prompted, type exact lowercase `y` once.

Do not invoke the suite a second time under any outcome. Do not manually repeat any scenario.

## Immutable injection safety

- only the exact validated listener PID may be force-killed;
- process-tree kill is forbidden;
- never kill PowerShell, pwsh, cmd, conhost, Firefox, Explorer, Windows Terminal, OpenConsole, the harness, or a harness ancestor;
- persist active-operation and target identity evidence before each injection;
- Gateway target must be validated as OpenClaw `node.exe`;
- provider target must be validated as Ollama;
- no manual `cnx start`, `cnx stop`, or other runtime transition is allowed between a hard crash and its natural convergence verdict;
- timeouts are observation fuses only, never recovery authority.

If target identity is ambiguous or unsafe, the harness must refuse the kill and the report must record `BLOCKED` or `FAIL`; do not improvise.

## Required scenario evidence

### Baseline

Record MANAGED mode, Ollama selection, Gateway/Ollama listener identities, recovery verdict `READY`, and provider-adapter expectation.

### Gateway crash

Record:

- exact old Gateway PID and validated identity;
- exact kill method `Stop-Process exact PID only`;
- different replacement Gateway PID;
- first and final recovery verdict;
- convergence observation count and elapsed seconds;
- final Gateway/Ollama listeners and MANAGED/Ollama state;
- proof no post-injection operator transition occurred.

PASS requires natural durable convergence to `READY`.

### Ollama crash

Record:

- exact old Ollama PID and validated identity;
- exact kill method `Stop-Process exact PID only`;
- different replacement Ollama PID;
- provider recovery incident diagnostic;
- `circuitOpen` value;
- first and final recovery verdict;
- convergence observation count and elapsed seconds;
- final Gateway/Ollama listeners and MANAGED/Ollama state;
- proof no post-injection operator transition occurred.

PASS requires the incident row to exist, the circuit not to remain open after this single injected crash, and natural durable convergence to `READY`.

### Intentional stop/start

Record:

- exact `cnx stop` command and exit code;
- maintenance mode with desired Gateway/provider stopped;
- Gateway listener absent;
- continuous no-auto-recovery observation for at least the harness-configured 10 seconds;
- exact single `cnx start` command and exit code;
- Gateway and Ollama listeners returned;
- first/final recovery verdict, observations, and elapsed seconds;
- final MANAGED/Ollama state and recovery verdict `READY`.

Intentional stop must not be classified as a crash.

## Evidence integrity

The harness is expected to create:

- `%USERPROFILE%\Downloads\CNX_V093_OLLAMA_RECOVERY_V3_<timestamp>.txt`;
- `%USERPROFILE%\Downloads\CNX_V093_OLLAMA_RECOVERY_V3_<timestamp>.json`.

Record:

- exact paths;
- file sizes;
- SHA256 for both files;
- JSON schema version, scenarios, start/completion/failure timestamps, result, error, activeOperation, and every step status;
- suite exit code;
- every skipped or not-reached scenario explicitly.

Do not claim PASS if the suite exit code is nonzero, JSON result is not `PASS`, a scenario is absent or skipped, an evidence file is missing, or any required scenario/cleanup step is `FAIL`.

## Failure and cleanup rule

The single authorized suite invocation may perform its built-in best-effort reconcile on failure. Do not independently rerun cleanup, `cnx start`, a crash scenario, or the full suite afterward.

After the suite exits, use read-only checks to record final status, provider status, recovery verdict, listeners, and PIDs.

If final state is unhealthy or cleanup failed, report that exactly and recommend only the narrowest next diagnostic. Do not conceal the failure or convert a partial result to PASS.

## Prohibited actions

- no second suite execution;
- no manual scenario replay;
- no process-tree kill;
- no source, harness, workflow, test, installer, or runtime edit;
- no package/software installation;
- no `cnx reset` or `cnx uninstall`;
- no release-path install or reinstall yet;
- no OpenClaw or Ollama uninstall or modification;
- no LM Studio management;
- no v0.9.2 change;
- no force-push or unrelated-worktree cleanup.

## Acceptance criteria

PASS requires every source, checkout, load, CI, preflight, and scenario gate above to pass with complete TXT/JSON evidence and hashes, exact old/new PIDs, exact commands/exit codes, and final MANAGED/Ollama/`READY` state.

Anything less is `FAIL` or `BLOCKED`, with skipped scenarios visible.

## Report

Write only:

`docs/operations/coordination/reports/CNX-20260822-010-full-windows-v3-process-recovery.md`

Include:

- start HEAD and source/blob/checkout/load/CI gates;
- exact preflight;
- exact one-time command and confirmation;
- scenario-by-scenario verdicts;
- exact PID identities and transitions;
- convergence and provider-incident evidence;
- TXT/JSON paths, sizes, SHA256, and parsed summaries;
- final read-only state;
- safety notes;
- every unproven or skipped item;
- recommended next step.

Only this matching Codex report may change. Commit message must begin:

`report: CNX-20260822-010`

Never force-push. Stop after publishing the report.
