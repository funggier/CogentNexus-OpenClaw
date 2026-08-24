# CNX-20260824-058 — Fresh Plugin Generation Rollover Plan Checkpoint

Status: `READY_FOR_HERMES`

Execution mode: `MANUAL_WITH_HUMAN_GATE`

Current authorization: `PHASE_A_PLAN_ONLY`

Owner: ChatGPT

Executor: Hermes after the operator's manual signal

## Goal

Use the accepted Task 057 inventory-schema compatibility fix to independently regenerate the live CogentNexus-OpenClaw v0.9.3 plugin-generation recovery plan from a fresh read-only checkpoint. Publish the exact machine-generated plan SHA-256 and bounded bindings, then stop for ChatGPT review and a separate human authorization before any apply.

This task authorizes Phase A only. No rollover apply, generation retirement, ownership rewrite, plugin enable, startup/supervisor enable, MANAGED transition, installer, or lifecycle mutation is authorized.

## Executor substitution authorization

The operator explicitly selected Hermes to execute Task 058 instead of Codex. Hermes is authorized only as the executor of the exact Task 058 Phase A procedure below and receives no broader authority.

References to `HermesAgent` in the excluded-system safety fence mean the separate HermesAgent project/system must not be inspected, repaired, mutated, or used as a target of this task. They do not prohibit Hermes from acting as the selected executor for this CogentNexus-OpenClaw task.

## Required source

Use a fresh isolated full clone of:

`funggier/CogentNexus-OpenClaw`

Branch:

`agent/v0.9.3-recovery-reality-tests`

Required ancestors:

- Task 055 rollover implementation `6ad87e6f3ae65327a14bab4b5144dda4416d3645`;
- Task 056 accepted blocker report `884c84f269203338eeb144f7db715afe8eee8a51`;
- Task 057 implementation `f379e5c5d8dddb144cb0d1991b645b16055e1303`;
- Task 057 report `da3525c38c24f76e19c977e28446603b8c7c7063`;
- Task 057 review `0bfeefe9e889a4f336f8860efc9dcae0f73af7ad`.

Do not checkout, reset, clean, repair, or mutate the primary repository at `C:\Users\CDQ-P\.openclaw\workspace`.

## Accepted prior state

Task 056 established, without live mutation:

- controller PASSTHROUGH, generation 7;
- startup disabled and CogentNexus supervisor absent;
- healthy Gateway and Ollama with the same four model identities;
- exact ownership/controller/policy/SQLite/AGENTS/launcher preservation hashes;
- exactly one disabled canonical OpenClaw registration at the replacement generation root;
- two exact canonical v0.9.3 payload roots;
- ownership manifest still binding the prior generation root;
- live OpenClaw inventory shape with no `packageName` field.

These are expectations only. Task 058 must freshly re-prove the current state before planning. Any contradiction stops as BLOCKED without mutation.

## Evidence boundary

Before live inspection, create a new unique retained evidence directory under:

`%LOCALAPPDATA%\Temp\cnx058-rollover-plan-<UTC-token>`

Record at minimum:

- fetched repository HEAD and clean status;
- UTC command transcript and exit codes;
- redacted preflight/poststate JSON;
- fresh raw OpenClaw plugin inventory JSON;
- fresh machine-generated rollover plan JSON;
- independently computed plan SHA-256;
- bounded plan proofs/hashes required below;
- report draft and publication verification.

Do not overwrite or reuse the Task 056 evidence directory, its inventory capture, or its failed planning attempt. Retained Task 054/056 evidence may be read only for named preservation comparisons when needed; do not mutate it.

Do not record secrets, tokens, API keys, full OpenClaw configuration, environment dumps, or unrelated user data.

## Duplicate and concurrency fence

Before execution:

- fetch the coordination branch and require local/remote HEAD equality;
- verify all required ancestors;
- verify the fresh isolated clone is clean;
- verify `ACTIVE.md`, `STATUS.md`, this task, and `Current authorization: PHASE_A_PLAN_ONLY` agree;
- verify no matching Task 058 report already records a completed Phase A;
- prove zero concurrent installer, uninstall/reset, CogentNexus lifecycle, rollover apply, report publisher, Procmon capture, or another Task 058 executor.

Do not infer apply authority from a bare manual continuation signal.

## Phase A — authorized plan checkpoint only

### A1. Fresh read-only preservation preflight

Using exact-path/read-only commands, prove current state before inventory capture:

- controller mode exactly PASSTHROUGH and startup disabled;
- no CogentNexus-OpenClaw supervisor task/adapter active;
- Gateway healthy/reachable;
- Ollama healthy with the same four model identities;
- SQLite opens read-only with integrity `ok` and bounded ticket/event/outbox/session counts;
- ownership manifest, controller, registered policy, AGENTS baseline, launcher, and Task 049 manifest are present and freshly hashed;
- ownership manifest still binds the prior exact generation payload;
- current product plugin inventory still contains exactly two exact canonical v0.9.3 payload candidates and no unexpected product-owned third root;
- primary repository branch/status observed without mutation;
- unrelated plugin identities/count remain preserved.

Any preservation contradiction stops as `BLOCKED_LIVE_STATE_DRIFT` without planning or mutation.

### A2. Fresh supported OpenClaw inventory

Run exactly once for this task:

```powershell
openclaw plugins list --json
```

Save the raw JSON in the Task 058 retained evidence directory. Do not transform, edit, add `packageName`, or hand-author any inventory field.

Require exactly one canonical `cogentnexus-openclaw` record with:

- version `0.9.3`;
- nonempty `rootDir` within OpenClaw state;
- expected active replacement generation root;
- expected disabled/status state unless another accepted preflight fact explicitly proves otherwise.

`packageName` may be absent. If present, it must be the exact canonical package. Package identity for an absent field must be proven only by the fixed Task 057 planner from the exact bound payload.

### A3. Generate a new machine-produced plan

Run the accepted Task 057 implementation from the fresh isolated clone:

```powershell
python <isolated-clone>\skills\cogentnexus-openclaw\scripts\namespace_ownership.py rollover-plan `
  --root "C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw" `
  --workspace "C:\Users\CDQ-P\.openclaw\workspace" `
  --app-data "C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw" `
  --inventory-json <task058-fresh-inventory.json> `
  --plan <task058-rollover-plan.json>
```

Do not hand-author or edit the plan. Compute its SHA-256 independently and require exact equality with any planner-reported hash.

### A4. Verify every plan binding

The report must publish bounded values sufficient for ChatGPT review while retaining raw files locally. Verify at minimum:

- schema/operation/product/version exactness;
- workspace/state/OpenClaw/application-data boundaries;
- controller mode PASSTHROUGH;
- exact retired manifest-owned payload path and replacement active payload path;
- distinct old/new payload and npm project roots;
- exact expected v0.9.3 payload fingerprints and equality where required;
- active registration normalized package identity and `packageNameEvidence` (`inventory` or `payload-package-json`);
- exact retired/replacement managed-wrapper proofs and hashes;
- exact retired/replacement complete project-tree SHA-256 values;
- fresh raw plugin-inventory SHA-256;
- normalized active-registration SHA-256;
- manifest-before SHA-256;
- exact manifest-after replacement path;
- unique nonexistent backup destination under the external CogentNexus-OpenClaw rollover backup boundary;
- same-volume feasibility for the planned atomic `os.replace`;
- no unexpected extra product candidate or ambiguity.

If any check fails, do not repair manually and do not retry by weakening input. Stop as `BLOCKED_RECOVERY_PLAN_UNSAFE`.

### A5. Mandatory stop and publication

Task 058 must stop after a valid plan checkpoint. It must not invoke `rollover-apply` or any live mutation.

Publish:

`docs/operations/coordination/reports/CNX-20260824-058-fresh-rollover-plan-checkpoint.md`

For a valid plan, report:

Status: `AWAITING_HUMAN_GATE`

Result: `AWAITING_PLUGIN_GENERATION_ROLLOVER_APPLY`

The report must include:

- exact fresh plan path;
- exact plan SHA-256;
- fresh inventory SHA-256;
- every bounded plan binding above;
- fresh preflight/poststate preservation evidence;
- exact commands/exit codes;
- retained evidence directory path;
- live mutation count `0`;
- remaining uncertainty, if any.

The report commit must add only the matching Task 058 report path relative to the fetched execution HEAD. Fetch and remote-verify the report commit/path/blob, then stop.

## Future apply gate — explicitly not authorized

A later task may authorize `rollover-apply` only after:

1. ChatGPT accepts the exact Task 058 checkpoint report;
2. the operator explicitly approves the exact published Task 058 plan SHA-256;
3. a new coordination task records `PHASE_B_APPLY_AUTHORIZED`, the approved SHA-256, and the accepted Task 058 review commit.

Without all three, apply remains prohibited.

## Result tokens

Return exactly one:

- `AWAITING_PLUGIN_GENERATION_ROLLOVER_APPLY`
- `BLOCKED_LIVE_STATE_DRIFT`
- `BLOCKED_RECOVERY_PLAN_UNSAFE`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Hard fence

No `rollover-apply`, installer, generation move/delete, ownership rewrite, plugin enable/disable/install/uninstall, `cnxclaw enable/disable/start/stop/restart/reset/uninstall`, scheduler change, supervisor creation, Gateway/Ollama/model mutation, process termination, force-kill, primary-repository mutation, Procmon/Task 027/038 action, mutation of the separate HermesAgent project/system, Ecosystem, staged-capability-loop, merge, tag, release, or archive publication.

Report meaningful progress approximately every 3 minutes and immediately after duplicate/concurrency preflight, live-state preflight, inventory capture, plan generation, plan verification, publication, or blocker.
