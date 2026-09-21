# CNX-442 Session Handoff — Authoritative Stop Barrier

Date: 2026-09-21
Repository: `funggier/CogentNexus-OpenClaw`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Authoritative repository state

- Historical handoff source HEAD / remote HEAD: `beaa9cb2a76f64eb06e3713e2857f1f37acd664e` (superseded by final production candidate `8dee9cd635ca3dfcbf96f2f4161b5026355dbcf9`)
- Historical commit: `CNX-442 enforce authoritative Stop barrier`
- Working tree was clean at handoff.
- Important implementation ancestry:
  - `49d8e259fb6760583caa706af526cb1b165a5799` — bind queued ingress before `before_agent_run`
  - `f27a5fbd273419bebf9ac624c3fb0524403bb1c2` — queued ingress + active Discord typing hardening
  - `beaa9cb2a76f64eb06e3713e2857f1f37acd664e` — authoritative Stop barrier

## What already passed live

The queue/typing acceptance before the Stop test is GREEN:

1. A clean physical Discord session was created.
2. First operator turn produced exactly one Ticket and one actual run.
3. Second turn was durably persisted while the first run was active.
4. Second Ticket remained unbound with zero model calls / zero inference attempts while waiting.
5. First run completed and delivery was confirmed.
6. Only then did the second claim bind to a new run and start its model call.
7. The active writer changed from run 1 to run 2 only after run 1 terminal completion.
8. Discord visibly showed `Ce is typing...` when queued run 2 became active.
9. Both queue-test Tickets ended `completed`, deliveries `confirmed`, `activeRuns=0`, pending inputs/outbox/recovery all zero.
10. A Dashboard `Pinching...` indicator remained stale until browser refresh; authoritative Gateway/DB state was already terminal, so that symptom is client-side stale UI and is not part of CNX-442 core scope.

Queue-test physical session:
`116561dd-8ecb-4495-9262-87936f0e3667`

Queue-test Tickets:
- Run 1 Ticket: `CNXT-2f48ffcf-92fe-4e9c-84b3-6d37bff46919`
- Run 2 Ticket: `CNXT-6a2a15d3-f60c-4f7e-9266-45fd7be9bacc`

## Live Stop test that exposed the remaining bug

The deployed runtime during this test was still the older `49d8e259...` candidate, not `beaa9cb2...`.

Physical session:
`d18fa6bb-a870-4f5e-86a0-3d923a783cfa`

Current/active Stop-test Ticket:
- Ticket: `CNXT-49e1e2a4-e858-4c9f-889c-8f16be057c52`
- Run: `e07de29f-9e6d-47a1-af9c-435036354dab`
- Prompt: `CNX442_STOP_TEST_1`

Queued Stop-test Ticket:
- Ticket: `CNXT-1261f427-9861-4288-b1aa-bae5a0b30462`
- Provisional ingress existed before Stop.
- It had zero model calls and zero inference attempts while queued.
- After Stop, old runtime still dequeued/bound it to run `7085f04d-5fff-42a9-9935-34b45fc335ec`.
- It still had zero model calls / zero inference attempts.
- It was then blocked and failed with `Your message could not be sent: blocked by cogentnexus-openclaw`.
- Its recovery row ended `cancelled`.
- Final live state after the failed Stop semantics test: `activeRuns=0`, pending input=0, pending outbox=0, active recovery=0.

The old runtime classified the first stopped Ticket as:
- status = `failed`
- failure_class = `permanent`
- model call outcome = `error`
- failureKind = `aborted`

This was wrong for the intended Stop contract. User Stop should establish a session cancellation barrier and cancel current + queued Tickets.

## Exact authoritative Host evidence for user Stop

OpenClaw agent SQLite contains this exact `session.ended` event for run `e07de29f-9e6d-47a1-af9c-435036354dab`:

- sessionId = `d18fa6bb-a870-4f5e-86a0-3d923a783cfa`
- timestamp = `2026-09-20T16:32:48.781Z`
- status = `interrupted`
- aborted = `true`
- externalAbort = `true`
- timedOut = `false`
- idleTimedOut = `false`
- timedOutDuringCompaction = `false`
- timedOutDuringToolExecution = `false`
- timedOutByRunBudget = `false`
- promptError = `agent run aborted | OPENCLAW_DIRECT_ABORT`
- stopReason = `aborted`

This is the authoritative signal the new source fix uses. Do not rely only on `agent_end.error`: in the live Stop incident the plugin-facing `agent_end` error string was empty even though Host trajectory correctly recorded the external user abort.

The queued run later produced a different Host terminal event:
- run = `7085f04d-5fff-42a9-9935-34b45fc335ec`
- status = `error`
- aborted = false
- externalAbort = false
- promptError = `Your message could not be sent: blocked by cogentnexus-openclaw`

## Source fix at beaa9cb2

The source fix adds authoritative Stop handling in:
- `plugins/cogentnexus-openclaw/src/v095-host-terminal-evidence.ts`
- `plugins/cogentnexus-openclaw/src/index.ts`
- `plugins/cogentnexus-openclaw/src/v090.ts`
- focused regressions in CNX-442 and v0.9.0 test suites.

Important behavior:

- `isAuthoritativeUserStop(...)` recognizes only authoritative external user abort evidence.
- restart/supersession aborts are not treated as user Stop.
- `waitForHostRunTerminalEvidence(...)` waits boundedly for delayed Host terminal evidence.
- `cancelDirectOwnerSessionForAuthoritativeUserStop(...)` applies the owner-session cancellation barrier, advances the generation, cancels current + queued Tickets, cancels direct recovery, removes pending delivery work, and is idempotent.
- CNX host-terminal reconciliation invokes the Stop barrier when exact authoritative Host evidence says external user abort.
- v0.9.0 `agent_end` handling now resolves empty/ambiguous plugin errors against authoritative Host terminal evidence instead of guessing intent from the error string alone.
- A queued Ticket that Host later attempts to dequeue after Stop is fenced as cancelled and must not execute.

## Qualification already completed for beaa9cb2

Immediately before handoff:

- `src/cnx442-session-serialization-terminal-truth.test.ts`: 24/24 PASS
- `src/v090.test.ts`: 10/10 PASS
- combined focused Stop/terminal qualification: 34/34 PASS
- TypeScript build: PASS
- canonicalized 46 dist text files to LF
- source HEAD = remote HEAD = `beaa9cb2a76f64eb06e3713e2857f1f37acd664e`

Do not overclaim full qualification yet:
- A full plugin suite has NOT been rerun after the `beaa9cb2` Stop-barrier commit in this handoff session.
- The previous candidate before Stop-barrier changes had full-suite baseline with only the historical intentional CNX-383 projection RED.
- The new session should rerun full suite / plugin validation before install-over.

## Source vs currently installed live runtime

The authoritative source `beaa9cb2` is NOT deployed yet.

Hash comparison at handoff:

| File | Source HEAD SHA-256 | Installed live SHA-256 | Equal |
|---|---|---|---|
| `dist/index.js` | `967961C744D00909E802A96F55C34BBCC2B8C6899575457465AEB5C565F7B62A` | `CC91F8FBB98E8D2B084AB2A4886877B4517534A5E4D0F5FE24232ADEA5E6D3F1` | NO |
| `dist/v090.js` | `0C64F4C55E71E13A80D08C75A48E7FE35D2AB49B29DBA8E316F8926C29DD03A3` | `9669DE374833E0C1B3F09A9C70EB5270FD5BA32BE9459E7DBBD44D0FE6B10E43` | NO |
| `dist/v095-host-terminal-evidence.js` | `1A43A32AD85EF15513DB2B8F8677DAADFC87E68996318AC971F613DA38B13DED` | `95BBCA2115CDDBAF16B259F530A1AF63FE86E6B3D94B9D083006EB3DB31BF553` | NO |
| `dist/ticket-store.js` | `5491DE03F75824EFD45489B269EE4BE237781CBE411E0CA1E3BD098572469048` | same | YES |

Therefore the next session MUST NOT interpret the current live Stop behavior as evidence against `beaa9cb2`; that source has not been installed yet.

## Machine/runtime state at handoff

- Gateway was healthy after the Stop test.
- Discord `activeRuns=0`, `busy=false`.
- qwen3.8:27b was explicitly unloaded at handoff because there were no active runs.
- Keep desired model/runtime policy:
  - provider/model: `ollama/qwen3.8:27b`
  - `OLLAMA_CONTEXT_LENGTH=24576`
  - `OLLAMA_KEEP_ALIVE=2h`
  - `messages.queue.mode=followup`
- Do not raise context above 24K unless user explicitly requests it.
- Use T: for large temporary logs/backups when possible.
- Do not send semantic Discord messages on the user's behalf.

The failed Stop-test physical session is intentionally still present as evidence. It can be deleted through supported fenced `sessions.delete` after the new session has inspected anything it still needs. Do not mutate live SQLite directly.

## Exact next steps for the new ChatGPT session

1. Read:
   - `docs/operations/coordination/ACTIVE.md`
   - `docs/operations/coordination/STATUS.md`
   - this handoff report
   - existing CNX-442 task/report
2. Verify Git:
   - branch `cnx-357-openai-dashboard-ticket-first-requalification-v2`
   - local HEAD = remote HEAD = `beaa9cb2a76f64eb06e3713e2857f1f37acd664e`
   - worktree clean
3. Rerun source qualification for `beaa9cb2`:
   - full plugin test suite
   - expect only historical intentional CNX-383 RED if baseline remains unchanged; investigate any other RED
   - `npm run build`
   - `npm run plugin:validate`
   - `git diff --check`
4. If source remains GREEN by repository baseline, perform supported install-over from exact `beaa9cb2`.
5. Verify candidate/live SHA parity for at least:
   - `dist/index.js`
   - `dist/v090.js`
   - `dist/v095-host-terminal-evidence.js`
   - `dist/ticket-store.js`
6. Verify Gateway/Discord/controller/supervisor/queue mode and runtime attestation.
7. Inspect and then delete the failed Stop-test physical session through supported fenced `sessions.delete`; do not edit SQLite manually.
8. Begin a clean live Stop re-test:
   - user sends first long-running turn
   - verify exactly one Ticket/one active run
   - user sends second turn while first is active
   - verify second Ticket persisted, unbound, zero model calls/attempts
   - user presses Stop
9. Acceptance criteria after Stop:
   - first active Ticket = `cancelled` (not failed/permanent)
   - second queued Ticket = `cancelled`
   - second Ticket has zero model calls and zero inference attempts
   - queued claim must not become executable after Stop; if Host assigns a run anyway, CNX must suppress it as cancelled before inference
   - owner session generation advances exactly once for the Stop barrier
   - pending input = 0
   - pending outbox = 0
   - active recovery = 0
   - no recovery/resurrection after a bounded observation period
   - Discord/Gateway returns idle
10. If live Stop acceptance passes, update CNX-442 report/ACTIVE/STATUS and publish final checkpoint. Only then consider CNX-442 fully GREEN.

## Important side issue discovered but not part of the current Stop gate

Earlier qwen runs exceeded the CNX-recorded 15-minute model-call deadline (one observed model call ran about 18m24s). This suggests a timeout-contract issue between metadata and actual Host/Ollama cancellation. Record/follow it separately after CNX-442 Stop semantics are closed; do not mix it into the queue/Stop repair unless it blocks acceptance.

## Current handoff status

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
