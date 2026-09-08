# CNX-20260902-223 — Task-222 Exact Candidate Windows Install-Over Requalification

Status: `READY_FOR_HERMES`
Date: 2026-09-02 ICT
Parent: `CNX-20260901-222`
Repair parent: `CNX-20260831-198`
Parent umbrella: `CNX-20260831-188`
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Purpose

Requalify a real Windows install-over using the exact Task-222 repository/package candidate after the package-determinism blocker was closed.

This task is installer/provenance/runtime-health only. It authorizes exactly one installer invocation through the direct Windows Scheduled Task topology qualified by Task 215. It does **not** authorize Discord semantic traffic, reset, uninstall, fresh reinstall, Release/tag mutation, or product-source repair.

## Immutable publication authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No public tag, Release, or asset mutation is authorized.

## Exact installer candidate authority

Source candidate:

`a812f27815b3c87b7ca748dc2dea88f987601f70`

Accepted package proof:

```text
artifact ID: 9810139538
artifact digest: sha256:3164b7770e7d8991691d7bbedced092866c208add72b0c03b4aa3d39d1b50ff0
sourceCommit: a812f27815b3c87b7ca748dc2dea88f987601f70
packageVersion: 0.9.3
payloadFileCount: 192
payloadV2Fingerprint: e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
tar.gz SHA-256: 88f1c81d5c68da11e7420388a215bf8b72c55a30e7924f24cf6a83b8912a7494
zip SHA-256: 011aaff51462c47440d973a348b938b12a3c2aadcbbe436acf5d54d9f2ad003d
```

Authoritative CI on the exact candidate:

```text
Validate:                      33532084137  success
Windows Installer Pack Smoke: 33532084225  success
PS5.1 Acceptance Smoke:        33532084092  success
```

Task-222 review disposition:

`ACCEPT_PASS_STATIC_BYTE_GUARD__CI_WINDOWS_PAYLOAD_IDENTITY_EQUAL__WINDOWS_INSTALLER_REQUALIFICATION_AUTHORIZED`

## Historical execution boundaries that MUST be preserved

### Task 215 launcher qualification

The accepted durable launcher is a uniquely named one-shot Windows Scheduled Task whose top-level action is PowerShell and whose terminal result is observable through Task Scheduler. The direct action proved durable output and terminal result propagation.

Do **not** use the failed detached Python `Popen` topology from Tasks 212–213.

Do **not** introduce a nested detached PowerShell process or a wrapper topology equivalent to the failed Task-214 nested-child design.

### Task 221 exact-first checkout boundary

Do **not** clone/materialize the current branch working tree and then detach backward to the candidate.

The candidate must be selected before first working-tree materialization, for example:

```text
git clone --no-tags --no-checkout <repo> <source-root>
git checkout --detach a812f27815b3c87b7ca748dc2dea88f987601f70
```

or an equivalent `git init` + fetch exact SHA + first checkout topology.

### Task-205 delayed-output boundary

The historical Task-205 Ticket/recovery was cancelled through the supported cancellation boundary and must remain inert. Do not cancel it again and do not emit any Discord traffic during Task 223.

## Discord budget

`0 Sends`.

Any Discord/API semantic output is a task violation.

# Hard fences

Authorized:

- read-only preflight inspection of live controller/startup/Gateway/provider/delivery/recovery/SQLite state;
- one disposable exact-first candidate source root under `%LOCALAPPDATA%\Temp`;
- isolated candidate dependency/build/package/provenance verification;
- one uniquely named temporary Task-223 Scheduled Task;
- one harmless Task-223 runner script/evidence directory outside product paths;
- exactly one invocation of the exact candidate `scripts/install.ps1` against the normal workspace;
- passive observation of installer process/task/log/stage evidence;
- exact temporary Scheduled Task cleanup after terminal evidence;
- read-only post-install provenance/runtime-health verification;
- coordination report publication.

Not authorized:

- installer retry or second installer invocation;
- reset/uninstall/fresh reinstall;
- manual `cnxclaw enable/disable/start/stop/restart` unless the installer itself performs its documented lifecycle as part of the one invocation;
- manual plugin/config/ownership/staging/SQLite mutation;
- manual Gateway restart;
- provider/model substitution;
- unrelated process termination;
- product/source/test/workflow edits;
- Release/tag/asset mutation;
- force push/history rewrite;
- Discord Send/API semantic traffic.

# Required execution flow

## Phase A — Fresh authority and preflight safety gate

Before any candidate build, Scheduled Task registration, or installer launch:

1. fetch fresh remote branch authority;
2. verify Task 223 is active and `READY_FOR_HERMES`;
3. record exact remote HEAD;
4. verify candidate `a812f278...` is an ancestor of current coordination HEAD;
5. compare candidate → current HEAD and require no product/source/test/workflow drift after candidate other than Task-222 report/review, Task-223 task, and coordination files;
6. verify public `v0.9.3` authority remains unchanged;
7. read current live state without mutation.

Required live preflight evidence:

- controller mode/generation;
- startup-adapter status;
- canonical installed plugin id/version/source/enabled/status;
- current live plugin payload fingerprint;
- Gateway health;
- selected provider/model policy; expected provider remains Ollama;
- Delivery readiness;
- Recovery readiness;
- SQLite read-only integrity and relevant durable counts/state;
- Task-205 Ticket/recovery remains cancelled/inert and scheduler does not select it;
- no relevant installer/lifecycle process residue;
- no Task-223 Scheduled Task already exists.

Historical expected baseline is PASSTHROUGH on the older installed generation with Gateway healthy and Delivery/Recovery READY, but **fresh evidence is authoritative**. If material drift creates uncertainty or an emittable recovery hazard, stop:

`BLOCKED_PREFLIGHT_DRIFT`

Do not repair the live system in this task merely to satisfy preflight.

## Phase B — Materialize the exact candidate correctly

Create a new unique disposable Task-223 source root under `%LOCALAPPDATA%\Temp`.

The exact candidate must be the first working-tree materialization. Record:

```text
HEAD
remote URL
git status --porcelain=v2
git config --show-origin --get-all core.autocrlf
git check-attr -a -- <four static identity paths>
git ls-files --eol -- <four static identity paths>
```

Required immediately after checkout:

- HEAD exactly `a812f27815b3c87b7ca748dc2dea88f987601f70`;
- tracked status clean;
- four static identity paths LF working-tree bytes;
- effective `text eol=lf` for the guarded paths.

If exact-first materialization cannot be established, stop before installer:

`FAIL_SOURCE_PROVENANCE`

## Phase C — Reprove candidate/package identity before installer

From the exact candidate source root, run the repository-supported preparation/validation needed by the installer/package contract, including the plugin dependency/build/validation path.

At minimum require:

- `npm ci` for the plugin succeeds;
- focused static-byte guard succeeds;
- normal plugin build/validation succeeds;
- generated `dist` canonicalization is idempotent on a second pass;
- repository-supported payload identity returns exactly 192 files and fingerprint:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

- tracked status remains clean;
- `scripts/install.ps1` is read from this exact candidate root, not a retained older checkout.

Where the retained CI artifact is available, compare the installable payload path set and bytes to the retained proof again. A mismatch against the accepted candidate identity is a hard stop:

`FAIL_CANDIDATE_IDENTITY`

No installer may run after an identity mismatch.

## Phase D — Prepare the direct Scheduled Task installer action

Create one external Task-223 evidence root, for example:

`%LOCALAPPDATA%\Temp\cnx223-install-over-<timestamp>`

Create a unique temporary Scheduled Task, for example:

`CogentNexus-OpenClaw-Task223-Installer-<suffix>`

Requirements:

- one-shot/manual start only;
- no recurrence;
- no automatic retry;
- `ExecutionTimeLimit` at least `PT30M`; prefer `PT45M` if supported;
- absolute Windows PowerShell executable path;
- exact candidate runner/install script paths quoted safely;
- Task action/principal/settings read back after registration and compared with intended values;
- no reuse or alteration of any product startup Scheduled Task.

### Same-process requirement

The top-level Scheduled Task action must use the direct PowerShell topology qualified by Task 215.

A Task-223 runner may be used only if it keeps the candidate `install.ps1` execution in the same PowerShell host/process scope (for example a normal PowerShell script invocation/call in the host) and exists only to persist evidence/transcript/identity. It must not launch a second detached PowerShell process.

The evidence must make it possible to prove:

- Scheduled Task action identity;
- top-level PowerShell PID/creation time/executable/arguments;
- installer source path from the exact candidate root;
- one invocation count;
- durable stdout/stderr or transcript growth;
- terminal Scheduler state and `LastTaskResult`.

If the exact registered action cannot be read back or the topology is not proven, delete only the temporary Task-223 task and stop:

`FAIL_TASK_REGISTRATION`

## Phase E — Launch exactly once and observe without interference

Start the exact Task-223 Scheduled Task **once**.

Record the start count and `LastRunTime`. Never start it a second time in this task.

Observe independently through Task Scheduler and process/log evidence at useful intervals. Historical successful installs can exceed 10 minutes, so the observer must allow the configured execution window and must not infer failure merely because one foreground tool call times out or disconnects.

Observer timeout/reconnect MUST NOT:

- stop the installer;
- restart the task;
- create another Scheduled Task;
- kill the process;
- launch a second installer.

Required terminal installer evidence:

- exactly one Task-223 start/invocation;
- top-level process identity bound to the registered action;
- installer transcript/log is non-empty and grows;
- all installer stage `START` markers emitted by the candidate have corresponding terminal `COMPLETE`/success evidence; no unresolved stage remains;
- final installer success marker is present;
- Scheduled Task returns to non-running/Ready terminal state;
- `LastTaskResult = 0` or a rigorously documented equivalent success code;
- no automatic retry/second run occurred.

If the installer terminates nonzero, terminal evidence is incomplete, or invocation count exceeds one:

`FAIL_INSTALLER_TERMINAL`

Do not retry.

## Phase F — Clean up only the temporary Task-223 harness

After terminal evidence has been captured:

1. unregister only the exact Task-223 temporary Scheduled Task;
2. prove it is absent;
3. prove no Task-223 runner/installer process remains;
4. retain the external evidence directory and logs;
5. do not delete/alter the product startup task.

Failure to remove the temporary harness cleanly is:

`FAIL_TASK_CLEANUP`

and does not authorize unrelated cleanup.

## Phase G — Post-install exact provenance and runtime-health gate

Perform read-only verification after the single successful installer invocation.

### Installed provenance

Require:

- canonical plugin id is `cogentnexus-openclaw`;
- installed version is `0.9.3`;
- installed payload fingerprint exactly:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

- installed source/provenance binds to exact candidate `a812f27815b3c87b7ca748dc2dea88f987601f70` according to repository-supported installer provenance records;
- no pending/incomplete rollover transaction or ambiguous replacement path remains;
- no old-generation fingerprint is being reported as the installed candidate.

Any installed fingerprint/source mismatch is:

`FAIL_INSTALLED_PROVENANCE`

Do not repair it manually in this task.

### Runtime health

Read the installer’s documented resulting controller/startup state rather than assuming from history. Require the resulting state to be internally consistent with the install contract and healthy enough for the later semantic requalification.

At minimum record and require:

- controller state is not failed/inconsistent;
- startup adapter/task state is coherent with the installer contract;
- canonical plugin is loadable and expected enabled/managed state is reached if install-over contract specifies it;
- Gateway healthy;
- provider remains Ollama with accepted model policy; no substitution;
- Delivery READY;
- Recovery READY;
- SQLite integrity `ok`;
- no new nonterminal stale Ticket/recovery/outbox residue attributable to installation;
- Task-205 historical cancellation remains inert;
- no Discord traffic occurred.

If installer exit/provenance is PASS but resulting runtime health is not acceptable, classify:

`FAIL_POST_INSTALL_HEALTH`

Do not perform ad-hoc lifecycle repair within Task 223.

## Phase H — Mutation ledger

The report must record exact counts for:

```text
installer invocations
Task-223 Scheduled Task registrations
Task-223 Scheduled Task starts
Task-223 Scheduled Task deletions
manual cnxclaw lifecycle actions
manual Gateway restarts
manual plugin/config mutations
manual SQLite/ownership/staging writes
process terminations
provider/model substitutions
Discord Sends/API semantic traffic
Release/tag/asset mutations
product/source/test/workflow commits
```

Expected values:

```text
installer invocations: 1
Task-223 registrations: 1
Task-223 starts: 1
Task-223 deletions: 1 after terminal evidence
manual lifecycle/Gateway/plugin/SQLite/process/provider/Discord/Release/source mutations: 0
```

## Required evidence bundle

Retain at minimum:

1. fresh remote authority and compare;
2. preflight runtime snapshot;
3. exact-first clone/fetch commands and Git config/attribute/EOL/status output;
4. candidate validation and payload identity;
5. retained CI package-proof identity;
6. Task-223 runner/script hashes if a runner is used;
7. registered Scheduled Task action/principal/settings readback;
8. task/process identity samples;
9. complete installer transcript/stdout/stderr;
10. installer stage ledger;
11. Task Scheduler start/terminal state, LastRunTime and LastTaskResult;
12. task cleanup proof;
13. installed plugin provenance/fingerprint proof;
14. controller/startup/Gateway/Ollama/delivery/recovery/SQLite post-state;
15. Task-205 cancellation/inertness proof;
16. mutation ledger.

## Allowed final dispositions

Use exactly one primary disposition:

- `PASS_EXACT_CANDIDATE_WINDOWS_INSTALL_OVER_REQUALIFIED`
- `BLOCKED_PREFLIGHT_DRIFT`
- `FAIL_SOURCE_PROVENANCE`
- `FAIL_CANDIDATE_IDENTITY`
- `FAIL_TASK_REGISTRATION`
- `FAIL_INSTALLER_TERMINAL`
- `FAIL_TASK_CLEANUP`
- `FAIL_INSTALLED_PROVENANCE`
- `FAIL_POST_INSTALL_HEALTH`
- `BLOCKED_EVIDENCE`

## Stop boundary

Publish:

`docs/operations/coordination/reports/CNX-20260902-223-task222-exact-candidate-windows-install-over-requalification.md`

Then stop for independent ChatGPT review.

Even after PASS:

- do not send Discord traffic;
- do not reset/uninstall/reinstall;
- do not publish a Release/tag;
- do not start the final semantic acceptance automatically.

A separate successor task will authorize the one-Send Discord semantic/durable-delivery requalification if Task 223 passes independent review.
