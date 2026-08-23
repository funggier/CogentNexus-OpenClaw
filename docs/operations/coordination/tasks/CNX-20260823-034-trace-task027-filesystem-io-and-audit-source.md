# CNX-20260823-034 — Trace Task027 Filesystem I/O and Audit Deletion-Capable Source

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Execution mode: `AUTO`  
Predecessor: `CNX-20260823-033` (`ACCEPT`)

## Objective

Collect the single accepted next diagnostic: a bounded filesystem I/O trace focused on the exact Task 027 worktree, while independently auditing repository source for code paths capable of materializing, deleting, cleaning, pruning, resetting, or recycling CogentNexus/Codex worktrees.

Distinguish source capability, configured reachability, and observed runtime execution. Do not infer causation from capability alone.

## Exact identities

Primary repository: `C:\Users\CDQ-P\.openclaw\workspace`

Target: `C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-027`

Required detached HEAD: `748b6e7accb22b6bb4a5503c9ac04265f153f9e5`

Expected common repository: `C:\Users\CDQ-P\.openclaw\workspace\.git`

Accepted absent-list SHA256: `6A078DA7D54615B67E0020D978A065171E803B0A0DFE134CE978BB2616B91FB8`

Matching report: `docs/operations/coordination/reports/CNX-20260823-034-trace-task027-filesystem-io-and-audit-source.md`

## Duplicate-execution fence

After a fresh fetch, if the matching Task 034 report exists, do not repeat the trace or source audit. Stop awaiting review.

## Preflight

Revalidate target registration, detached HEAD, common-dir identity, counts, status, and absent-list hash. If identity differs, stop.

Inventory already-installed tracing facilities only (for example an existing Procmon, WPR/ETW facility, or another already-authorized tool). Do not download/install software, enable persistent auditing, change policy, or elevate privileges.

## Bounded trace

If a suitable already-installed trace facility is available:

1. configure it only for the exact target path and filesystem create/write/delete/rename/set-disposition operations;
2. capture initiator PID/process image, operation, exact path, result, and UTC timestamp;
3. run for at most 10 minutes;
4. do not restore/materialize any absent path merely to provoke activity;
5. stop only the diagnostic trace started by this task;
6. export the filtered trace to a task-specific temporary directory;
7. record SHA256, byte size, start/stop UTC, command/tool/version, exit result, filter, and event count.

If no suitable facility is already available, record `TRACE_TOOL_NOT_AVAILABLE`; do not improvise an installation or system-policy change.

## GitHub/source audit

Read the current branch source and relevant historical code without mutation. Search at minimum for:

- `Remove-Item`, `rmtree`, `unlink`, `DeleteFile`, recursive directory deletion;
- `git clean`, `git reset`, `git restore`, `git checkout`, `git worktree remove/prune`;
- worktree creation, cleanup, disposal, recycling, task-finalization, scheduled watcher cleanup;
- exact patterns `cogentnexus-CNX-`, `.openclaw\\worktrees`, Task 027 target construction;
- CogentNexus Supervisor/host code reachable from `host_control_v092.py ... supervisor tick --execute-safe`.

For every relevant match record repository path, line/function, exact operation, call chain or configured entry point, guard/preconditions, target scope, and whether it can reach the exact Task 027 path.

Classify each match exactly:

- `CAPABLE_AND_RUNTIME_OBSERVED`
- `CAPABLE_CONFIGURED_NOT_OBSERVED`
- `CAPABLE_NOT_REACHABLE_FOR_TARGET`
- `NOT_DELETION_CAPABLE`

A source match without trace/log evidence cannot be `CAPABLE_AND_RUNTIME_OBSERVED`.

## Correlation

Correlate trace events, PID/process inventory, scheduled-task configuration, Task 030–033 UTC timeline, and source call paths. Name an actor only from direct execution evidence.

## Report/evidence

Store local evidence only under a task-specific temporary directory and publish its exact paths/hashes in the report. The only repository mutation is the matching report. Stage/commit exactly that report path; prohibit `git add .`, `git add -A`, `git commit -a`, deletion, reset, clean, checkout, restore, and force push.

Commit begins `report: CNX-20260823-034`.

## Results

Return exactly one:

- `PASS_ACTOR_PROVEN`
- `PASS_SOURCE_CAPABILITY_MAPPED_NO_ACTOR`
- `BLOCKED_TARGET_IDENTITY_CHANGED`
- `BLOCKED_TRACE_TOOL_UNAVAILABLE_AND_SOURCE_INSUFFICIENT`
- `BLOCKED_REPORT_PUBLICATION_UNSAFE`

Include `Human decision required: YES|NO`.

## Progress communication

Report meaningful progress approximately every 3 minutes and immediately after preflight/tool discovery, trace start/stop, source audit, correlation, and blocker. Progress updates are not pause points.

## Prohibited

No restoration/materialization; no target/index/timestamp/config/ref/worktree mutation; no worktree create/remove/re-register/prune; no reset/clean/checkout/restore/add/refresh; no process/task/watcher/Supervisor state change except starting/stopping the bounded diagnostic trace itself; no software install/download; no audit/policy enablement; no Task 025 execution; no repository-reference migration; no CogentNexus/OpenClaw/Ollama runtime/provider/recovery/lifecycle action; no process kill or process-tree operation; no force push, merge, tag, or release.
