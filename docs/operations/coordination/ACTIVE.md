# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260823-020`  
Updated: 2026-08-23 13:18 ICT  
Owner: ChatGPT  
Executor: Codex

## Active task

[`tasks/CNX-20260823-020-isolated-adjudication-and-task017-removal.md`](tasks/CNX-20260823-020-isolated-adjudication-and-task017-removal.md)

## Predecessor review

[`reviews/CNX-20260823-019-adjudicate-and-remove-task017-worktree.md`](reviews/CNX-20260823-019-adjudicate-and-remove-task017-worktree.md)

Task 019 is `ACCEPT` only as a safe `BLOCKED` report. Its blanket no-worktree rule conflicted with the watcher-required isolated-worktree gate, so Codex correctly stopped before target inspection or mutation.

## Purpose

Task 020 permits exactly one watcher-compatible control worktree at the named Task 020 path. From there it must adjudicate only the three named tracked deletions in the wrong-head Task 017 target.

Only if every preservation, identity, no-operation, and no-use gate passes may it restore those exact files from the target's own HEAD and remove only the exact Task 017 worktree using normal non-force Git removal.

No fallback/suffix/second worktree, force, reset, clean, broad prune, process action, runtime command, provider diagnosis, install, reset, uninstall, reinstall, source change, merge, tag, or release is authorized.

Task 011 remains deferred while RAM remains stable.

## Duplicate-execution fence

If `docs/operations/coordination/reports/CNX-20260823-020-isolated-adjudication-and-task017-removal.md` exists, perform no further observation or action and stop awaiting ChatGPT review.
