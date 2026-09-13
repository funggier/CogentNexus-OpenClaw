# Coordination Channel Status

Status: `READY_FOR_HERMES`
State: `V0.9.5_IDLE_EVIDENCE_RECOVERY`
Execution mode: `SINGLE_EXECUTOR__ROOT_CAUSE_TDD`
Task ID: `CNX-20260913-322`
Parent: `CNX-20260913-321`
Executor: `Hermes`
Reviewer: `ChatGPT`
Release candidate: `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`
Candidate branch: `fix/v0.9.5-final-acceptance-installer-cli`
Authority branch: `coord/v0.9.5-final-acceptance`

## Current position

Task 321 reached a hard evidence boundary. The exact candidate, runtime health, and required OpenAI/Ollama provider scope were verified, but the idle checker returned no parseable observation records and idleTicks=0.

This is not a code-candidate defect. The unchanged candidate remains authorized.

## Release gate state

```text
Candidate                  fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23
Runtime                    PASS
OpenAI                     PASS / REQUIRED
Ollama                     PASS / REQUIRED
LM Studio                  NOT REQUIRED
Idle Quiescence            INDETERMINATE
Controlled Wake            NOT RUN
Finalization               BLOCKED
PR #38                     OPEN / UNMODIFIED
Merge                      None
Tag                        None
Release                    Not published
```

## Provider/model boundary

Do not restore, recreate, replace, or mutate provider/model configuration merely to obtain idle evidence. Do not restore `ollama/qwen3.5:9b` solely for pinned sessions. Do not substitute another provider or model.

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

- Do not modify or merge PR #38.
- Do not create, move, or delete `v0.9.5` tag.
- Do not publish GitHub Release.
- Do not force-push.
- Do not expose, record, copy, or mutate secrets or credentials.
- Do not perform unrelated Scheduled Task, service, provider-routing, or configuration changes.
- Do not manually mutate Ticket, SQLite, session, transcript, or delivery state outside documented normal acceptance operations.
- Do not fabricate observation records or infer PASS from absence of failure.
- If a genuine code defect is discovered, stop, reproduce, make only the minimum justified TDD repair, create a new candidate SHA, requalify it, and report it.
- If evidence requires an out-of-scope mutation, stop and report `BLOCKED`.

## Task 322 objective

Diagnose why the real runtime observation window contains zero parseable idle records. Restore normal observation/evidence collection only through a documented, supported, in-scope runtime path. Then collect at least two real supervisor cadences and prove the idle contract. Only after Idle PASS may Controlled Actionable Wake be executed.
