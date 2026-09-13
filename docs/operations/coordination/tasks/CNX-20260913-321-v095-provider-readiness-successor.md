# CNX-20260913-321 — v0.9.5 Provider Readiness Successor

Status: `READY_FOR_HERMES`
Executor: `Hermes`
Reviewer: `ChatGPT`

## Candidate

```text
fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23
```

Candidate branch:

```text
fix/v0.9.5-final-acceptance-installer-cli
```

Parent task:

```text
CNX-20260913-320
```

## Objective

Complete candidate-sensitive verification and live v0.9.5 acceptance after Task 320 reached a provider-acceptance boundary: Ollama and OpenAI reply paths passed, while the configured LM Studio endpoint was unreachable and full provider-switch acceptance therefore remained unproven.

## Required order

1. Verify the exact candidate SHA is `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`.
2. Re-run candidate-sensitive validation as required for this exact candidate.
3. Verify the existing installed runtime remains healthy and provenance/fingerprint remains bound to the candidate.
4. Perform bounded, read-only diagnosis of the LM Studio endpoint at `http://127.0.0.1:1234`.
5. Determine whether the documented acceptance procedure can proceed without unrelated provider/model mutation.
6. If the LM Studio acceptance precondition becomes available through a normal, already-authorized environment action, execute Provider Switch Acceptance.
7. Execute Idle Quiescence for >=2 supervisor cadences.
8. Execute Controlled Actionable Wake with exactly one durable work item.
9. Preserve raw evidence and publish the successor acceptance report.
10. Re-check candidate identity and every gate.
11. Stop before PR #38 update, merge, tag, or GitHub Release.

## Provider/model boundary

The acceptance environment previously lost `ollama/qwen3.5:9b` while some sessions remained pinned to it. Do not restore, recreate, replace, or otherwise mutate provider/model configuration merely to satisfy acceptance. Do not substitute another model or provider and claim LM Studio acceptance passed.

LM Studio failure evidence from Task 320:

```text
Endpoint: http://127.0.0.1:1234
Reachable: false
Healthy: false
Model count: 0
Error: WinError 10061 — connection refused
```

A successful Ollama or OpenAI exchange does not qualify the LM Studio gate.

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
- Do not create, move, or delete tag `v0.9.5`.
- Do not publish a GitHub Release.
- Do not force-push.
- Do not expose, record, copy, or mutate credentials, API keys, tokens, cookies, or secrets.
- Do not perform unrelated Scheduled Task, service, provider-routing, or configuration changes.
- Do not manually mutate Ticket, SQLite, session, transcript, or delivery state outside documented normal acceptance operations.
- Do not infer PASS from absence of failure.
- If a code defect is discovered, stop live acceptance, reproduce it, apply only a minimal TDD repair, create a new candidate SHA, requalify it, and report the new candidate explicitly.
- If the environment requires an out-of-scope provider/model mutation or other broader recovery, stop and report `BLOCKED`.

## Evidence contract

Every result must bind to `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23` and include environment, installed fingerprint/provenance, commands/procedure, timestamps, provider sequence, session/Ticket/run identity, generation/ownership evidence, LM Studio endpoint diagnosis, idle checker output, controlled-wake evidence, and evidence locations.

## Stop condition

The task ends after evidence collection/reporting or at a hard-fence boundary. Release promotion remains a separate successor decision.
