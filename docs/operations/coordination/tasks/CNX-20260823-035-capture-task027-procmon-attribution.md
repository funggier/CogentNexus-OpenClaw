# CNX-20260823-035 — Capture Exact Task027 Filesystem Attribution with Official Process Monitor

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Execution mode: `AUTO`  
Predecessor: `CNX-20260823-034` (`ACCEPT`)

## Human authorization

The human operator explicitly authorized:

`1 อนุญาต Task 035 ใช้ Procmon ตามขอบเขตนี้`

This authorization covers only the bounded official Microsoft Sysinternals Process Monitor acquisition and exact-path diagnostic defined below. It does not authorize restoration, containment, watcher/Supervisor changes, or CogentNexus/OpenClaw/Ollama runtime action.

## Role split

ChatGPT owns the causal hypothesis, fix direction, and any decision to broaden or contain. Codex owns only acquisition verification, exact-path tracing, evidence capture, and factual validation under this immutable task.

Do not invent a fix, attribute an actor without direct events, or broaden capture.

## Objective

Acquire the current official portable Microsoft Sysinternals Process Monitor package, prove its provenance, and capture at most 10 minutes of naturally occurring filesystem I/O directed at the exact Task 027 worktree.

The trace must identify initiator PID/image, operation, exact path, result, and UTC time. It must not capture or retain unrelated system/user activity.

## Exact identities

Repository: `funggier/CogentNexus-OpenClaw`

Branch: `agent/v0.9.3-recovery-reality-tests`

Primary repository: `C:\Users\CDQ-P\.openclaw\workspace`

Target: `C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-027`

Required detached HEAD: `748b6e7accb22b6bb4a5503c9ac04265f153f9e5`

Expected common repository: `C:\Users\CDQ-P\.openclaw\workspace\.git`

Accepted absent-list SHA256: `6A078DA7D54615B67E0020D978A065171E803B0A0DFE134CE978BB2616B91FB8`

Matching report: `docs/operations/coordination/reports/CNX-20260823-035-capture-task027-procmon-attribution.md`

## Duplicate-execution fence

Freshly fetch the branch before any diagnostic side effect.

If the matching Task 035 report exists at fetched HEAD, do not download, extract, launch, trace, terminate, export, clean, or repeat any Task 035 action. Stop awaiting ChatGPT review.

## Preflight

Before download:

1. Revalidate exact target registration, detached HEAD, common-dir, 387 indexed / 5 materialized / 382 absent, status count, and accepted absent-list hash.
2. Confirm no merge/rebase/cherry-pick/revert/bisect/index lock or other active Git operation for the target.
3. Inventory `Procmon.exe`, `Procmon64.exe`, `Procmon64a.exe`, running Procmon processes, Procmon driver/service entries, and any existing capture/backing file ownership.
4. If any Procmon process/capture is already running or ownership is ambiguous, return `BLOCKED_EXISTING_PROCMON_OWNERSHIP`. Do not terminate or reconfigure it.
5. Record free space for the task-specific temporary evidence location.

## Authorized acquisition and provenance

Official product page:

`https://learn.microsoft.com/en-us/sysinternals/downloads/procmon`

Exact authorized download endpoint:

`https://download.sysinternals.com/files/ProcessMonitor.zip`

Requirements:

1. Download once into a unique task-specific directory beneath `%TEMP%\cnx035-procmon\<UTC-stamp>`.
2. Record start/end UTC, resolved/final URL, HTTP result, byte size, and SHA256 of the ZIP.
3. Extract only inside that same task-specific directory. Do not copy to Program Files, PATH, the repository, OpenClaw directories, startup locations, or a shared tools directory.
4. On this x64 target, select only `Procmon64.exe`.
5. Record executable byte size, SHA256, file/product version, and complete Authenticode result.
6. Require Authenticode `Status=Valid` and a Microsoft signer identity consistent with the official Sysinternals distribution. If download, archive, architecture, or signature verification fails, do not execute it; return `BLOCKED_DOWNLOAD_OR_SIGNATURE`.
7. Do not use mirrors, package managers, Sysinternals Suite, Store packages, GitHub releases, or an alternate binary.

## Elevation and EULA boundary

The operator authorizes UAC/elevation only for the verified `Procmon64.exe` used by this task.

- `-AcceptEula` is authorized; record the Process Monitor HKCU settings/EULA-key prestate and poststate without reading unrelated registry content.
- Do not obtain or handle credentials.
- Do not bypass UAC, create a scheduled task, use PsExec, create a persistent service, enable boot logging, or weaken system policy.
- If unattended execution cannot obtain required elevation, do not improvise. Return `BLOCKED_ELEVATION_REQUIRED` and `Human decision required: YES`.
- No other executable receives elevation under this task.

## Mandatory no-broad-capture gate

Process Monitor can begin recording immediately. Therefore:

1. Start configuration only in a documented no-capture/no-connect state supported by the verified binary.
2. Inspect the bundled/current command help before relying on any switch.
3. Before capture begins, prove a saved/loaded task-specific configuration with:
   - `Path begins with C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-027` as an Include filter;
   - filesystem activity only;
   - delete/disposition, rename, create/open, write, and directory operations sufficient to identify removal/materialization attempts;
   - filtered-out events dropped rather than retained;
   - no Registry, Network, Profiling, boot logging, or unrelated path capture.
4. Record the exact configuration path, SHA256, filter rows/settings, and proof that capture was not active before the configuration loaded.
5. A display-only/post-capture filter is insufficient. Capturing broad events and filtering afterward is prohibited.
6. If the exact pre-capture filter and drop-filtered-events state cannot be proven—whether because an interactive GUI step is required or the current binary lacks a safe automation path—do not start capture. Return `BLOCKED_EXACT_FILTER_NOT_PROVABLE` and state the exact manual step needed.

## Bounded capture

Only after every gate passes:

1. Use a task-specific backing file under the evidence directory.
2. Capture for at most 10 minutes, spanning naturally occurring scheduled-watcher cycles.
3. Do not restore/materialize the 382 paths, create a replacement worktree, touch files, change timestamps, or otherwise provoke an event.
4. Do not pause, resume, edit, or trigger the Codex watcher or CogentNexus Supervisor.
5. Capture only events under the exact target filter.
6. Stop earlier if a successful delete/disposition/rename sequence directly identifies the actor and sufficient process metadata is preserved.
7. Record trace start/stop UTC, tool PID, process image/version, command line with secrets redacted only, backing-file growth, and event count.

## Stop, export, and cleanup verification

1. Stop only the verified task-owned Process Monitor instance/capture.
2. Do not use a global terminate operation unless preflight and current inventory prove that the task-owned instance is the only Procmon instance and the verified help documents the command.
3. Wait for the backing file to close cleanly. Verify no task-owned Procmon process remains.
4. Query Procmon driver/service state after exit. Do not force-delete an unexpected residual driver/service; return `BLOCKED_CAPTURE_CLEANUP_UNVERIFIED`.
5. Preserve locally until ChatGPT review:
   - filtered native `.PML`;
   - filtered `.CSV` export if the verified binary documents a safe export path;
   - filter/config file;
   - provenance manifest;
   - pre/post process/service inventory;
   - command/exit transcript.
6. Record exact local paths, byte sizes, and SHA256 values. Do not commit binary traces, CSV rows containing unrelated data, Procmon binaries, ZIPs, or registry exports to GitHub.
7. Retain the verified portable tool and evidence only inside the task-specific temporary directory until ChatGPT review so the PML remains readable. Cleanup of retained files requires a later exact authorization.
8. Publish only the minimal target-relevant event table needed for attribution: UTC, PID, process image, operation, exact target-relative path, result, and causal interpretation boundary.

## Attribution rule

Return `PASS_ACTOR_PROVEN` only if direct target-filtered events identify a process image/PID and a successful operation sequence capable of causing the observed absence.

Process presence, source capability, scheduled configuration, failed delete attempts, or timing correlation alone is not actor proof.

If no relevant operation occurs during the bounded natural observation, return `PASS_NO_RELEVANT_IO_OBSERVED`. Do not repeat or extend the trace automatically.

## Report publication fence

The only repository mutation is the matching Task 035 report.

Stage and commit exactly that path. Prohibit `git add .`, `git add -A`, `git commit -a`, deletion, reset, clean, checkout, restore, and force push. Verify the report commit changes exactly one path.

Commit begins `report: CNX-20260823-035`.

## Results

Return exactly one:

- `PASS_ACTOR_PROVEN`
- `PASS_NO_RELEVANT_IO_OBSERVED`
- `BLOCKED_TARGET_IDENTITY_CHANGED`
- `BLOCKED_EXISTING_PROCMON_OWNERSHIP`
- `BLOCKED_DOWNLOAD_OR_SIGNATURE`
- `BLOCKED_ELEVATION_REQUIRED`
- `BLOCKED_EXACT_FILTER_NOT_PROVABLE`
- `BLOCKED_CAPTURE_CLEANUP_UNVERIFIED`
- `BLOCKED_REPORT_PUBLICATION_UNSAFE`

Include `Human decision required: YES|NO`.

## Progress communication

Report meaningful progress approximately every 3 minutes and immediately after:

- duplicate/identity preflight;
- download and provenance verification;
- elevation/EULA boundary;
- exact-filter proof;
- capture start;
- actor event or trace stop;
- export/cleanup verification;
- blocker.

Progress updates are not pause points unless a defined safety or interactive gate blocks execution.

## Prohibited

No broad/system-wide capture; no unrelated user-content inspection; no restoration/materialization/touch; no worktree create/remove/re-register/prune; no Git reset/clean/checkout/restore/add/refresh; no watcher/Supervisor/task/config change; no process action except the verified task-owned Procmon lifecycle; no boot logging, persistent auditing, scheduled task, PsExec, UAC bypass, policy change, reboot, or software installation outside the task-specific temporary directory; no Task 025 execution; no repository-reference migration; no CogentNexus/OpenClaw/Ollama runtime/provider/recovery/lifecycle action; no process-tree operation; no force push, merge, tag, or release.
