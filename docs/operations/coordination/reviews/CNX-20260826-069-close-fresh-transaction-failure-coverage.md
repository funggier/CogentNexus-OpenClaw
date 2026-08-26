# Review — CNX-20260826-069 Close Fresh Transaction Failure Coverage

Decision: `REWORK`

Disposition: `REWORK_NONFRESH_INSTALL_MODE_ABORT_REGRESSION`

Reviewed report result:

`PASS_FRESH_TRANSACTION_FAILURE_COVERAGE_CLOSED`

Execution base:

`6163a549989609c5b57d5688113eb6e9d7567a3f`

Implementation HEAD:

`7f48bb803fe3ca46b7a786e50abe8df22da857fc`

Report HEAD:

`fee1a44b5e2212e3b21f627c57e943eb3154878c`

## Publication fence

Independent VCS comparison passes:

- execution base -> implementation: ahead 1 / behind 0;
- changed implementation files are only `scripts/install.ps1`, `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`, `tests/test_fresh_transaction_failure_coverage.py`, and `tests/test_installer_transaction_wiring.py`;
- implementation -> report: ahead 1 / behind 0;
- report commit adds only `docs/operations/coordination/reports/CNX-20260826-069-close-fresh-transaction-failure-coverage.md`.

## Accepted Task 069 evidence to preserve

The following work is useful and is not rejected by this review:

- one fresh pre-commit try/catch boundary now covers the fresh install operations between successful transaction begin and transaction commit;
- exact application-data product-root transaction authority is materially improved;
- `applicationDataPreexisting` prevents deleting a preexisting product app-data root;
- unsafe transaction-record paths are rejected before being written to `createdPaths`;
- committed markers do not authorize rollback;
- fresh plugin registration has an exact supported inverse using `openclaw plugins uninstall cogentnexus-openclaw --force` when this attempt created the registration;
- managed AGENTS policy application moved after ownership transaction commit;
- shared parent deletion protections from Task 068 remain preserved;
- reported npm 11/npm 12 reproducibility and full tests remain valuable regression evidence.

## Blocking finding — non-fresh modes are unconditionally aborted

The production `scripts/install.ps1` now contains this control flow immediately after the fresh transaction begin section:

```powershell
try {
    if (-not $isFreshTransaction) {
        throw "__UPGRADE_PASSTHROUGH__"
    }
    ... installer body ...
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

Therefore every coherent `upgrade` or `legacy` classification enters the try, immediately throws the sentinel, and terminates installation before the pre-existing upgrade/migration body can execute.

This is not merely a rollback-path distinction; it is a functional regression that disables install-over/upgrade and legacy migration.

The Task 069 report states that non-fresh installs "never enter the rollback path", but the implementation achieves this by aborting non-fresh installation entirely. That does not preserve predecessor behavior.

## Why current tests missed it

The F1/F2/F8 suite concentrates on the fresh transaction path. Its executable F1 harness extracts the production rollback helper and builds a fresh-only injected try/catch fixture. It does not execute or assert a coherent non-fresh installer path to completion.

The structural assertions prove a fresh catch exists, but they do not prove that upgrade/legacy execution remains reachable.

## Required correction

A successor source-only task must restore mode isolation without weakening the accepted fresh behavior:

1. coherent `upgrade` and `legacy` modes must execute the normal installer body rather than being intentionally thrown out of it;
2. failures in non-fresh modes must propagate normally and must never invoke fresh transaction rollback;
3. fresh mode must retain the single caught-failure rollback boundary before transaction commit;
4. successful fresh transaction commit remains after ownership create + exact verify;
5. post-commit behavior remains outside incomplete-transaction rollback authority;
6. remove the sentinel-abort construct or replace it with an equivalent structure that preserves real non-fresh execution;
7. add executable/structural regression tests proving both non-fresh reachability and fresh rollback behavior.

A minimal acceptable shape is one shared try/catch where the catch calls `Invoke-FreshTransactionRollback` only when `$isFreshTransaction` is true, otherwise rethrows the original non-fresh failure unchanged. Equivalent designs are allowed.

## Live state

No live mutation is accepted or authorized by this review. Keep the Task-066 residue untouched and preserve native OpenClaw/Ollama state until the source correction is independently accepted.
