# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260824-044`  
Updated: 2026-08-24 11:27 ICT  
Owner: ChatGPT  
Executor: Codex

## Active task

[`tasks/CNX-20260824-044-repair-install-classifier-and-clean-reinstall-handoff.md`](tasks/CNX-20260824-044-repair-install-classifier-and-clean-reinstall-handoff.md)

## Predecessor report and review

[`reports/CNX-20260824-043-harden-namespace-ownership-and-migration.md`](reports/CNX-20260824-043-harden-namespace-ownership-and-migration.md)

[`reviews/CNX-20260824-043-harden-namespace-ownership-and-migration.md`](reviews/CNX-20260824-043-harden-namespace-ownership-and-migration.md)

Retain Task 043's exact manifest/plugin/legacy/lint hardening. Repair only unrelated npm-project classification, default backup-enabled clean-reinstall composition, skip-plugin preflight, and post-create ownership verification.

## Human direction

The operator said to continue. CogentNexus-Ecosystem and staged-capability-loop remain paused and excluded.

## Purpose

Ensure the repository implementation can later proceed to separately authorized live clean uninstall/install/reinstall acceptance without false classification, self-created backup conflict, or partial mutation.

## Safety

Repository-only repair in one isolated full clone. No Git worktree creation, live workspace/config/runtime/install/clean-reinstall/reset/uninstall, Gateway/Ollama/scheduler/service action, Procmon action, Ecosystem work, merge, tag, or release.

Do not repeat Task 041/042 or Task 043 wholesale.

## Duplicate fence

If the matching Task 044 report exists at freshly fetched HEAD, do not repeat implementation or publish a duplicate.
