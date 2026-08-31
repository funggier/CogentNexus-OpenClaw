# CNX-20260826-068 — Wire Installer Transaction and Tighten Rollback Boundary

Status: `READY_FOR_HERMES`

Execution mode: `SOURCE_REWORK_TDD_PRODUCTION_INSTALLER_TRANSACTION`

Current authorization: `INSTALLER_TRANSACTION_WIRING_REWORK_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes after the operator's continuation signal

## Goal

Correct the remaining D2 defects from Task 067 by wiring the already-created fresh-install transaction/recovery API into the actual Windows installer, and make rollback stop at exact CogentNexus-owned roots.

This is source/tests only. Preserve the accepted Task 067 D1 lockfile/npm reproducibility fix unchanged unless a failing regression proves a minimal correction is necessary.

## Accepted predecessor evidence

Task 067 report result:

`PASS_INSTALL_REPRODUCIBILITY_AND_PARTIAL_RECOVERY_FIXED`

Implementation HEAD:

`ec51d7b20c228070a95a6cf0987cebd7e71cbfaf`

Report HEAD:

`30075a3a3e646f24e0144f74aac9104c0ce1e888`

Independent review:

Decision: `REWORK`

Disposition:

`REWORK_INSTALLER_TRANSACTION_NOT_WIRED_AND_ROLLBACK_PARENT_BOUNDARY`

Review commit:

`38b46a4e78a9a2a2bcfc2c2cbaa230d888f7312c`

Task 067 D1 lockfile/package correction is accepted as `ACCEPT_LOCKFILE_REPRODUCIBILITY_FIX` and must remain passing under npm 11.16.0 and npm 12.0.2.

## Current live preservation boundary

Do not mutate the live machine in this task.

Accepted live state remains:

- old Hermes-bound Supervisor task absent;
- `cnxclaw.cmd` absent;
- CogentNexus plugin unregistered;
- AGENTS managed block absent / baseline restored;
- OpenClaw Gateway native and healthy;
- Ollama healthy;
- Task-066 partial residue remains at the two reported workspace roots without valid `ownership.json`;
- no fresh CogentNexus installation is active.

No cleanup/adoption/install is authorized in Task 068.

## Confirmed defects

### D2a — transaction API is not wired into production install.ps1

The Task 067 implementation added `recovery-preflight` before classification, but the production installer never invokes `transaction-begin`, `transaction-record`, `transaction-commit`, or a caught-failure rollback surface.

Therefore the production fresh-install crash window is unchanged: skill/state artifacts can still be created before any recovery marker exists.

### D2b — tests exercise API order, not production installer order

Current R1/R1b call `begin_fresh_transaction()` directly and then synthesize residue. They do not prove `scripts/install.ps1` itself begins the transaction before its first fresh residue-capable mutation.

### D2c — rollback can remove shared parent namespace

`rollback_transaction()` and `recovery_preflight()` may remove `<workspace>\skills` after removing `<workspace>\skills\cogentnexus-openclaw` when the shared parent becomes empty.

Deletion authority must stop at exact CNX-owned roots. Empty shared parents remain out of scope.

## Required production behavior

### 1. Begin transaction at the exact installer boundary

After `classify-install` has successfully proven `mode == fresh`, but before the first operation that can leave a new CogentNexus artifact, production `scripts/install.ps1` must invoke the installed/source ownership surface to begin the fresh transaction.

The transaction marker itself may create the CNX state root; that marker is the authorized first fresh mutation.

Do not begin a fresh transaction for coherent upgrade or legacy migration paths.

### 2. Record recoverable created paths

For the fresh path, record every product-owned artifact/root whose creation may survive a failure and that rollback/recovery is authorized to remove. At minimum cover the actual residue-capable surfaces used by the installer, including as applicable:

- `<workspace>\.cogentnexus-openclaw` owned state root contents created by install;
- `<workspace>\skills\cogentnexus-openclaw`;
- `<workspace>\cnxclaw.cmd`;
- `%LOCALAPPDATA%\CogentNexus-OpenClaw` product runtime/application-data root if created during the transaction.

Plugin/config/task effects that require their own supported inverse must not be silently represented as filesystem deletion if that would bypass OpenClaw/Task Scheduler ownership semantics. Keep rollback behavior explicit and bounded.

Recording must occur before or atomically with the corresponding creation such that a crash cannot leave an unrecorded fresh artifact.

### 3. Caught failure rollback

A caught failure during a fresh transaction must invoke the production bounded rollback path before surfacing the failure, when it is safe to do so.

Do not mask rollback failure. Report both the original install error and rollback error/state.

A hard process crash/power loss remains covered by rerun `recovery-preflight` from the durable incomplete marker.

### 4. Successful commit

After `ownership.json` has been created and `verify_manifest` succeeds, production installer must invoke `transaction-commit`/equivalent so the marker no longer authorizes cleanup.

Do not mark committed before ownership verification.

### 5. Exact deletion boundary

Rollback/recovery may remove exact owned roots and their recorded descendants, but must never walk upward and delete shared parents such as:

- `<workspace>\skills`;
- `<workspace>`;
- `<LOCALAPPDATA>`;
- OpenClaw state roots outside exact CogentNexus ownership.

Remove the upward parent-walk behavior beyond exact product roots.

### 6. Marker validation remains fail-closed

Preserve Task 067 protections:

- unmarked residue is not adopted/deleted;
- tampered schema rejected;
- out-of-bound recorded paths rejected before deletion;
- committed marker without coherent ownership authorizes nothing;
- canonical ancestry checks remain mandatory.

## Strict TDD requirements

Use an isolated worktree/clone from current coordination HEAD. No production edit before the relevant RED is observed.

### P1 — production installer begin ordering RED/GREEN

Add an installer-facing test that inspects or executes the actual production `scripts/install.ps1` control path and proves:

1. fresh classification occurs;
2. `transaction-begin` is invoked only for fresh mode;
3. the begin call occurs before the first residue-capable mutation (`New-Item`/staging/copy/move/host init or equivalent fresh artifact creation).

RED against `ec51d7b...` must fail because no begin invocation exists.

A test that merely calls `begin_fresh_transaction()` directly is insufficient.

### P2 — production record coverage

Add a production installer contract/executable harness proving fresh-created state/skill/launcher/application-data paths are recorded before or atomically with creation.

Removing a required transaction-record call from `install.ps1` must make this test fail.

### P3 — production caught-failure rollback

Use a temp/non-live PowerShell harness or extracted production helper used by `install.ps1` to inject a failure after state/skill creation but before ownership commit.

Prove:

- rollback is invoked;
- exact CNX residue is removed/returned coherent fresh;
- original failure remains visible;
- unrelated workspace content is untouched.

### P4 — production success commit ordering

Prove transaction commit occurs after ownership create + verify and before final success reporting. Moving commit before verification must fail the test.

### P5 — shared parent preservation

Create a temp workspace with a preexisting empty/shared `skills` directory. Run rollback/recovery for recorded `skills\cogentnexus-openclaw` residue.

Assert:

- `skills\cogentnexus-openclaw` is removed;
- `<workspace>\skills` still exists;
- unrelated sibling directories/files remain unchanged.

Also test equivalent exact-root preservation around application-data parents where applicable.

RED against Task 067 rollback should expose the current upward parent deletion.

### P6 — preserve malicious/unmarked failure tests

Keep all Task 067 R5/R5b/R6 tests passing.

### P7 — crash/rerun production integration

Simulate a fresh installer interruption after at least one real transaction-recorded artifact exists, without invoking caught rollback. Run production `recovery-preflight` as the rerun installer does, then prove `classify-install` returns `fresh`.

This must use the same marker/recording contract wired by the production installer rather than separately constructed pseudocode.

## D1 regression gate

Re-run and preserve:

- clean `npm ci` with npm 11.16.0 / node v24.18.0;
- clean `npm ci` with npm 12.0.2 / compatible node;
- `npm run plugin:validate` under both;
- `npm test` under both;
- package-content/pack validation under both;
- exact OpenClaw dependency `2026.7.1-2` and plugin version `0.9.3`.

No fallback to permissive npm is allowed.

## Full verification

Run fresh:

1. P1-P7 RED/GREEN evidence as applicable;
2. existing transaction/recovery tests;
3. installer/runtime/ownership/startup focused tests;
4. full `pytest tests/ -q` in isolated dev venv with `requirements-dev.txt`;
5. both npm toolchain validation gates above;
6. `python scripts/check_baseline_consistency.py`;
7. `git diff --check`;
8. clean worktree after implementation commit.

Record exact counts and any skips.

## Publication discipline

Use separate commits:

1. implementation/tests commit(s);
2. report-only commit adding only:

`docs/operations/coordination/reports/CNX-20260826-068-wire-installer-transaction-and-tighten-rollback-boundary.md`

Report must state fetched execution HEAD, implementation HEAD, RED/GREEN evidence, production installer call ordering, rollback boundary proof, full test counts, npm 11/12 regression results, and explicit no-live-mutation accounting.

## Live hard fence

No live residue cleanup, install/install-over/uninstall/reset, lifecycle mutation, Scheduled Task change/run/end, Gateway/Ollama/plugin/config/AGENTS/SQLite mutation, process termination, reboot, primary workspace mutation, HermesAgent mutation, merge/tag/release.

## Result tokens

Use exactly one:

- `PASS_PRODUCTION_INSTALLER_TRANSACTION_WIRED`
- `BLOCKED_INSTALLER_TRANSACTION_INTEGRATION`
- `BLOCKED_ROLLBACK_BOUNDARY_SAFETY`
- `BLOCKED_TEST_OR_VALIDATION_FAILURE`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Pre-authorized successor

If Task 068 is independently accepted, proceed to a separate live Task 069 without further confirmation. Task 069 may re-prove and remove only the exact Task-066-created residue, fresh-install the accepted source, prove owned runtime/no-Hermes durable binding, observe at least three natural PT1M ticks with no console/conhost chain, and complete final MANAGED/OpenClaw/Ollama/plugin/ownership/AGENTS/SQLite health acceptance.
