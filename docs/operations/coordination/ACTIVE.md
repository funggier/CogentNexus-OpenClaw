# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260823-025`  
Updated: 2026-08-23 13:41 ICT  
Owner: ChatGPT  
Executor: Codex

## Active task

[`tasks/CNX-20260823-025-publish-task020-from-immutable-blob.md`](tasks/CNX-20260823-025-publish-task020-from-immutable-blob.md)

## Predecessor review

[`reviews/CNX-20260823-024-publish-verified-task020-report.md`](reviews/CNX-20260823-024-publish-verified-task020-report.md)

Task 024 is `ACCEPT` for its safe blocked execution. It detected that worktree-represented bytes differed by one byte from the accepted immutable Git blob and correctly refused publication without side effects.

## Purpose

Task 025 reads exact publication bytes directly from immutable Git blob `361be921ae0b70124769d1d8b5a2f33d1b277d88`, verifies its accepted SHA256/size/line count, and publishes only if the indexed and remotely fetched destination retain the same blob identity.

No checked-out source file may supply publication bytes. No worktree cleanup or runtime/provider/lifecycle action is authorized.

## Duplicate-execution fence

If either the Task 020 destination report or `docs/operations/coordination/reports/CNX-20260823-025-publish-task020-from-immutable-blob.md` already exists at fetched HEAD, perform no publication or repeated action and stop awaiting ChatGPT review.
