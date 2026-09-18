# CNX-20260918-420 — Operator-Created Fresh Session Ollama Route and Ticket-First Discrimination Report

## Result

Final classification:

`PASS_OPERATOR_FRESH_SESSION_OLLAMA_TICKET_FIRST_VERTICAL_SLICE`

Route classification:

`FRESH_SESSION_ROUTE_OLLAMA_CONFIRMED`

Ticket-first classification:

`FRESH_SESSION_TICKET_FIRST_CONFIRMED`

The Operator-created fresh Dashboard session actually executed through `ollama/qwen3.8:27b`. CogentNexus created and routed exactly one Ticket before exactly one model call, persisted the exact response, confirmed durable Dashboard delivery, and completed the Ticket. The visible assistant result matched the requested nonce.

The result is a PASS with a significant performance observation: the model call required `2,682,699 ms` — **44 minutes 42.699 seconds**. The response completed `1,782.700 seconds` — **29 minutes 42.700 seconds** — after the emitted 15-minute model-call deadline. No resend, retry, or recovery was used.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Task: `CNX-20260918-420`
- Parent: `CNX-20260918-419`
- Authoritative execution HEAD: `c2357d1ad93ded79336515648e41e8bc0f21754b`
- First report publication HEAD: `a2c6df22bacbe7aabf2c78311cfbd23ffdb7742e`
- GitHub remote remained authoritative.

The first report publication recorded the run as observation-window blocked while it was still running. The Operator then stated that the model was still working and would report completion. After the Operator confirmed a response, fresh durable and native evidence proved terminal success. This amended report supersedes that provisional classification.

## Stage 1 preflight

Stage 1 was captured at `2026-09-18T11:52:10.119887Z` and rechecked immediately before handoff at `2026-09-18T11:53:25.102417Z`.

| Gate | Result |
|---|---|
| Coordination status | `READY_FOR_HERMES` |
| OpenClaw | `2026.7.1-2 (0790d9f)` |
| Controller | `cnxMode=active`, desired Gateway `running` |
| Controller generation | `107` |
| Canonical CogentNexus plugin | exactly one, version `0.9.5`, enabled/loaded |
| Installed plugin fingerprint | `fa7243b4b88fea0b3467a42bc917b1241540c9710ebf495dc04ac1d1963bd41c` |
| Gateway | healthy, PID `13192`, port `18789` |
| Supervisor | enabled, `Ready`, last result `0` |
| Maintenance/recovery hazard | absent |
| Recovery | `READY`; no state changed |
| Delivery | `READY`; no state changed |
| SQLite integrity | `ok` |
| Pending outbox | `0` |
| Active model calls | `0` |
| Configured default route | `ollama/qwen3.8:27b` |
| Hermes browser mutations | `0` |

Three old nonterminal Discord Tickets existed before this task. Their newest update was `2026-09-07T09:28:49.810043Z`; they were unchanged, had no active model calls, and did not represent a current semantic acceptance run.

### Durable baseline

| Table | Baseline |
|---|---:|
| `tickets` | 23 |
| `ticket_events` | 864 |
| `ticket_outbox` | 0 |
| `cnx_assistant_delivery` | 14 |
| `cnx_direct_model_call` | 20 |
| `cnx_direct_recovery` | 5 |
| `cnx_sessions` | 59 |

## Operator handoff checkpoint

Nonce generated only after GREEN preflight:

`CNX420-20260918T115325Z-6A95AC07`

Exact prompt supplied:

```text
ตอบกลับข้อความนี้เพียงว่า CNX420-20260918T115325Z-6A95AC07
```

Hermes instructed the Operator to:

1. refresh the Dashboard once;
2. click New Session once;
3. select Ollama / `qwen3.8:27b`;
4. enter the exact prompt;
5. verify that the UI showed `qwen3.8:27b` before sending;
6. send exactly once manually;
7. return and say `ส่งแล้ว`.

The Operator confirmed `ส่งแล้วครับ` and supplied:

`http://127.0.0.1:18789/chat?session=agent%3Amain%3Adashboard%3A67a8d5a6-09aa-4ba0-9963-1a243c6691af`

Post-send inspection began only after that confirmation.

## Browser ownership and mutation ledger

All browser mutations belonged to the Operator.

Hermes performed:

- refresh actions: `0`;
- New Session actions: `0`;
- provider/model selection actions: `0`;
- composer focus/type actions: `0`;
- Send clicks: `0`;
- Enter/Ctrl+Enter actions: `0`;
- UI Automation mutation actions: `0`.

Hermes used read-only screenshot capture only after the Operator confirmation.

The final Dashboard capture showed one user bubble and one assistant bubble. The assistant bubble contained the exact nonce plus the CogentNexus delivery marker. The Operator initially wondered whether the response had duplicated, then corrected that observation: **it was not duplicated**. Durable evidence independently confirms one Ticket, one model call, one delivery row, one native assistant message, and no retry/recovery.

## Fresh session identity

- Session key: `agent:main:dashboard:67a8d5a6-09aa-4ba0-9963-1a243c6691af`
- Session ID: `1794f564-be6c-4a40-8416-91e876acb367`
- CNX session created at: `2026-09-18T11:53:39.775Z`
- Parent session key: `agent:main:dashboard:6e96fece-c6ad-47b9-bfb4-680dd8a3a75b`
- Final native session status: `done`
- Native session runtime: `2,682,873 ms`
- Native model metadata: `ollama/qwen3.8:27b`
- Agent runtime metadata: `auto`, source `implicit`
- Transcript: `C:\Users\CDQ-P\.openclaw\agents\main\sessions\1794f564-be6c-4a40-8416-91e876acb367.jsonl`
- Final transcript size: `1,551` bytes, `6` lines
- Final transcript SHA-256: `bb78a91fd8d26625399b86abb4a99f38fc408911c5f927ea076f00a1bcfe97e4`

Native transcript:

- user record at `2026-09-18T11:54:28.981Z` with the exact prompt;
- assistant record at `2026-09-18T12:39:11.717Z`;
- assistant provider: `ollama`;
- assistant model: `qwen3.8:27b`;
- assistant API: `ollama`;
- stop reason: `stop`;
- visible assistant text after removing the delivery marker: exact nonce.

Native record-to-record response interval:

`2,682.736 seconds` = **44 minutes 42.736 seconds**.

## Ticket-first evidence

Exact lineage:

- Ticket ID: `CNXT-901fe944-3e38-43e4-91f4-bdb4fb685bf8`
- Run ID: `bb96c508-1cbb-4988-85cc-fd77be263966`
- Model-call ID: `bb96c508-1cbb-4988-85cc-fd77be263966:model:1`
- Prompt SHA-256: `e1220d55ed1f6cee1ef5550e49e0865d8c153fd4a5892dc391d519e7139053c1`
- Admission trace ID: `848fe8f0-6f98-4664-a3b9-5abaf6b3897f`

Admission trace ordering:

1. `admission.trace.started` — `2026-09-18T11:54:28.895Z`;
2. `admission.trace.input`, `senderIsOwner=true`, Dashboard namespace match, `ticketFirst=true` — `11:54:28.898Z`;
3. `admission.trace.eligible` — `11:54:28.901Z`;
4. `admission.trace.ticket-decision`, `ticketIntakeEligible=true` — `11:54:28.905Z`;
5. `admission.trace.ticket-persisted` — `11:54:28.914Z`;
6. `admission.trace.completed`, outcome `pass` — `11:54:28.920Z`.

Durable event ordering:

1. event `865`, `accepted` — `2026-09-18T11:54:28.913Z`;
2. event `866`, `routed` — `11:54:28.917Z`;
3. event `867`, `direct_model_call_started` — `11:54:28.992Z`;
4. event `868`, `inference_attempt_started` — `11:54:29.001Z`;
5. event `869`, `direct_model_call_ended`, outcome `completed` — `12:39:11.692Z`;
6. event `870`, `inference_attempt_ended`, outcome `completed` — `12:39:11.697Z`;
7. event `871`, `response_ready` — `12:39:11.713Z`;
8. event `872`, `direct_response_durable` — `12:39:11.713Z`;
9. event `873`, `delivery_confirmed` — `12:39:11.720Z`;
10. event `874`, `completed` — `12:39:11.720Z`.

Ticket-first admission is positively confirmed because acceptance and routing preceded model execution on the same session, Ticket, and run.

Ticket-first classification:

`FRESH_SESSION_TICKET_FIRST_CONFIRMED`

## Actual execution route

Correlated model-call facts:

- provider: `ollama`;
- model: `qwen3.8:27b`;
- final state: `ended`;
- outcome: `completed`;
- started at: `2026-09-18T11:54:28.992Z`;
- ended at: `2026-09-18T12:39:11.692Z`;
- measured duration: `2,682,699 ms`;
- emitted deadline: `2026-09-18T12:09:28.992Z`;
- emitted timeout: `900000 ms`;
- call source: `openclaw-model-call-hook`;
- inference-attempt source: `cogentnexus-openclaw-canonical-attempt`.

The native assistant message independently reports provider `ollama`, model `qwen3.8:27b`, API `ollama`.

Route classification:

`FRESH_SESSION_ROUTE_OLLAMA_CONFIRMED`

CNX-420 therefore did not reproduce the CNX-419 OpenAI route mismatch.

## Long response-time observation

The Operator specifically requested that the report record how long this model took.

Authoritative timing:

| Interval | Duration |
|---|---:|
| Model-call start → model-call end | `2,682.699 s` = **44m 42.699s** |
| Native user record → assistant record | `2,682.736 s` = **44m 42.736s** |
| Ticket accepted → Ticket completed | `2,682.807 s` = **44m 42.807s** |
| Model-call deadline overrun | `1,782.700 s` = **29m 42.700s** |

The model was therefore **very slow but ultimately successful**. During the run, Gateway diagnostics reported `active_model_call_without_progress` and classified the session as long-running. The original bounded observer ended after 2,100 seconds while the run was still active. The Operator explicitly stated that it was still working and later confirmed the response. Fresh settlement evidence then proved completion.

The latency is not evidence of a retry: semantic sends remained `1`, model calls remained `1`, inference attempts remained `1`, and recovery rows remained `0`.

The fact that a call with emitted `timeoutMs=900000` completed after about 44 minutes is a runtime-authority anomaly worth reviewer attention. This report records the observed facts without assigning a repair or changing timeout configuration.

## Durable result and delivery

Final Ticket state:

- status: `completed`;
- `response_ready_at`: `2026-09-18T12:39:11.713Z`;
- `delivery_confirmed_at`: `2026-09-18T12:39:11.720Z`;
- failure class/message: null;
- delivery last error: null.

Durable delivery:

- delivery ID: `15`;
- kind: `direct_result`;
- text: exact nonce;
- status: `delivered`;
- attempt count: `0`;
- delivered at: `2026-09-18T12:39:11.720Z`;
- outbox rows: `0`;
- recovery rows for this Ticket: `0`.

The delivery marker was visible in the Dashboard presentation. There was one assistant message, not a duplicate.

## Durable deltas

Relative to Stage 1:

| Durable surface | Delta |
|---|---:|
| Tickets | `+1` |
| Ticket events | `+10` |
| CNX sessions | `+1` |
| Direct model calls | `+1` |
| Assistant deliveries | `+1` |
| Outbox rows | `+0` |
| Direct recovery rows | `+0` |

## Semantic cardinality ledger

| Action/effect | Count |
|---|---:|
| Operator fresh sessions | `1` |
| Operator semantic sends | `1` |
| Hermes semantic sends | `0` |
| Semantic retries/resends | `0` |
| CNX Tickets for the turn | `1` |
| CNX direct model calls | `1` |
| CNX inference attempts | `1` |
| CNX assistant deliveries | `1` |
| CNX outbox rows | `0` |
| Native user transcript records | `1` |
| Native assistant transcript records | `1` |
| Visible assistant responses | `1` |
| Duplicate assistant responses | `0` |
| Recovery attempts | `0` |

## Hard-fence ledger

- Hermes browser mutation: `0`.
- Hermes New Session: `0`.
- Hermes provider/model selection: `0`.
- Hermes typing/send/key action: `0`.
- Operator New Session: `1`.
- Operator semantic send: `1`.
- Semantic retry/resend: `0`.
- Direct provider/model probes: `0`.
- Provider/model config mutation: `0`.
- Manual Ticket/outbox/recovery/SQLite mutation: `0`.
- Gateway restart/reload/repair: `0`.
- Plugin lifecycle mutation: `0`.
- Installer/install-over: `0`.
- Lifecycle start/stop/restart: `0`.
- Production source repair: `0`.
- Release/tag/main: `0`.
- Force push/history rewrite: `0`.
- CNX-421 created/started: `0`.

## Interpretation

CNX-420 does not reproduce either CNX-419 defect:

- the refreshed, Operator-created fresh session honored `ollama/qwen3.8:27b`;
- CogentNexus Ticket-first admission occurred before inference.

This does not prove that stale browser presentation caused CNX-419. It proves only that the fresh-session route mismatch and Ticket-first bypass were not reproduced in CNX-420.

The complete required lineage exists:

`Dashboard/WebChat → admission trace → Ticket accepted/routed → Ollama qwen3.8:27b → response_ready → durable direct result → delivery_confirmed → Ticket completed → visible exact nonce`

Final classification:

`PASS_OPERATOR_FRESH_SESSION_OLLAMA_TICKET_FIRST_VERTICAL_SLICE`

The unusually long ~44m43s response time remains a significant performance/runtime-authority observation and should not be lost merely because the final result passed.

## Evidence paths

Evidence root:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw-Acceptance-Evidence\CNX-20260918-420`

Key artifacts:

- `stage1/authority-recheck.txt`
- `stage1/durable-baseline.json`
- `stage1/pre-handoff-delta.json`
- `stage1/runtime-summary.json`
- `stage1/operator-handoff.json`
- `post-send/authority-and-operator-confirmation.txt`
- `post-send/openclaw-target-final.json`
- `post-send/final-visible-response.png`
- `observations/latest.json`
- `observer-result.json`
- `final-success-summary.json`

Final visible-response screenshot was captured read-only after settlement; the screen showed one assistant bubble with the nonce and delivery marker.

Screenshot SHA-256:

`0b307492642b818eb51be96f8b78080024a325644211690d189da34b2a815af9`

## Secret disclosure accounting

No API key, bearer token, password, connection string, or credential value is included in this report or the summarized evidence.

## Closeout

ACTIVE.md and STATUS.md remain `WAITING_FOR_CHATGPT_REVIEW`, now with the final PASS and long-latency observation. CNX-421 was not created or started.
