# CNX-367 — OpenAI Dashboard Ticket-first semantic requalification

## Disposition

**Classification: CURRENT_RED**

The one authorized request was sent exactly once from the verified fresh Dashboard session and produced a successful OpenAI response, but the active runtime emitted no durable Ticket-first admission lifecycle. The first observable divergence is immediately after Dashboard input: the runtime went from `prompt.submitted` to `model.completed`, with no `before_agent_run`, admission trace, Ticket, Run lifecycle, or outbox evidence.

This is a diagnosis only. No repair, retry, controller edit, runtime mutation, provider/auth/routing change, reinstall, release/tag change, force-push, or second semantic test was performed.

## GitHub authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Authoritative pre-test HEAD: `916c68ed476943e3fae2a909d1b7dac11fb8f166`
- This report is published as the only change in the follow-up commit; the commit and branch were verified after push.

## Fresh-session identity and pre-send verification

- Session key: `agent:main:dashboard:83027933-3a42-4877-a79a-167caaa396a5`
- Dashboard session UUID: `83027933-3a42-4877-a79a-167caaa396a5`
- Firefox URL: `http://127.0.0.1:18789/chat?session=agent%3Amain%3Adashboard%3A83027933-3a42-4877-a79a-167caaa396a5`
- UI: Firefox / OpenClaw Control; `Ready to chat`; transcript blank; composer `Message Assistant`; composer empty before typing; provider/model pill `GPT-5.6 Luna · Medium`.
- Pre-semantic Dashboard request count: `0`.
- Pre-semantic runtime mutation count: `0`.
- Operator focus was already established by CNX-366; no focus/session/provider/model change was made in this task.

## Exact semantic request

Exactly one message was entered and submitted:

```text
Reply exactly with CNX365-DONE.
```

The field was verified containing the exact text before the single Return submission. No retry and no second send occurred.

## Correlated runtime evidence

The runtime session artifact is:

- Session file: `C:\Users\CDQ-P\.openclaw\agents\main\sessions\7b1a5ad4-0560-4b19-ae4e-609f9492b2c5.jsonl`
- Trajectory: `C:\Users\CDQ-P\.openclaw\agents\main\sessions\7b1a5ad4-0560-4b19-ae4e-609f9492b2c5.trajectory.jsonl`
- Runtime session ID: `7b1a5ad4-0560-4b19-ae4e-609f9492b2c5`
- Run ID: `c3e88413-5199-4d0c-bfec-deb33e86928e`
- traceId: `7b1a5ad4-0560-4b19-ae4e-609f9492b2c5`
- Provider: `openai`
- Model: `gpt-5.6-luna`
- API: `openai-chatgpt-responses`
- Thread ID: `01a0a9a3-21b4-76f3-9613-aee47672410f`
- Turn ID: `01a0a9a3-3583-79a2-87a3-ba59109b47c4`

Recorded trajectory ordering and timestamps:

| Sequence | Event | Timestamp | Evidence |
|---:|---|---|---|
| 1 | `session.started` | `2026-09-16T09:54:00.703Z` | exact session/run/trace/provider/model identity present |
| 2 | `context.compiled` | `2026-09-16T09:54:00.704Z` | same correlation identity |
| 3 | `prompt.submitted` | `2026-09-16T09:54:00.707Z` | exact prompt, thread and turn IDs |
| 4 | `model.completed` | `2026-09-16T09:54:07.458Z` | `timedOut:false`, `aborted:false`, usage recorded, assistant text `CNX365-DONE` |
| 5 | `session.ended` | `2026-09-16T09:54:07.458Z` | status `success` |

The session JSONL records the assistant result as:

- text: `CNX365-DONE`
- provider: `openai`
- model: `gpt-5.6-luna`
- API: `openai-chatgpt-responses`
- stop reason: `stop`
- usage: input `9282`, output `9`, cache read `6912`, total `16203`

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

## First divergence

**First divergence: after Dashboard input / `prompt.submitted`.** The expected next durable event `before_agent_run` and the complete `admission.trace.*` chain are absent. The active runtime proceeds directly to `model.completed` and records the assistant text. Therefore a visible Dashboard response is not being treated as proof of Ticket-first compliance; it is evidence of the bypass.

## Counts and fences

- Dashboard semantic request count: `1`
- OpenAI/model request count: `1` (one correlated successful `model.completed` with OpenAI provider/API)
- Runtime mutation count: `0`
- Retry count: `0`
- Second semantic send: `0`
- New session created: `0`
- Provider/model altered: `0`

## Final disposition and explicit next action

Final disposition: **CURRENT_RED** for the active current runtime. Stop after this diagnosis. The next action is to route the defect to the designated repair/owner workflow, which must add or restore the missing durable Ticket-first admission and lifecycle evidence before any further semantic requalification. Do not run another semantic request in this task.
