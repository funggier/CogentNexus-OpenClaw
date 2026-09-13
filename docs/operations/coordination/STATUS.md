# Coordination Channel Status

Status: `READY_FOR_HERMES`
State: `V0.9.5_PROVIDER_ACCEPTANCE_OPENAI_OLLAMA`
Execution mode: `SINGLE_EXECUTOR__ROOT_CAUSE_TDD`
Task ID: `CNX-20260913-321`
Parent: `CNX-20260913-320`
Executor: `Hermes`
Reviewer: `ChatGPT`
Release candidate: `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`
Candidate branch: `fix/v0.9.5-final-acceptance-installer-cli`
Authority branch: `coord/v0.9.5-final-acceptance`

## Current position

Task 320 established healthy v0.9.5 runtime and PASS results for the Ollama and OpenAI reply paths. LM Studio was unavailable, but it is not part of the required v0.9.5 provider acceptance scope.

The exact candidate remains `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`. Task 321 is authorized to verify the candidate, re-run candidate-sensitive validation, confirm OpenAI and Ollama acceptance, then complete Idle Quiescence and Controlled Actionable Wake.

## Release gate state

```text
Candidate                      fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23
Runtime health                 PASS
Ollama                         PASS / REQUIRED
OpenAI                         PASS / REQUIRED
LM Studio                     NOT REQUIRED
Provider Acceptance            PENDING EXACT-CANDIDATE REVERIFICATION
Idle Quiescence               INDETERMINATE
Controlled Wake               INDETERMINATE
Finalization                  BLOCKED
PR #38                        OPEN / UNMODIFIED
Merge                         None
Tag                           None
Release                       Not published
```

## Provider acceptance scope

```text
OpenAI    REQUIRED
Ollama    REQUIRED
LM Studio NOT REQUIRED
```

## Provider/model boundary

Do not restore, recreate, replace, or otherwise mutate provider/model configuration merely to satisfy acceptance. Do not restore `ollama/qwen3.5:9b` solely because older sessions remain pinned to it. Do not substitute another provider/model for the required OpenAI or Ollama acceptance.

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
