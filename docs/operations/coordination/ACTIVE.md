# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `MANUAL_WITH_HUMAN_GATE`  
Task ID: `CNX-20260824-050`  
Updated: 2026-08-24 19:01 ICT  
Owner: ChatGPT  
Executor: Codex after operator's manual signal

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` is project narrative and is not a Task 050 gate.

## Active task

[`tasks/CNX-20260824-050-fresh-install-current-v093.md`](tasks/CNX-20260824-050-fresh-install-current-v093.md)

## Accepted predecessor

[`reports/CNX-20260824-049-backup-remove-legacy-stop-at-fresh.md`](reports/CNX-20260824-049-backup-remove-legacy-stop-at-fresh.md)

[`reviews/CNX-20260824-049-backup-remove-legacy-stop-at-fresh.md`](reviews/CNX-20260824-049-backup-remove-legacy-stop-at-fresh.md)

Task 049 is reviewed `ACCEPT` as `ACCEPT_FRESH_WITH_EXPECTED_PREHOST_AGENTS_RESTORE`.

## Human authorization

The operator explicitly authorized opening Task 050 with response:

> `1`

This authorizes one fresh installation of reviewed CogentNexus-OpenClaw v0.9.3 after every source/fresh/runtime/sentinel gate passes.

Scheduled execution remains disabled. Codex starts only from the operator's manual signal.

## Accepted fresh baseline

- classifier: exact `mode=fresh`;
- legacy CogentNexus: absent;
- current CogentNexus-OpenClaw: absent;
- workspace `AGENTS.md`: 7,196 bytes, SHA-256 `C9A664B73200AE5D6B0DA0908DE3256CDB4DDA8BA6FE99F5E6C5115C3983604C`;
- Task 049 verified external backup retained;
- OpenClaw/Gateway, Ollama/four models, unrelated plugins/data preserved.

## Installation boundary

Run exactly one default installer invocation from a new isolated clone:

`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "C:\Users\CDQ-P\.openclaw\workspace"`

Do not run clean reinstall, migration, Release installer, custom flags, a second installer, or manual partial completion.

Expected namespace is only `cnxclaw.cmd`, `skills\cogentnexus-openclaw`, `.cogentnexus-openclaw`, plugin `cogentnexus-openclaw`, and task `CogentNexus-OpenClaw-Supervisor`.

## Safety

Preserve OpenClaw/Gateway, Ollama/models, user data, unrelated plugins/projects, primary repository, Task 049 backup, HermesAgent, Ecosystem, staged-capability-loop, and retained Procmon evidence.

On installer failure/timeout/partial state, do not retry or auto-restore. Inventory durable state, prove native rollback where applicable, publish the report, and stop.
