# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260822-005`  
Updated: 2026-08-22 22:37 ICT  
Owner: ChatGPT  
Executor: Codex  

## Active task

[`tasks/CNX-20260822-005-v3-smoke-unittest-validation.md`](tasks/CNX-20260822-005-v3-smoke-unittest-validation.md)

## Predecessor review

[`reviews/CNX-20260822-004-v3-convergence-semantics.md`](reviews/CNX-20260822-004-v3-convergence-semantics.md)

Task 004 is BLOCKED pending a narrow smoke-contract correction and dependency-free validation. The harness implementation exists at commit `592a6fbd37da05013b7a8a5875ccd8b17e188cfa`; parser and `-SyntaxOnly` passed, but v3 smoke CI failed because its new multiline regex crossed function boundaries. The requested Python tests use standard-library `unittest` and do not require installing pytest.

## Purpose

Correct only the false-positive v3 smoke contract, run the three existing unittest files directly, and require completed green CI for the exact fix head. No disruptive runtime action is authorized.

## Execution authorization

Because `Execution mode` is `AUTO`, the enabled Codex coordination watcher may begin this exact task after synchronization and all source/safety checks.

## Required behavior

1. re-read Task 005 and matching report state;
2. verify implementation commit and exact harness/workflow blobs;
3. replace the cross-function smoke regex with exact per-scenario convergence assertions;
4. run the three Python unittest files directly without installing pytest;
5. rerun parser, `-SyntaxOnly`, local smoke contract, and `git diff --check`;
6. push only the authorized workflow correction;
7. observe and record completed CI for the exact fix head;
8. publish the Task 005 report and stop.

## Duplicate-execution fence

If a completed report for `CNX-20260822-005` already exists, do not repeat edits, validations, commits, CI reruns, or side effects. Exit awaiting ChatGPT review.
