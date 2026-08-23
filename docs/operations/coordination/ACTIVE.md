# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260823-034`  
Updated: 2026-08-23 19:49 ICT  
Owner: ChatGPT  
Executor: Codex

## Active task

[`tasks/CNX-20260823-034-trace-task027-filesystem-io-and-audit-source.md`](tasks/CNX-20260823-034-trace-task027-filesystem-io-and-audit-source.md)

## Predecessor review

[`reviews/CNX-20260823-033-complete-recurring-materialization-loss-evidence.md`](reviews/CNX-20260823-033-complete-recurring-materialization-loss-evidence.md)

Task 033 is `ACCEPT` as a read-only evidence-completion result. It confirmed the recurring 382-path state with hashed inventories and a UTC timeline, but did not prove an actor. Neither Supervisor nor Codex watcher is implicated.

## Purpose

Task 034 performs the single accepted next diagnostic: a bounded filesystem I/O trace focused on the exact Task 027 target, plus a read-only source audit of deletion/materialization/worktree-cleanup code requested by the human operator.

Source capability must remain separate from runtime attribution. No restoration, containment, task/watcher/Supervisor change, software installation, audit enablement, or CogentNexus/OpenClaw/Ollama runtime action is authorized.

## Progress communication

During active execution, report meaningful progress approximately every 3 minutes and immediately after preflight/tool discovery, trace start/stop, source audit, correlation, or blocker. Progress updates are not pause points.

## Duplicate-execution fence

If `docs/operations/coordination/reports/CNX-20260823-034-trace-task027-filesystem-io-and-audit-source.md` already exists at freshly fetched HEAD, do not repeat the trace or source audit; stop awaiting ChatGPT review.
