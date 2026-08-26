# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Updated:** 2026-08-26 11:24 ICT
**Transport:** GitHub repository history
**Human authority:** operator authorized definitive repair through clean reinstall/live acceptance
**Execution trigger:** manual Hermes continuation; scheduled execution remains disabled

## Task 069 review

Task 069 result:

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

### Accepted Task 069 evidence

- fresh pre-commit failures are now conceptually consolidated into one caught recovery boundary;
- exact application-data product-root authority and `applicationDataPreexisting` preservation are implemented;
- unsafe transaction paths are rejected at record time;
- fresh plugin registration has an attempt-scoped supported inverse;
- managed AGENTS policy application moved after transaction commit;
- shared-parent deletion protections remain intact;
- reported full verification was `337 passed, 2 skipped` plus npm 11/npm 12 reproducibility;
- implementation/report publication fence is correct.

### Blocking regression

Production `scripts/install.ps1` now intentionally throws `__UPGRADE_PASSTHROUGH__` whenever `$isFreshTransaction` is false. Its catch then throws `Non-fresh install cannot use the fresh transaction failure boundary.`

This means coherent upgrade and legacy installs do not merely bypass fresh rollback; they abort before the existing install-over/migration body executes.

Task 069 tests did not exercise non-fresh installer reachability, so the regression passed the suite.

## Current live baseline

Machine remains in accepted Task-066 native state: no CNX Supervisor task, launcher or plugin registration; Gateway/Ollama healthy; Task-066 partial unowned residue remains intentionally untouched; AGENTS managed block absent.

## Active Task 070

[`tasks/CNX-20260826-070-restore-nonfresh-installer-mode-isolation.md`](tasks/CNX-20260826-070-restore-nonfresh-installer-mode-isolation.md)

Status: `READY_FOR_HERMES`

Authorization: `INSTALLER_MODE_ISOLATION_REWORK_AUTHORIZED`

Execution mode: `SOURCE_REWORK_TDD_INSTALLER_MODE_ISOLATION`

Task 070 must restore normal upgrade/legacy execution, keep fresh rollback scoped only to fresh transactions, prove non-fresh failures never call fresh rollback, and preserve all accepted npm/transaction/application-data/shared-parent protections.

## Live hard fence

No live residue cleanup, install/install-over/uninstall/reset/lifecycle action, Scheduled Task mutation, Gateway/Ollama/plugin/config/AGENTS/SQLite mutation, process termination, reboot, primary workspace mutation, HermesAgent mutation, merge/tag/release.

## Next gate

If Task 070 reports `PASS_INSTALLER_MODE_ISOLATION_RESTORED`, ChatGPT independently reviews mode reachability, fresh/non-fresh failure isolation, full tests, npm regressions and report-only publication fence.

Only after acceptance may Task 071 perform the one-time bounded cleanup of the exact Task-066 residue and complete fresh installation, owned-runtime/no-Hermes binding, at least three natural PT1M no-flash ticks and final MANAGED health acceptance.
