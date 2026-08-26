# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Updated:** 2026-08-26 16:19 ICT
**Transport:** GitHub repository history
**Human authority:** operator authorized definitive repair through clean reinstall/live acceptance
**Execution trigger:** manual Hermes continuation; scheduled execution remains disabled

## Task 070 review

Task 070 result:

`PASS_INSTALLER_MODE_ISOLATION_RESTORED`

Implementation HEAD:

`9df671670908241486afe2badf8a7f221410c6f8`

Report HEAD:

`573ca752e1c257a071d9a56b4206039c911b3b56`

Independent review:

Decision `REWORK`

Disposition:

`REWORK_MODE_SPECIFIC_UPGRADE_LEGACY_EVIDENCE_MISSING`

Review commit:

`3b3cea20d02e66e34704bd3ee8d1ed79f1610b79`

### Accepted candidate source observations

Independent review confirms the Task-069 synthetic non-fresh sentinel was removed from production. `scripts/install.ps1` now has a shared fresh/upgrade/legacy body and a catch that calls `Invoke-FreshTransactionRollback` only when `$isFreshTransaction` is true. Fresh transaction begin and commit remain fresh-only, with commit after ownership create + exact verify.

Task 070 publication fence also passed, and its report recorded full pytest `342 passed, 2 skipped`, PowerShell syntax success, and npm 11/npm 12 gates.

### Remaining evidence gap

Task 070 explicitly required executable M4/M5 mode-specific proofs but the published test suite does not contain them.

- No coherent v0.9.3 `upgrade` fixture executes production `classify_install()` and proves no fresh transaction marker is created/modified.
- No valid legacy ownership fixture executes production `classify_install()` / `prove_legacy_ownership()` and proves legacy migration/native-handoff reachability with no fresh marker.
- Existing M1/M2 executable harnesses set `$isFreshTransaction=$false` generically and therefore do not prove the separate production classification contracts.

## Current live baseline

Machine remains in the accepted Task-066 native state: no CNX Supervisor task, launcher or plugin registration; AGENTS managed block absent; Gateway/Ollama healthy; Task-066 partial unowned residue remains intentionally untouched; no valid ownership manifest.

## Active Task 071

[`tasks/CNX-20260826-071-prove-upgrade-legacy-mode-isolation.md`](tasks/CNX-20260826-071-prove-upgrade-legacy-mode-isolation.md)

Status: `READY_FOR_HERMES`

Authorization: `MODE_SPECIFIC_NONFRESH_VERIFICATION_AUTHORIZED`

Execution mode: `SOURCE_TEST_VERIFICATION_MODE_SPECIFIC_NONFRESH_ISOLATION`

Task 071 must add production-facing coherent upgrade and valid legacy fixtures, prove exact classification/reachability and absence of fresh transaction marker/rollback for each mode, preserve fresh rollback behavior, and rerun full/npm regression gates. Prefer test-only changes if production `9df6716` already satisfies the new executable proofs.

## Live hard fence

No live residue cleanup, install/install-over/uninstall/reset/lifecycle action, Scheduled Task mutation, Gateway/Ollama/plugin/config/AGENTS/SQLite mutation, process termination, reboot, primary workspace mutation, HermesAgent mutation, merge/tag/release.

## Next gate

If Task 071 reports `PASS_UPGRADE_LEGACY_MODE_ISOLATION_PROVEN`, ChatGPT must independently review the upgrade/legacy fixtures, mode-specific marker/rollback isolation, fresh regression, full tests, npm gates, and report-only publication fence.

Only after acceptance may Task 072 perform the one-time bounded cleanup of exact Task-066 residue and complete fresh installation, owned-runtime/no-Hermes binding, at least three natural PT1M no-flash ticks, and final MANAGED health acceptance.
