# CNX-20260824-050 — Fresh-Install Current CogentNexus-OpenClaw v0.9.3

Status: `READY_FOR_CODEX`

Execution mode: `MANUAL_WITH_HUMAN_GATE`

Owner: ChatGPT

Executor: Codex after the operator's manual signal

## Goal

Install the reviewed current **CogentNexus-OpenClaw v0.9.3** exactly once from the coordination branch source onto the accepted fresh Windows baseline, then prove canonical namespace ownership, MANAGED/Ollama runtime health, and preservation of unrelated data.

This is a fresh installation only. Legacy CogentNexus has already been backed up and removed by Task 049. Do not repeat any Task 049 handoff, uninstall, cleanup, or restore action.

## Human authorization

After Task 049 was reviewed and the exact fresh boundary was presented, the operator authorized this successor with:

> `1`

This authorizes the single installer invocation and its reviewed product-owned effects described below. Scheduled execution remains disabled; execution begins only from the operator's manual Codex signal.

## Authoritative coordination and accepted predecessor

Read only these coordination gates:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

Do not use `docs/operations/STATUS.md` as a task gate.

Required predecessor:

- report: `docs/operations/coordination/reports/CNX-20260824-049-backup-remove-legacy-stop-at-fresh.md`
- review: `docs/operations/coordination/reviews/CNX-20260824-049-backup-remove-legacy-stop-at-fresh.md`
- accepted disposition: `ACCEPT_FRESH_WITH_EXPECTED_PREHOST_AGENTS_RESTORE`
- accepted review/status head before Task 050: `ade2a1e1815346d55fb0a230541f3fc12bcf6215`

Required repository implementation:

- implementation commit `4c825f8ec1ed6b43a419ad52e0bb85cee28007c1` must be an ancestor;
- there must be no non-coordination drift after that implementation commit;
- v0.9.3 namespace/ownership/install implementation is already reviewed `ACCEPT`; do not reimplement or repair it in this task.

## Canonical live targets

Workspace:

`C:\Users\CDQ-P\.openclaw\workspace`

Expected current identities:

- launcher: `cnxclaw.cmd`
- skill: `skills\cogentnexus-openclaw`
- state root: `.cogentnexus-openclaw`
- ownership manifest: `.cogentnexus-openclaw\ownership.json`
- plugin ID: `cogentnexus-openclaw`
- npm package: `openclaw-plugin-cogentnexus-openclaw` version `0.9.3`
- scheduled task: `CogentNexus-OpenClaw-Supervisor`
- application-data root: `%LOCALAPPDATA%\CogentNexus-OpenClaw`
- provider: Ollama only
- new AGENTS markers: `<!-- cogentnexus-openclaw:begin -->` and `<!-- cogentnexus-openclaw:end -->`

Forbidden legacy live identities include:

- `cnx.cmd`
- `skills\cogentnexus`
- `.cogent`
- plugin/config/install record `cogentnexus-rotation`
- scheduled task `CogentNexus Supervisor`
- legacy managed-block markers `<!-- cogentnexus:begin -->` / `<!-- cogentnexus:end -->`

Internal reviewed compatibility implementation files such as `host_v091.py` do not count as live namespace aliases because they are contained inside the canonical `skills\cogentnexus-openclaw` ownership root. Do not delete or rename reviewed source files in this task.

## Phase 0 — duplicate, source, and concurrency fence

1. Freshly fetch `funggier/CogentNexus-OpenClaw` branch `agent/v0.9.3-recovery-reality-tests`.
2. Use one new isolated full clone under `%LOCALAPPDATA%\Temp`. Do not use or mutate the primary repository at `C:\Users\CDQ-P\.openclaw\workspace` as a Git checkout.
3. Record fetched start HEAD.
4. Require the exact Task 050 task plus both authoritative coordination files to identify `CNX-20260824-050` as `READY_FOR_CODEX`.
5. Stop if the Task 050 report already exists.
6. Prove commit `4c825f8ec1ed6b43a419ad52e0bb85cee28007c1` is an ancestor.
7. Require the diff after that commit to contain no non-coordination path.
8. Require `VERSION`, plugin manifest, package manifest, canonical skill metadata, and installer to identify v0.9.3 / CogentNexus-OpenClaw exactly.
9. Parse `scripts\install.ps1` with the Windows PowerShell parser before live mutation.
10. Run `python scripts\check_namespace_isolation.py` from the isolated source and require success.
11. Prove no other Codex/CogentNexus install, migration, reset, uninstall, clean-reinstall, lifecycle command, or report publisher is active.
12. Prove no Procmon process/capture is active. Do not access retained Task 027/038 evidence.

If any source, duplicate, branch, or concurrency gate fails, stop before live mutation.

## Phase 1 — accepted fresh baseline revalidation

Before invoking the installer, record and require:

1. the current repository classifier returns exact `mode=fresh`, with empty `new` and `legacy` arrays;
2. OpenClaw native registry inspection succeeds and native `openclaw plugins list --json` succeeds within a bounded 60-second observation;
3. the existing unrelated plugin identity set contains the accepted fresh count of 71 and has no `cogentnexus-openclaw` or `cogentnexus-rotation`;
4. no canonical current launcher, skill, state, application-data root, plugin, config entry/install record/load path, or scheduled task exists;
5. no forbidden legacy launcher, skill, state, plugin, config entry/install record/load path, or scheduled task exists;
6. workspace `AGENTS.md` is exactly 7,196 bytes with SHA-256 `C9A664B73200AE5D6B0DA0908DE3256CDB4DDA8BA6FE99F5E6C5115C3983604C` and contains neither legacy nor current managed-block markers;
7. the verified external Task 049 backup remains present and unchanged at:

   `C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw-Legacy-Removal-Backups\20260824T105507Z`

8. its retained manifest SHA-256 remains `7525DAB74EE1801A26B4B1CF824CB22155E971BCB63697149580ED1B9F42BA3A`;
9. Gateway is healthy/reachable in native OpenClaw mode;
10. Ollama is healthy and the same four-model inventory is present;
11. capture redacted/hash-only sentinels for OpenClaw config/user data, unrelated plugins/npm projects, AGENTS baseline text, Ollama model/data inventory, primary-repository branch/status, HermesAgent, Ecosystem, staged-capability-loop, and retained backup/evidence paths.

Do not use `registry --refresh`, `doctor --fix`, an OpenClaw upgrade/reinstall, a manual SQLite/config repair, or a plugin workaround. If native inventory or the accepted baseline has drifted, return a blocker before installation.

## Phase 2 — one exact fresh installer invocation

Only after every Phase 0/1 gate passes, invoke exactly once from the isolated clone:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "C:\Users\CDQ-P\.openclaw\workspace"
```

Do not pass:

- `-SkipPlugin`
- `-SkipGatewayRestart`
- `-SkipAgentsPolicy`
- `-LinkPlugin`
- a custom provider or any custom backup/config argument.

The reviewed default selects Ollama. Do not run `clean-reinstall.ps1`, a Release archive installer, an install-over/migration path, or any manual substitute copy/plugin/config/task command.

The installer is authorized to perform its reviewed current-product operations:

- stage and install the canonical skill;
- initialize `.cogentnexus-openclaw`;
- add only the canonical CogentNexus-OpenClaw AGENTS managed block;
- run plugin `npm ci`, validation, database bootstrap, `npm pack`, and exact native plugin install;
- create `cnxclaw.cmd`;
- create and exact-verify the ownership manifest before MANAGED authority;
- configure/enable only plugin `cogentnexus-openclaw`;
- create/enable only `CogentNexus-OpenClaw-Supervisor`;
- start/verify the reviewed MANAGED Gateway/Ollama integration.

### Timeout and retry fence

Track the exact installer child PID/tree and report progress approximately every 3 minutes.

- An outer-wrapper timeout is not proof that the installer failed.
- If the exact installer child remains alive, do not invoke a second installer and do not terminate it; continue bounded observation and inspect durable stage/poststate.
- Once the installer script body has begun, its invocation count is one even if it later fails.
- Do not retry installation.
- Do not manually complete partial copy/plugin/config/manifest/scheduler state.
- Do not automatically restore Task 049 legacy state.
- If failure occurs before transactional `enable`, inventory every partial current artifact and native runtime state and stop.
- If transactional `enable` fails, capture the reported rollback stages and prove whether it returned to PASSTHROUGH/native Gateway; stop without another enable/install.
- A purely syntactic shell-launch error is correctable only if process evidence and all fresh sentinels prove the installer script body never began and no live mutation occurred.

No force-kill is authorized.

## Phase 3 — post-install ownership and namespace proof

A PASS requires installer exit code `0` plus all of the following:

1. classifier result exactly `mode=upgrade`, not fresh/legacy/mixed/partial;
2. exact ownership manifest verification using the installed `namespace_ownership.py`;
3. manifest fields identify product `cogentnexus-openclaw`, display name `CogentNexus-OpenClaw`, version `0.9.3`, canonical workspace/state/skill/launcher/plugin path, expected task/service identities, UTC install time, and `migrationSource: null`;
4. exactly one verified installed plugin payload and no ambiguous duplicate direct/npm payload;
5. `cnxclaw.cmd` resolves only the installed `cnxclaw_v093.py` under the canonical skill and state root;
6. `cnxclaw.cmd status` succeeds;
7. `cnxclaw.cmd check cogentnexus` succeeds;
8. `cnxclaw.cmd check provider ollama` succeeds;
9. `cnxclaw.cmd provider status` identifies Ollama only;
10. plugin inventory contains exactly one `cogentnexus-openclaw` v0.9.3 registration/payload in the expected enabled state and no legacy plugin;
11. no legacy launcher/skill/state/task/config/load-path/install-record exists;
12. no generic permanent alias such as `cnx.cmd` was recreated;
13. `CogentNexus-OpenClaw-Supervisor` exists, is enabled, uses the canonical Python/runtime/state paths, and no legacy supervisor task exists;
14. source and live namespace lint pass within their intended scopes.

## Phase 4 — MANAGED runtime and preservation proof

Require and report:

- controller mode `managed`;
- desired Gateway `running`;
- desired provider `running`;
- registered provider Ollama only;
- Gateway status and probe healthy/reachable;
- Ollama endpoint/process healthy;
- the same four-model inventory preserved, with no pull/delete/reconfiguration;
- no orphan installer/npm/OpenClaw/CogentNexus lifecycle process;
- exactly one pair of new AGENTS managed markers and zero legacy marker;
- removing the new managed block in memory reproduces the exact accepted 7,196-byte baseline content/hash;
- the new installation's AGENTS pre-host backup contains the exact accepted baseline hash `C9A664B...3604C`;
- OpenClaw config differences are limited to reviewed CogentNexus-OpenClaw plugin/settings/install-record effects;
- unrelated plugin identities/npm projects and unrelated OpenClaw user/config data remain preserved;
- Task 049 external backup and manifest remain byte-identical;
- primary repository branch/status remains unchanged;
- HermesAgent, Ecosystem, staged-capability-loop, retained Procmon evidence, and unrelated workspace data remain unchanged.

Do not run destructive recovery tests, hard-crash injection, uninstall/reset/disable/stop/restart tests, Ticket side-effect tests, Procmon, or full recovery-reality scenarios in Task 050. This task proves fresh installation and healthy initial integration only.

## Failure handling

Return exactly one result:

- `PASS_FRESH_V093_INSTALLED`
- `BLOCKED_DUPLICATE_OR_SOURCE_FENCE`
- `BLOCKED_CONCURRENT_OPERATION`
- `BLOCKED_FRESH_BASELINE_DRIFT`
- `BLOCKED_NATIVE_PLUGIN_INVENTORY`
- `BLOCKED_FRESH_INSTALL_PARTIAL`
- `BLOCKED_MANAGED_ENABLE_ROLLED_BACK`
- `BLOCKED_POSTINSTALL_OWNERSHIP`
- `BLOCKED_POSTINSTALL_RUNTIME`
- `BLOCKED_PRESERVATION`
- `BLOCKED_REPORT_PUBLICATION_UNSAFE`

A nonzero installer exit, unresolved timeout, partial current namespace, failed ownership verification, PASSTHROUGH rollback, unhealthy Gateway/Ollama integration, or unexplained unrelated drift cannot be reported as PASS.

## Report and publication fence

Publish exactly one report:

`docs/operations/coordination/reports/CNX-20260824-050-fresh-install-current-v093.md`

The report must include:

- fetched start HEAD and source/ancestry/non-coordination-drift proof;
- exact preflight classifier/registry/plugin/runtime/sentinel results;
- exact installer command, invocation count, child PID/timing, exit code, and important stage outcomes;
- created/changed canonical artifact inventory;
- classifier and ownership-manifest verification output;
- launcher/plugin/scheduler/AGENTS/Gateway/Ollama poststate;
- before/after unrelated plugin/data/sentinel comparison;
- external backup preservation proof;
- all mutation/retry/restart/repair command counts;
- remaining uncertainty;
- one exact result token.

Do not commit machine-specific configs, backups, manifests, logs, command dumps, screenshots, binaries, package archives, secrets, or hashes as separate files. Commit only the Markdown report.

Before publication, prove the report commit changes exactly the one Task 050 report path relative to fetched execution HEAD. Use a commit message beginning:

`report: CNX-20260824-050 fresh install current v0.9.3`

No implementation repair or coordination-file edit is authorized inside Task 050.

## Progress communication

Report meaningful progress approximately every 3 minutes and immediately after:

- source/duplicate/concurrency fence;
- fresh classifier/native inventory/sentinel proof;
- immediately before installer invocation;
- skill/state/policy stage;
- plugin install;
- ownership verification;
- transactional MANAGED enable;
- post-install namespace/runtime/preservation proof;
- report publication or any blocker.

Progress updates are not pause points unless a stop gate fires.

## Prohibited

No Task 049 repeat; legacy restore; clean reinstall; second installer invocation; install-over migration; manual partial completion; reset; uninstall; disable/stop/restart acceptance test; destructive recovery test; force-kill; broad deletion; wildcard/parent cleanup; OpenClaw upgrade/downgrade/reinstall; manual SQLite/config edit; Ollama/model mutation; primary-repository Git mutation; checkout/reset/clean/worktree operation; HermesAgent/Ecosystem/staged-capability-loop action; Procmon/Task 027/038 access; merge; tag; GitHub Release; or archive publication.
