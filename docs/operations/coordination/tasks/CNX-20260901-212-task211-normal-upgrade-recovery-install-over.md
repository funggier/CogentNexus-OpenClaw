# CNX-20260901-212 — Task-211 Normal-Upgrade Recovery Install-Over

Status: `READY_FOR_HERMES`
Date: 2026-09-01 ICT
Parent: `CNX-20260901-211`
Repair parent: `CNX-20260831-198`
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Purpose

Recover the Windows host from the Task-210 observer-interrupted install boundary by performing one newly authorized, fresh normal-upgrade install-over of the exact Task-207 candidate **only after** re-proving the ordinary-upgrade state identified by Task 211.

Task 212 is install/provenance/health only. It must not perform Discord semantic acceptance. Stop after the recovered install is either proven converged or proven failed/ambiguous.

## Immutable authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task-207 repository-GREEN candidate:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Validated package proof:

```text
artifact ID: 9790881384
artifact digest: sha256:1733897690890f9adcb12176b79db2b43e27799a4022743c4597fad44d2d5a34
candidate plugin fingerprint: d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b
payload files: 192
zip SHA-256: 0321028fc6214e18dbc965ad79a6d04328a05a84dce6a9efc058fb1122237986
tar.gz SHA-256: 0ab3884621a518b4cfd46949e3c8e3e7f9f52995bee257743960dd7636794dcf
```

Exact-head CI authority:

```text
Validate: 33483589170 success
Windows Installer Pack Smoke: 33483589124 success
PS5.1 Acceptance Smoke: 33483589138 success
```

Accepted OpenClaw baseline:

`2026.7.1-2 (0790d9f)`

Task-211 accepted live old-generation fingerprint:

`f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`

## Accepted Task-211 interpretation

Task 211 proved:

```text
controller mode: passthrough
startup adapter: installed=false
Gateway: healthy
selected provider: ollama
SQLite integrity: ok
live plugin fingerprint: f82674172...
live plugin version: 0.9.3
live plugin root: canonical direct extension path
live plugin: disabled
candidate fingerprint: d0677581...
Task-205 stale Ticket/recovery: cancelled and inert
candidate-bound Task-210 rollover transaction: absent
classifier mode: upgrade
pendingRollover: false
pluginAlreadyExact: false
replacementPluginPath: null
legacy: []
```

This is not the supported `interruptedRolloverReentry=true` shape. It is accepted as a recoverable ordinary same-version upgrade boundary where the old plugin generation remains in place and the Task-207 replacement never became active.

## Critical observer rule

Historical successful install-over evidence shows:

- `plugin-rollover-prepare` may take approximately 430–434 seconds;
- full install-over may take roughly 13–14 minutes.

Therefore **do not run the installer inside one blocking executor command with a 420-second or similar outer timeout**.

Required observer shape:

1. launch exactly one standalone `powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File <verified install.ps1> -Workspace <workspace>` process;
2. redirect its stdout and stderr to durable evidence files;
3. record exact PID, creation time, executable path, and command line;
4. return control to the executor immediately after launch;
5. poll that exact root PID and the retained streams with separate bounded read-only observations;
6. if one observer call times out, reconnect and continue observing **the same PID**;
7. never start another installer while the original PID exists or terminal outcome is unresolved;
8. never kill the installer merely because an observer timeout occurs.

A process must be identified by PID + creation time + executable path before each interpretation to guard against PID reuse.

## Phase A — fresh authority and replay fence

Before live mutation:

- fresh-fetch branch HEAD, ACTIVE.md, STATUS.md, Task 211 report/review, and this Task 212;
- confirm no Task-212 report already exists;
- confirm repository product candidate remains `27fe0181...` and no unexplained product-source/test/workflow drift was introduced after it;
- verify the retained candidate package/archive hashes and candidate fingerprint again;
- confirm no installer/recovery/lifecycle process from Task 210/211 remains.

If any authority/replay/provenance fact is ambiguous: `BLOCKED_AUTHORITY`, no installer.

## Phase B — exact live normal-upgrade preflight

Read-only capture immediately before install:

- OpenClaw exact version;
- controller status/mode/generation;
- Gateway health;
- Ollama selected/ready state;
- startup adapter state;
- delivery/recovery checks;
- SQLite `PRAGMA integrity_check`;
- current plugin inventory JSON;
- current plugin fingerprint using the exact candidate ownership tool;
- ownership manifest and ownership verification;
- install-staging / transaction inventory;
- same-session Task-205 cancellation state and any nonterminal/emittable recovery/outbox/model-call residue;
- relevant process inventory.

Run the exact candidate's attested classifier using current plugin inventory plus expected replacement fingerprint `d0677581...`.

Required safe preflight shape:

```text
mode = upgrade
pendingRollover = false
pluginAlreadyExact = false
replacementPluginPath = null
legacy = []
live plugin fingerprint = f82674172...
candidate fingerprint = d0677581...
Task-205 stale recovery remains cancelled/inert
no pending assistant delivery/outbox/active-recovering model call able to emit old acceptance output
SQLite integrity = ok
no candidate-bound active/pending rollover transaction
no current installer/lifecycle process
```

If live fingerprint changed from `f826...`, do not assume success or failure. Stop `BLOCKED_PREFLIGHT_DRIFT` unless the new state independently proves already-converged exact Task-207 identity and is reviewed separately.

If classifier reports pending rollover, interrupted re-entry, foreign/legacy state, multiple candidates, or any unsafe ownership mismatch: `BLOCKED_PREFLIGHT_OWNERSHIP`, no installer.

## Phase C — exactly one newly authorized install-over

Use the verified extracted Task-207 package/source boundary from artifact `9790881384`.

Launch exactly once:

```text
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File <TASK212_VERIFIED_CANDIDATE>/scripts/install.ps1 -Workspace C:/Users/CDQ-P/.openclaw/workspace
```

No `-Provider` argument.

Do not use `Start-Process -Wait` or any executor wait primitive whose semantics include long-lived descendants.

Persist:

- exact command;
- installer PID;
- creation timestamp;
- stdout path/hash/size over time;
- stderr path/hash/size over time;
- process existence samples;
- installer stage START/COMPLETE records as they appear.

### Observation cadence

Poll approximately every 30–60 seconds while the exact PID exists. A single poll must be bounded and must not own/terminate the installer.

Allow at least **20 minutes** from installer start before treating long runtime alone as anomalous. Historical success took ~819 seconds.

If the process remains alive beyond 20 minutes:

- capture process tree, CPU/thread/handle deltas, stream growth and current stage;
- if meaningful progress continues, observation may continue on the same PID;
- if evidence is static/ambiguous, stop as `BLOCKED_INSTALLER_STILL_RUNNING` **without killing or retrying**.

### Terminal acceptance

Installer success requires all of the following:

1. exact root PID terminates naturally;
2. retained stdout contains all expected stage START/COMPLETE pairs with exit code `0` for:
   - `ticket-db-bootstrap`
   - `plugin-npm-pack`
   - `plugin-rollover-prepare`
   - `plugin-install-local-package`
   - `plugin-disable-post-install`
   - `plugin-rollover-finalize`
   - `owned-runtime-ensure`
3. stdout contains the final installation success line;
4. no terminal error line contradicts success.

A direct process exit code is desirable but not mandatory if the root process was intentionally detached and the accepted stage/success/natural-termination evidence is complete, matching prior accepted Task-170 evidence semantics.

If the process disappears without complete stage/success evidence: `BLOCKED_INSTALLER_TERMINAL`, no retry.

If any stage completes non-zero or installer emits terminal failure: `FAIL_INSTALLER`, no retry.

## Phase D — post-install exact provenance

Only after terminal install success, independently prove:

```text
installed plugin fingerprint = d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b
plugin id = cogentnexus-openclaw
plugin version = 0.9.3
plugin enabled = true
plugin status = loaded
plugin error = null
OpenClaw = 2026.7.1-2
ownership verify = pass
```

Capture the new rollover transaction and prove its expected replacement fingerprint equals `d0677581...` and final ownership is coherent. Historical transaction records may remain; do not delete them merely for cleanliness.

If installed fingerprint or registration differs: `FAIL_PROVENANCE`.

## Phase E — managed runtime health

Require:

- controller mode `managed`;
- desired Gateway/provider running;
- selected provider `ollama`;
- Gateway healthy on expected loopback port;
- Ollama reachable/ready;
- startup adapter installed/enabled/Ready with healthy last result;
- delivery `READY`, pending outbox `0`;
- recovery `READY`, no unexpected recovery incident;
- no active/recovering stale model call;
- Task-205 cancelled recovery remains inert;
- SQLite integrity `ok`;
- no installer/lifecycle process residue.

Perform a second read-only stability sample after convergence. Do not issue a compensating `enable`, restart, reset, uninstall, or reinstall if managed convergence fails; report the exact failure.

## Discord boundary

Task 212 authorizes:

`0 Discord sends`

No human Send, probe, bot/API/injected message, semantic model request, or acceptance nonce. Discord requalification will be a separate successor only after Task 212 is independently reviewed PASS.

## Explicit non-actions

Task 212 does **not** authorize:

- more than one installer launch;
- `cnxclaw enable/disable/start/stop/restart/reset/uninstall` as a workaround;
- manual plugin enable/disable;
- manual ownership/manifest/transaction/backup edits;
- raw SQLite writes;
- provider/model substitution;
- OpenClaw upgrade;
- source/test/workflow modification;
- Release/tag/asset mutation;
- force push;
- Discord traffic.

## Allowed dispositions

- `PASS`
- `BLOCKED_AUTHORITY`
- `BLOCKED_PREFLIGHT_DRIFT`
- `BLOCKED_PREFLIGHT_OWNERSHIP`
- `BLOCKED_INSTALLER_STILL_RUNNING`
- `BLOCKED_INSTALLER_TERMINAL`
- `FAIL_INSTALLER`
- `FAIL_PROVENANCE`
- `FAIL_MANAGED_HEALTH`
- `BLOCKED_EVIDENCE`

## Report

Publish:

`docs/operations/coordination/reports/CNX-20260901-212-task211-normal-upgrade-recovery-install-over.md`

The report must include:

- fresh authority/provenance gate;
- exact preflight classifier output;
- exact pre-install live/candidate fingerprints;
- exact installer PID/creation/command;
- stream hashes/sizes and stage table;
- natural process terminal evidence;
- post-install installed fingerprint and rollover transaction proof;
- plugin/OpenClaw/ownership/managed health;
- Task-205 inert-state confirmation;
- SQLite integrity;
- exact mutation ledger;
- final disposition.

Stop after publishing the report for ChatGPT review.
