# CNX-20260918-420 — Operator-Created Fresh Session Ollama Route and Ticket-First Discrimination Report

## Result

Combined task classification:

`BLOCKED_FRESH_SESSION_EVIDENCE`

Confirmed route sub-classification:

`FRESH_SESSION_ROUTE_OLLAMA_CONFIRMED`

Confirmed Ticket-first sub-classification:

`FRESH_SESSION_TICKET_FIRST_CONFIRMED`

Observed execution disposition:

`FAIL_OLLAMA_INFERENCE_NO_TERMINAL_SETTLEMENT`

This is not a full vertical-slice PASS. The fresh Operator-created session selected and actually entered `ollama/qwen3.8:27b`, and CogentNexus created the Ticket before the model call. However, the one model call remained active without progress beyond both its emitted deadline and the extended observation window. No terminal model-call event, `response_ready`, durable assistant delivery, native transcript message, or visible assistant response materialized.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Task: `CNX-20260918-420`
- Parent: `CNX-20260918-419`
- Authoritative starting HEAD: `c2357d1ad93ded79336515648e41e8bc0f21754b`
- Authoritative ending execution HEAD before report publication: `c2357d1ad93ded79336515648e41e8bc0f21754b`
- At both Stage 1 and closeout, local HEAD, remote-tracking HEAD, and live `git ls-remote` HEAD matched the authoritative HEAD.
- Matching report was absent before execution.

GitHub remote remained authoritative throughout execution.

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

Three old nonterminal Discord Tickets existed before this task. Their newest update was `2026-09-07T09:28:49.810043Z`; they were unchanged, had no active model calls, and did not represent a current semantic acceptance run. Counts remained unchanged between baseline and pre-handoff recheck.

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

Baseline cursors:

- maximum event ID: `864`;
- model-call row cursor: `20`;
- delivery row cursor: `14`;
- recovery row cursor: `5`;
- session row cursor: `59`.

## Operator handoff checkpoint

Nonce generated after GREEN preflight:

`CNX420-20260918T115325Z-6A95AC07`

Exact prompt supplied:

```text
ตอบกลับข้อความนี้เพียงว่า CNX420-20260918T115325Z-6A95AC07
```

Hermes instructed the Operator to:

1. refresh the Dashboard once;
2. click New Session once;
3. select Ollama / `qwen3.8:27b`;
4. enter the exact prompt above;
5. verify that the UI showed `qwen3.8:27b` before sending;
6. send exactly once manually;
7. return and say `ส่งแล้ว`.

Hermes explicitly stated that it would not inspect post-send state until the Operator said `ส่งแล้ว` and that no resend was allowed.

The Operator confirmed:

`ส่งแล้วครับ`

and supplied this fresh-session URL:

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

Hermes used read-only screenshot capture only after the Operator confirmation. The Dashboard screenshot showed:

- the exact user prompt bubble;
- the session still responding;
- the observational UI label `qwen3.8:27b · Medium`;
- no visible assistant result.

The UI label is observational evidence only and was not used as execution-route authority.

## Fresh session identity

- Session key: `agent:main:dashboard:67a8d5a6-09aa-4ba0-9963-1a243c6691af`
- Session ID: `1794f564-be6c-4a40-8416-91e876acb367`
- CNX session created at: `2026-09-18T11:53:39.775Z`
- OpenClaw `sessionStartedAt`: epoch `1789732419747`
- Parent session key: `agent:main:dashboard:6e96fece-c6ad-47b9-bfb4-680dd8a3a75b`
- Native session status at closeout: `running`
- Native model metadata at closeout: `ollama/qwen3.8:27b`
- Agent runtime metadata: `auto`, source `implicit`
- Session transcript path: `C:\Users\CDQ-P\.openclaw\agents\main\sessions\1794f564-be6c-4a40-8416-91e876acb367.jsonl`

At closeout the native transcript file remained zero bytes with SHA-256:

`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

Therefore no native user or assistant transcript record had yet been committed. The exact semantic prompt is instead proven by the Operator-confirmed UI bubble, the exact Ticket prompt, its prompt hash, and the correlated session/run lineage.

## Ticket-first evidence

The exact run was:

- Ticket ID: `CNXT-901fe944-3e38-43e4-91f4-bdb4fb685bf8`
- Run ID: `bb96c508-1cbb-4988-85cc-fd77be263966`
- Prompt SHA-256: `e1220d55ed1f6cee1ef5550e49e0865d8c153fd4a5892dc391d519e7139053c1`
- Admission trace ID: `848fe8f0-6f98-4664-a3b9-5abaf6b3897f`

Gateway/plugin trace ordering:

1. `admission.trace.started` at `2026-09-18T11:54:28.895Z`;
2. `admission.trace.input` with `senderIsOwner=true`, Dashboard namespace match, and `ticketFirst=true` at `11:54:28.898Z`;
3. `admission.trace.eligible` at `11:54:28.901Z`;
4. `admission.trace.ticket-decision` with `ticketIntakeEligible=true` at `11:54:28.905Z`;
5. `admission.trace.ticket-persisted` at `11:54:28.914Z`;
6. `admission.trace.completed`, outcome `pass`, at `11:54:28.920Z`.

Durable Ticket events:

1. event `865`, `accepted`, `2026-09-18T11:54:28.913Z`;
2. event `866`, `routed`, `2026-09-18T11:54:28.917Z`;
3. event `867`, `direct_model_call_started`, `2026-09-18T11:54:28.992Z`;
4. event `868`, `inference_attempt_started`, `2026-09-18T11:54:29.001Z`.

The accepted and routed events precede model execution. Ticket-first admission is therefore positively confirmed rather than inferred from configuration or UI state.

Ticket-first classification:

`FRESH_SESSION_TICKET_FIRST_CONFIRMED`

## Actual execution route

Correlated durable model-call evidence:

- call ID: `bb96c508-1cbb-4988-85cc-fd77be263966:model:1`;
- provider: `ollama`;
- model: `qwen3.8:27b`;
- state at closeout: `active`;
- started at: `2026-09-18T11:54:28.992Z`;
- emitted deadline: `2026-09-18T12:09:28.992Z`;
- emitted timeout: `900000 ms`;
- call source: `openclaw-model-call-hook`;
- inference-attempt source: `cogentnexus-openclaw-canonical-attempt`.

The actual route matches the Operator-selected route. This is stronger than the UI label because it is bound to the exact Ticket and run.

Route classification:

`FRESH_SESSION_ROUTE_OLLAMA_CONFIRMED`

No native assistant message materialized, so native assistant API/runtime metadata is unavailable. It is reported as unproven rather than guessed. Durable CNX provider/model evidence proves the attempted actual route.

## Extended observation and terminal failure

A read-only observer ran for 2,100 seconds with 15-second snapshots, producing 141 observations. This exceeded the expected first-response allowance and preserved the same exact run without retry.

At the final closeout observation `2026-09-18T12:32:57.662770Z`:

- elapsed since model-call start: `2308.67077 s` (about 38 minutes 29 seconds);
- time beyond emitted deadline: `1408.67077 s` (about 23 minutes 29 seconds);
- Ticket status: `accepted`;
- model-call state: `active`;
- model-call `ended_at`: null;
- terminal model-call event: absent;
- `response_ready`: absent;
- Ticket result: null;
- durable assistant delivery rows: `0`;
- outbox rows: `0`;
- Direct Recovery rows for the Ticket: `0`;
- native session status: `running`;
- native transcript bytes: `0`;
- visible assistant response: absent;
- Dashboard state: still responding.

Gateway diagnostics separately classified the session as long-running with:

- `reason=active_model_call_without_progress`;
- `classification=long_running`;
- `activeWorkKind=model_call`;
- `lastProgress=model_call:started`;
- `recovery=none`.

The log recorded this at 149, 300, 600, and 1201 seconds of age. No later progress event appeared.

The runtime remained generally healthy at closeout:

- Gateway PID `13192` remained running/Ready;
- Recovery check remained `READY`;
- Delivery check remained `READY`;
- SQLite integrity remained `ok`;
- global pending outbox remained `0`.

Those global health results do not promote this run to PASS because the exact Ticket never reached terminal model, result, or delivery state.

## Durable deltas

Relative to Stage 1:

| Durable surface | Delta |
|---|---:|
| Tickets | `+1` |
| Ticket events | `+4` |
| CNX sessions | `+1` |
| Direct model calls | `+1` |
| Assistant deliveries | `+0` |
| Outbox rows | `+0` |
| Direct recovery rows | `+0` |

The one Ticket and one model call are both bound to the exact fresh session and run.

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
| CNX assistant deliveries | `0` |
| CNX outbox rows | `0` |
| Native committed user transcript records | `0` |
| Native committed assistant transcript records | `0` |
| Visible assistant responses | `0` |

The zero native committed user records reflects the still-open zero-byte transcript, not a claim that the Operator did not send. The exact accepted Ticket and visible user bubble prove the one semantic turn.

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

CNX-420 does not reproduce the CNX-419 selected-route mismatch. The refreshed, Operator-created fresh session actually entered `ollama/qwen3.8:27b`.

CNX-420 also does not reproduce the CNX-419 Ticket-first bypass. CogentNexus admission, Ticket acceptance, routing, and model-call correlation all occurred before inference.

This does not prove that browser staleness caused CNX-419. It proves only that the fresh-session route mismatch was not reproduced in CNX-420.

The remaining observed failure is later in the vertical slice: the Ollama model call made no recorded progress and never reached terminal result or delivery state within the extended observation window.

Because the task's full PASS requires complete Ticket-first/durable lineage and visible output, the combined task result is:

`BLOCKED_FRESH_SESSION_EVIDENCE`

with execution disposition:

`FAIL_OLLAMA_INFERENCE_NO_TERMINAL_SETTLEMENT`

No repair or resend was attempted.

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
- `post-send/final-dashboard-still-responding.png`
- `post-send/gateway-status-final.json`
- `post-send/recovery-check-final.txt`
- `post-send/delivery-check-final.txt`
- `observations/latest.json`
- `observer-result.json`
- `closeout-summary.json`

Screenshot SHA-256:

`1245f5ba54dc6b0cc20fb2c500a2881ce67ff9e8d001b63ab3f7bce4c9f97325`

## Secret disclosure accounting

No API key, bearer token, password, connection string, or credential value is included in this report or the summarized evidence. Credential-bearing configuration was not dumped into the report.

## Closeout

ACTIVE.md and STATUS.md are moved to `WAITING_FOR_CHATGPT_REVIEW` with this report as the current result. Publication verification records the report blob, report SHA-256, exact remote HEAD, changed paths, and clean worktree externally after push.

CNX-421 was not created or started.
