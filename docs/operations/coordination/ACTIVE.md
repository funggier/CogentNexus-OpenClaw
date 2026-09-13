# Active Coordination Task

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

## Objective

Continue final v0.9.5 live acceptance after Task 320 established healthy runtime plus PASS results for Ollama and OpenAI, but LM Studio was unavailable at the configured local endpoint and therefore full provider-switch acceptance remained unproven.

## Authorized scope

Hermes may verify the exact candidate, run candidate-sensitive repository validation, verify the installed runtime and provenance, perform bounded read-only diagnosis of LM Studio at `http://127.0.0.1:1234`, and, only if the endpoint becomes available through an already-authorized normal environment condition, execute the documented Provider Switch Acceptance, Idle Quiescence for >=2 supervisor cadences, Controlled Actionable Wake with exactly one durable work item, and evidence collection.

## Required order

1. Verify exact candidate SHA.
2. Re-run candidate-sensitive validation.
3. Verify installed provenance/fingerprint and runtime health.
4. Diagnose LM Studio endpoint availability without unrelated provider/model mutation.
5. If the documented LM Studio precondition is available, execute Provider Switch Acceptance.
6. Execute Idle Quiescence for >=2 supervisor cadences.
7. Execute Controlled Actionable Wake with exactly one durable work item.
8. Preserve raw evidence and publish successor acceptance report.
9. Re-check candidate identity and all verdicts.
10. Stop before PR #38 update, merge, tag, or GitHub Release.

## Provider/model boundary

Do not restore, recreate, replace, or mutate provider/model configuration merely to make acceptance pass. In particular, do not restore `ollama/qwen3.5:9b` solely because older sessions remain pinned to it. Do not substitute another provider or model and claim LM Studio acceptance passed.

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
- Do not expose, record, or mutate credentials, API keys, tokens, cookies, or secrets.
- Do not perform unrelated Scheduled Task, service, provider-routing, or configuration changes.
- Do not manually mutate Ticket, SQLite, session, transcript, or delivery state outside documented normal acceptance operations.
- Do not infer PASS from absence of failure.
- If another genuine code defect is discovered, stop live acceptance, reproduce it, make only the minimum justified TDD repair, create a new candidate SHA, requalify it, and report the new candidate explicitly.
- If acceptance requires an out-of-scope provider/model mutation or broader recovery, stop and report `BLOCKED`.

## Evidence contract

Every live result must bind to `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23` and include environment, installed fingerprint/provenance, commands/procedure, timestamps, provider sequence, session/Ticket/run identity, generation/ownership evidence, LM Studio diagnosis, idle checker output, controlled-wake evidence, and evidence locations.

## Stop condition

The task ends after evidence collection/reporting or at a hard-fence boundary. Release promotion remains a separate successor decision.
