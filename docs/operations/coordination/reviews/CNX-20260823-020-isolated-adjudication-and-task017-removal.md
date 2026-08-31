# Review — CNX-20260823-020

Verdict: `ACCEPT`  
Reviewed: 2026-08-23  
Reviewer: ChatGPT

## Scope

Accept only the safe `BLOCKED_CONTROL_COLLISION` report. The exact Task 020 control path was already registered at the fetched authorized head before the task's absence fence, so Codex correctly stopped without inspecting Task 017 or mutating any worktree.

No cleanup, target preservation, provider diagnosis, or recovery gate is accepted.

## Evidence

Accepted:

- remote task authorization and report fence were verified;
- exact control path existed and was registered detached at `1718ea450c546abb55ad2892745f19f6e840ee5c`;
- Task 017 was not inspected;
- no worktree, file, process, runtime, or provider mutation occurred.

## Disposition

The collision is caused by the watcher creating the task control worktree before task execution. The replacement contract must distinguish an expected watcher-created exact control worktree from an unsafe pre-existing collision.

Task `CNX-20260823-021` authorizes only inspection and safe non-force removal of the exact Task 020 control worktree, using a separate exact Task 021 control worktree that may be adopted if the watcher already created it with the required identity.
