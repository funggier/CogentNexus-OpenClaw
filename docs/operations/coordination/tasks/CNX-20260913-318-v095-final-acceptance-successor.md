# CNX-20260913-318 — v0.9.5 Final Acceptance Successor

Status: `READY_FOR_HERMES`
Executor: `Hermes`
Reviewer: `ChatGPT`

## Candidate

Current candidate branch: `fix/v0.9.5-final-acceptance-installer-cli`
Current candidate SHA: `2a1be3b5c2e95664da97f2aea103a57a4947fd9d`
Parent candidate: `434b27185f7afd17d8cffeede9c016378df0a6aa`

The branch advanced by two commits after the previously authorized candidate:

```text
8ce1ef3a  test: cover canonical v0.9.5 installer state
2a1be3b5  fix: accept canonical v0.9.5 controller state
```

The successor candidate must be independently requalified. Results previously bound to `434b2718` do not transfer automatically.

## Objective

Complete candidate-sensitive requalification and final live acceptance for the current candidate, while preserving the release fence.

## Required order

1. Verify candidate SHA is exactly `2a1be3b5c2e95664da97f2aea103a57a4947fd9d`.
2. Run candidate-sensitive repository validation for the successor candidate.
3. Confirm the acceptance runtime is healthy and install-over the exact successor candidate.
4. Verify installed version, provenance, fingerprint, Gateway health, plugin state, generation, and provider ownership.
5. Execute Provider Switch Acceptance.
6. Execute Idle Quiescence for >=2 supervisor cadences.
7. Execute Controlled Actionable Wake with exactly one durable work item.
8. Preserve raw evidence and publish a successor acceptance report.
9. Re-check candidate identity and all verdicts.
10. Stop before PR #38 update, merge, tag, or GitHub Release.

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
- If a new genuine defect is found, stop the live acceptance path, reproduce it, identify root cause, make only the minimum justified repair, create a new candidate SHA, and restart candidate-sensitive validation for that new candidate.

## Current known delta from previous candidate

The successor candidate adds a regression test for canonical v0.9.5 installer state and changes `scripts/install.ps1` so an existing controller with canonical `cnxMode` is mapped to the installer boundary mode (`disabled -> passthrough`, `active -> managed`, `maintenance -> maintenance`) without mutating state.

## Evidence contract

Every live result must bind to the exact successor candidate SHA and include environment, installed version/fingerprint, commands/procedure, timestamps, provider sequence, session/Ticket/run identity, generation/ownership evidence, idle checker output, controlled-wake evidence, and evidence locations.

## Release state

PR #38 remains open and must remain untouched by this task. Merge, tag, and publication are separate successor decisions after acceptance evidence and candidate-sensitive CI are green.
