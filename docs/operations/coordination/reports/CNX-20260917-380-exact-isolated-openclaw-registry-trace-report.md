# CNX-20260917-380 — Exact Isolated OpenClaw Registry Trace

## Classification

**`EXACT_LIFECYCLE_STILL_CONTRADICTORY`**

The real OpenClaw `2026.7.1-2` loader and real effective CogentNexus artifact executed in a disposable process. The observed isolated lifecycle still reports no `before_agent_run` hook, but this run did not expose an `api.on` registration target containing that hook or a causal transition that removed it. Therefore no production cause is claimed.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Starting authoritative HEAD: `540aaafe37eab6dd20396379b7947092488b95f9`
- Task confirmed from fresh GitHub state: `CNX-20260917-380`, `READY_FOR_HERMES`
- Final HEAD: recorded after publication and remote read-back below

## Exact isolated process

- PID: `3576`
- Node: `v22.23.2`
- OpenClaw package: `2026.7.1-2`
- Production PID `27372` was not attached, restarted, or reloaded.
- Disposable workspace/config: `C:\Users\CDQ-P\cnx380-work\.isolated-workspace`
- Runner script was temporary and remains untracked; it was not committed.

## Effective artifact

- Path: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
- SHA-256: `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- The hash was recalculated directly before execution and matched the expected CNX-378 value.

## Exact module identities

| Module | SHA-256 |
|---|---|
| `dist/loader-D8d2EvVh.js` | `3a10479bdcbb713692c3ded7dbd5baad27c1b17ae3566172c117d45916dabce7` |
| `dist/hook-runner-global-BmIrGlLG.js` | `c066170e97a2355603f0bdd3079a687bf835632856a741fa9a92683d7d4b2750` |
| `dist/runtime-D0xGMZdc.js` | `a050a101e3c352345179b77f8c304da99596238fcde95cf03319ebc11dea8791` |
| `dist/registry-B8eQDFB4.js` | `25f3ef82756d85281ad5c25375a5cd2f405989a1145ed438de05992e8c995376` |

## Method

The harness imported the installed ESM modules by file URL and called the real exported `loadOpenClawPlugins`, runtime registry accessors, and global hook-runner accessors. It supplied an isolated config whose plugin load path pointed to the effective artifact. A `WeakMap<object,string>` assigned tokens to returned/observed registry objects. Lifecycle snapshots recorded monotonic sequence and elapsed milliseconds, registry identity, `hooks.length`, `typedHooks.length`, hook names, plugin status, and source paths.

This was not a reimplementation of registry composition. It executed the real loader, plugin module, `setActivePluginRegistry`/`initializeGlobalHookRunner` activation path, live collection, composed facade getters, and real `hasHooks` query.

## Lifecycle ordering

| Seq | Event | ms | Observation |
|---:|---|---:|---|
| 1 | process start | 2 | PID `3576`; artifact hash captured |
| 2 | plugin load returned | 5718 | loader returned registry `R1`; plugin status `loaded` |
| 3 | active registry read | 5718 | active registry was the same object `R1` |
| 4 | live collection read | 5718 | collection contained the active registry; no replacement/reset observed |
| 5 | composed facade evaluated | 5719 | real facade evaluated to zero ordinary hooks and six typed hooks |
| 6 | `getGlobalHookRunner().hasHooks("before_agent_run")` | 5719 | runner existed; result `false` |

No retirement, replacement, reset, or recomposition transition was observed between load and query.

## Identity matrix

| Boundary | Token / identity | Same object? | Hook count | Typed count | Notes |
|---|---:|---:|---:|---:|---|
| loader return / registration registry observable | `R1` | — | 0 | 6 | No `before_agent_run` entry present |
| active registry (`getActivePluginRegistry`) | `R1` | yes, `R1` | 0 | 6 | Same object as loader return |
| `collectLivePluginRegistries()` member | `R1` | yes, `R1` | 0 | 6 | No second live registry observed |
| composed facade object | `R2` | no | 0 | 6 | Facade is a newly created view object; its contents are derived from `R1` |
| `getGlobalHookRunnerRegistry()` at query | `R3` | no | 0 | 6 | Another newly created facade view; not a registry source |
| `hasHooks("before_agent_run")` query | runner-backed composed view | n/a | 0 matching | n/a | Returned `false` |

The identity result is therefore **not** an observed registration-registry mismatch: the loader return, active registry, and live collection member were `R1`. The facade tokens `R2`/`R3` are view objects, not evidence that the underlying source registry was replaced.

## Exact isolated inventory projection

The real loader returned a plugin record for the effective artifact:

- ID: `cogentnexus-openclaw`
- status: `loaded`
- source: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
- ordinary `hooks`: `0`
- typed hooks: `6`
- typed names: `gateway_start`, `gateway_stop`, `before_agent_reply`, `inbound_claim`, `after_compaction`, `session_end`
- `before_agent_run`: absent

This exact isolated projection agrees with the real runner query (`hasHooks=false`). It does not reproduce the CNX-376 premise that an executed `api.on("before_agent_run")` registration exists and then disappears.

## Causal assessment

Not reproduced. The exact run established:

1. Real loader execution succeeds.
2. The effective artifact loads as `loaded`.
3. Registry identity remains `R1` across loader return, active registry, and live collection.
4. The composed facade sees no `before_agent_run` hook.
5. The real global runner returns `false`.

The missing transition is before the observable loaded registry: this run does not prove whether the effective artifact's runtime path invoked `api.on("before_agent_run")`, whether a host policy prevented that registration, or whether the production inventory and this isolated configuration differ. No registry replacement, retirement, collection exclusion, owner/filter rejection, or recomposition cause was proven.

## Production versus isolated evidence

**Production evidence, not reproduced or modified here:** CNX-376/CNX-378 reported PID `27372`, OpenClaw `2026.7.1-2`, the same effective artifact hash, source-level `api.on("before_agent_run")` registration, and live inventory `hookCount: 0`/`hookNames: []`.

**Isolated evidence from PID `3576`:** exact installed module graph and effective artifact executed without production Gateway access; loader/active/live identity was `R1`; exact inventory had six different typed hooks and no `before_agent_run`; real `hasHooks` returned `false`.

CNX-379 synthetic harness results are not used as production cause evidence.

## Remaining uncertainty

- The exact production host/plugin invocation that would make `api.on("before_agent_run")` execute was not observed in this safe isolated run.
- The isolated config may differ from the production host's complete activation/configuration context even though it used the exact installed modules and artifact.
- Consequently the contradiction remains unresolved; no repair authority exists in CNX-380.

## Hard-fence compliance

- Production Gateway restart/reload: `0`
- Production config mutation: `0`
- OpenClaw dependency patch: `0`
- CogentNexus source/artifact patch: `0`
- Dashboard/model/semantic requests: `0`
- TicketStore/admission/provider/auth/routing/model changes: `0`
- Permanent instrumentation: `0`
- Temporary runner script: disposable, untracked, not committed
- Historical CNX-360–CNX-379 edits: `0`
- Force-push/history rewrite/release/main changes: `0`
- CNX-381 started: `0`

## Closeout

After this report is committed and pushed, `ACTIVE.md` and `STATUS.md` are set to `WAITING_FOR_CHATGPT_REVIEW`. No successor task is started.
