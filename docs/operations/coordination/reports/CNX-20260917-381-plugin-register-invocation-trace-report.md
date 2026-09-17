# CNX-20260917-381 — Plugin Register Invocation Trace Report

## Classification

**`PLUGIN_REGISTER_PATH_FAILURE_PROVEN`**

The exact OpenClaw `2026.7.1-2` loader invoked the effective CogentNexus plugin definition and its `register(api)`. The received API exposed a callable host `api.on`. Multiple `api.on("before_agent_run", handler)` calls occurred and returned `undefined` without throwing. The host then emitted the exact compatibility/policy diagnostic that blocked `before_agent_run` because the non-bundled plugin record's effective `hookPolicy.allowConversationAccess` was not true. The registration path therefore reached `api.on`, but the targeted hook was rejected before entering the host typed-hook registry.

This is isolated lifecycle evidence. It is not a production root-cause claim.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Task ID: `CNX-20260917-381`
- Required starting status: `READY_FOR_HERMES`
- Authoritative starting HEAD: `545033f2f5c2dbb4f7f789d6374efe31a63fb8e6`
- Starting remote HEAD: `545033f2f5c2dbb4f7f789d6374efe31a63fb8e6`
- Final HEAD: recorded after the report/state publication and remote read-back

`ACTIVE.md`, `STATUS.md`, and the task file all confirmed `Task ID = CNX-20260917-381` and `Status = READY_FOR_HERMES` before execution.

## Exact runtime and artifact

- OpenClaw package: `2026.7.1-2`
- OpenClaw Node runtime: `v22.23.2`
- Isolated process PID: `16216`
- Disposable isolated plugin root: `C:\Users\CDQ-P\cnx381\.cnx381-isolated\plugin`
- Temporary evidence: `C:\Users\CDQ-P\cnx381\cnx381-evidence.jsonl`
- Effective production artifact used as source input: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
- Effective artifact SHA-256: `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- Temporary instrumented copy SHA-256: `df1b61193f3493b6d5db5135627083cbcb77eb1ed2ecb22235f1d5bf1f3317b3`
- Instrumentation was applied only to the disposable copy; the effective artifact was not modified.

The exact installed OpenClaw module graph was imported from the installed `dist/` directory, including `loader-D8d2EvVh.js`, `runtime-D0xGMZdc.js`, `hook-runner-global-BmIrGlLG.js`, and `registry-B8eQDFB4.js`. The real `loadOpenClawPlugins` path was used; the lifecycle was not replaced by a synthetic registry model.

## Plugin definition evidence

The loader reported the temporary copy as:

- ID: `cogentnexus-openclaw`
- source: `C:\Users\CDQ-P\cnx381\.cnx381-isolated\plugin\dist\v091-release-entry.js`
- root: `C:\Users\CDQ-P\cnx381\.cnx381-isolated\plugin`
- status: `loaded`
- tools: five declared CogentNexus tools
- final inventory projection: `hookCount: 26` typed registrations, with ordinary `hooks: []`

The original effective artifact exported a definition with a `register` function and `hooks: { allowConversationAccess: true }`. The definition was loaded by the real loader, not merely imported by the harness.

## Register invocation evidence

The disposable instrumentation recorded:

| Event | Evidence |
|---|---|
| `register(api)` entry | `2026-09-17T01:50:05.569Z`, event `register-entry` |
| API value | JavaScript object, serialized identity prefix `[object Object]` |
| `api.on` | callable function (`typeof api.on === "function"`) |
| register completion | Loader returned normally; no register exception and no `register` failure diagnostic |
| plugin load result | `loaded 1 plugin(s) (1 attempted)` |

The exported outer entry performed its host-authority check, delegated through `legacyEntry.register(runtimeApi)`, and installed the downstream compatibility/runtime registrations. The loader's returned plugin record contained five registered services and 26 typed hook records, proving that execution progressed beyond a definition-only import.

## API and `api.on` evidence

The outer `register(api)` wrapper replaced only the disposable API object's `on` method with an observing delegate, preserving the original host function as `__cnx381origOn` and forwarding every call unchanged.

Observed facts:

- `api` was an object.
- `api.on` was a function.
- Calls were made through the host API path used by the loader.
- The delegate returned the original result; all observed registration calls returned `undefined`.
- No observed `api.on` call threw.
- The wrapper chain (`withDiscordLegacyDeliveryFence` then `withWebchatLegacyDeliveryFence`) delegated non-delivery hooks back to the same outer `api.on`, so the nested registration did not create a separate host registry mechanism.

## `before_agent_run` call evidence

The disposable trace recorded multiple calls to `api.on("before_agent_run", handler)`. Representative entries were:

| UTC timestamp | Result | Thrown | Handler evidence |
|---|---|---|---|
| `2026-09-17T01:50:05.570Z` | `undefined` | none | native restart ownership handler |
| `2026-09-17T01:50:07.219Z` | `undefined` | none | abort/restart authority handler |
| `2026-09-17T01:50:07.221Z` | `undefined` | none | delivery/inference bridge handler |
| `2026-09-17T01:50:07.223Z` | `undefined` | none | context/admission handler |
| `2026-09-17T01:50:07.224Z` | `undefined` | none | additional context/recovery handler |
| `2026-09-17T01:50:07.225Z` | `undefined` | none | finalization/compatibility handler |

The full raw trace is retained in the disposable evidence file above. The exact source registration in the effective artifact is also present at the compiled equivalent of `index.ts:753`, guarded by `config.preInferenceAdmission !== false`.

## Registry counts and mutation result

The real loader returned a registry whose final plugin projection reported:

- ordinary hook collection: `0`
- typed hook collection: `26`
- `before_agent_run`: absent from the final typed hook inventory
- `hasHooks("before_agent_run")`: `false`
- global runner typed-hook count: `26`

The host emitted these exact diagnostics during the same process:

```text
typed hook "before_agent_run" blocked because non-bundled plugins must set plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess=true
```

The diagnostic occurred repeatedly for the `before_agent_run` registrations, while other typed hooks were accepted. Thus the absence of `before_agent_run` is not explained by `api.on` never occurring. The call reached the real host `registerTypedHook` mechanism, but the targeted hook was rejected by the effective compatibility/policy gate and did not enter the final registry.

The API delegate observed no return-value signal distinguishing acceptance from rejection: both accepted and rejected calls returned `undefined`. The host diagnostic and final inventory are the decisive side-effect evidence.

The trace's per-call pre/post object snapshot was unavailable before registry initialization (`null` at the observing point), so no claim is made that every individual call changed a numeric count. The final loader-owned registry projection and host diagnostics directly prove the targeted hook was not stored, while other typed registrations were stored.

## Lifecycle ordering

Observed ordering:

1. Isolated process started: PID `16216`.
2. Exact artifact was copied byte-identically before temporary instrumentation; original SHA recorded.
3. Real loader discovered and loaded the isolated plugin definition.
4. `register(api)` entry occurred at `01:50:05.569Z`.
5. First `before_agent_run` `api.on` call occurred at `01:50:05.570Z`.
6. Additional delegated registrations occurred from `01:50:07.219Z` through `01:50:07.256Z`.
7. Host emitted the conversation-hook policy-block diagnostics during those calls.
8. Loader completed normally and activated the returned registry.
9. Final global runner view contained 26 typed hooks but no `before_agent_run`; `hasHooks("before_agent_run")` was false.

This run proves the targeted registration path failed before final registry storage. It does not show a later retirement, replacement, or collection exclusion.

## Compatibility/delegation chain

Static inspection of the exact source/build chain and the runtime trace establish:

```text
v091-release-entry.ts / exported releaseEntry
  -> definePluginEntry(...)
  -> outer register(api)
  -> hostPluginAuthority(api)
  -> withDiscordLegacyDeliveryFence(api, config)
  -> withWebchatLegacyDeliveryFence(discordFencedApi, config)
  -> legacyEntry.register(runtimeApi)
  -> v091-final-entry.ts
  -> v090-final-entry.ts
  -> v090-entry.ts
  -> v090.ts
  -> index.ts registration body
  -> api.on("before_agent_run", handler)
  -> OpenClaw registerTypedHook
  -> conversation-hook compatibility/policy gate
  -> final typed registry
```

Important distinctions:

- The outer `register(api)` is synchronous in the observed path and delegates to the nested registration function.
- The nested API is a wrapper object for delivery-fence behavior, but its non-delivery `on` calls delegate to the same outer host `api.on`; it does not create a new registry.
- The effective source contains conditional registration: `before_agent_run` is guarded by `preInferenceAdmission !== false`. The isolated config enabled that path, and the trace proves the calls occurred.
- No delayed Promise-only registration was needed to explain the observed result. The loader completed with the registrations that were accepted.
- The decisive conditional path was the host compatibility/policy gate for non-bundled conversation hooks.

## Explicit A/B/C/D/E assessment

- **Case A — `register(api)` not called:** disproven. Entry timestamp and normal loaded result prove invocation.
- **Case B — register called but nested path not reached:** disproven. Delegated registrations and 26 final typed hooks prove nested execution reached the registration body.
- **Case C — `api.on()` called but not the expected host mechanism:** disproven for the observed API boundary. The real loader supplied the API, the real OpenClaw registration delegate was reached, and the host emitted its native `registerTypedHook` policy diagnostic.
- **Case D — `api.on()` accepted but registry count unchanged:** not the best classification for `before_agent_run`. The host did not accept this targeted hook; it explicitly blocked it. Other typed registrations changed the final registry, showing the registry path itself was active.
- **Case E — mutation succeeded then later hook disappeared:** disproven in this run. No accepted `before_agent_run` mutation, retirement, replacement, or collection exclusion was observed.

Therefore the result is a registration-path failure at the host compatibility/policy gate, not a composition/lifecycle removal finding.

## Classification rationale

`PLUGIN_REGISTER_PATH_FAILURE_PROVEN` is selected because the exact isolated lifecycle directly proves:

1. the plugin definition was loaded;
2. the real `register(api)` was invoked;
3. the real API object's `on` function was invoked;
4. `before_agent_run` registration calls occurred;
5. those calls returned without throwing;
6. OpenClaw explicitly rejected the targeted non-bundled conversation hooks under its effective policy;
7. the final registry had other typed hooks but no `before_agent_run`.

This is the first proven broken edge in the isolated call graph: `api.on("before_agent_run")` → host conversation-hook acceptance.

## Production versus isolated evidence

### Production facts only

The following remain production observations and were not modified or re-tested by this task:

- PID `27372`
- OpenClaw `2026.7.1-2`
- effective artifact SHA-256 `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- plugin loaded
- production inventory `hookCount=0`

No production Gateway restart/reload, debugger attach, config mutation, semantic request, or model request occurred.

### Isolated evidence

Only PID `16216` and the disposable copied plugin/module environment support the invocation, API, `api.on`, policy diagnostic, and final registry claims in this report. The isolated process is not asserted to be byte-for-byte identical in every host configuration detail to production. In particular, this report does not claim that the production host currently exposes the same effective policy object; it reports the exact mechanism observed in the authorized isolated reproduction.

## Remaining uncertainty

- The isolated config-selected plugin had a host diagnostic saying the effective non-bundled hook policy was not true even though the exported definition object carried `hooks.allowConversationAccess: true`; the precise loader metadata projection that lost or failed to pass that property is not further patched or repaired here.
- The per-call numeric registry snapshot was unavailable before activation, so this report does not claim a numeric before/after delta for each individual rejected call.
- Production causal equivalence is not claimed without a production debugger or restart, both forbidden.
- No repair authority exists in CNX-381.

## Hard-fence compliance

- Production Gateway restart/reload: `0`
- Production configuration mutation: `0`
- OpenClaw dependency patch: `0`
- CogentNexus source/artifact patch: `0`
- Dashboard semantic/model/provider requests: `0`
- TicketStore/admission/routing/auth changes: `0`
- Permanent instrumentation: `0`
- Temporary instrumentation: disposable copied process only; not committed
- Historical CNX-360 through CNX-380 edits: `0`
- Force-push/history rewrite/release/tag/main: `0`
- CNX-382 started: `0`

## Closeout

After this report is published, `ACTIVE.md` and `STATUS.md` are updated to `WAITING_FOR_CHATGPT_REVIEW`. No repair is attempted and CNX-382 is not started.
