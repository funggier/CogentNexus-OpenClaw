# Active Coordination Task

Status: `AWAITING_HUMAN_AUTHORIZATION`  
Execution mode: `HUMAN_GATE`  
Task ID: `PENDING-CNX-20260824-045`  
Updated: 2026-08-24 12:26 ICT  
Owner: ChatGPT  
Executor: Codex only after explicit operator authorization

## Completed predecessor

[`reports/CNX-20260824-044-repair-install-classifier-and-clean-reinstall-handoff.md`](reports/CNX-20260824-044-repair-install-classifier-and-clean-reinstall-handoff.md)

[`reviews/CNX-20260824-044-repair-install-classifier-and-clean-reinstall-handoff.md`](reviews/CNX-20260824-044-repair-install-classifier-and-clean-reinstall-handoff.md)

Task 044 is reviewed `ACCEPT` for repository implementation commit `4c825f8ec1ed6b43a419ad52e0bb85cee28007c1`.

## Pending human gate

The next proposed task is a bounded live Windows clean-reinstall acceptance sequence using only the reviewed default backup root:

`%LOCALAPPDATA%\CogentNexus-OpenClaw-Clean-Reinstall-Backups`

It would read and preserve the current exact ownership/runtime state, create and verify one backup, enter PASSTHROUGH, uninstall only exact CogentNexus-OpenClaw-owned artifacts, install v0.9.3 fresh, and verify OpenClaw/Ollama plus namespace isolation.

This live task is destructive and is **not authorized yet**. Do not create or execute Task 045 until the operator explicitly approves the presented scope.

## Safety fence

Until authorization:

- no live workspace/config/runtime/install/clean-reinstall/reset/uninstall mutation;
- no Gateway/Ollama/scheduler/service mutation;
- no Procmon action;
- no CogentNexus-Ecosystem or staged-capability-loop work;
- no merge, tag, GitHub Release, or release archive;
- do not wake Codex for a live task.

Scheduled execution remains operator-controlled.
