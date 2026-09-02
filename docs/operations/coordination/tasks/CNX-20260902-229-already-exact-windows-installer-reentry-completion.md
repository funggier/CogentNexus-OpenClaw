# CNX-20260902-229 — Already-Exact Windows Installer Re-entry Completion

Status: `READY_FOR_HERMES`
Date: 2026-09-02 ICT
Parent: `CNX-20260902-228`
Repair parent: `CNX-20260902-226`
Failure parent: `CNX-20260902-223`
Forensic parents: `CNX-20260902-224`, `CNX-20260902-227`, `CNX-20260902-228`
Parent umbrella: `CNX-20260831-188`
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Purpose

Complete the interrupted Task-223 install-over through the supported **already-exact installer re-entry** path, using the exact repaired Task-226 source.

This task authorizes exactly **one** normal installer invocation, only after fresh read-only preflight proves all already-exact invariants. It does not authorize plugin replacement, rollover prepare/finalize, stale-evidence cleanup, manual lifecycle repair, Discord traffic, Release mutation, or retry after a failed installer attempt.

Expected pre-install classification/action contract:

```text
mode=upgrade
pendingRollover=false
pluginAlreadyExact=true
installPlugin=false
rolloverPlugin=false
```

The one installer invocation may perform its documented non-plugin installation, skill replacement, ownership/policy, host enable/startup/Supervisor/Gateway lifecycle and validation. No manual repair outside that invocation is authorized.

## Accepted parent authority

Task-228 report:

`docs/operations/coordination/reports/CNX-20260902-228-retained-inventory-provenance-reconciliation.md`

Task-228 independent review:

`docs/operations/coordination/reviews/CNX-20260902-228-retained-inventory-provenance-reconciliation-review.md`

Accepted review disposition:

`ACCEPT_PASS_HISTORICAL_TASK223_ARTIFACT_RECONCILED__ONE_CONTROLLED_ALREADY_EXACT_INSTALLER_REENTRY_AUTHORIZED`

## Exact repaired installer source authority

Use exact source commit:

`9a8510f1317c8e53c01c233b080ec20357cd22df`

This is the accepted Task-226 producer repair.

Do **not** use the older Task-223 source `a812f278...` for the live re-entry. Even with plugin installation skipped, `scripts/install.ps1` installs/copies the source skill tree into the live workspace; the repaired ownership implementation must become live authority.

Accepted plugin payload fingerprint remains:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No public Release/tag/asset mutation is authorized.

## Accepted CI authority

Task-228 report HEAD `11f788159aadb943bedb8a65ada8f1d0670c5756` is product-equivalent to repair commit `9a8510f...` except coordination files and has fresh successful workflows:

```text
Validate:                      33646023883  SUCCESS
Windows Installer Pack Smoke: 33646023869  SUCCESS
PS5.1 Acceptance Smoke:        33646023697  SUCCESS
```

Before execution, fresh GitHub authority remains mandatory.

## Historical stale evidence — preservation only

Task-223 transaction:

`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\install-staging\plugin-rollover-transaction-8469daf5669242189f18e8c87ed9a86c.json`

Accepted SHA-256:

`ec1b32ec2813e1b4e2c220679f39c6922789b7d77e88ec9ca4ad6ba82ccac510`

Task-223 matching inventory:

`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\install-staging\plugin-inventory-8469daf5669242189f18e8c87ed9a86c.json`

Accepted SHA-256:

`1a7299f926cda4e3f936577204c50059e0e4e716f8594535d4b3c40c40e51477`

Task-223 backup:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\plugin-generation-rollover-backups\cogentnexus-openclaw-8469daf5669242189f18e8c87ed9a86c`

Accepted proof:

```text
project-tree SHA-256: 7394401cb0ae9791c1c9b98661a9bf9df47ecb83c0b139b46cd742b17ee7342a
payload fingerprint: f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
```

These are immutable forensic evidence for this task. Do not finalize, edit, move, rename, delete, archive, replace, or reuse them.

# Hard fences

Authorized:

- fresh GitHub/Actions/source authority reads;
- read-only Windows preflight and postflight inspection;
- one unique disposable exact-first checkout of `9a8510f...` under `%LOCALAPPDATA%\Temp`;
- candidate dependency/build/plugin validation inside that disposable checkout;
- read-only candidate/live plugin fingerprint calculations;
- read-only `classify-install` before mutation;
- pure `resolve-plugin-lifecycle-actions.ps1` execution before mutation;
- one unique temporary Task-229 Windows Scheduled Task using the previously qualified direct PowerShell topology;
- exactly one invocation of exact repaired `scripts/install.ps1` against the normal workspace;
- passive Task Scheduler/process/transcript/stage observation;
- cleanup of only the Task-229 temporary harness after terminal evidence;
- read-only post-install provenance/runtime/health/evidence verification;
- coordination report publication.

Not authorized:

- a second installer invocation or retry;
- `-SkipPlugin`, `-SkipGatewayRestart`, `-SkipAgentsPolicy`, or `-LinkPlugin` override flags;
- direct `rollover-prepare`, `rollover-finalize`, `rollover-plan`, or `rollover-apply` invocation;
- manual `openclaw plugins install/enable/disable/uninstall`;
- manual stale transaction/inventory/backup cleanup or finalization;
- manual `cnxclaw enable/disable/start/stop/restart/reset/uninstall`;
- manual Gateway restart;
- manual ownership manifest or SQLite writes;
- process termination except normal disappearance of the temporary task process; do not kill it;
- provider/model substitution;
- Discord Send/API semantic traffic;
- public Release/tag/asset mutation;
- product/source/test/workflow edits;
- force push/history rewrite.

Discord budget: `0 Sends`.

# Required execution flow

## Phase A — fresh GitHub and live preflight gate

Before creating the candidate checkout or Task-229 Scheduled Task:

1. fetch fresh branch HEAD;
2. verify Task 229 is active and `READY_FOR_HERMES`;
3. verify exact repair commit `9a8510f...` is an ancestor of current branch HEAD;
4. compare `9a8510f... -> HEAD` and require no product/source/test/workflow drift after the repair beyond coordination files;
5. verify public `v0.9.3` remains unchanged;
6. verify accepted CI authority remains successful;
7. capture fresh read-only Windows state.

Minimum live preflight:

```text
controller mode + generation
startup adapter/task state
Supervisor state
AGENTS managed-policy state
installed plugin id/version/path/source/enabled/status/fingerprint
Gateway health
provider/Ollama health and selected policy
Delivery readiness + pending count
Recovery readiness
SQLite integrity + durable counts
Task-205 historical cancellation/inertness
relevant installer/lifecycle process residue
Task-229 temporary task absence
```

Expected historical state is PASSTHROUGH generation 33, startup absent, exact direct plugin present, Gateway/Ollama healthy, Delivery/Recovery READY, SQLite integrity ok. Fresh state is authoritative.

Stop before any mutation as `BLOCKED_PREFLIGHT_DRIFT` if state materially differs or there is an emittable recovery/Discord hazard.

## Phase B — preserve stale evidence before mutation

Read/hash the exact Task-223 transaction, inventory and backup without modifying them.

Require exact accepted identities listed above.

Also record transaction fields showing the known producer-defect mismatch:

```text
backupProjectTreeSha256  = 7394401cb0ae9791c1c9b98661a9bf9df47ecb83c0b139b46cd742b17ee7342a
retiredProjectTreeSha256 = ca74a262293d49b058fce6221db2fa5311214cde567ebb331ff845670c5a2cab
```

If any retained evidence identity changed, stop:

`BLOCKED_STALE_EVIDENCE_DRIFT`

Do not normalize or clean it.

## Phase C — exact-first repaired source materialization

Create a new unique disposable source root under `%LOCALAPPDATA%\Temp`.

The first working-tree materialization must be exact repair commit:

`9a8510f1317c8e53c01c233b080ec20357cd22df`

Use an exact-first topology such as:

```text
git clone --no-tags --no-checkout <repo> <source-root>
git checkout --detach 9a8510f1317c8e53c01c233b080ec20357cd22df
```

or equivalent init/fetch/first-checkout flow.

Record:

```text
HEAD
remote URL
git status --porcelain=v2
relevant EOL/attribute state
```

Require exact clean source. If not exact:

`FAIL_SOURCE_PROVENANCE`

## Phase D — candidate/plugin and repaired-source proof

From exact `9a8510f...` source:

- perform repository-supported plugin dependency/build/validation needed by installer classification;
- compute source plugin fingerprint with the exact ownership helper;
- require fingerprint exactly `e3bcce04...`;
- independently compute current installed direct plugin fingerprint and require the same value;
- hash candidate `skills/cogentnexus-openclaw/scripts/namespace_ownership.py` for post-install comparison;
- prove candidate contains the Task-226 fail-closed string/contract without modifying it:
  `pre-install backup project-tree attestation mismatch`.

Any mismatch stops before installer:

`FAIL_SOURCE_PROVENANCE`

## Phase E — mandatory read-only already-exact gate

Capture fresh `openclaw plugins list --json` to an external Task-229 evidence directory.

Run exact candidate `namespace_ownership.py classify-install` read-only with:

- normal workspace;
- normal application-data root;
- captured inventory;
- expected replacement fingerprint `e3bcce04...`.

Require exactly:

```text
mode=upgrade
pendingRollover=false
pluginAlreadyExact=true
manifestPluginPath = canonical direct plugin path
replacementPluginPath = same canonical direct plugin path
```

Then run exact candidate production action resolver purely/read-only with the returned state and no skip flags.

Require exactly:

```text
installPlugin=false
rolloverPlugin=false
skipPlugin=false
```

If any value differs, stop before installer:

`FAIL_ALREADY_EXACT_GATE`

Do not attempt a normal changed-source rollover and do not create any transaction.

## Phase F — prepare one direct Scheduled Task harness

Use the Task-215/Task-223 qualified topology: one uniquely named manual-start Windows Scheduled Task whose top-level action is Windows PowerShell and whose installer runs in that same host/process scope.

Create an external evidence root, e.g.:

`%LOCALAPPDATA%\Temp\cnx229-already-exact-reentry-<timestamp>`

Requirements:

- one-shot/manual start only;
- no recurrence;
- no automatic retry;
- `ExecutionTimeLimit >= PT30M`;
- absolute Windows PowerShell path;
- exact `9a8510f...` source runner/install script path;
- no detached/nested second PowerShell installer process;
- read back task action/principal/settings before start;
- do not reuse or alter the product startup Scheduled Task.

If registration/readback is not exact, remove only the temporary Task-229 task and stop:

`FAIL_TASK_REGISTRATION`

## Phase G — invoke installer exactly once

Invoke exact repaired:

`scripts/install.ps1`

against the normal workspace with **no override switches**:

```text
no -SkipPlugin
no -SkipGatewayRestart
no -SkipAgentsPolicy
no -LinkPlugin
```

Start the Task-229 Scheduled Task exactly once.

Never retry in Task 229.

Passive observation must preserve:

```text
registration count = 1
start count = 1
installer invocation count = 1
```

Do not kill/restart the task if observer calls time out.

## Phase H — installer stage/control-flow proof

Capture full installer transcript/stage evidence.

Because the preflight action is already-exact, require that the live invocation performs **zero** of the following external plugin/rollover mutations:

```text
openclaw plugins install
plugin-rollover-prepare
plugin-rollover-finalize
rollover-plan
rollover-apply
```

It is acceptable for candidate dependency/build/plugin validation to occur in the disposable source or documented installer pre-classification phase.

The installer may perform its documented remaining operations, including skill staging/replacement, runtime ownership verification/publication, managed policy integration, Host enable/startup/Supervisor/Gateway lifecycle and final status/doctor validation.

Require terminal evidence:

- no unclosed installer diagnostic stage;
- final installer success marker;
- Scheduled Task returns terminal/non-running;
- `LastTaskResult = 0` or rigorously equivalent success;
- no second start/retry.

Any nonzero/incomplete terminal result:

`FAIL_INSTALLER_TERMINAL`

Do not repair or retry.

## Phase I — clean only Task-229 harness

After terminal evidence:

- unregister only the exact Task-229 temporary Scheduled Task;
- prove it absent;
- prove its runner/installer PID is absent naturally;
- retain external evidence/log directory;
- do not terminate a process manually;
- do not alter product startup task.

Failure here:

`FAIL_TASK_CLEANUP`

## Phase J — post-install exact provenance

Read-only verify after installer success:

1. live plugin remains canonical direct `cogentnexus-openclaw` v0.9.3;
2. live plugin payload fingerprint remains exactly `e3bcce04...`;
3. no plugin replacement generation was created;
4. live workspace skill `scripts/namespace_ownership.py` byte hash equals the exact `9a8510f...` candidate file hash captured in Phase D;
5. live installed ownership source contains the Task-226 fail-closed contract;
6. ownership manifest verifies exactly and binds the canonical installed plugin;
7. no new/current rollover transaction was created by Task 229;
8. historical Task-223 transaction/inventory/backup remain byte/tree identical.

Any mismatch:

`FAIL_POST_INSTALL_PROVENANCE`

Do not repair manually.

## Phase K — post-install lifecycle and health

Record actual resulting state; do not invent an expected generation number.

Require the documented normal installer result to be coherent:

```text
controller: healthy managed/runtime-ready state consistent with installer contract
startup adapter/task: coherent with enabled managed state
Supervisor: healthy/doctor PASS
AGENTS managed policy: installed/verified as contract requires
Gateway: healthy
provider: Ollama, unchanged and healthy
Delivery: READY
Recovery: READY
SQLite: integrity ok
no new nonterminal stale Ticket/outbox/recovery residue attributable to install
Task-205 historical cancellation remains inert
Discord Sends/API semantic traffic: 0
```

If installer terminal PASS but lifecycle/health is not coherent:

`FAIL_POST_INSTALL_HEALTH`

No ad-hoc lifecycle repair is authorized.

## Phase L — final stale-evidence preservation proof

Recompute:

- Task-223 transaction SHA;
- Task-223 inventory SHA;
- backup project-tree SHA;
- backup payload fingerprint.

Require exact preflight identities.

The old transaction remains obsolete forensic evidence even after successful current installation. Do not remove it in Task 229.

If it changed unexpectedly:

`FAIL_STALE_EVIDENCE_PRESERVATION`

## Mutation ledger

Report exact counts for:

```text
installer invocations
Task-229 Scheduled Task registrations
Task-229 Scheduled Task starts
Task-229 Scheduled Task deletions
openclaw plugins install invocations
rollover-prepare invocations
rollover-finalize invocations
manual cnxclaw lifecycle actions
manual Gateway restarts
manual stale-evidence writes/deletes/moves
manual SQLite writes
process terminations
provider/model substitutions
Discord Sends/API semantic traffic
Release/tag/asset mutations
product/source/test/workflow edits
```

Expected:

```text
installer invocations: 1
Task-229 registrations: 1
Task-229 starts: 1
Task-229 deletions: 1 after terminal evidence
openclaw plugins install: 0
rollover-prepare: 0
rollover-finalize: 0
manual lifecycle/Gateway/stale-evidence/SQLite/process/provider/Discord/Release/source mutations: 0
```

Installer-owned documented non-plugin/lifecycle mutations must be listed separately from manual mutation counts.

## Allowed final dispositions

Use one primary disposition:

- `PASS_ALREADY_EXACT_WINDOWS_INSTALLER_REENTRY_COMPLETED`
- `BLOCKED_PREFLIGHT_DRIFT`
- `BLOCKED_STALE_EVIDENCE_DRIFT`
- `FAIL_SOURCE_PROVENANCE`
- `FAIL_ALREADY_EXACT_GATE`
- `FAIL_TASK_REGISTRATION`
- `FAIL_INSTALLER_TERMINAL`
- `FAIL_TASK_CLEANUP`
- `FAIL_POST_INSTALL_PROVENANCE`
- `FAIL_POST_INSTALL_HEALTH`
- `FAIL_STALE_EVIDENCE_PRESERVATION`
- `BLOCKED_EVIDENCE`

## Stop boundary

Publish:

`docs/operations/coordination/reports/CNX-20260902-229-already-exact-windows-installer-reentry-completion.md`

Then stop for independent ChatGPT review.

Even after PASS:

- do not clean the historical Task-223 evidence;
- do not send Dashboard/Discord semantic traffic;
- do not reset/uninstall/reinstall;
- do not mutate public Release/tag/asset state;
- do not begin final semantic/durable-delivery acceptance automatically.
