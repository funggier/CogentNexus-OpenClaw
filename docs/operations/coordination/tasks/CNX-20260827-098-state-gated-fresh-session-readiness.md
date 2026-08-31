# CNX-20260827-098 — State-Gated Fresh-Session Readiness

Status: `READY_FOR_HERMES`

Execution mode: `READ_ONLY_AUTHENTICATED_DASHBOARD_STATE_GATED_FRESH_SESSION_READINESS`

Current authorization: `TASK097_ACCEPTED_STATE_GATED_RETRY_POLICY_APPROVED`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Establish exactly one unambiguous authenticated Dashboard/WebChat fresh staged session that is safe for the final one-message semantic acceptance, while adopting the operator-approved state-gated bounded retry policy.

Task 098 must not send semantic content. It is a readiness task only.

## Operator-approved retry policy v1

The operator approved limited retries for simple/transient failures when fresh evidence proves retry cannot duplicate a harmful side effect.

Default policy from Task 098 forward:

1. **Read-only operations** — up to `3` attempts total when the operation cannot mutate external state.
2. **Low-impact state-changing operations** — up to `2` attempts total, but attempt 2 is allowed only after a bounded grace period and fresh state verification prove attempt 1 produced no effect.
3. If attempt 1's intended effect appears during the grace/verification phase, count attempt 1 as completed and **do not re-issue** it.
4. Any ambiguous state, partial mutation, delayed effect that cannot be correlated, or already-materialized side effect makes the operation non-retryable.
5. Semantic sends, provider inference, install/install-over/uninstall/reset, destructive cleanup, external side effects and other non-idempotent/high-impact operations remain **single-attempt by default** unless a later task first proves idempotency/zero-side-effect and explicitly authorizes bounded retry.
6. Every retry must record: attempt number, failure/unverifiable reason, grace interval, fresh state before retry, and the exact evidence that makes retry eligible.
7. `unverifiable` means **state unknown**, not `not executed`.

For Dashboard New Session in this task:

- attempt 1 is the normal UI action;
- after any `unverifiable`/transient result, wait at least `5 seconds`, then refresh/re-read session/UI state before deciding;
- attempt 2 is allowed only if session inventory, selected-session identity and UI state prove no new session/staged state resulted from attempt 1;
- if a new session appears during the wait, do not retry;
- if more than one new session or any ambiguous delayed mutation appears, stop rather than adding another click.

## Accepted predecessor state

Task 096 live deployment is independently accepted apart from its historical owner-readiness snapshot blocker.

Exact installed source:

`32212a4331e1f32b5a130bd30d271d4cbc56f6c1`

Installed plugin fingerprint:

`df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`

Controller/live baseline:

- MANAGED generation `24`;
- one candidate-exact canonical plugin generation;
- startup/Supervisor/Gateway/SQLite/Ollama healthy;
- Task-092 retired semantic evidence preserved;
- `NO_FLASH_MULTI_TICK_REPROVEN`.

Task 097 report:

`41a119b686daa4fc64b8f8481329a1be78462641`

Task 097 independent disposition:

`ACCEPT_BLOCKER_STATE_UNVERIFIED_UI_RETRY_DUPLICATED_FRESH_SESSION_ENTRY`

Task 097 proved the Dashboard owner/control surface was authenticated and produced zero semantic/provider effects, but its first delayed New Session click plus immediate re-issue materialized two empty Dashboard sessions. Those sessions are preserved evidence and must not be deleted merely to normalize the test.

---

# Absolute fence

Task 098 is readiness-only.

Allowed:

- read-only Gateway/controller/SQLite/session/device/log inspection;
- inspection of the already-authenticated Dashboard/WebChat UI;
- read-only Control UI RPCs such as `sessions.list`;
- selecting an already-existing Task-097-created empty Dashboard session if that is sufficient to establish a unique readiness target;
- at most one new New Session action plus at most one state-gated retry under the approved policy above, only if current state cannot otherwise establish readiness.

Forbidden:

- reading, printing, copying, logging, requesting or re-entering token/password values;
- any semantic user message or assistant injection;
- `chat.send`, `chat.inject`, `openclaw agent`, `sessions_send`, channel sends;
- generation of a semantic nonce;
- direct Ollama/provider inference/probe;
- install/install-over/uninstall/reset/cleanup;
- plugin generation/controller/startup/Supervisor/AGENTS/config/runtime/SQLite mutation;
- deletion/cleanup/repair of Task-097 duplicate empty sessions;
- repair/rewrite of Task-092 evidence;
- provider/model/timeout changes;
- restart/reboot;
- merge/tag/release/force push.

---

# Gate A — fresh baseline and session inventory

Before any low-impact UI mutation:

1. Fetch/reset coordination branch and record execution HEAD.
2. Verify Task 097 report/review are ancestors and publication fence remains valid.
3. Prove controller remains MANAGED generation 24.
4. Prove installed plugin fingerprint remains exact candidate fingerprint.
5. Prove Gateway healthy and SQLite integrity `ok`.
6. Snapshot Ticket/outbox/event counts and Task-092 retired ticket identity/status.
7. Enumerate current Dashboard sessions through authenticated read-only state/RPC.
8. Identify the two Task-097-created empty sessions if still present, without deleting or renaming them.
9. Record currently selected session identity and whether it has any transcript/user/assistant/provider activity.

## Preferred no-extra-action path

If exactly one currently selected Task-097-created Dashboard session can be unambiguously proven to be:

- distinct from Main Session;
- distinct from Task-092 session/history;
- empty/staged with no user or assistant semantic content;
- owner-authenticated through the current Control UI connection;
- associated with zero new Ticket/outbox/provider activity;

then use that session as the Task-098 readiness target and **do not press New Session again**.

This is preferred because readiness, not session-count normalization, is the goal.

If the current session cannot be proven fresh/empty/unambiguous, continue to Gate B.

---

# Gate B — state-gated New Session action only if needed

Use the actual authenticated Dashboard/WebChat New Session control.

### Attempt 1

1. Snapshot session inventory and selected session immediately before action.
2. Issue the New Session action once.
3. Do not escalate or re-issue immediately if the tool/UI result is `unverifiable`.
4. Wait at least `5 seconds`.
5. Re-read UI URL/state and authenticated `sessions.list` or equivalent.

### Decision after grace period

- If one new fresh session/staged state is now visible and correlatable: attempt 1 succeeded; no retry.
- If no session/state change occurred and fresh evidence proves zero effect: attempt 2 may be used once.
- If the first effect appears late, more than one session appears, selected identity changes ambiguously, or any partial effect exists: do **not** retry; stop with blocker.

### Attempt 2 — only if eligible

1. Record why attempt 1 is proven effect-free.
2. Re-issue New Session once.
3. Wait and verify state again.
4. No third attempt exists.

At completion, exactly one session must be selected as the readiness target. Other preserved empty Task-097 evidence may still exist; they need not be removed.

---

# Gate C — readiness target proof

For the chosen readiness target, prove all of:

1. Dashboard/WebChat owner/control surface is actively authenticated.
2. A supported read-only RPC succeeds over the same authenticated connection.
3. Target session identity is a Dashboard session and is distinct from Main Session and Task-092 retired semantic session/history.
4. Target transcript is empty/staged before first semantic send.
5. No stale/unknown-parent/reconnect/fallback error is active.
6. Ticket/outbox/event/provider state did not change due to readiness operations.
7. No semantic content/provider inference occurred in Task 098.

Required readiness token:

`DASHBOARD_OWNER_FRESH_SESSION_READY_NO_SEND`

Required task PASS token:

`PASS_STATE_GATED_DASHBOARD_FRESH_SESSION_READY_NO_SEND`

---

# Gate D — post-readiness health

Verify read-only:

- controller remains MANAGED generation 24;
- plugin fingerprint unchanged;
- Gateway healthy;
- SQLite integrity ok;
- Task-092 retired evidence unchanged;
- Ticket/outbox/event counts unchanged from Task-098 baseline except session-management metadata that is explicitly non-semantic;
- zero provider inference;
- no plugin generation or recovery churn.

---

# Publication fence

No product-source commit is expected.

Publish exactly one report-only commit:

`docs/operations/coordination/reports/CNX-20260827-098-state-gated-fresh-session-readiness.md`

Required result tokens:

- `PASS_STATE_GATED_DASHBOARD_FRESH_SESSION_READY_NO_SEND`
- `BLOCKED_DASHBOARD_OWNER_AUTH_UNPROVEN`
- `BLOCKED_FRESH_TARGET_AMBIGUOUS`
- `BLOCKED_STATE_GATED_RETRY_NOT_ELIGIBLE`
- `BLOCKED_FRESH_SESSION_ENTRY_FAILURE`
- `BLOCKED_UNEXPECTED_SEMANTIC_OR_PROVIDER_EFFECT`
- `BLOCKED_LIVE_HEALTH_REGRESSION`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Successor gate

Only independent acceptance of:

`PASS_STATE_GATED_DASHBOARD_FRESH_SESSION_READY_NO_SEND`

may authorize the final authenticated semantic acceptance.

The final semantic task must still keep the semantic send itself single-attempt: one brand-new nonce, one user send, no resend. It must prove the selected fresh Dashboard session, Ticket acceptance/routing before Ollama, durable final-payload staging before native delivery, one exact visible reply, exact delivery settlement through `delivery_confirmed` to `completed`, and then prove another New Session transition with zero additional semantic/provider effect using the state-gated retry policy for the session-management action only.