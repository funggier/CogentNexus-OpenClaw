# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Updated:** 2026-08-27 ICT
**Transport:** GitHub repository history
**Human authority:** operator approved state-gated bounded retries, confirmed a currently known-working Dashboard input method, and authorized Task 100 to continue through final authenticated semantic acceptance in the same task
**Execution trigger:** manual Hermes continuation; scheduled execution remains disabled

## Accepted live baseline

Task 096 live deployment remains accepted.

Exact installed source:

`32212a4331e1f32b5a130bd30d271d4cbc56f6c1`

Accepted plugin fingerprint:

`df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`

Live state remains MANAGED generation 24 with one candidate-exact canonical plugin generation, healthy startup/Supervisor/Gateway/SQLite/Ollama, preserved Task-092 retired evidence and accepted `NO_FLASH_MULTI_TICK_REPROVEN`.

## Task 099 result

Task 099 report:

`d5fde8d5f1e5968a1ae5ce11f4017a15d9884dac`

Independent disposition:

`ACCEPT_BLOCKER_DASHBOARD_WINDOW_FOREGROUND_TARGETING_BEFORE_SEND`

Exact target:

`agent:main:dashboard:89992501-1b33-46cf-85f7-eb0c1ef4d311`

Task 099 sent zero semantic messages. Its nonce is retired.

The blocker was OS/UI input targeting before send, not a semantic-pipeline regression. Task 092 previously proved Dashboard send -> Ticket -> one Ollama inference -> exact visible reply; Task 093 repaired the later durable staging boundary and Task 096 installed that source live.

## New operator evidence

The operator has now tested until Codex can type into the actual OpenClaw Dashboard composer and reports that Codex knows the working interaction method.

The operator further approved continuing the original semantic acceptance immediately rather than ending Task 100 after readiness proof.

## Active Task 100

[`tasks/CNX-20260827-100-dashboard-foreground-input-target-readiness.md`](tasks/CNX-20260827-100-dashboard-foreground-input-target-readiness.md)

Execution mode:

`LIVE_KNOWN_WORKING_DASHBOARD_INPUT_AND_FINAL_SEMANTIC_ACCEPTANCE`

Authorization:

`OPERATOR_APPROVED_KNOWN_WORKING_INPUT_REPRODUCTION_AND_FINAL_SEMANTIC_CONTINUATION`

Task 100 must first reproduce the method that actually works now and publish it under:

`Known-working Dashboard input method`

The report must record the real non-secret interaction sequence, targeting/focus method, waits/retries if any, proof that keystrokes reach the intended composer, and how the composer is returned to an empty state.

Task 100 may use a non-sent local sentinel `CNXINPUT-READY` to prove input targeting, provided it is never sent and is cleared completely before semantic nonce generation.

If an existing non-sent test draft is present, do not expose its contents; prove zero Ticket/provider effect, clear it, and re-verify empty composer. If a prior test was actually sent, stop and correlate that semantic effect instead of sending again.

## Final semantic contract inside Task 100

After input-method proof and clean baseline:

- generate one brand-new `CNXSEM4-...` nonce;
- send exactly one semantic Dashboard message;
- no resend exists;
- require exactly one new Ticket and route before provider;
- require exactly one `ollama/qwen3.5:9b` inference;
- require durable final payload staging before native delivery;
- require exactly one visible nonce;
- require exact lifecycle `response_ready -> delivery_confirmed -> completed`;
- reject duplicate Ticket/route/provider/outbox/reply/promotion effects;
- after durable completion only, prove New Session continuity with zero additional semantic/provider effect.

Required method token:

`DASHBOARD_KNOWN_WORKING_INPUT_METHOD_PROVEN`

Required final success token:

`PASS_FINAL_AUTHENTICATED_FRESH_SESSION_SEMANTIC_ACCEPTED`

## Retry policy v1

- read-only operations: maximum 3 attempts total;
- low-impact focus/click/activation/non-sent typing/clearing: maximum 2 attempts total after grace + fresh state proof;
- if attempt 1 appears late, treat it as success and do not retry;
- ambiguous/partial state is not retryable;
- semantic Send remains one attempt only;
- post-completion New Session may use state-gated retry for session management only.

## Hard fence

No second semantic send, Task-099 nonce reuse, CLI/channel substitute, direct provider/Ollama probe, synthetic Ticket creation, install/reset/repair/cleanup, session normalization, plugin-generation/controller/startup/Supervisor/AGENTS/config/runtime/SQLite mutation, prior-evidence rewrite, provider/model/timeout change, restart/reboot, merge/tag/release or force push is authorized.

Credential values must not be read, copied, printed, logged, requested or re-entered by the executor.

## Publication and final gate

Task 100 publishes exactly one report-only commit at:

`docs/operations/coordination/reports/CNX-20260827-100-dashboard-foreground-input-target-readiness.md`

Only independent review of that report and publication fence may close final OpenClaw semantic acceptance. A visible correct reply without durable staging, delivery confirmation and terminal completion remains a failure.
