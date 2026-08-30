# CNX-20260830-158 — Windows Install-Over Observability + Recovery Diagnosis Review

Disposition: `ACCEPT`

Reviewer: `ChatGPT self-review (operator-authorized; not independent)`

## Review scope

Review Task 158 as a repository-only TDD repair that adds installer-owned diagnostic boundaries for the real-Windows install-over path after Task 157 ended `BLOCKED` under an external execution ceiling.

This checkpoint is explicitly a **self-review**, not an independent review. It does not accept Phase P and it does not authorize Dashboard semantic delivery testing.

## Evidence reviewed

- Task 158:
  `docs/operations/coordination/tasks/CNX-20260830-158-windows-install-over-observability-recovery-diagnosis.md`
- Task-158 report:
  `docs/operations/coordination/reports/CNX-20260830-158-windows-install-over-observability-recovery-diagnosis.md`
- invalid first test-only attempt:
  `197c7dcee8df933d434283c0cb6d1c3334512b59`
- accepted RED:
  `a124f1d01fe9df59a67376e0686cc69a26a669a0`
- accepted RED Validate:
  `33298614302`
- production GREEN:
  `2e8ff49da2573d87236fa7a004bc156d8c94b880`
- exact-GREEN Validate:
  `33298739915`
- exact-GREEN PS5.1 Acceptance Smoke:
  `33298739927`
- exact-GREEN Windows Installer Pack Smoke:
  `33298739922`

## Findings

### 1. The accepted RED is genuine and behavior-specific

The first test-only attempt is correctly excluded because namespace isolation failed before pytest reached the intended regression.

The corrected RED at `a124f1d01fe9df59a67376e0686cc69a26a669a0` passed namespace isolation and then failed exactly because the production installer lacked the required machine-searchable stage markers and command bracketing.

Windows/Python 3.11 pytest summary:

`2 failed, 499 passed, 3 skipped, 4 subtests passed`

Result: `PASS`.

### 2. Production scope is minimal and diagnostic-only

The GREEN production delta is confined to `scripts/install.ps1` and adds installer-owned START/COMPLETE stage records, UTC timestamps, elapsed milliseconds, and captured child exit codes around the seven selected late substages.

The implementation preserves the pre-existing child commands and success/failure gates. No new retry, timeout, rollback, sleep, kill, package mechanism, dependency, OpenClaw source patch, Dashboard behavior, or transaction-order change was introduced.

Result: `PASS`.

### 3. The diagnostic contract is sufficient for a successor live retry

The production installer now records stable boundaries for:

1. `ticket-db-bootstrap`
2. `plugin-npm-pack`
3. `plugin-rollover-prepare`
4. `plugin-install-local-package`
5. `plugin-disable-post-install`
6. `plugin-rollover-finalize`
7. `owned-runtime-ensure`

A hard interruption can therefore leave an unpaired START record that identifies the active substage instead of producing the ambiguity seen in Task 157.

Result: `PASS`.

### 4. Exact-GREEN verification is sufficient

On exact production SHA `2e8ff49da2573d87236fa7a004bc156d8c94b880`:

- Validate `33298739915`: success;
- all six OS/Python matrix jobs: success;
- package dry-run: success;
- Windows/Python 3.11 pytest: `501 passed, 3 skipped, 4 subtests passed`;
- plugin suite: `51` files / `271` tests passed;
- Windows PowerShell syntax: PASS;
- PS5.1 serializer/root-process checks: PASS;
- evaluation/build: PASS;
- `npm audit --omit=dev`: `0 vulnerabilities`;
- plugin/schema/DB bootstrap/package-content checks: PASS;
- PS5.1 Acceptance Smoke `33298739927`: success;
- Windows Installer Pack Smoke `33298739922`: success.

Result: `PASS`.

### 5. Task-157 root cause remains intentionally unclaimed

The complete live `install-over.txt` from Task 157 was not published into GitHub. Task 158 correctly fixes observability and evidence-retention requirements without claiming which Task-157 subprocess caused the 420-second overrun.

Result: `PASS`.

### 6. Successor evidence requirements are appropriate

The Task-158 report requires a later Hermes retry to preserve the installer PID/start time/process state/exit code, original raw-log path and SHA-256, all stage markers, relevant surrounding errors, and post-state/provenance/health evidence. It also prevents an orchestration timeout from being treated as permission to kill and relaunch the installer.

Result: `PASS`.

### 7. Task fence was preserved

Task 158 performed no live Windows mutation, Dashboard semantic Send, reset, uninstall, reinstall, DB mutation, dependency upgrade, merge/tag/release/promotion, or force push.

Result: `PASS`.

## Disposition

`ACCEPT`

Task 158 is accepted as the repository-side observability prerequisite for a separate Hermes real-Windows diagnostic install-over retry.

Phase P remains pending. No Dashboard semantic Send is authorized by this review.

The next task may authorize only the repaired-candidate Windows install-over/recovery proof needed to resolve Task 157, with durable raw installer evidence retention and the existing hard fence against Dashboard semantic testing.