# CNX-20260830-151 — Final Dashboard Semantic / Durable-Delivery Acceptance

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_FINAL_DASHBOARD_DURABLE_DELIVERY_SINGLE_ATTEMPT`
Executor: Hermes/Codex using `control-mouse-keyboard-use-desktop` first, with operator fallback only when needed

## Objective

Execute Phase P of `CogentNexus_OpenClaw_Full_Stabilization_and_Final_Acceptance_Plan.md` against the exact accepted installed v0.9.3 candidate.

This is the final single-attempt semantic proof. It must prove not only a visible Firefox Dashboard reply, but the complete durable lifecycle:

`accepted → routed → direct_model_call_started → direct_model_call_ended → response_ready → direct_response_durable / cnx_assistant_delivery staged → native delivery → delivery_confirmed → completed`

Task 137 proved that a visible ACK without durable capture is a failure. Task 138 repaired that exact callback boundary. Task 151 is the real-runtime acceptance of that repair.

## Frozen product authority

Accepted production implementation:

`fb5781c1abd68280760bd5b3b4a65fabd8a60e58`

Expected installed plugin fingerprint:

`12c6d1b5b6ffd938353dd60c5d6190c34a609663369f619ff4fc7cbd176119e0`

Expected installed `namespace_ownership.py` SHA-256:

`10dda985e6d4553a73a8cdd3ef7f660937482c3ef0c2d2da8d15bcbfe8d39b66`

Task 150 ended in healthy `managed` state with semantic database counts zero and Dashboard semantic Send count zero. Re-verify; do not assume.

## Desktop-control policy for this task

Before asking the operator to click, focus, type, paste, or activate a normal desktop control, Hermes/Codex must first load/read and follow the skill named:

`control-mouse-keyboard-use-desktop`

Use that skill as the primary procedure for desktop targeting and input verification.

Default rule:

1. identify the exact Firefox Dashboard window/control;
2. use the skill-guided mouse/keyboard procedure;
3. verify the expected UI effect immediately;
4. only if the action was correctly targeted/executed but the expected non-semantic UI effect still did not occur, or the skill cannot establish a reliable target, ask the operator to perform that specific action.

Do not ask the operator merely because desktop automation is inconvenient.

For non-semantic focus/composer actions, a failed correctly targeted skill-guided action may fall back to the operator.

For the semantic **Send** boundary, duplicate prevention is stricter:

- if the executor has **not yet activated Send** and cannot establish a trustworthy Send target, it may ask the operator to activate Send once;
- if the executor has already activated/clicked Send and the result is ambiguous, the Send budget is treated as consumed/ambiguous: **do not ask the operator to click Send again**; stop and classify the result rather than risking duplicate delivery.

## Phase A — fresh authority and read-only preflight

Before any browser semantic input:

1. Fetch GitHub remote branch `agent/v0.9.3-full-stabilization` fresh.
2. Verify `ACTIVE.md` and `STATUS.md` still authorize Task 151 and no matching report/review/successor supersedes it.
3. Re-verify installed provenance and ownership.
4. Re-verify:
   - controller `managed`;
   - desired Gateway/provider `running/running`;
   - selected provider `ollama`;
   - one canonical non-reparse CNX plugin, enabled/loaded;
   - Gateway healthy on loopback;
   - Ollama healthy/ready;
   - recovery `READY`, read-only, no active incident;
   - delivery `READY`, read-only, pending outbox `0`;
   - SQLite `PRAGMA integrity_check=ok` through read-only access;
   - no active direct model call/recovery/delivery work;
   - transaction/rollover residue absent.
5. Record exact pre-send counts for at least:
   - `tickets`;
   - `ticket_events`;
   - `cnx_direct_model_call`;
   - `cnx_direct_recovery`;
   - `cnx_assistant_delivery`;
   - `ticket_outbox`;
   - `cnx_sessions`.
6. Record the configured provider/model route using configuration/runtime metadata only. Do not issue a separate inference/provider semantic probe.
7. Freshly rediscover the authenticated Firefox OpenClaw Dashboard PID/HWND. Do not reuse historical PID/HWND assumptions.
8. Use a dedicated fresh/empty Dashboard target session. Prove the `Message Assistant` composer is empty.
9. Prove `GetForegroundWindow` equals the exact target Firefox HWND.

If any preflight state is ambiguous, active work exists, the session is not fresh/empty, ownership/provenance drifts, or the exact browser target cannot be proven: verdict `BLOCKED` and stop before semantic input.

## Phase B — skill-first input-target proof

This gate is **desktop-control first**, not operator-first.

1. Executor identifies and describes the exact Firefox Dashboard window and exact `Message Assistant` composer.
2. Executor proves the target Firefox HWND is foreground.
3. Executor loads/uses `control-mouse-keyboard-use-desktop` and performs one controlled skill-guided focus action on the exact composer.
4. Executor verifies the expected focus/composer effect.
5. If the skill-guided action was correctly targeted but the composer still did not receive focus, or reliable focus cannot be proven, then and only then ask the operator to click the exact composer once with the real mouse.
6. After any operator fallback click, the operator must not click another window and the executor re-verifies exact foreground HWND/session/composer.
7. Do not perform blind repeated clicks.

An optional non-sent focus sentinel is authorized only if needed to prove typing target. If used:

- generate a fresh non-semantic sentinel;
- use the skill-guided typing procedure first;
- type it without Enter/Send;
- visually verify it appears exactly once in the intended composer;
- clear it completely without Enter/Send;
- prove durable semantic DB counts did not change.

If focus cannot be proven safely after the skill-first attempt and any necessary operator fallback, verdict `BLOCKED` and stop with Send count `0`.

## Phase C — fresh nonce and exact composer proof

Only after Phase A/B pass:

1. Generate one fresh unique nonce that has never been used in any prior acceptance task.
2. Verify the nonce is absent from relevant pre-existing durable Ticket/event/delivery/outbox content before use.
3. Construct exactly this semantic form:

```text
CogentNexus final durable-delivery acceptance <NONCE>. Reply with exactly: ACK <NONCE>
```

4. Put exactly one complete copy into the composer using the `control-mouse-keyboard-use-desktop` procedure first. Clipboard paste is allowed after focus is proven.
5. Before Send, visually verify:
   - composer contains exactly one complete intended message;
   - no stale/partial/duplicated draft remains;
   - nonce occurrence count is exactly two inside the intended request (request identifier + requested ACK phrase);
   - no Enter/Send has occurred;
   - pre-send durable semantic counts are unchanged.

If exact composition cannot be proven, clear without Send and stop `BLOCKED`. The nonce is retired even if composed but must never be sent later under another task if ambiguity occurred.

## Phase D — exactly one Dashboard Send

This is the single semantic side-effect boundary.

When and only when the executor has verified the exact prompt and explicitly marked Send as authorized:

1. Prefer the `control-mouse-keyboard-use-desktop` skill to target and activate the exact real Dashboard **Send message** control once.
2. If, **before any Send activation**, the executor cannot establish a trustworthy Send target or cannot safely perform the activation with the skill, ask the operator to activate the exact Send control once.
3. Immediately record a durable execution ledger:
   - Send budget `1 / 1 consumed` after activation;
   - nonce retired permanently;
   - no resend authorized.
4. If a skill-guided Send click/activation has already occurred but the UI result is ambiguous, do **not** ask the operator to Send again. Treat the semantic attempt as consumed/ambiguous and proceed only with read-only observation/classification.
5. After Send:
   - no second Send;
   - no Enter-to-resubmit;
   - no editing/resubmission;
   - no alternate Dashboard/API/CLI/Gateway semantic transport;
   - no model/provider inference probe;
   - no executor interruption that triggers a new semantic action.

After the one Send, all activity must be observation/read-only only.

## Phase E — read-only observation and durable proof

Observe until a definitive terminal durable result is proven, with a bounded maximum observation window of 45 minutes. A definitive terminal failure may be classified earlier.

Required PASS evidence for the single fresh nonce/Ticket:

- exactly one new Ticket;
- Ticket `accepted` is durable before `direct_model_call_started`;
- expected `routed` event;
- exactly one direct model-call row;
- model call ends;
- exact frozen configured route is used;
- exactly one `response_ready` boundary;
- exactly one durable `cnx_assistant_delivery` row for `kind='direct_result'`;
- delivery row text equals exactly `ACK <NONCE>` before marker handling/native transport semantics are interpreted;
- delivery row idempotency key is singular for the Ticket/generation;
- durable delivery row reaches `status='delivered'` and `delivered_at` is populated;
- Ticket `delivery_confirmed_at` is populated;
- `delivery_confirmed` event exists exactly once;
- `completed` event exists exactly once;
- Ticket terminal status is `completed`;
- visible Firefox Dashboard assistant reply is exactly `ACK <NONCE>` with no duplicate assistant reply;
- exactly one direct model call, no duplicate recovery/regeneration call;
- no duplicate delivery row/idempotency key;
- no pending outbox remains;
- no unexpected `failure_delivery_suppressed`, `direct_native_delivery_failed`, or terminal failure for this Ticket;
- final SQLite integrity remains `ok`;
- Gateway/Ollama remain healthy after settlement;
- recovery/delivery checks return safe read-only state with pending `0`.

The direct Dashboard path may finish with zero `ticket_outbox` rows; do not invent an outbox requirement. The authoritative durable result for this path is the singular delivered `cnx_assistant_delivery` row plus Ticket delivery confirmation/completion.

## Telemetry privacy acceptance

Inspect only the bounded relevant redacted `delivery-observe` evidence needed to identify the delivery boundary.

PASS requires:

- observability contains no raw prompt;
- observability contains no raw assistant response;
- observability contains no raw semantic nonce;
- observability contains no raw run/session identifiers or credentials;
- only bounded categorical/boolean/digest evidence is used.

Do not copy secrets or raw credentials into the report.

## Failure classification

This task is single-attempt. After the Send ledger is consumed, no retry is permitted.

If PASS is not achieved, stop at the first proven boundary and classify narrowly, for example:

- `FAIL_TICKET_FIRST`
- `FAIL_MODEL_EXECUTION`
- `FAIL_DURABLE_CAPTURE`
- `FAIL_NATIVE_DELIVERY_SETTLEMENT`
- `FAIL_DUPLICATE`
- `FAIL_UI_MISMATCH`
- `FAIL_RUNTIME_OR_PRODUCT`
- `BLOCKED`

Use redacted observability only to identify the first failing boundary. Do not guess beyond proven evidence.

## Hard fence

- No second Dashboard Send/resend.
- No alternate semantic channel or synthetic semantic injection.
- No manual Ticket/workflow/outbox/delivery/recovery/database mutation.
- No reset/uninstall/install/reinstall.
- No stop/start/restart/disable/enable.
- No crash/recovery injection.
- No manual plugin/config/controller/ownership normalization.
- No manual process/service/task lifecycle mutation.
- No reboot.
- No credentials/secrets disclosure.
- No merge/tag/GitHub Release.
- No force push.

## Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260830-151-final-dashboard-durable-delivery-acceptance.md`

Report must include:

- verdict;
- exact GitHub authority/installed provenance;
- preflight/baseline counts;
- Firefox/session/focus proof without secrets;
- whether each UI action used `control-mouse-keyboard-use-desktop` or operator fallback and why;
- fresh nonce and exact prompt form;
- Send ledger `1 / 1` or pre-send `0 / 1` if BLOCKED;
- Ticket/model/delivery durable timeline;
- final DB/runtime/UI evidence;
- duplicate accounting;
- telemetry privacy result;
- explicit statement that no retry/alternate semantic transport occurred.

Then stop for independent ChatGPT review. Do not create Phase-Q acceptance or release state yourself.
