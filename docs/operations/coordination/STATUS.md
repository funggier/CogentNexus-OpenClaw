# Coordination Channel Status

Status: `COMPLETE`
State: `CNX442_FINAL_LIVE_GREEN`
Task ID: `CNX-20260920-442`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
## CNX-442 — session serialization / terminal truth

Active task:

`docs/operations/coordination/tasks/CNX-20260920-442-session-input-serialization-and-terminal-truth.md`

Primary scope: native slash-command bypass, OpenClaw followup queue semantics for same-session concurrent user turns, and authoritative user-visible terminal settlement. Status/progress UI is explicitly out of scope for CNX-442.

CNX-442 is final live GREEN. Production candidate `8dee9cd635ca3dfcbf96f2f4161b5026355dbcf9` passed the affected suite 49/49, full suite 427 PASS / 1 historical CNX-383 RED, build, `plugin:validate`, Ticket DB/package checks, supported install-over, and final physical Discord Stop acceptance with no successor Host run.

Report:

`docs/operations/coordination/reports/CNX-20260920-442-session-input-serialization-and-terminal-truth-report.md`



## Final Discord acceptance — GREEN

The operator sent exactly one genuine Discord turn on channel `1391855033993138217`:

`@Ce CNX427_FINAL_ACCEPTANCE_20260920_A1 Reply exactly: CNX427_FINAL_OK_20260920_A1`

Observed lineage:

- physical OpenClaw session: `06e736f1-01e5-45b7-8c0b-bbaa9ed6f700`;
- authoritative run: `e683efcf-b00e-4ee9-bb11-cac0da94a840`;
- CNX Ticket: `CNXT-d6ed7093-5440-435d-91f7-77caaac7ffb3`;
- inference attempt: `cnx-attempt-8004886f-cf61-468d-8dd3-e7649a374398`;
- durable delivery: `27`;
- owner generation: `7`.

Ordering and cardinality from the clean pre-send baseline:

- Tickets: `47 -> 48` (+1);
- direct model calls: `35 -> 36` (+1);
- inference attempts: `33 -> 34` (+1);
- assistant deliveries: `26 -> 27` (+1);
- exactly one new target-channel Ticket;
- exactly one Ticket for the authoritative run;
- Ticket accepted at `2026-09-20T07:04:19.655Z`;
- model call started at `2026-09-20T07:04:19.714Z`;
- inference attempt started at `2026-09-20T07:04:19.726Z`;
- Ticket persistence therefore preceded model-call authority by about 59 ms;
- no direct-recovery row exists for the accepted Ticket;
- no duplicate Ticket, duplicate model call, duplicate inference attempt, or stale-generation settlement occurred.

Terminal delivery proof:

- model call ended `completed` at `2026-09-20T07:22:51.387Z`;
- inference attempt ended `completed` at `2026-09-20T07:22:51.396Z`;
- `response_ready` at `2026-09-20T07:22:51.460Z`;
- durable delivery row 27 was created at `2026-09-20T07:22:51.578Z`;
- durable idempotency key:
  `cnx-discord:CNXT-d6ed7093-5440-435d-91f7-77caaac7ffb3:g7:cnx-attempt-8004886f-cf61-468d-8dd3-e7649a374398`;
- delivery settled as `delivered / confirmed`;
- receipt evidence type:
  `discord-message-receipt-marker`;
- `delivery_confirmed` event count = `1`;
- `completed` event count = `1`;
- Ticket terminal status = `completed`;
- exact delivered text:
  `CNX427_FINAL_OK_20260920_A1`.

OpenClaw trajectory independently recorded:

- finalStatus = `success`;
- timedOut = `false`;
- provider/model = `ollama / qwen3.8:27b`;
- input tokens = `12105`;
- output tokens = `19`;
- compaction count = `0`;
- assistant text = `CNX427_FINAL_OK_20260920_A1`;
- target session status = `done`.

The operator supplied visual Discord screenshots confirming exactly one visible assistant response with the exact expected text.

Current local-model policy remains intentionally unchanged:

- primary model `ollama/qwen3.8:27b`;
- `contextWindow=24576`;
- `num_ctx=24576`;
- `OLLAMA_CONTEXT_LENGTH=24576`;
- `OLLAMA_KEEP_ALIVE=2h`.

The live acceptance used 24K context successfully. During execution llama-server private memory reached about 21.4 GB and free physical RAM was observed as low as about 1.3 GB, so 24K remains the operator-approved default unless future workload proves insufficient.

Final classifications:

`CNX427_EXTERNAL_INGRESS_TICKET_FIRST_DURABLE_DISCORD_GREEN`

`OPENCLAW95_DISCORD_DURABLE_MARKER_SETTLEMENT_GREEN`


## CNX-440 / CNX-441 current authoritative state

This section supersedes older pre-install baseline figures below.

- exact local/remote candidate HEAD: `5263b6aed9acf77a4db39be47c4d96fecfe8a431`;
- supported install session: `proc-1789885920190-35` / PID `10220`;
- installer terminal exit: `0`;
- live v095 adapter SHA-256 matches candidate: `7809B18C4BAE1209624D5E69112722EF9AD7F5E39A92A2815C6889DFF6C646A1`;
- CNX controller: active/managed generation `111`;
- Gateway: healthy, event loop not degraded;
- Discord: ready/connected;
- supervisor: Enabled/Ready, Last Result `0`;
- Ollama resident models: none;
- primary model: `ollama/qwen3.8:27b`;
- live context: `contextWindow=24576`, `num_ctx=24576`;
- environment: `OLLAMA_CONTEXT_LENGTH=24576`, `OLLAMA_KEEP_ALIVE=2h`;
- target Discord channel `1391855033993138217`: zero non-terminal CNX Tickets;
- fresh counters: Tickets `47`, max event `1109`, direct model calls `35`, inference attempts `33`, assistant deliveries `26`.

CNX-441: `INSTALLER_SUPERVISOR_HANDOFF_QUIESCENCE_GREEN`.

CNX-440: `OPENCLAW95_DISCORD_DURABLE_MARKER_SETTLEMENT_GREEN`.

## OpenClaw 9.5

Live version:

`OpenClaw 2026.9.5 (ec9c1a1)`

Current runtime:

- Gateway health GREEN;
- event loop settled, degraded=false;
- plugin errors 0;
- Discord ready/connected;
- Tailscale Serve active;
- remote HTTPS 200;
- CNX runtime runnerReady=true;
- supervisor Enabled / Last Result 0;
- shared DB v17 quick_check ok;
- agent DB v21 quick_check ok;
- CNX DB v0 quick_check ok.

## CNX-427 Track A

Two live Discord turns on 9.4 proved visible delivery without a CNX Ticket.

Acceptance #1:

- trace `343c6efbf788333b585d1160af9ed4e6`;
- run `a0660423-e586-4e89-a5c9-fca25d842e1d`;
- visible `CNX427_OK`;
- CNX Ticket absent.

Acceptance #2:

- trace `73bfcb525d0fbecc95372ddf49151c44`;
- run `77b8ed7a-f40c-4ac1-86f4-0884656b4e8e`;
- direct DB query: Tickets 0 / events 0 / CNX deliveries 0.

OpenClaw 9.5 contains upstream generation continuity fix `983782594807a23c006b49bd16172b1ba6980924`.

Final semantic acceptance on 9.5 is GREEN; see the authoritative final acceptance section above.

## CNX-436 / CNX-437 final live repair state

The OpenClaw 9.5 post-install lifecycle path is now GREEN.

CNX-436:

- implementation commit `321fda1e5a2564973a9868141413fb73b8c26805`;
- readiness budget = bounded 180 seconds;
- live installer crossed 5 readiness attempts and completed;
- classification `OPENCLAW95_LIFECYCLE_START_READINESS_GREEN`.

CNX-437:

- implementation commit `d67e86ae212222e62bd6eba2e194c1fd78fcf785`;
- Windows subprocess capture now uses explicit UTF-8 + replacement;
- focused regression 5/5 PASS;
- affected Host/session regression 55 PASS with 2 unrelated cases deselected;
- supported install-over terminal exit = 0;
- controller `cnxMode=active`, generation 109;
- plugin loaded by Gateway;
- supervisor Enabled / hidden / Last Result 0;
- Gateway health ok;
- Discord ready/connected;
- no new UnicodeDecodeError / NoneType JSON / transactional rollback after install;
- classification `WINDOWS_UTF8_SUBPROCESS_AND_GATEWAY_TEMP_COMPAT_GREEN`.

OpenClaw's native restart-loop breaker self-recovered after its 300000 ms window drained. No OpenClaw state DB rows were manually deleted.

## CNX-438 recovery/memory-pressure repair

The post-delete target Discord turn was automatically rehydrated by OpenClaw main-session restart recovery.

Recovery lineage:

- session `38ef9799-a8ed-49fb-963c-aad35519a771`;
- run `9000715c-c8db-4d2c-b040-6663f8235d33`;
- Ticket `CNXT-26e773e3-9506-4bfb-8ee0-4ec16fea9661`;
- qwen3.8 loaded with `num_ctx=262144`.

This caused severe local memory pressure and Gateway event-loop starvation.

The recovery was aborted through supported RPC, qwen unloaded, and the target session was deleted through supported OpenClaw session lifecycle.

qwen3.8 memory qualification:

- 65536 context: unsafe on this host; free physical RAM fell to about 0.6 GB;
- 32768 context: isolated one-token load completed successfully in about 22.46 s;
- current live OpenClaw qwen3.8 config: `contextWindow=32768`, `num_ctx=32768`.

Current final acceptance baseline:

- target Discord session key absent from OpenClaw session store;
- CNX session authority for the prior physical session: deleted, generation 6;
- recovery Ticket status: cancelled;
- no `cnx_direct_recovery` row for the target Ticket;
- historical active call/attempt rows are terminal-Ticket fenced from Host recovery;
- current model: `ollama/qwen3.8:27b`;
- context cap: 32768;
- CNX Tickets: 46;
- max Ticket event id: 1101;
- direct model-call rows: 34;
- inference attempts: 32;
- assistant deliveries: 26;
- Gateway health ok / event loop degraded=false;
- Discord ready/connected / activeRuns=0;
- free physical RAM about 21.4 GB.

Two unrelated historical non-terminal Tickets remain on other Discord channels from 2026-09-03 and 2026-09-06; neither belongs to target channel `1391855033993138217`.

That exact one-turn acceptance was completed successfully; no additional acceptance turn is required.

## CNX-428 supervisor cold-start repair

A live OpenClaw 9.5 cold start exposed a separate supervisor defect: the CNX external supervisor used two lightweight Gateway probes separated by one second and interpreted a valid slow cold start as a hard hang.

Measured service-owned 9.5 boot:

- HTTP listener after about 42.4 s;
- event-loop stall around 38 s during `sidecars.model-runtime`;
- `gateway ready` after about 90.7 s.

Repair commit:

`13dfba9a55f4d64ceb9aa8440670c9ee9792354a`

The repaired Host reads OpenClaw `gateway_boot_lifecycle` and applies a bounded 180-second startup/restart grace. A real live boot inside that window returned `gateway-starting`, `action=none`, `heavyPath=false`, and did not invoke restart.

Validation:

- focused Host: 8/8 PASS;
- expanded Python: 44/44 PASS;
- CNX-427 plugin tests: 5/5 PASS;
- full plugin suite: 381/382 PASS, with the sole failure the pre-existing intentional CNX-383 RED.

Recurring supervisor is restored Enabled / Last Result 0, the stale maintenance marker was reconciled, and no new post-repair restart request was observed.

Isolated PID-bound pre-acceptance probe:

- session `agent:main:cnx427-process-probe-1958`;
- run `62a61c83-8c61-446c-9a6d-20b4138dd857`;
- Ticket `CNXT-7a349016-6de3-4f20-bc7a-73c82cca6603`;
- exactly one user turn / one run / one Ticket / one model call;
- Ticket accepted at `12:59:26.475Z`;
- model call started at `12:59:26.521Z`;
- Ticket-first ordering therefore preceded model authority by about 46 ms;
- local `qwen3:1.7b` hit the explicit 90-second provider timeout and terminated `failed` without duplicate/recovery inference.

This proves the 9.5 execution-generation Ticket-first boundary before the genuine Discord final gate.

## OOM finding

The first live 9.5 start crashed because qwen3.8:27b remained loaded in Ollama and llama-server reserved ~22.94 GB private memory, filling the 20 GB pagefile and leaving ~2 GB free commit.

`ollama stop qwen3.8:27b` unloaded it without deleting the model.

After unload, free commit recovered to ~25 GB and live 9.5 became stable.

## Storage relocation

Operator-requested CNX backup relocation is GREEN.

Canonical destination:

`T:\CogentNexus\CogentNexus-OpenClaw`

Current state:

- C: `...\CogentNexus-OpenClaw\backups` -> T: `backups` via NTFS junction;
- C: `...\plugin-generation-rollover-backups` -> T: rollover tree via NTFS junction;
- main backup dry mirror: 509,383 files / 9.479 GiB, zero differences;
- rollover dry mirror: 159,271 files / 1.408 GiB, zero differences;
- authoritative manifest and critical backup hashes matched;
- authoritative reparse topology matched 10 -> 10;
- old rollback paths resolve through the original C: path;
- renamed C: source copies were removed only after fidelity verification and reparse-safe cleanup;
- C: free space recovered from ~13.43 GiB to ~25.48 GiB.

Post-relocation live runtime remains GREEN:

- OpenClaw 2026.9.5;
- Gateway service child PID 30416 after controlled handoff, health ok;
- Discord ready/connected;
- CNX runnerReady=true / globalHookCount=7;
- Tailscale Serve -> 127.0.0.1:12651;
- remote HTTPS 200;
- supervisor Last Result 0;
- `ollama ps` empty;
- free virtual/commit ~20.57 GiB.

Checkpoint:

`docs/operations/coordination/reports/CNX-20260919-427-storage-relocation-and-pre-acceptance-runtime-checkpoint.md`

## Handoff

Read:

`docs/operations/coordination/reports/CNX-20260919-427-full-session-handoff-openclaw-9.5-and-storage-relocation.md`

before continuing.

Final acceptance report:

`docs/operations/coordination/reports/CNX-20260920-427-440-final-discord-acceptance-report.md`

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

## CNX-442 Stop-barrier handoff — 2026-09-21

- Source/remote HEAD: `beaa9cb2a76f64eb06e3713e2857f1f37acd664e`
- Focused authoritative Stop/terminal qualification: 34/34 PASS
- TypeScript build: PASS
- Current installed live runtime is still the older pre-Stop-barrier candidate; source/live hashes differ for `index.js`, `v090.js`, and `v095-host-terminal-evidence.js`.
- Live queue + FIFO + single-writer + Discord typing acceptance is GREEN.
- Live Stop acceptance on the older runtime is RED: current Ticket became failed/permanent, queued Ticket was later dequeued/bound then blocked, though it never entered model inference.
- Exact Host Stop evidence: `status=interrupted`, `aborted=true`, `externalAbort=true`, `timedOut=false`, `stopReason=aborted`, `promptError=agent run aborted | OPENCLAW_DIRECT_ABORT`.
- New source fix at `beaa9cb2` uses authoritative Host terminal evidence to cancel the whole owner session and fence queued work.
- Full suite/plugin validation after `beaa9cb2` still must be rerun before install-over.
- qwen3.8:27b was unloaded at handoff because `activeRuns=0`.
- Full handoff report: `docs/operations/coordination/reports/CNX-20260921-442-session-handoff-stop-barrier.md`

Current gate:

`CNX442_SOURCE_STOP_BARRIER_GREEN_PENDING_FULL_QUALIFICATION_INSTALL_AND_LIVE_RETEST`

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
