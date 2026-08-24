# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260824-043`  
Updated: 2026-08-24 07:20 ICT  
Owner: ChatGPT  
Executor: Codex

## Active task

[`tasks/CNX-20260824-043-harden-namespace-ownership-and-migration.md`](tasks/CNX-20260824-043-harden-namespace-ownership-and-migration.md)

## Predecessor report and review

[`reports/CNX-20260824-042-openclaw-namespace-isolation.md`](reports/CNX-20260824-042-openclaw-namespace-isolation.md)

[`reviews/CNX-20260824-042-openclaw-namespace-isolation.md`](reviews/CNX-20260824-042-openclaw-namespace-isolation.md)

Task 042's broad namespace implementation is retained. Its PASS claim is blocked only on exact ownership verification, partial-new-state handling, actual plugin-path ownership, legacy-removal proof, clean-reinstall fail-closed behavior, and complete namespace lint.

## Human direction

The operator said to continue after the Task 042 report appeared.

CogentNexus-Ecosystem and staged-capability-loop are explicitly paused because they are optional and not part of the current live baseline. Do not touch them.

## Purpose

Make CogentNexus-OpenClaw v0.9.3 safe enough to proceed later to separately authorized live uninstall/install acceptance without risking OpenClaw, Ollama, CogentNexus-HermesAgent, or unrelated data.

## Safety

Repository-only repair in one isolated full clone. No Git worktree creation, live install/config/runtime/reset/uninstall, Gateway/Ollama/scheduler/service action, Procmon action, retained-evidence cleanup, Ecosystem work, merge, tag, or release.

Do not repeat Task 041 or the broad Task 042 rename.

## Duplicate fence

If the matching Task 043 report exists at freshly fetched HEAD, do not repeat implementation or publish a duplicate.
