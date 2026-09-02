# Active Coordination Task

Status: `IN_PROGRESS`
Execution mode: `TASK226_ROLLOVER_PREPARE_ATTESTATION_FAIL_CLOSED_REPAIR`
Current disposition: `TASK225_ACCEPTED__BOUNDED_TDD_REPAIR_AUTHORIZED`
Task ID: `CNX-20260902-226`
Parent task: `CNX-20260902-225`
Repair parent: `CNX-20260831-198`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-02 ICT
Executor: ChatGPT repository repair
Coordinator / final reviewer: ChatGPT

## Published authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No Release/tag/asset mutation is authorized.

## Accepted candidate authority

Repair baseline source candidate remains:

`a812f27815b3c87b7ca748dc2dea88f987601f70`

Accepted payload fingerprint remains:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

## Task-225 accepted result

Report:

`reports/CNX-20260902-225-rollover-prepare-attestation-producer-root-cause.md`

Independent review:

`reviews/CNX-20260902-225-rollover-prepare-attestation-producer-root-cause-review.md`

Accepted root cause:

`SOURCE_DEFECT_NONATOMIC_ATTESTATION`

Accepted deterministic RED lineage:

```text
f93d78324decf44cdccdeae3a9efe30636b681a8
Validate run 33616947769
Ubuntu/Python 3.11 job 100204920420
```

## Active Task 226

Execute:

`tasks/CNX-20260902-226-rollover-prepare-attestation-fail-closed-repair.md`

Required behavior:

- refine the regression to require explicit fail-closed prepare behavior;
- prove current source RED;
- minimally compute and compare retired/backup full-tree attestations before transaction success;
- preserve existing finalizer predicates and full-tree proof coverage;
- obtain targeted and full CI GREEN;
- report and stop before any live Windows installer retry.

## Runtime / Discord boundary

Task 226 is repository-only.

`0 Discord Sends`.

No live installer, live rollover prepare/finalize, lifecycle/plugin/Gateway/SQLite mutation, process termination, provider/model substitution, Release/tag mutation, or force push is authorized.
