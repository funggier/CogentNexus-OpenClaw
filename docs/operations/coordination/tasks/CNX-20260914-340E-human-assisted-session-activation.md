# CNX-340E — Human-Assisted Dashboard Session Activation

Status: `READY_FOR_OPERATOR`
Task ID: `CNX-340E`
Parent: `CNX-340D`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human action: `Operator`

## Objective

Establish one fresh Dashboard/Web Session using a human-confirmed UI action because CNX-340C and CNX-340D could not deterministically verify a synthetic browser click on `New session`.

This task separates the human UI activation from the later semantic timeout requalification. The operator performs the single state-changing `New session` click; Hermes performs only read-only post-action verification. No semantic input is permitted in this task.

## Base / Evidence

- CNX-340D final candidate commit: `30da4c5842d55f555e32155cc87391255938f296`
- Candidate implementation parent: `460a8cd661d02ba419cc1eff13c0efc721cfa928`
- Candidate artifact SHA-256: `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8`
- Published `v0.9.5`: `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95` (immutable)

## Human Action Protocol

1. Hermes must first provide the operator with the exact instruction to click the visible `New session` control in the authenticated OpenClaw Control Dashboard.
2. The operator performs exactly one click using the normal browser UI.
3. The operator replies with an explicit confirmation such as `กดแล้ว`.
4. Only after that confirmation may Hermes perform read-only browser/session verification.
5. Hermes must not click `New session`, send keyboard activation, type semantic content, press Enter, press Send, or otherwise submit a semantic request.

## Required verification

After operator confirmation, Hermes must capture the Dashboard state and prove:

- target window/process identity
- pre-action session identity if observable from retained capture/report
- post-action session identity
- independent evidence that the new session is distinct
- fresh session rendered state (conversation empty / equivalent fresh marker)
- composer ready and untouched
- semantic traffic count remains zero
- inference count remains zero
- no provider/model/config/timeout/controller mutation
- no production database mutation

If the normal UI action did not create a fresh session, do not attempt another click. Report the exact observed state and stop.

## Hard fences

- Exactly one human `New session` click.
- No Hermes click or keyboard fallback.
- No semantic request.
- No OpenAI/Ollama inference.
- No second session attempt.
- No retry, recovery, fallback, resend, manual dispatch.
- No provider/model/config/timeout mutation.
- No controller mutation.
- No production DB mutation.
- No installation/release/tag mutation.
- No force push/history rewrite.

## PASS criteria

PASS only if one human-confirmed click creates a new Dashboard session and Hermes independently verifies the new session identity and fresh rendered state before any semantic input.

## Failure classifications

- `UI_HUMAN_ACTION_NOT_CONFIRMED`
- `UI_NEW_SESSION_NOT_VERIFIABLE`
- `UI_FRESH_SESSION_STATE_NOT_VERIFIABLE`
- `UNEXPECTED_SEMANTIC_TRAFFIC`
- `PRODUCTION_STATE_MUTATION`
- `ARTIFACT_PROVENANCE_MISMATCH`

## Required report

Publish:
`docs/operations/coordination/reports/CNX-20260914-340E-human-assisted-session-activation-report.md`

Then stop for independent ChatGPT review. Do not proceed to live timeout requalification within this task.
