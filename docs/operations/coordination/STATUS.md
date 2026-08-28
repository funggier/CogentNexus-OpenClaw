# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `SOURCE_ONLY_TDD`  
**Updated:** 2026-08-28 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator authorized continued stabilization; Task 108 authorizes source/test/CI repair only  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260828-108-windows-plugin-rollover-transaction-repair.md`](tasks/CNX-20260828-108-windows-plugin-rollover-transaction-repair.md)

Task ID:

`CNX-20260828-108`

## Task 107 closure

Task 107 report was published at commit:

`582acb72dd09d1e3753452afcb5f76aa72929d5d`

Independent review was published at commit:

`b0487da1aacb5cd3663a6e7e6b2f3caed1db1ef0`

Review verdict:

`ACCEPTED FAIL — SOURCE DEFECT CONFIRMED`

Task 107 correctly stopped after its single failed install-over attempt. Its later destructive phases remain unexecuted and are not authorized for replay.

## What Task 107 proved

The Task 105 npm-12 / `npm-pack:` defect is repaired at the old failing boundary. The exact Task 107 candidate successfully used the local package install path:

```powershell
openclaw plugins install $packagePath --force
```

The new failure is a source-level transaction mismatch: OpenClaw `2026.7.1-2` can replace/remove the old plugin generation during the external install before the current ownership `rollover-plan` executes. The durable ownership manifest can therefore refer to an old root that no longer exists, and the planner correctly fails closed.

The fix must preserve that fail-closed invariant rather than weakening it.

## Authorized Task-108 sequence

Only source/test/CI work is authorized:

`reconcile remote -> RED production-shaped regression -> minimal transaction fix -> GREEN targeted tests -> full validation -> exact Actions/package proof -> report`

The expected semantic transaction shape is:

`pre-install old-state proof -> exactly one external local-.tgz install -> post-install exact replacement proof -> atomic ownership commit`

The implementation details must be derived through TDD.

## Source boundary

Last Task 107 candidate source:

`b14a711f24b3fd1cd0aaa51ce636c8502ba42404`

The branch history from that candidate through the Task 107 report and independent review changed coordination documents only. Executor must still fetch GitHub current state before editing and stop `BLOCKED` on unexplained production drift.

The Task 107 package-proof artifact `9677072214` is historical evidence only and must not become the next live acceptance artifact. Task 108 must produce a new exact package proof from its GREEN candidate.

## Hard fence

Task 108 does **not** authorize:

- any real Windows install-over/reset/uninstall/reinstall/lifecycle/recovery action;
- replaying Task 107;
- manual live cleanup/normalization;
- Dashboard semantic Send;
- OpenClaw/Ollama update, reinstall, or uninstall;
- model/provider/timeout changes;
- live SQLite/config/session mutation;
- credential/token/password access or re-entry;
- LM Studio management;
- process-tree kills;
- reboot;
- merge/tag/GitHub Release/force push;
- weakening ownership validation.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-108-windows-plugin-rollover-transaction-repair.md`

The report must include the RED test/commit and failure, minimal fix and files, GREEN tests, exact GREEN candidate source, exact workflow run IDs/results, and new package-proof artifact identity/hashes/fingerprint.

After report publication, stop for independent ChatGPT review. A new real-Windows lifecycle acceptance task is not authorized until that review accepts an exact candidate.
