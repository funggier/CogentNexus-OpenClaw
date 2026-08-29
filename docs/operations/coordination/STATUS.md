# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `LIVE_WINDOWS_FINAL_DASHBOARD_DURABLE_DELIVERY_SINGLE_ATTEMPT`  
**Updated:** 2026-08-30 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator requested continuation and changed the UI-control policy: Hermes must use `control-mouse-keyboard-use-desktop` first and ask the operator only when skill-guided control cannot produce/prove the required non-semantic UI effect, with stricter no-duplicate handling at Send  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260830-151-final-dashboard-durable-delivery-acceptance.md`](tasks/CNX-20260830-151-final-dashboard-durable-delivery-acceptance.md)

Task ID:

`CNX-20260830-151`

## Task-150 accepted result

Report:

`docs/operations/coordination/reports/CNX-20260830-150-runtime-lifecycle-stop-start-restart-disable-enable-acceptance.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260830-150-runtime-lifecycle-stop-start-restart-disable-enable-acceptance-review.md`

Disposition: **ACCEPT**.

Accepted production implementation SHA remains:

`fb5781c1abd68280760bd5b3b4a65fabd8a60e58`

## Plan position

The approved Full Stabilization plan orders the final live stages:

`M clean uninstall → N fresh install → O lifecycle → P final Dashboard semantic/durable delivery → Q final acceptance matrix`.

Task 151 is the Phase-P single semantic attempt.

## Desktop-control-first policy

Hermes/Codex must load/read and follow the skill:

`control-mouse-keyboard-use-desktop`

before asking the operator to click/focus/type/paste or activate a normal desktop control.

For composer/focus/pre-send actions:

- identify the exact Firefox Dashboard control;
- perform the skill-guided action;
- verify the expected UI effect;
- only if the correctly targeted action has no effect, or a reliable target cannot be established, request the specific operator action.

For Send:

- if no Send activation has occurred and a trustworthy target cannot be established, operator fallback for one Send is allowed;
- if a Send activation/click has already occurred and its effect is ambiguous, do not request another Send. Treat the single-attempt budget as consumed/ambiguous and observe/classify read-only.

No blind repeated desktop clicks are authorized.

## Task-151 durable authority

The Send budget is exactly `1 / 1`. Once consumed, the nonce is permanently retired and no resend/alternate semantic route is authorized.

PASS requires the full durable chain, not merely a visible answer:

- Ticket-first accepted before inference;
- exactly one direct model call;
- exact visible `ACK <NONCE>` once;
- exactly one durable direct-result `cnx_assistant_delivery` row;
- row reaches delivered state;
- Ticket `delivery_confirmed_at` populated;
- exactly one `delivery_confirmed` and one `completed` event;
- Ticket terminal `completed`;
- no duplicate inference/delivery/recovery/regeneration;
- redacted observability contains no raw semantic content/nonce/credentials;
- final pending `0`, SQLite `ok`, Gateway/Ollama healthy.

If the visible ACK appears but durable capture/settlement is absent, the result is FAIL and must not be converted to PASS from UI evidence.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260830-151-final-dashboard-durable-delivery-acceptance.md`

The report must state which UI actions were skill-driven versus operator fallback and why.

Then stop for independent ChatGPT review. Phase Q, merge, tag, release and promotion remain unauthorized until that review.

## Hard fence

No second Dashboard Send/resend; no alternate semantic transport; no manual Ticket/workflow/outbox/delivery/recovery/database mutation; no lifecycle/reset/install/uninstall/reinstall; no crash/recovery injection; no manual plugin/config/controller/ownership/process/service/task normalization; no reboot; no credentials/secrets; no merge/tag/GitHub Release; no force push.
