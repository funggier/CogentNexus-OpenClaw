# CNX-20260913-319 — v0.9.5 Final Acceptance Successor After npm stderr Repair

Status: `READY_FOR_HERMES`
Executor: `Hermes`
Reviewer: `ChatGPT`

## Candidate

Authorized candidate:

`345b92b4b1eac5cf8c3813de96565d6ca8b5f927`

Candidate branch:

`fix/v0.9.5-final-acceptance-installer-cli`

Parent task:

`CNX-20260913-318`

Authority branch:

`coord/v0.9.5-final-acceptance`

## Objective

Complete candidate-sensitive requalification and live v0.9.5 acceptance against the successor candidate created by the test-first repair of the Windows PowerShell 5.1 npm stderr boundary defect.

## Defect boundary inherited from Task 318

Task 318 stopped after a real installer defect was reproduced. The failure occurred because `scripts/install.ps1` invoked npm directly while `$ErrorActionPreference = "Stop"`; npm emitted warning diagnostics on stderr with exit code 0, and Windows PowerShell 5.1 raised `NativeCommandError` before `$LASTEXITCODE` could be evaluated.

Repair sequence:

```text
3b42bb2f  RED test: cover installer npm stderr boundary
345b92b4  minimal fix: preserve npm stderr diagnostics in installer
```

The repair wraps npm execution through the installer diagnostic boundary and evaluates the returned exit code without treating benign native stderr diagnostics as command failure.

## Required order

1. Verify the candidate SHA is exactly `345b92b4b1eac5cf8c3813de96565d6ca8b5f927` on the remote candidate branch.
2. Run candidate-sensitive repository validation and preserve the exact outputs.
3. Verify or restore a healthy acceptance runtime using bounded supported diagnostics/recovery only.
4. Install-over the exact successor candidate.
5. Verify installed version, provenance/fingerprint, Gateway health, plugin state, generation, and provider ownership.
6. Execute Provider Switch Acceptance using the documented acceptance procedure.
7. Execute Idle Quiescence for at least two supervisor cadences.
8. Execute Controlled Actionable Wake with exactly one durable work item.
9. Preserve raw evidence and publish a successor acceptance report.
10. Re-check candidate identity and every gate verdict.
11. Stop before PR #38 modification, merge, tag, or GitHub Release.

## Required idle evidence

```text
wakeReason=idle/no-actionable-work
heavyPath=false
heavySupervisorCalls=0
providerRecoveryActions=0
configMutations=0
gatewayLifecycleActions=0
idleTicks>=2
```

Missing, incomplete, or unusable evidence remains `INDETERMINATE`.

## Runtime/model boundary

A prior external operation removed `ollama/qwen3.5:9b` while some sessions remained pinned to that model. This state is explicitly outside the acceptance retry unless the documented Provider Switch Acceptance requires a bounded operation that is authorized by this task. Do not restore, recreate, or mutate unrelated provider/model state merely to make the environment look healthy. Record the observed state and stop if the required acceptance procedure cannot proceed within scope.

## Hard fences

- Do not modify PR #38 in this task.
- Do not merge PR #38.
- Do not create, move, or delete tag `v0.9.5`.
- Do not publish a GitHub Release.
- Do not force-push.
- Do not expose, copy, record, or mutate credentials, API keys, tokens, cookies, or secrets.
- Do not perform unrelated Scheduled Task, service, provider-routing, or configuration changes.
- Do not manually mutate Ticket, SQLite, session, transcript, or delivery state outside documented normal acceptance operations.
- Do not infer PASS from absence of failure.
- If another genuine defect is found, stop live acceptance, reproduce it, make only the minimum justified repair, create a new candidate SHA, rerun candidate-sensitive validation, and report the successor explicitly.
- Stop and report `BLOCKED` whenever a required action exceeds this authority.

## Evidence contract

Every live result must bind to:

`345b92b4b1eac5cf8c3813de96565d6ca8b5f927`

Evidence must include environment, installed version/fingerprint, exact procedures/commands, timestamps, provider sequence, session/Ticket/run identity, generation/ownership evidence, idle checker output, controlled-wake evidence, and evidence locations.

## Release state at task start

```text
PR #38: OPEN / UNMODIFIED
PR #38 HEAD: a986f3261b1570d1bcb1574d2458fe7068207a9c
Provider Switch: INDETERMINATE
Idle Quiescence: INDETERMINATE
Controlled Wake: INDETERMINATE
Finalization: BLOCKED
Merge SHA: None
Tag v0.9.5: None
GitHub Release: Not published
```

## Stop condition

Task 319 ends after candidate-sensitive validation and live evidence collection, or immediately at a hard-fence boundary. Release promotion requires a separate successor decision after all evidence is independently verified.
