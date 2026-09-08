# CNX-20260904-247 — Independent Review

## Verdict

`ACCEPT_PASS_POWERSHELL51_NATIVE_STDERR_CAPTURE_REPAIRED__FINAL_ANCESTRY_RED_PROVEN__REPORT_RED_SHA_STALE_NONBLOCKING__LIVE_INSTALLER_REQUALIFICATION_AUTHORIZED_SEPARATELY`

## Reviewed authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Task-247 report HEAD: `8cbbe2d405477e7b7c91b3fb649582e3a400e893`
- Accepted repaired executable candidate: `6c11a5e8f417300835e85441b88e0f37e3897353`
- Candidate plugin fingerprint remains: `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`
- Public `v0.9.3` tag remains immutable at `26ce64a624255278a3a0266ad38746e0e6ed2e31`.

## Independent findings

### 1. The Task-246 hypothesis was reproduced on real Windows PowerShell 5.1

Task 247 used a synthetic native child under `$ErrorActionPreference = 'Stop'` and reproduced the Task-245 failure shape: native stderr was promoted to a terminating `NativeCommandError`, only the first traceback line survived, the intended child exit code was not recoverable through the old capture shape, and an stderr-writing child that otherwise exited zero was also misclassified.

This is a meaningful RED at the installer-owning boundary, not a string-only contract test.

### 2. Final-ancestry RED is test-only

The report names pre-rebase RED `c3732628a7336daf7b0b6411be17e4ad6f6fa8ba`; that object is no longer reachable through GitHub after the reported rebase. The final branch ancestry contains the equivalent RED at:

`f5f04a7422be05f446d408d48e949473a113dc36`

That commit changes only:

`tests/test_task247_powershell51_native_stderr.py`

The production repair `6c11a5e8...` is the direct child of this final-ancestry RED. The stale pre-rebase SHA in the report is therefore a reporting/provenance gap, not a TDD-integrity failure.

### 3. Production repair is bounded to the owning capture boundary

`scripts/install.ps1` adds `Invoke-NativeInstallerDiagnostic`, which temporarily changes `$ErrorActionPreference` to `Continue` only while invoking the native child, captures merged stdout/stderr, snapshots `$LASTEXITCODE`, restores the caller preference in `finally`, and returns output plus exit code.

Only the `plugin-rollover-prepare` native capture call site uses the helper. Rollover transaction ordering, backup semantics, namespace ownership logic, expected fingerprint checks, plugin install/finalize ordering, and fail-closed nonzero behavior are unchanged.

Associated test edits only adapt existing observability assertions to the new helper and validate real Windows PowerShell 5.1 behavior.

### 4. GREEN evidence is sufficient

Reported local validation includes focused Task-247/installer tests GREEN, full Python GREEN, PowerShell parser GREEN, plugin validation GREEN, mixed-plugin verification GREEN, ticket DB bootstrap GREEN, and unchanged plugin fingerprint.

Exact repaired SHA Actions are terminal GREEN:

- PS5.1 Acceptance Smoke `33884732550` — SUCCESS
- Windows Installer Pack Smoke `33884732528` — SUCCESS
- Validate `33884732569` — SUCCESS on attempt 2, same SHA

Validate attempt 1 had unrelated timing/test instability and was rerun without any source mutation. This does not invalidate the repaired SHA.

### 5. Live effect fence was preserved

Task 247 performed no live installer invocation, Scheduled Task registration/start, rollover prepare/finalize, plugin/runtime/controller/Gateway/DB mutation, semantic send, replay/resend, process termination, or release/tag/history mutation.

## Disposition

Task 247 is accepted as repository/TDD PASS. The next step may be a separate one-shot Windows install-over requalification using exact candidate `6c11a5e8...`.

The successor must not interpret the Task-247 repair as proof that the underlying Python rollover preparation itself is healthy. If `plugin-rollover-prepare` still returns nonzero, the repaired installer must preserve the complete bounded child diagnostic (including traceback type/message or equivalent exact failing invariant), then stop with zero execution retry.

Semantic acceptance remains out of scope until installer requalification and independent post-install review pass.
