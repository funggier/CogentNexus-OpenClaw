# CNX-20260918-415 — Ticket DB Native-Stderr Repair Local Validation

Status: `READY_FOR_HERMES`

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Parent: `CNX-20260918-414`
- Executor: `Hermes`
- Reviewer: `ChatGPT`
- Human final authority: `Operator`
- Parent report: `docs/operations/coordination/reports/CNX-20260918-414-ticket-db-bootstrap-native-stderr-installer-repair-report.md`
- Exact product/source candidate: `c1baa815d6894f0d619d4d3695c61a442e206e38`

GitHub remote is authoritative.

## Objective

Validate the CNX-414 Windows PowerShell 5.1 ticket DB bootstrap stderr repair on the operator's local Windows checkout.

This task is source/test validation only.

Do not invoke the production installer.

## Required focused tests

At minimum run:

```text
python -m pytest tests/test_v095_installer_ticket_db_stderr_boundary.py -q
python -m pytest tests/test_task247_powershell51_native_stderr.py -q
python -m pytest tests/test_v095_installer_npm_stderr_boundary.py -q
```

The Task-247 tests must execute under real Windows PowerShell 5.1 rather than being skipped. If they skip because `powershell.exe` cannot be found, treat that as insufficient validation, not GREEN.

## PowerShell syntax validation

Parse the repaired installer without executing it.

Use Windows PowerShell 5.1 and the PowerShell parser API, e.g. a bounded equivalent of:

```powershell
$tokens = $null
$errors = $null
[System.Management.Automation.Language.Parser]::ParseFile(
  "<exact-candidate>\scripts\install.ps1",
  [ref]$tokens,
  [ref]$errors
) | Out-Null
$errors
```

Require zero parser errors.

Do not dot-source or execute the installer.

## Required installer regression validation

Run the relevant installer/static-contract regressions already in the repository, including at minimum:

- `tests/test_installer_observability_contract.py`
- `tests/test_task239_rollover_diagnostics.py`
- `tests/test_namespace_install_contract.py`
- `tests/test_v095_installer_npm_stderr_boundary.py`
- `tests/test_v095_installer_ticket_db_stderr_boundary.py`

If additional installer-focused tests are discovered by the repository's normal bounded validation convention, run them and record them exactly.

## Required behavioral proof

The validation must prove:

1. ticket DB bootstrap no longer uses a bare native Node call under `ErrorActionPreference=Stop`;
2. Node/native stderr with exit code 0 does not terminate PowerShell 5.1 before exit classification;
3. native stderr with nonzero exit preserves the child exit code and diagnostic;
4. caller `ErrorActionPreference` is restored after the helper returns;
5. ticket DB stage still emits START/COMPLETE diagnostics;
6. nonzero ticket DB child exit remains fail-closed;
7. Node warnings are not globally suppressed;
8. npm stderr protections remain GREEN;
9. installer syntax remains valid in Windows PowerShell 5.1.

## Repair authority

If validation exposes a bounded defect caused by CNX-414, minimal source/test repair is authorized using:

`RED -> root cause -> minimal fix -> GREEN`

Do not expand into installer redesign.

## Hard fences

- No production installer invocation.
- No production install/install-over.
- No Gateway restart/reload.
- No production lifecycle command.
- No plugin enable/disable mutation.
- No production config/state mutation.
- No Ticket/outbox/recovery/SQLite production mutation.
- No semantic/model/provider request.
- No provider/model/auth/routing mutation.
- No OpenClaw dependency patch/version change.
- No release/tag/main.
- No force push/history rewrite.
- Do not create/start CNX-416 yourself.

## Exit classification

Use one:

- `TICKET_DB_STDERR_LOCAL_VALIDATION_GREEN`
- `TICKET_DB_STDERR_LOCAL_REPAIR_GREEN`
- `TICKET_DB_STDERR_LOCAL_VALIDATION_FAILED`
- `BLOCKED_BY_POWERSHELL51_TEST_ENVIRONMENT`

## Closeout

Publish:

`docs/operations/coordination/reports/CNX-20260918-415-ticket-db-native-stderr-repair-local-validation-report.md`

Then set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW`, verify local HEAD equals remote HEAD, verify clean worktree, and stop.

Do not retry the production installer in CNX-415.
