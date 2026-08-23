# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260823-019`  
Updated: 2026-08-23 13:14 ICT  
Owner: ChatGPT  
Executor: Codex

## Active task

[`tasks/CNX-20260823-019-adjudicate-and-remove-task017-worktree.md`](tasks/CNX-20260823-019-adjudicate-and-remove-task017-worktree.md)

## Predecessor review

[`reviews/CNX-20260823-018-remove-wrong-head-task017-worktree.md`](reviews/CNX-20260823-018-remove-wrong-head-task017-worktree.md)

Task 018's safe `BLOCKED_TARGET_DIRTY` report is `ACCEPT`. The exact wrong-head Task 017 worktree has three tracked report deletions and was not removed. No force, reset, clean, prune, process action, or runtime action occurred.

## Purpose

Task 019 must adjudicate only the three named tracked deletions, prove their blobs are durable and no unpublished work would be lost, re-check that no process or Git operation uses the exact target, and then:

- restore only the three exact files from the target's own HEAD;
- verify the target is completely clean;
- remove only the exact Task 017 worktree using normal non-force Git removal;
- publish a precise PASS or BLOCKED report.

It must not create another worktree or perform provider diagnosis.

No process kill, recovery rerun, runtime command, install, reset, uninstall, reinstall, source change, merge, tag, or release is authorized.

Task 011 remains deferred while RAM remains stable.

## Duplicate-execution fence

If `docs/operations/coordination/reports/CNX-20260823-019-adjudicate-and-remove-task017-worktree.md` exists, perform no further observation or action and stop awaiting ChatGPT review.
