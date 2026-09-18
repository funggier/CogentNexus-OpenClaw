# CNX-20260918-414 — Ticket DB Bootstrap Native-Stderr Installer Repair Report

## Classification

`TICKET_DB_NATIVE_STDERR_REPAIR_IMPLEMENTED_PENDING_LOCAL_VALIDATION`

## Root cause

CNX-413 terminated at the Windows installer `ticket-db-bootstrap` stage even though the Node child emitted a successful bootstrap result.

The installer runs under:

`$ErrorActionPreference = "Stop"`

and the stage directly invoked:

```powershell
node (Join-Path $pluginDir "scripts\bootstrap-ticket-db.mjs") --workspace $Workspace
$ticketDbExit = $LASTEXITCODE
```

On Windows PowerShell 5.1, native stderr can be promoted to a terminating `NativeCommandError` before the script reaches `$LASTEXITCODE`.

The child emitted Node's benign SQLite experimental warning on stderr:

`ExperimentalWarning: SQLite is an experimental feature and might change at any time`

while otherwise completing the database bootstrap successfully.

## Existing owning-boundary primitive

The same installer already contains:

`Invoke-NativeInstallerDiagnostic`

which was introduced for the same Windows PowerShell 5.1 native-stderr class.

The helper:

- saves the caller's `$ErrorActionPreference`;
- uses `Continue` only around the native child;
- captures merged stdout/stderr;
- snapshots the true native `$LASTEXITCODE`;
- restores the caller preference in `finally`;
- returns `Output` and `ExitCode`.

Existing repository tests already exercise this helper with native stderr on Windows PowerShell 5.1 and prove both zero and nonzero native exit codes remain observable.

The installer also already routes its `npm ci` and `npm run plugin:validate` calls through this helper.

## TDD RED

Commit:

`c0b41078d5a700db5f76340a494dd470cf6f7e6f`

Added:

`tests/test_v095_installer_ticket_db_stderr_boundary.py`

The contract requires:

- no bare `node ... bootstrap-ticket-db.mjs` invocation at the installer stage;
- use of `Invoke-NativeInstallerDiagnostic -Executable "node"`;
- preservation of the ticket-db diagnostic stage start/complete boundary;
- exact workspace argument routing;
- classification by captured child exit code;
- bounded diagnostic on true failure;
- no global `NODE_NO_WARNINGS` / `--no-warnings` suppression.

Against the pre-repair installer, the no-bare-node assertion is intentionally RED.

## Minimal repair

Commit:

`c1baa815d6894f0d619d4d3695c61a442e206e38`

Modified only:

`scripts/install.ps1`

The ticket DB stage now:

1. opens the existing `ticket-db-bootstrap` diagnostic stage;
2. invokes:
   `Invoke-NativeInstallerDiagnostic -Executable "node"`;
3. passes the bootstrap script, `--workspace`, and exact Workspace as arguments;
4. prints captured child output;
5. uses the helper's captured `ExitCode`;
6. completes the diagnostic stage using that exit code;
7. throws only on a true nonzero native exit;
8. includes `Get-BoundedInstallerDiagnostic` output in a true failure.

## What did not change

The repair does not:

- set `NODE_NO_WARNINGS`;
- use `--no-warnings`;
- alter Node runtime flags;
- alter `bootstrap-ticket-db.mjs`;
- change Ticket DB schema/bootstrap semantics;
- weaken nonzero exit failure;
- change installer transaction ordering;
- change native handoff;
- change plugin rollover/install logic;
- change provider/model/auth/routing;
- change OpenClaw dependency versions.

## Production state

No production mutation occurred in CNX-414.

Production remains in the installer-owned partial state left by CNX-413:

- controller passthrough/disabled generation 106;
- plugin disabled;
- Gateway healthy;
- Recovery/Delivery READY;
- pending outbox 0;
- SQLite integrity OK;
- provider/model unchanged;
- no attestation call performed.

No manual enable/restart/install retry is authorized by this report.

## Validation status

This GitHub-side implementation environment did not execute the Windows installer or local PowerShell 5.1 tests.

Therefore GREEN is not claimed yet.

The next bounded validation must prove on the operator's Windows machine:

- the new static ticket-db contract;
- the pre-existing PowerShell 5.1 helper behavior;
- the npm native-stderr regression;
- PowerShell syntax/parser acceptance of `scripts/install.ps1`;
- relevant installer contract regressions.

Only after local validation is GREEN should another production installer invocation be authorized.

## Hard-fence accounting

- Production installer invocation: 0
- Gateway restart/reload: 0
- Semantic/model/provider requests: 0
- Provider/model/auth mutation: 0
- Ticket/outbox/recovery/SQLite production mutation: 0
- OpenClaw dependency change: 0
- Release/tag/main: 0
- Force push/history rewrite: 0

## Final classification

`TICKET_DB_NATIVE_STDERR_REPAIR_IMPLEMENTED_PENDING_LOCAL_VALIDATION`
