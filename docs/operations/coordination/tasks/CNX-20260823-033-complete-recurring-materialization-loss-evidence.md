# CNX-20260823-033 — Complete Recurring Materialization-Loss Evidence

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Execution mode: `AUTO`  
Predecessor: `CNX-20260823-032` (`REWORK`)

## Objective

Close the exact evidence gaps identified by Review 032 without restoring files or changing any process, task, watcher, repository, index, filesystem, audit policy, or runtime state.

## Exact identities

Primary repository: `C:\Users\CDQ-P\.openclaw\workspace`

Target: `C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-027`

Required detached HEAD: `748b6e7accb22b6bb4a5503c9ac04265f153f9e5`

Expected common repository: `C:\Users\CDQ-P\.openclaw\workspace\.git`

Accepted recurring absent-list SHA256: `6A078DA7D54615B67E0020D978A065171E803B0A0DFE134CE978BB2616B91FB8`

Matching report: `docs/operations/coordination/reports/CNX-20260823-033-complete-recurring-materialization-loss-evidence.md`

## Duplicate-execution fence

After a fresh fetch, if the matching Task 033 report exists, perform no repeated inspection and stop awaiting review.

## Mandatory read-only evidence

Publish exact command, exit/access result, observed values, timestamp, and a SHA256 for each generated local evidence artifact:

1. Revalidate registration, detached HEAD, common-dir, administrative directory, indexed/materialized/absent counts, canonical absent list, and status.
2. Record exact sparse-checkout/config state, all relevant index flags, active-operation markers, locks, hooks, maintenance configuration, and worktree registration metadata.
3. Enumerate all five surviving tracked paths and capture filesystem metadata for each; capture representative absent-parent metadata and target/admin/index metadata.
4. Capture an exact filtered process inventory with PID, PPID, executable, start time, and command line for references to the target, common repository, Git/worktree, Codex/ChatGPT coordination, or relevant watcher/indexing activity. Redact secrets only.
5. Capture exact scheduled-task name/path/state/triggers/actions for candidates; separately inventory watcher definitions and terminal sessions attached to the target/common repository.
6. Record every queried Windows event channel and exact UTC time window, query command, exit/access result, and matching entries or `NOT_AVAILABLE`. Do not enable auditing.
7. Record exact authorized shell/Codex artifact locations queried, search terms, UTC bounds, command, and outcome. Do not read unrelated user content or secrets.
8. Correlate the accepted Task 030 restoration time, target/admin/index timestamps, Task 031 discovery, process starts, scheduled triggers, and available log events into one UTC timeline.
9. Return one single next target:
   - an exact actor/mechanism supported by direct evidence; or
   - `CAUSE_NOT_PROVEN` plus one exact reversible evidence-acquisition diagnostic.
   
Do not propose “and/or” containment. Do not authorize containment. If evidence distinguishes neither Supervisor nor Codex watcher, explicitly leave both unchanged.

## Report publication fence

The only authorized repository mutation is the matching Task 033 report. Stage and commit exactly that path only. Prohibit `git add .`, `git add -A`, `git commit -a`, deletion, reset, clean, checkout, restore, and force push. Verify the commit changes exactly one path.

Commit begins `report: CNX-20260823-033`.

## Results

Return exactly one:

- `PASS_SINGLE_NEXT_DIAGNOSTIC_DEFINED`
- `PASS_DIRECT_ACTOR_EVIDENCE_FOUND`
- `BLOCKED_TARGET_IDENTITY_CHANGED`
- `BLOCKED_EVIDENCE_ACCESS`
- `BLOCKED_REPORT_PUBLICATION_UNSAFE`

Include `Human decision required: YES|NO`.

## Progress communication

Report meaningful progress approximately every 3 minutes and immediately after identity/config capture, inventory capture, event/artifact correlation, timeline completion, and on blocker. Progress updates are not pause points.

## Prohibited

No restoration/materialization write; no file/index/timestamp mutation; no worktree create/remove/re-register/prune; no reset/clean/checkout/restore/add/refresh; no process stop/kill/restart; no scheduled-task or watcher change; no audit/logging enablement; no configuration/ref/branch mutation; no Task 025 execution; no repository-reference migration; no CogentNexus/OpenClaw/Ollama runtime/provider/recovery/lifecycle action; no force push, merge, tag, or release.
