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

## Current classification

`CNX453_LOCAL_GREEN_CI_PENDING`
