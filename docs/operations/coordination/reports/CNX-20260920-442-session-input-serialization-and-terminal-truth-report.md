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

## CNX-442 queued-run typing hardening and clean-session checkpoint — 2026-09-20

This checkpoint supersedes the earlier `80a42cf...` live candidate for the current operator acceptance.

Implementation candidate:

`f27a5fbd273419bebf9ac624c3fb0524403bb1c2`

The candidate adds the post-live-test hardening that was not present in the earlier checkpoint:

- durable provisional ingress claims for queued follow-up turns, atomically bound to the authoritative run at dequeue;
- same-session Stop cancellation that fences current and queued Tickets against resurrection;
- migration-7 coverage for the ingress-claim ledger;
- installer enforcement of the surface-independent OpenClaw queue default `messages.queue.mode=followup`;
- Discord active-run typing continuity for an admitted run, including a dequeued follow-up run whose upstream outer-dispatch typing controller was already sealed;
- Discord typing uses OpenClaw's public SecretInput resolver, does not log/persist the credential, refreshes only while the exact run is active, stops at `agent_end`, and has a bounded 30-minute safety TTL;
- decorative Dashboard status phrases remain out of scope and unchanged.

Source qualification after the hardening:

- focused queue/terminal/Stop/installer/typing/migration suite: 44/44 PASS;
- Discord active-typing unit suite: 5/5 PASS;
- TypeScript/plugin build: PASS;
- `plugin:validate`: PASS;
- mixed-plugin schema: PASS;
- Ticket DB bootstrap: PASS (9 required tables + v0.9.5 registration fence);
- package verification: PASS, 286 files;
- `git diff --check`: PASS;
- first broad suite before the migration-test expectation repair: 412/414 PASS;
- the real new failure was only the stale migration expectation `[1..6]` versus schema migration 7; that focused regression was repaired and rerun GREEN;
- the only remaining broad-suite RED is the repository's pre-existing intentional CNX-383 projection test, already documented historically as unrelated.

Supported install-over from `f27a5fbd...`:

- terminal exit code: 0;
- terminal message: `CogentNexus-OpenClaw v0.9.5 installation completed successfully.`;
- MANAGED authority: `cnxMode=active`, `mode=managed`, generation `115`;
- Gateway 2026.9.5 healthy; event loop not degraded;
- Discord ready/running/connected; busy=false; activeRuns=0;
- supervisor Enabled/Ready; LastTaskResult=0;
- Ollama reachable with no resident model after install;
- `messages.queue.mode = followup`;
- runtime attestation: runnerReady=true, global before_agent_run hook count=7;
- OpenClaw's public runtime does not expose plugin-specific hook ownership, so the attestation classification remains conservatively `AMBIGUOUS` rather than being promoted to `PRESENT`.

Exact candidate/live SHA-256 parity is GREEN for:

- `dist/index.js` = `6002AE5F42349D5C69DC7E7331EC53E1CAF61042C3F73DEBF5FE58266DB10738`;
- `dist/v091-release-entry.js` = `4EA526CCF0E82D3A2EC24AD219A2EF38A78DB7367955DCECC0AE9F6F0AA19ADF`;
- `dist/discord-active-typing.js` = `A130C70FB61B784F2D34BA7C780A0B0DDDAFB6AB39F8E197B1AAEDFC07EDB9D3`;
- `dist/ticket-store.js` = `7EE132A195498FA35792F224B94784D218267B6BDF8E17D048F0784FA6104B8D`;
- `dist/ticket-admission-kernel.js` = `5728E6452A79D668E089E4D7BC0CEDAC8C6AC74F9329A8837EAFF08B9431738A`.

Clean-session preparation:

- prior physical Discord session: `e265aae1-a7ce-4384-a3e9-2e2042e1aa7c`;
- pre-delete state: status=done, pending inputs=0, target non-terminal Tickets=0, pending outbox=0, Direct Recovery=0, Discord activeRuns=0;
- the prior entry still retained its completed-run `activeWriterRunId`, so a genuinely new physical session was preferred for acceptance;
- supported fenced `sessions.delete` returned `deleted:true`;
- prior transcript was archived by OpenClaw;
- post-delete OpenClaw session-node count for the target key=0;
- post-delete CNX session state=`deleted`, generation=9;
- post-delete pending inputs=0, target non-terminal Tickets=0, pending outbox=0;
- Gateway/Discord health remained GREEN.

Current gate:

`CNX442_LIVE_READY_FOR_NEW_SESSION_OPERATOR_TURN`

The next semantic Discord message must be sent by the operator. The executor must not send it on the operator's behalf.

## CNX-442 first-turn duplicate-Ticket repair candidate — 2026-09-20

A genuine new-session Discord turn exposed a host ordering not covered by the prior candidate:

`before_dispatch -> before_agent_run -> reply_dispatch`

Under that ordering, the provisional ingress Ticket existed before the authoritative run, but `before_agent_run` created a second Ticket before `reply_dispatch` had a chance to bind the claim. The live turn therefore produced two Tickets for one user message.

Repair candidate:

`49d8e259fb6760583caa706af526cb1b165a5799`

The repair:
- adds lifecycle-fenced owner session/generation metadata to provisional ingress claims (schema migration 8);
- binds the next exact FIFO pending ingress claim during `before_agent_run` before ordinary Ticket admission;
- fences by owner session key, physical session identity/generation, prompt hash, and source channel;
- fails closed on FIFO/source mismatch rather than selecting a latest same-session Ticket;
- suppresses a previously cancelled queued ingress before provider/model execution;
- preserves the existing `reply_dispatch` binding path for host surfaces whose ordering reaches that adapter first.

TDD / qualification:
- exact live-order RED reproduced 2 Tickets before repair and GREEN 1 Ticket after repair;
- cancelled queued ingress before `before_agent_run`: GREEN;
- focused qualification: 88/88 PASS;
- full plugin suite: 415 PASS / 1 historical intentional CNX-383 projection RED, with no new regression;
- `plugin:validate`: PASS;
- TypeScript build: PASS;
- mixed-plugin schema: PASS (46 properties, 5 tools);
- Ticket DB bootstrap: PASS;
- package verification: PASS, 286 files;
- `git diff --check`: PASS.

Supported install-over from exact candidate:
- installer process exit code 0;
- terminal message `CogentNexus-OpenClaw v0.9.5 installation completed successfully.`;
- MANAGED canonical authority: `cnxMode=active`, generation 117;
- Gateway 2026.9.5 healthy; event loop not degraded;
- Discord ready/running/connected, busy=false, activeRuns=0;
- supervisor enabled, LastTaskResult=0;
- `messages.queue.mode=followup`;
- runtime attestation: runnerReady=true, global before_agent_run hook count=7;
- attestation classification remains conservatively `AMBIGUOUS` because OpenClaw does not expose plugin-specific hook ownership.

Candidate/live SHA-256 parity:
- `dist/index.js`: `CC91F8FBB98E8D2B084AB2A4886877B4517534A5E4D0F5FE24232ADEA5E6D3F1`;
- `dist/v091-release-entry.js`: `4EA526CCF0E82D3A2EC24AD219A2EF38A78DB7367955DCECC0AE9F6F0AA19ADF`;
- `dist/discord-active-typing.js`: `A130C70FB61B784F2D34BA7C780A0B0DDDAFB6AB39F8E197B1AAEDFC07EDB9D3`;
- `dist/ticket-store.js`: `5491DE03F75824EFD45489B269EE4BE237781CBE411E0CA1E3BD098572469048`;
- `dist/ticket-admission-kernel.js`: `5728E6452A79D668E089E4D7BC0CEDAC8C6AC74F9329A8837EAFF08B9431738A`.

Live DB migration proof:
- migrations = 1..8;
- `ticket_ingress_claims` includes `owner_session_id` and `owner_generation`;
- target physical OpenClaw session remains absent;
- target CNX session remains deleted at generation 10;
- target pending input / non-terminal Ticket / pending outbox = 0;
- one historical unbound claim remains from the pre-repair failed turn, but it is a cancelled Ticket with `owner_session_id=NULL` and `owner_generation=0`; generation 10 therefore fences it from any new lifecycle.

Pre-send baseline:
- Tickets 55;
- Ticket events 1167;
- direct model calls 40;
- inference attempts 39;
- assistant deliveries 30;
- ingress claims 1;
- target-channel Tickets 13;
- target-channel non-terminal Tickets 0;
- target session node count 0;
- pending inputs 0.

Current gate:

`CNX442_LIVE_READY_FOR_RETRY_FIRST_OPERATOR_TURN`

The operator must send the semantic Discord test message. The executor must not send it on the operator's behalf.
