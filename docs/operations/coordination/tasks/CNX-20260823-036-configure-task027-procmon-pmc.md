# CNX-20260823-036 — Configure Exact Task027 Procmon PMC Without Capture

Status: READY  
Owner: ChatGPT  
Executor: Codex with human interactive UAC/GUI assistance  
Execution mode: `AUTO_WITH_INTERACTIVE_GATE`  
Predecessor: `CNX-20260823-035` (`BLOCKED_EXACT_FILTER_NOT_PROVABLE`, review `BLOCKED`)

## Human authorization

The human operator explicitly authorized, twice after an interrupted turn:

`1 อนุญาต Task 036 ตั้งค่า Procmon .PMC แบบโต้ตอบเท่านั้น ห้ามเริ่ม capture`

This authorization covers only one interactive configuration-only session using the already downloaded and verified retained Task 035 `Procmon64.exe`. It permits UAC/EULA for that exact executable and creation of one task-specific `.PMC` plus minimal local provenance/poststate evidence.

It does not authorize capture, a PML/backing file, event stimulation, restoration, cleanup of retained evidence, watcher/Supervisor changes, or CogentNexus/OpenClaw/Ollama runtime action.

## Role split

ChatGPT defines the exact configuration, no-capture invariant, evidence boundary, and later validation gate.

Codex revalidates identity, opens only the verified retained binary in documented no-connect/no-filter mode, coordinates the human-visible UAC/GUI steps, records factual proof, closes the tool, and publishes only the matching report.

Do not redesign the filter, start a trace, test the filter by touching the target, or infer actor identity.

## Objective

Create one saved Process Monitor configuration for a later separately authorized exact-path trace while proving that no capture started during this task.

The saved configuration must contain:

- one exact `Path begins with` Include rule for the Task 027 worktree;
- filesystem activity enabled;
- Registry, Network, Process/Thread, and Profiling activity disabled;
- `Drop Filtered Events` enabled;
- no boot logging, backing file, capture, or unrelated path rule.

A later separate task must inspect and validate the saved `.PMC` before any capture may be authorized.

## Microsoft documentation basis

Official Process Monitor page:

`https://learn.microsoft.com/en-us/sysinternals/downloads/procmon`

Microsoft Configuration Manager documentation states that Process Monitor can be launched without capturing events and filters using:

`ProcMon.exe /NoConnect /NoFilter /AcceptEULA`

Source:

`https://learn.microsoft.com/en-us/intune/configmgr/tenant-attach/app-install-error-reference`

Microsoft Windows Server troubleshooting documentation identifies the GUI configuration workflow, stopping automatic capture before configuration, and `File > Export Configuration` for saving a `.PMC`.

Source:

`https://learn.microsoft.com/en-us/troubleshoot/windows-server/system-management-components/identify-cause-of-wmi-shutdown`

Use the retained v4.1 binary's observed UI labels when they differ cosmetically. Do not substitute an undocumented switch or a post-capture filter.

## Exact identities

Repository: `funggier/CogentNexus-OpenClaw`

Branch: `agent/v0.9.3-recovery-reality-tests`

Primary repository:

`C:\Users\CDQ-P\.openclaw\workspace`

Target:

`C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-027`

Required detached HEAD:

`748b6e7accb22b6bb4a5503c9ac04265f153f9e5`

Expected common repository:

`C:\Users\CDQ-P\.openclaw\workspace\.git`

Accepted absent-list SHA256:

`6A078DA7D54615B67E0020D978A065171E803B0A0DFE134CE978BB2616B91FB8`

Retained Task 035 directory:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx035-procmon\20260823T140738Z`

Exact retained executable:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx035-procmon\20260823T140738Z\extracted\Procmon64.exe`

Required executable SHA256:

`78D7148EF5E1472BBCEC02CFD655F5AA789006B65D9990862DD8546ECF6C9AF1`

Required file/product version: `4.1 / 4.1`

Required Authenticode status/signer: `Valid`, Microsoft Corporation

Exact output configuration:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx035-procmon\20260823T140738Z\task027-exact-filesystem-dropfiltered.pmc`

Matching report:

`docs/operations/coordination/reports/CNX-20260823-036-configure-task027-procmon-pmc.md`

## Duplicate and partial-execution fence

Freshly fetch the branch before any local action.

1. If the matching Task 036 report exists at fetched HEAD, do not launch Procmon, accept EULA again, modify/export a configuration, close another instance, or repeat any Task 036 action. Stop awaiting ChatGPT review.
2. If the exact output `.PMC` already exists locally and no matching report exists, do not overwrite, delete, import, or trust it. Return `BLOCKED_CONFIG_ALREADY_EXISTS` with its byte size, SHA256, and timestamps.
3. If any Procmon process/capture is already running or ownership is ambiguous, return `BLOCKED_EXISTING_PROCMON_OWNERSHIP`. Do not terminate or reconfigure it.
4. Do not repeat the Task 035 download/extraction or move the retained package.

## Read-only preflight

Before launch:

1. Revalidate exact target registration, detached HEAD, common directory, 387 indexed / 5 materialized / 382 absent state, status count, and accepted absent-list hash.
2. Confirm no merge/rebase/cherry-pick/revert/bisect/index lock or other active Git operation for the target.
3. Recompute the exact retained executable SHA256, file/product version, and Authenticode status/signer.
4. Require the exact retained path and identity above. Otherwise return `BLOCKED_RETAINED_BINARY_IDENTITY`.
5. Inventory all Procmon processes, related driver/service entries, the exact output `.PMC`, any PML/backing file under the Task 035 directory, and the HKCU `Software\Sysinternals\Process Monitor` task-relevant prestate only.
6. Record that no capture/backing file exists before launch. Do not read unrelated registry or user content.

## Interactive launch gate

Before requesting UAC, report the exact executable path, hash suffix, Microsoft signer, and the fact that this phase must not capture.

Launch only the verified retained executable with the documented arguments:

`/NoConnect /NoFilter /AcceptEula`

Elevation may be requested only for that executable. The human may approve UAC only when Windows identifies the exact retained `Procmon64.exe` and Microsoft Corporation as publisher.

Do not obtain credentials, bypass UAC, use PsExec, create a scheduled task, change policy, enable boot logging, install/copy the tool elsewhere, or elevate any other executable.

If an interactive desktop/UAC cannot be completed, return `BLOCKED_ELEVATION_OR_INTERACTIVE_SESSION`.

## Mandatory no-capture proof

Immediately after the GUI becomes visible and before opening any configuration dialog:

1. Prove visually that Capture Events is inactive/disconnected. The capture toolbar control must not indicate active capture.
2. Require zero event rows and no increasing event counter.
3. Require no PML/backing file creation.
4. Keep Capture Events inactive for the entire task. Do not press `Ctrl+E`, click the capture control, or use any command that starts capture.
5. If events appear, the counter advances, capture is active, or no-capture state cannot be confidently proven, do not continue configuration. Close the task-owned instance normally if safe and return `BLOCKED_NO_CAPTURE_GUARANTEE`. Do not save/filter captured events or claim the task was capture-free.

Record the no-capture observation before and after configuration. A display-only filter is not proof.

## Exact GUI configuration

While capture remains inactive:

1. Open `Filter > Filter`.
2. Confirm/reset to no inherited filters as established by `/NoFilter`.
3. Add exactly one path rule:
   - Column: `Path`
   - Relation: `begins with`
   - Value: `C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-027`
   - Action: `Include`
4. Do not add a broader `contains` rule, wildcard, parent-directory rule, process-name rule, Result rule, or unrelated include/exclude.
5. Enable `Show File System Activity` only.
6. Disable `Show Registry Activity`, `Show Network Activity`, and `Show Process and Thread Activity`.
7. Confirm Profiling Events are disabled.
8. Enable `Filter > Drop Filtered Events`.
9. Keep boot logging disabled and use no backing file.
10. Reopen/inspect the filter dialog and toolbar/menu state. Record the exact visible rule and each enabled/disabled class. Do not stimulate or touch the target to test it.
11. If any required setting cannot be selected or confidently observed while capture is inactive, do not export a final config. Return `BLOCKED_CONFIGURATION_UNVERIFIED`.

## Export-only action

Only after all visible settings match:

1. Use `File > Export Configuration`.
2. Save exactly:
   `C:\Users\CDQ-P\AppData\Local\Temp\cnx035-procmon\20260823T140738Z\task027-exact-filesystem-dropfiltered.pmc`
3. Do not create a PML, CSV, registry export, boot log, or alternate configuration.
4. Confirm the file exists, is nonzero, and record byte size, SHA256, creation/write UTC, and exact path.
5. Optionally retain local screenshots containing only the Procmon configuration/filter/no-capture UI. Do not capture unrelated desktop, event rows, paths, or user data.
6. Do not parse, edit, patch, regenerate, or load the binary `.PMC` in this task. Validation belongs to the next separate task.

## Normal close and poststate

1. Reconfirm capture is inactive and no events/backing file were created.
2. Close only the task-owned Procmon GUI normally.
3. Verify no Procmon process remains.
4. Query task-relevant Procmon driver/service state and HKCU Process Monitor EULA/config poststate.
5. Do not force-kill a process or force-remove a driver/service/registry value. If cleanup/poststate cannot be verified, return `BLOCKED_CLEANUP_UNVERIFIED`.
6. Retain the verified executable, ZIP/provenance, new `.PMC`, and minimal task evidence inside the Task 035 directory until ChatGPT review. Do not delete or move them.

## Report publication fence

The only repository mutation is the matching Task 036 report.

Stage and commit exactly that report path. Prohibit `git add .`, `git add -A`, `git commit -a`, deletion, reset, clean, checkout, restore, and force push. Verify the report commit changes exactly one path.

Commit begins:

`report: CNX-20260823-036`

The report must include:

- fetched start HEAD;
- exact human authorization;
- target and retained executable identity results;
- pre/post Procmon process, driver/service, and task-relevant HKCU state;
- exact launch arguments and UAC/EULA outcome;
- no-capture proof before/during/after configuration;
- exact visible filter and activity-class settings;
- `.PMC` path, byte size, SHA256, and UTC timestamps;
- confirmation that no PML/CSV/backing file/event stimulation/runtime/Git-worktree mutation occurred;
- side-effect accounting and remaining unproven items.

Do not commit the `.PMC`, Procmon binaries/ZIP, screenshots, registry exports, transcripts, or unrelated local evidence.

## Results

Return exactly one:

- `PASS_PMC_SAVED_NO_CAPTURE`
- `BLOCKED_TARGET_IDENTITY_CHANGED`
- `BLOCKED_RETAINED_BINARY_IDENTITY`
- `BLOCKED_EXISTING_PROCMON_OWNERSHIP`
- `BLOCKED_CONFIG_ALREADY_EXISTS`
- `BLOCKED_ELEVATION_OR_INTERACTIVE_SESSION`
- `BLOCKED_NO_CAPTURE_GUARANTEE`
- `BLOCKED_CONFIGURATION_UNVERIFIED`
- `BLOCKED_CLEANUP_UNVERIFIED`
- `BLOCKED_REPORT_PUBLICATION_UNSAFE`

Include `Human decision required: YES|NO`.

## Progress communication

Report meaningful progress approximately every 3 minutes and immediately after:

- duplicate/identity preflight;
- retained binary/signature verification;
- before the UAC/interactive gate;
- after GUI no-capture proof;
- after exact filter/class/drop-state proof;
- after `.PMC` export;
- after normal close/poststate verification;
- any blocker.

Progress updates are not pause points except at the UAC/interactive or defined safety gates.

## Prohibited

No capture, PML, backing file, CSV, event stimulation, target touch, restoration/materialization, replacement worktree, worktree create/remove/re-register/prune, Git reset/clean/checkout/restore/add/refresh, watcher/Supervisor/task/config change, process action except the one verified task-owned Procmon GUI lifecycle, process-tree operation, force-kill, boot logging, persistent auditing/service/task, PsExec, UAC bypass, policy change, reboot, software installation/copy outside the retained Task 035 directory, Task 025 execution, repository-reference migration, CogentNexus/OpenClaw/Ollama runtime/provider/recovery/lifecycle action, force push, merge, tag, or release.
