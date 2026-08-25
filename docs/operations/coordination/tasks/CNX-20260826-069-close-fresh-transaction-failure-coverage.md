# CNX-20260826-069 — Close Fresh Transaction Failure Coverage

Status: `READY_FOR_HERMES`

Execution mode: `SOURCE_REWORK_TDD_FRESH_TRANSACTION_FAILURE_COVERAGE`

Current authorization: `FRESH_TRANSACTION_FAILURE_COVERAGE_REWORK_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes after the operator's continuation signal

## Goal

Close the remaining production fresh-install transaction gaps found in Task 068 so any caught pre-ownership failure cannot recreate an unsupported partial-install dead end, and the exact `%LOCALAPPDATA%\CogentNexus-OpenClaw` product root participates safely in rollback/recovery.

This is source/tests only. Do not mutate the current live Task-066 residue or any live OpenClaw/Ollama/CogentNexus state.

## Accepted predecessor evidence

Task 068 report result:

`PASS_PRODUCTION_INSTALLER_TRANSACTION_WIRED`

Implementation HEAD:

`2a0ca9fd9abda07765e3da222f7fc4d7730d3d30`

Report HEAD:

`3fc596a394fa2167d6c50e1672294c355120e809`

Independent review:

Decision `REWORK`

Disposition:

`REWORK_CAUGHT_FAILURE_AND_APPLICATION_DATA_TRANSACTION_GAPS`

Review commit:

`ad914838420028b4170cab9fc1e6d466dc7d444f`

Preserve accepted work from Tasks 067-068:

- OpenClaw plugin devDependency exactly `2026.7.1-2`;
- npm 11.16.0 and npm 12.0.2 clean-install reproducibility;
- fresh-only transaction begin after classification and before first fresh workspace mutation;
- transaction commit after ownership create + exact verify;
- exact-root rollback does not remove shared parents such as `<workspace>\skills`;
- malicious/unmarked residue remains fail-closed.

## Current live preservation boundary

The accepted live state remains:

- no CogentNexus Supervisor task;
- no `cnxclaw.cmd` launcher;
- no registered CNX plugin;
- native OpenClaw Gateway healthy;
- Ollama healthy;
- Task-066 partial unowned residue remains only at the reported `.cogentnexus-openclaw` and `skills\cogentnexus-openclaw` workspace roots;
- no valid `ownership.json`;
- AGENTS managed block absent.

Task 069 must not clean, install, uninstall, enable, disable, reset, reboot, or otherwise mutate this live state.

## Blocking defect B1 — caught fresh failures before ownership are not rolled back

Current production `scripts/install.ps1` starts a fresh transaction, but `Invoke-FreshTransactionRollback` is called only when:

- ownership manifest creation fails;
- ownership verification fails.

Earlier caught failures throw directly. This includes failures after residue-capable mutation in:

- skill validation;
- host initialization;
- policy integration;
- `npm ci`;
- plugin validation/packing/installation/disable;
- runtime provisioning;
- plugin resolution;
- other pre-commit fresh steps.

Task 068 P3 checked only that the helper exists; it did not inject a production-path failure and prove cleanup.

### Required B1 outcome

Establish one production fresh-transaction failure boundary covering all operations after successful `transaction-begin` and before successful `transaction-commit`.

A caught exception/nonzero failure in this region must:

1. retain the original failure;
2. perform all safe bounded recovery required for effects created by this fresh attempt;
3. report both original and rollback/recovery failures if rollback is incomplete;
4. never silently continue;
5. never rollback an upgrade/legacy install as if it were fresh.

A hard process crash remains handled by durable marker + rerun recovery.

Do not merely add more isolated `if ($LASTEXITCODE)` rollback calls. Prefer one structured production boundary/helper so new pre-commit steps cannot silently fall outside recovery.

## Blocking defect B2 — application-data path is recorded but rejected by validation

Fresh production install records the exact product application-data root when it did not exist before the attempt:

`%LOCALAPPDATA%\CogentNexus-OpenClaw`

But marker validation currently allowlists only workspace state/skill/launchers. A legitimate marker containing application data can therefore be rejected during rollback/recovery.

### Required B2 outcome

Make the exact product application-data root a first-class transaction-owned deletion boundary only when the fresh attempt proved it did not preexist and recorded it.

Safety requirements:

- allow only the exact canonical product root, not arbitrary siblings under `%LOCALAPPDATA%`;
- never delete `%LOCALAPPDATA%` itself or any parent;
- descendants are permitted only as containment within the exact product root;
- application-data path/provenance used by begin, record, rollback, recovery, and CLI must be consistent;
- custom isolated `--app-data` roots used by tests must validate consistently rather than being compared against an unrelated environment-derived path;
- if application data preexisted before the fresh attempt, do not record/delete the preexisting root.

Validate a recorded path before adding it to `createdPaths`; do not permit a marker to be poisoned with a path that will only fail later during deletion.

## Pre-commit external effects

A fresh install may create OpenClaw/plugin effects before ownership commit. Filesystem rollback alone is not sufficient if these effects would make a rerun classify as partial/new.

For each product-owned external effect that can occur before commit, choose and prove one of:

1. safely reorder it to after ownership commit; or
2. add a supported, bounded inverse that applies only because fresh preflight proved the effect did not preexist.

At minimum inspect:

- `openclaw plugins install ...` registration/npm managed generation;
- plugin entry/load-path mutation caused by the fresh installer;
- managed AGENTS policy application;
- ticket DB/state created under owned filesystem roots;
- runtime/application-data provisioning.

Do not use broad OpenClaw config deletion or manually delete arbitrary npm project directories. Any inverse must use supported OpenClaw/product surfaces or exact transaction-owned filesystem boundaries.

Prefer moving AGENTS managed policy application to the post-ownership side if lifecycle semantics permit, so failed pre-commit installation cannot leave a managed block.

## Strict TDD requirements

Use a fresh isolated worktree from current coordination HEAD. Verify HEAD/tree/Task 069 coordination before editing. No live mutation.

### F1 — production early caught-failure RED/GREEN

Create a production installer-facing harness/test that injects a deterministic failure after state/skill creation but well before ownership create (for example validation/host-init/npm boundary) using the actual fresh transaction control boundary.

RED against Task 068 implementation must prove:

- installer failure occurs;
- caught rollback is not reached / exact fresh residue remains.

GREEN must prove:

- rollback/recovery is invoked automatically in the same caught execution;
- exact fresh filesystem residue is removed;
- original injected error remains in output/error;
- unrelated workspace sentinel survives;
- result classifies coherent `fresh` afterward.

A test that calls rollback helper directly is insufficient.

### F2 — failure after plugin registration but before ownership commit

In a fully isolated/safe OpenClaw fixture or a faithful supported-command harness, inject failure after the fresh plugin registration step but before ownership commit.

Prove the caught recovery path leaves no CNX plugin registration/config/generation that causes later fresh classification or violates preflight. Use supported inverse semantics; do not simulate success by deleting arbitrary project directories.

If a real isolated OpenClaw fixture is not feasible, refactor the product installer external-effect operations behind an executable helper with command-injection/mocks that prove exact supported inverse commands and ordering, then run at least one integration-level supported command test where possible.

### F3 — application-data exact-root rollback

Use an isolated temp application-data parent with:

- sibling sentinel directory/file;
- exact `CogentNexus-OpenClaw` product root created only after transaction begin;
- marker recording exact product root.

Run production rollback and recovery variants.

Assert:

- exact product root is removed when transaction-created;
- sibling sentinel survives;
- application-data parent survives;
- workspace shared parents survive;
- classification returns fresh.

RED against Task 068 should expose marker boundary rejection.

### F4 — preexisting application-data preservation

Create exact product application-data root before transaction begin with a sentinel.

Installer/transaction path must not record the preexisting root for deletion. Inject a caught failure and prove root/sentinel remains.

### F5 — record-time rejection

Attempt to `transaction-record`:

- workspace parent;
- sibling skill;
- arbitrary temp/user path;
- application-data sibling;
- `%LOCALAPPDATA%` parent itself.

The record operation must reject immediately and leave marker `createdPaths` unchanged.

### F6 — commit boundary regression

Keep proof that `transaction-commit` remains strictly after ownership create + verify and no fresh rollback can run after commit as if marker were incomplete.

### F7 — crash/rerun recovery regression

Simulate hard crash after recorded workspace and application-data artifacts but before commit. Rerun production `recovery-preflight`; prove exact owned residue and product app-data root recover, shared parents/siblings survive, then `classify-install` returns fresh.

### F8 — no external-effect residue regression

After each injected caught failure at representative pre-commit phases, assert the temp fixture has no product external effect that would make a supported rerun fail closed unexpectedly.

## D1/P5 regression gates

Preserve and rerun:

- npm 11.16.0 / node v24.18.0 clean `npm ci`;
- npm 12.0.2 / compatible node clean `npm ci`;
- `npm run plugin:validate` under both;
- `npm test` under both;
- exact OpenClaw `2026.7.1-2`, plugin v0.9.3;
- shared `<workspace>\skills` parent preservation;
- malicious/tampered/unmarked marker tests.

## Full verification

Run fresh in isolated environments:

1. F1-F8 focused RED/GREEN evidence;
2. Task 067/068 transaction/recovery suites;
3. installer/runtime/ownership/startup focused tests;
4. full `pytest tests/ -q` with `requirements-dev.txt` installed;
5. both npm toolchain gates;
6. canonical plugin build/validate/test/pack;
7. `python scripts/check_baseline_consistency.py`;
8. `git diff --check`;
9. clean worktree after implementation commit.

Record exact counts and explain skips.

## Publication discipline

Use separate commits:

1. implementation/tests commit(s);
2. report-only commit adding only:

`docs/operations/coordination/reports/CNX-20260826-069-close-fresh-transaction-failure-coverage.md`

Report must include fetched execution HEAD, implementation HEAD, exact production fresh failure boundary, application-data authority contract, external-effect rollback/reordering evidence, F1-F8 results, full test counts, npm 11/12 evidence, and no-live-mutation accounting.

## Live hard fence

No cleanup of Task-066 live residue; no install/install-over/uninstall/reset; no lifecycle command; no Scheduled Task mutation; no Gateway/Ollama/plugin/config/AGENTS/SQLite mutation; no process termination; no primary workspace mutation; no reboot; no HermesAgent mutation; no merge/tag/release.

## Result tokens

Use exactly one:

- `PASS_FRESH_TRANSACTION_FAILURE_COVERAGE_CLOSED`
- `BLOCKED_CAUGHT_FAILURE_ROLLBACK`
- `BLOCKED_APPLICATION_DATA_TRANSACTION_BOUNDARY`
- `BLOCKED_EXTERNAL_EFFECT_RECOVERY`
- `BLOCKED_TEST_OR_VALIDATION_FAILURE`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Pre-authorized successor

If ChatGPT independently accepts `PASS_FRESH_TRANSACTION_FAILURE_COVERAGE_CLOSED`, Task 070 may perform the one-time bounded cleanup of the exact Task-066 residue, fresh-install the accepted source, prove owned runtime/no-Hermes durable binding, observe at least three natural PT1M no-flash ticks, and complete final MANAGED/OpenClaw/Ollama/plugin/ownership/AGENTS/SQLite health acceptance without another confirmation.
