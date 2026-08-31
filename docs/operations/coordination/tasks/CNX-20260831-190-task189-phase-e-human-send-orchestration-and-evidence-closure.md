# CNX-20260831-190 — Task-189 Phase-E Human Send Orchestration and Evidence Closure

- **Status:** `READY_FOR_HERMES`
- **Date:** 2026-08-31 ICT
- **Repository:** `funggier/CogentNexus-OpenClaw`
- **Working branch:** `agent/v0.9.3-full-stabilization`
- **Parent umbrella:** `CNX-20260831-188`
- **Continues:** `CNX-20260831-189`
- **Executor:** Hermes on the accepted Windows host, with one genuine human Dashboard UI action by the user
- **Coordinator / final reviewer:** ChatGPT

## Purpose

Close only the remaining Phase-E boundary of Task 189.

Task 189 has already passed ChatGPT review through Phases A-D. The sole remaining acceptance boundary is one genuine human Dashboard Send followed by durable evidence collection.

This task exists so Hermes itself coordinates that human send and then continues evidence collection immediately after the user reports `ส่งแล้ว` in the Hermes conversation.

## Frozen product candidate

The immutable Task-188/189 product candidate remains:

`604569c286e930f1a596362ab926b065b56d486e`

Coordination-only commits after this SHA do not redefine the product candidate and must not be installed or tested as a replacement candidate.

Accepted executable facade SHA-256 remains:

`aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`

## Authoritative prerequisite evidence

Read before acting:

1. `docs/operations/coordination/reports/CNX-20260831-189-bounded-windows-documentation-payload-requalification.md`
2. `docs/operations/coordination/reviews/CNX-20260831-189-bounded-windows-documentation-payload-requalification-review.md`
3. `docs/operations/coordination/ACTIVE.md`
4. `docs/operations/coordination/STATUS.md`

The Task-189 report disposition is `WAITING_HUMAN_SEMANTIC_SEND`; ChatGPT accepted Phases A-D and did not authorize destructive lifecycle replay.

## Hard scope fence

This task authorizes only:

1. read-only pre-send baseline capture necessary to attribute the single turn;
2. Hermes prompting the user to perform exactly one genuine Dashboard Send;
3. waiting for the user's explicit `ส่งแล้ว` acknowledgement in the Hermes conversation;
4. immediate read-only post-send evidence collection;
5. publishing a durable Task-190 evidence report and coordination-only state updates.

This task does **not** authorize:

- a Hermes-generated Dashboard Send;
- `chat.inject` or equivalent synthetic injection;
- retry, regenerate, second Send, or duplicate prompt;
- reset, uninstall, fresh reinstall, provider replacement, state deletion, or recovery action merely to make the test pass;
- product/runtime/plugin executable source edits;
- test, dependency, workflow-behavior, provider-semantic, or durable-schema edits;
- release PR creation/merge, Release workflow dispatch, tag creation, GitHub Release publication, or force push.

If the single semantic turn fails in a way that would require another Send or lifecycle mutation, stop and report the evidence. Do not broaden scope automatically.

## Phase E.0 — sync and pre-send attribution baseline

When Hermes begins:

1. fetch GitHub current state fresh;
2. confirm the active branch still descends from the Task-190 coordination handoff and that the frozen product candidate is still `604569c286e930f1a596362ab926b065b56d486e`;
3. read the prerequisite files above;
4. on the accepted Windows host, capture a minimal read-only baseline immediately before asking the user to Send.

The baseline must be sufficient to calculate exactly one-turn deltas for at least:

- `tickets`;
- `ticket_events`;
- `ticket_outbox`;
- `cnx_assistant_delivery`;
- `cnx_direct_model_call`;
- `cnx_direct_recovery`;
- `cnx_sessions`;
- current delivery readiness / pending outbox;
- Gateway health;
- managed provider identity (`ollama`);
- SQLite integrity.

Do not mutate runtime state during this baseline.

## Phase E.1 — Hermes instructs the human UI actor

Immediately after the baseline, Hermes must generate a fresh nonce locally at instruction time using this semantic shape:

`CNX189-<UTC timestamp>-<short random suffix>`

Hermes must then tell the user, in the Hermes conversation, to paste/send exactly this one-line Dashboard prompt:

`ตอบกลับข้อความนี้เพียงว่า <fresh nonce>`

Hermes must explicitly instruct:

- use the normal OpenClaw Dashboard human message box;
- press Send exactly once;
- do not retry;
- do not regenerate;
- do not send a second message;
- after a logical assistant result appears, return to Hermes and say only `ส่งแล้ว`.

Hermes must not itself perform the Dashboard Send and must not substitute synthetic transport.

## Phase E.2 — wait boundary

After issuing the exact prompt, Hermes must stop active probing that could mutate semantics and wait for the user's `ส่งแล้ว` message in the same Hermes conversation.

Do not manufacture success while waiting.

If the user reports that they accidentally sent more than once, retried, regenerated, or otherwise violated the single-send boundary, record that fact and stop with `FAIL_SEMANTIC_BOUNDARY_CONTAMINATED` rather than attempting another turn.

## Phase E.3 — immediate post-send evidence collection

As soon as the user says `ส่งแล้ว`, Hermes must continue immediately and collect read-only durable evidence for the nonce it generated.

The required accepted shape is:

`1 human Send -> 1 Ticket -> 1 session/run -> 1 Ollama model call -> 1 durable assistant delivery -> 1 logical Dashboard assistant result`

Prove, using durable state and logs where applicable:

1. exactly one new Ticket attributable to the nonce;
2. the Ticket event sequence reaches the expected terminal/success state without duplicate semantic execution;
3. exactly one session/run attributable to the turn;
4. exactly one Ollama/direct model call attributable to the turn;
5. exactly one durable assistant-delivery record attributable to the turn;
6. the logical assistant content corresponds to the requested nonce acknowledgement;
7. no unexpected direct-recovery/retry path was used;
8. no duplicate assistant result was durably produced;
9. no pending terminal outbox residue remains;
10. Gateway/provider/delivery/SQLite health remains acceptable after the turn.

Do not infer success from the Dashboard UI alone. Durable evidence is authoritative.

## Dispositions

Use exactly one final disposition:

- `PASS` — all Phase-E acceptance requirements are proven;
- `FAIL_SEMANTIC_DURABLE_DELIVERY` — the single human turn occurred but the required durable shape failed;
- `FAIL_SEMANTIC_BOUNDARY_CONTAMINATED` — more than one human Send/retry/regeneration occurred or attribution cannot be made cleanly;
- `BLOCKED_HOST_DRIFT` — host/runtime baseline drift prevents a valid bounded test before the human Send;
- `REQUALIFICATION_SCOPE_EXPANSION_REQUIRED` — evidence demonstrates that destructive lifecycle or product changes would be required; do not perform them.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260831-190-task189-phase-e-human-send-orchestration-and-evidence-closure.md`

The report must include:

- exact branch HEAD observed at start;
- frozen product candidate SHA;
- generated nonce;
- pre-send baseline counts/health;
- user's `ส่งแล้ว` acknowledgement as the human completion boundary (do not claim Hermes performed the Send);
- post-send counts and exact deltas;
- Ticket/session/model-call/delivery identifiers sufficient for review;
- assistant logical result evidence;
- retry/recovery/outbox evidence;
- final health evidence;
- anomaly list, if any;
- exact final disposition.

## Coordination update

After publishing the report, Hermes may update only coordination files needed to point ChatGPT at the new evidence. Do not modify the frozen product candidate or publication artifacts.

## Stop boundary

After the Task-190 report is committed and pushed, Hermes must stop for ChatGPT review.

Hermes must not create/merge a release PR, dispatch the Release workflow, create `v0.9.3`, publish release assets, or force push.
