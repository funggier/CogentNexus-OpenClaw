# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260823-032`  
Updated: 2026-08-23 17:05 ICT  
Owner: ChatGPT  
Executor: Codex

## Active task

[`tasks/CNX-20260823-032-diagnose-recurring-task027-materialization-loss.md`](tasks/CNX-20260823-032-diagnose-recurring-task027-materialization-loss.md)

## Predecessor review

[`reviews/CNX-20260823-031-reconcile-task027-single-path-stat-cache.md`](reviews/CNX-20260823-031-reconcile-task027-single-path-stat-cache.md)

Task 031 is `BLOCKED`. It safely proved that the Task 027 control had returned from the Task 030 verified 387/387 materialization to 5/387, with the same broad absence pattern and no Task 031 mutation.

## Purpose

Task 032 is a read-only diagnostic to identify the recurring materialization-loss mechanism, exact actor or watcher when evidence supports one, and the time boundary. It inventories registration/config/index/filesystem metadata, processes, scheduled tasks, watchers, available event records, and a bounded 60-second stability window.

No restoration, file/index mutation, process/task action, Task 025 execution, repository-reference migration, or CogentNexus/OpenClaw/Ollama runtime action is authorized.

## Progress communication

During active execution, report meaningful progress at least approximately every 3 minutes and immediately after preflight, process/watcher inventory, event correlation, stability observation, or blocker. Progress updates are not pause points.

## Duplicate-execution fence

If `docs/operations/coordination/reports/CNX-20260823-032-diagnose-recurring-task027-materialization-loss.md` already exists at freshly fetched HEAD, perform no repeated diagnostic and stop awaiting ChatGPT review.
