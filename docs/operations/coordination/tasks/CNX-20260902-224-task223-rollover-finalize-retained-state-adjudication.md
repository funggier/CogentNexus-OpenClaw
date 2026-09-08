# CNX-20260902-224 — Task-223 Rollover-Finalize Retained-State Adjudication

Status: `READY_FOR_HERMES`
Date: 2026-09-02 ICT
Parent: `CNX-20260902-223`
Repair parent: `CNX-20260831-198`
Parent umbrella: `CNX-20260831-188`
Executor: Hermes / authenticated Windows forensic operator
Coordinator / final reviewer: ChatGPT

## Purpose

Determine the exact first failing predicate inside Task-223 `plugin-rollover-finalize` using the retained failed-install evidence and current read-only live state.

Task 224 is **forensics/adjudication only**. It must not retry or complete the installer, must not call the rollover finalizer, and must not mutate lifecycle, plugin, ownership, SQLite, Gateway, provider/model, or Discord state.

## Accepted parent disposition

Task-223 report:

`docs/operations/coordination/reports/CNX-20260902-223-task222-exact-candidate-windows-install-over-requalification.md`

Task-223 review:

`docs/operations/coordination/reviews/CNX-20260902-223-task222-exact-candidate-windows-install-over-requalification-review.md`

Accepted disposition:

`ACCEPT_FAIL_INSTALLER_TERMINAL__ROLLOVER_FINALIZE_ROOT_CAUSE_ADJUDICATION_REQUIRED`

## Immutable publication and candidate authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task-222/223 exact candidate:

`a812f27815b3c87b7ca748dc2dea88f987601f70`

Accepted candidate payload:

```text
artifact ID: 9810139538
artifact digest: sha256:3164b7770e7d8991691d7bbedced092866c208add72b0c03b4aa3d39d1b50ff0
payload files: 192
payload fingerprint: e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
```

Historical retired live fingerprint recorded by Task 223:

`f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`

## Accepted Task-223 partial state

Task 223 proved:

- one installer invocation;
- candidate package installation completed successfully;
- installed canonical plugin fingerprint is exact candidate `e3bcce04...`;
- `plugin-disable-post-install` completed exit 0;
- `plugin-rollover-finalize` completed exit 1;
- no final installer success marker;
- latest rollover transaction remains retained;
- controller remains `passthrough`, generation 33;
- startup adapter absent;
- Gateway/Ollama healthy;
- Delivery/Recovery READY;
- SQLite integrity `ok`;
- Discord Sends `0`.

Known Task-223 transaction:

`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\install-staging\plugin-rollover-transaction-8469daf5669242189f18e8c87ed9a86c.json`

Expected matching inventory filename, if retained by the installer:

`plugin-inventory-8469daf5669242189f18e8c87ed9a86c.json`

Do not assume it exists; prove it.

## Historical finalizer repairs to compare, not blindly repeat

Task 143 repaired direct canonical same-path A -> B finalization where path identity remains stable but exact payload fingerprint changes.

Accepted Task-143 repair commit:

`59952167f51657ae2ff900a28aae528f835f9b6e`

Task 144 subsequently required canonical lexical active registration before direct same-path authority.

Accepted Task-144 repair commit:

`fb5781c1abd68280760bd5b3b4a65fabd8a60e58`

The current Task-223 candidate includes those lineages. Their historical failure messages are comparison evidence only; do not classify a regression unless current retained data proves the same predicate is failing.

# Hard fences

Authorized:

- fresh GitHub authority/source reads;
- read-only Windows filesystem inspection;
- read-only copy of retained evidence into a new `%LOCALAPPDATA%\Temp` evidence directory;
- hash/JSON parsing/newline/path/identity computations on copied or source files;
- read-only OpenClaw inventory/config/status commands only when they are documented not to mutate state;
- read-only controller/Gateway/provider/delivery/recovery/SQLite checks;
- importing candidate Python ownership helpers for pure read calculations, provided no owning mutator/finalizer is invoked;
- isolated diagnostic scripts under the Task-224 external evidence directory;
- coordination report publication.

Not authorized:

- `scripts/install.ps1` or any installer invocation;
- `rollover-finalize` CLI or `finalize_plugin_rollover_transaction()` invocation;
- `rollover-prepare`;
- manual ownership-manifest write;
- transaction/inventory modification/deletion;
- backup modification/deletion;
- `cnxclaw enable/disable/start/stop/restart/reset/uninstall`;
- `openclaw plugins install/enable/disable/uninstall`;
- Gateway restart;
- live plugin/config mutation;
- SQLite write;
- provider/model substitution;
- process termination;
- Discord Send/API semantic traffic;
- product/source/test/workflow edit;
- Release/tag/asset mutation;
- force push/history rewrite.

Discord budget: `0 Sends`.

# Required execution flow

## Phase A — Fresh authority and preservation gate

Before inspecting retained data:

1. fetch fresh remote branch HEAD;
2. verify Task 224 is active and `READY_FOR_HERMES`;
3. verify candidate `a812f278...` remains ancestor of coordination HEAD;
4. compare candidate → HEAD and identify any product/source/test/workflow drift after candidate;
5. if unexpected product drift exists, stop `BLOCKED_PRODUCT_DRIFT`;
6. prove public `v0.9.3` remains unchanged;
7. record current read-only live state.

At minimum record:

```text
controller mode + generation
startup adapter state
installed plugin id/version/path/fingerprint/enabled/status
Gateway health
provider/Ollama health
Delivery readiness
Recovery readiness
SQLite integrity
Task-205 cancellation/inertness
relevant installer/lifecycle process residue
```

If current state has materially changed from the preserved Task-223 partial state in a way that destroys forensic authority, stop:

`BLOCKED_STATE_DRIFT`

Do not repair drift in this task.

## Phase B — Recover the exact specific Task-223 exception

Inspect the retained Task-223 evidence before performing any derived classification.

Primary transcript:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx223-install-over-20260902T\installer-transcript.txt`

Also inspect:

```text
runner-stage.log
observer.log
```

Search the complete transcript/stderr for the Python `rollover-finalize` invocation and capture the **first specific Python exception/RuntimeError/traceback message** preceding the generic PowerShell throw.

The report must quote only the minimum non-sensitive error line(s) needed to classify the predicate.

If the exact Python exception is retained, treat it as the primary first-failure evidence and then independently verify its predicate inputs in later phases.

If no exact Python exception is retained, state that explicitly and continue with predicate reconstruction. Do not guess.

## Phase C — Preserve and parse exact transaction/inventory evidence

Create a new external evidence root, for example:

`%LOCALAPPDATA%\Temp\cnx224-rollover-finalize-adjudication-<timestamp>`

Read and hash without modifying the live originals:

1. exact transaction JSON:
   `plugin-rollover-transaction-8469daf5669242189f18e8c87ed9a86c.json`;
2. exact matching inventory JSON, if present;
3. current ownership manifest;
4. retired-generation backup tree named by the transaction;
5. current installed plugin root;
6. relevant OpenClaw plugin inventory/config readback.

For each retained JSON/file authority record:

```text
absolute path
exists
size
SHA-256
parse success/failure
mtime where useful
```

Do not rewrite or pretty-print back into the live directories. Any normalized copies belong only under the external Task-224 evidence root.

If the transaction is missing or unparsable, classify:

`BLOCKED_MISSING_RETAINED_EVIDENCE`

Do not attempt recovery.

## Phase D — Reconstruct the finalizer predicates in exact source order

Use the exact candidate source:

`a812f27815b3c87b7ca748dc2dea88f987601f70`

Owning implementation:

`skills/cogentnexus-openclaw/scripts/namespace_ownership.py`

Do **not** invoke `finalize_plugin_rollover_transaction()`.

Instead evaluate its pre-write predicates independently and read-only, in source order. Record PASS/FAIL and the exact sanitized compared values for every item.

### D1. Replacement selection and fingerprint attestation

Reconstruct `_active_registered_plugin(plugin_inventory, openclaw_state)` against the retained Task-223 inventory.

Record:

```text
selected record id/name/version/rootDir/source/status/enabled fields that affect selection
resolved replacement root
replacement fingerprint
expectedReplacementFingerprint
retiredFingerprint
```

Evaluate:

- expected fingerprint format valid;
- retired fingerprint format valid;
- replacement fingerprint equals expected candidate.

### D2. Manifest stability

Record:

```text
transaction manifestBeforeSha256
current manifest SHA-256
transaction manifestBefore.pluginPath
current manifest pluginPath
```

Evaluate whether the manifest changed during the transaction.

Do not write the manifest.

### D3. Backup/tree proof

From transaction fields record:

```text
backupPath
backupProjectTreeSha256
retiredProjectTreeSha256
retiredPluginPath
retiredProjectRoot
```

Using the candidate implementation's read-only project-tree/payload calculation semantics, compute:

- current backup tree SHA-256;
- backup payload fingerprint;
- current retired/direct project tree only if required for classification and read-only.

Evaluate:

- backup directory exists;
- backup tree equals prepared backup hash;
- backup tree equals retired project tree hash;
- backup payload fingerprint equals retired fingerprint where the direct same-path branch requires it.

### D4. Direct transaction classification

Reconstruct the exact lexical/path keys used by candidate code:

```text
direct_root = <openclawState>/extensions/cogentnexus-openclaw
retiredPluginPath key
retiredProjectRoot key
manifestBefore.pluginPath key
```

Evaluate `direct_transaction` exactly as the source does.

Record whether the transaction is direct or managed by source semantics, not by intuition.

### D5. Canonical active registration

Record retained inventory `rootDir` exactly as serialized and the candidate-computed registration key.

Compare it to canonical `direct_key` using the same `abspath`/`normcase` lexical semantics.

Evaluate the Task-144 invariant:

- if direct transaction, active registration must be lexical canonical direct path.

Also independently record resolved filesystem identity so lexical and resolved identities are not conflated.

### D6. Direct-root real/non-reparse identity

For a direct transaction evaluate read-only:

- direct root exists as directory;
- not symlink/junction/reparse according to candidate semantics;
- `_canonical(direct_root)` equals transaction `retiredPluginPath` as required.

### D7. Same-path A -> B transition

Reconstruct:

`same_path = _canonical(replacement.root) == transaction.retiredPluginPath`

If same-path, evaluate:

- `direct_transaction` true;
- expected fingerprint differs from retired fingerprint;
- backup fingerprint equals retired fingerprint;
- current replacement fingerprint equals expected fingerprint.

### D8. Product-storage uniqueness

Reconstruct candidate `product_plugin_inventory(openclaw_state)` read-only.

Record all product evidence keys and canonical paths.

For direct same-path finalization require exactly:

```text
{"directPlugin"}
```

and that it binds the transaction retired/canonical direct path.

Any additional npm/product storage evidence must be named and proven rather than summarized as “conflict”.

### D9. Pre-write verdict

Identify the **first predicate in candidate source order that evaluates FAIL**.

If every pre-write predicate evaluates PASS, do not call finalizer. Continue to Phase E because the failure may be inside manifest write/final verification/rollback.

## Phase E — Adjudicate write/verification boundary without writing

Only if all pre-write predicates pass:

1. derive in memory the `manifest_after` object candidate code would construct;
2. compare that in-memory object against current manifest schema requirements;
3. run only read-only validation calculations that can predict `verify_manifest()` behavior without writing;
4. inspect Task-223 traceback for evidence that failure occurred after manifest write;
5. inspect current manifest hash/content to determine whether rollback restored `manifestBefore` or whether another durable result exists.

Do not create a temporary manifest in the live state root and do not invoke any function that writes/rolls back/quarantines ownership state.

If the write/verify branch cannot be adjudicated without mutation and no retained traceback identifies it, classify:

`BLOCKED_WRITE_BOUNDARY_EVIDENCE`

rather than testing it live.

## Phase F — Compare with historical Task 143/144 invariants

Explicitly answer:

1. Does the current failing predicate equal the historical Task-143 same-path path-inequality defect?
2. Does it equal the Task-144 noncanonical lexical registration defect?
3. Are both historical repairs present in candidate source?
4. Is the current failure caused by a new inventory/transaction/live-state shape instead?

Do not label “regression” merely because the generic installer message matches historical failures.

## Phase G — Root-cause classification

Classify exactly one primary root-cause category when evidence permits:

- `SOURCE_DEFECT` — current valid supported state is rejected by candidate finalizer;
- `TRANSACTION_EVIDENCE_INVALID` — transaction/backup/manifest attestation legitimately fails;
- `INVENTORY_REGISTRATION_MISMATCH` — retained post-install inventory is noncanonical/ambiguous/incompatible with valid finalization;
- `MANIFEST_DRIFT` — durable manifest changed after prepare;
- `BACKUP_DRIFT` — retired-generation backup/tree proof no longer matches;
- `CONFLICTING_STORAGE_EVIDENCE` — additional product storage makes finalization unsafe;
- `WRITE_VERIFY_BOUNDARY_FAILURE` — predicates pass but commit/verify/rollback failed;
- `OTHER_PROVEN` — only with exact evidence;
- `UNRESOLVED` — evidence cannot distinguish safely.

The report must identify:

```text
first failing predicate
expected value
observed value
source location/condition
whether failure is safety-correct or a product defect
whether offline TDD repair is required
whether a supported live completion path may exist after repair
```

## Phase H — Final preservation proof

Repeat read-only checks after forensics and prove Task 224 itself caused no live semantic/product mutation.

Mutation ledger expected:

```text
installer invocations: 0
rollover-finalize invocations: 0
rollover-prepare invocations: 0
manual lifecycle actions: 0
Gateway restarts: 0
plugin/config/ownership/transaction/backup writes: 0
SQLite writes: 0
process terminations: 0
provider/model substitutions: 0
Discord Sends/API semantic traffic: 0
Release/tag/asset mutations: 0
product/source/test/workflow commits: 0
```

Coordination report commit is allowed.

## Allowed final dispositions

Use one primary disposition:

- `PASS_FINALIZE_ROOT_CAUSE_PROVEN__SOURCE_REPAIR_REQUIRED`
- `PASS_FINALIZE_ROOT_CAUSE_PROVEN__STATE_EVIDENCE_REPAIR_REQUIRED`
- `PASS_FINALIZE_ROOT_CAUSE_PROVEN__WRITE_VERIFY_BOUNDARY`
- `BLOCKED_MISSING_RETAINED_EVIDENCE`
- `BLOCKED_STATE_DRIFT`
- `BLOCKED_PRODUCT_DRIFT`
- `BLOCKED_WRITE_BOUNDARY_EVIDENCE`
- `BLOCKED_ROOT_CAUSE_UNRESOLVED`

A PASS here means diagnostic root-cause closure only. It never means the install is complete.

## Stop boundary

Publish:

`docs/operations/coordination/reports/CNX-20260902-224-task223-rollover-finalize-retained-state-adjudication.md`

Then stop for independent ChatGPT review.

Even after diagnostic PASS:

- do not retry installer;
- do not call finalizer;
- do not perform lifecycle actions;
- do not send Discord traffic;
- do not modify public Release/tag/asset state.
