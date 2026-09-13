# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `V0.9.5_FINAL_ACCEPTANCE_RETRY`
Execution mode: `SINGLE_EXECUTOR__ROOT_CAUSE_TDD`
Task ID: `CNX-20260913-317`
Parent: `CNX-20260913-316`
Executor: `Hermes`
Reviewer: `ChatGPT`
Release candidate: `434b27185f7afd17d8cffeede9c016378df0a6aa`
Candidate branch: `fix/v0.9.5-final-acceptance-installer-cli`
Authority branch: `coord/v0.9.5-final-acceptance`

## Objective

Retry final v0.9.5 live acceptance against the repaired candidate after a real installer defect was reproduced and minimally repaired. The previous candidate remains historical evidence and is not the release target.

## Authorized scope

Hermes is authorized to diagnose the previously observed OpenClaw Gateway restart/probe timeout using bounded read-only diagnostics first; use the minimum supported recovery path required to restore a healthy acceptance runtime; install-over the exact repaired candidate; verify installed provenance/fingerprint; enable the plugin through the supported path; execute Provider Switch Acceptance, Idle Quiescence Acceptance for at least two supervisor cadences, and Controlled Actionable Wake with exactly one durable work item; and collect auditable evidence.

## Required order

1. Inspect current installation, Gateway state, and provenance.
2. Diagnose the known Gateway restart/probe timeout with bounded diagnostics.
3. Use only the minimum supported recovery required for a healthy acceptance runtime.
4. Install-over and verify the exact repaired candidate.
5. Enable the plugin through the supported path and verify runtime health.
6. Execute Provider Switch Acceptance.
7. Execute Idle Quiescence for >=2 supervisor cadences.
8. Execute Controlled Actionable Wake with exactly one durable work item.
9. Preserve raw evidence and update the report.
10. Re-check candidate identity and report all outcomes.
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
- Stop and report `BLOCKED` if a required action exceeds this authority.

## Candidate defect handling

The repaired candidate is:

`434b27185f7afd17d8cffeede9c016378df0a6aa`

Repair sequence:

```text
b2c7b0bb  RED test
c1401f56  minimal installer fix
434b2718  updated installer contract test
```

If a new genuine defect is discovered: reproduce it, identify root cause, make only the minimal justified repair, create a new candidate SHA, rerun required candidate-sensitive validation, and report the new candidate explicitly.

## Evidence contract

Every live result must bind to `434b27185f7afd17d8cffeede9c016378df0a6aa` and include environment, installed version/fingerprint, commands/procedure, timestamps, provider sequence, session/Ticket/run identity, generation/ownership evidence, idle checker output, controlled-wake evidence, and evidence locations.

## Stop condition

The task ends after evidence collection/reporting or at a hard-fence boundary. Release promotion remains a separate successor decision.