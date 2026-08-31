# CNX-20260830-165 — Hermes Windows Install-Over Provenance and Health

## Disposition

`PASS`

The single authorized Windows install-over completed through the repository installer. The installed CogentNexus-OpenClaw plugin fingerprint exactly matches the frozen Task-164 repaired candidate, the plugin is enabled and loaded, ownership verification passes, the controller returned to MANAGED state, Gateway and Ollama are healthy, the startup adapter is ready, the SQLite database remains integral with all scoped counts unchanged, and no Dashboard semantic Send or other semantic UI interaction occurred.

The wrapper's `System.Diagnostics.Process.ExitCode` field serialized as `null` after the child terminated. A direct child exit code is therefore **not claimed**. This does not hide an installer error: all seven installer diagnostic substages have paired START/COMPLETE records with child `exit_code=0`, the installer emitted its explicit completion message, the one child PID terminated, and independent postflight identity/health checks passed.

## Authority and lineage

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Task: `CNX-20260830-165`
- Fresh authoritative execution HEAD: `75e0d8cb59a4763b87ecfdfdc96612c534a56a0b`
- Accepted Task-164 implementation: `80b87dfbe0d9176e421f3748b4cee0827db12d0c`
- Accepted Task-164 report: `a9eccaba3d3acd46530cd59d256a6b13702b29ef`
- Task-164 ChatGPT review: `ACCEPT`
- `git merge-base --is-ancestor 80b87df... 75e0d8c...`: PASS
- Product/install/runtime diff from the Task-164 implementation to execution HEAD for `plugins scripts skills package.json package-lock.json`: empty
- Coordination-only commits after the implementation were not treated as product changes.

The remote branch, `ACTIVE.md`, `STATUS.md`, Task-165 task file, Task-164 review, and report-absence fence were re-read immediately before the live mutation. The live mutation gate remained at `75e0d8cb59a4763b87ecfdfdc96612c534a56a0b`, Task 165 remained `READY_HERMES`, and the Task-165 report did not yet exist.

## Frozen candidate provenance

Candidate preparation occurred in a fresh isolated checkout of the authoritative remote branch before live mutation.

- `npm ci --ignore-scripts`: exit `0`
- `npm run plugin:validate`: exit `0`
- mixed-plugin/schema artifact verification: PASS
- ticket DB bootstrap verification: PASS
- package-content verification: PASS
- package file count during the actual installer: `182`
- Package: `openclaw-plugin-cogentnexus-openclaw-0.9.3.tgz`
- Frozen package size: `205195` bytes
- Frozen package SHA-256: `ae4181d1a5c107c5077f40338701aa1b801e362b7f61d6accdadae696f7d23ba`
- Candidate plugin fingerprint: `5b23040f26ab1148c44647429cc5eff0ef89505e2f068b72d41d9a5fb0ee02e5`
- Task-164 production TypeScript SHA-256: `7f85723bb117944a3e44fddd1452fd38d85239a369b6fc8543a6810a92f69e20`
- Built production JavaScript SHA-256: `23c11f2107146710a5b0e5f930e310aa747a44f6286969a35477af1eda541ca3`

The frozen package was copied outside the installer/source deletion roots before the installer ran. The installed fingerprint is the authoritative content-parity proof because the supported installer independently rebuilds and packs the current source before installation.

## Read-only preflight

Preflight timestamp: `2026-08-30T17:37:21.430675+00:00` UTC.

- Existing controller: `mode=managed`, `desiredGateway=running`, `desiredProvider=running`, selected provider `ollama`
- Existing installed fingerprint: `07ac85dcc4eddca65d2107bac9123bedaf14751bedc66d2e8c5a12d88cf82d96`
- Gateway: healthy, OpenClaw `2026.7.1-2`, loopback `127.0.0.1:18789`, connectivity `ok`
- Ollama: reachable, healthy, ready; four models reported
- Startup adapter: installed, `State=Ready`, `Enabled=true`, `LastTaskResult=0`
- System/plugin/OpenClaw/Gateway/model/storage/recovery/delivery/resources checks: exit `0`
- Recovery: `READY`; no maintenance marker; no active Ollama recovery incident
- Delivery: `READY`; pending terminal deliveries `0`
- SQLite read-only `PRAGMA integrity_check`: `ok`
- No concurrent installer or install-over wrapper was present.

Pre-install scoped SQLite counts:

| Table | Count |
|---|---:|
| `tickets` | 2 |
| `ticket_events` | 14 |
| `cnx_direct_model_call` | 2 |
| `cnx_direct_recovery` | 0 |
| `cnx_assistant_delivery` | 0 |
| `ticket_outbox` | 0 |
| `cnx_sessions` | 3 |

## Exact authorized install-over

Exactly one supported installer child was launched:

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Users\CDQ-P\AppData\Local\Temp\cnx165-hermes-20260830T172744Z\repo\scripts\install.ps1" -Workspace "C:\Users\CDQ-P\.openclaw\workspace"
```

- Wrapper PID: `22620`
- Installer PID: `12916`
- Start UTC: `2026-08-30T17:39:18.1794866Z`
- Completion observation UTC: `2026-08-30T17:52:29.4913275Z`
- Second installer launches: `0`
- Kills/retries/rollbacks/timeout redesigns: `0`
- Direct installer process exit code: **not captured** (`null` in process metadata)
- Installer explicit completion message: `CogentNexus-OpenClaw v0.9.3 installation completed successfully.`

Installer diagnostic stages:

| Stage | Start UTC | Complete UTC | elapsed_ms | exit_code |
|---|---|---|---:|---:|
| `ticket-db-bootstrap` | `2026-08-30T17:41:42.7658098+00:00` | `2026-08-30T17:41:42.8196936+00:00` | 53 | 0 |
| `plugin-npm-pack` | `2026-08-30T17:41:44.6586037+00:00` | `2026-08-30T17:41:45.2884331+00:00` | 629 | 0 |
| `plugin-rollover-prepare` | `2026-08-30T17:41:45.3178854+00:00` | `2026-08-30T17:48:52.5446197+00:00` | 427227 | 0 |
| `plugin-install-local-package` | `2026-08-30T17:48:52.5456263+00:00` | `2026-08-30T17:49:08.9508489+00:00` | 16404 | 0 |
| `plugin-disable-post-install` | `2026-08-30T17:49:08.9518505+00:00` | `2026-08-30T17:49:14.9340118+00:00` | 5981 | 0 |
| `plugin-rollover-finalize` | `2026-08-30T17:49:19.6924000+00:00` | `2026-08-30T17:49:22.8220610+00:00` | 3128 | 0 |
| `owned-runtime-ensure` | `2026-08-30T17:49:22.8240599+00:00` | `2026-08-30T17:49:22.9653156+00:00` | 141 | 0 |

Stage integrity: `7 START`, `7 COMPLETE`, matching order, no unpaired stage, all recorded child exit codes `0`.

The stderr stream contains npm deprecation/allow-scripts warnings and the expected transitional warning that the CogentNexus plugin was disabled while its config remained present. No installer exception or terminal error appears.

## Independent post-install identity and health

Postflight timestamp: `2026-08-30T17:52:58.665254+00:00` UTC.

Installed plugin registry entry:

- ID: `cogentnexus-openclaw`
- Version: `0.9.3`
- Root: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw`
- Entrypoint: `dist\v091-release-entry.js`
- Origin: `global`
- `enabled=true`
- `status=loaded`
- Required dependency installed: yes
- Installed plugin fingerprint: `5b23040f26ab1148c44647429cc5eff0ef89505e2f068b72d41d9a5fb0ee02e5`
- Installed fingerprint equals frozen candidate: **PASS**

Independent ownership verification exited `0` and reported:

- product ID `cogentnexus-openclaw`
- installed version `0.9.3`
- expected workspace, state root, skill path, plugin path, and launcher path
- installed-at `2026-08-30T17:49:23.113294+00:00`

Independent lifecycle/health results:

- Controller: `managed`, desired Gateway/provider `running`, selected provider `ollama`
- Gateway: running and healthy; connectivity `ok`; listener `127.0.0.1:18789`
- Ollama: reachable, healthy, ready; four-model inventory retained
- Startup adapter: installed, `Ready`, enabled, hidden-background-logon, `LastTaskResult=0`
- System/plugin/OpenClaw/Gateway/model/storage/recovery/delivery/resources checks: all exit `0`
- Delivery: `READY`, pending deliveries `0`
- Recovery: `READY`, no maintenance marker, healthy supervisor snapshot, no active provider incident
- No installer/wrapper process remained after completion.

The bounded OpenClaw log window from `17:39Z` through `17:53Z` contains the expected install, passthrough suppression, managed reload, CogentNexus pre-runtime/context fences, crash-start recovery with zero recovered/mutated delivery rows, and `gateway ready`. No CogentNexus plugin/schema `ERROR` or `FATAL` event was found. Brief `startup-sidecars-pending` WebSocket warnings occurred during scheduled Gateway restarts and were followed by `gateway ready`; they are not plugin-loader failures.

## Database and semantic side-effect proof

Post-install SQLite opened read-only and returned `PRAGMA integrity_check=ok`.

| Table | Before | After | Delta |
|---|---:|---:|---:|
| `tickets` | 2 | 2 | 0 |
| `ticket_events` | 14 | 14 | 0 |
| `cnx_direct_model_call` | 2 | 2 | 0 |
| `cnx_direct_recovery` | 0 | 0 | 0 |
| `cnx_assistant_delivery` | 0 | 0 | 0 |
| `ticket_outbox` | 0 | 0 | 0 |
| `cnx_sessions` | 3 | 3 | 0 |

- Dashboard semantic Sends performed by Task 165: **`0`**
- Dashboard focus/click/type/paste performed by Task 165: **`0`**
- Manual Ticket/workflow/outbox/delivery/database mutations: **`0`**
- Second inference/regeneration requests: **`0`**

## Local evidence hashes

The task's hard fence permits publishing only this matching report, so raw local captures were not added to GitHub. Their identities are recorded for auditability:

| Evidence | Bytes | SHA-256 |
|---|---:|---|
| frozen candidate package | 205195 | `ae4181d1a5c107c5077f40338701aa1b801e362b7f61d6accdadae696f7d23ba` |
| installer stdout | 93030 | `617b0cfe6f682c1812e44730a4014cf9e45ba6da22ce1ceca73874e623465cbf` |
| installer stderr | 928 | `a23ccfd64f36d329417b0182297d02c58d23b9732405b0fc098375666296f626` |
| installer-start metadata | 984 | `12da0ee04096f77e170b35c2fe0d885bc2b767561a931f0c87938ff80afa6cbd` |
| installer-final metadata | 1062 | `a002f4ee8f975dc0bdba890a5e8402cd2d042dfa45224abcdaf846f0e0a003a5` |
| read-only preflight | 199968 | `3e263060f69575f6b8e5fa2420c9324029b577aa1a2b7880c3510308f230ef32` |
| read-only postflight | 199972 | `87e5533ed4ee206c0ce6b1afcb48d45befec29a42e5231e8f7dd2a16c3d81a03` |
| bounded loader-log capture | 94567 | `4627a3ee062c634972eb6004eb857fa14bd667b604b203a5232f8db2e5761e93` |

Local evidence root:

```text
C:\Users\CDQ-P\AppData\Local\Temp\cnx165-hermes-20260830T172744Z
```

## Hard-fence compliance

Authorized live mutations were limited to one supported install-over invocation and its installer-owned package rollover/replacement, temporary PASSTHROUGH boundary, plugin disable/re-enable, Gateway restarts, skill replacement/backup, ownership update, startup adapter update, and managed convergence.

Forbidden actions performed: **none**.

No Dashboard semantic interaction, Send, duplicate confirmation, clean uninstall, uninstall/reinstall, reset, manual source patch, dependency upgrade, OpenClaw source modification, manual DB mutation, alternate installer, kill, retry, rollback redesign, release, tag, default/release-branch merge, or force push occurred.

## Conclusion and next gate

Task 165 is `PASS`: the repaired Task-164 candidate is installed with exact fingerprint parity and the Windows runtime is managed, loaded, healthy, and database-stable.

This result does **not** authorize a Dashboard Send. The next step requires ChatGPT review and a separate successor task for the controlled single-Send acceptance. Hermes stops after publishing this report.

## Publication

This report is published as a report-only commit. The final remote report commit SHA, exact parent/execution HEAD, remote blob SHA, and one-path changed-file fence are verified after push and reported in the executor handoff.
