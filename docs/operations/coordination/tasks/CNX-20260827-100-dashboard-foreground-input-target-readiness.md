# CNX-20260827-100 — Dashboard Foreground Input-Target Readiness

Status: `READY_FOR_HERMES`

Execution mode: `READ_ONLY_DASHBOARD_FOREGROUND_INPUT_TARGET_READINESS`

Current authorization: `TASK099_ACCEPTED_BOUNDED_FOREGROUND_READINESS_APPROVED`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Prove that the exact authenticated OpenClaw Firefox Dashboard window for the accepted fresh/empty target session can be identified, made the actual Windows foreground input target, and its intended chat composer can be focused/selected while remaining empty — without generating a semantic nonce and without sending semantic content.

This task exists because Task 099 passed semantic preflight/session identity but stopped before send when a different Firefox window/process remained foreground. This is an OS/UI input-target readiness problem, not evidence of a CogentNexus semantic-pipeline regression.

## Accepted predecessor state

Task 096 accepted live deployment:

- exact installed source `32212a4331e1f32b5a130bd30d271d4cbc56f6c1`;
- exact installed plugin fingerprint `df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`;
- MANAGED generation `24`;
- one candidate-exact canonical plugin generation;
- startup/Supervisor/Gateway/SQLite/Ollama healthy;
- Task-092 retired evidence preserved;
- `NO_FLASH_MULTI_TICK_REPROVEN`.

Task 098 accepted authenticated fresh-session readiness with zero semantic/provider effect.

Task 099 report:

`d5fde8d5f1e5968a1ae5ce11f4017a15d9884dac`

Task 099 independent disposition:

`ACCEPT_BLOCKER_DASHBOARD_WINDOW_FOREGROUND_TARGETING_BEFORE_SEND`

Exact target session recorded by Task 099:

`agent:main:dashboard:89992501-1b33-46cf-85f7-eb0c1ef4d311`

Task 099 semantic send count was `0`; its generated nonce is retired and must not be reused.

## Historical control comparison

Task 092 previously proved the authenticated Dashboard send path can execute through a real fresh Dashboard session: one semantic send, one Ticket, accepted/routed before one `ollama/qwen3.5:9b` inference, and one exact visible nonce response. Task 092 failed later at durable delivery completion. Task 093 repaired the staging defect and Task 096 installed that repaired source live.

Task 100 must therefore focus only on the foreground/input-target boundary and must not redesign or repair the semantic pipeline.

---

# Absolute fence

Task 100 is readiness-only.

Allowed:

- read-only controller/Gateway/SQLite/session/device/log/window/process inspection;
- inspection of the already-authenticated Firefox OpenClaw Dashboard;
- read-only Windows window enumeration including HWND, PID, title/class and foreground-window identity;
- low-impact window activation/bring-to-front/focus operations under retry policy v1;
- focus/select the intended OpenClaw Dashboard composer, provided no semantic text is typed and no send occurs.

Forbidden:

- generating a semantic nonce;
- typing semantic test text into the composer;
- sending any user message;
- `chat.send`, `chat.inject`, `openclaw agent`, `sessions_send`, channel sends;
- direct Ollama/provider inference/probe;
- install/install-over/uninstall/reset/cleanup;
- plugin generation/controller/startup/Supervisor/AGENTS/config/runtime/SQLite mutation;
- deleting/renaming/normalizing Dashboard sessions;
- Task-092/Task-099 evidence repair or rewrite;
- provider/model/timeout changes;
- restart/reboot;
- merge/tag/release/force push;
- reading, copying, printing, logging, requesting or re-entering token/password values.

If credential re-entry is required by the executor, stop.

---

# Retry policy v1

Read-only operations may use up to 3 attempts total.

Low-impact focus/window-activation actions may use at most 2 attempts total.

A second activation attempt is allowed only after:

1. a bounded grace interval of at least 3 seconds;
2. fresh `GetForegroundWindow`/equivalent foreground evidence;
3. fresh window inventory/session/UI evidence;
4. proof that attempt 1 did not already acquire the intended foreground target or create any other state change.

If attempt 1 takes effect during verification, count it as success and do not re-issue.

If foreground state is ambiguous, multiple candidate Firefox windows cannot be disambiguated, or input focus is only partially/verifiably changed, stop rather than adding another action.

Semantic send remains unauthorized in Task 100.

---

# Gate A — fresh baseline and exact target preservation

Before any focus/activation action:

1. record coordination execution HEAD;
2. prove Task 099 report/review are ancestors and publication fence remains valid;
3. verify exact OpenClaw build remains `2026.7.1-2 (0790d9f)`;
4. verify controller remains MANAGED generation 24;
5. verify one canonical loaded/enabled plugin with exact accepted fingerprint;
6. verify Gateway healthy and SQLite integrity `ok`;
7. snapshot Ticket/event/outbox/direct-delivery/workflow counts that exist;
8. prove no active semantic/provider operation;
9. prove the accepted target session still exists:
   `agent:main:dashboard:89992501-1b33-46cf-85f7-eb0c1ef4d311`;
10. prove that target remains Dashboard-owned, authenticated, empty/staged, distinct from Main/Task-092, with no new semantic history.

If target is no longer empty/staged or identity is ambiguous, stop with:

`BLOCKED_TARGET_SESSION_NO_LONGER_FRESH`.

---

# Gate B — exact Firefox/OpenClaw window correlation

Enumerate visible Firefox top-level windows/processes without accessing credentials.

For the intended OpenClaw Dashboard window, correlate as many non-secret signals as available:

- HWND;
- process ID;
- executable identity `firefox.exe`;
- window title/class;
- visible Dashboard/OpenClaw UI state;
- browser URL/session UI state when safely observable without secrets;
- target session identity from rendered/read-only session state.

Require a unique candidate window that can be tied to the exact target session.

A generic Firefox process/window match is insufficient when multiple Firefox windows exist.

If unique correlation cannot be established, stop with:

`BLOCKED_DASHBOARD_WINDOW_IDENTITY_AMBIGUOUS`.

---

# Gate C — foreground acquisition

Record current foreground HWND/PID before activation.

If the exact OpenClaw Dashboard HWND is already foreground, do not activate again.

Otherwise perform one bounded foreground/activation attempt using a supported Windows/UI action. Do not type or send anything.

After the action, wait and re-read the actual foreground HWND/PID.

Success requires:

- `GetForegroundWindow`/equivalent equals the exact correlated OpenClaw Dashboard HWND;
- selected target session remains exact and empty/staged;
- no extra session/Ticket/provider effect occurs.

If attempt 1 is unverifiable, apply retry policy v1 exactly. No third attempt exists.

Blockers:

`BLOCKED_DASHBOARD_WINDOW_FOREGROUND_NOT_ACQUIRED`

`BLOCKED_FOREGROUND_RETRY_NOT_ELIGIBLE`

---

# Gate D — composer focus readiness with zero text

Only after exact OpenClaw HWND is proven foreground:

1. identify the intended Dashboard chat composer/control for the selected target session;
2. prove the selected session is still `agent:main:dashboard:89992501-1b33-46cf-85f7-eb0c1ef4d311`;
3. focus/select the composer using a low-impact UI action;
4. do not type any semantic/test string;
5. prove composer remains empty;
6. prove focus/selection belongs to the intended foreground OpenClaw window rather than another Firefox window/process;
7. prove no Send action occurs.

If composer focus cannot be proven without typing, stop with:

`BLOCKED_DASHBOARD_COMPOSER_FOCUS_UNPROVEN`.

Required readiness token:

`DASHBOARD_FOREGROUND_COMPOSER_READY_NO_SEND`

Required task PASS token:

`PASS_DASHBOARD_FOREGROUND_INPUT_TARGET_READY_NO_SEND`

---

# Gate E — post-readiness preservation

Verify read-only after focus readiness:

- exact target session remains empty/staged;
- semantic send count remains 0;
- Ticket/event/outbox/delivery/provider counts unchanged from baseline except non-semantic UI/session-selection metadata;
- no provider inference occurred;
- controller remains MANAGED generation 24;
- plugin fingerprint unchanged;
- Gateway healthy;
- SQLite integrity `ok`;
- no plugin generation/recovery churn;
- no credential value exposed.

---

# Publication fence

No product-source commit is expected.

Publish exactly one report-only commit:

`docs/operations/coordination/reports/CNX-20260827-100-dashboard-foreground-input-target-readiness.md`

Required result tokens:

- `PASS_DASHBOARD_FOREGROUND_INPUT_TARGET_READY_NO_SEND`
- `BLOCKED_TARGET_SESSION_NO_LONGER_FRESH`
- `BLOCKED_DASHBOARD_WINDOW_IDENTITY_AMBIGUOUS`
- `BLOCKED_DASHBOARD_WINDOW_FOREGROUND_NOT_ACQUIRED`
- `BLOCKED_FOREGROUND_RETRY_NOT_ELIGIBLE`
- `BLOCKED_DASHBOARD_COMPOSER_FOCUS_UNPROVEN`
- `BLOCKED_UNEXPECTED_SEMANTIC_OR_PROVIDER_EFFECT`
- `BLOCKED_LIVE_HEALTH_REGRESSION`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Successor gate

Only independent acceptance of:

`PASS_DASHBOARD_FOREGROUND_INPUT_TARGET_READY_NO_SEND`

may authorize a new final semantic acceptance task.

That successor must generate a brand-new nonce only after re-verifying exact target session + exact foreground Dashboard HWND + empty focused composer, then send exactly one semantic user message with no resend. It must prove Ticket-before-provider ordering, one correlated Ollama inference, durable final payload staging before native delivery, one exact visible nonce, exact `response_ready -> delivery_confirmed -> completed`, no duplicate semantic effect, and post-completion New Session continuity under state-gated retry policy for session-management only.