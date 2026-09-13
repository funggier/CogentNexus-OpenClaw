# CNX-20260913-321 — v0.9.5 Provider Acceptance Successor

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

Complete candidate-sensitive verification and live v0.9.5 acceptance with the required provider acceptance scope limited to the OpenAI and Ollama reply paths. LM Studio is not a release gate for this acceptance.

## Required order

1. Verify the exact candidate SHA is `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`.
2. Re-run candidate-sensitive validation as required for this exact candidate.
3. Verify the existing installed runtime remains healthy and provenance/fingerprint remains bound to the candidate.
4. Verify OpenAI reply-path acceptance.
5. Verify Ollama reply-path acceptance.
6. Execute Idle Quiescence for >=2 supervisor cadences.
7. Execute Controlled Actionable Wake with exactly one durable work item.
8. Preserve raw evidence and publish the successor acceptance report.
9. Re-check candidate identity and every required gate.
10. Stop before PR #38 update, merge, tag, or GitHub Release.

## Provider acceptance scope

Required providers for v0.9.5 final acceptance:

```text
OpenAI   REQUIRED
Ollama   REQUIRED
LM Studio NOT REQUIRED
```

A successful OpenAI exchange and a successful Ollama exchange satisfy the provider acceptance requirement when their evidence is bound to the exact candidate and acceptance runtime.

LM Studio may remain unavailable and must not block provider acceptance or be used as a reason to mutate unrelated provider/model state.

## Provider/model boundary

The acceptance environment previously lost `ollama/qwen3.5:9b` while some sessions remained pinned to it. Do not restore, recreate, replace, or otherwise mutate provider/model configuration merely to satisfy acceptance. Do not substitute another provider/model in place of OpenAI or Ollama and claim the required provider acceptance passed.

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
- Do not expose, record, or mutate credentials, API keys, tokens, cookies, or secrets.
- Do not perform unrelated Scheduled Task, service, provider-routing, or configuration changes.
- Do not manually mutate Ticket, SQLite, session, transcript, or delivery state outside normal documented acceptance operations.
- Do not infer PASS from absence of failure.
- If a code defect is discovered, stop live acceptance, reproduce it, apply only a minimal TDD repair, create a new candidate SHA, requalify it, and report the new candidate explicitly.
- If acceptance requires an out-of-scope provider/model mutation or other broader recovery, stop and report `BLOCKED`.

## Evidence contract

Every result must bind to `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23` and include environment, installed fingerprint/provenance, commands/procedure, timestamps, provider sequence for OpenAI and Ollama, session/Ticket/run identity, generation/ownership evidence, idle checker output, controlled-wake evidence, and evidence locations.

## Stop condition

The task ends after evidence collection/reporting or at a hard-fence boundary. Release promotion remains a separate successor decision.
