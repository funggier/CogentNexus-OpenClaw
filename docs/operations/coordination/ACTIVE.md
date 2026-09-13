# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `V0.9.5_FINAL_ACCEPTANCE_SUCCESSOR`
Execution mode: `SINGLE_EXECUTOR__ROOT_CAUSE_TDD`
Task ID: `CNX-20260913-318`
Parent: `CNX-20260913-317`
Executor: `Hermes`
Reviewer: `ChatGPT`
Release candidate: `2a1be3b5c2e95664da97f2aea103a57a4947fd9d`
Candidate branch: `fix/v0.9.5-final-acceptance-installer-cli`
Authority branch: `coord/v0.9.5-final-acceptance`

## Objective

Complete candidate-sensitive requalification and final v0.9.5 live acceptance against the successor candidate after the acceptance branch advanced beyond the previously authorized candidate.

## Authorized scope

Hermes is authorized to verify the exact successor candidate, run candidate-sensitive repository validation, restore or verify a healthy acceptance runtime using only bounded supported diagnostics/recovery, install-over the exact successor candidate, verify installed provenance/fingerprint and runtime health, execute Provider Switch Acceptance, Idle Quiescence Acceptance for at least two supervisor cadences, Controlled Actionable Wake with exactly one durable work item, and collect auditable evidence.

## Required order

1. Verify candidate SHA is exactly `2a1be3b5c2e95664da97f2aea103a57a4947fd9d`.
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

## Candidate delta

The successor is two commits ahead of `434b2718`:

```text
8ce1ef3a  test: cover canonical v0.9.5 installer state
2a1be3b5  fix: accept canonical v0.9.5 controller state
```

The delta adds a regression test and updates `scripts/install.ps1` to recognize canonical `cnxMode` without mutating controller state.

## Evidence contract

Every live result must bind to `2a1be3b5c2e95664da97f2aea103a57a4947fd9d` and include environment, installed version/fingerprint, commands/procedure, timestamps, provider sequence, session/Ticket/run identity, generation/ownership evidence, idle checker output, controlled-wake evidence, and evidence locations.

## Stop condition

The task ends after evidence collection/reporting or at a hard-fence boundary. Release promotion remains a separate successor decision.
