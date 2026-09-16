# CNX-20260917-375 — Dashboard Ticket-first Semantic Requalification Report

## Disposition

**`FAIL / TICKET_FIRST_STILL_BYPASSED`**

## Task Identity

- **Task ID:** `CNX-20260917-375`
- **Parent:** `CNX-20260916-374`
- **Branch:** `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- **Repository:** `funggier/CogentNexus-OpenClaw`
- **Executor:** Hermes
- **Reviewer:** ChatGPT

## GitHub Authority

- **Starting/Ending HEAD (repo):** `27cf7aed46411a1b599cb4437b9aaae66bb2fb00`
- **Preflight authority check:** ACTIVE.md = `READY_FOR_HERMES`, Task ID = `CNX-20260917-375`
- **Task spec path:** `docs/operations/coordination/tasks/CNX-20260917-375-dashboard-ticket-first-semantic-requalification.md`

## Runtime Identity

| Field | Value |
|---|---|
| Gateway PID (live, post-activation) | `27372` |
| OpenClaw version | `2026.7.1-2 (0790d9f)` |
| Plugin ID | `cogentnexus-openclaw` |
| Plugin version | `0.9.5` |
| Plugin origin | `global` (non-bundled) |
| Effective artifact source | `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js` |
| Effective artifact SHA-256 | `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95` |
| Plugin definition `hooks.allowConversationAccess` | `true` (line 174 of built artifact) |
| Gateway listener | `127.0.0.1:18789` |
| Dashboard provider | GPT-5.6 Luna · Medium |

## Repaired Artifact Identity (CNX-374 fix)

| Field | Value |
|---|---|
| Repaired file | `plugins/cogentnexus-openclaw/src/v091-release-entry.ts` |
| Fix | Added `hooks: { allowConversationAccess: true }` to plugin definition |
| Artifact SHA-256 (repaired) | `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95` |

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

## Controlled Semantic Request

- **Request count:** `1` (one single Dashboard submission)
- **Request text:** `CNX-375 controlled semantic requalification request: reply exactly CNX375-SEMANTIC-ACK`
- **Session URL:** `http://127.0.0.1:18789/chat?session=agent%3Amain%3Adashboard%3Ad4742ca0-1cef-43fc-b54c-0ed1a89853c0`
- **Dashboard session key:** `agent:main:dashboard:d4742ca0-1cef-43fc-b54c-0ed1a89853c0`
- **Dashboard session state (in `cnx_sessions`):** `active`, generation `0`, created `2026-09-16T22:30:10.463Z`
- **Send method:** Enter key on foreground Firefox window

## Observed Event Trajectory (Chronological)

| # | Time | Event | Evidence |
|---|---|---|---|
| 1 | T-0 | Session created in `cnx_sessions` | `session_key=agent:main:dashboard:d4742ca0...`, state=`active` |
| 2 | T-0 | User message sent via Dashboard UI | Screenshot shows message in composer + "Assistant is responding..." |
| 3 | T+~45s | Model response visible: "CNX375-SEMANTIC-ACK" | Dashboard screenshot confirms assistant bubble |
| 4 | — | **NO admission trace events** | `ticket_events` table empty for this session |
| 5 | — | **NO new ticket** | `tickets` table latest is still `CNXT-09dd6f84` (CNX-339, 14 Sep) |

## Missing/Blocked Evidence

| Required Evidence | Observed |
|---|---|
| `session.started` | ✅ session exists in `cnx_sessions` |
| `context.compiled` | not captured |
| `prompt.submitted` | not captured |
| `before_agent_run` hook evidence | ❌ **MISSING** |
| `admission.trace.started` | ❌ **MISSING** |
| `admission.trace.input` | ❌ **MISSING** |
| `admission.trace.eligible` | ❌ **MISSING** |
| `admission.trace.ticket-decision` | ❌ **MISSING** |
| `admission.trace.ticket-persisted` | ❌ **MISSING** |
| `admission.trace.blocked` | ❌ **MISSING** |
| `admission.trace.completed` | ❌ **MISSING** |
| Ticket creation | ❌ **NO NEW TICKET** |
| Ticket acceptance event | ❌ **MISSING** |
| Ticket routing | ❌ **MISSING** |
| pre-inference block | ❌ **NOT EVIDENT** |
| `model.completed` (UI only) | ✅ model responded with "CNX375-SEMANTIC-ACK" |
| `session.ended` | not captured |

## Ticket-first Evidence

- **Ticket ID:** *none created for this request*
- **Ticket acceptance:** *N/A*
- **Durable admission fingerprint:** *none*
- **Persistence:** `tickets`, `ticket_events`, `ticket_outbox` all empty for session `d4742ca0...`
- **Routing/dispatch:** *none*
- **Blocked-before-inference result:** *none — inference completed directly*

## Bypass Detection

| Check | Result |
|---|---|
| `model.completed` BEFORE Ticket-first block | ✅ **YES** — direct model inference occurred |
| Direct model execution without admission | ✅ **YES** |
| Second inference attempt | no evidence |
| Retry | no evidence |
| Fallback bypassing `before_agent_run` | not distinguished |

**Diagnosis:** The request produced a model response ("CNX375-SEMANTIC-ACK") but left **no durable admission or ticket lifecycle evidence**. The durable `cogentnexus-openclaw.sqlite3` shows no `tickets`, `ticket_events`, or `cnx_assistant_delivery` rows for the new session. The CNX-374 registry-wiring fix (enabling `before_agent_run` hook registration) did not restore the Ticket-first admission boundary at runtime.

## Classification Rationale

The decisive evidence is:

1. A fresh Dashboard session was created (`cnx_sessions` row present).
2. A semantic request was submitted once through the UI.
3. A model response was delivered.
4. **No ticket lifecycle was created** (`tickets` table has no row for this session; `ticket_events` is empty; `ticket_outbox` is empty).
5. **No `admission.trace.*` records** were produced.
6. The request reached ordinary model inference directly.

This is the original CNX-370 bypass pattern: direct inference without Ticket-first admission. The CNX-374 registry-wiring repair (allowing `before_agent_run` hook to register) was necessary but not sufficient — the Dashboard request path still executes model inference without the Ticket-first admission boundary.

## Mutation Counts

- Dashboard semantic requests: **1**
- Provider/model requests: **1** (GPT-5.6 Luna)
- Retries: **0**
- Configuration mutations: **0**
- Gateway restart/reload: **0** (already on repaired PID 27372)
- Source changes: **0**
- Historical CNX-360–CNX-373 edits: **0**
- Release/tag/main: **0**
- Force-push/history rewrite: **0**

## Hard-Fence Compliance

- ✅ Exactly one Dashboard semantic request.
- ✅ No repeated Dashboard traffic.
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
- ✅ No historical edits to CNX-360 through CNX-374.
- ✅ No CNX-376 created.

## Remaining Uncertainty

1. **Hook runtime registration state:** The `openclaw plugins list --json` inventory was not recaptured immediately after this task. The focused unit test (cnx374-registry-wiring.test.ts) still passes; the installed artifact still carries the fix (SHA-256 match). The gap is between "hook registers in plugin unit tests" and "Dashboard path invokes the registered hook" — that gap persists.

2. **Provider-specific path:** Dashboard selection runner may use a different hook dispatch for webchat/Dashboard than the path the CNX-374 unit-test exercises. The `selection-JInn13lc.js` dispatch was not observed at runtime.

3. **No debug-level Gateway log capture:** `admission.trace.*` events, if emitted at debug/trace level, may not appear in the standard `openclaw-2026-09-17.log` tail filtered here. The durable SQLite record (authoritative for ticket lifecycle) is definitive: no ticket was created.

## Recommendation

The CNX-374 registry-wiring fix does not restore Dashboard Ticket-first behavior end-to-end. A successor task should:

1. Determine whether the `before_agent_run` hook is actually dispatched on the Dashboard/WebChat selection-runner path (not just registerable).
2. If dispatched, inspect why Ticket-first gating does not trigger despite `ticketFirst=true`, `preInferenceAdmission=true`, `enforcedMode=true`.
3. If not dispatched, identify the owning boundary (likely in `selection-JInn13lc.js` / embedded selection runner) and route around it with minimal mutation.

Do **not** send another semantic request under this task authority.

---

*Report generated by Hermes Agent for CNX-20260917-375. Evidence-first: one Dashboard request, fresh session, durable lifecycle inspected, no ticket created, model inference direct — bypass confirmed.*
