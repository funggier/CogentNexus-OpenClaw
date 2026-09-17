# CNX-20260917-392 — Production-vs-Config-Origin Hook-Policy Replay Report

## Classification

`PRODUCTION_ORIGIN_REPLAY_DIAGNOSTICALLY_BLOCKED`

The installed-source trace shows that `global` and `config` are discovery-origin labels carried on the plugin record, and that the non-bundled conversation policy gate treats both identically (`record.origin !== "bundled"`). The loader passes the same `entry?.hooks` value as `hookPolicy` to `createApi` in the ordinary runtime path. However, a safe disposable reproduction of the exact production `origin=global` discovery path was not available without installing or mutating the production global extension tree. No substitute was fabricated. Therefore this task does not claim a causal A/B elimination or reproduction.

## Authority and closeout

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Authoritative starting remote/local HEAD: `36e4cd4a9773b3b6c95fd5a7536c4823c94f266a`
- Authoritative final remote HEAD: recorded after the report/state publication and remote read-back
- Starting gate: `READY_FOR_HERMES`
- Final coordination state: `WAITING_FOR_CHATGPT_REVIEW`

Remote was fetched first and a fresh clone was created at the authoritative tip. The clone was clean before the authorized report/state edits. Historical CNX-360 through CNX-391 files were not modified.

## Exact runtime and hashes

Installed OpenClaw source was inspected read-only from the exact candidate runtime used by predecessors:

- OpenClaw package: `2026.7.1-2 (0790d9f)`
- Node runtime: `v22.23.2`
- Effective CogentNexus artifact SHA-256: `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- Production config SHA-256: `19d7e6acf53ce370dc20e5e2a2547c9674c33b178208b79920cb0e9dce9b46b`

| Installed module | SHA-256 |
|---|---|
| `dist/discovery-7zi_zNvu.js` | `5489a4b1086fed443cedf54efccc76a730960e8419bba4d97010c3420a342ddd` |
| `dist/loader-D8d2EvVh.js` | `3a10479bdcbb713692c3ded7dbd5baad27c1b17ae3566172c117d45916dabce7` |
| `dist/registry-B8eQDFB4.js` | `25f3ef82756d85281ad5c25375a5cd2f405989a1145ed438de05992e8c995376` |
| `dist/runtime-D0xGMZdc.js` | `a050a101e3c352345179b77f8c304da99596238fcde95cf03319ebc11dea8791` |
| `dist/hook-runner-global-BmIrGlLG.js` | `c066170e97a2355603f0bdd3079a687bf835632856a741fa9a92683d7d4b2750` |

## Production and predecessor inventory evidence

Production observation (not reloaded or modified here): `origin=global`, `status=loaded`, `hookCount=0`, `hookNames=[]`.

CNX-390 disposable supported CLI replay: `origin=config`, `status=loaded`, `activated=true`, `hookCount=0`; registration calls and host policy were not exposed.

CNX-391 disposable exact-loader/API replay, with the same production-shaped entry and `allowConversationAccess=true`, directly observed `register(api)`, repeated `api.on("before_agent_run")`, and final typed-hook acceptance (six `before_agent_run` entries in a 42-hook final inventory). Its false-policy control omitted the targeted hook while retaining other typed hooks.

These are separate production and isolated observations; none proves production in-memory acceptance.

## Exact source trace

All line numbers below are from the hashed installed files above.

### Origin assignment

`discovery-7zi_zNvu.js:1231-1242` calls `discoverFromPath` with `origin: "config"` for configured load paths. `discovery-7zi_zNvu.js:1368-1382` calls it with `origin: "global"` for installed paths, and `:1383-1395` uses `origin: "global"` for the global directory scan. This establishes origin as discovery metadata attached at candidate construction; it does not by itself establish different registration behavior.

### Registration mode

`loader-D8d2EvVh.js:1794-1817` resolves `registrationPlan` and assigns `const registrationMode = registrationPlan.mode`. The mode is derived from the registration plan, not directly from the string origin. `loader-D8d2EvVh.js:2254-2258` uses the resulting mode only as the profile label around `runPluginRegisterSync(register, api)`.

`registry-B8eQDFB4.js:4384-4387` defaults `params.registrationMode` to `"full"` and resolves registration capabilities. `:4393-4404` passes `registrationMode`, config, and plugin config into the API builder. No source line found in the inspected path derives a distinct mode solely from `global` versus `config`.

### Hook-policy and registration boundary

`loader-D8d2EvVh.js:2237-2242` constructs the ordinary runtime API with `pluginConfig: validatedConfig.value`, `hookPolicy: entry?.hooks`, and `registrationMode`. The setup branch at `:1994-1999` likewise passes `hookPolicy: entry?.hooks`.

`registry-B8eQDFB4.js:4776` routes `api.on` to `registerTypedHook(..., params.hookPolicy)`. `:4180-4250` implements the policy boundary. For conversation hooks, `:4225-4235` rejects when `record.origin !== "bundled"` and `policy?.allowConversationAccess !== true`; `:4236-4244` separately rejects bundled plugins only when the explicit value is false. Thus both `config` and `global` are in the same non-bundled branch, while only `bundled` is treated differently. The inspected source contains no global-specific skip of `entry?.hooks` and no global-specific `createApi` hook-policy source.

Registration capabilities are resolved from mode at `registry-B8eQDFB4.js:4385-4386`; the inspected hook call is still supplied the same `params.hookPolicy` at `:4776`. Source evidence therefore supports metadata-only origin with respect to the conversation-policy branch, but does not replace the required runtime A/B evidence.

## Disposable A/B status and fixture provenance

| Case | Origin | Registration mode | `entry.hooks` | `hookPolicy` | `before_agent_run` | Final hook count |
|---|---|---|---|---|---|---|
| A (CNX-391 exact config-origin replay) | `config` | observed by loader/API path; exact numeric mode not retained in report | `allowConversationAccess=true` at production-shaped entry | true policy accepted in host registry | observed and accepted | `42` total; six targeted entries |
| B (required global-origin replay) | not safely reproduced | not observed | not observed | not observed | not observed | not observed |

The A fixture provenance was the CNX-391 disposable copy of the exact effective artifact and production-shaped non-secret plugin entry. CNX-391 recorded PID `6468` for true policy and PID `16468` for its false-policy control, Node `v22.23.2`, and the exact module identities listed above. No new semantic or production process was started by this task.

An exact B replay would require the real installed discovery/installation-record mechanism to classify the same artifact as `global`. Constructing that by adding an installation record or test extension to the production global extension root would violate the hard fence. A temporary copy alone would change the source path but would not prove the real global discovery mechanism; treating that substitute as B would be fabrication. Accordingly, no global-origin process/PID is claimed.

## Causal comparison

**Direct evidence:** origin assignment sites; `registrationMode` derivation from `registrationPlan.mode`; both runtime `createApi` call sites passing `entry?.hooks`; `api.on` routing to `registerTypedHook`; and the explicit non-bundled origin predicate in the policy gate. CNX-390 and CNX-391 predecessor observations are also direct evidence for their respective disposable runs.

**Inference:** within the inspected exact source path, `global` versus `config` does not select a different conversation-hook policy branch: both satisfy `record.origin !== "bundled"`. The source therefore weakens, but does not fully close, the hypothesis that the inventory origin alone caused the discrepancy. It does not prove the running production process consumed the same normalized entry or registration plan.

Because the required global-origin runtime A/B was diagnostically blocked, the permitted classification is `PRODUCTION_ORIGIN_REPLAY_DIAGNOSTICALLY_BLOCKED`, not `PRODUCTION_ORIGIN_DIFFERENCE_ELIMINATED` and not `PRODUCTION_ORIGIN_DIFFERENCE_CAUSALLY_REPRODUCED`.

## Predecessor comparison

- **CNX-381:** false/absent effective non-bundled policy reached `registerTypedHook` and was rejected before typed-registry storage.
- **CNX-390:** production-shaped config-origin CLI load was loaded/activated but did not expose registration or policy boundaries; `hookCount=0` was diagnostically blocked.
- **CNX-391:** exact config-origin loader/API instrumentation directly observed true-policy acceptance and a false-policy control rejection.
- **CNX-392:** exact source trace finds no origin-only policy branch; the required global-origin replay could not be safely constructed, so production origin remains unresolved as a runtime causal factor.

No registry-composition loss is claimed: this task did not observe an accepted host insertion followed by disappearance.

## Remaining production uncertainty

Production still has `origin=global` and zero reported hooks, but this report does not inspect production memory, attach a debugger, reload the Gateway, or infer a gate result from inventory. Remaining possibilities include runtime configuration/provenance or another activation/discovery difference not observable without the forbidden production lifecycle/debugger actions. Dashboard Ticket-first semantic success is not claimed.

## Counts and hard-fence compliance

- Semantic/model/provider/Dashboard requests: `0`
- Production mutation count: `0`
- Production Gateway restart/reload: `0`
- Production config/environment/Scheduled Task mutation: `0`
- Production artifact replacement/deploy/rebuild: `0`
- OpenClaw dependency patch/source repair: `0`
- Production debugger/inspector attachment: `0`
- Persistent test installation: `0`
- Permanent or committed instrumentation: `0` (no instrumentation committed)
- Historical CNX-360 through CNX-391 modifications: `0`
- Release/tag/main changes: `0`
- Force-push/history rewrite: `0`
- CNX-393 created/started: `0`

## Closeout

`ACTIVE.md` and `STATUS.md` were set to `WAITING_FOR_CHATGPT_REVIEW` in the publication commit. Execution stops here. No production retry, semantic request, repair, or successor task was started.
