# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260822-006`  
Updated: 2026-08-22 22:43 ICT  
Owner: ChatGPT  
Executor: Codex  

## Active task

[`tasks/CNX-20260822-006-v3-validation-only.md`](tasks/CNX-20260822-006-v3-validation-only.md)

## Predecessor review

[`reviews/CNX-20260822-005-v3-smoke-unittest-validation.md`](reviews/CNX-20260822-005-v3-smoke-unittest-validation.md)

Task 005 is BLOCKED because its immutable pre-fix workflow blob had already been superseded by the authorized correction before Codex began. Codex stopped safely. The actual workflow-fix commit is `929fbcc663251941d88f38f09544068a9b3e069d`; its v3 smoke run `32582330616` and job `97053475362` succeeded.

## Purpose

Complete only the missing direct unittest, parser, `-SyntaxOnly`, local contract, diff, and applicable-CI validation for the existing harness/workflow blobs. No source edit or disruptive runtime action is authorized.

## Execution authorization

Because `Execution mode` is `AUTO`, the enabled Codex coordination watcher may begin this exact task after synchronization and all source/safety checks.

## Required behavior

1. re-read Task 006 and matching report state;
2. verify ancestors `592a6fbd37da05013b7a8a5875ccd8b17e188cfa` and `929fbcc663251941d88f38f09544068a9b3e069d`;
3. verify harness blob `6d4c9347de12bbe4e3e5c428f2fe80333f92757f` and workflow blob `35b6796e4868447cfe3db6a86a7528d0288c8411`;
4. run the three standard-library unittest files directly without installing anything;
5. run Windows PowerShell parser, `-SyntaxOnly`, corrected local contract, `git diff --check`, and clean-status checks;
6. observe applicable CI read-only and record exact run/job conclusions;
7. add only the Task 006 report and stop.

## Duplicate-execution fence

If a matching report for `CNX-20260822-006` already exists, do not repeat tests, CI observation, edits, commits, or side effects. Exit awaiting ChatGPT review.
