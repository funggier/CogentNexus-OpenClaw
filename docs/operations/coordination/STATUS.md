# Coordination Channel Status

Status: `READY_FOR_HERMES`
State: `V0.9.5_FINAL_ACCEPTANCE_SYSTEM_CHECK_SUCCESSOR`
Execution mode: `SINGLE_EXECUTOR__ROOT_CAUSE_TDD`
Task ID: `CNX-20260913-320`
Parent: `CNX-20260913-319`
Executor: `Hermes`
Reviewer: `ChatGPT`
Release candidate: `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`
Candidate branch: `fix/v0.9.5-final-acceptance-installer-cli`
Authority branch: `coord/v0.9.5-final-acceptance`

## Current position

Task 319 stopped after a real post-install defect: `cnxclaw status` accepted canonical `cnxMode`, but `cnxclaw check system` still read only legacy `mode` and returned `invalid Host mode: None`. The defect was repaired test-first by `b53cea15` followed by `fc3f4bc0`.

Reported requalification for `fc3f4bc0`: focused 4 passed; Python 672 passed, 5 skipped, 38 subtests passed; npm 337 passed; plugin validation/build/package PASS. These results require exact-candidate verification by Hermes.

## Release gate state

```text
Previous Candidate             345b92b4b1eac5cf8c3813de96565d6ca8b5f927
Successor Candidate            fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23
Successor Automated Validation NOT YET VERIFIED HERE
Installation                   RETRY AUTHORIZED UNDER TASK 320
Provider Switch                INDETERMINATE
Idle Quiescence                INDETERMINATE
Controlled Wake                INDETERMINATE
Finalization                   BLOCKED
PR #38                         OPEN / UNMODIFIED
Merge                          None
Tag                            None
Release                        Not published
```

## Runtime/model boundary

A prior external operation removed `ollama/qwen3.5:9b` while some sessions remained pinned to that model. Do not restore, recreate, or mutate unrelated provider/model state merely to make acceptance pass. If documented acceptance cannot proceed without such mutation, stop and report `BLOCKED`.

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
- Do not expose, record, copy, or mutate secrets or credentials.
- Do not perform unrelated Scheduled Task, service, provider-routing, or configuration changes.
- Do not manually mutate Ticket/SQLite/session/transcript/delivery state outside normal documented acceptance operations.
- Do not infer PASS from absence of failure.
- Stop and report `BLOCKED` when a required action exceeds this authority.
