# CNX-20260828-109 — Rollover Finalize Fail-Closed Repair

- Status: `READY_FOR_HERMES`
- Execution mode: `SOURCE_ONLY_TDD`
- Owner: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-28 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Repair the residual post-mutation failure-path defect found by independent review of Task 108.

This task is **source/test/CI only**. It does not authorize any real-Windows lifecycle mutation.

## Authoritative predecessor evidence

Task 108 report:

`docs/operations/coordination/reports/CNX-20260828-108-windows-plugin-rollover-transaction-repair.md`

Task 108 independent review:

`docs/operations/coordination/reviews/CNX-20260828-108-windows-plugin-rollover-transaction-repair-review.md`

Review commit:

`bd303899b9b8ca9f011923e9d4563926b4ccad8c`

Review verdict:

`REJECTED — RESIDUAL FAILURE-PATH SOURCE DEFECT`

Reviewed production fix:

`f034cebe5cbe94116c10a81b89c2ef30de6646a8`

Reviewed report-only CI descendant:

`dc5e7a87867d03501b80b662e11aeaab833e0280`

The comparison from `f034cebe...` to `dc5e7a87...` changes only the Task-108 report; production and tests are identical.

## What Task 108 successfully established

Preserve these repairs:

- `rollover-prepare` validates the old durable ownership state before external mutation;
- the old managed npm project is snapshotted into the external backup boundary;
- install-over still executes exactly one local package command:

```powershell
openclaw plugins install $packagePath --force
```

- `rollover-finalize` validates the expected replacement fingerprint and transaction/manifest binding after the external install;
- the old npm-12 / `npm-pack:` invocation remains prohibited;
- fresh install and namespace ownership protections remain intact.

Task-108 local validation was GREEN (`70 passed` targeted; `422 passed, 3 skipped, 4 subtests passed` full), and the later report-only descendant had all three required workflows successful. Do not treat that as acceptance of the residual failure path.

## Confirmed residual defect

Task 108 explicitly required:

> A failure after the external command has mutated OpenClaw must remain fail-closed; do not falsely reassert a manifest for a generation that no longer exists.

Current `finalize_plugin_rollover_transaction` writes the replacement manifest and then performs final verification. If that verification raises, its exception handler writes `transaction["manifestBefore"]` back to the durable manifest path.

After `openclaw plugins install ... --force`, Task 107 proved the old `retiredPluginPath` may already have been removed. Restoring `manifestBefore` can therefore actively reassert ownership of a missing generation.

The pre-install backup does not make the original retired path live again.

This is the Task-109 defect. Do not broaden the task unnecessarily.

## Required invariant

After the external install has mutated OpenClaw:

- any post-install/finalization failure must return non-zero and remain fail-closed;
- code must not newly write or restore a normal durable ownership manifest that claims a missing retired generation;
- a replacement generation must not be declared successfully owned unless the final ownership proof succeeds;
- failure evidence sufficient for later authorized recovery/repair must remain durable;
- no unrelated OpenClaw state or user-owned state may be modified as compensating rollback;
- do not rerun the external plugin install to recover;
- successful prepare -> install -> finalize behavior must remain unchanged;
- all prior npm12/local-archive, namespace isolation, fresh-install and transaction protections must remain GREEN.

The exact failure-state representation is an implementation detail to derive through TDD. Acceptable designs may use an explicit indeterminate/pending transaction state, a safely validated commit-before-publish sequence, or another mechanism that proves the invariant. Do not suppress verification and do not turn a failed verification into success.

## Phase 0 — Reconcile current repository state

Before editing:

1. fetch the current remote branch HEAD;
2. confirm Task 109 is active in both `ACTIVE.md` and `STATUS.md`;
3. read the Task-108 report and independent review;
4. inspect `finalize_plugin_rollover_transaction`, the installer transaction wiring, existing transaction/rollback tests, and ownership verification consumers;
5. compare production source against `dc5e7a87867d03501b80b662e11aeaab833e0280` and stop `BLOCKED` on unexplained production drift.

Do not rely on stale local SHA/status.

## Phase 1 — RED production-shaped regression

Add a regression that reproduces the exact missing path before changing production behavior.

At minimum model:

1. valid old manifest-owned generation;
2. successful transaction prepare and external backup proof;
3. external install boundary removes/replaces the old generation and registers the expected replacement;
4. finalization reaches the replacement durable-commit path;
5. inject a failure at the final ownership verification/read-back boundary after the replacement commit attempt;
6. prove the current implementation raises but restores/reasserts `manifestBefore` even though `retiredPluginPath` no longer exists;
7. state the desired invariant: after the repair, that stale old ownership claim must not be durably reasserted.

The RED test must fail because of the real behavior, not syntax/string matching. Structural assertions may support but not replace the semantic regression.

Commit RED tests separately. Production files must not be changed in the RED commit except a strictly necessary test fixture/helper.

## Phase 2 — Minimal production fix

Implement the smallest safe failure-state/commit protocol that makes the RED regression GREEN while preserving Task-108 success semantics.

Likely production surface:

- `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`;
- `scripts/install.ps1` only if needed to persist/consume an explicit failure transaction state;
- directly related ownership verification/transaction code only when proven necessary by the regression.

Do not redesign unrelated lifecycle behavior.

Do not solve by:

- restoring `manifestBefore` to a missing old path;
- blindly accepting the replacement after verification failed;
- disabling final verification;
- rerunning `openclaw plugins install`;
- deleting unrelated OpenClaw/plugin projects;
- weakening namespace ownership validation.

## Phase 3 — GREEN targeted validation

Run at minimum:

- the new finalization-failure regression;
- all Task-108 prepare/finalize transaction tests;
- all `tests/test_plugin_generation_rollover.py` tests;
- installer transaction wiring tests;
- namespace install/ownership contract tests;
- fresh transaction failure/rollback coverage;
- npm-12 local archive boundary tests.

Record exact commands and counts.

## Phase 4 — Full repository validation

Run the repository full pytest/validation entry point and plugin validation. Record exact counts/results.

No PASS from targeted tests alone.

## Phase 5 — Exact same-candidate CI/package proof

Push the GREEN candidate and require all three workflows successful for the exact same source commit:

- `Validate`
- `Windows Installer Pack Smoke`
- `PS5.1 Acceptance Smoke`

Record exact run IDs.

Obtain a **new** package-proof artifact from that exact candidate and record:

- artifact ID/name;
- outer SHA256/digest;
- inner v0.9.3 ZIP SHA256;
- tar.gz SHA256;
- `PACKAGE_IDENTITY.json` source commit/version;
- payload file count/fingerprint;
- packaged installer still contains the local `.tgz` invocation and prepare/finalize contract;
- packaged recovery harness Git/source identity.

Task-108 artifact `9680707129` is historical evidence only and must not be used for the next live acceptance.

## Phase 6 — Report and stop

Publish exactly:

`docs/operations/coordination/reports/CNX-20260828-109-rollover-finalize-failclosed-repair.md`

Report:

- RED commit/test and exact failure;
- root cause;
- minimal fix and failure-state semantics;
- GREEN targeted/full results;
- exact candidate source;
- exact three workflow run IDs/results;
- new package-proof identity/hashes/fingerprint;
- residual uncertainty;
- final `PASS`, `FAIL`, or `BLOCKED`.

After report publication, stop for independent ChatGPT review. Hermes/Codex must not create or execute the next real-Windows acceptance task itself.

## Hard fence — NOT authorized

Task 109 does not authorize:

- real Windows install-over/reset/uninstall/fresh reinstall;
- lifecycle stop/start/restart acceptance;
- disruptive recovery harness execution;
- replay of Task 107;
- manual cleanup/normalization of live residue;
- Dashboard semantic nonce/message/Send;
- OpenClaw/Ollama update/reinstall/uninstall;
- provider/model/timeout changes;
- live SQLite/config/session mutation;
- credentials/tokens/password access or re-entry;
- LM Studio management;
- process-tree kills or reboot;
- merge/tag/GitHub Release/force push.

If a safe failure-state design cannot be proven, publish `BLOCKED` rather than weaken these constraints.
