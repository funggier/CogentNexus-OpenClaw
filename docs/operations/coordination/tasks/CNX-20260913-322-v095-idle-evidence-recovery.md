# CNX-20260913-322 — v0.9.5 Idle Evidence Recovery

Status: `READY_FOR_HERMES`
Executor: `Hermes`
Reviewer: `ChatGPT`
Parent: `CNX-20260913-321`
Candidate: `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`
Candidate branch: `fix/v0.9.5-final-acceptance-installer-cli`
Authority branch: `coord/v0.9.5-final-acceptance`

## Objective

Recover the missing Idle Quiescence evidence for the unchanged v0.9.5 candidate. The previous task proved runtime health plus required OpenAI and Ollama provider paths, but the idle checker observed zero parseable records and could not prove the idle contract.

## Required order

1. Verify candidate SHA exactly `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`.
2. Verify existing installed runtime and provenance remain healthy; do not reinstall unless required by documented evidence integrity.
3. Perform bounded read-only diagnosis of why the runtime ledger/observation window contains zero parseable idle records.
4. Restore observation/evidence collection only through the documented normal runtime path; do not fabricate records and do not alter provider/model configuration.
5. Observe at least two supervisor cadences and run the idle checker against those real observations.
6. Require all idle evidence fields:

```text
wakeReason=idle/no-actionable-work
heavyPath=false
heavySupervisorCalls=0
providerRecoveryActions=0
configMutations=0
gatewayLifecycleActions=0
idleTicks>=2
```

7. Only after Idle Quiescence is PASS, execute Controlled Actionable Wake with exactly one durable work item.
8. Preserve raw evidence and publish a successor acceptance report.
9. Re-check candidate identity and all gates.
10. Stop before PR #38 update, merge, tag, or GitHub Release.

## Scope boundary

This task is an evidence-acquisition recovery task, not a candidate-change task. Do not create a new code candidate unless a genuine code defect is reproduced.

Do not restore, recreate, replace, or mutate provider/model configuration merely to obtain idle evidence. Do not restore `ollama/qwen3.5:9b`. Do not substitute another provider/model.

Do not manually mutate Ticket, SQLite, session, transcript, or delivery state outside documented normal acceptance operations.

## Hard fences

- No PR #38 modification or merge.
- No v0.9.5 tag creation, movement, or deletion.
- No GitHub Release publication.
- No force-push.
- No credentials, API keys, tokens, cookies, or secrets exposure or mutation.
- No unrelated Scheduled Task, service, provider-routing, or configuration mutation.
- No inference of PASS from absence of failure.
- If another genuine code defect is found, stop, reproduce, make minimal TDD repair, create a new candidate SHA, requalify, and report it.
- If evidence cannot be obtained without broader/out-of-scope mutation, stop and report `BLOCKED`.

## Current gates at task start

```text
Candidate:         fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23
Runtime:            PASS
OpenAI:             PASS
Ollama:             PASS
LM Studio:          NOT REQUIRED
Idle Quiescence:    INDETERMINATE
Controlled Wake:    NOT RUN
Finalization:       BLOCKED
PR #38:             OPEN / UNMODIFIED
```

## Evidence contract

Every result must bind to the exact candidate and include environment, installed provenance/fingerprint, timestamps, observation-window boundaries, raw idle checker output, required idle fields, and Controlled Wake evidence if executed.
