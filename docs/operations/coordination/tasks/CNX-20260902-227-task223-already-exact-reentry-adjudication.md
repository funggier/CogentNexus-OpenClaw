# CNX-20260902-227 — Task-223 Already-Exact Re-entry Adjudication

Status: `READY_FOR_HERMES`
Date: 2026-09-02 ICT
Parent: `CNX-20260902-226`
Failure parent: `CNX-20260902-223`
Forensic parent: `CNX-20260902-224`
Repair parent: `CNX-20260831-198`
Parent umbrella: `CNX-20260831-188`
Executor: Hermes / authenticated Windows forensic operator
Coordinator / final reviewer: ChatGPT

## Purpose

Requalify the preserved Task-223 partial Windows state against the repaired current source and prove which installer state-machine branch a future retry would take.

Task 227 is **read-only adjudication only**. It must not invoke the installer, `rollover-prepare`, `rollover-finalize`, plugin lifecycle, CogentNexus lifecycle, Gateway restart, SQLite write, or Discord traffic.

The key question is whether the current canonical direct plugin is already the exact candidate and therefore safely enters the established:

```text
mode=upgrade
pendingRollover=false
pluginAlreadyExact=true
installPlugin=false
rolloverPlugin=false
```

path.

A PASS authorizes only an independent-review decision on whether a later Task 228 may perform one controlled installer re-entry. It does not itself authorize that retry.

## Accepted parent authority

Task-226 report:

`docs/operations/coordination/reports/CNX-20260902-226-rollover-prepare-attestation-fail-closed-repair.md`

Task-226 independent review:

`docs/operations/coordination/reviews/CNX-20260902-226-rollover-prepare-attestation-fail-closed-repair-review.md`

Accepted review disposition:

`ACCEPT_PASS_REPAIR_GREEN__ALREADY_EXACT_REENTRY_REQUALIFICATION_REQUIRED`

Accepted producer repair commit:

`9a8510f1317c8e53c01c233b080ec20357cd22df`

Accepted candidate plugin payload fingerprint:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No Release/tag/asset mutation is authorized.

## Preserved Task-223/224 state to re-prove, not assume

Historical read-only state from Task 224:

```text
controller mode: passthrough
generation: 33
startup adapter: installed=false
Gateway: healthy
provider: ollama, healthy/ready
Delivery: READY, pending=0, readOnly=true
Recovery: READY, readOnly=true
SQLite integrity: ok
canonical direct plugin path:
C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw
installed candidate fingerprint:
e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
```

Fresh Task-227 evidence is authoritative. If material state drift exists, stop rather than normalize it.

## Obsolete retained transaction evidence

Retained transaction:

`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\install-staging\plugin-rollover-transaction-8469daf5669242189f18e8c87ed9a86c.json`

Task-224 transaction SHA-256:

`ec1b32ec2813e1b4e2c220679f39c6922789b7d77e88ec9ca4ad6ba82ccac510`

Expected matching inventory file:

`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\install-staging\plugin-inventory-8469daf5669242189f18e8c87ed9a86c.json`

Task 224 observed it absent.

Retained backup:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\plugin-generation-rollover-backups\cogentnexus-openclaw-8469daf5669242189f18e8c87ed9a86c`

Task-224 proof:

```text
backup actual tree SHA:
7394401cb0ae9791c1c9b98661a9bf9df47ecb83c0b139b46cd742b17ee7342a

transaction backupProjectTreeSha256:
7394401cb0ae9791c1c9b98661a9bf9df47ecb83c0b139b46cd742b17ee7342a

transaction retiredProjectTreeSha256:
ca74a262293d49b058fce6221db2fa5311214cde567ebb331ff845670c5a2cab

backup payload fingerprint:
f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
```

Task 226 proved the producer defect that could emit this inconsistent pair. Task 227 must treat the transaction as evidence only.

# Hard fences

## Authorized

- fresh GitHub branch/Actions/source reads;
- fresh read-only Windows controller/startup/Gateway/provider/delivery/recovery/SQLite checks;
- read-only OpenClaw plugin inventory/config/status commands documented not to mutate state;
- read-only hashing/parsing of the retained Task-223 transaction and backup;
- read-only copy of evidence into a new `%LOCALAPPDATA%\Temp\cnx227-*` evidence directory;
- exact current-source candidate fingerprint calculation;
- calling `classify-install` with explicit inventory + expected fingerprint because this path is documented read-only;
- calling `scripts/resolve-plugin-lifecycle-actions.ps1` because it is a pure action decision helper;
- source/control-flow inspection proving stale transaction discovery behavior;
- coordination report publication.

## Not authorized

- `scripts/install.ps1` or any installer invocation;
- any `rollover-prepare` invocation;
- any `rollover-finalize` invocation;
- passing the Task-223 transaction to any mutator;
- transaction JSON edit/delete/move/rename;
- retained backup edit/delete/move/rename;
- manual ownership-manifest write;
- `openclaw plugins install/enable/disable/uninstall`;
- `cnxclaw enable/disable/start/stop/restart/reset/uninstall`;
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

## Phase A — Fresh authority and product-drift gate

1. Fetch fresh remote branch HEAD.
2. Verify Task 227 is active and `READY_FOR_HERMES`.
3. Verify accepted repair commit `9a8510f...` is an ancestor of current coordination HEAD.
4. Compare `9a8510f...` -> current HEAD.
5. Require any changes after the accepted repair to be coordination/report/review/task changes only. If product/source/test/workflow drift exists, stop:

`BLOCKED_PRODUCT_DRIFT`

6. Prove public `v0.9.3` remains unchanged.
7. Record fresh relevant workflow status for current branch authority.

## Phase B — Read-only live preservation gate

Record fresh:

```text
controller mode + generation
startup adapter/task status
canonical plugin id/version/rootDir/source/enabled/status
canonical plugin payload fingerprint
all product plugin candidate roots/storage evidence
ownership manifest absolute path + SHA-256 + pluginPath
Gateway health
provider/Ollama health
Delivery readiness
Recovery readiness
SQLite integrity
Task-205 cancelled/inert state
installer/lifecycle process residue
```

Historical expectation is the Task-224 state above, but fresh evidence wins.

If the controller is no longer PASSTHROUGH, the canonical installed plugin is missing/ambiguous, health has materially drifted, or a semantic-recovery hazard exists, stop:

`BLOCKED_STATE_DRIFT`

Do not repair drift.

## Phase C — Re-prove stale evidence identity

Create a new external read-only evidence root under `%LOCALAPPDATA%\Temp`, for example:

`cnx227-already-exact-reentry-<timestamp>`

Without changing live originals, record for the retained transaction:

```text
exists
absolute path
size
mtime
SHA-256
JSON parse status
all rollover identity/hash/fingerprint fields
```

Require the transaction SHA-256 to remain:

`ec1b32ec2813e1b4e2c220679f39c6922789b7d77e88ec9ca4ad6ba82ccac510`

Re-prove the matching Task-223 inventory file remains absent/present and record truth rather than assuming absence.

For the retained backup, re-compute with **current repaired helper read semantics only**:

```text
project-tree SHA-256
payload file count
payload fingerprint
```

If transaction/backup evidence changed since Task 224, stop:

`BLOCKED_STALE_EVIDENCE_DRIFT`

Do not clean it.

If unchanged, classify it explicitly:

`OBSOLETE_PRODUCER_DEFECT_EVIDENCE`

This classification means:

- never finalize it;
- never edit it into consistency;
- never use it as authority for a new rollover;
- preserve it until a later cleanup task explicitly disposes of it.

## Phase D — Prove the current candidate is already exact

Using the exact current branch source after the product-drift gate:

1. calculate repository candidate plugin payload fingerprint with the supported helper;
2. require exact expected fingerprint:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

3. require current canonical installed direct plugin fingerprint to equal that same value;
4. require exactly one canonical product payload candidate and require it to be the manifest-owned direct path;
5. prove the current ownership manifest still binds that same direct path.

If source and installed fingerprints differ, or more than one canonical candidate exists, stop:

`BLOCKED_NOT_ALREADY_EXACT`

Do not invoke rollover recovery.

## Phase E — Execute real read-only attested classification

Capture a fresh `openclaw plugins list --json` inventory into the external Task-227 evidence root only.

Invoke current repaired source:

```text
namespace_ownership.py classify-install
  --workspace <normal workspace>
  --app-data <normal CogentNexus-OpenClaw app-data root>
  --plugin-inventory-json <external read-only capture>
  --expected-replacement-fingerprint e3bcce04...
```

The call must be treated as read-only; snapshot/hash manifest and relevant sentinels before and after to prove no mutation.

Required result:

```text
mode: upgrade
pendingRollover: false
pluginAlreadyExact: true
manifestPluginPath: canonical direct plugin path
replacementPluginPath: canonical direct plugin path
```

`interruptedRolloverReentry` may be absent/false for the direct same-path partial state because the manifest-owned lexical path still exists; do not require the missing-path re-entry subtype.

Any different classification is:

`BLOCKED_CLASSIFICATION_MISMATCH`

## Phase F — Execute production action resolver read-only

Feed the exact classification decision into:

`scripts/resolve-plugin-lifecycle-actions.ps1`

Required production action result:

```text
mode: upgrade
pendingRollover: false
pluginAlreadyExact: true
skipPlugin: false
installPlugin: false
rolloverPlugin: false
```

Any `installPlugin=true` or `rolloverPlugin=true` is:

`BLOCKED_ACTION_MISMATCH`

No installer may be attempted by Task 227 regardless of result.

## Phase G — Prove stale transaction non-selection

Inspect current `scripts/install.ps1` and current ownership helper source and record the exact control flow proving:

1. a rollover transaction path is generated per invocation from a fresh GUID only when `classification.mode == upgrade` and `actions.rolloverPlugin == true`;
2. `rollover-prepare` is called only inside that branch;
3. `rollover-finalize` is called only when that current invocation created `$rolloverTransactionPath`;
4. installer does not enumerate, auto-resume, or pass arbitrary pre-existing `plugin-rollover-transaction-*.json` files to the finalizer;
5. when `pluginAlreadyExact=true`, action resolver sets both plugin lifecycle booleans false and the plugin install/rollover section is skipped.

If source contains any stale-transaction auto-discovery path that could consume Task-223 evidence, stop:

`BLOCKED_STALE_TRANSACTION_SELECTION_RISK`

## Phase H — Final preservation proof

Repeat the read-only live state snapshot and compare against Phase B.

Expected Task-227 mutation ledger:

```text
installer invocations: 0
rollover-prepare invocations: 0
rollover-finalize invocations: 0
manual lifecycle actions: 0
Gateway restarts: 0
plugin/config/ownership/transaction/backup writes: 0
SQLite writes: 0
process terminations: 0
provider/model substitutions: 0
Discord Sends/API semantic traffic: 0
Release/tag/asset mutations: 0
product/source/test/workflow commits by executor: 0
```

Coordination report publication is allowed.

# Required report

Publish:

`docs/operations/coordination/reports/CNX-20260902-227-task223-already-exact-reentry-adjudication.md`

The report must include:

- fresh remote HEAD and product-drift result;
- current live-state snapshot;
- stale transaction/backup identity and classification;
- source vs installed candidate fingerprint equality;
- exact `classify-install` JSON result;
- exact production action-resolver JSON result;
- installer stale-transaction non-selection proof;
- before/after preservation comparison;
- mutation ledger;
- one primary disposition.

## Allowed final dispositions

Use exactly one:

- `PASS_ALREADY_EXACT_REENTRY_PROVEN__ONE_INSTALLER_REENTRY_MAY_BE_REVIEWED`
- `BLOCKED_PRODUCT_DRIFT`
- `BLOCKED_STATE_DRIFT`
- `BLOCKED_STALE_EVIDENCE_DRIFT`
- `BLOCKED_NOT_ALREADY_EXACT`
- `BLOCKED_CLASSIFICATION_MISMATCH`
- `BLOCKED_ACTION_MISMATCH`
- `BLOCKED_STALE_TRANSACTION_SELECTION_RISK`
- `BLOCKED_EVIDENCE`

A PASS is re-entry adjudication only. It does not mean the installer has been retried or the installation is complete.

## Stop boundary

After publishing the report, stop for independent ChatGPT review.

Even after PASS:

- do not invoke installer;
- do not call rollover prepare/finalize;
- do not archive/delete stale transaction/backup;
- do not perform lifecycle actions;
- do not send Discord traffic;
- do not mutate Release/tag/asset state.
