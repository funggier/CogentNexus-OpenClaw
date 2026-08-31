# CNX-20260831-173 — Task-171 Read-Only UI Duplicate Verification

Status: `READY_HERMES`

Execution mode: `TASK171_READ_ONLY_UI_DUPLICATE_VERIFICATION_HERMES`

Authorization: `CNX-20260831-173_HERMES_TASK171_READ_ONLY_UI_DUPLICATE_VERIFICATION`

Executor: Hermes/Codex

Coordinator / final reviewer: ChatGPT

## Objective

Close the only remaining Task-171 acceptance gap without creating any new semantic action. Inspect the existing Dashboard session/history read-only and determine whether the frozen Task-171 nonce appears in exactly one visible user message and the expected Task-171 result appears in exactly one visible assistant message, with no duplicate visible result.

This task does not re-run, replay, or modify Task 171.

## Frozen prior action

- Product repair SHA: `231761fca24c315e90536955d3e384f55e2e232e`
- Installed fingerprint: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`
- OpenClaw: `2026.7.1-2`
- Task-171 nonce: `T171-20260831T020446Z-3142A528`
- Exact expected assistant result: `CNX-171-ACK-T171-20260831T020446Z-3142A528`
- Dashboard session key: `agent:main:dashboard:13b27c98-c09c-431e-928f-446175ed1937`
- Native session file identity: `7d2ca55f-ecda-4e24-b924-5f61e75a13b3.jsonl`
- Ticket: `CNXT-b5bf2532-d35d-47db-8951-fcf9f4729abf`
- Run: `8b69bede-030f-4c20-8bb8-0aa99e12422c`
- Task-171 Send count is permanently frozen at `1`.
- Task-173 semantic action budget is `0`.

## Why this task exists

Task 172 proved the native/durable path in detail but its report acknowledged that final visible Dashboard nonce counts remained uncertain. Task-171 acceptance criterion 8 is conjunctive and explicitly requires no duplicate UI/native result.

All non-UI parts of criterion 8 are already supported:

- native user nonce records: `1`;
- native assistant expected-response records: `1`;
- model executions for run: `1`;
- durable delivery rows for Ticket: `1`;
- direct recovery rows: `0`;
- conflicting outbox rows: `0`;
- duplicate durable rows: `0`.

Task 173 must address only the visible Dashboard duplicate condition.

## Fresh authority preflight

Before browser/UI observation:

1. read fresh remote branch HEAD;
2. read fresh `ACTIVE.md` and `STATUS.md`;
3. confirm Task 173 is authorized;
4. confirm this Task-173 report is absent;
5. confirm no successor or conflicting task has replaced Task 173;
6. record current browser/Dashboard state without typing or submitting anything.

If authority is stale or conflicting, report `BLOCKED` and stop.

## Authorized read-only UI actions

The executor may only perform non-semantic observation needed to inspect existing history, including:

- activate/focus the already-open Dashboard browser window;
- open the existing Dashboard/session history read-only if not currently foregrounded;
- scroll message history;
- expand/collapse non-semantic history UI when needed;
- use browser/accessibility/DOM inspection that does not edit page state semantically;
- capture screenshots;
- save read-only DOM/accessibility/message-list evidence;
- hash captured evidence;
- perform read-only local transcript/SQLite checks only to correlate the same frozen Task-171 identity.

No action may submit or change conversation semantics.

## Absolute semantic hard fence

Task 173 authorizes **zero** semantic actions.

Do not:

- click Dashboard Send;
- press Enter in or near the composer;
- type/paste text into the composer;
- focus the composer if avoidable;
- use `chat.inject`;
- call an alternate semantic input surface;
- invoke the model manually;
- invoke recovery/regeneration;
- create a replacement acceptance message;
- repeat the Task-171 prompt;
- mutate Ticket/database/transcript/delivery state;
- restart Gateway/Ollama/Supervisor/OpenClaw;
- install/uninstall/reinstall/reset/rollback;
- change product/source/test/workflow/dependency files;
- publish release/tag/package;
- merge or force push.

If any UI state is ambiguous, do not resolve ambiguity by sending or regenerating anything.

## Required UI verification

Inspect the existing Dashboard session/history corresponding to the frozen Task-171 session and nonce.

Record separately:

1. visible user message count containing exact nonce `T171-20260831T020446Z-3142A528`;
2. visible assistant message count containing exact expected result `CNX-171-ACK-T171-20260831T020446Z-3142A528`;
3. whether any second assistant bubble/card/message renders the same expected result;
4. whether any duplicate user message containing the nonce is visible;
5. whether the visible assistant result is associated with the same session/history context;
6. any UI virtualization/pagination/history-loading limitation that prevents a complete count.

Prefer exact DOM/accessibility message-node counting over visual inference when available. Use screenshots as corroboration, not as the sole count if the message list is virtualized or partially off-screen.

## PASS contract

Task 173 may report `PASS` only if it proves all of the following from current read-only UI evidence:

1. exactly one visible user message contains the Task-171 nonce;
2. exactly one visible assistant message contains the exact Task-171 expected result;
3. no duplicate visible assistant result exists for that nonce/result in the relevant Dashboard session history;
4. no duplicate visible user nonce exists;
5. the observation required zero semantic action;
6. no runtime/product/durable-state mutation was performed.

If the Dashboard history is unavailable, virtualized in a way that prevents complete counting, or otherwise cannot prove the visible duplicate condition, report `UNPROVEN` or `BLOCKED`. Do not infer PASS from native transcript evidence already accepted by Task 172; this task exists specifically to close UI visibility.

## Evidence requirements

Preserve at minimum:

- exact observation timestamp;
- browser/window/session identity;
- screenshot(s) showing the relevant user/assistant message pair where possible;
- DOM/accessibility/message-list extraction with exact count if available;
- SHA-256 hashes for critical screenshots/text dumps;
- explicit semantic-action count `0`;
- any scrolling/history-loading steps used;
- read-only correlation to nonce/session/Ticket/run;
- contradictions or limitations.

## Acceptance matrix

Report a compact matrix covering:

| Criterion | Verdict | Evidence |
|---|---|---|
| One visible user nonce | PASS/FAIL/UNPROVEN | exact UI/DOM pointer |
| One visible assistant expected result | PASS/FAIL/UNPROVEN | exact UI/DOM pointer |
| No duplicate visible result | PASS/FAIL/UNPROVEN | exact count/evidence |
| No duplicate visible user nonce | PASS/FAIL/UNPROVEN | exact count/evidence |
| Zero semantic action | PASS/FAIL | action ledger |
| No runtime/product/durable mutation | PASS/FAIL | observation/change fence |

A `PASS` disposition is invalid if any required UI count is `UNPROVEN`.

## Reviewer Verification Packet

Include 3–6 critical claims with exact evidence and narrow reviewer checks. At minimum include:

- exact visible user nonce count;
- exact visible assistant expected-result count;
- no duplicate visible result;
- zero semantic action;
- report-only publication fence.

## Required report

Publish only after observation is complete:

`docs/operations/coordination/reports/CNX-20260831-173-hermes-task171-read-only-ui-duplicate-verification.md`

The report must follow `EXECUTOR_REPORT_CONTRACT.md` and must not claim semantic acceptance beyond the narrow UI condition.

After report publication, stop for ChatGPT review. No successor semantic or lifecycle action is authorized.
