# CNX-20260917-378 — Live Registry Identity Correlation Diagnosis

## Classification

**`LIVE_REGISTRY_IDENTITY_CONTRADICTION_UNRESOLVED`**

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Authoritative starting HEAD: `f9b2af0daeb5c44ff829b89ba721a3c19e8b8b19`
- Final candidate HEAD: `f04c785ae11a31a40c1d4f81a61bb1d19560e5d6`
- Semantic requests: **0**
- Production restart/reload: **0**

## Live runtime identity

Read-only `openclaw gateway status` identified one live gateway:

- OpenClaw CLI version: `2026.7.1-2`
- Gateway version: `2026.7.1-2`
- Process: `node.exe`, PID `27372`
- Gateway: `127.0.0.1:18789`, listening and connectivity probe `ok`
- Runtime status: `running`, state `Ready`
- Log path: `C:\Users\CDQ-P\AppData\Local\Temp\openclaw\openclaw-2026-09-17.log`
- Node runtime reported in gateway log: `24.18.0`

The service command points to:

`C:\Program Files\nodejs\node.exe C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw\dist\index.js gateway --port 18789`

The process was independently correlated to PID `27372` by the listening socket on `127.0.0.1:18789`.

## Effective plugin identity

Fresh SHA-256 from the effective installed artifact:

`C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`

`2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`

Read-only `openclaw plugins list --json` correlated the live loaded record to the same path:

```json
{
  "id": "cogentnexus-openclaw",
  "source": "C:\\Users\\CDQ-P\\.openclaw\\extensions\\cogentnexus-openclaw\\dist\\v091-release-entry.js",
  "rootDir": "C:\\Users\\CDQ-P\\.openclaw\\extensions\\cogentnexus-openclaw",
  "origin": "global",
  "status": "loaded",
  "enabled": true,
  "hookCount": 0,
  "hookNames": [],
  "toolNames": []
}
```

The active configuration was also read without mutation. It has `preInferenceAdmission: true`, `ticketFirst: true`, and `hooks.allowConversationAccess: true` under the plugin entry.

## OpenClaw module/build identity

The installed package was read directly from:

`C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw\package.json`

Identity: `{ "name": "openclaw", "version": "2026.7.1-2" }`

Fresh hashes of the relevant loaded-installation module files:

| Module | SHA-256 |
|---|---|
| `dist/loader-D8d2EvVh.js` | `3a10479bdcbb713692c3ded7dbd5baad27c1b17ae3566172c117d45916dabce7` |
| `dist/hook-runner-global-BmIrGlLG.js` | `c066170e97a2355603f0bdd3079a687bf835632856a741fa9a92683d7d4b2750` |
| `dist/runtime-D0xGMZdc.js` | `a050a101e3c352345179b77f8c304da99596238fcde95cf03319ebc11dea8791` |
| `dist/registry-B8eQDFB4.js` | `25f3ef82756d85281ad5c25375a5cd2f405989a1145ed438de05992e8c995376` |

Source markers in those exact installed files show:

- loader line 1483: `setActivePluginRegistry(registry, ...)`
- loader line 1484: `initializeGlobalHookRunner(registry)`
- loader lines 1997 and 2240: `hookPolicy: entry?.hooks`
- hook-runner-global line 30: `composeLiveHookRegistry(lastInitialized)`
- hook-runner-global lines 89–98: facade getters recompute the composed view
- hook-runner-global line 1108: `initializeGlobalHookRunner(registry)`
- runtime line 584: `collectLivePluginRegistries()`
- runtime line 626: `setActivePluginRegistry(...)`
- registry line 4776: `api.on` maps to `registerTypedHook(...)`

## Registration and composition evidence

The live log contains plugin startup events for the same effective artifact/runtime family, including:

- plugin discovery naming the exact CogentNexus artifact path;
- `CogentNexus-OpenClaw delivery-observe {"event":"hook-registered", ...}`;
- gateway startup listing `cogentnexus-openclaw` among loaded plugins.

These logs prove plugin initialization-side activity, but they do not expose a stable registry object identity, the `registry` argument passed to `initializeGlobalHookRunner`, `state.registry`, or the composed facade's object/collection identity.

The supported plugin inventory simultaneously reports the exact loaded plugin as `status: loaded` with `hookCount: 0` and `hookNames: []`. This reproduces the CNX-376 observable symptom against the currently running OpenClaw version and effective plugin path, but it does not prove which internal boundary removed or excluded the hook.

## Process-local identity access result

No passive supported diagnostic endpoint exposed JavaScript object identity or global hook-runner state. Node inspector probes on ports 9229 and 9222 were unavailable. The supported gateway status/list commands exposed PID, version, paths, and inventory, but not registry references or `hasHooks` internals.

No debugger was attached, no live files/configuration were changed, and no restart was performed. Therefore the following required identities remain unobserved:

- registry object receiving the plugin `api.on` mutation;
- registry object stored in `state.registry`;
- live registry collection returned by `collectLivePluginRegistries()` at the Dashboard query;
- exact composed facade contents at the `hasHooks("before_agent_run")` call.

## Correlation conclusion

The runtime/build/artifact correlation is strong:

`PID 27372` → OpenClaw `2026.7.1-2` → installed module paths above → effective CogentNexus artifact SHA above → loaded plugin record → `hookCount: 0`.

However, the current installed OpenClaw source model says the global runner composes live registries and observes mutations dynamically, while the same live runtime reports no CogentNexus hooks. The evidence therefore establishes a **live contradiction**, not a proven instance mismatch, replacement/reset, composition exclusion, or ordering defect.

No repository-side repair is authorized or justified by this evidence. A source or dependency patch would be speculative and would violate CNX-378's diagnosis-only boundary.

## Validation and fences

- Authoritative branch was freshly fetched before investigation.
- Effective plugin hash computed directly from disk.
- Live gateway status and plugin inventory read without mutation.
- No semantic/model/provider request.
- No production restart/reload.
- No OpenClaw dependency patch.
- No plugin source patch.
- No configuration mutation.
- No TicketStore/admission/provider/model/auth/routing/Dashboard UI changes.
- No historical CNX-360 through CNX-377 edits.
- No force-push, release/tag/main mutation, or CNX-379 work.

## Handoff

`ACTIVE.md` and `STATUS.md` are set to `WAITING_FOR_CHATGPT_REVIEW`. Stop after this handoff.
