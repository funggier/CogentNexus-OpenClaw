# Independent Review — CNX-20260902-227 Task-223 Already-Exact Re-entry Adjudication

Date: 2026-09-02 ICT  
Coordinator / final reviewer: ChatGPT

## Verdict

`ACCEPT_BLOCKED_STALE_EVIDENCE_DRIFT__PROVENANCE_RECONCILIATION_REQUIRED`

Task 227 correctly stopped at its stale-evidence gate and did not overrun the read-only fence. The newly observed matching retained inventory file creates a real discrepancy with the Task-224 report and therefore must be reconciled before any installer re-entry is authorized.

This review does **not** accept the file's presence as proof of a new live mutation. Its observed last-write timestamp is historically aligned with the original Task-223 installer/finalizer interval, so the present evidence is more accurately classified as an unresolved **observation/provenance discrepancy** until the file metadata, contents, and Task-224 absence probe are independently reconciled.

No installer, stale-file cleanup, rollover prepare/finalize, lifecycle action, Gateway restart, SQLite write, provider/model change, Discord traffic, Release/tag mutation, or force push is authorized by this review.

## Fresh repository authority

Fresh branch HEAD reviewed:

`1ff389b83698a86b8b39b4267c37f5be85f26a77`

The only delta from the Task-227 activation commit `7ac15110fc1a1cc43ec6945dfd60f2973c3fb843` is the Task-227 coordination report. No product/source/test/workflow file changed.

Fresh Actions on `1ff389b...` are GREEN:

```text
Validate:                      33642680849  success
Windows Installer Pack Smoke: 33642680890  success
PS5.1 Acceptance Smoke:        33642680942  success
```

Therefore the current blocker is not repository CI or candidate source drift.

## Accepted Task-227 findings

Task 227 re-proved the preserved partial-state invariants read-only:

```text
controller: passthrough, generation 33
startup adapter: installed=false
Gateway: healthy
provider: ollama
Delivery: READY, pending=0
Recovery: READY
SQLite integrity: ok
Task-223 temporary task: absent
installed plugin version: 0.9.3
installed plugin fingerprint: e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
```

The accepted repaired/current source fingerprint and installed direct-plugin fingerprint are equal.

Task 227 also executed the supported read-only classifier before the discrepancy gate was adjudicated and obtained:

```text
mode=upgrade
pendingRollover=false
pluginAlreadyExact=true
manifestPluginPath=<canonical direct plugin path>
replacementPluginPath=<same canonical direct plugin path>
```

Pure production action resolution returned:

```text
installPlugin=false
rolloverPlugin=false
```

This is valid diagnostic evidence for the supported already-exact branch, but it is not yet installer authority.

## Retained transaction remains obsolete

The retained Task-223 transaction SHA remains:

`ec1b32ec2813e1b4e2c220679f39c6922789b7d77e88ec9ca4ad6ba82ccac510`

The retained backup still reproduces:

```text
actual/backupProjectTreeSha256:
7394401cb0ae9791c1c9b98661a9bf9df47ecb83c0b139b46cd742b17ee7342a

transaction retiredProjectTreeSha256:
ca74a262293d49b058fce6221db2fa5311214cde567ebb331ff845670c5a2cab
```

The mismatch remains unchanged. Task 226 repaired future producer behavior; it did not make this old transaction valid. The old transaction must never be edited, reused, or passed to `rollover-finalize`.

## Inventory-file discrepancy

Task 224 recorded the matching file as absent:

`plugin-inventory-8469daf5669242189f18e8c87ed9a86c.json`

Task 227 observed it present with:

```text
bytes: 156245
SHA-256: 1a7299f926cda4e3f936577204c50059e0e4e716f8594535d4b3c40c40e51477
last-write local: 2026-09-02 06:00:31.587591100 +0700
```

That timestamp converts to:

`2026-09-01T23:00:31.5875911Z`

Task-224 retained stage evidence recorded the historical Task-223 finalizer stage starting at the same instant:

`CNXCLAW_INSTALL_STAGE_START stage=plugin-rollover-finalize utc=2026-09-01T23:00:31.5875911+00:00`

Current installer source writes the matching `plugin-inventory-$rolloverId.json` immediately before it starts the `plugin-rollover-finalize` diagnostic stage. Therefore the observed timestamp is structurally consistent with the file having been written by the original Task-223 installer.

That correlation is significant, but timestamp correlation alone is not enough to override Task 224's prior absence observation. Do not attribute an actor yet.

## Required successor adjudication

A bounded read-only successor must determine whether this is:

1. `HISTORICAL_TASK223_ARTIFACT` — the file was created by Task 223 and Task 224's absence observation was incomplete/incorrect;
2. `POST_TASK223_STATE_MUTATION` — the file was later created/restored/copied into staging;
3. `UNRESOLVED_OBSERVATION_DISCREPANCY` — provenance cannot be established safely.

The successor must at minimum:

- read and hash the exact matching inventory without modifying it;
- record CreationTime/LastWriteTime/size and other safe filesystem metadata;
- parse JSON read-only and prove whether it describes the Task-223 post-install canonical candidate registration;
- compare its canonical plugin registration/fingerprint semantics with Task-223/224 retained evidence and current inventory;
- inspect the Task-223 transcript/stage ordering around inventory capture/finalizer start;
- inspect the exact Task-224 evidence/probe that produced the `absent` conclusion, including the path actually tested and any preserved script/output if available;
- repeat transaction/inventory hashes before and after inspection to prove no mutation;
- preserve `0 Discord Sends`.

If historical Task-223 origin is proven and no post-Task223 write is observed, the stale-evidence blocker may be retired as an observation discrepancy. If later mutation is proven or provenance remains unresolved, installer re-entry remains blocked.

## Installer-control-flow note

Task 227's source inspection is accepted: a normal already-exact invocation initializes its local rollover transaction variable to null, creates a new transaction only when `rolloverPlugin=true`, and does not enumerate arbitrary retained `plugin-rollover-transaction-*.json` files. Therefore the stale transaction/inventory pair is not automatically selected by the already-exact installer branch.

This does not answer whether the stale pair should be removed later for final cleanliness. Cleanup, if required, must be separately authorized only after provenance is preserved and reviewed.

## Review disposition

`ACCEPT_BLOCKED_STALE_EVIDENCE_DRIFT__PROVENANCE_RECONCILIATION_REQUIRED`

Next task: read-only retained-inventory provenance reconciliation. No installer retry yet.
