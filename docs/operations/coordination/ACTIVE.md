# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `MANUAL_WITH_HUMAN_GATE`  
Task ID: `CNX-20260824-045`  
Updated: 2026-08-24 12:34 ICT  
Owner: ChatGPT  
Executor: Codex after operator's manual signal

## Active task

[`tasks/CNX-20260824-045-live-windows-clean-reinstall-acceptance.md`](tasks/CNX-20260824-045-live-windows-clean-reinstall-acceptance.md)

## Predecessor report and review

[`reports/CNX-20260824-044-repair-install-classifier-and-clean-reinstall-handoff.md`](reports/CNX-20260824-044-repair-install-classifier-and-clean-reinstall-handoff.md)

[`reviews/CNX-20260824-044-repair-install-classifier-and-clean-reinstall-handoff.md`](reviews/CNX-20260824-044-repair-install-classifier-and-clean-reinstall-handoff.md)

Task 044 is reviewed `ACCEPT` for repository implementation commit `4c825f8ec1ed6b43a419ad52e0bb85cee28007c1`.

## Human authorization

The operator selected `1`, authorizing the bounded live Windows Task 045 scope recorded in the task.

Scheduled ChatGPT/Codex execution remains disabled. The operator will trigger Codex manually.

## Execution boundary

Task 045 first performs a read-only source/collision/current-state/ownership preflight.

Only an exact coherent v0.9.3 `upgrade` classification may proceed to one invocation of the reviewed default-backup clean-reinstall script.

Legacy, fresh-with-residue, mixed, partial, ambiguous, source-drift, collision, or ownership failure must stop before mutation. Legacy migration is not authorized by this task.

## Safety

- Default backup root only: `%LOCALAPPDATA%\CogentNexus-OpenClaw-Clean-Reinstall-Backups`.
- No `-NoBackup`, custom `-BackupRoot`, or `-LinkPlugin`.
- No destructive retry or automatic restore.
- No primary-repository checkout/reset/clean/worktree change.
- No Procmon or Task 027/038 evidence access.
- No CogentNexus-HermesAgent, CogentNexus-Ecosystem, staged-capability-loop, merge, tag, Release, or archive action.
