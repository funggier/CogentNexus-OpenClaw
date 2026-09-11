# CNX-20260911 — Plan 2 Start Boundary

## Repository

- Repository: `funggier/CogentNexus-OpenClaw`
- Base/main: `1e81b3cb9a8fe31a8e4df90563f15a3cde255c59`
- Working branch: `agent/v0.9.5-plan2-delivery-session-identity`
- Public release baseline: `v0.9.4`
- v0.9.5 is not released/tagged.

## Plan 2 scope

Continue the v0.9.5 architecture line after Plan 1 merge, focusing on physical session-generation semantics and the already-present canonical InferenceAttempt/Delivery Core identity surfaces.

## Initial finding

`v095-inference-attempt.ts` and `v095-delivery-core.ts` are present on main from the verified Plan 1 merge. The planned `v095-session-generation.ts` decision contract was not yet present, so this branch begins with its RED test.

## TDD boundary

RED test commit:

`147b34043701f79926a07114d2b5f648fb29ece6`

Plan document commit:

`d01e487345fb218129cb0333a999e0c65cb83abe`

The focused RED result must be proven by Actions before implementation. No production behavior change is authorized until the RED gate is observed.

## Hard fences

- Do not modify `main` directly.
- No release/tag/public-version mutation.
- Do not alter provider/model/auth routing.
- Preserve exact Ticket, inference-attempt, delivery, session-generation, terminal, and stale-owner fences.
