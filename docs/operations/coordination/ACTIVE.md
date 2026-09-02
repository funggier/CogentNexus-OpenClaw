# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK225_ROLLOVER_PREPARE_ATTESTATION_PRODUCER_ROOT_CAUSE`
Current disposition: `TASK224_ACCEPTED__TRANSACTION_INCONSISTENCY_PRODUCER_ADJUDICATION_REQUIRED`
Task ID: `CNX-20260902-225`
Parent task: `CNX-20260902-224`
Repair parent: `CNX-20260831-198`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-02 ICT
Executor: Hermes / authenticated Windows forensic operator
Coordinator / final reviewer: ChatGPT

## Published authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No Release/tag/asset mutation is authorized.

## Accepted candidate authority

Exact source candidate remains:

`a812f27815b3c87b7ca748dc2dea88f987601f70`

Accepted payload fingerprint remains:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

## Task-224 reviewed result

Report:

`reports/CNX-20260902-224-task223-rollover-finalize-retained-state-adjudication.md`

Independent review:

`reviews/CNX-20260902-224-task223-rollover-finalize-retained-state-adjudication-review.md`

Accepted review disposition:

`ACCEPT_PASS_FINALIZE_ROOT_CAUSE_PROVEN__TRANSACTION_INCONSISTENCY_PRODUCER_ADJUDICATION_REQUIRED`

Accepted first failing finalizer predicate:

```text
backup_tree == backupProjectTreeSha256        PASS
backup_tree == retiredProjectTreeSha256       FAIL
```

Observed retained values:

```text
backup tree actual:       7394401cb0ae9791c1c9b98661a9bf9df47ecb83c0b139b46cd742b17ee7342a
backupProjectTreeSha256:  7394401cb0ae9791c1c9b98661a9bf9df47ecb83c0b139b46cd742b17ee7342a
retiredProjectTreeSha256: ca74a262293d49b058fce6221db2fa5311214cde567ebb331ff845670c5a2cab
```

The finalizer is safety-correct to reject that retained transaction. However the producer-side origin of the inconsistent attestations is not yet established.

## Active Task 225

Hermes must execute:

`tasks/CNX-20260902-225-rollover-prepare-attestation-producer-root-cause.md`

Task 225 must determine why candidate `rollover-prepare` copied the retired project and then recorded different full-tree hashes for the retired source and backup while the backup payload fingerprint still matched the retired payload fingerprint.

Required focus:

1. exact prepare ordering and helper semantics;
2. project-tree versus payload-fingerprint inclusion boundaries;
3. retained backup/tree evidence and Task-223 timing;
4. isolated offline reproduction of single hypotheses;
5. distinguish supported concurrent mutation, unsupported mutation, non-atomic attestation source defect, or copy/hash semantic mismatch;
6. create a deterministic RED only if a source defect is proven enough to justify it;
7. publish report and stop for independent review.

## Runtime / Discord boundary

Task 225 authorizes `0 Discord Sends` and no live installer/rollover/lifecycle mutation.

No installer retry, live rollover prepare/finalize, manual ownership/transaction/backup repair, cnxclaw lifecycle action, OpenClaw plugin mutation, Gateway restart, SQLite write, provider/model substitution, process termination, Release/tag mutation, or force push is authorized.
