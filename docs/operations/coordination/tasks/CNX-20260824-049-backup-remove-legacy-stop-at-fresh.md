# CNX-20260824-049 — Back Up and Remove Proven Legacy, Stop at Fresh Before Install

Status: `READY_FOR_CODEX`  
Execution mode: `MANUAL_WITH_HUMAN_GATE`  
Owner: ChatGPT  
Executor: Codex after operator's manual signal  
Start HEAD: `3fde58cfa466498f42905aad6337a992cdadfd54`

## Objective

Create a verified external recovery backup, remove only the proven legacy CogentNexus installation, and reach the current repository classifier result `fresh`.

**Stop before installing CogentNexus-OpenClaw v0.9.3.**

This task must publish its report and return control to ChatGPT/operator before any invocation of `scripts/install.ps1`, `clean-reinstall.ps1`, an installer package, or any equivalent current-product installation path.

## Human authorization

The operator approved the bounded design with response `1` after stating:

- if Task 048 still did not complete the work, the next round may act fully;
- no current installation may occur;
- a report is mandatory before installation.

Authorized in Task 049:

- external backup and hash verification;
- evidence-driven native plugin inventory recovery if the previously intermittent gate fails again;
- legacy PASSTHROUGH/native handoff;
- exact native uninstall of the proven legacy plugin;
- exact removal of proven legacy launcher, skill, state, supervisor task, config entry/load path, and owned plugin residue;
- one graceful Gateway restart only if required to unload the removed plugin or complete native uninstall state;
- exact fresh-classification and preservation verification.

Not authorized: current CogentNexus-OpenClaw installation.

## Authoritative coordination paths

Use only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

Both must identify `CNX-20260824-049` and `READY_FOR_CODEX`.

`docs/operations/STATUS.md` is project narrative and is not an execution gate.

## Predecessors

- Task 046 safely stopped on a transient native inventory timeout before any mutation.
- Task 048 proved the exact native registry/list surfaces currently return valid JSON and identified the legacy plugin ownership.
- Task 048 review: `ACCEPT_BOUNDED_NONREPRODUCTION`.

Do not repeat Task 048's full diagnostic suite. Use its proven command once as the Task 049 pre-mutation gate.

## Duplicate, source, and collision fence

Before live action:

1. fetch the branch and record exact fetched HEAD;
2. require the two exact authoritative coordination paths above;
3. stop if the exact Task 049 report path already exists;
4. use a new isolated full clone; never change the primary repository branch;
5. prove `4c825f8ec1ed6b43a419ad52e0bb85cee28007c1` remains an ancestor;
6. require no non-coordination implementation drift after that reviewed commit;
7. require zero concurrent CogentNexus lifecycle commands and zero Procmon processes;
8. require no current/new namespace artifacts;
9. re-run the current repository classifier and require exact `mode=legacy`, `legacyMode=managed`;
10. require legacy controller mode `managed`, desired provider `running`, generation `32`, unless a newer generation is fully explained by normal read-only health activity;
11. capture Gateway/Ollama/models/scheduler/config/AGENTS/unrelated sentinels.

Return `BLOCKED_DUPLICATE_SOURCE_OR_COLLISION` if any fence is ambiguous.

## Proven legacy identity

Do not act on names alone. Re-prove these identities and Task 045/048 hashes before backup or removal:

- workspace launcher `cnx.cmd`;
- workspace skill `skills\cogentnexus`;
- workspace state `.cogent`;
- scheduled task `CogentNexus Supervisor`;
- native plugin id `cogentnexus-rotation`;
- package `openclaw-plugin-cogentnexus-rotation` version `0.9.1`;
- native managed plugin root from Task 048 inventory;
- exact `plugins.entries.cogentnexus-rotation` config ownership;
- any exact load path or install record returned by native inventory.

Known proof anchors:

- `cnx.cmd`: `0B2EB63FD725236BC6B8F9616307F2B454C4FEBE0BF46CE4DE68F32A9C61B637`
- legacy `SKILL.md`: `5F5136F0F280D4B00C8EF8CF75198BB8844C642CDF249E8A8C8ED63F90AF8C41`
- legacy controller: `F173EFE6EEE6D4E826B5CAF127614BD9AFE292AAE8CC8261EA3A3E0EE2129E5F`
- legacy plugin manifest: `367FC6790A56FAFF0FDF301EBE0E8ACBD64553A3832C0C17ED135025A46516A1`
- legacy package manifest: `513E95654275B0A381025501D7056D61143E132EF85AD59368E358550DC73775`
- OpenClaw config before Task 049: `F2A541DBDFDB8CDD08C1F4693734BF65763F0136804EEB19CA98C06A2BC1656A`
- workspace `AGENTS.md`: `C9BFD0288A379D62BD4C43B5B782AAFE0CFCAE43651B48EB5794780609B7DBBE`

If ownership or hashes drift without a safe explanation, return `BLOCKED_LEGACY_IDENTITY_DRIFT`.

## Phase 1 — one native inventory gate

Run exactly once with a 45-second bound and child-only lifecycle tracing:

`openclaw plugins list --json`

Require valid JSON and prove:

- registry source and state;
- exact legacy plugin id/package/version/root/install record;
- current total plugin inventory;
- unrelated plugin identity set for later comparison;
- zero diagnostic orphan.

If it succeeds, do not run registry repair and continue to backup.

### Conditional repair ladder

Use only if the one inventory gate times out or returns invalid JSON.

Before any repair, complete the backup phase below, including OpenClaw config and a consistent SQLite online backup.

Then:

1. run `openclaw plugins registry --refresh` once;
2. record exact stdout/stderr, config/database hashes/metadata, registry counts, and changed state;
3. retry `openclaw plugins list --json` once with the same 45-second bound;
4. only if still failing, run `openclaw doctor --fix` once;
5. record every reported fix and before/after state;
6. retry `openclaw plugins list --json` one final time.

If valid inventory still cannot be obtained, stop before legacy handoff/removal and return `BLOCKED_NATIVE_INVENTORY_REPAIR_FAILED`.

No OpenClaw upgrade/downgrade/reinstall, manual SQLite edit, manual install-record fabrication, plugin guessing, or repeated repair is allowed.

## Phase 2 — external verified backup

Create exactly one unique backup root beneath:

`%LOCALAPPDATA%\CogentNexus-OpenClaw-Legacy-Removal-Backups\<UTC-ID>`

Canonicalize it and prove it is outside the OpenClaw workspace, OpenClaw state/config roots, legacy state, managed plugin root, current product root, and primary repository.

Back up with explicit paths only:

- `cnx.cmd`;
- complete `skills\cogentnexus`;
- complete `.cogent`;
- exact native legacy plugin managed root;
- OpenClaw config file;
- consistent SQLite database using Python `sqlite3.Connection.backup` or another proven SQLite online-backup API; never raw-copy a live database as the only database backup;
- WAL/SHM metadata if present;
- exact scheduled-task XML/export;
- redacted native plugin inventory and classifier/controller status;
- relevant path/ownership/config/install-record metadata;
- hashes of AGENTS and unrelated sentinels without copying secrets unnecessarily.

The backup may contain secrets inherited from the live config/state. Restrict it to the current user, do not print secret values, and never commit backup contents.

Generate a manifest containing canonical source/destination paths, file counts, byte counts, SHA-256 for regular files, directory inventories, SQLite integrity check result for the backup, scheduled-task identity, and UTC timestamps.

Independently verify source/destination counts, bytes, hashes, SQLite integrity, and manifest self-consistency. If any required item cannot be backed up and verified, perform no live mutation and return `BLOCKED_BACKUP_NOT_VERIFIED`.

## Phase 3 — legacy handoff to native operation

After verified backup only:

1. record legacy controller/supervisor/Gateway/Ollama prestate;
2. invoke exact workspace `cnx.cmd disable` once;
3. require the legacy state to enter PASSTHROUGH/native operation;
4. verify Gateway remains reachable and healthy;
5. verify Ollama and the same four models remain unchanged;
6. prove no active CogentNexus ticket/workflow/external side effect is being abandoned or repeated;
7. prove controller/supervisor will not recreate removed legacy assets.

If handoff is not exact and stable, stop without plugin/path removal and return `BLOCKED_NATIVE_HANDOFF_FAILED`. Do not auto-restore.

## Phase 4 — native legacy plugin removal

Using the exact identity from the successful native inventory:

1. run the native uninstall preview/dry run if supported without mutation and verify only the legacy package/entry/load path/install record is targeted;
2. invoke `openclaw plugins uninstall cogentnexus-rotation --force` exactly once;
3. capture the native removal receipt;
4. re-run native inventory once and require the legacy id/package/install record/root to be absent;
5. compare every unrelated plugin identity against prestate and require no unrelated removal or disablement;
6. inspect OpenClaw config and registry/index to require no exact legacy entry/load path/install record remains.

If the native tool cannot prove a single owner/complete removal, or removes/changes unrelated plugins, stop and return `BLOCKED_NATIVE_PLUGIN_REMOVAL_UNSAFE`.

Do not manually delete the managed plugin root before the native uninstall finishes.

## Phase 5 — exact legacy host cleanup

After native plugin removal:

1. gracefully stop/end only the exact proven legacy controller/supervisor process if still running;
2. unregister only scheduled task `CogentNexus Supervisor`;
3. remove only the exact proven workspace `cnx.cmd`;
4. remove only complete `skills\cogentnexus`;
5. remove only complete `.cogent`;
6. remove exact residual legacy plugin root only if the native uninstall receipt owns it and it still exists;
7. remove only exact legacy config/load-path residue proven by the native receipt/inventory;
8. leave the external backup intact.

No wildcard, prefix match, parent-directory deletion, broad plugin cleanup, workspace cleanup, or unrelated config normalization.

If a file is locked, identify its exact owning PID/command. Gracefully stop only a proven legacy process. Never force-kill Gateway, Ollama, shell, browser, Codex, OpenClaw unrelated Node process, or unknown process. Return `BLOCKED_LEGACY_HOST_CLEANUP` if exact cleanup cannot finish safely.

## Phase 6 — unload and fresh classification

A single graceful `openclaw gateway restart` is allowed only if:

- native uninstall reports restart required; or
- post-uninstall inspection proves the removed plugin remains loaded in the current Gateway process.

Record pre/post PID, command, service registration, URL/profile, reachability, and unrelated plugin inventory. Do not change Gateway configuration.

Then require the current repository classifier to return exact `mode=fresh` with:

- no legacy launcher/skill/state/controller/scheduler/plugin/config/load-path/install-record/root;
- no current `cnxclaw.cmd`;
- no current `skills\cogentnexus-openclaw`;
- no current `.cogentnexus-openclaw`;
- no current product plugin/scheduler/controller;
- external verified backup present and intact.

Do not confuse OpenClaw registry state `fresh` with the CogentNexus installation classifier `mode=fresh`; both must be reported separately.

## Mandatory stop-before-install gate

After `mode=fresh` is proven:

- do not invoke `scripts/install.ps1`;
- do not invoke `clean-reinstall.ps1`;
- do not download/run a Release installer;
- do not create `cnxclaw.cmd`, the new skill, state root, plugin, controller, or scheduler;
- do not continue into any current-product installation phase.

Return control through the Task 049 report. Installation requires a successor task and new explicit operator approval after report review.

## Final preservation proof

Require:

- Gateway healthy and reachable in native OpenClaw mode;
- Ollama healthy; active model and four-model inventory unchanged;
- OpenClaw version/global package unchanged;
- all unrelated plugin identities unchanged;
- OpenClaw user data and unrelated workspace data preserved;
- AGENTS hash unchanged;
- primary repository branch/status unchanged;
- HermesAgent, Ecosystem, staged-capability-loop, retained Procmon/Task 027/038 evidence untouched;
- backup manifest and contents unchanged since verification;
- zero diagnostic/lifecycle orphan processes;
- no current CogentNexus-OpenClaw installation artifacts.

## Report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260824-049-backup-remove-legacy-stop-at-fresh.md`

Include:

- fetched HEAD and exact authority;
- preflight hashes/classifier/runtime/plugin inventory;
- whether the conditional repair ladder was skipped or used, with every command/change;
- backup root, ACL summary, manifest totals, hashes, and SQLite integrity result without secrets;
- handoff command/result;
- native uninstall preview/receipt/result;
- exact scheduler/process/path/config/index removals;
- any one Gateway restart and justification;
- classifier proof for `mode=fresh`;
- OpenClaw registry state separately;
- unrelated plugin/runtime/data before/after comparison;
- all command counts and exit results;
- exact confirmation that no current installer was invoked and no current-product artifact was created;
- backup/recovery instructions for the operator, but do not auto-restore;
- one next-step recommendation.

Return exactly one:

- `PASS_LEGACY_REMOVED_FRESH_STOPPED_BEFORE_INSTALL`
- `BLOCKED_DUPLICATE_SOURCE_OR_COLLISION`
- `BLOCKED_LEGACY_IDENTITY_DRIFT`
- `BLOCKED_BACKUP_NOT_VERIFIED`
- `BLOCKED_NATIVE_INVENTORY_REPAIR_FAILED`
- `BLOCKED_NATIVE_HANDOFF_FAILED`
- `BLOCKED_NATIVE_PLUGIN_REMOVAL_UNSAFE`
- `BLOCKED_LEGACY_HOST_CLEANUP`
- `BLOCKED_FRESH_CLASSIFICATION`
- `BLOCKED_FINAL_PRESERVATION`
- `BLOCKED_REPORT_PUBLICATION_UNSAFE`

## Publication fence

The final report commit must change exactly the one Task 049 report path. Do not commit backup data, config/database copies, logs, manifests, command dumps, screenshots, or unrelated evidence.

## Progress communication

Report meaningful progress approximately every 3 minutes and immediately before/after backup verification, any native repair, PASSTHROUGH handoff, plugin uninstall, scheduler/process/path cleanup, Gateway restart, fresh classification, final preservation, and publication/blocker. Updates are not pause points.

## Prohibited

No current CogentNexus-OpenClaw installation; no OpenClaw upgrade/downgrade/reinstall; no manual SQLite edit; no Ollama/model mutation; no broad wildcard/parent deletion; no force kill; no primary-repository checkout/reset/clean/worktree action; no HermesAgent, Ecosystem, staged-capability-loop, Procmon/Task 027/038, merge, tag, Release, or archive action.
