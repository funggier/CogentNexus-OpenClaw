# CNX-20260823-037 — Gracefully Clean Up Residual Task036 Procmon Processes

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Execution mode: `AUTO_WITH_UAC_GATE`  
Predecessor: `CNX-20260823-036` (`BLOCKED_CLEANUP_UNVERIFIED`, review `BLOCKED`)

## Human authorization

The human operator explicitly authorized:

`อนุญาต Task 037 ตรวจสอบ ownership และใช้ Procmon64.exe /Terminate ได้ 1 ครั้ง เฉพาะเมื่อยืนยันว่าไม่มี Procmon อื่น ห้าม force-kill และห้าม capture`

This authorizes one cleanup-only phase. It permits read-only ownership/poststate checks and at most one invocation of the verified retained `Procmon64.exe /Terminate`, only when exclusive Task 036 Procmon ownership is proven.

It does not authorize any force/process-tree termination, repeated terminate command, capture, filter/PMC configuration, target touch, restoration, retained-evidence deletion, or CogentNexus/OpenClaw/Ollama runtime action.

## Role split

ChatGPT defines the exclusive-ownership gate, the one-shot graceful cleanup action, and acceptance evidence.

Codex performs only exact local validation, the conditional one-shot graceful command, and poststate proof. Do not design a broader cleanup or retry Task 036.

## Objective

Resolve the Task 036 residual Procmon process state without capture or force.

Task 036 directly reported:

- parent PID `51880`, exact retained binary command line with `/NoConnect /NoFilter /AcceptEula`;
- child PID `59348`, parent PID `51880`, image/command line unavailable to the unelevated query;
- no `.PMC`, `.PML`, `.CSV`, backing file, or matching Procmon driver/service entry.

First revalidate current state. If it is already clean, skip `/Terminate` and report clean. If and only if all surviving Procmon processes are exclusively attributable to Task 036 and no other Procmon exists, invoke the exact verified retained executable with `/Terminate` once and verify clean poststate.

## Exact identities

Repository: `funggier/CogentNexus-OpenClaw`

Branch: `agent/v0.9.3-recovery-reality-tests`

Retained Task 035 directory:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx035-procmon\20260823T140738Z`

Exact retained executable:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx035-procmon\20260823T140738Z\extracted\Procmon64.exe`

Required SHA256:

`78D7148EF5E1472BBCEC02CFD655F5AA789006B65D9990862DD8546ECF6C9AF1`

Required file/product version: `4.1 / 4.1`

Required Authenticode: `Valid`, Microsoft Corporation

Task 036 residual identity:

- PID `51880` — exact retained binary, Task 036 launch command line;
- PID `59348` — child of PID `51880` during Task 036.

Matching report:

`docs/operations/coordination/reports/CNX-20260823-037-graceful-cleanup-task036-procmon.md`

## Duplicate-execution fence

Freshly fetch the branch before any local action.

1. If the matching Task 037 report exists at fetched HEAD, do not inventory for action, launch `/Terminate`, or repeat any Task 037 side effect. Stop awaiting ChatGPT review.
2. The `/Terminate` allowance is one-shot across the entire task. Never issue it more than once, including after timeout, uncertain exit code, UAC interruption, or partial result.
3. Do not repeat Task 035 acquisition or Task 036 GUI/configuration launch.
4. Do not delete, overwrite, move, or clean the retained Task 035 directory.

## Read-only preflight

Before any termination command:

1. Inventory all processes whose name, executable path, command line, description, or product identity indicates `Procmon`, `Procmon64`, `Procmon64a`, or Process Monitor.
2. Record PID, parent PID, process name, executable path when readable, command line when readable, creation/start time, session ID, owner/integrity information available without broad inspection, and parent/child relation.
3. Recompute the retained executable SHA256, file/product version, and Authenticode status/signer.
4. Inventory task-relevant Procmon driver/service state.
5. Inventory only the retained Task 035 directory for `.PMC`, `.PML`, `.CSV`, backing/log files, and Task 036/037 evidence. Record names, sizes, timestamps, and hashes for unexpected capture/config artifacts without opening their contents.
6. Do not read unrelated process/user content or unrelated registry state.

## Exclusive-ownership gate

Classify current state exactly:

### Already clean

If zero Procmon processes exist:

- do not invoke `/Terminate`;
- verify no unexpected Procmon driver/service or capture artifact;
- return `PASS_ALREADY_CLEAN_NO_TERMINATE` only when clean poststate is proven.

### Eligible for one graceful terminate

The one-shot `/Terminate` is eligible only when all of the following are true:

1. every current Procmon process is exactly PID 51880 and/or PID 59348 from Task 036, with no additional Procmon process;
2. surviving PID 51880 still resolves to the exact retained executable and Task 036 launch command line, or equivalent immutable identity evidence;
3. surviving PID 59348 is still directly attributable to PID 51880 by unchanged parent/child/process-start evidence, or its exact retained Process Monitor identity can be independently proven;
4. PID reuse, changed ancestry, changed executable, changed start identity, unrelated user ownership, or a separately opened Procmon instance is ruled out;
5. no `.PML`, `.CSV`, backing file, unexpected `.PMC`, active capture evidence, or unrelated Procmon ownership exists;
6. the exact retained binary still matches required hash/version/signature.

PID number or process name alone is insufficient.

If any requirement is uncertain, return `BLOCKED_OWNERSHIP_CHANGED_OR_AMBIGUOUS`. Do not invoke `/Terminate`.

## Authorized one-shot graceful action

Only after the exclusive-ownership gate passes:

1. Announce the exact verified executable and that `/Terminate` will be invoked once.
2. Invoke exactly:
   `C:\Users\CDQ-P\AppData\Local\Temp\cnx035-procmon\20260823T140738Z\extracted\Procmon64.exe /Terminate`
3. Use the verified Process Monitor graceful shutdown mechanism only. No additional arguments.
4. If UAC is required, the human may approve only the exact verified `Procmon64.exe` published by Microsoft Corporation.
5. Record command start/end UTC, launcher/child PID if observable, UAC outcome, and exit code or bounded outcome.
6. Never invoke `/Terminate` a second time.
7. Do not use `Stop-Process`, `taskkill`, Task Manager End Task, WMIC/CIM terminate methods, service/driver stop/delete, process-tree kill, force-kill, reboot, logoff, scheduled task, PsExec, UAC bypass, or policy change.

If elevation/interaction cannot complete, return `BLOCKED_ELEVATION_OR_INTERACTIVE_SESSION` without another attempt.

## Bounded poststate verification

After the single graceful invocation:

1. Observe process state read-only for at most 15 seconds.
2. Verify zero Procmon processes remain.
3. Verify no unexpected Procmon driver/service entry remains.
4. Verify no `.PMC`, `.PML`, `.CSV`, backing file, or capture artifact was created by Task 037.
5. Verify the retained binary/package/evidence still exists unchanged.
6. Do not delete EULA/config registry state or retained files.

If any Procmon process remains, return `BLOCKED_GRACEFUL_TERMINATION_FAILED`. Do not retry or escalate to force.

If process state is clean but driver/service/artifact poststate is uncertain, return `BLOCKED_CLEANUP_POSTSTATE`.

## Report publication fence

The only repository mutation is the matching Task 037 report.

Stage and commit exactly that path. Prohibit `git add .`, `git add -A`, `git commit -a`, deletion, reset, clean, checkout, restore, and force push. Verify the report commit changes exactly one path.

Commit begins:

`report: CNX-20260823-037`

The report must include:

- fetched start HEAD and exact human authorization;
- full narrow Procmon preflight inventory;
- retained executable hash/version/signature result;
- exclusive-ownership decision and evidence;
- whether `/Terminate` was skipped or invoked;
- if invoked, proof it occurred at most once and its bounded outcome;
- poststate process/driver/service/artifact inventory;
- confirmation that no capture/configuration/force/runtime/worktree action occurred;
- side-effect accounting and remaining uncertainty.

Do not commit binaries, ZIP, `.PMC`, `.PML`, `.CSV`, registry exports, screenshots, or unrelated local evidence.

## Results

Return exactly one:

- `PASS_ALREADY_CLEAN_NO_TERMINATE`
- `PASS_GRACEFUL_TERMINATE_CLEAN`
- `BLOCKED_RETAINED_BINARY_IDENTITY`
- `BLOCKED_OWNERSHIP_CHANGED_OR_AMBIGUOUS`
- `BLOCKED_CAPTURE_OR_CONFIG_ARTIFACT_PRESENT`
- `BLOCKED_ELEVATION_OR_INTERACTIVE_SESSION`
- `BLOCKED_GRACEFUL_TERMINATION_FAILED`
- `BLOCKED_CLEANUP_POSTSTATE`
- `BLOCKED_REPORT_PUBLICATION_UNSAFE`

Include `Human decision required: YES|NO`.

## Progress communication

Report meaningful progress approximately every 3 minutes and immediately after:

- duplicate and process inventory preflight;
- retained binary identity verification;
- exclusive-ownership decision;
- immediately before the one-shot graceful action;
- graceful outcome and bounded poststate;
- any blocker.

Progress updates are not pause points except at UAC/interactive or defined safety gates.

## Prohibited

No capture, Procmon GUI configuration launch, `.PMC` creation/overwrite, PML/backing file/CSV, target stimulation/touch, restoration/materialization, worktree create/remove/re-register/prune, Git reset/clean/checkout/restore/add/refresh, watcher/Supervisor/task/config change, `Stop-Process`, `taskkill`, Task Manager End Task, WMIC/CIM termination, service/driver stop/delete, process-tree/force kill, repeated `/Terminate`, reboot/logoff, scheduled task, PsExec, UAC bypass, policy change, retained-evidence cleanup, Task 025 execution, repository-reference migration, CogentNexus/OpenClaw/Ollama runtime/provider/recovery/lifecycle action, force push, merge, tag, or release.
