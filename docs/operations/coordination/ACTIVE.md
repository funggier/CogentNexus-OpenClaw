# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260822-003`  
Updated: 2026-08-22 21:08 ICT  
Owner: ChatGPT  
Executor: Codex  

## Active task

[`tasks/CNX-20260822-003-gateway-baseline-convergence.md`](tasks/CNX-20260822-003-gateway-baseline-convergence.md)

## Predecessor review

[`reviews/CNX-20260822-002-gateway-convergence.md`](reviews/CNX-20260822-002-gateway-convergence.md)

Task 002 ended safely as BLOCKED because the real Gateway scheduled task was stopped and port 18789 was not listening, despite desired state `running` and recovery verdict `READY`.

## Purpose

Restore a verified healthy Gateway baseline with at most one explicitly authorized pre-injection `cnx start`, then rerun the focused exact-PID Gateway convergence diagnostic. No manual runtime transition is allowed after failure injection.

## Execution authorization

Because `Execution mode` is `AUTO`, the enabled Codex coordination watcher may begin this exact task after synchronization and all safety checks.

## Required behavior

1. re-read the exact Task 003 and matching report state;
2. preserve unrelated and previously dirty worktrees;
3. classify the Gateway/recovery-verdict mismatch read-only;
4. use the one authorized pre-injection baseline `cnx start` only when required;
5. run the exact convergence diagnostic only after a healthy baseline;
6. preserve exact-PID/no-process-tree-kill invariants;
7. publish the Task 003 report and stop.

## Duplicate-execution fence

If a completed report for `CNX-20260822-003` already exists, do not repeat runtime transitions or disruptive effects. Exit awaiting ChatGPT review.
