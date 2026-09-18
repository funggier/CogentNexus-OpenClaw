# CNX-20260918-414 — Ticket DB Bootstrap Native-Stderr Installer Repair

Status: `IN_PROGRESS_CHATGPT`

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Parent: `CNX-20260918-413`
- Executor: `ChatGPT`
- Human final authority: `Operator`
- Parent review: `docs/operations/coordination/reviews/CNX-20260918-413-chatgpt-review.md`

## Objective

Repair the Windows PowerShell 5.1 installer boundary that caused CNX-413 to terminate at `ticket-db-bootstrap` even though the Node bootstrap child completed successfully.

The repair must reuse the existing `Invoke-NativeInstallerDiagnostic` helper and preserve installer fail-closed behavior on a true nonzero child exit.

## Root cause

Current `scripts/install.ps1` directly invokes:

```powershell
node (Join-Path $pluginDir "scripts\bootstrap-ticket-db.mjs") --workspace $Workspace
$ticketDbExit = $LASTEXITCODE
```

while the installer runs under `$ErrorActionPreference = "Stop"`.

On Windows PowerShell 5.1, benign native stderr can become a terminating `NativeCommandError` before `$LASTEXITCODE` is observed.

CNX-413 reproduced this with Node's normal SQLite `ExperimentalWarning` on stderr while the child otherwise emitted a successful bootstrap result.

## Required behavior

Route `ticket-db-bootstrap` through:

`Invoke-NativeInstallerDiagnostic`

with:

- executable: `node`
- arguments:
  - `scripts/bootstrap-ticket-db.mjs`
  - `--workspace`
  - exact Workspace path

Then:

1. emit captured child output for diagnostics;
2. classify success/failure exclusively by captured native exit code;
3. preserve `Start-InstallerDiagnosticStage` / `Complete-InstallerDiagnosticStage`;
4. true nonzero exit remains fail-closed;
5. true failure includes bounded captured child diagnostic;
6. do not globally suppress Node warnings;
7. do not change bootstrap script semantics.

## TDD

1. Add RED static contract test proving the installer contains no bare `node ...bootstrap-ticket-db.mjs` call under the Stop boundary and routes that stage through the existing helper.
2. Minimal `install.ps1` repair.
3. Repository-local validation delegated afterward.

## Hard fences

- Repository source/test only.
- No production installer invocation.
- No Gateway restart/reload.
- No production config/state mutation.
- No semantic/model/provider request.
- No Ticket/outbox/recovery/SQLite production mutation.
- No OpenClaw dependency change.
- No release/tag/main.
- No force push/history rewrite.
- Do not start CNX-415 before the repair/report is recorded.

## Exit classification

- `TICKET_DB_NATIVE_STDERR_REPAIR_IMPLEMENTED_PENDING_LOCAL_VALIDATION`
- `REPAIR_BLOCKED_BY_INSTALLER_CONTRACT_CONFLICT`
