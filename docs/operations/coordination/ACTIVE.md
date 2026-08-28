# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_ONLY_TDD`
Current authorization: `CNX-20260828-109_ROLLOVER_FINALIZE_FAILCLOSED_REPAIR`
Task ID: `CNX-20260828-109`
Updated: 2026-08-28 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260828-109-rollover-finalize-failclosed-repair.md`](tasks/CNX-20260828-109-rollover-finalize-failclosed-repair.md)

Task 109 is a **source-only TDD repair** for the residual post-mutation ownership-finalization failure path found during independent Task-108 review.

## Task 108 closure

Task 108 report:

`docs/operations/coordination/reports/CNX-20260828-108-windows-plugin-rollover-transaction-repair.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-108-windows-plugin-rollover-transaction-repair-review.md`

Review commit:

`bd303899b9b8ca9f011923e9d4563926b4ccad8c`

Review verdict:

`REJECTED — RESIDUAL FAILURE-PATH SOURCE DEFECT`

Task 108 is closed. Its candidate/artifact are evidence only and are not authorized for live acceptance.

## Confirmed residual defect

The Task-108 prepare/finalize architecture correctly bridges the normal external mutation boundary, but `finalize_plugin_rollover_transaction` currently restores `manifestBefore` when final replacement-manifest verification raises.

Task 107 proved that the preceding external command can already have removed the old generation:

```powershell
openclaw plugins install $packagePath --force
```

Therefore the exception path can actively reassert durable ownership of a missing retired generation. That violates the required fail-closed invariant.

## Required execution method

Strict TDD:

`reconcile -> RED post-commit verification failure regression -> minimal failure-state fix -> GREEN targeted -> full validation -> exact same-source CI/package proof -> report`

The RED regression must model:

`valid old ownership -> prepare -> external old-generation removal/replacement -> replacement commit attempt -> injected final verification failure`

The repaired behavior must fail non-zero without restoring a normal manifest that claims the missing retired generation. It must not declare the replacement successfully owned unless final proof succeeds.

## Source boundary

Reviewed production/test candidate:

`dc5e7a87867d03501b80b662e11aeaab833e0280`

Task-108 production fix commit:

`f034cebe5cbe94116c10a81b89c2ef30de6646a8`

`f034cebe... -> dc5e7a87...` differs only by the Task-108 report. The coordination review/task commits after `dc5e7a87...` are documentation-only. Hermes/Codex must still fetch current GitHub state and stop `BLOCKED` on unexplained production drift.

## Historical CI/package evidence

The report-only descendant `dc5e7a87...` later passed all three required workflows and produced artifact `9680707129`, proving the Task-108 code is reproducible. That artifact is **not** the next live candidate because independent source review rejected the residual failure path.

Task 109 must produce a new exact package proof after the failure-path repair.

## Hard fence

Task 109 does **not** authorize:

- any real-Windows lifecycle mutation;
- install-over/reset/uninstall/reinstall/stop/start/restart/recovery replay;
- replay of Task 107;
- manual cleanup/normalization of live residue;
- Dashboard semantic nonce/message/Send;
- OpenClaw or Ollama update/reinstall/uninstall;
- provider/model/timeout changes;
- live SQLite/config/session mutation;
- credentials/secrets access or re-entry;
- LM Studio management;
- process-tree kills or reboot;
- merge/tag/GitHub Release/force push;
- weakening ownership verification.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-109-rollover-finalize-failclosed-repair.md`

The report must contain RED evidence, minimal fix, failure-state semantics, GREEN validation, exact source commit, exact Actions run IDs, and the new package-proof identity/hashes. After publishing it, stop for independent ChatGPT review. Do not create the next live acceptance task.
