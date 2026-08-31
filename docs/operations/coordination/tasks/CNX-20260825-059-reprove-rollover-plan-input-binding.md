# CNX-20260825-059 — Re-prove Rollover Plan Input Binding

Status: `READY_FOR_HERMES`

Execution mode: `MANUAL_WITH_HUMAN_GATE`

Current authorization: `PHASE_A_PLAN_ONLY`

Owner: ChatGPT

Executor: Hermes after the operator's manual signal

## Goal

Regenerate the CogentNexus-OpenClaw v0.9.3 plugin-generation rollover plan from a fresh live read-only checkpoint while proving an unambiguous one-to-one binding between the single raw OpenClaw inventory capture, the exact file supplied to the accepted planner, and the published raw/normalized inventory hashes.

This task exists only because Task 058 was reviewed `REWORK_INVENTORY_CAPTURE_BINDING_AMBIGUOUS`. It must correct that evidence defect without weakening any Task 058 safety gate.

No recovery apply or other live mutation is authorized.

## Required source

Use a new fresh isolated full clone of:

`funggier/CogentNexus-OpenClaw`

Branch:

`agent/v0.9.3-recovery-reality-tests`

Require the following commits as ancestors before any live inspection:

- Task 057 accepted implementation `f379e5c5d8dddb144cb0d1991b645b16055e1303`;
- Task 057 accepted report `da3525c38c24f76e19c977e28446603b8c7c7063`;
- Task 057 accepted review `0bfeefe9e889a4f336f8860efc9dcae0f73af7ad`;
- Task 058 report `1650436aabb5d9c384e44a0e10013047090b7729`;
- Task 058 REWORK review `0e93970e145c8795d6578b8a4df6d2f198f6b3d9`.

Never checkout, reset, clean, repair, or mutate the primary repository at:

`C:\Users\CDQ-P\.openclaw\workspace`

## Non-reuse rule

Task 058 is not an accepted planning checkpoint.

Do not use any Task 058 inventory file, recapture, plan JSON, or plan SHA-256 as Task 059 planning input.

The rejected Task 058 plan SHA-256:

`360393b0ac8a9ffee0ad603e67efb23b48fe06a7f5e9719d0bc18d03ace76c2c`

must not be reused, approved, or supplied to `rollover-apply`.

Task 058 retained evidence may be read only if needed to understand the review defect; it must not be copied into the Task 059 evidence chain.

## Evidence boundary

Before any live inspection, create a new unique retained directory under:

`%LOCALAPPDATA%\Temp\cnx059-rollover-plan-<UTC-token>`

Retain at minimum:

- fetched repository HEAD and clean status;
- UTC transcript with exact commands and exit codes;
- redacted preflight/poststate JSON;
- exactly one raw OpenClaw plugin inventory file;
- a text record of that raw file's SHA-256 and size immediately after capture;
- the fresh machine-generated plan JSON;
- independent plan SHA-256;
- bounded verification output;
- report draft and publication verification.

Do not record secrets, tokens, API keys, full configs, environment dumps, or unrelated user data.

## Duplicate and concurrency fence

Before execution:

- fetch the coordination branch and require local/remote HEAD equality;
- verify all required ancestors;
- verify the new isolated clone is clean;
- verify `ACTIVE.md`, `STATUS.md`, and this task all agree on `READY_FOR_HERMES` / `PHASE_A_PLAN_ONLY`;
- verify no completed matching Task 059 report exists;
- prove zero concurrent installer, uninstall/reset, CogentNexus lifecycle, rollover apply, report publisher, Procmon capture, or other Task 059 executor.

A bare continuation signal authorizes only this Phase A task. It does not authorize apply.

## Phase A — fresh checkpoint only

### A1. Fresh preservation preflight

Using read-only exact-path commands, freshly prove:

- controller mode exactly PASSTHROUGH;
- startup disabled;
- no CogentNexus-OpenClaw supervisor/adapter active;
- Gateway healthy/reachable;
- Ollama healthy and model identities recorded;
- SQLite read-only integrity `ok` with bounded ticket/event/outbox/session counts;
- fresh SHA-256 values for:
  - ownership manifest;
  - controller;
  - registered policy;
  - AGENTS baseline;
  - launcher;
  - startup policy;
  - **Task 049 manifest**;
- ownership manifest still binds the retired/prior exact generation payload;
- exactly two exact canonical v0.9.3 product payload roots exist: retired manifest-owned and active replacement;
- no unexpected third product-owned payload root exists;
- unrelated plugin state remains preserved;
- primary repository is observed read-only only.

Any contradiction stops as `BLOCKED_LIVE_STATE_DRIFT` with zero live mutation.

### A2. Single immutable OpenClaw inventory capture

Invoke exactly once total for Task 059:

```powershell
openclaw plugins list --json
```

Redirect its stdout directly into exactly one uniquely named raw inventory file inside the Task 059 evidence directory, for example:

`task059-openclaw-plugins-list.raw.json`

Hard requirements:

1. this is the only `openclaw plugins list --json` invocation in Task 059;
2. do not recapture;
3. do not overwrite, replace, rename, normalize, rewrite, or hand-edit the raw file;
4. immediately after capture compute and record its exact byte size and SHA-256;
5. all subsequent inventory verification must parse this exact retained raw file;
6. the planner input must be this exact retained raw file path;
7. do not create a `before-recapture`, `after-recapture`, transformed inventory, or substitute planner-input file.

Require from that single file exactly one canonical `cogentnexus-openclaw` registration with version `0.9.3`, expected active replacement `rootDir`, expected disabled state, and exact packageName if present. If packageName is absent, package identity must be proven by the accepted Task 057 planner from the bound payload.

### A3. Generate exactly one fresh machine-produced plan

Run the accepted planner from the fresh isolated clone:

```powershell
python <isolated-clone>\skills\cogentnexus-openclaw\scripts\namespace_ownership.py rollover-plan `
  --root "C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw" `
  --workspace "C:\Users\CDQ-P\.openclaw\workspace" `
  --app-data "C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw" `
  --inventory-json <exact-task059-raw-inventory-path> `
  --plan <task059-rollover-plan.json>
```

Run `rollover-plan` exactly once.

Do not hand-author or edit the generated plan.

Compute the plan SHA-256 independently and require exact equality with the planner-reported plan SHA-256.

### A4. Verify input binding and all plan safety bindings

All verification must use the single A2 raw inventory file already captured. Never call OpenClaw inventory again.

Publish and verify at minimum:

- exact raw inventory file path;
- exact raw inventory byte size;
- exact raw inventory SHA-256;
- proof that the A3 `--inventory-json` argument is that same exact path;
- planner-normalized inventory SHA-256 recomputed by parsing that exact raw file;
- normalized active registration SHA-256;
- schema/operation/product/version exactness;
- workspace/state/OpenClaw/application-data boundaries;
- controller mode PASSTHROUGH;
- exact retired and replacement payload paths and project roots;
- exact v0.9.3 payload fingerprints and required equality;
- retired/replacement wrapper proofs and hashes;
- retired/replacement project-tree SHA-256 values;
- manifest-before SHA-256;
- manifest-after replacement path;
- exact unique nonexistent backup path under the external product rollover-backup boundary;
- same-volume atomic `os.replace` feasibility;
- exactly two expected product payload roots and no third;
- exactly one canonical active registration and no ambiguity.

If any binding fails, stop as `BLOCKED_RECOVERY_PLAN_UNSAFE`. Do not repair manually and do not weaken input.

### A5. Fresh poststate and mandatory stop

After plan verification, repeat only the bounded read-only preservation checks necessary to establish that no live state changed.

Do not rerun `openclaw plugins list --json` for poststate; use other read-only state checks and the single retained A2 inventory as the inventory evidence for this task.

Then publish only:

`docs/operations/coordination/reports/CNX-20260825-059-reprove-rollover-plan-input-binding.md`

For a valid plan:

Status: `AWAITING_HUMAN_GATE`

Result: `AWAITING_PLUGIN_GENERATION_ROLLOVER_APPLY`

The report must state clearly:

- inventory command invocation count = `1`;
- rollover-plan invocation count = `1`;
- raw inventory path/size/SHA-256;
- exact planner input path equal to that raw inventory path;
- plan path and exact fresh plan SHA-256;
- normalized inventory and active-registration SHA-256 values;
- Task 049 manifest SHA-256;
- the two exact payload roots and proof of no third;
- all other A4 bindings;
- pre/post preservation evidence;
- exact commands/exit codes;
- retained evidence directory;
- live mutation count `0`;
- remaining uncertainty.

The report commit must add only the matching Task 059 report path relative to the fetched execution HEAD. Fetch and remote-verify the report commit and blob, then stop.

## Future apply gate — not authorized

A later apply task may be created only after:

1. ChatGPT accepts the exact Task 059 checkpoint;
2. the operator explicitly approves the exact accepted Task 059 plan SHA-256;
3. a new coordination task records `PHASE_B_APPLY_AUTHORIZED`, that exact approved SHA-256, and the accepted Task 059 review commit.

No earlier plan SHA, including the rejected Task 058 SHA, is eligible.

## Result tokens

Return exactly one:

- `AWAITING_PLUGIN_GENERATION_ROLLOVER_APPLY`
- `BLOCKED_LIVE_STATE_DRIFT`
- `BLOCKED_RECOVERY_PLAN_UNSAFE`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Hard fence

No `rollover-apply`, installer, generation move/delete, ownership rewrite, plugin enable/disable/install/uninstall, `cnxclaw enable/disable/start/stop/restart/reset/uninstall`, scheduler change, supervisor creation, Gateway/Ollama/model mutation, process termination, force-kill, primary-repository mutation, Procmon/Task 027/038 action, mutation of the separate HermesAgent project/system, Ecosystem, staged-capability-loop, merge, tag, release, or archive publication.

Report meaningful progress approximately every 3 minutes and immediately after duplicate/concurrency preflight, live preflight, inventory capture, plan generation, verification, publication, or blocker.
