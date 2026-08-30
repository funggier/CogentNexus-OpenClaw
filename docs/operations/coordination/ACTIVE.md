# Active Coordination Task

Status: `IN_PROGRESS_CHATGPT`
Execution mode: `REPOSITORY_WINDOWS_INSTALL_OVER_OBSERVABILITY_DIAGNOSIS`
Current authorization: `CNX-20260830-158_WINDOWS_INSTALL_OVER_OBSERVABILITY_DIAGNOSIS`
Task ID: `CNX-20260830-158`
Updated: 2026-08-30 ICT
Owner / executor / reviewer: ChatGPT

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative.

## Active task

[`tasks/CNX-20260830-158-windows-install-over-observability-recovery-diagnosis.md`](tasks/CNX-20260830-158-windows-install-over-observability-recovery-diagnosis.md)

Task 157 completed its single authorized live attempt and is durably reviewed **BLOCKED** at:

`docs/operations/coordination/reviews/CNX-20260830-157-repaired-candidate-windows-install-over-health-proof-review.md`

The repaired candidate was not proven installed. Dashboard semantic reacceptance remains blocked.

## Task-158 execution contract

ChatGPT must:

1. diagnose the established Windows installer path from repository source/tests and Task-157 durable evidence;
2. use TDD for any production observability change;
3. add only the minimum stable stage/timestamp/elapsed/exit diagnostics needed to localize a later interrupted install-over;
4. preserve classification, passthrough/native handoff, plugin replacement, rollover, rollback, ownership, and runtime semantics;
5. run focused and relevant validation on the exact repair candidate;
6. publish the Task-158 report and explicit non-independent ChatGPT self-review;
7. only after ACCEPT, create a separate Hermes live-retry task.

## Evidence conclusion carried from Task 157

The complete raw `install-over.txt` remained on the real Windows executor and was not published into GitHub. The durable report establishes progress through native handoff, skill replacement, validation, host initialization, and database snapshot, but does not identify which later external substage consumed the executor window.

Repository inspection shows the installer lacks stable installer-owned start/completion/elapsed diagnostics around the critical late substages. Task 158 addresses diagnosability only; root cause remains unproven.

## Hard fence

No live Windows mutation; no Dashboard semantic Send or Dashboard semantic interaction; no reset/uninstall/reinstall; no runtime/database/semantic mutation; no retry/timeout/rollback/process-kill behavior change; no dependency upgrade; no OpenClaw source patch; no merge/tag/release/publish/promotion; no force push.
