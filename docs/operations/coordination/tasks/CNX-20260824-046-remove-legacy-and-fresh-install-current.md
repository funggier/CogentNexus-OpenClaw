# CNX-20260824-046 — Remove Proven Legacy CogentNexus and Fresh-Install Current CogentNexus-OpenClaw

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Execution mode: MANUAL_WITH_HUMAN_GATE  
Predecessor: CNX-20260824-045 (reviewed ACCEPT_SAFE_PREMUTATION_STOP)

## Human authorization and approved design

The operator directed:

`งั้นลบก่อนแล้วลงใหม่เลยครับ เคลียร์ออกอย่างไรก็ได้แล้วทำตัวที่เป็นปัจจุบันลงไปใหม่ก่อน`

After ChatGPT narrowed the destructive boundary to proven CogentNexus legacy state only and presented the backup/native-handoff/exact-removal/fresh-install design, the operator approved:

`ครับเอาแบบนั้นอนุมัติให้ทำได้เลยครับ`

and reconfirmed:

`1`

This authorizes one bounded legacy removal followed by one fresh CogentNexus-OpenClaw v0.9.3 installation from the reviewed current branch source.

“Clear” applies only to classifier/proof-bound CogentNexus legacy identities. It does not authorize deletion or reset of OpenClaw, Ollama, models, general workspace/user data, CogentNexus-HermesAgent, CogentNexus-Ecosystem, or staged-capability-loop.

Scheduled ChatGPT/Codex execution remains disabled by the operator. Execution begins only from the operator's manual Codex signal.

## Objective

On the operator's Windows machine:

1. prove and externally back up the managed legacy CogentNexus installation;
2. restore native/PASSTHROUGH OpenClaw with the exact legacy launcher;
3. remove only proven legacy CogentNexus launcher/skill/state/plugin/config/load-path/scheduled-task identities;
4. prove the live workspace is clean of both legacy and unowned new-namespace residue;
5. install the reviewed current CogentNexus-OpenClaw v0.9.3 once as a fresh installation;
6. exact-verify new ownership, plugin, runtime integration, scheduler, namespace isolation, backup, and unrelated data.

This task replaces the previously proposed install-over migration. Do not run the legacy-detection migration path and do not run `clean-reinstall.ps1`.

## Source and publication fences

- Freshly fetch `funggier/CogentNexus-OpenClaw`.
- Use branch `agent/v0.9.3-recovery-reality-tests`.
- Use one newly created isolated full clone under `%LOCALAPPDATA%\Temp` for source and report publication.
- Do not create/register a Git worktree.
- Do not checkout/reset/clean/repair/prune or alter `C:\Users\CDQ-P\.openclaw\workspace` as a Git repository. Its current branch may remain `master`.
- Record fetched start HEAD.
- Prove executable/install/test source has no drift after reviewed implementation `4c825f8ec1ed6b43a419ad52e0bb85cee28007c1`, excluding coordination documents.
- If executable source drift exists, stop before live mutation.
- The installation source is the reviewed current branch clone, not a GitHub Release. Release-package installation remains a later gate.

## Exact live paths and identities

Workspace:

`C:\Users\CDQ-P\.openclaw\workspace`

OpenClaw state:

`C:\Users\CDQ-P\.openclaw`

External legacy-removal backup parent:

`%LOCALAPPDATA%\CogentNexus-OpenClaw-Legacy-Removal-Backups`

Proven legacy core paths:

- `%USERPROFILE%\.openclaw\workspace\cnx.cmd`
- `%USERPROFILE%\.openclaw\workspace\skills\cogentnexus`
- `%USERPROFILE%\.openclaw\workspace\.cogent`

Proven legacy identities:

- plugin ID/package family: exact `cogentnexus-rotation` / its exact resolved npm wrapper/package paths;
- scheduled task: exact `CogentNexus Supervisor`;
- exact legacy config entry/load paths identified by read-only inventory;
- legacy controller mode from Task 045: `managed`.

Expected fresh v0.9.3 identities:

- launcher: `cnxclaw.cmd`
- skill: `skills\cogentnexus-openclaw`
- state: `.cogentnexus-openclaw`
- plugin: `cogentnexus-openclaw`
- scheduled task/service identity: `CogentNexus-OpenClaw-Supervisor`
- active application data: `%LOCALAPPDATA%\CogentNexus-OpenClaw`

## Phase 0 — duplicate, source, and collision fence

Before live access:

- confirm no matching Task 046 report exists;
- confirm Task 045 report/review and this exact authorization;
- verify fetched source ancestry and coordination-only drift;
- scan read-only for another active CogentNexus install/migration/uninstall/reset/clean-reinstall/lifecycle command;
- confirm no Procmon capture/process and do not touch Task 027/038 retained evidence;
- publish a progress update.

Duplicate, source drift, or concurrent lifecycle operation is a hard stop.

## Phase 1 — mandatory read-only proof

Re-run complete read-only preflight:

- Windows, PowerShell, Python, Node, npm, OpenClaw, Ollama versions;
- free disk space;
- primary repository branch/status;
- Gateway, Ollama, legacy scheduler/task, controller mode, legacy paths, plugin projects, config entries, and load paths;
- exact Task 045 hashes:
  - `cnx.cmd`: `0B2EB63FD725236BC6B8F9616307F2B454C4FEBE0BF46CE4DE68F32A9C61B637`
  - legacy `SKILL.md`: `5F5136F0F280D4B00C8EF8CF75198BB8844C642CDF249E8A8C8ED63F90AF8C41`
  - legacy controller: `F173EFE6EEE6D4E826B5CAF127614BD9AFE292AAE8CC8261EA3A3E0EE2129E5F`
  - OpenClaw config: `F2A541DBDFDB8CDD08C1F4693734BF65763F0136804EEB19CA98C06A2BC1656A`
  - workspace `AGENTS.md`: `C9BFD0288A379D62BD4C43B5B782AAFE0CFCAE43651B48EB5794780609B7DBBE`
- re-run reviewed `namespace_ownership.py classify-install` against the live workspace and application-data root;
- record HermesAgent, unrelated OpenClaw projects/plugins/user data, Ollama models/data, and any other unrelated sentinels needed for post-comparison.

Operational controller/config/AGENTS drift since Task 045 must be explained semantically. Any unexplained launcher/skill identity drift, mixed namespace, current v0.9.3 residue, ambiguous plugin identity, or unowned state is a pre-mutation blocker.

### Native plugin inventory timeout gate

Task 045 timed out twice on `openclaw plugins list --json`.

Task 046 may make one final read-only attempt with a bounded maximum of 120 seconds. Capture process/child-process state and exit code.

If exact native plugin inventory still cannot be obtained, stop before backup/mutation as:

`BLOCKED_NATIVE_PLUGIN_INVENTORY_TIMEOUT`

Do not bypass this gate by guessing from config or deleting npm project directories manually.

### Required pre-mutation classification

Proceed only if:

- classifier result is exactly `legacy`;
- legacy mode is `managed`, `maintenance`, or `passthrough`;
- exact legacy launcher/skill/controller ownership is proven;
- exact legacy plugin registration/path and exact scheduled task/config/load-path identities are proven;
- no current/new CogentNexus-OpenClaw artifact exists;
- unrelated-data sentinels and backup boundary are established.

Otherwise stop read-only.

## Phase 2 — create and verify one external backup

Create exactly one timestamped directory below:

`%LOCALAPPDATA%\CogentNexus-OpenClaw-Legacy-Removal-Backups`

The backup must be external to the active application-data root and all paths that will be deleted.

Back up before any live mutation:

- legacy `.cogent`;
- legacy `skills\cogentnexus`;
- `cnx.cmd`;
- exact resolved legacy plugin wrapper/package/payload;
- OpenClaw config;
- workspace `AGENTS.md`;
- exported exact `CogentNexus Supervisor` scheduled-task definition;
- controller/state evidence and exact plugin/config/load-path inventory;
- a local recovery manifest describing source/destination paths, hashes, timestamps, and manual decision requirement.

Compute and compare source/destination hashes for all regular files. Require exact file counts, byte counts, and hashes before handoff or deletion. Preserve the backup even after success.

Do not commit backup content, secrets, logs, configs, scheduled-task XML, or hashes as separate repository artifacts.

Backup creation/verification failure is a hard stop with zero removal.

## Phase 3 — exact native/PASSTHROUGH handoff

If the legacy controller is `managed` or `maintenance`:

- invoke the exact proven `cnx.cmd disable` once;
- require exit `0`;
- verify the legacy controller reached `passthrough`;
- verify native OpenClaw Gateway health and Ollama availability;
- ensure no CogentNexus lifecycle command remains active.

If already `passthrough`, verify it and do not repeat disable.

A failed or ambiguous handoff stops the task. Do not remove anything while legacy mode may remain managed/maintenance.

## Phase 4 — exact legacy removal

After verified backup and PASSTHROUGH only:

1. Uninstall exact legacy plugin ID `cogentnexus-rotation` once using OpenClaw's supported non-interactive exact-ID command.
2. Remove only its proven exact config entry and exact load-path items.
3. Unregister only the exact scheduled task `CogentNexus Supervisor` once.
4. Remove only the proven legacy paths:
   - `cnx.cmd`
   - `skills\cogentnexus`
   - `.cogent`
   - exact residual legacy plugin wrapper/package/payload paths proven by inventory.
5. Re-run native plugin/config/task/path inventory.
6. Re-run the reviewed classifier and require exact `fresh`.
7. Verify native OpenClaw Gateway and Ollama remain healthy before installation.

The exact plugin uninstall's supported `--force` behavior, exact scheduled-task unregister without prompt, and exact owned-path removals are authorized only here. No force-kill, broad wildcard, recursive deletion of a parent OpenClaw/npm/workspace directory, manual deletion of unknown plugin projects, Git reset/clean, or unrelated config rewrite is authorized.

If cleanup becomes partial or any unrelated path/config changes unexpectedly, stop. Do not manually improvise broader cleanup.

## Phase 5 — one fresh current installation

If and only if Phase 4 proves exact `fresh` and native health:

Invoke exactly once from the isolated reviewed source:

`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "C:\Users\CDQ-P\.openclaw\workspace"`

Do not use:

- `-SkipPlugin`
- `-SkipGatewayRestart`
- `-SkipAgentsPolicy`
- `-LinkPlugin`
- custom provider/config/backup arguments.

Capture complete redacted output and exit code.

Do not retry installation. Do not run `clean-reinstall.ps1`. Do not invoke the install-over legacy migration path; legacy artifacts must already be absent and classifier result must be `fresh`.

If fresh install fails, preserve the external backup and local recovery manifest, verify native OpenClaw remains/restores reachable where possible without new mutation, publish the failure report, and stop. Do not automatically restore legacy state or manually finish installation without new human authorization.

## Phase 6 — post-install acceptance

After successful installer exit:

- require classifier result exactly `upgrade`;
- exact-verify new ownership manifest, schema, canonical paths, installed version, launcher, skill, state root, application-data root, plugin ID/package/payload, and unique resolved plugin path;
- verify `cnxclaw.cmd status`;
- verify controller mode/desired state;
- verify plugin registration and enabled/disabled state expected by the installer;
- verify Gateway status/probe;
- verify Ollama process/model availability without pull/delete/reconfiguration;
- verify exact new scheduler/service identity and absence of exact legacy scheduler;
- prove absence of `cnx.cmd`, `skills\cogentnexus`, `.cogent`, `cogentnexus-rotation`, and exact legacy config/load paths;
- prove external backup remains readable and hash manifest unchanged;
- compare OpenClaw config and AGENTS semantically, accepting only expected product-specific changes;
- prove HermesAgent, unrelated OpenClaw projects/plugins/user data, Ollama models/data, Ecosystem, staged-capability-loop, Procmon evidence, and primary-repository branch/status were not harmed.

Do not claim success from installer exit alone.

## Destructive and retry accounting

Maximum authorized lifecycle invocations:

- legacy disable: once if required;
- legacy plugin uninstall: once;
- legacy scheduled-task unregister: once;
- exact legacy config/load-path cleanup: one bounded transaction;
- exact proven legacy path removal: one bounded transaction;
- fresh installer: once;
- destructive retry: zero;
- automatic restore: zero;
- clean reinstall: zero.

Record actual counts.

## Results

Return exactly one:

- `PASS_LEGACY_REMOVED_AND_FRESH_V093_INSTALLED`
- `BLOCKED_DUPLICATE_OR_SOURCE_DRIFT`
- `BLOCKED_CONCURRENT_LIFECYCLE_OPERATION`
- `BLOCKED_LEGACY_OWNERSHIP_UNPROVEN`
- `BLOCKED_NATIVE_PLUGIN_INVENTORY_TIMEOUT`
- `BLOCKED_MIXED_OR_UNOWNED_STATE`
- `BLOCKED_BACKUP_CREATION_OR_VERIFICATION`
- `BLOCKED_NATIVE_HANDOFF`
- `BLOCKED_LEGACY_PLUGIN_OR_CONFIG_REMOVAL`
- `BLOCKED_LEGACY_PATH_OR_TASK_REMOVAL`
- `BLOCKED_FRESH_CLASSIFICATION`
- `BLOCKED_FRESH_INSTALL`
- `BLOCKED_POSTINSTALL_VERIFICATION`
- `BLOCKED_UNRELATED_SIDE_EFFECT`
- `BLOCKED_REPORT_PUBLICATION_UNSAFE`

A PASS requires all six phases, verified backup, exact legacy absence, one successful fresh installer invocation, exact new v0.9.3 ownership/runtime integration, and no unexplained unrelated side effect.

## Report

Publish exactly one report:

`docs/operations/coordination/reports/CNX-20260824-046-remove-legacy-and-fresh-install-current.md`

Include:

- fetched start HEAD and source-drift proof;
- exact authorization and destructive counts;
- Task 045 hash comparisons and any explained drift;
- native plugin-inventory timeout resolution;
- pre/post classifier, controller, plugin, config/load-path, scheduler, Gateway, and Ollama evidence;
- backup path/boundary/file-count/byte-count/hash verification without exposing secret values;
- exact removed/created/changed paths and semantic config/AGENTS accounting;
- installer command/result;
- exact new ownership/plugin/version evidence;
- legacy absence proof;
- unrelated-data/sentinel accounting;
- remaining uncertainty;
- one result token;
- human decision required YES/NO.

Do not commit machine-specific backups, recovery manifests, configs, logs, command dumps, screenshots, binaries, ZIP/TGZ/package artifacts, or secrets. Commit only the Markdown report.

## Publication fence

The report commit must change exactly the one report path relative to fetched execution HEAD.

Commit message must begin:

`report: CNX-20260824-046 remove legacy and fresh install`

No repository implementation repair is authorized. If source behavior prevents safe execution, stop and report it for ChatGPT diagnosis.

## Progress communication

Report meaningful progress approximately every 3 minutes and immediately after:

- duplicate/source/collision fence;
- legacy/hash/plugin inventory proof;
- backup verification;
- just before native handoff;
- PASSTHROUGH confirmation;
- exact plugin/config/task/path removal;
- fresh classification;
- just before and after the single installer invocation;
- post-install/side-effect proof;
- report publication or blocker.

Progress updates are not pause points after execution starts, except mandatory pre-mutation blockers.

## Prohibited

No clean reinstall, install-over migration, reset, broad purge, unrelated path deletion, force-kill, Git checkout/reset/clean/worktree action, release/tag/archive, Procmon/Task 027/038 access, CogentNexus-HermesAgent action, CogentNexus-Ecosystem action, staged-capability-loop action, OpenClaw user-data reset, Ollama model/provider change, or deletion outside exact proven legacy CogentNexus identities.
