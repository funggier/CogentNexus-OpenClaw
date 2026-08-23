# CNX-20260823-032 — Diagnose Recurring Task 027 Materialization Loss

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Execution mode: `AUTO`  
Predecessor: `CNX-20260823-031` (`BLOCKED`)

## Objective

Identify, read-only, why the exact Task 027 registered worktree returned from the Task 030 verified 387/387 materialized state to 5/387 with the same 382 tracked paths absent.

Determine the narrowest evidence-supported actor/mechanism and time boundary before any new repair is authorized.

## Exact identities

Primary repository:

`C:\Users\CDQ-P\.openclaw\workspace`

Target:

`C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-027`

Required detached target HEAD:

`748b6e7accb22b6bb4a5503c9ac04265f153f9e5`

Expected common repository:

`C:\Users\CDQ-P\.openclaw\workspace\.git`

Expected indexed paths:

`387`

Observed recurring absent paths:

`382`

Accepted absent-list SHA256:

`6A078DA7D54615B67E0020D978A065171E803B0A0DFE134CE978BB2616B91FB8`

Matching report:

`docs/operations/coordination/reports/CNX-20260823-032-diagnose-recurring-task027-materialization-loss.md`

## Duplicate-execution fence

After fresh fetch, if the matching Task 032 report exists, perform no diagnostic repetition and stop awaiting review.

## Mandatory evidence collection

Use only read-only inspection.

1. Read ACTIVE, Task 032, Task 030/031 reports, and Task 030/031 reviews from freshly fetched HEAD.
2. Verify exact target registration, detached HEAD, common-dir identity, worktree administrative directory, config/sparse state, index flags, active-operation markers, locks, and current status.
3. Recompute indexed/materialized/absent counts and the canonical absent-list hash.
4. Record filesystem metadata for:
   - target directory;
   - all 5 surviving tracked paths;
   - representative absent parent directories;
   - target worktree administrative files and index;
   - Task 030/031 reports and relevant Git metadata.
5. Compare the surviving/absent pattern with the Task 029 and Task 031 evidence. Classify whether it is exactly the same 382-path set.
6. Inventory current processes read-only, including PID, parent PID, executable, start time, and command line, selecting only processes that reference:
   - the exact target path;
   - `cogentnexus-CNX-20260823-027`;
   - the common repository;
   - Git/worktree/Codex/ChatGPT watcher or indexing activity plausibly attached to the target.
7. Inventory scheduled tasks, watcher definitions, terminal sessions, Git hooks/config, maintenance settings, and repository automation whose command/action references the exact target or common repository.
8. Inspect available Windows filesystem/audit/Sysmon/event records read-only for recent create/delete/rename operations involving the exact target. If a log is unavailable or auditing was not enabled, record `NOT_AVAILABLE`; do not enable it.
9. Inspect shell/Codex task artifacts or logs only when already authorized and readable, searching for exact commands/path references that could have removed or rematerialized files. Do not read secrets or unrelated user content.
10. Perform a bounded read-only stability observation:
    - capture count/status/hash at start;
    - repeat at 30 seconds and 60 seconds;
    - record whether anything changes and correlate any change with process/event evidence.
11. Produce a remediation manifest naming:
    - evidence-supported cause or `CAUSE_NOT_PROVEN`;
    - exact actor/process/task/config if proven;
    - whether that actor is still active;
    - exact reversible containment candidate;
    - exact later restoration candidate;
    - evidence that must be captured before either action.

Do not infer an actor from process presence alone. Separate direct evidence, correlation, and unknowns.

## Report publication fence

The only authorized repository mutation is the matching report.

Stage and commit only that report path. Prohibit `git add .`, `git add -A`, `git commit -a`, deletion, reset, clean, checkout, restore, and force push. Verify the report commit changes exactly one path.

Commit begins `report: CNX-20260823-032`.

## Results

Return exactly one:

- `PASS_CAUSE_IDENTIFIED_CONTAINMENT_DEFINED`
- `PASS_CAUSE_NOT_PROVEN_SAFE_NEXT_DIAGNOSTIC_DEFINED`
- `BLOCKED_TARGET_IDENTITY_CHANGED`
- `BLOCKED_EVIDENCE_ACCESS`
- `BLOCKED_REPORT_PUBLICATION_UNSAFE`

Include `Human decision required: YES|NO`.

## Progress communication

Report meaningful progress at least approximately every 3 minutes and immediately after preflight, after process/watcher inventory, after event/log correlation, after stability observation, and on blocker. Progress updates are not pause points.

## Prohibited

No restoration or materialization write; no file/index/timestamp mutation; no worktree create/remove/re-register/prune; no reset/clean/checkout/restore/add/refresh; no process stop/kill/restart; no scheduled-task change; no audit/logging enablement; no configuration/ref/branch mutation; no Task 025 execution; no repository-reference migration; no CogentNexus/OpenClaw/Ollama runtime/provider/recovery/lifecycle action; no force push, merge, tag, or release.
