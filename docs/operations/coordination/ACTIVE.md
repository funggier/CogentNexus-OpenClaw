# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `V096_UI_CONTROL_REQUALIFICATION`
Execution mode: `SINGLE_EXECUTOR`
Task ID: `CNX-340D`
Parent: `CNX-340C`
Base candidate: `agent/v0.9.6-direct-model-call-timeout-authority-repair`
Base candidate HEAD: `460a8cd661d02ba419cc1eff13c0efc721cfa928`
Evidence qualification HEAD: `e42010f826a4707abc217cb4305b7639f76db8f8`
Active branch: `agent/v0.9.6-ui-control-requalification`

## Objective

Resolve the Dashboard/Web Session activation ambiguity that blocked CNX-340C. Establish a deterministic, repeatable control procedure that can select one fresh Dashboard session and prove the resulting session identity before any semantic input is submitted.

## Executor / Reviewer

- Executor: `Hermes`
- Reviewer: `ChatGPT`
- Human authority: fresh continuation explicitly authorized by the operator after CNX-340C review.

## Hard fences

- No semantic Dashboard request.
- No OpenAI or Ollama inference.
- No provider/model/config/timeout mutation.
- No controller or production database mutation.
- No installation/release/tag mutation.
- No retry, recovery, fallback, resend, or manual dispatch.
- No force push/history rewrite.
- Any ambiguous activation is consumed and is not repeated.

## Required evidence

1. Exact targeted browser process/window identity.
2. Exact control action sequence.
3. Verifiable pre-action session identity.
4. Verifiable post-action session identity or an independent fresh-session marker.
5. Proof the resulting session is fresh before semantic input.
6. Zero semantic traffic.
7. Zero production-state mutation.
8. If a test/control seam is added, focused verification and exact diff scope.

## PASS criteria

PASS only when a fresh Dashboard session can be established and independently verified before semantic input, with no semantic traffic or production mutation. This task must not run CNX-340C again.

## Failure classifications

- `UI_WINDOW_TARGET_NOT_DETERMINISTIC`
- `UI_FOREGROUND_NOT_VERIFIABLE`
- `UI_NEW_SESSION_NOT_VERIFIABLE`
- `UI_FRESH_SESSION_STATE_NOT_VERIFIABLE`
- `UNEXPECTED_SEMANTIC_TRAFFIC`
- `PRODUCTION_STATE_MUTATION`
- `CONTROL_SEAM_REGRESSION`
- `ARTIFACT_PROVENANCE_MISMATCH`

## Required report

Publish `docs/operations/coordination/reports/CNX-20260914-340D-ui-control-requalification-report.md` and stop for independent ChatGPT review. Do not self-accept CNX-340D.

## Previous state

- Plan 2 remains closed.
- CNX-339 remains historical evidence and is not replayed.
- CNX-340A is the timeout-authority repair.
- CNX-340B closed the hook-evidence gap.
- CNX-340C was blocked by `UI_ACTIVATION_AMBIGUOUS`; do not repeat that semantic attempt.
