# CNX-20260917-390 — Production Config Isolated Hook-Policy Replay

## Classification

`PRODUCTION_CONFIG_REPLAY_DIAGNOSTICALLY_BLOCKED`

The disposable replay used the exact OpenClaw `2026.7.1-2` CLI/loader path, the relevant production entry, and the required effective artifact. The real loader activated the plugin and the supported inventory reported `status=loaded`, `activated=true`, `origin=config`, and `hookCount=0`. However, this supported invocation did not expose `register(api)`, individual `api.on("before_agent_run")` calls, the host `registerTypedHook` policy diagnostic, or `hasHooks("before_agent_run")`. Therefore the requested accept/reject gate outcome cannot be classified from this run without inventing evidence.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Authoritative starting remote HEAD: `0995f3b22f7629f8eb77f530fef8a3c4db292a29`
- Authoritative starting local HEAD: `0995f3b22f7629f8eb77f530fef8a3c4db292a29`
- Starting status: `READY_FOR_HERMES`
- Final HEAD: recorded after publication and remote read-back

The remote branch was fetched before investigation and local/remote HEADs matched exactly. No historical CNX-360 through CNX-389 file was changed.

## Production baseline and read-only extraction

Production config was read-only at `C:\Users\CDQ-P\.openclaw\openclaw.json`.

Relevant entry: `plugins.entries.cogentnexus-openclaw`

- entry keys: `enabled`, `config`, `hooks`
- `enabled`: `true`
- `hooks.allowConversationAccess`: `true`
- `config` fields used: `ticketFirst=true`, `preInferenceAdmission=true`, `autoWorkflowCompletion=true`, `enforcedMode=true`, `autoResume=true`, `workspaceDir=C:\Users\CDQ-P\.openclaw\workspace`, `ticketDispatchLimit=1`, `ticketMaximumRunning=1`, `ticketMaximumAttempts=5`, `ticketRecoveryPollMs=60000`, `ticketDispatchPollMs=60000`, `ticketOutboxPollMs=60000`, `completionPollMs=60000`, `contextMaintenancePollMs=30000`, `providerMode=passthrough`
- no registration-mode field was present in the entry; installed discovery classified the plugin as non-bundled/config-origin, not bundled.
- production config SHA-256 observed read-only: `19d7e6acf53ce370ddc20e5e2a2547c9674c33b178208b79920cb0e9dce9b46b`

No secret-bearing field was needed in the relevant entry. The production file also contains unrelated gateway authentication material; it was not copied into the fixture, printed, or included in this report. Omitted category: gateway auth token, because it is unrelated to plugin registration and would create unnecessary secret exposure.

Production artifact/version baseline:

- OpenClaw: `2026.7.1-2 (0790d9f)`
- effective artifact: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
- artifact SHA-256: `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`

## Loader semantics verified from installed source

Installed source was inspected read-only. `config-normalization-shared-w2iz0aeC.js` preserves `hooks.allowConversationAccess` in normalized hook data. `loader-D8d2EvVh.js` constructs the real plugin registry and invokes the plugin load path. `registry-B8eQDFB4.js` contains the host `registerTypedHook` policy branch and its non-bundled conversation-hook diagnostic; the policy is supplied separately from the normalized plugin-entry hook policy. The installed source therefore supports the distinction between `entry.config`, `entry.hooks`, normalized entry, and host hook policy; no dependency was patched.

## Exact disposable fixture and runtime

A disposable config was created at:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx390-replay.json`

It contained only `plugins.load.paths` pointing to the installed CogentNexus extension root and the extracted `plugins.entries.cogentnexus-openclaw` entry. A disposable state directory was selected through `OPENCLAW_STATE_DIR=C:\Users\CDQ-P\AppData\Local\Temp\cnx390-state`. The production config was not modified and the production gateway was not contacted.

The real command executed was the installed OpenClaw CLI `plugins list --json`, which uses the real loader/plugin activation path. Fresh output for the CogentNexus record was:

- `origin=config`
- `enabled=true`
- `explicitlyEnabled=true`
- `activated=true`
- `activationSource=explicit`
- `activationReason=enabled in config`
- `status=loaded`
- source was the required effective artifact path
- `hookNames=[]`
- `hookCount=0`

The supported `plugins inspect cogentnexus-openclaw --json` invocation also reported `activated=true`, `status=loaded`, and `hookCount=0`. The disposable PID was not emitted by the CLI wrapper, so no PID is claimed; this is a diagnostic limitation, not a production PID. No semantic request was sent.

## Exact module identities

| Installed module | SHA-256 |
|---|---|
| `dist/loader-D8d2EvVh.js` | `3a10479bdcbb713692c3ded7dbd5baad27c1b17ae3566172c117d45916dabce7` |
| `dist/hook-runner-global-BmIrGlLG.js` | `c066170e97a2355603f0bdd3079a687bf835632856a741fa9a92683d7d4b2750` |
| `dist/runtime-D0xGMZdc.js` | `a050a101e3c352345179b77f8c304da99596238fcde95cf03319ebc11dea8791` |
| `dist/registry-B8eQDFB4.js` | `25f3ef82756d85281ad5c25375a5cd2f405989a1145ed438de05992e8c995376` |

## Lifecycle evidence boundary

Directly observed in the isolated process:

- real loader path returned a loaded plugin record;
- plugin was explicitly enabled and activated;
- source path and exact artifact identity matched;
- final supported inventory contained zero hooks.

Not observed and deliberately not inferred:

- `register(api)` entry event;
- `api.on("before_agent_run")` call/result;
- host `registerTypedHook` insertion or rejection;
- host policy diagnostic;
- final typed-hook inventory from the global runner;
- `hasHooks("before_agent_run")`.

Absence of the policy diagnostic from this CLI output is not evidence of acceptance. `hookCount=0` is a downstream symptom and cannot distinguish gate rejection from another loader/registry boundary.

## Comparison with predecessors

| Scenario | Config policy | Loader result | `before_agent_run` | Host diagnostic |
|---|---|---|---|---|
| CNX-385 known-good fixture | `true` | predecessor report: normalized path preserved the value and host gate accepted it in exact isolated A/B/C fixture | accepted/observable outcome as recorded by CNX-385; no extra detail invented here | recorded in CNX-385; this report does not restate unverified detail |
| CNX-390 production-shaped fixture | exact production value: `true` | fresh: loaded, activated, config-origin; `hookCount=0` | not exposed by supported CLI | not exposed; no pass inferred |
| CNX-381 rejection fixture | effective false/absent | predecessor report: real loader loaded plugin and register path ran | calls occurred but were rejected before final registry | exact non-bundled `allowConversationAccess=true` policy-block diagnostic recorded by CNX-381 |

CNX-381 remains direct isolated evidence that the false/absent effective policy rejects the targeted hook. CNX-385 remains direct isolated evidence for the known-good true-policy normalization/gate fixture. CNX-390 does not establish whether its true production-shaped value reached the gate.

## Direct evidence versus inference

Direct evidence is limited to the redacted entry extraction, exact hashes, disposable config path, exact version, real loader activation, and zero-hook supported inventory above.

Inference: the production-shaped entry was accepted by configuration discovery and activation, narrowing the question beyond plugin enablement. It does not prove production in-memory equivalence, host policy acceptance, or production root cause. The production in-memory gap is **not materially closed** by this replay; it is only narrowed to the boundary between activated loader record and unexposed typed-hook registration outcome.

This result neither proves nor disproves that configuration shape can reproduce CNX-381. A disposable instrumented copy or a supported loader-level lifecycle probe exposing the host registration boundary would be required for the requested accept/reject classification.

## Counts and hard-fence compliance

- semantic/model/provider requests: `0`
- production mutation count: `0`
- production Gateway restart/reload: `0`
- production config mutation: `0`
- environment mutation: `0`
- Scheduled Task mutation: `0`
- dependency patch: `0`
- CogentNexus source/artifact mutation/deploy: `0`
- debugger/inspector attachment: `0`
- Dashboard request: `0`
- TicketStore/admission/routing/auth changes: `0`
- permanent instrumentation: `0`
- historical CNX-360 through CNX-389 modifications: `0`
- release/tag/main changes: `0`
- force-push/history rewrite: `0`
- CNX-391 created/started: `0`

All temporary fixture files are outside the repository and disposable. No production gateway lifecycle action or semantic/model/provider request was issued.

## Remaining uncertainty

The supported CLI did not expose PID, `register(api)`, `api.on`, host policy diagnostic, typed-hook inventory, or `hasHooks`. Consequently the required accept/reject distinction remains unresolved. The isolated result is not a production root-cause claim and does not establish the historical production in-memory hook policy.

## Closeout

After publication, `ACTIVE.md` and `STATUS.md` are set to `WAITING_FOR_CHATGPT_REVIEW`. No successor task is created or started.
