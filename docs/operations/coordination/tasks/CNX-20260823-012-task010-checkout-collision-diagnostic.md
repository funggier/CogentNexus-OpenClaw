# CNX-20260823-012 — Task 010 Checkout-Collision and Duplicate-Execution Diagnostic

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Priority: current safety diagnostic  
Predecessor: `CNX-20260822-010` (`BLOCKED`)  
Execution mode: `AUTO`

## Objective

Determine, without changing local state, why two Task 010 checkout destinations appeared four seconds apart and whether any overlapping watcher process loaded or invoked the v3 recovery harness.

This task is metadata/evidence inspection only. It does not authorize the process-recovery suite, a scenario, confirmation, process kill, CogentNexus/OpenClaw/Ollama command, checkout cleanup, memory reclaim, or lifecycle action.

## Duplicate-execution fence

Before any local observation, fetch the branch and check for:

`docs/operations/coordination/reports/CNX-20260823-012-task010-checkout-collision-diagnostic.md`

If it exists, perform no local observation or other action. Stop awaiting ChatGPT review.

Confirm `ACTIVE.md` names this exact task with `READY_FOR_CODEX` and `AUTO`.

## Exact paths in scope

Inspect only these already documented paths and their direct Git/process metadata:

1. `C:\Users\CDQ-P\.openclaw\worktrees\CNX-20260822-010-full-windows-v3-process-recovery-20260823-003708`
2. `C:\Users\CDQ-P\.openclaw\worktrees\CNX-20260822-010-full-windows-v3-process-recovery-20260823-003712`
3. `C:\Users\CDQ-P\.openclaw\worktrees\CNX-20260822-010-report-blocked-20260823-0039`

Do not create another manual clone, worktree, checkout, destination directory, or temporary copy. Use only the watcher-provided coordination checkout for publishing the report.

## Required read-only inspection

Record exact commands and exit codes.

For each scoped path, record:

- exists/missing;
- directory type: full clone, registered worktree, report worktree, or unknown;
- creation and last-write timestamps;
- metadata-only total size and file count;
- Git HEAD and branch/detached state;
- redacted origin identity;
- `git status --porcelain=v1`;
- tracked deletions from `git diff --name-only --diff-filter=D`;
- whether the v3 harness physical file exists;
- harness Git blob, SHA256, and byte size when it exists;
- whether generated/untracked files indicate parser, syntax, CI, preflight, or suite activity;
- do not open unrelated project/user files.

Capture exact-PID process evidence for any safely observable process whose current directory, command-line path, executable metadata, or open-handle metadata references a scoped path. Record:

- PID and parent PID;
- process/executable name;
- start time;
- working set and private bytes where available;
- role: watcher, renderer, terminal, shell, Git, PowerShell harness, editor, or unknown;
- path relationship;
- command line only as a redacted role summary; never expose tokens, credentials, chat text, or unrelated arguments.

Specifically determine whether any active process references:

- `test-v093-ollama-recovery-windows-v3.ps1`;
- `-Scenario all`;
- `-RunDisruptive`;
- either full-process-recovery directory.

Do not stop, signal, suspend, attach a debugger to, or alter any process.

## Evidence-file accounting

Inspect only filename metadata for:

`%USERPROFILE%\Downloads\CNX_V093_OLLAMA_RECOVERY_V3_*.txt`
`%USERPROFILE%\Downloads\CNX_V093_OLLAMA_RECOVERY_V3_*.json`

Limit candidates to files created or modified at or after `2026-08-23 00:37:00 ICT`.

For each candidate, record exact path, timestamps, size, and SHA256. A Task 010 JSON candidate may be parsed read-only only to record schema version, start/completion/failure timestamps, result, error, activeOperation, scenarios, and step statuses. Do not alter, move, rename, or delete evidence.

Also inspect Git metadata and local shell/history only when a non-sensitive, task-scoped source can prove whether the exact harness command began. Do not read general PowerShell history, chat/session databases, browser history, or unrelated logs.

## Classification

Return exactly one primary classification:

- `NO_RUNTIME_STARTED`: both collision paths are inactive and no command/evidence proves harness execution;
- `ACTIVE_EXECUTION_DETECTED`: an exact live PID proves a Task 010 harness or prerequisite is still running;
- `COMPLETED_OR_FAILED_UNREPORTED_EXECUTION`: evidence proves a suite invocation occurred outside the matching report;
- `CHECKOUT_ONLY_RACE`: overlapping runs created/initialized checkout paths but did not reach Windows runtime;
- `AMBIGUOUS`: evidence cannot safely distinguish the above.

If active execution is detected, observe only once, publish the report, and stop. Do not wait for completion and do not interfere.

## Prohibited actions

- no recovery harness, scenario, parser, `-SyntaxOnly`, CI wait, or Windows health preflight;
- no lowercase `y` confirmation;
- no process kill, tree operation, suspend, restart, window close, or app restart;
- no `cnx`, OpenClaw, or Ollama command;
- no clone/worktree creation beyond the watcher-provided execution environment;
- no `git worktree remove`, `git worktree prune`, `git clean`, `git reset`, repair, reuse, deletion, archive, or rename;
- no chat/project/session/cache deletion;
- no install, reset, uninstall, reinstall, merge, tag, release, package change, or force-push.

## Acceptance criteria

PASS requires complete exact-path metadata, exact-PID attachment accounting, evidence-file accounting, one primary classification, and an explicit statement of what remains unproven.

This diagnostic never passes the v0.9.3 process-recovery gate.

## Report

Write only:

`docs/operations/coordination/reports/CNX-20260823-012-task010-checkout-collision-diagnostic.md`

Include:

- Task ID, start HEAD, ACTIVE verification;
- exact commands/exit codes;
- per-path metadata table;
- exact-PID/path relationship table;
- evidence-file table;
- primary classification;
- safety accounting;
- unproven items;
- narrow recommended next step.

Only this matching report may change. Commit message must begin:

`report: CNX-20260823-012`

Never force-push. Stop after publishing the report.
