# CNX-20260926-453 — Scheduled Supervisor Direct-Lease Fence and Gateway Recovery Settlement

Status: `ACTIVE`
Owner: ChatGPT
Executor: ChatGPT
GitHub issue: `#45`
Baseline SHA: `09eec4113b371d39334d90a332fa9a6455530db0`
Baseline task: CNX-451 candidate (code/CI/install green; live acceptance blocked by this defect)
Baseline release: `v0.9.8` (immutable)
Working branch: `cnx-453-supervisor-direct-lease-fence`

## Trigger

A dedicated CNX-451 live acceptance run exposed a physical Gateway recovery defect while an Ollama Direct model call still had an unexpired 45-minute durable lease.

Session:
- `agent:main:dashboard:cnx451-soft-acceptance-01`
- OpenClaw session id `50bf4189-2a86-4a6c-be1c-c9dc6a0153cb`
- Ticket `CNXT-071588b9-4d6b-4e30-8935-51ba99887293`
- run `b40ea823-e273-4f37-81e2-d987d9d7509a`
- call `b40ea823-e273-4f37-81e2-d987d9d7509a:model:1`
- provider/model `ollama/qwen3.8:27b`
- model-call lease: `10:03:47.895Z -> 10:48:47.895Z`

At `10:20:26Z`, before lease expiry, the scheduled Host entered hard-hang maintenance and stopped the Gateway. The OpenClaw agent client consequently ended with WebSocket 1006.

## Physical evidence

- The call crossed the historical 15-minute timeout boundary without being timed out; CNX-449 45-minute lease was installed.
- Before recovery: exactly one model call and one inference attempt; no duplicate recovery.
- Ledger seq 484: maintenance enabled for confirmed unresponsive Gateway at `10:20:26Z`.
- Ledger seq 485: Gateway stop/force; stop command timed out, but verification confirmed Gateway stopped.
- Startup reconciliation later restored Gateway healthy and created a recovery continuation Ticket rather than requiring user resend.
- Original Ticket became `waiting/interrupted`, but its original `cnx_direct_model_call` and `cnx_inference_attempt` rows remained `active`.
- No `host_direct_model_gateway_interruption_authorized` event was written for the original call.
- Installed/source SHA-256 parity is exact for `host_v091.py`, `host_stall_v091.py`, `host_control_v092.py`, and `host_provider_v092.py`.
- Historical-state replay at `10:20:26Z` with the known Ticket/call state returns `gateway-long-running-protected`; therefore the existing unit guard is correct in isolation but insufficient as the destructive recovery fence observed physically.

## Objective

Make the destructive Gateway recovery boundary fail closed around active Direct execution and make startup recovery settle stale execution evidence atomically enough that later supervisor ticks cannot treat an interrupted old call as still live.

## Required semantics

1. An active, unfenced, unexpired Direct model-call lease is a destructive-restart fence.
2. A failed Gateway health probe alone must not override that lease.
3. The scheduled-supervisor composition must enforce the fence before lifecycle prepare/stop/restart.
4. If a Gateway process boundary is confirmed and Direct work is interrupted, the old model-call row and canonical inference-attempt row must be ended/interrupted before a resume is authorized.
5. Startup fallback promotion must not leave active model-call/inference-attempt rows attached to a Ticket it converts to interrupted recovery.
6. Recovery continuation may create a new run only from durable interruption authority; user resend is not required.
7. No duplicate inference or duplicate delivery.
8. Provider/model/auth ownership remains OpenClaw-owned.
9. `v0.9.8` remains immutable.

## TDD acceptance

- RED: exact periodic-supervisor composition with an unexpired active Direct call cannot reach destructive Gateway recovery.
- GREEN: destructive lifecycle method is not invoked while the lease is unexpired.
- Expired/fenced control: bounded recovery remains allowed.
- Startup interruption fixture: promoted Direct Ticket has no stale active model-call row and no stale active canonical inference attempt.
- Existing CNX-448 terminal fence, CNX-449 lease, CNX-451 soft-pressure and Direct recovery tests remain green.
- Full Python/Vitest/build/evaluation/plugin validation/audit/diff-check.
- Exact-SHA GitHub CI.
- Physical install-over and live requalification.

## Local qualification checkpoint

Implemented locally:

- scheduled-entry outer Direct-lease fence;
- active Direct evidence survives `workflow_eligible` lane drift;
- startup promotion settles predecessor model-call + canonical inference attempt;
- Windows Scheduled Task recovery budget increased from `PT2M` to `PT15M` while retaining `IgnoreNew`;
- validator and dedicated template contract test prevent scheduler-budget regression.

Validation:

- focused CNX-453 Host tests: `32/32 PASS`;
- full Python: `753 passed, 5 skipped, 38 subtests passed`;
- full Vitest: `95 files / 444 tests PASS`;
- build/evaluation/plugin validation/audit/diff-check/skill validation: PASS;
- evaluation evidence SHA-256: `83c89865e15166039807a7ba99db517ed8d161037c1e5f2274aa0adffb3eb622`.

Operational note: persistent User `OLLAMA_KEEP_ALIVE` is now `6h`; the running Ollama process still has the inherited `2h` value and will be restarted only after durable work is quiescent.

## Physical candidate checkpoint

First candidate `21176b07ad98ada944612d444fe5e2d9a8ee0d2b`:
- exact-SHA CI 3/3 SUCCESS;
- physical install-over exit `0`;
- installed/source Host hashes exact for repaired surfaces;
- Windows Supervisor reports `ExecutionTimeLimit=PT15M`, `IgnoreNew`, and successful ticks;
- controller returned MANAGED generation `40`.

Physical requalification exposed one narrower boundary case: the session freshness fence correctly prevents resuming a session older than 15 minutes, but the same filter also prevented settlement of that session's pre-boundary active model-call / canonical inference-attempt.

Follow-up repair:
- execution settlement is now independent of stale-session resume authorization;
- non-promotable pre-cutoff active Direct calls are settled as `host-startup-boundary-settled`;
- their canonical attempts end with the same outcome;
- Ticket lane/status is not promoted merely to settle execution evidence;
- fresh-session promotion retains existing `host-startup-interruption-promoted` semantics.

Follow-up validation:
- RED reproduced the physical stale active call;
- focused GREEN `2/2`;
- CNX-453 Host regressions `33/33`;
- full Python `754 passed, 5 skipped, 38 subtests passed`;
- full Vitest `95 files / 444 tests PASS`;
- build/evaluation/plugin validation/audit/diff-check/skill validation PASS;
- evaluation evidence SHA-256 `48e3dc446018c96cc4dcff6d888d06eb281a5e525b0526b2c8cce90c5a1f8d6f`.

## Final physical qualification

Follow-up candidate `f90a67b739ed60355c9194407f6b7e20309a5918` passed exact-SHA CI:
- Validate `36241804747` — SUCCESS;
- PS5.1 Acceptance Smoke `36241804750` — SUCCESS;
- Windows Installer Pack Smoke `36241804778` — SUCCESS.

Installed Host surfaces match source byte-for-byte for the repaired files. The installed Windows Supervisor reports `ExecutionTimeLimit=PT15M`, `MultipleInstances=IgnoreNew`, one-minute cadence, and successful ticks.

Physical long-running requalification:
- session `agent:main:dashboard:cnx453-soft-live-v2`;
- Ticket `CNXT-41b9af1b-a2e9-48ff-81b4-b1d468fbc6da`;
- run `2e4c1f7f-372b-4702-916d-7c943eabeb31`;
- provider/model `ollama/qwen3.8:27b`;
- call #1 ran `1,384,388 ms` (~23m04s) and ended `toolUse`;
- the intermediate tool-use did not produce `response_ready`, delivery, or completion;
- call #2 ran `233,345 ms` (~3m53s) and produced the terminal assistant result;
- Ticket completed only after call #2;
- one durable response/delivery confirmation, zero outbox residue;
- Gateway stayed HTTP 200 and scheduled supervisor ticks remained successful throughout the >15-minute execution;
- no premature maintenance or Gateway restart occurred.

Startup settlement requalification:
- original prime call `b40ea823...:model:1` is now `interrupted / host-startup-boundary-settled`;
- its canonical attempt is `ended / host-startup-boundary-settled`;
- continuation call `c3b3fc87...:model:1` and attempt are ended with `host-gateway-interruption-authorized`;
- no active Direct model-call residue remains.

Operational keep-alive:
- persistent User `OLLAMA_KEEP_ALIVE=6h`;
- live `ollama ps` confirms `qwen3.8:27b ... UNTIL 6 hours from now`.

Two historical inference-attempt rows from 2026-09-22/23 remain marked active without active model-call rows. They predate CNX-453 and are recorded as separate cleanup debt; they did not participate in this recovery or lease decision.

Status: `COMPLETE`

## Final classification

`CNX453_SCHEDULED_SUPERVISOR_DIRECT_LEASE_GREEN`
