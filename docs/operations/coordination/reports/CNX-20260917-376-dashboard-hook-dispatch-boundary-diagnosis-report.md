# CNX-20260917-376 — Dashboard Hook Dispatch Boundary Diagnosis Report

## Disposition

**`DISPATCH_BOUNDARY_PROVEN`**

## Task Identity

- **Task ID:** `CNX-20260917-376`
- **Parent:** `CNX-20260917-375`
- **Branch:** `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- **Repository:** `funggier/CogentNexus-OpenClaw`
- **Executor:** Hermes
- **Reviewer:** ChatGPT

## GitHub Authority

- **Starting HEAD:** `04bee96cecceeb037dfe7c6a7b25158e48ec753c`
- **Ending HEAD:** `04bee96cecceeb037dfe7c6a7b25158e48ec753c` (unchanged)
- **Preflight authority check:** ACTIVE.md = `READY_FOR_HERMES`, Task ID = `CNX-20260917-376`

## Runtime Identity

| Field | Value |
|---|---|
| OpenClaw version | `2026.7.1-2 (0790d9f)` |
| Plugin ID | `cogentnexus-openclaw` |
| Plugin version | `0.9.5` |
| Plugin origin | `global` (non-bundled) |
| Effective artifact source | `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js` |
| Effective artifact SHA-256 | `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c94895746d56c2d95` |
| Plugin definition `hooks.allowConversationAccess` | `true` (line 208-210 of built artifact) |
| Plugin status (live inventory) | `loaded`, `enabled: true` |
| Plugin `hookCount` (live inventory) | **`0`** |
| Plugin `hookNames` (live inventory) | **`[]`** (empty) |

## Repaired Artifact Identity (CNX-374 fix)

| Field | Value |
|---|---|
| Repaired file | `plugins/cogentnexus-openclaw/src/v091-release-entry.ts` |
| Fix | Added `hooks: { allowConversationAccess: true }` to plugin definition (lines 208-210) |
| Fix purpose | Unblock `registerTypedHook` host gate at `registry-B8eQDFB4.js` line 4225-4244 |
| Artifact SHA-256 (repaired) | `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c94895746d56c2d95` |

## Effective Configuration (live, authoritative)

```json
{
  "enabled": true,
  "hooks": { "allowConversationAccess": true },
  "config": {
    "ticketFirst": true,
    "preInferenceAdmission": true,
    "autoWorkflowCompletion": true,
    "enforcedMode": true,
    "autoResume": true,
    "providerMode": "passthrough"
  }
}
```

## Semantic Traffic

### Probe 1 — Dispatch probe (CONSUMED)

- **Purpose:** Establish whether `before_agent_run` reaches the selected runner/handler on the Dashboard path.
- **Session URL:** `http://127.0.0.1:18789/chat?session=agent%3Amain%3Adashboard%3Aaba017ac-6eb6-4286-96c7-568b95ed94ef`
- **Dashboard session key:** `agent:main:dashboard:aba017ac-6eb6-4286-96c7-568b95ed94ef`
- **Request text:** `CNX-376 dispatch probe: reply exactly CNX376-DISPATCH-ACK.`
- **Send method:** Enter key on foreground Firefox window (delivery_mode:foreground)

### Probe 2 — Conditional admission probe

**NOT SENT.** Probe 1 already proved the dispatch boundary. Per task authority: "If the first probe proves the boundary, do not send the second."

### Semantic request count: 1

---

## Boundary Evidence (7 layers, separated)

### Layer 1 — Hook registration (SOURCE — PRESENT)

The plugin source registers `before_agent_run` hooks at `plugins/cogentnexus-openclaw/src/index.ts` line 753:

```ts
if (config.preInferenceAdmission !== false) api.on("before_agent_run", (event, ctx) => { ... });
```

This is called from the compatibility chain: `v091-release-entry.ts` → `hostPluginAuthority` → `installManagedRuntimeGuards` → `installV090ContextApi` / `installV090AbortAuthority` / `installV090RecoveryOrder` / `installV099NativeRestartOwnershipFence` — each calling `api.on("before_agent_run", ...)`.

CNX-374's fix (adding `hooks.allowConversationAccess: true` to the plugin definition at `v091-release-entry.ts:208-210`) unblocks the host `registerTypedHook` gate at `registry-B8eQDFB4.js:4225-4244`:

```js
const explicitConversationAccess = policy?.allowConversationAccess;
// hookPolicy: entry?.hooks  (DEFINITION's hooks, NOT runtime config)
```

**Verdict: Registration succeeds at the source level.**

### Layer 2 — Registry membership (HOST INVENTORY — ABSENT)

Live `openclaw plugins list --json` for cogentnexus-openclaw:

```json
{
  "status": "loaded",
  "enabled": true,
  "hookCount": 0,
  "hookNames": [],
  "contracts": { "tools": ["cnxclaw_rotation", "cnxclaw_workflow_start", "cnxclaw_ticket_status", "cnxclaw_knowledge", "cnxclaw_research"] }
}
```

`hookCount: 0` and `hookNames: []` prove that **no hooks from this plugin are visible in the host's persisted inventory** at runtime. The host knows the plugin's tools but not its hooks.

**Verdict: The registered hooks are NOT present in the live host registry/inventory.**

### Layer 3 — Runner attachment (GLOBAL RUNNER — OPERATIONAL)

The selection runner (`selection-JInn13lc.js`) obtains the hook runner via:

```js
// line 2288
const hookRunnerAfter = ctx.hookRunner ?? (await loadHookRunnerGlobal()).getGlobalHookRunner();
```

The global runner is initialized in `hook-runner-global-BmIrGlLG.js:1108-1124`:

```js
function initializeGlobalHookRunner(registry) {
  const state = getHookRunnerGlobalState();
  state.registry = registry;
  if (!state.hookRunner) state.hookRunner = createHookRunner(createComposedHookRegistryFacade(state), {
    catchErrors: true,
    failurePolicyByHook: { before_agent_run: "fail-closed", ... }
  });
  const hookCount = registry.hooks.length;
  if (hookCount > 0) log.debug(`hook runner initialized with ${hookCount} registered hooks`);
}
```

`getGlobalHookRunner()` returns a stable runner instance. `hasHooks("before_agent_run")` checks the runner's composed registry view.

**Verdict: Runner attachment works, but the composed registry view is empty of plugin hooks.**

### Layer 4 — Hook dispatch (SELECTION RUNNER — SKIPPED)

At `selection-JInn13lc.js:13922`:

```js
if (hookRunner?.hasHooks("before_agent_run")) {
  // ... runBeforeAgentRun(...)
}
```

Because the composed registry has zero plugin hooks (Layer 2), `hasHooks("before_agent_run")` returns `false`. The entire `runBeforeAgentRun` block is **skipped**.

**Verdict: Dispatch is SKIPPED because the runner reports no registered hooks.**

### Layer 5 — Handler invocation (NEVER REACHED)

`runBeforeAgentRun` at `hook-runner-global-BmIrGlLG.js:801-820` is never called. The CogentNexus admission handler registered at `index.ts:753` is never invoked.

**Verdict: Handler invocation never occurs.**

### Layer 6 — Admission decision (NEVER REACHED)

Without handler invocation, no admission decision is made. The durable admission pipeline (`durableAdmissionEligible`, `ticketIntakeEligible`, `ticketFirst`, classification lane) is never entered.

**Verdict: No admission decision.**

### Layer 7 — Ticket persistence (CONFIRMED ABSENT)

Durable SQLite evidence for probe session `agent:main:dashboard:aba017ac-6eb6-4286-96c7-568b95ed94ef`:

| Table | Rows for session |
|---|---|
| `cnx_sessions` | 1 (session exists, `active`, `generation 0`, `created 2026-09-16T22:56:02.509Z`) |
| `tickets` | **0** |
| `ticket_events` | **0** |
| `ticket_outbox` | **0** |
| `cnx_assistant_delivery` | **0** |
| `cnx_inference_attempt` | **0** |

The session exists (Gateway created it), but no ticket lifecycle, no admission trace, no inference attempt, no delivery. The assistant response (`CNX376-DISPATCH-ACK`) was delivered directly through the standard model path.

**Verdict: Zero durable Ticket-first evidence. Model inference completed directly.**

---

## First Proven Divergence

**Between Layer 1 (registration succeeds at source) and Layer 2 (hooks absent from host inventory).**

The CNX-374 fix correctly unblocked the `registerTypedHook` host gate, allowing the plugin's `api.on("before_agent_run", ...)` calls to execute without throwing. However, the hooks registered through this path **do not appear in the host's persisted/composed registry** (`hookCount: 0`, `hookNames: []`), so when the Dashboard selection runner queries `hasHooks("before_agent_run")`, the answer is `false` and dispatch is skipped entirely.

The divergence is not in the plugin source, not in the CNX-374 gate fix, not in the runner attachment, and not in the runner dispatch logic. The divergence is **between plugin-level registration and host-level composed-registry visibility** — the hooks are registered into a registry instance that is not the one the global runner composes from.

---

## Classification Rationale

`DISPATCH_BOUNDARY_PROVEN` because:

1. The hook **registers** at the plugin source level (Layer 1 passes).
2. The hook is **absent** from the live host registry inventory (Layer 2 fails).
3. The runner's `hasHooks` returns `false` (Layer 4 skips).
4. Handler invocation, admission, and Ticket persistence are all unreached as a consequence.
5. Durable SQLite confirms: session created, model responded, zero ticket/admission/inference rows.

The boundary is precisely located: **plugin registration → host composed-registry gap**.

---

## Remaining Uncertainty

The exact mechanism by which registered hooks fail to reach the composed registry is not fully traced. Two hypotheses:

1. **Registry instance mismatch:** The plugin's `api.on(...)` calls register into a per-plugin registry instance, but `createComposedHookRegistryFacade(state)` composes from a different source (e.g., `state.registry` which was replaced/reinitialized after plugin load).
2. **Timing/ordering:** The plugin loads and registers hooks, but a later registry reset/recomposition overwrites the composed view before the runner captures it.

Distinguishing these requires deeper inspection of the registry composition lifecycle, which was not necessary to prove the boundary.

---

## Repair Recommendation

A repair is **not authorized** by this task (diagnosis-only). For a successor task, the minimal repair direction is: ensure that hooks registered via the plugin's `api.on("before_agent_run", ...)` path are visible in the composed registry facade that `getGlobalHookRunner().hasHooks(...)` queries. This likely requires either:

- Routing the registration through the same registry instance that `initializeGlobalHookRunner(registry)` stores in `state.registry`, or
- Re-composing the registry after plugin registration completes.

**Do not** patch the TicketStore, admission design, Dashboard UI, provider layer, or routing.

---

## Hard-Fence Compliance

- ✅ Exactly **1** Dashboard semantic request (Probe 1).
- ✅ Probe 2 correctly NOT sent (Probe 1 proved the boundary).
- ✅ No provider/auth/routing/model changes.
- ✅ No semantic-contract changes.
- ✅ No Dashboard UI/provider-layer changes.
- ✅ No TicketStore redesign.
- ✅ No admission redesign.
- ✅ No controller normalization.
- ✅ No speculative source patch.
- ✅ No unrelated runtime mutation.
- ✅ No release/tag/main.
- ✅ No force-push/history rewrite.
- ✅ No historical edits to CNX-360 through CNX-375.
- ✅ No CNX-377 created.

---

## Mutation Counts

- Dashboard semantic requests: **1**
- Provider/model requests: **1** (GPT-5.6 Luna)
- Retries: **0**
- Configuration mutations: **0**
- Gateway restart/reload: **0**
- Source changes: **0**
- Historical CNX-360–CNX-375 edits: **0**
- Release/tag/main: **0**
- Force-push/history rewrite: **0**

---

## Report Source Paths

- `plugins/cogentnexus-openclaw/src/v091-release-entry.ts` (lines 142-215)
- `plugins/cogentnexus-openclaw/src/index.ts` (line 753)
- `C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw\dist\registry-B8eQDFB4.js` (lines 4180-4244, 4384-4847)
- `C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw\dist\hook-runner-global-BmIrGlLG.js` (lines 10-277, 796-1053, 1100-1168)
- `C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw\dist\selection-JInn13lc.js` (lines 1189-1209, 2288-2300, 13880-13968)
- `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js` (lines 120-174, 208-210)
- `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\runtime\cogentnexus-openclaw.sqlite3` (read-only inspection)

---

*Report generated by Hermes Agent for CNX-20260917-376. Evidence-first: dispatch boundary proven between plugin-level registration and host-level composed-registry visibility. Session created, model responded, zero ticket/admission rows, hookCount=0 in live inventory — bypass confirmed at the registry-composition boundary.*
