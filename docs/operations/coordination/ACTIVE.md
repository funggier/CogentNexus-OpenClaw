# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260824-040`  
Updated: 2026-08-24 00:44 ICT  
Owner: ChatGPT  
Executor: Codex

## Active task

[`tasks/CNX-20260824-040-classify-task038-worktree-415-path-loss.md`](tasks/CNX-20260824-040-classify-task038-worktree-415-path-loss.md)

## Predecessor report and review

[`reports/CNX-20260824-039-inventory-task038-detached-worktree.md`](reports/CNX-20260824-039-inventory-task038-detached-worktree.md)

[`reviews/CNX-20260824-039-inventory-task038-detached-worktree.md`](reviews/CNX-20260824-039-inventory-task038-detached-worktree.md)

Task 039 is reviewed `BLOCKED`.

## Proven state

The exact Task 038-created worktree is registered by the primary repository and detached at the documented Task 038 report commit. Its index and registration metadata remained stable and no process is attached.

It has 415 tracked working-tree deletions, with zero staged, non-deletion modified, untracked, ignored, conflict, submodule, sparse, nested, or active-process state.

The worktree is not clean and is not removal-eligible.

## Purpose of Task 040

Classify the exact deleted/present path selection pattern using read-only Git tree, index, path, and filesystem metadata.

Local path-set proof is delegated to Codex because ChatGPT cannot access the operator machine's exact inventory. Codex must not design a fix or claim an actor/process without direct evidence.

## Safety boundary

Use `GIT_OPTIONAL_LOCKS=0`. No tracked-file content read and no Task 027 worktree access.

No new worktree, clone, branch, repository, manifest, repair, removal, prune, checkout, reset, clean, restore, add/refresh, index rewrite, process termination, watcher/Supervisor change, Procmon launch/config/capture, retained-evidence cleanup, or CogentNexus/OpenClaw/Ollama runtime/recovery/lifecycle action.

A PASS classifies the path-loss predicate only. It authorizes no remediation or removal.

## Duplicate-execution fence

If the matching Task 040 report exists at freshly fetched HEAD, do not inspect the target again or create another report. Stop awaiting ChatGPT review.
