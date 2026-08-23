# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260823-018`  
Updated: 2026-08-23 12:15 ICT  
Owner: ChatGPT  
Executor: Codex

## Active task

[`tasks/CNX-20260823-018-remove-wrong-head-task017-worktree.md`](tasks/CNX-20260823-018-remove-wrong-head-task017-worktree.md)

## Predecessor review

[`reviews/CNX-20260823-017-offline-provider-durable-convergence-diagnosis.md`](reviews/CNX-20260823-017-offline-provider-durable-convergence-diagnosis.md)

Task 017's safe `BLOCKED` report is `ACCEPT`. Its worktree command used an unset ref variable and created the exact authorized path at wrong local HEAD `78f6cba4748e59d5975940ca9854961d0e7ff550`. Codex stopped before source diagnosis or Windows/runtime action.

## Current problem

The wrong-head Task 017 worktree remains at:

`C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-017`

It must be handled by an exact reviewed cleanup task before provider diagnosis is reauthorized. Provider durable-convergence root cause remains unproven.

## Purpose

Task 018 must:

- verify the exact path, Git registration, wrong HEAD, clean state, absence of Git operations/unpublished work, and absence of processes bound to the path;
- remove only that exact worktree using normal non-force Git removal if every gate passes;
- verify the path and registration are absent;
- publish an exact PASS or BLOCKED report.

Task 018 must not create another worktree or perform provider diagnosis.

No process kill, recovery rerun, runtime command, install, reset, uninstall, reinstall, source change, merge, tag, or release is authorized.

Task 011 remains deferred while RAM remains stable.

## Duplicate-execution fence

If `docs/operations/coordination/reports/CNX-20260823-018-remove-wrong-head-task017-worktree.md` exists, perform no further observation or action and stop awaiting ChatGPT review.
