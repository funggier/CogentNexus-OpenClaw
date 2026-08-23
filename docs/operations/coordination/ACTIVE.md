# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260823-028`  
Updated: 2026-08-23 14:59 ICT  
Owner: ChatGPT  
Executor: Codex

## Active task

[`tasks/CNX-20260823-028-diagnose-incomplete-watcher-control.md`](tasks/CNX-20260823-028-diagnose-incomplete-watcher-control.md)

## Predecessor review

[`reviews/CNX-20260823-027-reconcile-task025-tree-index-worktree.md`](reviews/CNX-20260823-027-reconcile-task025-tree-index-worktree.md)

Task 027 is `ACCEPT` for its safe precondition stop only. Its watcher-provided control contained many tracked/indexed paths absent from the working tree, so the required Task 025 reconciliation remains unproven.

## Purpose

Task 028 performs a narrow read-only diagnosis of incomplete watcher control materialization, including worktree registration, configuration origins, sparse-checkout state, representative tree/index/filesystem comparisons, and preservation requirements.

No checkout repair, cleanup, worktree removal, process action, or runtime/provider/lifecycle action is authorized.

## Duplicate-execution fence

If `docs/operations/coordination/reports/CNX-20260823-028-diagnose-incomplete-watcher-control.md` already exists at fetched HEAD, perform no repeated inspection and stop awaiting ChatGPT review.
