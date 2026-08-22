# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260822-004`  
Updated: 2026-08-22 22:33 ICT  
Owner: ChatGPT  
Executor: Codex  

## Active task

[`tasks/CNX-20260822-004-v3-convergence-semantics.md`](tasks/CNX-20260822-004-v3-convergence-semantics.md)

## Predecessor review

[`reviews/CNX-20260822-003-gateway-convergence.md`](reviews/CNX-20260822-003-gateway-convergence.md)

Task 003 is accepted. Exact-PID Gateway process recovery succeeded and durable recovery naturally converged from `READY_WITH_WARNINGS` to `READY` after 8 read-only observations in 14.769 seconds without a post-injection runtime transition.

## Latest human signal

The human operator sent `ทำต่อเลยครับ` at 2026-08-22 22:33 ICT. This reaffirms execution of the existing exact Task 004 only. It does not expand scope, bypass gates, or authorize duplicate execution.

## Purpose

Correct the v3 full-suite evidence semantics so post-transition acceptance explicitly observes durable/runtime convergence. This task changes and validates the harness only; it does not authorize a disruptive Windows run.

## Execution authorization

Because `Execution mode` is `AUTO`, the enabled Codex coordination watcher may begin this exact task after synchronization and all source/safety checks.

## Required behavior

1. re-read Task 004 and matching report state;
2. use a clean isolated worktree and verify exact source blobs;
3. add bounded read-only durable convergence observation to the v3 harness;
4. preserve exact-PID, protected-process, provider-incident, and intentional-stop invariants;
5. strengthen the PS5.1 smoke regression contract;
6. run safe non-disruptive validation only;
7. publish the Task 004 report and stop.

## Duplicate-execution fence

If a completed report for `CNX-20260822-004` already exists, do not repeat edits, commits, validations, or side effects. Exit awaiting ChatGPT review.
