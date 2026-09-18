# CNX-20260918-419 — Preserved Draft Enter-Key Submit and Ollama Ticket-First Report

## Final classification

`BLOCKED_TICKET_FIRST_ORDERING`

Secondary observed failure:

`BLOCKED_SELECTED_ROUTE_NOT_HONORED`

The exact preserved Dashboard draft materialized as one authenticated owner WebChat user message and received one exact visible nonce response. However, no CogentNexus Ticket, admission event, route event, direct model-call row, assistant-delivery row, or outbox row was created. The native OpenClaw transcript proves the response ran through `openai/gpt-5.6-luna` using `openai-chatgpt-responses`, despite the pre-send session metadata and Dashboard footer both showing `ollama/qwen3.8:27b`.

This is a live semantic bypass of Ticket-first admission and a selected-route mismatch. It is not an Ollama vertical-slice PASS.

## Fresh authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Authoritative execution HEAD: `3ef098fb037b5c2fa99732011c3eae28bcb6019e`
- Local HEAD, fetched remote-tracking tip, and live `git ls-remote` tip matched before execution and again before publication.
- ACTIVE/STATUS: `READY_FOR_HERMES`
- Task: `CNX-20260918-419`
- Matching report at execution HEAD: absent.
- Authority required reuse of the preserved session and draft, prohibited Send-button/Ctrl+Enter fallback, and allowed one Enter-path semantic submission.

## Runtime and preserved-session preflight

Read-only preflight began at `2026-09-18T10:15:26Z`.

| Gate | Live result |
|---|---|
| OpenClaw | `2026.7.1-2` |
| Controller | active/managed, desired Gateway `running` |
| Controller generation | `107` |
| Canonical CNX plugin | exactly one, version `0.9.5`, enabled/loaded |
| Installed fingerprint | `fa7243b4b88fea0b3467a42bc917b1241540c9710ebf495dc04ac1d1963bd41c` |
| Gateway | healthy, PID `13192`, port `18789` |
| Supervisor | enabled, `Ready`, recent result `0` |
| Maintenance marker | absent |
| Recovery | `READY` |
| Delivery | `READY` |
| Pending outbox | `0` |
| SQLite integrity | `ok` |
| Active provider/model calls | `0` |

Exact preserved identity:

- session key: `agent:main:dashboard:6e96fece-c6ad-47b9-bfb4-680dd8a3a75b`;
- session ID: `18fab7b9-2fb1-409f-9aed-d79168aaffdc`;
- CNX state: `active`;
- CNX generation: `0`;
- reset/delete/compact transition: none.

Pre-submit transcript:

- one session header only;
- user messages `0`;
- assistant messages `0`;
- bytes `144`;
- SHA-256 `5f4e6cf7ddb32d51f0f3cbcb35222ffc25f0e4756c28954e87668a496cef59af`;
- target Tickets/model calls/deliveries/outbox rows: all `0`.

Pre-submit global durable baseline:

| Durable object | Count |
|---|---:|
| Tickets | 23 |
| Ticket events | 864 |
| Ticket outbox | 0 |
| Assistant deliveries | 14 |
| Direct model calls | 20 |
| Direct recoveries | 5 |
| CNX sessions | 59 |

## Preserved draft and Enter-shortcut proof

The exact existing draft was preserved unchanged:

`ตอบกลับข้อความนี้เพียงว่า CNX418-20260918T095632Z-2E7A2E6B`

Windows UI Automation read-back from Firefox HWND `983994` proved immediately before submission:

- control type: `Edit`;
- accessible name: `Message Assistant`;
- enabled and keyboard-focusable;
- `hasKeyboardFocus=true` on the active instance;
- accelerator key: `Enter`;
- value exactly matched the preserved draft;
- bounds: `1052,1334,670,38`.

The accessibility accelerator value is the Windows UIA projection of the composer's `aria-keyshortcuts="Enter"` state. Therefore no Send-shortcut preference change was needed or performed.

Pre-submit target route evidence:

- OpenClaw session metadata: `modelProvider=ollama`, `model=qwen3.8:27b`;
- provider/model override fields: null;
- Firefox composer footer: `qwen3.8:27b · Medium`.

## Submission ownership and materialization

Hermes prepared and verified the read-only baseline, exact draft, target HWND/session, keyboard focus, and Enter shortcut. The Operator then requested control of the final submission and reported that it had been sent. Hermes did not issue a keypress or click in CNX-419.

The physical keyboard event was not separately instrumented, but the exact pre-submit composer exposed the Enter shortcut and the native transcript proves one accepted authenticated WebChat owner input materialized:

- user transcript ID: `f93bfcd7-caa8-4104-b33c-abef6c03d1a5`;
- source channel: `webchat`;
- `senderIsOwner=true`;
- user idempotency key: `82396cfb-2ec9-4e77-bc4e-8bd9294e534c:user`;
- internal user timestamp: `2026-09-18T10:18:02.483Z`;
- transcript-record timestamp: `2026-09-18T10:18:14.094Z`;
- exact text: the preserved CNX-418 prompt.

No second submission or retry occurred. The authoritative equivalent accepted-input evidence is the owner WebChat user transcript row; the sampled Gateway log window did not emit a `chat.send` method line.

## Ticket-first ordering failure

At every post-submit observation through closeout at `2026-09-18T10:22:14Z`:

- target Ticket count: `0`;
- target ticket-event count: `0`;
- accepted events: `0`;
- routed events: `0`;
- admission trace: absent;
- target CNX direct-model-call count: `0`;
- target CNX assistant-delivery count: `0`;
- target outbox count: `0`;
- target recovery count: `0`.

Global durable counts remained exactly unchanged from baseline:

| Durable object | Baseline | Closeout | Delta |
|---|---:|---:|---:|
| Tickets | 23 | 23 | 0 |
| Ticket events | 864 | 864 | 0 |
| Ticket outbox | 0 | 0 | 0 |
| Assistant deliveries | 14 | 14 | 0 |
| Direct model calls | 20 | 20 | 0 |
| Direct recoveries | 5 | 5 | 0 |
| CNX sessions | 59 | 59 | 0 |

Despite the absence of Ticket admission, an assistant inference result materialized. Consequently there can be no accepted/routed-before-model-start proof. The required Ticket-first invariant failed at its first durable boundary:

`BLOCKED_TICKET_FIRST_ORDERING`

## Actual provider/model route

The assistant transcript row is authoritative for the actual native OpenClaw execution:

- assistant transcript ID: `31e4632b-8014-4b8b-af18-a3ffe6364d65`;
- parent user ID: `f93bfcd7-caa8-4104-b33c-abef6c03d1a5`;
- API: `openai-chatgpt-responses`;
- provider: `openai`;
- model: `gpt-5.6-luna`;
- stop reason: `stop`;
- output tokens: `36`;
- input tokens: `12114`;
- assistant internal timestamp: `2026-09-18T10:18:23.190Z`;
- assistant transcript-record timestamp: `2026-09-18T10:18:23.195Z`.

Post-run OpenClaw session metadata also resolved to:

- `modelProvider=openai`;
- `model=gpt-5.6-luna`;
- status `done`;
- agent runtime `codex`, source `implicit`.

Measured intervals:

- internal user-to-assistant timestamps: `20,707 ms`;
- transcript-record timestamp interval: `9,101 ms`.

No Ollama direct probe was performed, and no Ollama/CNX model-call row exists. The actual execution route contradicted the selected pre-send route:

`BLOCKED_SELECTED_ROUTE_NOT_HONORED`

The observed OpenAI request was a product routing outcome, not an executor provider-selection change.

## Visible response and native transcript

Firefox displayed exactly one user bubble and exactly one assistant bubble. The assistant text exactly matched the required normalized nonce:

`CNX418-20260918T095632Z-2E7A2E6B`

Final native transcript:

- rows: `3` — session header, one user message, one assistant message;
- roles: user `1`, assistant `1`;
- nonce occurrences: `2`;
- bytes: `1422`;
- SHA-256: `4f155527787570e9100a81b38999aa632a3d424401c6fc002995795169405ba5`.

Visible correctness does not satisfy CNX-419 because Ticket admission, selected Ollama routing, and CogentNexus durable completion were absent.

## Durable completion and duplicate accounting

No CogentNexus result-ready, delivery-confirmed, Ticket completion, or result outbox evidence exists for this semantic turn. Recovery and Delivery remained generically READY only because no CNX lineage was created; those global statuses do not convert the bypassed native OpenClaw response into durable CNX completion.

| Effect | Count attributable to CNX-419 |
|---|---:|
| Materialized owner WebChat user messages | 1 |
| Visible assistant replies | 1 |
| Exact nonce assistant replies | 1 |
| CogentNexus Tickets | 0 |
| Accepted events | 0 |
| Routed events | 0 |
| Admission traces | 0 |
| CogentNexus direct model calls | 0 |
| Native OpenClaw provider responses | 1 |
| Actual OpenAI responses | 1 |
| Ollama responses | 0 |
| CNX assistant-delivery rows | 0 |
| CNX outbox rows | 0 |
| Recovery effects | 0 |
| Duplicate user messages | 0 |
| Duplicate assistant messages | 0 |

## Final health and preservation

Post-submit health captured at `2026-09-18T10:19:50Z` and closeout durable observation at `2026-09-18T10:22:14Z` proved:

- Gateway remained healthy on PID `13192`;
- Supervisor remained enabled/Ready with result `0`;
- controller remained active/managed generation `107`;
- Recovery remained READY;
- Delivery remained READY;
- pending outbox remained `0`;
- SQLite integrity remained `ok`;
- active CNX model calls remained `0`;
- no late Ticket, event, model-call, delivery, outbox, or recovery row appeared;
- the exact session remained intact;
- no retry or second semantic message occurred.

Evidence pack:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw-Acceptance-Evidence\CNX-20260918-419`

## Exact hard-fence ledger

| Action/effect | Count |
|---|---:|
| New Session/New Chat | 0 |
| Send-button clicks/UIA Invoke in CNX-419 | 0 |
| Ctrl+Enter submissions | 0 |
| Materialized semantic submissions | 1 |
| Operator-owned final submissions | 1 |
| Hermes Enter-key actions | 0 |
| Semantic resend/retry | 0 |
| Send-shortcut preference changes | 0 |
| Direct Ollama/model probes | 0 |
| OpenAI semantic responses observed | 1 |
| Provider/model selection changes by executor | 0 |
| Other config mutation | 0 |
| Installer/install-over | 0 |
| Plugin lifecycle mutation | 0 |
| Gateway restart/reload/repair | 0 |
| CNX lifecycle mutation | 0 |
| Manual Ticket/outbox/recovery/SQLite mutation | 0 |
| Manual delivery/replay | 0 |
| Session reset/delete/compact | 0 |
| Release/tag/main | 0 |
| Force push/history rewrite | 0 |
| CNX-420 creation/start | 0 |

## Final classification

Primary:

`BLOCKED_TICKET_FIRST_ORDERING`

Secondary:

`BLOCKED_SELECTED_ROUTE_NOT_HONORED`

One authenticated owner semantic turn and one exact visible response occurred, but the turn bypassed CogentNexus Ticket-first admission and executed through OpenAI/Luna instead of the selected Ollama route. No resend was attempted, the evidence was preserved, and Hermes did not create or start CNX-420.
