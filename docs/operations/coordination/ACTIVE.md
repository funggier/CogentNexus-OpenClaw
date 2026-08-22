# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260822-002`  
Updated: 2026-08-22 21:00 ICT  
Owner: ChatGPT  
Executor: Codex  

## Active task

[`tasks/CNX-20260822-002-gateway-convergence-clean-worktree.md`](tasks/CNX-20260822-002-gateway-convergence-clean-worktree.md)

## Predecessor review

[`reviews/CNX-20260822-001-gateway-convergence.md`](reviews/CNX-20260822-001-gateway-convergence.md)

Task 001 ended safely as BLOCKED because its selected worktree contained unrelated tracked test-file deletions. Those modifications must remain untouched.

## Purpose

Run the focused Gateway durable-recovery convergence diagnostic from a newly created clean isolated checkout/worktree and determine whether the recovery marker returns to `READY` naturally after automatic Gateway restoration.

## Execution authorization

Because `Execution mode` is `AUTO`, an enabled Codex coordination Scheduled task following `WATCH_MODE.md` may begin this exact task automatically after synchronizing and verifying all task-specific safety gates.

Manual fallback remains:

```text
ต่อ
```

## Required behavior

1. synchronize the coordination branch safely;
2. re-read `CODEX_BOOTSTRAP.md`, `WATCH_MODE.md`, this file, the active task, and matching report state;
3. preserve the previously dirty worktree without modification;
4. create/use a new clean isolated checkout as authorized by Task 002;
5. execute only the active task;
6. publish the matching Codex report/evidence references;
7. stop the run and wait for ChatGPT review.

## Duplicate-execution fence

If a completed report for `CNX-20260822-002` already exists at the synchronized GitHub state, do not repeat disruptive effects. Exit awaiting ChatGPT review.

## Completion rule

This pointer remains `READY_FOR_CODEX` until Codex publishes the matching report. ChatGPT will review the report and advance the pointer.
