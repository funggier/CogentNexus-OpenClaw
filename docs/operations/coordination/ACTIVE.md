# Active Coordination Task

Status: `READY_FOR_OPERATOR`
State: `V096_HUMAN_ASSISTED_SESSION_ACTIVATION`
Execution mode: `HUMAN_UI_ACTION__READ_ONLY_VERIFICATION`
Task ID: `CNX-340E`
Parent: `CNX-340D`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human action: `Operator`
Base CNX-340D HEAD: `30da4c5842d55f555e32155cc87391255938f296`
Active branch: `agent/v0.9.6-human-assisted-session-activation`

## Objective

Establish exactly one fresh Dashboard/Web Session by having the human operator perform the visible `New session` click, then allow Hermes to verify the resulting session identity and fresh state read-only. No semantic request is permitted in this task.

## Hard fences

- Exactly one human `New session` click.
- No Hermes click or keyboard fallback.
- No semantic request.
- No OpenAI/Ollama inference.
- No second session attempt.
- No retry, recovery, fallback, resend, manual dispatch.
- No provider/model/config/timeout mutation.
- No controller or production database mutation.
- No installation/release/tag mutation.
- No force push/history rewrite.

## Operator protocol

1. Hermes tells the operator to click the visible `New session` control once.
2. Operator performs the click normally in the authenticated OpenClaw Control Dashboard.
3. Operator replies with explicit confirmation, e.g. `กดแล้ว`.
4. Hermes performs read-only verification only after confirmation.
5. If a new session is not verifiable, stop; do not click again.

## Required evidence

- exact browser process/window identity
- pre-action session identity
- operator-confirmed action
- post-action session identity
- independent fresh-session marker
- fresh rendered state
- zero semantic traffic/inference
- zero production-state mutation

## PASS criteria

PASS only if the operator-confirmed click creates one fresh Dashboard session and Hermes independently verifies its new identity and fresh rendered state before any semantic input.

## Required report

Publish `docs/operations/coordination/reports/CNX-20260914-340E-human-assisted-session-activation-report.md` and stop for independent ChatGPT review. Do not run live timeout requalification inside CNX-340E.
