# CNX-20260916-370 Live Semantic Requalification Report

## Disposition

**Classification: FAIL / NOT_REQUALIFIED**

The single authorized controlled Dashboard semantic request was sent exactly once from the verified Dashboard session against the repaired runtime from CNX-368/CNX-369. The request produced a successful OpenAI model response (`CNX370-SEMANTIC-ACK`), but the active runtime again emitted **no durable Ticket-first admission lifecycle**. The lifecycle trace is structurally identical to CNX-367's `CURRENT_RED` signature: `prompt.submitted` → `model.completed` with no `before_agent_run`, no `admission.trace.*`, no Ticket, and no Ticket-linked Run/lifecycle/delivery evidence.

This is a requalification diagnosis only. No repair, retry, source change, controller/provider/auth/routing change, release/tag change, force-push, or second semantic test was performed, consistent with the task's hard fences.

## GitHub authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Starting HEAD: `964c4ffea2a9c78342406686d05ba525fc162cda`
- Remote: `https://github.com/funggier/CogentNexus-OpenClaw`

## Canonical runtime identity at requaliability time

| Metric | Value |
|---|---|
| Timestamp (UTC) | `2026-09-16T15:27:27.951381500Z` |
| Remote HEAD SHA | `964c4ffea2a9c78342406686d05ba525fc162cda` |
| Branch tracking | `origin/cnx-357-openai-dashboard-ticket-first-requalification-v2` |
| Gateway PID | `6444` |
| Gateway executable | `C:\Program Files\nodejs\node.exe` |
| Gateway command | `C:\Program Files\nodejs\node.exe C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw\dist\index.js gateway --port 18789` |
| Gateway listening | `127.0.0.1:18789` |
| Installed entrypoint SHA-256 | `04e12be2dc24a8f60c079031737c32bca5990251e8c219066a4413c31eab802b` |
| Repaired entrypoint SHA-256 (CNX-368 target) | `04e12be2dc24a8f60c079031737c32bca5990251e8c219066a4413c31eab802b` |
| Entrypoint match | `True` |
| Controller SHA-256 | `9424cbb2d637b169da975e231a0bf37b3e0925791c74f8e8bb971cf9dd83648f` |
| Controller `cnxMode` | `active` |
| Controller `schemaVersion` | `2` |

The active Gateway process (PID `6444`) is the same process established by CNX-369's bounded `cnxclaw.cmd enable` activation, and it demonstrably loads the repaired artifact whose installed entrypoint SHA-256 still exactly equals the CNX-368 repaired SHA. The semantic request therefore ran against the repaired runtime.

## Pre-request verification

1. **Synchronized with remote** — local HEAD reset to `origin/cnx-357-openai-dashboard-ticket-first-requalification-v2` at `964c4ffe`; tracking clean apart from pre-existing untracked files (`CNX-20260910-…`, `CNX-20260914-331-…`, `CNX-20260914-339-…`, `CNX-20260914-340-…`, `plugins/cogentnexus-openclaw/src/v090-reproducer.test.ts`) that are not part of this task.
2. **Coordination state re-read** — `ACTIVE.md`, `STATUS.md`, and the CNX-370 task spec all authorize this exact task.
3. **Active runtime confirmed as CNX-369-verified** — PID `6444`, entrypoint SHA matches repaired SHA.
4. **Dashboard session identity** — browser address bar showed `http://127.0.0.1:18789/chat?session=agent%3Amain%3Adashboard%3A83027933-3a42-4877-a79a-167caaa396a5`; Firefox tab `OpenClaw Control`; model pill `GPT-5.6 Luna · Medium`; composer empty before entry.

## Exact semantic request

Exactly one message was entered and submitted through the verified Dashboard chat composer:

```text
CNX-370 controlled semantic requalification request: reply exactly CNX370-SEMANTIC-ACK.
```

No retry and no second send occurred. No new session was created. No provider/model/auth/routing change was made.

## Correlated runtime evidence

Runtime session artifact:

- Session file: `C:\Users\CDQ-P\.openclaw\agents\main\sessions\7b1a5ad4-0560-4b19-ae4e-609f9492b2c5.jsonl`
- Trajectory: `C:\Users\CDQ-P\.openclaw\agents\main\sessions\7b1a5ad4-0560-4b19-ae4e-609f9492b2c5.trajectory.jsonl`
- Runtime session ID: `7b1a5ad4-0560-4b19-ae4e-609f9492b2c5`
- Run ID: `7e4cc015-4e3b-4152-bd05-a0a5990a8d27`
- traceId: `7b1a5ad4-0560-4b19-ae4e-609f9492b2c5`
- Provider: `openai`
- Model: `gpt-5.6-luna`
- API: `openai-chatgpt-responses`
- Thread ID: `01a0a9a3-21b4-76f3-9613-aee47672410f`
- Turn ID: `01a0aad2-1754-7ef1-9361-748acf9902da`

Trajectory ordering and timestamps:

| Seq | Event | Timestamp (UTC) | Evidence |
|---:|---|---|---|
| 1 | `session.started` | `2026-09-16T15:24:50.388Z` | exact session/run/trace/provider/model identity |
| 2 | `context.compiled` | `2026-09-16T15:24:50.388Z` | same correlation identity, system prompt and 20 tools compiled |
| 3 | `prompt.submitted` | `2026-09-16T15:24:50.388Z` | exact prompt, thread/turn IDs recorded |
| 4 | `model.completed` | `2026-09-16T15:24:54.525Z` | `timedOut:false`, `aborted:false`, usage input `9319`/output `13`/cacheRead `6912`/total `16244`, assistant text `CNX370-SEMANTIC-ACK` |
| 5 | `session.ended` | `2026-09-16T15:24:54.525Z` | status `success` |

The assistant result is recorded in the session JSONL as text `CNX370-SEMANTIC-ACK`, provider `openai`, model `gpt-5.6-luna`, API `openai-chatgpt-responses`, stop reason `stop`.

## Required Ticket-first lifecycle checks

No records were found for this exact request/session/run/trace for any of the following:

- `before_agent_run`
- `admission.trace.started`
- `admission.trace.input`
- `admission.trace.eligible`
- `admission.trace.ticket-decision`
- `admission.trace.ticket-persisted`
- durable Ticket row or Ticket ID
- ticket event sequence
- Run/lifecycle identity distinct from the direct runtime run
- direct model-call/inference-attempt durable admission evidence
- Result record linked through Ticket-first lifecycle
- assistant-delivery record linked through Ticket-first lifecycle
- outbox row or delivery-completion evidence

The only correlated lifecycle is the five-event trajectory above. It demonstrates direct prompt submission followed by model completion and session completion, not Ticket admission followed by Ticket, Run, Call/Inference, Result, Delivery, and Outbox completion.

No ticket database (`.sqlite`/`.db`) was found under the active `.cogentnexus-openclaw` state root, the `extensions/cogentnexus-openclaw/dist` directory, or the workspace runtime directory. The installed `ticket-store.js`, `admission.js`, `ticket-dispatcher.js` and the `cnx368-ticket-first-admission.test.js` test module all exist on disk (CNX-368 source-level artifacts), but none produced a live admission trace for this request.

## First divergence

**First divergence: after Dashboard input / `prompt.submitted`.** The expected next durable event `before_agent_run` and the complete `admission.trace.*` chain are absent. The active runtime proceeds directly to `model.completed` and records the assistant text. A visible Dashboard response is therefore not proof of Ticket-first compliance; it is evidence that the bypass persists after the CNX-368/CNX-369 repair and activation.

## Comparison with CNX-367 failure signature

| Dimension | CNX-367 (CURRENT_RED) | CNX-370 (this task) |
|---|---|---|
| Session key | `agent:main:dashboard:83027933-…` | `agent:main:dashboard:83027933-…` (same) |
| Trajectory shape | `session.started` → `context.compiled` → `prompt.submitted` → `model.completed` → `session.ended` | identical five-event shape |
| `before_agent_run` | absent | absent |
| `admission.trace.*` | absent | absent |
| Ticket ID | absent | absent |
| Model completion | present (`CNX365-DONE`) | present (`CNX370-SEMANTIC-ACK`) |
| Conclusion | bypass proven | bypass reproduced after repair |

The CNX-368 schema-v2 compatibility repair and the CNX-369 bounded activation demonstrably restored the plugin registration chain at the source/registration level, but they did **not** restore the live Dashboard → Ticket-first admission path. The semantic behavior is unchanged from CNX-367.

## Counts and fences

- Dashboard semantic request count: `1`
- OpenAI/model request count: `1` (one correlated successful `model.completed` with OpenAI provider/API)
- Runtime mutation count: `0`
- Retry count: `0`
- Second semantic send: `0`
- New session created: `0`
- Provider/model altered: `0`
- Source-code changes: `0`
- Configuration redesign / controller normalization: `0`
- Provider/auth/routing changes: `0`
- Historical CNX-360–CNX-369 edits: `0`
- Release/tag/main changes: `0`
- Force-push or history rewrite: `0`

## Hard-fence compliance

- ✅ One minimum-necessary controlled Dashboard semantic request only; no CNX-367 retry or reproduction.
- ✅ No source-code changes.
- ✅ No configuration redesign or controller normalization.
- ✅ No provider/auth/routing changes.
- ✅ No unrelated Dashboard/model traffic.
- ✅ No repeated CNX-367 reproduction.
- ✅ No historical edits to CNX-360 through CNX-369.
- ✅ No release/tag/main changes.
- ✅ No force-push or history rewrite.
- ✅ No repair work performed; publishing evidence and stopping as required.

## Final disposition and explicit next action

Final disposition: **FAIL / NOT_REQUALIFIED** for the repaired runtime. The Dashboard Ticket-first admission path is not restored at the semantic level. Stop after this report. The next action is to route the defect to a separate, explicitly authorized repair task that addresses the live admission path (not just the source-level registration chain) before any further semantic requalification. Do not run another semantic request in this task.

---
*Report generated by Hermes Agent for CNX-20260916-370*
*Execution discipline: remote sync → authoritative state re-read → runtime identity verification → one controlled Dashboard request → correlated runtime evidence capture → comparison with CNX-367 → FAIL classification → report publication*
*Strict hard-fence compliance: Dashboard=1, OpenAI/model=1, retries=0, runtime mutations=0, source changes=0, no force-push, no repair*
