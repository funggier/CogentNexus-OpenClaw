# CNX-20260919-425 — Controlled Live OpenClaw 2026.9.4 Upgrade and Post-Upgrade Acceptance Report

## Current classification

`WAITING_FOR_OPERATOR_SEMANTIC_SEND`

The controlled live upgrade itself has completed successfully through every non-semantic acceptance gate.

The only remaining CNX-425 phase is one bounded Dashboard owner-message acceptance. LConnect has no browser/UI automation surface, so substituting a CLI message would not prove the required Dashboard/provider/model/harness contract.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Task: `CNX-20260919-425`
- Parent: `CNX-20260919-424`
- Upgrade authorization commit: `40dcd82db91baa6826d426037ecae8f1ea6c94a1`
- Human final authority: Operator
- Executor: ChatGPT via LConnect

## Pre-upgrade live baseline

Verified immediately before mutation:

- OpenClaw: `2026.7.1-2 (0790d9f)`
- Gateway: `127.0.0.1:18789`
- Gateway PID: `13192`
- service owner: Windows Scheduled Task `OpenClaw Gateway`
- CNX supervisor: Windows Scheduled Task `CogentNexus-OpenClaw-Supervisor`
- sessions: `19`
- shared state DB: `user_version=1`
- agent DB: `user_version=1`
- CNX DB quick-check: `ok`

CNX runtime baseline:

- tickets: accepted `3`, cancelled `4`, completed `17`
- ticket events: `874`
- pending ticket outbox rows: `0`
- direct recovery: awaiting_delivery `1`, cancelled `2`, pending `2`
- assistant delivery: delivered `14`, pending `1`
- direct model calls: ended `21`
- inference attempts: ended `4`

## Rollback snapshot

The Gateway was gracefully stopped and the CNX supervisor disabled before the authoritative snapshot.

Rollback root:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\backups\CNX-20260919-425-preupgrade-20260919T054451`

### Authoritative OpenClaw-home snapshot

Use:

`openclaw-home-fidelity`

Do **not** use the earlier `openclaw-home` copy. The earlier copy dereferenced junctions and was explicitly rejected as rollback authority.

The fidelity snapshot used robocopy with junction/symlink preservation.

Verification:

- files: `83,595`
- bytes: `2,956,871,173`
- mirror mismatch: `0`
- failed: `0`
- extras: `0`
- source reparse/junctions: `10`
- snapshot reparse/junctions: `10`
- type/target matches: `10/10`
- dry mirror after copy: `0 copied`, `0 mismatch`, `0 failed`, `0 extras`
- critical config/session/workspace/state/CNX hashes: all source/snapshot matches
- shared SQLite quick_check: `ok`
- agent SQLite quick_check: `ok`
- CNX SQLite quick_check: `ok`

Also retained:

- old global OpenClaw package
- old npm wrappers
- scheduled task XML definitions
- rollback manifest
- rollback README

Binary-only downgrade over migrated state remains prohibited.

## Qualified packages

Exact OpenClaw target:

`openclaw-2026.9.4.tgz`

- SHA256: `4F1F656770461D4677DEA755B1899CBA12B912B06798C89A59E2F0C18688B761`
- SHA1: `C377DB97052EBBBC7CCC1EA9F466D38D12292C07`
- npm registry shasum matched exactly

Qualified CNX-424 plugin:

`openclaw-plugin-cogentnexus-openclaw-0.9.5.tgz`

- SHA256: `8A1014AA1B9D96D07D1DE1F6E79ABAB4F0CDD3AB960228C0849859703AAC8200`

Qualified CNX runtime JS SHA256:

`F443CC53E2F7267DF7AB0AA0C1A440771ABFD3C54BF7441BFB42748B40A5C9A5`

The installed live CNX runtime hash matches this value exactly.

## Exact OpenClaw installation

Installed from the pinned local tarball, not from `latest`.

Result:

- npm install exit: `0`
- live CLI: `OpenClaw 2026.9.4 (3a9d69d)`

## State/config migration

The first target plugin-install attempt correctly failed on retired config keys after target state migrations had begun. Because the full rollback snapshot was already verified, migration continued through the canonical doctor path:

`openclaw doctor --fix --non-interactive --yes --no-workspace-suggestions`

Doctor exit: `0`

Important completed migrations:

- shared OpenClaw state: `v1 -> v17`
- main agent DB: `v1 -> v19`
- legacy session store -> SQLite
- sessions: `19 -> 19`
- transcript events imported: `166`
- legacy transcript artifacts archived: `50`
- unreferenced JSONL artifacts archived: `117`
- auth/profile/device/TUI/config-audit/workspace state migrated
- legacy `gateway.tailscale.resetOnExit` retired
- model policy migrated into target schema
- explicit OpenAI session overrides preserved
- one stale Codex routing state cleared
- HEARTBEAT/TOOLS/workspace setup migrated according to target semantics

After migration:

- config validate: PASS
- shared DB user_version: `17`, quick_check `ok`
- agent DB user_version: `19`, quick_check `ok`
- CNX DB quick_check: `ok`
- migrated session count: `19`

## CNX and official plugin upgrade

The qualified CNX-424 tarball was installed with explicit capability/policy acknowledgement.

Result:

- install exit: `0`
- installed live dist hash matches qualified candidate
- accepted plugin surface persisted
- no CNX diagnostics

Official plugin drift was resolved before the successful Gateway start:

- Codex: `2026.9.4`
- Discord: `2026.9.4`
- llama-cpp: `2026.9.4`
- voice-call: `2026.9.4`

Discord dry-run initially saw registry `2026.9.5`, rejected it as incompatible with the 9.4 runtime, and selected compatible `2026.9.4`.

Final `pluginVersionDrift.drifts=[]`.

## Gateway service migration

The old gateway wrapper still carried the 2026.7.1-2 service marker, so the service was regenerated canonically:

`openclaw gateway install --force --port 18789 --json`

Result:

- `ok=true`
- Scheduled Task regenerated for the 2026.9.4 runtime
- Node heap wrapper uses `--max-old-space-size=8192`

## Tailscale startup blocker and bounded repair

The first target Gateway startup reached HTTP-server startup but failed closed because:

`tailscale serve failed: unexpected state: NoState`

OpenClaw v2026.9.4 source review confirmed that managed `gateway.tailscale.mode=serve` failures are fatal by design.

External Tailscale state:

- Windows service: Running / Automatic
- CLI version: `1.102.4`
- active account/profile unchanged
- `LoggedOut=false`
- `WantRunning=true`
- backend: `NoState`
- health: `Tailscale is starting. Please wait.`
- no Tailscale IP

Non-destructive recovery attempts:

- `tailscale up`
- `tailscale up --timeout 30s`
- idempotent switch to already-active profile

All retained the same account/profile but did not leave `NoState`.

Restarting/killing the LocalSystem Tailscale service was denied to the LConnect account. No logout, reset, re-authentication, profile replacement, or identity deletion was attempted.

The pre-upgrade config had:

- `tailscale.mode=serve`
- retired `resetOnExit=true`

Stopping the old Gateway for maintenance likely left Tailscale down through that legacy reset-on-exit behavior.

To recover the local OpenClaw service without destructive Tailscale actions, the target config was changed canonically with:

`openclaw config set gateway.tailscale.mode off`

Current:

- gateway bind: `loopback`
- Tailscale managed exposure: `off`

This is the only known post-upgrade degraded external dependency. The rollback snapshot retains the original configuration.

## Successful live Gateway acceptance

After disabling managed Tailscale exposure:

- Gateway Scheduled Task started successfully
- live PID: `10396`
- listener: `127.0.0.1:18789`
- server version: `2026.9.4`
- build: `2026.9.4-release-3a9d69db306c-2026-09-10T22-53-16.719Z`
- RPC: connected
- health: `ok=true`
- sessions: `19`
- plugin errors: `0`
- Discord: enabled/running/connected/ready
- Dashboard HTTP: `200`

Loaded live plugins include:

- codex
- cogentnexus-openclaw
- discord
- ollama
- openai
- memory-core
- browser
- other target bundled plugins

Live startup log proves:

- CNX qualified plugin loaded
- `reply_dispatch` registration observed
- `hasReplyDispatch=true`
- CNX pre-runtime fence: no owner/workflow/native/synthetic failures
- crash-start recovery mutation counts: all `0`
- context pre-start fence: no failures
- Gateway reached `gateway ready`

## Runtime attestation

Live target attestation:

- `runnerReady=true`
- `globalHookCount=7`
- `latestRegistryPluginHookCount=null`
- classification: `AMBIGUOUS`

This is the previously reviewed conservative target-SDK behavior: OpenClaw 2026.9.4 does not expose the plugin-specific registry count through the public runtime SDK.

## Runtime-state preservation

CNX counters immediately before successful start and again after successful start were identical to the pre-upgrade baseline:

- tickets accepted `3`, cancelled `4`, completed `17`
- events `874`
- outbox `0`
- direct recovery awaiting_delivery `1`, cancelled `2`, pending `2`
- assistant delivery delivered `14`, pending `1`
- direct model calls ended `21`
- inference attempts ended `4`

Therefore startup did not unexpectedly consume legacy recovery/outbox state.

Post-start DB integrity:

- shared state v17 quick_check: `ok`
- agent DB v19 quick_check: `ok`
- CNX DB quick_check: `ok`

## Supervisor restoration

`CogentNexus-OpenClaw-Supervisor` was re-enabled after non-semantic health passed.

A controlled tick was triggered.

Result:

- task result: `0`
- Gateway PID remained `10396`
- Gateway health remained `ok=true`
- CNX counters remained unchanged

Normal operational ownership is restored.

## Provider/model readiness

Current OpenClaw model state:

- default: `ollama/qwen3.8:27b`
- CNX provider mode: `passthrough`
- CNX Ticket-first: `true`
- OpenAI OAuth: `status=ok`
- allowed OpenAI models include:
  - `openai/gpt-5.6-luna`
  - `openai/gpt-5.6-sol`
  - `openai/gpt-5.6-terra`

The most recent Dashboard session is an existing explicit override:

- provider: `openai`
- model: `gpt-5.6-luna`
- runtime: `codex`

Because CNX-419 previously demonstrated stale Dashboard/provider state, that old session must not be reused for the final semantic acceptance.

## Control UI freshness warning

After the upgrade, an existing client identifying itself as:

`Hermes/0.17.0`

attempted to connect with:

`clientBuild=legacy`

OpenClaw 2026.9.4 rejected it with:

`reload required`

This is a stale client/UI-build warning, not a Gateway/CNX health failure.

The local Dashboard itself responds HTTP `200`.

## Required single operator action

Use the local Dashboard:

`http://127.0.0.1:18789/`

Then:

1. reload/refresh the Dashboard so it loads the 2026.9.4 Control UI build;
2. create a **new session**;
3. explicitly choose provider **OpenAI**;
4. explicitly choose model **gpt-5.6-luna**;
5. send exactly one owner message:

`CNX-425 semantic acceptance — reply exactly CNX425_OK`

Do not resend if the UI appears slow. Report back only that the message was sent.

The executor will then inspect the new run/Ticket/event/model/delivery evidence and complete CNX-425.

## Current decision

`WAITING_FOR_OPERATOR_SEMANTIC_SEND`

The OpenClaw 2026.9.4 live upgrade is retained and healthy locally. No rollback trigger is currently met.

The full verified pre-upgrade rollback snapshot must remain untouched through final acceptance review.
