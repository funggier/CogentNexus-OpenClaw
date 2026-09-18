# CNX-20260918-404 — Production Loader Cache and Registry Correlation Report

## Classification

`PRODUCTION_REGISTRY_CACHE_CORRELATION_INCONCLUSIVE`

Read-only production evidence proves PID 27372, the selected release artifact, the plugin-side registration events, and a persisted `plugins list --json` projection. Exact installed OpenClaw source proves cache-hit restore, active-registry compatibility/scope short circuits, and unconditional registry activation/replacement. No available production-local record correlates a loader invocation, cache decision, registry identity, activation ordering, or host typed-hook acceptance to PID 27372. The evidence is therefore neither a production cache/activation proof nor a source-only negative classification.

## Authority and starting identity

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Task: `CNX-20260918-404`
- Parent: `CNX-20260918-403`
- Embedded task baseline: `2f9c3b584476b9f8de581d4df0c4d7dbec474404` (stale; not used)
- Authoritative starting GitHub HEAD after explicit fetch: `0f81839e515783b5202e7c38ba094d287ee9cf18`
- Local starting HEAD: `0f81839e515783b5202e7c38ba094d287ee9cf18`
- Starting gate: `READY_FOR_HERMES`

The branch was fetched with an explicit refspec and `git ls-remote` matched the checked-out starting HEAD. A clean dedicated workspace checkout was used; an unrelated dirty checkout was not modified.

## Exact runtime, artifact, and module identity

- OpenClaw: `2026.7.1-2 (0790d9f)`
- Gateway PID: `27372`
- Gateway endpoint: `127.0.0.1:18789`
- Executable: `C:\Program Files\nodejs\node.exe`
- Command line: `"C:\Program Files\nodejs\node.exe" C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw\dist\index.js gateway --port 18789`
- Process creation: `2026-09-17 05:13:48` (local process query)
- Selected production artifact: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
- Selected artifact SHA-256: `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- Alternate, unselected/unproven artifact: `v091-dashboard-verified-delivery.js`, SHA-256 `1276bd624b62f96692eaa19f493f69e422771b6994b39ded94b2bcb3399e1f98`
- Installed module root: `C:\Users\CDQ-P\.openclaw\workspace\test\CogentNexus-OpenClaw\plugins\cogentnexus-openclaw\node_modules\openclaw\dist`

| Module | SHA-256 |
|---|---|
| `loader-D8d2EvVh.js` | `3a10479bdcbb713692c3ded7dbd5baad27c1b17ae3566172c117d45916dabce7` |
| `registry-B8eQDFB4.js` | `25f3ef82756d85281ad5c25375a5cd2f405989a1145ed438de05992e8c995376` |
| `runtime-registry-loader-Duw3fvRO.js` | `bd6a9f363bc7aac2fb0503640e339ffce52e0eab15336e6489b6f8129df748fb` |
| `runtime-D0xGMZdc.js` | `a050a101e3c352345179b77f8c304da99596238fcde95cf03319ebc11dea8791` |
| `discovery-7zi_zNvu.js` | `5489a4b1086fed443cedf54efccc76a730960e8419bba4d97010c3420a342ddd` |
| `manifest-registry--UiRn6nq.js` | `819c76c314e6ed1fd39c5ed6b169d63997905b3ae8a98b9373783d626431ace4` |
| `status-C_8oCXNB.js` | `f93a43546c7a59cf6f86f701fac887bde2924fefa2f65486847450fe44b05db1` |

## Exact source observability map

Line ranges below are from the exact hashed installed modules above.

| Boundary | Source range | Existing observability and actual meaning |
|---|---:|---|
| `loadOpenClawPlugins` cache path | `loader:1486-1527` | Cache lookup, restore, activation, and return exist as control flow; no built-in per-invocation log, ID, or hit/miss diagnostic was exposed. |
| Cache key/context | `loader:1028-1062`, `1190-1266` | Key construction is internal and includes normalized context, roots, discovery fingerprint, settings, install records, scope/mode, and activation inputs; no supported key/fingerprint projection was found. |
| Cache state | `loader:79-134`, `591-593`, `950-980` | Two process-global bounded LRU registry caches and compatibility reuse; cache contents and hit/miss state are private. |
| Cache restore | `loader:1508-1524` | Restores retained state, calls `activatePluginRegistry(cached.state.registry, ...)`, returns the cached registry; skips discovery, `createApi`, and `register(api)`. No built-in marker identifies this in production logs. |
| New-registry completion | `loader:1527-1529`, `2327-2344` | Miss path clears/loads/registers, captures state, activates, and finishes; no invocation counter or activation event is emitted to a supported production surface. |
| Active-registry compatibility | `loader:1291-1379` | Internal compatibility checks can reuse the active registry or call the loader; no registry identity/version/key diagnostic is exposed. |
| Scope short circuit | `runtime-registry-loader-Duw3fvRO.js:69-117` | `activeRegistrySatisfiesScope` can return without invoking the loader; no supported lifecycle marker identifies the return. |
| Activation/replacement | `loader:1482-1484`; `runtime-D0xGMZdc.js:626-640` | `setActivePluginRegistry` unconditionally assigns the active pointer; retirement is conditional cleanup only. No activation/replacement log or registry identity is exposed. |
| Registry retirement/clear | `loader:627-645`; `runtime:635-639` | Cache/runtime clear and conditional retirement exist; no production diagnostic identifies the retired object or reason. |
| Plugin registration/API | `loader:1988-1999`, `2237-2242`; plugin source/artifact ranges in CNX-400 | `createApi` and `register(api)` are source-level paths. The production plugin emits its own `hook-registered` event after its `api.on` calls, but this is not host acceptance evidence. |
| Typed hook gate/storage | `registry:4180-4255`, API closure around `registry:4776` | Policy rejection/acceptance and `typedHooks.push` are internal. No PID-correlated accepted-hook snapshot or host diagnostic was present. |
| Supported status projection | `status:192-210` and CLI metadata path `loader:2346-2673` | Status can be cache-disabled when `loadModules=true`; metadata/inventory can be persisted/derived. It does not expose live private registry identity or loader lifecycle. |

No source-defined production marker was found for loader invocation ID/count, cache hit/miss, cache key, registry identity, activation/replacement, `createApi` reachability, or typed-hook acceptance. Existing diagnostics arrays are registry/status projections, not a lifecycle trace.

## Production log evidence and timestamps

The available production chronology for PID 27372 is:

| Timestamp | Exact event/message | PID correlation | Proves | Does not prove |
|---|---|---|---|---|
| `05:13:48` | Process creation for OpenClaw gateway PID `27372` | Direct process query | The gateway process and command line existed. | Which loader invocation or registry object was used. |
| startup window | Config load and discovery activity | Prior bounded production log evidence; no loader ID | Startup/discovery-labelled activity occurred. | Cache miss, candidate identity, registry identity, or `createApi`. |
| `05:13:58.242` | `CogentNexus-OpenClaw delivery-observe {"event":"hook-registered","registrationCount":1,"hasReplyDispatch":true,"hasReplyPayloadSending":true}` | Prior production log evidence for the PID window | The plugin-side event path ran; CNX-400 source maps it to `register(api)` after plugin `api.on` calls. | Host acceptance of `before_agent_run`, cache miss, registry identity, or activation. |
| `05:13:59.061` | `HTTP server listening`; includes `cogentnexus-openclaw`; `3.9s` | Same startup window | Server listening and plugin presence in the listening summary. | Which registry object supplied the summary or typed-hook state. |
| `05:14:00.265` | `gateway ready` | Same startup window | Gateway readiness. | Cache/registry lifecycle. |
| later startup/prewarm-labelled phase | Discovery/prewarm-labelled activity | Same production chronology | A later labelled activity was logged. | Whether it was a cache hit, cache miss, active-registry short circuit, or another caller. |
| `05:14:10.542` | second plugin-side `hook-registered`, `registrationCount`: `2` | Same production window | A second execution of the plugin-side event path. | A distinct loader invocation, cache decision, registry identity, activation ordering, or host acceptance. |

No exact source-defined cache/loader/activation marker was found in the production window. Timestamp proximity is deliberately not used as registry identity evidence. The local `gateway-restart.log` contains only older August restart records and is not evidence for PID 27372; `config-audit.jsonl` contains historical config-write records but no loader/cache/registry telemetry for PID 27372.

## Supported diagnostics and negative findings

The supported read-only command `openclaw plugins list --json` completed with exit code `0`. Its CogentNexus record was:

- `registry.source`: `persisted`
- `registry.diagnostics`: `[]`
- `id`: `cogentnexus-openclaw`
- `source`: `...\\extensions\\cogentnexus-openclaw\\dist\\v091-release-entry.js`
- `rootDir`: `...\\extensions\\cogentnexus-openclaw`
- `origin`: `global`
- `enabled`: `true`
- `status`: `loaded`
- `hookNames`: `[]`
- `hookCount`: `0`

This is useful projection evidence and confirms the corrected selected artifact path. It is not a live active-registry identity, cache record, invocation trace, or host acceptance result. The exact status/CLI source paths show why it cannot answer those private lifecycle questions.

No supported read-only surface exposed:

- loader invocation ID or count;
- cache hit/miss;
- cache key/fingerprint;
- active registry identity/version/key;
- activation/replacement/retirement order;
- `createApi` reachability for PID 27372;
- accepted typed-hook names/count from the live Gateway registry;
- a plugin registration outcome joined to a registry identity.

No command was run that forces production plugin load/register. No production restart, reload, retry, semantic request, or instrumentation was performed.

## PID and process/environment provenance

Direct read-only process inspection returned PID `27372`, executable `node.exe`, command line shown above, and creation time `2026-09-17 05:13:48`. The Gateway endpoint is `127.0.0.1:18789`. The runtime command line contains no explicit `--config` or state selector. Existing environment selectors were inspected without mutation; no permitted observation exposes the already-running process's private normalized config or module object graph. The supported plugin projection names the global root and corrected release entry but does not bind those values to a historical loader invocation identity.

## Cache/registry correlation result

The production evidence can establish only this bounded sequence:

`PID 27372 startup -> plugin-side hook-registered at 05:13:58.242 -> server listening -> gateway ready -> later labelled activity -> plugin-side hook-registered at 05:14:10.542`

The following required distinctions remain unavailable:

| Candidate sequence | Production result |
|---|---|
| `register(api) -> registry A -> activate A -> later activate B` | Not directly observed; no registry identity or activation ordering. |
| `cache hit -> activate retained B -> no register(api)` | Source-supported mechanism, not observed in PID 27372. |
| `active-registry short circuit -> no loader/register` | Source-supported mechanism, not observed in PID 27372. |
| cache miss/new registry and fresh registration | Compatible with each plugin-side event, but not proven by a cache decision or loader ID. |

The two plugin-side events exclude a pure cache-hit explanation for those event lines because exact plugin source emits them only after `register(api)` executes. They do not exclude a silent cache restore or active-registry short circuit at another time, and they do not prove that `before_agent_run` was accepted into the final active registry.

## Relation to CNX-401, CNX-403, and missing `before_agent_run`

CNX-401 source evidence remains valid: activation swaps the complete registry object; it does not merge `typedHooks`; a cached registry can be activated without fresh `register(api)`; and active-registry scope reuse can bypass loading. CNX-404 adds fresh production-boundary evidence that these mechanisms still have no existing PID-correlated observability in the installed build.

CNX-403 directly observed one supported manifest-selected global root and no second same-ID candidate, but did not expose the historical live candidate array. CNX-404 does not convert that projection into registry identity or prove a cache event. The corrected release artifact remains the only reconciled selected identity; the dashboard artifact remains alternate/unselected/unproven.

For the missing `before_agent_run` state, the evidence narrows the possibilities but does not select one: (a) an unobserved incomplete retained/active registry, (b) a registration path reaching the host gate but being rejected before `typedHooks.push`, or (c) another unobserved loader/association lifecycle difference. The final missing-hook state cannot be causally attributed to cache restoration or registry replacement from available production evidence.

## Direct evidence versus inference

**Direct:** live GitHub starting SHA; exact process provenance; exact artifact and installed-module hashes; source line mappings; supported inventory output; two timestamped plugin-side events; server-listening/readiness chronology; and source semantics for cache restore, active-registry reuse, activation, replacement, retirement, and typed-hook storage.

**Inference/mechanism only:** cache-hit restore can suppress later registration; active-registry reuse can bypass the loader; activation can replace a registry lacking a hook; and a later silent lifecycle could leave the final registry without `before_agent_run`. None is claimed as a historical PID-27372 event.

## Hard-fence counts

- Semantic/model/provider/Dashboard requests: `0`
- Production mutations: `0`
- Gateway restart/reload: `0`
- Production config mutation: `0`
- Environment mutation: `0`
- Scheduled Task mutation: `0`
- Global extension installation/mutation: `0`
- Artifact replacement/deploy/rename/copy-over: `0`
- OpenClaw dependency patch: `0`
- CogentNexus source repair/rebuild: `0`
- Debugger/inspector attachment: `0`
- Production retry: `0`
- Permanent/committed instrumentation: `0`
- TicketStore/admission/routing/auth changes: `0`
- Historical CNX-360 through CNX-403 edits: `0`
- Release/tag/main changes: `0`
- Force-push/history rewrite: `0`
- CNX-405 created/started: `0`

## Closeout evidence

After publication, only this report and the requested status tokens were changed. Final verification recorded:

- authoritative final HEAD after final publication commit: `f6a69939808d2c2478695ca666a6167599d67d3a`;
- `ACTIVE.md`: `WAITING_FOR_CHATGPT_REVIEW`;
- `STATUS.md`: `WAITING_FOR_CHATGPT_REVIEW`;
- no historical CNX-360 through CNX-403 report changed;
- no CNX-405 created or started;
- clean worktree and exact changed paths verified before stop.
