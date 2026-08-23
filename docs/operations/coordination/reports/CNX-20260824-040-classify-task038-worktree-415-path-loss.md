# CNX-20260824-040 — Classify Task038 Worktree 415-Path Loss

Status: `PASS_PATH_LOSS_PATTERN_CLASSIFIED`

Repository: `funggier/CogentNexus-OpenClaw`
Branch: `agent/v0.9.3-recovery-reality-tests`
Fetched start HEAD: `5c6f65f687f812416374a04efde3a12b94fe9c29`
Primary: `C:\Users\CDQ-P\.openclaw\workspace`
Target: `C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260824-038`

## Read-only proof

Every target Git query used `GIT_OPTIONAL_LOCKS=0`. The matching report duplicate check returned exit 128 (absent); identity/tree/index/status/submodule queries otherwise completed normally. No manifest or checkout/index file was created.

The exact target exists, is registered by the primary repository, resolves to administrative gitdir `C:\Users\CDQ-P\.openclaw\workspace\.git\worktrees\cogentnexus-CNX-20260824-038`, shares common dir `C:\Users\CDQ-P\.openclaw\workspace\.git`, and is detached at expected HEAD `c4973137d4abce9340903498a717821ea7e333c8`.

## Canonical path sets

Canonical representation is UTF-8, ordinal-sorted paths joined with LF and no trailing LF, computed in memory.

- tracked at HEAD/index: 420
- deleted/absent: 415
- deleted-list SHA256: `DA9A667AF0DEFDDFBBFA3E91E7B5F2CDF05C63694670FCC88FCFF31840FC50F6`
- present tracked: 5
- present-list SHA256: `CBBEC27A599888B1ACF22386D8094650D7B3DA8C3B9BE93BD59DB2ECB6534CDF`

Full present allowlist:

- `.gitignore`
- `AGENTS.md`
- `README.md`
- `requirements-dev.txt`
- `VERSION`

## Distribution and predicate

Deleted top-level distribution:

- `docs` 159; `plugins` 97; `skills` 84; `tests` 40; `scripts` 16; `.github` 10; `benchmarks` 7; `templates` 2.

Deleted extension distribution:

- `.md` 191; `.ts` 87; `.py` 84; `.json` 11; `.ps1` 11; `.yml` 11; `.mjs` 6; `.sh` 3; `.cmd` 3; and one each of `.txt`, `.timer`, `.xml`, `.yaml`, `.keep`, `.gitkeep`, `.service`, `.plist`.

Present extensions: two `.md`, one `.txt`, one `.gitignore`, and one extensionless `VERSION`.

Exact deterministic predicate proven:

`deleted = every tracked path at HEAD except the five root-level paths {.gitignore, AGENTS.md, README.md, requirements-dev.txt, VERSION}`.

All directory-contained tracked paths are absent; no materialized directory subtree remains. This is not an extension/filename class beyond the exact five-file root allowlist.

## Index/tree/filesystem metadata

- `git ls-files -v`: all 415 deleted paths and all 5 present paths have normal `H` flags; no skip-worktree or assume-unchanged selection distinguishes the sets.
- HEAD tree: 416 mode `100644` blobs and 4 mode `100755` blobs.
- Deleted tree payload total: 2,674,422 bytes; present tree payload total: 12,127 bytes. Blob contents were not opened.
- Exact filesystem contains only `.git` indirection plus the five present files; no directories, junctions, or reparse points.
- Present file byte/timestamp metadata: `.gitignore` 372 bytes, `AGENTS.md` 1,653, `README.md` 10,396, `requirements-dev.txt` 18, `VERSION` 7; creation/write times fall at `2026-08-23T17:34:48.6774552Z` through `17:34:48.7569195Z`; all normal Archive attributes and not reparse points.
- Sparse-checkout/config.worktree, submodules, nested repositories, operation-in-progress locks, locked/prunable registration annotations: absent. Administrative `AUTO_MERGE` metadata exists and was preserved.
- `core.ignoreCase=true` from primary `.git/config`.
- Narrow process query excluding its own inventory process found zero attachment to the exact target.

## Durable comparison

Committed Task030–034 evidence for Task027 recorded 387 tracked / 5 present / 382 absent with the same five present root paths and absent-list SHA256 `6A078DA7D54615B67E0020D978A065171E803B0A0DFE134CE978BB2616B91FB8`.

Task038 has 33 additional tracked paths at its later HEAD, so its deleted count/hash differ, but its selection predicate is structurally identical: all tracked paths except the same five root allowlist are absent. This proves the same mass-loss signature class, not an actor or causal process.

## Metadata preservation and safety

Canonical pre/post administrative metadata SHA256 were identical:
`B7F6A99C97C5964F1341550037B92E2319E16BDB1F922646CA39D626B477F62E`.

Primary tracked status was empty before publication preparation, so no unrelated staged/unstaged tracked state was eligible for inclusion.

Direct evidence proves the deterministic path predicate and structural match. It does not prove who/what removed the paths, the exact time, or whether the same actor affected Task027 and Task038.

No worktree/index/tracked path/process/runtime/Procmon state was modified. No worktree create/remove/repair/prune, checkout/reset/clean/restore/add/refresh, process action, watcher/Supervisor action, or runtime action occurred. No side effect was repeated.

Human decision required: NO.