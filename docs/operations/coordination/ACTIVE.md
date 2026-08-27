# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_AND_READ_ONLY_LIVE_DASHBOARD_STAGING_DIAGNOSIS`
Current authorization: `OPERATOR_APPROVED_DIAGNOSIS_ONLY_NO_SEMANTIC_RESEND`
Task ID: `CNX-20260827-103`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Operator approval

The operator explicitly approved the bounded Task-103 diagnosis design after Task 102 reproduced the live durable-staging blocker.

No operator action is expected during Task 103. If a diagnostic step unexpectedly requires manual focus/click/authentication/send/restart or another operator mutation, the executor must stop before that step and report the exact required operator action.

## Task 102 accepted blocker

Task 102 report:

`4d23875f4c402cf47109439ebd6b6b5eb72e131b`

Independent disposition:

`ACCEPT_BLOCKER_LIVE_DURABLE_PAYLOAD_STAGING_REPRODUCED_AFTER_REPAIR`

Task 102 removed the Dashboard input ambiguity and proved the operator-assisted input method. Its one semantic Send produced exactly one new Ticket, one expected `ollama/qwen3.5:9b` Direct inference and one visible exact nonce reply, but durable staging remained absent:

- Ticket `CNXT-415b82d9-5553-4bd2-996a-54f57163f7e4`;
- `response_ready_at` present;
- `delivery_confirmed_at = null`;
- `cnx_assistant_delivery = 0`;
- no `delivery_confirmed`;
- no `completed`.

Task-102 semantic artifacts are retired. Do not resend, replay, repair or clean them.

## Active Task 103

[`tasks/CNX-20260827-103-diagnose-live-dashboard-staging-boundary.md`](tasks/CNX-20260827-103-diagnose-live-dashboard-staging-boundary.md)

Goal: identify the first exact failing boundary that allows visible Dashboard delivery without creating the durable `cnx_assistant_delivery` staging row.

Task 103 must diagnose, not fix, the boundary among:

- installed/source/dist/runtime payload mismatch;
- verified-delivery installer not registered;
- real Dashboard path bypassing `reply_dispatch`;
- real `reply_dispatch` event/context shape differing from the unit-test mock;
- final-payload/cardinality/session/correlation filter skipping staging;
- staging function/write failing before durable commit.

Required evidence includes:

- repository source -> build/dist -> packed payload -> installed live plugin -> active release-entry parity;
- exact OpenClaw `2026.7.1-2 (0790d9f)` hook/runtime/type contract;
- read-only correlation against the preserved Task-102 run/log window;
- a production-shaped source-only/disposable reproduction through the real release registration boundary where safely possible;
- explicit H1-H6 disposition and one root-cause token or `BLOCKED_ROOT_CAUSE_NOT_YET_ISOLATED`.

## Accepted live baseline

Exact installed source:

`32212a4331e1f32b5a130bd30d271d4cbc56f6c1`

Exact installed plugin fingerprint:

`df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`

Expected live state remains MANAGED generation 24 with accepted startup/Supervisor/Gateway/SQLite/Ollama health.

## Hard fence

Task 103 authorizes read-only live/runtime/source inspection and disposable isolated diagnostic harnesses only.

It does **not** authorize:

- a new semantic nonce or Dashboard Send;
- sent sentinel or Task-102 replay;
- direct provider probe;
- synthetic live Ticket;
- live SQLite/config/runtime mutation;
- maintained product-source/test fix;
- install/install-over/uninstall/reset/cleanup;
- session cleanup/normalization;
- model/provider/timeout change;
- Gateway/Supervisor restart or reboot;
- credential/token/password access or re-entry;
- merge/tag/release/force push.

After root cause is proven, Task 103 must report a minimal successor repair design and stop. Implementation requires a separate approved task.