# CNX-20260920-442 — Session Input Serialization and Terminal Truth

Status: `COMPLETE`

State: `FINAL_LIVE_GREEN`

Parent: `CNX-20260920-427`

Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`

Executor: `ChatGPT via LConnect`

Reviewer: `ChatGPT`

Human final authority: `Operator`

## Trigger

A live Discord turn on channel `1391855033993138217` exposed a same-session transcript race.

User turn:

`@Ce ช่วยดูหน่อยครับว่าวันนี้เป็นข้างขึ้นข้างแรม`

Authoritative run:

`673cb634-58e2-4706-94d8-0a45e7740784`

CNX Ticket:

`CNXT-8e762028-d5af-4ad9-a56d-8aae89600a9b`

Physical session:

`06e736f1-01e5-45b7-8c0b-bbaa9ed6f700`

The first model call completed and invoked `exec` successfully. During the second model call, native
`/context` mutated the same session transcript. OpenClaw terminated the run with:

`SQLite transcript changed while preparing rewrite for 06e736f1-01e5-45b7-8c0b-bbaa9ed6f700`

No final assistant answer was delivered.

CNX nevertheless recorded the Ticket as `completed`, exposing a terminal-truth mismatch.

Two native command Tickets were also incorrectly admitted and left `accepted`:

- `CNXT-7b523819-6b36-4c83-8ec7-8186e60417cc` — `/context`
- `CNXT-738a99f9-2619-4d50-a574-6b13aa6d1471` — `/context detail`

## Primary goal

Make every owner conversational session safe under concurrent human input while preserving Ticket-first durability.

This contract is **surface-independent**. It applies to Discord, WebChat/Dashboard, and any other supported OpenClaw owner ingress that enters the same reply/session pipeline. Discord is only the reproducing surface; it is not the scope boundary.

Required semantics:

1. Native slash commands handled by OpenClaw must not create CNX conversational Tickets on any supported owner ingress.
2. A new ordinary user turn arriving through any supported owner ingress while another run owns the session must be durably accepted without mutating the active run's transcript.
3. Ordinary queued user turns must preserve FIFO order and idempotency.
4. CNX must not classify a Ticket `completed` until the authoritative host run terminal outcome is known.
5. Host-level failure after model-call completion must settle the owning CNX Ticket as non-success, never completed.
6. Existing CNX-427/CNX-440 Ticket-first and durable Discord settlement guarantees must remain intact.

## Desired serialization

```text
User A
  -> Ticket A -> RUNNING
  -> User B arrives -> durable queue / Ticket B -> QUEUED
  -> User C arrives -> durable queue / Ticket C -> QUEUED
  -> Run A terminal
  -> Ticket A terminal
  -> dequeue B -> Run B
  -> dequeue C -> Run C
```

Native informational commands such as `/context` should stay in OpenClaw's command lane and must not enter
the CNX conversational Ticket pipeline.

Control commands whose purpose is to cancel/reset execution must retain native control semantics rather than
being silently converted into queued conversation.

## Status UI

Status/progress UI work is explicitly out of scope for CNX-442 by operator decision on 2026-09-20.
Decorative host phrases such as `Cracking…` or `Shelling…` are not modified by this task.

## TDD plan

### RED-A — Native command bypass

Prove `/context` and `/context detail` do not create CNX Tickets across representative owner surfaces while ordinary conversational text still does.

### RED-B — Same-session concurrent human turn

Reproduce one active run followed by a second ordinary user message across representative owner surfaces. Prove the second input is durably queued
and cannot mutate the active transcript before the first run reaches terminal state.

### RED-C — Terminal truth

Reproduce the observed ordering where model-call activity completes but the host run later ends in error.
Prove the Ticket cannot reach `completed` before authoritative run terminal success.

## Constraints

- Do not patch installed OpenClaw core files directly unless a supported plugin boundary is proven insufficient and separately escalated.
- Do not manually mutate OpenClaw session SQLite to simulate queueing.
- Do not directly edit live CNX Ticket rows before migration/repair behavior is source-tested.
- Preserve `ollama/qwen3.8:27b` at context `24576` and keep-alive `2h`.
- Source tests first; no live reinstall until the affected regression surface is GREEN.

## Surface-independence requirement

The repair must not special-case Discord for admission, queueing, or terminal truth.

Representative qualification surfaces:

- Discord owner channel;
- WebChat / Dashboard owner session;
- generic owner reply-dispatch context used by other supported OpenClaw ingress paths.

The implementation should prefer host-generic session/reply primitives. Channel-specific code is allowed only where transport semantics truly differ, such as Discord receipt settlement.

Queue policy should therefore be expressed at the OpenClaw messages/session layer rather than only under a Discord adapter.

## Source qualification

Implementation is source-qualified and ready for one supported live install-over.

Implemented boundaries:

- host-native command bypass at `reply_dispatch` using OpenClaw command facts/detection;
- surface-independent owner-session serialization through OpenClaw's supported session API with `queueMode=followup`;
- authoritative terminal reconciliation from exact `trajectory_runtime_events.session.ended` evidence in the owning agent's `openclaw-agent.sqlite`;
- silent successful runs complete only after authoritative Host success without duplicating `response_ready`;
- Host terminal failure clears unconfirmed response-ready state and atomically creates Direct Recovery;
- confirmed/transport-accepted delivery evidence remains fail-closed and is never silently rewritten.

Validation:

- CNX-442 focused suite: 13/13 PASS;
- CNX-440 + Discord/WebChat durable delivery: 11/11 PASS;
- CNX-427 + reply-dispatch/Ticket-first admission: 22/22 PASS;
- Host claim/session ingress fences: 8/8 PASS;
- `src/index.test.ts`: 42/42 PASS;
- v0.9.5 behavior/delivery/session/no-reply matrix: 21/21 PASS;
- total core targeted/integration regression count: **120 PASS**;
- `npm run plugin:validate`: PASS;
- package verification: PASS, 280 packed files;
- mixed-plugin artifact/schema verification: PASS;
- Ticket DB bootstrap: PASS;
- `git diff --check`: PASS;
- TypeScript/plugin build: PASS.

Status/progress UI is not part of this task and is intentionally unchanged.

Next gate:

1. freeze exact candidate commit and push;
2. run one supported `scripts/install.ps1 -Workspace C:\Users\CDQ-P\.openclaw\workspace` install-over;
3. verify live plugin/runtime health, session queue policy, command bypass behavior, and Host-terminal reconciliation without sending a semantic Discord message on the operator's behalf.

## Historical native-command retirement

Live preflight found the two reproducing command Tickets still stranded as `accepted`:

- `CNXT-7b523819-6b36-4c83-8ec7-8186e60417cc` — `/context`;
- `CNXT-738a99f9-2619-4d50-a574-6b13aa6d1471` — `/context detail`.

Both have zero Direct model-call rows, zero inference-attempt rows, zero assistant-delivery rows, and zero Direct-recovery rows.

CNX-442 now includes a bounded startup retirement migration. It retires only an old accepted Direct Ticket when:

- OpenClaw's own command detector recognizes the stored prompt as a native/control command;
- the Ticket is older than the bounded minimum age;
- response/delivery are still absent;
- no model-call, inference, delivery, or recovery evidence exists.

The migration preserves history by terminally cancelling the stranded Ticket and appending `native_command_ticket_retired`. It does not rewrite Tickets that have execution/delivery evidence.

Migration regression coverage: 3/3 PASS.

Additional release/authority wiring qualification after the migration was wired: 8/8 PASS.

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

## CNX-442 final live Stop acceptance — GREEN (2026-09-21)

Production candidate:

`8dee9cd635ca3dfcbf96f2f4161b5026355dbcf9`

Candidate ancestry relevant to the final repair:

- `120d8d6c002487904b828a034a276172d5f10dac` — move queued owner ingress behind a durable pre-dispatch FIFO barrier and add restart recovery for held ingress;
- `8dee9cd635ca3dfcbf96f2f4161b5026355dbcf9` — allow the first fresh ingress after a deleted owner session when the owner generation is unchanged.

### Why the architecture changed

Earlier Stop repairs cancelled CNX Tickets correctly but still allowed OpenClaw's native follow-up queue to dequeue a successor Host run. CNX then had to block that successor at `before_agent_run`, which preserved zero inference but surfaced the user-visible error:

`Your message could not be sent: blocked by cogentnexus-openclaw`

OpenClaw Dashboard Stop uses `chat.abort`; queue clearing performed after terminal lifecycle evidence is too late to be an authoritative ordering boundary. The final repair removes the race instead of compensating after it:

1. eligible owner ingress is durably persisted at `before_dispatch`;
2. if an older same-owner/same-generation Ticket is non-terminal, the later request remains held inside the claiming `before_dispatch` hook and never enters the Host queue;
3. normal predecessor completion releases the original request with its original Discord/auth/session context;
4. authoritative Stop increments the owner generation once and cancels current + held Tickets;
5. a held cancelled request returns `{handled:true}` from `before_dispatch`, so it is consumed silently before Host queue admission;
6. restart recovery exists only for held accepted ingress with `bound_run_id IS NULL`, and recovery ordering remains FIFO behind older non-terminal ingress.

The prior `sessions.abort(clearQueued:true)` lifecycle compensation and diagnostic instrumentation were removed from production. The lifecycle subscription remains only for authoritative human-Stop provenance.

### Source qualification

- affected Stop/FIFO/restart-recovery/wiring suite: `49/49 PASS`;
- full plugin suite: `427 PASS / 1 FAIL`;
- the one FAIL is the repository's pre-existing intentional CNX-383 hook-policy projection baseline and is unrelated to CNX-442;
- TypeScript/plugin build: PASS;
- `plugin:validate`: PASS;
- mixed-plugin/schema verification: PASS;
- Ticket DB bootstrap: PASS;
- package verification: PASS;
- `git diff --check`: PASS.

### Supported deployment

Supported install-over from exact candidate `8dee9cd...` completed with terminal exit code `0`.

- CNX controller: `active / managed`;
- managed authority generation after install: `129`;
- Gateway: reachable and event loop healthy;
- Discord: ON / OK;
- installed candidate parity verified for critical `index.js`, `ticket-store.js`, `v090-final-entry.js`, `v091-direct-recovery.js`, and `v095-ingress-restart-recovery.js` surfaces.

### Final physical Discord Stop test

Target owner: `agent:main:discord:channel:1391855033993138217`

Fresh physical session: `16c1fe33-c906-4391-91ae-b2f0bc3f51b0`

Owner generation before Stop: `22`

First Ticket / active run:

- Ticket: `CNXT-add61119-da8e-475b-9dc5-21d3e9096b9b`
- Run: `63d998b2-6b12-4639-a0b5-0ce240518fb1`
- source message ID: `1551501333431844867`
- prompt: first operator `OK1` Stop-test request
- provider/model: `ollama / qwen3.8:27b`
- context: `24576`
- one model call and one inference attempt started.

Second Ticket / held ingress:

- Ticket: `CNXT-abca44db-728b-4bf1-aef7-9c7d993002a0`
- source message ID: `1551501659312496701`
- prompt: second queued `QUEUE`-only operator request
- owner generation: `22`
- `bound_run_id = NULL`
- model-call rows: `0`
- inference-attempt rows: `0`
- Gateway log explicitly recorded that it was held behind the first Ticket at the pre-dispatch FIFO barrier.

After the operator pressed Stop:

- owner generation advanced exactly once: `22 -> 23`;
- first Ticket settled `cancelled`, not permanent failure;
- second Ticket settled `cancelled`;
- second Ticket remained `bound_run_id = NULL`;
- second Ticket remained `0` model calls / `0` inference attempts;
- pending outbox = `0`;
- active Direct Recovery = `0`;
- Gateway log recorded `consumed pre-dispatch FIFO ingress CNXT-abca44db-728b-4bf1-aef7-9c7d993002a0 without Host queue admission (state=cancelled)`;
- OpenClaw session terminal state = `killed`, not `failed`;
- Host trajectory contains exactly one run for the physical session, `63d998b2-...`;
- Host transcript contains only the first user message and contains no second queued user message;
- therefore no successor Host run was created;
- bounded post-Stop log inspection found no new `blocked by cogentnexus-openclaw` and no new `This turn ended before a reply`;
- Gateway remained reachable, event loop healthy, Discord OK.

The operator refreshed the browser and supplied final Dashboard + Discord screenshots. The operator explicitly accepted the resulting user-visible behavior as good: Stop is visible, the queued message does not execute, and no CNX block/failure message is shown.

Final classification:

`CNX442_PRE_DISPATCH_FIFO_AUTHORITATIVE_STOP_GREEN`

`CNX442_NO_SUCCESSOR_HOST_RUN_GREEN`

`CNX442_USER_VISIBLE_STOP_GREEN`
