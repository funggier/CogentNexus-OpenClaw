# CNX-20260917-400 — Production Loader Repeated-Registration and Cache Correlation Report

## Classification

`PRODUCTION_CACHE_CAUSALITY_NARROWED`

Exact source proves that the two observed `hook-registered` records are emitted inside the CogentNexus `register(api)` function, after actual `api.on(...)` calls. A pure OpenClaw loader-cache hit and the runtime active-registry short circuits return without invoking plugin registration, so neither can produce those records. This narrows the explanation for those specific events, but existing production telemetry does not expose cache hit/miss, cache key, registry identity, or the complete loader invocation graph; production cache causality is not claimed.

## Authority and identity

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Exact authoritative starting local/remote HEAD: `34ba6f1ed4d8b06f1b2931ae3bf8f36a355d53be`
- Embedded task baseline discrepancy: task body says `accde2e0...`; live GitHub authority was `34ba6f1e...` and was used.
- Starting gate: `READY_FOR_HERMES`
- Final HEAD: recorded after publication and remote read-back below.

GitHub was fetched first with an explicit branch refspec; `git ls-remote` matched the checked-out starting HEAD. ACTIVE, STATUS, CNX-400 and CNX-399 through CNX-391 were read. The checkout used was a clean dedicated workspace clone; unrelated untracked files in another local checkout were not touched.

## Exact runtime and hashes

Read-only installed runtime observations:

- OpenClaw: `2026.7.1-2 (0790d9f)`
- Effective production artifact inspected: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-dashboard-verified-delivery.js`
- Artifact SHA-256: `1276bd624b62f96692eaa19f493f69e422771b6994b39ded94b2bcb3399e1f98`
- Installed module root: `C:\Users\CDQ-P\.openclaw\workspace\test\CogentNexus-OpenClaw\plugins\cogentnexus-openclaw\node_modules\openclaw`

| Module | SHA-256 |
|---|---|
| `dist/loader-D8d2EvVh.js` | `3a10479bdcbb713692c3ded7dbd5baad27c1b17ae3566172c117d45916dabce7` |
| `dist/registry-B8eQDFB4.js` | `25f3ef82756d85281ad5c25375a5cd2f405989a1145ed438de05992e8c995376` |
| `dist/runtime-registry-loader-Duw3fvRO.js` | `bd6a9f363bc7aac2fb0503640e339ffce52e0eab15336e6489b6f8129df748fb` |

## 1. Exact `hook-registered` provenance

CogentNexus source (`plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts:773-778`) increments `OBSERVATION_REGISTRATION_COUNT` and calls `observeDelivery(api.logger, "hook-registered", ...)`. The preceding registration body contains the actual typed-hook calls, including `api.on("before_agent_run", ...)` and other `api.on(...)` calls (`:650-772`); the same exact built artifact contains the event at `dist/v091-dashboard-verified-delivery.js:797-802`.

Thus the call chain is:

```text
OpenClaw loader -> plugin register(api) -> api.on("before_agent_run", ...) / other api.on calls
  -> OBSERVATION_REGISTRATION_COUNT++ -> observeDelivery(..., "hook-registered", ...)
```

The event is not emitted by OpenClaw's `registerTypedHook`; it is plugin-side logging after the plugin's hook-registration calls. There is no alternate event producer in the inspected CogentNexus source. On the exact function path, the event requires execution of `register(api)` and cannot occur from a lifecycle that merely restores a host registry. It is therefore strong evidence of plugin registration-path execution, but it is not by itself proof that the host accepted `before_agent_run`: `api.on` can return without throwing while the host policy gate rejects storage (as CNX-391 demonstrated).

## 2. Cache-hit source mapping

In `loader-D8d2EvVh.js:1500-1527`, cache is enabled unless `options.cache === false` or raw-config resolution is requested. The loader performs lookup at `:1502-1507`; on hit (`:1508`) it restores retained side effects at `:1510-1521`, activates the retained registry at `:1522`, returns the cached registry at `:1524`, and never reaches the miss path beginning `:1527`.

The miss path subsequently discovers/builds records and invokes registration; the cached state is populated after that work at `:2327-2340`. The retained state contains the registry and registered agent harnesses, commands, compaction providers, detached task runtime registration, interactive handlers, embedding/memory provider state, and memory supplements (`:1510-1522`). It does not rerun plugin code or re-call `register(api)` on a hit. Therefore a pure cache hit cannot call CogentNexus `api.on`, cannot execute its `observeDelivery`, and cannot emit `hook-registered`.

## 3. Active-registry short circuits

`runtime-registry-loader-Duw3fvRO.js:87-93` returns immediately when the loaded scope and active registry satisfy the requested scope. The second short circuit at `:90-93` likewise returns after setting the scope marker when applicable. Only otherwise does it call `resolveOrLoadRuntimePluginRegistry` at `:102-112`; the module-global marker is updated at `:113`. These returns do not call the loader, plugin `register(api)`, or `api.on`. They cannot emit `hook-registered`.

## 4. Production chronology correlation

The pre-existing production chronology is recorded as: process creation → config load → first discovery → `hook-registered` at `05:13:58.242` → server listening → Gateway ready → later discovery/prewarm-labelled activity → `hook-registered` at `05:14:10.542`.

Source linkage supports only these bounded conclusions:

- Each event is evidence that the plugin registration function reached its plugin-side event logging path; it is not a cache-hit restore event.
- If the surrounding discovery records are distinct loader invocations, each event is compatible with a cache miss/new registration, or with another caller that explicitly bypasses/replaces the registry. The timestamps alone do not prove that mapping.
- A cache hit or active-registry short circuit could occur at other silent invocations and would suppress a new plugin-side event.
- The existing logs do not contain the cache key, cache hit/miss decision, registry identity, `createApi` identity, or a caller-to-event correlation. Consequently neither event proves production cache miss, and neither proves that the event's `before_agent_run` was accepted by the host.

No production process was restarted, retried, instrumented, or attached to. No semantic/model/provider/Dashboard request was made.

## 5. Registration-state restoration semantics

The source explicitly restores the listed captured global registration state and the cached registry object; it does not reconstruct or repair missing entries. A registry that was cached without `before_agent_run` remains without that entry when restored. A later cache hit therefore cannot repair it. Repair would require a cache miss/new registry and a registration path that calls `api.on` and passes the host policy gate, or an active-registry replacement caused by a non-short-circuited load. The cached-state fields do not include a mechanism that replays CogentNexus's registration function.

## 6. Direct evidence versus inference

**Direct evidence:** live GitHub starting SHA; exact installed hashes; plugin event source and line ranges; OpenClaw cache lookup/hit/restore/return lines; active-registry return lines; the earlier production chronology; CNX-391's direct observation that plugin-side calls may be rejected by host policy; and the process-global nature established by CNX-399.

**Inference, not proof:** the two timestamps likely correspond to separate startup/prewarm lifecycle activity; they may represent cache misses/re-registration. No source or telemetry binds either event to a specific loader caller or cache decision. `plugins list --json`, `hookCount`, `hookNames`, installed-index timestamps, and timestamp proximity are weak evidence and are not used as cache proof.

## 7. Boundary answers

1. **Does `hook-registered` require actual registration/API hook-call execution?** Yes, on the exact CogentNexus source path it requires `register(api)` to execute and reach the post-`api.on` event logger. It does not prove host acceptance.
2. **Can cache hit or active-registry short circuit produce it?** No; both return before plugin registration.
3. **Do the two events prove two actual registration paths?** They prove two executions of the plugin registration event path, not necessarily two distinct OpenClaw loader calls; an alternate direct caller is not shown in the source inspected. They do not prove two accepted hooks.
4. **Does this weaken a pure-cache-hit explanation for those events?** Yes. A pure hit cannot explain either event. It does not rule out cache reuse elsewhere in the process.
5. **Can cache reuse explain a later silent invocation?** Yes, as a mechanism: a hit can restore the prior (possibly incomplete) registry without new registration logging. This remains a production hypothesis, not a historical finding.
6. **What is still required?** Per-invocation PID-correlated telemetry containing caller/lifecycle, cache enabled flag, exact cache key or equivalent key fingerprint, hit/miss, registry identity, `createApi`/`register(api)` identity, and accepted host typed-hook registry state. Existing production read-only evidence exposes none of these as a complete correlated record.

## Disposable probe

No new probe was run. A public loader call without cache and registration identity observation would be non-probative; the permitted task supplied no safe, exact, non-invasive way to observe the production process's private cache state. Prior CNX-391 isolated instrumentation remains mechanism evidence only and was not modified or reused as production evidence.

## Impact on missing `before_agent_run` hypothesis

The cache hypothesis is narrowed, not established or eliminated. It cannot explain the two observed plugin-side `hook-registered` records as pure cache-hit outputs. It can still explain a subsequent silent invocation restoring an earlier registry that lacked the hook, but the production cache state and registry identity are unobserved. The remaining missing-hook possibilities at this boundary are therefore limited to (a) an unobserved incomplete cached/active registry, (b) a registration call reaching the host gate but being rejected, or (c) another unobserved lifecycle/association difference; this report does not select among them.

## Counts and hard-fence compliance

- Semantic/model/provider/Dashboard requests: `0`
- Production mutations: `0`
- Gateway restart/reload: `0`
- Production config/environment/Scheduled Task mutation: `0`
- Global extension installation/mutation: `0`
- Artifact replacement/deploy/rebuild: `0`
- OpenClaw dependency patch: `0`
- CogentNexus source repair: `0`
- Debugger/inspector attachment: `0`
- Permanent/committed instrumentation: `0`
- TicketStore/admission/routing/auth changes: `0`
- Historical CNX-360 through CNX-399 edits: `0`
- Release/tag/main changes: `0`
- Force-push/history rewrite: `0`
- CNX-401 created/started: `0`

## Closeout

Report publication is followed by changing only the requested status token in `ACTIVE.md` and `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW`. No successor task is created or started.
