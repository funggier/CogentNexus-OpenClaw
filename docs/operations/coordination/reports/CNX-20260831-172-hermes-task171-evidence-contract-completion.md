# CNX-20260831-172 — Task-171 Evidence-Contract Completion

- **Disposition:** `PASS`
- **Executor:** Hermes/Codex
- **Execution mode:** `TASK171_EVIDENCE_CONTRACT_COMPLETION_HERMES`
- **Observed:** 2026-08-31 ICT
- **Evidence root:** `C:\Users\CDQ-P\AppData\Local\Temp\cnx172-evidence-20260831T024020Z`

## Objective and authority

Task-172 was activated by fresh GitHub state at remote HEAD `85411b03291c7a8e4846b1dcef3813ebba27cbd2`. Fresh remote `ACTIVE.md` and `STATUS.md` identify Task-172 as `READY_HERMES`. The task authorizes read-only inspection/hashing of the already-executed Task-171 evidence and publication of this report only.

The Task-171 semantic experiment was not repeated or altered. Task-172 semantic action count is exactly `0`; Task-171's frozen Send count remains exactly `1`.

Authoritative prior action:

- Task-171 activation HEAD: `b6ebb89860d176222773320087a7d1dfa34656a8`
- Task-171 report commit: `db4cbbbb63d6023653d271e6d15d87a477d6d8bd`
- Product repair SHA: `231761fca24c315e90536955d3e384f55e2e232e`
- Installed fingerprint: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`
- Package SHA-256: `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91`
- OpenClaw: `2026.7.1-2`
- Preserved Task-171 evidence root: `C:\Users\CDQ-P\AppData\Local\Temp\cnx171-evidence-20260831T020231Z`

The Task-172 report was absent from the remote tree before writing. The remote diff from Task-171 activation contains only coordination state, the Task-171 report/review, and the Task-172 task; no product/source/test/workflow drift was found.

## Exact Task-171 action identity

- Nonce: `T171-20260831T020446Z-3142A528`
- Prompt: `CNX-171 acceptance T171-20260831T020446Z-3142A528. Reply with exactly: CNX-171-ACK-T171-20260831T020446Z-3142A528`
- Expected response: `CNX-171-ACK-T171-20260831T020446Z-3142A528`
- Session key: `agent:main:dashboard:13b27c98-c09c-431e-928f-446175ed1937`
- Ticket: `CNXT-b5bf2532-d35d-47db-8951-fcf9f4729abf`
- Run: `8b69bede-030f-4c20-8bb8-0aa99e12422c`
- Prompt SHA-256: `1ae4127758cf946cf694e95e0bed0fcd7816eca4df63fbd23b933e95a0ea7f45`
- Frozen Send ledger: `b01-send-ledger.json`; one authorized Send, no retry
- Native nonce/response search: nonce occurs once in native user record and once in native assistant record

## Native transcript and marker identity

- Transcript: `C:\Users\CDQ-P\.openclaw\agents\main\sessions\7d2ca55f-ecda-4e24-b924-5f61e75a13b3.jsonl`
- Transcript SHA-256: `0da04a930e521ab146f9c3684a776ab974f091b8266fa6d62fe84ca3adb875f6`
- User message ID: `750be5ac`; timestamp `2026-08-31T02:14:23.003Z`; nonce count `1`
- Assistant message ID: `e682c442`; timestamp `2026-08-31T02:14:45.081Z`; expected-response count `1`
- Persisted assistant text starts with the exact expected response and contains one marker:
  `cogentnexus-openclaw-delivery:d3c50a5cae5a5c4084fb30460cc772cb`
- Parsed marker identity: `d3c50a5cae5a5c4084fb30460cc772cb`
- Trajectory: `C:\Users\CDQ-P\.openclaw\agents\main\sessions\7d2ca55f-ecda-4e24-b924-5f61e75a13b3.trajectory.jsonl`
- Trajectory SHA-256: `aaca650d8b72543fd3875bde086de8f4bdc3fa33f75fc83a4f2175497c9f0b02`
- Run-scoped trajectory events: one `prompt.submitted`, one `model.completed`, one successful `session.ended`; no abort or timeout

The marker-bearing assistant record is bound to the same Ticket/run through the durable delivery row and the `delivery_confirmed` event's `source=native-dashboard-marker`.

## Ticket, model, and request identity

- Ticket status: `completed`
- Run ID: `8b69bede-030f-4c20-8bb8-0aa99e12422c`
- Full model-call ID: `8b69bede-030f-4c20-8bb8-0aa99e12422c:model:1`
- Provider/model: `ollama` / `qwen3.5:9b`
- Model-call start: `2026-08-31T02:14:23.028Z`
- Model-call end: `2026-08-31T02:14:44.984Z`
- Outcome: `completed`; duration `21957ms`
- Ticket request key: `606a0129562d879e7f9904386927dfee3edbdf2c06a4343c489faa129fedaf4b`
- Direct-result idempotency key: `cnxclaw-direct-result:CNXT-b5bf2532-d35d-47db-8951-fcf9f4729abf:g0`
- `response_ready_at`: `2026-08-31T02:14:45.052Z`
- `delivery_confirmed_at`: `2026-08-31T02:14:45.082Z`
- `durableDelivery=true`; `durablePayload=true`; `deliveryPending=false` at settlement

Ticket event sequence, in ascending event ID order:

| Event ID | Type | Timestamp | Material fields |
|---:|---|---|---|
| 22 | `accepted` | `2026-08-31T02:14:22.820Z` | run ID and prompt SHA |
| 23 | `routed` | `2026-08-31T02:14:22.870Z` | `workflowEligible=false` |
| 24 | `direct_model_call_started` | `2026-08-31T02:14:23.028Z` | full call ID, Ollama/model, 900000ms deadline |
| 25 | `direct_model_call_ended` | `2026-08-31T02:14:44.984Z` | same call ID, `completed`, 21957ms |
| 26 | `response_ready` | `2026-08-31T02:14:45.052Z` | durable delivery and payload hashes, idempotency key |
| 27 | `direct_response_durable` | `2026-08-31T02:14:45.052Z` | generation 0, idempotency key, payload SHA |
| 28 | `delivery_confirmed` | `2026-08-31T02:14:45.082Z` | native marker source, same idempotency key |
| 29 | `completed` | `2026-08-31T02:14:45.082Z` | `deliveryConfirmed=true`, `durablePayload=true` |

## Durable delivery row

Read-only SQLite inspection used the existing database and did not write state. Database integrity is `ok`. Exactly one row binds to the Task-171 Ticket:

- Delivery ID: `1`
- Ticket ID: `CNXT-b5bf2532-d35d-47db-8951-fcf9f4729abf`
- Owner session key: `agent:main:dashboard:13b27c98-c09c-431e-928f-446175ed1937`
- Owner generation: `0`
- Kind: `direct_result`
- Text: `CNX-171-ACK-T171-20260831T020446Z-3142A528`
- Text SHA-256: `9ef1529cb75e4f715e772ca655c033d169f1862af695959ede71d12abda95543`
- Target binding: `kind=direct`, same Ticket ID, run ID `8b69bede-030f-4c20-8bb8-0aa99e12422c`
- Idempotency key: `cnxclaw-direct-result:CNXT-b5bf2532-d35d-47db-8951-fcf9f4729abf:g0`
- Status: `delivered`
- Attempt count: `0`
- Last error: `null`
- Created: `2026-08-31T02:14:45.052Z`
- Updated/delivered: `2026-08-31T02:14:45.082Z`
- Claim token/expiry: `null` / `null`

## Duplicate, recovery, and outbox proof

Run-scoped and aggregate readbacks agree:

- Native user nonce records: `1`
- Native assistant expected-response records: `1`
- Direct model-call rows/events for the run: `1`
- Direct recovery rows for the run: `0`
- Conflicting outbox rows for the run: `0`
- Durable delivery rows for the Ticket: `1`
- Duplicate delivery rows: `0`
- Recovery/regeneration event in the Task-171 event sequence: `0`
- Post-state aggregate `ticket_outbox`: `0`
- Post-state `cnx_direct_recovery`: `0`

Task-171 post counts were `tickets=4`, `ticket_events=29`, `cnx_assistant_delivery=1`, `cnx_direct_model_call=4`, `cnx_direct_recovery=0`, and `ticket_outbox=0`; the corresponding preflight counts were `3`, `21`, `0`, `3`, `0`, and `0`.

## Nine-row Task-171 acceptance matrix

| # | Task-171 success criterion | Result | Exact evidence pointer |
|---:|---|---|---|
| 1 | Exactly one Dashboard semantic Send | `PASS` | `b01-send-ledger.json`; frozen budget `1`, no retry; native transcript has exactly one nonce-bearing user record |
| 2 | Exactly one model execution for the request | `PASS` | `b01-contract-packet.json` → trajectory `model.completed` count `1`; Ticket events 24–25; full call ID `8b69bede-030f-4c20-8bb8-0aa99e12422c:model:1` |
| 3 | Exactly one native persisted assistant result for nonce/expected answer | `PASS` | Native transcript SHA `0da04a...875f6`; assistant ID `e682c442`; expected-response count `1` |
| 4 | Expected native delivery marker/identity present | `PASS` | Native assistant marker `d3c50a5cae5a5c4084fb30460cc772cb`; Ticket event 28; delivery row ID 1 |
| 5 | Exactly one correctly bound `cnx_assistant_delivery` row | `PASS` | `b01-contract-packet.json` → one row, Ticket/run/session/idempotency all match |
| 6 | Post-persistence settlement succeeds and `delivery_confirmed_at` is authoritative/non-null | `PASS` | Events 26–29; `delivery_confirmed_at=2026-08-31T02:14:45.082Z`; source `native-dashboard-marker` |
| 7 | Final Ticket reaches successful terminal state | `PASS` | Ticket `CNXT-b5bf2532-d35d-47db-8951-fcf9f4729abf`, status `completed`; event 29 |
| 8 | No duplicate UI/native result, second inference, recovery reinjection, or conflicting outbox/delivery | `PASS` | Run-scoped counts above; transcript/trajectory hashes; recovery `0`; outbox `0`; delivery rows `1` |
| 9 | Installed fingerprint/OpenClaw pin/runtime/storage integrity acceptable after experiment | `PASS` | Task-171 `c05-status.txt`/`c06-gateway.txt`; accepted fingerprint, OpenClaw `2026.7.1-2`, managed/READY, Gateway/provider healthy, SQLite `integrity_check=ok` |

All nine required criteria are `PASS`. No criterion is `FAIL` or `UNPROVEN`.

## Reviewer Verification Packet

| # | Critical claim | Why it matters | Exact evidence | Suggested reviewer check |
|---:|---|---|---|---|
| 1 | The live Send budget was consumed exactly once | Prevents an accidental second semantic experiment | `b01-send-ledger.json`; Task-172 semantic action count `0` | Check ledger budget and native user nonce count; confirm no Task-172 UI action exists |
| 2 | Exactly one model execution served the request | Proves no hidden duplicate inference | Full call ID and Ticket events 24–25; trajectory SHA | Query events by run ID and require one start/end pair with completed outcome |
| 3 | Native transcript is immutable and contains one exact result | Establishes native persistence authority | Transcript path + SHA `0da04a930e521ab146f9c3684a776ab974f091b8266fa6d62fe84ca3adb875f6` | Hash the transcript and count nonce/expected-response records |
| 4 | Marker identity is bound to the durable result | Proves post-persistence settlement is not a UI-only claim | Marker `d3c50a5cae5a5c4084fb30460cc772cb`, delivery ID 1, same Ticket/run | Parse marker and compare its settled delivery/idempotency binding with SQLite row/events |
| 5 | Exactly one delivery row was delivered and confirmed | Proves durable exactly-once delivery | Delivery ID 1, status `delivered`, `attempt_count=0`, confirmation timestamp | Query Ticket-scoped delivery rows and compare text, idempotency key, timestamps |
| 6 | Ticket-first event ordering completed normally | Rules out response-before-Ticket and recovery races | Event IDs 22–29 in `b01-contract-packet.json` | Verify accepted/routed precede model call and durable/confirmed/completed follow response |
| 7 | No duplicate/recovery/outbox conflict remains | Demonstrates fail-closed duplicate prevention | Run-scoped recovery `0`, outbox `0`, duplicate native/delivery counts `0` | Query all rows/events using the exact run and Ticket IDs; require no conflicting rows |
| 8 | Accepted installed provenance and runtime survived the experiment | Connects the result to the repaired candidate | Task-170 fingerprint, package SHA, OpenClaw pin, `c05-status.txt`, `c06-gateway.txt` | Recompute fingerprint/version and inspect managed/Gateway/provider/SQLite read-only health |

## Immutable evidence index

| Artifact | SHA-256 |
|---|---|
| Task-171 `b01-send-ledger.json` | `6eaa1a249a8f0fcbb9504c431192369c39e38ffc7461b8e4997fccdf3f304b5e` |
| Task-171 `c02-post-db.json` | `11fcaf8e00f6d7dd914b5d1dd08aa7e43e668c1f0c0ba56cd3b326f4036ef8d0` |
| Task-171 `c03-check-delivery.txt` | `a5b9e6d5378897419059dcd8df9ce1bd1e801153b3f328eceda9184f18f3aa0d` |
| Task-171 `c04-check-recovery.txt` | `9fff3426af115cda2737be7e7f7ca8b7b9e5aad4d42515133057b14f284d5cc5` |
| Task-171 `c05-status.txt` | `0a8dd8dbc55115470b2a0cdd7cfc25c7f54ebbab8fe30e0a1a08026712109e09` |
| Task-171 `c06-gateway.txt` | `caeb99a136068dc7140daab9be34ecb94b8055831d576aa8a8e49af75a5be1af` |
| Task-171 `c09-native-settlement.json` | `6571f30f112880bb18004559a4daa8660cd6f1baa47d63f0a070ecfb7fcc35b5` |
| Task-171 Dashboard screenshot `computer_use_7067f2debe134b8cb859cb0a52db2059.png` | `b4b0fc0545360422da43c4cd7ac366fb83f5f47882c27f5fb12cd4d77e78685f` |
| Native transcript `7d2ca55f-ecda-4e24-b924-5f61e75a13b3.jsonl` | `0da04a930e521ab146f9c3684a776ab974f091b8266fa6d62fe84ca3adb875f6` |
| Native trajectory `7d2ca55f-ecda-4e24-b924-5f61e75a13b3.trajectory.jsonl` | `aaca650d8b72543fd3875bde086de8f4bdc3fa33f75fc83a4f2175497c9f0b02` |
| Task-172 generated packet `b01-contract-packet.json` | recorded in evidence root; packet contains the above field-level bindings |

Missing artifact: `c01-post-send-nonce-search.json` was not present in the preserved Task-171 evidence root because its original collector timed out. It was not regenerated. Pre-send nonce absence is independently recorded in the frozen ledger, and post-send nonce/native identity is proven by the immutable transcript and trajectory.

## Post-state and anomalies

Read-only post-state remained coherent: SQLite integrity `ok`; Ticket completed; one delivered row; non-null confirmation; zero outbox/recovery conflicts; managed Gateway/provider health remained ready; accepted fingerprint and OpenClaw pin were preserved.

The immediate Task-171 UI screenshot retained composer text after the Send click and did not prove final visible UI nonce counts. This is explicitly residual UI observation uncertainty. It does not override the native transcript/Ticket/delivery authority and is not a failure of any of the nine native/durable success criteria. No UI count is fabricated.

Task-172 collector initially exited nonzero after writing a valid packet because of a trailing helper sentinel; the helper was corrected and rerun read-only with exit code `0`. No runtime state changed. The original missing `c01` artifact remains missing and is disclosed above.

## Hard-fence compliance

Task-172 performed:

- semantic Send: `0`
- model inference: `0`
- Dashboard Enter/submission: `0`
- `chat.inject`: `0`
- recovery/regeneration: `0`
- installer/lifecycle/restart/reset: `0`
- DB/Ticket/result/outbox/delivery/transcript mutation: `0`
- source/test/workflow/product change: `0`
- upgrade/release/merge/force push: `0`

Only read-only GitHub/repository inspection, evidence hashing/inspection, read-only SQLite/transcript queries, and this report publication are authorized and performed.

## Residual uncertainty and recommendation

Residual uncertainty is limited to final visible Dashboard nonce counts and the missing historical `c01` collector artifact. Those facts were not reconstructed or inferred. Native persistence, marker binding, Ticket settlement, model identity, delivery identity, duplicate/recovery/outbox proof, and post-health are directly evidenced.

Recommended successor: none. Task-172 stops for ChatGPT final review; no semantic or lifecycle successor is authorized by this task.

## Publication state

This report is the only file authorized for Task-172 publication. Before publication it was confirmed absent on remote HEAD `85411b03291c7a8e4846b1dcef3813ebba27cbd2`. After commit/push, remote HEAD, blob SHA, and changed-path scope must be read back and recorded in the final execution response.
