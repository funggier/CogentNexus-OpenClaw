# CNX-20260902-225 — Rollover-Prepare Attestation Producer Root-Cause Report

Date: 2026-09-02 ICT  
Task: `CNX-20260902-225`  
Parent: `CNX-20260902-224`  
Exact accepted source candidate investigated: `a812f27815b3c87b7ca748dc2dea88f987601f70`

## Disposition

`PASS_PRODUCER_ROOT_CAUSE_PROVEN__RED_REPRODUCED_AWAIT_REPAIR_REVIEW`

The retained Task-223 finalizer failure is reproducible from candidate producer semantics without requiring installer replacement mutation or manual state corruption.

Primary classification:

`SOURCE_DEFECT_NONATOMIC_ATTESTATION`

`prepare_plugin_rollover_transaction()` can successfully return a transaction whose `retiredProjectTreeSha256` and `backupProjectTreeSha256` disagree when the retired project tree changes after backup copy but before source-tree attestation. The current prepare path does not verify source/backup full-tree equivalence before authorizing the transaction.

A deterministic TDD RED now reproduces exactly that condition while proving the plugin payload fingerprints remain equal.

No production/source repair was made in Task 225 because the task stop boundary requires independent review after RED.

## Fresh authority gate

Before repository changes, GitHub remained authoritative and showed:

- branch: `agent/v0.9.3-full-stabilization`;
- active task: `CNX-20260902-225`;
- public `v0.9.3` immutable at `26ce64a624255278a3a0266ad38746e0e6ed2e31`;
- accepted candidate: `a812f27815b3c87b7ca748dc2dea88f987601f70`;
- accepted candidate payload fingerprint: `e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`;
- Discord budget: `0 Sends`.

The branch HEAD immediately before the accepted RED harness correction was `007d6bfd24f8fdd00e7d36b4adb468dfaf8cdcb9`; the corrected RED commit is `f93d78324decf44cdccdeae3a9efe30636b681a8`.

## Parent retained evidence

Task 224 accepted these Task-223 retained values:

```text
backup tree actual:             7394401cb0ae9791c1c9b98661a9bf9df47ecb83c0b139b46cd742b17ee7342a
backupProjectTreeSha256:        7394401cb0ae9791c1c9b98661a9bf9df47ecb83c0b139b46cd742b17ee7342a
retiredProjectTreeSha256:       ca74a262293d49b058fce6221db2fa5311214cde567ebb331ff845670c5a2cab
backup payload fingerprint:     f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
retiredFingerprint:             f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
```

Therefore the retained state has the same structural signature as the deterministic reproduction:

```text
payload(source) == payload(backup)
project-tree(source) != project-tree(backup)
```

Task 225 does not claim that the deterministic test identifies the exact real-world actor that changed Task-223's retired tree. It proves that candidate prepare is capable of emitting exactly this internally inconsistent transaction from an otherwise valid payload state and therefore cannot safely attribute the retained failure to external/manual corruption alone.

## Exact producer ordering

Candidate `prepare_plugin_rollover_transaction()` performs the relevant operations in this order:

```python
retired_payload = _plugin_payload(retired_plugin)
retired_project = _plugin_project_root(retired_plugin)
...
shutil.copytree(retired_project, backup_path)
...
return {
    ...
    "retiredFingerprint": retired_payload["fingerprint"],
    "retiredProjectTreeSha256": _project_tree_sha256(retired_project),
    "backupProjectTreeSha256": _project_tree_sha256(backup_path),
    ...
}
```

The source project-tree SHA is not captured before the copy. It is captured **after** backup creation, and the backup project-tree SHA is captured separately afterward.

Consequently there is a producer observation window:

```text
T0 payload fingerprint retired source observed
T1 copytree(retired_project -> backup_path)
T2 source project-tree SHA observed
T3 backup project-tree SHA observed
T4 transaction serialized/returned
```

A non-payload source change between T1 and T2 can produce:

```text
retiredFingerprint == backup payload fingerprint
retiredProjectTreeSha256 != backupProjectTreeSha256
```

The prepare function currently returns that transaction rather than rejecting it.

## Finalizer contract

Candidate finalizer checks:

```python
backup_tree = _project_tree_sha256(backup_path)
if backup_tree != transaction["backupProjectTreeSha256"]:
    raise RuntimeError("pre-install owned-generation backup proof failed")
if backup_tree != transaction["retiredProjectTreeSha256"]:
    raise RuntimeError("pre-install backup no longer matches the retired generation")
```

Thus the producer can authorize a transaction which the finalizer is guaranteed to reject even before considering replacement ownership predicates.

The finalizer remains safety-correct to fail closed. The defect is that prepare does not establish the equivalence invariant required by finalize before returning success.

## Hash-boundary inclusion matrix

### Plugin payload fingerprint

`_plugin_payload()` fingerprints npm package payload material derived from:

- `package.json`;
- paths declared by `package.json.files`;
- recursively included regular file bytes and relative paths under those declarations.

Declared payload path validation rejects symlink/reparse indirection at the payload boundary.

### Full project-tree SHA

`_project_tree_sha256()` traverses the complete project root and includes:

- directories by relative path and `type=directory`;
- regular files by relative path, type, size, and bytes SHA-256;
- symlinks/junction-like entries by relative path, link type, and target;
- entries not named by `package.json.files`.

It does not rely on file mtime as proof material.

### Comparison

| Entry/property | payload fingerprint | project-tree SHA |
| --- | --- | --- |
| `package.json` | yes | yes |
| declared `package.json.files` regular files | yes | yes |
| non-declared regular files in project root | no | yes |
| non-declared directories | no | yes |
| non-declared symlink/reparse entries | no | yes |
| regular-file content bytes | yes for payload files | yes for all project files |
| relative path identity | yes for payload files | yes for all project entries |
| file size | indirect through content digest | explicit for project files |
| mtime | no | no |
| mode bits | no | no |

This boundary difference explains why equal payload fingerprints do not establish equality of full project-tree attestations.

## Additional copy-semantic hazard

There is a separate design hazard in the same producer path: candidate uses default `shutil.copytree(retired_project, backup_path)`, whose default `symlinks=False` follows symbolic links when copying, while `_project_tree_sha256()` represents link-like entries as links/targets rather than as dereferenced regular-file content.

Therefore a stable non-payload link-like entry can, depending on platform/link type and copy semantics, also make a source tree and copied backup represent different structures. This report does not classify that as the retained Task-223 primary cause because retained source-tree entry inventory sufficient to prove an actual link actor was unavailable. It is nevertheless a repair-design requirement: the successor must either reject unsupported link/reparse material before prepare or make copy/attestation semantics structurally consistent.

## Retained Windows evidence limitation

The configured Windows/LConnect resource was not operational in this ChatGPT session: discovery exposed it but invocation returned resource-not-found. No claim is made that Task 225 re-read or modified the retained Windows tree live.

This prevents direct attribution of Task-223's real-world changing path/actor beyond evidence already preserved in Task 224. It does **not** block source-defect proof because the candidate producer behavior is deterministic and independently reproduced in repository CI.

## TDD RED

### First harness attempt — rejected as invalid RED

Commit:

`007d6bfd24f8fdd00e7d36b4adb468dfaf8cdcb9`

The first hook monkeypatched `shutil.copytree` globally and therefore also intercepted recursive subdirectory copies. That unintentionally changed material inside the package payload boundary. GitHub Actions correctly failed earlier at payload fingerprint equality.

This run was rejected as a valid RED because it did not isolate the intended variable.

Example Validate run:

`33616772399`

Ubuntu/Python 3.11 job `100204384720` reported:

```text
1 failed, 475 passed, 33 skipped, 4 subtests passed
```

but failure was the payload-fingerprint equality assertion, so it is not accepted as proof of the target defect.

### Corrected deterministic RED — accepted

Commit:

`f93d78324decf44cdccdeae3a9efe30636b681a8`

File:

`tests/test_task225_rollover_prepare_attestation.py`

The corrected hook mutates the non-payload file exactly once, only after the top-level retired-project copy completes.

The test proves, in this order:

1. current prepare accepts a valid direct plugin layout;
2. a regular file outside `package.json.files` changes after top-level copy;
3. source and backup payload fingerprints remain equal;
4. prepare still returns a transaction;
5. returned `retiredProjectTreeSha256` and `backupProjectTreeSha256` differ.

GitHub Actions Validate:

- run: `33616947769`;
- Ubuntu/Python 3.11 job: `100204920420`;
- all setup, baseline, namespace, validation, self-test, workflow self-test, and py_compile steps passed before pytest;
- pytest failed only at the intended Task-225 tree-attestation equality assertion.

Observed RED:

```text
source payload fingerprint == backup payload fingerprint   PASS
retiredProjectTreeSha256 == backupProjectTreeSha256        FAIL

retiredProjectTreeSha256 = 8585b2996bdca0556e9fdeee247029f3c5fb3351904868ee35688edb4f81f434
backupProjectTreeSha256  = d5208599edc96303982ce80da590a337932655bc3f1513a4c57f3974f98c324c

1 failed, 475 passed, 33 skipped, 4 subtests passed
```

PS5.1 Acceptance Smoke for the corrected RED commit completed successfully as run `33616947804`, showing the test-only change did not break that independent smoke path.

The Validate workflow is intentionally RED at this task boundary; it must not be interpreted as an unrelated CI regression.

## Root-cause classification

Primary:

`SOURCE_DEFECT_NONATOMIC_ATTESTATION`

Proven producer operation/order permitting mismatch:

```text
copy retired project
    -> source may change
hash retired source tree
hash backup tree
return transaction without equality gate
```

Proven differing boundary class:

`non-package-payload regular project-root material`

State validity for the deterministic reproduction:

- canonical direct plugin layout;
- valid package identity/version;
- valid payload paths;
- non-payload project-root regular file accepted by current validator;
- no source/backup payload fingerprint transition;
- no installer replacement mutation required.

Candidate source safety assessment:

- finalizer: safety-correct fail closed;
- prepare: insufficiently safe because it can emit an internally unfinalizable transaction instead of failing before installer mutation.

Production repair required: `YES`.

## Smallest repair principle for successor review

The repair must establish the finalizer's source/backup full-tree equivalence invariant **inside prepare before a transaction is returned**.

At minimum, after backup creation the producer must compute source and backup tree attestations once, compare them, and fail closed if they differ rather than serialize inconsistent values.

The repair review must also adjudicate link/reparse semantics so a stable supported tree cannot be transformed structurally by backup copy while being attested under different semantics.

No implementation is authorized by Task 225 itself.

## Mutation ledger

```text
live installer invocations: 0
live rollover-prepare invocations: 0
live rollover-finalize invocations: 0
manual lifecycle actions: 0
Gateway restarts: 0
live plugin/config mutations: 0
live ownership/transaction/backup repairs: 0
SQLite writes: 0
process terminations: 0
provider/model substitutions: 0
Discord Sends/API semantic traffic: 0
Release/tag/asset mutations: 0
force pushes/history rewrites: 0
```

Repository mutations performed:

```text
007d6bfd24f8fdd00e7d36b4adb468dfaf8cdcb9  test: reproduce rollover prepare attestation race
f93d78324decf44cdccdeae3a9efe30636b681a8  test: isolate top-level rollover prepare attestation race
```

No production file was changed.

## Required next step

Independent ChatGPT review must assess Task 225 and, if accepted, open a bounded successor repair task that:

1. preserves this deterministic RED;
2. implements the minimum fail-closed prepare invariant;
3. explicitly resolves symlink/junction/reparse backup semantics;
4. obtains GREEN for the targeted test and relevant regression suite;
5. obtains fresh GitHub Actions GREEN before any live Windows installer retry is authorized.
