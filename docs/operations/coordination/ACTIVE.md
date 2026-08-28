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

Task 117 is a **source-only root-cause/TDD repair** for the Windows installer Provider binding failure exposed by Task 116.

## Task 116 closure

Task-116 report:

`docs/operations/coordination/reports/CNX-20260828-116-v093-real-windows-lifecycle-acceptance-final-candidate.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-116-v093-real-windows-lifecycle-acceptance-final-candidate-review.md`

Review verdict:

`ACCEPTED FAIL — CLEAN PRE-BODY PARAMETER-BINDING FAILURE; SUCCESSOR DIAGNOSIS/REPAIR REQUIRED`

Task 116 Phase 0 passed and proved the live machine coherent. Its only mutation attempt failed during PowerShell parameter binding before the installer body executed because `Provider` received `3D Objects` instead of the allowed Ollama value. The executor stopped correctly; no reset/uninstall/reinstall/lifecycle/recovery or Dashboard semantic Send occurred.

## Key Task-117 diagnostic invariant

Frozen Task-116 `scripts/install.ps1` declares a `Provider` parameter defaulting to `ollama`, but `$Provider` is otherwise unused. v0.9.3 is Ollama-only.

However, the current public install documentation still supports:

```powershell
.\scripts\install.ps1 -Provider ollama
```

Therefore `Provider` is a dead behavioral input but a live compatibility surface. Task 117 must trace `3D Objects` to its exact caller/binding origin before production repair. A test that only passes `-Provider "3D Objects"` explicitly is not sufficient RED evidence.

Required method:

`fresh reconcile -> read-only preserved Task-116 invocation evidence -> trace exact bad-value data flow -> TESTS-ONLY semantic RED -> minimal root-cause repair -> GREEN -> targeted/full validation -> exact same-SHA CI/package proof -> report -> independent review`

Preserve explicit `-Provider ollama` compatibility unless root-cause evidence and tests justify an intentional contract change. Do not invent provider auto-detection, LM Studio fallback, or multi-provider resolution.

## Preserved live boundary

Task 116 is the latest authoritative live-machine evidence:

- CNX passthrough, generation 25;
- OpenClaw exactly `2026.7.1-2`;
- selected provider Ollama, healthy;
- Gateway healthy;
- SQLite integrity `ok`;
- exact interrupted-reentry classification proven;
- post-failure state coherent;
- no lifecycle phase beyond the failed pre-body install-over binding was executed.

Task 117 must not mutate that live state.

## Hard fence

Task 117 does **not** authorize:

- live install-over/reset/uninstall/reinstall/lifecycle/recovery;
- Task-116 destructive command replay;
- manual cleanup/normalization of live residue;
- OpenClaw/Ollama changes;
- provider/model changes;
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
