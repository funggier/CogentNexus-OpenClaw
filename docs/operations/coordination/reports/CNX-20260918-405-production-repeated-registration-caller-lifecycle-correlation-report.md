# CNX-20260918-405 — Production Repeated Registration Caller and Lifecycle Correlation Report

## Classification

`PRODUCTION_REGISTRY_LIFECYCLE_PATH_MAPPED`

The exact installed OpenClaw build maps the relevant Gateway, runtime-ensure, middleware fallback, channel bootstrap, standalone-registry, and selected-runtime callers. The source fully explains how one Gateway process can execute multiple plugin registration lifecycles without duplicate filesystem roots, and how a later cached activation can replace the active registry without a new plugin-side registration event. Production logs provide plugin-side registration events and broad startup/prewarm chronology, but no caller-specific marker binds either event to a concrete caller or registry identity.

## Authority and identity

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Task: `CNX-20260918-405`
- Parent: `CNX-20260918-404`
- Embedded expected starting SHA: `988563fd5bb34623c00c5d4d2eba9b6f73e33168` (not assumed)
- Authoritative starting GitHub HEAD after explicit fetch: `be58edac3c3e12b908dc3f468ce06f9290be68e9`
- Local starting HEAD: `be58edac3c3e12b908dc3f468ce06f9290be68e9`
- Starting gate: `READY_FOR_HERMES`

The remote branch was fetched with an explicit refspec and `git ls-remote` matched the checked-out starting HEAD. The remote contained the CNX-405 task and changed ACTIVE/STATUS records; no stale CNX-404 state was used.

## Exact runtime, artifact, and module hashes

- OpenClaw: `2026.7.1-2 (0790d9f)`
- Production Gateway PID: `27372`
- Endpoint: `127.0.0.1:18789`
- Executable: `C:\Program Files\nodejs\node.exe`
- Command line: `"C:\Program Files\nodejs\node.exe" C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw\dist\index.js gateway --port 18789`
- Process creation: `2026-09-17 05:13:48`
- Selected artifact: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
- Selected artifact SHA-256: `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- Alternate unselected artifact: `v091-dashboard-verified-delivery.js`, SHA-256 `1276bd624b62f96692eaa19f493f69e422771b6994b39ded94b2bcb3399e1f98`
- Installed module root: `C:\Users\CDQ-P\.openclaw\workspace\test\CogentNexus-OpenClaw\plugins\cogentnexus-openclaw\node_modules\openclaw\dist`

| Module | SHA-256 |
|---|---|
| `loader-D8d2EvVh.js` | `3a10479bdcbb713692c3ded7dbd5baad27c1b17ae3566172c117d45916dabce7` |
| `runtime-registry-loader-Duw3fvRO.js` | `bd6a9f363bc7aac2fb0503640e339ffce52e0eab15336e6489b6f8129df748fb` |
| `runtime-D0xGMZdc.js` | `a050a101e3c352345179b77f8c304da99596238fcde95cf03319ebc11dea8791` |
| `registry-B8eQDFB4.js` | `25f3ef82756d85281ad5c25375a5cd2f405989a1145ed438de05992e8c995376` |
| `server-plugins-XoQmHCe9.js` | `5f9842ae09566a1d9aa57ea12f2132cfd843301d1323ca58d9d251d18eefc50b` |
| `server-startup-plugins-CaPrk84k.js` | `8b70e55b14e975707054ae2a0c96cdddd4f42d75d9a38ac570b7da6a1693ccf6` |
| `standalone-runtime-registry-loader-DHlUPKIt.js` | `a46a6acf013b5d92949d09484e4930545d655619e5cb3800de3622b98a2bb515` |
| `agent-tool-result-middleware-loader-BsZPH_qG.js` | `c3251ae8852c2739b1e7dd41c7f978349499075ed0a5a51fbc4089db73c3dbc2` |
| `runtime-plugin-BLmQLMt1.js` | `7b9b1295bf3c961733677869fcc688ffc57866b9e31cb786b3bc53ffb36f719c` |
| `channel-bootstrap.runtime-CDufwYqZ.js` | `a0abc25c12cbee13565e51e54caf3a6338fe0774f1874f6491f9c791618cd564` |

## Exact caller and lifecycle graph

### Gateway startup / primary production load

`server-plugins-XoQmHCe9.js:489-494` resolves startup plugin IDs from the lookup table. For non-empty IDs, `:514-531` calls `loadOpenClawPlugins` with the resolved config, activation source, workspace, scoped plugin IDs, Gateway runtime options, built-artifact preference, startup trace, and optional manifest registry. The caller then records `plugins.gateway-load` at `:536-551`, including `loaderCallsCount` and `loaderNativeHitsCount` statistics. These counters concern the native module loader statistics in this caller's startup trace; they are not OpenClaw plugin-registry cache hit/miss or registry identity telemetry.

If no plugin IDs exist, `server-plugins:496-508` creates an empty registry, calls `setActivePluginRegistry` at `:499`, and emits the same `plugins.gateway-load` marker with zero counts. `server-startup-plugins-CaPrk84k.js:93-98` can also set an empty/selected active registry during startup setup, with the minimal-test-gateway branch selecting the current active registry or an empty registry.

### Runtime ensure / active scope reuse

`runtime-registry-loader-Duw3fvRO.js:61-67` calls `loadOpenClawPlugins` only when `getLoadedRuntimePluginRegistry` does not satisfy the requested scope. `:69-113` implements `ensurePluginRegistryLoaded`:

- `:87-89`: returns when the module-global loaded scope and active registry satisfy the request;
- `:90-93`: returns when the active registry satisfies scope even though the loaded marker is `none` or a scoped load is requested;
- `:102-112`: otherwise builds scoped load options and reaches `loadOpenClawPlugins` through `resolveOrLoadRuntimePluginRegistry`;
- `:113`: records only the internal scope marker.

These reuse returns do not invoke `register(api)`. A later call with a different scope or unsatisfied active registry can invoke the loader and potentially register again.

### Gateway outbound-channel bootstrap

`channel-bootstrap.runtime-CDufwYqZ.js:25-48` is an on-demand runtime caller. If a selected channel cannot resolve a send-capable implementation, it deduplicates attempts using a key composed of active channel-registry version, active registry version, and channel (`:30-32`), then calls `resolveRuntimePluginRegistry` at `:36-43`. This can reach the loader after startup if the active registry does not satisfy the channel. The source does not emit a caller-specific production marker identifying the resulting loader/cache path.

### Selected agent-harness runtime

`runtime-plugin-BLmQLMt1.js:91-138` resolves a non-default selected runtime, computes its owning plugin IDs and memory plugin IDs, then calls `ensurePluginRegistryLoaded` with `scope: "all"` and an explicit plugin scope at `:129-137`. This is a separate runtime-ensure path that can trigger a scoped loader call when the active registry lacks the selected runtime plugins. No evidence binds it to PID 27372's observed timestamps.

### Tool-result middleware fallback

`agent-tool-result-middleware-loader-BsZPH_qG.js:84-106` first checks active middleware owners and `getLoadedRuntimePluginRegistry`. If required owners are missing, it calls `loadOpenClawPlugins` directly with `activate:false` and a scoped plugin list at `:98-106`. This path can load plugin code and execute registration for a missing scoped registry while deliberately not activating the resulting registry. It therefore can create a registration event without being the active-registry replacement path. No production caller marker identifies this path.

### Standalone registry loader

`standalone-runtime-registry-loader-DHlUPKIt.js:10-14` installs a supplied registry by calling `setActivePluginRegistry`. `:32-38` calls `loadOpenClawPlugins`, optionally forcing `cache:false`; the subsequent installation path can activate the result. This is a mechanism-capable replacement path, but no production evidence shows this standalone surface was used by PID 27372.

### CLI and non-production/diagnostic callers

`command-execution-startup-B1zeYC9U.js:13-21`, `register.message-TVdqEQ0c.js:191-195`, and the CLI/plugin-registry exports call `ensurePluginRegistryLoaded` for command execution. `status-C_8oCXNB.js:192-210` and CLI registry paths use cache-disabled or metadata-specific behavior. These surfaces explain why `plugins list --json` is not proof of Gateway live-registry identity and were not treated as production caller evidence.

## Activation lineage

`loader-D8d2EvVh.js:1482-1484` defines `activatePluginRegistry` as `setActivePluginRegistry` followed by hook-runner initialization.

- Empty Gateway plugin scope: `loader:1492` can activate a new empty registry.
- Cache hit: `loader:1508-1524` restores retained state, activates `cached.state.registry` at `:1522`, and returns without discovery, `createApi`, or `register(api)`.
- Cache miss: `loader:1527-1529` begins a new load; after discovery/registration and retained-state capture, `:2340` activates the new registry.
- Gateway load: `server-plugins:499` can directly activate an empty registry; the normal path activates through `loadOpenClawPlugins`.
- Standalone install: `standalone-runtime-registry-loader:11` calls `setActivePluginRegistry` directly for an existing/supplied registry.
- Active reuse: `runtime-registry-loader:87-93` returns without activation when scope is already satisfied.

`runtime-D0xGMZdc.js:626-640` unconditionally assigns the supplied registry to the active pointer. Retirement of the previous object at `:635-639` is separate conditional cleanup. Therefore a later cache-hit activation or another non-short-circuited lifecycle can replace the active registry after an earlier successful `register(api)` without another visible plugin-side registration event.

## Registration multiplicity

The exact source supports these one-process sequences without duplicate filesystem roots:

1. Gateway startup load miss → CogentNexus `register(api)` → registry A activated.
2. Later scoped runtime ensure with unsatisfied scope → second loader miss → `register(api)` again → registry B activated.
3. Gateway startup registration → later cache hit → retained registry B activated without `register(api)`.
4. Active-registry scope short circuit → no loader/register; later different scope → loader/register or cache activation.
5. Startup/plugin load or channel bootstrap → middleware fallback with `activate:false` → additional plugin registration path without replacing the active pointer.
6. Standalone runtime install → direct active-pointer replacement of an existing registry.

A pure cache hit or active-registry short circuit cannot produce `hook-registered`, because both return before plugin registration. The two observed plugin-side events therefore prove two executions of the plugin event path, but not two distinct OpenClaw callers, two cache misses, or two accepted `before_agent_run` hooks.

## Production chronology correlation

The read-only PID/process evidence remains:

| Timestamp | Production evidence | Caller correlation |
|---|---|---|
| `05:13:48` | PID `27372` Gateway process created | Direct process provenance only. |
| startup window | Config load and discovery activity | No caller-specific loader marker. |
| `05:13:58.242` | Plugin-side `hook-registered`, registration count `1` | Proves plugin registration path reached its event logger; caller identity unbound. |
| `05:13:59.061` | HTTP server listening; includes CogentNexus | No registry identity or caller marker. |
| `05:14:00.265` | `gateway ready` | No loader/activation marker. |
| later | Discovery/prewarm-labelled activity | No source-defined marker sufficient to distinguish Gateway load, runtime ensure, channel bootstrap, or another path. |
| `05:14:10.542` | Plugin-side `hook-registered`, registration count `2` | Proves a second plugin registration event path; caller identity and registry identity unbound. |

The source-defined `plugins.gateway-load` startup trace would be useful if present, because it contains `loaderCallsCount` and related fields at `server-plugins:536-551`. The inspected production chronology does not provide a PID-correlated instance of that marker. No source-defined marker was found that identifies `ensurePluginRegistryLoaded`, `resolveRuntimePluginRegistry`, cache hit/miss, registry identity, or activation ordering in the relevant log window.

It is therefore not valid to assign the first event to Gateway startup and the second to prewarm/runtime ensure solely from timestamp adjacency. That sequence is mechanically plausible, not production-proven.

## Relation to CNX-401, CNX-403, and CNX-404

- **CNX-401:** The caller graph strengthens the mechanism hypothesis. Multiple exact callers can reach fresh loads, scoped reuse, cache restore, or activation/replacement in one process. A later cached activation can replace the active registry without fresh registration.
- **CNX-403:** The graph does not require a second filesystem candidate to explain repeated registration. A second same-ID root remains unobserved and is not needed for the source-supported repeated-lifecycle model.
- **CNX-404:** CNX-405 maps the previously unresolved caller/lifecycle boundary, but production caller identity, cache decision, registry identity, and activation ordering remain unobserved. The classification remains a source/lifecycle mapping, not production causal proof.

## Missing `before_agent_run` impact

The remaining production explanation is materially narrowed from “duplicate root is required” to a lifecycle set that includes repeated fresh registration, scoped loader fallback, silent cache restoration, active-registry reuse, and later registry replacement. However, no available evidence proves which path occurred in PID 27372 or whether the host typed-hook gate accepted either registration. The final missing `before_agent_run` state remains causally unresolved between incomplete registry state, host policy rejection before `typedHooks.push`, and an unobserved lifecycle/association difference.

## Direct evidence versus inference

**Direct:** authoritative starting SHA; exact module hashes; exact call sites and line ranges; live PID/executable/command line; selected artifact hash; source-defined startup trace fields; two plugin-side event timestamps; and source semantics for cache, ensure, fallback, activation, and replacement.

**Inference/mechanism:** one process can execute multiple registration lifecycles without duplicate roots; Gateway startup plus later scoped/runtime callers are mechanically capable of producing the observed multiplicity; and later cache activation can silently replace the active registry. No concrete production caller or registry sequence is claimed.

## Production-local evidence still unavailable

- PID-correlated `plugins.gateway-load` trace instance;
- loader invocation ID/count for the plugin-registry loader;
- caller identity for each registration event;
- cache hit/miss and cache-key fingerprint;
- active registry identity/version/key;
- activation/replacement ordering;
- `createApi` reachability and registration record identity;
- host typed-hook acceptance and final live `typedHooks` contents.

## Hard-fence counts

- Semantic/model/provider/Dashboard requests: `0`
- Production mutations: `0`
- Gateway restart/reload: `0`
- Production config/environment/Scheduled Task mutation: `0`
- Production global extension/artifact mutation/deploy: `0`
- OpenClaw dependency patch: `0`
- CogentNexus source repair/rebuild: `0`
- Debugger/inspector attachment: `0`
- Production retry: `0`
- Permanent/committed instrumentation: `0`
- TicketStore/admission/routing/auth changes: `0`
- Historical CNX-360 through CNX-404 edits: `0`
- Release/tag/main changes: `0`
- Force-push/history rewrite: `0`
- CNX-406 created/started: `0`

## Closeout

The report is the only new report artifact authorized for publication. ACTIVE.md and STATUS.md will be set to `WAITING_FOR_CHATGPT_REVIEW` after publication. No CNX-406 will be created or started. Final authoritative HEAD, remote equality, changed paths, report blob, and clean-worktree state will be verified after the final push.
