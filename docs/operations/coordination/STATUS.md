# Coordination Channel Status

Status: `LIVE_READY_FOR_OPERATOR_TEST`
State: `CNX442_LIVE_READY_FOR_OPERATOR_TEST`
Task ID: `CNX-20260920-442`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
## CNX-442 — session serialization / terminal truth

Active task:

`docs/operations/coordination/tasks/CNX-20260920-442-session-input-serialization-and-terminal-truth.md`

Primary scope: native slash-command bypass, OpenClaw followup queue semantics for same-session concurrent user turns, and authoritative user-visible terminal settlement. Status/progress UI is explicitly out of scope for CNX-442.

Source qualification is GREEN: 120 targeted/integration tests PASS, `plugin:validate` PASS, build PASS, Ticket DB bootstrap PASS, package verification PASS, and `git diff --check` PASS.

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
