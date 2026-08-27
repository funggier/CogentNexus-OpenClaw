# Review — CNX-20260827-091 Prove Dashboard Owner Surface Without Secret Disclosure

Decision: `ACCEPT`

Disposition: `ACCEPT_DASHBOARD_OWNER_SURFACE_READY_NO_SECRET_DISCLOSURE`

Reviewed report HEAD:

`7390ae46dd61686e8d704f93043ead7fe7b9ca1e`

Execution HEAD:

`4f707b14a465e9130187629be160934ed6208e23`

## Publication fence

Accepted.

- Execution -> report is exactly one commit.
- The only changed file is `docs/operations/coordination/reports/CNX-20260827-091-prove-dashboard-owner-surface-without-secret-disclosure.md`.
- No product/source/config/runtime mutation is present in repository history for Task 091.

## Accepted owner-surface evidence

Task 091 proved an actual authenticated localhost OpenClaw Control UI/WebChat connection rather than HTTP reachability alone.

Accepted non-secret identity evidence:

- client `openclaw-control-ui`;
- mode `webchat`;
- role `operator`;
- effective scopes include `operator.admin`, `operator.read`, `operator.write`, `operator.approvals`, `operator.pairing`;
- successful authenticated `sessions.list` read-only RPC;
- existing paired Firefox browser profile reused;
- pending pairing requests remained zero;
- no shared token/password value was read, copied, entered, logged, persisted or reported.

Installed OpenClaw `2026.7.1-2` source/runtime inspection binds the authenticated admin/operator scope to the same owner/admin invariant used by the normal WebChat agent lifecycle. This closes the Task-090 owner-surface blocker without weakening authentication policy or substituting an owner-looking CLI session key.

Accepted readiness token:

`DASHBOARD_OWNER_SURFACE_READY`

## Fresh-session finding

Task 091 also established the exact installed UI contract that a new Dashboard/WebChat session is materialized by the first non-command message. Therefore it was correct not to fabricate a session by CLI or send content during the read-only readiness task.

Accepted preparatory token:

`DASHBOARD_OWNER_SURFACE_READY_FIRST_SEND_CREATES_SESSION`

This token proves the installed contract and readiness only. It does **not** independently prove that a fresh session can be opened and used end-to-end without stale-parent/session-lifecycle regressions.

The operator explicitly requested that final acceptance include real fresh-session behavior because prior testing had exposed new-session edge cases. Independent review therefore adds a mandatory fresh-session gate to the final semantic successor.

## Preserved live state

Task 091 preserved the accepted Task-090 MANAGED installation:

- controller MANAGED;
- one canonical loaded source-exact plugin;
- Supervisor healthy;
- Gateway/Ollama healthy;
- SQLite integrity `ok`;
- Tickets/outbox zero;
- Task-090 `NO_FLASH_MULTI_TICK_PROVEN` remains accepted;
- Task-091 semantic messages/provider calls remained zero.

## Successor authorization

Task 091 releases the authenticated Dashboard/WebChat owner surface for exactly one separately fenced final semantic acceptance attempt.

The final task must test the real **fresh-session** path, not an existing Main Session and not CLI `agent:main:main`:

1. snapshot existing sessions and durable counts;
2. invoke the real Control UI New Session/New Chat action before any semantic send;
3. fail before sending if the UI reports stale/unknown parent or cannot enter a fresh staged state;
4. generate a new nonce only at execution time;
5. send exactly one first non-command owner message through that fresh Control UI state;
6. prove a new session ID/key is materialized and is distinct from existing Main/history and the retired Task-076 session;
7. prove the fresh transcript contains no inherited semantic history;
8. prove Ticket acceptance and routing precede correlated provider inference;
9. prove one visible exact nonce response and lifecycle convergence through `response_ready -> delivery_confirmed -> completed`;
10. do not accept a visible reply while the Ticket remains `accepted` or `response_ready`;
11. prove no duplicate route/provider/resume/outbox side effect;
12. after completion, invoke New Session once more **without sending** and prove the UI returns to a fresh staged state without stale/unknown-parent failure and without creating another Ticket/provider call.

No second semantic message or retry is authorized.
