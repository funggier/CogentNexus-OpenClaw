# Review — CNX-20260827-102 Re-establish Dashboard Target and Final Semantic Acceptance

Decision: `ACCEPT`

Disposition: `ACCEPT_BLOCKER_LIVE_DURABLE_PAYLOAD_STAGING_REPRODUCED_AFTER_REPAIR`

Reviewed report commit:

`4d23875f4c402cf47109439ebd6b6b5eb72e131b`

Execution coordination HEAD:

`9b9cb77b77f3e4e57887c4ffa87a0cd273e4ef55`

## Publication fence

Independent compare of execution HEAD -> report HEAD shows exactly one commit and exactly one added file:

`docs/operations/coordination/reports/CNX-20260827-102-reestablish-dashboard-target-and-final-semantic-acceptance.md`

No product-source/config/runtime coordination artifact was changed in the report delta.

## Accepted evidence

Task 102 successfully removed the prior browser/input ambiguity.

Fresh live target proof established:

- Firefox/OpenClaw target was freshly opened and rediscovered;
- exact target session was `agent:main:dashboard:89992501-1b33-46cf-85f7-eb0c1ef4d311`;
- exact `Message Assistant` composer was present and empty;
- foreground equality was proven before input;
- no credential re-entry or disclosure occurred.

The bounded input-method ladder was executed safely. UIA direct edit was unsupported by the available driver snapshot contract and deterministic Win32 handoff did not acquire foreground ownership. The distinct fresh-Firefox/operator-click path did pass: the operator manually clicked the exact already-verified composer once, foreground/session/composer state was re-verified, a non-sent sentinel appeared in the exact composer, and the sentinel was cleared without Ticket/provider effect.

This establishes the current reproducible operator-assisted input method and earns:

`DASHBOARD_INPUT_METHOD_REPRODUCIBLY_PROVEN`

The one authorized semantic turn was then executed exactly once with a fresh Task-102 nonce. Evidence shows:

- exactly one new Ticket: `CNXT-415b82d9-5553-4bd2-996a-54f57163f7e4`;
- exact owner Dashboard session preserved;
- accepted/routed before provider execution;
- exactly one new direct model call on the expected `ollama/qwen3.5:9b` path;
- exactly one visible assistant reply equal to the nonce;
- no semantic resend, duplicate Ticket, duplicate route, duplicate provider call, or duplicate visible reply.

The durable lifecycle stopped after:

`accepted -> routed -> direct_model_call_started -> direct_model_call_ended -> response_ready`

Fresh post-response evidence showed:

- Ticket still `accepted`;
- `response_ready_at` present;
- `delivery_confirmed_at = null`;
- `cnx_assistant_delivery` count remained `0`;
- no `delivery_confirmed` event;
- no `completed` state.

Therefore final semantic acceptance is not earned. The report's blocker is sound:

`BLOCKED_DURABLE_FINAL_PAYLOAD_STAGING`

## Independent source-context check

The accepted installed source `32212a4331e1f32b5a130bd30d271d4cbc56f6c1` does contain the Task-093 verified-delivery implementation and the release entry calls `installV091DashboardVerifiedDelivery(api, config)` after legacy registration. The implementation registers a `reply_dispatch` hook that requires a correlated run id plus `ctx.dispatcher.appendBeforeDeliver`, then stages the final text into `cnx_assistant_delivery` before native delivery.

The existing production-shaped test directly simulates that hook/context and proves the synthetic path, but Task 102 proves the real OpenClaw 2026.7.1-2 Dashboard path can visibly deliver the final while producing zero durable staging rows. This narrows the next investigation to live hook registration/emission/context/correlation rather than owner UI targeting or provider execution.

## Successor constraint

Do not send another semantic message yet. The next task should be source + read-only live diagnosis only and must determine which exact boundary fails in live runtime:

1. verified-delivery installer/wiring not active in the live runtime;
2. real Dashboard delivery does not emit the expected `reply_dispatch` callback;
3. callback emits with a different run/session/dispatcher context than the test models;
4. hook fires but rejects/skips staging due to payload cardinality/correlation/session authority;
5. staging is attempted and throws/fails before commit.

No product fix should be proposed until one boundary is evidenced.

No operator action is required for this diagnosis-only successor. A later live semantic retest may again require the operator to click the exact verified `Message Assistant` composer once and, if explicitly instructed, perform the one authorized Send.