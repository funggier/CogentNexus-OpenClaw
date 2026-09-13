# CNX-20260913-318 — v0.9.5 Acceptance Blocked by Windows PowerShell npm stderr Boundary

## Result

```text
Task: CNX-20260913-318
Authorized candidate: 2a1be3b5c2e95664da97f2aea103a57a4947fd9d
Installation: FAIL
Provider Switch: INDETERMINATE
Idle Quiescence: INDETERMINATE
Controlled Wake: INDETERMINATE
Finalization: BLOCKED
PR #38: OPEN / UNMODIFIED
Merge: None
Tag: None
Release: Not published
```

## Defect

The exact candidate installation stopped before installation/mutation completed. On Windows PowerShell 5.1, `scripts/install.ps1` invoked `npm ci` directly while `$ErrorActionPreference = "Stop"`. npm emitted warning diagnostics on stderr while returning exit code 0; PowerShell promoted the native stderr stream to `NativeCommandError` before the installer could inspect `$LASTEXITCODE`.

This is a native-command boundary defect in the installer and is distinct from the earlier canonical-controller-state defect.

## Repair and requalification

```text
RED commit:
3b42bb2fb6ff6a30f094ea3e901470fa03f1cc14
  test: cover installer npm stderr boundary

New candidate:
345b92b4b1eac5cf8c3813de96565d6ca8b5f927
  fix: preserve npm stderr diagnostics in installer
```

Requalification reported for the new candidate:

```text
Focused tests: 5 passed
Python: 670 passed, 5 skipped, 38 subtests passed
npm: 337 passed
Plugin validation/build/package: PASS
```

Remote candidate branch HEAD is reported at the exact new candidate SHA and the worktree is reported clean.

## Evidence

Install transcript:
`C:\Users\CDQ-P\AppData\Local\Temp\cnx318-20260913T045720Z\install-transcript.log`

Transcript SHA-256:
`32ddecab34db076c6b7882c464e52d5344ebf2d3912254bcf5312f4cad117a2f`

No `install-result.json` was produced because PowerShell terminated the runner before terminal result serialization. Therefore installer success is not claimed and no retry was performed under task 318.

## External runtime state noted at stop

The runtime/model state also reported that `ollama/qwen3.5:9b` had been removed while several sessions remained pinned to that model. No attempt was made to restore or mutate that provider/model state because doing so would exceed the stop-gate scope after the installer defect and would be a separate provider mutation.

## Stop decision

Task 318 is closed at the defect boundary. No Provider Switch, Idle Quiescence, or Controlled Wake result can be inferred from the failed installation. A successor authority is required before any retry against the new candidate `345b92b4b1eac5cf8c3813de96565d6ca8b5f927`.
