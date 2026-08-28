# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_TDD_REPAIR`
Current authorization: `CNX-20260828-117_INSTALLER_PROVIDER_BINDING_ORIGIN_REPAIR`
Task ID: `CNX-20260828-117`
Updated: 2026-08-28 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260828-117-installer-provider-binding-origin-repair.md`](tasks/CNX-20260828-117-installer-provider-binding-origin-repair.md)

Task 117 is a **source-only root-cause/TDD repair** that converts the installer to a provider-neutral boundary after the Task-116 PowerShell binding failure.

## Task 116 closure

Task-116 report:

`docs/operations/coordination/reports/CNX-20260828-116-v093-real-windows-lifecycle-acceptance-final-candidate.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-116-v093-real-windows-lifecycle-acceptance-final-candidate-review.md`

Review verdict:

`ACCEPTED FAIL — CLEAN PRE-BODY PARAMETER-BINDING FAILURE; SUCCESSOR DIAGNOSIS/REPAIR REQUIRED`

Task 116 Phase 0 passed and proved the live machine coherent. Its single install-over attempt failed before installer-body execution because the installer exposed a Provider parameter and PowerShell bound the unrelated value `3D Objects` to it. No reset/uninstall/reinstall/lifecycle/recovery or Dashboard semantic Send occurred.

## Task-117 architectural invariant

**Every subsystem defines only data that is genuinely required to perform or verify that subsystem's own responsibility.**

For installation, provider/model/endpoint/timeout/provider executable and provider policy are not installation-owned data. Therefore Task 117 intentionally retires the installer-level `-Provider` API rather than preserving it.

The repaired installer must be provider-neutral:

- no `Provider` parameter;
- no provider ValidateSet/default;
- no provider auto-detection/inference;
- no direct provider executable prerequisite merely because runtime uses it;
- no `--provider ...` lifecycle argument from installer;
- no provider-specific installation-success claims;
- canonical install command has no provider argument.

Provider awareness remains only in runtime/configuration layers where it is actually required. This does not declare LM Studio or any other provider supported by current runtime; it prevents provider policy from leaking into installation.

Task 117 must still inspect preserved Task-116 evidence and trace `3D Objects` as far as evidence allows, then use tests-only RED before production repair.

Required method:

`fresh reconcile -> read-only Task-116 evidence/root-cause trace -> TESTS-ONLY provider-neutral RED -> minimal boundary repair -> GREEN -> targeted/full validation -> exact same-SHA CI/package proof -> report -> independent review`

## Preserved live boundary

Task 116 is the latest authoritative live-machine evidence:

- CNX passthrough, generation 25;
- OpenClaw exactly `2026.7.1-2`;
- current runtime provider healthy;
- Gateway healthy;
- SQLite integrity `ok`;
- exact interrupted-reentry classification proven;
- post-failure state coherent;
- no lifecycle phase beyond the failed pre-body install-over binding executed.

Task 117 must not mutate that live state.

## Hard fence

Task 117 does **not** authorize:

- live install-over/reset/uninstall/reinstall/lifecycle/recovery;
- Task-116 destructive command replay;
- manual cleanup/normalization of live residue;
- OpenClaw/provider-runtime changes on the live machine;
- provider/model/endpoint/timeout changes;
- live SQLite/config/session/manifest/plugin mutation;
- credentials/secrets access;
- Dashboard semantic Send;
- reboot/process-tree kill;
- merge/tag/release/force push.

Read-only inspection of preserved Task-116 evidence and isolated non-mutating Windows diagnostic reproduction is authorized.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-117-installer-provider-binding-origin-repair.md`

Then stop for independent ChatGPT review. Do not create or execute a new real-Windows lifecycle retry task.
