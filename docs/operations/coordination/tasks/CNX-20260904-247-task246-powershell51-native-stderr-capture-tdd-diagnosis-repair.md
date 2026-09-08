# CNX-20260904-247 — PowerShell 5.1 Native-Stderr Capture TDD Diagnosis / Repair

## Status
`READY_FOR_HERMES`

## Parentage
- Parent forensic task: `CNX-20260904-246`
- Parent installer failure: `CNX-20260904-245`
- Prior diagnostic repair: `CNX-20260904-239`
- Candidate-validation parent: `CNX-20260904-240`
- Parent umbrella: `CNX-20260831-188`

Reviewed Task-246 report HEAD: `18ec3763bdc8c5a6ffdd8815d863f59447e5e7f7`

Independent review verdict:
`ACCEPT_BLOCKED_EXACT_EXCEPTION_UNPROVEN__TASK245_EVIDENCE_PRESERVED_BYTE_IDENTICALLY__POWERSHELL51_NATIVE_STDERR_CAPTURE_HYPOTHESIS_REQUIRES_TDD_PROOF`

## Objective
Prove or reject whether the current Windows PowerShell 5.1 capture boundary loses the full native-child diagnostic when `$ErrorActionPreference='Stop'` and stderr is merged with `2>&1`.

If and only if a meaningful test-only RED reproduces the Task-245-style truncation, make the smallest production repair that preserves the full bounded child diagnostic, exact child exit code, fail-closed behavior, and exact restoration of the caller error preference.

This task is repository/test work only. No live installer execution is authorized.

## Fresh authority gate
Before work:
1. fetch the branch fresh;
2. read `ACTIVE.md`, `STATUS.md`, this task, Task-246 report and review;
3. confirm no unexplained product/source/test/workflow drift;
4. use GitHub/Actions as authority.

Accepted executable predecessor for the observed behavior: `18a51b15768fb3d2196e65f1ef470c34aeef7f36`.
Expected plugin payload fingerprint remains `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`.

## Accepted facts
Do not reopen without contradictory evidence:
- Task 245 used exact source/runner/manifest binding.
- installer child ran once and stopped at `plugin-rollover-prepare` with exit 1;
- no retry occurred;
- Task 246 preserved 34/34 Task-245 artifacts byte-identically outside Temp;
- complete retained stderr contains only the first Python traceback line plus Windows PowerShell `NativeCommandError` metadata;
- Python exception class/message/final traceback line are absent;
- exact Python exception is therefore unproven;
- no live repair or semantic action is authorized here.

## Phase A — test-only RED
Create a test-only commit before any production edit.

The test must execute actual Windows PowerShell 5.1 (`powershell.exe`) with `$ErrorActionPreference='Stop'` and a harmless disposable Python/native child that:
- emits one stdout marker;
- emits at least three stderr lines including a traceback header, `TASK247_FRAME_SENTINEL`, and `RuntimeError: TASK247_FINAL_SENTINEL`;
- exits with deterministic nonzero code 23.

Exercise the current installer-relevant stderr-capture semantics. The desired contract is:
- the capture boundary completes deterministically;
- child exit code is exactly 23;
- captured diagnostic includes the traceback header and both sentinels;
- surrounding `$ErrorActionPreference` is still `Stop` afterward;
- failure is classified from child exit code, not accidental PowerShell stream termination.

Also include a control child that writes stderr but exits 0. Desired behavior: exit 0 remains success; stderr alone must not create a false failure; error preference must be restored.

Record the exact RED commit SHA, Windows PowerShell version, command, observed output, and failed assertion. RED must not be caused by quoting/path/runtime availability defects.

If the current production behavior already satisfies the full contract, classify `BLOCKED_HYPOTHESIS_REJECTED`, make no production edit, publish the report, and stop.

## Phase B — minimal repair only after meaningful RED
If the RED reproduces the mechanism, repair only the owning native-command capture boundary used by `plugin-rollover-prepare`.

The repair must:
- retain complete stdout/stderr needed for bounded diagnostics;
- retain exact child exit code;
- keep exit 0 successful even if stderr contains text;
- keep nonzero exit fail-closed;
- restore caller `$ErrorActionPreference` exactly on every path;
- preserve the existing 4096-character bounded diagnostic contract;
- preserve stage markers, exact Python arguments, transaction ordering, backup semantics, and plugin lifecycle ordering;
- avoid global weakening of error handling;
- add no retry.

Do not change `namespace_ownership.py`, plugin payload behavior, ownership rules, rollover schema, provider/model/runtime behavior, or semantic delivery behavior.

## Phase C — GREEN
After the minimal repair:
1. rerun the exact Windows PowerShell 5.1 RED;
2. prove the exit-23 child preserves the complete sentinels and exact exit code;
3. prove the stderr+exit0 control stays successful;
4. prove error preference restoration;
5. run Task-239/240 diagnostic tests;
6. run relevant installer/namespace tests;
7. run full Python tests;
8. run plugin validation/tests and production npm audit where applicable;
9. inspect minimal production diff;
10. require exact-SHA GitHub Actions GREEN: `Validate`, `Windows Installer Pack Smoke`, `PS5.1 Acceptance Smoke`.

If plugin payload fingerprint changes, stop as unexpected drift.

## Zero live-effect budget
- live `scripts/install.ps1` invocations: 0
- installer task registrations/starts: 0
- live rollover/plugin/lifecycle/DB mutations: 0
- Dashboard/Discord/API semantic sends: 0
- recovery replay/resend: 0
- historical evidence cleanup: 0
- release/tag/history mutation: 0

Synthetic disposable PowerShell/Python test processes are allowed only for the isolated regression and must not invoke OpenClaw/CogentNexus live commands.

## Required report
Publish `docs/operations/coordination/reports/CNX-20260904-247-task246-powershell51-native-stderr-capture-tdd-diagnosis-repair.md` with RED SHA/evidence, hypothesis result, repair SHA/diff if any, tests, exact-SHA Actions, plugin fingerprint, zero-live-effect ledger, and final disposition.

Allowed dispositions:
- `PASS_POWERSHELL51_NATIVE_STDERR_CAPTURE_REPAIRED_GREEN`
- `BLOCKED_HYPOTHESIS_REJECTED`
- `BLOCKED_RED_NOT_MEANINGFUL`
- `FAIL_REPAIR_NOT_GREEN`
- `BLOCKED_CI`
- `BLOCKED_EVIDENCE`

Then STOP for independent ChatGPT review. Even a GREEN result does not authorize a live installer retry or semantic acceptance turn.
