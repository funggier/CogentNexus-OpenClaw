# CNX-20260823-036 — Configure Exact Task027 Procmon PMC Without Capture

Status: `BLOCKED_CLEANUP_UNVERIFIED`

Repository: `funggier/CogentNexus-OpenClaw`
Branch: `agent/v0.9.3-recovery-reality-tests`
Fetched start HEAD: `5307cd61b5c10400841ba68f13e665a4ec5b204d`
Human authorization: `1 อนุญาต Task 036 ตั้งค่า Procmon .PMC แบบโต้ตอบเท่านั้น ห้ามเริ่ม capture`

## Preflight and retained binary

- Matching report absent; exact output PMC absent before launch.
- Target remained registered/detached at `748b6e7accb22b6bb4a5503c9ac04265f153f9e5`, common repository `C:\Users\CDQ-P\.openclaw\workspace\.git`.
- Target state: 387 indexed / 5 materialized / 382 absent; status count 382; absent-list SHA256 `6A078DA7D54615B67E0020D978A065171E803B0A0DFE134CE978BB2616B91FB8`.
- Retained executable: `C:\Users\CDQ-P\AppData\Local\Temp\cnx035-procmon\20260823T140738Z\extracted\Procmon64.exe`.
- SHA256 `78D7148EF5E1472BBCEC02CFD655F5AA789006B65D9990862DD8546ECF6C9AF1`; file/product version 4.1/4.1; Authenticode `Valid`, Microsoft Corporation.
- No Procmon process, PML/CSV/backing file, output PMC, or HKCU Process Monitor key was observed before launch.

## Interactive action and blocker

The verified executable was launched once with exactly:

`/NoConnect /NoFilter /AcceptEula`

Windows opened `Process Monitor - Sysinternals: www.sysinternals.com`. The Computer Use helper reported that accessibility/control was unavailable because Procmon ran at a higher Windows integrity level. Therefore Codex could not visually prove Capture Events inactive, zero rows/counter stability, or configure/export the exact filter without violating the mandatory no-capture gate.

The operator was instructed to close the Procmon GUI normally without pressing Capture Events or saving anything and reported `ปิดแล้ว`.

Post-close checks found:

- no `.PMC`, `.PML`, or `.CSV` under the retained Task035 directory;
- no matching Procmon driver/service entry;
- two task-owned Procmon processes still present after an additional five-second wait:
  - PID 51880, command line is the exact retained binary with `/NoConnect /NoFilter /AcceptEula`;
  - child PID 59348, parent PID 51880, command line/path unavailable from the unelevated query.

No force-kill or global `/Terminate` was attempted because Task 036 prohibits force/process-tree operations and requires cleanup to be verified. The remaining processes make normal-close cleanup unverified.

## Result accounting

Proven: exact binary identity, exact launch arguments, higher-integrity interactive limitation, absence of output PMC/PML/CSV/backing file, and residual task-owned processes.

Not proven: visual no-capture state, zero event counter, exact filter/class/drop settings, EULA/config registry state in the elevated context, successful normal close, or creation/validation of a PMC.

No target event was stimulated; no restoration/materialization, Git/worktree/index/config/ref mutation, watcher/Supervisor/task change, runtime/provider/lifecycle action, boot logging, persistent auditing, alternate installation, capture export, or force-kill occurred. No side effect was repeated.

Blocker type: execution-environment / elevated interactive cleanup verification.

Safest narrow remediation: a reviewed follow-up task must first establish ownership and authorize a documented graceful close of only PIDs 51880/59348 or require the operator to close the remaining task-owned Procmon instance through its elevated UI. It must revalidate zero capture files and process/driver poststate before any future PMC configuration attempt.

Human decision required: YES — choose/authorize the exact graceful cleanup method for the two task-owned Procmon processes. The retained package/evidence remains in place.