# CNX-20260901-201 — Task 200 Original Installer Terminal Adjudication and Discord Closure

Status: `READY_FOR_HERMES`
Date: 2026-09-01 ICT
Parent: `CNX-20260831-200`
Repair parent: `CNX-20260831-198`
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Purpose

Resolve the Task-200 ambiguous installer boundary **without replaying any installation or lifecycle mutation**. If and only if the original Task-200 installer is now proven to have completed successfully and the current runtime is independently healthy in managed mode, continue directly to the still-unused one-human-Discord-Send requalification.

This task exists because Task 200 installed exact repaired candidate bytes but stopped while the original installer process was still running and before managed convergence / Discord Send were proven.

## Immutable product authority

Frozen repaired candidate:

`9f4eaa429b2540540e7d6f6c2af99067960e45fb`

Expected installed plugin fingerprint:

`f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`

Do not substitute current coordination HEAD for product identity.

Published v0.9.3 remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No release/tag/asset mutation is authorized.

## Task-200 retained authority

Task-200 report:

`docs/operations/coordination/reports/CNX-20260831-200-task198-repaired-discord-windows-requalification.md`

Evidence root reported by Task 200:

`C:/Users/CDQ-P/AppData/Local/Temp/cnx200-preflight-20260831T`

Original installer process observed at stop boundary:

- PowerShell PID: `11704`
- child conhost PID: `11588`
- gateway PID was separately identified as `21760` and is not an installer child

Important: **do not trust PID 11704 by number alone now.** Windows may reuse PIDs. Match command line, executable path, creation/start time, and retained Task-200 process metadata before classifying a current process as the original installer.

Task-200 Discord Send budget consumed:

`0 / 1`

The full budget therefore remains available only under the conditional Phase C gate below.

## Hard mutation fence before Phase C

During Phases A and B, perform read-only evidence collection only.

Do **not**:

- rerun `scripts/install.ps1`;
- call `cnxclaw enable` or `disable`;
- restart/start/stop Gateway, Host, supervisor, or provider;
- kill/terminate/suspend any process;
- reset or uninstall;
- fresh reinstall or install-over;
- modify SQLite/state/config;
- change provider/model;
- edit product/source/test/workflow files;
- send any Discord message;
- inject/synthesize a human message;
- mutate tag/Release/assets;
- force push.

If current state is not already independently acceptable, stop and report. Do not repair it inside this task.

## Phase A — adjudicate the original installer invocation

Read the Task-200 evidence root and capture the current time.

### A1. Process identity

Determine whether the **original Task-200 installer invocation** is now:

- `TERMINATED`, or
- `STILL_RUNNING_SAME_PROCESS`, or
- `PID_REUSED_OR_AMBIGUOUS`.

Use retained `b02-process-identity.json`, `b03-process-scan.*`, `b04-installer-tree.*`, command line, executable path, creation/start time, and current process metadata.

If PID `11704` exists now but identity does not match the original invocation, classify it as PID reuse; do not interact with it.

### A2. Final stdout/stderr/exit evidence

Inspect retained:

- `b01-install.stdout`
- `b01-install.stderr`
- any `b01-install.exit` or equivalent artifact that may have appeared after Task 200 stopped observing

Record:

- final file sizes;
- SHA-256 hashes;
- modification timestamps;
- final relevant output window;
- whether stderr contains a terminal PowerShell/OpenClaw/CogentNexus error;
- whether the stdout contains exactly:
  `CogentNexus-OpenClaw v0.9.3 installation completed successfully.`
- whether a direct installer exit code is now available.

Do not infer an exit code if none exists.

### A3. Late-boundary classification

Exact candidate `install.ps1` performs these operations after `owned-runtime-ensure`:

1. launcher write;
2. installed plugin resolution;
3. ownership create;
4. ownership verify;
5. managed policy apply;
6. `cnxclaw enable`;
7. gateway status;
8. supervisor doctor;
9. final CNX status;
10. final completion line.

Use retained stdout/stderr and current state to identify the last proven late boundary as precisely as evidence allows.

Do not claim a specific command hung unless the evidence proves it.

## Phase B — independent current read-only state

Capture without mutation:

1. OpenClaw version — expected `2026.7.1-2 (0790d9f)`;
2. installed CogentNexus version and plugin fingerprint;
3. ownership manifest verify using the derived state root;
4. host/controller mode;
5. startup policy/task state;
6. plugin enabled/loaded/error state;
7. Gateway status/listen health;
8. selected provider/model and Ollama readiness;
9. delivery readiness / pending outbox;
10. recovery state / attempts;
11. SQLite `PRAGMA integrity_check`;
12. durable counts for tickets, ticket_events, direct model calls, direct recovery, assistant delivery, outbox, sessions;
13. known healthy Discord owner session:
    `agent:main:discord:channel:1531199905673252946`.

## Phase B decision gate

### Gate PASS — late completion proven

Continue to Phase C only if **all** are true:

1. original installer is proven terminated;
2. final installer completion line is present, or equivalent terminal-success evidence is independently conclusive without inventing an exit code;
3. installed plugin fingerprint equals
   `f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`;
4. ownership verify passes;
5. host mode is already `managed`;
6. startup policy/task is already enabled/ready as expected;
7. plugin is enabled/loaded with no error;
8. Gateway is healthy;
9. managed provider remains Ollama and is ready;
10. delivery is ready with no pending outbox residue;
11. recovery is inactive with zero new recovery attempts attributable to Task 200/201;
12. SQLite integrity is `ok`.

No command may be used to force any of these conditions true.

### Stop — terminal incomplete

If the original installer is terminated but final success/managed convergence is not proven, stop before Discord Send.

Disposition:

`FAIL_INSTALLER_TERMINAL_INCOMPLETE`

Capture exact stdout/stderr tail, current passthrough/managed state, plugin identity, and all health evidence. Do not call `enable` or rerun installer.

### Stop — same installer still running

If the exact original installer process is still running after this extended interval, stop before Discord Send.

Disposition:

`BLOCKED_INSTALLER_STILL_RUNNING`

Do not kill or restart it. Capture its exact process tree, elapsed age, command line, CPU time if read-only available, stdout/stderr current tail/hash/mtime, and current runtime state.

### Stop — process identity ambiguous

If original termination cannot be safely distinguished from PID reuse or missing evidence:

Disposition:

`BLOCKED_PROCESS_IDENTITY`

Do not mutate runtime and do not Discord Send.

## Phase C — one genuine human Discord Send, conditional on Gate PASS only

Use known healthy Discord room/session:

`agent:main:discord:channel:1531199905673252946`

Hermes must generate a fresh nonce in this shape:

`CNX201-<UTC timestamp>-<short random suffix>`

Tell the user the exact single Discord message to send manually:

`ตอบกลับข้อความนี้เพียงว่า <NONCE>`

Then stop and wait for the user to say:

`ส่งแล้ว`

### Send budget

- human Discord Send: exactly `1 / 1`
- Hermes/bot/API Send: `0`
- retry: `0`
- regenerate: `0`
- second room/message: `0`
- injection: `0`

If the one Send visibly fails, do not send another message.

## Phase D — durable Discord correlation

After user says `ส่งแล้ว`, prove:

`1 human Discord Send -> 1 Ticket -> 1 Direct model call -> response_ready -> 1 native visible Discord assistant result -> delivery_confirmed -> completed`

Capture:

- nonce / prompt identity;
- owner session key;
- Ticket ID;
- request key / prompt SHA-256 if available;
- run ID;
- model call ID;
- provider/model;
- ordered Ticket events;
- `response_ready_at`;
- `delivery_confirmed_at`;
- terminal Ticket status;
- Ticket/outbox/recovery deltas;
- bounded OpenClaw/CNX logs;
- user-visible Discord result or authoritative channel-delivery evidence.

Required negatives:

- no `before_agent_run hook failed` for the tested Send;
- no duplicate Ticket;
- no duplicate model call;
- no Direct Recovery attempt;
- no retry/regenerate;
- no pending outbox residue;
- no stuck delivery residue attributable to the Send;
- no provider substitution.

Do not fail solely because Dashboard-observer diagnostics say `missing-run-correlation` or `missing-append-before-deliver`.

Do not require a `cnx_assistant_delivery` row for native Discord Direct delivery; Ticket-level native delivery confirmation is accepted.

## Phase E — post-send read-only health

Capture:

- Gateway health;
- host managed mode;
- startup/plugin state;
- Ollama readiness;
- delivery/recovery state;
- SQLite integrity;
- exact installed candidate fingerprint;
- final durable counts.

No evidence cleanup is authorized.

## PASS criteria

Task 201 is `PASS` only if:

1. Task-200 original installer is proven to have completed successfully without replay;
2. current runtime is already independently healthy and managed;
3. exact repaired candidate fingerprint is active;
4. exactly one genuine human Discord Send is used;
5. one Ticket and one model call correlate to that Send;
6. requested nonce is returned visibly once;
7. Ticket reaches `response_ready -> delivery_confirmed -> completed`;
8. no `before_agent_run hook failed` occurs for the tested Send;
9. no retry/recovery/duplicate/outbox residue occurs;
10. no forbidden lifecycle/publication/source mutation occurs.

## Final dispositions

Use exactly one:

- `PASS`
- `FAIL_INSTALLER_TERMINAL_INCOMPLETE`
- `BLOCKED_INSTALLER_STILL_RUNNING`
- `BLOCKED_PROCESS_IDENTITY`
- `FAIL_DISCORD_BEFORE_AGENT`
- `FAIL_DISCORD_SEMANTIC_DELIVERY`
- `FAIL_DURABLE_CORRELATION`
- `FAIL_HEALTH`
- `BLOCKED_EVIDENCE`

## Report

Publish:

`docs/operations/coordination/reports/CNX-20260901-201-task200-original-installer-terminal-adjudication-and-discord-closure.md`

Then stop for ChatGPT review.
