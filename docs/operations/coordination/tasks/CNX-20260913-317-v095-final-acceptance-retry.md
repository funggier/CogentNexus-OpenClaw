# CNX-20260913-317 — v0.9.5 Final Acceptance Retry

Status: `READY_FOR_HERMES`
Executor: `Hermes`
Reviewer: `ChatGPT`

Current repaired candidate:

`434b27185f7afd17d8cffeede9c016378df0a6aa`

Repair branch:

`fix/v0.9.5-final-acceptance-installer-cli`

## Authority

The previous final-acceptance task `CNX-20260913-316` is superseded because its exact-candidate install exposed a real installer defect, which was repaired through a test-first sequence. This task is the durable successor authority for retrying live acceptance against the repaired candidate.

## Authorized work

Hermes is authorized to diagnose the previously observed OpenClaw Gateway restart/probe timeout using bounded diagnostics first; use the minimum supported recovery path required for a healthy acceptance runtime; install-over and verify the exact repaired candidate; enable the plugin through the supported path; and execute the documented Provider Switch, Idle Quiescence, and Controlled Actionable Wake acceptance procedures.

Required idle evidence:

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

## Required execution order

1. Inspect current installation, Gateway state, and provenance.
2. Diagnose the known Gateway restart/probe timeout with bounded diagnostics.
3. Use only the minimum supported recovery required for a healthy acceptance runtime.
4. Install-over the exact repaired candidate and verify installed version/provenance/fingerprint.
5. Enable the plugin through the supported path and verify health.
6. Execute Provider Switch Acceptance.
7. Execute Idle Quiescence for at least two supervisor cadences.
8. Execute Controlled Actionable Wake with exactly one durable work item.
9. Preserve raw evidence and update the acceptance report.
10. Re-check candidate identity and report all outcomes.
11. Stop before PR #38 modification, merge, tag, or GitHub Release.

## Evidence contract

Every result must bind to candidate `434b27185f7afd17d8cffeede9c016378df0a6aa` and include environment, installed fingerprint, commands/procedure, timestamps, provider sequence, session/Ticket/run identity, generation/ownership evidence, idle checker output, controlled-wake evidence, and evidence locations.

## Hard fences

- No modification or merge of PR #38 in this task.
- No creation, movement, or deletion of tag `v0.9.5`.
- No GitHub Release publication.
- No force-push.
- No credential or secret exposure/change.
- No unrelated Scheduled Task, service, provider-routing, Gateway, or configuration mutation.
- No manual Ticket/SQLite/session/transcript/delivery mutation outside documented normal acceptance operations.
- Do not infer PASS from absence of failure.
- Stop and report `BLOCKED` if an action exceeds this authority.

## Defect handling

If a new genuine defect is discovered, reproduce it, identify root cause, make only the minimal justified repair, create a new candidate SHA, rerun candidate-sensitive validation, and report the new candidate explicitly.
