# Active Coordination Task

Status: `AWAITING_OPERATOR_DESIGN_APPROVAL`
Execution mode: `SOURCE_AND_READ_ONLY_LIVE_DASHBOARD_STAGING_DIAGNOSIS_PENDING_APPROVAL`
Current authorization: `NO_NEW_SEMANTIC_SEND_AUTHORIZED`
Task ID: `PENDING_CNX-20260827-103`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator design approval

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Task 102 independent review

Task 102 report:

`4d23875f4c402cf47109439ebd6b6b5eb72e131b`

Independent decision:

`ACCEPT`

Disposition:

`ACCEPT_BLOCKER_LIVE_DURABLE_PAYLOAD_STAGING_REPRODUCED_AFTER_REPAIR`

Review:

[`reviews/CNX-20260827-102-reestablish-dashboard-target-and-final-semantic-acceptance.md`](reviews/CNX-20260827-102-reestablish-dashboard-target-and-final-semantic-acceptance.md)

Publication fence is valid: execution `9b9cb77b77f3e4e57887c4ffa87a0cd273e4ef55` -> report `4d23875f4c402cf47109439ebd6b6b5eb72e131b` is one report-only commit.

## What Task 102 proved

The real Dashboard input path is now known and reproducible with bounded operator assistance:

1. open the authenticated Firefox Dashboard and freshly correlate exact HWND/session/composer;
2. prove the Firefox HWND is foreground;
3. operator manually clicks the already-verified `Message Assistant` composer once with the real mouse;
4. re-verify foreground/session/composer;
5. only then use foreground keystrokes;
6. visually verify exact text before any authorized Send.

Task 102 earned:

`DASHBOARD_INPUT_METHOD_REPRODUCIBLY_PROVEN`

The one semantic Send created exactly one Ticket and one expected provider call and visibly rendered the exact nonce once. It then stopped correctly because durable staging did not occur:

- Ticket `CNXT-415b82d9-5553-4bd2-996a-54f57163f7e4`;
- `response_ready_at` present;
- `delivery_confirmed_at = null`;
- `cnx_assistant_delivery = 0`;
- no `delivery_confirmed`;
- no `completed`.

No resend or duplicate semantic effect occurred.

## Pending Task 103 bounded diagnosis design

The next task is diagnosis-only: no product fix and no semantic resend.

It should establish the exact live boundary among:

- verified-delivery installer not active in the loaded runtime;
- `reply_dispatch` not emitted on the real Dashboard delivery path;
- emitted event/context lacks the run/dispatcher shape modeled by tests;
- hook receives the event but payload/session/cardinality/correlation checks skip staging;
- staging is attempted but errors before durable commit.

Required evidence should include source/dist/release-entry parity, actual active plugin entry/wiring, read-only Task-102 run/log correlation, and a production-shaped source-only reproduction using the real release registration path rather than calling the installer directly.

No operator action is required during this diagnosis-only task.

## Accepted live baseline

Exact installed source:

`32212a4331e1f32b5a130bd30d271d4cbc56f6c1`

Exact installed plugin fingerprint:

`df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`

Live baseline remains MANAGED generation 24 with accepted startup/Supervisor/Gateway/SQLite/Ollama health.

## Hard fence pending approval

Until Task 103 is approved:

- no new semantic nonce or Send;
- do not reuse Task-102 nonce;
- no provider probe;
- no install/reset/cleanup;
- no product-source fix;
- no SQLite/history mutation;
- no session normalization;
- no credential access/re-entry;
- no restart/reboot/tag/release/force push.

If a later live retest requires operator help, coordination must explicitly tell the operator when to open/keep Firefox foreground, when to click the exact composer once, and when/if to perform the single authorized Send.