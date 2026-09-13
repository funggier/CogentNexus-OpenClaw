# CNX-20260913-319 — v0.9.5 Post-Install Defect

## Result

```text
Installation: PASS
Post-install system check: FAIL
Provider Switch: INDETERMINATE
Idle Quiescence: INDETERMINATE
Controlled Wake: INDETERMINATE
Finalization: BLOCKED
```

## Authorized Candidate

```text
345b92b4b1eac5cf8c3813de96565d6ca8b5f927
```

## Installation Evidence

```text
Installed fingerprint: fdf08394bbb9d97920158c4f17e1bf6922cba5ba3527311af563a0e4408418db
Source fingerprint:    fdf08394bbb9d97920158c4f17e1bf6922cba5ba3527311af563a0e4408418db
Gateway:               Healthy
Plugin:                Enabled, v0.9.5
Generation:            97
Provider ownership:    openclaw
```

Evidence:

```text
Install transcript:
C:\Users\CDQ-P\AppData\Local\Temp\cnx319-20260913T053817Z\install-transcript.log
SHA-256: 8270f4dbad003d7f24473daa10b5975c8cbeebbd36c1a0c458776724d758ff78

Install result:
C:\Users\CDQ-P\AppData\Local\Temp\cnx319-20260913T053817Z\install-result.json
SHA-256: 256cd4ef86867295508116fe9c8e36473b1fa77812b0b62847d16821e3c68a7f
```

## Defect

`cnxclaw status` correctly derives the canonical controller state:

```text
cnxMode=active -> mode=managed
```

`cnxclaw check system` still reads only the legacy `mode` field from the canonical controller and therefore reports:

```text
Host controller state: FAIL
invalid Host mode: None
```

No manual controller or runtime mutation was performed.

## Root Cause / Repair

Root cause: the system-check path had not adopted the canonical v0.9.5 controller state boundary even though the status path had.

TDD repair:

```text
b53cea15  test: cover canonical v0.9.5 system check state
fc3f4bc0  fix: accept canonical state in system checks
```

The minimal repair derives the legacy view in memory only:

```text
active      -> managed
disabled    -> passthrough
maintenance -> maintenance
```

## Requalification Reported

```text
Focused:                         4 passed
Python:                          672 passed, 5 skipped, 38 subtests passed
npm:                             337 passed
Plugin validation/build/package: PASS
Local HEAD:                      fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23
Remote branch HEAD:              fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23
Worktree:                         clean
```

These results must be independently verified against the exact successor candidate before live acceptance resumes.

## Release State

```text
PR #38:             OPEN / unchanged
Provider Switch:    INDETERMINATE
Idle Quiescence:    INDETERMINATE
Controlled Wake:    INDETERMINATE
Finalization:       BLOCKED
Merge:              None
Tag:                None
Release:            Not published
```

Task 319 stops at the hard fence. A successor authority is required before install-over or live acceptance continues.
