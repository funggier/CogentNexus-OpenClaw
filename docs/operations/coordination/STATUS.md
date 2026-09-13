# Coordination Channel Status

Status: `READY_FOR_HERMES`
State: `V0.9.5_FINAL_ACCEPTANCE_NPM_STDERR_SUCCESSOR`
Execution mode: `SINGLE_EXECUTOR__ROOT_CAUSE_TDD`
Task ID: `CNX-20260913-319`
Parent: `CNX-20260913-318`
Executor: `Hermes`
Reviewer: `ChatGPT`
Release candidate: `345b92b4b1eac5cf8c3813de96565d6ca8b5f927`
Candidate branch: `fix/v0.9.5-final-acceptance-installer-cli`
Authority branch: `coord/v0.9.5-final-acceptance`

## Current position

Task 318 stopped after a real Windows PowerShell 5.1 installer defect: direct npm invocation under strict native-command error handling treated benign stderr diagnostics as command failure before `$LASTEXITCODE` could be evaluated.

Task 318 produced a test-first repair and the new authorized candidate is `345b92b4b1eac5cf8c3813de96565d6ca8b5f927`. Reported requalification: 5 focused tests passed; Python 670 passed, 5 skipped, 38 subtests passed; npm 337 passed; plugin validation/build/package PASS. These results require exact-candidate verification by Hermes.

## Release gate state

```text
Previous Candidate             2a1be3b5c2e95664da97f2aea103a57a4947fd9d
Successor Candidate            345b92b4b1eac5cf8c3813de96565d6ca8b5f927
Successor Automated Validation NOT YET VERIFIED HERE
Installation                   RETRY AUTHORIZED UNDER TASK 319
Provider Switch                INDETERMINATE
Idle Quiescence                INDETERMINATE
Controlled Wake                INDETERMINATE
Finalization                   BLOCKED
PR #38                         OPEN / UNMODIFIED
Merge                          None
Tag                            None
Release                        Not published
```

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

Missing or unusable evidence remains `INDETERMINATE`.

## Hard fences

- Do not modify or merge PR #38 in this task.
- Do not create, move, or delete `v0.9.5` tag.
- Do not publish GitHub Release.
- Do not force-push.
- Do not expose, record, or mutate secrets or credentials.
- Do not perform unrelated Scheduled Task, service, provider-routing, or configuration changes.
- Do not manually mutate Ticket/SQLite/session/transcript/delivery state outside normal documented acceptance operations.
- Do not infer PASS from absence of failure.
- Stop and report `BLOCKED` when a required action exceeds this authority.
