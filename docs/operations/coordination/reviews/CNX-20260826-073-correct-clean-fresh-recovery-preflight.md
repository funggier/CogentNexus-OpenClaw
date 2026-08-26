# Review — CNX-20260826-073 Correct Clean-Fresh Recovery Preflight Semantics

Decision: `REWORK`

Disposition: `REWORK_FULL_SUITE_LIVE_APPDATA_FIXTURE_COUPLING`

Reviewed report result: `PASS_CLEAN_FRESH_RECOVERY_PREFLIGHT_CORRECTED`

Implementation HEAD: `79b51ed06363f6e8862c491ee0a313ddb412c806`

Report HEAD: `ba4a04825fb7396617fa0fe17c62f84f5f5e1507`

## Accepted production correction

Independent source inspection accepts the substantive Task-073 production changes as the correction candidate:

- `recovery_preflight()` now distinguishes clean markerless/no-inventory state and returns `CLEAN_FRESH`;
- markerless new-namespace residue remains fail-closed;
- incomplete-marker recovery and ownership-present behavior remain intact;
- `scripts/install.ps1` now captures recovery-preflight exit/output, stops on nonzero before classification, and fail-closes unknown successful statuses;
- recovery preflight remains before classification and fresh transaction begin.

Do not redesign or revert these changes unless a new executable regression demonstrates a defect.

## Publication fence

PASS.

`99a22c6682a81254d18071af8ed2fcb6fcd28328 -> 79b51ed06363f6e8862c491ee0a313ddb412c806` changes only production correction/tests in scope.

`79b51ed06363f6e8862c491ee0a313ddb412c806 -> ba4a04825fb7396617fa0fe17c62f84f5f5e1507` adds only the Task-073 report.

## Blocking finding

Task 073 explicitly required full `pytest tests/ -q` as a regression gate and provides `BLOCKED_TEST_OR_VALIDATION_FAILURE` as a result token. The report nevertheless claims PASS while recording `4 failed` in the full suite.

The four failures are reproducible fixture-environment coupling, not evidence against the accepted production correction. Older transaction tests call production inventory/recovery surfaces without an isolated `app_data`, so production defaults resolve to the real `%LOCALAPPDATA%\CogentNexus-OpenClaw`. That product root now legitimately exists because Task 072 installed CogentNexus live. Consequently isolated temp-workspace tests can observe the real live application-data product root and fail.

This is still a regression-suite defect: the full suite is not deterministic or isolated on a machine with a valid installed product, and the explicit Task-073 full-suite gate is not green.

## Required successor correction

Use test-only changes unless a new RED proves production behavior wrong.

- isolate every affected fresh-install/recovery test from real user `%LOCALAPPDATA%` by passing an exact temp `.../CogentNexus-OpenClaw` application-data root consistently through begin/inventory/classify/recovery/rollback surfaces;
- include the installer-wiring crash/rerun fixture named in the Task-073 report;
- preserve the semantic intent of those tests; do not hide failures by deleting/renaming the live product root, changing environment globally, or weakening production inventory behavior;
- prove the affected tests RED in the current live-installed environment before test correction and GREEN after correction;
- run the entire full pytest suite to zero failures;
- rerun Task-073 focused recovery semantics, mode-isolation, transaction, npm 11/npm 12, PowerShell syntax, baseline consistency and diff checks;
- do not mutate the healthy Task-072 live installation.

Task 074 is authorized for this test-isolation correction only.
