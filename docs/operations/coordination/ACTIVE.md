# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260823-021`  
Updated: 2026-08-23 13:22 ICT  
Owner: ChatGPT  
Executor: Codex

## Active task

[`tasks/CNX-20260823-021-remove-stale-task020-control.md`](tasks/CNX-20260823-021-remove-stale-task020-control.md)

## Predecessor review

[`reviews/CNX-20260823-020-isolated-adjudication-and-task017-removal.md`](reviews/CNX-20260823-020-isolated-adjudication-and-task017-removal.md)

Task 020 is `ACCEPT` only as a safe blocked report. The watcher pre-created its exact control worktree, causing the task's strict path-absence fence to fail before Task 017 inspection.

## Purpose

Task 021 removes only the exact stale Task 020 control worktree after proving exact identity, cleanliness, reachability, no active Git operation, and no process use.

Its own exact Task 021 control worktree may be adopted when already created by the watcher only if path, registration, fetched HEAD, cleanliness, operation state, and reachability all match.

Task 017 must not be inspected in this task. No force, reset, clean, process action, runtime action, provider diagnosis, lifecycle action, merge, tag, or release is authorized.

## Duplicate-execution fence

If `docs/operations/coordination/reports/CNX-20260823-021-remove-stale-task020-control.md` exists, perform no further observation or action and stop awaiting ChatGPT review.
