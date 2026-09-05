# CNX-20260905-264 — ChatGPT Review: First-Turn Lifecycle Ordering

## Verdict

`REWORK_REQUIRED__FIRST_TURN_SESSION_START_ORDERING_RACE`

Task264 materially improves lifecycle identity fencing and its exact candidate
`cad96fad3d1cef07fac4173425f15714b33240d6` has valid TDD and exact-SHA CI
evidence. However it does not yet prove the user-visible contract that the
first Discord message after a web session Delete is admitted under the newly
created OpenClaw lifecycle.

## Accepted evidence

- RED commit `9b332dc567d6d577c97a3d77bcd5ff13d66f960c` correctly exposes the Task263 stale/different-lifecycle acceptance defect.
- Production commit `cad96fad3d1cef07fac4173425f15714b33240d6` explicitly rejects active B + stale A/C without mutating generation/session_id.
- `before_agent_run` now has an exact `sessionKey + sessionId` gate.
- Focused/full tests, build, plugin validation, and exact-SHA Actions are green.
- Exact candidate Actions independently verified:
  - PS5.1 Acceptance Smoke `33976180547` — success
  - Windows Installer Pack Smoke `33976180585` — success
  - Validate `33976180571` — success
- Task264 respected all source-only hard fences.

## Blocking defect

OpenClaw treats `session_start` as a void observation hook. Its hook runner binds
`runSessionStart` through the void-hook path, so a returned `{outcome:"block"}`
from a `session_start` handler is not an admission decision.

More importantly, OpenClaw fires `session_start` asynchronously and does not await
it before returning the newly initialized session to the reply pipeline. In
`src/auto-reply/reply/session.ts`, the new lifecycle is durably committed, then
`runSessionStart(...)` is launched through
`runWithGatewayIndependentRootWorkContinuation(...)` with `void`, and
`initSessionState` returns immediately.

Task264's owner-run gate is read-only:

`before_agent_run -> isCurrentSessionLifecycle(...)`

Therefore this race is allowed:

1. old lifecycle A is tombstoned by Delete;
2. OpenClaw creates lifecycle B on the same canonical key;
3. OpenClaw queues asynchronous `session_start(B)`;
4. the first owner turn reaches `before_agent_run(B)` before CNX's session-start callback commits B into `cnx_sessions.session_id`;
5. `isCurrentSessionLifecycle()` sees deleted A (or otherwise not-current B) and blocks the legitimate first message;
6. `session_start(B)` may commit later, so a second user message could succeed.

That is not deterministic recreation and does not satisfy the intended
`Delete -> next Discord message works` contract.

## Required repair direction

The actual admission boundary must reconcile the lifecycle identity atomically
instead of depending on prior completion of a fire-and-forget observation hook.

A minimal acceptable direction is:

- create/use one transactional lifecycle admission helper that receives exact `sessionKey + sessionId`;
- at `before_agent_run`, reconcile then decide in the same operation:
  - deleted A + A => reject;
  - deleted A + B => activate B exactly once, generation +1, admit;
  - active B + B => admit idempotently;
  - active B + A/C => reject without mutation;
  - deleting => reject;
  - active legacy NULL => deterministic bind without generation churn;
- `session_start` may still eagerly reconcile as an optimization/observation, but correctness must not depend on it running first;
- no stale/different lifecycle may hijack an already active B;
- old-generation Ticket/recovery/outbox/assistant-delivery/workflow/synthetic fences must remain unchanged.

## Required RED proof

Add a regression that reproduces OpenClaw ordering rather than manually calling `session_start` first:

1. database is tombstoned for A;
2. register plugin hooks;
3. invoke the actual registered `before_agent_run` for new B **before any session_start(B) handler is invoked**;
4. B must be admitted and durable row must become active/B with one generation advance;
5. invoke stale A/C afterward and prove fail-closed with no mutation;
6. invoke delayed/duplicate `session_start(B)` afterward and prove idempotency.

The RED must fail against Task264 production code for the intended first-turn reason.

## Authority

This review does not authorize live session deletion, Discord semantic sends,
Gateway changes, installer actions, or manual live DB mutation. Open bounded
source/test/CI rework only.
