# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `V0.9.5_FINAL_ACCEPTANCE`
Execution mode: `SINGLE_EXECUTOR__ROOT_CAUSE_TDD`
Task ID: `CNX-20260913-316`
Parent: `CNX-20260913-V095-FINALIZATION-BLOCKED`
Executor: `Hermes`
Reviewer: `ChatGPT`
Release candidate: `a986f3261b1570d1bcb1574d2458fe7068207a9c`
Candidate branch: `feat/v0.9.5-release-readiness-clean`
Authority branch: `coord/v0.9.5-final-acceptance`

## Objective

Provide a durable, auditable authority for final v0.9.5 live acceptance against the frozen candidate. The purpose of this task is to collect the missing runtime evidence needed to resolve the release blockers without mutating the frozen candidate or promoting the release prematurely.

## Authorized scope

Hermes is explicitly authorized to perform the following bounded live actions on the acceptance machine:

- install-over the exact candidate `a986f3261b1570d1bcb1574d2458fe7068207a9c` using a supported repository-defined installation path;
- verify installed version, provenance, and candidate fingerprint before acceptance;
- enable/activate the CogentNexus-OpenClaw plugin when required by the supported acceptance procedure;
- run the live Provider Switch Acceptance defined by `docs/operations/acceptance/V095_PROVIDER_SWITCH_ACCEPTANCE.md`;
- observe idle behavior for the required supervisor cadences and run the idle-quiescence evidence checker;
- perform the required controlled actionable wake with exactly one durable work item;
- collect raw logs, checker output, identity evidence, timestamps, and final PASS/FAIL/INDETERMINATE verdicts;
- create or update an evidence report on a report/evidence branch derived from this authority branch.

These permissions are explicit and supersede the previous blocker caused by the absence of a `READY_FOR_HERMES` authority. They do not authorize release promotion.

## Required execution order

1. Fresh-fetch this authority branch and the frozen candidate.
2. Inspect current installed provenance and verify the target machine is within scope.
3. Install-over the exact candidate through the supported path and verify the installed fingerprint.
4. Enable the plugin through the supported path and verify runtime health.
5. Execute Provider Switch Acceptance.
6. Execute Idle Quiescence Acceptance for at least two supervisor cadences.
7. Execute Controlled Actionable Wake with one durable work item.
8. Preserve raw evidence and update the final acceptance report.
9. Re-check candidate immutability and report all outcomes.
10. Stop before merge, tag, GitHub Release, or other release promotion.

## Hard fences

- Do not modify `a986f3261b1570d1bcb1574d2458fe7068207a9c` or its candidate branch unless a separately proven defect requires a new candidate and requalification.
- Do not merge PR #38.
- Do not create or move the `v0.9.5` tag.
- Do not publish a GitHub Release.
- Do not mutate or expose credentials, API keys, tokens, cookies, or secrets.
- Do not perform unrelated configuration, scheduled-task, service, Gateway, provider-routing, or system maintenance.
- Do not manually mutate Ticket, SQLite, session, transcript, or delivery state except through the documented acceptance procedure's normal supported operations.
- Do not classify missing evidence as PASS.
- If a destructive or broader action is required beyond this scope, stop and report `BLOCKED` with the exact boundary.

## Evidence contract

The final report must bind every live result to the exact candidate SHA and include environment, installed version/fingerprint, provider sequence, session/Ticket/run identity, generation/ownership evidence, idle checker output, controlled-wake evidence, timestamps, commands/procedure, and explicit verdicts.

The final release status must remain `BLOCKED` unless every required acceptance gate is directly proven PASS. This task itself does not authorize merge or release promotion.
