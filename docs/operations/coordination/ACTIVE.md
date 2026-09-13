# Active Coordination Task

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

## Objective

Continue final v0.9.5 live acceptance with the required provider acceptance scope limited to OpenAI and Ollama. LM Studio is not a release gate.

## Authorized scope

Hermes may verify the exact candidate, run candidate-sensitive repository validation, verify installed runtime and provenance, verify OpenAI and Ollama reply-path acceptance, execute Idle Quiescence for >=2 supervisor cadences, Controlled Actionable Wake with exactly one durable work item, and collect auditable evidence.

## Required order

1. Verify exact candidate SHA.
2. Re-run candidate-sensitive validation.
3. Verify installed provenance/fingerprint and runtime health.
4. Verify OpenAI reply-path acceptance.
5. Verify Ollama reply-path acceptance.
6. Execute Idle Quiescence for >=2 supervisor cadences.
7. Execute Controlled Actionable Wake with exactly one durable work item.
8. Preserve raw evidence and publish successor acceptance report.
9. Re-check candidate identity and all required gates.
10. Stop before PR #38 update, merge, tag, or GitHub Release.

## Provider acceptance scope

```text
OpenAI    REQUIRED
Ollama    REQUIRED
LM Studio NOT REQUIRED
```

Successful OpenAI and Ollama exchanges, when bound to the exact candidate and acceptance runtime, satisfy the provider acceptance requirement.

LM Studio may remain unavailable and must not block provider acceptance or trigger unrelated provider/model mutation.

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
- Do not expose, record, or mutate credentials, API keys, tokens, cookies, or secrets.
- Do not perform unrelated Scheduled Task, service, provider-routing, or configuration changes.
- Do not manually mutate Ticket, SQLite, session, transcript, or delivery state outside normal documented acceptance operations.
- Do not infer PASS from absence of failure.
- If another genuine code defect is discovered, stop live acceptance, reproduce it, make only the minimum justified TDD repair, create a new candidate SHA, requalify it, and report the new candidate explicitly.
- If acceptance requires an out-of-scope provider/model mutation or broader recovery, stop and report `BLOCKED`.

## Evidence contract

Every result must bind to `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23` and include environment, installed fingerprint/provenance, commands/procedure, timestamps, OpenAI and Ollama provider sequence, session/Ticket/run identity, generation/ownership evidence, idle checker output, controlled-wake evidence, and evidence locations.

## Stop condition

The task ends after evidence collection/reporting or at a hard-fence boundary. Release promotion remains a separate successor decision.
