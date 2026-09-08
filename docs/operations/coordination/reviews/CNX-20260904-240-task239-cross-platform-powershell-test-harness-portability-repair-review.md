# Independent Review — CNX-20260904-240

## Verdict

`ACCEPT_PASS_TEST_HARNESS_PORTABILITY_REPAIRED__TASK239_PRODUCTION_DIAGNOSTIC_REPAIR_VALIDATED__EXACT_CANDIDATE_READY_FOR_BOUNDED_LIVE_INSTALL_REQUALIFICATION`

## Authority reviewed

- Task-240 report head: `9833f3cba2cd5e6c27434164668241d915b8787f`
- Task-240 test-only candidate: `18a51b15768fb3d2196e65f1ef470c34aeef7f36`
- Task-239 production diagnostic repair retained unchanged: `ec29020632091aae3b50149b51303a36fde26310`
- Candidate plugin payload fingerprint: `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`
- Public `v0.9.3` remains immutable at `26ce64a624255278a3a0266ad38746e0e6ed2e31`.

Fresh GitHub repository / Actions evidence is authoritative over report prose.

## Independent findings

### 1. Task 240 is test-only

Commit `18a51b15768fb3d2196e65f1ef470c34aeef7f36` changes only:

`tests/test_task239_rollover_diagnostics.py`

It does not change `scripts/install.ps1`, plugin payload/runtime source, lifecycle code, workflows, release metadata, or published assets.

The portability repair resolves PowerShell capability dynamically:

- Windows: prefer `powershell.exe`, then `pwsh`;
- non-Windows: prefer `pwsh`, then `powershell`;
- when no PowerShell runtime exists, only the runtime-execution helper subtest is skipped;
- static Task-239 contract assertions continue on every platform;
- Windows continues executing the real PowerShell helper.

This directly addresses the Task-239 CI regression where Ubuntu/macOS attempted to execute hard-coded `powershell.exe` and raised `FileNotFoundError`.

### 2. Task-239 production repair remains bounded

The production diagnostic repair remains exactly `ec29020632091aae3b50149b51303a36fde26310`:

- combine `rollover-prepare` stdout/stderr via `2>&1 | Out-String`;
- bound preserved child diagnostic to 4096 characters;
- retain nonzero fail-closed behavior;
- do not change rollover arguments, ownership boundaries, backup/hash/transaction semantics, install order, or retry cardinality.

Task 240 introduced no production mutation on top of it.

### 3. Exact-SHA Actions are terminal GREEN

For exact candidate `18a51b15768fb3d2196e65f1ef470c34aeef7f36`:

- PS5.1 Acceptance Smoke `33832755287` — SUCCESS
- Windows Installer Pack Smoke `33832755300` — SUCCESS
- Validate `33832755313` — SUCCESS, run attempt 2

Validate attempt 1 failed only at macOS `npm audit --omit=dev` due registry/security-endpoint timeout. The corrective failed-only rerun on the same SHA completed SUCCESS. The Task-240 portability regression itself is no longer failing in the matrix.

### 4. Plugin identity remains stable

The test-only Task-240 change does not alter the plugin payload. Accepted candidate fingerprint remains:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

### 5. Zero-live-effect boundary is accepted

Task 240 reports and the repository diff support zero live installer/rollover/plugin/controller/Gateway/Ticket/outbox/recovery/SQLite/semantic/release mutation for this task.

The retained Windows evidence boundary from Tasks 237/238 therefore remains relevant until fresh read-only preflight supersedes it:

```text
controller = passthrough
generation = 39
candidate plugin not installed
live predecessor plugin fingerprint = e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
Gateway healthy
provider = ollama
Delivery READY / pending 0
Recovery READY
SQLite integrity = ok
```

Fresh live evidence must win; this review does not authorize manual normalization.

## Successor authorization

A separate bounded Windows installer-only requalification successor is authorized.

Required successor properties:

1. Bind installer source to a clean detached checkout of exact candidate `18a51b15768fb3d2196e65f1ef470c34aeef7f36`; do not invent unsupported installer parameters.
2. Verify source identity, clean worktree, package/plugin fingerprint, and fresh live preflight before product execution.
3. Permit at most one installer registration/start/invocation.
4. Once installer execution starts, close the installer retry gate permanently for that task.
5. If `plugin-rollover-prepare` fails, preserve the new bounded child diagnostic plus retained backup/transaction inventory and stop; no rerun.
6. If installation succeeds, prove installed candidate fingerprint, rollover/finalization consistency, managed convergence, startup/scheduler health, Gateway/Ollama/Delivery/Recovery/SQLite health, and zero semantic side effects.
7. Do not clean or mutate the retained Task-237 backup token `c6aaf93db7c34f718d01302477a292e1` or older forensic evidence.
8. Dashboard/Discord/API semantic submissions remain zero. Semantic acceptance requires a later separately reviewed task.

## Final disposition

Task 240 is accepted PASS at repository/test-validation scope. The combined exact candidate lineage is ready for one bounded live Windows install-over requalification, not for semantic acceptance yet.
