# CNX-20260824-045 — Live Windows Clean-Reinstall Acceptance

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Execution mode: MANUAL_WITH_HUMAN_GATE  
Predecessor: CNX-20260824-044 (reviewed ACCEPT)

## Human authorization

The operator selected:

`1`

This explicitly authorizes the previously presented bounded Task 045 scope:

1. read-only preflight and exact current-state/ownership snapshot;
2. one verified external backup at the reviewed default root;
3. PASSTHROUGH/native handoff;
4. cleanup of exact proven CogentNexus-OpenClaw-owned artifacts only;
5. one fresh v0.9.3 installation;
6. post-install namespace, OpenClaw, Ollama, scheduler, and rollback evidence;
7. stop immediately on any failed gate, preserve backup/recovery evidence, and do not delete unrelated OpenClaw/Ollama data;
8. no CogentNexus-Ecosystem, CogentNexus-HermesAgent, staged-capability-loop, merge, tag, release, or archive action.

Scheduled ChatGPT/Codex execution remains disabled by the operator. Execution starts only from the operator's manual signal to Codex.

## Objective

Prove on the operator's Windows machine that a classifier/manifest/plugin-verified CogentNexus-OpenClaw v0.9.3 installation can enter the native PASSTHROUGH boundary, create its default external backup, clean only its owned installation, reinstall fresh from the reviewed branch source, and return healthy without harming OpenClaw, Ollama, HermesAgent, or unrelated data.

This authorization does **not** authorize legacy CogentNexus migration. If the live source is legacy, fresh-with-residue, mixed, partial, ambiguous, or not an exact coherent v0.9.3 upgrade, stop before the first mutation and report the precise next authorization required.

## Source and repository fences

- Freshly fetch `funggier/CogentNexus-OpenClaw`.
- Use branch `agent/v0.9.3-recovery-reality-tests`.
- Use one isolated full clone under a newly created `%LOCALAPPDATA%\Temp` directory as executable source and publication repository.
- Do not create or register a Git worktree.
- Do not checkout, reset, clean, repair, prune, or alter the primary live repository at `C:\Users\CDQ-P\.openclaw\workspace`.
- Record fetched start HEAD.
- Prove that executable/install/test paths have no changes after reviewed implementation `4c825f8ec1ed6b43a419ad52e0bb85cee28007c1` except coordination documents. If executable source differs, stop before live access.
- The live workspace's current branch may be `master`; do not change it.

## Exact live targets

- Workspace: `C:\Users\CDQ-P\.openclaw\workspace`
- OpenClaw state root: `C:\Users\CDQ-P\.openclaw`
- Active application data: `%LOCALAPPDATA%\CogentNexus-OpenClaw`
- Only allowed backup root: `%LOCALAPPDATA%\CogentNexus-OpenClaw-Clean-Reinstall-Backups`
- Expected new launcher: `%USERPROFILE%\.openclaw\workspace\cnxclaw.cmd`
- Expected skill: `%USERPROFILE%\.openclaw\workspace\skills\cogentnexus-openclaw`
- Expected state: `%USERPROFILE%\.openclaw\workspace\.cogentnexus-openclaw`
- Expected plugin identity: `cogentnexus-openclaw`

Do not supply a custom `-BackupRoot`. Do not use `-NoBackup` or `-LinkPlugin`.

## Phase 0 — duplicate, source, and collision fence

Before live inspection:

- confirm no matching Task 045 report already exists;
- confirm the task, authorization, reviewed Task 044 report/review, implementation SHA, and branch head;
- prove executable paths are unchanged from the reviewed implementation;
- ensure no other Codex/CogentNexus install/reset/uninstall/migration/clean-reinstall operation is active;
- do not launch Procmon or touch Task 027/038 retained evidence;
- publish a progress update.

A duplicate, source drift, or concurrent lifecycle operation is a hard stop.

## Phase 1 — read-only preflight

Perform only read-only inspection first:

- record Windows, PowerShell, Python, Node, npm, OpenClaw, and Ollama versions;
- record free space on the workspace/application-data/backup volume;
- record relevant CogentNexus-OpenClaw/CogentNexus paths, sizes, timestamps, hashes/manifests, plugin registrations, launcher identity, controller mode, scheduler/service identities, Gateway status, Ollama process/model status, and current application-data state;
- record the primary repository branch/status without modifying it;
- run the reviewed `namespace_ownership.py classify-install` from the isolated source clone against the live workspace/application-data root;
- if classification is `upgrade`, exact-verify the ownership manifest, plugin payload, launcher, skill, state root, version, and canonical paths;
- inventory exact legacy markers separately;
- record sentinels for CogentNexus-HermesAgent, unrelated OpenClaw npm projects/plugins, OpenClaw user/config data, AGENTS policy, and Ollama models/data so permitted and unrelated changes can be distinguished.

### Mandatory pre-mutation stops

Do not mutate anything and return the matching blocker if:

- classification is `legacy`: `BLOCKED_LEGACY_MIGRATION_NOT_AUTHORIZED`;
- classification is `fresh` while any plugin/task/service/product residue exists: `BLOCKED_UNOWNED_LIVE_RESIDUE`;
- classification is mixed, partial, ambiguous, or verification fails: `BLOCKED_LIVE_OWNERSHIP_UNPROVEN`;
- the exact v0.9.3 launcher/plugin/manifest is missing or inconsistent: `BLOCKED_LIVE_SOURCE_NOT_COHERENT`;
- default backup root is equal to/inside active application data or otherwise unavailable: `BLOCKED_BACKUP_BOUNDARY`;
- required commands, disk space, source integrity, or collision fences fail: `BLOCKED_PREFLIGHT`.

Only an exact coherent `upgrade` classification may proceed to Phase 2 under this authorization.

## Phase 2 — one default backup and one clean reinstall

If and only if Phase 1 passes:

1. Record the exact pre-mutation snapshot and timestamp.
2. Invoke exactly once from the isolated source clone:

   `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\clean-reinstall.ps1 -Workspace "C:\Users\CDQ-P\.openclaw\workspace"`

3. Do not pass `-NoBackup`, `-BackupRoot`, or `-LinkPlugin`.
4. Allow only the script's reviewed exact actions:
   - verified ownership preflight;
   - default external backup creation;
   - `cnxclaw disable` PASSTHROUGH/native handoff;
   - exact `cogentnexus-openclaw` plugin uninstall;
   - removal of manifest-bound CogentNexus-OpenClaw skill/state/launcher/plugin/application-data paths;
   - one fresh installation from the isolated reviewed source;
   - exact manifest verification and normal Ollama-backed enable/postchecks.
5. Capture complete exit code/output without exposing secrets.
6. Do not retry the destructive command.

The reviewed script's exact scoped `--force` plugin-uninstall behavior and exact owned-path PowerShell removals are authorized only inside this one invocation. No other force-kill, force Git operation, reset, clean, broad recursive deletion, or manual substitute deletion is authorized.

## Phase 3 — backup and post-install proof

After the single invocation, whether successful or failed:

- identify exactly one newly created timestamped directory below the default backup root;
- prove the backup is outside active application data;
- inventory backup contents and compare available pre-mutation hashes/metadata for ownership manifest, skill, launcher, plugin payload, application data, AGENTS.md, and OpenClaw config;
- preserve and report `clean-reinstall-recovery.json` if created;
- do not move, delete, overwrite, or automatically restore the backup;
- re-run exact ownership classification and manifest/plugin verification when a new installation exists;
- verify `cnxclaw.cmd status`, controller mode, plugin registration/enabled state, Gateway health, Ollama availability, and the expected CogentNexus-OpenClaw scheduler/service identity;
- prove legacy `cnx.cmd`, `skills/cogentnexus`, `.cogent`, and legacy plugin/config identities were not newly introduced;
- compare HermesAgent, unrelated OpenClaw plugin/project, OpenClaw user-data, and Ollama sentinels;
- distinguish expected OpenClaw config/AGENTS changes from unrelated drift;
- do not pull/delete models, edit provider configuration, or alter unrelated services.

If the single clean-reinstall invocation fails, preserve backup/recovery evidence and stop. Do not retry, manually finish cleanup, reinstall again, or restore without a new human decision.

## Acceptance gates

Return exactly one:

- `PASS_LIVE_CLEAN_REINSTALL_ACCEPTANCE`
- `BLOCKED_LEGACY_MIGRATION_NOT_AUTHORIZED`
- `BLOCKED_UNOWNED_LIVE_RESIDUE`
- `BLOCKED_LIVE_OWNERSHIP_UNPROVEN`
- `BLOCKED_LIVE_SOURCE_NOT_COHERENT`
- `BLOCKED_BACKUP_BOUNDARY`
- `BLOCKED_PREFLIGHT`
- `BLOCKED_PASSTHROUGH_HANDOFF`
- `BLOCKED_BACKUP_OR_CLEANUP`
- `BLOCKED_FRESH_REINSTALL`
- `BLOCKED_POSTINSTALL_VERIFICATION`
- `BLOCKED_UNRELATED_SIDE_EFFECT`
- `BLOCKED_REPORT_PUBLICATION_UNSAFE`

A PASS requires all phases, one external backup, one successful clean-reinstall invocation, exact new ownership, healthy required runtime integration, and no unexplained unrelated side effect.

## Report

Publish one report only:

`docs/operations/coordination/reports/CNX-20260824-045-live-windows-clean-reinstall-acceptance.md`

The report must include:

- fetched start HEAD and source-drift proof;
- exact commands used with secrets redacted;
- complete preflight classification and manifest/plugin evidence;
- pre/post mode, plugin, Gateway, Ollama, scheduler/service state;
- exact destructive invocation count;
- backup path, boundary, inventory, verification, and recovery-record result;
- removed/created/changed path accounting;
- expected versus unexplained OpenClaw config/AGENTS changes;
- HermesAgent, unrelated OpenClaw, Ollama, Ecosystem, staged-capability-loop, Procmon, and primary-repository side-effect accounting;
- remaining uncertainty;
- result token;
- human decision required YES/NO.

Do not commit machine-specific backups, configs, secrets, logs, command dumps, screenshots, binaries, package archives, hashes as separate files, or any live artifact. Commit only the Markdown report.

## Publication fence

Before publishing, prove the report commit changes exactly the one report path relative to fetched execution HEAD. Use a commit message beginning:

`report: CNX-20260824-045 live clean-reinstall acceptance`

No implementation repair is authorized inside Task 045. If a repository defect is discovered, stop and report it for ChatGPT diagnosis.

## Progress communication

Report meaningful progress approximately every 3 minutes and immediately after:

- duplicate/source/collision fence;
- live classification and exact ownership proof;
- every mandatory pre-mutation stop;
- just before the single destructive invocation;
- PASSTHROUGH and backup/cleanup transition;
- reinstall completion or failure;
- post-install/side-effect proof;
- report publication or publication blocker.

Progress updates are not pause points except the explicit legacy/mixed/partial/ownership gates above.

## Prohibited

Outside the exact single reviewed invocation, no live install, migration, reset, uninstall, cleanup, path deletion, plugin mutation, config mutation, Gateway/Ollama/scheduler/service mutation, process termination, Procmon use, Git checkout/reset/clean/worktree operation, merge, tag, GitHub Release, archive, Ecosystem, staged-capability-loop, or HermesAgent action.
