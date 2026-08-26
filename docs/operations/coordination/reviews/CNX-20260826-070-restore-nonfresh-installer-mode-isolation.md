# Review — CNX-20260826-070 Restore Non-Fresh Installer Mode Isolation

Decision: `REWORK`

Disposition: `REWORK_MODE_SPECIFIC_UPGRADE_LEGACY_EVIDENCE_MISSING`

Reviewed report result: `PASS_INSTALLER_MODE_ISOLATION_RESTORED`

Implementation HEAD: `9df671670908241486afe2badf8a7f221410c6f8`

Report HEAD: `573ca752e1c257a071d9a56b4206039c911b3b56`

## Publication fence

PASS.

- Coordination base `71fdc6646719dd7477c66788a946a05c95e5506c` → implementation `9df671670908241486afe2badf8a7f221410c6f8`: one implementation commit touching only `scripts/install.ps1`, `tests/test_fresh_transaction_failure_coverage.py`, and new `tests/test_installer_mode_isolation.py`.
- Implementation → report `573ca752e1c257a071d9a56b4206039c911b3b56`: one report-only commit adding only the Task-070 report.

## Accepted implementation observations

Independent source inspection confirms the Task-069 synthetic non-fresh abort is removed.

The production shape at `9df6716` is now shared-body mode isolation:

```powershell
try {
    # common fresh / upgrade / legacy installer body
    ...
    if ($isFreshTransaction) {
        transaction-commit ...
    }
}
catch {
    if ($isFreshTransaction) {
        Invoke-FreshTransactionRollback ...
    }
    throw
}
```

Therefore the specific Task-069 sentinel regression is corrected in source. Fresh rollback remains guarded by `$isFreshTransaction`, and non-fresh failures are not routed through the fresh rollback helper.

The report also provides fresh evidence for full pytest, npm 11/npm 12, syntax parsing, and the accepted transaction regressions.

These portions are retained as accepted candidate evidence and should not be redesigned without a failing proof.

## Blocking evidence gap

Task 070 explicitly required executable mode-specific evidence for both non-fresh classifications.

### Missing M4 — coherent upgrade marker isolation

The task required a temp coherent ownership fixture or faithful production-classification harness that drives the upgrade mode guard and proves no `install-transaction.json` is created or modified before an injected stop point.

The published `tests/test_installer_mode_isolation.py` contains no M4 executable test. The report instead states M4 is covered by existing transaction suites plus M1 structural reachability. That does not drive an actual coherent `upgrade` classification and therefore does not prove the required mode-specific invariant.

### Missing M5 — legacy marker isolation and migration reachability

The task required an isolated legacy fixture satisfying the minimum `prove_legacy_ownership()` contract, or an equivalent production mode harness, proving:

- classification reaches `legacy`;
- no fresh transaction marker is created;
- migration/native-handoff path is reachable rather than synthetically aborted.

The published test file contains no M5 executable test. M1's `$isFreshTransaction = $false` mirror harness does not distinguish `upgrade` from `legacy` and does not exercise production classification or legacy ownership proof.

A repository search also found no `test_m4` / `test_m5` mode-isolation tests elsewhere.

## Why this blocks live Task 071/072

The source correction appears narrow and plausible, but the explicit acceptance contract required evidence that both supported non-fresh modes remain reachable and never create fresh transaction state. Moving to live cleanup/reinstall without that evidence would repeat the failure mode that Task 070 was created to prevent: a mode-isolation regression escaping structural tests.

## Required rework

Do not redesign the installer unless the new executable tests expose a real defect.

Add mode-specific production-facing tests that:

1. construct a coherent v0.9.3 upgrade fixture accepted by `classify_install()` and prove `mode == upgrade`;
2. drive the production fresh guard/boundary to an injected pre-side-effect stop and prove no transaction marker is created/modified;
3. construct a minimum valid legacy fixture accepted by `prove_legacy_ownership()` / `classify_install()` and prove `mode == legacy`;
4. prove the legacy/native-handoff branch is reachable through the same production boundary and no fresh marker is created;
5. inject a non-fresh failure for each mode and prove no `transaction-rollback` or fresh plugin inverse occurs;
6. re-run fresh failure regression and the full verification gates.

If these tests pass against `9df6716` without production changes, the implementation may remain unchanged and the successor may be evidence/tests-only.

## Live fence

No live Task-066 residue cleanup, install/uninstall/reset/lifecycle mutation, Scheduled Task change, Gateway/Ollama/plugin/config/AGENTS/SQLite mutation, process termination, reboot, primary workspace mutation, HermesAgent mutation, merge/tag/release.
