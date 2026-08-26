# CNX-20260826-076 — Final Semantic Ticket → Ollama → Delivery Acceptance

Status: `READY_FOR_HERMES`

Execution mode: `LIVE_BOUNDED_REAL_USER_MESSAGE_TICKET_OLLAMA_DELIVERY_ACCEPTANCE`

Current authorization: `FINAL_SEMANTIC_ACCEPTANCE_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes after the operator's continuation signal

## Goal

Prove one real user-message flow through the installed CogentNexus-OpenClaw MANAGED product:

`real OpenClaw owner-session message -> Ticket committed before inference -> Ollama-backed conversational inference -> durable response-ready/delivery evidence -> user-visible final response`

This is the final functional acceptance gate for the current v0.9.3 OpenClaw integration.

Do not simulate the semantic path by calling `TicketStore.accept()`, inserting SQLite rows, using a ticket CLI shortcut, invoking the model directly, or fabricating OpenClaw hook events. The message must enter through a supported OpenClaw user/session surface that triggers the installed plugin's real `before_agent_run`, agent execution, and final delivery hooks.

## Accepted predecessor

Task 075 result:

`PASS_INSTALL_OVER_SOURCE_LIVE_PARITY_NO_FLASH`

Independent review:

Decision: `ACCEPT`

Disposition:

`ACCEPT_INSTALL_OVER_SOURCE_LIVE_PARITY_NO_FLASH`

Accepted live source:

`79b51ed06363f6e8862c491ee0a313ddb412c806`

Accepted live properties before this task:

- controller MANAGED;
- desired Gateway/provider running, provider Ollama;
- Gateway Ready and dashboard healthy;
- exactly one canonical `cogentnexus-openclaw@0.9.3` plugin active;
- ticket-first, pre-inference admission, enforced mode, auto-resume and auto-workflow-completion enabled;
- CogentNexus-owned foreground/background runtime;
- no durable Hermes/Codex/temp dependency;
- Scheduled Task PT1M healthy;
- source/live parity with `79b51ed...`;
- no-flash re-proven over five natural PT1M ticks;
- ownership/AGENTS/SQLite health accepted.

Task 076 MUST NOT reinstall, install-over, uninstall, reset or clean anything.

## Product semantics being accepted

The installed plugin's actual direct-lane ticket-first path is:

1. `before_agent_run` receives an eligible owner-session prompt;
2. when `ticketFirst=true`, `TicketStore.accept()` commits the Ticket and `accepted` event before inference;
3. classifier routes the bounded simple prompt to `direct` (`workflow_eligible=0`) and inference proceeds;
4. OpenClaw executes the configured conversational model through provider Ollama;
5. successful `agent_end` records `response_ready` for the direct Ticket;
6. successful final reply delivery through `reply_dispatch`/`message_sent` confirms delivery;
7. Ticket reaches `completed` with `delivery_confirmed_at` and events `delivery_confirmed` + `completed`.

The final acceptance should exercise this minimal direct lane intentionally. Do not force a durable workflow merely to make the test larger; the purpose is to prove that every eligible simple user turn is durably Ticketed before conversational inference and that its real answer is durably tied to delivery.

## Phase A — read-only preflight

Before sending the semantic message:

1. Fetch/read current remote `ACTIVE.md`, `STATUS.md`, Task 076, Task-075 report/review, and Task-074/073 acceptance lineage.
2. Verify remote coordination HEAD and record execution starting HEAD.
3. Create an evidence directory outside product boundaries under `%LOCALAPPDATA%\Temp`.
4. Re-prove current live state remains materially Task-075 accepted:
   - controller `managed`;
   - provider Ollama and desired states running;
   - Gateway Ready/connectivity/dashboard healthy;
   - exactly one canonical CNX v0.9.3 plugin active;
   - launcher/task owned-runtime binding unchanged;
   - Supervisor healthy;
   - ownership verify passes;
   - AGENTS managed block exactly once;
   - SQLite `integrity_check=ok`;
   - Ollama healthy and model inventory unchanged.
5. Locate the authoritative live Ticket SQLite database through installed config/default product path. Do not guess if config overrides it.
6. Record exact BEFORE snapshots, without mutation:
   - ticket count/status counts;
   - maximum `ticket_events.event_id` (or 0);
   - maximum `ticket_outbox.outbox_id` (or 0);
   - session rows/counts relevant to the chosen owner session if available;
   - pending direct execution/outbox state;
   - latest relevant OpenClaw/Gateway log cursor/timestamp sufficient to isolate the semantic run.
7. Verify there is no pre-existing unfinished Ticket for the chosen acceptance session that could make attribution ambiguous. If there is, do not delete/reset it; choose a clean supported owner session or STOP and report ambiguity.

### Hard gate A

Proceed only if the live product remains healthy and the semantic run can be uniquely attributed without resetting existing durable state.

## Phase B — choose a real OpenClaw owner-session path

Use one supported OpenClaw user-message/session surface that actually enters the installed plugin's normal owner-session hook path. Examples may include the product's supported WebChat/session-send/agent message surface as actually available in OpenClaw `2026.7.1-2`; determine the exact supported command/API from local help/runtime evidence rather than inventing syntax.

The path MUST:

- resolve a real owner session key;
- trigger `before_agent_run` in the installed plugin;
- execute the normal conversational inference pipeline;
- produce a real final assistant response through OpenClaw's delivery path.

The path MUST NOT:

- call the Ticket database directly;
- call `cnxclaw ticket ...` as the semantic input;
- call Ollama directly;
- call internal plugin functions/test harnesses;
- synthesize hook events;
- bypass OpenClaw reply delivery.

Record the exact selected supported surface and why it is a real user-message path.

## Phase C — one bounded semantic message, exactly once

Generate a unique nonce for this task, for example:

`CNXSEM-<UTC timestamp>-<short random suffix>`

Send exactly ONE simple owner message containing that nonce. Use a prompt intentionally expected to remain direct-lane and to have no tool/file/network side effect, for example the semantic equivalent of:

`ตอบกลับข้อความนี้เพียงว่า <NONCE>`

The exact prompt may include a short instruction to echo the nonce, but MUST NOT include durable-contract keywords, multi-step requirements, named artifact creation, tests, external research, file operations or tool actions.

Record:

- exact prompt bytes/text and SHA-256;
- send timestamp;
- owner session key;
- OpenClaw run ID if surfaced;
- user-visible response text and receive/delivery timestamp.

Do not send the message a second time if it appears slow. Wait within a bounded reasonable timeout while observing durable state. A timeout/failure is evidence, not authorization to duplicate the user turn.

## Phase D — prove Ticket-first ordering before inference

Identify the unique Ticket created by the acceptance prompt using exact prompt SHA-256, run ID/session key, creation time and nonce attribution.

Prove exactly ONE new Ticket corresponds to the message.

Required Ticket evidence:

- `ticket_id` begins with expected `CNXT-` identity;
- exact `run_id` and `owner_session_key` match the semantic run;
- stored prompt SHA matches the sent prompt;
- one `accepted` event exists;
- one `routed` event exists with `workflowEligible=false` for the intended direct lane;
- no duplicate Ticket exists for the same acceptance run/request key.

Prove Ticket-first ordering using timestamps/log ordering as strongly as available:

- Ticket `created_at` / `accepted` event must precede the model inference start/request evidence for the same run;
- the plugin/OpenClaw logs should correlate the run/session/Ticket where available;
- do not claim pre-inference ordering only because source code says so — capture runtime evidence from this run.

If runtime logging cannot expose an inference-start timestamp precisely enough, use the strongest independent combination available (SQLite accepted timestamp plus OpenClaw run/provider/model start log or Ollama request/start observation). If ordering remains unprovable, report blocker rather than inferring it.

## Phase E — prove Ollama-backed inference

Prove the accepted run used provider Ollama through the normal OpenClaw model pipeline.

Record the actual model used; do not change the configured provider/model merely for this task.

Acceptable evidence includes correlated OpenClaw run/session/provider/model metadata or logs, with Ollama process/request activity tied to the same run/time window. Prefer provider/model metadata from OpenClaw plus corroborating local Ollama activity when available.

Reject as insufficient:

- merely observing that Ollama is installed;
- merely observing global provider config says Ollama;
- a separate manual `ollama run` test;
- Hermes executor's own model activity.

Distinguish Hermes/control-plane model traffic from the CogentNexus/OpenClaw product run.

## Phase F — prove response-ready and delivered terminal state

After the real final response is delivered, inspect the same Ticket.

PASS requires direct-lane terminal evidence consistent with current production semantics:

- Ticket `status='completed'`;
- `workflow_eligible=0`;
- `response_ready_at` non-null;
- `delivery_confirmed_at` non-null;
- `delivery_last_error` null/empty;
- `result_json` contains the direct-run result metadata;
- Ticket events contain, in monotonic event order:
  - `accepted`;
  - `routed` direct;
  - `response_ready`;
  - `delivery_confirmed`;
  - `completed`.

For this direct lane, a terminal `ticket_outbox` row is not required if the final user-visible direct reply was confirmed through the direct delivery path. Record whether an outbox row exists; if none, explain that direct confirmed delivery intentionally completes without durable terminal outbox replay. There must be no unexpected pending outbox residue for the acceptance Ticket after successful direct delivery.

The user-visible response MUST contain the unique nonce (ideally exactly the requested echo). Record the response but do not treat response text alone as success; durable Ticket/delivery evidence is mandatory.

## Phase G — idempotency / no duplicate side effect proof

Do NOT resend the user message.

Prove idempotency of the actual observed run by durable identity/accounting:

- exactly one Ticket for the run/request key;
- exactly one `accepted` event for that Ticket;
- exactly one `response_ready` transition;
- exactly one successful `delivery_confirmed` transition;
- exactly one terminal `completed` event;
- no duplicate active/pending Ticket for the same run;
- no duplicate final delivery/outbox side effect attributable to the acceptance run;
- no unexpected workflow was spawned because the request was direct-lane.

If the chosen OpenClaw surface retries transport internally, record evidence and prove those retries converge on the same run/request/Ticket rather than creating duplicate durable work.

## Phase H — post-semantic health

After terminal semantic proof, re-check:

- controller remains MANAGED;
- Gateway healthy/Ready and dashboard reachable;
- provider remains Ollama;
- Ollama healthy/model inventory unchanged;
- Supervisor remains healthy and owned-runtime bound;
- one canonical CNX plugin remains active;
- ownership verification passes;
- AGENTS managed block remains exactly once;
- SQLite integrity remains `ok`;
- no pending recovery/outbox state attributable to this successful acceptance run;
- no unrelated configuration or product topology was mutated.

No reboot is required in this task.

## Safety and mutation fence

Authorized semantic mutation is exactly the one real user message and the product's natural Ticket/session/model/delivery effects caused by that message.

Do NOT:

- install/install-over/uninstall/reset;
- clean/delete durable Ticket/session data;
- manually edit SQLite;
- manually mark Ticket/outbox state;
- restart Gateway/Ollama/Supervisor merely to obtain success unless an already-authorized product-native semantic recovery automatically does so;
- change model/provider/config;
- create files/tools/network side effects from the semantic prompt;
- send the acceptance prompt twice;
- merge/tag/release.

If the semantic run fails or becomes interrupted, preserve the durable evidence and observe whether the product's existing recovery semantics act. Do not mask the failure with manual state changes.

## Verification/report publication

Publish a report-only commit adding exactly:

`docs/operations/coordination/reports/CNX-20260826-076-final-semantic-ticket-ollama-delivery-acceptance.md`

Report must include:

- execution coordination HEAD;
- live source identity `79b51ed06363f6e8862c491ee0a313ddb412c806` / installed parity reference;
- preflight health and BEFORE database/event/outbox cursors;
- exact supported OpenClaw owner-message surface used;
- exact nonce prompt, SHA-256, session key, run ID if available, send/response timestamps;
- unique Ticket ID and row fields;
- runtime proof Ticket accepted before inference;
- provider/model proof showing the product run used Ollama;
- complete Ticket event sequence and timestamps;
- response-ready/delivery-confirmed/completed evidence;
- direct-outbox accounting;
- exact user-visible response containing the nonce;
- duplicate/idempotency accounting;
- post-run MANAGED/Gateway/Ollama/plugin/ownership/AGENTS/SQLite health;
- explicit statement that no install/reset/manual DB edit/provider/model change or duplicate semantic send occurred;
- report-only publication fence.

## Result tokens

Use exactly one:

- `PASS_FINAL_SEMANTIC_TICKET_OLLAMA_DELIVERY_ACCEPTANCE`
- `BLOCKED_SEMANTIC_ENTRY_PATH`
- `BLOCKED_TICKET_FIRST_ORDERING`
- `BLOCKED_OLLAMA_INFERENCE_PROOF`
- `BLOCKED_RESPONSE_OR_DELIVERY_TERMINAL_STATE`
- `BLOCKED_IDEMPOTENCY_OR_DUPLICATE_EFFECT`
- `BLOCKED_POST_SEMANTIC_HEALTH`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Completion meaning

If ChatGPT independently accepts `PASS_FINAL_SEMANTIC_TICKET_OLLAMA_DELIVERY_ACCEPTANCE`, the current CogentNexus-OpenClaw v0.9.3 acceptance chain is complete for the agreed scope: install/uninstall/install-over correctness, recovery boundaries, owned runtime, no-flash supervisor operation, source/live parity, Ticket-first real inference and durable delivery have all been demonstrated.
