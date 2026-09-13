# CNX-20260913-320 — v0.9.5 System Check Successor

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
CNX-20260913-319
```

## Objective

Requalify the exact successor candidate after Task 319 discovered a post-install defect in `cnxclaw check system`: the command still consumed only the legacy controller `mode` field while v0.9.5 canonical state is persisted as `cnxMode`.

## Required order

1. Verify the candidate SHA is exactly `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`.
2. Run candidate-sensitive repository validation.
3. Verify the system-check regression specifically covers canonical controller state and passes.
4. Verify or restore a healthy acceptance runtime using bounded supported diagnostics/recovery only.
5. Install-over the exact candidate and verify installed provenance/fingerprint and runtime health.
6. Verify `cnxclaw status` and `cnxclaw check system` both accept canonical v0.9.5 controller state without mutating the controller.
7. Execute Provider Switch Acceptance.
8. Execute Idle Quiescence for >=2 supervisor cadences.
9. Execute Controlled Actionable Wake with exactly one durable work item.
10. Preserve raw evidence and publish the successor acceptance report.
11. Re-check candidate identity and all verdicts.
12. Stop before PR #38 update, merge, tag, or GitHub Release.

## Expected canonical state mapping

```text
cnxMode=active      -> managed
cnxMode=disabled    -> passthrough
cnxMode=maintenance -> maintenance
```

The compatibility mapping is an in-memory derived view only. Do not rewrite canonical controller state merely to satisfy a legacy check.

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

The acceptance environment has a prior external provider/model mutation where `ollama/qwen3.5:9b` was removed while some sessions remained pinned to it. Do not restore, recreate, or mutate unrelated provider/model state merely to make acceptance pass. If a documented acceptance step cannot proceed without such mutation, stop and report `BLOCKED`.

## Hard fences

- Do not modify or merge PR #38 in this task.
- Do not create, move, or delete tag `v0.9.5`.
- Do not publish a GitHub Release.
- Do not force-push.
- Do not expose, record, copy, or mutate credentials, API keys, tokens, cookies, or secrets.
- Do not perform unrelated Scheduled Task, service, provider-routing, or configuration changes.
- Do not manually mutate Ticket, SQLite, session, transcript, or delivery state outside normal documented acceptance operations.
- Do not infer PASS from absence of failure.
- If another genuine defect is discovered, stop live acceptance, reproduce it, make only the minimum justified repair, create a new candidate SHA, rerun candidate-sensitive validation, and report the new candidate explicitly.
- Stop and report `BLOCKED` if a required action exceeds this authority.

## Evidence contract

Every live result must bind to `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23` and include environment, installed version/fingerprint, commands/procedure, timestamps, provider sequence, session/Ticket/run identity, generation/ownership evidence, system-check output, idle checker output, controlled-wake evidence, and evidence locations.

## Stop condition

The task ends after evidence collection/reporting or at a hard-fence boundary. Release promotion remains a separate successor decision.
