# CNX-20260825-059 — Re-prove Rollover Plan Input Binding

Status: **AWAITING_HUMAN_GATE**

Result: `AWAITING_PLUGIN_GENERATION_ROLLOVER_APPLY`

Current authorization: `PHASE_A_PLAN_ONLY`

Repository: `funggier/CogentNexus-OpenClaw`

Branch: `agent/v0.9.3-recovery-reality-tests`

Executor: Hermes (operator-selected substitute for Codex)

Fetched execution HEAD: `f6394e26db8df88934bc5cd487196eaee6f612c8`

## Scope and authorization

This report records only the authorized **Phase A plan checkpoint** for Task 059, created because Task 058 was reviewed `REWORK_INVENTORY_CAPTURE_BINDING_AMBIGUOUS`. It corrects the Task 058 evidence defect: exactly **one** immutable OpenClaw inventory capture, its size and SHA-256 recorded immediately, that exact file fed to the planner, and every verification performed from that same retained raw file (no recapture). No `rollover-apply`, installer, generation move/delete, ownership rewrite, plugin enable/disable/install/uninstall, lifecycle mutation, startup/supervisor enable, controller MANAGED transition, scheduler change, Gateway/Ollama/model mutation, process termination, primary-repository mutation, Procmon/Task 027/038 action, or mutation of the separate HermesAgent project/system was performed. Phase B apply remains explicitly unauthorized.

This task does **not** reuse any Task 058 inventory, recapture, plan JSON, or plan SHA-256. The rejected Task 058 plan SHA-256 `360393b0ac8a9ffee0ad603e67efb23b48fe06a7f5e9719d0bc18d03ace76c2c` is not reused, approved, or supplied to `rollover-apply`.

## Evidence boundary

Retained isolated clone:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx059-exec-20260824T180826Z\repo`

Retained evidence directory (unique, created before any live inspection, not reusing Task 058 evidence):

`C:\Users\CDQ-P\AppData\Local\Temp\cnx059-rollover-plan-20260824T181054Z`

Contents: `EVIDENCE_DIR.txt`, `01-preflight-and-capture.txt`, `inventory-capture-meta.txt`, `preflight-status.json`, `preflight-gateway.json`, `preflight-ollama.txt`, `preflight-startup.json`, `preflight-tasks.json`, `preflight-sqlite.json`, `preflight-hashes.json`, `task059-openclaw-plugins-list.raw.json`, `02-plan-gen.txt`, `task059-rollover-plan.json`, `verify_a4.py`, `03-verify-a4.txt`, `04-poststate.txt`, `poststate-status.json`, `poststate-startup.json`, `poststate-sqlite.json`, `poststate-hashes.json`.

## Duplicate and concurrency fence (satisfied)

- fetched execution HEAD `f6394e26…` equals remote HEAD `f6394e26…`;
- all five required ancestors present (`f379e5c5…`, `da3525c3…`, `0bfeefe9…`, `1650436…`, `0e93970…`);
- fresh isolated clone clean (working tree clean, 0 uncommitted);
- `ACTIVE.md` and `STATUS.md` both state `READY_FOR_HERMES` / `PHASE_A_PLAN_ONLY` and name Task `CNX-20260825-059`;
- no existing Task 059 report was present at fetched HEAD;
- zero concurrent installer / uninstall-reset / lifecycle / rollover-apply / report-publisher / Procmon / Task-059 executor processes observed.

## A1. Fresh preservation preflight (read-only)

Read-only exact-path commands, no mutation:

- `cnxclaw.cmd --json status` exit `0`: mode `passthrough`, generation `7`, desiredGateway `running`, desiredProvider `unchanged`, selectedProvider `ollama`, startup `disabled`, adapter `installed:false`;
- `openclaw gateway status --json` exit `0`: healthy/reachable at PID `47292` (OpenClaw `2026.7.1-2`);
- `ollama list` exit `0`: the same four model identities (`qwen3.5:9b`, `muse-glimmer:30b`, `qwen3.6:27b`, `qwen3.8:27b`);
- CogentNexus-OpenClaw supervisor task/adapter: absent. The only scheduled task matching `CogentNexus|OpenClaw` is the bundled `OpenClaw Gateway` task (not a product supervisor adapter);
- SQLite read-only (`file:...?mode=ro`): `integrity_check = ok`, counts `tickets=0`, `ticket_events=0`, `ticket_outbox=0`, `cnx_sessions=0`;
- ownership manifest still binds the prior exact generation payload root `c:\users\cdq-p\.openclaw\npm\projects\openclaw-plugin-cogentnexus-openclaw` (`ownership.json` `pluginPath`);
- exactly two canonical v0.9.3 product payload roots exist on disk (retired manifest-owned and active replacement); no unexpected third product-owned npm project root (`openclaw-plugin-cogentnexus-openclaw*` directory count under `%OPENCLAW%\npm\projects` = 2);
- unrelated plugin state preserved (71 unrelated of 72 `openclaw plugins list` records);
- primary repository `C:\Users\CDQ-P\.openclaw\workspace` observed read-only only.

Fresh SHA-256 values (all match the accepted Task 056/057 values):

- ownership manifest `ownership.json`: `D299F290D508C783AE33124FCC7E582349BF9C7A73C47D07DD38207EBF2F4207`;
- controller `host/controller.json`: `164F7FAC6081CA22AA6AD5391FB60E2EA57F26CF4A874CC4D19D50E02961EE7E`;
- registered policy `host/managed-policy.md`: `14EDEAD0180690C3D9565E864D2BDAAAE60E32DF9EF2C64EBD2A1238DF5CD8B4`;
- AGENTS baseline `AGENTS.md`: `C9A664B73200AE5D6B0DA0908DE3256CDB4DDA8BA6FE99F5E6C5115C3983604C`;
- launcher `cnxclaw.cmd`: `8DB1F256BB56C298FFFB14E8A761CAA7DBEC56EA334B0F4558C3CDA563AA46EF`;
- startup policy `runtime/startup-policy.json`: `CDF092FE1D076F0727B10BCE7789D44DC0BD05768CE9F2F825C9E072F0E6B7BE`;
- **Task 049 manifest** (`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw-Legacy-Removal-Backups\20260824T105507Z\manifest.json`, 176,927 bytes): `7525DAB74EE1801A26B4B1CF824CB22155E971BCB63697149580ED1B9F42BA3A`.

No preservation contradiction. A1 satisfied.

## A2. Single immutable OpenClaw inventory capture

Invoked **exactly once total** for Task 059:

`openclaw plugins list --json > <evidence>\task059-openclaw-plugins-list.raw.json` — exit `0`.

Immediately after capture, size and SHA-256 were recorded (`inventory-capture-meta.txt`):

- raw inventory path: `C:\Users\CDQ-P\AppData\Local\Temp\cnx059-rollover-plan-20260824T181054Z\task059-openclaw-plugins-list.raw.json`;
- raw inventory byte size: `151712`;
- raw inventory SHA-256: `B660AB4FEB4CCE610E61E0AF353F9B3046F6AA3DC857AB2607AF885679AF2BCD`.

The raw file was not overwritten, replaced, renamed, normalized, rewritten, or hand-edited. No `before-recapture` / `after-recapture` / transformed / substitute file exists; the inventory file count in the evidence directory is exactly one. All subsequent verification parses this exact retained raw file.

Bounded structure (parsed from the single raw file):

- `72` plugins total (`71` unrelated);
- exactly one canonical `cogentnexus-openclaw` record:
  - id `cogentnexus-openclaw`, name `CogentNexus-OpenClaw Bridge`, version `0.9.3`;
  - `rootDir` = `C:\Users\CDQ-P\.openclaw\npm\projects\openclaw-plugin-cogentnexus-openclaw__openclaw-generation__g-bbc979095f8845a1\node_modules\openclaw-plugin-cogentnexus-openclaw` (the expected active replacement generation root);
  - `origin` `global`, `enabled` `false`, `status` `disabled`;
  - `packageName` absent (`null`).

Requirement met: exactly one canonical v0.9.3 record at the expected replacement generation root, disabled, with `packageName` absent (package identity proven by the accepted Task 057 planner from the bound payload, per `packageNameEvidence: payload-package-json`).

Note: OpenClaw's raw `plugins list --json` serializes with nondeterministic key/array ordering across separate process runs, so the raw-byte SHA-256 can differ run-to-run while the canonical record and the planner's normalized `inventorySha256` binding are stable. This report binds the exact captured bytes (`B660AB4F…`, size 151712) and separately publishes the planner-normalized hash recomputed from this same file (see A4), establishing an unambiguous one-to-one binding between the single raw capture, the exact file supplied to the planner, and the published hashes.

## A3. Fresh machine-generated plan (single invocation)

Run exactly once (accepted Task 057 implementation, from the fresh isolated clone):

```text
python <isolated-clone>\skills\cogentnexus-openclaw\scripts\namespace_ownership.py rollover-plan
  --root "C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw"
  --workspace "C:\Users\CDQ-P\.openclaw\workspace"
  --app-data "C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw"
  --inventory-json <evidence>\task059-openclaw-plugins-list.raw.json
  --plan <evidence>\task059-rollover-plan.json
```

- planner `--inventory-json` argument was exactly the single A2 raw file path (recorded in `02-plan-gen.txt`: `INV_ARG=...task059-openclaw-plugins-list.raw.json`, `INV_EXISTS=yes`, `INV_SIZE=151712`);
- exit code `0`;
- plan generated by the planner; not hand-authored or edited.

Exact plan path: `C:\Users\CDQ-P\AppData\Local\Temp\cnx059-rollover-plan-20260824T181054Z\task059-rollover-plan.json`

Plan SHA-256 (independently computed from the on-disk file): `f81c60185b3e5ff5f7fd9ffdecda0760c53a5ce8d5aef1e7e2c84e8fd4fbf523`

The planner-reported `planSha256` was `f81c60185b3e5ff5f7fd9ffdecda0760c53a5ce8d5aef1e7e2c84e8fd4fbf523` — exact equality confirmed.

## A4. Input-binding and plan-binding verification

An independent verification script (`verify_a4.py`) parsed the single A2 raw inventory file, called OpenClaw inventory **zero** additional times, and recomputed every binding using the accepted planner's own helper functions (`_plugin_payload`, `_sha256_file`, `_project_tree_sha256`, `_json_sha256`). Result: **49 / 49 checks passed** (`A4_VERIFIED`).

Published bounded plan bindings:

- `schemaVersion` = `1`;
- `operation` = `cogentnexus-openclaw-plugin-generation-rollover`;
- `productId` = `cogentnexus-openclaw`;
- `installedVersion` = `0.9.3`;
- boundaries: `workspace` = `c:\users\cdq-p\.openclaw\workspace`; `stateRoot` = `c:\users\cdq-p\.openclaw\workspace\.cogentnexus-openclaw`; `openclawState` = `c:\users\cdq-p\.openclaw`; `applicationData` = `c:\users\cdq-p\appdata\local\cogentnexus-openclaw`;
- `controllerMode` = `passthrough`;
- `retiredPluginPath` = `c:\users\cdq-p\.openclaw\npm\projects\openclaw-plugin-cogentnexus-openclaw\node_modules\openclaw-plugin-cogentnexus-openclaw` (the manifest-owned prior generation root);
- `replacementPluginPath` = `c:\users\cdq-p\.openclaw\npm\projects\openclaw-plugin-cogentnexus-openclaw__openclaw-generation__g-bbc979095f8845a1\node_modules\openclaw-plugin-cogentnexus-openclaw`;
- `retiredProjectRoot` and `replacementProjectRoot` are distinct and both exist;
- `retiredFingerprint` = `0e5746d063af1bf6d82e0901ce4e5f3def57a9ecb41ec2d4bdd70ffcd6599ddb`;
- `replacementFingerprint` = `0e5746d063af1bf6d82e0901ce4e5f3def57a9ecb41ec2d4bdd70ffcd6599ddb` (equal to retired, expected for same-version v0.9.3 payloads);
- `retiredWrapperSha256` = `26f2cec7d59b75e70912150a177e880a92c90b7301930c2a4b917d64f02053ef`;
- `replacementWrapperSha256` = `26f2cec7d59b75e70912150a177e880a92c90b7301930c2a4b917d64f02053ef` (identical content, expected for same-version managed wrappers);
- `retiredWrapperProofSha256` = `b47da3bfd52abb5a01e3563a1a11ca3b445a0e9ddcfebe0dd4771725a1b0548c`;
- `replacementWrapperProofSha256` = `892c59eb0f1f6df03e5f2a9a225d4c972b81aab1369375da57b45b564a4aea32` (distinct);
- `retiredProjectTreeSha256` = `05981336d143a83b20d81803a29e66a849e845fe49064b8fd5c97cdecd3f94ee`;
- `replacementProjectTreeSha256` = `3621dbb46b6e6fadf5b0c0ecade860f1206640949804a26129612005202d1c7d` (distinct);
- `inventorySha256` (planner-normalized, recomputed from the single raw file) = `f6305077bccb11f3572d4a42be2b48377161bb2b017e1d9d80f49b5f950083f5` — matches the plan's embedded value;
- `activeRegistration` = `{ id: cogentnexus-openclaw, packageName: openclaw-plugin-cogentnexus-openclaw, packageNameEvidence: payload-package-json, version: 0.9.3, rootDir: <replacementPluginPath>, enabled: false, status: disabled }`;
- `activeRegistrationSha256` = `8cc399b12e2ab8fe0be352b8beea12fa093f19f97e07f62b6123c834ccda8c4d`;
- `manifestBeforeSha256` = `d299f290d508c783ae33124fcc7e582349bf9c7a73c47d07dd38207ebf2f4207` (equals the fresh ownership-manifest hash above);
- `manifestAfter.pluginPath` = the replacement payload path (ownership rebound to the replacement generation root);
- `backupPath` = `c:\users\cdq-p\appdata\local\cogentnexus-openclaw\plugin-generation-rollover-backups\openclaw-plugin-cogentnexus-openclaw-20260824t181210832193z` — unique (did not exist at plan time), under the exact product rollover-backup boundary, same volume (`C:`) as the retired project (enabling a same-volume atomic `os.replace`);
- exactly two expected product payload roots and no third; exactly one canonical active registration and no ambiguity.

All Task 059 A4 checks satisfied. No weakening of input, no manual repair, no inventory recapture.

## A5. Poststate and mandatory stop

After plan verification, only bounded read-only state checks were repeated (no `openclaw plugins list --json` recapture). Poststate hashes for ownership, controller, policy, launcher, and startup are byte-identical to preflight; SQLite remains `ok`/counts 0; controller remains `passthrough`, startup `disabled`. The single retained A2 inventory file is byte-identical to capture (`B660AB4F…`, 151712 bytes). No live state changed.

The task stops here. `rollover-apply` was not invoked. This report is the sole repository change for this execution.

## Exact commands and invocation counts

- `openclaw plugins list --json` (inventory capture): **1** invocation (A2).
- `namespace_ownership.py rollover-plan`: **1** invocation (A3).
- `openclaw plugins list --json` for poststate: **0** (explicitly not re-run).

| Step | Exit |
|------|------|
| clone (fresh isolated) | `0` |
| repo/remote HEAD compare | `0` |
| ancestor verify ×5 | `0` each |
| preflight `cnxclaw.cmd --json status` | `0` |
| preflight `openclaw gateway status --json` | `0` |
| preflight `ollama list` | `0` |
| preflight startup-policy read | `0` |
| preflight scheduled-task query | `0` |
| preflight SQLite read-only | `0` |
| preflight + Task 049 manifest hashes | `0` |
| A2 `openclaw plugins list --json` | `0` |
| A3 `namespace_ownership.py rollover-plan` | `0` |
| A4 `verify_a4.py` | `0` |
| A5 poststate (status/startup/sqlite/hashes) | `0` |

## Live mutation count

- `rollover-apply` invocations: **0**;
- installer / plugin install / uninstall / retirement: **0**;
- generation move / delete / ownership rewrite: **0**;
- lifecycle / enable / disable / start / stop / restart / reset commands: **0**;
- scheduler / supervisor creation or change: **0**;
- Gateway / Ollama / model mutation: **0**;
- process termination / force-kill: **0**;
- primary-repository mutation (until this report commit), Procmon / Task 027/038, or excluded HermesAgent actions: **0**;
- total live mutation count: **0**.

## Required publication values

- raw inventory path: `C:\Users\CDQ-P\AppData\Local\Temp\cnx059-rollover-plan-20260824T181054Z\task059-openclaw-plugins-list.raw.json`;
- raw inventory size: `151712`;
- raw inventory SHA-256: `B660AB4FEB4CCE610E61E0AF353F9B3046F6AA3DC857AB2607AF885679AF2BCD`;
- planner input path equals that raw inventory path: **yes**;
- plan path: `C:\Users\CDQ-P\AppData\Local\Temp\cnx059-rollover-plan-20260824T181054Z\task059-rollover-plan.json`;
- plan SHA-256: `f81c60185b3e5ff5f7fd9ffdecda0760c53a5ce8d5aef1e7e2c84e8fd4fbf523`;
- normalized inventory SHA-256: `f6305077bccb11f3572d4a42be2b48377161bb2b017e1d9d80f49b5f950083f5`;
- normalized active-registration SHA-256: `8cc399b12e2ab8fe0be352b8beea12fa093f19f97e07f62b6123c834ccda8c4d`;
- Task 049 manifest SHA-256: `7525DAB74EE1801A26B4B1CF824CB22155E971BCB63697149580ED1B9F42BA3A`;
- retired payload root: `c:\users\cdq-p\.openclaw\npm\projects\openclaw-plugin-cogentnexus-openclaw\node_modules\openclaw-plugin-cogentnexus-openclaw`;
- replacement payload root: `c:\users\cdq-p\.openclaw\npm\projects\openclaw-plugin-cogentnexus-openclaw__openclaw-generation__g-bbc979095f8845a1\node_modules\openclaw-plugin-cogentnexus-openclaw`;
- third product-owned payload root: **none**.

## Remaining uncertainty

None regarding plan safety or input binding. The machine-generated plan, every safety binding, and an unambiguous one-to-one binding between the single raw inventory capture, the exact planner input path, and the published raw/normalized hashes are all independently re-proven. Recovery apply remains unauthorized pending ChatGPT acceptance of this checkpoint and a separate explicit human approval of the exact plan SHA-256 `f81c60185b3e5ff5f7fd9ffdecda0760c53a5ce8d5aef1e7e2c84e8fd4fbf523`, followed by a new Task recording `PHASE_B_APPLY_AUTHORIZED`.

## Result token

`AWAITING_PLUGIN_GENERATION_ROLLOVER_APPLY`
