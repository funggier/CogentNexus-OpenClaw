# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `V0.9.5_FINAL_ACCEPTANCE_NPM_STDERR_SUCCESSOR`
Execution mode: `SINGLE_EXECUTOR__ROOT_CAUSE_TDD`
Task ID: `CNX-20260913-319`
Parent: `CNX-20260913-318`
Executor: `Hermes`
Reviewer: `ChatGPT`
Release candidate: `345b92b4b1eac5cf8c3813de96565d6ca8b5f927`
Candidate branch: `fix/v0.9.5-final-acceptance-installer-cli`
Authority branch: `coord/v0.9.5-final-acceptance`

## Objective

Complete candidate-sensitive requalification and live v0.9.5 acceptance against the successor candidate created by the test-first repair of the Windows PowerShell 5.1 npm stderr boundary defect.

## Authorized scope

Hermes is authorized to verify the exact successor candidate, run candidate-sensitive repository validation, verify or restore a healthy acceptance runtime using bounded supported diagnostics/recovery only, install-over the exact successor candidate, verify installed provenance/fingerprint and runtime health, execute Provider Switch Acceptance, Idle Quiescence Acceptance for at least two supervisor cadences, Controlled Actionable Wake with exactly one durable work item, and collect auditable evidence.

## Required order

1. Verify candidate SHA is exactly `345b92b4b1eac5cf8c3813de96565d6ca8b5f927`.
2. Run candidate-sensitive repository validation.
3. Verify or restore healthy acceptance runtime using bounded supported recovery only.
4. Install-over and verify the exact successor candidate.
5. Verify installed version/provenance/fingerprint, Gateway health, plugin state, generation, and provider ownership.
6. Execute Provider Switch Acceptance.
7. Execute Idle Quiescence for >=2 supervisor cadences.
8. Execute Controlled Actionable Wake with exactly one durable work item.
9. Preserve raw evidence and publish a successor acceptance report.
10. Re-check candidate identity and all verdicts.
11. Stop before PR #38 update, merge, tag, or GitHub Release.

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

A prior external operation removed `ollama/qwen3.5:9b` while some sessions remained pinned to that model. Do not restore, recreate, or mutate unrelated provider/model state merely to make the environment appear healthy. Record the observed state and stop if the documented acceptance procedure cannot proceed within this authority.

## Hard fences

- Do not modify or merge PR #38 in this task.
- Do not create, move, or delete tag `v0.9.5`.
- Do not publish a GitHub Release.
- Do not force-push.
- Do not expose, log, copy, or mutate credentials, API keys, tokens, cookies, or secrets.
- Do not perform unrelated Scheduled Task, service, provider-routing, or configuration changes.
- Do not manually mutate Ticket, SQLite, session, transcript, or delivery state outside documented normal acceptance operations.
- Do not infer PASS from absence of failure.
- If a new genuine defect is found, stop live acceptance, reproduce it, identify root cause, make only the minimum justified repair, create a new candidate SHA, rerun candidate-sensitive validation, and report the new candidate explicitly.
- Stop and report `BLOCKED` if a required action exceeds this authority.

## Evidence contract

Every live result must bind to `345b92b4b1eac5cf8c3813de96565d6ca8b5f927` and include environment, installed version/fingerprint, commands/procedure, timestamps, provider sequence, session/Ticket/run identity, generation/ownership evidence, idle checker output, controlled-wake evidence, and evidence locations.

## Stop condition

The task ends after evidence collection/reporting or at a hard-fence boundary. Release promotion remains a separate successor decision.
