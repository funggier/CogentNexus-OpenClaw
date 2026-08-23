# CNX-20260822-008 — Full Real-Windows V3 Process-Recovery Suite

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Priority: current  
Predecessor: `CNX-20260822-007` (BLOCKED; no runtime side effect)

## Objective

Run the accepted v3 Ollama-only process-recovery suite exactly once on the real Windows target and preserve complete evidence for:

1. healthy MANAGED/Ollama baseline;
2. exact-PID OpenClaw Gateway hard crash and natural durable convergence;
3. exact-PID Ollama listener hard crash, provider-incident evidence, and natural durable convergence;
4. intentional `cnx stop` remaining stopped;
5. one documented `cnx start` returning to MANAGED/Ollama/`READY`.

This task authorizes only this process-level recovery run. It does not authorize install, reset, uninstall, reinstall, source edits, or release actions.

## Task 007 safety carry-forward

Task 007 stopped before CI observation, Windows preflight, confirmation, suite invocation, process kill, lifecycle command, evidence collection, source edit, or package/runtime mutation. Its disruptive allowance was not consumed, but its matching report permanently closes Task 007.

Task 008 is the sole new authorization for one suite invocation. Do not resume Task 007. Do not execute anything if a matching Task 008 report already exists.

The Task 007 report reconstructed an invalid SHA that was not present in the immutable task. For Task 008:

- read the workflow-fix SHA literally from this file;
- compare the literal byte-for-byte with `929fbcc663251941d88f38f09544068a9b3e069d`;
- run `git cat-file -e 929fbcc663251941d88f38f09544068a9b3e069d^{commit}`;
- run the ancestor check using that exact literal;
- do not concatenate, shorten, autocomplete, substitute, or reconstruct the SHA from memory or another commit.

If the literal in the fetched task differs, report `BLOCKED` without any runtime action.

## Source gates

Repository: `funggier/cogentnexus`  
Branch: `agent/v0.9.3-recovery-reality-tests`  
Required accepted validation report ancestor: `5a22d9479ad7d62c7a159e4b49e2bc3f79fb6171`  
Required harness implementation ancestor: `592a6fbd37da05013b7a8a5875ccd8b17e188cfa`  
Required workflow-fix ancestor: `929fbcc663251941d88f38f09544068a9b3e069d`  
Harness: `scripts/test-v093-ollama-recovery-windows-v3.ps1`  
Required harness blob: `6d4c9347de12bbe4e3e5c428f2fe80333f92757f`

Later ChatGPT-owned coordination/documentation commits are allowed. Before any runtime action:

- fetch the branch;
- verify all three required ancestors;
- verify the exact harness blob;
- use a clean isolated worktree;
- record start HEAD and `git status --short`;
- verify no matching Task 008 report already exists.

If a source gate fails, report `BLOCKED` without running the suite.

## CI precondition

Before the disruptive command, use bounded read-only observation until all applicable workflows for the exact Task 008 start HEAD complete.

Every required workflow must conclude `success`. Do not run the disruptive suite if any workflow is failed, cancelled, unexpectedly skipped, or still in progress. Do not manually rerun workflows.

Record the complete workflow name/run/status/conclusion table.

## Read-only real-Windows preflight

Before confirmation or injection, record exact commands, exit codes, and output/evidence for:

- `openclaw.cmd --version`;
- `openclaw.cmd config validate`;
- `ollama.exe --version`;
- installed `%USERPROFILE%\.openclaw\workspace\cnx.cmd` path and SHA256;
- `cnx.cmd status`;
- `cnx.cmd provider status --json`;
- `cnx.cmd check recovery --json` with exit code 0 or 1 recorded;
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

Run exactly once:

`powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test-v093-ollama-recovery-windows-v3.ps1 -Scenario all -RunDisruptive`

When prompted, type exact lowercase `y` once.

Do not invoke the suite a second time in this task under any outcome. Do not manually repeat a scenario.

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
- first/final recovery verdict;
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
- first/final recovery verdict;
- convergence observation count and elapsed seconds;
- final Gateway/Ollama listeners and MANAGED/Ollama state;
- proof no post-injection operator transition occurred.

PASS requires the incident row to exist, the circuit not to remain open after this single injected crash, and natural durable convergence to `READY`.

### Intentional stop/start

Record:

- exact `cnx stop` command/exit code;
- maintenance mode with desired Gateway/provider stopped;
- Gateway listener absent;
- continuous no-auto-recovery observation for at least the harness-configured 10 seconds;
- exact single `cnx start` command/exit code;
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
- all skipped/not-reached scenarios explicitly.

Do not claim PASS if the suite exit code is nonzero, JSON result is not `PASS`, a scenario is absent/skipped, an evidence file is missing, or any required scenario/cleanup step is `FAIL`.

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
- no release-path install/reinstall yet;
- no OpenClaw or Ollama uninstall/modification;
- no LM Studio management;
- no v0.9.2 change;
- no force-push or unrelated-worktree cleanup.

## Acceptance criteria

PASS requires every source/CI/preflight gate and every scenario above to pass with complete TXT/JSON evidence and hashes, exact old/new PIDs, exact commands/exit codes, and final MANAGED/Ollama/`READY` state.

Anything less is `FAIL` or `BLOCKED`, with skipped scenarios visible.

## Report

Write:

`docs/operations/coordination/reports/CNX-20260822-008-full-windows-v3-process-recovery.md`

Include:

- start HEAD and source/blob/CI gates;
- exact preflight;
- exact one-time command and confirmation;
- scenario-by-scenario verdicts;
- exact PID identities and transitions;
- convergence/incident evidence;
- TXT/JSON paths, sizes, SHA256, and parsed summaries;
- final read-only state;
- safety notes;
- every unproven/skipped item;
- recommended next step.

Only this matching Codex report may change. Commit message must begin:

`report: CNX-20260822-008`

Never force-push. Stop after publishing the report.
