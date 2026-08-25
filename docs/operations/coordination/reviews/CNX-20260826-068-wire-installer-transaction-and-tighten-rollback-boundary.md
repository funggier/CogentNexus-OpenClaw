# Review — CNX-20260826-068 Wire Installer Transaction and Tighten Rollback Boundary

Decision: `REWORK`

Disposition: `REWORK_CAUGHT_FAILURE_AND_APPLICATION_DATA_TRANSACTION_GAPS`

Reviewed report result: `PASS_PRODUCTION_INSTALLER_TRANSACTION_WIRED`

Execution HEAD: `85352bb073bb3be1b1a563db40a57f37e892b152`

Implementation HEAD: `2a0ca9fd9abda07765e3da222f7fc4d7730d3d30`

Report HEAD: `3fc596a394fa2167d6c50e1672294c355120e809`

## Publication fence

PASS.

- execution -> implementation: one commit, only `scripts/install.ps1`, `namespace_ownership.py`, and the two focused test files;
- implementation -> report: one commit adding only the Task 068 report.

## Accepted portions

The following Task 068 work is valid and should be preserved:

1. fresh-only `transaction-begin` now occurs after classification and before the first fresh residue-capable workspace mutation;
2. `transaction-record` call sites exist for state root, skill root, launcher, and application-data root;
3. `transaction-commit` is ordered after ownership create and exact verify;
4. upward deletion of shared parents such as `<workspace>\skills` was removed;
5. Task 067 D1 npm 11/npm 12 lockfile reproducibility fix remains unchanged and its regression evidence remains useful;
6. report publication discipline is correct.

## Blocking finding B1 — caught-failure rollback is not wired across the fresh transaction

Task 068 requires: a caught failure during a fresh transaction invokes the production bounded rollback path before surfacing the failure when safe.

Production `scripts/install.ps1` defines `Invoke-FreshTransactionRollback`, but invokes it only for:

- ownership manifest creation failure;
- ownership manifest exact verification failure.

Earlier fresh-transaction failures still throw directly without rollback, including validation, host initialization, policy application, `npm ci`, plugin validation/install, runtime provisioning, plugin resolution, and similar pre-commit failures. This includes the same class of early failure that produced the accepted Task 066 residue.

P3 did not exercise this requirement: `test_p3_rollback_helper_exists_and_reports_both_errors` checks only that a helper definition contains rollback text. It does not inject a production-path failure and prove the helper is reached, residue is removed, original error remains visible, and unrelated state is preserved.

Therefore P3's required behavior is not proven and is not implemented generally.

## Blocking finding B2 — application-data record is incompatible with marker validation

Production fresh install records `%LOCALAPPDATA%\CogentNexus-OpenClaw` in `createdPaths` when the product application-data root does not yet exist.

However `_validate_marker_boundary()` allows created paths only under:

- `stateRoot`;
- `skillPath`;
- launchers.

It does not include the exact `applicationData` product root in the allowlist. Therefore a legitimate fresh marker containing the application's recorded runtime root can later be rejected as an out-of-bound marker by `transaction-rollback` or `recovery-preflight`.

The current P5 tests cover the workspace `skills` parent only and do not execute a rollback/recovery marker containing the exact application-data root.

## Additional integration requirement

Because a fresh installer can create OpenClaw plugin registration before ownership commit, the successor must make caught-failure recovery coherent for any product-owned external effect created before commit. A filesystem rollback alone must not leave plugin registration/config that causes rerun `classify-install` to dead-end. Prefer moving effects that can safely occur post-commit later; for unavoidable pre-commit plugin registration, use a bounded supported inverse and prove the fresh preflight showed no preexisting CNX registration before removing it.

Do not weaken ownership validation and do not broadly delete OpenClaw state.

## Required successor

Create a source/tests-only correction that:

- catches all fresh pre-commit installer failures at the production boundary and performs bounded recovery where safe;
- preserves original + rollback errors;
- makes exact application-data root a first-class validated transaction boundary without permitting parent/path escape;
- validates paths when recording, not only when deleting;
- proves rollback/recovery with application-data sentinels and parent preservation;
- proves a production-path injected failure before ownership commit returns the temp environment to coherent fresh state;
- handles any pre-commit plugin registration with supported bounded inverse or safe reordering;
- preserves all accepted D1/P5 behavior and full tests;
- makes no live mutation.

No Task 069 live install is authorized from this review. Live cleanup/reinstall moves to Task 070 after the correction is independently accepted.
