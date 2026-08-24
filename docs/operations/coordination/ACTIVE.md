# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `MANUAL_WITH_HUMAN_GATE`  
Task ID: `CNX-20260824-052`  
Updated: 2026-08-24 19:32 ICT  
Owner: ChatGPT  
Executor: Codex after operator's manual signal

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` is project narrative and is not a Task 052 gate.

## Active task

[`tasks/CNX-20260824-052-live-install-over-v093-acceptance.md`](tasks/CNX-20260824-052-live-install-over-v093-acceptance.md)

## Task 051 report and review

[`reports/CNX-20260824-051-align-canonical-check-help.md`](reports/CNX-20260824-051-align-canonical-check-help.md)

[`reviews/CNX-20260824-051-align-canonical-check-help.md`](reviews/CNX-20260824-051-align-canonical-check-help.md)

Task 051 is reviewed `ACCEPT` as `ACCEPT_CANONICAL_CHECK_HELP_ALIGNED`.

Implementation commit:

`6d90025f832bb36c477176809a0af2e6c1858c19`

## Human authorization

The operator approved using the update as a real install-over test and then directed continuation after the Task 051 report.

Scheduled execution remains disabled. Codex starts only from the operator's manual signal.

## Authorized operation

Invoke the reviewed default installer exactly once against the coherent current `mode=upgrade` installation:

`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "C:\Users\CDQ-P\.openclaw\workspace"`

Use an exit-code-retaining process wrapper. Do not use clean reinstall, custom flags, migration, manual installed-file edits, or a second installer.

## Acceptance focus

- install Task 051 help files through the supported upgrade path;
- capture observed installer exit code `0`;
- preserve Ticket/workflow/session/policy state;
- preserve AGENTS baseline and one canonical block;
- maintain one canonical plugin and scheduler;
- return MANAGED/Ollama/Gateway health;
- preserve 71 unrelated plugins, four models, Task 049 backup, primary repository, and excluded systems;
- prove canonical check passes and generic check remains rejected.

## Safety

On preflight drift, nonzero/unobserved exit, partial state, rollback, preservation failure, or runtime failure: do not retry, manually complete, clean reinstall, or restore. Publish the report and stop.
