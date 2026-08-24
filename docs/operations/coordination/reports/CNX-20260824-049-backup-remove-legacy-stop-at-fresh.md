# CNX-20260824-049 — Back Up and Remove Proven Legacy, Stop at Fresh

Status: **BLOCKED**

Result: `BLOCKED_FINAL_PRESERVATION`

Fetched start HEAD: `aa25dfa63a1e561676e25208cdf255acb205de9b`

Repository: `C:\Users\CDQ-P\AppData\Local\Temp\cnx049-clone-20260824T105331Z`

Branch: `agent/v0.9.3-recovery-reality-tests`

Human authority: the operator's Task 049 option `1` authorization recorded in the exact coordination `ACTIVE.md` and `STATUS.md`.

## Preflight and authority fences

Both exact authoritative paths, `docs/operations/coordination/ACTIVE.md` and `docs/operations/coordination/STATUS.md`, identified Task 049 as `READY_FOR_CODEX`. No matching report existed. A new isolated full clone was used; required commit `4c825f8ec1ed6b43a419ad52e0bb85cee28007c1` was an ancestor (exit `0`), non-coordination implementation drift was empty, and the primary repository remained on `master` with its pre-existing untracked state.

There were zero concurrent lifecycle commands and zero Procmon processes. No current namespace launcher, skill, or state existed. The repository classifier exited `0` with exact `mode=legacy`, `legacyMode=managed`. Controller was `managed`, desired Gateway/provider `running`, generation `32`.

Identity anchors matched:

- `cnx.cmd`: `0B2EB63FD725236BC6B8F9616307F2B454C4FEBE0BF46CE4DE68F32A9C61B637`
- legacy `SKILL.md`: `5F5136F0F280D4B00C8EF8CF75198BB8844C642CDF249E8A8C8ED63F90AF8C41`
- controller: `F173EFE6EEE6D4E826B5CAF127614BD9AFE292AAE8CC8261EA3A3E0EE2129E5F`
- plugin manifest: `367FC6790A56FAFF0FDF301EBE0E8ACBD64553A3832C0C17ED135025A46516A1`
- package manifest: `513E95654275B0A381025501D7056D61143E132EF85AD59368E358550DC73775`
- OpenClaw config: `F2A541DBDFDB8CDD08C1F4693734BF65763F0136804EEB19CA98C06A2BC1656A`
- pre-task `AGENTS.md`: `C9BFD0288A379D62BD4C43B5B782AAFE0CFCAE43651B48EB5794780609B7DBBE`

Gateway `2026.7.1-2` was reachable at PID 27560; Ollama had active `qwen3.5:9b` and the same four models; `CogentNexus Supervisor` was `Ready`.

## Native inventory gate

The single child-only traced `openclaw plugins list --json` gate returned normally in 4,934.76 ms with valid JSON, 151,572 stdout bytes, 1,617 lifecycle stderr bytes, registry source `persisted`, 72 plugins, and zero orphan. It proved enabled legacy id `cogentnexus-rotation`, package version `0.9.1`, and the exact managed root. The conditional registry-refresh/doctor repair ladder was skipped entirely.

## External verified backup

Backup root:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw-Legacy-Removal-Backups\20260824T105507Z`

The canonical root is outside workspace, OpenClaw state/config, legacy state, managed plugin, current product, and repository roots. ACL inheritance was removed and the final ACL grants `(OI)(CI)(F)` only to `CDQ-P\CDQ-P`.

The backup contains the exact launcher, complete legacy skill/state, exact managed plugin package, OpenClaw config, online SQLite backup, scheduler XML, redacted inventory/classifier/controller evidence, and reparse metadata. SQLite was copied through Python `sqlite3.Connection.backup`; two independent `pragma integrity_check` executions returned `ok`.

An initial backup-only copy followed the plugin's `node_modules\openclaw` junction and expanded the global package. Before any live mutation, that exact backup destination was removed and recopied with junction traversal disabled; the junction target was recorded as metadata. Final source/destination verification found 303 mirrored files, 2,265,852 bytes, all SHA-256 equal. Backup contains 312 total files including evidence/manifest/database/export. Manifest SHA-256 after verification: `7525DAB74EE1801A26B4B1CF824CB22155E971BCB63697149580ED1B9F42BA3A`; it remained unchanged at final verification.

## Handoff, uninstall, and cleanup

The exact workspace `cnx.cmd disable` was invoked once. The outer execution wrapper timed out while waiting, but durable poststate proved completion: controller became `passthrough`, desired Gateway `running`, provider `unchanged`, generation `33`; the legacy supervisor task was unregistered; no child remained. Gateway stayed healthy and was gracefully replaced with PID 40892. Ollama/model inventory remained unchanged.

`openclaw plugins uninstall cogentnexus-rotation --dry-run` exited `0` and targeted only the exact config entry, install record, and managed package directory.

`openclaw plugins uninstall cogentnexus-rotation --force` was invoked exactly once and exited `0`. Receipt: removed config entry, install record, and exact directory; Gateway restart required. Post-uninstall native inventory exited `0`, contained 71 plugins, legacy count zero, and unrelated plugin additions/removals both zero. The exact config entry/install record and managed root were absent.

Exact host cleanup removed only workspace `cnx.cmd`, `skills\cogentnexus`, and `.cogent`; the already-unregistered exact supervisor task remained absent. No wildcard/parent cleanup or force kill was used.

The receipt-justified `openclaw gateway restart` was invoked once and exited `0`; Gateway became healthy at PID 32936 with unchanged service command/profile and connectivity `ok`.

Command counts:

- native inventory preflight: 1, success
- registry refresh: 0; `doctor --fix`: 0
- backup roots created: 1; SQLite online backups: 1
- `cnx.cmd disable`: 1; durable result completed despite wrapper timeout
- uninstall dry-runs: 1; native uninstalls: 1, exit `0`
- post-uninstall inventory: 1, success
- legacy launcher/skill/state exact removals: one each
- legacy scheduler explicit unregister: 0 because disable removed it
- Gateway restarts after uninstall: 1, exit `0`
- current installer/clean reinstall/Release installer: **0**
- automatic restore: **0**

## Fresh proof and final blocker

The current repository classifier exited `0` with exact:

```json
{"mode":"fresh","new":[],"legacy":[]}
```

OpenClaw registry inspection separately returned state `fresh`, zero refresh reasons, and 71 persisted plugins. Legacy launcher/skill/state/controller/scheduler/plugin/config/load path/install record/root were absent. Current `cnxclaw.cmd`, current skill/state/plugin/controller/scheduler were also absent. No current CogentNexus-OpenClaw installation occurred.

Gateway, OpenClaw version, Ollama and four-model inventory were preserved. Backup manifest hash and SQLite integrity remained valid. Zero lifecycle/diagnostic orphan or Procmon process remained.

The immutable final preservation gate failed because workspace `AGENTS.md` changed during the authorized legacy disable handoff:

- before Task 049: 8,878 bytes, SHA-256 `C9BFD0288A379D62BD4C43B5B782AAFE0CFCAE43651B48EB5794780609B7DBBE`
- after handoff/removal: 7,196 bytes, SHA-256 `C9A664B73200AE5D6B0DA0908DE3256CDB4DDA8BA6FE99F5E6C5115C3983604C`, mtime `2026-08-24T10:58:42.1935794Z`

The poststate exactly equals legacy backup file `.cogent\install-backups\AGENTS.pre-host-change-20260822T101418Z.md` (same size/hash), proving `cnx disable` restored the pre-host AGENTS content. Task 049 nevertheless requires the AGENTS hash to remain unchanged. No file in the Task 049 external backup has the pre-task AGENTS hash because the task required hashing that sentinel rather than copying it. The task prohibits automatic restore, so no attempt was made to recreate or overwrite AGENTS.

## Result, recovery, and recommendation

Blocker type: final-preservation/task-behavior conflict. Legacy removal and `mode=fresh` succeeded, but the exact AGENTS preservation invariant did not.

Backup recovery instructions: retain the external backup unchanged. It contains the verified legacy launcher/skill/state/plugin/config/SQLite/scheduler export and manifest. Do not restore it automatically or broadly. Any recovery must be a reviewed exact-path operation; the live system currently is intentionally fresh, Gateway healthy, and legacy removed.

Narrow recommendation: ChatGPT should review whether the proven pre-host AGENTS restoration is the intended result of disable. If accepted, issue a successor acceptance task that records the new baseline without changing AGENTS. If the pre-task AGENTS content is required, first obtain an authoritative exact content source matching hash `C9BFD028...`; do not reconstruct it from memory or restore unrelated legacy state.

Human decision required: **YES** — decide whether to accept the restored pre-host `AGENTS.md` as the correct fresh-state baseline or provide an authoritative exact source for the pre-task AGENTS content.

No live OpenClaw repair, OpenClaw upgrade/reinstall, manual SQLite edit, current-product installation, Ollama/model mutation, broad deletion, force kill, primary-repository mutation, HermesAgent/Ecosystem/staged-capability-loop action, or Procmon evidence access occurred. No external side effect was repeated.
