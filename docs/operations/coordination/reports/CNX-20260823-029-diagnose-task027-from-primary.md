# CNX-20260823-029 — Diagnose Task 027 Control From Primary

Status: `PASS_CAUSE_IDENTIFIED_SAFE_REMEDIATION_DEFINED`

Repository path: `C:\Users\CDQ-P\.openclaw\workspace`
Affected control: `C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-027`
Branch: `agent/v0.9.3-recovery-reality-tests`
Fetched HEAD: `f9127003c6f53b37fc0c9f6983c316719ca68c50`
Required ancestor: `af53fb3d19d6245552699795c638e159edc83204` (verified, exit 0)
Task027 control HEAD: `748b6e7accb22b6bb4a5503c9ac04265f153f9e5` (detached)

## Commands/actions executed

All inspection commands were read-only, except publication of this report.

- `git -C C:\Users\CDQ-P\.openclaw\workspace fetch origin --prune` — exit 0.
- `git merge-base --is-ancestor af53fb3d19d6245552699795c638e159edc83204 origin/agent/v0.9.3-recovery-reality-tests` — exit 0.
- `git cat-file -e origin:docs/operations/coordination/reports/CNX-20260823-029-diagnose-task027-from-primary.md` — exit 128 (matching report absent).
- `git worktree list --porcelain` — exit 0; exact Task027 registration present, detached at `748b6e7accb22b6bb4a5503c9ac04265f153f9e5`, no lock/prunable annotation.
- `git -C <Task027> rev-parse --git-dir/--git-common-dir/--show-toplevel` — exit 0; git-dir is primary `.git/worktrees/cogentnexus-CNX-20260823-027`, common-dir is `C:\Users\CDQ-P\.openclaw\workspace\.git`.
- `git -C <Task027> status --porcelain=v2 --untracked-files=all` — exit 0; 382 tracked deletion records, no untracked/staged records. Full capture SHA256: `23C7BA8F5B2DED772AFB5B34891A3573A0C5909866EDD9E1566840DC16F97F40`.
- Task027 index/tree enumeration — exit 0: 387 tracked/indexed paths; 5 physically materialized; 382 absent. Absent-path list SHA256: `6A078DA7D54615B67E0020D978A065171E803B0A0DFE134CE978BB2616B91FB8`.
- Primary status capture — exit 0; 541 lines, SHA256 `5D163FCEE481E36CA026DA894188CB66EBD2972782502EE657DB5CEF4DF185B8`; primary not modified.
- Config/sparse queries — exit 0. `core.sparseCheckout`, `core.sparseCheckoutCone`, `core.worktree`, and `extensions.worktreeConfig` unset; `core.ignoreCase=true` from primary `.git/config`; `core.longpaths` unset. Task027 sparse-checkout and config.worktree files absent.
- Operation-lock inspection — exit 0; no MERGE/REBASE/CHERRY-PICK/REVERT/BISECT/index.lock artifacts in Task027 git-dir. No runtime/process/lifecycle action.

## Representative missing tracked paths

Each is in HEAD tree and index with identical blob SHA, normal `H` index flag (no skip-worktree/assume-unchanged), absent on disk, and parent directory absent:

- `.github/workflows/ps51-acceptance-smoke.yml` — `6d481a1bd09beb000c13366ae32b13e3339a21b7`
- `docs/operations/coordination/ACTIVE.md` — `e452630ab8ed6a83ed92d1b8e4ffa08ffa193dc3`
- `skills/cogentnexus/SKILL.md` — `66a91698c93d874330a5dfd62768790b0085f3ea`
- `scripts/accept-v092-windows-ps51.ps1` — `7053e4af0e19f726df5d0a865b4006fdde452e25`
- `tests/test_baseline_contract.py` — `1bcff0be86c4e3e9b228ab2f277c3eb987967147`
- `benchmarks/phase6-evaluation/README.md` — `52751fe16fe1837aa614b6a0c2b56202370aec41`

## Cause and limits

The control is an incomplete filesystem materialization of its registered Git tree: index and HEAD retain tracked paths, while the working tree has deleted 382 of 387 files. This is not explained by sparse-checkout, skip-worktree, assume-unchanged, an active Git operation, or unique local content. The evidence identifies the materialization failure, but cannot prove whether an external deletion, interrupted checkout, watcher pre-materialization race, or path/access event originally caused it.

Proven: registration/common identity, detached control HEAD, ancestor prerequisite, report absence, broad tracked deletion state, no sparse configuration, no operation locks, no unique staged/unstaged/untracked content, and representative tree/index/filesystem mismatch.

Failed: complete Task027 working-tree materialization.

Skipped/unproven: no repair/restore/removal; no runtime/process action; original deletion event and historical path/access error are not recoverable from current read-only state.

## Narrow safe remediation (proposed only; not executed)

Preserve the captures above; revalidate exact target, registration, intended commit, and locks immediately before any mutation. With explicit reviewed authorization, restore only the 382 absent tracked files from the control's own `HEAD` using a path-scoped non-force operation, then verify porcelain status, tracked/materialized counts, and representative blob hashes. Do not remove/recreate the worktree, discard unique content, alter sparse/config state, or force-push. If repair is not authorized, leave unchanged and open a separate narrow repair task.

Recommended option: ChatGPT should issue a separate explicitly authorized validation/repair task. Human decision required: NO.

Side-effect accounting: no runtime/provider/process/lifecycle action; no worktree creation/removal/repair; no checkout/reset/restore/clean/config/ref mutation; no deletion; no force push. Only mutation was publication of this matching report. Duplicate fence was checked and no prior matching report existed; no side effect was repeated.