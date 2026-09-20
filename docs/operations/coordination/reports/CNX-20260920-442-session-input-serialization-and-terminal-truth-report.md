# CNX-20260920-442 — Session Input Serialization and Terminal Truth Report

Status: `LIVE_READY_FOR_OPERATOR_TEST`

Classification:

`CNX442_SESSION_SERIALIZATION_TERMINAL_TRUTH_SOURCE_GREEN`

## Trigger

A live owner turn on Discord run `673cb634-58e2-4706-94d8-0a45e7740784` failed after native `/context` changed the same session transcript during the active run. OpenClaw ended the run with:

`SQLite transcript changed while preparing rewrite for 06e736f1-01e5-45b7-8c0b-bbaa9ed6f700`

CNX had already recorded the owning Ticket as `completed` even though no final assistant answer was delivered.

Two native command turns (`/context`, `/context detail`) were also admitted as conversational CNX Tickets.

## Repair

CNX-442 makes the contract provider- and surface-independent.

### Native command bypass

`reply_dispatch` now excludes Host-native commands before CNX Ticket admission. OpenClaw command facts and its own command detector are used; ordinary text that merely resembles a slash command is not excluded.

### Same-session serialization

Owner conversational sessions use OpenClaw's supported session API and are normalized to:

`queueMode=followup`

This applies to eligible owner sessions regardless of Discord, Dashboard/WebChat, or another supported ingress sharing the same session pipeline. Internal/subagent/cron-style sessions remain excluded.

### Authoritative terminal truth

CNX no longer treats `agent_end success` as sufficient proof that an owner Ticket completed when user-visible delivery is unresolved.

The reconciler reads exact per-run `session.ended` evidence from the owning agent's Host database:

`<agent-dir>\openclaw-agent.sqlite`

The implementation intentionally does not use `session.resolveStorePath()` for this proof because OpenClaw 2026.9.5 resolves that surface to legacy `sessions.json`, not the trajectory SQLite database.

Semantics:

- Host success + visible assistant output: existing durable delivery/receipt path remains authoritative.
- Host success + no visible output: complete only after Host terminal success, without emitting duplicate `response_ready`.
- Host terminal error before confirmed delivery: retract unconfirmed response-ready state and atomically create Direct Recovery.
- confirmed or transport-accepted delivery evidence: fail closed as a conflict; do not rewrite user-visible history.

## Status UI

Operator decision: out of scope. No changes were made to decorative host status phrases such as `Cracking…` or `Shelling…`.

## Validation

- CNX-442 focused suite: 13 PASS;
- CNX-440 + Discord/WebChat durable delivery: 11 PASS;
- CNX-427 + reply-dispatch/Ticket-first admission: 22 PASS;
- Host claim/session ingress fences: 8 PASS;
- index integration: 42 PASS;
- v0.9.5 behavior/delivery/session/no-reply matrix: 21 PASS.

Total core targeted/integration regressions:

`120 PASS`

Additional qualification:

- `npm run plugin:validate` — PASS;
- TypeScript/plugin build — PASS;
- mixed-plugin artifact verification — PASS;
- Ticket DB bootstrap — PASS;
- package contents verification — PASS (280 packed files);
- `git diff --check` — PASS.

## Live deployment state

Not yet installed at the time of this source-qualified report section.

Next gate is one supported install-over from the exact committed candidate, followed by read-only/live runtime qualification. No semantic Discord message will be sent by the executor.

## Historical stranded-command cleanup

Read-only live preflight proved both reproducing native-command Tickets remain stranded from the pre-repair runtime:

- `CNXT-7b523819-6b36-4c83-8ec7-8186e60417cc` — `/context`;
- `CNXT-738a99f9-2619-4d50-a574-6b13aa6d1471` — `/context detail`.

For each Ticket:

- model-call rows = 0;
- inference-attempt rows = 0;
- assistant-delivery rows = 0;
- Direct-recovery rows = 0;
- `response_ready_at` = null;
- `delivery_confirmed_at` = null.

A source-tested startup retirement migration now cancels only old recognized native-command Tickets with zero execution/delivery/recovery evidence and records `native_command_ticket_retired`.

The migration is intentionally fail-closed for fresh Tickets, unknown slash-looking text, incomplete schema, or any Ticket carrying execution/delivery/recovery evidence.

Focused CNX-442 suite is now 16/16 PASS. Core targeted/integration qualification totals 120 PASS. Release/authority wiring after migration is 8/8 PASS. Final `plugin:validate` is PASS and package verification reports 280 packed files.

## Live readiness checkpoint

Exact deployed implementation candidate:

`80a42cf4489196f653d1af84abfe92444e0099ff`

Supported install-over:

- LConnect session: `proc-1789896554229-45`;
- installer PID: `11784`;
- terminal exit: `0`;
- terminal text: `CogentNexus-OpenClaw v0.9.5 installation completed successfully.`;
- controller: `cnxMode=active`, `mode=managed`, generation `113`;
- Gateway healthy; event loop not degraded;
- Discord ready/running/connected; `activeRuns=0`;
- supervisor Enabled/Ready; `LastTaskResult=0`;
- Ollama resident model list empty after install.

Candidate/live SHA-256 parity is exact for:

- `dist/index.js`;
- `dist/v091-release-entry.js`;
- `dist/v095-session-serialization.js`;
- `dist/v095-host-terminal-evidence.js`;
- `dist/v095-native-command-retirement.js`.

Historical native-command cleanup is live:

- `CNXT-7b523819-6b36-4c83-8ec7-8186e60417cc` (`/context`) -> `cancelled`;
- `CNXT-738a99f9-2619-4d50-a574-6b13aa6d1471` (`/context detail`) -> `cancelled`;
- each received `native_command_ticket_retired`;
- target channel now has zero non-terminal CNX Tickets;
- no active Direct Recovery exists.

Live queue qualification found existing session entries did not persist a per-session `queueMode` override.
A supported OpenClaw config write was therefore applied:

`messages.queue.mode = followup`

OpenClaw reported no Gateway restart required. The active config now returns `followup`.
This provides the required provider- and ingress-independent safe default for sessions without an explicit override.

Current model policy remains:

- primary `ollama/qwen3.8:27b`;
- `OLLAMA_CONTEXT_LENGTH=24576`;
- `OLLAMA_KEEP_ALIVE=2h`.

The historical target Discord session still contains a stale persisted `activeWriterRunId` from the failed pre-repair run, while Host health reports `activeRuns=0` and no pending input rows exist. For the cleanest operator acceptance, start a new physical session before the first post-repair message.

Classification:

`CNX442_LIVE_READY_FOR_OPERATOR_TEST`
