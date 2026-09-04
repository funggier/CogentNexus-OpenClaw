# CNX-20260904-247 — PowerShell 5.1 Native-Stderr Capture TDD Diagnosis / Repair

## Disposition

`PASS_POWERSHELL51_NATIVE_STDERR_CAPTURE_REPAIRED_GREEN`

A real Windows PowerShell 5.1 reproduction proved the Task-245-style native stderr termination/truncation mechanism. The smallest owning-boundary repair was applied to `scripts/install.ps1`; the regression is now GREEN. No live installer or product operation was performed.

## Authority and lineage

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Fresh authority before report publication: `6c11a5e8f417300835e85441b88e0f37e3897353`
- Task: `CNX-20260904-247`
- Parent: `CNX-20260904-246`
- Accepted exact candidate: `18a51b15768fb3d2196e65f1ef470c34aeef7f36`
- Expected plugin fingerprint: `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

The remote `ACTIVE.md` and `STATUS.md` were re-read before execution and before publication. No Task-247 report existed before this publication.

## Phase A — meaningful RED

Test file initially added in the test-only RED commit:

```text
tests/test_task247_powershell51_native_stderr.py
```

RED commit before the production repair:

```text
c3732628a7336daf7b0b6411be17e4ad6f6fa8ba
```

The test executed actual:

```text
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
```

with:

```powershell
$ErrorActionPreference = 'Stop'
$captured = (& python.exe -u <disposable-child.py> 2>&1 | Out-String)
$childExit = $LASTEXITCODE
```

The disposable nonzero child emitted stdout plus these stderr lines:

```text
Traceback (most recent call last):
TASK247_FRAME_SENTINEL
RuntimeError: TASK247_FINAL_SENTINEL
```

and exited `23`. The control child emitted stderr and exited `0`.

Observed RED:

- nonzero child: PowerShell process exited `1` before returning the capture result;
- output retained only the first native stderr line and `NativeCommandError` metadata;
- exact child exit code `23` was not returned;
- stderr-only exit-0 control was incorrectly terminated as failure;
- failure was reproducible on real Windows PowerShell 5.1 and was not caused by quoting, path, or runtime availability.

This is the same boundary behavior seen in Task 245: native stderr became a terminating `NativeCommandError` while the caller had `ErrorActionPreference = Stop`.

## Minimal repair

Production file changed:

```text
scripts/install.ps1
```

Repair commit after rebase:

```text
6c11a5e8f417300835e85441b88e0f37e3897353
```

Production file SHA-256:

```text
c0779d9bae69d850a44073134e7799a48a1856935b09aae1ae8c7da9f57e0629
```

The repair adds `Invoke-NativeInstallerDiagnostic`, which:

1. saves the caller's `$ErrorActionPreference`;
2. sets it to `Continue` only around the native command capture;
3. merges native stdout/stderr with `2>&1 | Out-String`;
4. snapshots `$LASTEXITCODE` immediately;
5. restores the saved preference in `finally` on every path;
6. returns output and exact exit code as an object.

Only the `plugin-rollover-prepare` capture call site was changed to use the helper. Existing bounded 4096-character diagnostics, stage markers, fail-closed nonzero handling, exact Python arguments, transaction ordering, backup semantics, ownership rules, and plugin lifecycle ordering were preserved. No global error-handling weakening was introduced.

## Phase C — GREEN

Focused validation:

```text
15 passed in 1.81s
```

This included:

- real PS5.1 child exit `23` with complete traceback header and both sentinels;
- exact child exit code preservation;
- stderr plus child exit `0` remains success;
- `$ErrorActionPreference` remains/restores to `Stop`;
- Task-239 bounded diagnostic tests;
- installer observability contract;
- installer transaction wiring.

Full Python validation with repository root on `PYTHONPATH`:

```text
PYTHONPATH=. pytest -q
510 passed, 5 skipped, 4 subtests passed in 74.05s
```

A plain `pytest` invocation failed during collection because its launcher did not place the repository root on `sys.path` (`ModuleNotFoundError: No module named 'scripts'`). `python -m pytest` used Hermes' Python environment, which has no pytest installed. The canonical executable pytest run with `PYTHONPATH=.` passed the full suite; no package was installed to hide the environment issue.

Other validation:

```text
PowerShell parser: PASS
git diff --check: PASS
npm run plugin:validate: PASS
mixed-plugin artifact verification: PASS (45 config properties, 5 tools)
ticket DB bootstrap: PASS (9 required tables + v095 registration fence)
packedFileCount: 196
plugin fingerprint: 1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f
```

`npm audit --audit-level=high` reported `5 vulnerabilities (1 moderate, 4 high)`. The suggested `npm audit fix --force` would install OpenClaw `2026.9.1` outside the stated dependency range, so no dependency remediation was performed. This is recorded as a non-blocking validation warning, not attributed to the repair.

## Exact-SHA GitHub Actions

All runs below target exact HEAD `6c11a5e8f417300835e85441b88e0f37e3897353`:

- `PS5.1 Acceptance Smoke` run `33884732550`: `completed / success`
- `Windows Installer Pack Smoke` run `33884732528`: `completed / success`
- `Validate` first run `33884732569`: `failure`
- `Validate` corrective rerun `33884732569`: `completed / success`

The first Validate failure was preserved as a CI/test timing issue: five unrelated Vitest tests timed out or hit a lease-timing assertion on Windows/Python 3.14. The exact-SHA failed run was rerun once; the same run ID completed successfully. No source change occurred between the failed and successful Validate attempts.

## Payload and live-effect boundaries

The plugin fingerprint remained exactly:

```text
1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f
```

Task 247 performed no live installer invocation, no Scheduled Task registration/start, no rollover operation, no plugin installation, no controller/Gateway/provider/model/DB mutation, no semantic send, no recovery replay, no process termination, and no release/tag/history mutation.

Effect ledger:

```text
live scripts/install.ps1 invocations = 0
installer Scheduled Task registrations/starts = 0
live rollover prepare/finalize = 0
live plugin/runtime/controller/Gateway/DB mutation = 0
Dashboard/Discord/API semantic sends = 0
recovery replay/resend = 0
historical evidence cleanup = 0
release/tag/history mutation = 0
```

Synthetic disposable PowerShell/Python child processes were used only by the isolated tests.

## Conclusion and stop gate

The PowerShell 5.1 native stderr hypothesis is proven. The owning capture boundary now preserves the complete bounded diagnostic and exact child exit code while keeping stderr-only exit-0 success and restoring the caller error preference.

This GREEN repository repair does **not** authorize a live installer retry or semantic acceptance. Those require separate successor authority.

STOP for independent ChatGPT review.
