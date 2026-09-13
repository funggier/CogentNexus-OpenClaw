# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `V0.9.5_FINAL_ACCEPTANCE_SYSTEM_CHECK_SUCCESSOR`
Execution mode: `SINGLE_EXECUTOR__ROOT_CAUSE_TDD`
Task ID: `CNX-20260913-320`
Parent: `CNX-20260913-319`
Executor: `Hermes`
Reviewer: `ChatGPT`
Release candidate: `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`
Candidate branch: `fix/v0.9.5-final-acceptance-installer-cli`
Authority branch: `coord/v0.9.5-final-acceptance`

## Objective

Requalify and perform live v0.9.5 acceptance against the successor candidate after Task 319 found that the system-check path still consumed only legacy `mode` while canonical v0.9.5 state is `cnxMode`.

## Authorized scope

Hermes may verify the exact candidate, run candidate-sensitive repository validation, verify the system-check regression, use bounded supported runtime diagnostics/recovery, install-over the exact candidate, verify provenance/fingerprint and runtime health, verify canonical controller-state handling without manual state rewriting, execute Provider Switch Acceptance, Idle Quiescence for at least two supervisor cadences, Controlled Actionable Wake with exactly one durable work item, and collect auditable evidence.

## Required order

1. Verify candidate SHA exactly `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`.
2. Run candidate-sensitive validation.
3. Verify canonical system-check regression.
4. Verify or restore healthy acceptance runtime using bounded supported recovery only.
5. Install-over exact candidate and verify installed provenance/fingerprint and runtime health.
6. Verify `cnxclaw status` and `cnxclaw check system` both accept canonical controller state without mutating the controller.
7. Execute Provider Switch Acceptance.
8. Execute Idle Quiescence for >=2 supervisor cadences.
9. Execute Controlled Actionable Wake with exactly one durable work item.
10. Preserve raw evidence and publish successor acceptance report.
11. Re-check exact candidate identity and all verdicts.
12. Stop before PR #38 update, merge, tag, or GitHub Release.

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

## Runtime/model boundary

The acceptance environment has a prior external operation removing `ollama/qwen3.5:9b` while some sessions remained pinned to it. Do not restore, recreate, or mutate unrelated provider/model state merely to make acceptance pass. If documented acceptance cannot proceed without such mutation, stop and report `BLOCKED`.

## Hard fences

- Do not modify or merge PR #38 in this task.
- Do not create, move, or delete `v0.9.5` tag.
- Do not publish GitHub Release.
- Do not force-push.
- Do not expose, record, copy, or mutate credentials, API keys, tokens, cookies, or secrets.
- Do not perform unrelated Scheduled Task, service, provider-routing, or configuration changes.
- Do not manually mutate Ticket, SQLite, session, transcript, or delivery state outside normal documented acceptance operations.
- Do not infer PASS from absence of failure.
- If another genuine defect is discovered, stop live acceptance, reproduce it, make only the minimum justified repair, create a new candidate SHA, rerun candidate-sensitive validation, and report the new candidate explicitly.
- Stop and report `BLOCKED` if a required action exceeds this authority.

## Expected canonical mapping

```text
active      -> managed
disabled    -> passthrough
maintenance -> maintenance
```

Compatibility mapping must remain an in-memory derived view only.

## Evidence contract

Every live result must bind to `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23` and include environment, installed version/fingerprint, commands/procedure, timestamps, provider sequence, session/Ticket/run identity, generation/ownership evidence, system-check output, idle checker output, controlled-wake evidence, and evidence locations.

## Stop condition

The task ends after evidence collection/reporting or at a hard-fence boundary. Release promotion remains a separate successor decision.
