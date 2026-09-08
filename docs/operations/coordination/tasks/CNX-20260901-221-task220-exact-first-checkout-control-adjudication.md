# CNX-20260901-221 — Task-220 Exact First-Checkout Control Adjudication

Status: `READY_FOR_HERMES`
Date: 2026-09-01 ICT
Parent: `CNX-20260901-220`
Repair parent: `CNX-20260831-198`
Executor: Hermes / authenticated Windows repository operator
Coordinator / final reviewer: ChatGPT

## Purpose

Close the remaining ambiguity in Task 220 by determining whether the static CRLF bytes are produced by a **direct first materialization** of exact commit `4e31dbd79cd4c0a7eb161888c14221f0ae03bcc0` under Windows Git policy, or are carried over from an earlier checkout/attribute state before switching to that commit.

This task is diagnostic-only. It must not modify product source, run the installer, or touch live CogentNexus/OpenClaw state.

## Immutable/public authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No Release/tag/asset mutation is authorized.

## Accepted predecessor facts

Task 219:

- genuine real-boundary RED proved 43 generated `dist` CRLF/LF differences;
- bounded generated-`dist` canonicalizer lineage closes those generated differences;
- remaining package mismatch is outside `dist` in `README.md`, `openclaw.plugin.json`, and `scripts/bootstrap-ticket-db.mjs`.

Task 220:

- Git objects at `4e31dbd...` for those static files are LF-only;
- the measured working tree already had CRLF at D0 before npm/build;
- npm/build/validation did not change those static bytes;
- `core.autocrlf=false` control yielded LF-only working-tree bytes;
- Task 220 used a two-stage checkout: clone branch HEAD first, then detach to `4e31dbd...`.

Independent review disposition:

`ACCEPT_PARTIAL__STATIC_DIVERGENCE_PRE_NPM_PROVEN__EXACT_FIRST_CHECKOUT_CONTROL_REQUIRED`

## Critical ambiguity

At Task-220 execution time branch ancestry already contained:

`b081d55c4ffa5fcb03931dc320d39bdcf92a6cf5`

which differs from `4e31dbd...` only in `.gitattributes` (`text eol=lf` -> `-text` for the four static package paths). The static payload blobs themselves are unchanged between those two commits.

Therefore a normal clone followed by checkout to the older commit is not sufficient to prove direct target-commit checkout behavior. Task 221 must make `4e31dbd...` the first working-tree materialization in its primary controls.

## Hard fence

Authorized:

- disposable isolated Git clones/worktrees under `%LOCALAPPDATA%\Temp`;
- read-only Git object/config/attribute/index/worktree inspection;
- exact byte hashing and newline counting;
- safe forced rematerialization inside disposable clones only;
- report publication.

Not authorized:

- product/source/test/workflow edits or commits;
- installer/install-over;
- `cnxclaw` lifecycle actions;
- live OpenClaw plugin/config mutation;
- Gateway restart;
- live SQLite/ownership/transaction mutation;
- provider/model substitution;
- Discord traffic;
- Release/tag/asset mutation;
- force push/history rewrite;
- unrelated process termination.

## Phase A — fresh authority

1. Read fresh branch HEAD and record it.
2. Confirm no relevant installer/lifecycle process is active.
3. Preserve live runtime read-only only if needed to prove no mutation.
4. Record Git executable/version and all effective config origins for:
   - `core.autocrlf`
   - `core.eol`
   - `core.safecrlf`

Unexpected product/runtime mutation -> stop `BLOCKED_STATE_DRIFT`.

## Phase B — object identity

For exact commit `4e31dbd...`, record object SHA and byte metrics for:

- `plugins/cogentnexus-openclaw/package.json`
- `plugins/cogentnexus-openclaw/README.md`
- `plugins/cogentnexus-openclaw/openclaw.plugin.json`
- `plugins/cogentnexus-openclaw/scripts/bootstrap-ticket-db.mjs`
- `.gitattributes`

For each static path record SHA-256, byte count, CRLF count, LF-only count. Object bytes are the authority baseline.

Also prove via compare that `4e31dbd... -> b081d55...` changes only `.gitattributes` and not these static blobs.

## Phase C — exact first materialization controls

Create three independent disposable repositories where no working tree is populated before the exact target is selected. Prefer one of:

```text
git clone --no-checkout <repo> <dir>
# set local config control
# checkout --detach 4e31dbd...
```

or:

```text
git init <dir>
git remote add origin <repo>
git fetch --no-tags origin 4e31dbd...
# set local config control before checkout
# checkout --detach FETCH_HEAD
```

The critical requirement is: **the first working-tree materialization must be exact `4e31dbd...`**.

Controls:

### C1 inherited/default

Do not set local `core.autocrlf`; inherit machine config.

### C2 explicit true

Before first checkout:

```text
git config core.autocrlf true
```

### C3 explicit false

Before first checkout:

```text
git config core.autocrlf false
```

Immediately after first materialization and before npm/build, capture for all four static paths:

- worktree SHA-256;
- byte count;
- CRLF/LF-only count;
- object-vs-worktree equality;
- `git status --porcelain=v2`;
- `git ls-files --eol -- <path>`;
- `git check-attr -a -- <path>`;
- config plus origin.

No npm command is needed for the primary classification.

## Phase D — two-stage reproduction

Separately reproduce Task-220 topology:

```text
git clone <current branch HEAD> <dir>
git checkout --detach 4e31dbd...
```

under inherited/default config.

Capture the same immediate evidence and compare to C1.

If C1 and D differ, classify checkout-state carry-over as proven.

If C1 and D are identical, the first-materialization control supports the direct checkout-policy hypothesis.

## Phase E — forced rematerialization control

Only in the disposable D tree, if it has CRLF while the target attributes say `text eol=lf`, perform one safe explicit rematerialization method without editing source, for example a fresh no-checkout worktree/index materialization or a documented forced checkout-index refresh.

Record exact command and before/after bytes/status/eol attributes.

Do not use ad-hoc file rewriting or newline normalization; this phase tests Git materialization semantics only.

## Required classification

Choose exactly one primary disposition:

- `PASS_DIRECT_FIRST_CHECKOUT_AUTOCRLF_ROOT_CAUSE_PROVEN`
- `PASS_TWO_STAGE_ATTRIBUTE_CARRYOVER_ROOT_CAUSE_PROVEN`
- `PASS_MIXED_GIT_MATERIALIZATION_ROOT_CAUSE_PROVEN`
- `BLOCKED_EXACT_FIRST_CHECKOUT_CONTROL`
- `BLOCKED_STATE_DRIFT`
- `BLOCKED_EVIDENCE`

A PASS here is diagnostic closure only and does not authorize installation.

## Report

Publish:

`docs/operations/coordination/reports/CNX-20260901-221-task220-exact-first-checkout-control-adjudication.md`

The report must include:

- fresh authority HEAD;
- Git version/config origins;
- object metrics;
- C1/C2/C3 first-materialization table;
- D two-stage table;
- forced-rematerialization result if applicable;
- exact first boundary where bytes diverge;
- mutation ledger;
- final classification.

Then stop for ChatGPT review.

## Discord budget

`0 Discord Sends`.
