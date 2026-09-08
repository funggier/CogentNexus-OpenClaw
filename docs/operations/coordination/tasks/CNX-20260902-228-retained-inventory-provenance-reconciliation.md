# CNX-20260902-228 — Retained Inventory Provenance Reconciliation

Status: `READY_FOR_HERMES`
Date: 2026-09-02 ICT
Parent: `CNX-20260902-227`
Repair parent: `CNX-20260902-226`
Failure parent: `CNX-20260902-223`
Forensic parent: `CNX-20260902-224`
Parent umbrella: `CNX-20260831-188`
Executor: Hermes / authenticated Windows forensic operator
Coordinator / final reviewer: ChatGPT

## Purpose

Resolve the only remaining Task-227 blocker: why the exact Task-223 matching retained inventory file is present now after Task 224 recorded it as absent.

Task 228 is **read-only provenance reconciliation only**. It must decide whether the file is:

- a historical Task-223 artifact that Task 224 failed to observe correctly;
- a post-Task223 restored/copied/created artifact;
- or provenance-unresolved.

Task 228 must not invoke the installer, clean staging, call rollover prepare/finalize, perform lifecycle actions, restart Gateway, write SQLite, change provider/model state, or send Discord traffic.

## Accepted parent review

Task-227 report:

`docs/operations/coordination/reports/CNX-20260902-227-task223-already-exact-reentry-adjudication.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260902-227-task223-already-exact-reentry-adjudication-review.md`

Accepted disposition:

`ACCEPT_BLOCKED_STALE_EVIDENCE_DRIFT__PROVENANCE_RECONCILIATION_REQUIRED`

Accepted repaired source authority:

`9a8510f1317c8e53c01c233b080ec20357cd22df`

Accepted candidate plugin fingerprint:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

## Exact retained evidence under adjudication

Transaction:

`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\install-staging\plugin-rollover-transaction-8469daf5669242189f18e8c87ed9a86c.json`

Matching inventory:

`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\install-staging\plugin-inventory-8469daf5669242189f18e8c87ed9a86c.json`

Retired backup:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\plugin-generation-rollover-backups\cogentnexus-openclaw-8469daf5669242189f18e8c87ed9a86c`

Task-227 observed inventory identity:

```text
bytes: 156245
SHA-256: 1a7299f926cda4e3f936577204c50059e0e4e716f8594535d4b3c40c40e51477
LastWriteTime local: 2026-09-02 06:00:31.587591100 +0700
```

Historical Task-223 finalizer stage started at:

`2026-09-01T23:00:31.5875911Z`

These timestamps represent the same instant. Current installer source writes the matching inventory immediately before starting the finalizer diagnostic stage. This is a strong historical-origin hypothesis, not proof.

# Hard fences

Authorized:

- fresh GitHub branch/Actions/source/coordination reads;
- read-only Windows filesystem metadata queries;
- read-only hashing of exact retained transaction/inventory/backup;
- copying exact retained evidence into a new external `%LOCALAPPDATA%\Temp` Task-228 evidence root;
- parsing and analyzing only the external copy of the inventory/transaction;
- pure/read-only candidate helper calculations on copied evidence;
- read-only inspection of retained Task-223 and Task-224 external evidence directories/transcripts/scripts/logs;
- read-only controller/Gateway/provider/delivery/recovery/SQLite checks;
- read-only `classify-install` and pure lifecycle action resolver only if the provenance discrepancy is first reconciled as historical/no-later-write;
- coordination report publication.

Not authorized:

- `scripts/install.ps1` invocation;
- `rollover-prepare`, `rollover-finalize`, plan/apply, or any ownership mutator;
- deletion, rename, move, edit, archive, touch, ACL change, or timestamp change of the retained transaction/inventory/backup;
- plugin/config/lifecycle mutation;
- `cnxclaw enable/disable/start/stop/restart/reset/uninstall`;
- Gateway restart;
- SQLite write;
- process termination;
- provider/model substitution;
- Release/tag/asset mutation;
- product/source/test/workflow edit;
- force push/history rewrite;
- Discord Send/API semantic traffic.

Discord budget: `0 Sends`.

# Required execution flow

## Phase A — Fresh authority gate

Before Windows inspection:

1. fetch fresh branch HEAD;
2. verify Task 228 is active and `READY_FOR_HERMES`;
3. verify accepted repair `9a8510f...` remains ancestor of current coordination HEAD;
4. compare repair → HEAD and stop on unexpected product/source/test/workflow drift;
5. verify public `v0.9.3` remains unchanged;
6. record current Actions status for the current coordination HEAD.

Unexpected product drift:

`BLOCKED_PRODUCT_DRIFT`

## Phase B — Pre-open filesystem metadata and identity

Before opening/parsing the retained matching inventory, query safe filesystem metadata for the exact path and record at minimum:

```text
absolute path
exists
length
CreationTime / CreationTimeUtc
LastWriteTime / LastWriteTimeUtc
attributes
reparse/link status if relevant
owner/security identity only if obtainable read-only without privilege mutation
file ID if a documented read-only query is available
```

Do the same for the exact matching transaction.

Then hash both exact live files read-only and require the transaction SHA still equals:

`ec1b32ec2813e1b4e2c220679f39c6922789b7d77e88ec9ca4ad6ba82ccac510`

and record the current inventory SHA.

Do not use LastAccessTime as provenance authority because reading may affect access metadata on some systems.

If the inventory disappears or its identity changes before capture, stop:

`BLOCKED_EVIDENCE_DRIFT`

## Phase C — Preserve external copies

Create a unique external evidence root such as:

`%LOCALAPPDATA%\Temp\cnx228-retained-inventory-provenance-<timestamp>`

Copy, without changing the originals:

- exact transaction JSON;
- exact matching inventory JSON;
- Task-223 relevant transcript excerpts or copies where useful;
- Task-224 retained probe/script/log evidence where useful.

Hash external copies and prove byte equality with the live originals at capture time.

All parsing/normalization beyond simple live hash/metadata must use the external copies.

## Phase D — Inventory semantic identity

Parse the copied matching inventory read-only.

Record the exact product registration fields relevant to candidate selection:

```text
id
packageName when present
version/packageVersion
rootDir
source
enabled
status
```

Using pure current helper semantics on the copied file, derive the active canonical product registration and installed payload fingerprint without invoking any mutator/finalizer.

Require the retained inventory to be internally consistent with the historical Task-223 post-install state before calling it a Task-223 artifact:

```text
id = cogentnexus-openclaw
version = 0.9.3
canonical root = C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw
payload fingerprint = e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
```

Also record whether diagnostics or unrelated inventory records explain why the retained file byte hash differs from later fresh inventory captures.

Do not require entire inventory JSON byte equality with a later current inventory; classify product-semantic equality separately from unrelated diagnostics/order/timestamps.

## Phase E — Historical stage-order correlation

Inspect the retained Task-223 transcript/stage evidence read-only.

Prove the exact order from candidate installer behavior and retained stage timestamps:

```text
openclaw plugins list --json
write plugin-inventory-<rolloverId>.json
start plugin-rollover-finalize diagnostic stage
invoke rollover-finalize
```

Record the closest retained timestamps around inventory creation/finalizer start.

Compare:

- inventory CreationTimeUtc;
- inventory LastWriteTimeUtc;
- historical Task-223 finalizer stage start;
- Task-223 terminal time.

Important classification rule:

- a LastWriteTime equal to the Task-223 stage timestamp supports historical origin;
- a CreationTime materially later than Task 223 can indicate later copy/restore even when LastWriteTime was preserved;
- timestamp correlation alone cannot prove provenance.

## Phase F — Audit Task-224 `absent` observation

Inspect the external Task-224 evidence root and any retained scripts/logs/command output that produced the earlier conclusion that the exact matching inventory was absent.

Historical Task-224 evidence root:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx224-rollover-finalize-adjudication-20260902T`

At minimum determine:

1. whether the exact path tested is retained;
2. whether the exact filename/token `8469daf5669242189f18e8c87ed9a86c` was used;
3. whether the probe output itself is retained or only the report conclusion survives;
4. whether path quoting, wildcard, case, working-directory, timing, tool/session visibility, or another concrete issue can explain a false absence observation;
5. whether any Task-224 action could have moved/restored/created the file — expected answer is no unless evidence proves otherwise.

Do not invent an explanation if the exact Task-224 probe is not retained. In that case classify the prior absence observation as unreconstructable rather than false by assertion.

## Phase G — Provenance classification

Choose exactly one primary classification:

### `HISTORICAL_TASK223_ARTIFACT`

Use only if evidence supports all material points:

- file creation/write metadata is compatible with Task 223 rather than a later copy/restore;
- contents semantically match the Task-223 post-install candidate state;
- retained installer ordering explains the file's existence and timestamp;
- no evidence of a post-Task223 write/restore is found;
- the Task-224 absence observation is shown to be erroneous/incomplete, or its exact probe is unavailable and the positive provenance evidence independently dominates without contradiction.

### `POST_TASK223_STATE_MUTATION`

Use if metadata/content/probe evidence proves the file was created/restored/modified after the Task-223 terminal boundary.

### `UNRESOLVED_OBSERVATION_DISCREPANCY`

Use if the evidence cannot safely distinguish historical origin from later restoration/mutation.

Do not infer an actor unless exact evidence identifies one.

## Phase H — Conditional already-exact reconfirmation

Only if Phase G returns `HISTORICAL_TASK223_ARTIFACT`, repeat the Task-227 read-only attested classification and pure action resolver using fresh current inventory/candidate fingerprint.

Require exactly:

```text
mode=upgrade
pendingRollover=false
pluginAlreadyExact=true
installPlugin=false
rolloverPlugin=false
```

Also repeat current plugin fingerprint and basic health preservation checks.

If this state no longer holds, stop:

`BLOCKED_STATE_DRIFT`

This reconfirmation still does not authorize installer execution.

## Phase I — Final no-mutation proof

Re-hash the live retained transaction and matching inventory after all inspection.

Require their hashes unchanged from Phase B.

Repeat basic read-only preservation checks:

```text
controller mode/generation
Gateway health
provider remains ollama
Delivery READY
Recovery READY
SQLite integrity ok
Task-223 temporary Scheduled Task absent
no relevant installer/runner process residue
```

Mutation ledger must record:

```text
installer invocations: 0
rollover prepare/finalize: 0
stale evidence writes/moves/deletes: 0
manual lifecycle actions: 0
Gateway restarts: 0
SQLite writes: 0
process terminations: 0
provider/model substitutions: 0
Discord Sends/API semantic traffic: 0
Release/tag/asset mutations: 0
product/source/test/workflow edits by executor: 0
```

## Allowed final dispositions

Use exactly one primary disposition:

- `PASS_HISTORICAL_TASK223_ARTIFACT_RECONCILED__ALREADY_EXACT_REENTRY_RECONFIRMED`
- `BLOCKED_POST_TASK223_STATE_MUTATION`
- `BLOCKED_PROVENANCE_UNRESOLVED`
- `BLOCKED_EVIDENCE_DRIFT`
- `BLOCKED_PRODUCT_DRIFT`
- `BLOCKED_STATE_DRIFT`

A PASS is read-only provenance closure only. It does not authorize stale-file cleanup or installer re-entry.

## Stop boundary

Publish:

`docs/operations/coordination/reports/CNX-20260902-228-retained-inventory-provenance-reconciliation.md`

Then stop for independent ChatGPT review.

Even after PASS:

- do not delete or archive retained staging/backup evidence;
- do not invoke installer;
- do not call rollover prepare/finalize;
- do not perform lifecycle actions;
- do not send Discord traffic;
- do not modify public Release/tag/asset state.
