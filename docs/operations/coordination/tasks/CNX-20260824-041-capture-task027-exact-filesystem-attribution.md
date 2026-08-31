# CNX-20260824-041 — Capture Task027 Exact Filesystem Attribution

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Execution mode: AUTO_WITH_INTERACTIVE_UAC  
Predecessor: CNX-20260824-040 (reviewed ACCEPT)

## Objective

Task 040 proved that Task 038 and Task 027 share the same deterministic mass-loss signature: every tracked directory-contained path is absent while the same five tracked root files remain. It did not prove an actor, PID, event time, or deletion-versus-nonmaterialization mechanism.

Obtain direct filesystem event evidence using the retained operator-created Procmon configuration. The PMC is bound to Task 027; do not redirect it to Task 038 or broaden its filter.

## Human authorization

The operator explicitly authorized:

> **1 — อนุญาต capture สูงสุด 10 นาทีและ materialize 382 ไฟล์หนึ่งครั้งหลัง capture เริ่มแล้ว เต็มที่เลยครับ**

Authorization is limited to one exact-path capture lasting no more than 600 seconds and one materialization of the exact 382 absent Task 027 paths after capture-active proof.

No CogentNexus/OpenClaw/Ollama runtime action, repeated restore, broad capture, forced termination, cleanup, worktree removal, uninstall, reinstall, or reset is authorized.

## Exact identities

Repository: `funggier/CogentNexus-OpenClaw`  
Coordination branch: `agent/v0.9.3-recovery-reality-tests`

Primary workspace:

`C:\Users\CDQ-P\.openclaw\workspace`

Target worktree:

`C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-027`

Expected detached HEAD:

`748b6e7accb22b6bb4a5503c9ac04265f153f9e5`

Expected common repository:

`C:\Users\CDQ-P\.openclaw\workspace\.git`

Expected tracked/present/absent: `387 / 5 / 382`

Expected absent-list SHA256:

`6A078DA7D54615B67E0020D978A065171E803B0A0DFE134CE978BB2616B91FB8`

Expected present allowlist:

- `.gitignore`
- `AGENTS.md`
- `README.md`
- `requirements-dev.txt`
- `VERSION`

Procmon executable:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx035-procmon\20260823T140738Z\extracted\Procmon64.exe`

Expected executable SHA256:

`78D7148EF5E1472BBCEC02CFD655F5AA789006B65D9990862DD8546ECF6C9AF1`

Expected version/signature: `4.1`, Authenticode Valid, Microsoft Corporation.

PMC:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx035-procmon\20260823T140738Z\task027-exact-filesystem-dropfiltered.pmc`

Expected PMC length: `2051` bytes

Expected PMC SHA256:

`61F3BBB57B65F8DC708E66BC15B5B808AB44E9DC770799E8C32ED40724AE6CBC`

Expected semantics: Path begins with the exact Task 027 worktree path; Include; filesystem events only; Drop Filtered Events enabled.

Matching report:

`docs/operations/coordination/reports/CNX-20260824-041-capture-task027-exact-filesystem-attribution.md`

## Duplicate fence

Freshly fetch the coordination branch from the existing primary workspace. If the matching report exists at fetched HEAD, do not launch Procmon, capture, restore, or publish a duplicate.

Do not create a worktree, clone, branch, repository, temporary checkout, or alternate index.

## Phase 1 — immutable preflight

Before launching Procmon, prove and record:

1. target existence, exact registration/gitdir/common-dir, detached HEAD, and absence of operation-in-progress state;
2. `GIT_OPTIONAL_LOCKS=0` on every target Git query;
3. exactly 387 tracked, 5 present allowlist, and 382 absent tracked paths;
4. canonical absent-list hash exactly matches the expected SHA256;
5. no staged, non-deletion modified, untracked, ignored, sparse, submodule, nested-repository, reparse, conflict, or active-process state;
6. executable regular-file identity, expected SHA256/version, and valid Microsoft signature;
7. PMC regular-file identity, exactly 2051 bytes, expected SHA256, and bounded structural indicators for the exact Task 027 path, `FilterRules`, and `DestructiveFilter`;
8. zero Procmon/Procmon64 processes and zero Procmon driver/service state;
9. no pre-existing Task 041 PML/CSV/backing artifact in the newly selected evidence directory.

Any drift blocks launch and restore.

## Phase 2 — evidence and exact pathspec

Create one new directory:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx041-procmon\<UTC>`

Retain provenance/prestate metadata, the exact NUL-delimited 382-path pathspec, PML, CSV, bounded parsed attribution, and poststate metadata. Do not commit these artifacts.

Derive the pathspec only from the proven absent set. It must contain exactly 382 repository-relative paths and reproduce the expected canonical hash. No wildcard, directory, dot, or broad pathspec is allowed.

## Phase 3 — bounded elevated capture

Launch the exact verified Procmon64 executable through ordinary UAC using `Start-Process -Verb RunAs`. Prohibit UAC bypass, scheduled-task elevation, PsExec, alternate credentials, or another binary.

Use arguments equivalent to:

`/AcceptEula /Quiet /Minimized /LoadConfig <exact-PMC> /BackingFile <new-exact-PML> /Runtime 600`

Capture must never exceed 600 seconds.

If UAC is presented, report it and wait for the operator to approve. Do not emulate consent.

Before restoring, prove capture active using expected Procmon process identity, backing-PML initialization/growth, and capture start time. If capture-active proof is unavailable, do not restore.

## Phase 4 — exactly one materialization

Only after capture-active proof, run exactly once:

`git -C <Task027> restore --source=HEAD --worktree --pathspec-from-file=<exact-NUL-pathspec> --pathspec-file-nul`

Record process identity, command timing, exit code, stdout, and stderr. Never run a second restore.

After the restore returns, do not query, enumerate, hash, open, or stimulate Task 027 while capture remains active. Allow `/Runtime 600` to stop automatically.

Prohibit `/Terminate`, `Stop-Process`, `taskkill`, Task Manager End Task, force-kill, driver/service mutation, reboot, and logoff. If Procmon has not stopped within 60 seconds after the runtime boundary, return a blocker and request human direction without terminating it.

## Phase 5 — offline export and attribution

Only after capture is fully stopped and Procmon driver/service state is clean:

1. export the PML offline to CSV using the exact verified executable with `/OpenLog` and `/SaveAs`;
2. prove capture remains disabled during export;
3. parse without accessing Task 027;
4. prove every event path is rooted under the exact Task 027 path; any escape blocks;
5. separate expected Git restore/materialization events from later events;
6. identify successful post-restore deletion, disposition, replace, rename, or move-away events;
7. record exact time, Process Name, PID, Operation, Path, Result, Detail, and available command-line/process-tree identity.

Read/query/open/close operations, failed access, generic correlation, and process presence alone are insufficient for attribution.

## Phase 6 — poststate

After capture/export are fully stopped, perform one bounded Task 027 poststate count with `GIT_OPTIONAL_LOCKS=0`. Record tracked/present/absent counts and canonical hashes.

Do not restore again, repair, clean, remove, or prune regardless of result.

## Result

Return exactly one:

- `PASS_DELETE_ACTOR_ATTRIBUTED`
- `BLOCKED_PRESTATE_DRIFT`
- `BLOCKED_PROCMON_IDENTITY`
- `BLOCKED_PROCMON_PREEXISTING`
- `BLOCKED_CAPTURE_START_UNPROVEN`
- `BLOCKED_RESTORE_FAILED`
- `BLOCKED_CAPTURE_DID_NOT_STOP`
- `BLOCKED_TRACE_EXPORT_FAILED`
- `BLOCKED_FILTER_ESCAPE`
- `BLOCKED_NO_DELETE_EVENT_OBSERVED`
- `BLOCKED_DELETE_ACTOR_AMBIGUOUS`
- `BLOCKED_REPORT_PUBLICATION_UNSAFE`

A PASS requires direct successful post-restore event evidence identifying the actor. It authorizes no remediation or process action.

## Report and publication

Include fetched HEAD/duplicate result; all identities and hashes; evidence artifact inventory; capture start/stop proof and duration; one-restore proof and result; filter-escape proof; event counts; exact attribution rows or blocker; poststate; Procmon poststate; side-effect accounting; remaining uncertainty; explicit confirmation of no CogentNexus/OpenClaw/Ollama runtime action; and `Human decision required: YES|NO`.

The only repository mutation permitted is the matching Task 041 report. Publish from the existing primary workspace only. Stage exactly that report path; prohibit `git add .`, `git add -A`, and `git commit -a`.

Commit message begins `report: CNX-20260824-041`. Verify the commit changes exactly one path.

## Progress communication

Report meaningful progress approximately every 3 minutes and immediately after duplicate/preflight, Procmon/PMC identity, UAC/capture start, the single restore, automatic stop, export/filter proof, attribution, poststate, and publication/blocker.

Progress reports are not pause points except for UAC or a true blocker.

## Prohibited

No Task 038 access. No broad capture, PMC modification, target-filter change, second restore, target stimulation during active capture, worktree/clone/branch/repository creation, repair/removal/prune, index mutation, process termination, watcher/Supervisor/task/config change, retained-evidence cleanup, CogentNexus/OpenClaw/Ollama runtime/provider/recovery/lifecycle action, force push, merge, tag, release, uninstall, reinstall, or reset.
