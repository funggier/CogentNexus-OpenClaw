# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK248_TASK247_REPAIRED_CANDIDATE_WINDOWS_INSTALL_OVER_REQUALIFICATION`
Current disposition: `TASK247_ACCEPTED_PASS__POWERSHELL51_NATIVE_STDERR_CAPTURE_REPAIRED__LIVE_INSTALLER_REQUALIFICATION_REAUTHORIZED`
Task ID: `CNX-20260904-248`
Parent task: `CNX-20260904-247`
Installer failure lineage: `CNX-20260904-245`, `CNX-20260904-246`
Harness lineage: `CNX-20260904-243`, `CNX-20260904-244`, `CNX-20260904-245`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-04 ICT
Executor: Hermes / authenticated Windows operator
Coordinator / independent reviewer: ChatGPT

## Accepted Task-247 result

Independent review verdict:

`ACCEPT_PASS_POWERSHELL51_NATIVE_STDERR_CAPTURE_REPAIRED__FINAL_ANCESTRY_RED_PROVEN__REPORT_RED_SHA_STALE_NONBLOCKING__LIVE_INSTALLER_REQUALIFICATION_AUTHORIZED_SEPARATELY`

Reviewed Task-247 report HEAD:

`8cbbe2d405477e7b7c91b3fb649582e3a400e893`

Accepted repaired executable candidate:

`6c11a5e8f417300835e85441b88e0f37e3897353`

Expected plugin fingerprint:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Task 247 reproduced the real Windows PowerShell 5.1 `NativeCommandError` truncation under `$ErrorActionPreference='Stop'` and repaired only the native capture boundary. The final-ancestry RED is test-only commit `f5f04a7422be05f446d408d48e949473a113dc36`; the report's pre-rebase RED SHA is stale but nonblocking.

Exact repaired-candidate Actions are GREEN:

```text
PS5.1 Acceptance Smoke        33884732550 = SUCCESS
Windows Installer Pack Smoke 33884732528 = SUCCESS
Validate                      33884732569 = SUCCESS (attempt 2, same SHA)
```

## Active Task 248

Execute:

`docs/operations/coordination/tasks/CNX-20260904-248-task247-repaired-candidate-windows-install-over-requalification.md`

Required sequence:

```text
fresh GitHub/live preflight
-> fresh detached exact candidate 6c11a5e8...
-> prove clean source + plugin fingerprint + Task247 repair
-> create fresh non-temp durable evidence root
-> regenerate/hash/direct-qualify frozen hardened runner
-> create/hash/readback frozen launch manifest
-> prove exact installer -File binding
-> register installer Scheduled Task at most once
-> immediately re-prove all bindings
-> start at most once
-> installer child invocation at most once
-> retry gate CLOSED after start
-> terminal evidence
-> full read-only postflight
-> report
-> STOP for independent review
```

If `plugin-rollover-prepare` fails again, the Task-247 repaired capture must preserve the complete bounded Python diagnostic/type/message or exact failing invariant. Do not retry after observing the failure.

## Hard budgets

```text
successful installer task registrations <= 1
installer task starts <= 1
scripts/install.ps1 child invocations <= 1
installer retries after start = 0
manual plugin/lifecycle/Gateway/DB repair = 0
Dashboard/Discord/API semantic sends = 0
semantic retries = 0
recovery replay/resend = 0
production/source/test/workflow edits = 0
release/tag/history mutation = 0
```

Installer-owned writes inside the single authorized invocation are allowed.

## Stop boundary

Hermes must publish:

`docs/operations/coordination/reports/CNX-20260904-248-task247-repaired-candidate-windows-install-over-requalification.md`

Then STOP for independent ChatGPT review. Semantic acceptance remains a separate successor even if Task 248 passes.
