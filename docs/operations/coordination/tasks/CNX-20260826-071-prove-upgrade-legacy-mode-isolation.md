# CNX-20260826-071 — Prove Upgrade/Legacy Mode Isolation

Status: `READY_FOR_HERMES`

Execution mode: `SOURCE_TEST_VERIFICATION_MODE_SPECIFIC_NONFRESH_ISOLATION`

Current authorization: `MODE_SPECIFIC_NONFRESH_VERIFICATION_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes after the operator's continuation signal

## Goal

Close the remaining Task-070 evidence gap by proving with executable production-facing fixtures that both coherent `upgrade` and valid `legacy` classifications remain reachable, never create a fresh-install transaction marker, and never invoke fresh rollback semantics.

Prefer tests/evidence only. Do not change production `scripts/install.ps1` unless a new RED demonstrates an actual defect.

## Accepted predecessor candidate

Task 070 implementation HEAD:

`9df671670908241486afe2badf8a7f221410c6f8`

Task 070 report HEAD:

`573ca752e1c257a071d9a56b4206039c911b3b56`

Independent review:

Decision: `REWORK`

Disposition:

`REWORK_MODE_SPECIFIC_UPGRADE_LEGACY_EVIDENCE_MISSING`

Review commit:

`3b3cea20d02e66e34704bd3ee8d1ed79f1610b79`

## Accepted candidate behavior to preserve

Do not redesign these unless a failing executable proof requires it:

- Task-069 synthetic `__UPGRADE_PASSTHROUGH__` sentinel is absent;
- one shared installer body serves fresh / upgrade / legacy;
- fresh transaction begin remains guarded by `classification.mode == fresh`;
- catch invokes `Invoke-FreshTransactionRollback` only when `$isFreshTransaction` is true;
- fresh transaction commit remains after ownership create + exact verify;
- exact application-data authority, record-time path rejection, plugin inverse, shared-parent preservation, malicious/unmarked fail-closed behavior remain intact;
- OpenClaw devDependency remains exactly `2026.7.1-2` and npm 11/npm 12 reproducibility remains required.

## Current live preservation boundary

Do not touch the live machine product state in this task.

Accepted live baseline remains:

- no `CogentNexus-OpenClaw-Supervisor` task;
- no `cnxclaw.cmd` launcher;
- no registered CogentNexus plugin;
- AGENTS managed block absent;
- native OpenClaw Gateway healthy;
- Ollama healthy;
- Task-066 unowned partial residue remains only at the reported workspace `.cogentnexus-openclaw` and `skills\cogentnexus-openclaw` roots;
- no valid `ownership.json`.

## Strict method

Use a fresh isolated worktree from current coordination HEAD. Before editing:

1. verify fetched remote branch HEAD equals local execution HEAD;
2. verify clean worktree;
3. verify Task-070 review commit `3b3cea20d02e66e34704bd3ee8d1ed79f1610b79` is an ancestor;
4. verify ACTIVE/STATUS name Task 071;
5. verify no Task-071 report exists.

Use TDD for any new production correction. If the existing implementation passes the required new tests, do not manufacture a RED by altering working production code; the Task-070 review identified an evidence/test gap, so a test-only implementation commit is acceptable provided the tests genuinely execute the required production surfaces.

## U1 — coherent upgrade classification fixture

Build a temp workspace fixture that satisfies the production v0.9.3 ownership contract sufficiently for:

```python
classify_install(workspace, app_data=...)["mode"] == "upgrade"
```

Do not fake `mode = "upgrade"` by assigning a variable directly.

At minimum use the actual production `namespace_ownership.py` surfaces and exact expected paths/manifest fields. Where plugin verification would otherwise require a full OpenClaw fixture, use the narrowest production-supported fixture or monkeypatch boundary that still executes `classify_install()` and `verify_manifest()` semantics without duplicating the classifier in test code. Explain any controlled fixture substitution.

Prove:

- classification is exactly `upgrade`;
- no fresh transaction marker exists before classification;
- running the production fresh-mode guard/extracted installer boundary to an injected stop does not call `transaction-begin`;
- no `install-transaction.json` is created or modified.

## U2 — upgrade failure isolation

Using the same upgrade fixture/boundary, inject a deterministic failure after the shared installer body has been entered but before any live/external side effect in the fixture.

Prove:

- original failure propagates;
- fresh rollback helper is not invoked;
- `transaction-rollback` is not invoked;
- fresh plugin inverse is not invoked;
- no fresh marker appears;
- fixture sentinel state remains unchanged.

## L1 — valid legacy classification fixture

Construct an isolated legacy fixture satisfying the actual minimum `prove_legacy_ownership()` contract. Use production paths and real production classifier.

The fixture should provide at least three independent legacy ownership identities accepted by the current implementation, such as:

- legacy skill metadata;
- legacy controller structure/mode;
- legacy launcher content;
- legacy plugin identity if useful.

Prove:

```python
classify_install(workspace, app_data=...)["mode"] == "legacy"
```

and record the observed legacy evidence array/mode.

## L2 — legacy reachability and no fresh marker

Drive an executable production-facing boundary/harness using the actual legacy classification result, not a hand-assigned generic `$isFreshTransaction = $false` alone.

Prove:

- legacy classification reaches the shared installer/native-handoff/migration entry path past the Task-069 boundary opening;
- no `transaction-begin` is invoked;
- no `install-transaction.json` is created;
- the Task-069 sentinel abort text is absent;
- an injected legacy failure propagates through the ordinary non-fresh path;
- fresh rollback and fresh plugin inverse are not invoked.

The harness may stop before real migration mutation. This task is source/test-only and must not perform actual product migration on the live machine.

## F1 — fresh regression

Re-run the accepted Task-069 fresh injected-failure production harness and prove:

- same-run bounded rollback occurs;
- exact transaction-created workspace/app-data residue is removed;
- original error remains visible;
- unrelated/shared parents survive;
- classification returns coherent `fresh`.

## F2 — marker/authority regressions

Re-run focused suites covering:

- fresh transaction begin/record/commit/recovery;
- exact application-data created-vs-preexisting handling;
- record-time unsafe path rejection;
- committed-marker rollback refusal;
- crash/rerun recovery;
- shared-parent preservation;
- malicious/tampered/unmarked residue fail-closed;
- supported plugin inverse ordering;
- AGENTS policy after commit.

## Full verification

Run fresh in the isolated worktree:

1. U1/U2/L1/L2/F1/F2 focused tests;
2. `tests/test_installer_mode_isolation.py`;
3. `tests/test_fresh_transaction_failure_coverage.py`;
4. `tests/test_installer_transaction_wiring.py`;
5. `tests/test_fresh_install_transaction_recovery.py`;
6. full `pytest tests/ -q` in isolated dev venv with `requirements-dev.txt`;
7. PowerShell syntax parse of `scripts/install.ps1`;
8. clean npm 11.16.0 / node v24.18.0 `npm ci` + `plugin:validate` + `npm test`;
9. clean npm 12.0.2 / compatible node `npm ci` + `plugin:validate` + `npm test`;
10. exact plugin version `0.9.3` and OpenClaw devDependency `2026.7.1-2`;
11. `python scripts/check_baseline_consistency.py`;
12. `git diff --check`;
13. clean worktree after implementation/tests commit.

Explain all skips and fixture substitutions. Do not claim M4/M5 closure from structural inspection alone.

## Publication discipline

Use separate commits:

1. implementation/tests commit(s), preferably test-only if production code needs no correction;
2. report-only commit adding only:

`docs/operations/coordination/reports/CNX-20260826-071-prove-upgrade-legacy-mode-isolation.md`

Report must include:

- fetched execution HEAD;
- implementation/tests HEAD;
- exact upgrade fixture and observed `classify_install()` result;
- exact legacy fixture and observed ownership evidence/result;
- proof neither mode creates a fresh transaction marker;
- injected non-fresh failure isolation evidence for each mode;
- fresh rollback regression evidence;
- full test counts/npm gates;
- no-live-mutation accounting;
- report-only publication fence.

## Live hard fence

No cleanup of Task-066 residue; no live install/install-over/uninstall/reset; no lifecycle command; no Scheduled Task mutation; no Gateway/Ollama/plugin/config/AGENTS/SQLite mutation; no process termination; no primary workspace mutation; no reboot; no HermesAgent mutation; no merge/tag/release.

## Result tokens

Use exactly one:

- `PASS_UPGRADE_LEGACY_MODE_ISOLATION_PROVEN`
- `BLOCKED_UPGRADE_FIXTURE_OR_REACHABILITY`
- `BLOCKED_LEGACY_FIXTURE_OR_REACHABILITY`
- `BLOCKED_NONFRESH_ROLLBACK_ISOLATION`
- `BLOCKED_FRESH_REGRESSION`
- `BLOCKED_TEST_OR_VALIDATION_FAILURE`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Pre-authorized successor

If Task 071 is independently accepted, Task 072 may perform the one-time bounded cleanup of the exact Task-066 residue, fresh-install the accepted source, prove exact owned runtime/no-Hermes durable binding, observe at least three natural PT1M no-flash ticks, and complete final MANAGED/OpenClaw/Ollama/plugin/ownership/AGENTS/SQLite health acceptance without another confirmation.
