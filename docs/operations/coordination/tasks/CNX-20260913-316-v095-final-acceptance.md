# CNX-20260913-316 — v0.9.5 Final Live Acceptance

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260913-V095-FINALIZATION-BLOCKED`  
Executor: `Hermes`  
Reviewer: `ChatGPT`

## Authority

This is the successor coordination authority for the v0.9.5 final acceptance work.

The previous coordination state was explicitly `COMPLETED` and required future work to use a new task/branch. This task and its authority branch now provide the required durable `READY_FOR_HERMES` continuation trigger.

The frozen release candidate is:

`a986f3261b1570d1bcb1574d2458fe7068207a9c`

Candidate branch:

`feat/v0.9.5-release-readiness-clean`

Authority branch:

`coord/v0.9.5-final-acceptance`

## Objective

Resolve the remaining v0.9.5 finalization blockers by collecting direct, auditable live acceptance evidence on the exact frozen candidate.

Current known automated validation state is green. Remaining gates are:

- live Provider Switch Acceptance;
- Idle Quiescence Acceptance;
- Controlled Actionable Wake evidence.

## Explicit authorization

Hermes is authorized to perform bounded live operations required by the documented acceptance procedures, including:

1. install-over the exact candidate through a supported repository-defined installation path;
2. verify installed version, provenance, and candidate fingerprint;
3. enable/activate the CogentNexus-OpenClaw plugin through its supported path;
4. execute `docs/operations/acceptance/V095_PROVIDER_SWITCH_ACCEPTANCE.md`;
5. observe idle behavior for at least two supervisor cadences and run the available read-only idle-quiescence checker;
6. execute the controlled actionable wake defined by the acceptance procedure with exactly one durable work item;
7. collect raw logs, checker outputs, identity/ownership evidence, timestamps, and verdicts;
8. create or update the final acceptance evidence report on an appropriate report/evidence branch;
9. verify candidate immutability after acceptance.

This authorization is sufficient to overcome the previous lack of a `READY_FOR_HERMES` continuation trigger.

## Required execution order

### Phase A — Target preparation

- Fresh-fetch this authority branch.
- Fresh-fetch the exact candidate.
- Inspect installed provenance before mutation.
- Confirm the target runtime is the intended acceptance machine.
- Install-over only the exact candidate through the supported install path.
- Verify installed version/fingerprint against the candidate before proceeding.
- Enable the plugin through the supported path.
- Verify runtime health and establish a clean acceptance baseline.

### Phase B — Provider Switch

Execute the documented provider-switch acceptance procedure.

Record, at minimum:

- candidate SHA;
- installed version/fingerprint;
- provider/model before and after each switch;
- logical session key;
- session generation;
- Ticket ID and run ID;
- Ticket state;
- plugin state;
- Gateway lifecycle state;
- CNX policy/identity fields that are safe to record;
- delivery result;
- recovery result;
- exact timestamps and commands/procedure.

Do not record credentials, API keys, tokens, cookies, or other secrets.

PASS requires direct evidence that provider switching does not itself create CNX identity drift, alter generation unexpectedly, change policy ownership, trigger unintended lifecycle mutation, or bypass OpenClaw-owned provider/auth routing.

### Phase C — Idle Quiescence

Execute the documented idle-quiescence acceptance procedure.

At minimum collect evidence covering two supervisor cadences and prove:

```text
wakeReason=idle/no-actionable-work
heavyPath=false
heavySupervisorCalls=0
providerRecoveryActions=0
configMutations=0
gatewayLifecycleActions=0
idleTicks>=2
```

The checker verdict must be `PASS` for acceptance.

Missing or unusable evidence is `INDETERMINATE`, not PASS.

### Phase D — Controlled Actionable Wake

Create or expose exactly one durable actionable work item through the supported workflow.

Prove:

- exactly one effective wake;
- no duplicate/second owner;
- correct ownership/session generation;
- correct durable Ticket/work identity;
- correct delivery settlement.

Retain relevant evidence such as Delivery ID, Ticket ID, owner session key, generation, lease, and wake count when applicable and safe.

## Evidence rules

Every result must be explicitly bound to:

`a986f3261b1570d1bcb1574d2458fe7068207a9c`

A result from another candidate does not qualify.

Every gate must be classified as:

`PASS` / `FAIL` / `INDETERMINATE`

Never infer PASS from the absence of an observed failure.

## Defect handling

If a genuine candidate defect is discovered:

1. reproduce it;
2. identify root cause;
3. make only the minimal justified repair;
4. create a new candidate SHA;
5. rerun all required candidate-sensitive validation;
6. explicitly retire the old candidate as the release target;
7. report the new candidate and evidence.

Do not modify the frozen candidate merely to remove an evidence blocker.

## Hard fences

No authority is granted here for:

- merging PR #38;
- creating, moving, or deleting `v0.9.5` tags;
- publishing a GitHub Release;
- force pushing;
- exposing or changing credentials/secrets;
- unrelated configuration changes;
- unrelated Scheduled Task or service changes;
- manual Ticket/SQLite/session/transcript/delivery mutation outside the normal documented acceptance workflow;
- destructive cleanup outside the supported installation/acceptance path.

If a required step exceeds these bounds, stop and report `BLOCKED` with the exact boundary.

## Stop condition

Once live acceptance evidence has been collected and the final evidence report has been updated, stop before release promotion.

The next decision is a separate final-review/release-closure step.

## Required final report

The report must include:

```text
Repository
Candidate SHA
Authority task/branch
Installed version/fingerprint
Provider Switch verdict
Idle Quiescence verdict
Controlled Wake verdict
Automated Validation status
Finalization status
Evidence locations
Remaining blockers
```

At the end of this task, do not claim the release is merged, tagged, or published.
