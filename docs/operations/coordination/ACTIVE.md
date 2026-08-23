# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO_WITH_INTERACTIVE_UAC`  
Task ID: `CNX-20260824-041`  
Updated: 2026-08-24 01:20 ICT  
Owner: ChatGPT  
Executor: Codex

## Active task

[`tasks/CNX-20260824-041-capture-task027-exact-filesystem-attribution.md`](tasks/CNX-20260824-041-capture-task027-exact-filesystem-attribution.md)

## Predecessor

[`reports/CNX-20260824-040-classify-task038-worktree-415-path-loss.md`](reports/CNX-20260824-040-classify-task038-worktree-415-path-loss.md)

[`reviews/CNX-20260824-040-classify-task038-worktree-415-path-loss.md`](reviews/CNX-20260824-040-classify-task038-worktree-415-path-loss.md)

Task 040 is reviewed `ACCEPT`.

## Authorization

The operator authorized one exact-path Procmon capture for at most 10 minutes and one materialization of the exact 382 absent Task 027 paths after capture-active proof.

The PMC targets Task 027 and must not be redirected to Task 038.

## Safety

No Task 038 access, broad capture, PMC change, repeated restore, force termination, worktree creation/removal/repair/prune, watcher/Supervisor change, retained-evidence cleanup, or CogentNexus/OpenClaw/Ollama runtime/provider/recovery/lifecycle action.

Ordinary interactive UAC may require operator approval. If the matching Task 041 report already exists, do not execute again.
