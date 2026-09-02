# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK225_ROLLOVER_PREPARE_ATTESTATION_PRODUCER_ROOT_CAUSE`  
**Updated:** 2026-09-02 ICT  
**Transport:** GitHub repository + authenticated read-only Windows retained-state evidence through Hermes  
**Active task:** `CNX-20260902-225`  
**Parent:** `CNX-20260902-224`  
**Repair parent:** `CNX-20260831-198`  
**Parent umbrella:** `CNX-20260831-188`  
**Completed publication:** `CNX-20260831-197`  
**Disposition:** `TASK224_ACCEPTED__TASK225_PRODUCER_ROOT_CAUSE_READY`

## Publication and candidate authority

Published public `v0.9.3` remains untouched at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Exact accepted candidate remains:

`a812f27815b3c87b7ca748dc2dea88f987601f70`

Exact accepted payload fingerprint remains:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

## Task 224 accepted boundary

Task-224 report disposition:

`PASS_FINALIZE_ROOT_CAUSE_PROVEN__STATE_EVIDENCE_REPAIR_REQUIRED`

Independent review disposition:

`ACCEPT_PASS_FINALIZE_ROOT_CAUSE_PROVEN__TRANSACTION_INCONSISTENCY_PRODUCER_ADJUDICATION_REQUIRED`

Accepted first failing finalizer predicate:

```text
backup_tree == backupProjectTreeSha256   PASS
backup_tree == retiredProjectTreeSha256  FAIL
```

Accepted retained values:

```text
backup tree:               7394401cb0ae9791c1c9b98661a9bf9df47ecb83c0b139b46cd742b17ee7342a
backupProjectTreeSha256:   7394401cb0ae9791c1c9b98661a9bf9df47ecb83c0b139b46cd742b17ee7342a
retiredProjectTreeSha256:  ca74a262293d49b058fce6221db2fa5311214cde567ebb331ff845670c5a2cab
```

The candidate finalizer is safety-correct to fail closed for that transaction. Task 224 does not prove why `rollover-prepare` produced inconsistent source/backup full-tree attestations.

## Active Task 225

Hermes must execute:

`docs/operations/coordination/tasks/CNX-20260902-225-rollover-prepare-attestation-producer-root-cause.md`

Required outcome:

- trace exact prepare/copy/hash/serialization ordering;
- compare project-tree and payload-fingerprint boundaries;
- inspect retained backup and Task-223 timing evidence;
- perform isolated offline single-hypothesis reproduction only;
- classify supported concurrent mutation vs unsupported mutation vs non-atomic attestation defect vs tree/copy semantic mismatch;
- add a genuine deterministic RED only if a source defect is sufficiently proven;
- publish report and stop for independent review.

## Runtime / Discord boundary

`0 Discord Sends`.

Task 225 permits no installer retry, live rollover prepare/finalize, lifecycle command, OpenClaw plugin mutation, Gateway restart, ownership/transaction/backup/SQLite write, provider/model substitution, process termination, Release/tag mutation, or force push.
