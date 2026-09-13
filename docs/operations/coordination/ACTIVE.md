# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `V0.9.5_CONTROLLED_WAKE_PENDING`
Execution mode: `SINGLE_EXECUTOR__ROOT_CAUSE_TDD`
Task ID: `CNX-20260913-322`
Parent: `CNX-20260913-321`
Executor: `Hermes`
Reviewer: `ChatGPT`
Release candidate: `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`
Candidate branch: `fix/v0.9.5-final-acceptance-installer-cli`
Authority branch: `coord/v0.9.5-final-acceptance`

## Current objective

Idle Quiescence evidence has passed for the unchanged v0.9.5 candidate. The next authorized step is Controlled Actionable Wake with exactly one durable work item.

## Verified idle evidence

```text
verdict=PASS
wakeReason=idle/no-actionable-work
heavyPath=false
heavySupervisorCalls=0
providerRecoveryActions=0
configMutations=0
gatewayLifecycleActions=0
idleTicks=2
observationRecords=2
parseErrors=0
stateEvidencePresent=true
reason=bounded observation evidence is sufficient
```

Two real supervisor cadences were observed and normalized/deduplicated before checker evaluation.

## Provider scope

```text
OpenAI    REQUIRED / PASS
Ollama    REQUIRED / PASS
LM Studio NOT REQUIRED
```

## Required next step

Execute Controlled Actionable Wake with exactly one durable work item through the documented normal acceptance path. Preserve session/Ticket/run identity, generation/ownership evidence, and successful handling/settlement evidence.

## Hard fences

- Do not modify or merge PR #38.
- Do not create, move, or delete tag `v0.9.5`.
- Do not publish GitHub Release.
- Do not force-push.
- Do not expose, copy, or mutate secrets or credentials.
- Do not restore or recreate `ollama/qwen3.5:9b` solely to satisfy acceptance.
- Do not substitute another provider or model for the required OpenAI/Ollama scope.
- Do not perform unrelated service, Scheduled Task, provider-routing, or configuration changes.
- Do not manually mutate Ticket, SQLite, session, transcript, or delivery state outside documented normal acceptance operations.
- Do not fabricate evidence or infer Controlled Wake PASS from absence of failure.
- If a genuine code defect is discovered, stop, reproduce, make only the minimum justified TDD repair, create a new candidate SHA, requalify it, and report it.
- If Controlled Wake requires an out-of-scope mutation, stop and report `BLOCKED`.

## Evidence contract

Controlled Wake evidence must bind to candidate `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23` and include environment, installed provenance/fingerprint, timestamps, the single durable work-item identity, session/Ticket/run identity, generation/ownership evidence, wake/processing/settlement evidence, and evidence locations.

## Stop condition

After Controlled Wake evidence is collected and the successor report is published, stop. PR promotion, merge, tagging, and release remain a separate successor decision.
