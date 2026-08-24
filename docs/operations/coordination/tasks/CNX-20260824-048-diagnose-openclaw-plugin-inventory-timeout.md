# CNX-20260824-048 — Diagnose OpenClaw Plugin Inventory Timeout with Exact Coordination Paths

Status: `READY_FOR_CODEX`  
Execution mode: `MANUAL`  
Owner: ChatGPT  
Executor: Codex after operator's manual signal  
Start HEAD: `33480c4319df9959a95f0788f063efbd03ed857f`

## Objective

Resume the read-only diagnosis that Task 047 correctly did not start. Localize why OpenClaw `2026.7.1-2 (0790d9f)` does not return valid JSON from:

`openclaw plugins list --json`

No repair, removal, lifecycle action, or installation is authorized.

## Predecessors

- Task 046 report/review: native plugin inventory timeout; destructive authority consumed.
- Task 047 report: `BLOCKED_DUPLICATE_OR_SOURCE_FENCE`.
- Task 047 review: `ACCEPT_SAFE_SPECIFICATION_STOP`.

Task 047 selected a non-authoritative project-status file because its fence used abbreviated names. Task 048 corrects only that specification defect.

## Exact authoritative coordination paths

For every execution, duplicate, source, and active-task gate, use only these exact repository paths:

1. `docs/operations/coordination/ACTIVE.md`
2. `docs/operations/coordination/STATUS.md`

Both must identify `CNX-20260824-048` and `READY_FOR_CODEX`.

`docs/operations/STATUS.md` is a project-level narrative document. It is **not** an execution, duplicate, source, active-task, or publication gate for Task 048. Its contents must not block Task 048.

Do not substitute, shorten, infer, glob, basename-match, or search for alternative `ACTIVE.md`/`STATUS.md` files.

## Duplicate and source fence

Before diagnostics:

1. fetch `agent/v0.9.3-recovery-reality-tests` and record exact fetched HEAD;
2. read the two exact authoritative coordination paths above by full repository-relative path;
3. stop only if the matching Task 048 report path already exists;
4. Task 047's existing report is expected and is not a duplicate of Task 048;
5. use a new isolated full clone or clean read-only source checkout; never change the primary repository branch;
6. prove `4c825f8ec1ed6b43a419ad52e0bb85cee28007c1` remains an ancestor;
7. record non-coordination implementation drift;
8. prove zero concurrent CogentNexus lifecycle commands and zero Procmon processes.

Return `BLOCKED_DUPLICATE_OR_SOURCE_FENCE` only if one of these exact checks fails, and name the exact full path/check.

## Exact installed-source mapping

Use the installed OpenClaw package and official upstream commit `0790d9f` as authority. Resolve and hash the installed compiled artifacts/source maps corresponding to:

- `src/cli/plugins-list-command.ts`
- `src/plugins/status-snapshot.ts`
- `src/plugins/plugin-registry-snapshot.ts`
- `src/plugins/plugin-metadata-snapshot.ts`
- `src/plugins/status-dependencies-core.ts`

Prove or refute this live call path:

1. runtime config load;
2. `buildPluginRegistrySnapshotReport`;
3. `loadPluginRegistrySnapshotWithMetadata`;
4. metadata/manifest snapshot;
5. dependency-status projection;
6. JSON serialization/write.

Record installed-source divergence instead of assuming equivalence.

## Temporary evidence boundary

Create one unique directory only beneath:

`%LOCALAPPDATA%\Temp\cnx048-openclaw-plugin-diagnostic\<UTC-ID>`

Temporary scripts and bounded stdout/stderr logs may be written only there. Do not commit them.

Record, with all secrets redacted:

- Windows, PowerShell, Node, npm, OpenClaw versions;
- resolved `openclaw.cmd`, Node executable, global package root, state/config/database paths;
- relevant environment variable names and set/unset status only;
- plugin config keys, ids, canonical load paths, install-record ids, registry/index schema/version/count/size/timestamps;
- canonical plugin roots, existence, local/network status, reparse/junction/symlink status, and final targets;
- hashes/sizes of persisted registry/index artifacts and exact legacy plugin/package manifests;
- Gateway/Ollama health and legacy controller generation before and after.

Never publish credentials, tokens, full config/database content, model prompts, or conversation data.

## Bounded probes

Run sequentially and never repeat an identical probe. Capture exact command/environment, start/end UTC, wall time, result/exit, stdout/stderr byte counts, lifecycle lines, CPU/IO samples, created PID, verified descendants, and post-timeout orphan count.

A timeout wrapper may terminate only the exact diagnostic process it created and verified descendants. Never terminate Gateway, Ollama, CogentNexus processes, shells, browser, or unrelated Node processes. If exact ownership cannot be proved, return `BLOCKED_DIAGNOSTIC_PROCESS_OWNERSHIP`.

### Probe A

Maximum 30 seconds:

`openclaw plugins registry --json`

Inspection only. Never add `--refresh`.

### Probe B

Maximum 30 seconds. Set only in this child:

`OPENCLAW_PLUGIN_LIFECYCLE_TRACE=1`

Run:

`openclaw plugins list --json`

Record whether the `plugin registry snapshot` phase completes and whether valid JSON appears.

### Probe C

Run only if B does not return valid JSON. Maximum 30 seconds. Set only in this child:

- `OPENCLAW_PLUGIN_LIFECYCLE_TRACE=1`
- `OPENCLAW_DISABLE_PERSISTED_PLUGIN_REGISTRY=1`

Run:

`openclaw plugins list --json`

This is a process-local comparison, not a repair. Do not persist variables or refresh registry state.

## Offline boundary microprobes

If A–C do not localize the failure, write one temporary Node diagnostic script in the Task 048 temp directory. Import only the installed compiled modules that source mapping proves safe.

Time each synchronous boundary at most once with a 20-second bound:

1. runtime config read;
2. persisted installed-plugin index inspect/read;
3. plugin-registry snapshot load;
4. metadata/manifest snapshot load;
5. dependency-status build for each already enumerated plugin root;
6. JSON stringify of the in-memory report.

Stop at the first hanging boundary. Do not import/register plugin runtime modules, execute plugin code, or patch installed files. If a compiled boundary is not safely exported, report the limitation and use bounded file-system metadata checks only.

## Exact-root file-system checks

For only roots implicated by the first failing boundary:

- bounded canonicalization;
- parent-chain reparse metadata;
- bounded direct directory metadata;
- exact child names used by upstream code;
- missing/inaccessible/unavailable/network targets;
- ordinary ancestor `node_modules` candidates required by the legacy plugin package manifest.

No broad recursive scan, wildcard, ACL/ownership change, antivirus exclusion, network mount, or cleanup.

## Root-cause standard

Confirm root cause only when:

- one minimal comparison changes the result and the exact source path explains it; or
- one exact boundary hangs while the immediately preceding boundary completes.

Distinguish persisted registry/database read, stale fingerprint/derived discovery, exact plugin root/load path, dependency lookup, JSON output, command/config bootstrap, external/environmental wait, and insufficient evidence.

Do not attribute the problem to legacy CogentNexus merely because it is installed.

## Required poststate

Before publication prove:

- zero diagnostic child/orphan processes;
- legacy controller mode/generation unchanged;
- legacy `cnx.cmd`, `skills\cogentnexus`, and `.cogent` unchanged;
- no `cnxclaw.cmd`, new skill, or new state root created;
- OpenClaw config/registry/database, scheduler, Gateway, Ollama/models, AGENTS, primary repository, HermesAgent, Ecosystem, staged-capability-loop, and Procmon evidence unchanged;
- temporary evidence inventory and hashes recorded; the temp directory may remain for review.

## Report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260824-048-diagnose-openclaw-plugin-inventory-timeout.md`

Include:

- fetched HEAD and exact coordination paths used;
- publication fence;
- installed/upstream source mapping and hashes;
- redacted relevant live-state inventory;
- probes A/B/C with timing/process/output evidence;
- offline/file-system microprobes if used;
- exact first failing boundary;
- confirmed root cause or bounded uncertainty;
- before/after hashes and runtime poststate;
- one narrow next-step recommendation;
- explicit zero repair/lifecycle/removal/install statement.

Return exactly one:

- `PASS_ROOT_CAUSE_LOCALIZED`
- `BLOCKED_DUPLICATE_OR_SOURCE_FENCE`
- `BLOCKED_DIAGNOSTIC_PROCESS_OWNERSHIP`
- `BLOCKED_INSTALLED_SOURCE_DIVERGENCE`
- `BLOCKED_DIAGNOSTIC_ORPHAN`
- `BLOCKED_INSUFFICIENT_EVIDENCE`
- `BLOCKED_REPORT_PUBLICATION_UNSAFE`

## Publication fence

The report commit must change exactly the one Task 048 report path. Do not commit temporary evidence, copied config/database data, scripts, screenshots, or unrelated files.

## Progress communication

Report meaningful progress approximately every 3 minutes and immediately after source mapping, each probe, localization, poststate verification, and publication/blocker. Updates are not pause points.

## Prohibited

No CogentNexus disable/stop/start/reset/uninstall/install; no plugin enable/disable/install/uninstall/update/registry refresh; no `doctor --fix`; no OpenClaw config/state/database write; no scheduler change; no Gateway/Ollama/model lifecycle; no Procmon/Task 027/038; no dump; no ACL/ownership/antivirus change; no primary-repository checkout/reset/clean/worktree action; no HermesAgent, Ecosystem, staged-capability-loop, merge, tag, Release, or archive action.
