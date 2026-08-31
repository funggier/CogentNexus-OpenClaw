# CNX-20260830-158 Report — Windows Install-Over Observability + Recovery Diagnosis

Disposition: **PASS**

Task:

`docs/operations/coordination/tasks/CNX-20260830-158-windows-install-over-observability-recovery-diagnosis.md`

Branch:

`agent/v0.9.3-full-stabilization`

## Trigger and scope

Task 157 was durably reviewed `BLOCKED` after the single real-Windows repaired-candidate install-over crossed the native handoff boundary but exceeded the executor's 420-second observation window without a proven installer completion or exit status. The repaired candidate was not proven installed and Dashboard semantic reacceptance therefore remained blocked.

Task 158 was repository-only. Its purpose was to improve install-over diagnosability under TDD without changing installation, rollback, rollover, ownership, runtime, or Dashboard semantics.

## Task-157 log limitation carried into this task

The complete Task-157 live installer capture was recorded on the Windows executor at:

`C:/Users/CDQ-P/AppData/Local/Temp/cnx157-install-over-20260830T0610/install-over.txt`

but that raw file was not published into GitHub coordination evidence. ChatGPT therefore reviewed the Task-157 durable report/excerpts and source path, **not the complete raw live installer log**. This report does not claim a Task-157 root cause.

This limitation is distinct from Task-158 CI evidence: GitHub Actions raw RED/GREEN job logs were directly inspected during Task 158.

## Repository diagnosis

Before Task 158, `scripts/install.ps1` invoked critical late external substages and inspected `$LASTEXITCODE` only after those commands returned. It did not own a stable machine-searchable stage START / COMPLETE / elapsed-time record around all of those boundaries.

Consequently, when an external executor terminated or stopped observing the installer while a child command was still active, durable installer output could not reliably identify the active late substage from an installer-owned marker alone.

The late substages selected for the minimum diagnostic contract were:

1. `ticket-db-bootstrap`
2. `plugin-npm-pack`
3. `plugin-rollover-prepare`
4. `plugin-install-local-package`
5. `plugin-disable-post-install`
6. `plugin-rollover-finalize`
7. `owned-runtime-ensure`

## TDD — invalid first RED attempt

Initial test-only commit:

`197c7dcee8df933d434283c0cb6d1c3334512b59`

Message:

`test: expose Windows install-over observability gap`

Validate run:

`33298514981`

This first attempt used a marker spelling that violated the repository namespace-isolation gate. The workflow therefore failed before reaching the intended pytest regression. It is **not** counted as valid RED evidence and no production change was made from it.

## TDD — corrected RED

Corrected test-only commit:

`a124f1d01fe9df59a67376e0686cc69a26a669a0`

Message:

`test: repair Task 158 RED namespace fixture`

Regression file:

`tests/test_installer_observability_contract.py`

Validate run:

`33298614302`

Directly inspected Windows/Python 3.11 raw job:

`99222477547`

The namespace-isolation gate passed and pytest then failed for the intended production gap:

- `test_installer_diagnostic_record_format_is_machine_searchable` failed because `CNXCLAW_INSTALL_STAGE_START` was absent;
- `test_critical_late_install_over_substages_are_bracketed` failed because `ticket-db-bootstrap` had no diagnostic START bracket.

Exact pytest summary:

`2 failed, 499 passed, 3 skipped, 4 subtests passed in 86.88s`

This is the accepted RED checkpoint.

## GREEN — minimal production observability change

Production repair commit:

`2e8ff49da2573d87236fa7a004bc156d8c94b880`

Message:

`fix: add Windows installer stage diagnostics`

Production file changed:

`scripts/install.ps1`

Exact corrected-RED-to-GREEN comparison:

- files changed: 1
- additions: 51
- deletions: 8
- changed production path: `scripts/install.ps1` only

The installer now owns two stable records:

- `CNXCLAW_INSTALL_STAGE_START stage=<id> utc=<ISO-8601 UTC>`
- `CNXCLAW_INSTALL_STAGE_COMPLETE stage=<id> utc=<ISO-8601 UTC> elapsed_ms=<milliseconds> exit_code=<child-exit>`

For each instrumented child command, the implementation:

1. emits START immediately before the existing command;
2. executes the existing command unchanged;
3. snapshots `$LASTEXITCODE` immediately after return;
4. emits COMPLETE with elapsed milliseconds and the captured code;
5. applies the pre-existing success/failure gate to the captured code.

A hard external termination can therefore leave a final START without COMPLETE, identifying the substage active at termination.

## Semantic-preservation review

The Task-158 production delta does **not** add or change:

- retries;
- timeouts;
- sleeps;
- process termination;
- `--force` behavior;
- plugin install/replacement ordering;
- native handoff / `passthrough` behavior;
- rollover prepare/finalize semantics;
- fresh-install rollback semantics;
- upgrade rollback semantics;
- ownership creation/verification semantics;
- runtime-provisioning semantics;
- dependency versions;
- OpenClaw source;
- Dashboard delivery/runtime behavior.

The `$LASTEXITCODE` snapshot was moved into named variables only where required to preserve the child command's exact return value across the diagnostic helper call.

## GREEN verification

All verification below was executed against exact production SHA:

`2e8ff49da2573d87236fa7a004bc156d8c94b880`

### Validate

Run:

`33298739915`

Final result:

`completed / success`

Windows/Python 3.11 raw job inspected directly:

`99222813330`

Key results:

- namespace isolation: PASS
- baseline consistency: PASS
- repository validation: PASS
- Cogent self-test: PASS
- runtime self-test: PASS
- workflow self-test: PASS
- pytest: `501 passed, 3 skipped, 4 subtests passed in 109.39s`
- Windows PowerShell syntax validation: PASS
- PowerShell 5.1 evidence serializer self-test: PASS
- PowerShell 5.1 root-process exit-code self-test: PASS
- exact numeric root-process exit capture: PASS
- plugin test suite: `51 passed` test files / `271 passed` tests
- predecessor `v091-dashboard-verified-delivery.test.ts`: 11/11 PASS
- Task-155 regression `v154-dashboard-public-hook-fallback.test.ts`: 2/2 PASS
- evaluation/build: PASS (`passed: true`)
- `npm audit --omit=dev`: `found 0 vulnerabilities`
- plugin build/schema verification: PASS
- ticket DB bootstrap validation: PASS
- package-content verification: PASS

All six Validate matrix jobs (Windows/Linux/macOS × Python 3.11/3.14) completed successfully, and the package dry-run job succeeded.

### PS5.1 Acceptance Smoke

Run:

`33298739927`

Result:

`completed / success`

### Windows Installer Pack Smoke

Run:

`33298739922`

Result:

`completed / success`

## Evidence-retention contract for successor live retry

A successor Windows task must not repeat Task 157's evidence gap. It must durably preserve the actual installer evidence needed for review.

At minimum the later live report must include or publish a faithful text evidence artifact containing:

- original local raw-log path;
- SHA-256 of the original raw log after the installer exits or is proven terminated;
- installer command line;
- installer PID and start UTC;
- final installer process state;
- exact exit code when available;
- every `CNXCLAW_INSTALL_STAGE_START` and `CNXCLAW_INSTALL_STAGE_COMPLETE` record;
- surrounding output for any stage that fails or has START without COMPLETE;
- relevant first/last installer output lines and all relevant errors;
- post-state/provenance/health evidence.

If the full raw log is reasonably sized, publish a faithful complete text copy. If it is too large, preserve the original locally, hash it, and publish all stage markers plus the complete relevant error/active-stage window without silently omitting relevant failures.

The successor must also avoid treating an orchestration-call timeout as permission to kill and relaunch the installer. One installer process must remain uniquely observable until it exits or is explicitly proven terminated.

## Live-action fence

Task 158 performed repository/source/test/docs/CI work only.

Task-158 live Windows mutations: `0`

Task-158 Dashboard semantic Sends: `0`

Task-158 Dashboard semantic click/focus/type/paste operations: `0`

Task-158 reset/uninstall/reinstall actions: `0`

Task-158 runtime/database/semantic mutations: `0`

Task-158 dependency upgrades: `0`

Task-158 OpenClaw source patches: `0`

Task-158 merge/tag/release/promotion actions: `0`

Task-158 force pushes: `0`

## Acceptance checklist

1. Correct RED demonstrated against pre-fix installer: **PASS**
2. Minimal observability change passes regression: **PASS**
3. Existing installer/transaction/ownership regression set remains green: **PASS**
4. Relevant Windows installer/validation workflows green on exact repair SHA: **PASS**
5. Diff review confirms diagnostic-only semantic preservation: **PASS**
6. Task-158 report committed: **PASS by this report publication**
7. Explicit non-independent ChatGPT self-review: **PENDING until separate review commit**

## Disposition

Repository implementation/evidence portion of Task 158: **PASS**.

Task 158 becomes fully ACCEPT only after the separate explicit ChatGPT self-review is committed.

Phase P remains pending. No Dashboard semantic Send is authorized.

Expected next checkpoint after Task-158 self-review ACCEPT: a separate Hermes real-Windows repaired-candidate install-over diagnostic retry with durable raw evidence retention.
