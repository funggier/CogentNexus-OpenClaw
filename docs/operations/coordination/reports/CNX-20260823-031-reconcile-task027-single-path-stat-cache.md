# CNX-20260823-031 — Reconcile Task 027 Single-Path Stat Cache

Status: `BLOCKED_OTHER_DIRTINESS`

Repository: `funggier/CogentNexus-OpenClaw`
Branch: `agent/v0.9.3-recovery-reality-tests`
Primary: `C:\Users\CDQ-P\.openclaw\workspace`
Target: `C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-027`

## Commands and evidence

- `git fetch origin --prune` — exit 0 before inspection.
- Matching-report duplicate check — exit 128; Task 031 report absent at fetched HEAD.
- Target HEAD — `748b6e7accb22b6bb4a5503c9ac04265f153f9e5`, as required.
- Target status for exact anomalous path — `1 .D ...`; `git diff-files --raw` reports deletion of the exact path. The filesystem file is absent, so filesystem hash is unavailable; index and HEAD blob remain `d81361b07c42ff612f4f0ab7657cf4e6b9164944`.
- Target aggregate — 387 indexed, only 5 physically materialized, 382 absent.
- Exact target registration/common identity was unchanged in the observed check; no Git operation lock was observed.
- No refresh or repair mutation was executed because the mandatory gates require 387/387 materialization and the exact file to exist before any index refresh.

## Blocker

Task 030 had previously restored 387/387 paths, but this fresh Task 031 preflight observes the target back at 5/387 with the exact path absent. This is broader than the single-path stat-cache anomaly and violates the immutable pre-mutation gates. The cause of the reappearance is not established by this read-only check; repeating Task 030 restoration is explicitly prohibited by Task 031.

Proven: target commit identity, report duplicate fence, current broad materialization failure, index/HEAD blob identity for the selected path, and that no Task 031 mutation occurred.

Not proven: why the restored files disappeared again; clean status; any safe single-path stat refresh.

## Safety and recommendation

No file content, timestamp, index, ref, configuration, worktree registration, runtime, process, provider, or lifecycle mutation was performed. No restore/checkout/reset/clean/touch operation was performed. Duplicate side effect was not repeated.

Safest next step: ChatGPT should issue a new narrow diagnostic task for the recurring broad materialization loss and watcher/worktree lifecycle cause. Do not run Task 031 refresh until the target is independently proven 387/387 and the exact path exists.

Human decision required: NO.