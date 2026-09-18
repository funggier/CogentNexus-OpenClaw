# CNX-20260918-415 — Ticket DB Native-Stderr Repair Local Validation

## Classification

`TICKET_DB_STDERR_LOCAL_REPAIR_GREEN`

CNX-414 source validation required a bounded test-contract repair caused directly by the new ticket-db helper call. The production installer source was not changed in CNX-415.

## Authority and candidate

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- GitHub remote authoritative tip at start: `682a90efccf5c746f4f87c3fe69ced75910d9dc4`
- Starting local HEAD: `682a90efccf5c746f4f87c3fe69ced75910d9dc4`
- Exact CNX-414 product/source candidate: `c1baa815d6894f0d619d4d3695c61a442e206e38`
- Candidate relationship: candidate is an ancestor of the authoritative remote tip; validation used the fetched remote tip, not a reset to the embedded candidate SHA.
- Validation/repair commit before report publication: `54ce03caa7b90dd32c4a0aec5eb3db92a797e25f`

The remote branch was fetched before reading coordination authority. ACTIVE and STATUS both confirmed `READY_FOR_HERMES` and `CNX-20260918-415`.

## RED, root cause, and minimal repair

The first required run produced two directly related REDs:

1. `python -m pytest tests/test_v095_installer_ticket_db_stderr_boundary.py -q`
   - `1 failed, 1 passed`
   - The test selected an earlier `if (-not $SkipPlugin)` block and did not reach the repaired ticket-db stage.
2. `python -m pytest tests/test_installer_observability_contract.py -q`
   - `1 failed, 1 passed`
   - The contract still searched for the removed bare `node ... bootstrap-ticket-db.mjs` command and only accepted the older `$prepareCapture.ExitCode` spelling.

Root cause was stale test contracts after CNX-414's authorized source change. The minimal repair was test-only:

- anchor the ticket-db boundary test at the `ticket-db-bootstrap` diagnostic stage;
- require the existing `Invoke-NativeInstallerDiagnostic -Executable "node"` call;
- update the observability contract to recognize the helper invocation and `$ticketDbCapture.ExitCode`.

No installer redesign, warning suppression, dependency change, or production mutation was performed.

## Exact validation commands and results

### Required focused tests

```text
python -m pytest tests/test_v095_installer_ticket_db_stderr_boundary.py -q
```

Result after repair: `2 passed in 0.02s`

```text
python -m pytest tests/test_task247_powershell51_native_stderr.py -q
```

Result: `2 passed in 2.65s`

This executed real Windows PowerShell 5.1; it was not skipped.

```text
python -m pytest tests/test_v095_installer_npm_stderr_boundary.py -q
```

Result: `1 passed in 0.02s`

### Required installer regression tests

```text
python -m pytest tests/test_installer_observability_contract.py tests/test_task239_rollover_diagnostics.py tests/test_namespace_install_contract.py tests/test_v095_installer_npm_stderr_boundary.py -q
```

Result: `17 passed in 0.24s`

### Additional established installer-focused validation

The repository contained these additional installer-focused tests, so the bounded suite was run:

```text
python -m pytest tests/test_v095_installer_ticket_db_stderr_boundary.py tests/test_v095_installer_state_compat.py tests/test_v095_installer_npm_stderr_boundary.py tests/test_v095_installer_cli_contract.py tests/test_provider_neutral_installer_boundary.py tests/test_posix_provider_neutral_installer_boundary.py tests/test_npm_pack_installer_boundary.py tests/test_installer_transaction_wiring.py tests/test_installer_runtime_authority.py tests/test_installer_observability_contract.py tests/test_installer_mode_isolation.py -q
```

Result: `40 passed in 25.89s`

### PowerShell 5.1 parser validation

The installer was parsed, not executed, with Windows PowerShell 5.1's parser API:

```text
powershell.exe -NoProfile -NonInteractive -Command '$tokens=$null; $errors=$null; [System.Management.Automation.Language.Parser]::ParseFile("C:\Users\CDQ-P\CogentNexus-OpenClaw-cnx415\scripts\install.ps1", [ref]$tokens, [ref]$errors) | Out-Null; Write-Output ("PS_VERSION=" + $PSVersionTable.PSVersion.ToString()); Write-Output ("PARSER_ERRORS=" + $errors.Count); if ($errors.Count -gt 0) { $errors | ForEach-Object { $_.ToString() }; exit 1 }'
```

Result:

```text
PS_VERSION=5.1.19041.6456
PARSER_ERRORS=0
```

The installer was not dot-sourced and was not executed.

## Required behavioral proof

1. **No bare ticket-db Node call:** source contains the ticket-db diagnostic stage and `Invoke-NativeInstallerDiagnostic -Executable "node"`; the old bare invocation is absent.
2. **Native stderr + exit 0:** Task-247's real PS5.1 test passed with stderr marker and captured `exitCode == 0`; PowerShell continued successfully.
3. **Native stderr + nonzero:** Task-247's real PS5.1 test passed with complete stderr sentinels and exact `exitCode == 23`.
4. **Preference restoration:** both Task-247 cases asserted the caller preference remained `Stop` before and after the helper.
5. **START/COMPLETE diagnostics:** ticket-db contract and observability regression passed; the stage remains bracketed by `Start-InstallerDiagnosticStage` and `Complete-InstallerDiagnosticStage`.
6. **Fail-closed nonzero behavior:** ticket-db contract passed for captured exit classification and the true-failure path using `Get-BoundedInstallerDiagnostic` and `throw` on nonzero exit.
7. **No global Node warning suppression:** source contract passed with neither `NODE_NO_WARNINGS` nor `--no-warnings` present.
8. **npm protections:** npm native-stderr boundary test passed; the complete installer-focused suite passed.
9. **PS5.1 syntax:** parser errors were zero on Windows PowerShell 5.1.

## Hard-fence accounting

- Production installer invocation: 0
- Production install/install-over: 0
- Gateway restart/reload: 0
- Production lifecycle command: 0
- Plugin enable/disable mutation: 0
- Production config/state mutation: 0
- Ticket/outbox/recovery/SQLite production mutation: 0
- Semantic/model/provider requests: 0
- Provider/model/auth/routing mutation: 0
- OpenClaw dependency patch/version change: 0
- Release/tag/main changes: 0
- Force push/history rewrite: 0
- CNX-416 created/started: 0
- Installer execution or dot-sourcing during parser validation: 0

## Closeout state

The source/test validation and the authorized minimal test repair are complete. ACTIVE.md and STATUS.md are set to `WAITING_FOR_CHATGPT_REVIEW`. The final remote HEAD, report blob, changed paths, and clean worktree are verified after publication.

No production installer retry was performed, and no CNX-416 was created or started.
