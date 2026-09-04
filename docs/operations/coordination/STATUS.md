# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK247_POWERSHELL51_NATIVE_STDERR_CAPTURE_TDD_DIAGNOSIS_REPAIR`  
**Updated:** 2026-09-04 ICT  
**Transport:** GitHub repository / Actions authoritative; Task 247 is repository/test-only and proves or rejects the Windows PowerShell 5.1 native-stderr capture hypothesis before any repair  
**Active task:** `CNX-20260904-247`  
**Parent:** `CNX-20260904-246`  
**Parent installer failure:** `CNX-20260904-245`  
**Prior diagnostic repair:** `CNX-20260904-239`  
**Parent umbrella:** `CNX-20260831-188`  
**Disposition:** `TASK246_ACCEPTED_BLOCKED__EVIDENCE_PRESERVED__POWERSHELL51_NATIVE_STDERR_CAPTURE_HYPOTHESIS_REQUIRES_TDD_PROOF`

## Accepted Task-246 result

Reviewed report HEAD:

`18ec3763bdc8c5a6ffdd8815d863f59447e5e7f7`

Independent review verdict:

`ACCEPT_BLOCKED_EXACT_EXCEPTION_UNPROVEN__TASK245_EVIDENCE_PRESERVED_BYTE_IDENTICALLY__POWERSHELL51_NATIVE_STDERR_CAPTURE_HYPOTHESIS_REQUIRES_TDD_PROOF`

Task 246 successfully preserved the Task-245 temporary evidence before cleanup risk:

```text
artifacts copied = 34
missing = 0
source/destination SHA-256 equality = 34/34
```

The complete retained stderr proves the failing child crossed the `plugin-rollover-prepare` boundary but contains only the first Python traceback line followed by Windows PowerShell `NativeCommandError` metadata. The Python exception class/message/final traceback line are absent; exact invariant remains unproven.

No new Task-245 rollover transaction was persisted. Workspace install/skill backup and external generation-rollover backup domains remain distinct.

Task-246 report-head Actions are GREEN:

```text
PS5.1 Acceptance Smoke        33881077771 = SUCCESS
Windows Installer Pack Smoke 33881077746 = SUCCESS
Validate                      33881077796 = SUCCESS
```

## Why Task 247 is required

The accepted executable candidate uses global:

```powershell
$ErrorActionPreference = "Stop"
```

while the Task-239 rollover diagnostic capture merges native stderr with `2>&1 | Out-String`.

Task 245 observed a real Windows PowerShell 5.1 `NativeCommandError` wrapper and retained only the first traceback line. Existing Task-239/240 tests do not execute that exact Windows PowerShell 5.1 native-command stderr boundary with a multi-line failing child.

This is a concrete coverage gap and a plausible mechanism, but it must be reproduced before any production edit.

## Active Task 247

Execute:

`docs/operations/coordination/tasks/CNX-20260904-247-task246-powershell51-native-stderr-capture-tdd-diagnosis-repair.md`

Required flow:

```text
fresh authority
-> test-only RED on actual Windows PowerShell 5.1
-> harmless multi-line stderr child + deterministic exit code
-> prove/reject NativeCommandError/truncation hypothesis
-> hypothesis rejected => no production edit, report, STOP
-> meaningful RED => minimal owning-boundary repair
-> RED -> GREEN
-> targeted/full validation
-> exact-SHA Actions GREEN
-> report
-> STOP
```

A static source assertion or helper-only test is insufficient; the test must execute the native stderr boundary under `$ErrorActionPreference='Stop'`.

## Zero live-effect budget

```text
live scripts/install.ps1 invocations = 0
installer task registrations/starts = 0
live rollover/plugin/controller/Gateway/DB mutation = 0
Dashboard/Discord/API semantic sends = 0
recovery replay/resend = 0
historical evidence cleanup = 0
release/tag/history mutation = 0
```

Synthetic disposable PowerShell/Python regression processes are allowed only for isolated test evidence and must not invoke live OpenClaw/CogentNexus commands.

## Expected identity

Accepted executable predecessor:

`18a51b15768fb3d2196e65f1ef470c34aeef7f36`

Expected plugin payload fingerprint:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

## Stop boundary

Hermes must publish:

`docs/operations/coordination/reports/CNX-20260904-247-task246-powershell51-native-stderr-capture-tdd-diagnosis-repair.md`

Then stop for independent ChatGPT review. Live installer and semantic successors remain unauthorized until that review.
