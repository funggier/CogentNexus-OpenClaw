# CNX-20260830-156 — Self-Review Checkpoint Policy Integration

Status: `COMPLETED`
Execution mode: `GITHUB_COORDINATION_POLICY_ONLY`
Owner: ChatGPT
Reviewer policy: operator-authorized ChatGPT self-review is permitted through a distinct durable checkpoint; same-actor review is not independent review.

## Objective

Integrate the operator-approved workflow rule into the GitHub coordination layer so ChatGPT may continue repository-capable execution and review its own work through durable Task/Review checkpoints, while Hermes/Codex remains an optional handoff used only when materially necessary or explicitly requested by the operator.

## Scope clarification

This task changes **GitHub coordination workflow/documentation only** under `docs/operations/coordination/`.

It does **not** change CogentNexus runtime behavior, OpenClaw integration behavior, production source, lifecycle behavior, installer behavior, Dashboard behavior, or any live-machine state.

## Implemented policy

1. ChatGPT may execute and review the same repository-capable task when the operator allows that workflow.
2. Same-actor review must be recorded as a distinct durable Task/Review checkpoint.
3. Same-actor review must be explicitly labeled `ChatGPT self-review` and must never be described as `independent`.
4. Reviewer identity separation is optional unless the active task or operator explicitly requires it.
5. Self-review does not weaken safety fences, acceptance criteria, fail-closed behavior, exact-SHA requirements, or evidence thresholds.
6. Hermes/Codex must not be used solely to manufacture reviewer identity separation.
7. Hermes/Codex handoff is appropriate when real-machine/live proof is irreducible or when the operator explicitly requests the handoff.
8. GitHub remains the durable coordination source of truth and the operator remains final authority.

## Files changed

- `docs/operations/coordination/README.md`
  - commit `9d2fb97c761d62483756f922f62d00c1784c71d0`
  - adds durable self-review semantics and removes reviewer separation as a standing handoff requirement.
- `docs/operations/coordination/EXECUTION_OWNERSHIP.md`
  - commit `8576dc5c686cb7cf6b2f62582a2e6c7b5c414ecc`
  - defines the self-review contract and narrows Hermes/Codex escalation to irreducibly local/live proof or explicit operator request.

An accidental empty coordination artifact `.noop` created during checkpoint setup was immediately removed; it is not part of the resulting policy surface.

## Acceptance contract

- GitHub coordination policy only: **PASS**
- ChatGPT self-review explicitly permitted when operator-authorized: **PASS**
- same-actor review explicitly non-independent: **PASS**
- durable checkpoint requirement preserved: **PASS**
- safety/evidence/acceptance gates preserved: **PASS**
- Hermes not required solely for reviewer separation: **PASS**
- Hermes still available for irreducible local/live work or explicit operator handoff: **PASS**
- no CogentNexus runtime/product behavior changed: **PASS**

## Hard-fence result

- live Windows/runtime mutation: `0`
- Dashboard semantic Sends: `0`
- install/reset/uninstall/reinstall invocations: `0`
- production source changes: `0`
- dependency upgrades: `0`
- merge/tag/release operations: `0`
- force pushes: `0`

## Required completion signal

Publish the matching Task-156 review as a `ChatGPT self-review (operator-authorized; not independent)`. If accepted, use the resulting standing policy for subsequent repository-capable reviews and hand off to Hermes/Codex only when the next acceptance step genuinely needs its local/live execution surface or the operator explicitly requests it.
