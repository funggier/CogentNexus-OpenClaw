# CNX-20260823-022 — Diagnose Unexpected Task 020 Worktree HEAD

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Execution mode: `AUTO`  
Predecessor: `CNX-20260823-021` (`ACCEPT` safe blocked)

## Objective

Determine read-only whether unexpected Task 020 target HEAD `2bda9b71952f838da515e046fb3efa10a75f2089` is published/reachable and what exact changes it contains. Do not remove or modify any worktree.

## Execution control

Exact Task 022 control path:

`C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-022`

It may be created from fetched remote HEAD or adopted if already watcher-created, but adoption requires exact path/registration, fetched detached HEAD, complete cleanliness, no ignored/untracked content, no Git operation, and no unpublished commit. Any mismatch is `BLOCKED_CONTROL_COLLISION`; no fallback or suffix.

## Exact diagnostic targets

Task 020 target:

`C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-020`

Expected observed HEAD:

`2bda9b71952f838da515e046fb3efa10a75f2089`

Task 021 control (presence/accounting only):

`C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-021`

Task 017 must not be inspected.

## Duplicate fence

Fetch remote branch; verify Task 022 `READY_FOR_CODEX` / `AUTO`; verify matching report absent. If present, stop without observation.

## Required read-only evidence

For Task 020:

- exact path and registry entry;
- exact HEAD and detached/branch state;
- full porcelain status including ignored/untracked;
- active Git operations/locks;
- commit object existence;
- commit parents, author/committer timestamps, subject, tree ID;
- exact name-status and patch/stat versus every parent;
- whether commit is reachable from any local ref and from fetched remote refs;
- whether the commit equals or contains the Task 020 report publication, and exact file/blob identities;
- reflog entries relevant to how target HEAD moved, without modifying reflogs;
- path-filtered process use, distinguishing outside inspection arguments from actual binding.

For Task 021, record only path/registration/HEAD/status/operation state and whether a process is bound to it.

Do not infer publication from a clean tree. Classify exact reachability and content.

## Results

Return exactly one:

- `PASS_UNEXPECTED_HEAD_PUBLISHED_AND_EXPLAINED`
- `BLOCKED_UNEXPECTED_HEAD_UNPUBLISHED`
- `BLOCKED_TARGET_IDENTITY_CHANGED_AGAIN`
- `BLOCKED_TARGET_DIRTY`
- `BLOCKED_TARGET_OPERATION_ACTIVE`
- `BLOCKED_TARGET_IN_USE`
- `BLOCKED_CONTROL_COLLISION`
- `BLOCKED_EVIDENCE_INCOMPLETE`
- `BLOCKED_PUBLICATION_FAILED`

Include recommended narrow cleanup identity if and only if provenance is proven. Record `Human decision required: YES|NO`.

## Prohibited

No worktree removal/creation except the exact Task 022 execution control, no restore/reset/clean/prune/force/metadata edit, no Task 017 inspection, no process action, no runtime/recovery/provider/`cnx`/OpenClaw/Ollama action, no source change, lifecycle action, merge, tag, release, or force-push.

## Report

`docs/operations/coordination/reports/CNX-20260823-022-diagnose-task020-unexpected-head.md`

Commit begins `report: CNX-20260823-022`. Re-fetch and re-check the report fence before push. Stop after publication and exact control-cleanup accounting.
