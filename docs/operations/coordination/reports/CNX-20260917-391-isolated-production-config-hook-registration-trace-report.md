# CNX-20260917-391 — Isolated Production-Config Hook Registration Trace Report

## Classification

**`PRODUCTION_CONFIG_REPLAY_ACCEPTS_HOOK_POLICY`**

The production-shaped plugin entry, replayed through the exact installed OpenClaw loader/API lifecycle in a disposable process, invoked `register(api)` and multiple `api.on("before_agent_run")` calls. The final real registry contained `before_agent_run`; the false-policy control omitted it while retaining other typed hooks. This is isolated mechanism evidence only, not production-memory observation or direct production root-cause proof.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Authoritative starting local/remote HEAD: `185e1c15eaf833095211ac01e4c6dda1b3cb858f`
- Starting status: `READY_FOR_HERMES`
- Task: `CNX-20260917-391`
- Final HEAD: recorded after publication and remote read-back

Remote was fetched before execution; local HEAD equaled the requested authoritative remote HEAD. Historical reports CNX-380/381/382/385/387/388/389/390 and coordination ACTIVE/STATUS were read before execution.

## Exact baseline and hashes

- OpenClaw: `2026.7.1-2 (0790d9f)`
- Node: `v22.23.2` (`C:\Users\CDQ-P\AppData\Local\hermes\node\node.exe`)
- Effective artifact: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
- Effective artifact SHA-256: `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`

| Installed module | SHA-256 |
|---|---|
| `dist/loader-D8d2EvVh.js` | `3a10479bdcbb713692c3ded7dbd5baad27c1b17ae3566172c117d45916dabce7` |
| `dist/registry-B8eQDFB4.js` | `25f3ef82756d85281ad5c25375a5cd2f405989a1145ed438de05992e8c995376` |
| `dist/runtime-D0xGMZdc.js` | `a050a101e3c352345179b77f8c304da99596238fcde95cf03319ebc11dea8791` |
| `dist/hook-runner-global-BmIrGlLG.js` | `c066170e97a2355603f0bdd3079a687bf835632856a741fa9a92683d7d4b2750` |
| `dist/config-state-CtMlHVRM.js` | `af2e3bc003048755d820284d3e01a777fae907aff3be8bc4e281dee663f409c5` |
| `dist/zod-schema-O9ml_nmo.js` | `daca03ca77175870afbb2e32508693ad4641669e417d2a05112669c95d403813` |

These match predecessor evidence; no divergence was found.

## Production fixture provenance

Read-only extraction from `C:\Users\CDQ-P\.openclaw\openclaw.json` used only the relevant entry. The fixture preserved `enabled=true`, the non-secret plugin configuration fields, and `hooks.allowConversationAccess=true`. `workspaceDir` was redirected to the disposable workspace for isolation. The production workspace path was not used by the probe.

Secret-bearing categories were omitted because they were not required by loader registration: credentials/tokens/API keys/passwords and provider secret material. No secret value was printed or copied. Relevant non-secret config included `ticketFirst`, `preInferenceAdmission=true`, `autoWorkflowCompletion`, `enforcedMode`, `autoResume`, bounded polling values, and `providerMode=passthrough`.

Production config SHA-256 was re-established as `19d7e6acf53ce370dc20e5e2a2547c9674c33b178208b79920cb0e9dce9b46b`.

## Isolated method and instrumentation

A temporary copy of the extension was created under `C:\Users\CDQ-P\AppData\Local\Temp\cnx391-*`; only that copy was instrumented. A disposable state/workspace and controller file were created outside `.openclaw`. The real exported `loadOpenClawPlugins` (`loader-D8d2EvVh.js` export `s`) was called with the isolated config and plugin path. No synthetic registry model was used.

The instrumented copy logged entry into `register(api)` and delegated `api.on` calls to the original host function, recording hook name, return type, and throws. Instrumented-copy SHA-256: `18bb0475489acae94b86b46c84bbd4d9cdb6cbbe6ad7652350ce8304545a3386`.

### Case A — production-shaped `true`

- PID: `6468` (single disposable Node process)
- `register(api)`: directly observed
- `api.on("before_agent_run")`: directly observed repeatedly; representative calls returned `undefined`, no throw
- Final plugin status: `loaded`
- Final registry typed hooks: `42`
- `before_agent_run`: present (six occurrences in the final typed-hook names)
- Other accepted hooks included `before_message_write`, `reply_payload_sending`, `session_start`, `agent_end`, `session_end`, `before_tool_call`, `after_compaction`, `reply_dispatch`, `message_sent`, `subagent_spawned`, `subagent_ended`, `model_call_started`, `model_call_ended`, and `before_agent_finalize`
- `hasHooks("before_agent_run")`: the runner accessor was not exposed as a callable in this loader activation shape; final registry inventory is the direct acceptance evidence
- Native policy diagnostic: none emitted in the true run

### Case B — same isolated fixture, `hooks.allowConversationAccess=false`

Executed in a fresh disposable process, PID `16468`, to avoid lifecycle/database state reuse.

- `register(api)`: directly observed
- `api.on("before_agent_run")`: directly observed repeatedly; calls returned `undefined`, no throw
- Final plugin status: `loaded`
- Final registry typed hooks: `29`
- `before_agent_run`: absent
- Other typed hooks remained accepted, including `before_message_write`, `reply_payload_sending`, `session_start`, `session_end`, `before_tool_call`, `after_compaction`, `reply_dispatch`, `message_sent`, `subagent_spawned`, `subagent_ended`, `model_call_started`, and `model_call_ended`
- No false-run native diagnostic was surfaced through the supplied logger; the decisive A/B difference is direct call observation plus final real registry inventory, correlated with the installed `registerTypedHook` source gate.

The control establishes that the instrumentation distinguishes acceptance from rejection: identical plugin-side calls occur, but only the true-policy run stores `before_agent_run` in the real typed-hook registry.

## Host gate and policy evidence

Static source re-verification found `createApi(record, { ..., pluginConfig: validatedConfig.value, hookPolicy: entry?.hooks, registrationMode })` in `loader-D8d2EvVh.js` and `on: (...) => registerTypedHook(record, hookName, handler, opts, params.hookPolicy)` in `registry-B8eQDFB4.js`. The non-bundled gate tests `policy?.allowConversationAccess`; when not `true` it emits the native diagnostic and returns before storage. The A/B inventory result is consistent with this exact gate: true reaches storage; false is rejected before storage. The instrumentation did not patch OpenClaw or intercept private `registerTypedHook` internals.

## Comparison

- **CNX-381:** real loader/API and `api.on` reached the host gate, but false/absent effective policy produced the native non-bundled rejection and no `before_agent_run`. CNX-391 repeats the same boundary with direct positive and control cases.
- **CNX-385:** normalization-only known-good `true` fixture proved `entry.hooks` preservation through normalization and the intended host policy contract. CNX-391 adds real plugin registration acceptance.
- **CNX-390:** production-shaped CLI replay loaded/activated the plugin but exposed neither registration boundary nor gate, so `hookCount=0` was diagnostically blocked. CNX-391 uses disposable instrumentation to expose the boundary.
- **CNX-391:** production-shaped config through exact loader/API path accepted the conversation policy in isolation; false control rejected it.

## Direct evidence versus inference

Direct: exact hashes/version; fixture fields; disposable PIDs; `register(api)` entry; repeated `api.on("before_agent_run")`; no throws; final real typed-hook inventories; A/B difference; plugin loaded status. Inference: the A/B difference is the host `registerTypedHook` policy decision, because installed source binds `hookPolicy` from normalized `entry.hooks` and the false run omits only the targeted conversation hooks. No production process memory was inspected.

## Remaining production uncertainty

This does **not** prove that the production Gateway process accepted the hook. Uncertainty remains about the already-running process's effective in-memory config, lifecycle timing, and registry state. Production CLI absence and `hookCount=0` remain production observations only; they are not overwritten by this isolated acceptance result. Dashboard Ticket-first semantic success is not claimed.

## Counts and compliance

- Semantic/model/provider/Dashboard request count: **0**
- Production mutation count: **0**
- Production Gateway restart/reload: `0`
- Production config mutation: `0`
- Environment mutation: `0`
- Scheduled Task mutation: `0`
- Dependency patch/source repair/artifact replacement/rebuild: `0`
- Production debugger/inspector attachment: `0`
- Permanent or committed instrumentation: `0` (temporary copy only)
- TicketStore/admission/routing/auth changes: `0`
- Historical CNX-360 through CNX-390 edits: `0`
- Force-push/history rewrite/main/tags/releases: `0`
- CNX-392 created/started: `0`

## Closeout

Classification: **`PRODUCTION_CONFIG_REPLAY_ACCEPTS_HOOK_POLICY`** — isolated replay only. Report publication is followed by `ACTIVE.md` and `STATUS.md` set to `WAITING_FOR_CHATGPT_REVIEW`; execution stops here.
