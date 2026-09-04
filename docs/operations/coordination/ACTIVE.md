# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK247_POWERSHELL51_NATIVE_STDERR_CAPTURE_TDD_DIAGNOSIS_REPAIR`
Current disposition: `TASK246_ACCEPTED_BLOCKED__EVIDENCE_PRESERVED__POWERSHELL51_NATIVE_STDERR_CAPTURE_HYPOTHESIS_REQUIRES_TDD_PROOF`
Task ID: `CNX-20260904-247`
Parent task: `CNX-20260904-246`
Parent installer failure: `CNX-20260904-245`
Prior diagnostic repair: `CNX-20260904-239`
Candidate-validation parent: `CNX-20260904-240`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-04 ICT
Executor: Hermes / authenticated Windows operator
Coordinator / independent reviewer: ChatGPT

## Accepted Task-246 result

Independent review verdict:

`ACCEPT_BLOCKED_EXACT_EXCEPTION_UNPROVEN__TASK245_EVIDENCE_PRESERVED_BYTE_IDENTICALLY__POWERSHELL51_NATIVE_STDERR_CAPTURE_HYPOTHESIS_REQUIRES_TDD_PROOF`

Reviewed Task-246 report HEAD:

`18ec3763bdc8c5a6ffdd8815d863f59447e5e7f7`

Accepted facts:

```text
Task-245 temp evidence preserved outside Temp = 34/34 byte-identical
Task-245 installer child = exact candidate / one invocation
terminal stage = plugin-rollover-prepare
child exit = 1
new Task-245 rollover transaction = not observed
complete retained Python exception = unavailable
live repair/semantic effects in Task 246 = 0
```

Task-246 report-head Actions are GREEN:

```text
PS5.1 Acceptance Smoke        33881077771 = SUCCESS
Windows Installer Pack Smoke 33881077746 = SUCCESS
Validate                      33881077796 = SUCCESS
```

The exact Python exception must not be guessed.

## Active Task 247

Execute:

`docs/operations/coordination/tasks/CNX-20260904-247-task246-powershell51-native-stderr-capture-tdd-diagnosis-repair.md`

Required sequence:

```text
fresh GitHub authority
-> test-only Windows PowerShell 5.1 RED with harmless multi-line native stderr child
-> prove or reject NativeCommandError/truncation hypothesis
-> if hypothesis rejected: no production edit, report, STOP
-> if meaningful RED: minimal owning-boundary repair only
-> exact RED becomes GREEN
-> targeted + full repository validation
-> exact-SHA Actions GREEN
-> report
-> STOP for independent review
```

The RED must exercise `$ErrorActionPreference='Stop'` and the actual installer-relevant native stderr capture semantics. A helper-only or static-string test is insufficient.

## Hard boundaries

Task 247 is repository/test work only.

```text
live installer invocations = 0
installer Scheduled Task registrations/starts = 0
live rollover/plugin/controller/Gateway/DB mutation = 0
Dashboard/Discord/API semantic sends = 0
recovery replay/resend = 0
historical evidence cleanup = 0
release/tag/history mutation = 0
```

No production edit is allowed before a meaningful test-only RED. Do not change `namespace_ownership.py`, rollover ownership semantics, plugin payload behavior, lifecycle ordering, or semantic-delivery behavior.

## Expected payload identity

Accepted predecessor executable candidate:

`18a51b15768fb3d2196e65f1ef470c34aeef7f36`

Expected plugin payload fingerprint remains:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

## Stop boundary

Hermes must publish:

`docs/operations/coordination/reports/CNX-20260904-247-task246-powershell51-native-stderr-capture-tdd-diagnosis-repair.md`

Then STOP for independent ChatGPT review. A live installer retry and semantic acceptance remain separate, unauthorized successors.
