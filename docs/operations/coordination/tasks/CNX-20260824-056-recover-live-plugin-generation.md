# CNX-20260824-056 — Recover Live Plugin Generation

Status: `READY_FOR_CODEX`

Execution mode: `MANUAL_WITH_HUMAN_GATE`

Current authorization: `PHASE_A_PLAN_ONLY`

Owner: ChatGPT

Executor: Codex after the operator's manual signal

## Goal

Recover the exact Task 054 live two-root CogentNexus-OpenClaw v0.9.3 state without rerunning the installer. First produce and publish a fully bound recovery plan. Only after ChatGPT reviews that exact plan and the operator separately authorizes its SHA-256 may a later Task 056 execution apply it and transactionally return the existing installation to MANAGED.

This publication authorizes Phase A only. Phase B is specified for auditability but remains prohibited until the durable authorization gate is satisfied.

## Required source

Use a fresh isolated full clone of:

`funggier/CogentNexus-OpenClaw`

Branch:

`agent/v0.9.3-recovery-reality-tests`

Required ancestors:

- implementation HEAD `6ad87e6f3ae65327a14bab4b5144dda4416d3645`;
- Task 055 report commit `846a58189dea4d8c5ccb137da4bf4c1952eeaaa5`;
- the Task 055 review and Task 056 coordination commits published after that report.

Do not checkout, reset, clean, repair, or otherwise mutate the primary repository at `C:\Users\CDQ-P\.openclaw\workspace`.

## Accepted starting state

Task 054 established a safe partial installation:

- controller PASSTHROUGH, generation 7;
- CogentNexus-OpenClaw startup disabled and supervisor adapter absent;
- one disabled native canonical registration resolving to the new generated root;
- two exact canonical v0.9.3 payload roots with fingerprint `0e5746d063af1bf6d82e0901ce4e5f3def57a9ecb41ec2d4bdd70ffcd6599ddb`;
- the ownership manifest still binds the prior root and had SHA-256 `D299F290D508C783AE33124FCC7E582349BF9C7A73C47D07DD38207EBF2F4207`;
- Gateway and Ollama healthy, four models preserved, SQLite/policy/user data unchanged, and 71 unrelated plugins preserved.

These are expectations to re-prove, not assumptions. Any contradiction stops Phase A as BLOCKED without mutation.

## Durable evidence boundary

Before machine inspection, create one unique retained directory under:

`%LOCALAPPDATA%\Temp\cnx056-recovery-<UTC-token>`

Record at minimum:

- fetched repository HEAD and clean status;
- command transcript with UTC timestamps and exit codes;
- redacted preflight/poststate JSON;
- raw OpenClaw plugin inventory JSON used for planning;
- recovery plan JSON and SHA-256;
- bounded hashes/inventory needed by this task;
- report draft and publication verification.

Do not record tokens, API keys, complete OpenClaw configuration, environment dumps, or unrelated file contents. Retain the evidence directory and isolated clone through Phase A review and any later Phase B execution.

## Duplicate and concurrency fence

Before every phase:

- fetch the coordination branch and verify local/remote HEAD equality;
- verify the required ancestors;
- verify the isolated clone is clean;
- verify `ACTIVE.md`, `STATUS.md`, this task, and the current authorization agree;
- inspect the matching report and reviews to determine whether Phase A is complete or Phase B is authorized;
- prove zero concurrent installer, uninstall/reset, CogentNexus lifecycle, rollover apply, report publisher, Procmon capture, or other Task 056 executor.

Do not repeat a completed phase. Do not infer Phase B authority from a bare `ต่อ` signal.

## Phase A — currently authorized: plan and checkpoint only

### A1. Read-only preservation preflight

Using exact-path/read-only commands, prove:

- controller mode is exactly PASSTHROUGH and startup remains disabled;
- no CogentNexus-OpenClaw supervisor task/adapter is active;
- Gateway and Ollama are healthy and the same four model identities remain;
- SQLite opens read-only with integrity `ok`, and ticket/event/outbox/session counts remain bounded as observed;
- registered policy, AGENTS stripped baseline, Task 049 backup manifest, launcher, and Task 054 ownership manifest are present and hashed;
- the primary repository branch/status is observed without mutation;
- unrelated plugin identities/count and excluded systems remain preserved.

Read-only access to the retained Task 054 evidence directory is allowed only to compare its named hashes/paths with current state. Do not alter or remove it.

### A2. Capture exact active inventory

Run the supported read-only OpenClaw command once to save valid plugin JSON:

```powershell
openclaw plugins list --json
```

The saved JSON must contain exactly one canonical `cogentnexus-openclaw` registration with package `openclaw-plugin-cogentnexus-openclaw`, version `0.9.3`, and a `rootDir` contained by the OpenClaw state boundary. Record only bounded structural fields in the report; keep the raw inventory in retained local evidence.

### A3. Generate the reviewed plan

Run the Task 055 implementation from the isolated clone:

```powershell
python <isolated-clone>\skills\cogentnexus-openclaw\scripts\namespace_ownership.py rollover-plan `
  --root "C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw" `
  --workspace "C:\Users\CDQ-P\.openclaw\workspace" `
  --app-data "C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw" `
  --inventory-json <retained-inventory.json> `
  --plan <retained-rollover-plan.json>
```

Do not hand-author or edit the plan. Compute SHA-256 independently and require it to equal the command result.

Verify and report every plan binding:

- state/workspace/OpenClaw/application-data boundaries;
- controller mode PASSTHROUGH;
- exact old manifest-owned payload and wrapper/project roots;
- exact active replacement payload and wrapper/project roots;
- distinct old/new roots and equal expected payload fingerprint;
- private wrapper/package/lock proofs and hashes;
- complete old/new project-tree SHA-256 values;
- complete plugin-inventory SHA-256 and active-registration SHA-256;
- manifest-before SHA-256 and exact manifest-after replacement path;
- unique nonexistent backup path inside the external product backup boundary;
- same-volume feasibility for the planned atomic move.

### A4. Mandatory stop and checkpoint publication

Phase A must not invoke `rollover-apply`, move/delete either project, update ownership, enable the plugin, enable startup, create the supervisor, or change controller mode.

Publish the matching report:

`docs/operations/coordination/reports/CNX-20260824-056-recover-live-plugin-generation.md`

For a valid plan, the report status is `AWAITING_HUMAN_GATE` and its exact result token is:

`AWAITING_PLUGIN_GENERATION_ROLLOVER_APPLY`

The report must include the plan path, plan SHA-256, every bounded field above, preflight/poststate preservation, exact command/exit evidence, live mutation count `0`, and remaining uncertainty. The report commit may add only the matching report path. Fetch and remote-verify the report commit/path/blob, then stop.

ChatGPT will review the checkpoint. The operator must then explicitly approve the exact plan SHA-256. ChatGPT must publish a later coordination commit containing `Current authorization: PHASE_B_APPLY_AUTHORIZED`, the approved plan SHA-256, and the accepted checkpoint report/review commit. Without all three, Phase B is prohibited.

## Phase B — specified but not yet authorized

Phase B may run only when a freshly fetched `ACTIVE.md` and `STATUS.md` both contain:

- `Current authorization: PHASE_B_APPLY_AUTHORIZED`;
- the exact approved plan SHA-256;
- the accepted Phase A checkpoint review commit;
- the operator's explicit authorization recorded by ChatGPT.

When authorized, Phase B must:

1. re-run the complete read-only preflight and prove no drift;
2. capture a fresh second `openclaw plugins list --json` inventory to a new evidence file;
3. invoke `rollover-apply` exactly once with the retained plan, approved SHA-256, and fresh inventory;
4. never retry apply or perform manual repair if it blocks;
5. verify the prior project moved exactly to the planned backup, the replacement remains, exactly one canonical payload resolves, the manifest binds it, and controller remains PASSTHROUGH;
6. invoke the installed canonical launcher exactly once as `cnxclaw.cmd enable --provider ollama` through the Task 055 exact exit-code wrapper;
7. if enable fails, do not retry; rely on its transactional rollback and report the observed state;
8. if enable succeeds, prove MANAGED authority, plugin enabled/loaded at the replacement root, startup/supervisor installed, Gateway/Ollama healthy, the same four models, SQLite/policy/AGENTS/user data preserved, unrelated plugins preserved, and the rollover backup exact;
9. update the existing Task 056 report with final evidence and publish a report-only commit.

Phase B must not run an installer, uninstall, reset, clean reinstall, plugin install/uninstall, broad cleanup, manual config/manifest/AGENTS/database edit, model mutation, primary-repository mutation, or excluded-system action.

## Result tokens

Phase A returns exactly one:

- `AWAITING_PLUGIN_GENERATION_ROLLOVER_APPLY`
- `BLOCKED_LIVE_STATE_DRIFT`
- `BLOCKED_RECOVERY_PLAN_UNSAFE`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

If later authorized, Phase B returns exactly one:

- `PASS_LIVE_GENERATION_ROLLOVER_RECOVERED_MANAGED`
- `BLOCKED_APPROVED_PLAN_OR_STATE_DRIFT`
- `BLOCKED_ROLLOVER_APPLY_FAILED_ROLLBACK_COMPLETE`
- `BLOCKED_ROLLOVER_APPLY_FAILED_ROLLBACK_INCOMPLETE`
- `BLOCKED_MANAGED_ENABLE_FAILED_SAFE_PASSTHROUGH`
- `BLOCKED_POSTRECOVERY_VERIFICATION`
- `BLOCKED_REPORT_PUBLICATION_UNSAFE`

## Hard fence

Current authorization permits read-only inspection, one inventory capture, plan generation into retained evidence, and report publication only.

No installer, `rollover-apply`, generation move/delete, ownership rewrite, plugin enable/disable/install/uninstall, `cnxclaw enable/disable/start/stop/restart/reset/uninstall`, scheduler change, supervisor creation, Gateway/Ollama/model mutation, process termination, force-kill, Procmon/Task 027/038 action, primary-repository mutation, HermesAgent, Ecosystem, staged-capability-loop, merge, tag, release, or archive publication is currently authorized.

Report meaningful progress approximately every 3 minutes and immediately after duplicate/concurrency preflight, live-state preflight, inventory capture, plan creation, plan verification, checkpoint publication, and any blocker.

