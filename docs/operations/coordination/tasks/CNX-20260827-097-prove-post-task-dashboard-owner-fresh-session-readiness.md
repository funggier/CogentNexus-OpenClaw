# CNX-20260827-097 — Prove Post-Task Dashboard Owner Fresh-Session Readiness

Status: `READY_FOR_HERMES`

Execution mode: `READ_ONLY_AUTHENTICATED_DASHBOARD_FRESH_SESSION_READINESS`

Current authorization: `TASK096_POST_REPORT_OWNER_READINESS_PROOF_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Independently prove the current OpenClaw Dashboard/WebChat owner surface is authenticated and ready to enter a genuinely fresh New Chat state **without sending any semantic message**.

This task exists because Task 096 completed and published its report before the operator successfully entered the OpenClaw token. After Task 096 had ended, the operator manually entered the token and reported that the Dashboard is now accessible.

Do not rewrite the Task-096 report. Treat the current authenticated browser state as new post-report evidence.

## Accepted predecessor

Task 096 report:

`d397396fd5d688d84c16d90e8be622e1f59b1411`

Independent Task-096 disposition:

`ACCEPT_BLOCKER_OWNER_SURFACE_READINESS_SNAPSHOT_ONLY`

Task 096 already accepted the live deployment portion:

- exact installed source `32212a4331e1f32b5a130bd30d271d4cbc56f6c1`;
- final plugin fingerprint `df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`;
- one candidate-exact generation;
- MANAGED generation 24;
- Gateway/SQLite/Ollama/startup/Supervisor health;
- Task-092 retired evidence preserved;
- zero Task-096 semantic/provider activity;
- `NO_FLASH_MULTI_TICK_REPROVEN`.

Task 097 must not reinstall or repair anything.

---

# Absolute fence

Task 097 is readiness-only.

Allowed:

- read-only Gateway/controller/SQLite/session/device/log inspection;
- inspection of the already-open authenticated Dashboard/WebChat browser state;
- use of read-only Control UI RPC such as `sessions.list` or equivalent;
- one UI transition into **New Chat / fresh staged session state**, provided no user/assistant message is sent and no provider inference is triggered.

Forbidden:

- reading, printing, copying, logging, persisting, requesting, exporting or re-entering the Gateway token/password;
- `chat.send`, `chat.inject`, `openclaw agent`, `sessions_send`, channel sends or any semantic content send;
- generation of a semantic nonce;
- direct Ollama/provider inference/probe;
- install/install-over/uninstall/reset/cleanup;
- plugin generation/controller/startup/Supervisor/AGENTS/config/runtime/SQLite mutation;
- Task-092 evidence repair/rewrite;
- provider/model/timeout changes;
- restart/reboot;
- merge/tag/release/force push.

If the authenticated browser session disappears or requires secret re-entry by the executor, stop. Do not request the secret from the operator.

---

# Gate A — baseline snapshot

Before interacting with New Chat, record read-only evidence for:

- controller remains `managed`, generation 24;
- Gateway probe healthy;
- final installed plugin still resolves to exact fingerprint `df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`;
- SQLite integrity `ok`;
- current Ticket/outbox counts and exact Task-092 retired Ticket identity/status;
- no provider activity attributable to Task 097.

Do not assume ticket count is zero.

---

# Gate B — authenticated owner/control proof

Using the already authenticated browser/Gateway state, prove all of:

1. the OpenClaw Control UI is actively connected to the local Gateway;
2. the client is the Dashboard/WebChat control surface, not an arbitrary CLI session-key invocation;
3. authenticated role/scope includes the owner/operator control capability required for normal Dashboard chat operation (for example operator/admin/read scopes as exposed by this OpenClaw version);
4. at least one read-only RPC succeeds over that authenticated connection, preferably `sessions.list` or an equivalent supported read operation;
5. no token/password value is exposed in evidence.

Evidence may come from supported UI state plus Gateway connection/device/session metadata or logs. Redact any credential-bearing material before report publication.

If authenticated owner/control identity cannot be correlated to the current browser connection, stop with:

`BLOCKED_DASHBOARD_OWNER_AUTH_UNPROVEN`.

---

# Gate C — fresh-session readiness with zero send

Prove the exact user-facing New Chat behavior that previously had edge cases.

1. Snapshot the currently selected session/chat identity and visible transcript state.
2. Use the actual authenticated Dashboard/WebChat **New Chat** control once.
3. Do not send any message.
4. Prove the UI enters a fresh/staged empty-chat state rather than silently falling back to the previous Main/existing session.
5. Prove no `unknown parent session`, stale-parent, reconnect error or hidden fallback is emitted by the Gateway/UI.
6. If this OpenClaw version materializes a durable session only on first send, record that behavior explicitly; do not fabricate a session id before it exists.
7. Re-run read-only `sessions.list`/equivalent and correlate the result to the UI behavior without requiring a send.
8. Snapshot Ticket/outbox/provider state after the New Chat transition and prove no semantic/provider effect occurred.

Required readiness token:

`DASHBOARD_OWNER_FRESH_SESSION_READY_NO_SEND`

This token means only that authenticated fresh-session entry is ready for a first semantic send. It does **not** claim final semantic acceptance.

---

# Gate D — post-readiness health

After the New Chat readiness proof, verify read-only:

- controller remains MANAGED generation 24;
- Gateway probe healthy;
- plugin fingerprint unchanged;
- SQLite integrity ok;
- Task-092 retired evidence unchanged;
- Ticket/outbox counts unchanged from Task-097 baseline;
- zero provider inference during Task 097.

---

# Publication fence

No product source commit is expected.

Publish exactly one report-only commit:

`docs/operations/coordination/reports/CNX-20260827-097-prove-post-task-dashboard-owner-fresh-session-readiness.md`

Required result tokens:

- `PASS_DASHBOARD_OWNER_FRESH_SESSION_READY_NO_SEND`
- `BLOCKED_DASHBOARD_OWNER_AUTH_UNPROVEN`
- `BLOCKED_FRESH_SESSION_ENTRY_FAILURE`
- `BLOCKED_UNEXPECTED_SEMANTIC_OR_PROVIDER_EFFECT`
- `BLOCKED_LIVE_HEALTH_REGRESSION`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Successor gate

Only independent acceptance of:

`PASS_DASHBOARD_OWNER_FRESH_SESSION_READY_NO_SEND`

may authorize the final authenticated fresh-session semantic acceptance.

That final task must use one brand-new nonce exactly once through this Dashboard/WebChat owner surface; prove the first sent message creates/uses a genuinely fresh session; prove Ticket acceptance and routing occur before Ollama; prove final assistant payload is durably staged before native delivery; prove visible exact nonce once; settle the exact Ticket/run to `delivery_confirmed` then `completed`; and finally enter New Chat again without another send or stale-parent/provider effect.
