# Active Coordination Task

Status: `EXECUTING_CHATGPT`
Execution mode: `TASK188_DOCUMENTATION_PAYLOAD_CONVERGENCE_AND_PROPORTIONAL_REQUALIFICATION`
Current disposition: `IN_PROGRESS`
Task ID: `CNX-20260831-188`
Updated: 2026-08-31 ICT
Executor: ChatGPT / Hermes for bounded Windows requalification when required
Coordinator / final reviewer: ChatGPT
Human release authority: User — documentation must be made current first, then v0.9.3 publication may proceed when gates pass.

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative.

## Active task

[`tasks/CNX-20260831-188-documentation-payload-convergence-and-proportional-requalification.md`](tasks/CNX-20260831-188-documentation-payload-convergence-and-proportional-requalification.md)

Task-187 review:

[`reviews/CNX-20260831-187-final-documentation-convergence-and-v093-release-publication-review.md`](reviews/CNX-20260831-187-final-documentation-convergence-and-v093-release-publication-review.md)

## Starting authority

Task-188 pre-task HEAD:

`fa3c89d93b506f2e7ccfb167cc665e593ebf1373`

Previously accepted implementation candidate:

`f6392da3e4112ce441526d5ef19925c90a872b0b`

Accepted active facade SHA-256:

`aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`

Previously accepted package payload-v2:

`df6e395a47b632c779d12dd95f9ce762c7f28ca2740442b8b299ff622df94959` / `184` files

Accepted live installed-plugin inventory fingerprint:

`e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`

## Current objective

Correct stale current-facing plugin/skill documentation, freeze the resulting documentation-only artifact, prove executable/runtime identity preservation, run exact-candidate CI/package validation, then perform proportional Windows requalification before returning to PR/merge/release publication.

## Requalification principle

The implementation has already passed the full v0.9.3 stabilization sequence at a meaningful level. Documentation/instruction-only changes therefore require bounded proportional requalification by default, not automatic repetition of reset/uninstall/fresh-reinstall.

Default Windows requalification: exact install-over + provenance/health/skill-byte proof + one semantic durable-delivery turn. Destructive lifecycle tests repeat only if evidence requires them.

## Hard fence

No production/runtime/plugin executable source, test, dependency, workflow-behavior, provider/runtime semantic, or durable-schema changes under Task 188 merely to make release pass. No force push.
