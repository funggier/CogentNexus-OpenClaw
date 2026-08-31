# CNX-20260827-083 — Recover Partial Install and Prove Live Parity

Status: `READY_FOR_HERMES`

Execution mode: `LIVE_SUPPORTED_PARTIAL_INSTALL_RECOVERY_AND_PARITY`

Current authorization: `ONE_SUPPORTED_RECOVERY_INSTALL_OVER_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Recover the current Task-081 partial PASSTHROUGH installation using exactly one supported normal install-over from the independently accepted Task-082 source, then prove complete source/live parity, MANAGED/startup/Supervisor/AGENTS restoration, ownership/runtime integrity, five natural no-flash Supervisor ticks, Gateway/Ollama/SQLite health, and readiness of the authenticated Dashboard/WebChat owner surface.

This task is still not the final semantic acceptance task and must send zero semantic/user messages.

## Exact accepted recovery source

Use exactly:

`df412ed10522d79a722e1b48d681e7553cb79ae2`

This contains:

- accepted Task-078 semantic security/idempotency/recovery fixes;
- accepted Task-079 workflow-delivery atomicity fixes;
- accepted Task-080 crash-safe lock publication and exact delivery-run fencing;
- accepted Task-082 Windows/npm-11/npm-12 pack-artifact resolver repair.

Do not mix later unreviewed production source into the live recovery.

## Accepted predecessor reviews

Task 081:

- report HEAD `ade320d2c32dde1143c2e8dc4ffbf8f3580e44a1`;
- accepted as `ACCEPT_BLOCKER_SUPPORTED_INSTALL_OVER_NPM_PACK_PARSER`.

Task 082:

- implementation HEAD `df412ed10522d79a722e1b48d681e7553cb79ae2`;
- report HEAD `34057308f75cb7334c83e253b3077358d05918fd`;
- independent review `ACCEPT_NPM_PACK_INSTALLER_BOUNDARY_REPAIRED`.

## Accepted current partial live state

Task 081's single supported install-over failed after native handoff and skill copy but before plugin rollover/final MANAGED publication. Task 082 preserved this state read-only.

Expected starting facts:

- OpenClaw `2026.7.1-2`;
- Gateway present and healthy, dashboard HTTP `200`;
- Ollama healthy with the same four accepted models;
- ownership manifest verifies;
- `recovery-preflight = OWNERSHIP_PRESENT`;
- install classification `upgrade`;
- controller `passthrough`, generation 13 unless a natural read-only state detail changed without mutation;
- startup policy disabled;
- Supervisor Scheduled Task absent;
- AGENTS managed block absent;
- previous canonical `cogentnexus-openclaw@0.9.3` generation registered but disabled;
- launcher remains present and points at the product-owned runtime;
- SQLite integrity `ok`;
- Ticket count `0` and outbox count `0`;
- no active semantic run.

If the live state has been materially normalized, repaired, or mutated by another actor since Task 082, stop before installation and report `BLOCKED_PARTIAL_STATE_DRIFT` rather than silently adapting.

---

# Absolute semantic and mutation fences

## Allowed product-changing operation

Exactly one supported normal install-over from the exact Task-082 source:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace C:\Users\CDQ-P\.openclaw\workspace -Provider ollama
```

Equivalent invocation is allowed only if it executes the same script and arguments under the supported Windows PowerShell host.

Installer-internal supported lifecycle actions are allowed as part of that one command.

## Forbidden

Do NOT:

- run uninstall;
- run reset;
- perform clean reinstall;
- manually enable/disable controller or plugin before/after the installer;
- manually create/replace/delete Supervisor Scheduled Task;
- manually edit AGENTS;
- manually edit ownership/runtime/launcher/config;
- manually delete plugin generations/residue;
- use `SkipPlugin`, `SkipAgentsPolicy`, `LinkPlugin`, developer bypasses, or ad-hoc repair flags;
- call the installer a second time if the authorized install-over returns nonzero;
- send any Dashboard/WebChat message;
- call `chat.send`, `openclaw agent`, `sessions_send`, channel send, or equivalent user surface;
- generate/consume the final semantic nonce;
- create synthetic Tickets or mutate SQLite;
- call Ollama directly;
- change model/provider/timeouts;
- restart Gateway/Ollama/Supervisor merely to obtain a passing result outside installer-supported actions;
- reboot;
- merge, tag, or release.

If the one install-over fails, capture read-only post-failure evidence and stop.

---

# Phase A — execution fence and partial-state re-proof

Before any product mutation:

1. fetch the coordination branch and record the exact execution HEAD;
2. verify Task-082 report and independent ACCEPT review are ancestors;
3. create/use a clean isolated deployment checkout at exact `df412ed10522d79a722e1b48d681e7553cb79ae2`;
4. verify `git rev-parse HEAD` exactly equals that commit;
5. verify clean `git status --short`;
6. record Windows PowerShell/Node/npm versions;
7. record OpenClaw version;
8. re-prove the expected partial live state read-only.

At minimum record:

- controller mode/generation;
- startup state;
- Supervisor task presence/absence;
- launcher path/content and interpreter binding;
- ownership verification;
- `recovery-preflight` result;
- `classify-install` result;
- canonical plugin path/version/enabled state;
- plugin config values relevant to Ticket-first semantics;
- AGENTS managed marker count;
- authoritative SQLite path, integrity, Ticket/event/outbox counts;
- Gateway task/state, websocket/HTTP dashboard health;
- Ollama version/process/model list;
- no current semantic run.

Required pre-install classification:

`upgrade`

Required pre-install ownership result:

`OWNERSHIP_PRESENT`

No fresh transaction should be started.

If either condition is false, stop before mutation and report `BLOCKED_RECOVERY_INSTALL_MODE`.

---

# Phase B — candidate preflight and npm-pack boundary proof

Before running the live installer, perform source-side checks in the isolated candidate checkout only:

1. verify `scripts/resolve-npm-pack-artifact.ps1` is present and PowerShell syntax-valid;
2. verify `scripts/install.ps1` dot-sources/uses it after `npm pack --json` and before rollover;
3. run candidate `npm ci`;
4. run `npm run plugin:validate`;
5. run the focused Task-082 npm-pack boundary tests;
6. optionally run `npm pack --json` in the isolated candidate plugin directory and resolve that exact artifact through the production helper, then remove the isolated artifact.

This phase must not touch the live workspace/plugin/config.

If source-side candidate preflight fails, stop before the live install and report `BLOCKED_RECOVERY_CANDIDATE_PREFLIGHT`.

---

# Phase C — exactly one supported recovery install-over

Invoke the authorized installer exactly once.

Capture complete stdout/stderr/exit status and record milestones including:

- existing PASSTHROUGH/native boundary behavior;
- recovery preflight;
- classification;
- fresh transaction start or absence;
- skill backup/copy/validation;
- Ticket DB bootstrap;
- npm pack output shape and resolver-selected filename/path;
- plugin installation from the exact resolved npm-pack artifact;
- old/new plugin generation inventory and rollover plan;
- canonical generation selection;
- ownership publication/verification;
- startup policy restoration;
- Supervisor creation/restoration;
- AGENTS managed policy restoration;
- final controller transition to MANAGED;
- final installer exit code.

Expected:

- install exit `0`;
- no fresh transaction;
- no manual repair step;
- no second installer invocation.

If install returns nonzero, do not retry. Capture post-failure state read-only and report `BLOCKED_SUPPORTED_RECOVERY_INSTALL_OVER`.

---

# Phase D — source/live parity

After successful install-over, prove the installed product corresponds exactly to source `df412ed10522d79a722e1b48d681e7553cb79ae2`.

## D1 — installed skill parity

Compare the installed `skills\cogentnexus-openclaw` tree against the exact candidate source using normalized relative paths and SHA-256.

Exclude only known non-source runtime cache artifacts such as `__pycache__` where appropriate.

Require zero unexplained differences.

## D2 — canonical plugin parity

Prove:

- exactly one active canonical `cogentnexus-openclaw@0.9.3` generation wins runtime resolution;
- previous generation is retired/outside active resolution through the supported rollover mechanism;
- installed runtime-relevant package files match a package artifact built from exact candidate source;
- compare normalized file list plus per-file hash or equivalent zero-difference proof;
- include package metadata, `dist`, scripts included by package `files`, and plugin manifest.

Explicitly demonstrate the installed runtime contains the accepted semantic/delivery fixes and Task-082 resolver-backed package result.

No manual copy/patch is allowed to obtain parity.

If any runtime-relevant difference remains, report `BLOCKED_SOURCE_LIVE_PARITY`.

---

# Phase E — ownership/runtime/MANAGED restoration

Require all of the following after install-over:

1. controller `managed`;
2. desired Gateway/provider state `running`;
3. startup policy enabled/installed as expected;
4. Supervisor Scheduled Task exists, Ready/healthy, Hidden as expected, PT1M trigger;
5. Supervisor execute path is the product-owned background interpreter under `%LOCALAPPDATA%\CogentNexus-OpenClaw\runtime\python\...\pythonw.exe`;
6. Supervisor arguments point at installed CogentNexus host-control source, not a temp worktree;
7. launcher uses the product-owned foreground `python.exe`;
8. no Hermes venv, Codex path, temp checkout, console Python, `cmd.exe` or PowerShell wrapper is a durable Supervisor dependency;
9. ownership manifest verification passes through the owned interpreter;
10. AGENTS managed block exists exactly once;
11. stripped AGENTS baseline hash remains the accepted baseline;
12. exactly one canonical CogentNexus plugin is enabled and loaded;
13. Ticket-first/pre-inference/direct-delivery/recovery config remains the accepted values;
14. SQLite integrity `ok`;
15. no unexpected Ticket/outbox/recovery work exists from this install task;
16. Gateway remains healthy and dashboard HTTP remains successful;
17. Ollama remains healthy with the same four-model inventory;
18. no unrelated plugin/config state is altered.

If MANAGED restoration is incomplete despite install exit 0, report `BLOCKED_POST_RECOVERY_HEALTH`.

---

# Phase F — natural no-flash acceptance

Observe at least five **natural** Supervisor PT1M ticks after successful recovery.

Do not force-run the task as a substitute.

For each distinct tick record:

- timestamp;
- task LastRunTime / LastTaskResult;
- relevant process ancestry/descendants when observable;
- absence of CogentNexus-caused `conhost.exe`, console `python.exe`, Hermes/uv-agent trampoline, `cmd.exe`, PowerShell wrapper, or temp-worktree executable chain.

Required classification:

`NO_FLASH_MULTI_TICK_PROVEN`

A missing/failed Supervisor tick or causal console flash blocks the task as `BLOCKED_NO_FLASH_OR_RUNTIME_BINDING`.

---

# Phase G — authenticated Dashboard/WebChat owner-surface readiness without a message

Do not create a semantic turn.

Read exact local OpenClaw `2026.7.1-2` help/source/runtime metadata as needed and prove the supported control-UI/Dashboard/WebChat path that will be used by the final semantic task.

Record:

- dashboard URL/endpoint readiness;
- whether a fresh dashboard session can exist before its first message;
- expected canonical owner session-key namespace (for example `agent:<id>:dashboard:<id>` only when proven by exact runtime/source evidence);
- how `before_agent_run` receives `senderIsOwner`/session metadata on that surface;
- why this surface satisfies the existing least-privilege `durableAdmissionEligible()` policy;
- why `openclaw agent --session-key agent:main:main` remains forbidden as an owner-authentication substitute.

If creating the session itself inherently consumes the first user message, do not create it. Record exact first-send procedure for the final semantic task instead.

No Ticket, provider/model run, or nonce may be produced in this phase.

Required readiness disposition:

`DASHBOARD_OWNER_SURFACE_READY`

If the authenticated owner surface cannot be established read-only, report `BLOCKED_DASHBOARD_OWNER_SURFACE_READINESS` and do not send a test message.

---

# Phase H — final read-only health snapshot

After the five-tick window and owner-surface readiness proof, re-record:

- controller MANAGED;
- Supervisor healthy and owned runtime binding;
- Gateway healthy/dashboard HTTP;
- Ollama healthy/same model list;
- one canonical enabled CogentNexus plugin;
- ownership verification;
- AGENTS one managed block;
- SQLite integrity;
- Ticket/event/outbox counts and pending recovery state;
- no semantic message/provider run generated by Task 083;
- unrelated config preserved.

---

# Publication fence

Task 083 is a live task and should not change product source.

Publish only:

`docs/operations/coordination/reports/CNX-20260827-083-recover-partial-install-and-live-parity.md`

in one report-only commit after execution.

The report must include:

- execution HEAD;
- exact recovery source `df412ed10522d79a722e1b48d681e7553cb79ae2`;
- pre-install partial-state evidence;
- exact one-install invocation and exit status;
- resolver-selected npm artifact evidence;
- plugin rollover/source-live parity evidence;
- MANAGED/runtime/ownership/AGENTS/SQLite/Gateway/Ollama evidence;
- five natural PT1M ticks and no-flash classification;
- Dashboard/WebChat owner-surface readiness evidence;
- semantic/probe mutation accounting;
- publication fence.

## Result tokens

Use exactly one:

- `PASS_RECOVERY_LIVE_PARITY_NO_FLASH_OWNER_SURFACE_READY`
- `BLOCKED_PARTIAL_STATE_DRIFT`
- `BLOCKED_RECOVERY_INSTALL_MODE`
- `BLOCKED_RECOVERY_CANDIDATE_PREFLIGHT`
- `BLOCKED_SUPPORTED_RECOVERY_INSTALL_OVER`
- `BLOCKED_SOURCE_LIVE_PARITY`
- `BLOCKED_POST_RECOVERY_HEALTH`
- `BLOCKED_NO_FLASH_OR_RUNTIME_BINDING`
- `BLOCKED_DASHBOARD_OWNER_SURFACE_READINESS`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Successor logic

Only an independently accepted `PASS_RECOVERY_LIVE_PARITY_NO_FLASH_OWNER_SURFACE_READY` may authorize the final semantic acceptance task.

The final task will send exactly one fresh authenticated Dashboard/WebChat owner message with a unique nonce and must prove:

`authenticated owner message`
`-> Ticket durable accepted event before provider inference starts`
`-> routed direct lane`
`-> OpenClaw uses Ollama`
`-> response_ready`
`-> exact owner/run delivery confirmation`
`-> completed`
`-> one visible nonce response`

No merge/tag/release is implied by Task 083 or its successor unless separately authorized.
