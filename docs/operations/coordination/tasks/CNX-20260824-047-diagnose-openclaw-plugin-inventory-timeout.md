# CNX-20260824-047 — Diagnose OpenClaw Native Plugin Inventory Timeout

Status: `READY_FOR_CODEX`  
Execution mode: `MANUAL`  
Owner: ChatGPT  
Executor: Codex after operator's manual signal  
Start HEAD: `4fd61962fc5d6f8696fc8a8e30f3e6613e4432a8`

## Objective

Localize, without repairing or mutating live state, why OpenClaw `2026.7.1-2 (0790d9f)` does not return from:

`openclaw plugins list --json`

Task 047 is diagnosis only. It must establish the narrowest evidenced failure boundary across command bootstrap/config load, persisted installed-plugin registry, derived plugin discovery/manifest metadata, plugin-root fingerprinting, and dependency-status projection.

Do not guess the root cause and do not propose a live fix until the evidence distinguishes the failing stage.

## Predecessor

- report: `reports/CNX-20260824-046-remove-legacy-and-fresh-install-current.md`
- review: `reviews/CNX-20260824-046-remove-legacy-and-fresh-install-current.md`
- reviewed result: `BLOCKED_NATIVE_PLUGIN_INVENTORY_TIMEOUT`
- review decision: `ACCEPT_SAFE_PREMUTATION_STOP`

Task 046 performed zero destructive actions. Its removal/install authority is consumed and must not be reused.

## Duplicate and source fence

Before diagnostics:

1. fetch this branch and record exact fetched HEAD;
2. require this task to be active in both `ACTIVE.md` and `STATUS.md`;
3. stop if a matching Task 047 report already exists;
4. use a new isolated full clone or a clean read-only source checkout; never change the primary repository branch;
5. prove `4c825f8ec1ed6b43a419ad52e0bb85cee28007c1` remains an ancestor;
6. record non-coordination source drift after that implementation commit;
7. prove no concurrent CogentNexus lifecycle command and no Procmon process is running.

If coordination/source state is ambiguous, return `BLOCKED_DUPLICATE_OR_SOURCE_FENCE`.

## Exact upstream source boundary

Use the installed OpenClaw package and official upstream commit `0790d9f` as the authority. Read and hash the installed compiled artifacts/source maps corresponding to:

- `src/cli/plugins-list-command.ts`;
- `src/plugins/status-snapshot.ts`;
- `src/plugins/plugin-registry-snapshot.ts`;
- `src/plugins/plugin-metadata-snapshot.ts`;
- `src/plugins/status-dependencies-core.ts`.

Prove the live call path before running probes. Expected upstream structure:

1. config load;
2. `buildPluginRegistrySnapshotReport`;
3. `loadPluginRegistrySnapshotWithMetadata`;
4. metadata/manifest snapshot;
5. dependency-status projection;
6. JSON serialization/write.

Record any installed-source divergence rather than assuming equivalence.

## Read-only evidence collection

Create one unique temporary evidence directory beneath:

`%LOCALAPPDATA%\Temp\cnx047-openclaw-plugin-diagnostic\<UTC-ID>`

Temporary scripts and bounded stdout/stderr logs may be written only there. Never copy secrets into the report.

Record, with secret values redacted:

- Windows, PowerShell, Node, npm, OpenClaw versions;
- resolved `openclaw.cmd`, Node executable, global package root, state/config/database paths;
- relevant environment variable names and whether set, not secret values;
- plugin configuration keys, plugin ids, canonical load paths, install-record ids, and registry/index schema/version/count/size/timestamps;
- canonical plugin roots and whether each root exists, is local, is a reparse point/junction/symlink, or resolves outside the expected OpenClaw roots;
- hashes and sizes of the persisted registry/index artifacts and exact legacy plugin manifests/package manifests;
- Gateway/Ollama health and legacy controller generation before and after, read-only.

Do not publish tokens, API keys, Discord credentials, model prompts, conversation data, or full unredacted `openclaw.json`/state database content.

## Bounded phase probes

Run probes sequentially. Do not repeat an identical probe. Capture start/end UTC, wall time, exit/result, stdout/stderr bytes, CPU/IO samples, exact root process PID, verified descendants, and post-timeout orphan count.

A timeout wrapper may terminate only the exact process it created and its verified descendants. Never terminate Gateway, Ollama, CogentNexus controller/supervisor, shells, browser, or unrelated Node processes. If ownership is uncertain, do not terminate and return `BLOCKED_DIAGNOSTIC_PROCESS_OWNERSHIP`.

### Probe A — persisted registry surface

Run once, maximum 30 seconds:

`openclaw plugins registry --json`

This command is inspection only. Do not use `--refresh`.

### Probe B — baseline list with lifecycle trace

Run once, maximum 30 seconds, setting only for that child process:

`OPENCLAW_PLUGIN_LIFECYCLE_TRACE=1`

Command:

`openclaw plugins list --json`

Capture whether the `plugin registry snapshot` lifecycle line begins/completes and whether valid JSON appears.

### Probe C — process-local persisted-registry bypass

Run only if Probe B does not return valid JSON. Run once, maximum 30 seconds, setting only for that child process:

- `OPENCLAW_PLUGIN_LIFECYCLE_TRACE=1`
- `OPENCLAW_DISABLE_PERSISTED_PLUGIN_REGISTRY=1`

Command:

`openclaw plugins list --json`

This is a diagnostic comparison only. Do not persist either variable and do not refresh/repair registry state.

## Offline boundary microprobes

If A–C do not localize the stage, use a temporary Node diagnostic script outside all live OpenClaw/CogentNexus paths. Import only the already-installed compiled modules needed to time the synchronous boundaries proven from source.

Time each boundary independently with the same live inputs but no writes:

1. runtime config read;
2. persisted installed-plugin index inspection/read;
3. plugin-registry snapshot load;
4. metadata/manifest snapshot load;
5. dependency-status build for each already-enumerated plugin root;
6. JSON stringify of the resulting in-memory report.

Run each boundary at most once with a 20-second bound. Stop at the first hanging boundary. Do not import or register plugin runtime modules. Do not execute plugin code. Do not patch installed files.

If an exported compiled boundary cannot be called safely, report that limitation and use file-system timing only; do not invent an unsupported harness.

## File-system boundary checks

For only the exact roots implicated by the first failing boundary:

- canonicalize the path with a bounded call;
- inspect parent-chain reparse metadata;
- time direct directory metadata and the exact child names consulted by the upstream code;
- detect missing/inaccessible paths and paths resolving to unavailable/network locations;
- inspect ordinary ancestor `node_modules` candidates required by the legacy plugin package manifest.

No broad recursive scan, wildcard cleanup, ACL change, ownership change, antivirus exclusion, network mount, or file open intended to repair state is allowed.

## Root-cause standard

A root cause is confirmed only when one minimal comparison changes the outcome and the source path explains why, or when an exact boundary consistently hangs while the immediately preceding boundary completes.

Distinguish:

- persisted registry/database read;
- stale-policy/source fingerprint and derived discovery fallback;
- one exact plugin root/load path;
- one dependency ancestor lookup;
- JSON serialization/output;
- command bootstrap/config load;
- environmental/external wait;
- insufficient evidence.

Do not label the legacy CogentNexus plugin as the cause merely because it is installed.

## Required poststate

Before publication prove:

- zero diagnostic child/orphan processes;
- legacy controller mode/generation unchanged;
- `cnx.cmd`, `skills\cogentnexus`, and `.cogent` unchanged;
- no `cnxclaw.cmd`, new skill, or new state root created;
- OpenClaw config, installed-plugin registry/state database, scheduled task, Gateway, Ollama/models, AGENTS, primary repository, HermesAgent, Ecosystem, staged-capability-loop, and Procmon evidence unchanged;
- temporary evidence directory inventory and hashes recorded; it may remain for review.

## Report

Publish exactly one report:

`docs/operations/coordination/reports/CNX-20260824-047-diagnose-openclaw-plugin-inventory-timeout.md`

The report must include:

- fetched start HEAD and publication fence;
- installed/upstream source mapping and hashes;
- redacted inventory of relevant live paths/state;
- probe A/B/C commands, times, exits, lifecycle trace, stdout/stderr byte counts, CPU/IO/process samples, and orphan checks;
- offline microprobe results if used;
- exact first failing boundary and supporting comparison;
- confirmed root cause or explicitly bounded uncertainty;
- before/after hashes and live runtime poststate;
- one narrow next-step recommendation;
- explicit statement that no repair, lifecycle, removal, or installation occurred.

Return exactly one:

- `PASS_ROOT_CAUSE_LOCALIZED`
- `BLOCKED_DUPLICATE_OR_SOURCE_FENCE`
- `BLOCKED_DIAGNOSTIC_PROCESS_OWNERSHIP`
- `BLOCKED_INSTALLED_SOURCE_DIVERGENCE`
- `BLOCKED_DIAGNOSTIC_ORPHAN`
- `BLOCKED_INSUFFICIENT_EVIDENCE`
- `BLOCKED_REPORT_PUBLICATION_UNSAFE`

## Publication fence

The report commit must change exactly the one Task 047 report path. Do not commit temporary scripts/logs, copied config/database files, hashes as separate files, screenshots, or unrelated evidence.

## Progress communication

Report meaningful progress approximately every 3 minutes and immediately after source mapping, each bounded probe, root-cause localization, poststate verification, and publication/blocker. Progress updates are not pause points.

## Prohibited

No CogentNexus disable/stop/start/reset/uninstall/install; no plugin enable/disable/install/uninstall/update/registry refresh; no `doctor --fix`; no OpenClaw config/state/database write; no scheduled-task change; no Gateway/Ollama lifecycle or model change; no Procmon/Task 027/038 access; no dump capture; no ACL/ownership/antivirus change; no primary-repository checkout/reset/clean/worktree action; no Ecosystem, staged-capability-loop, HermesAgent, merge, tag, Release, or archive action.
