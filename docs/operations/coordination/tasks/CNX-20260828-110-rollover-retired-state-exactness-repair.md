# CNX-20260828-110 — Rollover Retired-State Exactness Repair

- Status: `READY_FOR_HERMES`
- Execution mode: `SOURCE_ONLY_TDD`
- Owner: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-28 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Repair the residual fail-closed exactness defect found during independent review of Task 109.

This task is **source/test/CI only**. It does not authorize any real-Windows lifecycle mutation.

## Authoritative predecessor evidence

Task 109 report:

`docs/operations/coordination/reports/CNX-20260828-109-rollover-finalize-failclosed-repair.md`

Task 109 independent review:

`docs/operations/coordination/reviews/CNX-20260828-109-rollover-finalize-failclosed-repair-review.md`

Review verdict:

`REJECTED — TDD PROVENANCE FAILURE + RESIDUAL RETIRED-STATE EXACTNESS DEFECT`

Reviewed Task-109 source candidate:

`dcca49d43d95a0a34d8d460a4b9ab5ad88d036ce`

The commits after that candidate through the Task-109 report correction are coordination/report-only. Executor must still fetch current GitHub state and stop on unexplained production drift.

## What Task 109 successfully established

Preserve these behaviors:

- `rollover-prepare` validates and snapshots the old owned generation before external mutation;
- transaction data retains `retiredProjectTreeSha256`, `retiredFingerprint`, `backupProjectTreeSha256`, previous manifest, and manifest hash;
- install-over uses exactly one local package invocation:

```powershell
openclaw plugins install $packagePath --force
```

- post-install replacement fingerprint and transaction binding are verified;
- when the old retired project is completely absent and final ownership verification fails, the normal ownership manifest is removed instead of restoring a missing-path ownership claim;
- operation remains non-zero/fail-closed;
- backup/transaction evidence is retained;
- successful transaction behavior and all prior npm12/namespace/fresh-install protections remain intact.

Do not regress these behaviors.

## Confirmed residual defect

Current Task-109 finalization decides whether `manifestBefore` may be restored after final verification failure using only:

```python
retired_project = Path(transaction["retiredProjectRoot"])
if retired_project.exists():
    restore manifestBefore
else:
    quarantine/remove normal manifest
```

That is insufficient.

Before external mutation, `rollover-prepare` records the exact old project tree hash and payload fingerprint. After external mutation, a project path may still exist while its contents are changed, partially removed, replaced, or otherwise no longer equal to the exact pre-install retired generation.

In that state, restoring `manifestBefore` would reassert normal durable ownership without re-proving the state that manifest originally described.

The decision must therefore be based on **exact retired-state proof**, not path existence alone.

## Required invariant

After external OpenClaw mutation and a failed final ownership verification:

- the operation must remain non-zero;
- replacement ownership must not be declared successful;
- `manifestBefore` may be restored only when the retired generation is still provably the exact pre-mutation state bound by the transaction;
- an existing-but-altered, partial, foreign, or otherwise non-exact retired project must be treated as unavailable for normal ownership restoration;
- when exact old-state restoration cannot be proven, normal ownership must remain quarantined/fail-closed;
- transaction and external backup evidence must remain available for later authorized recovery;
- no external plugin install may be rerun as compensation;
- no unrelated OpenClaw/user-owned state may be deleted or modified;
- successful prepare/install/finalize behavior must remain unchanged.

Use the strongest already-recorded transaction evidence that is appropriate. Do not invent weaker identity checks when an exact tree/payload attestation is already available.

## Phase 0 — Reconcile repository state

Before editing:

1. fetch current remote branch HEAD;
2. confirm Task 110 is active in both `ACTIVE.md` and `STATUS.md`;
3. read Task-109 report and independent review;
4. compare current production source with `dcca49d43d95a0a34d8d460a4b9ab5ad88d036ce` and stop `BLOCKED` on unexplained production drift;
5. inspect `prepare_plugin_rollover_transaction`, `finalize_plugin_rollover_transaction`, project-tree hashing, plugin payload attestation, manifest verification, and all related rollback/transaction tests.

Do not rely on stale local state.

## Phase 1 — RED semantic regression

Strict TDD is mandatory.

Create a **test-only RED commit before changing production code**.

The RED commit SHA must be published to GitHub before Phase 2 begins.

The production-shaped regression must at minimum model:

1. valid old manifest-owned generation;
2. successful `rollover-prepare` with exact backup/transaction evidence;
3. external mutation boundary occurs;
4. the retired project path remains present, but the retired project is no longer exact — for example mutate/remove an owned payload file, change the wrapper/lock tree, or otherwise make its project-tree proof differ while preserving the directory path;
5. the expected replacement is present/registered;
6. finalization reaches the replacement manifest commit path;
7. inject final ownership verification failure after that replacement commit attempt;
8. demonstrate current source restores `manifestBefore` merely because the retired path still exists;
9. assert the desired invariant: a non-exact retired project must not regain a normal durable ownership manifest.

The test must fail because of the real semantic behavior, not syntax, string matching, or a fabricated exception unrelated to the boundary.

Commit only test/strictly necessary test fixture changes in RED.

Record:

- RED commit SHA;
- exact command;
- exact failing test/assertion;
- why failure proves the current production defect.

If the new test unexpectedly passes, stop and investigate; do not weaken it merely to manufacture RED.

## Phase 2 — Minimal production repair

Only after verified RED, implement the smallest safe fix.

Likely production surface:

- `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`.

A valid repair should base old-manifest restoration on exact transaction evidence, such as the pre-recorded project-tree hash and any necessary plugin payload identity, rather than `exists()` alone.

Required behavior:

- exact unchanged retired state may still use the prior manifest when rollback is genuinely valid;
- missing or non-exact retired state must not be restored as normal ownership;
- inability to prove exactness is treated as non-exact/fail-closed, not as permission to restore;
- quarantine/removal failure itself must remain an explicit non-zero error;
- do not automatically copy the backup back into OpenClaw state in this task;
- do not rerun `openclaw plugins install`;
- do not broaden into unrelated transaction redesign.

Commit the production fix separately from the RED commit.

## Phase 3 — GREEN targeted validation

Run the new exactness regression first and show it turns GREEN.

Then run at minimum:

- all Task-108/109 prepare/finalize transaction tests;
- all `tests/test_plugin_generation_rollover.py` tests;
- installer transaction wiring tests;
- namespace install/ownership contract tests;
- fresh transaction failure/rollback coverage;
- npm-12 local archive boundary tests.

Record exact commands and counts.

Confirm both important failure cases remain covered:

- retired project fully missing;
- retired project path present but no longer exact.

Also preserve the valid case where the exact old state genuinely still exists and a prior-manifest rollback remains safe.

## Phase 4 — Full repository validation

Run the normal full repository validation and plugin validation.

At minimum record:

- full pytest result;
- plugin validation result;
- `git diff --check`;
- any repository structural/PowerShell installer analysis normally required for changed transaction code.

No PASS from targeted tests alone.

## Phase 5 — Exact candidate CI/package proof

Push the GREEN production candidate and require all three workflows successful for the **same exact candidate commit**:

- `Validate`;
- `Windows Installer Pack Smoke`;
- `PS5.1 Acceptance Smoke`.

Record exact run IDs/conclusions.

Obtain a new package-proof artifact from that same exact candidate and record:

- artifact ID/name;
- outer artifact SHA256/digest;
- inner v0.9.3 ZIP SHA256;
- tar.gz SHA256;
- `PACKAGE_IDENTITY.json` source commit/version;
- payload file count/fingerprint;
- `PAYLOAD_IDENTITY.json` agreement;
- packaged installer still uses `openclaw plugins install $packagePath --force`;
- packaged ownership source contains the exact-state fail-closed repair;
- recovery harness identity/blob SHA.

Do not reuse Task-109 artifact `9681526010` as the next live candidate.

## Phase 6 — Report and stop

Publish exactly:

`docs/operations/coordination/reports/CNX-20260828-110-rollover-retired-state-exactness-repair.md`

The report must include:

- reconciliation result;
- RED commit SHA and exact RED evidence;
- root cause;
- minimal production fix commit/files;
- GREEN targeted/full results;
- exact candidate source;
- exact three workflow run IDs/results;
- new package-proof identity/hashes/fingerprint;
- residual uncertainty;
- final `PASS`, `FAIL`, or `BLOCKED`.

After publishing the report, stop for independent ChatGPT review. Do not create or execute a live-Windows acceptance task.

## Hard fence — NOT authorized

Task 110 does not authorize:

- real Windows install-over/reset/uninstall/fresh reinstall;
- lifecycle stop/start/restart acceptance;
- disruptive recovery harness execution;
- replay of Task 107/109;
- manual cleanup/normalization of live residue;
- Dashboard semantic nonce/message/Send;
- OpenClaw/Ollama update, reinstall, uninstall, or rebaseline;
- provider/model/timeout changes;
- credentials/tokens/password access or re-entry;
- live SQLite/config/session mutation;
- LM Studio management;
- process-tree kills;
- reboot;
- merge/tag/GitHub Release/force push;
- weakening namespace or ownership verification.

If exact safe restoration cannot be proven, retain fail-closed quarantine behavior and report `BLOCKED` rather than invent a permissive fallback.
