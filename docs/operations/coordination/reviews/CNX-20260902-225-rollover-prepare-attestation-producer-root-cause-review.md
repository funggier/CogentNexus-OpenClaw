# Independent Review — CNX-20260902-225 Rollover-Prepare Attestation Producer Root Cause

Date: 2026-09-02 ICT  
Coordinator / final reviewer: ChatGPT

## Verdict

`ACCEPT_PASS_PRODUCER_ROOT_CAUSE_PROVEN__AUTHORIZE_BOUNDED_TDD_REPAIR`

Task 225 is accepted.

The accepted root cause is `SOURCE_DEFECT_NONATOMIC_ATTESTATION`: candidate `prepare_plugin_rollover_transaction()` copies the retired project, then observes the retired source tree and backup tree separately, and can return a transaction even when those two full-tree attestations disagree. The candidate finalizer later requires them to agree and therefore correctly rejects the transaction.

The corrected deterministic RED at `f93d78324decf44cdccdeae3a9efe30636b681a8` is valid evidence because:

1. the mutation is outside `package.json.files`;
2. source and backup payload fingerprints remain equal;
3. normal setup/validation/self-test/py_compile prerequisites pass;
4. the only pytest failure is the intended source/backup project-tree equality contract;
5. no installer replacement mutation or live-state repair is involved.

The earlier `007d6bfd...` test attempt is correctly excluded as evidence because its recursive copy hook polluted the payload boundary.

## Repair authorization

Open Task 226 for bounded repository-only TDD repair.

Required behavioral contract:

- `rollover-prepare` must never successfully return an internally inconsistent source/backup full-tree attestation pair;
- if source and backup tree attestations differ after backup creation, prepare must fail closed before transaction success is exposed;
- stable normal direct-plugin state must continue to prepare successfully;
- finalizer predicates and historical Task-143/144 protections must not be weakened.

The existing Task-225 test should be refined at the start of Task 226 to state the desired fail-closed API behavior explicitly (expected exception/current source RED), then production code may receive the minimum repair.

## Link/reparse boundary

Task 225 also identified a separate backup-semantic hazard: default `shutil.copytree(..., symlinks=False)` can dereference symbolic links while `_project_tree_sha256()` attests links structurally.

Task 226 need not broaden into a full link-preserving backup redesign unless tests prove that is required. The minimum safety requirement is that any such structural mismatch must be detected by the same source/backup equivalence gate and rejected before a successful prepare transaction is returned.

Do not weaken project-tree attestation or exclude non-payload entries merely to make hashes equal.

## Runtime boundary

Task 226 remains repository-only:

```text
live installer: forbidden
live rollover-prepare/finalize: forbidden
lifecycle/plugin/Gateway/SQLite mutation: forbidden
process termination: forbidden
Discord Sends/API semantic traffic: 0
Release/tag/asset mutation: forbidden
force push/history rewrite: forbidden
```

Live Task-223 retained state remains untouched pending repository GREEN and later explicit authorization.
