# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_ONLY_TDD`
Current authorization: `CNX-20260828-108_WINDOWS_PLUGIN_ROLLOVER_TRANSACTION_REPAIR`
Task ID: `CNX-20260828-108`
Updated: 2026-08-28 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260828-108-windows-plugin-rollover-transaction-repair.md`](tasks/CNX-20260828-108-windows-plugin-rollover-transaction-repair.md)

Task 108 is a **source-only TDD repair** for the Windows plugin ownership rollover transaction defect exposed by Task 107.

## Predecessor decision

Task 107 report:

`docs/operations/coordination/reports/CNX-20260828-107-v093-real-windows-lifecycle-acceptance-retry.md`

Report commit:

`582acb72dd09d1e3753452afcb5f76aa72929d5d`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-107-v093-real-windows-lifecycle-acceptance-retry-review.md`

Review commit:

`b0487da1aacb5cd3663a6e7e6b2f3caed1db1ef0`

Review verdict:

`ACCEPTED FAIL — SOURCE DEFECT CONFIRMED`

Task 107 is closed. It must not be replayed.

## Confirmed repair target

The old npm 12 / `npm-pack:` failure is not the Task 108 defect. Task 107 proved the repaired local archive command reached the real OpenClaw boundary:

```powershell
openclaw plugins install $packagePath --force
```

The active defect is the ownership rollover transaction contract around that external mutation. OpenClaw `2026.7.1-2` can remove/replace the old plugin generation during `plugins install --force` before the current post-install `rollover-plan` can validate the old manifest-owned root.

The ownership fail-closed result is correct. Task 108 must bridge the mutation boundary without weakening ownership validation.

## Required execution method

Strict TDD:

`RED regression -> minimal production fix -> GREEN targeted -> full validation -> exact CI/package proof -> report`

The RED regression must model the production semantic boundary where the external install removes/replaces the old generation. A string-order-only test is insufficient.

The repair must preserve the equivalent transaction semantics of:

`pre-install old-state proof -> one external local-.tgz install -> post-install exact replacement proof -> atomic durable ownership commit`

Failure after external mutation remains fail-closed.

## Repository source boundary

The last accepted Task 107 candidate source is:

`b14a711f24b3fd1cd0aaa51ce636c8502ba42404`

The commits from that source through the Task 107 report/review boundary changed coordination documents only. Task 108 must recheck GitHub current state before editing and stop on unexplained production drift.

## Hard fence

Task 108 does **not** authorize:

- any real-Windows lifecycle mutation;
- install-over/reset/uninstall/reinstall/stop/start/restart/recovery replay;
- manual cleanup/normalization of live residue;
- Dashboard semantic nonce/message/Send;
- OpenClaw or Ollama update/reinstall/uninstall;
- live SQLite/config/session mutation;
- credentials or secrets access/re-entry;
- LM Studio management;
- process-tree kills or reboot;
- merge/tag/GitHub Release/force push;
- weakening ownership verification.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-108-windows-plugin-rollover-transaction-repair.md`

The report must contain RED evidence, minimal fix, GREEN validation, exact source commit, exact Actions run IDs, and the new package-proof identity/hashes. After publishing it, stop for independent ChatGPT review. Do not create a new live acceptance task.
