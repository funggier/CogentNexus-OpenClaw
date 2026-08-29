# CNX-20260829-129 — Managed-State / State-Root Authority Read-Only Diagnosis

- Status: `READY_FOR_HERMES`
- Execution mode: `LIVE_WINDOWS_READONLY_DIAGNOSIS_ONLY`
- Owner / independent reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-29 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Determine why Task 128 observed `passthrough` / `selectedProvider=null` and could not prove the status-reported SQLite database even though Task 125's built-in cleanup had previously returned the installed system to a healthy managed Ollama baseline and the installed ownership/plugin/OpenClaw/Gateway/Ollama surfaces remained present and healthy.

This task is **forensic and read-only only**. It must establish the authoritative installed launcher → CLI → `--root` → controller/runtime/ownership/SQLite chain and classify whether Task-128's blocked preflight reflects:

1. genuine authoritative live state drift;
2. launcher/target/root mismatch;
3. alternate/stale `.cogentnexus-openclaw` root;
4. status/SQLite path interpretation defect;
5. scheduled-task/service authority mismatch;
6. another identifiable post-Task-125 transition.

It does **not** authorize correcting the state.

## Prior accepted facts

### Task 127 accepted repository candidate

- source candidate: `1b922bf400fdbccb1f9c7019b89b69fd67f44070`
- recovery harness: `scripts/test-v093-ollama-recovery-windows-v3.ps1`
- harness blob: `622f70b339fea0f2ef7c564253aa3c6bf90ffc97`
- package proof artifact: `9706878201`
- payload fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`

Task-127 independent review:

`docs/operations/coordination/reviews/CNX-20260829-127-recovery-harness-failclosed-contract-and-ci-proof-review.md`

### Task 128 safe block

Task-128 report:

`docs/operations/coordination/reports/CNX-20260829-128-v093-real-windows-recovery-reacceptance.md`

Task-128 independent review:

`docs/operations/coordination/reviews/CNX-20260829-128-v093-real-windows-recovery-reacceptance-review.md`

Accepted Task-128 facts:

- Task-128 recovery suite `0 / 1 launched`;
- confirmation prompt not reached;
- no lowercase `y` entered;
- baseline/gateway-crash/provider-crash/operator-stop all `0`;
- no lifecycle/provider/config/process mutation was authorized or performed;
- ownership verification and exact plugin fingerprint passed;
- OpenClaw `2026.7.1-2` remained present;
- Gateway and Ollama listeners/REST remained healthy;
- four-model inventory remained present;
- status reported `passthrough` and selected provider `null`;
- SQLite integrity was not established because the path used by the Task-128 probe did not exist.

Task 128 is closed. Do not resume it.

## Source authority facts to verify against the installed bytes

At accepted candidate `1b922bf...`, `scripts/install.ps1` constructs the installed launcher as follows:

- launcher path: `<Workspace>\cnxclaw.cmd`;
- CLI path: `<Workspace>\skills\cogentnexus-openclaw\scripts\cnxclaw_v093.py`;
- root argument: `<Workspace>\.cogentnexus-openclaw`;
- launcher invokes the owned foreground Python interpreter and appends `%*`.

`cnxclaw_v093.py` delegates global `--root` handling to the accepted backend, and `cnxclaw.py::parse_globals` resolves the explicit root and uses it for controller/provider/check operations.

These repository facts make current working directory alone an insufficient explanation **if and only if the installed launcher bytes actually match that contract**. Task 129 must prove the installed bytes and target literally rather than assume them.

## Historical consumed/live-operation ledger

Remain consumed and forbidden:

- Task-121 install-over `1 / 1`;
- Task-124 reset `1 / 1`;
- Task-124 uninstall `1 / 1`;
- Task-124 fresh reinstall `1 / 1`;
- Task-124 standalone stop/start/restart `1 / 1` each;
- Task-125 old-harness recovery suite `1 / 1`;
- Task-125 gateway-crash `1 / 1 PASS`;
- Task-125 provider-crash `1 / 1 old-harness convergence FAIL`;
- Task-128 repaired-harness recovery suite `0 / 1 launched`.

Task 129 authorizes **zero** lifecycle/recovery mutations.

## Phase 0 — authority and evidence root

1. Fresh-fetch GitHub coordination and confirm Task 129 remains authoritative and unsuperseded.
2. Record exact branch HEAD and accepted Task-127 candidate.
3. Create a fresh evidence directory under `%LOCALAPPDATA%\Temp` or another non-CNX-owned temporary location.
4. Record current date/time and Windows/PowerShell identity read-only.
5. Do not alter the installed workspace, CNX state, OpenClaw state, Ollama state, scheduled tasks, services, environment, or process state.

## Phase 1 — prove the installed launcher chain literally

Collect read-only evidence for:

1. Exact expected launcher path:
   `C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd` (derive from `$HOME`, do not hard-code user identity in logic).
2. `Test-Path`, file size, creation/write timestamps, SHA256, and complete textual bytes/content of that launcher.
3. `Get-Command cnxclaw.cmd -All` and any PATH-resolved aliases/wrappers with source paths.
4. Parse the installed launcher content and record literally:
   - foreground Python executable path;
   - `cnxclaw_v093.py` path;
   - explicit `--root` path;
   - `%*` forwarding.
5. Verify each parsed target exists; record file size/mtime/SHA256 for:
   - launcher;
   - installed `cnxclaw_v093.py`;
   - installed `cnxclaw.py`;
   - installed `host_control_v092.py` as relevant.
6. Compare the installed CLI source hashes/content identity against accepted candidate/package bytes where practical, without changing either copy.
7. Record current working directory separately to show whether it is or is not involved.

Do not execute any launcher other than the explicit installed launcher for authoritative probes below.

If the launcher points outside the installed workspace/state root, classify that fact immediately but continue read-only evidence collection.

## Phase 2 — authoritative root inventory

Using the **literal `--root` parsed from the installed launcher**, collect read-only filesystem metadata for the expected authoritative root and its important files/directories:

- `host\controller.json`;
- `runtime.json`;
- `ownership.json`;
- `state\cogent.db`;
- provider recovery state/ledger/incident files if present;
- supervisor health/state files if present;
- ticket/outbox/database paths relevant to status/check recovery;
- logs that can reveal a transition without requiring secret access.

For each relevant file, record:

- existence;
- absolute path;
- size;
- creation time;
- last-write time;
- SHA256 for ordinary files where safe/useful;
- parsed non-secret state fields required for diagnosis.

For `controller.json`, record at minimum:

- mode;
- selectedProvider;
- desiredGateway;
- desiredProvider;
- generation;
- updatedAt;
- providerTransition;
- providerSelection metadata if present.

For SQLite:

- first establish the exact authoritative path from source/status/root semantics;
- if the file exists, perform read-only SQLite integrity checking only (`PRAGMA integrity_check`/equivalent read-only invocation) and record result;
- do not create a missing database as a side effect;
- if using Python/sqlite3, open in URI read-only mode where feasible;
- if the path does not exist, record it as missing and do not initialize it.

## Phase 3 — enumerate competing roots without mutation

Search only bounded, relevant locations for other `.cogentnexus-openclaw` directories or controller/ownership files that could plausibly be mistaken for the installed state root, including:

- installed OpenClaw workspace;
- retained candidate/extraction/worktree locations already used by Tasks 121/123/128;
- `%LOCALAPPDATA%\CogentNexus-OpenClaw` only to classify app-data ownership/metadata;
- task/supervisor configured paths discovered from authoritative command lines.

Do **not** perform an unbounded whole-disk crawl.

For every competing candidate root found, record path, timestamps, key non-secret controller fields, ownership identity if present, and whether any installed launcher/task/service actually references it.

The goal is to distinguish an unused retained extraction from a live authority path.

## Phase 4 — explicit authoritative read-only command probes

Invoke **only the exact installed launcher path** determined in Phase 1, with direct argument-safe calls and captured literal command/path evidence:

- `cnxclaw.cmd status`;
- `cnxclaw.cmd provider status --json`;
- `cnxclaw.cmd check recovery --json` (allow its documented read-only nonzero verdict exit code);
- other strictly read-only component checks only if needed to resolve controller/SQLite/supervisor authority.

Requirements:

- do not call a PATH-ambiguous `cnxclaw.cmd` when collecting authoritative evidence;
- do not use a generic wrapper that can drop arguments;
- do not call a `cnxclaw_v093.py` located in a candidate checkout as a substitute for the installed launcher;
- if a controlled comparison against a retained candidate copy is useful, it must be separately labelled **non-authoritative comparison only**, use no mutating command, and must not be confused with installed evidence.

Compare command output paths/state with the literal root/controller files collected in Phase 2.

## Phase 5 — scheduled-task/service authority

Read-only inspect relevant Windows scheduled tasks/services, at minimum:

- `CogentNexus-OpenClaw-Supervisor`;
- OpenClaw Gateway task/service if present;
- any CNX-owned provider/recovery watcher task/service discovered.

Record:

- executable path;
- arguments;
- working directory if configured;
- task/service state;
- last run time/result where available;
- whether command lines reference the same installed workspace/root/CLI files proven above.

Do not start/stop/run/modify any task or service.

Also record relevant **non-secret** environment path overrides that can affect root/config resolution, including `OPENCLAW_CONFIG_PATH` and any CNX workspace/root variables actually used by source. Never record credentials/tokens/API keys.

## Phase 6 — reconstruct the state discontinuity read-only

Use durable evidence only to compare the current authoritative controller/state against Task-125 final cleanup evidence.

Establish if possible:

- Task-125 cleanup generation/mode/provider/updatedAt;
- current generation/mode/provider/updatedAt;
- whether generation advanced;
- whether `updatedAt` places the transition after Task 125;
- whether logs/events record a `disable`, maintenance transition, lifecycle transition, supervisor action, startup recovery, or state initialization/reset-like event;
- whether current `passthrough` is an intentional durable state, a default synthesized from a missing controller, or output from another root.

Do not infer a specific mutating actor unless durable evidence supports it.

## Required classification

Task 129 must end with one of these evidence-backed classifications, or explicitly `INDETERMINATE` if none can be proven:

### A. AUTHORITATIVE_STATE_DRIFT

The installed launcher targets the expected installed root, the current authoritative controller itself is passthrough/null-provider (or missing in a way that source synthesizes such a state), and the change occurred after Task-125 cleanup.

Report any durable transition evidence and likely authority, but do not repair it.

### B. LAUNCHER_OR_ROOT_MISMATCH

The Task-128/preflight observation or installed launcher targets a different root/CLI than the authoritative installed state, and a coherent managed authoritative root can be demonstrated separately.

Do not change the launcher under Task 129.

### C. SQLITE_PATH_OR_STATUS_PROBE_DEFECT

Managed controller authority is coherent but SQLite failure is caused by a demonstrably wrong/synthetic status/probe path rather than a missing authoritative database.

### D. MIXED_AUTHORITY

Launcher, controller, task/service, ownership, or database authorities disagree across installed surfaces in a way that cannot safely be treated as one coherent state.

### E. INDETERMINATE

Evidence is insufficient. Preserve the blocker; do not normalize.

Multiple classifications may be combined only when clearly supported (for example authoritative state drift plus an independent SQLite probe defect).

## Phase 7 — report and stop

Publish exactly:

`docs/operations/coordination/reports/CNX-20260829-129-managed-state-state-root-authority-readonly-diagnosis.md`

The report must include:

- exact coordination HEAD at execution start;
- evidence root;
- installed launcher path/content/hash and parsed CLI/root targets;
- installed CLI hashes/identity;
- explicit authoritative root;
- controller/runtime/ownership/SQLite path evidence;
- competing-root inventory;
- exact direct read-only launcher commands and results;
- scheduled-task/service authority paths;
- non-secret relevant environment overrides;
- Task-125 vs current state timeline/generation comparison;
- SQLite integrity result or exact reason it is unprovable;
- final classification from the list above;
- exact first unresolved ambiguity if `INDETERMINATE`;
- explicit statement that no lifecycle/recovery mutation or Dashboard semantic Send occurred;
- recommended **next task type only**, not authorization to execute it.

Then STOP for independent ChatGPT review.

## Hard fence

Task 129 authorizes **no mutation of the live runtime**.

Forbidden:

- Task-128 recovery suite or any recovery crash scenario;
- install/install-over;
- reset/uninstall/reinstall;
- start/stop/restart;
- enable/disable;
- provider selection or provider/model/config changes;
- direct edits to controller/runtime/ownership/database/state/log files;
- process kill;
- scheduled-task/service run/start/stop/restart/change;
- cleanup/normalization;
- database initialization/migration/write;
- OpenClaw or Ollama update/change;
- reboot;
- credentials/secrets access or capture;
- Dashboard semantic Send;
- source/runtime repair on the live machine;
- merge/tag/release;
- force push.

If any required read-only probe cannot be performed without mutation, report that item as unproven instead of crossing the fence.
