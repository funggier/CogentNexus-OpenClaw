# CNX-20260831-171 — Hermes Dashboard Exactly-One-Send Durable-Delivery Reacceptance

Status: `READY_HERMES`

Execution mode: `WINDOWS_DASHBOARD_EXACTLY_ONE_SEND_DURABLE_DELIVERY_REACCEPTANCE_HERMES`

Authorization: `CNX-20260831-171_HERMES_DASHBOARD_EXACTLY_ONE_SEND_REACCEPTANCE`

Executor: Hermes/Codex

Coordinator / final reviewer: ChatGPT

## Objective

Perform exactly one controlled semantic Dashboard Send on the Windows instance accepted by Task 170, then determine from native/durable evidence whether the Task-167 repair now provides correct durable delivery without duplicate inference, duplicate visible output, recovery reinjection, or ambiguous settlement.

This is a live semantic acceptance task. It is not a repair task.

## Accepted starting state

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Accepted product repair SHA: `231761fca24c315e90536955d3e384f55e2e232e`
- Installed candidate fingerprint accepted by Task 170: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`
- Task-170 package SHA-256: `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91`
- Pinned OpenClaw: `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c` / `2026.7.1-2`
- Task-170 review: `reviews/CNX-20260831-170-hermes-windows-install-over-provenance-health-review.md`
- Pre-Task-171 known durable state from Task 170: tickets `3`, direct model calls `3`, assistant delivery `0`, direct recovery `0`, outbox `0`, SQLite integrity `ok`.

Before any semantic side effect, re-read fresh remote `ACTIVE.md`, `STATUS.md`, current remote HEAD, and confirm the Task-171 report is absent. Reconfirm installed fingerprint, pinned OpenClaw, plugin loaded/enabled, Gateway/provider readiness, and SQLite integrity/read-only baseline.

If preflight does not match the accepted Task-170 checkpoint materially, do **not** Send. Report `BLOCKED` with evidence.

## Exactly-one semantic action

Generate one unique Task-171 nonce immediately before the action. Use a form that is globally recognizable, for example:

`T171-<UTC timestamp>-<random suffix>`

Send exactly one Dashboard prompt whose requested answer is deterministic and includes the nonce, for example:

`CNX-171 acceptance <NONCE>. Reply with exactly: CNX-171-ACK-<NONCE>`

Record the exact prompt text and expected exact answer before Send.

Then perform **exactly one semantic Dashboard Send**.

### Absolute no-retry rule

After the Send action is issued, no second semantic Send is authorized under any circumstance, including:

- timeout;
- blank UI;
- partial UI response;
- transport error;
- model error;
- Ticket failure;
- missing marker;
- missing durable row;
- delayed transcript;
- ambiguous settlement;
- executor uncertainty.

Do not use `chat.inject`, alternate semantic surfaces, manual replay, model regeneration, recovery injection, or a second inference to clarify the result.

## Required evidence after the single Send

Observe until the direct-result/Ticket path reaches a stable terminal or clearly timed-out state according to existing product policy. Collect read-only evidence sufficient to reconstruct the single action.

At minimum record:

### 1. Dashboard/UI observation

- exact session key;
- exact prompt/nonce;
- number of visible user messages containing nonce;
- number of visible assistant messages containing nonce;
- exact assistant response if present;
- whether any duplicate visible response occurred.

### 2. Native transcript authority

Identify the native OpenClaw session transcript file/record for the Dashboard session and prove:

- user nonce record count;
- assistant nonce record count;
- exact expected-answer record count;
- assistant native record ID/timestamp;
- CogentNexus delivery marker presence/absence;
- idempotency/delivery identity fields present on the persisted assistant record, if represented there;
- transcript SHA-256 after the observation.

The native persisted transcript remains the delivery authority. UI visibility alone is not success.

### 3. Ticket/run/model evidence

Record:

- Ticket ID;
- Run ID;
- request/idempotency identity;
- Ticket event sequence with timestamps;
- model provider/model;
- model-call count attributable to the nonce/run;
- direct model-call start/end/outcome/duration;
- final Ticket status;
- `delivery_confirmed_at` value;
- `durableDelivery`/equivalent state if exposed.

Exactly one model execution for this semantic request is required. Zero or more than one is a failure/blocked outcome according to the observed cause; do not compensate by retrying.

### 4. Durable delivery row

Inspect `cnx_assistant_delivery` read-only and prove for the Task-171 run:

- row count;
- Ticket/run binding;
- idempotency key;
- staged text/hash identity;
- claim/owner fields if present;
- final delivery/settlement state;
- timestamps;
- whether the row was settled only after native persistence evidence.

Expected success requires exactly one durable row for the result and correct post-persistence settlement.

### 5. Duplicate/recovery/outbox safety

Inspect read-only:

- `cnx_direct_recovery` scoped to the run;
- `ticket_outbox` scoped to the run;
- any recovery-attempt counters/events;
- any failure-delivery suppression or regeneration events;
- native transcript duplicates.

Success requires no second inference, no semantic recovery reinjection, no duplicate durable result, and no duplicate visible/native assistant result.

### 6. Post-state health

After the semantic path settles or fails closed, re-run read-only health checks:

- controller/system health;
- Gateway health/version;
- provider/Ollama readiness;
- plugin inventory/fingerprint;
- SQLite integrity;
- pending delivery/outbox/recovery state.

Do not restart or repair a degraded runtime inside Task 171. If the task itself exposes a health failure, record it.

## Acceptance contract

Task 171 may report `PASS` only if all of the following are proven:

1. exactly one Dashboard semantic Send was issued;
2. exactly one model execution produced the requested semantic result;
3. exactly one native persisted assistant result exists for the nonce/expected answer;
4. the native assistant record contains the expected CogentNexus delivery marker/identity required by the repaired path;
5. exactly one `cnx_assistant_delivery` result is durably staged/bound to the correct Ticket/run;
6. post-persistence settlement succeeds and `delivery_confirmed_at` is non-null/authoritative;
7. final Ticket reaches the expected successful terminal state;
8. no duplicate UI/native result, no second inference, no recovery reinjection, and no conflicting outbox/delivery row occurs;
9. installed fingerprint/OpenClaw pin/runtime/storage integrity remain acceptable after the experiment.

If any required property is false or cannot be proven, report `FAIL`, `BLOCKED`, or `UNPROVEN` as appropriate. Never retry the semantic action.

## Hard fence

Task 171 authorizes only:

- read-only preflight/observation;
- exactly one semantic Dashboard Send;
- read-only post-action evidence collection;
- publication of the Task-171 report.

Task 171 does **not** authorize:

- a second Dashboard Send;
- `chat.inject` or another semantic input surface;
- manual model invocation;
- recovery injection/regeneration;
- installer execution, uninstall, reinstall, reset, rollback, or repair;
- Gateway/Ollama/Supervisor/OpenClaw restart or lifecycle mutation;
- manual Ticket/workflow/result/outbox/delivery/database/transcript mutation;
- production/source/test/workflow repair;
- OpenClaw/dependency upgrade;
- release/tag/package publication;
- default/release merge;
- force push.

If the experiment fails, preserve the failure exactly and stop for ChatGPT review.

## Required report

Publish only after evidence collection is complete:

`docs/operations/coordination/reports/CNX-20260831-171-hermes-dashboard-exactly-one-send-durable-delivery-reacceptance.md`

The report must follow `EXECUTOR_REPORT_CONTRACT.md` and include:

- disposition;
- exact authority/head and installed provenance;
- exact prompt/nonce/session/Ticket/run/model identifiers;
- one-Send and one-model proof;
- native transcript proof;
- durable row and settlement proof;
- duplicate/recovery/outbox proof;
- post-state health;
- acceptance matrix;
- anomalies/contradictions/residual uncertainty;
- hard-fence compliance;
- Reviewer Verification Packet with 5–10 critical claims and narrow independent checks.

After report publication, stop. No successor action is authorized until ChatGPT review.