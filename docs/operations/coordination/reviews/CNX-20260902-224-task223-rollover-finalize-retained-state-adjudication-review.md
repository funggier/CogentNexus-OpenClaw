# Independent Review — CNX-20260902-224 Task-223 Rollover-Finalize Retained-State Adjudication

Date: 2026-09-02 ICT  
Coordinator / final reviewer: ChatGPT

## Verdict

`ACCEPT_PASS_FINALIZE_ROOT_CAUSE_PROVEN__TRANSACTION_INCONSISTENCY_PRODUCER_ADJUDICATION_REQUIRED`

Task 224 is accepted as a valid read-only diagnostic closure for the **first failing finalizer predicate**. It correctly proves that the retained Task-223 transaction cannot pass candidate finalization because the backup tree attestation is internally inconsistent.

This review does **not** accept the stronger conclusion that the ultimate root cause is necessarily external state drift. The retained transaction was produced by candidate `rollover-prepare`; therefore the next bounded task must determine why the producer emitted two different full-tree attestations for the retired generation and its immediately-created backup.

No live completion, installer retry, rollover-finalize invocation, lifecycle action, or Discord semantic traffic is authorized by this review.

## Accepted first-failure evidence

Task 224 reported:

```text
backup tree actual:             7394401cb0ae9791c1c9b98661a9bf9df47ecb83c0b139b46cd742b17ee7342a
backupProjectTreeSha256:        7394401cb0ae9791c1c9b98661a9bf9df47ecb83c0b139b46cd742b17ee7342a
retiredProjectTreeSha256:       ca74a262293d49b058fce6221db2fa5311214cde567ebb331ff845670c5a2cab
backup payload fingerprint:     f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
retiredFingerprint:             f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
```

The exact candidate finalizer checks, in order:

```python
if backup_tree != transaction["backupProjectTreeSha256"]:
    raise RuntimeError("pre-install owned-generation backup proof failed")
if backup_tree != transaction["retiredProjectTreeSha256"]:
    raise RuntimeError("pre-install backup no longer matches the retired generation")
```

Therefore:

1. prepared backup self-attestation passes;
2. retired-generation equivalence attestation fails;
3. this is the first proven pre-write failure;
4. the finalizer is safety-correct to fail closed for the retained transaction as written.

Task 224 also correctly separates this from the historical Task-143 same-path path-identity defect and Task-144 noncanonical lexical registration defect.

## Accepted preservation boundary

Task 224 remained read-only with respect to the live semantic/product state. Accepted preservation includes:

- controller remains PASSTHROUGH generation 33;
- startup adapter remains absent;
- Gateway and Ollama remain healthy;
- Delivery/Recovery remain READY and read-only;
- SQLite integrity remains `ok`;
- installed candidate fingerprint remains exact `e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`;
- no installer/finalizer/lifecycle invocation;
- no process termination;
- no Discord Send/API semantic traffic;
- no Release/tag/asset mutation.

The missing retained matching inventory file is an evidence gap, but it is not the first failing predicate because the current read-only reconstruction reaches the earlier backup/tree mismatch with canonical direct registration otherwise coherent.

## Why another root-cause task is required

The candidate prepare path creates the backup and only then records both tree attestations:

```python
shutil.copytree(retired_project, backup_path)
...
"retiredProjectTreeSha256": _project_tree_sha256(retired_project),
"backupProjectTreeSha256": _project_tree_sha256(backup_path),
```

For a stable retired tree, those two values should be identical immediately after the copy. The retained Task-223 transaction proves they were not.

At least three materially different explanations remain possible and must not be conflated:

1. **legitimate concurrent retired-tree mutation** between/during backup copy and attestation;
2. **producer/source defect** because prepare does not obtain an atomic or stable snapshot before emitting mutually-dependent attestations;
3. **tree-hash/copy semantic mismatch** such as a file class, reparse behavior, mutable generated file, or timing-sensitive entry that causes source and backup trees to differ while the plugin payload fingerprint remains identical.

The fact that `backup payload fingerprint == retiredFingerprint` while full project-tree hashes differ is especially important. It suggests the differing material may be outside the payload fingerprint boundary, but that must be proven from exact candidate helper semantics and reproducible evidence rather than inferred.

Task 224 therefore closes the finalizer failure location, but not yet the producer-side origin of the inconsistent transaction evidence.

## Required successor

Open Task 225 as an **offline/read-only transaction-attestation producer root-cause adjudication**.

It must:

1. keep all Task-223 retained live state untouched;
2. inspect exact candidate `prepare_plugin_rollover_transaction()` and all tree/payload helper semantics;
3. establish the exact ordering from retired-tree observation through `copytree` and transaction serialization;
4. identify which file classes are included by `_project_tree_sha256` versus plugin payload fingerprinting;
5. use retained backup evidence to enumerate any non-payload entries capable of changing the full-tree hash;
6. inspect Task-223 timestamps/logs for evidence of concurrent OpenClaw/npm/plugin filesystem activity during prepare;
7. reproduce the mismatch offline with the smallest deterministic test if possible;
8. distinguish external unsupported mutation from a valid-state race/non-atomic attestation defect;
9. if and only if a source defect is proven, produce a genuine RED test before any production change and stop at the repair authorization boundary unless the task explicitly permits the minimal repair;
10. publish a report and stop for independent review.

## Runtime / Discord boundary

Until Task 225 is independently reviewed:

```text
installer retry: 0
rollover-finalize invocation: 0
rollover-prepare invocation against live state: 0
manual ownership/transaction/backup repair: 0
cnxclaw lifecycle actions: 0
OpenClaw plugin mutation: 0
Gateway restart: 0
SQLite writes: 0
provider/model substitution: 0
process termination: 0
Discord Sends/API semantic traffic: 0
Release/tag/asset mutation: 0
force push/history rewrite: forbidden
```

Repository-side diagnostic tests/scripts are permitted only inside Task 225's explicit offline scope. Production/source repair remains gated on a proven root cause and RED reproduction.

## Disposition

`ACCEPT_PASS_FINALIZE_ROOT_CAUSE_PROVEN__TRANSACTION_INCONSISTENCY_PRODUCER_ADJUDICATION_REQUIRED`
