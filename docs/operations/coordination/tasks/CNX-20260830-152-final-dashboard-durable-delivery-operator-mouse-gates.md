# CNX-20260830-152 — Final Dashboard Durable-Delivery Acceptance With Operator Mouse Gates

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_FINAL_DASHBOARD_DURABLE_DELIVERY_OPERATOR_MOUSE_GATES`
Executor: Hermes/Codex; operator owns composer click and Send click

## Objective

Repeat Phase P after Task 151 proved automated mouse Send activation unreliable. This is a new single-attempt semantic acceptance with a fresh nonce. Task 151 created no Ticket/model/delivery side effect, but its nonce and Send ledger are permanently retired.

PASS requires:

`accepted → routed → direct_model_call_started → direct_model_call_ended → response_ready → direct_response_durable / cnx_assistant_delivery staged → native delivery → delivery_confirmed → completed`

## Frozen product authority

Accepted production implementation:

`fb5781c1abd68280760bd5b3b4a65fabd8a60e58`

Expected installed plugin fingerprint:

`12c6d1b5b6ffd938353dd60c5d6190c34a609663369f619ff4fc7cbd176119e0`

Expected installed `namespace_ownership.py` SHA-256:

`10dda985e6d4553a73a8cdd3ef7f660937482c3ef0c2d2da8d15bcbfe8d39b66`

## Prepared Dashboard state

The operator has already created a brand-new Dashboard session before Task-152 execution.

Hermes/Codex must **not create another session automatically**. It must instead verify the currently prepared Dashboard target is genuinely fresh and empty:

- authenticated Firefox OpenClaw Dashboard;
- no Task-151 draft/message in the current target;
- `Ready to chat` or equivalent empty-session state;
- `Message Assistant` composer empty;
- exact fresh PID/HWND rediscovered;
- no new durable Ticket/model/delivery/outbox side effect from the session creation itself.

If the current session is not provably fresh/empty, stop `BLOCKED` and ask the operator to prepare a new session; do not attempt semantic Send.

## Desktop-control policy

Do **not** use `control-mouse-keyboard-use-desktop` or another automated mouse method for the semantic mouse gates.

Operator owns exactly these physical mouse actions:

1. manually click the exact `Message Assistant` composer when instructed;
2. manually click the real Dashboard `Send message` control exactly once when instructed.

Hermes/Codex may enter/paste the exact prompt after operator focus is established. Task 151 proved the text-entry path works. The operator does not need to type the acceptance prompt unless executor text entry itself fails.

No automated click of the Send control is authorized.

## Phase A — fresh authority and read-only preflight

Before browser semantic input:

1. Fetch remote branch `agent/v0.9.3-full-stabilization` fresh.
2. Verify `ACTIVE.md` and `STATUS.md` still authorize Task 152 and no matching report/review/successor supersedes it.
3. Verify installed provenance/ownership exactly.
4. Verify controller `managed`, desired Gateway/provider `running/running`, selected provider `ollama`, one canonical non-reparse plugin enabled/loaded, Gateway/Ollama healthy, recovery/delivery `READY` read-only, pending outbox `0`, SQLite integrity `ok`, no active direct model/recovery/delivery work, and no transaction/rollover residue.
5. Record exact baseline counts for `tickets`, `ticket_events`, `cnx_direct_model_call`, `cnx_direct_recovery`, `cnx_assistant_delivery`, `ticket_outbox`, and `cnx_sessions`.
6. Record configured route using metadata only; no inference/provider semantic probe.
7. Freshly rediscover authenticated Firefox Dashboard PID/HWND.
8. Verify the operator-prepared current session is fresh/empty and composer empty.
9. Prove exact target HWND foreground.

Any ambiguity before semantic input => `BLOCKED`, Send count `0`.

## Phase B — operator composer-focus gate

1. Executor identifies the exact Firefox Dashboard and exact `Message Assistant` composer.
2. Executor proves exact target HWND foreground.
3. Executor instructs operator to click the exact composer once with the real mouse.
4. Operator clicks once and does not click elsewhere.
5. Executor re-verifies foreground/session/composer.

A non-sent sentinel may be used only if needed to prove typing target. Hermes may type/clear the sentinel without Enter/Send. Durable semantic counts must remain unchanged.

If focus cannot be proven, stop `BLOCKED` before prompt composition.

## Phase C — fresh nonce and executor text composition

1. Generate a new nonce never used previously, including not Task-151 nonce.
2. Prove it is absent from durable pre-existing content.
3. Exact prompt form:

```text
CogentNexus final durable-delivery acceptance <NONCE>. Reply with exactly: ACK <NONCE>
```

4. Hermes/Codex enters/pastes exactly one complete copy into the already manually focused composer using the proven text-entry path.
5. Visually verify exactly one complete message, nonce exactly twice, no stale/partial/duplicated draft, no Send/Enter yet, and durable counts unchanged.

If composition is wrong, it may be corrected before Send while the Send budget remains `0 / 1`; do not accidentally press Enter. If exact composition cannot be proven, clear without Send and stop `BLOCKED`. Retire any ambiguous nonce.

## Phase D — operator Send gate

Only after exact prompt verification:

1. Executor explicitly tells the operator that Send is authorized now.
2. Operator manually clicks the real Dashboard `Send message` control exactly once with the real mouse.
3. Immediately record Send ledger `1 / 1 consumed` and retire nonce permanently.
4. Executor must not click Send, press Enter to submit, or ask operator to Send again.

If activation status is ambiguous after the click, treat budget as consumed and do not retry.

After the one Send, all work is read-only observation only.

## Phase E — required durable proof

PASS requires for the fresh nonce:

- exactly one new Ticket;
- durable `accepted` before `direct_model_call_started`;
- exactly one `routed`;
- exactly one direct model-call row and call ends;
- exact configured route;
- exactly one `response_ready`;
- exactly one `cnx_assistant_delivery` row with `kind='direct_result'`;
- durable delivery text equals exactly `ACK <NONCE>` before marker/native interpretation;
- singular idempotency key for Ticket/generation;
- delivery row reaches `delivered`, `delivered_at` populated;
- Ticket `delivery_confirmed_at` populated;
- exactly one `delivery_confirmed` event;
- exactly one `completed` event;
- Ticket terminal `completed`;
- exactly one visible Firefox assistant reply equal to `ACK <NONCE>`;
- no duplicate model call/recovery/regeneration/delivery;
- pending outbox `0`;
- no unexpected failure-delivery event;
- final SQLite integrity `ok`;
- Gateway/Ollama healthy and recovery/delivery safe.

Direct Dashboard delivery may legitimately have zero `ticket_outbox` rows.

## Telemetry privacy

Inspect only bounded redacted `delivery-observe` evidence. No raw prompt/response/nonce/run/session identifier/credential may appear in telemetry evidence or report.

## Failure policy

This is single-attempt. After Send is consumed, never retry. Classify only the first proven failing boundary.

## Hard fence

No automated Send click; no second Send/resend; no alternate semantic channel; no manual semantic/database mutation; no reset/uninstall/install/reinstall; no lifecycle commands; no crash/recovery injection; no manual plugin/config/controller/process/service/task normalization; no reboot; no credentials/secrets; no merge/tag/release; no force push.

## Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260830-152-final-dashboard-durable-delivery-operator-mouse-gates.md`

Then stop for independent ChatGPT review. Do not create Phase Q or release state yourself.
