# Independent Review — CNX-20260827-099

Decision: `ACCEPT`

Disposition:

`ACCEPT_BLOCKER_DASHBOARD_WINDOW_FOREGROUND_TARGETING_BEFORE_SEND`

## Publication fence

Accepted.

Execution HEAD:

`44c343bc86df8020393f19ce971dff723e4384b5`

Report HEAD:

`d5fde8d5f1e5968a1ae5ce11f4017a15d9884dac`

The compare is exactly one commit and exactly one changed file:

`docs/operations/coordination/reports/CNX-20260827-099-final-authenticated-fresh-session-semantic-acceptance.md`

No product source change is published by Task 099.

## Accepted evidence

Task 099 passed the semantic preflight far enough to identify the exact selected authenticated fresh Dashboard target:

`agent:main:dashboard:89992501-1b33-46cf-85f7-eb0c1ef4d311`

The target was reported fresh/empty, distinct from Main and the retired Task-092 session, with the accepted live baseline still intact.

A fresh Task-099 nonce was generated only after preflight:

`CNXSEM3-20260827T082609Z-1687E2DA`

However the semantic message was never successfully sent. Semantic send count remained `0`.

The blocker occurred before product semantic execution: the exact OpenClaw Firefox window could not be proven to be the foreground input target. Another Firefox window/process was foreground, and background focus/typing remained unverifiable. The executor correctly refused to type/send into an unverified target.

Post-state remained read-only/healthy with no Task-099 Ticket, route, provider inference, assistant-delivery row, visible semantic reply, or outbox settlement.

## Comparison with the earlier successful UI semantic attempt

This blocker is materially different from Task 092. Task 092 proved that the authenticated Dashboard/WebChat path could create a fresh Dashboard session, send exactly one semantic prompt, create one Ticket, route before provider inference, invoke `ollama/qwen3.5:9b` once, and render the exact nonce visibly. Task 092 failed later at durable delivery completion, which is the defect repaired by Task 093 and subsequently installed in Task 096.

Task 099 never reached that semantic path. Therefore Task 099 is not evidence that the repaired staging implementation or Ticket/provider pipeline regressed.

## Safety/accounting

- Task-099 semantic send count: `0`.
- Direct provider probes: `0`.
- Product/live mutation: `0`.
- No resend or alternate channel was used.
- The Task-099 nonce is retired and must not be reused.
- The exact Task-099 Dashboard target may be reused only if a successor freshly proves it remains authenticated, selected or explicitly selected, empty, and semantically untouched.

## Successor requirement

Do not immediately repeat the semantic task with another nonce.

First prove the exact OpenClaw Dashboard Firefox window and composer can be safely acquired as the foreground input target with zero semantic send. A successor should separate OS/UI input-target readiness from semantic execution, use the approved state-gated retry policy only for low-impact focus/session-management actions, and stop before nonce generation if foreground/composer identity cannot be proven.

Only independent acceptance of that input-target readiness may authorize a new single-attempt semantic nonce/send.
