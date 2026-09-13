# CNX-339 — Dashboard End-to-End Durable Lifecycle Acceptance

Status: `BLOCKED_UI_CONTROL_CANNOT_NAVIGATE_DASHBOARD`
Task ID: `CNX-339`
Execution mode: `SINGLE_EXECUTOR`
Executor: `Hermes`
Reviewer: `ChatGPT`

## Verdict

The semantic live test did not occur. The executor could not drive the real Dashboard UI in the open Firefox window to create a fresh session and submit one semantic request. Durable state before and after is identical — no new session, Ticket, Run, Result, Delivery, recovery, or outbox row was created. Controller bytes are unchanged.

## Evidence

### Remote authority (unchanged)

- Branch: `agent/v0.9.5-plan2-delivery-session-identity`
- Remote HEAD: `0579605f3c56a825bea793919ea55cdd17153769`

### Runtime / controller

- Installed candidate SHA-256: `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8`
- Production controller before: `1cc5b42ba19e5d91620a5c4e754b900d8a986a74a624b0821e5cf363bd673d98`
- Production controller after:  `1cc5b42ba19e5d91620a5c4e754b900d8a986a74a624b0821e5cf363bd673d98`

### Durable before/after counts (read-only SQLite, `integrity_check = ok`)

| Table | Before | After |
|---|---|---|
| cnx_sessions | 26 | 26 |
| tickets | 20 | 20 |
| ticket_events | 834 | 834 |
| cnx_inference_attempt | 0 | 0 |
| cnx_direct_model_call | 17 | 17 |
| cnx_assistant_delivery | 11 | 11 |
| ticket_outbox | 0 | 0 |
| cnx_direct_recovery | 5 | 5 |

New tickets since `2026-09-13T23:40:00Z`: 0
New sessions since `2026-09-13T23:40:00Z`: 0

### UI control attempt

- The open Firefox window (`pid=17040, window_id=3736650`) showed `http://127.0.0.1:18789/chat?session=agent%3Amain%3Adashboard%3A3a29b499-6612-4051-9734-e9d66936ae01`.
- Element index `#53 "New session"` was clicked; the capture after was unchanged and the address bar still showed the same session URL.
- Keystroke/address-bar navigation attempts via `computer_use` were reported `unverifiable` or were routed to a non-Firefox foreground; the URL and rendered page did not change.
- No second click / navigation retry was issued after the first attempt, per the task's one-shot stop rule.

## Root cause

Desktop input from `computer_use` could not reach the Firefox window to perform the required "New session" activation and the typed semantic send. Background input was consistently reported `unverified`, and foreground routing either landed on a different window or left the Dashboard view unchanged. Because durable counts before and after are identical and the visible Dashboard URL/session did not change, no semantic admission, Ticket, Run, Result, Delivery, or Outbox activity occurred.

## Exclusions honored

No retry, recovery, fallback, manual dispatch, alternate transport, second Dashboard session, runtime mutation, provider/model change, controller mutation, plugin lifecycle action, or release/tag mutation occurred.

## Remote state

Remote HEAD remains `0579605f3c56a825bea793919ea55cdd17153769`. The v0.9.5 tag remains `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95`. No semantic traffic occurred on the remote branch.
