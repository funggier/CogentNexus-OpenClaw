# CNX-20260827-091 — Prove Dashboard Owner Surface Without Secret Disclosure

Status: `READY_FOR_HERMES`

Execution mode: `LIVE_READ_ONLY_CONTROL_UI_OWNER_AUTH_PROOF`

Current authorization: `BOUNDED_LOCAL_CONTROL_UI_AUTH_AND_PAIRING_PROOF_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Prove that exact installed OpenClaw `2026.7.1-2` exposes a real authenticated localhost Dashboard/WebChat Control UI owner surface that will enter the normal `chat.send` lifecycle with authenticated admin/operator authority, **without disclosing the Gateway token/password and without sending any semantic message**.

This task preserves the successfully restored MANAGED live state from Task 090 and exists only to close the remaining owner-surface readiness blocker.

This is still not the final semantic acceptance task.

## Accepted predecessor state

Task 090 report:

`docs/operations/coordination/reports/CNX-20260827-090-live-pending-rollover-recovery-retry-after-published-boundary-fix.md`

Report HEAD:

`c2d6f2586b32ebec6a57ebb487d924a3ec3101a4`

Independent review:

Decision: `ACCEPT`

Disposition:

`ACCEPT_BLOCKER_OWNER_SURFACE_READINESS_AFTER_LIVE_RECOVERY_PASS`

Review path:

`docs/operations/coordination/reviews/CNX-20260827-090-live-pending-rollover-recovery-retry-after-published-boundary-fix.md`

Accepted live state now includes:

- controller `managed`, generation 18;
- startup enabled;
- Supervisor Ready;
- AGENTS managed block restored;
- one canonical enabled/loaded CogentNexus plugin `0.9.3`;
- surviving generation `g-7257c4555ca8ad21`;
- exact source/live plugin fingerprint parity;
- normalized skill parity `86/86`;
- ownership verification passed;
- Gateway healthy on loopback;
- Ollama accepted four-model inventory preserved;
- SQLite integrity `ok`;
- Tickets/outbox zero;
- `NO_FLASH_MULTI_TICK_PROVEN` from five natural PT1M runs;
- zero semantic messages/provider probes during Task 090.

Do not reinstall, reset, normalize or otherwise repair this accepted live state during Task 091.

---

# Security model

Task 077 established that choosing an owner-looking session key is not owner authentication. Installed OpenClaw derives the owner signal from authenticated Gateway client scope; CLI `openclaw agent --session-key ...` is not an acceptable substitute.

Task 091 must therefore prove an actual Control UI/WebChat client authenticated as the supported operator/admin owner surface.

## Secret handling rules

The Gateway shared secret is never evidence and must not appear in any artifact.

Do NOT:

- print the Gateway token/password;
- use `openclaw gateway auth-token --show`;
- echo or `Write-Host` any secret value;
- include a token/password in a command line that is captured by process listings or evidence logs;
- save a credential-bearing URL to disk;
- commit a credential-bearing URL;
- paste a secret into report text;
- hash the secret and publish the hash;
- copy a shared secret into evidence or clipboard history merely for convenience;
- change or rotate Gateway authentication merely to make the task pass.

Allowed read-only auth metadata includes only non-secret facts such as:

- auth mode (`token`, `password`, trusted identity mode, etc.);
- whether a configured credential/reference exists;
- whether it is a SecretRef/runtime value when discoverable without resolution;
- sanitized endpoint host/port;
- client/device ID or public identity if it is not itself a bearer secret;
- role/scopes;
- pairing/request IDs;
- authenticated/connected boolean;
- sanitized browser/profile identity correlation.

If exact installed source cannot authenticate a real Control UI without exposing a shared secret to captured evidence, stop with the corresponding blocker rather than weakening policy.

---

# Absolute semantic and product-mutation fence

Task 091 may not send or inject any user/semantic content.

Forbidden:

- `chat.send`;
- `chat.inject`;
- Dashboard/WebChat composer submission;
- `openclaw agent`;
- `sessions_send`;
- channel send;
- synthetic Ticket creation;
- direct Ollama/provider call;
- final nonce generation or consumption;
- model/provider/timeout change;
- install/install-over/uninstall/reset/cleanup;
- plugin generation mutation;
- controller/startup/Supervisor/AGENTS/ownership/runtime/config repair;
- SQLite/Ticket/session transcript edit;
- reboot/merge/tag/release.

### Narrowly authorized auth-side effect

If and only if exact installed OpenClaw requires a new Control UI device pairing/approval, Task 091 may perform **one bounded supported device approval** for the fresh localhost Control UI device after independently proving the request identity and expected role/scopes.

No unrelated device may be approved/revoked/rotated.

If an already-paired valid localhost Control UI browser/device exists, prefer reusing it and make no new pairing mutation.

---

# Phase A — fresh read-only live re-proof

Before authentication work, record:

1. current coordination HEAD;
2. Task-090 report + ACCEPT review ancestry;
3. OpenClaw exact version `2026.7.1-2`;
4. controller remains MANAGED;
5. one canonical loaded CogentNexus plugin;
6. Gateway loopback health;
7. Supervisor Ready and recent natural LastTaskResult=0;
8. SQLite integrity `ok`, Tickets/outbox zero;
9. no current semantic/provider run.

If accepted Task-090 live state materially drifted, stop with:

`BLOCKED_LIVE_STATE_DRIFT_BEFORE_OWNER_AUTH`

Do not repair drift inside Task 091.

---

# Phase B — inspect the exact installed owner-handoff contract

Do not assume behavior from current online documentation or a newer OpenClaw release.

Inspect only the exact installed `2026.7.1-2` build:

1. `openclaw dashboard --help` and related CLI help, with output reviewed for credential-bearing behavior before persistence;
2. installed Control UI/dashboard command source;
3. installed Gateway WebSocket auth/connection source;
4. installed role/scope derivation relevant to Control UI/WebChat;
5. installed device-pairing behavior for localhost browser clients;
6. installed `chat.send` path only by source inspection — do not call it.

Required source conclusions:

- exact supported Dashboard/Control UI entry command/path;
- how localhost Control UI authenticates in this build;
- which role/scopes make `senderIsOwner` / `hasGatewayAdminScope` true;
- whether a CLI owner handoff or browser bootstrap exists;
- whether such handoff contains reusable shared secret material;
- whether first connection requires device pairing;
- whether fresh chat session creation happens before first send or only on first `chat.send`.

Record code locations or command-help evidence, but no credential value.

If installed behavior is ambiguous, stop with:

`BLOCKED_INSTALLED_OWNER_HANDOFF_CONTRACT_AMBIGUOUS`

---

# Phase C — choose the least-secret authentication path

Use this priority order.

## C1 — existing paired localhost Control UI

If a previously paired browser/device is already valid and can be correlated to localhost Control UI:

- reuse it;
- do not expose shared credentials;
- do not re-pair unnecessarily.

## C2 — installed supported one-time/local owner handoff

If exact source proves a supported local Dashboard owner handoff/pairing mechanism that does not expose the reusable shared secret into logs/artifacts:

- use the actual installed supported command/path;
- suppress or sanitize any output before persistence;
- never store a raw bootstrap URL if it contains credential material;
- allow the supported mechanism to open the real localhost Control UI browser profile;
- record only sanitized host/port, expiry/one-time status and non-secret handoff metadata.

## C3 — bounded device approval if required

If the fresh localhost Control UI produces a pairing request:

1. list pending requests through the supported read-only device surface;
2. correlate exactly one request to the just-opened localhost Control UI using request time, client type, device/public identity, role/scopes and other non-secret metadata;
3. require the requested authority to match the installed Control UI operator/admin contract from Phase B;
4. if multiple plausible requests exist or identity is ambiguous, stop;
5. approve only that one request;
6. record request ID + resulting non-secret device ID/role/scopes;
7. do not approve any unrelated request.

Required blocker for ambiguity:

`BLOCKED_PAIRING_IDENTITY_AMBIGUOUS`

## C4 — if only explicit shared-secret entry is possible

Do not expose or log the secret.

A local ephemeral helper may resolve a configured credential **only in process memory** and pass it directly to the actual localhost Control UI authentication path if all of the following are true:

- exact installed source proves this is the supported auth path;
- the value is never printed, persisted, placed in a captured command line, written to clipboard history or report;
- evidence records only success/failure and non-secret metadata;
- the helper does not impersonate the Control UI with a different client identity;
- actual Control UI device identity and role/scopes are still proven after authentication.

If these constraints cannot be met with available local tooling, stop with:

`BLOCKED_OWNER_AUTH_REQUIRES_SECRET_DISCLOSURE`

Do not ask the operator to paste the secret into chat.

---

# Phase D — prove actual authenticated owner scope without sending

After the real Control UI connects, collect read-only evidence proving all of:

1. client is the actual Dashboard/Control UI/WebChat client for exact installed OpenClaw;
2. connection is authenticated, not merely HTTP page reachable;
3. device/client role is the installed supported operator/admin role;
4. effective scopes include the exact admin/owner scope used by installed `hasGatewayAdminScope` / `senderIsOwner` derivation;
5. a read-only RPC such as `chat.history`, `sessions.list`, model status or equivalent succeeds through that authenticated Control UI connection;
6. no write/semantic RPC occurs;
7. no Ticket row, outbox row or provider run appears as a consequence of readiness proof.

Use Gateway logs, device/session metadata and/or read-only UI state to correlate the exact connection. Do not rely solely on the page visually rendering.

Required token if proven:

`DASHBOARD_OWNER_SURFACE_READY`

If connection succeeds but exact owner/admin scope is not independently provable, stop with:

`BLOCKED_OWNER_SCOPE_UNPROVEN`

---

# Phase E — prepare but do not send the future semantic session

Determine the exact next-task session behavior without sending content.

Preferred:

- identify/select a fresh empty Dashboard/WebChat session if exact installed UI supports doing so without `chat.send` or provider inference;
- prove zero user/assistant semantic messages and zero Tickets/provider calls for that session;
- record only non-secret session key/device ID/auth provenance.

The future session must not be:

- Task-076 session `f829224b-064f-4bb4-a845-2955be2a2c7f`;
- generic CLI `agent:main:main` used as an ownership substitute;
- any session with ambiguous prior semantic effects.

If exact installed Control UI creates a session only on the first `chat.send`, do not fabricate one. Record exact readiness token:

`DASHBOARD_OWNER_SURFACE_READY_FIRST_SEND_CREATES_SESSION`

This token is acceptable evidence **only together with** proven authenticated Control UI admin/owner scope from Phase D.

---

# Phase F — preservation checks

Before report publication re-prove read-only:

- controller still MANAGED;
- single canonical loaded plugin remains source-exact;
- Supervisor remains healthy;
- Gateway healthy;
- SQLite integrity `ok`;
- Tickets/outbox remain zero;
- semantic messages = 0;
- provider calls/probes = 0;
- no install/reset/manual CNX repair occurred;
- only allowed new device pairing, if any, occurred.

Do not require another five-minute observation; Task-090 `NO_FLASH_MULTI_TICK_PROVEN` remains accepted unless an auth action unexpectedly mutates Supervisor/runtime state, in which case stop and report drift.

---

# Publication fence

No product source commit is expected.

Publish one report-only commit:

`docs/operations/coordination/reports/CNX-20260827-091-prove-dashboard-owner-surface-without-secret-disclosure.md`

Execution HEAD -> report HEAD must be exactly one report-only commit.

Report must contain:

- execution/report HEADs;
- exact installed OpenClaw version;
- sanitized installed-source owner-auth findings;
- auth mode/presence facts without credential value;
- chosen authentication/handoff path;
- any pairing request/device IDs + role/scopes without bearer credentials;
- proof of actual authenticated Control UI connection;
- exact owner/admin scope evidence;
- read-only RPC evidence;
- fresh-session behavior/readiness token;
- zero semantic/provider/Ticket accounting;
- live MANAGED preservation;
- explicit secret-disclosure accounting = 0;
- publication fence.

Required final result tokens:

- `PASS_DASHBOARD_OWNER_SURFACE_READY_NO_SECRET_DISCLOSURE`
- `BLOCKED_LIVE_STATE_DRIFT_BEFORE_OWNER_AUTH`
- `BLOCKED_INSTALLED_OWNER_HANDOFF_CONTRACT_AMBIGUOUS`
- `BLOCKED_OWNER_AUTH_REQUIRES_SECRET_DISCLOSURE`
- `BLOCKED_PAIRING_IDENTITY_AMBIGUOUS`
- `BLOCKED_OWNER_SCOPE_UNPROVEN`
- `BLOCKED_OWNER_SURFACE_CONNECTION`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Successor gate

Only independent acceptance of:

`PASS_DASHBOARD_OWNER_SURFACE_READY_NO_SECRET_DISCLOSURE`

may authorize the final semantic acceptance task.

That final task may send exactly one fresh authenticated Dashboard/WebChat owner message and must use one new nonce generated only at execution time. It must prove durable Ticket acceptance/routing before correlated provider inference, response-ready, exact owner/run delivery confirmation, completed state and exactly one visible nonce response. It must never reuse Task-076 nonce/session and must never substitute CLI `openclaw agent --session-key agent:main:main` for the owner surface.
