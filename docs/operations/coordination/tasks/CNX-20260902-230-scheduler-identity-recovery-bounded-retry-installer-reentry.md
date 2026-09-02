# CNX-20260902-230 — Scheduler Identity Recovery + Bounded-Retry Installer Re-entry

Status: `READY_FOR_HERMES`
Date: 2026-09-02 ICT
Parent: `CNX-20260902-229`
Repair parent: `CNX-20260902-226`
Failure parent: `CNX-20260902-223`
Forensic parents: `CNX-20260902-224`, `CNX-20260902-227`, `CNX-20260902-228`, `CNX-20260902-229`
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Purpose

Recover from Task 229's Windows Scheduled Task registration/tooling failure without changing product source and then, only after a harmless scheduler canary proves a correct current-user principal/topology, complete exactly one already-exact installer re-entry.

Task 230 is also a controlled trial of a **bounded tooling retry policy** requested by the user. The executor may adapt and retry tooling/launcher/registration operations when they fail before installer start, but every retry must be evidence-driven, finite, and fully reported.

The retry policy does **not** authorize a second installer start or installer invocation.

## Parent review authority

Task-229 report:

`docs/operations/coordination/reports/CNX-20260902-229-already-exact-windows-installer-reentry-completion.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260902-229-already-exact-windows-installer-reentry-completion-review.md`

Accepted review verdict:

`REJECT_COMPLIANCE__ACCEPT_FAIL_CLOSED_PRODUCT_PRESERVATION__BOUNDED_TOOLING_RETRY_SUCCESSOR_REQUIRED`

Task 229 preserved product state but exceeded its original registration stop boundary by attempting multiple registration methods. Task 230 explicitly authorizes bounded retries so adaptation is no longer implicit or out-of-contract.

## Exact product/source authority

Use exact repaired source commit:

`9a8510f1317c8e53c01c233b080ec20357cd22df`

Accepted plugin payload fingerprint:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No public Release/tag/asset mutation is authorized.

## Historical scheduler authority

Task 215 previously proved on this same Windows host that a direct Scheduled Task can run Windows PowerShell for sustained execution and propagate terminal code `23` using an Interactive/Limited principal.

Accepted historical shape:

```text
Execute: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
Principal: CDQ-P / Interactive / Limited
ExecutionTimeLimit: PT3M
AllowDemandStart: true
RestartCount: 0
LastTaskResult: 23
```

Important: `CDQ-P` in a report is a display label, not sufficient proof of the exact XML/UserId identity string. Task 230 must recover the canonical live identity/SID rather than hard-code a bare username.

Task 214 also proved that the Windows PowerShell cmdlet enum on this host accepts `Interactive`, not the attempted `InteractiveToken` cmdlet value.

Task 229 proved that:

- `New-ScheduledTaskSettingsSet -AllowDemandStart` is not supported by the local cmdlet surface;
- a later registration path failed at `UserId` with `HRESULT 0x80070057`;
- an attempted `schtasks.exe` equivalent also failed at `UserId`;
- no temporary task was created and installer invocation count remained zero.

Do not repeat the exact unsupported `-AllowDemandStart` cmdlet argument.

# Hard fences

## Authorized

- fresh GitHub/Actions/source reads;
- read-only Windows/runtime/product preflight and postflight;
- read-only inspection of retained Task-214/215 external harness evidence if still present;
- read-only current Windows identity/SID/session inspection;
- one disposable exact-first source checkout of `9a8510f...` under `%LOCALAPPDATA%\Temp`;
- candidate dependency/build/plugin validation in that disposable checkout;
- read-only plugin fingerprint/classification/action-resolution gates;
- bounded temporary scheduler **canary** registration attempts under the retry policy below;
- start of exactly one successfully qualified harmless canary task;
- cleanup of only temporary Task-230 canary tasks created by this task;
- bounded installer-task **registration-only** retries before any installer task start, under the retry policy below;
- exactly one installer Scheduled Task start;
- exactly one invocation of exact repaired `scripts/install.ps1`;
- passive observation and read-only retry of observer/query commands;
- cleanup of only the exact Task-230 installer harness after terminal evidence;
- coordination report publication.

## Not authorized

- second installer task start;
- second installer invocation;
- retry after installer process has been observed, regardless of terminal result;
- `-SkipPlugin`, `-SkipGatewayRestart`, `-SkipAgentsPolicy`, `-LinkPlugin` overrides;
- direct rollover prepare/finalize/plan/apply;
- manual OpenClaw plugin install/enable/disable/uninstall;
- manual stale Task-223 evidence mutation/cleanup/finalization;
- manual `cnxclaw` lifecycle repair;
- manual Gateway restart;
- ownership manifest write outside the installer;
- manual SQLite write;
- process termination;
- provider/model substitution;
- Discord Send/API semantic traffic;
- product/source/test/workflow edits;
- public Release/tag/asset mutation;
- force push/history rewrite;
- broad Scheduled Task deletion or modification of unrelated/product startup tasks.

Discord budget: `0 Sends`.

# Bounded tooling retry policy

## Retry eligibility gate

A tooling retry is allowed only while all remain true:

```text
installer task start count = 0
installer invocation count = 0
no installer process has been observed
no product/live mutation has occurred
failure is attributable to harness/tooling/registration/quoting/transport/observer mechanics
```

If any installer task start occurs or installer process is observed, set:

```text
INSTALLER_RETRY_GATE=CLOSED
```

It remains closed for the rest of Task 230.

## Retry classes and budgets

### A. Read-only probes / observer commands

Transient read-only command failures may be retried up to **2 additional times per logical observation** when the failure is transport, quoting, timeout or tool-surface related.

A retry must not repeat any side effect. Never restart a task merely because an observer/query failed.

### B. Harmless canary registration qualification

Maximum **4 registration attempts total**.

Each attempt must use a unique Task-230 canary task name and must change a material identity/API hypothesis based on evidence. Do not blindly rerun the same failed command.

If an attempt creates a task but readback is wrong, unregister only that exact task and prove absence before consuming the next attempt.

If an attempt fails before task creation, prove exact task absence before the next attempt.

Stop `BLOCKED_TOOLING_RETRY_EXHAUSTED` after the fourth failed registration attempt.

### C. Installer-task registration before start

After one canary topology is fully qualified, register the installer task using that proven principal/logon model.

Maximum **2 installer-task registration attempts total**, and only while start count remains zero.

A second registration attempt is allowed only if the first failed before installer start, the first task is proven absent/cleaned, and the retry changes only a tooling/API/serialization detail while preserving the already-qualified principal/logon semantics.

If both fail, stop `FAIL_INSTALLER_TASK_REGISTRATION`.

### D. Installer execution

```text
start budget = 1
installer invocation budget = 1
retry budget after start = 0
```

No exception.

## Mandatory attempt ledger

Report every mutable/tooling attempt in a table containing at least:

```text
attempt_id
phase
UTC time
method/API
identity form used (redact nothing except secrets; SID is not a secret)
hypothesis being tested
exact task name
command/settings summary
task created? yes/no
readback exact? yes/no
started? yes/no
result/error/HRESULT
cleanup performed + result
retry budget remaining
why the next method differs
```

Also report read-only observer retry counts separately.

At task end classify retry-policy usefulness as exactly one:

- `RETRY_POLICY_EFFECTIVE`
- `RETRY_POLICY_NOT_NEEDED`
- `RETRY_POLICY_EXHAUSTED_WITHOUT_RECOVERY`
- `RETRY_POLICY_STOPPED_BY_PRODUCT_BOUNDARY`

# Required execution flow

## Phase A — fresh authority and drift gate

Fresh-fetch branch HEAD, `ACTIVE.md`, Task 229 report/review and Task 230.

Require repair commit `9a8510f...` to remain an ancestor and compare `9a8510f... -> current HEAD` for product/source/test/workflow drift. Coordination-only drift is acceptable; material product drift blocks.

Check current Actions. Do not claim GREEN for an in-progress run.

Verify public `v0.9.3` remains immutable.

## Phase B — live preflight preservation

Capture read-only:

```text
controller mode/generation
startup adapter/task
Supervisor
AGENTS managed policy
installed plugin path/source/status/enabled/fingerprint
Gateway health
selected provider/Ollama
Delivery readiness/pending
Recovery readiness
SQLite integrity + durable counts
installer/lifecycle process residue
Task-230 task namespace absence
```

Expected historical shape from Task 229:

```text
controller=passthrough
generation=33
startup adapter absent
Gateway healthy
provider=ollama
Delivery=READY pending=0
Recovery=READY
SQLite integrity=ok
installed plugin fingerprint=e3bcce04...
```

Fresh state is authoritative. Material drift: `BLOCKED_PREFLIGHT_DRIFT`.

## Phase C — immutable Task-223 evidence proof

Re-hash Task-223 transaction, matching inventory, ownership manifest and backup.

Accepted identities:

```text
transaction SHA-256:
ec1b32ec2813e1b4e2c220679f39c6922789b7d77e88ec9ca4ad6ba82ccac510

inventory SHA-256:
1a7299f926cda4e3f936577204c50059e0e4e716f8594535d4b3c40c40e51477

ownership manifest SHA-256:
081961df81f9bced0e4e72cf0bb4144e518e741ea9c010b4d7674404a1f247b6

backup project-tree:
7394401cb0ae9791c1c9b98661a9bf9df47ecb83c0b139b46cd742b17ee7342a

backup payload fingerprint:
f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
```

Any drift: `BLOCKED_STALE_EVIDENCE_DRIFT`.

Never mutate these artifacts.

## Phase D — exact repaired candidate + already-exact gate

Materialize exact-first `9a8510f...`, clean and detached.

Run supported dependency/build/plugin validation needed for candidate truth.

Require source and installed plugin fingerprint:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

Require repaired source contains:

`pre-install backup project-tree attestation mismatch`

Run actual read-only `classify-install` and production action resolver.

Require exactly:

```text
mode=upgrade
pendingRollover=false
pluginAlreadyExact=true
installPlugin=false
rolloverPlugin=false
skipPlugin=false
```

Mismatch: `FAIL_ALREADY_EXACT_GATE`.

No scheduler mutation is allowed before this gate passes.

## Phase E — reconstruct canonical scheduler identity

Before any registration, capture live identity from Windows itself:

- `[System.Security.Principal.WindowsIdentity]::GetCurrent().Name`;
- `[System.Security.Principal.WindowsIdentity]::GetCurrent().User.Value`;
- `whoami`;
- `whoami /user`;
- machine/domain context needed to explain the domain-qualified principal;
- current interactive session identity if available read-only.

If retained Task-214/215 harness evidence contains task XML/readback, inspect it read-only and extract the exact historical `<UserId>`, `<LogonType>`, run level and settings. Prefer this proven identity over report display text.

Record differences between:

```text
bare username
WindowsIdentity.Name
SID
historical Task-215 XML UserId (if available)
```

Do not assume they are interchangeable.

## Phase F — harmless canary registration with bounded adaptation

Create one harmless direct PowerShell canary script under Task-230 external evidence storage. It must:

- write start identity/PID/timestamp;
- write a terminal marker;
- write intended exit code `23`;
- exit `23`;
- reference no product path.

Use the bounded canary registration budget.

Evidence-driven identity/API strategy may include, as justified by live evidence:

1. the exact UserId/principal recovered from Task-215 XML;
2. current Windows SID with Interactive/Limited semantics where the chosen API supports SID identity;
3. current domain-qualified `WindowsIdentity.Name` with Interactive/Limited semantics;
4. an alternate Task Scheduler API/serialization surface using the same proven identity semantics.

Do not retry the exact Task-229 unsupported `New-ScheduledTaskSettingsSet -AllowDemandStart` invocation.

For each failed attempt, capture exact HRESULT/message and task-presence proof before adapting.

Once one task registers with exact readback, start that canary exactly once and require:

```text
start marker present
terminal marker present
intended exit code = 23
terminal/non-running scheduler state
LastTaskResult = 23 or rigorously equivalent scheduler evidence
start count = 1
```

Then unregister that exact canary and prove absence.

If registration budget exhausts: `BLOCKED_TOOLING_RETRY_EXHAUSTED`.

If registration succeeds but canary execution/terminal propagation fails: `FAIL_CANARY_EXECUTION`.

Do not proceed to installer registration unless canary fully passes.

## Phase G — register one installer task using proven identity

Create a new unique Task-230 installer task whose direct action is Windows PowerShell and whose runner invokes exact repaired `scripts/install.ps1` synchronously in the same task host/process scope, with durable stdout/stderr/stage/terminal evidence.

Use the exact principal/logon semantics that passed Phase F.

Do not add unsupported settings merely because a historical report displayed them. Require semantic equivalents by task readback/XML.

Installer task requirements:

```text
manual/demand start
no recurrence/repetition
automatic restart/retry disabled
ExecutionTimeLimit >= PT30M
absolute Windows PowerShell path
exact 9a8510f source path
no nested detached installer process
```

Use installer-task registration retry budget max 2 before start.

Require exact readback before start.

## Phase H — exactly one installer start/invocation

Immediately before start, recheck:

```text
already-exact gate still true
retained evidence unchanged
installer start count=0
installer invocation count=0
```

Start installer Scheduled Task exactly once.

After this point:

```text
INSTALLER_RETRY_GATE=CLOSED
```

Passive/read-only observer commands may retry under the observer policy, but never start the task again and never invoke installer directly.

## Phase I — terminal/control-flow proof

Require installer transcript/stages prove zero live plugin/rollover mutation:

```text
openclaw plugins install = 0
rollover-prepare = 0
rollover-finalize = 0
rollover-plan/apply = 0
```

Require terminal success:

```text
installer success marker present
no open diagnostic stage
scheduler terminal/non-running
LastTaskResult=0 or rigorously equivalent success
installer invocation count=1
installer task start count=1
```

Nonzero/incomplete terminal result: `FAIL_INSTALLER_TERMINAL` and stop. No retry.

## Phase J — exact harness cleanup

Unregister only the exact Task-230 installer task after terminal evidence. Prove absence and natural process disappearance.

No process termination.

Failure: `FAIL_TASK_CLEANUP`.

## Phase K — post-install provenance and health

Read-only verify:

- live plugin remains canonical direct path and fingerprint `e3bcce04...`;
- live workspace ownership source byte hash equals exact `9a8510f...` candidate source;
- Task-226 fail-closed contract is live;
- ownership manifest verifies;
- no new rollover transaction was created by Task 230;
- historical Task-223 evidence remains unchanged;
- controller/startup/Supervisor/AGENTS policy state is coherent with successful installer contract;
- Gateway healthy;
- provider remains Ollama and healthy;
- Delivery READY;
- Recovery READY;
- SQLite integrity ok;
- no new nonterminal residue attributable to install;
- Discord Sends/API semantic traffic = 0.

Do not manually repair an unhealthy post-state.

## Phase L — final immutable-evidence + retry-policy assessment

Repeat all Task-223 hashes/fingerprints from Phase C.

Report complete retry/attempt ledger and classify retry-policy usefulness exactly.

Explain:

- which identity form/API finally worked;
- why earlier attempts failed;
- whether a retry changed a meaningful hypothesis or merely repeated a command;
- whether the bounded retry mechanism avoided an unnecessary new task cycle;
- whether any retry rule should be generalized into coordination policy later.

# Allowed dispositions

Primary task result must be one of:

- `PASS_ALREADY_EXACT_INSTALLER_REENTRY__RETRY_POLICY_EFFECTIVE`
- `PASS_ALREADY_EXACT_INSTALLER_REENTRY__RETRY_POLICY_NOT_NEEDED`
- `BLOCKED_PREFLIGHT_DRIFT`
- `BLOCKED_STALE_EVIDENCE_DRIFT`
- `FAIL_SOURCE_PROVENANCE`
- `FAIL_ALREADY_EXACT_GATE`
- `BLOCKED_TOOLING_RETRY_EXHAUSTED`
- `FAIL_CANARY_EXECUTION`
- `FAIL_INSTALLER_TASK_REGISTRATION`
- `FAIL_INSTALLER_TERMINAL`
- `FAIL_TASK_CLEANUP`
- `FAIL_POST_INSTALL_PROVENANCE`
- `FAIL_POST_INSTALL_HEALTH`
- `FAIL_STALE_EVIDENCE_PRESERVATION`
- `BLOCKED_EVIDENCE`

Any failure after installer start must report retry policy as `RETRY_POLICY_STOPPED_BY_PRODUCT_BOUNDARY` and must not retry installer execution.

# Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260902-230-scheduler-identity-recovery-bounded-retry-installer-reentry.md`

Include:

- fresh exact branch HEAD and Actions state;
- exact source/candidate provenance;
- live Windows identity/SID evidence;
- Task-215 XML identity evidence if available;
- already-exact gate outputs;
- full canary and installer registration attempt ledger;
- read-only observer retry counts;
- canary start/terminal proof;
- installer task exact readback;
- installer start/invocation counts;
- installer transcript/stage/terminal proof;
- plugin/rollover mutation counts;
- before/after product/runtime/SQLite/retained-evidence state;
- Discord send count;
- retry-policy usefulness classification;
- exact cleanup result.

Then stop for independent ChatGPT review before any semantic/durable-delivery acceptance, stale-evidence cleanup or additional live mutation.
