# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK248_TASK247_REPAIRED_CANDIDATE_WINDOWS_INSTALL_OVER_REQUALIFICATION`  
**Updated:** 2026-09-04 ICT  
**Transport:** GitHub repository / Actions authoritative; Task 248 is a one-shot live installer requalification with non-temp durable evidence capture and zero semantic budget  
**Active task:** `CNX-20260904-248`  
**Parent:** `CNX-20260904-247`  
**Installer failure lineage:** `CNX-20260904-245`, `CNX-20260904-246`  
**Parent umbrella:** `CNX-20260831-188`  
**Disposition:** `TASK247_ACCEPTED_PASS__POWERSHELL51_NATIVE_STDERR_CAPTURE_REPAIRED__LIVE_INSTALLER_REQUALIFICATION_REAUTHORIZED`

## Accepted Task-247 result

Reviewed report HEAD:

`8cbbe2d405477e7b7c91b3fb649582e3a400e893`

Independent review verdict:

`ACCEPT_PASS_POWERSHELL51_NATIVE_STDERR_CAPTURE_REPAIRED__FINAL_ANCESTRY_RED_PROVEN__REPORT_RED_SHA_STALE_NONBLOCKING__LIVE_INSTALLER_REQUALIFICATION_AUTHORIZED_SEPARATELY`

Final-ancestry test-only RED:

`f5f04a7422be05f446d408d48e949473a113dc36`

Accepted repaired executable candidate:

`6c11a5e8f417300835e85441b88e0f37e3897353`

Expected plugin payload fingerprint remains:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Task 247 proved that Windows PowerShell 5.1 with `$ErrorActionPreference='Stop'` could turn native stderr into a terminating `NativeCommandError`, truncating diagnostics and preventing reliable exit-code capture. The repair scopes `ErrorActionPreference='Continue'` only around the native child capture and restores the caller preference in `finally`.

Exact repaired-candidate Actions:

```text
PS5.1 Acceptance Smoke        33884732550 = SUCCESS
Windows Installer Pack Smoke 33884732528 = SUCCESS
Validate                      33884732569 = SUCCESS on attempt 2 / same SHA
```

## Active Task 248

Execute:

`docs/operations/coordination/tasks/CNX-20260904-248-task247-repaired-candidate-windows-install-over-requalification.md`

Task 248 must use a fresh detached exact checkout plus a fresh frozen hardened runner and frozen launch manifest. Execution evidence must be written under the non-temp task archive from the start, not depend on `%TEMP%` for forensic retention.

One-shot cardinality:

```text
successful installer Scheduled Task registrations <= 1
installer starts <= 1
scripts/install.ps1 child invocations <= 1
installer retry after start = 0
```

If `plugin-rollover-prepare` still fails, preserve the full bounded child diagnostic now enabled by Task 247 and STOP. Do not perform a second installer attempt in Task 248.

PASS additionally requires exact installed plugin identity, coherent rollover/finalize evidence if used, managed convergence, healthy Gateway/Ollama/storage/delivery/recovery, SQLite integrity, and zero semantic/direct sends.

## Zero semantic/manual-repair budget

```text
Dashboard semantic submissions = 0
Discord semantic submissions = 0
direct Discord/API sends = 0
semantic retries = 0
manual Ticket/outbox/recovery/SQLite writes = 0
manual plugin/manifest/lifecycle/Gateway repair = 0
manual provider/model substitution = 0
process termination as repair = 0
production/source/test/workflow edits = 0
release/tag/history mutation = 0
```

## Stop boundary

Hermes must publish:

`docs/operations/coordination/reports/CNX-20260904-248-task247-repaired-candidate-windows-install-over-requalification.md`

Then stop for independent ChatGPT review. A Dashboard semantic acceptance turn remains unauthorized until Task 248 passes and is independently accepted.
