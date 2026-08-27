# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_READ_ONLY_CONTROL_UI_OWNER_AUTH_PROOF`
Current authorization: `BOUNDED_LOCAL_CONTROL_UI_AUTH_AND_PAIRING_PROOF_AUTHORIZED`
Task ID: `CNX-20260827-091`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260827-091-prove-dashboard-owner-surface-without-secret-disclosure.md`](tasks/CNX-20260827-091-prove-dashboard-owner-surface-without-secret-disclosure.md)

## Task 090 accepted blocker

Task 090 report:

`c2d6f2586b32ebec6a57ebb487d924a3ec3101a4`

Independent review:

Decision: `ACCEPT`

Disposition:

`ACCEPT_BLOCKER_OWNER_SURFACE_READINESS_AFTER_LIVE_RECOVERY_PASS`

Review:

[`reviews/CNX-20260827-090-live-pending-rollover-recovery-retry-after-published-boundary-fix.md`](reviews/CNX-20260827-090-live-pending-rollover-recovery-retry-after-published-boundary-fix.md)

Publication fence is accepted: execution `482223de...` -> report `c2d6f258...` is exactly one report-only commit.

## Accepted live state from Task 090

The live recovery portion is complete and accepted:

- exact installed source `d6daf8f93fcd5578f267b2017c6cc82e5de20095`;
- controller MANAGED, generation 18;
- startup enabled;
- Supervisor Ready;
- AGENTS managed block restored;
- canonical plugin generations converged `2 -> 1`;
- surviving generation is existing source-exact `g-7257c4555ca8ad21`;
- no third generation was created;
- plugin loaded/enabled `0.9.3` and fingerprint matches exact source;
- normalized skill parity `86/86`;
- ownership verification passed;
- product-owned runtime/launcher/Supervisor restored;
- Gateway healthy on `127.0.0.1:18789`;
- Ollama accepted four-model inventory preserved;
- SQLite integrity `ok`, Tickets/outbox zero;
- exactly one supported installer invocation, retry count zero;
- zero semantic messages/provider probes;
- `NO_FLASH_MULTI_TICK_PROVEN` from five natural PT1M observations.

Do not reinstall, reset or manually normalize this accepted state.

## Remaining blocker

Task 090 could load the Control UI page but could not prove an authenticated owner/admin WebSocket connection without handling the Gateway shared credential.

Therefore `DASHBOARD_OWNER_SURFACE_READY` remains unproven.

This does not invalidate live recovery/parity/no-flash acceptance.

## Task 091 requirements

Task 091 must inspect exact installed OpenClaw `2026.7.1-2` before choosing the owner-auth path. It must not assume newer documentation behavior.

It must prove a real localhost Dashboard/WebChat Control UI connection authenticated with the installed supported operator/admin authority while disclosing zero shared-secret material.

Priority:

1. reuse an already-paired localhost Control UI device if valid;
2. otherwise use the exact installed build's supported local owner-handoff/pairing mechanism if it can operate without exposing reusable credentials;
3. if a fresh pairing is required, approve only one exactly correlated localhost Control UI request with expected role/scopes;
4. if only shared-secret entry is possible, an ephemeral local in-memory handoff is allowed only if the value is never printed, persisted, placed in captured command lines/clipboard/report, and the actual Control UI identity/scopes are independently proven;
5. otherwise fail closed.

Required readiness proof:

- actual Control UI/WebChat client identity;
- authenticated Gateway connection, not HTTP reachability only;
- effective operator/admin role/scopes matching installed owner derivation;
- at least one read-only RPC succeeds;
- zero `chat.send`, semantic content, provider inference, Ticket/outbox mutation;
- future fresh Dashboard session behavior identified without sending.

Accepted readiness tokens:

- `DASHBOARD_OWNER_SURFACE_READY`, or
- `DASHBOARD_OWNER_SURFACE_READY_FIRST_SEND_CREATES_SESSION` only when admin/owner authentication is independently proven and the installed UI creates a session only on first send.

## Secret fence

Never print/log/copy/report the Gateway token/password. Do not run `openclaw gateway auth-token --show`. Do not store a credential-bearing URL. Do not publish a hash of the secret.

## Semantic/product fence

No Dashboard/WebChat composer send, `chat.send`, `chat.inject`, `openclaw agent`, `sessions_send`, channel send, synthetic Ticket, direct Ollama call, final nonce, provider/model/timeout change, install/install-over/uninstall/reset/cleanup, CNX repair, SQLite edit, reboot, merge/tag/release.

A single supported device approval is authorized only when exactly correlated to the fresh localhost Control UI request. Prefer no pairing mutation when an existing valid device is available.

## Successor gate

Only independent acceptance of:

`PASS_DASHBOARD_OWNER_SURFACE_READY_NO_SECRET_DISCLOSURE`

may authorize the final one-message authenticated Dashboard/WebChat semantic acceptance task.
