# CNX-20260916-372 — Selection Runner Hook Registry Runtime Observation

## Disposition

**INCONCLUSIVE — supported read-only runtime observation could not attach to the live selection-runner boundary. No repair, mutation, or semantic requalification was performed.**

The supported host diagnostics establish the live Gateway process, installed version, plugin inventory, and effective artifact identity. They do not expose the process-local `runEmbeddedAttempt` frame, `hookRunner` reference, the selection runner's effective registry, or invocation/return telemetry. The evidence therefore cannot distinguish `REGISTRY_ABSENT`, `HOOK_NOT_REGISTERED`, `DISPATCH_SUPPRESSED`, or `DISPATCH_REACHED`.

## GitHub authority and synchronization

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch requested: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Starting remote HEAD after fetch: `c26f11c0628933ef2f6adbddcd7305292fe5392e`
- Final remote HEAD before publication: `c26f11c0628933ef2f6adbdd7305292fe5392e` (verified before commit)
- Initial checkout was detached at the fetched remote tip.
- Pre-existing untracked files were preserved and were not part of this task.
- Authoritative `ACTIVE.md`, `STATUS.md`, CNX-372 task specification, CNX-371 report, and CNX-370 report were read from the fetched tip before observation.

## Observation method

### Supported methods attempted

1. Read-only `openclaw gateway status --json` against the existing Gateway.
2. Read-only `openclaw --version`.
3. Read-only `openclaw plugins list --json`.
4. Read-only process/listener inspection (`PID`, executable, command line, and port).
5. Read-only effective artifact hashing and installed-source inspection.
6. Read-only inspection for an already enabled Node inspector/diagnostic endpoint and for documented runtime hook diagnostics.

No undocumented RPC was invented or fuzzed. No debugger was attached because the running process exposed no already-enabled inspector endpoint, and enabling one would require a lifecycle/runtime mutation not authorized by this task. No controlled Dashboard request was sent because no supported observation interface was available that required one.

### Runtime mutation and semantic request counts

- Runtime mutations: `0`
- Gateway restart/reload: `0`
- Plugin reinstall/reload: `0`
- Configuration changes: `0`
- Dashboard semantic requests: `0`
- Provider/auth/routing/model changes: `0`
- Persistent monkey patches: `0`
- Source changes before this report: `0`

## Process identity and effective runtime

Observation timestamp: `2026-09-16T16:19:53.071Z`.

| Field | Observed value |
|---|---|
| Gateway PID | `6444` |
| Executable | `C:\\Program Files\\nodejs\\node.exe` |
| Command | `C:\\Program Files\\nodejs\\node.exe C:\\Users\\CDQ-P\\AppData\\Roaming\\npm\\node_modules\\openclaw\\dist\\index.js gateway --port 18789` |
| Listener | `127.0.0.1:18789` |
| Gateway state | `Ready`, RPC `ok: true` |
| OpenClaw version | `2026.7.1-2 (0790d9f)` |
| Gateway reported version | `2026.7.1-2` |
| RPC capability | `connected_no_operator_scope` |
| Effective plugin | `cogentnexus-openclaw`, version `0.9.5`, status `loaded`, enabled `true` |
| Effective plugin source | `C:\\Users\\CDQ-P\\.openclaw\\extensions\\cogentnexus-openclaw\\dist\\v091-release-entry.js` |
| Gateway service command source | `C:\\Users\\CDQ-P\\.openclaw\\gateway.cmd` |

The process and version remained stable during the read-only observations.

## Effective artifact hashes

| Artifact | SHA-256 |
|---|---|
| `openclaw/dist/index.js` | `9832720dcaf85519d315dda624497e352588f0d65c5607390df0501cc2358985` |
| `openclaw/dist/message-handler-CzwI6JjW.js` | `ce8653d5e612bb6b3ec28eb57b9762303de4ca3eeee8b41397d76e77604ef121` |
| `openclaw/dist/agent-D6kiZtPt.js` | `06a0b478abf02cdb542cc14a3641b57def58677d8d6eadd0ffe58ac063f940df` |
| `openclaw/dist/selection-JInn13lc.js` | `ccff13111aa60369ac9d88b526a58a7df1f733f1d99d205c01c6186036957e66` |
| `.openclaw/extensions/cogentnexus-openclaw/dist/v091-release-entry.js` | `04e12be2dc24a8f60c079031737c32bca5990251e8c219066a4413c31eab802b` |

The installed `selection-JInn13lc.js` contains the statically identified `runEmbeddedAttempt` boundary and the `hookRunner?.hasHooks("before_agent_run")` / `runBeforeAgentRun(...)` dispatch site described by CNX-371. This is static installed-artifact evidence, not runtime invocation evidence.

## Plugin registration inventory versus hook registry

The supported `plugins list --json` result reports the CogentNexus plugin as loaded and enabled, with its effective source path and version. Its inventory fields report:

- `hookNames: []`
- `hookCount: 0`
- `diagnostics: []`

This is host plugin inventory evidence only. It does **not** prove that the selection runner's `hookRunner` is absent, that the runner registry is empty, that `hasHooks("before_agent_run")` returned false at runtime, or that the registry reference used by the runner is the same registry represented by the inventory command. It also does not prove invocation or non-invocation of `runBeforeAgentRun(...)`.

The three claims remain separate:

1. **Plugin registered/loaded:** supported inventory says loaded and enabled.
2. **Runner hook registry contains `before_agent_run`:** not exposed by supported diagnostics.
3. **`runBeforeAgentRun(...)` invoked:** no runtime invocation evidence was exposed.

## Required boundary evidence

| Required fact | Evidence result |
|---|---|
| Selected runner identity | Static source identifies the candidate embedded selection runner; live selected runner not exposed. **Unproven.** |
| Exact `runEmbeddedAttempt` execution | Static function/site exists; no live frame/call event. **Unproven.** |
| `hookRunner` presence | Not exposed. **Unknown.** |
| `hookRunner` type | Not exposed. **Unknown.** |
| `hasHooks("before_agent_run")` result | Not exposed. **Unknown.** |
| Registry/plugin snapshot at boundary | Host inventory exists, but runner snapshot/reference is not exposed. **Unknown.** |
| `runBeforeAgentRun(...)` invoked | No invocation telemetry; no live request was issued. **Unknown.** |
| Return/decision | Not observable. **Unknown.** |
| sessionKey/sessionId/runId/trace correlation | None created by this observation; no controlled execution was authorized or required. **Not applicable / unavailable.** |
| Ordering relative to model execution | No new execution performed. CNX-370's prior trajectory is not reused as CNX-372 runtime-boundary evidence. |

## Runner/path assessment

- Static installed source remains consistent with CNX-371's candidate path: Dashboard Gateway agent → embedded selection runner → `runEmbeddedAttempt`.
- The read-only runtime status did not expose a different live runner or path.
- Absence of a live path observation is not evidence of a mismatch.
- `RUNNER_PATH_MISMATCH` is therefore not justified.

## Boundary classification

**`INCONCLUSIVE`**.

Evidence does not distinguish:

- `REGISTRY_ABSENT`;
- `HOOK_NOT_REGISTERED`;
- `DISPATCH_SUPPRESSED`; or
- `DISPATCH_REACHED`.

`DISPATCH_REACHED` cannot be claimed merely because the installed source contains a dispatch call. Likewise, loaded plugin inventory and `hookCount: 0` cannot be promoted to a runner-boundary `HOOK_NOT_REGISTERED` finding.

## Diagnostic finding only

The supported host/runtime diagnostic surface does not provide process-local selection-runner hook-boundary observability. A future task may need an approved, non-production diagnostic attachment or a host-supported runtime event interface that exposes the actual runner reference, registry identity/membership, and invocation decision. This is a diagnostic finding only. **No repair target was implemented or selected in CNX-372.**

## Hard-fence compliance

- No production source changes.
- No provider, auth, routing, or model changes.
- No configuration redesign or controller normalization.
- No Dashboard UI or provider-layer changes.
- No plugin reinstall/reload.
- No Gateway restart/reload.
- No semantic Dashboard request or semantic requalification.
- No repeated Dashboard request.
- No edits to CNX-360 through CNX-371 reports.
- No release/tag/main change.
- No force-push or history rewrite.
- No guessed repair.
- Runtime mutations remained `0`.

## Final state

After this report is published, coordination state is set to `WAITING_FOR_CHATGPT_REVIEW`. No repair task or semantic requalification task is created. Execution stops at the observation boundary.
