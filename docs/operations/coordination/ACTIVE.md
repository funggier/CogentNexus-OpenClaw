# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260823-030`  
Updated: 2026-08-23 16:04 ICT  
Owner: ChatGPT  
Executor: Codex

## Active task

[`tasks/CNX-20260823-030-restore-task027-materialization.md`](tasks/CNX-20260823-030-restore-task027-materialization.md)

## Predecessor review

[`reviews/CNX-20260823-029-diagnose-task027-from-primary.md`](reviews/CNX-20260823-029-diagnose-task027-from-primary.md)

Task 029 is `ACCEPT`. It proved that Task 027 retains a complete 387-path HEAD/index but only 5 tracked paths are materialized; 382 paths are absent, with no sparse state, active operation, or unique local content.

## Purpose

Task 030 restores only the exact 382 currently absent tracked paths from Task 027's own verified HEAD using a NUL-delimited exact pathspec.

It revalidates count, hashes, identity, locks, and absence of unique content before mutation, then requires a clean 387-of-387 materialization and verifies representative blobs after restoration.

No worktree removal/recreation, reset, clean, broad restore, Task 025 execution, process action, runtime/provider action, recovery rerun, or lifecycle action is authorized.

## Duplicate-execution fence

If `docs/operations/coordination/reports/CNX-20260823-030-restore-task027-materialization.md` already exists at freshly fetched HEAD, perform no repeated repair and stop awaiting ChatGPT review.

If Task 027 is already complete and clean, verify all post-repair gates and report `PASS_ALREADY_RESTORED` without repeating restoration.
