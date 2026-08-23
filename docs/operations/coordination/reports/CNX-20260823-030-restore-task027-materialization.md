# CNX-20260823-030 — Restore Task 027 Working-Tree Materialization

Status: `BLOCKED_POSTVERIFY_FAILED`

Repository: `funggier/CogentNexus-OpenClaw`
Branch: `agent/v0.9.3-recovery-reality-tests`
Primary: `C:\Users\CDQ-P\.openclaw\workspace`
Target: `C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-027`
Target HEAD: `748b6e7accb22b6bb4a5503c9ac04265f153f9e5` (unchanged, detached)

## Actions and exits

- `git fetch origin --prune` — exit 0.
- Required ancestor check for `af53fb3d19d6245552699795c638e159edc83204` — exit 0.
- Matching-report duplicate check — exit 128 (absent before run).
- Target identity/registration/common-dir checks — exit 0; exact registered target and expected common repository.
- Prestate status — exit 0; 382 deletion records, no staged/non-deletion/untracked records. Prior status capture SHA256 `23C7BA8F5B2DED772AFB5B34891A3573A0C5909866EDD9E1566840DC16F97F40`.
- Absent-path derivation — exit 0; exactly 382 paths. Canonical absent-list SHA256 `6A078DA7D54615B67E0020D978A065171E803B0A0DFE134CE978BB2616B91FB8`.
- Authorized exact NUL pathspec restore from target `HEAD` — exit 0. Pathspec SHA256 `B98921CDF052AB0048AB6377D284192918B4F52953AB0D5D8DA12E26DDF4DC50`.

## Post-repair evidence

- Target remains registered at the exact path, detached at the required HEAD, common-dir `C:\Users\CDQ-P\.openclaw\workspace\.git`.
- Tracked paths: 387; physically materialized: 387; absent: 0.
- Representative files under `.github/workflows`, coordination, skills, scripts, tests, and benchmarks exist and their `hash-object` values match the verified HEAD blobs.
- Primary repository status hash remained `5D163FCEE481E36CA026DA894188CB66EBD2972782502EE657DB5CEF4DF185B8`.

## Blocking anomaly

Required clean-status gate did not pass. `git status --porcelain=v2 --untracked-files=all` and `git diff-files --raw` report one worktree modification for:
`docs/operations/coordination/reports/CNX-20260823-027-reconcile-task025-tree-index-worktree.md`

However, `git hash-object` and the index blob both equal `d81361b07c42ff612f4f0ab7657cf4e6b9164944`, `git diff` emits no content diff, and no staged/untracked entries exist. `git update-index --really-refresh` was diagnostic only and returned exit 1 (`needs update`); no file content, ref, registration, configuration, or primary-repository change was intentionally made. This is a Git filesystem/stat-cache verification anomaly that prevents claiming the mandatory clean gate.

Proven: exact preconditions, exact-path restore, complete 387/387 materialization, representative blob identity, target/primary identity preservation, and no runtime/process side effects.

Not proven: clean post-repair status; whether the anomalous status is transient filesystem metadata or a durable worktree condition.

## Safety and recommendation

No worktree was created/removed/re-registered; no reset, clean, checkout, broad restore, config/ref mutation, runtime/provider/process action, or force push occurred. No unique content was overwritten by the restore because prestate had only the 382 expected deletions.

Safest next step: open a narrow diagnostic/fix task for this single path/stat anomaly. Do not repeat the 382-path restore until the clean-status gate can be demonstrated. Human decision required: NO.

Duplicate-execution accounting: matching report was absent before execution; the authorized restoration was executed once only. The only repository mutation beyond target materialization was publication of this matching report.