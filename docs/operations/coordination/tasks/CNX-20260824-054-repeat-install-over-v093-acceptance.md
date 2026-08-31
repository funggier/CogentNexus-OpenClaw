# CNX-20260824-054 — Repeat v0.9.3 Install-Over with Durable Evidence

Status: `READY_FOR_CODEX`

Execution mode: `MANUAL_WITH_HUMAN_GATE`

Owner: ChatGPT

Executor: Codex after the operator's manual signal

## Goal

Perform one new supported install-over of the healthy Task 050-prefix CogentNexus-OpenClaw v0.9.3 installation using the accepted Task 051 source, prove the corrected canonical help is installed, preserve the live system, and publish a durable report before any temporary evidence is removed.

This task supersedes the unaccepted Task 052 attempt. It is a new execution and must not claim or reconstruct Task 052 evidence.

## Human authorization

After Task 053 was created to reconcile the missing Task 052 evidence, the operator authorized a new install-over if the evidence was not found:

> `ถ้าไม่พบอีกก็ให้ install-over ใหม่ ได้เลยครับ ในเมื่อปัญหาตอนนี้ไม่ร้ายแรงอะไรก็จัดการได้เลยครับไม่ต้องระมัดระวังเกินไปนัก`

This authorizes exactly one new default install-over invocation after the essential preflight passes. Scheduled execution remains disabled; Codex starts after the operator's manual signal.

## Accepted predecessors

- Task 051 implementation: `6d90025f832bb36c477176809a0af2e6c1858c19`
- Task 051 disposition: `ACCEPT_CANONICAL_CHECK_HELP_ALIGNED`
- Task 053 report commit: `7b999b783e1e3d0ece8777fa81ee7741e0cbea1a`
- Task 053 disposition: `ACCEPT_RECONCILIATION_CURRENT_TASK050_HEALTHY_TASK052_UNACCEPTED`

Task 053 proved the current live system is healthy, coherent `mode=upgrade`, and still contains the Task 050 pre-fix help files. Task 052 is superseded and must not be rerun.

## Phase 0 — essential preflight

1. Freshly fetch `agent/v0.9.3-recovery-reality-tests` into one new isolated full clone under `%LOCALAPPDATA%\Temp`; no Git worktree.
2. Record fetched start HEAD and require `ACTIVE.md`, `STATUS.md`, and this Task 054 to agree.
3. Require the Task 051 implementation and Task 053 review as ancestors.
4. Stop if the Task 054 report already exists.
5. Prove no concurrent installer, migration, reinstall, reset, uninstall, lifecycle, or report-publisher process.
6. Require current classifier `mode=upgrade`, `legacy=[]`, exact-valid ownership, one canonical v0.9.3 plugin/supervisor, and no duplicate or legacy identity.
7. Confirm the live help files still match Task 050 and the isolated source help files match Task 051.
8. Confirm controller MANAGED/Ollama, Gateway reachable, Ollama healthy, SQLite integrity `ok`, one canonical AGENTS block with the accepted 7,196-byte stripped baseline, 71 unrelated plugins, four models, and the Task 049 backup.

If these essential gates fail, publish a blocker report without invoking the installer.

## Durable evidence rule

Before installer launch, create one unique evidence directory under `%LOCALAPPDATA%\Temp` containing:

- a preflight JSON summary;
- an initial `report-draft.md` containing fetched HEAD, exact paths, prestate summary, and the intended command;
- unique stdout/stderr paths;
- a wrapper poststate path.

Record the evidence directory path in every progress update.

After every major stage, update `report-draft.md`. Do not delete the evidence directory or isolated clone until the final report commit is pushed and a fresh remote fetch verifies the exact report path and commit SHA. If publication fails, leave both locations intact and report their exact paths and hashes.

Do not commit temporary evidence, logs, JSON, backups, or command dumps.

## Phase 1 — single install-over

Invoke exactly once from the isolated clone:

`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "C:\Users\CDQ-P\.openclaw\workspace"`

Use `Start-Process -PassThru` or an equivalent retained `System.Diagnostics.Process` object. The wrapper must:

1. create exactly one installer child;
2. retain and persist its exact PID and start UTC before waiting;
3. redirect stdout/stderr to the durable evidence directory;
4. wait for that exact process without discarding the object;
5. call `WaitForExit()`, refresh the object, and persist the observed `.ExitCode`, end UTC, duration, output sizes, and SHA-256 values atomically;
6. immediately append the observed exit and stage summary to `report-draft.md`.

No custom installer flags. No second installer or retry. If the child exit is nonzero or unobserved, publish the blocker report and stop without manual repair.

## Phase 2 — acceptance proof

After an observed exit `0`, verify:

- classifier remains exact `mode=upgrade`, `legacy=[]`;
- installed ownership verification passes;
- installed `cnxclaw.py` and `cnxclaw_v093.py` are byte-identical to Task 051 source;
- live help advertises `check cogentnexus-openclaw` and no complete-token generic `check cogentnexus`;
- canonical JSON check exits `0` with `READY`;
- generic JSON check exits `3` as unsupported;
- one canonical launcher, skill, state root, plugin v0.9.3, supervisor, and AGENTS marker pair; no legacy/duplicate identity;
- controller returns to MANAGED/Ollama with desired Gateway/provider running;
- Gateway status/probe and Ollama health succeed;
- SQLite integrity, registered policy, Ticket/workflow/task/session semantics, and AGENTS stripped baseline are preserved;
- the install-over skill backup contains the exact Task 050 pre-fix help files;
- the same 71 unrelated plugins, four models, Task 049 backup, primary repository, unrelated workspace/user data, HermesAgent, Ecosystem, staged-capability-loop, and retained evidence are unchanged;
- no installer/lifecycle/plugin-install orphan remains.

Expected installer-owned disable/enable, plugin replacement, backup, launcher/manifest/task recreation, and Gateway return are authorized effects of the one installer invocation.

## Results

Return exactly one:

- `PASS_REPEAT_INSTALL_OVER_V093_ACCEPTANCE`
- `BLOCKED_SOURCE_OR_DUPLICATE_FENCE`
- `BLOCKED_INSTALL_OVER_PREFLIGHT`
- `BLOCKED_INSTALLER_EXIT_UNOBSERVED`
- `BLOCKED_INSTALL_OVER_NONZERO_EXIT`
- `BLOCKED_CANONICAL_HELP_NOT_INSTALLED`
- `BLOCKED_STATE_OR_OWNERSHIP_PRESERVATION`
- `BLOCKED_POSTINSTALL_RUNTIME`
- `BLOCKED_UNRELATED_DRIFT`
- `BLOCKED_REPORT_PUBLICATION_UNSAFE`

PASS requires one observed exit `0`, exact Task 051 help files installed, preserved state/ownership/data, healthy MANAGED/Ollama runtime, and confirmed remote report publication.

## Report and publication fence

Publish exactly one report:

`docs/operations/coordination/reports/CNX-20260824-054-repeat-install-over-v093-acceptance.md`

The report must include fetched HEAD, preflight, evidence-directory path, exact command/invocation count, child PID/timing/observed exit, stdout/stderr sizes/hashes, installer stage summary, source/live hashes, canonical/generic checks, preservation/runtime results, backup proof, command counts, remaining uncertainty, and one exact result token.

The report commit must change exactly the Task 054 report path relative to fetched start HEAD. Commit message must begin:

`report: CNX-20260824-054 repeat install-over acceptance`

After push, freshly fetch the branch and verify the report file, commit SHA, exact one-path diff, and report content SHA before any cleanup. Keep evidence if any verification fails.

## Prohibited outside the installer

No second installer, clean/fresh reinstall, migration, reset, uninstall, manual installed-file/config/database/AGENTS/plugin/task edit, manual repair/restore, force-kill, broad cleanup, OpenClaw/Ollama/model mutation, primary-repository Git mutation, Procmon/Task 027/038 access, HermesAgent/Ecosystem/staged-capability-loop action, merge, tag, GitHub Release, or archive publication.

## Progress communication

Report meaningful progress approximately every 3 minutes and immediately after preflight, evidence initialization, installer launch, child exit capture, help/source verification, preservation/runtime verification, report push, and remote verification.

Progress updates are not pause points unless a stop gate fires.

