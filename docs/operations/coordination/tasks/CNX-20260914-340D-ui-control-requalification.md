# CNX-340D — Dashboard UI Control Requalification

Status: `READY_FOR_HERMES`
Task ID: `CNX-340D`
Parent: `CNX-340C`
Executor: `Hermes`
Reviewer: `ChatGPT`

## Objective

Resolve the Dashboard/Web Session activation ambiguity that blocked CNX-340C. Establish a deterministic, repeatable control procedure that can select one fresh Dashboard session and prove the resulting session identity before any semantic input is submitted.

## Base

- Coordination base: `04079485a315f143962c9b3cba7d27254713b51d`
- Evidence head: `e42010f826a4707abc217cb4305b7639f76db8f8`
- Candidate parent: `460a8cd661d02ba419cc1eff13c0efc721cfa928`
- Artifact reference: `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8`
- Published `v0.9.5` remains immutable at `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95`.

## Scope

1. Inspect CNX-340C evidence and the prior CNX-339B browser-control qualification.
2. Determine a deterministic control sequence using supported browser/control mechanisms.
3. Verify the exact target window/process before state-changing input.
4. Verify the post-action Dashboard session identity from UI/address state or another independent session marker.
5. Verify the resulting session is fresh before any semantic input.
6. Use control-only interaction; no semantic request is permitted.
7. Treat any ambiguous activation as consumed; do not repeat it.
8. Prefer existing control/test seams. Any production code change requires a separate TDD cycle and must remain behavior-neutral.

## Hard fences

- No semantic Dashboard request.
- No OpenAI or Ollama inference.
- No provider/model/config/timeout mutation.
- No controller or production database mutation.
- No installation/release/tag mutation.
- No retry, recovery, fallback, resend, or manual dispatch.
- No force push or history rewrite.

## Required evidence

- Exact process/window identity.
- Exact control sequence.
- Pre-action session identity.
- Post-action session identity.
- Independent fresh-session proof.
- Zero semantic traffic.
- Zero production-state mutation.

## PASS criteria

PASS only when a fresh Dashboard session can be deterministically established and independently verified before semantic input, with no semantic traffic or production mutation.

CNX-340D must not re-run CNX-340C. Its output is only a reliable UI-control procedure for a later live timeout requalification.

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
