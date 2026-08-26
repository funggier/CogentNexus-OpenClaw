# CNX-20260826-070 — Restore Non-Fresh Installer Mode Isolation

Status: `READY_FOR_HERMES`

Execution mode: `SOURCE_REWORK_TDD_INSTALLER_MODE_ISOLATION`

Current authorization: `INSTALLER_MODE_ISOLATION_REWORK_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes after the operator's continuation signal

## Goal

Correct the single production regression introduced by Task 069: coherent upgrade and legacy install paths are currently aborted by the fresh-transaction sentinel before the installer body can execute.

Restore normal non-fresh execution while preserving the accepted Task 067-069 fixes for npm reproducibility, fresh transaction recovery, exact application-data authority, supported plugin inverse, and shared-parent deletion safety.

This task is source/tests only. Do not touch the current live Task-066 residue or any live OpenClaw/Ollama/CogentNexus state.

## Accepted predecessor evidence

Task 069 report result:

`PASS_FRESH_TRANSACTION_FAILURE_COVERAGE_CLOSED`

Implementation HEAD:

`7f48bb803fe3ca46b7a786e50abe8df22da857fc`

Report HEAD:

`fee1a44b5e2212e3b21f627c57e943eb3154878c`

Independent review:

Decision `REWORK`

Disposition:

`REWORK_NONFRESH_INSTALL_MODE_ABORT_REGRESSION`

Review commit:

`a9112161391a2696733f1c09d1721e8611ab843a`

Preserve accepted portions from Tasks 067-069:

- plugin `openclaw` devDependency exact `2026.7.1-2`;
- clean npm 11.16.0 and npm 12.0.2 reproducibility;
- fresh transaction begin after fresh classification and before residue-capable fresh mutation;
- one fresh pre-commit caught-failure recovery concept;
- exact application-data product-root authority and `applicationDataPreexisting` preservation;
- record-time rejection of unsafe transaction paths;
- exact-root rollback that does not delete shared parents;
- supported fresh plugin inverse when this attempt created registration;
- AGENTS policy application after ownership transaction commit;
- transaction commit only after ownership create + exact verify;
- malicious/tampered/unmarked residue remains fail-closed.

## Current live preservation boundary

The accepted live state remains unchanged from Task 066:

- no CogentNexus Supervisor task;
- no `cnxclaw.cmd` launcher;
- no registered CNX plugin;
- AGENTS managed block absent;
- native OpenClaw Gateway healthy;
- Ollama healthy;
- Task-066 partial unowned residue remains at the reported workspace `.cogentnexus-openclaw` and `skills\cogentnexus-openclaw` roots;
- no valid `ownership.json`.

Task 070 MUST NOT clean, install, uninstall, enable, disable, reset, reboot, terminate processes, or otherwise mutate that live state.

## Blocking defect — sentinel aborts every non-fresh install

Current Task 069 production code does this after fresh transaction setup:

```powershell
try {
    if (-not $isFreshTransaction) {
        throw "__UPGRADE_PASSTHROUGH__"
    }
    # normal installer body
}
catch {
    if (-not $isFreshTransaction -or $_.Exception.Message -eq "__UPGRADE_PASSTHROUGH__") {
        if ($_.Exception.Message -eq "__UPGRADE_PASSTHROUGH__") {
            throw "Non-fresh install cannot use the fresh transaction failure boundary."
        }
        throw
    }
    Invoke-FreshTransactionRollback ...
}
```

For `classification.mode == upgrade` or `legacy`, `$isFreshTransaction` is false. The installer therefore always throws before reaching its normal upgrade/migration body.

This breaks install-over/upgrade and legacy migration behavior.

## Required production behavior

### 1. Non-fresh execution remains reachable

For coherent `upgrade` and `legacy` classifications:

- do not start a fresh transaction;
- execute the normal existing installer body;
- preserve existing upgrade/native-handoff/migration semantics;
- do not invoke fresh transaction rollback;
- propagate ordinary failures using the normal non-fresh error path.

Do not use a synthetic sentinel that aborts non-fresh execution.

### 2. Fresh caught-failure rollback remains intact

For `classification.mode == fresh`:

- successful `transaction-begin` still occurs before residue-capable mutation;
- all caught failures before successful transaction commit still route through the single bounded fresh recovery path;
- supported plugin inverse remains exact and attempt-scoped;
- original error remains visible;
- rollback error is not hidden;
- no fresh rollback can run after a successful commit as if the marker were incomplete.

### 3. Preferred control shape

A minimal safe structure is acceptable:

```powershell
try {
    # shared installer body for fresh / upgrade / legacy
    # fresh-only transaction commit remains guarded by $isFreshTransaction
}
catch {
    if ($isFreshTransaction) {
        Invoke-FreshTransactionRollback -WorkspacePath $Workspace -OriginalError $_.Exception.Message
    }
    throw
}
```

Equivalent designs are allowed if tests prove the same mode isolation.

Do not duplicate the entire installer body into separate fresh/non-fresh copies unless unavoidable.

### 4. Preserve post-commit ordering

Keep:

- ownership create;
- exact ownership verify;
- fresh transaction commit;
- then managed AGENTS policy / lifecycle enable and other post-commit behavior.

No accepted post-commit external effect needs to be pulled back into the incomplete fresh transaction.

## Strict TDD requirements

Use a fresh isolated worktree from the current coordination HEAD. Verify remote/local HEAD, clean tree, task/review ancestry, and absence of Task 070 report before editing.

### M1 — non-fresh reachability RED/GREEN

Add an installer-facing regression test against actual `scripts/install.ps1` proving coherent non-fresh execution is reachable.

RED against Task 069 implementation must fail because the sentinel abort exists.

GREEN must prove:

- no unconditional synthetic throw exists for `$isFreshTransaction == $false`;
- upgrade mode reaches installer body statements after the boundary opening;
- legacy mode reaches installer/migration body statements after the boundary opening;
- no fresh transaction begin is invoked for those modes.

A pure string check for absence of `__UPGRADE_PASSTHROUGH__` is not sufficient by itself; pair it with an executable or extracted-boundary mode harness.

### M2 — non-fresh failure does not fresh-rollback

Use an isolated PowerShell harness around the same production boundary/control helper or a narrowly extracted executable production surface.

Inject a deterministic non-fresh failure.

Assert:

- original non-fresh failure propagates;
- `Invoke-FreshTransactionRollback` is NOT called;
- no `transaction-rollback` command runs;
- no fresh plugin inverse runs;
- sentinel fixture/state remains unchanged.

### M3 — fresh failure regression

Re-run/integrate the Task 069 fresh injected-failure harness.

Assert:

- fresh failure still invokes same-run bounded rollback;
- exact transaction-created residue is removed;
- original error remains visible;
- unrelated sentinel/shared parents survive;
- classification becomes coherent fresh.

### M4 — upgrade mode does not create fresh marker

Use a temp coherent ownership fixture or a faithful production-classification harness sufficient to drive the mode guard.

Assert no `install-transaction.json` is created/modified by the upgrade path before the injected stop point.

### M5 — legacy mode does not create fresh marker

Use an isolated legacy fixture with the minimum ownership proof required by `prove_legacy_ownership()` or an equivalent production mode harness.

Assert no fresh transaction marker is created and the migration/native-handoff path is reachable rather than synthetically aborted.

### M6 — syntax/control-flow check

Parse/load the full production PowerShell installer in a no-execution syntax check. Fail if braces/try/catch structure is malformed.

### M7 — accepted transaction regressions

Keep all Task 067-069 transaction tests green, especially:

- exact app-data root created vs preexisting behavior;
- record-time unsafe path rejection;
- committed-marker rollback refusal;
- crash/rerun recovery;
- shared parent preservation;
- malicious/tampered/unmarked marker failure;
- plugin inverse ordering;
- commit after ownership verify;
- AGENTS policy after commit.

## Full verification

Run fresh in isolated environments:

1. M1-M7 RED/GREEN evidence;
2. `tests/test_fresh_transaction_failure_coverage.py`;
3. `tests/test_installer_transaction_wiring.py`;
4. `tests/test_fresh_install_transaction_recovery.py`;
5. installer/runtime/ownership/startup focused tests;
6. full `pytest tests/ -q` with `requirements-dev.txt` installed;
7. clean npm 11.16.0 / node v24.18.0 `npm ci` + `plugin:validate` + `npm test`;
8. clean npm 12.0.2 / compatible node `npm ci` + `plugin:validate` + `npm test`;
9. exact OpenClaw devDependency remains `2026.7.1-2`, plugin version `0.9.3`;
10. `python scripts/check_baseline_consistency.py`;
11. `git diff --check`;
12. clean worktree after implementation commit.

Explain any skips. Do not claim PASS from structural inspection alone.

## Publication discipline

Use separate commits:

1. implementation/tests commit(s);
2. report-only commit adding only:

`docs/operations/coordination/reports/CNX-20260826-070-restore-nonfresh-installer-mode-isolation.md`

Report must include:

- fetched execution HEAD;
- implementation HEAD;
- M1-M7 RED/GREEN evidence;
- exact resulting production control-flow shape;
- upgrade/legacy reachability evidence;
- proof non-fresh failure never invokes fresh rollback;
- fresh rollback regression evidence;
- full test counts;
- npm 11/npm 12 regression results;
- explicit no-live-mutation accounting;
- report-only publication fence.

## Live hard fence

No cleanup of Task-066 residue; no install/install-over/uninstall/reset; no lifecycle command; no Scheduled Task mutation; no Gateway/Ollama/plugin/config/AGENTS/SQLite mutation; no process termination; no primary workspace mutation; no reboot; no HermesAgent mutation; no merge/tag/release.

## Result tokens

Use exactly one:

- `PASS_INSTALLER_MODE_ISOLATION_RESTORED`
- `BLOCKED_NONFRESH_REACHABILITY`
- `BLOCKED_FRESH_ROLLBACK_REGRESSION`
- `BLOCKED_TEST_OR_VALIDATION_FAILURE`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Pre-authorized successor

If ChatGPT independently accepts `PASS_INSTALLER_MODE_ISOLATION_RESTORED`, Task 071 may perform the one-time bounded cleanup of the exact Task-066 residue, fresh-install the accepted source, prove exact owned runtime/no-Hermes durable binding, observe at least three natural PT1M no-flash ticks, and complete final MANAGED/OpenClaw/Ollama/plugin/ownership/AGENTS/SQLite health acceptance without another confirmation.
