# CNX-343 — Live Timeout Requalification Report

- **Task:** CNX-343
- **Verdict:** `PASS — pending independent ChatGPT review`
- **Execution boundary:** one semantic request in the specified existing Dashboard session; no retry, resend, recovery, fallback, manual dispatch, reinstall, rebuild, or Gateway restart
- **Report timestamp:** 2026-09-14T14:12:00Z

## Observed facts

### Preflight

- Firefox window: `OpenClaw Control — Mozilla Firefox`
- Firefox PID: `17040`
- Current Dashboard URL: `http://127.0.0.1:18789/chat?session=agent%3Amain%3Adashboard%3A945504d3-42f1-497a-b635-9975561e4bd5`
- Session identity: `agent:main:dashboard:945504d3-42f1-497a-b635-9975561e4bd5` — exact match
- Gateway PID: `17080`
- Gateway process start evidence: `2026-09-14 16:53:15 +07` (read-only process probe)
- Provider/model selected in Dashboard: `ollama / qwen3.8:27b`
- Configured defaults observed read-only: `agents.defaults.timeoutSeconds=2700`; `models.providers.ollama.timeoutSeconds=2700`
- Durable baseline immediately before this request: `tickets=22`, `ticket_events=854`, `ticket_outbox=0`, `cnx_direct_model_call=19`, `cnx_inference_attempt=2`; the database had 23 tickets after acceptance and 858 events after the request lifecycle.

Post-CNX-342 artifact/load evidence was read without mutation:

- Installed root: `C:/Users/CDQ-P/.openclaw/extensions/cogentnexus-openclaw`
- CNX-342 repair commit: `460a8cd661d02ba419cc1eff13c0efc721cfa928`
- Installed entry: `dist/v091-release-entry.js`, SHA-256 `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8`
- Installed lease: `dist/v091-direct-model-call-lease.js`, SHA-256 `5380b34e477979fdb3ad9154728eba0a86a3fafca089e1b997df7dba4dc893ab`
- CNX-342 evidence records that both installed hashes equal the exact-build hashes, the repaired resolver is present, exactly one Gateway restart loaded the installed artifact, the post-restart Gateway was healthy, and no semantic traffic occurred during installation.

### Exactly one semantic request

The only request sent in this task was:

```text
CNX-343-LIVE-TIMEOUT-REQUALIFICATION: Reply exactly with DONE.
```

The Dashboard displayed the request and the final visible response `DONE` with a native-dashboard delivery marker. No second request was sent.

### Durable lifecycle correlation

Read-only source database:

`C:/Users/CDQ-P/.openclaw/workspace/.cogentnexus-openclaw/runtime/cogentnexus-openclaw.sqlite3`

| Entity | Observed value |
|---|---|
| Session ID | `agent:main:dashboard:945504d3-42f1-497a-b635-9975561e4bd5` |
| Ticket ID | `CNXT-09dd6f84-a7f8-44fe-b4bc-6dbc3324b551` |
| Run ID | `4b3dc204-f7e7-45e3-a228-9b437eb75530` |
| Call ID | `4b3dc204-f7e7-45e3-a228-9b437eb75530:model:1` |
| Inference attempt ID | `cnx-attempt-2c96ac81-09ba-4fcb-bb38-f255aad86f09` |
| Session generation | `0` |
| Provider | `ollama` |
| Model | `qwen3.8:27b` |
| `startedAt` (direct call) | `2026-09-14T14:07:47.794Z` |
| `deadlineAt` | `2026-09-14T14:52:47.794Z` |
| `timeoutMs` | `2700000` |
| `endedAt` (direct call) | `2026-09-14T14:11:19.169Z` |
| `durationMs` | `211376` |
| Inference attempt state/outcome | `ended / completed` |
| Final ticket status | `completed` |
| Delivery confirmation | `2026-09-14T14:11:19.209Z`, source `native-dashboard-marker`, `deliveryConfirmed=true` |
| Final outbox count | `0` |

The corresponding durable event sequence is one correlated lifecycle:

`accepted` → `routed` → `direct_model_call_started` → `inference_attempt_started` → `direct_model_call_ended` → `inference_attempt_ended` → `response_ready` → `direct_response_durable` → `delivery_confirmed` → `completed`.

The `direct_model_call_started` event records:

```json
{"runId":"4b3dc204-f7e7-45e3-a228-9b437eb75530","callId":"4b3dc204-f7e7-45e3-a228-9b437eb75530:model:1","provider":"ollama","model":"qwen3.8:27b","deadlineAt":"2026-09-14T14:52:47.794Z","timeoutMs":2700000,"source":"openclaw-model-call-hook"}
```

The `inference_attempt_started` event records the same Ticket/session/call lifecycle and provider/model, with the attempt ID above.

### Timeout arithmetic

- `startedAt`: `2026-09-14T14:07:47.794Z`
- `deadlineAt`: `2026-09-14T14:52:47.794Z`
- Difference: exactly **45 minutes = 2,700,000 ms**
- Recorded `timeoutMs`: **2,700,000 ms**
- No `timeoutMs=900000` was present for this Ticket, Run, Call, or inference attempt.

Independent integer check: `2700 seconds × 1000 = 2700000 ms`.

### Duplicate and protected-state checks

- One Ticket for the exact request and session; one Run; one Call; one inference attempt.
- No duplicate owner/call row was observed for this request.
- `ticket_outbox` final count: `0`.
- No retry/resend/recovery/fallback/manual dispatch was observed in the correlated lifecycle.
- No production source/test file, provider, model, timeout, controller, or database configuration was changed by this task. The only task artifact written is this report.
- No `v0.9.5` path or history was touched.

## Deductions

1. The request was a real model call from the exact required Dashboard session, not a synthetic or isolated harness call, because the Dashboard-visible request/response correlates to the durable Ticket, Run, Call, canonical inference attempt, and native-dashboard delivery marker.
2. The live runtime timeout authority for this call was the repaired 2,700-second value: the durable lease records `timeoutMs=2700000`, and its deadline arithmetic independently agrees exactly.
3. The CNX-342 installed repaired artifact was loaded across its verified Gateway restart and governed this post-restart request. The artifact identity/load facts are inherited from and explicitly cross-referenced to the read-only CNX-342 report; this task did not restart or mutate the Gateway.
4. CNX-343 therefore satisfies the stated PASS gates. This is an executor report only; independent ChatGPT review and operator final authority remain outstanding.

## Gate assessment

- Exact session identity: **PASS**
- Exactly one semantic request: **PASS**
- Real `ollama / qwen3.8:27b` model call: **PASS**
- Durable lifecycle correlation: **PASS**
- `timeoutMs=2700000`: **PASS**
- `deadlineAt - startedAt = 2700000 ms`: **PASS**
- No legacy `timeoutMs=900000` for this call: **PASS**
- Delivery confirmed: **PASS**
- Final Ticket status `completed`: **PASS**
- Outbox `0`: **PASS**
- No duplicate owner: **PASS**
- Protected-state mutation absent: **PASS**

**Stop condition:** stop here for independent ChatGPT review. CNX-343 is not self-accepted.
