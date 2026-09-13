# Active Coordination Task

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

## Objective

Recover the missing Idle Quiescence evidence for the unchanged v0.9.5 candidate. Task 321 verified runtime health and the required OpenAI/Ollama provider scope, but the idle checker observed zero parseable records.

## Authorized scope

Hermes may verify the exact candidate, verify the existing runtime and provenance, diagnose the idle observation/evidence path using bounded read-only diagnostics, restore normal observation through the documented runtime path, observe at least two real supervisor cadences, run the idle checker, and only after Idle PASS execute Controlled Actionable Wake with exactly one durable work item.

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

## Candidate and provider boundary

Candidate remains exactly:

`fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`

Required provider acceptance:

```text
OpenAI    REQUIRED
Ollama    REQUIRED
LM Studio NOT REQUIRED
```

Do not change provider/model configuration merely to generate evidence. Do not restore `ollama/qwen3.5:9b` solely for pinned sessions. Do not substitute providers or models.

## Hard fences

- Do not modify or merge PR #38.
- Do not create, move, or delete tag `v0.9.5`.
- Do not publish GitHub Release.
- Do not force-push.
- Do not expose, copy, or mutate secrets or credentials.
- Do not perform unrelated service, Scheduled Task, provider-routing, or configuration changes.
- Do not manually mutate Ticket, SQLite, session, transcript, or delivery state outside documented normal acceptance operations.
- Do not fabricate observation records or infer PASS from absence of failure.
- If a genuine code defect is discovered, stop, reproduce, make only the minimum justified TDD repair, create a new candidate SHA, requalify it, and report it.
- If evidence requires an out-of-scope mutation, stop and report `BLOCKED`.

## Required order

1. Verify exact candidate SHA.
2. Verify installed provenance/fingerprint and runtime health.
3. Diagnose the zero-record idle observation window using bounded read-only checks.
4. Restore normal observation/evidence collection only if supported and in scope.
5. Collect >=2 real supervisor cadences and rerun the idle checker.
6. Require the complete idle evidence contract to PASS.
7. Run Controlled Actionable Wake with exactly one durable work item.
8. Preserve raw evidence and publish a successor report.
9. Re-check candidate identity and all gates.
10. Stop before PR #38 update, merge, tag, or release.

## Completion gates

```text
Candidate identity       VERIFIED
Runtime                  PASS
OpenAI                   PASS
Ollama                   PASS
Idle Quiescence          PASS
Controlled Wake          PASS
Evidence                 PUBLISHED
Finalization             remains a separate successor decision
```

## Evidence contract

Every result must bind to the exact candidate and include environment, installed provenance/fingerprint, timestamps, observation-window boundaries, raw idle checker output, required idle fields, and Controlled Wake evidence if executed.
