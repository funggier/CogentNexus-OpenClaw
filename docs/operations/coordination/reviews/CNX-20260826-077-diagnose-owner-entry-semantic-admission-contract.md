# Review — CNX-20260826-077 Comprehensive Semantic-Path Audit

Decision: `REWORK`

Disposition: `REWORK_UNRESOLVED_SEMANTIC_P1S_AND_PROVIDER_READINESS`

Reviewed branch/report HEAD: `b252879bdbc8cba8f187f883f943d9a913199204`
Execution HEAD: `e7348334e0a8536ecb73f6929e8ed9dc6763e73a`
Implementation/test HEAD: `6867af2cad75cb4ee8e70206d70b0ba5bd5abeea`
Initial report HEAD: `62622a3de3a4ee2d7a66ffc80c408946a7a6d1ff`
Final amended report HEAD: `b252879bdbc8cba8f187f883f943d9a913199204`

## Accepted findings

The following Task-077 work is accepted as valid evidence and must be preserved:

- Task 076 selected the wrong trust surface. `openclaw agent --session-key agent:main:main` can target an owner-looking session without itself carrying authenticated owner authority. The existing least-privilege CogentNexus admission rule must not be broadened merely to make that CLI path convenient.
- Dashboard/WebChat is the supported owner-surface candidate that must be proven/used for the eventual live semantic acceptance.
- The canonical installed v0.9.3 plugin generation/source identity and dynamic hook registration were materially verified.
- The test-only commit `6867af2...` usefully adds registered-`before_agent_run` positive owner and negative CLI/subagent coverage.
- Full Python/plugin/npm compatibility verification reported green and no live semantic/config/install mutation occurred.
- Publication lineage is clean in substance: execution HEAD -> one test-only implementation commit -> report-only commit -> report-only amendment. No product source mutation was hidden in the publication fence.

## Why Task 077 is not accepted as complete

The mandatory comprehensive addendum explicitly required that no successor live semantic message be authorized while any unresolved P0/P1 semantic blocker remained. The amended report itself carries multiple P1s forward, so its top-level PASS token cannot satisfy the Task-077 completion gate.

The result token `PASS_OWNER_ENTRY_COVERAGE_REPAIRED` is also misleading for the accepted owner-entry finding: no production owner-admission implementation changed. What was repaired was executable test coverage. If owner-entry were the only scope, the evidence corresponds more closely to `PASS_OWNER_ENTRY_SURFACE_CONTRACT_PROVEN_NO_SOURCE_CHANGE`; the comprehensive task, however, remains incomplete because adjacent blockers remain.

## Independently confirmed blockers

### 1. Delivery-marker owner/session binding — confirmed semantic-integrity defect

Production `before_agent_run` parses a CogentNexus delivery marker before `durableAdmissionEligible()`. If a marker parses, the hook returns `pass` whether `bindDeliveryRun()` succeeds or fails.

For ticket delivery, `TicketStore.bindOutboxRun(outboxId, runId)` currently updates any pending outbox row by numeric id and does not require the current session to equal `ticket_outbox.owner_session_key`. Workflow marker binding similarly validates task/revision/status but not current-session equality with `completion.json.ownerSessionKey`.

Consequences:

- an invalid/forged/stale internal marker can bypass normal Ticket admission;
- a marker that guesses/reuses a pending delivery identity can bind a run from the wrong session;
- later run settlement can falsely confirm/fail another owner's durable delivery.

This must be fixed fail-closed with explicit expected-owner/session binding and negative wrong-session/forged-marker tests.

### 2. Timeout recovery double authority — confirmed ordering defect

The current `agent_end` path invokes generic `scheduleInterruptedResume()` before the Ticket-first block calls `TicketStore.finalizeDirectRun()`.

For a resumable direct failure this permits the generic `cogent-resume-*` continuation to be scheduled before the same direct Ticket is promoted to durable recovery (`waiting`, `workflow_eligible=1`). The system can therefore expose two recovery authorities for one interrupted semantic turn.

The source repair must make the durable Ticket/Host authority win deterministically and suppress generic resume when a Ticket or Host recovery owns the interrupted run. Preserve generic auto-resume for non-Ticket runs.

### 3. Repeated admission routing is not idempotent — independently found missing addendum requirement

The addendum required repeated production hook invocation for the same run/request to converge without duplicate durable effects. Task-077 did not add that test.

`TicketStore.accept()` deduplicates by `ownerSessionKey + runId`, but `TicketStore.route()` updates any accepted Ticket and appends a new `routed` event on every call. A repeated `before_agent_run` for the same run can therefore produce one Ticket but multiple `routed` events.

Add a registered-hook repeated-run RED test and make routing idempotent while preserving exactly one initial `routed` event even for direct lane (`workflow_eligible=0`, which is also the schema default).

### 4. Provider-call lease close ordering — unresolved P1 hypothesis requiring executable proof

`installV091DirectModelCallLease()` closes any still-`active` model-call lease from its `agent_end` fallback. Host recovery can independently move a lease to `recovering`, and Ticket direct-finalization/recovery happens in another `agent_end` handler.

The current tests do not prove all relevant orderings. Task 078 must build deterministic race/order tests. If the state machine is already safe under SQLite serialization and hook ordering, downgrade this finding with proof rather than forcing a patch. If RED exposes lost Host classification, duplicate recovery, or a stranded Ticket/lease state, implement the smallest explicit ownership transition.

### 5. Workflow completion stale rescheduling — confirmed stale-state risk, concurrency proof required

`deliverWorkflowCompletion()` accepts a previously read notice and calls `markWorkflowDeliveryScheduled(path, notice)`. That function rewrites `deliveryStatus='pending'` and increments attempts from the stale object without re-validating the current on-disk terminal delivery state.

A stale/concurrent caller can therefore overwrite a newer `delivered` completion with `pending`. Add repeated/concurrent stale-notice RED tests and introduce a bounded atomic/CAS/claim mechanism that prevents terminal delivery resurrection. Do not redesign the workflow controller.

## Provider readiness remains a hard successor gate

Task 076 showed two approximately 120-second no-token idle-watchdog periods before failure. Task 077 did not establish an effective safe timeout/model/session path.

Task 078 must inspect exact installed OpenClaw `2026.7.1-2` timeout/model-resolution code and current read-only configuration/session state, including the model idle watchdog, Ollama transport timeout, provider/static-catalog timeout propagation, global stuck-session abort ceiling, and the size/context state of the Task-076 session.

A small bounded direct Ollama diagnostic may be used in Task 078 only because it does not enter the OpenClaw/CogentNexus semantic path; it must use a non-mutating echo-style prompt and record cold/warm first-token timing. No OpenClaw user message is authorized.

Do not solve provider timeout by blindly raising a number. Determine whether the next live acceptance should use a fresh Dashboard session, a supported exact OpenClaw configuration workaround, or another proven bounded remedy.

## Additional integration evidence required

Task 078 must strengthen the production-facing harness to prove in one coherent direct-lane scenario:

`trusted owner hook -> exactly one accepted -> exactly one routed(direct) -> provider boundary permitted only after commit -> agent_end response_ready -> correctly owner-bound delivery callback -> exactly one delivery_confirmed -> exactly one completed`

Also prove:

- duplicate `before_agent_run`, `agent_end`, `reply_dispatch` and/or `message_sent` callbacks converge;
- wrong-session delivery markers cannot bind or settle another Ticket/workflow;
- untrusted CLI/subagent/internal continuation remains unable to create a fresh owner Ticket;
- provider timeout/failure leaves one durable recovery authority and no duplicate continuation.

## Publication decision

Do not authorize a new live semantic message from Task 077.

Open a source-only successor that repairs/proves all semantic P1s and resolves provider readiness. Because production source will likely change, any accepted source repair must later pass supported install-over/source-live parity before final semantic acceptance.
