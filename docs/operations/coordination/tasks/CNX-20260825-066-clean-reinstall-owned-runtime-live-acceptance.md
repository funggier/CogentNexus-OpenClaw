# CNX-20260825-066 — Clean Reinstall Owned Runtime Live Acceptance

Status: `READY_FOR_HERMES`

Execution mode: `LIVE_CLEAN_REINSTALL_WITH_PRESERVATION_AND_MULTI_TICK_ACCEPTANCE`

Current authorization: `CLEAN_REINSTALL_AND_LIVE_RUNTIME_ACCEPTANCE_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes after the operator's continuation signal

## Goal

Repair the current Windows installation by removing the existing CogentNexus-OpenClaw cleanly and installing the exact reviewed Task 065 source fresh, then prove on the live machine that durable runtime ownership no longer depends on Hermes/another agent environment and that the recurring PT1M console/window flash is gone across multiple natural supervisor ticks.

This is the already-authorized live successor to accepted Task 065. No additional operator confirmation is required for the bounded uninstall/reinstall described here.

## Accepted predecessor

Task 065 report result:

`PASS_INSTALLER_RUNTIME_AUTHORITY_GAPS_CLOSED`

Task 065 implementation HEAD:

`21686f70520c5e0263e8aea4d644d2c87324e872`

Task 065 report HEAD:

`8c74686dfe4c6817e2dcc9cbe27e2a8670c24c76`

Task 065 review decision:

`ACCEPT`

Task 065 review disposition:

`ACCEPT_INSTALLER_RUNTIME_AUTHORITY_GAPS_CLOSED`

Task 065 review commit:

`f45f3c2c55828114026d07813ad447a5e4048b8e`

Accepted source properties:

- exact `scripts\runtime_authority.py` installer path;
- unconditional runtime ensure/validation on every install/install-over;
- capability probing of both owned `python.exe` and `pythonw.exe`;
- no Windows startup fallback to registration-time `sys.executable`;
- exact owned foreground launcher binding;
- post-provision MANAGED enable/status/ownership/doctor under `$ownedPython`;
- Task 063 flash classification remains `FLASH_CHILD_PROCESS` for the old live Hermes/uv chain.

## Current live baseline

The operator reports that the visible window still flashes periodically now. This is expected before Task 066 because Tasks 063-065 were source/tests only and did not modify the live installation.

The old live Scheduled Task is expected to remain bound to the historical Hermes-agent/uv interpreter chain until clean uninstall. Treat the continuing flash as **PRE_REINSTALL_BASELINE**, not as evidence against the source fix.

## Repository / install-source discipline

Use a fresh isolated coordination clone of:

`funggier/CogentNexus-OpenClaw`

branch:

`agent/v0.9.3-recovery-reality-tests`

Require before live mutation:

- local coordination HEAD equals remote branch HEAD;
- Task 065 review commit `f45f3c2c55828114026d07813ad447a5e4048b8e` is ancestor;
- `ACTIVE.md`, `STATUS.md`, and this task agree on Task 066 authorization;
- no matching Task 066 report exists.

For installation, use a separate fresh clean source clone/worktree pinned exactly to reviewed implementation commit:

`21686f70520c5e0263e8aea4d644d2c87324e872`

Do not install from the primary OpenClaw workspace, HermesAgent repository, a temp modified source tree, or an unreviewed later source commit.

Record the exact install-source HEAD/tree before install. No source edits are authorized in Task 066.

## Evidence boundary

Before any uninstall mutation create one external retained evidence directory outside all CogentNexus-owned deletion roots, for example:

`%LOCALAPPDATA%\Temp\cnx066-clean-reinstall-<UTC-token>`

Store only bounded operational evidence needed for review. Do not copy secrets or whole unrelated configuration files. Where config comparison is needed, compute normalized hashes/redacted structural summaries rather than publishing credentials/tokens.

## Phase A — fresh preflight and preservation proof

Capture immediately before uninstall:

1. current timestamp and boot identity/LastBootUpTime;
2. current `cnxclaw.cmd status` / controller mode and generation;
3. current CogentNexus supervisor Scheduled Task status, Execute, Arguments, Hidden, LastRunTime, LastTaskResult;
4. OpenClaw Gateway task/status and gateway health;
5. Ollama health and exact model inventory;
6. OpenClaw version;
7. plugin inventory sufficient to identify the canonical CogentNexus plugin plus all unrelated plugin identities/count;
8. CogentNexus plugin config/managed settings, with secrets redacted;
9. ownership manifest verification and exact owned paths/hashes where available;
10. managed AGENTS block state and stripped-baseline SHA using the accepted blank-line-aware stripping method;
11. readonly SQLite integrity and row counts for durable CNX tables;
12. installed skill/launcher/application-data roots and bounded tree/hash evidence;
13. normalized OpenClaw configuration hash **excluding only CogentNexus-owned plugin/config fields**, so unrelated configuration can be compared after uninstall/reinstall;
14. current recurring-flash baseline: Task 063 accepted `FLASH_CHILD_PROCESS` plus current operator observation. A new destructive/active trace is not required; if a read-only process-start observer is used, keep it bounded and do not alter task cadence.

If preflight reveals mixed/ambiguous ownership or unrelated user state inside a deletion boundary that the supported uninstall would remove, STOP and report before uninstall.

## Phase B — supported clean uninstall

Use the currently installed supported CogentNexus launcher/CLI to run the product's `uninstall` operation.

The operator has already authorized this exact clean uninstall. If the supported command has its normal explicit confirmation prompt, Hermes may provide the exact affirmative response required by the product (for example `y`) without requesting another chat confirmation. Do not bypass product confirmation logic or substitute broad manual deletion.

The current old launcher/interpreter may be used only as the one-time removal mechanism. It must not be re-registered as durable authority.

After supported uninstall completes, independently prove:

- `CogentNexus-OpenClaw-Supervisor` Scheduled Task absent;
- `cnxclaw.cmd` absent;
- installed `skills\cogentnexus-openclaw` absent;
- `.cogentnexus-openclaw` live product root absent as defined by supported uninstall semantics;
- `%LOCALAPPDATA%\CogentNexus-OpenClaw` product-owned application-data root/runtime absent as defined by clean uninstall semantics;
- canonical `cogentnexus-openclaw` plugin registration/load path/config entry removed as expected;
- managed AGENTS block removed and stripped file equals the accepted pre-managed baseline;
- OpenClaw Gateway still healthy/native;
- Ollama still healthy and model inventory unchanged;
- unrelated plugin identities unchanged;
- normalized unrelated OpenClaw configuration hash unchanged;
- no HermesAgent/Codex/other project files were removed or modified.

Do not manually hide an uninstall defect. If supported uninstall leaves a product-owned operational residue that its contract says should be removed, classify and STOP rather than deleting it by hand and claiming clean uninstall success.

## Phase C — fresh install from exact reviewed source

Use the separate clean install-source tree at exact commit:

`21686f70520c5e0263e8aea4d644d2c87324e872`

Run the normal supported Windows install path from that tree against the standard OpenClaw workspace. Do not use `-SkipPlugin`, `-SkipGatewayRestart`, `-SkipAgentsPolicy`, or link-plugin shortcuts for this fresh acceptance install.

Bootstrap Python may be transiently used only as designed by the reviewed installer. Record:

- bootstrap `sys.executable`;
- resolved non-venv base interpreter;
- resulting product runtime manifest.

The fresh install must create exactly the product-owned runtime root:

`%LOCALAPPDATA%\CogentNexus-OpenClaw\runtime\python`

and manifest paths:

- foreground `%LOCALAPPDATA%\CogentNexus-OpenClaw\runtime\python\Scripts\python.exe`;
- background `%LOCALAPPDATA%\CogentNexus-OpenClaw\runtime\python\Scripts\pythonw.exe`.

The durable launcher and Scheduled Task must contain **no** path containing `hermes`, `codex`, an executor/test venv, an isolated clone path as interpreter authority, or a temp directory.

A base interpreter outside the product runtime is allowed only under the reviewed Task 063-065 architecture: it must be a verified non-venv base/system Python and must not be an executor venv. Record this limitation explicitly; do not claim the product venv is fully standalone.

## Phase D — exact runtime-binding acceptance

After install, independently verify:

1. `cnxclaw.cmd` invokes exactly the manifest's owned foreground interpreter;
2. `CogentNexus-OpenClaw-Supervisor` Execute equals exactly the manifest's owned background `pythonw.exe`;
3. Scheduled Task Arguments target installed `host_control_v092.py` with the live CogentNexus root;
4. startup target remains v0.9.2 `host_control_v092.py`;
5. no durable artifact references Hermes/Codex/agent/test/temp interpreter paths;
6. runtime manifest validates against the exact product root;
7. foreground interpreter runs a bounded stdlib/product CLI probe successfully;
8. background interpreter runs a bounded sentinel/exit probe without console requirements.

## Phase E — multi-tick no-flash proof

Observe at least **three natural PT1M supervisor ticks** after the fresh install. Do not manually run the task to substitute for natural cadence.

Use a bounded read-only process-start trace/snapshot observer similar to Task 063, scoped only to the CogentNexus supervisor descendant chain. Correlate each tick with Scheduled Task LastRunTime/LastTaskResult.

For each of at least three ticks prove:

- Scheduled Task action starts the product-owned `pythonw.exe`;
- no `conhost.exe` is spawned causally from the supervisor chain;
- no console-subsystem `python.exe` trampoline from Hermes/uv/agent venv occurs;
- no `.cmd`/PowerShell wrapper is introduced into the periodic task action;
- LastTaskResult remains 0 or otherwise healthy according to the actual task contract;
- Gateway/Ollama remain healthy.

Acceptance classification:

- `NO_FLASH_MULTI_TICK_PROVEN` — at least three natural ticks show no console/conhost path and no visible-flash-producing child chain;
- `FLASH_REMAINS_BOUND` — a console/visible child is still causally observed after reinstall;
- `FLASH_NOT_OBSERVABLE` — evidence is insufficient to prove either condition.

Do not claim the flash fixed merely because `pythonw.exe` appears in Task Scheduler. The process-start evidence is mandatory.

## Phase F — post-install MANAGED health

After multi-tick observation verify:

- controller mode `managed`, desired Gateway/provider running, selected provider Ollama, no active transition;
- startup policy enabled;
- one canonical v0.9.3 plugin registration/root, enabled and loaded;
- plugin ownership manifest verifies exactly;
- managed plugin config includes accepted v0.9.3 MANAGED values including `ticketFirst=true` and `hooks.allowConversationAccess=true`;
- managed AGENTS block is present exactly once and underlying baseline remains correct when stripped with accepted boundary semantics;
- OpenClaw Gateway healthy;
- Ollama healthy with preflight model inventory unchanged;
- SQLite readonly integrity `ok` and expected durable tables readable;
- unrelated plugins/config remain preserved;
- no Hermes/Codex/agent path is part of CogentNexus durable runtime authority.

Do not perform a real user-message/LLM inference smoke in this task unless required solely by installer health. End-to-end Ticket -> LLM -> response acceptance remains a separate final gate so install repair is not conflated with semantic execution.

## Mutation fence

Task 066 authorizes only the bounded live changes caused by:

- supported CogentNexus clean uninstall;
- supported fresh CogentNexus install from exact reviewed source;
- normal lifecycle/plugin/Gateway changes that those supported operations intentionally perform.

It does not authorize:

- manual deletion of unrelated files/config;
- edits to OpenClaw/Ollama user data outside CogentNexus ownership;
- HermesAgent project mutation;
- arbitrary process termination;
- reboot/power-cycle;
- provider/model changes;
- merge/tag/release;
- source-code fixes during the live task.

If an unexpected source defect appears, stop and report it; do not patch live files.

## Verification and report

Record exact commands/actions, observations, evidence paths/hashes, and any unproven items. Distinguish supported product mutations from read-only observations.

Before publishing the report verify:

- no repository source files were changed;
- only the Task 066 report is committed by Hermes;
- publication fence from fetched execution HEAD to report HEAD contains only the matching report file;
- live state is either clearly accepted or clearly blocked.

Publish only:

`docs/operations/coordination/reports/CNX-20260825-066-clean-reinstall-owned-runtime-live-acceptance.md`

Allowed result tokens — exactly one:

- `PASS_CLEAN_REINSTALL_OWNED_RUNTIME_NO_FLASH`
- `BLOCKED_PREUNINSTALL_PRESERVATION_CONTRADICTION`
- `BLOCKED_CLEAN_UNINSTALL_CONTRACT`
- `BLOCKED_FRESH_INSTALL_FAILURE`
- `BLOCKED_RUNTIME_BINDING_OR_FLASH_REMAINS`
- `BLOCKED_POSTINSTALL_HEALTH`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

A PASS proves the live install/runtime/flash repair only. Final end-to-end Ticket/inference/recovery/release acceptance remains a successor gate.

Report meaningful progress approximately every 3 minutes and immediately after preflight, uninstall, post-uninstall preservation proof, fresh install, each natural-tick observation milestone, final MANAGED health, and report publication.