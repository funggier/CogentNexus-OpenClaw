# CNX-20260825-062 — Post-Power-Loss MANAGED Diagnosis

Status: `READY_FOR_HERMES`

Execution mode: `MANUAL_WITH_HUMAN_GATE`

Current authorization: `POST_POWER_LOSS_DIAGNOSIS_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes after the operator's manual continuation signal

## Goal

Establish the machine's fresh post-power-loss CogentNexus-OpenClaw state without repairing or restarting anything, reconstruct the exact v0.9.3 MANAGED execution path, and bind the root causes of Task 061's AGENTS/config observations sufficiently for a separately reviewed repair decision.

This is a **diagnosis-only** task. It authorizes evidence-directory creation, bounded read-only inspection, static source analysis in an isolated clone, and publication of the matching report only.

## Human and review authority

The operator explicitly asked ChatGPT to continue and then reported that the machine unexpectedly lost power after Task 061.

Task 061 report result:

`BLOCKED_POST_ENABLE_VERIFICATION`

Task 061 report commit:

`3029ca88d4814f7da2c6e6a088a85692452dc453`

Task 061 accepted review disposition:

`ACCEPT_BLOCKER_MANAGED_REENTRY_ACCEPTANCE_MODEL_MISMATCH`

Task 061 review commit:

`7bdd47b9dc0003fbee1c3a7bbdc8b229740c68a5`

The Task 061 report-time MANAGED state is historical evidence. It is **not** current-state authority after the reported power loss.

## Review findings that Task 062 must preserve

Task 061 used several acceptance expectations from the base `host.py` layer that are not valid invariants for the actual v0.9.3 operator path.

Known source architecture to verify independently from the fresh clone:

1. `cnxclaw_v093.py` is the v0.9.3 Ollama-only facade and delegates accepted lifecycle behavior to the v0.9.2 backend.
2. `cnxclaw.py` is the v0.9.2 operator facade and routes lifecycle/provider transitions through `host_control_v092.py`.
3. operator-level `enable` includes provider/route state plus a Host transition and a Gateway process boundary, so generation is not expected to increase exactly once.
4. `startup_v092.py` intentionally targets `host_control_v092.py`; this is the expected current Scheduled Task action surface.
5. the active transactional compatibility layer in `host_v091.py` stages managed settings with `60000` ms compatibility intervals for ticket recovery/dispatch/outbox, not the `5000` ms base-Host values asserted by Task 061.

These findings invalidate Task 061's exact `generation=8`, direct `host_control.py` startup target, and `5000` ms managed interval expectations. They do **not** resolve F1 or F2.

## Unresolved questions

### F1 — AGENTS round-trip

Task 061 proved the inserted managed block matched the registered policy but stripping it did not reproduce the accepted pre-enable baseline SHA-256:

`C9A664B73200AE5D6B0DA0908DE3256CDB4DDA8BA6FE99F5E6C5115C3983604C`

Determine the exact cause—content, newline, boundary whitespace, normalization, or another writer—without writing `AGENTS.md`.

### F2 — managed plugin config persistence

Task 061 observed only `ticketFirst=true` and `hooks.allowConversationAccess=true`; most managed keys appeared empty even though the active transactional enable implementation stages managed settings and the plugin schema contains those keys.

Determine whether the values were never persisted, were removed/normalized later in the layered transition, were read from the wrong config surface, or changed after Task 061/power loss. Do not set or unset any key.

### Power-loss recovery reality

Determine what actually survived and what automatically recovered after reboot: controller intent, startup adapter behavior, Gateway/provider state, plugin activation, ownership, SQLite/Tickets/sessions/recovery rows, and supervisor activity.

Do not create work to test recovery. Observe only the naturally occurring post-power-loss state.

## Required repository source

Use a fresh isolated full clone of:

`funggier/CogentNexus-OpenClaw`

branch:

`agent/v0.9.3-recovery-reality-tests`

Before live inspection require:

- local HEAD equals remote branch HEAD;
- clone is clean;
- Task 061 report commit `3029ca88d4814f7da2c6e6a088a85692452dc453` is an ancestor;
- Task 061 review commit `7bdd47b9dc0003fbee1c3a7bbdc8b229740c68a5` is an ancestor;
- `ACTIVE.md`, `STATUS.md`, and this task agree on `READY_FOR_HERMES` / `POST_POWER_LOSS_DIAGNOSIS_AUTHORIZED`;
- no matching Task 062 report already exists.

Never checkout/reset/clean/repair/commit from the primary workspace repository.

## Evidence boundary

Before live inspection create one unique retained directory under:

`%LOCALAPPDATA%\Temp\cnx062-post-power-loss-diagnosis-<UTC-token>`

Retain bounded text/JSON evidence for all observations and exact commands/exit codes. Redact secrets. Do not collect full environment dumps, API keys, tokens, full OpenClaw config, model contents, unrelated user files, browser data, or unrelated process command lines.

## Phase D1 — prove the reboot boundary

Read only:

- current UTC and local timestamps;
- `Win32_OperatingSystem.LastBootUpTime`;
- bounded Windows uptime;
- Task 061 report timestamp for historical comparison.

Record whether the current boot is demonstrably later than Task 061 execution/publication. If timing cannot prove this is the post-power-loss boot, state that limitation; do not invent a reboot time.

## Phase D2 — fresh live state before interpretation

First inspect durable files directly/read-only where possible, then use bounded status commands only where they are observational.

Capture:

- controller JSON: mode, generation, desiredGateway, desiredProvider, selectedProvider, providerTransition, update timestamps;
- startup policy JSON;
- Windows Scheduled Task `CogentNexus-OpenClaw-Supervisor`: exists/enabled/hidden/state/action/arguments/LastRunTime/LastTaskResult/NextRunTime;
- bundled `OpenClaw Gateway` Scheduled Task bounded identity/state;
- Gateway health/status;
- Ollama reachability and model-name inventory only;
- exactly one current `openclaw plugins list --json` capture for this task, with canonical plugin identity/root/version/enabled/status and bounded unrelated-plugin identity comparison;
- ownership manifest SHA-256 and pluginPath;
- `namespace_ownership.py verify` and `resolve-plugin --version 0.9.3` read-only results;
- accepted replacement project tree SHA and retained rollover-backup tree SHA;
- absence/presence of the retired OpenClaw npm project root;
- registered policy SHA-256;
- current workspace `AGENTS.md` byte size/SHA and marker counts;
- CNX SQLite URI read-only integrity and bounded counts for tickets/events/outbox/sessions plus relevant direct-recovery/context-maintenance/model-call tables if present.

Do **not** manually start Gateway, Ollama, the supervisor task, provider adapters, or any recovery worker if one is down. An unhealthy post-boot state is evidence.

The already-enabled Scheduled Task may execute autonomously during diagnosis. Task 062 does not authorize or suppress that existing behavior. Record any observed LastRunTime/controller/audit changes with timestamps so autonomous recovery is distinguishable from Hermes actions.

If current state indicates corruption, unsafe duplicate ownership, SQLite integrity failure, or uncontrolled repeated mutation, stop read-only inspection as:

`BLOCKED_POST_POWER_LOSS_STATE_UNSAFE`

Do not repair it.

## Phase D3 — reconstruct the exact installed operator chain

Compare installed files byte-for-byte against the fresh clone and record SHA-256 for at least:

- `scripts/cnxclaw_v093.py`;
- `scripts/cnxclaw.py`;
- `scripts/host_control_v092.py`;
- `scripts/host_v092.py`;
- `scripts/host_provider_v092.py`;
- `scripts/host_stall_v091.py`;
- `scripts/host_v091.py`;
- `scripts/host_control_v091.py`;
- `scripts/host_control.py`;
- `scripts/startup_v092.py`;
- `scripts/startup.py`;
- `templates/supervisor/windows-task.xml`;
- installed `cnxclaw.cmd` launcher.

Read the launcher content boundedly and establish its actual Python entry point; do not assume it targets `cnxclaw_v093.py` unless the installed launcher proves that.

Publish a call graph for the operator `cnxclaw enable` path from launcher through v0.9.3/v0.9.2/v0.9.1/base layers, including where provider-route transitions, Host enable, Gateway restart/process boundary, startup binding, and provider-selection commit occur.

Any installed-vs-clone code drift is diagnostic evidence. Do not replace the installed file.

## Phase D4 — account for controller generation

Statically identify every function on the actual Task 061 `enable` path capable of incrementing controller generation, including provider-transition begin/commit and lifecycle restart overlays.

Using Task 061 stdout/poststate plus current durable controller/audit timestamps where available, determine whether reported generation `12` is:

- expected from the real layered transition;
- explainable but not uniquely attributable;
- or evidence of an additional unexpected lifecycle actor.

Do not require an arbitrary generation number in Task 062. The objective is causal accounting.

## Phase D5 — validate startup-adapter architecture and power-loss behavior

Prove from source whether current v0.9.3 inherits `startup_v092.py` and therefore intentionally binds the Scheduled Task to `host_control_v092.py`.

Compare this expected action with the current post-boot Scheduled Task action exactly.

Use LastRunTime/LastTaskResult and bounded controller/audit timestamps to determine whether the supervisor executed after boot and whether it appears to have reconciled state. Do not manually run the task.

## Phase D6 — diagnose F1 AGENTS byte drift

Read-only procedure:

1. record current `AGENTS.md` bytes/SHA/line-ending characterization and marker counts;
2. extract the current managed block in memory and prove whether its normalized content equals registered policy;
3. apply the repository's current managed-block removal algorithm **in memory only** and hash the resulting bytes/text in each repository-defined canonical representation needed to explain the Task 061 report;
4. enumerate only bounded known `AGENTS.pre-host-change-*` / install-backup candidates under the CogentNexus state backup boundary; record path, timestamp, size, SHA;
5. where a candidate can be tied to the accepted pre-enable baseline, compare exact bytes and identify the smallest difference (newline style, separator blank lines, trailing newline, or actual content);
6. if no retained bytes can be authoritatively bound to SHA `C9A664B7...`, state that the exact original cannot be reconstructed from evidence instead of guessing.

No AGENTS write, normalization, copy-back, restore, or new backup is authorized.

## Phase D7 — diagnose F2 managed config persistence

Read only these exact bounded values individually from the current OpenClaw config surface:

- `ticketFirst`;
- `preInferenceAdmission`;
- `autoWorkflowCompletion`;
- `enforcedMode`;
- `autoResume`;
- `workspaceDir`;
- `ticketDispatchLimit`;
- `ticketMaximumRunning`;
- `ticketMaximumAttempts`;
- `ticketRecoveryPollMs`;
- `ticketDispatchPollMs`;
- `ticketOutboxPollMs`;
- `completionPollMs`;
- `contextMaintenancePollMs`;
- `hooks.allowConversationAccess`.

Also inspect only the bounded `plugins.entries.cogentnexus-openclaw` object if needed; redact unrelated or secret-bearing values and do not publish the full OpenClaw configuration.

Trace the active source path for:

- managed-config staging;
- `openclaw config validate`;
- plugin disable/enable sequencing;
- provider-route begin/commit/rollback;
- Gateway process-boundary restart;
- any config snapshot/restore/normalization invoked by those layers.

Use Task 061 retained report/evidence paths when accessible read-only, especially enable stdout/stderr/poststate and bounded config observations. Determine the narrowest supported causal classification:

- `CONFIG_NEVER_PERSISTED`;
- `CONFIG_PERSISTED_THEN_OVERWRITTEN`;
- `CONFIG_READ_SURFACE_MISMATCH`;
- `CONFIG_CHANGED_POST_TASK_OR_POWER_LOSS`;
- `CONFIG_CAUSE_NOT_YET_BOUND`.

Do not run `openclaw config set/unset`, plugin toggles, lifecycle commands, or Gateway reloads to test hypotheses.

## Phase D8 — power-loss continuity assessment

Correlate boot time, Scheduled Task runs, controller/audit timestamps, Gateway/provider health, plugin state, and SQLite durable-work state.

Report separately:

- what survived durably;
- what recovered automatically;
- what remains unhealthy or ambiguous;
- whether any durable Ticket/session/recovery row requires a later human-authorized action.

If rows exist, do not wake inference or deliver output during Task 062.

## Result classification

Use exactly one result token:

- `DIAGNOSIS_COMPLETE_ROOT_CAUSE_BOUND` — post-power-loss state is bounded and F1/F2 plus Task 061 model mismatches are sufficiently explained for a narrow successor decision;
- `BLOCKED_DIAGNOSIS_EVIDENCE_INSUFFICIENT` — important root cause cannot be bound from retained/current read-only evidence;
- `BLOCKED_POST_POWER_LOSS_STATE_UNSAFE` — current state is unsafe/corrupt/ambiguous enough that diagnosis must stop before broader inspection;
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE` — evidence is sound but matching report cannot be published safely.

A diagnostic `PASS` does not mean the product is accepted for release. It means the evidence is sufficient to design the next bounded step.

## Report contract

Publish only:

`docs/operations/coordination/reports/CNX-20260825-062-post-power-loss-managed-diagnosis.md`

The report must include:

- fetched execution HEAD and publication fence;
- proven boot timestamp and current observation time;
- every read-only command/exit code relevant to conclusions;
- current controller/startup/Gateway/Ollama/plugin/ownership/SQLite state;
- autonomous supervisor observations separated from Hermes actions;
- actual installed operator call graph;
- generation accounting conclusion;
- startup target conclusion;
- exact F1 evidence and causal classification;
- exact F2 evidence and causal classification;
- power-loss continuity conclusion;
- uncertainty and unproven claims;
- explicit live mutation accounting;
- exactly one result token.

Report publication commit must add only the matching Task 062 report relative to fetched execution HEAD. Verify the remote branch after push and stop.

## Hard fence

No `cnxclaw enable/disable/start/stop/restart/reset/uninstall`; no installer; no rollover plan/apply; no plugin install/uninstall/enable/disable; no OpenClaw config set/unset; no AGENTS write/restore/normalization; no startup task create/update/delete/run/end; no Gateway start/stop/restart; no Ollama start/stop/model mutation; no provider-route mutation; no ownership rewrite; no generation cleanup; no SQLite write; no Ticket/session/recovery wake/cancel/delivery; no process termination; no primary Git mutation; no Procmon Task 027/038 action; no HermesAgent project mutation; no Ecosystem work; no merge/tag/release/archive publication.

Report meaningful progress approximately every 3 minutes and immediately after reboot-boundary proof, fresh live-state capture, operator-chain reconstruction, F1/F2 diagnosis, continuity assessment, publication, or blocker.
