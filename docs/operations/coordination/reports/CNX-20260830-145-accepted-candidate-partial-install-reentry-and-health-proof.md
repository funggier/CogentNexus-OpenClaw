# CNX-20260830-145 — Accepted Candidate Partial-Install Re-entry and Health Proof

## Verdict

`PASS`

The supported v0.9.3 installer re-entered the preserved Task-142-derived partial state once and completed successfully. Post-install read-only proof shows the accepted candidate installed exactly, canonical ownership finalized, normal managed runtime state, healthy Gateway/provider/recovery/delivery, preserved durable history, no stale staging transaction, and zero Dashboard semantic Sends.

No Dashboard semantic operation was performed.

## Authority and execution boundary

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Fresh remote authority at start: `729b1d6478cda8736eda44cab670e195f03a990d`
- Fresh remote authority rechecked immediately before report publication: `729b1d6478cda8736eda44cab670e195f03a990d`
- Active task: `CNX-20260830-145`
- Initial and final gate: `READY_FOR_HERMES`
- Matching report was absent at both preflight and publication race check.
- Evidence root: `C:\Users\CDQ-P\AppData\Local\Temp\cnx145-20260829T174329Z\evidence`
- Detached source root: `C:\Users\CDQ-P\AppData\Local\Temp\cnx145-20260829T174329Z\source`

All timestamps below are UTC unless otherwise noted.

## Accepted candidate provenance

The deployment source was a fresh detached clone at the exact task-authorized implementation SHA:

`fb5781c1abd68280760bd5b3b4a65fabd8a60e58`

The source checkout was clean at that SHA. Phase-A validation was executed from `plugins/cogentnexus-openclaw`:

- Node: `v22.23.2`
- npm: `12.0.2`
- Python: `3.11.15`
- `npm ci`: exit `0`
- `npm run plugin:validate`: exit `0`
- package version: `0.9.3`
- packed file count: `178`
- package: `openclaw-plugin-cogentnexus-openclaw-0.9.3.tgz`
- package bytes: `200610`
- package SHA-256: `98a00a8a05ef4e7c600be045a4a4bbcbc6cb05f59acce5a3c54aabbacc80c014`
- candidate plugin fingerprint: `12c6d1b5b6ffd938353dd60c5d6190c34a609663369f619ff4fc7cbd176119e0`
- candidate `skills/cogentnexus-openclaw/scripts/namespace_ownership.py` SHA-256: `10dda985e6d4553a73a8cdd3ef7f660937482c3ef0c2d2da8d15bcbfe8d39b66`
- candidate `scripts/install.ps1` SHA-256: `446c4657db58a8e5895ac8d20e894c18d334f7b84ad72ca618a66f9a55c8b6a3`

The candidate fingerprint was recomputed from the candidate source; the historical Task-142 hashes were not reused as assumptions.

## Read-only preflight

Preflight ran from `2026-08-29T17:45:28Z` through `2026-08-29T17:45:42Z`.

- Direct OpenClaw entrypoint: `C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw\dist\index.js`
- OpenClaw version: `2026.7.1-2`
- Plugin inventory contained exactly one `cogentnexus-openclaw` identity.
- Raw plugin `rootDir`: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw`
- Plugin was `enabled=false`, `status=disabled`.
- Canonical root attestation: normal directory, `isReparse=false`, no link target.
- Installed preflight fingerprint: `12c6d1b5b6ffd938353dd60c5d6190c34a609663369f619ff4fc7cbd176119e0`.
- Installed preflight `namespace_ownership.py` hash: `e51f03553a24ea67037a3131b5ff4edb8aa435fbbc82b19974ae18f0d03df666`.
- Production `recovery-preflight`: `OWNERSHIP_PRESENT`, exit `0`.
- Candidate-aware production classifier: `mode=upgrade`, `pluginAlreadyExact=true`, `pendingRollover=false`, canonical direct replacement path.
- Lifecycle action resolver: `installPlugin=false`, `rolloverPlugin=false`.
- Controller mode: `passthrough`.
- Recovery and delivery checks: `READY`, `readOnly=true`, `stateChanged=false`, pending `0`.
- Gateway and Ollama were healthy before mutation.
- The preserved prior staging transaction was not manually inspected/removed/normalized; the supported installer owned the re-entry boundary.

One candidate-classification harness attempt failed before classification because PowerShell `Set-Content -Encoding utf8` produced a BOM that the production JSON reader correctly rejected. The inventory was then written without a BOM and the same read-only candidate classifier ran successfully. This was an executor harness correction, not a product result.

## Supported installer invocation

Exactly one supported invocation was performed from the detached candidate source:

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:/Users/CDQ-P/AppData/Local/Temp/cnx145-20260829T174329Z/source/scripts/install.ps1 -Workspace C:/Users/CDQ-P/.openclaw/workspace
```

- Invocation count: `1`
- Started: `2026-08-29T17:48:09.4116346Z`
- Ended: `2026-08-29T17:52:53.1323694Z`
- Exit code: `0`
- Native Node/npm path was pinned first while retaining the complete Python/PowerShell/Git toolchain.
- Installer output ended with: `CogentNexus-OpenClaw v0.9.3 installation completed successfully.`
- No retry, alternate installer, manual plugin operation, cleanup, reset, uninstall, or normalization was performed.

The installer-owned transition moved the controller from the preflight `passthrough` state to normal managed operation and refreshed ownership/runtime artifacts.

## Post-success proof

Post-success read-only probes ran from `2026-08-29T17:54:57Z` through `2026-08-29T17:55:05Z`.

### Candidate and ownership

- OpenClaw inventory still contained exactly one `cogentnexus-openclaw` identity.
- Post-install plugin root remained canonical: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw`.
- Post-install plugin state: `enabled=true`, `status=loaded`, version `0.9.3`.
- Installed plugin fingerprint exactly equals candidate: `12c6d1b5b6ffd938353dd60c5d6190c34a609663369f619ff4fc7cbd176119e0`.
- Installed `namespace_ownership.py` exactly equals candidate hash: `10dda985e6d4553a73a8cdd3ef7f660937482c3ef0c2d2da8d15bcbfe8d39b66`.
- Ownership `verify` exited `0`; manifest paths match workspace, state root, skill, launcher, and canonical plugin root.
- Ownership manifest `installedAt` refreshed to `2026-08-29T17:49:32.684197+00:00`.
- `install-staging` exists as an empty directory after completion; no stale transaction JSON remains.
- Direct plugin root remains a normal non-reparse directory.

### Runtime and provider health

- Controller mode: `managed`.
- Desired Gateway/provider: `running` / `running`.
- Gateway: healthy, connected, loopback listener `127.0.0.1:18789`.
- Gateway process uses native `C:\Program Files\nodejs\node.exe` and OpenClaw `2026.7.1-2`.
- Supervisor scheduled task and OpenClaw Gateway scheduled task are registered and Ready.
- Selected provider: `ollama`.
- Ollama API version: `0.32.15`; `/api/tags` returned the installed model inventory.
- Recovery check: `READY`, read-only, `stateChanged=false`.
- Delivery check: `READY`, read-only, `stateChanged=false`, pending terminal deliveries `0`.

### Durable data and semantic fence

SQLite was opened using an explicit `file:<path>?mode=ro` URI. `PRAGMA integrity_check` returned `ok`.

Post-install counts:

```text
tickets=2
ticket_events=14
cnx_direct_model_call=2
cnx_direct_recovery=0
cnx_assistant_delivery=0
ticket_outbox=0
cnx_sessions=2
```

The two existing Tickets remain terminal `failed` records with their original metadata timestamps. No new Ticket, event, model-call, recovery, outbox, delivery, or session row was created by this installer run.

Dashboard semantic Send count: `0`.

## Side-effect accounting

- Supported installer invocations: `1`
- Dashboard semantic Sends/resends: `0`
- Manual plugin copy/delete/replace/install/enable/disable: `0`
- Manual controller or ownership-manifest mutation: `0`
- Manual database/Ticket/workflow/outbox/delivery/recovery mutation: `0`
- Installer retries: `0`
- Reset/uninstall/clean reinstall: `0`
- Crash/recovery injection: `0`
- Unrelated process/service/task mutation: `0`
- Reboot: `0`
- Credential/secret access: `0`

Installer-owned lifecycle effects are included in the single supported invocation and are represented by the post-success evidence above.

## Harness notes and unproven items

- The first Phase-A inspection attempted a nonexistent repository-root `package.json`; the actual plugin package at `plugins/cogentnexus-openclaw/package.json` was then used successfully.
- A read-only preflight probe initially produced a BOM and was corrected without changing live state.
- A post-probe initially failed to write evidence due to a PowerShell case-insensitive variable collision; the probe was corrected and rerun read-only.
- These harness issues do not alter the single installer invocation or its exit code.
- No Dashboard semantic acceptance was authorized or performed; Dashboard behavior remains outside Task-145 scope.
- No crash/recovery injection was authorized or performed; recovery proof is read-only health proof only.

## Evidence index

Evidence is retained under:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx145-20260829T174329Z\evidence`

Key files:

- `a01-toolchain.txt`
- `a02-npm-ci.txt`
- `a03-plugin-validate.txt`
- `a04-npm-pack-json.txt`
- `a05-package-identity.txt`
- `a06-candidate-plugin-fingerprint.json`
- `a07-source-hashes.txt`
- `b03-openclaw-plugins.json`
- `b04-cnx-status.json`
- `b05-cnx-checks.json`
- `b06-filesystem.json`
- `b07-ownership-classify.json`
- `b08-recovery-preflight.json`
- `b09-candidate-classify-corrected.json`
- `b11-openclaw-direct.json`
- `c01-root-attestation.json`
- `c02-installed-fingerprint.json`
- `c03-ownership-verify.json`
- `d01-installer-run.json`
- `e01-openclaw-version.json`
- `e02-openclaw-plugins-direct.json`
- `e03-cnx-status.json`
- `e04-cnx-checks.json`
- `e05-installed-provenance.json`
- `e06-sqlite-readonly.json`
- `e07-ollama-health.json`
- `e08-gateway-listener.json`
- `e09-scheduled-task.json`
- `e10-filesystem-state.json`

Per the coordination contract, this matching report is the only repository file to be published for Task 145. Execution stops here for independent ChatGPT review.
