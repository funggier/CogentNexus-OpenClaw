# CNX-20260902-225 — Rollover-Prepare Attestation Producer Root-Cause Adjudication

Status: `READY_FOR_HERMES`
Date: 2026-09-02 ICT
Parent: `CNX-20260902-224`
Repair parent: `CNX-20260831-198`
Parent umbrella: `CNX-20260831-188`
Executor: Hermes / authenticated Windows forensic operator
Coordinator / final reviewer: ChatGPT

## Purpose

Determine why Task-223 `rollover-prepare` emitted a transaction whose immediately-created backup tree hash differs from the recorded retired project tree hash, while the backup payload fingerprint still matches the retired payload fingerprint.

Task 225 is producer-side root-cause adjudication. It must distinguish:

- legitimate concurrent/external mutation of the retired project tree;
- unsupported-state mutation;
- non-atomic prepare/attestation source defect;
- tree-hash versus payload-fingerprint boundary mismatch;
- copy/tree semantic differences;
- another specifically proven cause.

Do not repair live state or complete the installer in this task.

## Accepted parent authority

Task-224 report:

`docs/operations/coordination/reports/CNX-20260902-224-task223-rollover-finalize-retained-state-adjudication.md`

Task-224 review:

`docs/operations/coordination/reviews/CNX-20260902-224-task223-rollover-finalize-retained-state-adjudication-review.md`

Accepted review disposition:

`ACCEPT_PASS_FINALIZE_ROOT_CAUSE_PROVEN__TRANSACTION_INCONSISTENCY_PRODUCER_ADJUDICATION_REQUIRED`

Exact accepted candidate remains:

`a812f27815b3c87b7ca748dc2dea88f987601f70`

Accepted retained transaction facts:

```text
backup tree actual:             7394401cb0ae9791c1c9b98661a9bf9df47ecb83c0b139b46cd742b17ee7342a
backupProjectTreeSha256:        7394401cb0ae9791c1c9b98661a9bf9df47ecb83c0b139b46cd742b17ee7342a
retiredProjectTreeSha256:       ca74a262293d49b058fce6221db2fa5311214cde567ebb331ff845670c5a2cab
backup payload fingerprint:     f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
retiredFingerprint:             f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
```

Candidate prepare ordering includes:

```python
shutil.copytree(retired_project, backup_path)
...
"retiredProjectTreeSha256": _project_tree_sha256(retired_project),
"backupProjectTreeSha256": _project_tree_sha256(backup_path),
```

## Hard fences

Authorized:

- fresh GitHub authority/source reads;
- read-only Windows filesystem inspection;
- read-only copies of Task-223/224 retained evidence into a new external temp evidence root;
- exact candidate helper analysis;
- isolated offline diagnostic scripts/tests against copied fixtures or temporary directories;
- repository test additions only after a source-defect hypothesis is specifically proven enough to require RED reproduction;
- coordination/report publication.

Not authorized:

- live installer invocation;
- live `rollover-prepare` or `rollover-finalize` invocation;
- transaction/inventory/ownership/backup modification or deletion;
- `cnxclaw` lifecycle actions;
- OpenClaw plugin install/enable/disable/uninstall;
- Gateway restart;
- live plugin/config mutation;
- SQLite writes;
- provider/model substitution;
- process termination;
- Discord Send/API semantic traffic;
- Release/tag/asset mutation;
- force push/history rewrite.

Discord budget: `0 Sends`.

## Required execution flow

### Phase A — Fresh authority and preservation gate

1. Fetch fresh branch HEAD and coordination state.
2. Verify Task 225 is active and exact candidate remains accepted authority.
3. Verify no product/source/test/workflow drift supersedes the candidate.
4. Reconfirm preserved Task-223 live state read-only.
5. Reconfirm retained transaction and backup hashes before any derived work.
6. If forensic state materially drifted, stop `BLOCKED_STATE_DRIFT`.

### Phase B — Exact producer/source ordering

Using exact candidate `a812f278...`, trace `prepare_plugin_rollover_transaction()` completely from:

- retired root selection;
- retired payload calculation;
- retired project-root selection;
- backup destination creation;
- `shutil.copytree`;
- `retiredProjectTreeSha256` calculation;
- `backupProjectTreeSha256` calculation;
- transaction serialization.

Record whether source hashing occurs before or after backup creation and identify every gap in which the source tree may change.

### Phase C — Hash-boundary comparison

Read exact implementations of:

- `_project_tree_sha256()`;
- plugin payload fingerprint helper(s);
- `_plugin_project_root()` / root selection helpers;
- copy/ignore behavior if any.

Produce an explicit inclusion matrix for file/entry classes, including at minimum:

```text
regular files
relative paths
file bytes
file mode/metadata if relevant
symlinks
Windows junction/reparse entries
directories
node_modules or package-manager files
runtime/generated files
logs/cache/temp files
package payload-only files
```

Prove why the payload fingerprint can remain equal while project-tree SHA differs, or prove that it cannot.

### Phase D — Retained tree differential

Using only retained/copied Task-223/224 evidence:

1. enumerate the backup tree deterministically;
2. identify files/directories represented by project-tree hashing but outside payload fingerprinting;
3. inspect mtimes/sizes/hashes where retained evidence permits;
4. inspect Task-223 transcript/observer timing around `plugin-rollover-prepare`;
5. identify candidate actors that could mutate the retired direct plugin tree during the prepare interval;
6. do not infer an actor without timestamp/path evidence.

If no retained source-tree snapshot exists, state that exact limitation.

### Phase E — Offline reproduction / hypothesis test

Use scientific single-hypothesis tests in isolated temporary directories only.

Candidate hypotheses to test separately:

1. a source-tree file changes after `copytree` but before source-tree hash;
2. a non-payload file changes while payload fingerprint remains stable;
3. symlink/junction/reparse handling differs between copy and tree hashing;
4. metadata-only changes cannot explain the hash if metadata is excluded;
5. stable source tree always yields identical source/backup tree SHA.

For each hypothesis record:

```text
setup
single manipulated variable
source tree SHA
backup tree SHA
source payload fingerprint
backup payload fingerprint
result
```

### Phase F — Root-cause classification

Classify exactly one primary outcome when evidence permits:

- `SOURCE_DEFECT_NONATOMIC_ATTESTATION` — supported valid state can race between copy and source attestation, producing an internally inconsistent transaction;
- `EXTERNAL_SUPPORTED_MUTATION` — a normal supported actor is proven to mutate the retired tree during prepare;
- `EXTERNAL_UNSUPPORTED_MUTATION` — unsupported/manual mutation is proven;
- `TREE_COPY_SEMANTIC_MISMATCH` — stable source and copy can differ due to copy/hash semantics;
- `HASH_BOUNDARY_ONLY` — mismatch is fully explained by intentionally different attestation boundaries without a prepare defect;
- `OTHER_PROVEN`;
- `UNRESOLVED`.

The report must identify:

```text
producer operation/order causing or permitting mismatch
exact differing boundary/file class where proven
whether the state was valid/supported
whether candidate source behavior is safety-correct
whether production repair is required
smallest repair principle if required
```

### Phase G — TDD gate if source defect is proven

Only if `SOURCE_DEFECT_NONATOMIC_ATTESTATION` or another source defect is proven:

1. create the smallest deterministic RED test that reproduces a valid retired-tree mutation/race accepted by prepare but rejected by finalize;
2. prove RED on exact candidate behavior;
3. do not implement production repair unless the task is explicitly updated to authorize repair after RED evidence is reviewed.

If no source defect is proven, do not add speculative tests or source changes.

### Phase H — Final preservation

Repeat read-only preservation checks and record mutation ledger:

```text
installer invocations: 0
live rollover-prepare invocations: 0
rollover-finalize invocations: 0
manual lifecycle actions: 0
Gateway restarts: 0
live plugin/config/ownership/transaction/backup writes: 0
SQLite writes: 0
process terminations: 0
provider/model substitutions: 0
Discord Sends/API semantic traffic: 0
Release/tag/asset mutations: 0
force pushes: 0
```

Repository diagnostic test/report commits must be listed separately if created.

## Allowed final dispositions

- `PASS_PRODUCER_ROOT_CAUSE_PROVEN__SOURCE_REPAIR_REQUIRED`
- `PASS_PRODUCER_ROOT_CAUSE_PROVEN__NO_SOURCE_REPAIR`
- `PASS_PRODUCER_ROOT_CAUSE_PROVEN__RED_REPRODUCED_AWAIT_REPAIR_REVIEW`
- `BLOCKED_STATE_DRIFT`
- `BLOCKED_PRODUCT_DRIFT`
- `BLOCKED_MISSING_RETAINED_EVIDENCE`
- `BLOCKED_ROOT_CAUSE_UNRESOLVED`

## Stop boundary

Publish:

`docs/operations/coordination/reports/CNX-20260902-225-rollover-prepare-attestation-producer-root-cause.md`

Then stop for independent ChatGPT review unless the coordination state has already been explicitly advanced by the coordinator.
