# CNX-20260826-075 — Supported Install-Over, Source/Live Parity and No-Flash Acceptance

Status: `READY_FOR_HERMES`

Execution mode: `LIVE_SUPPORTED_INSTALL_OVER_SOURCE_PARITY_OWNED_RUNTIME_NO_FLASH`

Current authorization: `SUPPORTED_INSTALL_OVER_PARITY_ACCEPTANCE_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes after the operator's continuation signal

## Goal

Apply the accepted Task-073 installer/recovery-preflight correction to the currently healthy Task-072 MANAGED installation using exactly one supported install-over, with no uninstall or manual cleanup, then prove that the live installation matches the accepted source and still preserves CogentNexus-owned runtime authority, MANAGED health, canonical plugin ownership, and no-flash behavior across at least three natural PT1M supervisor ticks.

This is the final source/live parity gate before semantic end-to-end acceptance.

## Accepted source

Install-over source MUST be exactly:

`79b51ed06363f6e8862c491ee0a313ddb412c806`

This commit contains the accepted production corrections:

- clean markerless recovery preflight returns `CLEAN_FRESH`;
- unmarked partial residue remains fail-closed;
- valid incomplete transaction recovery remains bounded;
- ownership-present returns `OWNERSHIP_PRESENT`;
- installer stops on recovery-preflight nonzero before classification;
- unknown successful preflight status fails closed;
- accepted transaction, upgrade/legacy isolation, npm 11/npm 12, plugin and runtime-authority work remains preserved.

Task 074 is test-only and closes the full-suite acceptance blocker. Its report/review establishes `356 passed, 2 skipped, 0 failed` without altering production code.

## Current live baseline

Task 072 is independently accepted and currently installed from production source `9df671670908241486afe2badf8a7f221410c6f8`.

Accepted live properties to re-prove before mutation:

- controller mode `managed`;
- desired Gateway/provider `running`, provider Ollama;
- `CogentNexus-OpenClaw-Supervisor` exists, Enabled/Hidden, PT1M;
- launcher and Scheduled Task use exact CogentNexus-owned runtime under `%LOCALAPPDATA%\CogentNexus-OpenClaw\runtime\python`;
- no durable Hermes/Codex/temp binding;
- exactly one canonical v0.9.3 CogentNexus plugin registration;
- ownership verify passes;
- AGENTS managed block exists exactly once and strips to native baseline SHA `c9a664b73200ae5d6b0da0908de3256cdb4dda8ba6fe99f5e6c5115c3983604c`;
- SQLite integrity/readability passes;
- Gateway healthy;
- Ollama healthy with exactly:
  - `qwen3.5:9b`
  - `muse-glimmer:30b`
  - `qwen3.6:27b`
  - `qwen3.8:27b`;
- Task 072 already proved five natural PT1M ticks with `NO_FLASH_MULTI_TICK_PROVEN`.

Task 075 must not assume this state blindly; re-prove it before install-over.

## Authorized disruptive action

Exactly one normal supported install-over from source `79b51ed...` onto the current MANAGED installation.

Installer/lifecycle effects naturally required by that one install-over are authorized.

Do NOT:

- uninstall first;
- clean/reset product state;
- delete plugin generations manually;
- delete workspace/application-data roots;
- fabricate ownership/transaction markers;
- use skip/link/staging shortcuts;
- repeat the install-over after it has completed;
- reboot/power cycle;
- change provider/models;
- upgrade/downgrade OpenClaw;
- edit source during this task;
- perform semantic product LLM smoke.

If the session is interrupted, inspect actual live state before any continuation and never repeat a completed install-over.

## Phase A — coordination and live preflight

Before any mutation:

1. Fetch/read current remote `ACTIVE.md`, `STATUS.md`, Task 075, Task-074 report/review, Task-073 report/review and Task-072 live report.
2. Verify remote coordination branch HEAD equals local execution starting point used for evidence.
3. Create a new evidence directory outside product boundaries under `%LOCALAPPDATA%\Temp`.
4. Use a clean isolated source worktree/clone at exact `79b51ed06363f6e8862c491ee0a313ddb412c806`.
5. Record `git rev-parse HEAD` and empty `git status --porcelain`.
6. Record Node/npm/Python/OpenClaw versions that will be used.
7. Re-prove current live baseline listed above.
8. Record current ownership manifest, controller generation, plugin inventory/root, runtime manifest, launcher content, Scheduled Task action/trigger/LastTaskResult, AGENTS block count/baseline, SQLite integrity/counts, Gateway/Ollama state.
9. Record enough unrelated OpenClaw/plugin config evidence to compare after install-over.
10. Record current installed skill hashes for source/live parity comparison.

### Hard gate A

Proceed only if current state is materially the accepted Task-072 MANAGED installation and no unreviewed actor has changed ownership/runtime/plugin topology.

If ownership is missing/invalid, task/launcher/runtime no longer matches, CNX plugin topology is ambiguous, or unrelated state indicates another actor changed the installation, STOP and report. Do not use install-over to conceal a changed baseline.

## Phase B — one supported install-over

Run the normal Windows installer from exact `79b51ed...` exactly once:

`scripts/install.ps1 -Workspace C:\Users\CDQ-P\.openclaw\workspace`

No flags:

- no `-SkipPlugin`;
- no `-SkipGatewayRestart`;
- no `-SkipAgentsPolicy`;
- no `-LinkPlugin`.

Record complete installer output and exit code.

Expected upgrade-mode semantics:

1. recovery preflight observes coherent ownership and returns `OWNERSHIP_PRESENT` successfully;
2. `classify-install` returns coherent `upgrade`;
3. no fresh transaction is begun;
4. existing MANAGED installation enters the supported PASSTHROUGH/native handoff before replacement mutation;
5. skill/plugin/runtime/ownership are updated through supported surfaces;
6. plugin generation rollover uses exact ownership-safe plan/apply behavior;
7. ownership is recreated/verified for the accepted source;
8. managed AGENTS policy and lifecycle enable restore MANAGED operation;
9. Gateway returns healthy.

Capture explicit evidence for preflight status and classification.

### Hard gate B

If install-over fails:

- do not run uninstall/reset/manual cleanup;
- do not blindly rerun install-over;
- determine the exact phase and resulting live state;
- use only supported recovery semantics already authorized by the product;
- report blocker if state cannot be proven coherent.

## Phase C — source/live parity

After successful install-over, prove the installed production surfaces correspond to accepted source `79b51ed...`.

At minimum compare exact hashes/content for:

- installed `skills\cogentnexus-openclaw\scripts\namespace_ownership.py` vs source;
- installed runtime/startup authority scripts used by launcher/task;
- installed v0.9.3 CLI/host-control surfaces;
- plugin payload identity/version and canonical root;
- ownership manifest version/root identities.

The accepted recovery behavior must be present live:

- the installed `namespace_ownership.py` contains `CLEAN_FRESH` semantics;
- the installed source corresponds byte-for-byte to the accepted correction for relevant files.

Do not call clean-fresh preflight against the live owned installation expecting `CLEAN_FRESH`; on installed ownership the correct live status is `OWNERSHIP_PRESENT`.

## Phase D — ownership-safe plugin generation parity

Prove after install-over:

1. exactly one active canonical `cogentnexus-openclaw@0.9.3` registration exists;
2. active canonical plugin root resolves unambiguously;
3. prior canonical generation, if replaced, is retired only through the supported ownership rollover/backup boundary;
4. no duplicate active generation/load path remains;
5. no unrelated plugin registration/config was removed;
6. plugin MANAGED config values remain accepted:
   - `ticketFirst=true`;
   - `preInferenceAdmission=true`;
   - `autoWorkflowCompletion=true`;
   - `enforcedMode=true`;
   - `autoResume=true`;
   - dispatch/recovery/outbox/completion polls 60000ms;
   - context-maintenance poll 30000ms;
   - accepted hooks including conversation access.

Do not demand a fixed controller generation number; record actual value.

## Phase E — exact owned runtime authority after install-over

Re-prove:

- runtime root exactly `%LOCALAPPDATA%\CogentNexus-OpenClaw\runtime\python`;
- foreground interpreter exactly `...\runtime\python\Scripts\python.exe`;
- background interpreter exactly `...\runtime\python\Scripts\pythonw.exe`;
- runtime manifest exists and verifies current interpreter paths/base provenance;
- launcher invokes exact owned foreground interpreter + installed v0.9.3 CLI/root;
- Scheduled Task Execute is exact owned background `pythonw.exe`;
- task arguments target installed `skills\cogentnexus-openclaw\scripts\host_control_v092.py --root <stateRoot> supervisor tick --execute-safe`;
- task remains Enabled/Hidden/PT1M;
- durable binding scan contains no `hermes`, `hermes-agent`, `codex`, executor worktree, temp/test venv or `%TEMP%` path.

A verified non-venv/system/uv base Python behind the product-owned venv is permitted; durable authority must remain the product-owned foreground/background paths.

## Phase F — natural PT1M no-flash re-acceptance

Observe at least THREE distinct natural Scheduled Task executions after install-over. Four or five are preferable if observation timing is ambiguous.

Do not manually run the task and count that as natural cadence.

Use bounded process-start/process-tree evidence around each natural tick and prove:

1. PT1M natural cadence;
2. root task executable is exact product-owned `pythonw.exe`;
3. expected host-control/supervisor target is used;
4. no CNX-causal `conhost.exe` descendant;
5. no console `python.exe` trampoline from Hermes/uv agent/test venv;
6. no `cmd.exe`/PowerShell wrapper in the scheduled causal chain;
7. `LastTaskResult=0` or equivalently healthy result each observed tick;
8. Gateway stays healthy;
9. Ollama model inventory remains unchanged.

Final flash result must be exactly one of:

- `NO_FLASH_MULTI_TICK_PROVEN`
- `FLASH_REMAINS_BOUND`
- `FLASH_NOT_OBSERVABLE`

PASS requires `NO_FLASH_MULTI_TICK_PROVEN` with at least three natural ticks.

If a causal flash/conhost/console trampoline appears, STOP and report the exact chain; do not suppress it by changing cadence/task wrappers.

## Phase G — final MANAGED non-semantic health

After the natural-tick window prove:

1. controller mode `managed`;
2. desired Gateway/provider `running`, provider Ollama;
3. startup/Supervisor enabled and healthy;
4. Gateway running/Ready/connectivity and local dashboard health;
5. Ollama healthy with the same four models;
6. one canonical v0.9.3 plugin active as intended;
7. plugin config accepted values unchanged;
8. ownership manifest exists and exact production verification passes through the owned foreground runtime;
9. launcher/task still use only owned runtime;
10. AGENTS managed block exists exactly once and strips to native baseline SHA `c9a664b73200ae5d6b0da0908de3256cdb4dda8ba6fe99f5e6c5115c3983604c`;
11. SQLite `integrity_check` passes; durable tables are readable/coherent;
12. unrelated OpenClaw/plugin/config state from Phase A is preserved;
13. installed relevant source hashes match accepted `79b51ed...`.

## Semantic smoke prohibition

Do NOT send a real user message through CogentNexus/OpenClaw for LLM inference in Task 075.

Do not intentionally create the final Ticket/LLM/result delivery flow here. That is Task 076.

If product ticket/session counts are nonzero from unrelated activity, determine provenance and report; do not delete/reset them to make the acceptance look clean.

## Verification/report publication

Publish a report-only commit adding exactly:

`docs/operations/coordination/reports/CNX-20260826-075-install-over-source-live-parity-no-flash.md`

The report must include:

- fetched coordination HEAD;
- exact source HEAD `79b51ed06363f6e8862c491ee0a313ddb412c806`;
- Phase-A live baseline re-proof;
- exact one-time install-over command/result;
- `OWNERSHIP_PRESENT` recovery-preflight and `upgrade` classification evidence;
- source/live hash parity evidence;
- plugin generation rollover/active canonical root evidence;
- runtime manifest/launcher/task exact paths;
- >=3 natural PT1M process-chain observations;
- flash classification;
- final MANAGED/Gateway/Ollama/plugin/config/ownership/AGENTS/SQLite health;
- unrelated-state preservation;
- explicit semantic-smoke prohibition accounting;
- disruptive-action ledger confirming only one install-over;
- report-only publication fence.

## Result tokens

Use exactly one:

- `PASS_INSTALL_OVER_SOURCE_LIVE_PARITY_NO_FLASH`
- `BLOCKED_LIVE_BASELINE_CHANGED`
- `BLOCKED_INSTALL_OVER_OR_UPGRADE_PATH`
- `BLOCKED_SOURCE_LIVE_PARITY`
- `BLOCKED_PLUGIN_GENERATION_OR_OWNERSHIP`
- `BLOCKED_OWNED_RUNTIME_BINDING`
- `BLOCKED_NO_FLASH_MULTI_TICK_ACCEPTANCE`
- `BLOCKED_FINAL_MANAGED_HEALTH`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Pre-authorized successor

If ChatGPT independently accepts `PASS_INSTALL_OVER_SOURCE_LIVE_PARITY_NO_FLASH`, Task 076 may perform the final bounded real semantic acceptance:

`user message -> durable Ticket -> Ollama LLM -> durable result/delivery -> user-visible response`

Task 076 must not repeat install/install-over/cleanup and must prove durable Ticket/events/outbox/session/result evidence plus idempotent delivery semantics.
