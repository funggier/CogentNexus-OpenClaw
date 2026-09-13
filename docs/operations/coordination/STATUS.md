# Coordination Channel Status

Status: `READY_FOR_HERMES`
State: `V0.9.5_PROVIDER_READINESS_SUCCESSOR`
Execution mode: `SINGLE_EXECUTOR__ROOT_CAUSE_TDD`
Task ID: `CNX-20260913-321`
Parent: `CNX-20260913-320`
Executor: `Hermes`
Reviewer: `ChatGPT`
Release candidate: `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`
Candidate branch: `fix/v0.9.5-final-acceptance-installer-cli`
Authority branch: `coord/v0.9.5-final-acceptance`

## Current position

Task 320 established healthy v0.9.5 runtime and PASS results for the Ollama and OpenAI reply paths. The configured LM Studio endpoint at `http://127.0.0.1:1234` was unreachable with WinError 10061, so full Provider Switch Acceptance could not be claimed.

The exact candidate remains `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`. A bounded successor task is authorized to verify candidate identity, re-run candidate-sensitive validation, diagnose LM Studio availability, and continue acceptance only without unrelated provider/model mutation.

## Release gate state

```text
Candidate                      fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23
Runtime health                 PASS
Ollama                         PASS
OpenAI                         PASS
LM Studio                     FAIL / UNAVAILABLE at last evidence
Provider Switch                INDETERMINATE
Idle Quiescence               INDETERMINATE
Controlled Wake               INDETERMINATE
Finalization                  BLOCKED
PR #38                        OPEN / UNMODIFIED
Merge                         None
Tag                           None
Release                       Not published
```

## Provider/model boundary

Do not restore, recreate, replace, or mutate provider/model configuration merely to satisfy the acceptance gate. Do not restore `ollama/qwen3.5:9b` solely for pinned sessions. Do not substitute another provider/model and claim LM Studio acceptance passed.

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
- If another genuine code defect is discovered, stop live acceptance, reproduce it, make only the minimum justified TDD repair, create a new candidate SHA, requalify it, and report the new candidate explicitly.
- If acceptance requires an out-of-scope provider/model mutation or broader recovery, stop and report `BLOCKED`.
