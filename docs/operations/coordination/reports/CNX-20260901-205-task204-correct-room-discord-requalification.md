# CNX-20260901-205 — Correct-Room Discord Requalification

- **Task:** `CNX-20260901-205`
- **Parent:** `CNX-20260901-204`
- **Authority branch:** `agent/v0.9.3-full-stabilization`
- **Fresh authority SHA:** `0f43b11774c58b56278469b5e5ab216bfc8a7392`
- **Evidence root:** `C:/Users/CDQ-P/AppData/Local/Temp/cnx205-correct-room-20260901T`
- **Final disposition:** `FAIL_DURABLE_CORRELATION`

## Summary

Task 205 requalified the correct Discord room after Task 204's acknowledged wrong-room attempt. The exact numeric channel identity was proven directly from Discord's `Copy Channel ID` action and matched the task contract. Fresh managed health passed. One new human Send was performed by the operator using a fresh nonce. The nonce produced exactly one Ticket and exactly one completed direct Ollama model call with `response_ready`, but no durable native delivery confirmation was recorded during the bounded settlement window. The Ticket remained `accepted`, `delivery_confirmed_at` remained null, and no delivery row was correlated to the run.

No retry, regenerate, second message, second room, API send, injection, lifecycle mutation, or manual state repair was performed.

## Immutable authorities

```text
published v0.9.3 tag target: 26ce64a624255278a3a0266ad38746e0e6ed2e31
frozen repaired candidate: 9f4eaa429b2540540e7d6f6c2af99067960e45fb
expected installed fingerprint: f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
correct owner session: agent:main:discord:channel:1531199905673252946
correct numeric channel ID: 1531199905673252946
```

## Phase A — fresh managed-health gate

Captured at `2026-08-31T19:04:19.133011Z` using explicit native paths and read-only probes. The first probe attempt failed before execution because the subprocess PATH did not resolve `python`; this was preserved as `health-summary` harness evidence and corrected by using the absolute interpreter. The corrected probe passed.

```text
installed fingerprint: exact expected fingerprint
ownership verify: exit 0
Host mode: managed
desired Gateway/provider: running / running
selected provider: ollama
startup policy: enabled
startup adapter: installed=true, State=Ready, Enabled=true, LastTaskResult=0
plugin cogentnexus-openclaw: enabled=true, status=loaded
gateway: healthy, loopback 127.0.0.1:18789
Ollama: reachable/healthy/ready
delivery: READY, pending outbox 0
recovery: READY, active incident false, attempts 0
SQLite integrity: ok
lifecycle residue: []
```

Baseline durable counts:

```text
tickets: 10
ticket_events: 79
cnx_direct_model_call: 10
cnx_direct_recovery: 0
cnx_assistant_delivery: 7
ticket_outbox: 0
cnx_sessions: 19
```

## Phase B — exact room identity

The active Discord window was initially titled `#claw | General`; title/name alone was not used as proof. Discord's channel context menu was opened on the active `#claw` channel and the `Copy Channel ID` item was selected. The clipboard was read with:

```text
powershell.exe -NoProfile -Command "Get-Clipboard -Raw"
```

The exact result was:

```text
1531199905673252946
```

This matched both the task's numeric channel ID and the owner session key. No probe message was sent. The required confirmation was presented:

```text
CONFIRMED TARGET CHANNEL ID: 1531199905673252946
```

## Phase C — one human Send

A fresh nonce was generated only after the room and health gates passed, and a read-only SQLite search confirmed it was absent before instruction:

```text
CNX205-20260831T190442Z-8cdbed
```

The operator was instructed to send exactly:

```text
ตอบกลับข้อความนี้เพียงว่า CNX205-20260831T190442Z-8cdbed
```

The operator replied `ส่งแล้ว`. The ledger is:

```text
human Discord Send: 1 / 1 consumed
Hermes/bot/API/injected Send: 0
retry: 0
regenerate: 0
second message: 0
second room: 0
```

## Phase D — durable correlation

Immediate read-only capture after acknowledgement was taken at `2026-08-31T19:05:35.159345Z`. It established a new Ticket and model call. The first short observation series ended at `2026-08-31T19:06:26.364014Z`; a schema-bound metadata capture then ran at `2026-08-31T19:06:58.928559Z`.

Exact correlation:

```text
Ticket: CNXT-f23e2c11-e630-4319-84c2-c57ed7e7edf6
request_key: 09c9121cdac5dec9cb1fdea1a37aeafdacb098ce2e89f26a1b2a2f103fd5ed9f
run_id: b79dbb65-15eb-4b3e-8ffb-4084125e6cb5
owner_session_key: agent:main:discord:channel:1531199905673252946
prompt_sha256: bfcfe1d706817288fcf31bb9e4f8eac0459cbdade8be2e7fc181f5bdd672da61
call_id: b79dbb65-15eb-4b3e-8ffb-4084125e6cb5:model:1
provider/model: ollama / qwen3.5:9b
```

Ticket/event sequence:

```text
accepted                 2026-08-31T19:05:15.427Z
routed                   2026-08-31T19:05:15.431Z
direct_model_call_started 2026-08-31T19:05:15.546Z
 direct_model_call_ended 2026-08-31T19:06:52.235Z  outcome=completed duration=96689ms
response_ready           2026-08-31T19:06:52.333Z
```

The model-call row was terminal and completed with `recovery_started_at=null` and `recovery_attempt_count=0`. The Ticket's read-back was:

```text
status: accepted
a response_ready_at: 2026-08-31T19:06:52.333Z
delivery_confirmed_at: null
delivery_last_error: null
```

No `cnx_assistant_delivery` row matched the Ticket/run. No `cnx_direct_recovery` row matched it. Six read-only settlement samples were taken from `2026-08-31T19:07:15.020530Z` through `2026-08-31T19:08:05.049976Z`; all showed the same accepted Ticket, the same five events, null delivery confirmation, and no delivery row.

Durable counts after settlement:

```text
tickets: 11
ticket_events: 84
cnx_direct_model_call: 11
cnx_direct_recovery: 0
cnx_assistant_delivery: 7
ticket_outbox: 0
cnx_sessions: 19
```

The accepted chain therefore stops at `response_ready`:

```text
human Send -> Ticket -> direct model call -> response_ready
                                              X delivery_confirmed
                                              X completed Ticket
```

A visible/native Discord reply was not independently proven by durable evidence in the retained capture. No user-visible claim is upgraded to PASS without the required native/durable binding.

## Phase E — final health

Final read-only health was captured at `2026-08-31T19:08:26.214169Z`:

```text
Host: managed
desired Gateway/provider: running / running
selected provider: ollama
startup adapter: installed/enabled/Ready, LastTaskResult 0
Delivery: READY
Recovery: READY, no active incident, attempts 0
SQLite integrity: ok
counts: tickets 11, events 84, model calls 11, recovery 0, deliveries 7, outbox 0, sessions 19
lifecycle residue: []
```

The installed fingerprint remained the exact expected repaired fingerprint. Final runtime health passed; it does not override the missing per-run delivery settlement.

## Acceptance matrix

| Criterion | Result | Evidence |
|---|---|---|
| Fresh authority and task gate | PASS | remote SHA `0f43b117...` / Task 205 READY |
| Exact numeric room identity | PASS | Discord clipboard `1531199905673252946` |
| Fresh nonce absent before Send | PASS | `nonce.json`, no matches |
| Correct owner session binding | PASS | Ticket owner session exact target |
| Human Send budget | PASS | exactly `1/1` |
| Ticket-first ordering | PASS | `accepted` then `routed` then model start |
| Exactly one direct model call | PASS | one call, completed |
| response_ready | PASS | event and timestamp recorded |
| Native visible Discord result | NOT PROVEN | no retained native delivery receipt |
| delivery_confirmed | FAIL | Ticket field null; no delivery row |
| terminal Ticket completed | FAIL | Ticket remained `accepted` |
| Recovery attempt | PASS negative | zero recovery rows/attempts |
| Duplicate/retry/regenerate | PASS negative | none performed |
| Pending outbox | PASS | `0` |
| Final managed health | PASS | managed/Ready/healthy/SQLite ok |

## Harness and evidence issues

### I-01 — Initial absolute-toolchain miss

- **Observed:** first fresh-health Python subprocess failed with `WinError 2` because `python` was not resolvable from the child PATH.
- **Product state impact:** none; failed before the first probe and before any mutation.
- **Correction:** reran the same read-only gate with `sys.executable` and absolute Node/Python paths.
- **Remaining consequence:** initial failure is retained as harness evidence; corrected gate is authoritative.

### I-02 — Initial metadata observer schema assumption

- **Observed:** an observer queried `run_id` from `cnx_direct_recovery`, which lacks that column.
- **Product state impact:** none; read-only query failed and did not mutate state.
- **Correction:** inspected each table with `PRAGMA table_info` and built predicates only from columns actually present.
- **Remaining consequence:** failed query remains a harness issue; corrected metadata capture is authoritative.

### I-03 — Delivery settlement absent

- **Observed:** model call completed and `response_ready` was recorded, but delivery did not settle through six samples over approximately 50 seconds.
- **Product state impact:** the Task-205 semantic acceptance chain is incomplete.
- **Classification:** durable correlation failure; root cause not proven.
- **Action:** no retry or manual repair.

## Mutation ledger

```text
installer/install-over/reset/uninstall/reinstall: 0
lifecycle enable/disable/start/stop/restart: 0
process termination: 0
provider/model/config/SQLite manual mutation: 0
probe Send: 0
human Discord Send: 1 / 1
Hermes/bot/API/injected Send: 0
retry/regenerate/second message/second room: 0
source/test/workflow edit: 0
Release/tag/assets mutation: 0
force push: 0
```

## Final disposition

```text
FAIL_DURABLE_CORRELATION
```

The correct room was proven and the single authorized human Send reached one completed Ollama model call and `response_ready`. The required native/durable delivery confirmation and terminal Ticket completion were not observed. Runtime health remained green. This report does not claim a root cause; a future diagnosis/requalification task must allocate a new semantic budget if another Send is required.

## Evidence manifest

```text
health-summary.json
nonce.json
discord-post-send.json
discord-correlation-final.json
discord-settlement-series.json
settlement-final-series.json
final-health.json
status.stdout/stderr/exit
delivery.stdout/stderr/exit
recovery.stdout/stderr/exit
ownership.stdout/stderr/exit
fingerprint.stdout/stderr/exit
plugins.stdout/stderr/exit
gateway.stdout/stderr/exit
```

Payload bodies are not included in this report. No credentials, tokens, passwords, or connection strings were recorded.
