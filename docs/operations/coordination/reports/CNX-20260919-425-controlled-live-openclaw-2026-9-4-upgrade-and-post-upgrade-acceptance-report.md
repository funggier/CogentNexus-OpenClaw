# CNX-20260919-425 — Controlled Live OpenClaw 2026.9.4 Upgrade and Post-Upgrade Acceptance Report

## Current classification

`LIVE_OPENCLAW_2026_9_4_UPGRADE_ACCEPTED`

CNX-425 completed all required upgrade, migration, non-semantic, and semantic Ticket-first acceptance gates.

The live OpenClaw 2026.9.4 runtime is retained. No rollback trigger is met.

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

## Provider/model readiness and semantic acceptance

The operator refreshed the 2026.9.4 Dashboard, created a new session, explicitly selected OpenAI / GPT-5.6 Luna, and sent the single bounded acceptance message.

Dashboard session:

`agent:main:dashboard:2edc17af-d27c-440d-b175-6730239d4d38`

Session evidence:

- session id: `bec7851d-28ae-47a2-9286-7be557f7e192`;
- provider: `openai`;
- model: `gpt-5.6-luna`;
- provider override: `openai`;
- model override: `gpt-5.6-luna`;
- agent runtime: `codex`;
- run status: `done`;
- output tokens: `8`.

Acceptance prompt:

`CNX-425 semantic acceptance — reply exactly CNX425_OK`

CNX Ticket:

- ticket: `CNXT-14f69475-e05d-4364-a362-6762cc939b23`;
- run: `bbc34b0d-d681-4bdd-bc4b-6b083e0fc046`;
- final ticket status: `completed`;
- assistant delivery text: `CNX425_OK`;
- delivery status: `delivered`;
- delivery mode: `native-dashboard-marker`;
- delivery error: none.

Exact durable event chain:

1. event 896 — `accepted`;
2. event 897 — `routed`;
3. event 898 — `response_ready`;
4. event 899 — `direct_response_durable`;
5. event 900 — `delivery_confirmed`;
6. event 901 — `completed`.

This proves one eligible Dashboard owner request became one durable Ticket before the accepted run completed, while provider/model/harness remained OpenClaw-owned.

### Ollama Dashboard model-picker repair

After the successful OpenAI acceptance, the operator reported that Ollama models could not be selected in the 2026.9.4 Dashboard.

Initial evidence:

- Ollama runtime was healthy and listed the installed models;
- the bundled Ollama plugin was loaded;
- Dashboard-facing `models.list` projected the Ollama entries as `available=false`;
- OpenClaw status reported that auth readiness could not be confirmed for `ollama/qwen3.8:27b`.

Installed local Ollama models:

- `qwen3.8:27b`;
- `qwen3.6:27b`;
- `qwen3:1.7b`.

Root cause was a post-migration provider-config/readiness gap in OpenClaw 2026.9.4:

- the migrated Ollama provider retained `api=ollama` and timeout policy;
- the authored local `baseUrl` was absent;
- the canonical non-secret local marker `ollama-local` was absent from the provider entry;
- the authored provider `models` path was absent;
- OpenClaw 2026.9.4 requires a local provider config with non-empty `baseUrl`, `api`, and at least one explicit model before its local non-secret marker is considered usable by the read-only model availability evaluator;
- the ordinary Dashboard catalog request does not request detailed unknown-availability preservation, so the incomplete readiness was projected as disabled.

Bounded canonical repair:

- set `models.providers.ollama.baseUrl=http://127.0.0.1:11434`;
- set `models.providers.ollama.apiKey=ollama-local`;
- retained `api=ollama`;
- retained `timeoutSeconds=2700`;
- authored the three actually installed Ollama models;
- populated model capability metadata from the live local Ollama `/api/show` endpoint;
- removed obsolete configured entries for locally absent `qwen3.5:9b` and `muse-glimmer:30b`;
- replaced the broad `ollama/*` allow-list entry with the three installed model ids so the Dashboard does not expose non-installed catalog rows.

Live capability evidence:

`qwen3.8:27b`

- context window: `262144`;
- reasoning: true;
- input: text + image;
- tools: supported.

`qwen3.6:27b`

- context window: `262144`;
- reasoning: true;
- input: text + image;
- tools: supported.

`qwen3:1.7b`

- context window: `40960`;
- reasoning: true;
- input: text;
- tools: supported.

Final Dashboard-equivalent session-scoped `models.list` now contains exactly these three Ollama entries and reports all three as `available=true`.

The earlier failed Ticket `CNXT-e723d7d6-1138-4019-ae3a-05dbd28813a9` was an internal pre-repair Ollama probe with a roughly 20-second timeout. It occurred before the final CNX-425 acceptance and before the picker repair. It is not the acceptance Ticket and no new failed Ticket was created by the picker repair.

## Final live state

Current live runtime after the repair:

- OpenClaw: `2026.9.4 (3a9d69d)`;
- Gateway listener: `127.0.0.1:18789`;
- Gateway PID after controlled repair restart: `27576`;
- Gateway health: `ok=true`;
- plugin errors: `0`;
- Discord: connected / ready;
- sessions: `21` after subsequent operator Dashboard activity;
- CogentNexus supervisor: enabled;
- latest controlled supervisor tick result: `0`;
- default model: `ollama/qwen3.8:27b`;
- CNX provider mode: `passthrough`;
- CNX Ticket-first: `true`.

Database integrity remains valid:

- shared state DB `user_version=17`, `quick_check=ok`;
- agent DB `user_version=19`, `quick_check=ok`;
- CNX DB `quick_check=ok`.

The increase from the migration-preserved 19 sessions to 21 occurred through post-upgrade operator activity and is not migration loss/corruption.

## Known residual external dependency

Managed Tailscale exposure remains disabled because the separate Windows Tailscale daemon is still stuck in `BackendState=NoState` and the LConnect account does not have permission to restart its LocalSystem service.

Current OpenClaw exposure therefore remains:

- `gateway.bind=loopback`;
- `gateway.tailscale.mode=off`.

This does not block the healthy local Dashboard/Gateway/CNX acceptance and does not trigger rollback under the CNX-425 contract. The verified rollback snapshot is retained.

## Final decision

`LIVE_OPENCLAW_2026_9_4_UPGRADE_ACCEPTED`

CNX-425 is complete.

Evidence supports:

- exact OpenClaw 2026.9.4 live upgrade;
- successful canonical state migration;
- preserved state integrity;
- healthy Gateway and expected channel/plugin state;
- qualified CogentNexus runtime loaded;
- one bounded Dashboard OpenAI semantic acceptance with exact Ticket-first durable event chain;
- successful delivery of `CNX425_OK`;
- post-upgrade Ollama Dashboard picker defect identified and repaired without dummy secrets or binary patching.

No rollback action is required.

The full verified pre-upgrade rollback snapshot must remain retained until normal operator retention policy permits deletion.
