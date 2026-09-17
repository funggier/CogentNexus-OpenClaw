# CNX-20260917-399 — Global Loader Invocation and Cache Provenance Trace Report

## Classification

`LOADER_INVOCATION_CACHE_REUSE_PROVEN`

Exact installed OpenClaw source proves process-global bounded LRU registry caches keyed by a comprehensive load-context key. A cache hit returns the prior registry and restores retained registration state without rediscovering candidates or invoking `register(api)` again. The source therefore proves a concrete mechanism that can affect this registration boundary. It does not prove that this mechanism caused the production missing hook.

## Authority and identity

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Task: `CNX-20260917-399`
- Parent: `CNX-20260917-398`
- Exact authoritative starting local HEAD: `7331a720b455c5233925bc636e7087f41afdcc7b`
- Exact authoritative starting remote HEAD at start: `7331a720b455c5233925bc636e7087f41afdcc7b`
- Embedded expected baseline: `7331a720b455c5233925bc636e7087f41afdcc7b` (matched live GitHub)
- Starting coordination gate read from checkout: `WAITING_FOR_CHATGPT_REVIEW` for CNX-397; CNX-399 task authority was then read from the live branch.

GitHub was fetched first with an explicit branch refspec. `git ls-remote` matched the checked-out HEAD before investigation. ACTIVE, STATUS, this task, CNX-398, and CNX-397 through CNX-391 were read. No historical report was edited.

## Exact installed runtime and module hashes

- OpenClaw: `2026.7.1-2 (0790d9f)`
- Effective production artifact: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
- Effective artifact SHA-256: `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- Installed module root inspected: `C:\Users\CDQ-P\.openclaw\workspace\test\CogentNexus-OpenClaw\plugins\cogentnexus-openclaw\node_modules\openclaw`

| Module | SHA-256 |
|---|---|
| `dist/loader-D8d2EvVh.js` | `3a10479bdcbb713692c3ded7dbd5baad27c1b17ae3566172c117d45916dabce7` |
| `dist/discovery-7zi_zNvu.js` | `5489a4b1086fed443cedf54efccc76a730960e8419bba4d97010c3420a342ddd` |
| `dist/registry-B8eQDFB4.js` | `25f3ef82756d85281ad5c25375a5cd2f405989a1145ed438de05992e8c995376` |
| `dist/config-state-CtMlHVRM.js` | `af2e3bc003048755d820284d3e01a777fae907aff3be8bc4e281dee663f409c5` |

## Loader entry points and lifecycle mapping

All line ranges below are from the exact hashed installed modules.

| Caller | Lines | Inputs and behavior | Retention/reuse conclusion |
|---|---:|---|---|
| `loadOpenClawPlugins` | `loader:1486-1527`, `1599-1640` | Builds `resolvePluginLoadCacheContext(options)`, normalizes config, activation source, install records, then discovers with `workspaceDir`, `normalized.loadPaths`, `env`, `installRecords`; can accept supplied discovery/manifest registry. | Cache-enabled runtime path checks the process-global cache before discovery. Hit returns prior registry; miss constructs a new registry and discovers. |
| Gateway load caller | `server-plugins-XoQmHCe9.js:489-531` | Sends resolved config, activation-source config, workspace, scoped plugin IDs, gateway-bindable runtime options, built-artifact preference, and optional manifest registry. | Gateway startup/reload callers can receive a retained compatible active registry through loader cache/active-registry matching. |
| Runtime registry ensure | `runtime-registry-loader-Duw3fvRO.js:61-114` | `ensurePluginRegistryLoaded` computes scope and context, reuses active registry when scope/workspace/IDs satisfy, otherwise calls `loadOpenClawPlugins`; module-global `pluginRegistryLoaded` tracks scope. | This is an additional lifecycle short circuit. It can skip a loader call when the active registry satisfies the requested scope. |
| Status inventory | `status-C_8oCXNB.js:192-210` | When `loadModules` is true, calls loader with `activate:false, cache:false`; otherwise uses metadata snapshot. | Status load is explicitly cache-disabled. Metadata-only status is not live loader state. |
| Middleware fallback | `agent-tool-result-middleware-loader-BsZPH_qG.js:89-106` | Reuses a loaded runtime registry if it contains required middleware; otherwise calls loader with scoped IDs, `activate:false`, and `forceFullRuntimeForChannelPlugins:true`. | Reuse is conditional on active registry contents; fallback invocation is explicitly not shown with `cache:false`, so loader cache can apply. |
| CLI command registry | `cli-registry-loader-C9ID-m75.js:134-143` | Calls runtime loader with `activate:false, cache:false`, scoped IDs, and full-runtime preference. | Explicitly bypasses plugin registry cache and does not activate live state. |
| CLI metadata registry | `loader:2346-2375` | Builds a fresh registry and performs discovery/manifest construction itself with activation disabled. | Separate projection path; not the live Gateway registry. |

The source does not expose a separate named “prewarm” caller in the inspected module map. The runtime ensure path and Gateway load path are the relevant reusable lifecycle boundaries; production log labels such as prewarm/discovery cannot identify which caller ran without a loader lifecycle counter or PID-correlated trace.

## Cache and context lifetime

### Loader registry cache

`loader-D8d2EvVh.js:79-134` defines `PluginLoaderCacheState`. Each instance owns a `PluginLruCache`, an in-flight `Set`, and an open-allowlist warning `Set`. Two module-level instances are created at `:591-593`, each with maximum 128 entries: `pluginLoaderCacheState` for scoped loads and `fullWorkspacePluginLoaderCacheState` for full loads. They are process-global module state, not persisted and not invocation-local.

`getPluginRegistryCache` at `:950-951` selects the scoped cache when `onlyPluginIds` is present and the full-workspace cache otherwise. `getReusableCachedPluginRegistry` at `:959-980` first checks the exact key, then may reuse a gateway-bindable equivalent for default runtime-subagent mode.

The key is constructed at `:1028-1062`. It includes workspace/global/stock roots, bundled package identity (including package JSON size/mtime), discovery fingerprint, normalized plugin settings, install records, load paths, activation metadata hash, scope, setup/runtime mode, artifact preference, raw-env mode, module-load mode, discovery mode, runtime-subagent mode, SDK resolution, gateway method names, and activation mode. This is strong invalidation coverage, but it is key equality, not proof that every external file/config change is represented.

`loadOpenClawPlugins:1500-1525` enables this cache unless `cache:false` or raw-config-env resolution is requested. On a hit it restores retained commands, handlers, providers, memory state, then `activatePluginRegistry(cached.state.registry, ...)`; it returns without discovery, manifest construction, module loading, or `register(api)`. On a miss it begins in-flight tracking at `:1527`, clears activated state at `:1529`, loads/discovers/registers, stores the registry and captured live registration state at `:2327-2339`, activates at `:2340`, and removes the in-flight marker at `:2342-2344`.

Invalidation is explicit: `clearPluginLoaderCache:627-631` clears both caches and activated runtime state; `clearPluginRegistryLoadCache:642-645` clears cached registries and warning memory only. LRU eviction also removes entries when capacity is exceeded. In-flight entries are deleted in `finishLoad`; reentry for the same key throws at `:121-126`. No persisted registry cache was found.

### Normalized config and activation source

`resolvePluginLoadCacheContext:1190-1266` reads the current `options.config`/activation-source inputs, resolves environment values when requested, applies defaults, creates `normalized` at `:1201`, creates activation source at `:1202`, merges trust lists, reads installed-index install records at `:1216-1219`, and computes the cache key. The normalized object and activation-source snapshot are newly constructed on every call to this function. They are not themselves cached across calls.

However, on a cache hit those new objects are not used to rebuild the registry: the prior registry and retained registration state win. Thus stale normalized behavior can occur indirectly when a later invocation produces the same cache key despite an externally changed input not represented by that key. Explicit config/plugin fields and activation metadata are substantially represented; arbitrary plugin-config payload is deliberately redacted from the key in raw-env mode only (`:1091-1100`), while raw-env mode disables the registry cache (`:1500`). This supports “possible key-equivalent reuse,” not a claim that the target production config was stale.

### Discovery, manifest, candidate, and provenance state

Within a cache miss, discovery is invocation-local: `:1603-1612` uses a supplied manifest registry, supplied discovery, or calls `discoverOpenClawPlugins`; `:1613-1620` creates/loads the manifest registry; `:1640` creates a new `manifestByRoot = new Map(...)`; candidate ordering and `seenIds` are inside the invocation. No process-global discovery memoization or manifest-map cache was found in the exact loader path.

`createPluginCandidatesFromManifestRegistry:615-625` is a projection of a caller-supplied manifest registry, not a persistent cache. The discovery module is imported once by Node module caching, but its returned candidate collection is rebuilt on each loader miss unless the caller supplies one. The installed-index reader at `:1216-1219` supplies install records to context/discovery/provenance; source does not show installed-index plugin records being used as the live registry or as a retained candidate list.

### Active registry and scope short circuit

`setActivePluginRegistry`/`getActivePluginRegistry` are process-local runtime state imported from `runtime-D0xGMZdc.js`. The loader sets the active registry at `:1482-1484` and `:2340`; `getCompatibleActivePluginRegistry:1291-1360` can return it when cache keys, scopes, workspace, and runtime mode are compatible. `runtime-registry-loader:12-18,87-114` also retains a module-global scope rank and can return without loading when the active registry satisfies the requested scope. A later load with a different key can replace active state through `activatePluginRegistry`; the old cached registry may remain in the LRU until eviction/clear.

## Causal consequence for registration

The causal path is direct:

`cache key hit` → `cached.state.registry` + restored retained registrations → return from loader → no discovery/manifest lookup → no candidate loop → no `createApi` → no `register(api)` → no new `api.on("before_agent_run")`.

The retained state includes the registry object and registration side effects captured at `:2327-2339`; restoration is explicit at `:1509-1522`. The exact host gate remains `registry-B8eQDFB4.js:4225-4235`, with accepted typed hooks stored at `:4251-4255` as established by CNX-391. Therefore cache reuse can preserve a prior missing-hook registry or preserve a prior accepted-hook registry; it does not independently explain why the first cached registry lacked the hook.

The active-registry scope short circuit has the same boundary effect: it can skip a later loader call and therefore skip duplicate registration. Duplicate suppression inside one invocation is a separate `seenIds` mechanism from CNX-397; no cross-invocation duplicate-ID map was found.

## Production chronology and observability

Prior production evidence records process creation, configuration/discovery activity, plugin-side repeated `hook-registered`, server listening/readiness, and a later discovery/prewarm-labelled phase, but does not include loader cache key, cache hit/miss, invocation ID, registry identity, `createApi` reachability, or host typed-hook acceptance. The source supports distinct loader invocations and reuse/short-circuit possibilities, but timestamps alone cannot distinguish:

- a cache miss with fresh discovery;
- a cache hit restoring a prior registry;
- active-registry scope reuse;
- a new registry replacing the active registry; or
- repeated plugin-side logging from a separate plugin-side lifecycle unrelated to host registration.

Exact gap: production telemetry lacks PID-correlated `loadOpenClawPlugins` invocation counters, cache key/hash and hit/miss outcome, normalized-config identity/fingerprint, candidate/manifest selection, registry identity/replacement, `createApi` entry, and host `registerTypedHook` acceptance. No safe supported command was found that exposes those loader-local values. Existing inventory remains an installed-index/derived projection and cannot close this gap.

## Installed index versus live loader

The installed index is read by `loadInstalledPluginIndexInstallRecordsSync` for install records/context (`loader:1216-1219`) and is passed into discovery/provenance (`:1607-1619`). It contributes installation path/source metadata and cache-key inputs; it is not itself returned as a live registry and no source path was found that rehydrates its plugin record into typed-hook registration. `plugins list --json`/status may use metadata snapshots or cache-disabled status loading (`status:192-210`), so it is not proof of live loader state. A stale index could affect candidate provenance/ordering inputs if its install records are selected, but this report found no direct path from an index row to `register(api)` other than those indirect discovery/provenance inputs.

## Disposable probe status

No probe was run. The exact public loader export permits invocation, but a safe two-call probe requires an isolated plugin fixture and observation of private registry identity/registration boundaries. The task forbids patching OpenClaw, monkey-patching dependencies, and fabricating global-origin discovery; the available supported API does not expose cache contents, candidate injection, or host registry identity directly. Running an uninstrumented call would not prove the required identities or hook suppression. Classified as not safely probative, not as a runtime result.

## Boundary answers

1. **Share/reuse:** Yes. Process-global LRU registries and active-registry compatibility/scope reuse can span Gateway lifecycle calls.
2. **Normalized config:** The normalized object is freshly constructed per context call, but a cache hit bypasses its use; key-equivalent reuse can therefore retain prior effective state. Direct object reuse across invocations was not proven.
3. **Candidate/manifest/discovery:** No process-global candidate/manifest memoization was found in the loader miss path. They are rebuilt per miss, or caller-supplied snapshots are consumed. A cache hit skips them entirely.
4. **Registry retention/replacement:** Cached registry objects are retained in two bounded process-global LRUs; active registry is replaced on activation of a new load and can be restored from cache. Scope state can short-circuit a load.
5. **Registration suppression:** Yes. Cache hit or active-registry short circuit skips `createApi`, `register(api)`, and `api.on` for that invocation. This is causal to whether a later registration occurs, but does not identify the origin of the production missing hook.
6. **Production narrowing:** The missing-hook explanation is materially narrowed from “unknown repeated load behavior” to a concrete retained-registry/skip boundary. Production causality remains inconclusive because the required cache-hit/registry identity telemetry is absent.

## Direct evidence versus inference

**Direct:** exact GitHub starting SHA; exact installed module hashes; module-level cache construction; cache-key construction; cache hit/restore/return; miss discovery and manifest construction; cache invalidation; active-registry and scope short circuits; Gateway/status/CLI callers; installed-index input path; and the `createApi`/typed-hook path inherited from the exact installed source and predecessor reports.

**Inference:** cache reuse could preserve a prior registry and suppress later registration; a changed input not represented in the cache key could remain stale. No production cache hit, stale key, or registry identity was observed.

## Counts and hard-fence compliance

- Semantic/model/provider/Dashboard requests: `0`
- Production mutations: `0`
- Gateway restart/reload: `0`
- Production config/environment/Scheduled Task mutation: `0`
- Production global extension/artifact mutation/deploy: `0`
- OpenClaw dependency patch: `0`
- CogentNexus source repair/rebuild: `0`
- Debugger/inspector attachment: `0`
- Permanent/committed instrumentation: `0`
- TicketStore/admission/routing/auth changes: `0`
- Historical CNX-360 through CNX-398 edits: `0`
- Force-push/history rewrite/release/tag/main changes: `0`
- CNX-400 created/started: `0`

## Closeout

Report publication is followed by ACTIVE.md and STATUS.md set to `WAITING_FOR_CHATGPT_REVIEW`. No production state was changed. Final local/remote equality, changed paths, and clean-worktree state must be recorded after the publication commit; execution stops and no CNX-400 is created or started.
