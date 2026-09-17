# CNX-20260918-401 — Registry Activation and Replacement Lineage Trace Report

## Classification

`REGISTRY_REPLACEMENT_MECHANISM_PROVEN`

Exact OpenClaw source proves that activation unconditionally assigns a new registry object to the process-local active-registry pointer. The same source proves that both a cache hit and a cache-miss completion can call that activation path, and that cache-hit activation does not call `createApi` or `register(api)`. Typed hooks live on the registry object (`typedHooks`) and are appended during `api.on()` acceptance; activation swaps the object and does not merge typed hooks. Therefore an active registry containing `before_agent_run` can be replaced by a registry that does not contain it, including by cache restoration without fresh plugin registration. This proves the mechanism, not its occurrence in production.

## Authority and exact identity

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Expected baseline supplied by task: `100de748f9cf10ab07276da8551f5654b986b0ea`
- Exact authoritative starting local HEAD: `100de748f9cf10ab07276da8551f5654b986b0ea`
- Exact authoritative starting GitHub HEAD: `100de748f9cf10ab07276da8551f5654b986b0ea`
- Starting gate: `READY_FOR_HERMES`
- Dedicated clean checkout: `C:\Users\CDQ-P\cnx401-work`

GitHub was fetched with an explicit branch refspec before investigation. The live `git ls-remote` value matched the checkout. ACTIVE, STATUS, CNX-401, CNX-400, CNX-399, and the requested CNX-398 through CNX-391 reports were read. The pre-existing checkout with unrelated untracked files was not used or modified.

## Exact OpenClaw/artifact identity

OpenClaw runtime: `2026.7.1-2 (0790d9f)`.

Installed module root inspected:
`C:\Users\CDQ-P\.openclaw\workspace\test\CogentNexus-OpenClaw\plugins\cogentnexus-openclaw\node_modules\openclaw\dist`

| Module | SHA-256 |
|---|---|
| `loader-D8d2EvVh.js` | `3a10479bdcbb713692c3ded7dbd5baad27c1b17ae3566172c117d45916dabce7` |
| `registry-B8eQDFB4.js` | `25f3ef82756d85281ad5c25375a5cd2f405989a1145ed438de05992e8c995376` |
| `runtime-registry-loader-Duw3fvRO.js` | `bd6a9f363bc7aac2fb0503640e339ffce52e0eab15336e6489b6f8129df748fb` |
| `runtime-D0xGMZdc.js` | `a050a101e3c352345179b77f8c304da99596238fcde95cf03319ebc11dea8791` |

Effective production artifact identity retained from the exact current read-only evidence context: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-dashboard-verified-delivery.js`, SHA-256 `1276bd624b62f96692eaa19f493f69e422771b6994b39ded94b2bcb3399e1f98`.

## Exact call graph and line mapping

```text
loadOpenClawPlugins(options)
  -> resolvePluginLoadCacheContext(options)
  -> cache lookup
     hit:
       restoreRegisteredAgentHarnesses / commands / providers / memory state
       -> activatePluginRegistry(cached.state.registry, ...): loader:1508-1524
          -> setActivePluginRegistry(registry, ...): runtime:626-640
          -> initializeGlobalHookRunner(registry): loader:1482-1484
       -> return cached.state.registry: loader:1524
     miss:
       -> clearActivatedPluginRuntimeState(): loader:1527-1529
       -> construct registry and discover/load/register plugins
       -> capture retained state: loader:2327-2339
       -> activatePluginRegistry(registry, ...): loader:2340
          -> setActivePluginRegistry(...): runtime:626-640
```

### Registry construction

`createEmptyPluginRegistry()` is in `runtime-D0xGMZdc.js:451-505`. It returns a fresh object with independent arrays, including `plugins`, `hooks`, `typedHooks`, `channels`, `providers`, `commands`, `interactiveHandlers`, `runtimeLifecycles`, `agentEventSubscriptions`, `sessionSchedulerJobs`, `conversationBindingResolvedHandlers`, and `diagnostics`. This is object creation, not a clone or merge.

The normal loader miss creates its invocation-local registry through the loader's registry construction path before the candidate/register loop. The exact miss completion is `loader-D8d2EvVh.js:2327-2340`: it captures the registry and then activates that same object. `manifestByRoot` and `seenIds` are also invocation-local maps (`loader:1640,1650`); no process-global manifest/candidate registry was found.

### Activation and pointer semantics

`activatePluginRegistry` is `loader-D8d2EvVh.js:1482-1484`:

```js
setActivePluginRegistry(registry, cacheKey, runtimeSubagentMode, workspaceDir);
initializeGlobalHookRunner(registry);
```

`setActivePluginRegistry` is `runtime-D0xGMZdc.js:626-640`. It first saves the old pointer, then unconditionally executes `state.activeRegistry = registry` at line 628 and marks the supplied object active. It updates active version, key, workspace, runtime mode, and tracked HTTP/channel/session-extension surfaces. The identity guard `previousRegistry === registry` only controls retirement cleanup; it does not prevent replacement. Thus `new → active` and `cached → active` are unconditional pointer replacement operations once activation is called.

`getActivePluginRegistry` is `runtime:642-644` and returns the current pointer. `getActivePluginRegistryKey` is `runtime:754-756`.

After replacement, the old object may remain reachable through the process-global LRU cache, unless evicted or cleared. `setActivePluginRegistry` conditionally retires/cleans the old object only when `retirePluginRegistryIfUnused(previousRegistry)` permits it (`runtime:635-639`). This cleanup condition is separate from active-pointer assignment and does not merge old hooks into the new object.

### Compatibility and scope short circuits

`getCompatibleActivePluginRegistry` is `loader-D8d2EvVh.js:1291-1360`. It may return the current active object when the cache key, scope, workspace, runtime mode, or gateway-bindable compatibility checks match. `resolveRuntimePluginRegistry` at `loader:1363-1379` returns that compatible object; otherwise it calls `loadOpenClawPlugins`.

`ensurePluginRegistryLoaded` is `runtime-registry-loader-Duw3fvRO.js:69-117`. Its scope-rank and `activeRegistrySatisfiesScope` checks at `:87-93` return without invoking the loader when the active registry satisfies the requested scope. These are reuse/skip paths, not replacement paths. If they do not match, the function calls the loader through `resolveOrLoadRuntimePluginRegistry` (`:60-67`, `:101-114`). A later non-short-circuited load can therefore activate a different object.

## Cache relationship and replacement cases

### Cache hit → active

`loader:1500-1524` enables cache unless `options.cache === false` or raw-config resolution is requested. On hit, the loader restores retained global side effects at `:1510-1521`, calls `activatePluginRegistry(cached.state.registry, ...)` at `:1522`, and returns that exact cached registry at `:1524`. No discovery, module load, `createApi`, or `register(api)` occurs on this path.

Therefore a cached registry can supersede the currently active registry without fresh registration. This can be `active A → cached B`, or `active B → cached A`; the cache entry is selected by key/compatibility, not by merging typed hooks.

### Cache miss → new active

The miss path begins at `loader:1527`, clears activated state when applicable, constructs/discovers/registers a new registry, captures state at `:2327-2339`, then activates the new registry at `:2340`. This is `active A → new B`. Fresh `register(api)` is part of the normal registration loop for loaded candidates, but activation itself is the replacement operation and is not what performs registration.

### Active short circuit

A compatible active registry can be returned without a loader call. This preserves the existing object; it does not replace it. It can hide a later attempted lifecycle from registration, but cannot create `hook-registered`.

## Hook-state semantics

The exact typed-hook storage path is `registry-B8eQDFB4.js:4180-4255`:

1. `registerTypedHook(record, hookName, handler, opts, policy)` validates the hook.
2. Conversation hooks are rejected when the non-bundled policy does not explicitly allow access (`:4225-4235`); accepted hooks increment `record.hookCount` and push an object into `registry.typedHooks` (`:4251-4255`).
3. The plugin API's `on` closure reaches this function at `registry:4776`.

The `before_agent_run` registration chain is therefore:

```text
CogentNexus register(api)
  -> api.on("before_agent_run", handler, ...)
  -> registerTypedHook(...)
  -> policy/record-origin gate
  -> registry.typedHooks.push({ pluginId, hookName, handler, ... })
  -> registry activated as the complete object
```

Activation does not copy or merge `typedHooks`; it swaps `state.activeRegistry` to the supplied object. `createEmptyPluginRegistry` initializes `typedHooks: []`. Consequently:

- A registry A with accepted `before_agent_run` can be replaced by registry B with no such entry.
- B does not inherit A's typed hooks merely because A was previously active.
- A cached registry restores its own prior `typedHooks` because it is the same retained registry object; no hook replay occurs.
- Captured cache state at `loader:2327-2339` includes the registry plus agent harnesses, commands, compaction providers, detached-task registration, interactive handlers, embedding providers, memory embedding providers, memory capability, corpus supplements, and prompt supplements. It does **not** include a separate captured `typedHooks` collection. Hook state is present only insofar as it remains on the captured `state.registry` object.
- There is no source evidence that cache restore merges hooks from the current active object, or that it repairs a missing hook.

Handlers/providers/commands can be restored through their explicit `restore...` functions, but that does not imply typed-hook restoration from any separate side-effect list. The registry object's typed-hook array is retained by object identity.

## Exact source-supported cases

**Case A — A has the hook:** registration passes the policy gate, `registry A.typedHooks` contains an entry whose `hookName` is `before_agent_run`, and A is activated.

**Case B — B lacks the hook:** B is an empty/new registry, or its registration reached `api.on` but the host gate returned before the `typedHooks.push`, or B is a cache entry captured in that state.

The source permits:

```text
A active
  -> later cache hit selects B
  -> activatePluginRegistry(B)
  -> active pointer is B; B.typedHooks has no before_agent_run
```

and:

```text
B active
  -> later cache hit selects retained A
  -> activatePluginRegistry(A)
  -> active pointer is A; A's earlier typed-hook state returns
```

Both replacement directions can occur without `register(api)` in the replacing invocation when the replacing object comes from cache. A new-registry replacement normally follows a miss registration path, but the causal pointer swap remains separate from registration.

## Disposable probe

No disposable probe was run. The installed public loader APIs do not expose private registry identity, cache contents, or typed-hook state in a way that can be observed without patching/monkey-patching the dependency or building an instrumented fixture. An uninstrumented two-call loader invocation would not prove object identity or hook-state replacement and would be non-probative. No temporary probe files were retained.

## Production chronology correlation

The read-only production chronology remains:

`PID 27372 creation → config load → first discovery → first plugin-side hook-registered at 05:13:58.242 → server listening → Gateway ready → second discovery/prewarm-labelled phase → second hook-registered at 05:14:10.542`.

Directly proven:

- The two `hook-registered` events are emitted by the CogentNexus `register(api)` path after its `api.on(...)` calls (CNX-400 source evidence).
- A pure cache hit or active-registry scope short circuit cannot emit those events because both return before plugin registration.
- Exact OpenClaw source provides a mechanism for a later activation to replace the active registry, and cache-hit activation can do so without fresh registration.

Not proven in production:

- Registry identity associated with either event.
- Whether either discovery/prewarm-labelled phase was a cache hit or miss.
- Whether a later lifecycle selected A, B, or a newly constructed registry.
- Whether `before_agent_run` was accepted into the registry active at each event.
- Exact loader caller, invocation counter, cache key, or cache-key fingerprint.
- Whether any active-registry replacement actually occurred in PID 27372.

Timestamp proximity is not registry identity proof. The repeated events can coexist with a later silent cache restoration or replacement that leaves the final active registry without `before_agent_run`; this is mechanically compatible, not a production finding.

## Supported production observability and gap

Read-only supported surfaces expose plugin/status projections and startup/runtime diagnostics, but the inspected version provides no complete supported record containing all of: loader invocation ID, cache hit/miss, cache key, registry object identifier, activation/replacement event, `createApi` reachability, and accepted `typedHooks` snapshot. `plugins list --json`/status may be metadata or a separately loaded projection and cannot establish private object identity. No production instrumentation was added.

The exact evidence required to prove the historical sequence is therefore a PID-correlated lifecycle trace with cache decision/key fingerprint, registry identity/version, activation order, `register(api)`/`api.on` reachability, and host typed-hook acceptance state. Without it, production correlation remains unproven even though the mechanism is proven.

## Direct evidence versus inference

**Direct evidence:** live starting SHA; exact installed module hashes; fresh registry structure; unconditional active-pointer assignment; activation call sites; cache-hit restore and return; cache-miss capture and activation; compatibility/scope short circuits; typed-hook policy and storage lines; and the predecessor production chronology.

**Inference/mechanism application:** A registry A/B sequence with different hook state is source-supported because activation swaps complete registry objects and does not merge `typedHooks`. Applying that sequence to PID 27372 is not proven. The event timestamps do not identify A/B or cache state.

## Required answers

1. **Can a later loader invocation replace the active registry?** Yes. A later cache-hit or cache-miss completion can call activation, which unconditionally replaces the active pointer.
2. **Can replacement happen without fresh `register(api)`?** Yes, when a cached registry is activated; active/scope short circuits can also skip loading entirely.
3. **Does replacement preserve typed hooks?** Only within the selected registry object. Activation does not merge/preserve hooks from the prior active object.
4. **Can cache restoration select different hook state?** Yes. It can reactivate any retained registry, including one with or without `before_agent_run`.
5. **Can repeated events coexist with later hook loss?** Yes, mechanically. The events prove registration-path execution, not final active-registry identity or host acceptance.
6. **What is missing in production?** Invocation/caller, cache hit/miss/key, registry identity and activation sequence, `createApi` reachability, and accepted typed-hook snapshot.
7. **How much is the explanation narrowed?** Materially: registry replacement/retained-state selection is a proven mechanism capable of hiding a prior successful hook registration without a new registration event. It does not establish that this happened in production or exclude policy rejection at another registration path.

## Counts and hard-fence compliance

- Semantic/model/provider/Dashboard requests: `0`
- Production mutations: `0`
- Gateway restart/reload: `0`
- Production config/environment/Scheduled Task mutation: `0`
- Production global extension installation/mutation: `0`
- Artifact replacement/deploy/rebuild: `0`
- OpenClaw dependency patch: `0`
- CogentNexus source repair: `0`
- Debugger/inspector attachment: `0`
- Permanent/committed instrumentation: `0`
- TicketStore/admission/routing/auth changes: `0`
- Historical CNX-360 through CNX-400 edits: `0`
- Release/tag/main changes: `0`
- Force-push/history rewrite: `0`
- CNX-402 created/started: `0`
- Disposable probe files retained: `0`

## Closeout

Only this report and the requested status tokens are authorized for publication. `ACTIVE.md` and `STATUS.md` are set to `WAITING_FOR_CHATGPT_REVIEW`. No CNX-402 was created or started. Final local/remote HEAD, exact changed paths, report blob, and clean-worktree state are recorded in the closeout response after publication verification.
