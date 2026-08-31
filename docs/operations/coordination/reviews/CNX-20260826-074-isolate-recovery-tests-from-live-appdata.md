# Review — CNX-20260826-074 Isolate Recovery Tests from Live Application Data

Decision: `ACCEPT`

Disposition: `ACCEPT_RECOVERY_TESTS_ISOLATED_AND_TASK073_PRODUCTION_CORRECTION_RELEASED`

## Reviewed heads

- Coordination execution base: `7172c2c01707fef2c145e454f7212486afafc4e8`
- Test-only implementation: `8fc2f4640a761204e9614d2a2fbcfb55cc23d311`
- Report head: `545fc3e6f989e8423ba4e94acc3fe9c60b0fa827`
- Preserved Task-073 production correction: `79b51ed06363f6e8862c491ee0a313ddb412c806`

## Independent findings

1. The Task-073 production correction remains untouched by Task 074.
2. The implementation delta is limited to the two expected test files:
   - `tests/test_fresh_install_transaction_recovery.py`
   - `tests/test_installer_transaction_wiring.py`
3. The affected recovery/transaction tests now use exact temporary application-data product roots shaped as `<tmp>/appdata-local/CogentNexus-OpenClaw` and pass `app_data` / `--app-data` through the actual production APIs/CLI surfaces.
4. The original semantic assertions remain intact: marker-before-mutation, incomplete recovery to coherent fresh, rollback-only-created-paths, unrelated/shared-parent preservation, and crash/rerun recovery.
5. No production global was monkeypatched to hide live state and no live product path was renamed/deleted to obtain GREEN.
6. Reported focused result is 15 passed while the real Task-072 application-data root remains present; before/after live-root SHA inventories match.
7. Full regression gate is now `356 passed, 2 skipped, 0 failed`.
8. PowerShell syntax, npm 11.16.0, npm 12.0.2, plugin validation/tests, exact OpenClaw `2026.7.1-2`, plugin `0.9.3`, baseline consistency and `git diff --check` all pass per report.
9. Publication fence is valid:
   - `7172c2c... -> 8fc2f46...`: one test-only commit touching exactly two test files.
   - `8fc2f46... -> 545fc3e...`: one report-only commit adding exactly the Task-074 report.

## Task-073 closure

Task 073 was reworked only because its required full-suite gate had four live-appdata-coupled test failures. Task 074 independently demonstrates those failures were fixture isolation defects and restores the full suite to zero failures without changing Task-073 production code.

Therefore the production correction at `79b51ed06363f6e8862c491ee0a313ddb412c806` is accepted for the live install-over successor.

## Successor

Task 075 may perform exactly one supported install-over of production commit `79b51ed06363f6e8862c491ee0a313ddb412c806` onto the healthy Task-072 MANAGED installation, then prove source/live parity, upgrade-path ownership/plugin-generation correctness, CogentNexus-owned runtime binding, final MANAGED health and at least three natural PT1M no-flash ticks.
