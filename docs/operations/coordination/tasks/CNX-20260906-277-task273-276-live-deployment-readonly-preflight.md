# CNX-20260906-277 — Task273-276 Live Deployment Read-Only Preflight

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260906-276`
Executor: `Hermes`
Reviewer: `ChatGPT`

## Objective

Establish the exact live state needed to decide whether the accepted Task273-276 candidate can be safely deployed, without making any live mutation.

Accepted source/test/CI candidate:

`36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`

## Required read-only checks

1. Fresh-read `ACTIVE.md`, `STATUS.md`, Task277, and the Task276 ChatGPT review.
2. Identify the currently installed CogentNexus-OpenClaw plugin root, plugin id/version, payload fingerprint, and whether the installed payload already contains the Task273-275 Discord Direct durable-delivery repairs.
3. Compute/confirm the candidate-bound payload fingerprint for `36cd4c800ded28bdb7165fcad6e0bfb48b4e933b` using the supported repository/package identity path.
4. Compare installed fingerprint vs candidate fingerprint. Do not install or repair anything.
5. Read-only runtime health:
   - OpenClaw Gateway PID/listen/health/version;
   - Ollama/provider reachability/readiness/model;
   - CogentNexus host desired/actual state;
   - supervisor task enabled/cadence/result without mutation.
6. Read-only durable state:
   - protected old Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` and its owner session remain untouched;
   - pending Ticket outbox / assistant delivery / Direct Recovery / workflow counts;
   - sacrificial Discord setup session created for Task272, including exact sessionKey/sessionId/generation and current Ticket/delivery/recovery state.
7. Determine whether the sacrificial setup session is still blocked by the old Discord delivery-boundary defect or otherwise non-clean. Do not dispose, replay, redeliver, cancel, Delete, reset, or mutate it.
8. State the exact live action that would be required next if deployment is needed (normally one supported install-over of the accepted candidate, with installer-owned managed Gateway transition only).
9. Publish a preflight report and stop for ChatGPT review / human live authorization.

## Hard fences

```text
live semantic send                              = 0
live OpenClaw session Delete/reset              = 0
manual Ticket/session/SQLite mutation           = 0
recovery replay/redelivery/disposition           = 0
installer/install-over/uninstall/reset          = 0
Gateway/provider/service lifecycle mutation     = 0
Scheduled Task mutation                         = 0
release/tag/default-branch promotion            = 0
force push/history rewrite                      = 0
```

Task272's previously authorized session Delete/test-message authority remains parked and unconsumed. Do not infer install-over authority from it.

## Completion

Publish:

`docs/operations/coordination/reports/CNX-20260906-277-task273-276-live-deployment-readonly-preflight.md`

Then set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW` and stop.
