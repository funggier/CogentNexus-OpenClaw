# CNX-20260829-136 — Final Dashboard Durable-Delivery Acceptance

- Status: `READY_FOR_HERMES`
- Execution mode: `LIVE_WINDOWS_DASHBOARD_DURABLE_DELIVERY_ACCEPTANCE_ONLY`
- Owner / independent reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-29 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Perform the final real OpenClaw Dashboard durable-delivery acceptance for CogentNexus-OpenClaw v0.9.3.

This task authorizes exactly **one new benign semantic user message** through the real OpenClaw Dashboard UI and exactly **one submission activation**. It then proves, using durable state as authority, that the message was committed Ticket-first, processed once, reached a coherent terminal result, and its assistant result was delivered exactly once without duplicate external side effects.

This task does not authorize source repair, installer/lifecycle/recovery work, provider/model/config mutation, manual outbox retry, cleanup, normalization, merge, tag, or release.

## Accepted candidate and prerequisite chain

Accepted source candidate:

`1424d6fbee2c458c8c30440616783d2fa1bc1201`

Accepted recovery harness blob:

`a4138e00e2056db89b0a9eceed1b54e001c4e319`

Accepted package proof:

- artifact ID: `9709798190`
- outer artifact digest: `sha256:e8dbb2f742bfeffc93a80a7cda62a8c273ced9e2b1e9b47a3962dead52ccfeef`
- payload count: `178`
- payload/plugin fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`

Task 134 independently accepted the complete one-shot live recovery suite. That suite is consumed and must not be replayed.

Task 135 independently accepted the clean post-recovery delivery baseline:

- `pendingOutbox = 0`;
- `nonterminalTickets = 0`;
- no unresolved workflow/direct-recovery/assistant-delivery/outbound-send residue;
- recovery `READY`;
- delivery `READY`;
- SQLite integrity `ok`;
- no Dashboard Send had occurred under stabilization acceptance.

Task-135 independent review:

`docs/operations/coordination/reviews/CNX-20260829-135-post-recovery-delivery-residue-readonly-closeout-review.md`

## Single-message ledger

Task 136 creates one new semantic-delivery ledger only:

- fresh acceptance nonce: maximum `1`;
- Dashboard semantic message composition: `1`;
- Dashboard submission activation: maximum `1 / 1`;
- semantic resend: `0` allowed;
- alternate CLI/Gateway/API semantic injection: `0` allowed;
- manual outbox retry/ack: `0` allowed.

Once the first Dashboard submission activation occurs, this authorization is consumed regardless of UI outcome.

## Critical no-resend rule

**After the first Send activation, never submit the semantic message again.**

Do not resend because of:

- spinner or loading state;
- Dashboard reconnect;
- apparent timeout;
- missing immediate assistant bubble;
- uncertain browser response;
- UI refresh;
- ambiguous acknowledgement;
- transient Gateway/provider health display.

After the single submission, the authoritative evidence source becomes the durable Ticket/event/result/outbox/delivery state. UI ambiguity must be resolved by read-only observation, not by another Send.

## Phase 0 — fresh authority and zero-baseline preflight

Before composing or submitting the acceptance message:

1. Fresh-fetch branch HEAD, `ACTIVE.md`, and `STATUS.md`; confirm Task 136 remains authoritative and unsuperseded.
2. Confirm no source/runtime deployment change since accepted candidate requires reinstall. Do not install/install-over.
3. Use the explicit installed launcher:

   `C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd`

   Freshly read/hash/parse it and require explicit root:

   `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw`

4. Require an already-safe live baseline without normalization:
   - mode `managed`;
   - desired Gateway/provider `running`;
   - selected provider `ollama` in host/provider views;
   - recovery exact `READY`;
   - delivery exact `READY`;
   - no active provider incident/circuit/transition;
   - exact installed fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
   - OpenClaw `2026.7.1-2`;
   - exactly one CogentNexus-OpenClaw plugin loaded/enabled;
   - Gateway healthy;
   - Ollama healthy; record version/model inventory;
   - authoritative SQLite exists and `PRAGMA integrity_check` returns exactly `ok` using URI `mode=ro`;
   - `pendingOutbox=0`;
   - `nonterminalTickets=0`;
   - no unresolved workflow/direct-recovery/assistant-delivery/outbound-send residue.

If this baseline is not already clean, stop `BLOCKED`. Do not clean, retry, start/restart, cancel, ack, or otherwise manufacture a zero baseline.

## Phase 1 — fresh acceptance nonce

Generate one fresh opaque nonce after the zero baseline is captured, for example:

`CNX-DDA-<UTC timestamp>-<random short suffix>`

Requirements:

- no secret or personal data;
- record the exact nonce in evidence/report;
- use read-only database/log search to verify the nonce is absent from existing Ticket/event/delivery records before Send;
- do not create another nonce after Send;
- do not reuse a historical acceptance nonce.

The benign semantic message should be exactly one short user request containing that nonce, conceptually:

`CogentNexus final durable-delivery acceptance <NONCE>. Reply with exactly: ACK <NONCE>`

Record the exact message text used. It must have no requested tool call, file change, network side effect, code execution, or other external action beyond a normal assistant reply.

## Phase 2 — real Dashboard UI, exactly one Send

This acceptance must use the **real OpenClaw Dashboard conversation UI**. Do not substitute CLI, Gateway RPC, direct plugin API, database insertion, HTTP injection, or synthetic test transport.

Before Send:

- confirm the Dashboard is connected to the already-healthy accepted runtime;
- identify the intended normal/default conversation/session;
- ensure the input box contains the exact single acceptance message and no duplicate copy;
- capture sufficient UI evidence to identify pre-send state without exposing unrelated private conversation content in the repository report.

Submission:

- perform exactly one deliberate submission gesture;
- prefer one click/activation of the Dashboard Send control;
- do not additionally press Enter or click Send again;
- record UTC/local timestamp of the one activation as precisely as available;
- increment the Task-136 send ledger to consumed `1 / 1` immediately after activation.

If the real Dashboard cannot be used reliably, stop `BLOCKED` **before** Send. No alternate transport is authorized.

## Phase 3 — Ticket-first durability proof

After the single Send, do not resend. Observe durable state read-only.

Prove that the one semantic input produced exactly one new Ticket associated with the nonce.

Capture at minimum:

- Ticket ID;
- Ticket durable creation timestamp;
- relevant stable row/event IDs or ordering fields;
- initial Ticket status;
- complete status-transition sequence for the new Ticket;
- all relevant `ticket_events` event types/timestamps/order for that Ticket;
- workflow/direct-recovery association if the implementation creates one;
- no second Ticket containing the same nonce.

### Ticket-before-inference invariant

PASS requires affirmative evidence that the durable Ticket commit preceded inference/model execution.

Prefer monotonic durable ordering evidence (row/event sequence IDs, committed event ordering, or another implementation-owned durable order) over wall-clock inference alone.

If the implementation has a durable inference-start/model-start/admission event, report its identity and prove the Ticket/create event precedes it.

If inference-start evidence exists only in retained runtime/OpenClaw logs, correlate the earliest inference-start marker to the already committed Ticket/event order. Do not claim Ticket-first merely because the UI showed a message first.

If the available evidence cannot establish Ticket-before-inference unambiguously, verdict is `FAIL` or `BLOCKED` as appropriate. Do not resend or mutate the system to improve evidence.

## Phase 4 — processing/workflow/result/validator proof

For the exact new Ticket, observe normal runtime execution only.

Require a coherent single processing chain:

- one admitted semantic input;
- one Ticket execution chain;
- no duplicate active run for the same Ticket;
- any workflow ledger/event history is internally consistent;
- no recovery duplicate is created for an already progressing/terminal Ticket;
- terminal Ticket state is successful (`completed` or the implementation's reviewed equivalent);
- durable result/output exists for the exact Ticket;
- validators/guards associated with terminal completion pass;
- result identity/hash/metadata is coherent where the schema provides it.

Do not require a `ticket_workflows` row if the reviewed simple-message path legitimately uses only Ticket/event execution; instead report the actual durable path. Do not invent a workflow that does not exist.

If the model response is not exactly `ACK <NONCE>` but the durable processing/delivery chain otherwise succeeds, classify semantic-response mismatch separately and do not resend. For full PASS of this final acceptance, both the durable chain and the benign requested response should be coherent.

## Phase 5 — durable delivery and exactly-once proof

Track the new Ticket/result through the implementation's delivery path using read-only durable evidence.

Require:

- exactly one logical outbox/delivery chain for the new Ticket/result;
- terminal delivery status `delivered` or reviewed equivalent;
- no pending outbox residue after terminal delivery;
- attempt metadata captured where available;
- acknowledgement metadata captured where available;
- no duplicate outbox row/logical delivery for the same Ticket/result;
- no duplicate `cnx_assistant_delivery` or `cnx_outbound_send` external-send identity where those tables participate;
- no second semantic assistant delivery attributable to the one Ticket;
- no duplicate external side effect.

Compare pre-send and post-send counts/IDs. The pre-send authority is Task-136 Phase-0 zero baseline, not assumptions from UI.

If normal system-internal delivery machinery records multiple low-level attempt records for one logical delivery, report them explicitly and prove they resolve to one acknowledged external delivery. Do not hide retries, and do not manually trigger any retry.

The Dashboard's visible assistant response should correspond to the durable result/delivery record, but SQLite/event/ledger evidence remains authoritative.

## Phase 6 — bounded observation and failure rule

After Send, read-only polling/observation is allowed for a bounded period sufficient for the normal configured local-model completion/delivery horizon, up to 10 minutes unless the implementation's established timeout produces a terminal result sooner.

During this period:

- no second Send;
- no message edit/re-submit;
- no browser alternate submission;
- no manual Ticket dispatch;
- no outbox retry/ack;
- no start/restart/recovery action;
- no process kill;
- no database write;
- no cleanup/normalization.

If the one Ticket does not reach a coherent terminal and delivered state within the bounded observation period, preserve first-failure evidence and verdict `FAIL`. The single-send ledger remains consumed.

If UI is ambiguous while durable evidence reaches terminal delivered success, use durable evidence plus one final read-only UI observation; do not resend.

## Phase 7 — final read-only system snapshot

After the one Ticket/delivery reaches terminal state or the bounded observation fails, capture a final read-only snapshot:

- mode/desired Gateway/provider;
- selected provider;
- recovery verdict/checks/incident/circuit;
- delivery verdict/checks;
- Gateway/Ollama health;
- Ollama version/model inventory and equality with pre-send inventory;
- exact installed plugin/fingerprint unchanged;
- SQLite `PRAGMA integrity_check=ok`;
- new Ticket terminal state;
- `nonterminalTickets=0` expected after PASS;
- `pendingOutbox=0` expected after PASS;
- no unresolved workflow/direct-recovery residue;
- no duplicate assistant-delivery/outbound-send residue;
- Supervisor/OpenClaw task/service read-only state;
- no lifecycle/recovery/config mutation.

If the semantic chain reports success but final system state is inconsistent, verdict is `FAIL`; do not normalize.

## Required evidence/report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260829-136-final-dashboard-durable-delivery-acceptance.md`

The report must include:

- exact Task-136 coordination start HEAD;
- accepted candidate/package/fingerprint identity;
- authoritative launcher/root and preflight;
- exact zero-baseline counts/IDs;
- exact fresh nonce and semantic message text;
- proof nonce did not exist before Send;
- Dashboard/session identity sufficient to establish real UI path without unnecessary private content;
- exact one-send activation evidence and timestamp;
- explicit ledger `Send = 1 / 1`, resend `0`;
- Ticket ID and durable creation/event ordering;
- affirmative Ticket-before-inference proof;
- Ticket status/event/workflow/direct-recovery execution history;
- durable result and validator evidence;
- outbox/delivery row IDs/status/attempt/ack evidence;
- exactly-once / no-duplicate proof using pre/post deltas;
- final visible Dashboard outcome classification;
- final runtime/provider/delivery/SQLite/model snapshot;
- explicit no manual retry/cleanup/lifecycle/recovery/normalization;
- PASS/FAIL/BLOCKED and first-failure evidence if not PASS.

Retain detailed local evidence paths in the report. Do not publish unrelated conversation history or secrets.

Then STOP for independent ChatGPT review.

Do not merge, tag, publish a GitHub Release, or automatically open a release/finalization task.

## Hard fence

Forbidden except for the one explicitly authorized Dashboard semantic submission:

- any second semantic Send or resend;
- semantic message injection through CLI/Gateway/API/database/test harness;
- source/harness/runtime/plugin edits;
- install/install-over/reset/uninstall/reinstall;
- start/stop/restart/enable/disable;
- recovery suite/crash injection;
- provider/model/OpenClaw/config mutation;
- manual Ticket creation/dispatch/cancel;
- manual outbox retry/ack/delivery mutation;
- database writes/migrations/cleanup;
- process kill;
- scheduled-task/service mutation;
- manual normalization;
- reboot;
- credential/secret access;
- unrelated external side effects;
- merge/tag/release;
- force push.

The one Dashboard Send is the only semantic external action authorized by this task.
