# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260823-012`  
Updated: 2026-08-23 00:40 ICT  
Owner: ChatGPT  
Executor: Codex

## Active task

[`tasks/CNX-20260823-012-task010-checkout-collision-diagnostic.md`](tasks/CNX-20260823-012-task010-checkout-collision-diagnostic.md)

## Predecessor review

[`reviews/CNX-20260822-010-full-windows-v3-process-recovery.md`](reviews/CNX-20260822-010-full-windows-v3-process-recovery.md)

Task 010 is `BLOCKED`. Its reporting run stopped before clone validation, CI observation, Windows preflight, confirmation, harness execution, process injection, or any CogentNexus runtime transition because two Task 010 destination directories already existed.

The two full-process-recovery paths were created four seconds apart. The Task 010 report cannot establish whether another overlapping watcher run only created them or reached the harness. No process-recovery gate is accepted.

## Purpose

Inspect the exact three documented Task 010 paths, exact attached PIDs, and matching TXT/JSON evidence read-only. Classify whether this was a checkout-only race, active execution, an unreported completed/failed execution, no runtime start, or ambiguous.

## Execution authorization

Because `Execution mode` is `AUTO`, the Codex watcher may execute this exact metadata-only diagnostic after synchronization and duplicate-fence checks.

Task 012 does not authorize the recovery harness, parser, `-SyntaxOnly`, CI wait, Windows health preflight, confirmation, process kill, `cnx`, OpenClaw/Ollama commands, checkout cleanup, memory reclaim, install/reset/uninstall/reinstall, or another manual clone/worktree.

Task 011 remains queued and must not execute until explicitly activated.

## Required behavior

1. re-read Task 012 and matching report state;
2. if the report exists, perform no local action;
3. do not create another manual clone/worktree/checkout;
4. inspect only the three exact documented Task 010 paths and task-scoped evidence;
5. record exact-PID/path relationships without exposing sensitive command lines;
6. if active execution is detected, observe once, do not interfere, report, and stop;
7. publish only the matching Task 012 report.

## Duplicate-execution fence

If `docs/operations/coordination/reports/CNX-20260823-012-task010-checkout-collision-diagnostic.md` already exists, do not inspect any local path, process, evidence file, checkout, runtime, or UI. Exit awaiting ChatGPT review.
