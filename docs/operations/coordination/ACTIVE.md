# Active Coordination Task

Status: `AWAITING_HUMAN_INSTALL_AUTHORIZATION`  
Execution mode: `MANUAL_WITH_HUMAN_GATE`  
Task ID: `NONE`  
Updated: 2026-08-24 18:55 ICT  
Owner: ChatGPT  
Executor: Codex only after a new task and the operator's manual signal

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` is project narrative and is not a coordination gate.

## Latest completed task

[`reports/CNX-20260824-049-backup-remove-legacy-stop-at-fresh.md`](reports/CNX-20260824-049-backup-remove-legacy-stop-at-fresh.md)

[`reviews/CNX-20260824-049-backup-remove-legacy-stop-at-fresh.md`](reviews/CNX-20260824-049-backup-remove-legacy-stop-at-fresh.md)

Task 049 is reviewed `ACCEPT` as `ACCEPT_FRESH_WITH_EXPECTED_PREHOST_AGENTS_RESTORE`.

## Accepted fresh baseline

Legacy CogentNexus was backed up and removed. The current classifier is exact `mode=fresh`. No current CogentNexus-OpenClaw installation occurred.

The final workspace `AGENTS.md` is the accepted pre-host baseline:

- 7,196 bytes;
- SHA-256 `C9A664B73200AE5D6B0DA0908DE3256CDB4DDA8BA6FE99F5E6C5115C3983604C`;
- no legacy CogentNexus managed block.

This result is the intentional effect of legacy `cnx disable`; do not restore the pre-task managed version.

## Current gate

There is no active executable task.

Installing the current CogentNexus-OpenClaw requires:

1. a new successor task;
2. explicit operator authorization;
3. the operator's manual Codex execution signal.

Until then, do not run `scripts/install.ps1`, `clean-reinstall.ps1`, a Release installer, or any equivalent installation path.

## Safety

Retain the verified external backup unchanged. Preserve OpenClaw/Gateway, Ollama/models, user data, unrelated plugins/projects, primary repository, HermesAgent, Ecosystem, staged-capability-loop, and retained Procmon evidence.

No Task 049 action may be repeated. No legacy restore, OpenClaw upgrade/reinstall, manual SQLite edit, broad deletion, force kill, merge, tag, Release, or archive action is authorized.
