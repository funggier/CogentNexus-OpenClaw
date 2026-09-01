# CNX-20260901-220 — Task-219 Static Payload Checkout-Boundary Adjudication

Status: `READY_FOR_HERMES`
Date: 2026-09-01 ICT
Parent: `CNX-20260901-219`
Repair parent: `CNX-20260831-198`
Executor: Hermes / authenticated Windows repository operator
Coordinator / final reviewer: ChatGPT

## Purpose

Determine exactly where three static installable plugin files change from repository/CI LF bytes to the CRLF Windows working-tree bytes observed in Task 219. Do this before any further source/build repair.

Task 220 is diagnostic only. It must not modify or install the live CogentNexus/OpenClaw runtime and must not push product/source changes.

## Authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Generated-`dist` GREEN repair commit retained as evidence:

`9af329b4de7c02fda35b467d84e76bb0f0bb0944`

Primary static-checkout candidate under adjudication:

`4e31dbd79cd4c0a7eb161888c14221f0ae03bcc0`

Retained authoritative package proof for that lineage:

```text
artifact: 9807757662
payload files: 192
CI fingerprint: e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
```

Later `-text` experiment, diagnostic comparison only:

`b081d55c4ffa5fcb03931dc320d39bdcf92a6cf5`

Task-219 remaining differing paths:

```text
plugins/cogentnexus-openclaw/README.md
plugins/cogentnexus-openclaw/openclaw.plugin.json
plugins/cogentnexus-openclaw/scripts/bootstrap-ticket-db.mjs
```

Task 219 reports zero remaining `dist` differences; this task must not reopen the generated-output repair unless new evidence directly contradicts that result.

## Hard fence

Authorized:

- isolated fresh clones/worktrees under `%LOCALAPPDATA%\Temp`;
- read-only Git object/config/attribute inspection;
- `npm ci`, `npm run build`, and `npm run plugin:validate` inside isolated evidence trees;
- byte hashes/newline counts/status capture;
- disposable-index experiments such as `git add --renormalize` inside an isolated clone only;
- report publication.

Not authorized:

- product/source/test/workflow edits or commits other than the Task-220 report;
- installer/install-over/reset/uninstall/reinstall;
- `cnxclaw` lifecycle actions;
- live OpenClaw plugin/config mutation;
- Gateway restart;
- live ownership/staging/transaction/SQLite write;
- provider/model substitution;
- Discord Send/API/bot traffic;
- Release/tag/asset mutation;
- force push/history rewrite.

## Phase A — fresh authority and live preservation

1. Read fresh remote branch HEAD and current coordination state.
2. Confirm there is no active Task-219/installer/lifecycle process residue relevant to this diagnostic task.
3. Read live state only enough to prove preservation:
   - controller mode/generation;
   - Gateway health;
   - selected provider;
   - delivery/recovery readiness;
   - Task-205 cancellation remains inert.
4. Unexpected live mutation or active installer/lifecycle process -> `BLOCKED_ACTIVE_PROCESS`.

## Phase B — repository-object truth

For exact commit `4e31dbd...`, for all four static package paths covered by its `.gitattributes` (including `package.json` as control):

1. Record `git rev-parse <commit>:<path>` object SHA.
2. Read exact object bytes using `git cat-file blob` into evidence files without text-mode rewriting.
3. Record SHA-256, byte size, CRLF count, lone-LF count.
4. Record `.gitattributes` object bytes and SHA.
5. Prove whether repository object bytes themselves are LF-only or contain CRLF.

Do not infer line endings from ordinary console rendering.

## Phase C — Git policy truth

In a fresh isolated clone targeting exact `4e31dbd...`, before any npm command:

Record with origin/source where applicable:

```text
git config --show-origin --get core.autocrlf
git config --show-origin --get core.eol
git config --show-origin --get core.safecrlf
git config --show-origin --get core.attributesfile
git config --show-origin --get-regexp '^core\.(autocrlf|eol|safecrlf|attributesfile)$'
```

For each four static paths record:

```text
git check-attr text eol -- <path>
git check-attr -a -- <path>
git ls-files --eol -- <path>
git status --porcelain=v2 -- <path>
```

Also capture checkout method exactly (clone/worktree commands and any `-c` options).

## Phase D — checkpoint byte trace

For each of these checkpoints, record the same four path SHA-256/size/CRLF/LF counts plus `git ls-files --eol` and `git status --porcelain=v2`:

D0. immediately after exact checkout, before npm;
D1. after `npm ci` in `plugins/cogentnexus-openclaw`;
D2. after `npm run build`;
D3. after `npm run plugin:validate`.

At every transition, identify exactly which path bytes changed. If the first CRLF appears at one checkpoint, preserve before/after hashes and stop blaming earlier boundaries.

Also compute repository-supported payload fingerprint after D2/D3 and compare with retained CI fingerprint where applicable.

## Phase E — controlled checkout comparison

Create separate disposable fresh clones of exact `4e31dbd...` under otherwise identical conditions:

1. default inherited Git config;
2. explicit `-c core.autocrlf=false` checkout;
3. explicit `-c core.autocrlf=true` checkout.

Do not edit source. For each clone capture effective attributes, `git ls-files --eol`, working-tree newline counts, status and fingerprints after the normal build path.

The goal is to identify whether global/local Git configuration changes the outcome despite `text eol=lf`.

## Phase F — renormalization diagnostic

Only inside a disposable clone of `4e31dbd...`:

1. Capture clean/dirty status before.
2. Run `git add --renormalize` limited to the four static paths.
3. Capture `git diff --cached --binary -- <paths>` and staged blob SHAs.
4. Do **not commit**.
5. Determine whether the existing repository blobs are inconsistent with the declared `text eol=lf` normalization contract.
6. Destroy/discard the clone after evidence capture.

This phase diagnoses object/index normalization only; it is not an authorized repository fix.

## Phase G — `b081d55...` comparison

Repeat only the minimum object/attribute/immediate-checkout evidence for `b081d55...` to explain why the later `-text` experiment did or did not alter behavior.

Do not treat `-text` as preferred repair merely because it changes a checkout classification.

## Required classification

Choose exactly one primary disposition:

- `PASS_CHECKOUT_CONFIG_ROOT_CAUSE_PROVEN`
- `PASS_REPOSITORY_BLOB_NORMALIZATION_ROOT_CAUSE_PROVEN`
- `PASS_POST_CHECKOUT_COMMAND_MUTATION_ROOT_CAUSE_PROVEN`
- `PASS_MULTIPLE_STATIC_BYTE_CAUSES_PROVEN`
- `BLOCKED_STATIC_BYTE_ROOT_CAUSE`
- `BLOCKED_ACTIVE_PROCESS`
- `BLOCKED_EVIDENCE`

A PASS is diagnostic closure only. It does not authorize installation.

## Report

Publish:

`docs/operations/coordination/reports/CNX-20260901-220-task219-static-payload-checkout-boundary-adjudication.md`

The report must include:

- exact Git configs and their origin;
- exact object SHA + byte/newline metrics;
- effective attributes;
- `git ls-files --eol` at each checkpoint;
- first checkpoint where each static file diverges;
- status cleanliness at every checkpoint;
- default/autocrlf=false/autocrlf=true comparison;
- renormalization diagnostic;
- final root-cause classification;
- mutation ledger proving no live/product mutation.

Then stop for ChatGPT review.

## Discord budget

`0 Discord Sends`.
