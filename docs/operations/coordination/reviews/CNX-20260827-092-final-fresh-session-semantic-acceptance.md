# Review — CNX-20260827-092 Final Fresh-Session Semantic Acceptance

Decision: `ACCEPT`

Disposition: `ACCEPT_BLOCKER_DASHBOARD_DURABLE_PAYLOAD_STAGING`

Reviewed report HEAD:

`0939c8b0659f0254c754dd7bbf44dc422648c4da`

Execution HEAD:

`e1c970d39fead1bae43509ab720731f0229533c0`

## Publication fence

Accepted.

- Execution -> report is exactly one commit.
- The only changed file is `docs/operations/coordination/reports/CNX-20260827-092-final-fresh-session-semantic-acceptance.md`.
- No product/source/config/runtime mutation is present in repository history for Task 092.

## Accepted fresh-session evidence

The operator-requested fresh-session gate materially passed through the first semantic turn.

The authenticated Control UI invoked New chat before the send and entered a clean staged state. The semantic target became:

`agent:main:dashboard:76932fbc-9df2-4415-9020-b6c1d7228505`

Accepted facts:

- the session key was not present as the prior active Main semantic target;
- the staged transcript was empty before send;
- prior Main Session was not active;
- no stale/unknown/missing-parent error was observed;
- no silent fallback to the prior Main Session was observed;
- no Ticket/provider effect existed before the one authorized send;
- the fresh owner session then correlated to exactly one Ticket and one run.

Therefore the previously suspected first-New-Session/parent-resolution path is not the blocker in this run.

The required post-completion second New Session continuity check remains unexecuted because durable delivery did not reach `completed`; it must remain part of the eventual final semantic successor.

## Accepted semantic ordering/provider evidence

Task 092 used exactly one authenticated Dashboard/WebChat semantic message and did not retry it.

Accepted correlation:

- Ticket: `CNXT-90b73131-5460-4d0d-8669-2bc86a544754`
- Run: `a2ea6b32-fd1a-4235-a6c5-820d475ea4cc`
- Owner session: `agent:main:dashboard:76932fbc-9df2-4415-9020-b6c1d7228505`
- provider/model: `ollama/qwen3.5:9b`
- direct model call count: `1`

Durable ordering is accepted:

`accepted -> routed -> direct_model_call_started -> direct_model_call_ended -> response_ready`

with `accepted` and `routed` preceding provider start. No duplicate Ticket, route, provider call, resend, direct provider probe or semantic effect was observed.

The model produced the exact nonce and the Dashboard visibly rendered it exactly once.

## Delivery blocker

Final acceptance correctly failed because visible output did not become durable delivery completion.

Accepted blocker evidence:

- exactly one `response_ready` exists;
- visible exact nonce exists;
- `delivery_confirmed_at` is null;
- `cnx_assistant_delivery` row count is zero;
- Ticket ended `failed`, failure class `permanent`;
- failure text states that Direct response delivery became unverifiable before the final payload was durably captured and regeneration was refused;
- `failure_delivery_suppressed` is present;
- no duplicate output/regeneration occurred.

This is a valid fail-closed outcome. A visible response alone is not accepted as success.

## Independent source observation

The accepted v0.9.3 source intends Dashboard Direct delivery to stage the exact final text in `cnx_assistant_delivery` from `reply_dispatch` before native transport. `stageDashboardDirectResult()` creates that durable row and only a staged row may later be confirmed by the native dispatcher/marker settlement path.

Task 092 produced no `cnx_assistant_delivery` row despite a visible final response. Therefore the exact final payload staging boundary did not take ownership in the live WebChat path.

A particularly strong root-cause candidate is the v0.9.1 installation guard in `installV091DashboardVerifiedDelivery()`: the same `PATCH` marker on `TicketStore.prototype` guards both one-time prototype monkey-patching and registration of the runtime `reply_dispatch` hook. If the plugin is registered again in the same process after the prototype has already been patched, the function returns before registering `reply_dispatch` on the new runtime registration. This would preserve the V091 patched `finalizeDirectRun/recoverUndeliveredDirect` behavior while losing the staging hook — precisely the combination observed live.

This candidate is not yet promoted to proven root cause. The successor must inspect exact installed OpenClaw plugin reload/hook-lifetime behavior and Task-092 correlation evidence before changing production code. If reload lifetime does not explain the missing staging row, it must inspect the actual WebChat `reply_dispatch` event/context/payload shape and every early-return predicate.

## Retired semantic artifacts

Task-092 semantic artifacts are permanently retired and must not be reused:

- nonce `CNXSEM2-20260827T034759Z-89DA9619`;
- session `agent:main:dashboard:76932fbc-9df2-4415-9020-b6c1d7228505` as a final-acceptance target;
- Ticket `CNXT-90b73131-5460-4d0d-8669-2bc86a544754`;
- run `a2ea6b32-fd1a-4235-a6c5-820d475ea4cc`.

Do not repair or rewrite this failed Ticket manually. It is preserved evidence.

## Successor authorization

No new semantic message is authorized yet.

A source/test-only successor must first prove and repair the exact Dashboard durable-final-payload staging boundary with TDD, while preserving authenticated owner admission, Ticket-before-provider ordering, exact delivery ownership and no-regeneration guarantees.

Only after that source repair is independently accepted may a separately authorized supported install-over update the live plugin, followed by a new final fresh-session semantic acceptance with one new nonce/message.
