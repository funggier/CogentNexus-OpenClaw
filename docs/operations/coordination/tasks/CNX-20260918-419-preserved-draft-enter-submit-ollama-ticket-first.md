# CNX-20260918-419 — Preserved Draft Enter-Key Submit and Ollama Ticket-First Vertical Slice

Status: `COMPLETED_REPORTED`

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Parent: `CNX-20260918-418`
- Executor: `Hermes`
- Reviewer: `ChatGPT`
- Human final authority: `Operator`
- Parent review: `docs/operations/coordination/reviews/CNX-20260918-418-chatgpt-review.md`
- Parent report: `docs/operations/coordination/reports/CNX-20260918-418-preserved-session-ollama-semantic-vertical-slice-report.md`
- Installed source candidate: `c1baa815d6894f0d619d4d3695c61a442e206e38`

GitHub remote is authoritative.

## Historical coordination reconciliation

This task was temporarily marked as a draft during a coordination race while the CNX-418 report was still being finalized. The Operator subsequently authorized and completed the CNX-419 execution under the intended one-shot contract. The authoritative execution evidence is the published CNX-419 report and ChatGPT review.

## Objective

Reuse the exact preserved CNX-418 Dashboard session and its existing unsent nonce draft, submit it through the OpenClaw composer **Enter-key path**, and prove the complete Ticket-first Ollama vertical slice.

Do not click the Send button.
Do not use Ctrl+Enter as a fallback.
Do not create another session.

## Preserved target

- session key: `agent:main:dashboard:6e96fece-c6ad-47b9-bfb4-680dd8a3a75b`
- session ID: `18fab7b9-2fb1-409f-9aed-d79168aaffdc`
- selected route: `ollama/qwen3.8:27b`
- preserved unsent draft:
  `ตอบกลับข้อความนี้เพียงว่า CNX418-20260918T095632Z-2E7A2E6B`
- nonce:
  `CNX418-20260918T095632Z-2E7A2E6B`

The nonce is reusable because CNX-418 proved no semantic request materialized.

## Exact OpenClaw keyboard contract

Installed OpenClaw:

`2026.7.1-2 (0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c)`

Exact source:

`ui/src/pages/chat/components/chat-composer.ts`

When the composer send shortcut is `Enter`, the textarea exposes:

`aria-keyshortcuts="Enter"`

and the exact keydown handler:

1. prevents default newline insertion;
2. commits the textarea draft;
3. calls `props.onSend()`;
4. synchronizes composer state after send.

CNX-419 therefore uses only this keyboard path.

## Send-shortcut preference authority

The Operator explicitly prefers Enter for this acceptance.

Before semantic submission, read the current chat send-shortcut preference.

If it is already `Enter`, make no settings change.

If it is not `Enter`, CNX-419 authorizes exactly one **non-semantic UI preference change** through the normal OpenClaw Settings/Appearance/Chat control to set:

`Send shortcut = Enter`

This preference change must be proven to cause:

- `chat.send = 0`;
- Ticket delta = 0;
- model-call delta = 0;
- transcript delta = 0;
- delivery/outbox delta = 0.

Do not change provider/model or any runtime/configuration outside this chat UI preference.

After the preference is set, require the exact composer textarea to expose `aria-keyshortcuts="Enter"`.

If Enter cannot be established without broader mutation:

`BLOCKED_ENTER_SHORTCUT_NOT_ESTABLISHED`

Stop without semantic send.

## Semantic budget

Semantic submissions: maximum 1.

A semantic submission is considered materialized only when authoritative evidence shows a `chat.send` request or equivalent accepted user input.

CNX-418's failed UIA button Invoke did not materialize a semantic request, so this is not a resend.

After pressing Enter once, do not press Enter again under any result.

## Phase A — runtime and preserved-session preflight

Before any settings/composer interaction, require:

- OpenClaw `2026.7.1-2`;
- controller active/managed;
- exact CNX plugin enabled/loaded;
- Gateway healthy;
- Supervisor healthy;
- maintenance marker absent;
- Recovery READY;
- Delivery READY;
- pending outbox 0;
- SQLite integrity OK;
- no active provider/model call;
- exact preserved session key/ID unchanged;
- transcript still header-only:
  - user messages 0;
  - assistant messages 0;
- target Ticket count 0;
- target model-call count 0;
- target delivery/outbox count 0;
- selected route exactly `ollama/qwen3.8:27b`;
- existing composer draft exactly matches the preserved CNX-418 prompt.

If any of those materially drift:

`BLOCKED_PRESERVED_SESSION_DRIFT`

Do not repair and do not send.

## Phase B — establish Enter shortcut

Read the exact current composer `aria-keyshortcuts` and current Send shortcut preference.

If not Enter:

1. use normal OpenClaw UI settings only;
2. change Send shortcut to Enter exactly once;
3. return to the exact preserved session;
4. require the draft remains exactly unchanged;
5. require session identity remains exact;
6. require route remains `ollama/qwen3.8:27b`;
7. require zero semantic/durable effect from the settings change;
8. require textarea now reports `aria-keyshortcuts="Enter"`.

Do not type a new nonce.

Do not alter the existing draft.

## Phase C — exact one Enter submission

Immediately before Enter:

- focus the exact composer textarea;
- prove it is `document.activeElement` or equivalent UIA focus evidence;
- visually/read-back verify the exact draft;
- verify `aria-keyshortcuts="Enter"`;
- capture fresh Gateway log cursor and durable counters.

Then press:

`Enter`

exactly once.

Do not click Send.
Do not use Ctrl+Enter.
Do not use Shift+Enter.
Do not press Enter a second time.

## Phase D — immediate materialization gate

Immediately after the Enter key action, determine whether the user input materialized.

Require at least one authoritative indicator:

- one Gateway `chat.send` for the exact session and draft/nonce; or
- exact equivalent accepted Dashboard input under this OpenClaw version.

Also require the composer draft clears or the UI enters the normal accepted/sending state consistent with the request.

If no semantic request materializes:

`BLOCKED_ENTER_SUBMIT_NO_SEMANTIC_EFFECT`

Stop. Do not try any alternate shortcut or button.

## Phase E — Ticket-first ordering

If semantic materialization occurs, prove:

- exactly one new Ticket;
- exact preserved session owns the Ticket;
- exactly one accepted lifecycle;
- exactly one routed event;
- admission trace exists;
- accepted/routed are durably committed before correlated model-call start;
- no duplicate Ticket or route;
- no inference bypass.

Failure:
- `BLOCKED_TICKET_FIRST_ORDERING`
- `BLOCKED_DUPLICATE_ADMISSION`

## Phase F — exactly one Ollama inference

Require:

- provider = `ollama`;
- model = `qwen3.8:27b`;
- same session/run/Ticket;
- exactly one model call;
- no retry/second call.

If route differs:
`BLOCKED_SELECTED_ROUTE_NOT_HONORED`

If normal inference fails:
`BLOCKED_OLLAMA_INFERENCE`

## Phase G — visible result and durable completion

Require:

- exactly one assistant result;
- normalized assistant text equals:
  `CNX418-20260918T095632Z-2E7A2E6B`;
- exactly one visible Dashboard reply;
- durable result-ready event/current equivalent;
- durable delivery settlement;
- Ticket terminal `completed`;
- no pending result outbox;
- no recovery duplicate;
- no competing assistant payload;
- no second model call;
- no duplicate visible nonce.

A visible answer alone is not sufficient.

Use:
- `BLOCKED_VISIBLE_NONCE_RESPONSE`
- `BLOCKED_DURABLE_DELIVERY_COMPLETION`
- `BLOCKED_DUPLICATE_SEMANTIC_EFFECT`

as appropriate.

## Phase H — preserve the successful session

If PASS, preserve this same session intact for the next same-session provider/model-switch task.

Do not:

- New Session;
- send a second message;
- reset/delete/compact;
- change provider/model;
- manually mutate durable state.

## PASS classification

`PASS_ENTER_OLLAMA_TICKET_FIRST_VERTICAL_SLICE`

## Hard fences

- New Session/New Chat: 0
- Send-button clicks/UIA Invoke: 0
- Ctrl+Enter submissions: 0
- Enter semantic submission attempts: max 1
- semantic resend/retry: 0
- direct Ollama/model probes: 0
- OpenAI semantic requests: 0
- provider/model selection changes: 0
- Send-shortcut UI preference changes: max 1, only to Enter
- other config mutation: 0
- installer/install-over: 0
- plugin lifecycle mutation: 0
- Gateway restart/reload/repair: 0
- lifecycle start/stop/restart: 0
- manual Ticket/outbox/recovery/SQLite mutation: 0
- manual durable replay/delivery: 0
- session reset/delete/compact: 0
- release/tag/main: 0
- force push/history rewrite: 0
- do not create/start CNX-420 yourself.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260918-419-preserved-draft-enter-submit-ollama-ticket-first-report.md`

Include:

- fresh authority;
- runtime/session preflight;
- exact preserved draft proof;
- send-shortcut setting before/after;
- proof `aria-keyshortcuts="Enter"`;
- zero side effect from any preference change;
- exact Enter press count;
- immediate `chat.send` materialization evidence;
- Ticket/run/model-call IDs;
- accepted/routed/model-start ordering;
- provider/model;
- visible nonce;
- durable completion;
- duplicate/cardinality ledger;
- final preserved-session state;
- final classification.

Then:

1. set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW`;
2. verify local HEAD == remote HEAD;
3. verify clean publication worktree;
4. preserve session if PASS;
5. stop;
6. do not create/start CNX-420.
